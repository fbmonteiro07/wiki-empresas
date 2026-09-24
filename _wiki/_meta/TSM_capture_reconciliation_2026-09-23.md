# TSMC capture: reconstruction of the user-pasted table

Prepared 2026-09-23. Exhibit source, vintage, column dates, product scope and accounting basis are unconfirmed. This note does not attribute the exhibit or change a company forecast.

**Result: all 30 displayed percentages can be reproduced at one-decimal precision. Economic validation remains partial.** The fit does not identify a unique original formula.

## Equation and fitted assumptions

For the same product, cost scope and recognition period:

`TSMC revenue / customer product revenue = (TSMC content / product COGS) × (1 − product gross margin)`

The reconstruction adds a substantive assumption: the first factor is identical across all customers within each column.

| Input | Value | Grounding |
|---|---|---|
| User exhibit | Six rows, five columns | ANCHOR: transcribed values, not verified actuals |
| Nvidia product gross margin | 80% | PARTIAL: unnamed expert illustration, Capstone notes, 2026-09-09 |
| Broadcom product gross margin | 60% | PARTIAL: same expert illustration, not corporate margin |
| AMD / Marvell product gross margin | 60% | ESTIMATE: selected to fit their identical rows |
| MediaTek / Alchip product gross margin | 15% | ESTIMATE: inferred conditional on shared cost share and the margin normalization |
| TSMC share of COGS | 25.8%, 22.1%, 23.1%, 23.5%, 23.5% | ESTIMATE: inverse-fitted representative points within rounding intervals |

The shared factors are calibrated to the pasted table, not to independently observed invoices. There is no independent validation of their absolute levels.

| Reconstructed capture | Column 1 | Column 2 | Column 3 | Column 4 | Column 5 |
|---|---:|---:|---:|---:|---:|
| NVDA | 5.2% | 4.4% | 4.6% | 4.7% | 4.7% |
| AVGO / AMD / MRVL | 10.3% | 8.8% | 9.2% | 9.4% | 9.4% |
| MediaTek / Alchip | 21.9% | 18.8% | 19.6% | 20.0% | 20.0% |

## Worked calculation

At the final-column cost share of 23.5%:

- NVDA: `(1 − 80%) × 23.5% = 4.7%`.
- AVGO / AMD / MRVL: `(1 − 60%) × 23.5% = 9.4%`.
- MediaTek / Alchip: `(1 − 15%) × 23.5% = 19.975%`, displayed as `20.0%`.

These are gross margins. Using operating margins in this identity would be incorrect because operating expenses are not product COGS.

In an illustrative same-cost comparison, $100 of manufacturing cost and $23.50 of TSMC content imply customer selling prices of $500, $250 and approximately $117.65 for the three margin groups. TSMC gets the same $23.50 in each case; its larger capture percentage reflects a smaller customer-revenue denominator. A shift toward a lower-margin designer does not mechanically increase TSMC dollars per otherwise identical chip.

## Evidence and uncertainty

The [September 9 expert transcript](../../_equity_calls/Semis/2026-09-09_expert_NVDA-AI-chip-gross-margin-compression-in-house-design.md) explicitly illustrates the move from 80% to 60% gross margins. An earlier reference to Broadcom at 16% is inconsistent with the same speaker's arithmetic and subsequent explicit 60% statement. It is not adopted. These are approximate product illustrations, not company-reported consolidated margins.

MediaTek's 15% fitted margin is especially uncertain. In the [Fubon/Sherman Shang discussion hosted by Jefferies, August 3, 2026](../../relat%C3%B3rios%20bons/2026_08_03_sherman_update_03_08_26.html), the questioner cites heard estimates of 30–40% for TPU v8; Sherman speculates that v9 could achieve 50% or more, while explicitly saying he lacks the actual figure. This is an independent challenge to assuming 15% universally, not a like-for-like disproof: program generation, HBM accounting and original exhibit date are unknown.

Alchip's [official business-model description](https://www.alchip.com/en/Business_Models/model), undated and accessed 2026-09-23, describes several design, packaging and production hand-off models. It provides no numerical basis for assuming Alchip and MediaTek have identical margins or identical TSMC content shares.

Before using these rates to forecast revenue, confirm wafer-only versus wafer-plus-packaging content, HBM treatment, chip versus board/rack scope, and relevant product revenue versus consolidated company revenue. Procurement and recognized sales can fall in different periods.

## Sensitivity and guardrails

Holding the final-column TSMC/COGS share fixed at 23.5%:

| Scenario assumption | Recomputed capture |
|---|---:|
| NVDA gross margin 75% | 5.875%, or 5.9% displayed |
| Mid-group gross margin 50% | 11.75%, or 11.8% displayed |
| MediaTek gross margin 30% | 16.45%, or 16.5% displayed |
| MediaTek gross margin 40% | 14.1% |
| MediaTek gross margin 50% | 11.75%, or 11.8% displayed |

A 10% relative change in the assumed TSMC/COGS factor changes every capture rate by 10% relative, holding margins fixed. Both margins and the shared factor are load-bearing assumptions.

- Arithmetic: PASS, every displayed cell matches using decimal half-up rounding.
- Physical bounds: PASS within the proposed model; all cost shares and margins are between zero and one. This is not independent validation.
- Identification: PARTIAL. For example, margin groups of 78% / 56% / 6.5%, or 82% / 64% / 23.5%, with rescaled common factors, also reproduce the same table.
- Independent invoice-cost anchor: absent. Absolute economic capture rates remain unvalidated.
- Timing/flow checks: unavailable until the column dates and product definitions are established. No stock/flow inference is made.

Independent double-check completed 2026-09-23: arithmetic PASS; economic validation PARTIAL. The reviewer independently verified the stored input cells, rounding, alternative parameter families, sensitivities, and the two quoted archive transcripts. Valid findings were incorporated: explicit cost-share sensitivity, non-uniqueness, unchanged TSMC dollars in the same-cost example, and matched accounting/timing requirements. This was a bounded model audit, not a full filings or mailbox coverage audit.

Reproducible arithmetic: [model.py](../_data/tsm_capture_reconciliation_20260923/model.py). Full calculations: [results.json](../_data/tsm_capture_reconciliation_20260923/results.json). Provenance: [sources.md](../_data/tsm_capture_reconciliation_20260923/sources.md).
