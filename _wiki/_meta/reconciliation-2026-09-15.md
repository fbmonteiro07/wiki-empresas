# Reconciliation — 2026-09-15 (/run-inbox, 23:00 window, 5 sources)

_Bernstein's ASML SDC meeting note, Bernstein's Late-Q3'26 AWS web-metrics update, a Barclays FICC framework
special report, and two stale UBS cybersecurity notes swept off the P: backlog._

> ✅ **BLOOMBERG WAS LIVE TONIGHT — NO PENDING COLUMN.** Unusually for the 23:00 window the Terminal was logged in,
> so every consensus mark below is a **live `bdp` pull dated 2026-09-15**, taken with `BEST_FPERIOD_OVERRIDE` on the
> **annual 1FY/2FY/3FY lines** — never the CY block, which mislabels off-calendar fiscal years and embeds pre-print
> consensus for quarters already reported. EBIT is used for every growth comparison where both sides publish it.

> 🔁 **THREE OF TONIGHT'S FIVE SOURCES WERE ALREADY PARTLY IN THE WIKI.** Both Bernstein notes had already reached
> the pages via **desk relays** at the 21:00 `/wiki-ingest`. The primaries were ingested for net-new content only —
> and, as set out in DIVERGES #1, **the relay of the AWS note had corrupted the mechanism**, which is the single most
> consequential finding of this run.

> 🚫 **ONE SOURCE PATCHED NO COMPANY PAGE BY DESIGN.** The Barclays note is a **Special Report** that states on its
> own cover that it is *"not an equity or a debt research report under U.S. FINRA Rules 2241-2242"*, written by a
> member of the **FICC** research department who *"is not an equity or debt research analyst."* It carries **no
> rating, no price target, no estimate and no proprietary forecast** — every company reference in it is a recitation
> of already-public fact. It contributes **no quantitative mark to this reconciliation** and was routed to themes only.

> 🗄️ **TWO SOURCES ARE STALE AND CONTRIBUTE NO CURRENT MARK.** `ued35508` (UBS, **2026-01-13**, 8 months) and
> `ued45672` (UBS, **2026-06-09**, 3 months) were ingested at their real dates as a **historical baseline** on the
> `ai-cybersecurity` theme. **No rating, PT or estimate on any live page was updated from either**, and no
> intra-quarter row was written. Their January PT table is carried as an explicitly dated snapshot. Same handling as
> the 2026-03-20 Morgan Stanley cyber note on a prior run.

**Baselines used.** (1) Prior wiki comments — on disk. (2) Capstone house models — `_data/house.json` (`asof
2026-09-15`) covers **8 names (AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM)**; **none of tonight's names is in it**,
so AMZN, DDOG and NET reconcile on **two** baselines. **ASML gets a third** from the live peer model on P:
(`ASML_Peers_SemiCap_v17.xlsx`, `EUV Model` sheet) — see CONFIRMS #1 and DIVERGES #3. ANTHROPIC and OPENAI are
private: **prior wiki comments only, no consensus invented.** (3) **BBG consensus — live `bdp`, 2026-09-15.**

---

## The one-line summary

**Bernstein is at or above consensus on essentially every earnings line it published tonight, and below consensus on
three of its four price targets.** The entire divergence sits in the **multiple**, not the estimates — and it runs in
opposite directions across two desks of the same firm. That pattern, not any single number, is the alpha in this run.

| Name | Bernstein est. vs BBG | Bernstein PT vs BBG PT | Read |
|---|---|---|---|
| **ASML** | in line (+0.1% to +2.5%) | **+22.8%** | Pays **more** for the same numbers |
| **AMZN** | **FY27 EBIT +16.2% · FY28 EBIT +27.1%** | **−3.0%** | Pays **less** for much better numbers |
| **DDOG** | FY26 EPS +6.7% · FY27 EPS +10.2% | **−18.1%** | Pays less for better numbers |
| **NET** | FY26 EPS +3.0% · FY27 EPS **+15.9%** | **−52.1%** | Pays far less for better numbers |

