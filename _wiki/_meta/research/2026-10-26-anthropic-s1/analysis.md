# Anthropic S-1: the numbers and their forward implications

Research date: **October 26, 2026**. Source: the user-supplied **Anthropic, PBC S-1 dated October 26, 2026**, [original HTML](../../../../ANTHROPIC/ANTHROPIC_S-1_2026-10-26_0001628280-26-067168.html) _(link repointed 2026-10-26 by /run-inbox when the inbox copy was archived; accession 0001628280-26-067168 has since been verified on EDGAR)_. References below give printed prospectus pages and lines in [the readable extraction](filing-readable.txt). The attachment contains complete historical financial tables through June 2026, selected September operating metrics, and numerous blank September/IPO fields. An independently retrieved SEC accession URL was not established. This analysis describes the supplied document, without filling its blanks from press reports.

**My conclusion:** the document establishes a business that reached operating profitability in Q2, with unusually strong customer-serving economics, while committing to a much larger and more capital-intensive infrastructure model. The key underwriting question is how fast revenue can absorb the next wave of compute and equity compensation. Neither the headline net loss nor the reconstructed gross margin answers that question alone.

**Grounding labels:** **HARD** = explicitly disclosed in the supplied document, including unaudited figures; it does not mean audited or independently authenticated. **PARTIAL** = externally reported, rounded, or incomplete evidence. **DERIVED** = arithmetic on stated inputs. **ESTIMATE** = an explicit sensitivity assumption, not management guidance. Unless marked otherwise, dollar figures are USD billions. All S-1 attribution below is to Anthropic, October 26, 2026.

**1. The operating inflection is already visible in Q2.**

| HARD disclosed figures | FY2024 | FY2025 | H1 2025 | H1 2026 |
|---|---:|---:|---:|---:|
| Revenue | 0.386 | 4.585 | 1.163 | 16.286 |
| Compute and infrastructure | 2.522 | 7.326 | 2.334 | 8.945 |
| Personnel | 0.454 | 1.839 | 0.538 | 3.152 |
| Sales, marketing and partnerships, by nature | 0.043 | 0.568 | 0.120 | 3.168 |
| Other operating and administrative | 0.347 | 1.412 | 0.306 | 1.714 |
| Bartz settlement | — | 1.500 | — | — |
| GAAP operating income/(loss) | (2.980) | (8.060) | (2.135) | (0.693) |
| GAAP net income/(loss) | (8.309) | (41.965) | (12.969) | (80.748) |

Source: S-1 p.23, extraction lines 969–996. H1 2026 revenue growth is **1,300.3% DERIVED**, or **14.0 times** H1 2025: 16.286 / 1.163 − 1. Compare half-years with half-years, rather than H1 with the previous full year.

| Period | Revenue HARD | Sequential growth DERIVED | GAAP operating income HARD | Adjusted operating income HARD | Adjusted margin DERIVED |
|---|---:|---:|---:|---:|---:|
| Q1 2025 | 0.376 | — | (0.935) | (0.830) | (220.7%) |
| Q2 2025 | 0.787 | 109.3% | (1.200) | (1.019) | (129.5%) |
| Q3 2025 | 1.382 | 75.6% | (3.089) | (1.284) | (92.9%) |
| Q4 2025 | 2.040 | 47.6% | (2.836) | (1.721) | (84.4%) |
| Q1 2026 | 4.731 | 131.9% | (1.667) | (0.617) | (13.0%) |
| Q2 2026 | 11.555 | 144.2% | 0.974 | 2.235 | 19.3% |

Source: S-1 pp.158–161, lines 7401–7417 and 7516–7524. Q2 GAAP operating margin was **8.4% DERIVED**. The adjusted bridge is transparent: 0.974 + 1.261 of stock compensation = 2.235. The positive Q2 result is supported by the supplied statement; it does not establish a permanent margin floor.

