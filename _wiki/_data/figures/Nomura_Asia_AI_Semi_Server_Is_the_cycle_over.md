# Nomura Asia AI Semi & Server — "Is the cycle over?" (30 June 2026)

Figure-page transcription — pages 22, 25, 31, 49, 63, 70, 77, 84.
Machine transcription of chart/figure pages for text-searchability. Values read from chart images; marks [illegible] where unreadable. Attribution: Nomura, Asia AI Semi & Server, 30 Jun 2026.

## p.22 — Fig. 32: Meta's contribution to TSMC's AI revenue

Bar/line chart, USDmn (LHS), % contribution to AI revenue (RHS 0–2%). Years 2023–2027F.
- Series (bars): MTIA 100, MTIA 200, MTIA 300, MTIA 400/450. Line: Meta contribution to AI revenue (RHS).
- 2023: small MTIA 100 bar (~50); 2024: small MTIA 200 (~70); 2025: small MTIA 300 (~50); 2026F: MTIA 400/450 ~230; 2027F: MTIA 400/450 ~980. Contribution line: ~0.5% flat through 2025, rising to ~1.5% by 2027F. (approximate reads)
Source: Company data, Nomura estimates

## p.22 — Fig. 33: HBM base die contribution to TSMC's AI revenue

Bar/line chart, USDmn (LHS 0–2,000), % contribution (RHS 0–10%). Years 2023–2027F.
- HBM base die bars: ~0 in 2023–2025, ~330 in 2026F, ~1,700 in 2027F. Contribution line rises to ~2% by 2027F. (approximate reads)
Source: Company data, Nomura estimates

## p.22 — Fig. 34: Our take on the nVidia AI platform roadmap

Large table; platforms Ampere / Hopper / Blackwell / Rubin / Feynman.

| Row | Ampere | Hopper / Hopper+ | Blackwell / Blackwell Ultra | Rubin / Rubin Ultra | Feynman |
|---|---|---|---|---|---|
| Codename | Ampere (2020) | Hopper (2022), Hopper+ (2023) | Blackwell (2024), Blackwell Ultra (2025) | Rubin (2026F), Rubin Ultra (2027F) | Feynman (2028F) |
| Logic fabrication | TSMC N7 | TSMC N4 | TSMC N4P | TSMC N3P / TSMC N3P | TSMC A16? |
| Transistors (bn) | 54 | 80 | 208 | 336 / ? | ? |
| Assembly | CoWoS-S | CoWoS-S | CoWoS-L | CoWoS-L / CoWoS-L | SoIC + CoWoS/CoPoS? |
| Interposer size (1x reticle=830mm²) | 2x reticle | 2x reticle | 3.3x reticle | 5.0x / 5.0x reticle | c.6x reticle |
| FP8 Tensor core perf (dense) | 0.08 PFLOPS | 1.6 PFLOPS (PCIe), 2.0 PFLOPS (SXM) | 3.5 PFLOPS (B100), 4.5 PFLOPS (B200) / 7.5 PFLOPS (B300) | 25 PFLOPS (inference), 17.5 PFLOPS (training) / 50 PFLOPS | 12x HBM4E? |
| HBM specs | 6s HBM2/2E 8Hi | 6s HBM3 8Hi / 6s HBM3E 8Hi | 8s HBM3E 8Hi / 8s HBM3E 12Hi | 8s HBM4 12Hi / 16s HBM4E 16Hi | 12x HBM4E? (HBM stacking, customized HBM) |
| Max HBM capacity | 80GB | 96GB / 144GB | 192GB / 288GB | 288GB / 1TB | |
| DRAM layer technology | 1Y/1Z nm | 1Z nm / 1a/1b nm | 1a/1b nm | 1b/1c nm | |
| HBM I/Os | 1,024 | 1,024 | 1,024 | 2,048 | |
| Substrate dimension (mm²) | 55x55 | 58x55 | 81x73 | 97x83 / 97x83? | >100x100? |
| Chip max TDP | 400W | 700W | 700W (B100), 1,200W (B200) / 700W (single die), 1,400W (dual die) | 1,800W / 2,300W? | ? |
| ARM-based CPU | – | Grace (TSMC N5) | Grace (TSMC N5) | Vera (TSMC N3P) | Rosa |
| Superchip max TDP | – | 1,000W (GH200) | 2,700W (GB200) / 3,300W (GB300)? | ? / ? | ? |
| LPU | – | – | – | LP30 (SF4X) 128GB SRAM / LP35 | LP40 |
| DPU | – | BlueField-3 | BlueField-3 | BlueField-4 | BlueField-5 |
| NIC (max bandwidth) | CX6 (200Gbps) | CX7 (400Gbps) | CX7 (400Gbps) / CX8 (800Gbps) | CX9 (1.6Tbps) / CX9 (1.6Tbps) | CX10 |
| Optical module | 400Gbps | 800Gbps | 800Gbps | 1.6Tbps / 3.2Tbps | |
| Form factor | 4 DGX servers/rack | 4 DGX servers/rack | 4 B200 DGX servers/rack GB200 NVL36/72 / 4 B300 NVL16 servers/rack, Oberon: GB300 NVL72 | Oberon: NVL72 (copper scale-up), NVL576 (optical scale-up) / Oberon: NVL72, NVL576; Kyber: NVL144 | Kyber: NVL144 (copper scale-up), NVL1152 (CPO scale-up) |
| FP8 Tensor core perf (rack, dense) | 2.5 PFLOPS | 64 PFLOPS | 360 PFLOPS (GB200 NVL72) / 550 PFLOPS (inference), 360 PFLOPS (training) (GB300 NVL72) | 1,800 PFLOPS (inference), 1,250 PFLOPS (training) (Vera Rubin NVL72) / 7,500 PFLOPS (inference), 5,000 PFLOPS (training) (Rubin Ultra NVL576) | |
| GPU-GPU NVLink (max bandwidth) | NVLink 3 Switch (600GB/s) | NVLink 4 Switch (900GB/s) | NVLink 5 Switch (1.8TB/s) | NVLink 6 Switch (3.6TB/s) / NVLink 7 Switch (3.6TB/s) | NVLink 8 CPO |
| Cable connector | 56Gbps | 112Gbps | 224Gbps | 448Gbps (likely 224G SerDes with enhanced modulation) / 448Gbps? | 448G SerDes would require new materials |
| Rack-Rack Infiniband (max bw/port) | 200Gbps | 400Gbps | 800Gbps | 1.6Tbps | CPO |
| Rack-Rack Ethernet (max bw/port) | Spectrum 3 (200Gbps) | Spectrum 4 (400Gbps) | Spectrum 5 (800Gbps) | Spectrum 6 CPO (1.6Tbps) | Spectrum 7 CPO (3.2Tbps) |
| Power requirement (without redundancy) | 26kW | 40.8kW | 57.2kW (B200); 66kW (GB200 NVL36), 132kW (GB200 NVL72) | 132-145kW (GB300 NVL72) [as printed] / ? | New power supply architecture (e.g. HVDC) |
| Mainstream thermal solutions | Air cooling | Air cooling | Half liquid cooling (or air cooling for some HGX/DGX servers) | Full liquid cooling | |

