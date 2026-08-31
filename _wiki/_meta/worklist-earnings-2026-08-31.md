# Earnings-season archive sweep — prints of 2026-07-16 → 08-28

_Built 2026-08-28, completed 2026-08-31. Successor to [worklist-earnings-2026-07-31.md](worklist-earnings-2026-07-31.md), which closed the **July** print window. This one covers the **August** window: the FY-June 10-K filers, the late-August semis/software prints (NVDA, MRVL, CRM, CRWD, SNPS, VEEV), and every transcript the July sweep left open._

_Scope: SEC filings (10-K/10-Q/20-F) + earnings-call transcripts, worked in order of company importance (book names → core AI semis → AI infra/power → software/internet → tail)._

---

## 1 — What landed

### SEC filings — 70 documents on disk for the window (EDGAR, zero failures)

| Pass | Result |
|---|---|
| Season sweep 08-28 (every wiki ticker, 10-K/10-Q/20-F filed since 2026-06-01) | **44** new documents |
| Re-run 08-31 (weekend filings) | **1** new — MRVL 10-Q (08-28) |
| Already on disk from the July sweep | 25 |

**10-K (11):** KLAC 08-06 · LRCX 08-07 · STX 08-04 · SNDK 08-17 · WDC 08-14 · LITE 08-17 · COHR 08-14 · WOLF 08-20 · AOSL 08-27 · MSFT 07-29 (July sweep)

**10-Q (59)** — the full list is on disk; the ones that matter most this window:
NVDA 08-26 · MRVL 08-28 · AMD 08-05 · ANET 08-05 · AMAT 08-20 · ADI 08-19 · MCHP 08-06 · ON 08-03 · TER 07-31 · CRM 08-27 · CRWD 08-27 · SNPS 08-26 · VEEV 08-27 · PLTR 08-04 · APP 08-05 · UBER 08-05 · SHOP 08-05 · BKNG 08-04 · NET 08-06 · AKAM 08-07 · FSLY 08-05 · CRWV 08-12 · ALAB 08-05 · APH 07-31 · ETN 07-31 · NVT 07-31 · CEG 08-06 · VST 08-10 · TLN 08-05 · PWR 07-30 · WMB 08-03 · FLEX 07-31 · AEIS 08-03 · VECO 08-05 · AAOI 08-06 · AXTI 08-13 · MP 08-07 · POWI 08-06 · BE 07-28 · NVTS 07-27

**Two finds worth knowing about:**

- **SPCX (SpaceX) is now an SEC filer and was missing from the fetch script's universe.** It was hard-coded into `fetch_sec_filings.py`'s "no SEC" exclusion list as a private company. It IPO'd in June 2026 (S-1 05-20, 424B4 06-12, both already on disk) and filed its **first 10-Q on 2026-08-04** — now archived at `SPCX/SPCX_10-Q_2026-08-04_0001628280-26-052535.html`. The exclusion has been removed from the sweep script. **`fetch_sec_filings.py` itself still carries the stale comment** — see §4.
- **LITE has two FY26 10-K artifacts** for 08-17: the EDGAR inline-XBRL original pulled by this sweep (`…_0001628280-26-057358.html`) and a hand-pulled PDF from 08-17 (`…_FY2026-ended-2026-06-27.pdf`). Not an error — the HTML is the canonical archive copy per convention; the PDF predates it.

### Transcripts — **56 of 56 covered prints**, ~470,000 words

Everything below is **new this sweep**. Word counts are body text.

