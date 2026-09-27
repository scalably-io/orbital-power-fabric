# R4 — Photonic fabrication routes for a 4×4 (optionally 8×8) MZI-mesh test chip

Retrieved 2026-09-27. Evidence rows: `R4-photonic-fab.csv` (178 rows; claim_ids below). Local copies of every source: `evidence/sources/R4/`. Every quote was checked against the local copy by script, except rows marked "no local copy". Those rows came from WebFetch or a browser render.

## (a) Verdict

1. **The best route is CORNERSTONE (Southampton), 220 nm SOI passive + TiN heaters, MPW #50.** Sign up by **14 Oct 2026**, submit GDS by **11 Nov 2026**. A 5.5 × 4.9 mm die costs **£14,700** plus VAT, duties and £25 shipping. Delivery is 14 weeks, so chips arrive around **17 Feb 2027** (DERIVED). The PDK is open: the gdsfactory `cspdk` is MIT-licensed, and Europractice lists the CORNERSTONE PDK as open source with no license required. SMEs and start-ups can buy slots (R4-017/018/021/022/028/030/138).
2. **Free pilot, if you are eligible: openEBL-2026-10.** Deadline **17 Oct 2026**. It is free, 605 × 410 µm, and measured by SiEPICfab. It is passive only, so it can check couplers, directional couplers (DCs) and MZI loss, but it cannot measure heater power. Eligibility is limited to people who took a SiEPIC course (R4-080/082/083).
3. **The cheapest published heater-capable SOI slot is imec Passives+ via Europractice: €6,700 for a half block.** Reserve by 7 Oct 2026; tape-out is 16 Dec 2026. But the PDK is under a license agreement and the service is scoped to universities, research institutes and their spinouts. A layout made with it cannot be published as open hardware (R4-005/008/015/016).
4. **No license-clean, fabricated 4×4 Clements-mesh GDS exists that we could find.** The practical path is to compose 6 MZIs with 12 heaters from existing MIT-licensed cells in cspdk or ubcpdk, which is composition rather than new invention (R4-142/155).
5. **SiN routes (Ligentec, LioniX, CORNERSTONE SiN) have lower loss but much higher heater power.** One SiN platform measured **350 mW** per tuner, against **<20 mW/π** stated for CORNERSTONE SOI. That puts a 4×4 SiN mesh at about 4.2 W of static power (DERIVED), which is bad for the energy-per-operation goal (R4-033/167/172).
6. **Surprises:**
   - Europractice's price for CORNERSTONE rose **+34.5 %** from 2025 to 2026 (R4-040).
   - imec Passives+ slipped from July to December 2026 (R4-006).
   - SMART Photonics has no open runs (R4-107).
   - GlobalFoundries Fotonix costs **€242,000 per block** (R4-112).
   - Efabless is gone and ChipFoundry bought its assets (R4-117/119).

## (b) Shuttle table (as of 2026-09-27)

