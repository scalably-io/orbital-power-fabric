#!/usr/bin/env python3
"""Build the white paper from the evidence register: paper/paper.src.md -> paper/paper.md.

Every number in the prose is a {{placeholder}} filled here from the model (opf/, scripts/) or parsed from
evidence/claims.csv. The build fails if the template contains a typed number, an unresolved placeholder,
a claim/derivation/experiment ID that does not exist, an ACCESS-FAILED citation, an em dash or a hype word.
"""
import csv
import importlib.util
import io
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from opf import scenarios as sc
from opf.lifecycle import launches
from opf.params import VERIFIED


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"scripts/{name}.py")
    mod = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


vd, op, ev2 = load("verdict"), load("open_problems"), load("efficiency_v2")
R = vd.RESULTS
CLAIMS = {r["claim_id"]: r for r in csv.DictReader(open(ROOT / "evidence/claims.csv"))}


def num(cid: str, i: int = 0) -> float:
    """i-th number in a claim's value field (commas removed)."""
    vals = re.findall(r"\d+(?:\.\d+)?", CLAIMS[cid]["value"].replace(",", ""))
    return float(vals[i])


def f(x: float, d: int = 0) -> str:
    return f"{x:,.{d}f}"


def sig(x: float) -> str:
    return f(x, 0) if x >= 100 else (f(x, 1) if x >= 10 else f"{x:.3g}")


V: dict[str, str] = {}
L = R["L"]
V["L"] = f(L)
_alt, _mask = sc.b_leo_kg_per_kw.__defaults__
V.update(alt_km=f(_alt / 1e3), mask=f(_mask), gate="10",   # gate = SYNTHESIS gate 1 (10x vs B300)
         w_fp4=str(ev2.PAIRS["FP4"][0]), r_fp4=str(ev2.PAIRS["FP4"][1]), w_fp8=str(ev2.PAIRS["FP8"][0]), r_fp8=str(ev2.PAIRS["FP8"][1]),
         pue=f(sc.PUE, 2), ground_pv=f(sc.GROUND_PV * 100), lifecycles="10, 15 or 20")
V["version"] = "v1.0"
import datetime
V["date"] = datetime.date.today().isoformat()
# --- A ---
a_lo, a_hi = R["A"]["current"]
V.update(a_lo15=f(a_lo), a_hi15=f(a_hi), a_once_lo=f(R["A_once"]["current"][0], 1), a_once_hi=f(R["A_once"]["current"][1], 1),
         a_kwt=f(num("R1-005")), sat_life=f(num("R1-023")), a_launches=f(launches(L, sc.SAT_LIFE_LEO)),
         a_shortton=f(R["A_once"]["current"][0] * 0.90718474, 1),
         a_spec_lo=f(R["A"]["speculative"][0]), a_spec_hi=f(R["A"]["speculative"][1]), a_spec_kwt=f(num("R1-020")))
# --- B-LEO ---
V.update(bleo_cur=f(R["B_LEO"][("current", 208)][1]), bleo_next=f(R["B_LEO"][("next", 208)][1]),
         bleo_spec=f(R["B_LEO"][("speculative", 208)][1], 1), bleo_land_cur=f(R["B_LEO_land"]["current"]),
         tx_wkg=f(num("R2-043")), tx_kgm2=f(num("R2-043", 1), 1), tx_only=f(R["tx_only"]), tx_only15=f(R["tx_only"] * launches(L, 5)),
         need_tx=f(R["need_tx"]), need_tx_x=f(R["need_tx"] / 28, 1), pv_only=f(R["pv_only"]),
         pv_flown=f(sc.B["current"].pv_w_per_kg, 1), pv_cat=f(sc.B["next"].pv_w_per_kg, 1),
         need_tx_nasa=f(op.tx_n), pv_floor_lo=f(op.pv_n), pv_floor_hi=f(op.pv_m),
         chain_meas=f(sc.B["current"].post_pv * 100, 1), chain_nasa=f(sc.B["next"].post_pv * 100, 1),
         nasa_sys_lo=f(num("R2-018", 1)), nasa_sys_hi=f(num("R2-018", 0)), iorsa=f(num("R2-093", 0), 1))
