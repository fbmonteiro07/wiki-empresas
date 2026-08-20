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

## DIVERGES (the alpha)

| # | Name | New datapoint | Baseline it diverges from | Gap | Read |
|---|---|---|---|--:|---|
| **1** | **SKHYNIX** | JPM CY2026 **EPS W366,143** | BBG cons **W320,967** | **+14.1%** | 🔴 **A BELOW-THE-LINE disagreement, which is what makes it interesting.** JPM is **−0.7% on revenue and −1.1% on EBIT** yet +14.1% on EPS — arithmetically impossible from operations, so it lives in **tax rate, non-operating income or share count**. If JPM is right, the Street's CY26 EPS is ~12% too low on essentially identical operating forecasts. **Action: pull the published JPM note to identify the line.** |
| **2** | **SAMSUNG** | JPM CY2026 **EPS W50,797** | BBG cons **W46,404** | **+9.5%** | 🔴 **Same shape, same analyst, same year — and the parallel is the signal.** JPM is −0.02% on revenue and −1.5% on EBIT, +9.5% on EPS. **Two Korean memory models from one house, both ON consensus at the operating line and both 10-14% ABOVE it on EPS, points to one systematic house assumption below the operating line rather than two coincidences.** Highest-conviction item in this run. |
| **3** | **SAMSUNG** | JPM CY2027 **revenue W941,029bn / OP W549,257bn** | BBG cons **W990,684bn / W583,748bn** | **−5.0% / −5.9%** | 🔴 **The cleanest tradeable divergence, and it SURVIVES every adjustment.** ~W50tn of revenue and ~W35tn of profit below the Street, and it is **not** a margin call (margins within 50bp) — JPM simply has less Samsung revenue in the out-year. Note it runs *against* item 2: JPM is more conservative on 2027 operations while more generous below the line, so the two partly cancel at EPS and the headline EPS delta understates the real disagreement. |
| **4** | **SAMSUNG** | JPM capex **CY26 −W79,137bn / CY27 −W99,300bn** | BBG cons **−W75,972bn / −W91,715bn** | **+4.2% / +8.3%** | 🔴 **Widest read-through in the run, and it is a MIX call not a level call: JPM is ABOVE consensus on Samsung capex and BELOW on SK Hynix capex (−3.5%/−4.2%).** More Samsung spend, less Hynix spend than the Street. Directionally positive for tools levered specifically to Samsung. **Cross-check → [[AMAT]], [[LRCX]], [[KLAC]], [[ASML]], [[TOKYOELEC]], `themes/semicap-wfe`.** |
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
- **BBG live re-pull** — worth re-running `bloomberg.bdp` once the Terminal is logged in, to confirm the cached `asof 2026-08-19` figures and to fill `BEST_TARGET_PRICE` (absent from `estimates.json`, so no PT-vs-consensus placement was possible in this run).

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
