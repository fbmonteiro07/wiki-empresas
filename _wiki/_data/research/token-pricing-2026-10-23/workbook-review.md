# Workbook review — AI_Token_Consumption_Price_and_Mix.xlsx (2026-10-23)

File reviewed: `outputs/01a168b5-7786-7582-8082-7cd6bd45fd69/AI_Token_Consumption_Price_and_Mix.xlsx` (saved 2026-10-23 12:28; third version after `..._and_Minimum_Price.xlsx` 10:24 and `..._with_References.xlsx` 11:56). Six sheets: Consumption, Minimum price, Token mix, Inputs, Price references, Price build. 2,337 formulas, no defined names, no hidden sheets.

## Verdict

**Arithmetic: PASS. Inputs: PASS (traced to the house model). Usability as a token estimate: PARTIAL** — the number is right *conditional on the price basis*, and the two Ramp bases disagree by 70% on Anthropic tokens. The workbook already says so; what it lacks is (1) an external volume anchor, (2) a list-price bridge that explains the Ramp effective rates, (3) a constant-unit view of token growth.

### What was independently re-verified

| Check | Result |
|---|---|
| ARR inputs vs `P:\Felipe Monteiro\US Equities\Modelos oficiais\AI Model.xlsx` (saved 2026-10-23 09:50), ARR Tracker rows 98/84 (Anthropic gross/net) and 95/81 (OpenAI gross/net), P:AA | exact match, all 12 months × 4 series |
| API shares: `Anthropic!AB11` = 0.85 (gross), `OpenAI!AB29` = 0.2467 (net, row "API Revenue (net)") | exact match |
| Monthly price = Σ weekly cost ÷ Σ weekly tokens (token-weighted, not equal-weighted) | recomputed from raw rows: Anthropic Jun 1.098102 / Oct 0.802084; OpenAI Jun 0.836518 / Oct 0.500903 — match to 6 dp |
| ARR/12 ÷ $/M = quadrillion tokens/month; ×1000/calendar days = T/day | recomputed: Anthropic Oct 7.832654 Q, 252.666 T/day; OpenAI Oct 9.468183 Q, 305.425 T/day — match |
| Price-build identity (Σ share × effective rate = published price) | bridge error 0 in every observed month |
| Guards (shares sum to 1, residual ≥ 0, Nov/Dec override validity) | all PASS |
| Raw Ramp rows (tokenPrices 3,894 rows: all_tokens / uncached_input / output; tokenVolumes 19,156 rows) | match the archived JSON; same vintage `b1ACnM4ULJjULGFdkttsRs` |

Note: the E: copy of AI Model (`Modelos oficiais/AI Model/AI Model.xlsx`, 2026-07-16) does **not** contain these rows — the workbook used the P: copy. Keep the P: path in Inputs!C25.

## Improvements, ranked

### 1. Add an external-anchor block (the workbook has none)

Marks already on disk, with the workbook's implied values beside them:

| Anchor (source, date) | Mark | Workbook implied | Read |
|---|---|---|---|
| OpenAI API >6B tokens/min late-2025 exit (JPM Sur, AI Capex 2.0, 2026-06-16 — the anchor in `Tokenomics_bottom_up_v1.xlsx`) | 8.6 T/day | Jan-26 API-only 24.1 T/day (16.7 B/min) | 2.8x the late-25 floor one month later — driven by API share 24.7% here vs 17% in the house anchor, and Ramp's OpenAI price ($0.67) vs the back-solved $1.14 |
| OpenAI API ≈ 20 T/day at end-March-26 (Fireworks: ">40T/day = 2x the OpenAI API's volume at the end of March", Aug-26 ingest on `themes/tokenmaxxing.md`; third-party claim) | ~20 T/day | Mar-26 API-only 24.3 T/day | +20%, inside the noise of a third-party claim |
| House GW bridge mid-26 (`Tokenomics_GW_Bridge_v1.xlsx`, 2026-07-20): Anthropic ~4.1 Q/mo, OpenAI ~2.4 Q/mo | 4.1 / 2.4 Q | Jun-26 full-ARR 4.18 / 2.88 Q | +2% / +20% |
| Google direct-API 16 B tokens/min Mar-26 (Kurian, Stratechery 2026-04-23); 3.2 Q/mo all surfaces (I/O, May-26) | 0.69 Q/mo API | Anthropic Oct API-only 149 B/min | Anthropic implied at ~9x Google's direct API — state the ratio, it is the plausibility test |

### 2. Carry both Ramp bases as scenarios and add a list-price bridge

The published ($0.80) and matched-model ($0.46–0.48) October prices differ because the token denominators differ (T/N − 1 = 70%), not the cost. A bottom-up from the workbook's own pieces (Token mix family shares × Price references list rates × Price build category mix):

