# AKAM / Anthropic — conditional revenue and EPS bridge

Prepared 2026-09-24. **Directional scenario, not revised consensus or a calibrated forecast.** All dollar values USD; revenue/net income/share counts in millions, EPS in dollars. Annual FY lines are used consistently, rather than mixing the quarterly CY roll-up with annual consensus.

## Evidence and inputs

| Input | Value | Grounding / source |
|---|---|---|
| Additional contractual commitment | $11,600m over seven years | **HARD disclosed**, Akamai release, 2026-09-24, pp. 1–2; forward contractual value, not realized revenue |
| Contingent expansion | Up to $9,000m | **HARD disclosed contingency**; excluded from every scenario |
| Deal capex | Approximately $5,500m; $1,700m incremental in 2026 | **HARD company forecast**, same release; timing after 2026 not disclosed |
| 2026 revenue guide | No change | **HARD company statement**, same release; no corresponding EPS reaffirmation |
| Annual FY26 consensus | Revenue 4,488.423; adjusted EPS 6.692 | **HARD saved Bloomberg estimate**, snapshot 2026-09-24 |
| Annual FY27 consensus | Revenue 5,075.423; adjusted NI 1,102.560; EPS 7.259; EBIT 1,262.333 | **HARD saved Bloomberg estimate**, same snapshot |
| Annual FY28 consensus | Revenue 5,642.071; adjusted NI 1,247.071; EPS 8.125; EBIT 1,442.429 | **HARD saved Bloomberg estimate**, same snapshot |
| Incremental revenue realization | FY27 50% of annual equivalent; FY28 100%; FY27 25% stress | **ESTIMATE**. Illustrative timing, not company guidance. No observed deployment anchor is available for this contract |
| Expansion already embedded in baseline | Zero | **ESTIMATE**. The snapshot predates the release, but analysts may already include unsigned-pipeline growth. No constituent-model reconciliation was available; any overlap must be deducted from the additions below |
| Incremental operating margin, after depreciation | 20% central; 15% / 25% sensitivity | **ESTIMATE informed by PARTIAL analogs**. MS Sanjit Singh, Aug-31/Sep-4 relay, models 20% on a $1bn four-year deal and 25% on $500m. Q2 CFO commentary supplies a broader low/mid-20s to low-30s band. Neither calibrates an $11.6bn seven-year CPU deal; MS underlying note not read |
| Tax on incremental earnings | 19% | **ESTIMATE carry-forward** of **HARD** CFO Ed McGowan's 2026 guide, 2026-08-06, transcript 00:19:49 / 00:21:35 |
| Baseline modeling-equivalent shares | FY27 151.889; FY28 153.486 | **DERIVED from consensus anchors**, NI / EPS. Ratio of separately aggregated consensus series; not a reported or directly sourced diluted-share forecast |
| Incremental shares | 3.08m | **ESTIMATE** full initial-warrant economic dilution: 7.7m × 2/5. Underlying warrant terms are **HARD**, Akamai Sep-24. Vesting percentages are approximate; treasury-stock accounting would differ |
| Incremental funding expense | Zero in displayed operating scenarios | **ESTIMATE / exclusion**, not a funding forecast. Sensitivity shown below; lost interest, new debt interest, financing shares and startup losses beyond the chosen margin remain unresolved |

Bloomberg source file was saved at **2026-09-24 12:41:47 local**; it is a baseline and is **not verified to reflect today's announcement**. Its annual FY27 line is $5.075bn/$7.259; the wiki's quarterly CY27 roll-up is $5.087bn/$7.24. Preserve the distinction. [Frozen source snapshot](../_data/research/AKAM_Anthropic_2026-09-24/consensus_snapshot.json).

## Arithmetic and scenarios

Annual contract equivalent = 11,600 / 7 = **1,657.143**. This is a contractual average, not a disclosed annual run rate or deployment schedule.

FY27 central revenue = 5,075.423 + 1,657.143 × 50% = **5,903.995**.

FY27 incremental EBIT = 828.571 × 20% = **165.714**; incremental adjusted NI = 165.714 × (1 − 19%) = **134.229**.

FY27 illustrative EPS = (1,102.560 + 134.229) / (1,102.560 / 7.259 + 3.08) = **7.981**.

