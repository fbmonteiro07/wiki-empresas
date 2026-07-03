# UBS Data Centre Central — 800VDC looming faster. Introducing. (22 June 2026)

Machine transcription of figure pages 3, 4, 5, 8, 9, 10 from "UBS Data Centre Central 800VDC looming faster. Introducing.pdf". Transcribed from page images for text-searchability; values marked [illegible] where not readable. Very dense comps sheets (Figs 4–6) are transcribed for the most legible columns (Company, Rating, Analyst, Price, 12m TP, P/E 2026E); remaining columns (EV/EBIT, EV/EBITDA, EV/Sales, EBIT margin, EPS growth, Sales growth for 2026E–2028E) exist on the page but individual cells are small — spot values noted where clearly legible.

## p.3 — Figure 1: Data Centre architecture available today

Infographic: two versions of today's AC data-centre power architecture, each with a component chain and a VOLTAGE column.

**Version 1 — Rack density: up to c100kW**
| Component | Voltage |
|---|---|
| Grid | 33kVAC → 11kVAC |
| MV switchgear | 11kVAC |
| Transformer | 400/230VAC |
| AC main distribution | 400VAC |
| LV UPS | 400VAC |
| AC busbar with tap off boxes | 400VAC |
| Rack PDU to rack line up | 400VAC in → 230VAC outlets; 230VAC in → 12V DC |

**Version 2 — Rack density: up to c100kW**
| Component | Voltage |
|---|---|
| Grid | 33kVAC → 11kVAC |
| MV switchgear | 11kVAC |
| Transformer | 400/230VAC |
| AC main distribution | 400VAC |
| LV UPS | 400VAC |
| AC busways | 400VAC |
| PDU | 400VAC in → 230VAC out |
| Remote power panel | 230VAC |
| Rack PDU to rack line up | 230VAC in → 12V DC |

Source: Company reports, UBS estimates.

## p.4 — Figure 2: Three phases of 800V DC architecture (section: DATA CENTRE 800V ARCHITECTURE)

Infographic: three phases of 800V DC data-centre power architecture.

**Phase 1 (ORV3) — Rack density: 150kW**
| Component | Voltage |
|---|---|
| Grid | 33kVAC → 11kVAC |
| MV switchgear | 11kVAC |
| Transformer | 400/230V AC |
| AC main distribution | 400VAC |
| LV UPS | 400VAC |
| AC busbar with tap off boxes | 400VAC |
| PDU | 400VAC |
| AC → DC power shelf unit | 400V AC → 800V DC |
| Rack PDU to rack line up | 800V DC; 800V DC → 48/12V DC |

**Phase 2 (SIDECAR) — Rack density: up to 400kW**
| Component | Voltage |
|---|---|
| Grid | 33kV AC → 11kV AC |
| MV switchgear | 11kV AC |
| Transformer | 400/230V AC |
| AC main distribution | 400V AC |
| LV UPS | 400V AC |
| Sidecar* | 400V AC → 800V DC |
| Rack line up | 800V DC → 48/12V DC |

**Phase 3 (FULL SOLID STATE) — Rack density: 1MW**
| Component | Voltage |
|---|---|
| Grid | 33kVAC → 11kVAC |
| MV switchgear | 11kVAC |
| MV UPS | 11kVAC |
| Solid state transformer | 11kV AC → 800VDC |
| DC main distribution | 800VDC |
| Short term storage | — |
| Rack line up | 800VDC → 48/12VDC |

Source: Company reports, UBS estimates. *Icon represents 800V DC sidecar power distribution unit.

## p.5 — Figure 3: UBS Global Data Centres Coverage Map (section: UBS GLOBAL DATA CENTRES VALUE CHAIN COVERAGE MAP)

Analyst coverage grid by value-chain layer × region (US / EMEA / APAC). No financial data.

