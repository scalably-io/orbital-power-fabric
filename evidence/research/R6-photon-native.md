# R6: Photon-native and DC-native. Which conversions can be skipped?

Researcher R6 · retrieved 2026-09-27 · `R6-photon-native.csv`: 93 rows (81 claims + 12 ACCESS-FAILED), and `scripts/validate_evidence.py` rejected none of them. A script (`evidence/sources/R6/_build_r6.py`) checked every quote against the downloaded source text before the CSV was written. Curly quotes and dashes were converted to ASCII for that check, so the CSV quotes use ASCII punctuation. Sources and scratch helpers are in `evidence/sources/R6/`. Rows R2-xxx and R3-xxx are cited, not duplicated.

## (a) Verdict

1. **Keeping power as DC pays off now. Keeping it as light mostly doesn't yet**, except for narrow vision front ends and for holding optical weights.
2. From the grid to the 12 V board bus, today's AC chain loses 9.2% (0.908, R6-120). A native 800 VDC chain loses 4.5% (0.955, R6-121), a gain of **+5.2%**. That matches NVIDIA's "up to 5%" (R6-016). Measured 380 VDC sites showed 5–7% (R6-009) and 10% (R6-011).
3. **The biggest DC gain is on-site PV fed straight onto the DC bus: +6.8%** over AC-coupled on-site PV and **+12.4%** over PV delivered through the grid (DERIVED, R6-122). Measured savings in buildings are 4–8% (R6-013).
4. The largest remaining loss is not AC/DC at all. The 12 V→die regulator loses about 8% (R6-029). Estimated end-to-end delivery from platform to die today is below 70% (R6-031). A DC-native facility leaves that block untouched.
5. **Solar-pumped lasers (sunlight→laser with no electricity) are 2.6× worse today** than PV→DC-DC→fibre laser: the measured record is 4.64% (R6-060) against 12% for the PV chain (R6-123). No flight was found, and JAXA's own baseline is now a fibre laser (R6-069).
6. The best laser power converters are 68.9% at 858 nm (R6-040) and 53.7% at 1550 nm (R6-041, a lab web page). A buyable 808 nm unit reaches about 60% (R6-051). All of these run at 5–160 W/cm², which is 65–2,000× the 802 W/m² of sunlight in R6-061 (DERIVED: 5.2/0.0802 to 160/0.0802).
7. **Non-volatile optical weights remove hold power entirely**: thermo-optic shifters draw 1.3–25 mW per π, versus zero (R6-090/091). They beat thermo-optic holding when the weights stay fixed longer than 0.1 µs to 40 ms (R6-125). But multilevel endurance ranges from 27 cycles to 1.4e8 cycles (R6-095, R3-013).
8. Computing on natural light is real but narrow: 94% of a small vision CNN's operations move into passive optics (R6-082), and ACCEL drops the ADC (R6-080). Nothing like this exists for LLM-class compute, and I found no demonstration that splits the solar spectrum and sends one band to photonic compute.

## (b) Conventional chain

