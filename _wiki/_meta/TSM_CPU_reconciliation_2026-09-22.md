# TSMC CPU revenue reconciliation — 22 September 2026

**Working answer: a $200bn annual server-CPU TAM supports approximately $51bn/year of TSMC front-end wafer revenue and 142,000 300mm wafers/month, conditional on UBS's 2030 CPU mix, silicon requirement and wafer pricing.** It is a house scenario derived from broker estimates, not company guidance, a consensus revenue increment, or a commitment to new capacity. A case without the assumed increase in wafers per CPU gives about $36bn/year at the same future wafer price. These are explicit scenarios, not a statistical confidence interval.

Scope: server CPU silicon worldwide, including merchant and captive Arm processors and Nvidia CPUs. The $200bn target is the user's scenario; 2030 follows the wiki's existing server-CPU TAM framework. No PC/mobile TAM, accelerators, HBM, Arm royalties, server systems or cloud service revenue is added. Captive CPU values use the source's imputed silicon TAM convention.

## What TSMC earns from CPUs today

| Universe / period | TSMC revenue | Grounding |
|---|---:|---|
| Broad CPU business, 2025 | $15–16bn | PARTIAL: Bernstein / Mark Li et al., 2026-08-10, pp.2–3 |
| Broad CPU business, 2026E | Approximately $25bn | PARTIAL: same source, forecast |
| Broad CPU business, 2027E | High-$30bn | PARTIAL: same source, forecast |
| Server CPUs only, 2025 | $3.667bn | HARD sourced estimate: UBS / Sunny Lin et al., 2026-05-21, p.2 |
| Server CPUs only, 2027E | $14.003bn | HARD sourced estimate: same source; no current-year interpolation |

These numbers have different universes. Bernstein includes AMD client processors, Apple processors and Intel outsourced client CPU tiles. UBS's server model only allocates TSMC demand to AMD and Arm-architecture CPUs. Intel server compute demand remains in Intel's foundry in that model; this does not imply Intel buys nothing from TSMC across its broader product portfolio.

The arithmetic residual between Bernstein's 2025 broad CPU estimate and UBS's server estimate is **$11.333–12.333bn**. This is a cross-broker, cross-vintage reconciliation residual, consistent with the broader client exposure; it is not a disclosed non-server business segment and cannot be assigned entirely to any one customer. Source differences may also contribute. TSMC reported total 2025 revenue of **$122.42bn**; the broad CPU estimate is therefore about **12.3–13.1%** of total sales, consistent with Bernstein's approximately 13% depiction. That is a scale bound, not independent proof of the CPU estimate. [TSMC FY2025 annual report](https://investor.tsmc.com/static/annualReports/2025/english/index.html).

## Revenue per server CPU that TSMC manufactures

These are derived averages per CPU package served by TSMC, not wafer prices, retail CPU prices, or observed foundry invoices. Each CPU can consume several dies, and foundry manufacturing and CPU shipment timing can differ. Treat the bridge as annual flow-equivalent economics.

| UBS model year | Industry CPU units | AMD + Arm unit share served | TSMC-served CPU units | TSMC server CPU wafer revenue | Derived TSMC content / CPU |
|---|---:|---:|---:|---:|---:|
| 2025 estimate | 23m | 24% + 16% = 40% | 9.20m | $3.667bn | **$399** |
| 2030 estimate | 63m | 29% + 42% = 71% | 44.73m | $44.068bn | **$985** |

Source inputs: **HARD sourced broker estimates**, UBS / Sunny Lin et al., 2026-05-21, Figure 2 p.2. Calculated columns: house arithmetic, 2026-09-22. Arm denotes all Arm-architecture CPU designers here, not just Arm Holdings.

Worked arithmetic:

1. 2025 served units = 23m × (24% + 16%) = 9.20m.
2. 2025 content = $3.667bn ÷ 9.20m = $398.59 per CPU.
3. 2030 served units = 63m × (29% + 42%) = 44.73m.
4. 2030 content = $44.068bn ÷ 44.73m = $985.20 per CPU.

The rise is not a free assumption that TSMC collects a constant percentage of CPU selling prices. UBS models wafer ASP rising from **$17,000 to $30,000** and an implied **approximately 40% increase in wafers per CPU**. The first is a sourced broker forecast; the second is back-solved from its wafer and unit totals. Together these produce about **2.47×** foundry revenue per served processor. Larger/more dies, node mix and yields can affect that physical intensity; the table does not separately identify their contributions.

