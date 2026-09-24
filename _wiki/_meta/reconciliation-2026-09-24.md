# Reconciliation — run-inbox 2026-09-24

_32 sources (two nights of missed drops + 6 recovered off P:). Every NEW quantitative datapoint below is reconciled against (1) what the wiki already carried, (2) the house models, and (3) BBG consensus. **BBG leg: the Terminal is DOWN (port 8194 closed) all morning, so the consensus column is the on-disk `_data/estimates.json` snapshot, asof 2026-09-23** — one day old, not PENDING. Where a fiscal-vs-calendar mapping could not be verified against the snapshot's own `2FY`/`3FY` labels, it is flagged instead of asserted._

---

## 🔴 THE HEADLINE — three names, one pattern: the Street is above consensus on the NUMBERS and at-or-below it on the PRICE

This did not come from any single note. It only appears when the batch is reconciled against the snapshot together:

| Name | New house estimate vs BBG consensus | That house's PT vs BBG consensus PT | What it means |
|---|--:|--:|---|
| **MU** (UBS Arcuri, 09-23) | FY27E EPS **$184.19 vs $154.58 = +19.2%**; FY28E **$274.97 vs $178.11 = +54.4%** | **$1,625 vs $1,578.59 = +2.9%** | UBS is half again above the Street on FY28 earnings and prices the stock in line with it |
| **SKHYNIX** (UBS Gaudois, 09-22) | 2027E EPS **W610,284 vs W466,029 = +31.0%** | **W3,000,000 vs W3,314,921 = −9.5%** | Above the Street on earnings, **below it on price** |
| **CRWV** (UBS initiation, 09-22) | FY28E revenue **$45,575mn vs $42,700mn = +6.7%** (UBS's own text says "~6% above street") | **$120 vs $142.05 = −15.5%** | Same sign flip |

➤ **The mechanism is explicit in the UBS Micron note and it is the single most useful thing in this batch: the valuation bridge moved from `15x C2029E EPS ~$124-125` (06-25) → `11x on ~$165` → `8x on ~$219`, with the price target unchanged at $1,625 the whole way.** Three successive EPS raises have been fully absorbed by multiple compression. BofA is doing the same thing from the other side — it prints consensus FY27E EPS at "$150-200, up over 100% YoY" on "**~7x forward PE vs historically sustained ~10x**" and leaves its PO at $1,550 (−1.8% vs consensus PT).
➤ **So the memory debate is no longer about the numbers.** Four houses now agree the earnings are coming; they disagree with their own price targets about what those earnings are worth. The falsifiable question for the house model is not "are estimates too low" — it is **"does the terminal multiple hold at 7-8x."** ⚠️ Note the SKH PT ladder (GS W3.5m > Mirae W3.1m > UBS W3.0m > JPM W2.75m) straddles a consensus PT of **W3,314,921**, so only GS is above the Street on price.

---

## DIVERGES — where a new source contradicts what the wiki, the house or consensus holds

**1. HBM TAM — the ledger's canonical was 2.8x too low, on the same house's own name.** `_meta/assumptions.md` carried *"HBM TAM $35B 2025 → $100B 2028 (~40% CAGR) | Micron/JPM | 2026-05-28"*. JPM's 2026-09-22 model prints HBM industry revenue at **US$160.1bn (2027E) and US$282.2bn (2028E)**. BofA's $168bn **CY30** frame now sits *below* JPM's **CY28**, so the two are no longer "different horizons, both valid" — they conflict on level. **Ledger re-based this run**; the scope note now tells readers to cite the dated row, never the retired $100bn framing.

**2. CoWoS 2027 — a convergence the wiki logged on 09-17 has re-split.** UBS puts industry CoWoS at **270kwpm end-'27** against JPM's 260k. Worse for anyone reusing it: **no revised per-vendor split was published**, so the 180 TSMC / 60 ASE / 20 Amkor decomposition is stale against the new total and must not be netted into it.

**3. CXMT — the two China channels now say opposite things in the same month.** UBS's APAC tour reports **large preliminary orders for CXMT G4 (1z nm) but NOT YET for G5 (1a nm)**. This wiki's own 2026-09-20 ingest carried the line that **CXMT's G5 hit mass production two years early**. Both are dated, both are sourced, and they cannot both describe the same quarter. Unresolved and flagged on `themes/semicap-wfe`. Separately, Bernstein's initiation has CXMT **surpassing Micron on wafer capacity in 2028** (530k wpm 4Q28, "nearly 20% globally").

**4. Hybrid bonding in memory — three sources in 24 hours, pointing two ways.** Redburn (09-23): HBM4E is the insertion point, HVM 2027. UBS/ASMPT (09-22): TCB extended **potentially to HBM5**, volume adoption pushed out, *"in-line with comments from both Samsung and SK Hynix"*. DAMNANG (09-23): **Samsung has already delivered hybrid-bonded HBM4/HBM4E samples; SK hynix has not**. (2) and (3) disagree on whether Samsung is the hybrid-bonding champion or the TCB extender. Both can be literally true. ➤ **The test has been narrowed to a customer QUALIFICATION of a hybrid-bonded HBM4E part — not a sample, not an evaluation.**

**5. COHR's PhotonLink TAM — a machine summary against three earnings calls.** The page carries *">$15bn by 2030"* from the Q3 call, the FQ4 call and a Jefferies relay. A **Bloomberg automated summary** of the 09-21 conference presentation prints *"+$30bn by 2030 on top of the existing $60bn portfolio"*. Logged as **open drift, not a supersession** — a generated summary does not overwrite a call. ➤ Pull the PhotonLink deck from Coherent IR; it settles the basis, the "$15,000 per system or per 100 terabit I/O chip" unit, and whether the two hyperscaler LTAs are additional to the NVIDIA agreement.

**6. Morgan Stanley's four-note cyber package disagrees with itself.** The CRWD note says cyber spend moves to 2.5% of enterprise AI budgets *"from the ~1% it is today"*; the PANW and sector notes use **~1.5%**. 1.5%→2.5% is a 1.67x step; 1%→2.5% is 2.5x. This is the **third** documented internal inconsistency in one package (the others: CRWD bull PT printed $309 in the body and $308.00 on the risk-reward page; PANW bear $250 vs $253.00). The theme keeps 1.5% and **deliberately does not write it to `_meta/assumptions.md` while the package is inconsistent.**

**7. Meta compute resale — the wiki's framing that "no house has put Meta Compute revenue in a number" is now false.** Wells Fargo's model carries **0.25 GW average 2027E and 1.00 GW 2028E of resold capacity at $20bn/GW ⇒ $5bn (2027E) and $20bn (2028E) of revenue**, 1.78% / 5.38% of owned capacity. The `What the NeoCloud is worth` signal was re-scored ⚠ nuances → CONVERGED 09-17 → **SPLIT AGAIN 09-24**.

**8. DRAM 3Q26 pricing — the canonical is now the floor, not the central case.** Four of five new marks print at or above the top of TrendForce's +15-20%: BofA/Simon Woo **+20-30% q/q**, UBS **+~26% incl. LTAs**, UBS on SK hynix **+23.1%**, FundaAI **20-30% executed**; only Mirae's **+15.8%** is inside. The likeliest source of the spread is LTA treatment — UBS is the only house that states its figure is LTA-inclusive.

**9. NBIS–Meta contract value.** UBS prints **"$12+bn / 5 yrs"**; the wiki carries a **$20bn+ TCV** from Barclays. Same deal, ~1.7x apart. Both retained, unreconciled.

**10. CoreWeave contracted power.** UBS says "~6 GW" at end-2Q26; CoreWeave's own disclosure is ~3.7 GW (quarter-end) / ~4.2 GW (08-11). No bridge given — most likely a gross-facility vs IT-load basis gap, which is exactly the trap UBS itself documents three pages earlier.

---

## CONFIRMS — where the new sources corroborate what was already held

- **Micron HBM4 at ~$30/GB (UBS, 09-23) independently re-corroborates Redburn's $30-32/GB 2027 mark (06-23)** on a stack basis, three months later. The 3:1 → ~4:1 HBM/DRAM trade ratio also survives this batch intact.
- **The Morgan Stanley cyber primaries confirm the 09-19 relay with zero corrections.** Every relayed figure was re-checked against the PDFs: all confirmed, none corrected. Two provenance statements retired (both pages said "the PDF is NOT on disk" — it is now).
- **The `~$40M/MW` CoreWeave term flag is closed.** The 09-21 management mark was logged with the caveat that the term was not stated; UBS states it — **3-6 month contracts at up to $40m/MW = $40bn/GW ANNUALISED**, "3-4x the monetization per MW of the installed base".
- **IREN's own book dates the neocloud price move on one operator, one counterparty, three vintages:** Microsoft Nov-2025 at ~$10m/MW/yr → 5-yr today at ~$17m (+70%) → 3-yr at $20-25m (+100%), all inside 9-12 months. This corroborates the duration-priced tier ladder rather than any single $/GW number.
- **The de-spec did not destroy HBM bits, it moved them forward:** JPM's 3-year accumulated HBM bit demand is **unchanged at 163bn Gb** while 2026/27 rose and 2028 fell 7%.
- **AVGO PT $470 is a confirmation, not an action** — it appears only in UBS corporate-access boilerplate dated "as of 8.24.26".

---

## ⚠️ BASIS FLAGS — do not read these as divergences

- **META EPS vs BBG.** KeyBanc's 2027E EPS of **$35.09** is **−7.9% vs the snapshot's $38.11**, yet KeyBanc's own text claims **~+4% vs Street** on Visible Alpha. That is a GAAP-vs-adjusted / consensus-source difference, not a call. Basis-match before quoting either.
- **LITE.** Citi's 2027E EPS $23.03 is a fiscal-year figure (its own printed consensus comparator is $21.39); the snapshot's CY27 EPS is $28.11. Different periods — not comparable, and not a divergence.
- **CSCO.** Barclays' FY28 EPS of $5.58 is numerically identical to the snapshot's `2FY` EPS of $5.58; the period alignment could not be verified from the snapshot labels, so no gap is asserted.
- **The five GW bases are now six.** GS's Carbonomics GW are **installed GENERATION capacity** (67 GW global BTM by 2030), which carries a 9-47% overbuild margin over the IT load it serves; its "DC capacity" figure (217 GW global / 108 GW US by 2030) is a further distinct quantity. Neither is facility GW, IT-load GW, the 800V subset or XPU-deployment GW. Logged in the ledger this run.
- **Every GW in the Wells Fargo workbooks is derived, not disclosed** — backed out of a headline contract value at the broker's own $/GW revenue assumption, and WFS uses **$20bn/GW for the OpenAI-AWS GPU contract and $6bn/GW for the Trainium contract in the same file** (3.3x apart).
- **$/GB vs $/Gb, now an observed published error:** BofA printed TrendForce's HBM price as *"over $3.80/GB"*; it only reconciles per **Gb** ($3.80/Gb × 8 = $30.4/GB). Added to the ledger's scope note.
- **JPM's OAI/Anthropic ARR pairing** ("$40bn / $100bn" vs "$25bn / $14bn in Feb-26") appears **inverted** against every other mark on this wiki. Not adopted; flagged for checking.

---

## Source-integrity items from this run

- **One source was ~90% fabricated.** `2026_09_22_advantest_susq_22_set_26.txt` arrived with 2,058 lines of which only the **first 180** are the Advantest call; the rest is a machine-invented "Q3 2023" earnings script with one sentence repeated **1,754 times**. The tail was removed before the HTML render so it could never enter the corpus or search index; the delivered bytes are preserved at `_inbox\_done\2026_09_22_advantest_susq_22_set_26.RAW-with-hallucinated-tail.txt`. **No figure below line 181 was filed anywhere.**
- **A slug collision was silently overwriting source renders.** Every Outlook printout drops under the same filename and overwrote the previous render; nine pages pointed at whatever landed last. Repaired for today's article, the 09-18 Morgan Stanley printout was restored at the base slug, and `ingest_inbox.py` now disambiguates by content hash.
- **Two duplicate sources** were detected and cited once each: the UBS Micron preview (`ued51886` = the P: copy) and the Morgan Stanley CrowdStrike PDF.

---

## Open items carried forward

1. **Qualify, don't sample:** watch for a customer qualification of a hybrid-bonded HBM4E part (settles item 4).
2. **MU prints F4Q26 ~2026-09-30** — the bogey table on MU.md now carries guide vs UBS vs BofA vs Street side by side; the four things to listen for are on the page.
3. **CXMT G4-vs-G5** (item 3) needs a third channel.
4. **Meta–Oracle $20bn** sits in a published Wells Fargo model labelled "(Not Confirmed)" by Wells Fargo itself, unannounced by either party — recorded in `themes/ai-compute-deals.md` as a broker assumption, not a deal.
5. **Anthropic–Lambda $35bn** is now twice-reported and still unconfirmed by Lambda.
6. **BBG refresh owed** — the 12:03 `daily-wiki-consensus` run needs the Terminal up; this reconciliation used the 09-23 snapshot.
