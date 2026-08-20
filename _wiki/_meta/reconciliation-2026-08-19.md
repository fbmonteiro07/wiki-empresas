# Reconciliation — 2026-08-19 (/run-inbox)

_Variance pass on every NEW quantitative datapoint from the 2026-08-19 ingest, against three baselines: **(1)** prior wiki comments on disk, **(2)** Capstone house models / on-disk house data, **(3)** BBG consensus._

**Baseline-3 status: ⚠️ BBG LIVE WRAPPER DOWN — `bloomberg.bdp` raised `ConnectionError` (blpapi could not start session; localhost:8194 refused, "Terminal not running / logged out"). Terminal not logged in at run time (23:49).** ✅ **However `_wiki/_data/estimates.json` carries BBG consensus stamped `asof 2026-08-19` — i.e. SAME-DAY cached consensus for 98 names — so the consensus column below is BBG data, just not re-pulled live. No web data was substituted anywhere.** **Marked PENDING only where a name is absent from that file.**

---

## 🔴 HEADLINE: THE RECONCILIATION STEP OVERTURNED A REJECTION MADE EARLIER IN THE SAME RUN

The two JPM Korea model workbooks (`000660 KS Equity_MODEL_JPM_Aug 06 2026.xlsx`, `005930 KS Equity_MODEL_JPM_Jul 31 2026.xlsx`) were **initially rejected as corrupted** on a plausibility check: SK Hynix 2026E revenue +258.5% at a 77.2% operating margin, Samsung 2026E revenue +115.6% at 51.9%. Those looked impossible.

**Same-day BBG consensus says they are right.**

| | JPM model | BBG cons (2026-08-19) | Δ |
|---|--:|--:|--:|
| SK Hynix CY2026 revenue | W348,253bn | W350,802bn | **−0.7%** |
| SK Hynix CY2026 OP margin | 77.2% | 77.5% | **−30bp** |
| Samsung CY2026 revenue | W719,274bn | W719,382bn | **−0.02%** |
| Samsung CY2026 OP margin | 51.9% | 52.7% | **−80bp** |

➤ **The forecast columns were never corrupted; the reviewer's margin intuition was out of date for this tape.** The disconfirming evidence was already in hand during the same run: **Kioxia printed a 75% non-GAAP operating margin in Q1 FY26 and guided Q2 to 79.5%**, and this wiki already carries **SanDisk at an 84.6% gross margin**. Memory operating margins of 75-80% are the current cycle, not an artefact. Both files were subsequently ingested into `SKHYNIX.md` and `SAMSUNG.md`.

⚠️ **Process lesson (recorded in `_inbox/_ingest-log.md`): do not reject a broker model on an eyeballed plausibility check — reconcile against consensus FIRST. Here Step 7 caught a false negative that would have silently discarded two legitimate house models.**

---

## Where the new data DIVERGES

