# Edge tracker — house vs Street

_Generated 2026-08-24 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 11.89 | +62% |
| COHR | Revenue $bn | 2027 | 16.60 | 12.70 | +31% |
| NVDA | EPS | 2027 | 15.44 | 12.97 | +19% |
| GOOG | Revenue $bn | 2026 | 505.00 | 427.50 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.30 | +18% |
| AAPL | EPS | 2026 | 10.12 | 8.76 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-08-21.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| 🔴 MU | BMO initiates Outperform on a target 17.8% BELOW consensus | Action: MU: treat BMO as a MULTIPLE call, not an estimate call — EPS is consensus to within 0.3% on both years while the $1,300 target sits 17.8% BELOW the $1,581 consensus PT. An Outperform initiated below the Street. The open variable is the margin-to-EPS pass-through, not the margin. |
| 🔴 NVDA | a $340 target on consensus numbers: pure re-rating | Action: NVDA: interrogate any future PT move as a re-rating argument first and an estimate-revision argument second — BMO vs MS is like-for-like on FY-Jan with EPS within 3.1%, so the entire $340-vs-$288 gap is the multiple (25x vs ~22x). House 2027E EPS $15.49 is +19.1% vs consensus and stands alone at the top. |
| 🔴 SAMSUNG | MS's own capex undercuts Citi's dividend math | Action: SAMSUNG: MS model FY26E capex W109.9tn is +40% vs consensus W78.5tn and the FY24A/25A historicals tie to JPM within 0.3%, so it is not a definitional artefact. If MS is right, the FCF underwriting Citi's ~W120tn annualised dividend is materially lower than the Street assumes. Both new PTs sit BELOW the W490k consensus. Do NOT route the capex delta to semicap until the MS Hynix model is … |
| 🔴 CRWV | the run's largest outright divergence | Action: CRWV: largest outright divergence of the run — Arete $317 is +119% above the $144.74 consensus PT, on revenue +26%/+37% vs consensus in 28E/29E. Consensus still has CRWV loss-making until 3FY, so the target rests on a profitability crossover the Street has not underwritten. |
| 🟡 NBIS | the revenue upgrade is NOT free | Action: NBIS: discount the headline. The +41.7% PT gap overstates it — Arete's revenue upgrade (+14%/+54%/>+70%) comes with capex ALSO +66%/+94% above consensus, Arete's own words are 'partially offset by convertible and equity dilution and higher capex', and it ranks NBIS LEAST levered of its three neoclouds. |
| 🟡 IFX / TXN / ADI | the PT directions DISAGREE inside one deck | Action: Power semis: the deck is not uniformly bullish and the headline TPs hide it — IFX RAISED 9% to EUR124 (+41% vs consensus, and 2x management's own EUR2.5bn datacentre guide), TXN CUT 6% to $381 despite modelling FY28 EPS +26% above consensus (multiple compression on rising numbers), ADI a rounding move on a mark already held. Only IFX is a real new above-consensus call. |
| 🔴 ORCL / META / GOOG / AMZN | Off-balance-sheet AI financing is LARGER than the tracked issuance | Action: Hyperscaler financing: the '14% of USD IG corporate supply' figure UNDERSTATES the claim on credit. Oracle-tenanted third-party DC bonds are $16.87bn (~67% of Oracle's own issuance) and Meta's JV structures $39.93bn (~1.6x its own) — both outside that share. Oracle started widest and widened most on every tranche; the Meta JV channel repriced ~95bp wider between two deals. House GOOG/ME… |
| 🟡 SAMSUNG / MU / SKHYNIX | a BASIS dispute, not a level dispute | Action: CXMT pricing: a BASIS dispute, not a level dispute — the page's ~24% company-average discount (Wells Fargo 07-14) versus like-for-like 5-10% and a SIGN FLIP in server (CXMT 2.2% HIGHER). Both stand; they imply opposite conclusions about DRAM price risk, so never quote one without its denominator. |
| 🟢 KIOXIA / SNDK / PANW / CRWD | Stale marks now provably stale | Action: Stale marks: China Renaissance KIOXIA JPY55,400 is -51.8% vs consensus and SNDK $1,452 is BELOW SPOT — logged historical, and they did NOT displace live marks (backwards drift). Separately the MS PTs carried on PANW ($320) and CRWD ($172) are now below spot and need refreshing. The staleness itself yielded alpha: SNDK HBF timing drifted ~2 quarters right in 4 months. |
| 🟡 MU / NVDA / SKHYNIX | Open disagreements retained, not resolved | Action: Open disagreements deliberately retained, not resolved: 'MU leads HBM4' (BMO) against SemiAnalysis ~0%-of-first-12-months and two houses putting Samsung #1 in 2027; HDD-to-NAND structural against Bernstein's TCO math; and the Rubin Ultra HBM4 8-Hi claim, which is UNCONFIRMED per the author's own disclaimer and was not allowed to move any Sinal verdict. |

## Consensus PT vs spot — live pull in `reconciliation-2026-08-21.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| 285AJP | 54,320 | 114,935 | +112% | China Renaissance JPY55,400 = -51.8% vs cons -> STALE (04-30) |
| 000660KS | 1,761,000 | 3,231,945 | +84% | no new PT this run; CXMT read-through only |
| 005930KS | 270,000 | 490,018 | +81% | Citi W450k -8.2% / MS W381k -22.2% vs cons -> both BELOW cons |
| CRWVUS | 88 | 145 | +65% | Arete $317 = +119.0% vs cons PT -> largest divergence of the run |
| MUUS | 967 | 1,581 | +64% | BMO $1,300 = -17.8% vs cons PT on in-line EPS -> multiple bear |
| IFXGR | 56 | 88 | +57% | Arete EUR124 (RAISED from 114) = +41.4% vs cons -> the real call |
| NVDAUS | 215 | 308 | +43% | BMO $340 = +10.5% vs cons PT; EPS in line -> re-rating call |
| SNDKUS | 1,596 | 2,205 | +38% | China Renaissance $1,452 = -34.1% vs cons and BELOW SPOT -> STALE |
| NBISUS | 219 | 293 | +34% | Arete $415 = +41.7% vs cons PT, but capex +66/+94% vs cons too |
| ADIUS | 373 | 468 | +26% | Arete $490 = +4.6% vs cons; prior Arete mark was already $487 |
| TXNUS | 264 | 329 | +24% | Arete $381 CUT from $405, yet FY28 EPS +26% vs cons -> compression |
| MRVLUS | 237 | 272 | +15% | no new PT; bullish memory->connectivity read-through (unconfirmed) |
| CRWDUS | 192 | 213 | +11% | MS PT carried on page ($172) is now BELOW spot -> refresh needed |
| PANWUS | 358 | 367 | +3% | MS PT carried on page ($320) is now BELOW spot -> refresh needed |
