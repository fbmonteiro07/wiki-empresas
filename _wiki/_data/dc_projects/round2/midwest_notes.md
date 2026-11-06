# midwest lane, round 2 (OH / PA / IN first, then IL / MI / KY / NY), compiled 2026-11-06

Files:
- `midwest.csv`: 10 new rows.
- `midwest_fixes.csv`: 4 replacement rows for existing ids.
- `midwest_ramps.json`: 8 ramp entries (7 for new rows, plus PORTS-Pike and Hawesville).

All files use the SCHEMA.md header. Duplicates were checked: every new campus, developer and city was grepped across all `raw/*.csv`, and no new id collides with an existing one.

Web budget: **30 of 35 WebSearch calls used**. The rest came from WebFetch of primary pages: EDGAR (SB Energy S-1/A, NiSource 10-Q, TeraWulf 8-Ks), PJM LAS utility submissions, AEP Transmission/OPSB filings and PA DEP permit files.

## Rows added (10)

| project_id | MW | basis | cod_base (source) | why it matters |
|---|---|---|---|---|
| OH-JEFFERSONVILLE-AWSFAYETTE-P1 | 480 | grid | 2027-07 (estimate) + ramp to 2029-01 | AWS Fayette Phase 1. AES Ohio PJM filing gives the MW. The date is re-anchored on AES's Sep-2026 zone forecast (see Conflicts) |
| OH-HILLIARD-AWSCOSGRAY-FC | 73 | gen | 2027-09 (filing) | AWS Hilliard expansion, bridged by 72.9 MW of AEP-owned Bloom fuel cells (OPSB 25-0649). Air PTIO issued, appealed to ERAC by the city |
| IN-NEWLEBANON-MERIDIAN-ALL | 430 | IT | 2027-07 (analyst) + ramp to 2028-02 | Fluidstack/Next Frontier, Google-guaranteed lease, $5.7bn notes (credit dossier) |
| IN-LEBANON-META-ALL | 1,000 | unknown | 2027-12 (company) | Meta VP to Reuters: online at the end of 2027 or early 2028. Front-loaded, no phasing public |
| IN-NWINDIANA-AWSNIPSCO-ALL | 2,400 | grid | 2027-01 (filing) + ramp to 2032-12 | NIPSCO–Amazon special contract. IURC approved Jun-2026. Sites undisclosed, so lat/lon is a proxy |
| IN-LAPORTE-MICROSOFT-ALL | 788 | grid | 2028-06 (year_only) + ramp to 2031 | NiSource 10-Q: capacity commitment from 2028, 788 MW from 2031. IURC filing pending |
| MI-VANBURENTWP-GOOGLECANNOLI-ALL | 1,000 | unknown | 2027-12 (filing) + ramp to 2028-12 | MPSC approved the DTE contracts 2026-10-01: service Dec-2027, maximum load Dec-2028 |
| KY-ASHLAND-TERAWULFMUSKIE-P1 | 500 | grid | 2028-09 (company) | Kentucky Power ESA. Ramps from 2H-2028. No tenant |
| KY-ASHLAND-TERAWULFMUSKIE-P2 | 500 | grid | 2029-06 (year_only) | Amended ESA moves this phase from 2H-2030 to 2029, subject to KY PSC approval |
| IL-JOLIET-JTC-ALL | 1,800 | unknown | 2027-12 (press) + ramp to 2035 | PowerHouse/Hillwood. Council approved 2026-03-19. Phased over a decade |

## MW by state × cod year × mw_basis (new rows; never add across bases)

**A. On each row's cod_base** (whole row on its first date):

| state | basis | 2027 | 2028 | 2029 | total |
|---|---|---|---|---|---|
| OH | grid | 480 | | | 480 |
| OH | gen | 73 | | | 73 |
| IN | IT | 430 | | | 430 |
| IN | grid | 2,400 | 788 | | 3,188 |
| IN | unknown | 1,000 | | | 1,000 |
| MI | unknown | 1,000 | | | 1,000 |
| KY | grid | | 500 | 500 | 1,000 |
| IL | unknown | 1,800 | | | 1,800 |