| # | Name | New datapoint | Baseline it diverges from | Gap | Read |
|---|---|---|---|--:|---|
| **1** | **SKHYNIX** | JPM CY2026 **EPS W366,143** | BBG cons **W320,967** | **+14.1%** | 🔴 **A BELOW-THE-LINE disagreement, which is what makes it interesting.** JPM is **−0.7% on revenue and −1.1% on EBIT** yet +14.1% on EPS — arithmetically impossible from operations, so it lives in **tax rate, non-operating income or share count**. If JPM is right, the Street's CY26 EPS is ~12% too low on essentially identical operating forecasts. **Action: pull the published JPM note to identify the line.** ⚠️ **RE-PLACED 2026-08-20 on the BBG ANNUAL line → gap cuts to +4.7%, and the missing line is now IDENTIFIED. Still DIVERGES, de-escalated. See §BBG resolution.** |
| **2** | **SAMSUNG** | JPM CY2026 **EPS W50,797** | BBG cons **W46,404** | **+9.5%** | 🔴 **Same shape, same analyst, same year — and the parallel is the signal.** JPM is −0.02% on revenue and −1.5% on EBIT, +9.5% on EPS. **Two Korean memory models from one house, both ON consensus at the operating line and both 10-14% ABOVE it on EPS, points to one systematic house assumption below the operating line rather than two coincidences.** Highest-conviction item in this run. ❌ **WITHDRAWN 2026-08-20 — SHARE-COUNT BASIS ARTEFACT. At net income JPM is −3.6% BELOW consensus. Moved to CONFIRMS. See §BBG resolution.** |
| **3** | **SAMSUNG** | JPM CY2027 **revenue W941,029bn / OP W549,257bn** | BBG cons **W990,684bn / W583,748bn** | **−5.0% / −5.9%** | 🔴 **The cleanest tradeable divergence, and it SURVIVES every adjustment.** ~W50tn of revenue and ~W35tn of profit below the Street, and it is **not** a margin call (margins within 50bp) — JPM simply has less Samsung revenue in the out-year. Note it runs *against* item 2: JPM is more conservative on 2027 operations while more generous below the line, so the two partly cancel at EPS and the headline EPS delta understates the real disagreement. ✅ **CONFIRMED 2026-08-20 and RESIZED to −3.5%/−3.8%; corroborated at net income (−3.6%). Strongest surviving row in the run.** |
| **4** | **SAMSUNG** | JPM capex **CY26 −W79,137bn / CY27 −W99,300bn** | BBG cons **−W75,972bn / −W91,715bn** | **+4.2% / +8.3%** | 🔴 **Widest read-through in the run, and it is a MIX call not a level call: JPM is ABOVE consensus on Samsung capex and BELOW on SK Hynix capex (−3.5%/−4.2%).** More Samsung spend, less Hynix spend than the Street. Directionally positive for tools levered specifically to Samsung. **Cross-check → [[AMAT]], [[LRCX]], [[KLAC]], [[ASML]], [[TOKYOELEC]], `themes/semicap-wfe`.** ❌ **OVERTURNED 2026-08-20 — the MIX call does not exist on the annual line; semicap read-through CANCELLED. Moved to CONFIRMS.** |
| **5** | **KIOXIA** | Company-reported Q1 FY26 **non-GAAP OP ¥1,326.2bn**, **GM 80% (82% ex-JV)** | **Prior wiki comment** (relay): "OP ¥1.27tn", "GM 78.1%" | **+4.4% OP; +1.9pt GM** | 🔴 **A wiki-internal divergence, i.e. the page was wrong.** The primary transcript beat the relay on both lines. **More important is the framing: the page called it "a modest miss on a lowered bar" — the company BEAT its own guidance on revenue, OP, net income AND EPS; the miss was only vs the higher ¥1.372tn consensus.** Corrected on the page, old values in `## Changelog`. |
| **6** | **KIOXIA** | Management: CY26 bit growth high-teens **"in line with how we see our OWN bit growth"** | **Prior wiki comment** (relay): "explicitly in line with **Samsung** guidance" | n/a | 🔴 **The relayed cross-supplier corroboration was FABRICATED — there is no Samsung reference anywhere in the call.** The page then built a "Samsung's 60-70% LTA coverage disclosed the same week" read-across on top of it. **The bit-growth leg of that read-across is unsupported and has been withdrawn.** |
| **7** | **KIOXIA** | **¥78.2bn equity stake in NANYA** (Taiwan DRAM) + deliberate **DRAM inventory build (+¥25.5bn)** | **Prior wiki thesis:** *"the only large NAND maker without a captive DRAM business… the cleanest listed proxy for the NAND/SSD cycle"* | qualitative | 🔴 **A thesis-level qualifier that every broker relay dropped.** Not a captive fab and modest against a ¥4.7tn balance sheet, but Kioxia is now taking DRAM equity exposure *and* building DRAM inventory. The "clean NAND pure-play" framing needs a caveat. |
| **8** | **KIOXIA** | FY26 **R&D ~¥200bn** (BiCS 11 + AI-inference SSDs) | **Prior wiki comment:** "R&D rising to **¥230bn/yr**" (Investor Day, 2026-06-02) | **−13%** | ⚠️ **Possibly not a cut** — the Investor Day figure may be a multi-year average against an FY26 point. **Flagged as two different numbers that must not be quoted interchangeably**, not resolved. |
| **9** | **SNDK** | Management (Ismali): on a 1.2tn-parameter run, *"having just the HBM SSD was good enough… you really required a **minute amount of DDR**"*; on Vera Rubin's SOCAMM cut, *"you can go even further"* | **Prior wiki framing:** HBF-vs-HBM substitution is *"a live sell-side debate rather than a company slide"* (MS against, Jefferies open) | qualitative | 🔴 **The company has taken a side, and on a DIFFERENT and larger target than the page was tracking: eSSD + HBM displacing SYSTEM DRAM (DDR/SOCAMM), not HBM.** Cross-read **[[MU]], [[SAMSUNG]], [[SKHYNIX]]** conventional-DRAM demand and **[[NVDA]]** platform BOM. ⚠️ Vendor lab data, single workload, no methodology, obvious incentive — directional only, **not a sizing input**. |
| **10** | **SNDK** | Reitzes: HBF is not in the model but bits only grow mid-to-high teens — *"what are you getting rid of?"* → **management declined**; Ilkbahar separately: HBF *"entirely orthogonal to our storage business"* with capacity to *"easily increase our output if we choose to"* | **Prior wiki framing:** "HBF is free optionality, not a number" | qualitative | 🔴 **Sharpens the framing into a dependency: HBF upside is additive ONLY IF the latent productivity headroom is real. Management asserted it and refused to size it.** The same sentence also undercuts the *bull* supply-sink trade (HBF tightening NAND, lifting industry pricing) that Bernstein's read implies. **Now the single most important unquantified claim on the SNDK page.** |
| **11** | **themes/optical-cpo** | The 08-18 "SOURCE UNCONFIRMED" Virgo excerpt **is FUNDA** (verbatim match incl. *"Figure 2 below"* and *"fivefold increase"*) | **Prior wiki caveat:** *"plausibly the same author"* as the @SemiAnalysis_ post | n/a | ✅ **Attribution resolved, and the page's own guess corrected.** The two 08-18 blocks are **two different sources on two different axes** (SemiAnalysis scale-up, FUNDA scale-out) — they were never corroboration of each other, which is how the page had been reading them. **GF Securities (08-19) is the first genuinely independent third vote, and the first with ratings.** |
| **12** | **LITE / COHR** | GF Securities: **LITE Buy / COHR Hold** on one shared OCS thesis | **Prior wiki marks:** MS 08-04 ranks **COHR above LITE** on the China ban; Jefferies 08-07 *"bullish for COHR, less so LITE"* | direction | ⚠️ **The Street is genuinely split on the PAIR, not on the category.** GF sides with LITE; MS and Jefferies side with COHR. **Do not over-read: GF carries no PT, no estimates and no COHR-specific model work — its COHR content is two product lines in a beneficiary list.** A relative-preference mark only. |
| **13** | **Unitree (688836.SS, off-coverage)** | Nomura **BUY, TP CNY370**, +145.4% implied | **Prior wiki mark:** listed 2026-08-19 at **~US$53.3bn after a +492.18% debut** (@aleabitoreddit) | see read | ⚠️ **NOT a divergence — a base mismatch, and it matters.** The TP is struck off the **CNY150.80 IPO price**, not the post-debut tape. **A +492% debut may already have exceeded the target.** Anyone comparing TP to price must re-base first. No BBG/house baseline (Chinese A-share, off coverage) → reconciled vs prior wiki comment only. |
| **14** | **TSLA** | Unitree **H2 at CNY199k (~US$28k)** shipping at **60% gross margin** | **Prior wiki:** Optimus sub-US$20k target; Gen3 guided 2H26F | see read | ⚠️ **Reframes the Optimus cost argument: a shipping $28k robot at 60% GM versus a $20k aspiration not yet built at volume.** Nomura also flags Optimus Gen-3 pilot production as a risk to its OWN Buy — so the read runs both ways. |

