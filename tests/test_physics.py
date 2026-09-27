"""Physics sanity: limits, monotonicity, and textbook cross-checks."""
import math

import pytest

from opf import lifecycle, microwave, orbit, photonic, power_chain, reflector, thermal
from opf.constants import GEO_ALTITUDE


def test_slant_range_limits():
    assert orbit.slant_range(625e3, 90) == pytest.approx(625e3)
    # horizon distance sqrt((R+h)^2 - R^2) at 0 deg elevation
    assert orbit.slant_range(625e3, 0) == pytest.approx(math.sqrt((6371e3 + 625e3) ** 2 - 6371e3**2))


def test_footprint_grows_as_elevation_falls():
    areas = [reflector.footprint_area_m2(625e3, e, 0.53) for e in (90, 60, 45, 30, 20)]
    assert areas == sorted(areas)
    assert areas[3] / areas[0] == pytest.approx(6.38, abs=0.05)   # E002: ~167 km2 at 30 deg


def test_mirror_tilt_dawn_dusk():
    inc = reflector.incidence_deg(90.0)
    assert inc == 45.0
    flat = reflector.optical_w_per_m2_mirror(1367.5, 0.9, 0.0, 0.85)
    tilted = reflector.optical_w_per_m2_mirror(1367.5, 0.9, inc, 0.85)
    assert tilted / flat == pytest.approx(math.sqrt(0.5))


def test_airmass_transmission():
    assert reflector.transmission(0.85, 90) == pytest.approx(0.85)
    assert reflector.transmission(0.85, 30) == pytest.approx(0.85**2)


def test_visibility_and_eclipse():
    f = orbit.visible_fraction(625e3, 30)
    assert 0.004 < f < 0.006                      # one site sees a 625 km sat ~0.5% of the time
    assert orbit.fabric_visibility(625e3, 30, 1) == pytest.approx(f)
    assert orbit.fabric_visibility(625e3, 30, 100) > 0.35
    assert orbit.eclipse_fraction(625e3, 90) == 0.0          # dawn-dusk limit
    assert 0.35 < orbit.eclipse_fraction(625e3, 0) < 0.40    # worst case ~36-37% at LEO
    # GEO at equinox: ~72 min eclipse in a ~24 h orbit
    assert orbit.eclipse_fraction(GEO_ALTITUDE, 0) * 24 * 60 == pytest.approx(69.4, abs=3)


def test_goubau_round_trip():
    lam = microwave.wavelength_m(5.8e9)
    rx = microwave.rx_area_for_efficiency(0.95, 1e6, lam, GEO_ALTITUDE)
    tau = microwave.goubau_tau(1e6, rx, lam, GEO_ALTITUDE)
    assert microwave.collection_efficiency(tau) == pytest.approx(0.95)


def test_radiator_sink_reduces_flux():
    assert thermal.radiative_flux_w_m2(0.9, 350, 250) < thermal.radiative_flux_w_m2(0.9, 350)
    assert thermal.radiator_area_m2(1000, 0.9, 350, sides=2) == pytest.approx(
        thermal.radiator_area_m2(1000, 0.9, 350) / 2)


def test_mvm_energy_amortises_io_over_n():
    small = photonic.MVMEnergy(4, 1e-18, 0.2, 1e-12, 1e-12, 1e-13, 1e-12).per_mac()
    big = photonic.MVMEnergy(64, 1e-18, 0.2, 1e-12, 1e-12, 1e-13, 1e-12).per_mac()
    assert big["total"] < small["total"]
    assert small["laser"] == big["laser"] == pytest.approx(5e-18)


