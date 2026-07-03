# Irrational_17 may 2026.pdf — figure transcriptions (part 3)

Pages covered: 46, 47, 48, 49, 51, 52, 53, 56, 57, 59, 60, 61.
Machine transcription of figure/chart pages so the data is text-searchable. Transcribed faithfully; no interpretation added.

## p.46 — Figure 7: Universal gate driving circuit for GIT and SGT based on RC interface (Infineon EiceDRIVER 2EDB7259Y) + TI/Navitas simplified block diagram

Two circuit schematics, no numeric data series.

1. **Infineon EiceDRIVER 2EDB7259Y schematic** — "Figure 7 Universal gate driving circuit for GIT and SGT based on RC interface". Blocks: Controller (VDD, PWM1, PWM2, GPIOx, GND pins; VDDI, INA, INB, DISABLE, GNDI), isolated driver with UVLO / TX-RX / Control Logic / Logic blocks on channels A and B (VDDA/OUTA, VDDB/OUTB/GNDB, 8V supplies), RC gate networks (Rcc, Rgff, Rgn, Cc) driving two GaN devices labeled GIT/SGT (D, G, SK, S pins; SW node). Source line: none printed (Infineon application material).
   - Body text: "Infineon tries to make your life easier by selling a custom GaN driver. Does the above schematic still look complicated? It is complicated!" / "Let's compare Infineon's solution with TI/Navitas."
2. **"Simplified Block Diagram"** (TI integrated GaN part): pins VDD, IN, FLT/RDRV, GND or LDO5V or ZVD or ZCD, DRN, SRC. Internal blocks: Gate Driver + Protection (VDD), Slew Rate, Fault, "OCP, SCP, OTP, UVLO" block with Current/Voltage sensing, GaN FET. Source line: none printed (TI datasheet material).

## p.47 — TI integrated GaN FET block diagram (detailed)

Circuit block diagram, no numeric data series. Body text: "TI integrates all the painful driver shit into the same package as the GaN FET. You just use simple PWM control as if this was a normal Si or SiC part."
Diagram pins: VDD, FLT/RDRV, IN, GND, DRN, SRC. Blocks: UVLO (+5V, VDD), Drive strength detection circuit, Thermal Shutdown, Die Temp Sensing, De-sat Protection, Overcurrent Protection, Gating logic control & level shifting, GaN FET. A red hand-drawn circle highlights the integrated negative gate voltage circuit (buffer/current-source stage). Source line: none printed (TI datasheet material).
Body text: "There is the integrated negative gate voltage circuit. All of it is done for you." / "Navitas has something very similar. Arguably better as they include extra protection circuity."

## p.48 — Navitas GaNSafe NV6524 datasheet excerpt (Functional Description)

1. **Package graphic**: "Top-cooled TOLT-16L" (Top / Bottom photos) + "Simplified Diagram" showing driver + GaN FET with Cooling Pad.
2. **Navitas GaNSafe NV6524 datasheet banner** and section "14. Functional Description / 14.1 GaNSafe Operation: Internally-regulated VGS and Block Diagram". Key printed datapoints:
   - Industry-standard 4-pin package (Drain / Source / V_DRIVE / SK); regulated VGS and protection & performance features (highlighted).
   - V_DRIVE pin: isolated PWM with >=500mA output current and >=10V (absolute minimum); recommended V_DRIVE >=11V; typical 12V–13V with bootstrap for HS device; up to 15V with isolated DC-DC supply for HS device.
   - Minimum On-Time: integrated 5V supply fed by V_DRIVE; t_ON_MIN = 75ns.
   - Internally regulated VGS turns ON gate with optimized voltage, turns OFF at 0V; negative gate bias NOT required — internal Miller Clamp keeps gate off during PWM OFF state (highlighted).
   - VDS Rating: Drain toggles between Source voltage and V_IN (650V maximum); withstands non-repetitive pulses up to 800V for <100 us; see sect. 6 for V_DS(TRAN) rating.
   Source: Navitas GaNSafe NV6524 datasheet.

## p.49 — Figure 20: GaNSafe Block Diagram + Miller clamp explanation circuits

