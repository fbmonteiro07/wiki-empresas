# Reconciliation — run-inbox 2026-07-14

_New quantitative datapoints from the 12-file batch vs three baselines: (1) prior wiki comments on disk, (2) Capstone house models (`_data/house.json`, asof 2026-07-14), (3) BBG consensus._
**BBG column = PENDING this run** — Bloomberg Terminal not logged in (wrapper returned HTTP 503). Re-run `refresh_features.py --run-estimates` (or `wiki-consensus`) once the Terminal + Capstone VPN are back to fill it. On-disk baselines (1) + (2) done live below.

---

## Where the new data DIVERGES

| Name | New datapoint (source) | vs prior wiki | vs house model | BBG |
|---|---|---|---|---|
| **SKHYNIX** | Mirae **Buy, TP W4,200,000** + **2026F OP W266,817bn** (Mirae, 07-14) | New **street-high TP** (ties Jefferies), vs dispersion W2,221,000 (JPM 07-10) → W3,590,000 (BofA); Bernstein W3,300,000, UBS W3,200,000, MS W2,600,000 | no house model | Cons median TP **W3,416,433** (BBG asof 07-17) → **Mirae W4,200,000 = +23% above median** = street-high (ties Jefferies). |
| **SKHYNIX** | Mirae **2026F OP W266,817bn (~3% BELOW consensus W275,793bn)** yet carries street-high TP (Mirae, 07-14) | **Estimate/rating tension** — below-consensus '26 OP + above-consensus TP. Bull case rests on '27 (OP +46% to W388,855bn) not '26 | — | Cons CY26 OP **W275,049bn** (BBG asof 07-17, ≈ page's W275,793bn) → **Mirae W266,817bn = ~3% below cons**. Cons CY27 OP W443,271bn (hi W622,651bn). Below-cons '26 OP + street-high TP = the estimate/rating tension, confirmed. |
| **META** | JPM **capex $142.1B'26 / $202.1B'27** (JPM Anmuth, 07-14) | Above the capex trajectory implied by prior desks | House **$131B'26 / $170B'27** → JPM **~9%/~19% ABOVE house** | Cons capex CY26 **$148.7B** / CY27 **$185.2B**. JPM '26 $142.1B = **-4% below cons**; JPM '27 $202.1B = **+9% above cons**. **House $131B'26 is well below cons ($148.7B)** — house is the low outlier on '26 capex; JPM straddles cons on '27. |
| **META** | JPM **GAAP EPS '27 $34.19** (JPM, 07-14) | — | House **$38.24** → JPM **~11% BELOW house** (consistent w/ its higher capex/D&A) | Cons CY27 EPS **$37.40** (hi $40.39). JPM GAAP $34.19 = **-9% below cons** (GAAP vs non-GAAP street basis); house $38.24 = **+2% above cons** (~in-line). Divergence is JPM-vs-cons, not house-vs-cons. |
| **META** | JPM **Neutral, PT $725** (JPM, 07-14) | **Lone Neutral / lowest PT** on a page clustered MS $775 / WF $765 / BofA $835 / Citi $850 | — | Cons median PT **$816** → **JPM $725 = -11% below median** — confirmed low-end / lone Neutral. |
| **GOOG** | JPM **GAAP EPS '27 $14.34** (JPM, 07-14) | — | House **$16.20 (diluted)** → house **~13% above** JPM GAAP; basis differs (GAAP vs house diluted) | Cons CY27 EPS **$15.73** (hi $17.41). JPM GAAP $14.34 = **-9% below cons** (GAAP basis); house $16.20 = **+3% above cons**. Real gap is JPM GAAP vs cons/house, a basis story. |
| **GOOG** | JPM **rev '27 $604.5B** (JPM, 07-14) | — | House **$641B** → JPM **~6% below** house | Cons CY27 rev **$510.7B** — but BBG BEST_SALES for GOOG is **net-of-TAC** (cf. cons CY26 $423.7B ≈ BofA net $427B). JPM $604.5B & house $641B are **gross** → **gross/net basis mismatch, NOT a clean divergence** (see 07-16 screened-out). |
| **NVDA** | MS **2027E GM 73%** (MS · Moore, 07-14) | Below mgmt mid-70s guide | House **~74%** → MS **~1pt below** house & below mgmt | Cons CY27 GM **74.3%**. MS 73% = **~1.3pt below cons**, below house ~74% and mgmt mid-70s — MS trading peak margin for duration. |
| **AAPL** | MS **FY27e EPS $10.30** (MS · Woodring, 07-14) | Matches MS/06-16 ($10.30) & = JPM base but > JPM $9.85 07-07 read | House **$11.11** → house **~8% above** MS (both Sep-FY) | Cons EPS CY26 $8.90 / CY27 **$10.12** (hi $11.68). MS FY(Sep)27 $10.30 ≈ cons CY27 (slightly above); **house $11.11 = +10% above cons**, still below street-high. |
| **RDDT** | JPM **Neutral $200** (JPM, 07-14) | **Corrected** page's prior *inferred* "JPM OW"; published rating is Neutral | no house model | Cons median PT **$226** → JPM $200 = **-11% below median**, consistent with the Neutral rating. |

