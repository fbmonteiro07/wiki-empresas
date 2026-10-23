## Double-check verdict: Anthropic / OpenAI token-price sources — PARTIAL

Audited 2026-10-23. **The 37 quoted price/event rows PASS source verification. The USD 0.802084/M Anthropic and USD 0.500903/M OpenAI benchmarks PASS as saved Ramp panel ratios; their interpretation as realized company ASPs or measured consumption remains unvalidated.** This is a source and inference audit, not a certification of the house ARR forecast or the full spreadsheet engine.

Read-only work covered `price_references.json`, the category/model preparation and workbook builders, prior reconciliation, both archived raw Ramp exports, and their live endpoints. All 19 referenced URLs were checked: 17 vendor/methodology references through web retrieval, including the two page-specific links to the same dated PDF; the two JSON endpoints through PowerShell after the browser fetcher could not retrieve them. Live responses returned HTTP 200 and exactly matched the archived parsed objects: 3,894 price rows and 19,156 model-metric rows. Only this audit and its JSON companion were written by this reviewer.

### 1. Outlook email coverage

Not applicable to this narrow dataset/workbook audit. No broker-coverage claim is certified.

### 2. SEC filings coverage (last 2 years)

Not applicable. These are private-company scenario inputs and vendor/API sources, not a single-name securities preview. No filing-dependent claim is certified.

### 3. Bloomberg API cross-check (REFERENCE ONLY — not gabarito)

Not applicable. Independent recomputation from the raw source, rather than the previous audit's tables, produced:

| Saved period | Anthropic | OpenAI |
|---|---:|---:|
| Weeks ending October 4 and 11: all-token count | 44,634,785,737,866 | 49,264,564,561,661 |
| Same weeks: reported cost, USD | 35,800,852.69442121 | 24,676,765.75983598 |
| Reported cost / count, USD/M | 0.8020841167 | 0.5009029508 |
| Unclassified count residual / all tokens | 95.05982650% | 72.90761380% |
| October 11: price-feed count | 25,146,006,422,083 | 25,570,512,740,004 |
| October 11: model-feed count | 42,724,724,082,806 | 27,722,837,284,884 |
| Model-feed excess versus price-feed count | 69.90659815% | 8.41721309% |

