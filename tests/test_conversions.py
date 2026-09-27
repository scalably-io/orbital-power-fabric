import pytest

from opf.conversions import Chain, Step

# Branch B chain from the handoff factors (H-C004), as a conversion ledger
B = Chain("B orbital PV -> RF -> ground DC", (
    Step("pv", "photon", "dc", 0.35, "orbit", "H-C004"),
    Step("dc_dc_space", "dc", "dc", 0.90, "orbit", "H-C004"),
    Step("dc_rf", "dc", "rf", 0.70, "orbit", "H-C004"),
    Step("antenna", "rf", "rf", 0.90, "orbit", "H-C004"),
    Step("atmosphere", "rf", "rf", 0.98, "atmosphere", "H-C004"),
    Step("beam_capture", "rf", "rf", 0.95, "ground", "H-C004"),
    Step("rectenna", "rf", "dc", 0.78, "ground", "H-C004"),
    Step("dc_dc_ground", "dc", "dc", 0.90, "ground", "H-C004"),
))


def test_chain_matches_power_chain_module():
    assert B.efficiency() == pytest.approx(0.129699, abs=1e-6)
    assert B.domain_crossings() == 3          # photon->dc, dc->rf, rf->dc


def test_heat_conserves_energy():
    heat = B.heat_by_site(1.0)
    assert sum(heat.values()) + B.efficiency() == pytest.approx(1.0)
    assert heat["orbit"] > heat["ground"]     # most loss lands in orbit (PV + DC-RF)


def test_without_removes_and_bridges():
    shorter = B.without("dc_dc_space")
    assert len(shorter.steps) == len(B.steps) - 1
    bridged = B.without("dc_rf", "antenna", bridge=Step("direct", "dc", "rf", 0.8, "orbit", "ASSUMPTION:test"))
    assert [s.name for s in bridged.steps][:3] == ["pv", "dc_dc_space", "direct"]


def test_domain_mismatch_is_rejected():
    with pytest.raises(ValueError):
        Chain("bad", (Step("a", "photon", "dc", 0.5, "orbit", "x"), Step("b", "rf", "dc", 0.5, "ground", "x")))
