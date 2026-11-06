# Data-center deployment: US versus rest of world

Research date: 2026-11-06. Scope: annual capacity additions, with forecast vintages preserved. Capacity ready for IT equipment is not proof that chips are installed, serving workloads or drawing their full nameplate power.

## Best directly sourced geographic breakdown — SemiAnalysis

**2027E: US 38.0 GW + rest of world excluding China 13.2 GW = 51.2 GW of annual net IT-capacity additions, excluding China.** This is a forecast, not capacity already deployed. The original chart explicitly defines net additions as the change in year-end operating IT capacity and includes scheduled completions from under-construction and planned buildings.

All table inputs below are **HARD sourced figures**: the label means directly transcribed from the source, not that the forecast is certain. Source: SemiAnalysis / Jeremie Eliahou Ontiveros, Reyk Knuhtsen and Dylan Patel, *Datacenters 2027: The Year of Acceleration, +50GW in a Single Year*, email received 2026-10-19; email masthead Oct 18, public webpage Oct 19. Model as of October 2026. Both original charts inspected on November 6.

| Calendar year | US, IT GW added | RoW excluding China, IT GW added | Total excluding China, IT GW added | Status |
|---|---:|---:|---:|---|
| 2024 | 6.2 | 3.6 | 9.8 | Historical model estimate |
| 2025 | 10.2 | 5.5 | 15.6 | Historical model estimate; displayed components sum to 15.7 |
| 2026E | 18.1 | 6.9 | 25.0 | Forecast |
| 2027E | **38.0** | **13.2** | **51.2** | Forecast |

2025's 0.1 GW discrepancy is preserved as source rounding, not silently corrected. Source charts: [geographic split](https://substack-post-media.s3.amazonaws.com/public/images/7d297773-64db-4139-964b-8a2ec8f7a982_2700x1440.png), [construction status](https://substack-post-media.s3.amazonaws.com/public/images/d8a61ab9-ad4e-43e1-b6ec-21295e10b7d4_2700x1440.png), [article](https://newsletter.semianalysis.com/p/datacenters-2027-the-year-of-acceleration).

Arithmetic, using only this one model vintage:

- 2027 total: 38.0 + 13.2 = **51.2 GW**.
- US share: 38.0 / 51.2 = **74.2%**; RoW ex-China: 13.2 / 51.2 = **25.8%**. These are derived, not additional source inputs.
- 2026–27 combined additions: US 18.1 + 38.0 = **56.1 GW**; RoW ex-China 6.9 + 13.2 = **20.1 GW**; total **76.2 GW**. This is a two-year flow, not the installed stock at end-2027.
- Source construction-status chart: **39.4 GW operational + under construction**, **11.9 GW planned**, headline **51.2 GW** for 2027. Components sum to 51.3, a further 0.1 GW source-rounding discrepancy. The 39.4 is not 39.4 GW already delivered in 2027.

## China and 2028: what is established, and what remains unresolved

**China cannot be silently included in the 51.2 GW total.** Dylan Patel at CASPA on 2026-10-24 said China would build **7–8 GW in 2027**, but in that same answer described nearly 50 GW globally and about 35 GW in the US. That spoken framing does not reconcile with the written chart's 51.2 GW excluding China and 38 GW US. The speech does not explicitly specify IT versus facility GW. [Original transcript, 00:12:56–00:14:00](../../_podcasts/adhoc/2026-10-24%20-%20Semiconductor%20Industry%20Outlook%20Panel%20CASPA%202026%20CEO%20Summit.md).

The China-inclusive total is therefore **unresolved on a consistent basis**. A mechanical addition of the spoken China range to the written forecast would mix vintages and an unverified power definition; it is not adopted as the global forecast. Australia, India and Malaysia are named in the speech, but no country-level annual GW allocation is supplied.

| SemiAnalysis vintage | 2027/2028 claim | Treatment |
|---|---|---|
| Oct 19 report, October model | 2027 US 38.0 / ex-US ex-China 13.2 / total ex-China 51.2 IT GW | Preferred directly charted geography |
| Oct 19 report | 2028 ex-US share 35%, on the ex-China universe | HARD sourced percentage; GW bars deliberately blurred; absolute figures unavailable |
| Oct 24 CASPA / Patel | 2027 nearly 50 global / about 35 US / 7–8 China | Spoken, rounded, power basis unstated; inconsistent with written scope |
| Nov 1 / Barkin, Ma, Knuhtsen et al. | 2027 33.8 GW in top 20 US states | Subset, not a replacement for full-US capacity |
| Nov 1 / same | 2028 **62.2 GW US net additions**, most not started | HARD sourced forecast; article does not restate IT/facility basis |
| Nov 4, Ep. 043 / Ontiveros | 2027 roughly 40 GW in the US | Rounded spoken mark; not a new precise chart series |

