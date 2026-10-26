# Figure transcriptions — UBS, 'US Semiconductors: $210B Server CPU TAM By C2030; Gated By Memory Supply', 26-Oct-2026

UBS Global Research — Timothy Arcuri, Seth Cho. 39 pp; every table and chart is an image (narrative text only in the PDF text layer). Transcribed 2026-10-26 from 300+ dpi renders; Figs 25-31 extracted from the PDF's vector chart geometry (digitized, not printed numbers; segment labels where printed). Only PRINTED values are reproduced below — recomputed check columns are omitted. Full workbook with tie-outs and the DRAM<->CPU model: `_wiki/models/UBS_CPU_DRAM_2026-10-26.xlsx`. Original: `_inbox/_done/20261026_UBS_Arcuri_Server-CPU-TAM-gated-by-memory_ued53830.pdf`; render: `relatórios bons/20261026_UBS_210B_Server_CPU_TAM_By_C2030_Gated_By_Memory_Supply.html`.

Ratings in the note (p.29, prices 23-Oct-2026): AMD Buy (CBE) US$516.79; ARM Buy US$210.33 (PT $320, 1.8x PEG); INTC Neutral US$86.96 (PT cut $103 -> $100, SOTP); MU Buy US$877.55.

Headline (p.1-2): C2030 server-CPU TAM raised ~$175B -> ~$210B (bottom-up $208B: 30MM traditional + 37MM AI CPUs, ~77EB DRAM); 'unconstrained' demand ~150MM CPUs / $500B+ / 282EB DRAM, but memory supply caps it; CPU:GPU attach ~0.83:1 in C2030 (practitioners target 3-4:1); traditional CPU ~0.5TB DRAM today vs AI CPU ~1.5TB, 2-3TB in coming generations; CXL reuse of DDR4 adds high-single-digit % to supply; META Muse a demand signal, not a needle mover (~1MM units even at 1B users); read-throughs: DRAM (DDR), ABF substrates, TSMC, PCBs, MLCCs (Murata+SEMCO ~80% server MLCC share), WFE and test. 'We continue to believe MU is the best way to play server CPU demand.'

## p.3 — Figure 1: CPU requirements vary by different workloads (p.3)


_UBS layering of Dell white paper 'Characterizing CPU Demand for Agentic AI: Three Agentic Workloads on the Dell PowerEdge R7725' (14-Sep-26); R7725 = 2x AMD Turin 64-core CPUs_

| Workload tested | What the agent does | Workload CPU requirements | CPU quota per agent (cores) | Sustained agents on 2x AMD 64-core Turin | Measured CPU:GPU demand (x:1) | % of consumer agentic workload (UBSe) | Measured CPU cores:GPU (x:1) | Check: cores/GPU = CPU:GPU x 128 cores |  |
|---|---|---|---|---|---|---|---|---|---|
| Workload 1: pypi-server | Writes a Python package and serves it from a local package index | Light CPU: mostly model/code generation with short tool calls | 1 | 512 | 1 | 0.65 | 128 |  |  |
| Workload 2: sqlite-with-gcov | Compiles SQLite with code-coverage instrumentation and fixes build errors | Bursty CPU: compiler runs substantially between model reasoning turns | 1 | 238 | 7 | 0.3 | 896 |  |  |
| Workload 3: mcmc-sampling-stan | Writes a statistical model, compiles it, then runs computationally heavy sampling | Heavy CPU/HPC: sustained multi-core numerical computation | 4 | 60 | 18 | 0.05 | 2,304 |  | printed '<5%' — 5% used as upper bound |
| Blended CPU ratio (printed) |  |  |  | CPU:GPU | 4 | printed 4:1 |  |  |  |
|  |  |  |  | CPU cores:GPU |  |  | 421 |  |  |

_Capstone transcription note: Each row has cores:GPU = 128 x CPU:GPU (2 x 64-core Turin), so the printed blended 421 cores:GPU implies 421/128 = 3.29:1 whatever the weights (a ~3% weight on workload 3 reproduces it). The table's '4:1' is the outlier; the text's '~3:1' / 'we use 3:1' agree with 421._


_Capstone transcription note: Note text (p.3-4): layering this over Dell -> ~3:1 CPU:GPU on the current CPU generation, ~400 cores:1 GPU; core counts double every ~3-4 yrs (~500 cores/CPU by decade-end) but accelerator perf rises too -> UBS uses 3:1 in its demand estimate. Prior framework: ~0.33 standalone + ~0.5 head-node = ~0.85 CPUs/GPU._


## p.4-5 — Figures 2-3: META Muse CPU sizing (p.4-5)


_Muse ~2.5MM DAUs weeks after release; UBS: Muse is a demand signal, not a needle mover (~1MM units even at 1B users with 5-10% provisioning vs ~23MM CPUs shipped C2025)_

| Figure 2: META Muse Sensitivity Table |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| Scenario input | Base Case | High Engagement | Notes (as printed) |  |  |  |
| Daily Active Users (DAU) | 3,000,000 | 3,000,000 | UBSe (printed '3MM') |  |  |  |
| Peak Concurrent Sandboxes (% of DAU) | 0.25 | 0.5 | UBSe |  |  |  |
| vCPUs per Sandbox | 2 | 2 | META |  |  |  |
| Oversubscription | 4 | 1 | Conservative vs. Firecracker/DeepSeek |  |  |  |
| Cores per CPU | 126 | 126 | AMD EPYC 9D25 (126 cores/252 threads) |  |  |  |
| Math | Base (recomputed) | High (recomputed) | Printed base | Printed high | Math (as printed) |  |
| Concurrent Sandboxes |  |  | 1MM | 2MM | DAU x Concurrency |  |
| vCPUs Demanded |  |  | 2MM | 3MM | Sandboxes x vCPUs per Sandbox |  |
| Cores Needed |  |  | 375K | 3MM | vCPUs / Oversubscription |  |
| CPU Units (EPYC chips) |  |  | 2.98K | 23.81K | Cores needed / Cores per CPU |  |

_Capstone transcription note: Printed 'Concurrent Sandboxes 1MM / vCPUs 2MM' are rounded from 0.75MM / 1.5MM; the cores and CPU-unit lines use the unrounded values._

| # of CPU units — concurrency x oversubscription (printed) |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| Concurrency | 1x | 2x | 4x | 8x | Check 1x (recomputed) | Max /printed - recomputed/ in row |
| 0.1 | 4,762 | 2,381 | 1,190 | 595 |  |  |
| 0.25 | 11,905 | 5,952 | 2,976 | 1,488 |  |  |
| 0.5 | 23,810 | 11,905 | 5,952 | 2,976 |  |  |
| 1 | 47,619 | 23,810 | 11,905 | 5,952 |  |  |

_Figure 3: Assuming 5-10% Target Utilization (thread-based sizing)_

| Line | Base Case | High Engagement | Base recomputed | High recomputed | Notes (as printed) |  |
|---|---|---|---|---|---|---|
| Daily Active Users (DAUs) | 3,000,000 | 3,000,000 |  |  | Unique users who open Muse on a given day |  |
| (x) vCPUs per Sandbox | 2 | 2 |  |  | Virtual CPUs allocated to each user's virtual machine (VM) |  |
| Total Capacity Needed (Threads) | 6,000,000 | 6,000,000 |  |  | Hardware needed if every DAU ran at once on dedicated hardware at one thread per vCPU |  |
| (x) Peak Concurrent Sandboxes (% of DAUs) | 0.2 | 0.3 |  |  | UBSe share of DAU with a live sandbox (a running VM, whether active or idle) during peak hours |  |
| Concurrent sandboxes | 600,000 | 900,000 |  |  | # of VMs alive at peak |  |
| (/) Target Utilization | 0.7 | 0.65 |  |  | UBSe how fully the provisioned capacity runs at peak, remainder = headroom |  |
| Sandboxes Provisioned | 857,143 | 1,384,615 |  |  | Sandbox slots built, including headroom |  |
| vCPUs Provisioned | 1,714,286 | 2,769,231 |  |  | vCPUs across all provisioned slots |  |
| (/) Oversubscription | 3 | 3 |  |  | UBSe vCPUs sharing one physical hardware thread (benchmarked vs DeepSeek and AWS) |  |
| Threads Provisioned | 571,429 | 923,077 |  |  | Physical hardware threads needed after sharing |  |
| Hardware Deployed (% of total capacity) | 0.1 | 0.15 |  |  | UBSe: heavily oversubscribed cloud workloads deploy 5-10% of dedicated-equivalent hardware in base case |  |
| (/) Usable Threads per CPU | 240 | 230 |  |  | Hardware threads available for sandboxes after host OS and hypervisor take their share |  |
| # of CPUs being used | 2,382 | 4,012 |  |  | # of CPUs required |  |

## p.6 — Figure 4: Unconstrained Estimates Suggest a $500B+ CPU TAM by C2030 (p.6)

| Unconstrained Demand Ests | 2025 | 2027E | 2030E | Comment |
|---|---|---|---|---|
| Accelerators (NVDA, AMD, TPU, Trn), MM | 9 | 29 | 44 | Assumes units stay the same but TDP/performance increases; printed '~44' |
|  Head node CPU, MM | 3 | 11 | 22 | UBSe based announced systems; printed '~22' |
|   Head Node CPU-to-GPU attach rate | 0.29 | 0.36 | 0.5 |  |
|   Head Node ASP ($) | 2,430 | 3,160 | 4,480 | Higher ASP given higher portion of NVDA CPUs |
|  Standalone (outside of rack), MM | 0 | 20 | 95 | Additional CPU units outside of rack; printed '~20' / '~95' |
|   Standalone CPU-to-GPU attach rate |  | 0.69 | 2.16 | 3CPU:1GPU target ratio ex-head nodes and 50% of trad CPUs for tool calls |
|   Standalone CPU ASP ($) |  | 2,850 | 4,223 | Assumes higher share of x86 even over time for multithread |
| AI CPU Market (Bottom-up Ests), MM | 3 | 30 | 117 |  |
| AI CPU ASP ($) | 2,430 | 2,957 | 4,271 | Higher core counts and clock speeds increasing ASPs (row printed 'AI CPU ASP, K' but values are $) |
| AI CPU Market (Bottom-up Ests), $B | 7 | 90 | 500 |  |
| CPU-to-GPU Attach | 0.29 | 1.05 | 2.66 |  |
| Implied Total CPUs (AI + Traditional), MM | 23 | 56 | 147 |  |
| Implied Total CPU TAM, $B | 31 | 125 | 548 |  |
| Implied DRAM Memory, EB |  |  |  | Row printed blank in Fig 4 — the DRAM figure (282EB) is in Fig 8 |

## p.6 — Figure 5: Memory Demand For Agentic Workloads is 3-4x Higher vs Traditional CPUs (p.6)

| DRAM / CPU (TB) — as printed | C2025/26 | C2026/27 | C2030E | Growth | low 25/26 | high 25/26 | low 26/27 | high 26/27 | low 30E | high 30E | mid 25/26 | mid 26/27 | mid 30E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Traditional CPU | ~0.25-0.5TB | ~0.5-0.75TB | ~1.0TB | ~1.5-2x | 0.25 | 0.5 | 0.5 | 0.75 | 1 | 1 |  |  |  |
| AI head-node CPU | ~1-1.5TB | ~1-1.5TB | ~1.5-2TB | ~1.5x | 1 | 1.5 | 1 | 1.5 | 1.5 | 2 |  |  |  |
| AI standalone / agentic CPU | ~1.5-2TB | ~1.5-2TB | ~2-3TB | ~1.5x | 1.5 | 2 | 1.5 | 2 | 2 | 3 |  |  |  |
| Blended AI CPU | ~1.5TB | ~1.5TB | ~2-2.5TB | ~1.5x | 1.5 | 1.5 | 1.5 | 1.5 | 2 | 2.5 |  |  |  |

_UBS text (p.6): traditional ~0.5TB today -> ~1TB by end of decade; AI head-node already >1.5TB -> ~2TB; AI standalone may reach ~3TB over the next few generations. Low/high/mid columns are the printed ranges split into numbers for the link sheet._


## p.6-7 — Figures 6-7: UBSe DRAM capacity by vendor and ex-HBM DRAM available for CPUs (p.6-7)

| Figure 6: UBSe DRAM Capacity by Vendor (EB) |  |  |  |  |
|---|---|---|---|---|
| EB | C2025 | C2027E | C2030E | Note |
| Samsung | 14 | 19 | 31 |  |
| SK Hynix | 10 | 16 | 22 |  |
| Micron | 9 | 13 | 26 |  |
| CXMT | 3 | 6 | 10 |  |
| Total | 36 | 55 | 89 | printed total |

_Figure 7: Our Current Base Case Memory Model Suggests 77EB for Server DRAM in C2030_

| ex-HBM DRAM Market (EB) | C2025 | C2027E | C2030E | Note |
|---|---|---|---|---|
| MU DRAM ex-HBM | 9 | 13 | 23 |  |
| Total Mkt (MU share, UBS Ests) | 36 | 54 | 99 | MU ex-HBM / assumed MU share |
| Total non-HBM DRAM Mkt | 36 | 55 | 89 | equals Fig 6 total |
| Non-Server DRAM | 26 | 27 | 30 |  |
| Server DRAM Memory | 11 | 27 | 69 |  |
| Old DDR Reuse via CXL (UBS Ests) |  | 2 | 7 |  |
| Total DRAM Memory for CPUs, EB | 11 | 29 | 77 |  |

_UBS text (p.7): META at AI Infra Summit showed a 1TB server using a 3:1 mix of DDR5 RDIMMs and CXL-attached DDR4; usable in 25-33% of 4 META CPU-workload fleets -> UBS: +6-8% memory capacity via reuse of older RDIMMs (experts: high-single-digit %)._


## p.7 — Figure 8: The 3:1 CPU:GPU Attach Ratio Results in DRAM Demand ~4x Above UBS Estimates (p.7)

| DRAM / CPU | C2025 CPU, MM | C2025 DRAM, EB | C2027E CPU, MM | C2027E DRAM, EB | C2030E Base CPU, MM | C2030E Base DRAM, EB | C2030E Unconstr. CPU, MM | C2030E Unconstr. DRAM, EB |
|---|---|---|---|---|---|---|---|---|
| Traditional CPU | 20 | 10 | 26 | 12 | 30 | 15 | 30 | 15 |
| AI head-node CPU | 3 | 3 | 11 | 11 | 22 | 33 | 22 | 33 |
| AI standalone / agentic CPU | 0 | 0 | 5 | 7 | 15 | 29 | 117 | 234 |
| Total CPU, MM | 23 |  | 41 |  | 67 |  | 169 |  |
| Implied DRAM, EB |  | 14 |  | 29 |  | 77 |  | 282 |
| Implied TB per CPU (DRAM EB / CPU MM) |  |  |  |  |  |  |  |  |

_Capstone transcription note: Note: the Unconstrained column puts 117MM in the standalone row — 117MM is Fig 4's TOTAL AI CPU count (22 head-node + 95 standalone), giving 169MM CPUs vs Fig 4's 147MM and the text's '~150MM' (3 x 44 - 15 also equals 117, so the mechanism is not provable). On UBS's own TB/CPU, 147MM CPUs need ~238EB — see Report_Tieouts / DRAM_CPU_Link._