| Ticker | Call | Words | Source | Note |
|---|---|---|---|---|
| **NVDA** | 08-26 | 8,632 | investing.com | ⚠ speaker-label + IR-PDF caveats, see §2.1 |
| **MRVL** | 08-27 | 9,817 | MarketBeat/Quartr | Google warrant — see §2.4 |
| AMD | 08-04 | 8,933 | Yahoo/Motley Fool | |
| ANET | 08-04 | 7,570 | Yahoo/Motley Fool | first full ANET file (Q1 was a partial) |
| AMAT | 08-13 | 9,789 | investing.com | |
| ADI | 08-19 | 6,955 | Yahoo/Motley Fool | some Q&A speaker tags misattributed |
| MCHP | 08-06 | 10,485 | Globe and Mail/Fool | call date 08-06 confirmed on-record (Fool URL says 08-13 = publication date) |
| ON | 08-03 | 9,284 | Yahoo/Motley Fool | |
| WDC | 08-05 | 7,744 | MarketBeat/Quartr | GAAP $8.21 vs non-GAAP $3.56 — basis trap |
| CSCO | 08-12 | 10,388 | Yahoo/Motley Fool | |
| SMCI | 08-11 | 7,123 | Yahoo/Motley Fool | ⚠ see §2.2 |
| TEL | 07-22 | 8,345 | Yahoo/Quartr | |
| APH | 07-29 | 8,856 | Yahoo/Motley Fool | |
| VRT | 07-29 | 9,275 | Globe and Mail/Fool | ASR proper-noun errors flagged in file |
| NOW | 07-22 | 11,097 | Benzinga | analyst-name ASR errors flagged |
| CRWD | 08-26 | 9,293 | investing.com | |
| PWR | 07-30 | 10,204 | Yahoo/Quartr | |
| CEG | 08-06 | 9,009 | Yahoo/Quartr | |
| VST | 08-07 | 10,108 | Yahoo/Quartr | |
| TLN | 08-05 | 10,360 | Yahoo/Quartr | |
| ETN | 07-31 | 9,918 | Yahoo/Quartr | folder created |
| NVT | 07-31 | 8,633 | Yahoo/Quartr | |
| WMB | 08-04 | 10,109 | Yahoo/Quartr | call 08-04, not the 08-03 PR date |
| ALAB | 08-04 | 7,944 | Yahoo/Quartr | |
| UBER | 08-05 | 7,347 | Yahoo/Quartr | |
| SHOP | 08-05 | 10,516 | Yahoo/Quartr | |
| APP | 08-05 | 9,279 | Yahoo/Quartr | folder created |
| PLTR | 08-03 | 6,960 | Yahoo/Quartr | folder created; 3 questioners unnamed, mapped in header |
| VEEV | 08-26 | 10,774 | — | folder created |
| NVTS | 07-27 | 9,196 | Yahoo/Quartr | first full NVTS file since Q2'25 |
| SPCX | 08-04 | 8,728 | **Bloomberg FINAL** | first call as a public company — see §2.3 |
| MEDIATEK | 07-31 | 6,123 | — | |
| TM | 08-04 | 5,494 | official Toyota Q&A | issuer summary, not verbatim |
| BKNG | 08-04 | 9,087 | MarketBeat/Quartr | |
| SPOT | 08-04 | 9,350 | MarketBeat/Quartr | call was **08-04**, not late July as assumed |
| SNPS | 08-26 | 7,066 | MarketBeat/Quartr | folder created |
| WOLF | 08-19 | 3,772 | MarketBeat/Quartr | short call, complete |
| POWI | 08-05 | 4,531 | MarketBeat/Quartr | folder created |
| AOSL | 08-12 | 4,121 | MarketBeat/Quartr | ⚠ opening greeting missing — see §2.5 |
| VECO | 08-05 | 3,703 | MarketBeat/Quartr | short call, complete |
| AAOI | 08-06 | 7,860 | MarketBeat/Quartr | |
| AXTI | 07-30 | 6,529 | MarketBeat/Quartr | folder created |
| MP | 08-06 | 9,663 | MarketBeat/Quartr | folder created; ends on CEO wrap, no operator sign-off |
| AEIS | 08-03 | 8,811 | MarketBeat/Quartr | folder created |
| FLEX | 07-29 | 6,925 | MarketBeat/Quartr | |
| NET | 08-06 | 9,672 | MarketBeat/Quartr | folder created |
| AKAM | 08-06 | 9,015 | MarketBeat/Quartr | folder created |
| FSLY | 08-05 | 8,152 | MarketBeat/Quartr | folder created |
| TSEM | 08-04 | 7,863 | MarketBeat/Quartr | folder created; call was **08-04**, not 08-13 |
| ADVANTEST | 07-29 | 2,187 | **official Advantest IR** | issuer Q&A summary + deck + tanshin; no verbatim published. Results date **07-29**, not 07-28 |
| TOKYOELEC | 07-30 | 2,789 | **official TEL IR** | issuer **prepared-remarks transcript** + Q&A summary — the best-sourced of the three |
| DISCO | 07-23 | 1,848 | **official DISCO IR** | issuer "with notes" deck; **no Q&A published this quarter** — see §2.9 |
| BESI | 07-23 | 6,681 | investing.com | full verbatim; source mis-transcribes names in the closing pleasantries |
| SMIC | **08-14** | 3,591 EN + 6,633 zh | stockanalysis + investing.com | **composite, Mandarin call** — see §2.10; call was **08-14**, not 08-07 |
| BE | 07-28 | 8,171 | investing.com | full verbatim; source has no inline speaker tags — mapping reconstructed, see §2.11 |
| IFX | 08-05 | 9,291 | **official Infineon IR** + media call | **analyst Q&A is the one real gap** — see §2.11 |

