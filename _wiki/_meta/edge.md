# Edge tracker — house vs Street

_Generated 2026-09-03 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| GOOG | Revenue $bn | 2026 | 505.00 | 426.70 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 548.30 | +17% |
| AAPL | EPS | 2026 | 10.12 | 8.71 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-09-03.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| 🔴 D-1 · 🔴 AVGO | the house FY28 EPS sits ABOVE the entire visible sell-side range | The house is +5.0% ABOVE the street high and +24.2% above the median. |
| 🔴 D-2 · 🔴 AVGO | the house implicitly assumes a ship rate the supply chain is not underwriting | The house is not merely above the guide — it is above the guide *for a specific mechanical reason*: it assumes AVGO converts more of its backlog than the supply chain has been converting. |
| D-3 · ⚠️ AVGO | BBG consensus is internally inconsistent one day after the print | The most likely reading is that the FY28 total-revenue line has not yet fully absorbed the $230bn AI guide |
| 🔴 D-4 · 🔴 CRWV | Jefferies is ~90% above consensus on CY28 EBIT, and the same gap shows up twice | This is the cleanest testable divergence of the night. |
| D-5 · ORCL | the PT is 18% above consensus, and the stated downside case IS consensus | Jefferies' bear case for FY30 is approximately what consensus already expects for FY29 |
| D-6 · NVDA | both the house AND consensus sit below the company's own growth framing | both the house AND consensus sit below the company's own growth framing |
| 🔴 D-7 · 🔴 MSFT | Jefferies' M365 series was published one day before the segment restatement and is now ~2pts low | Any Sep-26 print scored against Jefferies' 13.9% would read as a large beat that is purely definitional. |
| D-8 · GEV | a 4GW JV that contributes nothing inside the consensus horizon | The entire GEV contribution from the largest announced data-center turbine JV sits beyond the last year consensus forecasts. |
| — | D-9 · pre-existing house-vs-consensus gaps re-confirmed (not new tonight, but they frame the new sources) | D-9 · pre-existing house-vs-consensus gaps re-confirmed (not new tonight, but they frame the new sources) |

## Consensus PT vs spot — live pull in `reconciliation-2026-09-03.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| CRWV | 85 | 146 | +72% | street high 317 · low 39 below spot · 29/11/3 of 43 |
| ORCL | 154 | 245 | +59% | street high 400 · low 110 below spot · 42/8/1 of 51 |
| AVGO | 357 | 532 | +49% | street high 675 · low 350 below spot · 58/4/0 of 62 |
| NVDA | 228 | 323 | +41% | street high 515 · low 180 below spot · 79/2/1 of 82 |
| GEV | 942 | 1,239 | +32% | street high 1,450 · low 827 below spot · 33/7/2 of 42 |
| MSFT | 510 | 571 | +12% | street high 870 · low 400 below spot · 69/4/0 of 73 |
