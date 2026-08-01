# Edge tracker — house vs Street

_Generated 2026-07-31 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 10.00 | +92% |
| COHR | Revenue $bn | 2027 | 16.60 | 11.20 | +48% |
| LITE | EPS | 2027 | 30.02 | 23.90 | +26% |
| COHR | EPS | 2026 | 8.27 | 6.82 | +21% |
| NVDA | EPS | 2027 | 15.44 | 12.91 | +20% |
| GOOG | Revenue $bn | 2026 | 505.00 | 426.70 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.40 | +18% |
| NVDA | Revenue $bn | 2027 | 661.00 | 568.20 | +16% |
| AAPL | EPS | 2026 | 10.12 | 8.78 | +15% |

## Curated divergences — latest reconciliation (`reconciliation-2026-07-31.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| D1 | **ASML** | ⚠ **The house model has been overtaken — sign flipped.** House is now **−5.6% / −3.3% / −8.2% BELOW consensus** and ~21% below Bernstein in 2028E. The page's standing "well above consensus (NTM ~34.87)" claim is **stale and now false**; the cited consensus anchor is itself ~€36.4/$42 today. **Action: refresh `ASML_Peers_SemiCap_v16.xlsx`.** Flag added to the page in two places. |
| D2 | **ASML** | **Street-high confirmed: +24.2% above the mean PT locally, +16.2% on the ADR.** ⚠ The two consensus PT lines don't reconcile with each other (€2,013 × 1.1527 = $2,320 vs $2,460, ~6% gap — different contributor sets); state which line you're quoting. |
| D3 | **ASML** | **The entire gap is out-year — this is a DURATION call, not a near-term-numbers call.** Consensus decays revenue growth to **+11% / +5%** in 29/30; Bernstein holds **+14% / +13%**. Near-term print risk ≈ nil (Bernstein is ~at consensus for 26-27). Falsifiable at two physical claims: DRAM EUV exposures → **26.3 MWPM by 2030** (4.5x) and blended litho intensity → **28%**. Margin split: GM gap trivial (~90bp), **OPM gap 350bp** — the disagreement is operating leverage, not pricing. |
| D4 | **ASML** | **The page's "same thesis, different multiple" framing is incomplete.** MS sits **~13% BELOW consensus** on the out-year EPS base while Bernstein sits ~16% above — roughly half the ~30% PT gap comes from the EPS base, not the 40x-vs-35x multiple. Correct that row next time it's touched. |
| D5 | **ASML** | **Upside is now 74.3%, not 84%** — don't carry 84% as a live number. The 20x claim survives: €1,434.20 / €75.25 = **19.1x** (18.1x at the note's close). |

## Consensus PT vs spot — live pull in `reconciliation-2026-07-31.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| 000660KSEquity | 1,718,000 | 3,292,948 | +92% | +92%. SK hynix — named the lead High-NA adopter. |
| 005930KSEquity | 259,000 | 488,627 | +89% | +89%. Samsung Electronics. Qualitative read-through (2× EXE:5200B, "industry reports" sourcing). |
| ASMLUSEquity | 1,629 | 2,460 | +51% | ADR line; +51% to consensus PT. ⚠ Does not reconcile with the NA line at spot FX (~6% gap) — different contributor sets. |
| ASMLNAEquity | 1,434 | 2,013 | +40% | Consensus sees +40%. Bernstein's €2,500 is **+24% above the consensus PT** — the Street-high. |
| TSMUSEquity | 404 | 549 | +36% | +36%. Qualitative read-through only (High-NA deferred to ~A10). |
| 8035JPEquity | 55,500 | 74,486 | +34% | +34%. Tokyo Electron — the correctly-routed "TEL" (see the dropped-route note). |
| INTCUSEquity | 90 | 119 | +32% | +32%. Qualitative read-through only (18A High-NA HVM validation). |
| KLACUSEquity | 183 | 234 | +28% | +28%. Bernstein has KLA **last of five** on both revenue (22%) and EPS (28%) CAGR CY25-28. |
| LRCXUSEquity | 293 | 372 | +27% | +27%. Bernstein has LAM **2nd of five** on growth (rev 28% / EPS 38%) — corroborates Lam IR's own 07-31 framing. |
| AMATUSEquity | 508 | 623 | +23% | +23%. Read-through name only — no new AMAT estimate in this note. |
