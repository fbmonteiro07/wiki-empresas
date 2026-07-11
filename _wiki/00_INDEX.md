# Research Wiki — by company

> 🌐 **Navigable version (offline):** open [`index.html`](index.html) — sidebar by theme + full-text search across all pages. Rebuild: `py E:/.claude/scripts/build_wiki_html.py`.
>
> 📊 **Dashboards** (hub: [`_dashboards/index.html`](_dashboards/index.html)): [edge tracker](_dashboards/edge.html) · [read-through map](_dashboards/readthrough.html) · [catalyst loop](_dashboards/catalysts.html) · [catalyst timeline (Gantt)](_dashboards/gantt.html) · [what changed](_dashboards/diff.html) · [canonical assumptions](_dashboards/assumptions.html) · [book exposure](_dashboards/book.html). Rebuild all: `py "_wiki/_tools/refresh_features.py"`.
>
> 🔎 **Full-corpus search** (reports + calls + briefings + transcripts + Stratechery, not just wiki pages): `py "_wiki/_tools/search.py" <query>` (index: `py "_wiki/_tools/build_search_index.py"`).

_Generated 2026-07-10 by `_tools/build_index.py` from [`_data/index_meta.json`](_data/index_meta.json) (hand-edit the json, not this file) · **100 companies + 2 private AI labs (102 pages)** · one page per ticker synthesizing all co-located sources in `E:\Wiki Felipe`: filings (10-K/10-Q/20-F) + earnings transcripts + investor-day decks + thematic equity calls (`_equity_calls`) + per-ticker roll-up of the email briefings (`_briefings/by-ticker`) + BBG consensus & street-high estimates (`_data/estimates.json`)._

Each page follows the [_TEMPLATE](_TEMPLATE.md): Snapshot · Current state (latest quarter) · Debate (bull/bear + where the sell-side stands, attributed + dated) · Catalysts · Risks · Consensus estimates (BBG) · Sources (links). Archive master index: [../INDEX.md](../INDEX.md). Thematic pages: [themes/00_THEMES.md](themes/00_THEMES.md).

> Attribution is the point: every datapoint carries its source (broker/analyst/call + date). Where on-disk coverage is thin (small-caps, power, Toyota), the page says so explicitly.

## AI — Semis & Compute
| Ticker | Page | One-line thesis |
|---|---|---|
| NVDA | [NVDA](NVDA.md) | Full-stack AI-factory platform at +85% rev; debate is demand sustainability vs ASIC erosion. |
| AVGO | [AVGO](AVGO.md) | #1 custom-ASIC/TPU partner; binary setup on the ">$100B" FY27 guide vs $250-300B FY28 (JPM). |
| AMD | [AMD](AMD.md) | AI-infra long with a server-CPU leg; risk concentrated in MI450 execution. |
| TSM | [TSM](TSM.md) | Sole-source leading-edge foundry (~70% share); pricing headroom vs overseas-fab dilution. |
| ASML | [ASML](ASML.md) | Supply-chain chokepoint (EUV near-monopoly); Street "behind the curve" on 2027/28 vs a 2028 DRAM air-pocket. |
| MU | [MU](MU.md) | Pure-play on AI memory intensity (HBM sold-out CY26); debate = peak earnings vs run-rate. |
| MRVL | [MRVL](MRVL.md) | #2 merchant custom-ASIC (Trainium/Maia) + optical DSP; debate = hyperscaler concentration + 1.6T share. |
| AXTI | [AXTI](AXTI.md) | Most direct InP-substrate bottleneck play (~80% non-China w/ Sumitomo); bull = optical supply oligopoly, bear = China-permit gate + trading-vehicle beta. |
| TSEM | [TSEM](TSEM.md) | Specialty foundry re-rating on SiPho/SiGe optical; $1.3B 2027 SiPho commit (NVDA-anchored per FinTwit); bear = ramp/concentration. SIG Positive $330. |
| POET | [POET](POET.md) | Pre-revenue EOI/CPO optionality de-risked by $50M Lumilens order; bear = valuation vs FOCI + CPO timeline slip. Thin coverage. |
| INTC | [INTC](INTC.md) | Binary IDM turnaround; 18A yielding, but the equity is a call option on the first big external foundry customer. |
| IFX | [IFX](IFX.md) | #1 power/auto-semi IDM; cyclical recovery + 800V AI-datacenter-power ramp (NVIDIA anchor); bear = DC-power share loss. |
| SMIC | [SMIC](SMIC.md) | China's national-champion mature-node foundry; self-sufficiency proxy vs mature-node price-war + EUV/export-control ceiling on its DUV 7nm push. |
| MEDIATEK | [MediaTek](MEDIATEK.md) | World's largest mobile-SoC vendor pivoting into a data-center custom-ASIC house (Google TPU v8t/v9/v10 roadmap); JPM sees DC ~30% of rev 2027 → ~60% 2028; GS PT NT$6,800. TWD, no SEC. |

