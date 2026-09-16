# Edge tracker — house vs Street

_Generated 2026-09-15 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| GOOG | Revenue $bn | 2026 | 505.00 | 427.40 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 545.30 | +18% |
| AAPL | EPS | 2026 | 10.12 | 8.76 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-09-15.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| 🔴🔴🔴 — | The relay that reached the wiki at 21:00 carried a mechanism that is not in the primary — and it pointed the opposite way | This is the third run in which a desk relay reached the wiki before the primary and distorted it. |
| 🔴🔴🔴 AMZN | Bernstein is +16% / +27% above consensus on FY27 / FY28 EBIT and still carries a PT below consensus | The tension is internal to Bernstein and it is large. |
| 🔴🔴 ASML | the house EUV model takes the 110 as the number, which is exactly what tonight's note says it is not | Sizing the gap on the house model's own ASP: |
| 🔴🔴 ASML | Bernstein's estimates are consensus, but its PT is +22.8% above consensus | On FY27 EBIT the two are within 0.1% of each other. |
| 🔴🔴 NET | a Market-Perform whose PT implies ≈−50%, while the same analyst's estimates sit above the company's own guide | The estimates and the target contradict each other, and the estimates are the more testable half. |
| 🔴 DDOG | above consensus on EPS in both years, 18% below on PT | above consensus on EPS in both years, 18% below on PT |
| ASML | a vintage/basis conflict on "current" throughput, flagged and not resolved | a vintage/basis conflict on "current" throughput, flagged and not resolved |

## Consensus PT vs spot — live pull in `reconciliation-2026-09-15.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| ASML | 1,591 | 2,459 | +55% | street high 2,859 · low 2,100 ABOVE spot · 21/0/0 of 21 |
| NVDA | 212 | 325 | +53% | street high 515 · low 180 below spot · 79/2/1 of 82 |
| LRCX | 271 | 377 | +39% | street high 475 · low 285 ABOVE spot · 31/6/0 of 37 |
| AMZN | 248 | 330 | +33% | street high 405 · low 230 below spot · 77/4/0 of 81 |
| DDOG | 230 | 289 | +26% | street high 340 · low 158 below spot · 46/3/1 of 50 |
| NET | 327 | 342 | +5% | street high 400 · low 160 below spot · 27/7/3 of 37 |
