# Edge tracker — house vs Street

_Generated 2026-08-20 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

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

## Curated divergences — latest reconciliation (`reconciliation-2026-08-19.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| 1 | **SKHYNIX** | 🔴 **A BELOW-THE-LINE disagreement, which is what makes it interesting.** JPM is **−0.7% on revenue and −1.1% on EBIT** yet +14.1% on EPS — arithmetically impossible from operations, so it lives in **tax rate, non-operating income or share count**. If JPM is right, the Street's CY26 EPS is ~12% too low on essentially identical operating forecasts. **Action: pull the published JPM note to identify the line.** |
| 2 | **SAMSUNG** | 🔴 **Same shape, same analyst, same year — and the parallel is the signal.** JPM is −0.02% on revenue and −1.5% on EBIT, +9.5% on EPS. **Two Korean memory models from one house, both ON consensus at the operating line and both 10-14% ABOVE it on EPS, points to one systematic house assumption below the operating line rather than two coincidences.** Highest-conviction item in this run. |
| 3 | **SAMSUNG** | 🔴 **The cleanest tradeable divergence, and it SURVIVES every adjustment.** ~W50tn of revenue and ~W35tn of profit below the Street, and it is **not** a margin call (margins within 50bp) — JPM simply has less Samsung revenue in the out-year. Note it runs *against* item 2: JPM is more conservative on 2027 operations while more generous below the line, so the two partly cancel at EPS and the headline EPS delta understates the real disagreement. |
| 4 | **SAMSUNG** | 🔴 **Widest read-through in the run, and it is a MIX call not a level call: JPM is ABOVE consensus on Samsung capex and BELOW on SK Hynix capex (−3.5%/−4.2%).** More Samsung spend, less Hynix spend than the Street. Directionally positive for tools levered specifically to Samsung. **Cross-check → [[AMAT]], [[LRCX]], [[KLAC]], [[ASML]], [[TOKYOELEC]], `themes/semicap-wfe`.** |
| 5 | **KIOXIA** | 🔴 **A wiki-internal divergence, i.e. the page was wrong.** The primary transcript beat the relay on both lines. **More important is the framing: the page called it "a modest miss on a lowered bar" — the company BEAT its own guidance on revenue, OP, net income AND EPS; the miss was only vs the higher ¥1.372tn consensus.** Corrected on the page, old values in `## Changelog`. |
| 6 | **KIOXIA** | 🔴 **The relayed cross-supplier corroboration was FABRICATED — there is no Samsung reference anywhere in the call.** The page then built a "Samsung's 60-70% LTA coverage disclosed the same week" read-across on top of it. **The bit-growth leg of that read-across is unsupported and has been withdrawn.** |
| 7 | **KIOXIA** | 🔴 **A thesis-level qualifier that every broker relay dropped.** Not a captive fab and modest against a ¥4.7tn balance sheet, but Kioxia is now taking DRAM equity exposure *and* building DRAM inventory. The "clean NAND pure-play" framing needs a caveat. |
| 8 | **KIOXIA** | ⚠️ **Possibly not a cut** — the Investor Day figure may be a multi-year average against an FY26 point. **Flagged as two different numbers that must not be quoted interchangeably**, not resolved. |
| 9 | **SNDK** | 🔴 **The company has taken a side, and on a DIFFERENT and larger target than the page was tracking: eSSD + HBM displacing SYSTEM DRAM (DDR/SOCAMM), not HBM.** Cross-read **[[MU]], [[SAMSUNG]], [[SKHYNIX]]** conventional-DRAM demand and **[[NVDA]]** platform BOM. ⚠️ Vendor lab data, single workload, no methodology, obvious incentive — directional only, **not a sizing input**. |
| 10 | **SNDK** | 🔴 **Sharpens the framing into a dependency: HBF upside is additive ONLY IF the latent productivity headroom is real. Management asserted it and refused to size it.** The same sentence also undercuts the *bull* supply-sink trade (HBF tightening NAND, lifting industry pricing) that Bernstein's read implies. **Now the single most important unquantified claim on the SNDK page.** |
| 11 | **themes/optical-cpo** | ✅ **Attribution resolved, and the page's own guess corrected.** The two 08-18 blocks are **two different sources on two different axes** (SemiAnalysis scale-up, FUNDA scale-out) — they were never corroboration of each other, which is how the page had been reading them. **GF Securities (08-19) is the first genuinely independent third vote, and the first with ratings.** |
| 12 | **LITE / COHR** | ⚠️ **The Street is genuinely split on the PAIR, not on the category.** GF sides with LITE; MS and Jefferies side with COHR. **Do not over-read: GF carries no PT, no estimates and no COHR-specific model work — its COHR content is two product lines in a beneficiary list.** A relative-preference mark only. |
| 13 | **Unitree (688836.SS, off-coverage)** | ⚠️ **NOT a divergence — a base mismatch, and it matters.** The TP is struck off the **CNY150.80 IPO price**, not the post-debut tape. **A +492% debut may already have exceeded the target.** Anyone comparing TP to price must re-base first. No BBG/house baseline (Chinese A-share, off coverage) → reconciled vs prior wiki comment only. |
| 14 | **TSLA** | ⚠️ **Reframes the Optimus cost argument: a shipping $28k robot at 60% GM versus a $20k aspiration not yet built at volume.** Nomura also flags Optimus Gen-3 pilot production as a risk to its OWN Buy — so the read runs both ways. |

## Consensus PT vs spot — live pull in `reconciliation-2026-08-19.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
