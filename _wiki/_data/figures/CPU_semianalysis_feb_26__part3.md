# CPU semianalysis_feb 26.pdf — figure transcriptions, part 3 (pages 30, 31, 32, 33, 34, 36, 38, 39, 40, 42, 43, 44)

Machine transcription of figure/chart pages for text-search purposes. Attribution: SemiAnalysis report "CPU semianalysis_feb 26.pdf"; each figure carries its printed source line.

## p.30 — SOC Architecture: Rome/Milan 9-die MCM

AMD slide (marked AMD Confidential). Caption: "Rome and Milan SoC Architecture. Source: AMD"

- Diagram: "ROME/MILAN 9 DIE MCM" — central "Memory / IO Die" with DDR4 interfaces, surrounded by eight "8 Cores + L3" CCDs connected via GMI-2 links (G Links); 2x 25G SERDES blocks; legend: dashed line = SATA capable on lower 8 lanes; shaded box = DIE.
- Right side, cache diagrams:
  - Zen2/Rome: two 4-core CCXs per CCD, each Z2 core with L2, 16MB L3 per CCX (2x 16MB L3).
  - Zen3/Milan: single 8-core CCX, each Z3 core with L2, shared "32+ MB L3".
- Body text data points: 2019 Rome = 64-core (Intel stuck at 28 cores); eight 8-core CCDs on TSMC N7, I/O die on GlobalFoundries 12nm; Rome appears as sixteen 4-core NUMA nodes with 2 NUMA domains; Milan (2021) increased CCX size to 8 cores via ring bus, reusing Rome I/O die.

## p.31 — Scale-Out: AMD Turin-Dense

AMD slide. Caption: "AMD Turin-Dense. Source: AMD"

- Up to 12 "Zen 5c" CCDs; 192 Cores; 384 Threads. Package photo with 12 CCDs around central I/O die.
- Body text data points: 2022 Genoa = 12 CCDs; 2024 Turin up to 16 CCDs on 128-core EPYC 9755; DDR5 and PCIe5 I/O die; Bergamo used Zen 4c; Turin-Dense variant 192-core Zen 5c; EPYC 8004 Siena = 4 Zen 4c CCDs on 6-channel memory platform.
- Inline article card: "Zen 4c: AMD's Response to Hyperscale ARM & Intel Atom" — Dylan Patel and Gerald Wong, 5 June 2023.
- Section heading begins: "Intel Diamond Rapids Architecture Changes".

## p.32 — Next-gen Xeon (Diamond Rapids Overview)

Slide. Caption: "Diamond Rapids Overview. Source: HEPiX via @InstLatX64" (footer: HEPiX TechWatch WG: CPU/GPU/AI)

- Targeted for 2026; new platform "Oak Stream" — two variants: 8-ch and 16-ch; PCIe Gen6.
- New SoC "Diamond Rapids": built on Intel 18A node; up to 4 compute tiles per CPU, 192 cores max; 500W TDP; 1S, 2S, 4S configuration; increased efficiency of AMX; native TF32, FP8 support.
- Diagram: 4 corner "Cores" tiles flanking two central I/O rows with DDR, PCIe 6, CXL 3, UPI 3, +4L PCIe4 blocks.
- Body text data points: Granite Rapids mesh 10x19; four Core Building Block (CBB) dies flank two I/O and Memory Hub (IMH) dies; within each CBB, 32 Dual Core Modules (DCM) on Intel 18A-P hybrid bonded onto base Intel 3-PT die (L3 + mesh); 2 cores share common L2 per DCM; 256 cores total, only up to 192 enabled for mainline SKUs; IMH dies: 16-channel DDR5, PCIe6 with CXL3, Intel accelerators (QAT, DLB, IAA, DSA); die-to-die interconnect no longer requires EMIB (substrate traces).

## p.33 — Single-Thread Optimized (Intel removes SMT on P-cores)

Intel slide (Intel Tech Tour TW). Caption: "Intel removes SMT on their P-cores. Source: Intel"

