# Irrational Analysis_21 apr 2026.pdf — figure transcriptions (part 3)

Pages covered: 37, 38, 39, 42, 43, 44, 46, 48, 49, 51, 53, 54.
Note: machine transcription of figure/chart pages so the data is text-searchable. Values read from chart images; approximate where charts have no data labels.

## p.37 — GaN FET output characteristic curves: Nexperia and Infineon

Top pair (Nexperia datasheet excerpts, chart ids aaa-036222 / aaa-036223):
- Fig. 4: "Output characteristics: drain current as a function of drain-source voltage; typical values", Tj = 25 °C. Axes: I_D (A) 0–100 vs V_DS (V) 0–6. Curves for V_GS = 6V, 5V, 4V, 3V, 2V (V_GS=6V reaches ~80 A at V_DS ~4V).
- Fig. 5: same, Tj = 125 °C. Axes: I_D (A) 0–50 vs V_DS (V) 0–6. Curves for V_GS = 6V, 5V, 4V, 3V, 2V.
Source: Nexperia datasheet (vendor label overlaid: "Nexperia").

Bottom pair (Infineon datasheet excerpts):
- Diagram 7: "Typ. static* output characteristics" — I_D = f(V_DS); Tj = 25 °C; parameter: I_GS (curves: 33 mA, 8.3 mA, 1.7 mA, 3.3 mA, 1.7 mA, 0.33 mA, 0.17 mA). Axes: I_D [A] 0–140 vs V_DS [V] 0–10.
- Diagram 8: same at Tj = 125 °C. Axes: I_D [A] 0–100 vs V_DS [V] 0–10.
- Footnote: "* Refer to gate drive application note".
Source: Infineon datasheet (vendor label overlaid: "Infineon").

## p.38 — GaN FET output characteristic curves: Innoscience and Navitas

Top pair (Innoscience datasheet excerpts):
- Left: I_D = f(V_DS, V_GS); Tj = 25 °C. Axes: I_D (A) 0–180 vs V_DS (V) 0–6. Curves V_GS = 6V (~145 A at 6V), 5V, 4V, 3V, 2V.
- Right: I_D = f(V_DS, V_GS); Tj = 125 °C. Axes: I_D (A) 0–120 vs V_DS (V) 0–6. Curves V_GS = 6V (~100 A at 6V), 5V, 4V, 3V, 2V.
Source: Innoscience datasheet (vendor label overlaid: "Innoscience").

Bottom pair (Navitas datasheet excerpts):
- Fig. 3: I_DS vs. V_DS, T_JUNC = 25 °C. Axes: I_DS (A) 0–250 vs V_DS (V) 0–6. Single curve reaching ~225 A at 6V.
- Fig. 4: I_DS vs. V_DS, T_JUNC = 150 °C (temperature highlighted in original). Axes: I_DS (A) 0–150 vs V_DS (V) 0–6. Single curve reaching ~130 A at 6V.
Source: Navitas datasheet (vendor label overlaid: "Navitas").

## p.39 — GaN FET output characteristic curves: ROHM and Renesas

Top pair (ROHM datasheet excerpts):
- Left: I_D = f(V_DS, V_GS); Tj = 25 °C. Axes: Drain Current I_D [A] 0–200 vs V_DS [V] (Drain to Source Voltage) 0–8. Curves V_GS = 6V (~180 A), 5V (~140 A), 4V, 3V, 2V.
- Right: I_D = f(V_DS, V_GS); Tj = 125 °C. Axes: I_D [A] 0–140 vs V_DS [V] 0–8. Curves V_GS = 6V (~120 A), 5V, 4V, 3V, 2V.
Source: ROHM datasheet (vendor label overlaid: "ROHM").

Bottom pair (Renesas datasheet excerpts):
- Figure 2: "Typical Output Characteristics, TJ = 25°C", parameter: V_GS. Axes: I_DS [A] 0–250 vs V_DS [V] 0–10. Curves: 12V, 8V, 7V, 6V, 5V.
- Figure 3: "Typical Output Characteristics, TJ = 150°C", parameter: V_GS. Axes: I_DS [A] 0–150 vs V_DS [V] 0–10. Curves: 12V, 7V, 6V, 5V.
Source: Renesas datasheet (vendor label overlaid: "Renesas").

## p.42 — Gate-driver schematic (TI) and Navitas GaNSafe block diagram

Top: annotated gate-drive schematic (isolated driver + GaN block). Elements: PWM_H / FLT_H into isolator (ISO), transformer driver SN6505 (PWR/SGND), C_VDDH, R_INH, C_INH, FLT/RDRV, RDRV_sel_H, CDRV_sel_H, GND; blue block "Gate Driver + Protection" with VDD, slew rate, fault, "OCP, SCP, OTP, UVLO"; GaN device with DRN/SRC pins, current/voltage sensing, SW node, C_VCC, V_dc. Red annotation boxes: "Use high-side signal ground plane to shield traces"; "Minimize the capacitor loop to mitigate switching noises"; "to mitigate transient overvoltage". Source: Texas Instruments application material (part of author's comparison; author's purple highlight marks).

