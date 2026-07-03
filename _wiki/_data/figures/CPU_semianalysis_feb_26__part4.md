# CPU semianalysis_feb 26.pdf — figure transcriptions (part 4)

Pages covered: 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 56, 58.
Machine transcription of figure/chart pages so the data is text-searchable. Attribution: SemiAnalysis report "CPU semianalysis_feb 26" unless a printed source line says otherwise.

## p.45 — "Five generations of price performance leadership" (Graviton CPU History)

AWS slide showing five Graviton package photos above a table. Banner text at bottom: "Customers trust predictable execution and price/perf curve". Caption: "Graviton CPU History. Source: AWS".

| Graviton Generation | Graviton1 | Graviton2 | Graviton3 | Graviton4 | Graviton5 (NEW!) |
|---|---|---|---|---|---|
| Year | 2018 | 2019 | 2021 | 2023 | 2025 |
| Cores | 16 | 64 | 64 | 96 | 192 |
| Transistors | 5 Billion | 30 Billion | 55 Billion | 73 Billion | 172 Billion |

Body text (key datapoints): AWS first hyperscaler to deploy own cloud CPUs (Annapurna Labs acquisition + ARM Neoverse CSS); Graviton2 = 64 Neoverse N1 cores; Graviton3 (preview late 2021) moved to Neoverse V1, 10x7 Core Mesh Network with 65 cores printed (1 disabled for binning), chiplets: four DDR5 + two PCIe5 I/O chiplets around central compute die on TSMC N5, connected with Intel EMIB.

## p.46 — Graviton5 core diagram

AWS slide "Graviton5". Spec list: 192 cores; 192x 2MB L2; 192 MB LLC; DDR5; PCIe gen6; 3nm; 3rd generation chiplet/package technology. Diagram shows core mesh surrounded by 12 DDR5 blocks (6 left, 6 right) and 8 PCIeG6 blocks (4 top, 4 bottom). Caption: "Graviton5 core diagram. Source: AWS".

Body text: Graviton4 adopted Neoverse V2, core counts and memory channels +50% to 96 cores and 12 channels, 30-45% speedups vs prior gen; PCIe5 lanes tripled 32→96; dual-socket support. Graviton5 (preview since December 2025): 192 Neoverse V3 cores, 172B transistors on TSMC 3nm; L2 2MB/core; shared L3 36MB (Graviton4) → 192MB (Graviton5); memory bandwidth +57% (12-channel DDR5-8800) despite doubling core count. Embedded article link: "Amazon Graviton 3 Uses Chiplets & Advanced Packaging To Commoditize High Performance CPUs | The First PCIe 5.0 And DDR5 Server CPU", Dylan Patel, 2 Dec 2021.

## p.47 — Graviton Pre-Silicon Design

AWS slide "Pre-Silicon Design — Bringing large workloads into the CPU design process". Text on slide: "Before silicon 10,000x slowdown — 1 second of runtime takes three hours; 5 minutes takes a month. Sample workloads in the lab." Caption: "Graviton Pre-Silicon Design. Source: AWS".

Body text: Graviton5 PCIe lanes upgraded to Gen6 but lane count regressed 96 (Graviton4) → 64 (Graviton5); 2 cores share a mesh stop, 8x12 mesh, CPU core mesh split over multiple compute dies. AWS Trainium3 accelerators use Graviton CPUs as head nodes, 1 CPU to 4 XPUs (initially Graviton4, future clusters Graviton5).

## p.48 — Microsoft Cobalt 200 server photo + Cobalt 200 SoC layout

1. Photo: "Microsoft Cobalt 200 Server. Source: Microsoft" (no data content — server board photo).
2. Diagram: "Cobalt 200 SoC (System-on-Chip)". Compute Chiplet 1 detailed: Arm Neoverse V3 CPU, Armv9.2, 66 cores per chiplet; I-Cache/D-Cache; L2 Cache (3MB); System Cache (1.5MB); Data Movement Accelerator (Engine 1/Engine 2, virtualization); Compression and Cryptography Accelerator; 3x Memory Controller + DDR PHY top and 3x bottom; 4x PCIe/CXL + PCIe PHY blocks; System Control (Low-Speed IO). Custom High-Bandwidth Interconnect joins Compute Chiplet 2: "66 Arm Neoverse V3 CPU Cores, 6 Memory Channels, Compression and Cryptography Accelerator, Data Movement Accelerator, System Control". Caption: "Cobalt 200 SoC Layout. Source: Microsoft".

Embedded article link: "Microsoft Infrastructure - AI & CPU Custom Silicon Maia 100, Athena, Cobalt 100", Dylan Patel and Myron Xie, 15 Nov 2023. Body text: Cobalt 200 launched late 2025.

## p.49 — Axion C4A Wafer and Package photos

Photos of Axion C4A wafer display case and packaged part. Caption: "Axion C4A Wafer and Package. Source: Hajime Oguri, Google Cloud Next '24". (no chart data — photos)

Body text datapoints: Cobalt 200 cores 128 → 132, Neoverse V3 (vs N2 prior gen), 3MB L2 per core, CMN S3 mesh across two TSMC 3nm compute dies; each die 8x8 mesh, 6 DDR5 channels, 64 PCIe6 lanes with CXL; 2 cores per mesh stop, 72 cores printed per die, 66 enabled for yield; 192MB shared L3; 50% speedup over Cobalt 100. Cobalt 200 only for Azure general-purpose compute, not AI head nodes; Maia 200 rackscale uses Intel Granite Rapids CPUs.

