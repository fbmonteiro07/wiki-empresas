# va_se round 2: VA / MD / WV / NC / SC (2026-11-06)

Files in `round2/`: `va_se.csv` (17 new rows), `va_se_fixes.csv` (11 full replacement rows for R1 ids), `va_se_ramps.json` (5 ramps; 4 for new rows, 1 for a fixed row). Header checked against SCHEMA.md. WebSearch budget: 35 of 35 used. The corpus had almost nothing at project level for this region. Searches for Henrico, Chesterfield, Mecklenburg, Blue Marlin, CloudHQ, Digital Dulles and Louisa returned no hits; the "amigo Felipe" deck gives only state totals.

## Rows added (17)

| project_id | MW | basis | cod_base | status | local approval |
|---|---|---|---|---|---|
| VA-STERLING-DIGITALDULLES-B9 | 106 | facility | 2026-06 yo | UC | unknown |
| VA-ASHBURN-CLOUDHQLC-LC11 | 92.6 (ALLOC) | IT | 2027-06 yo | UC | unknown |
| VA-ASHBURN-CLOUDHQLC-LC8LC10 | 200.6 | IT | 2027-06 yo | not started | unknown |
| VA-ASHBURN-CLOUDHQLC-2028 (LC5/9/12) | 277.8 (ALLOC) | IT | 2028-06 yo | not started | unknown |
| VA-ASHBURN-CLOUDHQLC-LC13 | 92.6 (ALLOC) | IT | 2029-06 yo | not started | unknown |
| VA-ASHBURN-CLOUDHQLC-LC14 | 92.6 (ALLOC) | IT | 2030-06 yo | not started | unknown |
| VA-MANASSAS-CLOUDHQMCC-MCC3MCC5 | 120 | IT | 2027-06 yo | UC | unknown |
| VA-MANASSAS-CLOUDHQMCC-MCC4 | 60 | IT | 2028-06 yo | not started | unknown |
| VA-GAINESVILLE-CORSCALE-B3 | 54 | unknown | 2026-06 yo | UC | unknown |
| VA-GAINESVILLE-CORSCALE-B4B5 | 128 (subtraction) | unknown | 2027-06 yo | not started | unknown |
| VA-LOUISA-AWSNECREEK-ALL (+ramp) | 700 | facility | 2028-06 yo | UC | approved (by-right TOD) |
| VA-STAFFORD-STACKSTC-REST (+ramp) | 1,047 (subtraction) | unknown | 2028-06 estimate | not started | approved 2023-09 |
| VA-LOUISA-EDGECORESHANNONHILL-ALL (+ramp) | 1,100 | unknown | 2028-06 yo | announced | approved (zoned 2019) |
| VA-STERLING-POWERHOUSEPACIFIC-ALL (+ramp) | 265 | grid | 2026-08 company | UC | approved (date n/a) |
| VA-CHESTER-CTP0203-ALL | 120 | grid | 2027-02 company | UC | approved 2024-06 |
| NC-HAMLET-AWSBLUEMARLIN-B6 | 65 | facility | 2028-06 yo | not started | unknown |
| NC-HAMLET-AWSBLUEMARLIN-B9 | 65 | facility | 2029-06 yo | not started | unknown |

`yo` = year_only. Face value is VA 4,456 MW and NC 130 MW, but much of it falls after 2030 once the ramps are applied (next table).

## New MW by state × year × basis (ramps applied; never add across bases)

| state | basis | 2026 | 2027 | 2028 | 2029 | 2030 | 2026-30 | after 2030 |
|---|---|---|---|---|---|---|---|---|
| VA | IT | | 413 | 338 | 93 | 93 | **936** | |
| VA | facility | 106 | | 175 | 175 | 175 | **631** | 175 (NE Creek 2031) |
| VA | grid | 88 | 297 | | | | **385** | |
| VA | unknown | 54 | 128 | 300 | 300 | 300 | **1,081** | 1,248 (STC to 2036, EdgeCore to 2033) |
| NC | facility | | | 65 | 65 | | **130** | |

Ramped rows: VA grid 2026-27 is PowerHouse Pacific (88 / 88 / 88) plus CTP-02/03 (120 in 2027). VA unknown 2028-30 is STC-REST at 116 a year plus EdgeCore at 183 a year. VA facility 2028-30 is NE Creek at 175 a year. MD, WV and SC get no new rows.

## Fixes (11, in `va_se_fixes.csv`; every notes field starts "R2 FIX:" and keeps the R1 note)

