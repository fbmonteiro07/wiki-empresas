# CPU semianalysis_feb 26.pdf — figure transcription, part 2 (pages 18–29)

Machine transcription of figure/chart pages so the data is text-searchable. Source report: SemiAnalysis, "CPU" report, Feb 2026 ("CPU semianalysis_feb 26.pdf"). Do not treat as primary — verify against the PDF.

## p.18 — Haswell EP Die Configurations (Intel slide)

Diagram of three Haswell-EP die chops (HCC, MCC, LCC) with ring-bus layouts. Caption below slide: "Haswell HCC Dual Ring Bus. Source: Intel". Slide note: "Not representative of actual die-sizes, orientation and layouts – for informational use only."

| Chop | Columns | Home Agents | Cores | Power (W) | Transistors (B) | Die Area (mm2) |
|---|---|---|---|---|---|---|
| HCC | 4 | 2 | 14-18 | 110-145 | 5.69 | 662 |
| MCC | 3 | 2 | 6-12 | 65-160 | 3.84 | 492 |
| LCC | 2 | 1 | 4-8 | 55-140 | 2.60 | 354 |

Body text data points: Broadwell HCC (2015) up to 24 cores with dual 12-core ring buses; Cluster on Die testing — latency within each ring under 50ns, cross-ring access over 100ns.

## p.19 — KNL Mesh Interconnect (Intel's Mesh Architecture)

Slide: "KNL Mesh Interconnect" — grid diagram of Tiles, EDC, iMC, IIO, MCDRAM, DDR blocks. Bullets: Mesh of Rings — every row and column is a (half) ring; YX routing: Go in Y → Turn → Go in X; messages arbitrate at injection and on turn. Cache Coherent Interconnect — MESIF protocol (F = Forward); distributed directory to filter snoops. Three Cluster Modes — (1) All-to-All (2) Quadrant (3) Sub-NUMA Clustering.
Caption: "Intel Knights Landing Mesh Interconnect. Source: Intel, Hot Chips 2016".
Body text: Skylake-X (2017) brought 28 cores in the XCC die.

## p.20 — Skylake-SP 28-core die (mesh diagram)

Slide diagram of 6-column mesh: top row IO blocks (2x UPI x20, PCIe x16, PCIe x16 / DMI x4 / CBDMA, On Pkg PCIe x16, 1x UPI x20, PCIe x16); grid of CHA/SF/LLC + SKX Core tiles; 3x DDR4 channels on each side via MC. Legend: CHA – Caching and Home Agent; SF – Snoop Filter; LLC – Last Level Cache; SKX Core – Skylake Server Core; UPI – Intel UltraPath Interconnect.
Caption: "Skylake-SP Mesh Diagram. Source: Intel".
Body text: 28 cores in 6x6 mesh with north IO cap and 2 IMC spots; die would exceed 26 x 33 mm reticle limit with another row/column. Knights Landing mesh grid 6 columns x 9 rows, mesh ran at 1.6GHz.

## p.21 — Ice Lake XCC 40-core Mesh Diagram

Grid diagram: UPI, PCIe Gen4 1x16 blocks, Dummy blocks along top; HA/CA/SF/LLC + ICL Core tiles; memory Ch 1/Ch 2 on sides; DMI/CBDMA, UPI, FIVR, PCIe Gen4 1x16 along bottom.
Caption: "Ice Lake XCC 40-core Mesh Diagram. Source: Intel".
Body text data: Skylake-X mesh clock 2.4GHz vs core up to 4.5GHz; Cascade Lake-AP 56-core dual-die MCM; Ice Lake 14nm→10nm shrink, 40 cores in an 8x7 mesh.

## p.22 — Intel's Disaggregation Journey + Sapphire Rapids XCC Topology

Figure 1 (Intel slide): "Intel's Disaggregation Journey" — Intel Xeon 3rd Gen Ice Lake: Monolithic, 10nm; Intel Xeon 4th & 5th Gen (Sapphire & Emerald Rapids): tiles with I/O mem & compute, EMIB, Intel 7; Intel Xeon 6 (Granite Rapids & Sierra Forest): I/O tiles, compute tiles (E-core & P-core), EMIB, Intel 7 + Intel 3; Intel Xeon 6+ (Clearwater Forest): I/O tiles, base tiles, compute tiles, EMIB, Foveros Direct 3D, Intel 7 + Intel 3 + 18A.
Caption: "Intel Xeon's Disaggregation Journey to Chiplets. Source: Intel".

Figure 2: Sapphire Rapids XCC mesh topology across 4 tiles — 1x24 16GT UPI at each corner (x24 UPI blocks), 1x8 Gen3 DMI / 1x8 Gen4 PCIe on non-legacy socket, multiple 1x16 Gen5 PCIe/CXL 1.1 blocks, 2x DDR5 memory controllers per side (4 sides), CHA/SF/LLC + GLC Core tiles, Phys Split boundaries, accelerator blocks (QAT, DSA, DLB, IAA), some bottom PCIe "Not Connected".
Caption: "Sapphire Rapids XCC Topology. Source: Intel".

## p.23 — (mostly text; embedded article card)

No chart. Text-page data points: Sapphire Rapids monolithic would fit only 34 cores; four mirrored 15-core dies, 8x12 mesh, ~1600 mm2 silicon; core-to-core latency 59ns vs Skylake 47ns; L2 2MB/core, L2 120MB vs L3 112.5MB; stepping E5, released early 2023 (originally slated 2021); Emerald Rapids late 2023, 2 dies, 60→66 cores (up to 64 enabled), L3 ~tripled to 320MB. Embedded link card: "Intel Emerald Rapids Backtracks on Chiplets – Design, Performance & Cost", Dylan Patel, Gerald Wong, and 3 others, 3 May 2023.