_Figure 9: Bottom Up TAM Difference (data labels as printed; legend says 'MM units' but values match the $B TAMs of Figs 4/10)_

| Series | 2025 | 2027E | 2030E | Note |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| UBS CPU TAM ($B; legend printed 'MM units') | 31 | 83 | 208 | equals Fig 10 bottom-up TAM |  |  |  |  |
| Demand CPU TAM ($B; legend printed 'MM units') | 31 | 125 | 548 | equals Fig 4 unconstrained TAM |  |  |  |  |

## p.8 — Figures 10-12: Updated ~$210B C2030 CPU TAM framework (p.8)

| Figure 10: Our Estimates Suggest a ~$210B TAM by C2030 |  |  |  |  |
|---|---|---|---|---|
| Estimate | 2025 | 2027E | 2030E | Comment |
| Traditional CPU Market |  |  |  |  |
|  Traditional CPU Market, MM | 20 | 26 | 30 | Grows from 2025 at 8% CAGR like C2005-2020 |
|  Traditional CPU ASP ($) | 1,200 | 1,348 | 1,606 | Grows from 2025 at 1.5x 4% CAGR like C2005-2020 (row printed 'ASP, K' but values are $) |
|  Traditional Market, $B | 24 | 35 | 48 | Implied by units and ASPs |
| AI CPU (Bottom-Up) |  |  |  |  |
|  AI Accelerator Units (Bottom-Up), MM | 9 | 29 | 44 | Largest programs (NVDA, AMD, TPU, Trn), ex-China |
|  AI CPU Market (Bottom-Up Ests), MM | 3 | 16 | 37 |  |
|   Head Node | 3 | 11 | 22 | UBSe based announced systems; printed '~22' |
|   Standalone | 0 | 5 | 15 | Additional CPU units outside of rack |
|  AI CPU ASP ($) | 2,430 | 3,058 | 4,378 | Higher core count and clock speed increasing ASPs |
|  AI CPU Market (Bottom-up Ests), $B | 7 | 48 | 160 |  |
| AI CPU (Top-Down) |  |  |  |  |
|  AI CPU Market (Top-Down Ests), MM |  |  | 80 | TAM based on 3-4T AI Spend, and 1-to-1 CPU/GPU attach |
|  AI CPU ASP ($) top-down |  |  | 3,000 | UBS ASP ests |
|  AI CPU Market, $B top-down |  |  | 240 | Implied by units and ASPs |
| Total Market |  |  |  |  |
|  Bottom-up Units, MM | 23 | 41 | 67 | Traditional CPU + AI CPU Bottom-up Ests |
|  Bottom-up TAM, $B | 31 | 83 | 208 |  |
|  Top-Down CPU Market, MM |  |  | 110 | Traditional CPU + AI CPU Top-Down Ests |
|  Top-Down CPU Market, $B |  |  | 288 |  |
| Figure 11: AI CPU Bottom-Up TAM Estimate |  |  |  |  |
| AI CPU Bottom-Up TAM Estimate | 2025 | 2027E | 2030E | Comment |
| Accelerators (NVDA, AMD, TPU, Trn) | 9 | 29 | 44 | Assumes units stay the same but TDP/performance increases |
|  Head Node CPUs, MM | 3 | 11 | 22 | UBSe based announced systems |
|   Head Node CPU per GPU attach rate | 0.29 | 0.36 | 0.5 |  |
|   Head Node ASP ($) | 2,430 | 3,160 | 4,480 | Higher ASP given higher portion of NVDA CPUs |
|  Standalone (outside of rack), MM | 0 | 5 | 15 | Additional CPU units outside of rack; printed '~15' |
|   Standalone CPU per GPU attach rate |  | 0.18 | 0.33 |  |
|   Standalone CPU ASP ($) |  | 2,850 | 4,223 | Assumes higher share of x86 even over time for multithread |
| AI CPU Market (Bottom-up Ests), MM | 3 | 16 | 37 |  |
| AI CPU ASP ($) | 2,430 | 3,058 | 4,378 | Higher core count and clock speed increasing ASPs |
| AI CPU Market (Bottom-up Ests), $B | 7 | 48 | 160 |  |
| CPU per GPU attach | 0.29 | 0.54 | 0.83 |  |

_Figure 12: CPU Market To Reach ~$210B By C2030E ($B; stacked bar — totals printed, segments = Fig 10/11 units x ASP)_

| Segment ($B) | 2025 | 2027E | 2030E | Basis |
|---|---|---|---|---|
| Traditional servers |  |  |  | Fig 10 traditional $B |
| AI Head Node |  |  |  | Fig 11 units x ASP |
| AI Standalone |  |  |  | Fig 11 units x ASP |
| Printed bar total | 31 | 83 | 208 |  |

_UBS text (p.8): ASP ~$4.4K (vs prior $3.8K/CPU); $4-5K/CPU possible in outer years if ASP/core holds and core counts double (vs $2-2.5K in C2025). AMD sizes the TAM at $220B, NVDA at $200B (no year)._


## p.11-12 — Figures 15-18: CPUs per GW and CPU power / compute capacity deployed (p.11-12)


_Figure 15: ~2.7MM traditional CPUs per GW, only ~1.4MM AI CPUs_

| CPUs per GW | Traditional CPU | AI CPU | Trad recomputed | AI recomputed | Note |
|---|---|---|---|---|---|
| CPU TDP (W) | 250 | 450 |  |  |  |
| Approx DRAM / CPU (TB) | 1 | 2 |  |  |  |
| DRAM/DIMM (W) | 15 | 15 |  |  |  |
| # of DIMMs populated | 8 | 16 |  |  |  |
| Total TDP per CPU (W) | 370 | 690 |  |  |  |
| # of CPUs per GW | 2,702,703 | 1,449,275 |  |  |  |
| CPU ASP ($) | 1,500 | 3,500 |  |  |  |
| CPU+DIMMs Capex per GW, $B | 17.6 | 34.1 |  |  | Text: CPU+memory capex/GW ~$34B (AI) vs ~$18B (traditional), memory the vast majority of the increase. |
| CPU Capex ($B/GW) | 4.1 | 5.1 |  |  |  |
| Memory Capex ($B/GW; printed '$12K/1TB') | 13.5 | 29 |  |  | Printed memory capex does NOT tie to the table's own 1TB x $12K/TB (recomputed cols: $32.4B / $34.8B). It ties EXACTLY at $10K/TB with traditional at 0.5TB (Fig 8's basis) and AI at 2TB: $5.0K / $20.0K of memory per CPU. |
| Memory price assumption ($ per TB, printed '$12K/1TB') | 12,000 | 12,000 |  |  |  |
| Figure 16: ~21GW of power required for new CPUs in C2030 |  |  |  |  |  |
| CPU Power, GW | 2025 | 2027E | 2030E | Note |  |
| Traditional CPUs, MM | 20 | 26 | 30 |  |  |
| W per CPU + DIMMs (trad) | 370 | 370 | 370 |  |  |
| Traditional Implied GW | 8 | 10 | 11 |  |  |
| AI Head node Implied GW |  |  |  | printed 'captured in GW racks' |  |
| AI Standalone CPUs, MM | 0 | 5 | 15 |  |  |
| W per CPU + DIMMs (AI) | 690 | 690 | 690 |  |  |
| AI Standalone Implied GW | 0 | 4 | 10 |  |  |
| Total CPUs, Implied GW | 8 | 13 | 21 |  |  |

_Figures 17-18: GW of annual compute / data-center capacity deployed (stacked bars; totals printed, CPU slice = Fig 16)_

| GW | 2025 | 2027E | 2030E | Note |  |
|---|---|---|---|---|---|
| Fig 17 annual compute capacity deployed (GPU+ASIC+CPU), GW | 19 | 62 | 126 | printed totals |  |
|   of which CPU (Fig 16), GW | 8 | 13 | 21 | Fig 16 total CPUs implied GW |  |
| Fig 18 annual DC capacity deployed at PUE 1.12, GW | 21 | 70 | 141 | printed totals |  |

_Capstone transcription note: GPU/ASIC split of Figs 17-18 is unlabeled in the chart (2030E roughly GPU ~60GW / ASIC ~45GW / CPU ~21GW by eye) — not tabulated. Text: CPU-driven infrastructure ~20% of 2030 annual compute capacity deployed; Fig 18 assumes PUE 1.12._


## p.13-14 — Figures 19-21: C2030E server-CPU revenue split and unit shares (p.13-14)

| Figure 19: UBSe Server CPU Market Breakdown C2030E |  |  |  |  |
|---|---|---|---|---|
| (Revenues $B) | C2030E | % (printed) | % (recomputed) |  |
| AMD Server | 62 | 0.3 |  |  |
| INTC Server | 44 | 0.21 |  |  |
| ARM Server | 102 | 0.49 |  |  |
|  of which ARM AGI | 15 | 0.07 |  |  |
|  of which NVDA | 53 | 0.25 |  |  |
|  of which Other | 35 | 0.17 |  |  |
| Total Server CPU | 208 | 1 |  |  |
| Figures 20-21: unit shares (pie labels) |  |  |  |  |
| Unit share | C2025 traditional CPU (Fig 20) | UBSe C2030 total CPU (Fig 21) | C2030 revenue share (Fig 19) | Implied C2030 ASP ($) = rev / (share x 67MM) |
| INTC | 0.6 | 0.28 |  |  |
| AMD | 0.24 | 0.34 |  |  |
| ARM | 0.16 | 0.38 |  |  |

_Capstone transcription note: Implied ASP column uses Fig 10's 67MM C2030 units: ARM-based revenue includes NVDA Grace/Vera and ARM AGI chips (full-chip $), not royalties. Text: AMD/INTC monetize ~$3-4K per CPU vs ARM IP economics ~$100+/CPU._


## p.16 — Figure 23: Server CPU Roadmap (p.16) — approximate timing read off the Gantt bars

| Vendor | Generation / platform | Microarchitecture | Product family | Process | Bar start (approx) | Bar end (approx) |
|---|---|---|---|---|---|---|
| AMD | 1st Gen | Zen | Naples | 14nm | 2017 | 2019 Q2 |
| AMD | 2nd Gen | Zen2 | General Purpose, Rome | 7nm, 14nm | 2019 Q3 | 2021 Q1 |
| AMD | 3rd Gen | Zen3, 3D V-Cache | General Purpose, Milan; Technical, Milan-X | 7nm | 2021 Q1 | 2022 Q3 |
| AMD | 4th Gen | Zen4/4C, 3D V-Cache | General Purpose, Genoa; Cloud Native - Bergamo; Technical - Genoa-X; Telco - Siena | 5nm | 2022 Q4 | 2024 Q3 |
| AMD | 5th Gen | Zen5/5c | Turin | TSMC 3nm | 2024 Q4 | 2026 Q2 |
| AMD | 6th Gen | Zen6/6c | Venice (26) and Verano (27) | TSMC 2nm | 2026 Q3 | 2028 Q2 |
| AMD | 7th Gen | Zen 7/7c | Florence | Next Gen Process Node | 2028 Q3 | 2029+ |
| INTC | 1st Gen (Purley) | - | Skylake-SP | 14nm+ | 2017 | 2019 Q1 |
| INTC | 1st Gen (Purley) | - | Cascade Lake-SP | 14nm++ | 2019 Q2 | 2020 Q1 |
| INTC | 2nd Gen (Purley) | - | Cooper Lake; Cascade Lake R | 14nm++ | 2020 | 2020 |
| INTC | 3rd Gen (Whitley) | - | Ice Lake-SP | 10nm+ | 2021 | 2022 |
| INTC | 4th Gen (Eagle Stream) | - | Sapphire Rapids & S.R. HBM | Intel 7 | 2023 Q1 | 2023 Q3 |
| INTC | 5th Gen (Eagle Stream) | - | Emerald Rapids | Intel 7 | 2023 Q4 | 2024 Q2 |
| INTC | 6th Gen (Birch Stream) | E-core | Sierra Forest | Intel 3 | 2024 Q3 | 2026 Q1 |
| INTC | 6th Gen (Birch Stream) | P-core | Granite Rapids | Intel 3 | 2024 Q3 | 2027 Q2 |
| INTC | 7th Gen (Birch Stream) | E-core | Clearwater Forest* | Intel 18A | 2026 Q2 | 2027 Q4 |
| INTC | 8th Gen (Oak Stream) | P-core | Diamond Rapids | Intel 18A-P | 2027 Q3 | 2028 Q3 |
| INTC | 9th Gen (TBA) | P-core | Coral Rapids | Intel 18A | 2028 Q1 | 2029+ |
| NVDA | 1st Gen | Neoverse V2, Armv9 | Grace | TSMC N4 | 2023 Q3 | 2026 Q2 |
| NVDA | Second Gen | Arm v9.2 | Vera | TSMC 3nm | 2026 Q3 | 2028 Q3 |
| NVDA | Third Gen | Arm | Rosa | TSMC 2nm | 2028 Q4 | 2029+ |
| ARM | 1st Gen | Armv9.2 | ARM AGI CPU | 3nm | 2026 Q4 | 2027 Q4 |
| ARM | 2nd Gen | TBA | TBA | TBA | 2028 | 2029+ |
| QCOM | 1st Gen (A) | Falkor | - | Samsung 10nm | 2018 | 2018 |
| QCOM | 1st Gen (B) | Oryon | Dragonfly C1000 | - | 2028 Q3 | 2029+ |
| AMZN | Gen 1 | Cortex-A72 | Graviton | 16nm | 2018 | 2019 |
| AMZN | Gen 2 | Neoverse N1 | Graviton2 | 7nm | 2020 | 2021 |
| AMZN | Gen 3 / 3E | Neoverse V1 | Graviton3/3E | 5nm | 2021 Q4 | 2023 Q3 |
| AMZN | Gen 4 | Neoverse V2 | Graviton4 | 5nm | 2023 Q4 | 2025 Q3 |
| AMZN | Gen 5 | Neoverse V3 | Graviton5 | 3nm | 2025 Q4 | 2027 Q3 |
| AMZN | Gen 6 | Neoverse V4 | Graviton6 | 2nm* | 2027 Q4 | 2029+ |
| MSFT | Gen 1 | Neoverse N2 / CSS N2 | Cobalt 100 | 5nm | 2023 | 2025 Q3 |
| MSFT | Gen 2 | Neoverse V3 / CSS V3 | Cobalt 200 | 3nm | 2025 Q4 | 2027 Q3 |
| MSFT | Gen 3 | Neoverse V4 / future CSS* | Cobalt 300 | 2nm* | 2027 Q4 | 2029+ |
| GOOG | Gen 1 | Neoverse V2 | Axion / C4A | 5nm | 2024 Q2 | 2025 Q3 |
| GOOG | Gen 2 | Neoverse N3 | Axion / N4A | 3nm | 2025 Q4 | 2027 Q3 |
| GOOG | Gen 3 | Neoverse V4/N4 | Axion Gen 3 | 2nm* | 2027 Q4 | 2029+ |

