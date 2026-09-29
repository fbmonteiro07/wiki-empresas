# Reconciliation — run-inbox 2026-09-28 (23h)

_11 sources (3 dropped in `_inbox` + 8 swept off `P:\US Equities\Relatórios para a wiki`). Every NEW quantitative datapoint is reconciled against (1) what the wiki already carried, (2) the Capstone house models (`_data/house.json`, asof 2026-09-28, read from `raw_rows`), and (3) BBG consensus. **BBG leg: the Terminal is DOWN (port 8194 refused at 23:18), so the consensus column is the on-disk `_data/estimates.json` snapshot, asof 2026-09-28 — same-day, so it is used as the baseline rather than marked PENDING.** Fiscal-vs-calendar mappings that could not be verified against the snapshot's own period labels are flagged, not asserted. Web data was not used anywhere._

Sources: Bernstein Weed/Moerdler "META hires MDB CEO" (09-28) · Jefferies Thill "AI Summit Recap" (09-24) · Goldman Portfolio Strategy Hammond/Snider "AI capex, required revenues, and what's priced in" (09-24) · Goldman Sheridan/Borges/Schneider "Sizing the AI Economy Needed to Justify ROIC on Hyperscaler AI Capex" (09-24) · Stratechery "Apps, Agents, and Aggregation" (09-28) · SemiAnalysis "How GLM5.3 Sparse Attention Affects HBM Memory Usage" (09-28) · Morgan Stanley Gutman/Nowak "Muse: Rewriting the Retail/Consumer Playbook" (09-28) · Jefferies expert call w/ Horizon Media exec (09-28) · Jefferies Colantuoni "ABNB/BKNG/EXPE: Skift takeaways" (09-27) · Deutsche Bank Weathers "Top Questions into Semicon West 2026" (09-27) · Capstone "OpenAI DevDay 2026 preview" (09-28, circular — link only, nothing reconciled).

---

## 🔴 THE HEADLINE — the house is BELOW the Street on META capex and ABOVE it on AVGO AI revenue, and the two Goldman notes disagree with each other by ~$60-240bn on what "AI capex" is

Read together, the two Goldman primaries put per-company CY26-27 capex on the page for the first time (Visible Alpha consensus as of 23-Sep, confirmed on the page image, not from pdfplumber):

| Company | VA consensus CY26-27 capex (GS Ex.1) | GS "Phase 2" AI-compute capex CY26-27 (GS Ex.4, 85-90% of total) | BBG snapshot FY1+FY2 capex | Capstone house CY26-27 capex | House vs consensus |
|---|--:|--:|--:|--:|--:|
| **META** | **$333bn** (YE25: $230bn) | $308.7bn → ~7GW | $139.3 + $197.9 = **$337bn** | **$131 + $170 = $301bn** (`Modelo Meta pós 2Q26`, 06-11) | **−10%** |
| **GOOGL** | **$507bn** (YE25: $253bn) | $470.1bn → ~11GW (GS-implied total ≈ $553bn at 85%) | $201.8 + $309.4 = $511bn | $183 + $310 = $493bn (`Google Modelo oficial`, 06-05) | −3% vs cons, **−11% vs GS-implied** |
| AMZN | $505bn (YE25: $301bn) | $424.3bn AWS-segment → ~10GW | $221.6 + $281.3 = $503bn | no house model | — |
| MSFT | $373bn (YE25: $227bn; PP&E adds excl. leases) | $327.3bn → ~8GW | $188.9 + $217.1 = $406bn ⚠ FY-Jun basis | no house model | — |
| ORCL | $174bn (YE25: $126bn) | $165.3bn → ~4GW ("illustrative — Oracle primarily leases") | $92.1 + $103.9 = $196bn ⚠ FY-May basis | no house model | — |
| SPCX | n/a | $30.6bn AI-segment → ~1GW | $68.3 + $169.2 = $237.6bn (total company) | no house model | scope gap: GS counts AI segment only |
| **5-name total** | **$1,892bn** (+66% / +$754bn YTD) | $1.73trn incl. SPCX | FY1 $844bn / FY2 $1,110bn | | |

