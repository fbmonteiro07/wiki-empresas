# Irrational Analysis_25 apr 2026.pdf — figure transcription (part 2: pages 20, 22, 23, 24, 25, 26)

Machine transcription of figure pages for text search. Report: "Irrational Analysis_25 apr 2026.pdf". Author: Irrational Analysis (Substack), 2026-04-25.

## p.20 — Infineon IMYH200R024M1H CoolSiC 2000 V SiC Trench MOSFET datasheet excerpt

Datasheet header: "IMYH200R024M1H — CoolSiC™ 2000 V SiC Trench MOSFET" (Infineon logo). Subtitle: "CoolSiC™ 2000 V SiC Trench MOSFET: Silicon Carbide MOSFET with .XT interconnection technology". Halogen-free mark; product photos (TO-247-style packages).

Features:
- V_DSS = 2000 V at T_vj = 25°C
- I_DCC = 89 A at T_c = 25°C
- R_DS(on) = 24 mΩ at V_GS = 18 V, T_vj = 25°C
- Very low switching losses
- Benchmark gate threshold voltage, V_GS(th) = 4.5 V
- Robust body diode for hard commutation
- .XT interconnection technology for best-in-class thermal performance
(section "Potential applications" cut off; "PRELI[MINARY]" watermark visible)

Absolute Maximum Ratings ("Stress beyond those listed under absolute maximum ratings may damage the device."):

| Parameter | Symbol | Rating | Unit |
|---|---|---|---|
| Drain-Source Voltage, across T_vj | V_DS(max) | 10000 (highlighted; likely a datasheet typo, printed as-is) | V |
| Maximum Gate-Source Voltage, Peak Transient Capability | V_GS(max) | -10/+25 | V |
| Static Gate-Source Voltage | V_GS(op) | -5/+20 | V |
| Continuous Drain Current¹ (T_c = 25°C) | I_DS | 20 | A |
| Continuous Drain Current¹ (T_c = 90°C) | I_DS | 15 (highlighted) | A |
| Pulsed Drain Current, t_p limited by T_vj(max) | I_DS(pulse) | 40 | A |
| Virtual Junction and Storage Temperature | T_vj, T_stg | -55 to +175 | °C |
| Maximum Processing Temperature, in non-reactive ambient | T_proc | 325 | °C |

Author caption below exhibit: "Very difficult to compare because the wolfspeed datasheet is preliminary and missing like 6 pages worth of charts."

Source: Infineon datasheet (IMYH200R024M1H), reproduced in Irrational Analysis 2026-04-25. No other printed source line.

## p.22 — Power dissipation as a function of case temperature limited by bond wire

Chart (from Infineon IMYH200R024M1H datasheet): P_tot = f(T_c). Y-axis: P_tot (W), 0–900. X-axis: T_c (°C), 0–175.
- Series R_th(j-c,max) (solid): flat at ~575 W from 0 to 25°C, then linear decline to 0 W at 175°C.
- Series R_th(j-c,typ) (dashed): flat at ~750 W from 0 to 25°C, then linear decline to 0 W at 175°C.

Source: Infineon datasheet, reproduced in Irrational Analysis 2026-04-25. No printed source line.

## p.23 — Maximum DC drain to source current as a function of case temperature limited by bond wire

Chart: I_DS = f(T_c). Y-axis: I_DS (A), 0–120. X-axis: T_c (°C), 25–175.
- Series R_th(j-c,max) (solid): ~89 A at 25°C, ~80 A at ~50°C, ~65 A at 100°C, ~50 A at ~130°C, falling steeply to 0 A at 175°C.
- Series R_th(j-c,typ) (dashed): ~102 A at 25°C, declining above the solid curve, converging to 0 A at 175°C.

Source: Infineon datasheet, reproduced in Irrational Analysis 2026-04-25. No printed source line.

## p.24 — Typical transfer characteristic

Chart: I_DS = f(V_GS); conditions V_DS = 20 V, t_p = 20 µs. Y-axis: I_DS (A), 0–1000. X-axis: V_GS (V), 0–28.
- Series T_vj = 25°C (solid): ~0 A up to ~4–5 V threshold, rising steeply from ~12 V (~200 A) to ~1000 A at 28 V.
- Series T_vj = 175°C (dashed): turns on earlier/softer, crosses the 25°C curve near ~12 V / ~180 A, then saturates around ~300 A at 28 V.

Source: Infineon datasheet, reproduced in Irrational Analysis 2026-04-25. No printed source line.

## p.25 — Typical on-state resistance as a function of junction temperature

Chart: R_DS(on) = f(T_vj); condition I_D = 40 A. Y-axis: R_DS(on) (mΩ), 0–80. X-axis: T_vj (°C), -50 to 175.
- Series V_GS = 18 V (solid): ~22 mΩ at -50 to 0°C, ~24 mΩ at 25°C, ~30 mΩ at 75°C, ~45 mΩ at 100°C, ~72 mΩ at 175°C.
- Series V_GS = 15 V (dashed): ~27 mΩ at -50 to 0°C, rising above the 18 V curve to ~76 mΩ at 175°C.
A second chart is cut off at the right edge (title/labels [illegible]).

Text below: "Subscribe for engineering-driven investment analysis."

Source: Infineon datasheet, reproduced in Irrational Analysis 2026-04-25. No printed source line.

## p.26 — (no data content — Substack footer page: Like/Comment/Restack buttons, "Pledge your support", Share buttons, © 2026, Unsubscribe, "Start writing")
