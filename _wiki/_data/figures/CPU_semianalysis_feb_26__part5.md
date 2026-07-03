# CPU semianalysis_feb 26.pdf — figure transcriptions (part 5)

Pages covered: 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 72.
Machine transcription of figure/chart pages for text-search purposes. Transcribed faithfully from page images; no interpretation added.

## p.59 — Kunpeng 920 Die Shots

(no data content — die-shot photograph of Huawei Kunpeng 920 chiplets. Caption: "Kunpeng 920 Die Shots. Source: 万扯淡". Surrounding body text notes: Kunpeng 920 (2019), 64 custom TaiShan V110 cores (ARM v8.2), two compute dies on TSMC 7nm, 8 clusters of 4 cores each, ring bus, 8 channels DDR4 total, first CPU with TSMC CoWoS-S, I/O die with 40 PCIe Gen4 lanes and dual 100 Gigabit Ethernet controllers; Kunpeng 930 failed to release in 2021 due to US sanctions.)

## p.60 — Kunpeng 920B Die Shots

(no data content — full-page die-shot photograph. Caption: "Kunpeng 920B Die Shots. Source: Kurnal".)

## p.61 — Huawei Kunpeng CPU Roadmap + TaiShan 950 SuperPoD

**Figure 1: Huawei Kunpeng CPU Roadmap. Source: Huawei** (presentation slide photo)

| Product | Timing | Specs (as printed) |
|---|---|---|
| Kunpeng 920 | 2024 Q1 | 64C; 80C/160T; 支持HCCS |
| Kunpeng 950 | 2026 Q4 | 96C/192T, 192C/384T; support for general-purpose computing SuperPoDs (支持通算超节点); dual-threaded LinxiCore (双线程灵犀核) |
| Kunpeng 960 | 2028 Q1 | High-performance model 高性能版本: 96C/192T, 50%+ improvement in individual core performance (for AI hosts, databases 面向AI host、数据库等场景，单核性能提升50%+); High-density model 高密版本: ≥ 256C/512T, optimized for virtualization, containers, big data, data warehouses (面向虚拟化、容器、大数据、数仓等场景) |

Slide tagline: "Kunpeng chips: Evolving nonstop, supporting SuperPoDs, more cores, and higher performance (鲲鹏芯片持续演进：支持超节点，更多核、更高性能)"

**Figure 2: Huawei TaiShan 950 SuperPoD. Source: Huawei** (presentation slide photo)

- TaiShan 950 SuperPoD — "World's first SuperPoD for general-purpose computing (全球首个通算超节点)", 2026 Q1
- Max nodes: 16 (32P) (最大16节点 (32P)); Max memory: 48 TB (最大内存 48 TB); Memory, SSD, and DPU pooling (支持内存/SSD/DPU池化)
- OLTP database (OLTP数据库): 2.9x speedup — 1.85mn tpmC (TaiShan 200 V2, GaussDB Centralized) → 5.4mn tpmC (TaiShan 950 SuperPoD, GaussDB Multi-Write)
- Virtualization (虚拟化): memory utilization improvement (内存利用率提升) 20% — 75% (TaiShan 200 V2) → 95% (TaiShan 950 SuperPoD)
- Spark workloads (Spark大数据): real-time data processing 30% faster — TPC-DS: 3,540s (TaiShan 200 V2) → 2,557s (TaiShan 950 SuperPoD)

Body text: Kunpeng 950 core count more than doubled to 192 (new LinxiCore, SMT); 96-core version also produced; 16 dual-socket servers per TaiShan 950 SuperPoD rack, up to 48TB DDR5 (12-channel memory design); adopted by Oracle Exadata database servers.

## p.62 — SemiAnalysis CPU Roadmap 2017-2028

**Figure: SemiAnalysis CPU Roadmap 2017-2028. Source: SemiAnalysis Estimates**

Gantt-style roadmap chart spanning 2017–2028 across 9 companies (AMD, Intel, Nvidia, Ampere, AWS, Google, Microsoft, ARM, Huawei; client roadmap also features Qualcomm). Individual product boxes and dates are [illegible] at this resolution. Body text notes: Ampere Computing's lineup will be changed to try to intersect with OpenAI following the acquisition; report details AMD Verano and Florence, Intel Coral Rapids and cancelled CPU lines, ARM Venom, Qualcomm SD2, NVIDIA Bluefield-4.

## p.63 — AMD Rackscale AI Infrastructure Roadmap

**Figure: AMD Rackscale AI Infrastructure Roadmap. Source: AMD** (slide: "Advancing AI Infrastructure on an Annual Cadence")

| Year | CPU | GPU | Networking | Rack |
|---|---|---|---|---|
| 2025 | AMD EPYC "Turin" | AMD Instinct MI350 Series | AMD Pensando Pollara 400 | (rack pictured) |
| 2026 | AMD EPYC "Venice" | AMD Instinct MI400 Series | AMD Pensando "Vulcano" | "Helios" |
| 2027 | AMD EPYC "Verano" | AMD Instinct MI500 Series | AMD Pensando "Vulcano" | Next Gen AI Rack |

