# Irrational_17 may 2026.pdf — figure transcriptions (part 2)

Pages covered: 27, 28, 32, 33, 34, 37, 38, 39, 40, 41, 44, 45.
Machine transcription of figure/chart pages so the data is text-searchable. Transcribed faithfully from page images; no interpretation added. Source: "Irrational_17 may 2026.pdf" (Irrational Analysis, irrationalanalysis.substack.com, May 17 2026 report).

## p.27 — Infineon datasheet diagrams 5–8 (typ. output characteristics and Rds_on)

Four datasheet diagrams (Infineon part; author notes Infineon recommends 18V drive voltage for this part).

- Diagram 5: Typ. output characteristics. Ids=f(Vds); Tj=25 °C; parameter: Vgs. X: Vds [V] 0–20; Y: Ids [A] 0–200. Curves for Vgs = 20 V (~185 A at 20 V), 18 V (~155 A), 15 V (~95 A), 12 V (~50 A), 10 V (~25 A), 8 V (~5 A).
- Diagram 6: Typ. output characteristics. Ids=f(Vds); Tj=175 °C; parameter: Vgs. Same axes. Curves 20 V (~140 A at 20 V), 18 V (~120 A), 15 V (~85 A), 12 V (~50 A), 10 V (~30 A), 8 V (~8 A).
- Diagram 7: Typ. drain-source on-state resistance. Rds(on)=f(Ids); Tj=125 °C; parameter: Vgs. X: Ids [A] 0–200; Y: Rds(on) [Ω] 0.060–0.160. Curves for Vgs = 10 V, 12 V, 15 V, 18 V, 20 V (Rds(on) ~0.065–0.070 Ω at low current for 18–20 V, rising with current; lower Vgs curves rise steeply).
- Diagram 8: Drain-source on-state resistance. Rds(on)=f(Tj); Id=18.2 A; Vgs=18 V. X: Tj [°C] -50 to 175; Y: Rds(on) [normalized] 0.5–2.0. Curve rises from ~0.95 at -50/-25 °C through 1.0 at ~25 °C to ~1.65 at 175 °C.

Page text: "Each curve corresponds to a gate drive voltage. Remember that Infineon recommends a drive voltage of 18V for this part." / "Parasitic resistance varies due to many factors, but the one we care about the most is temperature." / "Also handy reference for parasitic capacitance."

Source line: none printed (Infineon datasheet diagrams reproduced by the author).

## p.28 — MOSFET parasitic capacitance diagram; section [4] Datasheet Comparisons

- Diagram: MOSFET equivalent circuit with parasitic capacitances between Gate (G), Drain (D), Source (S): Cgd, Cgs, Cds.
- Definitions printed: Input capacitance (Ciss) = Cgd + Cgs; Output capacitance (Coss) = Cds + Cgd; Reverse transfer capacitance (Crss) = Cgd.
- Section header "[4] Datasheet Comparisons" followed by a meme image ("SHOW ME WHAT YOU GOT!", Rick and Morty).
- General Rules for the comparison: 1. Only compare discrete MOSFETs (no compound devices such as half bridge). 2. Chose the lowest Rds_on part from each vendor.

Source line: none printed.

## p.32 — Navitas CEO quote + meme

(mostly no data content — transcript screenshot plus meme)

Screenshot of transcript quote, Chris Allexandre, President and CEO [Navitas], timestamp 0:06:34: "Navitas is uniquely positioned as one of the very few companies that can claim deep long-term experience in both GaN and high voltage SiC technologies. We're also agnostic and readily offer customers the ability to choose the optimal solution for their specific application [glass puicture]. As a result of our proven capability in both SiC and GaN, we believe it allows us to address more of the power chain and ultimately capture greater content per system. Briefly profiling the trends and opportunities specific to each of our four targeted end markets, starting with AI data center."

Below: "See? Nobody cares." meme captioned "Hey this guy has GaN and SiC!"

