## Double-check verdict: GSXUSWCH / GSCBSWC2 / PLNT — PASS (bounded numerical audit)

The observed-liquidity calculations and explicitly hypothetical USD100m allocations pass. Actual Goldman basket order flow and causal PLNT price impact remain unavailable. This is not approval of an investment thesis or a price-impact estimate.

Scope: independently inspect the raw Bloomberg captures, recompute all twenty top-ten basket rows and both PLNT scenario rows, check all 55 constituent liquidity denominators, and inspect `Basket_ADTV_and_PLNT.md` for causal or unit errors. The calculations were reproduced with a separate standard-library Python calculation, without importing `adtv_analysis.py`.

### 1. Outlook email coverage

Not applicable to this bounded Bloomberg arithmetic audit. No claim about broker research coverage or actual client basket orders was tested or approved.

### 2. SEC filings coverage (last 2 years)

Not applicable. The work tests market-data arithmetic and conditional allocations, not company fundamentals.

### 3. Bloomberg API cross-check (REFERENCE ONLY — not gabarito)

- Raw source captures independently inspected: `../reference.json` (2026-09-23 08:57:22 -03:00), `../metadata.json` (08:57:34), `../constituents_primary.json` (08:59:17), `constituents_history.json` (09:07:16), and `constituents_reference.json` (09:07:21). These were existing Bloomberg Desktop API captures; the skeptic did not represent a fresh HTTP-wrapper pull as having occurred.
- Fields verified: `INDX_MWEIGHT`, `PX_LAST`, `PX_VOLUME`, `TURNOVER`, `CRNCY`, and relevant update dates. Bloomberg's `TURNOVER` definition in `../metadata.json:202` differentiates equity traded value from index traded value scaled by 1,000.
- Recomputed from raw constituent primary-listing rows: GSXUSWCH volume **154,013,798** = index volume **154,013,798**; GSCBSWC2 volume **87,192,431** = index volume **87,192,431**. All constituent snapshot update dates used in these reconciliations are September 22. This supports the constituent-volume interpretation; it does not identify orders in the baskets.
- Weight sums: GSXUSWCH **100.000003%**, GSCBSWC2 **99.999998%**. Top-ten ordering and PLNT's ranks (16 and 12 respectively) match the raw weights.
- All 55 US-composite constituents have twenty complete, positive-volume and positive-turnover observations from **August 24 through September 21**, with no missing or duplicate dates in the selected baseline. September 22 is excluded. USD currency checks passed.
- All twenty top-ten scenario allocations and both PLNT allocations match the independently recomputed raw-input calculations; no numerical discrepancies. All 55 dollar ADTV and share ADV denominators also match.
- Unit sanity check: for every constituent, September 22 turnover divided by volume is within 10% of the independently returned close. This catches gross scale mistakes, not market-data truth or causality.

PLNT input evidence: raw weights at `../reference.json:193` and `:369`; raw daily history begins at `constituents_history.json:7134`. Bloomberg historical September 22 close is **$42.60**, previous close **$47.05**, volume **7,466,189 shares**, and turnover **$320,508,600**.

| Independently reproduced PLNT item | Result |
|---|---:|
| Close-to-close return | -9.46% |
| Prior twenty-session dollar ADTV | $91,372,829.50 |
| Prior twenty-session share ADV | 1,798,864.05 |
| Observed September 22 turnover / dollar ADTV | 350.7701% |
| Observed September 22 shares / share ADV | 415.0502% |
| GSXUSWCH hypothetical $100m allocation | $2,609,978 |
| GSXUSWCH hypothetical allocation / dollar ADTV | 2.8564% |
| GSCBSWC2 hypothetical $100m allocation | $4,714,943 |
| GSCBSWC2 hypothetical allocation / dollar ADTV | 5.1601% |
| GSXUSWCH hypothetical basket notional for 10% PLNT dollar ADTV | $350,090,420 |
| GSCBSWC2 hypothetical basket notional for 10% PLNT dollar ADTV | $193,794,134 |

Hard factual or arithmetic errors: none found in the audited report. The 10% ADTV level is an illustrative threshold, not an empirically established price-impact threshold.

### 4. Transcript coverage

Not applicable. No management statements or company thesis were evaluated.

### 5. Unsourced or weakly-sourced claims in prior work

- **Unobserved:** actual client basket notional, direction, execution schedule, dealer cash hedges and netting. Consequently actual basket-related participation in PLNT and its causal price impact cannot be computed.
- **Assumptions, not observations:** USD100m notional, 100% execution in cash equities and use of the September 23 snapshot weights for the illustrative allocation. The reviewed report explicitly labels all three as scenario assumptions. Raw weights are HARD only as a dated snapshot; they are not verified September 22 execution weights.
- The observed PLNT turnover and share-volume ratios include all trading. They are not basket flows, net selling or percentages of the price decline.
- The external NYSE citation was opened and checked: [Choey Li, October 17, 2023](https://www.nyse.com/data-insights/closing-auction-immediate-market-impact-price-drift-and-transaction-cost-of-trading-part-2) supports the qualitative relevance of volatility, spread, participation, order size and timing. It does not calibrate this PLNT scenario.

### 6. What the prior analyst MUST do before this work ships

- Preserve the report's explicit distinction between observed constituent trading and hypothetical basket cash execution. The report reviewed meets this requirement.
- Preserve the prior-session denominator, dollar-versus-share distinction, snapshot date and scenario assumption labels. The report reviewed meets these requirements.
- Do not claim that a basket order caused, should have caused, or explains any quantified part of PLNT's price decline. No such conclusion is supported.
- If actual order data arrives, replace the scenario normalization with the documented notional, signed direction, execution-time weights and cash executions. An impact estimate would require additional observed execution conditions and a separately validated impact model.

Sensitivity is exactly proportional for this accounting identity: doubling notional or the cash-executed fraction doubles dollar allocation and its percentage of ADTV, holding weights and the denominator fixed. There is no fitted impact constant to calibrate and no justification for converting ADTV percentage into a price-move percentage.

### 7. Bottom line

The numerical work passes and the report makes the necessary limitations explicit. The decisive missing input is actual signed basket cash execution; without it, a claim that these baskets explain PLNT's decline would fail regardless of the precision of the ADTV calculations.
