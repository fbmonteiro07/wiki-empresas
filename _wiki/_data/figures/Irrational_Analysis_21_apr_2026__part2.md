# Irrational Analysis_21 apr 2026.pdf — figure transcriptions (part 2)

Pages covered: 19, 20, 22, 24, 27, 28, 30, 31, 32, 33, 35, 36.
Note: machine transcription of figure/chart pages (image OCR by Claude, 2026-07-02). All data reproduced from printed figures; attribution per printed source lines where present. Report author: Irrational Analysis (Substack), dated 21 Apr 2026. Subject: GaN power transistor vendor comparison (Navitas, Innoscience, Nexperia, Infineon, Renesas, ROHM, Texas Instruments).

## p.19 — Navitas GaNSafe NV6512C datasheet excerpt (package + simplified diagram)

(no numeric data content — datasheet cover graphic: "GaNSafe(TM) / NV6512C DATASHEET" banner; photo of "Bottom-cooled TOLL-4L" package (Top and Bottom views, Navitas GaNSafe Power IC); "Simplified Diagram" schematic with driver + GaN FET and cooling pad, FET circled in purple by the author. Source: Navitas NV6512C datasheet.)

## p.20 — Innoscience DFN package datasheet excerpt

(no numeric data content — Innoscience datasheet excerpt: partial caption "…stor in Dual Flat No-lead package (DFN) with…"; package renders showing pin labels D (drain, pins on one edge), S/SK/G (source, source-Kelvin, gate; pins 1, 8, 9 marked); transistor symbol schematic (G, SK, D terminals) circled in purple by the author. Source: Innoscience datasheet.)

## p.22 — Navitas NV6512C — 10. Electrical Characteristics table

Header: Navitas "Electrify Our World" / GaNSafe / NV6512C datasheet, section "10. Electrical Characteristics". Conditions unless otherwise specified: V_DS = 400V, V_DRIVE = 15V, T_CASE = 25°C, I_DS = 13A, R_DRIVE = 5Ω.

Author margin annotations (handwriting-style callouts): "Leakage current = wasted energy"; "Faster switching is better. Rise time in particular tends to be a pain point."; "Rds_on is most important. Lower is better. Parasitic capacitance also bad but can be mitigated."

| Symbol | Parameter | Min | Typ | Max | Units | Conditions |
|---|---|---|---|---|---|---|
| **Drive Pin Characteristics** | | | | | | |
| I_DRIVE_OPERATING | V_DRIVE operating current | | 3.3 | | mA | V_DRIVE = 15V, F_SW = 300kHz, 50% D.C., V_DS = 0V |
| I_DRIVE_LEAKAGE | V_DRIVE leakage current | | 1.5 | | mA | V_DRIVE = 15V |
| **Switching Characteristics** | | | | | | |
| t_ON | Turn-ON propagation delay | 24 | | 35 | ns | Fig 1,2; -40°C ≤ T_CASE ≤ +150°C; R_DRIVE = 1Ω |
| t_OFF | Turn-OFF propagation delay | 7 | | 13 | ns | Fig 1,2; -40°C ≤ T_CASE ≤ +150°C; R_DRIVE = 1Ω |
| t_ON_MIN | Minimum valid V_DRIVE on-time pulse duration (first PWM ON pulse) | 75 | | | ns | R_DRIVE = 5Ω |
| t_RISE | Turn-OFF rise time | | 8 | | ns | Fig 1,2; R_DRIVE = 1Ω |
| t_FALL | Turn-ON fall time | | 7 | | ns | Fig 1,2; R_DRIVE = 10Ω |
| **Short Circuit Protection (SCP)** | | | | | | |
| V_DS_SCP | V_DS(ON) Short Circuit Detect Threshold | 11.5 | 13.5 | | V | 18V ≥ V_DRIVE ≥ 11V, T_JUNC = -40°C to +150°C, verified by design |
| t_SCP_DLY_TURN-ON | Delay from Short Circuit Event to Soft Shut Down, into Turn-ON | | 350 | | ns | 18V ≥ V_DRIVE ≥ 11V, T_JUNC = -40°C to +150°C, verified by design |
| t_SCP_DLY_OPER | Delay from Short Circuit Event to Soft Shut Down, during Operation | | 50 | | ns | 18V ≥ V_DRIVE ≥ 11V, T_JUNC = -40°C to +150°C, verified by design |
| **GaN FET Characteristics** | | | | | | |
| I_DSS | Drain-Source leakage current | | 2.0 | 100 | µA | V_DS = 650 V, V_DRIVE = 0 V |
| I_DSS | Drain-Source leakage current | | 21 | | µA | V_DS = 650 V, V_DRIVE = 0 V, T_JUNC = 150 °C |
| R_DS(ON) | Drain-Source resistance | | 40 | 55 | mΩ | V_DRIVE = 15V, I_DS = 13 A |
| R_DS(ON) | Drain-Source resistance | | 94 | | mΩ | V_DRIVE = 15V, I_DS = 13 A, T_JUNC = 150 °C |
| V_SD | Source-Drain reverse voltage | | 3.3 | | V | V_DRIVE = 0 V, I_SD = 13 A |
| I_SD | Source-Drain reverse current | | 66 | | A | V_DRIVE = 0V, V_SD = 7V, 50µs pulse, based on P_DISSIPATION |
| Q_OSS | Output charge | | 59 | | nC | V_DS = 400 V, V_DRIVE = 0 V |
| Q_RR | Reverse recovery charge | | Zero | | nC | |
| C_OSS | Output capacitance | | 74 | | pF | V_DS = 400 V, V_DRIVE = 0 V |
| C_O(er) (Note 5) | Effective output capacitance, energy related | | 99 | | pF | V_DS = 400 V, V_DRIVE = 0 V |
| C_O(tr) (Note 6) | Effective output capacitance, time related | | 148 | | pF | V_DS = 400 V, V_DRIVE = 0 V |
| E_ON | Switching energy, Turn-ON | | 67 | | µJ | V_DS = 400 V, I_DS = 13 A, R_DRIVE = 10Ω |
| E_OFF | Switching energy, Turn-OFF | | 0.5 | | µJ | V_DS = 0 to 400 V, I_DS = 13 A, R_DRIVE = 2Ω |

