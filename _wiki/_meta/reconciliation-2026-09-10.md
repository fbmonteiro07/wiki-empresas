# Reconciliation — 2026-09-10 (/run-inbox, 20 sources)

_Oracle's FQ1 FY27 print plus three Goldman Communacopia **management** firesides (NVDA/CRWD/PANW), a J.P. Morgan
META upgrade, a Morgan Stanley NVDA cross-asset webcast, and a Morgan Stanley cyber backlog dated back to
2026-01-26. **Four of tonight's primaries are company management, not broker research** — the keyword router
labelled the CrowdStrike fireside "Citi"._

**Baselines used.** (1) Prior wiki comments — on disk. (2) Capstone house models — `_data/house.json`, `asof 2026-09-10`,
**8 names only (AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM)**; ORCL, CRWD, PANW and MSFT have **no house model**,
so those names reconcile on two baselines. (3) **BBG consensus — `_data/estimates.json`, `asof 2026-09-10`, 106 names,
0 carry-overs** (refreshed live earlier today by `/wiki-consensus`). The Terminal was not re-queried at 23:00; the
same-day snapshot is a valid baseline, so the BBG column is **NOT** marked PENDING.

> ⚠️ **THE SNAPSHOT IS PRE-PRINT AND THAT IS THE POINT.** The BBG fetch runs intraday; Oracle reported after the
> close. ORCL `px $152.94` and every ORCL estimate below are the **pre-print** Street. That makes them the correct
> yardstick for tonight's guidance — but they must never be quoted as a post-print mark, and the ORCL consensus
> figures here will be stale the moment the Street revises.

> ⚠️ **FISCAL-PERIOD TRAP AVOIDED — read this before reusing any ORCL number.** Oracle has a **May fiscal year-end**,
> so its `CY2026` block (`rev $76.2bn / EPS $7.32`) is **NOT** FY27 and is not comparable to tonight's guide.
> Reconciling the guide against the CY block would have manufactured a **fake +18.1% revenue beat and a fake +10.7%
> EPS beat**. Every ORCL comparison below uses the **`1FY` annual line**, verified as FY27 (Jun-26 → May-27) by
> triangulation: `1FY rev $89,595m` is **+33.0%** on the FY26 actual of `$67,357m`, matching management's own "+34%"
> characterisation of the ≥$90bn guide. The same applies to the quarterly line — BBG's `1FQ` is **labelled "Q4-26E"
> (a calendar quarter) but IS Oracle's fiscal Q2 FY27**.

---

## DIVERGES — the alpha

### 1. ORCL — the "guidance raise" is worth **+0.5% on revenue and +0.4% on EPS** against a Street that already had it

| FY27 (Jun-26 → May-27) | Management, 2026-09-10 | BBG consensus `1FY`, pre-print | Delta |
|---|--:|--:|--:|
| Total revenue | **"at least $90bn"** (+34% y/y) | $89,595m | **+0.5%** |
| Non-GAAP EPS | **$8.10** | $8.066 | **+0.4%** |
| Capex | **$90–95bn** (mid $92.5bn) | $92,666m | **−0.2%** |

