## Double-check verdict: ANTHROPIC (private) — PARTIAL

Audit date: October 26, 2026. Scope: the numerical analysis in `calculate.py` / `calculations.json`, the supplied S-1 HTML, and the model's cited Q3 secondary report. This is a single-document model audit, not an email synthesis, comprehensive investment thesis, or approval to size a position. Historical arithmetic passes. Forward outputs are conditional sensitivities; they are not validated forecasts.

Source checked: `E:/Wiki Felipe empresas/_inbox/20261026_Anthropic_S-1_SEC.htm`, supplied as dated October 26, 2026; SHA-256 `01ceed043cd6ff4f67d9053ec6f8dac703c931b3327e98d6abf2d56fef45dc89`. Line references below refer to `filing-readable.txt` in this folder. I independently checked the indicated financial statements, footnotes and contracts, recalculated the model's core outputs, and spot-checked the raw HTML for revenue, cost of revenue, purchase commitments, uncommenced leases and RSU costs. This does not independently authenticate an EDGAR accession. The June interim statements are unaudited (lines 14724–14728); HARD means an exact input from the supplied document, not audited interim results.

### 1. Outlook email coverage

- Window pulled: not applicable to this assigned single-document numerical audit.
- Broker notes available / referenced / priority senders: not counted. No email-coverage conclusion is made.
- Missing senders or dates: no broker consensus or broker stance claim is approved by this audit.

### 2. SEC filings coverage (last 2 years)

- Document checked: supplied S-1 and its historical statements, quarterly schedules, accounting policies, commitments and subsequent events. No claim that separate 10-Ks or 10-Qs were reviewed.
- Specific inputs and calculations verified:

| Item | Independent check, USD billions unless stated | Source in supplied S-1 |
|---|---|---|
| H1 revenue | 4.731 + 11.555 = 16.286 | Lines 7401–7402, 971 |
| H1 GAAP operating result | −1.667 + 0.974 = −0.693 | Lines 7410, 979 |
| H1 adjusted operating result | −0.617 + 2.235 = 1.618; also −0.693 + 2.185 + 0.126 | Lines 7517–7521 |
| Q2 operating margins | 0.974 / 11.555 = 8.429%; 2.235 / 11.555 = 19.342% adjusted | Lines 7402, 7410, 7521 |
| H1 derived gross margin | (16.286 − 2.380) / 16.286 = 85.386% | Lines 971, 15847 |
| H1 expense classification bridge | 2.380 + 9.741 + 3.808 + 1.050 = 16.979 | Lines 15847–15852; matches natural-expense total at 978 |
| H1 adjusted net income | −80.748 + 72.388 + 8.720 + 2.185 + 0.126 = 2.671 | Lines 986, 14651–14655, 7532–7538 |
| H1 CFO and cash capex | CFO 3.929 − cash PP&E purchases 0.482 = 3.447; less finance principal 0.004 = 3.443 | Lines 14663–14672 |
| Cash-flow movements in operating assets/liabilities | −4.982 + 2.094 + 2.679 − 0.003 + 1.380 = +1.168; CFO before these movements = 2.761 | Lines 14658–14663 |
| Net investment purchases | 18.972 − 2.610 = 16.362, explaining most of 17.181 investing cash use | Lines 14666–14669 |
| June liquid assets | 112.389 cash + 19.262 short-term investments = 131.651; 2.529 restricted cash is separate | Lines 14488–14493, 1036 |
| June disclosed obligation subtotal | 265.6 purchase commitments + 321.4 uncommenced lease obligations = 587.0; adding commenced undiscounted operating 1.601 and finance 0.523 gives 589.124 | Lines 16791–16797, 15722–15734 |
| Revenue mix and RPO | Consumption 13.064 + subscription 3.222 = 16.286; RPO 10.8 × approximately 75% = approximately 8.1 expected over next 12 months | Lines 15329–15355 |

- All six quarterly revenue, compute, GAAP operating and adjusted operating inputs match the quarterly tables, including 2025. Functional expenses for 2024, 2025 and H1 2025 also match the supplied schedules.
- The cash-flow bridge reproduces CFO 3.929. Calling the 1.168 adjustment “working capital” is shorthand: the source includes other operating assets/liabilities, not solely conventional current working capital.
- September financial tables and IPO pro forma fields are incomplete. No completed September financial statements, IPO share count, IPO cash withholding amount, or complete current annual obligation schedule can be manufactured from these blanks.

### 3. Bloomberg API cross-check (REFERENCE ONLY — not gabarito)

