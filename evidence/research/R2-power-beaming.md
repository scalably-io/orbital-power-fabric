# R2: Power beaming, space PV, launch cost, exposure limits, orbit availability

Evidence ledger: `R2-power-beaming.csv` (128 rows: 119 claims + 9 ACCESS-FAILED). Retrieved 2026-09-27. Downloaded sources and their text extractions are in `evidence/sources/R2/`.

## (a) Verdict

1. **NASA's eight chain factors are confirmed verbatim** (OTPS 2024, Tables 6–7, the same for RD1 and RD2, at 1,367.5 W/m²). The handoff's 12.97%, 37.06% and 177.4 W/m² are correct arithmetic on them. However, they are study inputs, and NASA's cited source (Rodenbeck 2021) supports only 3 of the 8 values: 0.90 space DC-DC, 0.98 atmosphere and 0.78 rectenna.
2. **Every measured number falls well short of that chain.** MAPLE measured 3.4–3.7% DC-to-DC in orbit over 30 cm. PRAM-FX converted about 8% of sunlight to RF in orbit. JAXA's GaN array reached 35.1% DC-to-RF, against NASA's assumed 70%. The best end-to-end result ever recorded is 54% DC-to-DC, in a 1975 lab test.
3. **Caltech's own 2025 technoeconomic study gives 2.77% sunlight-to-grid today and 4.14% after 10 years of development** (24-hour average, GEO). That is 3–5× below NASA's 12.97%, although Caltech's figure includes sun-angle geometry and inverter losses that NASA's does not.
4. **Mass is the binding gap.** NASA's baseline implies about 910–940 W/kg for the whole system at PV output. Flown iROSA wings are 84.6 W/kg at beginning of life, large ROSA wings 71–98 W/kg, and flown missions cluster around 30 W/kg. At current flown hardware, the PV wings alone weigh about 32 t per delivered MW.
5. **No net space-to-ground power transfer has ever been demonstrated.** MAPLE's beam-to-Earth was detection only: about 20 dB above the noise floor, with roughly 1e-17 W predicted at the receiver. OHISAMA has not flown; its launcher has failed three times. Arachne has not flown. Aetherflux rebranded as Cowboy Space in May 2026 and pivoted toward orbital data centers.
6. **Launch.** Rideshare is $7,000/kg for 2026 launches with a 50 kg minimum ($350k), but **$7,500/kg ($375k) for 2027 launches**. Falcon 9 lists at $74M. Starship has not reached orbit; Flight 14, its first orbital attempt, is scheduled for 2026-09-28.
7. **Economics.** NASA's baseline LCOE is $0.61/kWh (RD1) and $1.59/kWh (RD2), and NASA states SBSP would not be competitive "even if access to space were free". Launch is 71–77% of cost.
8. **Beam densities in these designs exceed public exposure limits by 8–125×.** CASSIOPeiA peaks at 245 W/m², Caltech's 0.5 GW example at about 1.25 kW/m², and NASA's rectennas average 76–102 W/m². FCC and ICNIRP general-public limits are 10 W/m² whole-body, so rectenna sites must be exclusion zones.
9. **Geometry.** A dawn-dusk SSO is in eclipse about 2% of the year. But one LEO satellite sees a given site for at most about 12 minutes per overhead pass at 500 km (7.4 minutes above 10° elevation). MAPLE's measured pass was about 7 minutes.

## (b) Key model inputs

"...": elided table cells in a quote. Provenance classes as in the CSV `status` column.

