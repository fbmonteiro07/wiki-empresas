# Reconciliation — run-inbox 2026-07-14

_New quantitative datapoints from the 12-file batch vs three baselines: (1) prior wiki comments on disk, (2) Capstone house models (`_data/house.json`, asof 2026-07-14), (3) BBG consensus._
**BBG column = PENDING this run** — Bloomberg Terminal not logged in (wrapper returned HTTP 503). Re-run `refresh_features.py --run-estimates` (or `wiki-consensus`) once the Terminal + Capstone VPN are back to fill it. On-disk baselines (1) + (2) done live below.

---

## DIVERGES (the alpha)

| Name | New datapoint (source) | vs prior wiki | vs house model | BBG |
|---|---|---|---|---|
| **SKHYNIX** | Mirae **Buy, TP W4,200,000** + **2026F OP W266,817bn** (Mirae, 07-14) | New **street-high TP** (ties Jefferies), vs dispersion W2,221,000 (JPM 07-10) → W3,590,000 (BofA); Bernstein W3,300,000, UBS W3,200,000, MS W2,600,000 | no house model | PENDING |
| **SKHYNIX** | Mirae **2026F OP W266,817bn (~3% BELOW consensus W275,793bn)** yet carries street-high TP (Mirae, 07-14) | **Estimate/rating tension** — below-consensus '26 OP + above-consensus TP. Bull case rests on '27 (OP +46% to W388,855bn) not '26 | — | PENDING (cons on page: W275,793bn) |
| **META** | JPM **capex $142.1B'26 / $202.1B'27** (JPM Anmuth, 07-14) | Above the capex trajectory implied by prior desks | House **$131B'26 / $170B'27** → JPM **~9%/~19% ABOVE house** | PENDING |
| **META** | JPM **GAAP EPS '27 $34.19** (JPM, 07-14) | — | House **$38.24** → JPM **~11% BELOW house** (consistent w/ its higher capex/D&A) | PENDING |
| **META** | JPM **Neutral, PT $725** (JPM, 07-14) | **Lone Neutral / lowest PT** on a page clustered MS $775 / WF $765 / BofA $835 / Citi $850 | — | PENDING |
| **GOOG** | JPM **GAAP EPS '27 $14.34** (JPM, 07-14) | — | House **$16.20 (diluted)** → house **~13% above** JPM GAAP; basis differs (GAAP vs house diluted) | PENDING |
| **GOOG** | JPM **rev '27 $604.5B** (JPM, 07-14) | — | House **$641B** → JPM **~6% below** house | PENDING |
| **NVDA** | MS **2027E GM 73%** (MS · Moore, 07-14) | Below mgmt mid-70s guide | House **~74%** → MS **~1pt below** house & below mgmt | PENDING |
| **AAPL** | MS **FY27e EPS $10.30** (MS · Woodring, 07-14) | Matches MS/06-16 ($10.30) & = JPM base but > JPM $9.85 07-07 read | House **$11.11** → house **~8% above** MS (both Sep-FY) | PENDING |
| **RDDT** | JPM **Neutral $200** (JPM, 07-14) | **Corrected** page's prior *inferred* "JPM OW"; published rating is Neutral | no house model | PENDING |

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
