# Reconciliation — 2026-09-14 (/run-inbox, 6 sources)

_Two compiles of the analyst's own GS Communacopia small-group and broadcast notes (24 + 15 meetings), a SemiAnalysis
HBM article, a FundaAI cybersecurity note, a contaminated Semtech management call, and a **ten-month-stale** Morgan
Stanley agentic-commerce note swept off the P: backlog._

> ⚠️ **NEITHER OF THE TWO LARGEST SOURCES IS BROKER RESEARCH.** Despite `GS_` filenames, both GS conference files are
> **Felipe's own compiled notes** from company-management sessions at Goldman Sachs' Communacopia + Technology 2026.
> **No rating, no price target and no house estimate exists in either document**, and none was created. Same failure
> mode as the nine BBG fireside transcripts corrected on 2026-09-09 — from the same conference.

> 🔁 **THREE OF THE SIX SOURCES WERE ALREADY IN THE WIKI.** The Semtech call was ingested by the 21:00 `/wiki-ingest`;
> the SemiAnalysis 4-hi article was ingested 09-13 via the equity-calls corpus; and the GS broadcast sessions were
> ingested 09-09 as Bloomberg transcripts. For **TSM, ASML, AMAT and GOOG the overlap is total and nothing was
> re-inserted** — a second compile of a session already held as a primary is not corroboration, and treating it as one
> would manufacture false weight of evidence behind single-meeting numbers. Those four pages carry the check as an
> explicit negative result.

> 📚 **ONE SOURCE IS TEN MONTHS OLD AND IS NOT FLOW.** `INTERNET_20251117_2110.pdf` (MS · Feather/Nowak/Gutman,
> *"Agentic Shoppers Are Coming…"*) is dated **2025-11-17**. Ingested at its real date as the **origin** of the
> agentic-commerce framework the wiki already debates. It **supersedes nothing**, moved nothing into any Changelog, and
> **contributes no quantitative mark to this reconciliation**. Its $192 SHOP PT is the same $192 MS still carried on
> 2026-07-19; the intervening path is not on disk and was not inferred.

**Baselines used.** (1) Prior wiki comments — on disk. (2) Capstone house models — `_data/house.json`, `asof
2026-09-14`, **8 names (AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM)**. Of tonight's names only **AVGO, GOOG, NVDA,
TSM, LITE, COHR and META** have a house model; **ADVANTEST, TER, SNDK, ASML, AMAT, MSFT, CRWV, NBIS, SNOW, CRM, NOW,
BKNG, PANW, CRWD, OKTA, NET, AKAM, FSLY, DDOG, ESTC, CSCO, SMTC, MRVL, OPENAI and ANTHROPIC reconcile on two
baselines.** (3) **BBG consensus — `_data/estimates.json`, `asof 2026-09-14`, 107 names.**

> ✅ **BBG is NOT marked PENDING.** The Terminal was logged out at 23:27 (`blpapi: could not start session`, the
> expected 23:00 state), but the on-disk snapshot is **same-day** and was itself verified this morning by
> `/wiki-consensus`, which caught and re-fetched a phantom same-day vintage. **Orphan-ticker audit run in both
> directions: `set(companies) − set(TICKERS)` and the reverse are both empty (107 = 107).** No `px`/`pt` nulls.

> ⚠️ **PERIOD-BASIS RULE APPLIED THROUGHOUT.** For off-calendar fiscal years the **1FY/2FY/3FY annual lines override
> the CY blocks**. On AVGO the wedge is large and one-directional — the CY sum runs **+16.8% above** the annual line in
> FY1 and **+11.8%** in FY2. Using the CY block would have flattered every comparison below by roughly a seventh.

---

## DIVERGES — the alpha

### ① AVGO — the house model sits ABOVE the company's own AI revenue path, on both years

Management reiterated **~$115bn of AI revenue in FY2027 and ~$230bn in FY2028**, explicitly framed as *conservative and
supply-constrained* (GS Communacopia 2026 — Hock Tan broadcast, 2026-09-08).

| AI semis revenue | FY2027 | FY2028 |
|---|--:|--:|
| **Management (this source)** | ~$115bn | ~$230bn |
| **Capstone house model** | **$132bn** | **$251bn** |
| **House vs management** | **+14.8%** | **+9.1%** |

