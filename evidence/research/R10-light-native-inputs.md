# R10 — Light-native inputs: computing on light before it is detected

Researcher R10. Retrieved 2026-09-27. Ledger: `R10-light-native-inputs.csv`, 86 rows: 83 claims and 3 ACCESS-FAILED. `scripts/validate_evidence.py` rejected none.

Before the CSV was written, `evidence/sources/R10/_build_r10.py` checked every quote against the downloaded source text (Unicode and whitespace normalised). Sources and scratch files are in `evidence/sources/R10/`. R3 and R6 rows (ACCEL, spectral CNN, meta-imager, passive diffractive network) are cited by ID, not duplicated.

## (a) Verdict

1. **Computing on incoherent scene light before detection works, but only at small scale.** The best measured optical encoder reduces an image to 2–4 detector values (196:1 to 800:1).
   - It beats linear encoders: 79% against 69.5% optical and 74% digital (QuickDraw, 196:1).
   - Its optics transmit only 2.9% of the light, and no energy per inference is reported (R10-001…005).
2. **Only one optical pre-detection processor for Earth observation has flown.** BUPT-spectra01 (launched November 2024) is a coded-aperture snapshot hyperspectral camera.
   - It puts 47 bands on one frame, so it reads out 47× less data. It weighs 1.5 kg.
   - In orbit it reached 80.5% ground-cover classification (R10-068…070).
   - Every "optical AI in orbit" project I found digitises the image first and re-encodes it on a laser (R10-071…073).
3. **Earth observation is limited by the downlink first.**
   - About 67% of scenes are cloudy (R10-052).
   - A bent pipe gets less than 21% of cloud-free Landsat-8 data to the ground (R10-053).
4. **Once triage moves on board, compute energy, time and heat become the limit.**
   - Φ-Sat-1 used only 3 of its 10 bands because of memory and power (R10-061).
   - A cloud filter deployed directly on board took 98 s per frame against a 22 s deadline (R10-054).
   - Computing used 30–40% of a 12U satellite's energy (R10-064).
5. **Derived (DERIVED): electronic triage trades energy for link capacity; optical triage saves only the energy.**
   - The flown Myriad-2 cloud CNN costs 1.4–7.7× more energy per tile than the radio energy it saves (R10-083).
   - Optical triage before detection sends the same 43.8 Mbit per 100 tiles as electronic triage (−67% against a bent pipe). For image products that is no extra downlink saving (R10-084).
   - It cuts on-board energy about 4–9× (1.3–12.6 J against 11.5–51 J per 100 tiles), but only under strong assumptions (R10-085).
6. **Physics rules out waveguide meshes for scene light.**
   - A sunlit, perfectly white scene gives at most 0.17 pW per mode per THz at 550 nm, about 4.7×10⁵ photons/s (DERIVED, R10-079).
   - One 8-bit read from a single-mode input therefore takes about 14 ms per 10 THz of bandwidth.
   - Only free-space, multimode, non-negative optics feeding large-area detectors fit (R10-080, R10-081).
7. **H2 survives in a narrower form.** "Compute on the light to remove the on-board triage bottleneck and skip readouts" survives. "Downlink less than on-board electronics" does not.

## (b) Approaches