Revenue per dollar of **total compute expense** rose from **$0.69 in Q4 2025** to **$1.40 in Q1 2026** and **$2.08 in Q2 2026**, DERIVED from the quarterly tables. This is realized revenue divided by total compute expense, including research and internal usage. It is neither inference gross margin nor revenue per GW, and it does not identify a token price or compute utilization rate.

**2. The hidden gross-margin table is favorable, but the full expense bridge matters more.**

The main statement presents expenses by nature. Note 8 also discloses them by function, allowing reconstruction of gross profit. The company recast earlier periods to the same presentation; the presentation change did not change operating loss. Source: S-1 Note 1, lines 14708–14723; Note 8, p.F-40, lines 15842–15862.

| Functional economics | FY2025 | H1 2025 | H1 2026 |
|---|---:|---:|---:|
| Revenue HARD | 4.585 | 1.163 | 16.286 |
| Cost of revenue HARD | 2.773 | 1.019 | 2.380 |
| Gross profit DERIVED | 1.812 | 0.144 | 13.906 |
| Gross margin DERIVED | 39.5% | 12.4% | **85.4%** |
| Research and development HARD | 6.338 | 1.850 | 9.741 |
| Sales and marketing, by function HARD | 0.911 | 0.239 | 3.808 |
| General and administrative HARD | 1.123 | 0.190 | 1.050 |

The H1 2026 calculation is (16.286 − 2.380) / 16.286 = **85.4%**. This is reconstructed from the GAAP expense footnote; it is not the externally reported Q3 adjusted gross margin.

Cost of revenue principally contains customer-serving compute, plus some personnel and overhead. Research compute and internal usage sit mainly in R&D. Channel partner fees sit in sales and marketing. Consequently, subtracting all compute from revenue would misstate gross margin, while treating 85.4% as a fully loaded operating spread would also mislead.

The complete H1 functional bridge is:

**85.4% gross margin − 23.4% functional sales and marketing − 59.8% R&D − 6.4% G&A = −4.3% GAAP operating margin**, all DERIVED from the table. Revenue less cost of revenue and all functional sales and marketing leaves **62.0%**, an analytical subtotal, not a company-defined margin or a pure channel-adjusted gross margin.

**3. Revenue quality: broadening customers, but substantial usage and channel exposure.**

| Metric | S-1 disclosure / calculation | Interpretation |
|---|---|---|
| H1 2026 consumption revenue | **13.064 HARD; 80.2% DERIVED** | Usage sensitivity dominates the business. |
| H1 2026 subscription revenue | **3.222 HARD; 19.8% DERIVED** | Subscription revenue is not the same as enterprise revenue. |
| H1 2026 international revenue | **4.523 HARD; 27.8% DERIVED** | Geography is based on billing address. |
| CSP marketplace share | **48% HARD**, H1 2026; 47% FY2025 | Distribution partners remain economically important. |
| Customers above $100k TTM revenue | **>11,900 HARD**, September 2026; >950 September 2025 | An expanding cohort, not a count of all paying enterprises. |
| Customers above $1m / $10m TTM revenue | **>1,900 / approximately 250 HARD**, September 2026 | Threshold groups are nested and must not be added. |
| Net revenue retention | **Approximately 900% HARD**, September 2026 | Same qualified cohort's quarterly revenue versus its year-earlier quarter; excludes Claude Pro and Max subscribers. |
| Top-five concentration | **Approximately 21% DERIVED for Q3**, from 79% outside the top five; approximately 36% in Q1 | Concentration declined as the customer base broadened. |
| Largest customer | No single customer above **10% HARD of nine-month 2026 revenue** | This is not a Q3-only concentration statement. |
| Policy-violating customers | Company estimate **5–7% of nine-month 2026 revenue HARD as a disclosed estimate** | Potential revenue attrition as enforcement tightens; not automatically fraud, fake revenue, or a restatement. |

Sources: S-1 definitions pp.3–4, lines 251–259; adoption pp.135–136, lines 6411–6426; customer discussion pp.143–144, lines 6745–6796; revenue risk p.146, lines 6873–6884; Note 1 lines 14808–14815 and 15058–15064; Note 2 p.F-27, lines 15320–15335.

