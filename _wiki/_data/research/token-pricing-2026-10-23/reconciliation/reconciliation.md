# Ramp denominator reconciliation — 2026-10-23

**MODEL STATUS: HOLD.** Cost numerators nearly reconcile; token denominators do not. Neither published nor matched-model ratios are validated company realized ASPs. No adjustment factor has been fitted. Independent review: arithmetic PASS, denominator suitability FAIL, overall PARTIAL; see [audit](audit.md).

Source: Ramp Economics Lab / Ara Kharazian, public chart exports re-fetched October 23, 2026. Latest complete week: October 5-11. Data version `b1ACnM4ULJjULGFdkttsRs`.

**HARD** = source fields as reported. **DERIVED** = exact calculations from them. **PARTIAL** = model-name classification and accounting hypotheses. No assumed cache rate or discount.

## Same-week bridge

| Item | Anthropic | OpenAI |
|---|---:|---:|
| Price-series tokens N (trillion) | 25.146006 | 25.570513 |
| Model-series tokens T (trillion) | 42.724724 | 27.722837 |
| Difference G=T-N (trillion) | 17.578718 | 2.152325 |
| Difference as % of N | 69.9066% | 8.4172% |
| Difference as % of T | 41.1441% | 7.7637% |
| Price-series cost C ($) | 20,221,880.22 | 12,243,575.09 |
| Model-series cost S ($) | 20,225,929.59 | 12,245,081.91 |
| Cost difference (%) | 0.0200% | 0.0123% |
| Published price C/N ($/M) | 0.804179 | 0.478816 |
| Matched-model ratio ($/M) | 0.480288 | 0.443242 |
| Missing-spend model tokens (trillion) | 0.613031 | 0.097112 |
| Maximum share of gap these could explain (%) | 3.4873% | 4.5120% |
| Gap after removing ALL missing-spend volume (trillion) | 16.965686 | 2.055212 |

The missing-volume subtraction is a conditional maximum, not a demonstrated source filter. Absence of spending is not evidence of free consumption. Matched-model ratios exclude those missing-spend models and positive spending with zero reported tokens.

## Worked Anthropic arithmetic

- G = 42,724,724,082,806 - 25,146,006,422,083 = 17,578,717,660,723 tokens; G/N = 69.90659815%.
- Published price = $20,221,880.22128914 / 25,146,006,422,083 x 1,000,000 = $0.804178599/M.
- Matched tokens = 42,724,724,082,806 - 613,031,313,288; matched cost = $20,225,929.59437014 - $199.40127425; ratio = $0.480287751/M.
- Multiplying the published rate by the model-volume count would imply $34,358,308.77, versus $20,221,880.22 of price-series cost: 69.91% excess by construction. This is a basis-error illustration, not revenue.
- Opus share is separately 70.3704% of T. It is not the 69.9066% denominator gap.
- claude-opus-5-5 alone has 25,454,369,373,469 tokens, exceeding the entire price-series denominator N. This demonstrates incompatible totals; it does not identify the faulty series.

## Hypotheses tested

- **Stale or differently dated downloads:** live and archived JSON records are identical, including UTF-8 labels. Both endpoints use the same live dataVersion.
- **Our aggregation / top-N UI filter:** no duplicate row keys; all model records are weekly seven-day flows. Ramp frontend sums all model rows by maker and separately computes price as 1e6*cost/count. Top-N display choices do not reconcile the raw bases.
- **Timing:** +/-7-day shifts on a common 39-week 2026 sample worsen median cost alignment. No shift jointly reconciles cost and tokens. Source timezone and upstream bucket rules still need confirmation.
- **Missing/zero-price models:** no positive-token model has an explicit zero spending record in the latest week. Missing-spend tokens can cover at most 3.4873% of Anthropic and 4.5120% of OpenAI gaps if all are excluded from N.
- **OpenAI non-text models:** removing the union of missing-spend and name-matched embedding/moderation/media models can cover only 25.85% of its latest gap, even if every removal were justified. This is a coverage test, not an approved exclusion rule.
- **Simple no-cache identity N=U+O:** fails numerically. This would reject all-cache exclusion ONLY if the cohorts matched and U/O exhaustively covered compatible non-cache categories. Those assumptions remain unverified, so caching as a broader explanation is not ruled out.
- **Duplicating the entire arithmetic residual once:** G is not equal to N-uncached_input-output. This rejects that identity, not other cache treatments, nested-field overlap or different cohorts.
- **Multiple provider connections, missing price-eligible usage, or upstream joins:** plausible but unverified; the exports contain no connection, customer, token-type-by-model, or inclusion flags to test these. Ramp product documentation supports separate API/Enterprise app connections, but that does not establish subscription inclusion in the Index. The frontend describes model-attributed API spend.

