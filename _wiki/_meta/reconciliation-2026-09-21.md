# Reconciliation — 2026-09-21 (/run-inbox 23h, scheduled/unattended)

**Sources reconciled (10 patched of 12 unique; 2 dropped whole — see `_inbox/_ingest-log.md`):**
Bernstein · Stacy Rasgon, *"Notes from the road — Silicon Valley bus tour"*, 2026-09-21 · **Rothschild & Co Redburn · Alex Haissl / Luke Han, *"AI Infrastructure: Capital Carousel"*, 2026-09-21 (148pp PRIMARY)** · Morgan Stanley · Byrd/Faucette, *"Powering AI: Racking Up the Power Shortfall"*, 2026-09-21 · Morgan Stanley · Meta A Marshall, *"Attack of the Agents"*, 2026-09-20 · Goldman Sachs · Gabriela Borges, *"MSFT NDR Meetings"*, 2026-09-20 · Wells Fargo · Ken Gawrelski, *"Meta Platforms — Emerging Product Cycle Story into Meta Connect"*, 2026-09-20 · Jefferies · Joe Gallo, Capstone cyber call, 2026-09-21 · SemiAnalysis · Tanj Bennett (theme-only) · Irrational Analysis (anonymous, theme + 3 pages) · Asymmetrical Bets (paywalled retail Substack).

**Baselines used:**
1. **Prior wiki marks** — read on every page before editing (intra-quarter tables, "where the sell-side stands", `## Changelog`).
2. **Capstone house models** — `_data/house.json` (asof 2026-09-21). Covers **NVDA, META, AVGO, COHR, LITE** (+AAPL, GOOG, TSM, TER, ADVANTEST). **No house model exists for ORCL, MSFT, AMZN, CRWV, NBIS, INTC, NXPI, AMAT, CRWD, PANW, OKTA, MU** — those reconcile on baselines 1 and 3 only.
3. **BBG consensus** — ⚠️ **the live wrapper is DOWN** (`blpapi: could not start session` / `connect event failed` on `localhost:8194` — Terminal logged out, as it always is at this hour). **NOT marked PENDING:** the on-disk snapshot `_data/estimates.json` carries **`asof: 2026-09-21` — same-day**, which is a valid baseline under the standing rule. No web data was substituted. ⚠️ **One exception, see §DATA INTEGRITY: the entire memory complex in that snapshot is unusable.**

---

## 🔴 DIVERGES — the alpha

### ① ★★★ Redburn holds the **STREET LOW** on three names at once, and BBG's own panel already proves it

Every mark below is from the same 148-page note, published the same day. The BBG panel (asof 2026-09-21) has already absorbed them — which independently **validates the PT extraction from the PDF**, because the panel's minimum equals the extracted target to the dollar on three of them.

| Name | Redburn | Consensus PT | vs cons | Panel low | Panel high | n | Flag |
|---|--:|--:|--:|--:|--:|--:|---|
| **ORCL** | **Sell $110** | $240.01 | **−54.2%** | **$110** | $400 | 49 | **= STREET LOW (exact)** |
| **NBIS** | **Sell $84** | $282.84 | **−70.3%** | **$84** | $415 | 25 | **= STREET LOW (exact)** |
| **AMZN** | **Neutral $230** | $329.90 | **−30.3%** | **$230** | $405 | 81 | **= STREET LOW (exact)** |
| **CRWV** | **Sell $54** | $142.63 | **−62.1%** | $39 | $317 | 44 | below cons, not the low |
| MSFT | Neutral $440 (from $400) | $573.69 | −23.3% | $400 | $870 | 71 | near the low |

➤ **This is not five independent calls; it is one thesis expressed five times** — that credit is pricing a risk equities ignore, and that the compute layer is where it bites. ORCL's panel carries **only one Sell among 49 analysts**, and that Sell is now the street low. **Treat the package as a single high-conviction position, and size any read-through accordingly** — if Redburn is wrong, all five marks are wrong together.

### ② ★★★ MSFT: a **45% price-target spread between two houses, 24 hours apart**, with no new company disclosure in between

| Date | House | Rating | PT | vs consensus $573.69 | vs price $501.61 |
|---|---|---|--:|--:|--:|
| **2026-09-20** | **Goldman (Borges)** | **Buy · Conviction List** | **$640** | **+11.6%** | **+27.6%** |
| **2026-09-21** | **Redburn (Haissl/Han)** | **Neutral** | **$440** | **−23.3%** | **−12.3%** |

