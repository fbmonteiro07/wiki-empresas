# Theme — Hyperscaler Capex

_Wiki · generated 2026-06-25 · cross-company theme · sources: the AI_Demand_Capex project (`E:\AI_Demand_Capex`, dashboard build 2026-06-11), BBG consensus, company 10-Ks, and the official Capstone models (`P:\Felipe Monteiro\US Equities\Modelos oficiais`). Company pages: [../00_INDEX.md](../00_INDEX.md) · themes index: [00_THEMES.md](00_THEMES.md)._

> **Live dashboard:** [Capex Cloud](../_dashboards/hyperscaler-capex/Capex_Cloud.html) (snapshot in the wiki). Build source / source of truth: `E:\AI_Demand_Capex` (`build_capex_cloud.py` → also publishes to `E:\ASML - Copia\.publish_semicap\CapexCloud`). **TODO (next pass):** improve this dashboard with our own model data — see the house-model reconciliation below.

## What it is / why it matters
Hyperscaler capex (MSFT, AMZN, GOOGL, META, ORCL) is the single biggest **demand signal** for the entire AI hardware chain — GPUs/ASICs, memory, optical, power, semicap. Tracking the trajectory (and the gap between **consensus**, our **house model**, and the **street-high**) is how we size the cycle and judge whether the supply names are pricing too much or too little. This page is the synthesis layer over the AI_Demand_Capex dashboard.

## State of play (latest) — capex US$bn
Calendarized capex; 2025 = actual, 2026E/2027E = consensus mean vs street-high vs our house line.

| Name | 2025A | 2026E cons | 2026E st-high | 2026 **house** | 2027E cons | 2027E st-high | 2027 **house** |
|---|--:|--:|--:|--:|--:|--:|--:|
| MSFT | ~83 | 158 | 193 | 170 | 192 | 252 | 280 |
| AMZN | 132 | 199 | 208 | 200 | 228 | 277 | 300 |
| GOOGL | 91 | 187 | 192 | 180 | 242 | 305 | 285 |
| META | 70 | 135 | 145 | 125 | 162 | 202 | 160 |
| ORCL | 35 | 71 | 85 | 92 | 90 | 151 | 150 |