---

## DIVERGES (the alpha)

### 1. 🔴🔴🔴 The relay that reached the wiki at 21:00 carried a mechanism that is **not in the primary** — and it pointed the opposite way

| | |
|---|---|
| **Claim in the wiki at 21:00** | The Q4 AWS deceleration is AMZN *"lighting up more capacity for OPENAI"* — a benign capacity-**mix** story (Bernstein tech daily · Tyler Seidman, specialist **sales**, 2026-09-15) |
| **The primary actually says** | The signal is **trailing SSO web-metric engagement vs 2025 QoQ levels**, persisting from May **through early September** and **widening in the first two weeks of September** (partly a later Labor Day) — a **soft-core demand** read (Bernstein Research · Mark Shmulik, 2026-09-15) |
| **Why it matters** | The two have **opposite implications for the durability of the AWS reacceleration.** A mix story is neutral-to-bullish; a core-consumption story is the bear case. The relay's clause appears **nowhere** in Shmulik's note. |
| **Action taken** | Relay rows kept as the record of what the desk said; the **primary's mechanism now carries the signal tables** on AMZN, OPENAI and DDOG, flagged ⚠️⚠️ in three places. The relay's *"low-40% AWS growth"* bogie was withdrawn as absent from the primary. |

Two further relay defects corrected the same way: the relay labelled **both** OpenAI growth figures as *"observed
third-party consumption (telemetry/observability spend), NOT revenue, NOT ARR"* — **the primary says the opposite**;
and it asserted Bernstein has *"no rating, no price target, no house model on DDOG"* — **it has Market-Perform,
PT $237.** Both retired to the respective Changelogs.

➤ **This is the third run in which a desk relay reached the wiki before the primary and distorted it.** The standing
rule holds: **the primary wins, and the relay's value is the Changelog entry recording what the desk was telling
clients.**

### 2. 🔴🔴🔴 AMZN — Bernstein is **+16% / +27% above consensus on FY27 / FY28 EBIT** and still carries a PT **below** consensus

| Metric | Bernstein (2026-09-15) | BBG consensus (live) | Δ |
|---|--:|--:|--:|
| PT | $320.00 | $329.82 | **−3.0%** |
| FY26E revenue | $836,601m | $828,783m | +0.9% |
| FY27E revenue | $969,103m | $949,660m | +2.0% |
| FY28E revenue | $1,121,480m | $1,092,285m | +2.7% |
| FY26E **EBIT** | $106,482m | $110,295m | −3.5% |
| **FY27E EBIT** | **$163,504m** | **$140,733m** | **+16.2%** |
| **FY28E EBIT** | **$227,830m** | **$179,193m** | **+27.1%** |

Spot $248.42 → Bernstein's PT implies **+28.8%**, consensus **+32.8%**.

➤ **The tension is internal to Bernstein and it is large.** On revenue they are ~1-3% above consensus; on **out-year
EBIT they are 16-27% above** — i.e. they model materially more operating leverage than the Street — yet their target
price sits *below* the consensus target. Either the PT is stale relative to their own model (the note explicitly
says *"no change to models, price targets, or recommendations"*, so it was not revisited tonight), or they are
applying a visibly lower exit multiple than the Street. **This is the cleanest actionable question in tonight's run:
if their FY28 EBIT is right, the $320 is the constraint, not the earnings.**

> ⚠️ **Do not use the EPS line for this comparison.** Bernstein FY26E GAAP EPS $12.65 vs BBG $14.545 looks like a
> −13.0% gap, but Bernstein's is **GAAP including a one-off**: FY26 carries 2Q26 *"Other Expenses (Benefits)"* of
> **−$35,186m**, which is why their FY27 EPS *falls* −4% ($12.13) on far **higher** EBIT. The EPS series is not
> comparable across the two bases. **EBIT is.**

### 3. 🔴🔴 ASML — the house EUV model takes the **110 as the number**, which is exactly what tonight's note says it is not

