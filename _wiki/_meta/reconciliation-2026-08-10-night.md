# Reconciliation — 2026-08-10 (night /run-inbox)

**Source reconciled:** J.P. Morgan · Jay Kwon / Sangsik Lee / Neelay Kamath / Harlan Sur / Mio Shikanai — *"Global Memory Market: Global Memory TAM and S&D update"*, **2026-08-09**, 43pp. (The other ingested file, the MS scale-up primer of 2026-07-13, was a duplicate; its only new quantitative item is a **correction**, treated separately at the bottom.)

**Baselines used:**
1. **Prior wiki marks** — read off the patched pages before editing.
2. **Capstone house models** — `_data/house.json`, asof 2026-08-10. ⚠️ **Covers only 8 names: AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM. There is NO house model for MU, SKHYNIX, SAMSUNG or KIOXIA** — i.e. the entire memory complex this note is about is unmodelled in-house. That is itself a finding (see §6).
3. **BBG consensus** — `_data/estimates.json`, **asof 2026-08-10 18:31 (same-day on-disk snapshot)**. ⚠️ **The live Terminal was NOT reachable on this run** — `bdp()` returned `HTTP 503: "Bloomberg connection test failed - please ensure you are logged in to Bloomberg Terminal"` (blpapi could not connect to 127.0.0.1:8194) at 23:37. **No refresh was possible; no web data was substituted.** The on-disk snapshot is only ~5 hours old, so it is used as the consensus baseline rather than marking the column PENDING — but it is a snapshot, not a live read.
   - ⚠️ **Standing caveat applied:** `estimates.json` CY2026 sums embed **pre-print consensus for already-reported quarters**, so CY2026 understates. Only two forward quarters are stored (`1FQ`, `2FQ`), so a sum-of-quarters rebuild of CY2026 is not possible from this file. **CY2027 is the clean column and the comparisons below lean on it.**
   - FX for cross-currency comparison: **~1,380 KRW/USD, ~150 JPY/USD, assumed** — BBG FX was unavailable this run. All KRW/JPY figures are also given natively so the conversion can be redone.

---

## DIVERGES — where this note disagrees with what the wiki already holds (the alpha)

### ① ★ THE BIG ONE: JPM's 2027 HBM industry revenue is ~35-40% BELOW the level implied by the UBS marks already on the wiki. Two houses, same industry, same year, ~$75bn apart.

| 2027E HBM industry | JPM (08-09, NEW) | UBS (08-07, already on wiki) | Gap |
|---|---|---|---|
| Bits | **6,268mn 1GB-eq ≈ 50.1bn Gb** (demand); 7,205mn ≈ 57.6bn Gb (procurement, t+4mo) | **61.5bn Gb** end-consumption (raised from 58.7bn) | **JPM ~19% lower** on the demand basis |
| Blended ASP | **~$2.75/Gb** ($22.0 per 8Gb-eq) | **HBM4 $3.5/Gb, HBM4E ~$3.9/Gb** → blended ~$3.6 | **JPM ~24% lower** |
| ASP growth y/y | **+42%** | **+79%** | **JPM is barely half** |
| **Industry revenue** | **$145,617mn** | ~**$221bn** implied (61.5bn Gb × ~$3.6) | **~$75bn / ~34% lower** |

- **The two disagreements compound rather than offset** — JPM is lower on *both* volume and price, in the same direction.
- **⚠️ Basis warning, stated so the gap is not overstated:** UBS's "end-consumption" and JPM's "bit demand" / "procurement demand (t+4 months)" are **three different bases**, and JPM's own procurement line (57.6bn Gb) closes most of the *volume* gap with UBS's 61.5bn Gb. **The price gap does not close on basis.** The **+42% vs +79% ASP disagreement is a clean, like-for-like, same-metric, same-year conflict with no basis escape** — and it is the single most actionable divergence in this run.
- **JPM says it is deliberately conservative:** *"far more reasonable but shy of the market's bullish expectation of 2x y-y."* So JPM knows it is the low mark. **UBS's +79% is closer to the "market expectation" JPM is arguing against.**
- **Neither adopted.** Both retained on `themes/hbm-memory.md` with their dates. **This is the number to resolve — it drives the 2027 earnings power of MU / SKHYNIX / SAMSUNG more than any other single assumption in the memory complex.**

