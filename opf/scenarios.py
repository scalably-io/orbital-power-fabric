"""Verdict scenarios by tier, built ONLY from evidence/claims.csv values (claim_id per field).

Tiers (docs/PREREGISTRATION.md): current = flown/qualified/measured, next = best demonstrated,
speculative = projected. Where a quantity has no sourced value (e.g. GEO power-satellite life),
it is NOT assumed: the verdict reports the break-even value instead (opf/breakeven.py).
Choices that favour the orbital-energy branches (B, C) are marked FAVOURABLE — if B or C
lose with them, they lose without them.
"""
import math
from dataclasses import dataclass

from . import microwave, orbit
from .constants import GEO_ALTITUDE

S = 1360.8                       # W/m2, R2-119 measured TSI
PUE = 1.15                       # ASSUMPTION (swept elsewhere)
SAT_LIFE_LEO = 5.0               # y, R1-023 / R1-079 (orbital data-centre filings); applied to LEO energy sats = ASSUMPTION
SERVER_LIFE = 5.5                # y, R1-035 (SpaceX 424B4 5-6 y)
LAND = 0.291                     # R12-019 USGS land fraction (receivers only on land)
CLEAR_SKY = 0.66                 # R12-016 all-hours clear-sky mean, 12 utility-PV regions (range 0.44-0.84)
GEO_LIFE = 15.0                  # y, R12-022 median GEO comsat DESIGN life
MIRROR_LIFE = 1.0                # y, R1-115 Earendil-1 filing: ~1 y of operations (drag deorbit ~5 months, R1-116);
                                 # the only sourced life for an orbital reflector (E028, Opus review)
GLOBAL_CLEAR_SKY = 0.33          # R10-052: MODIS global cloud fraction ~67% -> clear ~0.33 (global coverage)


@dataclass(frozen=True)
class TierA:
    kg_per_kw: tuple[float, float]   # continuous kW; range from the kW/t numerator ambiguity (R1-012)
    life: float
    src: str


A = {
    # R1-005 75 kW/t; numerator avg 175 kW -> 2.33 t -> 13.3 kg/kW, peak 250 kW -> 3.33 t -> 19.0 kg/kW (R1-003/004/012)
    "current": TierA((1000 * 175 / 75 / 175, 1000 * 250 / 75 / 175), min(SAT_LIFE_LEO, SERVER_LIFE), "R1-005,R1-012,R1-023"),
    # R1-020 SpaceX filing target 100 kW/t (PROJECTED)
    "speculative": TierA((1000 * 175 / 100 / 175, 1000 * 250 / 100 / 175), min(SAT_LIFE_LEO, SERVER_LIFE), "R1-020"),
}


@dataclass(frozen=True)
class TierB:
    pv_w_per_kg: float       # array-level
    tx_w_per_kg_rf: float    # transmitter RF-out specific power (inf = folded into pv figure)
    post_pv: float           # orbital PV DC -> ground DC
    dc_rf: float             # DC -> RF efficiency inside post_pv (sizes the transmitter)
    src: str


# post-PV chain, measured components where they exist: DC-RF 0.351 and rectenna 0.59 (JAXA 2015, R2-042);
# the rest NASA study factors (R2-002, R2-004..006, R2-008).
_MEASURED_CHAIN = 0.90 * 0.351 * 0.90 * 0.98 * 0.95 * 0.59 * 0.90
B = {
    "current": TierB(88.15, 28.0, _MEASURED_CHAIN, 0.351, "R2-093 median ROSA wing, R2-043 JAXA GaN tx, R2-042 chain"),
    "next": TierB(124.1, 28.0, 0.3706, 0.70, "R2-093 OPAL best wing, R2-043, R2-011/R2-003 NASA chain"),
    "speculative": TierB(923.5, math.inf, 0.3706, 0.70, "R2-018 NASA-implied whole system (mean of 938/909), R2-011"),
}


def b_kg_per_w_dc(t: TierB) -> float:
    # transmitter mass per W of orbital DC: RF out = DC * dc-dc 0.90 (R2-002) * DC-RF (in post_pv)
    rf_per_dc = 0.90 * t.dc_rf
    tx = 0.0 if math.isinf(t.tx_w_per_kg_rf) else rf_per_dc / t.tx_w_per_kg_rf
    return 1.0 / t.pv_w_per_kg + tx          # structure/bus = 0: FAVOURABLE to B


