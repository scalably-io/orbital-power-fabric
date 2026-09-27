"""The model must reproduce the handoff's reference numbers before it may disagree with them.

Expected values are copied from handoff/REFERENCE_MODEL_OUTPUT.txt (E001).
"""
import math

import pytest

from opf import microwave, orbit, photonic, power_chain, reflector, thermal
from opf.params import h as v  # handoff values only (reproduction)

CHAIN = power_chain.RFChain(
    pv=v("pv_eff"), dc_dc_space=v("dc_dc_space"), dc_rf=v("dc_rf"), antenna=v("antenna"),
    atmosphere=v("atmosphere_rf"), beam_capture=v("beam_capture"), rectenna=v("rectenna"),
    dc_dc_ground=v("dc_dc_ground"),
)
FACILITY_W = v("rack_kw") * v("pue") * 1000.0


def test_rf_chain_matches_handoff():
    assert CHAIN.total() == pytest.approx(0.129699, abs=1e-6)
    assert CHAIN.post_pv() == pytest.approx(0.370570, abs=1e-6)
    assert power_chain.delivered_w_per_m2(v("solar_constant"), CHAIN) == pytest.approx(177.36, abs=0.01)
    assert power_chain.collector_area_m2(FACILITY_W, v("solar_constant"), CHAIN) == pytest.approx(920.7, abs=0.1)


def test_overhead_mirror_spot_matches_handoff():
    area = reflector.footprint_area_m2(v("reflector_altitude"), 90.0, v("sun_angle"))
    d = orbit.slant_range(v("reflector_altitude"), 90.0)
    assert d == pytest.approx(625_000.0, rel=1e-9)
    assert reflector.spot_diameter_m(d, v("sun_angle")) / 1000 == pytest.approx(5.78, abs=0.005)
    assert area / 1e6 == pytest.approx(26.25, abs=0.01)


def test_handoff_mirror_yield_is_zero_tilt_flat_atmosphere():
    optical = reflector.optical_w_per_m2_mirror(v("solar_constant"), v("mirror_reflectivity"), 0.0,
                                                v("atm_clear_zenith"))
    assert optical * v("ground_pv_eff") == pytest.approx(313.8, abs=0.1)
    assert reflector.mirror_area_for_load(FACILITY_W, optical, v("ground_pv_eff"), 1.0) == pytest.approx(520.3, abs=0.1)


def test_radiator_and_photon_match_handoff():
    assert thermal.radiative_flux_w_m2(0.9, 350.0) == pytest.approx(765.8, abs=0.1)
    assert thermal.radiator_area_m2(175_000, 0.9, 350.0) == pytest.approx(228.5, abs=0.1)
    assert photonic.photon_energy_j(1550e-9) / 1e-18 == pytest.approx(0.1282, abs=1e-4)
    assert photonic.photons_per_mac(20e-18, 1550e-9) == pytest.approx(156.1, abs=0.1)


def test_diffraction_ledger_values():
    # PHYSICS_AND_MATH_LEDGER §3 and §7
    assert microwave.airy_first_null_diameter_m(1064e-9, 550e3, 1.0) == pytest.approx(1.43, abs=0.005)
    lam = microwave.wavelength_m(10e9)
    assert 1.22 * lam * 550e3 / 30.0 == pytest.approx(670, rel=0.01)