➤ **The two notes are not arguing about Azure demand — they are arguing about what the capex is worth.** Goldman's NDR note is *management-sourced* (IR's Neilson and Criste, following CFO Amy Hood) and its whole argument is that front-loading long-dated capex bought Microsoft **flexibility** (long-dated mix ~50% → ~33% over three quarters; GPU dock-to-live −50%; the binding constraint now shell space, not chips). Redburn's is an *accounting* argument: **>$1trn of uncommenced leases across AMZN/MSFT/META/ORCL, with MSFT the most exposed at ~$330bn**, which at ~19% yield-on-cost is ~$300-400bn of self-build-equivalent obligation that never passes through reported FCF. **Both can be true.** The falsifiable bridge is Redburn's Azure line: **FY29E Azure $253.1bn vs consensus $296.0bn — a $43bn hole, −14.5%.** ➤ **That is a modellable, dated edge and it belongs in the edge tracker.** Note Goldman's own model already shows the squeeze Redburn is pricing: **GS has MSFT FCF falling FY26A $66,987m → FY27E $40,027m → FY28E $11,903m** (a 0.3% FCF yield) before recovering — i.e. the bull case concedes the cash-flow trough, it just refuses to capitalise it.

### ③ ★★ META: the PT went **up 24%** while the estimates went **down** — and the apparent size of the cut is mostly below the line

Wells Fargo (Gawrelski) **raised its PT to $796 from $640 (+24.4%)** while cutting EPS. The PT bridge is arithmetically **pure multiple**: **25.0× × $31.86 = $796.5** vs prior **20.0× × $32.07 = $641.4**. Every dollar of the $156 increase is re-rating, none is earnings.

⚠️ **Reconcile at EBIT, not EPS** — the standing below-the-line guard changes the conclusion by ~4×:

| Metric | WF new | BBG consensus | WF vs BBG |
|---|--:|--:|--:|
| FY26 EPS | $29.31 | $34.98 | **−16.2%** |
| **FY26 EBIT** | **$80,240m** | **$86,785m** | **−7.5%** |
| FY27 EPS | $31.86 | $38.34 | **−16.9%** |
| **FY27 EBIT** | **$99,255m** | **$103,501m** | **−4.1%** |

➤ **The headline "17% below consensus" is not an operating call — at EBIT the FY27 gap is 4.1%.** And the FY26 cut is explicitly a one-off: verbatim, *"Reduce '26 OI estimate by 12%, primarily driven by legal settlement with $10B charge in 3Q:26. Trim '27 / '28 OI by 1%."* The quarterly split proves it — **Q3:26 EPS $3.59E vs $6.98E prior while Q4:26 is flat ($9.09E vs $9.12E)**; the entire annual cut lands in the accrual quarter.

**vs the house model** (`Modelo Meta pós 2Q26`, 2026-06-11): house 2026E EPS **$32.72**, 2027E **$38.24**.
- House 2027E is **+20.0% above Wells Fargo** and **−0.3% vs BBG** — i.e. **the house is sitting on consensus and Wells Fargo has stepped away from both.**
- ⚠️ **Curiosity worth noting, not a finding:** the house's 2026E EPS of **$32.72 is exactly Wells Fargo's *prior* 2026 number.** Same vintage of consensus, not evidence of anything — but it means **this cut moves the Street below the house for the first time on that line.**

### ④ ★★ ORCL: the Sell rests entirely on **out-year margin**, and the only clean same-basis check says revenue is fine

⚠️ **Basis guards — do not net these:** Redburn is **Y/E May** and **GAAP**; the page's BBG snapshot is calendar-year and **adjusted**. The *only* clean comparison is revenue.

| FY27 (Y/E May) | Redburn | BBG 1FY | Δ | Basis |
|---|--:|--:|--:|---|
| Revenue | $90,459m | $90,418m | **+0.05%** | ✅ same basis — **in line** |
| EBIT | $29,032m (GAAP) | $36,102m (adj) | −19.6% | ❌ GAAP vs adjusted — not comparable |
| EPS | $6.63 (GAAP) | $8.16 (adj) | −18.8% | ❌ GAAP vs adjusted — not comparable |

The note's **own** internally-consistent comparison (vs Visible Alpha, same basis) is the one to use — and **all 18 internal cross-checks recomputed and tied exactly**:

| vs VA consensus | FY27 | FY28 | FY29 |
|---|--:|--:|--:|
| Revenue | (0.0%) | +1.0% | (2.8%) |
| Operating profit | (1.3%) | (7.3%) | **(14.6%)** |
| EPS | +0.7% | **(12.8%)** | **(21.3%)** |

