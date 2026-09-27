# Derivations

Every formula in `opf/` is derived here from first principles or cited. Each entry: statement · derivation · assumptions · implementation · test that pins it. Symbols: R = Earth mean radius (6,371 km), h = altitude, r = R + h, e = elevation angle, λ = wavelength, e₀ = elementary charge. Constants are CODATA 2018 exact values where defined (`opf/constants.py`).

---

## Orbit and geometry

### D01 — Slant range at elevation e
**Statement.** d(e) = √(r² − R² cos² e) − R sin e.
**Derivation.** Triangle Earth-centre O, site S, satellite P. The angle at S between SO and SP is 90° + e. Law of cosines: r² = R² + d² − 2Rd cos(90° + e) = R² + d² + 2Rd sin e. Solve the quadratic in d and keep the positive root.
**Assumptions.** Spherical Earth, no refraction. **Code** `orbit.slant_range`. **Test** `test_slant_range_limits` (e = 90° → d = h; e = 0 → horizon distance √(r² − R²)).

### D02 — Visibility cap and time fraction
**Statement.** Earth central angle λ = arccos(R cos e_min / r) − e_min; fraction of Earth's surface seeing the satellite above e_min is f = (1 − cos λ)/2.
**Derivation.** In triangle OSP the nadir angle η satisfies sin η / R = sin(90° + e)/r, so sin η = R cos e / r. Angles sum to 180°: λ = 90° − e − η = arccos(R cos e / r) − e. A spherical cap of angular radius λ has area 2πR²(1 − cos λ); divide by 4πR².
**Assumptions.** Long-run time fraction = area fraction if the ground track covers the sphere uniformly (not true at latitudes above the orbit inclination). **Code** `orbit.central_angle`, `orbit.visible_fraction`. **Test** `test_visibility_and_eclipse` (≈0.48% at 625 km, 30° mask).

### D03 — Receiver fabric coverage
**Statement.** Random independent placement: P = 1 − (1 − f)^N. Disjoint caps (optimal spacing): P = min(1, N f).
**Derivation.** Random: each receiver independently fails to see the sub-satellite point with probability 1 − f. Disjoint: caps do not overlap, so the sub-satellite point lies in at most one; probabilities add.
**Assumptions.** Uniform sub-satellite point. The two are lower/upper bounds for a real, land-constrained network. **Code** `orbit.fabric_visibility(placement=…)`. **Test** `test_fabric_visibility_bounds`.

### D22 — Per-site service in a dawn-dusk orbit
**Statement.** An equatorial site lies within reach of a terminator-following (dawn-dusk) orbital plane for a fraction 4λ/360° of the day, λ the cap half-width of D02 (8.8% at 625 km, 30° mask). A single satellite is overhead only for minutes per pass; D03 covers how many are needed.
**Derivation.** A dawn-dusk orbit's ground track stays near the terminator. Earth's rotation carries a site through the band of half-width λ around the terminator twice a day (dawn and dusk), each crossing taking 2λ/360° of a day.
**Consequence.** Continuous delivered energy summed over a global receiver fabric (D03) is not continuous power at any one site: a continuous load at one site needs storage or a grid linking sites, which the model does not count (favourable to B and C). **Assumptions.** Equatorial site, ground track exactly on the terminator; higher latitudes see the terminator band for different durations through the year. **Code** `orbit.terminator_site_fraction`. **Test** `test_dawn_dusk_orbit_serves_one_site_a_small_share_of_the_day`.

### D04 — Eclipse fraction, circular orbit, beta angle β
**Statement.** f_ecl = (1/π) arccos(√(h² + 2Rh) / (r cos β)) for |β| < β* = arcsin(R/r); 0 otherwise.
**Derivation.** Sun direction ŝ = cos β â + sin β n̂, with â in the orbit plane. Position u(θ) = cos θ â + sin θ b̂. Distance to the Sun–Earth axis d² = r²(1 − cos² β cos² θ). Shadow (cylindrical) ⇔ u·ŝ < 0 and d < R ⇔ cos θ < 0 and |cos θ| > √(r² − R²)/(r cos β). That is an arc of total angle 2θ₀ around θ = π with cos θ₀ = √(r² − R²)/(r cos β); fraction θ₀/π. Note r² − R² = h² + 2Rh.
**Assumptions.** Cylindrical umbra (no penumbra), circular orbit. **Code** `orbit.eclipse_fraction`. **Tests** `test_visibility_and_eclipse` (GEO equinox ≈ 69–70 min/day) and `test_eclipse_formula_matches_geometry_by_sampling` (brute-force: 200,000 orbit samples, agreement < 1e-4).

