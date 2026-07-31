# Earnings-week archive sweep — prints of 2026-07-16 → 07-31

_Built 2026-07-31. Complements the auto-generated `worklist.md` (remediate.py): that file tracks standing gaps, this one closed the loop on the July print season. **Status: executed the same day** — SEC filings pulled from EDGAR, transcripts swept off the open web. What is still missing is listed in §4, and needs to be supplied by hand._

_Why it was needed: the bulk SEC/transcript archive was ingested 2026-06-17→20 and stopped at the **April** prints. The wiki PAGES were current (the 07-30 ingest runs patched them); the RAW ARCHIVE underneath them was three months stale._

---

## 1 — What landed

### SEC filings — 566 documents across 48 tickers (EDGAR, zero failures)

| Pass | Scope | Result |
|---|---|---|
| Incremental | every wiki ticker, anything filed since 2026-06-01 not already on disk | **51** filings / 30 tickers |
| Earnings 8-K | this + prior week's printers, since 2026-07-15 | **30** documents (8-K + EX-99 press releases) |
| Exhibit backfill | EX-99.* for 8-K/6-K whose primary doc was already archived | **31** press releases / shareholder letters |
| SK hynix | first-ever SEC filings (Nasdaq ADR since 2026-07-10) | **5** 6-Ks, incl. the Q2 earnings 6-K (07-29) |
| Folder backfill | the 14 wiki names that had **no ticker folder at all** — 3 years of 10-K/10-Q/20-F | **449** filings |

Every print in the window now has a 10-Q/10-K **or** its earnings press release on disk. Two names have neither and correctly never will: **SAMSUNG** (KRX only) and **DISCO** (TSE only) — neither is SEC-registered.

Two finds worth knowing about:
- **`RDDT_8-K_ex992_exhibit_2026-07-30_…html` is the Q2 shareholder letter** — the "Search referrals were choppy in the quarter" language that the bear case rests on. That is the primary source, now on disk.
- **`TSM_6-K_ex992_exhibit_2026-07-16_…html` is the 2Q26 earnings-conference deck.**

### Transcripts — all 17 covered prints, plus 6 prior-week stragglers

Word counts are post-cleanup (Bloomberg per-page furniture stripped — see §2.9).

| Ticker | Call | Words | Quality |
|---|---|---|---|
| META | 07-29 | 10,662 | verbatim — Bloomberg **FINAL** |
| KLAC | 07-28 | 10,199 | verbatim — Bloomberg **FINAL** |
| LRCX | 07-29 | 10,365 | verbatim |
| MSFT | 07-29 | 9,948 | verbatim — Bloomberg **INITIAL DRAFT** ⚠ see §2.9 |
| RDDT | 07-30 | 9,691 | verbatim |
| CDNS | 07-27 | 9,439 | verbatim (ASR — proper-noun errors, flagged in file) |
| STX | 07-28 | 8,938 | verbatim |
| TER | **07-29** | 8,869 | verbatim — Bloomberg **FINAL** |
| SANM | 07-27 | 8,496 | verbatim (ASR — proper-noun errors, flagged in file) |
| GLW | 07-28 | 8,454 | verbatim |
| AMZN | 07-30 | 8,369 | verbatim ⚠ **live ASR, see §2.1** |
| NXPI | 07-28 | 8,162 | verbatim |
| AAPL | 07-30 | 8,104 | verbatim (Six Colors; ex-IR boilerplate) |
| ARM | 07-29 | 7,298 | verbatim |
| QCOM | 07-29 | 6,159 | verbatim |
| SKHYNIX | 07-29 | 6,061 | verbatim — Bloomberg **FINAL** |
| SAMSUNG | 07-30 | 2,406 | **mixed** — official English IR deck in full + Q&A summarized |

Plus **AEHR** FQ4-FY26 (07-14), 10,148w verbatim Bloomberg FINAL — archived but **outside the covered universe**, see §4.

