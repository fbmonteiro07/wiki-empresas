# Lane tx_b: Texas hyperscaler self-builds and multi-tenant colo (round 2, 2026-11-06)

Files: `tx_b.csv` (32 new rows), `tx_b_fixes.csv` (2 fixes), `tx_b_ramps.json` (14 ramp entries). Schema v1; as_of 2026-11-06.

**Method.** The corpus has almost nothing on these sites. The working sources were:
- **Texas TDLR TABS.** Its search API (`/TABS/Search/SearchProjects`, server-side DataTables POST) answers stdlib urllib without a login. I swept every county in the target list for projects of $200m or more completing from Oct-2025 on, then pulled the project pages (start date, completion date, cost, owner, scope).
- **Baxtel.** Building pages are readable by urllib. They give years and descriptions; MW is gated.
- **Cleanview's free Texas top-10 list.** It gives full-build-out power capacity for the largest campuses.
- **19 of 35 WebSearches**, used for MW.

TDLR rarely states MW; Vantage, QTS, Prime, Digital Realty and Stream filings are the exceptions. **MW, not dates, was the binding constraint.**

## Rows added (32)

| project_id | MW | basis | cod_base | note |
|---|---|---|---|---|
| TX-BOLING-AWSEAGLE-ALL | 75 | grid | 2027-01 | AWS, 10 bldgs; "more than 75 MW" peak (floor) |
| TX-CASTROVILLE-MSFTSAT89-B1 | 93 | gen | 2027-07 | 30 × 3.1 MW gensets |
| TX-HASKELL-GOOGLESOUTHHASKELL-ALL | 250 | grid | 2027-04 | 250 MVA substation proxy |
| TX-HASKELL-GOOGLEJOURNEY-1A2A | 640 | gen | 2027-08 | **Quantum solar nameplate; a proxy, not load** |
| TX-PAMPA-GOOGLEMEITNER-ALL | 840 | grid | 2027-11 | Cleanview |
| TX-VERNON-GOOGLERISE-ALL | 850 | grid | 2028-03 | Cleanview |
| TX-WHITNEY-CYRUSONEDFW10-B1 | 190 | grid | 2026-10 | Calpine Thad Hill |
| TX-WHITNEY-CYRUSONEDFW17-ALL | 210 | grid | 2026-12 | 400 − 190, derived |
| TX-FAIRFIELD-CYRUSONEDFW20-PH1 | 380 | grid | 2027-03 | Calpine Freestone |
| TX-CASTROVILLE-CYRUSONESAT14-A | 189 | gen | 2027-06 | 84 × 2.25 MW gensets |
| TX-CASTROVILLE-CYRUSONESAT14-B | 189 | gen | 2028-06 | Baxtel year only |
| TX-HUTTO-SKYBOX-ALL | 600 | grid | 2026-06 | two 300 MW substations |
| TX-LANCASTER-SKYBOX-ALL | 300 | grid | 2026-05 | |
| TX-LANCASTER-STACKDFW02-ALL | 310 | IT | 2027-03 | |
| TX-REDOAK-DATABANK-PH1 | 180 | unknown | 2026-12 | |
| TX-REDOAK-DATABANK-PH2 | 300 | unknown | 2027-10 | 480 − 180, derived |
| TX-TEMPLE-ROWAN-ALL | 300 | unknown | 2027-06 | |
| TX-LYTLE-ROWANCINCO-PH1 | 60 | grid | 2026-06 | |
| TX-LYTLE-ROWANCINCO-PH2 | 90 | grid | 2026-09 | |
| TX-LYTLE-ROWANCINCO-PH3 | 150 | grid | 2028-06 | |
| TX-FORTWORTH-EDGEDDFW02-ALL | 196 | unknown | 2027-12 | Fort Worth moratorium |
| TX-FORTWORTH-PRIMEDFW04-B1B3 | 144 | IT | 2026-01 | **date conflict, see below** |
| TX-GARLAND-PRIMEDFW02-B2 | 48 | IT | 2026-09 | campus ≥100 MW not sourced |
| TX-FORTWORTH-QTSFTW1-DC2 | 42 | unknown | 2026-04 | energized |
| TX-WILMER-QTSDFW2-DC3 | 90 | unknown | 2027-01 | |
| TX-TURKEY-QTSHALL-ALL | 1,000 | grid | 2028-06 | Lancium 1 GW connection under ERCOT study |
| TX-FORTWORTH-CORAVEL-HICKSFIELD | 140 | IT | 2027-06 | lease→filing mapping is an inference |
| TX-WESTLAKE-POWERHOUSE-B1 | 75 | unknown | 2027-06 | 300 / 4, derived |
| TX-GARLAND-DLRDFW45-B1 | 80 | unknown | 2029-01 | campus ≥100 MW not sourced |
| TX-CEDARCREEK-EDGECONNEX-AUS01 | 96 | unknown | 2026-06 | |
| TX-CEDARCREEK-EDGECONNEX-AUS11AUS12 | 240 | unknown | 2028-12 | |
| TX-SANANTONIO-VANTAGETX1-B1 | 32 | IT | 2026-09 | energized; round 1 missed it |

