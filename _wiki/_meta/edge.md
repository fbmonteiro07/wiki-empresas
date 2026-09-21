# Edge tracker — house vs Street

_Generated 2026-09-20 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| GOOG | Revenue $bn | 2026 | 505.00 | 427.20 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.10 | +18% |
| AAPL | EPS | 2026 | 10.12 | 8.76 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-09-18.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| ★★ — | Cumulative burn: the company's own plan is 2.5x the number this page carried | Cumulative burn: the company's own plan is 2.5x the number this page carried |
| ★ — | Revenue ladder: the company plan runs ~20% above the Barclays-relayed plan in 2026 and ends at $350bn in 2030 | Revenue ladder: the company plan runs ~20% above the Barclays-relayed plan in 2026 and ends at $350bn in 2030 |
| ★ — | Compute + infrastructure spend: $856bn through 2030 vs the page's $650bn obligations / $450bn opex plan | Compute + infrastructure spend: $856bn through 2030 vs the page's $650bn obligations / $450bn opex plan |
| — | Liquidity and valuation: the runway is now dated, and it changes the read on the $1.2tn round | Liquidity and valuation: the runway is now dated, and it changes the read on the $1.2tn round |
| — | IPO: the autumn target is gone | IPO: the autumn target is gone |
| ★★ — | [[NFLX]]: the downgrade is a MULTIPLE call, not an estimate call — and it created the Street's only SELL | Wells Fargo cut its numbers by 1-3% and its price target by 29% — the entire call is the de-rating, not the model. |
| ★★ AI capex 2030: three marks in one week | and two of them are NOT comparable | On the only comparable pair, New Street is ~38% above BofA — and BofA sits almost exactly where New Street itself sat before this note. |
| ★★ HBM 2030: four marks, all agreeing on 2025 | and New Street is ~2x the next highest | All four agree within ~3% on the 2025 base and then fan out 3.3x by 2030 — and NSR and the house agree at ~$190bn in 2027, so the entire disagreement is the 2028-30 compounding. |
| ★★ — | CXMT passes [[MU]]: two houses, two days apart, two years apart | Morgan Stanley has CXMT surpassing Micron in DRAM capacity by 2028; Deutsche Bank's model has it happening only in 2030. |
| ★★ — | [[AVGO]] AI revenue: JPM is above the company's own framing in FY27 and FY28 | Two independent sources put FY28 AI revenue at $230bn — the number this wiki already carried as the company's own guide — and JPM is $15bn above it, with the real gap in FY27, i.e. a pull-forward call rather than a bigger-end-state call. |
| ★ — | [[MRVL]]: JPM's data-center-only CY28 exceeds consensus for the whole company | JPM models Marvell data-center revenue at ~$28bn in CY28 against a BBG consensus of $26.3bn for total Marvell revenue in the matching fiscal year — the segment alone is ~6% above the company. |
| ★ [[MU]]: Deutsche Bank is 7% above consensus on FY27 EPS | and the CY block would have manufactured a fake −24% | DB sits essentially at consensus on the year in progress and 7% above it on FY27, still inside the Street high — a timing call, consistent with its own supply table. |
| ★★ — | [[SNDK]]: the wiki's nine HBF marks are not nine independent observations | A BofA-hosted expert says there is still no measured HBF silicon — power, thermals, delivered bandwidth and latency are all unmeasured — and that the Hot Chips comparison was *"based on just what the Sandisk numbers are. What they are targeting." |
| ★ — | HBM/DRAM LTA coverage: the broker is more locked-up than the company says it is | JPM's deck says ">70% of total wafers for BOTH DRAM and NAND" are under long-term agreement; Samsung management, the same week, says 30-40% of its capacity is NOT bound by LTAs — i.e. 60-70%. |
| ★ [[SAMSUNG]]: a single method variable | the preferred discount — is essentially the entire PT gap | Goldman applies a 27% target discount to the preferred and BofA applies 32%; those five points are almost exactly the W360,000-vs-W340,000 difference between the two targets on the same name on the same day. |
| ★ — | Rubin Ultra de-spec: two magnitudes that cannot both describe the same change | Deutsche Bank describes 12-Hi HBM4e → HBM4/HBM4e 8-Hi (about −⅓); SemiAnalysis describes "1024GB to now ~200GB of HBM per chip" (about −80%). |
| — | HBM stack height: a three-way, 4x-wide split published inside one week | SemiAnalysis argues 4-hi gives the best $/bandwidth and that stacks could go lower still; Intel Technology Research says reducing stack height would not reduce the capacity requirement; BofA Korea models *more* dies per stack (16-hi, 20-hi). |

## Consensus PT vs spot — live pull in `reconciliation-2026-09-18.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| SAMSUNG | 261,000 | 490,018 | +88% | street high 725,000 · low 300,000 ABOVE spot · 44/0/0 of 44 |
| ORCL | 148 | 240 | +63% | street high 400 · low 110 below spot · 40/8/1 of 49 |
| MU | 1,016 | 1,578 | +55% | street high 2,200 · low 900 below spot · 57/4/0 of 61 |
| AVGO | 358 | 532 | +49% | street high 715 · low 350 below spot · 58/4/0 of 62 |
| WDC | 441 | 656 | +49% | street high 900 · low 525 ABOVE spot · 22/6/0 of 28 |
| ASML | 1,680 | 2,459 | +46% | street high 2,859 · low 2,100 ABOVE spot · 21/0/0 of 21 |
| NVDA | 222 | 323 | +45% | street high 515 · low 180 below spot · 79/2/1 of 82 |
| UBER | 70 | 102 | +45% | street high 150 · low 70 below spot · 49/8/1 of 58 |
| NFLX | 72 | 95 | +32% | street high 135 · low 57 below spot · 49/15/1 of 65 |
| SNDK | 1,792 | 2,288 | +28% | street high 3,900 · low 1,400 below spot · 27/4/0 of 31 |
| MRVL | 244 | 289 | +18% | street high 400 · low 143 below spot · 47/5/0 of 52 |
