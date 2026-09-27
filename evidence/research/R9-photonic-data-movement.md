# R9 — Photonic data movement: how much AI energy is moving bits, and how much of it can light remove?

Retrieved 2026-09-27. Ledger: `R9-photonic-data-movement.csv` (82 rows: 76 claims + 6 ACCESS-FAILED). Every quote was checked verbatim against the downloaded text by `evidence/sources/R9/_build_csv.py`. The checker was mutation-tested: 3 altered quotes, 3 caught. All derived numbers come from `evidence/sources/R9/_derive.py`, which uses the repo's `opf.transformer`.
Classes: MEASURED · VENDOR-STATED · STUDY-ASSUMED · DERIVED (formula in notes) · PROJECTED. Scope excludes physics floors and devices (R8) and conversion-as-compute (R7).

## (a) Verdict

1. **Light's big movement win is long reach, not the HBM weight fetch:** co-packaged optics at ~4–6 pJ/bit replaces 13–21 pJ/bit pluggable/long-reach SerDes beyond ~1 m (R9-024, R9-031, R9-037).
2. **GH200's measured 11.68 pJ/bit HBM fetch** is 74% control logic (8.69) and 26% datapath (2.99); storing/sensing the bit is ~1% (0.11–0.18) and the interposer I/O optics could replace is 2–7% (0.25–0.8) (R9-001, R9-002, R9-011, R9-009).
3. **Commercial optics (2.3–5 pJ/bit) cost 3.5–20× the in-package wires they would replace:** +13–37% on fetch energy; a 209 Tb/s HBM4 interface = 0.48–0.96 kW optical vs 52–167 W electrical (R9-022). The academic frontier only ties electrical (0.12 measured, ~0.22–0.24 pJ/bit projected; R9-043).
4. **Qwen2.5-72B per-token fetch/MAC split:** decode B=1 98.9/1.1%; B=64 1k-ctx 61.7/38.3%; B=64 32k-ctx KV alone 69%; prefill 95.8% MAC (R9-070 to R9-073).
5. **Optical MACs remove** ≤1.1% (B=1), ≤38% (B=64), ≤96% (prefill); bottom-up optics 1 / 30–34 / 75–85%; the only measured full photonic processor (2.47 pJ/MAC) adds energy in every case (R9-074).
6. **Optical movement of weights/KV removes** 0–5% at best (academic frontier) and adds 8–37% with commercial parts (R9-075).
7. **Not moving weights is the real decode lever:** HBM-PIM ~2× system efficiency on GPT-J; NorthPole 23.7 mJ/token (3B LLM, no DRAM); analog PCM 0.16 pJ/MAC. Capacity is the limit: ~4,155 PCM chips for 72.7B weights (R9-060 to R9-065).
8. **No source measures or models an inference J/token saving from optically attached memory;** those papers report only throughput, TTFT or latency (R9-055, R9-057, R9-058).

## (b) HBM energy per bit, broken down

Per bit fetched. Sources: HBM2 device breakdown from NVIDIA's FGDRAM model (the only open, component-level split); GPU-level figures from the Antepara SC25 microbenchmarks (MEASURED).

