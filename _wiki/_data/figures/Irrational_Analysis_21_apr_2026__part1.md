# Irrational Analysis_21 apr 2026.pdf — figure transcriptions (part 1)

Pages covered: 3, 4, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17.
Machine transcription of figure pages so chart/table data is text-searchable. Transcribed faithfully; no interpretation added.

## p.3 — Earnings-call transcript screenshot (Navitas Q&A on 800 V data center)

Screenshot of an earnings-call transcript app (dark theme), with author highlights. No printed source line on the exhibit; content is a Navitas earnings call Q&A.

- Operator (0:38:13): "Next question comes from the line of Jon Tanwanteng with CJS Securities. Your line is open."
- Jonathan Tanwanteng, Managing Director (0:38:20): "Hi, good afternoon. Thanks for taking my questions, and I'll join the queue in wishing Todd well wishes on his journey. If you could start, maybe talk a little bit about the competitive landscape in supplying the 800 V data center. What, what are you seeing just in terms of who you're bidding against in these sockets, if they're, you know, outpricing you or doing better in technology? On top of that, you know, how is your partnership with Infineon evolving in that space as well? Thank you."
- Chris Allexandre, President and CEO (0:38:50): "Thank you for your question, Jon. I'll start with the end. We continue our partnership with Infineon. We have a cross license, as you know, and we share the same vision, which is to enable the accelerated adoption of GaN and silicon carbide in the AI DC, right? SiC as the traditional architecture and GaN in the 800 V DC, right? There's a lot of dialogue between the two companies on that front, right? Number two, you know, you will have seen that there are multiple vendors having been listed on the 800 V AI factory kind of ecosystem. As a matter of fact, I think it's up to 13 vendors today, but we don't see all of them in each of the sockets we target." [the "13" is highlighted in red/pink in the exhibit]
- Chris Allexandre, President and CEO (0:39:35): "I would, you know, I would recommend that you look at how many of those 13 are actually in the high voltage GaN. How many of them have a 650 V GaN in the right package to be able to enable 800 V HVDC? How many of them have mid-voltage GaN to enable the 50 V secondary side? Some of them are listed on as a silicon vendor, okay? We are listed as a GaN vendor. The other thing is, as we talked about SiC being used on the AC-DC as well, there is a natural pull on more SiC as we get to higher voltage and also outside of data center. To do the 800 V HVDC, you need to enable a change of the grid architecture."
- Chris Allexandre, President and CEO (0:40:17): [cut off at bottom of page — begins] "This is now a high voltage, ultra-high voltage SiC play. What [illegible]..."

## p.4 — Google search / AI Overview screenshot: "navitas infineon license"

Screenshot of a Google search results AI Overview. No printed source line beyond the Google UI (cites "Navitas Semiconductor +4", "Navitas Q3 2024 results", Compound Semiconductor article).

Text: Navitas Semiconductor and Infineon Technologies entered a strategic partnership, including a cross-license agreement for GaN (Gallium Nitride) patents, to accelerate technology adoption in AI data centers, electric vehicles, and motor drives. This collaboration enables a dual-sourcing model, providing customers with reliable, compatible low-voltage GaN technology, ensuring consistent packaging and footprints.

Key Aspects of the Navitas–Infineon Agreement:
- Cross-Licensing: Reciprocal access to GaN patent portfolios allows both companies to innovate without litigation risk.
- Dual-Sourcing Strategy: Focuses on creating a "second source" capability for customers, enhancing supply chain security for high-volume applications.
- Technology Focus: Centers on low-voltage (80–120V) GaN, particularly for 48V systems, as reported in Navitas Q3 2024 results.
- Common Standards: The partnership ensures common specs for packaging and footprints, facilitating ease of adoption for designers.

Author caption below exhibit: "As the Navitas CEO mentioned, they have a cross-licensing and second-source agreement with Infineon."

## p.7 — Bar chart: preferred funding rounds vs. May '24 dilutive G42 option (Cerebras context implied by report; entity not named on the page)

Bar chart, y-axis in $B ($0 to $4B gridlines at $1B intervals); x-axis = funding rounds by date. Red annotation: "May '24 — Dilutive G42 Option backstabs Series D+E+F investors at $14.66/share" (red arrow pointing to a red bar between Jul '17 and Nov '18 positions).

| Round | Amount | Price/share |
|---|---|---|
| Jan '17 (Series B Preferred) | $240M | $2.75/share |
| Jul '17 (Series C Preferred) | $860M | $8.95/share |
| Nov '18 (Series D Preferred) | $1.7B | $16.15/share |
| Nov '19 (Series E Preferred) | $2.42B | $18.32/share |
| May '24 dilutive G42 option | [amount not shown, small red bar ~$0.7B height] | $14.66/share |

Backstab icons overlay the Series D and Series E bars. No printed source line.

## p.8 — (no data content — screenshot of a LaTeX/PDF editor showing a "Contents" page of a prior Cerebras report, plus text: "Irrational Analysis is heavily invested in the semiconductor industry", note that a V2 of the report is in progress, and start of a Contents list: "1. Switching Regulator Basics")

