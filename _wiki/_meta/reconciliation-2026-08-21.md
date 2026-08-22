_Wiki · reconciliation · generated 2026-08-21 · `/run-inbox` scheduled run · 16 sources, 27 company pages + 9 theme dossiers patched._

# Reconciliation — 2026-08-21

Every NEW quantitative datapoint from tonight's ingest, placed against three baselines:

1. **Prior wiki comments** — the most recent mark already on the page (on disk).
2. **Capstone house models** — the `## Capstone estimates (house model)` block, where one exists (12 of 104 pages; NVDA / GOOG / META are the relevant ones tonight).
3. **BBG consensus** — **LIVE**, pulled 2026-08-21 via `E:\bloomberg_api` `bdp()` with `BEST_FPERIOD_OVERRIDE` in `1FY`/`2FY`/`3FY`. Terminal was logged in; **no PENDING columns this run.**

> **Period-basis warning, read before using any table below.** `1FY`/`2FY` resolve to each company's own FISCAL year, not calendar. MU is FY-Aug, NVDA is FY-Jan. A broker's "FY27E" and a `CY2027E` column are **different windows**, and in a steeply rising series the earlier window prints lower — comparing across them manufactures disagreements that do not exist. Tonight that trap was live on MU (see D-1) and was initially got backwards. Where a mark's period label is unverified in the source (Bernstein's MU "2027E"), it is EXCLUDED from like-for-like ranking rather than assumed.

## BBG consensus pull — live `bdp`, 2026-08-21 (upside = cons PT vs spot)

| Ticker | PX_LAST | Cons. PT | 1FY EPS | 2FY EPS | 3FY EPS | Note |
|---|--:|--:|--:|--:|--:|---|
| NVDA US | 214.72 | 307.56 | 8.994 | 13.005 | 16.127 | BMO $340 = +10.5% vs cons PT; EPS in line -> re-rating call |
| MU US | 966.78 | 1,581.01 | 72.778 | 151.678 | 167.966 | BMO $1,300 = -17.8% vs cons PT on in-line EPS -> multiple bear |
| 005930 KS | 270,000 | 490,018 | 48,041 | 70,400 | 76,002 | Citi W450k -8.2% / MS W381k -22.2% vs cons -> both BELOW cons |
| 000660 KS | 1,761,000 | 3,231,945 | 349,876 | 463,074 | 517,438 | no new PT this run; CXMT read-through only |
| CRWV US | 87.85 | 144.74 | −3.899 | −1.692 | 1.376 | Arete $317 = +119.0% vs cons PT -> largest divergence of the run |
| NBIS US | 219.13 | 292.94 | −2.036 | −1.670 | 0.429 | Arete $415 = +41.7% vs cons PT, but capex +66/+94% vs cons too |
| IFX GR | 55.93 | 87.67 | 1.737 | 2.808 | 3.763 | Arete EUR124 (RAISED from 114) = +41.4% vs cons -> the real call |
| TXN US | 264.36 | 328.68 | 8.375 | 10.177 | 12.450 | Arete $381 CUT from $405, yet FY28 EPS +26% vs cons -> compression |
| ADI US | 373.09 | 468.38 | 12.805 | 16.392 | 18.710 | Arete $490 = +4.6% vs cons; prior Arete mark was already $487 |
| 285A JP | 54,320 | 114,935 | 10,225 | 13,146 | 14,660 | China Renaissance JPY55,400 = -51.8% vs cons -> STALE (04-30) |
| SNDK US | 1,596.08 | 2,204.72 | 211.34 | 258.10 | 204.31 | China Renaissance $1,452 = -34.1% vs cons and BELOW SPOT -> STALE |
| PANW US | 357.87 | 367.03 | 3.772 | 4.362 | 4.821 | MS PT carried on page ($320) is now BELOW spot -> refresh needed |
| CRWD US | 191.95 | 212.95 | 1.222 | 1.545 | 1.848 | MS PT carried on page ($172) is now BELOW spot -> refresh needed |
| MRVL US | 237.04 | 271.85 | 4.049 | 6.290 | 9.643 | no new PT; bullish memory->connectivity read-through (unconfirmed) |

