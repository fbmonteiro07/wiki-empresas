# Reconciliation — 2026-09-01 (/run-inbox, scheduled 23h)

_Every NEW quantitative datapoint from this run, placed against three baselines: **(1)** prior wiki marks on the page, **(2)** the Capstone house model where one exists, **(3)** BBG consensus._

> **BBG status: ⚠️ LIVE WRAPPER DOWN — consensus is an ON-DISK SNAPSHOT, not a live pull.**
> `bdp` raised `ConnectionError: blpapi could not start session` (`Failed to connect to 127.0.0.1:8194`, 3 retries) at 23:30 — **Terminal not logged in at this hour.** Per the skill, no web data was substituted.
> Consensus below is `_wiki\_data\estimates.json`, **`asof: 2026-09-01`, file written 18:30:18 BRT** — the same trading day, so it is *usable*, but it is **~85 minutes after the DELL print (16:05 ET / 17:05 BRT) and therefore PRE-REVISION**: it still carries the Street's pre-print estimates for Dell. That is exactly the right baseline for a guide-vs-Street gap and exactly the wrong one for "where does the Street sit now". **Re-run the PT placements when the Terminal is back** — `estimates.json` carries **no `BEST_TARGET_PRICE`**, so no broker-PT-vs-consensus-PT placement was possible this run (marked ⏳ PENDING-PT below). ✅ **BOTH CLAUSES OF THIS NOTE ARE NOW SPENT:** the PT placements were made on 09-02 (§1 of the layer below) and re-confirmed 09-03, and **`estimates.json` HAS carried `BEST_TARGET_PRICE` since 2026-09-03** — the `⏳ PENDING-PT` marker in §4 is struck. Read this paragraph as a record of the 09-01 state, not as an open instruction.

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

🔴🔴 **CORRECTION 2026-09-02 — TWO OF THE THREE `eps` "DEFECTS" ABOVE ARE NOT DEFECTS. THEY ARE STOCK SPLITS, AND THE BOX'S "real count" COLUMN IS THE THING THAT WAS WRONG.** Settled with a live BBG `EQY_SH_OUT_ACTUAL` pull (2026-09-02), not from memory:

| name | box claimed "real count" | **BBG `EQY_SH_OUT_ACTUAL`** | `mktcap`/`px` | `ni`/`eps` | implied P/E | verdict |
|---|--:|--:|--:|--:|--:|---|
| **TSM** | 25,930m ordinary | **5,186,474,000 ADS** | 5,186.5m | 5,173.1m | — | ✅ **BOX CORRECT** — per-ADS 5:1 |
| **NOW** | ~208m | **1,034,000,000** | 1,034.0m | 1,028.2m | **34.1x** | ❌ **BOX REFUTED** — `eps` 4.06 is right |
| **BKNG** | ~32m | **751,380,500** | 751.4m | 766.5m | **19.3x** | ❌ **BOX REFUTED** — `eps` 10.29 is right |

➤ **The test was run backwards.** For NOW and BKNG, `mktcap/px` and `ni/eps` — two independent fields from the same pull — **agree to within 0.6% and 2.0%**, and the resulting P/Es (34.1x ServiceNow, 19.3x Booking) are ordinary. The box instead trusted a **remembered, pre-split** share count and declared the internally-consistent BBG data broken. Its "corrected" figures are the artifacts: **$20.04 for NOW is a 6.9x P/E** and **$246.6 for BKNG a 0.8x P/E**. The "447x P/E" cited as proof of breakage came from pairing a post-split EPS with a pre-split price anchor. ✅ **`eps` is USABLE for NOW and BKNG.** TSM's entry stands — and its true hazard is compound: **per-ADS *and* `ni`/`eps` in TWD while `px`/`mktcap` are USD** (so the raw pair prints a nonsense 0.8x P/E).

