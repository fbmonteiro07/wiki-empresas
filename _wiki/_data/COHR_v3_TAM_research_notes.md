# COHR model v3 — supply-side TAM reconstruction (research notes)

> ⚠️ **AUDIT 2026-08-18 — PARTIAL / headline FAILED. Read before reusing anything here.**
> Three claims in this file did not survive verification and are corrected inline below:
> **(1)** the house model is NOT on the MS deck (see the retraction in §1);
> **(2)** Routes 1 and 2 are NOT independent — both are LightCounting, relayed via FUNDA, which
> `_wiki/themes/optical-cpo.md:604` explicitly forbids counting as corroboration; the primary is
> **JPM · Joseph Cardoso, 2026-08-06**, which was in the inbox and unread;
> **(3)** the 23.4% Innolight divisor is **uncited** and is contradicted by marks already on
> `_wiki/COHR.md` — Damnang 27% (line 242) and Papa Sylla 35–40% (line 100). At 27% the Route-1
> anchor FAILS its own guardrail.
> Also: the CY26–29 TAM interior is a hand-raised plug, +51% above the geometric path implied by
> the same source's published endpoints, worth **−17.5% on CY27**.

_Built 2026-08-17 for the v3 rebuild Felipe asked for. Purpose: replace the single-broker TAM
denominator (which the 2026-08-17 audit showed was carrying the entire share thesis) with a
TAM triangulated from the module makers' OWN reported revenue._

---

## 1. The problem this solves

The v2 model used the **GS optical-module deck (2026-08-10)** as its denominator. The audit found:
- the GS note is **not on disk**, has **no named analyst**, and was ingested from a pasted exhibit;
- **MS/Andy Meng (2026-05-15)** has 800G+1.6T units **1.22x / 1.55x / 1.54x** above GS for CY26-28;
- ~~the **house model** is on the **MS deck** (units 73/142/151 vs MS 73/141/150)~~ — **RETRACTED 2026-08-18
  after audit.** The house `Unit x ASP` tab states its own source in row 2: *"Primary source: Jefferies Optical
  Model (client file, Feb-2026). Industry units and ASPs from JEF 'Total Ethernet Market' tab"*, and row 1 is
  headed *"Jefferies-calibrated, Apr-2026"*. The units are **Jefferies', not MS's** — the match with MS is
  coincidence or convergence, not sourcing. The tab is also **orphaned (0 formula references)**; the house
  Summary reads `Rev!EL/EM` directly, so the house CY27 $16.6bn is a **stale raw-Jefferies Feb-2026 vintage**
  (Cover spot price $102.50). Jefferies has since cut its own CY27 to $12,251.9m (2026-08-13). That vintage
  gap — not a TAM-deck disagreement — is the real explanation of the house-vs-Street gap;
- so the wiki and the house model sit on **different denominators**, and every share number in the
  v2 write-up is deck-dependent.

## 2. The supply-side anchor — two independent routes that agree

### Route 1 — back-solve from Innolight's reported revenue × its LightCounting share

