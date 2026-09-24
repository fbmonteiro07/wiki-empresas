# Source ledger — CPU to TSMC reconciliation — 2026-09-22

All figures below were read from the original page images. HARD means exact sourced figure, NOT a reported actual when the source is a broker estimate. PARTIAL means sourced range or approximate chart value. No company-disclosed server CPU revenue or realized average foundry invoice per CPU was found.

## UBS — Sunny Lin / Randy Abrams / Nicolas Gaudois — 2026-05-21

Report: Quantifying the server CPU opportunity. Original: `relatórios bons/CPU_TAM_-_UBS.html`; images `_assets/CPU_TAM_-_UBS/p001.jpg` through `p005.jpg` visually inspected. Tables on p.2.

Figure 1, bottom-up total market: 2025 23m units / $31bn; 2030 63m units / $173bn. The headline rounds to ~$170bn; the independent top-down framework is $168bn / 70m units. Use the $173bn denominator with the 63m-unit bottom-up model. All HARD-sourced broker estimates. Do not combine the top-down 70m units with bottom-up $173bn.

Figure 2:

| Metric | 2025 | 2027E | 2030E |
|---|---:|---:|---:|
| Total server CPU units, m/year | 23 | 38 | 63 |
| Arm architecture unit share | 16% | 32% | 42% |
| AMD unit share | 24% | 27% | 29% |
| Intel unit share | 60% | 40% | 29% |
| Arm advanced wafer demand, k/month | 6.1 | 21.0 | 65.7 |
| AMD advanced wafer demand, k/month | 11.8 | 27.6 | 56.7 |
| Intel advanced wafer demand, k/month | 53.3 | 60.9 | 78.3 |
| Industry wafer demand, k/month | 71.3 | 109.5 | 200.7 |
| TSMC wafer demand, k/month | 18.0 | 48.6 | 122.4 |
| TSMC wafer ASP, USD | 17,000 | 24,000 | 30,000 |
| TSMC server CPU revenue, USD m/year | 3,667 | 14,003 | 44,068 |
| Server CPUs / TSMC sales | 3% | 6% | 11% |

All cells HARD-sourced broker estimates. Model attribution: TSMC serves AMD + Arm, with no Intel server compute outsourcing. Arm here includes Nvidia / hyperscaler CPUs; it is not Arm Holdings royalty revenue. Row rounding: 2025 6.1+11.8=17.9 vs total 18.0; 18k*12*$17k=$3.672bn vs printed $3.667bn. 2030 122.4k*12*$30k=$44.064bn vs printed $44.068bn. Retain the printed $44.068bn for revenue normalization; tiny implied-ASP differences are rounding.

Source issue: Figure 1 gives 36m bottom-up units in 2027; Figure 2 gives 38m. 2027 shares sum to 99%. Do not use 2027 units to calibrate. 2025 and 2030 unit totals are consistent. Figure 14 p.5 TSMC total USD revenue $391.987bn for 2030 is a contemporaneous UBS forecast, not current consensus.

## Bernstein — Mark Li / Edward Hou / Yipin Cai — 2026-08-10

Report: TSMC: Higher revenue & capex on CPU. Original `relatórios bons/BERN_259272.html`; pp.2–4 visually inspected.

TSMC broad CPU revenue: 2023 $6–7bn; 2024 $11–12bn; 2025 $15–16bn (~13% of sales); 2026E ~ $25bn; 2027E high-$30bn, about 16% of total. PARTIAL ranges and approximate forecasts. Includes AMD, Apple, Amazon, Intel and newer CPU customers; explicitly discusses client CPU tiles. This universe is broader than UBS's server-only revenue.

2025 CPU customer mix: AMD 35–40%; Intel mid-30s%; others 25–35%. PARTIAL. Most CPUs do not carry TSMC advanced packaging; source identifies Venice packaging at ASE and Vera at Amkor (p.4). Exclude a generic CoWoS markup from server wafer demand.

