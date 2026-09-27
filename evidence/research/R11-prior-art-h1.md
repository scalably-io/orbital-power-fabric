# R11: prior art for H1 (resident-weight analog photonic pipeline)

Retrieved 2026-09-27. Ledger: `R11-prior-art-h1.csv`, 69 rows: 65 evidence rows (21 MEASURED, 15 FILING, 24 STUDY-ASSUMED, 2 PROJECTED, 3 DERIVED) and 4 ACCESS-FAILED. Every quote was checked against the downloaded source text by `evidence/sources/R11/_build_csv.py` (NFKC, alphanumeric-only match): 0 misses. `scripts/validate_evidence.py` (report mode, no `--write`): 0 rejects.
Element key: **(a)** non-volatile in-place photonic weights · **(b)** photon→charge integration at the detector · **(c)** receiverless detector-driven modulator as inter-layer activation (no TIA/ADC/DAC) · **(d)** ≥2 cascaded layers with resident weights. `c*` = all-optical or amplified substitute for (c).

## (a) Novelty verdict — PARTIAL (thin)

1. **Not found:** all four elements in one analog, non-spiking engine whose activation is a receiverless detector-driven *modulator* (searches in (c)).
2. **Three triples exist in single documents:**
   - a+c+d: MIT US10268232B2, priority 2016 (R11-001…003).
   - a+b+d: MIT US11546077B2, priority 2021, and its paper, which proposes converter-free analog links between layers (R11-004…007, 014/015).
   - b+c+d: George et al. 2019, simulated (R11-016…019).
3. **a+b+c exists only in weaker forms:** US11546077's receiverless PD→modulator is linear and does summation (TIA/ADC kept between layers); UC US11144821B2 (2017) has all four in spiking form, with transistors driving an LED/laser (R11-009…011).
4. **Built hardware stops at pairs or triples:** PDONN (c+d, 4 layers, heater weights), FICONN (c+d), ACCEL (fixed-mask a + b).
5. **What is new is narrow:** build it and measure its wall-plug support overhead. That measurement is the contribution; the architecture is plausibly obvious (inferred, not a legal opinion).
6. **Flaw in H1's (b):** with static weights, read-out amortises over fan-in N only, not N·T (R11-053…056). **Weakest element: (a)** — see (e).

## (b) Works that combine H1 elements