| Component | Value | Status | claim_id | Can an optical link replace it? |
|---|---|---|---|---|
| Row activation + sensing (the storage-intrinsic part) | 1.21 pJ/bit (HBM2 average over GPU workloads) · 909 pJ per 1 KB activate → **0.111 pJ/bit** when a weight stream uses the whole row · 0.18 pJ/bit (HBM-CO model, streaming) | STUDY-ASSUMED; DERIVED | R9-007, R9-010, R9-011, R9-013 | **No.** Intrinsic to DRAM storage; ~1–1.5% of GH200's 11.68 |
| On-DRAM-die data movement: sense amp → global sense amps → TSV → base die, ~9.9 mm | 2.24 pJ/bit (HBM2 average) · 1.48 toggle-independent + 2.31 column at 50% toggle · model: 0.2 pJ/bit/mm + 0.148 pJ/bit/layer TSV | STUDY-ASSUMED | R9-008, R9-012, R9-013 | **Not by an off-package link.** Would need photonics inside the DRAM die (speculative tier) |
| I/O across the interposer (DRAM I/O + host PHY) | 0.3 (HBM2, real toggle rates) to 0.80 (50% activity) · 0.25 (HBM-CO / UCIe-class) · 0.36 (TSMC aLSI, HBM4 test vehicle) · 0.65 (XMAS next-gen HBM I/O) | STUDY-ASSUMED; MEASURED | R9-009, R9-010, R9-013, R9-051, R9-050 | **Yes.** The only directly replaceable segment: 2–7% of 11.68 |
| HBM device total | 3.92 (HBM2, incl. ECC; split 31% activation / 57% on-die movement / 8% I/O) · 3.44 HBM3E · 5.74 HBM3E "IO included" | STUDY-ASSUMED; conflicting secondary citations of one IEDM 2023 paper | R9-007, R9-015, R3-082 | Mostly no |
| GPU side: memory controller, L2→controller NoC, address/tag control | 8.24 (= 11.68 − 3.44) or 5.94 (= 11.68 − 5.74) | DERIVED (Low) | R9-016 | **No.** Logic and control plane, not wires |
| **GPU-level measured totals** | **GH200 (HBM3e): 11.68 = 8.69 control + 2.99 datapath** · MI300A (HBM3): 14.72 = 13.47 + 1.25 · A100 (HBM2e): 13.11 | MEASURED | R9-001, R9-002, R9-006 | The 2.99 datapath is the physical ceiling for any link technology |
| Full streaming path to the SM (HBM + L2 + L1) | 18.00 pJ/bit (the Table 3 HBM column is the HBM increment only; Eq. 9) | DERIVED | R9-005 | R3 and E014 use 11.68, which may understate a GPU weight fetch by ~35% |
| HBM4 | +40% power efficiency (SK hynix) · VDDQ 1.1 → 0.75 V (Samsung, ISSCC 2026) · no pJ/bit published · GPU-level projection 10.3–10.7 pJ/bit if only the device improves | VENDOR-STATED; DERIVED | R9-017, R9-018, R9-020 | Device gains barely move the GPU-level number |

**Reading.** At GPU level, fetching one bit of weights costs:
- ~1% to store and sense it;
- ~19–20% (2.24 of 11.68 per the HBM2 split) to move it inside the DRAM stack;
- 2–7% to cross the interposer;
- the remainder, mostly control logic, on the GPU.

"Memory energy" is therefore overwhelmingly wires and control, not storage. But the wires are short (millimetres), and the control is logic. Neither is where optics is competitive (R9-054).

## (c) Optical vs electrical links

