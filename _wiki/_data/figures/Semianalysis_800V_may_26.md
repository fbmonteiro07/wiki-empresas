# Semianalysis_800V_may 26.pdf — figure-page transcriptions

Pages covered: 9, 12, 20, 21, 28, 42, 44, 71, 73, 74.
Note: machine transcription of chart/figure pages (image-to-text) so the data is text-searchable. Attribution per printed source lines on each figure.

## p.9 — 800VDC adoption, 2025–2030 (bar + line chart) & Phase 1 white-space retrofit diagram

Chart: "800VDC adoption, 2025–2030"
- Left axis: Incremental Capacity (GW); Right axis: Penetration (%)
- Series: Retrofit (Sidecar) [orange bars], Facility-level [blue bars], Penetration % [green line]

| Year | Retrofit (Sidecar) GW | Facility-level GW | Penetration % |
|---|---|---|---|
| 2025 | ~0 | ~0 | ~0% |
| 2026 | ~0 | ~0 | ~0% |
| 2027 | 16.3 | ~0 | 38% |
| 2028 | 22.5 | ~2 [stacked top, unlabeled] | 60% |
| 2029 | 18.5 | 16.1 | 74% |
| 2030 | 12.5 | 25.9 | 78% |

Source: SemiAnalysis Industrials Model

Diagram: "Phase 1: White-space retrofit" — GREY SPACE (unchanged AC infrastructure): MV AC (Grid/BTM, 13.8–34.5 kVAC) → MV Switchgear → LV Transformer (415/480 VAC) → LV UPS (415/480 VAC) → AC Distribution → [415/480 VAC] → WHITE SPACE (HVDC power rack added): HVDC Power Rack (800 VDC) → IT Rack (Power Shelf). (No printed source line visible on this diagram itself.)

## p.12 — HVDC Side-Car Debug/Bring up (photo) + sidecar component table

Photo: "HVDC Side-Car Debug/Bring up" — sidecar rack front/back with callouts: AC-PDU (8 x 200A); DC-PDUs (4 x 54kW out); Power Shelves (180kW); BBU / CBU Shelves; HVDC Busbar; Crosslink to IT-Rack. Source: Rittal

Table (Source: SemiAnalysis):

| Component | Function |
|---|---|
| AC-PDU | Receives 200A AC whips from the tap box, distributes AC to the power shelves |
| AC-DC Power Shelves | Rectify 415-480V AC to 800VDC (or +/-400VDC bipolar per Mt Diablo) |
| BBU Shelves | Lithium-ion battery backup for ride-through during utility outage |
| CBU / Supercapacitor Shelves (optional) | Capacitor Backup Units. EDLC or HSC cells for peak buffering during GPU load transients |
| HVDC Busbar | Distributes 800VDC from the rectifier shelves to the DC-PDU output stage. |
| DC-PDU | Connects the HVDC busbar to multiple 50kW cables going to adjacent IT racks |
| Power Management / BMS | Rack-level controller managing cell health, charge cycles, thermal monitoring, and CAN/I2C communications |

Text below: sidecar evolved through OCP rack/power specs — ORv2 at 12V, ORv3 at 48V, HPR V1/V2 variants pushing single-rack 48V designs up to ~190 kW with liquid-cooled busbars and upgraded 72 kW power shelves.

## p.20 — Sidecar power rack TAM, 2026–2030 (bar + line chart)

Chart: "Sidecar power rack TAM, 2026–2030"
- Left axis: Revenue ($B); Right axis: Retrofit GW
- Series: Power Rack Revenue [bars], Incremental Retrofit GW [blue line]

| Year | Power Rack Revenue | Incremental Retrofit GW (read off right axis) |
|---|---|---|
| 2026 | $0.[illegible]B (~$0.1B) | ~0 |
| 2027 | $8.2B | ~16 |
| 2028 | $11.3B | ~22 |
| 2029 | $9.2B | ~18.5 |
| 2030 | $6.2B | ~13 |

Source: SemiAnalysis Industrials Model

Phase 1 Summary text: white-space retrofit delta estimated at roughly +$400-500k/MW vs current architectures, HVDC power rack the large majority.

## p.21 — Phase 1 power chain cost delta vs baseline (table) + Phase 2 diagram

Table: "Phase 1 power chain cost delta vs baseline" (Source: SemiAnalysis Industrials Model)

| Equipment | Baseline $M/MW | Phase 1 $M/MW | Delta $M/MW |
|---|---|---|---|
| MV Transformer | $0.35M | $0.35M | — |
| MV Switchgear | $0.70M | $0.70M | — |
| LV Transformer | $0.15M | $0.15M | — |
| LV Switchgear | $0.40M | $0.40M | — |
| Generator | $1.00M | $1.00M | — |
| Central UPS | $1.20M | $1.20M | — |
| Busway / PDU | $0.30M | $0.30M | — |
| Rack PDU | $0.05M | $0.00M | -$0.05M |
| Busbar | $0.00M | $0.05M | +$0.05M |
| HVDC Power Rack | $0.00M | $0.40M | +$0.40M |
| Power Shelf / PSU | $0.20M | $0.20M | — |
| TOTAL | $4.35M | $4.75M | +$0.40M |