| Work | Year | Elements | Built / measured? | Energy reported (and what it includes) | Difference from H1 | claim_ids |
|---|---|---|---|---|---|---|
| **MIT US11546077B2** (Bernstein, Sludds, Englund) | prio 2021-04-16, granted 2023-01-03 | a (claimed static zero-power NEMS/LC/memristive; PCM in description) · b (charge summed on wires; TIA reads accumulated charge) · receiverless PD→ring modulator · d (via TIA/ADC/electronic NL/VCSEL) | Patent; paper version built with SLM + camera | "tens of aJ/MAC", a patent statement; paper projects ~10 fJ/MAC system | PD→modulator is linear and used for summation. Conversions remain between layers. | R11-004…008, R7-030/031 |
| **Bernstein et al., single-shot ONN** | arXiv 2022 | a (proposed: PCM, fixed mask, MEMS) · b · analog NL between layers with no DAC/ADC (proposed) · d | Built with LCoS SLMs, camera and digital NL | ~10 fJ/MAC projected (R7-030) | Closest paper in words. Its NL is generic analog electronics, not a receiverless modulator. | R11-014/015 |
| **MIT US10268232B2** (Shen, Harris, Soljačić, Englund…) | prio 2016-06-02, granted 2019-04-23 | a (PCM phases, "no power to maintain") · c (photodetector drives the cavity: ReLU/sigmoid) · d (hidden layers) | Patent; the combination was not built | none | No time integration. PCM is only an option; the main embodiment uses thermal MZIs. | R11-001…003 |
| **UC US11144821B2** (Yoo) | prio 2017-08-30, granted 2021-10-12 | a (NEMS non-volatile MZI, described) · b (integrating capacitor) · c-variant (PD→2 transistors→LED/laser) · d (claimed layers + MZI meshes) | Patent. The neurons were prototyped (2021) and fabricated (2024) with thermal MZI meshes. | 1.18 pJ/spike, neuron only, measured (R11-029); 10 fJ/spike projected (R11-028) | Spiking; the emitter is a light source, not a modulator on supply light; has a transistor gain stage; non-volatility never built | R11-009…011, R11-027…030 |
| **George et al., Opt. Express 27, 5181** (GWU/Princeton) | 2019 | b (PD integrates weighted products on the EAM capacitance) · c (capacitive, receiverless) · d (2×100, clocked two-phase) | Simulation | Formula only (CV²f + laser) | Weights are generic MRR/MZI, not non-volatile. Two-phase clocking halves throughput. | R11-016…019 |
| **NIST SOEN** (Shainline et al.) | 2017–2023 | a-analogue (flux-storage weights, >400 states) · b (integration loop) · c-variant (emitter = LED/laser/modulator) · d (MLP designs) | Synapses built and measured | 33 aJ per synapse event excluding cooling; 0.4 fJ programming including cooling | Needs 4 K; spiking; weight is electronic, not photonic transmission | R11-012, R11-024…026 |
| **PDONN** (Wu et al., HUST/CUHK, LSA) | 2025 | c (differential photocurrent directly drives an MRM; measured net gain > 0) · d (4 layers on one chip) | Built and measured (94–96 % accuracy) | 10.57 W "system", but a **calculated tally** (SI S4): laser 6.45 W, heaters 2.72 W, VOAs 0.96 W, circuits 0.41 W, NAFs 30 mW. Gives 121.7 pJ/OP. No host PC or TEC. | Thermal (volatile) weights; the authors propose PCM/MEMS. Only Kirchhoff summation. | R11-031…040, R11-057 |
| FICONN (MIT, Nat. Photon.) | 2024 | c (NOFU) · d (3 layers) | Built | 30 fJ/activation estimated; ≤9.8 pJ/OP on-chip | Thermal weights; no integration | R7-037…042, R3-055 |
| ACCEL (Tsinghua, Nature) | 2023 | a-degenerate (fixed etched SiO₂ masks) · b (photocurrent on precharged lines, no ADC) · d (2 diffractive layers + 1 electronic) | Built and measured | 4.4 nJ/frame: laser 3.4 (optical energy), SRAM 0.4, control 0.6, EAC 0.012 nJ. Input SLM and laser WPE excluded. | Masks are not rewritable. No optical re-emission, so no (c). | R11-041…043, R3-051…053 |
| Song et al. (MPI, Nat. Commun.) | 2024 | a proposed (PCM/photomask) · c-variant (op-amp + LED) · d (3 layers) | Built | 11.5 GOPS/W estimated (R3-029) | Amplifiers; LCD weights; no integration | R11-044/045 |
| Wang et al. (McMahon, Nat. Photon.) | 2023 | c-analogue (image intensifier) · d (2 layers) | Built | none | LCD weights; an intensifier is not integrable | R11-046 |
| Microsoft AOC (Nature) | 2025 | c-variant (analog electronics in the loop) · d (recurrent) | Built (256 weights) | 500 TOPS/W projected | Volatile SLM; amplifiers | R11-047/048 |
| NARCA (HUST, LSA) | 2026 | a (GST, >5 bit) | Built, 1 layer | ~0.76 TOPS/W, supplementary evaluation | Host + AWG between layers; the authors propose PD + electronic NL | R11-049…052 |
| Teo et al. (Nanophotonics) | 2022 | a · c* (GST, femtosecond pump) · d (3-layer model) | Material measured, network simulated | none | All-optical; needs a femtosecond pump | R11-020/021 |
| Feldmann et al. (Nature) | 2019 | a · c* (PCM neuron) | Built, 1 layer (4 neurons) | 430–710 pJ per neuron switch (R7-060/061) | All-optical; single layer | R11-023 |
| Chakraborty et al. | 2018 | a · c* · d (SNN simulation) | Simulation | — | All-photonic PCM neuron | R11-022 |
| Münster charge accumulation (Nanophotonics) | 2023 | b (98.9 % at 10 ns) | Bench | — | **Needs fast MZM weights** | R11-053/054 |
| HEANA | 2024 | b (BPCA) | Simulation | — | Weights streamed from a FIFO | R11-055 |
| SEPhIA (HPE Labs) | 2025 | b (LIF capacitor) · c-variant (CMOS→MRM) · d | Co-simulation | — | No non-volatile weights; spiking | R11-062 |
| Princeton KR20230072440A | prio 2021-11-17 | a (PCM among the options) · c-variant (PD/TFT→OLED) · d | Filing | — | English text may be a machine translation (Low confidence) | R11-013 |
| Netcast, TFLN, VCSEL, photoelectric multiplication | 2019–2024 | b | Built or simulated | see R7 | All stream weights | R7-001…025 |
| Lightmatter US10763974B2 | filed 2019, granted 2020 | b (RC low-pass sums K time-sequential outputs after the TIA; one slow-ADC read) | Patent | — | TIA kept; no non-volatile weights or detector-driven activation found in the OCR text | R11-068 |
| Lightelligence US11734556B2 | filed 2021, granted 2023 | electrical summation; DAC in, ADC out, digital nonlinearity | Patent (10 of 193 pages read) | — | Conventional conversion chain | R11-069 |
| Luminous US20200284984A1 (Nahmias) | 2020 | filter-bank photonic computing | Patent application | — | No non-volatile, integration or receiverless terms in the OCR text | — |

