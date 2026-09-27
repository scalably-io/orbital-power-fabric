# R7: conversion as compute (photon→electron "transformation gates")

Retrieved 2026-09-27. Ledger: `R7-conversion-as-compute.csv` has 112 rows: 102 evidence claims and 10 ACCESS-FAILED. A script checked every quote verbatim against the downloaded source text (`evidence/sources/R7/_build_csv.py`); 0 quotes were missing and 0 were fuzzy matches. `scripts/validate_evidence.py` reports 0 rejects.

Classes: MEASURED · VENDOR-STATED · STUDY-ASSUMED (a paper's estimate built from assumed or literature values) · DERIVED (my arithmetic, formula in the CSV notes) · PROJECTED.
Budget baseline: the R3 bottom-up per-MAC budget at N = 128 (R3-105/106). All of its terms are **per MAC**. In decode it totals 1.62–1.80 pJ/MAC for accelerator + HBM, of which HBM is 1.46 pJ.

## (a) Verdict

1. **Yes, the conversion can do three useful jobs, and each has been shown on hardware.**
   - **Accumulate.** The detector integrates charge, so one ADC read covers 100 to 131,072 MACs (R7-002, R7-013).
   - **Sign.** Balanced detection gives signed weights (R7-014, R7-043).
   - **Activate.** A photodiode drives a modulator directly, with no receiver: 30 fJ per activation, against ~3 pJ with a TIA (R7-037/038). NTT's femtofarad O-E-O device costs 21.5 fJ/bit and reaches an optical gain of 1.8–2.4 (R7-045/047).
2. **No such system has a measured wall-plug energy per MAC.** Only optical energies (40 aJ/MAC, 0.038 photons/MAC) and single-device energies are measured. The papers' electrical "full-system" figures are component budgets built from literature ADC/DAC/memory values: 10 fJ/MAC, 7 fJ/OP, and 6.5 fJ/OP (the last projected) (R7-004/018/015).
3. **Decode barely moves.** The terms these devices remove (ADC, TIA, activation SRAM, DAC) are 5–10% of the R3 decode budget. Decode goes from 1.62–1.80 to 1.54–1.62 pJ/MAC at best (DERIVED, R7-100), because HBM weight streaming is untouched.
4. **Prefill gains are real but at low precision.** Prefill goes from 0.20–0.39 to 0.12–0.26 pJ/MAC (DERIVED, R7-098/100), still at 5-bit detection.
5. **Several designs move conversions rather than remove them.**
   - Time-division integrators cut ADC reads 131,072× but need 2 DAC samples per MAC, i.e. 1–2 pJ/MAC if nothing is shared (DERIVED, R7-017).
   - Netcast shifts weight modulation onto the server.
   - The VCSEL network's 7 fJ/OP amortises only the input side of the computation.
6. **Ranking** (DERIVED, section c):
   - (1) Receiverless O-E-O activation, next tier.
   - (2) Time-integrating or charge-domain readout, current-to-next tier. The one measured charge-domain chip reaches 11.9 fJ/op at the accelerator and 0.22 pJ/op at SoC level (1-bit-normalised, R7-080/081).
   - (3) All-optical χ(2)/photonic-crystal activations at 16–80 fJ, speculative: they need a femtosecond pump and none has been cascaded.
7. **Sunlight-driven compute works only for digital logic.** A memristor binarized network (BNN) ran with no regulator from 0.08 to 8 suns. The authors state that analog MACs need a regulated supply (R7-084/086/088).
8. **CORNERSTONE:**
   - The passive + heater run lists no photodetector, so none of the electrical gates can be built on it (R7-093).
   - The active run has modulators and 4 implants but lists no Ge photodetector.
   - Detection there needs the bonded-photodiode service (R4-043) or the unverified graphene beta service (R7-095).

## (b) Approaches compared

| Approach (source) | Conversions removed | Measured energy (what it includes) | Precision | Speed | Layers cascaded | Tier | claim_ids |
|---|---|---|---|---|---|---|---|
| Time-integrating WDM receiver, incoherent (Netcast) | ADC ÷100 (M = 100); TIA replaced by integrator; client holds no weights | **40 aJ/MAC optical at receiver** (MEASURED); client electrical ≈10 fJ/MAC is a literature model, server-side weight modulation excluded | ≈8 bit (scalar mults) | 1 kHz deployed; SNSPD run at 30 kHz, 0.8 K | 3-layer MLP; between layers digital | next (off-the-shelf 10 pF integrator IC) | R7-001…006 |
| Charge-integration balanced receiver, time-division (TFLN, 120 GOPS) | ADC ÷131,072; signed accumulation in one pass; **adds 2 DAC samples per MAC** | none measured; 6.5 fJ/OP PROJECTED for an unbuilt 64λ × 64-core version (laser, DACs, integrators, CMOS switches) | 6.04 bit | 60 Gbaud, 120 GOPS | 4-layer MLP, digital between | next | R7-011…017 |
| Coherent VCSEL homodyne + time integration | ADC ÷784; DAC and memory ÷81 (input side only) | 7 fJ/OP STUDY-ASSUMED (ADC/TIA 1 pJ, DAC 0.5 pJ, memory 100 fJ from literature); batch-1 weight side ~0.5 pJ/OP DERIVED | ~6 bit | 100 MS/s used (1 GS/s max) | 3 layers, digital serialisation | next | R7-018…025 |
| Multiport Ge PD sums 16 waveguides on one detector | ADC ÷16; no WDM needed | none | n/a | 11.8 GHz (16-port) | 3-layer Iris, digital between | next (AMF) | R7-027…029 |
| Photon counting; single-photon-detector click = activation | TIA; multi-bit ADC (binary click) | 0.038 photons/MAC; 0.64 photons per multiplication at ~90% (optical only) | binary, stochastic | ≥10 MHz | 1 hidden layer | speculative | R7-006, R7-008…010 |
| Charge-domain MAC in switched-capacitor readout (MANTIS imager SoC) | per-pixel ADC → MAC before one SAR ADC per group | **11.9 fJ/op accelerator** (analog memory, SC amplifiers, SAR ADCs, drivers); **0.22 pJ/op SoC** (+ imager, CPU, SRAM); both MEASURED, 1-bit-normalised | 4b weights, RMSE 3–11% | 29 fps | 1 conv stage | **current** (0.11 µm CMOS) | R7-080…083 |
| Receiverless O-E-O activation (FICONN NOFU: photodiode → pn microring) | TIA, ADC, DAC, SRAM between layers | 30 fJ/activation electrical (author estimate from measured 75 µA) + ~75 fJ optical tap (DERIVED); ~3 pJ if a TIA is added | n/a | 435 ps inference (layout estimate) | **3 matrix layers + 2 NOFU layers**, N = 6 | next (Elenion commercial process) | R7-037…042 |
| Photodiode sum → off-chip TIA → microring ReLU (Ashtiani PDNN) | ADC, DAC, memory, clock (TIA kept, 7 off-chip) | none reported; supply laser 2.5 mW | 93.8 / 89.8% accuracy | <570 ps (from component bandwidths) | **3 layers**, clock-less | next (AMF 180 nm) | R7-032…036 |
| Balanced PD wired to microring modulator (Tait) | TIA, ADC, DAC | none; on-chip O/O gain 1.36 | n/a | injection-mode ring | 1 neuron (autapse) | next | R7-043/044 |
| Femtofarad O-E-O transistor (NTT InP photonic crystal, 2 fF) | amplifier, ADC, DAC | **21.5 fJ/bit total** (1.6 optical PD + 3.2 electrical + 16.7 optical EOM) at 10 Gb/s, η = 0.6; 60.1 fJ/bit with gain 2.3 at 2.5 Gb/s; PD alone 4.8 fJ/bit; EOM 42 aJ/bit | binary switching | 3.3 GHz | cascadable repeater (gain 1.8–2.4) | next (III-V) | R7-045…050 |
| Amplified EO activation (design study) | ADC, DAC | 100 mW circuit → 10 pJ/activation (STUDY-ASSUMED) | — | 10 GHz | model | reference | R7-051/052 |
| RTD photodetector + VCSEL spiking neuron | ADC, DAC | none measured | spiking | ~100 ns spikes | fan-in logic (AND/XOR) only | next | R7-053 |
| PNN with on-chip backpropagation (Ashtiani 2026) | digital training loop; all linear and nonlinear ops on chip | not accessible (paywalled) | >90% on two tasks | — | multi-layer (count not accessible) | next | R7-054 |
| Photoelectric-multiplication theory; single-shot free-space ONN projection | per-cycle ADC (charge integration) | 50 zJ/MAC optical bound (PROJECTED); ~10 fJ/MAC system (PROJECTED) | — | GHz (claimed) | model | speculative | R7-007, R7-030 |
| All-optical χ(2) in TFLN (switch; ReLU) | all O-E-O | **80 / 20 fJ** switch; **16 fJ** ReLU, optical only, pump/bias excluded | analog ReLU | 18–75 fs | 0 on chip | speculative | R7-055…058 |
| Photonic-crystal carrier switch (InGaAsP) | all O-E-O | 0.42 / 0.66 fJ (optical) | binary | tens of ps | not shown | speculative | R7-059 |
| Phase-change spiking neuron | all O-E-O | 430 pJ threshold; 710 pJ / 200 ns pulses | spiking | 200 ns | 1 layer (4 neurons) | next | R7-060/061 |
| Ge-Si photodiode as all-optical activation + monitor | TIA/ADC for the activation; photocurrent doubles as monitor | 1.1 mW threshold (≈55 fJ at 20 GHz, DERIVED); 6.2 dB loss; 0.27 pJ/op calculated | — | 20 GHz detection | **3 layers** across 3 chips (fibre) | next | R7-062…066 |
| SOA gain as weight (InP) | — (adds E/O) | 42 mW/SOA; ≈4.2 pJ/op (STUDY-ASSUMED) | Iris 85.8% | 10 GS/s | 3 layers, software nonlinearity | current platform | R7-067…069 |
| Programmable-responsivity photodetectors (WSe2; dual-gate Si; ferroelectric PZT; Si PD + RRAM; MoS2) | per-pixel ADC, input DAC (light is the input), weight modulator | none per MAC. 25 levels, ≥24 h retention, 10⁶ cycles (ferroelectric); ~10 nW device estimate (MoS2) | 1–1.5 bit typical | 50 ns (WSe2); 3/12 ns rise/fall, TIA-limited (Si) | 1 layer, 3×3 arrays | next (sensor front end) | R7-070…079 |
| Solar cell wired straight to a digital memristor BNN | voltage regulator / DC-DC | 45 nJ per whole-chip inference (bench supply); works from 0.08 to 8 suns | binary | 10–66 MHz | 1 chip | next | R7-084…088 |
| Photovoltaic modulator (the light powers its own modulator) | modulator driver supply | 20 zJ/bit electrical + 40 fJ/bit optical at 1 Mbps | binary | 1 Mbps | — | current process (GF 45RFSOI) | R7-089…091 |

**ADC conversions per MAC.** All values DERIVED from the cited configurations:
- Conventional N = 128 crossbar (R3 baseline): 1/128 = 7.8×10⁻³.
- Multiport PD: 1/16.
- Netcast: 1/100.
- VCSEL: 1/784.
- Free-space OLED/SLM setup, where one detector integrates a ~5×10⁵-element dot product: ~1/5×10⁵ (R7-009).
- TFLN: 7.6×10⁻⁶.
- Receiverless O-E-O, intermediate layers: 0.

## (c) Best transformation-gate candidates, ranked by system energy per MAC

All numbers in this section are **DERIVED**. Baseline is R3-105/106: 128 × 128 crossbar, 10 GS/s, 5-bit detection, 8-bit weights, batch 64. The R3 per-MAC terms are:

| Term | fJ/MAC |
|---|---|
| Laser | 78 |
| DAC | 3.9–7.8 |
| ADC | 17–117 |
| TIA | 19 |
| Activation SRAM | 38 |
| Thermo-optic weight hold | 0–83 |
| HBM weight streaming, decode | 1,460 |
| HBM weight streaming, prefill | 46 |

Each candidate swaps in its own measured or estimated device term and removes the terms it makes unnecessary. Only the photonic-system budget is compared; the GPU comparison stays in R3 because weight precision differs.

| Rank | Candidate | Arithmetic (per MAC, N = 128) | Decode, accel + HBM | Prefill, accel + HBM | Basis | Tier |
|---|---|---|---|---|---|---|
| 1 | **Receiverless O-E-O activation between weight-resident layers** (photodiode drives the modulator; NOFU class) | remove ADC + TIA + SRAM + DAC = 78–182 fJ; add 30/128 = 0.23 fJ electrical (+0.59 fJ optical) | **1.54–1.62 pJ** (was 1.62–1.80) | **0.12–0.21 pJ** (was 0.20–0.39) | R7-037, R7-039, R7-099, R7-100 | next |
| 1b | Same gate built from the NTT femtofarad O-E-O transistor | 21.5 fJ / 128 = 0.17 fJ, same removals | ≈ rank 1 | ≈ rank 1 | R7-045, R7-102 (binary, III-V) | next |
| 2 | **Time-integrating / charge-domain readout** (Netcast/TFLN/VCSEL receivers; MANTIS-style switched-capacitor MAC) | ADC ÷ (N·M): 2.19–15 pJ / (128 × 100) = 0.17–1.17 fJ; TIA → integrator | **1.58–1.67 pJ** | **0.16–0.26 pJ** | R7-096, R7-097, R7-098; measured chip anchor R7-080 | current (CMOS charge domain) / next (photonic) |
| 3 | All-optical χ(2) activation (TFLN) | 16–80 fJ / 128 = 0.13–0.63 fJ **optical**, pump wall-plug unknown | ≈ rank 1 (lower bound) | ≈ rank 1 (lower bound) | R7-055, R7-058, R7-101 | speculative |
| 4 | Single-photon detection as activation | optical 0.038 photons/MAC; detector electronics and cooling not reported | n/a | n/a | R7-010 | speculative |

How to read this:
- **Candidate 2 is the only one with a measured, charge-domain, photodiode-to-MAC chip.** MANTIS reaches 11.9 fJ/op at the accelerator and 0.22 pJ/op at SoC level, 1-bit-normalised (R7-080/081).
- **Candidates 1 and 3 rest on device-level energies inside networks of at most 3 layers and N = 6.**
- **Candidates 1 and 2 do not add.** Rank 1 already removes the ADC for intermediate layers; rank 2 then helps only the final readout.
- **Rank 1 assumes all layer weights sit on chip at once.** For LLMs this is impossible (R3-012; ferroelectric write endurance 10⁶ cycles, R7-076). For an LLM, rank 1 falls back to rank 2.
- **Rank 2 in its time-division form adds 2 DACs per MAC, 1–2 pJ (R7-017).** It must be built as a spatial crossbar plus integrator, or with fan-out/batch, to stay in this table.
- **Integration may also shrink the laser term (DERIVED, speculative).**
  - R3's laser term puts 78 × 0.4 / 100 = 0.31 fJ/MAC at the detector.
  - Netcast measured 0.04 fJ/MAC at M = 100 (R7-001), but at kHz rates.
  - If that 8× margin held at 10 GS/s, the laser term would drop from 78 to ~10 fJ/MAC. No source shows this at speed.
- **Against the measured anchor**, Lightmatter's full system runs at 2.47 pJ/MAC (R3-043). Even the best DERIVED prefill (0.12–0.21 pJ/MAC at 5-bit) has never been built as one system.

**Synthesis (inferred, not a source claim).** The closest physical "transformation gate" is a femtofarad node where three things happen together:
- Photocurrent charges the modulator's own capacitance (accumulate).
- The modulator's transfer curve shapes the result (activate).
- Fresh supply light regenerates the signal (cascade).

NTT's 2 fF O-E-O device, the FICONN NOFU and the MIT photovoltaic modulator (R7-045, R7-037, R7-089) each show part of this. None of them shows it as an analog, multi-bit, multi-layer neuron.

## (d) What fits the CORNERSTONE process

**Passive + TiN heaters (MPW #50, the planned OPF-MZI4 run):**
- The platform page lists etch depths, TiN heaters and implants for active batches only, and no photodetector (R7-093). The gdsfactory `cspdk` 1.4.5 si220 cell library has no photodetector or modulator cell (checked in the local `.venv`).
- So **no monolithic electrical transformation gate can be built on it**: no integrating receiver, no O-E-O neuron, no programmable-responsivity photodetector.
- **Feasible now (current tier):** route mesh outputs to the bonded-photodiode service (£750 for 1 PD per die, £1,500 for 2–5; R4-043), or to external fibre-coupled PDs, followed by an off-the-shelf switched integrator. Netcast used such an integrator IC with 10 pF (R7-005 notes). This measures detector-side accumulation (ADC reads per MAC, optical aJ/MAC) on our own 4×4 mesh. It is a test-bench experiment, not an on-chip gate.
- **Unverified:** the MPW #50 graphene integration beta service (R7-095) might provide waveguide photodetectors on a passive run. Device types and specs are in the MPW #50 design rules, which I did not read.
- **Not recommended:** heaters as the "modulator" of an O-E-O loop. They respond thermally in microseconds and cost ~2 pJ/MAC to hold weights (NEGATIVE-FINDINGS #13), so they cannot be a useful activation.

**Active (MPW #51; sign-up 9 Dec 2026, design due 13 Jan 2027; 36-week delivery; R4-021/025):**
- The run offers 4 implants and 1.8 mm carrier-depletion MZMs at >28 Gb/s (R7-094). This supplies the modulator half of an O-E-O neuron.
- The detector half is not listed. No Ge photodiode appears; doped-microring and sub-bandgap Si detection are not stated. Whether the pn-junction implants support microrings is inferred, not verified.
- A 1.8 mm MZM has far higher capacitance than the 2 fF or microring devices that make receiverless drive work. The demonstrations used microring or photonic-crystal modulators (R7-037, R7-043, R7-045).

**Where these gates have actually been fabricated:**

| Gate | Process |
|---|---|
| Multiport PD; Ashtiani PDNN | AMF |
| FICONN | Elenion |
| TeMPO modulator | AIM |
| Photovoltaic modulator | GF 45RFSOI |
| NTT O-E-O | InP photonic crystal |

(R7-027, R7-036, R7-042, R7-026, R7-091.) An on-chip transformation-gate test chip therefore needs a Ge-photodiode active MPW; the options are in R4. On CORNERSTONE it is at best a hybrid with bonded photodiodes.

## (e) Negative findings

1. **No measured wall-plug energy per MAC exists** for any detector-accumulation, charge-domain photonic or O-E-O photonic network. Measured values are optical energies (R7-001, R7-006, R7-008, R7-010) or single-device energies (R7-045…050, R7-055…059).
2. **"Full-system" figures are component budgets.**
   - VCSEL, 7 fJ/OP: literature values of ADC 1 pJ, TIA 1 pJ, integrator 1 fJ, DAC 0.5 pJ, memory 100 fJ (SRAM-class, no HBM) (R7-018, R7-020, R7-021).
   - Netcast, 10 fJ/MAC: client only; server-side weight modulation excluded (R7-004).
   - TFLN, 6.5 fJ/OP: projection for an unbuilt 64 × 64 WDM system (R7-015).
3. **Conversions are often moved, not removed.**
   - Time-division integrators trade 1/131,072 ADC reads for 2 DAC samples per MAC (R7-017).
   - Netcast puts weight modulation on the server.
   - The VCSEL network's weight lasers and DACs are not amortised at batch 1; this is ~0.5 pJ/OP, DERIVED with Low confidence (R7-025).
4. **In decode, removing conversions saves ≤10%**, because HBM weight streaming dominates (R7-097, R7-100; R3-105). The single-shot ONN authors say the same: data that does not fit on chip meets the "same memory wall" (R7-031).
5. **The O-E-O demonstrations stop short of a full gate.**
   - Ashtiani's PDNN, the only O-E-O network with measured classification, keeps 7 off-chip TIAs and reports no energy (R7-034). Its 570 ps appears to come from component bandwidths (R7-032).
   - FICONN's 30 fJ is an estimate from measured current and an assumed ~1 ns carrier lifetime (R7-037).
   - Tait's gain was measured at an artificially low pump, and its cascade is a single-neuron autapse (R7-044).
6. **All-optical activation energies exclude the source.** They need table-top femtosecond OPO pulses at 2.09 µm, the bias pulse is "not included since it is not dissipated and can be reused", and nothing was cascaded on chip (R7-055, R7-058). Phase-change neurons need 430–710 pJ (R7-060/061). The Ge-Si activation loses 6.2 dB, so it cannot cascade without gain (R7-063).
7. **"Zero-energy" in-sensor and self-powered claims exclude readout.**
   - The reservoir excludes current-to-voltage conversion and the readout network (R7-092).
   - The ferroelectric sensor's zero energy is "prospected", and it works only at 365 nm UV (R7-077).
8. **Photodetector-as-weight has hard limits.**
   - Typical weights are 1–1.5 bit, limited by fixed-pattern noise (R7-083).
   - WSe2 weights live in external memory, fed via cabling (R7-071).
   - The Si dual-gate device's speed is TIA-limited (R7-073).
   - Ferroelectric write endurance of 10⁶ cycles rules out re-tiling weights per token (R7-076).
9. **Sunlight-direct analog compute is contradicted by the one measured regulator-free chip.** Its authors chose digital because analog in-memory compute needs "a stable and precise power supply" (R7-088). Its 45 nJ per inference was measured on a bench supply, not the solar cell (R7-087).
10. **MANTIS's abstract swaps its accelerator and SoC efficiencies** relative to its own table (84.1 accelerator, 4.57 SoC; R7-080). After moving MACs into the charge domain, digital logic takes 78% of SoC power (R7-082), an Amdahl ceiling.
11. **An amplified O-E-O activation (100 mW, ≈10 pJ each; R7-051) or SOA weighting (42 mW, ≈4.2 pJ/op; R7-067/068) erases any photonic advantage.** In the SOA DNN, electrical/optical conversions also dominate the error (R7-069).
12. **Netcast's ≈8-bit precision is for scalar multiplications**, not at the 40 aJ/MAC operating point (R7-003). Its 0.1 aJ/MAC needs 0.8 K SNSPDs (R7-006).

## (f) Failed sources and open questions

**ACCESS-FAILED:** R7-103…112.
- Jang 2022 main text: abstract and supplement used.
- Lefebvre ISSCC 2021 in-sensor current-domain MAC: repository timeout, API 429.
- De Marinis PEMAN charge-integrating photonic-electronic neuron: 403 everywhere.
- Mourgias-Alexandris SOA neuron: page gated by JavaScript.
- Main texts behind paywalls: Nozaki 2019, Ashtiani 2022, Ashtiani 2026, the Kerr "complete photonic neuron" (Yan 2025) and Nozaki 2010.
- A search-snippet "3.74 pJ/op end-to-end" figure for an InP CNN, excluded as unsourced.

Open questions:
1. What is the wall-plug energy per MAC of any integrate-and-dump photonic MVM at ≥1 GS/s, including laser, DAC, ADC and memory? It does not exist yet.
2. What is the energy per conversion of slow ADCs (≥6 ENOB at MS/s rates) that sit after an integrator? This would tighten R7-096, which conservatively reuses the ≥10 GS/s figures.
3. Does integration cut the laser term at speed? The 8× margin in section (c) is shown only at kHz.
4. Can a receiverless photodiode→microring neuron deliver 5–8-bit linear activations, and what is its energy measured rather than estimated?
5. Hardware questions for CORNERSTONE:
   - Can the bonded-photodiode service put several waveguides onto one PD (multiport summing)?
   - What devices does the MPW #50 graphene beta offer?
   - Does the active run support doped microrings or any 1550 nm silicon detection?
6. Radiation (branch E): Ge photodiode dark current rises with displacement damage, which becomes offset drift on a charge integrator. The integrate-and-dump approach has no orbit data (see R3 radiation section).
7. Could weight-resident layers ever cover a transformer block (e.g. an MLP tile)? This decides whether rank 1 ever applies to LLMs.
