# West region (AZ, NV, UT, WY, CO, OR, WA, CA, ID, MT): notes for `raw/west.csv`

Compiled 2026-11-06 from the wiki corpus plus the web. The file has **31 rows**, and coverage is thin: it falls well short of the Aterio yardstick in Nevada, Arizona and Utah. The cause is missing public schedules and the web-search budget (see "Source caveats"), not evidence that the capacity is absent. Rows were not padded to close the gap.

Rows by state: NV 6 · AZ 5 · UT 3 · WY 4 · CO 1 · ID 1 · MT 0 · OR 7 · WA 2 · CA 2.

## MW by state × phase_status × cod year (MW basis in brackets; do not add across bases)

| State | energized (2026) | under_construction | not_started | Total rowed |
|---|---|---|---|---|
| NV | – | 2026: 72 [IT] + 289 [unknown] · 2027: 539 [IT] | – | 900 |
| AZ | 157 [IT] | 2028: 286 [grid] · 2030: 156 [IT] | 2028: 700 [gen] | 1,299 |
| UT | – | 2026: 203 [IT] + 72 [unknown] | 2027: 101 [IT] | 376 |
| WY | 152 [IT] | 2026: 302 [unknown] · 2027: 1,800 [unknown] | 2027: 55 [IT] | 2,309 |
| CO | – | 2027: 70 [unknown] | – | 70 |
| ID | 152 [IT] | – | – | 152 |
| MT | – | – | – | 0 |
| OR | 77 [IT] + 144 [unknown] | 2026: 126 [unknown] | 2028: 145 [unknown] | 492 |
| WA | – | 2026: 288 [grid] | 2027: 57 [unknown] | 345 |
| CA | – | 2027: 48 [IT] · 2028: 48 [IT] | – | 96 |
| **West** | **682** | **4,299** | **1,058** | **6,039** (mixed bases) |

Energized rows are all dated 2026, between 2026-04 and 2026-08.

**mw_basis mix:** IT 15 rows / 1,760 MW · unknown 13 rows / 3,005 MW · grid 2 rows / 574 MW (Project Blue TEP agreement 286; Microsoft Malaga Chelan PUD contract cap 288) · gen 1 row / 700 MW (Project Baccara gas-plant nameplate). Facility: 0 rows. Wyoming's 1.8 GW Tembo row alone is 60% of the unknown-basis MW.

**cod_source mix:** analyst 16 (Epoch AI satellite estimates, Baxtel tracker quarters, the Barclays seed for Fleet) · year_only 9 · company 3 · press 2 · estimate 1. **Likelihood:** high 17, medium 14.

### Rows that hold a whole campus on one date (front-loaded)

Read these as upper bounds for the early year:

- **WY Tembo:** 1,800 MW sits on 2027-11, but the ramp runs to peak in 2030 (Black Hills 8-K, 2026-10-06).
- **WY Related Digital (CoreWeave):** the 302 MW campus maximum sits on 2026-11, which is the B1 date.
- **NV Vantage NV1:** 224 MW sits on 2026-05, which is the first-building date.
- **AZ Baccara:** 700 MW gen sits on 2028-06. The two buildings open in 2028 and 2030.
- **WA Malaga:** the 288 MW contract cap sits on 2026-03, the B1 date. B2 and B3 are "driven by customer demand".
- **AZ Stream Goodyear "REST":** 156 MW sits on 2030-01 and mixes under-construction and unstarted buildings.

## Coverage against the yardstick

The yardstick is the Aterio data in the Capstone deck: GW under construction with energization in 2026-30.

| State | Yardstick | Under construction rowed here | Shortfall |
|---|---|---|---|
| Nevada | ~4.6 GW | 0.90 GW | ~3.7 GW |
| Arizona | ~3.8 GW | 0.44 GW (plus 0.16 GW energized in 2026 and 0.70 GW gen not started) | ~3.4 GW |
| Wyoming | ~2% of 139.5 GW (~2.8 GW) | 2.10 GW | small; mostly Microsoft Cheyenne |
| Utah | ~1% (~1.4 GW) | 0.28 GW | ~1.1 GW |

The Aterio figure counts every dated phase on a campus where construction has started. Read it as an outer bound, not a target.

## Biggest campuses not pinned down, and why

