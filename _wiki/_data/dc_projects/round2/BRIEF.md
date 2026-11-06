# Round 2 brief (shared by all five lanes), 2026-11-06

## What this is for
We are building a bottom-up US data-center registry: one row per campus phase or building, with MW, city and expected energization date. It feeds a model of how much GW post-election state and local permit pauses delay in 2026-30 (TX TCEQ/ERCOT freeze, VA SB 843, GA/OH/NM governors, local moratoria).

Round 1 holds 283 rows, about 49 GW IT-equivalent. The benchmark it should approach is a reference deck on an Aterio base: **139.5 GW under construction, dated 2026-30**. Its state totals are TX 35.1, VA 17.8, OH 9.7, PA 6.5, IN 6.2, GA 6.0, MO 4.7, NV 4.6, LA 4.5 and AZ 3.8 GW (basis not stated). Registry GW by state today: TX 10.1, VA 3.6, OH 2.1, PA 1.9, IN 2.3, GA 1.1, MO 2.4, NV 0.9, LA 2.3, AZ 0.6. **Round 2 closes the largest gaps.** Rank your work by GW: a 1 GW campus with a sourced schedule beats ten 50 MW colo halls.

## Files
- Schema, mandatory, follow it exactly: `E:\Wiki Felipe empresas\_wiki\_data\dc_projects\SCHEMA.md` (header, enums, scope, rules).
- Existing rows: `E:\Wiki Felipe empresas\_wiki\_data\dc_projects\raw\*.csv`. Your lane names your region's file and the gap list in its `*_notes.md`.
  - Before adding a campus, grep ALL raw/*.csv for the campus, developer and city, so no phase is rowed twice.
  - Keep the project_id convention `ST-CITYSLUG-CAMPUSSLUG-PHASE`.
- Ramp format: `E:\Wiki Felipe empresas\_wiki\_data\dc_projects\ramps.json`.
- Epoch AI Frontier Data Centers CSVs: `C:\Users\FELIPE~1.MON\AppData\Local\Temp\claude\6b53237a23bdb163\925d1185-0ad2-4267-b570-de5a23fe14c0\scratchpad\epoch_dl\`. Round 1 already mined them; use them only to cross-check.

## Write ONLY to `E:\Wiki Felipe empresas\_wiki\_data\dc_projects\round2\`
- `<lane>.csv`: NEW rows. Header exactly as SCHEMA.md, UTF-8, RFC-4180 quoting.
- `<lane>_fixes.csv`: full replacement rows for EXISTING project_ids where you found better data. Same header; start the notes field with `R2 FIX: <what changed and why>`.
- `<lane>_ramps.json` (optional): ramps.json format, for a campus total that sources date only as a window.
- `<lane>_notes.md`:
  - rows added;
  - MW by state × cod year × mw_basis (never add across bases);
  - fixes made;
  - rows dated from Texas TDLR construction-completion dates (list their project_ids);
  - the biggest campuses still un-pinned, with their MW and why;
  - paywalled or blocked sources.

Do not edit anything else: no raw/, projects.csv, overrides.csv, rules JSON, wiki pages or git.

## Sources, in this order
1. **Wiki corpus.** Free; costs no web budget.
   - `py "E:\Wiki Felipe empresas\_wiki\_tools\search.py" [-t TICKER] [-k call,transcript,report,briefing,damnang] <query>` for full-text search over broker reports, calls, briefings and transcripts.
   - Grep `E:\Wiki Felipe empresas\_wiki\*.md`, `_wiki\themes\ai-compute-deals.md` and `_wiki\themes\*.md`.
   - Ticker folders hold SEC filings and transcripts (e.g. `E:\Wiki Felipe empresas\IREN\`).
2. **WebFetch on primary pages:**
   - company press releases and IR decks; EDGAR 10-Q / 8-K / S-1 text;
   - utility IRPs and large-load filings;
   - county and city agendas, rezonings and building permits;
   - state air-permit databases. Backup-generator permit-to-install filings give a facility size: record mw_basis `gen` and note "backup genset nameplate".
   - Georgia DRI filings.
   - Texas TDLR TABS project registrations. They give estimated construction completion: put that month in cod_base with cod_source `filing`, start the notes with `TDLR completion YYYY-MM-DD`, and list the id in your notes. Do NOT shift the date yourself; a +6-month energization shift is applied centrally.
3. **WebSearch.** HARD CAP: **35 calls** for your lane. Five lanes share one budget of about 200. If a search returns a cap or limit error, stop searching and write up what you have.
   - Trackers often 403 or sit behind paywalls: Baxtel, DCD, morethanjustparks, Cleanview, datacentermap. Note it and move on.
   - The machine is behind a TLS proxy and runs Python stdlib only. If urllib fails on SSL, use `ssl._create_unverified_context()`.

## Row rules (the model is only as good as these)
- Every row needs `source` (URLs or corpus paths relative to `E:\Wiki Felipe empresas`, `;`-separated) and `source_date`.
- **MW basis:** record the basis the source states (IT / facility / grid / gen / unknown). Never convert.
- **Permit status:**
  - never guessed: blank or `unknown` unless a source states it;
  - air_permit `n/a` = grid-only with ordinary backup gensets;
  - `pending` only if an application is on file;
  - interconnection `agreement` only if a signed ESA, LLIS or contract is reported.
- **Dates.** cod_base = expected energization on the latest pre-pause schedule.
  - Year-only sources: `YYYY-06` with cod_source `year_only`.
  - Never invent a date.
  - Campus total with a sourced first date AND a sourced window or end date: write one `-ALL` row dated at the first phase, plus a ramps entry. Even tranches are fine; say in "why" that the split is a Capstone estimate.
  - Only a first-phase date: row the first phase if its MW is sourced.
  - No date at all: NO row. List the campus in notes with its MW.
- **Scope:**
  - US; campus ≥100 MW, or ≥50 MW if part of a hyperscaler or AI-lab program;
  - cod_base 2026-01 … 2030-12, plus phases energized during 2026;
  - leave out phases energized before 2026 and campuses that are withdrawn, denied or voided (list those in notes).
- **likelihood** follows Aterio's tiers in SCHEMA.md.
- Put every conflict between sources in notes.
- lat/lon to 3 dp; use the city centroid if the site is unknown.
- `local_approval` + `local_approval_date` and `local_moratorium` matter for the model. Fill them when sourced: county rezoning, CUP or site-plan approval dates.
- as_of = 2026-11-06. Write in English.

## What to return (≤250 words)
- Rows added and fixes made.
- New MW by state and basis.
- The 3-5 biggest campuses still missing, with MW.
- Any source conflict I should adjudicate.