## Token-type bridge (do not label the residual a measured cache rate)

| Provider | N, trillion | Uncached input U | Output O | R=N-U-O | R/N | G/R |
|---|---:|---:|---:|---:|---:|---:|
| anthropic | 25.146006 | 1.037370 | 0.215971 | 23.892665 | 95.02% | 73.57% |
| openai | 25.570513 | 6.201685 | 0.684240 | 18.684588 | 73.07% | 11.52% |

The Claude API separately reports uncached input, cache reads, cache creation and output. In the Messages response documented under prompt caching, the cache-creation aggregate overlaps its 5-minute/1-hour subfields, so summing both would double count. The organization Usage Report example instead exposes the nested subfields without that duplicate aggregate. Ramp documents Admin API ingestion but does not disclose the precise transformation behind these exports. This illustrates a schema risk, not evidence that Ramp made that error. The public Ramp all_tokens export provides no comparable partition.

## Historical instability

| Week ending | Anthropic T/N-1 | OpenAI T/N-1 |
|---|---:|---:|
| 2025-12-28 | 0.17% | 1.80% |
| 2026-01-25 | 7.09% | 1.84% |
| 2026-03-29 | 33.23% | 3.01% |
| 2026-06-28 | 40.93% | 10.13% |
| 2026-07-26 | 70.83% | 13.03% |
| 2026-09-27 | 83.36% | 14.26% |
| 2026-10-11 | 69.91% | 8.42% |

A flat 1.6991x correction is contradicted by history. Without a matched cohort and common token definition, the price trend cannot be attributed solely to tariff changes, cache adoption, discounts or family mix.

## What is needed to release the model hold

1. A bridge for October 5-11 by provider, model, connection/product and token type, explaining Anthropic 42.724724T -> 25.146006T and OpenAI 27.722837T -> 25.570513T.
2. Exact all_tokens and token_volume definitions, including cache writes/read, aggregate-versus-subfield overlap, reasoning and media tokens, and free/early-access usage.
3. Identical customer/connection filters, timezone/date rules and deduplication keys for the two exports; explicit API versus Enterprise app/Claude Code/Codex treatment.
4. Whether cost means billed net revenue, pre-discount list-equivalent usage, credits valued at overage prices, or another estimate; treatment of tools and zero-token costs.
5. Corrected historical series or a documented reproducible bridge, rather than a one-week factor.

Until then, retain model-family shares as source-specific volume observations; do not combine them with the published-price denominator, use a blended ASP in revenue forecasts, or carry over the earlier 10pp mix sensitivity as a validated economic result.

## Primary-source evidence

- [Ramp AI Index, Ara Kharazian](https://ramp.com/data/ai-index): TSM sample description, published chart figures; checked October 23, 2026.
- [Live price export](https://ramp.com/data/ai-index/chart-data/tokenPrices?version=b1ACnM4ULJjULGFdkttsRs) and [live model export](https://ramp.com/data/ai-index/chart-data/tokenVolumes?version=b1ACnM4ULJjULGFdkttsRs): saved locally with hashes.
- [Ramp public frontend bundle](https://ramp.com/_next/static/immutable/chunks/3esy_8xboh9bh.js): maker sum (offset 18327), direct cost/token price formula (offset 28614), and model-attributed API spend source label; saved locally with hash.
- [Ramp AI Spend Management documentation](https://support.ramp.com/ai-token-spend-management), checked October 23: API and Enterprise app connections are separate; OpenAI API credit-plan estimates may value included/prepaid consumption at overage rates instead of actual billed spend. The documentation does not say whether the public Index uses those estimates.
- [Ramp agent-tool definitions](https://agents.ramp.com/docs/reference/agent-tools): distinguishes estimated usage/cost aggregates from actual vendor spend from payment records.
- [Claude token accounting](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) and [Messages Usage Report](https://platform.claude.com/docs/en/api/beta/organization/usage_report/retrieve_messages): disjoint top-level token categories and nested cache-creation subfields. No Ramp backend lineage disclosed.

## Changelog

- 2026-10-23 follow-up: preserved the initial study and all original raw observations. Extended audit confirms live mismatch; added explicit HOLD for economic model use. Earlier matched-model rates and mix sensitivities remain arithmetic diagnostics, not approved model inputs.
