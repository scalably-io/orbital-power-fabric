# R3 — Photonic compute energy accounting (evidence ledger companion)

Retrieved 2026-09-27. Ledger: `R3-photonic-energy.csv` (108 claims, every quote checked verbatim against the downloaded source; sources in `evidence/sources/R3/`).
Classes: MEASURED · VENDOR-STATED · STUDY-ASSUMED (a paper's estimate built from assumed or literature component values) · DERIVED (my arithmetic; formula in notes) · PROJECTED · ACCESS-FAILED.

## (a) Verdict

1. **No published photonic system beats a B300 on total joules per useful transformer operation today.** The only measured full-stack photonic AI processor (Lightmatter, Nature 2025) runs at **0.81 TOPS/W ≈ 2.5 pJ/MAC system-level**. Its optical core alone reaches 262 TOPS/W, so the core is **~318× more efficient than the system around it** (R3-043, R3-044, R3-045).
2. **The handoff's fJ headline numbers are estimates, not measurements.**
   - 370 fJ/OP is a component model (R3-002).
   - 56.8 fJ/MAC is heater power alone, divided by a hypothetical 88-wavelength throughput, for an optical-fibre MIMO device that is not an AI accelerator (R3-005).
   - "65 TOPS" is per-channel throughput × 124 channels, and its energy is an estimated 1.5 pJ/OP, 94% of it laser (R3-016, R3-017).
3. **LLM decode is memory-bound.** Streaming weights from HBM is ~99% of weight-plus-MAC energy at batch 1 and ~74% at batch 64 (R3-088). Photonics only shrinks the MAC term. A complete photonic decode system costs **~2.8–3.1 pJ/MAC best case** (bottom-up) and **~9.3 pJ/MAC** from the measured anchor, against ~6.8 for a GPU-class FP16 system (R3-103, R3-104, R3-105).
4. **Prefill is the only regime where photonics can win.** The best case is 0.20–0.39 pJ/MAC at the accelerator vs 0.56 for B300 FP8 at peak (1.4–2.8×), and only at 5-bit detection. At 8-bit, the laser term alone is 0.6–5 pJ/MAC (R3-106, R3-107).
5. **Branch E heat is kilowatts, not watts.** Decode needs ~2.8–9.3 kW of heat rejection per PMAC/s; the handoff assumed 1.9–57 W (R3-108).
6. **C018 "zero holding power" is a discussion sentence, not a measurement.** PCM rewrites cost ~67 µJ each and endure 1.4×10⁸ cycles, and capacitive analog weights leak within 0.8 ms (R3-010 to R3-014).
7. **Radiation: passive SiN and silica are essentially tolerant.** Biased Si modulators degrade at 200–500 krad, roughly 100× the 1-year LEO dose. Ge photodetectors and III-V lasers carry the hardness burden. No thin-film lithium niobate (TFLN) or photonic-PCM space-radiation data exist in open literature (R3-091 to R3-101).

## (b) Comparison table

| System (source) | Workload run | Precision | Throughput | Reported energy | What it includes | Measured / projected | claim_ids |
|---|---|---|---|---|---|---|---|
| Lightmatter 4×128² PTC + 2 digital dies (Nature 2025) | ResNet, BERT-tiny (hardware), Atari RL; BERT-Large only in emulation | ABFP16 (7-bit DAC in, 11-bit ADC out) | 65.5 TOPS avg (262 peak) | 0.81 TOPS/W system (2.5 pJ/MAC); 262 TOPS/W core only | System: ADC/DAC, digital, lasers (78 W elec + 1.6 W opt); host/DRAM outside. Core: vector+weight encoding only (0.25 W) | MEASURED | R3-042 to R3-047 |
| Lightelligence PACE 64×64 (Nature 2025) | Ising / max-cut (not a NN) | 1-bit vectors, 8-bit weights, 7.61 ENOB | 8.19 TOPS | 2.38 TOPS/W incl. lasers (420 fJ/op); 4.21 excl. | 3.44 W: electronics 1.9 W + 4 lasers; TEC & weight loading (3 ms/refresh) excluded | MEASURED | R3-048 to R3-050 |
| Tsinghua ACCEL (Nature 2023) | 3-class ImageNet, MNIST (vision) | analog | 4.55×10³ TOPS (convention) | 4.4 nJ/frame; 74.8 POPS/W | Laser (light energy), SRAM, control, analog electronics; diffractive ops counted as MACs | MEASURED energy; op count is a convention | R3-051 to R3-053 |
| Tsinghua Taichi (Science 2024) | 1623-class Omniglot, AIGC | n/a | n/a | 160 TOPS/W headline | Unverifiable (full text 403) | ACCESS-FAILED | R3-054 |
| FAST-ONN VCSEL+SLM (src 29, LSA 2026) | one 2×2-kernel conv layer inside ResNet-18 COCO classifier | 5–6 bit | 45 GOPS | 369 fJ/OP (current); 2 fJ/OP projected | VCSEL bias, DAC, SLM (prorated 3 µW/pixel), TIA, ADC, NL; no memory/host | STUDY-ASSUMED / PROJECTED | R3-001 to R3-004 |
| Programmable unitary processor (src 28, Nat Photon 2026) | 3-mode fibre MIMO descrambling (not AI) | n/a | 1.1×10¹⁴ MAC/s assumed | 56.8 / 9.6 / 1.9–3.0 fJ/MAC | Thermo-optic heater static power only | PROJECTED | R3-005 to R3-009 |
| 65-TOPS 4-core OPU (src 30, Nat Commun 2026) | edge-detect convs; MNIST OE-CNN 95.08% | 4.68 bit | 65.04 TOPS (derived) | 1.50 pJ/OP (1.90 with real ADC/DAC) | Laser 94%, modulators, ADC, DAC, heaters; DRAM/I/O excluded | STUDY-ASSUMED | R3-016 to R3-020 |
| Single-shot MMM diffraction (src 27, Nat Commun 2026) | CNN+FC MNIST 96.4% vs 97.5% digital | 8.5 bit @100 MSa/s | 16.3 TOPS (formula) | 250 fJ/MAC; 5 fJ/MAC projected; 20 aJ/MAC optical | Nominal ~1 pJ modulators/DAC/ADC; NO laser term | STUDY-ASSUMED / PROJECTED | R3-021 to R3-025 |
| SLiM single-layer chip (src 26, Nat Commun 2025) | GPT-like LLMs up to 0.345B / 384 layers; 100-layer ImageNet CNN | 1-bit converters | 327.68 TOPS (calc, 128×128) | 856.85 TOPS/W (1.17 fJ/OP) | Literature per-channel powers; memory, host, bench instruments excluded | MEASURED accuracy; STUDY-ASSUMED energy | R3-026, R3-027 |
| Partial-coherence EAM core 9×3 (src 25, Nature 2024) | MNIST conv, 92.4% vs 95.0% | not stated | 0.108 TOPS | 1 TOPS/W | Light source 54%, ADC, DAC/drivers, receivers; PCM weights = 0 | STUDY-ASSUMED | R3-015, R3-028 |
| Incoherent LED/LCD multilayer (src 24, Nat Commun 2024) | MNIST 92.3% vs 95.4% | analog | 1.7 GOPS | 11.5 GOPS/W; 35 TOPS/W scaled | Hidden-layer circuits only; LCD, input ADC excluded | STUDY-ASSUMED / PROJECTED | R3-029, R3-030 |
| Spectral CNN on CMOS sensor (src 23, Nat Commun 2025) | first conv layer on natural light | analog | 8.7 GOPS system (2.2 TOPS theoretical) | none reported | n/a | MEASURED speed | R3-031, R3-032 |
| Graphene-Si PhC activator (src 33, LSA 2026) | activation function only | n/a | ps response | 4 fJ threshold (optical) | Optical pulse energy only | MEASURED / PROJECTED | R3-033, R3-034 |
| DEOAM analog memory (src 31, Nat Commun 2026) | MNIST by emulation | 4–8 bit control | n/a | retention 0.835 ms | memory element only | MEASURED | R3-014 |
| MIT FICONN (arXiv v1; Nat Photon 2024) | vowel classification 92.7% = digital | n/a | 0.53 TOPS | 9.8 pJ/OP on-chip (upper bound); ~10 fJ/OP projected | Thermal phase shifters dominate | STUDY-ASSUMED / PROJECTED | R3-055, R3-056 |
| PCM tensor core, Feldmann (arXiv v1; Nature 2021) | MNIST CNN 95.3% vs 96.1% | 5 bit | ~2 TMAC/s (calc) | 0.4 TOPS/W; 17 fJ/MAC optical-only | Optical power, ADCs, modulators (calc) | STUDY-ASSUMED / PROJECTED | R3-057, R3-058 |
| Optical Transformers (Cornell, arXiv 2023) | sampled real-Transformer ops on SLM system + calibrated simulation | ~5-bit in / 7-bit out | n/a | ~140× (530B) to ~8500× (4q-param) vs A100 | Full model: DRAM/SRAM, DAC, ADC, TIA, modulators, optics | PROJECTED | R3-059 to R3-064 |
| Photonic transformer chip KKA (PhotoniX 2025) | 2-head toy ViT, 10×10 attention | ~7.7-bit programming | >200 POPS projected | ~500 TOPS/W projected | Projection only; experiment used DC sources and power meters | PROJECTED | R3-065 |
| Photonic tensor processor rack unit (Nat Commun 2026) | MNIST 98.1%, CIFAR-10 72.0% | analog | 27 GMAC/s | 0.022 TOPS/W (45 pJ/OP) | Whole box, projected 2.5 W; DAC/ADC/TIA dominate | STUDY-ASSUMED | R3-066 |
| **NVIDIA B300 / GB300 (baseline)** | any | NVFP4 / FP8 | 15 / 5 PFLOPS dense per GPU | 1,400 W TGP → 187 / 560 fJ/MAC chip; 263 / 789 fJ/MAC NVL72 rack | Peak utilisation; HBM inside TGP | VENDOR-STATED → DERIVED | R3-067 to R3-073 |
| **GH200 measured coefficients (baseline)** | microbenchmarks | FP16 | n/a | 0.52 pJ/FLOP tensor; 11.68 pJ/bit HBM | Control + datapath, attributed | MEASURED | R3-078, R3-079 |

## (c) Handoff check

| Handoff item | Verdict | Correct statement | claim_id |
|---|---|---|---|
| ~370 fJ/op "full-system prototype" (src 29) | **CORRECTED** | 369 fJ/OP is a component-level estimate "with appropriate electronic circuitry" (literature DAC/ADC/TIA/NL values), = 738 fJ/MAC. It excludes memory and host, and prorates the 8 W SLM to 3 µW/pixel; charging the full SLM to the measured 45 GOPS gives 178 pJ/OP. | R3-002, R3-004 |
| ~2 fJ/op projected (src 29) | **CONFIRMED (PROJECTED)** | For 32×32 VCSELs × 32×32 fanout at 25 GS/s (Table S1 column: N=M=1000). ADC-dominated. | R3-003 |
| ~56.8 fJ/MAC prototype (src 28) | **CORRECTED** | Not a measured prototype figure: static heater power only (6.4 W, assumed π/2 mean phase), divided by a hypothetical 88-wavelength × 10 GBd × 8×8 throughput. The device is a fibre-MIMO unitary for long-haul SDM, not an AI accelerator. No lasers, modulators, detectors, converters or DSP included. | R3-005, R3-008 |
| ~9.6 fJ/MAC optimized (src 28) | **CONFIRMED (PROJECTED, heater-only)** | Three-stage MPLC with trench-isolated heaters, 1.1 W. | R3-006 |
| ~1.9–3 fJ/MAC projected (src 28) | **CONFIRMED (PROJECTED, heater-only)** | Si 1.9, SiN 3.0 fJ/MAC. | R3-007 |
| 65 TOPS (src 30) | **CORRECTED** | 65.04 TOPS is paper arithmetic, 524.52 GOPS × 31 λ × 4 cores (the paper calls it experimental). Energy is an estimated 1.50 pJ/OP (1.90 with realistic converters), 94% laser; precision 4.68 bit. | R3-016, R3-017, R3-018, R3-020 |
| C013 natural/incoherent light computes | **CONFIRMED (scoped)** | True for the first convolution layer only; everything after is electronic. No energy per op reported. System speed is readout-limited to 8.7 GOPS. | R3-031, R3-032 |
| C014 deep photonic systems evaluated transformer-like models | **CONFIRMED with caveats** | SLiM ran GPT-like LLMs up to 0.345B in 8×8 tiles on bench AWG/oscilloscope with 1-bit converters (loss 3.04 vs A100 2.955). Lightmatter ran BERT-tiny on hardware. No wall-plug energy was measured on an LLM. | R3-026, R3-046 |
| C015 ~56.8 fJ/MAC current, lower projected | **CORRECTED** | As in the source-28 rows above. | R3-005 |
| C016 ~370 fJ/op current, ~2 fJ/op projected | **CORRECTED** (current) / **CONFIRMED** (projected) | As in the source-29 rows above. | R3-002, R3-003 |
| C017 65 TOPS demonstrated | **CORRECTED** | Derived aggregate; energy estimated, not measured. | R3-016, R3-017 |
| C018 passive/self-holding ≈ zero standby power | **CONFIRMED as a discussion statement; not measured** | Holds only for phase-shifter holding power on a never-changing matrix. PCM rewrite ≈ 67 µJ per shifter (DERIVED from pulse data); endurance 1.4×10⁸ cycles; capacitive analog weights leak (τ 0.835 ms); radiation-induced index drift needs active tuning. | R3-010 to R3-014, R3-097 |
| Branch E heat illustration: 56.8 / 9.6 / 1.9 W per PMAC/s | **CORRECTED** | System-level: ~2.8–9.3 kW (decode), ~350–670 W (prefill, best case). | R3-108 |
| 766 W/m² ideal radiator at 350 K, ε=0.9 | arithmetic checks (DERIVED): 5.670e-8 × 350⁴ × 0.9 = 766 W/m², one-sided, no absorbed flux | outside R3 scope | — |

## (d) What a complete photonic transformer system needs per useful MAC today (DERIVED)

Useful operation = one MAC of a transformer layer. All inputs are ledger claims; all totals are **DERIVED** by me and are not paper claims.

**Route 1 — top-down from the only measured full-stack processor (Lightmatter), FP16-class, decode batch 64**

| Component | Energy per MAC | Arithmetic | Input |
|---|---|---|---|
| Photonic processor, full (lasers, PTC, ADC/DAC, digital pipeline, SRAM on die) | 2.47 pJ | 2 / 0.81 TOPS/W | R3-043 |
| Weight streaming from HBM, 16-bit, reused over batch 64 | 2.92 pJ | 16 × 11.68 pJ/bit / 64 | R3-078 |
| **Accelerator + memory** | **5.39 pJ** | | R3-103 |
| Host CPU & DRAM, idle capacity, PUE | ×1.72 | Google fleet measurement | R3-087 |
| **Total** | **9.27 pJ/MAC** | 5.39 × 1.72 | R3-103 |
| GPU-class reference, same case (GH200 FP16 MAC 1.04 pJ + 2.92) | 3.96 → 6.81 pJ/MAC | 2 × 0.52 + 2.92; ×1.72 | R3-104 |

On measured anchors, the photonic system uses ~36% **more** energy per useful decode MAC. In prefill with 2048-token reuse it is 2.56 vs 1.13 pJ/MAC.

**Route 2 — bottom-up from the best published components (optimistic; never built as one system).** Assumptions: 128×128 crossbar (Lightmatter-scale), 10 GS/s, 5-bit detection, 20 dB optical loss, 8-bit weights from HBM.

| Component | Energy per MAC (N=128) | Arithmetic | Input |
|---|---|---|---|
| Laser wall-plug (40% WPE) | 78 fJ | 10^(2+0.1·20)/N | R3-037 |
| Input DAC | 3.9–7.8 fJ | 0.5–1 pJ / N | R3-038 |
| Modulator drive | ≈0.04 fJ | 1 fJ/bit × 5 / N | R3-062 (notes) |
| Photodetection + TIA | 19 fJ | 2.4 pJ / N | R3-062 (notes) |
| Output ADC (best / median measured ≥10 GS/s, ≥6 ENOB) | 17–117 fJ | 2.19–15 pJ / N | R3-083, R3-084 |
| Weight holding (PCM/passive → thermo-optic) | 0–83 fJ | 0.83 mW / 10 GS/s | R3-010, R3-102 |
| Activation SRAM read + write | 38 fJ | 2 × 8 bit × 0.3 pJ/bit / N | R3-062 (notes) |
| Weight re-tiling via PCM | not viable: ~1 µJ per MAC at batch 64 | 67 µJ / 64 | R3-012 |
| Weight streaming from HBM, 8-bit, batch 64 | 1,460 fJ | 8 × 11.68 / 64 | R3-078 |
| Softmax, norm, nonlinearities (electronic) | small, not quantified (inferred from the Optical Transformers breakdown; not a ledger number) | — | — |
| KV-cache reads in attention (no weights-in-place possible) | ~93 pJ per attention MAC, 8-bit, no batch reuse | 8 × 11.68 | R3-061, R3-078 |
| **Accelerator + HBM, decode, linear layers** | **1.62–1.80 pJ** | sum | R3-105 |
| **With host, idle, PUE ×1.72** | **2.8–3.1 pJ/MAC** | | R3-105 |
| Same, prefill (each weight reused over 2048 tokens) | 0.20–0.39 pJ → 0.35–0.67 pJ/MAC | HBM term 0.046 pJ | R3-106 |
| 8-bit detection instead of 5-bit | laser term 5.0 pJ (N=128) / 0.64 pJ (N=1000) | ×64 per same formula (×8 if √SNR) | R3-107 |

Reading the table:
- The photonic core plus converters is 118–222 fJ/MAC at N=128 and 15–28 fJ/MAC at N=1000.
- HBM weight streaming is 80–90% of the decode total. It is identical for GPU and photonic hardware, so photonics cannot remove the decode memory wall.
- KV-cache attention traffic is excluded from the totals above because it depends on the model (context length, grouped-query attention). It adds the same cost to both technologies.
- **Best-sourced range today for a complete photonic transformer system: ~3–9 pJ per useful MAC in decode, ~0.35–4.4 pJ/MAC in prefill.** B300 at peak is 0.56 pJ/MAC FP8 (chip) and 0.79 pJ/MAC (NVL72 rack) (R3-070, R3-073).

## (e) Negative findings and contradictions

- **No measured wall-plug energy exists for any photonic system running a real LLM at scale.**
  - SLiM's LLM ran as 8×8 tiles on bench instruments (R3-026).
  - Lightmatter ran BERT-tiny on hardware at 39–458 inferences/s, far below its 65.5 TOPS peak (R3-046).
  - Optical Transformers is a calibrated simulation (R3-059).
  - The PhotoniX chip ran a 10×10 toy attention with DC voltage sources (R3-065).
- **Photonic papers mostly report core energy.** The Nature Photonics perspective says so explicitly (R3-039), and Lightmatter's own authors stress "accounting for total processor power" (R3-044).
- **Source 27's "total system energy" contains no laser term** (R3-022).
- **Source 23 reports no energy at all** (R3-031).
- **SLiM's 856.85 TOPS/W does not reproduce.** Recomputing from its listed per-channel powers gives ~799 TOPS/W; ~857 is reached only if the N×M phase-shifter term is dropped (R3-027).
- **SLiM is internally inconsistent** about array size: K=128 in the supplement vs 8×8 cores in Methods (R3-026).
- **ACCEL's 74.8 POPS/W counts diffractive propagation as MACs**, so it cannot be compared per op. Its A100 comparison is a batch-1 serial run (R3-052, R3-053).
- **NVIDIA's own pages disagree on per-GPU throughput.** The technical blog gives 15 PF dense NVFP4 and 5 PF dense FP8 per Blackwell Ultra; the HGX B300 page implies 13.5 and 4.5 PF. This is probably a different power point (R3-069, R3-071).
- **HBM3E energy per bit is inconsistent across sources.**
  - The same SK hynix IEDM 2023 paper is cited as 3.44 pJ/bit (RPU) and as 5.74 pJ/bit with IO (LLMET) (R3-081, R3-082).
  - Measured GPU-level HBM path energy is 11.68 pJ/bit, because it includes controller and on-chip network control energy (R3-078).
- **LEO dose context differs by >100×:** "<15 rad" for <1 year (Arnold et al., ISS-like context) vs 3–5 krad(Si)/yr at 500 km behind 4 mm Al (qualification review) (R3-092, R3-093).
- **The ISS on-orbit Si-photonics test (Mao 2024) flew unpowered devices**, so it does not test biased operation (R3-091, R3-095).
- **The analytical LLM-energy model uses K=6 FLOPs/parameter/token**, a training constant; inference is ~2. This biases its compute share upward (R3-090).
- **The perspective's compiled GB200 INT8 figure of 200 fJ/MAC is well below my derived B300 FP8 560 fJ/MAC** at TGP. Its derivation is not shown (R3-040, R3-070).
- **No open data exists on TFLN modulator radiation or on photonic-PCM weight drift under space radiation.** The only LiNbO3 radiation evidence is for bulk Ti-diffused/APE modulators (R3-099); the GST displacement threshold is ion-beam data (R3-101).

## (f) Failed sources and open questions

**ACCESS-FAILED or partial**
- Source 21 main text (paywalled; free supplement used).
- Source 22 (paywalled, no supplement) — R3-036.
- Source 32 (paywalled; its supplement has no energy per op) — R3-035.
- Source 34 main text (paywalled; supplement Table S1 used).
- Lightmatter main text (paywalled). Hardware accuracy numbers for ResNet and BERT were not read; the supplement was used.
- Taichi full text and supplement (science.org 403) — R3-054.
- MIT FICONN, Feldmann 2021 and Optical Transformers published versions (paywalled or not re-checked; arXiv versions used).
- MDPI Crystals 2024 LN-film gamma study (403).
- Zeiler et al. 2017 CERN CDS PDF (not retrievable).
- Applied Optics 2026 full text (captcha; abstract via Crossref).
- SK hynix IEDM 2023 HBM3E primary (paywalled; secondary citations only).
- Horowitz ISSCC 2014 primary (read via EIE Table I).
- PhotoniX PDF (scripted download blocked; read in a browser session).

**Open questions**
1. End-to-end tokens/s per watt of any photonic accelerator on a real transformer, including host, memory and utilisation. This number does not exist yet.
2. Lightmatter's hardware accuracy and utilisation on BERT (paywalled main text).
3. Whether any photonic architecture reduces HBM or KV-cache traffic, rather than only the MAC term. None found.
4. Laser power vs precision scaling (∝SNR vs ∝√SNR). It decides whether 8-bit photonic prefill beats B300 FP8 at all.
5. Radiation on biased photonic compute under LEO spectra: TFLN, photonic PCM weight retention, Ge photodetector dark current at realistic proton fluence.
6. A DAC energy survey comparable to Murmann's ADC survey. Published DAC figures span 0.5–17.7 pJ per sample (R3-038, R3-063, R3-085).
7. Reconcile B300 per-GPU dense FP8 (4.5 vs 5 PF) and the per-GPU power in HGX vs GB300 configurations.