| Approach | Input light (incoherence / étendue handling) | Conversions removed | Measured accuracy and energy | Tier | claim_ids |
|---|---|---|---|---|---|
| Multilayer nonlinear ONN encoder (Wang 2023) | Incoherent broadband; LED-lit DMD emulates the scene. Non-negative LCD intensity weights; free-space multimode path | Detector reads and ADCs 196–800× fewer; most digital layers | 79% vs 69.5% (linear optical) and 74% (linear digital) at 196:1; 93% vs 88.5% at 400:1. Transmission 2.9%. **No energy reported**; nonlinearity is a powered image intensifier | next | R10-001…006 |
| Meta-optic / diffractive encoders feeding a full sensor (Wirth-Singh 2025, Huang 2024, Chang 2018) | Incoherent (µLED/OLED), or laser scrambled by diffusers. Non-negative point-spread functions; "pseudo-negative" via channel pairs | Digital MACs only (85.8k vs 17M; 12% of FLOPs). **Readouts unchanged** | 93.4% vs 98.4% (MNIST); 44.4% vs 51.9% (grayscale CIFAR-10). Advantage only at ≤8×8 readouts. Energy only PROJECTED (17 µJ → 85 nJ) | next | R10-011…019 |
| Angle-sensitive pixels (ASP Vision) | Incoherent scene through a lens. Grating response gives a differential intensity filter; loses light (QE down to 10%) | First conv layer; about 90% of ADC events and bits (10:1) | Within 0.1–5.6 pp of baselines (simulated). Sensor 1.8 mW total, ADCs 100 µW (measured) | next | R10-007…010 |
| ACCEL, spectral CNN, meta-imager, passive diffractive network (from R3/R6) | Incoherent or partially coherent; ACCEL needs a reduced aperture to raise coherence | ADC removed in ACCEL's path; 94% of operations moved into optics | ACCEL 4.38 nJ/frame vs 18.5 mJ on A100 (batch 1); 85% on 100 flashlight samples | next | R3-051…053, R6-080…084 |
| Few-photon sensing (PANS, 2026) | Incoherent OLED structured illumination; single-photon detectors | Detections reduced to a few photons per inference | 86% on MNIST with 8.6 detected photons | next | R10-022 |
| In-sensor electronic compute (SCAMP-5, compressive CIS, WSe₂ sensor network) | Incoherent camera light (SCAMP-5, CIS); laser + SLM (WSe₂) | Per-pixel ADC and off-chip transfer; 4× fewer conversions before the ADC | 96.9% MNIST at 0.7 mJ/frame; 51 pJ/pixel with 4× compression; 20 Mbins/s on 3×3 pixels | current / next / speculative | R10-023…028 |
| Optical random projection (LightOn OPU) | **Coherent** 532 nm laser; data re-encoded by a DMD | None: adds DMD → light → camera | VENDOR 1500 TOPS at 30 W (not reproducible, R10-030). MEASURED 45 J/batch; GPU uses more energy above D = 18,000, >10× at D = 58,000 | current (product) | R10-029…033 |
| Fourier 4f amplitude-only CNN (Miscuglio 2020) | **Coherent** HeNe laser | None for light-native input | 2 MP at 10 kHz; 98% MNIST, 54% CIFAR-10. **No energy** | next | R10-034 |
| **Coded-aperture snapshot spectral imager, flown (BUPT-spectra01)** | Incoherent sunlight; reflective mask + prism code intensity (non-negative); multimode focal plane | 46 of 47 readouts vs a full-cube capture (47× less data) | 80.5% in-orbit K-means ground cover (no full-cube baseline); 1.535 kg; **no power figure** | **current** | R10-068…070 |
| Laser/MZI "optical AI in orbit" (TU Berlin concept) | **Coherent** laser; image digitised first | None | 84.5% (4×4 hardware), 93.3% vs 96.6% (MNIST subset). Energy "neglected" | speculative | R10-071…073 |
| Diffractive spectral object detection for EO (simulation) | Simulated | — | 91.56% / 84.27% (simulated) | speculative | R10-074 |
| *Baseline:* electronic on-board AI (Φ-Sat-1, Myriad 2) | Detect first | Downlink bits (−67% via cloud triage) | 95.1% tile accuracy, 0.8% false positives; ~102 ms per tile at ~1 W nominal | current | R10-058…063 |

**How incoherence and étendue are handled across these approaches**
- Every approach that works on real scene light uses **intensity-domain, non-negative weights**. Signed weights need paired channels and differential readout.
- All of them are **free-space and multimode**.
- A passive lossless network combining N mutually incoherent modes into one single-mode port keeps at most 1/N of the power (unitarity, R10-081). Incoherent summation must therefore land on a detector with ≥ N modes of étendue.
- The coherent systems (OPU, 4f, MZI) only work after the scene has been detected and re-emitted by a laser.

## (c) Earth observation: is the downlink or on-board energy the binding constraint?

**Instruments produce data faster than links can carry it.**
- Sentinel-2's MSI generates 1.3 Gbit/s raw, compressed to 450 Mbit/s, against a 560 Mbit/s X-band link (R10-036, R10-037). That is 1.5 TB/day per satellite (R10-038; the same page also says 1.6 TB per orbit, a contradiction, R10-039).
- A Planet Dove moves 12–15 GB per 7–10-minute pass (R10-043).
- Kodan's Landsat-8 simulation: a bent pipe downlinks less than 21% of observable cloud-free data. Perfect on-board cloud filtering would deliver 3× more (R10-053).
- For comparison outside EO: the MMS science mission downlinks about 4% of what it generates (R10-056).
- About 67% of the planet is cloud-covered at any time (R10-052).