Notes column (technological challenge): yield challenge and TSMC execution; high-precision LSI pick & place, SoIC (GPU-on-GPU), thermal solution (SiC), CoPoS development?; large-die bonding without warpage and CTE mismatch, evaluate CoWoS/FOPLP to lower cost (likely delayed to 2H29); HBM stacking / customized HBM; evaluation of new material to build >100x100mm substrates; heat spreader design (microchannel lid?); heat dissipation a key issue for 1.6Tbps NIC — SiPh and CPO may kick in from CX9; M9Q processing (mechanical/laser drilling), backplane PCB production?
Source: Company data, Nomura estimates

## p.25 — Fig. 38 & 39: Vera CPU packaging photos

(no data content — two die-shot photos: "Fig. 38: Vera CPU packaged on TSMC CoWoS-R" and "Fig. 39: Vera CPU packaged at Amkor S-SWIFT"; NVIDIA markings, date codes 2550 and 2545. Source: Company data, Nomura research)

## p.31 — Fig. 48: Floorplan of AMD MI455 and cross section

Diagram: 4x XCD (N2) compute dies flanked by 8x HBM4 stacks and dummy dies; 2x MID (N3) top/bottom. Cross-section: carrier silicon; XCD (N2) over AID (N3), hybrid bond; MID (N3); reconstituted interposer (5.5x reticle); microbump; LSI.
Source: Company data, Nomura research

## p.31 — Fig. 49: Possible Feynman floorplan

Diagram: two "Feynman (A16?)" compute dies, surrounded by 12x HBM4E stacks (6 top, 6 bottom) and I/O dies on left/right sides.
Source: Company data, Nomura estimates

## p.31 — Fig. 50: TSMC's latest SoIC roadmap

TSMC slide "TSMC-SoIC Boosts AI Compute": SoIC with 3D interconnect offers 56X interconnect density and 5X power-efficiency over CoWoS with 2.5D interconnect; 6µm pitch entered volume production in 2025; continue scaling to A14-on-A14 with 4.5µm pitch for production in 2029. Roadmap chart (interconnect IO count vs 2023–2029): Pitch 9µm TD: N7 BD: ≥N7 (TBV); Pitch 6µm TD: N5 BD: ≥N5 (TBV); Pitch 6µm TD: N3P BD: ≥N3P (TBV); Pitch 6µm TD: N3P BD: ≥N2P (TBV); Pitch 4.5µm TD: A14 BD: ≥A14 (TBV) — Logic-on-Logic.
Source: TSMC, Nomura research

