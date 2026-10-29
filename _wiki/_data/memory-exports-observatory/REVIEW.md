# Independent review: Memory Observatory — PASS for exploratory research calculations

Reviewed 28 October 2026. This verdict covers source fidelity, normalization, historical calculations and dashboard wording in source. It does not validate an operational forecast or historical real-time availability. The parent must rebuild and inspect the published page after the three fixes below; the reviewed pre-rebuild payload was built at 15:01:28 -03:00.

## 1. Source coverage actually checked

- **106 new company-product targets, all checked against archived primary-source text, from 53 distinct documents.** SK hynix: 80 rows, 40 quarterly company releases, 2010Q1–2019Q4. Samsung: 26 rows, 13 official earnings-call scripts, 2016Q4–2019Q4. All original-file SHA256 hashes match the source ledger. Every stored wording excerpt occurs in the original text or specified script page after punctuation/whitespace normalization. I separately read every new Hynix price-change statement and every Samsung target source page; this was not a sampled audit.
- The **104 original target records are unchanged**, both as Python objects and as individually serialized JSON records. No duplicate company/product/quarter keys.
- New exact percentage disclosures retain HARD tags. Samsung qualitative bands retain PARTIAL tags. The three Hynix “stable” observations—2014Q1 DRAM, 2014Q3 DRAM and 2019Q4 NAND—use the disclosed analyst convention of midpoint 0 with -1/+1 pp bands and PARTIAL tags.
- Exact examples checked: SK hynix 2011Q3 DRAM -29%, company release dated 27 October 2011; SK hynix 2019Q1 NAND -32%, company release dated 25 April 2019. Samsung 2019Q1 DRAM and NAND both use “mid-20% ASP decline” on page 6 of the 30 April 2019 official script, represented as -26% to -24%, midpoint -25%.
- The 2015Q3 Hynix exception preserves both the original 22 October event dateline and 28 October newsroom header date. Samsung event dates are retained from the archived official event calendar.
- Full record-level evidence: `all_new_target_source_audit.json`. Missing earlier Samsung disclosures remain missing. Existing excluded Hynix downturn records remain excluded.

## 2. Raw source fidelity, units and coverage

Independent verification against retained raw responses, without importing production analysis functions:

| Dataset | Work performed | Result |
|---|---|---|
| Bloomberg / InSpectrum | 20,877 raw observations; source/currency metadata; 2,419 monthly rows across 26 series; raw hashes | All matched |
| KCS core | All 603 normalized rows; each source file/hash, HS code, month, USD amount and net kg | All matched |
| KCS extended | All 1,993 normalized rows across 38 combined core/extended source files | All matched |
| BOK ECOS | All 1,407 observations against raw API pages, including explicit dollar-basis `ITEM_CODE2=D` | All matched |
| Flash + SSD Tornqvist | Every one of 153 monthly index levels independently reconstructed from dollar-value shares and USD/kg changes | All matched |
| Displayed coverage | All 35 series: first/last complete month, observation count and missing-month count | All matched |

KCS source export values are rounded **thousand USD**; multiplying by 1,000 is correct. Net kg are preserved. The audit found no kg-to-bit conversion. Quarterly customs features correctly use summed value divided by summed weight; they do not average monthly unit values without weight.

Spot levels use the mean of observed daily closes, subject to the stated monthly coverage test. Contract series use the last monthly quotation. Complete-month exclusions reproduce. No legacy/modern specification splicing, backfilling, or expanding basket membership was found. The fixed equal-weight baskets use the common component months.

The source expansion supplies 201 complete monthly KCS/BOK observations from January 2010 through September 2026. That is not 16 years of modern DDR5 history: DDR5 contracts begin May 2023 and DDR5 spot begins October 2023. The UI records the actual shorter and gapped histories.

## 3. Fit, comparison and direction reproduction

`independent_audit.py` contains independent month/quarter construction, feature calculations and OLS. It imports no production analysis functions.

- Reproduced every fit in **156 company / product / benchmark / information-set models**.
- Reproduced all **3,183 quarterly test predictions**, including exact target-quarter membership, ten-prior-observation minimum, training count, training endpoint, target and persistence value.
- Reproduced all **1,196 common-sample monthly predictions** across six spot/contract pairs and lags 0–3. The 24-prior-target minimum and target-date-at-or-before-origin training restriction hold. Lags 2–3 correctly use the latest target available at the origin for persistence, not an unavailable t-1 observation.
- Reproduced regime MAE, signed bias, persistence and zero baselines, accuracy at 0 and ±3 pp, the full confusion matrices, balanced accuracy, downside/upside recall, always-up and persistence direction baselines, turning-point detection and false alarms.
- Both classes are required for balanced accuracy. Neutral predictions count as misses against non-neutral actuals. Turns require adjacent calendar quarters, and neutral periods or missing quarters do not create turns.
- Within-model comparisons use the same target observations. The separate standard-family comparison intersects target quarters across all included benchmarks. Short DDR5 and legacy models do not silently shrink that fixed intersection.

**Zero numeric or source mismatches.** Full maximum-error and observation-count output is in `independent_results.json`.

