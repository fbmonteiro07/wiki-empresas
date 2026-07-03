# Irrational Analysis_8 may 2026.pdf — figure transcriptions (part 2)

Pages covered: 23, 24, 27, 28, 30, 31, 32, 33, 35, 37, 39, 41.
Note: machine transcription of figure/chart pages so the data is text-searchable. Transcribed faithfully; no interpretation added.

## p.23 — Joker meme (GloFo monolithic node)

(no data content — Joker movie still meme; page text: "You see, the GloFo monolithic node is different from what they are now promoting in investor relations slides. ENHANCE")

## p.24 — GlobalFoundries SCALE CPO platform slide

Screenshot of GF investor/marketing slide plus quoted text:
- "GF's SCALE CPO solution and silicon photonics technology offer an advanced portfolio of fully-qualified photonic devices, such as 50Gbps and 100Gbps micro-ring modulators, coupled ring resonators and integrated photodiodes. Additional features include through silicon vias (TSVs) for high-speed signaling and power delivery and copper pad pitches ranging from 110µm down to sub-45µm for 2.5D/3D stacking from organic substrates to silicon interposers, enabling customers to move quickly from design to volume production. The platform integrates electrical ICs on…"
- Slide diagram labeled "SCALE — Enabled by GF's Ecosystem": Fiber Attach Unit (FAU), Fiber Array, Electronic IC (EIC), Photonic IC (PIC). Zoomed image repeats labels "Electronic IC (EIC)" / "Photonic IC (PIC)" (two discrete dice).
- Author commentary: unclear if the "new" SCALE platform is hybrid bonded; slide shows two discrete dice so not the fusion node; GloFo apparently abandoned monolithic after Ayar Labs and Lightmatter fled to TSMC COUPE; monolithic fusion node was promoted as recently as ~2.5 months ago at OFC 2026.
- Source: GlobalFoundries slide/material as reproduced in Irrational Analysis, 8 May 2026 (no printed source line).

## p.27 — onsemi earnings call Q&A excerpt (data center power content)

Transcript screenshot (onsemi earnings call):
- Neil Young, Analyst, Needham & Co (for Quinn Bolton): question on full AI data center power tree (UPS, rack-level power, point of load) and biggest incremental content opportunities as architectures move to higher voltage distribution.
- Hassane El-Khoury, President & CEO, onsemi: covers from the rack or 800 volt or HVDC to the outlet; large opportunity in Solid-State Transformers (SST), forward-looking and incremental. Key figures: "today, at the rack today, you can think about a 120 kilowatt rack at $9,500. At the 800 volt or high voltage rack, we're thinking about $115,000 content. Although our content is almost 10x inside the rack, there is additional incremental content from the rack all the way to the infrastructure… 'cause this is all high voltage, which is exactly right in our sweet spot."
- Second excerpt (El-Khoury): fully focused on it, dedicated team; "Now, the V-GaN is more on the high voltage. I mentioned last time we are sampling V-GaN, and we're on track to continue to do that with revenue, starting 2027" (announced in Q4).
- Author commentary: interested in data-center power, not automotive.
- Source: onsemi earnings call transcript screenshot, as reproduced in Irrational Analysis, 8 May 2026.

## p.28 — [6.b] Navitas — earnings call Q&A excerpt (GaN vs SiC in AI power)

Transcript screenshot (Navitas earnings call):
- Madison DePaola (Rosenblatt Securities, for Kevin Cassidy): question on GaN and SiC in AI power, design win activity vs larger competitors.
- Chris Allexandre (Navitas CEO): 4 high-power markets — AI data center mostly GaN and SiC; grid infrastructure mostly SiC; high-performance computing more GaN; industrial both SiC and GaN. Current architecture: 50-volt bus bar, grid 480/400-volt AC converts to 50-volt DC, mostly SiC. First step (announced at GTC): 800 volt, 3-phase higher power AC/DC converting 400/480-volt AC to 800-volt DC, starting end of this year/early next year — mostly SiC. NVIDIA GTC DC-DC top-of-rack converter at 15 kilowatt uses either GaN or SiC. Second phase of 800-volt DC architecture: high-density rack, "megawatt rack will be Kyber for NVIDIA" or other high-density racks for "the Googles of this world"; DC-DC conversion moves inside the rack — "you have no choice than to use GaN. Because the level of density, the level of power requirements make it impossible to use silicon, but also silicon carbide doesn't have the switching frequency." Fourth step: grid side, replacing AC-DC PSU on the side rack by SST.
- Author commentary: "great summary by the Navitas CEO," useful for choosing circuits to simulate.
- Source: Navitas earnings call transcript screenshot, as reproduced in Irrational Analysis, 8 May 2026.