### D05 — Image of the Sun after a flat mirror
**Statement.** Beam diameter at distance d: D = D_m + 2d tan(α/2), α = solar angular diameter.
**Derivation.** Each point of the solar disc arrives as a plane wave at a different angle within a cone of full angle α. A flat mirror preserves those angles, so every mirror point emits a cone of full angle α; the envelope at distance d is the mirror width plus 2d tan(α/2). This is an étendue (angular-source) limit, not a diffraction limit.
**Assumptions.** Perfectly flat mirror; real figure errors, jitter and atmosphere only enlarge it. **Code** `reflector.spot_diameter_m`. **Test** `test_overhead_mirror_spot_matches_handoff` (5.78 km at 625 km).

### D06 — Oblique ground footprint
**Statement.** A = (π/4) D² / sin e.
**Derivation.** A beam of circular cross-section D meeting a plane at angle e (between beam and plane) projects to an ellipse with minor axis D and major axis D / sin e.
**Assumptions.** Flat ground over the footprint. **Code** `reflector.footprint_area_m2`. **Test** `test_footprint_grows_as_elevation_falls` (×6.38 at 30°).

### D07 — Mirror tilt
**Statement.** Incidence i = ψ/2, where ψ is the angle between the Sun and target directions seen from the mirror; intercepted power ∝ A cos i.
**Derivation.** Law of reflection: the normal bisects the reversed incoming ray and the outgoing ray. The sunlight crossing the mirror equals the flux times the projected area A cos i.
**Code** `reflector.incidence_deg`, `reflector.optical_w_per_m2_mirror`. **Test** `test_mirror_tilt_dawn_dusk` (ψ = 90° → ×0.707).

### D08 — Airmass
**Statement.** τ(e) = τ_z^{1/sin e}.
**Derivation.** Beer–Lambert, plane-parallel atmosphere: slant path = vertical path / sin e.
**Assumptions.** Poor below ~10–15° elevation (Earth curvature, refraction). **Code** `reflector.transmission`. **Test** `test_airmass_transmission`.

## Beams and heat

### D09 — Diffraction and aperture-to-aperture collection
**Statement.** Airy first-null diameter 2.44 λL/D. Goubau parameter τ = √(A_t A_r)/(λL); optimally tapered collection η ≈ 1 − exp(−τ²).
**Derivation.** Far field of a uniform circular aperture ∝ 2J₁(x)/x, first zero at x = 3.832 ⇒ sin θ = 1.22 λ/D ⇒ diameter 2.44 λL/D (small angles). The Goubau relation is the standard result for power transfer between two apertures with optimal illumination. Cited: τ definition Brown 1970 NASA report (R12-023); closed form η = 1 − e^(−τ²) via Shinohara 2010, who calls it an approximation (R12-024); URSI 2007 gives 99.63% at τ = 2.4 vs 99.68% closed form (R12-025/026). Original Goubau/Brown papers paywalled.
**Code** `microwave.*`. **Tests** `test_diffraction_ledger_values`, `test_goubau_round_trip`, `test_geo_rectenna_scale`.

### D10 — Radiator floor
**Statement.** q = εσ(T⁴ − T_sink⁴) per radiating side; A = P/(n_sides q).
**Derivation.** Stefan–Boltzmann for a grey body exchanging with an effective sink.
**Assumptions.** A hard floor: view factors, gradients, Earth/albedo loads and structure only enlarge real radiators. **Code** `thermal.*`. **Tests** `test_radiator_and_photon_match_handoff`, `test_radiator_sink_reduces_flux`.

## Photonic computing energy

