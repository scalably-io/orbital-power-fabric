#!/usr/bin/env python3
"""Open problems with quantified targets — the hand-over table for teams that can build the next step.

Every 'today' value is a claim_id; every 'target' is computed from opf/ (derivation or experiment ID).
Writes docs/generated/open_problems.md.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import importlib.util

from opf import scenarios as sc
from opf.breakeven import flip_value
from opf.lifecycle import launches, min_service_life

_spec = importlib.util.spec_from_file_location("efficiency_v2", ROOT / "scripts/efficiency_v2.py")
ev2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ev2)

L = 15.0
a_lo = sc.A["current"].kg_per_kw[0] * L / sc.A["current"].life


def floors(tier):
    t = sc.B[tier]
    cc = a_lo * t.post_pv / (1000 * sc.PUE * L / sc.SAT_LIFE_LEO)
    return 1 / cc, 0.90 * t.dc_rf / cc          # array floor W/kg, transmitter floor W/kg (other part weightless)


pv_m, tx_m = floors("current")
pv_n, tx_n = floors("next")
geo = [sc.A["current"].life * sc.b_geo_kg_per_kw(sc.B[t], gw * 1e9, 44.7) / sc.A["current"].kg_per_kw[0]
       for t in ("current", "next") for gw in (1, 10)]
fp = 26.5e6
mirror_km2 = 2.6 * fp / sc.MIRROR_OPTICAL / 1e6
c_ideal = sc.c_kg_per_kw(sc.C["current"], 208) * launches(L, sc.MIRROR_LIFE)
life_be = [min_service_life(L, sc.c_kg_per_kw(sc.C[t], 208) / sc.CLEAR_SKY, a_lo) for t in ("current", "next")]
h1 = [ev2.family_r(f, 1024, "pc")["support_for_10x"] for f in ("FP4", "FP8")] + [ev2.family_r(f, 256, "pc")["support_for_10x"] for f in ("FP4", "FP8")]
decode_bound = max(ev2.family_s(f, 64)["bound"] for f in ("FP4", "FP8"))
lad = {f: ev2.ladder(f) for f in ("FP4", "FP8")}
real_fp4 = lad["FP4"][4][2]
from opf import limits as _lim


def _support_at(loss_db: float) -> float:   # FP4 realistic end (all ladder corrections) at a given optical loss
    t = ev2
    per_mac = max(_lim.dist_photons_per_mac(5) * _lim.photon_energy_j(t.LAMBDA_REAL) / t.QE_REAL, 2 * t.OEO_PD_J / 1024)
    s = _lim.Stack(n=1024, detect_j=per_mac * 1024, loss_db=loss_db, wallplug=0.20, dac_j=t.DAC / t.LAYERS, mod_j=t.OEO,
                   tia_j=t.TIA / t.LAYERS, adc_j=t.adc(5) / t.LAYERS)
    return t.B300["FP4"] / (10 * s.per_mac()["total"])


assert abs(_support_at(20.0) - real_fp4) < 1e-9          # same model as the ladder's last 20 dB step
loss_be = flip_value(lambda x: _support_at(x) - 1.0, 20.0, 40.0)
_tb = sc.B["next"]
geo_tx = flip_value(lambda w: sc.b_geo_kg_per_kw(sc.TierB(_tb.pv_w_per_kg, w, _tb.post_pv, _tb.dc_rf, ""), 10e9, 44.7)
                    * launches(L, sc.GEO_LIFE) - a_lo * 3 / (L / sc.A["current"].life), 28.0, 1e5)
c_next_clear = sc.c_kg_per_kw(sc.C["next"], 208) * launches(L, sc.MIRROR_LIFE) / a_lo
r_sizes = [(n, n * n * ev2.LAYERS, n * n * ev2.LAYERS / ev2.DENSITY / 100) for n in (256, 1024)]
# per MWh of AI (IT) electricity: terrestrial $/delivered-MWh x PUE (E028)
launch_be = [mwh * sc.PUE * 8.76 * sc.A["current"].life / sc.A["current"].kg_per_kw[0] for mwh in sc.FIRM_SOLAR_USD_PER_MWH]
mirror_km2_hi = 5.0 * fp / sc.MIRROR_OPTICAL / 1e6

rows = [
    ("P1", "Space microwave transmitter specific power (W/kg RF out)", "28 (R2-043, JAXA GaN, measured)",
     f"LEO: ≥ {tx_n:.0f}–{tx_m:.0f} even with a weightless array; GEO next-tier 10 GW, 15-y life: ≥ {geo_tx:.0f}", f"{geo_tx/28:.1f}–{tx_m/28:.1f}×", "E021, E028, fig breakeven_bleo"),
    ("P2", "Space solar array specific power (W/kg, array level)", "88 median ROSA-family wing (flight and catalogue); 124 OPAL catalogue wing; large flown class 71–98 (R2-093)",
     f"≥ {pv_n:.0f}–{pv_m:.0f} even with a weightless transmitter", f"{pv_n/sc.B['next'].pv_w_per_kg:.1f}–{pv_m/sc.B['current'].pv_w_per_kg:.1f}× (each vs its own tier's array)", "E021"),
    ("P3", "GEO power-satellite service life (years)", "15 y median DESIGN life of GEO comsats (R12-022); no power satellite flown",
     f"none: counting whole spacecraft, one current/next-tier launch (1–10 GW, transmitter sized by power, D20) already exceeds orbital GPUs' {L:.0f}-y total, so no service life suffices; only the transmitter (P1) can change this", "n/a", "E021, E027, E028, E033"),
    ("P4", "Orbital-mirror scale per receiving site", "Earendil-1: 18×18 m, 142 kg (R1-112/113)",
     f"≥ {mirror_km2:.2f}–{mirror_km2_hi:.2f} km² of mirror over each spot at once (≈{mirror_km2*1e6/324:.0f}–{mirror_km2_hi*1e6/324:.0f} Earendil-1s) to clear the 2.6–5 W/m² inverter start (ideal / 50% low-light module)", "n/a", "E021, E028, R5-069"),
    ("P5", "Clear-sky fraction at mirror-fed sites", "0.66 all-hours mean, range 0.44–0.84, 12 PV regions (R12-016)",
     f"filed Earendil-1 system at its filed 1-y life: {'cannot win' if c_ideal > a_lo else f'≥ {c_ideal/a_lo:.2f}'} even with ideal coverage (needs > 1.0 clear sky); flown-sail density (ACS3, 200 g/m²) onto a fully covered receiver: ≥ {c_next_clear:.2f} ideal coverage, {'cannot win' if c_next_clear / sc.LAND > 1 else f'≥ {c_next_clear/sc.LAND:.2f}'} land-only", "n/a", "E023, E027, E028"),
    ("P6", "Launch price for orbital GPUs to match 97–99.4%-firm ground solar (launch cost only, per MWh of AI load)", "$3,600/kg (R1-057, STUDY-ASSUMED)",
     f"≤ ${launch_be[0]:.0f}–{launch_be[1]:.0f}/kg (hardware cost excluded)", f"{3600/launch_be[1]:.1f}–{3600/launch_be[0]:.1f}× cheaper", "E021 V3"),
    ("P7", "Photonic full-system support overhead (system ÷ optical core)", "318× (R3-045, Lightmatter Nature 2025)",
     f"H1' at 1024², to beat B300 by 10×: system ÷ core ≤ {real_fp4:.2f}× with measured parts and precision over real outputs (NVFP4 pairing; FP8 fails at any overhead); ≤ {lad['FP8'][0][2]:.1f}–{lad['FP4'][0][2]:.1f}× only in the idealised case (full-scale precision, unsourced 1 fF node); 318× is an upper bound (its core excludes laser and ADCs)", f"≥ {318/lad['FP4'][0][2]:.0f}× lower (idealised); unattainable at FP8", "E032 ladder (supersedes E028, E025, E018)"),
    ("P8", "Measured wall-plug energy of an integrating + receiverless photonic system", "none published (R7)",
     "a measured J/MAC including drivers, control and calibration", "n/a", "E022, R11"),
    ("P9", "Non-volatile photonic weight density (weights/mm²)", "5.8–3,183 (R8-104 upper bound; N2 SRAM 4.76 M, R8-084)",
     f"≥ ~10⁵/mm² to hold a 1 B-weight model on ~100 cm²; today H1' holds {r_sizes[0][1]/1e6:.1f}–{r_sizes[1][1]/1e6:.1f} M weights on {r_sizes[0][2]:.1f}–{r_sizes[1][2]:.0f} cm² ({r_sizes[0][0]}²–{r_sizes[1][0]}² × {ev2.LAYERS} layers)", "≥ 30×", "E028, R8-124"),
    ("P10", "Precision equivalence of analog fixed-point read-out", "no ledger claim links b-bit analog outputs to NVFP4/FP8 model accuracy",
     "a model run end-to-end on 5-bit fixed-point analog outputs (with measured noise) matching its NVFP4 or FP8 accuracy; note D11's σ = 1 LSB is ≈ b − 1.8 effective bits, and ENOB = b needs 12× the photons", "n/a", "D11 (E028), fresh-context AI reviews"),
    ("P12", "Optical loss of a 1024 × 1024 resident-weight layer, laser to detector (dB)", "20 dB assumed (R3-037, PROJECTED); no measured layer at this size",
     f"≤ {loss_be:.1f} dB for H1' (NVFP4 pairing, measured parts) for the whole system to stay within the 10× gate at all (system ÷ core ≥ 1); +6 dB over 20 dB leaves {lad['FP4'][5][2]:.2f}×", "n/a", "E032, E033"),
    ("P11", "Orbital reflector service life (years)", "~1 y operations, drag deorbit ~5 months (Earendil-1 filing, R1-115/116)",
     f"≥ {life_be[0]:.2f} y (filed Earendil-1 density) / ≥ {life_be[1]:.2f} y (flown-sail density) to match orbital GPUs, whole launches, all-hours cloud-free share, ideal coverage", f"{life_be[0]:.1f}×", "E028, E033"),
]
rows.sort(key=lambda r: int(r[0][1:]))
out = ["# Open problems — generated by scripts/open_problems.py. Do not edit by hand.\n",
       "Each row: what must improve, today's sourced value, the target our model derives, the gap, and where the number comes from. "
       "A team that closes any row changes the verdict — rerun `python3 scripts/verdict.py` with the new value.\n",
       "| # | Quantity | Today (source) | Target (derived) | Gap | Evidence |", "|---|---|---|---|---|---|"]
out += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} |" for r in rows]
(ROOT / "docs/generated").mkdir(exist_ok=True)
(ROOT / "docs/generated/open_problems.md").write_text("\n".join(out) + "\n")
if __name__ == "__main__":
    print("\n".join(out))