- Comparison: P-core with Hyper-Threading ON (HT on, 2 threads per core) vs P-core Efficiency optimized (1 thread, optimized core).
- Figures for optimized (SMT-less) P-core vs HT-capable P-core: +5% Perf/power; -15% Perf/area; +15% Perf/power/area. Fine print: "All figures estimated based on hypothetical comparison of HT-capable P-core vs. Optimized P-core."
- Body text data points: SMT removal started with Lion Cove in 2024 client PC; vs 128-core/256-thread Granite Rapids, the 192-core/192-thread Diamond Rapids expected only ~40% faster (SemiAnalysis expectation); Intel cancelled the mainstream 8-channel Diamond Rapids-SP platform, leaving highest-volume core market without a new generation into at least 2028.

## p.34 — AMD "Venice" die layout

Caption: "AMD Venice die layout. Source: @HighYieldYT" (marked "Analysis by HighYield")

- AMD "Venice": 256-core Zen 6, TSMC N2 + N6.
- 8x CCD: 32C Zen 6 each, TSMC N2P, ~160mm² each.
- 2x IO-die: TSMC N6, ~350mm² each, flanked by IPD blocks.
- Body text: AMD adopts EMIB-equivalent advanced packaging for Venice; high-speed short-reach links CCD→I/O die; volumes in SemiAnalysis "Accelerator, HBM, and Advanced Packaging Model".

## p.36 — Delivering the Next Generation of Performance ("Venice")

AMD slide. Caption: "AMD Venice Performance Claims. Source: AMD"

- Next Generation "Venice" EPYC: >1.3x Thread Density; >1.7x Performance & Efficiency. Fine print: "See Endnote VEN-001A. Performance/watt efficiency based on SPECrate2017_int_base performance projection/processor TDP."
- Body text data points: top 256-core Venice >1.7x perf/W vs top 192-core Turin in SPECrate®2017_int_base; Zen 6 new instructions AVX512_FP16, AVX_VVNI_INT8, AVX512_BMM (bit matrix multiplication, 16x16 binary matrices, OR/XOR accumulate); 96c Turin matches 128c Granite Rapids (perf per core); AMD to introduce 8-channel Venice SP8 platform as Intel cancels its 8-channel part.

## p.38 — AMD Venice Costing (BoM tables, values redacted)

Caption (on p.39): "AMD Venice BoM Costing. Source: SemiAnalysis Estimates, sales@semianalysis.com". Value cells are blacked out (paywalled/redacted) — shown as [illegible].

Table: AMD Venice Costing

| Variant | SP7-D | SP7-C | SP8-D | SP8-C |
|---|---|---|---|---|
| Compute Die Dense CCD32 | 8 | 0 | 4 | 0 |
| Compute Die Classic CCD12 | 0 | 8 | 0 | 8 |
| IO Die SP7 | 2 | 2 | 0 | 0 |
| IO Die SP8 | 0 | 0 | 2 | 2 |
| Active Silicon Cost | [illegible] | [illegible] | [illegible] | [illegible] |
| Advanced Packaging Cost | [illegible] | [illegible] | [illegible] | [illegible] |
| Advanced Packaging Yield | [illegible] | [illegible] | [illegible] | [illegible] |
| Testing Cost (ATE/SLT) | [illegible] | [illegible] | [illegible] | [illegible] |
| Test Pass Rate | [illegible] | [illegible] | [illegible] | [illegible] |
| **Total Unit Cost** | [illegible] | [illegible] | [illegible] | [illegible] |

Table: Active Silicon Cost

| Die | CCD32 | CCD12 | IO SP7 | IO SP8 |
|---|---|---|---|---|
| Node | N2 | N2 | N6 | N6 |
| Wafer Cost (Wfr+bump+sort) | [illegible] | [illegible] | [illegible] | [illegible] |
| Length | [illegible] | [illegible] | [illegible] | [illegible] |
| Width | [illegible] | [illegible] | [illegible] | [illegible] |
| GDPW | [illegible] | [illegible] | [illegible] | [illegible] |
| Sort Yield | [illegible] | [illegible] | [illegible] | [illegible] |
| **Cost per Die** | [illegible] | [illegible] | [illegible] | [illegible] |

Table: Advanced Packaging Cost — rows: CoWoS-L Wafer Cost, Interposers Per Wafer, Silicon Bridges Per Interposer, Advanced Packaging Unit Cost — all values [illegible].

Table: Packaging Cost (columns SP7, SP8) — first row Substrate Unit Cost (continues onto p.39) — values [illegible].