**Radio energy per bit is not what binds.**
- Downlink energy is 29.9 nJ/bit (Planet HSD2) to 80 nJ/bit (XLink-X), i.e. 0.36–0.96 µJ per 12-bit sample (DERIVED, R10-045, R10-048).
- That is below Sentinel-2's whole-instrument detection cost of 1.57–2.46 µJ per sample (DERIVED, R10-042).
- The binding quantity is link *capacity* (contact minutes × rate).
- At 2020 AWS prices, contact time costs $4.7–18 per GB (DERIVED, R10-051). The current AWS page publishes no prices (R10-050).

**Once triage moves on board, energy, time and heat bind.**
- Φ-Sat-1 ran CloudScout on 3 of 10 bands "for two main reasons: memory constraints… and power limits derived from the satellite power budget". Reducing the bands in flight "was deemed prohibitive due to the necessary power" (R10-061).
- Its platform stores about 46 Wh, and the HyperScout-2 imager draws 6 W while processing (R10-062, R10-063).
- In Kodan, a directly deployed cloud filter needed 98 s against a 22 s frame deadline. It gained 9% instead of 3× (R10-054). About 15 W is taken as the practical ceiling for a 3U compute subsystem (R10-055).
- On BUPT-1 (12U), measured in orbit:
  - computing used 30–40% of the satellite's energy;
  - about 9 W for 10 h overheated the payload;
  - battery depth of discharge exceeded 30%, even 50% (R10-064…066).

**Answer.** For missions whose product is the raw image, downlink capacity binds first. The fix is on-board triage, and that makes compute energy, time and heat the second limit. On small satellites, the second limit decides how much of the first can be removed. H2 optics target this second limit.

## (d) Worked example (DERIVED): tile-level cloud triage, 100 tiles

**Setup.**
- Tile: Φ-Sat-1 CloudScout input, 192×192×3 = 110,592 samples (R10-059), at 12 bit/sample (Sentinel-2 quantisation, R10-040). That is 1.327 Mbit per tile.
- Cloudy fraction: 0.67 (R10-052).

**Per-tile energy terms.**
- On-board CNN: 1–2 W × 0.102 s = **0.10–0.20 J** (R10-082).
- Radio: 1.327 Mbit × 29.9–80 nJ/bit = **0.040–0.106 J** (R10-083).
- Readout, per sample:
  - E_r = 51 pJ for a best-case IoT CMOS sensor with 4× analog compression (R10-025).
  - E_r = 1.57–2.46 µJ for the Sentinel-2 MSI whole-instrument average (R10-042, an upper bound).

| Scenario | Downlinked bits (100 tiles) | On-board energy (100 tiles) | Formula |
|---|---|---|---|
| A. Bent pipe | 132.7 Mbit | 4.0–37.8 J | 100·N·E_r + 100·E_radio |
| B. Detect → Myriad-2 CNN → send clear tiles (flown today) | **43.8 Mbit (−67%)** | **11.5–51 J** | 100·N·E_r + 100·E_cnn + 33·E_radio |
| C. Passive optical encoder decides before detection, gated readout, send clear tiles | **43.8 Mbit (−67%)** | **1.3–12.6 J** | 100·K·E_r + 33·N·E_r + 33·E_radio, with K = N/196 = 564 |

**Reading the table**
- **Bits: C = B.** When the downlinked product is the image, optical preprocessing adds no downlink saving over electronic triage. It saves bits only when the product is the decision or latent vector. Then it sends K = 564 values per tile, or fewer.
- **Energy: C/B ≈ 0.11–0.25.** The saving comes almost entirely from removing the CNN. Skipping cloudy readouts also matters when E_r is flight-instrument-sized.
- **Electronic triage loses energy.** It spends 1.4–7.7× the radio energy it saves (R10-083). It pays off only because link capacity binds. Optical triage makes the same decision close to energy-free, so it could run on every frame. That removes Kodan's 98 s vs 22 s bottleneck.
- **Link use: triage fits ~3× more cloud-free tiles into each pass.** A pass carries 72,000–90,000 raw tiles; with only cloud-free tiles sent, about 3× more useful ones get down (R10-086). Electronic and optical triage give the same gain.

