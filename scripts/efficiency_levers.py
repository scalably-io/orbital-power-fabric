#!/usr/bin/env python3
"""E014 — how much more efficient can photonic MVM get, lever by lever? (DERIVED from R3 inputs)"""
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from opf import limits

N, BITS = 128, 5
today = limits.Stack(
    n=N, detect_j=limits.R3_PRACTICAL_DETECT_J, loss_db=20, wallplug=1.0,   # R3-037 rule
    dac_j=0.5e-12,                      # R3-038 (low end of 0.5-1 pJ)
    tia_j=2.4e-12,                      # R3-062 list
    adc_j=2.19e-12,                     # R3-083 best measured >=10 GS/s, >=6 ENOB
    hold_j_per_mac=83e-15,              # R3-102 1.66 mW/pi, crossbar amplitude MZI: mean phase pi/2 (D14) at 10 GS/s
    sram_j_per_mac=2 * 8 * 0.3e-12 / N, # R3-062 SRAM 0.3 pJ/bit
    fetch_j_per_mac=8 * 11.68e-12 / 64, # R3-078 HBM 11.68 pJ/bit, 8-bit weights, batch 64
)
steps = [
    ("L0 today's best parts (decode, batch 64)", today),
    ("L1 + non-volatile weights (no hold power)", replace(today, hold_j_per_mac=0.0)),
]
steps.append(("L2 + time-integrating read-out T=32", replace(steps[-1][1], t_integrate=32)))
steps.append(("L3 + direct O-E-O between layers (no DAC)", replace(steps[-1][1], dac_j=0.0)))
steps.append(("L4 + weights reused over 2048 tokens", replace(steps[-1][1], fetch_j_per_mac=8 * 11.68e-12 / 2048)))
# POST-HOC (added after first run, E014 amendment): photon -> charge directly on a 1 fF node at 1 V,
# no TIA (tia_j = 0), laser sized for that node instead of the NEP-limited receiver; 40% wall-plug.
steps.append(("L4b + direct photon->charge read (1 fF, 1 V, no TIA) [post-hoc]",
              replace(steps[-1][1], detect_j=limits.capacitive_detection_j(1e-15, 1.0), wallplug=0.4, tia_j=0.0)))
floor = limits.Stack(n=N, detect_j=limits.shot_noise_detection_j(BITS), loss_db=20, wallplug=0.4)
steps.append(("L5 physics floor: shot noise only (20 dB, 40% wall-plug)", floor))

# Precision-matched GPU refs (R3-070, DERIVED from NVIDIA-stated 1,400 W max TGP at peak dense
# throughput): B300 NVFP4 93.3 fJ/FLOP = 187 fJ/MAC, FP8 280 fJ/FLOP = 560 fJ/MAC, chip level, 100%
# utilisation (GPU best case). 5-bit analog read-out sits between FP4 and FP8 in precision.
B300_FP4, B300_FP8 = 187e-15, 560e-15
FETCH_DECODE = 8 * 11.68e-12 / 64          # same 8-bit weight fetch the photonic stack pays (R3-078)
GPU_DECODE = (FETCH_DECODE + B300_FP4, FETCH_DECODE + B300_FP8)
print(f"N={N}, {BITS}-bit read-out. fJ per MAC. GPU refs: B300 FP4 {B300_FP4*1e15:.0f} / FP8 {B300_FP8*1e15:.0f} fJ (reuse); "
      f"decode {GPU_DECODE[0]*1e15:.0f}-{GPU_DECODE[1]*1e15:.0f} fJ (same 8-bit fetch + FP4..FP8)")
hdr = ["laser", "dac", "tia", "adc", "weight_hold", "sram", "memory", "total"]
print(f"{'step':58s}" + "".join(f"{h:>10s}" for h in hdr))
print("SUPERSEDED by E025/E028 (scripts/efficiency_v2.py). Rows marked INVALID combine T>1 with no streamed-weight "
      "energy (Stack.issues(), R8-129), and the GPU decode reference below adds HBM fetch to a TGP figure that already contains it (E028); kept only as the logged E014/E015 record, not as results.")
for name, s in steps:
    t = s.per_mac()
    flag = "  INVALID" if s.issues() else ""
    print(f"{name:58s}" + "".join(f"{t[h]*1e15:10.2f}" for h in hdr) + flag)

print("\nMatrix size sweep — photonic stack is bottom-up and EXCLUDES digital control/nonlinearity/calibration")
print("(the only measured full system spent 318x its core energy on those, R3-045); GPU refs include everything on the board:")
for n in (64, 128, 256, 512):
    l3 = replace(steps[3][1], n=n, sram_j_per_mac=2 * 8 * 0.3e-12 / n).per_mac()["total"]
    l4 = replace(steps[4][1], n=n, sram_j_per_mac=2 * 8 * 0.3e-12 / n).per_mac()["total"]
    l4b = replace(steps[5][1], n=n, sram_j_per_mac=2 * 8 * 0.3e-12 / n).per_mac()["total"]
    print(f"  N={n:4d}: decode L3 {l3*1e15:7.1f} fJ ({GPU_DECODE[0]/l3:3.2f}-{GPU_DECODE[1]/l3:3.2f}x) | "
          f"reuse L4 {l4*1e15:6.1f} fJ ({B300_FP4/l4:3.1f}-{B300_FP8/l4:3.1f}x) | "
          f"L4b {l4b*1e15:5.1f} fJ ({B300_FP4/l4b:3.1f}-{B300_FP8/l4b:4.1f}x)  [x = GPU/photonic, FP4..FP8]")

print("\nReceiver gap: practical 5-bit detection (R3-037 rule) needs "
      f"{limits.R3_PRACTICAL_DETECT_J/limits.shot_noise_detection_j(BITS):.0f}x the shot-noise photons; "
      f"a 1 fF / 1 V capacitive node needs {limits.capacitive_detection_j(1e-15, 1.0)/limits.shot_noise_detection_j(BITS):.1f}x")
print(f"Physics floor {steps[-1][1].per_mac()['total']*1e15:.2f} fJ/MAC = {B300_FP4/steps[-1][1].per_mac()['total']:.0f}x below B300 FP4")