# --- B-GEO ---
geo = {(g["tier"], g["gw"]): g for g in R["GEO"]}
V.update(geo_cap=f(R["geo_cap_rf_gw"], 2), geo_gw="10", geo_rf_next=f(geo[("next", 10)]["rf_gw"], 1),
         geo_rf_cur=f(geo[("current", 10)]["rf_gw"], 1), geo_life=f(sc.GEO_LIFE),
         geo_tx_be=f(R["GEO_tx_be"]["next"]), geo_tx_x=f(R["GEO_tx_be"]["next"] / 28, 1),
         geo_once_next=f(geo[("next", 10)]["once"], 1), geo_once_cur=f(geo[("current", 10)]["once"], 1),
         rectenna_km2=f(sc.geo_rectenna_m2() / 1e6, 1))
# --- C ---
V.update(c_cur15=f(R["C"][("current", 208)][1], 1), c_next15=f(R["C"][("next", 208)][1], 1), c_spec15=f(R["C"][("speculative", 208)][1], 1),
         c_cur_gm2=f(sc.C["current"].kg_per_m2 * 1000), c_next_gm2=f(sc.C["next"].kg_per_m2 * 1000),
         c_spec_gm2=f(sc.C["speculative"].kg_per_m2 * 1000, 1), mirror_life=f(sc.MIRROR_LIFE),
         c_launches=f(launches(L, sc.MIRROR_LIFE)), km2_lo=f(R["mirror_km2"][0], 2), km2_hi=f(R["mirror_km2"][1], 2),
         n_mirror_lo=f(R["mirror_count"][0]), n_mirror_hi=f(R["mirror_count"][1]),
         c_cur_wx=f(R["C_wx"][("current", "ideal")]["vals"][0], 1),
         c_next_be_clear=f(R["C_wx"][("next", "ideal")]["be_clear"], 2),
         c_cur_be_life=f(R["C_wx"][("current", "ideal")]["be_life"], 2), c_next_be_life=f(R["C_wx"][("next", "ideal")]["be_life"], 2),
         c_next_land=f(R["C_wx"][("next", "land-only")]["vals"][0]),
         start_lo=f(num("R5-069", 0), 1), start_hi=f(num("R5-069", 5)),
         clear_all=f(num("R12-016", 0), 2), clear_night=f(vd.NIGHT_CLEAR, 2), clear_global=f(sc.GLOBAL_CLEAR_SKY, 2),
         land=f(num("R12-019"), 1), earendil_kg=f(num("R1-112")), earendil_m2=f(num("R1-113", 2)))
# --- V3 ---
a3 = next(r for r in R["V3"] if r["name"].startswith("A current"))
_v3 = {r["name"].split(",")[0].split(" (")[0]: r for r in R["V3"]}
V.update(bleo_floor=f(_v3["B-LEO current"]["usd_mwh"]["starship_floor"]), cnext_floor=f(_v3["C next"]["usd_mwh"]["starship_floor"], 1))
V.update(ter_lo=f(R["terrestrial_usd_it_mwh"][0]), ter_hi=f(R["terrestrial_usd_it_mwh"][1]),
         firm_lo=f(num("R5-027")), firm_hi=f(num("R5-028")), launch_now=f(num("R1-057")),
         a3_now=f(a3["usd_mwh"]["current"]), a3_2035=f(a3["usd_mwh"]["speculative_2035"]),
         a3_be_lo=f(a3["be_usd_kg"][0]), a3_be_hi=f(a3["be_usd_kg"][1]), launch_2035=f(sc.LAUNCH_USD_PER_KG["speculative_2035"]),
         launch_floor=f(sc.LAUNCH_USD_PER_KG["starship_floor"]), a3_floor=f(a3["usd_mwh"]["starship_floor"], 1),
         grid_months=f(num("R5-042")), dc_plus=f((num("R6-122", 2) - 1) * 100, 1), dc_grid_plus=f((num("R6-122", 4) - 1) * 100, 1),
         vdc_plus=f((num("R6-121", 1) - 1) * 100, 1), cpo=f(num("R9-030", 2)), plug_lo=f(num("R9-030", 0)), plug_hi=f(num("R9-030", 1)))