_Capstone transcription note: '*' as printed in the note (unconfirmed / expected). Start/end quarters are read from bar edges and are approximate (+/- 1 quarter)._


## p.17 — Figure 24: CPU Specs (p.17)

| Spec | AMD Venice | INTC Clearwater Forest | INTC Diamond Rapids | NVDA Vera | ARM AGI | AWS Graviton5 | MSFT Cobalt 200 | QCOM Dragonfly C1000 | Google Axion N4A |
|---|---|---|---|---|---|---|---|---|---|
| Process | TSMC N2 | Compute 18A; Base INTC 3; I/O INTC 7 | Cores 18A-P; Base INTC 3-T; Fabric hubs INTC 3 | - | TSMC N3P | TSMC 3nm | TSMC 3nm | - | TSMC 3nm |
| Package | 8 CCDs + 2 I/O dies | 12 compute + 3 bases + 2 I/O tiles | 16 core chiplets on 4 base tiles + 2 fabric hubs | Monolithic compute die + separate memory controller and I/O dies | 2 chiplets | 4 chiplets | 2 chiplets | Multi-chiplet | - |
| Base / nominal clock | 2.55 GHz (9996) | 2.2 GHz (6990E+, 450W) | - | - | 3.2 GHz (128/136C); 3.5 GHz (64C); 2.8 GHz typical | - | - | - | - |
| Max boost | 5.0 GHz (F-SKUs); 5.15 GHz (Venice-X) | 3.2 GHz (2.8 all-core) | - | - | 3.5 GHz (128/136C); 3.7 GHz (64C) | - | - | - | - |
| TDP | Up to 600W | 300-450W | Up to 650W | 250-450W | 300W | - | - | - | - |
| Core design | Zen 6 / Zen 6c | Darkmont E-core | Panther Cove | Custom Olympus | Neoverse V3 | Neoverse V3 | Neoverse V3 | Custom Oryon | Neoverse V3 |
| Max cores | 256 Zen 6c; 128 Gen 6 | 288 | 256 | 88 | 136 | 192 | 132 | 250+ | - |
| Max threads | 512 | 288 | - | 176 | - | - | - | - | - |
| Multithreading | SMT 2 threads/core | None | - | Spatial multithreading 2 threads/core | - | - | - | - | - |
| Core-count options | SP7: 64-256; SP8: 8-128 | 144 / 192 / 264 / 288 | - | Single 88-core SKU | 64 / 128 / 136 | - | - | - | - |
| Compute dies x core | 8 x 32 Zen 6c | 12 x 24 | 16 x up to 16 | 1 x 88 | 2 x 70 physical | 4 chiplets | 2 x 66 active | Multi-chiplet | - |
| Total LLC | 1,024 MB (9996, 4 MB/core); 1,152 MB Venice-X | 576 MB | Up to 1.28 GB | 164 MB | 128 MB system-level cache | 192 MB | 192 MB | - | - |
| Memory type | DDR5 RDIMM / MRDIMM | DDR5 RDIMM | DDR5 RDIMM / MRDIMM | LPDDR5X (SOCAMM2) | DDR5 RDIMM | 12-ch DDR5-8800 | DDR5 | - | DDR5 |
| Peak memory bandwidth | 1.6 TB/s | 768 GB/s | Up to 1.6 TB/s | 1.2 TB/s | ~845 GB(/s) at DDR5-8800; ~614 GB/s at 6400 | 845 GB/s | - | - | - |
| PCIe | 128 PCIe 6.0 lanes | 96 PCIe 5.0 lanes | 128 flexible lanes (PCIe 6.0 / CXL 3.0 / UPI 3) + 8 PCIe 4.0 | 88 PCIe Gen 6 lanes | 96 PCIe 6.0 lanes (768 GB/s each way) + 6 PCIe 4.0 lanes | PCIe Gen 6 | - | PCIe Gen 7 (>2 TB/s incl. CXL) | - |
| CXL | CXL 3.1 | 64 CXL 2.0 lanes | CXL 3.0 (on flexible lanes) | CXL 3.1 | CXL 3.0 Type 3 | - | - | - | - |
| Other links | - | 6 UPI 2.0 links | UPI 3 (on flexible lanes) | NVLink-C2C (1,800 GB/s) | 2 socket SMP; AMBA CHI extension links | - | - | - | - |

_Capstone transcription note: Memory capacity per CPU is NOT given in Fig 24 (only type/bandwidth). Vera capacity context lives on Cross_Check (1.5TB SOCAMM spec -> 768GB per JPM 24-Aug-26)._


## p.18 — Figure 25: Intel, AMD and ARM Server CPU Units (p.18) — DIGITIZED


_Chart values extracted from the PDF's vector geometry (charts are vector forms; axis fit residual <=0.003MM / <=0.04pp), cross-checked by a 600-dpi pixel measurement (max diff 0.01MM / 0.22pp); printed segment labels used where present (+/-0.5pp rounding) — see Fig28_31_Provenance. Not printed numbers._

| quarter | intel_mm | amd_mm | arm_mm | total_mm |
|---|---|---|---|---|
| 1Q19 | 6.724 | 0.197 | 0.036 | 6.957 |
| 2Q19 | 6.557 | 0.233 | 0.03 | 6.82 |
| 3Q19 | 7.771 | 0.347 | 0.042 | 8.16 |
| 4Q19 | 8.931 | 0.425 | 0.048 | 9.404 |
| 1Q20 | 8.507 | 0.461 | 0.054 | 9.022 |
| 2Q20 | 8.435 | 0.521 | 0.054 | 9.01 |
| 3Q20 | 8.082 | 0.574 | 0.06 | 8.716 |
| 4Q20 | 8.142 | 0.622 | 0.066 | 8.83 |
| 1Q21 | 7.406 | 0.724 | 0.054 | 8.184 |
| 2Q21 | 8.315 | 0.873 | 0.066 | 9.255 |
| 3Q21 | 8.77 | 0.999 | 0.072 | 9.841 |
| 4Q21 | 9.5 | 1.142 | 0.09 | 10.73 |
| 1Q22 | 9.201 | 1.215 | 0.083 | 10.5 |
| 2Q22 | 7.938 | 1.281 | 0.083 | 9.302 |
| 3Q22 | 6.718 | 1.43 | 0.078 | 8.226 |
| 4Q22 | 6.879 | 1.472 | 0.174 | 8.525 |
| 1Q23 | 5.109 | 1.119 | 0.21 | 6.437 |
| 2Q23 | 4.959 | 1.131 | 0.281 | 6.371 |
| 3Q23 | 4.008 | 1.214 | 0.329 | 5.551 |
| 4Q23 | 4.433 | 1.334 | 0.377 | 6.144 |
| 1Q24 | 4.05 | 1.25 | 0.353 | 5.653 |
| 2Q24 | 4.086 | 1.298 | 0.383 | 5.767 |
| 3Q24 | 4.349 | 1.394 | 0.425 | 6.168 |
| 4Q24 | 4.462 | 1.544 | 0.61 | 6.616 |
| 1Q25 | 4.612 | 1.729 | 0.826 | 7.167 |
| 2Q25 | 4.63 | 1.735 | 0.868 | 7.233 |
| 3Q25 | 4.582 | 1.759 | 1.101 | 7.442 |
| 4Q25 | 4.726 | 2.016 | 1.31 | 8.052 |
| 1Q26 | 4.666 | 2.328 | 1.448 | 8.441 |
| 2Q26 | 4.959 | 2.615 | 1.621 | 9.195 |

## p.18 — Figure 26: Server CPU Unit Share (p.18) — DIGITIZED


_Chart values extracted from the PDF's vector geometry (charts are vector forms; axis fit residual <=0.003MM / <=0.04pp), cross-checked by a 600-dpi pixel measurement (max diff 0.01MM / 0.22pp); printed segment labels used where present (+/-0.5pp rounding) — see Fig28_31_Provenance. Not printed numbers._

| quarter | intel_pct | amd_pct | arm_pct |
|---|---|---|---|
| 1Q19 | 96.65 | 2.85 | 0.5 |
| 2Q19 | 96.14 | 3.36 | 0.5 |
| 3Q19 | 95.19 | 4.31 | 0.5 |
| 4Q19 | 94.96 | 4.54 | 0.5 |
| 1Q20 | 94.32 | 5.09 | 0.59 |
| 2Q20 | 93.64 | 5.77 | 0.59 |
| 3Q20 | 92.73 | 6.59 | 0.68 |
| 4Q20 | 92.23 | 7.09 | 0.68 |
| 1Q21 | 90.46 | 8.86 | 0.68 |
| 2Q21 | 89.87 | 9.45 | 0.68 |
| 3Q21 | 89.14 | 10.09 | 0.77 |
| 4Q21 | 88.55 | 10.63 | 0.81 |
| 1Q22 | 87.64 | 11.54 | 0.81 |
| 2Q22 | 85.33 | 13.77 | 0.91 |
| 3Q22 | 81.69 | 17.31 | 1 |
| 4Q22 | 80.69 | 17.27 | 2.04 |
| 1Q23 | 79.33 | 17.4 | 3.27 |
| 2Q23 | 77.87 | 17.77 | 4.36 |
| 3Q23 | 72.15 | 21.9 | 5.95 |
| 4Q23 | 72.19 | 21.63 | 6.18 |
| 1Q24 | 71.65 | 22.09 | 6.27 |
| 2Q24 | 70.83 | 22.49 | 6.68 |
| 3Q24 | 70.51 | 22.49 | 7 |
| 4Q24 | 67.47 | 23.36 | 9.18 |
| 1Q25 | 64.42 | 24.08 | 11.49 |
| 2Q25 | 63.97 | 23.99 | 12.04 |
| 3Q25 | 61.56 | 23.63 | 14.81 |
| 4Q25 | 58.65 | 25.08 | 16.27 |
| 1Q26 | 55.29 | 27.54 | 17.18 |
| 2Q26 | 53.92 | 28.45 | 17.63 |

## p.18 — Figure 27: Intel vs AMD x86 Server CPU Revenue Share (p.18) — DIGITIZED


_Chart values extracted from the PDF's vector geometry (charts are vector forms; axis fit residual <=0.003MM / <=0.04pp), cross-checked by a 600-dpi pixel measurement (max diff 0.01MM / 0.22pp); printed segment labels used where present (+/-0.5pp rounding) — see Fig28_31_Provenance. Not printed numbers._

| quarter | point_index | intel_pct | amd_pct | sum_pct |
|---|---|---|---|---|
| 1Q08 | 0 | 90.98 | 9.02 | 100 |
| 2Q08 | 1 | 91.02 | 8.98 | 100 |
| 3Q08 | 2 | 89 | 11 | 100 |
| 4Q08 | 3 | 89.13 | 10.87 | 100 |
| 1Q09 | 4 | 88.95 | 11.05 | 100 |
| 2Q09 | 5 | 91.2 | 8.8 | 100 |
| 3Q09 | 6 | 91.79 | 8.21 | 100 |
| 4Q09 | 7 | 92.51 | 7.49 | 100 |
| 1Q10 | 8 | 92.01 | 7.99 | 100 |
| 2Q10 | 9 | 93.14 | 6.86 | 100 |
| 3Q10 | 10 | 93.36 | 6.64 | 100 |
| 4Q10 | 11 | 94.44 | 5.56 | 100 |
| 1Q11 | 12 | 95.25 | 4.75 | 100 |
| 2Q11 | 13 | 96.47 | 3.53 | 100 |
| 3Q11 | 14 | 95.66 | 4.34 | 100 |
| 4Q11 | 15 | 95.25 | 4.75 | 100 |
| 1Q12 | 16 | 95.34 | 4.66 | 100 |
| 2Q12 | 17 | 96.56 | 3.44 | 100 |
| 3Q12 | 18 | 97.32 | 2.68 | 100 |
| 4Q12 | 19 | 97.41 | 2.59 | 100 |
| 1Q13 | 20 | 97.28 | 2.72 | 100 |
| 2Q13 | 21 | 97.01 | 2.99 | 100 |
| 3Q13 | 22 | 97.5 | 2.5 | 100 |
| 4Q13 | 23 | 98.04 | 1.96 | 100 |
| 1Q14 | 24 | 98.45 | 1.55 | 100 |
| 2Q14 | 25 | 98.81 | 1.19 | 100 |
| 3Q14 | 26 | 99.12 | 0.88 | 100 |
| 4Q14 | 27 | 99.35 | 0.65 | 100 |
| 1Q15 | 28 | 99.48 | 0.52 | 100 |
| 2Q15 | 29 | 99.62 | 0.38 | 100 |
| 3Q15 | 30 | 99.8 | 0.2 | 100 |
| 4Q15 | 31 | 99.8 | 0.2 | 100 |
| 1Q16 | 32 | 99.89 | 0.11 | 100 |
| 2Q16 | 33 | 99.89 | 0.11 | 100 |
| 3Q16 | 34 | 99.89 | 0.11 | 100 |
| 4Q16 | 35 | 99.9 | 0.11 | 100 |
| 1Q17 | 36 | 99.89 | 0.11 | 100 |
| 2Q17 | 37 | 99.8 | 0.2 | 100 |
| 3Q17 | 38 | 99.75 | 0.25 | 100 |
| 4Q17 | 39 | 99.66 | 0.34 | 100 |
| 1Q18 | 40 | 98.76 | 1.24 | 100 |
| 2Q18 | 41 | 98.36 | 1.64 | 100 |
| 3Q18 | 42 | 97.86 | 2.14 | 100 |
| 4Q18 | 43 | 97.32 | 2.68 | 100 |
| 1Q19 | 44 | 97.41 | 2.59 | 100 |
| 2Q19 | 45 | 97.05 | 2.95 | 100 |
| 3Q19 | 46 | 96.47 | 3.53 | 100 |
| 4Q19 | 47 | 95.88 | 4.12 | 100 |
| 1Q20 | 48 | 96.2 | 3.8 | 100 |
| 2Q20 | 49 | 94.4 | 5.6 | 100 |
| 3Q20 | 50 | 92.33 | 7.67 | 100 |
| 4Q20 | 51 | 91.38 | 8.62 | 100 |
| 1Q21 | 52 | 89.18 | 10.82 | 100 |
| 2Q21 | 53 | 88.41 | 11.59 | 100 |
| 3Q21 | 54 | 85.67 | 14.33 | 100 |
| 4Q21 | 55 | 85.62 | 14.38 | 100 |
| 1Q22 | 56 | 82.38 | 17.62 | 100 |
| 2Q22 | 57 | 76.76 | 23.24 | 100 |
| 3Q22 | 58 | 72.3 | 27.7 | 100 |
| 4Q22 | 59 | 72.17 | 27.83 | 100 |
| 1Q23 | 60 | 72.21 | 27.79 | 100 |
| 2Q23 | 61 | 72.94 | 27.06 | 100 |
| 3Q23 | 62 | 68.79 | 31.21 | 100 |
| 4Q23 | 63 | 68.21 | 31.79 | 100 |
| 1Q24 | 64 | 67.04 | 32.96 | 100 |
| 2Q24 | 65 | 66.19 | 33.81 | 100 |
| 3Q24 | 66 | 66.19 | 33.81 | 100 |
| 4Q24 | 67 | 63.62 | 36.38 | 100 |
| 1Q25 | 68 | 60.52 | 39.48 | 100 |
| 2Q25 | 69 | 58.81 | 41.19 | 100 |
| 3Q25 | 70 | 60.56 | 39.44 | 100 |
| 4Q25 | 71 | 58.67 | 41.33 | 100 |
| 1Q26 | 72 | 53.77 | 46.24 | 100 |
| 2Q26 | 73 | 55.43 | 44.57 | 100 |