| Link | pJ/bit | Included | Bandwidth · density | Latency | Status | claim_id |
|---|---|---|---|---|---|---|
| **OPTICAL** | | | | | | |
| Columbia 3D EIC/PIC link (Nat. Photon. 2025) | **0.120** measured; 0.221–0.238 projected total | TX+RX electronics measured; laser 30–47 fJ + tuning 71 fJ projected | 80 × 10 Gb/s; **5.3 Tb/s/mm²** | n/a | MEASURED + PROJECTED | R9-043 |
| Sun et al. 2015, processor↔memory over light | 1.3 circuits; **15.6 wall-plug** | laser at 11.6% wall-plug efficiency | 2.5 Gb/s; ~300 Gb/s/mm² | n/a | MEASURED | R9-041, R9-042 |
| OCM, disaggregated DDR4 (model) | 1.07 (added on top of DDR4's 39) | link only | 615 Gb/s per link | n/a | STUDY-ASSUMED | R9-044 |
| Lightmatter Passage | 2.3 PIC+laser · 4.3 incl. SerDes · **4.6 wall-plug (demo)** | 1.1 laser off-package | M1000: 114 Tbps over 4,000 mm² = 28.5 Gb/s/mm² (derived); design point 160 Gb/s/mm²; 4 fibres/mm | n/a | VENDOR-STATED / STUDY-ASSUMED | R9-023 to R9-027 |
| Celestial AI → Marvell Photonic Fabric | ~2.4 | not stated | 4.4 Tbps per chiplet | ~300 ns server→memory; 283 / 224 ns read/write round trip (emulated) | VENDOR-STATED / STUDY-ASSUMED | R9-038, R9-039 |
| Ayar Labs TeraPHY | <5 (2021: 1.024 Tbps; 2023: 2.048 Tbps/dir at 10 W → 2.4–4.9 derived) | laser inclusion unstated | 8 Tbps bidirectional (current); energy under NDA | 10 ns per chiplet; <25 ns end-to-end | VENDOR-STATED | R9-033 to R9-036 |
| Intel OCI (OFC 2024) | 5 (vs ~15 pluggable) | on-chip lasers | 4 Tbps bidirectional, 100 m | n/a | VENDOR-STATED | R9-037 |
| NVIDIA Quantum-X / Spectrum-X Photonics CPO | 9 W vs 30 W per 1.6 T port → **5.6 vs 18.75** (derived) | per port; laser unstated | switches up to 409.6 Tb/s | "no DSP retimers" (no number) | VENDOR-STATED → DERIVED | R9-031, R9-032 |
| Broadcom Bailly (TH5 CPO, Hot Chips 2024) | 4.7 optical engine + 2.3 laser = 7.0 | host SerDes excluded | 51.2 Tb/s | n/a | VENDOR-STATED (secondary) | R9-028 |
| Broadcom TH6-Davisson | "70% reduction", ">3.5× lower" than pluggables; ~5 (second-hand) | optical interconnect | 102.4 Tb/s | n/a | VENDOR-STATED | R9-029, R9-030 |
| Generic 2.5D CPO · LPO · pluggable (incl. host SerDes) | 12 · 13 · 21 (pluggable 15–20 per Marvell) | optics + PHY + laser | CPO ~1 Tb/s/mm shoreline, 34 Gb/s/mm²; LPO 1.3 Gb/s/mm² | DSP 100–150 ns | STUDY-ASSUMED | R9-024, R9-027, R9-030 |
| Marvell coherent-lite 800G (ISSCC 2026) | 3.72 excl. silicon photonics | DSP transceiver | 40 km | <300 ns | MEASURED (secondary) | R9-040 |
| **ELECTRICAL** | | | | | | |
| TSMC Active LSI D2D (12×HBM4 test vehicle) | **0.36** | incl. 0.07 active bridge | n/a | n/a | MEASURED (secondary) | R9-051 |
| Microsoft D2D | 0.25–0.33 system (0.17–0.23 analog) | | 20–24 Gb/s/lane | n/a | MEASURED (secondary) | R9-051 notes |
| UCIe-A / UCIe-S targets | 0.3 / 0.5 (0.75–1.2 via PCB) | PHY | **5.2 / 0.9 Tb/s/mm** at 16 Gb/s/pin | 2 ns TX+RX | VENDOR-STATED | R9-049, R9-052 |
| XMAS next-gen HBM I/O (28 nm) | 0.65 | transceiver | **3.6 TB/s/mm = 28.8 Tb/s/mm** | n/a | MEASURED | R9-050 |
| HBM-CO I/O model | 0.25 | | 102.5 GB/s/mm | n/a | STUDY-ASSUMED | R9-052 |
| NVLink ground-referenced signalling (<10 mm) | 1.17 | | 32 GB/s/mm | n/a | STUDY-ASSUMED | R9-052 |
| NVLink-C2C (Grace Hopper) | 1.3 | | 900 GB/s | n/a | VENDOR-STATED | R9-045 |
| PCIe Gen 5 | >6.5 | implied by NVIDIA's ">5×" | n/a | n/a | DERIVED | R9-046 |
| 224 Gb/s SerDes (ISSCC 2022/2024) | 1.41 (RX only) · 3 (TX+RX, DSP excluded) | | n/a | n/a | MEASURED | R9-048 |
| Long-reach SerDes with DSP | 4.5–6 ("at parity" with 5 pJ/bit optics) | | 14.4 Tb/s × 5 pJ = 72 W per GPU | n/a | STUDY-ASSUMED | R9-047 |

**Reading.**
- **Inside the package,** electrical links are 3.5–20× cheaper per bit (0.25–0.65 vs 2.3–5 pJ/bit) and 5–29× denser per mm of shoreline (5.2–28.8 vs ~1 Tb/s/mm).
- **Break-even distance** (R9-054). A fixed optical cost of 2.3–4.6 pJ/bit equals on-die wire energy (0.1–0.2 pJ/bit/mm) only at 11.5–46 mm, longer than the ~10 mm HBM path. The academic 0.22 pJ/bit would break even at 1–2 mm (speculative tier).
- **Where optics wins today:** beyond about a metre, where electrical needs 4.5–6 pJ/bit SerDes plus retimers, or 13–21 pJ/bit pluggables.
- **Latency:** optical adds ~10 ns per conversion chiplet (Ayar). Its latency case is against switched CXL (70–500 ns per hop), not against HBM.

## (d) DERIVED: decode and prefill split — optics for movement vs optics for MACs

**Model.** Qwen2.5-72B-Instruct, 72,706,203,648 parameters, 80 layers, 8 KV heads (E005, `opf/transformer.py`). FP8 weights and KV.

**Energy per token:**

E = W·8·e_bit / B + KV·8·e_bit + MACs·e_MAC

- W = parameter bytes (72.706e9);
- KV = bytes of K and V cache read per token (0.1678 GB at 1k context, 5.3687 GB at 32k);
- B = weight reuse (batch in decode, prompt length in prefill);
- e_bit = 11.68 pJ/bit (R3-078);
- e_MAC = 2 × 0.52 = 1.04 pJ (R3-079; FP16 measured);
- MACs = 72.80 G at 1k context, 114.41 G at 32k (E005).

**Conventions.** This follows the E014 convention: 8-bit fetch with an FP16-measured MAC. The mismatch inflates the MAC share, which favours optics-for-MACs, so the movement conclusion is conservative.

**Excluded:**
- static and idle power;
- the 1.72 production overhead (scales all terms, so shares do not change);
- activations, nonlinearities, and L2/L1 (the 18.0 pJ/bit sensitivity covers the caches).

**Per-token energy (R9-070 to R9-073):**

| Case | Weights | KV cache | MACs | Total | Weight / KV / MAC share |
|---|---|---|---|---|---|
| Decode B=1, 1k | 72.706e9 × 8 × 11.68 pJ = **6.794 J** | 0.1678e9 × 8 × 11.68 pJ = 0.0157 J | 72.80e9 × 1.04 pJ = 0.0757 J | **6.885 J** | 98.7 / 0.2 / **1.1%** |
| Decode B=1, 32k | 6.794 J | 0.5017 J | 0.1190 J | 7.414 J | 91.6 / 6.8 / 1.6% |
| Decode B=64, 1k | 6.794 / 64 = 0.1062 J | 0.0157 J | 0.0757 J | **0.1975 J** | 53.7 / 7.9 / **38.3%** |
| Decode B=64, 32k | 0.1062 J | 0.5017 J | 0.1190 J | 0.7268 J | 14.6 / **69.0** / 16.4% |
| Prefill, 2,048-token prompt (mean attention context 1,024) | 6.794 / 2048 = 3.32 mJ | KV write 2 × 80 × 1024 × 8 × 11.68 pJ = 15.3 µJ | 75.7 mJ | **79.0 mJ** | 4.2 / 0.02 / **95.8%** |

Fetch-to-MAC ratio: 90× (decode B=1), 1.6× (B=64, 1k), 5.1× (B=64, 32k), 0.04× (prefill) (R9-076).

**Optics for MACs (R9-074).** Removable share = MAC share × (1 − e_photonic / 1.04):

| Case | Ceiling (MAC → 0) | Bottom-up photonic core + converters, 118–222 fJ/MAC (R3 §d; excludes digital support) | Measured full photonic processor, 2.47 pJ/MAC (R3-043) |
|---|---|---|---|
| Decode B=1, 1k | 1.1% | 0.9–1.0% | −1.5% (adds) |
| Decode B=64, 1k | 38.3% | 30.1–34.0% | −52.7% |
| Decode B=64, 32k | 16.4% | 12.9–14.5% | −22.5% |
| Prefill | 95.8% | 75.3–84.9% | −131.7% |

**Optics for movement (R9-075).** Removable share = fetch share × (e_I/O − e_optical) / 11.68. The electrical I/O it replaces, e_I/O, is 0.25–0.8 pJ/bit.

| Case (fetch share) | Gross ceiling (interface → 0) | All-datapath ceiling (2.99 → 0, speculative) | Net, commercial optics (+1.50 to +4.35 pJ/bit) | Net, academic best (0.221–0.238 pJ/bit) |
|---|---|---|---|---|
| Decode B=1, 1k (98.9%) | 2.1–6.8% | 25.3% | −12.7 to −36.8% (adds) | +0.1 to +4.9% |
| Decode B=64, 1k (61.7%) | 1.3–4.2% | 15.8% | −7.9 to −23.0% | +0.1 to +3.1% |
| Decode B=64, 32k (83.6%) | 1.8–5.7% | 21.4% | −10.7 to −31.1% | +0.1 to +4.2% |
| Prefill (4.2%) | 0.1–0.3% | 1.1% | −0.5 to −1.6% | ≤0.2% |

**Sensitivity: full streaming path, 18.0 pJ/bit (R9-005).** The MAC share becomes 0.7% (B=1), 28.7% (B=64, 1k), 11.3% (B=64, 32k) and 93.6% (prefill). Movement dominates decode even more.

**Where optics-for-movement does pay (R9-059).** Only when the bits would otherwise cross a long electrical or pluggable path. One example is disaggregated or offloaded weights at batch 1, where every weight crosses a link every token: 581.6 Gbit × 5 pJ = 2.9 J at CPO against 8.7–12.2 J at 15–21 pJ/bit pluggable. That saves 5.8–9.3 J per token on the link. It is still added on top of the far-side DRAM energy, and local HBM (6.8 J per token) remains cheaper than any remote path.

**Answer to the question.**
- **Decode:** most per-token energy is data movement, but the movement is millimetre-scale HBM traffic dominated by control logic. Neither moving it with light (net loss today; ≤5% at the academic frontier) nor computing with light (≤1% at batch 1, ≤38% at batch 64) removes much.
- **Prefill:** optics-for-MACs has the only large ceiling, but no photonic system has yet shown it at system level.
- **Long reach:** optics-for-movement pays at rack and cluster reach. That is interconnect and disaggregation energy, not the dominant per-token term of a single-GPU decode.

## (e) Compute-in-memory comparator: not moving weights at all

| System | Workload | Energy | What is avoided | Status | claim_id |
|---|---|---|---|---|---|
| IBM analog PCM chip, 34 tiles, 35 M devices (Nature 2023) | RNN-T speech (45 M weights over 5 chips); **not an LLM** | 12.4 TOPS/W chip-sustained → **0.161 pJ/MAC**; system 6.7 TOPS/W (with estimated digital) → 0.30 pJ/MAC; tile peak 0.10 pJ/MAC | Weight fetch, fully (weights stationary) | MEASURED; DERIVED | R9-060 |
| Same technology scaled to a 72.7B LLM | Qwen2.5-72B weights | ≈ 4,155 chips at 2 PCM devices per weight | Capacity is the barrier | DERIVED | R9-061 |
| IBM NorthPole, 12 nm, weights + KV in on-chip SRAM, 16 cards | 3B LLM, w4a4, mini-batch 28 | 28,356 tok/s at 672 W → **23.7 mJ/token ≈ 7.9 pJ/MAC** (card level); 72.7× vs H100's lowest-latency point but only 2.2× vs L4's best-energy point | DRAM entirely | MEASURED; DERIVED | R9-062 to R9-064 |
| Samsung HBM-PIM on AMD MI100 | GPT-J 6B | **~2× system energy efficiency** (1.79–2.24×); AMD says "85% less energy" vs conventional HBM | Most HBM→GPU transfer for GEMV | MEASURED (vendor); VENDOR-STATED | R9-065, R9-066 |
| T-REX, 16 nm (ISSCC 2025) | small factorised transformers | 0.41–3.95 µJ/token incl. external memory; external memory access = up to 81% of energy in prior accelerators | Weight reloads (compression + sharing) | MEASURED | R9-067 |
| EnCharge EN100, analog in-memory | edge AI; 128 GB LPDDR at 272 GB/s | 200+ TOPS in 8.25 W → ≤0.083 pJ/MAC (peak, precision unstated) | Only what fits in the arrays: a 72.7 GB model would stream at 267 ms/token | VENDOR-STATED; DERIVED | R9-068 |
| Gain-cell analog attention (Nat. Comput. Sci. 2025) | GPT-2-class attention | 6.1 nJ per token per head (simulated); 40,000–90,000× vs GPUs for attention alone | KV-cache movement | STUDY-ASSUMED | R9-069 |

**Photonic comparator (R3):**
- bottom-up core + converters: 118–222 fJ/MAC (excludes digital support);
- measured full processor: 2.47 pJ/MAC;
- neither removes weight or KV fetch.

**Reading.**
- **Analog electronic compute-in-memory already reaches ~0.1–0.3 pJ/MAC measured.** That matches the optimistic photonic core, and it removes weight movement.
- **Its blocker is capacity (thousands of chips per 70B model), the same one photonic meshes have.** Once weights stream from DRAM, both hit the same memory wall.
- **The measured decode wins come from near-memory electronics:** HBM-PIM (~2×) and NorthPole (no DRAM). Neither comes from optics.
- **Removing DRAM does not automatically beat a GPU at batch.** NorthPole's 23.7 mJ/token is higher than a GH200-coefficient estimate of 8.1 mJ/token at the same batch of 28 with 4-bit fetch. That estimate uses component coefficients only and excludes static power, so it is an optimistic lower bound for the GPU (R9-063).

## (f) Negative findings, failed sources, open questions

**Negative findings**
- **No inference energy-per-token saving from optically attached or disaggregated memory exists in open sources.**
  - Celestial/Marvell (CelestiSim): only throughput (3.66–7.04×), latency, and a *training* data-movement saving of 60–90% (R9-055).
  - Marvell photonic-CXL: TTFT 6.6× and latency only (R9-057).
  - Cornell optical HBM: 4.2× performance with a "slight overhead in … energy" (R9-058).
- **Vendor energy savings rest on inflated electrical baselines.** CelestiSim assumes 50 pJ/bit for internal NVLink and 65 pJ/bit for adapters. NVIDIA's own C2C is 1.3 pJ/bit and GRS is 1.17 (R9-056 vs R9-045, R9-052).
- **NVIDIA publishes no pJ/bit and no latency for its CPO switches.** Its efficiency ratio rose from 3.5× (March 2025) to 5× (January 2026) (R9-032).
- **No public figure for Ayar TeraPHY energy; the current generation's numbers are under NDA** (R9-035).
- **Broadcom's TH6 release gives only relative figures** (R9-029).
- **The optical link is added, not substituted.** OCM's 1.07 pJ/bit comes on top of DDR4's 39 pJ/bit (R9-044). Sun 2015's laser made wall-plug 12× the circuit energy (R9-042).
- **Contradictions kept in the ledger:**
  - HBM3E 3.44 vs 5.74 pJ/bit, both citing the same IEDM 2023 paper (R9-015, R3-082).
  - JEDEC HBM4 6.4 Gb/s (SemiAnalysis) vs "8Gbps" (SK hynix) (R9-017, R9-019).
  - Lightmatter 4.3 (paper) vs 4.6 pJ/bit (blog) (R9-024, R9-025).
  - The RPU paper's "74/14/12%" split, attributed to FGDRAM, does not appear in FGDRAM's text; FGDRAM's average split is 31/57/8 (R9-014).
- **Possible understatement in R3/E014.** Antepara's HBM column excludes L2/L1, so a GPU streaming fetch is 18.0 pJ/bit, not 11.68 (R9-005). This does not change the photonic comparison, but on the GPU side the batch-1 decode fetch term is 54% larger than R3/E014 assume (11.68 understates 18.0 by 35%).

**ACCESS-FAILED (6):**
- R9-077: NVIDIA ISSCC 2026 DWDM link energy (ResearchGate 403; IEEE paywall).
- R9-078: Broadcom bcm78900 page (404).
- R9-079: Ayar Hot Chips 2025 energy and density (slides are images; NDA).
- R9-080: Intel "0.5 pJ/bit HBM3 PHY" (IEEE empty response).
- R9-081: AttAcc (ACM 403).
- R9-082: SK hynix IEDM 2023 HBM3E primary (paywall).

**Other fetch failures, with a substitute used:**
- BusinessWire (Ayar 2023, Broadcom) curl exit 92 → Converge and Yahoo mirrors.
- Intel newsroom 403 → intc.com.
- Broadcom investor page timed out.

**Open questions**
1. **HBM3E and HBM4 component split** (activation / on-die / TSV / I/O) from a primary source. Only HBM2 (2017) is open.
2. **Split of Antepara's 8.69 pJ/bit control plane** into DRAM-side row/column control vs GPU memory controller vs NoC. That split decides what any memory-interface redesign can reach.
3. **A measured pJ/bit and latency for NVIDIA's CPO** and its ISSCC 2026 DWDM scale-up link, and for Ayar's third-generation TeraPHY, laser included.
4. **Any measured J/token for LLM inference with optically attached or pooled memory,** including the far-side DRAM energy.
5. **Whether photonics in the DRAM die** (replacing the 2.24 pJ/bit on-die path) is physically plausible at 0.1–0.2 pJ/bit. This belongs to R8 (devices and floors).
6. **Weight-stationary capacity:** how many bits per mm² a photonic or analog array can hold, compared with the ~4,155-chip PCM figure for a 72.7B model.
