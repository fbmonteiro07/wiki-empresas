# Independent workbook arithmetic and source audit — 2026-10-23

Verdict: **PARTIAL overall; PASS for arithmetic and repaired controls.** The final audited export passes the independent source, default-formula and scenario checks below. Underlying company token consumption remains an unvalidated conditional estimate.

Scope: read-only audit of the numerical workbook, original house ARR model and saved Ramp raw files. No single-name earnings work, SEC/Outlook completeness assertion, or vendor webpage verification is implied by this audit.

## Evidence and method

- Public workbook: `R:\AI_Token_Consumption_and_Minimum_Price_with_References.xlsx`.
- Matching local workbook: `E:\Wiki Felipe empresas\outputs\01a168b5-7786-7582-8082-7cd6bd45fd69\AI_Token_Consumption_Price_and_Mix.xlsx`.
- Both pre-fix SHA-256 hashes: `a709f212fbbe75b56d5031dc0536a69368cf350d3dee19bce0afc0f5489a32e8`.
- Original source: `P:\Felipe Monteiro\US Equities\Modelos oficiais\AI Model.xlsx`, SHA-256 `3d9eda23569aed4b4dfb8858b07faceb1daa8425c06821ad35247e6dc11b93b5`.
- Independent stdlib OOXML parsing; no reliance on builder verification files. Recomputed the raw JSON aggregations, matched-model treatment, category bridge, family allocation and unit conversions. **3,278 source/calculation comparisons passed.** Independently parsed/evaluated **all 2,337 formula caches**, with zero default-cache mismatches. The evaluator is a mathematical check, not a substitute for native Excel recalculation.
- Public workbook has no external link parts and no cached Excel error cells. Original model errors elsewhere were neither imported nor repaired.

## Severity-ranked findings

### 1. HIGH — API scenario controls allowed impossible output (pre-fix)

`Inputs!D10:O10` and `D16:O16` feed `Consumption!D14:O14` and `D32:O32` without range/economic guards. Independent in-memory formula evaluation showed:

- `Inputs!N10=-10%`: `Consumption!N18=-0.8302613458 Q/month`.
- `Inputs!N16=110%`: `Consumption!N36=11.8471189675 Q/month`, greater than `Consumption!N35=10.7937284589 Q/month`.
- `Inputs!D4=2`, `Inputs!N10=10%`: `Consumption!N18=-0.08302613458 Q/month`, even though the entered share is between zero and 100%.

The last case matters: Anthropic gross/net differences are allocated wholly to API. The source currently implies an 11% gross-to-net gap, so gross API share must be at least 11% for nonnegative net API. Necessary conditions are finite numeric gross ARR >= net ARR > 0; raw share between 0 and 1; transformed gross/net API revenues within their corresponding total ARR. The exact zero-net-API boundary should remain valid; round only tiny floating-point residuals. No silent economic clamping.

Root also found a live artifact-engine zero-versus-blank issue in forecast mix overrides. That engine-specific result is root-owned; the independent mathematical evaluator treats zero as a real override and computes a valid price of $0.5893092083/M for Anthropic input/output/residual shares 1%/0%/99%.

**Remediation status: repaired and independently verified in the final audited export.** The 24 API-share formulas now enforce source/derived revenue bounds; the 12 forecast-mix overrides use ISBLANK. All tested zero boundaries remain valid.

### 2. MEDIUM — inherited OpenAI gross-up denominator is ambiguous

This is a source-model ambiguity, not a proven error in copying or in the output workbook.

Original `ARR Tracker!P29=20%`; `B29` says `(-) % Take CSP sobre API 3P`. `P30=OpenAI!AB29*OpenAI!AB30=12.3327185374%`; `B30` says `% API 3P (CSP) / Receita (Anthropic L19)`. `OpenAI!A26` labels API Revenue (net); `AB29=24.6654370748%`; `A30` says `% vendido via cloud`, with `AB30=50%`. These labels do not explicitly define the 20% denominator. No relevant cell comment supplies it.

`ARR Tracker!P28=P7*(1+$P$29*$P$30)`, shared through AA28, produces API gross revenue equal to 1.10 times API net revenue. If 20% is a take rate on gross customer billings, exact gross API revenue would instead be:

`net API × [50% + 50% / (1 - 20%)] = net API × 1.125`.

October net API ARR is $13.6996099212bn. Current gross API ARR is $15.0695709134bn versus $15.4120611614bn under that conditional alternative. API-equivalent volume would rise from **2.507067635 to 2.564046445 Q/month (+2.2727%)**; full-company gross ARR rises 0.601792%. Preserve the source and disclose the basis ambiguity unless the source owner defines the denominator.