## AI — Hyperscalers & Software
| Ticker | Page | One-line thesis |
|---|---|---|
| MSFT | [MSFT](MSFT.md) | AI ARR >$37B/+123%; swing is capex (CY27 ~$276B) vs Azure revenue + OpenAI concentration. |
| AMZN | [AMZN](AMZN.md) | AWS re-acceleration (+28%) + in-house silicon (Trainium); debate = $200B capex/ROIC. |
| GOOG | [GOOG](GOOG.md) | Full-stack compounder (Search +19%, Cloud +63%); debate is valuation, not fundamentals. |
| META | [META](META.md) | Fastest grower in Mag7 ex-GPU; bear = capital intensity and negative incremental ROIC. |
| ORCL | [ORCL](ORCL.md) | Turned into an AI-infra hyperscaler (RPO $638B/+363%); bear = dot-com-peak capex/sales + dilution. |
| NOW | [NOW](NOW.md) | Beat-and-raise (cRPO +21%) + agentic pivot to consumption; on-disk transcripts are paraphrased (fidelity). |

## AI labs (private)
| Ticker | Page | One-line thesis |
|---|---|---|
| ANTHROPIC | [Anthropic](ANTHROPIC.md) | Private frontier lab (Claude); enterprise/coding leadership + Amazon/Google compute; ~$40B+ ARR. No public financials. |
| OPENAI | [OpenAI](OPENAI.md) | Private frontier lab (ChatGPT/GPT); scale + distribution vs cash burn + sub-50% share; Microsoft-anchored. No public financials. |

## Semiconductor equipment (semicap)
| Ticker | Page | One-line thesis |
|---|---|---|
| AMAT | [AMAT](AMAT.md) | Broadest-line front-end WFE; share-gainer into a $200B/$250B '27-'28 WFE cycle; bear = memory beta + crowded positioning. |
| KLAC | [KLAC](KLAC.md) | Process-control near-monopoly (~7x peers); only semicap to guide CY27 WFE > CY26; back-half-of-cycle revision story. |
| TER | [TER](TER.md) | Cleanest back-end proxy for AI test intensity (~70% AI); bear = ~2-customer concentration + H1-weighted book. |
| VECO | [VECO](VECO.md) | Specialty process equipment (LSA / ion-beam / MBE / MOCVD); now an Axcelis all-stock merger-arb / ACLS proxy. |
| AIXA | [AIXA](AIXA.md) | Near-monopoly compound-semi MOCVD (~100% InP, >85% GaN); AI-optical inflection (Jefferies Buy €73); thin internal coverage. |
| LRCX | [LRCX](LRCX.md) | Etch/deposition WFE — completes the AMAT/KLAC/LRCX trio; most memory-capex-levered (NAND/HBM). |
| TOKYOELEC | [Tokyo Electron](TOKYOELEC.md) | Broadest-line Japanese WFE (coater/developer ~91% share, dielectric etch >50%); cleanest Japan-listed proxy for leading-edge WFE + HBM packaging. ¥, FYE March. |
| ADVANTEST | [Advantest](ADVANTEST.md) | #1 ATE in a duopoly with Teradyne; ~80% of SoC test is HPC/AI and effectively sole SoC tester at the GPU/CoWoS leaders — levered to test intensity, not wafer starts. ¥. |
| DISCO | [DISCO](DISCO.md) | Near-monopoly precision dicing/grinding/polishing (~70-80% share of HBM wafer-thinning tools) + consumables; sixth straight record year on AI GPU/HBM. ¥, FYE March. |
| BESI | [BESI](BESI.md) | Hybrid-bonding / TCB leader for HBM and 2.5D/3D stacking (AI ~50% of 2025 orders, GM 63-66%); AMAT hardware partner on the high-end HB roadmap. |

