# Plains / Upper Midwest: DC project registry notes (IA, MO, WI, MN, NE, KS, OK, ND, SD)

Built 2026-11-06 for `raw/plains.csv` (schema v1, `SCHEMA.md`). There are **41 rows** covering 24 campuses, about **13.2 GW** in total: **1.5 GW energized in 2026**, **9.6 GW under construction** and **2.2 GW not started**. No row carries a cod_base after 2029.

## MW by state × phase_status × cod year

| state | phase_status | 2026 | 2027 | 2028 | 2029 | total |
|---|---|---:|---:|---:|---:|---:|
| MO | energized | 105 | - | - | - | 105 |
| MO | under_construction | - | 1,500 | 1,200 | - | 2,700 |
| MO | not_started | - | - | - | 120 | 120 |
| WI | energized | 369 | - | - | - | 369 |
| WI | under_construction | - | 400 | 2,616 | - | 3,016 |
| IA | energized | 79 | - | - | - | 79 |
| IA | under_construction | 535 | 859 | - | - | 1,394 |
| OK | energized | 315 | - | - | - | 315 |
| OK | under_construction | 100 | 82 | 1,000 | - | 1,182 |
| ND | energized | 150 | - | - | - | 150 |
| ND | under_construction | 575 | 550 | - | - | 1,125 |
| ND | not_started | - | - | 150 | - | 150 |
| NE | energized | 300 | - | - | - | 300 |
| NE | under_construction | - | 142 | - | - | 142 |
| NE | not_started | - | - | 158 | 1,000 | 1,158 |
| KS | not_started | - | 100 | - | - | 100 |
| MN | energized | 178 | - | - | - | 178 |
| MN | not_started | - | 150 | - | - | 150 |
| SD | not_started | - | - | 500 | - | 500 |
| **All** | energized / under_construction / not_started | 1,496 / 1,210 / 0 | 0 / 3,534 / 250 | 0 / 4,816 / 808 | 0 / 0 / 1,120 | 1,496 / 9,560 / 2,178 |

**MW basis mix. Bases are mixed and were never converted, so do not sum them without a haircut:**
- **IT:** 6,736 MW over 27 rows. Sources are Epoch AI, the Applied Digital 10-Q and Vantage's 902 MW.
- **facility:** 1,800 MW over 2 rows (Nebius ≥800 MW; Gage County low end 1,000 MW).
- **grid:** 1,720 MW over 3 rows (Google–OG&E ESA 1,000; Sioux Falls 500; Meta Beaver Dam/Alliant cap 220).
- **unknown:** 2,978 MW over 9 rows (Spade 1,200; Mica 700; Fighting Pike 455; plus others).

**Likelihood (MW):** high 7,972 · medium 3,512 · low 1,750.

**cod_source (MW):** analyst 3,612 · company 2,866 · year_only 2,338 · estimate 1,900 · press 1,795 · filing 722.

## Conventions used
- **Half-year and vague dates:** 1H → `-04`, 2H → `-10`, Q4 → `-11`, "early YYYY" → `-03`, "late YYYY" → `-11`. A year alone → `-06` with cod_source `year_only`, as the schema requires.
- **Epoch AI rows** (`cod_source=analyst`) carry Epoch's satellite-based IT-MW estimate per building. Epoch's dates for future buildings are its own projections.
- **Rows that put a whole campus at its first-phase date** overstate MW in the early year. Spread or haircut them in the engine:
  - `MO-KANSASCITY-GOOGLEMICA-ALL` (700 MW)
  - `MO-INDEPENDENCE-NEBIUS-ALL` (800 MW)
  - `OK-STILLWATER-GOOGLEOGE-ALL` (1 GW ESA that ramps over about 5 years to about 2031)
- **Capstone placeholder dates** (`cod_source=estimate`) are used where there is no public schedule:
  - **Mica:** Feb-2026 start plus 18–24 months, the schedule range Google gave KSHB.
  - **Spade:** announcement plus about 24 months.