### 3. Material model limitation — internal consistency does not prove company traffic

`Consumption!C5`, `Price build!C4:C5`, and the explanatory notes already disclose this limit. The October Ramp all-token price is $0.8020841167/M for Anthropic and $0.5009029508/M for OpenAI. Applying company house ARR to a Ramp sample requires unverified representativeness and billing/revenue comparability.

The residual shares at `Price build!M16=95.05982650%` and `M56=72.90761380%` are subtraction results, not independently observed cache-read shares. The tokenVolumes-versus-tokenPrices denominator gaps at `Minimum price!M18=77.84379255%` and `M34=9.51103263%` remain unresolved. Consequently, the lower-reference price is a scenario, not an economic floor, confidence interval or validated company ASP. This is correctly disclosed in the workbook and should remain prominent.

## What passed

1. **ARR basis and source mapping.** All 48 gross/net monthly ARR values match `ARR Tracker!P98:AA98`, `P84:AA84`, `P95:AA95` and `P81:AA81`. The source explicitly labels these average monthly ARR; separate beginning/end-of-period rows exist. The workbook did not mistakenly divide endpoint ARR by 12. `Inputs!D10:O10` correctly copies Anthropic CY2026 gross API share from `Anthropic!AB11=85%`; `D16:O16` correctly copies OpenAI net share from `OpenAI!AB29=24.6654370748%`. Holding annual shares across months is an estimate, disclosed in Inputs.
2. **Gross/net transformations.** Anthropic gross API ARR = gross ARR × 85%; net API subtracts the gross/net difference. OpenAI net API = net ARR × its net share; gross API adds the gross/net difference. Correct relative to the original house-model convention, subject to finding 2.
3. **Time and units.** Monthly-average ARR in $bn /12 /($ per million tokens) yields quadrillion tokens/month. Multiply by 1,000 and divide by calendar days for trillion/day. Both January–December chains reconcile, including February 28 days. Historical price observations are 41 nonoverlapping seven-day windows per provider, ending Jan4–Oct11; October includes Sep28–Oct11. This is not exact calendar-month billing. Nov/Dec carry October mix and rates at the default zero price-change setting.
4. **Raw observations.** 3,894 price records and 19,156 volume records were parsed. No duplicate price keys were found. All 82 used provider/week pairs, 130 family/month rows and 82 category input rows reconcile to raw source records. Missing model spending is excluded from matched prices; zero-token spending is excluded from matched cost. No missing-spend volume was silently priced at zero.
5. **All 24 monthly outputs.** Independent prices, category shares/rates/contributions, minimum references, full/API volumes, family shares and allocations match cached outputs. Family allocations sum to full-ARR equivalents, not API-only equivalents; that basis is explicit in the formulas and should be understood when reading the allocations.
6. **Forecast mathematics.** A -10% monthly rate change gives November/December Anthropic prices $0.7218757051/$0.6496881346 per million and December full-ARR equivalent 10.8651484760Q/month. -100%, below -100%, and invalid category sums suppress consumption. Net-mode October API equivalents independently recompute to Anthropic 5.7961641122Q and OpenAI 2.2791523952Q. Zero-override execution must be verified in the workbook engine, as described above.

## Post-fix verification

Final audited artifact: `E:\Wiki Felipe empresas\outputs\01a168b5-7786-7582-8082-7cd6bd45fd69\AI_Token_Consumption_Price_and_Mix_Audited.xlsx`.

SHA-256: `56533ae22ce49c0fbb773d0d4a8c4c861336b6edf946ec36580d0ea8bd6547a4`.

- All **3,278 source/default-output comparisons** pass again against the new OOXML export.
- All **2,361 final cached formulas** pass an independent stdlib AST evaluation, including the new IF/ISBLANK/ROUND logic. No cached Excel error cells.
- **316 in-memory scenarios / 320 output checks** pass. Coverage spans all 12 months, both ARR modes and both providers: negative/>100%/text/blank API shares; Anthropic 10% invalid and exact 11% zero net-API boundary; OpenAI zero net-API share; negative/text/inconsistent gross/net ARR; both forecast months with an explicit zero output-token share.
- In the explicit 1% input / 0% output / 99% residual forecast, Anthropic price independently computes to $0.5893092083/M; OpenAI price to $0.2328400959/M. Zero is honored as an input.
- Original source-workbook capture hash still matches the actual file, and all 12 source/public month headings map correctly. No source assumption was revised by this audit.
- This is an independent mathematical/formula check, not native Excel execution. Root separately performed live artifact-engine recalculation and checked layout/preservation.

No remaining numerical/control blocker was found. Evidence remains PARTIAL for the disclosed sample-to-company transfer, residual interpretation and source-model CSP-take denominator.
