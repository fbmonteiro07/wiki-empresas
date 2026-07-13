# Reconciliation — run-inbox 2026-07-06

New quantitative datapoints from 4 sources (GS 2Q Preview 07-05 · Bernstein ASML HNA 07-06 · SemiAnalysis NVDA backstop 07-06 · UBS Memory Monthly 07-03) reconciled vs three baselines:
1. **Prior wiki** (on disk) — most recent PT/estimate already logged on each page.
2. **Capstone house models** (on disk) — the `## Capstone estimates` block (models exist for NVDA, GOOG, TSM, ASML-peers among these names).
3. **BBG consensus** — **PENDING**: Bloomberg wrapper raised **HTTP 503 (Terminal not logged in)**. Re-run `refresh_features.py --run-estimates` (or `/wiki-consensus`) once the Terminal is up + Capstone VPN connected. No web data substituted.

SemiAnalysis is qualitative/thematic (NVDA backstop mechanics + proprietary AI-debt macro) — no PT/EPS to place against consensus; noted under CONFIRMS only.

---

## Where the new data DIVERGES

| Name | New datapoint | vs prior wiki | vs house model | vs BBG | Read |
|---|---|---|---|---|---|
| **KLAC** | GS Neutral, **PT $230** / norm EPS **$6.50** (35x), CY26 EPS **8% below Street** (07-05) | Page carries **UBS PT $1,260 / EPS $44.22** — GS is **~5.5x lower on PT, ~6.8x on EPS** | no KLAC house model | **BBG cons PT $238.55, spot $224.32; cons EPS CY26 $4.35 / CY27 $5.86 — all POST 10:1-split** | **✅ Data-integrity flag RESOLVED — split hypothesis confirmed.** GS's $230 PT ≈ cons $238.55 and GS's $6.50 norm EPS is on the same post-split scale as cons ($4.35–$5.86), i.e. GS is on the **split-adjusted basis**; the page's UBS $1,260 / $44.22 is the **pre-split** figure (~5.5×) and needs restating to the split basis. So NOT a target cut — **reclassify to CONFIRMS** (PT ≈ cons). Residual signal: GS **Neutral with CY26 EPS ~8% below Street** = a mild genuine relative-caution call (WFE mix skewed to DRAM, low inspection/metrology intensity). |
| **SKHYNIX** | UBS Buy **KRW 3.20m** (raised fr 3.00m, 07-03) vs **Bernstein OP KRW 1.15m** (07-06) | prior wiki UBS **KRW 2.25m** (05-20) → UBS keeps raising | no house model | **BBG cons PT KRW 3.42m (spot KRW 1.83m)** | **UBS KRW 3.20m ≈ just below cons; Bernstein KRW 1.15m ~66% below cons** — the Street sits with UBS's earnings-power frame, not Bernstein's 1.5× 2-yr-fwd BVPS book multiple. Real debate on valuing a peak-cycle Korean memory name — track which frame the market pays. (Bernstein garbled line "KR 3,300,000" excluded.) |
| **SAMSUNG** | UBS "Key Call" Buy **KRW 550k** (fr 400k, 07-03) vs **Bernstein OP KRW 225k** common (07-06) | prior wiki UBS **KRW 400k** (05-20) | no house model | **BBG cons PT KRW 504.9k (spot KRW 257.5k)** | **UBS KRW 550k ~+9% above cons; Bernstein KRW 225k ~55% below cons.** Same UBS-earnings-power vs Bernstein-BVPS split as SK Hynix; Street ≈ UBS frame. (Bernstein garbled "KRW 440,000" excluded.) |
| **MU** | UBS Buy **$1,625** (07-03) vs **Bernstein OP $1,300** (07-06) | — | no MU house model | **BBG cons PT $1,564 (spot $940.62); cons EPS CY26 $96.51 / CY27 $164.51 (hi 234.04)** | **UBS $1,625 ~+4% above cons; Bernstein $1,300 ~17% below cons** — consensus converges near UBS. Both bullish; magnitude gap = how much peak-DRAM upcycle each capitalizes. |
| **WDC** | GS **Neutral**, PT **$650 (fr $400, +63%)** (07-05) | prior GS $400 | no house model | **BBG cons PT $599.13 (spot $557); cons CY27 EPS $22.03 (hi 27.99)** | **Rating-vs-PT tension**: GS $650 is ~+8.5% above cons yet rating held Neutral, GS explicitly prefers Buy-rated STX to take near-term share. Bullish HDD tape (WDC +240% YTD vs SOXX +103%) but GS not chasing — relative-value caution flag. |
| **ASML** | Bernstein OP **PT €2,300 (fr €1,700, +35%)**, EPS basis €49.2, P/E 40x; EUV units **91/113** '27/'28 (07-06) | prior Bernstein €1,700 | house EPS **2027E $56.85 / 2028E $68.74, "well above consensus (~$34.87)"** | **BBG cons PT (ASML NA) €1,756; cons EPS CY26 €31.92 / CY27 €44.69 (hi 53.21)** | Bernstein PT €2,300 is +31% above cons (Street-high); its €49.2 EPS basis sits above cons €44.69 toward the €53.21 street-high. **Note the on-page "cons ~$34.87" was stale — fresh CY27 cons is €44.69.** House 2027E €56.85 is above even the street-high — the standing ASML above-Street edge, reinforced. |

