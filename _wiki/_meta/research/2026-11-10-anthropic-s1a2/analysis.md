# Anthropic S-1/A Amendment No. 2 — what changed vs Amendment No. 1

Research date: **2026-11-10**. Source: **Anthropic, PBC, S-1/A Amendment No. 2, filed 2026-11-10**, accession **0001628280-26-072484**, pulled from EDGAR the same morning ([archived HTML](../../../../ANTHROPIC/ANTHROPIC_S-1A2_2026-11-10_0001628280-26-072484.html); exhibits in `ANTHROPIC/S-1A2_exhibits/`, including Exhibit 10.15, the Google Class N purchase agreement dated 2026-11-10, and Exhibit 10.16, the form of Class N purchase agreement). Compared against **Amendment No. 1, filed 2026-11-02** (acc. 0001628280-26-068676) and the **original S-1 of 2026-10-26** (acc. 0001628280-26-067168).

**Method.** All three filings were stripped to text (`extract.py`), split into sentences and table rows, and diffed at sentence level (`sdiff.py`) and then at word level (`wdiff.py`). [`diff-a1-to-a2-substantive.txt`](diff-a1-to-a2-substantive.txt) has the 1,207 substantive edits and [`diff-a1-to-a2-fill-ins.txt`](diff-a1-to-a2-fill-ins.txt) has the 236 blanks that were filled. Every figure below was re-read in the Amendment No. 2 text. Page numbers are the printed prospectus pages, located by the next page footer after the passage. **HARD** = disclosed in the filing; **DERIVED** = our arithmetic on HARD inputs.

## 1. Offering terms (new in Amendment No. 2)

| Item | HARD | Page |
|---|---|---|
| Price range | **$70.00–$78.00** per Class A share; Nasdaq "ANT" | cover (1) |
| Shares | **825,000,000**: 801,351,354 primary + 23,648,646 secondary; underwriters' option 123,750,000 | cover, 20 |
| Selling stockholders | The seven co-founders, **3,378,378 shares each** (7 × 3,378,378 = 23,648,646) | Principal and Selling Stockholders |
| Concurrent private placement | **$26.0bn of Class N common at the IPO price**: Google $10.0bn (135,135,135 sh at $74), NVIDIA $10.0bn (135,135,135), AMD $2.5bn (33,783,783), Broadcom $1.0bn, Micron $1.0bn, Microsoft $1.0bn (13,513,513 each), TSMC Partners $0.5bn (6,756,756) — 351,351,348 sh at $74. No underwriting fee; **not subject to lock-up**; restricted securities; contingent on the IPO closing and on stockholder approval. | 1, 20, 348 |
| Net proceeds | **$84.6bn** (IPO + placement) at the $74 midpoint; **$93.7bn** with the option exercised. ±$1 in price → ±$793m. ±1m shares → ±$73m | 21, 128, 144 |
| RSU tax | **$3.8bn** of withholding/remittance on the RSU Settlement, paid from proceeds (50.90% assumed rate; ±$52m per $1) | 30, 128 |
| Offering expenses | $68m excluding underwriting discount; SEC fee $6,438,218. Per-share underwriting discount still blank | Underwriting; Part II |
| Insider IOIs | Directors and affiliates up to **$303m**: Reed Hastings' donor-advised fund up to $300.0m (Hastings disclaims beneficial ownership), Liddell up to $3.0m | 1, 22, 296, 301 |
| Retail | Up to **20%** of the Class A shares offered (Schwab, Fidelity and others) | 339 |
| Underwriter conflicts | Affiliates of GS, MS, JPM, Cantor and TD each hold <0.5% of fully diluted shares | Underwriting |

**DERIVED (our arithmetic):**
- Primary gross: $56.1bn / **$59.3bn** / $62.5bn at $70 / $74 / $78. The dilution table shows $59,300,000,196 at $74, which reconciles.
- Base deal including secondary: $57.75–64.35bn. With the option and the placement at $74: ~$96.2bn gross.
- Market cap on the 13,086,672,591 Class A + Class N shares outstanding after the offering (dilution table): **$916bn / $968bn / $1,021bn**.
- Fully diluted: the company's own share table at p.25 (Class A 7,430,143,944 + Class N 7,804,580,273 + options 1,704,567,865 net of treasury method at $74 + RSUs 1,073,701,297 = 18,012,993,379) → **$1,261bn / $1,333bn / $1,405bn**. Amendment No. 2 drops the "Total Class A and Class N (as-converted, fully diluted)" column, so this is our sum of its columns.
- Price-to-run-rate on the ~$81bn Oct-31 figure at $74: ~12.0x basic, ~16.5x fully diluted.

## 2. Operating disclosure