_(BBG consensus + actuals: AI_Demand_Capex `capex_cloud_data.js`, build 2026-06-11. "house" = the dashboard's `capstone` series — see the reconciliation below; it is NOT yet tied to the official models.)_

## Key debates
- **Bull / where the money is:** demand visibility keeps pulling guides up (GOOG 2026 capex guided $75B→$175-185B→$180-190B over four prints; MSFT/AMZN/META all raising). Backlog (GOOG Cloud $462B, ~2x q/q, Q1 2026) underwrites the spend (Google official model, Transcript Dashboard).
- **Bear / what could break it:** ROIC/FCF — GOOG FCF went negative in Q1 2026 ($-26.6B) as capex/rev hit ~32% (Google official model, Cash Flow tab). The debate is digestion/air-pocket risk if monetization lags the build.
- Watch the **consensus-vs-house-vs-street-high spread** as the positioning signal per name.

## Recent signals (Jun 24-25)
- **GOOGL '28 capex/build quantified by MS: 9 GW incremental, ~$375B capex (MS TMT / Skyler Risom, 2026-06-30).** MS's desk (relaying Nowak's $415 OW) sizes Alphabet's **'28 build at 9 GW** (~7 GW TPU + ~2 GW NVDA GPU) driving **capex to $350B '27 / $375B '28** ('27 raised +17% vs prior), with Core Cloud monetizing at $15/$18 per watt. Read for the capex theme: the house 2027 GOOGL line ($285-310B) is now below MS's $350B '27 — the street-high is migrating up as '28 TPU visibility improves. (MS TMT / Skyler Risom, 2026-06-30; see also [GOOG.md](../GOOG.md))
- **OpenAI Q1 cash burn ~$3.7B (~$15B annualized) (The Information, 2026-06-30).** A fresh quantified burn print on the largest single demand anchor behind hyperscaler/neocloud capex — feeds the "can the model companies fund the compute commitments" question underpinning the whole cycle, and the delayed-IPO (2027) capital-markets-tolerance debate. (The Information, 2026-06-30; see also [OPENAI.md](../OPENAI.md))
- **OpenAI leaning toward delaying IPO to 2027 — retail enthusiasm lacking at $1T+ valuation (Vital Knowledge / NYT, 2026-06-25).** OpenAI is now leaning toward delaying its IPO until **2027**, with both Vital Knowledge and the NYT citing that retail investor enthusiasm is insufficient at OpenAI's current private-market valuation ($1T+). This is a structural read-through for the AI capex cycle: (1) if OpenAI stays private longer, its capital raises remain private-markets-dependent (SoftBank Vision Fund, NVDA equity deals, Apollo/Blackstone SPVs) — capex-cycle continuity depends on PE/VC appetite, not equity-market sentiment; (2) the $1T+ valuation vs "retail enthusiasm lacking" frames a tension between model-company ARR ($47B+ run-rate per FundaAI) and public-market pricing tolerance — the same macro that is pushing hyperscaler PEs down. (Vital Knowledge / NYT, 2026-06-25; see also [OPENAI.md](../OPENAI.md))
- **MSFT positioned as indirect beneficiary of OpenAI Jalapeño (Broadcom ASIC) via IP ownership through 2031 (FinTwit, 2026-06-24).** Per QCOM Investor Day, OpenAI's custom chip "Jalapeño" (designed with Broadcom) has its IP owned by MSFT through 2031 under OpenAI investment terms. If Azure becomes the deployment fabric for OpenAI's Jalapeño-powered inference, the MSFT Azure capex-per-GW of inference effectively drops (substituting NVDA GPU $/kW with in-house-designed ASIC on a more favorable TCO curve). This is a **capex-mix story**, not a capex-magnitude story — MSFT's total DC spend stays elevated, but the composition shifts toward lower-cost inference per GW as Jalapeño ramps. Net: MSFT's capex spend is unchanged in aggregate, but the efficiency per dollar of inference improves. (@SouthernValue95; @PatrickMoorhead, 2026-06-24; see also [MSFT.md](../MSFT.md))
- **BofA framing: "internet stocks could rotate back" as AI capex compounds (BofA context, 2026-06-24).** The broader BofA tech-strategy read (from their AI 2030 note, referenced in their June flows) is that the AI capex cycle is now large enough that "internet stocks could rotate back" — with advertising and software beneficiaries (META, GOOG, MSFT apps) seeing a second-wave re-rate as AI monetization proves out, rotating capital away from the picks-and-shovels semis (NVDA, AVGO) that have already re-rated. For the capex theme: this reframe does not change the capital flows but suggests the **equity leadership in the cycle is rotating from suppliers to users**, which is a read-through for the relative trade (hyperscalers vs semis into the second half of 2026). (BofA "AI 2030", 2026-05-13; buy-side desk feedback, 2026-06-24)
- **AWS monetizing the shortage; Anthropic pushing back on price (BofA / Rothschild, 2026-06-30).** AWS is raising fees **+20% on select GPU workloads** (on top of the +20% EC2 Capacity Block hike effective Jul 1) — a **1-2pt benefit to 2H26 AWS growth** (BofA / Justin Post) — evidence that hyperscalers are recouping capex via compute pricing power as supply stays tight. Counter-signal on the model-layer economics: **Anthropic is renegotiating a key part of its Amazon partnership, changing how Amazon pays to use Anthropic's models next year** (R&Co: Anthropic "flexing pricing power over Amazon"; Neutral) — a reminder that the frontier labs can claw back some of the value in the capex-for-tokens exchange. (BofA / Justin Post; Rothschild & Co / Rowan Adley, 2026-06-30; see also [AMZN.md](../AMZN.md))

## House-model reconciliation (cross-check, 2026-06-25)
The dashboard's `capstone` line does **NOT** currently match the official Capstone models — and only GOOG + META have official models at all.

| Name | Dashboard house 25/26/27 | Official model (canonical Summary tab) | Verdict |
|---|--|--|--|
| GOOGL | 91.4 / 180 / 285 | 91.4 / **182.7** / **310** (Google model, Summary) | 2025 ✓; 2026 & 2027 ✗ (model Summary 2027 = 310; the 285 matches the model's *Chip-breakdown* tab, not Summary). Model is internally inconsistent: 2027 capex reads 280 / 285 / 310 across tabs. |
| META | 72 / 125 / 160 | 69.9 / **130.9** / **169.6** (Meta model, Meta Summary) | none cleanly match. 2025 dashboard (72) > actual (~69.7); 2026 (125) matches the model's *PP&E Detail / guidance* path but not Summary (131); 2027 (160) ≠ either tab (150 vs 170). |
| MSFT | 104.6 / 170 / 280 | — **no official model** | unverifiable |
| AMZN | 132 / 200 / 300 | — **no official model** | unverifiable |
| ORCL | 33.1 / 92 / 150 | — **no official model** | unverifiable |

**Takeaways:** (1) the dashboard house line is stale/decoupled from the official GOOG/META models; (2) the official models disagree *with themselves* across tabs (Summary vs PP&E/Chip-build/Scenarios) — pick one canonical capex row before wiring; (3) we have **no** official MSFT/AMZN/ORCL model, so those house lines are placeholders. This is the "improve later" work the dashboard needs.

## Who's exposed (companies)
| Ticker | Angle | Read |
|---|---|---|
| [MSFT](../MSFT.md) | Azure capex | guide ramping; no official model yet |
| [AMZN](../AMZN.md) | AWS + Trainium capex | highest absolute spend; no official model yet |
| [GOOG](../GOOG.md) | TPU + Cloud capex | official model exists (Summary 26/27 = 182.7/310) |
| [META](../META.md) | AI infra capex | official model exists (guidance path 125 in '26) |
| [ORCL](../ORCL.md) | OCI capex | fastest % ramp off a small base; no official model yet |

Downstream read-throughs: [NVDA](../NVDA.md), [AVGO](../AVGO.md), [TSM](../TSM.md), [VRT](../VRT.md) and the [800v-dc-power](800v-dc-power.md) / [ai-datacenter-power](ai-datacenter-power.md) / [custom-asic-tpu](custom-asic-tpu.md) themes.

## Sources
- **Dashboard / data:** [Capex Cloud](../_dashboards/hyperscaler-capex/Capex_Cloud.html) · build source `E:\AI_Demand_Capex` (`build_capex_cloud.py`, `capex_cloud_data.js`, `ppe_data.js`), build 2026-06-11.
- **Official Capstone models:** `P:\Felipe Monteiro\US Equities\Modelos oficiais\Google Modelo oficial.xlsx` (Summary tab, CapEx row), `…\Modelo Meta pós 2Q26.xlsm` (Meta Summary / PP&E Detail tabs). No MSFT/AMZN/ORCL model on disk.
- **Consensus:** BBG (BEST_CAPEX), via the dashboard. **Actuals:** company 10-Ks / press releases.

## Changelog
- 2026-06-25 — page created; folded the AI_Demand_Capex dashboard into the wiki (snapshot under `_dashboards/`). Ran a house-model cross-check: dashboard `capstone` capex does NOT match the official GOOG/META models (2026/2027 differ), models are internally inconsistent across tabs, and MSFT/AMZN/ORCL have no official model. Flagged for the dashboard-improvement pass.