## p.39 — Packaging Cost table (cont.) + Nvidia Grace Hopper Superchip

- Continuation of Packaging Cost table (values [illegible]): Lid/Stiffener Ring Cost, Package Capacitors Cost, TIM Cost, Total Packaging Unit Cost. Caption: "AMD Venice BoM Costing. Source: SemiAnalysis Estimates, sales@semianalysis.com". Italic text notes SemiAnalysis offers BoM costing for AMD Turin, Venice, Intel Granite Rapids, Diamond Rapids, NVIDIA Grace, Vera and hyperscale ARM CPUs from AWS, Microsoft, Google.
- Figure: "NVIDIA Grace Hopper Superchip". Caption: "Nvidia's Grace CPU connections. Source: NVIDIA"
  - Grace CPU: CPU LPDDR5X ≤512 GB (x2 shown), ≤546 GB/s memory bandwidth; High-Speed I/O via 4x 16x PCIe-5 = 512 GB/s.
  - NVLink C2C 900 GB/s between Grace CPU and Hopper GPU.
  - Hopper GPU: GPU HBM3 ≤96 GB (x2 shown), ≤3000 GB/s; 18x NVLink 4 = 900 GB/s to NVLink Network ≤256 GPUs. "Hardware Consistency" domain.

## p.40 — Nvidia Grace Scalable Coherency Fabric

Caption: "Nvidia Grace Scalable Coherency Fabric. Source: NVIDIA"

- 72 Cores — Arm Neoverse V2 cores with 2X Perf/W over "today's server"; 117 MB L3 cache; 900 GB/s NVLink C2C; 3.2 TB/s NVIDIA Scalable Coherency Fabric; 500 GB/s LPDDR5X with ECC.
- Body text data points: NVLink-C2C 900GB/s bi-directional; up to 480GB memory per Grace CPU; LPDDR5X 500GB/s on 512-bit bus; Grace Hopper 1 Grace per GPU, Grace Blackwell 1 CPU per 2 GPUs; dual-Grace superchip for HPC; Neoverse V2 with 1MB private L2 on 6x7 mesh housing 76 cores (up to 72 enabled for yield), 117MB L3; Cache Switch Node connects up to 2 cores + L3 slices; 3.2TB/s bisection bandwidth; Grace Performance Tuning Guide: code-locality optimization can yield 50% speedups.

## p.42 — NVIDIA Vera Rubin diagram

Caption: "Vera Rubin NVLink C2C Diagram. Source: NVIDIA"

- CPU:GPU coherent memory. Vera CPU with CPU LPDDR5X up to 1.5 TB; PCIe Gen 6 on both sides; NVLINK C2C 1.8 TB/s to two Rubin GPUs, each with GPU HBM4 288 GB (plus additional GPU HBM4 blocks below).

## p.43 — NVIDIA Vera CPU specifications

NVIDIA slide. Caption: "Vera CPU Specifications. Source: NVIDIA". Subtitle: "Built for data movement and agentic processing".

- 88 NVIDIA custom Olympus cores; 176 threads with NVIDIA Spatial Multi-threading; 1.8 TB/s NVLink-C2C enabling CPU:GPU coherent memory; 1.5 TB system memory (3X Grace); 1.2 TB/s memory bandwidth with SOCAMM LPDDR5X; rack-scale confidential compute.
- Bottom banner: 2X Data Processing; 2X Compression; 2X CI/CD.

## p.44 — Vera Floorplan Annotated

Caption: "Vera Floorplan Annotated. Source: NVIDIA, SemiAnalysis Estimates"

- Annotated die photo: I/O chiplet (PCIe 6.0, CXL 3.1) at top; central compute die "Olympus CPU cores, 162MB L3"; four LPDDR CTRL+PHY chiplets on the sides; NV-HBI links; NVLINK-C2C at bottom.
- Body text data points: custom Olympus core supports SMT — 88 cores / 176 threads; last NVIDIA custom core was Tegra Xavier SoC 8 years ago (10-wide Carmel cores); ARMv9.2 Olympus FPU widened to 6x 128b-wide ports vs 4 on Neoverse V2; supports ARM SVE2 FP8; 2MB private L2 per core (doubled from Grace); Nvidia claims 2x performance improvement going to Vera.
- Next section heading begins: "AWS Graviton5".