## CONFIRMS — no action

| Name | New datapoint | Baseline check | Note |
|---|---|---|---|
| **TSM** | Bernstein OP **PT $430** = 20× fwd Q5-8 EPS **NT$139** (07-06) | house **2027E EPS NT$143.5**; BBG cons per-share ≈ NT$130 (ADR NT$649.85 ÷5) | Bernstein's NT$139 ≈ house NT$143.5 and just above cons NT$130 → earnings-power views aligned. No edge vs house. |
| **GOOG** | UBS HBM-equiv **TPU units 4.2m'26 / 9.1m'27** (raised, 07-03) | house **compute ~4.6→7.75 GW '26/'27E**; house 2027E EPS $16.20 > cons ~$14.5 | Different unit (chips vs GW) but same steep-ramp direction; corroborates house TPU thesis. UBS note has no GOOG EPS to reconcile. |
| **NVDA** | SemiAnalysis: market **still materially below its Accelerator Model on 2H'26 shipments/revenue** (07-06, qualitative) | house model **rev $216B→$407B→$661B '25/26/27E** (already above Street) | Qualitatively **confirms the house "Street too low" lean**. Backstop mechanics (take-or-pay guarantee, AA/Aa2, revenue-share) additive; AI-debt macro (>$7T '29, ~$11.1T cum capex) is SemiAnalysis-proprietary, not a consensus-comparable metric. |
| **AMD** | GS Buy **PT $640 (fr $450, +42%)**; 2027 EPS **$14.50, 13% above Street** (07-05) | no AMD house model; BBG cons PT $519.62, CY27 EPS $13.27 (hi 19.41) — GS $640 / $14.50 above cons +23% / +9% | Large PT raise + explicitly-above-Street EPS — consistent with the bullish server-CPU/MI450 narrative already on the page. Above-Street but flagged by GS itself; monitor vs consensus when BBG returns. |
| **AMAT / LRCX / TER** | GS Buy PT raises **$520→$645 / $290→$380 / $350→$465**; CY26 EPS **+6% / +3% / +2% above Street** (07-05) | no house models; BBG cons PT AMAT $615 / LRCX $373 / TER $408 — GS $645 / $380 / $465 modestly above cons | WFE upcycle PT raises with modest above-Street EPS — in line with the semicap-wfe thesis (2028 visibility, DRAM/WFE pull-ins). No divergence beyond direction. |
| **SNDK / STX** | GS Buy PT **$1,200→$2,200 / $700→$960**; SNDK CY26 EPS **>~30% above Street** (07-05) | no house models; BBG cons PT SNDK $2,222 (GS $2,200 ≈ cons) / STX $966 (GS $960 ≈ cons); SNDK CY26 EPS cons $146.9 | Storage/NAND upcycle; SNDK's >30%-above-Street EPS is the notable one — reconcile vs consensus when BBG up. |
| **CDNS / ARM / QCOM / MCHP / NXPI / ON / TXN** | GS PTs $410 / $150 / $180 / $115 / $325 / $95 / $200 (07-05) | prior wiki (QCOM fr $145, ON fr $80); BBG cons PT CDNS $395 / ARM $301 / QCOM $229 / MCHP $116 / NXPI $316 / ON $114 (TXN n/a) — GS ARM $150, QCOM $180, ON $95 sit BELOW cons | Analog/EDA/mobile marks broadly in line with existing page views; QCOM/ON PT-up-rating-Neutral noted but modest. No standalone edge. |

---

### Follow-ups — ✅ RESOLVED 2026-07-13
- **BBG PENDING column filled** (estimates.json asof 2026-07-13; target prices via BEST_TARGET_PRICE). ASML edge reinforced (Bernstein €2,300 / house €56.85 EPS both well above cons €44.69; cons PT €1,756). SK Hynix / Samsung / MU cross-broker spread anchored: cons sits with **UBS's earnings-power marks**, not Bernstein's book-multiple. **AMD** GS $640 / 2027 EPS $14.50 confirmed above cons ($519.62 PT +23% / $13.27 EPS +9%). **SNDK** GS $2,200 ≈ cons $2,222; the >30%-above-Street CY26 EPS is on GS's own number vs cons $146.9.
- **KLAC GS basis VERIFIED** — GS $230 / $6.50 is the **10:1-split-adjusted** basis (cons PT $238.55, cons EPS $4.35–$5.86 confirm it); NOT an extraction artifact or a target cut. The page's UBS $1,260 / $44.22 is pre-split and should be restated to the split basis.

_BBG column resolved 2026-07-13 — estimates.json asof 2026-07-13; consensus target prices pulled live via BEST_TARGET_PRICE (Bloomberg wrapper)._
