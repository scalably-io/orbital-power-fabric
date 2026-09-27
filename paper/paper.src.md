# Move the energy, not the data centre?

## A falsifiable model of orbital energy for AI, and exactly what must change before space wins

*Pavle Lazić, ScalablyAI · report SR-2026-003 · {{version}} · {{date}} · model and code: Apache-2.0 · text, data and figures: CC BY 4.0 · test-chip design files: CERN-OHL-P-2.0 · repository: https://github.com/scalably-io/orbital-power-fabric · archived code and data: https://doi.org/{{doi}}*

---

## 1. Summary

**Question.** Should space first serve artificial intelligence as an energy layer, beaming power or reflecting sunlight to data centres on Earth, rather than as a compute layer with GPUs in orbit? The case for the energy layer is that GPUs depreciate in a few years while energy infrastructure could last decades, so one should launch only the long-lived part.

**Method.** We built an open model in which every input is a sourced claim with a verbatim quote, a numbered derivation with a test, or a labelled assumption. We fixed the metric and the verdict rules before computing any break-even. Independent reviewers with fresh context, who had not seen our reasoning, then tried to break the model; they were AI models, not human experts (section 3). Their reviews reversed several of our intermediate conclusions; the main reversals are in section 9 and all of them in `docs/NEGATIVE-FINDINGS.md`.

**Answer, with today's hardware and prices.**

