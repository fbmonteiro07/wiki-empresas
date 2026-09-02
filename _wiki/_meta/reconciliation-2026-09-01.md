# Reconciliation — 2026-09-01 (/run-inbox, scheduled 23h)

_Every NEW quantitative datapoint from this run, placed against three baselines: **(1)** prior wiki marks on the page, **(2)** the Capstone house model where one exists, **(3)** BBG consensus._

> **BBG status: ⚠️ LIVE WRAPPER DOWN — consensus is an ON-DISK SNAPSHOT, not a live pull.**
> `bdp` raised `ConnectionError: blpapi could not start session` (`Failed to connect to 127.0.0.1:8194`, 3 retries) at 23:30 — **Terminal not logged in at this hour.** Per the skill, no web data was substituted.
> Consensus below is `_wiki\_data\estimates.json`, **`asof: 2026-09-01`, file written 18:30:18 BRT** — the same trading day, so it is *usable*, but it is **~85 minutes after the DELL print (16:05 ET / 17:05 BRT) and therefore PRE-REVISION**: it still carries the Street's pre-print estimates for Dell. That is exactly the right baseline for a guide-vs-Street gap and exactly the wrong one for "where does the Street sit now". **Re-run the PT placements when the Terminal is back** — `estimates.json` carries **no `BEST_TARGET_PRICE`**, so no broker-PT-vs-consensus-PT placement was possible this run (marked ⏳ PENDING-PT below).

> ### ⚠️ DATA-QUALITY DEFECT FOUND IN THE SNAPSHOT ITSELF — read before using any EPS from it
> Testing implied diluted shares (`ni ÷ eps`) across all 99 records: the ratio is internally consistent for almost every name, then blows out for three.
>
> | name | implied shares | real count | factor | verdict |
> |---|--:|--:|--:|---|
> | **TSM** | 5,169m | 25,930m ordinary | **÷5.01** | `eps` is **per-ADS** — BBG ticker is `TAIWAN SEMICONDUCTOR-SP ADR`, 5 ordinary : 1 ADS |
> | **NOW** | 1,020m | ~208m | **×4.9** | `eps` unusable (CY2026 4.06 vs `ni`-derived **$20.04**) |
> | **BKNG** | 768m | ~32m | **×24** | `eps` unusable (CY2026 10.28 vs `ni`-derived **$246.6**; 10.28 implies a 447x P/E) |
>
> `ni` / `rev` / `ebit` / `capex` are **fine** on all three — only `eps` is broken. **Two of the three (TSM, BKNG) are names in this run.**
> 🔴 **This nearly manufactured the run's headline.** Raw fields show TSM house NT$102.5 vs consensus NT$518.74 — a *5x* "divergence". Corrected to an ordinary-share basis, consensus CY2026 is **NT$103.75 vs house NT$102.50 = +1.2%, a CONFIRM.** An ADS-vs-ordinary artifact, one step from being written up as alpha. Same class as the SAMSUNG common-vs-preferred trap. Also: **TSM's `mktcap` reads as USD while its `ccy` says TWD** — don't mix it with the TWD fundamentals.

**House-model coverage** (`_wiki\_data\house.json`, asof 2026-09-01): AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM. **Absent for this run's other names** — DELL, MSFT, ASML, SKHYNIX, SAMSUNG, MU, ORCL, CRM, NOW, MRVL, INTC, MEDIATEK, BKNG — so those get baselines (1) and (3) only.

---

## Where the new data DIVERGES — the alpha

### 1. 🔴🔴 THE HEADLINE: DELL's own FY27 EPS guide is **ABOVE THE STREET HIGH**, while its revenue guide sits INSIDE it. The Street's error is the MARGIN, not the revenue — which adjudicates the "margin stacking on memory" fight this page has been running since 08-14.

Management guide (Q2 FY27 call, 2026-09-01) vs pre-revision consensus:

