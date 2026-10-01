# Edge tracker — house vs Street

_Generated 2026-10-01 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| GOOG | Revenue $bn | 2026 | 505.00 | 427.20 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 545.00 | +18% |
| AAPL | EPS | 2026 | 10.12 | 8.76 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-10-01-inbox.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| 🔴 COHR | house Neutral $285 is the Street's second-lowest PT; Bernstein OP $350 sits below the consensus median | Action: decide whether the house's 25x-CY27 framing is still right now that every outside mark prices the FY28 ramp — the house is ~$128 below the Street median on a P&L that is within 5% of consensus for CY27. |
| 🔴 TSM | JPM capex US$86 / 100bn for 2027/28 is +14% / +16% above consensus; house 2026 line stale | Action: refresh the house 2026 line (two quarters reported since the model) and take a view on whether 2027-28 capex is the ~US$75 / 86bn the Street carries or JPM's US$86 / 100bn; the CoWoS and semicap read-throughs differ by ~US$11-14bn a year. |
| 🔴 NVDA | Fubon's 2027 GPU shipments are 53% above the house's chip count | Action: put a unit bridge into the NVDA model — packages × revenue per package for Blackwell/Rubin/Rubin Ultra in 2027 against Fubon's 11.56mn and Bernstein's rack BOM; this is the same volume-vs-price question the 09-28 report raised in GW terms (GS 18 GW vs house 24.8 GW). |
| 🔴 MU | FY27 consensus is post-print on the quarter but not on the year; capex consensus sits below the implied floor | Action: treat the FY27 consensus line as stale until it settles near the post-print broker cluster (~$182-184); for supply bears the capex datapoint is the more important one — the increase is construction-led cleanroom for late-CY28+, which dates the oversupply debate. |
| 🔴 LITE / COHR (optics TAM) | Bernstein's transceiver market is 2.3x Goldman's for 2028; no "2028 pause" | Action: the house optics model should state which TAM shape it sits on (GS's 2028 rollover or Bernstein's 40% CAGR); LITE's CY27 EPS premium rests on margin, COHR's discount on not pricing FY28 — both are TAM-shape bets. |
| 🔴 META | house CY27 capex is $28bn (−14%) below the Street; Barclays gives Muse's cost per user | Action: same bridge as 09-28 — house capex vs Street — now with a per-user cost anchor: $4.07 × DAU ramp × 12 is the incremental opex/compute the house needs to size; the Street's +$28bn CY27 capex is roughly 570m DAU of Barclays' cost (my arithmetic, illustrative). |
| ANET | Bernstein 2027 revenue is +9-14% above consensus, but the note prints three different figures | Action: the divergence is 2027 revenue, not the target; quote Exhibit 60's $17.87bn (the model line), not the text's $18.6bn. |
| Celestica (no wiki page) | Bernstein 2027 EPS is +20% above consensus; PT near the Street high | Action: no page to carry it; log on optical-cpo/custom-asic-tpu only — CLS is the highest-conviction above-consensus call in the initiation. |
| CIEN | Outperform with a PT 15% below consensus, on a PT basis that mislabels the year | Action: carry Bernstein's CIEN view as "above on FY27-28 EPS, below on multiple"; note the FY29 basis wherever $440 is quoted. |
| CSCO / GLW | Bernstein's two Market-Performs are at or near the Street LOW on PT, with estimates in line | Action: GLW is the only name in the initiation where Bernstein is BELOW consensus EPS; CSCO is a pure multiple call. Neither has a house model. |
| MU / SKHYNIX (memory price path) | Fubon's DRAM contract price falls 16% from the 2Q27 peak while Micron says supply stays constrained through CY28 | Action: the shape (peak 2Q27, −16% into 2Q28) is the first dated commodity-DRAM rollover from a primary on the page; reconcile it against MU FY28 consensus before treating FY28 EPS growth as safe. Do not quote the level until the unit is confirmed on the page image. |

## Consensus PT vs spot — live pull in `reconciliation-2026-10-01-inbox.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| SKHYNIX | 1,833,000 | 3,282,675 | +79% | street high 5,300,000 · low 1,535,000 below spot · 47/1/0 of 48 |
| AVGO | 344 | 530 | +54% | street high 715 · low 350 ABOVE spot · 58/4/0 of 62 |
| MU | 1,097 | 1,597 | +46% | street high 2,700 · low 900 below spot · 57/4/0 of 61 |
| NVDA | 231 | 323 | +40% | street high 515 · low 180 below spot · 79/2/1 of 82 |
| CIEN | 379 | 516 | +36% | street high 660 · low 347 below spot · 17/4/1 of 22 |
| COHR | 319 | 413 | +30% | street high 500 · low 280 below spot · 23/6/0 of 29 |
| CSCO | 109 | 139 | +28% | street high 170 · low 110 ABOVE spot · 20/11/0 of 31 |
| ANET | 204 | 247 | +21% | street high 330 · low 181 below spot · 34/2/1 of 37 |
| TSM | 459 | 551 | +20% | street high 700 · low 440 below spot · 31/1/0 of 32 |
| MEDIATEK | 4,980 | 5,970 | +20% | street high 10,369 · low 1,751 below spot · 31/1/0 of 32 |
| GLW | 160 | 190 | +19% | street high 238 · low 129 below spot · 15/5/0 of 20 |
| SNPS | 491 | 581 | +18% | street high 700 · low 448 below spot · 24/1/0 of 25 |
| LITE | 1,046 | 1,151 | +10% | street high 1,400 · low 820 below spot · 31/4/0 of 35 |
| META | 726 | 790 | +9% | street high 1,000 · low 580 below spot · 72/6/1 of 79 |
| AMD | 616 | 633 | +3% | street high 1,250 · low 465 below spot · 56/12/0 of 68 |
