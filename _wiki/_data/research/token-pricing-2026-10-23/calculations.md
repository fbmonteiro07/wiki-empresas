# Anthropic and OpenAI token pricing: 2026 through October 23

**2026-10-23 FOLLOW-UP — MODEL USE: HOLD.** See [denominator reconciliation](reconciliation/reconciliation.md). The initial panel observations below are preserved. Neither blended ratios nor earlier 10pp sensitivities are validated economic model inputs; reported cost is not established actual billed revenue.

Source: Ramp Economics Lab / Ara Kharazian, https://ramp.com/data/ai-index. Raw capture: 2026-10-14 11:39. Latest complete token week: October 5-11, 2026.

**HARD:** raw source records. **ANCHOR:** reported model volumes and cost (actual billed revenue unvalidated). **PARTIAL:** provider-wide representativeness and family mapping. **ESTIMATE:** hypothetical sensitivity.

There is no invented input/output ratio, cache rate or discount factor. Model mix is directly anchored to observed volumes. No independent company-wide validation is available.

## Published blended-price series

USD per million tokens; trailing seven days at selected month-end Sundays. October is partial. These are snapshots, not monthly averages.

| Week ending | Anthropic | OpenAI |
|---|---:|---:|
| 2026-01-25 | 1.4515 | 0.6935 |
| 2026-02-22 | 1.5664 | 0.7666 |
| 2026-03-29 | 1.4235 | 0.7228 |
| 2026-04-26 | 1.1914 | 0.7160 |
| 2026-05-31 | 1.1861 | 0.8051 |
| 2026-06-28 | 0.9063 | 0.9276 |
| 2026-07-26 | 1.4035 | 0.9341 |
| 2026-08-30 | 1.0739 | 0.5902 |
| 2026-09-27 | 0.8617 | 0.6567 |
| 2026-10-11 | 0.8042 | 0.4788 |

## Product family mix: observed panel proxy

All shares use model-volume records only. The tables are not blended with the published-price denominator. Zero-cost rows remain in the volume mix.

### Anthropic

| Family | Jan 25 token % | Jun 28 token % | Oct 11 token % | Oct 11 observed spending % | Oct 11 matched-model USD/M |
|---|---:|---:|---:|---:|---:|
| Opus | 41.89 | 53.91 | 70.37 | 75.84 | 0.5102 |
| Sonnet | 46.22 | 18.02 | 19.98 | 13.33 | 0.3159 |
| Fable | 0.00 | 0.00 | 6.08 | 9.31 | 0.7257 |
| Haiku | 11.79 | 28.07 | 2.11 | 1.42 | 0.3174 |
| Other/unmapped | 0.10 | 0.00 | 1.43 | N/A: missing | N/A |
| Mythos | 0.00 | 0.00 | 0.03 | 0.10 | 1.6646 |

### Openai

| Family | Jan 25 token % | Jun 28 token % | Oct 11 token % | Oct 11 observed spending % | Oct 11 matched-model USD/M |
|---|---:|---:|---:|---:|---:|
| Luna/mini/nano | 62.45 | 41.36 | 50.09 | 12.45 | 0.1098 |
| Sol | 0.00 | 0.04 | 30.52 | 31.49 | 0.4557 |
| Astra | 0.00 | 0.00 | 8.15 | 29.85 | 1.6186 |
| Other text/legacy | 32.55 | 54.82 | 6.66 | 18.62 | 1.2780 |
| Terra | 0.00 | 0.00 | 2.80 | 4.12 | 0.6506 |
| Embedding/moderation | 4.83 | 3.57 | 1.63 | 0.21 | 0.0613 |
| Media/audio | 0.18 | 0.20 | 0.15 | 3.25 | 9.3167 |

## Reconciliation: material unresolved denominator difference

| Provider, Oct 11 | Published tokens, trillion | Model-series tokens, trillion | Token difference | Published USD/M | Model-series USD/M |
|---|---:|---:|---:|---:|---:|
| anthropic | 25.146006 | 42.724724 | 69.91% | 0.8042 | 0.4803 |
| openai | 25.570513 | 27.722837 | 8.42% | 0.4788 | 0.4432 |

Cross-table spending differs by less than 0.1% in the latest week, but token denominators do not reconcile. Anthropic is RED (>25% gap); OpenAI is AMBER (>1% gap). Do not blend the two bases or infer caching from the residual. Model-series prices use matched positive-token records; mix uses all model-volume records.

## Worked calculation and sensitivity

For each matched model: P_i = 1,000,000 x spending_i / tokens_i. Matched-model weight w_i = tokens_i / sum(matched tokens_i). Therefore sum(w_i x P_i) = 1,000,000 x matched spending / matched tokens. This is an accounting identity, not external validation.

anthropic: published-price basis = $20,221,880.22 / 25,146,006,422,083 tokens x 1,000,000 = $0.804179/M. Separately, matched-model basis = $20,225,730.19 / 42,111,692,769,518 x 1,000,000 = $0.480288/M. Matched token coverage = 98.565%; spending with zero tokens = $199.40.

openai: published-price basis = $12,243,575.09 / 25,570,512,740,004 tokens x 1,000,000 = $0.478816/M. Separately, matched-model basis = $12,244,893.61 / 27,625,724,966,501 x 1,000,000 = $0.443242/M. Matched token coverage = 99.650%; spending with zero tokens = $188.30.

ESTIMATE scenario, openai: move 10 percentage points of MATCHED model-series tokens from Luna/mini/nano to Astra, fixed observed family rates. Delta = 0.10 x (1.618621 - 0.109822) = $0.150880/M (34.04%).

ESTIMATE scenario, anthropic: move 10 percentage points of MATCHED model-series tokens from Sonnet to Opus, fixed observed family rates. Delta = 0.10 x (0.510211 - 0.315892) = $0.019432/M (4.05%).

## Guardrails

- PASS: row uniqueness, nonnegative quantities, weights sum to 100%, weighted-price identity on matched records. Missing price records are excluded explicitly.
- RED/AMBER: cross-table token denominators; cause unresolved.
- UNAVAILABLE: independent company-wide realized-ASP and stable-cohort validation.
- No stock/flow comparison: all calculations use matching seven-day flows.

## Limitations
- Published-price denominator differs from the model-volume sum. Cause unknown; no caching, discount or tokenizer residual is inferred.
- No global API revenue or token-volume anchor; these outputs cannot establish company ASPs.
- Subscriptions, API-equivalent allowances, enterprise contracts, and revenue shares cannot be converted to dollars per token without matched usage and recognized revenue.
- A weighted-price identity verifies arithmetic only. It is not independent economic validation.
- Different model tokenizers and changing workloads mean tokens are not constant compute or constant successful tasks.
- Missing model spending is null, not zero: price calculations exclude unpaired volume and zero-token rows. Full token-mix calculations retain all observed volumes.
- Explicit zero model spending is retained as reported; it is not interpreted as a free list price.
- The 10pp sensitivity fixes all within-family billing rates and is a partial-equilibrium scenario.

## Changelog

- 2026-10-23 follow-up: original rates, mix and scenario arithmetic preserved. Updated status from qualified panel study to explicit HOLD for economic model use after live-source reconciliation. Replaced ambiguous billing terminology with reported cost; no original numerical observation overwritten. See reconciliation/reconciliation.md.