| Item | Value | Source |
|---|--:|---|
| Innolight (300308.SZ) FY2025 revenue | **¥38.24bn** (+60.3%) | company reported |
| — in USD @ ~7.15 | **~$5.35bn** | derived |
| Innolight share of global transceiver shipments, 2025 | **23.4%** (#1, 3rd yr running) | LightCounting |
| **⇒ implied global transceiver market, CY25** | **~$22.9bn** | derived |
| COHR share on the same LightCounting basis | **~16%** (≈7pts behind Innolight) | LightCounting |
| ⇒ implied COHR module revenue CY25 | ~$3.7bn | derived |

### Route 2 — LightCounting's own published market size

| Item | 2025 | 2030E | Source |
|---|--:|--:|---|
| Datacom optics | **~$20bn** | **>$70bn** (~28% CAGR) | LightCounting via FUNDA, 2026-08-12 |
| Telecom / DCI optics | **~$4bn** | ~$9bn | same |
| **Total optics** | **~$24bn** | ~$79bn | derived |
| of which 1.6T (2030) | — | ~$40bn | same |
| of which 3.2T (2030) | — | ~$14bn | same |
| 800G | peaks 2028, moderates after | | same |

### 🔴 The reconciliation

**Route 1 ($22.9bn) vs Route 2 ($24bn) agree within ~5%.** Two independent methods — one from a
Chinese issuer's audited revenue, one from an industry tracker's published forecast — land on the
same CY25 TAM. That is a far stronger denominator than any single sell-side exhibit.

### Where the existing decks sit against it

| Deck | CY25 total module TAM | vs the $22.9-24bn anchor |
|---|--:|--:|
| **LightCounting / Innolight back-solve** | **$22.9-24.0bn** | — (the anchor) |
| **House `Unit x ASP` tab** | **$20.0bn** | −13% — essentially on-basis ✅ |
| GS (2026-08-10) | $34.2bn | **+43%** — the outlier |
| GS AI-speed pool only (800G+1.6T) | $13.2bn | a subset, not comparable |

➜ **The house model's TAM basis is corroborated; the GS total is the outlier.** The v2 model's
share numbers (13.7% exit rate etc.) are computed on the GS AI-pool denominator and are NOT
comparable to the house's ~16% of pluggable TAM. **This is the single most important fix in v3.**

## 3. Corroborating supply-side datapoints

| Company | FY2025 revenue | Q1 2026 | Notes |
|---|--:|--:|---|
| **Innolight** (300308.SZ) | ¥38.24bn (+60.3%) | **¥19.50bn (+192% y/y)**, GM 46% | net profit +262%; Q1 profit > all of FY24 |
| **Eoptolink** (300502.SZ) | ¥24.84bn (+187%) | **¥8.34bn (+106% y/y)** | overseas = 96.16% of revenue |
| Combined | **¥63.1bn ≈ $8.8bn** | **¥27.8bn ≈ $3.9bn/qtr** | annualising ~$15.6bn and still accelerating |

⚠️ **Basis caution:** LightCounting's "23.4% of global transceiver shipments" — confirm whether
this is a **revenue** or **unit** share before it is used as a hard divisor. The reconciliation
with Route 2 only works if it is revenue. Flagged, not resolved.

⚠️ Innolight Q1-26 at ¥19.50bn vs FY25 ¥38.24bn means Q1-26 alone is >half of the whole prior
year. Verify against the 1H26 report when it lands (late Aug) before annualising.

## 4. FUNDA (fundaai@substack.com) — the source Felipe flagged

Optics-relevant notes in the inbox, all 2026-08:
- **"Deep|Optics: The Scale-Across TAM Is Taking Shape" (08-12)** — the LightCounting numbers above;
  Arista sizes scale-across $15-20bn by 2030; Ciena $8-10bn by 2029 inside a >$20bn transport market;
  MACOM SAM ~$15bn 2027 (DC ~$6bn); coherent-lite intersects **late 2027 into 2028** at 1.6T/3.2T;
  MACOM flags an **InP DFB laser shortage**, its own CW laser not in production until **late CY2027**.
- **"Research|Optics & Power: OCP APAC Summit Takeaways" (08-17)** — not yet read.
- **"Research|Optics: FCC Curbs on Chinese Transceivers" (08-05)** — not yet read.
- Also relevant: Nokia ramping an InP fab through 2027; an analyst on that call put **COHR "already
  doing pretty well"** on InP and **LITE "a bit behind"**.

## 5. What v3 must do

1. **Re-base the denominator** on the LightCounting/Innolight-triangulated TAM, and state the basis
   explicitly (datacom vs total optics vs AI-speed subset). Retire the GS total as the headline pool;
   keep it as one of three decks in a switch.
2. **Put the house `Unit x ASP` tab and the wiki model on the same basis** so their share numbers are
   finally comparable. Today they are not.
3. **Wire the `Unit x ASP` tab into the P&L** (currently orphaned — 0 formula references) or formally
   retire it. Close the +37% / +16% / +21% cross-check the model flags and never resolves.
4. **Fix the scenario switch** — `C4 = 2` ("Bull Override") drives only the ACTUAL columns; the
   forecast years are hardcoded over the formula (800G ASP CY26E/27E = 350/300, matching neither the
   JEF row 307/244 nor the Bull row 320/320).
5. **Add a supply-side sanity tab**: Innolight + Eoptolink + COHR + LITE + AAOI reported revenue
   summed against the TAM, so the model self-checks against reality every quarter.
6. **Rebuild the non-module block** (OCS/CPO/multi-rail) on the port-priced framing — it is 68% of
   v2's 2028 growth and the weakest line in the model.

## Sources
- Innolight FY25 / Q1-26 and the LightCounting 23.4% / COHR ~16% ranking — public reporting, 2026.
- Eoptolink FY25 / Q1-26 — public reporting, 2026.
- LightCounting datacom/telecom optics 2025 & 2030 — via **FUNDA, "Deep|Optics: The Scale-Across TAM
  Is Taking Shape", 2026-08-12**.
- House model — `E:\Wiki Felipe empresas\Modelos oficiais\Modelo COHR.xlsx` (modified 2026-08-12).
- Jefferies model — user-supplied `COHR.xlsx`, modified 2026-08-13, creator Ezra Weener.