## p.30 — [6.c] Wolfspeed — FY26 Q3 financial highlights + fiscal 4Q26 outlook

Wolfspeed FY26 Q3 Financial Highlights slide ("Financial discipline while investing in technology leadership"):

| Category | Metric | Value |
|---|---|---|
| Income Statement & Cash Flow | Revenue | $150M |
| Income Statement & Cash Flow | Adj. EBITDA¹ | $(62)M |
| Income Statement & Cash Flow | Op. Cash Flow | $(84)M |
| Balance Sheet | Cash | $1.2B |
| Balance Sheet | Net CapEx | $5M (Net of $33M NY ESD Subsidy) |
| Balance Sheet | Net Debt | $555M |

Fiscal 4Q26 Financial Outlook table:

| Item | Guidance |
|---|---|
| Revenue | $140 million – $160 million |
| Non-GAAP Gross Margin¹ | Expected to remain negative (highlighted) |
| Operating Expenses | Approximately flat quarter-over-quarter |

Source: Wolfspeed company presentation slides (© 2026 Wolfspeed, Inc.; footnote 1: non-GAAP financial measure), as reproduced in Irrational Analysis, 8 May 2026.

## p.31 — Wolfspeed GAAP→non-GAAP gross margin reconciliation + CEO remarks

WOLFSPEED, INC. — Reconciliation of GAAP to Non-GAAP Measures (in millions of USD, unaudited):

| Line | Successor: 3 months ended Mar 29, 2026 | Predecessor: 3 months ended Mar 30, 2025 |
|---|---|---|
| GAAP gross loss | ($40.0) | ($22.5) |
| GAAP gross margin percentage | (27)% (highlighted) | (12)% |
| Adj: Stock-based compensation expense | 2.8 | 9.7 |
| Adj: Restructuring and facility closure costs | 6.2 | 16.8 |
| Non-GAAP gross (loss) profit | ($31.0) | $4.0 |
| Non-GAAP gross margin percentage | (21)% | 2% |

Robert Feurle, CEO (transcript excerpt, 0:02:52): disciplined R&D on high-return programs; "This quarter, we introduced the first commercially available 10-kilovolt silicon carbide power MOSFET and launched our next-generation TOLT portfolio" (highlighted); 10 kilovolt to cement leadership in high-voltage applications; all device production shifted to 200 millimeter at Mohawk Valley; Durham facilities anchor materials capabilities, including commercial-scale 300 millimeter development; refinanced a portion of first lien senior secured notes.

Author commentary: TOLT is a standard packaging format for power semis; right package needed for AI/datacenter market; footprint is critical.

Source: Wolfspeed press release / earnings materials, as reproduced in Irrational Analysis, 8 May 2026.

## p.32 — Infineon TOLG package diagram; [7] Optics / [7.a] AAOI intro

Product photo/diagram of an Infineon TOLG package: labels Top, Bottom, Drain, Gate, Source (leadframe package shown top and bottom views).
Author text: no SPICE model for the 10KV SiC part, so building own model in LTSPICE. Section [7] Optics: "Everything down. Seems like market jitters and some pod monkies rotating. Not much news on engineering side." [7.a] AAOI: "Cursed chart lol."
Source: Infineon package image, as reproduced in Irrational Analysis, 8 May 2026.

## p.33 — AAOI (Applied Optoelectronics) 5-day stock chart screenshot

Trading-app screenshot (NASDAQ: AAOI):
- Last price 150.44, down -7.12 (-4.52%)
- H/L: 177.88 – 143.58; Vol 17.94M; Mkt Cap 12.04B
- Last 1W: -33.17 (-18.08%)
- BOLL(20,2.00): Median 150.38, Upper 152.41, Lower 148.34
- 5D chart range shown: high 197.19 (+7.45%), low 132.75 (-27.66%); dates 05/03–05/08
Source: trading app screenshot (unattributed platform), as reproduced in Irrational Analysis, 8 May 2026.

## p.35 — AAOI earnings call excerpts (ELSFP/CPO laser capacity; DC revenue mix)

Transcript excerpt 1 (AAOI management): plans to increase manufacturing capacity for external light source (ELSFP) for co-packaged optics (CPO), using the ultra-narrow linewidth high-power laser announced late last year; very limited production now, ramping later this year and into 2027, "culminating in about 400 thousand pieces per month by 2027"; will make the high-power lasers in-house for the ELSFP; in-house laser manufacturing for many years, avoided shortages; expanding footprint in Texas; "We expect to further expand our laser fabrication capacity by around 350% by 2027." (highlighted)