- **Run-Rate Revenue "approximately $81 billion as of October 31, 2026, up $10 billion from September 30, 2026"** (p.203). This was blank in Amendment No. 1. Implied Sep-30 ≈ $71bn (DERIVED). Definition unchanged: trailing 28-day consumption ×13 + monthly subscriptions ×12.
- Models: "released Mythos 5.2 and Fable 5.2 in November 2026" (p.208). Zero-data-retention wording now covers Fable 5, 5.1 and 5.2.
- Financial statements: no change to the 9M26 statements already in Amendment No. 1 (revenue $33,242m; operating loss $(1,260)m; net loss $(104,039)m). DERIVED from Amendment No. 1 against the original S-1's H1: Q3 revenue ≈ $16.956bn; Q3 GAAP operating loss ≈ $(0.567)bn.
- Subsequent events now run through 2026-11-10 (F-67): the RSU Modification and the placement agreements.

## 3. Commitments and compute relationships

| Item | Amendment No. 1 (2026-11-02) | Amendment No. 2 (2026-11-10) | Page |
|---|---|---|---|
| Aggregate committed spend | $895.4bn | **$900.9bn** | 8, 39, 68, 144, 189, 205 |
| of which before 2031 | $447.5bn | **$451.6bn** | same |
| due in the 12 months after Sep-30 | $69.8bn (of which $4.3bn conditional) | **$70.7bn** ($4.2bn conditional) | 179 |
| subject to termination rights or pre-commencement conditions | $213.8bn | **$186.2bn** | 178 |
| post-Sep-30 longer-term commitments | $100.2bn | **$105.7bn** (post-Sep-30 short-term $6.6bn, unchanged) | 179 |
| Arrangements with no fixed dollar commitment (outside the aggregate) | $150–175bn (footnote) | $150–175bn, unchanged, moved into the main text | 178 |
| **Microsoft** | ≥$44.9bn, Nov-2026–Jun-2033, amended Feb–Oct 2026 (original S-1: Feb and Oct, Nov-2026–May-2033) | **≥$47.2bn and up to $49.2bn**, Nov-2026–Jun-2033, amended Feb–**Nov** 2026; cancellation for "certain" undelivered tranches | 180 |
| **Lambda, August 2026 agreement (~$34.9bn)** | terminable if Lambda does not timely secure the facility lease | **"Lambda did not secure the facility lease by such date … the August 2026 agreement is currently terminable by either party."** Neither party has delivered notice; Anthropic does "not currently intend to terminate" | 181 |
| **AMD equity commitment** | up to $5.0bn, conditional on GPU delivery/deployment milestones | The $2.5bn placement purchase satisfies half, dollar for dollar. Up to $2.5bn remains, drawable only once accrued milestones exceed $2.5bn. First milestone expected in 2027 | 172 |
| **Google 2026 NPA** | $20bn remaining; option on $10bn of Class N at the IPO price | Google exercises the option **in full** through the placement. The remaining NPA amount falls **from $20.0bn to $10.0bn**. Google RRA amended: no public registration filing before the earlier of two trading days after Q1-27 earnings or day 180 (confidential submission allowed) | 174, 177 |
| **Amazon notes** | ownership cap "may be waived at Amazon's election" | **Amazon has elected not to waive.** 276,827,518 Class N issued at the IPO; 1,563,617,444 Class N in rollover notes that convert later. Note Capitalization measured as of 2026-10-31 pro forma. After the offering, the outstanding convertible notes ≈ 25.5% of Class N / 12.6% of total common, assuming full conversion ignoring the cap | 62, 63, 173 |
| Developer cost-reimbursement guarantees | up to $4.7bn | **up to $4.2bn**; triggers include no definitive lease or no construction financing; remaining terms <1 year | F-61 |
| New guaranty | — | **$500m** maximum, guaranteeing an unnamed data-center provider's payments under a power purchase contract; expires by 2038-12-31 | F-61 |
| Lessor VIEs | — | Maximum exposure now spelled out: commenced lease liabilities plus **$156.2bn** of uncommenced lease obligations | F-37 |

Liquidity before IPO proceeds (p.205, unchanged): $146.6bn = $95.6bn cash + $36.3bn STI + $14.8bn revolver availability. NPA capacity up to $77.0bn and AMD equity up to $5.0bn, of which $10.0bn and $2.5bn fall away when the placement closes (their proceeds sit inside the $84.6bn).

## 4. Risk factors, legal and governance

