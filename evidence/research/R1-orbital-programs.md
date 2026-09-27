# R1: Orbital compute programs (Branch A), passive reflectors (Branch C), reference AI load

Researcher: R1 · Retrieved: 2026-09-27 · Ledger: `R1-orbital-programs.csv` (154 claims, R1-001 to R1-154). Every quote was machine-checked against a local copy in `evidence/sources/R1/`. Treat everything here as a claim until the orchestrator merges it.

## (a) Verdict

1. Every handoff number in R1's scope checks out against its source. Two things are wrong. The C007 citation mixes up two different papers. The reflector model's clear-sky atmosphere factor of 0.85 is too optimistic: Çelik & McInnes use about 0.64 at zenith and about 0.13 at the ends of a pass (R1-136).
2. For the refresh argument, the key new source is SpaceX's own IPO prospectus (424B4, 2026-06-12). It books satellites at 3–5 years and servers at 5–6 years. It also says "the useful life of our satellites is inherently shorter than that of the information technology systems and infrastructure they host" (R1-034, R1-035). The SpaceX and Starcloud FCC filings both give a 5-year satellite life (R1-023, R1-079). Hyperscalers book servers at 5–6 years (R1-105 to R1-108). In other words, the orbital platform wears out about as fast as the GPUs it carries, or faster. That weakens the handoff's "GPUs depreciate faster than energy infrastructure" argument when applied to Branch A; it applies only to Branch B/C hardware that outlives 5 years.
3. AI1 thermal/power (VENDOR-STATED): 175 kW average compute, a 160 m² radiator and a 210 kW array at 250 W/m². Rejecting 175 kW from 160 m² needs a radiator at 322 K or more even under ideal assumptions: both sides radiating, sink at 0 K, no environmental loads (R1-014). That is 75 kW/t for the whole spacecraft (R1-005). A terrestrial GB300 NVL72 rack alone is about 90 kW/t (R1-104).
4. Reflector (DERIVED): an ideal Earendil-1 at zenith from 625 km delivers about 0.0166 W/m² into a 5.8 km spot (R1-123). Reflect's 2030 target of 50 W/m² would need about 3,000 such mirrors over one spot, or about 4,700 once atmosphere is included (R1-124). The company's roadmap has 5,000+ satellites in total by 2030 (R1-125).
5. No one has published measured free-flyer LEO radiation data on data-center GPUs or HBM. Google's Trillium numbers come from a ground proton beam: HBM irregularities at 2 krad(Si), no hard failure up to 15 krad(Si) (R1-047, R1-048). Starcloud-1 has no published telemetry, and SpaceX says in its prospectus that orbital AI compute is untested (R1-036).
6. Launch-price assumptions among orbital-compute proponents range from about $30/kg (Starcloud 2024, R1-083) to below $200/kg by about 2035 (Google, R1-053) to $500/kg as Starcloud-3's cost-parity point (R1-077). The model must sweep at least $15–3,600/kg.

## (b) Key model inputs

