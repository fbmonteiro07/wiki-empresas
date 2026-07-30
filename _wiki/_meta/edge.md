# Edge tracker — house vs Street

_Generated 2026-07-30 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 10.00 | +92% |
| COHR | Revenue $bn | 2027 | 16.60 | 11.20 | +48% |
| LITE | EPS | 2027 | 30.02 | 23.90 | +26% |
| COHR | EPS | 2026 | 8.27 | 6.82 | +21% |
| NVDA | EPS | 2027 | 15.44 | 12.87 | +20% |
| GOOG | Revenue $bn | 2026 | 505.00 | 426.70 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.40 | +18% |
| NVDA | Revenue $bn | 2027 | 661.00 | 567.10 | +17% |

## Curated divergences — latest reconciliation (`reconciliation-2026-07-30.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| META | Q2'26 call validates the house cost side: total costs +55% y/y; $2.40B legal + $1.18B May-RIF severance; **3P AI token costs newly named as a P&L driver** (META Q2'26 call, 2026-07-29) | House **−3.0% on EPS**, **+1.8% on revenue**. ⚠️ **Correction of magnitude:** the body's −11.5% came off the **fiscal 1FY annual-override** pull (EPS $36.97); on the tracker's **CY quarterly-sum** basis the gap is −3.0%. Same date, same period (META's FY = CY), ~$3.25 apart. The direction holds — house still below Street on EPS while above on revenue — but the body's "cleanest same-basis divergence in the run" **overstates it**; the ~$4/share consensus-cut vector is not supported on the CY basis. Both marks retained. |
| META | **NO FY27 capex guide** — Li: "we aren't providing a specific outlook for 2027 CapEx at this time" (call, 2026-07-29); JPM (Anmuth) 2027 capex est **$243B, +70% y/y** (2026-07-30) | ⚠️ **Sign reversal vs the body.** Live CY-basis consensus **$206.3bn** lands **on** the ~$200-205bn "Street–JPM" mark the body proposed retiring, and ~$23bn **above** the fiscal 2FY pull ($183.0bn) it argued from. Consensus has **risen** ($198.2bn → $206.3bn), not come down. **Do not retire the $200-205bn mark.** Against $206.3bn: JPM's $243B is **+18%**, Redburn's ~$145bn is **−30%**, Bernstein's $250bn+ is **+21%** — the ~$105bn spread survives the print untested, as the body says. |
| MSFT | CY26 capex **~$175B**, "CY26 investment expectations remain unchanged" — a finance→operating lease reclass on a 15→25-yr useful-life extension, **not a cut**; Q1FY27 **>$50B**; no FY27 dollar figure (MSFT 4QFY26 call, 2026-07-29) | **(a) CONFIRMED:** even after the definitional reduction, mgmt's ~$175B sits **~$18bn ABOVE** the CY26 consensus mean and still **below** street-high $182.4bn — the Street models less capex than the company intends to spend. **(b) Partly de-escalated:** the FY27 bogeys (BofA $243.5B · UBS $255-260B · JPM ~$260B · MS-Altimeter CY27 $276B) are **not** "far above" consensus on the CY basis — they sit between the CY27 mean **$208.0bn** and street-high **$260.8bn**, i.e. at the top of a range the Street already carries, and only MS-Altimeter is through the high. Still struck on the **pre-reclass** definition, so the bridge remains **blocking** and the MSFT capex edge stays **unquantified, not resolved**. |
| MSFT | Q4 **OCF $55.4B (+30%)**, **FCF POSITIVE $19.6B**; **FY27 explicitly guided FCF-positive** (call, 2026-07-29) | A binary directional call, resolved against the bears by **management guidance**, not by consensus — and no consensus line exists to place it against, so this cannot be scored off BBG at all. Weakens the funding-gap/bond-debut thread by removing the near-term trigger, without contradicting it. → log to `_meta/outcomes.md` (UBS −$21B FY27 FCF, bear lost). |
| MSFT | Q4 EPS **$4.74** vs cons $4.24 / UBSe $4.41, including **$0.27 of discrete benefit** — largest piece a **$3.2B gain on the Anthropic investment**; clean ≈**$4.47** (call, 2026-07-29) | Still a beat on both marks, so not a miss dressed as a beat — but **+$0.27 of a +$0.50 headline beat is non-operating and its largest component is a mark on an unlisted holding**. A reported quarter cannot be placed against forward consensus; the flag stands on its own. Any FY27 EPS bridge starts from **~$4.47, not $4.74**. Asymmetry retained: MSFT **sizes the Anthropic gain and never sizes the OpenAI drag**. |
| LITE | **TD Cowen $990 → $800** (first PT *cut* logged on this page) · UBS re-affirmed hold · Citi Buy $1,100 + catalyst watch · quoted full range **$900-$1,400** (2026-07-29) | TD Cowen's $800 is **−29% vs the consensus mean** — a genuine street-low-side mark, unusually wide dispersion. ⚠️ But consensus implies **+63% from spot $693.24**, not the **+87%** the body computed off $602.35 (the **pre-print 07-29 close**; LITE has since moved +15.1%). **House-vs-consensus CONFIRMS the body's calendarization almost exactly:** on the CY basis house CY26E $12.81 is **−1.8%** vs $13.08 and CY27E $30.02 is **+25.6%** vs $23.90 — in line on the current year, above on the out-year, *not* the +57% a naive $12.81-vs-fiscal-$8.16 comparison implies. The **$900-$1,400 range still needs its definition confirmed** before citing. |
| NBIS | SemiAnalysis: **DataOne campus, phased and expandable to 300 MW**, paired with **Bloom Energy behind-the-meter fuel cells** (2026-07-29) | 300 vs 400 MW, fuel cells vs reciprocating gas engines, different counterparty framing. May be two sites, two phases, or one site at different vintages. **Both marks left standing; neither adopted.** BBG is structurally no help here — this is resolvable only from primary filings/permits. **Do NOT mix these into any GW build-up** (facility GW ≠ IT-load GW). |
| SNAPSHOTS | All 97 page Snapshot blocks rendered **`asof` BLANK**; META's capex line flagged stale (this report, item 8) | **Root-caused and fixed:** `build_snapshot.py` read a per-company **`revisions.asof`** key that exists on **0 of 97** companies, so every block had *always* rendered blank — re-running alone would never have fixed it. Now falls back to the `estimates.json` fetch stamp. ⚠️ **Second correction: the body's directional read does not hold.** On a like-for-like CY basis consensus capex **ROSE** on both years ($144.7bn → $147.1bn CY26; $198.2bn → $206.3bn CY27) — "the Street has been CUTTING META capex into the print" was an artifact of comparing a **CY-basis snapshot against a fiscal-annual-override pull**. Note also that CY26 consensus **$147.1bn is now ABOVE the $145B top of the narrowed guide**, which is the opposite of the body's "consensus sits on the ~$137.5bn midpoint". |

## Consensus PT vs spot — live pull in `reconciliation-2026-07-30.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