Bottom: "Figure 20. GaNSafe Block Diagram" (Navitas NV6524). Annotations: "100 V/ns Immunity with wide-range input (12~18V)"; "All pins 2kV HBM"; blocks: ESD, Internal V_CC Supply (ultra-low I_QUIESCENT), Level Shift/Deglitch/UVLO and Control, V_GS Reg, PTAT, Miller Clamp P/D Block, SCP dV/dt, Gate, GaN Power Device; pins V_DRIVE, SK, Drain, Source. Callouts: "Integrated V_GS regulation maintains optimized V_GS with reliability margin"; "Ultra-fast Short-Circuit Desat detection"; "No gate-loop inductance or ringing"; "Integrated Miller Clamp: negative gate bias not required, highest Reliability against Shoot-Thru"; "Ultra-low quiescent current makes high-power GaN feasible in 4-pin package". Source: Navitas NV6524 GaNSafe datasheet.

## p.43 — Navitas V_DRIVE pin text excerpt

(no chart/table — datasheet text excerpt plus author commentary)
Datasheet excerpt (Navitas NV6524): V_DRIVE pin is a patent-pending multi-function input for BOTH isolated PWM signal AND internal bias power for the GaN power IC. Requires isolated PWM with >=500mA output current and >=10V (absolute minimum). Recommended V_DRIVE >=11V. Typical V_DRIVE 12V to 13V when using Bootstrap for HS device; up to 15V when using isolated DC-DC supply for HS device.
Author commentary: "The Navitas part has a built-in regulator (very very nice feature) but requires Vdrive (Vg) to be rather high at 12-13V. Because of the internal regulation, I suppose the ripple requirements on Vdrive is not strict."
Source: Navitas NV6524 GaNSafe datasheet excerpt.

## p.44 — Navitas NV6524 reference schematic + recommended isolator ICs table

Top: "14.8. Reference Schematic" from Navitas GaNSafe NV6524 datasheet — dual NV6524E (Q1 high-side, Q2 low-side) half-bridge with Si8273BB isolator (U1, circled by author), R/C network (C1 15.0nF, C3 0.15uF, R3 1.00K, R6/R9 100R, C9/C10 100pF, C2 0.10uF, D3 ES1J, R2 10.0R, R1 1.00K, C11/C12 47.0pF, R5 4.99R, C8 1.00uF, R8/R7 10.0R/1.00K, D5/D6), bus caps C4–C7 0.22uF 650V 1210; nodes VIN, VSW, PGND. [some component values small/approximate]

Bottom: "14.9. Recommended Isolator IC's":

| Supplier | Isolated P/N | UVLO Setpoint | CMTI (V/ns) | Drive Strength | Channels |
|---|---|---|---|---|---|
| SkyWorks (Si Labs) | SI8273BBD-IS1 | VDDI: 1.85V / VDDO: 8.0V | 200 | 1.8A source/4A sink | Dual |
| SkyWorks (Si Labs) | SI8275BBD-IM1 | VDDI: 1.85V / VDDO: 8.0V | 200 | 1.8A source/4A sink | Dual |
| NovoSense | NSI6602VB-Q1SWR | VDDI: 2.5V / VDDO: 8.0V | 150 | 6A source/8A sink | Dual |
| NovoSense | NSI6602B-Q1SWR | VDDI: 2.35V / VDDO: 8.0V | 150 | 4A source/6A sink | Dual |
| Infineon | 2EDF8275F | VDDI: 2.75V / VDDO: 8.0V | 150 | 4A source/8A sink | Dual |
| Infineon | 1EDB8275F | VDDI: 2.7V / VDDO: 8.0V | 300 | 5A source/9A sink | Single |

Author commentary (bottom): "Ok ok this makes a lot more sense now. Inside the Navitas chip is a buffer (triangle) just like the TI part. They even have a helpful list of recommended dr[ivers…]" [text cut off at page edge]
Source: Navitas NV6524 GaNSafe datasheet.

## p.46 — Skyworks/Silicon Labs Si827x isolator functional description

Datasheet page "DATA SHEET — Si8271/Si8273/Si8274/Si8275", section 2.2 Functional Description. Text: Si827x channel operation analogous to optocoupler + gate driver but with modulated RF carrier instead of light; robust isolated data path, no special start-up considerations.
- Figure 8. Simplified Channel Diagram: Transmitter (dead-time control → modulator, RF oscillator) → Semiconductor-Based Isolation Barrier → Receiver (demodulator → driver, V_DD/Gnd, 4 A peak output) — input A to output B.
- Figure 9. Modulation Scheme: three traces — Input Signal (square wave), Modulation Signal (RF bursts, on/off keying), Output Signal (reconstructed square wave).
Source: Silicon Labs / Skyworks Si8271/Si8273/Si8274/Si8275 datasheet.