⚠️ **A REAL trap was found while running the test, and it is the opposite of the one the box describes: `EQY_SH_OUT` IS THE UNRELIABLE FIELD ON MULTI-CLASS STRUCTURES.** For **DELL** it returns **325.0m — the Class C line only** — while `CUR_MKT_CAP`/`px` **(646.1m)** and `ni`/`eps` **(650.9m)** both give the all-class count. Had DELL been screened on `EQY_SH_OUT`, its EPS would have been declared 2x broken and this run's headline lost. **Standing rule: test `ni/eps` against `mktcap/px` — same pull, both all-class — never against a share count from memory, and never against `EQY_SH_OUT` alone.**

**House-model coverage** (`_wiki\_data\house.json`, asof 2026-09-01): AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM. **Absent for this run's other names** — DELL, MSFT, ASML, SKHYNIX, SAMSUNG, MU, ORCL, CRM, NOW, MRVL, INTC, MEDIATEK, BKNG — so those get baselines (1) and (3) only.

---

## Where the new data DIVERGES

### 1. 🔴🔴 DELL — the Street's error was the MARGIN, not the revenue, and the guide sits **+6.5% above the FY27 consensus median** — but **NOT above the street high** (basis-corrected 09-02; the quarterly leg closed inside one session)
➤ **The edge, correctly based: DELL's FY27 EPS guide of $25.50 is +6.5% above the BBG annual median of $23.94 with the street high still $2.7bn/share of EPS above it at $28.60 — so the bull case is NOT exhausted by the guide; and consensus models FY28 EPS +19.0% and FY29 +20.2%, i.e. the Street does not treat FY27 as peak earnings, which management declined to answer.**


Management guide (Q2 FY27 call, 2026-09-01) vs pre-revision consensus:

| Metric | **Dell guide** | Consensus **median** | vs median | Consensus **STREET HIGH** | vs high |
|---|--:|--:|--:|--:|--:|
| F3Q27 revenue | **$49.0bn** | $41.91bn | 🔴 **+16.9%** | $56.45bn | inside |
| F3Q27 EPS | **$6.50** | $4.547 | 🔴 **+43.0%** | **$6.50** | 🎯 **exactly ON the high** |
| FY27 revenue | **$192bn** | $164.91bn | 🔴 **+16.4%** | $194.88bn | just inside |
| FY27 EPS | **$25.50** | $17.26 | 🔴 **+47.7%** | $22.15 | 🔴🔴 **+15.1% ABOVE the high** |

⚠️ **Period-basis caveat, and it matters:** `estimates.json` labels Dell's **fiscal Q3 FY27 as "Q3-26E"** and its **FY27 as "CY2026"** (`lrq 2026-07-31`). Dell's FY27 ends ~Jan-2027, so the CY2026 block is the closest available comparator but is a **mixed basis** (`n_actual = 2`). The quarterly row is the clean comparison; the FY row is directional. **Derive the period from `lrq`, never from the label.**

🔴 **THE READ: on revenue the Street's most bullish analyst is already above Dell's own guide; on EPS not one analyst reaches it.** The whole distribution is mis-specified on margin, not on demand. Management then supplied the mechanism the bulls lacked — the ISG margin bridge is **scale**: *"just over **400 basis points**"* in Q3 and *"over **650 basis points**"* for the full-year guide, with the **ISG rate guided UP even as AI-server revenue triples to $74bn**.

✅ **RESOLVED 2026-09-02 — THE STREET REVISED ONTO THE GUIDE INSIDE ONE TRADING DAY, AND THE 09-01 READ WAS RIGHT ABOUT *WHY*.** `estimates.json` refreshed **asof 2026-09-02** (99/99 live). The quarterly gap did not narrow — it **closed**:

| Metric | **Dell guide** | median 09-01 (pre) | median 09-02 (post) | **guide vs post-median** | high 09-02 | **guide vs high** |
|---|--:|--:|--:|--:|--:|--:|
| F3Q27 revenue | **$49.0bn** | $41.91bn | **$49.21bn** | ✅ **−0.4%** | $49.72bn | inside (−1.5%) |
| F3Q27 EPS | **$6.50** | $4.547 | **$6.515** | ✅ **−0.2%** | $6.63 | inside (−2.0%) |
| F3Q27 gross margin | — | 17.60% | **19.07%** | **+147bp revised UP** | — | — |

➤ **The +43.0% EPS gap became −0.2% in one session, and the mechanism was the one the 09-01 read named: MARGIN.** Consensus F3Q27 gross margin was revised **+147bp** (17.595% → 19.065%) and CY26 **+70bp** (17.6% → 18.3%). Meanwhile the revenue **street-high came DOWN 11.9%** ($56.45bn → $49.72bn) as the median rose **+17.4%** — i.e. **the distribution collapsed onto the guide from both sides.** The 09-01 finding was not wrong; it was **arbitraged within 24 hours**. Moved to **CONFIRMS** as a *closed* call, not a failed one.

🔴🔴 **BUT THE FY LEG SURVIVES — AND ON THE CLEAN ANNUAL BASIS IT POINTS THE OPPOSITE WAY FROM THE CY-SUM.** The 09-01 table read FY27 off the **CY2026** block, which this report correctly flagged as mixed-basis (`n_actual=2`). An ad-hoc **`BEST_FPERIOD_OVERRIDE=1FY`** pull returns the genuine BBG **annual** line, and DELL's `EQY_FISCAL_YR_END` of `01/2026` confirms **1FY = FY27 (ending Jan-2027)** — corroborated by BBG annual revenue **$191.17bn** against the company's own **$192bn** FY27 guide (+0.4%):

| FY27 metric | **Dell guide** | **BBG ANNUAL (1FY)** | vs annual | **BBG annual HIGH** | vs high | CY2026 CY-sum | vs CY-sum high |
|---|--:|--:|--:|--:|--:|--:|--:|
| Revenue | **$192.0bn** | **$191.17bn** | **+0.4%** | $200.65bn | ✅ **inside (−4.2%)** | $181.57bn (+5.8%) | 🔴 $188.15bn → **+2.1% ABOVE** |
| EPS | **$25.50** | **$23.94** | **+6.5%** | **$28.60** | ✅ **−10.8% BELOW the high** | $21.40 (+19.2%) | 🔴 $23.85 → **+6.9% ABOVE** |

🔴🔴 **THE CY-SUM-VS-ANNUAL WEDGE FLIPS THE SIGN OF THE STREET-HIGH COMPARISON ON BOTH LINES — a 17.8pp swing on EPS.** The CY-sum says the guide is **above** the street high on revenue *and* EPS (the shape of the 09-01 headline); the genuine annual line says it is **comfortably inside on both** (−4.2% and −10.8%). The CY-sum understates the annual line by **−5.0% on revenue, −10.6% on EPS and −16.6% on the EPS high**. ⚠️ **This is the third name on which this wedge has inverted a conclusion (after CRM and META) and the first where it did so on a company's own guide. Never place an off-calendar FYE against a `CY20xx` block — pull the `1FY` annual override.**

➤ **The surviving, correctly-based edge is therefore NOT "the guide beats the street high" — it is that the guide sits 6.5% above the median with EPS headroom still above it.** The bull case is not exhausted by the guide.

✅ **AND THE ANNUAL PULL ANSWERS THE ONE QUESTION MANAGEMENT DECLINED.** Melius asked whether FY27 is peak earnings and management **refused** (§1). Consensus answers it: **FY28 EPS $28.48 (+19.0% on FY27) and FY29 $34.23 (+20.2%)**, on revenue **$226.97bn (+18.7%)** then **$258.99bn (+14.1%)**. **The Street does not model FY27 as peak** — so "is FY27 peak earnings?" is a live short thesis *against consensus*, not a question consensus shares. FY29 EPS high **$53.61** is 57% above the FY29 median: the dispersion has moved out to FY29.