## Memory & storage
| Ticker | Page | One-line thesis |
|---|---|---|
| SAMSUNG | [Samsung](SAMSUNG.md) | Cheapest way to own the memory super-cycle; HBM4 catch-up vs SK Hynix + foundry optionality. ₩, no SEC. |
| SKHYNIX | [SK Hynix](SKHYNIX.md) | #1 HBM, NVDA's primary supplier, sold out through 2026; bear = HBM4 commoditization. ₩, no SEC. |
| KIOXIA | [Kioxia](KIOXIA.md) | Cleanest listed NAND/SSD-cycle proxy; no DRAM/HBM offset on the downturn. ¥, no SEC, IPO'd 2024. |
| SNDK | [SanDisk](SNDK.md) | Post-spin pure-play NAND on AI storage; price-driven blowout + $42B LTA backlog vs blowoff-top risk. |
| WDC | [WDC](WDC.md) | Pure-HDD post-SanDisk-spin; nearline exabyte growth + HAMR; the "1B" to Seagate's "1A". |
| STX | [STX](STX.md) | HAMR/Mozaic front-runner in a supply-constrained nearline cycle; pricing escalators into CY27/28. |

## Analog & processors
| Ticker | Page | One-line thesis |
|---|---|---|
| ADI | [ADI](ADI.md) | Highest-quality large-cap analog; industrial recovery + datacenter-power (Empower); crowded/premium. |
| TXN | [TXN](TXN.md) | Crowded analog long; 300mm capex→FCF inflection + 800V DC-power share; valuation the bear (GS Sell). |
| QCOM | [QCOM](QCOM.md) | High-FCF handset franchise eroding (Apple modem); re-rating hinges on auto/IoT/PC diversification. |
| ARM | [ARM](ARM.md) | Upstream IP toll on every SoC; ARMv9/CSS royalty + >$100B server-CPU TAM; own-silicon pivot the risk. 20-F filer. |
| NXPI | [NXP](NXPI.md) | Highest auto-beta analog/embedded; content-per-vehicle + datacenter doubling; concentration the risk. |
| MCHP | [MCHP](MCHP.md) | Textbook deep-cyclical MCU/analog recovery; GM 54%→62%; supply-gated, already re-rated. |
| ON | [onsemi](ON.md) | Bottoming auto/SiC power IDM + AI-DC-power (800V) kicker; share not TAM (Citi Neutral vs TXN). |

## Optical / Networking
| Ticker | Page | One-line thesis |
|---|---|---|
| ANET | [ANET](ANET.md) | Best-positioned merchant AI-Ethernet name; risk = 2H26 backlog drawdown + rich multiple. |
| CIEN | [CIEN](CIEN.md) | Optical/DCI leader; demand outruns supply, debate purely valuation (~85x NTM). |
| COHR | [COHR](COHR.md) | InP chokepoint in AI interconnect; NVIDIA stake + CPO deal; bear is relative vs LITE. |
| LITE | [LITE](LITE.md) | US photonics pure-play (rev +90%); demand isn't the question, supply/execution is. |
| AAOI | [AAOI](AAOI.md) | Volatile small-cap with in-house InP fab; 2027 projection trading on FinTwit conviction. |
| GLW | [GLW](GLW.md) | Re-rate to AI-infra (Optical +36%, Meta/Nvidia LTAs); bear = valuation + CPO payoff 2028+. |
| CSCO | [CSCO](CSCO.md) | Incumbent re-rating to AI-infra (orders +35%); bear prefers ANET, flags pull-forward. |
| CRDO | [CRDO](CRDO.md) | AI-connectivity pure-play — active-copper (AEC) + SerDes/optical DSP; ~68% GM, hyperscaler-concentrated. |
| ALAB | [ALAB](ALAB.md) | Scale-up connectivity (PCIe/CXL retimers + Scorpio fabric); >$1k content/accelerator; concentration + rich multiple. |

