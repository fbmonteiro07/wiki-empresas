# Industrial800VinDataCenters.pdf — figure transcription

Covers pages 2, 3, 6, 7, 9, 10. Machine transcription of figure pages (Baird deck, Tristan Gerra, Senior Research Analyst, tgerra@rwbaird.com | 415.593.8058). Transcribed 2026-07-02 for text search; verify against original PDF for load-bearing use.

## p.2 — 800V – AI Data Center Power (R)Evolution: "Data Center Roadmap — Architecting AI Infrastructure for Next-Gen AI Factories"

Two power-chain diagrams (Nvidia roadmap):

**2025 (today):** Utility / On-Prem Gen (optional, G) → Medium Voltage Network (13.8–35k VAC) → Diesel Gen → Main Switchboard → 480 VAC → AC UPS → 480 VAC → Power Distribution Unit → 415 VAC → AC Dist → 415 VAC → Energy Storage (optional) → Compute Rack (415 VAC → PSU → 54 VDC), rack size **3–4 MW**. Labeled "415 VAC Distribution".

**2027:** Utility / On-Prem Gen (G) / Battery Energy Storage System → Medium Voltage Network → 13.8–35k VAC → Medium Voltage Rectifier or Solid-State Transformer → 800 VDC → AC Dist → 800 VDC → Energy Storage → Compute Rack (800 VDC), rack size **Up to 8 MW**. Labeled "800 VDC Distribution".

Caption: "The top diagram shows today's data center, with multiple AC-to-AC conversions before being converted to DC at the compute rack. The bottom diagram shows the AI factory of the future, with a single AC-to-800 VDC conversion. 800 VDC is distributed within the data center and used directly by the compute rack. Read our 800 VDC whitepaper to learn more."

Source: Nvidia

## p.3 — 800V – AI Data Center Power (R)Evolution (2): power tree evolution (Navitas)

Three architectures with per-row metrics ("Navitas anchor products / capabilities" flagged along the chain):

| Architecture | Chain | Server rack | Energy efficiency | Typical power tree | Wideband Gap content per MW |
|---|---|---|---|---|---|
| Today: Centralized AC with rack-level AC-DC conversion | Utility grid → AC 13.8k/34.5k VAC → Transformer → AC 480 VAC → UPS, PDU… → AC 415 VAC → AC-DC PSU → DC 48 VDC busbar → IBC Conversion → DC 12VDC → VRM → DC 0.7xV → GPU | <250kW | 80–85% | 95+% Silicon-based | – |
| Short- to Mid-term evolution — 800V HVDC | Utility grid → AC 13.8/34.5k → Transformer → 480 VAC → 800 V DC Power side rack (AC-DC PSU, PDU, BBU…) → 800V DC → 800V DC Power distribution board → DC 48V/12V/6V → IBC conversion (if needed for 48V) → DC 12V/6V → VRM → 0.7xV → GPU | >250kW | Up to 90% | Significant GaN / SiC | $10K–$20K |
| Mid- to Long-term evolution — 800V HVDC | Utility grid → AC 13.8k/34.5 kVAC → Solid state transformer → DC 800V HVDC → 800V DC Power distribution Board → DC 12V/6V → VRM → 0.7xV → GPU | >600kW | Over 90% | Accelerating GaN / SiC | $25K–$35K |

Annotation: "SSTs to further accelerate demand for MV/HV power semis."
Note: PDU – Power Distribution Unit; PSU – Power Supply Unit; BBU – Battery Backup Unit; UPS – Uninterrupted Power Supply; IBC – Intermediate Bus Converter; VRM – Voltage Regulator Module.

Source: Navitas

## p.6 — GaN Power Device TAM

Headline: "GaN in Data Centers: $1B–2.1B TAM — 80–110% 5Y CAGR"

**Chart 1 — GaN power devices TAM, $M (stacked bars):**
- 2025: total 550 (mostly Mobile)
- 2030: total 3,600–4,700; CAGR 45–55%. Segments (2030): AI Datacenters 1,000–2,100; Performance Computing 400; Energy & Grid Infrastructure 200; Industrial Electrification 200; Mobile 1,200; Automotive (EVs) 550; Others 50.

**Chart 2 — Navitas SAM (GaN only), $M:** SAM excludes all EV on-board electronics and Mobile & Other markets.
- 2025: 130
- 2030: 1,800–2,900; CAGR 70–85%. Segments (2030) with CAGRs: AI Datacenters 1,000–2,100 (80–110%); Performance Computing 400 (110%); Energy & Grid Infrastructure 200 (60%); Industrial Electrification 200 (35%).