**Total: 8,379 MW of source MW, mixed bases:**
- grid 4,995
- unknown 1,599
- gen 1,111
- IT 674

## MW by state × cod year × mw_basis (TX only; never add across bases)

Row cod_base (before ramps):

| year | IT | grid | gen | unknown |
|---|---|---|---|---|
| 2026 | 224 | 1,450 | – | 318 |
| 2027 | 450 | 1,545 | 922 | 961 |
| 2028 | – | 2,000 | 189 | 240 |
| 2029 | – | – | – | 80 |

After `tx_b_ramps.json`, with even tranches (a Capstone estimate):

| year | IT | grid | gen | unknown |
|---|---|---|---|---|
| 2026 | 224 | 792 | – | 198 |
| 2027 | 192 | 1,322 | 922 | 703 |
| 2028 | 52 | 1,605 | 189 | 338 |
| 2029 | 103 | 425 | – | 240 |
| 2030 | 103 | 225 | – | – |
| 2031-35 (outside scope) | – | 625 | – | 120 |

By likelihood:
- **high:** grid 2,945 / gen 922 / unknown 948 / IT 172
- **medium:** grid 2,050 / IT 502 / unknown 651 / gen 189

Air permit:
- `n/a` (grid-only) on all rows except Meitner and Rise. Those two are `unknown`: Meitner has on-site gas firming; AES's fuel mix for Rise is not stated.
- None of these rows has a TCEQ prime-generation permit on file that I could verify. The TCEQ portal returned 401.

## Fixes (2), in `tx_b_fixes.csv`

- **TX-REDOAK-GOOGLE-B2:** cod_source analyst → filing. TDLR RED2A completes 2026-12-12 (TABS2027003112, Alamo Mission LLC = Google shell). Month unchanged.
- **TX-CAMERON-MILAM-B1:** 2027-06 year_only → 2026-10 filing. The TDLR "Freebird Data Center Phase 1" registration (TABS2026017746) completes 2026-10-15; Baxtel ties it to SB Energy Milam Bldg 1 (Orion DC I). With the central +6-month shift this lands about 2027-04, consistent with the S-1/A's "first-phase RFS 2027".
- **Goodnight is not touched.** tx_a already fixed B1, B2 and B3B6. For reference, TDLR B3-B5 dates exist:
  - B3: 2027-01-29 (TABS2026003348); a later "Llano Building 3" shell filing (TABS2026026002) shows 2026-08-01
  - B4: 2027-02-26 (TABS2026003350); a second filing (TABS2026026118) shows 2027-03-15
  - B5: 2027-05-28 (TABS2026010858)

## Rows dated from Texas TDLR construction-completion dates (cod_source `filing`; notes start "TDLR completion YYYY-MM-DD")

- Hyperscaler self-builds:
  - TX-BOLING-AWSEAGLE-ALL
  - TX-CASTROVILLE-MSFTSAT89-B1
  - TX-HASKELL-GOOGLESOUTHHASKELL-ALL
  - TX-HASKELL-GOOGLEJOURNEY-1A2A
  - TX-PAMPA-GOOGLEMEITNER-ALL
  - TX-VERNON-GOOGLERISE-ALL
- CyrusOne:
  - TX-WHITNEY-CYRUSONEDFW10-B1
  - TX-WHITNEY-CYRUSONEDFW17-ALL
  - TX-FAIRFIELD-CYRUSONEDFW20-PH1
  - TX-CASTROVILLE-CYRUSONESAT14-A
