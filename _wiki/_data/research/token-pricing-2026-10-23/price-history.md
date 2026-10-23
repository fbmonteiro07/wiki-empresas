# Official token-price history — prepared October 23, 2026

All prices below are USD per million tokens, standard processing and short/default context, uncached input / output. **HARD** denotes a published vendor rate; this is not a realized revenue figure. Launch dates are distinguished from later revisions. No price after October 23 is treated as an outcome.

## Anthropic

| Event date | Models/event | Input / output | Source |
|---|---|---|---|
| Opening 2026; launch 2025-11-24 | Opus 4.5 | 5 / 25 | [Anthropic launch](https://www.anthropic.com/news/claude-opus-4-5) |
| 2026-02-17 | Sonnet 4.6 keeps Sonnet 4.5 prices | 3 / 15 | [Anthropic launch](https://www.anthropic.com/news/claude-sonnet-4-6) |
| Opening 2026 | Haiku 4.5 | 1 / 5 | [Anthropic Haiku comparison, October 7](https://www.anthropic.com/claude-haiku-5-5) |
| 2026-06-09 | Fable 5 / Mythos 5 | 10 / 50 | [Anthropic launch](https://www.anthropic.com/news/claude-fable-5-mythos-5). Access suspended June 12 and redeployed July 1; does not imply continuous June availability. |
| 2026-06-30 | Sonnet 5 introductory rate | 2 / 10 | [Anthropic launch and revision log](https://www.anthropic.com/news/claude-sonnet-5) |
| 2026-07-24 | Opus 5, same rates as Opus 4.8 | 5 / 25 | [Anthropic launch](https://www.anthropic.com/news/claude-opus-5) |
| 2026-08-10 | Sonnet 5 intro price made permanent | 2 / 10 | [Official revision log](https://www.anthropic.com/news/claude-sonnet-5). The planned September 1 rate of 3 / 15 was cancelled, not implemented. |
| 2026-09-22 | Opus 5.5 | 4 / 20 | [Anthropic launch](https://www.anthropic.com/claude-opus-5-5). Cache reads 0.20, down from 0.50. |
| 2026-09-28 | Sonnet 5.5 | 2 / 10 | [Anthropic launch](https://www.anthropic.com/claude-sonnet-5-5). The current launch page incorporates later cache-price revisions. |
| 2026-10-07 | Haiku 5.5, prompts up to 100k | 0.10 / 0.50 | [Anthropic launch](https://www.anthropic.com/claude-haiku-5-5). Over 100k: 0.50 / 2.50. |
| 2026-10-07 | Sonnet 5.5 cache-read cut | 0.20 → 0.10 cached input | [Dated announcement](https://www.anthropic.com/claude-haiku-5-5). This announcement supplies the effective date rather than backdating the current Sonnet page. |

Current Fable 5.1 rate is 10 / 50; cache reads 0.25. [Vendor pricing page, accessed October 23](https://claude.com/pricing).

## OpenAI

| Event date | Models/event | Input / output | Source |
|---|---|---|---|
| Opening 2026; launch 2025-12-11 | GPT-5.2 | 1.75 / 14 | [OpenAI launch](https://openai.com/index/introducing-gpt-5-2/) |
| 2026-03-05 | GPT-5.4 | 2.50 / 15 | [OpenAI launch](https://openai.com/index/introducing-gpt-5-4/) |
| 2026-04-24 API availability | GPT-5.5 | 5 / 30 | [OpenAI launch with API update](https://openai.com/index/introducing-gpt-5-5/). Pro separately 30 / 180. |
| 2026-07-09 | GPT-5.6 Sol / Terra / Luna | 5 / 30; 2.50 / 15; 1 / 6 | [OpenAI launch](https://openai.com/index/gpt-5-6/) |
| 2026-07-30 | GPT-5.6 Terra / Luna cuts | 2 / 12; 0.20 / 1.20 | [OpenAI price-performance announcement](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/). Published cuts 20% / 80%; rates reconciled with original launch and later GPT-6 comparison. |
| 2026-08-21 | GPT-5.6 Sol promotion | 4 / 20 | [Dated launch-page update](https://openai.com/index/gpt-5-6/) and [explicit subsequent comparison](https://openai.com/index/introducing-gpt-6-sol-and-luna/). Current docs say available at least through November 21; this remains a promotional price. |
| 2026-09-03 announcement | GPT-6 Astra | 10 / 50 | [OpenAI launch](https://openai.com/index/gpt-6-astra/) |
| 2026-09-22 | GPT-6 Sol / Luna | 2 / 10; 0.10 / 0.50 | [OpenAI launch](https://openai.com/index/introducing-gpt-6-sol-and-luna/) |
| 2026-09-29 | GPT-6.1 Sol | 2 / 10 | [OpenAI launch](https://openai.com/index/introducing-gpt-6-1-sol/). Cache reads 0.10 versus GPT-6 Sol's 0.20. |

[Current OpenAI API rate card, accessed October 23](https://developers.openai.com/api/docs/pricing) confirms current standard versus batch/flex/fast/ultrafast rates. The flagship path is not a same-product price index: GPT-6 Astra adds a new premium tier while Sol and Luna address lower-cost workloads.

## Billing basis

Cache reads, cache writes, output, and uncached input carry distinct rates. Standard list prices cannot be averaged with arbitrary equal weights. Batch/flex discounts, fast-tier premiums, long-context rates, enterprise discounts, subscription allowances and cloud reseller revenue recognition affect realized revenue per token. Reasoning tokens are billable output where applicable, rather than just visible answer tokens. No adjustment factor for these items is guessed in this study.

## Evidence strength

Official rates: HARD as published. Ramp observed mix and price inputs: HARD within its TSM sample, with source-table discrepancies flagged. Applying that mix to entire providers: PARTIAL, not independently calibrated. The 10pp scenarios in calculations.md are ESTIMATE counterfactuals. No forecast for November-December is presented.
