# R12: citation gaps (cloud, land fraction, GEO life, three formulas, solar disc)

Retrieved 2026-09-27. 33 rows in `R12-citation-gaps.csv`; `scripts/validate_evidence.py` (report mode) rejects none. Sources and the two scripts that recompute the derived rows are in `evidence/sources/R12/` (`build_r12_csv.py`, `ucs_geo_comms_life.py`).

## 1. Cloud cover and clear-sky fraction (C_reflector)

- **Global mean cloud fraction: 67 %** (MODIS cloud mask; King et al. 2013), so the global clear fraction is 0.33. **Over land: 55 %. Over ocean: 72 %.** Claims R12-001 to R12-003, MEASURED.
- **Utility-PV regions:** annual cloud amount comes from CERES SYN1deg via the NASA POWER 2001–2020 climatology, read at 12 representative 1° cells (R12-004 to R12-015). The clear-sky probability is 1 − CF (R12-016, DERIVED):

| region (cell) | cloud % all-hours | clear all / day / night |
|---|---|---|
| Mojave (35.0, −115.5) | 31.1 | 0.69 / 0.71 / 0.67 |
| central Arizona (33.4, −112.6) | 32.1 | 0.68 / 0.72 / 0.63 |
| Atacama (−23.0, −69.5) | 26.3 | 0.74 / 0.85 / 0.62 |
| inland Dubai (24.75, 55.4) | 33.8 | 0.66 / 0.72 / 0.60 |
| central Saudi (24.5, 46.0) | 22.8 | 0.77 / 0.82 / 0.72 |
| Ouarzazate (31.0, −6.9) | 40.2 | 0.60 / 0.62 / 0.57 |
| Aswan (24.5, 32.7) | 16.0 | 0.84 / 0.88 / 0.80 |
| Riverina NSW (−34.6, 146.0) | 40.8 | 0.59 / 0.57 / 0.61 |
| Alice Springs (−23.7, 133.9) | 31.5 | 0.69 / 0.71 / 0.66 |
| W Rajasthan (27.5, 71.9) | 24.7 | 0.75 / 0.80 / 0.69 |
| S Karnataka (14.1, 77.3) | 50.4 | 0.50 / 0.52 / 0.47 |
| Qinghai (36.1, 100.4) | 56.4 | 0.44 / 0.45 / 0.43 |
| **mean of 12** | | **0.66 / 0.70 / 0.62** |

- **Instrument check:** ground sunshine recorders in the same US-SW area give **Phoenix 85 %** and **Las Vegas 84 %** of possible sunshine (NOAA CCD, 1965–1983; R12-017 and R12-018). Over the same cells, the satellite daytime clear fraction is 0.71–0.72. The satellite mask also counts thin cirrus and sub-cell cloud, so treat the POWER values as a **conservative lower bound** for a direct-beam mirror link. For US-SW daytime, the bracket is about 0.71–0.85.
- **Caveats:** the regional mean gives each region equal weight; it is not weighted by PV capacity. The query points are representative locations, not plant coordinates. Night clear fraction is lower than day almost everywhere, which matters for night and twilight mirror delivery. The CERES SYN1deg quality summary warns that the product is not climate-quality for trends; that does not affect using it as a climatology.

## 2. Earth's land fraction (X_common)

- **29.1 %** of Earth's surface is land at present (USGS Professional Paper 1386-A, Fig. 9); R12-019, MEASURED. This replaces `LAND = 0.29 # ASSUMPTION` in `scripts/verdict.py`, which becomes 0.291. The figure includes ice-covered land, so land usable for receivers is smaller.

## 3. GEO comsat design life (B_rf_power)

- **15 years, "often exceeding 15 years"**: Airbus Eurostar Neo brochure (2025); R12-020, VENDOR-STATED.
- **"lifetime over 15 years"** for Spacebus Neo and Eurostar Neo: ESA Neosat page; R12-021.
- **Median 15 years** across 426 GEO communications satellites with a numeric expected lifetime in the UCS Satellite Database (data to 2023-05-01). 72 % of them list exactly 15 years; the mean is 14.35 years. R12-022, DERIVED.
- **Caveat:** these are stated design lives, not observed service lives.

