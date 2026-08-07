# Edge tracker — house vs Street

_Generated 2026-08-07 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 10.00 | +92% |
| COHR | Revenue $bn | 2027 | 16.60 | 11.20 | +48% |
| LITE | EPS | 2027 | 30.02 | 23.96 | +25% |
| COHR | EPS | 2026 | 8.27 | 6.82 | +21% |
| NVDA | EPS | 2027 | 15.44 | 12.91 | +20% |
| GOOG | Revenue $bn | 2026 | 505.00 | 426.80 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.30 | +18% |
| NVDA | Revenue $bn | 2027 | 661.00 | 568.20 | +16% |
| AAPL | EPS | 2026 | 10.12 | 8.77 | +15% |

## Curated divergences — latest reconciliation (`reconciliation-2026-08-06.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| GOOG | Mgmt 2026 capex guide **$195-205bn**; BBG CY26 **$200.8bn** | ① House is stale to the 07-22 raise — 2027 matches BBG to the decimal, so this is a missed update, not a call. Fix before any capex/FCF work. |
| PLTR | Q2 **+93% y/y** actual; FY26 guide **$8.15bn** | ② The steep decel is unexpressed in consensus and is the cleanest long-side read of the RSI thesis in the book — but FUNDA's own FDE-compression argument cuts the other way. Both legs on page. |
| PLTR | FUNDA: Q1'26 **+85%**, "**ARR >$6.5B**" | ③ **Do not propagate.** Must not be mixed with US Commercial RDV $6.238bn (different metric, similar level). Resolve vs the Q1'26 10-Q. |
| AMZN | FUNDA (Oct-25) Trainium **order book 2.2-2.6M** units for 2026 | ④ Three bases, never netted. A reusable **calibration prior** on how much an early order book overstates output — NOT a revision. CoWoS leg scored far better than the unit leg. |
| AMZN | FUNDA Project Rainier **4.5GW** / 3 campuses | ⑤a Facility vs IT-load never stated. All three stand per the `assumptions.md` GW rule. |
| GOOG | FUNDA Anthropic deal "**up to 1M TPUs**" | ⑤b Filed as a unit-contract **ceiling**, not netted against the GW or $ marks. |
| macro | FUNDA: semis' worst month since **2002** | ⑤c Instrument/window mismatch (SOX vs SOXX vs broad basket). Both retained; any use must name the index. |
| GOOG | — | ⑥ **CY-sum defect — use sum-of-quarters, do not cite.** Second ticker showing this class after the SPCX capex bug (08-05). |

## Consensus PT vs spot — live pull in `reconciliation-2026-08-06.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
