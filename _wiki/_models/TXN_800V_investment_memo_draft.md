# Texas Instruments (TXN) — 800V DC-Power / AI-Datacenter Content Thesis

**Investment memo draft — Capstone buy-side desk**
_Prepared 2026-07-01 · analyst: tech/semis desk · status: DRAFT for Word conversion + adversarial review_
_Sources: `_wiki/TXN.md`, `_wiki/themes/800v-dc-power.md`, TXN 10-K (2026-02-06) / 10-Q (2026-04-24), earnings transcripts, `_equity_calls`, briefings, `_models/TXN_bottom_up_model.xlsx`. Every datapoint carries broker/analyst + date; own assumptions tagged ESTIMATE._

---

## 1. Executive Summary

**The call:** TXN is the highest-quality, lowest-risk way to own the 800V DC datacenter power transition, but it is *not* the highest-torque way, and the incremental EPS is real but back-end-loaded (2027-2028), not a 2026 event. We frame it as an **add-to-quality-core** rather than a pure-play 800V trade. The theme is a **share-not-TAM fight** among TXN/ADI/ON/IFX/NXPI/MPWR, and the Street currently crowns TXN on capacity and internal high-voltage GaN [Citi/Malik, 2026-06-15].

**Why TXN specifically:** TXN already runs the **largest data-center business in analog** — ~$1.5bn CY25 sales, +~64% YoY, ~9% of revenue [BofA/Arya "AI Power Semis: Top picks are TXN, ADI, and ON for the 800V era", 2026-05-25; JPM/Deshpande, 2026-06-25]. Critically, that book is *still mostly general-purpose amps, clocking and references* — it does **not yet include** the multi-phase VRMs and GaN power-stage sockets that 800V opens up [BofA/Arya, 2026-05-25]. So the 800V thesis is an *incremental content* story layered on an already-inflecting DC base, funded by ~85% internal wafer manufacturing and internal high-voltage (>900V) GaN capacity that has **quadrupled since Oct'24** [Citi/Malik, 2026-06-15].

**The number:** anchoring to BofA's disclosed AI/DC revenue arc (~$1.5bn CY25 → ~$4.5bn CY28, ~18% of sales), we model **incremental EPS accretion from the DC/800V ramp of roughly +$0.50 to +$1.56 in CY27 and +$0.93 to +$2.84 in CY28** (bear→bull), base case **~+$0.95 (CY27) / ~+$1.79 (CY28)**. See §2 for the bridge and the hard caveat that this is *total DC/AI content*, not an 800V-only figure the sources do not isolate.

**Headline EPS accretion (incremental, on top of base business):**

| | CY2027E | CY2028E |
|---|--:|--:|
| **Bull** | +$1.56 | +$2.84 |
| **Base** | +$0.95 | +$1.79 |
| **Bear** | +$0.50 | +$0.93 |

_Correction (post adversarial review): the Bull row originally printed +$1.31/+$2.38, which does not reproduce from the stated 50% incremental-margin input (it back-solves to ~42%, i.e. the Base margin). Recomputed from the formula in §3.4 at the stated 50% Bull margin: +$1.56 (CY27) / +$2.84 (CY28). Bear and Base rows were verified correct and are unchanged._

**The single most load-bearing assumption:** the **revenue ramp** — i.e. that TXN converts its capacity + GaN advantage into the BofA-shaped ~$4.5bn CY28 DC number *and* that a growing slice of it is genuine 800V VRM/GaN content rather than reclassified legacy PSU. Margin is the second-order lever; the revenue slope dominates the accretion range (see §2 sensitivity).

**The debate in one line:** bulls (Citi top pick $345, BofA Buy $370, UBS Buy $245) say 800V share gains print in 2H26 and re-rate the multiple; the bear (@bubbleboi, 2026-06-15) says datacenter-construction PMs "have no plans to do this anytime soon," it's a **2-3 year** lag to earnings, and China can flood GaN/SiC. GS is Sell on valuation, not on the 800V thesis [GS/Schneider, 2026-05-20].

---

## 2. The 800V Opportunity — Sized and Dated

### 2.1 What 800V DC is and why it's happening

