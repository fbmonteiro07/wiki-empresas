# Reconciliation — 2026-07-10 run

New quantitative datapoints from the 07-10 ingest (8 substantive sources) reconciled vs three baselines:
**(1)** prior wiki comments (on disk), **(2)** Capstone house models (`_data/house.json`, as-of 2026-07-10), **(3)** BBG consensus.

> **BBG column = PENDING.** The Bloomberg wrapper returned **HTTP 503 — "Bloomberg connection test failed, please ensure you are logged in to Bloomberg Terminal"** (Terminal not logged in / Capstone VPN down). On-disk baselines (1) & (2) done now; re-run the BBG leg via `/wiki-consensus` or `refresh_features.py --run-estimates` once the Terminal is back. Per protocol, web data was **not** substituted for consensus.

Purely qualitative/structural inputs (SK Hynix ADR mechanics & LTA philosophy, Bernstein LTA-effectiveness math, AVGO Tomahawk/SerDes/COT commentary, INTC IMT-yield color, Samsung 2nm-share color, Chairman Chey interview) are excluded from the variance table.

---

## Where the new data DIVERGES

| Metric | New sell-side | (1) Prior wiki | (2) House model | (3) BBG | Read |
|---|---|---|---|---|---|
| **NVDA out-year revenue** | MS MW **$393B (FY27e) / $599B (FY28e)** (MS "NVDA NDR", 07-10) | MS PT $288 already logged 06-16; page carried MS ModelWare only as a thin FinTwit echo | House **2026E $407B / 2027E $661B** (calendar-shifted ~1yr vs MS FY labels) | BBG cons rev **CY26 $390.9B** (hi 417) / **CY27 $561.4B** (hi 732) | **House ABOVE both MS and BBG cons** on the comparable out-year — house CY27 $661B vs cons $561.4B (+18%) and vs MS FY28e $599B (+10%), still below the $732B street-high. MS FY27e $393B ≈ cons CY26 $390.9B; MS FY28e $599B ~+7% above cons CY27. |
| **NVDA out-year EPS** | MS MW EPS **$8.96 (FY27e) / $13.08 (FY28e)** | (as above) | House EPS **$9.26 (2026E) / $15.44 (2027E)** | BBG cons EPS **CY26 $8.87** (hi 10.12) / **CY27 $12.88** (hi 16.59) | **House EPS ~18% above MS and +20% above BBG cons** ($15.44 vs cons $12.88, approaching the $16.59 street-high). MS FY27e $8.96 ≈ cons CY26 $8.87; MS FY28e $13.08 ≈ cons CY27 $12.88. Edge = *long-side conviction beyond the Street*; check the FY-alignment bridge before sizing. |
| **AVGO AI-semis growth** | MS: NVDA & AVGO AI both **+80% next year**, supply-constrained ("NVDA NDR", 07-10) | AVGO 07-08 Sur summary already on page (same event underlies the 07-07 call) | House AI semis **$63B (26E)→$132B (27E) = +110%**, →$251B (28E) = +90% | No BBG segment line — cons is total-company only (AVGO rev **CY26 $123.0B → CY27 $189.1B, +54%**; EPS $13.59→$21.14) | House 2027 AI-semis growth (**+110%**) runs **hotter than MS's "+80% next year"**; converge closer on 2028 (+90%). House the more bullish AI-semis ramp; BBG carries no AI-semis-segment line, only total-company (house ≈ cons on total EPS — see 07-02). |
| **MediaTek ASIC revenue** | GS: **2027 ~$20B (raised from ~$12B) / 2028 ~$52B**; HomoFish 4.5M @ ~$4,500 (27), 3M @ ~$16k + ZebraFish 1M (28); **contested 50/50 Broadcom split** (GS "TSMC preview", 07-09) | Prior wiki carried GS's earlier ~$12B (2027) mark | No house model | No BBG ASIC-segment line — total-company cons (2454 TT) rev **CY26 NT$646bn → CY27 NT$1,039bn**; EPS NT$64.58 → NT$127.47 | GS's **+67% upward revision** to 2027 ASIC and a Street-high-ish 2028 $52B. The **live debate is the Broadcom/MediaTek share split** (GS 50/50 vs US-investor view of higher Broadcom share) — Hock Tan (07-07) dismisses the MediaTek A8 program ("still in the Fab", "PR agency of MediaTek"). Two-sided; edge = which side of the split is right. BBG carries no ASIC-segment consensus to adjudicate. |
| **TSM 2Q26 gross margin** | 2Q GM **~69.5-70%** vs guide 67.5% (JPM·Gokul 07-08; GS 07-09 68.5→70%) | Page tracked guide ~67.5% | House **FY26E GM ~66%** | BBG cons GM **FY26 65.7% / FY27 65.9%** (full-year) | 2Q print tracking **~70%, above guide (67.5%), BBG cons FY26 (65.7%) and house FY-avg (~66%)** → margin upside risk to full-year consensus (FY avg carries N2/overseas dilution, not fully comparable, but the 2Q level is a positive surprise). |

## CONFIRMS (no action)

| Metric | New sell-side | Baseline | Read |
|---|---|---|---|
| **TSM FY26 revenue growth** | FY26 guide lift to **+mid-to-high 30s%** (JPM/GS 07-08/09) | House 2026E **$165B (US$) = +35% vs $122B '25** | In line — house already at the top of the old guide range. |
| **NVDA price target (MS)** | MS reiterate **OW/Top Pick, PT $288** (07-10) | Prior wiki logged **MS OW $288 on 06-16** | Unchanged — NDR reaffirms, no PT move. |
| **GEV (BofA power gap)** | BofA **Buy**, US 100+GW shortfall thesis | Reconciled **2026-07-08** (this 07-10 file is a re-drop of the same note under a new slug) | Already actioned; only the accelerator-GW-ramp datapoint (~15-17→58-60 GW/yr CY25-30) was net-new. |
| **TSM 2027 capex** | GS **$78B (from $70B)**; JPM ~$220B cum 26-28 (78/85) | House model carries no explicit capex line | **BBG cons CY27 capex ≈ US$67.6B** (NT$2.20tn ÷ ~32.5) — GS/JPM $78B is ~+15% ABOVE cons; the Street's own high-end sell-side marks run above the consensus capex line. |

---

## To re-run when Bloomberg is back — ✅ DONE
`NVDA / TSM / AVGO / MU / MEDIATEK / GEV` pulled 2026-07-13. Resolution: **NVDA out-year** — BBG cons sits with MS's lower case (CY27 rev $561.4B / EPS $12.88), NOT the house $661B/$15.44; the house is +18%/+20% above cons (edge intact, below the $732B/$16.59 street-high). **MediaTek 2027 ASIC** — no BBG ASIC-segment line; total-company cons NT$1,039bn'27, GS's $20B ASIC unadjudicable at segment level.

_BBG column resolved 2026-07-13 — estimates.json asof 2026-07-13; consensus target prices pulled live via BEST_TARGET_PRICE (Bloomberg wrapper)._