By architecture/vendor, the same UBS figures imply AMD server content about **$436 in 2025 / $1,117 in 2030**, and Arm server content about **$338 / $894**. Totals do not tie perfectly to the blended value because source rows are rounded.

## From $200bn TAM to TSMC annual revenue and wafers

The UBS report's headline says approximately $170bn, but Figure 1's matching **bottom-up** 2030 calculation is **$173bn / 63m units**. Its other top-down calculation is $168bn / 70m units; do not mix these denominators.

| Input | Value | Tag and source |
|---|---:|---|
| Scenario server CPU TAM | $200bn/year | ESTIMATE / scenario: user; 2030 horizon assumed from wiki context |
| Baseline CPU market value | $173bn/year | HARD sourced forecast: UBS, 2026-05-21, p.2 Fig.1 |
| Baseline global CPU units | 63m/year | HARD sourced forecast: same source |
| TSMC-served unit share | 71% | Derived from HARD sourced 29% AMD + 42% Arm, Fig.2 |
| Baseline TSMC server wafer demand | 122.4k wafers/month | HARD sourced forecast: Fig.2 |
| Future wafer ASP | $30,000 | HARD sourced forecast: Fig.2 |
| Same CPU ASP, vendor mix and wafer intensity at $200bn | Held constant | ESTIMATE: house scenario extension, not disclosed by UBS |

1. Industry CPU ASP = $173bn ÷ 63m = **$2,746**.
2. CPU units at $200bn, unchanged ASP = $200bn ÷ $2,746 = **72.83m/year**.
3. Units served by TSMC = 72.83m × 71% = **51.71m/year**.
4. TSMC wafer revenue = 51.71m × $985.20 = **$50.95bn/year**.
5. Front-end wafer demand = 122.4k × ($200bn ÷ $173bn) = **141.50k/month**, or **1.698m/year**.

Equivalent shortcut: **$200bn × ($44.068bn ÷ $173bn) = $50.95bn**. The implied 25.47% foundry-revenue / total-CPU-TAM ratio is an output of this model, not an assumed foundry take rate. 71% is a unit share, not a revenue share. Multiplying $200bn by 71% and treating it as TSMC revenue would be incorrect.

Multiplying the rounded wafer quantity by $30,000 yields $50.941bn, versus $50.946bn using the printed UBS revenue: a 0.009% rounding difference. No economic adjustment is needed.

This represents about **$47.28bn of server CPU revenue growth versus UBS's 2025 estimate**, spread over the scenario horizon. It does not represent incremental revenue versus 2030 consensus or the entire TSMC company: existing CPU forecasts are already in broker models, and client CPU revenue is outside this scenario. Likewise, 142kwpm is total monthly CPU wafer demand in the scenario, not 142kwpm of new fabs.

## Independent checks and limitations

**1. Different unit forecast, similar revenue magnitude.** BofA / Vivek Arya et al. (2026-08-12, p.5) forecast 2030 CPU TAM $210.6bn, with AMD 24.9m and Arm 27.8m units. Applying UBS's vendor-specific wafer content and normalizing to $200bn:

`[(24.9m × $1,117.24) + (27.8m × $893.88)] × 200 / 210.6 = $50.02bn`.

This is within 1.8% of the $50.95bn scenario. The unit forecast is independent; wafer content is reused. This is a hybrid house check, not a BofA forecast for TSMC and not complete independent validation. BofA's 2025 unit total is 29.9m vs UBS 23m, so vendor histories should remain separate.

**2. Different foundry-content model supports order of magnitude.** MS / Charlie Chan et al. (2026-08-24, p.9 Exhibit 12) forecast 2027 Venice compute-wafer revenue of $6.804bn / 5.670m CPUs = **$1,200/CPU**, and Vera $6.229bn / 5.750m = **$1,083/CPU**. These are respectively 7.4% and 21.2% above UBS's 2030 AMD and Arm averages. Both are below a pre-specified 25% order-of-magnitude deviation threshold, but they compare particular 2027 products with a 2030 fleet average and omit separately priced I/O dies. They establish plausibility, not equality or actual realized pricing. MS's front-end wafer columns are used; its separate packaging allocations are not counted as front-end wafers.

**3. Actual calibration remains unavailable.** TSMC's consolidated reported revenue bounds the segment estimates but does not disclose CPU-specific revenue or units. Thus this model back-solves constants from identifiable broker estimates, not from an observed CPU invoice/revenue series. No independent CPU-level historical level/flow back-test is claimed. Physical die/yield decomposition is also not separately established. This is the principal reason for the overall PARTIAL status.

