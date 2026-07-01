# Edge tracker — house vs Street

_Generated 2026-06-30 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| _none over threshold_ | | | | | |

## Curated divergences — latest reconciliation (`reconciliation-2026-06-30.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| NFLX | Morningstar FV **$80** / BofA technical downside **$50** (Barron's, 2026-06-29) | Sharpest new bear datapoint across the whole batch — page had zero bear-side valuation anchors before today. |
| ASML | Ex-Samsung EVP expert call: WFE "passing $200bn/yr but never reaching $300bn" (2026-06-30) | Bear-sourced call explicitly contradicts both UBS's and BofA's own just-logged bull numbers — sharpest cross-source disagreement in the batch. |
| MSFT | Tigress Financial PT **$680** (Barron's, 2026-05-18) | New Street-high PT on the page. |
| NVDA | Tigress Research PT **$425** (Barron's, 2026-05-27) | New Street-high PT by a wide margin. |
| GOOG | TD Cowen (Blackledge) PT **$475** (Barron's, 2026-06-29) | Fresh Street-high, layered on top of a same-week GS raise. |
| GOOG | Forward multiple compressed **~30x (Feb) → 23.5x** (Barron's, 2026-06-29) | Wiki itself flags this as a thesis-drift supersession — material multiple compression over the quarter, now with a harder press number attached. |
| MU | Three EPS bases now on one page: Barron's next-FY consensus **$144.27**, MS's own FY27 **$168**, UBS's C2029E **$124-125** | The new "cheap at 9x fwd P/E, 0.04 PEG" framing is *built off* the lowest of the three EPS bases — flag before repeating that framing without qualification. |
| SKHYNIX/SAMSUNG/MU | SemiAnalysis Rubin-HBM-share triangle: SK hynix **~60%** / Samsung **~30%** / Micron **~0%** (first 12 months) | Internally consistent within the SemiAnalysis report, but each leg sits in tension with a different pre-existing number on its own page — the mismatched denominators (forward Rubin-specific vs. blended-2026) are never reconciled explicitly on any of the three pages. |
| AVGO/TSM | Nomura (2026-06-30) vs. Redburn/Fubon/MS on MediaTek-TPU-share pace and CoWoS 2027F capacity target (2,000kpcs Nomura target vs. 1,800kpcs Nomura's own model; Redburn's MediaTek >30%-by-2028 vs. Nomura's >30%-by-2027) | Genuine, self-acknowledged cross-shop disagreement on both the AVGO and TSM pages. |
| AMD | Vendor "40% data-center CPU share" claim (Barron's, relaying AMD's own framing) | AMD's self-reported figure runs well ahead of every third-party unit-share estimate already on the page; page flags it as a vendor claim but the gap itself deserves a sharper caveat. |
| INTC | SemiAnalysis quantified claim: 192c/192t Diamond Rapids "only ~40% faster" than 128c/256t Granite Rapids | Converts a vague management concession into the single most consequential quantified competitive gap now on the INTC page. |
| DRAMWFEcapex2026 | SemiAnalysis: SK hynix +34% / Samsung +26% / Micron +20% | New information, not yet corroborated by BBG (PENDING) or actual company capex guidance — track forward. |
| AAPL | 33x fwd EPS (Barron's, 2026-06-08) | Barron's uses a lower multiple than the page's two most bullish PTs (BofA/MS) without the page yet reconciling why. |
| TSM | Barron's "2027 P/E 21x" and "+90% EPS growth by 2027" | Barron's multiple sits below UBS/Fubon but well above the house model's; Barron's EPS growth understates the house model's own implied growth by ~27pts — likely a different EPS base/consensus, flagged for a follow-up basis check. |

## Consensus PT vs spot — live pull in `reconciliation-2026-06-30.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