➤ **META is the actionable gap.** The house model is ~$32-36bn (10%) below both Visible Alpha and BBG on CY26-27 capex, on a page where the bull case leans on Muse and the bear case on capex. Either the house is under-modelling the Muse compute ramp (Stratechery quotes a 2-core / 8GB RAM / 8GB storage VM per Muse user; MS calls Muse "the most credible agentic threat we have seen") or the Street is over-extrapolating the +45% YTD revision — the model needs a bridge either way. The house's 2027 FCF (−$23bn per `raw_rows`) already sits on the lower capex.
➤ **The two GS notes do not agree on the aggregate, and the gap is the "who else is spending" number.** Portfolio Strategy: hyperscaler capex $800bn 2026 / $1.1trn 2027 consensus / GS $1.2trn 2027 / $1.4trn 2028. Sheridan's semis bottom-up (Exhibit 3, cells reconciled by column sum: 682+126+31+11+11 = 861; 879+250+85+101+23 = 1,338; 1,091+500+112+263+42 = 2,008): **$861bn / $1,338bn / $2,008bn** on 20 / 35 / 57 GW. The 2026 gap is $61bn; 2027 is $138-238bn; 2028 is $600bn — that is the labs/sovereign/enterprise AI capex the hyperscaler consensus does not carry, and it is the number the `hyperscaler-capex` canonical framing should quote with its scope attached (`_meta/assumptions.md` still frames the aggregate on a hyperscaler-only basis).
➤ The BBG FY2 sum of the five names is $1,110bn — it reproduces the "$1.1trn 2027 consensus" in the GS strategy note, so the snapshot is on the same basis as Visible Alpha (CONFIRMS the baseline itself).

---

## Where the new data DIVERGES

### 1. META — house capex $301bn vs Street $333-337bn CY26-27 (−10%); GS Buy PT $725 sits BELOW the consensus PT
- Capex: see the headline table. Prior wiki comment: the page carried the 09-25 desk relay of the GS note without per-company numbers; nothing superseded, but the house/Street gap is new.
- PT: GS Sheridan **Buy, PT $725** (Sizing note p.19) vs BBG consensus PT **$789.29** (hi $1,000 / lo $580, 79 analysts, rating 4.77); px $715.62. GS is −8% vs the Street median on a Buy — the same "above on thesis, below on price" pattern the 09-24 reconciliation flagged on MU/SKH/CRWV. MS keeps O (disclosure table, price $751.66 on the 03/20/2023 rating date — no PT in the note).
- ⚠ GS strategy footnote: "EBIT margin not applied to META required revenues" — META's required-revenue line in the $300bn breakeven is on a different basis from the other four.

### 2. AVGO — house AI-semis revenue ABOVE Goldman's bottom-up AND above BBG total revenue
- GS Exhibit 3: AI revenue **$57.8bn / $125.5bn / $240.3bn** (2026/27/28; XPU $39.4 / $86.2 / $168.1bn + connectivity $18.5 / $39.3 / $72.2bn) on **5 / 10 / 20 GW** at an assumed $25bn capex/GW. House (`Modelo Avgo pós 2Q26`, 06-10): AI semis **$63 / $132 / $251bn** → house **+9% / +5% / +4%** vs GS. House total revenue $115 / $190bn vs BBG FY1 **$106.0bn** / FY2 **$173.9bn** → house **+8% / +9%** vs consensus.
- The GS 10GW / 20GW figures are AVGO's own FY27/FY28 guidance, and AVGO's stated $20-30bn/GW opportunity would imply $200-300bn / $400-600bn — GS models roughly half of that, the house slightly more than GS. ⚠ FY(Oct) vs CY basis on both the GS and house rows is unverified against the snapshot labels.
- Sinal on the AVGO page held at "$/GW ✗" — the house's implied AI revenue per GW (~$11.6-12.5bn, Capstone arithmetic labelled on the page) is far below AVGO's $20-30bn talk; that tension is now on the page with numbers.