General equation: `(baseline NI + incremental revenue × operating margin × (1 − tax) − additional pretax costs × (1 − tax)) / (baseline NI / baseline EPS + additional shares)`.

**The EPS columns below assume zero additional funding cost and zero losses outside the operating-margin assumption. They include full assumed initial-warrant share dilution, but no adjustment for customer-warrant consideration in reported revenue.**

| Scenario | Total revenue | EPS at 15% margin | EPS at 20% margin | EPS at 25% margin |
|---|---:|---:|---:|---:|
| FY27: 25% of annual equivalent | 5,489.709 | 7.440 | 7.548 | 7.656 |
| FY27: 50% of annual equivalent | 5,903.995 | 7.764 | 7.981 | 8.197 |
| FY28: 100% of annual equivalent | 7,299.214 | 9.251 | 9.680 | 10.108 |

For FY26, unchanged revenue guidance supports no incremental revenue in this bridge. The release does **not** establish unchanged EPS. Do not carry the old EPS number forward as a revised forecast.

## Sensitivity and checks

- **Timing:** 10 percentage points of annual-equivalent recognition changes revenue by $165.714m; no evidence currently makes a half-year-equivalent 2027 forecast more than a scenario. A seven-year average is not a ceiling on peak annual revenue.
- **Margin:** five percentage points changes FY27 half-year-equivalent EPS by $0.217 and FY28 annual-equivalent EPS by $0.429.
- **Funding / unmodeled startup costs:** each additional $100m pretax costs reduces EPS by $0.523 in FY27 / $0.517 in FY28. Thus central-case FY27 EPS becomes **$7.46** with $100m of additional annual costs. Around **$138.1m** erases all FY27 central-case accretion versus baseline EPS. These are sensitivities, not financing estimates.
- **Warrants:** full initial economic dilution is a conservative denominator convention, not the treasury-stock method. Exercise proceeds are not assumed available; customer-consideration accounting and its possible revenue effect remain unmodeled.
- **PASS — basis/reconciliation:** contractual stock versus annual flow labeled; old $1.8bn not subtracted from an explicitly incremental commitment; optional $9bn excluded; no invented MW; annual Bloomberg lines kept separate from CY roll-ups; capex not directly expensed or added to revenue.
- **PARTIAL — calibration:** effective shares are anchored to baseline NI/EPS only for bookkeeping. The underlying contract margin and revenue timing have no observed calibration. Prior Q2 corporate operating margin of 24.6% and consensus FY27 EBIT margin of 24.87% are context, not independent validation of this contract.
- **PARTIAL — economics:** operating-margin assumptions include depreciation, but capex deployment, asset lives, funding, startup losses and warrant accounting are not modeled independently. MS's older $100m-capex EPS sensitivity is not extrapolated to $5.5bn.

**Independent double-check verdict: PARTIAL.** Source terms and arithmetic verified; contract-specific margin, ramp and funding prevent treating the output as a precise forecast. The independent review requested the visible 15% margin case, prominent financing exclusion, and no inference of unchanged FY26 EPS; all are incorporated.

## Sources

- Akamai primary release, **2026-09-24**, [archived PDF](../../AKAM/sources/2026-09-24_Anthropic_agreement_PR.pdf), [text](../../AKAM/sources/2026-09-24_Anthropic_agreement_PR.txt), [IR original](https://www.ir.akamai.com/static-files/e742c1c3-d75a-4fcb-a6f5-df289f242c95). Explanatory call scheduled for 5:30 p.m. ET; content not yet reviewed in this pre-call note.
- Bloomberg, **2026-09-24**, [frozen annual/CY snapshot](../_data/research/AKAM_Anthropic_2026-09-24/consensus_snapshot.json); [calculated scenarios](../_data/research/AKAM_Anthropic_2026-09-24/scenarios.json).
- Akamai CFO Ed McGowan, **2026-08-06**, [Q2 transcript](../../AKAM/transcripts/AKAM_Q2-2026-earnings_2026-08-06.md), 00:19:49–00:22:32. Third-party Quartr/MarketBeat transcript; management ranges are not contract-specific.
- Morgan Stanley / Sanjit Singh, **2026-08-31 and 2026-09-04**, sales relays retained in [AKAM wiki](../AKAM.md); underlying research model not read.