**Key growth drivers box:** AI Datacenters (datacenter HVDC power conversion and delivery, energy storage (BBUs, CBUs) etc.); Performance computing (high-power, high-density chargers as portable computers evolve with AI-native processing); Energy and grid infrastructure (HVDC transmission systems, grid-tied inverters in utility-scale renewable energy farms, BESS etc.); Industrial electrification (non-EV traction systems e.g. rail, heavy machinery, ATEs, high-efficiency industrial motor drives, robotics etc.).

Assumptions 2030: Penetration of non-commoditized GaN devices — Industrial: 85%; Computing and high-power delivery: 95%.

Source: Navitas, Yole, McKinsey

## p.7 — SiC Power Devices TAM

Headline: "SiC in Data Centers: $1.1B TAM — 40% 5Y CAGR"

**Chart 1 — SiC power devices TAM, $M (stacked bars):**
- 2025: total 5,700 — Automotive (EVs) 3,000; Industrial Electrification 1,400; AI Datacenters 200; Energy & Grid Infrastructure 1,100.
- 2030: total 10,450–11,200; CAGR 13–14% — Automotive (EVs) 5,000 (11% CAGR); Industrial Electrification 2,100 (8%); AI Datacenters 1,100 (40%); Energy & Grid Infrastructure 2,250–3,000 (15–22%).

**Chart 2 — Navitas SAM, $M:** SAM excludes all EV on-board electronics and all low-voltage SiC (i.e., below 750V).
- 2025: 200
- 2030: 1,700–2,450; CAGR 53–65% — Industrial Electrification 450 (45% CAGR); AI Datacenters 400 (45%); Energy & Grid Infrastructure 850–1,600 (65–87%).

**Key growth drivers box:** AI Datacenters (high-voltage AC/DC, DC/DC converters in datacenter power tree, BBUs, UPS, cooling systems etc.); Energy & grid infrastructure (SSTs for HVDC transmission, renewable grid integration e.g. utility-scale solar farms, BESS, PF correction systems etc.); Industrial electrification (non-EV traction systems e.g. rail, heavy machinery, ATEs, robotics, megawatt charger systems, high-efficiency industrial motor drives, high-power induction heating systems etc.).

Assumptions 2030: Penetration of non-commoditized GaN devices — Industrial: 85%, computing and high-power delivery: 95%.

Source: Navitas, Yole, McKinsey

## p.9 — How to Play the Theme Within Our Coverage: NVTS

Headline: "NVTS - GaN + SiC: 60-75% 5Y CAGR". Navitas SAM, $M.

**By product category (GaN / HV-UHV SiC stacked bars):**

| Year | GaN | HV/UHV SiC | Total |
|---|---|---|---|
| 2025 | 130 | 200 | 330 |
| 2026 | 263 | 398 | 661 |
| 2027 | 546 | 618 | 1,164 |
| 2028 | 910 | 851 | 1,761 |
| 2029 | 1,348 | 1,106 | 2,455 |
| 2030 (Base) | 1,800 | 1,700 | 3,500 |
| 2030 (High) | 2,900 | 2,450 | 5,350 |

CAGR 60–75% (2025→2030).

**By market segment ($M):**

| Segment | 2025 | 2030 (Base) | 2030 (High) | CAGR Base | CAGR High |
|---|---|---|---|---|---|
| AI Datacenters | 110 | 1,400 | 2,500 | 66% | 87% |
| Energy & Grid Infra. | 90 | 1,050 | 1,800 | 63% | 82% |
| Industrial Electrification | 120 | 650 | 650 | 40% | 40% |
| Performance Computing | 10 | 400 | 400 | 110% | 110% |
| Total | 330 | 3,500 | 5,350 | | |

Source: Navitas, Yole, McKinsey

## p.10 — Nvidia 800V Ecosystem

(no data content — logo wall of Nvidia 800V ecosystem partners: ABB, Alpha & Omega Semiconductor, Analog Devices, BizLink, Delta, Eaton, EPC, Flex, GE Vernova, Heron, Hitachi, Infineon, Innoscience, Lead Wealth, LiteOn, Megmeet, Mitsubishi Electric, MPS, Navitas, onsemi, Power Integrations, Renesas, Richtek, Rohm, Schneider Electric, Siemens, STMicroelectronics, Texas Instruments, Vertiv. Source: Nvidia)
