# Reconciliation — /run-inbox 2026-11-10

_This report checks each new quantitative datapoint from tonight's sources against three baselines: (1) prior wiki marks; (2) Capstone house models; (3) BBG consensus._

- **BBG is OFFLINE** (`127.0.0.1:8194` refused, ~23:27). The on-disk snapshot `estimates.json` is dated **2026-11-10**, so it is used as the consensus baseline (no web substitute). ⚠️ It was very likely taken BEFORE CoreWeave's 11-10 after-market print, so the CRWV column is **pre-print consensus**; re-pull with `/wiki-consensus` once the Terminal is back to see the post-print revisions.
- **Sources with numbers:** CoreWeave Q3 2026 earnings call (fast-follow transcript) + Q3 2026 outlook presentation (both 2026-11-10). Podcasts with host-recalled numbers: The Circuit (Bajarin/Goldberg, pub 2026-11-09), Semi Doped (Sekar/Lyons, pub 2026-11-09).
- **No new numbers:** Alex Karp on The Builders (taped 2026-08-06; no figures); AEI "No Gas, No Chips" (2026-11-04; industry shares and prices only, no covered-company estimate — logged on themes/china-export).
- **House models:** CRWV (Template DCF CRWV.xlsx, 2026-10-14) — the only one that applies tonight.

## DIVERGES (the alpha)

| Name | New datapoint (source) | vs prior wiki | vs house | vs BBG (snapshot 11-10, pre-print) | Read |
|---|---|---|---|---|---|
| CRWV | **2027 capex "in line with 2026"** if building only against committed backlog (call, 11-10) — i.e. ~$37-39bn | UBS CY27E capex $46.97bn; Barclays $47.2bn (10-15/10-23) | house CY27E **$50.9bn** | cons 2FY capex **$47.9bn** | Management's committed-backlog case sits ~20% below consensus and ~25% below the house. It is conditional (success-based capex), but it is the single biggest swing in the funding math. Bridge the house model: either 2027 power adds are lower than the house's 1.9→3.2 GW, or capex/GW falls. |
| CRWV | **<$5bn of incremental parent-level capital through 2027**; ~$9bn prepayments/deposits in the next 3 months; next DDTL at **7-7.5%**, >90% loan-to-capex (call) | House NTM map (10-23): **~$19bn residual** to fund over 3Q26-2Q27 before ATM/insurer loans; 10-26 UBS-call source guessed DDTL ~10-10.5% | house map did not include the ~$9bn prepayments or an IG DDTL at >90% LTC | n/a | The company's sources-and-uses is far less punitive than the house map. Not reconciled tonight (no 2027 sources-and-uses table on the call) — flagged for the model owner. Execution still pending: the IG DDTL has not launched. |
| CRWV | FY26 **adj. operating income guide $1.275-1.375bn** (mid $1.325bn), from $0.96-1.15bn (deck + call) | Q2 guide $0.96-1.15bn (08-11); Jefferies CY26 EBIT $1,056m | house AOI CY26E **$1.03bn** | cons 1FY EBIT **$1,055m** | Midpoint ~26% above consensus and ~29% above the house. Implied 4Q adj. OI ~$0.75-0.85bn vs cons 4Q EBIT **$663m** (DERIVED; BBG EBIT basis may differ from adjusted OI). Expect upward revisions. |
| CRWV | Q3 actuals: revenue **$3.7bn**, adj. OI **$379m** (10%), adj. EBITDA $2.3bn, interest **$846m** (call) | Visible Alpha 3Q $3.5bn / $243m; Barclays 3Q rev $3,581m; guide $3.45-3.60bn / $200-260m / interest $860-940m | n/a (annual model) | pre-print cons on page $3.5bn | Beat on revenue (~+5%) and a large beat on adj. OI (+56% vs VA). Interest below the guide. |
| CRWV | Exit-2026 ARR **$20-21bn** (from $18.5-19.5bn) | Q2 guide (08-11) | house CY27 revenue $26.7bn | cons 2FY revenue **$26.9bn** | Exit ARR of $20.5bn ×(growth through 2027) makes the $26.9bn consensus look undemanding, and the 2027/28 roll-off book adds ~$4bn / ~$10bn of annualised revenue at current prices with no capex (company figures). Upside risk to 2FY revenue. |

## CONFIRMS (no action)

| Name | New datapoint (source) | vs prior wiki | vs house | vs BBG (snapshot 11-10, pre-print) | Read |
|---|---|---|---|---|---|
| CRWV | FY26 revenue guide **$13.0-13.3bn** (mid $13.15bn), from $12.4-13.2bn | Q2 guide; Jefferies CY26 $12,990m; UBS $13,050m | house CY26E **$12.8bn** | cons 1FY **$12,861m** | Midpoint +2.2% vs cons, +2.7% vs house: a raise, but small. Implied 4Q revenue ~$4.6-4.9bn vs cons 4Q **$4,702m** — in line. |
| CRWV | FY26 capex **$37-39bn** (low end raised from $35bn) | Q2 guide $35-39bn; Barclays $37.99bn | house **$37.0bn** | cons 1FY **$35.6bn** | House is at the low end; consensus will move up ~$2-3bn. |
| CRWV | Adj. net income positive in 1H28 and FY28 (call) | UBS CY28E EPS $0.74; MS $2.37 | house CY28E EPS **$0.54** | cons 3FY EPS **$1.10** | All three baselines already positive in 2028. |
| CRWV | EBITDA less interest to "more than double" in 2027 (call) | — | house 2027 adj. EBITDA $16.55bn vs interest ~$5.4bn (model) | cons 2FY EBITDA $16.7bn vs 1FY $7.5bn | Consistent with both baselines on the EBITDA leg; interest is the swing. |
| CRWV | Pricing: new 4-5yr contracts **$20-25m/MW**, short-term >$40m/MW per year (call) | UBS 09-22: short-dated "up to $40m per MW"; blended installed base ~$11bn/GW | house revenue per GW **$12.0bn** (2027) | n/a | Different quantities: the house figure is the blended installed base. New-contract pricing ~2x the house blend supports the model's rising revenue/GW path. Do not net. |
| AMD | "Could conceivably do **$100bn** next year in revenue" (host on The Circuit, pub 11-09; [transcribed "$und00 billion"]) | — | n/a | cons 2FY revenue **$95.4bn** (CY2027 quarterly sum $96.9bn, the figure cited on AMD.md) | Host extrapolation ~5% above consensus. Podcast, not a forecast. |
| INTC | Fab 28 cost ~$300m this quarter and ~$300m next (Semi Doped hosts, recalling the call) | INTC.md: ~$300m Q4 revenue, "similar" 1Q27 (Q3 call 10-29) | n/a | — | Confirms the two marks; the hosts' "700 or 800 would not surprise" is opinion, matching the 10-Q's refusal to bound it. |
| ANTHROPIC | Growth "150% → 40%" sequential; Q3 compute "$10bn, $5.5bn contracted" (Goldberg on The Circuit, hedged) | S-1/A: revenue $4,731m / $11,555m / $16,956m (q/q +144% → +47%); Q3 compute **$9.9bn, $5.0bn under short-term commitments** | n/a (private) | n/a (private) | Growth ✅. The compute split is 🔭 vs the filing; the page logs the filing's figures, not the host's. |
| NET | Q3 paying-customer adds "158,000" (Goldberg; [transcribed "158,000 000"]) | Q2 call: ">80,000" adds | n/a | — | UNCONFIRMED until the Q3 print is on disk; logged as host's figure only. |
