#!/usr/bin/env python3
"""E025 → E028 — consistent photonic efficiency families (supersede E014/E015/E018).

E028 (Codex + Opus reviews):
- GPU reference: B300 board energy at max TGP on the roofline (memory- or compute-bound), never TGP + extra fetch
  (R3-070 notes: HBM is inside TGP). An UPPER bound on the GPU in decode.
- Photonic weight fetch = HBM access + the engine's own SRAM (R9-005 note), not the GPU's L2/L1 path.
- Precision pairs: 5-bit read-out vs NVFP4 (4-bit weights), 8-bit read-out vs FP8 (8-bit weights). Neither pair is
  shown to give equal model accuracy (open problem P10).
- Laser amortises over min(n, k) (D13 correction 3): H1' uses square, chainable n = k layers.
Every photonic figure is an optical-core budget (D13): its ratio to B300 is the support overhead the core could
absorb, not a system gain.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from opf import limits

B300 = {"FP4": 187e-15, "FP8": 560e-15}          # R3-070, chip level at max TGP and peak dense throughput
B300_TGP = 1400.0                                 # W, R3-067
B300_HBM_BPS = 576e12 / 72                        # B/s per GPU: GB300 NVL72 576 TB/s (R1-100) / 72 GPUs (R1-094), DERIVED
B300_PEAK_MAC = {"FP4": 15e15 / 2, "FP8": 5e15 / 2}   # dense MAC/s: FP4 15 PFLOPS (R3-068), FP8 5 PFLOPS (R3-069)
PAIRS = {"FP4": (4, 5), "FP8": (8, 8)}            # format -> (weight bits, read-out bits)
HBM, SRAM_BIT = 11.68e-12, 0.3e-12                # J/bit: GH200 HBM access (R3-078), SRAM (R3-062)
DAC = 1.56e-12                                    # J/sample, R8 measured GS/s DAC (8-bit figure, applied to 5-bit too)
TIA = 2.4e-12                                     # R3-062
ADC_6B = 2.19e-12                                 # R3-083 best measured >= 10 GS/s, >= 6 ENOB


def adc(bits: int) -> float:
    return ADC_6B * 2 ** max(0, bits - 6)         # Walden figure of merit: energy x2 per extra bit (ASSUMPTION)


OEO = 60.1e-15   # R7-046 NTT O-E-O in its cascadable gain mode (2.5 Gbit/s); no-gain 21.5 fJ/bit (R7-045). Measured per
                 # BIT (binary); used as a per-activation proxy — multilevel analog transfer is unmeasured (P8, P10).
                 # Includes optical energy the laser term also supplies -> conservative against photonics.
LAYERS, T_STREAM = 8, 32
DENSITY = 3183.0                                  # weights/mm2, R8-104 upper bound


def gpu_roofline(reuse: float, fmt: str) -> float:
    """B300 board energy per MAC at max TGP, at the roofline MAC rate (memory- or compute-bound)."""
    wbits = PAIRS[fmt][0]
    return B300_TGP / min(B300_PEAK_MAC[fmt], B300_HBM_BPS * reuse / (wbits / 8))


HBM_ALT = {"GH200 HBM access incl. control, measured (R3-078)": 11.68e-12, "HBM3E incl. IO, study value (R3-082)": 5.74e-12,
           "HBM3E, SK hynix via secondary citation (R3-081)": 3.44e-12}
# R3-080 (2.93 pJ/bit) is a refresh-based upper bound, not an access energy, so it cannot set a fetch floor (E034)


def decode_cap(e_bit: float, fmt: str = "FP8", reuse: float = 64) -> float:
    """Most a weight-streaming engine can gain over the B300 board in memory-bound decode if its compute were free:
    B300 roofline energy per MAC / the memory energy per MAC it must still pay (E033: shown for each HBM energy)."""
    wbits = PAIRS[fmt][0]
    return gpu_roofline(reuse, fmt) / (wbits * e_bit / reuse)


def nep_detect(bits: int) -> float:
    # R3-037 rule at 5 bits; an NEP (thermal-noise) limited receiver needs signal AMPLITUDE x2 per bit -> optical
    # power x2 per bit (x8 for +3 bits, R3-107 notes); E031 corrected the earlier x4 per bit (shot-noise scaling)
    return limits.R3_PRACTICAL_DETECT_J * 2 ** (bits - 5)


def pc_detect(bits: int) -> float:
    """Photon->charge node sized so shot noise supports `bits` (D11/D12): >= 4^b electrons, at least 1 fF x 1 V."""
    return max(limits.capacitive_detection_j(1e-15, 1.0), limits.shot_noise_detection_j(bits))


def family_s(fmt: str, reuse: float, n: int = 128) -> dict:
    wbits, rbits = PAIRS[fmt]
    s = limits.Stack(n=n, detect_j=nep_detect(rbits), loss_db=20, wallplug=1.0, dac_j=DAC, tia_j=TIA, adc_j=adc(rbits),
                     t_integrate=T_STREAM, weight_j=DAC, weight_reuse=reuse,
                     sram_j_per_mac=2 * 8 * SRAM_BIT / n, fetch_j_per_mac=wbits * (HBM + SRAM_BIT) / reuse)
    assert not s.issues(), s.issues()
    t = s.per_mac()
    gpu = gpu_roofline(reuse, fmt)
    return {"total": t["total"], "terms": t, "gpu": gpu, "bound": gpu / (wbits * HBM / reuse)}


def family_r(fmt: str, n: int, readout: str, loss_db: float = 20.0) -> dict:
    rbits = PAIRS[fmt][1]
    if readout == "nep":
        det, wp, tia = nep_detect(rbits), 1.0, TIA
    else:
        det, wp, tia = pc_detect(rbits), 0.20, 0.0            # 20% laser wall-plug (R8-072)
    s = limits.Stack(n=n, detect_j=det, loss_db=loss_db, wallplug=wp, dac_j=DAC / LAYERS, mod_j=OEO,
                     tia_j=tia / LAYERS, adc_j=adc(rbits) / LAYERS)   # DAC at layer 1, read-out at the network output
    assert not s.issues()
    t = s.per_mac()
    return {"core": t["total"], "terms": t, "ratio": B300[fmt] / t["total"], "support_for_10x": B300[fmt] / (10 * t["total"]),
            "cm2": n * n * LAYERS / DENSITY / 100}


# --- E032: realistic bracket as a correction ladder (one sourced change per step, cumulative) ---------------
NODE = {"FP4": (2e-15, 1.0), "FP8": (10.5e-15, 1.0)}   # R8-128: measured-parts node 2 fF (<= 6.8 bits at 1 V); 8-bit needs >= 10.5 fF
LAMBDA_REAL, QE_REAL = 1310e-9, 0.91                   # R8-128 (1,310 nm, QE 0.91), wavelength of the 20% laser (R8-072)
OEO_PD_J = 6.4e-15                                     # R7-046: optical energy into the O-E-O photodiode at its gain operating point


def ladder(fmt: str, n: int = 1024, rbits: int | None = None) -> list[tuple[str, float, float]]:
    """(step, core J/MAC, support allowed for 10x) — cumulative realistic corrections to the idealised H1'.
    rbits overrides the read-out bits paired with the format (sensitivity: E033)."""
    rbits = PAIRS[fmt][1] if rbits is None else rbits
    steps = []

    def add(label, detect_j, loss_db=20.0, tia=0.0, dist=False):
        if dist:   # D21: delivered light per MAC set by output-distribution precision, floor 2*E_min/k
            per_mac = max(limits.dist_photons_per_mac(rbits) * limits.photon_energy_j(LAMBDA_REAL) / QE_REAL, 2 * detect_j / n)
            detect_j = per_mac * n
        s = limits.Stack(n=n, detect_j=detect_j, loss_db=loss_db, wallplug=0.20, dac_j=DAC / LAYERS, mod_j=OEO,
                         tia_j=tia, adc_j=adc(rbits) / LAYERS)
        core = s.per_mac()["total"]
        steps.append((label, core, B300[fmt] / (10 * core)))

    ideal = pc_detect(rbits)
    c, v = (NODE["FP8"] if rbits > 6 else NODE["FP4"])
    add("idealised H1' (A4): full-scale precision, 1 fF / QE 1 / 1,550 nm node, 20 dB", ideal)
    node = max(limits.capacitive_detection_j(c, v, LAMBDA_REAL, QE_REAL),
               limits.shot_noise_detection_j(rbits, LAMBDA_REAL, QE_REAL))
    add("+ detector node from measured parts (R8-128)", node)
    oeo = max(node, OEO_PD_J)
    add("+ O-E-O at its measured operating point (R7-046)", oeo)
    add("+ precision over the output distribution (D21)", oeo, dist=True)
    add("+ buffer before the ADC at the network output (R3-062)", oeo, dist=True, tia=TIA / LAYERS)
    for loss in (26.0, 30.0):
        add(f"  … at {loss:.0f} dB optical loss instead of 20 dB", oeo, loss_db=loss, dist=True, tia=TIA / LAYERS)
    return steps


if __name__ == "__main__":
    print("Family S — streamed weights + T=32 integration, N=128 (weights pay DAC + HBM + own SRAM every use)")
    for label, reuse in (("decode, batch 64", 64), ("prefill, 2048-token reuse", 2048)):
        for fmt in PAIRS:
            r = family_s(fmt, reuse)
            t = r["terms"]
            print(f"  {label:26s} {fmt} (w{PAIRS[fmt][0]}/r{PAIRS[fmt][1]}): photonic core+memory {r['total']*1e15:7.1f} fJ/MAC "
                  f"(memory {t['memory']*1e15:.1f}, weights {t['weights']*1e15:.1f}, laser {t['laser']*1e15:.1f}) | B300 board roofline "
                  f"{r['gpu']*1e15:6.0f} -> {r['gpu']/r['total']:.2f}x (photonic support NOT included) | any streaming engine, free core: <= {r['bound']:.2f}x")

    print(f"\nFamily R — H1' resident non-volatile weights, square N x N layers (chainable), T=1, receiverless O-E-O "
          f"{OEO*1e15:.1f} fJ, DAC at layer 1 of {LAYERS}, read-out at the output")
    for n in (256, 1024):
        for fmt in PAIRS:
            for ro, lab in (("nep", "NEP receiver (R3-037 rule)"), ("pc", "photon->charge node")):
                r = family_r(fmt, n, ro)
                t = r["terms"]
                print(f"  N={n:4d} {fmt} {PAIRS[fmt][1]}-bit {lab:27s} core {r['core']*1e15:6.2f} fJ/MAC (laser {t['laser']*1e15:.2f}, "
                      f"DAC {t['dac']*1e15:.2f}, ADC {t['adc']*1e15:.2f}, O-E-O {t['modulator']*1e15:.2f}) | B300 {fmt} / core "
                      f"{r['ratio']:5.0f}x | support allowed for 10x: {r['support_for_10x']:5.1f}x (measured system 318x)")
        print(f"      {n}x{n} x {LAYERS} layers = {n*n*LAYERS:,} weights -> {n*n*LAYERS/DENSITY/100:,.1f} cm2 at {DENSITY:,.0f}/mm2 (R8-104 upper bound)")
    print("\nE032 realistic bracket — correction ladder, 1024 x 1024, cumulative (support allowed for 10x vs B300):")
    for fmt in PAIRS:
        for label, core, sup in ladder(fmt):
            print(f"  {fmt} {label:78s} core {core*1e15:8.2f} fJ/MAC | support allowed {sup:6.2f}x")
    r30 = family_r("FP4", 1024, "pc", loss_db=30.0)
    print(f"  loss sensitivity: N=1024 FP4 photon->charge at 30 dB instead of 20 dB -> core {r30['core']*1e15:.2f} fJ/MAC, "
          f"support allowed {r30['support_for_10x']:.1f}x")
