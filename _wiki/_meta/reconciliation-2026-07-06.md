# Reconciliation — run-inbox 2026-07-06

New quantitative datapoints from 4 sources (GS 2Q Preview 07-05 · Bernstein ASML HNA 07-06 · SemiAnalysis NVDA backstop 07-06 · UBS Memory Monthly 07-03) reconciled vs three baselines:
1. **Prior wiki** (on disk) — most recent PT/estimate already logged on each page.
2. **Capstone house models** (on disk) — the `## Capstone estimates` block (models exist for NVDA, GOOG, TSM, ASML-peers among these names).
3. **BBG consensus** — **PENDING**: Bloomberg wrapper raised **HTTP 503 (Terminal not logged in)**. Re-run `refresh_features.py --run-estimates` (or `/wiki-consensus`) once the Terminal is up + Capstone VPN connected. No web data substituted.

SemiAnalysis is qualitative/thematic (NVDA backstop mechanics + proprietary AI-debt macro) — no PT/EPS to place against consensus; noted under CONFIRMS only.

---

## DIVERGES — the alpha

| Name | New datapoint | vs prior wiki | vs house model | vs BBG | Read |
|---|---|---|---|---|---|
| **KLAC** | GS Neutral, **PT $230** / norm EPS **$6.50** (35x), CY26 EPS **8% below Street** (07-05) | Page carries **UBS PT $1,260 / EPS $44.22** — GS is **~5.5x lower on PT, ~6.8x on EPS** | no KLAC house model | PENDING | **⚠ Data-integrity flag, not a real Street-low.** GS's $230=35×$6.50 is internally consistent but on a wildly different per-share base than the page's UBS figures and vs where KLA trades (~$1,000+). Almost certainly a **split-adjusted / normalized basis** (or extraction convention) mismatch. Logged as-printed; **needs human verification before any comp use** — do NOT treat $230 as a genuine target cut. Separately, GS holds **Neutral while CY26 EPS 8% below Street** → genuine relative-caution call (WFE mix skewed to DRAM, low inspection/metrology intensity). |
| **SKHYNIX** | UBS Buy **KRW 3.20m** (raised fr 3.00m, 07-03) vs **Bernstein OP KRW 1.15m** (07-06) | prior wiki UBS **KRW 2.25m** (05-20) → UBS keeps raising | no house model | PENDING | **UBS ≈ 2.8× Bernstein** on nearly the same date. Pure methodology gap: UBS earnings-power/upcycle framing vs Bernstein **1.5× 2-yr-fwd BVPS** book multiple. Real debate on how to value a peak-cycle Korean memory name — track which frame the market pays. (Bernstein garbled summary line "KR 3,300,000" excluded.) |
| **SAMSUNG** | UBS "Key Call" Buy **KRW 550k** (fr 400k, 07-03) vs **Bernstein OP KRW 225k** common (07-06) | prior wiki UBS **KRW 400k** (05-20) | no house model | PENDING | **UBS ≈ 2.4× Bernstein.** Same UBS-earnings-power vs Bernstein-1.6×-BVPS split as SK Hynix. (Bernstein garbled "KRW 440,000" excluded.) |
| **MU** | UBS Buy **$1,625** (07-03) vs **Bernstein OP $1,300** (07-06) | — | no MU house model | PENDING | **UBS ~25% above Bernstein**, adjacent dates. Both bullish; magnitude gap = how much peak-DRAM upcycle each capitalizes. |
| **WDC** | GS **Neutral**, PT **$650 (fr $400, +63%)** (07-05) | prior GS $400 | no house model | PENDING | **Rating-vs-PT tension**: +63% PT while rating held Neutral, GS explicitly prefers Buy-rated STX to take near-term share. Bullish HDD tape (WDC +240% YTD vs SOXX +103%) but GS not chasing — relative-value caution flag. |
| **ASML** | Bernstein OP **PT €2,300 (fr €1,700, +35%)**, EPS basis €49.2, P/E 40x; EUV units **91/113** '27/'28 (07-06) | prior Bernstein €1,700 | house EPS **2027E $56.85 / 2028E $68.74, "well above consensus (~$34.87)"** | PENDING | Bernstein's big topline/PT raise runs **in the same direction as (and is corroborated by) the house's well-above-consensus EPS**. Flag as DIVERGES-vs-Street (house + Bernstein both materially above cons) — this is the standing ASML edge, now reinforced. |

## CONFIRMS — no action

| Name | New datapoint | Baseline check | Note |
|---|---|---|---|
| **TSM** | Bernstein OP **PT $430** = 20× fwd Q5-8 EPS **NT$139** (07-06) | house **2027E EPS NT$143.5**; BBG PENDING | Bernstein's NT$139 ≈ house NT$143.5 → earnings-power views aligned. No edge vs house. |
| **GOOG** | UBS HBM-equiv **TPU units 4.2m'26 / 9.1m'27** (raised, 07-03) | house **compute ~4.6→7.75 GW '26/'27E**; house 2027E EPS $16.20 > cons ~$14.5 | Different unit (chips vs GW) but same steep-ramp direction; corroborates house TPU thesis. UBS note has no GOOG EPS to reconcile. |
| **NVDA** | SemiAnalysis: market **still materially below its Accelerator Model on 2H'26 shipments/revenue** (07-06, qualitative) | house model **rev $216B→$407B→$661B '25/26/27E** (already above Street) | Qualitatively **confirms the house "Street too low" lean**. Backstop mechanics (take-or-pay guarantee, AA/Aa2, revenue-share) additive; AI-debt macro (>$7T '29, ~$11.1T cum capex) is SemiAnalysis-proprietary, not a consensus-comparable metric. |
| **AMD** | GS Buy **PT $640 (fr $450, +42%)**; 2027 EPS **$14.50, 13% above Street** (07-05) | no AMD house model on page; BBG PENDING | Large PT raise + explicitly-above-Street EPS — consistent with the bullish server-CPU/MI450 narrative already on the page. Above-Street but flagged by GS itself; monitor vs consensus when BBG returns. |
| **AMAT / LRCX / TER** | GS Buy PT raises **$520→$645 / $290→$380 / $350→$465**; CY26 EPS **+6% / +3% / +2% above Street** (07-05) | no house models; BBG PENDING | WFE upcycle PT raises with modest above-Street EPS — in line with the semicap-wfe thesis (2028 visibility, DRAM/WFE pull-ins). No divergence beyond direction. |
| **SNDK / STX** | GS Buy PT **$1,200→$2,200 / $700→$960**; SNDK CY26 EPS **>~30% above Street** (07-05) | no house models; BBG PENDING | Storage/NAND upcycle; SNDK's >30%-above-Street EPS is the notable one — reconcile vs consensus when BBG up. |
| **CDNS / ARM / QCOM / MCHP / NXPI / ON / TXN** | GS PTs $410 / $150 / $180 / $115 / $325 / $95 / $200 (07-05) | prior wiki (QCOM fr $145, ON fr $80); BBG PENDING | Analog/EDA/mobile marks broadly in line with existing page views; QCOM/ON PT-up-rating-Neutral noted but modest. No standalone edge. |

---

### Follow-ups
- **Re-run BBG** (`/wiki-consensus` or `refresh_features.py --run-estimates`) once Terminal + VPN are up to fill the PENDING column — priority names: ASML (house vs cons edge), AMD/SNDK (above-Street EPS), SK Hynix/Samsung/MU (cross-broker PT spread).
- **Verify KLAC GS basis** — resolve whether GS's $230/$6.50 is split-adjusted or an extraction artifact before it feeds any comp.
