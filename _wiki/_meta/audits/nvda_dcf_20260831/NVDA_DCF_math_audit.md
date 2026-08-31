# NVDA DCF arithmetic and model-logic audit — 31 August 2026

Source: Felipe Monteiro, Template DCF NVDA.xlsx, saved 31 August 2026 at 08:48:45 São Paulo time. Original: P:/Felipe Monteiro/US Equities/Modelos oficiais/Template DCF NVDA.xlsx. All model figures below come from this saved workbook; corrected figures are audit recalculations dated 31 August 2026, holding its assumptions constant unless stated. Dollar amounts in financial schedules are treated as US$ millions, consistent with the scenario-engine label X117 and the per-share calculations.

The original workbook was not changed. Its SHA-256 at extraction and verification was 19703e93c903167788684adda6d03f1bfed2558e3ac1d1af6b85d8cb0b86b9fb.

**Verdict: the saved arithmetic reproduces, but the workbook should not receive an unqualified model-logic sign-off.** The important issues are inconsistent terminal discounting, mixed cloud commissioning lags, depreciation that does not implement the stated asset lives, and stale descriptions of the active assumptions. The existing corrected valuation, E88, is mathematically sound under its stated convention and the workbook's cash-payout assumptions.

**Coverage and checks passed**

- Both worksheets, including hidden rows 16–38 of Capa DCF - Base, were examined.
- All 1,287 ordinary formula cells independently reproduced their saved results. This includes expanded shared formulas, array INDEX formulas, all ordinary cross-sheet references, and the six external-link formulas. There were no formula-evaluation errors, unexplained numeric cache mismatches, or circular dependencies encountered.
- The remaining formula anchor is Excel's two-variable Data Table E97:J102. All 36 results reproduced independently by changing D92 and D93 and recalculating E88.
- All 25 CAGR/share scenario engines reproduced their saved values and achieved their specified CY2028–45 revenue CAGR. Their discounting convention still has the timing issue described below.
- Historical and near-term capex components, hyperscaler totals, other-player totals, top-level designer totals, and AVGO subcomponents reconcile. The MRVL displayed breakdown needs an explicit Alchip allocation bridge.
- Gross profit, negative operating costs, EBIT, taxes, earnings, payout cash, and the terminal numerator reconcile mechanically.
- D57:I57 match the 24 directly referenced values in R:/Modelo Felipe NVDA .xlsx, Total rev, EV:FA, rows 7, 11, 15 and 17; linked file saved 27 August 2026. That is a direct-input check, not a full audit of the larger source workbook.
- The cloud revenue-hurdle formulas correctly invert their stated NOPAT/return equations for the denominator and depreciation used.

These checks verify mathematical implementation. They do not validate the commercial accuracy of the hardcoded capex, market-share, margin, demand, tax, or discount-rate forecasts. There is no full balance sheet or cash-flow statement in this two-sheet file.

**1. Terminal value is discounted one year too far in the old valuation. The existing correction has not propagated.**

Location: Capa DCF - Base!D85, D88, E88, D90:E90.

D85 is =NPV(D81,G79:AA79). G79:Z79 contains 20 annual distributions, CY2026 through CY2045. AA79 is the terminal value at the end of CY2045. Placing AA79 after those 20 flows makes Excel discount it as period 21 rather than period 20. Microsoft documents that NPV treats successive values as successive end-of-period cash flows: https://support.microsoft.com/en-us/excel/functions/npv-function

The workbook already documents this issue beside E88. The error is therefore not an undisclosed discovery; the audit confirms that the correction is right and that dependent outputs still use the old branch.

Using D81 = 10%, D83 = 2.5%, D86 = 24,100 million shares:

1. PV of the 20 forecast distributions = US$3,942,694.779 million.
2. Terminal value = 1,367,737.083 × 1.025 / (0.10 − 0.025) = US$18,692,406.805 million.
3. Correct terminal PV at the start-of-2026 reference point = 18,692,406.805 / 1.10^20 = US$2,778,507.164 million.
4. The old formula instead uses US$2,525,915.604 million.
5. Old per-share value = (3,942,694.779 + 2,525,915.604) / 24,100 = US$268.4071.
6. Fixing only the terminal discount period gives US$278.8880. The timing-error effect alone is US$10.4810 per share.
7. Rolling that value forward by 238/365 years to 27 August 2026 gives 278.8880 × 1.10^(238/365) = US$296.7701. This agrees with E88.
8. Updating only the valuation date to 31 August 2026, with all financial inputs unchanged, gives US$297.0803.

Do not describe the full US$28.36 gap from D88 to E88 as the terminal-period error: it also includes the valuation-date roll-forward.

D90 and E90 use D88 divided by H76 and I76. They show 15.8341× and 11.8154×. Using the corrected E88 price consistently gives 17.5073× CY2027 and 13.0639× CY2028. Their earnings denominators are NOPAT per share, as discussed below.