## (c) Search log (all on 2026-09-27)

"Relevant" means a hit that combines at least 2 H1 elements, or is a closest-candidate I then read.

| # | Query (abridged) | Database | Hits (relevant) |
|---|---|---|---|
| 1 | non-volatile phase-change PNN optoelectronic activation photodetector modulator multilayer | web search | 9 (0) |
| 2 | "non-volatile" photonic weights "time-integrating" detector NN | web search | 10 (0) |
| 3 | phase-change photonic tensor core "optoelectronic nonlinearity" cascaded | web search | 9 (1: Sorger PTC) |
| 4 | "photoelectric multiplication" optoelectronic activation receiverless | web search | 9 (2: Hamerly, MPI) |
| 5 | "receiverless" PNN photodetector drives modulator nonvolatile | web search | 9 (2: US11546077, FICONN; eLight 2026 MRR neuron read: TIA + single neuron, not relevant) |
| 6 | non-volatile + (nonlinear OR activation) + photonic NN | arXiv API | 3 (1: Teo) |
| 7 | "phase-change" + photonic + neural + photodetector | arXiv API | 0 |
| 8 | photonic neural + time-integrating/integrate-and-dump/charge integration | arXiv API | 3 (0 new) |
| 9 | (nonvolatile OR phase change) + photonic + neural | arXiv API | 41 (3: Teo, Chakraborty, MEMS memristor) |
| 10 | photonic neural + receiverless/optoelectronic activation | arXiv API | 3 (0) |
| 11 | same as 1 | Semantic Scholar API | FAILED (429) |
| 12 | same as 1 | OpenAlex API | 298 total, top 50 read (0) |
| 13 | Memory in integrated PNNs (review) | web search | 9 (1 review) |
| 14 | nonvolatile PNN O-E-O PCM weights multilayer experiment | web search | 9 (3: NARCA, chalcogenide, event-driven) |
| 15 | superconducting optoelectronic networks flux storage | web search + arXiv (au:Shainline) | 9 + 17 (1 family: SOEN) |
| 16 | photonic in-memory charge integration capacitor PCM | web search | 9 (1: SKYLIGHT, not read) |
| 17 | weight-stationary photonic, nonvolatile, no DAC/ADC between layers | web search | 10 (3: NARCA, MPI, HEANA) |
| 18 | "charge accumulation" photonic matrix processor | web search | 9 (1) |
| 19 | Yoo optoelectronic spiking neurons / attojoule nanophotonics | web search + arXiv (au:Yoo) | 9 + 9 + 6 (3: US11144821, 2105.02809, 2311.15474) |
| 20 | Microsoft AOC; ACCEL; McMahon intensifier; MPI incoherent | web search | 4×9 (4) |
| 21 | full H1 boolean (non-volatile/PCM + PD + modulator + activation + integrat* + layer) | Google Patents | 5,671, top 40 read (1: Princeton KR) |
| 22 | nonvolatile/PCM/ferroelectric/memristor + PD "drives (the/a) modulator" + weight | Google Patents | 229, top 40 read (0 new) |
| 23 | nonvolatile/PCM + PD + modulator + activation, CPC G06N3/067 | Google Patents | 167, top 60 read (3: US11144821, US11283002, KR20230072440) |
| 24 | assignee sweeps: Lightmatter, Lightelligence, Luminous, Celestial AI | Google Patents | FAILED (503 "automated queries") |
| 25 | site:patents.google.com Lightmatter / Lightelligence / Luminous / Salience / Akhetonics, Q.ANT, Arago, Optalysys, iPronics | web search | 5×9 (3: US10268232, US11546077, US20200284984) |
| 26 | patent "receiverless" photodetector modulator neural nonvolatile | web search | 9 (1: US11546077) |
| 27 | Lightmatter PCM patent; Celestial AI activation patent | web search | 18 (0) |
| 28 | photodetector integrates photocurrent on capacitor drives EAM, amplifier-free | web search | 9 (2: George 2019, FICONN) |
| 29 | PCM tensor core + time/charge integration | web search | 10 (0 new) |
| 30 | fully nonvolatile multilayer PNN experiment 2025–2026 | web search | 9 + 9 (0 multilayer built) |
| 31 | "photocurrent directly drives" MRM, PCM | web search | 9 (1: PDONN) |
| 32 | measured system power, per-inference energy, TOPS/W wall-plug 2025–26 | web search | 3×10 (3: PDONN, Xiang, PTP 2026) |
| 33 | Taichi energy accounting; Q.ANT, Lumai, Arago, Akhetonics energy | web search | 3×9 (Taichi: access failed; vendors relative only) |
| 34 | PEMAN; Takenaka ferroelectric; HPE memristor ONN; Tossoun | web search | 4×9 (1: SEPhIA; PEMAN failed) |
| 35 | CN113657580 (PCM + MRR CNN accelerator) | web search | 0 (not reachable) |
| 36 | USPTO image PDFs + OCR: US10268232, US11546077, US20200284984, US10763974 (all 122 pp.), US11734556 (front + last 10 of 193 pp.) | USPTO ppubs | 5 read (2 close; Lightmatter b-only; Lightelligence and Luminous not relevant) |

