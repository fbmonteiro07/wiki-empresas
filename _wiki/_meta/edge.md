# Edge tracker — house vs Street

_Generated 2026-08-24 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 11.89 | +62% |
| COHR | Revenue $bn | 2027 | 16.60 | 12.70 | +31% |
| NVDA | EPS | 2027 | 15.44 | 12.97 | +19% |
| GOOG | Revenue $bn | 2026 | 505.00 | 427.50 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.30 | +18% |
| AAPL | EPS | 2026 | 10.12 | 8.76 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-08-24.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| 🔴🔴 HBM 2027 ASP | UBS +90% vs JPM +42%. The widest pricing gap on the wiki. | ACTION: resolve at the 4Q26 / January disclosures, or by rebuilding UBS's blended ASP on JPM's $/Gb basis from the `SKH HBM` / `Samsung HBM` sheets in `JPM_HBM_client_model_Aug2026.xlsx` (now archived in `_inbox\_done\`). Until then, do not quote either number without its basis. OPEN. |
| 🔴 MRVL CY28 EPS | Wells Fargo ~$11/sh vs UBS $9.82: +12.0%, and the two most recent PTs move in opposite directions. | So the open MRVL question is now the MULTIPLE, not the earnings power |
| Samsung FY27 operating profit | Goldman W561.7tn is −3.8% below consensus, and the house spread stays ~15% wide. | Goldman W561.7tn is −3.8% below consensus, and the house spread stays ~15% wide. |
| Samsung EPS | UBS is −6.2% below consensus for CY26 while +25.6% above for CY28. A duration disagreement, not a level one. | UBS is −6.2% below consensus for CY26 while +25.6% above for CY28. A duration disagreement, not a level one. |
| "Vera Rubin crushes Blackwell" | disconfirmed by its own primary. | Not a valuation item, but a corpus-integrity one: a relay claim that the primary does not support, caught only because the primary arrived. |

## Consensus PT vs spot — live pull in `reconciliation-2026-08-24.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