def test_lifecycle_replacement_logic():
    a = lifecycle.OrbitalCompute(kw_per_tonne=75, gpu_refresh_years=5, vehicle_life_years=10)
    assert a.kg_per_kw() == pytest.approx(13.333, abs=1e-3)
    assert a.lifecycle_kg_per_kw(15) == pytest.approx(40.0, abs=1e-3)   # refresh binds: 3 launches
    chain = power_chain.RFChain(0.35, 0.9, 0.7, 0.9, 0.98, 0.95, 0.78, 0.9)
    b = lifecycle.PowerBeaming(chain, pv_w_per_kg=100, tx_w_per_kg=1e12, structure_fraction=0,
                               link_duty=1.0, sunlit_fraction=1.0, vehicle_life_years=15, pue=1.0)
    # 1 kW delivered needs 1/0.37057 kW of orbital DC at 100 W/kg
    assert b.kg_per_kw() == pytest.approx(1000 / 0.37057 / 100, rel=1e-4)


def test_flip_value_finds_crossing_and_reports_none():
    from opf.breakeven import flip_value
    assert flip_value(lambda x: x - 3.0, 0, 10) == pytest.approx(3.0, abs=1e-6)
    assert flip_value(lambda x: x + 1.0, 0, 10) is None


def test_geo_rectenna_scale():
    # 5.8 GHz, 1 km transmit aperture at GEO, 95% collection -> rectenna of order 10 km2
    lam = microwave.wavelength_m(5.8e9)
    tx = math.pi / 4 * 1000.0**2
    rx = microwave.rx_area_for_efficiency(0.95, tx, lam, GEO_ALTITUDE)
    assert 1.0e7 < rx < 2.0e7


def test_fabric_visibility_bounds():
    f = orbit.visible_fraction(625e3, 30)
    rnd = orbit.fabric_visibility(625e3, 30, 100, "random")
    dis = orbit.fabric_visibility(625e3, 30, 100, "disjoint")
    assert rnd < dis == pytest.approx(100 * f)
    assert orbit.fabric_visibility(625e3, 30, 10_000, "disjoint") == 1.0


def test_eclipse_formula_matches_geometry_by_sampling():
    # brute force: sample the orbit, count points inside the cylindrical shadow (D04)
    import numpy as np
    R, h, beta = 6371e3, 625e3, math.radians(40)
    r = R + h
    s = np.array([math.cos(beta), 0.0, math.sin(beta)])
    th = np.linspace(0, 2 * np.pi, 200_000, endpoint=False)
    pos = r * np.stack([np.cos(th), np.sin(th), np.zeros_like(th)], axis=1)
    along = pos @ s
    perp = np.sqrt(np.maximum(r**2 - along**2, 0))
    frac = np.mean((along < 0) & (perp < R))
    assert orbit.eclipse_fraction(h, 40) == pytest.approx(frac, abs=1e-4)


def test_whole_launches():
    # D17 correction (E028): a spacecraft is launched whole
    assert [lifecycle.launches(L, 5) for L in (10, 15, 20)] == [2, 3, 4]
    assert [lifecycle.launches(L, 15) for L in (10, 15, 20)] == [1, 1, 2]
    assert lifecycle.launches(15, 5.5) == 3


def test_min_service_life_counts_whole_launches():
    # Codex paper review (E033): the filed mirror at 0.66 weather is 4.61 kg/kW per launch vs a 40 kg/kW budget
    # -> at most 8 launches in 15 y -> life >= 1.875 y (the continuous approximation gave 1.7 y)
    assert lifecycle.min_service_life(15, 3.04 / 0.66, 40.0) == pytest.approx(15 / 8)
    assert lifecycle.min_service_life(15, 94.8, 40.0) == float("inf")      # next-tier GEO: one launch exceeds A
    assert lifecycle.min_service_life(15, 10.0, 40.0) == pytest.approx(3.75)


def test_dawn_dusk_orbit_serves_one_site_a_small_share_of_the_day():
    # D22 (E033, Opus paper review): 625 km, 30 deg mask -> cap half-width ~7.9 deg -> ~8.8% of the day
    lam = math.degrees(orbit.central_angle(625e3, 30.0))
    assert lam == pytest.approx(7.9, abs=0.1)
    assert orbit.terminator_site_fraction(625e3, 30.0) == pytest.approx(4 * lam / 360, rel=1e-9)
    assert orbit.terminator_site_fraction(625e3, 30.0) == pytest.approx(0.088, abs=0.002)