✅ **Open item (d) was ALREADY CLOSED by the management primary on 09-01 — the carry-forward line listing it as open was itself stale, and consensus now independently corroborates the primary.** `DELL.md` records the CFO verbatim (*"For Q3, we expect revenue to be **$49 billion at the midpoint**"*, David Kennedy, Q2 FY27 call), which settled **Barclays $49.0bn right / UBS $46.76bn wrong** on the day. **The primary is the adjudicator; this layer only adds a second, independent check** — post-print consensus converged to **$49.21bn**, within **0.4%** of Barclays and **5.2% above** UBS. ⚠️ **Recorded because the order matters: convergence of consensus is corroboration, never a substitute for the company's own words.**

⚠️ **DELL PT baseline, now on file:** consensus PT **$570.70** (high $735 · low $428) vs spot **$448.06** = **+27.4%** implied; 31 analysts, **21 buy / 10 hold / 0 sell**. This places the one DELL PT that reached the wiki through the DB relay — **$480** — at **−15.9% BELOW the consensus median** and only **65.3% of the street high**, i.e. a Buy rating carrying a bottom-quartile target.

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
- **Rating/PT reiterated, NOT changed:** Outperform, **PT €2,500 / ADR $2,859**, 40x Q5-8, EPS €24.72/38.91/53.56 — identical to 07-30. ✅ **PT RESOLVED** — placed in full under §1 of the 09-02 layer below, and **re-confirmed unchanged on a fresh 2026-09-03 pull of both listings**: the **€2,500 IS `BEST_TARGET_HI` on the Amsterdam line to the decimal (+23.3% above the €2,027.47 median, +75.5% above a €1,424.40 spot)**, and the **$2,859 IS `BEST_TARGET_HI` on the ADR to the decimal (+17.4% above the $2,435.80 median)**. Both medians and both highs are **identical to 09-02** — the tape has not moved on ASML in a session. ⚠️ **Never net the two panels: Amsterdam polls 42 analysts, 36/4/**2 SELLS** (rating 4.62); the ADR polls 21, **21/0/0, zero sells** (rating 4.95).**

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
| 13 | DELL FY27 revenue guide **$192bn** | consensus street-high **$194.88bn** (pre-print CY-sum) | ✅ inside — the revenue line is NOT the disagreement. ⚠️ **BASIS CORRECTED 09-02: this baseline was the CY-sum high, which post-revision FELL to $188.15bn — on which the guide would read +2.1% ABOVE. The conclusion survives only on the genuine BBG ANNUAL high of $200.65bn (guide −4.2% inside).** ⇒ §1 |
| **14** | ✅ **MOVED FROM DIVERGES 09-02** — DELL **F3Q27 revenue** guide **$49.0bn** | **post-revision** consensus median **$49.21bn** (asof 09-02) | ✅ **−0.4%** — was +16.9% against the pre-print median. **The Street revised onto the guide in one session.** ⇒ §1 |
| **15** | ✅ **MOVED FROM DIVERGES 09-02** — DELL **F3Q27 EPS** guide **$6.50** | **post-revision** consensus median **$6.515** (asof 09-02) | ✅ **−0.2%** — was +43.0%, and the gap closed through a **+147bp gross-margin revision**, i.e. via exactly the mechanism the 09-01 read named. **Correct call, arbitraged inside 24h.** ⇒ §1 |
| **16** | DELL **FY27 EPS** guide **$25.50** | **BBG ANNUAL (1FY)** high **$28.60** | ✅ **−10.8% INSIDE the street high** — the *opposite sign* to the CY-sum's "+6.9% above". **The 09-01 headline's street-high claim does not survive a correct-basis test; the +6.5%-above-median edge does.** ⇒ §1 |
| **17** | **BKNG** Bernstein EPS **2026E $10.44 / 2027E $12.05** | BBG annual **FY2026 $10.461 / FY2027 $12.371** | ✅ **−0.2% / −2.6%** — essentially ON consensus, against a PT **21% below the median**. **Quantifies §13: the divergence is ~100% multiple, ~0% estimates.** Placeable only because the `eps` field was cleared of the false defect. |
| **18** | **ASML** broker EPS ladder **€38.91 / €53.56** | BBG annual **FY2026 €37.84 / FY2027 €52.14** | ✅ **+2.8% / +2.7%** — the street-HIGH €2,500 PT rests on a **40x multiple**, not on above-Street earnings (€2,500÷40 = €62.50, between FY27 and FY28 ✓). ⚠️ *year-mapping inferred, not stated in the note.* |
| **19** | **MSFT** BofA's stated **28x CY27E** | refreshed CY2027E EPS **$21.34** | ✅ **28.1x reproduces exactly** on the 09-02 vintage (was $21.32 → 28.1x). The multiple is confirmed; §5's read that **the $600 is financed entirely by it** stands. |

---

## ✅ PENDING — RESOLVED 2026-09-02 (Terminal live, `estimates.json` asof 2026-09-02)

**1. ALL BROKER-PT-vs-CONSENSUS-PT PLACEMENTS — CLOSED.** `estimates.json` still carries **no `BEST_TARGET_PRICE`** (unchanged script defect), so these come from an ad-hoc live pull of `PX_LAST / BEST_TARGET_PRICE / BEST_TARGET_HI / BEST_TARGET_LO / BEST_ANALYST_RATING / TOT_{BUY,HOLD,SELL}_REC`, **2026-09-02**:

| Name | Broker PT | **BBG cons. PT** | vs median | **street HIGH** | vs high | **street LOW** | spot | placement |
|---|--:|--:|--:|--:|--:|--:|--:|---|
| **ASML** (NA, EUR) | **€2,500** | €2,027.47 | **+23.3%** | **€2,500.00** | 🎯 **IS the high** | €1,291 | €1,440.60 | most bullish PT on the Street |
| **ASML** (US ADR) | **$2,859** | $2,435.80 | **+17.4%** | **$2,859.00** | 🎯 **IS the high** | $2,100 | $1,669.65 | most bullish PT on the Street |
| **MSFT** BofA | **$600** | $572.23 | **+4.9%** | $870 | only **69.0%** of high | $400 | $497.80 | ⚠️ barely above median |
| **MSFT** BofA *prior* | **$500** | $572.23 | **−12.6%** | $870 | 57.5% of high | $400 | $497.80 | ⚠️ **+0.4% from spot** |
| **META** BofA | **$835** | $745.22 | **+12.0%** | $1,000 | 83.5% of high | $580 | $595.33 | above-Street |
| **META** BofA *superseded* | **$810 → $800** | $745.22 | **+8.7% → +7.4%** | $1,000 | 80.0% of high | $580 | $595.33 | a **−4.2% walk-down**, still above-Street |
| **BKNG** Bernstein | **$188** | $238.03 | **−21.0%** | $301 | 62.5% of high | **$188.00** | $198.58 | 🎯 **IS the street LOW** |
| **DELL** (DB relay) | **$480** | $570.70 | **−15.9%** | $735 | 65.3% of high | $428 | $448.06 | bottom-quartile Buy |

🔴 **THE CROSS-CUTTING FINDING: THREE OF THESE FOUR CALLS ARE PURE MULTIPLE CALLS — THE ESTIMATES AGREE AND ONLY THE RATING DOES THE WORK.**

- 🎯 **ASML — the €2,500 IS the street high to the decimal, on BOTH listings, yet the EPS is within 3% of consensus.** Matching the note's €24.72/38.91/53.56 ladder onto the live annual overrides (FYE 12/2025 ⇒ 1FY = FY2026) implies the three figures are **2025/2026/2027**: **€38.91 vs BBG FY2026 €37.84 = +2.8%** and **€53.56 vs FY2027 €52.14 = +2.7%**. And the stated **40x on Q5-8** reproduces: €2,500 ÷ 40 = **€62.50**, which sits between BBG FY2027 €52.14 and FY2028 €66.94 ✓. **The street-high target is financed entirely by a 40x multiple, not by above-Street earnings.** ⚠️ *The year-mapping is INFERRED from a two-year +2.7/+2.8% fit — the note does not label the years. Flagged, not adopted.*
- 🔴 **MSFT — and here the resolution cuts AGAINST the note's framing.** The 09-01 write-up headlined BofA's $600 as a rare **multiple** upgrade (24x → 28x). Against the tape it is **+4.9% above the median and $270 below the street high** — a bull-case target only 69% of the way to the actual bull case. Set beside §5's finding that BofA sits **BELOW** consensus on the earnings, the note is **below-Street on numbers and barely above-Street on price**: materially less bullish than it reads. ⚠️ **And the prior $500 was 0.44% from spot — fully consumed by the tape.** A raise that restores 20.5% of upside from a PT the market had already reached follows price rather than leading it. The stated **28x reproduces exactly on refreshed data: $600 ÷ CY2027E EPS $21.34 = 28.1x** ✓ (was $21.32).
- 🎯 **BKNG — Bernstein's $188 is not merely "the lowest PT on the page" (09-01 §13); it is the lowest PT ON THE STREET, equal to `BEST_TARGET_LO` to the cent.** And the estimate leg is now measurable, because the `eps` field is **not** broken (see the correction above): **2026E $10.44 vs BBG CY2026 $10.29 (+1.5%) / annual FY2026 $10.461 (−0.2%)**; **2027E $12.05 vs CY2027 $12.28 (−1.9%) / annual FY2027 $12.371 (−2.6%)**. 🔴 **So ~100% of a −21% PT divergence is MULTIPLE and ~0% is estimates** — the exact conclusion §13 could only assert as a caveat while believing the data unusable. ⚠️ Note also that with **41 analysts and ZERO sells**, Bernstein holds the tape's lowest target from inside the 9-name *hold* bucket.
- **META — BofA stays above-Street throughout its own walk-down.** $835 → $810 → $800 is a **−4.2%** cut by the same analyst, ending **+7.4% above** a $745.22 median. Context: the street **low of $580 is BELOW the $595.33 spot**, so the Street's own bear is already in the money.

⚠️ **NEW BASIS HAZARD FOUND WHILE RESOLVING THIS — ASML HAS TWO DIFFERENT ANALYST PANELS AND THEY DO NOT AGREE.** The Amsterdam line (`ASML NA`) carries **42 analysts, 36 buy / 4 hold / 2 SELL, rating 4.62**; the ADR (`ASML US`) carries **21 analysts, 21 buy / 0 hold / 0 sell, rating 4.95**. **The ADR panel is structurally more bullish and contains no sells at all.** Any "ASML consensus PT upside" quoted off the ADR is a different, smaller, more bullish poll than the primary listing's — **never net or substitute the two.** (The PT pair itself is coherent: $2,859/€2,500 implies EURUSD **1.1436** vs the spot-implied ADR/local ratio of **1.1590**, a 1.3% FX drift since the note; ASML's ADR is 1:1 with the local line.)

**2. DELL POST-PRINT CONSENSUS — CLOSED.** ⇒ resolved in full under §1 above: the quarterly gap **closed from +43.0% to −0.2%** inside one session via a **+147bp** margin revision, while the FY leg **flipped sign** between the CY-sum and the genuine annual basis.

**3. THE THREE `eps` FIELDS AND THE CY2026 PRE-PRINT DEFECT — PARTLY RETIRED, PARTLY STANDING.**
- ✅ **RETIRED:** the NOW and BKNG `eps` entries were never defects (splits — see the correction block above). **No script change is needed for either.**
- ✅ **STANDING ITEMS (a) AND (b) ARE FIXED IN THE SCRIPT AS OF 2026-09-03 — they will not recur.** (a) `estimates.json` now carries a **`pt` block per name** (`BEST_TARGET_PRICE` / `_HI` / `_LO` / `BEST_ANALYST_RATING` / `TOT_{ANALYST,BUY,HOLD,SELL}_REC`) for all 100 names — **the fourth consecutive run would have paid the ad-hoc cost; instead the field was added.** (b) BBG's **own annual `1FY/2FY/3FY` consensus lines** (rev/ebit/ebitda/ni/eps/gm/capex + `_hi`) are now fetched alongside the CY sums, so any fiscal-year claim — and every off-calendar-FYE name like DELL — has the correct basis on file without an ad-hoc pull, and **FY3 is reachable at all** (there is still no CY2028 aggregate). Validation: the new annual lines reproduce this report's own 09-02 ad-hoc pull **exactly** — ASML 1FY €37.839 / 2FY €52.135 / 3FY €66.941 against the €37.84 / €52.14 / €66.94 recorded in §1 — and reproduce the 09-02 reference table to **≤0.2% on 6 of its 7 names**. ⚠️ **(b) is a NEW-DATA fix, not a retro-fix: the CY-sum wedge itself is unchanged and still drifts by name AND by year** — measured across all 100 names this run, **59 of 197 year-pairs differ by ≥5%**, with the sign INVERTING between names (MU CY26 **+26.0% ABOVE** its annual line, SNDK **−26.3% BELOW**; POET −44.7%, LITE −27.9%, STX −20.0%, AVGO **+16.4%**). **Never hard-code a correction factor; read the annual line.** (c) ⏳ **STILL STANDING, AND WORSE THAN LOGGED: the currency mismatch is NOT "TSM only".** It is **five names**, and the new `pt` block **inherits it**, because `px` and `pt` are in the TRADING currency while `rev`/`eps` are in the FUNDAMENTALS currency: **TSM** (USD px vs TWD eps ⇒ naive PE 0.8), **SMIC** (HKD vs USD ⇒ 358.2), **ASML** ADR (USD vs EUR ⇒ 44.3 not ~38.2), **SPOT** (USD vs EUR ⇒ 47.6), **TM** (USD vs JPY). **`build_wiki_html.py`'s screener computes `pe = px / eps` and therefore renders a wrong PE for these five today.** Not fixed in this run — the fix is a design choice (convert via FX vs suppress the cell) that should not be made unattended. **Never divide `pt` or `px` by `eps` for these five names.**

**4. NOT RESOLVABLE FROM BBG (unchanged, recorded so it is not re-attempted):** the BofA MSFT **FY-June** EPS line has no figure in the primary, so it cannot be placed against the now-on-file annual baselines (**FY27 $19.801 · FY28 $23.527 · FY29 $28.525**); the next MSFT note can be placed directly. ⚠️ **One suspicion raised by those baselines and explicitly NOT adopted:** the 07-07 MS credit action assumed *"~$190bn CY26 capex"*, which is **+23.6% above** BBG's true **calendar** CY2026 capex of **$153.69bn** but within **0.8%** of the **FY-June-2027** line (**$188.55bn**). That pattern is consistent with a **fiscal-labelled-as-calendar** mislabel, but MS's figure is its own estimate and may legitimately sit above consensus. **Both numbers logged; neither adopted; do not net them.**

---

## BBG consensus pull — live PT vs spot (2026-09-02)

_Ad-hoc live pull (`PX_LAST` / `BEST_TARGET_PRICE` / `BEST_TARGET_HI` / `BEST_TARGET_LO` / `TOT_{BUY,HOLD,SELL}_REC`), because `estimates.json` still carries no `BEST_TARGET_PRICE`. Feeds the PT-vs-spot panel of `_meta/edge.md`._

| Ticker | Spot | Cons PT | Street high | Street low | Buy/Hold/Sell | Read |
|---|--:|--:|--:|--:|--:|---|
| **DELL** | 448.06 | 570.70 | 735 | 428 | 21/10/0 | Widest consensus upside in this run. The lone relayed broker PT (**$480**, DB) sits **−15.9% below** this median. |
| **ASML** | 1669.65 | 2435.80 | 2859 | 2100 | 21/0/0 | *(US ADR line.)* ⚠️ **ADR panel only — 21 analysts, ZERO holds or sells.** The Amsterdam line polls **42 analysts incl. 2 SELLS** (PT €2,027.47, high €2,500). **Never net the two panels.** The reiterated **€2,500 / $2,859 IS the street high on both lines.** |
| **META** | 595.33 | 745.22 | 1000 | 580 | 71/7/0 | Street **low ($580) is BELOW spot**. BofA's $835→$810→$800 walk-down still ends **+7.4% above** this median. |
| **BKNG** | 198.58 | 238.03 | 301 | 188 | 32/9/0 | Bernstein's **$188 IS `BEST_TARGET_LO`** — the lowest target on the Street, from inside the hold bucket, with **no sell ratings anywhere**. |
| **MSFT** | 497.80 | 572.23 | 870 | 400 | 68/4/0 | BofA's raised **$600 is only +4.9%** above this median and **69% of the high**; its prior **$500 was 0.4% from spot**. |

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

---

_BBG column resolved 2026-09-02 — `estimates.json` asof **2026-09-02** (**99/99 live, 0 FAIL lines, 0 `error` keys, 0 null/zero prices, 0 `carried_over` stamps**, and only **1 of 99** records byte-identical to the 09-01 vintage — **KIOXIA**, a thin-coverage Japanese listing, i.e. a genuinely unchanged record and not a silent carry-over). Plus two ad-hoc live pulls the same date: **PT/rating/dispersion** for ASML (both listings), MSFT, BKNG, META and DELL; and **`BEST_FPERIOD_OVERRIDE=1FY/2FY/3FY`** annual lines for DELL, MSFT, BKNG and ASML — the annual override being the only correct basis for DELL's off-calendar FY27, and the reason this layer could show that **the CY-sum had inverted the street-high comparison**. Shares outstanding settled with a live **`EQY_SH_OUT_ACTUAL`** pull. **Both `PENDING` items are closed** (item 1 in full, item 2 in full); item 3 is split into one **retired** half and one **standing script-level** half. **DELL's quarterly leg moved DIVERGES → CONFIRMS** (closed by revision inside 24h, not falsified), while **DELL's FY leg stays in DIVERGES with its sign corrected**. **Two claimed data defects (NOW, BKNG) were refuted and their `eps` fields readmitted** — which is what made the BKNG placement, the sharpest CONFIRMS in this layer, possible at all. **No web data was substituted at any point.**_

_BBG column resolved 2026-09-03 — `estimates.json` asof **2026-09-03** (100/100 live, 0 FAIL lines, 0 `error` keys, 0 null prices, 0 `carried_over` stamps, 0 records byte-identical to the earlier same-day 09:10 vintage). This layer closes the **last open `PENDING` marker in the entire 46-file backlog** — the §4 ASML `⏳ PENDING-PT`, which the 09-02 layer had already resolved in its §1 but never struck inline — and closes **standing script items 3(a) and 3(b) by changing `fetch_estimates.py`** rather than logging them a fourth time. Canonical header `## Where the new data DIVERGES` applied (was `## Where the new data DIVERGES — the alpha`). Item 3(c) is **re-opened wider**: the currency mismatch affects five names, not one. **No web data was substituted at any point.**_
