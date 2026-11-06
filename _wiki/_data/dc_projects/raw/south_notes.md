# South region — GA, AL, TN, MS, LA, AR, FL (raw/south.csv, compiled 2026-11-06)

**37 rows, 13.6 GW** (35 rows carry MW; 2 Amazon/STACK Louisiana rows have no public MW). By state: GA 13 rows, MS 9, AL 7, LA 4, TN 3, AR 1. **Florida has no rows.** No Florida project of 100 MW or more is under construction in the sources found; Florida's large projects are proposed, suspended or cancelled (see gaps).

## MW by state × phase_status × cod year

| State | phase_status | 2026 | 2027 | 2028 | 2029 | no date | Total |
|---|---|---|---|---|---|---|---|
| GA | energized | 343 | | | | | 343 |
| GA | under_construction | 400 | 528 | | | 633 | 1,561 |
| GA | not_started | 120 | | 3,200 | 400 | 422 | 4,142 |
| LA | under_construction | | 245 | | 2,064 | (1 row, no MW) | 2,309 |
| LA | not_started | | | | | (1 row, no MW) | 0 |
| MS | energized | 473 | | | | | 473 |
| MS | under_construction | 1,018 | 321 | 341 | | 320 | 2,000 |
| MS | not_started | | | 667 | | | 667 |
| TN | energized | 488 | | | | | 488 |
| TN | under_construction | 450 | | | | | 450 |
| AL | energized | 299 | | | | | 299 |
| AL | under_construction | | 505 | | | | 505 |
| AL | not_started | | | 210 | | | 210 |
| AR | under_construction | | | | | 150 | 150 |

**GW by state:** GA 6.05 (0.34 energized / 1.56 UC / 4.14 not started), LA 2.31 (all UC, before the 2 no-MW AWS rows), MS 3.14 (0.47 / 2.00 / 0.67), TN 0.94 (0.49 / 0.45), AL 1.01 (0.30 / 0.51 / 0.21), AR 0.15.

**Bases are mixed, so do not add MW across these columns without a basis conversion:** IT 16 rows / 5,596 MW · grid 5 / 4,600 · unknown 11 / 1,915 · facility 5 / 1,486. The grid basis is dominated by Camellia's 3,200 MW utility contract. The AWS Mississippi rows are facility basis because Epoch's IT series is chip-inferred and stays flat for the Canton B6-7 step.

**Against the yardstick** (Capstone deck on Aterio data: GW under construction with a 2026-30 energization date): GA ~6.0, LA ~4.5, MS ~3% of 139.5 (~4.2).
- **Georgia** UC + energized here is only ~1.9 GW. The 6.05 GW total is inflated by not-started Camellia (3.2 GW).
- **Louisiana** has 2.3 GW, plus Amazon's undisclosed MW.
- **Mississippi** has ~3.1 GW.
- **Context:** Georgia Power's own Q1-2026 filing (PSC Docket 55378, via Kadoa) shows 8,500 MW under construction across 31 projects and 12,400 MW committed. Those are utility-wide aggregates, not facility MW. **Most of Georgia's under-construction load is not pinned to named rows here.**

## Biggest campuses not pinned down (and why)
1. **Meta Hyperion expansion, 2 → 5 GW (LA, about +3 GW).**
   - Excluded: news puts full 5 GW at about 2032.
   - Entergy's 7 new CCGTs (5,278 MW) are in service 2030-31, and the LPSC decision is targeted for Dec-2026.
   - No phase dates exist. Meta's second north-Louisiana ESA (Evest LLC, Mar-2026) is also unsized.
2. **Amazon/STACK NW Louisiana, $12bn** (Caddo + Bossier). Rows exist, but there is no MW and no phase dates; operations are "in phases over the next several years".
3. **Georgia hyperscaler builds with no public MW or dates:**
   - AWS $11bn: River Park (Butts), Lithia Springs (Douglas), Covington (Newton), Lamar County.
   - Microsoft Douglas County campus (UC) and the Rome/Floyd 114-acre site (UC; separate from the 422 MW Huffaker Rd DRI row).
   - Vantage Douglasville (UC), DC Blox Atlanta West (UC), Meta Newton County AI campus.
   - The rest of the QTS Fayetteville full build. Georgia Power IRP testimony reportedly treats it as ~1,500 MW (single secondary source).
4. **Georgia proposed campuses with MW but no schedule** (secondary tracker only; not rows):
   - Project Arrowhead, Irwin County: 1.2-1.3 GW (DRI Apr-2026).
   - QTS Project Blue Hole, Early County: 1.0 GW.
   - Prologis Project Sail, Coweta: 900 MW ($17bn, 832 acres).
   - CyrusOne Project Peach, Coweta: 700 MW.
   - 600 MW each: Nixon Tech Campus (Richmond), Hogansville and Project West (Troup).
   - Eatonton 520 MW; Coosa/Atlas (Floyd) 504 MW; Project Springbank/Atlas (Bartow) 432 MW; T5 ATL IV, Fairburn 300 MW.
   - Social Circle 288 MW; Fort Gillem/Digital Realty 200 MW; Project Indo/DataBank 200 MW.
   - Not counted: Stillwater, Lovejoy (1.3 GW) is withdrawn.
5. **xAI/SpaceX Memphis-DeSoto items without MW and date:**
   - Project SPAM (started 2026-10-05, December target).
   - The new 312k sq ft building at 5414 Tulane Rd ($659m permit filed Mar-2026; Epoch Building 3 est. Feb-2027).
   - Olive Branch, MS 863k sq ft warehouse (liens).
   - A 474k sq ft Southaven building (SemiAnalysis 08-07: "~1GW of capacity or more").
   - The "Gun Range" MS plot.
   - FundaAI's "fifth site approved in September".
   - Macrohard's 700 MW TVA request; its identity versus Colossus II and MACROHARDRR is unresolved.