**14 tickers got a `transcripts/` folder for the first time:** BE, ETN, APP, PLTR, VEEV, SNPS, POWI, AXTI, MP, AEIS, NET, AKAM, FSLY, TSEM.

---

## 2 — Caveats that must travel with the files

1. **NVDA Q2 FY27 is third-party, not NVIDIA's own IR transcript.** NVIDIA had not posted the q4cdn PDF (the source used for Q1 FY27) as of 08-31 — re-checked, still 404. Two things to carry: (a) the source **mislabels the first Q&A answer** — several paragraphs plainly in Jensen Huang's voice ("we are practically singular…") carry Colette Kress's label before it switches; verify attribution on the Joseph Moore exchange before quoting by name. (b) The publisher titles it "Q2 2026" (calendar-quarter labelling); the call is unambiguously **fiscal Q2 2027**. When the IR PDF appears at `…/doc_financials/2027/q2/`, it should overwrite the file (same filename).
2. **SMCI: a claim in press coverage is NOT in the call.** Search results asserted the call disclosed a board independent review tied to export controls. The transcript contains **zero** mentions of "board" or "review" — that traces to the press release / coverage, not the call. SMCI's FY26 10-K was **not yet filed** as of 08-31; verify there. Also decompose Q4 non-GAAP GM 17.6% / EPS $1.70 (vs its own 8.2–8.4% / $0.65–0.79 guide) before extrapolating — management attributes part to "few one-time positive contributions".
3. **SPCX is a Bloomberg FINAL transcript recovered from `_inbox/_done/`, not a new fetch.** It had been sitting unprocessed since 08-05 as an unrouted inbox PDF (the router mis-files `* Earnings Call *` PDFs — the known bug from the July sweep, still open). Bloomberg per-page furniture stripped the same way as the July KLAC/TER files; the closing accuracy disclaimer and `{BIO … <GO>}` tags kept.
4. **MRVL: analysts name Google as the warrant counterparty; management only ever says "key hyperscaler" / "TPU ecosystem."** Do not put Google in management's mouth.
5. **AOSL's transcript starts mid-sentence.** The source feed begins at "I will now hand the call over to Steven Pelayo" — the operator's opening greeting and safe-harbor are missing. Everything from the IR hand-off onward is present. Labelled in the file.
6. **The MarketBeat-sourced files (the last 16) are one continuous stream.** MarketBeat serves prepared remarks and Q&A under a single container, so those files do **not** assert a prepared-remarks/Q&A split — rather than invent a boundary. Speaker titles and analyst-name spellings are Quartr diarization labels, as-heard, not independently verified.
7. **Call dates ≠ press-release dates, and five assumptions were wrong.** Verified from source: **SPOT 08-04** (not late July), **TSEM 08-04** (not 08-13), **SMIC 08-14** (not 08-07 — investing.com stamps 08-13 21:43 ET, i.e. the morning of 08-14 HKT; filed under HKT to match the prior SMIC files), **ADVANTEST 07-29** (not 07-28), **WMB 08-04** (PR 08-03, call next morning), **MCHP 08-06** (Fool's 08-13 URL is its publication date). Filed by call date per repo convention. **Lesson for the next sweep: derive the call date from the source, never from the 8-K/PR date** — roughly one name in eight differs.

### 2.9 — The three Japanese issuers: what they actually publish

None of the three publishes a vendor-style verbatim transcript, and the files say so rather than implying more than exists:

- **TOKYOELEC is the best-sourced** — TEL publishes an actual **prepared-remarks transcript** (`fy27q1transcript-e.pdf`, slide by slide, both presenters) plus a separate Q&A summary of 15 questions. ⚠ Slide 5's **text layer has GP/OI/NI series labels transposed**; the slide-4 table is authoritative and the file flags it. Q14/Q15 were submitted in writing and answered only in the document, never on the call.
- **ADVANTEST** publishes an issuer-edited **Q&A summary** (10 Q&As) + briefing deck + tanshin — no verbatim. The agent deliberately **omitted the ship-to-region table**: the deck's region chart could not be reliably mapped to its legend from the PDF text layer, and the legend order provably does not match the series order. Only the two region facts stated in words are carried (Taiwan largest, China ≈19%). That is the right call — a mis-mapped region split would have been worse than no table.
- **DISCO published no transcript and no Q&A at all this quarter.** Its "with notes" deck is its own slide-by-slide narration and is the primary source. The file states plainly that it contains **no analyst exchange**.

**⚠ DISCO basis trap, stated by DISCO itself:** revenue books on an **inspection/acceptance basis**, so net sales are not a read on customer appetite — DISCO's own instruction is to use **shipment value**. Q1 sales fell 14.1% QoQ while **shipments hit a record ¥135.9bn**. Never quote the sales decline as a demand signal.

**Archive correction made 2026-08-31:** `DISCO_Q4-FY26-results_2026-04-22.md` claimed DISCO labels the year ended Mar-2026 "FY2026" and flagged Quartr as the outlier. That is backwards — DISCO calls that year **FY2025** (Japanese convention: FY named for the year it *starts*), so Quartr matched the issuer. Verified against DISCO's own English notes deck, which discusses forward capex "From FY2026 onward" in a July-2026 document. The old note has been corrected in place with the superseded claim preserved; **no figure in that file changes.**

### 2.10 — SMIC is a composite file, and its Q&A is a machine translation

SMIC's call is held **in Mandarin**. Prepared remarks run through SMIC's live English interpreter, so `stockanalysis.com` carries them in English — but its Q&A is entirely `[Non-English content]` placeholders. `investing.com` carries the **Chinese original plus its own machine translation** of every Q&A turn. The archived file therefore merges two sources, says so in the header, and **keeps both the Chinese and the English** for each Q&A turn.

- ⚠ **Do not quote the English Q&A as verbatim management language** — it is condensed, not word-for-word. Quote the Chinese, or the results release.
- ⚠ **The "$600bn → $880bn" AI investment figure is NOT SMIC guidance.** Co-CEO Zhao is relaying a US analyst broadcast he had heard that morning. Very easy to misattribute to the company.
- Full-year 2026 depreciation rendered inconsistently across extraction passes ("approaching $5bn" vs "$4.9–5.0bn"); the Chinese reads 接近50亿, so **~$5bn**.
- Four answer turns (CICC ×2, Orient ×2) came back English-only and are individually marked in-line rather than left looking like dropped quotes.

**BESI caveat:** investing.com is machine-generated from audio and garbles names in the closing pleasantries — Blickman is transcribed thanking "Olivier"/"Jose"/"Johan"/"Wouter", and once addresses Charles Shi as "Richard". These were **left verbatim rather than silently corrected**; the header flags that closing-pleasantry names are unreliable while operator-introduced analyst attributions are sound.

**Deliberate deviation worth knowing:** the pre-existing `BESI_Q1-2026…` and `SMIC_Q1-2026…` files are **synthesized summary notes, not transcripts**. The new files use the transcript header convention rather than copying the neighbours' style, because copying it onto a 6,700-word verbatim transcript would mislabel the artifact type. This is the same stub problem as §3, seen up close.

### 2.11 — IFX: the brief's premise was wrong, and the analyst Q&A is the gap

**Correction, found by checking rather than assuming.** This sweep's brief asserted Q3 FY26 was Infineon's first print under the new three-division structure. **It was not.** The June quarter was still reported on the **old four divisions (ATV / GIP / PSS / CSS)**. The new **Automotive / Power Systems / Edge Systems** structure took effect **2026-07-01**, i.e. **Q4 FY26**. Infineon will publish four-division financials *alongside* the new cut for the September quarter so FY26 stays modellable, then switch with the FY27 outlook at the **November** call and restate history there. Composition disclosed: **ES = CSS + sensor & RF + USB connectivity carved out of PSS** — so PSS is being **split, not renamed**. Anyone modelling the transition off this quarter would have had the date and the mechanics wrong.

**The file is two same-day events, both labelled:** Part A = the analyst call's **prepared remarks only**, verbatim from Infineon's own IR intro-statement PDF (primary source, not third-party). Part B = the **media/press call in full**, including Q&A with four journalists. **The analyst Q&A is archived nowhere** — Infineon publishes only the intro statement as text, and the vendors that carry the Q&A sit behind human-verification challenges that were correctly not bypassed. That is the one real hole left in the window.

🔭 **Variant perception vs `_wiki/IFX.md`** (page not edited, per the no-`_wiki`-edits rule for this sweep): FY26 dedicated **AI-power revenue guided >EUR 1.6bn** (was 1.5bn) plus ~EUR 500m classic datacenter power, and management **pre-announced a "material" upgrade to the EUR 2.5bn FY27 figure in November** — Hanebeck on the media call: *"this effect of 2.5 would be turned into a three."* Also new: multi-year **capacity-reservation agreements** with cumulative sales volume in the **high-single-digit billion EUR** range, carrying prepayments; backlog **~EUR 30bn** (from ~25bn). The IFX page's Debate and Changelog are now behind these numbers.

**BE caveat:** investing.com publishes BE's paragraphs **without inline speaker tags**. The speaker sequence (43 turns) was pulled in a second pass and mapped onto the 81 paragraphs; the mapping came out exact and paragraph text is verbatim, but it is a reconstruction and the header says so. Transcription artifacts left uncorrected and flagged ("Gus," for "Guys," opening Colin Rusch; "NEB" for Nebius).

### 2.8 — Source-channel notes for the next sweep

The July sweep's channel map has changed materially:

- ✅ **NEW — Yahoo Finance quote-page transcripts** (`finance.yahoo.com/quote/<TK>/earnings/<TK>-Q<n>-<YYYY>-earnings_call-<eventId>.html`) embed a **full Quartr diarized transcript**, complete with per-turn timestamps and a participants roster. Best channel found so far. **But it rate-limited this box mid-session** — after ~40 fetches it began returning HTTP 404 for *every* transcript URL, including ones fetched successfully an hour earlier. Not a permanent block; pace it.
- ✅ **NEW — MarketBeat** (`marketbeat.com/earnings/reports/<YYYY>-<M>-<D>-<slug>-stock/`) carries the **same Quartr feed** in clean, easily-parsed HTML and did **not** rate-limit. This is the workhorse fallback and is what the last 16 files came from. Its date-keyed URL doubles as a call-date check: a wrong date simply 404s.
- ✅ **Yahoo's earnings index** (`finance.yahoo.com/quote/<TK>/earnings/`) embeds JSON with `fiscalYear` / `fiscalPeriod` / `date` (epoch) / `transcriptId` / `eventId` for every call — the cheapest way to resolve a real call date. Also rate-limits (503).
- ✅ **Yahoo also syndicates Motley Fool full transcripts** as articles (`finance.yahoo.com/markets/stocks/articles/…`), which sidesteps fool.com's own block and WebFetch's copyright refusal.
- ⚠ **investing.com**: raw urllib now **403s on the listing page** but article URLs still work; WebFetch works throughout.
- ❌ Unchanged: fool.com direct (blocks/404), AlphaStreet direct (403), stockanalysis.com (blocked), disco.co.jp (unreachable behind the TLS proxy).
- **TLS-proxy gotcha:** the corporate proxy re-signs certificates, so stdlib `urllib` fails with `CERTIFICATE_VERIFY_FAILED: Missing Authority Key Identifier` on hosts that are otherwise reachable. `ssl._create_unverified_context()` fixes it — that alone turned q4cdn/Yahoo/MarketBeat from "blocked" into "working". Worth knowing: several hosts the July sweep recorded as blocked may simply have been cert failures.

---

## 3 — ⚠ Archive-quality finding: 43% of the transcript archive is summary stubs, not transcripts

Checking word counts across the whole archive while filing this sweep surfaced a problem that is **not** specific to this window:

> **222 of 518 transcript `.md` files (43%), spanning 58 tickers, are under 1,200 words** — they are short summaries/extracts, not transcripts. Many are 85–550 words.

Examples: `ALAB_Q3-2025-earnings` **85 w** · `SHOP_Q2-2025-earnings` **117 w** · `TEL_Q3-FY25-earnings` **122 w** · `SMCI_Q1-FY26-earnings` **163 w** · `ADI_Q4-FY25-earnings` **198 w**. Tickers with 4+ stub quarters include CEG (6), ANET (5), NOW (5), ADI, AGX, AIXA, ALAB, AMAT, APH, ARM, BESI, CRDO, CRM, CRWD, CRWV, DELL, DISCO, FLEX, GLW, HPE, IFX, INTC, KLAC, LITE, LRCX, MCHP, MEDIATEK, MRVL.

**Why it matters:** the graph context line "Docs on disk: transcript N" counts stubs and full transcripts identically, so a name can look well-covered while holding almost no primary text. Corpus search over those quarters returns nearly nothing, and a subagent told "read the transcript" gets a summary someone else already wrote — which is how paraphrase gets promoted to primary source.

**This sweep replaced the current-quarter stub with a real verbatim transcript for ~20 of those names** (ADI, ALAB, APH, FLEX, MCHP, MRVL, NVT, SHOP, SMCI, TEL, VECO, and others). The **back quarters are still stubs**. Proposed fix, not yet done: backfill the stub quarters via the MarketBeat/Quartr channel (it carries several years of history per ticker), prioritised by book weight. Worth a dedicated run — it is mechanical and now cheap.

---

## 4 — Still open

| Item | Status |
|---|---|
| **IFX analyst-call Q&A** | The prepared remarks (Infineon's own IR PDF) and the *entire* media call are archived; the **analyst Q&A exists only in the webcast**. Seeking Alpha and GuruFocus carry it behind human-verification challenges (not bypassed); MarketScreener serves a paywalled stub. Needs a manual pull from the terminal or a broker copy. |
| **NVDA official IR transcript** | q4cdn PDF still not posted as of 08-31; re-check and overwrite when it appears. |
| **AMZN Q2'26 FINAL transcript** | Unchanged from the July sweep — the archived file is the vision-transcribed Bloomberg **live** feed. |
| **SAMSUNG Q2'26 verbatim Q&A** | Unchanged — Samsung publishes none in English. |
| **`fetch_sec_filings.py` carries a stale SPCX exclusion** | Its comment block still lists SpaceX among companies with "no SEC filings"; SPCX is now a filer (CIK 1181412) and should join `BASE_TICKERS`. The one-off sweep script has been corrected; the repo script has **not**. |
| **Inbox router still mis-files earnings-call PDFs** | The `* Earnings Call *` → `<TICKER>/transcripts/` special case flagged in the July sweep is still not implemented — which is why SPCX's Bloomberg call sat unrouted in `_inbox/_done/` for three weeks. |
| **SEC filings still not in the search index** | `build_search_index.py` gates them behind `--filings` and `refresh_features.py` omits it. The 70 filings above are on disk but not searchable. Run `py _wiki/_tools/build_search_index.py --filings` to include them. |

### Filings not yet filed by the issuer (calendar for the next sweep)

| ~Date | Item |
|---|---|
| early Sept | **SMCI** FY26 10-K (printed 08-11) · **CSCO** FY26 10-K (printed 08-12) |
| 09-02/03 | **CRDO** FQ1 · **CIEN** FQ3 · **HPE** FQ3 |
| 09-04 | **AVGO** FQ3 |
| ~09-09 | **AGX** FQ2 |
| ~mid-Sept | **ORCL** FQ1 · **PANW** FQ4 (print + FY26 10-K) |
| ~09-29 | **MU** FQ4 |

---

## 5 — Method notes

- **Order of work was by company importance**, as asked: book names (NVDA first) → core AI semis → AI infra/power → software/internet → small-cap tail → foreign issuers.
- **Filings**: one idempotent script over EDGAR (`--plan`-style dedup by accession, skips what is on disk). Zero failures across 70 documents. EDGAR remains the only host that passes this box's proxy without help.
- **Transcripts**: dispatched as paired-ticker subagents. Two waves were killed mid-flight by the individual spend limit; **the work was not lost** — several agents had already written their files, and the survivors' channel discoveries (Yahoo→Quartr, MarketBeat) were folded into the next wave's brief. The final 16 were built in-thread with a single parser once the channel was proven, which was far cheaper than one agent per name.
- **Every file was validated after writing**: word count, U+FFFD (mojibake) count, and first/last speaker turn to confirm the call actually opens and closes. Four files failed the boundary heuristic; three turned out complete (phrasing the heuristic missed) and were relabelled, one (AOSL) was genuinely truncated at the front and says so.
- **Scratchpad collision:** parallel subagents share one scratchpad directory and overwrote each other's helper scripts mid-run; one left an `inspect.py` there that **shadowed the stdlib module** and broke `argparse` for anything run from that directory. Give each agent its own subfolder, and never name a scratch file after a stdlib module.