| Foundry | Platform | Components | Next deadline | Smallest-die price (published) | PDK openness | Small company can buy? | claim_ids |
|---|---|---|---|---|---|---|---|
| **CORNERSTONE** | 220/340/500 nm SOI; 300 nm SiN; Ge-on-Si | TiN heaters on passive runs; modulators on active runs; photodiode (PD) pick-and-place service £750/die | Sign-up 14 Oct 2026 / GDS 11 Nov 2026 (#50 SOI passive); active #51 13 Jan 2027; SiN #14 10 Feb 2027 | £8,875 passive, £14,700 with heaters (5.5 × 4.9 mm); Europractice €17,787 standard / €17,052 discounted | Open: cspdk (MIT); standard components open; the IPKISS version needs a Luceda license | Yes (SMEs, start-ups); 50 % off for UK only | R4-017–046, 138–139 |
| **imec** (Europractice / IC-Link) | 220 nm SOI | Passives+: metal heaters. iSiPP50G: modulators, Ge PD, SiN | Reserve 7 Oct 2026; final GDS 11 Dec; tape-out 16 Dec 2026 | Passives+ half block €6,700 standard / €6,400 discounted. iSiPP50G quarter block €11,000 | License agreement | Europractice: universities, institutes, spinouts. IC-Link company route not stated | R4-005–016 |
| **AIM Photonics** (US) | SOI + SiN | Active PIC: Ge PD, 2 Cu metal levels, thermal phase shifters (Dream library). Passive PIC has no metal | 1 Dec 2026 (active ships 4 May 2027; passive 2 Mar 2027) | Passive 25 mm² $34,320; Active 8 mm² $42,900 (non-member; 20 chips) | License, development use only | Non-members yes. Non-US membership needs government approval; no individual membership | R4-047–060 |
| **Ligentec** | SiN (AN800/350/150); TFLN via LN runs | "High-efficiency heaters" module; InGaAs PD on AN800 | AN800-45: register 1 Oct, design 22 Oct 2026. AN800-46: 22 Jan 2027 | CHF 21,000 for 5 × 10 mm², 16 chips (JePPIX price page, last modified 2025-04-30) | DKLA signed by the institution | Institutions | R4-061–068 |
| **Applied Nanotools** (e-beam) | 220 nm SOI (single full etch on MPW); SiN | TiW heaters + Au pads; thermal isolation trenches; no modulators or PDs | Si MPW final GDS 13 Oct 2026, then 24 Nov 2026 | **Not public (login)** | SiEPIC EBeam PDK is MIT; ANT's own PDK pages sit behind a login | Online account (terms not verified) | R4-069–079, 133–137 |
| **VTT** | 3 µm SOI | Thermo-optic + PIN phase shifters, Ge PD (2022 document) | **No 2026 schedule found** | 2022: €11.3k for 5 × 4.75 mm² active flow (stale) | DKLA; gdsfactory/vtt is MIT | Unknown | R4-088–091, 140 |
| **LioniX TriPleX** | SiN | Heaters | Run 38 tape-out 27 Nov 2026, devices 30 Apr 2027 | €17,800 for 10 × 10 mm², 4 copies; academic €9,550 (JePPIX 2025-04) | NDA (JePPIX) | Yes (commercial price listed) | R4-092–095, 105 |
| **IHP photonic BiCMOS** | SOI photonics + 0.25 µm SiGe BiCMOS | "Full photonic device set" (heater availability not verified) | EPIC tape-in 2 Nov 2026, ships ~5 Jul 2027 (Europractice lists 2 Oct) | €9,000/mm² standard; minimum 0.8 mm² → €7,200 (DERIVED) | Not verified | IHP direct or Europractice | R4-096–101 |
| **Fraunhofer HHI** | InP | Thermo-optic + electro-optic phase shifters, MZMs, PDs, lasers | HHI44: PO 22 Oct, design 1 Nov 2026, delivery 22 Apr 2027 | €8,280 for 2 × 8 mm², 4 chips (JePPIX 2025-04) | NDA | Ships only to the legal entity that issues the purchase order | R4-102–106 |
| **SMART Photonics** | InP | — | **No runs open**; "2027 by inquiry" | €7,250 XS (stale) | NDA | Closed | R4-107–108 |
| **Tower PH18** | SOI + SiN | Heater, Ge PD, PIN phase shifters/MZMs | B6418 tape-in 27 Oct 2026, ships 21 Jun 2027 | **Not published** | Not verified | Contact form | R4-109–111 |
| **GlobalFoundries Fotonix (45SPCLO)** | Monolithic 45 nm SOI CMOS + photonics | Phase shifters, modulators, Ge PD | Europractice registration deadline 21 Dec 2026 (GDS within 6 weeks) | **€242,000 per 5 × 5 mm block** (mini@sic €154,000, academic only) | Not verified | Standard price via Europractice | R4-112–114 |
| AMF (extra, via Europractice) | 220 nm SOI | Modulators, Ge PD, 2 metal levels (TiN heaters used by Pai 2023) | GDS 4 Nov 2026 | €21,000 for a 22 mm² block (the "discount" column says €600, which looks anomalous) | Not verified | Via Europractice | R4-115–116, 149, 171 |
| **Europractice** (broker) | — | — | 2027 schedule not yet published | Standard tier for everyone who is not an eligible academic | — | Yes, at standard price; SME support programme | R4-001–004, 175–176 |

## (c) Open designs

| Repo | License | GDS or simulation | Fabricated with published measurements? | claim_ids |
|---|---|---|---|---|
| SiEPIC/SiEPIC_EBeam_PDK | MIT | GDS / KLayout PCells | Yes: its components are fabricated in openEBL runs and the data is posted. No mesh included | R4-136, 137, 087 |
| gdsfactory/ubc (ubcpdk) | MIT | GDS (Python) | Through SiEPIC/ANT runs; heater cells are in the "Beta" library only | R4-133–135 |
| gdsfactory/cspdk | MIT | GDS | CORNERSTONE standard components have vendor-measured data | R4-138, 139, 037 |
| gdsfactory/gdsfactory | MIT | GDS building blocks (mzi, mzi_lattice, straight_heater_metal) | Generic cells, not tied to a fab; no Clements-mesh cell found | R4-142 |
| gdsfactory/vtt | MIT | GDS | No 2026 run to map it to | R4-140 |
| gdsfactory/lxt_pdk_gf | MIT ("sample") | GDS (TFLN) | Not checked | R4-141 |
| SiEPIC/openEBL-* run repositories | MIT | GDS + posted measurement data | Yes, including 2024 heater runs | R4-143, 084, 087 |
| solgaardlab/dphox | MIT | Layout library | Used to design a 15-MZI 6 × 6 mesh made at AMF and measured (Pai et al.); whether the chip GDS itself is public was not verified | R4-149, 171 |
| solgaardlab/phox | **No license** | Control/simulation code | Tied to the chip above, but no reuse rights | R4-150–151 |
| fancompute/neuroptica | MIT | Simulation | No | R4-144 |
| solgaardlab/neurophox | MIT | Simulation | No | R4-145 |
| flaport/photontorch | AGPL-3.0 | Simulation | No | R4-146 |
| JeremieMelo/pytorch-onn | MIT | Simulation | No | R4-147 |
| BYUCamachoLab/simphony | MIT (+NOTICE) | Simulation | No | R4-148 |
| atharveeee-netizen/qfoton | MIT | GDS generator (hackathon project) | No | R4-152 |
| XanaduAI/strawberryfields | Apache-2.0, archived | Simulation | No | R4-153 |

**Design rule (Clements):** a mesh needs N(N−1)/2 MZIs. A 4 × 4 mesh is 6 MZIs with 12 phase shifters; 8 × 8 is 28 MZIs with 56 (R4-154/155).

## (d) Recommended routes (ranked)

**1. CORNERSTONE MPW #50, 220 nm SOI passive + heaters, designed with gdsfactory + cspdk (MIT).**
- **Cost:** £14,700 for 5.5 × 4.9 mm, or £19,980 for 11.47 × 4.9 mm to fit both a 4 × 4 and an 8 × 8 plus test structures. All prices exclude VAT, duties and £25 shipping (R4-018/027). Through Europractice at standard price the half block is €17,787 (R4-038).
- **Time:** sign-up 14 Oct 2026, GDS 11 Nov 2026, chips around 17 Feb 2027 (DERIVED, assuming the 14 weeks start at the design deadline) (R4-017/021/022).
- **What can be measured:**
  - Heater power per π: vendor states <20 mW/π; Harris 2014 measured 24.77 mW/π in a comparable SOI foundry process (R4-033/156).
  - Heater-to-heater thermal crosstalk: 1 % was measured in an 88-MZI SOI mesh (R4-162).
  - MZI extinction ratio (66.3 dB measured for one MZI) and optical crosstalk (about 40 dB measured in a 30-MZI mesh) (R4-163/169).
  - MZI and mesh loss: the 88-MZI chip lost 0.97 dB on-chip (DERIVED) (R4-160/161).
  - Grating coupler loss: 5.5–6.5 dB per coupler, so the fiber-to-fiber budget is dominated by coupling (R4-037).
  - Static power: 0.24 W for a 4 × 4 and 1.12 W for an 8 × 8, both at 20 mW/π (DERIVED) (R4-172).
  - Energy per operation, using a formula that R3 owns.
  - CORNERSTONE also sells chip-level characterisation of heater power and thermal crosstalk; no price is published (R4-042).
- **Risks:**
  - Price rose 34.5 % year on year (R4-040), and CORNERSTONE may cancel calls (R4-045).
  - The two published prices for the passive full block conflict: £9,470 vs £12,790 (R4-019/020). The number of dies delivered is not stated.
  - There is no on-chip photodetector on passive runs; pick-and-place PDs cost £750 per die and add 4 weeks (R4-043).
  - cspdk is maintained by gdsfactory, not by the foundry.
  - UK VAT and customs treatment for a non-UK buyer was not verified.
  - An 8 × 8 probably needs the full block. This is inferred: 8 columns of the 625 µm MZIs used in Pai's chip already come to about 5 mm before couplers and pads (R4-171).

**2. openEBL (free pilot now) → Applied Nanotools NanoSOI paid run with heaters, using the SiEPIC EBeam PDK (MIT).**
- **Cost:** openEBL is free (R4-080). ANT's price is **not published** (login wall, R4-073).
- **Time:**
  - openEBL deadline 17 Oct 2026; measurements arrive 4–6 weeks after tape-out (R4-082/083).
  - ANT deadlines are 13 Oct and 24 Nov 2026, with 6–8 weeks turnaround including metal. The fastest possible silicon is roughly late Nov to Dec 2026 (DERIVED) (R4-069–071).
- **What can be measured:**
  - openEBL (passive only): DC split ratio, passive MZI loss, grating coupler loss.
  - A full 4 × 4 cannot be tested in openEBL's automated setup: at most 3 outputs are measured per input, and 8 couplers at 127 µm pitch need about 889 µm, more than the 410 µm available (R4-085/086).
  - ANT run: heater power per π and crosstalk, with isolation trenches available (R4-074/076).
- **Risks:**
  - Eligibility for openEBL requires SiEPIC course alumni status; the edX course price was not verified (R4-177).
  - No openEBL heater run found after July 2024 (R4-084).
  - Heater cells in the PDK are "Beta" (R4-135).
  - MPW runs allow only a single full etch.
  - ANT's price is unknown.

**3. imec Passives+ via Europractice, only if an academic partner or spinout places the order.** A US entity can instead use AIM Active.
- **imec cost and time:** €6,700 for a half block, 25 dies per Europractice (IC-Link says 10). Reserve by 7 Oct 2026; tape-out 16 Dec 2026; turnaround is not published (R4-005/008/011/012).
- **AIM alternative:** $42,900 non-member for 8 mm², with Ge photodetectors on chip. Design due 1 Dec 2026, chips 4 May 2027 (R4-048/051/054).
- **Risks:**
  - The PDK license and NDA mean the layout cannot be released as open hardware (R4-016/056/057).
  - imec's service is scoped to universities, institutes and spinouts (R4-015), and its schedule has already slipped once (R4-006).
  - AIM needs government approval for non-US membership (R4-059).

**Not recommended for this test chip:**
- **SiN (Ligentec, LioniX):** heater power of about 350 mW, so about 4.2 W for a 4 × 4 (R4-167/172).
- **InP (HHI):** only 4 chips per order (R4-103).
- **GF Fotonix:** €242,000 per block (R4-112).
- **Tower:** no published price (R4-111).

**Companion ASIC (not on the critical path).** Heater drive could probably use off-the-shelf multichannel DACs; this is inferred, not sourced. If a chip is wanted anyway:
- **Tiny Tapeout:** €185 for an individual (one tile plus devkit). TTSKY26d closes 30 Nov 2026 and TTGF26c closes 7 Dec 2026; shipping around 9 Jun 2027 (R4-122/123).
- **wafer.space GF180:** $3,000 standard for 1,000 dies; GDS by 16 Dec 2026; parts ship Q2 2027 (R4-126/127).
- **ChipFoundry CI2612:** $14,950; tapeout 7 Dec 2026; delivery 25 May 2027 (R4-120/121).
- **IHP open-source CMOS5L:** €1,500/mm²; register by 26 Oct 2026. The design must be released under Apache-2.0, and the run only happens if all customers together reach 90 mm² (R4-128/129).

## (e) Negative findings

- **Efabless** shut down (announced 1 Mar 2025). ChipFoundry bought its IP on 3 Sep 2025 and runs chipIgnite shuttles again (R4-117–121).
- **SMART Photonics** has no runs open for 2026 (R4-107).
- **GlobalFoundries Fotonix** costs €242k per block, and mini@sic is for academics only (R4-112/114).
- **NDA or license walls:**
  - imec: license agreement (R4-016).
  - AIM: license for development use only (R4-056/057).
  - Ligentec: DKLA (R4-066).
  - VTT: DKLA (R4-090).
  - JePPIX foundries (HHI, SMART, LioniX): NDA (R4-105).
  - CMC's ANT kit: NDA (R4-078).
  - ANT pricing and PDK pages: login required (R4-073/079).
- **openEBL:** the 2026 runs are passive only (R4-082/084).
- **Unpublished prices:** Tower (R4-111), AIM packaging/test (R4-060), and Tyndall/Europractice packaging (R4-173).
- **Europractice:**
  - Ligentec, ANT, HHI, SMART, Tower and VTT photonics are not on its 2026 photonics menu (R4-003).
  - Its 2027 schedule page is not yet published (R4-175).
- **No reusable, fabricated 4 × 4 mesh layout found.** phox has no license (R4-151), and qfoton was never fabricated (R4-152).

## (f) Failed sources and open questions

**Failed:**
- ANT pricing, PDK, packaging and measurement pages: login wall (R4-073/079).
- Ligentec site: curl returned HTTP 403. WebFetch extraction was used instead, so R4-062/066–068 are not byte-verified.
- VTT: no 2026 MPW information, and the ePIXfab calendar returned 404 (R4-091).
- Europractice: 2027 page and photonics overview page both returned 404 (R4-175/176).
- edX course page (R4-177).
- Optica Photonics Research coupling review: JavaScript wall (R4-178).
- Tower building blocks, the ChipFoundry press release and Tiny Tapeout pricing were captured via WebFetch or a browser render only.

**Open questions:**
1. How many dies does CORNERSTONE deliver per MPW slot, and which passive full-block price (£9,470 or £12,790) applies?
2. imec: 25 or 10 dies, and what is the turnaround? Can a non-spinout company buy through IC-Link?
3. What does the €600 "discount" figure for AMF mean?
4. Does IHP EPIC include heaters, and what are its PDK terms? Is a 2027 photonics-only (PIC) run planned?
5. VTT's 2026/27 schedule and price.
6. ANT's MPW price, and whether ANT or openEBL will run with heaters in 2026–27.
7. UK VAT and customs treatment for a Serbian buyer at CORNERSTONE.
8. Is openEBL open to someone who is not a student?
9. No sourced SOI data on directional-coupler split tolerance; only the SiN figure of σ = 0.126 is available (R4-164).
10. Is the GDS of Pai et al.'s AMF chip public?
11. Do a 4 × 4 mesh plus couplers plus pads fit in 5.5 × 4.9 mm? This needs a draft layout to answer.
12. JePPIX prices (Ligentec, LioniX, HHI, SMART) date from 2025-04-30 and may be stale.