**Second pass, 2026-07-31 (Bloomberg FINAL PDFs supplied from the terminal):** KLAC
4,677w → **10,856w** and TER 4,060w → **9,402w**, both now full verbatim with complete
Q&A, superseding the third-party partials. The desk-analysis blocks those partials
carried (headline-number quick reference, load-bearing market calls, market reaction)
were preserved as a labelled *"Desk notes — NOT part of the transcript"* appendix
rather than discarded. **AEHR** Q4-FY26 (07-14) archived new at **10,794w**. Source
PDFs preserved in `_inbox/_done/`.

The Bloomberg KLAC transcript settles the earlier data question: **non-GAAP diluted
EPS $1.05, GAAP $1.04**, Sept guide **$1.16 ±$0.10** on ~1.3bn diluted shares —
confirming the post-split basis and that Quartr's "$1.5" rendering was a data error.

Prior-week stragglers also filled: **GOOG** (9,256), **TSLA** (9,824 — folder created), **INTC** (9,121), **GEV** (8,555), **TXN** (7,865), **NFLX** (6,703, from Netflix's own IR transcript PDF).

Three tickers got folders created from scratch: **SANM**, **TSLA**, **CDNS/transcripts**.

---

## 2 — Caveats that must travel with the files

1. **AMZN is Bloomberg's LIVE feed, not the FINAL transcript.** The inbox PDF was a Print-to-PDF of `Live Transcript.html` with **no text layer** (pdfplumber and PyMuPDF both return 0 chars), so it was vision-transcribed from 170dpi page renders. It preserves real-time mis-hearings — Trainium→"Tradium", Claude Code→"Cloud Code", AgentCore→"Bedrock Agent Corp", Kiro→"spec-driven curo", Graviton→"Gravitat", Amazon Haul→"Amazon Hall", NBA→"MBA", Profitero→"Profittero", Prime Day→"Prime Bay". The full table is in the file header. **Verify any load-bearing quote against the 8-K EX-99.1 before citing it on a page.** Also: Bloomberg's roster omits Jason Helfstein and Ken Gawrelski — one is the `Unidentified Participant` whose line dropped, so do not attribute an unlabelled question to a named analyst.
2. **TER's call was 07-29, not 07-28** (press release 07-28 4:35pm ET, call next morning 8:30am ET — Teradyne's standing pattern). Filed by call date per repo convention.
3. **CDNS and SANM are complete but machine-transcribed (ASR)**, and misrecognise proper nouns: SANM renders Jure Sola as "Yuri" and Jon Faust as "John"; CDNS renders Anirudh Devgan as "Aru"/"Ader"/"Andrew", labels Siti Panigrahi as "CP", and mis-assigns one John Wall line to Devgan. Left uncorrected and flagged inline — verify exact wording against the webcast before quoting in client-facing work. Both files keep the earlier structured extract as a labelled **"Desk notes — NOT part of the transcript"** appendix, because it held non-call facts (guide progression, GAAP figures from the PR).
   - ⚠ **SANM Q3 FCF basis conflict is real and comes from management, not the transcription:** Faust says "free cash flow was $223.7 million" on the call while also giving OCF $124.5M and capex $100.9M, which imply **~$24M** — matching the press release. Flag the basis every time SANM Q3 FCF is quoted.