---

## CONFIRMS (no action)

| Name | New datapoint | Baseline | Verdict |
|---|---|---|---|
| **KIOXIA** | Q1 revenue **¥1,767.1bn**; Q2 guide **rev ¥2,390bn / OP ¥1,900bn** | Prior wiki (relay) ¥1.76tn / ¥2.39tn / ¥1.9tn | ✅ Relay was right on these three; now sourced to the primary. |
| **KIOXIA** | **ASP +70% QoQ** like-for-like AND blended, volume up low-single-digit | Prior wiki: "ASP +70% q/q like-for-like on low-single-digit bit growth" | ✅ Exact match, verbatim from management. |
| **KIOXIA** | Capex **¥470bn/yr avg FY26-28**; ¥800bn/30mn-share buyback (3 Aug–30 Oct); 3-for-1 split effective 1 Oct | Prior wiki (Investor Day + relay) | ✅ All confirmed. |
| **KIOXIA** | CY2027 *"demand will exceed supply"* | Prior wiki | ✅ Confirmed verbatim. |
| **KIOXIA** | Q3-26E BBG cons rev **¥2,456bn** / EPS **¥2,552** vs company Q2 guide ¥2,390bn / EPS ¥2,335.70 | BBG cons (asof 2026-08-19) | ✅ **Consensus sits ~2.8% above the company's own next-quarter revenue guide and ~9% above its EPS guide — normal beat-expectation posture for this name, not a divergence.** (Note the label offset: BBG "Q3-26E" is calendar-quarter; Kioxia's Q2 FY26 is the Sep quarter.) |
| **SKHYNIX** | JPM CY2026 revenue / EBIT / capex | BBG cons | ✅ **−0.7% / −1.1% / −3.5% — all inside noise.** |
| **SAMSUNG** | JPM CY2026 **net income W297,408bn** (the share-count-free line) | BBG annual-line cons **W308,535bn** | ✅ **MOVED HERE FROM DIVERGES #2 on 2026-08-20. −3.6%, and it sits consistently with −1.5% revenue / −3.0% EBIT. The +9.5% "EPS premium" was JPM's common-only EPS read against a preferred-inclusive consensus. No below-the-line anomaly exists.** |
| **SAMSUNG / SKHYNIX** | JPM capex SAMSUNG **CY26 W79,137bn / CY27 W99,300bn**; SKHYNIX **CY26 W47,328bn / CY27 W60,000bn** (both read from the workbooks, not back-solved) | BBG annual-line cons SAMSUNG **W78,475bn / W98,325bn**; SKHYNIX **W45,519bn / W60,234bn** | ✅ **MOVED HERE FROM DIVERGES #4 on 2026-08-20. +0.8% / +1.0% Samsung and +4.0% / −0.4% Hynix — JPM is above consensus on BOTH names in 2026 and on it for both in 2027. The claimed Samsung-over-Hynix MIX does not exist; if anything the 2026 tilt runs the other way. Semicap read-through cancelled.** |
| **SAMSUNG** | JPM CY2026 revenue / EBIT | BBG cons | ✅ **−0.02% / −1.5%.** Revenue match is near-exact. |
| **SKHYNIX** | JPM CY2027 EPS **W447,275**, de-biased for the known Korean CY-sum inflation (~+20.1%) → cons ≈ **W471,071** | BBG cons (de-biased) | ✅ **−5.1%, i.e. broadly in line. The raw −20.9% was a false divergence created by our own CY-sum construction — do NOT trade it.** |
| **SAMSUNG** | JPM CY2027 EPS **W72,303**, de-biased (~+6.8%) → cons ≈ **W70,410** | BBG cons (de-biased) | ✅ **+2.7% — the raw −3.8% FLIPS SIGN once de-biased.** |
| **SNDK** | *"100% of excess cash"* = cash generated less investment in the business, returned in full ("there is no trick"); Q1 $5bn generated / $4.5bn returned | Prior wiki carried two wordings ("100% of excess FCF" GS vs "100% of FCF") | ✅ **Definition settled by the CFO; ambiguity closed.** |
| **SNDK** | NBM coverage **FY29 "consistent with the '28 number"** (~2/3); *"quarter-by-quarter for the next 3 to 5 years"*; "3 months → 4 years of visibility in 2 quarters" | Prior wiki: 50% FY27 / 67% FY28 bits; SIG "more than four years of average visibility" | ✅ **Confirms SIG from the company, and extends coverage one year further out than the page carried.** |
| **GOOG / LITE / COHR** | 6D torus: optical ports per chip **1.5 → 6 (4x)**; links per 64-chip block **96 → 384**; 4,096-chip diameter **~24 → ~12 hops** | Prior wiki (SemiAnalysis, 08-18): "ICI links per chip double from 6 to 12"; 24 → 12 hops | ✅ **Consistent, NOT contradictory — see unit guard below.** Hops confirmed identically by all three sources. |
| **LITE** | FUNDA: *"R300 deployed at Google; next-generation product in customer sampling"*; *"200G EML capacity … through the end of 2026"* | Prior wiki: FY26 10-K "shift to 200G lane speeds" ASP-up; "all EML capacity locked in LTAs through FY27" | ✅ Third-party corroboration of both legs. |
| **COHR** | FUNDA: *"first to introduce a 400G D-EML"*; OCS **300×300 DLX** | Prior wiki: TSEM all-silicon 400G/lane route with COHR (SIG, 2026-07-01); Citi 07-16 400mW InP CW laser | ✅ Consistent with the existing 400G/lane roadmap. |
| **NVDA** | Nomura: Jetson Orin in Unitree Go2 / G1 EDU; US content 10-20% of G1 EDU BOM | No prior wiki mark | ✅ New, immaterial to the model. Logged for the design-win and the export-control vector. |
| **LITE / COHR** | BBG cons Q3-26E: LITE rev **$1,252.9m** / EPS **$4.21** / GM 51.2%; COHR rev **$2,304.7m** / EPS **$1.98** / GM 40.6% | BBG (asof 2026-08-19) | ✅ **Context only — neither 08-19 optics note carries an estimate or PT, so there is nothing to reconcile against consensus.** |