## p.33 — memes; section header [4.b] SiC 1200V-class

(no data content — two memes: "YOUR SIC IS BAD AND YOU SHOULD FEEL BAD" (Futurama Zoidberg) and a three-headed dragon meme with vendor logos Infineon + STMicroelectronics / Wolfspeed + onsemi / Navitas (derpy head). Page ends with section header "[4.b] SiC 1200V-class".)

## p.34 — Table: 1200V Class SiC Power Device Landscape

Table header notes: "All values at 100C. Assume Vds = 800V." Watermark/logo: irrationalanalysis.substack.com.

| Vendor | Part# | Package | Tech | Integrated Driver? | Vds_max (V) | Rds_on (mOhm) | Max Power Dissapation (W) | Crss (pF) | Coss (pF) | Ciss (pF) | Eoss (uJ) | Qoss (nC) | Comment |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Infineon | IMCQ120R004M2H | Q-DPAK | SiC | No | 1200 | 5.5 | 750 | 50 | 600 | 20000 | 242 | 898 | Capacitance at 0.1 MHz. Counterintuitivly, this part is the best because of super low Rds_on and very high power density. |
| Navitas | G4R12MT12U | HV-T2PAK | SiC | No | 1200 | > 12 | Private datasheet. Rds_on is shit anyway so not gona bother. | | | | | | |
| Renesas | (row) | | | | They exited SiC due to losses. Have a deal with Wolfspeed. | | | | | | | | LOL |
| STM | SCTHC250N12G3AG | STPAK HC | SiC | No | 1200 | 10.5 | 560 | 30 | 350 | 7000 | ? | ? | Capacitance at 1 MHz. Weird package. |
| On Semi | NVBG022N120M3S | D2PAK7 | SiC | No | 1200 | 31 | ? | 15 | 150 | 3000 | ? | ? | Capacitance at 1 MHz. Wrong package. |
| Wolfspeed | C4M502512QJ2 | TO-263-7 XL | SiC | No | 1200 | 32.5 | 210 | 5 | 200 | 3000 | 45 | ? | Capacitance at 0.1 MHz |
| Nexperia | NSF017120T1A0 | Q-DPAK | SiC | No | 1200 | 22 | 240 | 5 | 250 | 5000 | 90 | 345 | Capacitance at 0.5 MHz |
| ROHM | SCT4018KE | TO-247N | SiC | No | 1200 | 29 | 150 | 9 | 150 | 5000 | > 50 | ? | Eoss at 25C. Capacitance at 1 MHz. Very wrong package. |
| Toshiba | TW015N120C | TO-247N | SiC | No | 1200 | 18 | 210 | 8 | 300 | 6000 | 110 | ? | Capacitance at 1 MHz. Wrong package. |
| Fuji Electric | (row) | | | | Their website is very confusing. I cannot find datasheets for discrete FETs. | | | | | | | | |
| Semiq | GP3T016A120TS | TSPAC | SiC | No | 1200 | 19 | 140 | 20 | 200 | 7000 | 85 | ? | Capacitance at 0.2 MHz |
| Sanan | SMS1200014M3 | TO-247N | SiC | No | 1200 | 13 | 250 | 10 | 200 | 5000 | 80 | ? | Capacitance at 0.1 MHz. Wvery wrong package. |
| Power Integ | (row) | | | | Highly integrated. I have no idea how to properly compare or evaluate these devices. Datasheets missing all the info I am looking for. | | | | | | | | |

Page text: "Thankfully the higher voltage we go, the fewer players there are so these tables are less painful to make." / "Infineon wins with extraordinarily low Rds_on. The capacitance numbers are huge but so is the density. This thing can handle insane power in a single, compact device with proper topside cooling."

Also on page: package drawing with pin labels 1, 2, 3-11, 12-22.

Source line: irrationalanalysis.substack.com table (author-compiled from vendor datasheets).

## p.37 — Infineon FF1000UXTR23T2M1P datasheet page (XHP 2 module)