6. **Mississippi:**
   - AWS Vicksburg (Warren, UC, no MW).
   - Bloomberg's "$25bn Mississippi DC for Anthropic" (relayed 2026-05-15); it may overlap the Madison rows.
   - AVAIO Taurus later phases (~920 of 1,036 MW).
   - Echelon Meridian 500 MW and Corscale Canton 312 MW (proposed).
7. **Alabama** (all proposed): Project Marvel, Bessemer 1.2 GW; NorthPoint Wilsonville 1.0 GW; Childersburg 500 MW.
8. **Arkansas:**
   - Google West Memphis, Crittenden ($4bn, UC, MW undisclosed; Entergy Arkansas).
   - Apollo/Helena Harbor 1.0 GW and Grant County 800 MW (proposed).
   - Serverfarm Clarksville (UC, unsized).
   - The AVAIO Leo row has no date.
9. **Louisiana, other:**
   - Applied Digital Delta Forge 1. A tracker places "Delta Forge One" in Rapides Parish, UC; MW undisclosed.
   - Greenwood Road / Resilient Tech Park, Caddo (litigation).
   - Project Cayman, Ascension (ONE Nuclear, proposed).
   - SpaceX "Starbase Louisiana": SemiAnalysis says it could add >1 GW in 2027, but there is no site or basis.
   - Hut 8 River Bend optional +1,050 MW.
10. **Tennessee** (proposed): Cielo Clarksville 350 MW; Project MidSpan, Bradley 300 MW.
11. **Florida:**
    - Proposed: Fort Meade (Polk) 1.2 GW, Cielo Haines City 300 MW, Atlas Compute (St. Lucie) 240 MW, NextNRG Nassau 200 MW.
    - Sentinel Grove 1.0 GW is suspended. Project Tango 600 MW and DCIP Arcadia 300 MW are cancelled.

## Source caveats
- **The web-search budget ran out partway through** (cap of 200 per turn, shared across agents). After that, only direct fetches of known URLs and the corpus were used. Several fetches returned 403 (DCD, Arkansas Business, Effingham Herald, the OpenAI blog, Axios). Not searched: AWS Georgia MW, Microsoft Douglas, Google West Memphis MW, the MDEQ permit text, and AWS Mississippi expansions. A follow-up run with search budget could close several gaps.
- **Epoch AI rows** (cod_source `analyst`) are satellite and permit estimates; several are explicitly inferred or projected. The CSV is updated 2026-11-05, but the latest observations are mid-2026. "Energized" for Meta Montgomery/Huntsville/Gallatin, AWS Ridgeland and Dalton 1 is Epoch's inference, not company-confirmed.
- **morethanjustparks.com is a secondary lead list.** Many entries are marked "not yet read back against the source", and MW basis is usually unstated. Rows that rest only on it: Augusta/Eisenhower, Edged, Maysville, Dalton D3, AVAIO Leo, and the Brookwood MW.
- **Front-loaded rows** (one cod for a multi-year build):
  - Camellia: 3.2 GW put in 2028, though delivered 2028-32.
  - Pegasus: 400 MW site potential put at the end-2026 P1 date.
  - Union City: 324 MW at the 2027 first building; all three buildings are due by 2032.
  - Compass Meridian: 320 MW with no date, built through 2033.
- **Derived numbers:**
  - Colossus II Memphis 2026 adds: 401 MW = Arete 640 − Epoch 239.
  - Southaven T2: 1,018 MW = Arete's residual rising from 497 to 1,515 MW. Its Dec-2026 cod maps Musk's 09-25 GB300 tranches to Southaven (Capstone inference).
  - Brookwood = Applied Digital Delta Forge 2 is an inference (210 MW match).
- **Possible duplicates:**
  - Maysville/Northern Data vs Anthropic's "Rum Group" Georgia site (≤120 MW).
  - Epoch's chip-inferred Colossus 2 series may already include Southaven. Rows follow Arete's split instead.
- **Permit-field policy:**
  - air_permit is `n/a` only where a utility supply covers the load and no on-site generation is reported.
  - The Colossus II and Southaven rows carry the Southaven turbine plant's MDEQ status (`issued`, 2026-07). That rests on SemiAnalysis's "binding requirement signed July 30, 2026"; the MDEQ document itself was not read.
  - local_approval is `unknown` unless a source states it; energized rows count as approved.
- **Local pauses:**
  - Rows that carry a local moratorium: Fayetteville GA (ban on new DCs; Fairwater grandfathered), Birmingham AL (large-DC ban from Mar-2026; Nebius claims exemption), and Augusta-Richmond (listed, no dates).
  - Not in force: Caddo Parish Res. 53 (a proposed 2-year moratorium the parish attorney says cannot be enacted by resolution).
  - New Orleans (1 year) and Ascension (90 days) cover no row. Search found Ascension writing rules in Aug-2026 and "no company has proposed" a DC there, so the 90-day pause is unconfirmed by this run.
  - The tracker also lists Jackson MS and Memphis moratorium entries (unverified; no row inside Jackson city).
- **Election overlay is not applied in the CSV.** Bottoms' Georgia pause and the 3-2 Democratic PSC go in `state_rules.json`. Georgia rows with cod ≥2027 that are not yet approved are the exposed set: Camellia, Rome, Azalea, Rum Group and Union City's later buildings.