And the house total-revenue line sits above BBG on the same years:

| Total revenue | FY2027 (2FY) | FY2028 (3FY) |
|---|--:|--:|
| **BBG consensus (annual lines)** | $173.96bn | $274.82bn |
| **Capstone house model** | **$190bn** | **$315bn** |
| **House vs consensus** | **+9.2%** | **+14.6%** |
| House EPS vs BBG EPS | $21.07 vs $19.20 (**+9.7%**) | $35.96 vs $30.65 (**+17.3%**) |

➤ **The house is above the company's own guide on the AI line and above consensus on the total. That is a real position,
but the first thing to check is staleness, not conviction:** the model is `Modelo Avgo pós 2Q26.xlsx`, dated
**2026-06-10** — it predates the **September 2 earnings call**. A model built three months and one print ago being 9-15%
above is as likely to be an un-refreshed file as a view. ⚠️ **Action: re-cut the AVGO model against the Sept 2 print
before this is quoted as a divergence.** Until then it is a maintenance flag, not an edge.

➤ **The genuinely checkable claim in management's own numbers:** $230bn of AI revenue against a consensus FY28 total of
$274.8bn implies **AI is ~84% of ALL Broadcom revenue by FY2028** — the entire infrastructure-software franchise
included. Whatever one thinks of the AI line, consensus's total must rise or its non-AI line must be near zero. Those
are the only two ways the arithmetic closes.

⚠️ **Not a raise.** The note itself states this *"confirms the existing thesis but is not another upward revision versus
the September 2 earnings call."* Logged as confirmatory, with the incremental content being the **anatomy of "supply
constrained"**: 2027 wafers, memory and substrates largely locked; the binding constraint is whether customer sites have
power, buildings, permits, transformers and turbines on time — *"a site required in 2028 generally needs to begin
construction now."*

### ② SNDK — the FY29 gap is UNCHANGED after 18 days, and management just made it harder to defend

| SanDisk, BBG annual lines | FY27 (1FY) | FY28 (2FY) | FY29 (3FY) |
|---|--:|--:|--:|
| Revenue | $48,826m | $58,589m | **$52,671m** |
| y/y | — | +20.0% | **−10.1%** |
| EPS | $212.51 | $260.70 | $211.10 (**−19.0%**) |

➤ **This is the same open divergence first written up on 2026-08-27, and consensus has not moved a dollar:** the FY29
line is **$52,671m then and $52,671m now** — byte-identical 18 days later. Management guided **mid-to-high-teens revenue
growth every year FY28-30** (Investor Day, 2026-08-13); at +16% FY29 would be ~$67,963m. **The gap is ~$15.3bn, ~23%.**

➤ **Tonight's small group tightens it further rather than resolving it:** management described long-term agreements
carrying **~80% gross-margin floors on roughly two-thirds of FY28 supply**, backed by escrowed guarantees, with data
centre now more than half the NAND TAM — and the fab characterised as a fixed-cost machine (**~75% fixed cost, ~500,000
wafers/month, ~$10bn invested**). **A book that is two-thirds pre-sold at an 80% gross-margin floor is difficult to
reconcile with a −10% revenue year and a −19% EPS year immediately after it.** Either consensus is modelling a
post-contract cliff it has not published, or the FY29 line is stale.

⚠️ **Do not treat the 08-27 flag as re-confirmed by tonight's source in the strong sense** — the escrow and floor detail
was already on the page from the 09-05 print, the 09-09 GS/Bloomberg primary and the 09-11 BTG block. What is new is
only the fixed-cost decomposition. **The divergence stands on the consensus line's failure to move, not on new evidence.**

### ③ Cybersecurity — the beneficiary ladder is INVERSELY ranked against consensus implied upside

FundaAI ranks the beneficiaries *"by the strength of the benefit case"*. Placing each rung against the BBG consensus PT
on the same 2026-09-14 snapshot:

| FundaAI rung | Name | Spot | Consensus PT | Implied | Analysts |
|---|---|--:|--:|--:|--:|
| **1 — security platforms** | PANW | $374.04 | $400.59 | **+7.1%** | 60 |
| **1 — security platforms** | CRWD | $237.82 | $238.58 | **+0.3%** | 56 |
| **2 — identity** | OKTA | $185.18 | $182.43 | **−1.5%** | 47 |
| 3 — app/API security | NET | $325.73 | $342.13 | +5.0% | 37 |
| 3 — app/API security | AKAM | $105.41 | $155.27 | **+47.3%** | 26 |
| 3 — app/API security | FSLY | $24.34 | $27.00 | +10.9% | 13 |
| **6 — observability/data (weakest)** | DDOG | $229.76 | $289.27 | **+25.9%** | 50 |
| **6 — observability/data (weakest)** | ESTC | $84.37 | $109.71 | **+30.0%** | 29 |
| **6 — observability/data (weakest)** | CSCO | $110.27 | $140.43 | **+27.4%** | 30 |

➤ **The note's three strongest-benefit names carry an average implied upside of ~+2%, and its weakest rung carries
~+28%.** The ranking and the Street's own price targets point in opposite directions almost monotonically. That is the
finding: **if FundaAI's ladder is right, the expression is not the top rung — it is already priced.** The tradeable
version of this thesis sits at rung 3 (AKAM at +47.3%, though on only 26 analysts) and rung 6, where the AI-security
demand case is *weakest* but the consensus PT has the most room.

⚠️ **Two guards on this table.** (1) Implied upside to a consensus PT is a measure of **positioning and Street
optimism**, not of value — a name can be "fully priced" and still compound. (2) FundaAI is **independent research with
no rating, no price target and no house model**; it does not itself claim any of these are buys, so this is a comparison
between a qualitative benefit ranking and a quantitative price mark, not between two price views.

➤ **The one place the note and the tape agree:** CRWD's own reported **net new ARR of $333m in FY27Q2** and the FY
net-new-ARR growth guidance midpoint raised to **34%** — both of which were **already on the page** (Q2 FY27 block; MS ·
Wigg, 08-26). FundaAI cites them as its evidence; the wiki already held them. No new mark.

### ④ The HBM de-spec chain now has vendors on BOTH sides, and one supplier has broken ranks

The wiki's de-spec read-through (ONTO cutting 2027 advanced-packaging growth to ~50% from ~60%; BESI 2027/28E
hybrid-bonding shipments cut to 115/190) rests on stack-height downticks being a **content negative**. Three of tonight's
sources push back, each in its own line:

- **TER (Communacopia small group, 09-13):** *"lower HBM stack heights can be POSITIVE for tester TAM because the same
  DRAM wafer pool creates MORE HBM stacks requiring performance test"*, and *"2027 HBM is expected to grow rather than
  enter a digestion phase."* **For test the sign inverts — test scales with the number of stacks, not the height of one.**
- **AMAT (same week):** hybrid-bonding adoption is driven by **IO density rather than stack height**.
- **SemiAnalysis (09-13, written article):** models a **~10% $/GB premium on 4-hi versus 8-hi**, which amortises the base
  die against higher packaging yields and makes 4-hi the **higher-margin** product for the supplier.

➤ **And the supplier split is now named for the first time anywhere in the corpus:** *"only **Micron** is complying and
testing it for at least 2 clients. However, **Samsung and SK Hynix have pushed back** on shipping 4-hi and are not
willing to do so yet."* ➤ **That inverts the reflexive reading that shorter stacks are a supplier haircut — the one
supplier leaning in is the one with the least HBM share to defend.** ⚠️ Supply-chain intelligence from an independent
source, unconfirmed by any of the three companies; no estimate moves on it.

⚠️ **All four items are assertions by interested parties or unverified channel work.** None is adopted into an estimate.
They are logged as a **falsifiable counter-argument** to a chain the wiki has been building since 09-08 — the falsifier
is the 2027 HBM stack-count series and the next third-party advanced-packaging shipment table.

### ⑤ ADVANTEST — a price mark this page has never carried, and the third vendor in one week to put price on the table

Management put **tester ASP at +10-15% per year** and shortened the **ASIC-versus-GPU test-demand crossover from 2-3
years to roughly one year**, with the 10k-tester capacity target pulled forward (GS Communacopia 2026 — Advantest
meeting, 2026-09-13). ➤ **This is the first pricing figure ever logged on the ADVANTEST page**, and it lands in the same
week as ASML's one-time 5-10% structural EUV price step-up and Applied's *"value-based pricing expanding across new and
existing products"* — **three semicap vendors putting price on the table within seven days, Advantest at the largest
annual rate of the three.** The prior capacity-ramp timing mark was superseded and moved to that page's Changelog.