## p.50 — Axion N4A CPU photo

Photo of Axion N4A package. Caption: "Axion N4A CPU. Source: Google". (no chart data — photo)

Body text datapoints: Axion announced 2024, GA 2025. Axion C4A: up to 72 Neoverse V2 cores, 8 channels DDR5, PCIe5, monolithic 5nm die; wafer images suggest 81 cores printed in 9x9 mesh, 9 disabled for yield; new 3nm die believed designed for 96-core C4A bare metal instances in preview late 2025. Axion N4A in preview with 64 lower-performance Neoverse N3 cores.

## p.51 — The Ampere Roadmap: Powerful Roadmap with Rapid Innovation

Ampere Computing slide. Subtitle: "Continued Commitment to Leadership Performance Per Rack for AI Compute in Air Cooled Environments". Caption: "AmpereOne 2024 Roadmap. Source: Ampere Computing".

AmpereOne Family:
| Product | Specs | Status |
|---|---|---|
| AmpereOne | Up to 192 Cores, 5nm, 8 Ch DDR5 | Shipping Now |
| AmpereOne "M" | Up to 192 Cores, 5nm, 12 Ch DDR5 | Shipping Q4 '24 |
| AmpereOne "MX" | Up to 256 Cores, 3nm, 12 Ch DDR5 | In Fabrication |
| AmpereOne Aurora | Up to 512 Cores, Integrated AI Silicon Training and Inference, Air Cooled | Next Design Product |

Ampere Altra Family: Up to 80 Cores 7nm 8 Ch DDR4; Up to 128 Cores 7nm 8 Ch DDR4 — "Continued Ship Support at Least Through 2030".

Body text: Axion N4A is full custom Google design on TSMC 3nm; Google to design Axion CPUs as head nodes in TPU clusters powering Gemini.

## p.52 — Ampere Altra Max and Altra die shots

Die photos. Caption: "Ampere Altra Max (Left) and Altra (Right). Source: Ampere Computing". (no data content — die photographs)

## p.53 — Delidded AmpereOne CPU

Photo of delidded AmpereOne package showing chiplets. Caption: "Delidded AmpereOne CPU. Source: Brendan Crain, Wikimedia". (no data content — package photo)

## p.54 — AmpereOne Compute Chiplet (mesh architecture)

Ampere Hot Chips 2024 slide. Bullets: TSMC 5nm; fully connected 8x9 mesh, up to 5.7 TB/s cross-sectional bandwidth; 192 Ampere custom CPU cores arranged in 6 columns of 8 clusters, 2 MB private L2 cache per core; 64 distributed coherency engines, 1 MB system level cache each (64 MB total), snoop filter tracking. Labels: Core Cluster, System Level Cache, Snoop Filter, Die-to-Die Interface. Caption: "AmpereOne Mesh Architecture. Source: Ampere Computing, Hot Chips 2024".

Body text datapoints: Ampere Altra 80-core / Altra Max 128-core, Neoverse N1, 4-core clusters, 8 channels DDR4, 128 PCIe4 lanes, single TSMC 7nm die. AmpereOne: 192 cores, 5nm, chiplet MCM (separate DDR5 and PCIe dies, no interposer), custom ARM core, 2MB L2, 9x8 mesh; integer performance doubled vs Altra Max. AmpereOne-M adds 2 memory controller dies (12-channel); AmpereOne-MX reuses I/O chiplets with a 3nm compute die.

## p.56 — "Enabling a Faster Path to Custom Silicon" (ARM CSS positioning chart)

ARM Neoverse slide (© 2023 Arm). Conceptual scatter: X axis "DIFFERENTIATION & CUSTOMIZATION", Y axis "COST & RISK". Points low→high: SoC ("Lowest development cost, but no differentiation or customization"); CSS ("*New* validated CSS to accelerate development at lower cost"; CSS+IP boxed as "Optimal for Custom Silicon Development"); IP ("Fully customizable SoC but requires considerable design effort to tune and validate"); Arch ("Ground-up custom design, but requires world-class design resources and years to develop"). Caption: "ARM's CSS Offerings Balance Customization with Development Cost. Source: ARM".

Body text datapoints: over 1 Billion Neoverse cores deployed across datacenter CPUs and DPUs; 21 CSS licenses signed across 12 companies; datacenter royalty revenue more than doubled YoY; CSS projected >50% of royalty revenue in next couple of years. ARM in 2026 offering full datacenter CPU designs, codename Phoenix, Meta first customer; ARM also designing custom CPUs for OpenAI (Stargate OpenAI SoftBank venture); Cloudflare a prospective Phoenix customer. Embedded article link: "Arm and a Leg: Arm's Quest To Extract Their True Value", Dylan Patel, Myron Xie, and 2 others, 14 Sep 2023.

## p.58 — Die shots (uncaptioned on this page)

(no data content — full-page die shot images: two identical large compute-die shots stacked plus one darker I/O-style die at bottom; no legible labels, axis, or caption visible on the page)