Infineon final datasheet excerpt: "XHP™2 module with CoolSiC™ Trench MOSFET and NTC / pre-applied thermal interface material".

- Electrical features: Vdss = 2300 V; Idn = 2000 A / Idrm = 4000 A; high current density; low inductive design; low switching losses; Tvj,op = 175 °C.
- Mechanical features: substrate for low thermal resistance; copper base plate; high creepage and clearance distances; high power density; package with CTI > 600; pre-applied thermal interface material.
- Potential applications: central inverter, wind power generation, energy storage systems, industrial drives, traction drives, DC/DC converter, high-power converters, high-frequency switching application.
- Product validation: qualified for industrial applications according to relevant tests of IEC 60747, 60749 and 60068.
- Description: circuit diagram of half-bridge module (two power transistors + NTC).

Page text: "See the two power transistors? This does not count. Infineon SiC stops at 2000V under my definition." / "So… let's take a look at the Wolfspeed datasheet in detail."

Source line: Infineon datasheet (logo printed on page).

## p.38 — Wolfspeed CPM3-10000-0300A bare die datasheet excerpt

- Title: CPM3-10000-0300A — SiC 10 kV, 305 mΩ MOSFET Bare Die.
- Description: "This high-performance silicon carbide MOSFET die is developed to maximize the performance and simplify the design architecture of mid and high-voltage applications. This device can be implemented into any custom package providing additional design flexibility."
- Table: Part Number CPM3-10000-0300A; Die Size (mm) 8.1 × 8.1. Pin diagram: G-Gate, S-Source, D-Drain.
- Typical Applications: Pulsed Power; Medium-Voltage Drives; Solid-State Transformers; Smart Grid/Grid-Tie Distributed Generation; Medium-Voltage UPS Systems; Nuclear Power Generation for AI Data Centers (highlighted).

Page text: "Bare die is fine given how crazy this part is." / "Really guys? You reaching here lol."

Source line: Wolfspeed datasheet (marked PRELIMINARY watermark).

## p.39 — Wolfspeed CPM3-10000-0300A Absolute Maximum Ratings table

"Stress beyond those listed under absolute maximum ratings may damage the device."

| Parameter | Symbol | Rating | Unit |
|---|---|---|---|
| Drain-Source Voltage, across Tvj (highlighted) | Vds(max) | 10000 (highlighted) | V |
| Maximum Gate-Source Voltage, Peak Transient Capability | Vgs(max) | -10/+25 | V |
| Static Gate-Source Voltage | Vgs(op) | -5/+20 | V |
| Continuous Drain Current (Note 1) | Ids, Tc = 25 °C | 20 | A |
| Continuous Drain Current (Note 1) | Ids, Tc = 90 °C | 15 | A |
| Pulsed Drain Current, tp limited by Tvj(max) | Ids(pulse) | 40 | A |
| Virtual Junction and Storage Temperature | Tvj, Tstg | -55 to +175 | °C |
| Maximum Processing Temperature, in non-reactive ambient | Tproc | 325 | °C |

Note 1: Assume testing at Vgs = +20 V, with a junction-to-case thermal resistance R_TH(J-C) = 0.34 °C/W.

Page text: "Remember you never want to be anywhere close to Vds_max. Let's get a clue on what voltage Wolfspeed recommends for this part."

Source line: Wolfspeed datasheet (PRELIMINARY watermark).

## p.40 — Wolfspeed CPM3-10000-0300A Electrical and Body Diode Characteristics tables

Electrical Characteristics (Tvj = 25 °C unless otherwise specified):

