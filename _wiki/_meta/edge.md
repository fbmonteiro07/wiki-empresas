# Edge tracker — house vs Street

_Generated 2026-08-19 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 11.89 | +62% |
| COHR | Revenue $bn | 2027 | 16.60 | 12.70 | +31% |
| NVDA | EPS | 2027 | 15.44 | 12.95 | +19% |
| GOOG | Revenue $bn | 2026 | 505.00 | 426.90 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.40 | +18% |
| AAPL | EPS | 2026 | 10.12 | 8.76 | +16% |
| NVDA | Revenue $bn | 2027 | 661.00 | 573.00 | +15% |

## Curated divergences — latest reconciliation (`reconciliation-2026-08-18-run-inbox.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| 🔴🔴 AVGO | our house FY28 AI number ($251bn) is +22.3% above the Street-HIGH sell-side note and +49% above the Street. The entire house edge in this name lives in FY28, not FY27 | Action: bridge the FY28 house numbers against Wells' published ladder (11.4GW × $13.2bn blended) BEFORE the 2026-09-02 print, and state explicitly whether the house edge is GW or $/GW. Wells' own note concedes the independent Epoch-implied rate is ~$11bn/GW; if the house is at Wells' GW and a higher rate, that assumption is the whole position and should be defended in writing rather than carrie… |
| 🔴🔴 GOOG | Wells' TPU fleet (8.2GW in 2028) is smaller than Barclays' EXTERNAL-only TPU-aaS capacity (11.5GW) already on the page. Both cannot be right | Action: until this is pinned down, treat every GW-based sizing of Google's TPU economics on this wiki as unsafe, including the TPU-aaS unit economics. It is cheap to resolve at the next disclosure and it is the highest-value open question of the run. |
| 🔴 GOOG | Wells' $811bn purchase-commitment figure fails its own arithmetic; the wiki's primary-sourced $707.0bn stands | Action: none on the number — the wiki figure stands. Carry the lesson instead: this line is now large enough that a ~$100bn discrepancy passes unnoticed through a published note, so purchase commitments must be taken from the filing every quarter and never from a broker restatement. |
| 🔴🔴 CROSS-THEME | memory alone at $1.61tn of 2027 revenue does not fit inside $5.8tn of six-year hyperscaler capex | Action: size where that memory revenue is actually SOLD. Three resolutions with opposite trade implications — (a) memory forecasts are too high (bearish MU/SAMSUNG/SKHYNIX/SNDK); (b) hyperscaler capex is too low (bullish the complex); (c) memory sells far beyond the five hyperscalers into sovereign, neocloud, enterprise and on-device demand, which would make memory structurally LESS hyperscaler… |
| 🔴 AVGO | the Street-high forecast and a BELOW-consensus forecast differ by one unobservable assumption on identical volumes | Action: $/GW is now the dominant variable in every custom-ASIC forecast on this wiki and the range in active use spans ~2×. REJECT any GW-based ASIC number quoted without its $/GW rate. Standing unit rule re-applied: these are CONTENT-per-GW figures and must never be netted against project-DEBT-per-GW ($34.5bn ÷ >1GW) or build-cost-per-GW anchors. |
| 🔴 SKHYNIX | two houses now hand the 2027 HBM bit-share lead to Samsung, but the mechanism weakens the claim | Action: the falsifiable claim is "SK Hynix ships LESS than currently modelled in 2027" — NOT "Samsung ships more." That is checkable against SK Hynix's own capacity disclosures and is the cleanest test this theme can run in the next two quarters. |
| MEDIATEK | a named house now contests the part-level attribution the DC-ASIC sizing rests on | Action: part attribution is now an ASSUMPTION rather than a given. Anyone sizing MediaTek's 2027 DC-ASIC revenue off a specific part number must say so explicitly. Resolvable at the next TPU disclosure; kept as an open contest on the MEDIATEK page, not a correction. |

## Consensus PT vs spot — live pull in `reconciliation-2026-08-18-run-inbox.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
