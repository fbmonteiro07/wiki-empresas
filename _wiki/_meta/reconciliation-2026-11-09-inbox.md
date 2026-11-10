# Reconciliation — /run-inbox 2026-11-09

_This report checks each new quantitative datapoint from tonight's sources against three baselines: (1) prior wiki marks; (2) Capstone house models; (3) BBG consensus._

- **BBG is LIVE.** Pulled tonight (~23:50) with `bdp`: `PX_LAST`, `BEST_TARGET_PRICE`, and `BEST_EPS` / `BEST_SALES` / `BEST_OPP` / `BEST_CAPEX` / `BEST_EBITDA` at `BEST_FPERIOD_OVERRIDE` 1FY/2FY/3FY (calendar FY26/27/28 for every name below). The on-disk snapshot `estimates.json` is also dated 2026-11-09.
- **Sources with numbers:** Morgan Stanley "Memory – Key Debate Post Mid-terms" (Shawn Kim et al., 2026-11-09); CEG Q3 2026 call and NRG Q3 2026 call (both 2026-11-09); The Information on Meta enterprise sales (2026-11-09); UBS "Midterm Election Impact on AI Build-Outs" (2026-11-08; MW lists only, no estimates).
- **No new numbers:** the Lip-Bu Tan CASPA fireside and the Zscaler CEO interview (qualitative; ZS "$10bn+" ARR is a CEO confidence statement vs a >$8bn Investor-Day base case, logged on the ai-cybersecurity theme).
- **House models:** none for SK hynix, Samsung, CEG or NRG. META has one (FY26 capex $150.7bn).
- KRW figures: BBG returns millions; converted to trillions (tr) below.

## DIVERGES (the alpha)

| Name | New datapoint (source) | vs prior wiki | vs house | vs BBG (live 11-09) | Read |
|---|---|---|---|---|---|
| SK hynix | PT **W1,600,000** (OW) (MS, 11-09) | MS W2,600,000 (05-18 / 07-02 / 08-19) | n/a | cons PT **W3,144,512**; px W1,210,000 | MS is ~49% below the consensus PT while staying OW; the cut is pure multiple (long-run HBM margin ~70% vs 78-80% prior), not estimates. |
| SK hynix | OP FY28e **W472.8tr** (MS) | note's prior W468.2tr | n/a | cons 3FY OP **W547.1tr** | MS ~14% below consensus on 2028 operating profit — the "2028 earnings cliff" is exactly where MS sits below the Street. FY26/27 OP (W285.8tr / W467.9tr) are in line with cons W282.5tr / W473.5tr. Caveat: cons 3FY EPS (W654,010) is in line with MS (W652,384) despite the OP gap → the BBG EPS and OP panels differ; reconcile at OP. |
| Samsung Elec. | PT **W309,000** common / W247,200 pref; new MS Top Pick (MS, 11-09) | MS W381,000 (08-21) / W304,800 (08-19) | n/a | cons PT **W480,344** (pref W335,300); px W199,400 | Same shape: Top Pick with a PT ~36% below consensus. |
| Samsung Elec. | OP FY27e **W688.0tn**; EPS FY27e **W85,656** (MS) | MS model 08-07: W629.0tn; note's prior EPS 73,569 | n/a | cons 2FY OP **W623.3tr**, EPS **W77,591** | MS ~10% ABOVE consensus on 2027 OP/EPS. FY28 OP W690.4tn ≈ cons W694.8tr. MS is bullish 2027 and flat-to-cliff 2028. |
| Samsung Elec. | Capex FY28e **W94.2tn** (MS) | none | n/a | cons 3FY capex **W118.1tr** | MS ~20% below consensus on 2028 capex while its debate is a 2028 supply response — internally consistent only if MS sees Samsung's own capex peaking in 2027 (W100.0tn). Worth checking the bridge. |
| CEG | FY26 adj. EPS guide raised & narrowed to **$12.50-12.80** (CEG Q3 call, 11-09) | $11.00-12.00 (Q1, 05-11) → $11.50-12.50 (Q2, 08-06); Bernstein 2026E $11.82 (10-06) | n/a | cons 1FY **$12.10** | Midpoint $12.65 is ~4.5% above consensus; the BOTTOM of the new range is above consensus → expect upward revisions. Cons 2FY $13.43 / 3FY $16.91. Cons PT $347.57 vs px $276.09. |
| NRG (no page) | 2027 guide midpoints: adj. EPS **$9.05**, adj. EBITDA $5.75bn, FCF before growth $3.15bn — existing portfolio, excluding the LS Power asset sale (NRG Q3 call, 11-09) | no page | n/a | cons 2FY EPS **$10.24**, EBITDA **$5.82bn** | EPS guide ~12% below consensus while EBITDA is only ~1% below → the gap is below EBITDA (D&A/interest/share count, or consensus already including buyback/asset-sale effects). Logged on ai-datacenter-power; no page to patch. |