## 4. Formulas

**(a) Goubau / Brown** (B_rf_power)
- **τ = √(A_t A_r)/(λD):** W. C. Brown, NASA-CR-103090 (Raytheon PT-2931, 1970), Fig. 3-17, which credits the curve to Goubau 1970. R12-023.
- **η = 1 − e^(−τ²), with τ² = A_tA_r/(λD)²:** Shinohara 2010, Eqs. (2)–(3), citing Brown 1992. R12-024.
- **URSI 2007:** η → 100 % for τ > 2 with Gaussian tapers, and 99.63 % at τ = 2.4 (R12-025, R12-026). At τ = 2.4 the closed form gives 99.68 %, within 0.05 percentage points of the curve value.
- **Caveats:**
  - Brown's primary report shows τ and an efficiency curve, not the closed form. The closed form comes from a secondary source, and that paper itself calls it "approximation".
  - I did not read the original Goubau 1970 or Brown & Eves 1992 papers; both are paywalled.

**(b) Clements et al.** (D_ground_photonic)
- **N(N−1)/2 beam splitters** give a universal N×N interferometer (R12-027).
- **Each beam splitter is one MZI, and the mesh has optical depth N** (Reck: 2N−3) (R12-028).
- **Source:** quotes are from arXiv v2. Crossref confirms the publication as Optica 3(12):1460, 2016-12-06. The Optica full text was bot-blocked. R4-154 already covers this result but has no count quote.

**(c) Hamerly et al., PRX 9, 021032 (2019)** (D_ground_photonic)
- **Photoelectric multiplication:** inputs are time-encoded, and each homodyne detector integrates Q_i ∝ Σ_j A_ij x_j (R12-029).
- **SQL:** 0.5–1 aJ per MAC (5–10 photons) at N = 100, and 50–100 zJ per MAC (0.5–1 photon) at N = 1000 (R12-030).
- **Photons per detector N·n_mac ≫ 1** (R12-031). This is the paper's own support for the E015 time-integration correction.
- **Status:** all three rows are STUDY-ASSUMED because the bound is simulated and network-dependent. R12-030 overlaps R8-001 and R7-007.

## 5. Solar angular diameter (C_reflector)

- **1919″ at 1 AU** (max 1952″, min 1887″): NASA Sun Fact Sheet; R12-032, MEASURED. That is **0.5331° = 9.304 mrad**, with a seasonal swing of ±1.7 %.
- **From IAU constants:** 2·asin(R⊙N/au) = **9.3010 mrad = 0.5329°**. R12-033, DERIVED, using IAU 2015 B3 R⊙N = 6.957×10⁸ m and IAU 2012 B2 au = 149 597 870 700 m.
- **Result:** the two agree to 0.03 % and confirm the model's 0.533° / 0.0093 rad.

## Failed / unusable sources

- **CIA World Factbook (land/water area):** cia.gov now serves "The World Factbook ... has sunset" (February 4, 2026) instead of the data; I replaced it with USGS.
- **NASA POWER `CLRSKY_DAYS` climatology:** the annual value is −999 (fill) at 6 of 12 cells, and the monthly values exceed the number of days in a month (for example, Mojave January = 123). I don't use it.
- **NSSDC live host (nssdc.gsfc.nasa.gov):** connection refused or timed out. I read the Wayback snapshot of 2026-09-22 instead.
- **Maxar 1300 product page:** it 301-redirects to vantor.com with no spec content. A Maxar FY2019 10-K has no design-life statement.
- **USGS Water Science School "how much water" page and noaa.gov ocean-coasts:** HTTP 403.
- **Paywalled primaries, not retrieved:**
  - Goubau & Schwering 1961 (IRE Trans. AP-9)
  - Goubau 1970 (J. Microwave Power 5(4))
  - Brown 1984 and Brown & Eves 1992 (IEEE MTT)
  - Optica published full text (bot wall)
