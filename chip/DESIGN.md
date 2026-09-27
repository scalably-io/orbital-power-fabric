# OPF-MZI4 v0.1 — open 4×4 photonic matrix test chip

**Status 2026-09-27: layout v0.1 built and connectivity-checked. NOT tapeout-ready** — foundry DRC deck not yet obtained (see Open items). License: CERN-OHL-P-2.0 (`chip/LICENSE-CERN-OHL-P-2.0.txt`).

## What it is
A 4×4 Clements mesh of Mach-Zehnder interferometers (6 MZIs, 12 thermo-optic heaters) on CORNERSTONE 220 nm SOI passive + TiN heaters, MPW #50 small block (5.5 × 4.9 mm). It measures the terms our energy model cannot source well: heater power per π, thermal crosstalk, MZI/mesh loss, splitter imbalance — and therefore the heater-hold energy per MAC (E012: ≈2 pJ/MAC at 10 GS/s, flat in N).

## Provenance (built on existing open designs)
Every primitive is an **unmodified** cell from `gdsfactory/cspdk` 1.4.5 (MIT, © 2024 gdsfactory; R4-138): `mmi2x2`, `straight_heater_metal` (default 320 µm), `straight`, `bend_s`, `grating_coupler_rectangular`, `pad`, `text_rectangular`, `rectangle`. Only the arrangement is ours (`chip/mesh_cells.py`, `chip/opf_mzi4.py`). No license-clean fabricated 4×4 Clements layout existed to reuse (R4 dossier); the Clements arrangement itself is from Clements et al., Optica 2016.

## Floorplan
| Region | Content |
|---|---|
| West edge | 6 grating couplers at 127 µm pitch: 4 mesh inputs + 1 loopback pair (fibre-array alignment) |
| East edge | 6 grating couplers at 127 µm pitch: 4 mesh outputs + 1 loopback pair |
| Centre | Clements mesh, modes at 80 µm pitch, 3.62 mm long; no output phase screen (intensity detection cannot see output phase) |
| Lower band | Stand-alone calibration MZI with its own input/output couplers |
| North edge | 16 pads — heaters on top arms (contacts face north) |
| South edge | 12 pads — bottom-arm heaters of the m = 0 MZIs (8) + calibration MZI (4) |

Heaters of the lowest mode pair sit on the bottom arm so every heater reaches a pad crossing at most one waveguide; the simulator mirrors this (`opf/mesh.py`, `chip_layout=True`). Pads sit directly above/below their contacts (≥150 µm pitch), so routes are nearly straight.

## Verification done
- `chip/check_nets.py` (LVS-lite): 28 metal islands = 2 × 14 heaters, each with exactly one pad; every heater touches exactly two islands → **PASS**. Mutation-tested: an injected short (27 islands) and an injected open (islands without pads) both FAIL.
- `tests/test_chip.py` rebuilds the GDS and reruns the net check (venv: 31/31 pass).
- Visual review of the full-die render `chip/gds/opf_mzi4_v0.1.png`.
- GDS sha256 prefix `607f4bb977672e57` (v0.1, 2026-09-27).

## Test plan (what we measure → model term)
1. Loopback pairs → grating-coupler loss (vendor 5–6 dB/grating, R4/E011).
2. Calibration MZI heater sweep → P_π (vendor < 20 mW/π; 24.77 mW/π measured in a comparable process, R4-156) and extinction ratio.
3. Mesh: program Haar-random matrices, measure the 4×4 power transfer |U|² → POWER fidelity (`mesh.power_fidelity`; a power-only measurement cannot certify the complex fidelity, which needs a phase-sensitive measurement — E028); fit per-MZI splitter ratios. Prediction (E012/E028, σ = 1–5 % coupler error): power fidelity 0.9983–0.9999 programmed-as-ideal → 1.0000 after re-programming with the fitted splits.
   **Scope.** A Clements mesh realises unitary matrices only; a general weight matrix needs an SVD arrangement (two meshes + per-mode attenuators). This chip tests heaters, loss, crosstalk and unitary programming — it does NOT validate H1' (resident non-volatile weights, photon→charge read-out, receiverless layers).
4. Heater-to-heater thermal crosstalk (drive one, watch neighbours).
5. Total hold power for random matrices → heater-hold energy per MAC (model: 0.33 W mean → ≈2 pJ/MAC at 10 GS/s).

## Open items before any order
1. **Foundry DRC deck / design rules** — not in cspdk, not published on the CORNERSTONE pages (E011). Obtain at sign-up; run and fix; fresh-context review. Until then no tapeout-ready claim.
2. **Purchase decision (Pavle):** small die £14,700 with heaters, sign-up by 14 Oct 2026, GDS by 11 Nov 2026 (confirmed live, E010). Large die (4×4 + 8×8) £19,980.
3. UK VAT / customs treatment for a non-UK (Serbian) buyer — unverified.
4. Test setup: fibre array (127 µm) or two single fibres + a 28-needle DC probe or wire-bonding; heater drivers (multichannel DAC/current sources).

## Rebuild
`.venv/bin/python chip/opf_mzi4.py && .venv/bin/python chip/check_nets.py chip/gds/opf_mzi4_v0.1.gds 14`
