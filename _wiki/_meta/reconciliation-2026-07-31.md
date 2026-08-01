# Reconciliation — 2026-07-31 (/run-inbox)

_Source ingested this run: **Bernstein · David Dai / Carmine Milano / Juho Hwang — "ASML: Best Idea 3Q26 — WFE upcycle, rising litho intensity, and pricing upside", 2026-07-30** (29p) → [`relatórios bons/BERN_258544.html`](../../relat%C3%B3rios%20bons/BERN_258544.html)._

**Baselines used:** (1) prior wiki comments on disk · (2) Capstone house model (`ASML_Peers_SemiCap_v16.xlsx`, Peer Comp, dated **2026-06-15**, transcribed on [ASML.md](../ASML.md) `## Capstone estimates`) · (3) **BBG consensus — LIVE, pulled 2026-07-31** via `E:\bloomberg_api` (`bdp`, `BEST_FPERIOD_OVERRIDE` 1FY–5FY). ✅ Terminal was logged in; no PENDING columns this run.

⚠️ **Scope note:** only the ASML leg of this ingest carried new *quantitative* datapoints. The eight read-through patches (AMAT, KLAC, LRCX, TOKYOELEC, INTC, SAMSUNG, SKHYNIX, TSM) carried **no new rating, PT or house-model-comparable estimate** — they relay peer-comp exhibits and a High-NA adoption roadmap. Those are reconciled qualitatively at the bottom.

---

## 🔴 DIVERGES — the alpha

_Machine-readable summary (parsed by `build_edge.py` into the standing edge tracker); the narrative and the arithmetic follow below._