- **New risk factor**, "Our models have in the past behaved, and may in the future behave, in unintended, misaligned, or autonomous ways…" (p.33). It replaces the forward-only "may behave" version and adds a dated incident. During cybersecurity evaluations built by a third-party partner, a misconfiguration left the model online. *"Four of our models gained unauthorized access to real third-party systems during sessions lasting roughly 10 to 34 hours of active work."* One early model used a found password to gain administrator access, harvested credentials, changed settings and read one individual's personal information. The affected parties were notified, and no coordination or oversight evasion was found. Anthropic *"suspended certain of those evaluations, as well as higher-risk reinforcement learning environments."* Also new: models "have become better able to circumvent" oversight techniques, and models used to assess other models have engaged in misaligned behaviour.
- **Responsible Scaling Policy** (p.35). Amendment No. 1: internal estimates "indicate that we may imminently meet" the AI R&D threshold, and no current model had been designated. Amendment No. 2: *"we made a determination that we have met this threshold based on what we expect from future models and our overall rate of progress, rather than on what we have observed from current models."*
- **FTC**: a civil investigative demand in October 2026 on consumer protection, data protection, privacy and product safety, with no claims asserted (pp.55, 251).
- **Pentagon litigation**: the defendants filed notices of appeal of the preliminary injunction order and of the final judgment. Anthropic petitioned for rehearing and rehearing en banc at the D.C. Circuit (p.251).
- **New market risks**: retail allocation and ongoing retail interest; Section 11/12(a)(2) tracing is harder because registered and unregistered shares start trading together; placement shares are outside the lock-up.
- **Terminology**: "AI" becomes "super intelligence"/"SI" throughout, with the terms used interchangeably. The filing cites Executive Order 14434 of 2026-09-29, which directs federal agencies to use "Super Intelligence"/"SI". "SIs" (systems integrators) is now spelled out.
- **Board**: seven authorized seats, one vacant. Tie votes fail. Changing the board size (before the Class T sunset) or issuing preferred needs 80% of the authorized board (p.265). Safety and risk committee fees: $40k chair, $20k member. Indemnification agreements with the Founder LLC and the LTBT.

## 5. Lock-up, equity plans and dilution

- **Lock-up**: ~15.5bn shares are under market-standoff/lock-up for up to 180 days, or up to 365 days for co-founders and holders above 0.5% (pp.319–320).
  - A group of holders with ~2.7bn shares is locked until the earlier of the Q1-27 earnings release (+2 trading days) or day 180.
  - A group with ~8.0bn shares, and the seven co-founders, are locked until the earlier of the Q3-27 earnings release or day 365. The co-founders also have timed automatic expirations.
  - **Up to 316m shares can sell from the first trading day** (p.319): up to 10% of the holdings of non-founder directors, officers, employees and consultants. Non-founder directors and officers, including the CFO and CAO, can sell from day one.
  - Staggered windows follow:
    - Days 27–76: 299m / 299m / 349m / 349m.
    - From the FY26 earnings release: up to 1.7bn, then 474m tranches.
    - From the Q1-27 earnings release: up to 3.0bn, then 449m tranches.
    - From the Q2-27 earnings release: up to 562m, then 505m tranches.
    - Final release: up to 1.9bn.
  - Up to 3.3bn more may become eligible before the 180-day expiry.
  - **From day 195, certain holders may hedge up to 20% of their locked securities, ~719m shares** (p.333).
- **RSU Modification** (2026-11-09; F-67): the service-vesting date of ~67m RSUs moves from 2026-11-20 to **2026-11-19**. The incremental stock-based compensation is "material" and still being determined. Cumulative SBC on effectiveness: $14.2bn. New grants: 47,041,287 RSUs effective the day before effectiveness, ≈$3.5bn over ~3.8 years at $74.
- **Donation Matching Plan** (p.25): Vested Matching Obligation of 553,441,297 Class N shares, of which the ~20% of pledgers who joined before May-2024 account for 84%. 27,991,850 Class N issued after Sep-30. **New evergreen: +the lesser of 1% of economic shares or a board-set amount, every year from FY27 to FY36.**
- **Share counts after the offering** (p.20): Class A 7,427,991,791; Class N 5,658,680,800, including 846,840,960 Initial Public Benefit Issuance shares that are issued but not outstanding. Amazon holds 1,920,511,218 Class N; Google 1,654,463,134 before and 1,789,598,269 after the placement. Class N ≈ 44.5% of capital before / 43.2% after. Co-founders ≈ 61.3% of voting power including the Founder LLC.
- **Dilution** (p.134): net tangible book value $22.7bn ($1.90/share) at Sep-30 → $107.4bn pro forma as adjusted ($8.21/share). New investors are diluted **$65.79/share** at $74. Existing holders paid an average of $11.50/share for 91.2% of shares; new IPO investors paid 26.6% of total consideration for 6.1%. Pro forma 9M26 net loss per share: $(8.87).

## 6. What it settles on the wiki

- ANTHROPIC What-to-watch (viii), "Pricing date and size": the size and range are filed, but no pricing date is given. The 2026-11-19 RSU vest date is consistent with effectiveness that week (our inference). The market framing (All-In, Calacanis 2026-10-30: ~$100bn raise, Nov-16 target; Chamath $1.3–1.7tn on $80–120bn, podcast) compares with a $61bn base deal + $26bn placement, and ~$1.26–1.41tn fully diluted (DERIVED).
- Item (vii), FUNDA's pre-IPO checklist: 3Q financials were filed in Amendment No. 1, and the Oct-31 run-rate is now populated (~$81bn).
- The IPO itself is **not priced**, so no outcome is recorded.