The Capstone peer model (`ASML_Peers_SemiCap_v17.xlsx`, `EUV Model` sheet — calibrated, 2024/2025 actuals match)
carries Low-NA EUV shipments of **65 (2026) · 85 (2027) · 110 (2028) · 115 (2029)** — ASML's communicated ladder,
with only **+4.5% above the 110 in 2029** and **no above-110 upside modelled in 2028 at all**.

Tonight's note is a direct challenge to that: *"The EUV shipment numbers are not supply caps… Capacity is therefore
not physically capped at these levels,"* with Bernstein's read that if demand proves durable ASML **could expand
beyond 110, particularly in 2028** (and JPM's CFO visit on 09-11 adding that management is *"looking into whether
they can do more than 110 EUV tools in '28"*).

➤ **Sizing the gap on the house model's own ASP:** 2028 Low-NA ASP is **€271.95m**, so **each tool above 110 is
≈€272m of revenue** — roughly **+0.8% of 2028 EUV revenue per tool** against the model's €33.5bn 2028 EUV line.
Ten extra tools would be **≈+€2.7bn, or +8.1%**. The house model is not wrong to use the communicated number; it is
simply **carrying zero optionality on the exact variable two houses now say is open.**

### 4. 🔴🔴 ASML — Bernstein's estimates are consensus, but its PT is **+22.8% above** consensus

| Metric (EUR) | Bernstein | BBG consensus | Δ |
|---|--:|--:|--:|
| PT | 2,500.00 | 2,035.21 | **+22.8%** |
| FY26E EPS | 38.91 | 37.96 | +2.5% |
| FY27E EPS | 53.56 | 52.44 | +2.1% |
| FY26E EBIT | 17,737 | 17,522 | +1.2% |
| **FY27E EBIT** | **24,280** | **24,265** | **+0.1%** |

Spot €1,378.80 → Bernstein's PT implies **+81.3%**, consensus **+47.6%**.

➤ **On FY27 EBIT the two are within 0.1% of each other.** The entire €465 PT gap is the **multiple** — Bernstein's
stated method is **40x applied to Q5-8 EPS**. So the ASML bull case, as this house builds it, is not an earnings
call at all; it is a re-rating call, and it is falsifiable on the multiple alone.

### 5. 🔴🔴 NET — a **Market-Perform whose PT implies ≈−50%**, while the same analyst's estimates sit **above the company's own guide**

| | Bernstein | Reference | Δ |
|---|--:|--:|--:|
| PT | $164.00 | BBG consensus PT $342.13 | **−52.1%** |
| PT vs spot ($327.23) | — | — | **≈−50%** |
| FY26E EPS | $1.32 | BBG $1.282 | +3.0% |
| **FY27E EPS** | **$1.98** | BBG $1.709 | **+15.9%** |

➤ **The estimates and the target contradict each other, and the estimates are the more testable half.** Bernstein is
above consensus on both years — and, per the page work, **above the top of the company's own raised FY26 guide**.
A Market-Perform implying −50% is also inconsistent with Bernstein's own published rating definition (±15pp vs
index). This reads as a **maintained-but-stale target**, and it is carried on the page as the valuation bear anchor,
**not as a short signal.** The note itself changed nothing ("no change to models, price targets, or recommendations").

➤ **The testable claim is separate and lands in Q4:** consumption names with limited AI exposure — NET and TWLO are
named — should see *"a more pronounced headwind to revenue growth during Q4"* because they lack the AI offset that
cushions AWS and Datadog. **That is a clean, dated, falsifiable divergence against this page's agentic-consumption
bull.** Both stand, dated; Q4 resolves it.

### 6. 🔴 DDOG — above consensus on EPS in both years, 18% below on PT

| Metric | Bernstein | BBG consensus | Δ |
|---|--:|--:|--:|
| PT | $237.00 | $289.27 | **−18.1%** |
| FY26E EPS | $2.70 | $2.53 | +6.7% |
| FY27E EPS | $3.45 | $3.13 | +10.2% |

