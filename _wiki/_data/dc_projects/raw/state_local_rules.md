# State & local data-center pauses after the 2026-11-03 elections — rules layer

_As of 2026-11-06. Companion to `rules_research.json` (same folder). Research only: no wiki page was edited._

**How to read the dates.** `base` = the most likely end given the election results. `stress` = the long end. Texas also gets a `short` end, the shorter branch in the sourced range. **"Inferred"** = a date Capstone derived from a rule (a session calendar or an effective-date rule), not one a source stated. Results are unofficial and uncertified (Wikipedia 2026 gubernatorial page, read 2026-11-06; Luminix 2026-11-05).

**Source quality, by weight.** Primaries and law-firm alerts on the orders (DLA Piper, B&D, Ballard Spahr, GTLaw, Loudoun County releases). SemiAnalysis 2026-09-15 and 2026-11-01 (independent research, sells the model it cites). Wells Fargo and FundaAI 2026-11-04 (on the wiki 11-05 block). Local and regional press. The **Moratorium Nation** inventory (Michael Bommarito, CC-BY-4.0, 1,293 local instruments, cohort 2026-11-05) for local moratoria. **Luminix** 2026-11-05 is an aggregator report, used as secondary and flagged each time. The **"amigo Felipe" deck** (2026-11-06) is the scenario under test, never used as a source of record. SemiAnalysis Ep. 043 is a **podcast, not research**.

⚠️ **Coverage gap.** The shared web-search budget ran out mid-task. These items were **not verified on the web**:
- Ascension Parish (LA)
- Tucson and Chandler (AZ)
- Farmington and Hermantown (MN)
- Post-election data-centre stances of Benson (MI), Crowley (WI), Klobuchar (DFL-MN) and Holscher (KS)
- The outcome of Loudoun's Oct-20 formal resolution

---

## Who won (data-centre-relevant governors)

| State | 2026 → 2027 | Flip | Data-centre stance | Takes office |
|---|---|---|---|---|
| TX | Abbott (R) → **Hinojosa (D)** | ✅ | Ban on "all data center approvals" until the Legislature passes protections | 2027-01-19 |
| OH | DeWine (R) → **Acton (D)** | ✅ | "Conditional moratorium" on new DCs (4-6 conditions) | 2027-01-11 (rule, inferred) |
| GA | Kemp (R) → **Bottoms (D)** | ✅ | Temporary pause on state approvals for new DCs; no end date; PSC flips 3-2 D | Jan-2027 (day not verified) |
| NV | Lombardo (R) → **Ford (D)** | ✅ | Pause on new **tax abatements** only; no permit pause | 2027-01-04 (rule, inferred) |
| IA | Reynolds (R) → **Sand (D)** | ✅ | Conditions, **no pause** | Jan-2027 |
| KS | Kelly (D) → Holscher (D) leads 50.3-49.7, **not called** | ? | not researched | — |
| NM | Lujan Grisham (D) → **Haaland (D)** | — | **Day-one EO moratorium** on new large-scale DCs until protections and rulemaking | 2027-01-01 |
| PA / OR / NY / AZ / IL | incumbents re-elected (D) | — | conditions (PA), permit holds (OR, NY), tax freezes (AZ, IL) | — |
| OK | Stitt (R) → Mazzei (R) | — | opposes a pause; developers pay their own way | — |
| MI / WI / MN | Benson (D) / Crowley (D) / Klobuchar (DFL), all holds | — | **not verified** | — |
| VA / IN / LA / MO | no 2026 race (Spanberger D / Braun R / Landry R / Kehoe R) | — | VA: EO 22 conditions; IN, LA, MO: local only | — |

Sources: Wikipedia 2026 gubernatorial elections (rev. 1384082438); KFOX/Texas Tribune 2026-11-04; statenews 2026-07-27; WTVM 2026-11-05; NM Political Report 2026-09-17; Cleanview 2026-11-04; Fox5 Vegas 2026-08-19; SemiAnalysis 2026-11-01.

