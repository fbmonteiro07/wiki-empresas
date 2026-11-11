# Theme — US data-center construction pipeline (Aterio census)

_Wiki · generated 2026-11-09 · reference theme · source: Aterio US data-center census, licensed project-level export as of **2026-08-31** (internal use; `P:\Felipe Monteiro\Aterio`), plus the Aterio team on a Goldman Sachs call (2026-10-20, [render](../../relat%C3%B3rios%20bons/2026_10_20_aterio_gs_20_oct_2026.html)). Per-company sections: every company page below carries a "DC construction pipeline — Aterio census" section. Company pages: [../00_INDEX.md](../00_INDEX.md) · themes index: [00_THEMES.md](00_THEMES.md)._

## What it is / why it matters

**2026-11-10 Meta audit:** independent building-row arithmetic agrees with the dashboard, but the company total is a filtered US census scenario. Meta's **11.53 GW IT-eq** is additions during 2026–30; the pre-2026 base takes end-2030 to **15.22 GW**, or **16.51 GW with Medium**. Bernstein's later-dated November 6 chart shows about **15 GW construction** versus **8.85 GW facility** in the August export; its power basis, exact data vintage and attribution remain unverified. The dashboard's prior same-basis wording has been corrected. Uniform facility/IT conversion remains the agreed house rule; native-IT replacement is only a sensitivity. [Full audit and source-field gaps](../_meta/aterio-meta-audit-2026-11-10.md). Existing house numbers and export are preserved.
Since 2026-11-09 Capstone holds Aterio's building-level census of US (and some Canadian) data centers: 8,226 buildings, 77 fields, monthly point-in-time snapshots back to 2024-12, an events log, Aterio's weekly report (with its own activation forecast) and a behind-the-meter (BTM) generation inventory. **It is the house reference for how much data-center capacity gets built in the US in 2026-30, where, by whom, and how likely each project is to happen.** Use it with the basis rules below; cite it as "Aterio data-center census, as of 2026-08-31" and say facility vs IT and building vs campus every time.