➤ **Redburn is AT consensus in FY27 and 13-21% below in FY28-29. The Sell is a duration call on margin, not a demand call** — and they *raised* their own numbers into it (revenue +0.5/+2.8/+2.1%, EPS +12.7/+7.0/+1.3%). ➤ **Critically, it is not Oracle-specific:** the same note has MSFT at (14.0%) and AMZN at (15.5%) below consensus on out-year GAAP operating profit. **This is a house view on hyperscaler out-year margins wearing three different tickers.** Dated test: the **Oracle Financial Analyst Meeting, 2026-10-28**.

### ⑤ ★★ NVDA: Redburn's own bull case quantifies the bear case — $126.5bn of FY27 demand is vendor-stimulated

Redburn is **Buy, PT $325** — which is **+0.7% vs the consensus PT of $322.70**, i.e. *exactly at consensus*, from a note whose entire thesis is that the build-out is credit-fragile. Bernstein the same day is **Outperform $400 (+24.0% vs consensus)**.

The number that matters is not the target, it is this: Redburn estimates **"stimulated demand" at $126.5bn = 33% of FY27 data-centre revenue**, on a path **FY24 3% → FY25 14% → FY26 36% ($70.5bn of $194bn) → FY27E 33% → FY28E ~16% → FY29E ~6%**; sensitivity at 75% of lab capital going to compute takes FY27 to **~$185bn = 49%**.

➤ **Cross-check against the house model:** `Modelo Felipe NVDA` has 2026E DC revenue **$379bn**; Redburn's 33% of "c$381bn" FY27 DC revenue implies essentially the same base (NVDA FY27 ends Jan-2027 ≈ CY2026). **The two models agree on the denominator and disagree on nothing except whether a third of it is self-funded.** The house carries no stimulated-demand haircut at all. ➤ **This is the cleanest "same numerator, different quality-of-revenue" divergence in the batch** — it does not change FY27 EPS, it changes what multiple that EPS deserves, which is precisely the MSFT argument in ② wearing a different ticker.

⚠️ Redburn's rebuttal is on the record and should be carried with it: the activity is disclosed not hidden; the stimulated share **fades to ~6% by FY29E**; and NVDA *"sits above the part of the buildout we are most cautious on rather than inside it."*

### ⑥ ★ AMAT: Bernstein's ~$300bn 2028 WFE is **~15-20% above the Street** — but it is a derivation, not a company forecast

AMAT management (Chen/Haran/Parker) told the tour it is **doubling quarterly output capacity by 2028** with customer discussions running to 2030, and that planned capacity *"would support a market of that magnitude based on current share."* Bernstein frames that as **~$300bn vs Street ~$250-260bn for 2028**.
➤ ⚠️ **Share is the free variable and AMAT did not forecast the market** — the page carries it explicitly as Bernstein's derivation. ⚠️ **And it is cheap optionality, not conviction: ~80% of AMAT's cost structure is variable**, so the capacity can be unwound. Against the wiki's existing marks (UBS ~$226bn/~$275bn; buy-side mode $290-300bn) this **corroborates the high end from the supply side for the first time** — a capital commitment rather than an opinion. Bernstein PT **$700 vs consensus $660.63 (+6.0%)**.

### ⑦ ★ MS raises its own US power shortfall 50% — but **~15 GW of the move is MS correcting its own double-count**

Headline: '26-28 US DC incremental demand **97 GW** (from 68); gross shortfall **57 GW from 38 GW**; net of "time to power" solutions **33 GW = 34% of chip demand**.
➤ 🔴 **The relay that reached the wiki at 21h attributed the entire 19 GW widening to the NVL72 rack re-spec. The primary says otherwise, verbatim:** *"part of the Net Shortfall increase was the elimination of a **double-counting of PSP sites**, artificially reducing the shortfall by ~15GW in the previous model."* **The demand raise (68→97 GW) is the rack re-spec; roughly half the *net* move is bookkeeping.** Anyone who read only the relay is over-reading the fundamental signal by about half. Guard written onto all six power pages.
➤ Second-order: on MS's **own high case** the remedies (BTM turbines 49 + Bloom 8 + nuclear 8, probability-weighted 57 GW) **close the gap entirely (0 GW net)** — so the shortfall is a base-case artefact, not a physical certainty.

### ⑧ ★ Optical: a falsifiable engineering attack on COHR's laser — and the "LITE wins" read does **not** follow