**B. Spread by `midwest_ramps.json` tranches** (this is what the engine will produce once the ramps are merged):

| state | basis | 2027 | 2028 | 2029 | 2030 | 2031+ |
|---|---|---|---|---|---|---|
| OH | grid | 120 | 240 | 120 | | |
| OH | gen | 73 | | | | |
| IN | IT | 287 | 143 | | | |
| IN | grid | 480 | 677 | 677 | 197 | 1,157 |
| IN | unknown | 1,000 | | | | |
| MI | unknown | 333 | 667 | | | |
| KY | grid | | 500 | 500 | | |
| IL | unknown | 300 | | 300 | 300 | 900 |

Inside the 2026-30 window, by basis, new rows add:
- **grid: 3.5 GW** (OH 0.48, IN 2.03, KY 1.0);
- **unknown: 2.9 GW** (IN 1.0, MI 1.0, IL 0.9);
- **IT: 0.43 GW** (IN);
- **gen: 0.07 GW** (OH).

## Fixes (4, in `midwest_fixes.csv`)

| project_id | change | MW effect (2026-30) |
|---|---|---|
| OH-PIKETON-PORTSPIKE-P1 | Replaced the 800 MW (unknown) row with the **whole campus: 8,024 MW IT**, 17 buildings of ~472 MW. Source: SB Energy S-1/A 2026-09-21, status "Not started", first-phase RFS 2028, final 2032. Ramp: 5 annual tranches 2028-32. Interconnection set to `study`, since only ~0.8 GW of gross load is contracted with AEP. The id is kept so the old row is replaced, not duplicated; consider renaming it to `-ALL` centrally | 800 unknown → 4,815 IT in 2028-30 (+3,210 IT in 2031-32) |
| PA-FALLSTWP-AWSKEYSTONE-ALL | MW was blank. Now **198 MW gen**: PA DEP plan approval 09-0261 (2025-07-25), 72 × 2.75 MW critical gensets. Row narrowed to phase 1, energized Jun-2026 (PECO). Phase 2 is unsized and its gas-genset permit 09-0261A is pending, so it is not rowed | +198 gen, 2026, energized |
| KY-HAWESVILLE-TERAWULF-JUSTIFIED | Basis unknown → **IT** (401 MW critical IT, WULF Q3). cod 2027-09 → **2027-12**, ramp to 2028-06 (Fluor EPC 8-K 2026-11-04: phased RFS from late-2027 through Q2-2028). Interconnection → `agreement` (KY PSC approved the ESA, Aug-2026) | 401 → 134 (2027) + 267 (2028), IT |
| PA-HOMERCITY-HCR-ALL | Tenant and notes only: Forbes, in EQT's 425 of 2026-11-05, says AWS "is erecting 36 buildings". cod stays blank | none |

**Rows dated from Texas TDLR completion dates:** none (no Texas rows in this lane).

## Utility-zone yardsticks (PJM LAS submissions for the 2027 forecast, Sep-2026)

These are grid-basis, contract-backed totals, useful for capping the rows. They are not project rows.

- **AEP**, cumulative adds 2027 / 28 / 29 / 30 / 31:
  - AEP Ohio: 4,980 / 7,459 / 9,623 / 13,900 / 15,574 MW (ultimate 17,116). This is the "17.9 GW signed" anchor.
  - I&M: 1,813 → 4,330 MW.
  - Kentucky Power: 33 → 533 (2029) → 1,033 MW.
- **AES Ohio (DAY zone)**, nine hyperscale customers:
  - 75 MW (2027), ~410 MW (2028, read from the chart), 1,820 MW (2029), ~3,750 MW (2030), 5,870 MW (2031), 6,485 MW (2033).
  - "No large-scale data centers currently operating" in the zone.
  - The customer list carries milestone MW of 1,500 / 500 / 135 / 400 / 300 / 1,400 / 800 / 1,300 / 300, anonymised.
