# Edge tracker — house vs Street

_Generated 2026-08-07 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 10.00 | +92% |
| COHR | Revenue $bn | 2027 | 16.60 | 11.20 | +48% |
| LITE | EPS | 2027 | 30.02 | 23.96 | +25% |
| COHR | EPS | 2026 | 8.27 | 6.82 | +21% |
| NVDA | EPS | 2027 | 15.44 | 12.91 | +20% |
| GOOG | Revenue $bn | 2026 | 505.00 | 426.80 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.30 | +18% |
| NVDA | Revenue $bn | 2027 | 661.00 | 568.20 | +16% |
| AAPL | EPS | 2026 | 10.12 | 8.77 | +15% |

## Curated divergences — latest reconciliation (`reconciliation-2026-08-06.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| GOOG | Mgmt 2026 capex guide **$195-205bn**; BBG CY26 **$200.8bn** | ① House is stale to the 07-22 raise — 2027 matches BBG to the decimal, so this is a missed update, not a call. Fix before any capex/FCF work. |
| PLTR | Q2 **+93% y/y** actual; FY26 guide **$8.15bn** | ② The steep decel is unexpressed in consensus and is the cleanest long-side read of the RSI thesis in the book — but FUNDA's own FDE-compression argument cuts the other way. Both legs on page. |
| PLTR | FUNDA: Q1'26 **+85%**, "**ARR >$6.5B**" | ③ **Do not propagate.** Must not be mixed with US Commercial RDV $6.238bn (different metric, similar level). Resolve vs the Q1'26 10-Q. |
| AMZN | FUNDA (Oct-25) Trainium **order book 2.2-2.6M** units for 2026 | ④ Three bases, never netted. A reusable **calibration prior** on how much an early order book overstates output — NOT a revision. CoWoS leg scored far better than the unit leg. |
| AMZN | FUNDA Project Rainier **4.5GW** / 3 campuses | ⑤a Facility vs IT-load never stated. All three stand per the `assumptions.md` GW rule. |
| GOOG | FUNDA Anthropic deal "**up to 1M TPUs**" | ⑤b Filed as a unit-contract **ceiling**, not netted against the GW or $ marks. |
| macro | FUNDA: semis' worst month since **2002** | ⑤c Instrument/window mismatch (SOX vs SOXX vs broad basket). Both retained; any use must name the index. |
| GOOG | — | ⑥ **CY-sum defect — use sum-of-quarters, do not cite.** Second ticker showing this class after the SPCX capex bug (08-05). |

## Consensus PT vs spot — live pull in `reconciliation-2026-08-06.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| GOOG | 356 | 427 | +20% | 🔴 **Largest upside in the run, and it sharpens ① rather than softening it.** ⚠️ The C-share sample is thin (18 recs) because most of the Street publishes on the A-share — **GOOGL corroborates almost exactly: spot 356.95 / PT 428.35 / +20.0%, rating 4.73/5 on 74 recs.** The Street pays a 20% premium to spot **while carrying 2026 capex at the guide midpoint ($200.79bn)**. So the house's $183bn is not conservatism that buys margin of safety — it models ~$18bn **less** cash out than the Street on a name the Street already thinks is 20% cheap, which means **house FCF is overstated against both the company and the Street.** |
| AMZN | 278 | 327 | +17% | ✅ **Highest-rated name in the run on the deepest sample.** Nothing in this run's AMZN findings is an estimate call — ④ is an order-book **calibration prior** and ⑤a a **basis** conflict — and the capex CONFIRMS row holds on the fresh pull (BBG CY26 capex **$214.16bn** vs Jassy's ~$220bn, −2.7%). **CONFIRMS.** |
| PLTR | 169 | 196 | +16% | 🔴 **Weakest conviction of the four — and the entry has deteriorated hard in one session.** The stock ran **155.92 → 169.19 (+8.5%)** since the 08-06 snapshot against an unchanged PT, so upside compressed from **+25.6% to +15.8% on price alone.** Reads with ②: the Street's PT is anchored to a CY27 that decelerates to +54%, and **the tape moved toward the guide before the PTs did.** The divergence stands; the risk/reward on it does not. |
| MSFT | 502 | 563 | +12% | ✅ **Lowest upside of the four, and it is entirely a price move.** PT essentially unchanged from the 08-04 live pull (**$563.65 → $563.49, −0.03%**) while spot rose **$490.64 → $502.20** — the compression from +14.9% to +12.2% carries **no estimate content**. MSFT's only contribution to this run is the top-4 capex CONFIRMS row, which holds. **CONFIRMS.** |