## p.10 — Infographic: "Switching regulator operating modes" (ABLIC)

Diagram of a buck switching regulator: VIN → MOS FET 1 (high side) / MOS FET 2 (low side) → L: Inductor → C: Capacitor → Load → VOUT. Right panel: voltage-vs-time square wave between 0V and VIN, showing "Pulse width" and "1 cycle" with MOS FET 1 ON / MOS FET 2 ON alternation.

- "The frequency is fixed, but the pulse width changes to control the output voltage" → PWM control
- "The pulse width is fixed, but the frequency changes to control the output voltage" → PFM control

Watermark: www.ablic.com (source: ABLIC). Author caption: "Switching regulators convert DC DC using two transistors (high side and low side) followed by a simple (typically external) LC low-pass filter."

## p.11 — Infographic: "Schematic drawing and operation of a switching regulator" (ABLIC)

Schematic: VIN → SW1 / SW2 → L: Inductor → C: Capacitor → Load → VOUT. Three voltage-vs-time inset plots: (1) constant VIN; (2) "Converted to pulse" — square wave alternating SW1 ON / SW2 ON between 0V and VIN; (3) constant VOUT after "Smoothing using LC filter".

Watermark: www.ablic.com (source: ABLIC). Author caption: "You can spot the components of a power delivery system pretty easily."

## p.12 — (no data content — product photo of an AI accelerator board with 4 large GPU/ASIC packages and 2 smaller chips; author caption: "Let me zoom in and highlight part of the power delivery system.")

## p.13 — Annotated board photo: power delivery components highlighted

Zoomed board photo with color overlays. Legend printed below:
- Red = filtering inductors
- Blue = switching regulators (square chips) + filtering capacitors (small rectangles)

Three red rows (inductor banks) alternate with blue rows below/around the chip package. No printed source line.

## p.14 — Datasheet excerpt: "TYPICAL APPLICATION" — MPS MP86935-A Intelli-Phase

Application schematic of MP86935-A Intelli-Phase: inputs 3.3V → VDRV/VDD/AGND; PWM, SYNC, CS, VTEMP/FLT signal pins; power pins VIN, BST, SW, PGND; SW output through inductor + capacitor (circled in purple) to VOUT and PGND.

Author caption: "Purple crayon surrounds the output low-pass filter." Source: MPS (Monolithic Power Systems) MP86935-A datasheet.

## p.15 — Datasheet page: "MP86935-A — 60A, INTELLI-PHASE SOLUTION in TLGA-35 (3mmx6mm) PACKAGE" — TYPICAL PERFORMANCE CHARACTERISTICS

Five oscilloscope plots (source: MPS MP86935-A datasheet):
- Switching Waveform: VIN = 6V, L = 50nH (highlighted), IOUT = 30A; CH3: VSW 2V/div; 100ns/div.
- Dead Time at SW Rising: IOUT = 30A; CH3: VSW 0.3V/div; 2.5ns/div.
- CS Output Waveform: IOUT = 0A; CH1: VIOUT 300mV/div, CH3: VSW 5V/div; 500ns/div.
- CS Output Waveform: IOUT = 30A; CH1: VIOUT 300mV/div, CH3: VSW 5V/div; 500ns/div.
- High-Side Current Limit: CH1: VFAULT 5V/div; CH2: IL 20A/div; CH2: VSW 10V/div; CH1: PWM 5V/div; 2µs/div.

## p.16 — Datasheet excerpt: "FUNCTIONAL BLOCK DIAGRAM" (Figure 1) — MPS MP86935-A

Block diagram: pins VDD, VDRV, BST, VIN, PWM, SYNC, AGND, VTEMP/FLT, CS, SW, PGND. Blocks: UVLO (RDY→VIN), Control Logic (with 6kΩ and 5kΩ resistors on PWM/SYNC inputs), HS Current Limit, ZCD (inductor current crossed zero), Negative Current Limit, Level Shift, Temperature Sense and Fault Indicator, Current Sense. HS-FET and LS-FET (both circled in purple by the author) drive SW.

Author captions: "The external LC filter smooths out the square wave (V_sw, switching regulator output voltage)." / "Don't get hung up on the complicated block diagram. Switching regulators are in reality two beefy, fast transistors switched in a precise manner." Source: MPS MP86935-A datasheet.

## p.17 — Datasheet chart: "TYPICAL CHARACTERISTICS — Efficiency" — MPS MP86935-A

Line chart. Conditions (highlighted): VIN = 6V, L = 50nH, fSW = 1MHz. X-axis: OUTPUT CURRENT (A), 0–60. Y-axis: EFFICIENCY (%), 80–96.

- MP86935-A 0.8V (yellow): rises from ~80% near 0A, peaks ~92.8% around 12–15A, declines to ~83.5% at 60A.
- MP86935-A 1.2V (blue): rises from ~82% near 0A, peaks ~94.2% around 15A, declines to ~86.5% at 60A.

Author caption: "And the most important plot is the efficiency at a particular input+output voltage." Source: MPS MP86935-A datasheet.