### ② JPM's HBM shortage is NARROWING versus its own prior model — a quiet negative revision inside a bullish note.

| HBM S-D glut | 2026E | 2027E | 2028E |
|---|---|---|---|
| JPM **May-26** model | −20% | **−35%** | −37% |
| JPM **Aug-26** model (NEW) | −15% | **−14%** | −22% |
| Accumulated (weeks), 2027E | | **−13.9 vs −24.2 prior** | |

- The note's framing is *"softening shortage but still a shortage"* and it does not lead with this. **The wiki was carrying the May-model shortage depth; it should be marked down.** Recorded as JPM's mark, not adopted.
- **Part of the narrowing is packaging, not memory:** CoWoS yield revised **+1/+1/+3pp to 92%/94%/96%**, which mechanically adds shippable HBM bits. Flagged on `themes/cowos-packaging.md`.

### ③ JPM pre-commits to the bear side of a question Morgan Stanley says is still open.
- **JPM: "assume 70% of SKUs adopt the downsized HBM specs for Rubin/Rubin Ultra."**
- **MS Asia (08-10, on `NVDA.md` directly below the new JPM row): the Rubin Ultra spec is "several SKUs," high-end HBM4E 8-Hi vs lower-end variants, "decision still open until end-3Q26."**
- **A 70% assumption is a modelling choice presented as an input.** If the tiered mix skews richer than 70% downsized, JPM's HBM bit cut (−4%/−10%/−19%) is too deep and its HBM revenue too low — which would also narrow divergence ①. **Flagged on `NVDA.md` as the number to attack.**

### ④ SK hynix buyback sizing: a 2-6x spread on the same disclosed intent.
- **UBS (08-07):** Won **12tn** 2H26 buyback.
- **JPM (08-09, NEW):** buyback of **W29.3tn (2026E)** and **W73.3tn (2027E)**; cash yield **5.4% / 16.7% / 9.5%** across 26/27/28E.
- Only the **timing** (within 3Q26) is company-disclosed. Both are estimates. **Logged on `SKHYNIX.md`, not netted.**
- **BBG cross-check gives JPM room:** SKHYNIX CY2027 consensus EBIT **KRW 433.4tn (~$314bn)** on revenue KRW 544.0tn. A W73.3tn return is ~17% of consensus EBIT — **arithmetically comfortable**, so JPM's larger number is not implausible on consensus earnings. It is the *payout policy*, not the earnings capacity, that is uncertain.

### ⑤ Samsung's capital-return FORM is modelled two different ways on the same page.
- **JPM models 100% dividend / ZERO buyback across 2026-28E** (yield 8.3% / 8.8% / 10.7%).
- **BofA (08-07, same page)** reports a capital-return **execution schedule** with a buyback component.
- Matters for per-share compounding, not for total cash returned. **Flagged unreconciled on `SAMSUNG.md`.**

### ⑥ MU's HBM share: JPM models it FLAT, against management's own on-the-record framing.
- **JPM: MU HBM share by sales 20% ('25) → 20% ('26E) → 21% ('27E) → 20% ('28E)** — flat.
- **The wiki carries MU management's "HBM share = DRAM share, and reached" framing** plus the SIG (08-10) view of *"HBM share gains against SK Hynix."*
- **JPM does not argue against management — it simply does not model share gains.** A silent disagreement, which is the easiest kind to miss. Both retained on `MU.md`.