| Parameter | Value | Class | claim_id |
|---|---|---|---|
| Solar constant (NASA) / measured TSI | 1,367.5 / 1,360.8 W/m² | STUDY-ASSUMED / MEASURED | R2-009, R2-119 |
| PV, space DC-DC, DC-RF, antenna, atmosphere, capture, rectenna, ground DC-DC (NASA) | 0.35, 0.90, 0.70, 0.90, 0.98, 0.95, 0.78, 0.90 | STUDY-ASSUMED | R2-001..008 |
| Sunlight-to-ground DC (NASA chain) | 12.97% | DERIVED | R2-010 |
| Rodenbeck Solar High WPT DC-DC (excludes PV) | 45.4% | STUDY-ASSUMED | R2-035 |
| Caltech 24-hour average sunlight-to-grid (current / 10-yr / 20-yr) | 2.77 / 4.14 / 6.63% | PROJECTED | R2-065 |
| Caltech DC-RF (current / middle / asymptotic) | 33 / 50 / 60% | PROJECTED | R2-066 |
| Best measured end-to-end DC-DC (1975 lab, 2.45 GHz) | 54.18% | MEASURED | R2-038 |
| MAPLE in-orbit DC-DC link (30 cm, 10 GHz) | 3.37–3.66% | MEASURED | R2-053 |
| PRAM-FX sunlight-to-RF module (orbit) | ~8% | MEASURED | R2-044 |
| GaN phased array DC-RF (JAXA 2015, ground) | 35.1% (PA 60.3%) | MEASURED | R2-042 |
| Rectenna RF-DC: array 2.45 GHz / array 5.8 GHz / best single element | >80% / 82% / 91.4% | MEASURED | R2-039, R2-041, R2-040 |
| Transmitter specific power, JAXA GaN array (RF out) | ~28 W/kg | DERIVED | R2-043 |
| Flown array specific power: iROSA wing BOL / large ROSA range / flown-mission cluster | 84.6 / 71–98 / ~30 W/kg | DERIVED / DERIVED / MEASURED | R2-093, R2-089 |
| Best space cells (BOL, AM0) | 32.2% (433 W/m²) | VENDOR-STATED | R2-091 |
| NASA implied whole-system specific power at PV DC | 909–938 W/kg | DERIVED | R2-018 |
| NASA in-space mass per delivered kW | 2.88 (RD1) / 4.95 (RD2 average) kg/kW | DERIVED | R2-019 |
| Caltech system average specific power (current / 10-yr) | 25 / 199 W/kg | PROJECTED | R2-067 |
| CASSIOPeiA mass per delivered kW | 1.43 kg/kW | DERIVED | R2-082 |
| NASA launch cost (baseline / sensitivity) | $1,000 ($850) / $500 ($425) per kg | STUDY-ASSUMED | R2-021 |
| Rideshare $/kg (2026 / 2027) and minimum mass | $7,000 / $7,500; 50 kg | VENDOR-STATED | R2-101, R2-102 |
| Falcon 9 list price | $74M | VENDOR-STATED | R2-103 |
| LCOE: NASA RD1/RD2; Caltech current/middle; Frazer-Nash for ESA (20% hurdle) | $0.61/$1.59 per kWh; 777.8/9.4 ¢/kWh; €106–206/MWh | STUDY-ASSUMED / PROJECTED | R2-023, R2-068, R2-080 |
| Exposure limit, 2–6 GHz: FCC public / FCC occupational / ICNIRP public whole-body / ICNIRP public local | 10 / 50 / 10 / 40 W/m² | FILING | R2-108..111 |
| SBSP beam-center design density (CASSIOPeiA / Caltech example) | 245 W/m² / ~1,250 W/m² | STUDY-ASSUMED | R2-084, R2-064 |
| Dawn-dusk SSO eclipse (season / annual fraction) | ~80 d, ≤18 min per orbit / ~2% | MEASURED / DERIVED | R2-113, R2-114 |
| Longest overhead pass at 500 / 1,000 km (elevation >10°) | 7.4 / 12.6 min | DERIVED | R2-117 |

## (c) HANDOFF CHECK

