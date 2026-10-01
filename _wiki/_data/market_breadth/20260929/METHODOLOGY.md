# Market breadth — September 29, 2026

Source: licensed local Bloomberg Desktop API. All prices are dated closing observations through September 29, 2026. The exact retrieval timestamp is retained in raw.json and summary.json. No estimates or simulated prices are used.

## Universe and window

- Nasdaq means the Nasdaq Composite (CCMP Index), not Nasdaq 100.
- SPY is represented by its benchmark, the S&P 500 (SPX Index). The displayed index return is the S&P 500 price return, not SPY's dividend-inclusive return.
- Russell means the Russell 2000 (RTY Index).
- The endpoint is September 29, 2026. September 8 is the baseline; September 9–29 contains 15 trading sessions. The chart includes the baseline plus those 15 closes.
- Constituents are the September 29 snapshot, held fixed across the window. This is a current-constituent comparison, not a point-in-time historical index backtest; removals before the snapshot are not represented.
- Share classes are separate securities. This is why the S&P 500 has 503 rows.
- Membership comes from INDX_MWEIGHT_HIST with END_DATE_OVERRIDE=20260929. INDX_MEMBERS truncates Nasdaq at 2,500 names; the historical member field returned all 3,396. Index weights are not used.
- Bloomberg US exchange suffixes are normalized to the US composite security for price retrieval. The union comprises 4,524 distinct securities.

## Calculation

1. Obtain INTERVAL_HIGH from the beginning of Bloomberg's available history through September 8, using START_DATE_OVERRIDE=19000101, END_DATE_OVERRIDE=20260908, and MARKET_DATA_OVERRIDE=PX_HIGH. The requested date is a search boundary, not a claim of continuous history since 1900.
2. For each subsequent close, extend that high using only PX_HIGH observations up to that date. Later highs never enter earlier observations.
3. Drawdown = 100 × (1 − closing price / running historical high).
4. Count securities with drawdown ≥10%, ≥20%, ≥30%, and ≥50%. These counts overlap: a security down 50% is in all four groups. Do not sum the four counts.
5. Divide each count by the fixed covered universe to plot comparable percentages. The table shows the actual count, percentage, and net count change versus September 8. A positive count change means more securities below the specified threshold.

PX_LAST and PX_HIGH requests explicitly enable split adjustments and disable normal and abnormal cash dividend adjustments and DPDF-following. The historical high is the maximum available intraday high, not the highest close and not a total-return peak. Provider corporate-action and security-history conventions carry through to the calculation.

Example (Bloomberg, September 29, 2026): Apple close 329.40; historical intraday high 345.34. Drawdown = (1 − 329.40 / 345.34) × 100 = 4.6157%; Apple is outside all four groups.

## Missing observations and coverage

Missing daily observations use the last available valid close, including a 60-calendar-day pre-window lookup where necessary. A carried price is explicitly flagged in the constituent export; it is not represented as a fresh trade. A stock without a pre-window high or valid baseline close is excluded from every date, maintaining a constant denominator.

| Index | Covered / members | Excluded | Latest carried prices |
|---|---:|---:|---:|
| Nasdaq Composite | 3,374 / 3,396 | 22 | 114 |
| S&P 500 | 503 / 503 | 0 | 0 |
| Russell 2000 | 1,975 / 1,976 | 1 | 1 |

Exclusions and reasons are listed individually in summary.json and validation.json. Several are recent listings; other names have unavailable or suspended price histories. Counts describe the covered cohort, not an extrapolation to unavailable names. The maximum possible missing-stock contribution to any threshold is the excluded count shown above. The Nasdaq comparison includes thinly traded acquisition companies because they appear in the Bloomberg constituent list.

## Validation

- Bloomberg's separate ALL_TIME_HIGH_PERCENT field agrees within 0.02 percentage points for all 4,500 eligible securities whose snapshot price equals the panel's endpoint price. One of the 4,501 unique covered securities had a different snapshot quote and was not compared.
- A separate full daily-history pull for Apple, Nvidia, Ford, and GE reproduces the baseline INTERVAL_HIGH values, within reported price precision.
- All threshold counts are nested and bounded by the covered universe on all dates. Denominators are constant.
- Stock-level data retain each close, price observation date, running high, drawdown, carried-price flag, source, and retrieval timestamp.
- These checks validate implementation and consistency within Bloomberg, not independence of the underlying provider's data.

## Reading the chart

The line charts use the same percentage scale for cross-index comparison; tables report current counts. The hover guide follows the cursor, while the tooltip explicitly reports the nearest observed daily close. The threshold legend toggles the corresponding series across all three panels.

ATH drawdowns describe long-run distance from historical peaks, so old peaks and structural losers can keep levels high. For the user's question, the change over the common 15-session window is especially useful alongside the level. This measure is distinct from advancing/declining issues, moving-average participation, or distance from a 52-week high.

## Files

- breadth_daily.csv: daily counts and percentages by index and threshold.
- constituent_drawdowns.csv: complete auditable stock-level panel.
- raw.json and batch JSON files: cached Bloomberg responses.
- summary.json: chart-ready aggregate data, excluded securities, and index returns.
- validation.json: reconciliation outcomes.
- ../field_info.json: Bloomberg field definitions and supported overrides.
- ../full_high_validation.json: separate daily-history validation sample.

Fetch: `_wiki/_tools/market_breadth_bbg.py --fetch` (run after the US close; requires the local Bloomberg Terminal).
Aggregate: `_wiki/_tools/build_market_breadth.py` (reuses cached data; requires Bloomberg only for a missing baseline-backfill cache).
The delivered chart and labels are the dated September 29 snapshot; no recurring refresh has been scheduled.