Where to look:
- **House view (the figure to quote):** the "Capstone house view" section below: 186.1 GW IT-eq due in 2026-30 under the house rules of 2026-11-09, by year, state and company. Vintages and sensitivity: [dc-delay-risk.html#aterio-deck](../_dashboards/dc-delay-risk.html#aterio-deck).
- **Hyperscalers and company lookup:** [aterio-hyperscalers.html](../_dashboards/aterio-hyperscalers.html) (Amazon, Google, Meta, Microsoft: where they build, how much, at what likelihood; search for any company the census names).
- **Explorer:** [aterio-dc.html](../_dashboards/aterio-dc.html) (12 sections, every building, filters and CSV download).
- **Registry cross-check and delay model:** [dc-delay-risk.html#aterio](../_dashboards/dc-delay-risk.html) (Capstone's public-source registry vs the census, contradictions checked against sources).
- **Company view:** a section on each company page (operator, tenant, backer, financier, power partner), built by `_tools/build_aterio_company.py` into `_data/aterio/company_blocks/`. Each section carries the facility tables on Aterio's basis and a house-view table (GW IT-eq) per role.
- **Deck:** `P:\Felipe Monteiro\Aterio - adição por estado e cenários - Nov 2026` (PT + EN), 3 slides by state and scenario.

## State of play (export 2026-08-31, US)
| Stage | GW facility | ≈ GW IT-eq (÷1.15) |
|---|---|---|
| Active (operating) | 51.8 | 45.1 |
| Under construction | 71.5 | 62.2 |
| Delayed | 8.8 | 7.7 |
| Planned (announced + land bank) | 382.7 | 332.8 |
| Withdrawn / not approved / cancelled | 40.0 | 34.8 |

- **Later vintage, same source:** the Aterio team on the Goldman Sachs call (2026-10-20, citing its report of the prior Friday) put the US at **~55 GW active (~2,000 data centers), ~83 GW under construction (~858 buildings) and ~455 GW announced**, up from 44 / 43 / 214 GW in its 16-Jan-2026 report. Our export is the 08-31 vintage, so it sits below those marks.
- **Not yet active, activation 2026-30: 345.5 GW facility**, of which under construction 71.5, delayed 5.7 and planned 268.3. By Aterio likelihood: **High 205.1 · Medium 107.3 · Low 33.1 GW**.

**When it is due to switch on (GW facility, by Aterio activation year; not yet active only)**

| | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---|---|---|---|---|
| Under construction | 13.1 | 27.0 | 26.8 | 3.5 | 1.1 |
| Delayed | 0.1 | 1.0 | 1.6 | 2.5 | 0.5 |
| Planned · High | 0.0 | 10.5 | 45.9 | 50.0 | 25.9 |
| Planned · Medium | 0.0 | 4.7 | 34.4 | 38.4 | 28.1 |
| Planned · Low | 0.0 | 0.3 | 7.4 | 9.2 | 13.3 |

- **Aterio's own forecast (weekly report, 2026-30 additions, facility):** optimistic 346 / baseline 283 / conservative 210 GW; baseline ~200 GW cumulative online by end-2028 against ~52 GW active today. Capstone's reconstruction (deck above): optimistic ≈ the whole live pipeline; conservative ≈ active + under construction + High.
- **Largest states, 2026-30 not yet active (GW facility):**

| State | Under constr. | Delayed | Planned · High | Planned · Medium | Planned · Low | Total |
|---|---|---|---|---|---|---|
| TX | 16.6 | 1.7 | 37.3 | 32.8 | 7.0 | 95.4 |
| VA | 9.1 | 1.0 | 20.1 | 11.1 | 1.1 | 42.4 |
| GA | 4.5 | 0.0 | 6.6 | 7.5 | 0.8 | 19.5 |
| PA | 2.6 | 0.0 | 5.5 | 7.7 | 2.3 | 18.0 |
| OH | 4.5 | 0.0 | 8.2 | 2.8 | 0.1 | 15.6 |
| UT | 1.1 | 1.7 | 3.9 | 4.5 | 2.1 | 13.3 |
| AZ | 2.1 | 0.0 | 3.8 | 5.6 | 0.5 | 12.0 |
| NY | 0.5 | 0.5 | 0.1 | 6.8 | 2.2 | 10.1 |
| IN | 2.4 | 0.0 | 5.3 | 2.2 | 0.0 | 9.8 |
| IL | 1.2 | 0.0 | 3.7 | 2.7 | 1.2 | 8.9 |
| NV | 2.2 | 0.0 | 5.0 | 1.1 | 0.2 | 8.5 |
| WV | 0.5 | 0.0 | 5.0 | 1.9 | 0.0 | 7.4 |

## Capstone house view (house rules of 2026-11-09)
<!-- aterio-house-view:begin asof=2026-08-31 · generated by _tools/build_aterio_company.py into _data/aterio/theme_house_view.md; refresh = rerun aterio_capstone_view.py then the script, and paste the new section between these markers (agent edit + Changelog line), never by script -->
_Aterio data-center census as of 2026-08-31, Capstone treatment. Rules: `_data/aterio/treatment.json` (decided by Felipe, 2026-11-09); one shared loader applies them everywhere: `_tools/aterio_core.py`. The rest of this page stays on Aterio's own basis (facility MW, every likelihood tier); this section is the figure to quote as the house view. Dashboards: [house view and vintages](../_dashboards/dc-delay-risk.html#aterio-deck) · [hyperscalers and company lookup](../_dashboards/aterio-hyperscalers.html)._

**186.1 GW IT-eq is due to switch on in the US in 2026-30** (214.0 GW facility; 2,528 buildings on 661 campuses), against 306.5 GW IT-eq that Aterio dates to the same window with no filter.

- **Rule 1, basis:** IT-eq = facility MW ÷ 1.15, Aterio's own facility/IT median on the 1,025 buildings that carry both fields (417 of them at exactly 1.000). The MW-weighted ratio (÷1.17) gives 183 GW and the ratio without the 1.000 rows (÷1.27) gives 169 GW: quote 169-186 GW as the band.
- **Rule 2, universe:** what switched on since Jan-2026, plus buildings under construction or delayed, plus planned buildings rated High.
- **Rule 3, dates:** Aterio's activation date as published, with no Capstone haircut on top.
- **Rule 4, exclusion:** a campus rated Low whose buildings name no end user is dropped in every stage.
- **Registry:** Capstone's public-source registry ([dc-delay-risk](../_dashboards/dc-delay-risk.html)) stays independent; Aterio is the cross-check, not the base.

| GW IT-eq | 2026 | 2027 | 2028 | 2029 | 2030 | 2026-30 |
|---|---|---|---|---|---|---|
| Switched on (Jan-Aug 2026) | 6.1 | – | – | – | – | 6.1 |
| Under construction | 11.4 | 23.5 | 23.3 | 3.0 | 1.0 | 62.2 |
| Delayed | 0.1 | 0.8 | 1.4 | 0.4 | 0.1 | 2.6 |
| Planned · High | – | 9.2 | 40.0 | 43.5 | 22.6 | 115.1 |
| **House view** | **17.6** | **33.4** | **64.6** | **46.9** | **23.6** | **186.1** |
| Aterio's dating, no filter | 17.6 | 37.8 | 101.0 | 90.1 | 60.0 | 306.5 |

**What the rules take out of the window (GW IT-eq):** planned Medium 91.9 · planned Low 26.3 · Low-likelihood campuses with no tenant 2.3 (under construction, delayed or switched on). Outside the window and not counted: 100.7 GW dated after 2030 and 1.5 GW with no date.

**Largest states, house view (GW IT-eq, 2026-30)**

| State | House view | Switched on | Under constr. + delayed | Planned · High | Aterio's dating, no filter |
|---|---|---|---|---|---|
| TX | **48.9** | 1.3 | 15.1 | 32.4 | 84.2 |
| VA | **27.5** | 1.4 | 8.6 | 17.5 | 38.2 |
| OH | **11.7** | 0.6 | 3.9 | 7.2 | 14.1 |
| GA | **10.0** | 0.3 | 4.0 | 5.8 | 17.2 |
| PA | **7.0** | – | 2.3 | 4.8 | 15.7 |
| IN | **6.9** | 0.3 | 2.0 | 4.6 | 8.8 |
| NV | **6.2** | – | 1.9 | 4.3 | 7.4 |
| AZ | **5.4** | 0.3 | 1.9 | 3.3 | 10.7 |
| WV | **4.7** | – | 0.4 | 4.3 | 6.4 |
| MO | **4.6** | 0.1 | 2.1 | 2.5 | 4.9 |
| UT | **4.5** | 0.1 | 1.0 | 3.4 | 11.7 |
| IL | **4.4** | 0.1 | 1.1 | 3.2 | 7.9 |

**House view by company (GW IT-eq, 2026-30)** — same rules and code; a hyperscaler self-build counts as naming its own tenant for rule 4 (as on the hyperscaler dashboard), which adds under 0.1 GW to the US total. A building counts for every company with a role on it, so never add rows or columns. Blank = the company has no such role in the census; – = it has the role but nothing survives the rules.

| Ticker | Operator / self-build | Named end user | Backer | Project financing | Power / equipment partner | Serving utility |
|---|---|---|---|---|---|---|
| [AMZN](../AMZN.md) | 25.9 | 8.58 |  |  |  |  |
| [MSFT](../MSFT.md) | 8.95 | 1.78 |  |  |  |  |
| [GOOG](../GOOG.md) | 13.1 | 5.13 |  | 3.73 |  |  |
| [META](../META.md) | 8.10 | 3.43 |  |  |  |  |
| [ORCL](../ORCL.md) | – | 5.70 |  |  |  |  |
| [AAPL](../AAPL.md) | 0.08 |  |  |  |  |  |
| [OPENAI](../OPENAI.md) | 1.39 | 9.85 |  |  |  |  |
| [ANTHROPIC](../ANTHROPIC.md) |  | 6.73 |  |  |  |  |
| [SPCX](../SPCX.md) | 0.97 |  |  |  |  |  |
| [CRWV](../CRWV.md) | 0.37 | 2.58 |  |  |  |  |
| [NBIS](../NBIS.md) | 1.65 | 0.23 |  |  |  |  |
| [NSCALE](../NSCALE.md) | 1.20 | 0.29 |  |  |  |  |
| [IREN](../IREN.md) | 3.44 |  |  |  |  |  |
| [TSLA](../TSLA.md) | 0.43 |  |  |  |  |  |
| [NVDA](../NVDA.md) |  | 1.49 | – | 3.19 |  |  |
| [AMD](../AMD.md) |  | 0.41 |  | 0.15 |  |  |
| [JPM](../JPM.md) | – |  |  | 1.16 |  |  |
| [GS](../GS.md) |  |  |  | 0.29 |  |  |
| [BX](../BX.md) |  |  | 4.24 |  |  |  |
| [KKR](../KKR.md) |  |  | 0.62 |  |  |  |
| [BLK](../BLK.md) |  |  | 1.40 | 0.87 |  |  |
| [OWL](../OWL.md) |  |  | 0.94 | 4.57 |  |  |
| [GEV](../GEV.md) |  |  |  |  | 5.52 |  |
| [BE](../BE.md) |  |  |  |  | 2.64 |  |
| [TLN](../TLN.md) |  |  |  |  | 0.77 | 0.77 |
| [VST](../VST.md) |  |  |  |  | 0.81 |  |
| [WMB](../WMB.md) |  |  |  |  | 0.35 |  |
<!-- aterio-house-view:end -->

## How to read it (basis traps)
- **Likelihood is Aterio's call, not ours.** High = the provider has negotiated power, secured land, financing lined up or capex committed on earnings calls; Low = a sign on a site with no power or financing signal; community pushback lowers a tier, backers or a signed lease raise it. Aterio's hit rates: **High >80% materialise, Medium ~50-60%, Low under 40% "even 30%"**; and *"Probability of getting built doesn't mean that they will actually meet timelines"* (Aterio team, Goldman Sachs call, 2026-10-20). Tiers can split one campus: Fermi America's first 200-300 MW tranche is High, its full 11 GW plan Low (same call; transcribed "Ferme America"). Active buildings carry no tier.
- **Facility, not IT.** `SELECTED_POWER_CAPACITY_MW` is facility power per building, published where Aterio has it and its own estimate otherwise. Facility/IT median 1.15 (n = 1,025 rows with both). Never put it on an IT-load or a GPU-power axis without converting, and never mix it with BTM generation nameplate.
- **Aterio's spoken totals are facility power too.** The Goldman Sachs call (2026-10-20) states no basis for its 55 GW active / 83 GW under construction. This export, seven weeks older, matches the call on the facility field and not on IT-eq: 51.8 GW active (45.1 IT-eq); 80.4 GW and 912 buildings under construction or delayed (69.9 IT-eq; stage Construction alone 71.5 GW / 821 buildings); 28.0 GW under construction dated 2027 against the call's "about 30". Capstone reads the call's figures as facility since 2026-11-10: **83 GW under construction = 72.2 GW IT-eq** (÷ 1.15), the anchor of the coverage check in [dc-delay-risk](../_dashboards/dc-delay-risk.html). Capstone reading, not an Aterio statement.
- **Building, not campus.** Rows are buildings. `TOT_PROJECT_COST` is campus-level and repeats on every building (naive sum $32.7tn vs ~$2.4tn de-duplicated). The reference deck's 139.5 GW "campuses under construction" reproduces only at campus level (every building on a campus with ≥1 building under construction).
- **Dates are mostly Aterio's estimates.** Only 20% of the 2026-30 not-yet-active MW carries a public-source activation date. Dates slip: of the 22.3 GW under construction on 2025-08-31 and dated after it, 88% (MW-weighted) now carries a later date, median +9 months; of 15.2 GW due by 2026-08-31, 3.9 GW is active.
- **Growth is partly coverage.** In the 12 months to 08-31 the census added 3,330 buildings / 308 GW, 78 GW of it announced before 2025-08-31 (backfill). Compare snapshots, not a snapshot against today's reconstruction.
- **Aterio counts site work as construction.** Clearing and grading are "Construction" in the census. Capstone's registry keeps a campus "announced" until vertical build when public sources say planned or pending (Microsoft La Porte, PowerHouse Carlisle, Meta Piqua, T5 Grayslake, Meta Henrico — dc-delay-risk, 2026-11-09).

## Key debates
- **How much of the pipeline gets built:** 383 GW planned is 5.3× what is under construction; even the High tier alone (205.1 GW in 2026-30, incl. most of what is under construction) is several years of record build. The tiers are the first haircut; permit pauses (Texas, Virginia, local moratoria) are the second — sized in [dc-delay-risk](../_dashboards/dc-delay-risk.html) and [ai-datacenter-power](ai-datacenter-power.md).
- **Census vs Capstone registry:** 86% of Aterio's 2026-30 construction (IT-eq) now sits on campuses the registry carries, after 56 Aterio-only campuses were added on 2026-11-09 against public sources; on 24 shared campuses the two disagreed, and in 8 checked cases public sources were ahead of Aterio (e.g. Crusoe Childress, Meridian Arc) (registry cross-check, 2026-11-09).
- **Who is building:** hyperscaler self-builds (AMZN, GOOG, META, MSFT, ORCL, AAPL as provider) are 38% of construction GW; Texas, Virginia and Georgia hold 42% (census 08-31).

## Who's exposed (companies)
MW facility; a building can count for several companies (operator, tenant, financier), so never add rows across companies. Roles come from Aterio's fields (`PROVIDER_*`, `END_USER_COMPANIES`, `PROVIDER_BACKED_BY`, `PROJECT_FINANCING_COMPANIES`, `CONSTRUCTION_EQUIPMENT_PROVIDER_COMPANIES`, utility, BTM inventory) and are not verified one by one. The full breakdown sits on each company page. This table stays on Aterio's basis (facility MW, every tier); the house view per company (GW IT-eq) is in the "Capstone house view" section above and on each company page.

| Ticker | Role in the census | Buildings | Active MW | Under constr. MW | 2026-30 not yet active: High · Medium · Low (MW) | Largest 2026-30 campus |
|---|---|---|---|---|---|---|
| [AMZN](../AMZN.md) | Operator / self-build | 839 | 10,164 | 10,084 | 28,554 · 3,399 · 86 | GW Ranch Project (TX) |
| [AMZN](../AMZN.md) | Named end user | 201 | 566 | 4,866 | 9,570 · 2,442 · 644 | Alpha Digital Campus (TX) |
| [AMZN](../AMZN.md) | BTM generation customer | 5 phases | – | – | nameplate 10,277 MW (no tier) | GW Ranch Energy Center (TX) |
| [MSFT](../MSFT.md) | Operator / self-build | 312 | 5,527 | 3,783 | 9,095 · 897 · 84 | Indiana 1, Microsoft Campus (IN) |
| [MSFT](../MSFT.md) | Named end user | 55 | 910 | 1,670 | 1,790 · 1,483 · – | Reeves County Campus (TX) |
| [MSFT](../MSFT.md) | BTM generation customer | 4 phases | – | – | nameplate 3,368 MW (no tier) | Kilby Power Plant (TX) |
| [GOOG](../GOOG.md) | Operator / self-build | 279 | 5,463 | 5,868 | 14,579 · 42 · – | Roman III (TX) |
| [GOOG](../GOOG.md) | Named end user | 46 | 168 | 3,866 | 5,820 · – · – | Project Spade (MO) |
| [GOOG](../GOOG.md) | Project financing | 28 | – | 1,240 | 4,295 · – · – | Nexus Hubbard Campus (TX) |
| [GOOG](../GOOG.md) | BTM generation customer | 7 phases | – | – | nameplate 4,950 MW (no tier) | BFC Power and Cheyenne Power Hub Project (WY) |
| [META](../META.md) | Operator / self-build | 237 | 4,831 | 7,088 | 8,386 · 1,789 · – | Hyperion, Meta Campus (LA) |
| [META](../META.md) | Named end user | 32 | 370 | 1,761 | 3,611 · – · – | Big Cedar Industrial Park (IA) |
| [META](../META.md) | BTM generation customer | 20 phases | – | – | nameplate 3,820 MW (no tier) | Socrates Power Solution Facilities (OH) |
| [ORCL](../ORCL.md) | Operator / self-build | 10 | 17 | – | – · – · – | – |
| [ORCL](../ORCL.md) | Named end user | 72 | 1,006 | 5,903 | 5,903 · – · – | OpenAI Stargate - Michigan Campus (MI) |
| [AAPL](../AAPL.md) | Operator / self-build | 18 | 449 | – | 92 · – · – | Maiden, Apple Campus (NC) |
| [OPENAI](../OPENAI.md) | Operator / self-build | 4 | – | – | 1,600 · – · – | Project Camellia (GA) |
| [OPENAI](../OPENAI.md) | Named end user | 106 | 1,485 | 6,561 | 10,524 · – · – | Ports Technology Campus (OH) |
| [ANTHROPIC](../ANTHROPIC.md) | Named end user | 68 | 1,408 | 3,013 | 7,259 · – · – | Nexus Hubbard Campus (TX) |
| [SPCX](../SPCX.md) | Operator / self-build | 8 | 1,278 | 620 | 620 · 1,000 · – | XAI Texas Campus (TX) |
| [SPCX](../SPCX.md) | BTM generation developer | 9 phases | – | – | nameplate 1,518 MW (no tier) | Colossus 2 (BTM) (MS) |
| [SPCX](../SPCX.md) | BTM generation customer | 9 phases | – | – | nameplate 1,518 MW (no tier) | Colossus 2 (BTM) (MS) |
| [CRWV](../CRWV.md) | Operator / self-build | 4 | 13 | 75 | 430 · – · – | The Northeast Science & Technology Campus (NJ) |
| [CRWV](../CRWV.md) | Named end user | 43 | 790 | 1,664 | 2,592 · 350 · – | Galaxy Helios Campus (TX) |
| [NBIS](../NBIS.md) | Operator / self-build | 13 | – | 500 | 1,900 · – · – | Nebius Pennsylvania Campus (PA) |
| [NBIS](../NBIS.md) | Named end user | 5 | 100 | 250 | 250 · – · – | NEP Real Estate Campus (NJ) |
| [NSCALE](../NSCALE.md) | Operator / self-build | 18 | – | 460 | 1,380 · 1,840 · – | Monarch Compute Campus (WV) |
| [NSCALE](../NSCALE.md) | Named end user | 5 | – | 219 | 339 · – · – | Cedarvale AI Campus (TX) |
| [NSCALE](../NSCALE.md) | BTM generation developer | 14 phases | – | – | nameplate 12,800 MW (no tier) | Monarch Cloud Campus (BTM) (WV) |
| [NSCALE](../NSCALE.md) | BTM generation customer | 14 phases | – | – | nameplate 12,800 MW (no tier) | Monarch Cloud Campus (BTM) (WV) |
| [IREN](../IREN.md) | Operator / self-build | 45 | 75 | 1,300 | 3,876 · – · – | Iren Sweetwater 1 (TX) |
| [CEREBRAS](../CEREBRAS.md) | Operator / self-build | 1 | 10 | – | – · – · – | – |
| [CEREBRAS](../CEREBRAS.md) | Named end user | 4 | 16 | – | – · 55 · – | AI Data Center (AL) |
| [TSLA](../TSLA.md) | Operator / self-build | 2 | 250 | 250 | 250 · – · – | Cortex 2.0 (TX) |
| [TSLA](../TSLA.md) | BTM generation equipment | 19 phases | – | – | nameplate 5,312 MW (no tier) | Fairfield Energy Center (OH) |
| [NVDA](../NVDA.md) | Named end user | 11 | – | 730 | 1,708 · 508 · – | South Valley Technology Park (NV) |
| [NVDA](../NVDA.md) | Owner / backer of the developer | 2 | – | – | – · – · – | – |
| [NVDA](../NVDA.md) | Project financing | 30 | – | – | 3,663 · – · – | Ports Technology Campus (OH) |
| [AMD](../AMD.md) | Named end user | 5 | 25 | 292 | 450 · – · – | Core Scientific Pecos Campus (TX) |
| [AMD](../AMD.md) | Project financing | 2 | – | 50 | 170 · – · – | Core Scientific Dalton Campus (GA) |
| [JPM](../JPM.md) | Operator / self-build | 2 | 25 | – | – · – · – | Project Sycamore (Phase 2) (NY) |
| [JPM](../JPM.md) | Project financing | 12 | – | 875 | 1,330 · – · – | El Paso, Meta Campus (TX) |
| [GS](../GS.md) | Project financing | 1 | – | 330 | 330 · – · – | Hut8 St Francisville Campus (LA) |
| [BX](../BX.md) | Owner / backer of the developer | 160 | 2,945 | 2,600 | 4,386 · 50 · – | Big Cedar Industrial Park (IA) |
| [KKR](../KKR.md) | Owner / backer of the developer | 70 | 1,085 | 247 | 645 · 31 · 255 | Yorkville, CyrusOne Campus (IL) |
| [BLK](../BLK.md) | Owner / backer of the developer | 36 | 802 | 933 | 1,394 · 108 · – | Conesville Industrial Park - Aligned (OH) |
| [BLK](../BLK.md) | Project financing | 11 | – | 545 | 1,000 · – · – | El Paso, Meta Campus (TX) |
| [OWL](../OWL.md) | Owner / backer of the developer | 49 | 838 | 510 | 576 · 473 · – | Lancium Clean - Project Stargate (TX) |
| [OWL](../OWL.md) | Project financing | 95 | 1,036 | 4,068 | 4,687 · 2,403 · – | Hyperion, Meta Campus (LA) |
| [GEV](../GEV.md) | Power / equipment / construction partner | 82 | 750 | 2,790 | 5,899 · – · – | Nexus Hubbard Campus (TX) |
| [GEV](../GEV.md) | BTM generation equipment | 34 phases | – | – | nameplate 22,430 MW (no tier) | Nexus Data Center Hubbard (BTM) (TX) |
| [BE](../BE.md) | Power / equipment / construction partner | 19 | 220 | 1,627 | 2,963 · 900 · – | Hedgehog Rice Power and Data Campus (TX) |
| [BE](../BE.md) | BTM generation equipment | 18 phases | – | – | nameplate 9,848 MW (no tier) | BFC Power and Cheyenne Power Hub Project (WY) |
| [TLN](../TLN.md) | Power / equipment / construction partner | 47 | 107 | 346 | 850 · 100 · – | Cumulus Data Center Campus (PA) |
| [TLN](../TLN.md) | Serving utility | 17 | 107 | 346 | 850 · – · – | Cumulus Data Center Campus (PA) |
| [TLN](../TLN.md) | BTM generation developer | 1 phases | – | – | nameplate – MW (no tier) | Anthony Township BTM (PA) |
| [VST](../VST.md) | Power / equipment / construction partner | 21 | – | – | 936 · – · – | Project Spectrum (TX) |
| [WMB](../WMB.md) | Power / equipment / construction partner | 6 | – | – | 400 · – · – | Project Azalea (GA) |
| [WMB](../WMB.md) | BTM generation developer | 19 phases | – | – | nameplate 3,454 MW (no tier) | Socrates Power Solution Facilities (OH) |
| [PWR](../PWR.md) | BTM generation equipment | 6 phases | – | – | nameplate 3,740 MW (no tier) | Delta Gigasite (BTM) (UT) |

## Sources
- Aterio export 2026-08-31: `P:\Felipe Monteiro\Aterio\data-centers\inventory\data_center_inventory_20260831.csv`, `power-generation\behind-the-meter-inventory\behind_the_meter_power_generation_inventory_20260831.csv`, monthly history, events, `Data Centers Data Dictionary.xlsx`, `reports\Aterio US Data Centers Weekly Report.xlsx` (licensed, internal use).
- Aterio team on a Goldman Sachs call, 2026-10-20: [render](../../relat%C3%B3rios%20bons/2026_10_20_aterio_gs_20_oct_2026.html) (ASR; speakers not confirmed).
- Derived: `_data/aterio/summary.json` (explorer), `_data/aterio/company_exposure.json` + `company_blocks/` (company view), `_data/dc_projects/aterio/xchk.json` + `registry_map.json` (registry cross-check).
- House view: rules in `_data/aterio/treatment.json` (decided by Felipe, 2026-11-09); `_data/aterio/capstone_view.json` (US total, states, sensitivity, vintages); `_data/aterio/theme_house_view.md` (the section above, as generated); `_data/aterio/hyperscalers.json`. One shared loader for every Aterio builder: `_tools/aterio_core.py`.

## Changelog

- 2026-11-10 — Meta source/aggregation audit: original 8.10 GW self-built and 3.43 GW tenant additions preserved; documented stock/flow, US scope, Hyperion timing, unresolved Bernstein comparison and source-field gaps. Corrected dashboard labels and unsupported common-basis/strict-floor claims. No census or treatment override. [Audit](../_meta/aterio-meta-audit-2026-11-10.md).
- 2026-11-09 — page created from the 08-31 export: market totals, likelihood tiers (definitions re-read in the GS call primary), basis traps, and the company table; matching sections added to 29 company pages.
- 2026-11-09 — added the "Capstone house view" section (Aterio census as of 2026-08-31, Capstone treatment; house rules of 2026-11-09): 186.1 GW IT-eq due in 2026-30 (214.0 GW facility) against 306.5 GW IT-eq on Aterio's own dating, band 169-186 GW on the facility/IT ratio; by year, by state and by company. A house-view table was added to the section on 28 company pages (PWR has only a behind-the-meter role). All Aterio builders now read the export through one loader (`_tools/aterio_core.py`); outputs were checked identical before and after. Facility tables on this page are unchanged; nothing superseded.
- 2026-11-10 — basis traps: added the reading of Aterio's Goldman Sachs call totals (2026-10-20; 55 GW active, 83 GW under construction, basis not stated on the call) as facility power, from the match with this export's facility field. Capstone treatment: 83 GW = 72.2 GW IT-eq. The delay model's coverage check used 83 GW as stated until this date (registry coverage 0.87; 1.00 after). Decided by Felipe, 2026-11-10. No figure on this page changed.
