# Basket liquidity and PLNT

Bloomberg Desktop API, retrieved September 23, 2026. Stock observations refer to September 22, 2026.

The previously extracted index volume equals the sum of the constituents’ volumes on their listed exchanges. It does not identify Goldman basket order flow, direction, client notional or dealer hedge executions. The basket turnover field likewise aggregates underlying trading. Neither is a valid observed basket trade notional.

## Inputs and scope

- **HARD:** constituent weights from Bloomberg `INDX_MWEIGHT`, reference snapshot on September 23 before US trading. These are snapshot weights, not verified execution-time weights.
- **HARD:** constituent prices, shares traded and dollar turnover from Bloomberg historical `PX_LAST`, `PX_VOLUME` and `TURNOVER`, using US composite tickers. Equity TURNOVER is USD; the index field is USD thousands and is not used in the participation calculation.
- **DERIVED from HARD:** dollar ADTV is mean daily TURNOVER over the 20 sessions from August 24 through September 21, excluding the September 22 event day. Share ADV is separately calculated from shares traded over the same sessions.
- **ESTIMATE / illustrative scenario:** USD100,000,000 one-way basket order, 100% executed in constituent equities in proportion to the September 23 snapshot weights, compared with the liquidity baseline preceding September 22. The notional, full cash pass-through and applicability of snapshot weights are scenario assumptions. This does not reconstruct September 22 basket execution. A swap transaction need not result in the same immediate cash hedging.
- Top ten means the ten largest basket weights. PLNT is shown separately even when outside the top ten.

## PLNT: observed trading and hypothetical allocation

Close: $42.60, versus $47.05 on September 21. Derived close-to-close return: -9.46%.

Observed share volume: 7,466,189; preceding 20-session share ADV: 1,798,864.05; volume / ADV = 415.05%.

Observed dollar turnover: $320,508,600; preceding 20-session dollar ADTV: $91,372,829.50; turnover / ADTV = 350.77%.

These observed ratios describe all trading in PLNT and do not isolate basket-related trading.

**GSXUSWCH Index:** PLNT weight 2.609978% (rank 16).

1. Hypothetical PLNT allocation = $100,000,000 × 0.02609978 = $2,609,978.
2. Dollar participation = $2,609,978 / $91,372,829.50 × 100 = 2.8564% of dollar ADTV.
3. Basket order corresponding to 10% of PLNT dollar ADTV = 0.10 × $91,372,829.50 / 0.02609978 = $350,090,420.

**GSCBSWC2 Index:** PLNT weight 4.714943% (rank 12).

1. Hypothetical PLNT allocation = $100,000,000 × 0.04714943 = $4,714,943.
2. Dollar participation = $4,714,943 / $91,372,829.50 × 100 = 5.1601% of dollar ADTV.
3. Basket order corresponding to 10% of PLNT dollar ADTV = 0.10 × $91,372,829.50 / 0.04714943 = $193,794,134.

## GSXUSWCH Index: top ten weights

USD100m scenario is hypothetical. Dollar ADTV is consolidated US turnover; both percentage columns below use that same dollar denominator.

| Stock | Weight (HARD) | Dollar ADTV20 (USD m, derived) | Observed Sep 22 turnover / ADTV | Hypothetical USD100m basket leg / ADTV |
|---|---:|---:|---:|---:|
| T | 3.224% | 946.23 | 94.8% | 0.34% |
| NYT | 3.200% | 169.60 | 321.4% | 1.89% |
| PGR | 3.086% | 447.52 | 221.7% | 0.69% |
| SIRI | 3.077% | 110.79 | 149.9% | 2.78% |
| VZ | 3.056% | 1032.10 | 148.0% | 0.30% |
| W | 2.958% | 228.06 | 83.9% | 1.30% |
| AMP | 2.945% | 286.27 | 187.4% | 1.03% |
| ALL | 2.943% | 413.65 | 292.8% | 0.71% |
| TMUS | 2.934% | 824.54 | 139.1% | 0.36% |
| SF | 2.920% | 87.40 | 135.5% | 3.34% |

## GSCBSWC2 Index: top ten weights

USD100m scenario is hypothetical. Dollar ADTV is consolidated US turnover; both percentage columns below use that same dollar denominator.

| Stock | Weight (HARD) | Dollar ADTV20 (USD m, derived) | Observed Sep 22 turnover / ADTV | Hypothetical USD100m basket leg / ADTV |
|---|---:|---:|---:|---:|
| T | 5.461% | 946.23 | 94.8% | 0.58% |
| CMCSA | 5.406% | 664.94 | 153.2% | 0.81% |
| TMUS | 5.390% | 824.54 | 139.1% | 0.65% |
| HRB | 5.344% | 83.36 | 135.3% | 6.41% |
| VZ | 5.309% | 1032.10 | 148.0% | 0.51% |
| SIRI | 5.283% | 110.79 | 149.9% | 4.77% |
| INTU | 5.217% | 1378.64 | 102.4% | 0.38% |
| NYT | 5.169% | 169.60 | 321.4% | 3.05% |
| W | 4.984% | 228.06 | 83.9% | 2.19% |
| Z | 4.893% | 114.32 | 98.2% | 4.28% |

## Price impact, sensitivity and checks

No calibrated PLNT price-impact coefficient or actual signed basket order was supplied or observed. A causal price impact, expected PLNT closing price or portion of its observed decline attributable to these baskets is therefore unavailable. A percentage of ADTV is not a percentage price move.

The participation equation has no fitted constant: allocation = basket notional × weight; participation = allocation / dollar ADTV. Doubling the hypothetical notional doubles participation. Changing the actual cash-hedged fraction scales the result proportionally. There is no claim of linearity between participation and price impact.

Guards: both basket weight sums are within rounding of 100%; all constituent baselines have 20 prior trading sessions; currencies and consolidated volume bases match; historical turnover divided by volume produces a price consistent with the independently returned close. These checks validate the data and arithmetic, not a causal trading model.

Pre-trade impact also depends on execution timing, volatility, spread, order size and participation. Source: [NYSE, Choey Li, October 17, 2023](https://www.nyse.com/data-insights/closing-auction-immediate-market-impact-price-drift-and-transaction-cost-of-trading-part-2).

Raw Bloomberg source capture: [weights](../reference.json), [constituent history](constituents_history.json), [reference checks](constituents_reference.json), [original index-volume reconciliation](../verification.json). Calculation inputs and outputs: [analysis.json](analysis.json).

Independent skeptic review: see [audit verdict](audit_verdict.md).
