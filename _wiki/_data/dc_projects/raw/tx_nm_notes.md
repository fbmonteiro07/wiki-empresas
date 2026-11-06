# TX + NM data-center registry: compile notes (2026-11-06)

File: `raw/tx_nm.csv`, schema v1 (`SCHEMA.md`). Built from the wiki corpus, Epoch AI's data-center CSVs (downloaded 2026-11-06, last updated 2026-11-05), company/filing pages and a few fetched press pages.

**The web-search budget ran out partway through.** The tool hit its shared limit of 200 searches per turn. After that, only known URLs were fetched. Several large campuses are therefore listed under gaps instead of being rowed.

## Row count

- **58 rows:** 54 TX, 4 NM.
- **24 campuses:** 22 TX, 2 NM. Phases are split wherever a public schedule exists:
  - Stargate Abilene buildings 3-8
  - Frontier buildings 1-10, using TDLR completion dates
  - Goodnight
  - Helios phases
  - Black Pearl data halls
  - Beacon Point phases 1-2
  - Milam buildings 1-2
  - IREN Horizons and 2027 tranches
- **Excluded because they energised before 2026:** Abilene B1-B2, Meta Temple B1-B2, Microsoft SAT40, and Denton capacity live by 2025-12-31.

## MW by state × phase_status × cod year

These sums mix MW bases (see the next section). Read them as source MW, not as IT GW.

| state | phase_status | 2026 | 2027 | 2028 | total |
|---|---|---|---|---|---|
| TX | energized | 969 | – | – | 969 |
| TX | under_construction | 910 | 4,968 | 2,357 | 8,235 |
| TX | not_started | – | 89 | 4,053 | 4,142 |
| **TX** | **all** | **1,879** | **5,057** | **6,410** | **13,346** |
| NM | energized | 31 | – | – | 31 |
| NM | under_construction | – | 550 | 1,750 | 2,300 |
| **NM** | **all** | **31** | **550** | **1,750** | **2,331** |

- **TX not_started 2028 is dominated by Project Kilby.** Kilby's 2,670 MW is **generation nameplate** (`gen`), not data-center load. Without Kilby, TX totals 10,676 MW.
- **Nothing is dated 2029-30.** Every undated pipeline campus sits in the gaps list below.
- **Likelihood (TX):** high 7,961 MW, medium 5,385 MW.
- **Likelihood (NM):** Jupiter is medium (2,200 MW); Los Lunas is high (131 MW).
- **TX air-permit exposure (TCEQ):** `pending` on 5,837 MW. That covers:
  - Crusoe Abilene expansion (Microsoft), 672 MW
  - Vantage Frontier, 1,400 MW
  - Goodnight, 1,006 MW
  - Kilby, 2,670 MW gen
  - Nscale Ward County, 89 MW
- **TX air permit `unknown` on 2,618 MW:**
  - Abilene B3-B8, which have an existing on-site gas plant of unstated permit status
  - Crusoe/Lancium Childress
  - Meta El Paso, whose McCloud bridge plant needs TCEQ and PUCT approval
- **All other TX rows are `n/a`:** grid-only with ordinary backup gensets.
- **Reminder from the rules research:** the TCEQ hold also covers stormwater and water permits. `n/a` air does not mean a project is fully exempt.

## mw_basis mix

| state | IT | facility | grid | gen | unknown |
|---|---|---|---|---|---|
| TX rows (MW) | 35 rows (5,657) | 3 (700) | 4 (2,830) | 1 (2,670) | 11 (1,489) |
| NM rows (MW) | 2 (131) | – | – | – | 2 (2,200) |

- **IT:**
  - Abilene, the Abilene expansion and Goodnight per-building MW are Epoch AI estimates (see caveats).
  - Milam, Beacon Point, Helios, Barber Lake, Black Pearl, Stingray and Abernathy are company or filing figures.
- **facility:** IREN's "gross MW" 2027 tranches.
- **grid:**
  - Crusoe/Lancium Childress, "1.0 GW grid-connected"
  - Helios II's 830 MW ERCOT approval
  - Meta El Paso, from El Paso Electric load filings
- **unknown:**
  - Vantage Frontier: Vantage's 1.4 GW; Epoch treats it as IT
  - Jupiter: GS's 2.2 GW
  - Nscale Ward County: the 89 MW lease

## Coverage against the yardstick

The Aterio-based deck ("amigo Felipe", received 2026-11-06) puts Texas at **35.1 GW** under construction with dates in 2026-30. Its basis is not stated.