## CONFIRMS (no action)

| Name | New datapoint (source) | vs prior wiki | vs house | vs BBG (live 11-09) | Read |
|---|---|---|---|---|---|
| SK hynix | EPS FY26/27/28e W356,482 / W550,275 / W652,384; sales W365.2tr / W585.2tr / W648.7tr (MS) | note's priors 361,277 / 451,280 / 506,170 | n/a | cons EPS W359,712 / W537,988 / W654,010; sales W359.6tr / W586.6tr / W699.9tr | EPS in line all three years; 2028 sales ~7% below cons (consistent with the OP gap above). |
| SK hynix | Capex FY26/27/28e W46.6tn / W76.1tn / W84.3tn (MS) | none | n/a | cons W47.5tr / W67.8tr / W80.4tr | In line / modestly above in 2027. |
| Samsung Elec. | Revenue FY26/27/28e W744.1tn / W1,159.5tn / W1,251.0tn; OP FY26e W397.0tn (MS) | MS 08-07 W729.3 / 1,059.4 / 1,141.2tn | n/a | cons sales W724.3tr / W1,025.9tr / W1,182.0tr; OP 1FY W385.0tr | Above consensus but consistent with the OP call; 2026 in line. |
| META | Capex "as much as $145bn" this year (The Information, 11-09) | guide $135-145bn (10-21, incl. finance-lease principal) | house FY26 **$150.7bn** | cons 1FY capex **$139.7bn** | The article quotes the TOP of the company guide; not new information. House sits above both the guide top and consensus — the existing house-vs-guide gap (finance-lease basis) stands. |
| CEG | Contracted >8,500 MW YTD; ~1,200 MW uprates for ~$4.3bn; ~$3bn buyback since March (CEG Q3 call) | Calvert Cliffs 690 MW (10-01); ~900-1,000 MW uprates (Q3'25) | n/a | n/a | Consistent with the page's direction; the uprate MW is up vs prior. Google MW on the 4,560 MW is an inference (Bernstein 3.6 GW + 690 + 270), flagged on the page. |

## No baseline (logged only)

- UBS MW lists (Figures 1-5, read from the page images): MSFT 8,058 MW, GOOG 10,463 MW, AMZN 21,830 MW, ORCL 7,192 MW, CRWV 1,684 MW of large projects; not-started Texas = Pecos/Kilby 2,000 MW (MSFT) and GW Ranch 5,000 MW (AMZN). "Proposed power" mixes MW bases (CRWV Helios 526 MW = IT vs 800 MW gross) — never sum against IT-load GW series.
- UBS industry checks (Texas power 3 GW 2022 → ~40 GW; >500 moratoria; 54 GW utility contracts + 30 GW queue; 6.8 GW PJM backstop) — third-party relays, logged on ai-datacenter-power.
- MS/TrendForce 2027 HBM share: Samsung ~39% / SK hynix ~37% / Micron ~22% — first time on the wiki.
- INTC: ASIC, physical AI and advanced packaging each a "10% revenue" opportunity (Tan, no year, no $). ZS ARR "$10bn+" (CEO) vs Investor Day >$8bn base case.
