# Muse memory requirement: chart reconstruction

Prepared 2026-09-21. This reconstructs the user-supplied exhibit; its author, publication date and denominator years remain unconfirmed. It is a scenario model, not a Capstone adoption forecast or a company procurement estimate.

## Result and grounding

All 16 displayed percentages are reproduced, at the exhibit's precision, with **35 decimal EB of annual DRAM output** and **1,000 decimal EB of annual NAND output**. These denominators are **back-solved from the exhibit**, not independently verified industry forecasts. The numerator is a deployment capacity stock. The percentages express that stock relative to the quantity produced in one year, not the share of installed memory worldwide or recurring annual purchases.

| Adoption of Meta DAP | Users | DRAM full allocation | DRAM lower use | NAND full allocation | NAND lower use |
|---|---:|---:|---:|---:|---:|
| 5% | 180m | 4.1% | 0.26% | 1.8% | 0.18% |
| 10% | 360m | 8.2% | 0.51% | 3.6% | 0.36% |
| 25% | 900m | 20.6% | 1.3% | 9.0% | 0.90% |
| 50% | 1,800m | 41.1% | 2.6% | 18.0% | 1.8% |

Source for scenario inputs and displayed targets: user-supplied chart, received 2026-09-21; original author/date pending. Calculations: this reconstruction, 2026-09-21. “Lower use” replaces the exhibit's unsupported probability label “more likely.” “Full allocation” is an upper scenario within this per-VM model, not a ceiling on the entire service.

## Input ledger

| Input | Value | Tag | Source / basis |
|---|---:|---|---|
| Meta Family daily active people | 3.60bn | HARD | Meta Q2 2026 release, 2026-07-29; June 2026 average. This is the potential distribution base, not Muse users. |
| Adoption | 5%, 10%, 25%, 50% | ESTIMATE | Scenarios printed in supplied exhibit; not observed adoption. |
| Full allocation DRAM per VM | 8 GB | ESTIMATE | Supplied exhibit; physical allocation not verified. |
| Full allocation resident fraction | 100% | ESTIMATE | Supplied exhibit, every VM awake with all memory filled. |
| Lower-use resident fraction | 25% | ESTIMATE | Supplied exhibit; must represent physically resident VMs, not merely active CPU utilization. |
| Lower-use RAM per resident VM | 2 GB | ESTIMATE | Supplied exhibit; no memory telemetry verified. |
| RAM per nonresident VM | 0 GB | ESTIMATE | Implicit in the exhibit's lower-use formula; requires memory reclamation/suspension. |
| Full allocation NAND | 100 GB/user | ESTIMATE | Supplied exhibit; not a verified product quota. Treated as total physical NAND-equivalent in this replication. |
| Lower-use primary files | 5 GB/user | ESTIMATE | Supplied exhibit. Does not separately enumerate OS images, logs or databases. |
| Lower-use total NAND-equivalent | 10 GB/user | PARTIAL, DERIVED | Lower NAND bar is one tenth of 100 GB bar. Exact split of replication, media, compression and other bytes unknown. |
| Equivalent total copies | 2x | ESTIMATE / CALIBRATED | 10 GB / 5 GB, conditional on all copies on NAND and no other factors. Means original + one copy, not two additional backups. |
| NAND residency | 100% | ESTIMATE | Required simplifying assumption to interpret the NAND bars as physical NAND capacity. Actual storage medium/tiering undisclosed. |
| Annual DRAM denominator | 35 EB/year | PARTIAL, DERIVED | Rounded chart-consistent denominator; year, geography, production vs shipments and HBM inclusion not given. |
| Annual NAND denominator | 1,000 EB/year | PARTIAL, DERIVED | Chart-consistent denominator; year and production vs shipments not given. |
| Published chart percentages | 16 labels | ANCHOR | Observable exhibit labels only, not independently observed physical output. |
| Unit identity | 1 EB = 10^9 GB; 8 bits = 1 byte | EXACT | Decimal convention adopted consistently. GB vs GiB in the product remains unverified. |

Source: [Meta Q2 2026 release, July 29](https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/).

## Calibration

Use the 50% adoption bars because their larger values reduce rounding noise:

- Users = 3.6bn x 50% = 1.8bn.
- Full DRAM stock = 1.8bn x 8 GB = 14.4 EB.
- Implied annual DRAM output = 14.4 / 41.1% = 35.0365 EB/year; choosing the round value 35 reproduces all four upper DRAM labels and all four lower labels.
- Full NAND stock = 1.8bn x 100 GB = 180 EB.
- Implied annual NAND output = 180 / 18.0% = 1,000 EB/year.
- Lower NAND intensity = 100 GB x (1.8% / 18.0%) = 10 GB/user. The interpretation 5 GB x 2 total copies is one chart-consistent construction, not a disclosed infrastructure specification.

