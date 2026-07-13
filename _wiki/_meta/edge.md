# Edge tracker — house vs Street

_Generated 2026-07-13 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 9.79 | +96% |
| COHR | Revenue $bn | 2027 | 16.60 | 11.10 | +50% |
| LITE | EPS | 2027 | 30.02 | 23.69 | +27% |
| GOOG | Revenue $bn | 2027 | 641.00 | 512.40 | +25% |
| COHR | EPS | 2026 | 8.27 | 6.80 | +22% |
| GOOG | Revenue $bn | 2026 | 505.00 | 421.00 | +20% |
| NVDA | EPS | 2027 | 15.44 | 12.88 | +20% |
| NVDA | Revenue $bn | 2027 | 661.00 | 561.40 | +18% |

## Curated divergences — latest reconciliation (`reconciliation-2026-07-10.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| NVDAout-yearrevenue | MS MW **$393B (FY27e) / $599B (FY28e)** (MS "NVDA NDR", 07-10) | **House ABOVE both MS and BBG cons** on the comparable out-year — house CY27 $661B vs cons $561.4B (+18%) and vs MS FY28e $599B (+10%), still below the $732B street-high. MS FY27e $393B ≈ cons CY26 $390.9B; MS FY28e $599B ~+7% above cons CY27. |
| NVDAout-yearEPS | MS MW EPS **$8.96 (FY27e) / $13.08 (FY28e)** | **House EPS ~18% above MS and +20% above BBG cons** ($15.44 vs cons $12.88, approaching the $16.59 street-high). MS FY27e $8.96 ≈ cons CY26 $8.87; MS FY28e $13.08 ≈ cons CY27 $12.88. Edge = *long-side conviction beyond the Street*; check the FY-alignment bridge before sizing. |
| AVGOAI-semisgrowth | MS: NVDA & AVGO AI both **+80% next year**, supply-constrained ("NVDA NDR", 07-10) | House 2027 AI-semis growth (**+110%**) runs **hotter than MS's "+80% next year"**; converge closer on 2028 (+90%). House the more bullish AI-semis ramp; BBG carries no AI-semis-segment line, only total-company (house ≈ cons on total EPS — see 07-02). |
| MediaTekASICrevenue | GS: **2027 ~$20B (raised from ~$12B) / 2028 ~$52B**; HomoFish 4.5M @ ~$4,500 (27), 3M @ ~$16k + ZebraFish 1M (28); **contested 50/50 Broadcom split** (GS "TSMC preview", 07-09) | GS's **+67% upward revision** to 2027 ASIC and a Street-high-ish 2028 $52B. The **live debate is the Broadcom/MediaTek share split** (GS 50/50 vs US-investor view of higher Broadcom share) — Hock Tan (07-07) dismisses the MediaTek A8 program ("still in the Fab", "PR agency of MediaTek"). Two-sided; edge = which side of the split is right. BBG carries no ASIC-segment consensus to adjudicate. |
| TSM2Q26grossmargin | 2Q GM **~69.5-70%** vs guide 67.5% (JPM·Gokul 07-08; GS 07-09 68.5→70%) | 2Q print tracking **~70%, above guide (67.5%), BBG cons FY26 (65.7%) and house FY-avg (~66%)** → margin upside risk to full-year consensus (FY avg carries N2/overseas dilution, not fully comparable, but the 2Q level is a positive surprise). |

## Consensus PT vs spot — live pull in `reconciliation-2026-07-10.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