A correct start-of-2026 total PV formula is:
=NPV(D81,G79:Z79)+AA79/(1+D81)^20

Use one clearly dated valuation output for the main price, multiples, and all sensitivity tables.

**2. The second sensitivity table still embeds the period-21 terminal error.**

Location: Capa DCF - Base!D109:H113; engine X118:X142.

Every engine total uses the pattern:
=NPV($D$81,$G$79:$I$79,F118:V118,W118)

There are three CY2026–28 flows plus 17 CY2029–45 flows, then terminal value W118 as an extra 21st period. This branch also lacks E88's August date roll-forward. By contrast, the first sensitivity table E97:J102 correctly uses E88 and all 36 saved outputs reconcile.

Example: 7.5% CY2028–45 revenue CAGR and 50% terminal share, output F110 / engine row 129:
- Saved old-basis result: US$301.9135 per share.
- Correct period-20 terminal value and 27 August 2026 date: US$334.6867 per share.

A corrected engine formula for row 129, retaining the current date convention, is:
=(NPV($D$81,$G$79:$I$79,F129:V129)+W129/(1+$D$81)^20)*(1+$D$81)^((DATE(2026,8,27)-DATE(2026,1,1))/365)

The output table then continues to divide the engine value by D86.

The CAGR back-solve itself is correct. It changes capex growth to achieve the selected NVDA revenue CAGR, conditional on the selected share. Thus, holding a CAGR row constant also holds terminal NVDA revenue constant across the share columns; share changes the required capex path and intermediate cash flows. This is a conditional scenario table, not a pure share sensitivity at fixed industry capex. Also, the engine assumes flat capex growth after CY2028, whereas the base case uses 10% in CY2029 and 8% thereafter. A base-case CAGR is therefore a reference, not an exact replication of the base path. C117 incorrectly says CY25–45 even though the formula and main title use CY28–45.

**3. The cloud-return sheet uses inconsistent commissioning lags.**

Location: ROIC Cloud!C2, F16:Z18, F20:Z23, G26:N26, C32.

- The title and row 26 describe t−2.
- Row 16 actually references the immediately prior year's capex: for CY2029, J16 = I15, i.e. CY2028 capex.
- Rows 17–18 and 26 follow that t−1 input.
- Fleet rows 20–23 actually use t−2 commissioning: CY2029's newest cohort is H15, CY2027 capex.

With the present 90% EBITDA margin, 15% tax rate and 14.398685% first-year depreciation rate, M_A = (15% / 85% + 14.398685%) / 90% = 0.356063821.

For CY2029:
- t−1 cloud capex = US$1,747.859 billion; annual revenue needed for 15% vintage ROIC = US$622.349 billion.
- t−2 cloud capex = US$1,131.248 billion; the comparable hurdle = US$402.796 billion.
- Row J26's saved single-vintage ROIC is 17.2453%; using t−2 in that same single-vintage formula gives 33.3163%.

These two vintage ROIC figures both allocate all house demand to one cohort and should not be mistaken for aggregate fleet returns. The workbook itself warns about this simplification.

Choose the intended commissioning convention, then align formulas, labels, and comparisons. This audit does not assume that t−2 is economically preferable merely because the title says so.

**4. The fleet does not actually implement the stated 5/6/15-year depreciation schedule.**

Location: ROIC Cloud!D9:E9 and F20:Z23.

D9 correctly calculates a first-year weighted depreciation rate using the fixed CY2027 capex weights:
chip share / 5 + network-and-CPU share / 6 + hard-asset share / 15 = 14.398685%.

However, the fleet then depreciates every whole cohort at this single rate, equivalent to approximately 6.945 years, and carries only seven in-service cohorts. That keeps depreciating the five-year chip component after year five and removes fifteen-year assets far too early. A weighted first-year rate is not equivalent to preserving separate asset lives through time.

Recomputing each component separately, retaining the workbook's CY2027 mix, two-year commissioning lag, 90% margin, 15% tax and average-net-capital convention:
- CY2033 fleet ROIC changes from −2.8455% to −1.9332%.
- CY2035 revenue required for 15% fleet ROIC changes from US$3.8052 trillion to US$3.6092 trillion.
- CY2045 revenue required changes from US$8.4119 trillion to US$8.7265 trillion. The direction is not uniform through time.

There is also a smaller final-year averaging issue. MAX(0,1−(age+0.5)×rate) is not exactly the average of beginning and ending net book values when an asset reaches zero during the year. Average the separately floored opening and closing balances. Under the existing blended-life approximation this changes CY2045 average net capital from US$17.1517 trillion to US$17.1658 trillion; this is much smaller than the asset-life issue.

**5. Several cloud narrative conclusions describe an older case.**