- **PPL**, ESA/CSA capacity: 771 / 2,256 / 6,559 / 9,871 MW (2027-30); LOA load is added only from 2030. PPL said 6.5 GW is under construction (Q2-26, press).
- **PECO** (incl. in-service): 135 / 489 / 793 / 968 / 1,105 MW, 2027-31. This caps AWS Falls Twp phase 2.
- **ComEd** (incl. in-service): 2,070 / 3,379 / 4,919 / 6,286 / 7,670 MW, 2027-31.
- **Duquesne:** zero until 2031. Three projects (1,145 MW) are rated 9.5-27.5% probable.

## Biggest campuses still un-pinned (MW, and why)

1. **AWS Ohio, beyond Fayette Phase 1 and the Hilliard expansion.** Multi-GW; SemiAnalysis says Ohio becomes AWS's largest state outside VA by 2028.
   - **Beech Rd** (Licking, ≥1 GW): no MW or date; Cleanview's per-building data is paywalled. Its search snippet put "Building 8" at 76 MW / 2028, unverified.
   - **Smith's Mill** and **Miller Rd**: no MW or date found.
   - **Sunbury** ($2bn): the first building's construction is to start Jan-2028 and finish Dec-2034, so it is likely after 2029. A single unverified source reports a Sunbury council moratorium until Jan-2027.
   - **Marysville**: no MW or date found.
   - **Sidney** ($3bn tax break) and an **18-building campus near Cincinnati**: DCD returned 403.
   - **Fayette beyond Phase 1**: Cleanview says 800 MW / 2029.
   - **AEP LONs with unnamed customers**:
     - Green Chapel station (New Albany): 440 MW initial, growing to 1,560 MW.
     - Jorden station: 54 MW, growing to 270 MW, customer-requested in-service Nov-2026.
     - Neither can be attributed to a company.
2. **Homer City (PA): ~3.7 GW reserved for data centers** (Baxtel), AWS with 36 buildings (Forbes).
   - The only schedule found is an aggregator's four construction phases, Dec-2026 to Jun-2036. No energization date.
3. **AWS Salem Twp (PA) beyond building 4.** DCD has a 15-building / ~960 MW plan.
   - PA DEP approved 48 × 2.75 MW gensets in Jan-2026; an application for 86 more was filed Apr-2026.
   - The Talen PPA minimum ramp is 240 MW (mid-26) → 480 MW (mid-28) → 840-1,200 MW (2029) → 1.68-1.92 GW (~2032) (TLN Investor Update 2025-09-09). That is a supply ramp, so it is not rowed, to avoid double-counting Epoch's building rows.
4. **Google Monrovia (Morgan Co., IN): 1.2 GW** per Cleanview. Construction started Nov-2025, but there is no date or primary MW.
5. **Digital Realty Kokomo (IN): ~1 GW IT / ~1.5 GW power, completion 2033.** No first date.
6. **Cologix Johnstown (OH): 800 MW, 8 buildings.** COL7 is listed, with no dates.
7. **CyrusOne Sangamon Co. (IL): 600-634 MW.** County approved Apr-2026; first phase in 2027 per press, but the phase MW is not stated.
8. **Other Illinois sites:**
   - Equinix Minooka: 1.2 GW IT, phase 1 480 MW / 2027, from a tracker only.
   - Tract Morris: 1 GW, planned.
   - Aligned Cook County: 1.8 GW, TBD.
   - Compass Hoffman Estates: 200 MW, 2026, Cleanview only.
9. **Microsoft Licking County (Heath, Hebron, New Albany):** no MW; dates come from an unverified tracker.
10. **Smaller items, or items without size or date:**
    - Alphabet's NIPSCO contract (IURC approved Jul-2026): MW and site not captured.
    - Aligned Conesville: mid-2026 first capacity, no MW.
    - Aligned Sandusky NEO-01: 96 MW.
    - Project BOSC, Lima OH: 115 gensets, developer unnamed.
    - Cipher Ohio: 200 MW grid-approved, no schedule.
    - NorthPoint Hazle Twp: 15 buildings.