- **Capstone arithmetic splits:**
  - **Lighthouse:** GS's 20/80 FY28/FY29 phasing applied to Vantage's 902 MW IT.
  - **Fairwater B2 and B3–B11:** derived from Epoch's cumulative curve.
  - **Polaris Forge 2:** a 50 MW initial tranche (300 MW ND target by YE26, less 250 MW live at PF1).
  - **Red Wolf Building 1:** 600 MW / 6 buildings.
  - **Teton Trinity phase 2:** 100 − 30 MW.
- **`local_approval=approved` without a date** is inferred from active construction or operation. Every other permit field comes from a source or is `unknown`.
- **Grid region is inferred from location** for the ND rows and is flagged in each row's notes.
- **Coordinates:**
  - Epoch building-footprint centroids where Epoch covers the site.
  - Otherwise the tracker's site pin.
  - Otherwise an approximate city centroid, flagged in notes: Mica, Nebius, Harwood, Tioga, KCK, St. Louis, Stillwater, Sioux Falls, Beatrice.

## Against the coverage yardsticks (not targets)

| state | yardstick (2026-30 under construction) | this file | gap / comment |
|---|---|---|---|
| MO | 4.7 GW (Aterio via Capstone deck 2026-11-06) | 2.7 GW under construction + 0.1 GW energized | The gap of about 2 GW is mostly AWS Project Green (no MW published), Google KC East B2–B4 and CRG Festus. |
| WI | about 2% of 139.5 GW, ≈2.8 GW | 3.0 GW under construction + 0.37 GW energized | Fairwater B3–B11 (1.5 GW) is an Epoch projection without a Microsoft date. |
| OK | about 2%, ≈2.8 GW | 1.2 GW under construction + 0.3 GW energized | Meta Tulsa, Beale Clydesdale/Mustang, Potentia Inola and further Pryor expansion have no MW. |
| IA | about 1%, ≈1.4 GW | 1.4 GW under construction | Close to the yardstick. |

The WI/OK/IA shares come from the brief. The deck text on disk (`relatórios bons/2026_11_06_amigo_felipe_gw_atrasa_pausas_estaduais.html`) only shows the top 10, which includes MO 4.7 GW.

SemiAnalysis (2026-11-01, `ai-datacenter-power.md`) puts Oklahoma at 2.1 GW of 2028 additions, 94% not started. Its basis is unstated, so do not net it against these rows.

## Biggest campuses not pinned down, and why

**Under construction, but no MW published (or no MW and no date):**
- **AWS Project Green, New Florence/Montgomery County MO.** $10bn, 1,000 acres; phase 1 has 8 buildings and phase 2 up to 13 (Ameren). No MW, no schedule.
- **Google KC East (Hunt Midwest) B2–B4.** No MW or date. Epoch only rows B1.
- **Meta Tulsa "Project Anthem" phase 1.** Ground broken April 2026; more than $1bn; 2028 target. Phase 2 rezoning was withdrawn. No MW.
- **Beale "Project Clydesdale"** (Owasso/Tulsa County OK) and **"Project Mustang"** (Claremore OK, up to 3 DCs in phases, approved 2026-05-18). No MW.
- **Beale "Project Pilot", De Soto KS.** $3.1bn; 2.9m sq ft; phase 1 (2 buildings) due 2028. No MW.
- **QTS New Century KS.** No MW.
- **Potentia Inola OK.** No MW.
- **Google Papillion NE B4/B5.** Shell nearly complete in May 2026. No MW.
- **Google Mills County IA, Meta Altoona expansion, Microsoft West Des Moines campuses.** No MW or date. The tracker shows "Campus IV" at 200 MW but gives no date.
- **Edged Council Bluffs IA.** About 200 MW, topped out. No date.
- **Kearney NE "Tech One Crossing"** (MARA/Worldwide Mission Critical). 368 MW; approved 2026-09-08; construction "soon". No COD.

