# Reconciliation — 2026-09-03 (/run-inbox, 5 sources)

_Every NEW quantitative datapoint from tonight's ingest, placed against three baselines:
**(1) prior wiki comments** · **(2) Capstone house models** (`_data/house.json`, asof 2026-09-03) ·
**(3) BBG consensus**._

> ⚠️ **BBG BASELINE — READ THIS BEFORE USING ANY NUMBER BELOW.** The Bloomberg Terminal was **offline at run
> time** (23:29, `blpapi: could not start session`), so **no live pull was made**. The BBG column is served from
> the **on-disk snapshot `_wiki/_data/estimates.json`, asof 2026-09-03** — written by today's earlier
> `/wiki-consensus` refresh across 100 names. That is a same-day BBG snapshot, not stale data and **not** a web
> substitute — but it is a *morning* mark against sources dated as late as tonight, and for **AVGO specifically
> it was taken ~1 day after the FQ3 print, while consensus was still migrating.** Treat AVGO consensus as
> in-flight (see D-3). Nothing here is marked PENDING; nothing here came from the web.
>
> **Period discipline applied throughout:** all fiscal-year claims use the BBG **annual `1FY`/`2FY`/`3FY` lines**,
> never the CY sums — the CY-vs-annual wedge inverts by name and has flipped a street-high comparison before.
> GOOG is reconciled **at EBIT, not EPS** (its BBG EPS carries below-the-line items and *falls* while EBIT rises).

---

## DIVERGES — the alpha

### D-1 · 🔴 AVGO — the house FY28 EPS sits ABOVE the entire visible sell-side range
The single most important line of the night. Four independent marks on AVGO's FY28 (fiscal, ending ~Nov 2028)
earnings power now exist, and the house is above all of them:

| Mark | FY28 EPS | vs BBG consensus |
|---|---|---|
| BBG consensus (`3FY`, asof 09-03) | **$28.95** | — |
| AVGO's own guide ("~$30 of earnings power") | ~$30 | +3.6% |
| JPM · Harlan Sur, in print 09-03 | $32-33 | +10.5% to +14.0% |
| BBG **street high** (`3FY eps_hi`) | $34.25 | +18.3% |
| **Capstone house model** (`Modelo Avgo pós 2Q26.xlsx`, 2026-06-10) | **$35.96** | **+24.2%** |

➤ **The house is +5.0% ABOVE the street high and +24.2% above the median.** That is not a disagreement with
consensus — it is a position outside the range consensus is even quoting. The house also runs above consensus in
the two nearer years, but *inside* the high in FY27: FY26 $12.89 vs cons $11.62 (+10.9%, and **+7.2% above the
$12.02 street high**); FY27 $21.07 vs cons $19.08 (+10.4%, −4.3% vs the $22.01 high). **The gap widens as the
years go out** — the house's edge is entirely a back-year call.
**Action:** this is either the best idea on the book or an un-audited extrapolation. The model predates the print
by ~3 months (2026-06-10) and has not been re-marked against the FQ3 guide. **Re-run the AVGO model bridge before
sizing anything off FY28.**

### D-2 · 🔴 AVGO — the house implicitly assumes a ship rate the supply chain is not underwriting
JPM's framing, now on the page: AVGO's **FY27 order book is $140-150bn**, and the supply-constrained ship rate
across NVDA, MRVL and AVGO is **80-85% of book** — which is exactly how you get from the book to AVGO's **$115bn**
guide. The house model carries **AI semis of $132bn in 2027**.

- House $132bn = **88-94% of the $140-150bn order book** — above the 80-85% benchmark JPM applies to the whole group.
- House $132bn is **+14.8% above the company's own guide**; JPM, who calls the guide "extremely conservative",
  only previewed **$130bn** and now models upside off $115bn.
- 2028 is directionally the same but milder: house **$251bn vs the $230bn guide (+9.1%)**, ≈90-93% of the
  $270-280bn book JPM infers.

➤ **The house is not merely above the guide — it is above the guide *for a specific mechanical reason*: it assumes
AVGO converts more of its backlog than the supply chain has been converting.** That is a falsifiable assumption
with a named test (Samsung second-source 2nm/3nm wafers landing in 2H27). ⚠️ Do not read the house's "2026E total
revenue $115bn" as agreeing with the "$115bn FY27 AI revenue" guide — **same number, different year, different
measure.**

### D-3 · ⚠️ AVGO — BBG consensus is internally inconsistent one day after the print
Subtracting the AI guide from BBG **total** revenue leaves a non-AI residual that cannot be right in both years:

| | BBG total rev | less AI guide | implied non-AI |
|---|---|---|---|
| FY27 (`2FY`) | $173.8bn | $115bn | **$58.8bn** |
| FY28 (`3FY`) | $261.9bn | $230bn | **$31.9bn** |

AVGO's non-AI semis + infrastructure software does not shrink by $27bn in a year. ➤ **The most likely reading is
that the FY28 total-revenue line has not yet fully absorbed the $230bn AI guide** (JPM puts pre-print sell-side AI
at $180bn and buyside at ~$205-210bn), i.e. **consensus FY28 AI is still somewhere below the guide**. Re-pull AVGO
once the Terminal is up and re-test this residual — if FY28 total revenue rises toward ~$280bn, consensus has
finished migrating and D-1's gap narrows on its own.

### D-4 · 🔴 CRWV — Jefferies is ~90% above consensus on CY28 EBIT, and the same gap shows up twice
Jefferies says Buy/$150 on "**7x our rolled forward CY28 EV/EBIT**". CRWV's EV in the same snapshot is **$93.3bn**
→ that multiple implies a **Jefferies CY28 EBIT of ~$13.3bn**. BBG consensus `3FY` EBIT is **$7.0bn**.

- **Jefferies EBIT is +90% above BBG consensus.**
- Independent cross-check, same direction: Jefferies expects margins "toward the **mid-20s by 2028**"; BBG's `3FY`
  EBIT margin is **16.6%** ($7.0bn on $42.4bn). ~8pts apart.
- Note the PT itself is *not* the divergence — $150 vs a $145.54 consensus median is +3.1%. **The disagreement is
  entirely in the earnings, hidden behind an in-line target.** (Dispersion is enormous: hi $317, lo $39.)

➤ **This is the cleanest testable divergence of the night.** Two independent routes to the same conclusion, from
one note. If Jefferies is right the stock is cheap on their number; if consensus is right the "7x" is really ~13x.