**This is the finding of the run.** Oracle "upgraded" FY27 guidance to a number the Street had already fully
modelled — on all three lines, to within half a percent. The headline is a formalisation of consensus, not an
upgrade to it. Anyone trading the words "raising our guidance" is trading ~40bp of actual revision.
➤ **The corollary matters more than the datapoint:** if the stock moves materially on this, the move is
sentiment/positioning (ORCL went into the print at `$152.94`, ~5.9% below the `$162.52` Barclays referenced on
09-09, and sits on MS's tax-loss-harvesting basket), **not** estimate revision. Watch whether the Street's FY28
line moves — that is where the +$26bn of new RPO, explicitly said not to touch revenue "until fiscal 28 or beyond",
actually lands.

### 2. ORCL — management's RPO conversion pace contests the standing BofA bear, but the bases differ

The page carries BofA (07-20): **RPO conversion only 12% over the next 12 months, vs MSFT 25%**. Tonight:
*"We now expect around **half of our RPO to convert into sales over the next 36 months**."*
⚠️ **Not directly comparable and must not be netted** — one is a 12-month conversion rate, the other a 36-month
cumulative share. But 12%/yr sustained implies ~36% over three years against management's ~50%, i.e. management is
guiding conversion **materially faster than the bear case assumes**. The gap is the debate; the units are the trap.
⚠️ No absolute RPO total was given, so the page's `$638bn` (Q4 FY26) mark stands — the `+$26bn q/q` was **not**
chained into a new total.

### 3. NVDA — the Capstone house model is ~7pp below **both** management and consensus on FY28 growth

| FY28 / CY27 | Capstone house | BBG consensus `2FY` | Delta |
|---|--:|--:|--:|
| Revenue | $661bn | $693.7bn | **house −4.7%** |
| Growth y/y | **+62%** | **+69.3%** | **−7.3pp** |
| EPS | $15.44 | $15.856 | house −2.6% |

Jensen, 2026-09-10: *"We could grow 70% year-over-year, and we are confident about that."* Consensus already carries
**+69.3%**. **The house does not.** That is a **$32.7bn revenue bridge** to name — and it is the house sitting below
both the sell-side and the company, on the one number management chose to reaffirm in public. Either the house has a
deliberate supply-constraint haircut it should state, or the model needs updating.

### 4. META — JPM's PT went up 28% on **zero** change to earnings

JPM upgraded Neutral → Overweight and took the Dec-27 PT **$640 → $820**. Both targets sit on the **same 2028E GAAP
EPS of $35.44**; only the multiple moved, **18x → ~23x**. JPM simultaneously *raised* spend (2027 capex $243bn, +70%;
2028 $284bn) and held FCF at **−$65bn to −$70bn a year**, and states it is *"not yet building in new AI product
monetization."*
➤ **So the upgrade is a re-rate, not a revision.** Placed against the other two baselines it is nonetheless the
most aggressive mark on the page:

| Adj. EPS | JPM | BBG consensus | vs cons | Capstone house | vs house |
|---|--:|--:|--:|--:|--:|
| 2026E | $36.46 | $34.534 | **+5.6%** | $32.72 | **+11.4%** |
| 2027E | $41.08 | $37.845 | **+8.5%** | $38.24 | **+7.4%** |

PT $820 vs BBG consensus PT $749.71 = **+9.4%**; vs spot $644.38 = **+27.3%**. Street high $1,000, low $580 — so $820
is aggressive but not a Street high. **The house is the low man on 2026 (−5.3% vs consensus) while being *above*
consensus on revenue** ($257bn vs $254.1bn), i.e. the house is carrying a materially heavier 2026 margin/spend
assumption than the Street. That is the real house-vs-Street gap on META, and tonight's upgrade widens it.

### 5. PANW — Morgan Stanley calls it a **Top Pick** with a price target **below** the Street median

MS PT **$387** vs BBG consensus PT **$400.59** = **−3.4%** (Street high $475; spot $338.49 ⇒ MS +14.3% vs consensus
+18.3%). A "Top Pick" designation and a below-median target is a rating-vs-PT tension worth naming.
➤ It compounds a second inversion the page now carries: **MS's own FY27 model is BELOW consensus** (revenue +18.2%
vs +20.9%; NGS ARR +20.5% vs +22.9%) while the note argues the FY27 *guide* will print *above* it. Not internally
contradictory — but the bull case is explicitly "guide beats MS's own model", which is a lower bar than "guide beats
the Street".

### 6. NVDA — Morgan Stanley is Overweight on **below-consensus** numbers and a **below-consensus** target

MS CY27e EPS **$15.01** vs BBG `2FY` **$15.856** = **−5.3%**. MS PT **$300** vs BBG consensus PT **$324.61** = **−7.6%**.
So the Overweight does not rest on above-Street estimates at all — it rests on multiple plus un-modelled optionality,
which MS says outright: revenue-sharing is *"upside not yet in numbers"* (+9.42% FY29 EPS at a $12/hr market GPU price,
+15.14% at $18/hr, on 5GW). ➤ **Read the OW as an options position on rev-share, not as an earnings call.**

### 7. NVDA — the same house is Overweight the equity and **sidelined on the credit**, on one webcast

Joseph Moore: **Overweight, PT $300**. Lindsay Tyler, same deck, same day: **Neutral | Sidelined** — *"the tail remains
too early-stage, opaque, and sizable to step in."* Credit sizes CY28-end all-in exposure at **~$200bn, ~$170bn of it
away from funded debt**: ~$40bn lease/ratings adjustments + ~$65bn residual-value support on the >$500bn partnership
(RVS up to 25%, illustrative tail peaking **~$90bn shortly after CY28-end, ~$70bn tax-affected**) + ~$65bn rev-share
credit support on 5GW. ⚠️ **The ~$65bn rev-share bucket and the +9.42%/+15.14% EPS upside grid run off the SAME 5GW** —
they are two sides of one assumption. Do not count the upside without the contingent exposure.

---

## CONFIRMS — no action