| Layer | US (analyst — tickers) | EMEA | APAC |
|---|---|---|---|
| Hyperscalers | Karl Keirstead (US Software) — MSFT, ORCL, PLTR; Stephen Ju (US Internet) — GOOG, AMZN, META | — | Kenneth Fong (China Internet) — Alibaba, Tencent |
| Compute, Memory, Storage & Chip Production | Timothy Arcuri (US Semiconductors) — NVDA, AMD, AVGO, INTC, MU, ARM, MRVL | Francois-Xavier Bouvignies (EMEA Tech Hardware) — ASML, IFXGn; Sebastian Vogel (EMEA Switzerland) — COTNE; Joern Iffert (EMEA Switzerland) — VAT | Nicolas Gaudois (APAC Tech) — SK Hynix, Samsung Electronics; Sunny Lin, Jerry Su, Diana Chang (Taiwan Tech) — TSMC, ASE, KYEC, ASpeed, Mediatek, GUC, Alchip, Chroma, Unimicron |
| Switching / Optical | David Vogt (US IT Hardware) — CLS, ANET, CSCO, HPE, LITE, CIEN; Timothy Arcuri — NVDA; Joshua Spector (US Autos) — GLW | Francois-Xavier Bouvignies — NOKIA; Andre Kukhnin (EMEA Cap Goods) — HLMA | — |
| Servers / Hardware assembly | David Vogt (US IT Hardware) — DELL, HPE, JBL, SNX, CLS | — | Randy Abrams (Taiwan Equity) — Hon Hai, Quanta, Wiwynn, Wistron, Inventec, Lenovo, Asus, Delta; Diana Chang (Taiwan Equity) — Giga-byte, King Slide |
| Electrical / Thermal | Amit Mehrotra (US EEMI) — ETN, VRT, JCI, TT, CARR; Neal Burk — HUBB, MOD, NVT; Joshua Spector (US Autos) — ECL | Andre Kukhnin, Jingyi Zheng (EMEA Cap Goods) — SCHN, LEGD, SIE, ABB, MTRS; Sven Weier (EMEA Cap Goods) — ALFA; Sebastian Vogel (EMEA Switzerland) — BEAN, CNTL | Sara Wang (China Telecoms & Software) — Envicool; Phyllis Wang (China Industrials) — Inovance; Jiayi Du (China Industrials) — Hanbell |
| Connectivity / Cables | Joseph Spak (US Autos) — TEL, APH | Christopher Leonard (EMEA Cap Goods) — PRY, NEXS; Tommaso Operto (EMEA Switzerland) — HUBN | Jasmine Huang (China Telecoms & Software) — YOFC |
| Power / Engines | Joseph Spak (US Autos) — BWA; Steven Fisher (US Machinery, E&C) — CAT, CMI; Gavin Parsons (US Aerospace & Defence) — HWM, WWD | Christopher Leonard (EMEA Cap Goods) — ENR1, CWR; Sven Weier (EMEA Cap Goods) — WRT1V, ANDR; Ian Douglas-Pennant (EMEA Aerospace & Defence) — RR | Kunlun Li (China Industrials) — Megmeet, Hongfa, Faratronic; Amily Guo (China oil, gas, chemical) — Jereh, OFS; Wei Shen, Xinyu Fang (China Autos) — Weichai, Yuchai, TGood |
| Construction | Joshua Chan (US Business Services) — FIX; Steven Fisher (US Machinery, E&C) — PWR; Avinatan Jaroslawicz (US Machinery, E&C) — EMCOR | Tommaso Operto (EMEA Switzerland) — IMPN | Sara Wang (China Telecoms & Software) — CCS |
| Colo/Operators Real Estate | John Hodulik, Ryan Gravett (US Data Centers/Compute Infrastructure) — EQIX, DLR | Charles Boissier (European Real Estate) — MRL | Sara Wang (China Telecoms & Software) — GDS, VNET |

Source: UBS research

## p.8 — Figure 4: US Comps Sheet (section: COMP SHEET DATA CENTRE COVERAGE)

Comps table. Columns on page: Company, Rating, Analyst, Price, 12m TP (local), CCY, Mkt Cap (local), EV (local), Mkt Cap (€m), EV (€m), ADV (€m), then 2026E/2027E/2028E for: P/E (UBSe), EV/EBIT (UBSe), EV/EBITDA (UBSe), EV/Sales (UBSe), EBIT Margin (UBSe), EPS Growth (UBSe), Sales Growth (UBSe). Key legible columns:

| Company | Rating | Analyst | Price | 12m TP | P/E 2026E |
|---|---|---|---|---|---|
| **Hyperscalers** | | | | | |
| Microsoft Corp. | Buy | Keirstead | 379.4 | 510.0 | 20.8 |
| Oracle Corporation | Buy | Keirstead | 184.3 | 285.0 | 23.1 |
| Palantir Technologies Inc | Buy (CBE) | Keirstead | 128.5 | 200.0 | — |
| Alphabet Inc. | Neutral | Ju | 367.5 | 410.0 | 25.6 |
| Amazon.com | Buy | Ju | 244.4 | 333.0 | 21.6 |
| Meta Platforms | Buy | Ju | 577.2 | 865.0 | 17.4 |
| **Compute, Memory, Storage & Chip Production** | | | | | |
| NVIDIA Corp | Buy | Arcuri | 210.7 | 280.0 | 22.5 |
| Advanced Micro Devices Inc | Buy (CBE) | Arcuri | 537.4 | 455.0 | — (2027E 39.1) |
| Broadcom Inc. | Buy | Arcuri | 411.4 | 485.0 | 30.3 |
| Intel Corp. | Neutral | Arcuri | 134.0 | 83.0 | — |
| Micron Technology Inc | Buy | Arcuri | 1,134.0 | 1,625.0 | 12.0 |
| Arm Holdings PLC | Buy (UR) | Arcuri | 439.5 | 260.0 | — |
| Marvell Technology Group | Buy | Arcuri | 310.6 | 230.0 | — |
| **Switching / Optical** | | | | | |
| Celestica Inc | Neutral (CBE) | Vogt | 372.6 | 400.0 | 36.3 |
| Arista Networks Inc | Buy (CBE) | Vogt | 169.7 | 187.0 | — (2027E 38.5) |
| Cisco Systems Inc. | Buy | Vogt | 119.5 | 132.0 | — (2027E 26.4) |
| Hewlett Packard Enterprise | Neutral | Vogt | 47.4 | 65.0 | 12.5 |
| Lumentum Holdings Inc | Neutral (CBE) | Vogt | 850.0 | 960.0 | — |
| Ciena Corporation | Neutral (CBE) | Vogt | 428.2 | 320.0 | — (2027E 38.5) |
| NVIDIA Corp | Buy | Arcuri | 210.7 | 280.0 | 22.5 |
| Corning Inc | Buy | Spector | 194.9 | 228.0 | — (2027E 25.2) |
| **Servers / Hardware assembly** | | | | | |
| Dell Technologies | Neutral (CBE) | Vogt | 409.5 | 440.0 | 23.4 |
| Hewlett Packard Enterprise | Neutral | Vogt | 47.4 | 65.0 | 12.5 |
| Jabil Inc | Neutral | Vogt | 371.9 | 430.0 | 26.6 |
| TD Synnex Corp | Buy | Vogt | 284.6 | 310.0 | 16.8 |
| Celestica Inc | Neutral (CBE) | Vogt | 372.6 | 400.0 | 36.3 |
| **Electrical / Thermal** | | | | | |
| Eaton Corporation PLC | Neutral | Mehrotra | 421.8 | 360.0 | 31.7 |
| Vertiv Holdings Co | Buy | Mehrotra | 333.1 | 370.0 | — (2027E 31.4) |
| Johnson Controls International plc | Buy | Mehrotra | 144.8 | 180.0 | 24.9 |
| Trane Technologies PLC | Buy | Mehrotra | 483.4 | 570.0 | 32.2 |
| Carrier Global Corp | Buy | Mehrotra | 71.8 | 78.0 | 25.1 |
| Hubbell Inc | Neutral | Burk | 523.7 | 515.0 | 26.5 |
| Modine Manufacturing Co | Buy | Burk | 297.4 | 355.0 | 39.0 |
| nVent Electric PLC | Buy | Burk | 177.0 | 200.0 | 38.4 |
| Ecolab | Buy | Spector | 269.1 | 325.0 | 32.4 |
| **Connectivity / Cables** | | | | | |
| TE Connectivity PLC | Buy | Spak | 217.6 | 261.0 | 18.7 |
| Amphenol Corp | Buy | Spak | 164.0 | 178.0 | 32.9 |
| **Power/Engines** | | | | | |
| BorgWarner, Inc. | Buy | Spak | 71.8 | 95.0 | 13.5 |
| Caterpillar Inc. | Neutral | Fisher | 985.8 | 900.0 | 39.6 |
| Cummins Inc. | Buy | Fisher | 716.9 | 830.0 | 23.9 |
| Howmet Aerospace Inc | Neutral | Parsons | 277.7 | 290.0 | — |
| Woodward Inc | Buy | Parsons | 430.1 | 429.0 | — (2027E 34.8) |
| **Construction** | | | | | |
| Comfort Systems USA Inc | Buy | Chan | 1,967.4 | 2,125.0 | — (2027E 36.5) |
| Quanta Services | Buy | Fisher | 702.3 | 900.0 | — (2027E 33.6) |
| EMCOR Group Inc | Buy | Jaroslawicz | 836.6 | 975.0 | 27.8 |
| **Colo/Operators Real Estate** | | | | | |
| Equinix Inc | Buy | Hodulik | 1,092.2 | 1,210.0 | — |
| Digital Realty Trust | Buy | Hodulik | 188.2 | 227.0 | — |

