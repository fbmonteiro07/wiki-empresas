# House models registry

_Seeded 2026-07-06. THE rule: before building any estimate, CHECK THIS TABLE — if a house model already answers the question, start from it, not from memory. (Born from the 2026-07-06 optical audit FAIL: the Susq transceiver share matrix existed on disk while an analyst rebuilt it from memory.) Keep rows updated when models move or new ones land; model cards live in `_wiki/models/`._

| Model | Path | Answers | Key tabs | Updated |
|---|---|---|---|---|
| **AI Model (house master)** | `P:\Felipe Monteiro\US Equities\Modelos oficiais\AI Model.xlsx` (+ dated "comentado" snapshots) | AI capex, GW, accelerator units & designer revenue by client (NVDA/AMD/ASICs), CY23-28E | `Resumo \| Designers`, `Resumo \| Total`, `Bottom-up Capex`, clouds/labs | 2026-07-06 (comentado) |
| **Consolidado óptico (LITE/COHR/CIEN/GLW)** | `P:\...\Modelos oficiais\Modelo consolidado incl. LITE .xlsx` | Optical/transceiver industry + names; **Susq market tab = transceiver share matrix (BBG-sourced Innolight/Eoptolink)**; AI networking decomposition; AEC/650 | `Susq market`, `AI Networking Model`, `Inno + Eop`, `GLW Optical Oppty`, per-name model tabs | 2026-06-16 |
| **AI Chip Designers TAM** | `E:\AI_Demand_Capex\AI_Chip_Designers_TAM.xlsx` | Component TAMs (capex × BofA mix — 1.6-2.2x BofA scope, ceilings) + designer revenue + per-subsector company build-ups (CPU/HBM/switching/optical/copper/storage) | `Designers TAM`, `AI DC TAM (BofA mix)`, `Build \| *` | 2026-07-06 |
| **Memory S/D Base Case** | `E:\AI_Demand_Capex\Memory_Supply_Demand_Basecase.xlsx` | DRAM/NAND/HBM supply-demand, pricing (history+fwd), vendor P&L, scenarios — card: [memory-sd-basecase](../models/memory-sd-basecase.md) | `Memory Bible`, `Scenarios`, `Vendor P&L`, `DRAM/NAND S-D`, `Print tracker` | 2026-07-06 |
| **Comp sheet / models dashboard** | `P:\...\Comp Dashboard\` (publishes to Capstone-Wiki) | Fwd P/E bands, EPS revisions, house-vs-street per name | `build_modelos.py` / `build_dashboard.py` outputs | live |
| **Per-name official models** | `P:\...\Modelos oficiais\` (NVDA, AAPL, AVGO, COHR, META, TSM, GOOG, SemiCap v16) | House P&L per name — the numbers behind `house.json` / edge tracker | Summary tabs (see modelos dashboard config) | rolling |
| **Memory Apple BOM** | `E:\Wiki Felipe empresas\_wiki\models\memory-apple.html` (+ `memory-prices-bbg.csv`) | Memory content/cost in iPhone; inSpectrum price archive | single page + CSV | 2026-06-25 |

| **Bernstein DRAM SxD (reference)** | `E:\research-sources\reports\Bernstein SxD.xlsx` (orig. P:\Felipe Monteiro) | Broker reference: DRAM S&D 2009-2028, supply = wafers×density by vendor, demand = units×content by app. Their view: 2026 balanced, **2028 bust (+5% surplus, ASP −55%)** — replicated with house numbers in the Memory basecase tab `S&D \| Capstone engine` | `S&D`, `SR Client Version` | 2026-07-06 (Jun-26 vintage) |

_Candidates to add when they stabilize: MediaTek TPU model (edge tracker flagged "watch for house model init"), 800V/AI-power model (`E:\800V_Model`)._