**Assumptions that could flip C (unverified; the parts not yet measured).**
1. A passive optical encoder at 196:1 reaches CloudScout-grade decisions (95% tiles, <1% false positives). This has not been shown on EO imagery.
2. The imaging sensor supports readout gated per tile. Push-broom sensors may not.
3. The digital back end and the light split between the encoder and imaging branches are ignored.
4. Myriad 2 is a 2016-class chip. A current edge accelerator (vendor-stated 0.5 pJ/op, R10-057) could shrink E_cnn a lot. I could not quantify this because CloudScout's op count is not reported.

## (e) Negative findings

- **No light-native optical front end reports measured energy per inference on real scene light.**
  - Wang 2023 reports none.
  - The meta-optic encoders report MAC counts only.
  - ASP gives sensor power without frame rate.
  - Miscuglio's 4f system reports no energy.
  - BUPT-spectra01 gives no payload power (R10-001, R10-015, R10-007, R10-034, R10-069).
- **PSF-engineering encoders do not remove conversions.** "The power and latency required to capture an image and convert it to digital input is the same regardless of the network" (R10-016).
- **Optics' accuracy advantage appears only at very small readout sizes.** Above 8×8 values, hybrid and digital accuracies are identical (R10-011). A single optical conv layer gives no energy advantage unless the input is very large (R10-013).
- **Generic compression favours plain lenses.** In the low-noise regime typical of daylight EO, lens imaging plus binning beats engineered point-spread functions at equal compression (simulation, R10-017).
- **Optical encoders cost photons.** Wang's encoder has 2.9% transmission and "cannot support low-light operation" (R10-005); ASP pixels drop to 10% relative QE (R10-010).
- **The LightOn OPU figure is not reproducible.** 1500 "TeraOPS" does not follow from its stated dimensions (3.8×10¹⁵ MAC/s implied; R10-030). The OPU is laser-driven and adds conversions (R10-032).
- **No incoherent-optics EO processing has flown except coded-aperture spectral imaging.** The in-orbit optical-AI effort found (TU Berlin) digitises, then re-encodes on a laser, and neglects energy (R10-071…073).
- **Sentinel-2 figures on the same eoPortal page disagree.** 1.5 TB/day vs 1.6 TB/orbit; MSI power 170 W vs <266 W (R10-038…040).
- **Wideband incoherent processing needs a very large number of diffractive features.** Universal incoherent intensity transforms need N ≥ ~2·Ni·No features, about 1.2×10⁸ for one EO tile at 196:1 (simulation, R10-021).
- **LiDAR:** one search found only post-detection electronic processing. No optical pre-detection LiDAR compute was found (not searched further; out of time budget).

## (f) Failed sources and open questions

**Failed or partial access**
- DOE-4f ship recognition, Signal Processing 2024: ScienceDirect 403, no Crossref abstract (R10-075).
- Dove high-speed-downlink SmallSat 2017 paper: Cloudflare/403. The eoPortal reproduction was used (R10-076).
- AWS Ground Station pricing: no prices on the live page (R10-050). The Feb 2020 NASA ESTO deck was used.
- CEAS Space J. 2026 full text (Springer redirect): abstract via Crossref only.
- MDPI Remote Sensing 17:3381: access denied; abstract via Crossref.
- Optica full text of Miscuglio 2020: blocked; arXiv used.
- NASA Sun fact sheet: connection timed out; IAU 2015 B3 used instead.
- Park 2021 JSSC: abstract via WebFetch only (saved in `webfetch-yonsei-park2021-abstract.txt`).
- Colburn 2019 (Appl. Opt.): not read; only cited through Huang 2024.

**Open questions (decision-relevant)**
1. Can a passive, incoherent optical encoder reach flight-grade cloud or ship triage (≥95% tile accuracy, <1% false positives) on real multispectral EO tiles? What is its measured end-to-end energy? This is the gate-2 evidence gap for H2.
2. What does a modern radiation-tolerant accelerator spend in J per CloudScout-class tile? If it is ≪0.1 J, the energy case for optical triage (R10-085) shrinks.
3. Do EO focal planes support readout gated per tile (row or region skipping) at acceptable complexity? Without it, C saves only the CNN.
4. Where does BUPT-spectra01 reconstruct its data (orbit or ground), what does the payload draw, and what is the accuracy against a full-cube baseline on the same scene?
5. What is the photon-budget margin of a 2.9%-transmission encoder for a push-broom dwell of about 1 ms at 10–50 m GSD? It needs the pixel dwell time and aperture of a specific mission; not derived here.
