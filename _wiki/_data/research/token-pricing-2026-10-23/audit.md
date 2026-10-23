# Independent quantitative review — October 23, 2026

Verdict: **arithmetic PASS; provider-wide inference PARTIAL**.

The quant-estimate skill's double-check agent independently recalculated all 80 provider-week totals and matched-model prices from the archived raw JSON. It confirmed source hashes, seven-day flow alignment, monthly snapshot calculations and the two 10-percentage-point sensitivities. Official pricing was spot-checked against the Opus 5.5, Haiku 5.5, Sonnet 5, OpenAI July 30 and GPT-6.1 Sol announcements; it did not independently re-verify every chronology row.

Three valid findings were incorporated before delivery:

- Missing family spending is N/A, not zero; spending shares refer to reported observed spending.
- Sensitivity weights explicitly use matched model-token records, not the published-price denominator or all reported model tokens.
- Transcription models enter the Media/audio group before mini/nano classification.

The source-table token discrepancy remains unresolved: 69.9066% Anthropic and 8.4172% OpenAI at October 11. No cache or discount residual was fitted. Matched-model token coverage is 98.5652% and 99.6497%, respectively. These source tables are not independent economic validations of each other.

The research can be used as a qualified panel study, with observed mix serving as a PARTIAL proxy. It does not establish company-wide token prices, consolidated revenue per token, subscription economics, or a stable-cohort price trend. No November-December outcome is asserted.

## Follow-up — October 23, 2026

The original review above is preserved. A deeper live-source reconciliation has now been independently reviewed: **arithmetic PASS; denominator suitability for revenue modeling FAIL; model status HOLD**. See [reconciliation](reconciliation/reconciliation.md) and [independent follow-up audit](reconciliation/audit.md). Original prices and sensitivities remain descriptive arithmetic only. Cost agreement does not establish common token populations or actual billed revenue; no causal cache or subscription explanation has been verified.
