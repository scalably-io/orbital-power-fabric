# OPF-MZI4 — open build guide (for anyone who wants to fabricate and test it)

**We do not fabricate this chip ourselves** (decision 2026-09-27). Everything needed to build, test and extend it is here, under CERN-OHL-P-2.0 (hardware) and Apache-2.0 (code). Prices, dates and specifications below are vendor statements retrieved 2026-09-27 with claim IDs in `evidence/claims.csv` — **re-check every date and price before you commit money**; shuttle calendars move and vendors may cancel runs (R4-045).

**Status of the design:** layout v0.1 built and connectivity-checked (28 metal islands = 2 × 14 heaters, one pad each; mutation-tested). **Not tapeout-ready:** the foundry's design-rule check (DRC) has not been run because CORNERSTONE does not publish its rules or deck (they come with sign-up). Step 3 below is mandatory.

## 1. What you get
| File | What it is |
|---|---|
| `chip/gds/opf_mzi4_v0.1.gds` (+ `.png`) | Full 5.5 × 4.9 mm die layout, CORNERSTONE 220 nm SOI + TiN heaters |
| `chip/mesh_cells.py`, `chip/opf_mzi4.py` | Parametric generator — every primitive is an unmodified `cspdk` cell (MIT) |
| `chip/check_nets.py` | Connectivity check (shorts/opens on the metal layers) |
| `chip/render.py` | KLayout rendering of any window of the GDS |
| `opf/mesh.py` | Simulator: program any 4×4 unitary, fit measured splitter errors, heater power |
| `scripts/chip_predictions.py` | Predicted heater power, energy per MAC and calibration benefit (EXPERIMENTS E012) |
| `chip/DESIGN.md` | Floorplan, provenance, test plan |

## 2. Choose a fabrication route
| Route | Platform | Next published slot (as retrieved) | Price (excl. VAT/duties) | Design kit | Notes |
|---|---|---|---|---|---|
| **CORNERSTONE MPW #50** (this layout's target) | 220 nm SOI passive + TiN heaters | Sign-up 14 Oct 2026, GDS 11 Nov 2026 (R4-017); 14 weeks (R4-021) | £14,700 for 5.5 × 4.9 mm with heaters; £8,875 without (R4-018/019); +£25 shipping (R4-027); via Europractice €17,787 (R4-038) | Open (`cspdk`, MIT) | Photodiode pick-and-place £750/die (R4-043); heater/crosstalk test service, price unpublished (R4-042); graphene beta service £7,000, device types unpublished (R7-095) |
| SiEPIC openEBL | 220 nm SOI, passive only | 17 Oct 2026 (R4-082); results 4–6 weeks (R4-083) | Free for SiEPIC-course alumni (R4-080) | Open (SiEPIC EBeam, MIT) | No heaters → tests couplers and passive MZIs only; area 605 × 410 µm |
| Applied Nanotools NanoSOI | e-beam 220 nm SOI + heaters | 13 Oct 2026 (R4-069); 6–8 weeks with metal (R4-071) | Not public (R4-073) | Open (SiEPIC EBeam) | Needs porting to `ubcpdk` |
| imec Passives+ (Europractice) | 220 nm SOI + heaters | Reserve by 7 Oct, tape-out 16 Dec 2026 (R4-005) | €6,700 half block (R4-008) | Licence agreement (R4-016) — **design cannot be published as open hardware** | Academic/spinout scope (R4-015) |
| AIM Photonics Active | SOI + Ge photodiodes + 2 Cu levels (R4-054) | Design due 1 Dec 2026, ship 4 May 2027 (R4-051) | $42,900 non-member, 8 mm² (R4-048) | Licence | On-chip detectors — the route for H1' read-out experiments |

