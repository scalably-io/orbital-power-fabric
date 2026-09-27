# R5 — Terrestrial baseline (branch T) and PV at low irradiance (branch C)

Researcher R5 · retrieved 2026-09-27 · ledger: `evidence/research/R5-terrestrial.csv` (91 rows: 87 claims + 4 ACCESS-FAILED; `scripts/validate_evidence.py` → 0 rejected). Every quote was string-matched against the downloaded source by `evidence/sources/R5/build_r5.py` before the CSV was written; a deliberately wrong quote fails that check.

## (a) Verdict

1. **Energy on Earth is cheap.** New unsubsidized utility PV costs $40–98/MWh (R5-001) and CCGT $51–129/MWh (R5-005). US industrial retail power averaged 8.62 ¢/kWh in 2025 (R5-032). Near-24/7 solar plus battery costs $104/MWh at 97% of hours (R5-027) and $167/MWh at 99.4% (R5-028). A 90%-solar off-grid data-centre microgrid costs $109/MWh (R5-029). NASA's SBSP baseline is $610–1,590/MWh (NEGATIVE-FINDINGS #7): 4–15× these figures.
2. **On Earth the constraint is time, not cost.** The median US generator took 61 months from request to operation (R5-042). Data-centre connection queues reach up to 7 years in Northern Virginia (R5-035). In 2025 Dominion connected 0.744 GW of data centres against >48 GW in contracting (R5-046). The IEA puts ~20% of planned projects at risk of delay (R5-037). This is the only axis on which an orbital option could compete. Off-grid PV+storage also avoids the grid queue, and PV builds in 1–4 years (R5-033).
3. **Power is a minority of AI capex.** A GB300 NVL72 rack costs $27–48k per kW of IT (R5-085). Near-24/7 PV+battery costs about $11.8k per continuous kW (R5-086). Electricity costs $0.46–1.46k per kW-yr (R5-087).
4. **Low light: a rack-sized mirror (0.02 W/m²) produces zero AC.** A median utility inverter starts at about 2.6 W/m² plane-of-array with an ideal module, and about 5 W/m² at realistic low-light efficiency (R5-069, R5-070). The rack mirror falls 130–6,400× short of that threshold (R5-073).
5. **A km²-class mirror (10–100 W/m²) is above the threshold, but yields little.** A tracking plant under it gives only 0.3–5 MW_DC per km² (R5-074, R5-075), against ~59 MW_DC/km² peak in sunlight (R5-077).
6. **Land.** Tracking PV array density is 59 MW_DC/km² and 97 GWh/km²/yr (R5-077, R5-079). Total fenced area is lower, at about 30 MW_AC/km² (R5-081). A 90%-solar 24/7 design needs about 10 km² per GW of continuous load (R5-031).

## (b) Model inputs (tier `current` unless noted)

