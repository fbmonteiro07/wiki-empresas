# GEV — Q3 FY26 print-night report (2026-10-28 BMO)

**1. Print.** Orders $29.3B (+96% organic); revenue $12.6B (+27% / +18% organic); adj. EBITDA $1.94B, 15.4% margin; GAAP EPS $4.81; FCF $5.41B; RPO $196.7B, guided above $200B in 4Q26 (GEV Q3 FY26 press release + 10-Q, 2026-10-28). Gas: 11 GW signed and 13 GW of SRAs converted. Backlog 64 GW is now above SRAs at 58 GW, a year ahead of the '27 guide; YE target ≥130 GW (was ≥125). All gas GW are turbine nameplate. Against management's own Q3 guide: Power +25% revenue / 21.4% margin vs +17–19% / ~17–18%; Electrification $3.86B, inside $3.8–4.0B. FY26 raised to $46.5–47.5B revenue, 13.5–14.5% margin, $16–17B FCF. **Not scored vs Street**: the page had no Q3 consensus and estimates.json had already rolled.

**2. Sections edited.** Snapshot prose, Current state (new Q3 block), Debate (dated bullet), Catalysts (Q3 resolved; 4 new items; 3 marked ✅), Risks (tariffs + M&A), Intra-quarter (Q2 window moved into a Changelog ARCHIVED section; fresh window opened), Mgmt-evolution (+Q3'26 column), Sources, Changelog. Superseded values moved to Changelog: FY26 revenue/margin/FCF guide, Power and Wind guides, the GW target, backlog timing, the buyback authorization, and the tariff estimate ($250–350M → under $100M).

**3. outcomes.md:** `- GEV 2026-10-28 — bull won — Q3 FY26: backlog GW > SRA GW a year early, Power margin 21.4% vs ~17–18% guided, FY26 guide raised (FCF $16–17B), RPO $196.7B → >$200B in 4Q26; preliminary, no post-print tape in corpus`

**4. Compute-deal items:** none. The hyperscaler MV-UPS order and the 6 MW SST award are equipment orders, not compute or capacity deals.

**5. Theme read-throughs**
- ai-datacenter-power: Electrification data-center orders slowed to ~$1.4B in 3Q (vs $2.7B in 2Q), >$6B YTD. Data centers are ~20% of gas customers (GEV Q3 call).
- 800v-dc-power: first MV-UPS hyperscaler order. SST prototype in testing at Malta, NY; the 6 MW outdoor SST award goes to contract in 4Q (GEV Q3 call).
- hyperscaler-capex: no customer financing stress, no SRA exits, cash terms unchanged (Strazik answering Arcaro/MS).
- ai-datacenter-power (HV grid): Trench is ≈€8.0B at 13x 2028 EBITDA. Management sizes HV equipment at ~$130B of a $300B 2030 TAM (GEV Q3 call; 10-Q Item 5).

**6. 🔭 Variant perception**
- The order-peak bear now has management's own cadence. 3Q signings were 11 GW vs 21/20 GW in 1Q/2Q, and 2027 quarters will "feel like 3Q and 4Q". That cuts against the 09-16 desk relay that 20 GW was "conservative".
- The page's ✓ on the Electrification/DC row is now weaker: organic orders −9%, DC orders halved, equipment backlog up only ~$1B q/q.
- On Electrification margin above 30%, Strazik said "directionally in the neighborhood". The page still carries a 22% target for '28.
- The tariff figure in the page's Risks section had missed two updates.

**7. Garbles:** "margin and backlog" → margin **in** backlog (Strazik, prepared remarks + Electrification answer; Q4 FY25 call usage). Glossary addition proposed.

**8. Open items:** Julian Mitchell is tagged JPMorgan by the transcript but Barclays on the page, so his affiliation is unconfirmed. Surnames for the new CFO "Claire" and Wind leader "Hakan" are unconfirmed. The call's slide deck (Trench financials) is not on disk. The Q4 print date was not given (only "January"). Whether >half of the 2031 slots will be sold by YE was not disclosed. There is no post-print reaction yet. QA: `transcript_qa.py --pages _wiki/GEV.md` found 0 flagged hits, and a glossary scan of the 133 lines added to GEV.md also found 0. The full `--diff` run is left to the coordinator.


> **Correction (verifier, 2026-10-28):** the backlog-GW > SRA-GW crossover was guided for **2H26** on the Q2 call ("In the second half of the year… achieving an important inflection point with gigawatts in backlog greater than SRAs"), so it arrived **as guided, not "a year early"**; Electrification equipment backlog was **+$1.6B q/q** ($40.6B in the Q2 10-Q), not "~+$1B". The page is corrected; the outcomes.md line was written with the corrected wording.
