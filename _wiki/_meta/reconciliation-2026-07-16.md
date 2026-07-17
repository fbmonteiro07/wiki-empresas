# Reconciliation — 2026-07-16 run-inbox (56-file P: backlog sweep)

Variance pass on the NEW quantitative datapoints folded this run, vs three baselines:
1. **Prior wiki comments** (on disk) — the most recent PT/estimate already logged on each page.
2. **Capstone house models** (`_wiki/_data/house.json`, asof 2026-07-16 — covers AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM).
3. **BBG consensus** — **PENDING**: Bloomberg wrapper returned HTTP 503 (Terminal not logged in / Capstone VPN down) at run time. Re-run `/wiki-consensus` or `refresh_features.py --run-estimates` once the Terminal is back to populate this column.

Private names (ANTHROPIC, OPENAI) have no BBG/house → reconciled vs prior wiki only.

---

## Where the new data DIVERGES

| Name | New sell-side datapoint | Capstone house (2026-07-16) | Prior wiki | BBG | Read |
|---|---|---|---|---|---|
| **TSM** | Print + Fubon: FY26 EPS **NT$108.80**, FY27 **NT$155.41**; 2Q26 GM **67.7%**; FY26 capex **$60-64bn** confirmed; FY26 rev growth **">40%"** (Fubon, TSMC 2Q26 call, 07-16) | FY26 EPS **NT$102.5**, FY27 **NT$143.5**; rev **US$165bn**; GM **66%** | capex "reportedly $60-64bn" (now confirmed) | Cons (asof 07-17): CY26 EPS NT$102.7/sh, CY27 NT$138.9/sh (ADR 513.3/694.4 ÷5); GM 65.9%; capex ~$57bn (NT$1.86tn); rev ~$165bn (NT$5.37tn). **Fubon FY26 EPS +6%, FY27 +12% ABOVE cons**; ">40%"/~$172bn ≈ street-high (NT$5.56tn); 2Q GM 67.7% > cons FY 65.9%. Cons median PT (ADR) $625. | **House trails the print.** Fubon FY26/27 EPS ~+6%/+8% above house; ">40%" growth implies ~US$172bn vs house $165bn; GM 67.7% > house 66%. **→ raise house TSM post-print.** |
| **LITE** | Citi FY27E EPS **$21.18** (raised from $20.03), Buy PT **$1,100** (Citi, 07-16) | CY27 EPS **$30.02** (2026 $12.81) | Buy ~$1,100 on page | Cons CY27 EPS **$23.77** (street-high $36.81; CY26 $13.07). Citi FY(Jun)27 $21.18 ≈ CY26.5. **House CY27 $30.02 = +26% above cons**, still below street-high. Cons median PT **$1,128** ≈ Citi $1,100. | House CY27 LITE EPS sits **well above** Citi's FY27 trajectory even after FY(Jun)/CY alignment — house is Street-aggressive on LITE out-years. **→ sanity-check house LITE CY27 build.** |
| **GOOG** | BofA clean-basis FY27 EPS **$14.70** / FY28 $18.12; FY26 **$19.70** *(incl. ~$80bn one-time Anthropic-stake revaluation OI)*; PO $430 Buy (BofA/Post, 07-16) | 2027 EPS **$16.20** (2026 $11.80) | prior FY26 $14.43 | Cons CY27 EPS **$15.73** (hi $17.41; CY26 clean $12.62). BofA clean FY27 $14.70 = **-7% below cons**; house $16.20 = **+3% above cons**. FY26 $19.70 non-comparable (Anthropic markup). Cons median PT **$435** ≈ BofA PO $430. | Clean-basis **house 2027 ($16.20) > BofA ($14.70) > cons is between** — house most bullish out-year. FY26 $19.70 is distorted by the non-recurring Anthropic markup — do **not** compare to house directly. (See also GOOG revenue-basis artifact in "screened out".) |
| **ARM** | UBS PT **$470** (from $245), **108x** CY28E EPS $4.33; EPS CY26/27/28 $2.00/$2.97/$4.33 (UBS, 06-24) | — (no house) | stale UBS $245 | Cons EPS CY26 **$1.99** (=UBS $2.00), CY27 **$2.79** (UBS $2.97 above; hi $3.36); no CY28 cons line. Cons median PT **$306** → **UBS $470 = +54% above median** (top-of-street). | PT nearly doubled but is **multiple-driven** (61x→108x), not EPS-driven — rating-vs-PT/valuation tension. Treat as sentiment, not earnings, upside. |
| **ANTHROPIC** | Arete forward ARR **~$70bn by Sept-26 / >$110bn YE** (SDK-correlation, 04-14) vs BofA **~$45-47bn exiting 2Q26** run-rate (07-06) | — (private) | >$47B May-26 (Nomura); >$60B 3Q26 (SemiAnalysis); Yipit $69B | no BBG (private) | **Wide source dispersion** on the ARR ramp — Arete's SDK-extrapolated forward is far above BofA's booked run-rate. Also new: Google marks stake **$380bn→$965bn** (BofA). |
| **AMD** | UBS new **Street-high PT $700** (from $670 06-24; stale $300 retired); EPS C26/27/28 $7.69/$14.63/$21.11 (UBS, 07-15) | — (no house) | UBS $670 (06-24) | Cons EPS CY26 **$7.35** (UBS $7.69 above; hi $8.98), CY27 **$13.44** (UBS $14.63 above; hi $19.75). Cons median PT **$535** → **UBS $700 = +31% above median = confirmed Street-high**. | New Street-high, GPU rev C27 $41bn/C28 $61bn. No house to check — flag as the top of the AMD range. |