## 3. Adapt, check, submit
1. **Environment:** Python 3.12 venv, `pip install cspdk` (pins gdsfactory 9.45.0). Chip commands always run with that venv's Python.
2. **Regenerate:** `.venv/bin/python chip/opf_mzi4.py` → `chip/gds/opf_mzi4_v0.1.gds`. Die size, mode pitch (80 µm), heater length (320 µm, cspdk default), pad pitch (150 µm) and grating pitch (127 µm) are constants at the top of the two files.
3. **Design rules and DRC (mandatory, not done by us):** obtain the foundry's design manual and DRC deck at sign-up; run it (KLayout or the foundry's tool); fix every violation; re-run `chip/check_nets.py <gds> 14` after any change. Do not submit on our v0.1 without this.
4. **Porting:** other open PDKs (e.g. `ubcpdk` for SiEPIC/Applied Nanotools) need the heater, MMI and grating cells swapped in `mesh_cells.py`; keep the Clements arrangement and the "heaters of the m = 0 MZIs on the bottom arm" rule so metal crosses at most one waveguide.
5. **Submit** the GDS per the foundry's instructions; keep a hash of exactly what you sent.

## 4. Test setup (what a lab needs; prices not sourced — get quotes)
- Tunable C-band laser; two fibre arrays at 127 µm pitch (inputs west, outputs east) or single fibres; the loopback pairs are for alignment.
- 28 DC probes at ≥150 µm pitch (or wire-bond to a PCB); 14 independent heater current/voltage sources.
- Off-chip photodetectors on the four outputs (the passive run has no on-chip detector).

## 5. Measurements, in order (from chip/DESIGN.md)
| Step | Measure | Expected (source) | Feeds |
|---|---|---|---|
| 1 | Loopback insertion loss | 5.5–6.5 dB per grating (R4-037) | coupling budget |
| 2 | Calibration MZI heater sweep → P_π, extinction | < 20 mW/π vendor (R4-033); 24.77 mW/π measured elsewhere (R4-156); extinction up to ~66 dB reported (R4-163) | energy model P_π |
| 3 | Thermal crosstalk (drive one heater, watch neighbours) | ~1% nearest-neighbour reported in SOI meshes (R4-162) | calibration model |
| 4 | Mesh: program Haar-random unitaries, measure the 4×4 power transfer \|U\|² | power fidelity 0.9983–0.9999 before calibration for 1–5% splitter error; 1.0000 after fitting measured splits (E012/E028). Complex fidelity needs a phase-sensitive measurement. | `opf/mesh.power_fidelity`, `opf/mesh.program(..., splits=…, chip_layout=True)` |
| 5 | Total hold power for random matrices → energy per MAC | 0.33 W mean at 20 mW/π → ≈2 pJ/MAC at 10 GS/s (E012) | photonic energy model (D14) |

**What this chip does and does not test.** It realises unitary matrices only (a Clements mesh); general weight matrices need two meshes plus attenuators (SVD). It measures loss, P_π, crosstalk, unitary programming and heater hold power — it does not test H1'.

## 6. Where a well-resourced team should take it next (the H1' programme)
The measurement that decides whether resident-weight photonic inference is a breakthrough is **support overhead: full-system wall-plug energy ÷ optical-core energy** — today 318× in the only measured full-stack processor (R3-045); Our own analysis is negative: H1' (square layers, direct photon→charge read-out) could absorb 10–21× only under idealised assumptions; with measured parts and precision over real outputs it leaves ≤ 2.65× at NVFP4 pairing and fails at FP8 (EXPERIMENTS E032, docs/SYNTHESIS.md A7). A team that beats those numbers with a measurement changes the conclusion. The architecture is already in the patent literature (MIT US11546077B2, SYNTHESIS A5) — the open contribution is the measurement. Next builds, in order: on-chip detectors (AIM Active or the CORNERSTONE graphene service), direct photon→charge read-out on a ~1 fF node (DERIVATIONS D12), detector-driven modulators between layers (R7-037/045/046), non-volatile weights (R8: density ≤ 3,183/mm², so small models only; measured retention 1–24 h, R11). Open problems with numeric targets: `docs/generated/open_problems.md` (P7–P11).