### Nevada
- **Switch Citadel Campus (TRIC) and Switch "Bighorn".** Switch's site calls the Citadel a "Multi-Gigawatt Expansion". Davis Polk advised lenders on $4.5bn of Bighorn project finance in Nov-2024 (turnkey + powered shell, outside Reno). Proximo labels the deal 300 MW on its deal page and 360 MW in its text.
  - No building-level MW or dates are public. Switch press releases from 2025-26 name no campus, and the trackers (Cleanview, morethanjustparks) are paywalled or show no MW.
  - Search snippets cited Cleanview "Building 4 118 MW 2026" and "Building 7 118 MW 2028". Neither could be verified on the page, so they are not rowed.
  - The Switch Las Vegas Core is "up to 495 MW upon completion" (switch.com), with no schedule.
  - Switch is probably the largest single piece of the NV shortfall. This is an inference.
- **Tract parks beyond the two bond projects.** Baxtel lists Peru Shelf / South Valley Technology Parks, Virginia Highlands 1 (planned) and Virginia Highlands Expansion (land bank), with no MW or dates. The Fleet SV/PR rows may overlap Baxtel's Peru Shelf (200 MW, Q4-2026) and South Valley (170 MW, Q1-2027) entries. Those were not double-rowed.
- **Others without schedules:**
  - Microsoft North Ridge / East Valley (TRIC land bank)
  - Apple Reno (land bank parcels)
  - Google Storey County B4 (foundation 2026-04, Epoch) and Google Henderson
  - EdgeCore Reno B2-B3 (2 × 72 MW, undated)
  - Copia Power Monarch DC1/DC2 (planned)
  - CleanArc's Las Vegas JV (early stage; UBS expert call 2026-10-23, corpus)
  - Apex/North Las Vegas 432 MW (a JLL land listing with power in 2029-30, not a project)
- **NV Energy.** The 2026 IRP says almost all signed large-load agreements are in northern Nevada. The Tract dossier cites about 22 GW of requested service. No named-customer MW table was reachable: the PUCN docket was not read, and Nevada Current returned 403.

### Arizona
These come from the Arizona fork's gaps.
- **Microsoft Goodyear B5-B6.** Foundations were seen 2026-04-27 (Epoch), with no MW. B1-B4 (202 MW IT) were energized before 2026.
- **Microsoft El Mirage.** No MW was found.
- **EdgeCore Mesa.** EdgeCore's site says 496 MW critical IT across 5 buildings. About 290 MW is left after the 206 MW commissioned by May-2025, with no split or dates.
- **Prime PHX01 B1-B3 (Avondale).** 144 MW IT, groundbreaking 2026-05-21, hyperscaler-leased. The row was dropped because Prime released no timeline and the schema needs cod_base. Add it once a date appears.
- **Trackers only, no per-building MW:** Compass Goodyear/El Mirage and Vantage AZ.
- **GW parks with no tenant or dates:**
  - Tract Buckeye 1.8 GW
  - Hassayampa Ranch 1.5 GW
  - La Osa (Eloy), cut to ≤1 GW
  - Ryan Southwest Crossing 400 MW
- **Corrections to the context.** SemiAnalysis (2026-11-01) has Arizona adding 2.6 GW in 2028, 91% of it not yet under construction, so most AZ capacity probably sits in unstarted phases these rows cannot see. The "$14bn Goodyear withdrawal" in the water theme was Tract's 2024 application, not a 2026 event.

### Utah
- **Meta Eagle Mountain.** B1-B2 (133 MW IT) were energized around 2025-12 (Epoch), so they are out of scope. Later buildings (Prime Station / Park Alpha / South Station per Baxtel) have no MW.
- **QTS Eagle Mountain B4-B5.** Baxtel lists 5 buildings for 2026-29; B4-B5 are undated.
- **Joule (Millard County / Delta).** Behind-the-meter gas, CUP executed, no MW or dates.
- **Other planned sites without data:** Tract Pole Canyon / Pony Express, Edged Bluffdale, Aligned SLC-02. O'Leary's "Stratos", raised on the Aterio/GS call of 2026-10-20 where Aterio called Utah's pipeline partly low-likelihood, was not found.

### Wyoming
- **Microsoft Cheyenne.** Expansion announced 2026-04-14, about 3,200 acres, with no MW. Black Hills says its 600 MW of data-center demand by 2030 is "primarily Microsoft and Meta" (Q1-26 call, 2026-05-07; grid basis).
- **Prometheus Hyperscale (Evanston).** Phase 1 is 1,250 MW and lands around 2031, outside the window.

### Montana, Colorado, Idaho
- **Montana:** the NorthWestern Energy / Sabey / Atlas Power / Quantica letters of intent were not researched.
- **Colorado:** QTS DEN1-DC3 (60 MW) is undated, and Vantage CO21/CO22 are planned.
- **Idaho:** Meta Kuna's two northern buildings are under construction with no MW.

