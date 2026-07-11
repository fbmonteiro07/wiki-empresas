# Canonical assumptions — one number per debate

_Generated 2026-07-10 from `_data/assumptions.json` (asof 2026-07-01). Every cross-page industry number lives here once, with all sourced variants. When a new source disagrees, add a variant to the JSON — never silently rebase a page. Rebuild: `py _wiki/_tools/build_assumptions.py`._

## Custom-ASIC vs merchant-GPU share of AI accelerators  `asic-vs-gpu-share`

_ASIC/XPU vs merchant-GPU split of AI accelerator shipments — ALWAYS state basis (units vs dollars) and horizon._

**Canonical:** Near-term unit share inflects to ASICs (JPM: 42% 2026E -> 53% 2027E, units) while long-term dollar/unit share settles ~65-70% GPU (BofA AI 2030, UBS durable 70/30). These are horizons, not contradictions — the debate is whether the 2027 unit inflection sticks or plateaus.

> ⚠️ **Scope:** Unit share ≠ dollar share (ASIC ASPs are far lower). NVDA-page '~70% defensible' framing = long-horizon accelerator share, consistent with BofA 65-70% by 2030, NOT a rebuttal of JPM's 2027 unit-share call.

| Value | Source | Date | Scope |
|---|---|---|---|
| 42% ASIC / 58% GPU units 2026E -> 53% / 47% 2027E; ASIC units +109% y/y vs GPU +39% (2026) | JPM Sur, AI Capex 2.0 | 2026-06-16 | unit share, near-term |
| ~70/30 GPU/ASIC durable long-term | UBS Arcuri | 2026-06-04 | long-term split |
| ~65-70% GPU / 30-35% ASIC by 2030; NVDA ~68-77% of accelerators CY25->CY30, AVGO 8%->16% | BofA Arya, AI 2030 | 2026-05-13 | share by 2030 |

**Debate:** Does the 2027 ASIC unit-share inflection (JPM) stick, or does GPU hold ~70% long-term (UBS/BofA)? Watch TPU v9 volumes, Trainium 3 ramp, MTIA.

**Unreconciled sightings** (pages matching this metric, not in the ledger's `cited_in`):
- `ADVANTEST.md` — …akers — demand pulled by GPU/HPC/custom-ASIC leaders (NVDA the single biggest opportunity); ~98% overseas, China ~20–25% | | **Key suppliers** | Ups…
- `ANTHROPIC.md` — …26**, and (assuming ~1,000W TDP per TPU/ASIC) **20 GW ≈ 7mn+ TPU units ≈ 360–460k CoWoS demand** — a rare bottoms-up unit read on…
- `ARM.md` — …h largely doesn't build CPUs) wins more ASIC share, every Broadcom/MTIA deployment **still needs a host CPU**…
- `AVGO.md` — …g as "conservative messaging." Context: ASICs ~42% of total DC AI-chip units in 2026 → ~53% in 2027, with ASIC units growing ~3x faster…
- `GOOG.md` — …TPU is one of the two dominant merchant ASICs; total ASIC + ASIC-server units both seen +50%+. - **CoWoS allocation reset higher** for T…
- `MEDIATEK.md` — …supporting the **2026 target of US$2bn ASIC revenue** (400-500k unit shipments). For 2027, management guided **US$7-12bn ASIC re…
- `MRVL.md` — …— higher margin and durability vs. the ASIC opportunity" (MS Scale-up primer). TD Cowen adds that the nascent scal…
- `SKHYNIX.md` — …nder-executed on Western-tool access. **ASIC share of HBM is "going up a little" but the majority of HBM still…
- `TER.md` — …-12-15)_: **Neutral, PT $193.37** — VIP-ASIC TAM durability + NVDA share gains the 2026 watchpoint; robotics still sub-breakeven. -…
- `themes/ai-datacenter-power.md` — …er still the binding constraint; ASICs ~42% of AI chip units 2026 → ~53% 2027 (ASIC units +109% y/y vs GPU +39%) (JPM, 2026-06-16).…
- `themes/hbm-memory.md` — …o a higher HBM mix lowers volatility. **ASIC share of HBM is rising but "the majority still goes into GPU."**…
- `themes/macro-cycle.md` — …nsible. The current sell-side split is ~70/30 bull vs skeptic, but the skeptic case has gotten more sophi…

## WFE market size CY26 / CY27 / CY28  `wfe-tam`

_Total wafer-fab equipment market ($bn) by calendar year._

**Canonical:** CY26 ~$140-160B (all sources agree). CY27: house $180-215B vs MS ~$191B vs UBS $200B. CY28 is the genuine conflict: house top end $260B vs UBS $250B vs MS-implied ~$230-240B; skeptic ceiling 'never $300B' (ex-Samsung foundry EVP). Swing variable = memory-capex intensity + EUV availability post-2027 + first NAND greenfield (CY28).

> ⚠️ **Scope:** House CY28 top-of-range ($260B) sits ABOVE street — this is a deliberate house-vs-street edge, tracked, not an error.

