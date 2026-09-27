"""Branch B efficiency chain: sunlight -> orbital PV -> RF -> rectenna -> ground DC."""
import math
from dataclasses import dataclass, fields


@dataclass(frozen=True)
class RFChain:
    pv: float
    dc_dc_space: float
    dc_rf: float
    antenna: float
    atmosphere: float
    beam_capture: float
    rectenna: float
    dc_dc_ground: float

    def total(self) -> float:
        """Incident sunlight -> delivered ground DC."""
        return math.prod(getattr(self, f.name) for f in fields(self))

    def post_pv(self) -> float:
        """Orbital PV DC output -> delivered ground DC."""
        return self.total() / self.pv


def delivered_w_per_m2(solar_w_m2: float, chain: RFChain) -> float:
    """Instantaneous ground DC per m² of active orbital collector, while beaming."""
    return solar_w_m2 * chain.total()


def collector_area_m2(load_w: float, solar_w_m2: float, chain: RFChain) -> float:
    """Active collector area needed to supply `load_w` while the link is up."""
    return load_w / delivered_w_per_m2(solar_w_m2, chain)
