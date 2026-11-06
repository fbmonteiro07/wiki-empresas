# midwest_ne: OH / PA / IN / MI / IL / KY / NY / NJ / New England, raw registry rows (compiled 2026-11-06)

File: `raw/midwest_ne.csv`, header exactly as in SCHEMA.md v1. It has **44 rows**: OH 15, PA 10, IN 9, MI 1, IL 1, KY 1, NY 4, NJ 3. New England has none (see Gaps).

The rows are built mainly on **Epoch AI's Frontier Data Centers dataset**, which gives satellite-dated, building-level IT and facility MW (`data_center_timelines.csv`, downloaded 2026-11-06). The wiki corpus supplies the credit dossiers (Saline, Elk Grove, Lake Mariner), the Williams Q2-26 call, and the NBIS, CRWV, ANTHROPIC, OPENAI and compute-deals pages. Primary or press web pages fill the rest.

⚠️ **The web-search budget ran out partway through.** It is a 200-call cap shared by every agent in the turn. After that, only direct fetches of URLs already in hand were possible. Indiana beyond Epoch's sites, most of Illinois, Michigan beyond Saline, Kentucky beyond Hawesville, upstate New York and New England were therefore **not researched on the web**. Treat those states as under-covered, not as empty.

## MW by state × phase_status × cod year

⚠️ **The table mixes MW bases** (see the basis table): mostly IT, plus 4,400 MW of gas *generation* at Homer City. `0*` marks a row with blank MW, `undated` a blank cod_base, and `(blank)` a phase_status that is not reported.

| state | phase_status | 2026 | 2027 | 2028 | 2029 | 2030 | undated | total MW | rows |
|---|---|---|---|---|---|---|---|---|---|
| OH | energized | 482 |  |  |  |  |  | 482 | 3 |
| OH | under_construction | 205 | 1,022 | 413 |  |  |  | 1,640 | 11 |
| OH | not_started |  |  | 800 |  |  |  | 800 | 1 |
| PA | energized | 30 |  |  |  |  |  | 30 | 1 |
| PA | under_construction | 31 | 153 |  | 2,000 |  | 4,400 (gen) + 0* | 6,584 | 6 |
| PA | not_started |  |  |  | 400 | 540 |  | 940 | 2 |
| PA | (blank) |  | 260 |  |  |  |  | 260 | 1 |
| IN | energized | 462 |  |  |  |  |  | 462 | 2 |
| IN | under_construction | 300 | 345 | 888 |  |  |  | 1,533 | 5 |
| IN | (blank) |  |  | 345 |  |  |  | 345 | 2 |
| MI | under_construction |  | 974 |  |  |  |  | 974 | 1 |
| IL | energized | 72 |  |  |  |  |  | 72 | 1 |
| KY | (blank) |  | 401 |  |  |  |  | 401 | 1 |
| NY | energized | 84 |  |  |  |  |  | 84 | 2 |
| NY | under_construction | 168 | 168 |  |  |  |  | 336 | 2 |
| NJ | energized | 50 |  |  |  |  |  | 50 | 1 |
| NJ | under_construction | 250 + 0* |  |  |  |  |  | 250 | 2 |
| **all** | | 2,134 | 3,323 | 2,446 | 2,400 | 540 | 4,400 | 15,243 | 44 |

Excluding Homer City's undated generation figure, **10.8 GW is dated in 2026-30** (OH 2.9 · PA 3.4 · IN 2.3 · MI 1.0 · KY 0.4 · NY 0.4 · NJ 0.3 · IL 0.07). 1.2 GW of that is already energized in 2026.

### Against the coverage yardstick

The yardstick is the Capstone/Aterio deck: GW under construction with a 2026-30 date. It is a rough comparison, not a target, and the bases are not stated in the deck.

| state | this file (dated MW, 2026-30) | Aterio yardstick | comment |
|---|---|---|---|
| OH | ~2.9 GW | ~9.7 GW | Big gap: AWS Ohio is almost entirely missing (see Gaps) |
| PA | ~3.4 GW, plus 4.4 GW gen undated | ~6.5 GW | Homer City data-center phasing and AWS Salem/Falls MW are the hole |
| IN | ~2.3 GW | ~6.2 GW | Only Epoch-tracked sites; web research stopped |
| IL | ~0.07 GW | ~2.8 GW | Essentially uncovered |
| MI | ~1.0 GW | ~1.4 GW | Saline alone; its grid contract is 1,383 MW |

## mw_basis mix (MW, row count)