Footnotes: (5) C_O(er) is a fixed capacitance that gives the same stored energy as C_OSS while V_DS is rising from 0 to 400 V. (6) C_O(tr) is a fixed capacitance that gives the same charging time as C_OSS while V_DS is rising from 0 to 400 V.
Printed source line: Navitas NV6512C Datasheet, p.5, Rev May 7th, 2025.

## p.24 — Fig. 7. Normalized R_DSON vs. T_JUNC (Navitas NV6512C datasheet)

Line chart. X-axis: T_J (°C), -50 to 150 (ticks every 25). Y-axis: Normalized R_DS(ON), 0.0 to 2.5. Curve (approximate read): ~0.6 at -50°C; ~0.8 at 0°C; 1.0 at ~25°C; ~1.3 at 50°C; ~1.45 at 75°C; ~1.6 at 100°C; ~1.85 at 125°C; ~2.2 at 150°C.
Source: Navitas NV6512C datasheet, Fig. 7.

## p.27 — Navitas parametric part-selector table (screenshot) + author selection criteria

Screenshot of Navitas website part table (columns: Part Number, Product Status, Application, Family, Type, VDS(V), VDS(Dyn), RDS(ON)typ. (mOhms), Package, Datasheet, 3D Model, Spice Model, Check Stock). All parts Industrial application, VDS 700 V continuous / 800 V dynamic:

| Part Number | Status | Family | Type | VDS(V) | VDS(Dyn) | RDS(ON) typ (mΩ) | Package |
|---|---|---|---|---|---|---|---|
| NV6247M | Active | GaNSense Motor Drive | Half-Bridge | 700 | 800 | 150 | PQFN 6 x 8 |
| NV6245M | Active | GaNSense Motor Drive | Half-Bridge | 700 | 800 | 275 | PQFN 6 x 8 |
| NV6269M | Active | GaNSense Motor Drive | Half-Bridge | 700 | 800 | 79 | PQFN 8 x 10 |
| NV6257 | New Release | GaNSense Motor Drive | Half-Bridge | 700 | 800 | 170 | PQFN 6 x 8 |
| NV6267 | New Release | GaNSense Motor Drive | Half-Bridge | 700 | 800 | 170 | PQFN 8 x 10 |
| NV6288 | New Release | GaNSense Motor Drive | Half-Bridge | 700 | 800 | 120 | PQFN 8 x 10 |
| NV6269C | Active | GaNSense | Half-Bridge | 700 | 800 | 79 | PQFN 8 x 10 |
| NV6247C | Active | GaNSense | Half-Bridge | 700 | 800 | 160 | PQFN 6 x 8 |
| NV6138C | Active | GaNSense | Single | 700 | 800 | 120 | PQFN 6 x 8 |
| NV6136C | Active | GaNSense | Single | 700 | 800 | 170 | PQFN 6 x 8 |
| NV6135C | Active | GaNSense | Single | 700 | 800 | 210 | PQFN 6 x 8 |
| NV6134C | Active | GaNSense | Single | 700 | 800 | 260 | PQFN 6 x 8 |
| NV6133C | Active | GaNSense | Single | 700 | 800 | 330 | PQFN 6 x 8 |
| NV6132C | Active | GaNSense | Single | 700 | 800 | 450 | PQFN 6 x 8 |
| NV6245C | Active | GaNSense | Half-Bridge | 700 | 800 | 275 | PQFN 6 x 8 |
| NV6156 | NRND | GaNSense | Single | 700 | 800 | 170 | PQFN 5 x 6 |