Anthropic explicitly recognizes CSP marketplace sales **gross**, as principal; the CSP acts as collection agent. That resolves the accounting basis of the reported financial statements. It does not prove that the wiki's earlier $65bn and >$70bn press run-rate figures used identical definitions.

The S-1 defines **Run-Rate Revenue = trailing 28-day consumption fees × 13 + current monthly subscription fees × 12**. It is not annual contract value, an annual forecast, or an annualization of the busiest hour. The actual September run-rate dollar field is blank. Source: definitions, lines 290–294 in the readable extraction; see also the original extraction lines 398–402.

Two reasons to avoid projecting the 900% retention metric mechanically: the prior-year cohort began from a much smaller base, and the filing reports that models released in the preceding six months generated **over 80% of Q3 revenue HARD**. Continued growth requires repeated successful model releases. It also discloses a roughly **20% two-week holiday spending decline HARD** around year-end 2025; that is a short-period seasonality observation, not a forecast of a 20% quarterly decline.

**4. The $80.75bn net loss is mostly valuation accounting; positive cash flow still needs qualification.**

The H1 net-loss-to-adjusted-income reconciliation is:

| Bridge | Amount |
|---|---:|
| GAAP net loss HARD | (80.748) |
| Add back convertible/derivative/SAFE fair-value changes HARD | 72.388 |
| Add back other specified mark-to-market financial instruments HARD | 8.720 |
| Add back stock compensation HARD | 2.185 |
| Add back noncash charitable contributions HARD | 0.126 |
| Adjusted net income, reconciled | **2.671** |

Source: S-1 non-GAAP reconciliations, corroborated by Q1+Q2 at lines 7531–7538. Adjusted operating income was **1.618 HARD**; adjusted net income also benefits from interest income. Financing revaluations are largely noncash but reflect real equity claims and dilution. They should not be described as an $80.75bn operating cash burn, or dismissed as having no shareholder consequence.

| H1 2026 cash bridge | Amount |
|---|---:|
| Operating cash flow HARD | 3.929 |
| Less cash purchases of PP&E HARD | (0.482) |
| CFO less cash capex DERIVED | **3.447** |
| Less finance-lease principal HARD | (0.004) |
| After that additional principal payment DERIVED | **3.443** |

Source: S-1 cash-flow statement p.F-13, lines 14643–14680. These are explicitly defined analytical free-cash-flow measures, not a company-defined FCF metric. They do not subtract all noncash lease additions or yet-to-commence commitments. H1 also included **445m HARD of finance-lease assets acquired noncash** and **148m HARD of increased unpaid PP&E purchases** (Note 8, lines 15827 and 15836). These explain why cash capex understates infrastructure investment. The **1.2bn HARD unpaid Bartz settlement liability at June** is another future cash claim, despite the expense being adjusted out of prior-period earnings (Note 13, lines 16816–16820).

Working capital provided a net **1.168 DERIVED**: receivables used 4.982, prepaid/other assets released 2.094, payables/accruals provided 2.679, deferred revenue provided 1.380, and lease liabilities used 0.003. CFO before those movements was therefore **2.761 DERIVED**. Positive cash conversion is real for H1, but it received working-capital support.

Investing outflow of **17.181 HARD** is not all infrastructure spending: **16.362 DERIVED** was net purchases of short-term investments. The remaining **0.819 DERIVED** comprises cash capex and other investing activities. Similarly, the June liquidity stock was created predominantly through financing: H1 net financing inflow was **110.774 HARD**.

**5. The balance sheet has liquidity; future infrastructure payments remain the critical gap.**

At June 30, 2026: cash **112.389 HARD** plus short-term investments **19.262 HARD** = **131.651 DERIVED**, with **2.529 HARD restricted cash separately**. Convertible notes carried at **108.566 HARD** are fair-value accounting liabilities, not a simple cash debt balance to subtract from liquidity. September cash and pro forma post-IPO balances are blank. Sources: p.F-6, lines 14480–14510; p.24–25, lines 1033–1042.