An anonymous engineering newsletter (self-disclosed semis positions, did **not** attend ECOC) claims Coherent's UHP/CPO/NPO 400mW laser reports **intrinsic/instantaneous linewidth** rather than the **effective beta-separation linewidth** that governs link quality, and therefore *"catastrophically fails the 1 MHz effective linewidth spec of all standard NPO and CPO systems, including OCI MSA."*
➤ ⚠️ **The decisive evidence is a bitmap.** The PDF text layer contains none of the plot's values, so the area-under-curve comparison behind *"100% proof"* **could not be machine-verified**; it is the author's reading of a chart we have not measured.
➤ 🔴 **The important catch: his own Lumentum figure is 0.5-1.2 MHz effective — a range that STRADDLES the 1 MHz spec he says Coherent fails.** *"Coherent fails"* is therefore **not** the same claim as *"Lumentum passes"*, and LITE was scored **⚠ nuance, not ✓** on that basis.
➤ **vs house:** the Capstone initiation on COHR (2026-09-01) is already **NEUTRAL, PT $285** with CY27E EPS $11.30 — so this **adds a downside mechanism to a stance the house already holds** rather than challenging it. **BBG consensus PT $417.88 vs the house's $285** is the standing divergence, and tonight's note cuts the house's way. For LITE, house 2027E EPS **$30.02 vs BBG 2FY $33.91**.

---

## ✅ CONFIRMS — no action

| Item | New datapoint | Prior baseline | Read |
|---|---|---|---|
| **AVGO XPU scale** | Anthropic 5GW is *"Anthropic-specific demand (they are writing the checks)"*, separate from Google's internal TPU demand; 2027 sites *"largely complete"*, 2028 *"sufficiently advanced"* (Bernstein/Hock Tan, 09-21) | The page's 09-21 notion-ingest already had JPM's Sur and Jefferies' Curtis describing the 10GW as two product lines | **Management resolves the ambiguity in favour of the "separate demand" reading.** Bernstein PT $575 vs consensus $531.89 (+8.1%) |
| **AVGO revenue frame** | *"If customers ultimately deploy the full GW amounts, revenue would be higher than the current outlook of $115B/$230B"* for 2027/28 | House AVGO 2026E/2027E EPS $12.89/$21.07, **+10% above BBG on both** | House already sits above consensus in the direction management is pointing — **consistent, no change** |
| **CRWV funding cost** | Full DDTL ladder: SOFR+962bp (Jul-23) → +225bp trough (Mar-26, Meta) → **+550bp (Aug-26, undisclosed)** | Page carried 5.9% (DDTL 4.0 fixed) and ~10% (5yr unsecured) from SemiAnalysis 07-06 | **Redburn independently reproduces both marks.** Not netted — different instruments/seniority. The *arc* is net-new: the round-trip is the argument, not the level |
| **NVDA consensus PT** | Redburn $325 | BBG consensus $322.70 (n=82, 79 buy / 2 hold / 1 sell) | Dead on consensus — **no PT signal**; the signal is the stimulated-demand math (⑤) |
| **INTC / NXPI** | Bernstein MP $110 / MP $290 | Consensus $118.55 / $312.96 | **−7.2% / −7.3% — both ordinary**, inside the panel, no edge |
| **Cyber re-rating** | Gallo: average name **+~100% since April 10th**, *"priced for perfection"* | MS "Attack of the Agents" scenario work (already ingested 09-20) | Two houses, same conclusion on the setup. ⚠️ **Corrected in place: Gallo's *"both very cheap"* refers to Check Point and Zscaler, NOT CRWD/PANW** |
| **OKTA** | Gallo: *"our favorite name here is Okta"*; VAR agentic-security mind share **16% → 36%**, tied 1st with Microsoft | Page had "conversion, not direction" as the open debate | First *measured* read on that debate — but **opinion, not bookings**, and a 16→36 move in one quarter is narrative-speed. Logged, not adopted as evidence of conversion |

**Not reconcilable (no consensus/house exists):** the SemiAnalysis MoE-inference architecture note (theme-only, no company), the Asymmetrical Bets agentic-commerce piece (paywalled, no numbers for BKNG/UBER), and the BTG CoreWeave transcript (already ingested 21h; no new datapoint).

---

## ⚠️ DATA INTEGRITY — the BBG memory complex in `estimates.json` is **unusable**, and four wiki pages are publishing it

Found while building baseline 3. **This is not tonight's ingest — it is pre-existing and already committed**, and it affects live published pages.