---

## PENDING

- **Unitree (688836.SS)** — no BBG entry and no Capstone house model (off-coverage Chinese A-share). Reconciled against prior wiki comments only, per protocol for names without consensus/house baselines. **Nomura's 2027F/28F sales growth (+101%/+144%) and 25x 2027F P/S cannot be placed against a consensus median.**
- **Capstone house models** — `P:\Felipe Monteiro\US Equities\Modelos oficiais\` covers NVDA, GOOG, AVGO, COHR, LITE, META, TSM, AAPL and ASML-peers. **No house model exists for SKHYNIX, SAMSUNG, KIOXIA or SNDK**, so baseline 2 is structurally unavailable for the five largest divergences above (items 1-8). ⚠️ **Given that items 1-4 are Korean memory and the cycle now runs at 75-80% operating margins, the absence of a house Korea model is the most consequential coverage gap this reconciliation can point at.**
- **GOOG / LITE / COHR / NVDA optics notes** — no quantitative estimate to reconcile: GF gives ratings without PTs or estimates; FUNDA gives no rating, PT or estimates. The only figures are architecture ratios and a self-labelled upper-bound content estimate (**~$13,700/TPU**, modules/OCS/cabling only, excluding switching). **Not comparable to consensus by construction.**
- ~~**BBG live re-pull** — worth re-running `bloomberg.bdp` once the Terminal is logged in, to confirm the cached `asof 2026-08-19` figures and to fill `BEST_TARGET_PRICE`.~~ ✅ **DONE 2026-08-20 — and it did NOT merely confirm the cached figures: it overturned two of the four Korean rows.** Full live re-fetch (`estimates.json` asof **2026-08-20**, 98/98 names, 0 FAIL, 0 null prices, **0 records byte-identical to the 08-19 vintage**) plus ad-hoc annual-line (`1FY`/`2FY`) pulls for both Korean names. ⚠️ **`BEST_TARGET_PRICE` remains absent from the wrapper output, so PT-vs-consensus placement is STILL not possible** — this is a standing wrapper limitation, not a run-specific failure, and should stop being written as an open item.

---

## Unit guards applied in this run (recurring source of false precision)

1. **"ICI links 6→12" (2x, SemiAnalysis) ≠ "optical ports 1.5→6" (4x, FUNDA/GF).** Different quantities — links are copper + optical, ports are only the wrap-around links leaving the rack. **Never average them; the optical-supply-chain number is the 4x.**
2. **TPU 8i optical ratios are a copper-to-optics transition off a ZERO base (256-chip all-copper pod → ~1.25:1), not a step-down from the 1.5:1 training figure.** Wrong baseline manufactures a false bear.
3. **Kioxia's "datacenter + enterprise >60%" is OF THE SSD & STORAGE SEGMENT**, not of total revenue — must not be read as the Investor Day's FY2028 ">60% of revenue" target already being met.
4. **SNDK's own datacentre mix ~1/3 ≠ SIG's "~50% of INDUSTRY bits in CY26."** Company mix and industry bit share are different denominators.
5. **GF's aggregate 1:8.5 TPU-to-port ratio must not be added to FUNDA's separate 6:1 scale-up figure** — different constructions of the same architecture.
6. **Korean CY-sum EPS inflation (~+20.1% SKHYNIX, ~+6.8% SAMSUNG vs BBG's annual line)** — applied to items 1-3 and to the CONFIRMS table. Without it, this run would have reported a spurious −20.9% SK Hynix EPS divergence and the wrong SIGN on Samsung CY2027 EPS.
7. **Nomura's Unitree TP is struck off the IPO price (CNY150.80), not the post-debut tape** — a +492% debut may already exceed it.

## Figures flagged, NOT adopted

- **Kioxia "¥550 billion a year"** of special employee compensation — implausible against ¥1,326bn of quarterly operating profit; **¥55.0bn** is the likely intended figure. Translated-call artefact.
- **Kioxia EPS rendered as "¥1,621.81 billion"** (and Q2 "¥2,335.7 billion") — obviously per-share; units artefact.
- **FUNDA's ~$13,700/TPU** optical + OCS content — carried with the author's own label: *"a very optimistic, upper-bound estimate."*
- **FUNDA's module ASPs (~$700 1.6T DR8 IMDD, ~$1,500 2.4T Coherent Lite)** — FUNDA estimates, not quoted prices. The ~2.1x step is the single most important assumption behind "value uplift exceeds 4x."
- **Unitree regulatory citations (§2.804(c)(2), §2.911(d)(9)-(11))** — logged as printed, **unverified against primary regulatory text.**
- **"Intel RealSense D435i" at CNY1,869 / 4.5% of G1 BOM** — RealSense was separated from Intel in 2025; **do not book as [[INTC]] revenue** without confirming the current owner of the product line.
---

## BBG resolution — live annual-line pull, 2026-08-20 (`/wiki-consensus`)

_Resolves the `## PENDING` re-pull item. `estimates.json` refreshed to **asof 2026-08-20** (98/98 names live, 0 FAIL lines, 0 null prices, **0 records byte-identical to the 08-19 vintage** — so no silent carry-overs), plus ad-hoc `BEST_FPERIOD_OVERRIDE=1FY/2FY` pulls of `BEST_SALES / BEST_EBIT / BEST_NET_INCOME / BEST_EPS / BEST_EPS_HI / BEST_CAPEX` for both Korean names. JPM figures below are read **directly out of the two workbooks** (`Report-Consol` / `Report` sheets), not back-solved from the percentages this report originally printed._

