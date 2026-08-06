# Edge tracker — house vs Street

_Generated 2026-08-06 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 10.00 | +92% |
| COHR | Revenue $bn | 2027 | 16.60 | 11.20 | +48% |
| LITE | EPS | 2027 | 30.02 | 23.96 | +25% |
| COHR | EPS | 2026 | 8.27 | 6.82 | +21% |
| NVDA | EPS | 2027 | 15.44 | 12.91 | +20% |
| GOOG | Revenue $bn | 2026 | 505.00 | 426.70 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.30 | +18% |
| NVDA | Revenue $bn | 2027 | 661.00 | 568.20 | +16% |
| AAPL | EPS | 2026 | 10.12 | 8.77 | +15% |

## Curated divergences — latest reconciliation (`reconciliation-2026-08-05.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| SPCX | CFO: Q3 and Q4 capex *"very similar to the current quarter"* → **~$18.4bn/qtr, ~$36.8bn for 2H26** | **Consensus is $9.9bn / 27% BELOW the guide, and 38% below on Q3 alone.** Snapshot is post-print, so the Street is mid-revision, not un-informed. **A negative cash-line revision is still to come, into a name whose bear case just migrated from segment losses to burn.** Watch whether Q3 converges to ~$18bn within two weeks; if not, Q3 is a capex miss waiting to happen. |
| SPCX | *"$100 billion of ARR… based on our expected revenue in the MONTH OF DECEMBER"* → **Dec-26 revenue must be ~$8.33bn** | **The two are not mutually consistent.** If Dec = $8.33bn, Oct+Nov = $9.45bn (avg $4.72bn/mo) vs a Q3 average of $4.13bn/mo — **an implied +76% single-month Nov→Dec step.** On a smooth ramp to $8.33bn, Q4 is ~$22.2bn and **consensus is ~20% too low.** The ramp mechanics are genuinely back-loaded (GOOG/ANTHROPIC deals + $6.7bn of new contracts all start in October), but annualizing one month flatters exactly this shape. **Resolves at the Q3 print.** |
| SPCX | Exit-2027: **~10 GW nameplate compute** AND **15-20 GW power-and-cooling**; **$30-50/W** Rubin monetization; **$1T revenue in 2030**; **"one flight a day"** by ~Aug-27 | **Management is 2-3x every Street baseline on the page, and the 15-20 GW power figure has NO Street or house baseline at all.** ⚠️ **Different GW bases — ~10 GW is IT load, 15-20 GW is power-plant level; never net them.** The overbuild is deliberate (*"far more power cooling and electrical equipment than we have GPUs"*), implying **~1.5-2x power capacity to IT load** — if that behaviour generalises, every GW sizing in `themes/ai-datacenter-power` built off IT load **understates the electrical/cooling order book by 50-100%.** ⚠️ FUNDA's six channel sources say 3.5-5 GW (P(8GW) ≈ 12-17%); treat as procurement INTENT. |
| CRWV | Two AlphaSense practitioners: high-end GPU prices decay **20-25% over 18 months** post-generation, and the **scarcity premium compresses** as supply matures | **Flatly contradictory — and the split is chronological: both expert views are Feb/Apr-2026 FORECASTS of compression; both August datapoints are OBSERVATIONS of the opposite.** Honest reading: the experts described the normal post-generation decay curve and the 2026 shortage has suspended it. **The open question for the whole neocloud complex is whether 20-25%/18mo reasserts when supply catches up.** ⚠️ Do NOT average. Track at the next contract-renewal datapoint. |

## Consensus PT vs spot — live pull in `reconciliation-2026-08-05.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