## p.31 — Fig. 51: TSMC's SoIC capacity

Bar chart, SoIC capacity by year end, kwpm: 2025: 5; 2026F: 10; 2027F: 20+; 2028F: 40+.
Source: Company data, Nomura estimates

## p.49 — Fig. 78: G3 policy rate expectations

Three line charts (%, OIS forward rates by maturity 0–5 years), snapshots dated 26/2/2, 26/2/27, 26/3/31, 26/5/19, 26/6/25.
- Japan (y-axis 0.4–3.0%): curves start ~0.7–1.0% at 0Y rising to ~1.9% (26/2/27) up to ~2.75% (26/5/19) at 5Y; latest 26/6/25 ~2.6% at 5Y.
- US (y-axis 2.8–4.4%): all start ~3.6% at 0Y; 26/2/27 dips to ~2.9% at 1-2Y then to ~3.45% at 5Y; 26/5/19 rises to ~4.15% at 5Y; 26/6/25 ~3.7% at 2-3Y, ~3.8% at 5Y.
- Europe (y-axis 1.8–3.2%): start ~1.9–2.2% at 0Y; 5Y range ~2.65% (26/2/27) to ~3.05% (26/5/19).
Note: OIS forward rates for each maturity.
Source: Bloomberg Finance L.P, Nomura

## p.63 — Fig. 93: TSMC's share price vs Bloomberg consensus EPS revisions

Line chart Jun-21 to Jun-26. LHS: Price (TWD) 0–2,700; RHS: EPS 20–180. Series: Price (TWD; LHS); 2024E, 2025E, 2026E, 2027E, 2028E EPS.
- Price ~600 TWD Jun-21, dips ~400 mid-2022, rises through 2024–25 to ~2,500-2,600 by Jun-26. 2024E EPS ~40 settling ~45; 2025E ~40→~65; 2026E rises to ~100; 2027E to ~125-130; 2028E to ~165 by Jun-26. (approximate reads)
Source: Company data, Bloomberg Finance L.P. consensus estimates, Nomura research

## p.70 — Fig. 103: ASEH's share price vs Bloomberg consensus EPS revisions

Line chart Jun-21 to Jun-26. LHS: EPS 5–35; RHS: share price (TWD) 0–800. Series: 2024E–2028E EPS; Share price (TWD, RHS).
- Share price ~100 TWD through 2021-24, ~100-150 into 2025, spikes to ~650-700 by Jun-26. 2024E EPS ~14-16 falling to ~8; 2025E ~13-15 range then ~9-10; 2026E ~15-16; 2027E rises to ~25-31; 2028E ~30-31 by Jun-26. (approximate reads)
Source: Company data, Bloomberg Finance L.P., Nomura research

## p.77 — Fig. 110 & 111: ASPEED unveils AST1840

Fig. 110 ("AST1840 could simplify design without FPGA") — diagram "Evolving Server Architecture (Single Node)": (1) BMC —LTPI→ Server HPM board with FPGA → CPU; (2) AST2700 —LTPI→ AST1700 → CPLD → CPU; or (3) AST2700 —LTPI→ AST1840 (eFPGA) → CPU. Source: Company data, Nomura research.
Fig. 111 — photo of ASPEED demo board: "AST1840 eFPGA – Root of Trust Protected" (boots from internal flash, Caliptra authenticates AST1840 eFPGA image before configuration, secure booth with Caliptra (Root of Trust)) and "AST1840 eFPGA – OCP Streaming Port" (eFPGA image stored in flash on DC-SCM, Caliptra (BMC) authenticates image then streams to AST1840 for eFPGA configuration; Caliptra + Streaming Boot architecture). Source: Company data, Nomura research.

## p.84 — Fig. 120: Gen AI website traffic share

Stacked bar chart (Similarweb, All Traffic | Worldwide), monthly May 2025–Apr 2026, 0–100%. Series: ChatGPT, Gemini, DeepSeek, Grok, Claude, Perplexity, Copilot, Other. ChatGPT share declines from ~75% (May 2025) to ~52% (Apr 2026); Gemini (pink band) expands correspondingly; other services small slivers. (approximate reads)
As of Apr 2026. Source: Similarweb

## p.84 — Fig. 121: Gen AI website traffic share

Line chart, x-axis: 12 / 6 / 3 / 1 months ago. LHS 0–30% (Gemini, DeepSeek, Grok, Claude, Perplexity, Copilot); RHS 0–90% (ChatGPT). ChatGPT (RHS) declines from ~78% to ~55%; Gemini rises from ~8% to ~27%; Claude rises from ~2% to ~7%; DeepSeek declines ~6%→~2%; Grok/Perplexity/Copilot ~1-3% flat. Caption: "Gemini and Claude continued to grow". (approximate reads)
Source: Similarweb, Nomura research
