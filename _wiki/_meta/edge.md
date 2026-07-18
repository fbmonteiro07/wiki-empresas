# Edge tracker — house vs Street

_Generated 2026-07-17 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 9.93 | +93% |
| COHR | Revenue $bn | 2027 | 16.60 | 11.10 | +49% |
| LITE | EPS | 2027 | 30.02 | 23.77 | +26% |
| GOOG | Revenue $bn | 2027 | 641.00 | 510.70 | +26% |
| COHR | EPS | 2026 | 8.27 | 6.81 | +21% |
| NVDA | EPS | 2027 | 15.44 | 12.86 | +20% |
| GOOG | Revenue $bn | 2026 | 505.00 | 423.70 | +19% |
| NVDA | Revenue $bn | 2027 | 661.00 | 565.80 | +17% |

## Curated divergences — latest reconciliation (`reconciliation-2026-07-16.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| TSM | Print + Fubon: FY26 EPS **NT$108.80**, FY27 **NT$155.41**; 2Q26 GM **67.7%**; FY26 capex **$60-64bn** confirmed; FY26 rev growth **">40%"** (Fubon, TSMC 2Q26 call, 07-16) | **House trails the print.** Fubon FY26/27 EPS ~+6%/+8% above house; ">40%" growth implies ~US$172bn vs house $165bn; GM 67.7% > house 66%. **→ raise house TSM post-print.** |
| LITE | Citi FY27E EPS **$21.18** (raised from $20.03), Buy PT **$1,100** (Citi, 07-16) | House CY27 LITE EPS sits **well above** Citi's FY27 trajectory even after FY(Jun)/CY alignment — house is Street-aggressive on LITE out-years. **→ sanity-check house LITE CY27 build.** |
| GOOG | BofA clean-basis FY27 EPS **$14.70** / FY28 $18.12; FY26 **$19.70** *(incl. ~$80bn one-time Anthropic-stake revaluation OI)*; PO $430 Buy (BofA/Post, 07-16) | Clean-basis **house 2027 ($16.20) > BofA ($14.70) > cons is between** — house most bullish out-year. FY26 $19.70 is distorted by the non-recurring Anthropic markup — do **not** compare to house directly. (See also GOOG revenue-basis artifact in "screened out".) |
| ARM | UBS PT **$470** (from $245), **108x** CY28E EPS $4.33; EPS CY26/27/28 $2.00/$2.97/$4.33 (UBS, 06-24) | PT nearly doubled but is **multiple-driven** (61x→108x), not EPS-driven — rating-vs-PT/valuation tension. Treat as sentiment, not earnings, upside. |
| ANTHROPIC | Arete forward ARR **~$70bn by Sept-26 / >$110bn YE** (SDK-correlation, 04-14) vs BofA **~$45-47bn exiting 2Q26** run-rate (07-06) | **Wide source dispersion** on the ARR ramp — Arete's SDK-extrapolated forward is far above BofA's booked run-rate. Also new: Google marks stake **$380bn→$965bn** (BofA). |
| AMD | UBS new **Street-high PT $700** (from $670 06-24; stale $300 retired); EPS C26/27/28 $7.69/$14.63/$21.11 (UBS, 07-15) | New Street-high, GPU rev C27 $41bn/C28 $61bn. No house to check — flag as the top of the AMD range. |

## Consensus PT vs spot — live pull in `reconciliation-2026-07-16.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
