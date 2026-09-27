#!/usr/bin/env python3
"""Verdict charts as inline SVG, generated from opf/scenarios.py (never hand-drawn).

House chart pattern (locked 2026-09-18): dataviz EMPHASIS form — our subject in brand green
#00c896, context in de-emphasis gray #9a978f; ink #0a0a09, muted #5a5a55, grid #e2dfd8, paper
#faf9f7; Instrument Serif title, Figtree labels, JetBrains Mono ticks; direct labels; <title>
hover on every mark; role="img" + aria-label; responsive viewBox.
Validator (dataviz/scripts/validate_palette.js, light, surface #faf9f7): gray fails the chroma
floor by design (it is the de-emphasis role, not a category); green contrast 2.06:1 and deutan
dE 6.1 are relieved by a direct label on every mark plus the table in docs/generated/verdict_v1.md.
Writes figures/verdict_mass.svg, figures/breakeven_bleo.svg, figures/index.html (preview).
"""
import html
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from opf import scenarios as sc
from opf.lifecycle import launches

GREEN, GRAY, INK, MUTED, GRID, PAPER = "#00c896", "#9a978f", "#0a0a09", "#5a5a55", "#e2dfd8", "#faf9f7"
SERIF = "'Instrument Serif', Georgia, serif"
SANS = "Figtree, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', Menlo, monospace"
L = 15.0


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def logx(v, lo, hi, x0, x1):
    return x0 + (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * (x1 - x0)


def signoff(w, h):
    return (f'<text x="{w-24}" y="{h-14}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}">'
            f'scalably<tspan fill="{GREEN}">.</tspan>io · orbital-power-fabric</text>')


def chart_mass() -> str:
    a_lo, a_hi = (x * L / sc.A["current"].life for x in sc.A["current"].kg_per_kw)
    rows = []
    for tier, lab in (("current", "today's parts"), ("next", "NASA study chain"), ("speculative", "NASA-implied")):
        rows.append((f"Microwave from LEO · {lab}", sc.b_leo_kg_per_kw(sc.B[tier], 208) * launches(L, sc.SAT_LIFE_LEO), sc.B[tier].src))
    for tier, lab in (("current", "today's parts"), ("next", "NASA study chain"), ("speculative", "NASA-implied")):
        tx_kg_m2 = 0.0 if tier == "speculative" else 44.7
        rows.append((f"Microwave from GEO, 10 GW · {lab}", sc.b_geo_kg_per_kw(sc.B[tier], 10e9, tx_kg_m2) * launches(L, sc.GEO_LIFE),
                     sc.B[tier].src + ", 15-y life R12-022, transmitter sized by power D20"))
    for tier, lab in (("current", "filed Earendil-1"), ("next", "flown ACS3 sail density"), ("speculative", "membrane + booms")):
        rows.append((f"Mirrors · {lab} · ideal receiver", sc.c_kg_per_kw(sc.C[tier], 208) * launches(L, sc.MIRROR_LIFE),
                     sc.C[tier].src + ", 1-y life R1-115, fully covered 30% PV receiver"))
        rows.append((f"Mirrors · {lab} · real solar farm", sc.c_kg_per_kw(sc.C[tier], 208, site_conv=sc.SITE_PV_REAL_FARM) * launches(L, sc.MIRROR_LIFE),
                     sc.C[tier].src + ", 1-y life R1-115, real tracking farm 5.9% of site light R5-077"))
    W, H = 900, 170 + 46 * len(rows) + 70
    x0, x1, top = 300, W - 60, 138
    lo, hi = 0.05, 3000
    y_end = top + 46 * len(rows)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" '
         f'aria-label="{esc("Launched mass per continuous kilowatt of AI load over 15 years. Orbital GPUs: " + f"{a_lo:.0f}-{a_hi:.0f}" + " kg/kW. " + "; ".join(f"{r[0]}: {r[1]:.2f} kg/kW" for r in rows))}">',
         f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         f'<text x="24" y="44" font-family="{SERIF}" font-size="27" fill="{INK}">What it costs to launch 1 kW of always-on AI</text>',
         f'<text x="24" y="70" font-family="{SANS}" font-size="13" fill="{MUTED}">Launched kg per continuous kW over 15 years, log scale. Grey band: GPUs in orbit (SpaceX AI1-class).</text>',
         f'<text x="24" y="88" font-family="{SANS}" font-size="13" fill="{MUTED}">Benefit of the doubt: ideal receiver spacing, no clouds, dawn-dusk sun, no storage. Mirrors live 1 year (as filed).</text>']
    xa, xb = logx(a_lo, lo, hi, x0, x1), logx(a_hi, lo, hi, x0, x1)
    s.append(f'<rect x="{xa:.1f}" y="{top-18}" width="{xb-xa:.1f}" height="{y_end-top+18}" fill="{GRAY}" fill-opacity="0.22">'
             f'<title>GPUs in orbit · current · {a_lo:.1f}–{a_hi:.1f} kg/kW over 15 y · R1-005, R1-012, R1-023</title></rect>')
    s.append(f'<text x="{(xa+xb)/2:.1f}" y="{top-24}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTED}">'
             f'GPUs in orbit {a_lo:.0f}–{a_hi:.0f}</text>')
    for v in (0.1, 1, 10, 100, 1000):
        x = logx(v, lo, hi, x0, x1)
        s.append(f'<line x1="{x:.1f}" y1="{top-8}" x2="{x:.1f}" y2="{y_end}" stroke="{GRID}" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{y_end+18}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">{v:g}</text>')
    s.append(f'<text x="{(x0+x1)/2:.1f}" y="{y_end+38}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTED}">'
             f'kg launched per continuous kW, 15 years  ·  ← lighter than orbital GPUs   heavier →</text>')
    for i, (name, val, src) in enumerate(rows):
        y = top + 20 + 46 * i
        x = logx(val, lo, hi, x0, x1)
        s.append(f'<text x="{x0-16}" y="{y+4}" text-anchor="end" font-family="{SANS}" font-size="12" fill="{INK}">{esc(name)}</text>')
        s.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{GRID}" stroke-width="1" stroke-dasharray="2 4"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{y}" r="7" fill="{GREEN}" stroke="{PAPER}" stroke-width="3">'
                 f'<title>{esc(name)} · {val:.2f} kg/kW over 15 y · {esc(src)}</title></circle>')
        s.append(f'<text x="{x+13:.1f}" y="{y+4}" font-family="{MONO}" font-size="11" fill="{INK}">{val:.3g}</text>')
    s.append(signoff(W, H))
    s.append("</svg>")
    return "\n".join(s)