Author text: "Each has a lot of ... parts. To narrow the search and make comparisons as fair as reasonably possible: 1. Only parts with 650+ Vds continuous, 800V dynamic will be considered. 2. Pick lowest Rds_on part. 3. Attempt to match package type but probably will fail."
Source: Navitas website product selector (screenshot in report).

## p.28 — Vendor comparison table: lowest-Rds_on 650V-class GaN FET per vendor

Author-compiled comparison table (criteria continued: "4. Single FET parts only."). SpongeBob "Two Hours Later..." meme image above table.

| Vendor | Part # | Rds_on (25C) mΩ | Rds_on (150C) mΩ | Vds_max_cont (V) | Vds_max_trans (V) | Package | Comment |
|---|---|---|---|---|---|---|---|
| Nexperia | GAN080-650EBE | 60 | 135 | 650 | 800 | 8x8 DFN | Smallest package, bad Rds_on |
| Infineon | IGT65R045D2 | 45 | 96 | 650 | 900 | 9.9x10.4 TOLL | Highest margin of safety. |
| Renesas | TP65H03064PQS | 30 | 62 | 650 | | 9.9x10.4 TOLL | |
| Innoscience | INN650TA030AH | 26 | 55 | 650 | 800 | 9.9x10.4 TOLL | |
| Navitas | NV6524 | 18 | 43 | 650 | 800 | 9.9x10.4 TOLL | Best Rds_on |
| Texas Instruments | LMG365xR025 | 22 | 44 | 650 | 800 | 9.8x11.6 TOLL | Close to Navitas on Rds_on. Slightly larger package. |

Author text: "At a surface level, Navitas and TI are tied for first place. This is just based on Rds_on so don't be too quick to judge." Section [4.a] Power Dissipation begins: each transistor has a max power dissipation at 25C which degrades over temperature.
Source: author compilation from vendor datasheets (Irrational Analysis, 21 Apr 2026).

## p.30 — Power dissipation vs. case temperature derating curves (six vendors)

Grid of datasheet derating charts, each with author callout box giving max power dissipation at 25C and 100C:

| Vendor | P_diss @ 25C | P_diss @ 100C |
|---|---|---|
| Nexperia | 240 W | 96 W |
| Infineon | 131 W | 50 W |
| Innoscience | 462 W | 180 W |
| Navitas | 450 W | 180 W |
| ROHM | 291 W | 110 W |
| Renesas | 192 W | 75 W |
| Texas Instruments | (datasheet does not have this information) | — |

Chart details: Nexperia chart plots P_der (%) vs T_mb (°C), 0–200, with formula P_der = P_tot/P_tot(25°C) × 100%. Infineon: P_tot [W] 0–140 vs T_C 0–160°C. Innoscience: P [W] 0–500 vs T_C 0–150°C. Navitas: P_TOT (W) 0–500 vs T_C 0–150°C, "Fig. 12. P_DISSIPATION vs. T_CASE". ROHM: P_D [W] 0–350 vs T_C 0–150°C. Renesas: P_tot [W] 0–200 vs T_case 0–175°C. All curves flat to ~25°C then derate linearly to 0 at ~150°C (Renesas ~175°C).
Source: vendor datasheets (Nexperia, Infineon, Innoscience, Navitas, ROHM, Renesas), compiled by Irrational Analysis.

## p.31 — TI LMG365xR025 thermal recommendations excerpt + Safe Operating Region intro

(no chart data — text page.) Author: "Navitas and Innoscience are clear winners. Unfortunately, the TI datasheet does not have this information." Reproduces TI datasheet section 8.4.1.8 Thermal Recommendations for LMG365xR025 (lateral device on Si substrate; thermal pad connects to source; with high power dissipation PCB cooling alone may be insufficient; TI recommends heat sink on back of PCB; power planes, thicker copper, thermal vias, via capping, TIM, etc.). Section [4.b] Safe Operating Region: safety region defined by three parameters — 1. Vds (voltage across the switch), 2. Id (drain current), 3. Switching speed; "At higher switching speeds, more juice can safely flow."
Source: Texas Instruments LMG365xR025 datasheet section 8.4.1.8.

