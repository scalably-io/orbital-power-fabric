"""Pin the verdict v1 building blocks (E021) so later changes show up as test diffs."""
import math

import pytest

from opf import scenarios as sc


def test_branch_a_range_from_kw_per_tonne_ambiguity():
    assert sc.A["current"].kg_per_kw == pytest.approx((13.333, 19.048), abs=1e-3)
    assert sc.A["current"].life == 5.0


def test_b_leo_transmitter_alone_exceeds_orbital_gpus():
    t = sc.B["current"]
    tx_only = 1000 * sc.PUE * (0.90 * t.dc_rf / t.tx_w_per_kg_rf) / t.post_pv
    assert tx_only == pytest.approx(92.3, abs=0.5)
    assert tx_only > sc.A["current"].kg_per_kw[1]


def test_c_current_uses_filed_earendil_system_density():
    assert sc.C["current"].kg_per_m2 == pytest.approx(142 / 324)
    assert sc.c_kg_per_kw(sc.C["current"], 1000) == pytest.approx(3.03, abs=0.01)


def test_geo_rectenna_and_launch_cost_units():
    assert sc.geo_rectenna_m2() / 1e6 == pytest.approx(13.05, abs=0.05)
    # 13.33 kg/kW x $3,600/kg over 5 y of continuous operation = 43.8 MWh -> $1,096/MWh
    assert sc.launch_usd_per_mwh(13.333, 3600, 5) == pytest.approx(1095.9, abs=0.5)


def test_geo_transmitter_is_sized_by_power_not_only_aperture():
    # D20: a 1 km JAXA-class panel (44.7 kg/m2, 28 W/kg RF-out) radiates at most ~0.98 GW RF,
    # so 10 GW delivered (next-tier chain) needs a power-sized transmitter (Codex review 2026-09-27).
    t = sc.B["next"]
    cap = math.pi / 4 * 1000**2 * 44.7 * 28.0
    assert cap / 1e9 == pytest.approx(0.983, abs=0.005)
    assert sc.geo_rf_w(t, 10e9) / 1e9 == pytest.approx(17.0, abs=0.05)
    assert sc.b_geo_kg_per_kw(t, 10e9, 44.7) == pytest.approx(94.8, abs=0.2)
    # below the aperture's capacity the aperture binds
    small = sc.b_geo_kg_per_kw(t, 0.5e9, 44.7)
    pv = 1000 * sc.PUE * (1 / t.post_pv / t.pv_w_per_kg)
    assert small == pytest.approx(pv + 1000 * sc.PUE * math.pi / 4 * 1000**2 * 44.7 / 0.5e9, rel=1e-9)


def test_mirrors_onto_a_real_solar_farm_are_about_five_times_heavier():
    # E034: measured tracking-farm density 59.3 MW_DC/km2 (R5-077) vs 30% on every lit m2 (favourable)
    assert sc.SITE_PV_REAL_FARM == pytest.approx(0.0593)
    ideal = sc.c_kg_per_kw(sc.C["next"], 208)
    real = sc.c_kg_per_kw(sc.C["next"], 208, site_conv=sc.SITE_PV_REAL_FARM)
    assert real / ideal == pytest.approx(0.30 / 0.0593, rel=1e-9)
