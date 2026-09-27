#!/usr/bin/env python3
"""E012 — what the 4x4 (and 8x8) test chip should measure, before it exists."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from opf import mesh

rng = np.random.default_rng(2026)
P_PI = {"R4-033 vendor <20 mW/pi": 0.020, "R4-156 measured 24.77 mW/pi": 0.02477}

for n, samples in ((4, 40), (8, 8)):
    powers = {k: [] for k in P_PI}
    for _ in range(samples):
        u = mesh.random_unitary(n, rng)
        ph, f = mesh.program(u, rng, restarts=10)
        assert f > 1 - 1e-6, f
        for k, ppi in P_PI.items():
            powers[k].append(mesh.heater_power_w(ph, ppi, n))
    print(f"N={n}: {len(mesh.layout(n))} MZIs, {mesh.n_phases(n)} heaters (incl. {n} output), {samples} random matrices")
    for k, vals in powers.items():
        m = float(np.mean(vals))
        print(f"  {k}: hold power mean {m:.3f} W (min {min(vals):.3f}, max {max(vals):.3f})")
        for rate in (1e9, 1e10):
            print(f"      heater-hold energy per MAC at {rate/1e9:>4.0f} GS/s input rate: {m/(n*n*rate)*1e12:7.3f} pJ/MAC")

print("\nCoupler imbalance (splitting ratio 0.5 +/- sigma per coupler), N=4:")
for sigma in (0.01, 0.03, 0.05):
    f_naive, f_cal, p_naive, p_cal = [], [], [], []
    for _ in range(10):
        u = mesh.random_unitary(4, rng)
        ph, _ = mesh.program(u, rng, restarts=10)
        splits = np.clip(0.5 + sigma * rng.standard_normal((len(mesh.layout(4)), 2)), 0.01, 0.99)
        real = mesh.unitary(4, ph, splits)
        f_naive.append(mesh.fidelity(real, u))
        p_naive.append(mesh.power_fidelity(real, u))
        pc, fc = mesh.program(u, rng, restarts=10, splits=splits)
        f_cal.append(fc)
        p_cal.append(mesh.power_fidelity(mesh.unitary(4, pc, splits), u))
    print(f"  sigma={sigma:.2f}: complex fidelity (simulation only) programmed-as-ideal {np.mean(f_naive):.4f} | "
          f"re-programmed {np.mean(f_cal):.6f}; MEASURABLE power fidelity {np.mean(p_naive):.5f} | {np.mean(p_cal):.6f}")