Spot $230.27 → Bernstein's PT implies **+2.9%** (consistent with the Market-Perform), consensus **+25.6%**.

➤ Same shape as NET and AMZN: **an estimate bull and a multiple bear.** Method is the average of a DCF (11% WACC,
3% terminal) and 16x P/Sales. The **AI-offset argument is un-decomposed** — Bernstein asserts OpenAI and Anthropic
are Datadog's two largest AI-native customers and infers broader token-consumption strength, but the note contains
**no customer-level revenue decomposition anywhere**. Logged as contested, not adopted.

### 7. ⚠️ ASML — a vintage/basis conflict on "current" throughput, flagged and **not** resolved

Bernstein calls **~330 wph** the throughput of *"current LNA systems"*. ASML IR's own ladder **six days earlier**
(09-09 Capstone transcript) puts current at **220-260 wph**, with 300 wph (G model) *"towards the end of the
decade"*, and this wiki dates 330 wph (NXE:4200H) to **post-2030**. **Both cannot be "current."** Nothing was
superseded; the conflict is logged on the ASML and semicap-wfe pages.

---

## CONFIRMS (no action)

### 1. ✅✅ ASML's brand-new "memory ≈50% of future EUV demand" lands on **exactly** the house model's own number

Tonight's note is the first memory-share-of-EUV mark anywhere in this wiki: *"memory could account for roughly 50%
of future EUV demand and potentially maintain that share."* The Capstone peer model, built independently, carries
DRAM at **50.0% of EUV demand in 2028** and **51.2% in 2029** (rising from 37.7% in 2026 and 41.0% in 2027).

➤ **An independent house model and the vendor's own IR converge on the same number for the same year.** Note the
model has **zero NAND EUV**, so house "DRAM" and Bernstein "memory" are the same quantity here — the bases are
comparable. This is the strongest confirm of the run and it materially de-risks the DRAM-led WFE thesis the
`semicap-wfe` page has been building.

### 2. ✅ ASML order-book tightness — the house model independently shows 2027, not 2028, as the binding year

The model's supply-minus-demand line runs **−1.5 (2026) · −14 (2027) · +6 (2028) · +6 (2029)** tools, i.e. a
**14-unit shortfall in 2027** and slack in 2028. Bernstein's IR meeting says **2026 revenue is effectively covered,
2027 EUV production is largely booked and DUV close to fully allocated**, with 2028 orders already in hand.

