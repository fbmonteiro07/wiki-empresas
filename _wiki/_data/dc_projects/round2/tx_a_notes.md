# Round 2, lane tx_a: Texas BTM/on-site gas, neoclouds, miner-to-HPC (2026-11-06)

Files: `tx_a.csv` (21 new rows), `tx_a_fixes.csv` (11 full replacement rows), `tx_a_ramps.json` (4 entries). Schema v1. as_of 2026-11-06.
Web budget: **11 of 35 WebSearch calls used.** Most data came free from EDGAR (Q3-2026 10-Qs, 8-Ks, decks filed 10-27 to 11-05), the TCEQ issued/pending gas-turbine list (`turbine-lst.xlsx`, version 2026.10.7) and one TDLR record.

## Rows added (21)

| project_id | MW | basis | cod_base | status | likelihood | key source |
|---|---|---|---|---|---|---|
| TX-AMARILLO-MATADOR-TW1 | 156 | IT | 2028-01 (+ramp to 2028-02) | not_started | high | Fermi 10-Q, fact sheet 10-14 |
| TX-AMARILLO-MATADOR-TWEXP | 428 | facility | 2028-12 | not_started | low | Fermi 10-Q (tenant option) |
| TX-HUBBARD-NEXUS-HB1 | 300 | unknown | 2027-10 | under_construction | medium | TDLR via Baxtel; WFS Exh.3 |
| TX-HUBBARD-NEXUS-HB2 | 300 | unknown | 2028-01 | under_construction | medium | TDLR TABS2026023798 |
| TX-CORSICANA-RIOT-P1 | 400 | IT | 2027-09 | not_started | high | Riot 10-Q 11-04 (Anthropic) |
| TX-CORSICANA-RIOT-P2 | 200 | IT | 2028-01 | not_started | high | Riot 10-Q |
| TX-CORSICANA-RIOT-P3 | 310 | IT | 2028-07 | not_started | high | Riot 10-Q |
| TX-ROCKDALE-RIOT-ANTH1 | 96 | IT | 2027-12 | under_construction | high | Riot 10-Q + deck |
| TX-ROCKDALE-RIOT-ANTH2 | 95 | IT | 2028-06 | under_construction | high | Riot 10-Q + deck |
| TX-ROCKDALE-RIOT-AMD1 | 25 | IT | 2026-05 | energized | high | Riot 10-Q |
| TX-ROCKDALE-RIOT-AMD2A | 10 | IT | 2026-11 | energized | high | Riot 10-Q + deck |
| TX-ROCKDALE-RIOT-AMD2B | 15 | IT | 2027-05 | under_construction | high | Riot 10-Q |
| TX-PECOS-CORZ-AMD | 185 | IT | 2027-06 (+ramp to 2028-12) | under_construction | high | CORZ Q3 deck 11-05 |
| TX-GREENVILLE-CORZ-HUNT | 110 | IT | 2028-06 (+ramp to 2028-12) | under_construction | high | CORZ Q3 deck + 10-Q |
| TX-SANANGELO-COLCHIS-ALL | 1,000 | grid | 2028-06 (year_only) | not_started | medium | Cipher Q3-26 update; AEP DCA |
| TX-ODESSA-TCDC-PH1 | 207 | facility | 2027-08 | not_started | medium | New Era 8-Ks (Vistra PPA) |
| TX-MONAHANS-IONIC-WARD377 | 377 | grid | 2027-11 | not_started | medium | Ionic Q3 release 11-04 |
| TX-SANMARCOS-CLOUDBURST-PH1 | 50 | unknown | 2026-11 | under_construction | low | W.Media 2025-11-19 (stale) |
| TX-LAREDO-DATACITY-PH1 | 300 | unknown | 2026-06 (year_only) | not_started | low | Bisnow 2025-03; Cleanview "Planned" (stale) |
| TX-FORTSTOCKTON-GWRANCH-ALL | 5,000 | gen | 2027-06 (+ramp to 2030-06) | not_started | low | Pacifico via DCD/EnergyTech (search summary) |
| TX-WINK-BLACKPEARL-PH1REM | 32 | IT | 2026-12 | under_construction | high | Cipher Q3-26 update (split from DH1NH1) |

## MW by state × cod year × mw_basis (row dates; never add across bases)

