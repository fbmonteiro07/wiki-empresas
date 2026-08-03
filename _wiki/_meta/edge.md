# Edge tracker — house vs Street

_Generated 2026-08-03 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 10.00 | +92% |
| COHR | Revenue $bn | 2027 | 16.60 | 11.20 | +48% |
| LITE | EPS | 2027 | 30.02 | 23.90 | +26% |
| COHR | EPS | 2026 | 8.27 | 6.82 | +21% |
| NVDA | EPS | 2027 | 15.44 | 12.91 | +20% |
| GOOG | Revenue $bn | 2026 | 505.00 | 426.70 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.30 | +18% |
| NVDA | Revenue $bn | 2027 | 661.00 | 568.20 | +16% |
| AAPL | EPS | 2026 | 10.12 | 8.77 | +15% |

## Curated divergences — latest reconciliation (`reconciliation-2026-08-01.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| TER | ① Mgmt re-cut FY26 to 50-52% of revenue in H1 → FY26 rev ≈ $5.00-5.22B; H1 non-GAAP EPS already $5.02 | 🔴 **Not an edge — a broken model.** House is **-32% vs the CY26 line, -39% vs sum-of-quarters and -39% vs CY27**, and H1 actual EPS alone is 92% of the full-year house number. Unchanged on the live pull. **Re-mark the TER line before it is used in any screen, comp or edge calc; until then every "house vs consensus" edge shown for TER is an artefact.** |
| KLAC | ② Higgins softened "CY27 > CY26" to **"≈ CY26"** (mid-20s WFE growth on ~$190B), Q4 FY26 call 2026-07-28 | 🟠 **The alpha is the derivative, not the level.** Management dropped the acceleration commitment and consensus responded by nudging CY27 growth **up 0.2pt**, not down — the Street is still modelling continuation. Nobody reported the Q&A retraction. **Strip ">"-based acceleration language from the CY27 bull case.** |
| KLAC | ③ Memory-component cost hit *"around 100bps, probably a little bit more… continues through 2027"*; declined to endorse a Dec step-up | 🟠 Consensus still expands CY27 GM *through* the headwind management says persists. **Small: flat GM costs ~$119M gross profit ≈ $0.08 CY27 EPS (~1.3%).** Directional, not P&L-material — read with ④. Sinal row re-scored ✓ → ⚠ nuança. |
| KLAC | ④ Higgins on pricing: *"pretty hard to go back to your customers after you've taken orders and start to change prices"* — resets deferred to new products | 🔴 **Structural, and the most durable item in the run.** UBS's name-specific call (KLAC least likely to price) is now confirmed on tape; the theme's sector generalisation is corrected to **ASML and LRCX monetise via price, KLAC does not**. Combined ②+③+④ migrates the bear case from a revisions call to a **valuation call: the one large-cap semicap without a pricing lever, growing ≈ in line in CY27, at the highest multiple in the group.** ✅ Cross-read positive for [[ASML]]. |
| TER | ⑤ BBG's CY2026 aggregate reads **-3.5% rev / -9.8% EPS below the sum of BBG's own quarterly lines** | 🔴 **Hypothesis was wrong and the re-run does NOT fix it — root cause now identified and it is ours, not Bloomberg's.** Our CY aggregate re-pulls already-reported quarters via `BEST_FPERIOD_OVERRIDE`, which returns the **pre-print consensus mean, not the comparable actual** — so every CY2026 line understates a beat. Probe: TER Q1 actual $1,282.5M/$2.56 vs `-1FQ` $1,215.0M/$2.107; Q2 $1,329.0M/$2.47 vs `0FQ` $1,217.2M/$2.044 → **-$179.3M / -$0.88, matching the gap exactly.** **Systematic across all 97 names — every one has ≥1 reported 2026 quarter embedded in its CY2026 line (KLAC: -$102M/-1.6%); CY2027 (n_actual=0 for all 97) is clean.** See method flag 7. |
| TER | ⑥ CPO test *"$300-700M market by 2028"*, but 2027 *"aiming towards more of the low side… low-end would be in the $200 million range"* | 🟡 **Phasing correction, not a thesis break** — ~$100M 2026 → ~$200M 2027 → $300-700M 2028, with 2028 contingent on scale-out ramps succeeding *during* 2027. Relevant to anyone underwriting CPO in TER's or [[ADVANTEST]]'s CY27. ⚠️ TER also warned it and a customer had **entirely different definitions of insertion 2** — discount every insertion-share % on the page. |
| ADVANTEST | ⑦ Advantest guided to gaining SOC / losing memory share; TER's CEO agreed on memory but called SOC *"pretty flat, maybe a slight incremental gain for us"* | 🟡 **Both cannot be gaining SOC share unless the donor is a smaller vendor** — logged as an open contradiction, settles with FY2026 final ATE share data (~April 2027). **PT placement now live: Bernstein ¥39,200 is only +2% vs the cons median — the Street median, not a Street-high. JEF ¥30,000 is -18% below the median and still BELOW spot** — 2 months stale and not Buy-consistent; treat as un-refreshed. |

## Consensus PT vs spot — live pull in `reconciliation-2026-08-01.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| ASML | 1,415 | 2,013 | +42% | Highest upside of the semicap set — consistent with ④'s cross-read (ASML monetises the cycle via price, KLAC does not). Bernstein's €2,300 Best-Idea PT is +14% vs the median. |
| KLAC | 178 | 236 | +32% | Cons median sits between GS $230 and UBS $240; MS $274 is the true high mark, Bernstein $197.50 the true low. Stock below every published PT on the page. |
| GLW | 144 | 189 | +31% | MS $180 is now **-4.9% BELOW the median** — the 07-21 "above-mean PT" framing is stale (note's own mean was $158.87 on 07-20). |
| CRM | 189 | 245 | +30% | MS $185 is **-24.6% below the median and below spot** — confirms the downgrade as a genuine Street-low. |
| SHOP | 118 | 150 | +27% | Redburn's $130 is **-13.4% below the median** — confirms the structural bear. |
| META | 594 | 752 | +27% | Redburn's $1,000 (07-21 report) is **+32.9% above the median** — top-of-street, the aggressive-bull anchor. |
| TER | 359 | 451 | +26% | House peer-model EPS is -32%/-39% vs the CY26/CY27 consensus lines (①) — the PT gap is Street-wide optimism, not a house view. |
| ADVANTEST | 31,430 | 38,414 | +22% | Bernstein ¥39,200 ≈ the median (+2%), MS ¥36,000 below it, JEF ¥30,000 -18% below and under spot (stale). |
| MSFT | 485 | 564 | +16% | MS $600 (cut from $650) is only **+6.4% above the median** — mildly constructive, not an outlier. |
| GOOG | 373 | 429 | +15% | BofA's $430 (07-16) is effectively the median. |
| AMZN | 286 | 326 | +14% | Lowest upside in the set. |