| Input | Value | Provenance | claim_id |
|---|---|---|---|
| AI1 compute, avg / peak | 175 / 250 kW | VENDOR-STATED | R1-004, R1-003 |
| AI1 specific power (whole vehicle) | 75 kW/ton (numerator undefined) | VENDOR-STATED | R1-005, R1-012 |
| AI1 radiator area | 160 m² (one- vs two-sided unstated) | VENDOR-STATED | R1-006 |
| AI1 solar array / areal power | 210 kW; 250 W/m² → ~840 m² | VENDOR-STATED / DERIVED | R1-007, R1-008, R1-013 |
| AI1 radiator temperature floor at 175 kW | ≥322 K (2-sided) / ≥383 K (1-sided) | DERIVED | R1-014 |
| SpaceX target specific power (early sats) | ~100 kW/t; 100 kW per satellite | PROJECTED (SEC filing) | R1-028, R1-029 |
| SpaceX ODC satellite life | 5 yr | FILING | R1-023 |
| SpaceX book lives: satellites / servers | 3–5 yr / 5–6 yr | FILING | R1-035 |
| First SpaceX AI-sat deployment | as early as 2028 | PROJECTED | R1-027 |
| Starship payload | 100 t (V3), 200 t (future) | PROJECTED | R1-030 |
| Starcloud-3 mass / arrays | 2,000 kg; 2 × (5.0 × 107 m, 535 kg) → 1.0 kg/m² | FILING / DERIVED | R1-073, R1-074, R1-075 |
| Starcloud-3 power | 100 kW (Dec 2025) or 200 kW (Mar 2026), basis unstated | VENDOR-STATED, Low | R1-076 |
| Suncatcher ISL need / demo | ~10 Tbps per link; 1.6 Tbps bench (MEASURED) | STUDY-ASSUMED / MEASURED | R1-042, R1-043 |
| Suncatcher formation | 81 sats, R = 1 km, 100–200 m spacing, 650 km | STUDY-ASSUMED | R1-040, R1-041 |
| TPU TID: HBM first irregularity / no hard fail | 2 krad(Si) / ≥15 krad(Si) | MEASURED (ground beam) | R1-047, R1-048 |
| Shielded LEO dose | ~150 rad(Si)/yr; 750 rad(Si)/5 yr | STUDY-ASSUMED | R1-049 |
| SDC / HBM UECC / SEFI rates | 1/17 rad; 1/44 rad; 1/450 (CPU), 1/400 (RAM) rad | MEASURED (ground) | R1-050, R1-051, R1-052 |
| Launch price today / break-even | $3,600/kg; <$200/kg by ~2035 | STUDY-ASSUMED / PROJECTED | R1-057, R1-053 |
| Launched power price (Starlink v2-type) | $14,700 → $810 /kW/yr | PROJECTED | R1-059 |
| Terrestrial power spend | $570–3,000 /kW/yr | STUDY-ASSUMED | R1-060 |
| GB300 NVL72 rack power / mass | 142 kW / ~1,580 kg | VENDOR-STATED | R1-095, R1-101 |
| GB300 NVL72 FP4 dense / FP8 sparse / HBM | 1,080 PF / 720 PF / 20 TB | VENDOR-STATED | R1-098, R1-099, R1-100 |
| Server useful life (MSFT/GOOGL/META/AMZN) | 2–6 / 6 / 5–5.5 / 5–6 yr | FILING | R1-105 to R1-108 |
| NVIDIA cadence | 1 architecture per year | FILING | R1-109 |
| Earendil-1 mass / mirror / orbit | 142 kg; 18 × 18 m; 625 ± 25 km, 88° | FILING | R1-112 to R1-114 |
| Earendil-1 life / deorbit | ~1 yr ops (2-yr license); ~5 months passive deorbit | FILING | R1-115, R1-116 |
| Sun angular diameter | 0.0093 rad (0.533°) | STUDY-ASSUMED | R1-134 |
| Atmospheric transmission, reflected light | ~0.64 zenith, ~0.13 pass ends, ≤0.70 | STUDY-ASSUMED | R1-136 |
| Reflector areal density | film 4–6 g/m²; structure 10–12 g/m²; ~140 kW/kg intercepted | STUDY-ASSUMED | R1-142, R1-140 |
| Reflector delivery window | ~16.5 min per visit per day (894 km SSO) | STUDY-ASSUMED | R1-144 |
| ACS3 flown membrane / system areal density | ≤4.25 g/m² quadrant; ~96 g/m² incl. booms+deployer | DERIVED | R1-149, R1-151 |

## (c) Handoff check