| Handoff claim | Verdict | Evidence |
|---|---|---|
| C004: NASA chain gives ~12.97% | **CONFIRMED** (arithmetic; NASA itself says "about 13%") | R2-010. Instantaneous, sun-normal; capacity factor applied separately. |
| C005: MAPLE transmitted detectable microwave power from LEO to Earth | **CONFIRMED**, with one qualifier | R2-052, R2-057. By Caltech's own definition this was "detection" (recovered power below what the receiver needs), not power transfer. Received signal about 20 dB above the noise floor. |
| C006: JAXA demonstrated retrodirective / pilot-signal beam control | **CONFIRMED** (ground only) | R2-045..047. 1.8 kW at 5.8 GHz over 55 m, 320–340 W DC received, 0.15° RMS pointing. No in-orbit JAXA result exists. |
| C011: SWELL about 1.5 W, about 11%, 1.45 m | **CONFIRMED** | R2-072, from an archive.org copy (the primary URL returns 403). |
| C019: rideshare $350k per 50 kg to SSO + $7k/kg | **CONFIRMED for 2026 launch-year pricing; CORRECTED for 2027 launches: $375k per 50 kg, $7.5k/kg** | R2-101, R2-102. The price does not depend on orbit. The handoff URL `new.spacex.com/rideshare` does not resolve. |
| PV 0.35 | **CONFIRMED** as NASA's input | R2-001. Attribution inconsistent: the table cites Rodenbeck, while Table 2 cites a NASA smallsat assessment. |
| Space DC-DC 0.90 | **CONFIRMED** | R2-002. Matches Rodenbeck. |
| DC-RF 0.70 | **CONFIRMED** as NASA's input; **UNVERIFIABLE** in its cited source | R2-003, R2-035. Not in Rodenbeck (75% / 82% there). Measured systems reach about 33–35%. |
| Antenna 0.90 | **CONFIRMED** as input; **UNVERIFIABLE** in its cited source | R2-004 |
| Atmosphere 0.98 | **CONFIRMED** | R2-005. Matches Rodenbeck. |
| Beam capture 0.95 | **CONFIRMED** as input | R2-006. Rodenbeck's GEO tables use 88% and 93%; 95% appears only for a 400 km optimized case (R2-037). |
| Rectenna 0.78 | **CONFIRMED** | R2-007. Matches Rodenbeck Solar High. |
| Ground DC-DC 0.90 | **CONFIRMED** as input | R2-008. Rodenbeck uses 95–97%. |
| 12.97% / 37.06% / 177.4 W/m² | **CONFIRMED** (arithmetic) | R2-010..012. At the measured TSI of 1,360.8 W/m², the last figure becomes 176.5 W/m². |
| Solar constant 1,367.5 W/m² | **CONFIRMED** as NASA's value | R2-009. About 0.5% above the measured TSI (R2-119). |
| "100–140 W/kg class" arrays | **CORRECTED** | Flown large ROSA wings are 71–98 W/kg at beginning of life; iROSA is 84.6 (R2-093). The flown-mission cluster is about 30 W/kg (R2-089). 115–130 W/kg is a next-generation design class (R2-095). Only the small OPAL wing reaches 124 W/kg. |
| "19–27 t PV per delivered MW" | **CORRECTED** | About 32 t/MW at iROSA's 84.6 W/kg, range 22–38 t (R2-097). About 90 t/MW at the 30 W/kg flown cluster. |

## (d) Negative findings and contradictions

- **NASA factor provenance.** NASA attributes all eight factors to Rodenbeck et al. 2021. That paper's link-budget tables (Tables 8–9, which are images) support only 0.90 (space DC-DC), 0.98 (atmosphere) and 0.78 (rectenna). The 0.35 PV value is attributed to two different sources within the same report (R2-001, R2-035).
- **Errors inside the NASA report.**
  - Combined-sensitivity LCOE for RD1 is 0.03 $/kWh in the executive summary but 0.04 in Table 3; emissions are 3.78 vs 3.87 gCO₂/kWh (R2-026).
  - The text says "1000 MT vs 585 MT"; the tables say 10,000 t vs 5,852 t, a factor-of-10 error (R2-032).
  - "2,3216 launches" is a typo for 2,321 (R2-022).