### D11 — Shot-noise photon floor for b-bit read-out
**Statement.** N_ph ≥ 4^b / QE; energy E = N_ph h c / λ.
**Derivation.** Photon counts are Poisson: mean N, standard deviation √N. Resolving 2^b levels needs σ ≤ full-scale / 2^b: √N / N ≤ 2^−b ⇒ N ≥ 4^b.
**Assumptions.** Ideal detector, no excess noise. The ±½ LSB convention changes this by a small constant factor (stated wherever used). 8-bit at 1,550 nm: 65,536 × 0.1282 aJ = 8.40 fJ. **Code** `limits.shot_noise_*`. **Test** `test_shot_noise_floor_values`.
**Precision meaning (2026-09-27, E028).** b bits here is FIXED-POINT resolution relative to full scale, like an INT-b ADC — not a floating-point format. Signed sums in a balanced (differential) pair: the difference spans −N_max…+N_max while noise is √(N₊ + N₋) ≤ √(2N_max), so 2N_max ≥ 4^b photons in total across both arms keeps σ ≤ full-scale/2^b; a nearly cancelling sum keeps that absolute error, so its RELATIVE error grows, exactly as for a small value in INT-b. Whether b-bit fixed-point analog outputs give a model the accuracy of NVFP4 or FP8 (which carry per-block exponents) is not shown by any claim in the ledger and is listed as an open problem (P10).

### D12 — Direct photon→charge read-out (no amplifier)
**Statement.** Photons to swing a node of capacitance C by V: N = CV/(e₀ QE).
**Derivation.** Q = CV; each absorbed photon releases at most one electron.
**Check.** kT/C noise at 1 fF, 300 K: √(k_B T / C) = 2.0 mV, below the 31 mV LSB of a 5-bit read-out on a 1 V swing; shot noise of 6,242 electrons is 1.3%, about 6.3 bits. So a 1 fF / 1 V node supports 5-bit read-out. 1 fF at 1 V costs 0.80 fJ optical at 1,550 nm (6.1× the 5-bit shot-noise floor). **Code** `limits.capacitive_detection_j`. **Test** `test_capacitive_detection`.

### D13 — Per-MAC energy of an N × N optical matrix engine
**Statement.** Per MAC: laser E_det 10^{L/10}/(η_wp N T) + DAC/N + modulator/N + (TIA + ADC)/(N T) + hold + SRAM + memory fetch.
**Derivation.** Per cycle: N² MACs, N input encodings and N output reads. Each output read needs E_det at the detector. The laser supplies N E_det through loss L at wall-plug η_wp, so laser per MAC = E_det 10^{L/10}/(η_wp N). Encoding is paid once per input and shared by N MACs. Read-out is paid once per output per T integrated cycles, shared by N T MACs.
**Correction (2026-09-27, E015).** With time integration the output is one dot product of length N·T, and the precision target (D11 / D12) applies to that integrated sum: signal and shot noise both add over the T cycles, so the photons required per READ are spread across T cycles. Laser per MAC is therefore E_det 10^{L/10}/(η_wp N T), not /N. (Photoelectric multiplication, Hamerly et al., PRX 2019: each detector integrates the time-encoded inputs into a full dot product, R12-029; stated quantum limit 50–100 zJ/MAC at N = 1000, R12-030.) E014 L2–L4b understated this lever; E015 re-runs them.
**Correction 2 (2026-09-27, E025, found by R8-129).** A length-(k·T) dot product means a DIFFERENT weight every cycle: time integration implies streamed weights, which cost (E_DAC + E_mod) per weight symbol shared over the inputs that reuse it (term `weights` = weight_j / weight_reuse). With weights resident (non-volatile), T must be 1 and accumulation must be spatial: fan-in k replaces N in the laser and read-out terms (laser / (η k), read-out / k). `Stack.issues()` flags T > 1 without streamed weights.
**Correction 3 (2026-09-27, E028, Opus review) — power conservation.** A passive single-wavelength network mapping k inputs to n < k outputs realises W, an n × k block of a unitary, so ‖Wx‖² ≤ ‖x‖² and, averaged over inputs, the fraction of light reaching the outputs is ‖W‖²_F / k ≤ n/k. Delivering E_det to each of n detectors therefore needs ≥ k·E_det of input light per cycle: laser per MAC ≥ E_det 10^{L/10}/(η_wp n T), i.e. amortised over min(n, k), not k. Summing k inputs incoherently into one single-mode detector is capped at 1/k by étendue (the D18 principle); a multimode detector escapes it only with capacitance growing with k, which breaks D12's 1 fF node. The full fan-in k is available only when the k inputs ride k distinct wavelengths (WDM), which a single-mode detector sums incoherently. Consequence: H1' is restated with square n = k layers (also the only chainable form). **Test** `test_laser_cannot_amortise_beyond_outputs_without_wdm`.
**Assumptions.** Square crossbar, full utilisation; digital control, nonlinearities, softmax, calibration and I/O are NOT included (in the only measured full system those dominated, R3-045). Every figure from this formula is therefore an OPTICAL-CORE budget, never a system energy; comparisons with GPU chip-level figures are stated as the support overhead the core can absorb. **Code** `limits.Stack`. **Tests** `test_stack_reproduces_r3_105_components` (R3-105 term by term), `test_time_integration_without_streamed_weights_is_flagged`, `test_spatial_fan_in_amortises_like_time_integration`.

