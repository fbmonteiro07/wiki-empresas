# Memory dashboard protocol — 28 October 2026

Written before evaluating the longer-history models. This extends, rather than replaces, PRICING_PROTOCOL.md. The original October 28 earnings refit and all prior inputs are frozen under audit/2026-10-28/long_history/before and audit/2026-10-28/refit.

## Inputs and scope

- Request KCS DRAM/flash/MCP from January 2010, flash+SSD detail from January 2014, BOK dollar export price indices from January 2010, and InSpectrum prices from January 2010. Display actual coverage, missing months and observation dates, never requested coverage as obtained coverage.
- Source levels and exact company ASP disclosures are HARD. Qualitative company bands are PARTIAL. Stable wording added from older releases uses a zero midpoint and a -1/+1 pp convention, explicitly PARTIAL. Regression coefficients, predictions and statistical summaries are ESTIMATE/derived.
- Legacy DDR3, MLC and TLC specifications are separate series. No generation splicing, hidden reweighting, forward fill of missing historical months, or conversion of kg to bits. Closed historical quarters require all months.
- Corporate ASP targets retain source wording, event/publication/retrieval dates and local original evidence. Existing targets are never overwritten. Pre-Solidigm NAND and the HBM era are different mixes: show fixed date regimes and restricted-window sensitivity.

## Estimation and tests

- Retain the log-linear equation and ten-prior-quarter expanding-window minimum. Predict each quarter only using preceding company quarters. Run complete-quarter and two-month carry features separately; complete-quarter results are nowcasts/backtests, not forecasts available at quarter start.
- All MAE/baseline/direction comparisons for a model use identical target quarters. The standard cross-benchmark comparison uses the existing common-sample family; legacy and short DDR5 histories do not change that intersection.
- Benchmark pairs for monthly lead/lag are specified before comparison: DDR4, DDR5, NAND TLC basket, MLC64, MLC128 and TLC128. Zero lag is contemporaneous. Monthly models require 24 prior known target observations; compare lags on common target months.
- Show MAE, bias, up/down/flat counts, confusion matrices, downside recall, balanced directional accuracy only when both up and down exist, and always-up and prior-ASP baselines. Flat threshold is a visible user choice (0 or 3 pp), not optimized. A direction rate is not a probability for the next forecast.
- Turning points mean a change between nonzero direction classes in adjacent calendar quarters; ignore gaps and neutral transitions. Report detection of actual turns plus false alarms; no trading-return claim.
- Date-regime checks are fixed: pre-2020, 2020–2023, and 2024 onward. Historical company-mix changes and missing downturn targets remain explicit.
- Use reproducible non-circular moving-block resampling of paired absolute-error advantages over persistence: 4-quarter / 6-month blocks, 600 resamples, 95% percentile range. Blocks never bridge missing calendar periods. Runs shorter than a block remain eligible as shorter intact blocks. This is an exploratory resampling uncertainty range, not a calibrated future prediction interval or post-selection significance test. Review correction: the initial draft said circular; the implemented and reviewed method is non-circular so that end/start wrapping never creates artificial adjacency.
- Keep 2024 onward as a displayed temporal stress period, not a newly untouched holdout (already observed). No series, lag or weighting is selected and called validated from these comparisons. No calibrated probability or operational company forecast is published.

## Guardrails and review

The UI evidence label is a disclosed descriptive screen: “Historical edge” requires at least 20 paired test quarters, at least five up and five down targets, lower MAE than both persistence and direct benchmark growth, and a paired-advantage resampling range above zero. Otherwise it says mixed or limited. The screen is not an independent statistical validation or a probability.

Coverage, duplicate dates, complete months, chronological training, identical baseline samples, two-sided direction samples, regime changes and source attribution are machine-checked. Old and newly retrieved overlapping source observations are compared and revisions documented. An independent double-check review must inspect new historical targets, formulae, calendar gap handling, resampling and the rendered claims before completion.