| Characteristics | Symbol | Min. | Typ. | Max. | Unit | Test Conditions | Note |
|---|---|---|---|---|---|---|---|
| Drain-Source Breakdown Voltage | V(BR)DSS | 10 | | | kV | Vgs = 0 V, Ids = 100 µA | |
| Gate Threshold Voltage | Vgs(th) | 1.8 | 2.8 | 3.5 | V | Vds = Vgs, Ids = 1 mA | |
| Gate Threshold Voltage | Vgs(th) | | 2.1 | | V | Vds = Vgs, Ids = 1 mA, Tvj = 175 °C | |
| Zero Gate Voltage Drain Current | Idss | | 1 | 10 | µA | Vds = 10 kV, Vgs = 0 V | |
| Gate-Source Leakage Current | Igss | | 20 | | nA | Vgs = 20 V, Vds = 0 V | |
| Drain-Source On-State Resistance | Rds(on) | | 305 | 380 | mΩ | Vgs = 20 V, Ids = 15 A | Fig. 1 |
| Drain-Source On-State Resistance | Rds(on) | | 1113 | | mΩ | Vgs = 20 V, Ids = 15 A, Tvj = 175 °C | |
| Transconductance | gfs | | 8.1 | | S | Vds = 30 V, Ids = 15 A | Fig. 5 |
| Transconductance | gfs | | 5.3 | | S | Vds = 30 V, Ids = 15 A, Tvj = 175 °C | Fig. 5 |
| Turn-On Switching Energy, Tj = 25/125/175 °C | Eon | | 22.8 / 20.9 / 22.4 | | mJ | Vds = 6000 V (highlighted), Vgs = -5/+15 V, ID = 15 A, RG(ext) = 25 Ω, timing relative to Vds, inductive load | Fig. 13, 14, 15 |
| Turn-Off Switching Energy, Tj = 25/125/175 °C | Eoff | | 1.4 / 1.4 / 1.5 | | mJ | same | Fig. 13, 14, 15 |
| Input Capacitance | Ciss | | 8136 | | pF | Vgs = 0 V, Vds = 3000 V, f = 100 kHz, Vac = 25 mV | Fig. 10, 11 |
| Output Capacitance | Coss | | 76 | | pF | same | Fig. 10, 11 |
| Reverse Transfer Capacitance | Crss | | 3.4 | | pF | same | Fig. 10, 11 |
| Coss Stored Energy | Eoss | | 342 | | µJ | Vds = 3000 V (highlighted), f = 100 kHz | Fig. 9 |
| Internal Gate Resistance | RG(int) | | 4 | | Ω | f = 100 kHz, Vac = 25 mV | |
| Gate to Source Charge | Qgs | | 122 | | nC | Vds = 6000 V (highlighted), Vgs = -5 V/+15 V, Ids = 15 A, RG,ON = RG,OFF = 25 Ω | Fig. 12 |
| Gate to Drain Charge | Qgd | | 48 | | nC | same | Fig. 12 |
| Total Gate Charge | Qg | | 268 | | nC | same | Fig. 12 |

Body Diode Characteristics (Tvj = 25 °C unless otherwise specified):

| Characteristics | Symbol | Min. | Typ. | Max. | Unit | Test Conditions | Note |
|---|---|---|---|---|---|---|---|
| Diode Forward Voltage | Vsd | | 5.3 | | V | Vgs = -5 V, Isd = 7.5 A | Fig. 7 |
| Diode Forward Voltage | Vsd | | 4.5 | | V | Vgs = -5 V, Isd = 7.5 A, Tvj = 175 °C | Fig. 8 |
| Reverse Recovery Time | trr | | 186 | | ns | Vgs = -5 V, Isd = 15 A, VR = 6000 V; dIf/dt = 680 A/µs, Tvj = 175 °C | |
| Reverse Recovery Charge | Qrr | | 2.91 | | µC | same | |
| Peak Reverse Recovery Current | Irrm | | 22.5 | | A | same | |

Page text: "3000-6000V. Ok understandable. Still crazy."

Source line: Wolfspeed datasheet, CPM3-10000-0300A (PRELIMINARY watermark).

## p.41 — Wolfspeed CPM3-10000-0300A charts: normalized Rds_on vs temperature; capacitance vs Vds