- **Rows here cover about 9.2 GW of TX that is energised in 2026 or under construction**, plus 1.5 GW not_started excluding Kilby. That is roughly **a quarter to a third** of the yardstick on any basis.
- The gaps below explain most of the difference. Fermi's full scope alone is 11 GW announced; Aterio rates it low likelihood beyond the first 200-300 MW.
- WFS (11-04) puts Texas at ~81 GW of the cumulative US pipeline (Tusa's tracker). SemiAnalysis (11-01) puts it at 18 GW of 2028 net adds across 13 states and **16.7 GW** of Texas planned capacity "exposed".
- None of these bases is reconciled with the others.

## Biggest campuses not pinned down

Each is listed with the reason it has no row.

1. **Fermi America Project Matador** (Carson Co., Amarillo; SPP/Xcel SPS, BTM gas).
   - TensorWave signed a 15-year lease for the first 222 MW (Fermi, 2026-10-14).
   - Turbines are arriving: Siemens F-class units from Sep-18, three GE 6B units on Oct-15.
   - Fermi says TCEQ approved air permits for up to 6 GW in Feb-2026. WFS Exh.3 (11-04) instead shows a pending application for 5 GW of *additional* gas, permit No. 183462, caught by the TCEQ hold.
   - Aterio (GS call, 10-20): high likelihood for the first 200-300 MW, low for the full 11 GW.
   - **No first-power or first-hall date found.**
2. **Poolside / CoreWeave "Horizon"** (West Texas, ~2 GW announced). Not in the corpus, and no searches were left to look it up.
3. **Nexus Hubbard** (Hill Co.; WFS says it is leased to Anthropic).
   - About 600 MW of gas-powered first phase.
   - WFS reports that banks are delaying a $5-7bn bond sale on a $15bn loan.
   - No date. The Hill County moratorium (May-2026, Stratechery 05-18) was rescinded after a developer suit, per `state_local_rules.md`.
   - NRG Prairie Energy Center (Hill Co.) is a nearby gas plant with a major-source air notice mailed 9/22. It is a power plant, not a data center.
4. **Google Haskell County** (part of the Nov-2025 $40bn Texas plan). No MW or dates in the corpus.
5. **Riot Rockdale** (Anthropic: ~191 MW, 20 years, $9.1bn; 241 MW IT under contract across two agreements) **and Corsicana** (1 GW gross LOI). No delivery dates found.
6. **Core Scientific Pecos and Hunt County.** Pecos has 300 MW of base load plus 300 MW of studied load. Hunt County is ~430 MW gross with construction started. AMD has 377 MW leased across Pecos, Muskogee and Hunt. No per-site split or dates.
7. **Cipher pipeline.** Batch Zero classifications are conditional:
   - Colchis 1,000 MW
   - Mikeska 500, Apollo 900 and McLennan 500 MW, studied load
   - Stingray II 200 MW, 2030+
   - plus a plan for ~2.5 GW of BTM generation
   - None has a schedule.
8. **IREN Sweetwater.** The remainder of Sweetwater 1 (~1.1 GW of the 1.4 GW grid connection) and Sweetwater 2 (600 MW) are "well under construction" (Draper, 11-05 call) but undated. Only the 300 MW Vera Rubin tranche for late 2027 is rowed.
9. **Galaxy Helios III (1,000 MW), Caspian (700) and Selene (900).** All studied load, undated.
10. **Nscale Ward County base lease.**
    - Sizes: 234 MW (Ionic S-1), 200 MW IT (Nscale S-1), or 240 MW scalable to 1.2 GW (Kodiak call). The Microsoft GB300 link comes from an Oct-2025 announcement.
    - No energisation date was found. Only the 89 MW expansion is rowed (Jefferies: 2H27).
    - **Circe Energy E. Monahans** (Ward Co.; Cummins 2.0 GW BTM order with deliveries 2026-30; status "proposed") may be the same campus. That is not established, and it has no data-center MW.
11. **SpaceX Starbase** and **Terafab (Grimes Co.).**
    - SemiAnalysis (11-03): Starbase is in vertical construction and "may use 1 GW of APRs". Terafab is a fab plus a test data center, with Phase I targeted for 2028.
    - FundaAI (11-04) finds no Texas exposure for xAI 2027. No MW or dates.
12. **Pacifico "GW Ranch"** (Pecos Co.) and 22V's "Amazon — GW ranch — TX" (08-17). No usable detail in the corpus.
13. **SB Energy Borden Co. (836 MW-IT) and Scurry Co. (900 MW-IT).** S-1/A lists them with no tenant and no dates.
    - **SB Energy Cosmos** (Austin, 50 MW-IT, SoftBank tenant, RFS 4Q26 to May-27) is left out on scope: the tenant is not a hyperscaler or AI lab.
14. **Multi-tenant colo** in DFW, San Antonio and Austin (QTS, Aligned, CyrusOne, STACK, Skybox, Tract and others) and Laredo/San Marcos mega-campus proposals. Not covered.
15. **Project Kilby's data-center IT MW.** Not disclosed. The row carries the 2.67 GW of co-located generation.

## Choices and conventions

- **cod_base is the latest schedule whose slip is not attributed to the permit pause.**
  - Customer-driven slips are kept and the old date goes in `notes`:
    - IREN Horizons 2-4: Q4-26 → Jan-27, a Microsoft network change
    - Barber Lake: Sep-26 → Q4-26/Q1-27, tenant change orders
  - Quarter-precision sources use the quarter's middle or end month; this is stated per row.
  - "Late 2027" is entered as 2027-11.
- **TDLR (Texas building-registration) construction-completion dates stand in for energisation** at Frontier, Goodnight, the Abilene expansion, Crusoe Childress, Denton B8 and Vantage TX1. Epoch adds ~6 months before a building is "operational". Its estimates are given in `notes`.
- **Derived MW is flagged in notes:**
  - Goodnight B3-B6: 1,006 − 206
  - El Paso phase B: 1,000 − 440
  - Jupiter: GS's 25% / 75% of 2.2 GW
  - Denton 2026 tranche: 262 − 67
- **Permit fields come only from sources.** Frontier and Goodnight are `pending`, based on the VoltaGrid ABI-1 and Goodnight generation applications.
  - The Abilene-expansion `pending` maps WFS's "Stargate Abilene expansion filing (July)" to the Microsoft plant. That mapping is ours.
  - El Paso's McCloud plant is `unknown`: TCEQ approval is needed, but the docket outcome was not found.
- **local_approval is `approved` only for Milam and Jupiter.**
  - Milam: S-1/A says "key permits obtained".
  - Jupiter: Doña Ana County IRBs. A state senator has floated clawing them back (10-23 call).
  - Texas counties have little zoning power; tax abatements are not counted as approvals.
- **local_moratorium is blank.** None of the rowed sites sits in an active TX or NM local moratorium in the rules tracker (Lavon, Brownsville, Hays, Harlingen, Austin Co.; Socorro NM).
- **Grids:**
  - El Paso and Jupiter are **WECC** (El Paso Electric), not ERCOT.
  - Abernathy is **SPP** (Xcel SPS).
  - Fermi is SPP (gap).
  - Goodnight is entered as ERCOT on press-summary evidence only. It is in the Panhandle, so verify.

## Source-quality caveats

- **Epoch AI** (satellite plus TDLR, data_center_timelines.csv) supplies many per-building IT MW figures and dates. These are model estimates, not company figures:
  - Abilene ~103 MW per building, inferred from Oracle's 618 MW across six buildings
  - Abilene expansion 336 MW per building
  - Goodnight, Temple, Midlothian, Red Oak, Vantage TX1 and Los Lunas
- **Bond-financed sites** (Barber Lake, Black Pearl, Stingray, Abernathy, Helios, Beacon Point, El Paso, Denton) come from the Capstone AI-credit dossiers (2026-10-16). Those compile offering memoranda, 8-Ks and press, and dates there are company targets.
  - The Black Pearl hall schedule is a Feb-2026 deck target that the company says is being re-phased.
- **Search-summary-only (unverified) items:**
  - Goodnight's ~933 MW gas figure (attributed to Cleanview) and its ERCOT tag
  - Kilby's FID by YE-2026 and the ~2 GW Microsoft DC figure, which was not used
- **Broker and vendor views are not company schedules:**
  - GS's Jupiter phasing, Jefferies' Ward County 2H27, and Epoch's estimates are all third-party.
  - Aterio's likelihood tiers are applied by us, not taken from Aterio's dataset.
- **The Abilene expansion has two conflicting dates.** The Aterio-derived scenario deck dates a 0.34 GW Abilene building with its own plant to Mar-28, while TDLR gives B1 Sep-27 and B2 Nov-27. The difference is kept in `notes`.
- **Corpus files used** (paths relative to `E:\Wiki Felipe empresas`):
  - WFS Revich 11-04 (`relatórios bons\Texas_Policy_Reset_...html`; Exhibit 3 read from the PDF page image)
  - FundaAI 11-04 (`relatórios bons\tx_data_center.html`)
  - SemiAnalysis 11-01
  - Aterio/GS 10-20
  - NM Jupiter call 10-23
  - `_wiki\ORCL.md`, `_wiki\IREN.md`, `_wiki\NSCALE.md`, `_wiki\CRWV.md`
  - `_wiki\themes\ai-compute-deals.md`, `_wiki\themes\ai-datacenter-power.md`, `_wiki\themes\debt-equity-deals-2026h2.md`
  - `_briefings\2026\2026-10-16-ai-credit-live-workbook-dossiers.md`
  - IREN Q1 FY27 call (11-05) and BTG websession (09-22)
  - SB Energy S-1/A (SEC, 2026-09-21)