Diagram: "Phase 2: 800V-native compute" (Source: SemiAnalysis Industrials Model) — GREY SPACE (LV UPS becomes operator-dependent): MV AC (Grid/BTM, 13.8-34.5 kVAC) → MV Switchgear → LV Transformer (415/480 VAC) → LV UPS (greyed, 415/480 VAC) → AC Distribution → [415/480 VAC] → WHITE SPACE (power shelf folded into compute blade): HVDC Power Rack (800 VDC) → IT Rack (On-Blade Power).

## p.28 — Phase 3: Where the AC Switchboard Function Lands (infographic)

Hand-drawn style infographic, "Three product categories absorb the split-and-protect function":
- Option (i): MW-Scale Rectifier with Integrated SSCBs — 800VDC feed → MW-Scale Rectifier (AC → 800VDC, SSCB per output) → to rack / to rack / to row / to row. "The rectifier becomes its own distribution device."
- Option (ii): DC Busway with Breaker-Equipped Tap-Offs — 800VDC feed → 800VDC Busway with Tap-off + DC breaker units → to rack/row. Warning: "Requires mature DC arc interruption." "Protection lives in the distribution medium itself."
- Option (iii): Prefabricated Grey-Space Pod — 800VDC feed → Factory-Built Skid (Rectifier + Switchboard + Busway) → to rack/row. "Bundled rectifier + switchboard + busway. Common in hyperscaler procurement."
Preceding text lists the same three categories. (No printed source line on the infographic.)

## p.42 — Novos Power SST product photo + spec strip

Spec strip: ≥98.5% Peak Efficiency | 1–50 MW Rated Power | DC 400–1500 V Supported DC Output Range. Photo of Novos Power SST cabinet. Source: Novos Power

Text ("Datacenter Layout Implications"): SST eliminates LV equipment at ~$0.55M/MW and Phase 2 rectifier at ~$0.20M/MW; estimated SST cost ~$1.0-1.5M/MW → first SSTs at upfront capex premium over directly replaced equipment.

## p.44 — SST market revenue, 2026–2030 (bar + line chart)

Chart: "SST market revenue, 2026–2030"
- Left axis: Revenue ($B); Right axis: Facility GW
- Series: SST Revenue [bars], Incremental Facility-Level GW [blue line]

| Year | SST Revenue | Incremental Facility-Level GW (read off right axis) |
|---|---|---|
| 2026 | ~0 | ~0 |
| 2027 | ~0 | ~0 |
| 2028 | $0.9B | ~1-2 |
| 2029 | $8.0B | ~16 |
| 2030 | $13.0B | ~26 |

Source: SemiAnalysis Industrials Model

Text ("Electrical System Cost"): total electrical content per MW stays in a $3.6-4.8M band across four of the five architectures modeled; main headline is content migration from grey space to white space.

## p.71 — Panasonic medium-term plan (datacenter sales outlook) + supply capabilities table

Chart: "Sales outlook for data-centers (including for generative-AI servers)" (yen: billions), stacked bars — Existing products (current BBU series: Backup, Peak-shaving) dark blue; Next-generation products (CBU, BBU for power racks) light blue. Approx values read off chart:

| Fiscal year | Total (¥bn, approx) | of which next-gen (approx) |
|---|---|---|
| FY3/25 | ~170 | 0 |
| FY3/26 | ~300 | 0 |
| FY3/27 | ~500 | small (~20) |
| FY3/28 | ~650 | ~100 |
| FY3/29 | ~810 | ~170 |

Notes: "Over 80% of sales through FY3/29 have been already received awards"; Award = projects agreed with customers to advance product development and secure future orders. Source: Panasonic

Table: "Strengthening supply capabilities" (Source: Panasonic)

| Region | Plan |
|---|---|
| Japan | Cell: expand production capacity to approx. 3x (vs. FY3/26); increase production lines at existing facilities and modify automotive lines (start of production FY3/27 1Q). Module: further enhancement of production capacity (with partner companies) |
| North America | Cell: utilize part of automotive base in Kansas, US (under review). Module: made decision on building a new factory, in addition to expansion of existing production lines at current factory (both in Mexico) |

Text: Musashi Seimitsu (7220 TYO), via subsidiary Musashi Energy Solutions (MES), holds essentially a monopoly in supercapacitors; pivoting into AI datacenter energy storage.

## p.73 — Bloom Energy conference slide photo: Role of Supercapacitors in Load Following

Photo of a projected PowerGen conference slide (Source: Bloom Energy). Legible elements: Bloom DC Energy Stamp [illegible, appears 15MW]; ±400Vdc; Bloom Inverter; Auxiliaries/AC Loads/AC Datacenter; DC Datacenter; Bloom Supercap Modules 2MW; power-vs-time chart showing ~1MW/2MW/3MW levels, supercapacitor power, discharge energy / charge energy, ~74s span; second chart of repeated load transients [values mostly illegible]. Host utility: CPS. Page footer: 73 Likes · 4 Restacks (Substack page furniture).

## p.74 — (no data content — Substack comments/footer page: "Write a comment...", © 2026 Dylan Patel, Substack links)
