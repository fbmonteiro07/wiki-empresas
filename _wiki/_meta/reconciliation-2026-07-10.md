# Reconciliation — 2026-07-10 run

New quantitative datapoints from the 07-10 ingest (8 substantive sources) reconciled vs three baselines:
**(1)** prior wiki comments (on disk), **(2)** Capstone house models (`_data/house.json`, as-of 2026-07-10), **(3)** BBG consensus.

> **BBG column = PENDING.** The Bloomberg wrapper returned **HTTP 503 — "Bloomberg connection test failed, please ensure you are logged in to Bloomberg Terminal"** (Terminal not logged in / Capstone VPN down). On-disk baselines (1) & (2) done now; re-run the BBG leg via `/wiki-consensus` or `refresh_features.py --run-estimates` once the Terminal is back. Per protocol, web data was **not** substituted for consensus.

Purely qualitative/structural inputs (SK Hynix ADR mechanics & LTA philosophy, Bernstein LTA-effectiveness math, AVGO Tomahawk/SerDes/COT commentary, INTC IMT-yield color, Samsung 2nm-share color, Chairman Chey interview) are excluded from the variance table.

---

## DIVERGES (the alpha)

| Metric | New sell-side | (1) Prior wiki | (2) House model | (3) BBG | Read |
|---|---|---|---|---|---|
| **NVDA out-year revenue** | MS MW **$393B (FY27e) / $599B (FY28e)** (MS "NVDA NDR", 07-10) | MS PT $288 already logged 06-16; page carried MS ModelWare only as a thin FinTwit echo | House **2026E $407B / 2027E $661B** (calendar-shifted ~1yr vs MS FY labels) | PENDING | **House is materially ABOVE the MS Street case** on the comparable out-year — house 2027E rev **$661B** vs MS's comparable FY28e **$599B** (~+10% house). House 2026E $407B ≈ MS FY27e $393B. |
| **NVDA out-year EPS** | MS MW EPS **$8.96 (FY27e) / $13.08 (FY28e)** | (as above) | House EPS **$9.26 (2026E) / $15.44 (2027E)** | PENDING | **House EPS ~18% above MS** on the comparable year ($15.44 vs $13.08). Combined w/ revenue, the house NVDA model sits well above even MS's constructive OW/Top-Pick framing → our edge is *long-side conviction beyond the Street*, but check the FY-alignment bridge before sizing. |
| **AVGO AI-semis growth** | MS: NVDA & AVGO AI both **+80% next year**, supply-constrained ("NVDA NDR", 07-10) | AVGO 07-08 Sur summary already on page (same event underlies the 07-07 call) | House AI semis **$63B (26E)→$132B (27E) = +110%**, →$251B (28E) = +90% | PENDING | House 2027 AI-semis growth (**+110%**) runs **hotter than MS's "+80% next year"**; house and MS converge closer on 2028 (+90%). House is the more bullish AI-semis ramp. |
| **MediaTek ASIC revenue** | GS: **2027 ~$20B (raised from ~$12B) / 2028 ~$52B**; HomoFish 4.5M @ ~$4,500 (27), 3M @ ~$16k + ZebraFish 1M (28); **contested 50/50 Broadcom split** (GS "TSMC preview", 07-09) | Prior wiki carried GS's earlier ~$12B (2027) mark | No house model | PENDING | GS's own **+67% upward revision** to 2027 ASIC and a Street-high-ish 2028 $52B. The **live debate is the Broadcom/MediaTek share split** (GS 50/50 vs US-investor view of higher Broadcom share) — Hock Tan (07-07) publicly dismisses the MediaTek A8 program ("still in the Fab", "PR agency of MediaTek"). Two-sided; our edge = which side of the split is right. |
| **TSM 2Q26 gross margin** | 2Q GM **~69.5-70%** vs guide 67.5% (JPM·Gokul 07-08; GS 07-09 68.5→70%) | Page tracked guide ~67.5% | House **FY26E GM ~66%** | PENDING | 2Q print tracking **~70%, above both guide and house FY-avg ~66%** → margin upside risk to the house TSM model (FY avg carries N2/overseas dilution, so not fully comparable, but the 2Q level is a positive surprise). |

## CONFIRMS (no action)

| Metric | New sell-side | Baseline | Read |
|---|---|---|---|
| **TSM FY26 revenue growth** | FY26 guide lift to **+mid-to-high 30s%** (JPM/GS 07-08/09) | House 2026E **$165B (US$) = +35% vs $122B '25** | In line — house already at the top of the old guide range. |
| **NVDA price target (MS)** | MS reiterate **OW/Top Pick, PT $288** (07-10) | Prior wiki logged **MS OW $288 on 06-16** | Unchanged — NDR reaffirms, no PT move. |
| **GEV (BofA power gap)** | BofA **Buy**, US 100+GW shortfall thesis | Reconciled **2026-07-08** (this 07-10 file is a re-drop of the same note under a new slug) | Already actioned; only the accelerator-GW-ramp datapoint (~15-17→58-60 GW/yr CY25-30) was net-new. |
| **TSM 2027 capex** | GS **$78B (from $70B)**; JPM ~$220B cum 26-28 (78/85) | House model carries no explicit capex line | New sell-side; no house baseline to contradict. Log for BBG-consensus check when Terminal returns. |

---

## To re-run when Bloomberg is back
`NVDA / TSM / AVGO / MU / MEDIATEK / GEV` — pull `PX_LAST, BEST_TARGET_PRICE, BEST_EPS, BEST_SALES, BEST_CAPEX` at `1FY/2FY/3FY` and slot each broker figure vs the consensus median. Priority: **NVDA out-year EPS/rev** (does consensus sit with the house $661B/$15.44 or with MS's lower $599B/$13.08?) and **MediaTek 2027 ASIC** (is GS's $20B above or below the Street after the raise?).