### D14 — Thermo-optic weight hold energy per MAC is independent of N
**Statement.** E_hold/MAC ≈ (⟨φ⟩/π) P_π / f.
**Derivation.** Thermo-optic phase is linear in heater power, so P(φ) = (φ/π) P_π for φ ∈ [0, 2π). A Clements mesh has N(N − 1) internal/external phases (+N output phases), ≈ N², while a cycle performs N² MACs. The ratio is N-independent. For uniformly distributed phases ⟨φ⟩ = π ⇒ P_π / f: 20 mW / 10 GHz = 2 pJ/MAC. **Check** E012 measured (simulated Haar-random) 0.327 W over 16 heaters at 20 mW/π ⇒ ⟨φ⟩/π = 1.02. **Code** `mesh.heater_power_w`, `scripts/chip_predictions.py`.
**Two architectures, two means (E028, Codex review).** In a Clements mesh the phases of a Haar-random unitary spread over [0, 2π) ⇒ ⟨φ⟩ ≈ π (E012). In a crossbar where each weight is ONE amplitude MZI, transmission 1 → 0 needs φ ∈ [0, π]; uniformly distributed weights ⇒ ⟨φ⟩ = π/2 ⇒ E_hold/MAC = P_π/(2f) (R3-102 notes: 1.66 mW/π → 0.83 mW mean → 83 fJ/MAC at 10 GS/s). `scripts/efficiency_levers.py` models a crossbar, so it uses π/2.

### D19 — Streamed-weight energy per MAC
**Statement.** E_weights/MAC = (E_DAC + E_mod) / r, and E_fetch/MAC = b_w · E_bit / r, where r = number of input vectors that reuse each streamed weight symbol (batch or broadcast).
**Derivation.** With time integration (T > 1) a detector sums a length-(k·T) dot product, so each cycle needs a new weight at every cell (D13 correction 2). A streamed weight must be fetched (b_w bits at E_bit each) and encoded onto light (one DAC conversion and one modulator drive). That weight symbol takes part in exactly one MAC per input vector that shares it in the same cycle; with r such vectors the cost is split r ways. Resident (non-volatile) weights pay neither term, but then T = 1 (D13).
**Assumptions.** One modulator per weight symbol; reuse limited to the batch/broadcast actually present (decode batch 64; prefill 2,048 tokens in E025). **Code** `limits.Stack` (`weight_j`, `weight_reuse`, `fetch_j_per_mac`), `Stack.issues()`. **Test** `test_time_integration_without_streamed_weights_is_flagged`.