### ⑦ CXMT capacity: two houses, two irreconcilable bases (carried forward from 08-10 PM, now with a second data point).
- **UBS (08-07 initiation):** 240K → 292K → 382K → **466K wpm end-28E**, ~9-10% bit share '27.
- **JPM (08-09, NEW):** **16% capacity / 11% bit share by 2028E**, citing reported ambition *"as high as 600K wfpm"* plus a new Beijing greenfield; **~60% bit/wafer discount**, 2-3yr tech gap.
- Installed-and-validated (UBS) vs reported ambition (JPM). **Not reconcilable as stated. The house has no CXMT capacity mark.**

### ⑧ WATCH ITEM against the house book: the Rubin Ultra de-content vs the house's above-consensus NVDA.
- **House model (`house.json`, asof 08-10): NVDA 2027E revenue $661bn, EPS $15.44.** BBG CY2027 consensus: **$568bn / $12.91.** **The house is ~16% above consensus on revenue and ~20% on EPS.**
- **JPM's new datapoint is a de-CONTENT, not just a de-spec:** *"Rubin Ultra — 4 compute dies originally to 2 compute dies"*, plus the HBM ladder 1,024→576GB and 768→384GB.
- **A halving of compute dies is an ASP-relevant product change, not only a memory-content change.** The wiki's established reading (UBS 08-07) is that de-spec is *volume-offset* — more GPUs, same or more total consumption — which protects the memory names. **It does not automatically protect NVIDIA's revenue per unit.**
- **This is not a contradiction of the house number — JPM makes no NVDA revenue forecast — but it is the mechanism by which an above-consensus NVDA 2027 could be wrong, and the house is carrying the above-consensus position.** Logged as a watch item; **no house number changed.**

---

## CONFIRMS — where the new datapoints corroborate what the wiki/consensus already holds

### ⑨ ★ JPM's $1,442bn 2027E memory TAM is corroborated BOTTOM-UP by BBG consensus company revenue — it is not a broker outlier.
Aggregating CY2027 consensus revenue for the four listed pure-plays against JPM's industry TAM:

| CY2027E consensus revenue | Native | ≈US$bn |
|---|---|---|
| MU | $262,475mn | **262** |
| SK hynix | KRW 544.0tn | **394** |
| Kioxia | ¥12.54tn | **84** |
| Samsung (TOTAL company, incl. non-memory) | KRW 990.2tn | 717 → **memory ~390 assumed** |
| **Sum (Samsung memory portion assumed)** | | **~1,130** |
| **JPM 2027E memory TAM** | | **1,442** |
| **Implied residual for China / Taiwan / Solidigm / others** | | **~312 ≈ 22%** |

- **A ~22% residual for CXMT + YMTC + Nanya + Winbond + Powerchip + Solidigm is plausible** and sits close to JPM's own China share assumptions (11% DRAM bits, 16% NAND bits by 28E). **✓ The TAM reconciles.** ⚠️ The Samsung memory split (~54% of company revenue) is **my assumption, not a disclosure or a JPM figure** — it is the one soft input in this check.

### ⑩ JPM's memory capex is consistent with BBG consensus capex for the big three.
- **JPM 2027E: total memory capex $172.1bn, of which DRAM $144.3bn.**
- **BBG CY2027 consensus capex:** MU **$52.2bn**; SK hynix KRW 63.7tn ≈ **$46.2bn**; Samsung KRW 91.1tn ≈ **$66.0bn** (⚠️ **total company — includes foundry/logic/display, so only a portion is memory**); Kioxia ¥498bn ≈ **$3.3bn**.
- MU + SKH alone = **~$98bn**; adding a memory portion of Samsung's capex plus China/Taiwan brings the total into JPM's **$172bn** range. **✓ Broadly confirms — JPM's capex step-up is already in consensus, not incremental news.**

