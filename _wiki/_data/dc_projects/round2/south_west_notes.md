# Round 2, lane `south_west` (GA, NV, AZ, LA, MO): notes, 2026-11-06

Files: `south_west.csv` (21 new rows), `south_west_fixes.csv` (3 replacement rows), `south_west_ramps.json` (13 ramp entries).
WebSearch used: 15 of 35. Most of the yield came from free primary sources: Georgia DCA DRI forms, EDGAR (APLD, ETR), developer pages, and Baxtel/MTJP building pages.

## Rows added (21)

| project_id | MW | basis | cod_base | likelihood | key source |
|---|---|---|---|---|---|
| GA-AUGUSTA-NIXONTECH-ALL | 600 | grid | 2028-06 (ramp to 2029) | low | Georgia DRI #4853 |
| GA-OCILLA-ARROWHEAD-ALL | 1,250 | grid | 2030-06 (ramp to 2034) | low | DRI #4689 |
| GA-KINGSTON-THORKINGSTON-ALL | 150 | grid | 2030-06 | low | DRI #4835 |
| GA-LITHIASPRINGS-DCBLOXATLWEST-AB | 120 | IT | 2026-06 (ramp to 2028-02) | medium | DC BLOX page + Baxtel |
| GA-LITHIASPRINGS-DCBLOXATLWEST-C | 80 | IT | 2029-02 | low | DC BLOX page + Baxtel |
| AZ-AVONDALE-STACKPHX01-ALL | 225 | IT | 2027-06 (ramp to 2029) | medium | STACK page + Baxtel |
| AZ-PHOENIX-STACKPHX02-ALL | 250 | unknown | 2028-06 (ramp to 2032) | medium | STACK page + Baxtel (permit Jan-2026) |
| AZ-AVONDALE-PRIMEPHX01-B1B2 | 96 | IT | 2027-06 | high | Prime page (leased) + Baxtel |
| AZ-AVONDALE-PRIMEPHX01-B3 | 48 | IT | 2028-06 | high | same |
| AZ-AVONDALE-PRIMEPHX01-B4 | 48 | IT | 2029-06 | medium | same (unleased) |
| AZ-AVONDALE-PRIMEPHX01-B5 | 48 | IT | 2030-06 | low | same (development) |
| AZ-MESA-NOVVA-ALL | 300 | unknown | 2027-06 (ramp to 2031) | medium | Novva page + Baxtel |
| AZ-MESA-EDGECORE-EXP | 290 | IT | 2027-06 | medium | EdgeCore page (496 MW) − 206 MW (round-1 notes) + Baxtel |
| AZ-ELMIRAGE-COMPASSPHXII-B1 | 36 | unknown | 2026-06 | medium | Bisnow/Azbex (108 MW, 3 bldgs) + Baxtel |
| AZ-ELMIRAGE-COMPASSPHXII-B2B3 | 72 | unknown | 2027-06 | medium | same |
| AZ-PHOENIX-MENLOMDPX1-ALL | 257 | unknown | 2027-06 (ramp to 2031) | medium | MTJP (azcentral) + Baxtel |
| AZ-MESA-NTTPACIFIC-ALL | 324 | unknown | 2028-11 (ramp to 2034) | medium | NTT release (snippet) + Baxtel |
| LA-ALEXANDRIA-DELTAFORGE1-ALL | 300 | IT | 2027-04 (ramp to 2028-02) | high | APLD 10-Q 2026-10-07, 8-K, deck |
| LA-HOLLYRIDGE-HYPERIONEVEST-EXP | 3,000 | unknown | 2030-06 (ramp to 2031) | medium | Entergy Q3-26 10-Q (Evest ESA; 7 CCGTs 2030-31) + Meta site |
| MO-TROY-CLOVERLEAF-ALL | 500 | unknown | 2028-06 (ramp to 2033) | low | Baxtel + MTJP (KSDK) |
| NV-MCCARRAN-SWITCHCITADEL-B7 | 118 | unknown | 2028-06 | medium | Cleanview snippet (unverified) + Baxtel |

## New MW by state × basis (never add across bases)

| state | IT | grid | unknown |
|---|---|---|---|
| GA | 200 | 2,000 | – |
| AZ | 755 | – | 1,239 |
| LA | 300 | – | 3,000 |
| MO | – | – | 500 |
| NV | – | – | 118 |

### By cod_base year, as rowed (each row at its first date)

