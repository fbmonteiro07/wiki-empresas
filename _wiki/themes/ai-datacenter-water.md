# Theme — AI Data-Center Water & Ultrapure Water

_Wiki · opened 2026-08-25 · cross-company theme · **RADAR STATUS — this theme is opened as a watch item, not as a researched position.** No name here is in Capstone coverage; no transcript is on disk yet. Company index: [../00_INDEX.md](../00_INDEX.md) · themes index: [00_THEMES.md](00_THEMES.md) · sibling: [ai-datacenter-power](ai-datacenter-power.md)._

## What it is / why it matters

The claim is that **water repeats the power trade**: data centres hit a grid constraint and answered it with behind-the-meter generation ([ai-datacenter-power](ai-datacenter-power.md) is that story, ~500 lines of it); the argument here is that they are now hitting a **water and permitting constraint** and will fund private water infrastructure the same way. If true, the trade is a picks-and-shovels re-rating in water equipment/services — and, more usefully for our existing coverage, a **cost-and-schedule line on every advanced fab and every hyperscale campus we already model**.

Two reasons it belongs on the radar rather than in the bin:

1. **The permitting leg is already corroborated on our own pages.** [ai-datacenter-power](ai-datacenter-power.md) ingested the Data Center Watch series on Aug 20 (~$156bn blocked/delayed in 2025, **$130bn in 1Q26 alone**), the Texas audit halt (Aug 14/15), ERCOT auditing **>474 GW** of queued load, states taxing the build (Aug 2), and the Seattle DC moratorium (June 9, in `_briefings/by-ticker/AMZN.md`). Water is one of the two named grievances driving that friction. This theme did not have to import its premise — the wiki already believed it.
2. **The fab leg touches coverage directly.** Ultrapure water (UPW) scope on an advanced fab is claimed at **$50-100mn per project**. That is a real line inside the fab-capex numbers we carry on [semicap-wfe](semicap-wfe.md) and [TSM](../TSM.md), and we have never sized it.

## State of play — what is VERIFIED (web, 2026-08-25)

**Xylem (`XYL`) 2Q26, reported 2026-07-28 — the anchor print.**
- **Applied Water orders +9% organic to $538mn, with data-centre orders up >300% y/y.**
- Management guides **data-centre revenue +~200% in 2026, reaching ~2% of total sales exiting the year.**
- Company-level: revenue **$2,336mn** (+2% reported, +1% organic), adj. EPS **$1.46** (+16% y/y); **total orders +42% y/y to $3.1bn**, backlog **$5.3bn**, book-to-bill well above 1. FY26 guide raised to **~$9.2bn revenue / $5.55-5.70 adj. EPS**.
- ⚠️ **Read the base rate before the growth rate: ~2% of sales exiting 2026.** This is a backlog/narrative re-rating candidate, not an earnings-revision story yet. The bull case is explicitly an analogue to CAT (backlog surged ~3.5x and the stock re-rated *before* revenue arrived) — i.e. it asks you to pay for order momentum. That is a legitimate trade and also exactly the kind that de-rates fastest if orders flatten.

**Ecolab (`ECL`) 2Q26, reported 2026-07-28 — the competitor that is further along, and the reason this theme is bigger than one name.**
- **Global High-Tech scaled from $150mn (2021) to a ~$1.5bn annualised run-rate**, +29% growth — split roughly **$0.5bn legacy / $0.5bn CoolIT / $0.5bn Ovivo**.
- **Ovivo's electronics UPW business acquired for $1.8bn cash** (announced Aug 2025, since closed) — semiconductor UPW, retained brand, HQ near Basel. **This is a direct competitor to the Evoqua/UPW channel in the XYL pitch, bought at a disclosed price.**
- **CoolIT Systems acquired for ~$4.75bn cash**, expected to close 3Q26 — Calgary-based liquid-cooling supplier.
- Management claims the combined offering captures **3-5x more revenue per data centre** vs legacy water-only, and integrated 3D TRASAR into CoolIT units within two weeks of closing.
- ➤ **The read for the XYL pitch: a $1.8bn arm's-length price on a pure-play electronics-UPW asset is a valuation anchor the pitch does not use.** And ECL's "3-5x per DC when you own the cooling loop too" says the money may sit at the water/cooling *interface* rather than in water treatment alone.

