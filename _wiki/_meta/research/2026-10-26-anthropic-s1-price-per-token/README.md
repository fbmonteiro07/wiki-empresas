# Anthropic S-1: price-per-token read (2026-10-26)

Requested by Felipe on 2026-10-26: "highlights of the S-1 and a price-per-token read". This complements the separate numerical review in `../2026-10-26-anthropic-s1/` and does not replace it.

- **Source:** Anthropic, PBC, Form S-1, filed 2026-10-26, accession 0001628280-26-067168 (per the inbox `.source.json`).
- **Run:** `py -I ppt.py`. The output is in `output.txt`.

## Inputs, tagged

| Input | Tag | Where |
|---|---|---|
| Quarterly revenue and compute & infrastructure, 1Q25–2Q26 | HARD | S-1 p.158 |
| Functional cost of revenue: FY24 752, 1H25 1,019, FY25 2,773, 1H26 2,380 ($M) | HARD | Note 8, F-40 |
| Consumption share of revenue: 1H26 $13,064M of $16,286M | HARD | Note 2, F-27 |
| CSP marketplace share: 48% of 1H26 revenue | HARD | p.57; F-17 |
| Channel-fee increase $2.7bn (1H26) and $341M (FY25); marketing increase $273M | HARD | pp.150, 152 |
| Anthropic realized $/Mtok, all tokens incl. cache, from the Ramp TSM sample | PARTIAL | `_data/ramp-ai-index/panel.json`, pulled 2026-10-14 |
| June-2026 revenue split inside 2Q26 (geometric path, g = 1.20–1.30) | ESTIMATE | — |
| ~5Q tokens/month for June 2026 | PARTIAL, not independent | SemiAnalysis via @zephyr_z9, 2026-07-08 |

## Results

Ranges run from Ramp's spend÷volume series to its published 7-day price series.

- **Revenue ÷ cost of revenue** went 0.51x (FY24) → 1.14x (1H25) → 1.65x (FY25) → **6.84x (1H26)**. The 1H26 gross margin is 85.4%, using S-1 figures only.
- **Revenue per dollar of total compute** went 0.57x (2Q25) → 2.08x (2Q26).
- **Realized price:** 2Q25 $2.41–2.48/Mtok → **2Q26 $0.80–1.19**; June 2026 $0.73–1.10.
- **Implied paid tokens in 2Q26:** 3.3–4.8Q per month on all revenue. June: 4.1–6.7Q all-in, or 3.3–5.4Q consumption-only.
- **Allocated serving cost:** 1H25 $2.10–2.15/Mtok → **1H26 $0.135–0.186** (−91% to −94%).
- **Total compute per Mtok:** $4.82 → $0.51–0.70.
- **2Q y/y decomposition:** revenue 14.7x = price 0.33–0.48x × volume ~31–44x.
- **Channel fees (derived):** about $2.7–2.8bn in 1H26, ~17% of total revenue. That would be ~35% of marketplace revenue only if every fee went to a CSP, so treat it as an upper bound. FY25 works out to ~16–18% of marketplace revenue.

## Skeptic audit

A hostile double-check agent reviewed the model on 2026-10-26 and returned **PARTIAL**. All of its fixes are folded into the results above.

- Every S-1 HARD input was verified, and the unit math is correct.
- **Two Ramp series diverge about 1.5x in 2026.** The model now carries both as a range instead of choosing one.
- **Ramp is a weak calibrator.** Its June-26 sample is ~$53M, about 1% of revenue. It is API and direct-billed, so it probably misses CSP-marketplace sales and committed-price contracts. The direction of the bias is unknown.
- **"All-in" is a floor for paid tokens.** Subscription tokens are priced below API rates, and free-tier tokens are excluded entirely.
- **SemiAnalysis's 5Q is not an independent check.** It is likely revenue × an assumed price, so the write-up calls it the same order of magnitude, not a validation.
- **The cost-per-token figure depends on how costs are allocated.** It is management's split of a single fungible compute pool, Note 8 is now a supplemental table, and lease and depreciation costs only begin in 2026. It is labeled an allocated serving cost, with total compute as the bound.
- **Comparison claims were reworded.**
  - Hock Tan's primary quote is $30bn ARR per GW against about $10bn per year of cost, a 3x ratio (AVGO.md). JPM's relay of $5bn per GW, a 6x ratio, is the outlier.
  - SemiAnalysis's gross-margin path matches the S-1 functional basis for 2024 and 2025 (−95% and 40%). It does **not** reconcile with 1H26 at 85%.
- **The list-price mix fit was dropped.** It cannot identify the model mix.

**Which input drives each result:**
- Gross margin: S-1 only, through the cost allocation and the treatment of channel fees.
- Tokens per month: the Ramp series choice (1.5x), then the consumption-share basis (1.25x), then the June path (±3.5%).
- Cost per Mtok: the Ramp series (1.4x) times the allocation.
