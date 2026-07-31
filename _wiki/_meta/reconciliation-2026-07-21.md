# Reconciliation — 2026-07-21 run-inbox (MS earnings-week batch + Jefferies/Redburn previews)

_Variance pass on every NEW quantitative datapoint from this run vs three baselines: (1) prior wiki comments on the page, (2) Capstone house models (`_data/house.json`, asof 2026-07-21 — only AAPL/AVGO/COHR/GOOG/LITE/META/NVDA/TSM modelled), (3) BBG consensus. **BBG live re-pull is PENDING** — Terminal returned HTTP 503 (not logged in / VPN). Used the on-disk cached snapshot `_data/estimates.json` (asof 2026-07-21, CY-calendarized EPS/rev/capex) as the consensus proxy; it carries **no target-price field**, so all PT-vs-consensus placements are PENDING the live pull. Its price column also looks stale/mismatched vs the notes' Jul-20 closes (e.g. GLW 162.41 on disk vs $153.10 note close; MSFT 397.75 vs $402.29) — treat EPS/rev as the reliable consensus columns, prices as indicative only._

Sources this run: MS "Battle of the AI Stack" (MSFT, Adam Wood); MS Corning Q2 Preview (GLW, Meta Marshall); MS MKS note; MS 2Q26 CIO Survey; MS 2Q26 internet preview (Nowak); Jefferies 2Q26 On-Cycle Preview (Thill); Redburn "One Prompt Entrepreneur" (Meta/Shop, Ball). All 07-20/07-21.

---

## DIVERGES (the alpha)

| Name | New datapoint (source) | Prior wiki | House | BBG consensus (cached 07-21) | Divergence |
|---|---|---|---|---|---|
| **META** | Redburn Buy **PT $1,000** (from $900); **2027 GAAP EPS $43.2** @23x; rev vs cons **+6/+17/+29%** (26/27/28E) via SMB-LLM ("one-prompt entrepreneur"), ~45% IRR, >$209bn ex-China TAM | Consensus-bull views on core ads; SMB-LLM optionality was thematic, un-quantified | House 2027 EPS **38.24**, rev 313, capex 170 | CY27 EPS **36.09**, rev 302.9 | **Aggressive bull.** Redburn '27 EPS $43.2 is **~13% above house / ~20% above cons**; rev +17% above cons by '27. Biggest above-Street call this run — the SMB-LLM/AI-cloud monetization is the whole gap. Watch as the bull-case anchor. |
| **AMZN** | MS Nowak **'27 capex >$300B**; AWS +34% 2Q; backlog +$100B q/q. Jefferies Top Pick, FY26 capex ~$215B | Capex/FCF-digestion debate open | (no AMZN house) | CY27 capex **233.1**, CY26 200.9 | **MS '27 capex >$300B is ~30% above cons $233B** — materially heavier AWS build than Street models. Jefferies FY26 ~$215B also ~7% above cons CY26 $201B. Capex is the divergence; the AWS re-accel (+34%) is consensus-range. |
| **SHOP** | Redburn **PT $130** (from $160), structural bear; net rev **-7% below Street by 2028E**; GP CAGR-to-2030 cut ~26%→~19%; ~50% US volume exposed to Meta SMB-LLM | Bull/mixed (JPM/DB bullish); disintermediation was tail-risk | (no house) | CY27 EPS 2.45 (Redburn '27 non-GAAP EPS $2.55 ≈ in line) | **Structural bear vs a bullish book/Street** — EPS in line but the out-year *revenue* call (-7% by '28) and halved GP CAGR is the disagreement. Mirror image of the META bull (same SMB-LLM thesis, opposite side). |
| **GOOG** | Cloud **+77% 2Q** (Nowak) / Jefferies bogey **75%+ vs Street ~65%**; compute-constrained (SpaceX ~$50/watt) | Cloud "at least 70" (JPM, 07-14) | House 2027 capex **310** vs EPS 16.20 | CY27 capex **269.4**, EPS 15.8 | Cloud-growth bogey **~10pts above Street** = bull cloud. House '27 capex $310B is **~15% above cons $269B** (pre-existing house view, corroborated by the compute-constraint narrative). |

## CONFIRMS (no action)

| Name | New datapoint (source) | Baseline check |
|---|---|---|
| **MSFT** | MS **PT $600** (cut from $650, Adam Wood assumes cov.); FY26/27/28e EPS 17.35/19.62/23.86; Jefferies FY27 capex $209B | PT cut **already logged** to Changelog by earlier wiki-ingest → confirms. FY EPS vs cached cons (CY26 17.74 / CY27 20.93) ~in line to ~6% below on out-year (FY-vs-CY basis). Jefferies capex $209B ≈ cons CY27 $197.6B. Mild. |
| **GLW** | MS EW, **PT $180**; EPS FY26/27/28e 3.09/4.15/5.53 | EPS ~2-3% below cached cons (CY26 3.19 / CY27 4.23) — in line. **Rating/PT tension worth noting:** EW but $180 PT = **+18% vs $153 close**, and MS is EW vs Street **71% OW** (note's own cons PT mean $158.87). Below-consensus *rating*, above-mean *PT*. |
| **MKS** (theme only, no page) | MS OW/Top Pick **PT $442**; SepQ rev ~$1.3bn (**above** Street $1.24bn), GM% ~48%/EPS $3.50, 50% GM late-'27 | Above-Street SepQ (rev + GM). No house/page; logged in `themes/semicap-wfe.md`. Confirms strong WFE-subsystem demand; MS "comfortable underwriting 30%+ semi growth 2027." |
| **CRM** | Adam Wood downgrade **PT $185** (folded earlier from companion note) + CIO-survey bear (in-house rebuilds, 10-20% price pushback) | CIO survey corroborates the downgrade. PT $185 vs cached cons CY26 EPS 13.42 (px 170) = cautious/~9% upside. Consistent bear. |
| **CRWV / NBIS / ORCL** | MS margin-benchmark ladder (Rev/MW + standardized GM: neoclouds floor → ORCL +32% → full-stack MSFT); Jefferies CRWV ~9x EV/CY28 EBIT vs NBIS 45x | Qualitative margin-benchmarking, no new hard PT/EPS to place vs cons. ORCL cached cons CY27 EPS 9.2. Additive; no action. |

---

## Action items
1. **Re-run BBG live** once Terminal is logged in / VPN up: `py "E:\Wiki Felipe empresas\_wiki\_tools\refresh_features.py" --run-estimates` (or `py E:/.claude/scripts/fetch_estimates.py META AMZN SHOP GOOG MSFT GLW`) to (a) confirm the cached CY EPS above and (b) get the **consensus target-price distribution** to place the Redburn META $1,000 / SHOP $130 and MS MSFT $600 / GLW $180 PTs vs the Street — the PT-placement column is the missing piece here.
2. **META vs SHOP is one paired trade** — Redburn is long META / cautious SHOP on the *same* SMB-LLM thesis. If the SMB-LLM disintermediation is right, it's the META bull anchor AND the SHOP bear anchor. Highest-conviction divergence pair this run.
3. **AMZN '27 capex** — MS >$300B vs Street $233B: name the bridge (AWS accel + custom-silicon buildout). Track into the print.