| state | year | IT | grid | unknown |
|---|---|---|---|---|
| AZ | 2026 | – | – | 36 |
| AZ | 2027 | 611 | – | 629 |
| AZ | 2028 | 48 | – | 574 |
| AZ | 2029 | 48 | – | – |
| AZ | 2030 | 48 | – | – |
| GA | 2026 | 120 | – | – |
| GA | 2028 | – | 600 | – |
| GA | 2029 | 80 | – | – |
| GA | 2030 | – | 1,400 | – |
| LA | 2027 | 300 | – | – |
| LA | 2030 | – | – | 3,000 |
| MO | 2028 | – | – | 500 |
| NV | 2028 | – | – | 118 |

### By tranche year, after applying `south_west_ramps.json` (MW rounded)

| state | basis | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032-34 (out of window) |
|---|---|---|---|---|---|---|---|---|
| AZ | IT | – | 461 | 123 | 123 | 48 | – | – |
| AZ | unknown | 36 | 183 | 208 | 208 | 208 | 208 | 189 |
| GA | IT | 40 | 40 | 40 | 80 | – | – | – |
| GA | grid | – | – | 300 | 300 | 400 | 250 | 750 |
| LA | IT | – | 150 | 150 | – | – | – | – |
| LA | unknown | – | – | – | – | 1,500 | 1,500 | – |
| MO | unknown | – | – | 83 | 83 | 83 | 83 | 167 |
| NV | unknown | – | – | 118 | – | – | – | – |

## Fixes (3), in `south_west_fixes.csv`