## 4. Resampling, sensitivity and interpretation

`raw_and_resampling_audit.py` independently reproduces **all 340 non-null resampling ranges**, using seed 20261028, 600 resamples, four-quarter or six-month blocks, paired persistence absolute error minus model absolute error, and the stated percentile order statistics. Each source block is contiguous in calendar time; no source block crosses a missing period. Runs shorter than the nominated block length remain intact shorter blocks.

The implemented method is **non-circular**. The initial protocol incorrectly said circular. The parent corrected the protocol with an explicit review-history note; the numerical method was not changed to manufacture a result. This remains an exploratory moving-block range. It is not a future ASP prediction interval or a post-selection significance claim. Short, fragmented histories and unequal endpoint representation limit its precision.

The calibration equation is `ASP = 100 × [exp(alpha + beta × log(1 + benchmark_growth / 100)) - 1]`. Coefficients are fitted from observed company targets; no manually chosen multiplier was found. All-target normalization sensitivity is correctly described as a source-band envelope, not forecast uncertainty. Training-window sensitivity is explicitly a fitted-value exercise, including the endpoint where applicable.

The current BOK/Hynix DRAM calibration illustrates why a historical edge is not a current-quarter forecast guarantee: 2026Q3 BOK benchmark growth is 14.7675%; the full-history fitted ASP is 12.1398% versus the recorded actual of 28%. The full-history and 2024-onward fitted values differ (12.14% versus 17.31%). These are in-sample calibration numbers, not new forecasts.

## 5. Confirmed findings and fixes

1. **Stale observation presented as current:** the pre-rebuild `partial_spot` array included retired DDR3 2Gb's November 2019 partial month, through 6 November 2019. `overview()` rendered it under “Latest spot pulse.” The parent patched `analyze_pricing.py` so the panel's data are limited to the current as-of month. Rebuild the payload/page and confirm that only October 2026 observations appear.
2. **Derived baskets labelled HARD:** the history panel originally labelled fixed-weight baskets and the analyst-created Tornqvist index HARD OBSERVATIONS. `dashboard_ui/app.js` now labels these DERIVED BENCHMARK and identifies hard source inputs plus analyst aggregation. Source code verified.
3. **Protocol/implementation mismatch:** the initial protocol said circular block resampling; the code was non-circular. The revised protocol now states non-circular and explains the review correction. Verified against the implementation.

The parent also made the historical-edge grading thresholds visible. The rule requires at least 20 tests, at least five down and five up observations, a positive lower resampling bound for the MAE advantage over persistence, and a smaller MAE than the direct benchmark. This is a disclosed diagnostic rule, not probability calibration.

No unresolved source-value, formula, chronology or sample-alignment blocker was found. Final rendered-page inspection and rebuilding are parent-owned release checks.

## 6. What the longer history does and does not establish

Hynix, complete-quarter inputs, all available comparable test quarters; all MAEs are percentage points. These are within-model comparisons. Model rows with different sample sizes are not directly ranked.

| Benchmark | Tests | Model MAE | Prior-ASP MAE | Model advantage | 95% exploratory advantage range |
|---|---:|---:|---:|---:|---:|
| KCS DRAM USD/kg | 52 | 9.76 | 8.67 | -1.09 | -3.11 to +1.35 |
| BOK DRAM | 52 | 5.89 | 8.67 | +2.78 | +1.39 to +5.30 |
| KCS flash USD/kg | 47 | 11.28 | 9.82 | -1.46 | -4.24 to +1.05 |
| BOK flash | 47 | 7.54 | 9.82 | +2.28 | +0.74 to +3.71 |
| KCS flash + SSD Tornqvist | 31 | 12.37 | 11.50 | -0.87 | -3.78 to +1.70 |

Source: independently reproduced calculations from the 28 October 2026 dashboard input vintage. These results do not support calling raw customs unit values a generally reliable company-ASP forecasting signal. BOK's historical relationship is stronger, with balanced direction accuracy of 85.7% for DRAM and 81.5% for flash on their respective all-history samples. Neither percentage is a forecast probability.

Remaining research limitations are material and already appropriate for disclosure: latest-vintage rather than historical-publication data; company mix shifts including HBM and Solidigm; incomplete corporate downturn coverage; analyst-defined qualitative target bands; short modern specification histories; multiple exploratory model comparisons. Eligible Hynix coverage is 65 DRAM quarters and 61 NAND quarters. Missing DRAM: 2022Q4 and 2024Q1. Missing/ineligible NAND: 2022Q1, 2022Q3–Q4, 2023Q3–Q4 and 2024Q1. Do not interpret a longer benchmark history as complete company-target coverage.

## 7. Bottom line

The new source work is evidenced, and the historical arithmetic survives an independent reconstruction. PASS applies to an explicitly exploratory research dashboard after the confirmed source-code fixes are rebuilt and visually checked; it does not authorize an operational company forecast. The most important economic finding is that longer data weaken the case for customs unit values as a general ASP translator while leaving stronger, still conditional historical evidence for BOK indices.

Audit artifacts are confined to `audit/2026-10-28/long_history/skeptic/`. No production file was modified by this reviewer.
