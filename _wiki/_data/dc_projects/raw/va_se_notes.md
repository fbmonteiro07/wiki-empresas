# va_se: VA / MD / WV / NC / SC / DE / DC, raw registry rows (compiled 2026-11-06)

File: `raw/va_se.csv` (header exactly as in SCHEMA.md v1). **61 rows**: VA 39, MD 6, WV 3, NC 9, SC 4. There are no rows for DE or DC (reasons under Gaps).

## MW by state × phase_status × cod year

⚠️ **The table mixes MW bases. Do not net the totals against any GW series without the basis table below.** A `0*` marks a row with blank MW. `undated` means a blank cod_base (14 rows; see Flags).

| state | phase_status | 2026 | 2027 | 2028 | 2029 | 2030 | undated | total MW | rows |
|---|---|---|---|---|---|---|---|---|---|
| VA | energized | 550 |  |  |  |  |  | 550 | 8 |
| VA | under_construction | 180 | 1,888 | 436 |  |  | 1,844 | 4,348 | 24 |
| VA | not_started |  | 36 | 302 | 562 | 452 |  | 1,352 | 7 |
| MD | under_construction | 326 | 285 |  |  |  |  | 611 | 5 |
| MD | not_started |  |  | 48 |  |  |  | 48 | 1 |
| WV | under_construction |  | 460 |  |  |  |  | 460 | 1 |
| WV | not_started |  |  | 910 |  |  | 785 | 1,695 | 2 |
| NC | energized | 65 |  |  |  |  |  | 65 | 2 |
| NC | under_construction |  | 500 | 65 |  |  | 0* | 565 | 5 |
| NC | not_started |  |  | 0* | 200 |  |  | 200 | 2 |
| SC | energized | 69 |  |  |  |  |  | 69 | 1 |
| SC | under_construction | 60 | 201 |  |  |  |  | 261 | 2 |
| SC | not_started |  |  | 201 |  |  |  | 201 | 1 |
| **all** | | 1,250 | 3,370 | 1,962 | 762 | 452 | 2,629 | 10,425 | 61 |

## mw_basis mix (MW, row count)

| state | IT | facility | grid | gen | unknown |
|---|---|---|---|---|---|
| VA | 1,126 (9) | 248 (3) | 1,200 (4) |  | 3,676 (23) |
| MD |  |  | 395 (2) |  | 264 (4) |
| WV | 1,370 (2) |  |  | 785 (1) |  |
| NC | 65 (2) | 65 (1) | 300 (1) |  | 400 (5) |
| SC | 129 (2) | 402 (2) |  |  |  |
| all | 2,690 (15) | 715 (6) | 1,895 (7) | 785 (1) | 4,340 (32) |

- **IT** comes from Epoch AI satellite rows (QTS Richmond, Google Bristow/Arcola, STACK NVA02, Meta Aiken, Core Scientific Marble), Nscale's S-1 (Monarch), EdgeCore's "critical IT" (Culpeper) and the DCD "critical load" for ODATA.
- **grid** is a substation or utility-load figure: CleanArc ("900 MW of grid capacity"), PowerHouse substations, Rowan/Quinbrook "utility load", and PowerHouse Charlotte "secured power".
- **facility** is Cleanview "power capacity", which Cleanview defines as the electricity a campus is built to draw from the grid.
- **gen** is the 785 MW gas plant at Ridgeline. It is generation nameplate, not data-center load.
- **unknown** covers the developer headlines that give no basis (Amazon campuses, Vantage, STACK STC, Digital Realty Charlotte, MTJP "announced" MW).
- Likelihood mix: high 4.07 GW, medium 3.93 GW, low 2.43 GW.
- cod_source mix: year_only 26, blank 14, analyst 9 (Epoch AI), company 8, filing 2, press 1, estimate 1.

**Against the yardstick.** An Aterio-based deck puts ~17.8 GW of Virginia campuses under construction with energization dated 2026-30. The VA rows here sum to ~6.25 GW on mixed bases, and that includes not-started phases (about 35% of the yardstick at face value). NC rows sum to 0.83 GW against ~4.2 GW (3% of 139.5 GW). WV rows sum to 2.2 GW, of which 0.79 GW is the gen-basis Ridgeline row, against ~2.8 GW. The deck's basis (IT vs facility) is unstated, so these ratios are indicative only.

## Flags the merger should read