# --- sensitivity ---
sw = R["sweep"]
V.update(sw_bleo_max=f(max(r["B-LEO"] for _, r in sw), 3), sw_geo_min=f(min(r["B-GEO 10 GW"] for _, r in sw), 2),
         sw_geo_max=f(max(r["B-GEO 10 GW"] for _, r in sw), 2), sw_c_min=f(min(r["C"] for _, r in sw), 2), sw_c_max=f(max(r["C"] for _, r in sw), 2))
# --- photonics ---
fs = {(fmt, reuse): ev2.family_s(fmt, reuse) for fmt in ev2.PAIRS for reuse in (64, 2048)}
fr = {(fmt, n, ro): ev2.family_r(fmt, n, ro) for fmt in ev2.PAIRS for n in (256, 1024) for ro in ("nep", "pc")}
V.update(decode_bound=f(fs[("FP4", 64)]["bound"], 2), decode_ratio_lo=f(min(fs[(k, 64)]["gpu"] / fs[(k, 64)]["total"] for k in ev2.PAIRS), 2),
         decode_ratio_hi=f(max(fs[(k, 64)]["gpu"] / fs[(k, 64)]["total"] for k in ev2.PAIRS), 2),
         gpu_decode_fp8=f(fs[("FP8", 64)]["gpu"] * 1e12, 2), hbm=f(num("R3-078"), 2), gpu_path=f(num("R9-005"), 1),
         tgp=f(num("R3-067")), hbm_bw=f(num("R1-100", 2) / num("R1-094")),          h1_core_fp4=f(fr[("FP4", 1024, "pc")]["core"] * 1e15, 2), h1_core_fp8=f(fr[("FP8", 1024, "pc")]["core"] * 1e15, 2),
         h1_sup_fp4=f(fr[("FP4", 1024, "pc")]["support_for_10x"], 1), h1_sup_fp8=f(fr[("FP8", 1024, "pc")]["support_for_10x"], 1),
         h1s_core_fp4=f(fr[("FP4", 256, "pc")]["core"] * 1e15, 1), h1s_sup_fp8=f(fr[("FP8", 256, "pc")]["support_for_10x"], 1),
         h1_nep_max=f(max(v["support_for_10x"] for k, v in fr.items() if k[2] == "nep"), 1),
         h1_cm2_lo=f(fr[("FP4", 256, "pc")]["cm2"], 1), h1_cm2_hi=f(fr[("FP4", 1024, "pc")]["cm2"]),
         h1_w_lo=f(256 * 256 * ev2.LAYERS / 1e6, 1), h1_w_hi=f(1024 * 1024 * ev2.LAYERS / 1e6, 1), layers=f(ev2.LAYERS),
         support_meas=f(num("R3-045")), lm_tops=f(num("R3-043"), 2), density=f(num("R8-104")), sram_density=f(num("R8-084"), 2),
         retention=f(num("R11-060")), wallplug=f(num("R8-072")))
lad = {fmt: ev2.ladder(fmt) for fmt in ev2.PAIRS}
V.update(lad_fp4_ideal=f(lad["FP4"][0][2], 1), lad_fp8_ideal=f(lad["FP8"][0][2], 1), lad_fp4_real=f(lad["FP4"][4][2], 2),
         lad_fp8_real=f(lad["FP8"][4][2], 2), lad_fp4_26=f(lad["FP4"][5][2], 2), lad_extra_db="6",
         lad_fp8_core_real=f(lad["FP8"][4][1] * 1e15, 0), lad_fp8_gain_real=f(560e-15 / lad["FP8"][4][1], 1),
         n_layer="1,024", node_ideal="1", loss_ideal="20",
         # D21: sigma_y / LSB = (sqrt(N)/3) / (2N / 2^b) for x ~ U[0,1], w ~ U[-1,1] over a +/-N full scale
         typ_lsb5=f((1024 ** 0.5 / 3) / (2 * 1024 / 2 ** ev2.PAIRS["FP4"][1]), 2),
         typ_lsb8=f((1024 ** 0.5 / 3) / (2 * 1024 / 2 ** ev2.PAIRS["FP8"][1]), 1))
