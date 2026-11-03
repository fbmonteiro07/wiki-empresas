# Reconciliation — /run-inbox 2026-11-02

_This report checks each new quantitative datapoint from tonight's sources against three baselines: (1) prior wiki marks; (2) Capstone house models; (3) BBG consensus._

- **BBG live is OFFLINE**: `bdp` gets "Failed to connect to 127.0.0.1:8194", so the Terminal is not logged in. The BBG column uses the **on-disk snapshot `_wiki/_data/estimates.json`, asof 2026-11-02**. It is same-day (the 11-02 /wiki-consensus run, 107/107), so it does not need re-running.
- **House models:** GOOG (`Google Modelo oficial.xlsx`, 2026-06-05) is the only house model relevant tonight. There is none for BKNG, CSCO or OPENAI, and LITE/MRVL have no new numbers.
- **Private names** (OPENAI, ANTHROPIC) are checked against prior wiki marks only.
- **Sources tonight:**
  - Wells Fargo GOOG (2026-11-01).
  - SemiAnalysis "The Datacenter Backlash Goes Bipartisan" (2026-11-01).
  - Two Capstone BKNG docs (2026-11-02).
  - Bernstein LITE webinar invite (2026-11-02; no numbers).
  - Three podcasts (a16z/Eve 10-30; Cisco's Patel @ UC Irvine CDT, posted 11-02; Altman @ ADIPEC 11-02).

## DIVERGES (the alpha)

| Name | New datapoint (source) | vs prior wiki | vs house | vs BBG (snapshot 11-02) | Read |
|---|---|---|---|---|---|
| **GOOG** | Search growth cut to **+9% 4Q26 / +4% 1Q27 / +6% 2Q27**, with AI Overviews penetration (est. 82% global, +~7pts in October) as the driver. Paid clicks +4% / 0% (Wells Fargo · Gawrelski / Young, "AI Overviews Penetration Primary Factor in Search Revenue Deceleration", 2026-11-01) | Management blamed FX first and expects "a couple of points" of lapping in Q4 (page Sinal). Wells' own 4Q was +10% before this note | house has no quarterly Search line | Wells puts itself 1pt / **5pts** below consensus for 4Q / 1Q27 (its own statement; no Search field in our snapshot) | **The 1Q27 +4% is the outlier.** Wells calls the cause structural (AI Overviews), not macro, and sees no recovery before 2Q27. That contests management's FX framing. Watch for 4Q paid clicks ≤+4%. |
| **GOOG** | PT **$371 → $365** (25x FY27 EPS), Overweight; upside / downside scenarios $421 / $243 (Wells, 11-01) | Wells' last mark on the page was $417 (10-06); the $371 (10-29) was never logged. Both are now in the Changelog | — | cons PT **$399.5** (hi $475 / **lo $350**, n=17) → Wells is **−8.6%** vs the median and near the low end. Price $278.04 → **+31%** upside | The low end of the panel is still Overweight, so the Street has no bear PT. |
| **GOOG** | EPS 2027E **$14.60** (from $14.84); FY28E $17.79 (Wells, 11-01) | — | house 2027E EPS **$16.20** → Wells **−9.9%** | BBG 2FY EPS **$15.88** → **−8.0%**. Wells' own VisibleAlpha consensus is $15.05 | ⚠️ **This is mostly a basis effect, not an operating miss.** Wells' **EBIT 2027E $213.7bn vs BBG 2FY $215.6bn is −0.9%**: in line. The EPS gap sits below the line (the OI&E equity marks; see memory `bbg-eps-below-the-line-contamination`). **Reconcile at EBIT.** The real call is the Search cut above. |
| **OPENAI / ai-compute-deals** | **Project Camellia**: Effingham County, GA; **3.2 GW** power commitment, implemented 2028-2032; up to 1 GW curtailment; Georgia Power says OpenAI pays for the infrastructure; Georgia's governor race is a risk (SemiAnalysis, 11-01) | 🆕 not on the page. It may be the same project as the 10-28 Savannah watch item (UNCONFIRMED, kept separate) | — | — | New ID **OAI-GAPOWER-CAMELLIA**, recorded as a utility power commitment, not compute. It is the first site-specific election risk on the page. |
| **ai-datacenter-power** | US 2028 net additions **62.2 GW**, mostly not started. 13 states = 43.5 GW (70%), 10 of them electing a governor on 11-03. The Texas TCEQ freeze is the biggest single risk (TX 18 GW = 41.3% of the 13 states); ERCOT report targeted for Dec 10 (SemiAnalysis, 11-01) | The same team called 2028 *oversupply* "the main risk" on SemiAnalysis Weekly Ep. 039 (10-20). Now the 2028 risk is **permits delaying supply**. Both views are kept and flagged | — | — | The 2027 leg is locked in (~3/4 of 33.8 GW under construction; global +50 GW confirmed). **The 2028 capex leg now carries a permitting-timing risk**, which also bears on AMZN (Ohio / Pennsylvania) and GOOG (Goodnight's generation permit is pending). |
| **AMZN** | Ohio becomes AWS's largest state outside Virginia by 2028; AWS is ~44% of Pennsylvania's 2.4 GW of 2028 additions (≈1.05 GW, Capstone arithmetic), including the Anthropic campus at Susquehanna (SemiAnalysis, 11-01) | Management: AWS growth "over 40%" in 2027 and 2028 | none | — | ⚠ nuance on the 2028 leg (page Sinal). Not an estimate change. |
| **tokenmaxxing** | Global average **~100,000 tokens/month per capita**; the "token leader" uses ~500bn/month (Altman @ ADIPEC, 11-02 — exec, on stage) | That implies ~0.8 quadrillion/month (**Capstone arithmetic**, ~8bn people) vs **~35 quadrillion/month** (AMD, 07-23) and >30 quadrillion (Exponential View, 06-25) | — | — | About 40x apart. **The bases almost certainly differ** (human/ChatGPT use vs all API and agent traffic). Do not reconcile, and do not chain into a series. |
| **CSCO** | "More engineers in two years than less" (Patel @ UC Irvine CDT, posted 11-02; recording ~09-09/10, UNCONFIRMED) | vs the ~4,000-job (~5%) Q3 FY26 restructuring on the page | none | — | Tone divergence only: a stated belief, no number. |

## CONFIRMS (no action)

| Name | Datapoint | Baseline | Result |
|---|---|---|---|
| GOOG | Wells EPS 2026E **$19.46** (from $19.50); revenue 2026E **$502.97bn** | BBG 1FY EPS **$18.59**; house revenue 2026E **$505bn** | EPS +4.7% vs BBG (2026 includes actual OI&E gains, so the basis is noisy); revenue **−0.4% vs house**. ⚠️ BBG 1FY revenue $434bn is on a different (net) basis: an artifact, not a divergence |
| GOOG | Wells revenue 2027E **$695.6bn** | house **$641bn**; BBG 2FY $565bn (net basis) | +8.5% vs house on the same gross basis. The house model is from 2026-06-05, before the Cloud/TPU re-rating, so this points to a stale house model rather than to Wells; flag it for the next house update |
| GOOG | Sessions (Google + Gemini) +36% y/y in 3Q | management: record query growth | ✅ ties ("aligns", per Wells) |
| CSCO | AI hyperscale **orders** $2.3bn (FY25) / $9.3bn (FY26), "orders take a while to get to revenue" (Patel) | page FY26 $9.3bn orders; 10-29 A Bit Personal row | ✅ identical; the moderator's "$9 billion plus revenue" was his own wording |
| CSCO | 70% of the portfolio 100% AI-written by end of next year; ~$63bn revenue | FT 2026-09-24 ("software products"); FY26 guide $62.8-63.0bn | ✅ |
| CSCO / tokenmaxxing | 60% of compute consumed in inference by end-2026 (Patel) | AMD ~60% (07-23) | ✅ (no basis given) |
| OPENAI | Millennium-Prize run: 10,000 agents for "about 4 days" (Altman) | 10,000 agents / 88h (Axios via MS, 09-09) | ✅ (≈96h at his rounding). 🆕 the "next GPT… released soon" signal, with no date |
| OPENAI | ADNOC–G42 "OpenAI Frontier" agreement (the moderator's words) | no G42 / Stargate UAE deal ID | **no $ / MW / terms**, so a watch note only, no deal ID |
| BKNG | Capstone house 3Q room nights **~6% (calculation) / 6.5% (house)**; bogey **5-6%** (from the 10-30 buy-side +4-5%); expected 4Q guide +3-5% (Capstone "Preview Travel 3Q26", 2026-11-02) | 10-30 house bar (now in the Changelog); BofA's expected 4Q guide +3-5% (10-25) | BBG has no room-night field. Q3 cons rev $9,544m / EPS $4.493; **4Q cons EPS $2.301** | The house sits above the bogey. The 4Q guide expectation matches BofA's. Circular risk: the house doc partly draws on the wiki |
| BKNG | Hotel 3Q: Marriott RevPAR +6.5% vs a +3.5-4.0% guide; 5 of 6 chains raised FY; October RevPAR MTD US +9% / Europe +5% | demand ✓ on the page | ✅ demand. ⚠ the Europe gains are price-led. The 27% French-cancellation figure is UNCONFIRMED |
| ai-datacenter-power | Global 2027 +50 GW | SemiAnalysis Weekly Ep. 039 "fifty gigawatts" | ✅ (now explicitly global) |
| LITE / MRVL | Bernstein "The deal is real; earnings beat" (title only) | definitive agreement already on both pages from the primary (11-02) | no numbers; full note queued in `_inbox/PENDING_FULL_REPORTS.md` |

## Qualitative only (not reconciled)
- a16z/Eve: the labor → token reallocation (about half of a ~⅓ contingency fee); 100 → 500 clients per attorney at one firm; seat → outcome pricing. These are company or VC claims, unaudited.
- Patel: agents at 5x human token use (no source given); Cisco as Codex's first design partner; 90,000 employee agents. Logged, not modelled.