| state | year | IT | facility | grid | gen | unknown |
|---|---|---|---|---|---|---|
| TX | 2026 | 67 | – | – | – | 350 |
| TX | 2027 | 696 | 207 | 377 | 5,000 | 300 |
| TX | 2028 | 871 | 428 | 1,000 | – | 300 |
| **TX** | **total** | **1,634** | **635** | **1,377** | **5,000** | **950** |

- After the ramps are applied: IT 2027 ≈ 604 and 2028 ≈ 964 (Pecos splits 92.5/92.5); GW Ranch gen 1,250 a year in 2027-30.
- **All 1,634 MW IT is high likelihood**: signed leases with Anthropic (Riot), AMD (Riot, CORZ) and TensorWave (Fermi).
- **Medium:** 600 MW unknown (Nexus), 1,377 MW grid (Colchis, Ionic) and 207 MW facility (TCDC).
- **Low:** 350 MW unknown (CloudBurst, Data City), 428 MW facility (Fermi option) and 5,000 MW gen (GW Ranch).
- **GW Ranch is generation nameplate with no data-center MW or tenant.** Treat it like the Kilby row; drop it if the model should hold data-center load only.
- **Black Pearl net change is 0 MW:** 50 → 18 + 32.

## Fixes (11 rows in tx_a_fixes.csv)

- **TX-ABILENE-CRUSOEEXP-B1, -B2: air_permit `pending` is now verified on TCEQ records.**
  - Permit 182126 / PSDTX1688 / GHGPSDTX263, applicant Crusoe Energy Systems LLC.
  - Scope: "Longhorn Data Center Buildings 9 and 10", 615 FM 2404 Abilene.
  - Received 2025-11-07; still Pending on the turbine list. It covers 39 × LM2500/DT35, 1,330 MW.
  - Cleanview calls the Microsoft AI Factory "Longhorn Bldg 9-10".
  - Changes: air_permit_date 2026-07 → 2025-11; lat/lon moved to the TCEQ map point (32.508, -99.777).
  - WFS's "July filing, 41 turbines + 18 generators" is a different or amended filing and was not matched.
- **TX-CLAUDE-GOODNIGHT-B1, -B2, -B3B6: `pending` verified.**
  - Permit 182880 / PSDTX1698, Crusoe, Claude (Armstrong Co.): 20 × LM6000/DT46 = 932.9 MW.
  - Received 2026-01-30, still Pending. air_permit_date is now 2026-01.
  - This confirms the 933 MW that round 1 carried as unverified. SemiAnalysis 11-01 agrees.
  - Goodnight is not in WFS Exh.3.
- **TX-AFTON-HELIOS-PH3:** 2028 is now Galaxy's own date (Q3-26 deck slide 16: rent from 2028, 133 MW IT).
  - not_started is sourced: the Oct-2026 aerial shows only Phases I-II under development.
  - cod stays 2028-06 (year_only).
- **TX-AFTON-HELIOS-HELIOSII:** still unleased (Q3 release 10-27) and labelled "Contractable".
  - The deck ramp shows 824 MW of uncontracted capacity energizing earliest in 2028.
  - not_started and 2028-06 are now sourced. 830 vs 824 is not reconciled.
- **TX-PECOS-KILBY-ALL:** data-center IT MW is still not disclosed.
  - air_permit_date 2025-10 added: TCEQ 181895, Energy Forge One, GE 7HA.02, received 2025-10-17, Pending.
  - Press figures of a 2.5 GW DC on 7,000 acres conflict with ">2,000 acres" and were not used.
- **TX-WINK-BLACKPEARL-DH1NH1:** 50 → 18 MW. Cipher says 18 MW IT has been delivered to date.
  - The 32 MW balance is the new row TX-WINK-BLACKPEARL-PH1REM.
- **TX-WINK-BLACKPEARL-DH2:** cod 2026-10 → 2026-12. The Oct-31 target passed undelivered; the company says RFS "through year-end".
- **TX-MONAHANS-NSCALE-WARDEXP:** cod 2027-09 (Jefferies) → 2027-11 (Ionic, company: "late 2027").
  - mw_basis unknown → grid (gross MW of the 466 MW large-load request).
  - interconnection → study (provisional Batch Zero Baseload pathway (b)).