The revolver increased to **15bn HARD in September**, matures in September 2031, and has a **5bn minimum-liquidity covenant HARD**. The full 15bn is facility size, not evidence of October undrawn availability or unrestricted incremental cash; letters of credit can use it. Source: pp.163–164, lines 7626–7662; Note 17 p.F-65, lines 17113–17116.

The S-1 lists conditional financing capacity, as of June: **Amazon 15bn**, **Google 20bn**, and **Broadcom 42bn HARD**. These amounts are subject to milestones and conditions, and Broadcom's facility finances specified lease payments. They cannot be counted as cash already on hand. The Broadcom notes carry **9% PIK**, conversion at **90% of trailing VWAP**, with **13% / 85%** terms when specified revenue conditions are not met. Sources: pp.166–168, lines 7770–7858. Supplier financing provides flexibility but also creates contingent dilution and can become less available in a slowdown.

**6. Compute: retain contract dates, cancellation rights, and different dollar bases.**

| Counterparty / structure | HARD amount disclosed in the S-1 | Timing and qualification |
|---|---:|---|
| Microsoft | At least **44.9** | Nov.2026–May2033; November 2025 agreement amended February and October 2026. Usage-independent minimum, with specified breach/undelivered-tranche exceptions. |
| Google | At least **114.5** | Apr.2026–Jul.2033; March agreement amended May–August. True-up if spend falls short, subject to adjustments/exceptions. |
| Additional TPU procurement | Estimated **125–150** | Capacity delivered 2028–2031; deployment/pricing conditions; outside the fixed commitments table. A disclosed company estimate, not a fixed minimum. |
| Amazon | At least **110.0** | May2026–Apr2036; usage-independent minimum with specified exceptions. |
| SpaceXAI | Up to **120.5** | Terms into 2029; **3.1/month** once all capacity is delivered, expected December 2026. Cancellation on 90 days' notice after initial periods ending January/March 2027. |
| Nscale | Up to **44.6** | Terms into 2033; fees begin with delivery and acceptance; qualifying financing and performance conditions remain relevant. |
| Lambda | Approximately **41.3** | May, June and August agreements, terms into 2034. August component approximately **34.9**; termination right if facility lease not timely secured. |
| Broadcom equipment leases | Approximately **161.2 excluding interest** | Five-year finance leases; payment generally starts at readiness, but can start earlier with facility delays. Includes the 2026 lease discussed separately at **125.2**. |
| AMD initial tranche | Expected **>20** if fully procured | 2027 capacity, no fixed dollar commitment; excluded from fixed commitments table. Potential additional capacity is not an extra booked minimum. |

Source: S-1 pp.171–173, lines 7985–8066; 2026 Broadcom lease subset at lines 3587–3607. These are whole-contract, minimum, estimated, or upper-bound amounts as explicitly labeled. They are not comparable annual cash expenses. Do not sum this table into a supposedly non-cancelable backlog, or add it to the financial-note aggregates.

The **SpaceX 3.1/month × 12 = 37.2bn DERIVED annualized full-delivery payment cadence** illustrates the step-up in procurement. It is not guaranteed 2027 spend: delivery is prospective, fees vary during the ramp, and termination rights matter.

The financial notes independently disclose June **265.6bn fixed/minimum purchase commitments HARD** and **321.4bn uncommenced lease obligations HARD**, a **587.0bn DERIVED subtotal**. Adding **1.601bn operating** and **0.523bn finance** commenced undiscounted lease payments gives **589.124bn DERIVED of identified June categories**, subject to the disclosed contractual conditions. Sources: Note 7 p.F-37 lines 15712–15734; Note 13 p.F-59 lines 16776–16797.