## BofA — Vivek Arya / Duksan Jang / Michael Mani / Liam Pharr — 2026-08-12

Report: Rise of the agents: raising CPU TAM (again) to $210bn. Original `relatórios bons/Vivek_on_CPU.html`; pp.3,5,6 visually inspected.

Exhibit 3, 2030: total TAM $210.6bn (rounded; Exhibit 4 $210.637bn), 82.0m CPU units; AMD 24.9m units and $64.6bn revenue; Arm architecture 27.8m units and $99.7bn revenue; Intel 29.3m units and $46.3bn revenue. HARD-sourced forecast, rounded rows. Arm comprises merchant 17.7m units / $79.9bn and custom 10.1m units / $19.8bn. Merchant contains Nvidia, Arm Holdings own CPUs and Qualcomm; do not add Arm royalty sales. Custom CPU TAM uses BofA's imputed silicon value, not hyperscaler cloud revenue.

Exhibit 3: 2025 total units 29.9m, substantially above UBS's 23m; AMD 7.2m, Arm 4.1m, Intel 18.5m. Different vintage / universe estimates; do not silently overwrite UBS's denominator. BofA's 2030 unit mix is an independent forecast cross-check; attaching UBS foundry content is a hybrid house estimate, not a BofA TSMC forecast.

## Morgan Stanley — Charlie Chan / Daniel Yen / Daisy Dai / Tiffany Yeh et al. — 2026-08-24

Report: AI Supply Chain: Google ASIC, who gets what for design services? Original `relatórios bons/GLOBAL_20260824_1435.html`; cover and pp.7–10 visually inspected; Exhibit 12 p.9 contains the following 2027E front-end wafer figures.

Venice CPU: 5.670m units; 155 mm² compute die, 8 compute dies per CPU, 2nm; 227k front-end wafers; $30,000 per wafer; $6,804m front-end wafer revenue TAM. Vera CPU: 5.750m units; 850 mm², 1 compute die per CPU, 3nm; 228k front-end wafers; $27,300 per wafer; $6,229m wafer revenue TAM. HARD-sourced forecasts, rounded wafer counts. Packaging allocation is a separate column (270k Venice / 250k Vera); it is NOT front-end wafer consumption.

Derived independently from MS: Venice $1,200/CPU, Vera $1,083.30/CPU. Product-specific 2027E compute-wafer content checks order of magnitude of UBS's 2030 average AMD $1,117 and Arm $894; does not validate the fleet mix or prove a realized ASP. Figures exclude separately costed I/O dies, so scope remains narrower than a complete bill.

## Reported company anchor

TSMC FY2025 annual report: total revenue $122.42bn; 2025 HPC mix 58% (Q4 2025 earnings / annual reporting). HARD actual consolidated total. https://investor.tsmc.com/static/annualReports/2025/english/index.html . Useful for bounding CPU estimates, but does NOT identify actual CPU-only revenue and cannot validate a CPU-specific conversion rate.

## Excluded shortcut

Bernstein / Stacy Rasgon 2026-09-21, Intel meeting with John Pitzer, `BERN_260438.html` p.7: ~$15–20 wafer cost per $100 of revenue for a synthetic integrated AMD/TSMC company. Visually verified. This is not an identified TSMC foundry-sales take rate, is not a 2030 server-CPU-only ratio, and may eliminate intercompany foundry margin. Do not multiply a CPU TAM by 15–20% on this basis.

## Existing ledger errors discovered, not used in the calculation

`_wiki/_meta/assumptions.md:560` labels $4bn→$44bn as Arm-as-maker / Bernstein. Original UBS p.2 establishes this is TSMC server-CPU wafer revenue. At line 563 the suggestion that 200kwpm is cumulative is also incorrect: UBS p.2 explicitly labels it monthly wafer demand across all CPU producers in 2030; TSMC's subset is 122.4kwpm. These observations are recorded here without replacing the canonical page or its other research vintages.