### 🔴 The headline of the resolution: this report compared broker ANNUAL models to our synthetic CY-SUM, and for Korean names those are not the same number

`estimates.json` builds CY figures by **summing quarterly consensus**. For SAMSUNG and SKHYNIX that sum diverges materially from BBG's own annual consensus line — **in both directions, and on capex as well as EPS**:

| Name | Metric | Our CY-sum | BBG annual line | CY-sum bias |
|---|---|--:|--:|--:|
| SKHYNIX | CY2026 EPS | W320,927 | W349,876 | **−8.3%** |
| SKHYNIX | CY2027 EPS | W566,102 | W463,073 | **+22.3%** |
| SKHYNIX | CY2026 capex | W49,049bn | W45,519bn | **+7.8%** |
| SKHYNIX | CY2027 capex | W62,664bn | W60,234bn | **+4.0%** |
| SAMSUNG | CY2026 EPS | W46,404 | W48,041 | **−3.4%** |
| SAMSUNG | CY2027 EPS | W75,198 | W70,400 | **+6.8%** |
| SAMSUNG | CY2026 capex | W75,972bn | W78,475bn | **−3.2%** |
| SAMSUNG | CY2027 capex | W91,715bn | W98,325bn | **−6.7%** |

⚠️ **The known "+20.1% / +6.8% Korean CY2027 EPS inflation" is confirmed live (+22.3% / +6.8%) — but it is NOT confined to CY2027 EPS.** In CY2026 the bias **inverts** (our sum is 3-8% *below* the annual line) and it is present on **capex** in both years with **opposite signs for the two names**. Unit guard #6 in this report de-biased CY2027 EPS only; every CY2026 row and every capex row was therefore placed on the wrong denominator. **For Korean names, place broker annual models against `1FY`/`2FY`, never against the CY-sum.**