- **Not changed, flagged for review: TX-ABERNATHY-FLASH-PH1.**
  - TeraWulf's Q3 deck says it sold its JV stake "prior to project completion", so the row's 2026-09 date may be stale. No new date was found.
  - The TCEQ list shows "Forth Worth Power Core LLC, Abernathy (Hale)", 6 × SGT-800 = 330 MW, standard permit issued 2025-06-11.
  - If that plant serves this site, the row's air_permit `n/a` is wrong. The link is not established.

## Rows dated from Texas TDLR construction-completion dates

- **TX-HUBBARD-NEXUS-HB2:** TABS2026023798, completion 2028-01-05, fetched directly.
- **TX-HUBBARD-NEXUS-HB1:** Oct-2027 per Baxtel's 2026-06-27 report of the TDLR filing. The TABS number and the day were not found.
- None of the fixes changed a TDLR-dated row's date.

## Biggest campuses still un-pinned

1. **Fermi Matador beyond TensorWave.**
   - 11 GW gas plan: 6 GW issued + 5 GW pending.
   - Hillcore BOOT for up to 2.6 GW of generation (initial ~360 MW block).
   - No other tenant and no dates.
   - The 2026-11-10 covenant to sign a 400 MW lease was waived (8-K 10-16).
2. **Nexus Hubbard beyond ~600 MW.** Cleanview puts the full build-out at 6,400 MW; the WSJ (via the CRWV page) has 1.6 GW / $15bn. No phase dates.
3. **Galaxy pipeline**, 4,930 MW gross uncontracted beyond Helios I.
   - Sites: Helios II 830, Helios III 1,000, Helios IV 1,000, Caspian 700, Selene 900, Merlin I 74, Merlin II 426.
   - Only a portfolio-level "earliest potential" ramp exists: 824 MW in 2028, +1,450 in 2029, +2,656 in 2030+.
   - It is not site-identified, so only Helios II is rowed.
4. **IREN Sweetwater:** 1,400 + 600 MW gross, grid-connected / Batch Zero base load, "well under construction".
   - Only the 300 MW Vera Rubin tranche (late 2027) has a date.
   - Roberts: "constructing capacity to be available" in 2028, not site-specific.
5. **SB Energy Borden (836 MW IT) and Scurry (900 MW IT).**
   - The S-1/A (09-21) says ~2.35 GW gross power is "available in 2028" under Batch Zero Base Load. There is no tenant, and delivery is "N/A".
   - Not rowed, because power availability is not a delivery schedule. **Adjudicate.**
6. **Cipher pipeline.**
   - Mikeska 500 and McLennan 500: 2028-29 window, studied load.
   - Apollo 900 and Stingray II 200: 2030+.
   - On-site generation ~1,000 MW: 2027-28, not site-assigned.
   - Reveille (LaSalle, TX) 70 MW, Q3-27: below 100 MW, out of scope.
   - Horizon 70 MW, 2029: out of scope.
7. **Poolside / PIC Project Horizon** (Pecos Co., Longfellow Ranch).
   - 2 GW announced Oct-2025. CoreWeave's anchor lease was reportedly pulled in spring 2026; that comes from aggregator reports only.
   - PIC (08-17-2026): "400 MW under development".
   - TCEQ standard permit 183235 was issued 2026-03-12 to "Poolside LF Phase 2 DC Ops LLC" for 12 × TM2500 = 332 MW.
   - No dates.
8. **Other undated sites:**
   - TCDC Phase 2: 550 MW, air permit filed.
   - MARA's Texas site (MAT 1177, ex-HIF USA): 2,000 MW utility letter agreement (8-K 09-25).
   - Hut 8's Poolin West Texas sites: up to 230 MW.
   - Bitdeer's Rockdale AI parcel: the site has 563 MW interconnected, but no AI MW is disclosed.
   - CORZ Pecos studied load: ~200 MW.
   - AMD reservation: up to 1,925 MW through Dec-2028.
   - Riot's AMD options: 50 + 100 MW.
9. **Excluded on scope:** Nscale's Ward County base lease (234 MW) commenced 2025-12-19 (Ionic 10-Q), which is pre-2026.

## Source conflicts to adjudicate