### D21 — Photons for b bits over the output distribution (balanced incoherent read-out)
**Statement.** With inputs x ∈ U[0,1] carried as p·x photons per unit and weights w ∈ U[−1,1] realised as transmissions on the + or − arm of a balanced detector pair, holding shot noise to one LSB of b bits spanning ±4σ_y needs p ≥ 9·4^b/256. Photons reaching the weight elements per MAC = p·E[x] = 9·4^b/512 (18 at 5 bits, 1,152 at 8 bits), independent of the fan-in k; photons detected per output = 9k·4^b/1024.
**Derivation.** y = Σ w_i x_i over k terms has mean 0 and σ_y² = k E[w²] E[x²] = k/9. Detected counts n₊ ~ Poisson(p Σ_{w>0} w x), n₋ ~ Poisson(p Σ_{w<0} |w| x); ŷ = (n₊ − n₋)/p has noise variance Σ|w|x / p ≈ k E|w| E[x] / p = k/(4p). One LSB of b bits over ±4σ_y is 8σ_y/2^b. Requiring √(k/(4p)) ≤ 8√k/(3·2^b) gives p ≥ 9·4^b/256. The light delivered to the elements is p Σ x = pk/2 per output, i.e. p/2 per MAC.
**Why it matters.** D11/D13 measure b bits against the largest possible k-term sum (full scale ∝ k), whereas a typical output is σ_y/FS ≈ 1/(3√k) of full scale — about 0.17 LSB at 5 bits and k = 1,024, so typical outputs quantise to zero. That definition is what lets the laser term fall as 1/k (D13); over the real output distribution the photons per MAC are independent of k. The favourable definition is supported only where a network tolerates the noise, which Hamerly et al. show by simulation for MNIST-scale networks (R12-030). Both are reported as brackets; model accuracy decides (P10).
**Assumptions.** Uniform, independent inputs and zero-mean weights; ideal detectors; each weight on one arm (a passive split of every input to both arms doubles the delivered light). Any node or device that needs E_min per read raises the delivered light per MAC to at least 2·E_min/k. **Code** `limits.dist_photons_per_mac`, `scripts/efficiency_v2.py::ladder`. **Test** `test_dist_precision_photons_by_monte_carlo` (Poisson simulation reproduces noise = 1 LSB within 5%).

### D15 — Clements mesh
**Statement.** N columns, MZIs on pairs (m, m+1), m = c mod 2, c mod 2 + 2, … ⇒ N(N − 1)/2 MZIs. MZI: T = B(r₂) diag(e^{iθ}, 1) B(r₁) diag(e^{iφ}, 1), B(r) = [[√r, i√(1−r)], [i√(1−r), √r]].
**Derivation (count).** N even: N/2 even columns of N/2 MZIs and N/2 odd columns of N/2 − 1: N²/4 + N(N − 2)/4 = N(N − 1)/2. The arrangement is universal with N(N − 1)/2 beam splitters and depth N (Clements et al., Optica 3, 1460 (2016); R12-027/028).
**Code** `mesh.layout`, `mesh.mzi`, `mesh.unitary`. **Tests** `test_layout_counts_match_clements`, `test_mesh_programs_random_unitaries`, `test_chip_layout_bottom_heaters_still_universal`.

### D16 — Transformer decode operator counts
**Statement.** Per token, per layer: q, o projections d²; k, v projections d·d_kv; attention scores and AV each h·d_h·T; SwiGLU MLP 3dI; plus LM head d·V. Weight bytes per token = params × bytes / batch; KV bytes per token = 2 L d_kv T bytes.
**Derivation.** Direct count of multiply-accumulates in each matrix product of a decoder-only transformer with grouped-query attention.
**Code** `transformer.*`. **Tests** `tests/test_transformer.py` (short-context MACs/token = non-embedding params + LM head within 1%).
**Correction (2026-09-27, E028, Codex review).** With untied embeddings the input embedding is a lookup: each token reads one row (d weights), not the table. Weight bytes per token = (params − V·d) × bytes / batch + d × bytes. For Qwen2.5-72B at 8-bit, batch 1, v1 overcounted 1.246 GB/token (1.7%). **Test** `test_untied_embedding_reads_one_row_per_token`.

## Lifecycle mass

