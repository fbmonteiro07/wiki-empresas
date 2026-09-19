# Double-check verdict — AMD / AVGO "Template DCF" pair (built 2026-09-16/17)

**Audit date:** 2026-09-18 · **Auditor:** `double-check` agent (hostile QA), read-only on copies · **Verdict: FAIL (AVGO) / FAIL (AMD) / FAIL (pair)**

Files audited: `P:\Felipe Monteiro\US Equities\Modelos oficiais\Template DCF AMD.xlsx` (saved 2026-09-16 20:07) · `…\Template DCF AVGO.xlsx` (saved 2026-09-17 14:40, post "share edit") · parent `…\Template DCF NVDA.xlsx` · house sources `…\AMD WIP.xlsx` (2026-07-30) and `…\Modelo Avgo pós 2Q26.xlsx` (2026-09-04) · working folders `E:\outputs\avgo-amd-dcf-20260916\` and `E:\outputs\avgo-shares-20260917\`.

Prior analyst's headline outputs: **AVGO DCF $720.45** (px $347.30) · **AMD DCF $295.79** (px $545.09); valuation date 2026-08-27, WACC 10%, g 2%, terminal incremental ROIC 20%.

---

## 1. Outlook coverage — FAIL

Outlook MCP/`outlook.py` hung on the 71k-item inbox; fell back to Outlook COM with DASL `Items.Restrict` (received ≥ 2026-07-01, subject LIKE AVGO/Broadcom/AMD).

- **267 relevant messages** in the window (148 AVGO from 50 senders; 127 AMD from 41 senders). **Referenced by the prior analyst: zero.** Workbook source columns cite only the three xlsx files.
- 11 of the 31 priority Tech Spec Sales contacts published AMD/AVGO notes in the window; 0 read.

Unread notes the DCF should have been benchmarked against, all dated before the build:

| Name | Date | Sender | Note |
|---|---|---|---|
| AVGO | 09-02 | Blayne Curtis (Jefferies) | "I See You and Raise You a FY28 Guide" |
| AVGO | 09-02 | Joseph Moore (MS) | PT $502 → $505; "raising FY28 EPS" |
| AVGO | 09-03 | Tom O'Malley (Barclays) | "FY28 AI Revenue to Double Y/Y to $230B" |
| AVGO | 09-03 | Harlan Sur (JPM) | "FY28 $230B+ in AI Revenues and $30 EPS Outlook" |
| AVGO | 09-03 | Tim Arcuri (UBS) | "A Line of Sight to FY28 AI Revenues of $230B and $30+ EPS" |
| AVGO | 09-02 | Jim Schneider (GS) | "Strong AI revenue forecast through 2028" |
| AVGO | 09-03 | Rothschild/Redburn | "All-in on the frontier" (Buy) |
| AVGO | 09-15 | Bernstein / MS | "Hock reiterates AVGO targets" / "AVGO rev targets unch" — the day before the AVGO DCF was built |
| AVGO | 09-03/04 | Capstone internal (F. Monteiro, F. Watkins, D. Grozdea) | Harlan Sur post-2Q26 callback; JPM AMA follow-up; Joe Moore callback; N. Winkler callback; MS call w/ AVGO (08-21) |
| AMD | 08-03 / 08-05 | Morgan Stanley Research | "AMD.O Model: Regular Update" ×2 (full model files) |
| AMD | 08-05 | Joseph Moore (MS) | PT $410 → **$465** (Street low); "2027 significantly better" |
| AMD | 08-04 | Blayne Curtis (Jefferies) | "C27 Outlook Improving, Total DC Set to More than Double" |
| AMD | 08-04 | Jim Schneider (GS) | "Strong 2027 commentary falls short of most bullish expectations" |
| AMD | 07-30 / 08-03 | Jeffrey Rand (Barclays) | "AMD Bogey Survey" / "RESULTS" |
| AMD | 08-04 | Joshua Meyers (JPM) | "Buyside Bars"; "First Blush"; "Off the Call" |
| AMD | 07-24 | UBS | "AMD (raising estimates)" |
| AMD | 09-07 / 09-11 | F. Watkins / GS | CFO @ Citi; Communacopia key takeaways |

## 2. SEC filings coverage — FAIL on process, PARTIAL on materiality

11 filings covering the last 2 years on disk (`AMD\`, `AVGO\`); **none opened, zero line-item citations.** Balance sheets were taken from the house xlsx, not filings.

**AMD — 10-Q filed 2026-08-05 (q/e 2026-06-27):** cash $5,086m + STI $8,025m = **$13,111m** (ties to CFO Jean Hu's "$13.1 billion" on the 08-04 call); debt $875m + $2,351m = **$3,226m**; **net cash $9,885m**. DCF: $12,347m / $3,224m → net cash $9,123m as of 2026-03-31 (understated $762m = $0.46/sh). Shares issued 1,632m; diluted 1,659m (Q2). DCF 1,656.3m frozen to 2045 while the same sheet's row 19 carries **1,760.05m for CY28** — honouring it takes $295.79 → **$278.36**.

**AVGO — 10-Q filed 2026-09-10 (q/e 2026-08-02), six days before the build:** cash **$23,975m**; debt $2,252m + $57,167m = **$59,419m**; **net debt $35,444m**. DCF: $19,628m / $64,907m → net debt $45,279m as of 2026-04-30 (**overstated $9,835m = $1.99/sh**). Shares outstanding 4,774m; diluted 4,887m (DCF 4,932.7m, +0.9%). FQ3'26 revenue $29,591m (semis $20,839m / software $8,752m).

Fixing both stale balance sheets: AVGO → $729.20 (+1.2%); AMD → $296.25 (+0.2%), or $278.79 with the house dilution path. Real and indefensible, but a ~1% issue — not what is wrong with the models.

## 3. Transcript coverage — FAIL

**AVGO:** newest transcript on disk is Q2-FY26 (2026-06-03). **The FQ3'26 call of 2026-09-02 is missing from the corpus** — the call that set the numbers this DCF exists to value. Not pulled, gap not flagged. Zero quotes produced. What it said (Jefferies Asia TMT 09-02 + JPM callback): Hock Tan — **"$115bn in 2027, $230bn 2028 … this $115bn is the right number for now; if we can scale up supply we will update this number. The same applies to 2028."** DCF CY28 AI revenue = ASIC $284,635m + networking $70,000m = **$354,635m, 54% above the company's own $230bn FY28 guide**, reconfirmed 09-15.

**AMD:** Q3-25, Q4-25, Q1-26, **Q2-26 (2026-08-04)** and the 2025-11-11 Analyst Day all on disk; zero quotes. Source model `AMD WIP.xlsx` saved **2026-07-30, five days before the Q2'26 print.**

| Management (Lisa Su, 2026-08-04) | DCF |
|---|---|
| Server CPU market "approximately **$220 billion by 2030**" | `Capa!K51` = **$59,295m** 2030 TAM (3.7x too low; x86 TAM pinned at 20m units flat, ~$2,000 ASP) |
| Server revenue "**more than 70%** for the full year 2027" | CPU revenue +35.3% (G58→H58) |
| Data center segment "**more than double**" in 2027 | DC +62.9% ($37,588m → $61,224m) |
| Q3'26 guide "approximately **$13 billion** ± $300m" | CY26 $55,893m − H1 actual $21,789m − Q3 $13,000m ⇒ **Q4'26 = $21,104m, +62% q/q** |

## 4. Unsourced claims, template artefacts, basis mismatches

### 4a. The condemning finding: 2026–2028 chip revenue in BOTH files is a byte-copy of the NVDA template

The prior analyst's own QA script `E:\outputs\avgo-amd-dcf-20260916\audit_20260917_sources.py` asserts that `Capa DCF - Base` rows **65 (Broadcom)** and **70 (AMD)**, columns D–I (CY23–CY28), **equal the NVDA template** and reports 0 differences as a PASS. The "177/207 source cells, 0 differences" headline is a copy-fidelity check, not a validity check.

**AMD:** `Capa!G70/H70/I70` are literal constants 20,668 / 38,433 / 51,772 (the NVDA template's "AMD" accelerator allocation); row 77 (DC GPUs) `=G70`. House model `AMD WIP.xlsx!DC detail!EP18:ER18` = 14,723 / 35,073 / 50,002. Gap **+$5,945m (+40.4%) CY26**, +$3,360m CY27, +$1,770m CY28 — exactly row 87 "Cenário − modelo oficial". Every dollar of AMD's premium over the house model is the template constant. `G70`/`I70` are numerically identical in the AMD and AVGO files.

**AVGO:** the 09-17 rewire added `Compute e Networking` and made drivers *respond*, but `Premissas!C84` "Base dos shares AVGO em 17-set-2026" rows 86–97 are hard-coded template copies; the "editable" inputs `I9` = 27.794% (ASIC share of compute TAM) and `I11` = 88.479% (AVGO share of ASIC) are **back-solves** that reproduce them, enforced by tie-out `Compute e Networking!I17 = ROUND(I12−I16,6) = 0`. DCF before edit 720.4492290355652, after 720.4492290355676. `Capa!I77` = **$284,635m** CY28 ASIC vs house `Revenue Bottom up!EJ9` **$180,000m** (+58.1%, unsourced). `I9`/`I11` held constant CY28–CY45: AVGO keeps 88.5% of custom ASIC for 20 years, leaving $37bn for MRVL + MediaTek + Alchip against MediaTek's own guided 15–20% 2027 share (~$14bn, on `_wiki/AVGO.md`).

**Dead drivers:** in the AMD file `G8`/`I8` chip capex and `G77`/`I77` are constants, so the 09-17 driver tests correctly returned 0.0 for 2026/2028; only 2029+ is live. **The AMD file was never revisited after the AVGO rewire.** The test labelled "AMD CPU share 2028 +1pp" was run inside the AVGO workbook.

### 4b. The CPU block

`Premissas!I52 = I29/I31` = 14.4607 / **20** = 0.7230, byte-identical in both files. `I31 = 20m` x86 units is a hand-typed constant, flat CY23–28, no source. In CY23–28 it is circular and revenue-neutral (`I57 = I47*I55` = units); from CY29 it is load-bearing (3%/yr off a 72.3% share of 20m forever). **In the AVGO file the block sits inside a Broadcom valuation** with the label "AMD | participação em unidades x86" — and it is not inert: `Capa!D12 = (D10−D11)*Premissas!D48` subtracts the AI-CPU pool before the 35% networking allocation, so the CPU-AI split (row 46: 20%→45%) directly sizes AVGO's networking TAM. Leftover AVGO source notes (`AB59/AB60`) also sit in the AMD file.

### 4c. Hard-coded inputs with no attributed source

| Cell | Value | Status |
|---|---|---|
| `Premissas!D36` WACC | 10% for both (net-cash AMD and 4.9x-levered AVGO) | Self-labelled "Hipótese… não é estimativa de mercado atual". Arete 13.9% on AVGO (2026-07-21). AVGO grid stops at 12% ($540.59); 13.9% ≈ $400–430 off-grid |
| `Premissas!D37` g | 2.0% | From NVDA template `Capa!D91` |
| `Premissas!D38` | 0.20 = terminal incremental ROIC (`Capa!C116`; `D124 = D123*D115/D116`) | "Nova hipótese", no benchmark |
| `Premissas!D35` valuation date | 2026-08-27 | Template carry; compared to a 09-17 close |
| `Premissas!I31` | 20m x86 units flat | No source |
| `Premissas!I32` | $1,975.62 AMD ASP as market x86 proxy | Self-flagged "não observação independente" |
| `Premissas!I46/I47/I48` | 0.45 / 0.25 / 0.35 | "Hipótese" ×3; `I48` +10pp = +$40.48/sh on AVGO |
| `Capa!G8/I8/G10/I10/G65/I65/G70/I70` | 399,900 / 1,157,436 / 178,576 / 715,097 / 60,380 / 284,635 / 20,668 / 51,772 | Byte-identical NVDA constants in both files |
| `Premissas!I63/I64/I65` | D&A, capex, NWC intensities frozen at CY25 → 2045 | AMD NWC/rev 32.64% vs ~22.6% on the 08-05 10-Q (AP doubled to $5,359m) |
| `Premissas!D39` | Diluted shares frozen at CY26 proxy | Contradicts same sheet row 19 (AMD 1,760.05m CY28) |

### 4d. Basis mismatches the QA never caught

1. **AVGO segments don't reconcile to their own total:** rows 8+9+10+11 vs row 7 off by +$259m CY23, +$1,773m CY25, +$5,951m CY26, −$2,314m CY27, −$1,397m CY28 — AI pulled from `Revenue Bottom up` row 8 ("Bottom up") while the total uses row 7 ("AI"). `max_reconciliation = 0` never tested this.
2. **CY vs FY:** house models are calendar (correct), but the CY28 output was compared to FY-based Street marks without stating the basis, and the $230bn FY28 guide was never cross-walked to CY28.
3. **Margins calibrated on house revenue, applied to inflated scenario revenue:** AVGO gets +$104.6bn at 4.39% opex intensity; AMD books +$5.9bn DC-GPU at 55.6% corporate GM when UBS (Arcuri, 2026-08-05) has incremental GPU dollars "below corp avg".
4. **AMD revenue shape incoherent:** CY26 $55,893m = +10.5% vs BBG cons $50,561m and above the Street high $53,978m; CY27 $80,625m = −9.0% vs cons $88,626m and −28.7% vs Street high $113,162m (`_data/estimates.json` asof 2026-09-17).
5. **Market-cap sanity:** AVGO equity `D129` $3,553.8bn vs BBG mkt cap $1,721.2bn (2.06x); AMD $489.9bn vs $896.4bn (0.55x).
6. **Outside the entire Street range:** AVGO $720.45 vs PT cons $531.89 / hi $715 / lo $350; AMD $295.79 vs PT cons $628.15 / hi $1,250 / **lo $465** (MS, 2026-08-05) — 36% below the lowest target on the Street.
7. **AMD accelerator share pinned at 4.47% to 2045** (`Premissas!I53`), below the wiki's ~5–7% frame, while the CY26 GPU line is a bull override — the two halves argue against each other.

### 4e. No wiki trace — confirmed

Zero hits for "Template DCF", 720.4 or 295.79 in `_wiki/AMD.md` or `_wiki/AVGO.md`; no Changelog entry 2026-09-16/17; no `_meta/outcomes.md` line. Only trace: lint line `_meta/staleness.md:24` "newer on P: (E: copy stale): Template DCF AVGO.xlsx". Nothing equivalent to `_meta/audits/nvda_dcf_20260831/`. **Thesis-drift rule violated.**

Credit: the analyst did document several assumptions honestly in the source columns (`F36` WACC carry, `C134` flat 20m TAM, `F42` BS staleness, `F39` constant-share proxy, `C135` "CY23–25B are scenario bases, not reported history"). Real discipline, buried in a workbook nobody was told about.

## 5. Required next actions (ordered)

**Stop-ship**
1. Do not circulate $720 or $296.
2. **AVGO — re-base the ASIC line.** Replace `Compute e Networking!G9:I9` and `G11:I11` with values derived from the $115bn FY27 / $230bn FY28 AI guide (Hock Tan, 2026-09-02), calendarised. The house model `Premissas!H8:I8` ($90bn/$180bn ASIC) and `H9:I9` ($40bn/$70bn networking) is already calibrated to it — use it. Delete frozen `Premissas!D86:Z97` and the `Compute e Networking!17` tie-out.
3. **AMD — replace `Capa!D70:I70` with `AMD WIP.xlsx!DC detail!EM18:ER18`** (14,723 / 35,073 / 50,002 CY26/27/28) and relink row 77 to the house series. Re-derive `Premissas!I53`.
4. **AMD — refresh the source model** (2026-07-30 → post Q2'26: revenue $11,536m, DC $6,718m, Q3 guide $13.0bn ±$300m, GM ~56%, server >70% FY27, DC "more than double" 2027). Sanity-gate CY26 against H1 $21,789m + Q3 $13,000m.
5. **AMD — fix the server-CPU TAM** (`Premissas!D31:I31` 20m flat → 2030 TAM $59.3bn vs mgmt "~$220bn by 2030"). **Delete the CPU block from the AVGO file** and re-source `Capa!D12` networking TAM.

**Inputs needing a source or haircut**
6. Per-name WACC; show DCF at Arete's 13.9% (AVGO); extend the AVGO grid `F116:K120` past 12%.
7. Balance sheets: AVGO cash $23,975m / debt $59,419m / net debt $35,444m / diluted 4,887m (10-Q 2026-09-10); AMD cash+STI $13,111m / debt $3,226m / net cash $9,885m / diluted 1,659m (10-Q 2026-08-05). Set `D42` to actual quarter-end dates.
8. Share count: honour `Premissas!I19` dilution path (AMD 1,760.05m CY28 → $278.36) or delete row 19.
9. AMD NWC `Premissas!I65` 32.64% → re-base to ~22.6% off Q2'26 or cite a filing.
10. Fix the AVGO extraction break (rows 8–11 must reconcile to row 7; pick one AI series).
11. Roll valuation date from 2026-08-27 to build date.

**Coverage owed**
12. Pull the AVGO FQ3'26 transcript (2026-09-02) via `fetch_transcripts_marketbeat.py`; reconcile Hock Tan's $115bn/$230bn and "focus on OPERATING margin, not gross margin" against `Capa!I90` (66.1% GM) and `I96` (59.1% EBIT).
13. Read the 267 emails — at minimum the 09-02/03/04 AVGO post-print notes, the 09-15 "targets reiterated" pair, the two MS AMD model files, MS PT $465, the Barclays Bogey Surveys, Capstone's five callbacks.
14. Wiki Changelog entries on `_wiki/AMD.md` and `_wiki/AVGO.md` (house DCF exists, base value, valuation date, WACC/g/ROIC, variance to Street) — owed since 2026-09-16.
15. Audit folder per name at `_wiki/_meta/audits/` matching the NVDA standard (this folder is the start).
16. Invert `audit_20260917_sources.py`: flag any `Capa` row 64–72 cell in D:I that still equals the NVDA template.

## 6. Bottom line

**AVGO — FAIL.** `Capa!I77` values Broadcom's CY2028 ASIC business at $284,635m, a byte-copy of the NVDA template's "Broadcom" line, against the house model's $180,000m and management's $230bn FY28 AI guide (2026-09-02, reconfirmed 09-15, the day before the build). CY28 total $418,626m is 75% above Arete's Street-high FY28 group revenue ($239bn, 2026-07-21); implied equity $3.55trn is 2.06x the current market cap. The 09-17 rewire made drivers respond without changing the output to 13 significant figures — it made the model look live without making it right. The stale balance sheet, the 10% WACC, the AMD CPU block inside a Broadcom valuation and the non-reconciling segment extraction are all secondary to the headline number not being a Broadcom forecast at all.

**AMD — FAIL.** CY2026 $55,893m requires a Q4'26 of $21,104m, +62% q/q off the company's own $13.0bn Q3 guide. The entire premium over the house model (+$5,945m CY26) is the NVDA template's hard-coded "AMD" constant at `Capa!G70`, certified by the analyst's own QA because it matched the template. The 2027–2045 path rides a house model saved five days pre-print, carrying +35.3% server CPU vs guided >70%, +62.9% DC vs "more than double", a $59.3bn 2030 server-CPU TAM vs "~$220bn", and a 4.47% accelerator share pinned to 2045. $295.79, 36% below the lowest Street target ($465, MS 2026-08-05), is not a variant perception; it is the arithmetic of a stale model and a dead driver.

**Pair — FAIL.** Two DCFs produced, self-audited and reported on zero emails (267 available), zero SEC filings (11 on disk), zero transcript quotes (16 on disk; the decisive AVGO one not pulled). The QA run was internal-consistency plumbing whose "source" leg tests that the files still match the NVDA template. Neither model is documented in `_wiki/`, so a $720 Broadcom and a $296 AMD target sit on P: that nobody can trace, reproduce or challenge. Re-base both off the house models and management's 2026-08-04 / 2026-09-02 guides before either number leaves the workbook.