1. **"Figure 20. GaNSafe Block Diagram"** (Navitas datasheet). Annotations: "100 V/ns Immunity with wide-range input (12~18V)"; "All pins 2kV HBM"; blocks: ESD, Internal Vcc Supply (ultra-low I_QUIESCENT), Level Shift/Deglitch/UVLO and Control, VGS Reg, PTAT, SCP dV/dt, Miller Clamp P/D Block, GaN Power Device; pins V_DRIVE, SK, Drain, Gate, Source. Callouts: "Integrated VGS regulation maintains optimized VGS with reliability margin"; "Ultra-fast Short-Circuit Desat detection"; "No gate-loop inductance or ringing"; "Integrated Miller Clamp: negative gate bias not required, highest Reliability against Shoot-Thru"; "Ultra-low quiescent current makes high-power GaN feasible in 4-pin package". Source: Navitas GaNSafe NV6524 datasheet.
2. **Miller clamp circuits a) and b)**: half-bridge with V_POWER (400V), C_MILLER, S2 (HS-Gate Voltage), S1 (LS-Gate Voltage), V_OUT, I_MILLER (red path), I_S1 (orange), V_G pulse; version b) adds comparator S3 with V_REF clamping the gate to ground. Source line: none printed.
   Body text: "Ah so it's just an extra transistor that that protects the gate driver by sending nasty pulses to ground. Seems similar in spirit to spamming Shockley diodes on all drive circuitry."

## p.51 — Infineon application note cover: "LLC design guide: 600 W converter"

Reproduction of Infineon Application Note AN_2110_PL52_2110_182323, "LLC design guide: 600 W converter — Simplified algorithm based on FHA and vector method", author Mladen Ivankovic, Lead Principal Engineer, V1.0, 2021-11-11, www.infineon.com/eval-600w-12v-llc-p7. Includes full table of contents (Introduction; Design-oriented analysis; Design steps; Design verification using LTspice; MOSFET selection — R_DS(on) selection, impact of C_o(tr), FHA calc vs LTspice). No chart data.
Author's comment: "These detailed guides and documents are public because the consequence of mistake is kaboom. You do not see this kind of stuff from TSMC floating on the free and open internet. :)"
Source: Infineon Application Note AN_2110_PL52_2110_182323.

## p.52 — Figure 1: Principle schematic of a half-bridge LLC converter

Infineon app-note page (Introduction / 1.1 Overview of the LLC resonant converter). "Figure 1 Principle schematic of a half-bridge LLC converter": Switching bridge (S1, S2, Vsw), Resonant tank (Cr, Lr, Lm), Transformer and rectifier (Np, Ns, Ns, D1, D2), Output capacitor (Co, Ro, Vo), waveform inset (VSW, t_d, I_Lr, I_Lm, ZCS Load Current, ZVS current I_Lm Primary, T_S). Source: Infineon Application Note AN_2110_PL52_2110_182323.
Author body text: "A LLC resonant converter consists of four parts: 1. Two strong SiC transistors. 2. A resonant tank consisting of one capacitor and two inductors. 3. A transformer+rectifier consisting of three inductors and two diodes. 4. At least one output filtering/decoupling capacitor." / "I will skip 14 pages of math and go directly to what we chare about, how the MOSFET selection effects the design."

## p.53 — Infineon app note section 5: MOSFET selection (equations)

Text/equation page from the Infineon LLC app note (section 5 / 5.1 Primary-side MOSFET R_DS(on) selection). Printed datapoints and equations:
- Conduction losses dominate on LLC switches (ZVS turn-on); MOSFET brings parasitic output capacitance C_o(tr) (highlighted).
- Eq (27): P_c = R_dson * I_rms^2
- Magnetizing current: i_m = I_pk * (4*t*f_sw − 1) for 0 <= t <= T_sw/2; Eq (28): I_pk = (n*V_o.nom)/(4*L_m*f_sw)
- Reflected secondary current: i_Rp = (pi/2) * I_o * sin(2*pi*f_r*t); Eq (29): I_o = P_o/(n*V_o.nom)
- Eq (30): I_pr.rms = sqrt((pi/(2*sqrt(2)) * I_o)^2 + I_pk^2/3) = 3.61 A
- Efficiency target eta = 97.5 percent; 20 percent of total LLC losses assigned to primary-side MOSFET conduction. Eq (31): R_dson.T * I_rms^2 = k_R * P_o, with k_R (conduction losses coefficient) typical value 0.005 or 0.5 percent.
- Eq (32): R_DS(on).T = R_DS(on) * k_T; R_DS(on) = MOSFET on-resistance at T_j = 25 C.
Source: Infineon Application Note AN_2110_PL52_2110_182323, p.16, V1.0, 2021-11-11.
Author body text: "Remember, Rds_on is the most important parameter. In general, lower is better…"