## p.32 — Safe operating area charts: Nexperia and Infineon

Three log-log SOA charts (I_D [A] vs V_DS [V]):
- Nexperia Fig. 2 ("Safe operating area; continuous and peak drain currents as a function of drain-source voltage"): I_D 10^-2 to 10^2 A, V_DS 1 to 10^3 V; curves labeled t_p = 10 µs, 100 µs, 1 mS, DC; note "Limit R_DSon = V_DS / I_D"; T_mb = 25°C; I_DM is a single pulse. Author callout: "Nexperia — 25C ONLY".
- Infineon Diagram 3: Safe operating area, I_D = f(V_DS); T_C = 25°C; D = 0; parameter t_p; curves 20 ns, 1 µs, 10 µs, 100 µs, 1 ms, DC; I_D 10^-2–10^2 A, V_DS 10^0–10^3 V.
- Infineon Diagram 4: Safe operating area, same but T_C = 125°C; curves 20 ns, 1 µs, 10 µs, 100 µs, 1 ms, DC; I_D 10^-3–10^2 A.
Source: Nexperia and Infineon datasheets.

## p.33 — Safe operating area charts: Innoscience, Navitas, Renesas, ROHM (+ TI note)

- Innoscience Figure 16 (SOA, I_D = f(V_DS), T_C = 25°C) and Figure 17 (T_C = 125°C): Drain Current (A) 0.1–1000 (Fig 16) / 0.1–100 (Fig 17) vs Vds 0.1–1000 V; curves 10µs, 100µs, 1ms, DC; "Limit by Rdson"; BVDSS limit line.
- Navitas Fig. 14 "Safe Operating Area, T_CASE = 25°C": I_DS (A) 0.1–100+ vs V_DS (V) 0.1–1000; curves 10µs, 100µs, 1ms, DC. Author callout: "Navitas — ONLY 25C".
- Renesas Figure 14 "Safe Operating Area T_C = 25°C": Ids [A] vs Vds [V]; curves 1µs, 10µs, 100µs. Author callout: "Renesas — ONLY 25C".
- ROHM Fig.3 (Max. Safe Operating Area, I_D = f(V_DS, P_W); T_C = 25°C) and Fig.4 (T_C = 125°C): Drain Current I_D [A] 0.01–100 vs V_DS [V] 0.1–1000; pulse-width curves P_W = 1µs, 10µs, 100µs, 1ms, 10ms; Single Pulse. Author callout: "ROHM — 125C, not 150C".
- Author note box: "TI datasheet does not have this but their part can operate up to 175C junction temperature. This is impressive and above everyone else."
Source: Innoscience, Navitas, Renesas, ROHM datasheets.

## p.35 — Generic FET characteristic curves (I_drain vs E_drain-to-source)

Educational chart (no vendor data). Y-axis: I_drain; X-axis: E_drain-to-source. Regions: Ohmic region / Below pinch-off Triode region vs Above pinch-off Saturation region, separated by dashed boundary |V_DS| = |V_P| - |V_GS|. Curves for V_gate-to-source = 0 V (highest), 0.5 V, 1 V, and 2 V = V_p (pinch-off, zero current). Source line not printed (textbook-style illustration).

## p.36 — NMOS/PMOS operating-region equation table

| Region | NMOS | PMOS |
|---|---|---|
| Cutoff | V_GS < V_TN; I_D = 0 | \|V_GS\| < \|V_TP\|; I_D = 0 |
| Triode | V_GS ≥ V_TN and V_DS < V_GS − V_TN; I_D = K_n(V_GS − V_TN − V_DS/2)·V_DS | \|V_GS\| ≥ \|V_TP\| and \|V_DS\| < \|V_GS\| − \|V_TP\|; I_D = K_p(\|V_GS\| − \|V_TP\| − \|V_DS\|/2)·\|V_DS\| |
| Saturation | V_GS ≥ V_TN and V_DS ≥ V_GS − V_TN; I_D = (K_n/2)(V_GS − V_TN)^2 | \|V_GS\| ≥ \|V_TP\| and \|V_DS\| ≥ \|V_GS\| − \|V_TP\|; I_D = (K_p/2)(\|V_GS\| − \|V_TP\|)^2 |

Author text below table: "At one point in time I knew this... how to read the charts. Some of the vendors did a ... job at plotting this stuff... the gate controls the switch so you can either plot the transistor characteristic curves at various Vgs values or Igs. Both are valid." Source line not printed (textbook-style table).
