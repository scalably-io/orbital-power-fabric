"""Parameter registry. Every value carries its source and tier.

Two sets, never mixed:
- HANDOFF: the original handoff's numbers, frozen, used only to prove the model
  reproduces them (tests/test_handoff_baseline.py, scripts/first_cut.py = E004).
- VERIFIED: values from evidence/claims.csv (claim_id) or ASSUMPTION:<why>.
  This is what the verdict uses.
tier: current | next | speculative (never mixed inside one scenario).
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Param:
    value: float
    unit: str
    source: str
    tier: str = "current"
    note: str = ""


HANDOFF = {
    "solar_constant": Param(1367.5, "W/m2", "H-C004"),
    "sun_angle": Param(0.53, "deg", "H-C007"),
    "rack_kw": Param(142.0, "kW", "H-C009"),
    "pue": Param(1.15, "-", "H-baseline_params"),
    "pv_eff": Param(0.35, "-", "H-C004"),
    "dc_dc_space": Param(0.90, "-", "H-C004"),
    "dc_rf": Param(0.70, "-", "H-C004"),
    "antenna": Param(0.90, "-", "H-C004"),
    "atmosphere_rf": Param(0.98, "-", "H-C004"),
    "beam_capture": Param(0.95, "-", "H-C004"),
    "rectenna": Param(0.78, "-", "H-C004"),
    "dc_dc_ground": Param(0.90, "-", "H-C004"),
    "reflector_altitude": Param(625_000.0, "m", "H-baseline_params"),
    "mirror_reflectivity": Param(0.90, "-", "H-baseline_params"),
    "atm_clear_zenith": Param(0.85, "-", "H-baseline_params"),
    "ground_pv_eff": Param(0.30, "-", "H-baseline_params"),
    "radiator_emissivity": Param(0.90, "-", "H-baseline_params"),
    "radiator_temp": Param(350.0, "K", "H-baseline_params"),
    "orbital_compute_kw_per_tonne": Param(75.0, "kW/t", "H-C001"),
}

VERIFIED = {
    # --- common ---
    "solar_constant": Param(1360.8, "W/m2", "R2-119", note="measured TSI at 2008 solar minimum; NASA used 1367.5 (R2-009)"),
    "sun_angle": Param(0.5331, "deg", "R12-032", note="1919 arcsec at 1 AU (NASA); IAU 0.5329 (R12-033); Celik 0.0093 rad (R1-123)"),
    "land_fraction": Param(0.291, "-", "R12-019", note="USGS PP 1386-A"),
    "clear_sky_fraction": Param(0.66, "-", "R12-016", note="all-hours mean, 12 PV regions, NASA POWER 2001-2020; range 0.44-0.84; satellite values are a conservative lower bound (R12-017/018)"),
    "geo_design_life_years": Param(15.0, "y", "R12-022", note="median design life, 426 GEO comsats (UCS); design, not observed"),
    # --- reference AI load ---
    "rack_kw": Param(142.0, "kW", "R1-095", note="GB300 NVL72 max rack power, vendor"),
    "pue": Param(1.15, "-", "ASSUMPTION:illustrative (a typical liquid-cooled data centre); not swept in v1.0"),
    # --- branch B chain: NASA OTPS 2024 study inputs (STUDY-ASSUMED, not measured) ---
    "pv_eff": Param(0.35, "-", "R2-001"),
    "dc_dc_space": Param(0.90, "-", "R2-002"),
    "dc_rf": Param(0.70, "-", "R2-003", note="best measured space-grade GaN array total DC-RF 35.1% (R2-042)"),
    "antenna": Param(0.90, "-", "R2-004"),
    "atmosphere_rf": Param(0.98, "-", "R2-005"),
    "beam_capture": Param(0.95, "-", "R2-006"),
    "rectenna": Param(0.78, "-", "R2-007"),
    "dc_dc_ground": Param(0.90, "-", "R2-008"),
    "pv_w_per_kg_flown": Param(84.6, "W/kg", "R2-093", note="iROSA wing BOL (SUNSTONE 28 kW / 331 kg)"),
    "pv_w_per_kg_today_caltech": Param(25.0, "W/kg", "R2-067", note="Caltech 2025 estimate, system"),
    # --- branch C ---
    "reflector_altitude": Param(625_000.0, "m", "ASSUMPTION:handoff altitude, swept"),
    "mirror_reflectivity": Param(0.90, "-", "ASSUMPTION:no sourced value yet"),
    "atm_clear_zenith": Param(0.64, "-", "R1-136", note="Hottel model, ~0.13 at pass ends; handoff used 0.85"),
    "ground_pv_eff": Param(0.30, "-", "ASSUMPTION:full-sun value; low light is lower (R5)"),
    "membrane_areal_density": Param(4.25e-3, "kg/m2", "R1-149", note="ACS3 membrane quadrant incl. hardware; booms extra (R1-150)"),
    "inverter_start_irradiance": Param(2.6, "W/m2", "R5-069", note="median CEC utility inverter at ILR 1.32 with IDEAL module; ~5 W/m2 at 50% low-light efficiency (same row); R5-068 = 0.35% of AC rating, recomputed E016"),
    # --- thermal ---
    "radiator_emissivity": Param(0.90, "-", "ASSUMPTION:typical coating"),
    "radiator_temp": Param(350.0, "K", "ASSUMPTION:handoff value; AI1 needs >=322 K two-sided (R1-014)"),
    # --- branch A ---
    "orbital_compute_kw_per_tonne": Param(75.0, "kW/t", "R1-005",
                                          note="vendor; numerator ambiguous (peak 250 vs avg 175 kW -> 3.33 or 2.33 t, R1-012)"),
    "satellite_life_years": Param(5.0, "y", "R1-023", note="SpaceX and Starcloud FCC filings; 424B4 books satellites at 3-5 y (R1-035)"),
    "server_life_years": Param(5.5, "y", "R1-035", note="SpaceX 424B4: servers and networking 5-6 y"),
}


def v(name: str) -> float:
    """Verified value (for the verdict)."""
    return VERIFIED[name].value


def h(name: str) -> float:
    """Handoff value (only for reproducing the handoff)."""
    return HANDOFF[name].value