- **Allocated MW: 16 rows, every note starts or contains "ALLOC:".** The source gave a campus or phase total but no per-building MW, so Capstone split it evenly or by square footage:
  - Cosner ×4 (450 MW by 2029 less 75 MW B1, over 6 bldgs)
  - Lake Anna ×3 (≥420 MW over 7 bldgs)
  - STACK STC B1 (">1 GW across 19 data centers" ÷ 19)
  - Vantage VA4 B1 (192 MW ÷ 3)
  - Aligned IAD04 ×3 (264 MW less IAD-06 72 MW, ÷ 4)
  - Rowan Bauxite II/III ×2 (395 MW split by sq ft)
  - Digital Realty Charlotte ×2 (400 MW ÷ 2)

  Drop or re-weight these rows if allocations are unwanted.
- **Subtraction-derived MW** (stated totals minus stated parts):
  - QTS Richmond and Google Bristow increments (Epoch cumulative series)
  - Marble hall 3 (65 − 36)
  - Monarch B2-B3 (1,370 − 460 IT)
  - PowerHouse 95 P2-3 (800 − 300)
  - Iron Mountain remainder (200 − 48)
- **Undated (cod_base blank), 14 rows.** Most are MTJP "under construction" listings with announced MW and no schedule: ODATA 250, TA Realty Leesburg 430, Aligned Ashburn 180, PowerHouse Arcola 120, EdgeCore Ashburn 114, Aurora AI Factory 96, Village Place 210, STACK Loudoun Digital Campus II 144, and PowerHouse/Chirisa Chesterfield 300. The rest are Google Botetourt, Google Chesterfield "Peanut", Microsoft Chase City, Microsoft Hickory and Fundamental Data Ridgeline. The engine needs a default for these. Almost all are already under construction, so they very probably fall inside 2026-30.
- **No MW, 6 rows:** Google Botetourt, Google Chesterfield, Microsoft Chase City, Microsoft Conover, Microsoft Hickory, Compass Statesville. Hyperscalers disclose no MW, and Google and APCo cite an NDA.
- **One `estimate` row:** Microsoft Lyle Creek (Conover). Groundbreaking was 1Q26 (SemiAnalysis X post, 2026-05-07 briefing). Adding Aterio's "16 to 18 months from breaking ground" (GS call, 2026-10-20) gives 2027-09.
- **Epoch AI rows** are satellite-based. Some dates are Epoch assumptions, not observations: QTS Richmond 2 B5, QTS Richmond 3 B2-B3 and B4-B5, Meta Aiken B2 (Meta's own guidance is "spring 2027"), and STACK NVA02's "all 6 AI buildings by Jan-28". Dataset: `epoch.ai/data/data_centers/data_center_timelines.csv`, accessed 2026-11-06.
- **Year-only dates** (`YYYY-06`, cod_source `year_only`) come mostly from tracker building years (Baxtel, Cleanview). "Early 2028" for EdgeCore Culpeper is entered as 2028-03 with cod_source `company`.
- **Permits:**
  - `air_permit` is `n/a` for every grid-only row.
  - Monarch is `pending` 2026-04, from Cleanview's "DEP construction permit application filed April 2026". This is unverified and is probably the WVDEP R13 air permit.
  - Ridgeline is `issued` 2025-08. The Air Quality Board upheld it on 2026-02-05, and an appeal is pending at the WV Intermediate Court of Appeals.
  - `local_approval` is set only where a source states it: CleanArc ("fully permitted, approved site plan"), Cosner rezoning 2023-10, Stevensburg rezoning 2022, Mattameade partial 2023 rezoning, Digital Realty Charlotte RZ 2024-144 approved 2025-05, Compass Statesville 2025-09, Google Peanut (heavy-industrial zoning since 1966), and QTS York (county-approved). Energized rows are marked `approved` because they are operating.
  - Everything else is `unknown`.
- **local_moratorium is blank on every row.** No row is covered as far as the sources show:
  - **Loudoun.** On 2026-09-15 the Board voted 7-1-1 to consider a resolution pausing *final Board votes on legislative* data-center and substation applications for up to 12 months, retroactive to 9/15. Administrative processes are unaffected. Adoption was deferred to the **2026-11-17** meeting (loudoun.gov AID=10874; WJLA/DCD). Separately, grandfathering covers 15 projects (30 bldgs, ~10.5M sf) with site plans accepted by 2025-02-12, protected to Feb-2028. On 2026-10-06 the Board tabled its repeal (credit-workbook dossier, `_briefings/2026/2026-10-16-ai-credit-live-workbook-dossiers.md`). That list is not public, so it is not mapped to rows.
  - **Frederick County, MD.** The County Executive paused new data-center applications to **2027-07-01**, exempting approvals granted before 2025-06-17, so Aligned and Rowan are not covered. Quantum Maryland is suing over the freeze (technical.ly; WYPR 2026-09-15).
  - **Prince George's County** passed a 2-year moratorium (Jul-2026). Montgomery and Baltimore County have pauses and Baltimore City a 1-year one. None of these has a row.
  - **Chesterfield.** MTJP lists a county moratorium on *new* applications. The Chesterfield rows are existing projects.

## Biggest campuses not pinned down, and why

**Virginia.** Most of the gap to ~17.8 GW is here.
- **Undated remainders of large campuses**, where no per-building MW or schedule is public:
  - QTS Richmond: Cleanview 2,054 MW full build-out against ~0.6 GW IT that Epoch dates.
  - Digital Realty Digital Dulles: "another gigawatt" (DCD); Cleanview 1,723 MW. Only B7 and B10 are dated.
  - CloudHQ LC South: 1,310 MW under construction (Cleanview); LC8 due 2027, MW unknown.
  - STACK STC: 1.1 GW through 2036; only B1 is dated.
  - Amazon Northeast Creek (Louisa): 700 MW under construction per Cleanview, but MTJP and Baxtel report an Amazon Louisa campus *withdrawn*. Not added because of the conflict.
  - CloudHQ Manassas Corporate Center: 535 MW (Cleanview).
  - Corscale Gainesville Crossing: 228 MW remaining.
  - Vantage VA4 B2-B3: 128 MW.
- **Hyperscaler self-builds with no public MW or date:**
  - AWS: us-east-1 C3 Leesburg, C5 Chantilly, Ashburn IV, Light Speed Plaza, Potomac Church (Stafford), Manassas II (250 MW, MTJP), Wellington Glen (200 MW proposed), and Devlin Tech Park, Bristow (269 ac bought late-2025 for $700m; Baxtel first build 2027; zoning status conflicting).
  - Microsoft: Bristow, Hansen Farm, Jacksonville Rd, Boydton Phase 11, and the Jun-26 filing for 3 bldgs on 490 ac next to AVC17. LYH04 shows as 87 MW / 2026 in a tracker snippet whose URL could not be confirmed, so it was not added.
  - Google: Chesterfield "Project Skye" (rezoned May-25) and a Loudoun expansion (80 MW, MTJP, possible overlap with Arcola).
  - Meta: the Henrico expansion (475 ac bought 2022).
  - QTS Ashburn mega campus and QTS Henrico.
- **Proposed, with no COD. This is the pipeline most exposed to SB 843 (Jul-27 to Jul-30), and none of it has a row:**
  - Google West Creek, Goochland, 1,200 MW: due diligence; 4 Dominion engineering LOAs in a Jul-26 SCC filing; no plans submitted.
  - Dahlgren West, King George, 1,200 MW.
  - EdgeCore Shannon Hill, Louisa, 1.1 GW: Phase II Army Corps filing.
  - TAC Wythe, 1,000 MW.
  - Tract Tuckahoe, Goochland, 900 MW: CUP filed Aug-26.
  - Haven Oak, Dinwiddie, 900 MW.
  - 300 MW each: Appomattox, Province Powhatan, SDC VA-04 (PW), CloudHQ PW, TECfusions Clarksville.
  - 200 MW each: DigitalBridge Spotsylvania, Route 58 East (Pittsylvania).
  - Amazon King George (Birchwood): one building of 144 MW; stalled in county litigation as of Mar-26.
  - Wilderness Crossing, Orange (2,600 ac): Cleanview shows 1,500 MW / "2027", but the rezoning is in litigation.
- **Dead or withdrawn, excluded:**
  - PW Digital Gateway: rezoning voided Aug-25, upheld on appeal 2026-03-31; QTS withdrew its Supreme Court of Virginia appeal 2026-07-02. This matches Aterio's "QTS project getting withdrawn in Virginia" (GS call 2026-10-20).
  - Balico, Pittsylvania: denied Apr-25.
  - Hunting Hawk and Mountain Road (Tract), Hanover: 900 MW each, withdrawn or canceled.
  - Gigaland, Fauquier: 800 MW.
  - Ryan Road, Loudoun: 780 MW.
  - STACK Bristow campus: rejected Sep-25.
  - Amazon Bridgefield (GWU land, Ashburn): withdrawn. This confirms the CleanArc CCO relay on the AMZN page (2026-10-23).

**Maryland.**
- The rest of TPG's Quantum Frederick park (2,100 ac; the developer is suing the county over the freeze).
- Lerner's Landover campus in Prince George's County (820 MW in a 2024 presentation), now under the 2-year moratorium.
- AWS's own Maryland buildings beyond Rowan Bauxite I (231 MW, delivered late-2025, so out of window).

**West Virginia.**
- Starwood "Project Tamarack", Mason County: 2.16 GW from the grid, certified 2026-09-03, no schedule.
- Penzance Bedington, Berkeley County: 600 MW IT, the first "high impact" certification (2026-02-26), no timeline.
- Monarch's expansion to 8 GW gross (2031, outside the window).
- Ridgeline: undated.
- Cleanview counts 0 WV buildings under construction (32 planned), although Monarch shows earthmoving. It is a tracker lag.

**North Carolina.**
- Amazon Blue Marlin, Richmond County: 20 bldgs, $10bn. Only one building is dated (Cleanview: 65 MW, 2028; others 2029 and 2032).
- Microsoft: Maiden and Newton (rest of the $1bn Catawba plan) and the Person County Mega Park (1,350 ac).
- Natelli, Vance County: 900 MW site plan.
- Compass Statesville MW. Duke signed Microsoft and Compass power deals (Feb-26) that took its data-center contracts from 3 to 4.5 GW, but the sites were not named.
- Google Lenoir expansion; T5 Kings Mountain.

**South Carolina.**
- Google Berkeley County (Moncks Corner) and Dorchester expansions. No data was gathered because the search budget ran out.
- QTS York Phase 3: DC7-DC9, ~201 MW, undated.
- Cleanview counts 7 campuses under construction in SC but names only QTS York and Meta Aiken.

**Delaware.** Starwood "Project Washington", Delaware City, 1.2 GW: Technical.ly says it is "not moving forward as proposed", and a tracker lists it canceled as of Jul-26. There is no county vote or developer statement, so no row.

**DC.** No qualifying (≥100 MW) project was found.

## Aggregate context (not rows; do not add to row totals)

- **Dominion, Q3-26:** 54.9 GW of data-center capacity "in various stages of contracting", of which ~12.2 GW is under electric service agreements, up 6.3 GW YTD. Sources: DCD; Zacks; the Q3-26 call.
- **Duke Energy:** data-center contracts of 4.5 GW, up from 3 GW, in the Q4-25 deck (Bloomberg 2026-02-10).
- **Tracker counts:**
  - Cleanview VA (2026-11-05): 846 buildings on 253 campuses; 125 buildings under construction, 363 planned.
  - MTJP VA (Nov-26): 358 facilities; 50 under construction, 107 proposed, 38 stopped or paused.
  - Cleanview under-construction buildings elsewhere: MD 8, NC 14, SC 10, WV 0.

## Source caveats

- **The web search budget ran out.** The per-turn WebSearch limit (200, shared across all agents in the turn) was reached after ~55 searches by this agent. Later fills used WebFetch on URLs already found. Not searched: Vantage/ODATA follow-ups, Google SC, Meta Henrico, Microsoft Person County, Natelli, T5, NOVEC loads. A follow-up turn could close these.
- **Thin corpus for this region.** Only these sources were usable:
  - CleanArc: UBS expert call, John Day, 2026-10-23.
  - Monarch: Nscale S-1, via `_wiki/NSCALE.md`.
  - Loudoun grandfathering: credit-workbook dossier, 2026-10-16.
  - Microsoft self-build restart: SemiAnalysis X post in the 2026-05-07 briefing.
  - Build-time rule: Aterio @ GS, 2026-10-20.
  - The SemiAnalysis 11-01 "Backlash" file and the Barclays 11-05 DCD Connect Virginia file are image-only and were not mined.
- **Trackers are third-party:** Cleanview, Baxtel, MorethanJustParks (MTJP) and datacentermap.
  - Cleanview building pages are now paywalled. Cleanview MW and years were taken from search-engine snippets of earlier free versions.
  - MTJP project pages carry "announced" MW and no schedules. Several are flagged by MTJP itself as "not yet checked against source".
  - Baxtel building years are planning entries, not confirmed schedules.
- **DCD returned HTTP 403.** DCD facts came through search summaries or mirror pages (Construction Dive, Construction Owners, w.media, PR Newswire).
- **Conflicts** are noted on each row. The main ones:
  - CleanArc P1: May-27 (company, 10-23) vs 1Q27 (press) vs a tracker's "200 MW by 3Q26".
  - PowerHouse 95 first delivery: 2026 vs 2027.
  - Mattameade status: UC (Cleanview) vs proposed (MTJP).
  - Meta Aiken B2: Epoch Nov-26 vs Meta spring 2027.
  - Monarch B1: early 2027 (local press), 2H27 / end-27 (trackers), 1H28 (S-1, for the full 2 GW phase).
  - STACK NVA02: Baxtel shows F and G operational in 2026; Epoch shows only B1 operational at Feb-26.
  - Aligned Maryland: 4 bldgs (DCD) vs 5 (Baxtel).
- **Lat/lon** is a site pin where a source gave one (CleanArc, Corscale, Chirisa, STACK STC, Iron Mountain). Otherwise it is the city or town centroid (approximate).
