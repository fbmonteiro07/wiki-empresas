# Sentiment decision lab — research verdict

Built 2026-10-28T23:29:40.494859+00:00. Bloomberg total returns through 2026-10-27; social through 2026-10-28.

## Decision

Keep the research cockpit. Do not adopt the sentiment trade signal.

The incremental sentiment test does not clear the predeclared evidence threshold. Monitoring value is separate from demonstrated predictive value.

## Primary comparison

Technical + fixed-FY revisions + X versus Technical + fixed-FY revisions. 20-session holds, same eligible stocks and dates, next-close execution, 10 bps per one-way traded notional.

| Year | Completed periods | Mean incremental return per hold | Paired 95% interval | Cumulative difference |
|---|---:|---:|---|---:|
| 2024 | 12 | -2.60 pp | -5.81 pp / -0.57 pp | -43.23 pp |
| 2025 | 12 | -1.18 pp | -1.78 pp / -0.47 pp | -20.95 pp |
| 2026 | 10 | -0.54 pp | -2.33 pp / +1.09 pp | -9.17 pp |

## Grounding and limits

HARD: retrieved prices and vendor observations. PARTIAL: original data vintages, parsed text, current watchlist history. ESTIMATE: fixed research weights, windows and transaction-cost scenarios. No weight was fitted. Costs are scenarios, not a claim about achievable execution. No expected future return is estimated.

Signals use only source dates before the signal session. Fixed target fiscal year equals signal calendar year + 1, used for both estimate observations; target differs in time-to-maturity across fiscal calendars. EPS uses symmetric change to handle zero/negative earnings.

Cumulative differences are percentage-point differences between compounded long-only portfolios. Holding-period confidence intervals refer to paired mean differences, not cumulative alpha. No multiple-testing adjustment. Current watchlist selection and hindsight prevent out-of-sample claims.

## Guardrails

- PASS — Independent cache price reconciliation: 1070 same-security/date observations, fresh Bloomberg PX_LAST versus existing OHLCV cache; tolerance 0.1%.
- PASS — Information cutoff before execution: Every event: source-date cutoff < signal session < next-close entry < exit.
- PASS — Cash and return reconciliation: Compounded holding-period returns reconcile to the marked portfolio, including gaps and liquidation costs.
- PASS — Missing realized prices: 0 whole matched events excluded after a missing outcome. No replacement stock or shortened return was inserted.
- PASS — Listing currency and exchange: 96 US listings verified with Bloomberg CRNCY. Financial-reporting currency is never used for portfolio eligibility.
- PARTIAL — Original point-in-time vintages: Fixed fiscal targets prevent horizon roll. Vendor corrections, original release times and original consensus constituent vintages are not certified.
- PARTIAL — Historical universe membership: Current wiki watchlist projected backward; includes selection and survivorship bias. This is not a broad investable-universe test.
- PARTIAL — Genuine out-of-sample evidence: Rules frozen before this run, but 2026 has been studied previously. All reported history is retrospective; no live validation yet.
- PASS — Relative-context event alignment: 15734 company event scores match their exact-date peer context; 5/20-session windows and non-overlap verified. 778 unavailable company rows remain placeholders in the 16512-slot master schedule.
- PARTIAL — Independent skeptic review: Approved for descriptive retrospective research including frozen train2024–2025/pair validation2026. Independent reconstruction completed379,486 checks with zero discrepancies:all384 training choices,24,930 ledger rows,759 paired contrasts and638 direct2,000-draw block bootstrap runs. All15,734 raw TRI returns and exact windows rechecked.253 cases qualified in training;38 outperformed all benchmarks in observed2026;93 had full validation support;0 passed every incremental gate. Data vintages,current membership,previously examined2026 and approximate local inference prevent a validated forecasting claim.

## Reproduce

`py -B _wiki/_tools/build_sentiment_research.py` (offline cached inputs).

`py -B _wiki/_tools/fetch_sentiment_research.py --asof YYYY-MM-DD` refreshes only this experiment’s Bloomberg inputs.

Source input hashes, complete matched event ledgers, scenario results and protocol: `_data/sentiment_research/`. Existing hub layouts and source company pages are unchanged.
