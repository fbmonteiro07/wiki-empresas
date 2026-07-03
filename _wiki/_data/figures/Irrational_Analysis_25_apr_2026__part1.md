# Irrational Analysis_25 apr 2026.pdf — figure transcriptions (part 1)

Pages covered: 3, 5, 7, 9, 10, 11, 12, 13, 14, 15, 17, 18.
Note: machine transcription of figure/chart pages for text search. Values transcribed as printed; no interpretation added.

## p.3 — Figure 20. GaNSafe Block Diagram

Block diagram of a GaNSafe (Navitas-style integrated GaN) power device, 4-pin package (VDRIVE, SK, Drain, Source). Right edge annotations partially cut off.
- Annotations: "100 V/ns Immunity with wide-range input (12~18V)"; "All pins 2kV HBM"; "Integrated VGS regulation maintains optimized VGS with reliability margin" (circled in the report author's markup); "Ultra-low quiescent current makes high-power GaN feasible in 4-pin package"; "Ultra-fa[st] Desa[turation…]" [cut off]; "N… induct…" [cut off]; "Inte… Clamp… bias… high… again…" [cut off].
- Internal blocks: ESD; Internal VCC Supply (ultra-low IQUIESCENT); Level Shift, Deglitch, UVLO, and Control; VGS Reg (highlighted in markup); PTAT; SCP, dV/dt; Miller Clamp P/D Block; Gate → GaN Power Device.
- Printed source line: none printed (figure caption "Figure 20. GaNSafe Block Diagram"; appears to be a vendor datasheet excerpt, vendor not printed on this crop).

## p.5 — Wolfspeed FY26 Q2 Earnings cover slide

(no data content — cover slide of a "Wolfspeed FY26 Q2 Earnings" deck, dated February 2026.)

## p.7 — Buck Converter Power Stage (TI application note excerpt)

Links printed on page: https://www.ti.com/lit/an/slva477b/slva477b.pdf ; https://www.ti.com/lit/slyy193
Author text: "For the purposes of this VERY OVERSIMPLIFIED, DIRRECTIONALY CORRECT explanation, I will be used a basic Buck converter." [sic]
Excerpt "1 Basic Configuration of a Buck Converter" with Figure 1. Buck Converter Power Stage (schematic: VIN, CIN, SW [circled in red markup], D, L, COUT, VOUT, IIN, IOUT).
"1.1 Necessary Parameters of the Power Stage": (1) Input voltage range: VIN(min) and VIN(max); (2) Nominal output voltage: VOUT; (3) Maximum output current: IOUT(max); (4) Integrated circuit used to build the buck converter.
Source: Texas Instruments application note SLVA477B (as linked).

## p.9 — Infineon datasheet comparison: CoolGaN G5 (IGT65R045D2) vs CoolSiC MOSFET 650V G2 (IMT65R050M2H)

Side-by-side Infineon final datasheets, both TOLL package, with "Table 1 Key performance parameters" from each:

CoolGaN Transistor 650 V G5, IGT65R045D2 (200 mm / 8-inch wafer technology):

| Parameter | Value | Unit |
|---|---|---|
| V(DS),max | 650 | V |
| V(DS,trans),max | 900 | V |
| R(DS(on)),max | 54 | mΩ |
| Q(G,typ) | 6 | nC |
| I(D,pulse) | 76 (highlighted) | A |
| Q(oss) @ 400 V | 45 | nC |
| Q(rr) | 0 | nC |

CoolSiC MOSFET 650 V G2, IMT65R050M2H (2nd-gen SiC trench):

| Parameter | Value | Unit |
|---|---|---|
| V(DSS) over full T(vjrange) | 650 | V |
| R(DS(on)),typ | 50 | mΩ |
| R(DS(on)),max | 62 | mΩ |
| Q(G,typ) | 22 | nC |
| I(D,pulse) | 114 (highlighted) | A |
| Q(oss) @ 400 V | 47 | nC |
| E(oss) @ 400 V | 6.3 | µJ |

Author text: "First observe the pulse current of the GaN part is 33% lower than the SiC part." / "Looking at the safe operating area, with lines added for the design requirements, we can learn something."
Source: Infineon final datasheets IGT65R045D2 and IMT65R050M2H (marked Public).

## p.10 — Safe operating area diagrams (GaN vs SiC)

Two log-log SOA charts with author-added green design-requirement lines:
- Diagram 3: Safe operating area (GaN, IGT65R045D2). Axes: ID [A] (10^-2 to 10^2) vs VDS [V] (10^0 to 10^3). Parameter curves: 20 ns, 1 µs, 10 µs, 100 µs, 1 ms, DC. Caption: ID=f(VDS); TC=25°C; D=0; parameter: tp.
- Diagram 2: Safe operating area (SiC, IMT65R050M2H). Axes: IDS [A] (10^-2 to 10^3) vs VDS [V] (10^0 to 10^3). Parameter curves: 1 µs, 10 µs, 100 µs, 1 ms, 10 ms, DC. Caption: IDS=f(VDS); TC=25 °C; D=0; parameter: tp.
Author text: "The GaN part needs to run at 1 MHz or faster, up to theoretically 50 MHz." / "The SiC part needs to run at 0.1 MHz or faster up to theoretically 1 MHz."
Source: Infineon datasheets (as p.9).

## p.11 — Inductor ripple current equation (TI app note excerpt)

Equation: Inductor Ripple Current ΔIL = ((VIN(max) − VOUT) × D) / (fS × L), with fS and L highlighted.
Definitions: VIN(max) = maximum input voltage; VOUT = desired output voltage; D = duty cycle calculated in Equation 1; fS = minimum switching frequency of the converter; L = selected inductor value.
Author text: "Inductor ripple scales inversely with switching speed and inductor size." / "Bigger inductor = more footprint = bad" / "Thus, higher switching frequency is desirable as it lowers footprint requirements for passive components." / "GaN wins here."
Source: Texas Instruments application note SLVA477B.

## p.12 — Output Capacitor Selection (TI app note excerpt)

Section "7 Output Capacitor Selection": best practice is low-ESR capacitors (ceramic X5R or better).
Equation (12): COUT(min) = ΔIL / (8 × fS × ΔVOUT), with fS highlighted. Definitions: COUT(min) = minimum output capacitance; ΔIL = estimated inductor ripple current; fS = minimum switching frequency of the converter; ΔVOUT = desired output voltage ripple.
Equation (13): ΔVOUT(ESR) = ESR × ΔIL.
Author text: "Similarly, bigger capacitor = more footprint = bad" / "Thus higher switching frequency is once again desirable." / "As an aside, larger passive components have larger parasitics. So a large capacitor will have intrinsically more effective-series-resistance // ESR."
Source: Texas Instruments application note SLVA477B.

## p.13 — Real capacitor equivalent-circuit model

Schematic: series ESR — capacitor C (with parallel resistance Rp) — series ESL.
Author text: "So why not just max out switching frequency?"
Source: not printed.

## p.14 — "What limits power density: switching losses" (TI white paper excerpt, text page)

Two-column text page (TI SLYY193-style white paper), key equations:
- Equation (2): PSW = 1/2 × CDS × (VDS)^2 × fSW
- Equation (3): PGATE = QG × VG × fSW
- Definitions (partly highlighted): CDS = MOSFET drain-to-source capacitance; VDS = MOSFET drain-to-source voltage; fSW = switching frequency; QG = gate charge; VG = gate-to-source voltage.
- Key limiting factor No. 2: reverse-recovery losses; Equation (4): ERR = (VIN × IL × tRR) + (VIN × QRR).
Highlighted text: increasing switching frequency causes increased switching losses and associated temperature rise, largely caused by a few dominant switching losses.
Source: Texas Instruments white paper (linked on p.7 as https://www.ti.com/lit/slyy193).

## p.15 — Psw (lower is better): parasitic switching power vs frequency, GaN vs SiC

Log-log chart, author-generated. Title: "Psw (lower is better)". X-axis: switching frequency 10^5 to 10^8 Hz; Y-axis: 10^11 to 10^15 (relative Psw units, unlabeled).
Series: red = IGT65R045D2 – GaN (plotted ~10^6 to ~5×10^7 Hz, rising from ~4×10^12 to ~2×10^14); blue = IMT65R050M2H – SiC (plotted ~10^5 to 10^6 Hz, rising from ~4×10^11 to ~4×10^12). The two lines meet at ~10^6 Hz.
Author text: "As you can see, GaN always loses at every switching frequency EXCEPT the tie where GaN is switching as slow as possible while SiC is switching as fast as [cut off]" / "At that point (Fsw), the Psw parastici is slightly better for GaN part due to slightly lower gate capacitance." [sic]
Source: author's own calculation from Infineon datasheet parameters.

## p.17 — Wolfspeed slide: "SiC CONTINUES TO TAKE MARKET SHARE IN HIGH VOLTAGE APPLICATIONS"

Bubble chart: Power = (Voltage x Current) on Y-axis (1 kW, 10 kW, 100 kW, 1 MW, 10 MW) vs Frequency on X-axis (1 kHz, 10 kHz, 100 kHz, 1 MHz, 10 MHz). Three overlapping market ellipses:
- Si: 2024 Market – $23B (low frequency, broad power range)
- SiC: 2024 Market – $3.4B (mid/high power, mid frequency)
- GaN: 2024 Market – $355M (lower power, high frequency)
Key Statistics box: "SiC is growing at a ~21% CAGR from 2026 to 2030, outpacing Si"; "Currently ~50% of Si market is addressable by SiC"; "SiC market is currently ~10x larger than GaN"; "SiC adoption is expected to accelerate in high voltage applications due to performance, reliability, and system cost savings."
Printed source line: "Source: Yole Power SiC 2025 – Markets and Applications, Status of the Power Electronics Industry 2025, Yole Power GaN 2025" (Wolfspeed FY26 Q2 earnings deck, Feb 2026).
Author text (cut off at right): "My view is GaN and SiC are BOTH valid and the details matter a lot. Only high-density (400W-class) GaN parts can properly compete with SiC in terms of [cut off]"

## p.18 — Author's GaN vendor comparison table

Table (author's own scorecard, colored cells; "Power Dissapation" [sic] column crossed out and Integrated Safety column bracketed in markup):

| Vendor | Part # | Rds_on | Power Dissapation | Integrated Safety | Vgs_th | Package |
|---|---|---|---|---|---|---|
| Nexperia | GAN080-650EBE | bad | ok | NO | ok | smallest |
| Infineon | IGT65R045D2 | ok | bad | NO | good | standard |
| Renesas | TP65H030G4PQS | good | bad | NO | bad | standard |
| Innoscience | INN650TA030AH | good | good | NO | ok | standard |
| Navitas | NV6524 | excellent | good | YES | Best (regulated) | standard |
| Texas Instruments | LMG365xR025 | excellent | ??? | YES | Best (regulated) | slightly larger |

Author text: "BUT, GaN has a ceiling. From my last post, recall that the highest end commercially available GaN parts are at 650V // 450 Watt where most are capped i[cut off]" / "Someone asked why I skipped POWI. Their datasheet is revolting and unreadable." / "ON claims to have vertical GaN capable of ~double that voltage at 1200V and presumably very high power density."
Source: author's own comparison (Irrational Analysis), from vendor datasheets.