- BBG pull run: no. This assignment is a supplied-document model audit of a private company; no listed security or market-consensus claim was supplied for verification.
- Fields pulled: none.
- Reference-data divergences: none adjudicated. The 1.5 trillion and 2.0 trillion equity values are ESTIMATE valuation scenarios, not verified market capitalizations or an IPO price.
- Hard factual errors confirmed via BBG: none; no BBG verification is claimed.
- Sanity checks completed locally: 1,500 / 53.246 = 28.17× and 2,000 / 53.246 = 37.56× equity value / FY2026 scenario revenue. These are not enterprise-value multiples. Financing instruments and conversion/share-count blanks prevent an exact IPO EV or dilution bridge.

### 4. Transcript coverage

- Quarterly / investor-day transcripts: not part of the single-document assignment; none represented as read.
- Q3 external input: independently reproduced an indexed Reuters Breakingviews excerpt reporting 16.8 billion revenue for the three months to September, attributed to people familiar with the October 14 investor presentation. Author Karen Kwok; published October 15, updated October 16, 2026. The supplied S-1's populated statements do not provide this figure. Keep it PARTIAL and visibly separate from filing data. [Original report](https://www.breakingviews.com/40925ca4af2b/columns/breaking-view/anthropics-2-trln-dream-faces-deflation-trap-2026-10-15/).
- The directly opened page displayed a shorter excerpt with 45% growth; an independent targeted search returned the exact 16.8 number. `web-evidence.txt` preserves the prior analyst's indexed excerpt. Do not claim complete article access or company confirmation.
- Headcount/productivity check: approximately 5,300 employees and TTM revenue per employee above 6.6 million appear together at lines 9653–9654. The computation 5,300 × 6.6 million − Q4 2025 revenue 2.040 billion − H1 2026 revenue 16.286 billion gives approximately 16.654 billion. It is a rounded scale check using the same company's disclosures, not a strict bound or independent audited validation of Q3.

### 5. Unsourced or weakly-sourced claims in prior work

1. **Forward noncompute expense ratio: material uncertainty.** Q2 adjusted noncompute expense is correctly derived as 10.581 − 5.558 − 1.261 = 3.762, or 32.557% of revenue. Holding that ratio constant is an ESTIMATE. Q1's actual adjusted noncompute expense was 6.398 − 3.387 − 0.924 − 0.126 = 1.961, or 41.450% of revenue. The Q2 calibration predicts only 1.540 for Q1: 21.454% below actual, equivalent to an 8.893 percentage-point error in operating margin. A boolean “within 25%” is not evidence of forecast precision. The holdout should be AMBER, with the margin error displayed.

   | Compute / revenue assumption | Adjusted margin using Q2 noncompute ratio 32.557% | Using Q1 noncompute ratio 41.450% |
   |---|---|---|
   | 50% | 17.44% | 8.55% |
   | 60% | 7.44% | −1.45% |
   | 70% | −2.56% | −11.45% |

   Both forward uses of historical ratios are ESTIMATE sensitivities. The loss/profit sign changes at the 60% compute assumption. Show this; a compute-only sensitivity understates model uncertainty. A 1 percentage-point increase in either cost ratio reduces adjusted margin by 1 percentage point, holding the other ratio constant.

2. **85.386% derived gross margin is not a full economic margin or an inference-efficiency measure.** Revenue through CSP marketplaces is recognized gross because Anthropic is principal (15058–15064), while channel partner costs are in sales/marketing (15086–15088; 15858–15860). CSP marketplace revenue was approximately 48% of H1 revenue (14808–14815). Functional S&M was 3.808, versus natural sales/marketing/partnerships of 3.168; do not interchange those categories or double-count them. Subtracting all functional S&M as well as cost of revenue produces 62.004%, but this is an illustrative ratio, not a disclosed net-revenue margin or pure channel-adjusted gross margin. Total compute 8.945 also includes research and internal usage (15070–15078); revenue / total compute is an aggregate expense-efficiency ratio, not token unit economics.

3. **Historical positive cash generation does not validate forward cash generation.** CFO less cash capex is correctly calculated, but H1 also includes 0.445 of finance-lease assets obtained noncash and 0.148 increase in PP&E acquired but unpaid (15827, 15836). Finance principal is only 0.004 for this historical period. The upcoming lease ramp can make CFO-minus-cash-capex diverge sharply from infrastructure investment and future payments. Do not deduct noncash additions from cash flow without labeling a separate investment measure. No numerical annual cash runway or 2027 FCF is justified by the blank obligation schedule. H1 adjusted net income also includes 1.111 interest income (980), so it should not stand in for operating profit.