**Veralto (`VLTO`) 2Q26, reported 2026-07-29 — third independent confirmation, from a different socket.**
- ChemTreat industrial water growing **double digits** on the data-centre ecosystem (power, mining, semis); **industrial is now ~50% of water-segment sales**, NA-led. Revenue $1.47bn (+7.5% y/y), adj. EPS +19.4%, FY26 adj. EPS guide raised to **$4.35-4.43**.
- **2026-05-18: ChemTreat joined Dow's Coolant Care Network** as a strategic national service provider for AI data-centre cooling, and **Dow's only preferred service provider in Virginia** — adding DOWFROST LC / HD heat-transfer fluids for direct-to-chip and facility loops.
- ➤ **Three separate industrials independently reporting double-digit-to-triple-digit DC water growth in the same fortnight is the strongest form of this evidence.** It is not one management team talking its book.

**The physical/cooling interface — Munters and SPX.**
- **Munters (`MTRS SS`) 2Q26: organic order intake +144%**, driven by DC. Named awards: **SEK 2.1bn** from a US hyperscaler (chilled-water CRAHs, CDUs, chillers; deliveries 4Q26 → 1Q28) and **SEK 2.0bn** from a US colocator (booked in 2Q26, deliveries from early 2027). ⚠️ Margin pressure in Data Center Technologies from supply chain + tariffs.
- **SPX Technologies (`SPXC`): Marley OlympusMAX launched 2026-04-29** — modular dry/adiabatic fluid cooler for data centres, bolt-on adiabatic module, explicitly sold on **"energy and water-use predictability"**. Hybrid dry/wet towers claim **up to 50% less seasonal water** vs conventional wet towers.
- ➤ **SPX is the carrier of the bear case, not the bull case** — see the debate below.

**Permitting (verified, and consistent with what [ai-datacenter-power](ai-datacenter-power.md) already holds).**
- **Arizona: Gov. Hobbs signed a 3-year pause on new DC sales-tax exemptions, 2026-07-01 → 2029-06-30**, in the June budget deal. Preceded by the **Chandler council's 7-0 rejection (Dec 2025)** and the Tucson/Project Blue backlash. Tucson's large-quantity-water-user code bites at **7.48mn gallons/month**.
- 🔴 **THE COUNTER-DATAPOINT THE PITCH OMITS: between June 15 and June 30 2026, the Arizona Commerce Authority received 113 applications** for the exemption ahead of the freeze — roughly matching the prior thirteen years combined (Axios Phoenix, 2026-07-08). **Demand is being tolled, not killed.** That is arguably *more* bullish for a picks-and-shovels water trade than the moratorium headline, and it should be carried alongside it.
- **Pima County staff directed to develop a DC moratorium (AZPM, 2026-08-13)** — the friction is still widening as of two weeks ago.
- **Data Center Watch Q1 2026: ~75 projects / ~$130bn blocked or delayed**, "largest single-quarter concentration on record," matching all of 2025 in three months; **active opposition groups 396 → 833 across 49 states**; **>300 bills** introduced in statehouses in the first six weeks of 2026, described as a structural shift from incentive-focused policy toward regulatory oversight.

## ⚠️ UNVERIFIED — pitch material pending source confirmation

The following came in as an **un-attributed pitch (received 2026-08-25, broker/author NOT yet confirmed)** and is logged here **only** so the claims are on the record with their status. Per the house rule on pasted exhibits, none of it is to be quoted onward or folded into any model until the source is confirmed:

- **GWI**: AI ecosystem needs **~31bn m³** of incremental annual water by 2050 = **$15-31bn annualised spend**; **UPW demand +613% by 2050**.
- **40%** of the world's data centres sit in high or extremely-high water-stress areas.
- Channel sizing: Applied Water **$1-2mn per 25MW DC** (27% CAGR modelled); Evoqua UPW **~$194mn starting base, ~12% CAGR**; WSS ≈ **2/3 of AI-related revenue**, PPA-like long-term contracts, **~$20mn per SMR / >$50mn per full-scale nuclear**; WaterFleet supporting a Texas hyperscaler build; Sensus/Vue — **AMZN partnered with XYL on Mexico City + Monterrey utilities**.
- A **$14bn Goodyear (AZ) development withdrawn**; a **Tucson project's water permit revoked**; **Chandler blocked a 100mn+ gallon/yr request**.
- Valuation framing: *"the market is pricing XYL as a quality industrial growing at 5%."*

📌 **Structural note for whoever picks this up: Evoqua is not a standalone issuer.** Xylem acquired Evoqua in May 2023 (all-stock). "Evoqua" and "WSS" (Water Solutions & Services) in the pitch are **XYL reporting segments** — there is no Evoqua call to pull. Anyone told to "get the Evoqua transcript" should pull XYL.

## Key debates

1. 🔴 **CLOSED-LOOP IS THE BEAR CASE, AND IT IS ALREADY IN OUR CORPUS.** Two sources on disk — **Stratechery, 2026-05-18 ("Data Center Discontent")** and the **JPM DC call, 2026-05-04** — both note modern data centres increasingly run **closed-loop** cooling, which collapses consumptive draw. SPX's own marketing (**up to 50% less seasonal water** on hybrid dry/adiabatic towers) is the vendor confirming it. ➤ **The tension is sharp and unresolved: closed-loop adoption is precisely the industry's *response* to the permitting friction this theme is built on. It can cannibalise the volumetric TAM (the GWI m³ number) while simultaneously *supporting* the equipment/capex TAM — because closed-loop is itself equipment, and adiabatic/dry coolers are a sale.** Any m³-based sizing that does not model closed-loop penetration is measuring the wrong quantity. **This is the first thing to test.**
2. **Is it a TAM story or a share story?** Three companies claim DC water growth; only ECL has bought its way to an end-to-end position (Ovivo + CoolIT). Whether XYL's 300% order growth is the market growing or ECL/VLTO/Munters splitting the same campuses is not answerable from press-release data.
3. **Does the CAT analogue hold?** It requires backlog to convert. At ~2% of sales exiting 2026 the conversion evidence does not exist yet, and the pitch is explicitly asking to pay ahead of it.
4. **BASIS DISCIPLINE — do not mix water units with power units.** Same rule as [800v-dc-power](800v-dc-power.md): facility GW ≠ IT-load GW. Here: **m³/yr of withdrawal ≠ m³/yr of consumption ≠ $ of equipment scope ≠ $/MW of water capex.** The GWI 31bn m³ figure and the "$1-2mn per 25MW" figure are on different bases and must never be multiplied together. See [../_meta/assumptions.md](../_meta/assumptions.md).

## Who's exposed (companies) — and the transcript pull list

**None of these are in Capstone coverage; none have a wiki page or a transcript on disk.** Listed with the call to pull. Convention follows [outros-asia](outros-asia.md): off-coverage names are plain text + listing code, no broken links.