### D17 — Launched mass per continuous kW of AI load
**Statement.** A: (1000 / k) · L / min(R_gpu, S). B: 1000 · PUE · m_W / (η_postPV δ_link δ_sun) · L/S, with m_W = (1/w_pv + 1/w_tx)(1 + s). C: 1000 · PUE · ρ_A / (q_mirror η_pv c δ_link δ_sun) · L/S.
**Form used by the verdict (2026-09-27, E033, Codex paper review).** `opf/scenarios.py` states the transmitter by its RF output, so m_W = 1/w_pv + η_dcdc·η_DC-RF / w_tx,RF (w_tx,RF in W of RF out per kg; η_dcdc = 0.90, R2-002) with s = 0 (favourable), and every L/S factor is the whole-launch count ⌈L/S⌉. The generic `lifecycle.PowerBeaming` keeps 1/w_tx with w_tx per W of DC in. The break-even service life is the shortest S with m·⌈L/S⌉ ≤ budget, i.e. L / ⌊budget/m⌋, and none exists when one launch exceeds the budget (`lifecycle.min_service_life`, test `test_min_service_life_counts_whole_launches`).
**Derivation.** Average delivered power per unit orbital hardware is the product of chain efficiency and duty factors; mass per delivered watt is its inverse times specific mass; replacements over the lifecycle are L / service life (continuous approximation).
**Code** `lifecycle.*`. **Test** `test_lifecycle_replacement_logic`.
**Correction (2026-09-27, E028, Codex review).** The preregistered metric counts every replacement, and a spacecraft is launched whole: launches over L = ⌈L / S⌉ (L = 10/15/20 y; S = 5 y → 2/3/4; S = 15 y → 1/1/2). The continuous form L/S is kept only as a stated approximation. With equal 5-year lives, A/B-LEO/C ratios are identical at every L; only B-GEO (S = 15 y) changes. **Code** `lifecycle.launches`. **Test** `test_whole_launches`.

### D20 — GEO transmitter mass: power-limited or aperture-limited, whichever is larger
**Statement.** m_tx = max(ρ_A · πD²/4, P_RF / w_tx), with P_RF = P_delivered / (η_postPV / (η_dcdc η_DC-RF)).
**Derivation.** A transmitter panel of specific power w_tx (W of RF out per kg) and areal density ρ_A radiates at most w_tx ρ_A per m². Beam capture fixes a minimum aperture πD²/4 (D09); the RF power fixes a minimum mass P_RF / w_tx. The mass is the larger of the two. At JAXA's measured panel (ρ_A = 44.7 kg/m², w_tx = 28 W/kg, R2-043) a 1 km aperture radiates at most 0.98 GW RF, while 10 GW delivered through the next-tier chain needs 17.0 GW RF, so power sets the mass (E028; the v1 model used the aperture alone and understated it 3.3×).
**Assumptions.** Power density across the aperture limited only by the panel's specific power (no thermal limit beyond it); PV, bus and structure as in D17; rectenna not launched. **Code** `scenarios.geo_rf_w`, `scenarios.b_geo_kg_per_kw`. **Test** `test_geo_transmitter_is_sized_by_power_not_only_aperture` (mutation-checked: aperture-only → FAIL).

## Light sources

### D18 — Brightness theorem: sunlight power per spatial mode
**Statement.** A single spatial mode filled by a blackbody at temperature T collects at most P = p · n̄ · hν · Δν, with n̄ = 1/(e^{hν/k_B T} − 1) and p = 2 polarisations.
**Derivation.** Thermal radiation has n̄ photons per mode (Bose–Einstein). The mode density per unit bandwidth is one per polarisation per spatial mode, so power per mode is n̄ hν per unit bandwidth per polarisation. Passive optics conserve radiance (étendue), so no lens or concentrator can raise the photon occupancy of a mode above the source's n̄. A single-mode collector sees the full solar radiance whenever its field of view (~λ²/A) is smaller than the solar disc (aperture ≳ λ/θ_sun ≈ 0.17 mm at 1,550 nm).
**Numbers.** Sun ≈ 5,772 K, 1,550 nm: hν = 0.80 eV, k_B T = 0.497 eV, n̄ = 0.250; 1 THz band, both polarisations → 64 nW per mode.
**Consequence.** Per-output power ≈ P after loss (each output gathers N inputs each split N ways) → 5-bit reads at ≤ 10⁶–10⁷ /s even with a 1 fF photon→charge node (E018). Sunlight can drive only slow, massively multimode (incoherent) optics.
**Code** `limits.thermal_occupancy`, `limits.thermal_mode_power_w`. **Test** `test_sunlight_per_mode_brightness_bound`.