- **VA-ARCOLA-POWERHOUSEARCOLA-ALL:** was undated. Now **2027-08 company** (PowerHouse page: Power Delivery Q3 2027); basis grid ("Max Utility MW Capacity: 120 MW"); approved; likelihood high (2 hyperscale pre-leases). The meta text "by August 2026" is stale.
- **VA-SPOTSYLVANIA-POWERHOUSE95-P1:** 2027-06 year_only becomes **2027-08 company** (Power Delivery Q3 2027). Approved **2024-03** (Entitlements Q1 2024).
- **VA-SPOTSYLVANIA-POWERHOUSE95-P23:** 500 unknown becomes **600 grid**. The company now states a 900 MW campus. The date stays 2029-06.
- **NC-CHARLOTTE-POWERHOUSECLT-ALL:** 300 becomes **380 grid** (company page). cod stays 2027-04. Ramp added 2027-04 → 2028-10 (construction/delivery runs to Q4 2028).
- **VA-CHESTERFIELD-POWERHOUSECHIRISA-P1:** 300 becomes **180**, still undated. CTP-02/03 (120 MW, Q1-27) is split out as a new row. If CTP-02/03 is not inside the "initial 300 MW", restore 300.
- **VA-LEESBURG-TAREALTY-ALL:** 430 undated becomes **285, 2027-06 year_only**, likelihood high.
  - The first 2 of 5 buildings (165 MW IT) were completed and sold in Feb-26, so they are out of window. The campus is 450 MW and fully leased to one cloud provider, with completion "expected 2027".
  - The 165 comes from the TA Realty release, read only through the search index.
- **VA-MINERAL-AWSLAKEANNA-EASTRIDGE / -2026 / -2027:** local_approval becomes **approved**. Campus 1 is by-right in the Louisa Technology Overlay District (Engage Louisa, 2025-06-05).
- **VA-STAFFORD-STACKSTC-B1:** local_approval becomes **approved 2023-09** (Baxtel: the zoning covers 23 buildings).
- **NC-HAMLET-AWSBLUEMARLIN-B19:** phase relabelled "Bldg 5". Current Cleanview snippets give B19 = 2032 and B5/B6 = 2028, so the R1 2028 building was mislabelled. MW and date are unchanged.

Net effect: 525 MW of undated VA rows are now dated (Arcola 120, TA Realty 285, CTP 120 moved out of the undated Chirisa row); 145 MW of TA Realty's R1 total drops out as already built. MW added on existing campuses: +100 (PH95), +80 (Charlotte).

## TDLR-dated rows
None (no Texas rows in this lane).

## SB 843 read (the VA bear case: hold from Jul-27 to Jul-30)
- These new VA rows already have local approval before Jul-27: NE Creek (by-right), STC-REST (2023-09), EdgeCore Shannon Hill (by-right park, zoned 2019), PowerHouse Pacific and CTP-02/03 (entitlements complete).
- After the fixes, PH95-P1, Arcola, Lake Anna and STC-B1 are also approved.
- CloudHQ, Corscale, Digital Dulles B9, and Blue Marlin (NC) stay `unknown`. Most of them are already under construction.
- These are the pipeline names that would sit inside the hold. None has a sourced COD, so none is rowed:
  - Google West Creek (1,200 MW)
  - Tract Tuckahoe (900 MW; CUP filed Aug-26, no Planning Commission date, TOD lawsuit)
  - Dahlgren West (1.2 GW IT, 10 bldgs)
  - Haven Oak (~1,000 ac, Tract)
  - QTS's 17-building / ~8M sf White Oak plan (May-26)
- **Local instruments seen, none mapped to a row:**
  - **Chesterfield** said on 2026-08-27 that it will approve no more data-center projects (BizSense, 403). Google Skye and Loch were approved before that.
  - **Goochland:** a TOD lawsuit is pending; as of late Oct-26 a judge was weighing dismissal.
  - **Loudoun:** the 12-month pause on legislative applications is up for adoption on 11-17. It does not reach by-right or administrative site plans.
  - **Prince William:** the county is weighing whether to remove the data-center overlay (by-right use). That bears on AWS Devlin.

## Biggest campuses still un-pinned
1. **Digital Dulles, about 1.3 GW undated.** Cleanview puts the full build-out at 1,723 MW. Rowed so far: B7, B9, B10 (318 MW), plus B1 at 106 MW in 2032. DLR's "14 buildings" have no per-building dates outside Cleanview's paywall.
2. **QTS Richmond / White Oak, about 1.1 GW.** Cleanview: 2,054 MW full build-out against 921 MW operating. RIC3 is fully rowed. The new 17-building plan (May-26) has no MW or schedule.
3. **Google West Creek (1,200) and Dahlgren West (1,200 IT).** Proposed, no COD. Tamarack in WV (2,160 grid) has no timeline; Starwood did not answer WSAZ.
4. **Hyperscaler self-builds with no MW:**
   - Google Chesterfield Skye: 4 bldgs; online 2028 per VPM (Jun-26), first building operational 2029 per BizSense. Peanut: site plans under review Jun-26.
   - Microsoft AVC22 (Baxtel 2030) and Person County, NC (Baxtel 2029).
   - AWS Devlin Tech Park (Baxtel 2027, 3.5M sf, 3 substations).
   - Meta Henrico "Tropical" (2 bldgs).
   - Google Dorchester, SC: 2 campuses, $9bn over 2026-27, no MW.