---

## Texas — the one that moves GW

**Before the election (Abbott).**
- **Aug-3-2026 directive (PUCT/ERCOT):** every DC advancing through ERCOT interconnection is verified and audited before it can move forward. That covers the Batch Zero ≥75 MW queue and a community-impact RFI for loads ≥25 MW. No DC energization approvals until verification. SemiAnalysis 09-15: 17 facilities / 6.6 GW had cleared every other gate and were waiting.
- **Sep-14:** TWDB water-reporting directive.
- **Sep-21:** letter to TCEQ to *"pause the issuance of all permits related to data center projects until ERCOT completes its review."*
  - Covers air (on-site generation and gensets), water, stormwater and water rights.
  - Covers new **and** in-process applications.
  - No MW floor, and no exception for BTM or non-ERCOT areas (B&D; DLA Piper 09-25).
  - SemiAnalysis 11-01: site prep can proceed, but generating equipment and its foundations can't; missing stormwater cover blocks land disturbance even earlier.
- **Audit timeline:** ERCOT report targeted **Dec-10-2026**, PUCT review Dec-17. That report *"does not by itself reopen permitting"* (SemiAnalysis; WFS).
- **Batch Zero:** the study that allocates MW to studied load (scheduled to Apr-9-2027) is paused. ERCOT's Seely: *"We will not have the study done by April 9, 2027."*

**After the election (Hinojosa, sworn in Jan-19-2027).**
- Her pledge (Oct-22 video, quoted by KFOX 11-04): *"When I am governor I will issue a moratorium — a ban — on all data center approvals until laws can be passed by the Legislature."*
- She works with a **Democratic House**. The **Senate stays Republican** (~19-12; Luminix, secondary).
- An NBC DFW sidebar headline (not read) reports Lt. Gov. Patrick lost to Goodwin. That would change who sets the Senate agenda; unverified.

**What it blocks in the model.** Air permits (TCEQ) for on-site power, plus any new ERCOT large-load approval. The pledge would extend this to "any new permits" for DCs.

| Instrument | Start | Short | Base | Stress |
|---|---|---|---|---|
| TX-TCEQ permit freeze | 2026-09 | 2027-06 | **2027-09** | 2027-12 |
| TX-ERCOT audit / interconnection | 2026-08 | 2027-06 | **2027-09** | 2027-12 |
| Hinojosa moratorium (pledge, executed through the two above) | 2027-01 | 2027-06 | **2027-09** | 2027-12 |

**Why these ends.**
- **Session and effective date:** the session runs Jan-12 to May-31-2027 (WFS). Bills without two-thirds of both chambers take effect **Sep-1** (FundaAI). Base = she holds approvals until the law applies, so projects approved Jun-Aug don't escape the new rules (inferred).
- **Short (Jun-27):** the hold is lifted when the bill passes or is signed. That is WFS's "likely runs through the 2027 session" and SemiAnalysis's "~8 months from September". FundaAI's base is shorter still: filed applications resume review in 1H27.
- **Stress (Dec-27, inferred):** the Republican Senate stalls the bill, so it takes a special session (≤30 days). Special-session laws take effect ~91 days after adjournment without two-thirds.
- **Lag after reopening:** the deck assumes ~12 months to build on-site power once the air permit issues (Abilene example: Mar-28 → Sep-28).

**Grandfathering.**
- Permits issued before Sep-21 stand, but a campus can still need approval for its next power phase.
- TCEQ suspended ~16-17 permits issued after Sep-21 and shut its STEERS portal (Luminix; Public Citizen per KFOX).
- ERCOT Base Load (executed IA etc.) is "modeled but not re-evaluated" but still needs verification.
  - **Open question 1:** whether Hinojosa's ban reaches already-classified Base Load. This is FundaAI's swing factor.
  - **Open question 2:** whether lame-duck Abbott releases verified projects between Dec-17 and Jan-19. No source either way.