## p.24 — Xeon 6 Platform Features + Xeon 6 Compute and I/O Die Diagrams

Figure 1 (Intel slide): "Intel Xeon 6 Processors | 6700 and 6900 Platform Series — shared underlying platform". Feature list: P-core and E-core SKU selections; increased core counts; increased memory bandwidth with DDR5; Multiplexed Combined Rank DIMM (MCR DIMM); increased inter-socket bandwidth with UPI 2.0; Compute Express Link (CXL) 2.0; increased I/O bandwidth on PCIe 5.0; increased shared LLC; Intel Accelerator Engines; HW-enhanced security; common OS and firmware. Shows Xeon 6700-series and Xeon 6900-series packages.
Caption: "Xeon 6 Platform Features. Source: Intel".

Figure 2: Compute die (Intel 3 process) — monolithic mesh, cores, cache, memory controllers and EMIB technology; DDR5/MRDIMM memory on both sides. I/O die (Intel 7 process) — universal I/O stacks with UPI, PCIe, CXL and Accelerator Engines (DSA, IAA, QAT, DLB blocks; UIO/Accel/IO blocks over I/O Fabric).
Caption: "Xeon 6 Compute and I/O Die Diagrams. Source: Intel".

## p.25 — Xeon 6 Compute Die Mosaic

Die photo mosaic of four compute dies. Caption: "Xeon 6 Compute Die Mosaic. Clockwise from Top Left: UCC 44c, HCC 50c, HDCC 152c, LCC 20c. Source: Intel, SemiAnalysis Estimates".
Body text data: Granite Rapids-AP Xeon 6900P — 10x19 mesh over 5 dies, 132 cores printed, up to 128 enabled; Sierra Forest 144-core, E-cores in 4-core clusters per mesh stop, 8x6 mesh, 152 cores printed / up to 144 active; dual-die 288-core Sierra Forest-AP (Xeon 6900E) did not reach general availability.

## p.26 — Twelve 24-core Clearwater Forest Compute Dies on 18A

Die photo (grid of 12 compute dies). Caption: "Twelve 24-core Clearwater Forest Compute Dies on 18A. Source: Intel, SemiAnalysis".
Body text data: Foveros Direct hybrid bonding, 18A core dies atop base dies (mesh, L3, memory interface), core counts up to 288; I/O dies reused from Xeon 6.

## p.27 — Clearwater Forest Performance Projections (Darkmont Projections)

Intel slide: "µArchitecture Power & Performance" vs Crestmont. Claims: up to 1.17x higher performance with Clearwater Forest (288c/450W) vs Sierra Forest (288c/500W); up to 1.3x higher performance per watt (same comparison). Footnote: based on 1-socket projections as of 9/19/25, results may vary; pre-production projections 288c/450W Intel Xeon 6+.

Bar chart (baseline Sierra Forest 288c/500W = 1.00); series: Sierra Forest 144c/330W, Sierra Forest 288c/500W, Clearwater Forest 288c/450W:

| Metric | SRF 144c/330W | SRF 288c/500W | CWF 288c/450W |
|---|---|---|---|
| TDP (lower is better) | 0.66 | 1.00 | 0.90 |
| Cores | 0.50 | 1.00 | 1.00 |
| Perf | 0.55 | 1.00 | 1.17 |
| Perf/W | 0.84 | 1.00 | 1.30 |

Caption: "Clearwater Forest Performance Projections. Source: Intel".
Body text: availability delayed from H2 '25 to H1 '26; vertically disaggregated interconnect bandwidth only 35GB/s per 4-core cluster to base die's L3/mesh.

## p.28 — AMD EPYC Server CPU Leadership + Intel Criticizing AMD's Naples

Figure 1 (AMD slide): "AMD EPYC Server CPU Leadership — Consistent Delivery of Industry-Leading Performance & Efficiency". Package shots: "Naples" 1st Gen, "Rome" 2nd Gen, "Milan" 3rd Gen, "Genoa" 4th Gen, "Turin" 5th Gen.
Caption: "AMD EPYC CPU Generations. Source: AMD".

Figure 2 (Intel slide, Intel Press Workshops – June 2017): "Intel Xeon Scalable Processor Family: Architected for the Data Center — Implementation Matters". Intel side ("fully integrated"): single die maximizes performance; optimized for data sharing between all threads in a socket; mesh architecture enables low and consistent latencies; data center-specific features: up to 8-socket support, AVX-512, QuickAssist Technology, Trusted Execution Technology, RAS, Innovation Engine. AMD Naples side ("partitioned and disjointed"): repurposed desktop dies for server; 4 glued-together desktop dies; inconsistent performance and higher latencies due to die-to-die interconnect.
Caption: "Intel Criticizing AMD's Naples. Source: Intel".

## p.29 — AMD Zeppelin SoC Architecture (An SoC for Multi-chip Architectures)

ISSCC 2018 slide: Zeppelin die annotated with Zen cores, L3, DDR, IFOP, IFIS/PCIe/SATA blocks; arrows to three configurations: Mainstream Desktop (1 die), Performance Server (4-die MCM), High-End Desktop (2 dies + 2 Dummy dies). Slide footer: 2018 IEEE International Solid-State Circuits Conference, "2.4: 'Zeppelin': an SoC for Multi-chip Architectures".
Caption: "AMD Zeppelin SoC Architecture. Source: AMD, ISSCC 2018".
Body text data: Naples 4-die MCM, 8 cores per Zeppelin die, 32 cores total vs Intel's 28; 2 CCX per die, 4 cores + 8MB L3 per CCX.