### ⑪ AMD: JPM's +50% 2027E HBM bit revision is directionally consistent with consensus' MI450 ramp.
- **JPM raises AMD HBM bit demand +9%/+50%/+12%** (235/634/999mn 1GB-eq), procurement **+52%/+61%/+22%** — **the only accelerator line revised UP in a note that cut industry HBM demand.**
- **BBG: AMD CY2026 $50.4bn → CY2027 $86.6bn (+72% y/y)**, EPS $7.50 → $15.31. Consensus already embeds a steep ramp. **✓ Confirms** — an independent, memory-side, bottom-up corroboration of the MI450/MI455 volume story. **No house model for AMD** to compare against.
- ⚠️ **Unresolved and left open:** SemiAnalysis (07-21/07-24) documented Meta's custom MI450/MI455 cutting HBM **12 stacks → 6, 12-Hi → 8-Hi**. JPM raises bits anyway, implying **units more than offset content**; it does not reconcile the two and does not disclose its AMD content assumptions. **Treated as a units call, not a content call.**

### ⑫ AVGO: three independent marks now converge, and the house is at consensus.
| AVGO 2027E | Revenue | EPS |
|---|---|---|
| **House model** (`house.json`) | $190bn | $21.07 |
| **BBG CY2027 consensus** | $190.7bn | $21.28 |
| **Mizuho** (08-09, ingested this afternoon) | $184bn (F27) | $21.27 |

- **The house is effectively AT consensus on AVGO 2027 — no edge either way**, which is worth stating plainly given how much AVGO content the wiki has taken on this week.
- JPM's new AVGO datapoint (the SEC **>$200bn LTA at 90-95% HBM-for-ASIC**) is **supply-securing and qualitatively supportive** of the 2027-28 ASIC ramp, with **no numerical conflict**. ⚠️ The allocation is JPM-modelled and the "OpenAI/Anthropic" customers are JPM's own hedge — **not adopted as company datapoints.**