| Metric | **Dell guide** | Consensus **median** | vs median | Consensus **STREET HIGH** | vs high |
|---|--:|--:|--:|--:|--:|
| F3Q27 revenue | **$49.0bn** | $41.91bn | 🔴 **+16.9%** | $56.45bn | inside |
| F3Q27 EPS | **$6.50** | $4.547 | 🔴 **+43.0%** | **$6.50** | 🎯 **exactly ON the high** |
| FY27 revenue | **$192bn** | $164.91bn | 🔴 **+16.4%** | $194.88bn | just inside |
| FY27 EPS | **$25.50** | $17.26 | 🔴 **+47.7%** | $22.15 | 🔴🔴 **+15.1% ABOVE the high** |

⚠️ **Period-basis caveat, and it matters:** `estimates.json` labels Dell's **fiscal Q3 FY27 as "Q3-26E"** and its **FY27 as "CY2026"** (`lrq 2026-07-31`). Dell's FY27 ends ~Jan-2027, so the CY2026 block is the closest available comparator but is a **mixed basis** (`n_actual = 2`). The quarterly row is the clean comparison; the FY row is directional. **Derive the period from `lrq`, never from the label.**

🔴 **THE READ: on revenue the Street's most bullish analyst is already above Dell's own guide; on EPS not one analyst reaches it.** The whole distribution is mis-specified on margin, not on demand. Management then supplied the mechanism the bulls lacked — the ISG margin bridge is **scale**: *"just over **400 basis points**"* in Q3 and *"over **650 basis points**"* for the full-year guide, with the **ISG rate guided UP even as AI-server revenue triples to $74bn**.