## CONFIRMS — no action (in-line / additive)

| Name | New datapoint | Baseline | Note |
|---|---|---|---|
| **MSFT** | MS FY EPS 06/27e **$19.62** / 06/28e $23.86 (slight cut from $19.71/$24.03); PT $650 OW reiterated (MS, 07-16) | prior wiki $19.71/$24.03; no house | Cons EPS CY26 $17.73 / CY27 $20.93; MS FY(Jun)27 $19.62 straddles the two (~in-line). Cons median PT $558 → MS $650 = +16% above median (bullish PT). Minor trim, thesis intact. |
| **ASML** | 2Q26 EPS €7.58 (~11% above street); Redburn PT **€2,100** (from €1,900); net sales FY26/27/28 €44.1/55.8/69.2B (Bernstein/Redburn/didier, 07-15/16) | prior €1,900; page already carries Bernstein €2,500 "Triple happiness" | Post-print beat; new PT inside the on-page €2,100-2,500 bull range. House ASML lives in `P:\...\ASML_Peers_SemiCap_v17.xlsx` (not parsed into house.json) — reconcile there manually. Cons rev CY26 €42.0B / CY27 €56.0B → Redburn €44.1B/€55.8B ≈ in-line to street-high (CY26 hi €44.7B). Cons median PT €2,352 → Redburn €2,100 sits **below** cons median; page's Bernstein €2,500 above it. |
| **COHR** | Citi Buy $420 (reaff.), EPS $5.47/$9.78 (Citi, 07-16) | house CY26 $8.27 / CY27 $19.21 | Citi FY(Jun) vs house CY: on aligned periods Citi ~in-line/slightly above house near-term; house CY27 $19.21 maps to Citi FY28 (not given). No clean divergence. |
| **NXPI/TXN/ADI/ON/MCHP/IFX/NVTS** | MS Analog Playbook marks (07-13): NXPI OW $335, **TXN UW $221**, ADI OW $428, ON EW, MCHP EW $94, IFX OW €91, **NVTS UW $13.7** | prior wiki reaffirms; no house | Mostly reaffirmations. Two notable **bear marks**: TXN UW $221, NVTS UW $13.7. |
| **CEG/VST/WMB/GEV/PWR** | MS Byrd OW screen: CEG +38%/VST +39%/WMB +25% to PT (04-06); GEV MS transformer top-pick (~6% 2027E EPS upside, 03-29); **PWR Bernstein M PT $538**, EPS 2026E $13.04/2027E $15.32 (04-16) | no PTs previously on disk for these; no house | All NEW ratings — fill prior gaps; nothing to diverge from. |
| **STX/WDC** | JPM initiation STX PT $525 / EPS FY26-28 $13.15/$20.06/$27.00 (03-30); MS STX $582 / WDC $380 (04-06) | superseded by later June numbers already on pages | Historical coverage origin only — later same-broker numbers already govern the pages. |

## Screened out (not real divergences)

- **GOOG revenue basis** — BofA "FY26 net rev **$427bn**" is net-of-TAC; house "$505bn" is gross. **Gross/net artifact**, not a divergence. Do not action.
- **COHR / LITE FY-vs-CY** — Coherent & Lumentum report June-fiscal-year; Citi labels are FYs, house is CY. Nominal-year EPS gaps above are period-mismatch, aligned in the reads.

## Feeds the edge tracker
Genuine open divergences to carry into `_meta/edge.md` (via `refresh_features.py`): **TSM (house trails print — raise)**, **LITE (house CY27 above Street)**, **GOOG (house 2027 above BofA, clean basis)**, **ANTHROPIC (ARR source dispersion)**. ARM/AMD are Street-level PT moves (no house), logged for context.

_BBG column resolved 2026-07-17 — estimates.json asof 2026-07-17 (median targets via BEST_TARGET_PRICE wrapper pull same date)._
