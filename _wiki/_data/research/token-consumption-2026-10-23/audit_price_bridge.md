## Double-check verdict: Anthropic / OpenAI average-price bridge — PARTIAL

Audited October 23, 2026. **Arithmetic PASS. Published-panel benchmark choice PASS as a scenario reference. Actual company ASP and cache mix remain unvalidated.** This memo audits the proposed category bridge and source preparation; the workbook author owns final export and visual/recalculation verification.

### 1. Outlook email coverage

Not applicable. No broker or consensus claim is certified.

### 2. SEC filings coverage (last 2 years)

Not applicable. This is an audit of the Ramp public data and the requested scenario methodology.

### 3. Bloomberg API cross-check (REFERENCE ONLY — not gabarito)

Not applicable. Independently recomputed the October aggregates from `token-pricing-2026-10-23/raw/tokenPrices.json` and checked all 24 provider-month records in `category_mix_inputs.json`. No arithmetic differences were found beyond floating-point precision.

October uses the nonoverlapping weeks ending October 4 and 11, covering September 28–October 11. This is a partial weekly sample, not full October billing or an observed October 23 price.

| October bridge | Anthropic | OpenAI |
|---|---:|---:|
| All-token count N | 44,634,785,737,866 | 49,264,564,561,661 |
| Source all-token cost C, USD | 35,800,852.69442121 | 24,676,765.75983598 |
| Uncached-input tokens U / N | 4.05120788% | 24.38077290% |
| Output tokens O / N | 0.88896562% | 2.71161330% |
| Unclassified residual (N−U−O) / N | 95.05982650% | 72.90761380% |
| Uncached-input ratio, USD/M | 2.818354400 | 0.953406979 |
| Output ratio, USD/M | 16.773844171 | 3.835478650 |
| Residual cost/count ratio, USD/M | 0.566793600 | 0.225561643 |
| Published base C/N, USD/M | **0.802084117** | **0.500902951** |

Attribution: Ramp Economics Lab / Ara Kharazian, October 23 capture of the published series through October 11. Source fields are HARD as published. All sums, shares, residuals and ratios are DERIVED. Interpreting the residual as cache-related or transferring the panel to company-wide usage is PARTIAL.

Worked reconstruction, USD/M: Anthropic 0.114177396 input contribution + 0.149113708 output contribution + 0.538793013 residual contribution = 0.802084117. OpenAI 0.232447990 + 0.104003349 + 0.164451611 = 0.500902951. The identity reconstructs the same numerator and denominator and is therefore **not independent validation**.

### 4. Transcript coverage

Not applicable. No management or earnings-call claim is certified.

Source preparation uses the correct same-feed fields, equal category-date coverage, and sums of costs/counts rather than equally averaging weekly ratios. All 20 observed provider-month residual counts and costs are nonnegative. November and December are October carry-forward assumptions, not new observations.

### 5. Unsourced or weakly-sourced claims in prior work

- **Cache identification is unresolved.** The observed fields are `all_tokens`, `uncached_input`, and `output`. Their difference is an algebraic residual. It does not identify cache reads, cache writes, cache-hit rates, or a physically exhaustive token partition. Economic interpretation requires common cohorts and compatible category definitions, which remain unproved.
- **The residual ratio is not a cache-read price.** It can contain multiple token/cost categories or source-coverage differences. Official rate cards may identify incompatible claims but cannot recover unknown cache or model weights.
- **The published base is the most defensible benchmark available in these files.** It preserves the source's intended price series with the fewest additional assumptions. It is not necessarily closer to either company's true realized ASP. No independent company-wide average is established.
- **The lower matched-model ratio is a separate scenario.** October's approximately USD 0.459245/M Anthropic and USD 0.459526/M OpenAI use unresolved alternative denominators. Neither minimum selection nor averaging the two series repairs that difference.
- **Mix sensitivities must be named accurately.** A 5-point transfer from residual to uncached input, or 1-point transfer from residual to output, is an ESTIMATE scenario at fixed category rates and total tokens. It is not a measured effect of reducing cache hits. The October arithmetic gives 0.914662157 / 0.964154622 for Anthropic and 0.537295218 / 0.537002121 for OpenAI, respectively.

### 6. What the prior analyst MUST do before this work ships

1. Label the base as a **published-panel price benchmark**; retain exact formulas and display approximately USD 0.80/M Anthropic and USD 0.50/M OpenAI. Do not describe either as validated company ASP.
2. Label the third category **“Unclassified residual (possible cache / other)”**. If a shorter cache-related label is necessary, display PARTIAL beside it and explicitly state that measured cache-read/write shares are unavailable. Keep “uncached” in the input label.
3. Show the raw category counts/costs, derived residuals, category shares/rates, and weighted contributions. Check positive denominators, nonnegative residuals, category-date coverage, share sum, and reconstruction, while identifying the last two as internal arithmetic checks.
4. Name sensitivity transfers **residual**, not cache. Preserve fixed-total-token/fixed-rate assumptions and ensure the transferred share never exceeds the donor share. These October shifts are feasible against the reported residual shares.
5. Keep model-series family weights out of this price-series bridge. Continue separate lower-price scenarios, October partial-period labeling, forecast labels, and the earlier HOLD on empirical company-consumption claims.

### 7. Bottom line

Retaining the published cost/count series is more defensible than choosing its unresolved lower counterpart or inventing model/cache weights. The category bridge explains the arithmetic of that benchmark, but it does not solve the source-denominator discrepancy or deliver a measured cache mix.