⚠️ **But the bear is wounded, not killed:** management **conceded** *"a notion of inflation inside our growth"* and **refused to split price from volume**. And the **FY28-comp question was asked (Melius, against NVDA's ~+70%) and DECLINED** — "is FY27 peak earnings?" survives the call. Only anchor given: 2H **+68%** vs 1H **+71%**.

### 2. 🔴🔴 The HBM $/Gb anchor this wiki has been quoting is the WRONG VENDOR'S PRICE

Page carried **UBS $3.5-3.9/Gb** (08-07) as *the* HBM4/4E price on NVDA consumption. SemiAnalysis (09-01): that is **Samsung's** price. **SK hynix's Nvidia price is $3.0-3.3/Gb — 14-16% below**, with **$3.7-4.1/Gb** for other Tier 1 buyers.

➤ **There is no single "2027 HBM price": three vendor curves, two customer tiers, ~30% spread.** Every model on this wiki that used one number needs re-basing to a vendor × tier cell.

- 2027 step-ups to NVDA: **SK hynix ~+70% · Micron +89% · Samsung +98%** — corroborates the high side of the page's UBS +90% vs JPM +42% spread.
- ✅ **Net-new and favourable to [[MU]]:** Micron realises **+89%**, *between* Samsung and SK hynix — the #3 supplier gets a better price because **it has no sovereign quid pro quo to fund**. Flagged as the NVDA book, **not** a blended ASP.
- ⚠️ SemiAnalysis is **internally inconsistent**: $3.0-3.3/Gb in one paragraph, $3.0-3.4/Gb two paragraphs later. No level adopted; only the relative gap is used.

### 3. 🔴 2027 DRAM bit supply — a three-way split with TWO LEGS INSIDE MORGAN STANLEY

| Source | 2026 | 2027 |
|---|--:|--:|
| MS · Sean (07-28, on page) | 25% → **~31%** | ~24% |
| **MS semicap (08-25, on page)** | **+32%** | **+38%** |
| **MS · Shawn Kim (09-01, NEW)** | **~35%** | **~25%** |

🔴 **Kim is 13pp below his own firm's equipment analysts on 2027**, and against **UBS + Samsung IR (08-25)** who say undersupply *worsens*. His mechanism: *"at the peak of the cycle, basically everyone lies about their expansion"* — supply started the year at ~25% and is tracking 31%. **This is the single most consequential open disagreement in the run: it decides whether the memory upcycle extends or rolls in 2027.**

- Pricing: 3Q **+15-20%** (consistent with page's Trendforce +13-18%); **4Q ~+5% for both DRAM and NAND — net-new, the page had no 4Q mark.** Weakest link smartphone.
- ⚠️ Same-firm tension: **MS Greater China 3Q26E conventional DRAM +8-13%** vs **Kim's +15-20%**. Flagged, unresolved.

### 4. 🔴 ASML — the wiki was carrying High-NA's WORST-CASE throughput, for the segment that adopts FIRST

Morning relay logged EXE:5200B **135 wph** / 5400E **180 wph**. Bernstein publishes **both modes**: 5200B **175 AA / 135 AB** · 5200C 190/160 · 5200D ≥195/≥175 · 5400E ≥210/≥180 · EXE:5600 ≥250. **AB is the stitched two-reticle mode for large logic die; AA is the DRAM mode — and DRAM is the segment Bernstein says adopts first.**

- 🔴 **"High-NA is a one-customer market" (semicap-wfe 08-11, echoed on INTC) is wrong as stated** — it conflated *Samsung logic* (~1nm/A10 ≈2030, correctly logged) with **Samsung + SK hynix DRAM at 1d in 2027**. SK hynix assembled an EXE:5200B at M16 in Sep-2025; Samsung reportedly ordered two. **Both the bull and the bear reading of that bullet need re-grading.**
- 🔴 **A High-NA push-out is NOT a bear datapoint for ASML** — inverts how this wiki has read Samsung/TSMC slippage since 08-11: *"it's economically better to sell more LNA EUV machines than fewer HNA machines… much higher margin for LNA over HNA."* Litho-tool cost 1×HNA vs 2×LNA: **1.6x (2025) → 1.1x (2030), never crossing 1.0x.**
- ⚠️ **The falsifiable leg is the analyst's, not the company's:** ASML itself puts DRAM insertion at **0a**; Bernstein pulls it to **~1d (2027)**.
- ⚠️ The headline **−23% cost-per-exposure (€82→€63) is priced off 95% availability**, i.e. **3-4 years out** — not a today number (same-day marks: SEMICON relay 84% vs Bernstein/ASML ">80% 2025 → 90% 2026 → ~95% in 3-4 yrs").
- **Rating/PT reiterated, NOT changed:** Outperform, **PT €2,500 / ADR $2,859**, 40x Q5-8, EPS €24.72/38.91/53.56 — identical to 07-30. ⏳ PENDING-PT vs consensus.

### 5. 🔴 MSFT — BofA raises to $600 while sitting **BELOW** consensus on the earnings it is paying 28x for

| | BofA | BBG | Visible Alpha |
|---|--:|--:|--:|
| FY27E adj EPS | **$19.55** | $19.78 | $19.68 |
| FY28E adj EPS | **$22.89** | $23.50 | $23.39 |

**PO $500 → $600** (Buy reiterated, px $507.29, +18.3%), basis **24x → 28x CY27E** ("a premium to the peer group of 18-25x"). **PO is the only line changed in the Key Changes table — no estimate moved.**

✅ **Independent check from the snapshot: $600 ÷ CY2027E EPS $21.32 = 28.1x** — reproduces BofA's stated 28x. **The $600 is financed entirely by the multiple.**

- 🔴 **BofA's Azure model contradicts management's own shape:** **+41.8% FY27E → 37.7% FY28E** against a guided **~45% 1Q27** and management's "H1 FY27 accelerates". A 41.8% year off a 45% first quarter is an **implicit fade**. Open disagreement, not adopted.
- 🔴 **A relay on the page was wrong:** the 09-01 spec-sales row says BofA's RPO is *"~$700bn"*. The primary says **$678bn** — matching the page's own 07-30 marks. Row retained (keep-all-rows), correction stated alongside.
- Published: Azure **39% → 43% → guided 45%** vs a Street bar BofA puts at **40.6%**; **M365 Copilot paid seats >30mn**, net adds **>2x q/q**; **RPO +84% y/y at $678bn**.
- ⚠️ **Basis trap:** BofA is **FY-June**; the page snapshot is **calendar**. Never netted.

### 6. 🔴 MRVL's Google block — a three-way conflict that decides whether the $120bn warrant is ADDITIVE or CANNIBAL

- **MS · Charlie Chan (09-01):** Marvell on the **memory interface INSIDE TPU v10**.
- **FundaAI (09-01):** reads the warrant's own disclosed scope (*"memory interface controllers, and near-memory compute"*) the same way.
- **JPM · Gokul (08-31, already on the pages):** the Google-Marvell deal is *"mostly for **XPU attach and non-TPU accelerator projects**"*.

All three keep **MediaTek as integrator**. ➤ **What it decides: whether the $120bn warrant ceiling is additive to AVGO/MediaTek content or comes out of it. Adjudicator: the v10 block award.**

### 7. 🔴 NVDA — the first BEARISH read of the 70% guide in the open window

Chan: if **10-15%** of the 2027 guide is price passing through **memory cost**, implied **compute VOLUME growth is ~50-60%** — *"very similar to our previous call assumption"* ⇒ *"that 70% doesn't really give us… further upside for our numbers for capacity whatsoever."*

Against the page's standing marks (JPM PT $320 · MS $300 · UBS $300 · SIG ~$700bn FY28 · Redburn ~20% EPS upgrade · GS "upside to the 70% base") and a Síntese that says *"revenue is not the question."*

⚠️ **He does not contest the revenue line — he re-labels 10-15pp of it as inflation.** That leaves unit forecasts unchanged **and makes the Demand row and the Margin row the same event**. Double-count flagged on the page.

- **Ranked bottlenecks: ABF substrate > HBM4 > TSMC wafer (wafer LAST)** — against management naming none.
- ✅ House vs consensus, unchanged and tight: house 2027 rev **$661bn** / EPS **$15.44** vs consensus CY2027 **$687.95bn / $15.39** (−3.9% rev, **+0.3% EPS**).

### 8. 🔴 GOOG/AVGO/ANTHROPIC — the FT (08-04) SIZES a figure the wiki had marked unsizeable, and it is the EARLIER source

GOOG.md carried: *"Epoch says 'part of' the losses and gives no cap… **it cannot be sized from this source**."*

**FT (08-04, eight days BEFORE Epoch's 08-12):** Google backstopped **10 developments / 2.4GW**, on the hook for **as much as $44bn**, carried at **$815mn** on balance sheet (**~54x gap**), with step-in rights on the leases. Epoch's 5 projects / 1,428MW / $15.183bn is only **~half** the backstopped capacity.

- 🔴 **A forward leg absent from Epoch entirely:** an **April** agreement to sell **another 3.5GW of TPU hardware to Broadcom** (4.5GW cumulative) — and **AVGO's filed $128bn of purchase commitments ($55.2bn FY27 / $72.9bn FY28) relate "almost entirely" to it.** AVGO.md already carried those figures from Wells Fargo (08-18) as generic *"primarily inventory"*; the FT supplies **customer, product, power and date**, and corroborates the F2Q26 10-Q's singular *"long-term contract"*.
- **Cost of capital, measured:** Google-backed DC projects borrowed at **7.1% median vs 9.3%** for Nvidia-orbit neoclouds (**~220bp**) — the hard version of the Ben Thompson claim already on GOOG.
- **AVGO's guarantee has a decay curve:** *"residual value support,"* ~$30bn of $35bn, **declining as Anthropic pays** ⇒ with Epoch's ~16-stage draw, exposure is a **hump peaking ~mid-2027**, not a plateau at the $29bn cap.
- ⚠️ **House vs consensus on GOOG (unchanged, but worth stating):** house 2027 rev **$641bn** vs consensus **$548.3bn (+16.9%)** while house EPS **$16.20** vs **$16.59 (−2.3%)** — the house carries materially more revenue at a materially lower margin. Not created by this run; flagged because two sources this run touched the capex/financing line.

### 9. 🔴 Rating-action DATING was wrong on two pages

ORCL carried *"CREDIT UPGRADED to overweight"* and META carried *"JPM DOWNGRADED META credit OW→N"*, both under **07-20**, sourced to the Hyperscalers joint equity+credit call. **Both actions are dated 2026-07-07 and were taken by a different JPM team — Spear/Degen, IG TMT credit.** 07-20 was the relay. (Same class as the Blayne-Curtis attribution drift already on file.)

Full 07-07 credit actions: **MSFT → UNDERWEIGHT** (on ~$190bn CY26 capex and no bond-market access) · **META → Neutral** · **ORCL → Overweight** · GOOG/AMZN unchanged OW.

- 🔴 **Two IG credit desks, opposite signs on the same mechanism:** JPM (07-07) credits Oracle's **chip prepayments** with *improving* the funding profile; **MS (08-25, on the page) calls the same $4.6bn of customer prepayments economically DEBT.**
- ⚠️ **Sign conflict inside Oracle's own ATM debate:** the credit desk lists *"a shift away from equity funding"* as a **risk to its Overweight** — it *wants* the ~$20bn ATM; the equity side of the page treats the same ATM as dilution overhang. Both carried.

### 10. ⚠️ InP routing INVERSION — cuts against the moat LITE and COHR both run on

The in-tray entry bar, attributed to **LITE's own CTO at ECOC 2025** ($0.10/Gbps, <4 pJ/bit, <1 FIT, >2 Tbps/mm): *"**silicon photonics and VCSELs are the leading candidates** at this tier, while **InP and TFLN fall short on density and power**."*

➤ **The opposite routing from the DAMNANG block sitting directly above it on `optical-cpo`** (scarcity binds *"at the substrate and the light source"*; three firms hold 80-90% of InP). **Logged in both directions, NOT netted** — different chains on different clocks (today's pluggable/CPO vs a 2029-30+ in-tray tier).

⚠️ **Scale-in dating discipline:** first scale-in product is **two to three years after** the 2027 scale-up-optics ship = **2029-2030+**. **Nothing in LITE's FY27/FY28 bridge depends on it and it must not be underwritten into one.**

### 11. ⚠️ China memory — the derating argument, and the constraint is mis-located on the wiki

- **CXMT** wafer capacity may exceed **Micron by 2028 → #3 DRAM** (basis now stated: **wafer capacity**, rank **CXMT #3 / MU #4**); **YMTC ≥100k wafers/yr → potentially #2 NAND above SK hynix by 2028-29**. **2Q gross margin 87.6%**, mature-product yield **>90%**; 3Q pricing at a **5-10% discount** to global at the Chinese government's request (temporary).
- 🔴 **EUV mis-locates the constraint.** The 08-31 CXMT-HBM3E block framed US equipment restrictions as the cap. Chan: **12-Hi HBM (24GB) is reachable via wafer-on-wafer on DUV + hybrid bonding with NO EUV** (5,600MHz today → 8,000MHz target); **EUV isn't needed until 1B/~12nm and CXMT is ~16nm**. The real bear case to his own thesis is **DUV shipment continuity**, not EUV.
- **Derating mechanism:** nobody accepts share loss → capex/R&D forced up → less operating leverage → lower through-cycle margin → lower sustainable ROIC. Anchor: **Dec-2017, industry >70% OP margins, Korean stocks never above 2x book**; this cycle reached ~4x. **Against** the page's JPM *"<4x P/E … upside risk"* (09-01) and KB-via-Jefferies *"4x P/E → valuation normalisation"* (08-20).
- ⚠️ **Two MS analysts disagree on 3D DRAM on the SAME CALL** (Chan: "wild card", base case small production end-2028 · Kim: "really hard"). Preserved, not smoothed.

### 12. ⚠️ Demand-side ceiling nobody on the wiki had priced: **server units capped at ~+30% next year by NON-memory shortages**

Single-source Japanese **aluminium capacitors**, **47µF MLCC**, **ABF substrate**, MOSFETs. Against the page's 08-20 frame (required server bit growth 50-70% vs commitments high-teens-to-low-20s) this **closes part of that gap from the demand side**.

⚠️ **De-spec now has a FOURTH position with a DIFFERENT driver:** Kim says **affordability**, not supply allocation — and extends it to **SOCAMM**, plus **next-year iPhone 12GB → ~9GB**. 🔴 **Direct same-date collision:** SemiAnalysis says Nvidia **locked a long-term SOCAMM agreement** with SK hynix.

⚠️ **SEMCO/Murata ≠ Samsung Electronics** — the MLCC item is carried only as a server-unit constraint with an entity guard on three pages; the transcript's unnamed *"big LTA announcement today"* was **dropped as unattributable rather than guessed**.

### 13. ⚠️ BKNG — Bernstein is the lowest PT on the page and the only one below spot

**Bernstein MARKET-PERFORM, PT $188** vs 27-Aug close **$202.56 (−7%)**, behind JPM OW $236 · MS OW $230 · GS Neutral $225 · Barclays OW $210 (all 08-04/05). Note dated **08-28** — logged as historical, nothing superseded.

Bernstein EPS 2026E **$10.44** / 2027E **$12.05**. ⚠️ **Do NOT anchor these to the snapshot's BKNG `eps` field — it is one of the three broken ones** (see the defect box). On Bernstein's own basis this is **a valuation call, not an estimate call**.

🔴 The disclosure that matters: Google's group PM for Search **James Byers on the record** that Google not being merchant of record / not handling customer service **"may change"**, and Google passes only *"strictly necessary"* data with *"no insight into the context of the booking"* — **cuts the proprietary-intent-data leg of Fogel's bull case.** Booking −3%, Expedia −4%.

---

## CONFIRMS — no action

| # | Datapoint | Baseline | Result |
|---|---|---|---|
| 1 | **TSM** consensus CY2026 EPS **NT$103.75** (NI-derived, ordinary) | house **NT$102.50** | ✅ **+1.2%** — the apparent 5x gap was the ADS artifact |
| 2 | **TSM** consensus CY2027 **NT$142.46** (NI-derived) | house **NT$143.50** | ✅ **−0.7%** |
| 3 | **NVDA** house 2027 EPS **$15.44** | consensus **$15.39** | ✅ **+0.3%** |
| 4 | **META** house 2027 rev **$313bn** / EPS **$38.24** | consensus **$304.8bn / $36.63** | ✅ +2.7% / +4.4% |
| 5 | **LITE** house 2027 rev **$8.1bn** / EPS **$30.02** | consensus **$7.95bn / $28.08** | ✅ +1.8% / +6.9% |
| 6 | **MSFT** BofA's stated **28x CY27E** | snapshot-derived **28.1x** | ✅ reproduces exactly |
| 7 | **CRM** Rothschild FY27 EPS **$13.48** (period-decoded) | consensus **$13.38** | ✅ **+0.7%** — a 6-month-old model still on consensus ⇒ **his PT cut was a DE-RATING, not an estimate cut** |
| 8 | **SAMSUNG** KRW 90-110trn / ~30trn dividends / 15trn employee buyback | page's 08-21 company disclosure | ✅ exact; resolves the 100-150trn press range at the low end |
| 9 | **SK hynix** ">50% of FCF, detail at 3Q26" | page | ✅ confirmed |
| 10 | Samsung 2027 HBM step-up **+98%** | page's UBS +90% vs JPM +42% spread | ✅ corroborates the high side |
| 11 | NVDA→LITE **$2bn**, NVDA→COHR **$2bn @ $257** (Mar-2026), Celestial AI **$3.25bn**, GOOG-MRVL warrant **$120bn = 240 × $500m / 58,970,907 sh @ $206.58**, MRVL **~$1bn** FY27 prepayments | page primaries (8-K, 10-Q, calls) | ✅ all corroborate; **primaries stand, nothing overwritten** |
| 12 | SKT **2GW DSX** AI factory | page's 08-19 "SK Hyper" item | ✅ same commitment, **double-count guard written in** |
| 13 | DELL FY27 revenue guide **$192bn** | consensus street-high **$194.88bn** | ✅ inside — the revenue line is NOT the disagreement |

---

## ⏳ PENDING — re-run when the Terminal is back

1. **All broker-PT-vs-consensus-PT placements.** `estimates.json` has no `BEST_TARGET_PRICE`. Affects: **ASML** €2,500/$2,859 (reiterated) · **MSFT** BofA $600 · **BKNG** Bernstein $188 · **META** BofA $835 (superseded by same-analyst $810/$800) · **BofA MSFT prior $500**.
2. **DELL post-print consensus.** The snapshot is pre-revision by ~85 minutes. The +43%/+47.7% gaps above measure *guide vs the Street's pre-print view*; re-measure after the Street revises to see how much closes.
3. **A live re-pull will NOT fix the CY2026 pre-print-consensus defect** (already proven 08-03) nor the three broken `eps` fields — those need the fetch script corrected, not re-run.

---

## Process notes from this run

- **8 parallel patch agents, file-disjoint.** Audit results: **0 files changed EOL convention class** (LF-only stayed LF-only, CRLF-only stayed CRLF-only, and both MIXED files kept their anomaly count exactly: `optical-cpo` 8→8, `semicap-wfe` 12→12); **0 newly-introduced table-column mismatches** across **62 added table rows**; **17 pre-existing mismatches left untouched** (ORCL L200, META L301/L801-803 and others are rows **missing their trailing `|`**; `MEDIATEK.md` L396 is a **broken multi-line row** — a class the column audit cannot see, since continuation lines don't start with `|`). Worth a dedicated formatting pass; not mixed into an ingest run.
- ⚠️ **A briefing error of mine was caught by an agent rather than propagated:** I told the META/themes agent the SemiAnalysis note carried a *"1GW+ compute deal with Nvidia"* belonging to Korea's programme. **It belongs to Thinking Machines** ($2bn at $12bn post), cited only as a resource comparator against Motif's 768 B200s. Nothing was written on the bad premise; recorded in the Changelog so it isn't reintroduced.
- **Korea programme uses $919bn**, not the headline *"Trillion-Dollar"*.
- **Two unrelated $200bn now sit on GOOG.md** — MS *"$200bn of 1P TPU revenue"* (08-24, the '27+'28 **sum**) and the FT's **$200bn contract notional** on the Anthropic programme. **Must not be merged.**
- **Four quantities, one programme — held apart, never netted:** ① **>$150bn** chip/hardware *value* · ② **~$200bn** contract *notional* · ③ **~$50bn** *debt raised* · ④ **$35bn** *purchase price* for the first ~1GW. **No unit chaining:** $128bn ÷ 3.5GW ≈ $36.6bn/GW is AVGO's **purchase price for complete Google rack systems** — not comparable to AVGO content at $10-20bn/GW (Hock) or Jefferies' $11bn/GW; $35bn ÷ 1GW is a grossed-up **sale price**, not a build cost.
- **Unresolved 3-way, none adopted:** TeraWulf/Lake Mariner = **360MW** (FT 08-04) vs **366MW** (Barclays FICC 08-20) vs **378MW critical IT** (Epoch 08-12) — on an **identical $3.2bn of debt**. Different power bases; no source states its basis.
- **Two YMTC numbers in ONE transcript**, both kept, explicitly not averaged: prepared remarks *"≥100,000 wafers every year"* vs Q&A *"50,000 wafers, new capacity for next year"*.
- **Unit hazard caught on NVDA:** Lumentum's **14.4 Tbps (one-way)** and NVDA's **3.6 TB/s (both-ways)** are the **same link**, carried from two sources.
- **"Google is dropping HBM"** (08-01, theme page) is **refuted** — 8th-gen TPUs still use HBM3e.
- **GS "Decoding the Agentic Economy" (05-05) logged as failed-or-unproven:** the cost leg (60-70% p.a. cost/token decline) held; the *"token prices stabilising / margin inflection in 1H26"* leg is contradicted by the page's own later measured series. **All nine of its PTs kept OUT of company pages.**
