# Bristlemoon Global Fund Quarterly (June 2026) — ASML EUV/DUV bottoms-up model — figure transcriptions

Covers exhibits: p.15 (EUV specs + N2 node capex) and p.16 (DRAM EUV demand + ASML system shipments + immersion DUV). Machine transcription of the two data-table exhibits so the numbers are text-searchable. **Attribution: Bristlemoon Capital — Bristlemoon Global Fund Quarterly Report, June 2026 (buy-side; ASML a top-5 long).** These are the two reusable bottoms-up models the desk flagged as templates — see memory [[euv-fab-capex-model]] and [[dram-euv-tool-demand-model]]. All arithmetic verified internally consistent.

## p.15 — MODEL A: EUV specs → N2 node → capex per 10kwpm

The chain: derate the tool's nameplate throughput for real-world dose + uptime → wafers/tool/month → EUV tools per fab → EUV capex → gross up through litho / WFE / shell → **capex per 10kwpm**.

**EUV specs (NXE:3800E)**

| Item | Value | Note |
|---|--:|---|
| EUV model | NXE:3800E | |
| Nameplate throughput | 220 wph | |
| Reference dose | 30 mJ/cm² | |
| Layers/day | 5,280 | = 220 × 24 |
| Layers/month | 158,400 | = 5,280 × 30 |

**N2 node**

| Item | Value | Note |
|---|--:|---|
| EUV layer count | 22 | unchanged vs N3 |
| Uptime | 45% | implied by ASML field data @ reference dose |
| Dose | 40 mJ/cm² | real-world (vs 30 reference) |
| Throughput @ dose | 165 wph | = 220 × 30/40 |
| Wafers/day | 81 wpd | = 165 × 24 × 45% ÷ 22 layers |
| % overall equip. efficiency | **34%** | vs spec @ 30 mJ/cm² (≈ real throughput ~1/3 of nameplate) |
| Wafers/month | 2,430 wpm | = 81 × 30 |
| Fab size | 25,000 wpm | fab size limits; **no longer ~40kwpm as in the past** (TSMC module) |
| **EUV tools required** | **11** | = 25,000 ÷ 2,430 (round up; could be higher w/ redundancy / non-TSMC efficiency) |
| Tool price | 240 US$M | north of €200m |
| Total EUV capex | 2,640 US$M | = 11 × 240 |
| % EUV share of litho | 80% | Bristlemoon assumption |
| Total litho capex | 3,300 US$M | = 2,640 ÷ 0.80 |
| % litho share of WFE | 40% | Bristlemoon assumption |
| Total WFE capex | 8,250 US$M | = 3,300 ÷ 0.40 |
| % WFE share of fab total | 70% | 20-30% fab shell |
| Total fab capex | 11,786 US$M | = 8,250 ÷ 0.70 |
| **N2 capex per 10kwpm** | **4.7 US$B** | = 11,786 × (10 ÷ 25) |

Source: Bristlemoon Capital.

## p.16 — MODEL B: DRAM EUV demand → ASML system shipments (vs Bloomberg consensus)

Two engines feed ASML units: (1) DRAM/HBM EUV tool demand (below), (2) foundry EUV demand (TSMC/Intel/Samsung/Rapidus). ArFi immersion is then backed out from an EUV/ArFi ratio.

**DRAM EUV demand**

| Metric | Unit | 2024 | 2025 | 2026 | 2027 | 2028 |
|---|---|--:|--:|--:|--:|--:|
| HBM generation | | 3 | 3E | 4 | 4E | 5 |
| HBM industry demand | GB m | 1,348 | 2,594 | 4,500 | 7,247 | 9,783 |
| % yoy | | | 92% | 73% | 61% | 35% |
| DRAM node for HBM | | 1z | 1a | 1b | 1c | 1d |
| DRAM density | Gb/mm² | 0.22 | 0.31 | 0.43 | 0.56 | 0.70 |
| % yoy | | | 41% | 39% | 30% | 25% |
| Capacity per die | Gb | 16 | 24 | 24 | 32 | 40 |
| Implied die size | mm² | 73 | 77 | 56 | 57 | 57 |
| Dies per wafer | | 820 | 780 | 1,080 | 1,080 | 1,080 |
| GB per wafer | GB | 1,640 | 2,340 | 3,240 | 4,320 | 5,400 |
| HBM:DRAM trade ratio | | 3.0 | 3.0 | 4.0 | 4.0 | 4.5 |
| HBM wafers required | kwpm | 206 | 277 | 463 | 559 | 679 |
| EUV layers/wafer | | | 3 | 4 | 5 | 6 |
| Total EUV layers | 000s | | 831 | 1,852 | 2,796 | 4,076 |
| Nameplate layers/tool/month | | | 158,400 | 158,400 | 158,400 | 158,400 |
| % OEE | | | 45% | 45% | 45% | 45% |
| Actual layers/tool/month | | | 71,280 | 71,280 | 71,280 | 71,280 |
| **EUV tools required for HBM** | | | 12 | 26 | 39 | 57 |
| Industry DRAM capacity | mwpm | | 1,600 | 1,680 | 1,932 | 2,222 |
| % yoy | | | | 5% | 15% | 15% |
| % HBM share of wafers | | | 17% | 28% | 29% | 31% |
| **EUV tools required for DDR** | | | 56 | 68 | 96 | 130 |
| **Total tools required for DRAM** | | | 67 | 94 | 136 | 187 |
| Existing tools (UBSe) | | | 60 | 75 | | |
| **Incremental tools** | | | | 19 | 41 | 51 |

Notes: HBM demand = median of Bernstein, MS, UBS, Arete. DRAM density ~blended MU + SK Hynix. GB per wafer = commodity DRAM, not HBM. HBM:DRAM trade ratio captures TSV, density and yield loss. EUV layers/wafer = est. blend of the 3 majors. % OEE higher for memory than logic. Industry DRAM capacity is ex-CXMT. DDR = commodity DRAM. Incremental DRAM tools (19/41/51) flow into ASML shipments below as the "DRAM" line.

**ASML system shipments**

| EUV shipments | 2026 | 2027 | 2028 | Note |
|---|--:|--:|--:|---|
| TSMC | 36 | 45 | 45 | assume ~100kwpm N3/N2/A16 adds p.a. |
| Intel | 5 | 9 | 11 | 3×40kwpm fabs by 2030 requires 50+ EUV tools |
| DRAM | 19 | 41 | 51 | = incremental DRAM tools above |
| Other (Sam. Foundry, Rapidus) | 5 | 5 | 5 | mainly Samsung; 10kwpm+ SF2+ adds p.a. |
| **Total EUV tools** | **65** | **100** | **112** | |
| Bloomberg ccs | 65 | 89 | 101 | Bristlemoon materially ahead in '27/'28 |

**Immersion DUV shipments**

| Item | 2026 | 2027 | 2028 | Note |
|---|--:|--:|--:|---|
| EUV/ArFi ratio | 50% | 55% | 55% | should rise as EUV takes over more critical layers |
| Implied ArFi tools | 131 | 182 | 205 | = EUV total ÷ ratio |
| Bloomberg ccs | 123 | 145 | 156 | Bristlemoon materially ahead in '27/'28 |

Source: Bristlemoon Capital, Bloomberg, industry reports.
