# Edge tracker — house vs Street

_Generated 2026-09-11 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| GOOG | Revenue $bn | 2026 | 505.00 | 427.40 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 547.10 | +17% |
| AAPL | EPS | 2026 | 10.12 | 8.74 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-09-10.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| ORCL | management's RPO conversion pace contests the standing BofA bear, but the bases differ | management's RPO conversion pace contests the standing BofA bear, but the bases differ |
| NVDA | the Capstone house model is ~7pp below both management and consensus on FY28 growth | the Capstone house model is ~7pp below both management and consensus on FY28 growth |
| META | JPM's PT went up 28% on zero change to earnings | So the upgrade is a re-rate, not a revision. |
| PANW | Morgan Stanley calls it a Top Pick with a price target below the Street median | Morgan Stanley calls it a Top Pick with a price target below the Street median |
| NVDA | Morgan Stanley is Overweight on below-consensus numbers and a below-consensus target | Read the OW as an options position on rev-share, not as an earnings call. |
| NVDA | the same house is Overweight the equity and sidelined on the credit, on one webcast | the same house is Overweight the equity and sidelined on the credit, on one webcast |
| ORCL | the Street's post-print revision underwrites ~8% of the new RPO, and almost none of it lands in FY28 _(opened 2026-09-11 out of §1's corollary)_ | $2.08bn of cumulative revenue added across three fiscal years against +$26bn of new RPO booked in the quarter — ~8% of the gross backlog addition. |

## Consensus PT vs spot — live pull in `reconciliation-2026-09-10.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| ORCL | 153 | 243 | +58% | street high 400 · low 110 below spot · 40/8/1 of 49 |
| NVDA | 220 | 325 | +48% | street high 515 · low 180 below spot · 79/2/1 of 82 |
| PANW | 327 | 401 | +22% | street high 475 · low 190 below spot · 47/12/1 of 60 |
| CRWD | 205 | 239 | +17% | street high 425 · low 119 below spot · 41/14/1 of 56 |
| META | 651 | 751 | +15% | street high 1,000 · low 580 below spot · 72/7/0 of 79 |