- Skybox and STACK:
  - TX-HUTTO-SKYBOX-ALL
  - TX-LANCASTER-SKYBOX-ALL
  - TX-LANCASTER-STACKDFW02-ALL
- DataBank:
  - TX-REDOAK-DATABANK-PH1
  - TX-REDOAK-DATABANK-PH2
- Edged and Prime:
  - TX-FORTWORTH-EDGEDDFW02-ALL
  - TX-FORTWORTH-PRIMEDFW04-B1B3
  - TX-GARLAND-PRIMEDFW02-B2
- QTS:
  - TX-FORTWORTH-QTSFTW1-DC2
  - TX-WILMER-QTSDFW2-DC3
- Other colo:
  - TX-FORTWORTH-CORAVEL-HICKSFIELD
  - TX-WESTLAKE-POWERHOUSE-B1
  - TX-GARLAND-DLRDFW45-B1
- EdgeConneX:
  - TX-CEDARCREEK-EDGECONNEX-AUS01
  - TX-CEDARCREEK-EDGECONNEX-AUS11AUS12
- Vantage:
  - TX-SANANTONIO-VANTAGETX1-B1
- Fixes:
  - TX-REDOAK-GOOGLE-B2
  - TX-CAMERON-MILAM-B1

Ramps also use TDLR dates for later buildings, and Baxtel "Year Planned" where no filing exists.

## Biggest campuses still un-pinned (dated or sized, but not both)

1. **Microsoft San Antonio / Castroville / Medina program.** Microsoft discloses no MW, and genset counts were found only for SAT89. TDLR completions:
   - SAT82: two filings, 2028-02-08 and 2028-07-24
   - SAT90 (with SAT89): 2027-07-31
   - SAT94: 2027-06-15
   - SAT93: 2027-06-15, re-registered with completion 2029-04-30 (TABS2026014456)
   - SAT15: 2026-05-01
   - SAT16/SAT 17: 2027-12-01
   - Cleanview: "Microsoft Texas Research Park" has 409 MW operating.
2. **AWS Horizon Junction** (Floydada, Floyd Co.). Owner Amazon Data Services; Bldgs A-D at $300m each, TDLR 2027-04-01. No MW.
3. **Google's other new Texas sites:**
   - Project Roman (Deaf Smith Co., with Intersect): first phase is 4 bldgs, 2026 to fall 2028.
   - Quest and Ranger (Haskell Co.): abatements only.
   - Midlothian "Sharka" Bldg 5: TDLR 2027-02-24, $492m (Baxtel: $880m).
   - None has MW.
4. **QTS South Dallas DFW2.** DC1, DC2, DC5, DC6 and DC7 (TDLR 2025-12 to 2027-12; 363k-470k sf each) have no MW; only DC3's 90 MW is rowed.
5. **EdgeConneX Cedar Creek.** Six more 730k-sf buildings (EDCAUS13-16, 31-32), about $4bn, TDLR 2028-05 to 2029-03, no MW. The first campus also has up to about 336 MW in future phases (AUS02-04, 2028-31).
6. **"Project Clocktower"** (Quanah, Hardeman Co.). TDLR "NWB 05" network building, **$8bn**, completion 2028-12-31, owner 19000-200 Holdings LLC. Cleanview calls it "Integra Quanah Data Center Campus". No MW.
7. **Edged Maxwell** (Caldwell Co.): one 869,684 sf building, $2.8bn, TDLR 2028-06-30.
   - **Prime Lockhart AUS01/02:** 2 × 380k sf, TDLR 2027-09-30; an 8-building plan runs to 2034.
   - **Tract Caldwell Valley:** a 1.6 GW substation, first capacity Q1-2028; powered land with no data-center tenant named.
   - None of the three has data-center MW.
8. **Smaller undated or unsized items:**
   - Vantage TX2 (TX21, TX22: 2027-06-15)
   - Stream: SATB (5 bldgs) and DFWC1 (48 MW; campus total unsourced)
   - CloudHQ SAT (5 bldgs)
   - Aligned DFW-03 (Plano)
   - Yondr Lancaster (5 bldgs, 2029)
   - QTS Greene Road Lancaster (5 bldgs, 2030)
   - Switch Round Rock
   - CyrusOne Fort Worth DFW7 / DFW8 (TFO 2027-10)
   - DA12 Dallas (TDLR 2027-10, 20 generators)
   - CoreSite DA1 Irving (2028-12)
   - Colovore Hutto and Alliance (2028-12)
   - Skybox PowerCampus Wichita Falls