### Re-placement of items 1-4 on the annual line

| # | Name | Metric | JPM (workbook) | BBG annual cons | Δ (was, vs CY-sum) | Verdict |
|---|---|---|--:|--:|--:|---|
| 1 | SKHYNIX | CY2026 EPS | W366,143 | W349,876 | **+4.7%** (was +14.1%) | 🔴 **DIVERGES, de-escalated** |
| 1 | SKHYNIX | CY2026 net income | W265,922bn | W253,477bn | **+4.9%** | — |
| 1 | SKHYNIX | CY2026 revenue / EBIT | W348,253bn / W268,932bn | W349,829bn / W271,095bn | **−0.5% / −0.8%** | inside noise |
| 2 | SAMSUNG | CY2026 EPS (headline) | W50,797 | W48,041 | **+5.7%** (was +9.5%) | ❌ **basis artefact** |
| 2 | SAMSUNG | CY2026 net income | W297,408bn | W308,535bn | **−3.6%** | ✅ **→ CONFIRMS** |
| 3 | SAMSUNG | CY2027 revenue / EBIT | W941,029bn / W549,257bn | W975,122bn / W570,790bn | **−3.5% / −3.8%** (was −5.0% / −5.9%) | 🔴 **DIVERGES, holds** |
| 3 | SAMSUNG | CY2027 net income | W436,712bn | W452,973bn | **−3.6%** | corroborates |
| 4 | SAMSUNG | capex CY26 / CY27 | W79,137bn / W99,300bn | W78,475bn / W98,325bn | **+0.8% / +1.0%** (was +4.2% / +8.3%) | ❌ **→ CONFIRMS** |
| 4 | SKHYNIX | capex CY26 / CY27 | W47,328bn / W60,000bn | W45,519bn / W60,234bn | **+4.0% / −0.4%** (was −3.5% / −4.2%) | ❌ **sign flip** |

