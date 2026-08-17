# Edge tracker — house vs Street

_Generated 2026-08-17 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 11.57 | +66% |
| COHR | Revenue $bn | 2027 | 16.60 | 12.60 | +32% |
| NVDA | EPS | 2027 | 15.44 | 12.93 | +19% |
| GOOG | Revenue $bn | 2026 | 505.00 | 426.90 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.40 | +18% |
| NVDA | Revenue $bn | 2027 | 661.00 | 569.10 | +16% |
| AAPL | EPS | 2026 | 10.12 | 8.74 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-08-15.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| 🔴🔴 MU | consensus models an 86% CY27 gross margin, but management has just disclosed that most contracted volume is CEILINGED at CQ2-2026 pricing | The call sharpens from "86% may be a ceiling modelled as a base case" to: consensus needs ~415bp of pure cost-and-mix expansion off an already-record 81.9% base, on volume whose price is contractually capped. |
| 🔴 MU vs SNDK | the two largest LTA books are priced the OPPOSITE way round, and the wiki had been treating them as one trade | the two largest LTA books are priced the OPPOSITE way round, and the wiki had been treating them as one trade |
| 🔴 SNDK | Bernstein's Street-high $3,000 is built on a model that REJECTS the growth guide it endorses | Bernstein's Street-high $3,000 is built on a model that REJECTS the growth guide it endorses |
| 🔴 SNDK | consensus CY27 gross margin (84.3%) sits ABOVE the company's own FY28-30 target (~80%) | consensus CY27 gross margin (84.3%) sits ABOVE the company's own FY28-30 target (~80%) |
| AMAT | Arcuri's capacity-derived 2028 systems number is far above anything in the consensus trajectory | Arcuri's capacity-derived 2028 systems number is far above anything in the consensus trajectory |
| SNDK | the post-Investor-Day house cluster sits ABOVE the on-disk consensus, which has not yet caught up | the post-Investor-Day house cluster sits ABOVE the on-disk consensus, which has not yet caught up |
| SNDK | Citi is 33% ABOVE consensus in the out-year while 6% BELOW it in the near year | Citi is 33% ABOVE consensus in the out-year while 6% BELOW it in the near year |

## Consensus PT vs spot — live pull in `reconciliation-2026-08-15.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| MU | 1,034 | 1,586 | +53% | 🔴 **Largest upside in the run, on the deepest sample of the six — and it sits directly on top of item ①.** The Street pays a **53% premium to spot while carrying an 86.0% CY27 gross margin that is 415bp ABOVE the margin MU actually realised in the ceiling quarter** (see ①). The PT is not evidence the estimate is safe; it is the same estimate expressed as a target. **Divergence stands and is the highest-conviction row in the report.** |
| NVDA | 228 | 304 | +33% | ✅ **Highest-rated name in the run on the deepest sample anywhere (81 recs).** Consistent with ⑧/⑨: no estimate dispute near-term, the call is the calendar roll. **CONFIRMS.** |
| AMAT | 538 | 654 | +22% | ⚠️ Reads with ⑤ — the Street is constructive on the name but its **CY27→H1-28 revenue trajectory cannot accommodate Arcuri's systems number** (see ⑤). Upside is priced off the consensus trajectory, not off the capacity-doubling one. |
| SNDK | 1,812 | 2,196 | +21% | 🔴 Reads with ③: **Bernstein's Street-high $3,000 is +36.6% above the consensus PT of $2,196**, and +65.6% above spot vs the Street's +21.2%. The gap between the Street-high and the Street is **larger than the Street's entire upside case**. |
| KLAC | 206 | 235 | +14% | **Weakest conviction of the six** (4.29/5, the only sub-4.5 rating). KLAC contributes no quantitative row to this run — its TSMC-capex remark stays in the unquantifiable table. |
| LRCX | 342 | 377 | +10% | **Lowest upside of the six.** LRCX's only datapoint this run is the industry NAND-WFE figure, which is a **TAM line and not an LRCX revenue line** — see the basis-mismatch table. No estimate content. |