Conditional on exact per-user assumptions and conventional rounding, all DRAM labels jointly permit approximately 34.9939–35.0365 EB/year. With lower NAND fixed at 10 GB/user, all NAND labels permit approximately 997.2299–1,002.7855 EB/year. These are **rounding-consistency intervals, not confidence intervals**. Matching other chart bars is an internal reproduction check, not external validation.

## Worked example: 25% adoption

1. Users: 3.60bn x 25% = **900m**.
2. Full DRAM: 900m x 8 GB = **7.2 EB**. Divide by one year's output of 35 EB: **20.57%**, displayed **20.6%**.
3. Lower DRAM: 900m x 25% resident x 2 GB = **0.45 EB**. Divide by 35 EB: **1.286%**, displayed **1.3%**.
4. Full NAND: 900m x 100 GB = **90 EB**. Divide by 1,000 EB: **9.0%**.
5. Lower NAND: 900m x 5 GB x 2 total copies = **9 EB**. Divide by 1,000 EB: **0.90%**.

The lower DRAM scenario is 16x smaller: (25% x 2 GB) / 8 GB = 1/16. The lower NAND scenario is 10x smaller: (5 GB x 2) / 100 GB = 1/10.

## What Meta actually confirms

Meta's launch and engineering descriptions, both September 8, 2026, confirm a dedicated cloud VM, persistence, external inference and continuous backups. The engineering post does not quantify RAM per VM, physical memory reservation, suspension/resume policy, storage quota, replication factor or NAND/HDD allocation. Background operation does not establish either 100% physical RAM residency or the chart's 25% assumption.

- [Meta launch, September 8](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)
- [Tarek Sheasha / Meta, engineering description, September 8](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)

This model concerns user VMs and files. It does not quantify shared inference weights, KV cache, accelerator HBM, training, host overhead, redundancy beyond the specified storage equivalent, or flash overprovisioning. DRAM and NAND percentages have different denominators and must not be added. Neither denominator establishes marginal available supply or scarcity in server DDR/enterprise SSDs.

## Sensitivity

Holding other exhibit inputs fixed, at 25% adoption:

| Hypothetical assumption change | Lower DRAM share of one year's output | Lower NAND share of one year's output |
|---|---:|---:|
| Exhibit inputs | 1.286% | 0.900% |
| Resident fraction 10% | 0.514% | 0.900% |
| Resident fraction 50% | 2.571% | 0.900% |
| Resident RAM 4 GB, resident fraction 25% | 2.571% | 0.900% |
| Nonresident VMs retain 1 GB, resident RAM 2 GB | 3.214% | 0.900% |
| Primary files 10 GB, 2 total copies | 1.286% | 1.800% |
| Primary files 5 GB, 3 total copies | 1.286% | 1.350% |

All changes above are illustrative ESTIMATES, not observed operational ranges. Adoption, active RAM and NAND-equivalent bytes scale their respective results proportionally. Resident fraction scales DRAM proportionally only when nonresident RAM is zero. Doubling the output denominator halves the corresponding percentage. A 25% smaller denominator raises the ratio by 33.3%; a 25% larger denominator lowers it by 20%.

## Stock-to-flow bridge

Annual physical purchases require a separate deployment schedule:

**Purchases during year = closing deployed capacity - opening deployed capacity + retirements - net transfers into the service + change in uninstalled inventory.**

Use matching physical capacity units and distinguish new procurement from repurposed hardware. A deployment spread over several years cannot be counted in full every year. NAND capacity retained is a stock; cumulative bytes written are a different metric. Do not add the resulting procurement estimate to a baseline forecast without checking whether the forecast already includes this use case. No annual purchase forecast is supplied because these inputs are unavailable.

## Checks and skeptic review

- **PASS — internal arithmetic:** all 16 screenshot labels reproduced at their displayed precision.
- **PASS — sourced distribution base:** 3.60bn Family DAP independently confirmed, not treated as current Muse users.
- **PASS — dimensional consistency:** decimal GB/EB; memory capacity separated from storage capacity; one year's output is the stated scale benchmark.
- **NOT VALIDATED — industry flow:** the exhibit supplies no traceable source/year for annual DRAM/NAND output. No comparable external validation of those denominators is claimed.
- **NOT VALIDATED — installed stock:** no reported Muse deployed memory stock or physical concurrency telemetry.
- **NOT VALIDATED — annual purchases:** no deployment ramp, procurement or reuse data.
- **CONDITIONAL — technical plausibility:** resident fractions are bounded 0–100% and capacities nonnegative; physical resource reservation and NAND-equivalent storage remain assumptions.
- **Skeptic:** independent double-check review, 2026-09-21: PASS on arithmetic; PARTIAL overall because source attribution, supply basis and real usage remain unverified.

The deliverable is an internally consistent reconstruction. Directional use-case sizing remains conditional on its load-bearing ESTIMATE inputs.
