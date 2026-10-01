# Token economics review — 2026-09-29

Reference: user-provided OpenRouter/JPM four-panel exhibit; user confirmed OpenRouter as the underlying source on 2026-09-29. Exact report date and JPM formula unavailable. This is Capstone's reproducible implementation, not a transcription.

## Independent audit

The quant-estimate workflow's double-check agent independently reconstructed all 13 retained captures using Decimal arithmetic and raw OpenRouter ranking, model and catalogue files. It verified model/variant keys, all last-active date buckets, matching source hashes and same-capture prices. The resulting token sums, average prices, weighted prices and cache scenarios agreed with the implementation. The latest completed-week total also reconciled to the separate OpenRouter model-chart endpoint. Arithmetic: PASS. Interpretation as economic spending: PARTIAL, because no comparable verified billed-spend anchor exists.

## Adjudication and corrections

- Public `total_usage` contains nonzero values, including some free-tagged rows. Its public-ranking units, attribution and fee scope remain unresolved. Retain and show it in a diagnostic table; do not call it USD, calibrate a multiplier from it or silently discard it.
- Raw cache and BYOK counters are zero in the examined captures. This is not proof of zero real caching or BYOK. State that limitation beside the scenarios.
- Duplicate usage windows must preserve their earliest valid capture. A later catalogue must not silently reprice an old window. Added a regression test.
- Total price coverage hides weaker categories. Display each category's latest coverage, include historical coverage in tables and mark low-coverage price/spend chart points. Unmatched tokens are absent from both weighted-price numerator and denominator.
- Tokenizers and workloads differ; tokens are not constant compute or constant task output. The public feed is a subset of OpenRouter traffic and OpenRouter is a subset of the AI market.

The revised study makes all five limitations explicit. Snapshot-price application and open/closed metadata remain PARTIAL; observed counts and list rates are HARD; hypothetical cache fractions are ESTIMATE. No arbitrary calibration constant was fitted.

## Methodology correction to the older dashboard

Older dashboard wording described cache-off list-price calculations as a ceiling approximately three times realized spend and compared a current run rate with March/June anchors. On 2026-09-29 those claims were replaced with “uncalibrated list-price scenario.” The historical anchors remain dated context, not a same-period calibration. Cache writes, tiers and fees mean cache-off base prices are not a guaranteed upper bound. The new four-panel study uses per-capture prices, separate scope labels and explicit coverage.

Primary definitions: [OpenRouter model API](https://openrouter.ai/docs/api/api-reference/models/list-all-models-and-their-properties), [prompt caching](https://openrouter.ai/docs/guides/best-practices/prompt-caching), [public data scope](https://openrouter.ai/docs/cookbook/administration/data-api). No public definition found there establishes the ranking feed's `total_usage` as comparable billed spending.

## Delivery verification

On 2026-09-29, all 12 token-economics tests, six gateway-chart tests and five Vercel tests passed. The integrated refresh rebuilt successfully after the Vercel collection advanced through 2026-09-28; `status.json` reported no errors. OpenRouter prices were captured on 2026-09-28 for the completed token window ending 2026-09-27.

HTTP checks returned 200 and confirmed the study on the main dashboard, standalone study, weekly brief and chart pack. The standalone contains four SVGs; the weekly pack contains fourteen and no JavaScript. Chart/section IDs are unique. The dated attachment exactly matches the published pack and passed the Outlook sender's dry-run validation (`validated_not_sent`); no test email was sent. The existing Friday heartbeat was updated in place, preserving 09:00 America/Sao_Paulo, the original task and sole authorized recipient. The existing Windows OpenRouter refresh task is enabled and calls the updated main builder.

Visual browser inspection could not be completed: the in-app navigation timed out and the Chrome native-host diagnostic reported a missing registry registration. No browser settings were changed. This limits visual QA only; the HTTP, HTML structure, numeric and email validation above succeeded.