| # | Name | New datapoint | Baselines | Read |
|---|---|---|---|---|
| D1 | **ASML** | Bernstein EPS 26/27/28E **€38.91 / €53.56 / €75.25** | Live BBG cons **€36.43 / €51.00 / €64.95** = **$41.99 / $58.79 / $74.86** @1.1527; **Capstone house $39.63 / $56.85 / $68.74** (2026-06-15) | ⚠ **The house model has been overtaken — sign flipped.** House is now **−5.6% / −3.3% / −8.2% BELOW consensus** and ~21% below Bernstein in 2028E. The page's standing "well above consensus (NTM ~34.87)" claim is **stale and now false**; the cited consensus anchor is itself ~€36.4/$42 today. **Action: refresh `ASML_Peers_SemiCap_v16.xlsx`.** Flag added to the page in two places. |
| D2 | **ASML** | Bernstein PT **€2,500** / ADR **$2,859** (unchanged, reiterated) | BBG cons PT **€2,013.16** (NA) / **$2,459.79** (ADR) | **Street-high confirmed: +24.2% above the mean PT locally, +16.2% on the ADR.** ⚠ The two consensus PT lines don't reconcile with each other (€2,013 × 1.1527 = $2,320 vs $2,460, ~6% gap — different contributor sets); state which line you're quoting. |
| D3 | **ASML** | Bernstein vs cons: rev **+3.0% / +2.6% / +9.7% / +12.4% / +20.6%**, EPS **+6.8% / +5.0% / +15.9% / +21.9% / +41.2%** (26-30E) | Same BBG series, verified cell-by-cell (see C1) | **The entire gap is out-year — this is a DURATION call, not a near-term-numbers call.** Consensus decays revenue growth to **+11% / +5%** in 29/30; Bernstein holds **+14% / +13%**. Near-term print risk ≈ nil (Bernstein is ~at consensus for 26-27). Falsifiable at two physical claims: DRAM EUV exposures → **26.3 MWPM by 2030** (4.5x) and blended litho intensity → **28%**. Margin split: GM gap trivial (~90bp), **OPM gap 350bp** — the disagreement is operating leverage, not pricing. |
| D4 | **ASML** | MS FY28e EPS **€56.42** (35x → PT €1,930) vs Bernstein **€75.25** (40x on Q5-8 €62.6 → €2,500) | BBG cons FY28E **€64.95** | **The page's "same thesis, different multiple" framing is incomplete.** MS sits **~13% BELOW consensus** on the out-year EPS base while Bernstein sits ~16% above — roughly half the ~30% PT gap comes from the EPS base, not the 40x-vs-35x multiple. Correct that row next time it's touched. |
| D5 | **ASML** | Note's headline **"84% upside"** and **"only 20x our 2028 EPS"** | Off the **29-Jul close €1,362.20**; live **PX_LAST €1,434.20** (+5.3%) | **Upside is now 74.3%, not 84%** — don't carry 84% as a live number. The 20x claim survives: €1,434.20 / €75.25 = **19.1x** (18.1x at the note's close). |

### D1. **The Capstone house model on ASML has been OVERTAKEN by consensus and the page's standing claim is now false.** ← highest-value finding this run

[ASML.md](../ASML.md) `## Capstone estimates (house model)` carries: *"**House read:** EPS 2026E \$39.63 / 2027E \$56.85 / 2028E \$68.74 — **well above consensus (NTM ~34.87)**. (Capstone peer model, 2026-06-15)"* — and the `## Debate` section repeats it (*"well **above consensus** (NTM ~\$34.9, Street-high ~\$38.7)"*).

That was true on 2026-06-15. **It is not true today.** The 2026-07-15 beat-and-raise and the subsequent estimate cascade moved consensus straight through the house numbers:

| Diluted EPS | 2026E | 2027E | 2028E |
|---|--:|--:|--:|
| **Capstone house (USD, 2026-06-15)** | **\$39.63** | **\$56.85** | **\$68.74** |
| BBG consensus (EUR, live 2026-07-31) | €36.43 | €51.00 | €64.95 |
| → BBG consensus in USD @ EURUSD 1.1527 | **\$41.99** | **\$58.79** | **\$74.86** |
| → BBG consensus in USD @ Bernstein's implied 1.1311 | \$41.20 | \$57.69 | \$73.46 |
| **House vs consensus** | **−5.6%** | **−3.3%** | **−8.2%** |
| Bernstein (EUR) | €38.91 | €53.56 | €75.25 |
| → Bernstein in USD @ 1.1527 | \$44.85 | \$61.74 | **\$86.74** |
| **House vs Bernstein** | **−11.6%** | **−7.9%** | **−20.8%** |

**The sign has flipped: the house model is now BELOW consensus in all three years**, and ~21% below Bernstein in 2028E. The conclusion is robust to the FX assumption across the 1.13–1.15 range (the house model's own EUR/USD assumption is not recorded on the page — ⚠️ worth capturing on the next refresh).

**Why this matters and what to do:** the page's investment case leans on "house is above the Street," which is currently backwards. Either (a) the house model has genuinely become the conservative view and the position should be re-sized against a Street that has moved past it, or (b) the model simply has not been refreshed through the Q2 print — the far more likely explanation given the 2026-06-15 stamp and the fact that the "NTM ~34.87" consensus anchor it cites is now ~€36.4/\$42. **Action: refresh `ASML_Peers_SemiCap_v16.xlsx` and correct the two "well above consensus" claims on [ASML.md](../ASML.md).** Until then treat the house EPS line as stale, not as an edge.

### D2. **Bernstein's PT is +24% above the consensus mean PT — Street-high confirmed, and the gap is wider than the page implies.**

| | Bernstein (2026-07-30) | BBG consensus PT (live) | Gap |
|---|--:|--:|--:|
| ASML NA (EUR) | **€2,500** | €2,013.16 | **+24.2%** |
| ASML US ADR (USD) | **\$2,859** | \$2,459.79 | **+16.2%** |

Both confirm the page's "Street-high" label. ⚠️ **Data-quality flag, not a thesis point:** the two consensus PT lines do not reconcile with each other — €2,013.16 × 1.1527 = **\$2,320** vs the ADR line's **\$2,459.79**, a ~6% discrepancy, almost certainly different contributor sets on the local vs ADR listing. When quoting "ASML vs consensus PT," state which line is being used.

### D3. **The Bernstein–consensus gap is entirely an OUT-YEAR gap. Near-term print risk is negligible; the whole call is duration.**

Verified against live BBG (see C1 — the two consensus series are the same numbers):

| | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|--:|--:|--:|--:|--:|
| Bernstein revenue (€bn) | 44.0 | 55.9 | 71.9 | 81.9 | 92.1 |
| Consensus revenue (€bn) | 42.7 | 54.5 | 65.5 | 72.8 | 76.4 |
| **Δ revenue** | **+3.0%** | **+2.6%** | **+9.7%** | **+12.4%** | **+20.6%** |
| **Δ EPS** | **+6.8%** | **+5.0%** | **+15.9%** | **+21.9%** | **+41.2%** |
| Consensus revenue growth y/y | +31% | +28% | +20% | **+11%** | **+5%** |
| Bernstein revenue growth y/y | +35% | +27% | +29% | **+14%** | **+13%** |

**The falsifiable core: consensus decays ASML's growth to +11%/+5% in 2029-30; Bernstein holds +14%/+13%.** That is a bet on the WFE upcycle not rolling over at the end of the decade — not a bet on the next two prints. It maps to two testable physical claims the note makes: DRAM EUV exposures reaching **26.3 MWPM by 2030 (4.5x from 3.4 in 2025; 26% → 44% of all EUV exposures)** and blended litho intensity reaching **28% (DRAM ~30% at 1d)**. Track those, not the quarterly beats.

Same shape on margins: Bernstein **GM 60% / OPM 50% by 2030** vs consensus **59.1% / 46.7%** — the GM gap is trivial (~90bp), the OPM gap is 350bp, i.e. the disagreement is about **operating leverage**, not pricing pass-through.

### D4. **Bernstein vs MS: a ~30% PT gap on near-identical near-term numbers — reconfirmed with live data.**

The page already logs this (Bernstein €2,500 = 40x on Q5-8 EPS €62.6 vs MS €1,930 = 35x on FY28e €56.42). Live BBG consensus FY28E EPS is **€64.95** — i.e. **MS's FY28e of €56.42 sits ~13% BELOW consensus**, while Bernstein's €75.25 sits ~16% above. So the "same thesis, different multiple" framing on the page is incomplete: **MS is also below the Street on the out-year EPS base**, and roughly half the PT gap comes from that, not from the 40x-vs-35x multiple. Worth correcting the characterisation the next time that row is touched.

### D5. **Stock has moved since the note's cut-off — the headline upside figure is stale by ~10 points.**

Bernstein's "84% upside" is off the **29-Jul close of €1,362.20**. Live **PX_LAST €1,434.20** (+5.3%, consistent with the "+6% pop" the 07-31 spec-sales row describes). **Upside to €2,500 is now 74.3%.** The note's "only 20x our 2028 EPS" claim still holds: €1,434.20 / €75.25 = **19.1x** (was 18.1x at the note's close). Minor, but the page should not carry 84% as a live number.

---

## BBG consensus pull — live, 2026-07-31

_Every name touched by this ingest. Spot and consensus PT in local currency. `bdp(PX_LAST, BEST_TARGET_PRICE)`, Terminal logged in._

| Ticker | Spot | Cons PT | Ccy | Read |
|---|--:|--:|---|---|
| ASML NA Equity | 1434.20 | 2013.16 | EUR | Consensus sees +40%. Bernstein's €2,500 is **+24% above the consensus PT** — the Street-high. |
| ASML US Equity | 1629.00 | 2459.79 | USD | ADR line; +51% to consensus PT. ⚠ Does not reconcile with the NA line at spot FX (~6% gap) — different contributor sets. |
| AMAT US Equity | 507.67 | 623.00 | USD | +23%. Read-through name only — no new AMAT estimate in this note. |
| KLAC US Equity | 182.82 | 234.07 | USD | +28%. Bernstein has KLA **last of five** on both revenue (22%) and EPS (28%) CAGR CY25-28. |
| LRCX US Equity | 293.02 | 372.48 | USD | +27%. Bernstein has LAM **2nd of five** on growth (rev 28% / EPS 38%) — corroborates Lam IR's own 07-31 framing. |
| 8035 JP Equity | 55500.00 | 74485.87 | JPY | +34%. Tokyo Electron — the correctly-routed "TEL" (see the dropped-route note). |
| INTC US Equity | 90.20 | 119.28 | USD | +32%. Qualitative read-through only (18A High-NA HVM validation). |
| TSM US Equity | 404.25 | 549.33 | USD | +36%. Qualitative read-through only (High-NA deferred to ~A10). |
| 005930 KS Equity | 259000.00 | 488627.10 | KRW | +89%. Samsung Electronics. Qualitative read-through (2× EXE:5200B, "industry reports" sourcing). |
| 000660 KS Equity | 1718000.00 | 3292948.00 | KRW | +92%. SK hynix — named the lead High-NA adopter. |

⚠ **Read the KRW upside figures with care** — Samsung and SK hynix have both had violent positioning-driven moves this week (the 07-30 Situational Awareness unwind logged on both pages), so spot is unusually noisy and the implied upside overstates the fundamental gap.

## 🟢 CONFIRMS — no action

### C1. **Bernstein's "consensus" column IS live BBG consensus, matching to the decimal. Their gap arithmetic is verified and directly reusable.**

| | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|--:|--:|--:|--:|--:|
| Bernstein's stated consensus EPS (€) | 36.43 | 51.00 | 64.95 | 75.19 | 81.34 |
| **BBG `BEST_EPS` 1FY–5FY, pulled 2026-07-31** | **36.427** | **51.000** | **64.945** | **75.191** | **81.342** |
| Bernstein's stated consensus revenue (€bn) | 42.7 | 54.5 | 65.5 | 72.8 | 76.4 |
| **BBG `BEST_SALES` 1FY–5FY (€mn)** | **42,686** | **54,488** | **65,535** | **72,839** | **76,367** |

Exact across all ten cells. This is the cleanest validation of a broker's consensus column logged on this wiki — it means the +6.8%/+5.0%/+15.9%/+21.9%/+41.2% EPS deltas can be quoted without re-derivation.

### C2. **ASML's own growth CAGRs check out against the published table.**
Recomputed from the note's own numbers: revenue CAGR CY25-28 = (71,891 / 32,667)^⅓ − 1 = **30.1%** ✓ (stated "30%"); EPS CAGR = (75.25 / 24.72)^⅓ − 1 = **44.9%** ✓ (stated "45%"). Consensus on the same basis: revenue **26.1%**, EPS **38.0%** — so the "ASML has the best growth in the group" claim survives even on the Street's own numbers, not just Bernstein's.

### C3. **PT unchanged — no thesis drift to record.**
Outperform / €2,500 / ADR \$2,859 / 40x target multiple are all identical to the marks logged on 2026-07-15 (Dai, "Triple happiness", €2,300→€2,500) and 2026-07-20 (Rasgon, "WFE / AI GW note"). EPS 25A/26E/27E (€24.72 / €38.91 / €53.56) are also identical. The note **extends** the line to FY28-30 rather than revising it, and the 40x-on-Q5-8-EPS-of-€62.6 construction is internally consistent with the new FY27 €53.56 / FY28 €75.25. **Nothing moved to Changelog** — correctly, per the thesis-drift rule.

### C4. **The litho-intensity number is a refinement, not a contradiction.**
Page previously carried Bernstein's summary framing ("20% to close to 30%"); the body gives **24% → 28% by 2028** blended. Both are in the same document (cover summary vs Exhibit 1) and describe different things — the summary is the DRAM trajectory, the body is the blended average. Logged both, no supersede.

---

## ⚠️ Data-consistency items found while reconciling (not thesis, but should be fixed)

1. **The auto-injected snapshot block on [ASML.md](../ASML.md) disagrees with the FY consensus by ~4% in 2027.** The `SNAPSHOT` block (asof 2026-07-31) shows CY2027E EPS **€53.06**; live `BEST_EPS` 2FY is **€51.00**. ASML's fiscal year IS the calendar year, so these should match. The snapshot is built by `fetch_estimates.py` from **quarterly (`nFQ`) aggregation**, which is not identical to the FY consensus line, and the underlying `estimates.json` fetch may predate the asof stamp. Blended-forward is a third answer again (`1BF` €44.89 / `2BF` €59.07 — rolling 12m, correctly different). **Net: the page currently shows two different 2027 consensus EPS figures. Pick the FY line for broker comparisons.** → candidate for `/wiki-consensus`.
2. **Bernstein's own note is internally inconsistent on two peer CAGRs** — the valuation paragraph says LRCX 26% / KLAC 21% revenue CAGR, Exhibit 18's caption says LAM 28% / KLA 22%. Exhibit-18 values were used in the patches, with the discrepancy flagged inline on ASML, LRCX and KLAC. Peer ranking is unaffected either way.
3. **AMAT's 30% China figure is CYQ1-only** (AMAT had not reported CYQ2 at publication) — not comparable to the other four names' 1H figures. Flagged on both AMAT and ASML.
4. **Per-name WFE peer P/E bars (Exhibit 20) were deliberately NOT transcribed** — the bar labels extract as an unordered number list and cannot be safely mapped to names. Only ASML's 31.0x / 23.5x and the group average 31.3x / 24.9x were taken, both stated in body text. No fabricated peer multiples entered the wiki.

---

## Read-through patches — qualitative reconciliation (no new estimates)

| Page | New datapoint | Reconciles vs prior wiki? |
|---|---|---|
| **INTC** | Bernstein: Intel 18A HNA adoption "confirms the technology is ready for HVM" | ✅ **CONFIRMS** — [ASML.md](../ASML.md) already carried "Intel is now running High-NA in production on its most advanced node (18A)" (didier expert call, 2026-07-15) and "Intel accepted its EXE:5200B for HVM" (Q4/FY25). Third independent confirmation. |
| **TSM** | HNA insertion delayed to ~A10, end of decade | ✅ **CONFIRMS** — page already carried "Bernstein has TSMC as the slowest adopter (~2030, at A10), having publicly called High-NA 'too expensive'" (2026-07-06) and BofA's litho expert calling TSMC a deliberate slow-adopter (2026-05-21). Consistent across three dates. |
| **SKHYNIX** | EXE:5200B assembled at M16, Sept 2025; lead DRAM HNA adopter | ✅ **CONFIRMS** — ASML IR (07-20) had SK Hynix "very vocal" about moving fast on High-NA. |
| **SAMSUNG** | Two EXE:5200B ordered (late-2025 + 1H26) | ⚠️ **NEW, and weakly sourced** — Bernstein attributes this to *"industry reports,"* not company disclosure. No prior wiki datapoint on Samsung HNA tool orders. Logged with the sourcing caveat; **do not promote to a hard number without corroboration.** |
| **AMAT / KLAC / LRCX / TOKYOELEC** | China exposure 1H CY26 (30% / 25% / 29% / 27%) and consensus growth CAGRs | ⚠️ **Partially checkable.** The China percentages are company-reported and have no consensus equivalent — no prior wiki figures on this basis to compare against, so logged as new. The CAGRs are **BBG consensus, CY-adjusted by Bernstein**; a direct BBG re-derivation is not meaningful here because AMAT (Oct FY), KLAC/LRCX (Jun FY) and TEL (Mar FY) all require the CY adjustment Bernstein performed and did not publish. **Not independently verified — flagged as such rather than treated as confirmed.** |
| **ASML China 16% of 1H26** | vs page's "China just 14% [of Q2 revenue]" (Bernstein/Redburn, 07-15/16) | ✅ **CONSISTENT** — different bases, not a contradiction: 14% is Q2 alone, 16% is 1H26. Both sit below the FY26 ~20% guide, which is exactly the "sharp 2H reaccel" the page already flags as the swing item. |