### What each row becomes

1. **SKHYNIX CY2026 EPS — STAYS DIVERGES, but at a third of the claimed size, and the missing line is now IDENTIFIED.** The gap is **+4.7% on EPS / +4.9% on net income against −0.5% revenue and −0.8% EBIT** — a ~5.5pt operating-to-bottom-line spread, not the ~15pt the report implied. **The report's action item ("pull the published JPM note to identify the line") is CLOSED from the workbook itself: JPM carries W77,504bn of non-operating income in 2026E (pre-tax W346,435bn against EBIT W268,932bn, i.e. +28.8% of EBIT), taxed at 23.2%.** The disagreement is non-operating income, not tax rate or share count. ⚠️ **And JPM is 18.1% BELOW the street-high EPS (W446,951) — it is a mid-range bull inside the distribution, not an outlier.** Tradeable only if you can form a view on that W77.5tn non-operating line; it is not an operating call.

2. **SAMSUNG CY2026 EPS — WITHDRAWN. This was the run's self-described "highest-conviction item," and it was a share-count basis artefact.** JPM's headline EPS (W50,797) is struck on **common shares only** — its own net income implies **5.855bn shares**, and the workbook carries a second line, *"EPS (W) inc. pref. Shares" = W44,857*. BBG's consensus EPS implies **6.422bn shares** (`BEST_NET_INCOME` ÷ `BEST_EPS`), i.e. a preferred-inclusive blend. **Comparing the two measures a share count, not a forecast.** At **net income — which has no share count in it — JPM is 3.6% BELOW consensus**, sitting consistently with its −1.5% revenue and −3.0% EBIT. **There is no below-the-line anomaly at Samsung, and therefore no "two Korean models from one house, both above consensus below the line" pattern.** The parallel that made item 2 "the highest-conviction item in this run" does not exist: SK Hynix has a real non-operating gap, Samsung has an artefact.

