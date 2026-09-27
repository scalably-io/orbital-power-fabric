# R8 — Physics floors and best measured device energies for photonic MACs

Retrieved 2026-09-27. Ledger: `R8-physics-floors.csv` (150 rows: 138 claims + 12 ACCESS-FAILED). Every quote was machine-checked verbatim (whitespace-normalised) against the downloaded text in `evidence/sources/R8/` (`_build_r8_csv.py`, 0 mismatches). The arithmetic is in `_derive_r8.py`, with output in `_derive_r8.out.txt`.
Classes: MEASURED · VENDOR-STATED · STUDY-ASSUMED (a paper's analysis or estimate) · DERIVED (my arithmetic, formula in the notes) · PROJECTED.

## (a) Verdict

1. **The photonic-specific terms are no longer the floor; the converters and memory are.** From measured parts, a time-integrating photonic engine (T = 32, N = 128, 8-bit) spends about **1.2 fJ/MAC on laser plus read-out**. It spends **12 fJ on the input DAC** (1.56 pJ/sample ÷ N), **19 fJ on activation SRAM** and **46 fJ on HBM weight fetch** (prefill). DERIVED, R8-130–R8-135.
2. **Best-achievable system energy from measured parts, prefill:** 8-bit is **62–111 fJ/MAC** at N = 256–64 (78 fJ at N = 128). 4-bit is **35–67 fJ/MAC** (45 at N = 128). **Decode at batch 64: ~1.5 pJ/MAC (8-bit), of which HBM is 96%.** All of these EXCLUDE control, nonlinearities, calibration and host. In the only measured full photonic system, those items cost 318× the core (R3-045).
3. **D13 has a physical inconsistency.** Time integration over T cycles needs the weights to change every cycle. So T > 1 forces streamed weights: a DAC plus modulator per weight symbol, shared across fan-out B. Non-volatile "zero-hold" weights cannot be combined with T = 32 (R8-129). E014/E015 L1 + L2 must add a weight-encoding term (E_DAC + E_mod)/B.
4. **Non-volatile photonic weights cannot hold an LLM.** Measured densities are 5.8–3,183 weights/mm², against 4.76 M/mm² for 2 nm SRAM. That puts 72.7 B weights at 23–12,500 m² of photonics (R8-124). Time-sharing one crossbar wears out memresonator, PCM and ferroelectric cells within one model pass. Magneto-optic cells last about 541 passes (R8-125).
5. **The shot-noise floor is real but not binding.** Per read it is 4^b photons: 38.8 aJ at 4 bits and 9.94 fJ at 8 bits (1310 nm). Measured sub-photon-per-MAC results (0.038–3.2 photons/MAC) come from fan-in over ~10²–10⁵ terms at kHz–10 MHz. They do not come from beating the per-read floor (R8-013, R8-018).
6. **Converter floors are empirical and stubborn.** No ADC with ≥ 4 ENOB at ≥ 100 MS/s has gone below 0.78 pJ per conversion in 30 years of ISSCC/VLSI. The best 2023–26 figures are 1.06 pJ (≥ 4 ENOB) and 4.19 pJ (≥ 8 ENOB) (R8-060–R8-066). The only measured GS/s DAC is 1.56 pJ/sample including its driver (R8-069).
7. **The measured laser wall-plug efficiency for the silicon-photonics band is 20%** (1310 nm DFB, 75 °C), not the 40% used in E014/E015. Comb sources are 1.1–5.6% (R8-072, R8-074, R8-075).

## (b) Floor table per component (4-bit and 8-bit)

Photon energy at 1310 nm = 0.1516 aJ. Floors are physics (D11/D12). "Best measured" means a device measurement, 2023–26 where available.

| Component | Physics floor, 4-bit | Physics floor, 8-bit | Best measured, 4-bit class | Best measured, 8-bit class | claim_ids |
|---|---|---|---|---|---|
| Optical energy at detector, per read | 256 photons = 38.8 aJ (QE 1) | 65,536 photons = 9.94 fJ | 506 photons/read gave 4 noise-equivalent bits (6% RMS), 2× floor [MEASURED, 10 MHz free-space]. TIA-limited 1,654 photons = 0.25 fJ [DERIVED from measured TIA noise]. Receiverless 2 fF at 1 V: 13,720 photons = 2.08 fJ [DERIVED] | TIA-limited 85,148 photons = 12.9 fJ; receiverless ≥ 10.5 fF at 1 V: 10.92 fJ (QE 0.91) [DERIVED]. Both are shot-dominated | R8-012, R8-013, R8-050, R8-052, R8-127, R8-128 |
| Per-MAC optical floor (N·T = 4096, η = 1, 0 dB) | 0.0095 aJ | 2.43 aJ | Netcast integrating receiver ~10 aJ/MAC (~100 photons, M = 100) [MEASURED] | — | R8-016, R8-127 |
| Detector node, kT/C at 300 K | — | — | 2 fF integrated O-E-O node (18 e⁻ rms). A 4-bit read needs ≥ 443 e⁻ (35.5 mV swing) because kT/C exceeds the 16 e⁻ shot noise | 10 fF commercial Ge PD with parasitics: 40 e⁻ rms, below the 256 e⁻ shot noise | R8-026, R8-055, R8-059, R8-128 |
| Laser wall-plug η | no sourced floor | same | DFB 1310 nm 20% (>100 mW, 75 °C). VCSEL 940 nm 61.3% CW, 74% ns-pulsed. Comb 1.1–5.6% | same | R8-072, R8-074–R8-077 |
| Modulator, per symbol | → 0 as C·V² → 0 (no sourced bound) | same | Si MRM 0.97 fJ/bit (0.43 Vpp, C estimated) [STUDY-ASSUMED]. TFLN 2.07 fJ/symbol (O-band PAM8) [DERIVED]. Plasmonic 0.23 fJ/bit at 4 K, 25 fJ/bit at 128 GBd. VCSEL < 5 aJ/symbol | No 8-bit-linear analog modulator energy found. Assumed equal to the per-swing C·V²/4 | R8-036, R8-042–R8-044, R8-046 |
| DAC, per sample | no sourced floor | — | none measured at 4 bits (8-bit number used) | 1.5625 pJ (8b, 160 GS/s, incl. driver) [DERIVED from 0.25 W] | R8-068, R8-069, R8-150 |
| Receiver amplifier, per read | 0 (receiverless) | 0 | TIA 165 fJ per read (56 GBd, 9.22 mW). Receiverless reset C·V² = 2 fJ (2 fF, 1 V) [DERIVED] | same TIA; reset 10.5 fJ (10.5 fF) | R8-050, R8-052, R8-128 |
| ADC, per conversion | thermal-noise-limited power × 4 per bit (authors' rule) | — | 1.0625 pJ (6.6 ENOB, 4.8 GS/s). All-years room-temperature floor 0.96 pJ | 4.194 pJ (9.7 ENOB, 1.8 GS/s). At ≥ 10 GS/s: 14.98 pJ | R8-034, R8-060–R8-066 |
| SRAM, per bit | — | — | GH200 L1 datapath 0.29 pJ, total 1.45 pJ [MEASURED]. 7 nm 8 KB 117 fJ [VENDOR-STATED] | same | R8-078, R8-079, R8-081 |
| HBM, per bit | — | — | 11.68 pJ (GH200, total) | same | R8-080 |
| Non-volatile weight write | — | — | Memresonator 0.15 + 0.36 pJ (1,000 cycles). Magneto-optic 143 fJ/bit (volatile electromagnet demo). BTO 4.6–26.7 pJ. Sb₂S₃ 35 nJ / 0.48 mJ | same (5-bit PCM is non-volatile; 7-bit needs a live heater) | R8-095, R8-101, R8-102, R8-109, R8-115, R8-116 |
| Digital reference, 8-bit MAC | Landauer < 0.1 aJ (8-bit multiply) | — | — | 7 nm int8 multiply + add ≈ 77 fJ, arithmetic only [VENDOR-STATED + DERIVED] | R8-005, R8-082 |
| "Bits" convention (analog photonic link) | SNR convention: shot noise 6 dB/bit (4^b), thermal 3 dB/bit | — | Tait's SFDR convention: shot 9 dB/bit, thermal 4.5 dB/bit. His 8-bit shot floor is 3.9 pJ, about 460× D11 at the same 1550 nm (8.40 fJ) | — | R8-028–R8-031 |
| RIN, −155 dB/Hz | SNR convention: 8.8 bits at 10 GHz, 11.3 bits at 312 MHz [DERIVED] | — | Tait's SFDR convention: 8 bits only up to 410 MHz | — | R8-032, R8-033 |

## (c) Best-achievable system energy per MAC from measured parts — DERIVED

**Formula.** This is D13 with T applied to the read-out and the output write, plus the weight-encoding term that D13 is missing:

E/MAC = E_det·10^(L/10)/(η·N·T) + E_DAC/N + E_mod/N + (C·V² + E_ADC)/(N·T) + b·E_SRAM/N + b·E_SRAM/(N·T) + (E_DAC + E_mod)/B + b·E_HBM/B

**Inputs, all measured or derived from measured values:**

| Symbol | Value | Source |
|---|---|---|
| λ | 1310 nm | band of the laser and detector measurements |
| QE | 0.91 | R8-054 |
| η | 0.20 | R8-072 |
| L | 10 dB | ASSUMPTION (optimistic build-up): 0.9 dB coupling (R8-073) + 1.5 dB weight element (R8-107) + 3 dB mean weight transmission + margin. No measured laser-to-detector loss for an N ≥ 64 crossbar was found. 20 dB shown as sensitivity |
| E_det | 2.08 fJ (4-bit: 2 fF at 1 V); 10.92 fJ (8-bit: shot-limited, 10.5 fF at 1 V) | R8-128 |
| E_DAC | 1.5625 pJ | R8-069 |
| E_mod | 0.97 fJ | R8-036 |
| E_ADC | 1.0625 pJ (4-bit); 4.194 pJ (8-bit) | R8-060, R8-062 |
| E_SRAM | 0.29 pJ/bit | R8-079 |
| E_HBM | 11.68 pJ/bit | R8-080 |
| T | 32 | ≤ the M = 100 measured by Netcast, R8-016 |
| b | 4 or 8, used for both activations and weights | — |

**Worked example: 8-bit, N = 128, T = 32, prefill with every weight symbol fanned out to B = 2048 tokens.**

| Term | Arithmetic | fJ/MAC |
|---|---|---|
| Laser | 65,536/0.91 × 0.1516 aJ = 10.92 fJ; × 10 (10 dB) ÷ 0.20 ÷ 4096 | 0.133 |
| Input DAC | 1,562.5 fJ ÷ 128 | 12.21 |
| Input modulator | 0.97 fJ ÷ 128 | 0.008 |
| Read-out | (10.5 fJ reset + 4,194 fJ ADC) ÷ 4096 | 1.026 |
| Activation SRAM | 8 × 0.29 pJ ÷ 128 (read) + 8 × 0.29 pJ ÷ 4096 (write) = 18.13 + 0.57 | 18.69 |
| Weight encoding | (1,562.5 + 0.97) fJ ÷ 2048 | 0.763 |
| Weight fetch, HBM | 8 × 11.68 pJ ÷ 2048 | 45.63 |
| **Total** | | **78.45** |

**Sweep (fJ/MAC, L = 10 dB, SRAM 0.29 pJ/bit):**

| Case | 4-bit N=64 | 4-bit N=128 | 4-bit N=256 | 8-bit N=64 | 8-bit N=128 | 8-bit N=256 |
|---|---|---|---|---|---|---|
| Prefill, weight fan-out B = 2048, T = 32 | 67.3 | 45.4 | 34.5 | 110.5 | 78.5 | 62.4 |
| Prefill, fan-out only 64 (weights staged in SRAM, re-read per 64) | 109.1 | 87.2 | 76.3 | 170.4 | 138.4 | 122.3 |
| Decode, batch 64, T = 32 | 798 | 776 | 765 | 1,549 | 1,516 | 1,500 |
| Weight-resident crossbar, T = 1, no weight traffic (area-infeasible, see d) | 78.9 | 39.5 | 19.7 | 171.2 | 85.6 | 42.8 |
| Prefill, T = 1 (no time integration) | 102.5 | 63.0 | 43.3 | 217.5 | 132.0 | 89.2 |

**Sensitivity, 8-bit, N = 128, prefill B = 2048:**
- 20 dB loss gives 79.7 fJ. The laser goes from 0.13 to 1.33 fJ.
- 20 dB loss with realistic SRAM (1.45 pJ/bit, GH200 L1 total) gives 154.4 fJ, with SRAM at 93.5 fJ (R8-138).

**Reading it:**
- Photonic compute, excluding SRAM and HBM, is 14.1 fJ/MAC at 8 bits (N = 128, T = 32). That is about 5.4× below a 7 nm digital int8 MAC's arithmetic, 77 fJ (vendor-stated, no data movement).
- The input DAC is 86% of that 14.1 fJ. Direct O-E-O between layers (E014 L3) would remove it, but has only fJ-level binary demonstrations (R8-059).
- Against B300 at peak (R3-070: 560 fJ/MAC FP8, 187 FP4, chip-level, including HBM and control), the bottom-up 78 fJ looks 7× better. But the photonic number excludes control, softmax/LayerNorm, calibration and I/O. It is also a stack that has never been built.
- In decode, HBM makes photonic and GPU equal to first order, as R3 found.

## (d) Weight density and analog-depth limits

**Non-volatile photonic weights (measured). Densities are DERIVED from footprint; areas are for all 72.71 B Qwen2.5-72B weights (E005), one weight per cell.**

| Technology | Cell | Levels | Write energy / speed | Endurance | Retention | Weights/mm² | Area for 72.7 B | claim_ids |
|---|---|---|---|---|---|---|---|---|
| Memresonator (HfO₂ on III-V/Si ring) | 20 µm diameter ring, 0.18π shift | 3 states | 0.15 / 0.36 pJ, 0.3–0.9 ns | 1,000 | 12 h | ≤ 3,183 (ring only) | 22.8 m² | R8-101–R8-104 |
| MEMS phase shifter (volatile, electrostatic) | 100 × 45 µm, 0.33 dB | continuous | < 40 pJ reconfiguration, 2 µs; < 10 fW standby | n/r | holds while biased | 222 | 327 m² | R8-121–R8-123 |
| Magneto-optic Ce:YIG ring, CoFeB non-volatile | r = 50 µm | ≥ 11 (~3.5 bit) | 143 fJ/bit at 1 ns (volatile demo); NV cell > 200 mA | 2.4 × 10⁹ | 4 days | ≤ 127 | 571 m² | R8-094–R8-100 |
| Ferroelectric HfAlO ring | 5 µm projected | 3 | 5 V pulses | 4 × 10⁴ | 1,000 s measured, > 10 y extrapolated | 2,500 (projected) | — | R8-111–R8-114 |
| PCM tensor core (GST on SiN crossings) | 285 × 354 µm MAC cell | 5-bit | nJ-scale (R3) | — | — | 9.9 | 7,336 m² | R8-117, R8-118 |
| PCM Sb₂S₃ ring | n/r | 22 NV (5-bit); 127 with live heater | 35 nJ / 0.48 mJ | > 2,000 events | — | — | — | R8-115, R8-116 |
| BTO non-volatile mesh (Nature Photonics 2026) | 950 µm unit cell, 1.48 dB | multilevel | 80 ns; 560 nW per π static | 10⁹–10¹² (cited, not measured) | TEC needed | 5.8 | 12,536 m² | R8-092, R8-105–R8-108 |
| TSMC N2 SRAM (reference) | 0.021 µm² bitcell | 8-bit | — | ∞ | — | 4.76 M | 0.015 m² | R8-083, R8-084 |

**Consequences (DERIVED):**
- Photonic weight-resident LLM inference is ruled out by area, by 3–6 orders of magnitude.
- Re-tiling one 128×128 non-volatile crossbar across the model means 4.44 M rewrites per cell per full pass. Memresonator, PCM and HfAlO cells wear out before one pass completes. Magneto-optic cells survive about 541 passes, roughly 35 k tokens at batch 64 (R8-125).
- A Clements mesh of depth N built from measured non-volatile elements loses 189 dB (BTO) or 42 dB (MEMS) at N = 128. Only architectures with one weight element per optical path are viable (R8-126).
- Weights must therefore be streamed by modulators. That is the (E_DAC + E_mod)/B term in (c).

**Analog depth:**
- Theory says noise accumulation is bounded, and suppressed when the activation slope is below 1 (R8-085). It was not tested on transformer blocks.
- With unity-slope propagation and independent per-stage noise, error grows as √L and costs ½·log₂L bits: 2.5 bits at L = 32, 3.2 at L = 80, 4.2 at L = 320 (R8-093, DERIVED). Digital re-quantisation between layers resets this.
- In MZI meshes, error grows with depth O(N). Correction reduces it quadratically but it still grows (R8-086, R8-087). The 3-splitter design removes the size dependence in theory only (R8-088).
- Measured: a 6-mode mesh reached fidelity 0.900 with direct programming and 0.987 after error correction (R8-090). That calibration used 300 × 100 = 30,000 input/output measurements (R8-091).
- Lightmatter recalibrates once per hour (R8-035). The non-volatile BTO mesh still needs a TEC (R8-092). No source reports calibration energy.

## (e) Negative findings

- **Sub-photon/MAC is a fan-in effect, not a floor breach.** Wang's 0.001 photons/MAC was 506 photons per read, giving 4 bits. It ran at ≥ 10 MHz with attenuated light (R8-012, R8-013). Netcast's < 1 photon/MAC ran at 30 kHz on SNSPDs (R8-018). McMahon notes that electrical fan-in achieves similar efficiency (R8-021).
- **Headline modulator fJ/bit figures are calculated, not measured energies.**
  - MRM 0.97 fJ/bit uses an estimated 21 fF and excludes the driver and heater lock at 81 pm/mW (R8-036–R8-038).
  - TFLN 0.69 fJ/bit is termination dissipation, excluding the driver (R8-040).
  - Plasmonic 230 aJ/bit is at 4 K, sub-FEC, with estimated C, and costs 5.9 dB of optical loss (R8-043, R8-045).
  - A complete measured VCSEL transmitter costs 1.3 pJ/bit (R8-070).
- **"Full-system 7 fJ/OP" (VCSEL ONN) is a component sum** of measured optics and literature ~1 pJ ADC/TIA/DAC values (R8-047).
- **There is no measured 4-bit GS/s DAC, and no DAC survey exists.** The 8-bit number is used for 4-bit inputs (R8-069, R8-150).
- **Low-rate ADCs are not cheaper in recent literature.** The best 0.1–1 GS/s design at ≥ 4 ENOB is 3.6 pJ (cryogenic) or 5.2 pJ (room temperature), because recent papers target 10–12 bits (R8-065).
- **8-bit reads at ≥ 10 GS/s cost ~15–37 pJ per conversion** (R8-063, R8-065). 8-bit photonics needs time integration.
- **The magneto-optic "143 fJ, 1 ns" figure is the volatile electromagnet demo.** The non-volatile CoFeB cell needs > 200 mA and a 50 µm ring (R8-095–R8-098).
- **SFDR-convention analyses put the 8-bit floor about 460× above D11** (same wavelength), and cap 8-bit bandwidth at 410 MHz from RIN (R8-031, R8-032). The D11 SNR convention is the optimistic one.
- **Cooling does not help total energy** once the Carnot cost is paid. This is relevant to branch E (R8-008).
- **Measured wall-plug efficiency is 20% for the silicon-photonics band,** half the 40% assumed in R3-037 and E014/E015 (R8-072).
- **SRAM measured at GPU level is 1.45 pJ/bit total, 5× the 0.3 pJ/bit in D13/E014.** Only the datapath part, 0.29 pJ/bit, matches it (R8-078, R8-079).

## (f) Failed sources and open questions

**ACCESS-FAILED (12):**
- NTT 2016 Optica full text (bot wall; abstract used) and NTT 2019 Nature Photonics full text (paywalled, so the attojoule modulator value is missing). R8-139, R8-140.
- Geler-Kremer 2022 BTO primary (values carried second-hand). R8-141.
- Gao 2025 MDPI (HTTP 403; Crossref abstract used). R8-142.
- MEMS arrays, Nature Photonics 2023 full text. R8-143.
- DFB, Optical Engineering 2023 full text. R8-144.
- Lumentum CLEO 2022 PDF. R8-145.
- The BTO "9 fJ/bit" modulator (source not located; number not used). R8-146.
- Si MRM 5.3 fJ/bit, CLEO 2021. R8-147.
- Nahmias, JSTQE 2020. R8-148.
- Measured SRAM energy per bit at 3/2 nm. R8-149.
- A DAC survey. R8-150.
- Partial: ISSCC 2024 session 18 was read from a third-party copy of the digest, not IEEE Xplore (R8-068–R8-071).

**Open questions:**
1. Which "bits" convention (SNR or SFDR) predicts transformer accuracy on analog hardware? It moves the 8-bit floor by about 460×.
2. The energy of an 8-bit-linear analog modulator symbol, and of a 4-bit DAC at GS/s. Neither was found.
3. The largest optical fan-out B of one weight symbol that has been demonstrated. The prefill figure moves from 78 to 138 fJ/MAC between B = 2048 and B = 64.
4. Calibration energy and time as a function of N. It is reported as a cadence (hourly) or a sample count (30,000 at N = 6), never in joules.
5. A measured receiverless node below 2 fF that includes the transistor gate. 300 aF is a proposal (R8-023).
6. The measured 8-bit error of cascaded analog layers at depth ≥ 10 inside a transformer block. The error growth rate is only simulated.
7. D13 should gain a weight-encoding term, and E014/E015 L1 + L2 should be re-derived with streamed weights (R8-129). That is for the orchestrator; `opf/` was not touched.
