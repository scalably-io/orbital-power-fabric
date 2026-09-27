"""Lifecycle launched mass per continuous kW of AI load (preregistered primary metric).

A (orbital GPU): the whole vehicle is relaunched at min(GPU refresh, vehicle life).
B (orbital PV -> RF -> ground): orbital hardware relaunched at vehicle life; GPUs
  refresh on the ground at zero launch mass. Delivered power is diluted by the
  time a receiver is in view and by eclipse.
C (orbital mirror -> ground PV): as B, with mirror area set by delivered power.
All results in kg of launched hardware per continuous kW of accelerator IT load.
"""
import math
from dataclasses import dataclass

from .power_chain import RFChain


def replacements(lifecycle_years: float, service_years: float) -> float:
    """Launches over the lifecycle (continuous approximation; 10 y at 5 y life -> 2.0)."""
    return lifecycle_years / service_years


def launches(lifecycle_years: float, service_years: float) -> int:
    """Whole spacecraft launched to cover the lifecycle (D17 correction): ceil(L / S)."""
    return math.ceil(lifecycle_years / service_years - 1e-9)


def min_service_life(lifecycle_years: float, kg_per_launch: float, budget_kg: float) -> float:
    """Shortest service life S with kg_per_launch * ceil(L / S) <= budget (whole launches, D17 correction).
    inf when even one launch exceeds the budget: no service life within L can match it."""
    n_max = math.floor(budget_kg / kg_per_launch + 1e-12)
    return math.inf if n_max < 1 else lifecycle_years / n_max


@dataclass(frozen=True)
class OrbitalCompute:
    kw_per_tonne: float        # vehicle-level compute kW per tonne launched
    gpu_refresh_years: float
    vehicle_life_years: float

    def kg_per_kw(self) -> float:
        return 1000.0 / self.kw_per_tonne

    def lifecycle_kg_per_kw(self, lifecycle_years: float) -> float:
        service = min(self.gpu_refresh_years, self.vehicle_life_years)
        return self.kg_per_kw() * replacements(lifecycle_years, service)


@dataclass(frozen=True)
class PowerBeaming:
    chain: RFChain
    pv_w_per_kg: float           # array-level specific power (PV DC out per kg)
    tx_w_per_kg: float           # transmitter specific power (RF-chain DC in per kg)
    structure_fraction: float    # bus/structure/thermal/ADCS mass as a fraction of PV+TX
    link_duty: float             # fraction of time a receiver is in view and beaming
    sunlit_fraction: float       # 1 - eclipse fraction
    vehicle_life_years: float
    pue: float

    def kg_per_w_orbital_dc(self) -> float:
        return (1.0 / self.pv_w_per_kg + 1.0 / self.tx_w_per_kg) * (1.0 + self.structure_fraction)

    def avg_delivered_per_w_orbital_dc(self) -> float:
        return self.chain.post_pv() * self.link_duty * self.sunlit_fraction

    def kg_per_kw(self) -> float:
        per_w_delivered = self.kg_per_w_orbital_dc() / self.avg_delivered_per_w_orbital_dc()
        return 1000.0 * per_w_delivered * self.pue

    def lifecycle_kg_per_kw(self, lifecycle_years: float) -> float:
        return self.kg_per_kw() * replacements(lifecycle_years, self.vehicle_life_years)


@dataclass(frozen=True)
class MirrorFabric:
    optical_w_per_m2_mirror: float   # sunlight reaching ground per m² mirror (tilt + atmosphere applied)
    ground_pv_eff: float             # PV efficiency AT the delivered irradiance (low light is worse)
    capture: float                   # share of footprint energy on receiving PV
    link_duty: float
    sunlit_fraction: float
    kg_per_m2: float                 # system areal density incl. booms, bus, ADCS
    vehicle_life_years: float
    pue: float

    def kg_per_kw(self) -> float:
        avg_w_per_m2 = (self.optical_w_per_m2_mirror * self.ground_pv_eff * self.capture
                        * self.link_duty * self.sunlit_fraction)
        return 1000.0 * self.kg_per_m2 / avg_w_per_m2 * self.pue

    def lifecycle_kg_per_kw(self, lifecycle_years: float) -> float:
        return self.kg_per_kw() * replacements(lifecycle_years, self.vehicle_life_years)