def chart_breakeven() -> str:
    """B-LEO beats A (lower bound 40 kg/kW / 15 y) where 1/pv + k/tx < C; C = A * chain / (1000 PUE L/life)."""
    a_lo = sc.A["current"].kg_per_kw[0] * L / sc.A["current"].life
    W, H = 900, 580
    x0, x1, y0, y1 = 110, W - 60, 490, 130
    lo_x, hi_x, lo_y, hi_y = 10, 10000, 10, 10000
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" '
         f'aria-label="Break-even map for microwave power beaming from low Earth orbit versus GPUs in orbit. Today\'s flown hardware sits far below and left of both break-even curves.">',
         f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         f'<text x="24" y="44" font-family="{SERIF}" font-size="27" fill="{INK}">How much lighter must beaming hardware get?</text>',
         f'<text x="24" y="70" font-family="{SANS}" font-size="13" fill="{MUTED}">Microwave beaming from LEO beats GPUs in orbit only up and to the right of a curve '
         f'(ideal coverage, no bus mass, 15 years, {a_lo:.0f} kg/kW).</text>']
    ly = lambda v: y0 - (math.log10(v) - math.log10(lo_y)) / (math.log10(hi_y) - math.log10(lo_y)) * (y0 - y1)
    lx = lambda v: logx(v, lo_x, hi_x, x0, x1)
    for v in (10, 100, 1000, 10000):
        s.append(f'<line x1="{lx(v):.1f}" y1="{y1}" x2="{lx(v):.1f}" y2="{y0}" stroke="{GRID}"/>')
        s.append(f'<text x="{lx(v):.1f}" y="{y0+18}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">{v:g}</text>')
        s.append(f'<line x1="{x0}" y1="{ly(v):.1f}" x2="{x1}" y2="{ly(v):.1f}" stroke="{GRID}"/>')
        s.append(f'<text x="{x0-10}" y="{ly(v)+4:.1f}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}">{v:g}</text>')
    s.append(f'<text x="{(x0+x1)/2:.1f}" y="{y0+42}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTED}">solar array specific power, W/kg</text>')
    s.append(f'<text x="30" y="{(y0+y1)/2:.1f}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTED}" '
             f'transform="rotate(-90 30 {(y0+y1)/2:.1f})">transmitter specific power, W/kg RF out</text>')
    gaps = []
    for tier, lab in (("current", "measured chain (14.1%)"), ("next", "NASA study chain (37.1%)")):
        t = sc.B[tier]
        k, cc = 0.90 * t.dc_rf, a_lo * t.post_pv / (1000 * sc.PUE * L / sc.SAT_LIFE_LEO)
        pts = []
        for i in range(400):
            pv = 10 ** (math.log10(lo_x) + i / 399 * (math.log10(hi_x) - math.log10(lo_x)))
            if 1 / pv < cc:
                tx = k / (cc - 1 / pv)
                if lo_y <= tx <= hi_y:
                    pts.append(f"{lx(pv):.1f},{ly(tx):.1f}")
        if pts:
            s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{GRAY}" stroke-width="2.5" stroke-linecap="round">'
                     f'<title>break-even · {lab} · array &gt; {1/cc:.0f} W/kg and transmitter &gt; {k/cc:.0f} W/kg required · R2-042/R2-011</title></polyline>')
            if tier == "next":        # left curve: label on its left, higher up
                pv_at, ty, anchor, dx = 1 / (cc - k / 5000), 5000, "end", -10
            else:                     # right curve: label on its right
                pv_at, ty, anchor, dx = 1 / (cc - k / 3000), 3000, "start", 10
            s.append(f'<text x="{lx(pv_at)+dx:.1f}" y="{ly(ty)+4:.1f}" text-anchor="{anchor}" font-family="{SANS}" font-size="12" fill="{MUTED}">{lab}</text>')
            gaps.append((lab, 1 / cc, k / cc))
    for pv, tx, lab, src in ((88.15, 28.0, "today: median ROSA-family wing + ground-test GaN transmitter", "R2-093, R2-043"),
                             (124.1, 28.0, "OPAL catalogue wing (large flown class 71–98 W/kg)", "R2-093 OPAL")):
        s.append(f'<circle cx="{lx(pv):.1f}" cy="{ly(tx):.1f}" r="7" fill="{GREEN}" stroke="{PAPER}" stroke-width="3">'
                 f'<title>{esc(lab)} · {pv:g} W/kg array · {tx:g} W/kg transmitter · {src}</title></circle>')
    s.append(f'<text x="{lx(88.15)-10:.1f}" y="{ly(28)+26:.1f}" font-family="{SANS}" font-size="12" fill="{INK}">'
             f'arrays 88 (ROSA median) to 124 (catalogue) W/kg · measured transmitter 28 W/kg</text>')
    s.append(f'<text x="{lx(3500):.1f}" y="{ly(1200):.1f}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTED}">beaming beats orbital GPUs here</text>')
    (l1, pv1, tx1), (l2, pv2, tx2) = gaps
    s.append(f'<text x="24" y="90" font-family="{SANS}" font-size="13" fill="{MUTED}">Floors (the other part weightless): array ≥ {pv2:.0f}–{pv1:.0f} W/kg '
             f'({pv2/sc.B["next"].pv_w_per_kg:.1f}–{pv1/sc.B["current"].pv_w_per_kg:.1f}× its tier), transmitter ≥ {tx2:.0f}–{tx1:.0f} W/kg ({tx2/28:.1f}–{tx1/28:.1f}×).</text>')
    s.append(signoff(W, H))
    s.append("</svg>")
    return "\n".join(s)


def main():
    out = ROOT / "figures"
    out.mkdir(exist_ok=True)
    a, b = chart_mass(), chart_breakeven()
    (out / "verdict_mass.svg").write_text(a)
    (out / "breakeven_bleo.svg").write_text(b)
    (out / "index.html").write_text(f'<!doctype html><meta charset="utf-8"><title>OPF charts</title>'
                                     f'<body style="margin:0;background:{PAPER};max-width:960px">'
                                     f'<figure style="margin:24px">{a}</figure><figure style="margin:24px">{b}</figure></body>')
    print("wrote figures/verdict_mass.svg, figures/breakeven_bleo.svg, figures/index.html")


if __name__ == "__main__":
    main()