**4. No generic packaging uplift.** Bernstein / Mark Li et al. (2026-08-10, p.4) identify CPU packaging work at ASE and Amkor. MS models front-end CPU wafer revenue separately. This bridge excludes unquantified I/O/packaging upside; a GPU-style CoWoS/HBM surcharge cannot be attached automatically.

**5. An apparently useful cost shortcut is not compatible.** Intel / John Pitzer, relayed by Bernstein / Stacy Rasgon (2026-09-21, p.7), discusses wafer cost for a synthetic integrated AMD/TSMC business. That is not an identified foundry revenue take rate for server CPUs and may remove the intercompany foundry margin. The reported 15–20% cost illustration is therefore not used as a TAM-to-TSMC-sales coefficient.

## Sensitivities — every row retains a $200bn CPU TAM

| Scenario | TSMC CPU wafer revenue / year | Wafer demand / month | Assumption classification |
|---|---:|---:|---|
| UBS 2030 mix, wafer intensity and prices | **$50.9bn** | **141.5k** | House extension of sourced estimates |
| Preserve 2025 wafers per CPU; use 2030 wafer ASP and served mix | **$36.4bn** | **101.2k** | Historical broker intensity held constant, explicit scenario |
| Entire $173bn → $200bn TAM uplift comes from CPU price | **$44.1bn** | **122.4k** | Pure price scenario; no extra units or foundry content |
| CPU ASP 20% above UBS; same $200bn TAM | **$42.5bn** | **117.9k** | ESTIMATE stress parameter; fewer units |
| Wafer ASP 20% below UBS | **$40.8bn** | **141.5k** | ESTIMATE stress parameter; physical demand unchanged |
| Wafer ASP 20% above UBS | **$61.1bn** | **141.5k** | ESTIMATE stress parameter; physical demand unchanged |
| TSMC serves 61% rather than 71% of units, proportional loss across its mix | **$43.8bn** | **121.6k** | ESTIMATE stress parameter; not a share forecast |

Interpretation: $200bn of CPU sales alone is insufficient to identify foundry demand. The growth must be decomposed into CPU volume, TSMC-served mix, wafers per CPU and wafer pricing. The last two also determine whether the foundry receives the same economic benefit as the CPU designer.

## Source ledger corrections identified

The existing canonical ledger at `_wiki/_meta/assumptions.md:560` incorrectly describes the $4bn→$44bn series as Arm-as-CPU-maker and attributes it to Bernstein. The original UBS table identifies it as **TSMC server-CPU wafer revenue**, with $3.667bn in 2025 and $44.068bn in 2030. Its industry 200.7kwpm is **monthly wafer demand**, not cumulative demand; TSMC's part is 122.4kwpm. These are recorded corrections to the source interpretation; this memo does not silently overwrite the canonical file.

## Audit status

**Independent double-check skeptic verdict: PARTIAL (2026-09-22).** The reviewer visually verified all five requested UBS, Bernstein, BofA and MS exhibits and found no material arithmetic error. Arithmetic and units PASS; this remains a conditional broker-based scenario without observed CPU-level calibration. Accepted findings: describe per-CPU values as front-end wafer revenue for TSMC-served AMD/Arm CPUs; identify BofA's reused content assumption; call the broad/server difference a cross-broker scope/vintage gap; keep compatibility checks separate from actual validation. Those distinctions are reflected above and in the calculator. Tiny rounding differences are below displayed precision. The industry/TSMC distinction also checks: at the $200bn scenario, all-industry demand would scale to approximately 232kwpm, of which TSMC's subset is 141.5kwpm. No direct current-year server-revenue estimate or historical CPU actual validation is claimed.

## Reproduction and original exhibits

- [Source ledger](../_data/cpu_tsm_reconciliation_20260922/sources.md)
- [Reproducible stdlib calculator](../_data/cpu_tsm_reconciliation_20260922/model.py)
- [Machine-readable results and guardrails](../_data/cpu_tsm_reconciliation_20260922/results.json)
- [UBS original report](../../relatórios%20bons/CPU_TAM_-_UBS.html), pp.1–5; principal table p.2.
- [Bernstein original report](../../relatórios%20bons/BERN_259272.html), pp.2–4.
- [BofA original report](../../relatórios%20bons/Vivek_on_CPU.html), pp.3,5,6.
- [MS original report](../../relatórios%20bons/GLOBAL_20260824_1435.html), p.9.