| Step | Domains | Efficiency | Status | claim_id |
|---|---|---|---|---|
| Grid transmission and distribution (remote generation) | ac→ac | ~95% (5% loss, US 2018–22) | MEASURED (EIA estimate) | R6-003 |
| PV inverter, utility central | dc→ac | 98.5% CEC-weighted (98.8% max) | VENDOR-STATED | R6-001 |
| MV/LV transformer, 2500 kVA, 50% load | ac→ac | ≥99.53% (US floor); 98% measured in 2006 demo | FILING / MEASURED | R6-002, R6-008 |
| UPS double conversion | ac→dc→ac | up to 97% new; installed base 86–95% at full load, 81–93% at 25% load | VENDOR-STATED / MEASURED | R6-004, R6-006 |
| Server PSU (AC→54/12 V), ≥750 W | ac→dc | 90 / 94 / 96 / 91% at 10/20/50/100% load (Titanium-level floor) | FILING | R6-007 |
| 54/48 V→12 V board stage | dc→dc | ~98% | STUDY-ASSUMED | R6-120 notes |
| 48 V→~1 V regulator (includes 48→12 V) | dc→dc | 90% reference; 90.9% measured hybrid | STUDY-ASSUMED / MEASURED | R6-029, R6-033 |
| Board/package delivery, platform→die | dc→dc | <70% estimated; >30% loss reported | STUDY-ASSUMED | R6-031, R6-030 |
| **Grid MV → 12 V bus, AC today** | | **0.908** | DERIVED | R6-120 |
| Measured best AC chain, 2006 (UPS·transformer·PSU) | | 0.79 | MEASURED | R6-008 |
| Electrically pumped laser (DC→light) | dc→photon | ~38% fibre laser | VENDOR-STATED | R2-073 |
| Laser power converter (LPC), 808 nm, buyable | photon→dc | ~60% at 1 W in | DERIVED from vendor data | R6-051 |
| LPC 858 nm (GaAs thin film) | photon→dc | 68.9% at 11.4 W/cm² | MEASURED | R6-040 |
| LPC 811 nm, 6-junction | photon→dc | >64% at 160 W/cm² (65% peak at 30–75) | MEASURED | R6-045 |
| LPC 1064 nm | photon→dc | 50.6% at 5.2 W/cm² | MEASURED | R6-049 |
| LPC 1319 nm | photon→dc | 52.8% at 5.9 W/cm² | MEASURED | R6-043 |
| LPC 1446 / 1455 nm, 4-junction | photon→dc | 53.6% at 15.2 W/cm²; 55.9% at 27.1 W/cm² | MEASURED | R6-046, R6-047 |
| LPC 1550 nm | photon→dc | 53.7% at 12.9 W/cm² (lab page); germanium 30.8% at 6.7 W/cm² | MEASURED | R6-041, R6-048 |
| LPC 1520 nm, 10-junction | photon→dc | 45.6% at 16.5 W/cm² | MEASURED | R6-042 |

## (c) Alternatives that skip steps

| Alternative | Steps removed | Efficiency vs the chain it replaces | Tier | claim_ids |
|---|---|---|---|---|
| 380 VDC facility (built 2006–2012) | UPS inverter, PDU transformer, PSU rectifier | 5–7% less input energy than best AC (measured); 10% (measured, vendor-reported) | current | R6-009, R6-011 |
| 800 VDC facility (SST + 800→12.5 V) | LV transformer, UPS double conversion, rack AC/DC PSU, 54 V bus | Grid→12 V: 0.955 vs 0.908, **+5.2%**. DERIVED; next-tier DC vs current-tier AC, a mismatch I flag. NVIDIA/Vertiv say "up to 5%". | next (Kyber 2027; MV-direct SST "toward 2029") | R6-016, R6-021, R6-023, R6-024, R6-020, R6-121 |
| Same, with a conventional transformer + rectifier | LV AC stages | ~97.3% grid-to-rack (vendor) | next | R6-025 |
| UPS Dynamic Online / ECO mode | double conversion in the normal path | 99% vs 97% | current | R6-004, R6-005 |
| **PV DC-coupled onto the DC bus** | inverter, 2 transformers, UPS, PSU | PV→12 V: 0.951 vs 0.891 on-site (**+6.8%**), vs 0.846 for remote PV over the grid (**+12.4%**). DERIVED, cross-tier. Buildings: 4–8% measured. | current (buildings); next (800 VDC data centres) | R6-012, R6-013, R6-014, R6-122 |
| DC-coupled PV + storage at a PV plant | inverter pass for clipped energy | recovers ~2% of PV energy, ~1% more value (model) | current | R6-015 |
| Single-stage 800 V→12 V next to the GPU | 54 V intermediate bus | >97%; 26% less board area | next | R6-019, R6-023 |
| 48 V→1 V at the die (vertical delivery) | 12 V intermediate stage, lateral delivery losses | 84% modelled vs <70% estimated today | speculative | R6-031, R6-032 |
| Solar-pumped laser | PV cell, DC-DC, laser driver, diode pump | sunlight→laser 4.64% measured vs ~12% via PV + fibre laser: **worse**. At a 1064 nm receiver: 2.4% vs 6.1%. | next (ground lab only; no flight found) | R6-060…066, R6-123, R6-124 |
| Computing on natural light (ACCEL, meta-imager, spectral CNN, passive incoherent diffractive network) | sensor ADC; camera→coherent-light re-encoding; 94% of digital operations | Task-specific, e.g. ACCEL 4.38 nJ vs 18.5 mJ per frame against an A100 (R3-053) | next | R6-080…084 |
| Spectrum splitting to several PV cells | thermalization in a single junction | >40% sunlight→electricity (concentrated light, NREL-confirmed) | current / next | R6-085 |
| Spectral-split PV + heat collector | nothing (it adds heat) | electrical 7.4–9.4%; ">70% overall" is mostly heat | current | R6-086 |
| Non-volatile weights (phase-change, BaTiO₃, MEMS, memristor ring) | continuous hold power → heat | hold 1.3–25 mW per π → 0; switching 0.15 pJ – 17 nJ (67 µJ for the Sb₂Se₃/ITO-heater case); break-even 0.1 µs – 40 ms | next (HZO: speculative) | R6-090…101, R6-125 |