### 3. NVDA — same revenue, different GW × $/GW decomposition (GS fewer GW at higher $/GW than the house)
- GS: **14 / 18 / 22 GW** of NVDA deployments (2026/27/28: Blackwell 12/3/–, Rubin 2/15/19, Feynman –/–/3) with revenue per GW **$25bn Blackwell → ~$40bn Rubin → ~$45bn Feynman** (company statements + GS assumption). House (`Modelo Felipe NVDA`, 06-17): GW sold **~16.0 / ~24.8** (2026/27) at **~$24 / ~$25bn revenue per GW**.
- GS-implied NVDA content revenue ≈ 14×25 = $350bn (2026) and 3×25 + 15×40 = $675bn (2027) vs house DC revenue $379bn / $629bn and BBG FY revenue $410.8bn / $701.3bn (FY27≈CY26 / FY28≈CY27). The totals bracket each other; the split does not: **the house needs ~38% more 2027 GW than GS to hit a lower number because it does not step Rubin up to $40bn/GW.** This is the Rubin-ASP debate stated in GW; it decides whether the 2027 number is volume- or price-led, and CoWoS/HBM read-throughs differ accordingly.
- GS Buy PT (not in this note; page carries $235 from 09-10) vs BBG cons PT $322.97 — no change.

### 4. BKNG — Jefferies initiates the page's first HOLD, PT $200, near the Street LOW
- Jefferies Colantuoni **Hold, PT $200** (+22% vs $163.95) vs BBG consensus PT **$238.95** (hi $301 / lo $188, 42 analysts, rating 4.55); px $163.87. Jefferies is −16% vs the consensus PT and $12 above the Street low. Prior wiki board: MS OW $230 · JPM OW $236 · GS N $225 · Barclays OW $210 · Bernstein MP $188 — Jefferies is now the second-lowest mark. Net-new house, nothing superseded.
- The disagreement is qualitative too: Jefferies carries Fogel's "consumers will still prefer to book on BKNG because of trust/customer service" as the counter to Muse; MS lists EXPE (not BKNG) as "More at Risk" and treats the transaction as defensible. Both are pre-DevDay (29-Sep) — a ChatGPT travel agent is the near-term test.

### 5. MEDIATEK — Goldman's 2027 datacenter-ASIC revenue is ABOVE the company's own guide
- GS Exhibit 3: DC ASIC revenue **US$2.2bn / $20.25bn / $52.5bn** (2026/27/28) on 0.4 / 4 / 11 GW at $5bn revenue per GW. Page carries the company's **US$12-16bn** 2027 guide and JPM/Nomura marks below GS; GS's 2028 is where UBS sits for 2029. BBG snapshot: FY2 revenue NT$1,153.8bn (+73% vs FY1) — consistent with a large ASIC step-up but not decomposable to the GS line. No house model. DIVERGES: GS above guide and above the page's broker marks.

### 6. MSFT and AMZN — the pages were carrying stale PTs (thesis-drift caught by the coverage tables, not by a rating action)
- **MSFT**: Bernstein's coverage table (Weed note p.3) prints **Outperform, PT $660** (px $516.17; EPS $17.28 / $19.96 / $24.01); the page had **$646 (06-22)**. Moved to Changelog. GS Sheridan **Buy $640** (28x SNTM) is new to the page. Both vs BBG cons PT **$570.05** (hi $700) — GS +12%, Bernstein +16% above the median; px $509.22.
- **AMZN**: GS PT history (Sizing note p.26) shows **$375 since 31-Jul-26** (from $335 on 08-Jul-26); the page still carried $335 (07-07). Moved to Changelog. vs BBG cons PT **$330.91** (hi $405) → GS +13% above the median.
- Neither is an alpha call in itself; both are evidence that "where the sell-side stands" blocks go stale on the raise that follows a print — the same failure class as the 09-14 Blayne Curtis attribution drift.

