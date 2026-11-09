# Reconciliation — /run-inbox 2026-11-08

_This report checks each new quantitative datapoint from tonight's sources against three baselines: (1) prior wiki marks; (2) Capstone house models; (3) BBG consensus._

- **BBG live is OFFLINE.** The `bdp` call failed with `127.0.0.1:8194 connect event failed`, meaning the Terminal is not logged in. The BBG column therefore uses the **on-disk snapshot** (`_wiki/_data/estimates.json` and the PANW page block, asof **2026-11-06**). That is a valid same-week baseline. There is no web substitute.
- **Tonight's only new source with content is a podcast:** Nikesh Arora (PANW Chairman & CEO) on the David Senra podcast. It was posted 2026-11-08; the recording date is not stated (~10-20/21, inferred from the PHP-week references). It has no rating, PT, EPS or guidance, and every figure is the CEO's own illustration.
- **No content patched from the rest:** two backfill summaries (All-In 11-07 → NVDA; the Tan fireside → CDNS/CEREBRAS/CRDO/MRVL) were re-checked in the transcripts and stay passing mentions. Three Notion "Resumo" PDFs (JPM hyperscalers 11-04, NH Korea 11-04, CyberEdge 11-05) are AI summaries of calls whose transcripts were ingested and reconciled on 11-06 (`reconciliation-2026-11-06-inbox.md`). They are not new primaries, so they are not re-reconciled.
- **House models:** PANW has no house model (none in `Modelos oficiais`; no `## Capstone estimates` block on the page), so that column is n/a.

## DIVERGES (the alpha)

| Name | New datapoint (source) | vs prior wiki | vs house | vs BBG (snapshot 11-06) | Read |
|---|---|---|---|---|---|
| **PANW** | **"40% operating margin business"**: the framework is to cut S&M plus support from ~60% of cost to 20, with R&D at 15-18% and G&A at 6-10% (Arora on David Senra, posted 11-08) [00:09:51] | Non-GAAP OM was **29.2%** in FY26; the F1Q27 guide is **29.5%**; MS's FY27 preview has **30.4% vs Street 29.6%** (page) | n/a | Cons EBITDA/revenue CY27 $5.3bn / $15.1bn ≈ **35% EBITDA margin** (house arithmetic, EBITDA basis, not OM) | **~10pt gap between the stated aspiration and both the actuals and consensus.** It is his 2018 plan framework with no timeline, and M&A (CyberArk, Chronosphere) is diluting the >30% streak. Do NOT treat it as guidance. It is a long-run marker to hold against the S&M leverage line on future prints. |
| **PANW** | **Endpoint economics v3:** *"25 bucks a year"*, *"150 megabytes a day"*. AI would cost *"$5,000 a day… $500… $50 a day"* [00:57:10]–[00:57:46] | GS 09-10: industry $30-40/endpoint, 160 MB/day, an LLM costs >$40/yr. All-In 10-21: $20/yr, "hundreds of megabytes" | n/a | n/a | **His own numbers move from one appearance to the next:** price $20 → $25 vs a $30-40 industry average, and the AI comparator from >$40/yr to $50-5,000/day. Traffic is stable at 150-160 MB/day. The bull case's unit-cost leg is still CEO illustration, not disclosure. ⚠ The podcast summary's "20-40 MB vs 150 MB" divergence was wrong: on 10-21 the 20-40 MB was the on-endpoint model payload. |
| **PANW** | *"Our business has gone up since Mythos came in"* [00:57:10]. Qualitative, no metric | The page carried the Mythos effect as meetings and pipeline (~2,000 briefings, Prisma AIRS ~$120M ARR, WFC partners above plan) | n/a | Cons revenue CY26 $13.0bn → CY27 $15.1bn (+16%) | **Untestable until the F1Q27 print (~2026-11-18).** Q1 guide revenue $3,300-3,310M; NGS ARR and AIRS are the lines to watch. Logged as a management claim, not evidence. |

## CONFIRMS (no action)

| Name | Datapoint | Baseline | Result |
|---|---|---|---|
| PANW | *"we buy 35 companies"* [00:17:19] | U-M lecture 10-22 "35 plus"; GS 09-10 "47 acquired" (different count basis, already flagged on the page) | ✅ consistent with U-M |
| PANW | 2018 market cap *"$18 billion"* → aim *"north of 100"* [00:09:00] | U-M 10-22 (page) | ✅ same |
| PANW | Virtual patching as the PHP-week product [00:57:10] | WFC "Patch Notes" 10-25 (patch ~9 hrs before the vendor's) | ✅ qualitative confirm |
| ai-cybersecurity | "The products that will secure AI don't exist fully yet" [00:41:55] | GS 09-10: the AI-security industry "has still to be built" | ✅ same line |

## No baseline (logged only)

- Target valuations *"three times or four times more expensive"* than 2 years ago [00:31:58]. There is no private-market valuation baseline on the wiki.
- *"6,000 people in the field"* [00:24:52] and *"70 plus products"* [00:07:20]. Not previously on the page as numbers.
- Cyber split ~50% perimeter / 10-20% hygiene / 20-30% detect-and-respond [00:55:10]–[00:55:51]. This describes the job, not a spend split, so it does not reconcile against any TAM.