## (d) Top 3 "keep it DC / keep it as light" opportunities, ranked by end-to-end gain

Ranking basis: fraction of the source power that reaches the 12 V compute bus. The 12 V→die regulator is identical in every chain compared, so it cancels. #1 includes the facility savings of #2.

1. **On-site PV (or any DC receiver: laser converter, rectenna, PV under a reflector) fed straight onto an 800 VDC bus. Gain +6.8% on-site, +12.4% against grid-delivered PV.** DERIVED (R6-122):
   - AC-coupled: 0.985 (inverter, R6-001) × 0.9953² (two transformers, R6-002) × 0.97 (UPS, R6-004) × 0.96 (PSU, R6-007) × 0.98 (12 V stage) = **0.8905**.
   - DC-coupled: 0.98 (MPPT DC-DC, R6-014) × 0.97 (800→12.5 V, R6-023) = **0.9506**. Ratio 1.068.
   - Remote PV: 0.8905 × 0.95 (transmission/distribution, R6-003) = 0.8459. Ratio 1.124.
   - Heat at the site falls from 11.0% (15.4% remote) to 4.9% of source power.

   Mismatch stated: the DC stages are next tier and the AC stages current tier. The measured building analog is 4–8% (R6-013). This matters for branches B and C: their ground receivers already output DC, so converting to AC first throws away 6–12%.
2. **A grid-fed DC-native facility. Gain +5.2%.** DERIVED (R6-121): the AC chain gives 0.9953 × 0.97 × 0.96 × 0.98 = 0.9083, and the DC chain gives 0.985 (SST, R6-024) × 0.97 (R6-023) = 0.9554. Ratio 1.052, and losses fall from 9.2% to 4.5%. The comparison is cross-tier. The tier-consistent measured version (380 VDC, current) is 5–7% (R6-009) and 10% (R6-011).
3. **Non-volatile optical weights: hold power goes to zero.** DERIVED break-even reprogramming interval t = E_switch / P_hold (R6-125):
   - 17 nJ (GST) / 1.66 mW (measured thermo-optic, R3-102) = 10 µs.
   - 67 µJ (Sb₂Se₃ with ITO heater, R3-012) / 1.66 mW = 40 ms.

   Weight-stationary inference holds weights for seconds to hours, far beyond break-even. For every 1,000 thermo-optic weights, 1.66 W of hold power is removed (1000 × 1.66 mW). **The system-level share is unknown** (see f). It is ranked below #1 and #2 only because that share has not been quantified.

Not ranked:
- Computing on natural light shows the largest per-task factor, but it applies only to vision front ends.
- Vertical 48 V→1 V delivery (<70% → 84%, ×1.2, PROJECTED, R6-031/032) would beat everything above. It is already DC-to-DC, though, so it is not a keep-DC or keep-as-light change.

## (e) Negative findings