⚠️ **Not adopted:** management's *"revenue growth accelerating toward roughly 40%"*. The source gives no period and no
basis (FY vs CY, total vs Test System), and **it is indistinguishable from the BBG consensus already in that page's own
snapshot, which carries CY27E at +40.3% y/y.** Quoting it as management colour would have double-counted consensus.

---

## CONFIRMS — no action

| Name | New datapoint | Baseline | Verdict |
|---|---|---|---|
| **SMTC** | FQ3 guide: revenue $410m ±$5m · GM 58.3% · EPS $1.05 ±$0.03 | **BBG consensus $410.6m · 58.17% · $1.059** | ✅ **The Street has simply taken the guide** — within 0.2% on revenue, 13bps on GM, 0.9% on EPS. Consensus PT $206.13 vs spot $151.20 (**+36.3%**), 16 buy / 1 hold / 0 sell. |
| **AVGO** | ~$115bn FY27 AI revenue | Sept 2 earnings call | ✅ Reiteration, not a raise — and it **resolves the 09-09 ASR defect** where the Bloomberg initial draft rendered the guide as *"$115 million"*. |
| **OPENAI** | >$40bn annualised revenue, enterprise +32% MoM | Already on page — CFO Friar, GS fireside 09-08 | ✅ No thesis drift required. Net-new is only the arithmetic beneath it (~$3.3bn/month; ~$7bn annualised added in one month). |
| **CRWD** | $333m net new ARR FY27Q2; FY NNARR growth midpoint 34% | Already on page — Q2 FY27 print; MS · Wigg 08-26 | ✅ FundaAI cites the wiki's own numbers back to it. |
| **BKNG** | LLM traffic well below 1%; CS cost per booking −10%+ | Already on page — Steenbergen fireside 09-09 | ✅ |
| **TSM / ASML / AMAT / GOOG** | Entire conference sections | Already on page — 09-09/09-10 primaries | ✅ **Checked line by line, nothing re-inserted.** Logged as deliberate negative results. |

---

## Open items carried forward

1. **AVGO house model is dated 2026-06-10 and predates the Sept 2 print.** Re-cut before the +9-15% gap above consensus
   is quoted as a view. → `/wiki-consensus` or a model refresh.
2. **SNDK FY29 consensus ($52,671m) has not moved since 2026-08-27** despite the Investor Day and two management
   sessions. **~23% below management's own guided growth.** Highest-conviction open divergence on the wiki.
3. **MSFT Jalapeño IP conflict** — rights to 2032 *and* in-window development available *in perpetuity* (09-14 notes)
   versus *"We give back the IP come 2032"* (09-09 transcript). Both carried; unresolved. **This is the terminal value of
   Microsoft's second silicon leg — worth an IR question.**
4. **OPENAI FrontierMath tier** — Tier 4 (09-14) vs Tier 1 (09-04). Different difficulty bands; both dated, neither merged.
5. **META lease commitments** — *"reportedly ~$600bn"* (09-14) vs **$347bn of uncommenced leases** (09-11). Different
   scope, one of them unsourced. Reconcile at the next 10-Q.
6. **ANTHROPIC "$60-70bn" valuation in the 09-13 compile REJECTED** — the page carries a **$965bn** Series H. Off by an
   order of magnitude; logged as a source-quality flag against that compile, not as a datapoint.
7. **AVGO's second 09-09 ASR defect is still open** — *"big five"* versus *"five gigawatts"* on the Anthropic ramp. No
   source tonight resolves it; it has not been guessed.
8. **PANW *"Instinct"* garble still unresolved** (the other three PANW/CRWD garbles were closed tonight).
9. **SHOP.md and BKNG.md carry rows misfiled into ARCHIVED intra-quarter windows** by earlier runs (SHOP: 09-04, 09-09,
   two 09-14; BKNG: three 09-09 and the 09-14 Redburn row — both windows closed 2026-08-04/05). Not introduced tonight,
   not fixed tonight. → `/wiki-lint`.

**No BBG column is PENDING anywhere in this report.**
