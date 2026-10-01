# Morning analyst source checks for 30 September 2026

Research cutoff: pre-US-market morning, America/Sao_Paulo. Selective event and model checks, not a complete overnight inbox or filing audit. No company pages, house estimates, or canonical assumptions edited.

## Signal snapshot comparison

build_analyst.py completed on 2026-09-30: 85 active signals, 5 high, 43 focus names, 0 belief changes. Prior saved daily history (2026-09-29): 91 active, 7 high, 45 focus, 3 belief changes. No added IDs.
Removed IDs: beli-7bb92a0aa39e (META); beli-eadc1630c9a3 (RDDT); beli-7116cc7a997e (SHOP); cata-ea28e3f17616 (META enterprise-platform date); cata-b3f9e760f403 (MDB Investor Day); cata-c1c11b199fbb (CRWV conference September 29 through October 1).
Surviving fields compared: title, why_now, belief_update, source, priority, event_date. Changes limited to priority: GOOG cata-00a12a4ae7d5 medium to high; META reco-efc1dbae5cee high to medium; KIOXIA cata-8ac5e497f97b watch to medium. These are ranking changes, not new evidence.
Latest reconciliation still reconciliation-2026-09-28-inbox.md. Book asof July 1 is seed true with null weights.

## MDB original broker research read in Outlook

- UBS Karl Keirstead / Jack Fyda, report dated 2026-09-29, email received 2026-09-30 00:48 BRT, "MT Growth Guidance of 20%+" (Neutral). Full research email body read; linked PDF not opened.
  URL: https://outlook.cloud.microsoft/mail/id/AAQkADllY2NkMmU1LTc3YTEtNGRkMC1hMjBkLWU1NjIzOTY5OTZhMQAQADH4RdBQrxpCgwN8o9OzeTA%3D
  UBS relays new roughly three-year targets: Atlas mid-20s growth versus prior 20%+; total revenue 20%+ versus high-teens; annual non-GAAP operating-margin expansion maintained at 100–200bp. It raises growth estimates but cuts PT $410 to $375 as CY28 EV/sales goes approximately 7.5x to 6.5x. FY30/CY29 growth estimates now Atlas 23% / total 20%. Neutral retained. AI-native cohort described inconsistently as Atlas ARR then revenue in the email; its small-cohort metrics were excluded from the brief rather than conflated.
- Barclays Raimo Lenschow / Sheldon McMeans, body dated 2026-09-29, released 2026-09-30 02:36 GMT, received September 29 23:37 BRT. "Investor Day - Evolving AI Story, But Uncertainty Post-CEO Departure Still Tangible."
  URL: https://outlook.cloud.microsoft/mail/id/AAQkADllY2NkMmU1LTc3YTEtNGRkMC1hMjBkLWU1NjIzOTY5OTZhMQAQAETiNg%2B0K6pKms1PTioweP0%3D
  Email is an excerpt, not the full report. OW / PT $480 retained. Positive product and financial-target discussion offset by concern about the future of executives hired by the departed CEO. No estimate revision inferred from the truncated preview.
- Vital Knowledge / Adam Crisafulli, September 29 post-close company news, received 18:55 BRT.
  URL: https://outlook.cloud.microsoft/mail/id/AAQkADllY2NkMmU1LTc3YTEtNGRkMC1hMjBkLWU1NjIzOTY5OTZhMQAQAJWmFGBIKhtEqsNuKwJNGmk%3D
  Says $1bn added to buyback, "total" $1.35bn. Checked against the reproduced company 8-K: aggregate authorization $2bn; remaining authorization $1,353,700,000. Do not label remaining as aggregate or authorization as executed purchases. Board action September 25, filing September 29. Buyback left out of main brief to prioritize operating-model debate.

## MDB company sources and source limits

- September 28 CEO transition: https://investors.mongodb.com/news-releases/news-release-details/mongodb-announces-ceo-transition
  Desai stepped down immediately for a senior role at Meta; Dev Ittycheria interim CEO; permanent search initiated; Q3/FY27 guidance reaffirmed on September 28.