| Value | Source | Date | Scope |
|---|---|---|---|
| $148-158B CY26 / $180-215B CY27 / $202-260B CY28 | Capstone house model | 2026-06-15 | house |
| $147B CY26 / ~$191B CY27 / mid-teens growth CY28 | MS Moore-Shane | 2026-06-22 | street |
| ~$150B CY26 / ~$170B CY27 base | Tokyo Electron (SIG tour) | 2026-06-18 | vendor view |
| $200B CY27 / $250B CY28 | UBS Arcuri | 2026-05-15 | street bull |
| $272B by 2030 (18% CAGR) | Redburn | 2026-06-17 | 2030 frame |
| WFE<->EUV mapping: ~110 EUV slots ~= $225B WFE | UBS Arcuri | 2026-06-15 | unit reconciliation |
| house CY28 $260B implies ASML ~110-120 EUV shipments 2028 (vs supply chain sized ~90; JPM: 110+ possible without new buildings) | Capstone reconciliation (Memory_supply_demand.xlsx EUV tab, sec.9) | 2026-07-01 | house-vs-street bridge |
| 'never $300B' ceiling | former Samsung foundry EVP (expert call) | 2026-06-30 | skeptic ceiling |

**Debate:** CY28: house $260B top vs street $230-250B. Resolves on memory greenfield timing + EUV shipments. UNIT BRIDGE (2026-07-01): believing house $260B = believing ASML flexes to ~110-120 EUV ships in 2028 (above the ~90 supply-chain sizing; JPM says 110+ feasible). Base bottom-up demand supports ~88-95; the gap = faster DRAM node migration + 2029 pre-provisioning.

