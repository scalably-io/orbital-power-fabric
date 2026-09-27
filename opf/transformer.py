"""Transformer operator map for decode (one new token), from a model config.json.

Classes that matter for photonics:
  static   - activation x fixed weight (projections, MLP, LM head): a photonic
             mesh can hold the weights, but only a tiny slice of a 70B model fits
             on any mesh, so weights must be reloaded -> weight-loading energy/time.
  dynamic  - activation x activation (QK^T, attention x V): both operands change
             every token; no weight-stationary benefit.
  nonlinear- softmax, SiLU, RMSNorm: electronic today.
Memory traffic per token (weights / batch + KV cache) is independent of how the
MACs are done — photonics cannot remove it.
"""
import json
from dataclasses import dataclass
from pathlib import Path

DATA = Path(__file__).parent / "data"


@dataclass(frozen=True)
class Config:
    hidden: int
    intermediate: int
    layers: int
    heads: int
    kv_heads: int
    vocab: int
    tied_embeddings: bool

    @property
    def head_dim(self) -> int:
        return self.hidden // self.heads

    @property
    def kv_dim(self) -> int:
        return self.kv_heads * self.head_dim

    @classmethod
    def from_hf(cls, name: str) -> "Config":
        c = json.loads((DATA / name).read_text())
        return cls(c["hidden_size"], c["intermediate_size"], c["num_hidden_layers"],
                   c["num_attention_heads"], c["num_key_value_heads"], c["vocab_size"],
                   c.get("tie_word_embeddings", False))

    def params(self) -> int:
        d, i, kv = self.hidden, self.intermediate, self.kv_dim
        per_layer = (d * d + d) + 2 * (d * kv + kv) + d * d + 3 * d * i + 2 * d
        emb = self.vocab * d * (1 if self.tied_embeddings else 2)
        return self.layers * per_layer + emb + d


def decode_ops(cfg: Config, context: int) -> list[tuple[str, str, float]]:
    """(op, class, MACs or elementwise ops per token) for one decoded token."""
    d, i, kv, h, hd, L = cfg.hidden, cfg.intermediate, cfg.kv_dim, cfg.heads, cfg.head_dim, cfg.layers
    return [
        ("q_proj", "static", L * d * d),
        ("k_proj", "static", L * d * kv),
        ("v_proj", "static", L * d * kv),
        ("attn_scores_QK", "dynamic", L * h * hd * context),
        ("attn_softmax", "nonlinear", L * h * context),
        ("attn_AV", "dynamic", L * h * hd * context),
        ("o_proj", "static", L * d * d),
        ("mlp_gate_up", "static", L * 2 * d * i),
        ("mlp_silu_mul", "nonlinear", L * 2 * i),
        ("mlp_down", "static", L * i * d),
        ("rmsnorm", "nonlinear", L * 2 * 2 * d),
        ("lm_head", "static", d * cfg.vocab),
    ]


def decode_bytes(cfg: Config, context: int, bytes_per_weight: float, bytes_per_kv: float,
                 batch: int) -> dict:
    """Bytes read from memory per generated token.

    Every weight matrix is streamed once per batch step, except an UNTIED input embedding: each
    token reads only its own row (d weights), not the whole table (D16 correction, E028).
    """
    streamed = cfg.params() - (0 if cfg.tied_embeddings else cfg.vocab * cfg.hidden)
    embed_row = 0 if cfg.tied_embeddings else cfg.hidden
    weights = streamed * bytes_per_weight / batch + embed_row * bytes_per_weight
    kv_cache = 2 * cfg.layers * cfg.kv_dim * context * bytes_per_kv
    return {"weights": weights, "kv_cache": kv_cache, "total": weights + kv_cache}


def class_shares(ops: list[tuple[str, str, float]]) -> dict:
    macs = {k: 0.0 for k in ("static", "dynamic")}
    for _, cls, n in ops:
        if cls in macs:
            macs[cls] += n
    total = sum(macs.values())
    return {k: v / total for k, v in macs.items()} | {"total_macs": total}