## Power & Energy
| Ticker | Page | One-line thesis |
|---|---|---|
| CEG | [CEG](CEG.md) | Owns what the AI-power cycle is short: 24/7 carbon-free nuclear; risk is PPA timing. |
| VST | [VST](VST.md) | Largest US merchant power turning into an AI-power play; debate is pace, not direction. |
| TLN | [TLN](TLN.md) | PJM merchant IPP (Susquehanna nuclear + AWS PPA); risk = concentration + co-location regulation. |
| GEV | [GEV](GEV.md) | Cleanest AI-power earnings-revisions story (orders +71%); bear = order peak + Wind. |
| PWR | [PWR](PWR.md) | Labor pick-and-shovel on the grid/data-center super-cycle (backlog $48.5B). |
| WMB | [WMB](WMB.md) | Gas-midstream compounder (Transco + Power Innovation); debate = valuation + PI earnings quality. |
| AGX | [AGX](AGX.md) | EPC pure-play on the firm-power super-cycle (backlog ~79% gas); nil coverage on disk. |
| ETN | [ETN](ETN.md) | "AI-factory power" electrical name (switchgear/busway); RMT sharpens portfolio; bull = capex/800V, bear = Q1 margin trim. |
| BE | [BE](BE.md) | On-site SOFC fuel cells for DC power (Nebius/Google); bull = grid bottleneck, bear = Redburn Sell + Delta/Ceres competition. |

## Power components & datacenter infra
| Ticker | Page | One-line thesis |
|---|---|---|
| AEIS | [AEIS](AEIS.md) | RF/DC power for semicap (~30% share) + AI-DC power shelves; EPS power to high-teens; debate = DCC lumpiness + 800V positioning. |
| APH | [APH](APH.md) | AI-interconnect compounder; 800V busbar/connector content + CommScope optical; debate = copper terminal value. |
| TEL | [TEL](TEL.md) | TE Connectivity — connector power/signal AI-DC content (AI rev →~$2.4bn FY26); auto-mix the drag. |
| NVT | [NVT](NVT.md) | nVent — AI-DC power + liquid cooling (DC ~$1B, backlog $2.6B); NVIDIA CDU partner; order lumpiness. |
| VRT | [VRT](VRT.md) | Vertiv — cleanest AI-DC power+cooling proxy; co-designs NVIDIA 800VDC; $15B backlog; order opacity. |
| FLEX | [FLEX](FLEX.md) | EMS re-rating to AI-DC power (Anord Mardix) + JetCool cooling; CPI spin Q1-CY27; margin-dilutive near-term. |
| WOLF | [WOLF](WOLF.md) | Wolfspeed — post-Ch11 SiC; 800V datacenter call-option but negative GM + restructuring overhang. |
| NVTS | [NVTS](NVTS.md) | Navitas — GaN/SiC; binary on the NVIDIA 800V design win (rev 2027); cash burn + small-cap volatility. |
| POWI | [POWI](POWI.md) | Power-conversion ICs; FinTwit NVDA 800VDC "main stages" partner, but no capital catalyst + consumer drag. Thin coverage. |
| AOSL | [AOSL](AOSL.md) | Power MOSFET/IC small-cap in the 800VDC Rubin-rack basket; design-win unconfirmed, negative EPS. Thin coverage. |

## Software / security / internet
| Ticker | Page | One-line thesis |
|---|---|---|
| PANW | [PANW](PANW.md) | Cybersecurity platformization land-grab + agentic SecOps; debate = organic vs M&A-flattered NGS ARR. |
| CRWD | [CRWD](CRWD.md) | Falcon consolidation flywheel + Charlotte AI; net-new ARR re-accel; valuation/crowding + 2024-outage tail the bear. |
| CRM | [CRM](CRM.md) | Agentforce $0→$1B+ ARR is the AI-monetization test case; bear = ~10-13% growth + SaaS-seat-reset (BofA UW $160). |
| RDDT | [RDDT](RDDT.md) | Dual engine: ads + AI data-licensing; binary on Google AI-Overviews referral-traffic cannibalization. |
| SHOP | [SHOP](SHOP.md) | Commerce OS at 30%+ GMV; agentic-commerce binary (TAM-expander vs LLM-storefront disintermediation). |
| PLTR | [PLTR](PLTR.md) | Ontology/"action engine" moat (claimed 5-yr); momentum strong but valuation split (UBS Buy $200 vs DB Hold $200). |
| APP | [APP](APP.md) | AXON AI ad engine; eCommerce inflection + fading META threat the bull, drawn-out eComm ramp the bear (DB Buy $660 / GS Neutral $585). |
| VEEV | [VEEV](VEEV.md) | Life-sciences cloud; Vault CRM migration vs AI-disclosure overhang until Q4 Investor Day (MS EW $215). |