4. **ARM's transcript has swapped speaker labels.** The transcription service appears to confuse Rene Haas and Jason Child in at least three places — most visibly an answer labelled "Jason Child" that opens *"I'll take both parts of that question, and Jason, you can add on."* Text is verbatim, caveat is in the header; check Arm's own IR transcript before quoting those passages. Separately, investing.com's URL slug says `q1-2026` but the call is unambiguously **fiscal Q1 2027** (operator and IR both say so) — publisher error, documented in the file.
5. **SAMSUNG has no verbatim Q&A anywhere** — Samsung doesn't publish one. The file marks every section `[official deck]` vs `[Q&A — summarized]`, and is better-sourced than the four prior quarters in the archive (which are third-party).
6. **KLAC's 10-for-1 split (effective 2026-06-11) is NOT a problem** — checked, because a subagent flagged it as one. The press release retroactively adjusts per-share data (FQ4 non-GAAP EPS $1.05, FY26 $3.76), `_data/estimates.json` is already on the post-split basis (px $180.33, 1FQ EPS $1.158), and [KLAC.md](../KLAC.md) flags the basis at every mark and has the pre-split figures parked in its Changelog. No action needed.
7. **SEC filing HTMLs are not in the search index by default.** `build_search_index.py` gates them behind `--filings`, and `refresh_features.py` calls it without that flag. Transcripts *are* indexed. To make the 566 filings searchable: `py _wiki/_tools/build_search_index.py --filings`.
8. **⚠ MSFT's Bloomberg PDF is an `INITIAL DRAFT TRANSCRIPT`, not FINAL** — the status marker is printed on every page and the first pass asserted FINAL for all six Bloomberg-sourced files without reading it. Corrected: the status is now parsed out of the document, and the MSFT file carries an explicit warning that draft wording gets revised and speaker attribution is less reliable. **Verify MSFT quotes against Microsoft's own IR transcript** (`cdn-dynmedia-1.microsoft.com/…/TranscriptQandAFY26Q4` follows the pattern of the archived FY26Q3 file) or a FINAL Bloomberg export. META, SKHYNIX, KLAC, TER, AEHR and the pre-existing TSM file are all genuine FINAL.
9. **Bloomberg per-page furniture was polluting the search index** and is now stripped: copyright line, running company header (`KLA Corp (KLAC US Equity)`), the status marker and the date stamp — 4 lines × every page, i.e. 84 junk lines in a 21-page transcript. All six Bloomberg files were rebuilt; word counts in §1 dropped 5-10% purely from removing this. Two things deliberately kept: the closing accuracy disclaimer (real provenance) and the `{BIO nnnnnnn <GO>}` terminal tags (harmless, and they disambiguate speakers).
   - ⚠ **`TSM/transcripts/TSM_Q2-2026-earnings_2026-07-16.md` still has the un-stripped furniture and mojibake** (`â€"` for em-dashes) — it was written by an earlier ingest, not this sweep, and was left alone. Worth rebuilding from `_inbox/_done/Taiwan Semiconductor…2026716…pdf` with the same script.
   - SKHYNIX date note: Bloomberg stamps its transcript **07-28** (US Eastern) for a call held the morning of **07-29 KST**. Filed under the KST date to match the four prior SKHYNIX files.
10. **POET dumped 295 6-Ks** (Canadian issuer, one per press release). The 249 filed before 2026-01-01 were moved to `POET/6-K_archive_pre2026/` so they don't drown the ticker folder; the 20-Fs and 2026 6-Ks stay at top level.

---

## 3 — Housekeeping still open