4. **IPO-related compensation remains an essential omission unless presented prominently.** The supplied source says June cumulative RSU expense would have been 2.9 if the performance condition had been probable, with 23.7 additional unrecognized RSU cost over a weighted-average 2.1 years (16478–16486). The 23.7 / 2.1 = 11.286 annual equivalent is arithmetic, not a straight-line accounting forecast or a cash expense forecast. It excludes future grants and is not the entire compensation backlog: unrecognized options were another 2.8 over 1.2 years (16452–16454), plus 0.325 of RSAs over 2.7 years (16518–16519). IPO tax withholding/remittance is a real use of cash with the amount blank (6089–6096). June's 2.9 is not an exact eventual IPO catch-up charge; additional service, awards and forfeitures can change it.

5. **Commitment stock must remain separated from spending flow.** The 589.124 June subtotal combines disclosed multi-year, undiscounted categories, including conditional uncommenced obligations; it is not annual compute expense, total balance-sheet liabilities, or a fully current noncancelable cash floor. Subsequent new and amended agreements disclose approximately 245 long-term and 21 short-term (17153–17160), not a reconciled rollforward. Named counterparties overlap aggregate disclosure; do not add their face values again. Variable/unfixed agreements are excluded from the June purchase aggregate (16793–16797). The absence of a current total is substantive, not a formatting problem.

6. **Contract optionality matters.** SpaceXAI's 3.1 per month × 12 = 37.2 is a full-capacity annualized payment scale. It is not a guaranteed 2027 expense: delivery is expected in December, ramp fees differ, initial noncancelable periods end in January/March 2027, and agreements can then be cancelled on 90 days' notice (8008–8015). Nscale requires financing efforts and delivery/acceptance (8026–8035); a substantial Lambda tranche is conditional on a facility lease (8036–8044). Broadcom's 161.2 is stated excluding interest, unlike some undiscounted lease-payment aggregates (8046–8064). Google additional compute estimates of 125–150 and AMD expenditures above 20 are outside the table and conditional (7996–8000, 8016–8025). Preserve these bases rather than creating an apparently exact grand total.

7. **Forward revenue and valuation precision is conditional.** With PARTIAL Q3 revenue 16.8, ESTIMATE Q4 growth of −10% / 0% / +20% / +40% gives FY revenue 48.206 / 49.886 / 53.246 / 56.606. Arithmetic passes. These scenarios have no demonstrated probabilities. Calling +20% a “mid” case should not suggest a statistically estimated base case. Quarter × 4 is not the filing's Run-Rate Revenue, defined as trailing-28-day consumption × 13 plus current monthly subscriptions × 12 (290–294); the model correctly warns about this distinction. The sampled growth range does not cap possible downside.

8. **Bartz still has cash consequences.** The 1.5 settlement was charged in 2025, but 1.2 remained a current liability at June 30 after the earlier 0.3 payment (16816–16820). Excluding the historical charge from adjusted earnings does not erase the remaining cash obligation. This belongs beside the cash-flow discussion, without inventing its payment schedule.

9. **Tags need to distinguish inputs from outputs.** `input_tag: HARD` appears at whole-record level on quarterly and functional records that also contain derived margins and growth. Render each sourced input as HARD and each calculation as DERIVED; show forward output dependence on PARTIAL/ESTIMATE prominently. Do not let a row-level HARD label imply a computed output was reported verbatim.

### 6. What the prior analyst MUST do before this work ships

- Keep the historical calculation bridge and source line references; they passed.
- Show both Q1 and Q2 noncompute-ratio sensitivities, display the 8.89 percentage-point holdout margin miss, and mark forecast validation AMBER/unavailable.
- Make gross revenue / channel cost classification, finance-lease investment and the RSU catch-up/backlog visible beside the attractive gross margin, adjusted margin and cash-flow numbers.
- Keep Q3 as PARTIAL secondary reporting, all growth/valuation assumptions as ESTIMATE, and annualized quarterly revenue separate from the defined Run-Rate metric.
- Label the June obligation subtotal by date and basis; retain cancellation/delivery terms. Do not construct a current grand total or annual runway without a reconciled schedule.
- Label the June RSU annual equivalent as a scale sensitivity only; include the unquantified IPO withholding cash requirement and unpaid Bartz liability.

### 7. Bottom line

The historical source work and arithmetic withstand checking. The forward margin conclusion does not have the same evidentiary strength: using another observed quarter's noncompute ratio can flip an apparently profitable scenario into a loss. PARTIAL is the appropriate verdict until those sensitivities and the cash/compensation caveats are made prominent; no precise earnings or cash-flow forecast is approved.