- **GA-LAGRANGE-PEGASUS-ALL.**
  - Before: 400 MW grid, front-loaded at 2026-12 (Thor Equities' site potential).
  - After: 350 MW grid with a ramp from 2026-12 to 2029-06, utility MEAG Power.
  - Source: Georgia DRI #4797 "PRL2" at 411 Pegasus Pkwy (developer listed as KDC). It covers the existing building plus a ~470k sq ft phase finishing in 2029, with a peak connected load of 350 MW.
- **GA-ROME-MSFTHUFFAKER-ALL.**
  - Before: undated, basis unknown.
  - After: 422 MW grid, cod 2029-06, ramp to 2032.
  - Sources: DRI #4860 "ATL80" (Microsoft) gives 422 MW / 444 MVA peak connected load, backup diesel only, overall completion 2032. Baxtel ("Project Firecracker") says planned 2029, expansions through 2032.
- **GA-ATLANTA-EDGEDTILFORD-ATL0103.**
  - Before: 168 MW basis unknown, undated.
  - After: narrowed to building ATL01-3, 42 MW IT, 2027-02, tenant Alibaba Cloud, Georgia Power ESA executed.
  - Sources: Edged site for per-building MW; the EDGCOM credit dossier (Fitch, Apr-2026) for the date, tenant and ESA.
  - ATL01-01 (27 MW) and ATL01-02 (100 MW) have no public dates, so they are not rowed.

## Texas TDLR-dated rows
None (no Texas in this lane).

## Biggest campuses still un-pinned

**Georgia.** DRI forms since 2026 ask for "estimated peak connected electrical load (MW)"; older forms have no MW.

| campus | MW | why not rowed |
|---|---|---|
| QTS Blakely / Project Blue Hole (Early County), DRI #4651 | 1,500 grid (pending studies) | Single phase, completion Q4-2035: out of window. |
| Hampton Technology Park (Henry County), DRI #4624 | 1,500 peak | Single phase, completion 2033. |
| Bridgeport (Coweta County), DRI #4727 | up to 1,500 (load request) | Overall 2034, no phase date. |
| Google White Oak / Project JGK (Columbia County, Appling), DRI #4736 | 1,400 | Only mass grading (LDP, "2027 est.") is dated; $17bn MOU 2026-08-26 (Kinetic Infrastructure Solutions = Alphabet); no COD. Largest dated-pending item in GA. |
| Eatonton 379 (Putnam County) | 520 | Completion 2031. |
| Canoochee River (Candler County) | 500 | Completion 2033. |
| DataBank Project Indo (Bartow County) | 200 IT (288 utility) | ~2032. |
| 75 South (Spalding County), DRI #4607 | 450 | DRI review completed Feb-2026 with completion 2030, but MTJP lists it as Withdrawn (Griffin Daily News). Not rowed: conflict. |
| Microsoft Douglasville (4 × 245k sq ft; Baxtel B1-B3 2027, B4 2028) | not published | No MW. |
| Microsoft Palmetto (2027/2028), Project Rita Tyrone (2028/2029), ATL50 Union City (DRI #4843, 910k sq ft, 2031-32) | not published | ATL50's DRI MW field is "*". |
| AWS sites: River Park/Butts (12-14 bldgs; PILOT from 2027), Alcovy Rd/Covington (2027), Douglasville ATL114 (2028-30; EPD genset application 2026), Echo Rd (2027-29; no permits as of 2026-07), Lamar County (985-acre land bank), Rock House Rd ("In Doubt") | not published | No MW. A Georgia EPD genset narrative could give a gen-basis MW: next step. |
| QTS ATL2 East (Fayetteville), DRI #4603 | "TBD" | 2M sq ft, overall 2029. The Georgia Power IRP ~1,500 MW campus figure is still single-source. |
| Switch KEEP 2.0 Atlanta North (phase 1 online Q2-2026; two buildings UC; through 2030), Vantage Douglasville, Vantage South Fulton (DRI: Westlake Jan-2028, Stacks Rd Jan-2027), Meta Newton County AI campus | not published | No MW. |

**Nevada.** The gap stays large; there is no MW + date source for Switch.

| campus | MW | why not rowed |
|---|---|---|
| Switch Citadel B5 and B6 (2026), B8 (2029) | not published | Baxtel dates only; MW hidden. |
| Switch Core 2.0 Apex (2030-32) | not published | No MW. |
| Switch LAS 19 / EVO AI Factory | +115 (to 545 total) | No date. |
| Switch "Bighorn" | 300-360 | Proximo; no site or date. |
| Tract Silver Springs | 700 initial (under utility study) | No date. |
| Tract Peru Shelf park | up to 810 utility | Partly the Fleet rows. |
| Copia Monarch (Lyon County) | 500 gas gen | DC1 2028 (Baxtel); no per-phase MW. |
| AWS at Switch Citadel, Google Storey B4/East, Google Henderson III, Edged LAS01 (Q1-2028), Townsite Boulder City (2028-31) | not published | No MW. |
| NV Energy filings | – | 6 GW signed large-load agreements (~5 GW north); no per-customer MW. Large-load dockets of 2026-05-27 cover AWS (Sparks), Prologis, Novva and Fleet, with no MW. |

**Arizona.**

| campus | MW | why not rowed |
|---|---|---|
| Microsoft Goodyear PHX72-74 (2026-28), El Mirage PHX82/83 (2026-27), Dysart DC1-3 (2027+) | not published | No MW. |
| AWS Pecos Rd PHX065/066 (2026), Dobbins/Laveen (2028-32) | not published | No MW. |
| QTS PHX3 Glendale (16 bldgs, DC1 2027), QTS Hermosa Ranch (2028-34), Vantage AZ15/AZ3 (2028), Aligned PHX-07/08/09, CyrusOne Mesa (2027), EdgeConneX Mesa (2027), Google Redhawk 3 (2029) | not published | No MW. |
| EdgeCore Dobson Farms / Florence | 720 (tracker) | No date. |
| Tract Buckeye | 1,800 | Buckeye 1 dated 2027 by Baxtel, no MW. |
| Hassayampa 1.5 GW, Tonopah 1.0 GW, Marana 750, Davis-Monthan 500, Southwest Crossing 400 | as listed | No dates. |

**Louisiana.** AWS/STACK NW Louisiana is now $18bn with a third Shreveport site, still with no MW or phases.

**Missouri.**

| campus | MW | why not rowed |
|---|---|---|
| Crusoe Warrenton (2 × 805k sq ft; B1 UC 2027, B2 2029) | conflict, see below | Part of Meta's ~1.6 GW Crusoe deal (Childress + Warrenton, Bloomberg via Crypto Briefing 2026-06-19). |
| AWS Project Green / "Prairie Green" (STL100-103 UC 2027, STL104 2029, up to 17 bldgs to 2031; $10bn, up to $35bn per Baxtel) | not published | No MW. |
| Google Kestrel (5 × 500k sq ft; K1 UC 2028, K2 2029), Google Shale B3 (2027) / B4 (2028), which is probably KC East B3-B4 | not published | No MW. |
| Provident Gateway, Villa Ridge (13 bldgs, B1 2028) | not published | No MW. |
| Geronimo Jasper 400, Wildwood Joplin 200, Metrobloks Liberty 150 | as listed | No dates. |

## Source conflicts (for adjudication)

1. **Hyperion expansion basis and timing.**
   - The new row (3,000 MW basis unknown) is Meta's "5 GW compute capacity" minus its original ">2 GW". The P1 row is 2,064 MW **IT**, so the two rows may overlap or mix bases.
   - Timing conflicts:
     - Entergy: CCGTs in service 2030-31; the Evest ESA is conditional on the LPSC vote targeted 2026-12-16.
     - Citi (2026-07-01): "5GW+ by '30".
     - Round-1 news: full build ~2032.
   - Entergy calls it a second Evest data center; media call it the Hyperion expansion.
2. **Crusoe Warrenton MW.** Baxtel market page 200; Cleanview B2 450 (snippet); `themes/ai-compute-deals.md` house allocation 600 (0.3/0.3, labelled a Capstone estimate). Not rowed until you pick one.
3. **75 South, Spalding (450 MW):** DRI completed vs tracker "Withdrawn".
4. **Pegasus:** DRI 350 MW (KDC/PRL2) vs Thor 400 MW. Round-1 said the project "skipped DRI review"; PRL2 is a later DRI for the follow-on phase.
5. **Fleet/Tract mapping (NV).** Baxtel's "Fleet: Peru Shelf Tech Park" describes Fleet's maiden 197-month-lease project, the TRACTC deal, as sitting on **Peru Shelf**, not South Valley. This bears on the round-1 SV/PR mapping; no MW change.
6. **Delta Forge locations.**
   - FY26 10-K: Delta Forge land is in ND and Louisiana.
   - Q1 FY27 release (2026-10-07): DF1 is in Louisiana, DF2 in **Alabama**. This supports the AL Brookwood row.
   - DF1 timing: 8-K says initial ops "mid-2027"; 10-Q says "1H CY2027". The row uses the later filing.
7. **Campus MW conflicts.**

   | campus | used | alternative |
   |---|---|---|
   | NTT Mesa | 324 (NTT) | 360 (DCD) |
   | STACK PHX01 | 225 (STACK) | 150 (MTJP) |
   | Novva Mesa | 300 (Novva) | 96 (MTJP, likely phase 1) |
   | EdgeCore Mesa | 496 (EdgeCore) | 450 (MTJP) |
   | DC BLOX A | 2026 (Baxtel) | first capacity "as soon as 2027" (loan coverage) |

8. **Unverified MW.** NV-MCCARRAN-SWITCHCITADEL-B7 (118 MW) rests on a Cleanview search snippet that round 1 declined. Drop it if Cleanview snippets are not acceptable.

## Paywalled or blocked
- **Cleanview:** building pages paywalled; they redirect to the campus page.
- **HTTP 403 via urllib/WebFetch:** La. Illuminator / NewsFromTheStates, constructionreviewonline, Shreveport-Bossier Journal, Entergy newsroom and entergy-louisiana.com, The Augusta Press, DCD, roselawgroupreporter, edgeconnex.com.
- **Partial or failed fetches:**
  - Prime: 403 via urllib, but WebFetch worked.
  - newprojectmedia: urllib timed out, but WebFetch worked.
  - NTT bizwire mirror: SSL handshake failure.
  - Proximo deal page: paywalled.
- **Not attempted:** Georgia EPD permit narratives (genset MW for the AWS/Microsoft GA sites) and the LPSC docket U-37882 (in-service dates per unit).

## Georgia DRI data-center filings with MW (reference; https://apps.dca.ga.gov/DRI/Submissions.aspx)

| DRI | project | county | peak MW | completion | status |
|---|---|---|---|---|---|
| 4853 | Nixon Technology Center | Richmond | 600 | 2028-29 | rowed |
| 4689 | Project Arrowhead | Irwin | 1,250 | 2030 / 2034 | rowed |
| 4835 | Kingston Technology Hub (Thor) | Bartow | ~150 | 2030 | rowed |
| 4797 | PRL2 (Pegasus site) | Troup | 350 | 2029 | fix |
| 4860 | ATL80 (Microsoft) | Floyd | 422 | 2032 | fix |
| 4602 | Project Azalea | McDuffie | 400 | 2029 | already rowed in R1 |
| 4607 | 75 South | Spalding | 450 | 2030 | withdrawn per tracker |
| 4624 | Hampton Technology Park | Henry | 1,500 | 2033 | out of window |
| 4651 | QTS Blakely | Early | 1,500 | Q4-2035 | out of window |
| 4727 | Bridgeport | Coweta | ≤1,500 | 2034 | out of window |
| 4736 | Project JGK (Google White Oak) | Columbia | 1,400 | grading 2027 | no COD |
| 4735 | Project Squash | Columbia | 200 | LDP 2027 | no COD |
| 4761 | Project Indo (DataBank) | Bartow | 200 IT / 288 | ~2032 | out of window |
| 4846 | Canoochee River | Candler | 500 | 2033 | out of window |
| 4861 | Eatonton 379 | Putnam | 520 | 2031 | out of window |
| 4794 | Stillwater | Clayton | 1,250 | – | withdrawn |