11. **Out of scope:** Edged Aurora (IL), 72 MW IT for CoreWeave, Q2-2027. The campus totals 96 MW, under the 100 MW threshold.

## Conflicts to adjudicate

- **AWS Fayette.** AES Ohio's 2024 filing ramps 65 → 480 MW between Sep-2026 and Sep-2027. AES's own 2026-09-21 submission says nothing is operating and the whole zone reaches only 75 MW by Jul-2027 and ~410 MW by Jul-2028. I re-dated the row (`estimate`) to Jul-2027 → Jan-2029. If you prefer filing-only dates, the alternative is the 2024 ramp, which is stale.
- **PORTS-Pike.**
  - The old 800 MW was utility gross load (grid basis); the S-1 figure is 8,024 MW IT.
  - First RFS "2028" / "early 2028" (S-1) vs SemiAnalysis's "first in NVDA FY2029".
  - Developer: construction not started (2026-09-08).
- **Muskie phase 2:** 2H-2030 (May-2026) vs 2029 (Oct-2026 amendment, pending PSC approval). 2029 is used.
- **Joliet.**
  - Dates: initial capacity "by late 2027" (Datacentres.com), construction to start early 2027 (ABC7), first sub-campus in 2028 (search summary).
  - Grid: the article says both ComEd and "MISO"; Joliet is in PJM.
- **Hawesville:** "2H27 first power" (Jul-2026) vs "late 2027 to Q2-2028 RFS" (Nov-2026). The newer one is used.
- **Meridian:** a reprint's "300 MW by Dec-2026" vs Fitch's first 65 MW hall in Jul-2027. Fitch is used.
- **Meta Lebanon:** basis of the 1 GW not stated. The whole campus is front-loaded on end-2027.
- **Hilliard backup gensets run hours:** Amazon says ~10 h/yr, Ohio EPA ~50 h/yr. The draft permit covers up to 158 gensets.

## Permit / moratorium items for the rules files

- **KY:** Governor Beshear's **Executive Order 2026-494** on data-center development. TeraWulf says Muskie will comply (8-K 2026-10-05). Not in the rules research; check it.
- **OH:**
  - Sunbury council moratorium until Jan-2027 (one GDELT item, unverified).
  - City of Hilliard's ERAC appeal of the Amazon fuel-cell PTIO (filed 2025-11-07, outcome not found).
- **MI:**
  - AG Nessel petitioned for rehearing of the Google/DTE approval (2026-10-30).
  - The Saline appeal at the Court of Appeals is still pending.
- **PA:** pending DEP genset plan approvals for Falls Twp phase 2 (09-0261A, 1,236 comments) and for Salem Twp (+86 gensets).
- **PORTS-Pike:** air permits for backup gens and for the 9.2 GW gas plants are not filed (S-1).

## Paywalled or blocked sources

- **DCD:** returned 403 on every article tried.
- **Cleanview:** MW, dates and permits are behind the paid plan.
- **Ohio regulators:** PUCO DIS rejected the request.
- **Indiana regulators:** in.gov/IURC refused the connection or timed out, so the IURC order 46322 was not read.
- **Michigan:** michigan.gov (the MPSC and AG releases) and Michigan Advance returned 403.
- **News sites:**
  - Reuters is blocked; the Meta Lebanon quote was read via the Spokesman-Review syndication.
  - The Star (Malaysia) returned 403.
  - Databid, idcnova and Hometown Stations returned 404.
- **PJM:** ftp.pjm.com did not resolve, but the same files on www.pjm.com worked.
- **FirstEnergy and Duke LAS slides:** their filenames were not found, so Homer City's Penelec-zone data was not checked.