## p.18 — Figure 28: INTC Server Units Decomposition (p.18)


_Chart values extracted from the PDF's vector geometry (charts are vector forms; axis fit residual <=0.003MM / <=0.04pp), cross-checked by a 600-dpi pixel measurement (max diff 0.01MM / 0.22pp); printed segment labels used where present (+/-0.5pp rounding) — see Fig28_31_Provenance. Not printed numbers._

| quarter | granite_rapids_pct | sierra_forest_pct | emerald_rapids_pct | sapphire_rapids_pct | ice_lake_pct | cascade_lake_pct | others_pct | unplotted_residual_pct | row_sum_pct |
|---|---|---|---|---|---|---|---|---|---|
| 1Q21 | 0 | 0 | 0 | 0 | 2 | 76 | 22 | 0 | 100 |
| 2Q21 | 0 | 0 | 0 | 0 | 7 | 75 | 18 | 0 | 100 |
| 3Q21 | 0 | 0 | 0 | 0 | 12 | 72 | 17 | 0 | 101 |
| 4Q21 | 0 | 0 | 0 | 0 | 18 | 70 | 13 | 0 | 101 |
| 1Q22 | 0 | 0 | 0 | 0.1 | 28 | 63 | 9 | 0 | 100 |
| 2Q22 | 0 | 0 | 0 | 1 | 33 | 58 | 8 | 0 | 100 |
| 3Q22 | 0 | 0 | 0 | 1 | 37 | 55 | 7 | 0 | 100 |
| 4Q22 | 0 | 0 | 0 | 2.5 | 42 | 50 | 6 | 0 | 100 |
| 1Q23 | 0 | 0 | 0 | 5 | 45 | 45 | 5 | 0 | 100 |
| 2Q23 | 0 | 0 | 0 | 13 | 45 | 40 | 3 | 0 | 101 |
| 3Q23 | 0 | 0 | 1 | 27 | 39 | 33 | 0 | 0 | 100 |
| 4Q23 | 0 | 0 | 4 | 41 | 31 | 24 | 0 | 0 | 100 |
| 1Q24 | 0 | 0.5 | 10 | 36 | 41 | 12 | 0 | 0 | 99.5 |
| 2Q24 | 0 | 2.5 | 12 | 42 | 38 | 5 | 0 | 0 | 99.5 |
| 3Q24 | 0.5 | 4 | 13 | 47 | 34 | 2 | 0 | 0 | 100 |
| 4Q24 | 1.5 | 6 | 19 | 49 | 25 | 0 | 0 | 0 | 100 |
| 1Q25 | 3.6 | 6 | 22 | 45 | 23 | 0 | 0 | 0 | 99.6 |
| 2Q25 | 10 | 10 | 26 | 35 | 19 | 0 | 0 | 0 | 100 |
| 3Q25 | 16 | 12 | 31 | 32 | 10 | 0 | 0 | 0 | 101 |
| 4Q25 | 18 | 12 | 35 | 27 | 8 | 0 | 0 | 0 | 100 |
| 1Q26 | 24 | 13 | 38 | 18 | 6 | 0 | 0.5 | 0 | 99.5 |
| 2Q26 | 26 | 12 | 42 | 12 | 3 | 0 | 2.4 | 2.6 | 100 |

## p.18 — Figure 29: AMD Server Units Decomposition (p.18)


_Chart values extracted from the PDF's vector geometry (charts are vector forms; axis fit residual <=0.003MM / <=0.04pp), cross-checked by a 600-dpi pixel measurement (max diff 0.01MM / 0.22pp); printed segment labels used where present (+/-0.5pp rounding) — see Fig28_31_Provenance. Not printed numbers._

| quarter | venice_pct | turin_pct | bergamo_pct | siena_pct | genoa_pct | milan_pct | others_pct | unplotted_residual_pct | row_sum_pct |
|---|---|---|---|---|---|---|---|---|---|
| 1Q21 | 0 | 0 | 0 | 0 | 0 | 14 | 14 | 72 | 100 |
| 2Q21 | 0 | 0 | 0 | 0 | 0 | 26 | 11 | 63 | 100 |
| 3Q21 | 0 | 0 | 0 | 0 | 0 | 47 | 8 | 45 | 100 |
| 4Q21 | 0 | 0 | 0 | 0 | 0 | 54 | 8 | 38 | 100 |
| 1Q22 | 0 | 0 | 0 | 0 | 0.1 | 62 | 7 | 30.9 | 100 |
| 2Q22 | 0 | 0 | 0 | 0 | 0.1 | 67 | 6 | 26.9 | 100 |
| 3Q22 | 0 | 0 | 0 | 0 | 1.9 | 75 | 6 | 17.1 | 100 |
| 4Q22 | 0 | 0 | 0 | 0 | 6 | 75 | 5 | 14 | 100 |
| 1Q23 | 0 | 0 | 0.1 | 0 | 12 | 73 | 5 | 9.9 | 100 |
| 2Q23 | 0 | 0 | 2 | 0.2 | 19 | 67 | 4 | 7.8 | 100 |
| 3Q23 | 0 | 0 | 23 | 0.5 | 29 | 38 | 4 | 5.5 | 100 |
| 4Q23 | 0 | 0 | 22 | 1 | 47 | 21 | 3 | 6 | 100 |
| 1Q24 | 0 | 0 | 22 | 2 | 50 | 18 | 4 | 4 | 100 |
| 2Q24 | 0 | 0.1 | 20 | 1.9 | 56 | 17 | 2.3 | 2.7 | 100 |
| 3Q24 | 0 | 1.9 | 20 | 1.9 | 58 | 14 | 1.6 | 2.6 | 100 |
| 4Q24 | 0 | 6 | 20 | 1.9 | 60 | 8 | 1.5 | 2.6 | 100 |
| 1Q25 | 0 | 13 | 30 | 1.9 | 45 | 6 | 1.4 | 2.7 | 100 |
| 2Q25 | 0 | 25 | 24 | 2 | 40 | 6 | 1.4 | 1.7 | 100 |
| 3Q25 | 0.1 | 34 | 20 | 2 | 35 | 6 | 1.4 | 1.5 | 100 |
| 4Q25 | 0.1 | 38 | 14 | 2 | 37 | 5 | 1.3 | 2.6 | 100 |
| 1Q26 | 2 | 41 | 9 | 1.8 | 39 | 4 | 1.3 | 2 | 100 |
| 2Q26 | 6 | 45 | 9 | 1.6 | 33 | 3 | 1.2 | 1.1 | 99.9 |

## p.19 — Figure 30: INTC Server Units by Node (p.19)


_Chart values extracted from the PDF's vector geometry (charts are vector forms; axis fit residual <=0.003MM / <=0.04pp), cross-checked by a 600-dpi pixel measurement (max diff 0.01MM / 0.22pp); printed segment labels used where present (+/-0.5pp rounding) — see Fig28_31_Provenance. Not printed numbers._

| quarter | intel_14_pct | intel_10_pct | intel_7_pct | intel_3_pct | unknown_other_pct | unplotted_residual_pct | row_sum_pct |
|---|---|---|---|---|---|---|---|
| 1Q21 | 76 | 2 | 0 | 0 | 22 | 0 | 100 |
| 2Q21 | 75 | 7 | 0 | 0 | 18 | 0 | 100 |
| 3Q21 | 72 | 12 | 0 | 0 | 17 | 0 | 101 |
| 4Q21 | 70 | 18 | 0 | 0 | 13 | 0 | 101 |
| 1Q22 | 63 | 28 | 0.1 | 0 | 9 | 0 | 100 |
| 2Q22 | 58 | 33 | 1 | 0 | 8 | 0 | 100 |
| 3Q22 | 55 | 37 | 1 | 0 | 7 | 0 | 100 |
| 4Q22 | 50 | 42 | 3 | 0 | 6 | 0 | 101 |
| 1Q23 | 45 | 45 | 5 | 0 | 5 | 0 | 100 |
| 2Q23 | 40 | 45 | 13 | 0 | 3 | 0 | 101 |
| 3Q23 | 33 | 39 | 28 | 0 | 0 | 0 | 100 |
| 4Q23 | 24 | 31 | 45 | 0 | 0 | 0 | 100 |
| 1Q24 | 12 | 41 | 46 | 0.5 | 0 | 0 | 99.5 |
| 2Q24 | 5 | 38 | 54 | 3 | 0 | 0 | 100 |
| 3Q24 | 2 | 34 | 60 | 5 | 0 | 0 | 101 |
| 4Q24 | 0 | 25 | 68 | 8 | 0 | 0 | 101 |
| 1Q25 | 0 | 23 | 67 | 10 | 0 | 0 | 100 |
| 2Q25 | 0 | 19 | 61 | 20 | 0 | 0 | 100 |
| 3Q25 | 0 | 10 | 63 | 28 | 0 | 0 | 101 |
| 4Q25 | 0 | 8 | 62 | 30 | 0 | 0 | 100 |
| 1Q26 | 0 | 6 | 56 | 37 | 0.5 | 0 | 99.5 |
| 2Q26 | 0 | 3 | 54 | 41 | 2 | 0 | 100 |

## p.19 — Figure 31: AMD Server Units by Node (p.19)


_Chart values extracted from the PDF's vector geometry (charts are vector forms; axis fit residual <=0.003MM / <=0.04pp), cross-checked by a 600-dpi pixel measurement (max diff 0.01MM / 0.22pp); printed segment labels used where present (+/-0.5pp rounding) — see Fig28_31_Provenance. Not printed numbers._

| quarter | 7nm_pct | 5nm_pct | 3_4nm_pct | 2nm_pct | unknown_other_pct | unplotted_residual_pct | row_sum_pct |
|---|---|---|---|---|---|---|---|
| 1Q21 | 86 | 0 | 0 | 0 | 14 | 0 | 100 |
| 2Q21 | 89 | 0 | 0 | 0 | 11 | 0 | 100 |
| 3Q21 | 92 | 0 | 0 | 0 | 8 | 0 | 100 |
| 4Q21 | 92 | 0 | 0 | 0 | 8 | 0 | 100 |
| 1Q22 | 93 | 0.1 | 0 | 0 | 7 | 0 | 100 |
| 2Q22 | 94 | 0.1 | 0 | 0 | 6 | 0 | 100 |
| 3Q22 | 92 | 2 | 0 | 0 | 6 | 0 | 100 |
| 4Q22 | 89 | 6 | 0 | 0 | 5 | 0 | 100 |
| 1Q23 | 83 | 12 | 0 | 0 | 5 | 0 | 100 |
| 2Q23 | 75 | 21 | 0 | 0 | 4 | 0 | 100 |
| 3Q23 | 44 | 52 | 0 | 0 | 4 | 0 | 100 |
| 4Q23 | 26 | 70 | 0 | 0 | 3 | 0 | 99 |
| 1Q24 | 22 | 74 | 0 | 0 | 4 | 0 | 100 |
| 2Q24 | 20 | 78 | 0.1 | 0 | 2 | 0 | 100 |
| 3Q24 | 17 | 80 | 2 | 0 | 1.6 | 0 | 101 |
| 4Q24 | 11 | 82 | 6 | 0 | 1.5 | 0 | 100 |
| 1Q25 | 8 | 77 | 13 | 0 | 1.4 | 0 | 99.4 |
| 2Q25 | 8 | 66 | 25 | 0 | 1.4 | 0 | 100 |
| 3Q25 | 8 | 57 | 34 | 0 | 1.4 | 0 | 100 |
| 4Q25 | 7 | 53 | 38 | 0 | 1.3 | 0 | 99.3 |
| 1Q26 | 6 | 50 | 41 | 2 | 1.3 | 0 | 100 |
| 2Q26 | 5 | 43 | 45 | 6 | 1.3 | 0 | 100 |

## p.21 — Figure 32: AMD - Summary Model (p.21)


_Transcribed from the image table as printed (UBS estimates; Company data, FactSet). Percentages stored as fractions._