- **NASA assumes about 11× lighter hardware than anything flown** (R2-098). No flown array comes close to 900 W/kg at system level. Caltech's own 2025 estimate for today is 25 W/kg for the whole system (R2-067).
- **Caltech's own chain is lower than NASA's.** The 2022 design gives 7–14%, with NASA's figure at the top of that range (R2-061). The 2025 study gives 2.77–6.63% on a 24-hour average (R2-065). Caltech's asymptotic DC-RF (60%) is below NASA's 70%.
- **The MAPLE beam-to-Earth result is a detection, not power delivery.** EIRP was about 0.5–0.7 W (R2-056).
- **No in-orbit SBSP-to-ground demonstrator has flown as of 2026-09-27.**
  - OHISAMA is still planned; Kairos failed on 2024-03-13, 2024-12-18 and 2026-03-05 (R2-048, R2-050). Its reported specs drifted from about 180 kg / 400 km (2023 press) to about 150 kg / 450 km (2026).
  - AFRL Arachne is listed only as "2026" with no launch vehicle (Gunter's Space Page, secondary; not recorded in the CSV).
- **Aetherflux, the leading LEO laser-beaming startup, rebranded as Cowboy Space (May 2026) and moved toward on-orbit data centers** (R2-078). aetherflux.com now redirects to cowboyspace.com. It still says it plans a beaming demo satellite in 2026. This is a market signal against the thesis's premise.
- **Beam density vs exposure limits.** Every SBSP reference design puts beam-center or average density at 8–125× the FCC/ICNIRP general-public whole-body limit (R2-084, R2-064, R2-112 vs R2-108, R2-110).
- **Caltech 2022 misstates the FCC occupational averaging time**: it says 30 minutes; 47 CFR 1.1310 specifies 6 minutes (R2-109).
- **Falcon Heavy's price is no longer on SpaceX's Capabilities sheet**, which was created 2026-01-13 (R2-103). The "$97M" figure circulating in blogs is unverified; Caltech's Joule paper also uses $97M for "Falcon 9H" (R2-069).
- **Probable typo in the Caltech Joule paper**: the InP cell specific power is printed as "12,000 kW/kg" but is almost certainly W/kg (R2-071).
- **A 2026 perovskite review contradicts itself** on whether flexible perovskite has been characterized in orbit (R2-099).
- **Starship.** No orbital flight and no payload service yet. Flight 13's Starlink V3s re-entered about 20 minutes after deployment (R2-105). Every Starship $/kg figure is PROJECTED.

## (e) Failed sources

All are also recorded as CSV rows R2-120..R2-128 with status ACCESS-FAILED.

| Source | Failure | Workaround |
|---|---|---|
| NRL SWELL release | HTTP 403 | archive.org `id_` snapshot |
| ScienceDirect MAPLE paper | HTTP 403 | Author copy at chic.caltech.edu |
| Cell/Joule 2025 paper | HTTP 403 | Author PDF at its.caltech.edu |
| `new.spacex.com/rideshare` | DNS: CNAME with no A record | Public price-configuration GET used by rideshare.spacex.com, saved as JSON |
| ESA "Cost vs. benefits studies" page | HTTP 404 | Frazer-Nash primary PDF and press release; Roland Berger summary page |
| Roland Berger full report | Not public | Summary page only. The €8.1bn/€7.5bn figures appear only in secondary sources and are not recorded |
| Northrop Grumman UltraFlex pages | HTTP 404 | Only JPL's 2008 ST8 target (175 W/kg) recorded |
| NASA NSSDC Earth fact sheet | Connection refused | IERS TN36 constants used |
| SpaceX Capabilities PDF at `/media/` path | HTTP 404 | Found at `/assets/media/` |

## (f) Open questions

1. **ESA CM25 (November 2025) decision on SOLARIS.** Was a demonstrator phase funded? I found no primary source.
2. **Starship Flight 14 (NET 2026-09-28).** Did it reach orbit? When will non-SpaceX payload service and a real $/kg exist?
3. **Starlink array specific power.** SpaceX has not published W/kg or m² for V2-mini or V3 arrays. FCC technical attachments are the next place to look.
4. **Space-qualified DC-RF.** No flown GaN or CMOS phased array above about 35% DC-RF was found. We need a flight-qualified number, or a current lab record for GaN PAs at 5.8/10 GHz, from primary papers.
5. **Rectenna at SBSP-realistic density.** The >80% figures come at up to 1.7 kW/m² (Goldstone). What efficiency is demonstrated at 10–250 W/m², where exposure limits and design densities sit?
6. **Pass statistics for SSO over one mid-latitude site.** The CSV has only the geometric maximum and one measured pass. The model needs passes per day and their duration distribution from a propagated ephemeris.
7. **OHISAMA.** Will it launch on Kairos F5 in FY2026, and at what measured ground DC?
8. **The source of NASA's 0.70 DC-RF, 0.90 antenna and 0.35 PV values.** Possibly an Aerospace Corporation interim report, which is not public.