[Nov 1 original article](https://newsletter.semianalysis.com/p/the-datacenter-backlash-goes-bipartisan). Do not combine its 62.2 GW with the October 35% share to manufacture a precise 2028 RoW total: that assumes an unchanged forecast vintage and definition. The 2028 permit exposure discussed in that article is not capacity already cancelled or delayed. No later complete geographic model export was recovered.

## Independent geographic bridge — Morgan Stanley

Morgan Stanley / Stephen Byrd, Joseph Moore and Brian Nowak, *What Does the Power Shortfall Mean for Semis?*, 2026-10-05. **Facility/power GW, global**, distinct from SemiAnalysis's ex-China IT-capacity basis. Figures were read from original Exhibit 1 (p4) and Exhibit 5, annual Part II.D.2 (p7). The US and RoW energised columns below are **DERIVED** from HARD sourced inputs; they are not separately published geographic forecasts.

| Year | Global incremental demand, HARD | US demand, HARD | US shortfall, HARD | Global energised, HARD | US energised, DERIVED | RoW energised, DERIVED |
|---|---:|---:|---:|---:|---:|---:|
| 2026E | 32 | 22 | 9 | 23 | **13** | **10** |
| 2027E | 56 | 30 | 5 | 51 | **25** | **26** |
| 2028E | 86 | 45 | 18 | 68 | **27** | **41** |
| 2029E | 124 | 63 | 35 | 89 | **28** | **61** |

[Report](../../relat%C3%B3rios%20bons/GLOBAL_20261005_0401.html) · [Exhibit 1](../../relat%C3%B3rios%20bons/_assets/GLOBAL_20261005_0401/p004.jpg) · [Exhibit 5 annual table](../../relat%C3%B3rios%20bons/_assets/GLOBAL_20261005_0401/p007.jpg).

Worked 2027 bridge:

1. Global demand 56 − US shortfall 5 = **51 GW globally energised**, as MS publishes.
2. US demand 30 − US shortfall 5 = **25 GW US energised**, derived.
3. Global energised 51 − US energised 25 = **26 GW RoW**, derived.
4. 25 + 26 = 51. This is an arithmetic identity, not independent validation.

This preserves MS's own framework, which subtracts a US shortfall from global demand. It does not independently establish that every RoW project can be delivered. MS's 55% US share relates to compute demand: multiplying all global energisation by 55% would misstate the geography after US supply constraints. Use the annual demand row directly; differences of rounded cumulative rows give different results (e.g. 51 − 22 = 29 versus the annual table's 30 in 2027).

## Other estimates: useful checks, not interchangeable totals

| Source and date | Geographic / power scope | 2026E additions | 2027E additions | 2028E additions | Use |
|---|---|---:|---:|---:|---|
| SemiAnalysis / Ontiveros, Knuhtsen, Patel, Oct 19 | US, IT net additions | 18.1 | 38.0 | Not visible in this chart | Geographic anchor above |
| Jefferies / Jonathan Petersen et al., Oct 9 | **North America**, delivered IT GW | 12.9 | 18.0 | 26.0 | Independent project-census forecast; NA is not US |
| Jefferies / same | North America, gross GW | 15.7 | 23.1 | 32.4 | Same source's gross basis; not an independent second forecast |
| Bernstein / Madison Rezaei et al., Oct 1–2 | US, IT GW; annual additions series archived in wiki | 13.4 | 19.5 | 25.1 | Secondary extraction; stock/additions discrepancy needs reconciliation |
| UBS / Timothy Arcuri et al., Sep 29 | Global ex-China, **compute shipment** GW | 26.5 | 50.8 | 67.7 | Demand/shipment benchmark, not delivered DC capacity |
| UBS / same | Global ex-China, confirmed powered shells | — | ~38 | ~50 | Separate shell-supply forecast; no recovered US/RoW annual split |

Jefferies primary [Exhibit 1, p2](../../relat%C3%B3rios%20bons/_assets/7913a58c-eb91-4769-8994-eb43cb2104d5/p002.jpg) and [p3](../../relat%C3%B3rios%20bons/_assets/7913a58c-eb91-4769-8994-eb43cb2104d5/p003.jpg) were inspected. Its 2029/2030 base deliveries are 31.9/33.6 IT GW; installed North America stock reaches 161.3 IT GW in 2030. These are different quantities.

Bernstein [report](../../relat%C3%B3rios%20bons/BERN_260832.html), [archived model extraction](../themes/ai-datacenter-power.md): installed IT stocks 33.7 / 47.3 / 67.0 / 92.4 in 2025–28 imply differences 13.6 / 19.7 / 25.4, rather than the archived additions 13.4 / 19.5 / 25.1. Do not silently relabel either series as the other. UBS [report](../../relat%C3%B3rios%20bons/20260930_UBS_AI_Research_-From_Semiconductors_To_Powered_Shell-_Wha.html), [source reconciliation in theme](../themes/ai-datacenter-power.md): its PUE 1.12 converts its own compute demand into shell demand, not forecast completed supply.

## Guardrails, sensitivity and coverage

- **PASS — arithmetic and units within each source.** Source rounding retained. No IT-to-facility conversion imposed. Annual flows separated from installed stocks, manufacturing output, interconnection queues and contract announcements.
- **PASS — no guessed geographic share.** SemiAnalysis split is directly observed in its chart. MS split is a residual derived from its own demand and shortfall tables. There is no fitted constant to calibrate.
- **UNRESOLVED — independent forecast agreement.** SemiAnalysis's US IT forecast is materially above Jefferies' wider North America IT forecast. Neither is an observed outcome, so agreement would not validate future deployment; averaging them would hide the disagreement.
- **UNRESOLVED — whole-world SemiAnalysis total and 2028 absolute RoW.** China basis/vintage is inconsistent; 2028 geography is incomplete. No arbitrary China plug or US market-share extrapolation is adopted.
- **Sensitivity:** for the MS bridge, holding source demand fixed, each additional 1 GW of US shortfall lowers US and global energised additions by 1 GW; RoW residual is unchanged by construction. That invariance is a feature of MS's model, not proof of RoW deliverability. A future revision to SemiAnalysis's US/ex-US forecast changes the reported split directly; no separate conversion assumptions are used.
- **Coverage:** archive FTS and power-theme/assumptions review; targeted Outlook search and recovery of the full Oct 19 SemiAnalysis email; original SemiAnalysis charts and Nov 1 webpage; CASPA transcript; original MS and Jefferies exhibits. This is not a complete export of SemiAnalysis's subscription model or an exhaustive review of every email. Bernstein/UBS comparison rows rely on their existing archive synthesis as labelled.
- **Deal deduplication:** reviewed the compute-deal timeline; these aggregate forecasts do not establish a new contract, funding milestone or delivery. No project MW or TCV was added to commitments.
- **Skeptic: PARTIAL overall; arithmetic PASS.** Independent reviewer inspected the SemiAnalysis regional chart, MS exhibits, Jefferies exhibit and CASPA transcript. Required qualifications are incorporated: no China-inclusive bridge, no 2028 cross-vintage extrapolation, MS RoW explicitly a residual, and historical estimates distinguished from forecasts. Remaining partial status reflects incomplete geographic coverage and future-delivery uncertainty, not an arithmetic failure.

## Changelog

- 2026-11-06 — Created. Corrected the prior archive shorthand that treated SemiAnalysis's roughly 50 GW as unqualified global capacity: original October charts explicitly say global **excluding China** and **IT capacity**. Preserved spoken and later vintages separately. No existing company forecast or deal total overwritten.

## Regional capacity snapshot recovered on 2026-11-06

SemiAnalysis / Everlyn Tan, Dylan Patel and Patrick Schaabi, 2026-09-25, The Chinese AI Infrastructure Boom. Original exhibit explicitly labels **live IT capacity, 2026 year-end**. This is a capacity stock, not annual additions or a 2028 forecast.

| Region | 2026YE IT capacity (GW), source labels |
|---|---:|
| North America | 58 |
| US (within North America) | 56 |
| APAC excluding China | ~15 |
| EMEA | ~14 |
| Latin America | ~2 |
| China | 24+ |

Source: https://newsletter.semianalysis.com/p/the-chinese-ai-infrastructure-boom
Original exhibit: https://substack-post-media.s3.amazonaws.com/public/images/713c729d-e750-45c3-b09a-2cacd2f3bb59_4290x2414.png
Verified against the original exhibit and the September 25 Outlook newsletter. North America 58 includes US56; do not sum both rows. No same-vintage 2028 annual-additions split across these regions recovered. No conversion of this stock into annual delivery flows.

Presentation update: chart 1 includes US2028 62.2GW from November 1 in a separate-color series with missing RoW encoded null. October2028 exUS35% remains a separate-vintage callout. No absolute RoW inferred by combining them.