Source: UBS Research

## p.9 — Figure 5: EMEA Comps Sheet

Same column structure as Figure 4. Key legible columns:

| Company | Rating | Analyst | Price | 12m TP | P/E 2026E |
|---|---|---|---|---|---|
| **Compute, Memory, Storage & Chip Production** | | | | | |
| ASML | Buy | Bouvignies | 1,591.2 (EUR) | 1,900.0 | — (2027E 32.8) |
| Infineon Technologies AG | Neutral | Bouvignies | 79.3 (EUR) | 61.0 | 39.2 |
| Comet | Buy | Vogel | 389.4 (CHF) | 452.0 | 35.7 |
| VAT Group AG | Buy | Iffert | 665.4 (CHF) | 745.0 | — |
| **Switching / Optical** | | | | | |
| Nokia | Neutral | Bouvignies | 12.0 (EUR) | 11.0 | 31.0 |
| Halma Plc | Buy | Kukhnin | 4,020.0 (GBX) | 4,775.0 | 32.3 |
| **Electrical / Thermal** | | | | | |
| Schneider Electric | Buy | Kukhnin | 277.0 (EUR) | 310.0 | 27.1 |
| Legrand | Neutral | Kukhnin | 138.7 (EUR) | 160.0 | 24.8 |
| Siemens | Buy | Kukhnin | 273.1 (EUR) | 310.0 | 22.3 |
| ABB Ltd | Neutral | Kukhnin | 84.0 (CHF) | 69.0 | 16.9 |
| Munters Group AB | Buy | Zheng | 195.9 (SEK) | 245.0 | 29.7 |
| Alfa Laval | Neutral | Weier | 543.8 (SEK) | 570.0 | 23.5 |
| Belimo | Sell | Vogel | 952.5 (CHF) | 500.0 | — |
| Comfel [likely Centiel/Comfel — small print] | Neutral | Vogel | 7.8 (CHF) | 6.3 | — (2027E 35.4) |
| **Connectivity / Cables** | | | | | |
| Prysmian SpA | Buy | Leonard | 146.4 (EUR) | 175.0 | 28.2 |
| Nexans SA | Buy | Leonard | 149.4 (EUR) | 155.0 | 16.5 |
| Huber+Suhner | Buy | Operto | 245.0 (CHF) | 320.0 | — (2027E 30.9) |
| **Power/Engines** | | | | | |
| Siemens Energy AG | Buy (CBE) | Leonard | 156.1 (EUR) | 175.0 | 36.2 |
| Wartsila | Neutral | Weier | 33.5 (EUR) | 40.0 | 29.1 |
| Andritz | Buy | Weier | 78.8 (EUR) | 92.0 | 14.8 |
| Rolls-Royce | Buy | Douglas-Pennant | 1,393.0 (GBX) | 1,400.0 | 35.3 |
| **Construction** | | | | | |
| Implenia AG | Buy | Operto | 72.9 (CHF) | 100.0 | 14.8 |
| **Colo/Operators Real Estate** | | | | | |
| Merlin Properties | Buy | Boissier | 15.3 (EUR) | 16.9 | 27.5 |

Source: UBS Research

## p.10 — Figure 6: APAC Comps sheet

Same column structure as Figure 4. Key legible columns:

| Company | Rating | Analyst | Price | 12m TP | P/E 2026E |
|---|---|---|---|---|---|
| **Hyperscalers** | | | | | |
| Alibaba Group | Buy | Fong | 111.0 (USD) | 184.0 | 20.6 |
| Tencent Holdings | Buy | Fong | 445.4 (HKD) | 780.0 | 12.5 |
| **Compute, Memory, Storage & Chip Production** | | | | | |
| SK Hynix | Buy | Gaudois | 2,521,000.0 (KRW) | 3,000,000.0 | 7.2 |
| Samsung Electronics | Buy | Gaudois | 346,500.0 (KRW) | 550,000.0 | 6.9 |
| Taiwan Semiconductor Manufacturing | Buy | Lin | 2,385.0 (TWD) | 3,000.0 | 24.1 |
| ASE Industrial | Buy | Lin | 595.0 (TWD) | 660.0 | 34.1 |
| King Yuan Electronics | Buy | Lin | 280.5 (TWD) | 380.0 | — |
| MediaTek Inc. | Buy | Lin | 4,460.0 (TWD) | 5,500.0 | — (2027E 27.3) |
| ASPEED Technology Inc | Buy | Lin | 18,155.0 (TWD) | 22,000.0 | — |
| Alchip Technologies | Buy | Su | 4,320.0 (TWD) | 6,000.0 | 28.0 |
| Chroma ATE | Buy | Su | 2,230.0 (TWD) | 2,960.0 | — (2027E 35.8) |
| Global Unichip | Buy | Su | 5,075.0 (TWD) | 6,260.0 | — (2027E 34.6) |
| Unimicron Technology | Buy | Chang | 988.0 (TWD) | 1,200.0 | — (2027E 35.9) |
| **Servers / Hardware assembly** | | | | | |
| Hon Hai Precision | Buy | Abrams | 272.0 (TWD) | 310.0 | 15.7 |
| Quanta | Buy | Abrams | 374.0 (TWD) | 420.0 | 15.6 |
| Wiwynn | Buy | Abrams | 3,090.0 (TWD) | 6,400.0 | 10.5 |
| Wistron | Buy | Abrams | 162.5 (TWD) | 215.0 | 10.5 |
| Inventec | Neutral | Abrams | 67.5 (TWD) | 50.0 | 20.4 |
| Lenovo Group | Neutral | Abrams | 24.9 (HKD) | 18.0 | 19.3 |
| Asustek Computer Inc. | Neutral | Abrams | 803.0 (TWD) | 700.0 | 14.8 |
| Delta Electronics | Buy | Abrams | 2,155.0 (TWD) | 2,600.0 | — (2027E 33.7) |
| King Slide Works | Buy | Chang | 6,620.0 (TWD) | 5,350.0 | — (2027E 36.9) |
| Giga-Byte Technology | Neutral | Chang | 347.5 (TWD) | 340.0 | — |
| **Electrical/ Thermal** | | | | | |
| Shenzhen Envicool Technology Co., Ltd | Buy | Wang | 74.6 (CNY) | 123.0 | — (2027E 21.3) |
| Shenzhen Inovance Technology | Buy | Wang | 69.8 (CNY) | 86.0 | 32.6 |
| Shanghai Hanbell Precise Machinery | Buy | Du | 31.2 (CNY) | 31.1 | 28.0 |
| **Connectivity/ Cables** | | | | | |
| Yangtze Optical Fibre and Cable | Buy | Huang | 227.2 (HKD) | 290.0 | 39.7 |
| **Power/Engines** | | | | | |
| Shenzhen Megmeet Electrical | Neutral | Li | 178.9 (CNY) | 124.8 | — |
| Hongfa Technology | Buy | Li | 33.9 (CNY) | 44.0 | 23.7 |
| Xiamen Faratronic | Neutral | Li | 170.1 (CNY) | 118.0 | 23.7 |
| Jereh Oilfield Services | Buy | Guo | 157.7 (CNY) | 200.0 | — (2027E 28.7) |
| Weichai Power | Neutral | Shen | 38.5 (CNY) | 32.1 | 21.0 |
| China Yuchai International | Buy | Shen | 50.5 (USD) | 80.0 | 15.3 |
| Qingdao TGood Electric | Buy | Fang | 38.8 (CNY) | 55.0 | 25.5 |
| **Construction** | | | | | |
| China Communications Services | Neutral | Wang | 4.1 (HKD) | 4.6 | 6.8 |
| **Colo/Operators Real Estate** | | | | | |
| GDS | Buy | Wang | 33.3 (USD) | 60.0 | 25.1 |
| VNET | Buy | Wang | 9.0 (USD) | 15.5 | — |

Source: UBS Research