---

## DIVERGES — the alpha

### 1. 🔴 MU — BMO initiates Outperform on a target 17.8% BELOW consensus

| Metric | BMO (2026-08-20) | Baseline | Δ |
|---|--:|--:|--:|
| Price target | **$1,300** | BBG cons. PT **$1,581.01** | **−17.8%** |
| FY26E EPS | $73.00 | BBG 1FY (FY-Aug-26) $72.778 | +0.3% |
| FY27E EPS | $151.91 | BBG 2FY (FY-Aug-27) $151.678 | **+0.2%** |
| FY26E revenue | $129,099mm | BBG 1FY $128,187mm | +0.7% |
| FY27E revenue | $248,935mm | BBG 2FY $245,837mm | +1.3% |
| FY26E capex | $29,602mm | BBG 1FY $28,062mm | +5.5% |
| FY27E capex | $40,000mm | BBG 2FY $44,874mm | **−10.9%** |

**The call is a multiple call, not an estimate call.** BMO's earnings are consensus to within 0.3% on both years. The target gap is entirely valuation: BMO applies **8.5x** ("at least a mid-cycle multiple") where the consensus PT implies **~10.4x** on the same FY27 number. So this is an **Outperform rating sitting below the Street's own average target** — a genuinely unusual posture and the cleanest read of the note.