# B300 chip figures parsed from the claim's unit text "(= 187 / 560 fJ/MAC)"
b300 = re.findall(r"(\d+) / (\d+) fJ/MAC", CLAIMS["R3-070"]["unit"])[0]
V.update(b300_fp4=b300[0], b300_fp8=b300[1])
from opf import limits
V["sun_nw"] = f(limits.thermal_mode_power_w(5772, 1550e-9, 1e12) * 1e9)
V["n_claims"] = f(sum(1 for r in CLAIMS.values() if r["status"] != "ACCESS-FAILED"))
V["n_measured"] = f(sum(1 for r in CLAIMS.values() if r["status"] == "MEASURED"))
V["n_failed"] = f(sum(1 for r in CLAIMS.values() if r["status"] == "ACCESS-FAILED"))
V["n_problems"] = f(len(op.rows))
V["core_share"] = f(num("R3-045", 1), 2)
from opf import orbit as _orbit
_hbm = {k: ev2.decode_cap(e) for k, e in ev2.HBM_ALT.items()}
_r42 = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", CLAIMS["R3-042"]["value"])]      # 65.5 TOPS, 78 W el., 1.6 W opt.
_core_w = num("R3-044")                                                                   # 0.25 W optical core
_sys_w = _r42[1] + _r42[2]
V.update(site_share=f(_orbit.terminator_site_fraction(*sc.b_leo_kg_per_kw.__defaults__) * 100, 1),
         cap_lambda=f(__import__("math").degrees(_orbit.central_angle(*sc.b_leo_kg_per_kw.__defaults__)), 1),
         geo_refuel=re.search(r"GEO needs (\d+) refuel", CLAIMS["R2-021"]["notes"]).group(1),
         sc3_kg=f(num("R1-073")), sc3_kw_lo=f(num("R1-076", 0)), sc3_kw_hi=f(num("R1-076", 2)),
         sc3_lo=f(num("R1-073") / num("R1-076", 2)), sc3_hi=f(num("R1-073") / num("R1-076", 0)),
         last_hours_cost=re.search(r"\$([\d,]+)/MWh more", CLAIMS["R5-028"]["notes"]).group(1),
         last_hours_share=re.search(r"Marginal ([\d.]+)%", CLAIMS["R5-028"]["notes"]).group(1),
         land_km2_gw=f(num("R5-031")), vdc_year=re.search(r"in (20\d\d)", CLAIMS["R6-016"]["notes"]).group(1),
         ret_hours=f(num("R11-060")), ret_days=f(num("R8-099")),
         lm_like_lo=f(_sys_w / (_core_w + _r42[2] / (num("R8-072") / 100))), lm_like_hi=f(_sys_w / (_core_w + _r42[2])),
         cap_lo=f(min(_hbm.values()), 1), cap_hi=f(max(_hbm.values()), 1),
         fp8_6=f(ev2.ladder("FP8", rbits=6)[4][2], 1), fp8_7=f(ev2.ladder("FP8", rbits=7)[4][2], 1),
         loss_be=f(op.loss_be, 1), swell_w=f(num("R2-072", 0), 1), swell_eff=f(num("R2-072", 1)), swell_m=f(num("R2-072", 2), 2),
         spot_km2=f(vd.SPOT_M2 / 1e6, 1), maple_cm=re.search(r"~(\d+) cm", CLAIMS["R2-053"]["claim"]).group(1),
         nasa_x=f(num("R2-018", 1) / num("R2-093", 0), 0), n_regions=re.search(r"across (\d+) representative", CLAIMS["R12-016"]["claim"]).group(1),
         gpu_decode_note="64")
