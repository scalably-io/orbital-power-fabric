"""Conversion ledger: every change of energy form along a delivery chain.

Each Step moves energy between domains (photon, dc, ac, rf, heat) with an
efficiency; the loss (1 - eff) becomes heat at `heat_site`. A chain reports its
end-to-end efficiency, how many domain crossings it makes, and where heat lands
— the inputs to "keep photons as photons where a conversion is not needed".
Efficiencies must cite a claim_id (or ASSUMPTION:<why>) like every model value.
"""
import math
from dataclasses import dataclass

DOMAINS = {"photon", "dc", "ac", "rf", "compute", "heat"}


@dataclass(frozen=True)
class Step:
    name: str
    src: str
    dst: str
    eff: float
    heat_site: str      # "orbit" | "ground" | "chip" | "atmosphere"
    source: str
    avoidable_by: str = ""   # alternative that removes this step, if any

    def __post_init__(self):
        if self.src not in DOMAINS or self.dst not in DOMAINS:
            raise ValueError(f"{self.name}: unknown domain {self.src}->{self.dst}")
        if not 0.0 < self.eff <= 1.0:
            raise ValueError(f"{self.name}: efficiency {self.eff} out of range")


@dataclass(frozen=True)
class Chain:
    name: str
    steps: tuple[Step, ...]

    def __post_init__(self):
        for a, b in zip(self.steps, self.steps[1:]):
            if a.dst != b.src:
                raise ValueError(f"{self.name}: {a.name} ends in {a.dst} but {b.name} starts in {b.src}")

    def efficiency(self) -> float:
        return math.prod(s.eff for s in self.steps)

    def domain_crossings(self) -> int:
        return sum(1 for s in self.steps if s.src != s.dst)

    def heat_by_site(self, input_w: float = 1.0) -> dict:
        """Heat deposited per site for `input_w` entering the chain."""
        heat, p = {}, input_w
        for s in self.steps:
            loss = p * (1.0 - s.eff)
            heat[s.heat_site] = heat.get(s.heat_site, 0.0) + loss
            p -= loss
        return heat

    def without(self, *names: str, bridge: Step | None = None) -> "Chain":
        """Chain with named steps removed (optionally replaced by one bridging step)."""
        kept = [s for s in self.steps if s.name not in names]
        if bridge is not None:
            first = next(i for i, s in enumerate(self.steps) if s.name in names)
            kept.insert(sum(1 for s in self.steps[:first] if s.name not in names), bridge)
        return Chain(f"{self.name} − {'/'.join(names)}", tuple(kept))