### D-5 · ORCL — the PT is 18% above consensus, and the stated downside case IS consensus
Jefferies Buy/**$290** vs BBG PT consensus **$245.49** → **+18.1%** (hi $400), px $154.04.
More interesting than the PT: Jefferies' *downside* math is "a ~30% miss on ORCL's FY30E $21 EPS target (to ~$15)
at 15x → a ~$225 stock". **BBG's FY29 (`3FY`) EPS consensus is $15.70.** ➤ **Jefferies' bear case for FY30 is
approximately what consensus already expects for FY29** — i.e. the downside scenario prices a full year of lost
time, not a broken model. That is a much weaker bear case than "30% miss" sounds, and it is the reason the
risk/reward reads as asymmetric. ⚠️ Balance it against what Jefferies itself concedes: net leverage ~4.5x, near
historical highs, on a company with a rating-agency track record that could work against it.

### D-6 · NVDA — both the house AND consensus sit below the company's own growth framing
NVDA IR (via BTG, 09-02) re-states the **~70% FY28 growth** guide and is explicit that it is a **supply**
constraint, not a demand one, with the upside lever being supply unlock.

| | FY28 revenue growth |
|---|---|
| Company framing (IR) | **~70%** |
| BBG consensus (`2FY`/`1FY`) | **+65.3%** ($408.0bn → $674.3bn) |
| Capstone house | **+62.4%** ($407bn → $661bn) |

➤ Consensus is ~5pts below the company; **the house is ~7.6pts below it and ~3pts below consensus.** Given IR
frames 70% as supply-limited (and the page already carries the FY28 guide being called *"a floor"*), the house is
positioned for the conservative case on a name where management is signalling the opposite. ✅ Note the house is
otherwise almost exactly on consensus (FY28 rev −2.0%, **EPS $15.44 vs $15.39, +0.3%**) — so this is a growth-path
disagreement, not a level disagreement.

### D-7 · 🔴 MSFT — Jefferies' M365 series was published one day before the segment restatement and is now ~2pts low
Jefferies models M365 Commercial Cloud y/y growth **13.9% (Sep-26E) → 14.7% → 15.6% → 16.6% (Jun-27E)**, published
2026-09-02. Microsoft's own restatement deck (09-03) mechanically re-based the **same F1Q27 guide from ~15% cc to
~17% cc**, because M365 commercial cloud now absorbs GitHub cloud, other developer cloud services and Security
Copilot out of Azure.
➤ **Any Sep-26 print scored against Jefferies' 13.9% would read as a large beat that is purely definitional.**
The whole Jefferies M365 path needs ~+2pts of re-basing before it is comparable. The same trap runs in the other
direction on Azure — **every Azure growth number on the MSFT page is old-definition** (the +43% print, the ~45% cc
guide, BofA's 41.8% FY27E, the 40.6% Street bar).
⚠️ Related disclosure loss, worth flagging to anyone who models the segments: **LinkedIn and Dynamics 365 are both
retired as separately disclosed metrics** — LinkedIn disappears as a revenue line ($19,817m in FY26).

### D-8 · GEV — a 4GW JV that contributes nothing inside the consensus horizon
The unattributed BTM call puts Chevron's GE Vernova JV at **4GW of turbines**, but **full capacity on the GEV
turbines is not reached until 2031**, with smaller Caterpillar units taking the early ramp and a grid connection
planned for 2030. BBG's furthest annual line for GEV is **`3FY` = FY28** ($60.7bn revenue).
➤ **The entire GEV contribution from the largest announced data-center turbine JV sits beyond the last year
consensus forecasts.** Headline GW ≠ near-term revenue. The inverse test is now logged on the page: **if a future
note models GEV revenue from this JV before 2031, reconcile it against this entry.**

### D-9 · pre-existing house-vs-consensus gaps re-confirmed (not new tonight, but they frame the new sources)
- **GOOG** — house 2026E revenue **$505bn vs BBG `1FY` $432bn (+16.9%)**. Large and long-standing. ✅ But house
  **capex 2027E $310bn vs BBG `2FY` $308.6bn (+0.5%)** is essentially exact — the house disagrees on the revenue
  line, not the spend.
- **META** — house capex 2027E **$170bn vs BBG `2FY` $197.1bn (−13.7%)**. (Annual line used deliberately; the CY
  sum runs ~8-9% higher on META and has produced a false capex divergence before.)
- **GOOG GW vs TPU units — do NOT net these.** House implies Google compute **~4.6GW → ~7.75GW (+68%)** in 2027,
  while JPM has **total TPU units +115%**. Different bases (facility GW vs unit count); the gap is only a
  contradiction if you assume flat GW-per-unit. Flagged as a question, not a finding.

---

## CONFIRMS — no action

| # | Datapoint | Source | Baseline | Result |
|---|---|---|---|---|
| C-1 | **Micron gross margin FY26E ~80%** | Jefferies p27 (Visible Alpha) | BBG `1FY` gm **80.6%** | ✅ **Confirmed to within 0.6pt.** ⚠️ Worth recording *why* this matters: an 80% gross margin looks absurd and this wiki has previously **rejected a broker model on plausibility and been wrong**. It was checked, not rejected. BBG `1FY` EBIT margin is 76.2%, so a ~80% GM is required, not optional |
| C-2 | CRM CY26 revenue $46,146m | Jefferies p52 | BBG `1FY` $46,284m | ✅ **−0.30%.** (⚠️ Jefferies' "CY26" is CRM's *fiscal* year — the CY label lies for an off-calendar FYE; compared against the annual line, not the CY block) |
| C-3 | NOW CY26 revenue $16,196m | Jefferies p52 | BBG `1FY` $16,211m | ✅ **−0.09%** |
| C-4 | AMZN Buy PT $330 | Jefferies p44 | BBG PT cons $329.82 | ✅ **+0.05% — the PT IS the consensus median.** The differentiation is the multiple argument (~11x NTM EV/EBITDA vs GOOGL 15x / WMT 18x), not the target |
| C-5 | MSFT Buy PT $575 | Jefferies p44 | BBG PT cons $571.39 | ✅ **+0.6%.** Also a **reiteration** — the same mark the page has carried since 2026-06-06; no PT superseded |
| C-6 | AVGO "12 times F28 earnings" | JPM, 09-03 | px $357.16 ÷ $30 guide EPS | ✅ **11.9x — arithmetic checks exactly** |
| C-7 | **Neoclouds ~3GW (end-2025) → ~8GW (exit 2026)** | NVDA IR via BTG, 09-02 | The **09-01 Barclays relay** already on the NVDA page | ✅ **Company primary confirms the relay.** Logged as one datapoint with an upgraded attribution — explicitly **not** double-counted as a second mark |
| C-8 | **MSFT restated FY26 Azure $101,938m** | Microsoft primary | Page's "FY26 Azure surpassed $100B for the first time" (old definition) | ✅ **The $100bn milestone survives the redefinition.** Restated growth computed off the disclosed table: +39.7 / +39.2 / +40.3 / +42.0% by quarter, **FY26 +40.4%** |
| C-9 | **The Azure redefinition costs only ~0-1pt** | Microsoft primary p21 | The ~45% cc F1Q27 guide already on the page | ✅ Re-based guide is **44-45% cc** vs ~45% before — far smaller than the amount of revenue that moved out. Restated FY26 *actuals* agree: 40% vs 41% reported |
| C-10 | NVDA house FY28 EPS $15.44 | `house.json` | BBG `2FY` $15.395 | ✅ **+0.3%** (revenue −2.0%) |
| C-11 | GOOG house capex 2027E $310bn | `house.json` | BBG `2FY` $308.6bn | ✅ **+0.5%** |
| C-12 | CRWV market cap "$44bn" | Jefferies (priced 9-2) | BBG mktcap $47.3bn (09-03) | ✅ Consistent with one day of drift |
| C-13 | AVGO FY28 order book ≈ $270-280bn ⇒ guide is ~85% of it | JPM, 09-03 | AVGO's own $230bn guide | ✅ 230/275 = 83.6%, internally consistent with the 80-85% ship-rate framing |
| C-14 | META = 10% of AVGO AI revenue in FY27 and FY28 | JPM, 09-03 | BBG META capex `2FY` $197bn / `3FY` $216bn | ✅ Implies **$11.5bn (5.8% of capex) → $23.0bn (10.7%)** of Broadcom purchases — a plausible share, no conflict |

---

## Cross-source contradictions logged rather than resolved

1. **JPM contradicts itself on Google-internal FY27 TPU growth — four times in one call**: "flat to maybe slightly
   up" (given as the *bears'* framing) · "still growing slightly sequentially" · "about 10, 12% year over year" ·
   "still growing 12 to 15%". Logged on GOOG, AVGO and `custom-asic-tpu` as an **unresolved ~10-15% range with the
   bear low case**; **no point estimate adopted**. 2028 does converge (+30-35% JPM vs the +33% bear number).
2. **AVGO's customer-mix columns sum to 101%** in both 2027 and 2028 as given on the call. Reproduced as stated,
   **not normalised**.
3. **NVDA's Anthropic+OpenAI concentration**: NVDA IR **declined to size it** on the BTG call ("hard for me to
   directly answer"), while the same page carries a JPM virtual NDR **from the same day (09-02)** putting
   OpenAI+Anthropic at **~20% of the business today on an end-consumption basis → ~25% in FY28**. Logged as a
   same-day contrast — the JPM number stands as the page's mark, the refusal stands as evidence the figure is not
   volunteered. **Not a contradiction.**
4. **The $/GW basis argument narrows but does not close.** Hock's callback clarification (that $20-30bn/GW is
   *total hardware infrastructure*, not Broadcom content) resolves the AVGO-internal confusion, but his denominator
   still is not the same as the "total data-centre/system cost incl. power and cooling" denominator used by other
   houses on the page. **Four bases from the JPM call plus a fifth from Jefferies (NBIS $40-50m/MW = contract
   revenue) are now fenced in unit-guard blocks on six pages.**

## Not reconcilable against any baseline (recorded so nobody tries)
- **Anthropic ~$30bn ARR/GW against ~$5bn/yr fully-loaded cost/GW** (Hock via JPM) — Anthropic is private; no BBG,
  no house model. Reconciled against prior wiki comments only.
- **SpaceX CFO "less than a one-year payback" on AI compute** (Jefferies p40) — a unit-economics claim with no P&L
  line to test it against. For scale, BBG has SPCX `1FY` capex at $69.1bn on $43.3bn of revenue.
- **The $26.5T AI TAM** (Jefferies p3) is explicitly labelled a **SpaceX estimate**, not a Jefferies estimate.
  Segments foot: Enterprise Applications $22.7T + AI Infrastructure $2.4T + Consumer Subscriptions $760bn +
  Digital Advertising $600bn ≈ $26.5T (~21% of global GDP).
- **AVGO's "15x logic compute die per package" packaging claim** — an analyst characterisation of an unshipped
  capability, flagged on-page as a claim to falsify rather than a datapoint.

## To re-run when the Terminal is back
1. **AVGO** — re-pull `2FY`/`3FY` and re-test the D-3 residual; it decides how much of D-1 is a real house edge
   versus a consensus that had not finished migrating on 09-03.
2. **CRWV** — confirm the `3FY` EBIT of $7.0bn; D-4's ~90% gap rests entirely on it.
3. **MU** — re-confirm the 80.6% `1FY` gross margin after the next print.
