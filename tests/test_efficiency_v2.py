"""Pin the E028 photonic families (scripts/efficiency_v2.py) so the published H1' and decode numbers are tested."""
import importlib.util
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location("efficiency_v2", Path(__file__).resolve().parent.parent / "scripts/efficiency_v2.py")
ev2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ev2)


def test_decode_cannot_beat_the_memory_wall():
    # any engine that streams weights pays HBM; B300 board at max TGP on the roofline caps the gain below 2x
    for fmt in ("FP4", "FP8"):
        r = ev2.family_s(fmt, 64)
        assert r["bound"] == pytest.approx(1.87, abs=0.01)
        assert 1.5 < r["gpu"] / r["total"] < r["bound"]


def test_h1_square_photon_to_charge_core_and_support_budget():
    fp4 = ev2.family_r("FP4", 1024, "pc")
    fp8 = ev2.family_r("FP8", 1024, "pc")
    assert fp4["core"] == pytest.approx(0.91e-15, rel=0.02)
    assert fp8["core"] == pytest.approx(5.42e-15, rel=0.02)
    assert fp4["support_for_10x"] == pytest.approx(20.6, abs=0.3)
    assert fp8["support_for_10x"] == pytest.approx(10.3, abs=0.3)


def test_h1_fails_gate_with_a_conventional_receiver():
    for n in (256, 1024):
        for fmt in ("FP4", "FP8"):
            assert ev2.family_r(fmt, n, "nep")["support_for_10x"] < 2.0


def test_realistic_ladder_loses_the_gate():
    # E032: each cumulative sourced correction can only raise the core energy; the realistic end fails 10x
    for fmt in ("FP4", "FP8"):
        steps = ev2.ladder(fmt)
        main = [s for s in steps if not s[0].startswith("  ")]
        cores = [c for _, c, _ in main]
        assert cores == sorted(cores)
        assert main[0][2] > 10 if fmt == "FP4" else main[0][2] > 5          # idealised end (A4)
    fp4, fp8 = ev2.ladder("FP4"), ev2.ladder("FP8")
    assert fp4[4][2] == pytest.approx(2.65, abs=0.05)                     # all corrections, 20 dB
    assert fp8[4][2] < 1.0                                                  # FP8 fails with zero support overhead
    assert fp4[5][2] < 1.0                                                  # +6 dB loss: FP4 fails too


def test_nep_receiver_scales_x2_per_bit():
    assert ev2.nep_detect(8) / ev2.nep_detect(5) == pytest.approx(8.0)