### 7. RDDT — the agency expert's wallet-share growth (+20-25%/yr) is BELOW the Street's revenue growth (+32%)
- Horizon Media (Jefferies expert call, 09-28): Reddit wallet share growing **~20-25% annually**, budgets 30-35% Google / 30-35% Meta / ~30% diversified (5-10% TikTok). BBG snapshot: FY2/FY1 revenue **$4,477mn / $3,386mn = +32%**; cons PT $213.91 (hi $300 / lo $130), px $143.08.
- Not a contradiction (one agency's wallet ≠ platform revenue; pricing and new-advertiser adds sit outside the expert's view), but it is the first bottom-up datapoint on the page that grows slower than consensus, from a large-agency buyer who says he "won't cut Reddit Max". ⚠ Watch vs the "pricing drives most of the growth" line in the same call.

### 8. LRCX — DB's FY27/FY28 EPS are 1.5% / 4% above the snapshot; the printed 2026A P/E does not reconcile
- DB Weathers (09-27): EPS **2026A $5.82 / 2027E $9.60 / 2028E $12.39**, P/E 33.7 / 32.0 / 24.8, EV/EBITDA 27.9 / 25.7 / 20.5, Buy, px $307.16, Top Pick; no PT in the note (the page's standing DB PT $320 from 08-06 is untouched). BBG snapshot: 1FY EPS **$9.46** / 2FY **$11.90** / 3FY $14.09; cons PT $375.55 (hi $475 / lo $285), px $314.47. ⚠ Assumes the snapshot's 1FY = FY-Jun-27; the label is generic.
- $307.16 / $5.82 = 52.8x, not the printed 33.7x, while 2027E and 2028E tie exactly — the 2026A cell is on a different basis (likely a stale column). Logged on the page with the flag; not a divergence on the estimates themselves.

---

## Where the new data CONFIRMS (no action)

| Datapoint (source) | Prior wiki | House | BBG snapshot (09-28) | Verdict |
|---|---|---|---|---|
| Hyperscaler capex $800bn 2026 / $1.1trn 2027 consensus, GS $1.2trn / $1.4trn (GS strategy 09-24) | Already on `hyperscaler-capex` from the 09-25 relay; primaries now on disk | n/a | Sum of 5 names FY2 capex = $1,110bn | ✓ snapshot reproduces the consensus basis |
| GOOGL CY26-27 capex $507bn cons / $470bn GS Phase-2 (GS Sizing 09-24) | page carried GS Buy $435 = note | $493bn (−3%) | $511bn | ✓ house within 3% of consensus; GS PT $435 vs cons $425.75 in line |
| ORCL GS Buy PT $240 (15x 2030E adj NI; raised from $239 on 14-Sep) | no GS PT on page (new) | n/a | cons PT **$240.01** | ✓ exactly at consensus |
| SPCX GS Buy PT $220 SOTP (from $205 on 05-Aug) | page carried $220 (09-25 table) | n/a | cons PT $217.26 | ✓ at consensus |
| MDB Bernstein Outperform PT $484 (coverage table 09-28; "no change to models, PTs or recommendations") | page carried Bernstein $449 (06-16) → moved to Changelog; Barclays $480 (09-02) | n/a | cons PT $467.47 (hi $565 / lo $365); px $334.68 vs Bernstein's quoted $410.44 = −18.5% (the "down as much as 20%" day) | ✓ Bernstein +3.5% above the median, inside the range; the page had missed an earlier raise |
| GS ROIC hurdle: $1.42trn cumulative CY28-30 revenue / ~$11.6bn per GW / 15% ROIC / $42bn per GW / 70-30 compute-shell (GS Sizing) | 09-25 relay said "AWS may only need to realize 60% of its backlog" | n/a | n/a | ⚠ relay corrected: 59.3% is the three-CSP aggregate ($1.00trn required / $1.69trn backlog); AWS is 67.7%, GOOGL 77.7%, MSFT 39.6% |
| AMD $15-20bn revenue per GW; DC GPU revenue $15.7 / $42.3 / $56.0bn (GS Sizing) | page carried AMD's own $/GW talk | no house model | FY1 rev $51.1bn / FY2 $88.2bn total | ✓ consistent (DC GPU 2027 ≈ 48% of FY2 total) |
| MRVL DC ASIC $2.28 / $4.66 / $8.44bn at $5bn per GW (GS Sizing) | JPM $10bn / $16bn (custom total) | n/a | FY1 rev $12.0bn / FY2 $18.3bn | ⚠ basis differs (GS = custom ASIC only, not netted) — flagged on page, not a divergence |
| CRWV sold out through 2027, 500MW online last quarter, $40M/MW shorter-duration deals (Jefferies summit) | page carried UBS init (09-22) capacity framing | n/a | FY1 capex $35.7bn / FY2 $47.8bn; cons PT $139.87, px $85.07 | ✓ qualitative confirmation; $40M/MW is a deal-price datapoint for `ai-compute-deals` (not netted here) |
| Jefferies roster prices/ratings (summit p.41): NVDA BUY $225.51, AMD BUY $614.61, CRM BUY $237.58, SNOW BUY $334.81, OKTA BUY $205.36, PANW BUY $393.30, META BUY $744.10, AAPL Underperform $337.02, CRWV BUY $86.90 | all consistent with page ratings | — | — | ✓ no rating actions |
| GB300 lowest modelled cost at 150 tok/s; GB200 $0.044 vs MI355X $0.238 per M tokens; 13,950 vs 11,873 tok/s/GPU at $2.31 vs $1.86/hr (SemiAnalysis 09-28) | new to `tokenmaxxing` / NVDA / AMD | n/a | n/a | ✓ no consensus analogue; sparse attention does NOT cut HBM capacity (top-k needs full context in HBM) — `hbm-memory` thesis holds |
| Digital ad budgets ~10% y/y 2026 and 2027; no Iran-war / oil impact (Horizon Media expert) | GOOG/META pages had no agency-level budget datapoint | n/a | — | ✓ consistent with GOOG/META FY2/FY1 revenue growth (+26% / +20%) being platform-share-led |
| GS memory framing: memory P/E ~4x on ~80% GM implies ~50% earnings decline; GS prefers fabless (Buy NVDA/AVGO, Neutral MU) (GS strategy) | 09-24 reconciliation: "the memory debate is no longer about the numbers, it is the terminal multiple" | — | — | ✓ same conclusion from the strategy desk; screen-only, not a verdict (see the 09-25 correction memo on the BBG memory complex) |

---

## BBG leg — status
Terminal offline at 23:18 (blpapi connect to 127.0.0.1:8194 refused). All consensus figures above are from `_data/estimates.json` asof **2026-09-28** (same-day). Nothing is PENDING; a live re-pull would only refresh PX_LAST. Re-run `/wiki-consensus` when the Terminal is back if intraday moves matter for the MDB and META rows.

## Model bridges suggested
1. **META capex** — bridge house $301bn → Street $333-337bn CY26-27 (Muse compute per user × user ramp; GS's ~7GW YE26 / ~14GW YE27 pipeline).
2. **NVDA GW × $/GW** — restate the 2027 DC line as GW × revenue/GW with Rubin at $40bn/GW (GS) vs ~$25bn (house) and see which needs fewer CoWoS wafers.
3. **AVGO AI revenue** — house $132bn 2027 vs GS $125.5bn vs AVGO's 10GW × $20-30bn; decide whether the house is modelling share or GW.