| Advanced Micro Devices (AMD) - Key Metrics (in $MM except EPS and Units) | C2023A | C2024A | C2025A | CQ1A | CQ2A | CQ3E | CQ4E | C2026E | CQ1E | CQ2E | CQ3E | CQ4E | C2027E | CQ1E | CQ2E | CQ3E | CQ4E | C2028E | C2029E | C2030E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   Revenue | 22,680 | 25,785 | 34,639 | 10,253 | 11,536 | 13,180 | 17,122 | 52,092 | 19,063 | 20,930 | 25,508 | 32,421 | 97,922 | 32,538 | 33,841 | 35,995 | 37,618 | 139,993 | 176,924 | 221,588 |
|     Y/Y Growth | -0.04 | 0.14 | 0.34 | 0.38 | 0.5 | 0.43 | 0.67 | 0.5 | 0.86 | 0.81 | 0.94 | 0.89 | 0.88 | 0.71 | 0.62 | 0.41 | 0.16 | 0.43 | 0.26 | 0.25 |
|   Gross Profit (Non-GAAP) | 11,436 | 13,759 | 18,165 | 5,685 | 6,488 | 7,386 | 9,476 | 29,035 | 10,492 | 11,499 | 14,066 | 17,958 | 54,016 | 18,105 | 18,897 | 20,208 | 21,213 | 78,424 | 101,143 | 129,261 |
|   Gross Margin | 0.504 | 0.534 | 0.524 | 0.554 | 0.562 | 0.56 | 0.553 | 0.557 | 0.55 | 0.549 | 0.551 | 0.554 | 0.552 | 0.556 | 0.558 | 0.561 | 0.564 | 0.56 | 0.572 | 0.583 |
|     Ex-Semi-Custom GM (UBSe) | 0.57 | 0.55 | 0.54 | 0.56 | 0.57 | 0.57 | 0.56 | 0.56 | 0.55 | 0.55 | 0.55 | 0.56 | 0.55 | 0.56 | 0.56 | 0.57 | 0.57 | 0.56 | 0.58 | 0.59 |
|   R&D (GAAP) | 5,872 | 6,456 | 8,091 | 2,397 | 2,528 | 2,638 | 2,818 | 10,381 | 3,118 | 3,368 | 3,608 | 3,848 | 13,942 | 3,968 | 4,038 | 4,108 | 4,178 | 16,292 | 17,712 | 19,512 |
|   SG&A (GAAP) | 2,352 | 2,783 | 4,144 | 1,253 | 1,401 | 1,491 | 1,591 | 5,736 | 1,661 | 1,731 | 1,781 | 1,831 | 7,004 | 1,806 | 1,856 | 1,931 | 2,001 | 7,594 | 8,184 | 8,754 |
|   Other & Non-GAAP Adjustment (GAAP) | 1,835 | 1,586 | 1,223 | 290 | 284 | 284 | 284 | 1,142 | 284 | 284 | 284 | 284 | 1,136 | 284 | 284 | 284 | 284 | 1,136 | 1,136 | 1,136 |
|     Total Opex (Non-GAAP) | 6,616 | 7,669 | 10,397 | 3,145 | 3,394 | 3,634 | 3,914 | 14,087 | 4,284 | 4,604 | 4,894 | 5,184 | 18,966 | 5,279 | 5,399 | 5,544 | 5,684 | 21,906 | 23,916 | 26,286 |
|       Y/Y Growth | 0.1 | 0.16 | 0.36 | 0.42 | 0.4 | 0.32 | 0.3 | 0.35 | 0.36 | 0.36 | 0.35 | 0.32 | 0.35 | 0.23 | 0.17 | 0.13 | 0.1 | 0.16 | 0.09 | 0.1 |
|   Operating Income (Non-GAAP) | 4,854 | 6,138 | 7,768 | 2,540 | 3,094 | 3,752 | 5,562 | 14,948 | 6,208 | 6,895 | 9,172 | 12,774 | 35,050 | 12,826 | 13,498 | 14,664 | 15,529 | 56,518 | 77,227 | 102,975 |
|   Operating Margin | 0.214 | 0.238 | 0.224 | 0.248 | 0.268 | 0.285 | 0.325 | 0.287 | 0.326 | 0.329 | 0.36 | 0.394 | 0.358 | 0.394 | 0.399 | 0.407 | 0.413 | 0.404 | 0.436 | 0.465 |
|   Non-GAAP EPS | 2.65 | 3.31 | 4.17 | 1.37 | 1.66 | 2 | 2.87 | 7.91 | 3.17 | 3.5 | 4.59 | 6.23 | 17.58 | 6.19 | 6.46 | 6.97 | 7.3 | 26.94 | 35.57 | 45.18 |
| Free Cash Flow |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| CFFO | 1,667 | 3,041 | 7,709 | 2,955 | 2,366 | 4,145 | 4,329 | 13,796 | 5,815 | 6,149 | 7,185 | 9,622 | 28,771 | 12,585 | 12,292 | 13,057 | 13,979 | 51,913 | 68,439 | 91,002 |
| Capex | 546 | 636 | 974 | 389 | 808 | 958 | 1,158 | 3,313 | 900 | 900 | 900 | 900 | 3,600 | 900 | 900 | 900 | 900 | 3,600 | 3,600 | 3,600 |
|   FCF | 1,121 | 2,405 | 6,735 | 2,566 | 1,558 | 3,187 | 3,171 | 10,483 | 4,915 | 5,249 | 6,285 | 8,722 | 25,171 | 11,685 | 11,392 | 12,157 | 13,079 | 48,313 | 64,839 | 87,402 |
|     % revenue | 0.05 | 0.09 | 0.19 | 0.25 | 0.14 | 0.24 | 0.19 | 0.2 | 0.26 | 0.25 | 0.25 | 0.27 | 0.26 | 0.36 | 0.34 | 0.34 | 0.35 | 0.35 | 0.37 | 0.39 |
| Segment Revenues |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|   Data Center | 6,496 | 12,579 | 16,635 | 5,775 | 6,718 | 8,394 | 12,467 | 33,355 | 14,419 | 16,400 | 20,747 | 27,432 | 78,999 | 27,556 | 28,897 | 30,359 | 31,716 | 118,528 | 153,270 | 196,924 |
|     Data Center GPU Revenue | 555 | 5,025 | 6,754 | 2,430 | 2,750 | 3,550 | 6,400 | 15,130 | 7,600 | 8,500 | 11,250 | 15,900 | 43,250 | 15,900 | 17,000 | 18,100 | 19,200 | 70,200 | 97,800 | 131,400 |
|     Server CPU Revenue | 5,433 | 6,794 | 8,827 | 3,065 | 3,684 | 4,539 | 5,705 | 16,993 | 6,457 | 7,537 | 9,133 | 11,167 | 34,295 | 11,261 | 11,468 | 11,793 | 12,010 | 46,531 | 52,961 | 61,987 |
|       Server ASP ($) | 1,140 | 1,351 | 1,347 | 1,535 | 1,591 | 1,647 | 1,725 | 1,638 | 1,775 | 1,850 | 1,975 | 2,100 | 1,943 | 2,107 | 2,114 | 2,121 | 2,128 | 2,118 | 2,254 | 2,420 |
|       Server Units (K) | 4,768 | 5,028 | 6,554 | 1,997 | 2,316 | 2,756 | 3,307 | 10,375 | 3,638 | 4,074 | 4,624 | 5,318 | 17,654 | 5,344 | 5,425 | 5,560 | 5,644 | 21,973 | 23,493 | 25,616 |
|         Server TAM (K units) | 23,307 | 22,432 | 26,046 | 6,506 | 6,640 | 6,727 | 6,939 | 26,812 | 6,683 | 6,823 | 6,913 | 7,126 | 27,545 |  |  |  |  |  |  |  |
|         AMD Share | 0.2 | 0.22 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|     XLNX FPGAs | 252 | 318 | 385 | 89 | 93 | 98 | 102 | 382 | 97 | 92 | 88 | 83 | 361 | 86 | 88 | 91 | 94 | 359 | 405 | 455 |
|     Pensando | 254 | 441 | 669 | 191 | 191 | 208 | 260 | 850 | 265 | 271 | 276 | 282 | 1,094 | 310 | 341 | 375 | 412 | 1,437 | 2,104 | 3,081 |
|     Data Center Operating Margin | 0.2 | 0.28 | 0.22 | 0.28 | 0.31 | 0.31 | 0.35 | 0.32 | 0.36 | 0.36 | 0.36 | 0.36 | 0.36 | 0.37 | 0.37 | 0.37 | 0.37 | 0.37 | 0.38 | 0.38 |
|     Data Center Operating Profit Y/Y Drop-through |  |  |  | 0.32 | 0.65 | 0.38 | 0.37 |  | 0.42 | 0.39 | 0.39 | 0.37 |  | 0.38 | 0.38 | 0.39 | 0.43 |  |  |  |
|   Client | 4,651 | 7,054 | 10,640 | 2,885 | 3,062 | 2,997 | 2,957 | 11,901 | 2,900 | 2,847 | 2,987 | 3,147 | 11,881 | 2,943 | 2,969 | 3,466 | 3,605 | 12,983 | 14,080 | 14,290 |
|     PC Revenue | 4,386 | 6,718 | 10,154 | 2,751 | 2,914 | 2,952 | 2,938 | 11,555 | 2,876 | 2,822 | 2,947 | 3,130 | 11,775 | 2,921 | 2,947 | 3,431 | 3,589 | 12,888 | 13,995 | 14,205 |
|       Desktop Revenue | 1,386 | 1,863 | 3,196 | 798 | 829 | 862 | 827 | 3,317 | 820 | 807 | 851 | 909 | 3,387 | 889 | 884 | 1,038 | 1,101 | 3,912 | 4,389 | 4,617 |
|       AMD DT ASP ($) | 174 | 188 | 266 | 270 | 275 | 275 | 272 | 273 | 278 | 282 | 286 | 288 | 284 | 286 | 286 | 311 | 311 | 299 | 309 | 307 |
|       AMD DT Units (K) | 7,950 | 9,931 | 12,029 | 2,956 | 3,015 | 3,135 | 3,041 | 12,147 | 2,950 | 2,862 | 2,976 | 3,155 | 11,942 | 3,107 | 3,092 | 3,339 | 3,539 | 13,078 | 14,202 | 15,038 |
|         DT TAM (K units) | 67,010 | 69,021 | 75,737 | 17,683 | 17,652 | 19,987 | 21,236 | 76,558 | 17,685 | 17,667 | 20,019 | 21,277 | 76,647 | 18,215 | 18,197 | 20,619 | 21,915 | 78,947 | 81,315 | 83,754 |
|         AMD Share | 0.12 | 0.14 | 0.16 | 0.17 | 0.17 | 0.16 | 0.14 | 0.16 | 0.17 | 0.16 | 0.15 | 0.15 | 0.16 | 0.17 | 0.17 | 0.16 | 0.16 | 0.17 | 0.17 | 0.18 |
|       Mobile Revenue | 3,001 | 4,854 | 6,958 | 1,953 | 2,085 | 2,090 | 2,111 | 8,239 | 2,056 | 2,015 | 2,096 | 2,221 | 8,388 | 2,032 | 2,062 | 2,393 | 2,488 | 8,975 | 9,606 | 9,588 |
|       AMD Mobile ASP ($) | 98 | 115 | 157 | 173 | 173 | 170 | 170 | 172 | 180 | 180 | 180 | 180 | 180 | 178 | 178 | 193 | 193 | 186 | 193 | 193 |
|       AMD Mobile Units (K) | 30,609 | 42,212 | 44,314 | 11,264 | 12,052 | 12,293 | 12,416 | 48,026 | 11,423 | 11,195 | 11,642 | 12,341 | 46,601 | 11,415 | 11,587 | 12,398 | 12,893 | 48,293 | 49,774 | 49,681 |
|         Mobile TAM (K units) | 160,289 | 186,556 | 180,960 | 41,006 | 42,182 | 43,053 | 43,653 | 169,894 | 41,751 | 42,715 | 43,538 | 43,951 | 171,955 | 43,004 | 43,996 | 44,844 | 45,270 | 177,114 | 182,427 | 187,900 |
|         AMD Share | 0.19 | 0.23 | 0.24 | 0.27 | 0.29 | 0.29 | 0.28 | 0.28 | 0.27 | 0.26 | 0.27 | 0.28 | 0.27 | 0.27 | 0.26 | 0.28 | 0.28 | 0.27 | 0.27 | 0.26 |
|       AMD Pro Graphics Revenue | 267 | 335 | 486 | 134 | 148 | 45 | 19 | 346 | 24 | 25 | 40 | 17 | 106 | 23 | 22 | 35 | 15 | 95 | 85 | 85 |
|     Client Operating Margin | -0.01 | 0.13 | 0.23 | 0.16 | 0.15 | 0.19 | 0.2 | 0.18 | 0.18 | 0.19 | 0.2 | 0.21 | 0.2 | 0.19 | 0.19 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 |
|     Client Operating Profit Y/Y Drop-through |  |  |  | 0.03 | -0.3 | -0.57 | 0.05 |  | 3.51 | -0.35 | -2.79 | 0.37 |  | 0.86 | 0.19 | 0.2 | 0.13 |  |  |  |
|   Gaming | 6,212 | 2,595 | 3,910 | 720 | 779 | 640 | 514 | 2,653 | 583 | 511 | 568 | 623 | 2,285 | 795 | 720 | 839 | 927 | 3,281 | 3,725 | 3,795 |
|     PC GPU Gaming Revenue | 858 | 707 | 1,618 | 440 | 388 | 369 | 313 | 1,510 | 282 | 310 | 217 | 272 | 1,081 | 244 | 269 | 188 | 226 | 927 | 771 | 641 |
|     Semi-Custom Revenue | 5,354 | 1,888 | 2,292 | 280 | 391 | 271 | 201 | 1,143 | 301 | 201 | 351 | 351 | 1,204 | 551 | 451 | 651 | 701 | 2,354 | 2,954 | 3,154 |
|     Gaming Operating Margin | 0.16 | 0.11 | 0.12 | 0.11 | 0.15 | 0.15 | 0.17 | 0.14 | 0.16 | 0.15 | 0.14 | 0.15 | 0.15 | 0.16 | 0.14 | 0.13 | 0.14 | 0.14 | 0.16 | 0.16 |
|   Embedded | 5,321 | 3,557 | 3,454 | 873 | 977 | 1,149 | 1,184 | 4,183 | 1,160 | 1,172 | 1,207 | 1,219 | 4,757 | 1,243 | 1,256 | 1,331 | 1,371 | 5,200 | 5,849 | 6,579 |
|     Embedded Operating Margin | 0.49 | 0.4 | 0.36 | 0.39 | 0.4 | 0.42 | 0.44 | 0.41 | 0.35 | 0.32 | 0.85 | 1.76 | 0.83 | 1.56 | 1.71 | 1.98 | 2.15 | 1.86 | 2.67 | 3.75 |
| Q/Q Revenue Growth |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|   Data Center |  |  |  | 0.07 | 0.16 | 0.25 | 0.49 |  | 0.16 | 0.14 | 0.27 | 0.32 |  | 0 | 0.05 | 0.05 | 0.04 |  |  |  |
|   Client |  |  |  | -0.07 | 0.06 | -0.02 | -0.01 |  | -0.02 | -0.02 | 0.05 | 0.05 |  | -0.06 | 0.01 | 0.17 | 0.04 |  |  |  |
|   Gaming |  |  |  | -0.15 | 0.08 | -0.18 | -0.2 |  | 0.13 | -0.12 | 0.11 | 0.1 |  | 0.28 | -0.09 | 0.17 | 0.1 |  |  |  |
|   Embedded |  |  |  | -0.08 | 0.12 | 0.18 | 0.03 |  | -0.02 | 0.01 | 0.03 | 0.01 |  | 0.02 | 0.01 | 0.06 | 0.03 |  |  |  |
| Y/Y Revenue Growth |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|   Data Center |  | 0.94 | 0.32 | 0.57 | 1.07 | 0.93 | 1.32 | 1.01 | 1.5 | 1.44 | 1.47 | 1.2 | 1.37 | 0.91 | 0.76 | 0.46 | 0.16 | 0.5 | 0.29 | 0.28 |
|   Client |  | 0.52 | 0.51 | 0.26 | 0.23 | 0.09 | -0.05 | 0.12 | 0.01 | -0.07 | 0 | 0.06 | 0 | 0.01 | 0.04 | 0.16 | 0.15 | 0.09 | 0.08 | 0.01 |
|   Gaming |  | -0.58 | 0.51 | 0.11 | -0.31 | -0.51 | -0.39 | -0.32 | -0.19 | -0.34 | -0.11 | 0.21 | -0.14 | 0.36 | 0.41 | 0.48 | 0.49 | 0.44 | 0.14 | 0.02 |
|   Embedded |  | -0.33 | -0.03 | 0.06 | 0.19 | 0.34 | 0.25 | 0.21 | 0.33 | 0.2 | 0.05 | 0.03 | 0.14 | 0.07 | 0.07 | 0.1 | 0.12 | 0.09 | 0.12 | 0.12 |

## p.22 — Figure 33: INTC - Summary Model (p.22)


_Transcribed from the image table as printed (UBS estimates; Company data, FactSet). Percentages stored as fractions._