Note 17 then discloses post-June new/amended agreements with **approximately 245bn future minimum payments** and **approximately 21bn short-term minimum non-cancelable payments HARD**. Those disclosures are not a complete roll-forward: existing obligations were consumed, some agreements were amended, and the September maturity table is blank. **Do not call 589 + 245 + 21 the current commitment balance.** Likewise, the older 518bn press aggregate and the 180bn through-2029 investor spending figure have different dates and bases. Sources: pp.F-65–F-66, lines 17147–17160; older vintages preserved in the wiki.

Revenue backlog does not match that infrastructure duration. June remaining performance obligations were **10.8bn HARD**, with approximately **75% HARD expected to convert within 12 months**, or **8.1bn DERIVED**. This excludes future uncommitted usage and is not a revenue ceiling. It nevertheless shows why supplier obligations cannot be treated as already matched by equally durable customer contracts. Source: Note 2 p.F-27, lines 15349–15355.

Management explicitly says the shift to dedicated infrastructure will raise capex and cause significant net cash use even if financial performance improves. It also warns that short-term compute purchases and newly delivered long-term capacity can compress margins. Sources: pp.134–138 and 162–163, lines 6377–6396, 6491–6519, 7580–7625. A reliable 2027 cash-flow forecast needs the missing payment schedule, opening liquidity, deployment timing and lease/capex split.

**7. Equity compensation is a material post-IPO bridge.**

H1 recognized stock compensation was **2.185 HARD**, versus personnel expense of **3.152 HARD**. Yet the June RSUs had not met their performance condition, so their expense had not been recognized. The company says satisfaction of that condition as of June would have resulted in **2.9bn cumulative expense HARD**, plus **23.7bn unrecognized service-period compensation HARD** over a weighted-average **2.1 years HARD**. Separately, unrecognized options cost was **2.8bn HARD over 1.2 years**, and subsequent RSU grants carried **5.8bn grant-date fair value HARD**. Sources: Note 10 pp.F-52–F-53, lines 16453–16486; Note 17, lines 17105–17112.

The ratio 23.7 / 2.1 = **11.3bn annual equivalent DERIVED** is a scale illustration only. It is not an expense forecast: vesting patterns, new grants, forfeitures, modifications and IPO timing change recognition. The final IPO catch-up and associated tax-withholding cash requirements cannot be determined from the blank pro forma fields. Adjusted margins will exclude much of this economic compensation cost.

There is also a **2.0bn HARD Q3 donation-matching charge**, settled with shares in October, disclosed in subsequent events; therefore do not infer Q3 GAAP profitability from reported adjusted profitability. The separate public-benefit framework initially earmarks shares equivalent to **5%** of the specified June fully diluted base and allows discretionary additional **2%** contributions at successive **50%** share-price milestones. Shares retained within the wholly owned fund are not yet ordinary externally outstanding stock for accounting; subsequent transfers can affect shareholders. Source: pp.144–145, lines 6805–6831; Note 17, lines 17126–17145.

**8. Forward revenue: a conditional bridge, not a manufactured company forecast.**

**PARTIAL external evidence:** Reuters Breakingviews / Karen Kwok, October 15, updated October 16, reports Q3 revenue of **16.8bn** from people familiar with the investor presentation. That exact figure appears in the indexed article excerpt retrieved for this analysis; the attachment's Q3 financial fields remain blank. [Original reporting](https://www.breakingviews.com/40925ca4af2b/columns/breaking-view/anthropics-2-trln-dream-faces-deflation-trap-2026-10-15/); [retrieval record](web-evidence.txt).

The reported Q3 figure implies **45.4% sequential growth DERIVED**, down from Q2's 144.2%. As a rough independent scale check, the filing's approximately 5,300 employees and >$6.6m TTM revenue per employee imply about 35bn TTM revenue; subtract Q4 2025 and H1 2026 and the residual is around 16.7bn. Because headcount is rounded and productivity is a lower-bound metric, this corroborates scale, not an exact Q3 result. Source: S-1 lines 3025–3028 and 6472–6474; calculation in calculations.json.