| Anthropic | Jan-26 | Oct-26 |
|---|---:|---:|
| List-weighted uncached input (family mix) | 3.61 | 3.89 |
| Ramp effective uncached input | 2.83 (−22%) | 2.82 (−28%) |
| List-weighted output | 18.07 | 19.45 |
| Ramp effective output | 19.69 (+9%) | 16.77 (−14%) |
| List-weighted cache-read | 0.36 | 0.18 |
| Ramp residual effective rate | 0.95 (2.6x) | 0.57 (3.2x) |
| Implied cache-WRITE share of residual tokens (reads + writes at list) | 14% | 8% |
| Blended list, residual = all reads | 0.97 | **0.50** |
| Blended list, with implied writes | 1.49 | **0.87** |
| Ramp published / matched | 1.44 / 1.36 | 0.80 / 0.46 |

Read: both Ramp bases are consistent with the rate card — the matched basis ≈ "residual is all cache reads", the published basis ≈ "8% of residual tokens are cache writes". List prices do not pick a winner, so present Low (matched) / High (published) rather than one "average", and show the implied write share (a checkable number: Claude Code workloads typically write 5–15% of cached tokens). Output lands near list; uncached input runs 22–28% below list (batch 50% tier and/or discounts).

For OpenAI the same bridge **fails** (effective input −52%, output −63% vs list-weighted by family): the tokenVolumes family mix and the tokenPrices category rates are not the same population. Drop the OpenAI family allocation in Token mix or label it unusable.

Revenue split the bridge yields (Oct-26): Anthropic input 14% / output 19% / residual 67%; OpenAI 46% / 21% / 33%.

### 3. Tokens are not a constant unit in 2026 — decompose growth

Three breaks sit inside the price series: the Claude 4.7+ tokenizer (~30% more tokens for the same text, vendor statement; 4.7 landed around April-26), cache-read cuts (Opus 5.5 $0.50→$0.20 on 2026-09-22; Sonnet 5.5 $0.20→$0.10 on 2026-10-07), Haiku 5.5 at $0.10 input. Add rows: ARR growth, price change, and "constant-price tokens" (revenue ÷ January price). Anthropic Jan→Oct: ARR 6.3x × price 0.56x⁻¹ = tokens 11.3x; at constant price 6.3x. The 1.8x between them is price, mix and tokenizer, not demand.

### 4. Nov/Dec extrapolation

October is two weeks (Sep-28 to Oct-11) with Haiku 5.5 and the Sonnet cache cut only half in; Inputs!D5 = 0% holds that blend flat. Default D5 to the Sep→Oct observed change, or drive it from a dated list-price event table.

### 5. Mechanical / presentation

- Token mix applies tokenVolumes shares (denominator T, 70% larger; Opus alone exceeds N) to Q computed on N — inconsistent by construction. Compute family Q on the matched basis or drop.
- Price build overrides (rows 27–29 / 67–69): make the residual the plug (1 − input − output) so one edit cannot invalidate the month.
- API-share conversion assumes all gross−net belongs to API (Anthropic on gross basis, OpenAI on net) — make it a visible dial.
- Ramp restates history silently (see `ramp-ai-index` memory); the vintage hash is in Inputs!C38 — re-pull before reuse.
- Ramp sample = card-paying SMB/mid-market; invoiced enterprise and cloud marketplaces (Bedrock/Vertex/Azure) are absent. The price is a pay-as-you-go read.

### 6. Three house price bases now coexist — pick one canonical

| Base | 2026 price | Where |
|---|---:|---|
| Tokenomics_bottom_up_v1 / full_market v2–v3 | $0.85 (2026), $0.65 (2027+); $1.14 2025 anchor | `Modelos oficiais/AI Model/` |
| GW bridge v1.2 | $1.40 (band 1.10–1.90), mid-26 | `P:\Felipe Monteiro\Semis MAP\Tokenomics_GW_Bridge_v1.xlsx` |
| This workbook (Ramp) | Anthropic YTD $1.16 published / $0.73 matched (Q1 1.53 → Q2 1.19 → Q3 1.14 → Oct 0.80); OpenAI $0.73 / $0.67 | this file |

The Ramp Anthropic path tracks the SemiAnalysis Tokenomics shape (~$1.02 1Q26 → ~$0.65 4Q26 exit) that the bottom-up model used. A canonical `tokens` entry in `_meta/assumptions.md` was left pending in July; this is the moment to set it.

## Status

Review only — no cell in the workbook was changed. Research folder `audit.md` / `reconciliation/` HOLD stands.