1. **Solar-pumped lasers lose today.** Sunlight→laser is 4.64% measured against 0.35 × 0.90 × 0.38 = 12.0% for PV + DC-DC + fibre laser (R6-123; ground AM1.5 vs a space AM0 study assumption, mismatch stated). At a 1064 nm receiver the figures are 2.4% vs 6.1% (R6-124). JAXA's ">20%" (R6-067) has no stated basis and is not demonstrated.
2. **No solar-pumped laser has flown** as far as I found. JAXA lists only ground tests: 500 m in 2012–13, and a 200 m tower test at 350 W in 2016 (R6-070). JAXA's planned 1 kW laser test from the ISS JEM module (R6-068) has no evidence of flight. Its current light-source baseline is a 1070 nm fibre laser (R6-069).
3. The widely quoted 51.7 W/m² solar-laser "record" is a Zemax/LASCAD **simulation** (R6-065). Single-mode (TEM00) output is only 2.06% efficient (R6-064), a beam-quality penalty for beaming.
4. Laser power converters reach 50–69% only at 5–160 W/cm² (65–2,000× the 802 W/m² sunlight in R6-061). Reflected sunlight (branch C) can never use converter-class efficiency without concentrating the light. For 1.53 µm at 0.1 W/cm², one paper reports only harvested power, not efficiency (R6-047 notes).
5. **No measured system splits sunlight and sends one band to a photonic compute core.** The 2026-09-27 search returned only a Medium blog post. The handoff's §14 A/B/C endpoint should be treated as speculative.
6. Spectral PV-thermal ">70% overall" is mostly low-grade heat; the electrical share is 7.4–9.4% (R6-086). This confirms the handoff's §13 warning.
7. The industry's 800 VDC documents publish no measured efficiency. The NVIDIA 2026 white paper gives no number (R6-020). The Mt Diablo post gives none (R6-027). Google's "at least 30%" for 48 V has no stated basis (R6-028). ST's ">98%" is for an 800→50 V stage, not 800→12 V (R6-022). NVIDIA's own copper figures (85% vs 157% more power per conductor) are not reconciled (R6-017).
8. The size of the DC gain depends on the baseline. Against a "typical" 2008 AC chain it was 28% (R6-010). Against the best AC it is 5–7% measured (R6-009). Against today's Titanium chain it is ~5% (R6-121).
9. Multilevel phase-change weights are fragile in foundry devices:
   - 27 cycles × 7 levels, with the first two levels merging after 19 cycles (R6-095).
   - Contrast falls to half after ~500 cycles (R6-096).
   - 1,500 cycles on a >7-bit attenuator (R6-094).
   - 1.4e8 cycles, in a 2026 preprint (R3-013).

   Retention is 12 h for the memristor ring (R6-097). The HZO ferroelectric needs 120–210 V pulses (R6-100).

## (f) Failed sources and open questions

**ACCESS-FAILED (12 rows, R6-130…141):**
- OSTI 1482212 (AC vs 380 VDC) and OSTI 2345321 (meta-imager): timeouts. The meta-imager was recovered from the PMC author manuscript.
- OCP Diablo 400 spec and OCP LVDC white paper: 403.
- Navitas 800 VDC white paper: the URL returns a JavaScript page shell, not the PDF.
- Wiley (Helmers 2021) and MDPI Photonics ×3: 403. I used abstracts from the Semantic Scholar API, plus the Fraunhofer page and the Zenodo copy of the review.
- Optica journals: bot wall. I used PubMed abstracts.
- Taylor & Francis solar-laser review: 403.
- EUR-Lex 2019/424: challenge page.
- Medwin NOVA review: HTTP 522.
- Cell Rep Phys Sci 2024 "66.5% at 21 W/cm²": 403. Not used.

**Open questions:**
1. What is the measured grid→die efficiency of a GB300-class rack? The <70% (R6-031) is an estimate, and no public measurement was found.
2. No 800 VDC site has published a measurement yet (Kyber: 2027; the power rack enters production Q3 2026).
3. What do laser power converters achieve at the non-uniform, mW–W/cm² irradiance of a real space-to-ground beam, and at 1070 nm (JAXA's wavelength)? Only 1064 nm (50.6%) and 1319/1550 nm lab values were found.
4. How do solar-pumped lasers perform under AM0 in orbit, and what are their mass, thermal load and beam quality? No data found.
5. **What share of a photonic accelerator's power is weight-hold power?** This is needed to turn R6-125 into a system gain. Example: how many thermo-optic elements the 65-TOPS OPU of R3-102 has × 1.66 mW, against its total power.
6. Retention of non-volatile weights over months, and radiation tolerance (see R3-101 for GST).
7. Is any PV plant DC-coupled straight into an 800 VDC compute bus deployed anywhere? NVIDIA lists renewable interconnection only as future flexibility (R6-020).
