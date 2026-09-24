# Morning Analyst Inbox — 2026-09-23

Today's focus: LITE/COHR and META first; GOOG data reconciliation next; MSFT/ORCL and NVDA for the financing debate. Research priorities, not trade instructions. Book prioritization is provisional: book.json remains a July 1 seed with unknown weights.

## Five priority ideas

1. LITE/COHR: fresh ECOC evidence supports optical content, but narrows the OCS extrapolation.

Broker evidence: Morgan Stanley's Meta Marshall / Antonio Jaramillo, September 23, report greater confidence in first-generation NPO adoption/trials in parts of scale-up networks in 2028, with many suppliers sold out for 12–18 months and InP substrates the main constraint. Early external-laser architectures support LITE/COHR. However, MS expects later OCS customers to be smaller than Google and mentions an unnamed cancellation after qualification. MS explicitly did not meet LITE; this is not a new LITE management guide. No direct CRDO post-meeting recap was verified in this check.

Inference/action: prioritize LITE's Google OCS conversion and high-power laser execution, not a blanket multi-hyperscaler OCS uplift. Obtain direct LITE/CRDO meeting recaps before changing estimates; test CRDO optical qualification/ramp timing separately from NPO. Falsifier: architectures bypass external lasers, or supply/order conversion disappoints.

Signal: manual-ecoc-20260923-ms (editorial supplement); follow-ups to archived cata-3194d63aa353 / cata-cbe6366939c9. Evidence: _wiki/_meta/analyst-evidence/2026-09-23-ms-ecoc.md.

2. META: Connect must turn product enthusiasm into measurable earnings evidence.

Documented broker revision: Wells Fargo / Ken Gawrelski, September 20, raised its target to $796 from $640 while lowering 2027 EPS to $31.86 from $32.07; its valuation multiple rose to 25x from 20x. The September 21 reconciliation shows the FY27 operating-profit gap to that day's Bloomberg consensus was much smaller than the EPS gap. This is principally a re-rating thesis, not an earnings upgrade.

Inference/action: before Connect, freeze expectations for retained usage, paid conversion, transaction economics and operating-cost commitments. Distinguish a demo from monetization. Falsifier of the valuation-led reading: disclosed paid adoption supports material operating-estimate upgrades rather than only higher multiples.

Signals: reco-ddd0bbcca0d3; cata-a2fece2adf44. Evidence: _wiki/_meta/reconciliation-2026-09-21.md; relatórios bons/b13ae3c4-1f51-4b58-ab2c-f5c5e155f477.html (primary, p1 checked).

3. GOOG: repair a confirmed FCF sign mismatch before trusting the model screen.

Hard local evidence: the Capstone model table dated June 5 shows 2026/2027 FCF of -$3bn/-$55bn. September 22 house.json preserves those negatives in raw_rows but publishes +3/+55 in parsed fields. Separately, house revenue is $505bn/$641bn versus September 22 Bloomberg CY consensus of $427.3bn/$544.1bn, while displayed 2027 house EPS of $16.20 is below the latest CY consensus $16.60. Higher revenue does not automatically mean an EPS edge; the old page claim of EPS above consensus needs refreshing after basis checks.

Action: verify the original workbook, repair/test extraction, then bridge gross/net revenue, margins, tax and share count. No model change justified yet. Falsifier: the workbook establishes a different valid basis or supersedes the wiki table; that determines which representation is wrong.

Signals: esti-bf7122f00934 / esti-56921f2baecc; manual-goog-fcf-sign-20260923 (editorial supplement). Evidence: _wiki/GOOG.md; _wiki/_data/house.json; _wiki/_data/estimates.json; _wiki/_meta/analyst-evidence/2026-09-23-goog-fcf-sign.md.

4. MSFT/ORCL: test returns on capacity, not simply demand growth.

Broker evidence: Goldman / Gabriela Borges, September 20, reiterates MSFT Buy/Conviction List, $640, after management meetings; Redburn / Alex Haissl and Luke Han, September 21, carries Neutral/$440. Redburn models FY29 Azure revenue at $253.1bn versus its cited consensus $296.0bn. For ORCL, its same-basis FY29 operating profit is 14.6% below Visible Alpha despite revenue only 2.8% below. These are correlated financing/margin views, not independent bearish votes.

Action: build one capacity-to-revenue and lease-to-cash-flow bridge; keep ORCL GAAP and adjusted earnings separate. Falsifier: utilization, cloud margins and lease-inclusive cash generation improve together enough to close the out-year gaps.

Signals: reco-604281b7c03c / reco-c77e0919e898 / reco-3df2752f1ae2. Evidence: _wiki/_meta/reconciliation-2026-09-21.md; relatórios bons/Capital_Carousel.html.

5. NVDA: separate reported growth from customer-funding quality.

Broker estimate, not company disclosure: Redburn's Timm Schulze-Melander, in Capital Carousel dated September 21, estimates $126.5bn, or 33% of FY27 data-center revenue, as vendor-stimulated demand. Importantly, he remains Buy/$325 and models the share fading to about 6% by FY29: the report is not forecasting that all stimulated sales disappear.

Inference/action: track customer self-funding, backstop use and cash conversion before imposing an EPS haircut. This challenges durability and valuation more directly than near-term shipment estimates. Falsifier: independent customer cash generation grows and funding dependence declines along the broker's projected path.

Signal: reco-32e2a145dcb3. Evidence: relatórios bons/Capital_Carousel.html, pp133–134 checked; _wiki/_meta/reconciliation-2026-09-21.md.

## Other model conflicts and catalyst preparation

- AAPL: Capstone's June 16 model has 2026 EPS $10.12 versus September 22 Bloomberg $8.76. Reconcile fiscal/calendar periods and adjusted/diluted definitions before calling this upside. Signal esti-b1a3e9a61c68; evidence _wiki/_data/house.json and _wiki/_data/estimates.json.
- September 23–24: META Connect; pre-write the adoption/monetization scorecard above (Wells Fargo, September 20). GOOG's September 23 AI Agenda event is listed from The Information's August 6 announcement: reconfirm the schedule and look for internal-versus-merchant compute allocation, not just model benchmarks. Signals cata-a2fece2adf44 / cata-dce3c37069bc; evidence _wiki/META.md and _wiki/GOOG.md.
- September 24: the wiki flags Trump–Xi headline risk from UBS / Timothy Arcuri, August 31. Treat this as a calendar item requiring fresh confirmation; prepare both restriction and easing scenarios for NVDA/TSM. Signals cata-eb95103055e4 / cata-c34f156a3a81; evidence _wiki/NVDA.md and _wiki/TSM.md.

## What changed versus yesterday

Generated history comparison: 108 to 90 active signals; seven high-priority signals unchanged; no new generated IDs, no changes to retained numeric values, and zero detected belief changes. Five September 22 catalysts expired and thirteen September 1 findings crossed the engine's 21-day carry-forward limit. Neither expiry proves resolution. Sources: _wiki/_data/analyst/history/signals-2026-09-22.json; _wiki/_data/analyst/signals.json; _wiki/_tools/build_analyst.py.

The substantive additions from this run are the September 23 MS ECOC first take and the newly verified GOOG FCF sign mismatch. They are editorial supplements, not changes already captured by the engine. Latest full reconciliation remains September 21; Bloomberg snapshot is September 22. No full overnight inbox ingestion or company-page edits were performed.