| Ticker | Last reported FY revenue | 1FY consensus | Implied growth | Implied EBIT margin |
|---|--:|--:|--:|--:|
| **MU** | $37,378m | **$129,507m** | **+246%** | **76.2%** |
| **SKHYNIX** | ₩97.1tn | **₩347.6tn** | **+258%** | **77.4%** |
| **KIOXIA** | ¥2.34tn | **¥10.08tn** | **+331%** | **79.3%** |
| **SNDK** | $20,248m | **$48,826m** | +141% | **79.5%** |

➤ **The entire memory complex — and only the memory complex — shows ~2.5-4× revenue jumps at ~76-80% EBIT margins.** No DRAM or NAND maker has ever run an 80% operating margin; Micron's best-ever gross margin is ~60%. MU's **1FQ alone ($51.3bn) is 37% larger than its entire last fiscal year**.
➤ **`_wiki/MU.md` is currently publishing a consensus snapshot claiming Micron does $163.7bn revenue at 83.2% gross margin and $96.98 EPS in CY2026.** Same for SKHYNIX, KIOXIA, SNDK.
➤ It is **long-standing and drifting normally** (MU's line went $163.1bn → $163.4bn → $163.7bn across the 09-17/09-18/09-21 rebuilds), so the pipeline is running — it is reading the wrong field or scale for these names, not failing.
➤ **Action taken tonight:** MU was **excluded as a reconciliation baseline** (the MS memory-content read-through on MU.md was filed against the note's own BoM figures, not against consensus). **NVDA 65.4% and AVGO 66.9% EBIT margins also tripped the screen but are legitimate**; APP 77.9% is legitimate. **A dedicated fix to `fetch_estimates.py` / `build_snapshot.py` for the memory names is required before any memory number in this wiki is quoted.**

---

## Cross-source tensions logged but NOT resolved

1. **Substrates.** NVDA (Kress/Hari) calls substrates *"manageable"*; Intel (Pitzer) calls acceptable large-format substrates and supplier yields **the** binding constraint on EMIB-T and is raising capital partly to secure them — **within 48 hours, from two managements**. Neither adopted.
2. **Time-to-power vs terminal cost.** MS solves for speed (powered shells at $10-12/watt, 15-19% unlevered FCF yields, a one-year time advantage worth ~$4.5/watt ≈ $80/MWh); Redburn solves for the cost curve (fuel cells $0.11-0.13/kWh, nuclear >$0.10 vs ~$0.06 for on-site gas — *"what looks like an acceptable premium during a period of scarcity can ultimately become a structural cost disadvantage"*). **Falsifiable on contract TENOR**, which neither states.
3. **Memory de-spec.** Bernstein has NVDA *"not currently pursuing memory de-specification for existing architectures (including Vera Rubin)"*; Jefferies on 09-20 had *"4hi work acknowledged, nothing decided."* Sharpened, not superseded.
4. **HBM tiering.** SemiAnalysis argues idle KV should move to network-attached DDR because HBM is *"too expensive and supply-constrained to be a good default for passive context storage"* — **the opposite side of this wiki's own 09-11 expert** ("cold tiers do not substitute"). Both retained.
5. **MS internal contradiction on cyber share gains.** The sector note reads *"~50bps of share gains… vs ~100bps for CRWD"* as what the **price contains**; the single-name notes read CRWD as embedding only ~75bps against MS's ~100bps expectation. **On the sector note's own reading there is no CRWD share-gain gap at all.** Direction survives, magnitude does not.
6. **Redburn's ~70% backlog concentration** appears twice with different scopes (p27: OpenAI + Anthropic; p44: + Meta). p44 version kept, marked approximate.

---

## Recommended for the edge tracker

1. **MSFT — Redburn FY29E Azure $253.1bn vs consensus $296.0bn (−14.5%).** Dated, modellable, and the cleanest expression of the "capex is worth less than you think" thesis. Paired against Goldman's $640 Buy-CL from the day before.
2. **ORCL — Redburn FY29 operating profit −14.6% / EPS −21.3% vs VA consensus**, with the **2026-10-28 Financial Analyst Meeting** as the dated test. Street low, 1-of-49 Sell.
3. **NVDA — $126.5bn (33% of FY27 DC revenue) of stimulated demand** against a house model carrying no haircut on the same denominator. A quality-of-revenue divergence, not an estimate divergence.
4. **META — house 2027E EPS $38.24 vs Wells Fargo $31.86 (+20%)**, house at consensus. ⚠️ Reconcile at EBIT (WF −4.1% vs BBG), not EPS (−16.9%).