3. **SAMSUNG CY2027 revenue / OP — HOLDS, and is now the strongest surviving row in the run.** Resized to **−3.5% revenue / −3.8% EBIT**, i.e. **~W34tn of revenue and ~W21.5tn of profit below the Street** (the report's ~W50tn / ~W35tn was CY-sum inflation). **It is independently corroborated at net income (−3.6%), and the margin gap is only −17bp — so "not a margin call, JPM simply has less Samsung revenue in the out-year" survives and tightens.** Note this also removes the offset the report described: with item 2 withdrawn, item 3 no longer "runs against" anything — JPM is uniformly below consensus on Samsung in 2027 at revenue, EBIT and net income alike.

4. **Capex MIX — OVERTURNED. The report called this "the widest read-through in the run"; on the annual line it does not exist.** Samsung **+0.8% / +1.0%** and SK Hynix **+4.0% / −0.4%**: JPM is *above* consensus on **both** names in 2026 — and **more above on Hynix than on Samsung**, the opposite of the claimed tilt — and on consensus for both in 2027. 🔴 **The cross-checks this row fired into [[AMAT]], [[LRCX]], [[KLAC]], [[ASML]], [[TOKYOELEC]] and `themes/semicap-wfe` are CANCELLED. Nothing should be positioned on a JPM Samsung-over-Hynix WFE mix; there is no such call in the models.** The original −3.5% / −4.2% Hynix figures were computed against a CY-sum capex that runs 4-8% above the annual line.

### Rows NOT changed by this pull

- **Consensus itself barely moved 08-19 → 08-20.** SKHYNIX CY2026 revenue −0.03% / EPS −0.01%; SAMSUNG, KIOXIA and SNDK estimates **identical to the decimal**. Every change above comes from correcting the *basis*, not from a consensus revision. **Prices moved instead: SKHYNIX W1,624,000 → W1,710,000 (+5.3%), SAMSUNG W257,500 → W273,000 (+6.0%), KIOXIA ¥49,950 → ¥52,950 (+6.0%), SNDK $1,568.87 → $1,594.11 (+1.6%).**
- **Items 5-14** (KIOXIA primary-vs-relay, SNDK HBF/HBM, optics attribution, Unitree, TSLA) are wiki-internal or qualitative and carry no consensus baseline — unchanged, and none is affected by the CY-sum correction.
- **The HEADLINE section stands.** The JPM Korea workbooks were correctly un-rejected: on the annual line SK Hynix CY2026 revenue is **−0.5%** vs consensus at a **77.2% vs 77.5%** operating margin, and Samsung **−1.5%** at **51.9% vs 52.7%** — still comfortably inside noise, so the plausibility-based rejection was still wrong. **Only the size and direction of the residual gaps changed.**

_BBG column resolved 2026-08-20 — `estimates.json` asof **2026-08-20** (98/98 live, 0 FAIL, 0 null prices, 0 byte-identical carry-overs), plus ad-hoc `1FY`/`2FY` annual-line pulls for SAMSUNG and SKHYNIX. **Two rows crossed DIVERGES → CONFIRMS (items 2 and 4); item 1 stayed DIVERGES at a third of its size with its open question closed; item 3 held and was resized.** Canonical header `## Where the new data DIVERGES` applied (was `## DIVERGES (the alpha)`). No web data substituted anywhere._