- September 29 product release: https://investors.mongodb.com/news-releases/news-release-details/mongodb-launches-mongodb-90-best-version-ever-built-and-atlas
  MongoDB 9.0 GA; Atlas Infinite public preview on AWS, compute/storage separated, consumption-based pricing rather than capacity provisioned for peaks. This supports the research question about workload expansion versus optimization, not a revenue forecast.
- Company 8-K reproduced at https://www.stocktitan.net/sec-filings/MDB/8-k-mongo-db-inc-reports-material-event-9849865060d6.html
  Read original Item 7.01/8.01 body (not relying on the website's generated interpretation). Company deck is furnished, not deemed filed. Buyback scope checked as above. Direct SEC retrieval attempted but unavailable. Full deck and webcast not reviewed; no new margin endpoint adopted.

## Today and tomorrow calendar

- MU company August 26 announcement: https://investors.micron.com/news/press-release/2026/Micron-Technology-to-Report-Fiscal-Fourth-Quarter-Results-on-September-30-2026/default.aspx — September 30, 2:30pm Mountain / 4:30pm ET call.
- HPE September 3 announcement: https://www.hpe.com/us/en/newsroom/press-release/2026/09/hpe-to-webcast-networking-investor-day-event.html — September 30, 8:30am PT / 10:30am CT.
- SNPS official notice: https://investor.synopsys.com/news/news-details/2026/Synopsys-Announces-Earnings-Release-Date-for-Third-Quarter-Fiscal-Year-2026/default.aspx — September 30 Investor Day. 1pm ET time is sourced separately to BofA/Fenske relaying Arya, September 27, _wiki/SNPS.md, not claimed as verified on the official event page.
- Apple developer terms, August 18 update, retrieved September 30: https://developer.apple.com/support/apps-in-the-eu — October 1 effective date; standard IAP 26%, alternative in-app 20%, actionable link-out 15%, exceptions apply. Outside-App-Store CTC 5% is a separate distribution basis. Not a blended take-rate estimate.
- GOOG October 1 Suncatcher event remains a NYT via 22V/Peterson September 24 relay; launch confirmation was not independently verified in this run.
- CRWV September 29–October 1 conference remains in progress on the source calendar although date-filtered signal expired. No outcome inferred.

## Local model and narrative checks

- Read current MU, SNPS, HPE, MDB, AAPL and GOOG Debate/Changelog material relevant to selected questions. Post-ECOC LITE/CRDO transcript had been read directly in the immediately preceding research turn; it is carried context, not newly received September 30 evidence.
- MU _wiki/MU.md lines 826–831: JPM Sur Sept28 Street Nov $56.3bn/$35.71; MS Moore Sept28 realized like-for-like pricing +10–12% vs starting contract discussion +15–20%; Barclays Rand Sept28 buy-side November EPS $38–39. Distinct panels and bases preserved. Latest subject:Micron Outlook search Sept29–30 produced desk relay/event invitations and internal work, not a newly reviewed covering-analyst earnings preview.
- SNPS _wiki/SNPS.md lines 172 onward: BofA/Arya through Fenske Sept27 targets are broker upside scenarios, not company targets; MS/Simpson Sept24 requires execution beyond LT-target increases; HSBC Sept25 upgrade remains a desk relay with analyst unnamed.
- HPE _wiki/HPE.md line 291: BofA Mohan Sept28 Helios range is switches versus full-rack scope, not comparable orders. No company guide adopted.
- GOOG house.json checked directly: years.2026.fcf=3 and years.2027.fcf=55, but raw_rows FCF=-3/-55 and _wiki/GOOG.md house-model row also negative. Revenue $505/$641bn from June 5 house versus Sept29 BBG $427.3/$544.1bn. No repair made.
- AAPL EPS house June16 $10.12 versus Sept29 BBG $8.76 requires FY/CY check. Bernstein Newman Sept25 December EPS $3 to $2.87 is a distinct, dated estimate revision.
- Read reconciliation-2026-09-28-inbox.md. Its AVGO headline wrongly describes AI revenue above BBG total revenue; the body instead compares house TOTAL $115/$190bn with BBG TOTAL $106/$173.9bn and house AI with GS AI. Not repeated as a valid investment signal. Fiscal/calendar mapping remains open.
- The reconciliation's RDDT expert wallet-share growth is not like-for-like with company revenue growth; not adopted as a shortfall forecast.