9. **Compass Red Oak:** not rowed. Planned capacity is 360 MW (datacentermap), but Cleanview shows **323 MW already operating**. That leaves the remaining buildings VI-X ambiguous; TDLR TFO completions for Bldgs 8-10 are 2027-10, 2028-03 and 2028-08.
10. **SpaceX Starbase compute and Terafab.**
    - SemiAnalysis 11-03 (image-only on disk) says Starbase "may use 1GW of APRs". No MW or date.
    - No TDLR data-center filing exists in Cameron or Grimes counties; the only Cameron hit is "Gigabay", a factory.
    - Baxtel places Terafab in Conroe.
11. **Excluded as denied:** Sailfish Project Panther / Project Lion (Hood Co.). The development commission recommended rejection and the county denied the on-site permit.
12. **No new Meta Texas campus was found.** Baxtel's El Paso list (11 bldgs, 2027-29) is consistent with the existing rows.

## Conflicts to adjudicate

1. **GW Ranch (tx_a row TX-FORTSTOCKTON-GWRANCH-ALL, 5,000 MW gen, low, tenant blank).** Three sources point to AWS:
   - TDLR shows **Amazon Data Services** as owner of Bldgs A-C at 6000 TX-18, completion 2026-12-01 (TABS2026026954/55/59).
   - Texas Public Radio (2026-09-18) and Baxtel say Amazon bought the site and Pacifico sells it the plant's output.
   - The TCEQ air permit (7.65 GW) was issued Jan-2026.

   This suggests tenant Amazon and likelihood medium or high for phase 1. I did not row it, to avoid a duplicate.
2. **Prime DFW04 timing.** TDLR completion is 2026-01-29 for all three buildings, but the status is still "Project Registered"; Baxtel lists 2027.
3. **Vantage TX12 (existing TX-SANANTONIO-VANTAGETX1-B2).** The 96 MW fit-up has its own TDLR completion of 2028-03-30 (TABS2026012091), versus 2027-08-31 for the base building used in round 1.
4. **DataBank PH1.** Tenant fit-out dates (2026-12 to 2027-03) are earlier than the shell completions (2027-02 to 2028-07).
5. **Google Journey's 640 MW is solar nameplate, not load.** Keep it or drop it.
6. **Rowan Cinco:** 300 MW in 2028 (local presentation) vs "full operation 2027" (Rowan).
7. **CyrusOne DFW10:** 190 MW vs 144 MW.
8. **Edged phase 2:** TDLR 2028-04 vs the city plan's 2031.
9. **EdgeConneX AUS11/12:** TDLR 2028-12 vs DCD's "mid-2026".

## Leads for tx_a

- **Horizon Junction (Floydada) is AWS**, not Poolside.
- **Project Hyper "Spur"** (Kent Co.): TDLR Bldg 1 2029-06-07 and Bldg 2 2029-05-25, $2.4bn each.
- **Galaxy Helios Phase 2** TDLR completions:
  - Helios 2: 2027-02-08
  - Helios 3: 2027-08-29
  - Helios 4: 2027-11-29
- **Riot "Project Ditto"** (Corsicana): TDLR 2028-05-19.
- **ADC LBB01** (Hale Co.): 2027-11-15, $425m.
- **BT Gateway** (Royse City, Giga AFM LLC): 2027-02-12, $384m.
- **Burr Computer Environment** (the EdgeConneX entity behind EDCAUS11) is the same name as the 400 MW Victoria TCEQ permit in tx_a's notes.
- **CloudBurst (tx_a row)** sits in Hays County. The Hays County emergency water-protection review (LOC-TX-054, 2026-06 to 2026-12) applies.

## Paywalled or blocked

- **Returned 403 or 404:**
  - DCD (403 for both urllib and WebFetch)
  - EdgeConneX site, BusinessWire, EnergyTech, Power-Eng, Community Impact, Dallas Express (403)
  - DataCenterHawk (404)
- **Timed out:** Constellation IR.
- **TCEQ air-permit database:** 401.
- **Gated:** Cleanview building and campus data beyond the free top-10, and Baxtel MW fields.
- **Image-only on disk, not OCR'd:** the WFS Texas note, SemiAnalysis 11-03 and FundaAI 11-04.
