# Edge tracker — house vs Street

_Generated 2026-09-02 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| GOOG | Revenue $bn | 2026 | 505.00 | 427.20 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 548.30 | +17% |
| AAPL | EPS | 2026 | 10.12 | 8.71 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-09-01.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| 🔴🔴 DELL | the Street's error was the MARGIN, not the revenue, and the guide sits +6.5% above the FY27 consensus median — but NOT above the street high (basis-corrected 09-02; the quarterly leg closed inside one session) | The edge, correctly based: DELL's FY27 EPS guide of $25.50 is +6.5% above the BBG annual median of $23.94 with the street high still $2.7bn/share of EPS above it at $28.60 — so the bull case is NOT exhausted by the guide; and consensus models FY28 EPS +19.0% and FY29 +20.2%, i.e. the Street does not treat FY27 as peak earnings, which management declined to answer. |
| 🔴🔴 — | The HBM $/Gb anchor this wiki has been quoting is the WRONG VENDOR'S PRICE | There is no single "2027 HBM price": three vendor curves, two customer tiers, ~30% spread. |
| 🔴 2027 DRAM bit supply | a three-way split with TWO LEGS INSIDE MORGAN STANLEY | a three-way split with TWO LEGS INSIDE MORGAN STANLEY |
| 🔴 ASML | the wiki was carrying High-NA's WORST-CASE throughput, for the segment that adopts FIRST | the wiki was carrying High-NA's WORST-CASE throughput, for the segment that adopts FIRST |
| 🔴 MSFT | BofA raises to $600 while sitting BELOW consensus on the earnings it is paying 28x for | BofA raises to $600 while sitting BELOW consensus on the earnings it is paying 28x for |
| 🔴 MRVL's Google block | a three-way conflict that decides whether the $120bn warrant is ADDITIVE or CANNIBAL | What it decides: whether the $120bn warrant ceiling is additive to AVGO/MediaTek content or comes out of it. Adjudicator: the v10 block award. |
| 🔴 NVDA | the first BEARISH read of the 70% guide in the open window | the first BEARISH read of the 70% guide in the open window |
| 🔴 GOOG/AVGO/ANTHROPIC | the FT (08-04) SIZES a figure the wiki had marked unsizeable, and it is the EARLIER source | the FT (08-04) SIZES a figure the wiki had marked unsizeable, and it is the EARLIER source |
| 🔴 — | Rating-action DATING was wrong on two pages | Rating-action DATING was wrong on two pages |
| InP routing INVERSION | cuts against the moat LITE and COHR both run on | The opposite routing from the DAMNANG block sitting directly above it on `optical-cpo` |
| China memory | the derating argument, and the constraint is mis-located on the wiki | the derating argument, and the constraint is mis-located on the wiki |
| — | Demand-side ceiling nobody on the wiki had priced: server units capped at ~+30% next year by NON-memory shortages | Demand-side ceiling nobody on the wiki had priced: server units capped at ~+30% next year by NON-memory shortages |
| BKNG | Bernstein is the lowest PT on the page and the only one below spot | Bernstein is the lowest PT on the page and the only one below spot |

## Consensus PT vs spot — live pull in `reconciliation-2026-09-01.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| ASML | 1,670 | 2,436 | +46% | *(US ADR line.)* ⚠️ **ADR panel only — 21 analysts, ZERO holds or sells.** The Amsterdam line polls **42 analysts incl. 2 SELLS** (PT €2,027.47, high €2,500). **Never net the two panels.** The reiterated **€2,500 / $2,859 IS the street high on both lines.** |
| DELL | 448 | 571 | +27% | Widest consensus upside in this run. The lone relayed broker PT (**$480**, DB) sits **−15.9% below** this median. |
| META | 595 | 745 | +25% | Street **low ($580) is BELOW spot**. BofA's $835→$810→$800 walk-down still ends **+7.4% above** this median. |
| BKNG | 199 | 238 | +20% | Bernstein's **$188 IS `BEST_TARGET_LO`** — the lowest target on the Street, from inside the hold bucket, with **no sell ratings anywhere**. |
| MSFT | 498 | 572 | +15% | BofA's raised **$600 is only +4.9%** above this median and **69% of the high**; its prior **$500 was 0.4% from spot**. |
