## Double-check verdict: Anthropic / OpenAI Ramp reconciliation — PARTIAL

Reviewed October 23, 2026. **Arithmetic PASS; denominator suitability for revenue modeling FAIL; model status HOLD.** The investigation establishes a persistent difference between two published bases. It does not identify the backend cause or validate either ratio as realized company ASP.

Scope: independent, read-only review of `reconcile.py`, `reconciliation.json`, `reconciliation.md`, archived `../raw/tokenPrices.json` and `../raw/tokenVolumes.json`, fresh response files, capture metadata, and `js/3esy_8xboh9bh.js`. Only this audit file was written. HARD means source-reported fields; calculated quantities below are DERIVED, with no forecast constants.

### 1. Outlook email coverage

Not applicable. This assignment audits a public dataset reconciliation, not broker coverage or a single-name thesis.

### 2. SEC filings coverage (last 2 years)

Not applicable. No filing-dependent claim is being certified.

### 3. Bloomberg API cross-check (REFERENCE ONLY — not gabarito)

Not applicable. No Bloomberg-dependent market-data claim is being certified. Independent raw-data arithmetic produced:

| October 5–11, 2026 | Anthropic | OpenAI |
|---|---:|---:|
| Published-price tokens N | 25,146,006,422,083 | 25,570,512,740,004 |
| Sum of model tokens T | 42,724,724,082,806 | 27,722,837,284,884 |
| Gap T−N | 17,578,717,660,723 | 2,152,324,544,880 |
| Gap / N | 69.906598% | 8.417213% |
| Published cost C, USD | 20,221,880.22128914 | 12,243,575.09029095 |
| Sum of reported model cost S, USD | 20,225,929.59437014 | 12,245,081.91170570 |
| Cost difference / C | 0.020025% | 0.012307% |
| Missing-spend tokens M | 613,031,313,288 | 97,112,318,383 |
| Conditional maximum M / (T−N) | 3.487349% | 4.511974% |
| Gap after removing all M | 16,965,686,347,435 | 2,055,212,226,497 |
| Published C/N, USD per million | 0.804178599 | 0.478816175 |
| Matched-model diagnostic, USD per million | 0.480287751 | 0.443242435 |

Source: Ramp Economics Lab / Ara Kharazian, the archived and October 23 response records for October 11. The missing-token subtraction is a conditional bound, not a documented filter. Anthropic still differs by **67.468711% of N** after that subtraction. Neither price row is an approved revenue-model input.

### 4. Transcript coverage

Not applicable. Primary documentation and frontend code were checked instead:

- The frontend sums model rows by maker and computes price directly as `1e6*token_cost_usd_7d/token_count_7d`. Its source label describes **model-attributed API spend**. This supports separate published calculations, not identical backend populations. [Public bundle](https://ramp.com/_next/static/immutable/chunks/3esy_8xboh9bh.js)
- Ramp documents separate API/Enterprise connections and OpenAI credit-plan cost estimates that may differ from actual billing. It does not establish those estimates or Enterprise subscriptions as the cause of the Index gap. [Ramp support](https://support.ramp.com/ai-token-spend-management)
- Claude Messages responses contain an aggregate cache-creation count and overlapping duration subfields. The organization Usage Report example instead shows nested cache creation without that duplicate aggregate. Which schema Ramp ingests is unproved. [Prompt-caching schema](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [Usage Report](https://platform.claude.com/docs/en/api/beta/organization/usage_report/retrieve_messages)

### 5. Unsourced or weakly-sourced claims in prior work

1. **Cache elimination originally overstated.** `N != U+O` rejects that identity. Calling it a rejection of all-cache exclusion requires a common cohort and exhaustive compatible non-cache categories, neither verified. Likewise `G != R`, with `R=N−U−O`, rejects duplication of that entire arithmetic residual once; it does not reject partial caching/accounting differences. The main reconciliation has now narrowed these claims correctly.
2. **Cost agreement is not cohort validation.** Close dollar totals do not establish common token definitions, customers, connection joins, or recognized revenue. Both tables originate from Ramp, so they are not independent economic anchors.
3. **Retrieval consistency is narrower than source correctness.** All 3,894 price rows and 19,156 model-metric rows have unique export keys. Every model period is a seven-day flow. Fresh and archived parsed objects match exactly; token-volume file bytes differ because serialization differs. This excludes a local version mismatch, not stale upstream data, alias duplication, or backend aggregation errors.
4. **Timing test is useful but bounded.** Independently reproduced the common 39-week, ±7-day comparison. Same-day median cost errors are 0.044450% Anthropic and 0.041698% OpenAI. The shifts minimizing token discrepancies still leave 39.860039% and 5.125944% median token gaps, while cost errors rise to 6.679403% and 5.060090%. A fixed day offset does not reconcile these exports; intraday timezones and upstream bucketing remain untested.
5. **A flat correction fails the historical check.** Anthropic T/N−1 is 7.088265% January 25, 40.932629% June 28, 70.832416% July 26, 83.361745% September 27, and 69.906598% October 11. A constant 1.6991 factor is unsupported.

### 6. What the prior analyst MUST do before this work ships

The conditional cache wording and Messages-versus-Usage-Report distinction were corrected and verified in the regenerated script and report before this audit was finalized.

- Retain HOLD on both blended ratios for company revenue-model use and on any combination of published price with model-series volume.
- Retain the conditional wording on cache tests, the schema endpoint distinction, and the distinction between consistent retrieval and validated backend accounting.
- Require a documented bridge by model, token type, customer/connection, product, period and cost basis before lifting HOLD. Source-specific model-family shares may remain descriptive; their company-wide representativeness and token comparability remain unvalidated.

### 7. Bottom line

The reconciliation work supports the HOLD decision and its arithmetic checks out. The largest gap remains the absence of a common token universe and backend lineage; describing it as a known caching issue, subscription issue, or corrected ASP would exceed the evidence.