| Parameter | Value | Provenance | claim_id |
|---|---|---|---|
| Utility PV LCOE, unsubsidized (US new build) | 40–98 $/MWh (avg 69) | STUDY-ASSUMED | R5-001 |
| Utility PV LCOE, empirical 2024 fleet (no ITC) | 60 $/MWh | STUDY-ASSUMED | R5-018 |
| Utility PV PPA price, 2024 COD (IQR) | 22–40 $/MWh (mean 29) | FILING | R5-019 |
| Solar PPA offer, P25 North America, Q2 2026 | 52.65 $/MWh | VENDOR-STATED | R5-022 |
| PV + 4 h storage (50%) LCOE | 61–156 $/MWh | STUDY-ASSUMED | R5-003 |
| PV+battery hybrid LCOE, US 2024 (before ITC) | 87 $/MWh | STUDY-ASSUMED | R5-020 |
| Solar LCOE + capacity firming, 6 ISOs | 92–135 $/MWh | STUDY-ASSUMED | R5-008 |
| Near-24/7 solar (97% of hours) | 104 $/MWh (6 kW PV + 17 kWh per continuous kW) | STUDY-ASSUMED | R5-027 |
| 99.4% of hours | 167 $/MWh (7 kW PV + 35 kWh per kW) | STUDY-ASSUMED | R5-028 |
| 90% solar + gas backup, off-grid DC | 109 $/MWh (off-grid gas 86) | STUDY-ASSUMED | R5-029 |
| CCGT LCOE | 51–129 $/MWh; capex 1,450–2,100 $/kW (quotes 2,400–2,600) | STUDY-ASSUMED | R5-005, R5-006 |
| Nuclear PPA benchmarks | TMI ~110–115 $/MWh (analyst); Talen–Amazon ≥61 $/MWh (lower bound) | STUDY-ASSUMED / DERIVED | R5-023, R5-026 |
| US industrial retail price 2025 | 8.62 ¢/kWh (2026 YTD 9.03) | MEASURED | R5-032 |
| Utility PV capex | 1.49 $/W_AC (ATB 2024); 1.61 $/W_AC = 1.22 $/W_DC installed 2024 | STUDY-ASSUMED / MEASURED | R5-011, R5-017 |
| PV fixed O&M | 24.66 $/kW_AC-yr | STUDY-ASSUMED | R5-012 |
| PV AC capacity factor (US, tracking) | 19.4–31.5% | STUDY-ASSUMED | R5-013 |
| Battery capex 2024 | 241 $/kWh + 372 $/kW (4 h = 334 $/kWh); all-in hybrids 458 $/kWh | STUDY-ASSUMED / MEASURED | R5-014, R5-021 |
| Battery life / RTE | 15 yr / 85% | STUDY-ASSUMED | R5-015 |
| Battery 2035 (low/mid/high), tier `next` | 147/243/339 $/kWh | PROJECTED | R5-016 |
| Standalone 4 h LCOS | 210–292 $/MWh | STUDY-ASSUMED | R5-007 |
| PV array power density (tracking / fixed) | 59.3 / 86.5 MW_DC per km² | DERIVED from MEASURED | R5-077 |
| PV energy density (tracking / fixed) | 97.4 / 110.5 GWh/km²/yr | DERIVED from MEASURED | R5-079 |
| PV total-area density (NREL 2013, 1-axis) | 29.8 MW_AC/km²; 74.9 GWh/km²/yr | DERIVED | R5-081 |
| Land, 24/7 90%-solar DC | 10.2 km² per GW continuous | DERIVED | R5-031 |
| Generator interconnection, median | 61 months | MEASURED | R5-042 |
| DC load connection queue | US 1–3 y; N. Virginia up to 7 y | STUDY-ASSUMED | R5-035 |
| Grid connection lead time / transmission build | 3–7+ y / 4–8 y | STUDY-ASSUMED | R5-034, R5-036 |
| Global DC demand 2030 | 945–950 TWh (485 TWh in 2025) | PROJECTED | R5-038, R5-039 |
| US DC demand 2030 | 521–843 TWh (192 TWh in 2024) | PROJECTED | R5-041 |
| GB300 NVL72 rack power | 135 kW TDP, 155 kW peak | VENDOR-STATED | R5-082 |
| GB300 NVL72 rack price | 3.7–4.0 $M (Loop) to 6.0–6.5 $M (Tom's HW) | STUDY-ASSUMED | R5-083, R5-084 |
| Rack capex per kW_IT | 27.4–48.1 k$/kW | DERIVED | R5-085 |
| Inverter start power Pso/Paco (169 inverters ≥1 MW) | median 0.35% (IQR 0.25–0.45%) | DERIVED from FILING | R5-068 |
| PV plant start irradiance | 2.6 W/m² (ideal) · ~5 W/m² (r=0.5); range 0.5–7.6 | DERIVED | R5-069 |

## (c) The low-light answer

**Physically, a utility PV plant stops producing at about 1–10 W/m² plane-of-array. The central estimate is 2.6 W/m² with an ideal module and about 5 W/m² allowing for low-light efficiency (R5-069).** Below that, the array's DC power is less than the inverter's start power Pso, so AC output is zero. The inverter then draws its night tare, Pnt (R5-066). PVsyst's modelling rule of thumb agrees: 0.5% of Pnom corresponds to 5 W/m² (R5-070).

"Useful" output is a different question. Heavy overcast gives 30–50 W/m² (R5-071), and energy below the threshold is under 0.1% of a normal site's annual energy (R5-072). No commercial plant is designed to run on 10 W/m².

Curve points found (cell-level unless marked):

| Irradiance (W/m²) | Efficiency / relative to STC | Source | claim_id |
|---|---|---|---|
| 1000 | 0.070 abs (1.00) — lab mc-Si cell | Reich 2009 Fig. 2b | R5-056 |
| 200 | 0.97 (modern TOPCon module) · 0.88 (2009 mono-Si module) | Adani datasheet · Solar ABCs | R5-052, R5-051 |
| ~100 | 0.84 (mono-Si module, outdoor) · ~0.84 (lab cell at ~150) | Solar ABCs · Reich | R5-050, R5-057 |
| ~10 | 0.035 abs (0.50) | Reich Fig. 2b | R5-058 |
| ~3 | 41 commercial cells: 2.3–13.1% abs c-Si, 1.5–5.9% mc-Si (STC ~15%); same-bin pair 0.19 vs 0.40 | Reich §2.2 | R5-053, R5-054 |
| 2.93 (LED) | 9.3% abs c-Si mini-module (12.5% cell), visible-only spectrum | NIST 2021 | R5-065 |
| ~2 | 0.020 abs (0.29) | Reich Fig. 2b | R5-059 |
| ~0.7 | 0.012 abs (0.17) | Reich Fig. 2b | R5-060 |
| ~0.1 | 0.003 abs (0.04) | Reich Fig. 2b | R5-061 |
| ~0.04 (lowest measured) | 0.0015 abs (0.02) | Reich Fig. 2b | R5-062 |
| Voc at 1000 / 10 / 2 / 0.1 / 0.04 | 0.54 / 0.34 / 0.24 / 0.06 / 0.03 V | Reich Fig. 2b | R5-063 |

Mechanism: below ~100 W/m² efficiency falls roughly logarithmically, because Voc ∝ ln(Jsc). Shunt resistance then dominates, so cells from the same power bin can diverge by 2× (R5-055, R5-054).

Consequences for branch C:
- **Rack mirror, 0.0207 W/m².** The array DC output is ≈2×10⁻⁵ × r of STC, where r is the low-light relative efficiency (≈0.02 at 0.04 W/m²). The inverter start threshold is 2.6×10⁻³ of array STC. The result is zero AC, a 130–6,400× shortfall (R5-073). In daylight the extra light adds only a 0.002% boost.
- **km²-class mirror at 10–100 W/m².** A tracking plant yields about 0.30 MW_DC/km² at 10 W/m² and about 5.0 MW_DC/km² at 100 W/m² (R5-074, R5-075). One 135 kW rack would need about 0.027 km² of PV under a continuous 100 W/m² (before PUE and conversion losses).

## (d) Negative findings

1. **Lazard publishes no 24/7 solar cost.** Its PV+storage case is 4 h at 50% of PV nameplate (R5-003, R5-009). Its "LCOE + firming" is a capacity-accreditation adder that "does not represent the cost of building a 24/7 firm resource on a single project site" (R5-010). The 24/7 figures here come from Ember and Paces/Scale/Stripe, which are study models (R5-027..R5-031).
2. **No standard data below 100 W/m².** The IEC 61853-1 matrix stops at 100 W/m² (R5-049). No accessible modern (TOPCon/HJT/CdTe) module-level measurement between 1 and 100 W/m² was found. The sub-100 curve rests on one 2009 lab mc-Si cell (7% STC), 41 commercial 2009-era cells at 3 W/m², and one NIST LED point. Modern cells likely do better, but that is unmeasured here.
3. **Two sources disagree on voltage.** PVsyst models no voltage threshold, saying "array MPP voltage remains significant" at very low irradiance (R5-070 notes). Reich's cell loses about 56% of Voc by 2 W/m² and about 95% by 0.04 W/m² (R5-063). Both can be true for different cell quality and irradiance ranges. Branch C at sub-W/m² fails on either reading, because of the power threshold.
4. **No national dataset of large-load wait times.** LBNL Queued Up covers generators and storage only (R5-044). Load wait times come only from utility and ISO statements and IEA compilations (R5-035, R5-045, R5-046).
5. **Soft prices.** GB300 NVL72 has no vendor list price; the two press estimates differ 1.7× (R5-083, R5-084). The TMI PPA price is an analyst estimate (R5-023). The Talen–Amazon $/MWh can only be lower-bounded (R5-026). LevelTen P25 values are developer offers, not executed contracts (R5-022).
6. **Ember's numbers are not US numbers.** Ember uses 2024 global-average prices, and its text gives "average global battery prices ... $165/MWh", apparently meaning $/kWh; that figure was not used. US all-in hybrid battery capex was $458/kWh in 2024 (R5-021), so US 24/7 solar costs more than $104/MWh. This is still a small multiple of grid power and far below SBSP.
7. **The rack-scale reflector is dead on sourced data** (confirms NEGATIVE-FINDINGS #3; R5-073).

## (e) Failed sources

| Source | Failure | Workaround |
|---|---|---|
| Mavromatakis et al. 2017, *Low irradiance losses of PV modules* (R5-088) | OSTI connection refused / timeout; ScienceDirect 403; no abstract via Crossref or Semantic Scholar | none — search-snippet numbers not used |
| King et al. 2007, SAND2007-5036 inverter model (R5-089) | OSTI timeout | pvlib docs (R5-066) + SAM CEC library (R5-067) |
| ERCOT April 2026 large-load update (R5-090) | Incapsula bot wall / 403 | Utility Dive report of Dec 2025 ERCOT board (R5-045) |
| HPE GB300 NVL72 QuickSpecs (R5-091) | empty response / 60 s timeout | Lenovo LP2357 (R5-082) |
| atb.nrel.gov | DNS ENOTFOUND (NREL renamed; site moved) | atb.nlr.gov, docs.nlr.gov — resolved |
| LBNL emp.lbl.gov PDFs | Cloudflare challenge without browser UA | re-fetched with UA — resolved |
| renewablesnow (LevelTen), RSC indoor-PV review | 403 / Cloudflare | pv magazine USA; NIST paper on PMC — resolved |
| LevelTen's own Q2 2026 page | fetched text lacked the P25 numbers | pv magazine report (R5-022) |

All downloads and scratch files are in `evidence/sources/R5/`.

## (f) Open questions

1. **Modern-module efficiency between 1 and 100 W/m².** Source it from the NREL PERT field I-V dataset (Marion et al. 2014, OEDI/OSTI 1811521), a retry of Mavromatakis 2017, or a lab measurement. This decides how much a km²-mirror plant yields.
2. **US-cost 24/7 PV+battery LCOE.** Compute it in `opf/` from ATB and NREL inputs (R5-011..R5-016) rather than rely on Ember's global prices. Ember's "6 GW" DC-vs-AC basis is unstated, which affects R5-086.
3. **PUE for GB300-class liquid-cooled halls** was not sourced here, but is needed to convert IT kW to site kW. HPE (132 kW) vs Lenovo (135 kW) TDP also needs reconciling.
4. **Twilight light for branch C.** Dawn–dusk reflector light arrives on long slant paths (spectral shift, extinction). Does the architecture add light to daytime sun or deliver it alone at night? That choice decides whether the inverter threshold or only the marginal efficiency applies.
5. **Primary large-load wait times** (ERCOT April 2026, PJM, ComEd). Retry with a browser.
6. **Lead for R1/C:** arXiv 2608.06433, "Atmospheric Light Pollution by Proposed Reflect Orbital Space Mirrors" (Aug 2026), not read.