1. **Microwave power beaming loses to GPUs in orbit on launched mass, from low orbit and from geostationary orbit, at every non-speculative tier.** The transmitter is the wall. The only measured transmitter specific power in our ledger, from a 2015 ground-test panel, is {{tx_wkg}} W of radio-frequency power per kg (R2-043). Beaming from low orbit needs at least {{need_tx_nasa}}–{{need_tx}} W/kg even if the solar array weighed nothing. From geostationary orbit, with NASA's study-assumed conversion chain and {{geo_gw}} GW delivered, it needs at least {{geo_tx_be}} W/kg ({{geo_tx_x}} times today); with today's arrays no transmitter is light enough.
2. **Orbital mirrors are lighter than GPUs in orbit only if two favourable conditions hold at once:** the areal density of a flown solar sail ({{c_next_gm2}} g/m², NASA's ACS3, R1-151) and a purpose-built receiving field that turns every watt of mirror light into electricity at full-sun efficiency. Aimed at a real tracking solar farm, which converts about {{site_conv_pct}}% of the light landing on its site (R5-077), sail-density mirrors are {{c_next_real}} kg per continuous kW over {{L}} years against {{a_lo15}}–{{a_hi15}}, and only a bare membrane with no deployer or bus is lighter. Reflect Orbital's filed Earendil-1 system, at its own filed life of about {{mirror_life}} year, is {{c_cur15}} kg per kW even onto the ideal receiver with no clouds, inside the range of GPUs in orbit. Any mirror fleet must also hold {{km2_lo}}–{{km2_hi}} km² of mirror over each receiving site at once before a ground inverter at a site in darkness produces anything.
3. **At today's launch price, the launch alone of GPUs in orbit, of microwave beaming and of sail-class mirrors costs more than ground solar with storage sized for {{hours_lo}}–{{hours_hi}}% of hours** (${{ter_lo}}–{{ter_hi}} per MWh of AI load); only speculative hardware passes on launch cost, and the last hours on the ground need backup we did not price. Of the options we compared, the ground is the best supported today: solar and storage built on site, with optics used for interconnect.
4. **Photonic matrix engines that stream weights cannot fix large-model inference, and our resident-weight photonic design fails with measured parts.** An engine that streams weights from high-bandwidth memory is capped at {{cap_lo}}–{{cap_hi}} times a B300 GPU in memory-bound decode even if its computation were free, depending on the memory's energy per bit. A resident-weight engine with direct photon-to-charge read-out beats a B300 by {{gate}} times only in an idealised case that cannot be built as specified. With measured parts and precision required on real outputs, its whole system may use at most {{lad_fp4_real}} times its optical-core energy at NVFP4 pairing, leaving the control, calibration, clocking and I/O electronics less than twice the core, and at FP8 pairing the core alone misses the gate. The architecture is not new; the negative result and its brackets are. Other photonic architectures are not ruled out by this analysis.

**What would change the verdict.** Table 9 lists {{n_problems}} quantities, each with today's sourced value and the value at which a conclusion flips. Every measured or derived number in the prose is filled in by code from the ledger or the model, and design choices such as layer size are set in the build script: `./scripts/reproduce.sh` and `python3 paper/build_paper.py` rebuild it.

![Launched mass per continuous kW of AI load](../figures/verdict_mass.svg)

*Figure 1. Launched kg per continuous kW of AI load over {{L}} years. Grey band: GPUs in orbit. Energy options receive ideal receiver spacing, no clouds, dawn-dusk sunlight and no storage. Mirrors are shown twice: onto an ideal receiver fully covered with PV, and onto a real tracking solar farm.*

## 2. Question and preregistered metric

The unit of comparison is one kilowatt of AI accelerator load (IT power, GB300 NVL72 class) running continuously for L = 10, 15 or 20 years. Four branches supply it:

- **A, GPUs in orbit.** The accelerator flies and is relaunched at the shorter of its refresh cadence and the vehicle life.
- **B, microwave beaming.** Orbital solar arrays feed a microwave transmitter; a ground rectenna feeds GPUs on Earth. Low orbit (B-LEO, {{alt_km}} km, {{mask}}° minimum elevation) and geostationary orbit (B-GEO).
- **C, orbital mirrors.** Mirrors reflect sunlight onto ground solar farms that feed GPUs on Earth.
- **T, the ground.** Solar and storage on Earth. The original handoff compared orbital energy only with orbital compute; any orbital option must also beat the ground.

**Primary metric:** lifecycle launched mass per continuous kW of AI load, counting every replacement as a whole spacecraft. Because the orbital-GPU baseline is a range, "lighter" means below its lower end, "heavier" means above its upper end, and anything between is inside the range. The verdict rules V1 to V4 and the metric were committed in `docs/PREREGISTRATION.md` before any break-even was computed; later changes are dated amendments.

**Tiers, and where they depart from our own rule.** The preregistration defines *current* as flown, qualified or buyable, *next* as best demonstrated and *speculative* as projected, and each B or C tier is compared with the same tier of A. The evidence does not fill every cell that way, so we state what each cell really is:

- A current is a vendor statement for a vehicle that has not flown (R1-005); A has no demonstrated next tier, so A next equals A current.
- B current combines flight and catalogue solar wings (median {{pv_flown}} W/kg, R2-093), a ground-tested transmitter (R2-043) and a conversion chain with two measured factors and five study assumptions. B next is a scenario: a catalogue wing and NASA's study-assumed chain, not demonstrated hardware.
- C current is a filing (Earendil-1, R1-112, R1-113). C next uses the density of a flown sail spacecraft, which is flown but is not a mirror. C speculative counts membrane and booms only.

**Choices that favour B and C.** No bus or structure mass for B; receivers spaced so that their visibility caps never overlap (an upper bound on coverage, D03); dawn-dusk sunlight; energy delivered to the receiver network counted as if it served one continuous load (D22); launched mass to geostationary orbit counted like mass to low orbit; no eclipse storage, rectenna exclusion zone or land for geostationary beaming; for mirrors, a receiving field fully covered with PV at its full-sun efficiency of {{ground_pv}}% (we also show a real solar farm), zenith atmosphere and full capture. Where B or C lose with these choices, they lose without them.

## 3. Method: an auditable evidence ledger

The ledger `evidence/claims.csv` holds {{n_claims}} claims ({{n_measured}} of them measurements) plus {{n_failed}} sources we could not access, kept so that nobody repeats the dead end. Each row carries a source URL, a locator (page, table or section), a verbatim quote of at most forty words, a retrieval date and a status: MEASURED, VENDOR-STATED, FILING, STUDY-ASSUMED, DERIVED or PROJECTED. We speak of them differently: a vendor statement is not a measurement, and a study assumption is not a demonstration.

Every formula in the model has a numbered derivation (D01–D22, appendix A) and a test that pins it; guard tests were mutation-checked by deleting the guarded code and confirming the test fails. When a quantity has no source, we either label the assumption (appendix B) or report the value at which the conclusion flips. Some model constants are code literals that carry their claim IDs in comments rather than being read from the ledger at run time.

**How this was made.** Scalably built this work with AI research agents (Anthropic's Claude) that searched primary sources and wrote ledger rows into separate files. Rows were merged only after an automated validator passed, with quotes spot-checked against the downloaded source text for each research batch, not every row (EXPERIMENTS E006…E029, E035). For a derived value the quote gives an input and the row's notes give the derivation. The model and this paper were then reviewed by AI models with fresh context (Anthropic's Claude Opus and OpenAI's Codex), not by human domain experts. We publish it so that people who build this hardware can check it.

To challenge a number, open an issue with the claim ID and a better source. The verdict, the tables and the prose regenerate from the ledger.

## 4. Results

The summary table compares the three energy branches with GPUs in orbit, tier by tier, over {{L}} years. Every B and C value uses the favourable choices listed in section 2.

*Table 1. Launched kg per continuous kW of AI load over {{L}} years, with no clouds.*

{{T_summary}}

### 4.1 GPUs in orbit

SpaceX states {{a_kwt}} kW per ton for its Starmind AI1 vehicle (R1-005, vendor-stated). The page does not say whether the numerator is average or peak power, which gives {{a_once_lo}}–{{a_once_hi}} kg per continuous kW per launch; if the ton is a short ton, the lower end is {{a_shortton}}. Starcloud's Starcloud-3 has been described as {{sc3_kg}} kg in a filing (R1-073) and, in press accounts, as a two-tonne, {{sc3_kw_lo}} kW or a three-tonne, {{sc3_kw_hi}} kW spacecraft with the power basis not given (R1-076); each description gives {{sc3_lo}}–{{sc3_hi}} kg per kW, consistent with that range. Satellite filings give a {{sat_life}}-year life (R1-023), so {{L}} years takes {{a_launches}} launches: {{a_lo15}}–{{a_hi15}} kg per kW. A filed target of {{a_spec_kwt}} kW per ton (R1-020, projected) sets the speculative tier at {{a_spec_lo}}–{{a_spec_hi}}.

### 4.2 Microwave beaming from low orbit

With perfect receiver coverage, beaming costs {{bleo_cur}} kg per kW over {{L}} years with today's parts and {{bleo_next}} with a catalogue array and NASA's study-assumed chain, against {{a_lo15}}–{{a_hi15}} for GPUs in orbit. Only NASA-implied whole-system hardware ({{bleo_spec}}) is lighter. With receivers only on land, the current tier rises to {{bleo_land_cur}}.

The transmitter decides it. At the measured {{tx_wkg}} W/kg (JAXA's 2015 ground-test GaN panel, R2-043; no space-qualified value was found, R2-042), the transmitter alone costs {{tx_only}} kg per kW per launch, {{tx_only15}} over {{L}} years, even with weightless solar arrays. The break-even transmitter is {{need_tx_nasa}}–{{need_tx}} W/kg ({{need_tx_x}} times today with the chain of today's parts). With today's arrays the arrays alone weigh {{pv_only}} kg per kW over {{L}} years, so no transmitter, however light, rescues current-tier beaming.

![Break-even for microwave beaming](../figures/breakeven_bleo.svg)

*Figure 2. Microwave beaming from low orbit beats GPUs in orbit only above and to the right of a curve. The measured transmitter ({{tx_wkg}} W/kg) and today's arrays ({{pv_flown}}–{{pv_cat}} W/kg) sit far below both curves.*

The solar array is the second wall. NASA's own space-solar study implies {{nasa_sys_lo}}–{{nasa_sys_hi}} W/kg for the whole system (R2-018), about {{nasa_x}} times the {{iorsa}} W/kg of the flown iROSA wing (R2-093). NASA concludes that its baseline is not cost-competitive even if access to space were free (R2-028).

A dawn-dusk orbit keeps the satellites in sunlight, but it also keeps them over the day-night line. An equatorial receiver lies within reach of a dawn-dusk orbital plane for only about {{site_share}}% of the day, in two windows around dawn and dusk (D22), and any single satellite passes overhead for minutes. The receiver network as a whole can take energy continuously, but a continuous load at any one site would need storage or a grid linking sites, which we do not count.

### 4.3 Microwave beaming from geostationary orbit

Geostationary orbit removes the visibility problem: one satellite sees one rectenna almost all the time. It does not remove the transmitter. A panel of given specific power cannot radiate more than that power times its own mass (D20), so a one-kilometre JAXA-class aperture, which already needs a {{rectenna_km2}} km² rectenna, can radiate at most {{geo_cap}} GW of radio-frequency power. Delivering {{geo_gw}} GW needs {{geo_rf_next}}–{{geo_rf_cur}} GW radiated, and the transmitter must grow with it.

*Table 2. Microwave beaming from geostationary orbit, transmitter sized by the power it radiates (D20).*

{{T_geo}}

GEO satellites are designed for a median {{geo_life}} years (R12-022); no power satellite has flown. Counting whole spacecraft, no service life lets current- or next-tier GEO beaming match GPUs in orbit within {{L}} years: a single launch ({{geo_once_next}}–{{geo_once_cur}} kg per kW) already exceeds their {{L}}-year total. Only the transmitter can change this (P1). The model is generous to GEO in several ways. It counts mass lifted to geostationary orbit like mass lifted to low orbit, although geostationary orbit takes far more launch energy. It delivers power through the eclipses around the equinoxes with no storage (D04). It keeps the one-kilometre receiving geometry, although a transmitter sized for {{geo_gw}} GW at the measured panel density would be about {{tx_diam_lo}}–{{tx_diam_hi}} km across. And it charges nothing for the rectenna site, although {{geo_gw}} GW on {{rectenna_km2}} km² averages about {{rect_wm2_lo}}–{{rect_wm2_hi}} W/m² of microwaves against a general-public exposure limit of {{pub_limit}} W/m² (R2-108), so the site would need an exclusion zone.

### 4.4 Orbital mirrors

A mirror in orbit reflects an image of the Sun, not a beam. At {{alt_km}} km the image covers about {{spot_km2}} km² at zenith (D05), so a single mirror adds almost nothing to the irradiance on the ground. Utility inverters start producing at {{start_lo}} W/m² with an ideal module and about {{start_hi}} W/m² at half efficiency in low light (R5-069). A receiving site in darkness therefore needs {{km2_lo}}–{{km2_hi}} km² of mirror overhead at once, about {{n_mirror_lo}}–{{n_mirror_hi}} Earendil-1-size mirrors, before any power flows. The mass figures below assume a fleet at that scale. Like beaming, a dawn-dusk mirror serves each site near its own dawn and dusk (D22), which suits extending existing solar farms but not a continuous load at one site.

The only sourced life for an orbital reflector is Earendil-1's filing: about one year of operations and a passive drag deorbit in about five months (R1-115, R1-116). We apply that {{mirror_life}}-year life to every tier, because lighter reflectors with more area per kilogram decay faster, and report the life each tier needs.

*Table 3. Orbital mirrors: kg per continuous kW over {{L}} years with weather, and what each tier needs to match GPUs in orbit.*

{{T_mirror}}

The filed Earendil-1 system ({{earendil_kg}} kg for {{earendil_m2}} m², R1-112, R1-113) is {{c_cur15}} kg per kW onto the ideal receiver with no clouds, inside the range of GPUs in orbit, and {{c_cur_wx}}, above the whole range, with the average cloud cover of solar regions; counting whole launches it would need a life of at least {{c_cur_be_life}} years. At the density of the flown ACS3 sail spacecraft ({{c_next_gm2}} g/m², R1-151) mirrors are lighter with ideal coverage and at least {{c_next_be_clear}} of the site cloud-free, but not with receivers only on land. ACS3 is a sail, not a mirror: its optical quality as a sunlight relay is undemonstrated. All of these figures assume a receiving field fully covered with PV. A real tracking solar farm holds {{farm_density}} MW of panels per km² at full sun (R5-077), so it turns only about {{site_conv_pct}}% of the light landing on its site into electricity; aimed at such a farm, even with no clouds, the filed system is {{c_cur_real}} kg per kW, the sail-density mirror {{c_next_real}} and the bare membrane {{c_spec_real}}. Mirrors that beat GPUs in orbit need a dedicated receiver built for them, whose area and cost this paper does not model. The weather factor is one minus the mean cloud amount, the expected share of a site in direct sun: {{clear_all}} over all hours and {{clear_night}} at night across {{n_regions}} utility-PV regions (R12-016), and about {{clear_global}} worldwide (R10-052). It ignores light passing through thin cloud and the loss when partial cover pushes part of a site below inverter start. Light pollution and debris risk from fleets of this size are outside the metric.

### 4.5 Cost against the ground

The terrestrial comparator is solar with batteries sized for flat output during {{hours_lo}}% and {{hours_hi}}% of hours in Las Vegas: ${{firm_lo}} and ${{firm_hi}} per MWh delivered (R5-027, R5-028, modelled with 2024 global prices). Per MWh of AI load that is ${{ter_lo}}–{{ter_hi}}. The last {{last_hours_share}}% of the year's energy costs about ${{last_hours_cost}} per MWh more than the {{hours_lo}}% case (R5-028), so full firmness is expensive on the ground too.

*Table 4. Launch cost alone per MWh of AI load (hardware excluded), and the launch price at which each option matches the ground.*

{{T_v3}}

At today's ${{launch_now}}/kg (R1-057, a study assumption), launch alone for GPUs in orbit costs ${{a3_now}} per MWh of AI load, and the break-even launch price is ${{a3_be_lo}}–{{a3_be_hi}}/kg with hardware free. At ${{launch_2035}}/kg, projected for the mid-2030s (R1-053), it falls to ${{a3_2035}}. If launch were bought at ${{launch_floor}}/kg, a Starship cost scenario with rapid reuse in Google's Suncatcher study (R1-056, a cost to the launcher, not a customer price), it would be ${{a3_floor}}. At today's price two of the speculative rows pass: NASA-implied geostationary hardware and mirrors of bare membrane and booms.

### 4.6 Sensitivity

Table 5 draws the uncertain inputs across stated ranges and reports the share of draws in which each option is lighter than GPUs in orbit. It is not a probability of success: the ranges span tiers and regions, their shapes are assumptions, and no transmitter above {{tx_wkg}} W/kg or array above {{pv_cat}} W/kg is sourced, so their upper ends are shown at several values.

*Table 5. Share of draws lighter than GPUs in orbit over {{L}} years.*

{{T_sweep}}

Low-orbit beaming is lighter in at most {{sw_bleo_max}} of draws under the five priors shown. Geostationary beaming moves from {{sw_geo_min}} to {{sw_geo_max}} as the allowed transmitter improves: its verdict is a statement about transmitter specific power. Mirrors range from {{sw_c_min}} to {{sw_c_max}}, before the site scale of section 4.4 is counted.

## 5. What the evidence supports today

**Energy for AI, on the ground.** Of the options we modelled, near-firm solar with storage on the ground is the cheapest per MWh (R5-027, R5-028). We did not compare it with grid power, gas, wind or nuclear, so we do not claim it is the best ground option. The binding constraint for new capacity is often time: the median utility project built in 2025 took {{grid_months}} months from interconnection request to operation (R5-042). Off-grid generation on site avoids that queue; a modelled off-grid microgrid meeting {{mg_share}}% of a data centre's load from solar costs ${{mg_cost}} per MWh (R5-029) and needs about {{land_km2_gw}} km² of land per GW of continuous load (R5-031). Coupling on-site PV directly to an 800 VDC rack bus is modelled to deliver {{dc_plus}}% more energy than AC coupling and {{dc_grid_plus}}% more than remote PV over the grid (R6-122, excluding battery round-trip losses); that rack architecture is expected in production in {{vdc_year}} (R6-016).

**Space is not yet the energy layer.** Beaming is transmitter-limited in both orbits, mirrors need sail-class hardware in fleets of hundreds per site, and at today's launch price only speculative hardware passes on launch cost. GPUs in orbit approach ground prices only when launch falls to a few hundred dollars per kilogram (Table 4).

**Photonics' proven energy win today is interconnect.** Photonic arithmetic exists (R3-042) but is not yet more efficient than GPUs at system level (section 6). Co-packaged optics move data at about {{cpo}} pJ/bit against {{plug_lo}}–{{plug_hi}} for pluggable transceivers (R9-030), at rack-to-cluster reach.

## 6. Photonic computing: where light wins and where it cannot

**The memory wall.** Generating one token with a large language model reads every weight once per batch step (D16). High-bandwidth memory costs {{hbm}} pJ/bit on a measured GH200, including the GPU's control logic (R3-078), and {{gpu_path}} pJ/bit through the GPU's caches (R9-005). A photonic engine that streams weights pays the same memory access, because light does not store weights. We bound its best case from above: a B300 draws at most {{tgp}} W (R3-067) while reading {{hbm_bw}} TB/s of memory (R1-100, R1-094), so in memory-bound decode at batch {{gpu_decode_note}} its whole board spends at most {{gpu_decode_fp8}} pJ per multiply-accumulate with {{w_fp8}}-bit weights. Even with a free compute core, the photonic engine is capped at {{cap_lo}}–{{cap_hi}} times the B300, depending on the memory energy assumed: {{T_caps}}.

*Table 6. Streamed-weight photonic engine (time-integrating read-out) against a B300 at its roofline, with the GH200 memory energy. Photonic support electronics are not included, so every ratio favours photonics.*

{{T_stream}}

**Support overhead.** The only measured full-stack photonic AI processor runs at {{lm_tops}} TOPS/W at system level, and its optical core draws {{core_share}}% of the system power (R3-043, R3-045). That core excludes the laser and the converters. Counted the way we count cores below, with its laser at the {{wallplug}}% wall-plug efficiency we assume for H1' (R8-072), its whole system uses about {{lm_like_lo}} times its core ({{lm_like_hi}} times if the laser's optical output is counted directly). It is a different architecture at a different precision, so it illustrates the size of support overhead in a real system; it does not bound H1'.

**Sunlight cannot replace the laser.** By the brightness theorem (D18) one spatial mode collects at most {{sun_nw}} nW of sunlight per THz of bandwidth at the telecom wavelength, whatever the collector. That supports far too few precise reads per second for a gigahertz engine; sunlight can feed only slow or massively multimode optics.

**Precision.** A b-bit analog read-out in this paper means fixed-point resolution with shot noise equal to one least-significant bit (D11, D21). That is closer to an INT format than to NVFP4 or FP8, which carry per-block exponents. We pair {{r_fp4}}-bit read-out with NVFP4 and {{r_fp8}}-bit read-out with FP8; whether either pair gives equal model accuracy is open problem P10, so "matched precision" below means these chosen pairings.

## 7. A testable hypothesis that fails: resident-weight photonic inference

**H1'.** Weights stay in place in non-volatile photonic cells (no hold power, no weight fetch). Each layer is square. Detectors integrate photocurrent directly onto a small capacitive node, with no amplifier (D12): the photon-to-charge conversion is the read-out. Detector-driven modulators pass activations between layers without converters, and the only data converters sit at the input of the first layer and the output of the last.

*Table 7. The idealised case: H1' optical-core energy per multiply-accumulate, {{layers}} layers, precision measured against full scale, a {{node_ideal}} fF node and {{loss_ideal}} dB loss, paired with B300 NVFP4 ({{b300_fp4}} fJ/MAC) and FP8 ({{b300_fp8}} fJ/MAC) at chip level (R3-070).*

{{T_h1}}

**The idealised case passes on paper but cannot be built as specified.** With photon-to-charge read-out, a {{h1_core_fp4}} fJ/MAC core at NVFP4 pairing lets the whole system use up to {{h1_sup_fp4}} times the core's energy before the {{gate}}-fold gain over B300 is lost, and {{h1_sup_fp8}} times at FP8. With a conventional receiver the allowance is at most {{h1_nep_max}} times the core at any size, which leaves almost nothing for the electronics around it. But a square single-wavelength layer shares its laser light across all outputs only as a lossless unitary (D13): meshes built from measured non-volatile elements lose tens to hundreds of dB (R8-126), and summing many waveguides incoherently onto one single-mode detector collects at most one of them (D13). A real layer would need one wavelength per input or accept those losses.

**Measured parts do not pass.** Table 8 changes one assumption at a time to a sourced value, cumulatively. At NVFP4 pairing three steps each take a large share: the measured-parts detector node (system allowance {{h1_sup_fp4}} to {{lad_node}} times the core), the O-E-O device's measured input energy of {{oeo_pd}} fJ per read (R7-046), which sets a floor on the light every output needs (to {{lad_oeo}} times), and precision over real outputs (to {{lad_prec}} times). At FP8 pairing precision dominates. Measured against the largest possible sum of {{n_layer}} terms, as in the idealised case, a typical output spans only a small part of full scale: about {{typ_lsb5}} of one least-significant bit at {{r_fp4}} bits, so it quantises to zero, and about {{typ_lsb8}} at {{r_fp8}} bits. Asking for the same bits over the real output distribution (D21, checked by a photon-counting simulation) makes the photons per multiply-accumulate independent of layer size, which at {{r_fp8}} bits multiplies the light needed many times over.

*Table 8. From the idealised case to measured parts, {{n_layer}} × {{n_layer}}, cumulative. Each row is one sourced change.*

{{T_ladder}}

**Verdict.** With today's measured components and our chosen precision pairings, resident-weight photonic inference does not reach a {{gate}}-fold energy gain over a B300. At NVFP4 pairing the whole system may use {{lad_fp4_real}} times the core's energy, so control, calibration, clocking and I/O get less than twice the core; the only full system measured, a different design, uses about {{lm_like_lo}} times its core counted the same way. At FP8 pairing its core alone is {{lad_fp8_core_real}} fJ/MAC, only {{lad_fp8_gain_real}} times below a B300 before any support electronics; with {{r_fp8_7}}-bit or {{r_fp8_6}}-bit read-out instead of {{r_fp8}}, the system allowance is {{fp8_7}} or {{fp8_6}} times the core. More than {{loss_be}} dB of optical loss leaves no allowance at all at NVFP4: the core alone would miss the gate. Not modelled, and each would lower the budget further: power to lock ring resonances (R8-103), static power at a stated clock rate, and splitting light to both arms of a balanced pair. The {{gate}}-fold gate is the gate we fixed in advance for claiming a large gain (docs/SYNTHESIS.md); the preregistered V4 test, full-system energy below a GB300-class GPU, remains open at both pairings because no full-system measurement exists.

**What would overturn it.** A measured resident-weight layer beating these budgets at the wall plug (P7, P8, P12), or a model evaluation showing that precision defined against full scale is enough for real networks (P10). The favourable definition is supported today only by simulations of small networks, at under one photon per multiply-accumulate (R12-030). Retention of non-volatile photonic weights is reported as test durations from {{ret_s}} seconds (R8-112) to {{ret_days}} days (R8-099); these are lower bounds, and some cells are extrapolated to years, and the best density we found is an upper bound of {{density}} weights per mm² for ring footprints against {{sram_density}} million for SRAM (R8-104, R8-084). At that density the layer sizes we tested hold {{h1_w_lo}}–{{h1_w_hi}} million weights on {{h1_cm2_lo}}–{{h1_cm2_hi}} cm², so even the idealised case concerns small fixed models, and the larger case spans several lithographic reticles.

**Prior art.** The architecture is not new. MIT's US11546077B2 (priority 2021) describes static weights that attenuate photocurrents without consuming power and charge summation, with photodetectors driving modulators for linear summation while converters remain between layers; US10268232B2 (2016) and the University of California's US11144821B2 (2017) cover other combinations, the latter in spiking form (R11-001…019). Built hardware stops at pairs or triples of these elements. What no one has published is the measurement that decides the question: the full-system wall-plug support overhead of such an engine.

### 7.1 The open test chip, OPF-MZI4

A 4×4 Clements mesh of Mach-Zehnder interferometers with titanium-nitride heaters on the CORNERSTONE 220 nm silicon-on-insulator process, assembled from unmodified cells of the MIT-licensed cspdk design kit. It measures grating-coupler loss, heater power per π phase shift, thermal crosstalk, unitary programming and the heater power needed to hold a matrix. It realises unitary matrices only and does not test H1'. Because a power-only measurement cannot certify the complex matrix, the test plan uses an intensity-only fidelity. The layout passes our connectivity check, but the foundry's design-rule check has not been run, because the rules are released only at sign-up. We do not fabricate it ourselves; `chip/TAPEOUT-GUIDE.md` gives routes, prices with claim IDs, the test setup and the measurement order for any lab that wants to.

## 8. Open problems for teams that can build

Each row is a quantity that changes a conclusion of this paper if it moves past the derived target. Rerun `python3 scripts/verdict.py` with the new value to see where the verdict flips. Identifiers such as E021 refer to entries in the repository's experiment log, `EXPERIMENTS.md`.

*Table 9. Open problems, generated by `scripts/open_problems.py`.*

{{T_open}}

## 9. Negative results, including our own errors

Negative results are deliverables. The full list, with evidence classes, is `docs/NEGATIVE-FINDINGS.md`. The most consequential:

- **The original handoff omitted the ground as a comparator.** Every orbital option must beat solar and storage on Earth, not only orbital compute.
- **Space-to-ground power beaming has so far been shown as detection, not usable power.** Caltech's MAPLE beam was detected on the roof of its campus (R2-052), up to {{maple_db}} dB above the ground station's noise floor (R2-057); its best in-orbit microwave transfer measured {{mapl}}% DC to DC over about {{maple_cm}} cm inside one spacecraft (R2-053). Caltech's own estimate of today's sunlight-to-grid efficiency from geostationary orbit is {{caltech_today}}% (R2-065), and NASA's baseline costs ${{nasa_kwh_lo}}–{{nasa_kwh_hi}} per kWh (R2-023).
- **Our geostationary "win" was a modelling error.** An earlier version of our verdict kept the transmitter at one kilometre for any power and showed next-tier beaming winning at {{geo_gw}} GW. Sized by the power it must radiate, a single launch already outweighs GPUs in orbit over {{L}} years (reviewer finding, E028).
- **We gave Reflect's mirror five years it does not have.** We had borrowed the life of data-centre satellites. The mirror's own filing states about one year, and at that life it is not lighter than GPUs in orbit (E028).
- **We counted GPU memory energy twice.** B300's energy per operation is its total board power divided by peak throughput, which already includes memory; we had added memory energy on top. The corrected bound is in section 6 (E028).
- **We used fractional spacecraft for break-even lives.** Counting whole launches, the filed mirror needs {{c_cur_be_life}} years, not less, and no life rescues geostationary beaming within the lifecycle (E033).
- **We let mirror light convert at full efficiency on every lit square metre.** A real solar farm covers only part of its land with panels; aimed at one, no mirror we could source is lighter than GPUs in orbit except a bare membrane (E034).
- **Our photonic hypothesis failed three times.** Time-integrating read-out needs a new weight every cycle, so it cannot combine with resident weights (E025). Our next design shared laser light across more inputs than outputs, which power conservation forbids in a single-wavelength network (E028). The design that survived both, H1', fails once built from measured parts (E031, E032; section 7).

## 10. Limitations, and the strongest case against our conclusions

**Limitations.** Cost comparisons count launch only; spacecraft hardware would widen every gap. The orbital-GPU baseline rests on vendor statements for vehicles that have not flown. The {{sat_life}}-year life of beaming satellites is borrowed from data-centre filings. Receiver coverage is an upper bound, the land-only case is an approximation, and continuous per-site supply is not modelled (D22). Mirror optics are assumed perfect. The photonic results are optical-core budgets at an assumed optical loss, precision equivalence is unshown, and resonance-locking and static power are not modelled. Laser power beaming is not modelled: the only in-orbit laser demonstration in our ledger delivered about {{swell_w}} W at about {{swell_eff}}% over {{swell_m}} m inside one payload (R2-072), which is not yet a space-to-ground data point. No human domain expert has reviewed this work yet.

**The strongest case against us.**

- *Launch will become cheap.* That changes the cost comparison, not the mass ranking. Current-tier microwave beaming matches the ground on launch cost only below ${{bleo_be_lo}}–{{bleo_be_hi}}/kg (Table 4), below the customer price projected in Google's Suncatcher study but within reach of that study's cost scenarios for heavily reused Starships (R1-056). Beaming remains heavier than GPUs in orbit at every non-speculative tier.
- *Transmitters will improve.* That is the one lever that matters for beaming, and we give its target: {{geo_tx_be}} W/kg for next-tier geostationary beaming (P1). No such space transmitter is in the ledger.
- *Mirrors are not meant to power a continuous load.* Their business case is extending existing solar farms into dawn and dusk, which is also where a dawn-dusk orbit serves each site (D22), and onto such farms they convert only a few percent of their light (section 4.4). Our metric follows the handoff's question, continuous AI load, and so does not value shifting energy in time. A fair test compares a mirror-delivered MWh at dawn with a battery-shifted MWh, and we leave it open.
- *GPUs in orbit are a moving target too.* The filed goal of {{a_spec_kwt}} kW per ton would lower A to {{a_spec_lo}}–{{a_spec_hi}} kg per kW, raising every bar in this paper.

## 11. Reproduce and contribute

```
git clone https://github.com/scalably-io/orbital-power-fabric && cd orbital-power-fabric
python3 -m pip install numpy scipy matplotlib pytest
./scripts/reproduce.sh          # validates the ledger, runs the tests, regenerates verdict, tables, figures and this paper
python3 paper/build_paper.py    # regenerates this paper; fails on any typed number or unknown citation
```

To change an assumption, edit it in `opf/scenarios.py` (each value carries its claim ID) and rerun. To correct a claim, open an issue with the claim ID, the better source, its locator and a verbatim quote. Code is Apache-2.0, text, data and figures are CC BY 4.0, and the chip design files are CERN-OHL-P-2.0.

## Appendix A. Derivations

Each derivation in `docs/DERIVATIONS.md` gives a statement, the derivation, its assumptions, the code that implements it and the test that pins it.

{{T_derivations}}

## Appendix B. Parameter registry

Values used by the model with their sources (`opf/params.py`). "Assumption" marks a value with no source, stated as such.

{{T_params}}