| Handoff claim | Verdict | Evidence |
|---|---|---|
| C001 AI1: 30 m, 75 m, 250 kW peak / 175 kW avg, 75 kW/ton | **CONFIRMED** | R1-001 to R1-005. The handoff URL `new.spacex.com` did not resolve on 2026-09-27; the same page is live at `www.spacex.com/spacexai/starmind`. The THERMAL and SOLAR tabs add a 160 m² radiator, a 210 kW array and 250 W/m² (R1-006 to R1-008). |
| 30 m / 75 m / 250 kW / 175 kW / 75 kW/ton | **CONFIRMED** (each) | R1-001, R1-002, R1-003, R1-004, R1-005. Caveat: the page never says which kW figure (or which ton) the 75 kW/ton refers to (R1-012). |
| C002 up to 1,000,000 sats at 500–2,000 km | **CONFIRMED** | R1-017, R1-018. Added from the filing: 30° and SSO inclinations; shells up to 50 km; ICFS SAT-LOA-20260108-00016; filed 2026-01-30; still pending. The technical attachment and Schedule S give **no** per-satellite mass, power, area or radiator figures. Schedule S gives a 5-year life (R1-023). |
| C003 Suncatcher names thermal, radiation and optical ISLs as major challenges | **CONFIRMED** | R1-061 (thermal is qualitative only), R1-046 to R1-052 (radiation), R1-042 to R1-044 (ISL). The 2026-09-24 page also changes the prototype plan: one TPU prototype on Transporter-18 "next week", then two satellites in 2027 (R1-038). The 2025 plan was two satellites by early 2027 (R1-037). |
| C007 ~0.53° gives a ~5.8 km image at 625 km | **CONFIRMED arithmetic; CORRECTED citation** | 625 km × 0.0093 rad = 5.81 km (R1-123, R1-134). The handoff pairs eprint 257425 with DOI 10.1016/j.actaastro.2022.03.015, but those are two papers. The eprint is Çelik & McInnes, *Adv. Space Res.* 69(1):647–663, doi 10.1016/j.asr.2021.10.033. The DOI is Çelik, Viale, Oderinwale, Sulbhewar & McInnes, *Acta Astronautica* 195:276–286 (open copy: eprints.gla.ac.uk/253463). Both were read (R1-134 to R1-146). Also note that 5.8 km is the zenith image from a point reflector; off zenith the spot stretches into an ellipse (Çelik Sec 2). |
| 0.53° | **CONFIRMED** | 0.0093 rad = 0.533° (R1-134) |
| C008 NASA ACS3 as the deployable-membrane precedent | **CONFIRMED** | 12U spacecraft, 80 m² sail, deployed in flight 2024-08-28 (R1-147, R1-152). Numbers the handoff lacked: 2.115 µm PEN film; ≤4.25 g/m² per quadrant including hardware; 164 g per 7 m boom; 7.7 kg sail-boom subsystem, about 96 g/m² at system level (R1-148 to R1-151). |
| C009 GB300 NVL72: 72 GPUs, up to 142 kW | **CONFIRMED** | R1-094, R1-095. Added: 36 CPUs, liquid cooled, FP4 1,080 PF dense, 20 TB HBM, ~1,580 kg (Lenovo OEM) (R1-097 to R1-101). |
| C010 142 kW × PUE 1.15 = 163.3 kW | **CONFIRMED** (arithmetic; PUE is an assumption) | R1-103 |
| Reflect Earendil-1 18 m × 18 m | **CONFIRMED** (FILING) | R1-113 (ODAR). Also 142 kg (R1-112); license granted 2026-07-09 under DA 26-706 (R1-114). |
| ~5 km ground footprint | **CONFIRMED as a third-party description** | AAS: "5-km-wide beam" (R1-122). Reflect's own FCC filings (as reviewed) never state a spot size. It is consistent with the derived 5.8 km (R1-123). |
| Reflector model: atmosphere 0.85 (Branch C power model, in scope) | **CORRECTED** | Çelik & McInnes (Hottel model): ~0.64 at zenith, ~0.13 at pass ends, never above 0.70 (R1-136). The full-capture yield falls from 313.8 to 236.3 W_e/m² of mirror, and the zenith mirror area for 163.3 kW rises from about 520 m² to about 691 m² (R1-154). The pass-averaged value is lower still (R1-137, R1-138). |