| Q4 sequential assumption ESTIMATE | Q4 revenue DERIVED/PARTIAL | FY2026 revenue DERIVED/PARTIAL | Q4 average-quarter annualization DERIVED/PARTIAL |
|---|---:|---:|---:|
| −10% stress | 15.12 | 48.21 | 60.48 |
| 0% | 16.80 | 49.89 | 67.20 |
| +20% | 20.16 | 53.25 | 80.64 |
| +40% | 23.52 | 56.61 | 94.08 |

Worked path: **Q3 16.8 PARTIAL × 1.20 ESTIMATE = Q4 20.16; H1 16.286 HARD + Q3 16.8 + Q4 20.16 = FY2026 53.246**. These growth assumptions are transparent stresses around deceleration, not fitted parameters or probabilities. The annualized-quarter column is not the company's defined run-rate metric and is not a 2027 forecast. Each 10 percentage points of Q4 growth changes FY2026 revenue by **1.68bn DERIVED**.

**9. Forward margin: use observed costs to calibrate the sensitivity.**

Q2 adjusted non-compute expense was **10.581 total expense − 5.558 compute − 1.261 stock compensation = 3.762bn DERIVED**. Divide by Q2 revenue 11.555 and the observed ratio is **32.6%**. The future assumption that this ratio stays constant is an **ESTIMATE**, not a fact.

| Future compute / revenue ESTIMATE | Adjusted margin using Q2 other-cost ratio, 32.6% ESTIMATE | Adjusted margin using Q1 other-cost ratio, 41.5% ESTIMATE |
|---|---:|---:|
| 50% | 17.4% | 8.5% |
| 60% | 7.4% | (1.5%) |
| 70% | (2.6%) | (11.5%) |

Equation: **adjusted operating margin = 100% − compute share − 32.557%**. A ten-percentage-point rise in compute intensity costs ten margin points if the other ratio stays fixed. The Q2-calibrated adjusted break-even compute share is **67.4%**, versus **56.5%** for GAAP using the Q2 non-compute expense ratio including recognized compensation. These are sensitivity thresholds, not estimates of what management will deliver.

The separate-period check is deliberately cautionary: applying the Q2 ratio to Q1 predicts 1.540bn of adjusted non-compute costs versus 1.961bn actually incurred, an understatement of **21.5%**, or **8.9 margin points**. The Q1 ratio is calibrated separately as 1.961 / 4.731 = **41.5%**. The 60% compute case changes from a profit to a loss when that observed ratio is used. That is too material to call the forecast validated. The scenario is **directional** and should not be used to value a stable mature margin.

**10. Valuation: distinguish hypothetical equity value from actual IPO terms.**

At **1.5tn / 2.0tn hypothetical equity values ESTIMATE**, the 53.25bn middle revenue sensitivity implies **28.2x / 37.6x equity value / FY2026 sales DERIVED**. On the externally reported Q3 revenue annualized to 67.2bn, the same values imply **22.3x / 29.8x**. These are neither EV/revenue multiples nor confirmed IPO valuations; IPO price, proceeds, dilution and the final share denominator are blank.

Such prices would require sustained growth and durable cash economics after infrastructure payments and equity compensation. The attachment makes the operating inflection credible; it does not establish that the entire multi-year build is internally funded or that a particular valuation is justified.

**Verification and limits.** Historical revenue, operating-income, functional-expense, adjusted-income and cash-flow arithmetic reconcile. Rounded September productivity is consistent with the externally reported revenue scale, with the caveats above. The Q1 cost holdout is amber, the consolidated commitment roll-forward and forward cash-flow schedule are unavailable, and future assumptions are not externally validated. **Independent numerical skeptic verdict: PARTIAL overall; historical arithmetic PASS, forward profitability assumption-sensitive.** Its findings were incorporated: both historical cost ratios are shown, finance-lease/noncash investment and the unpaid settlement sit beside cash flow, and RSU annual equivalents are explicitly not forecasts. [Audit memo](audit.md) · [calculations](calculations.json) · [reproducible script](calculate.py).