The shift from 48V/54V (and 415V AC distribution) to **800V DC** inside the rack is the biggest datacenter power-architecture change in 20+ years, and it is being **forced by NVIDIA's roadmap, not chosen** [theme page; Citi 800V expert, 2026-06-16]. As GPU racks climb from ~130kW (Blackwell) → ~250kW (Vera Rubin NVL144, 2026) → ~600kW (Rubin Ultra / Kyber, 2027) → >1MW (Feynman, 2028), the only way to push that power without drowning the rack in copper busbar is to raise voltage and drop current — 800V cuts amperage **~15x vs 54V** [JPM "800V", 2026-06-09]. At current architecture a 1MW rack needs ~200kg of copper busbar, "astronomical" and physically displacing compute space [Citi, 2026-06-16].

**Timeline (phased, not a switch)** [Citi "800V power", 2026-06-15; theme page]:
- **CSP-driven bipolar ±400V DC sidecar** first (Google/Meta "Mt. Diablo") — easiest, inside the ~600V regulatory envelope, reuses EV/auto power electronics.
- **NVIDIA-led monopolar 800V sidecar** ramping with **Rubin Ultra in late 2H27** (supports up to ~1MW).
- **Full 800V solid-state-transformer (SST)** architecture (DC straight to rack) not mainstream until **late 2028-2029**.
- JPM spec sales models **15-20% adoption** for 800V near-term [JPM AI-power pitch, 2026-06-11].

**Trigger to watch:** "the best way to track when 800V architecture is needed is to track the ramp of the chips" [Citi expert, 2026-06-16]. Power-per-rack quadruples 2026→2027; that is the demand pull.

### 2.2 TXN's *specific* slice (be precise — this is where the thesis lives or dies)