- The five Bloomberg call PDFs that arrived via `_inbox` are still **duplicated** in `relatórios bons\` as image-stub HTMLs (`Microsoft_Corp_Earnings_Call_…`, `Meta_Platforms_Inc_…`, `SK_hynix_Inc_…`, `amzn_earnigns_call`, `Taiwan_Semiconductor_…`). They are indexed there as kind `report`. Now that proper transcripts exist, those stubs are redundant — optional dedup.
- `relatórios bons\d3906787-….html` is Apple's FQ3'26 8-K, mis-detected as a "Citi" note by the router (corrected in `_inbox\_ingest-log.md` 07-30). The clean EDGAR copy is now at `AAPL/AAPL_8-K_2026-07-30_…html`. Same for `relatórios bons\0001193125-26-323660.html` = MSFT's FY26 10-K.
- **Router fix pending:** `ingest_inbox.py` should special-case `* Earnings Call *` PDFs → `<TICKER>/transcripts/`. Spun off as a separate task.
- Add SK hynix 6-Ks to the routine sweep now that it is an SEC filer.
- **RDDT shareholder letters** are load-bearing primary docs for that name — the EX-99.2 pull now captures them automatically.

---

## 4 — Still missing — needs to be supplied by hand

Everything below was searched for on the open web and could not be retrieved.

✅ **Closed on 2026-07-31** by Bloomberg FINAL PDFs from the terminal: **KLAC**, **TER**, **AEHR**.

Still open:

| Item | Why it failed | What would fix it |
|---|---|---|
| **AMZN Q2'26 FINAL transcript** (07-30) | the copy supplied from `Downloads` is **byte-identical** to the one already in `_inbox/_done` (sha256 `b274ef19…`, 16 pages, 0 extractable chars) — same live-ASR export, not the FINAL | a Bloomberg **FINAL** export of this call, which would replace the vision-transcribed live version. This is the last real gap in the window |
| **SAMSUNG Q2'26 verbatim Q&A** (07-30) | Samsung does not publish one in English | a broker's transcription, if any desk has it |
| **DISCO Q1-FY27 results package** (07-23) | `disco.co.jp` is unreachable behind the TLS proxy (both the EN IR library and the top-level IR page) | the results presentation / tanshin PDF, or a Smartkarma/Bernstein note — `outcomes.md` already carries a FLAG that the print figures are not sourced on-page |

**Coverage question left open: does AEHR belong in the universe?** Its transcript is now archived and indexed, but Aehr Test Systems has **no wiki page**, so it sits outside the covered 101. Note that `_inbox\_done\` also holds a broker note on it (*"The Inflection Arrives; New AI, SiPho, and Memory Customers Offer Upside to Guide"*), so there is real research flow on the name — the archive is accumulating AEHR material with nowhere to synthesize it. Two copies of the call PDF now exist there (the user-supplied `20260714_Aehr_Test_Systems-…` and the older `Aehr Test Systems Earnings Call 2026714…`); same content, different export metadata.

### Filings not yet filed by the issuer (calendar for the next sweep)

| ~Date | Item |
|---|---|
| ~08-04/05 | **STX** FY26 10-K · **KLAC** FY26 10-K · **TER** Q2 10-Q |
| ~08-15+ | **LRCX** FY26 10-K (files mid/late Aug) |
| 08-04 | **AMD** Q2'26 prints → transcript + 10-Q |
| 08-05 | **IFX** FY3Q26 prints — first print under the new 3-division segmentation → transcript + interim report (German issuer, no SEC) |

---

## 5 — Method notes for the next sweep

**EDGAR** works fine from this box with stdlib `urllib` + a declared User-Agent. Two things that cost time and are worth hard-coding:
- **Never guess exhibit filenames.** They are wildly inconsistent (`googexhibit991q22026.htm`, `q226earningsrelease.htm`, `stxq42026pressreleasefinan.htm`, `lrcx_exhibitx991xq4x2026.htm`). Read the **Type** column out of `{accession}-index.html` instead — that is authoritative and gives you the EX number, which is how the RDDT shareholder letter (EX-99.2) was found.
- **Dedup by accession skips exhibits.** A filing whose primary doc is already on disk will be skipped wholesale, so a separate exhibit-backfill pass is needed after any change to exhibit logic.
- **SK hynix resolves as `SKHY`** (also `HXSCL`), CIK 2120882.

**Transcripts on the open web** — what worked and what did not:
- ✅ **investing.com `/news/transcripts/`** was the single most reliable host — complete transcripts, and it went through cleanly for CDNS, SANM, GLW, NXPI, QCOM, RDDT.
- ✅ **AlphaStreet** worked for GOOG/INTC/TSLA/GEV/TXN, but **only via WebSearch's own retrieval** — direct WebFetch of its canonical and AMP URLs returns HTTP 403.
- ✅ **Netflix and Samsung publish first-party English transcripts/decks** on their IR sites; Apple's best free source is **Six Colors**, not Motley Fool (which had no AAPL FQ3'26 page).
- ❌ Raw `urllib` from this machine is blocked for investing.com (403), stockanalysis.com, AlphaStreet and disco.co.jp — the TLS proxy only reliably passes EDGAR. Use WebFetch for anything else.
- ⚠ **WebFetch summarises by default.** Asking for "the transcript, verbatim, no summarising" still returns bullet-point highlights. What beat it: ask for a **numbered list where each item is one paragraph copied character-for-character**, and anchor each continuation chunk on the **last sentence of the previous chunk** rather than a paragraph number. Watch for a duplicated paragraph at chunk seams. WebFetch also refuses verbatim reproduction of fool.com on copyright grounds.
- **Bloomberg call PDFs already in `_inbox\_done\` usually have a clean text layer** — PyMuPDF (`fitz`) extracted MSFT/META/SKHYNIX/TSM/AEHR at 43-67k chars each even though the earlier ingest reported them as image-only. Always retry with fitz before falling back to vision.
