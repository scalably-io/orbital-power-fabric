import pytest

from opf.transformer import Config, class_shares, decode_bytes, decode_ops

CFG = Config.from_hf("qwen2.5-72b-instruct.config.json")


def test_config_parsed_and_param_count_matches_72b_class():
    assert (CFG.hidden, CFG.layers, CFG.heads, CFG.kv_heads, CFG.head_dim) == (8192, 80, 64, 8, 128)
    assert 70e9 < CFG.params() < 75e9


def test_static_macs_are_about_params_per_token():
    # at short context, decode MACs/token ~= non-embedding params + LM head
    shares = class_shares(decode_ops(CFG, context=1))
    assert shares["total_macs"] == pytest.approx(CFG.params() - CFG.vocab * CFG.hidden, rel=0.01)


def test_dynamic_share_grows_with_context():
    short = class_shares(decode_ops(CFG, 1_000))["dynamic"]
    long = class_shares(decode_ops(CFG, 100_000))["dynamic"]
    assert short < long


def test_batch1_decode_is_weight_memory_bound():
    b = decode_bytes(CFG, context=4096, bytes_per_weight=1.0, bytes_per_kv=1.0, batch=1)
    assert b["weights"] > 10 * b["kv_cache"]


def test_untied_embedding_reads_one_row_per_token():
    # D16 correction (E028): Qwen2.5-72B has untied embeddings -> the input table is not streamed
    assert CFG.tied_embeddings is False
    b = decode_bytes(CFG, context=1, bytes_per_weight=1.0, bytes_per_kv=1.0, batch=1)
    assert b["weights"] == CFG.params() - CFG.vocab * CFG.hidden + CFG.hidden
    assert CFG.params() - b["weights"] == pytest.approx(1.246e9, rel=1e-3)