- **ORCL Q2 FY27 guide is in line.** BBG `1FQ` (labelled "Q4-26E", = fiscal Q2 FY27) consensus EPS **$1.903** sits
  inside the guided **$1.85–$1.93** and near its top; consensus revenue **$21,110m** is consistent with the guided
  **+30–34%**. ⚠️ The EPS range is **reconstructed from an ASR garble** (*"between $1 and $0.85 and 193"*) — the
  reliable management mark is the **+21–25% ex-Ampere** growth range, and this comparison should be re-run against
  the FINAL transcript.
- **ORCL capex is exactly where the Street had it** — guide $90–95bn vs consensus $92,666m. No revision.
- **NVDA's 70% reaffirmation is already in the estimates.** Consensus `2FY` growth is **+69.3%**; Jensen said ~70%.
  Nothing to add — and note the fireside **never touched gross margin**, which the page had flagged as the thing to
  watch at this venue. The 72–73% FY28 settle stands untested.
- **CRWD — Morgan Stanley *is* the consensus, to within 0.4% on every line.** FY01/27 $1.25 vs $1.255 (−0.4%);
  FY01/28 $1.61 vs $1.606 (+0.2%); FY01/29 $2.08 vs $2.074 (+0.3%); PT $238 vs consensus PT $238.58 (**−0.2%**).
  There is no edge here in either direction — the MS ladder ($172 → $227 on 07-21 → $238 on 08-27, held 09-03) has
  simply converged on the Street. Spot $208.86 ⇒ +14.0% to target.
- **GPU residual value — two independent datapoints, same day, same direction.** Oracle: GPUs coming up for renewal
  were *"renewed or resold at a 20% PREMIUM to prior contracts"*, and *"the majority of those GPUs are four years or
  older."* Jensen: *"You can still rent Voltas. Volta is 10 years old… All the Amperes in the world are all rented
  out."* ➤ A customer and the vendor, independently, on the depreciation-schedule bear. This is the strongest
  same-day corroboration in the run and it cuts against aggressive useful-life shortening.
- **Vera Rubin — a customer corroborates the ramp.** Oracle: Rubin systems *"performing better than expected across
  hardware quality, manufacturing yield, and performance"*, first units to customers in Q2. Independent of NVDA's own
  commentary.
- **ORCL's $20bn ATM completed in Q1, in full** — resolving the three-sided sign conflict the page has carried since
  August (DB wanted the update, JPM credit listed a *shift away from* equity funding as a risk to its Overweight,
  the equity side read the same $20bn as dilution overhang). Resolved **as an event, not as an argument**: the
  multi-year funding gap the three houses sized (UBS ~$36bn FY27-30, DB's $40bn FY27 intention vs ~$28.5bn raised,
  BofA's ~$20bn equity + more debt over 3 years) is longer than this issuance and was not addressed. Scored ✗ → ⚠.

---

## Traps carried out of this run

1. **⚠️⚠️ THE 18/25/40 UNIT COLLISION.** Same day, same conference cycle: Morgan Stanley published
   **$18bn / $25bn / $40bn per GIGAWATT** (Hopper/Blackwell/Vera Rubin — NVDA *revenue* per GW) while Jensen said
   **$18,000 / $25,000 / $40,000 per GPU SYSTEM** (ASP). **Identical digits, different metrics.** Jensen additionally
   gave **"$60bn" for a 1GW data centre** (basis ambiguous — he prefixes it "we sell it for") and **"~$50bn revenue per
   gigawatt"** (the *operator's* annual rental flow), while his Australia example — **2GW for 2027 = $80bn** —
   reconciles exactly at **$40bn/GW**. At least three distinct per-GW bases now circulate inside one conversation, and
   MS's **$3/watt** rev-share price floor is a fourth, unrelated animal. **Chaining any of these is barred.**
2. **The ORCL CY-block trap** (see the header box) — would have produced a fake +18.1% revenue beat.
3. **Three of four primaries are non-final transcripts** — ORCL and CRWD are Bloomberg **LIVE**, PANW an **INITIAL
   DRAFT**. Every number above that comes from them is provisional pending the FINAL transcripts, and the ORCL Q2 EPS
   range in particular is a reconstruction.
4. **Chart values refused throughout** — the MS neocloud-capex bar series, the JPM template deck's comps/rank-order
   tables, and the MS "Cybersecurity 101" deck are all image-only or label-mispairing risks. Only prose figures logged.
5. **`$8.5m` NVL72 rack vs `72 × $25,000` (~$1.8m)** — a ~4.7x gap inside one answer, and **"250,000 kilowatts"** for a
   single rack (~250x the ~1MW/rack the wiki carries). Both flagged on NVDA.md, neither resolved nor adopted.

_No house model exists for ORCL, CRWD, PANW or MSFT — those names were reconciled against prior wiki comments and BBG
consensus only. ANTHROPIC and OPENAI are private: read-throughs only, reconciled against prior wiki comments._
