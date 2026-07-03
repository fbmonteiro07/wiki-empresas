# Figure transcriptions — "(3) Uncovering the Secrets to GLM 5.2s Amazing Performance.pdf"

Pages covered: 9, 11, 12, 14, 22, 37. Machine transcription of figure/chart pages so the data is text-searchable. No printed broker source lines on these pages (Substack article by Devansh); source noted per figure where printed.

## p.9 — Attention visualization (BertViz-style token-to-token attention diagram)

Interactive attention visualizer screenshot. Controls: "Layer: 0", "Attention: All", with a row of colored head selectors. Two columns of tokens (left = query, right = key) connected by attention lines: [CLS], many, people, dislike, steve, jobs, ",", while, acknowledging, his, genius, [SEP]. No numeric data.

Accompanying text: earlier efficient attention methods (e.g., Longformer) used fixed sliding windows and predetermined sparse patterns; fixed patterns cannot adapt to input, causing a severe quality gap.

Source: none printed (attention-visualization tool screenshot).

## p.11 — Infographic: "WHAT COMES AFTER TRANSFORMERS?"

Intro text: Transformer hitting a physical memory wall; global self-attention forces O(n²) prefill compute tax and a KV cache bandwidth tax. At 1M tokens the KV cache alone exceeds cluster VRAM limits. Five structural escape routes.

Chart 1: "KV Cache Size vs Context (70B Model)" — x-axis: context length (4K, 32K, 128K, 1M); y-axis: Cache Size (GB), gridlines 0/25/50/75/100/125/150. Dashed reference line: "80GB H100 VRAM Limit" (~80 GB). Line rises from ~0 GB at 4K, small at 32K, ~25 GB at 128K, to ~160 GB at 1M.

Chart 2: "Inference Hardware Cost / 1M Output Tokens" — y-axis Cost (USD) 0–20. Bars: 4K context (59 Users) = $0.34; 128K context (1 User) = $19.84.

Boxes (mechanism/tradeoff):
1. Transformer-Preserving (KV Redesign & Compression) — MLA low-rank projection, KIVI asymmetric quantization, SnapKV prunes 'useless' tokens. Tradeoff: memory for computation; MLA needs on-the-fly reconstruction and breaks standard RoPE; eviction risks pruning tokens needed hundreds of steps later.
2. State Space Models (Mamba, Mamba-2) — removes attention; recurrent O(1) loop; bypasses O(n²) prefill via Convolution Theorem and FFTs. Tradeoff: error compounds through time; quantization drift; fixed state causes feature collision, destroying 'needle-in-a-haystack' recall.
3. Linear Attention (GLA, RetNet) — removes softmax via Kernel Factorization; compresses sequence into fixed-size Fast-Weight memory grid. Tradeoff: Arithmetic Intensity Trap — memory-bound during generation; 'identity blur' forces decay gates that ruin pure parallelization.
4. Hybrid Architectures (Jamba, RecurrentGemma) — SSM/Linear blocks compress local syntax [continues on p.12].

Source: none printed (infographic credited "Devansh/Chocolate Milk Cult Leader" on p.12).

## p.12 — Infographic continuation: escape route 5 + "Context Scaling Trilemma"

Continuation of box 4: deploys sparse Exact Attention layers periodically (e.g., 1 in 8) as global routers to retrieve 'needles'. Tradeoff: massive kernel-switching overhead; swapping activation tensors between HBM and SRAM craters FLOP utilization; complicates memory allocators like PagedAttention.

Box 5. Extreme Context Systems (Distributed & Sinks) — Ring Attention shards sequences across GPUs, passing KV blocks in a ring; StreamingLLM locks early 'sink' tokens, maintains rolling window. Tradeoff: Ring Attention decode bottlenecked by InfiniBand cables rather than GPU HBM; StreamingLLM = absolute amnesia for middle context.

"TAKEAWAY: THE CONTEXT SCALING TRILEMMA" — triangle diagram with vertices: Perfect Exact Recall (Token Identity Preserved) — Standard Attention, Ring Attention; O(1) Memory Footprint (Infinite Context Scalability) — Pure Mamba, Linear Attention; Max Hardware Efficiency (SRAM / TFLOPS Utilized) — FlashAttention Kernels; center: Hybrids (Jamba). You cannot simultaneously achieve all three.

"THE FINAL VERDICT": during generation the bottleneck is BYTES MOVED, not MATH COMPUTED; you pay with VRAM, precision, or infrastructure complexity.

Signed: Devansh/Chocolate Milk Cult Leader.

Below: section "The DeepSeek Sparse Attention Solution" begins, quote: DSA replaces dense O(L²) attention — prohibitively expensive at 128K contexts — with dynamic fine-grained selection.

## p.14 — Figure 6: SFT loss curves, MLA vs DSA training

Line chart. X-axis: Step (0.0–1.0, normalized); y-axis: Loss (~0.33–0.57). Series: MLA (blue) and DSA (red), nearly overlapping — loss falls from ~0.57 at step 0 to ~0.45 by 0.1, ~0.40 at 0.4–0.5, ~0.36 at 0.6, minimum ~0.33 near 0.8–0.9, slight uptick to ~0.34 at 1.0. Inset "Relative Loss": oscillates within roughly ±0.0004 over steps 0.66–0.78.

Caption: "Figure 6: SFT loss curves comparison between MLA and DSA training. Results are smoothed by Running Average with a window size of 50."

Source: none printed (figure from DeepSeek paper as reproduced in article).

## p.22 — Figure 4: PPO vs GRPO diagram (DeepSeekMath paper)

Flow diagram, no numeric data.
- PPO: q → Policy Model → o → {Reference Model (KL, ⊕ → r), Reward Model, Value Model (→ v)} → GAE → A. Legend: Trained Models (yellow), Frozen Models (blue).
- GRPO: q → Policy Model → o1, o2, …, oG → Reference Model (KL) + Reward Model → r1, r2, …, rG → Group Computation → A1, A2, …, AG.

Caption: "Figure 4 | Demonstration of PPO and our GRPO. GRPO foregoes the value model, instead estimating the baseline from group scores, significantly reducing training resources."

Page also contains equations (2) per-token KL-penalized reward and (3) the GRPO objective J_GRPO(θ), with ε and β hyper-parameters and group-relative advantage Â_{i,t}.

Source: none printed (reproduced from DeepSeek GRPO/DeepSeekMath paper).

## p.37 — (no data content — Substack comments/footer page: "Write a comment...", © 2026 Devansh, Substack links)