Author commentary/questions: what is the linewidth (intrinsic or effective, at 50C)? What is your RIN? Does AAOI have decent laser capacity or expanding at the same time as everyone else?

Transcript excerpt 2 (AAOI Q1): data center revenue mix — 41% from 100G products, 46.7% from 200G and 400G products, 5.6% from 800G transceiver products (highlighted), 5.6% from 10G and 40G transceivers. CATV revenue $66.8 million, +4% YoY and +24% sequentially, high end of expectations of $61–$67 million; shipped a significant quantity of 1.8 gigahertz amplifiers to largest CATV customer in Q1; 2026 demand seen somewhat higher than initial projections.

Source: AAOI earnings call transcript screenshots, as reproduced in Irrational Analysis, 8 May 2026.

## p.37 — AAOI call Q&A on indium phosphide capacity

Transcript excerpt 1: Stefan Murry — shortage of indium phosphide laser manufacturing capacity across the industry right now, expected to persist and "even get more acute with the advent of ELSFP"; hence need to "expand our indium phosphide fabrication capability pretty dramatically over the next 12 to 18 months." (highlighted)
Analyst follow-up on securing substrate capacity for indium phosphide. Thompson Lin: four to five suppliers, four outside of China; enough inventory minimum for almost one year; making calls with all suppliers as volume increases fast.

Transcript excerpt 2 (Thompson Lin): equipment delivery-to-revenue takes more than three months or longer including manufacturing cycle time; sometimes customers need another on-site audit and qualification (highlighted); readiness more like Q3; Q2 maybe ~30% growth (capacity-limited), Q3 and Q4 talking about 60%, 70%, or even 80% growth in each quarter, even into Q1 next year.

Author commentary: "I agree." / "Qualifying new lines takes time this is true."
Source: AAOI earnings call transcript screenshots, as reproduced in Irrational Analysis, 8 May 2026.

## p.39 — Lumentum "Class-leading CPO Laser Performance" slide (via author's tweet)

Tweet by Irrational Analysis (@insane_analyst, Apr 29): "Only $LITE has publicly shown (many times) their high power laser noise performance. Not a single competitor has dared to publicly show their noise. Go ask $COHR, $AAOI, Furukawa, or any of the 'Chinese competition' what their RIN and linewidth are. They will not answer you." (7 replies, 16 reposts, 268 likes, 23K views)

Embedded Lumentum slide "Class-leading CPO Laser Performance" — four charts:
1. Light vs. Current: Facet Power (mW) vs Current (A, 0–2); annotation 400mW dashed line; 50°C; multiple device series [series labels illegible].
2. Power Conversion Efficiency: PCE (%) vs Facet Power (mW, ~100–600); annotation "20% PCE" dashed line; 50°C.
3. Linewidth Spectrum vs. Optical Power: Power (dBm) vs Frequency (Hz); series 100mW/200mW/300mW/400mW [approx.]; 50°C; exact values [illegible].
4. RIN Spectrum vs. Optical Power: RIN (dB/Hz, ~-143 to -152 axis) vs Frequency (GHz, 0–40); series 150mW/300mW/400mW [approx.]; 50°C; exact values [illegible].

Author commentary: "The giant fab in Greensboro, North Carolina is a fucking death star."
Source: Lumentum slide (© 2026 Lumentum Operations LLC), via @insane_analyst tweet, as reproduced in Irrational Analysis, 8 May 2026.

## p.41 — Lumentum AI-art image + earnings call Q&A on ELS

Top: AI-generated promotional-style image of a man on a sci-fi ship bridge with Lumentum logos and a globe of laser links (no data content).

Transcript excerpt (Lumentum earnings call): Papa Sylla (analyst) asks about CPO opportunity — mostly ultra-high power lasers into 2H 2027 — and vertical integration / providing more ELS-type product, and whether engagement comes from the same customers buying ultra-high power lasers. Michael E. Hurlston (CEO): "on ELS, we definitely have a very significant opportunity" (highlighted); getting closer to converting that into numbers; "the non-primary customer engagements are largely driven by ELS" (highlighted); engineering teams less familiar with optics; currency to engage those customers initially will be the ELS; no significant wins yet but "just around the corner"; expanding CPO horizon requires the vertical integration strategy.

Author commentary: ELSFP is a massive opportunity for Lumentum, simpler than transceiver in some ways. Standard SiPho transceiver component groups: 1. CW lasers + lenses + isolators; 2. SiPho chip with modulators. (list continues past page)

Source: Lumentum earnings call transcript screenshot, as reproduced in Irrational Analysis, 8 May 2026.