- **Execution caveat:** TCEQ and PUCT commissioners are Abbott appointees on staggered terms (deck; SemiAnalysis 11-01). The legality of a governor-directed permit hold is untested.

**Local Texas.** Counties have little zoning power (Luminix). The tracker has 5 active instruments:
- Lavon (90 d), Brownsville (90 d from Nov-4), Hays County (to Dec-26), Harlingen (to Dec-26), Austin County (open-ended).
- Fort Worth: proposed.
- Hill County: rescinded after a $100M developer suit.
- **Average 3.3 months (n=3): local Texas pauses don't bind.**

---

## Virginia — no state pause in base; SB 843 is the tail

**Before and after.** No 2026 governor race.
- **EO 22** (Spanberger, signed 2026-09-18, effective immediately) is **conditions, not a pause** (GTLaw):
  - NDA ban for state agencies.
  - ≥25 MW DCs barred from VEDP Business Ready Sites and expedited permitting.
  - Eastern Virginia groundwater area designated cooling-water-scarce.
  - DEQ noise and backup-generation rules due within 180 days (~Mar-27).
  - SCC/PJM cost allocation.
- She has **not** accepted calls for a statewide moratorium (WTVR). The deck's quote "é uma escolha local" was not found in a primary.

**SB 843** (Sen. Russet Perry D-Loudoun, with Sen. Roem).
- Would bar local approvals and state permits for **new** DCs (and, per reports, related energy infrastructure) from **Jul-1-2027 to Jul-1-2030**.
- Prefiled and referred to Senate Local Government on 2026-10-09.
- Opposed by the Data Center Coalition. Sturtevant (R) is drafting his own version.
- Grandfathering is not written in. Perry says projects already in process may hold "vested rights".
- The 2027 session convenes in January, with a reconvened (veto) session in April; acts take effect Jul-1.
- **Base: not enacted. Stress: Jul-27 → Jul-30** (deck: 3.5-3.9 GW to 2031+).

**HB 1515** (continued to 2027): a local-approval moratorium until pending interconnection requests are met or **Jul-1-2028**. Stress only.

