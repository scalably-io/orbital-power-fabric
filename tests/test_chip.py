"""Chip build + connectivity (runs in .venv, where gdsfactory/cspdk are installed; skipped elsewhere)."""
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("gdsfactory")
pytest.importorskip("cspdk")

ROOT = Path(__file__).resolve().parent.parent


def test_chip_builds_and_nets_pass(tmp_path):
    subprocess.run([sys.executable, str(ROOT / "chip/opf_mzi4.py")], check=True, cwd=ROOT)
    gds = ROOT / "chip/gds/opf_mzi4_v0.1.gds"
    assert gds.exists()
    r = subprocess.run([sys.executable, str(ROOT / "chip/check_nets.py"), str(gds), "14"],
                       capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stdout
    assert "PASS" in r.stdout