| Intel (INTC) - Key Metrics (in $MM except EPS and units) | C2024A | C2025A | CQ1A | CQ2A | CQ3E | CQ4E | C2026E | CQ1E | CQ2E | CQ3E | CQ4E | C2027E | CQ1E | CQ2E | CQ3E | CQ4E | C2028E | C2029E | C2030E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Revenue (Non GAAP) | 53,101 | 52,853 | 13,577 | 16,128 | 16,974 | 17,769 | 64,448 | 17,886 | 18,134 | 19,202 | 19,970 | 75,192 | 19,978 | 21,156 | 22,673 | 23,482 | 87,288 | 107,256 | 132,058 |
|   Y/Y Growth | -0.02 | 0 | 0.07 | 0.25 | 0.24 | 0.3 | 0.22 | 0.32 | 0.12 | 0.13 | 0.12 | 0.17 | 0.12 | 0.17 | 0.18 | 0.18 | 0.16 | 0.23 | 0.23 |
| Gross Profit (Non -GAAP) | 19,099 | 19,410 | 5,570 | 6,737 | 7,180 | 7,552 | 27,039 | 7,566 | 7,798 | 8,449 | 8,897 | 32,709 | 8,780 | 9,361 | 10,101 | 10,543 | 38,786 | 48,792 | 62,686 |
|   Gross Margin | 0.36 | 0.367 | 0.41 | 0.418 | 0.423 | 0.425 | 0.42 | 0.423 | 0.43 | 0.44 | 0.446 | 0.435 | 0.44 | 0.443 | 0.446 | 0.449 | 0.444 | 0.455 | 0.475 |
|   R&D (Non-GAAP) | 16,546 | 13,774 | 3,375 | 3,368 | 3,775 | 3,860 | 14,378 | 3,840 | 3,820 | 3,870 | 3,930 | 15,460 | 4,050 | 4,170 | 4,290 | 4,410 | 16,920 | 20,140 | 23,050 |
|   MG&A (Non-GAAP) | 5,507 | 4,624 | 1,038 | 1,175 | 1,250 | 1,280 | 4,743 | 1,200 | 1,250 | 1,320 | 1,380 | 5,150 | 1,310 | 1,430 | 1,530 | 1,560 | 5,830 | 6,240 | 6,890 |
|   Other | -2,700 | -1,904 | -511 | -576 |  |  | -1,087 |  |  |  |  |  |  |  |  |  |  |  |  |
| Total Opex (Non-GAAP) | 19,353 | 16,494 | 3,902 | 3,967 | 4,475 | 4,564 | 16,908 | 4,503 | 4,526 | 4,614 | 4,711 | 18,354 | 4,761 | 4,965 | 5,140 | 5,266 | 20,131 | 23,162 | 25,978 |
|   Y/Y Growth | 0.02 | -0.15 | -0.09 | -0.08 | 0.14 | 0.15 | 0.03 | 0.15 | 0.14 | 0.03 | 0.03 | 0.09 | 0.06 | 0.1 | 0.11 | 0.12 | 0.1 | 0.15 | 0.12 |
| Operating Income (Non-GAAP) | -254 | 2,916 | 1,668 | 2,770 | 2,705 | 2,988 | 10,131 | 3,062 | 3,272 | 3,835 | 4,186 | 14,355 | 4,020 | 4,396 | 4,961 | 5,278 | 18,655 | 25,630 | 36,708 |
|   Operating Margin | -0.005 | 0.055 | 0.123 | 0.172 | 0.159 | 0.168 | 0.157 | 0.171 | 0.18 | 0.2 | 0.21 | 0.191 | 0.201 | 0.208 | 0.219 | 0.225 | 0.214 | 0.239 | 0.278 |
| Non-GAAP EPS | -0.13 | 0.42 | 0.29 | 0.43 | 0.39 | 0.45 | 1.57 | 0.46 | 0.5 | 0.59 | 0.64 | 2.2 | 0.64 | 0.69 | 0.78 | 0.83 | 2.94 | 3.96 | 5.42 |
| Free Cash Flow |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|   CFFO | 8,288 | 9,697 | 1,096 | 7,006 | 6,561 | 4,747 | 19,410 | 3,903 | 6,388 | 7,502 | 7,448 | 25,241 | 6,945 | 8,754 | 9,748 | 9,549 | 34,996 | 47,299 | 58,197 |
|     Less: Gross Capex | 25,122 | 17,672 | 5,136 | 2,479 | 6,000 | 6,600 | 20,215 | 7,500 | 7,000 | 7,000 | 7,000 | 28,500 | 10,000 | 10,000 | 10,000 | 10,000 | 40,000 | 40,000 | 30,000 |
|     Add: Contribution from Partners | 14,650 | 6,685 | 1,607 | 2,642 | 1,900 | 2,000 | 8,149 | 1,200 | 700 | 200 | 200 | 2,300 | 200 | 200 | 200 | 200 | 800 | 800 | 800 |
|   Net Capex | 10,472 | 10,987 | 3,529 | -163 | 4,100 | 4,600 | 12,066 | 6,300 | 6,300 | 6,800 | 6,800 | 26,200 | 9,800 | 9,800 | 9,800 | 9,800 | 39,200 | 39,200 | 29,200 |
| FCF | -2,228 | -1,612 | -2,433 | 7,169 | 2,461 | 147 | 7,344 | -2,397 | 88 | 702 | 648 | -959 | -2,855 | -1,046 | -52 | -251 | -4,204 | 8,099 | 28,997 |
|   % of revenue | -0.04 | -0.03 | -0.18 | 0.44 | 0.15 | 0.01 | 0.11 | -0.13 | 0 | 0.04 | 0.03 | -0.01 | -0.14 | -0.05 | 0 | -0.01 | -0.05 | 0.08 | 0.22 |
|   Y/Y Growth |  |  | -0.34 | -7.83 | 1.75 | -0.93 |  | -0.01 | -0.99 | -0.71 | 3.42 |  | 0.19 | -12.89 | -1.07 | -1.39 |  |  |  |
| Product Revenue |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Intel Products | 49,471 | 49,147 | 12,779 | 15,139 | 15,932 | 16,654 | 60,504 | 16,634 | 16,916 | 17,884 | 18,609 | 70,042 | 18,219 | 19,177 | 20,374 | 20,739 | 78,508 | 86,779 | 93,871 |
| Q/Q |  |  | -0.01 | 0.18 | 0.05 | 0.05 |  | 0 | 0.02 | 0.06 | 0.04 |  | -0.02 | 0.05 | 0.06 | 0.02 |  |  |  |
| Y/Y | 0.04 | -0.01 | 0.09 | 0.28 | 0.26 | 0.29 | 0.23 | 0.3 | 0.12 | 0.12 | 0.12 | 0.16 | 0.1 | 0.13 | 0.14 | 0.11 | 0.12 | 0.11 | 0.08 |
| Operating Income | 13,008 | 12,739 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Operating Margin | 0.26 | 0.26 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|   CCPG | 33,346 | 32,228 | 7,727 | 8,877 | 8,895 | 8,756 | 34,255 | 8,098 | 7,801 | 8,148 | 8,143 | 32,190 | 7,624 | 8,014 | 8,384 | 8,158 | 32,181 | 33,196 | 34,783 |
|   Q/Q |  |  | -0.06 | 0.15 | 0 | -0.02 |  | -0.08 | -0.04 | 0.04 | 0 |  | -0.06 | 0.05 | 0.05 | -0.03 |  |  |  |
|   Y/Y |  | -0.03 | 0.01 | 0.13 | 0.04 | 0.07 | 0.06 | 0.05 | -0.12 | -0.08 | -0.07 | -0.06 | -0.06 | 0.03 | 0.03 | 0 | 0 | 0.03 | 0.05 |
|   Operating Income | 11,594 | 9,317 | 2,516 | 2,343 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|   Operating Margin | 0.35 | 0.29 | 0.33 | 0.26 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|     Desktop Revenue | 9,650 | 8,966 | 2,141 | 2,310 | 2,159 | 2,029 | 8,639 | 1,844 | 1,741 | 1,758 | 1,671 | 7,014 | 1,503 | 1,503 | 1,549 | 1,626 | 6,182 | 6,078 | 5,977 |
|       Q/Q |  |  | -0.07 | 0.08 | -0.07 | -0.06 |  | -0.09 | -0.06 | 0.01 | -0.05 |  | -0.1 |  | 0.03 | 0.05 |  |  |  |
|       Y/Y | -0.05 | -0.07 | 0.01 | 0.07 | -0.1 | -0.12 | -0.04 | -0.14 | -0.25 | -0.19 | -0.18 | -0.19 | -0.18 | -0.14 | -0.12 | -0.03 | -0.12 | -0.02 | -0.02 |
|       Desktop Units ('000s) | 58,316 | 52,506 | 10,886 | 11,267 | 10,478 | 9,849 | 42,479 | 8,864 | 8,244 | 8,244 | 7,832 | 33,184 | 7,048 | 7,048 | 7,260 | 7,623 | 28,980 | 27,785 | 26,257 |
|       Desktop ASP | 165 | 171 | 197 | 205 | 206 | 206 | 203 | 208 | 211 | 213 | 213 | 211 | 213 | 213 | 213 | 213 | 213 | 219 | 228 |
|     Notebook Revenue | 19,091 | 18,657 | 4,449 | 5,381 | 5,537 | 5,648 | 21,015 | 5,196 | 5,013 | 5,290 | 5,340 | 20,840 | 5,011 | 5,412 | 5,683 | 5,344 | 21,450 | 22,345 | 23,798 |
|       Q/Q |  |  | -0.08 | 0.21 | 0.03 | 0.02 |  | -0.08 | -0.04 | 0.06 | 0.01 |  | -0.06 | 0.08 | 0.05 | -0.06 |  |  |  |
|       Y/Y | 0.12 | -0.02 | 0.01 | 0.21 | 0.12 | 0.17 | 0.13 | 0.17 | -0.07 | -0.04 | -0.05 | -0.01 | -0.04 | 0.08 | 0.07 | 0 | 0.03 | 0.04 | 0.06 |
|       Notebook Units ('000s) | 150,490 | 148,178 | 30,748 | 33,207 | 32,543 | 32,543 | 129,041 | 29,940 | 28,742 | 30,179 | 31,085 | 119,946 | 28,598 | 30,886 | 32,430 | 30,808 | 122,722 | 125,598 | 128,541 |
|       Notebook ASP | 127 | 126 | 145 | 162 | 170 | 174 | 163 | 174 | 174 | 175 | 172 | 174 | 175 | 175 | 175 | 173 | 175 | 178 | 185 |
|     Other | 1,549 | 1,365 | 353 | 355 | 357 | 359 | 1,424 | 364 | 369 | 374 | 379 | 1,485 | 384 | 390 | 396 | 402 | 1,572 | 1,666 | 1,766 |
|     NEX in CCG | 3,056 | 3,239 | 784 | 831 | 848 | 848 | 3,310 | 848 | 848 | 890 | 917 | 3,503 | 899 | 890 | 934 | 962 | 3,685 | 3,866 | 4,057 |
|   DCAI | 16,125 | 16,919 | 5,052 | 6,262 | 7,037 | 7,898 | 26,357 | 8,536 | 9,115 | 9,736 | 10,466 | 37,853 | 10,595 | 11,163 | 11,989 | 12,580 | 46,328 | 53,583 | 59,088 |
|   Q/Q |  |  | 0.07 | 0.24 | 0.12 | 0.12 |  | 0.08 | 0.07 | 0.07 | 0.07 |  | 0.01 | 0.05 | 0.07 | 0.05 |  |  |  |
|   Y/Y |  | 0.05 | 0.22 | 0.59 | 0.71 | 0.67 | 0.56 | 0.69 | 0.46 | 0.38 | 0.33 | 0.44 | 0.24 | 0.22 | 0.23 | 0.2 | 0.22 | 0.16 | 0.1 |
|   Operating Income | 1,414 | 3,422 | 1,542 | 2,956 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|   Operating Margin | 0.09 | 0.2 | 0.31 | 0.47 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|     Edge (ex-NEX in DCAI, incl Custom until D | 3,308 | 3,250 | 766 | 687 | 694 | 701 | 2,849 | 687 | 701 | 743 | 773 | 2,904 | 757 | 750 | 787 | 811 | 3,105 | 3,258 | 3,418 |
|     Custom ASIC |  |  | 370 | 500 | 650 | 800 | 2,320 | 1,000 | 1,150 | 1,288 | 1,443 | 4,881 | 1,587 | 1,745 | 1,920 | 2,112 | 7,364 | 9,558 | 11,062 |
|     Server Revenues | 12,817 | 13,419 | 3,916 | 5,075 | 5,693 | 6,397 | 21,080 | 6,784 | 7,197 | 7,635 | 8,177 | 29,793 | 8,173 | 8,587 | 9,196 | 9,568 | 35,523 | 40,359 | 44,112 |
|       Server Units ('000s) | 15,315 | 16,709 | 4,354 | 4,397 | 4,661 | 4,941 | 18,353 | 5,039 | 5,191 | 5,346 | 5,560 | 21,137 | 5,393 | 5,501 | 5,721 | 5,779 | 22,395 | 22,682 | 22,975 |
|       Server ASP | 824 | 791 | 887 | 1,142 | 1,221 | 1,295 | 1,143 | 1,334 | 1,374 | 1,415 | 1,457 | 1,396 | 1,501 | 1,546 | 1,592 | 1,640 | 1,571 | 1,761 | 1,898 |
|     Accelerators | 200 | 200 | 53 | 55 |  |  | 108 | 64 | 67 | 71 | 74 | 276 | 78 | 82 | 86 | 90 | 335 | 408 | 495 |
| Intel Foundry | 17,317 | 17,826 | 5,421 | 5,765 | 6,365 | 7,037 | 24,588 | 6,945 | 7,060 | 7,422 | 7,598 | 29,025 | 7,600 | 8,190 | 8,861 | 9,301 | 33,950 | 45,310 | 62,637 |
| Q/Q |  |  | 0.2 | 0.06 | 0.1 | 0.11 |  | -0.01 | 0.02 | 0.05 | 0.02 |  | 0 | 0.08 | 0.08 | 0.05 |  |  |  |
| Y/Y | -0.08 | 0.03 | 0.16 | 0.31 | 0.5 | 0.56 | 0.38 | 0.28 | 0.22 | 0.17 | 0.08 | 0.18 | 0.09 | 0.16 | 0.19 | 0.22 | 0.17 | 0.33 | 0.38 |
|   Internal Foundry Revenue | 17,288 | 17,683 | 5,251 | 5,477 | 6,025 | 6,627 | 23,380 | 6,495 | 6,560 | 6,822 | 6,958 | 26,835 | 6,750 | 7,020 | 7,371 | 7,371 | 28,510 | 28,510 | 28,510 |
|   External Foundry Revenue | 29 | 143 | 170 | 288 | 340 | 410 | 1,208 | 450 | 500 | 600 | 640 | 2,190 | 850 | 1,170 | 1,490 | 1,930 | 5,440 | 16,800 | 34,127 |
| Operating Income | -13,291 | -10,318 | -2,320 | -2,320 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Operating Margin | -0.77 | -0.58 | -0.43 | -0.4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| All Other | 3,601 | 3,563 | 628 | 701 | 702 | 705 | 2,736 | 802 | 717 | 719 | 722 | 2,960 | 909 | 808 | 810 | 813 | 3,340 | 3,677 | 4,061 |
| Q/Q |  |  | 0.09 | 0.12 | 0 | 0 |  | 0.14 | -0.11 | 0 | 0 |  | 0.26 | -0.11 | 0 | 0 |  |  |  |
| Y/Y |  | -0.01 | -0.33 | -0.33 | -0.29 | 0.23 | -0.23 | 0.28 | 0.02 | 0.02 | 0.02 | 0.08 | 0.13 | 0.13 | 0.13 | 0.13 | 0.13 | 0.1 | 0.1 |
| Operating Income | -57 | 264 | 103 | -139 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Operating Margin | -0.02 | 0.07 | 0.16 | -0.2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

## p.23 — Figure 34: ARM - Summary Model (p.23)


_Transcribed from the image table as printed (UBS estimates; Company data, FactSet). Percentages stored as fractions._

| Arm Holdings Plc. (ARM) - Key Metrics (in $MM except EPS and units) | C2022A | C2023A | C2024A | C2025A | FQ4:26A CQ1A | FQ1A CQ2A | FQ2E CQ3E | FQ3E CQ4E | C2026E | FQ4:27E CQ1E | FQ1E CQ2E | FQ2E CQ3E | FQ3E CQ4E | C2027E | FQ4:28E CQ1E | FQ1E CQ2E | FQ2E CQ3E | FQ3E CQ4E | C2028E | C2029E | C2030E | F2023A | F2024A | F2025A | F2026E | F2027E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Revenue | 2,703 | 2,938 | 3,694 | 4,671 | 1,490 | 1,289 | 1,379 | 1,552 | 5,711 | 1,923 | 1,710 | 1,855 | 2,162 | 7,650 | 2,505 | 2,554 | 2,692 | 2,893 | 10,644 | 14,648 | 24,698 | 2,679 | 3,233 | 4,007 | 4,920 | 6,143 |
|     Y/Y Growth |  | 0.087 | 0.257 | 0.264 | 0.201 | 0.224 | 0.215 | 0.25 | 0.223 | 0.29 | 0.326 | 0.345 | 0.393 | 0.34 | 0.303 | 0.494 | 0.451 | 0.338 | 0.391 | 0.376 | 0.686 | -0.009 | 0.207 | 0.239 | 0.228 | 0.249 |
| Gross Profit (Non-GAAP) | 2,592 | 2,837 | 3,607 | 4,588 | 1,465 | 1,264 | 1,354 | 1,527 | 5,611 | 1,818 | 1,628 | 1,730 | 1,951 | 7,126 | 2,212 | 2,223 | 2,358 | 2,501 | 9,294 | 12,070 | 17,305 | 2,580 | 3,131 | 3,926 | 4,832 | 5,964 |
| Gross Margin | 0.959 | 0.966 | 0.976 | 0.982 | 0.983 | 0.981 | 0.982 | 0.984 | 0.982 | 0.946 | 0.952 | 0.932 | 0.902 | 0.932 | 0.883 | 0.87 | 0.876 | 0.864 | 0.873 | 0.824 | 0.701 | 0.963 | 0.968 | 0.98 | 0.982 | 0.971 |
| Opex (Non-GAAP) | 1,839 | 1,821 | 1,994 | 2,549 | 734 | 733 | 780 | 822 | 3,069 | 866 | 900 | 931 | 966 | 3,662 | 999 | 1,038 | 1,077 | 1,117 | 4,232 | 4,909 | 5,564 | 1,797 | 1,723 | 2,049 | 2,717 | 3,202 |
|     Y/Y Growth |  |  | 0.095 | 0.278 | 0.297 | 0.184 | 0.204 | 0.148 | 0.204 | 0.18 | 0.227 | 0.193 | 0.174 | 0.193 | 0.154 | 0.154 | 0.157 | 0.157 | 0.155 | 0.16 | 0.133 | -0.029 | -0.041 | 0.189 | 0.326 | 0.178 |
| Operating Income (Non-GAAP) | 753 | 1,016 | 1,613 | 2,039 | 731 | 531 | 574 | 705 | 2,541 | 952 | 728 | 799 | 986 | 3,464 | 1,213 | 1,185 | 1,281 | 1,384 | 5,062 | 7,161 | 11,741 | 783 | 1,408 | 1,877 | 2,115 | 2,762 |
| Operating Margin | 0.279 | 0.346 | 0.437 | 0.437 | 0.491 | 0.412 | 0.416 | 0.454 | 0.445 | 0.495 | 0.426 | 0.431 | 0.456 | 0.453 | 0.484 | 0.464 | 0.476 | 0.478 | 0.476 | 0.489 | 0.475 | 0.292 | 0.436 | 0.468 | 0.43 | 0.45 |
| Non-GAAP EPS | 0.62 | 0.94 | 1.45 | 1.72 | 0.6 | 0.45 | 0.48 | 0.58 | 2.1 | 0.78 | 0.6 | 0.66 | 0.81 | 2.85 | 0.99 | 0.97 | 1.05 | 1.13 | 4.14 | 5.8 | 9.31 | 0.64 | 1.28 | 1.64 | 1.77 | 2.28 |
| Free Cash Flow |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| CFFO | 256 | 906 | 806 | 1,522 | 260 | 902 | 510 | 536 | 2,208 | 538 | 1,013 | 686 | 684 | 2,921 | 859 | 1,156 | 1,159 | 1,200 | 4,374 | 5,644 | 8,910 | 739 | 1,090 | 397 | 1,524 | 2,486 |
| Capex and intangibles | -104 | -182 | -233 | -629 | -108 | -237 | -177 | -200 | -722 | -247 | -203 | -220 | -256 | -926 | -297 | -277 | -292 | -314 | -1,180 | -1,474 | -2,239 | -133 | -183 | -298 | -642 | -861 |
|   FCF | 152 | 724 | 573 | 893 | 152 | 665 | 332 | 337 | 1,486 | 291 | 810 | 466 | 427 | 1,995 | 562 | 879 | 867 | 886 | 3,194 | 4,170 | 6,671 | 606 | 907 | 99 | 882 | 1,625 |
|     % of revenue | -0.06 | -0.246 | -0.155 | -0.191 | -0.102 | -0.516 | -0.241 | -0.217 | -0.26 | -0.151 | -0.474 | -0.251 | -0.198 | -0.261 | -0.224 | -0.344 | -0.322 | -0.306 | -0.3 | -0.285 | -0.27 | 0.226 | 0.281 | 0.025 | 0.179 | 0.265 |
|     Y/Y Growth |  | 3.763 | -0.209 | 0.558 | -0.067 | 3.433 | -0.191 | 0.993 | 0.664 | 0.915 | 0.219 | 0.403 | 0.269 | 0.342 | 0.93 | 0.085 | 0.859 | 1.072 | 0.601 | 0.306 | 0.6 | 0.751 | 0.497 | -0.891 | 7.909 | 0.843 |
| Revenue Reporting |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|   Royalty revenue | 1,725 | 1,662 | 2,075 | 2,549 | 671 | 715 | 708 | 807 | 2,901 | 831 | 856 | 899 | 975 | 3,561 | 1,019 | 1,029 | 1,112 | 1,201 | 4,361 | 5,332 | 6,377 | 1,675 | 1,802 | 2,168 | 2,613 | 3,061 |
|     % of revenue | 0.64 | 0.566 | 0.562 | 0.546 | 0.45 | 0.555 | 0.513 | 0.52 | 0.508 | 0.432 | 0.501 | 0.485 | 0.451 | 0.466 | 0.407 | 0.403 | 0.413 | 0.415 | 0.41 | 0.364 | 0.258 | 0.625 | 0.557 | 0.541 | 0.531 | 0.498 |
|     Y/Y growth |  | -0.037 | 0.248 | 0.228 | 0.105 | 0.222 | 0.142 | 0.095 | 0.138 | 0.239 | 0.197 | 0.27 | 0.209 | 0.228 | 0.226 | 0.202 | 0.237 | 0.231 | 0.224 | 0.223 | 0.196 | 0.072 | 0.076 | 0.203 | 0.205 | 0.171 |
|     Q/Q growth |  |  |  |  | -0.09 | 0.066 | -0.01 | 0.14 |  | 0.03 | 0.03 | 0.05 | 0.085 |  | 0.045 | 0.01 | 0.08 | 0.08 |  |  |  |  |  |  |  |  |
|     of which ARM v7 |  |  | 0.9 | 0.25 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0.43 | 0.36 | 0.286 | 0.25 |  |
|     of which ARM v8 |  |  | 1.35 | 0.44 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0.49 | 0.465 | 0.447 | 0.15 |  |
|     of which ARM v9 |  | 0.25 | 0.95 | 0.31 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0.08 | 0.175 | 0.267 | 0.6 |  |
|   License and other revenue | 978 | 1,276 | 1,619 | 2,122 | 819 | 574 | 672 | 745 | 2,810 | 991 | 754 | 776 | 807 | 3,328 | 936 | 908 | 890 | 899 | 3,634 | 3,659 | 3,693 | 1,004 | 1,431 | 1,839 | 2,307 | 2,982 |
|     % of Total revenue | 0.36 | 0.434 | 0.438 | 0.454 | 0.55 | 0.445 | 0.487 | 0.48 | 0.492 | 0.516 | 0.441 | 0.418 | 0.373 | 0.435 | 0.374 | 0.356 | 0.331 | 0.311 | 0.341 | 0.25 | 0.15 | 0.375 | 0.443 | 0.459 | 0.469 | 0.485 |
|     Y/Y growth |  | 0.305 | 0.269 | 0.311 | 0.292 | 0.226 | 0.304 | 0.476 | 0.324 | 0.211 | 0.313 | 0.156 | 0.083 | 0.184 | -0.056 | 0.205 | 0.147 | 0.114 | 0.092 | 0.007 | 0.009 | -0.12 | 0.425 | 0.285 | 0.254 | 0.293 |
|     Q/Q growth |  |  |  |  | 0.622 | -0.299 | 0.17 | 0.11 |  | 0.33 | -0.24 | 0.03 | 0.04 |  | 0.16 | -0.03 | -0.02 | 0.01 |  |  |  |  |  |  |  |  |
|     Annualized Contract Value (ACV) | 4,171 | 4,346 | 4,898 | 6,113 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 1,030 | 1,182 | 1,365 |  |  |
|       % Y/Y |  | 0.042 | 0.127 | 0.248 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0.148 | 0.155 |  |  |
|       % Q/Q |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|     Remaining Performance Obligation (RPO) | 6,993 | 8,177 | 9,362 | 8,852 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 1,712 | 2,484 | 2,226 |  |  |
|       % Y/Y |  | 0.169 | 0.145 | -0.054 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | -0.022 | 0.451 | -0.104 |  |  |
|       % Q/Q |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|       implied orders | 408 | 1,528 | 1,162 | 1,043 | 518 | 935 | 1,020 | 1,132 | 3,604 | 1,505 | 1,151 | 1,186 | 1,233 | 5,076 | 1,431 | 1,397 | 1,369 | 1,383 | 5,580 | 5,655 | 5,746 | 530 | 1,823 | 1,163 | 1,143 | 4,592 |
|       book-to-bill | 2.4 | 0.8 | 1.4 | 2 | 0.9 | 1.1 | 1 | 1 | 0.8 | 1 | 1 | 1 | 1 | 0.7 | 1 | 1 | 1 | 1 | 0.7 | 0.6 | 0.6 | 0.9 | 1.7 | 0.8 | 0.9 | 1 |

## p.24 — Figure 35: INTC - New vs Old Estimates (p.24)


_Transcribed from the image table as printed (UBS estimates; Company data, FactSet). Percentages stored as fractions._

|  | C2026E New | C2026E Old | C2026E Change | C2027E New | C2027E Old | C2027E Change | C2028E New | C2028E Old | C2028E Change |
|---|---|---|---|---|---|---|---|---|---|
| Revenue ($MM) | 64,448 | 64,448 |  | 75,192 | 75,192 |  | 87,382 | 87,382 |  |
|   Y/Y Growth | 0.219 | 0.219 |  | 0.167 | 0.167 |  | 0.162 | 0.162 |  |
| Gross Margin | 0.42 | 0.42 |  | 0.435 | 0.435 |  | 0.444 | 0.444 |  |
| Operating Margin | 0.157 | 0.156 | 0.002 | 0.191 | 0.191 |  | 0.214 | 0.214 |  |
| Non-GAAP EPS | 1.57 | 1.55 | 0.011 | 2.2 | 2.19 | 0 | 2.94 | 2.94 | 0 |
| FCF | 7,344 | 7,244 | 0.014 | -959 | -962 | -0.003 | -4,077 | -4,080 | -0.001 |
| Gross Capex | 20,215 | 20,215 |  | 28,500 | 28,500 |  | 40,000 | 40,000 |  |
| Segment Revenues ($MM) |  |  |  |  |  |  |  |  |  |
| Intel Products | 60,504 | 60,504 |  | 70,042 | 70,042 |  | 78,602 | 78,602 |  |
|   Y/Y Growth | 0.231 | 0.231 |  | 0.158 | 0.158 |  | 0.122 | 0.122 |  |
|   Client Computing (CCPG) | 34,255 | 34,255 |  | 32,190 | 32,190 |  | 32,181 | 32,181 |  |
|     Y/Y Growth | 0.063 | 0.063 |  | -0.06 | -0.06 |  | 0 | 0 |  |
|   Datacenter and AI (DCAI) | 26,357 | 26,357 |  | 37,853 | 37,853 |  | 46,421 | 46,421 |  |
|     Y/Y Growth | 0.558 | 0.558 |  | 0.436 | 0.436 |  | 0.226 | 0.226 |  |
| Intel Foundry | 24,588 | 24,588 |  | 29,025 | 29,025 |  | 33,950 | 33,950 |  |
|   Y/Y Growth | 0.379 | 0.379 |  | 0.18 | 0.18 |  | 0.17 | 0.17 |  |
|   of which external revenue | 1,208 | 1,208 |  | 2,190 | 2,190 |  | 5,440 | 5,440 |  |
| All Other | 2,736 | 2,736 |  | 2,960 | 2,960 |  | 3,340 | 3,340 |  |
|   Y/Y Growth | -0.232 | -0.232 |  | 0.082 | 0.082 |  | 0.128 | 0.128 |  |
| Intersegment Eliminations | -23,380 | -23,380 |  | -26,835 | -26,835 |  | -28,510 | -28,510 |  |

## p.25 — Figure 36: UBSe vs. Street (p.25)


_Transcribed from the image table as printed (UBS estimates; Company data, FactSet). Percentages stored as fractions._

|  | Actual 2025 | Actual 2026/1F | Actual 2026/2F | Estimate 2026/3F | Estimate 2026/4F | Estimate 2026 | Estimate 2027/1F | Estimate 2027/2F | Estimate 2027/3F | Estimate 2027/4F | Estimate 2027 | Estimate 2028/1F | Estimate 2028/2F | Estimate 2028/3F | Estimate 2028/4F | Estimate 2028 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Revenues ($MM) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|   UBS New | 52,853 | 13,577 | 16,128 | 16,974 | 17,769 | 64,448 | 17,886 | 18,134 | 19,202 | 19,970 | 75,192 | 19,978 | 21,156 | 22,673 | 23,482 | 87,288 |
|   UBS Old |  |  |  | 16,974 | 17,769 | 64,448 | 17,886 | 18,134 | 19,202 | 19,970 | 75,192 | 19,899 | 21,155 | 22,757 | 23,571 | 87,382 |
|   Consensus |  |  |  | 16,518 | 17,119 | 63,341 | 16,928 | 17,858 | 18,799 | 19,584 | 73,169 | 19,507 | 20,357 | 21,513 | 22,612 | 83,990 |
|   Delta |  |  |  | 0.028 | 0.038 | 0.017 | 0.057 | 0.015 | 0.021 | 0.02 | 0.028 | 0.024 | 0.039 | 0.054 | 0.038 | 0.039 |
| Non-GAAP EPS |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|   UBS New | 0.42 | 0.29 | 0.43 | 0.39 | 0.45 | 1.57 | 0.46 | 0.5 | 0.59 | 0.64 | 2.2 | 0.64 | 0.69 | 0.78 | 0.83 | 2.94 |
|   UBS Old |  |  |  | 0.39 | 0.45 | 1.57 | 0.46 | 0.5 | 0.59 | 0.64 | 2.2 | 0.63 | 0.69 | 0.79 | 0.83 | 2.94 |
|   Consensus |  |  |  | 0.4 | 0.44 | 1.56 | 0.41 | 0.49 | 0.58 | 0.65 | 2.13 | 0.67 | 0.75 | 0.85 | 0.94 | 3.22 |
|   Delta |  |  |  | -0.035 | 0.024 | 0.008 | 0.137 | 0.018 | 0.008 | -0.016 | 0.028 | -0.054 | -0.075 | -0.083 | -0.123 | -0.087 |

## p.26 — Figure 37: Intel SOTP Valuation (New) (p.26)


_Transcribed from the image table as printed (UBS estimates; Company data, FactSet). Percentages stored as fractions._

|  | Total $MM | Per Share | Comments |
|---|---|---|---|
| Intel Products |  |  |  |
|   Revenue | 70,042 |  |  |
|   Normalized EBIT margin | 0.25 |  |  |
|     Normalized EBIT | 17,511 |  |  |
|   Peer EV/EBIT | 27 |  |  |
|     Products SoTP Value | 465,783 | 86 |  |
| Intel Foundry |  |  |  |
|   Intel Capacity (k-wsm) | 364 |  |  |
|   Peer Value per k-wsm | 160 |  |  |
|     Gross Foundry Value | 58,393 | 11 |  |
| Noncontrolling Interest | -14,200 | -3 | Brookfield only, at historical cost |
|     Net Foundry SoTP Value | 44,193 | 8 |  |
| Other |  |  |  |
|   Market Cap | 14,310 |  | Based on valuation and market cap. |
|   Intel Stake | 0.61 |  |  |
|     Other SoTP Value | 8,736 | 2 |  |
| TOTAL |  |  |  |
|   SoTP Enterprise Value | 518,712 | 95 |  |
| Net Debt | 27,184 | 5 |  |
|   SoTP Equity Value | 545,896 | 100 |  |

## p.26 — Figure 38: Intel SOTP Valuation (Old) (p.26)


_Transcribed from the image table as printed (UBS estimates; Company data, FactSet). Percentages stored as fractions._

|  | Total $MM | Per Share | Comments |
|---|---|---|---|
| Intel Products |  |  |  |
|   Revenue | 70,042 |  |  |
|   Normalized EBIT margin | 0.25 |  |  |
|     Normalized EBIT | 17,511 |  |  |
|   Peer EV/EBIT | 27 |  |  |
|     Products SoTP Value | 476,289 | 88 |  |
| Intel Foundry |  |  |  |
|   Intel Capacity (k-wsm) | 364 |  |  |
|   Peer Value per k-wsm | 166 |  |  |
|     Gross Foundry Value | 60,445 | 11 |  |
| Noncontrolling Interest | -14,200 | -3 | Brookfield only, at historical cost |
|     Net Foundry SoTP Value | 46,245 | 9 |  |
| Other |  |  |  |
|   Market Cap | 14,888 |  | Based on valuation and market cap. |
|   Intel Stake | 0.62 |  |  |
|     Other SoTP Value | 9,198 | 2 |  |
| TOTAL |  |  |  |
|   SoTP Enterprise Value | 531,732 | 98 |  |
| Net Debt | 27,184 | 5 |  |
|   SoTP Equity Value | 558,916 | 103 |  |

## p.26 — Figure 39: Intel Foundry Comps (p.26)


_Transcribed from the image table as printed (UBS estimates; Company data, FactSet). Percentages stored as fractions._

| Ticker | Company Name | Capacity | EV | EV/k-wsm |
|---|---|---|---|---|
| 2330-TW | TSMC | 1,642 | 1,802,505 | 604 |
| 005930-KR | Samsung Foundry | 1,685 | 969,422 | 178 |
| 2303-TW | UMC | 440 | 45,618 | 104 |
| 981-HK | SMIC | 507 | 65,426 | 129 |
| GFS-US | GlobalFoundries | 292 | 23,736 | 81 |
| 1347-HK | Hua Hong | 247 | 18,747 | 76 |
| 688249-CN | Vanguard (200mm) | 146 | 8,752 | 60 |
| 6770-TW | PSMC (200mm) | 163 | 8,379 | 51 |
|  | Simple Average | 640 | 367,823 | 160 |
|  | Median | 366 | 34,677 | 92 |

## p.18 — Figs 28-31: provenance of each digitized cell


_label = printed segment label (+/-0.5pp) · measured = vector segment height (+/-0.05pp) · measured_x_S = height rescaled by the bar's plotted sum S (Fig 29 bars are drawn scaled to 100% although the plotted series sum to only 28-99%; the unplotted residual is almost certainly Rome/Zen 2 — Fig 31's 7nm = Milan + residual within 1pp) · not_drawn = segment absent_

| Fig 28 INTC product mix |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| quarter | granite_rapids_src | sierra_forest_src | emerald_rapids_src | sapphire_rapids_src | ice_lake_src | cascade_lake_src | others_src | unplotted_residual_src |
| 1Q21 | not_drawn | not_drawn | not_drawn | not_drawn | measured | label | label | n/a |
| 2Q21 | not_drawn | not_drawn | not_drawn | not_drawn | label | label | label | n/a |
| 3Q21 | not_drawn | not_drawn | not_drawn | not_drawn | label | label | label | n/a |
| 4Q21 | not_drawn | not_drawn | not_drawn | not_drawn | label | label | label | n/a |
| 1Q22 | not_drawn | not_drawn | not_drawn | measured | label | label | label | n/a |
| 2Q22 | not_drawn | not_drawn | not_drawn | measured | label | label | label | n/a |
| 3Q22 | not_drawn | not_drawn | not_drawn | measured | label | label | label | n/a |
| 4Q22 | not_drawn | not_drawn | not_drawn | measured | label | label | label | n/a |
| 1Q23 | not_drawn | not_drawn | not_drawn | measured | label | label | label | n/a |
| 2Q23 | not_drawn | not_drawn | not_drawn | label | label | label | label | n/a |
| 3Q23 | not_drawn | not_drawn | measured | label | label | label | not_drawn | n/a |
| 4Q23 | not_drawn | not_drawn | measured | label | label | label | not_drawn | n/a |
| 1Q24 | not_drawn | measured | label | label | label | label | not_drawn | n/a |
| 2Q24 | not_drawn | measured | label | label | label | label | not_drawn | n/a |
| 3Q24 | measured | label | label | label | label | label | not_drawn | n/a |
| 4Q24 | measured | label | label | label | label | not_drawn | not_drawn | n/a |
| 1Q25 | measured | label | label | label | label | not_drawn | not_drawn | n/a |
| 2Q25 | label | label | label | label | label | not_drawn | not_drawn | n/a |
| 3Q25 | label | label | label | label | label | not_drawn | not_drawn | n/a |
| 4Q25 | label | label | label | label | label | not_drawn | not_drawn | n/a |
| 1Q26 | label | label | label | label | label | not_drawn | measured | n/a |
| 2Q26 | label | label | label | label | label | not_drawn | measured_x_S | 100-S |
| Fig 29 AMD product mix |  |  |  |  |  |  |  |  |
| quarter | venice_src | turin_src | bergamo_src | siena_src | genoa_src | milan_src | others_src | unplotted_residual_src |
| 1Q21 | not_drawn | not_drawn | not_drawn | not_drawn | not_drawn | label | label | 100-S |
| 2Q21 | not_drawn | not_drawn | not_drawn | not_drawn | not_drawn | label | label | 100-S |
| 3Q21 | not_drawn | not_drawn | not_drawn | not_drawn | not_drawn | label | label | 100-S |
| 4Q21 | not_drawn | not_drawn | not_drawn | not_drawn | not_drawn | label | label | 100-S |
| 1Q22 | not_drawn | not_drawn | not_drawn | not_drawn | measured_x_S | label | label | 100-S |
| 2Q22 | not_drawn | not_drawn | not_drawn | not_drawn | measured_x_S | label | label | 100-S |
| 3Q22 | not_drawn | not_drawn | not_drawn | not_drawn | measured_x_S | label | label | 100-S |
| 4Q22 | not_drawn | not_drawn | not_drawn | not_drawn | label | label | label | 100-S |
| 1Q23 | not_drawn | not_drawn | measured_x_S | not_drawn | label | label | label | 100-S |
| 2Q23 | not_drawn | not_drawn | measured_x_S | measured_x_S | label | label | label | 100-S |
| 3Q23 | not_drawn | not_drawn | label | measured_x_S | label | label | label | 100-S |
| 4Q23 | not_drawn | not_drawn | label | measured_x_S | label | label | label | 100-S |
| 1Q24 | not_drawn | not_drawn | label | measured_x_S | label | label | label | 100-S |
| 2Q24 | not_drawn | measured_x_S | label | measured_x_S | label | label | measured_x_S | 100-S |
| 3Q24 | not_drawn | measured_x_S | label | measured_x_S | label | label | measured_x_S | 100-S |
| 4Q24 | not_drawn | label | label | measured_x_S | label | label | measured_x_S | 100-S |
| 1Q25 | not_drawn | label | label | measured_x_S | label | label | measured_x_S | 100-S |
| 2Q25 | not_drawn | label | label | measured_x_S | label | label | measured_x_S | 100-S |
| 3Q25 | measured_x_S | label | label | measured_x_S | label | label | measured_x_S | 100-S |
| 4Q25 | measured_x_S | label | label | measured_x_S | label | label | measured_x_S | 100-S |
| 1Q26 | measured_x_S | label | label | measured_x_S | label | label | measured_x_S | 100-S |
| 2Q26 | label | label | label | measured_x_S | label | label | measured_x_S | 100-S |
| Fig 30 INTC node mix |  |  |  |  |  |  |  |  |
| quarter | intel_14_src | intel_10_src | intel_7_src | intel_3_src | unknown_other_src | unplotted_residual_src |  |  |
| 1Q21 | label | measured | not_drawn | not_drawn | label | n/a |  |  |
| 2Q21 | label | label | not_drawn | not_drawn | label | n/a |  |  |
| 3Q21 | label | label | not_drawn | not_drawn | label | n/a |  |  |
| 4Q21 | label | label | not_drawn | not_drawn | label | n/a |  |  |
| 1Q22 | label | label | measured | not_drawn | label | n/a |  |  |
| 2Q22 | label | label | measured | not_drawn | label | n/a |  |  |
| 3Q22 | label | label | measured | not_drawn | label | n/a |  |  |
| 4Q22 | label | label | label | not_drawn | label | n/a |  |  |
| 1Q23 | label | label | label | not_drawn | label | n/a |  |  |
| 2Q23 | label | label | label | not_drawn | label | n/a |  |  |
| 3Q23 | label | label | label | not_drawn | not_drawn | n/a |  |  |
| 4Q23 | label | label | label | not_drawn | not_drawn | n/a |  |  |
| 1Q24 | label | label | label | measured | not_drawn | n/a |  |  |
| 2Q24 | label | label | label | label | not_drawn | n/a |  |  |
| 3Q24 | label | label | label | label | not_drawn | n/a |  |  |
| 4Q24 | not_drawn | label | label | label | not_drawn | n/a |  |  |
| 1Q25 | not_drawn | label | label | label | not_drawn | n/a |  |  |
| 2Q25 | not_drawn | label | label | label | not_drawn | n/a |  |  |
| 3Q25 | not_drawn | label | label | label | not_drawn | n/a |  |  |
| 4Q25 | not_drawn | label | label | label | not_drawn | n/a |  |  |
| 1Q26 | not_drawn | label | label | label | measured | n/a |  |  |
| 2Q26 | not_drawn | label | label | label | label | n/a |  |  |
| Fig 31 AMD node mix |  |  |  |  |  |  |  |  |
| quarter | 7nm_src | 5nm_src | 3_4nm_src | 2nm_src | unknown_other_src | unplotted_residual_src |  |  |
| 1Q21 | label | not_drawn | not_drawn | not_drawn | label | n/a |  |  |
| 2Q21 | label | not_drawn | not_drawn | not_drawn | label | n/a |  |  |
| 3Q21 | label | not_drawn | not_drawn | not_drawn | label | n/a |  |  |
| 4Q21 | label | not_drawn | not_drawn | not_drawn | label | n/a |  |  |
| 1Q22 | label | measured | not_drawn | not_drawn | label | n/a |  |  |
| 2Q22 | label | measured | not_drawn | not_drawn | label | n/a |  |  |
| 3Q22 | label | label | not_drawn | not_drawn | label | n/a |  |  |
| 4Q22 | label | label | not_drawn | not_drawn | label | n/a |  |  |
| 1Q23 | label | label | not_drawn | not_drawn | label | n/a |  |  |
| 2Q23 | label | label | not_drawn | not_drawn | label | n/a |  |  |
| 3Q23 | label | label | not_drawn | not_drawn | label | n/a |  |  |
| 4Q23 | label | label | not_drawn | not_drawn | label | n/a |  |  |
| 1Q24 | label | label | not_drawn | not_drawn | label | n/a |  |  |
| 2Q24 | label | label | measured | not_drawn | label | n/a |  |  |
| 3Q24 | label | label | label | not_drawn | measured | n/a |  |  |
| 4Q24 | label | label | label | not_drawn | measured | n/a |  |  |
| 1Q25 | label | label | label | not_drawn | measured | n/a |  |  |
| 2Q25 | label | label | label | not_drawn | measured | n/a |  |  |
| 3Q25 | label | label | label | not_drawn | measured | n/a |  |  |
| 4Q25 | label | label | label | not_drawn | measured | n/a |  |  |
| 1Q26 | label | label | label | label | measured | n/a |  |  |
| 2Q26 | label | label | label | label | measured | n/a |  |  |