## (d) Negative findings and contradictions

1. **No per-satellite hardware data in the SpaceX ODC filing.** The Narrative, Technical Attachment, Schedule S and 3/16 opposition contain no mass, power, area or radiator figures. The only per-satellite spec sheet is the Starmind marketing page.
2. **SpaceX is internally inconsistent.** AI1 is listed at 75 kW/ton (R1-005). The FCC narrative and the 424B4 use about 100 kW/t (R1-020, R1-028). The prospectus says "early satellites generating 100 kilowatts", while AI1 is 175 kW average and 250 kW peak (R1-029). Peak compute (250 kW) is larger than the array (210 kW) (R1-015). On timing, Starmind says production starts "as soon as late 2027" and the prospectus says deployment "as early as 2028" (R1-010, R1-027).
3. **The AI1 radiator is tight.** At 175 kW it must run at 322 K or more under the idealized assumptions (R1-014). Starcloud's own 20 °C net-flux figure (633 W/m²) would reject only about 101 kW over 160 m² (R1-082 notes).
4. **Lifetimes do not support a refresh advantage for orbit.** SpaceX says satellites have shorter lives than the IT they host (R1-034). Every filing uses about 5-year satellite lives (R1-023, R1-079, R1-035), which roughly matches hyperscaler server lives of 5–6 years (R1-105 to R1-108). Amazon cut a subset from 6 to 5 years explicitly because of the pace of AI and ML (R1-108). NVIDIA ships a new architecture every year (R1-109).
5. **There is no in-orbit radiation data for data-center accelerators.** The Trillium results are from a ground proton beam on a single chip, irradiated through the heatsink (R1-046 to R1-052). Starcloud-1 has published no telemetry or error rates (R1-067). HPE SBC-1/2 flew inside the shielded ISS, not on free flyers, and not as GPU/HBM data-center tests (R1-110, R1-111).
6. **Starcloud numbers drift.** Starcloud-3 was "2-ton, 100-kW" in Dec 2025 and "three-tonne, 200-kW" in Mar 2026; the FCC DAS input is 2,000 kg (R1-073, R1-076). Starcloud-2 slipped from Oct 2026 to 2027 (R1-070). Applying the stated 100× ratio to Starcloud-2's 8 kW implies about 80 W of generation on Starcloud-1 (R1-072, Low confidence). The A6000 launch failure appears in one secondary source only (R1-068).
7. **Suncatcher's thermal section is qualitative.** The paper and blogs give no radiator area, temperature or kg/m² (R1-061). The ISL result is a bench demo (R1-043), and the 10 Tbps requirement is an analysis (R1-042).
8. **Reflect Orbital contradicts itself.** Its website says the light will not "harm eyes, even when viewed through a telescope". The FCC Order cites Reflect's own filing saying harm requires a telescope larger than 12 inches (R1-129). The website roadmap gives 36 satellites for 2027 in one layout and 38 in another (R1-125).
9. **The reflector scale check (DERIVED, first-order) is sobering.** An ideal 18 × 18 m mirror at 625 km delivers about 1.2×10⁻⁵ of full sun at zenith (R1-123). Reflect's 2030 target of 50 W/m² for 20 minutes needs about 3,000 such mirrors on one spot, or about 4,700 with the Çelik atmosphere. Its 2035 target of 300 W/m² needs about 18,000, or about 28,000 with atmosphere (R1-124), against a roadmap of 5k+ satellites by 2030 and 50k+ by 2035 (R1-125). Mirrors larger than Earendil-1 would change this, but Reflect has published no larger design.
10. **The FCC will not regulate reflector light.** The FCC ruled reflector operation outside its authority (R1-130) and imposed no NSF coordination condition. The AAS and IAU objections are on the record (R1-131 to R1-133). The regulatory path for a larger reflector constellation is therefore undefined, not cleared.
11. **FCC typo.** Public Notice DA 26-113 lists 18.3–19.3 GHz, but the application itself uses 18.8–19.3 GHz (Narrative p.6; Technical Attachment A.2). This is a TT&C detail with no model impact.
12. **Rack figures are incomplete.** NVIDIA does not state a dense FP8 figure for GB300 NVL72 (R1-099). The rack mass comes from an OEM (Lenovo) user guide, not from NVIDIA (R1-101).