**Proposed or large announcements with no COD, excluded rather than guessed:**
- **OK:** IREN Kiowa/"Emerald" (1.2–1.6 GW; IREN 10-K: early-stage) and IREN Woods County (1.6 GW). Sources may double-count these two. Also Project Thunderbird, Enid (3.3 GW); Chickasha (500 MW BTM); Frisco Gateway (500 MW).
- **KS:** Flint Hills, Emporia (1 GW, zoning approved Jul-2026); Digital Realty Astra North (600 MW); Cloverleaf Bluestem (600 MW); Alcove Osawatomie (500 MW); Quindaro "Yardbird" (200 MW); Google Barber County.
- **MO:** Cloverleaf Troy (500 MW); Geronimo Jasper County (400 MW); Wildwood Joplin (200 MW, under legal challenge); Metrobloks Liberty (150 MW); CRG Festus ($6bn, approved 2026-03-30, lawsuit); Google "Kestrel" (~$100bn per Wells Fargo relay).
- **IA:** COPT Van Meter (1 GW); APLD Adair (200 MW); Google Linn County/Duane Arnold (up to 6 DCs).
- **NE:** Sagebrush Hallam (1.7 GW).
- **ND:** Geronimo Harmony Township (540 MW).
- **MN:** Cielo Chisago (300 MW); CloudHQ Carver (180 MW).
- **WI:** Microsoft Kenosha (early planning; residents seek a pause); QTS Madison (15 buildings, inside Dane County / City of Madison moratoria); Janesville; Vantage/Cloverleaf additional Port Washington acreage.

**Moratoria that touch rows or gaps:**
- **Gage County NE, 12 months.** Covers the Google/Tenaska row.
- **Independence MO, 180 days on new projects.** Nebius was approved before it.
- **Linn County IA, 18-month rural pause.** Does not cover the Cedar Rapids rows.
- **Fairfax IA ban.** Relevant to the Morgan Valley gas plant that would serve the Google/QTS Cedar Rapids sites.
- **Tulsa city (March 2026) and Broken Arrow (6 months) OK.** Affect Meta Tulsa and other gap projects.
- **Oliver County ND, 180 days.** Repealed April 2026 for Polaris Forge 3.
- **Others:** Sedgwick, Harvey and Shawnee/Topeka KS; Otoe, Cass, Logan and Seward NE; St. Charles and St. Joseph MO; several Iowa counties; Dane County and Madison WI. Moratorium list: tracker below.

## Source caveats
- **Corpus is thin for this region.** `search.py` hits were limited to:
  - the ORCL Q4 FY26 transcript (Port Washington)
  - the AI-credit workbook dossiers (APLD / PFORGE / ELNFOR: `_wiki/_data/credit_workbook.json`, `_briefings/2026/2026-10-16-ai-credit-live-workbook-dossiers.md`)
  - `_wiki/ORCL.md` (MS Credit 2026-09-30, GS 2026-10-22, Barclays)
  - `_wiki/MSFT.md` (Fairwater 2028)
  - `_wiki/GOOG.md` (Kestrel/Mica relay)
  - `_wiki/IREN.md` (Kiowa)
  - the NBIS filings and transcripts
  - SemiAnalysis 2026-11-01

  `search.db` returned "database is locked" during parallel runs.
- **Epoch AI Frontier Data Centers** (directory pages updated Jun–Oct 2026) gives satellite-based IT-MW estimates, not company disclosure. It is the backbone for the Google, Meta, QTS and Microsoft building splits.
- **morethanjustparks.com tracker ("Public Lands Intelligence", read 2026-11-06)** was used for discovery, status and MW quotes. Where possible MW was traced to the tracker's cited source. Its "Under construction" labels are not always confirmed: Spade's comes only from the tracker. **missouridc.pages.dev** is an opposition-run tracker (it carries a petition tool), last updated 2026-05-03. It was used only for corroboration.
- **The session's shared WebSearch budget ran out midway.** Later facts came from direct fetches of known URLs. DCD, Axios, Wisconsin Watch and FOX4 block scripted fetches, so some DCD facts (Teton, Scannell, Red Wolf 600 MW, Edged) are quoted from the tracker's excerpts of DCD.
- **Stale sources:** Sioux Falls (2025-08-07) and Red Wolf (2025-11-09) have no 2026 confirmation.
- **Fighting Pike, Williston ND:** completion in Aug-2026 is "expected" per KFYR, not confirmed. Earlier phases may predate 2026, and AI vs crypto use is not stated.