**Unreconciled sightings** (pages matching this metric, not in the ledger's `cited_in`):
- `ADVANTEST.md` — …d-through):** JEF Japan raised 2026/27E WFE to **$149bn / $165bn (+10%/+9%)**, still likely below buy-side (>25% for CY27)…
- `AMAT.md` — …T a share-gainer.** Arcuri (UBS) frames WFE to **~$200B in 2027 and ~$250B in 2028** (+$50B/yr); AMAT recovers ~half the **280 bps** o…
- `INTC.md` — …is: SpaceX AI capex ~$1.1T/5yrs, ~20% (~$225B) to Terafab; at 60% capex-to-WFE → ~$135B WFE over 5yrs (~= this year's entire global WFE TA…
- `KIOXIA.md` — …y comp. - Capacity adds and CY2027 NAND WFE up-cycle (BofA Hosseini flagged $200bn+ annualized WFE into 2H CY27, briefing 2026-05-15) — suppl…
- `KLAC.md` — …r** (SpaceX AI capex ~$1.1T/5yrs, ~20%/~$225B to Terafab, 60% capex-to-WFE → **~$135B WFE over 5yrs ≈ the entire global WFE TAM this y…
- `LRCX.md` — …(Sur/JPM, 2026-05-15; 2026-05-22). The WFE TAM ceiling keeps rising — UBS holds **$200B CY27 / $250B CY28** and reads Lam's capacity actions as con…
- `MU.md` — …bottleneck until ~110 physical slots (~$225B WFE); ASML is getting the same 8-10-quarter visibility as US to…
- `NVDA.md` — …model-builder that reinvests in capex. WFE $250B in 2028. | | 06-15 | Barclays · O'Malley / Rand | valuation…
- `TOKYOELEC.md` — …treet keeps raising — UBS/Arcuri models WFE TAM ~$200B CY27 / ~$250B CY28 and says the buy side is "not there" ([semicap-wfe](th…
- `TSM.md` — …der (SpaceX AI capex ~$1.1T/5yrs, ~20%/~$225B to Terafab, ~$135B WFE/5yrs). Cuts mixed for TSMC: near-term it validates that TSM…
- `themes/hbm-memory.md` — …to be the limitation"; UBS raised 2028 WFE to $250B and floats 2029 into the $300B range, with memory not enter…

## Hyperscaler / AI-datacenter capex CY25 / CY26 / CY27  `hyperscaler-capex`

_Aggregate capex of the big US hyperscalers — ALWAYS state the basket (top-4 = MSFT/AMZN/GOOGL/META; five-name adds ORCL)._

**Canonical:** Top-4: ~$410B 2025A -> ~$700-725B 2026E (+~75%) -> ~$1.1T 2027E (JPM AI Capex 2.0). Five-name consensus: ~$700B 2026 / ~$900B+ 2027. Buy-side 2027 bogey ~$1.2T ('could be 1.3-1.4', Jefferies). Constraint is power/physical buildout, not demand.

> ⚠️ **Scope:** Top-4 vs five-name basket differences masquerade as revisions. GOOG-only: ~$350B 2027 / ~$375B 2028 (MS Nowak 2026-06-29).

| Value | Source | Date | Scope |
|---|---|---|---|
| top-4: ~$410B 2025A / ~$700-725B 2026E / ~$1.1T 2027E | JPM Sur, AI Capex 2.0 | 2026-06-16 | top-4 |
| ~$1.2T 2027 buy-side bogey ('could be 1.3-1.4') | Jefferies power/hyperscalers | 2026-05-08 | buy-side bogey |
| five-name consensus ~$700B 2026 / ~$900B+ 2027 | BBG / house | 2026-06-11 | five-name |
| GOOG ~$350B 2027 / ~$375B 2028 (~9 GW incremental 2028) | MS Nowak | 2026-06-29 | GOOG only |

**Debate:** Level agreed near-term; the debate is 2027+ durability (see macro-cycle: bubble vs supercycle).

**Unreconciled sightings** (pages matching this metric, not in the ledger's `cited_in`):
- `AMAT.md` — …e of SPE suppliers."** SpaceX AI capex ~$1.1T/5yrs, ~20% (~$225B) to Terafab; at 60% capex-to-WFE → **~$135B WFE over 5yrs (~= this year's entire glob…
- `ANTHROPIC.md` — …stors that would value it at as much as $900bn** in a ~$30bn tender offer just one month after OpenAI's M…
- `INTC.md` — …gles). Broader thesis: SpaceX AI capex ~$1.1T/5yrs, ~20% (~$225B) to Terafab; at 60% capex-to-WFE → ~$135B WFE over 5yrs (~= this year's entire global…
- `KLAC.md` — …$50B/yr WFE spender** (SpaceX AI capex ~$1.1T/5yrs, ~20%/~$225B to Terafab, 60% capex-to-WFE → **~$135B WFE over 5yrs ≈ the entire global WFE TAM…
- `LRCX.md` — …$50B/yr WFE spender** (SpaceX AI capex ~$1.1T/5yrs, ~20%/~$225B to Terafab, 60% capex-to-WFE → **~$135B WFE over 5yrs ≈ the entire global WFE TAM…
- `MSFT.md` — …364B CY25 (Top-4), funded largely from ~$700B/yr OCF, with AI/DC issuers now ~14.5% of the JULI IG index…
- `NVDA.md` — …venue exiting 2026," MS 2027 hyperscale capex chart lifted $950B→$1.1T (panel thinks ~$1.5T incl. SpaceX/neoclouds). - **Hardware…
- `OPENAI.md` — …re-asserted with GPT-5.5; TAM seen at **$700bn+ by 2030** across consumer/hardware/ads/enterprise (JPM in…
- `SAMSUNG.md` — …ory cost; premium/QD-OLED strategy. - **Capex/return:** Q1 capex KRW 11.2tn (DS 10.2tn); 2026 "substantial y/y increase." Quarterly di…
- `STX.md` — …n FY25; demand is driven by hyperscaler capex (FY25 10-K). Top-3 CSP RPO of $1.1T concentrates both upside and risk. - **Double-ordering / ab…
- `TSM.md` — …ial new >$50B/yr WFE spender (SpaceX AI capex ~$1.1T/5yrs, ~20%/~$225B to Terafab, ~$135B WFE/5yrs). Cuts mixed…
- `VRT.md` — …in 2024 → >$500bn 2025E, +23% CAGR to >$900bn by 2028, of which **Electrical equipment ~$18bn and Therma…
- `VST.md` — …FCF yield. Hyperscaler capex tailwind: >$700B in 2026, ~+50% YoY (Q4 FY25); Jefferies flags +$0.5T of CY2…
- `themes/ai-tam-bofa.md` — …](custom-asic-tpu.md) (accelerator $1.0→$1.2Tn, NVDA/AVGO/AMD split), [hyperscaler-capex](hyperscaler-capex.md) (demand envelope), [ai-datacenter-po…
- `themes/hbm-memory.md` — …21% YoY; memory to >50% of CSP hardware capex; memory TAM to $1.3trn 2027 (JPM · Gokul Hariharan, "Asian Semis / May WSTS", 20…
- `themes/semicap-wfe.md` — …disk (`ued46938.html`): sizing chain (~$1.1T SpaceX AI capex → ~$225B Terafab → ~$135B WFE over 5yrs ≈ entire global WFE…

## AI datacenter power (GW) — facility GW vs IT-load GW vs 800V-debate GW  `ai-dc-power-gw`

_THREE DISTINCT BASES — never mix: (1) facility GW deployed/added (grid + on-site); (2) IT-load GW (compute load in racks); (3) 800V-transition GW (subset of IT load moving to 800VDC)._

**Canonical:** Facility: ~14-16 GW built 2026 / ~20 GW 2027 vs ~40-45 GW proposed (Jefferies satellite tracking, 50% haircut); ~138 GW capacity through 2030 (JPM). IT-load: ~300 GW by 2030 (+25% CAGR, JPM/Omdia) or ~240-280 GW global (JPM First Principles). 800V debate: Citi models 9 GW -> 21 GW 2025-30 — a SUBSET, not total deployment.

> ⚠️ **Scope:** STANDING RULE: the 800V notes' GW figures (IT load ~300 GW, Citi 9->21 GW) must NOT be folded into total-GW-deployed answers. Citi's 9->21 GW is the AI-specific 800V-relevant increment.

| Value | Source | Date | Scope |
|---|---|---|---|
| ~14-16 GW built 2026 / ~20 GW 2027 vs ~40-45 GW proposed (50% haircut) | Jefferies / SinMax / Industrial Info satellite tracking | 2026-06-22 | facility GW added |
| ~138 GW DC capacity through 2030 (base case) | JPM AI Capex 2.0 | 2026-06-16 | facility GW cumulative |
| ~9.4 GW US leased 1Q26 (5x y/y) / ~11 GW near-term pipeline | TD Cowen | 2026-05-19 | facility GW leased |
| ~21 GW built in prior 25 years vs ~40 GW of NVDA chips into US 2025-2030 | Cantor (CoreWeave) | 2026-06-18 | historical context |
| ~300 GW IT load by 2030 (+25% CAGR, >35 GW/yr new) | JPM 800V / Omdia | 2026-06-09 | IT-LOAD — 800V debate, keep separate |
| ~240-280 GW global by 2030 (US >160 GW, ~2x 2025's ~115 GW) | JPM First Principles: AI Power Infrastructure | 2026-06-25 | IT-LOAD — 800V debate, keep separate |
| 9 GW -> 21 GW 2025-30 (Citi model) | Citi 800V power | 2026-06-15 | 800V-DEBATE GW — subset of IT load, keep separate |

**Debate:** No numeric conflict — the risk is basis conflation. Any new GW datapoint must be labeled facility / IT-load / 800V-subset before it enters a page.

**Unreconciled sightings** (pages matching this metric, not in the ledger's `cited_in`):
- `CEG.md` — …x 2.0", 2026-06-16):** JPM now models **138 GW of US data-center capacity growth through 2030** (up from 1…
- `GEV.md` — …s raised chip forecast (208GW of global IT load 2026-30 — AI-accelerator GW deployed/yr ~4x from ~15-17GW in CY25 to ~58-60GW by CY30 —…
- `TLN.md` — …ackdrop is supportive: JPM now models **138 GW US DC capacity growth through 2030** (up from 122 GW) withi…
- `VST.md` — …'s load-growth thesis: JPM now models **138 GW of US DC capacity growth through 2030** (up from 122 GW) wi…

## AI compute revenue / rental rate per GW  `rev-per-gw`

_Annualized $ revenue (or rental rate) per GW of AI compute capacity — state chip type (ASIC vs merchant GPU) and whether it is a rental rate or realized revenue. Distinct from facility BUILD cost per GW._

**Canonical:** Rental/revenue per GW of compute: Trainium <$10B/GW (Anthropic/OpenAI); merchant GPU ~$12-13B/GW (neocloud & AWS, pre-2H26 shortage); premium GPU ~$25B/GW (~$25M/MW/yr, SpaceX–Google deal). MS pegs 1P merchant TPU at ~$20B rev/GW (20% GM base). Colocation POWER-ONLY rent: ~$60/kW-month historically -> ~$120-160 typical now, up to ~$200 (weak-credit tenant + good DC), as low as ~$80-100 (India / mid DC / poor grid). Rev/GW is a data-center-QUALITY metric: credit, utilization, networking and speed-to-market drive a ~2x spread — a top-operator GW ≈ 2x a generic GW.

> ⚠️ **Scope:** THREE distinct bases — never mix: (a) compute rev/rental $/GW (ASIC vs GPU, the monetization/quality metric); (b) colocation $/kW-month = power+shell only, NOT compute; (c) facility BUILD cost ~$30-40B/GW (ASIC) vs ~$50B/GW (NVDA-GPU infra) — see custom-asic-tpu. A $/kW-month figure ×12×1e6 ≈ $/GW-year only for the power-shell layer, not the compute.

| Value | Source | Date | Scope |
|---|---|---|---|
| Trainium <$10B/GW rental to Anthropic/OpenAI (floor mechanism; cancellable if it underperforms) | SemiAnalysis / Dylan Patel (Sequoia 'Training Data') | 2026-06-30 | ASIC rental rate |
| merchant GPU ~$12-13B/GW rental (neocloud & AWS, pre-2H26 shortage) | SemiAnalysis / Dylan Patel (Sequoia 'Training Data') | 2026-06-30 | GPU rental rate |
| premium GPU ~$25B/GW (~$25M/MW/yr) — SpaceX–Google deal | SemiAnalysis / Dylan Patel (Sequoia 'Training Data') | 2026-06-30 | premium GPU rental |
| colo power-only ~$60/kW-mo historical -> ~$120-160 typical, up to ~$200 (weak credit + good DC), ~$80-100 (India / mid DC) | SemiAnalysis / Dylan Patel (Sequoia 'Training Data') | 2026-06-30 | colocation $/kW-month (power+shell only) |
| data-center quality: a top-operator GW ~2x a generic GW; Google runs ~1.5 GW hardware in a 1 GW DC (power-sloshing + utility oversell) | SemiAnalysis / Dylan Patel (Sequoia 'Training Data') | 2026-06-30 | quality / utilization spread |
| 1P merchant TPU ~$20B rev/GW at 20% GM base case | MS Nowak (ALPHABET) | 2026-06-29 | merchant TPU realized rev/GW |

**Debate:** Rev/GW is emerging as a data-center-quality metric: ASIC (<$10B) < merchant GPU ($12-13B) < premium operator ($25B). The spread reflects credit quality, utilization, networking and speed-to-market — not just chip type. Watch whether the 2H26 GPU shortage pushes realized GPU rev/GW above the $12-13B pre-shortage mark.

**Unreconciled sightings** (pages matching this metric, not in the ledger's `cited_in`):
- `AMD.md` — …GW**, of which **AMD revenue is $15-20B/GW** ($14-18B compute, ~$2B networking), and lifts AMD GPU uni…
- `AMZN.md` — …**lowest cost per incremental GW: ~$25bn/GW in 2026 (vs Google $37bn, Meta $45bn)**, reflecting AWS's s…
- `ANTHROPIC.md` — …nAI at sub-$10bn per GW/yr, vs ~$12–13bn/GW for GPUs (pre the last six months' shortage) and ~$25bn/GW…
- `ARM.md` — …-18, $300): agentic AI = ~120M CPU cores/GW, ~4x a traditional data center; Arm holds ~50% CPU share am…
- `AVGO.md` — …cks… all a chip business only" — content/GW rises as CPU cores/HBM embed into XPUs (agentic). - **AI XP…
- `CRWV.md` — …3 of CRWV backlog tied to Meta; $40-60bn/GW deal pricing; ~29% hyperscaler cash ROIC (2026-07-01). Bern…
- `GEV.md` — …ts tracked (>$2.5tn of US spend at ~$55mm/MW), GEV equipment anchors several — **Homer City Energy Campu…
- `META.md` — …nt capacity partnerships valued at ~$50B/GW (Citi, 2026-07-01). **Morgan Stanley (Brian Nowak et al.) r…
- `NBIS.md` — …cl. NBIS; compute-deal pricing ($40-60bn/GW annually, 30-60%+ premium to spot), hyperscaler cash ROIC ~…
- `NVDA.md` — …B networking) — roughly 2x AMD's $15-20B/GW capture. NVDA GPU unit shipments modeled **6.2M (2025) → 8.…
- `OPENAI.md` — …+ Anthropic at ~15GW in F28 at ~$15-17bn/GW (AVGO call, 2026-06-05). AMD signed OpenAI to a ~6GW / ~$10…
- `ORCL.md` — …Lancium, fully contracted by ORCL; ~$13mm/MW ex-IT); Frontier / Shackelford County TX (1.4 GW, Vantage,…
- `WMB.md` — …rclays pegs implied build economics ~$4mm/MW including supporting gas infra for Prometheus, and estimate…
- `themes/ai-datacenter-power.md` — …ter capacity 27→39→57 GW (2025→27); cost/GW spread $25-45bn; capacity deals >$40bn/GW (BofA "Raising In…
- `themes/hyperscaler-capex.md` — …~$1T CY2030 ⇒ **24.2GW of DC at ~$31.3B/GW**; GS's $1T-hyperscaler-capex-2027 with ~40-50% to memory a…
- `themes/tokenmaxxing.md` — …quadruple peers' revenue-per-MW** (~$50B/GW of annual revenue; **200MW ≈ >$10B/yr**), with a 90-day bil…

## HBM — capacity, pricing, allocation, sold-out claims  `hbm-cycle`

_HBM wafer capacity, $/GB or $/Gb pricing (state which), allocation priority, sold-out horizon._

**Canonical:** Sold out CY26 incl. HBM4 (Micron Q1 FY26). Capacity ~473k wspm end-26E -> ~668k end-27E (SemiAnalysis). Pricing: NVDA HBM ~$17-18/GB 2026 -> $30-32/GB 2027, +70-80% (Redburn); blended ASP +~30% (JPM/Micron). Live tension: general-server DRAM overtook HBM as allocation priority #1 (Redburn/TrendForce) yet HBM pricing still marches higher. 2027 supply revised 60B -> 50B Gb-equiv on allocation, not demand (Redburn).

> ⚠️ **Scope:** $/GB (stack) vs $/Gb (die) are ~8-16x apart — always state units. TAM frames: $35B'25 -> $100B'28 (Micron/JPM) vs $168B CY30 (BofA) are different horizons, both valid.

| Value | Source | Date | Scope |
|---|---|---|---|
| sold out CY26 on price and volume, incl. HBM4 | Micron Mehrotra, Q1 FY26 | 2025-12-17 | sold-out |
| ~123k -> ~331k -> ~473k -> ~668k wspm (end-23/25/26E/27E); HBM ~35% of DRAM wafer cap end-27E | SemiAnalysis Memory Mania | 2026-02-06 | capacity |
| NVDA HBM ~$17-18/GB 2026 -> $30-32/GB 2027 (+70-80%) | Redburn Conor | 2026-06-23 | $/GB stack pricing |
| blended HBM ASP +~30% next year (~10% like-for-like + mix) | JPM / Micron Jay | 2026-05-28 | blended ASP |
| general-server DRAM now allocation #1, HBM #2 (4-yr reversal); 2027 HBM supply 60B -> 50B Gb-equiv | Redburn / TrendForce | 2026-06-23 | allocation |
| HBM TAM $35B 2025 -> $100B 2028 (~40% CAGR) | Micron / JPM | 2026-05-28 | TAM to 2028 |
| HBM TAM $35B CY25 -> $168B CY30 (+37% CAGR) | BofA Arya, AI 2030 | 2026-05-13 | TAM to 2030 |

**Debate:** Allocation deprioritization (Redburn) vs pricing-marches-higher (JPM/TrendForce). Watch HBM4 LTA finalization (~90-100% up vs last year's LTA).

**Unreconciled sightings** (pages matching this metric, not in the ledger's `cited_in`):
- `AMD.md` — …cron sourcing (Citi, 2026-06-29); watch HBM/DRAM allocation as a gate on the GPU ramp and 2H Client/Gaming. - **Q2 FY26…
- `ARM.md` — …customers can't place a TSMC PO without HBM allocation Arm can't help secure), so "AGI revenue will be more about…
- `ASML.md` — …e guide) | | **Memory / DRAM** | Memory HBM/DDR "sold out" '26, tight thru '26 | UBS: ASML ~30% of DRAM WFE dollars (…
- `AVGO.md` — …x drags consolidated GM toward low-70s; HBM pass-through pricing an added headwind, now quantified at ~$2.5k of a ~$12k TPU…
- `KLAC.md` — …" (Scemama/BofA, 2026-06-08), so a DRAM/HBM pricing wobble hits the multiple. UBS is the explicit skeptic on KL…
- `LRCX.md` — …conference wrap, 2026-06-08), so a DRAM/HBM pricing wobble hits the group. The dissenting fundamental call is o…
- `MU.md` — …nly 50-66% of key-customer demand, CY26 HBM sold out | | **Key suppliers** | TSMC (HBM4 base die, N12/N3) + IP p…
- `OPENAI.md` — …g" (2026-06-29) — Jalapeño specs (216GB HBM3e, ~740mm², ~700W, TSMC 3nm, ASP ~$15k, ~50% lower cost / 40% lower power vs Blackwell, 9-mo…
- `SAMSUNG.md` — …s Samsung/SK/Micron divert capex toward HBM and smaller players are cash-constrained — supportive of pricing (MS AI NAND overview; Phison 2Q25). - **HBM:** first to mas…
- `SKHYNIX.md` — …demand epicentre of the AI capex cycle: HBM has been "sold out since 2023," 2026 DRAM/HBM volume is contracted out (Q3 202…
- `SNDK.md` — …5.43/$243.73 (adj P/E 7.1x)   - Mizuho "HBM4e Ramping / Sizing Agentic AI / HBF-LTAs" (2026-05-27) — SNDK PT $1,825, OW; Gen1 HBF 2H26E on 16-l…
- `themes/cowos-packaging.md` — …mpute die + smaller I/O die, **6x 12-Hi HBM3e = 216GB**, 3nm, ~$15k ASP, ships end-C26 with volume in 2H27 (Jefferies "Revisiting o…
- `themes/custom-asic-tpu.md` — …roadcom charges the hyperscaler for the HBM** — so with HBM pricing rocketing (NVDA $17–18/GB 2026 → $30–32 2027), cutting HBM…
- `themes/cxl-memory-fabric.md` — …e AI memory bottleneck is shifting from HBM allocation to *fabric architecture*, which makes CXL a front-burner th…
- `themes/semicap-wfe.md` — …) and the demand-side beneficiary (DRAM/HBM/NAND pricing + KV-cache NAND tier). | Strongly positive. UBS (Arcuri) PT…

## NVDA GPU units / GW shipped per year  `nvda-units-gw`

_NVDA accelerator unit shipments and implied GW/yr — distinguish GPU units, Vera standalone CPU, Vera-Rubin racks._

**Canonical:** GPU units: 6.2M 2025 -> 8.9M 2026E (+39%) -> 9.9M 2027E (JPM); Fubon '10M+ in 2027' consistent with JPM's 9.9M 2027E. Racks: 54.5k-62k NVL72 2027F (Nomura). Capstone GW frame: ~16 GW/yr sold 2026 -> ~25 GW 2027 (house, NVDA page 2026-06-17) — the bottoms-up cross-check vs JPM units. [Year labels corrected 2026-07-06 — a prior version showed 6.2M as 2026, shifted one year vs the JPM source quoted in NVDA.md.]

> ⚠️ **Scope:** Vera standalone CPU (500k 2026 -> 3M 2027 JPM; 5.75M units 2027 to ASE FoCoS per MS) is NOT the same series as Vera-Rubin racks (~2.0-2.2M units 2026, cut from 2.8-2.9M on HBM4 issues).

| Value | Source | Date | Scope |
|---|---|---|---|
| GPU units 6.2M 2025 -> 8.9M 2026E (+39%) -> 9.9M 2027E; total accelerators 10.1M -> 16.3M -> 23.3M | JPM AI Capex 2.0 (per NVDA.md sec. 'Per-GW economics') | 2026-06-16 | GPU units |
| could ship 10M+ GPUs in 2027 | Fubon | 2026-06-05 | GPU units |
| ~16 GW sold/yr 2026 -> ~25 GW 2027 (house estimate) | Capstone model | 2026-06-17 | GW shipped (house) |
| 54.5k -> 62k NVL72 racks 2027F | Nomura | 2026-06-30 | racks |
| Vera CPU 500k 2026 -> 3M 2027; MS: 5.75M units 2027 (ASE FoCoS) | JPM Jay / MS Asia AI Supply Chain | 2026-06-23 | Vera standalone CPU |

**Debate:** House 25 GW 2027 vs JPM 9.9M units 2027E — reconcile via W/unit assumptions when the Capstone GW model updates. AI Model.xlsx (2026-07-02 save) has 7.6M CY26 / 7.7M CY27 — BELOW JPM's 8.9M/9.9M; CY27 flatness is the open question.

**Unreconciled sightings** (pages matching this metric, not in the ledger's `cited_in`):
- `AVGO.md` — …05-29):** Broadcom's **TPU order book ≈ 6.5M units for next year** (up from a prior ~5.5-6M check); ships ~$2…
- `CRWV.md` — …**CoreWeave contributed two spare GB300 NVL72 racks** to the open-source effort and is named an InferenceX supp…
- `GOOG.md` — …it estimate to 4.2m units for 2026E and 9.1m units for 2027E (2027 raised)** — part of tweaking up HBM procur…
- `TSM.md` — …a structural tailwind: each GW ≈ 7,200 NVL72 racks ≈ ~33k TSMC wafers and ~US$1.0–1.5bn of TSMC revenue (found…
- `themes/humanoids-robotics.md` — …E, $3.91M in 2026E). Industry GB200/300 NVL72 racks: **28,232 (2025E)**, 57,740 cumulative through Q2'26. Top-4…

## CoWoS capacity and NVDA allocation share  `cowos-allocation`

_NVDA's share of TSMC CoWoS capacity; TPU-substrate splits within Google._

**Canonical:** NVDA ~50-55% of TSMC CoWoS 2027 (Fubon ~50%+; Nomura <55% vs NVDA's targeted ~60% — i.e. target likely missed on TPU squeeze). Within Google TPU: AVGO ~66-68% / MediaTek ~32-34% (Nomura).

> ⚠️ **Scope:** The 'targeted ~60%' is NVDA's ask, not an outcome — don't cite it as achieved share.

| Value | Source | Date | Scope |
|---|---|---|---|
| ~50%+ of TSMC CoWoS 2027 | Fubon | 2026-06-05 | NVDA share |
| <55% 2027F, down from targeted ~60% (TPU squeeze) | Nomura | 2026-06-30 | NVDA share |
| AVGO ~66-68% / MediaTek ~32-34% of Google TPU | Nomura | 2026-06-30 | TPU split |

**Debate:** Does NVDA claw back toward 60% or does TPU keep the squeeze on?

**Unreconciled sightings** (pages matching this metric, not in the ledger's `cited_in`):
- `AMAT.md` — …D for GAA | | **Advanced packaging (HBM/CoWoS)** | To >double to >$3B; share above co. avg | HBM among fastest-growing segments | Fastes…
- `AMD.md` — …ors — Sector Keys", 2026-07-02)  **2027 CoWoS allocation ~240k, MI455/MI450 ~1.5mn units (MS · Charlie Chan, "AI…
- `AVGO.md` — …pply chain & foundry capacity (new) - **CoWoS allocation raised:** Fubon (dist. Jefferies) lifts AVGO's total TSM…
- `BESI.md` — …on needs (HBM stacking, logic-on-logic, CoWoS-class 2.5D). AI-related orders were ~50% of total 2025 orders (Q4-25 call, 2026-02-19). Margins are…
- `GOOG.md` — …ASIC-server units both seen +50%+. - **CoWoS allocation reset higher** for TPU 2027 projects (TSMC AP7/AP8 fully…
- `INTC.md` — …execution holes*: EMIB yield well below CoWoS, long-term server-CPU share erosion (UBS) against Redburn's contrarian read (60% in 202…
- `MEDIATEK.md` — …ed TP, citing "TPU upside."** Its 2027F CoWoS-allocation work argues **Google's TPU CoWoS share rises to 26% in 2027 (from 23% in 2026)** — nearly doubling…
- `NVDA.md` — …06-05) checks: NVDA still ~50%+ of TSMC CoWoS allocation in 2027, total NVDA GPU production "could reach 10mn+ in…
- `SAMSUNG.md` — …TPU), 2027 CapEx revised up to ~$78bn, CoWoS to ~220k/mo by end-2027 — implying limited near-term 2nm share leakage to Samsung/Intel; read alongside Gokul's ~5-6% Sams…
- `TSM.md` — …~$170bn/'30, ~$44bn for TSMC · MS Chan: CoWoS 200kwpm/'27 (~60% YoY XPU); CPU becomes a material 2.5D consumer · **JPM Goku…

## AI TAM by 2030  `ai-tam-2030`

_AI datacenter TAM frames — ALWAYS state scope (systems-only vs total infra)._

**Canonical:** BofA ~$1.7T CY30 AI-DC-systems TAM (accelerators ~$1.2T, networking ~$316B, optical ~$88B, HBM $168B). Jensen's '$3-4T end-of-decade AI infra' is a BROADER scope (adds power/grid/software) — not a conflict with BofA.

> ⚠️ **Scope:** Never compare $1.7T (systems) against $3-4T (infra) as if same quantity.

| Value | Source | Date | Scope |
|---|---|---|---|
| ~$1.7T CY30 AI-DC-systems TAM (accel ~$1.2T / networking ~$316B / optical ~$88B) | BofA Arya, AI 2030 | 2026-05-13 | systems TAM |
| ~$3-4T end-of-decade AI infra | NVDA Jensen, Q1 FY27 | 2026-05-20 | broad infra TAM |

**Debate:** Scope discipline only — systems vs infra.

**Unreconciled sightings** (pages matching this metric, not in the ledger's `cited_in`):
- `AMD.md` — …VGO/MU/AMD/MRVL); AI DC TAM CY30 $1.4Tn→$1.7Tn, accelerator TAM ~$1.2Tn (AMD modeled ~5-7% share, GPU $6.…
- `CIEN.md` — …Comms-infra TAM $600bn'25 → $1.1T'26 → $1.7T'30 (Dell'Oro). Pluggables/Cisco flagged as an earnings-powe…
- `CSCO.md` — …wer. Comms-infra TAM $600bn'25→$1.1T'26→$1.7T'30 (Dell'Oro). Light read-through; CSCO not the subject. (M…
- `MSFT.md` — …emi market to $27bn (28% CAGR) inside a $1.7tn AI-DC-systems TAM. Microsoft's own **Maia** custom ASIC ap…
- `NVDA.md` — …rket $7.9bn → $27bn (28% CAGR) inside a $1.7tn AI-DC-systems TAM. This is the distinct source-of-record b…
- `SPCX.md` — …oal is explicitly unproven. Valuation (~$1.7tn+ implied) prices in enormous execution. **NEW:** xAI repor…
- `themes/800v-dc-power.md` — …5mn → $1.8bn (~49% CAGR)**, inside a **~$1.7tn AI-data-center-systems LT TAM**. **Content-per-rack ~25x:…
- `themes/optical-cpo.md` — …CAGR / copper $22bn at +61%), inside a ~$1.7Tn total AI-DC-systems TAM; CPO transceiver TAM is modeled sm…

## Conventional DRAM pricing cadence Q3/Q4 2026  `dram-pricing-2026`

_QoQ contract-price growth for conventional DRAM, 2H26._

**Canonical:** TrendForce REVISED (2026-06-30, supersedes 06-23): +15-20% Q3 / +3-8% Q4 — vs experts +20-25% Q3 (Redburn/Sherman/Edison) and market chatter +30-40%. Direction agreed; magnitude is the debate.

> ⚠️ **Scope:** The 06-23 TrendForce +8-13% Q3 is SUPERSEDED — don't cite it as current.

| Value | Source | Date | Scope |
|---|---|---|---|
| +15-20% Q3 / +3-8% Q4 (revised up) | TrendForce | 2026-06-30 | current base case |
| +20-25% Q3 / +20% Q4 (vs chatter +30-40%) | Redburn / Sherman / Edison experts | 2026-06-23 | expert view |
| +8-13% Q3 / +3-8% Q4 [SUPERSEDED 2026-06-30] | TrendForce | 2026-06-23 | superseded |

**Debate:** Magnitude of 2H26 DRAM hikes: TrendForce conservative vs expert +20-25% vs chatter +30-40%.

**Unreconciled sightings** (pages matching this metric, not in the ledger's `cited_in`):
- `MU.md` — …are-competition reasons. (Her base-case DRAM price view is the market's most conservative: Q3 +8-13% / Q4 +3-8%, with gut-feel upside to Q3 >+20% and Q4 +10-15% — vs…