| state | IT | facility | grid | gen | unknown |
|---|---|---|---|---|---|
| OH | 1,822 (13) | 300 (1) |  |  | 800 (1) |
| PA | 214 (4) |  |  | 4,400 (1) | 3,200 (5; incl. 1 blank-MW row) |
| IN | 2,340 (9) |  |  |  |  |
| MI | 974 (1) |  |  |  |  |
| IL | 72 (1) |  |  |  |  |
| KY |  |  |  |  | 401 (1) |
| NY | 420 (4) |  |  |  |  |
| NJ | 50 (2; incl. 1 blank-MW row) |  |  |  | 250 (1) |
| **all** | 5,892 (34) | 300 (1) | 0 | 4,400 (1) | 4,651 (8) |

Basis notes:
- Epoch IT is modelled from cooling, generator and permit evidence, not disclosed by the owner. Epoch facility MW runs at about 1.2-1.4x IT.
- **AWS New Albany (284 MW IT)** is Capstone arithmetic: Epoch's AI-only share (+125 MW) divided by its stated ~44% AI share. It is flagged in the row.
- **Homer City 4,400 = gas generation nameplate**, not data-center load. Never add it to IT rows.
- Saline is 974 MW IT (KBRA). Its DTE grid contract is 1,383 MW, which is not used as mw.

## Campuses I could not pin down

Ranked roughly by likely size.

1. **AWS Ohio (biggest hole).** SemiAnalysis (2026-11-01) says Ohio becomes AWS's largest state outside Virginia by 2028. Cleanview (2026-11-05) shows the campuses only as size bands, and its MW, dates and building detail are paywalled. DCD returned 403 and Aterio returned 429. Campuses:
   - AWS Jeffersonville, Fayette County: ≥1 GW, under construction, ~$5bn by 2030.
   - AWS Beech Road, Licking County: ≥1 GW, under construction.
   - AWS Smith's Mill Road expansion.
   - AWS Sunbury: $2bn.
   - AWS Marysville.
   - AWS Miller Road middle-campus buildings 10/12-14, seen operating 2026-03 but possibly energized in 2025.
2. **PORTS-Pike, the rest of OpenAI's first 4.25 GW** (~3.45 GW after the 800 MW row). The build-out runs to 2032 with no public phase dates. The developer said on 2026-09-08 that construction had not started, and no Ohio EPA air or OPSB generation filing had been made as of Aug-2026.
3. **Homer City (PA): data-center MW and phasing.** Only the 4.4 GW plant is rowed, with cod blank. Its air permit was issued 2025-11-18 and appealed. An AWS 36-building, four-phase (Dec-2026 to Jun-2036) filing appears only on an aggregator and is unverified.
4. **AWS Pennsylvania beyond Berwick B2-B4.**
   - Salem Twp has a 15-building / ~960 MW decade plan (DCD).
   - Falls Twp (Keystone Trade Center): phase 1 was energized Jun-2026, but there is no MW in any primary source. The Sierra Club cites 400-500 MW, unverified. The row is kept with blank MW.
   - SemiAnalysis puts AWS at ~44% of PA's 2.4 GW of 2028 adds.
5. **Other Ohio campuses without MW or dates:**
   - Google New Albany building 5 (Epoch: ~3 months to operation in May-2026, no MW) and its new 85-acre site.
   - Microsoft New Albany (Beech Rd), under construction per Cleanview.
   - Vantage New Albany outside the Prometheus buildings.
   - Cologix Johnstown: 800 MW / $7bn campus, first phase started 2025.
   - Aligned CMH-02 Conesville: first capacity targeted mid-2026, no MW.
   - Aligned Sandusky.
   - AEP Ohio had **17.9 GW of signed data-center contracts at Feb-2026**, which shows how far the rows undercount.
6. **Indiana beyond Epoch's sites:**
   - AWS northern-Indiana expansion beyond New Carlisle.
   - Google Monrovia (Morgan County, under construction per Cleanview).
   - Microsoft, Meta and other Indiana sites, plus the Hobart and Indianapolis-area projects, were not researched.
7. **Illinois:**
   - Compass ORD I, Aligned Elk Grove (Northwest Point) and the NTT Chicago expansion, which Cleanview lists as the largest under construction.
   - The Prime Elk Grove campus beyond ORD-01 (175-275 MW).
   - Edged Chicago (CoreWeave/Alibaba, 114 MW Chicago + Atlanta combined).
   - Microsoft and Meta DeKalb expansions.
8. **Michigan beyond Saline:**
   - The Google DTE contract that the MPSC approved Oct-2026 (site and MW not captured).
   - Lansing and Consumers Energy-area projects.
   - The Panattoni GW-scale site near Detroit.