## CDN / Edge cloud
| Ticker | Page | One-line thesis |
|---|---|---|
| NET | [NET](NET.md) | Cloudflare — developer/edge platform + Zero Trust security, AI-inference-at-edge (Workers AI); +34% rev, "agentic-AI-first" ~20% RIF; bull = platform/RPO compounding, bear = valuation + GM mix-down. |
| AKAM | [AKAM](AKAM.md) | Akamai — legacy CDN delivery (declining) pivoting to Security + Cloud Compute; $1.8B 7-yr frontier-model infra deal re-accelerates growth to double-digits 2027 (BofA upgrade Buy $175). |
| FSLY | [FSLY](FSLY.md) | Fastly — edge-delivery turnaround diversifying into Security + Compute (Sec +47%); first profitable year; bear = customer concentration (TikTok/top-10) + Cloudflare/hyperscaler competition. |

## Systems & neoclouds
| Ticker | Page | One-line thesis |
|---|---|---|
| DELL | [DELL](DELL.md) | AI-server integration winner ($53B backlog, $60B FY27 guide); bear = thin AI-server margins + pull-forward. |
| HPE | [HPE](HPE.md) | Multi-segment beat + Juniper synergies; durability debate (GS bull $79 vs MS/Bernstein EW). |
| SMCI | [SMCI](SMCI.md) | Fastest NVIDIA rack integrator + DLC leader; thin assembly margin + governance overhang (Hold). |
| CRWV | [CRWV](CRWV.md) | Highest-visibility GPU neocloud ($99B backlog) but ~$25B high-coupon debt + customer concentration. |
| SANM | [SANM](SANM.md) | EMS re-rating via ZT Systems AMD-rack integration (FY27 $16B+, ~2x FY25); bear = ZT margin/pull-forward (JPM/BofA/SIG all Neutral). |
| NBIS | [NBIS](NBIS.md) | Highest-octane listed neocloud (ARR→$7-9B, NVDA stake); capex burn + circular-financing scrutiny. |
| CEREBRAS | [Cerebras](CEREBRAS.md) | Wafer-scale fast-inference vs NVDA; OpenAI take-or-pay; UAE concentration. Recent IPO, no public consensus. |
| SPCX | [SpaceX](SPCX.md) | IPO'd Jun-2026 (~$75bn, largest ever); Starlink + Launch + AI (ex-xAI: Grok/X/COLOSSUS ~1GW, ~325k GPUs). FY25 rev $17.2bn, net loss ~$(4.9)bn; Musk ~82% vote. Read-through to NVDA/CRDO. |

## Consumer / Internet / Other
| Ticker | Page | One-line thesis |
|---|---|---|
| AAPL | [AAPL](AAPL.md) | Strong franchise + memory-dislocation advantage; bear = AI catch-up + price elasticity. |
| NFLX | [NFLX](NFLX.md) | Clean organic algorithm (12-14% rev, 31.5% margin); near-term setup is a catalyst vacuum. |
| BKNG | [BKNG](BKNG.md) | World's #1 OTA; binary debate on agentic LLMs (TAM expander vs disintermediation). |
| UBER | [UBER](UBER.md) | Winner-take-most demand aggregator (~$10B FCF); everything hinges on the AV binary. |
| SPOT | [SPOT](SPOT.md) | High-quality audio compounder; debate = AI-music monetization (Remix) vs <2% rev 2030. |
| TM | [TM](TM.md) | HEV volume leader generating cash; margin compressed 3 years by tariffs/FX; thin coverage. |
| TSLA | [TSLA](TSLA.md) | Rotating from EV volume to autonomy/robotics re-rate (FSD, Optimus, Terafab); MS EW $415, JPM just to Neutral. |
| MP | [MP](MP.md) | Only scaled ex-China rare-earth/magnet play; de-China "follow the gigawatt" bull vs trade-deal/execution risk (BofA Buy). Thin coverage. |

## EDA & design software
| Ticker | Page | One-line thesis |
|---|---|---|
| CDNS | [CDNS](CDNS.md) | EDA duopoly (with SNPS) + hardware emulation; ~80% recurring, AI-design tailwind; bear = China/export-control exposure + rich multiple. |
| SNPS | [SNPS](SNPS.md) | #1 EDA franchise + Design IP, now multiphysics via the ~$35B Ansys deal; AI-design secular grower; bear = Ansys integration/leverage + China. |
