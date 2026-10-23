## Double-check verdict: Anthropic / OpenAI consumption scenarios — PARTIAL

Audited October 23, 2026. **Arithmetic PASS at supplied inputs. Economic inference PARTIAL.** The workbook can serve as a conditional revenue-to-token scenario. It does not establish actual company consumption, a calibrated company ASP, or an economic minimum price. The earlier HOLD on interpreting Ramp ratios as validated company ASPs remains in force.

Read-only review covered `prepare_data.py`, `model_inputs.json`, `build_workbook.mjs`, `arr_source.json`, the original `AI Model.xlsx`, Ramp raw datasets, and the exported `AI_Token_Consumption_and_Minimum_Price.xlsx`. Only this audit file was written.

### 1. Outlook email coverage

Not applicable. No broker-consensus or email-coverage claim is certified.

### 2. SEC filings coverage (last 2 years)

Not applicable. The source is the user's house model, not reported company actuals.

Source workbook SHA-256 independently matches `3d9eda23569aed4b4dfb8858b07faceb1daa8425c06821ad35247e6dc11b93b5`. The original sheet identifies USD millions and monthly-average annualized ARR. Correct selected ranges are:

- Anthropic gross `ARR Tracker!P98:AA98`; net `P84:AA84`.
- OpenAI gross `ARR Tracker!P95:AA95`; net `P81:AA81`.
- Anthropic API share `Anthropic!AB11 = 85%`, gross basis. Underlying labels distinguish direct API and gross third-party cloud sales.
- OpenAI API share `OpenAI!AB29 = 24.6654370748%`, net basis, derived from the source's net API revenue over total revenue. Column AB is CY2026E.

Using annualized monthly-average ARR / 12 is dimensionally correct. The source's cached house estimates are preserved; this audit does not certify the source workbook's entire forecast or its unrelated existing errors.

### 3. Bloomberg API cross-check (REFERENCE ONLY — not gabarito)

Not applicable. Independent recalculation from raw Ramp data reproduced all **24 provider-month calculations** and the saved workbook's inspected outputs.

| October, gross ARR basis | Anthropic | OpenAI |
|---|---:|---:|
| Average annualized ARR, USD bn | 75.389370364 | 56.911688794 |
| Published weekly-sample monthly price, USD/M | 0.802084117 | 0.500902951 |
| Matched-model monthly price / minimum reference, USD/M | 0.459245418 | 0.459526106 |
| Full-ARR equivalent at published price, Q/month | 7.832654206 | 9.468182859 |
| Full-ARR equivalent at minimum reference, Q/month | 13.679935136 | 10.320720995 |
| API-only equivalent at published price, Q/month | 6.657756075 | 2.507067635 |
| API-only equivalent at minimum reference, Q/month | 11.627944866 | 2.732810082 |

Here Q = 10^15 tokens and M = 10^6 tokens. Worked path: Anthropic 75.389370364 / 12 = USD 6.282447530bn monthly equivalent; dividing by USD 0.802084117/M gives 7.832654206 Q/month. Conversion to T/day is Q/month × 1,000 / calendar days.

Gross/net API adjustments are algebraically consistent with the stated assumption that all gross/net differences belong to API channels. For Anthropic, API gross = 0.85G and API net = 0.85G−(G−N), producing 83.14606742% of net ARR. For OpenAI, API net = 0.246654370748N and API gross adds G−N, producing 26.47886793% of gross ARR. Holding the annual shares across months is an ESTIMATE assumption, not observed monthly mix.

### 4. Transcript coverage

Not applicable. Source-table and workbook checks replace transcript work for this narrow assignment.

Monthly aggregation correctly divides summed costs by summed tokens across nonoverlapping weeks ending in each month. It does not average weekly prices equally. The 82 provider-week records include January 4, whose week starts December 29, 2025. October uses September 28–October 11, not an exact October calendar-month billing sample. November/December carry October price and mix unless the forecast price input is changed.

Missing-spend token volume remains in all-token mix but is excluded from matched prices. Positive spending with zero tokens is also excluded from matched prices. Explicit zero spending with positive tokens would remain a reported observation. No arbitrary cache factor is inserted. Inspected exported sheets contain no cached Excel error cells, and family-share totals reconcile to one.

### 5. Unsourced or weakly-sourced claims in prior work

1. **The minimum is a selection rule, not an estimated true minimum.** `MIN(published ratio, matched-model ratio)` mechanically produces the larger implied volume from two unresolved bases. It is defensible only as the user's authorized reference scenario. For October it raises full-ARR equivalent volumes 74.652612% for Anthropic and 9.004242% for OpenAI. That uplift is not evidence of extra physical demand.
2. **Full ARR is not matched API spending.** It includes subscriptions and other revenue. API-only allocation reduces this mismatch but still depends on a house share and gross/net assumption; it does not cure sample, discount, reseller, or token-definition differences.
3. **Family allocation is illustrative.** Applying the panel's all-token family mix to company revenue-equivalent volume is not independently calibrated. Missing-price models remain in that mix. The workbook appropriately labels this transfer as PARTIAL.
4. **Input-boundary defect corrected.** The initially inspected export allowed a forecast price change below −100%, which could make December prices positive again after an invalid November. The final saved workbook now has numeric input validation at −100% and a formula-level guard against nonnumeric or below−100% values and invalid preceding prices. The builder also includes both invalid-input cases for both providers and forecast months. Saved guards were independently inspected.
5. **Presentation corrected.** The final saved title is “Implied token consumption scenarios.” The subtitle and output labels identify equivalents and the unresolved pricing basis.

### 6. What the prior analyst MUST do before this work ships

- Retain scenario wording, ESTIMATE treatment of house ARR/API shares, the unresolved-denominator warning, and October/forecast period qualifications.
- Retain the corrected price-driver guard. The saved default is 0% and supplied-input calculations are unaffected.
- Do not present the selected minimum as a lower bound, an independently supported best estimate, or a release of the earlier company-ASP HOLD.
- Final exported title and driver guard were confirmed in the file saved at 10:24:55 local time on October 23; its sheets have zero cached Excel error cells. Visual and live-engine recalculation QA remain the workbook author's responsibility. This audit checked saved formulas/caches and independently recalculated the numerical model, not a live Excel session.

### 7. Bottom line

The source ranges, units, monthly weighting, gross/net adjustments, and supplied-input arithmetic check out, and the identified input-boundary defect is corrected. The workbook can be delivered as an explicitly conditional scenario; interpreting its outputs as measured company consumption would exceed the evidence.