9. **Kentucky:** TeraWulf's Muskie site has Kentucky Power service up to 1 GW but no data-center schedule. Bowling Green, Meade and Mason county proposals were not researched.
10. **New York:**
    - The Lake Mariner expansion (162 MW pipeline / 250 MW of extra power, subject to interconnection).
    - STAMP (Genesee County) and Massena were not researched.
11. **New England:** no ≥100 MW campus was identified, and the region was not researched after the search budget ran out.
12. **Other excluded or partial rows:**
    - CoreWeave Lancaster beyond building 1 (~200 MW): no date.
    - CoreWeave Kenilworth: 250 MW site, with only the first tranche ('tens of MW', 2026) rowed and MW left blank.
    - Archbald / Lackawanna cluster: PPL Archbald Mountain substation not before 2029-30, nothing under construction. Includes Project Gravity at 186 MW and a reported 1.6 GW largest site.
    - TECfusions Keystone Connect.
    - Pennsylvania crypto-site conversions.
    - **5C CMH01 Springfield, OH**: 75 MW total per Ideastream 2026-08-14, below scope. Its phase 1 is 25 MW. An older 200 MW figure conflicts with this.

## Permit / moratorium fields

- **Air permits found:**
  - Homer City: **issued 2025-11**, under appeal.
  - Meta Bowling Green, Apollo BTM 350 MW: **pending**. The Ohio EPA application was complete 2025-12-08 and the permit was still pending at 2026-02-03; later status not verified.
  - PORTS-Pike gas: **not_filed** as of Aug-2026. This comes from a search summary of the Mint newsletter and ICN, not a docket read.
  - Socrates South/North/Younger (Prometheus): OPSB case 25-0188-EL-BGN. The Ohio EPA permit was not verified, so these are left `unknown` even though Socrates South is in service.
- **Local approvals sourced:**
  - Saline: consent judgment 2025-10.
  - Fort Wayne: council resolution 2023-12.
  - Shippingport: conditional use 2026-03-31.
  - Vineland expansion: approved Aug-2026.
  - Salem Twp: rezoning, date not captured.
  - Everything else is `unknown`.
- **local_moratorium is blank on every row.** No rowed site was shown to sit inside a local moratorium. Moratoria known in the region:
  - Springfield, OH: 6-month moratorium on new hyperscale DCs from Jul-2026, plus a charter-ban petition for the Nov ballot.
  - Hazle Township, PA: Jul-26 to Jan-27.
  - Indianapolis: Aug-26 to Dec-27 (Capstone deck).
  - The state-level NY Executive Order 62 (Jul-2026) pauses discretionary DC permits. Lake Mariner's 10-Q does not say whether it affects CB-4/CB-5.
  - The PA governor's EO (Aug-2026) is state-level. Arete says it may delay Nebius Highridge by 1-2 quarters; the pre-pause cod is kept.

## Source caveats

- **Epoch AI** dates are estimates from satellite imagery plus a roof-to-operation rule of thumb. Where Epoch's date has passed but operation was not observed, the row stays `under_construction` with the past cod: New Carlisle B17-18, Berwick B3.
  - Prometheus B2-6 is dated to the 2026-01-18 image. Part of it may have energized in Dec-2025.
  - Fort Wayne B5-B6 and the Prometheus Vantage buildings are spacing extrapolations.
- **Front-loaded rows** put a whole campus on its first date because per-building MW is not public:
  - Aligned Project Phoenix: 2 GW at 2029-06. Baxtel has one of three buildings in 2030.
  - Saline: 974 MW at 2027-12, the DTE full-load date. KBRA says completions are staggered from Dec-2026 to Jan-2028.
- **Aggregators** (Cleanview, Baxtel, datacentermap) are used only for status and size bands, or are flagged as unverified.
- **Search-summary-only facts** are flagged in the notes: PORTS air/OPSB status, Bowling Green "FirstEnergy" utility, and the Falls Twp MW.
- **Location and grid fields:**
  - lat/lon are city or township centroids. Butler Twp (Schuylkill) and Falls Twp are approximate.
  - utility and grid are filled only where sourced or where the state lies wholly in one ISO (OH, PA, NJ = PJM; MI lower peninsula = MISO; NY = NYISO).
  - They are left blank for the Indiana and Kentucky sites.
- **Conflicts kept in notes:**
  - Vineland: 300 MW (SemiAnalysis/Nebius) vs 400 MW islanded (Barclays).
  - Lake Mariner CB-3 date: Epoch May vs company Jul-2026; company used.
  - Prime Elk Grove: 175 vs 275 MW campus.
  - Saline building count: 3 vs 4.
  - New Carlisle: Epoch 1,037 MW IT vs JPM ~910 MW vs expert 2.2 GW.
  - 5C Springfield: 75 vs 200 MW.