def b_leo_kg_per_kw(t: TierB, n_receivers: int, alt=625e3, mask=30.0) -> float:
    duty = orbit.fabric_visibility(alt, mask, n_receivers, "disjoint")   # FAVOURABLE placement
    sunlit = 1.0                                                          # dawn-dusk SSO: FAVOURABLE
    return 1000.0 * PUE * b_kg_per_w_dc(t) / (t.post_pv * duty * sunlit)


def geo_rf_w(t: TierB, delivered_w: float) -> float:
    """RF the transmitter must radiate to deliver `delivered_w` DC on the ground (D20)."""
    return delivered_w / (t.post_pv / (0.90 * t.dc_rf))


def b_geo_kg_per_kw(t: TierB, delivered_w: float, tx_kg_m2: float, f_hz=5.8e9, tx_d=1000.0) -> float:
    """GEO: continuous view; mass = PV for the delivered power + the transmitter (D20).

    The transmitter is the larger of (a) the aperture needed for beam capture (tx_d, areal density)
    and (b) the RF power it must radiate at its specific power: a panel of given W/kg cannot radiate
    more than W/kg x its own mass, so a fixed aperture cannot carry any power level.
    """
    pv_mass = delivered_w / t.post_pv / t.pv_w_per_kg
    aperture_mass = math.pi / 4 * tx_d**2 * tx_kg_m2
    power_mass = 0.0 if math.isinf(t.tx_w_per_kg_rf) else geo_rf_w(t, delivered_w) / t.tx_w_per_kg_rf
    return 1000.0 * PUE * (pv_mass + max(aperture_mass, power_mass)) / delivered_w


def geo_rectenna_m2(f_hz=5.8e9, tx_d=1000.0, eta=0.95) -> float:
    lam = microwave.wavelength_m(f_hz)
    return microwave.rx_area_for_efficiency(eta, math.pi / 4 * tx_d**2, lam, GEO_ALTITUDE)


@dataclass(frozen=True)
class TierC:
    kg_per_m2: float
    src: str


C = {
    # FILING: FCC-filed system, no flight in the ledger (vendor/filed values allowed for `current` where nothing has flown)
    "current": TierC(142.0 / 324.0, "R1-112 142 kg / R1-113 324 m2 (Earendil-1 filed system)"),
    # flown: ACS3 whole spacecraft 16 kg / 80 m2 — a solar SAIL; optical quality as a sunlight relay undemonstrated
    "next": TierC(16.0 / 80.0, "R1-151 ACS3 flown spacecraft ~16 kg / 80 m2 (sail, not a mirror)"),
    # components only: membrane + 4 booms, no deployer or bus (R1-151: small systems are deployer/bus dominated)
    "speculative": TierC(4.25e-3 + 4 * 0.164 / 80.0, "R1-149 membrane + R1-150 4 booms, no deployer/bus"),
}
# optical W/m2 of mirror on the ground at zenith, dawn-dusk tilt 45 deg:
MIRROR_OPTICAL = S * 0.90 * math.cos(math.radians(45)) * 0.64   # 0.90 reflectivity ASSUMPTION; 0.64 R1-136
GROUND_PV = 0.30                                                  # ASSUMPTION, full-sun efficiency: FAVOURABLE


# E034 (Codex final review): a real solar farm does not cover its land with panels. Measured tracking-farm density
# 59.3 MW_DC per km2 at 1,000 W/m2 (R5-077) = 0.0593 W of DC per W of sunlight landing on the SITE; GROUND_PV (0.30 on every
# lit m2) describes a purpose-built, fully covered receiving field and is the FAVOURABLE case.
SITE_PV_REAL_FARM = 59.3e6 / 1e6 / 1000.0


def c_kg_per_kw(t: TierC, n_receivers: int, alt=625e3, mask=30.0, site_conv: float = GROUND_PV) -> float:
    duty = orbit.fabric_visibility(alt, mask, n_receivers, "disjoint")
    return 1000.0 * PUE * t.kg_per_m2 / (MIRROR_OPTICAL * site_conv * duty)


LAUNCH_USD_PER_KG = {"current": 3600.0, "rideshare_2027": 7500.0, "speculative_2035": 200.0, "starship_floor": 60.0}
# R1-057 (Suncatcher F9 assumption), R2-101, R1-053, R1-056
FIRM_SOLAR_USD_PER_MWH = (104.0, 167.0)   # R5-027, R5-028


def launch_usd_per_mwh(kg_per_kw: float, usd_per_kg: float, life_years: float) -> float:
    return kg_per_kw * usd_per_kg / (8.76 * life_years)          # 8.76 MWh per kW-year