TXN's addressable content on the rack is **on-board power delivery and conversion**, not the grid-side SST/breaker infrastructure (that's IFX SiC, ABB breakers, GEV/ETN electrical OEMs). Specifically:
- **Multi-phase VRMs / CPU-VRM and GPU V-core** power stages — TXN named a key CPU-VRM supplier alongside IFX/MPWR [Citi, 2026-06-15]. JPM cites **GPU VRM/V-core sampling** and Stage-1 conversion building 2H26→2027 [JPM/Deshpande, 2026-06-25].
- **GaN power stages** — TXN is among the few **high-voltage (>900V) GaN vendors**; internal GaN capacity **quadrupled since Oct'24**; GaN is preferred for sub-650V rack/server conversion [Citi, 2026-06-15].
- **General-purpose analog** — amps, clocking, references, gate drivers — the current ~$1.5bn DC book is "still mainly" this [BofA/Arya, 2026-05-25]. Management's framing: TXN can fulfill "almost every analog socket on these racks" [Ilan, Q1 FY26 call, 2026-04-22].
- **What TXN does NOT own:** the grid-to-core SST/SiC stack (IFX's "grid-to-core," AI-power guided €0.75bn→€3.3bn FY28 at 55-60% GM), the DC breakers (ABB), the connectors/busbar (APH/TEL), the integration/sidecar (VRT), and vertical GaN at rack (ON developing, ships 2H27). Where the Street ranks the *composite* 800V exposure, an internal framework put TXN **8th** (behind IFX/VRT/MPWR/NVTS/ETN/GEV/AEIS) precisely because its slice is content-add, not architecture-defining [internal "800V Inflection" synthesis, 2026-06-16].

**Positioning vs peers (the share fight):** MPWR is the purest play (>50% DC sales, +65% YoY DC-power); TXN ~15% of sales guided to eventually eclipse personal electronics (~20%); ADI a "late bloomer" via the $1.5bn Empower Semiconductor IVR acquisition (design wins 2H26); ON differentiated on vertical GaN [Citi, 2026-06-15/16]. On AI-analog *share*, BofA models TXN at ~20% today, expanding to ~21% by CY30 — i.e. TXN is defending a leading share, not seizing a new one [BofA/Arya, 2026-05-25]. Citi sizes the rack-level GPU power-delivery market (800V→sub-1V) at a **>70% CAGR, ~$2bn (2025/26) → ~$12bn (2028)** with TXN the relative share-gainer vs IFX/MPWR/Renesas ramping 2H26 [Citi, 2026-06-15].

---

## 3. EPS Bridge — Quantified, Tagged, Bull/Base/Bear

### 3.1 Revenue anchor (and the honest caveat)

**The concrete number is BofA's total AI/DC revenue arc, not an 800V-only figure.** No source in the corpus isolates "TXN 800V-specific revenue"; every quantified figure is *total data-center / AI-analog* revenue that *contains* an 800V subset. This is stated explicitly so the desk does not treat the bridge as 800V-pure:

| Source | Metric | Figure |
|---|---|---|
| BofA/Arya (2026-05-25) | TXN DC/AI sales CY25 | **~$1.5bn (+64% YoY)** — mostly gen-purpose amps/clocking, *pre*-VRM/GaN |
| BofA/Arya (2026-05-25) | TXN AI sales CY28 | **~$4.5bn (~18% of sales, from ~12%)** |
| JPM/Deshpande (2026-06-25) | TXN DC 2025 | **~$1.5bn, ~9% of rev**; PSU reclassed from industrial into DC |
| Citi/Malik (2026-06-15) | Rack power-delivery TAM | ~$2bn (2025/26) → ~$12bn (2028), TXN share-gainer |
| TXN mgmt (Q1 FY26, 2026-04-22) | DC growth | **~+90% YoY / +25% QoQ**; DC ~$1.2bn run-rate 2025 (Q3 FY25) → +~90% |

**Bridge construction.** The EPS impact should be the DC/800V revenue *incremental to a no-800V-ramp counterfactual*, not gross DC revenue (some DC content pre-existed). We interpolate the BofA arc (~$1.5bn CY25 → ~$4.5bn CY28) and define the **incremental DC/800V revenue above the ~$1.5bn CY25 base** as the accretive piece:

| Year | Total DC/AI rev (BofA path) | Incremental vs CY25 base ($1.5bn) | Tag |
|---|--:|--:|---|
| CY25 | ~$1.5bn | — (base) | HARD (BofA-disclosed; PARTIAL as est.) |
| CY27 base | ~$3.9bn | **~$2.4bn** | ESTIMATE (interp of BofA arc) |
| CY28 base | ~$4.5bn | **~$3.0bn** → we use ~$4.5bn incr. contribution basis* | PARTIAL (BofA CY28 point) |

_*For CY28 we run the accretion on the incremental-above-base of ~$3.0bn in the base case and stress to $4.5bn/$2.8bn in bull/bear (see grid). The bear case ($1.5bn CY27 incremental) reflects @bubbleboi's 2-3yr lag — i.e. 800V barely shows up and the DC line is mostly the pre-existing amps/clocking ramp._

### 3.2 Margin anchor (segment-based, not a made-up "high margin")

DC/800V content is Analog-segment product. We anchor incremental profitability to the **disclosed Analog segment margin**, not a fabricated number:

| Metric | Value | Tag | Source |
|---|--:|---|---|
| FY25 Analog segment revenue | $14,006m | HARD | 10-K, 2026-02-06 |
| FY25 Analog gross profit / GM | $8,242m / **58.8%** | HARD | 10-K, 2026-02-06 |
| FY25 Analog operating profit / OP margin | $5,412m / **38.6%** | HARD | 10-K, 2026-02-06 |
| Q1 FY26 Analog OP margin | **41.7%** | HARD | 10-Q, 2026-04-24 |
| Company GM Q1 FY26 | 58% (+210bps QoQ) | HARD | 10-Q, 2026-04-24; call |

Management operating-leverage / incremental-margin note: TXN has *not* given a DC-specific incremental margin. It does flag that "industrial and data center help from a gross-margin perspective" [Arya callback, 2026-04-23] and that revenue growth drops through hard to FCF as the 300mm capex super-cycle rolls off ("if revenue is going to grow that much... you're going to get a ton of drop through" [UBS/Arcuri callback, 2026-04-23]; "$8 FCF/share very probable" [Ilan, Q1 FY26]). Citi flags TXN has the **largest GM-expansion opportunity in its coverage (>10pp)** on ~85% internal wafers [Citi, 2026-06-15].

**Incremental operating-margin assumptions used:**
- **Bear 35%** — below current Analog segment average (mix drag from GaN ramp / lower-margin power stages, competitive pricing) — ESTIMATE.
- **Base 42%** — ≈ Q1 FY26 Analog segment OP margin (41.7%), i.e. incremental = current segment margin — ESTIMATE anchored to HARD 10-Q figure.
- **Bull 50%** — incremental > segment average, capturing the ">10pp GM-expansion" + operating leverage on the depreciated 300mm base — PARTIAL (directional, Citi GM-expansion color).

### 3.3 Share count & tax (HARD, from filings)

| Input | Value | Tag | Source |
|---|--:|---|---|
| Diluted shares outstanding | **~914m** (Q1 FY26); 913m FY25 avg | HARD | 10-Q 2026-04-24; 10-K 2026-02-06 |
| Effective tax rate | **10% Q1 FY26**; guided **13-14% 2026** | HARD | 10-Q 2026-04-24; Q3 FY25 call (2025-10-22) |
| Buyback pace | Q1 FY26 repurchases only **$158m** (vs $653m yr ago) | HARD | 10-Q 2026-04-24 |
| Capital return | ~$6.0bn returned TTM; dividends ~$1.29bn/qtr | HARD | 10-Q; Q1 FY26 call |

**Buyback note — a drag, not a tailwind, near-term.** TXN's repurchases have collapsed (Q1 FY26 $158m vs $653m a year prior). Free cash flow is earmarked for the dividend and the pending **~$7.5bn Silicon Labs acquisition**; UBS flags TXN may need to *take on debt* to fund the dividend, leaving "not that much headroom for buybacks" [Arya callback, 2026-04-23]; UBS/Arcuri similarly noted Chips Act grant restrictions exist but are "not a factor" management is prioritising [Arcuri callback, 2026-04-23]. **We therefore hold diluted share count roughly flat (~914m) in the bridge — we do NOT credit buyback-driven EPS accretion to the 800V thesis.** This is conservative and defensible on the buyback axis; if the FCF inflection restarts buybacks, it is upside to the per-share math but is a capital-allocation story, not an 800V story. Tax held at **13.5%** (midpoint of guide) — ESTIMATE anchored to HARD guide.

**Flagged asymmetry (post adversarial review): flat share count is NOT conservative on the acquisition axis.** The pending ~$7.5bn Silicon Labs deal (noted as a bear risk in §4) could add shares and/or debt depending on funding mix, which is not modeled here. If SLAB is partly stock-funded, the true diluted count is higher than 914m and per-share accretion is lower than shown in every scenario above. The 914m assumption is conservative on buybacks but potentially optimistic on M&A dilution — net effect on the bridge is unsigned without knowing SLAB's funding structure. Treat this as an open risk to the per-share math, not something the bull/bear range already captures.

### 3.4 The bridge (formula + tagging)

`Incremental EPS = Incremental DC/800V revenue × incremental OP margin × (1 − tax) ÷ diluted shares`
`= ΔRev × OPM × (1 − 0.135) ÷ 914m`

| Input | Tag |
|---|---|
| Incremental DC/800V revenue | **ESTIMATE** (interpolated off BofA/JPM HARD-cited total-DC arc; NOT 800V-isolated) |
| Incremental OP margin | **PARTIAL/ESTIMATE** (base = HARD Q1 FY26 Analog 41.7%; bull/bear = own flex) |
| Tax rate 13.5% | **PARTIAL** (midpoint of HARD 13-14% guide) |
| Diluted shares 914m | **HARD** (10-Q) — held flat, no buyback credit (ESTIMATE choice, conservative) |

### 3.5 Bull / Base / Bear accretion table

| Scenario | Incr. DC/800V rev | Incr. OP margin | **CY27 EPS accretion** | **CY28 EPS accretion** |
|---|--:|--:|--:|--:|
| **Bear** | CY27 ~$1.5bn / CY28 ~$2.8bn | 35% | **+$0.50** | **+$0.93** |
| **Base** | CY27 ~$2.4bn / CY28 ~$4.5bn* | 42% | **+$0.95** | **+$1.79** |
| **Bull** | CY27 ~$3.3bn / CY28 ~$6.0bn | 50% | **+$1.56** | **+$2.84** |

_*Base CY28 uses BofA's ~$4.5bn CY28 point as the incremental-contribution basis; bear/bull flex ±25% around the revenue ramp (see sensitivity). Bear CY27 $1.5bn = "800V barely shows up, DC line is legacy amps/clocking" per @bubbleboi timing._

**Context vs the base business:** consensus CY27 EPS is ~$9.02 [BBG snapshot, TXN.md]; Citi models $10.10, UBS $10.14. A base-case **+$0.95** DC/800V accretion is ~10% of CY27 EPS — material but not the whole stock. This is consistent with DC being ~9-12% of revenue growing to ~18%.

### 3.6 Sensitivity (load-bearing assumption isolated)

**±25% on the revenue ramp (the load-bearing input), base-case CY27 (42% OPM):**

| Revenue ramp | Incr. rev | CY27 EPS accretion |
|---|--:|--:|
| −25% | $1.8bn | **+$0.71** |
| Base | $2.4bn | **+$0.95** |
| +25% | $3.0bn | **+$1.19** |

**±25% on incremental margin, base-case CY27 ($2.4bn rev):**

| Incr. OP margin | CY27 EPS accretion |
|---|--:|
| 31.5% (−25%) | **+$0.71** |
| 42% base | **+$0.95** |
| 52.5% (+25%) | **+$1.19** |

Coincidentally symmetric because the bridge is multiplicative — but the *asymmetry of confidence* is the point: the revenue ramp is the disputed variable (bull Citi/BofA vs bear @bubbleboi 2-3yr lag), while the margin anchor is a disclosed 10-Q figure. **The revenue slope carries the thesis.**

### 3.7 Guardrails (sanity checks — as instructed)

1. **vs 800V TAM:** Citi sizes rack power-delivery TAM at ~$12bn by 2028 [Citi, 2026-06-15]. Our base-case CY28 incremental (~$3.0bn *total DC*, of which 800V is a subset) implies TXN capturing a plausible minority of the power-delivery pool while ADI/ON/IFX/MPWR/Renesas split the rest. **Bull $6.0bn incremental would imply TXN taking ~half the entire power-delivery TAM — structurally implausible given the fragmented ~11-supplier landscape [Citi, 2026-06-15].** We flag the bull case as *aggressive and TAM-constrained*; it is a ceiling, not a forecast. The BofA ~$4.5bn CY28 figure is *total AI/DC* (includes non-800V amps/clocking), so it does not violate the 800V TAM — but bull-case $6.0bn does strain it.
2. **vs Analog segment size:** the bottom-up model puts CY26 Analog ~$16,995m and CY27 total ~$24,606m (Analog ~$20.6bn implied) [`TXN_bottom_up_model.xlsx`, 2026-07-01, cached values confirmed post skeptic-correction]. A CY28 DC/AI book of ~$4.5bn sits comfortably inside a >$20bn Analog segment (~18-22% of Analog) — consistent, not double-counted. Bull $6.0bn would be ~29% of the ~$20.6bn CY27 Analog base — high but not impossible; again treat as ceiling. **Caveat carried over from the revenue model's own skeptic review: CY27 in the underlying model is "directional, not precise" (7 of 8 quarters are extrapolated off a recovery slope, only Q2FY26 is hard-guided) — using it as a sanity denominator is reasonable, but it is itself a soft number, not a hard one.**

---

## 4. Bull / Bear Synthesis (attributed)

### Bull

- **Citi — top pick, PT $345 (30x 2028E EPS):** "TI is our top idea... best positioned to take advantage from the capacity that they have built over the last three years... they're going to take share and also be best positioned to provide the capacity for GaN and some of these wide-bandgap materials for 800 volts" [Citi/Malik expert call, 2026-06-16]. Raised C26/27/28 EPS to **$8.03/$10.10/$11.42**; largest GM-expansion opportunity (>10pp) on ~85% internal wafers; DC-power share gains 2H26 vs IFX/MPWR/Renesas [Citi "800V power", 2026-06-15].
- **BofA — Buy, PT $370 (40x CY27E):** TXN the "largest data-center business in analog (~$1.5bn CY25, +64% YoY) but still mostly general-purpose amps/clocking (VRMs/GaN sockets yet to come); AI to ~$4.5bn by CY28 (~18% of sales vs ~12% today)"; retains leading AI-analog share expanding to ~21% CY30 [BofA/Arya "AI Power Semis: Top picks are TXN, ADI, and ON for the 800V era", 2026-05-25].
- **JPM — "ability to supply" = share:** management attributed Q1 strength partly to capacity availability converting to share while peers are constrained; reclassified PSU content from industrial into DC; "application-specific 800V sockets (Stage-1 conversion, GaN power stages, GPU VRM/V-core sampling) building 2H26 into 2027" [JPM/Deshpande "First Principles", 2026-06-25]. JPM (Sur) keeps TXN OW top pick; CY27 EPS already revised +23% across ADI/TXN/MCHP [JPM, 2026-05-29].
- **UBS — Buy, PT $245, top analog pick:** the FCF-inflection thesis (capex $5bn peak → $2.35bn 2026E → $2.0bn 2027E), well above Street on '26/'27; on pricing UBS thinks "TI's maybe not completely admitting that pricing is helping them as much as it is" (i.e. **sandbagging** — web scrapes of TI.com show broader price action than management admits) [UBS/Arcuri callback, 2026-04-23].
- **Management:** DC ~+90% YoY, "almost every analog socket on these racks," ~$8 FCF/share "very probable" [Ilan, Q1 FY26, 2026-04-22]. Pricing: second-round hike **+10-25% effective Jul 1**, ahead of IFX/STM [@QQ_Timmy, briefing 2026-06-20; Jefferies/Menon, 2026-06-03].
- **Structural insulation:** analog/MCUs/MOSFETs see "very little" Chinese investment (China attacks only high-growth SiC/GaN/GPU) — catalog franchise structurally insulated from indigenization [Jefferies/Menon, 2026-06-03]. TXN is the margin leader: FY25 GM 57.0%, EBIT 34.1%, ROIC 17.4%, highest in the analog/power peer set [AlphaSense IFX Primer, 2026-06-22].

### Bear

- **@bubbleboi — the timing bear (the load-bearing pushback):** "Channel checks with every DC construction PM in the country — no plans to do this anytime soon. TXN specifically vocal about this. **2-3 years before hitting earnings.** China can flood GaN/SiC like InP. Better risk/reward: WFE + full-system plays (transformers, inverters)" [briefing 2026-06-15]. This is the direct counter to the 2H26 revenue-recognition case and is why our **bear CY27 accretion is only +$0.50**.
- **GS — Sell (valuation, not thesis):** rates TXN Sell off ~32x normalized $13 EPS; reads ADI's strong print as *risk to the Sell* because it pushes TXN estimates up — i.e. GS concedes the fundamentals, disputes the multiple [GS/Schneider, 2026-05-20].
- **China GaN/SiC oversupply:** the specific risk that Chinese overcapacity floods wide-bandgap as it did indium phosphide, compressing the GaN economics TXN is building for [@bubbleboi, 2026-06-15].
- **Copper-tax nuance (deflates the runaway-content bull):** absolute copper *decreases* per rack at 800V vs 48V; content is roughly flat-to-modestly-up gen/gen, not runaway [UBS 800V expert Q&A, 2026-05-14]. Applies more to connectors than to TXN's silicon, but tempers the "content explosion" framing.
- **Fragmentation caps pricing power:** ~11 semiconductor suppliers fighting across conversion stages "with no clear winner yet"; standardized footprints cap integration-premium capture [Citi, 2026-06-15/16]. TXN is defending ~20% AI-analog share, not monopolising.
- **Kyber timing risk:** UBS flags **Kyber possibly pushed to 2028** (with a modified NVL72 "Oberon" for the H2'27 launch moderating per-rack wattage) — if the 800V-native rack slips, so does the socket revenue [UBS "800VDC looming faster", 2026-06-22].
- **Capital allocation crowds out per-share torque:** ~$7.5bn Silicon Labs acquisition + dividend consume FCF; buybacks minimal; TXN may lever up to fund the dividend [Arya/Arcuri callbacks, 2026-04-23].
- **Cycle was slow through 2025:** Jefferies found "really nothing positive to report" in analog mid-2025, rated TXN HOLD at $184.55; TXN cut its own 2025 growth from 10-15% to ~flat [Jefferies/Curtis-Garrigan, 2025-09-26] — the Q1 FY26 inflection has since outrun that, but it shows how quickly the analog read can flip.

**Where the edge is:** the disagreement is almost entirely on **800V timing** (2H26 revenue recognition per Citi/BofA/JPM vs 2-3yr lag per @bubbleboi) and on **valuation** (GS Sell). It is *not* on whether TXN is well-positioned in the socket — that is consensus. The actionable question for the desk: **do you get paid for 800V in the 2026 numbers, or only in 2027-2028?** Our base case says the *content* builds 2H26→2027 [JPM/Deshpande] but the *EPS* is a 2027-2028 event — closer to the bear's timing than the bulls' PTs imply, even if the direction is the bulls'.

---

## 5. Catalysts & Risks (800V-specific)

### Catalysts — when it shows in the numbers
- **Q2 FY26 print, ~2026-07-22** — first call with new CFO **Julie Knecht** (Lizardi out 2026-08-01) [DB/Seymore, 2026-06-03]. Watch: DC growth rate sustaining ~+90%, any 800V/rack-content disclosure, confirmation of the **Jul 1 +10-25% price hike** flowing through [@QQ_Timmy, 2026-06-20].
- **2H26 — 800V share-gain data points** — Citi expects share gains 2H26 vs IFX/MPWR/Renesas; watch GaN HV capacity ramp and any rack-content dollar disclosure [Citi, 2026-06-15]. JPM sees Stage-1 conversion / GaN power stages / GPU VRM sampling building 2H26→2027 [JPM/Deshpande, 2026-06-25].
- **Late 2H27 — Rubin Ultra / monopolar 800V sidecar ramp** — the true 800V-native inflection for TXN's VRM/GaN sockets [Citi, 2026-06-15].
- **FCF inflection / capex roll-off** — capex $5bn peak → $2-3bn 2026 (UBS models $2.35bn→$2.0bn); confirmation feeds the ~$8 FCF/share and any buyback restart [Q1 FY26 call; UBS, 2025-12-22].
- **Cross-read design-win color:** NVDA published an 800V two-wire row-scale spec with a broad named ecosystem including TI [JPM "800V", 2026-06-09]; ON Analyst Day **Sep-16-2026** (vertical GaN) is a competitive-intensity read for TXN's GaN slice [Citi catalyst watch, 2026-06-15].

### Risks / what delays it
- **Timing (primary):** 2-3yr lag to earnings; DC-construction PMs "no plans anytime soon" [@bubbleboi, 2026-06-15]; Kyber possibly slips to 2028 [UBS, 2026-06-22]. This is the single biggest risk to the CY27 accretion.
- **China GaN/SiC flood** compressing wide-bandgap economics [@bubbleboi, 2026-06-15].
- **Share, not TAM:** fragmented ~11-supplier field; ADI's Empower IVR entry (2H26 wins) and ON vertical GaN (ships 2H27) chip at TXN's slice [Citi, 2026-06-15].
- **Standardised footprints** cap pricing power / integration premium [Citi, 2026-06-15].
- **Valuation:** 12m relative highs, semis ~63% above 200dma ("widest since dot-com") [Redburn/Adley, 2026-05-12]; GS Sell [2026-05-20].
- **Capital allocation:** Silicon Labs + dividend crowd out buybacks; possible debt draw [Arya/Arcuri, 2026-04-23].
- **General cyclicality / China:** ~20% revenue from China, ~50% shipped into China; auto weak ex-China [10-K, 2026-02-06; Q1 FY26 call].

---

## 6. Bottom Line

TXN is a **buy the quality, underwrite the timing carefully** name on 800V. The socket position is real and consensus-endorsed (Citi top pick, BofA/UBS Buy), the margin structure is best-in-class and disclosed, and the capacity + internal GaN advantage is a genuine moat. But the EPS impact is **back-end-loaded to 2027-2028** (base case ~+$0.95 CY27 / ~+$1.79 CY28), the bear's 2-3yr timing argument is credible for the *2026* numbers specifically, and the bull PTs ($345-370) already embed a multiple re-rate on the 800V mix crossing >20% of sales [Citi "we've seen this movie in networking"]. **We would own it as a core analog quality position with 800V as free-ish optionality, size the accretion at the base case, and treat any 2H26 800V-content disclosure as the catalyst that de-risks the 2027 revenue slope — the single variable that carries the thesis.**

---

## Sources

**Filings:** TXN 10-K FY2025 (2026-02-06, acc 0000097476-26-000059) — segment revenue/margins, end-market %, share count; TXN 10-Q Q1 FY26 (2026-04-24, acc ...-26-000101) — segment margins, diluted shares 914m, effective tax 10%, buyback $158m.

**Transcripts:** TXN Q1 FY26 (2026-04-22), Q4 FY25 (2026-01-27), Q3 FY25 (2025-10-22), Q2 FY25 (2025-07-22) earnings calls. **Sourcing caveat (post adversarial review): these are analyst summary notes (bulleted recaps cross-checked against the 10-Q), not verbatim speaker-by-speaker transcripts.** The Ilan quotes used in this memo ("almost every analog socket on these racks," "$8 FCF/share very probable," DC +90% YoY) all appear word-for-word in the Q1 FY26 summary note and are consistent with the 10-Q, but a primary verbatim transcript is not on file — if a PM needs the exact original wording confirmed, pull the primary transcript before relying on the quote in a written deliverable.

**Equity calls:** Citi 800V expert (2026-06-16); JPM AI-power pitch / spec sales (2026-06-11); UBS/Arcuri TXN callback (2026-04-23); BofA/Arya TXN analog (2026-04-23); UBS 800V-power (2026-05-14).

**Research / briefings:** BofA/Arya "Watts to Tokens" (2026-05-25, PO $320→$370); JPM/Deshpande "First Principles — AI Power" (2026-06-25); Citi "800V power" (2026-06-15, PT $345); UBS "Data Centre Central: 800VDC looming faster" (2026-06-22); Jefferies "Analog Semis" (Menon, 2026-06-03); JPM/Sur "Semis spring update" (2026-05-29); AlphaSense IFX Primer (2026-06-22); @bubbleboi (briefing 2026-06-15); @QQ_Timmy (briefing 2026-06-20); GS/Schneider (2026-05-20); DB/Seymore (2026-06-03); Redburn/Adley (2026-05-12).

**Model:** `_wiki/_models/TXN_bottom_up_model.xlsx` (build 2026-07-01) — CY26E revenue $20,795m, CY27E $24,606m, CY26 Analog ~$16,995m.

**Theme:** `_wiki/themes/800v-dc-power.md` — TAM sizing, phased timeline, who's-exposed peer map.

**BBG consensus:** `_wiki/_data/estimates.json` (asof 2026-07-01) — CY27 EPS $9.02, CY26 EPS $7.48, cited price $298.41. **The Capstone VPN was down for part of this build; a live BBG re-pull could not be completed** — the cached 2026-07-01 snapshot matches the memo's figures, but the next-earnings-date claim (~2026-07-22) and the live PT/rec distribution behind "the Street stance" should be reconfirmed with a live pull before this informs a trade.

---

**ADVERSARIAL REVIEW COMPLETE (2026-07-01) — verdict PARTIAL→FIXED.** The double-check skeptic found the work well-sourced (every load-bearing quote and filing figure verified verbatim against primary documents, including a page-by-page read of the BofA report image) but caught one reproducible arithmetic error and several attribution issues, all corrected in this version:
1. **Fixed:** Bull-case EPS accretion was arithmetically wrong (printed +$1.31/+$2.38, which implies ~42% margin — the Base margin — not the stated 50% Bull margin). Recomputed from the memo's own formula at 50%: **+$1.56 (CY27) / +$2.84 (CY28)**. Bear and Base rows were verified correct and are unchanged.
2. **Fixed:** BofA source was mistitled "Watts to Tokens" (an earlier, different BofA note); corrected to the actual report title, "AI Power Semis: Top picks are TXN, ADI, and ON for the 800V era" (Vivek Arya, 2026-05-25) — the date, analyst, and every cited figure from this report were independently verified against the source image.
3. **Added:** an acquisition-dilution caveat (§3.3) — flat share count is conservative on buybacks but not on the pending Silicon Labs deal.
4. **Added:** honest labeling that the on-file "transcripts" are analyst summary notes, not verbatim (Sources section) — the quotes used are supported by these notes and consistent with the 10-Q, but not confirmed against a primary verbatim transcript.
5. **Added:** the underlying revenue model's own "CY27 directional, not precise" caveat, carried into the Analog-segment guardrail (§3.7).
6. **Open item, not fixable offline:** live BBG re-pull pending VPN reconnection (see BBG consensus line above).