_bleo = next(r for r in R["V3"] if r["name"].startswith("B-LEO current"))
V.update(bleo_be_lo=f(_bleo["be_usd_kg"][0]), bleo_be_hi=f(_bleo["be_usd_kg"][1]), r_fp8_7="7", r_fp8_6="6",
         oeo_pd=f(ev2.OEO_PD_J * 1e15, 1))
import math as _m
V.update(c_cur_real=f(R["C_real"][("current", 208)], 0), c_next_real=f(R["C_real"][("next", 208)], 0),
         c_spec_real=f(R["C_real"][("speculative", 208)], 1), farm_density=f(num("R5-077"), 1),
         site_conv_pct=f(sc.SITE_PV_REAL_FARM * 100, 1), pub_limit=f(num("R2-108", 2)))
_rect = sc.geo_rectenna_m2()
_rf = {t: sc.geo_rf_w(sc.B[t], 10e9) for t in ("next", "current")}
V.update(rect_wm2_lo=f(_rf["next"] * 0.95 / _rect), rect_wm2_hi=f(_rf["current"] * 0.95 / _rect),
         tx_diam_lo=f(_m.sqrt(4 * _rf["next"] / (num("R2-043") * num("R2-043", 1)) / _m.pi) / 1e3, 1),
         tx_diam_hi=f(_m.sqrt(4 * _rf["current"] / (num("R2-043") * num("R2-043", 1)) / _m.pi) / 1e3, 1))
_sc3 = [(num("R1-073"), num("R1-076", 0)), (3000.0, num("R1-076", 2))]   # 2,000 kg with the 100 kW description; "three-tonne" with 200 kW (R1-076 quote)
V.update(sc3_lo=f(min(m / k for m, k in _sc3)), sc3_hi=f(max(m / k for m, k in _sc3)))
_ld = ev2.ladder("FP4")
V.update(lad_node=f(_ld[1][2], 1), lad_oeo=f(_ld[2][2], 1), lad_prec=f(_ld[3][2], 1))
V.update(ret_s=f(num("R8-112")), maple_db=f(num("R2-057")))
V["T_caps"] = "; ".join(f"{f(v, 2)} times with {k}" for k, v in _hbm.items())
V["mg_share"], V["mg_cost"] = re.search(r"meeting (\d+)% of", CLAIMS["R5-029"]["claim"]).group(1), f(num("R5-029"))
V["hours_lo"] = re.search(r"(\d+(?:\.\d+)?)% of hours", CLAIMS["R5-027"]["claim"]).group(1)
V["hours_hi"] = re.search(r"(\d+(?:\.\d+)?)% of 24/365", CLAIMS["R5-028"]["claim"]).group(1)
V["mapl"] = f"{num('R2-053', 0)}–{num('R2-053', 1)}"
V["caltech_today"] = f(num("R2-065", 0), 2)
V["nasa_kwh_lo"], V["nasa_kwh_hi"] = f(num("R2-023", 0), 2), f(num("R2-023", 1), 2)