➤ **Two independent constructions agree that 2027 is the tight year** — which is a useful corrective to a market
debate (and tonight's headline) fixated on whether 110 caps **2028**. Vendor self-assessment not adopted; logged as
falsifiable.

### 3. ✅ Anthropic's ARR ladder gets an independent sell-side house on the record

Bernstein: ARR **over $65B in July 2026, up from $47B in May and only $9B at end-2025**. The wiki already carried
**>$47B May-26 → >$60B 3Q26 → $65B+** from Jefferies (09-02), SemiAnalysis (08-21) and the relay — **and the $9B
end-2025 base was already on the page.** Nothing new; the additive parts are a **precise July anchor in published
research** rather than a relay, and the whole slope stated by one house in one sentence instead of stitched across
three. Signal held at **⚠ nuance**, not upgraded — the note resolves no basis question.

### 4. ✅ The AWS Q3 read is *not* the bear half, and the page now says so

Bernstein expects **Q3 AWS ex-AI growth to accelerate a further ~50bps** against the **22%** they model, because the
web-metric series runs on a **~1-quarter lead** and Q2 started strong with weakness only from May/June. The risk is
**Q4**, where the headwind could be **up to −100bps worse than the ~150bps already embedded**. This *confirms and
sizes* the "4Q risk" Bernstein first flagged in June — the May signal did not reverse. Their own caveat is carried
verbatim: *"this is alt data with good historic fit, but for a variety of reasons it could stop being predictive."*

### 5. ✅ ASML litho-intensity floor in memory — vendor now agrees with LRCX from the opposite end of the tool chain

ASML *"continues to disagree"* that litho intensity falls on the 6F²→4F² DRAM transition, expecting **more EUV
layers** and migration from DUV multi-patterning to EUV single exposure. LAM already called DRAM de-speccing *"a
red herring"* (09-09). ➤ Two vendors, opposite ends of the chain, same conclusion. Not adopted — both are
interested parties — but the bear case now needs to beat two independent denials.

### 6. ✅ NVDA–Groq framing corroborated

Barclays: December 2025, **non-exclusive licensing plus talent**, Groq independent, GroqCloud uninterrupted —
*"best understood as a licensing and talent arrangement, not an acquisition of Groq."* This **corroborates**
`NVDA.md` and `tokenmaxxing.md`, which both already carry it as a licensing deal. ⚠️ It **contradicts**
`hbm-memory.md:199`, which carries a third-party quote asserting *"Groq was acquired by NVIDIA"* — left unedited
(it is a verbatim quotation and out of tonight's scope), but **flagged for the owner of that page.**

---

## Housekeeping flags raised by this run

1. **The ASML page's house block is stale and no longer traceable.** It cites `ASML_Peers_SemiCap_v16.xlsx`
   (Peer Comp, 2026-06-15); **P: is now on v17, which has no `Peer Comp` sheet at all** — the model was
   restructured. The EPS table on the page cannot be refreshed from the current model as written.
2. **⚠️ `ASML_Peers_SemiCap_v17.xlsx` is internally inconsistent and one of its sheets must not be quoted.** The
   `ASML Rev BU` **top-down exercise** sheet implies 2026E/2027E/2028E revenue of **€48.8bn / €66.3bn / €80.2bn** —
   **11-43% above both Bernstein and consensus** — and its own EUV unit row reads **100 / 86 / 175**, which
   contradicts the calibrated `EUV Model` sheet's **65 / 85 / 110**. Its variance-to-reported row is forced to zero
   for all forward years. **It is scratch work, not a house forecast**, and no number from it is used above.
3. **The house EPS table's currency label looks wrong.** The page prints "Diluted EPS ($)" with 2026E/2027E/2028E of
   **39.63 / 56.85 / 68.74**, which sit within 2-8% of the **EUR** consensus (37.96 / 52.44 / 67.63) and nowhere
   near a USD translation. Almost certainly **EUR mislabelled as USD**. Flagged, not silently changed.
4. **`OPENAI.md` line 532 carried an unbalanced `**` at HEAD** (pre-existing, from an earlier run). Fixed to match
   the convention used by every neighbouring row: bold closes, citation unbolded, then the cell pipe.
5. **PANW "Idira" garble closed.** The 09-15 Capstone-call block asserts *"NO SUCH BRAND EXISTS ANYWHERE IN THIS
   CORPUS."* The June UBS note names **"Palo Alto's Idira"** in Gartner's identity session — three months earlier.
   Does **not** confirm the ~$1.5bn attached on that call.
6. **ASML ~500 wph upgraded from ⚠ ASR-uncertain to corroborated.** The 09-09 IR transcript's *"new high
   productivity platform… 500 an hour"* was suspected to be a speech-recognition garble; Bernstein's written
   **330 → 400-500 wph** bracket confirms it independently. Still **not adopted** as a dated model input.
7. **Wiki-wide gap closed:** before tonight, **no DORA, EU AI Act or confidential-compute/TEE mark existed anywhere
   in the wiki.** The regulatory timeline is genuinely net-new on `secure-sovereign-infrastructure`.
8. **First IEA power mark in the wiki, and it is not comparable to the existing one.** Barclays carries IEA's
   **global** data-centre consumption ~415TWh (2024) → ~945TWh (2030). The nearest existing mark
   (`ai-datacenter-power.md:821`) is Bernstein's **US** ~250 → 500TWh. Different scopes — **never net or chain them.**
