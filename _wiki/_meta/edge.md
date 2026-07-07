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

## Curated divergences — latest reconciliation (`reconciliation-2026-07-06.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| KLAC | GS Neutral, **PT $230** / norm EPS **$6.50** (35x), CY26 EPS **8% below Street** (07-05) | **⚠ Data-integrity flag, not a real Street-low.** GS's $230=35×$6.50 is internally consistent but on a wildly different per-share base than the page's UBS figures and vs where KLA trades (~$1,000+). Almost certainly a **split-adjusted / normalized basis** (or extraction convention) mismatch. Logged as-printed; **needs human verification before any comp use** — do NOT treat $230 as a genuine target cut. Separately, GS holds **Neutral while CY26 EPS 8% below Street** → genuine relative-caution call (WFE mix skewed to DRAM, low inspection/metrology intensity). |
| SKHYNIX | UBS Buy **KRW 3.20m** (raised fr 3.00m, 07-03) vs **Bernstein OP KRW 1.15m** (07-06) | **UBS ≈ 2.8× Bernstein** on nearly the same date. Pure methodology gap: UBS earnings-power/upcycle framing vs Bernstein **1.5× 2-yr-fwd BVPS** book multiple. Real debate on how to value a peak-cycle Korean memory name — track which frame the market pays. (Bernstein garbled summary line "KR 3,300,000" excluded.) |
| SAMSUNG | UBS "Key Call" Buy **KRW 550k** (fr 400k, 07-03) vs **Bernstein OP KRW 225k** common (07-06) | **UBS ≈ 2.4× Bernstein.** Same UBS-earnings-power vs Bernstein-1.6×-BVPS split as SK Hynix. (Bernstein garbled "KRW 440,000" excluded.) |
| MU | UBS Buy **$1,625** (07-03) vs **Bernstein OP $1,300** (07-06) | **UBS ~25% above Bernstein**, adjacent dates. Both bullish; magnitude gap = how much peak-DRAM upcycle each capitalizes. |
| WDC | GS **Neutral**, PT **$650 (fr $400, +63%)** (07-05) | **Rating-vs-PT tension**: +63% PT while rating held Neutral, GS explicitly prefers Buy-rated STX to take near-term share. Bullish HDD tape (WDC +240% YTD vs SOXX +103%) but GS not chasing — relative-value caution flag. |
| ASML | Bernstein OP **PT €2,300 (fr €1,700, +35%)**, EPS basis €49.2, P/E 40x; EUV units **91/113** '27/'28 (07-06) | Bernstein's big topline/PT raise runs **in the same direction as (and is corroborated by) the house's well-above-consensus EPS**. Flag as DIVERGES-vs-Street (house + Bernstein both materially above cons) — this is the standing ASML edge, now reinforced. |

## Consensus PT vs spot — live pull in `reconciliation-2026-07-06.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