### ⑬ Kioxia's TSR math checks out on consensus earnings.
- **JPM: TSR yield 0% ('25A) → 4% ('26E) → 8% ('27E), then 45% cumulative for 27E-29E** (32% even if 2029E falls 70%).
- **BBG: KIOXIA CY2027 EPS ¥13,533 against a ¥48,010 price — a ~3.5x P/E.** At that earnings level a 50% FCF payout produces very large yields arithmetically. **✓ The 45% is internally consistent** — but it rests **entirely on JPM's own 50%-FCF-payout assumption**, which is not policy. **Not adopted.**

### ⑭ The ASIC-overtakes-NVDA crossover corroborates the wiki's ASIC ramp from an independent direction.
- **JPM HBM bit-demand mix: ASIC 22% ('25) → 35% ('26E) → 48% ('27E) vs NVDA 69% → 59% → 42%.**
- Independently reached from a **memory bill-of-materials** model, versus the wiki's existing accelerator-unit evidence (Mizuho total ASICs 9.4M → 38M '26-29E). **✓ Two different modelling routes, same conclusion.**
- ⚠️ **Honest debit recorded on every page it was filed to:** roughly **half the crossover is NVDA content coming DOWN**, not ASIC units going up. **Read alone it overstates relative ASIC strength.**

---

## Also new, with NO baseline to reconcile against (logged, not adopted)

- **HBF spec** (stacked NAND 8-hi/16-hi, up to **512GB**, **~0.4–3TB/s**) — no prior quantified mark anywhere on the wiki; there is no consensus or house analogue for a pre-revenue product category. Filed to `themes/cxl-memory-fabric.md`.
- **YMTC bit/wafer at parity with the leading makers; ~16% of global NAND supply by 2028E** — **first quantified YMTC read on the wiki.** No baseline. **The derived conclusion — oversupply risk sits "more in NAND vs DRAM" — is the load-bearing one and lands hardest on `KIOXIA` and `SNDK`.**
- **Memory OPM "new norm" high-70%** (76%/78%/77%) — cross-checks loosely against BBG CY2027 consensus GM of **86.0% (MU)**, **83.7% (SKH)**, **82.4% (Kioxia)**; different metric (OPM vs GM) so **not a like-for-like check**, but the direction is consistent with consensus already modelling structurally elevated memory margins.
- **Peak market cap / memory TAM at 2.8x → "~50% upside on 27E, ~88% on 28E"; 4x P/EBIT → ~110%.** ⚠️ **Mkt-cap basis is SEC + SKH + MU only.** A relative-value frame, not a forecast. **Not adopted.**
- **AI CPU unit TAM +155% CAGR** (Vera/Rosa) — no baseline on the wiki for AI-CPU *units*; the adjacent mark is BofA's server-CPU TAM ~$170bn by CY30 on `themes/custom-asic-tpu.md`, a **revenue** basis, so not comparable.
- **CoWoS yield 92/94/96%** — no baseline; and JPM does not define the basis. **Held as JPM's construct.**

---

## Correction applied this run (not a reconciliation — a factual fix)

**`themes/custom-asic-tpu.md` — MS accelerator unit share, 2026E.** The page carried **"Google TPU ~13%"** since 07-17, taken from the **MS Tech Talk podcast companion**. The **primary note's Exhibit 10 (p.10)** reads, in legend order: **AMD 3% · Other AVGO ASIC 2% · AWS Trainium 11% · NVIDIA GPU 48% · Google TPU 24% · Other 13%** — **the relay assigned the residual "Other" bucket to Google TPU.**

- **Corrected value: Google TPU = 24% of 2026E accelerator units.**
- **Internal-consistency check that settles it:** 24% puts TPU units at **roughly half of NVIDIA's**, consistent with the **~3.1-3.2mn 2026 TPU production** already on `GOOG.md` against ~6-7mn NVDA units. **13% (~1.7mn) contradicted every TPU unit mark the wiki carries.**
- **Materiality:** `custom-asic-tpu.md` hosts an active **12-15M (Fubon) vs 20-35M (Mizuho) 2028 TPU fork**, and the 2026 base feeds it. A 13% base made the aggressive end look impossible.
- **Thesis-drift rule applied** — old sentence retained in place, correction appended beneath, old value logged in the page Changelog.
- **⚠️ Process finding: this is the second relay-corruption caught this quarter** (after the TER "10-20 months"→weeks unit inversion). **The standing rule is reaffirmed: when a primary and a desk/podcast relay both exist, the primary wins and the relay's residual value is the Changelog entry.**

---

## Open items for the next run

1. **Resolve divergence ① (JPM +42% vs UBS +79% 2027 HBM ASP).** Highest-value open question in the memory complex; drives 2027 EPS for MU/SKHYNIX/SAMSUNG more than any other assumption.
2. **BBG live read was unavailable** (Terminal offline, 503). Re-run `fetch_estimates.py` + `build_snapshot.py` when the Terminal is up, then re-check ⑨/⑩/⑪ against a live pull rather than the 18:31 snapshot.
3. **No house model exists for MU, SKHYNIX, SAMSUNG or KIOXIA** — the entire memory complex, which is the single most active theme on this wiki, has no Capstone house numbers to reconcile against. **Raised as a structural gap, not a task artefact.**
4. **`P:\US Equities\Relatórios para a wiki\20260726_Bernstein_NVDA_Global_Memory-_NVIDIA_-_Broadcom-_Quick_thoughts_on_stra.pdf` has been file-locked and skipped on at least two consecutive runs and has NEVER been ingested.** Needs a manual copy — it is a memory/NVDA/AVGO note and therefore directly relevant to divergence ①.
5. **CXMT still has no wiki page** despite two houses now modelling it as a load-bearing input (third consecutive run raised). **KEYS** and **SMTC** also unpaged; KEYS was the MS note's only rating action (upgraded EW → OW, PT $350 → $400).
