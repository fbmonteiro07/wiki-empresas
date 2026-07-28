# Edge tracker — house vs Street

_Generated 2026-07-27 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 10.00 | +92% |
| COHR | Revenue $bn | 2027 | 16.60 | 11.20 | +48% |
| LITE | EPS | 2027 | 30.02 | 23.90 | +26% |
| COHR | EPS | 2026 | 8.27 | 6.82 | +21% |
| NVDA | EPS | 2027 | 15.44 | 12.87 | +20% |
| GOOG | Revenue $bn | 2027 | 641.00 | 535.50 | +20% |
| GOOG | Revenue $bn | 2026 | 505.00 | 424.60 | +19% |
| NVDA | Revenue $bn | 2027 | 661.00 | 567.10 | +17% |

## Curated divergences — latest reconciliation (`reconciliation-2026-07-27.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| STX | ⭐ **MS · Woodring: PT $1,035** (20.0x CY27 EPS **$51.67**); bull $1,446 / bear $490; OW, Top Pick (2026-07-27) | **The Street's PTs already discount earnings its own estimates don't carry.** Either estimates rise toward the PTs or the PTs are unsupported; the checks (300-400EB/yr shortfall through CY28, 2032 CSP visibility, $25-30/TB) point at the estimate side. **Largest gap in the batch. Build the house model before the print.** |
| WDC | ⭐ **MS · Woodring: PT $650** (20.0x CY27 EPS **$32.29**); bull $920 / bear $322; OW (2026-07-27) | Same structural setup as STX but less extreme — MS stays inside the Street high here. **STX carries the asymmetry; WDC confirms the direction.** New company-sourced leg: WDC mgmt sees "an opportunity" for $/TB growth to reach **teens % Y/Y** vs +9% in March |
| INTC | UBS Neutral, **PT $121**, implied **CY26 EPS $1.42** / CY27 $1.96 (back-solved from stated 70.4x / 51.1x at $100) | **Rating-vs-numbers tension:** a Neutral rating carrying a +32% target and an above-high near-year estimate. ⚠ **PARTIAL** — EPS is derived from a P/E, not printed. Press the analyst on why this is Neutral |
| MEDIATEK | ⭐ UBS Buy, **PT NT$6,500**, implied **CY27 EPS 181.2** (from 20.7x at NT$3,750) | **The whole divergence is the Google TPU v9 ramp, and it is past design-intent** — UBS's ~90% EMIB-T packaging yield is measured on **trial production runs of MediaTek's v9 prototype**. Two dependencies outside MediaTek's control: Ibiden's ¥220bn Gama plant only reaches MP late-2027 (and Google TPU demand alone "could largely absorb" it), and EMIB-T *substrate* yields are ~50% vs >80% for HPC ABF. **Consensus CY27 may be 37% too low, untested by any house view** |
| MSFT | ⭐ **Microsoft's own capex guide decomposed:** memory hardware inflation adds **$5bn in 4Q/Jun and $20bn across 2H CY26 → $25bn of the CY26 $190bn guide from memory price alone** | **≈13% of the guide buys no incremental compute** (derived ratio). The wiki's canonical **"$1.4trn 2028 hyperscaler capex"** frame (MS · Nowak, 2026-07-12) does **not** split price from capacity, so every capex→GW inference on the wiki silently assumes capex ≈ capacity. A material slice lands on **[[MU]] / [[SKHYNIX]] / [[SAMSUNG]]** revenue instead. **Most re-usable number in the batch. Not additive to the $1.4trn frame** |
| MSFT | UBS **cuts PT $510 → $480**, holds Buy; FY06/27E EPS 19.49 → **19.26**, FY06/28E 22.68 → **22.12**; FY27 capex $234b → **$261b** | **Only PT cut in a batch of four raises, and the rating is held anyway.** The substance is the balance sheet: equity FCF yield **2.4% → 0.1%** in FY06/27E; net cash 51,414 → 49,906 → **1,299** → **net debt (13,408)** by FY28E. First source on the page to date Microsoft going net-debt. ⚠ **BASIS:** the $261bn is **all-in = $209.0bn cash P&E + $51.6bn capital leases**, so it is *not* like-for-like with the $230-235bn sell-side consensus or BofA's $243.5bn bogey |
| SMIC | Named 2026 recipient of domestic immersion-DUV tools; CEO Zhao Haijun (May call): overseas customers want China capacity "because capacity was tight elsewhere" | **A 16% capex step-down is inconsistent with a fab adding tools, qualifying a new domestic supplier and fielding overflow demand.** Flag the SMIC CY27 capex line as the number in this batch most likely to be wrong-footed |
| ASML | MATCH Act would widen restrictions to immersion DUV **and curb servicing** at some Chinese fabs; China domestic output ~5 tools 2026 / ~20 in 2027 | **Size the tool story down, and move the attention to the annuity.** The servicing curb attacks the installed-base service/upgrade line — carried in no CY26/27 consensus number, and un-backfillable by 5-20 domestic units/yr. Relevant against ING's standing ~1%-of-revenue service-licence estimate. **Watch the service line, not the China tool line** |
| AAPL | Bernstein (2026-03-03, backfill): iPhone BOM **+~25%**; 12GB DRAM line **$28.93 → $114.00 (+294%)**, memory ~5% → ~16-17% of BOM; FY27 scenario grid **$11.43 / $10.28 / $9.54 / $8.81** | ⚠ **BASIS** (fiscal-Sep vs calendar). Even after the shift, **house EPS is ~14% above consensus** — pre-existing, not created by this run — and sits between Bernstein's S1 and S2, i.e. the house implicitly underwrites a **benign memory-cost outcome**. Bernstein's BOM work is the sharpest available bear input. **Action: run the house model against the S3/S4 legs** |

## Consensus PT vs spot — live pull in `reconciliation-2026-07-27.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