## p.48 — GaN vendor comparison scorecard (author's table)

Author's spec comparison table (color-coded scorecard):

| Vendor | Part # | Rds_on | Power Dissapation | Integrated Safety | Vgs_th | Package |
|---|---|---|---|---|---|---|
| Nexperia | GAN080-650EBE | bad | ok | NO | ok | smallest |
| Infineon | IGT65R045D2 | ok | bad | NO | good | standard |
| Renesas | TP65H030G4PQS | good | bad | NO | bad | standard |
| Innoscience | INN650TA030AH | good | good | NO | ok | standard |
| Navitas | NV6524 | excellent | good | YES | Best (regulated) | standard |
| Texas Instruments | LMG365xR025 | excellent | ??? | YES | Best (regulated) | slightly larger |

Below the table, section heading: "[6] Navitas GaNSafe, Shitco Bullshit Marketing or Real Feature?"
Source: author's own analysis (Irrational Analysis), compiled from vendor datasheets.

## p.49 — Navitas NV6524 GaNSafe functional description + block diagram

Navitas GaNSafe NV6524 datasheet, section 14 Functional Description / 14.1 GaNSafe Operation: Internally-regulated V_GS and Block Diagram. Key text: industry's first GaN power devices in industry-standard 4-pin package (Drain / Source / V_DRIVE / SK) with regulated V_GS and protection features. V_DRIVE pin: isolated PWM >=500mA and >=10V absolute minimum; recommended >=11V; typical 12–13V (bootstrap HS) or up to 15V (isolated DC-DC HS). Minimum On-Time: integrated 5V supply fed by V_DRIVE; t_ON_MIN 75ns. Internally regulated V_GS; negative gate bias not required (internal Miller Clamp). V_DS rating: Drain toggles between Source voltage and V_IN (650V maximum); non-repetitive pulses up to 800V for <100 us (V_DS(TRAN) rating). Isolated PWM IC: SI8273BBD-IS1 dual PWM driver (Sect. 14.8/14.9).
Bottom: same "GaNSafe Block Diagram" as p.42 (100 V/ns immunity, 12~18V input, all pins 2kV HBM, integrated V_GS regulation, short-circuit desat detection, integrated Miller Clamp callouts).
Source: Navitas NV6524 GaNSafe datasheet.

## p.51 — Infineon CoolGaN Drive HB 600 V G5 datasheet page

Infineon final datasheet IGI60L1414B1M (Public), "CoolGaN Drive HB 600 V G5" — 140 mOhm / 600 V GaN half-bridge with level-shift gate drivers.
Features: two 140 mOhm GaN switches in half-bridge with integrated high/low-side gate drivers (source/sink driving current +0.29 A / -0.7 A; configurable turn-on/off speed; integrated ultra-fast low-resistance bootstrap diode); fast input-to-output propagation (typ. 98 ns) with small channel-to-channel mismatch; PWM input; standard logic input levels; single gate driver supply voltage (typ. 12 V) with fast UVLO recovery; low-side open source for current sensing with external shunt; thermally enhanced 6 x 8 mm TFLGA-27 package; JEDEC-qualified for industrial applications.
Description: 140 mOhm (typ. R_dson) / 600 V enhancement-mode CoolGaN switches with integrated gate drivers; low-to-medium power; motor drives and SMPS. "When driven by a continuous gate current of a few mA in the 'on' state, a minimum on-resistance R_dson is always guaranteed."
Bottom: block diagram "CoolGaN Drive HB" — controller PWMH/PWML → INH/INL, logic level shift delay match, UVLO+logic per side, BS diode, GH/DH/VB, SW, GL/SL/VDD, C_boot, C_VDD, R_sense.
Source: Infineon IGI60L1414B1M final datasheet.

## p.53 — Brokerage P&L overview screenshot (author's trading account)

Screenshot (brokerage app, likely Webull), "P&L Overview", Range: 01/02/2026 – 04/21/2026 (YTD):
- P&L: +$906,062.49; P&L%: +85.80%; benchmark SMH: +28.83%.
- YTD Trend Analysis (P&L%): green line (account) ending at 52.59% [chart label]; orange line (SMH) ending at -1.20%. X-axis marks: 01/02, 02/27.
- YTD Realized P&L: -$36,798.42; YTD Dividends: -$380.00.
Note: account line label (52.59%) differs from headline P&L% (85.80%) as printed.
Source: author's brokerage account screenshot (Irrational Analysis).

## p.54 — Brokerage account value screenshot (author's trading account)

Screenshot, "Net Account Value": $1,881,241.91. Day's P&L: +$22,350.00 (+1.20%). Open P&L: +$1,458,168.63 (+76.70%). Market Value: $2,820,395.00. Cash Balance: -$939,153.09. Day-Trade BP: 1,928,172.64. Overnight BP: 390,720.72. Options BP: 195,360.36. Day Trades Left: Unlimited. Risk Level: Safe.
Source: author's brokerage account screenshot (Irrational Analysis).