| Priority | Name | Code | Why | Transcript to pull |
|---|---|---|---|---|
| 1 | Xylem | `XYL` | The pitch itself — all four channels (Applied Water, Evoqua/UPW, WSS, Sensus) are XYL segments | **2Q26, 2026-07-28** |
| 1 | Ecolab | `ECL` | Furthest along; Ovivo ($1.8bn) = the UPW comparable, CoolIT ($4.75bn) = the cooling-loop land grab; the 3-5x-per-DC claim | **2Q26, 2026-07-28** |
| 1 | Veralto | `VLTO` | ChemTreat + Dow Coolant Care Network; independent third confirmation from the chemistry/service socket | **2Q26, 2026-07-29** |
| 2 | Munters | `MTRS SS` | +144% organic orders, two named SEK-2bn awards — the hard volume evidence on chilled-water architecture; also the margin warning | **2Q26** |
| 2 | SPX Technologies | `SPXC` | Cooling towers / Marley; **carries the closed-loop bear case** (dry/adiabatic, "water-use predictability") | **2Q26** |
| 2 | Vertiv | [VRT](../VRT.md) | Already covered + in [ai-datacenter-power](ai-datacenter-power.md) / [800v-dc-power](800v-dc-power.md); thermal-management read-through. **We are missing the 2Q26 call — latest on disk is Q1-2026 (2026-04-22)** | **2Q26 — gap in our own coverage** |
| 3 | Kurita Water Industries | `6370 JP` | THE fab-UPW player globally; the direct check on "$50-100mn per advanced fab" and the +613% UPW claim | Latest results briefing |
| 3 | Organo Corp | `6368 JP` | The other Japanese UPW specialist, heavily semiconductor-levered | Latest results briefing |

**Read-through into existing coverage:** [TSM](../TSM.md) and [semicap-wfe](semicap-wfe.md) (UPW scope per fab is an unsized line in fab capex); [ai-datacenter-power](ai-datacenter-power.md) (shared permitting constraint — this page should not duplicate it, only cross-link); [AMZN](../AMZN.md) (named in the pitch's Sensus/Mexico-utilities claim, unverified).

## Suggested next step

Pull the three Tier-1 calls (`XYL`, `ECL`, `VLTO` — all late-July 2026) into `E:\Wiki Felipe empresas\<TICKER>\transcripts\` and read them against **debate #1 (closed-loop)** first. That single question decides whether this is a real theme or a well-packaged extrapolation, and it is answerable from management Q&A rather than from more sell-side sizing.

## Sources

- Xylem 2Q26 (2026-07-28) — earnings call transcript via Investing.com; call highlights via GuruFocus.
- Ecolab 2Q26 (2026-07-28) — earnings call transcript via Investing.com; highlights via GuruFocus. Ovivo acquisition: Ecolab IR release (Aug 2025), Manufacturing Dive. CoolIT: deal terms via PrivSource.
- Veralto 2Q26 (2026-07-29) — earnings call transcript via Investing.com; ChemTreat/Dow Coolant Care Network (2026-05-18).
- Munters 2Q26 — company release + Investing.com slides; order announcements via Cooling Post / TipRanks / PR Newswire.
- SPX Technologies — Marley OlympusMAX launch (2026-04-29), SPX Cooling Tech.
- Arizona: AZ Capitol Times (2026-07-09), Bloomberg Tax, azfamily (2026-06-10), Axios Phoenix (2026-07-08), AZPM Pima County (2026-08-13).
- Data Center Watch Q1 2026 report; NBC News; Newsweek.
- Closed-loop counter-evidence (on disk): Stratechery 2026-05-18 "Data Center Discontent"; JPM DC call 2026-05-04 (`relatórios bons\2026_05_04_dc_call_jpm_4_may_26.html`).
- ⚠️ Un-attributed pitch received 2026-08-25 — **source pending confirmation**, quarantined in its own section above.

## Changelog

- **2026-08-25** — Theme opened on radar status. Trigger: an un-attributed water-as-the-next-BTM pitch built around XYL. Everything checkable in it verified against 2Q26 prints and primary permitting coverage; the pitch's own sizing (GWI m³, per-channel $ figures) quarantined pending source confirmation. Two additions the pitch did not carry: the **113 Arizona applications filed in the two weeks before the freeze** (demand tolled, not killed), and **Ecolab's $1.8bn Ovivo / $4.75bn CoolIT** positioning as the competitive and valuation anchor. Closed-loop cooling logged as debate #1 from corpus material already on disk (Stratechery 2026-05-18, JPM 2026-05-04). No numbers from this page are canon; nothing folded into [../_meta/assumptions.md](../_meta/assumptions.md).
