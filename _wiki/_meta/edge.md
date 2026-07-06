# Edge tracker — house vs Street

_Generated 2026-07-06 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 9.75 | +97% |
| COHR | Revenue $bn | 2027 | 16.60 | 11.00 | +50% |
| LITE | EPS | 2027 | 30.02 | 23.53 | +28% |
| GOOG | Revenue $bn | 2027 | 641.00 | 512.30 | +25% |
| COHR | EPS | 2026 | 8.27 | 6.80 | +22% |
| GOOG | Revenue $bn | 2026 | 505.00 | 419.80 | +20% |
| NVDA | EPS | 2027 | 15.44 | 12.90 | +20% |
| NVDA | Revenue $bn | 2027 | 661.00 | 559.80 | +18% |

## Curated divergences — latest reconciliation (`reconciliation-2026-07-02.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| MEDIATEK | UBS **Key Call Buy, PT NT$1,800 → NT$6,500** (3.6×); TPU sales US$18/35bn 2027/28E; TPU design-service share 9%→38% 2026/27E; Cloud-ASIC EPS NT$111/219; new drivers ~83% of 2028E rev vs ~40% 2023 (UBS "Sector Keys", 07-02) | **Biggest single move in the batch.** The bull case is now "MediaTek = the #2 merchant TPU ASIC vendor." Stock +203% YTD already prices much of it; the debate is share durability vs Broadcom (which still ships 91%/62% in 26/27E). Watch for a house model init. |
| AVGO | UBS: Broadcom TPU **ship share 91% → 62%** 2026→27E as MediaTek takes 9%→38%; Google moving front-end TPU design in-house (UBS, 07-02) | **Share-cede risk to the AVGO 2028 EPS.** Not a today problem (units still grow), but the mix shift caps the TPU-driven upside. Bridge the house 2028 vs the 62%-and-falling share path. |
| META | SemiAnalysis: **>5GW contracted across Cloud & Colo in 1H26** (excl self-build), 2.5GW under construction in two campuses, 2027 capex "shockingly high," ~$10B Anthropic-type deal in talks (SemiAnalysis "Meta Compute", 07-02) | **Capex-upside / FCF-downside tension.** If Meta contracts >5GW in H1 alone and accelerates self-build, the house 2027 FCF looks high. Stress-test the FCF line against a higher 2027 capex. |
| ANTHROPIC(private) | SemiAnalysis: **+$21B net-new ARR to ~$30B** (from ~$9B), inference GM **mid-60s** (from ~38% 2025, −94% 2024), OI-profitable in 2Q ex-SBC, >$100B ARR potential by year-end (SemiAnalysis "Bedrock Mix", 05-27) | **The engine behind the AWS margin story.** The GM ramp (38%→mid-60s) is the reconciling variable — it's what lets Bedrock/Claude lift AWS EBIT +213bp. Verify the prior ARR anchor on the page; if stale, this is a step-change. |
| SKHYNIX/SAMSUNG | MS Korea: SK hynix **+KRW1,000tn** AI-DC capex (nearly doubled commitment); Samsung extended chip/HBM plan; Korea "Three Mega Projects" ~KRW2,000tn/$1.5tn (MS "S. Korea Industrial Strategy", 07-01) | **Scope divergence across brokers on one announcement** — flagged on-page, not reconciled to a single number. The signal is the capex-commitment direction, not the headline size. |

## Consensus PT vs spot — live pull in `reconciliation-2026-07-02.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
