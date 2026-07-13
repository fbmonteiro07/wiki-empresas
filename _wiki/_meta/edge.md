# Edge tracker — house vs Street

_Generated 2026-07-13 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

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

## Curated divergences — latest reconciliation (`reconciliation-2026-07-10.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| NVDAout-yearrevenue | MS MW **$393B (FY27e) / $599B (FY28e)** (MS "NVDA NDR", 07-10) | **House is materially ABOVE the MS Street case** on the comparable out-year — house 2027E rev **$661B** vs MS's comparable FY28e **$599B** (~+10% house). House 2026E $407B ≈ MS FY27e $393B. |
| NVDAout-yearEPS | MS MW EPS **$8.96 (FY27e) / $13.08 (FY28e)** | **House EPS ~18% above MS** on the comparable year ($15.44 vs $13.08). Combined w/ revenue, the house NVDA model sits well above even MS's constructive OW/Top-Pick framing → our edge is *long-side conviction beyond the Street*, but check the FY-alignment bridge before sizing. |
| AVGOAI-semisgrowth | MS: NVDA & AVGO AI both **+80% next year**, supply-constrained ("NVDA NDR", 07-10) | House 2027 AI-semis growth (**+110%**) runs **hotter than MS's "+80% next year"**; house and MS converge closer on 2028 (+90%). House is the more bullish AI-semis ramp. |
| MediaTekASICrevenue | GS: **2027 ~$20B (raised from ~$12B) / 2028 ~$52B**; HomoFish 4.5M @ ~$4,500 (27), 3M @ ~$16k + ZebraFish 1M (28); **contested 50/50 Broadcom split** (GS "TSMC preview", 07-09) | GS's own **+67% upward revision** to 2027 ASIC and a Street-high-ish 2028 $52B. The **live debate is the Broadcom/MediaTek share split** (GS 50/50 vs US-investor view of higher Broadcom share) — Hock Tan (07-07) publicly dismisses the MediaTek A8 program ("still in the Fab", "PR agency of MediaTek"). Two-sided; our edge = which side of the split is right. |
| TSM2Q26grossmargin | 2Q GM **~69.5-70%** vs guide 67.5% (JPM·Gokul 07-08; GS 07-09 68.5→70%) | 2Q print tracking **~70%, above both guide and house FY-avg ~66%** → margin upside risk to the house TSM model (FY avg carries N2/overseas dilution, so not fully comparable, but the 2Q level is a positive surprise). |

## Consensus PT vs spot — live pull in `reconciliation-2026-07-10.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