**Local.**
- **Loudoun County** — the one that matters.
  - Voted **7-1-1 on 2026-09-15 to pause Board votes** on legislative (special-exception) DC and substation applications, effective immediately.
  - Runs up to **12 months (Virginia's statutory clock)** or until Phase 2 standards are done (expected summer 2027). End ≤ Sep-2027.
  - Grid-reliability substations are excepted.
  - **≥17 grandfathered by-right cases (>11M sq ft) are NOT affected.** The County Attorney says a blanket pause on administrative applications is illegal (Loudoun release 2026-09-16).
  - The formal resolution was due Oct-20; Luminix says a vote is set for Nov-17. Not reconciled.
- **Chesapeake:** deferral of discretionary applications, 8 months to ~Mar-27.
- **Virginia Beach:** 12 months to ~Aug-27.
- **Prince William:** no moratorium. Rezoning denials instead: Digital Gateway voided by the Court of Appeals in Apr-26 and abandoned by QTS in Jul-26; Dulles South rejected 2026-07-07.

---

## Ohio — conditional, mechanism unknown

- **Before.** No state pause. DeWine paused **new sales-tax-exemption** approvals (SemiAnalysis: May-26; Luminix: ~May-27 *and* "announced Aug-5"). That is cost, not delay.
- **After.** Acton (D) pledges a **"conditional moratorium"** on new DCs. Projects proceed only if they meet her conditions. The condition lists differ by source:
  - statenews 07-27 names four (union labour, environmental standards, community-benefit agreements, cover all utility costs), plus no NDAs and ideally their own energy.
  - Luminix lists six (adds incentive clawbacks and brownfield siting).
  - The deck says "6 conditions".
- **Mechanism.** No draft EO has been published. Republicans keep both chambers. A statute takes effect 90 days after signing (SemiAnalysis 11-01).
- **Model.** **Base: no binding pause.** Compliant projects proceed; SemiAnalysis notes a single qualifying project can move. **Stress: a ~6-month hold on state approvals Jan-27 → Jul-27** (inferred levers: Ohio EPA air permits, Power Siting Board for >50 MW generation).
- **Local Ohio** is the densest state. The tracker has **148 active DC instruments, mean 11.5 months (n=137).** Big-project ones:
  - Sunbury (to Jan-31-2027; AWS site)
  - Commercial Point (18 months; Amazon "Project Cosmos")
  - St. Clair Township (12 months; AWS/Trenton annexation)
  - Lima (18 months)
  - Urbana (CyrusOne/Thor)
  - Ashville (to Jan-2027; EdgeConneX)
  - Monroe Township, Adams County (AWS interest)
  - Perry (Province Group site exempted)
- **Ballot 11-03 (permanent, no sunset):** 11 prohibitions passed — Conneaut, Defiance, Granville, Hubbard, Oregon, Pataskala, Piqua, Sunbury, Trenton, Upper Sandusky, Urbana. Grove City now needs a voter OK for ≥20 MW. Wilmington voters rejected 4 rezonings ~20-80. Barclays/Ballotpedia: 17 prohibitions nationally, 11 in Ohio.

---

## Georgia — a pause with no mechanism yet

- **Before.** No state pause. Kemp. The PSC was 3-2 R. Project Camellia's (OpenAI, Effingham, 3.2 GW) Georgia Power contract was approved in Aug-26.
- **After.** Bottoms (D) pledges a temporary pause on **state approvals for new DCs** "until consumer protections are established" (WTVM 11-05).
  - No end date, no exemptions and no mechanism (SemiAnalysis 11-01).
  - Luminix: "one month, six months, or longer"; not permanent. One report says by executive order.
  - Democrats won the **PSC 3-2**. It plans an affordability docket and a review of DC billing. Commissioner Hubbard says it is not his "power or interest to stop data center expansion".
  - Legislature: Luminix says the House flipped D and the Senate stays R 29-27 (secondary).
- **What it would block (inferred).** EPD permits: air for gensets and on-site generation, water withdrawal, NPDES. Local zoning is outside a governor's reach.
- **Model.** **Base Jan-27 → Jul-27** (6 months, inferred: statutory protections adopted in the 40-day session, effective Jul-1). **Stress → Jan-28** (12 months, Senate blocks).
  - The deck is internally inconsistent: slide 2 says Jan-27 → Jan-28, slide 3 says 6 months base / 12 stress.
  - Grandfathering is unstated. Projects with approvals in hand, e.g. Camellia, are the likeliest carve-out.
- **Local Georgia:** 50 active DC instruments, but **short — mean 5.1 months (n=55).**
  - Coweta: 180 d to ~Dec-13-26; 5 vested proposals incl. Project Sail ~900 MW exempt.
  - DeKalb: extended to Mar-30-27.
  - Savannah, Chatham County, Bloomingdale: ~155 d to Jan/Feb-27, prompted by Camellia.
  - Madison County: to Feb-22-27.
  - Douglas: its 2025 90-day pause expired; a 4.4M sq ft rezoning was denied 2026-07-08.
  - Monroe County: replaced by a UDO in Apr-26 (Google-purchased site).

---

## New Mexico — a new day-one moratorium

- **Haaland (D)**, takes office Jan-1-2027. She pledged a **day-one EO moratorium on new large-scale DC projects** until protections are in place and "any necessary rulemaking is completed" (NM Political Report 09-17; Cleanview 11-04). No MW threshold is stated, and the approvals covered are not specified.
- **Model.** **Base Jan-27 → Sep-27**: the 2027 60-day session runs ~Jan-19 to ~Mar-20; laws take effect 90 days after adjournment (~mid-Jun); add ~3 months of rules (all inferred). **Stress → Jan-28** (rulemaking ~6 months).
- **Project Jupiter (Oracle/OpenAI).** The air-permit hearing was set for Dec-5, with a ruling hoped for by Dec-30 before the new administration (10-23 call, speakers UNCONFIRMED). *"If this goes into January … all bets are off."* Pre-election, Haaland said *"I don't have the power to stop Project Jupiter."*
- **Local:** Socorro County 1-year moratorium (to ~Jun-27).

---

## Oregon, New York — holds already in force, end mid-2027

- **Oregon (Kotek re-elected).** Two holds, both to **Jul-1-2027**:
  - Sep-8 pause on state-land deals. SemiAnalysis: no forecast impact.
  - **Oct-9 DEQ hold** on NPDES, WPCF, ACDP and Title V permits for new or expanded DCs, plus municipal wastewater permits serving DCs. Pending applications are frozen. Projects holding every DEQ permit are not directly hit, but phases, modifications, renewals and stormwater can be (Ballard Spahr 10-20).
  - **Base Jul-27; stress Dec-27** (inferred): technical review remains after the hold (SemiAnalysis: "July 1 is not a promise that permits arrive the following day"). A 3-year statutory moratorium is proposed for 2027 — tail.
- **New York (Hochul re-elected).** **EO 62 (Jul-14-2026):**
  - DEC discretionary permits for **≥50 MW** DCs are held until the DPS GEIS is done ("up to a year").
  - Applications deemed complete before Jul-14 are exempt. Local permits are not frozen.
  - SemiAnalysis: ~1.4 GW exposed, ~0.8 GW delayed by 6-10 months.
  - **Base Jul-27; stress Jan-28** (inferred): the GEIS slips, or the **RDCD Act** (1-year ≥20 MW pause, passed Jun-4) is signed instead of vetoed. Hochul must act by end-Dec-26; a veto is expected.

---

## Pennsylvania, Indiana, Nevada, Iowa, Arizona, Louisiana — no state pause

- **Pennsylvania.** **EO 2026-05 (Aug-18):** for >25 MW, DEP won't issue permits until GRID compliance (consent order) **and local approvals**. DCs are out of Fast Track; NDAs banned.
  - SemiAnalysis does not count it as a pause (no expiry). Delay = time to get local approval.
  - HB 2650 (GRID codification) passed the House 134-68 on Jun-24; the R Senate has not acted. The session ends Nov-30-2026, so it dies unless passed in the lame duck (inferred).
  - **Local: 23 active, mean 5.9 months (n=23)** ← the Municipalities Planning Code 180-day curative-amendment ceiling.
    - **Hazle Township:** 180 d from **Jun-8-2026 → ~Dec-5-2026** (tracker; SemiAnalysis "June 2026"). **The deck's Jul-26 → Jan-27 is one month late.** It binds NorthPoint "Project Hazelnut" into 2027.
    - Upper Burrell: TECfusions permits already granted are excluded.
    - Falls Township: AWS under construction is excluded.
    - Clinton Township, Wayne County: Linde $6bn.
- **Indiana.** No state pause (Braun R).
  - "Nearly a third of counties" restricted DCs by Jul-26 (WFYI: 11 ordinances, ≥17 moratoria, 2 bans). Bond Buyer, Sep-26: 25 of 92 counties with moratoria, 3 bans. A later IIB headline: "over half" (not read).
  - **Indianapolis/Marion: MDC approval Aug-19-2026, effective immediately, through ≤Dec-31-2027** ✓ deck. It excludes approved DC Blox, Metrobloks and Sabey.
  - **Tracker mean 12.5 months (n=24)** ✓ the deck's ~12. Fulton County (500 MW Decennial), Jeffersonville (Meta excluded), Madison County (to Jun-27).
- **Nevada.** Ford's pledge is a **tax-abatement pause only**. **The deck draws a state-pause outline around NV — not supported.** Local: Reno to Aug-31-27, Nye County open-ended (Manse $18.4bn).
- **Iowa.** Sand is conditions-only. The deck's R→D flag is right, but there is no pause. Local: 41 active, mostly counties.
- **Arizona.** HB 4168 s.31 sets a 3-year freeze on **new tax-program certifications** (Jul-1-2026 → Jun-30-2029). Tax only. Local: Pima County 120 d (Aug-11 → ~Dec-9-26; "Project Gravel" caught). Tucson and Chandler not verified.
- **Louisiana.** No state pause. **New Orleans:** interim zoning district + permitting hold from **Jan-28-2026**, 1 year + one 180-day extension allowed (→ Jan-27 or ~Jul-27). **Ascension Parish (90 days): deck only, unverified.**
- **Oklahoma.** Mazzei (R), no pause. Local: **Oklahoma City and Tulsa (Project Anthem) to Dec-31-2026** or earlier zoning.
- **Missouri.** Local: St. Charles County to end-Jan-27 (6 months); the City of St. Charles moved to a permanent ban in May-26 (Project Cumulus withdrawn).
- **Michigan / Wisconsin / Minnesota.** Local pauses only:
  - MI: 124 active, mean 10.0 months. Saline Township excludes "The Barn"; Dorr Township (Microsoft); Lyon (Project Flex approved, unaffected).
  - WI: 39 active, mean 13.9 months. Dane and Dodge 18 months (Meta Beaver Dam excluded); Milwaukee 1 year.
  - MN: 26 active, mean 11.2 months.
  - Statewide bills died in 2026 in WI and MN.

---

## Local moratoria — summary for the model

- **Universe.** 1,293 local instruments (all sectors); **934 data-centre instruments active or extended** across 46 states (tracker, cohort 2026-11-05). Earlier counts: SemiAnalysis 09-15 ">300 enacted", Barclays 09-16 ">300".
- **Average original term (data-centre sector, enacted): 10.6 months mean / 12 median (n=863).** By state, mean:
  - Short: GA 5.1, PA 5.9, ME 5.7, OR 3.9, TX 3.3, CA 1.9 (urgency ordinances).
  - About a year: IN 12.5, OH 11.5, MI 10.0, MN 11.2, NY 13.5, WI 13.9, KY 12.1, MD 14.9, TN 14.9.
  - Full table in the JSON.
- **The deck's IN ~12 and PA ~6 are confirmed** by the tracker (12.5, n=24; 5.9, n=23).
- **Why they rarely bind** (SemiAnalysis 09-15):
  - County moratoria stop at city lines.
  - They freeze **new** applications, not granted approvals.
  - Short terms expire before 2028+ projects need the approval.
  - Other constraints may already gate the schedule.
  - Result: ~20 GW sits inside restricted boundaries, but only **1,525 MW is delayed** (3 projects), and ~80% of live restrictions hold no modelled capacity.
- **The JSON lists 100 entries.** 74 are in force: the requested ones, plus every tracker record naming a hyperscaler, ≥100 MW or a $bn project, plus the 11-03 Ohio and Kansas ballot prohibitions, the Wilmington referenda, and the Prince William and Douglas denials.
  - `end_inferred=true` means start + stated term, not a reported expiry.
  - The tracker's own status lines are mostly "Active as of 2026-09-23".

---

## Where sources disagree

| Item | Source A | Source B | Note |
|---|---|---|---|
| TX pause end | WFS 11-04: "through the 2027 session" (~Jun-27) | Deck / SemiAnalysis long branch: Sep-27 (law effective) | FundaAI base is shorter: filed applications resume 1H27. Carve-out of filed applications is the swing factor. |
| TX pre-vote base | SemiAnalysis 11-01, Barkin on Ep. 043, GS 11-01: Abbott wins, December restart | Result: Hinojosa won | ✗ on all three pre-vote bases |
| Hazle Twp dates | Deck: Jul-26 → Jan-27 | Tracker: Jun-8-26 + 180 d → ~Dec-5-26; SemiAnalysis: adopted June | Use the tracker |
| GA pause length | Deck slide 2: Jan-27 → Jan-28 | Deck slide 3: 6 m base / 12 m stress; Luminix: "1 month, 6 months, or longer" | No primary yet |
| OH conditions | Deck: "6 conditions" | statenews: 4 named (+2 soft); Luminix: 6 | Same direction |
| OH tax pause start | SemiAnalysis: May-26 | Luminix: ~May-27 and "announced Aug-5" | Tax only |
| NV | Deck: state-pause outline | Ford: tax-abatement pause only | Drop NV from state pauses |
| VA Spanberger quote | Deck: "é uma escolha local" | WTVR: has not accepted a statewide moratorium; EO 22 | Quote unverified |
| Loudoun formal vote | County release: resolution Oct-20 | Luminix: vote set Nov-17 | Pause itself enacted 09-15 per county |
| Ballot counts | Barclays/Ballotpedia: 41 measures, all but 1 restrictive (Harwood ND) | GS Pastrick: 43 of 44; Luminix: 46/47 or 40/41; FundaAI: ≥50 proposed | Counts carry no GW |
| Local count | SemiAnalysis 09-15: 300+ enacted, 400+ tracked | Tracker: 1,293 instruments, 934 DC active | Different vintages and definitions |

---

## Biggest open questions

1. **Texas carve-outs:** does Hinojosa's ban reach (a) applications filed before Sep-21, and (b) ERCOT Base Load already classified? Does Abbott release anything between Dec-10/17 and Jan-19?
2. **Texas Senate:** a Republican Senate plus a reportedly Democratic Lt. Gov. (unverified). Does a bill pass by May-31, and with two-thirds for immediate effect?
3. **Georgia and Ohio mechanism:** which state approvals a governor can actually hold (EPD/Ohio EPA air permits? siting board?), and whether courts allow it.
4. **New Mexico:** whether the Jupiter air permit issues before Jan-1, and whether the EO grandfathers it.
5. **Virginia SB 843:** committee fate in Jan-Feb 2027; the Spanberger veto/amendment in April. Is vested-rights language added?
6. **NY RDCD Act:** veto or signature by end-Dec-2026.
7. **Loudoun:** the formal resolution, and whether the 2025 grandfathering (17+ by-right cases) is ended.

## Sources (main)

**Corpus (paths relative to `E:\Wiki Felipe empresas`):**
- `_wiki\themes\ai-datacenter-power.md` (11-06, 11-05, 11-02, 10-14, 10-01, 09-16 blocks)
- SemiAnalysis 2026-11-01 email: `relatórios bons\2026_11_01_ENC_The_Datacenter_Backlash_Goes_Bipartisan_...email.html`
- SemiAnalysis 2026-09-15: `E:\research-sources\emails\semianalysis\2026-09-15-datacenter-moratoriums-us-buildout.html`
- SemiAnalysis Ep. 043 transcript (podcast): `_podcasts\semianalysis\2026-11-04 - Ep. 043 ...md`
- Deck: `relatórios bons\2026_11_06_amigo_felipe_gw_atrasa_pausas_estaduais.html`
- MS Byrd Tech Talk 2026-08-07: `relatórios bons\2026_08_14_stephen_byrd_texas_data_center_pause.html`
- GEV page (Loudoun, MS desk 09-17)

**Web:**
- Moratorium Nation inventory and state tracker (mjbommar.github.io/moratorium-data-2026, cohort 2026-11-05)
- Loudoun County releases 2026-09-16/17
- GTLaw EO 22 (Sep-26); Holland & Knight 2026-10-19; WTVR (Oct-26)
- KFOX 2026-11-04; NBC DFW (Nov-26)
- DLA Piper 2026-09-25; Beveridge & Diamond (Sep-26)
- Ballard Spahr 2026-10-20
- WTVM 2026-11-05
- NM Political Report 2026-09-17; Cleanview 2026-11-04
- statenews 2026-07-27
- Fox5 Vegas 2026-08-19
- Fortune 2026-11-05; CNBC 2026-11-04
- Luminix 2026-11-05 (secondary)
- Wikipedia 2026 gubernatorial elections