5. **Remaining building lists:**
   - AWS Blue Marlin: ~16 more bldgs at 65 MW each (≈1 GW); only B5, B6 and B9 are dated in window.
   - CloudHQ MCC: MCC6Z and MCC7 (2027) have no MW.
   - Vantage VA4 B2-B3: 128 MW, no date after B1 (4Q27).
   - STACK LDC II: 144 MW; the STACK release and brochure give no date.
   - Village Place: 210 MW, no date.
   - Penzance, WV: 600 MW IT, no timeline.

## Conflicts for the merger
- **Louisa, resolved.** Amazon's campus 2, Northeast Creek, is under construction: Cleanview UC; WWBT 2026-07-28 reports a neighbour lawsuit and completion in 2031. The withdrawn campus is the 3rd one (1,370 ac, 7 substations, CUP filed May-25).
- **Possible double count: VA-MANASSAS-ODATA-ALL (R1, 250 MW critical) vs STACK NVA02.** MTJP's ODATA header names STACK. STACK's 2020 Hornbaker Rd campus was announced at "250MW of critical load", and NVA02 is at 9590 Hornbaker Rd. Check before summing.
- **VA-ASHBURN-ALIGNED-EXP (R1, 180 MW, undated) is probably already operating.** The 180 MW Quantum Park campus was announced in 2018 and phased through 2020 (DCF / BusinessWire). Cleanview shows Aligned Ashburn operating at 414 MW. Probably drop it.
- **QTS York (SC):**
  - Baxtel: phase 1 is 4 bldgs, first operational 2028; phases 2-3 have no date.
  - R1 rows (Cleanview): DC1-3 in 2027 and DC4-6 in 2028.
- **CloudHQ LC:**
  - CloudHQ's own page gives 1,256 MW critical in total and 756 available, while its overview text says >1.7 GW.
  - Cleanview "LC South" is 1,310 MW.
  - LC8 is 108 MW in datacentermap and 151 MW in Cleanview.
  - Rows use the company's 756 MW, allocated by building.
- **Corscale B3:** 54 MW (CommercialSearch / DCD) vs a Cleanview snippet showing a 76 MW building operational in 2026.
- **CTP-02/03:** 120 MW utility (spec) vs "60 MW BTS" (meta text). Epoch's CoreWeave Chester B2 may already be CTP-02.
- **TA Realty:** the lease was for 430 MW; the 2026 sale describes a 450 MW campus.
- **PH95:** 900 MW (company now) vs 800 (2024) vs Cleanview 525 MW.
- **Google Skye:** online 2028 (VPM) vs first building operational 2029 (BizSense).

## For other lanes (found incidentally on powerhousedata.com, 2026-11-06; not rowed here)
| Campus | State | MW | Power delivery / note |
|---|---|---|---|
| Grand Prairie | TX | 1.8 GW | Q4-26 |
| Irving | TX | 201 MW | Q1-26 |
| Circle T | TX | 300 MW | Q2-27 |
| Joliet | IL | 1.8 GW | Q4-28 |
| Hobart | IN | 450 MW | Q2-27 |
| Louisville | KY | 525 MW | Q4-26 |
| Reno | NV | 200 MW | Power Q4-25, delivery Apr-26 |
| PAX-1 | not on page | 1.35 GW | Phase 1 Q2-27, build to Q3-31 |
| 1600 Digital Drive | not on page | 300 MW+ | Q3-27 |

## Paywalled / blocked
- **Paywalled or blocked:**
  - Cleanview building pages are paywalled; MW and years come from search snippets.
  - DCD, Richmond BizSense, ConnectCRE and Cardinal News return 403.
  - datacentermap returned 429.
  - The TA Realty press-release mirror fails the SSL handshake.
  - pulse.bot dropped the socket.
- **Readable but incomplete:**
  - Baxtel campus pages load, but MW sits behind "Request Dataset"; years are tracker planning entries.
  - MTJP's VA list loads (50 UC projects), with no dates.
- **Primary sources read directly:** the PowerHouse campus pages (powerhousedata.com/data-center/*) and the EdgeCore, STACK and CloudHQ company pages.