- **Fermi air permit: no real conflict.**
  - The 6 GW permit got TCEQ final approval in Feb-2026 (KCBD 02-25; Fermi fact sheet: "~6 GW currently permitted").
  - The pending No. 183462 / PSDTX1704 is the 5 GW *additional* gas. Its TCEQ public meeting on 2026-08-24 was cancelled, to be rescheduled.
  - Together: 6 GW issued + 5 GW pending = 11 GW. The TW1 row is `issued` (2026-02).
- **Fermi TensorWave lease:** effectiveness needed project financing, with closing extended to 10-31. Closing is not confirmed in the filings read; the row is kept high per Aterio's tier for the first 200-300 MW.
- **Nexus Hubbard size:** 600 MW (WFS) vs 1.6 GW (WSJ) vs 6.4 GW (Cleanview). The rows use 600 MW, split 300/300 (Capstone).
- **Riot Corsicana interconnection.** About 400 MW is energized today (10-Q), and the deck gives 1.0 GW of utility load; Bernstein (08-04) calls RIOT "fully grid approved".
  - P1 is `energized` (our mapping); P2 and P3 are `unknown`.
- **CORZ MW basis:** "leasable" IT (CORZ convention) vs gross MW at peers. The rows record IT.
- **GW Ranch timing:** first power 1H-2027 (CEO) vs "first 1 GW in 2028" (Aug-2025). Full build-out 2030 vs 2031.
- **CloudBurst and Data City:** dates are 2025 vintage and no 2026 progress was found. Both are kept as low.

## Leads for other lanes (not rowed here)

**tx_b**
- Cleanview TX list (2026-11-06), under construction:
  - Google Wilbarger Co. 850 MW
  - "Meitner Data Center" (Google, Gray Co.) 840 MW
  - Stargate Frontier 1,820 MW
  - Meta El Paso 988 MW
  - Stargate Milam 939 MW
- SB Energy S-1/A: Milam Bldg 2 (445 MW IT) is in vertical construction (NTP Apr-2026), with delivery in 2028.
- SpaceX TCEQ pending:
  - Bastrop: 4 × LM2500, 149 MW, received 2026-09-16
  - Brownsville: 31 MW
- Burr Computer Environments Properties LLC, Victoria: 400 MW, issued 2026-06-09. Possibly a data center.

**Midwest / South / Plains**
- TeraWulf "Justified" (Hawesville, KY): 401 MW IT for Anthropic, delivery late-2027 to Q2-2028.
- TeraWulf Muskie (Grayson, KY): 1 GW, initial 500 MW ramping Q4-2028.
- Cipher Ulysses (OH): 200 MW gross, Q4-2027, interconnection approved.
- Bitdeer Clarington (OH): 570 MW, Q2-2027.
- CleanSpark Sandersville (GA): $2.227bn notes.
- CORZ AMD/neocloud:
  - Muskogee OK: 82 MW, 2H27
  - Dalton GA: 120 MW, 2H27
  - Auburn AL: 32 MW, 1H27

**TCEQ gas-turbine leads with no data-center link established**

| Company | Location | MW | Status |
|---|---|---|---|
| Featherwood Capital | Pecos | 931 | issued 2026-01-08 |
| Steadfast Energy Center | Odessa | 878.8 | pending since 2026-08-10; TCDC Phase 2? |
| Evolve Energy | San Marcos | 630 | pending |
| Stella Power | Mustang Ridge | 400 | issued |
| ProEnergy | Navasota (Grimes) | 600 | pending |
| ProEnergy | Lufkin | 600 | issued |
| Frontiergen | Mathis | 500 | pending |
| Frontiergen | George West | 500 | pending |
| Gulf Nexus I | Danevang | 500 | pending |
| Briscoe County Power Plant | Briscoe Co. | 446 | pending |
| Forth Worth Power Core | Panhandle, Carson Co. (next to Fermi) | 330 | issued 2025-06 |

## Paywalled or blocked

- **Returned 403:** DataCenterDynamics, EnergyTech.
- **Returned 429:** Aterio event page, Galveston Daily News.
- **Returned 404:** idcnova (Poolside article).
- **Cleanview:** only the Texas overview rendered; project detail is paid.
- **TCEQ English PLS PDF:** text not extractable. The Spanish NORI was read instead.
- **Poolside status after April 2026:** comes only from aggregator or AI summaries (tech-insider, latent.space wiki); low confidence.