## CONFIRMS (no action)

| Name | New datapoint (source) | Baseline it confirms |
|---|---|---|
| **GOOG** | JPM **OW, PT $460** (street-high) (JPM, 07-14) | Confirms house bull stance (rev $505/$641B '26/'27; capex JPM $293.4B'27 ≈ house $310B) |
| **AMZN** | JPM **OW $330** (reiteration); rev '26/'27 $824/$934B; GAAP EPS $9.00/$10.38 (JPM, 07-14) | Reiteration — no prior AMZN PT superseded; no house model (vs prior wiki only) |
| **NFLX** | JPM **OW $118** (reiteration); FY26 rev $51.7B, OI margin 31.6% (JPM, 07-14) | Confirms prior OW stance |
| **UBER** | JPM **OW $110**; FY26 GBs $236.0B, Adj EBITDA $8.73B (JPM, 07-14) | Confirms prior OW |
| **SPOT** | JPM **OW $650**; FY26 GAAP EPS $14.40, rev $22.6B (JPM, 07-14) | Confirms prior OW |
| **BKNG** | JPM **OW $208** (JPM, 07-14) | **First published rating on the page** — no prior to reconcile; new anchor |
| **AAPL** | MS **OW, PT $360** (MS, 07-14) | = MS/Woodring PT already on page (06-16); conviction-deepener, not re-rating |
| **ASML** | Bernstein **PT €2300** on rising litho intensity (Bernstein, 07-06); + Euro top Buy (Redburn, 07-14) | Already folded 07-13; corroborated by Redburn strategy screen |
| **TSM** | TSMC 2Q26 beat, June rev NT$443bn +68% YoY record; backlog $2.1tr (Mirae read-through, 07-14) | Confirms house AI-foundry ramp (rev $165B'26, EPS NT$102.5) — qualitative, no estimate change |
| **AVGO** | ~10GW+ TPU 2028 (~3GW external) (Nowak, 07-14); OpenAI Jalapeño 4-yr ramp (650 Group, 07-14) | Confirms house AI-semi ramp ($251B AI semis / EPS $35.96 by 2028) |
| **LRCX / LITE / COHR / APH / BESI** | Redburn strategy "top Buy" inclusions w/ 6-mo RoCE/FCF/sales deltas (Redburn, 07-14) | Screen-level confirmation; existing single-name PTs (e.g. Redburn LRCX $420, LITE $1,270) retained — no drift |
| **ANET** | Ethernet switching TAM >$200B before mid-2030s (from ~$45B); AI-net ~$300B (650 Group, 07-14) | TAM datapoint, no PT — confirms structural bull |

## Private names (vs prior wiki only — no BBG/house)

| Name | New datapoint | Note |
|---|---|---|
| **ANTHROPIC** | Platform architecture knowledge→execution→coordination (Sequoia, 07-14); majority Claude prod tokens on Google TPU, Trainium2 serves Sonnet not Opus/Fable, GLM 5.2 codegen threat (Archera, 07-13) | Qualitative; no financials to reconcile |
| **OPENAI** | Incidental only (Redburn) — not patched | — |

---

### Watch-items surfaced
1. **META capex is the debate.** JPM models Meta capex **materially above house** ($202B vs $170B '27) and takes EPS **below** house — the only Neutral desk. If house capex proves too low, JPM's Neutral is the right side. Cross-check house `Modelo Meta pós 2Q26.xlsm` capex line into 2H26 (JPM also models a **new $40B Meta debt raise 2H26** per Nowak).
2. **SK Hynix — below-consensus '26 OP + street-high TP.** Whole bull case is back-end-loaded to '27 (+46% OP). The ~W2m PT dispersion across desks is itself the signal; watch which estimate anchor the market adopts post-2Q26 print.
3. **GOOG EPS basis gap.** JPM GAAP '27 $14.34 vs house diluted $16.20 — reconcile the GAAP/non-GAAP + share-count bridge before treating as a real divergence.
4. **NVDA GM into 2027.** MS 73% sits below mgmt mid-70s + house ~74% — MS is trading peak margin for duration (HBM4 renegotiation ~1yr out per Moore NDR). Watch the guide.

_BBG column resolved 2026-07-17 — estimates.json asof 2026-07-17 (median targets via BEST_TARGET_PRICE wrapper pull same date)._