## (d) Measured wall-plug system energies (other than Lightmatter)

**None found that is a true wall-plug, per-inference measurement including host, TEC and calibration.**

What exists:
- **PDONN, 2025 (R11-035…040, R11-057).** The only multi-layer receiverless-O-E-O chip with a system figure: 10.57 W → 121.7 pJ/OP. It is a **calculation**, not a meter reading:
  - The laser term uses an assumed 3.1 % WPE and is 61 % of the total.
  - The per-inference latency of 4.1 ns is estimated.
  - DERIVED: 43.3 nJ/inference and ~243 pJ/MAC, i.e. 6×10⁴–8×10⁵ × the H1 core.
  - DERIVED (R11-040): at the chip's calculated ~105 MHz RC bandwidth, its receiverless activation costs ~2.9 pJ (0.3 mW operating point). That is TIA-class, not the 30 fJ FICONN estimate.
- **ACCEL, 2023 (R11-043).** Measured 4.4 nJ/frame. It counts laser *optical* energy, not electrical, and excludes the input SLM, so it is not wall-plug.
- **Lightelligence PACE (R3-048/049).** 2.38 TOPS/W including lasers; TEC and weight loading excluded. Already known.
- **Xiang et al., 2025 (R11-061).** 1.39 TOPS/W, computed from ~1.8 W chip power and an *estimated* throughput at a 5 GHz clock.
- **NARCA (R11-052).** ~0.76 TOPS/W, a supplementary evaluation.
- **Neuron-only figures.** UC Davis 1.18 pJ/spike measured (R11-029); NIST 33 aJ per synapse event excluding cooling (R11-026).
- **Not usable:**
  - Taichi's 160 TOPS/W accounting (supplement 403, R11-064).
  - Vendor claims (Q.ANT, Lumai): relative factors only, no absolute watts per inference found.

