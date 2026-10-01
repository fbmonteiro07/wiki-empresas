# Distance from historical high — September 29, 2026

Source: Bloomberg Desktop API, September 29, 2026 closing prices. Drawdown is the dated closing price divided by the highest available historical intraday price, minus one. These are calculations from observed published series, not estimates of unavailable ex-top-10 baskets.

| Market | Full index / ETF below ATH | Excluding ten largest companies below own ATH |
|---|---:|---:|
| S&P 500 | 1.8660% | 3.7543% |
| QQQ | 1.4319% | Not validated |
| Russell 2000 | 8.5281% | Not validated |

S&P full: SPX Index, 7,670.84 / 7,816.70 − 1 = −1.8660%.

S&P ex-top-10: SPXX Index (US 500 Excluding Top 10 Price Return Index; Bloomberg INDX_SOURCE = Standard & Poor's), 4,849.11 / 5,038.26 − 1 = −3.7543%. Its highest historical intraday observation was August 17, 2026; its available history begins December 31, 1999. The maximum of the full daily history agrees with the independently requested INTERVAL_HIGH field. SPXX Index is distinct from the Nuveen fund SPXX US Equity.

Constituent cross-check: SPXX Index has 492 securities, all contained in the 503-member SPX snapshot. The difference is 11 share classes representing 10 companies: AAPL, AMZN, AVGO, BRK/B, GOOG and GOOGL (one company), META, MSFT, MU, NVDA, and TSLA. Thus the published S&P exclusion is a ten-company exclusion, not merely ten security lines. The published series follows its provider's historical selection/rebalance rules; it is not a backcast that removes today's ten companies from all historical dates.

QQQ: QQQ US Equity, 737.93 / 748.65 − 1 = −1.4319%. Available history begins March 10, 1999. ATH observation June 3, 2026. This is the ETF price, split-adjusted with cash dividends unadjusted.

Russell 2000: RTY Index, 2,807.922 / 3,069.709 − 1 = −8.5281%. Available history begins December 29, 1978. ATH observation August 14, 2026.

## Unresolved exact ex-top-10 calculations

No matching published Nasdaq-100 ex-top-10 or Russell-2000 ex-top-10 price series was identified in the instrument searches retained in this directory. This is a search result, not a claim that no such custom index can exist.

Reconstruction is blocked by unusable index weights in the available Bloomberg responses: INDX_MWEIGHT, INDX_MWEIGHT_HIST, INDEX_MEMBERS_WEIGHTS, and INDX_MWEIGHT_PX variants return the same tiny negative value (approximately −2.4245362661989844e−14) for constituent weights. The original Bloomberg message string also contains these invalid weights, so this is not solely a JSON parsing issue. The weights neither sum to 100% nor identify the largest companies. No portfolio estimate has been inferred from them.

An exact custom index would require usable historical memberships/weights, an explicit top-ten selection and rebalancing convention, and a reconstructed historical price series. Current holdings alone, or averages of individual-stock drawdowns, cannot establish that basket's own all-time high.

An available Nasdaq-100 ex-top-30 series (NDX70P Index) was also verified: 4.9006% below its historical high as of September 29, 2026. This is a different exclusion and is intentionally not substituted into the ex-top-10 comparison.

## Evidence

- verified_drawdowns.json: prices, highs, dates, and reference/history reconciliation.
- benchmarks_full_history.json: complete Bloomberg historical responses for SPX, QQQ, and RTY.
- published_ex_reference.json and published_ex_full_history.json: SPXX and NDX70P metadata, memberships, and historical prices.
- current_weights.json, start_weights.json, alternate_weights.json, raw_weight_message.txt: failed weight inputs.
- search_*.json and final_search_*.json: instrument searches.

The prior breadth chart describes constituent stocks' individual drawdowns. Different stocks reach their highs on different dates; those figures do not represent the distance of the combined index from its own peak.
