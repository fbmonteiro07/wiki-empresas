# CPU semianalysis_feb 26.pdf — figure transcriptions (part 1)

Pages covered: 1, 2, 3, 4, 7, 10, 11, 12, 13, 15, 16, 17.
Machine transcription of figure/chart pages for text-search purposes. Report: "CPUs are Back: The Datacenter CPU Landscape in 2026", Gerald Wong and Dylan Patel, SemiAnalysis, Feb 09 2026 (paid).

## p.1 — Cover page

(no data content — report title page: "CPUs are Back: The Datacenter CPU Landscape in 2026"; subtitle "RL and Agent Usage, Context Memory Storage, DRAM Pricing Impacts, CPU Interconnect Evolution, AMD Venice, Verano, Florence, Intel Diamond Rapids, Coral Rapids, Arm Phoenix + Venom, Graviton 5, Axion"; byline Gerald Wong and Dylan Patel, Feb 09 2026; hero illustration of a CPU with sunglasses.)

## p.2 — Intel Q4'25 DCAI Revenue (Intel earnings slide)

Chart: "DCAI" — bars for Segment Revenue and Segment Op Income ($B), line for Segment OM%.

| Quarter | Segment Revenue ($B) | Segment Op Income ($B) | Segment OM% |
|---|---|---|---|
| Q4'24 | $4.4 | $0.4 | 8.6% |
| Q1'25 | $4.1 | $0.6 | 13.9% |
| Q2'25 | $3.9 | $0.6 | 16.1% |
| Q3'25 | $4.1 | $1.0 | 23.4% |
| Q4'25 | $4.7 | $1.3 | 26.4% |

Slide tagline: "Strong Sustainable Demand, Working with Customers to Support Needs Beyond 2026."
Caption: "Intel Q4'25 DCAI Revenue. Source: Intel"

## p.3 — SemiAnalysis Datacenter CPU Core Count Trend 1998–2028

Line chart. Y-axis: Core Count (0, 64, 128, 192, 256, 320, 384, 440, 512). X-axis: years 1998–2028. Series (legend): AMD, Intel SP, Intel AP, Intel E, NVIDIA, Ampere, AWS Graviton, Google Axion C, Google Axion N, Microsoft Cobalt, ARM, Huawei Kunpeng.
Legible shape: all series near 0–low single/double digit cores through ~2017; inflection from ~2018 (~64 cores) rising steeply after 2023; by 2024–2025 several series at ~64–192; by 2026–2028 series fan out to ~128, ~256, ~288, ~320 and one series reaching ~512 cores in 2028. Individual per-series values [illegible].
Caption: "Datacenter CPU Core Count Trend. Source: SemiAnalysis Estimates" (chart footer: "Source: SemiAnalysis Estimates").

## p.4 — Intel Pentium Pro

(no data content — photograph of Intel Pentium Pro chip package. Caption: "Intel Pentium Pro. Source: Intel".)

## p.7 — Pat Gelsinger photo

(no data content — photo of Pat Gelsinger receiving a VMware tattoo. Caption: "Pat Gelsinger, VMware CEO 2012-2021, Intel CEO 2021-2024. Source: X @PGelsinger".)

## p.10 — AMD Turin Dense 7:1 Socket Consolidation (AMD slide) + Microsoft Fairwater satellite photos

Infographic: "Easily Upgrade to 5th Gen AMD EPYC CPUs — Modernize your data center — Add more capacity for your compute needs"
- 1000 Old Servers (2P Intel Xeon Platinum 8280 servers) → 131 Modern Servers (2P AMD EPYC 9965 servers); ratio "7 to 1".
- "Easy to migrate to AMD: X86 architecture, Mature ecosystem, Robust tools."
- Up to 68% less power; up to 87% fewer servers; up to 67% lower 3-yr TCO.
- Footnote: "Servers required to achieve a total of 391,000 SPECrate 2017_int_base performance score."
Caption: "AMD Turin Dense 7:1 Socket Consolidation. Source: AMD"