## (e) Weakest element: (a), rewritable non-volatile photonic weights inside a cascaded network

- **No multi-layer hardware uses rewritable non-volatile photonic weights.** Every built cascade uses something else:
  - heaters: PDONN, FICONN, UC Davis;
  - LCD or SLM: MPI, McMahon, AOC;
  - fixed masks: ACCEL.
  - Built PCM networks are single-layer (NARCA R11-049; Feldmann R11-023). The multi-layer PCM designs are simulations (Teo R11-020, Chakraborty R11-022).
- **Retention does not match "fixed, always-on" inference.** Measured non-volatile photonic cells hold for hours:
  - MEMS memristor >1 h (R11-058);
  - charge-trap 24 h verified (R11-059);
  - memresonator 12 h (R11-060).
  - PCM holds longer but has write noise (NARCA) and a ~67 µJ rewrite cost (R3).
- **Payoff is capped.** On the one chip where it was costed, removing hold power saves 26 %, because the laser dominates (R11-038).
- **(c) is now the second-weakest element, no longer the weakest.**
  - It has two built cascades (FICONN with 3 layers; PDONN with 4 layers and net gain > 0).
  - Its energy per activation has never been measured, only estimated (30 fJ to ~2.9 pJ).
- **(b) is well measured, but not in the form H1 needs.** Every demo that shares read-out over T time slots streams its weights: Münster "crucial" fast MZMs, HEANA FIFO, Netcast, TFLN (R11-054…056). H1 must restate (b) as spatial charge summation. That is what ACCEL and US11546077 already do.

## (f) Failed sources and open questions

**Failed**
- Google Patents XHR and page fetches: 503 after 3 queries, so the company assignee sweeps were not run (R11-066). Lightmatter US10763974B2 (all pages) and Lightelligence US11734556B2 (front page + last 10 of 193 pages only) were read via USPTO image PDF + tesseract OCR instead (R11-068/069). Other Lightmatter, Lightelligence and Celestial AI families were not read.
- Semantic Scholar API: 429 (R11-067).
- Taichi supplement: 403 (R11-064).
- PEMAN / De Marinis full text: 403 and reCAPTCHA (R11-065).
- CN113657580 and CN118297125A (Chinese PCM + photonic NN filings): not reachable.
- Salience Labs, Akhetonics, Q.ANT, Arago, Optalysys, iPronics: site-restricted search found no relevant patents. That is weak evidence of absence (search engine, not a patent database).
- Not read: Adv. Opt. Mater. 2026 "multimode nonvolatile PNN (phase-change metasurface)", paywalled; SKYLIGHT (2602.19031).

**Open questions**
1. Does any 2025–26 Chinese filing combine PCM weights with PD→MRM activation? PDONN's authors propose exactly that; check CNIPA directly.
2. What is the *measured* energy per activation of a depletion-mode (not injection) receiverless MRM at ≥1 GHz inside a cascade?
3. Non-volatile weight retention over months at operating temperature, with drift, for Sb₂Se₃ or GSST inside a network.
4. Is the MIT 2021 patent family (US 2022/0337333) still pending with broader claims? Check continuations before any filing.
5. A true wall-plug per-inference measurement (meter at the supply, host excluded but stated) of any multi-layer photonic chip. PDONN is the cheapest candidate to reproduce.
