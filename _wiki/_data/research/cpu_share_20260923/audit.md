## Double-check verdict: CPU market-share source tables — PARTIAL

Audit date: 2026-09-23. Scope: `research.json`, its cited source images, and the proposed arithmetic; not a single-name investment review or a review of the rendered Word document. **Source transcription: PASS. Arithmetic: PASS. Empirical validation of the PC 2029–30 extension: NOT ESTABLISHED.**

### 1. Outlook email coverage

- Not applicable to this bounded audit of specified research exhibits. No Outlook pull was run, and no claim of exhaustive broker coverage is approved.
- Directly inspected BofA, Vivek Arya / Duksan Jang / Michael Mani / Liam Pharr, 2026-08-12, `relatórios bons/_assets/Vivek_on_CPU/p001.jpg`, p005, p006, p016, p019, p020 and p021; UBS, Sunny Lin / Randy Abrams / Nicolas Gaudois, 2026-05-21, `relatórios bons/_assets/CPU_TAM_-_UBS/p001.jpg` and p002; BofA 2026-02-23, `relatórios bons/_assets/CPU/p017.jpg`.

### 2. SEC filings coverage (last 2 years)

- Not applicable to the specified cross-market source-table audit. No filings were read, and the source estimates must not be described as audited company-reported market shares.
- BofA p021 Exhibit 30: every Intel / AMD / Arm-based PC value-share row for 2021–2028 and server value-share row for 2021–2028 agrees with `research.json`.
- BofA p006 Exhibit 4: 2029 server value shares are Intel 23.2%, AMD 31.0%, and combined Arm 45.8% (36.6% merchant + 9.2% custom); 2030 is 22.0%, 30.7%, and 47.3% (37.9% + 9.4%). These agree with the proposed series.
- BofA p016 Exhibit 17 and p019 Exhibit 26: all supplementary annual 2023–2026 and 2Q26 unit-share observations agree. Full-year estimates and individual quarters remain separate.
- BofA p005 Exhibit 3: 2030 units are 29.3m Intel, 24.9m AMD, 27.8m Arm, total 82.0m. Derived unit shares are 35.7317%, 30.3659%, and 33.9024%, displayed as 35.7% / 30.4% / 33.9%. These percentages are derived from rounded source units, not exact printed percentages.
- UBS p002 Figure 2: 2030 unit shares are Intel 29%, AMD 29%, Arm 42%; 2025 total units are 23m and 2030 total units are 63m. These are not the same totals as BofA's 29.9m and 82.0m. The report's Figure 1 also differs from Figure 2 in 2027; use Figure 2 consistently if extending its unit table.

### 3. Bloomberg API cross-check (REFERENCE ONLY — not gabarito)

- BBG pull run: No. No traded-security price, valuation, earnings-date, consensus EPS, or broker-rating claim is included in this bounded audit. Bloomberg consensus would not validate these broker-specific architecture-share forecasts.
- Internal arithmetic guardrails: every sourced share lies within 0–100%; every supplied share row sums within 0.1 percentage point of 100%. This is consistent with printed one-decimal rounding. Do not silently normalize the source shares.
- These are accounting and domain checks. They do not independently validate the forecast.

### 4. Transcript coverage

- Not applicable to this exhibit transcription and arithmetic audit. No transcript was read. No conclusion about Intel, AMD, Arm Holdings, or NVIDIA management guidance is approved by this memo.

### 5. Unsourced or weakly-sourced claims in prior work

- **PC extension is not calibrated to an observed 2028 outcome.** Its rates combine BofA's historical 2025 estimate with its 2028 forecast. Describe the procedure as an illustrative continuation of a broker path, not an independently calibrated market forecast. The load-bearing assumption is persistence beyond 2028.
- **Do not interpret HARD as certainty.** HARD can mean an exact transcription, including an uncertain broker forecast. Historical estimates, broker forecasts, and illustrative extensions must remain visibly distinguished in the table and charts. Prefer `PARTIAL / DERIVED` for the rate calculation; its arithmetic is exact while its future relevance is uncertain.
- **Historical server value shares were materially restated.** February BofA p017 assigns 2025 Arm 11.0% value share, 13.6% unit share and $720 ASP. August p019 assigns 32.3%, 13.7% and $2,748 ASP. The change between report vintages is not observed market adoption. The main historical series must be called the August 2026 vintage of historical estimates.
- **Pricing caveat needs precision.** August p005 states approximately 75% of AMD ASP for custom Arm and approximately 1.25x for merchant Arm, but the table does not apply those ratios uniformly across history and the aggregate merchant category. For example, 2026 aggregate merchant Arm ASP is $4,246 versus AMD $1,635; the merchant aggregate includes NVIDIA's separate pricing and mix. In 2025 custom Arm ASP is $666 versus AMD $1,322. Cite those statements as modeling assumptions, not a universal formula reconstructing the entire table.
- **Internal source disagreements are real.** August p021's 2025 PC value shares 64.5 / 23.2 / 12.3 differ from p016's 64.8 / 23.3 / 11.9. August p006 prose says merchant Arm approximately 28% in 2026, while its chart and p005 table show approximately 33%. Keep p021 as the annual value-share source and identify the discrepancy; do not mix the annual tables. The 2028 combined Arm components on p006 round to 45.0%, while p021 prints 45.1%; use p021's combined figure consistently.
- **Arm-based is an architecture group.** It combines merchant suppliers and hyperscaler custom silicon; custom silicon value uses imputed silicon cost. It is neither Arm Holdings sales nor a single vendor's market share.
- **UBS is a comparison, not validation.** Its unit universe and vintage differ. It cannot be averaged with BofA or described as an independent confirmation of the PC extrapolation. Likewise, the Mercury table on August p020 runs only through 2027; its headline's long-term framing is not a sourced 2030 point estimate.

### 6. What the prior analyst MUST do before this work ships

1. Keep a visible boundary between historical source estimates (2021–2025), broker forecasts (2026 onward), and the illustrative PC extension (2029–2030). Label shares as annual shipment/value flows, not installed base.
2. Place the historical restatement and architecture/imputed-value caveats close to the server chart/table. Without them, the main value-share conclusion invites a false economic interpretation.
3. Amend the ASP caveat as specified above. No share-value correction is necessary.
4. Show the PC calculation: AMD step = (25.8 − 23.2) / 3 = 0.8667 pp/year; Arm step = (16.8 − 12.3) / 3 = 1.5 pp/year; Intel = 100 − AMD − Arm. This gives 2029 Intel / AMD / Arm of 55.0 / 26.7 / 18.3 and 2030 of 52.7 / 27.5 / 19.8 after display rounding.
5. Display sensitivity as assumption scenarios, not confidence intervals: at 0x persistence, 2030 is 57.4 / 25.8 / 16.8; at 1x, 52.7 / 27.5 / 19.8; at 1.5x, 50.3 / 28.4 / 21.3. All are internally consistent; none is externally validated by the cited evidence.
6. State that final Word layout and displayed labels require the producing agent's separate review. This memo audits source data and model arithmetic only.

### 7. Bottom line

The source-table work and arithmetic pass. The extension remains an illustrative assumption, and the largest risk is presenting revised broker value estimates as observed market economics. This can ship as a clearly labeled broker-based comparison with a limited extension; it cannot ship as an independently validated 2030 market-share forecast.