Second figure: three satellite images of Microsoft "Fairwater" datacenters, labeled November 2025, November 2025, March 2025. Annotations: "295MW GPU Building" and "48MW CPU Building" in each campus (one image annotates 295MW GPU Building only plus 48MW CPU building).
Caption: "Microsoft 'Fairwater' GPU and CPU buildings. Source: Google Earth"

## p.11 — Reinforcement Learning Training Loop diagram

Diagram: boxes Trainer, Generator, RL Env. Arrows: 1. Trainer → Generator; 2. Generator → RL Env; 3. RL Env → Generator; 4. Generator → Trainer.
Caption: "Reinforcement Learning Training Loop. CPUs used in RL Environment (Green). Source: SemiAnalysis"
Adjacent text datapoints: Microsoft Fairwater — 48MW CPU and storage building supports the main 295MW GPU cluster.

## p.12 — Text page

(no data content — body text on RL/agentic CPU demand; notes CPU:GPU power ratio 1:6 seen in Fairwater, possibly higher for Rubin generation; embedded link card to "Scaling Reinforcement Learning: Environments, Reward Hacking, Agents, Scaling Data", Dylan Patel and AJ Kourabi, 8 June 2025; AMD sees server CPU TAM growing "strong double digits" in 2026.)

## p.13 — Intel Tulsa Die Shot (Hot Chips 2006 slide)

Die-shot slide: "Tulsa Die Shot" — two CORE blocks, Clock, unCore, PADS, and "16 MBy LLC" (16MB last-level cache shared between two cores). Slide footer: "INTEL Corporation — 19, 21 Aug 06, The Tulsa Processor, JDG".
Caption: "Intel Tulsa Die Shot. Source: Intel, Hot Chips 2006"

## p.15 — AMD Opteron Istanbul die

(no data content — die photograph of AMD Opteron Istanbul 6-core die. Caption: "AMD Opteron Istanbul 6-core die. Source: AMD".)

## p.16 — Intel Nehalem-EX Ring Interconnect (Hot Chips 2009 slide)

Slide: "On-die network: Ring Interconnect" (Nehalem-EX Architecture, Hot Chips 2009).
- High BW Ring Interconnect: two counter rotating rings; average latency 1/2 of unidirectional ring; 4X the BW of unidirectional ring; 4 protocol rings; data ring 32 Bytes in each direction.
- Simple arbitration rules: ring advances one stop per clock; "rotary rules" — traffic on the ring wins arbitration; ring stops shared by core/cache; ring stops tagged as "even"/"odd" polarities; ring stops only sink from a single ring/polarity per cycle; ring traffic injector responsible for polarity match at target polarity.
- Scalable fabric: BW scales with ring stops; simulated >250GB/s of interconnect BW.
- Diagram: 8 cores (Core0–Core7) with LLC Slice0–Slice7 around two rings; QPI0–QPI3 links, MC0/HA0, CA0, Router, CA1, HA1/MC1, SMI0, SMI1.
Caption: "Intel Nehalem-EX Ring Interconnect. Source: Intel, Hot Chips 2009"

## p.17 — Intel Ivytown Virtual Rings (Hot Chips 2014 slide)

Slide: "Scalable On-die Interconnect" — Goal: scalable ring performance (keep latency and area increase in check; improve performance); 3 virtual rings; North/South switches dynamically configure the rings. Two diagrams: "Clockwise" Outer Ring and "Counter-clockwise" Outer Ring — Slice columns, HA (Home Agent) blocks, R3 QPI, R2 PCIE stops. Overview diagram of Ivy Bridge-EX die: cores in three columns of five (15 cores), QPI agents, Home Agents, DDR3/SMI2 memory controllers.
Caption: "Intel Ivytown Virtual Rings. Source: Intel, Hot Chips 2014"