Location: ROIC Cloud!D7, C3, C34, C36.

D7 currently assumes a 90% rental EBITDA margin. C34 says fleet returns are approximately 5% in CY2029 and 0% in CY2030, whereas the current saved J27 and K27 are 15.0364% and 7.6593%. Its quoted revenue hurdles of approximately US$1.0 trillion and US$1.8 trillion also differ from current J22/K22, US$0.6728 trillion and US$1.2111 trillion.

In C36:
- M at 50% EBITDA margin, 0.641, and at 70%, 0.458, remain correct.
- The five-year-life M15 is 0.4183 at the current 90% margin, not 0.627.
- The pre-tax M15 is 0.3267, not 0.490.

The latter two old figures correspond approximately to a 60% margin. These are stale descriptions, not stale Excel calculation caches. The 90% margin is an explicit model assumption; this arithmetic audit does not validate it commercially.

The project-IRR equivalents mentioned in C3 are not backed by an explicit project cash-flow/IRR schedule in this file, so they do not establish returns including construction timing.

**6. MRVL's displayed subcomponents need an allocation bridge; do not increase the total blindly.**

Location: Capa DCF - Base!H46:I51.

CY2027: MRVL = US$9.2891 billion, while Trainium + MSFT = 10.6153 + 1.6257 = US$12.2410 billion. The US$2.9519 billion gap equals Alchip in H51 exactly.

CY2028: MRVL = US$13.2860 billion, while Trainium + MSFT = 13.5550 + 3.2515 = US$16.8065 billion. The US$3.5205 billion gap equals Alchip in I51 exactly.

The top-level designer totals already reconcile when Alchip is included separately. This appears to need an explicit gross-to-net allocation/deduction in the displayed MRVL breakdown, rather than adding the residual to MRVL and double-counting it. The intended allocation should be documented.

**7. Material valuation assumptions remain outside the arithmetic sign-off.**

Location: Capa DCF - Base!rows 69–79, D81:D86 and AA79.

The modeled distribution is EBIT × (1 − tax) × payout. Row 75 is therefore NOPAT, not net income after interest. There is no explicit bridge through NVIDIA's capex, depreciation, working capital, financing, or excess cash. This is a payout proxy discounted at cost of equity, not a fully reconciled equity-cash-flow model. Cost of equity can be appropriate for genuine equity distributions, but the bridge to those distributions needs justification. See Damodaran's cash-flow distinctions: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/littlebook/cashflows.htm

Payout is 80% through CY2044, then jumps to 100% in Z78 and carries into the terminal value while distributions grow 2.5% forever. The formula follows that assumption correctly; the funding of sustained growth is not modeled. See the reinvestment/terminal-growth relationship: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/valquestions/termvalueexreturns.htm

Keeping payout at 80% in CY2045 and the terminal period, with everything else unchanged, gives US$270.4382 rather than US$296.7701 on the same 27 August basis. This is an assumption sensitivity, not a recommended fair value or a mechanical correction.

**Other completeness and maintenance flags**

- D56:E56, historical CY2023–24 NVIDIA networking revenue, are blank. D59:E59 therefore treat networking as zero. Confirm whether chips already includes it or fill/document the missing component. Those historical cells do not currently drive the forecast valuation.
- The hardcoded “other” capex residual is negative in D36 (US$−20.0761 billion) and F36 (US$−11.5070 billion); D30 total other-player capex is US$−4.0449 billion. Components still sum. These need a residual/adjustment label or an input reconciliation, rather than being presented as literal spending.
- H22 hyperscaler AI capex is US$1,125.5151 billion versus H16 total hyperscaler model capex US$1,097.7528 billion; H28 correctly reports 102.5290%. These are distinct builds, so the discrepancy is an input/basis reconciliation issue, not a broken division.
- A comment on C30 dated 26 June 2026 already warns that lease and BYOC structures may double-count capex between hyperscalers, neoclouds and labs. No explicit elimination bridge is present in this workbook. This could matter much more than the Excel arithmetic; its effect cannot be quantified from the supplied schedules.
- Source comments are comparisons or older source notes, not proof that the current hardcoded values equal those sources. No broker attribution was inferred where absent.
- There are 42,403 defined names, including 12,170 containing #REF!, and 90 external-link records. Ordinary worksheet formulas only actively use link 90 through D57:I57. No active cell formula references the broken names, and no saved worksheet cell contains an Excel error. The unused metadata is a hygiene problem, not evidence of 12,170 valuation errors.
- E88 hardcodes the valuation date as 27 August 2026. Use a labeled date input if the file is intended to show a current valuation.
- The current terminal-rate condition, 10% > 2.5%, passes. There is no visible guard against a future user setting growth at or above the discount rate.

No workbook edits, link refreshes, or source-forecast changes were made.