## p.56 — (no data content — stock photo of a high-voltage grid transformer at a substation; caption text: "(its not the power plant that blows up… its the grid itself…)" and "This is a high-voltage transformer. You have probably seen some of these at some point. They come in multiple sizes.")

## p.57 — (no data content — stock photo of multiple substation transformers; caption: "These are surprisingly simple devices. Basically giant inductors and capacitors.")

## p.59 — Solid-state transformer (SST) architecture + IEEE PES "Background" slide

1. **SST block diagram** (video screenshot): MV System → AC-DC Conversion → MV DC Link → High-Frequency Transformer (DC-DC Conversion) → LV DC Link → DC-AC Conversion → LV System. Source line: none printed (video still).
2. **IEEE PES presentation slide "Background" — Conventional Transformers vs. Solid-State Transformers**:
   - Conventional: Passive devices; ~99% efficient; Can introduce harmonics; Pass disturbances along; Very large footprint; Require 1+ year for replacement.
   - SST: Phase & frequency decoupling; Reactive power control (e.g., VAR support); Power quality management; Reduced footprint, deployment burden, and inventory overhead; Potential to correct phase imbalance; "DC in the middle" enables natural integration of DC-based IBRs (e.g., PV); Frequency insensitivity enables natural integration of variable frequency AC sources (e.g., wind).
   - Slide note: "Because of these advantages vs. conventional transformers, it is hypothesized that SSTs have potential to prevent/reduce cascading failures arising from severe events, thus improving grid resilience."
   - Side graphic shows grid chain: power plant → step-up transformer (12 kV) → 400 kV high-voltage transmission line → step-down transformer (substation, 13 kV) → step-down transformer (240 V), plus SST block chain.
   Source: IEEE PES presentation (logo printed).
   Author body text: normal transformers pass load-induced phase/voltage/current ripple along, leading to grid instability.

## p.60 — IEEE "Conclusions" slide on SST grid resilience

IEEE PES slide "Conclusions" (bullets, verbatim):
- The SST is an important step to creating a more resilient power grid to disturbances caused by multiple threat vectors, e.g., cyber-attacks and natural disasters (hand-annotated "AI")
- An SST modeling and control design methodology was presented
- A simulation example based on the IEEE RTS-96 3-area system compared a base case with no SST to the same base case except with an SST using the control design methodology
- The base case illustrated a weak connection between Area 3 and Areas 1 and 2 due to the severe disturbances leading to significant load shedding
- The base case with an SST showed significant improvements in reducing load shedding and improving frequency nadir vs. conventional transformer for the same events
- Future work: optimization strategies using SSTs to maximize grid resilience; robust control designs given parameter uncertainties and measurement noise
Source: IEEE PES presentation (logos printed).
Author body text: "SST never really took off because it was too expensive. Nobody wanted to pay a premium for load/voltage/current/phase regulation." / "**I am incredibly bullish SST. Way more bullish than the SiC/GaN companies themselves.**" / "Do you know what reactive power is?" (followed by video still: Keysight oscilloscope + miniature power-line diorama; no data).

## p.61 — Google search screenshot: "reactive power" (AI Overview)

Screenshot of a Google AI Overview for "reactive power" (no chart data):
- Definition: reactive power is a mathematical concept in AC electrical circuits representing energy that oscillates back and forth between the source and a load; performs no useful "real" work but is essential for maintaining voltage levels and sustaining magnetic and electric fields. (cited: Basic Electronics Tutorials +2)
- Video card: "What is Reactive power" — Flirting with Technology, YouTube, Jan 1, 2024; captions "Increase transmission losses, wasting energy and requiring larger conductors" / "Reduce the efficiency of power generation and distribution systems."
- The Three Types of AC Power: 1. Active Power (P) — watts (W)/kilowatts (kW), actual useful work; 2. Reactive Power (Q) — volt-amperes reactive (VAR)/kilovolt-amperes reactive (kVAR), establishes electromagnetic fields in transformers and induction motors; 3. Apparent Power (S) — volt-amperes (VA)/kilovolt-amperes (kVA), total combination of active and reactive power. (cited: Basic Electronics Tutorials +1; A. Eberle +4)
- Why Does It Matter?: insufficient reactive power → voltage drops, equipment failures, cascading blackouts (Ansys +2); too much reactive power circulating overloads wires and transformers (Reddit r/ElectricalEngineering).
Source: Google search AI Overview screenshot (as printed in the report).