### Oregon, Washington, California
- **Amazon "Threemile", Boardman.** About 1 GW and 20 buildings per Morrow County planning documents (Mar-Apr 2026). Amazon says plans are "not final". There is no timetable, and the project sits squarely inside Kotek's DEQ hold.
- **Meta Prineville Phase V.** Under construction, with no MW.
- **Hillsboro (PGE).** PGE's 8-K of 2026-05-12 shows 430 MW of executed DC contracts and 1.7 GW of requests, not tied to projects.
- **Not researched:** Quincy / Moses Lake (WA) and Apple Prineville. This is a budget gap.
- **Imperial Valley (CA).** About 330 MW. A court voided the county approval on 2026-09-09.

## Source caveats

- **Web-search budget.** The turn's shared WebSearch cap of 200 calls was exhausted midway, across this agent and its three state sub-agents. Arizona, Utah, Montana, Colorado, Quincy and Hillsboro were cut short, and later Nevada checks used WebFetch on known URLs only. A follow-up run could close the Switch, Microsoft (AZ/WY), EdgeCore Mesa, Quincy and Montana gaps.
- **Epoch AI rows** (Google Storey B3, Google Mesa B2, Google The Dalles B2, Stream Goodyear, QTS Eagle Mountain, Meta Cheyenne, Meta Kuna):
  - MW and dates are satellite and cooling-model estimates of **IT power**, not company figures.
  - The energized status of Google Mesa B2, Google The Dalles B2, Stream AI1, Meta Cheyenne B1-B2 and Meta Kuna B1-B2 is Epoch's estimate.
  - Incremental MW per phase is Capstone arithmetic on Epoch's cumulative series.
- **Tracker fallbacks (Baxtel/Cleanview/BlackRidge)** carry 12 rows:
  - OR, 6 rows: the AWS buildings (5) and QTS Hillsboro DC1. The Cleanview pages are now paywalled and could not be re-read.
  - NV, 2 rows: PowerHouse Reno 1 and the EdgeCore B1 date.
  - UT Novva WJ3, CO QTS DEN1-DC2, and WY Related Digital (a Baxtel relay of Oct-2025 news).
  - WA EAT06 uses Cleanview/BlackRidge.
- **Fleet/Tract (NV) dates.** These come from the Barclays seed in Daniel Grozdea's AI_Credit_Live dossier (2026-10-16, `_briefings/2026/2026-10-16-ai-credit-live-workbook-dossiers.md`), flagged there as unverified. MW (200 IT / 230 utility capacity each) is from Fleet's own releases (2026-02-24, 2026-05-01). Tenant NVIDIA is Bloomberg-reported (2026-02-12), not named by the issuer.
- **Edits made when merging the sub-agent rows:**
  - local_approval set to `unknown` wherever it was only inferred from construction or operation.
  - Third-party dates labelled `analyst`; `estimate` is kept only for the Capstone-derived Santa Clara SJC37 date.
  - Google The Dalles tracker row (62 MW) replaced by Epoch's dated building (77 MW IT), to avoid double-counting what is probably the same building.
  - The unverified Hillsboro city pause moved from `local_moratorium` to notes.
- **Oregon convention.** air_permit is `unknown` rather than `n/a` even for grid-only sites. Oregon DEQ issues ACDP air permits for backup gensets, and Kotek's 2026-10-09 directive pauses DEQ ACDP/Title V/NPDES/WPCF permits for new or expanded data centers to 2027-07-01 (OPB 2026-10-13; Ballard Spahr). Elsewhere, backup-only sites are `n/a`.

## State and utility instruments (not written into local_moratorium; for `state_rules.json`)

- **AZ:** Hobbs's freeze on new DC sales-tax-exemption applications runs 2026-07-01 → 2029-06-30 and leaves existing exemptions in place. The ACA received 113 applications on 2026-06-15/30 (Axios Phoenix, 2026-07-08, via the water theme). APS has made no new DC commitments since 2024-01, with about 4 GW allocated (KJZZ, 2026-09-02). The SRP board discussed a moratorium on new DC interconnection agreements on 2026-11-02. The AG is challenging the Project Blue ESA (Feb-2026).
- **OR:** Kotek's DEQ permit hold to 2027-07-01. A Hillsboro city pause was reported (KPTV, Jul-2026) and is unverified.
- **NV:** the governorship flipped R→D on 2026-11-03, and no instrument has been announced. Fleet's temporary gas plants have NDEP air permits pending or unknown (PUCN conditional approval, 2026-09-17). NV Energy v. Tract (filed ~2026-07-24) is the power-side risk for both Fleet rows.
- **CA:** Imperial County imposed a 45-day freeze in Jun-2026, and a court voided the county approval on 2026-09-09.
