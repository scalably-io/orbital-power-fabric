#!/usr/bin/env python3
"""E018 — first-principles screen of synthesis candidates H1 and H3 (gates: docs/SYNTHESIS.md)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from opf import limits

B300_FP4, B300_FP8 = 187e-15, 560e-15      # R3-070, chip level, peak utilisation
LOSS_DB, BITS, T, LAYERS = 20.0, 5, 32, 8

print("SUPERSEDED by E025/E028 (scripts/efficiency_v2.py): every H1 row below combines resident weights with T=32 "
      "integration, which is physically inconsistent (R8-129, Stack.issues()). Kept as the logged E018 record only.\n")
print("H1 — resident-weight analog photonic pipeline (per MAC, fJ) [INVALID, see above]")
print("   inputs: non-volatile weights (hold 0, fetch 0), no activation SRAM (analog O-E-O),")
print(f"   DAC only at the first of {LAYERS} layers, T={T} integration, modulator 5 fJ/sample (R3-062: 1 fJ/bit x 5 bits)")
variants = {
    "NEP receiver (R3-037 rule), ADC every read": dict(detect_j=limits.R3_PRACTICAL_DETECT_J, wallplug=1.0, tia_j=2.4e-12, adc_j=2.19e-12),
    "photon->charge 1 fF/1 V, ADC every read":   dict(detect_j=limits.capacitive_detection_j(1e-15, 1.0), wallplug=0.4, tia_j=0.0, adc_j=2.19e-12),
    "photon->charge, ADC only at network output": dict(detect_j=limits.capacitive_detection_j(1e-15, 1.0), wallplug=0.4, tia_j=0.0, adc_j=2.19e-12 / LAYERS),
}
allow = []
for n in (128, 256):
    for name, kw in variants.items():
        s = limits.Stack(n=n, loss_db=LOSS_DB, dac_j=0.5e-12 / LAYERS, mod_j=5e-15, t_integrate=T, **kw)
        core = s.per_mac()["total"]
        s_max4, s_max8 = B300_FP4 / (10 * core), B300_FP8 / (10 * core)
        allow += [s_max4, s_max8]
        print(f"   N={n:3d} {name:44s} core {core*1e15:6.2f} fJ/MAC | vs B300 {B300_FP4/core:5.0f}-{B300_FP8/core:5.0f}x "
              f"| support overhead allowed for >=10x: {s_max4:4.1f}x (FP4) {s_max8:5.1f}x (FP8)")
MEASURED_SUPPORT = 318.0   # R3-045: full system / photonic core, the only measured full-stack processor
print(f"   Only measured full system (R3-045): support = {MEASURED_SUPPORT:.0f}x core -> H1 clears the 10x gate only if support")
print(f"   overhead is cut {MEASURED_SUPPORT/max(allow):.1f}x (best variant) to {MEASURED_SUPPORT/min(allow):.0f}x (worst) below that measured system.")

print("\nH3 — sunlight as the compute light source (brightness theorem, D18)")
for dnu in (1e12, 5e12):
    p_mode = limits.thermal_mode_power_w(5772, 1550e-9, dnu)
    print(f"   one single-mode input, {dnu/1e12:.0f} THz band: {p_mode*1e9:6.1f} nW (n = {limits.thermal_occupancy(5772, 1550e-9):.3f} photons/mode)")
    for n in (16, 128):
        per_output_w = p_mode / 10 ** (LOSS_DB / 10)         # an input's light is spread over n outputs,
        # but each output collects from n inputs -> per-output power ~ p_mode * n / n = p_mode (after loss)
        e_read = limits.capacitive_detection_j(1e-15, 1.0)    # best-case read energy at the detector
        rate = per_output_w / e_read
        print(f"      N={n:3d}: max 5-bit reads per output ~ {rate:9.3g} /s  (vs 1e10 /s for a 10 GS/s engine)")