Body text: Verano likely a Venice variant with Zen 6 cores, same 256-core count, new 3nm I/O die with PCIe Gen7 and 200G Ethernet SerDes, UALoE support; Zen 7 EPYC "Florence" expected 2028 on TSMC A16 (backside power), alternatively A14 for 2029; core count estimated around 320 (SemiAnalysis estimate).

## p.64 — AMD Zen CPU Core Roadmap

**Figure: AMD Zen CPU Core Roadmap. Source: AMD** (slide: "Leadership CPU Core Roadmap", timeline 2022 → 2026)

| Node | Cores | Features |
|---|---|---|
| 5nm · 4nm — Performance & Density | Zen 4, Zen 4c | AVX-512 AI ISA Support; Dual Core Design Points; Larger L2 Cache |
| 4nm · 3nm — New Foundation | Zen 5, Zen 5c | Wider/Deeper Compute; Full 512 Bit AI Vectors; Re-optimized Cache Hierarchy |
| Industry-First 2nm — Extension of Leadership | Zen 6, Zen 6c | New AI Data Type Support; More AI Pipelines |
| Future Node — Next-Generation | Zen 7 | New Matrix Engine; AI Data Format Expansion |

Footnote on slide: "All roadmaps subject to change."

## p.65 — Intel 18A-Ultra and 14A-P (Continuing Process Node Evolutions)

**Figure: Intel 18A-Ultra and 14A-P. Source: Intel** (Intel Foundry slide, timeline: Available Now / 2026 / 2027 / 2028)

- RibbonFET + Backside Power:
  - Intel 14A — "Industry 1st High-NA EUV, PowerDirect" → 14A, 14A-E, 14A-P
  - Intel 18A — "Industry 1st PowerVia" → 18A, 18A-P, 18A-U, 18A-PT
- FinFET:
  - Intel 3 — Intel 4, Intel 3, Intel 3-T, Intel 3-E, Future Customer Derivative
  - Mature Nodes — Intel 7, Intel 16, Intel 16-E, UMC 12, Future Customer Derivative
- Legend: P = Performance improvement, T = Through silicon vias for 3D stacking, E = Feature Extension, U = Ultra

Body text: Coral Rapids returns SMT to P-core; believed originally designed for Intel 14A (P1280), risk production 2027 → launch late 2028/early 2029; may be ported to refined 18A-Ultra to accelerate.

## p.66 — Qualcomm Datacenter CPU Announcement

**Figure: Qualcomm Datacenter CPU Announcement. Source: Qualcomm, ServeTheHome** (keynote photo: "Qualcomm expansion into data center — The next step in our diversification", showing CPU and AI chip renders)

Body text data: Centriq 2400 (2017): 48 Falkor ARMv8 cores, 6 channels DDR4. SD1 (never productized): 80 Oryon cores, TSMC N5, 16 channels DDR5-5600, 70 lanes PCIe Gen 5, 98x95mm LGA9470 socket, dual-socket support. SD2: re-entry from 2027, supplying Saudi Arabia's HUMAIN AI project; supports NVLink Fusion.

## p.67 — Bluefield-4 NVIDIA Context Memory Storage Platform

**Figure: Bluefield-4 NVIDIA Context Memory Storage Platform. Source: NVIDIA CES 2026** (slide)

- A New POD-Level Context Memory Platform
- BlueField-4 Data and Storage Processor
- Spectrum-X Ethernet RDMA Infrastructure
- 5X Higher Tokens per Second
- 5X Higher Power Efficiency
- Partner logos: AIC, Cloudian, DDN, Dell Technologies, HPE, Hitachi Vantara, IBM, Nutanix, Pure Storage, Supermicro, VAST, WEKA

Body text: Qualcomm Q4 2025 earnings call — SD2 ships for revenue in 2027; datacenter CPU market called a multi-billion dollar opportunity. Gerard Williams III and original Nuvia team members left Qualcomm January 2026.

## p.68 — Bluefield-4 Package Rendering

**Figure: Bluefield-4 Package Rendering. Source: NVIDIA, SemiAnalysis Estimates** (package render labeling GRACE CPU die and CX-9 die on one package)

Body text data: Bluefield-4 DPU co-packages a Grace CPU with a ConnectX-9 chip; used in each Rubin compute tray as frontend NIC; four BF4s in the Context Memory Storage Platform for KV-Cache offload to high-speed NAND; 64 enabled Grace cores, 128GB LPDDR5.

## p.72 — Report scope bullet list / Substack footer

(no data content — end-of-post page: bullet list describing paywalled report contents (floorplan analysis, NUMA comparison, advanced packaging schematics, CoWoS-L (AMD Venice) / CoWoS-R (NVIDIA Vera) / EMIB-Foveros Direct 3D (Intel Clearwater Forest) selection discussion, SPECint2017 estimates for AMD Venice and Intel Diamond Rapids), plus Substack "267 Likes · 23 Restacks" footer and comment box.)