Source: Ramp Economics Lab / Ara Kharazian, October 23 retrieval, [price feed](https://ramp.com/data/ai-index/chart-data/tokenPrices?version=b1ACnM4ULJjULGFdkttsRs) and [model feed](https://ramp.com/data/ai-index/chart-data/tokenVolumes?version=b1ACnM4ULJjULGFdkttsRs). Ratios are derived, not independent observations. Formula: one million times summed reported cost divided by summed token count. The October sample covers September 28–October 11; it is neither full October nor a current October 23 price.

### 4. Transcript coverage

Not applicable. Original vendor documentation was checked instead. The following maps every reference-table row to the independently opened source. All prices are USD/M; pairs are input/output unless three values are explicitly described as input/cache-read/output. Blank/not-quoted cache fields were not treated as zero.

| Reference rows | Independent verification | Result |
|---|---|---|
| History 1 | Opus 4.5, November 24, 2025; 5/25. [Launch](https://www.anthropic.com/news/claude-opus-4-5) | PASS |
| History 2 | Sonnet 4.6, February 17, 2026; 3/15, unchanged from 4.5. [Launch](https://www.anthropic.com/news/claude-sonnet-4-6) | PASS |
| History 3–5 | Effective May 27 PDF: Opus 4.8 5/0.5/25, Sonnet 4.6 3/0.3/15, Haiku 4.5 1/0.1/5. Scope, writes and context qualifiers match pages 1–2. [Dated rate card](https://www-cdn.anthropic.com/files/4zrzovbb/website/3684c2faafb97418665782cea0001f439f74b1d2.pdf) | PASS |
| History 6 | Fable/Mythos 5, June 9; 10/50. June 12 suspension and July 1 restoration are documented. [Launch and updates](https://www.anthropic.com/news/claude-fable-5-mythos-5) | PASS |
| History 7–8 | Sonnet 5, June 30; 2/10. August 10 edit makes it permanent and cancels the planned September increase. [Launch revision log](https://www.anthropic.com/news/claude-sonnet-5) | PASS |
| History 9, 11–13 | August 21 Sol promotion 4/20; September 22 Sol 2/0.2/10 and Luna 0.1/0.01/0.5; September 29 Sol 6.1 2/0.1/10 with 2.5 writes. Dates/rates explicit. [API changelog](https://developers.openai.com/api/docs/changelog) | PASS |
| History 10 | Opus 5.5, September 22; 4/0.2/20, with Opus 5 comparison. [Launch](https://www.anthropic.com/claude-opus-5-5) | PASS |
| History 14; modifiers 1 | Sonnet 5.5 October 7 read-price cut; September 28 launch; March 13 standard-price long context for Opus/Sonnet 4.6. [Release notes](https://platform.claude.com/docs/en/release-notes/overview) | PASS |
| History 15–16 | Haiku 5.5, October 7; up to 100k 0.1/0.01/0.5; over 100k 0.5/0.05/2.5. Write rates match. [Launch table](https://www.anthropic.com/claude-haiku-5-5) | PASS |
| Current 1 | GPT-5.2 current 1.75/0.175/14; snapshot identifier December 11, 2025. [Model page](https://developers.openai.com/api/docs/models/gpt-5.2) | PASS |
| Current 2 | GPT-5.4 current 2.5/0.25/15; long-context multiplier verified. March 5 release corroborated separately in changelog. [Model page](https://developers.openai.com/api/docs/models/gpt-5.4) | PASS |
| Current 3 | GPT-5.5 current 5/0.5/30; April 24 API launch corroborated separately in changelog. [Model page](https://developers.openai.com/api/docs/models/gpt-5.5) | PASS |
| Current 4–9 | GPT-5.6 Sol, Astra, Sol 6.1, Luna and Sol Flex/Batch/Fast rates, cache writes and promotional qualifier match current official table. [Pricing](https://developers.openai.com/api/docs/pricing) | PASS |
| Current 10–15; modifiers 6 | Fable 5.1, Opus/Sonnet 5.5 standard, specified batch rows, writes, and approximate newer-tokenizer effect match the current table. [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing) | PASS |
| Modifiers 2–4 | July 30 Terra/Luna cuts and Fast tier; October 20 introduction of 12h writes at 2.5x input. [API changelog](https://developers.openai.com/api/docs/changelog) | PASS |
| Modifiers 5 | Eligible Batch work has 50% discount and asynchronous service conditions. [Batch guide](https://developers.openai.com/api/docs/guides/batch) | PASS |

Historical and current-snapshot evidence are separated correctly. A current GPT-5.2/5.4/5.5 rate card does not prove the corresponding historical launch price, and the workbook explicitly says so. The official rates do not supply observed model, cache-duration, service-tier, regional, or contract weights. October 20 cache terms postdate the Ramp sample and must not be treated as its observed billing terms.

### 5. Unsourced or weakly-sourced claims in prior work

1. **HIGH — Cost numerator is not validated as billed or recognized revenue.** The public [Index methodology](https://ramp.com/data/ai-index) describes imported usage/billing information but does not document net recognized revenue. [Ramp support](https://support.ramp.com/ai-token-spend-management), checked October 23, says some OpenAI API credit-plan cost estimates value included/prepaid usage at overage rates and are not actual billed spend. Its [tool documentation](https://agents.ramp.com/docs/reference/agent-tools) separately distinguishes estimated usage/cost aggregates from actual vendor spend. The exact public-Index lineage is unconfirmed: do not assert that its cost is definitely list-equivalent. Even if the token-count difference were repaired, this numerator question would remain. Main outputs `Consumption!M16/M34` and `Price build!M10/M50` need a direct nearby warning, not just an indirect revenue caveat.

2. **HIGH — There is no validated common token denominator or company population.** Independent live retrieval confirms the raw mismatch rather than resolving it. Nearly matching cost totals cannot prove matched customers, connections or token definitions. Ramp itself says the TSM sample is not representative of total Ramp AI spend; that is narrower than either provider's worldwide business. Use 0.802084/0.500903 as source-specific benchmark scenarios only, with the full period and source visible. They are not evidence of the true company ASP or a best estimate selected by economic validation.

3. **MEDIUM — The residual remains unclassified.** `Price build!M16/M56` contain 95.06%/72.91% arithmetic remainders. The adjacent heading and note correctly disclose that they are not measured cache reads, but `Consumption!C52/C56` still put “cache” into the short label. Preferred wording is “unclassified residual (possible cache/other)” everywhere. Native APIs distinguish ordinary input, cache creation, cache reuse, and output; prices differ across model generations and durations. The source feed does not provide a verified read/write partition. Source equality and nonnegative residuals establish neither exhaustive categories nor common cohorts.

4. **MEDIUM — The minimum is a scenario selection rule, not a lower bound.** Taking the smaller of two incompatible ratios raises implied volume mechanically. Official cheap-model rates and batch discounts do not turn that selection into a company minimum ASP; actual weights and contracts are missing. Retain “lower of two unresolved Ramp references” language beside the result.

5. **LOW — Date and current-card discipline must survive presentation.** The reference worksheet handles snapshot versus historical evidence correctly. Preserve that distinction in any summary; do not describe the two-week price as “October 23 realized pricing,” extrapolate one tokenizer factor into a cross-feed correction, or explain the price trend solely as tariff/cache changes.

These are economic interpretation limits, not newly discovered arithmetic defects. The workbook already discloses most of them. No factual price/event error was found in the 37 reference rows.

### 6. What the prior analyst MUST do before this work ships

- Put an explicit cost-basis warning next to the headline outputs: **“Ramp cost basis is not verified as billed/recognized revenue; some documented credit-plan estimates use overage-rate valuation, and applicability to this public Index is unconfirmed.”** Attribute Ramp support, October 23, 2026.
- Keep the published-panel benchmark, unresolved-denominator, partial-period, forecast, and equivalent-consumption labels. Avoid presenting the 0.8021/0.5009 recommendation as a validated company ASP.
- Keep “unclassified residual” first in short labels. Do not describe residual-share sensitivities as measured cache-hit effects.
- Before claiming actual provider consumption, obtain a common-customer, common-product bridge by model/token category/period and reconcile billed or recognized API revenue to the numerator. A new rate-card citation alone cannot supply this evidence.

### 7. Bottom line

The price-reference work is supported: all 37 dated/current rows checked out against official sources. The source-defined benchmarks are reviewable scenario inputs, but actual company pricing, cache use and token consumption remain unproven; the largest missing evidence is a revenue-matched token universe, not another arithmetic identity.
