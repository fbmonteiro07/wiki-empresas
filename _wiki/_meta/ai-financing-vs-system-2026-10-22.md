# The AI debt wall vs the capital system — 2027 / 2028 sizing (2026-10-22)

_Capstone internal analysis note (Felipe Monteiro's question, 2026-10-22: "will there be enough capital to fund ~$1tn of build-out debt next year and ~$1.5tn in 2028 — how much of the system is that, who else is asking for capital, e.g. the French government?"). Built with the quant-estimate discipline: every input tagged **HARD / PARTIAL / ANCHOR / EST**, guardrails, and a double-check skeptic run BEFORE publication (verdict PARTIAL → fixes applied, §7). Model: [`_data/ai-debt-capacity-2028/ai_financing_vs_system_v2.py`](../_data/ai-debt-capacity-2028/ai_financing_vs_system_v2.py) (stdlib; output `ai_financing_vs_system_v2_out.json` beside it). Companion pages: [themes/hyperscaler-capex](../themes/hyperscaler-capex.md) (issuance ledger), [themes/macro-cycle](../themes/macro-cycle.md) (GS credit dashboard, issuance mechanism), `_dashboards/ai-capex-funding.html` (house AI Model capex/OCF series), `_data/credit_workbook.json` (project-bond universe), `_data/ai-debt-capacity-2028/` (CRWV/big-4 2028 underwriting screen)._

## 1. The answer

- **$1tn for 2027 is the top of the defensible range, not the centre.** On the house AI Model capex path with like-for-like four-name hyperscaler marks, the AI build-out needs **~$0.85–0.93tn of external financing in 2027 (range $0.75–1.03tn)** and **~$1.4tn in 2028 (range $1.15–1.65tn)**. On Goldman's narrower AI-infrastructure perimeter the same shares give only ~$0.5tn / ~$0.75tn; on New Street's whole-economy perimeter ~$1.15tn / ~$1.75tn. The 2028 number rests on the house's $2.9tn total-AI-capex line, which only New Street ($3.3tn) corroborates — Goldman is at $2.0tn.
- **It is not a savings-pool problem, it is a channel-and-duration problem.** ~$0.9tn is **~3% of world gross saving, ~3% of global sovereign+corporate borrowing and ~8% of all US long-term fixed-income issuance** — the world can fund it. But hyperscaler issuance is concentrated at the long end: Exante Data (via Rodrigo Nascimento, 09-11) puts hyperscalers' >10-year issuance at ~$200bn in 2026 and >$300bn in 2027 against ~$400bn/yr of US Treasury net ≥10-year supply after Fed holdings — **~50% of the Treasury's long-end supply now, ~75% next year.** GS's hard version: ~$510bn of incremental USD-IG absorption before index-concentration conventions bind, vs ~$2tn of ratings capacity.
- **Who competes.** On net new money in 2027 the AI complex (~$0.9tn) is the **third-largest borrower after the US Treasury (~$2.1tn) and China's government (~$1.7tn ex the hidden-debt swap)**, ahead of every European sovereign (Germany ~$0.24tn net, France ~$0.17tn deficit), ~5x Japan's new-money JGBs, and ~1.4x Europe+Canada's entire defence budget. France is the right example because it is raising a **record €340bn in 2027 (announced 29-Sep-26, up from €310bn)** at a 5.4% deficit, with the OAT–Bund spread going from 114bp (29-Sep) to ~168bp and the 10-year OAT above 5% (22-Oct, press) — and the euro long end is where hyperscaler overflow supply (GOOG $35bn foreign-currency YTD, AMZN sterling, UBER euro) now lands.
- **What gives: price first, then volume.** MS models spreads as "the natural release valve" (a funding tax); GS models a USD-IG quantity ceiling (a funding stop). The observables already moving: new-issue concessions 2–3bp → 20bp, AI-related USD HY 360bp (+25bp in two days, Oct 13–14), hyperscaler spreads +26–29bp YTD vs the IG index +1bp, insurers' $50m+ 30-year orders halved, September AI issuance only ~$23bn after $445bn through August (MS 10-01, "A Pause, Not a Pullback").

## 2. Where the ~$0.9tn / ~$1.4tn comes from — the arithmetic

**Equation (flow, $bn, calendar year):**

`external need = hyper_share × big-4 TOTAL capex + nonhyper_share × (total AI capex − big-4 AI capex)`

Two cohorts because they borrow differently: the big four (MSFT/AMZN/GOOG/META) fund most capex from OCF and issue corporate IG against the residual; everyone else (ORCL, SPCX, neoclouds, data-centre developers/JVs, labs' own DCs, sovereign and enterprise) is mostly externally financed — project bonds, ABS/CMBS, private credit, converts, HY, prepayments, vendor backstops.

| Input | 2026 | 2027 | 2028 | Tag · source |
|---|--:|--:|--:|---|
| Total AI capex, all players | 901.6 | 1,885.4 | 2,913.1 | **HARD (house)** — Capstone AI Model `Resumo | Total`, Aug-26 vintage |
| Big-4 AI capex (per-name PLAYERS sums) | 681.9 | 1,192.2 | 1,550.5 | **HARD (house)** — ⚠️ the model's r18 line is 1,125 / 1,425 with the offset in "outros"; residual built on the PLAYERS sums so it is internally consistent |
| Big-4 OCF (consensus-based exhibit) | 687 | 921 | 1,197 | **PARTIAL** — pasted exhibit Aug-26; 4- vs 5-name perimeter unverified |
| Big-4 TOTAL capex (AI + non-AI) | 723 | 1,014 cons / 1,229 JPM | 1,119 cons / 1,356 JPM-scaled | **HARD** BBG BEST_CAPEX live 10-22; **HARD** JPM Anmuth 10-15 (366.4+378.3+242.7+241.9); 2028 JPM-scaled = **EST** |
| Hyperscaler debt share of total capex (4-name) | 0.33 | 0.33 | 0.30 | **ANCHOR** 2026 = Barclays 4-name YTD-Aug 197.7 + ~40 "moderate" Q4 (MS 10-01) ÷ 723; 2027 held at the run-rate; 2028 **EST** ≤ GS's "2027 peaks" |
| Non-hyperscaler external share | — | 0.75 | 0.75 | **ASSUMPTION, range 0.60–0.90** — see identification below |

**2027, step by step (central = house residual, JPM big-4 total):** 0.33 × 1,229 = **406** (hyperscaler corporate debt; 335 on consensus capex) + 0.75 × (1,885.4 − 1,192.2 = 693) = **520** (project finance incl. DC bonds, private credit/SPVs, neocloud HY/converts, prepayments) → **$926bn** (855 on consensus capex).
**2028:** 0.30 × 1,356 = **407** (336 on consensus) + 0.75 × (2,913.1 − 1,550.5 = 1,363) = **1,022** → **$1,429bn** (1,358 on consensus).
**Range:** 2027 $751bn (consensus capex, 0.60) – $1,030bn (JPM capex, 0.90); 2028 $1,153bn – $1,633bn.

**Reconciliation of the hyperscaler leg (why debt > "AI capex − OCF"):** 2027: AI capex − OCF = 1,192 − 921 = 271; + non-AI capex ~37 (1,229 − 1,192) + ~100 of dividends/buybacks (EST; GOOG's buyback is already zero) = 408 vs modelled 406 ✓. 2028: 354 − 194 + 100 = 259 vs 407 — **🔴 the house 2028 four-name AI capex (1,550) exceeds the Street's scaled TOTAL capex (1,356): the house is above the Street on the big four in 2028, so the hyperscaler leg is sized on the Street, the residual on the house.** Also missing from this identity (skeptic): cash drawdown (JPM six-name net cash +$227bn → −$264bn in 2027 while debt raised is $357bn), equity (GOOG $84.75bn + $18bn mandatory convert; META Class C), lessor-funded finance leases inside MSFT capex.

**Identification of the non-hyper share (why it is an assumption, not a calibration):** MS all-channel AI-related issuance FY26E ~$505bn ($466bn to 9/30 + moderate Q4) − four-name ~$238bn − semis/vendors ~$60bn ($42bn YTD-Aug) = ~$207bn of non-hyperscaler, non-vendor AI issuance, against non-hyperscaler AI capex of ~$220bn → **~0.9 on a same-year basis**. But that numerator includes securitised take-outs of stabilised DCs (refinancing), REITs, and financing signed 18–24 months ahead of spend (financial close precedes construction) — a lag-adjusted ratio is ~0.4. And the 2027–28 residual changes composition: the labs' own build (0 → 154 → 505 in the house) is mostly equity-funded. Hence 0.75 central, 0.60–0.90 range; ORCL/SPCX inside the residual at 0.75 come to ~$260bn (2027) vs JPM's modelled corporate debt of $102bn — the difference is their off-balance-sheet project financing (Saline, Abilene, Stargate SPVs).

**The same quantity on other houses, like-for-like perimeters ($bn):**

| Basis | 2027 | 2028 | Comment |
|---|--:|--:|---|
| **This model, house capex + JPM big-4 total (central)** | **926** | **1,429** | shares 0.33 / 0.30 and 0.75 |
| This model, house capex + consensus big-4 total | 855 | 1,358 | |
| GS semis bottom-up AI infra ($1.3tn / $2.0tn) + same shares | 487 | 744 | narrower perimeter |
| NSR total AI capex ($2.19tn / $3.33tn) + same shares | 1,154 | 1,742 | whole-economy perimeter |
| NSR's own funding stack re-scaled to annual (base $16.5tn) | 491 / 757 | 747 / 1,150 | $3.7tn external on NSR's upgraded OCF / $5.7tn on consensus OCF |
| Redburn AI-financing call (10-19, Capstone notes by Fernanda Watkins; Outlook, not yet archived) | ~1,000/yr | — | first 100GW ≈ $5tn; hyperscaler FCF ~$2tn/3yrs + US system (10% of corporate bond market + 20% of private credit) ~$2tn → ~$1tn gap |
| **Four-name hyperscaler corporate debt only:** this model | 335–406 | 336–407 | at/above the Street — the model's one aggressive leg |
| · JPM 10-15 (GOOGL 80 / AMZN 75 / META 75 / MSFT 25) | 255 | 300 | |
| · GS 10-15 $420bn scaled 5→4 names (skeptic) | ~384 | — | GS's $420bn and 35% are a FIVE-name set incl. ORCL |
| · BofA 09-15 | 215 | 125 | "$278B to date" reads as cumulative 2025–26; the 310/215/125 path is ambiguous → PARTIAL |
| · MS Nowak 09-07 "$290bn of debt needed" vs OCF $980bn / $1.2tn (7–8x) | ~145–290 | | 7–8x only works if $290bn is cumulative 2027–28 |
| JPM six-name modelled debt raises (incl. SPCX/ORCL) | 357 | 431 | corporate only |
| GS 2027: direct $420bn (5 names) + global project finance $300bn ("firmly skewed to the upside") | 720 | — | |

➤ **Read:** the published *hyperscaler-corporate* numbers sit at $215–385bn for 2027 on four names; the gap to ~$0.9tn is the **non-hyperscaler channel** — project finance (USD IG+HY PF already $106bn YTD-Oct vs $37bn in all of 2025, GS), data-centre bonds ($76bn YTD-Aug vs $36bn FY25, Barclays; outstanding $27bn → $112bn), private-credit SPVs, neocloud paper. That is also where the credit risk sits: NSR puts ~$3.3tn of its $3.7tn on neoclouds "with the support of hyperscalers (guarantees and backstops)", and the 2028 underwriting screen in `_data/ai-debt-capacity-2028` has CRWV passing only if 2028 principal stays ≤ ~$16bn.

**Sensitivity of the 2027 central ($926bn) — elasticities from the skeptic's recompute:** total AI capex 1.43 (the residual is leveraged ~2.5x), house big-4 AI capex −0.85, non-hyper share 0.58, hyper share / big-4 total 0.42. **The load-bearing input is the total-AI-capex perimeter**: is the house "outros players" line of $693bn (2027) and $1,363bn (2028) real cash capex, and whose balance sheet does it sit on? The house 2028 total of $2.9tn is the single most load-bearing estimate for the $1.4tn.

**Guardrails (v2):** hyperscaler 2027 leg 335–406 vs Street 215–385 ⚠️ at the top · non-hyper 2027 leg 520 vs GS project finance $300bn (incl. DC bonds) + private credit/neocloud/prepayments ~$150–250bn 🟢 · cumulative gross AI issuance 2025–29E ~$4.7tn vs SemiAnalysis "$7tn+ outstanding by the late 2020s" — order-of-magnitude only (outstanding ≠ cumulative gross; no method published) · reconciliation 2027 🟢 (406 vs 408), 2028 🔴 on the house-vs-Street capex basis (documented above).

## 3. How much of the system is that

All denominators are **flows per year** unless marked STOCK. Need = ~$0.93tn (2027) / ~$1.43tn (2028), gross external financing, all channels and currencies. Where a denominator is net, the ratio modestly overstates AI's share (AI refinancing is small today, rising from 2029 as ≤5-year chip loans roll).

| Denominator | Size | 2027 | 2028 | Tag · source |
|---|--:|--:|--:|---|
| World gross saving (~27% × $118tn GDP) | ~$32tn | 3% | 4.5% | EST (IMF saving rate from memory; GDP PARTIAL) |
| OECD sovereign + corporate borrowing 2026, gross, as reported ("$27tn 2025 → $29tn 2026") | $29tn | 3% | 5% | HARD — OECD Global Debt Report 2026 (Mar-26) |
| Global corporate bonds + syndicated loans (2025) | $13.8tn | 7% | 10% | HARD — OECD ($6.8tn + $7.0tn) |
| Global corporate bond issuance (2025) | $6.8tn | 14% | 21% | HARD — OECD |
| US long-term fixed-income issuance 2025, all sectors (UST $4.8tn, MBS $1.9tn, corporates $2.2tn, agency $1.4tn, munis $0.6tn, ABS $0.5tn) | $11.5tn | 8% | 12% | HARD — SIFMA 2026 Fact Book; SemiAnalysis: 2026 is "the last year AI debt issuance is <10% of US fixed-income issuance" |
| OECD sovereign gross issuance 2026 | $18tn | 5% | 8% | HARD — OECD (record; ~80% refinancing) |
| US Treasury net marketable borrowing, CY2026 (Q2 $190bn + Q3 $739bn + Q4 $628bn + Q1 EST) | ~$2.1tn | 44% | 68% | HARD quarters (Treasury Aug-26) / PARTIAL annual |
| US Treasury net ≥10-year supply after Fed holdings | ~$0.4tn | hyperscaler >10y issuance alone ~75% (2027) vs ~50% (2026) | — | PARTIAL — Exante Data via Rodrigo Nascimento (Outlook 09-11), not yet archived |
| USD IG gross issuance 2027 | $2.4tn | 15–18% like-for-like (USD IG-eligible AI paper ~$370–430bn); 39% if every dollar had to come from USD IG | 25% / 60% | HARD — GS credit dashboard 10-15; AI share of IG supply was ~7% (2025) → 14–18% (2026 YTD) |
| IEA global energy investment 2026 (spend — compare with AI **capex** $1.9tn = 55%, not with financing) | $3.4tn | — | — | HARD — IEA WEI 2026 (grids $550bn, electricity $1.6tn) |
| Private credit AUM (STOCK) | ~$1.85tn | 50% | 77% | PARTIAL — Preqin ~1.7 / Chambers ~2.0; dry powder ~$0.5tn |
| All private-capital dry powder, PC + infra + RE + PE (STOCK) | ~$4.5tn | 21% | 32% | HARD quote — GS credit podcast 08-03 |
| Global bond market outstanding (STOCK) | $109tn | 0.9% | 1.3% | HARD — OECD |
| World GDP / US GDP | $118tn / $31.8tn | 0.8% / 2.9% | 1.2% / 4.5% | PARTIAL — IMF |

➤ **Reading the table:** against the *pool* (savings, total borrowing, bond stock) AI is 1–5%: fundable. Against the *channels it actually uses* (USD IG long end, project finance, private credit) it is a large share of a year's flow and a majority of the long-end supply: not fundable without (a) the AI share of USD IG supply rising again with ever-longer tenor (40% of 15-year-plus IG issuance in 2026 was AI-related; AMZN is now the highest duration weight in the IG index), (b) project finance tripling again, (c) private credit deploying a large part of its dry powder into one theme, or (d) spreads doing the rationing. GS's ~$510bn of incremental USD-IG absorption is the hard version of (a), and GS itself calls it generous.

## 4. Who else is asking for capital in 2027 (the competing borrowers)

Gross programmes unless stated; FX EUR 1.17 / GBP 1.33 / JPY 150 / CNY 7.1 (EST). 2027 programmes for most sovereigns are published in December; where known they are shown.

| Borrower / use | 2026 | 2027 | Basis | Tag · source |
|---|--:|--:|---|---|
| **US Treasury** | ~$2.1tn net marketable (CY, PARTIAL); deficit $1.8tn first 10m FY26 | similar or higher (CBO: trade-policy changes add $0.9tn over 2027–36; tariff revenue the swing) | net | HARD quarters — Treasury refunding Aug-26, CBO |
| **China central + local government** | ~$1.66tn net ex-swap: deficit CNY5.89tn + ultra-long specials 1.3tn + local specials 4.6tn (+ CNY2tn hidden-debt swap = refinancing) | NPC March 2027 (2026 quotas flat, "below expectations") | net / swap = refi | HARD quotas — NPC/MNI |
| **Japan** | ¥180.7tn ≈ $1.2tn gross; new money ~¥28.6tn ≈ $0.19tn | FY27 plan Dec-26 | gross / net | HARD — MOF |
| **France (AFT)** | €310bn net-of-buybacks MLT ≈ $363bn; **deficit 5.4% of GDP (vs 4.6% targeted) ≈ €165bn** | **€340bn MLT net of buybacks — a record, announced 29-Sep-26**; 2027 deficit target 5.0% (6.5% "without measures"), 3% by 2029; €54bn package in a minority parliament before the 2027 presidential; OAT–Bund 114bp (29-Sep, first >100bp since 2012) → ~168bp and 10y OAT 5.14% (22-Oct teaser, France Épargne — press, verify on AFT/Bloomberg); debt → 121.7% of GDP | gross MLT / deficit | HARD programmes — AFT; deficit & spread — press Sep/Oct-26 |
| **Germany** | €525.5bn total issuance incl. Bubills (capital-market €349.5bn ≈ $409bn); net borrowing €174.3bn ≈ $204bn | net borrowing €203bn ≈ $237bn (draft): core €118.7bn + infra fund €54.9bn + defence fund €30bn; "Zeitenwende: issuance +40%" | gross / net | HARD — Finanzagentur Sep-26, draft budget |
| **Italy (MEF)** | H2-26 MLT gross €130–145bn, net €10–25bn (ex-NGEU/SAFE loans); full year ~€320–340bn gross ≈ $390bn | similar | gross MLT | HARD H2 guidance (press); full-year PARTIAL |
| **Spain (Tesoro)** | gross €285.7bn (MLT €176.9bn + bills €108.8bn); **net €55bn**, flat | similar | gross / net | HARD — Tesoro Público |
| **UK (DMO)** | £246.2bn gilt sales 2026-27 ≈ $327bn (long-dated cut to £23bn) | remit Mar-27 | gross | HARD — DMO Apr-26 revision |
| **EU (NGEU + SAFE defence loans + Ukraine)** | €180bn ≈ $211bn | ≥ similar (Ukraine Support Loan 2026-27) | gross | HARD — Commission May/Jun-26 |
| **Europe sovereign + EU, gross MLT, sum of above** | **~$1.9tn** | ~$2.0tn+ | gross | derived |
| **Defence (NATO Europe + Canada)** | $634bn (+11%); 2.53% core + 1.4% related = 3.93% of GDP | → 3.5% core by 2035: Europe ~$700bn → ~$1tn (Capital Alpha scenario); EU "€800bn to 2029" | spend, inside the sovereign deficits above | HARD 2026 — NATO Jul-26; path PARTIAL |
| **Energy / grids / power** | $3.4tn global energy investment; grids $550bn (+20%); electricity $1.6tn | rising; utilities are IG issuers (GS: AI-adjacent Energy/Utilities spreads resilient) | spend, mostly OCF + regulated-utility debt | HARD — IEA WEI 2026 |
| **US non-financial corporate maturity wall (refinancing)** | — | $572bn (2027) → $1.03tn (2030); IG $437bn → $513bn 2027-29; HY $68bn → $314bn by 2029 | gross refi | HARD — Reuters/LSEG |
| **AI labs — equity, not debt** | OpenAI $122bn (Mar-26; FT: cash "exhausted in 2028"), Anthropic $65bn Series H ($965bn post), xAI $20bn | OpenAI plan ~$1.2tn raise through 2030; All-In (10-16): Anthropic "needs $150–200bn" next | equity, competes for the same allocators | HARD rounds; plans PARTIAL |
| **Semis supply chain capex (TSM / memory / WFE)** | TSMC ~$220bn 2026-28; WFE $200–280bn 2027/28 | self-funded from OCF | spend, not a borrower | HARD — wiki semicap-wfe |
| **AI build-out (this note)** | ~$0.5tn observed (MS: $466bn to 9/30, Sep ~$23bn, Q4 "moderate"; ~70% unsecured corporate) | **~$0.9tn** | **~$1.4tn in 2028** | gross external financing | this model |

➤ **Ranking for 2027 on net new money:** US Treasury (~$2.1tn) > China government (~$1.7tn) > **AI build-out (~$0.9tn)** > Europe sovereign net (~$0.7–0.9tn: Germany $0.24tn, France ~$0.19tn deficit, Italy/Spain/UK ~$0.4tn) > EM sovereigns > Japan new money (~$0.2tn). On *gross* (refinancing included) sovereigns dwarf everything (OECD $18tn), which is why the "will there be capital" question is really "will there be *duration* and *IG-index room*", and why the 2027 sovereign calendars landing in December matter.

**Why France is the right example.** (i) It is the largest or second-largest euro issuer (€310bn → €340bn, vs Italy ~€330bn) and the one with the widest political-risk premium — OAT–Bund 114bp at the 2027-programme announcement and ~168bp on 22-Oct per press, with the 10-year above 5% and a minority government carrying a €54bn package into the 2027 presidential cycle. (ii) The AI complex has started using the euro and sterling markets as the overflow for USD indigestion: GOOG $35.3bn of foreign-currency bonds YTD (of $80.3bn), AMZN £4.25bn debut sterling, UBER €4.5bn debut euro, all in September. (iii) Germany's own supply is +40% (infrastructure + defence funds), so the euro real-money bid is being asked to absorb Bunds + OATs + SAFE + hyperscalers at once. The euro long end is where sovereign and AI supply collide first.

## 5. Where ~$0.9tn can actually clear — channel by channel (2027, $bn, debt channels only; equity shown separately as relief)

| Channel | 2026 observed / run-rate | 2027 capacity read | Ceiling / tell | Tag |
|---|--:|--:|---|---|
| Hyperscaler corporate IG, 4 names, all currencies | 4-name $197.7bn YTD-Aug (Barclays), FY ~$235–250bn; 14% of USD IG corporate supply, Tech 37% of IG non-financials; 32% priced outside USD | Street 215–385; model 335–406 | GS ~$510bn incremental USD-IG absorption (generous); insurers' 30-yr orders halved; concession 20bp; Exante: ~75% of UST net ≥10y supply | HARD marks |
| ORCL / SPCX corporate (IG + converts) | ORCL $25bn, SPCX $25bn YTD-Aug | JPM 102 | ORCL FCF-negative; SPCX IPO'd | HARD |
| Project finance, USD IG+HY, all sectors (DC-dominated) — **includes the data-centre bond complex** (DC bonds $76bn YTD-Aug; outstanding $27bn → $112bn; ~4GW HY pipeline) | $106bn YTD-Oct vs $37bn FY25 | GS 300, "firmly skewed to the upside" | tenant quality is the price: ~8% AMZN-offtake vs 11.5–14.2% CRWV-offtake | HARD |
| Private credit / SPVs / chip-leasing (Apollo-Blackstone-Anthropic $35bn with 82% AVGO backstop; NVDA $500bn platform = MOUs only, ≤25% residual support) | inside the ~$200bn non-hyper 2026 leg | 100–200 | dry powder ~$0.5tn all strategies; GPU residual value (CME H100/B200 rental futures) | PARTIAL |
| Neocloud HY / converts / DDTLs (CRWV, NBIS, IREN, CIFR…) | NBIS ~0% 3.5y / 4–4.5% 7.5y; CRWV 5Y CDS 1,164bp (CDS_FLAT_SPREAD, 10-16) | 50–100 | AI-related USD HY 360bp; CRWV 2028 screen conditional on principal ≤ ~$16bn | PARTIAL |
| Customer prepayments / vendor financing (ORCL $4.6bn prepayments; AVGO/NVDA backstops; AWS–QCOM warrants) | growing | 50–100 | economically debt (MS Castagno) | PARTIAL |
| **Debt stack** | ~$0.5tn | **~$0.8–1.1tn at stretched run-rates** | ~$0.9tn clears only if every channel prints a record, and spreads carry the adjustment | — |
| Equity relief (GOOG $84.75bn + $18bn mandatory convert, buyback to zero; META Class C "capital raising"; lab rounds ~$210bn in 2026) | ~$300bn | 150–300 | substitutes for debt in the hyperscaler leg; competes with it for the same allocators in the lab leg | HARD events / EST |

➤ **Mechanism to hold:** the big four can pay (MS: OCF 7–8x required debt; GS: balance sheets "not a binding constraint", interest coverage "extremely healthy"). The **marginal dollar is raised by entities whose credit is underwritten by someone else's income statement** (NSR's 2.2x debt/EBITDA uses hyperscaler + NVDA + AVGO EBITDA against neocloud debt). The crowding-out shows up first as price in the AI-related sub-indices and as non-USD migration, not as a failed sovereign auction.

## 6. What is hard, what is a guess, and what to watch

- **HARD:** house capex series (house numbers, above the Street on the big four in 2028), JPM per-name 2027 capex, BBG four-name consensus capex, GS $420bn/$300bn (five-name) and 27/33/35% path, MS $466bn YTD-Sep / $500–550bn FY26, Barclays 4-name $197.7bn YTD-Aug and $76bn DC bonds, GS $106bn project finance YTD, OECD $29tn/$18tn/$6.8tn/$7tn, SIFMA $11.5tn, AFT €310bn/€340bn, Finanzagentur €525.5bn/€174bn/€203bn, Tesoro €285.7bn/€55bn, DMO £246.2bn, MOF ¥180.7tn, EU €180bn, Treasury $739bn/$628bn, GS USD IG $2.4tn, IEA $3.4tn, NATO $634bn.
- **PARTIAL / EST (the ones to challenge):** house total-AI-capex perimeter for 2028 ($2.9tn — the biggest lever; GS $2.0tn, NSR $3.3tn); the non-hyper external share 0.75 (0.60–0.90; same-year ~0.9, lag-adjusted ~0.4; labs equity-funded); the 2027 hyperscaler share 0.33 (at the top of the Street); 2028 share 0.30 and JPM-scaled capex 1,356; vendor issuance ~$60bn; Italy full-year; US Treasury CY annualisation; OECD net = 20% of gross; FX; world saving rate; shareholder returns ~100; the BofA 310/215/125 path (ambiguous "to date" base).
- **Not counted (upside to the ask):** utility/grid borrowing induced by AI (GS puts AI-adjacent Energy/Utilities in its AI-related perimeter; IEA grids $550bn), China's AI capex (JPM: China CSP capex +105% y/y 2Q26), lab opex funded by equity (counted as competing equity, not as build-out debt), refinancing of the 2025–26 AI paper (≤5-year chip loans start rolling in 2029–30).
- **Sources in Outlook not yet archived on the wiki (skeptic's sweep):** MS Credit "The State of AI Financing: A Pause, Not a Pullback" (10-01); Exante Data via Rodrigo Nascimento (09-11); Redburn AI-financing call notes by Fernanda Watkins (10-19); UBS AI Debt Financing Monitor (09-22); JPM credit "AI Financing Update" call (Hamid/Spear, 10-16); 22V DeBusschere (08-23: the binding constraint is 10y yields and inflation, not the savings pool). Ingest before the next iteration of this note.
- **Tells to track (already on the wiki's lanes):** new-issue concessions on hyperscaler deals (GS's own signpost); AI-related USD HY spread (360bp) and the GS "AI leaders" basket vs IG index; insurer participation in 30-year tranches; META's post-3Q issuance and MSFT's first dollar; non-USD share of hyperscaler issuance; project-finance prints vs GS's $300bn; CME GPU rental futures (residual value); OAT–Bund and the December sovereign calendars (AFT already out at €340bn; Finanzagentur, MOF, DMO to come).

## 7. Skeptic verdict and adjudication

**Double-check agent, 2026-10-22, verdict PARTIAL** ("arithmetic clean, wiki quotes mostly accurate, central message survives; $1.0tn is the high end for 2027 because it applied a five-name GS share to JPM's above-consensus four-name capex; $1.66tn for 2028 rested on an unidentified 0.77 share applied to an equity-funded labs cohort and an Aug-26 house capex path that only NSR corroborates").

Accepted and applied (v1 → v2): GS $800bn / 35% / $420bn are five-name incl. ORCL → four-name like-for-like marks and a four-name 2026 anchor (0.33); residual built on the PLAYERS-consistent four-name sums (693 / 1,363, not 760 / 1,488); the 0.77 presented as an assumption with its identification range (0.60–0.90) rather than a calibration; 2028 share 0.30 (GS: 2027 peaks) and the JPM-scaled 2028 capex computed as stated (1,356, not 1,450); BofA 310/215/125 downgraded to PARTIAL (the "$278B to date" base is cumulative); China net ex-swap $1.66tn; US Treasury CY2026 ~$2.1tn (PARTIAL) instead of a two-quarter annualisation; OECD $29tn labelled as reported, not as a sum of components; Germany capital-market issuance for the Europe sum; NSR rescaling on $16.5tn; France 2027 €340bn record and the 114bp spread at announcement; MS Nowak's $290bn and the Exante duration statistic added; §5 stack no longer double-counts DC bonds inside project finance and no longer adds equity to a debt need; ranking corrected (third behind the US Treasury and China). **Headline moved from $1.02tn / $1.66tn to ~$0.9tn / ~$1.4tn, and "2028 is if anything higher" withdrawn.**

Pushed back / kept with a label: the cumulative-issuance vs SemiAnalysis "$7tn+ outstanding" check is kept as an order-of-magnitude cross-reference only (outstanding ≠ cumulative gross); the same-year non-hyper ratio is the right framing for "how much gets *issued* in 2027" even though it embeds the financing lead — so it is shown as a range, not dropped; the IEA comparison is re-based to AI capex (55%) as suggested.

## Changelog
- 2026-10-22 — v2 after the skeptic (PARTIAL → fixes above). v1 headline $1.02tn (2027) / $1.66tn (2028) on a five-name share × four-name capex and a 0.77 "calibrated" share; superseded by ~$0.93tn / ~$1.43tn central, ranges $0.75–1.03tn / $1.15–1.65tn.
- 2026-10-22 — note created (interactive session, Felipe's question).
