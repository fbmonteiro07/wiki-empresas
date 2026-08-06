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
| GOOG | Revenue $bn | 2026 | 505.00 | 426.80 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.30 | +18% |
| NVDA | Revenue $bn | 2027 | 661.00 | 568.20 | +16% |
| AAPL | EPS | 2026 | 10.12 | 8.77 | +15% |

## Curated divergences — latest reconciliation (`reconciliation-2026-08-05.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| SPCX | CFO: Q3 and Q4 capex *"very similar to the current quarter"* → **~$18.4bn/qtr, ~$36.8bn for 2H26** | 🔴 **STAYS — and the Q3 leg STRENGTHENED.** _Original 08-05 read:_ consensus $9.9bn / 27% below the guide, 38% below on Q3 alone; snapshot post-print so the Street was mid-revision, not un-informed; a negative cash-line revision still to come into a name whose bear case just migrated from segment losses to burn; **watch whether Q3 converges to ~$18bn within two weeks.** → ✅ **RESOLVED 08-06: it did NOT converge — it FELL to $10.83bn (−41.1% vs guide).** The Street absorbed the guide into **Q4 alone** (now −1.1% vs guide). **Not one analyst is at the Q3 guide — the street high is still 21% below it.** 2H gap narrows to $7.8bn / 21%, but only via Q4. **Consensus is modelling a back-half-loaded capex curve management explicitly denied — so the Q3 capex miss is MORE likely now, not less.** |
| SPCX | *"$100 billion of ARR… based on our expected revenue in the MONTH OF DECEMBER"* → **Dec-26 revenue must be ~$8.33bn** | **The two are not mutually consistent.** _Original 08-05:_ if Dec = $8.33bn, Oct+Nov = $9.45bn (avg $4.72bn/mo) vs a Q3 average of $4.13bn/mo — **an implied +76% single-month Nov→Dec step**; on a smooth ramp Q4 is ~$22.2bn and consensus ~20% too low. → ✅ **08-06: NARROWS, and the direction of revision SUPPORTS the finding.** Oct+Nov now $10.38bn (avg $5.19/mo) vs Q3 avg $4.24/mo ⟹ implied Nov→Dec step **+76% → +61%**; consensus now **15.7% below** the smooth-ramp $22.2bn. **The street high ($29.44bn) sits ABOVE the smooth ramp — the bull tail is already underwriting the December-weighted quarter.** Still not reconciled; **resolves at the Q3 print (early Nov).** |
| SPCX | Exit-2027: **~10 GW nameplate compute** AND **15-20 GW power-and-cooling**; **$30-50/W** Rubin monetization; **$1T revenue in 2030**; **"one flight a day"** by ~Aug-27 | **Management is 2-3x every Street baseline on the page, and the 15-20 GW power figure has NO Street or house baseline at all.** ⚠️ **Different GW bases — ~10 GW is IT load, 15-20 GW is power-plant level; never net them.** The overbuild is deliberate (*"far more power cooling and electrical equipment than we have GPUs"*), implying **~1.5-2x power capacity to IT load** — if that behaviour generalises, every GW sizing in `themes/ai-datacenter-power` built off IT load **understates the electrical/cooling order book by 50-100%.** ⚠️ FUNDA's six channel sources say 3.5-5 GW (P(8GW) ≈ 12-17%); treat as procurement INTENT. |
| CRWV | Two AlphaSense practitioners: high-end GPU prices decay **20-25% over 18 months** post-generation, and the **scarcity premium compresses** as supply matures | **Flatly contradictory — and the split is chronological: both expert views are Feb/Apr-2026 FORECASTS of compression; both August datapoints are OBSERVATIONS of the opposite.** Honest reading: the experts described the normal post-generation decay curve and the 2026 shortage has suspended it. **The open question for the whole neocloud complex is whether 20-25%/18mo reasserts when supply catches up.** ⚠️ Do NOT average. Track at the next contract-renewal datapoint. ✅ **08-06: consensus did not move a decimal, so the pricing-regime question is entirely UNEXPRESSED in estimates — this stays open with no consensus anchor either way.** |

## Consensus PT vs spot — live pull in `reconciliation-2026-08-05.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| SPCX | 112 | 222 | +99% | 🔴 **The Street carries +99% upside on a name whose own Q3 capex consensus sits 41% BELOW the guide management just gave.** PT unmoved on the print ($222.60 on 08-05) even though consensus revenue and capex both moved — the PT is not yet reflecting the cash line. |
| CRWV | 89 | 139 | +56% | Consensus estimates unmoved to the decimal this run; the GPU-pricing-regime debate (④) is unexpressed in both estimates and PT. |
| NBIS | 211 | 265 | +26% | Neocloud comp read-across for ④; no new datapoint this run. |
| AMZN | 274 | 326 | +19% | 📌long. Highest-rated name in the run; CY2026 capex $214.16bn confirms mid-guide. Lowest upside of the four — the least contested. |