- Chart 1: Normalized Drain-Source On-Resistance Rds,on (p.u.) vs Junction Temperature (°C). X: 0–200 °C; Y: 0.0–4.0. Conditions: Ids = 15 A, Vgs = 15 V, tp < 200 µs. Curve: 1.0 at 25 °C, ~1.5 at ~75 °C, ~2.0 at ~100 °C, ~2.5 at ~125 °C, rising to ~3.7 at 175 °C.
- Chart 2: Capacitance (pF, log scale 1–10000) vs Drain-Source Voltage Vds (V), 0–3000 V. Series: Ciss ~8000–9000 pF, flat; Coss falls from ~1000s of pF at low Vds to ~100 pF then ~75–80 pF at 3000 V; Crss falls to ~3–4 pF at high Vds.

Page text: "Rds_on degrades… very severely against temperature. Even at a conservative 100C, you get 2x so 610 mOhm. Custom package and cooling needed to use this part. It's gona kick out a comical amount of head in such a small footprint."

Source line: Wolfspeed datasheet charts.

## p.44 — Infineon GaN gate drive whitepaper: Introduction (text excerpt)

Text page (Infineon whitepaper "1 Introduction" excerpt) — no chart/table. Key transcribed points:

- Infineon's GaN portfolio comprises enhancement-mode (normally-off) concepts using a p-doped gate: "gate injection transistor" (GIT) with ohmic gate contact or "Schottky gate transistor" (SGT). GITs used exclusively in high-voltage applications (up to 700 V); SGTs cover a broader 100 to 700 V range.
- All GaN switches characterized by low terminal capacitances → gate charge almost an order of magnitude lower than silicon counterparts.
- Highlighted: "However, there is a parameter typical for enhancement-mode (e-GaN) switches that significantly influences gate drive concepts. It is the low threshold voltage of the p-GaN gate, typically only slightly above +1 V. This has severe consequences:" — a relatively small gate current for switch-off at zero gate voltage; an increased sensitivity with respect to cross-conduction in half-bridge applications.
- Mitigation: negative gate drive voltage, with drawback of increased voltage-drop in reverse (third quadrant) operation and higher conduction losses during dead-time.

Page text (author): "GaN transistors have very low threshold voltage. Too low. It creates control issues."

Source line: Infineon whitepaper (gate drive concepts for GIT and SGT product families).

## p.45 — Infineon whitepaper 2.1.2 RC interface for SGT: Figures 3 and 4

- Text (highlighted): for a Schottky gate GaN switch, the optimum gate voltage range in the "on"-state is relatively small (typically 5 V to 6 V); due to the low threshold, a negative gate drive can be beneficial to allow fast switching "off" and to avoid cross-conduction, particularly in hard-switched applications at higher voltage and power levels.
- Figure 3: "Equivalent circuit of CoolGaN™ SGT and gate drive with RC interface and clamping diodes" — ideal driver (Vdd, logic/level shift/isolation, S1/S2), RC interface with clamp (Ron, Roff, Rss, Cc, Zener diodes ZD1, ZD2), Schottky gate transistor (Cgd(Vgd), Cgs, Cds(Vds), 0.2 Rds(on), Ls). ZD1 typically a 5.3 V Zener diode, resulting in gate drive voltage of ~6 V; if VDD sufficiently high (e.g. VDD = 9 V), a negative gate drive voltage -VN is generated in the "off"-state.
- Figure 4: "Typical gate current and gate voltage waveforms for SGT" — (a) gate current Ig vs t: Ion pulse at turn-on, transient current Ion/Ioff up to 1 A, Ioff pulse at turn-off; (b) gate voltage Vgs vs t: Vdd, Vzd, 6 V plateau in "on", drops to -VN in "off".

Page text (author): "Negative gate drive voltage is required to proper operation. This makes the control circuits much more complicated. Really everyone, this is so fucking annoying lol."

Source line: Infineon whitepaper, Figures 3 and 4.