**And it is internally in tension.** The same note carries a **>70% FY26 gross-margin floor** (BMO's prose) — which BMO's own uncorrupted revenue/gross-profit lines imply is really **~80.5% FY26E / ~86.0% FY27E** — while simultaneously holding the **lowest FY-labelled EPS mark on the page** (vs MS FY27 $168, Arete FY27E $175.39). A house bullish on margin and cautious on per-share earnings. **The unresolved variable is therefore the margin→EPS pass-through** (share count, tax, the FY-vs-CY window), not the margin.

⚠️ **Basis discipline:** BMO's $151.91 is the lowest of the *named FY broker marks* but is ~in line with *same-basis consensus*. It diverges from the bullish broker tail, **not from the Street.** Do not rank it against `CY2027E $163.85` — CY27 is a later window and the comparison is invalid. `estimates.json` cannot rebuild an FY-Aug annual line for MU (it holds only 1FQ/2FQ quarterlies plus CY aggregates, and its CY column is a calendar sum mixing forecasts with adjusted actuals); reproducing $151.678 requires the live wrapper with `BEST_FPERIOD_OVERRIDE=2FY`.

**Plausibility question closed.** BMO's FY26E is not a heroic forecast: F4Q26E $50,140mm / $30.81 sits against Micron's own ~$50bn / ~$31 guide, and FY26E is three printed quarters plus that guided one. The ramp is arithmetic.

➜ **Action: MU: treat BMO as a MULTIPLE call, not an estimate call — EPS is consensus to within 0.3% on both years while the $1,300 target sits 17.8% BELOW the $1,581 consensus PT. An Outperform initiated below the Street. The open variable is the margin-to-EPS pass-through, not the margin.**

### 2. 🔴 NVDA — a $340 target on consensus numbers: pure re-rating

| Metric | BMO (2026-08-20) | BBG cons. | Δ | Capstone house | House vs cons. |
|---|--:|--:|--:|--:|--:|
| Price target | **$340** | 307.56 | **+10.5%** | — | — |
| FY27E EPS | $8.97 | 8.994 (1FY) | −0.3% | 2026E $9.30 | +3.4% |
| FY28E EPS | $13.56 | 13.005 (2FY) | +4.3% | 2027E **$15.49** | **+19.1%** |
| FY27E revenue | $396,762mm | 395,318 (1FY) | +0.4% | 2026E $407bn | +3.0% |
| FY28E revenue | $595,705mm | 571,722 (2FY) | +4.2% | 2027E **$661bn** | **+15.6%** |

**Like-for-like and clean:** BMO and MS are both on NVDA's FY-Jan basis over identical periods, and BMO's non-GAAP EPS is matched against MS's consensus-method EPS (not ModelWare), so no calendarisation or GAAP adjustment is involved. BMO vs MS: revenue **+1.0% / −0.6%**, EPS **−0.1% / +3.1%** — against a **$340 vs $288** target gap. **The entire dispersion is the multiple (25x vs ~22x).**

**Operational consequence:** any future PT move on NVDA should be interrogated as a re-rating argument first and an estimate-revision argument second.

**House is the outlier bull:** Capstone 2027E EPS $15.49 is **+19.1% above consensus** and +14.2% above BMO. Direction is consistent (house > BMO > Street) but the house sits alone at the top — that gap is the position, and it rests on revenue ($661bn vs BMO $595.7bn) more than on margin.

**New negative not in the BMO note.** Arete flags NVDA as the **last xPU vendor to vertical power** ("vertical VRM supply is extremely tight… lack of credible suppliers"; TI/ON designed in for relief; Feynman late '28). Rubin Ultra now carries **four independent constraints — rack thermals, PCB midplane, HBM stack height, VRM — against zero estimate cuts.** Most testable thing on the page into the print.

➜ **Action: NVDA: interrogate any future PT move as a re-rating argument first and an estimate-revision argument second — BMO vs MS is like-for-like on FY-Jan with EPS within 3.1%, so the entire $340-vs-$288 gap is the multiple (25x vs ~22x). House 2027E EPS $15.49 is +19.1% vs consensus and stands alone at the top.**

### 3. 🔴 SAMSUNG — MS's own capex undercuts Citi's dividend math

| Metric | Source | Baseline | Δ |
|---|--:|--:|--:|
| Citi TP | **W450,000** | BBG cons. PT W490,018 | **−8.2%** |
| MS PT | **W381,000** (unch) | BBG cons. PT W490,018 | **−22.2%** |
| MS model FY26E revenue | W729,299bn | BBG 1FY W729,874bn | **−0.1%** |
| MS model FY27E revenue | W1,059,408bn | BBG 2FY W975,122bn | +8.6% |
| **MS model FY26E capex** | **W109,872bn** | **BBG 1FY W78,475bn** | **+40.0%** |
| KB 2026 OP | KRW381tn | MS model FY26E 388.7tn | −2.0% |
| KB 2027 OP | KRW575tn | MS model FY27E 629.0tn | −8.6% |

**The cross-source tension is the finding.** Citi's bull case is a ~W30tn quarterly dividend *sustained* to ~W120tn annualised, underwritten by the 50%-of-2024-26-FCF framework. But Morgan Stanley's own model carries FY26E capex **40% above consensus** (W109.9tn vs W78.5tn) — and the FY24A/25A historicals match JPM within 0.3%, so this is **not a definitional artefact.** If MS's capex is right, the FCF funding Citi's dividend arithmetic is materially lower than the Street assumes. **Two houses, one framework, incompatible cash flows.**

**Both new targets are BELOW consensus.** Neither house went to Street-high on the announcement — consensus (W490,018) is already above both. The board disclosure is being read as *confirmation, not upgrade*.

**MS reaffirmed without marking its own dividend rows to the filing.** MS prints FY26E DPS W4,090 → ×~6,607mn shares ≈ **W27tn for the whole year**, *less than the ~W30tn announced for 3Q26 alone*. Independently, W120tn ÷ 6,607mn ÷ W281,500 = **6.45%**, reproducing Citi's 6.4% yield exactly — so Citi's arithmetic checks and MS is the stale input. On the residual W60-80tn mix, BofA's 08-20 dividend-first mechanic sides with Citi: **2-1, MS the outlier.**

**Wider dispersion nobody is arguing about:** FY27E OP runs **JPM W549tn → KB W575tn → cons W571-584tn → MS W629tn**, a ~15% spread.

⚠️ **Anchored on net income / operating profit throughout**, per the Samsung common-vs-preferred share-count trap. MS's "EPS for consensus" W48,652 vs BBG 1FY W48,041 (+1.3%) lines up only because MS computed it on the consensus basis; it is not a clean like-for-like and is not used as a baseline here. Note also the MS rating-history line "005935.KS … W207,000" is the **preferred** share, a different security.

**Not routed:** the +40% capex divergence was deliberately NOT pushed to AMAT/LRCX/KLAC/ASML or `themes/semicap-wfe`. The Samsung-over-Hynix WFE mix call was overturned 2026-08-20 and this needs the MS Hynix model on the same annual basis first. **Open verification item.**

➜ **Action: SAMSUNG: MS model FY26E capex W109.9tn is +40% vs consensus W78.5tn and the FY24A/25A historicals tie to JPM within 0.3%, so it is not a definitional artefact. If MS is right, the FCF underwriting Citi's ~W120tn annualised dividend is materially lower than the Street assumes. Both new PTs sit BELOW the W490k consensus. Do NOT route the capex delta to semicap until the MS Hynix model is on the same annual basis.**

### 4. 🔴 CRWV — the run's largest outright divergence

| Metric | Arete (2026-08-21) | Baseline | Δ |
|---|--:|--:|--:|
| Price target | **$317** (raised from $303) | BBG cons. PT $144.74 | **+119.0%** |
| Revenue '28E | — | — | **+26% vs consensus** |
| Revenue '29E | — | — | **+37% vs consensus** |

Arete says "materially ahead of consensus"; Bloomberg confirms it emphatically. Implied **8.2x EV/operating income '29E**. Consensus has CRWV loss-making until 3FY (1FY −$3.90, 2FY −$1.69, 3FY +$1.38), so the target rests on a profitability crossover the Street has not yet underwritten.

Mechanism is priced, not asserted: **+25% July price rise** plus a 5-10ppt Vera Rubin margin uplift, framed as price captured *beyond* the ~20% higher GPU capex/MW implied by the 70-80% rack premium and ~50% higher power draw.

⚠️ Source-internal inconsistency logged, not silently resolved: Arete's ticker table and disclosure page say the prior PT was **$303**, the CoreWeave section text says **$301**. Adopted $303 (2:1, and it is the disclosure page).

➜ **Action: CRWV: largest outright divergence of the run — Arete $317 is +119% above the $144.74 consensus PT, on revenue +26%/+37% vs consensus in 28E/29E. Consensus still has CRWV loss-making until 3FY, so the target rests on a profitability crossover the Street has not underwritten.**

### 5. 🟡 NBIS — the revenue upgrade is NOT free

| Metric | Arete | Baseline | Δ |
|---|--:|--:|--:|
| Price target | **$415** (raised from $380) | BBG cons. PT $292.94 | **+41.7%** |
| Revenue '27E / '28E / '29E | — | vs consensus | **+14% / +54% / >+70%** |
| **Capex '27E / '28E** | — | **vs consensus** | **+66% / +94%** |

**This is the one to read carefully.** The headline is a big above-consensus revenue call, but Arete's own words are that the raise is "partially offset by convertible and equity dilution and higher capex" — and the capex is up *more* in percentage terms than revenue in '28E. Arete also ranks NBIS **least levered** of its three neoclouds (33 unsold MW/$bn market cap vs CRWV's 50). So the +41.7% PT gap materially overstates the enthusiasm.

⚠️ Unresolved: Arete says the convertible is "$5bn upsizeable to $5.75bn"; the page carries the 08-19 launch at **$4.5bn**. Probably launch vs upsized/priced — not adopted.

➜ **Action: NBIS: discount the headline. The +41.7% PT gap overstates it — Arete's revenue upgrade (+14%/+54%/>+70%) comes with capex ALSO +66%/+94% above consensus, Arete's own words are 'partially offset by convertible and equity dilution and higher capex', and it ranks NBIS LEAST levered of its three neoclouds.**

### 6. 🟡 IFX / TXN / ADI — the PT directions DISAGREE inside one deck

| Name | Arete TP | Prior Arete | Direction | BBG cons. PT | Δ vs cons. |
|---|--:|--:|:--|--:|--:|
| **IFX GR** | **EUR124** | EUR114 | **RAISED +9%** | 87.67 | **+41.4%** |
| **TXN US** | **$381** | **$405** | **⚠️ CUT −6%** | 328.68 | +15.9% |
| ADI US | $490 | **$487** (07-21) | raised +0.6% | 468.38 | **+4.6%** |
| `MPWR` | $2,013 | — | **INITIATE** | *no wiki page* | — |
| `STM` | $70 | — | — | *no wiki page* | — |

**This is not a uniformly bullish deck, and the headline TPs hide it.** IFX is raised 9% and sits +41% above consensus; **TXN is CUT 6%**; ADI's "+$3" is a rounding move on a mark the page already carried (Arete $487, 07-21 — moved to Changelog). Only IFX is a real new above-consensus call. The filename (`…TXN_Datacentre_Power_Semis…`) points at the wrong name — IFX carries 104 mentions to TXN's 8.

**TXN is the subtle one: a PT CUT on estimates far ABOVE consensus.** Arete models TXN datacentre revenue at **$9.9bn by '28** and **FY28 EPS $15.7 vs BBG 3FY $12.45 (+26%)**, yet cut the target — i.e. **multiple compression on rising numbers**, the mirror image of BMO's NVDA call (D-2). Ex-D/C is deliberately conservative, so the entire aggression sits in one line. It also **backs TXN management on pricing**: TI is the only vendor marked **FLAT** on realised SPS pricing while every peer is Up, corroborating TXN IR's "the blended is not that" against the page's open Jefferies "haven't seen enough" debate.

**IFX — the divergence is against company guidance, not just consensus.** Arete's FY27 build is **EUR4.8bn AI / EUR6.13bn total datacentre**, roughly **2x management's EUR2.5bn guide** and **~55% above BofA's EUR3.96bn**. But the note is honest about the cost: IFX has **already lost VRM share** to MPS/Renesas after SPS lead times went **52→89 weeks**, and Arete expects NVIDIA to design **TI into Rubin Ultra** for relief (TI ~16 weeks vs IFX ~90). It also **contests two standing page claims** — placing IFX *third in IVR* (page says "lacks a competitive offering") and recording 200mm+300mm GaN (page carries Innoscience's "no 8-inch"). Ties to D-2: the same VRM tightness is NVDA's fourth Rubin Ultra constraint.

**ADI — the title is the warning.** "Fantastic Portfolio, **Limited Supply Base**": capacity graded **"Weak"**, ranked *last of five* on upside despite FY28 EPS $24 vs visible-alternative $19. The September price round is now sized — **<30%, broad** — with the rationale shifting Feb→Sep from "inflation" to "inflation *and demand*", which quantifies a catalyst the page had flagged but could not measure.

**Two pageless-name findings worth keeping:**
- **`NVTS`** — named a leader in IBC/PSU/SST with the **lowest Rds-on of any 650V GaN FET (25mΩ)**, contradicting the page's Citi and FinTwit rows — but priced at only **~$10m of '26E datacentre sales (rank #7)**, absent from VRM and IVR (the two largest sockets), and "unlikely to support a large hyperscaler as primary source near-term." The page's open low-voltage-GaN question now has a hard negative: Navitas's own 800→6V design uses a **25V silicon** secondary. TSMC-exit risk sized at **>50% of TSMC GaN demand**.
- **`WOLF`** — capacity graded **"Strong"** (200mm MV SiC fab **~30% utilised**, $1bn+ headroom), which **inverts the sign** on the underutilisation this page treats purely as a GM drag. Against three net-new negatives: the 10kV part is "only a bare die" when "SST players will buy modules"; "recent bankruptcy proceedings may deter partners" (IFX has 20 SST partnerships, WOLF one); worst Rds-on in the group at 1.2kV and 2kV. Most consequential: **SST TAM cut to ~$200m in '28**, so the page was re-pointed at **PSU ($2bn TAM)** — which matches management's own "fastest AI ramp is PSU."

Framework: AI power-semis TAM **$24bn in 2028**; **GW capacity doubling every 13 months**; near-term earnings lever is the cyclical trio — lead times extending, capacity tightening, **pricing up everywhere.**

⚠️ Source inconsistency logged, neither asserted: IFX's CPU TAM reads ~EUR2bn→EUR6.5bn on the summary slide but EUR1.1bn→EUR3.3bn on the CPU slide. Also dropped as extraction artefacts: TXN's ">210bn of AI power semis revenue" and NVTS's 24% "D/C % Sales" (irreconcilable with ~$10m in the same row).

➜ **Action: Power semis: the deck is not uniformly bullish and the headline TPs hide it — IFX RAISED 9% to EUR124 (+41% vs consensus, and 2x management's own EUR2.5bn datacentre guide), TXN CUT 6% to $381 despite modelling FY28 EPS +26% above consensus (multiple compression on rising numbers), ADI a rounding move on a mark already held. Only IFX is a real new above-consensus call.**

### 7. 🔴 ORCL / META / GOOG / AMZN — Off-balance-sheet AI financing is LARGER than the tracked issuance

Barclays' headline is ~$338bn YTD (vs $179bn full-year 2025) and hyperscalers at **14% of USD IG corporate supply (~17% incl. data center bonds)**. The deal-level detail says that **understates** the claim on credit:

| Channel | Size | vs the name's own issuance |
|---|--:|---|
| **Oracle-tenanted** 3rd-party DC bonds (RDMICH $14.0bn/974MW, PFORGE $2.15bn/200MW, YNDRDC $715mn/48MW) | **$16.87bn / 1,222MW** | **≈ 67% of Oracle's own $25.0bn** |
| **Meta JV** structures (Blue Owl/Beignet $27.29bn/2,064MW, BlackRock/Sopapilla $12.64bn/960MW) | **$39.93bn / 3,024MW** | **≈ 1.6x Meta's own $25.0bn** |

Both sit outside the IG-corporate-supply share. **Oracle started widest and widened most on every tranche** (issue-to-current +63/+74bp on everything '36+, YTW to 7.90%, cash to 87.4) against META +40bp, SPCX +57bp, GOOGL +27bp, AMZN +9bp. The Meta JV channel **repriced ~95bp wider** between the only two deals done in it, with Barclays expecting more supply.

**House models corroborate the direction:** Capstone has GOOG capex 2027E **$310bn** with FCF **−$55bn**, and META capex 2027E **$170bn** with FCF **−$23bn**. Both are consistent with Barclays' "IG bond supply will continue to grow" — the funding gap is in the house numbers already.

⚠️ Three incompatible perimeters now on the pages — Barclays **$338bn** (USD-only), MS **$445bn** ("across credit channels"), GS **$194bn** (five names ex-SPV). Guard-rail written on every page carrying more than one; no netting.
⚠️ Unresolved: Barclays marks two Amazon-offtake bonds at **5.98%/6.42% YTW** where AMZN.md carries **7.9%/8.8%** from MS for what the megawatts identify as the same bonds. Both retained.

➜ **Action: Hyperscaler financing: the '14% of USD IG corporate supply' figure UNDERSTATES the claim on credit. Oracle-tenanted third-party DC bonds are $16.87bn (~67% of Oracle's own issuance) and Meta's JV structures $39.93bn (~1.6x its own) — both outside that share. Oracle started widest and widened most on every tranche; the Meta JV channel repriced ~95bp wider between two deals. House GOOG/META capex already implies the funding gap.**

### 8. 🟡 SAMSUNG / MU / SKHYNIX — a BASIS dispute, not a level dispute

`SAMSUNG.md` carries a **~24% CXMT ASP discount** (Wells Fargo / Rakers, 07-14). The DAMNANG note argues any company-average discount is a **mix artefact**: ~2/3 of CXMT revenue is low-priced mobile, like-for-like the gap is **5-10% per CXMT's own IPO prospectus**, and **in server the sign flips** — July 2026, a 64GB DDR5 module on CXMT chips at **RMB18,999 vs RMB18,595** on Samsung/SK hynix, i.e. CXMT **2.2% higher**, reportedly quoted above Samsung's US$1,240/module contract.

Both marks stand. **The disagreement is about the denominator, not the number** — and it matters, because a 24% structural discount and a 2% server premium imply opposite conclusions about DRAM price risk. Flagged independently by two agents.

The same note **refutes all four legs** of the CXMT bear case (13% of wafer starts → only 6% of capacity; 1Q26 +71% y/y decomposes to +11% volume / +57% ASP; IPO supply 2028 at the earliest; HBM <2% of starts at ~25% yield). Its net call: the memory correction is "more likely to END after the CXMT listing than to continue." Reusable incumbent-side identity: **HBM = 22% of 2026 global DRAM wafer capacity producing 9% of memory capacity.**

➜ **Action: CXMT pricing: a BASIS dispute, not a level dispute — the page's ~24% company-average discount (Wells Fargo 07-14) versus like-for-like 5-10% and a SIGN FLIP in server (CXMT 2.2% HIGHER). Both stand; they imply opposite conclusions about DRAM price risk, so never quote one without its denominator.**

### 9. 🟢 KIOXIA / SNDK / PANW / CRWD — Stale marks now provably stale

| Mark | Source date | vs cons. PT | vs spot |
|---|---|--:|--:|
| KIOXIA TP JPY55,400 | 2026-04-30 | **−51.8%** (cons 114,935) | +2.0% |
| SNDK TP $1,452 | 2026-04-30 | **−34.1%** (cons 2,204.72) | **−9.0% (BELOW SPOT)** |
| PANW — MS PT $320 *(on page)* | — | vs cons 367.03 | **BELOW SPOT $357.87** |
| CRWD — MS PT $172 *(on page)* | — | vs cons 212.95 | **BELOW SPOT $191.95** |

The China Renaissance PTs are logged as historical and did **not** displace any live mark (SNDK's ladder runs Bernstein $3,000 → MS/Jefferies $1,750). Pushing newer numbers into Changelog on the strength of an older note would be backwards thesis drift.

**But the staleness itself yielded alpha:** the note records SanDisk's *own April guidance* as "HBF samples 2HCY26, commercialization early-2027", against the August Investor Day's 2027 samples and **no commercial date**. That is a dated third-party timestamp showing **~two quarters of rightward drift in four months.**

Separately, MS's own 08-21 disclosure prices PANW at $349.56 and CRWD at $190.34 — so the MS PTs carried on those pages are below spot and need refreshing.

➜ **Action: Stale marks: China Renaissance KIOXIA JPY55,400 is -51.8% vs consensus and SNDK $1,452 is BELOW SPOT — logged historical, and they did NOT displace live marks (backwards drift). Separately the MS PTs carried on PANW ($320) and CRWD ($172) are now below spot and need refreshing. The staleness itself yielded alpha: SNDK HBF timing drifted ~2 quarters right in 4 months.**

### 10. 🟡 MU / NVDA / SKHYNIX — Open disagreements retained, not resolved

- **"MU leads in HBM4"** (BMO) collides with SemiAnalysis's ~0%-of-first-12-months and Fubon's 08-03 "only a small volume", and with the 08-18 block where two houses put Samsung #1 in 2027. Three marks, all standing.
- **HDD→NAND becomes structural** (BMO) against Bernstein's ex-WDC TCO-crossover math.
- **Rubin Ultra HBM4 8-Hi** — carries the author's own "UNCONFIRMED, based on industry checks" disclaimer at every occurrence, and was deliberately NOT allowed to move any Sinal verdict. It is the **fourth** de-spec sighting and lands on MS's "decision open until end-3Q26" rather than UBS's 08-07 "settled." A confirmed downshift would be the first genuine mix-DOWN in HBM content per GPU — too consequential to let a rumour carry.
- **SpaceX→Google $/MW premium** — Arete's $55m/MW implies ~2.2-2.8x peers; SemiAnalysis said **4x** for the same deal (07-02). Bases do not convert (GB300 packs far fewer GPUs per MW than Hopper).

---

➜ **Action: Open disagreements deliberately retained, not resolved: 'MU leads HBM4' (BMO) against SemiAnalysis ~0%-of-first-12-months and two houses putting Samsung #1 in 2027; HDD-to-NAND structural against Bernstein's TCO math; and the Rubin Ultra HBM4 8-Hi claim, which is UNCONFIRMED per the author's own disclaimer and was not allowed to move any Sinal verdict.**

## CONFIRMS — no action

- **BMO's NVDA and MU estimates are consensus.** Revenue and EPS land within 0.4-4.3% on NVDA and 0.2-1.3% on MU. Both initiations are valuation statements, not forecast statements. (This is what makes D-1 and D-2 readable at all.)
- **MS's Samsung FY26E revenue IS consensus** — W729,299bn vs W729,874bn, −0.1%. The model is mainstream on the top line; the divergence is concentrated in capex.
- **Citi's dividend arithmetic checks out** — W120tn ÷ 6,607mn shares ÷ W281,500 = 6.45% vs Citi's stated 6.4%.
- **CoreWeave's $20-25m/MW pricing is now externally corroborated** — promoted from a Nebius/CoreWeave disclosure to an industry-level observation.
- **ANTHROPIC $65B+ ARR** supersedes SemiAnalysis's own `>$60B (3Q26)` mark (moved to Changelog). It **tilts** the 08-20 conflict flag: the only bottoms-up modeller has moved onto the ~$65bn end-July desk figure and away from FUNDA's >$70B. Tilt, **not** resolution — gross-vs-net and peak-hour annualisation remain open.
- **Barclays independently confirms MS's per-name splits** — ORCL $25.0bn USD / $0 foreign; META $25.0bn USD / $0 foreign. This **closes a standing guard-rail** on META.md that read "DO NOT infer a per-name split."
- **AMZN is the largest IG borrower in the complex** — $62.0bn USD + $30.4bn foreign = $92.4bn YTD, with the single largest transaction in the table ($37.0bn, 3/10).
- **PANW's organic split finally sized** — FQ3 M&A ~$388M revenue / ~$1.6bn NGS ARR / ~$1.8bn RPO against **organic NGS ARR +28%** vs a ~60% headline. Quantifies the UBS/Redburn bear rather than refuting it; the ✗ verdict holds.
- **CRWD's AIDR judged "a clean incremental AI-security offering rather than a relabeling of endpoint revenue"** — first channel-checked answer to that bear on the page.
- **MU's HBM trade ratio ~4:1** — second house after Mizuho at approximately 4x.

---

## Data-quality items (flagged, not silently fixed)

1. **`NVDA.md` house-model block shows operating margin ~89/92/94% against gross margin ~71/75/74%.** Operating margin cannot exceed gross margin — that row is mislabelled (possibly op income as % of gross profit). Not corrected here because the intended metric is a guess.
2. **BMO's MU block-model GM/OpM rows extracted corrupted** (GM "1,142.5%", OpM 0.0). No BMO margin *percentage* from the table appears on MU.md. Only the clean prose ">70% FY26" is carried, plus a clearly-labelled derivation (~80.5% / ~86.0%) from the uncorrupted revenue and gross-profit lines.
3. **BMO's MU capex is internally inconsistent** — "$25 billion in FY2026" (prose) vs $29,602mm (model) vs ">$27bn" (commitment). All three logged, none adopted.
4. **Five pre-existing broken Sources links** across GOOG/NVDA/GEV/optical-cpo/ai-datacenter-power point to two report HTMLs absent from `relatórios bons\`. Pre-existing in HEAD, not caused by this run.
5. **`SPCX.md` has no `## Intra-quarter` section**, so the mandatory log row + Sinal re-score could not be performed there (second consecutive run). Nothing hand-scaffolded — a Sinal table would require inventing a management column.