## (e) Failed or degraded sources

| Source | Result | Workaround |
|---|---|---|
| `new.spacex.com/spacexai/starmind` | ACCESS-FAILED: DNS (Cloudflare CNAME, no A record) | Same path on `www.spacex.com`. The page is JS-only, so the text was captured with a headless browser (`spacex_starmind_rendered_2026-09-27.txt`). |
| peer.org copy of SpaceX Consolidated Opposition | HTTP 403 | Wayback snapshot 2026-04-03 (PDF, 32 pp.) |
| aas.org PDFs: SpaceX ODC petition, SpaceX ODC reply, Reflect petition to deny | ACCESS-FAILED: 403 Cloudflare; Wayback 404 | The AAS position was taken from the AAS press page (browser) and from DA 26-706 citations. The petitions' own numbers were **not** read. |
| compasse.aas.org, fcc.report | ACCESS-FAILED: 403 | none |
| ICFS pleading lists (Reflect docket: 1,888 entries; SpaceX docket) | ACCESS-FAILED: paginated JS app; an in-page API call hung for 30 min | **Not retrieved:** Reflect Consolidated Opposition (2026-03-24; the source of the 12-inch figure and likely spot/irradiance numbers), Reflect April 23 ex parte (Attachment B), and SpaceX filings after 3/16. Filing-document attachments were fetched directly from the ICFS attachment API. |
| ADA Space HKEX prospectus | not attempted within budget | Used China in Space (secondary), Medium confidence |
| ACS3 "900 g per boom" (search-engine summary) | not found in any NASA primary | Used NASA ISSS-2023 "164 g" instead (R1-150) |
| HPE SBC-2 SSD/PSU failure counts | not found in a primary source | not used |
| WebFetch AI summaries | not used as evidence | Every quote comes from a locally saved copy |

## (f) Open questions

1. AI1: vehicle mass, altitude, radiator temperature, and whether 160 m² is planform or radiating area. Also the array basis (BOL/EOL) and what the 75 kW/ton numerator is.
2. Do the SpaceX Gen3 Starlink filing (seen in search as SAT-LOA-20260630-00264, "Gen3_Technical_Attachment") or any later ODC amendment carry V3 bus mass and power? SpaceX says AI satellites reuse the V3 platform with about 5× its array output (R1-028). Not checked.
3. Did Suncatcher's prototype launch on Transporter-18, and what were its specs (Planet bus, TPU count, power)?
4. Reflect Orbital: the Consolidated Opposition (Mar 2026) and the Apr 23 ex parte likely contain the company's own irradiance, lux, spot size and eye-safety calculations. Has Earendil-1 launched? The application said NET 2026-04-24; the license was granted 2026-07-09.
5. Is there any free-flyer LEO SEE/TID data on HBM-bearing accelerators (the first Suncatcher prototype, Starcloud-1 telemetry)?
6. What is the basis of Starcloud-3's power figure (array vs compute), and what is its radiator area? The Sept 2026 FCC response gives the arrays only.
7. Power and mass of the Three-Body Computing Constellation satellites (ADA Space prospectus).
8. Not reviewed, but likely relevant: arXiv 2607.14172, "The Cost and Network Limits of Space-Based AI Compute" (2026), an independent analysis that could cross-check Branch A.
9. Reflector: what mirror reflectivity and specular quality should the model assume? Neither Reflect's filings nor Çelik give a flown value.