# --- tables ---
def table(header: list[str], rows: list[list[str]]) -> str:
    return "\n".join(["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] + ["| " + " | ".join(r) + " |" for r in rows])


def call(x, lo, hi):
    return "lighter" if x < lo else ("heavier" if x > hi else "inside the range")


rows = []
for tier in ("current", "next", "speculative"):
    lo, hi = vd.a_range(tier)
    b = R["B_LEO"][(tier, 208)][1]
    g = geo[(tier, 10)]["once"] * launches(L, sc.GEO_LIFE)
    c = R["C"][(tier, 208)][1]
    cr = R["C_real"][(tier, 208)]
    rows.append([tier, f"{f(lo)}–{f(hi)}", f"{f(b, 1)} ({call(b, lo, hi)})", f"{f(g, 1)} ({call(g, lo, hi)})", f"{f(c, 1)} ({call(c, lo, hi)})",
                 f"{f(cr, 1)} ({call(cr, lo, hi)})"])
V["T_summary"] = table(["tier", "GPUs in orbit (A)", "microwave, LEO, ideal coverage", "microwave, GEO, 10 GW",
                        "mirrors, fully covered receiver", "mirrors, onto a real solar farm"], rows)

rows = [[g["tier"], f"{g['gw']} GW", ("folded into system W/kg" if g["tier"] == "speculative" else f"{f(g['rf_gw'], 1)} GW"),
         f(g["once"], 1), ("none within the lifecycle" if g["life_needed"] == float("inf") else f"{f(g['life_needed'], 1)} y"),
         "wins" if g["life_needed"] <= sc.GEO_LIFE else "loses"] for g in R["GEO"]]
V["T_geo"] = table(["tier", "delivered", "RF to radiate", "kg per kW per launch", f"service life needed to match A over {f(L)} y (whole launches)", f"at the {f(sc.GEO_LIFE)}-year design life"], rows)

rows = []
for tier in ("current", "next", "speculative"):
    for cov in ("ideal", "land-only"):
        w = R["C_wx"][(tier, cov)]
        rows.append([tier, cov] + [f(x, 1) for x in w["vals"]] + [f"{f(vd.a_range(tier)[0])}–{f(vd.a_range(tier)[1])}",
                     (f"≥ {f(w['be_clear'], 2)}" if w["be_clear"] <= 1 else "cannot win"),
                     ("none within the lifecycle" if w["be_life"] == float("inf") else f"≥ {f(w['be_life'], 2)} y")])
V["T_mirror"] = table(["tier", "coverage", f"cloud-free {V['clear_all']}", f"night {V['clear_night']}", f"global {V['clear_global']}",
                       "same-tier A", "cloud-free share needed", "mirror life needed (whole launches)"], rows)

rows = [[r["name"].replace(", 208 rx", ""), f(r["kg"], 2), f"{f(r['life'])} y", f(r["usd_mwh"]["current"], 1), f(r["usd_mwh"]["speculative_2035"], 1),
         f"{f(r['be_usd_kg'][0])}–{f(r['be_usd_kg'][1])}"] for r in R["V3"]]
V["T_v3"] = table(["option", "kg per kW per launch", "life", f"launch $ per IT-MWh at ${V['launch_now']}/kg", f"at ${V['launch_2035']}/kg",
                   f"break-even $/kg vs ${V['ter_lo']}–{V['ter_hi']}"], rows)

V["T_sweep"] = table(["ranges drawn", "microwave, LEO", "microwave, GEO 10 GW", "mirrors"],
                     [[lab, f(r["B-LEO"], 3), f(r["B-GEO 10 GW"], 3), f(r["C"], 3)] for lab, r in sw])

rows = []
for (fmt, reuse), r in fs.items():
    rows.append(["decode, batch 64" if reuse == 64 else "prefill, 2,048-token reuse", f"{fmt} ({ev2.PAIRS[fmt][0]}-bit weights, {ev2.PAIRS[fmt][1]}-bit read-out)",
                 f(r["total"] * 1e15, 0), f(r["gpu"] * 1e15, 0), f(r["gpu"] / r["total"], 2), f(r["bound"], 2)])
V["T_stream"] = table(["workload", "precision pair", "photonic core + memory, fJ/MAC", "B300 board, fJ/MAC", "ratio", "cap with a free core"], rows)

rows = []
for (fmt, n, ro), r in fr.items():
    rows.append([f"{n} × {n}", f"{'NV' if fmt == 'FP4' else ''}{fmt}, {ev2.PAIRS[fmt][1]}-bit read-out",
                 "conventional receiver" if ro == "nep" else "photon→charge node", sig(r["core"] * 1e15), sig(r["ratio"]), sig(r["support_for_10x"])])
V["T_h1"] = table(["layer", "paired with", "read-out", "optical core, fJ/MAC", "B300 ÷ core", "system ÷ core allowed for 10×"], rows)

V["T_ladder"] = table(["cumulative change (one sourced step each)", "NVFP4 pairing: core fJ/MAC", "system ÷ core allowed for 10×",
                       "FP8 pairing: core fJ/MAC", "system ÷ core allowed for 10×"],
                      [[a[0].strip().lstrip("+ ").replace("…", "and").strip(), sig(a[1] * 1e15), sig(a[2]), sig(c[1] * 1e15), sig(c[2])]
                       for a, c in zip(lad["FP4"], lad["FP8"])])

V["T_open"] = "\n".join(l for l in (ROOT / "docs/generated/open_problems.md").read_text().splitlines() if l.startswith("|"))

rows = []
for name, prm in VERIFIED.items():
    rows.append([f"`{name}`", f"{prm.value:g}", prm.unit, prm.source.replace("ASSUMPTION:", "assumption: ")])
V["T_params"] = table(["parameter", "value", "unit", "source"], rows)

heads = sorted(re.findall(r"^### (D\d+) — (.+)$", (ROOT / "docs/DERIVATIONS.md").read_text(), re.M), key=lambda h: int(h[0][1:]))
V["T_derivations"] = table(["ID", "derivation"], [[d, t] for d, t in heads])

# --- render + asserts ---
src = (ROOT / "paper/paper.src.md").read_text()
used = set(re.findall(r"\{\{(\w+)\}\}", src))
missing = used - V.keys()
assert not missing, f"placeholders without a value: {sorted(missing)}"

ALLOWED = re.compile(r"\{\{\w+\}\}|SR-\d{4}-\d{3}|R\d+-\d{3}…\d{3}|R\d+-\d{3}|E\d{3}…E\d{3}|D01–D\d{2}|P1–P\d{1,2}|D\d{2}|E\d{3}|P\d{1,2}|"
                     r"GH200|G?B\d{3}|NVL\d+|H100|US\d+B\d|(NV)?FP\d|H\d'?|python3|"
                     r"[Ss]ection \d+(\.\d+)?|Table \d+|Figure \d+|Earendil-1|Starcloud-3|AI1|ACS3|L = 10, 15 (and|or) 20|"
                     r"Qwen2\.5-72B|OPF-MZI4|4 ?× ?4|800 VDC|CC BY 4\.0|Apache-2\.0|CERN-OHL-P-2\.0|20\d\d|^#+ \d+(\.\d+)*|^\d+\. |"
                     r"V[1-4]|MZI4|220 nm", re.M)
stray = [ln for ln in ALLOWED.sub("", src).splitlines() if re.search(r"\d", ln)]
assert not stray, "typed numbers in template (put them in a placeholder):\n" + "\n".join(stray[:20])

out = re.sub(r"\{\{(\w+)\}\}", lambda m: V[m.group(1)], src)
for cid in set(re.findall(r"R\d+-\d{3}", out)):
    assert cid in CLAIMS, f"unknown claim {cid}"
    assert CLAIMS[cid]["status"] != "ACCESS-FAILED", f"cites ACCESS-FAILED claim {cid}"
dtext = (ROOT / "docs/DERIVATIONS.md").read_text()
for d in set(re.findall(r"\bD\d{2}\b", out)):
    assert f"### {d} " in dtext, f"unknown derivation {d}"
etext = (ROOT / "EXPERIMENTS.md").read_text()
for e in set(re.findall(r"\bE\d{3}\b", out)):
    assert f"| {e} |" in etext, f"unknown experiment {e}"
dash = [l[:90] for l in out.splitlines() if "—" in l]
assert not dash, "em dash in the paper:\n" + "\n".join(dash[:8])
for w in ("revolutionary", "groundbreaking", "game-chang", "unprecedented", "breakthrough", "paradigm"):
    assert w not in out.lower(), f"hype word: {w}"
(ROOT / "paper/paper.md").write_text(out)
words = len(re.sub(r"^\|.*$", "", out, flags=re.M).split())
cited = set(re.findall(r"R\d+-\d{3}", out))
print(f"paper/paper.md: {words:,} words of prose (tables excluded), {len(used)} placeholders, "
      f"{len(cited)} claim IDs cited")
