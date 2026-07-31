"""
Cross-company management-communication dashboard.

Reads the '## Management commentary — evolution' table off each covered page and
renders them side by side, on top of four hand-curated cross-company panels:

  1. The print cross-section  — capex message vs the tape, Jul 22-30 window
  2. Growth trajectories      — small multiples, each panel its own metric
  3. Investment posture       — FY26 guide evolution + FY27 stance
  4. Disclosure posture       — what each management will and will not quantify

Read-only on pages; writes only _wiki/_dashboards/mgmt-communication.html.

    py _wiki/_tools/build_mgmt_comms.py

Palette: the dataviz reference palette, validated with its own script —
series blue #2a78d6/#3987e5 and orange #eb6834/#d95926 pass every gate in both
modes (worst adjacent CVD dE 24.7 light / 26.8 dark). The reaction bars use the
DIVERGING pair blue<->red (#e34948/#e66767, CVD dE 21.6/19.2), deliberately NOT
green/red: green #006300 vs red #d03b3b measures CVD dE 4.6 protan, far below
the floor of 6, so a red-green reader cannot separate them. Every bar is also
signed, so colour never carries the sign alone.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "_wiki"
OUT = WIKI / "_dashboards" / "mgmt-communication.html"

TICKERS = ["MSFT", "AMZN", "GOOG", "META", "NVDA", "TSM", "ASML", "AVGO"]
NAMES = {
    "MSFT": "Microsoft", "AMZN": "Amazon", "GOOG": "Alphabet", "META": "Meta",
    "NVDA": "NVIDIA", "TSM": "TSMC", "ASML": "ASML", "AVGO": "Broadcom",
}
# who buys compute vs who sells it — drives the two-colour grouping
SIDE = {"MSFT": "demand", "AMZN": "demand", "GOOG": "demand", "META": "demand",
        "NVDA": "supply", "TSM": "supply", "ASML": "supply", "AVGO": "supply"}

ASOF = "2026-07-31"

# ── panel 2 — growth trajectories ────────────────────────────────────────────
# Each series is that company's own lead metric, taken from its evolution table.
# Different metrics and units, so these are SMALL MULTIPLES with a per-panel
# axis — never one shared scale.
SERIES = {
    "MSFT": dict(metric="Azure revenue growth", unit="% y/y (cc where reported)",
                 pts=[("Q2'25", 31), ("Q3'25", 35), ("Q4'25", 39), ("Q1'26", 39),
                      ("Q2'26", 38), ("Q3'26", 40), ("Q4'26", 42)],
                 note="Q4'26 reported +43%, ~42% cc. Basis is mixed across the row — "
                      "the first and last quarters are reported, the middle four cc."),
    "AMZN": dict(metric="AWS revenue growth", unit="% y/y",
                 pts=[("Q4'24", 19), ("Q1'25", 17), ("Q2'25", 17.5), ("Q3'25", 20.2),
                      ("Q4'25", 24), ("Q1'26", 28), ("Q2'26", 36.7)],
                 note="Q2'26 is the fastest in 18 quarters; fifth consecutive quarter "
                      "of acceleration."),
    "GOOG": dict(metric="Google Cloud revenue growth", unit="% y/y",
                 pts=[("Q2'25", 32), ("Q3'25", 34), ("Q4'25", 48), ("Q1'26", 63),
                      ("Q2'26", 82)],
                 note="Q1'26 onward includes TPU sales in backlog; management called "
                      "the Q2'26 acceleration “meaningful” ex-TPU."),
    "META": dict(metric="Ad revenue growth", unit="% y/y",
                 pts=[("Q1'25", 16), ("Q2'25", 22), ("Q3'25", 26), ("Q4'25", 24),
                      ("Q1'26", 33), ("Q2'26", 28)],
                 note="The only demand-side name whose lead metric DECELERATED this "
                      "print. Mix rotated from volume to price: impressions +19%→+14%, "
                      "price/ad held +12%, US&C pricing accelerated to +20%."),
    "NVDA": dict(metric="Data Center revenue growth", unit="% y/y",
                 pts=[("Q1FY26", 73), ("Q2FY26", 56), ("Q3FY26", 66), ("Q4FY26", 75),
                      ("Q1FY27", 92)],
                 note="Has NOT printed in this cycle — Q2 FY27 lands 2026-08-26. "
                      "Latest column is the May-2026 call."),
    "TSM": dict(metric="Gross margin", unit="%",
                pts=[("Q2'25", 58.6), ("Q3'25", 59.5), ("Q4'25", 62.3), ("Q1'26", 66.2),
                     ("Q2'26", 67.7)],
                note="Margin is TSMC's comparable quarterly series; its revenue row is "
                     "qualitative. Q3'26 guided to a 66% midpoint — N2 ramp is a "
                     "3-4pt H2 drag, overseas fabs 2-3pt widening to 3-4pt."),
    "ASML": dict(metric="FY26 revenue guide, midpoint", unit="€B",
                 pts=[("Q4'25", 36.5), ("Q1'26", 38.0), ("Q2'26", 44.0)],
                 note="Not a growth rate — the GUIDE LADDER. Raised twice in one year "
                      "(€34-39B → €36-40B → €43-45B), more than 10ppt on the top line, "
                      "with GM guided 54-56% from 51-53%."),
    "AVGO": dict(metric="AI semiconductor revenue growth", unit="% y/y",
                 pts=[("Q4'24", 150), ("Q1'25", 77), ("Q2'25", 46), ("Q3'25", None),
                      ("Q4'25", 74), ("Q1'26", 106), ("Q2'26", 143)],
                 note="Has NOT printed in this cycle — FQ3 FY26 lands ~Sept 2026. "
                      "Q3'25 is a genuine GAP in the source table, not a zero: the line "
                      "is broken there rather than interpolated."),
}

# ── panel 1 — the print cross-section ────────────────────────────────────────
CROSS = [
    dict(tk="GOOG", date="07-22", capex="RAISED FY26 to $195-205B",
         move=-3.5, move_label="−3 to −4%", verdict="bull won",
         why="Operating bar cleared on every line — Search +17%, YouTube +13%, "
              "Cloud +82% with $514B backlog. But capex doubled to $44.9B, FCF was "
              "−$5.9B, and no FY27 capex number was given. Capital intensity left "
              "unresolved."),
    dict(tk="MSFT", date="07-29", capex="HELD — CY26 ~$190B → ~$175B on a lease reclass",
         move=None, move_label="rallied", verdict="bull won",
         why="The modelled negative-FCF year did not arrive: Q4 OCF $55.4B, FCF "
              "+$19.6B against UBS −$21B and BofA's $32B trough, FY27 guided "
              "FCF-positive. Azure +43% beat the 39-40% cc guide. The capex step-down "
              "is a DEFINITION change (15→25-yr useful life), not a spending cut."),
    dict(tk="META", date="07-29", capex="NARROWED $130-145B, ceiling untouched, no FY27",
         move=-8.5, move_label="−8 to −9%", verdict="bear won",
         why="Numbers were fine — rev $60.8B +28% vs Street $60.2B, Q3 guide in line. "
              "What was missing did the damage: Meta Compute named but no scale, no "
              "pricing, no GW, no logo, no revenue; FY27 deferred to the planning "
              "cycle. 2027 EPS barely moved — a narrative event, not an estimate one."),
    dict(tk="AMZN", date="07-30", capex="RAISED FY26 ~$200B → ~$220B",
         move=9.0, move_label="+8 to +10% AH", verdict="bull won",
         why="Raised spend AND showed the return: AWS +36.7%, fastest in 18 quarters, "
              "with AWS margin EXPANDING to 39.4% while capex ripped. Backlog $364B "
              "→ $496B. Gave the season's only quantified payback framework. The "
              "increment was attributed to memory costs — ~$20B buying no extra compute."),
]
CROSS_FINDING = (
    "Same 48 hours, three different capex messages, three different tapes — and the "
    "spend level did not predict any of them. Microsoft held and rallied, Amazon "
    "<em>raised</em> and rallied hardest, Meta narrowed and fell 8-9%. The "
    "discriminator was <strong>visible accelerating cloud revenue alongside the "
    "spend</strong>, not how much was being spent."
)

# ── panel 3 — investment posture ─────────────────────────────────────────────
POSTURE = [
    dict(tk="MSFT", fy26="CY26 ~$190B → ~$175B", dir="basis",
         delta="Definition change, not a cut",
         detail="Finance-to-operating lease reclassification on a 15→25-yr useful-life "
                "extension. Management stated CY26 investment expectations are "
                "UNCHANGED. Every FY27 bogey struck on the old basis is now "
                "non-comparable.",
         fy27="FY27 “will grow y/y”; Q1 FY27 >$50B"),
    dict(tk="AMZN", fy26="FY26 ~$200B → ~$220B", dir="up", delta="+$20B",
         detail="Increment attributed EXPLICITLY to higher memory costs — roughly "
                "$20B of extra spend buying no incremental compute. Q2 P&E $54.2B. "
                "FCF −$9B vs consensus −$1B.",
         fy27="“Heavy capex over next few years”; demand > supply for 2026 and 2027"),
    dict(tk="GOOG", fy26="FY26 $180-190B → $195-205B", dir="up", delta="+$15B at the mid",
         detail="Second raise in two quarters. Q2 capex doubled y/y to $44.9B and FCF "
                "went to −$5.9B.",
         fy27="“Significant increase” — still no number, two quarters running"),
    dict(tk="META", fy26="FY26 $125-145B → $130-145B", dir="flat",
         delta="Low end raised, ceiling untouched",
         detail="The narrowest move of the four and the only one with no forward "
                "number at all. Plans “geared towards maximizing 2026 and 2027 "
                "capacity”; 2028 is land and power now, chip decisions deferred.",
         fy27="NO FY27 guide — “highly dynamic”; financing deferred to the planning cycle"),
    dict(tk="TSM", fy26="FY26 $52-56B → $60-64B", dir="up", delta="+$8B at the mid",
         detail="70-80% to advanced nodes, ~10% specialty, 10-20% packaging/test/mask. "
                "Plus a surprise additional $100B Arizona commitment ($265B total).",
         fy27="Next 3 years “even more significantly” higher"),
    dict(tk="ASML", fy26="Capacity, not capex", dir="up",
         delta="EUV cap ~85 ('27) → ~110 ('28)",
         detail="Low-NA EUV and ArFi capacity going up 30%/yr for 2027 and 2028; DUV "
                "immersion capacity ~220 by 2028. This is the supply ceiling every "
                "buyer above is spending into.",
         fy27="FY26 revenue guide raised twice: €34-39B → €36-40B → €43-45B"),
    dict(tk="NVDA", fy26="— recipient, not a spender", dir="na", delta="—",
         detail="Frames the demand side instead: $1T of Blackwell+Rubin visibility "
                "across cal-2025-27, customer capex above $1T in 2027.",
         fy27="Q2 FY27 prints 2026-08-26 — not yet in this cycle"),
    dict(tk="AVGO", fy26="— recipient, not a spender", dir="na", delta="—",
         detail="Sells into it: FY26 AI revenue $56B (+180%), 6 core custom-XPU "
                "customers on multi-generation LTAs.",
         fy27="FY27 AI revenue >$100B reiterated; FQ3 prints ~Sept 2026"),
]

# ── panel 4 — disclosure posture ─────────────────────────────────────────────
DISCLOSURE = [
    dict(tk="AMZN", rank="most forthcoming",
         quantified="AI business >$25B run-rate; chips >$25B separately, both "
                    "triple-digit % y/y; backlog $496B; AWS margin 39.4%",
         withheld="Nothing material on the AI P&L was dodged",
         standout="Gave the season's ONLY quantified payback framework — “a little "
                  "less than three years to break even” on servers/networking against "
                  "a ≥5-6 year useful life, off 30+ year shells worth “five to six "
                  "generations of server economics,” with the server half explicitly "
                  "demand-gated."),
    dict(tk="MSFT", rank="forthcoming, one asterisk",
         quantified="Azure +43%; RPO $678B +84%; +25% ex-OpenAI; bookings +18% "
                    "ex-OpenAI; >30M Copilot seats; ~90% of FY26 cloud revenue from "
                    "outside Frontier model companies",
         withheld="Never sizes the OpenAI drag, while sizing the Anthropic gain",
         standout="Changed the capex BASIS mid-stream. Also: the $4.74 EPS includes "
                  "$0.27 of discrete benefit (a $3.2B Anthropic mark-up), so clean EPS "
                  "is ~$4.47. The Azure-rationing evidence on the page was left "
                  "unmentioned and unrefuted."),
    dict(tk="TSM", rank="forthcoming",
         quantified="Capex $60-64B with the mix split; N2 at 3% of wafer revenue; GM "
                    "dilution quantified (N2 3-4pt H2, overseas 2-3pt widening to 3-4pt); "
                    "HPC 66% of revenue",
         withheld="No customer names; packaging capacity framed by customer growth "
                  "rather than absolute units",
         standout="Quantifies its own margin headwinds rather than leaving them to be "
                  "discovered — the opposite posture to Meta's."),
    dict(tk="ASML", rank="forthcoming",
         quantified="EUV capacity ~85 ('27) / ~110 ('28); DUV ~220 ('28); memory "
                    "revenue +75% y/y; FY26 guide raised twice",
         withheld="Stopped separately quantifying the China mix this call — it was "
                  "~20% for three straight quarters before that",
         standout="First time management named PRICING POWER as emerging "
                  "(value/overlay-based, not just throughput)."),
    dict(tk="NVDA", rank="forthcoming on the aggregate",
         quantified="$1T Blackwell+Rubin visibility cal-25-27; customer capex >$1T "
                    "in '27; networking $15B, nearly tripled y/y",
         withheld="China: H200 licensed, $0 revenue, and deliberately excluded from "
                  "the outlook entirely",
         standout="Quantifies a multi-year TAM rather than a quarter — the framing "
                  "everyone else's capex is then measured against."),
    dict(tk="AVGO", rank="forthcoming on backlog",
         quantified="FY26 AI $56B (+180%); FY27 >$100B; 6 core XPU customers; GM 77.1% "
                    "with Q3 ~74% on AI mix",
         withheld="Customer identities; the boundary between the 6 “core” customers "
                  "and prospects has moved repeatedly",
         standout="Only name here guiding a forward AI revenue number that far out and "
                  "reiterating it."),
    dict(tk="GOOG", rank="selective",
         quantified="FY26 capex $195-205B; Cloud +82% and backlog $514B with >50% "
                    "converting inside 24 months; ~22B tokens/min",
         withheld="FY27 capex number — “significant” for a second straight quarter; "
                  "TPU-vs-GCP revenue mix",
         standout="Flagged its own coming headwinds (Q3 comp-lapping, FX flip, "
                  "third-party capacity “bridge” with margin pressure accepted) — "
                  "candid on the near term, silent on the forward capex line."),
    dict(tk="META", rank="least forthcoming",
         quantified="Ad revenue $60.8B +28%; price +12% / impressions +14%; ads-AI "
                    "gains (+8.3% clicks, +15.7% conversions on FB); Advantage+ >$75B "
                    "run-rate; Meta AI daily interactors +60%",
         withheld="On Meta Compute: no scale, no pricing, no GW committed to third "
                  "parties, no enterprise logo, no dollar of revenue — and declined to "
                  "rank which monetisation leg scales first. No FY27 capex guide.",
         standout="JPM's desk titled it “META Q2 ‘Trust Me, Bro’.” Management IS on "
                  "the record demand-constrained (“nowhere near enough Compute for all "
                  "the demand”) and getting offers at “a significant premium over what "
                  "we paid” — but would not put a number on any of it."),
]

CAVEATS = [
    "Every cell in the per-company tables below is management's own commentary, "
    "paraphrased, sourced to the call date in its column header. The cross-company "
    "panels above are this desk's reading of those tables plus "
    "<code>_meta/outcomes.md</code>; they are interpretation, not company statements.",
    "<strong>NVDA and AVGO have not printed in this cycle.</strong> NVDA's Q2 FY27 "
    "lands 2026-08-26 and Broadcom's FQ3 FY26 around September, so their latest "
    "columns are May-2026 and June-2026. Do not read their position here as a "
    "response to the same tape as the other six.",
    "<strong>MSFT's Q4'26 column was added 2026-07-31</strong> from the 4QFY26 call. "
    "The underlying Bloomberg PDF is an <em>initial draft</em> transcript, not a final "
    "one — draft wording gets revised, so verify any MSFT quote against Microsoft's "
    "own IR transcript before citing it.",
    "<strong>AVGO's table skips Q3'25.</strong> That quarter was never added to the "
    "page, so its sparkline is broken at that point rather than interpolated across it.",
    "Basis traps carried from the pages, not resolved here: Microsoft's CY26 capex "
    "step-down is a lease reclassification and not comparable to FY27 bogeys struck on "
    "the old basis; Alphabet's Q1'26-onward Cloud backlog includes TPU sales; "
    "Microsoft's Azure row mixes reported and constant-currency growth.",
]


# ── read the per-company tables off the pages ────────────────────────────────
def read_evolution(tk):
    p = WIKI / f"{tk}.md"
    txt = p.read_text("utf-8", "replace")
    m = re.search(r"^## Management commentary[^\n]*$", txt, re.M)
    if not m:
        return None
    rest = txt[m.start():]
    nxt = re.search(r"\n## ", rest)
    sec = rest[:nxt.start()] if nxt else rest
    heading = sec.splitlines()[0].lstrip("# ").strip()
    rows = [l.strip() for l in sec.splitlines() if l.strip().startswith("|")]
    if len(rows) < 2:
        return None
    def cells(line):
        return [c.strip() for c in line.strip().strip("|").split("|")]
    header = cells(rows[0])
    body = [cells(r) for r in rows[2:] if not set(r.replace("|", "").strip()) <= {"-", " "}]
    src = ""
    ms = re.search(r"^_Source:(.+?)_$", sec, re.M | re.S)
    if ms:
        src = " ".join(ms.group(1).split())
    return dict(heading=heading, header=header, rows=body, source=src)


# ── tiny markdown → html for cell contents ──────────────────────────────────
def md_inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[\[([A-Z0-9_.-]+)\]\]", r"<span class='xref'>\1</span>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


def build():
    evo = {tk: read_evolution(tk) for tk in TICKERS}
    missing = [tk for tk, v in evo.items() if not v]
    if missing:
        print(f"  ! no evolution table found for: {', '.join(missing)}")

    payload = {
        "series": SERIES, "side": SIDE, "names": NAMES,
        "cross": CROSS, "asof": ASOF,
    }

    # per-company tables
    tabs, panes = [], []
    for tk in TICKERS:
        e = evo.get(tk)
        if not e:
            continue
        tabs.append(f'<button class="tab" data-tab="{tk}" type="button">'
                    f'<span class="dot {SIDE[tk]}"></span>{tk}</button>')
        nq = len(e["header"]) - 1
        thead = "".join(f"<th>{md_inline(h)}</th>" for h in e["header"])
        trows = []
        for r in e["rows"]:
            tds = "".join(
                (f'<th scope="row">{md_inline(c)}</th>' if i == 0
                 else f"<td>{md_inline(c)}</td>")
                for i, c in enumerate(r))
            trows.append(f"<tr>{tds}</tr>")
        panes.append(
            f'<section class="pane" id="pane-{tk}" hidden>'
            f'<h3>{NAMES[tk]} <span class="tk">{tk}</span> '
            f'<span class="muted">— {nq} quarters</span></h3>'
            f'<div class="scroll"><table class="evo"><thead><tr>{thead}</tr></thead>'
            f"<tbody>{''.join(trows)}</tbody></table></div>"
            + (f'<p class="src">{md_inline(e["source"])}</p>' if e["source"] else "")
            + "</section>")

    # cross-section cards
    cross_cards = []
    for c in CROSS:
        cls = "up" if (c["move"] or 0) > 0 else ("down" if c["move"] is not None else "flat")
        bar = ""
        if c["move"] is not None:
            # Diverging bar: zero is the track's midpoint, so ONE ARM is 50% of the
            # track. Scaling to 100% here let the arm overflow the card and bleed
            # into the neighbouring one. Full scale = +/-10%.
            w = min(abs(c["move"]) / 10 * 50, 50)
            side = "pos" if c["move"] > 0 else "neg"
            bar = (f'<div class="rbar"><div class="rtrack">'
                   f'<div class="rzero"></div>'
                   f'<div class="rfill {side}" style="width:{w:.1f}%"></div></div>'
                   f'<div class="rscale"><span>&minus;10%</span><span>0</span>'
                   f'<span>+10%</span></div></div>')
        cross_cards.append(
            f'<article class="xc {cls}">'
            f'<header><span class="tk">{c["tk"]}</span>'
            f'<span class="muted">{c["date"]}</span>'
            f'<span class="verdict {"v-bull" if "bull" in c["verdict"] else "v-bear"}">'
            f'{c["verdict"]}</span></header>'
            f'<p class="capex">{c["capex"]}</p>'
            f'<p class="react {cls}">{c["move_label"]}</p>{bar}'
            f'<p class="why">{c["why"]}</p></article>')

    # posture rows
    ARROW = {"up": "&#9650;", "flat": "&#9644;", "basis": "&#8644;", "na": "&mdash;"}
    posture_rows = []
    for p in POSTURE:
        posture_rows.append(
            f'<tr><th scope="row"><span class="dot {SIDE[p["tk"]]}"></span>'
            f'<span class="tk">{p["tk"]}</span></th>'
            f'<td class="nowrap">{p["fy26"]}</td>'
            f'<td class="dircell d-{p["dir"]}"><span class="arrow">{ARROW[p["dir"]]}</span>'
            f'{p["delta"]}</td>'
            f'<td>{p["detail"]}</td><td>{p["fy27"]}</td></tr>')

    # disclosure rows
    RANKCLS = {"most forthcoming": "r-best", "least forthcoming": "r-worst"}
    disc_rows = []
    for d in DISCLOSURE:
        disc_rows.append(
            f'<tr><th scope="row"><span class="dot {SIDE[d["tk"]]}"></span>'
            f'<span class="tk">{d["tk"]}</span>'
            f'<span class="rank {RANKCLS.get(d["rank"], "")}">{d["rank"]}</span></th>'
            f'<td>{d["quantified"]}</td><td>{d["withheld"]}</td>'
            f'<td>{d["standout"]}</td></tr>')

    caveats = "".join(f"<li>{c}</li>" for c in CAVEATS)

    doc = TEMPLATE.format(
        asof=ASOF,
        finding=CROSS_FINDING,
        cross_cards="".join(cross_cards),
        posture_rows="".join(posture_rows),
        disc_rows="".join(disc_rows),
        tabs="".join(tabs),
        panes="".join(panes),
        caveats=caveats,
        payload=json.dumps(payload, ensure_ascii=False),
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    print(f"mgmt-communication: {len(TICKERS)} names, "
          f"{sum(len(evo[t]['rows']) for t in TICKERS if evo.get(t))} theme rows")
    print(f"  -> {OUT}")


TEMPLATE = r"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Management communication — cross-company · Capstone wiki</title>
<style>
/* Dark is this page's committed look — it does NOT follow the OS setting, because
   the request was for a dark dashboard. A viewer who explicitly stamps
   data-theme="light" still gets a validated light set as an escape hatch.
   Series colours validated against THIS surface (#171b22), not the default:
   blue #3987e5 + orange #d95926 pass every gate; the reaction poles blue<->red
   #e66767 pass all-pairs. */
:root{{
  --page:#0d0f14; --surface:#171b22; --surface-2:#1c212a;
  --header:#0a0d14; --header-ink:#f3f5f9;
  --header-mut:#8b96ab; --header-link:#7fb0ff;
  --ink:#e8eaf0; --ink-2:#b9bfc9; --mut:#8b93a1;
  --rule:#262c36; --rule-2:#2f3743; --zebra:#1c212a; --chip:#232a37;
  --demand:#3987e5; --supply:#d95926;
  --pos:#3987e5; --neg:#e66767;
  --bull:#7fb0ff; --bear:#e66767;
  --shadow:0 1px 0 rgba(255,255,255,.03), 0 2px 12px rgba(0,0,0,.34);
  color-scheme:dark;
}}
:root[data-theme="light"]{{
  --page:#f5f6f8; --surface:#ffffff; --surface-2:#fafbfc;
  --header:#0f1729; --header-ink:#ffffff;
  --header-mut:#8492ad; --header-link:#7fb0ff;
  --ink:#1a1f29; --ink-2:#52585f; --mut:#6b7280;
  --rule:#e3e7ee; --rule-2:#dde2ea; --zebra:#fafbfc; --chip:#eef1f6;
  --demand:#2a78d6; --supply:#eb6834;
  --pos:#2a78d6; --neg:#e34948;
  --bull:#1c5cab; --bear:#b23434;
  --shadow:0 1px 3px rgba(15,23,41,.07);
  color-scheme:light;
}}
*{{box-sizing:border-box}}
body{{margin:0;font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,
  Helvetica,Arial,sans-serif;color:var(--ink);background:var(--page)}}
header.top{{background:var(--header);color:var(--header-ink);padding:18px 28px;
  border-bottom:1px solid var(--rule)}}
header.top h1{{margin:0;font-size:20px;letter-spacing:-.01em}}
header.top p{{margin:5px 0 0;color:var(--header-mut);font-size:13px;max-width:96ch}}
header.top nav{{margin-top:11px;display:flex;flex-wrap:wrap;gap:14px;font-size:12.5px}}
header.top nav a{{color:var(--header-link);text-decoration:none}}
header.top nav a:hover,header.top nav a:focus-visible{{text-decoration:underline}}
main{{max-width:1240px;margin:0 auto;padding:22px 28px 90px}}
h2{{font-size:13px;text-transform:uppercase;letter-spacing:.07em;color:var(--mut);
  margin:34px 0 4px;font-weight:700}}
h2:first-of-type{{margin-top:8px}}
.lede{{margin:0 0 14px;font-size:15px;color:var(--ink-2);max-width:88ch}}
.finding{{background:var(--surface);border:1px solid var(--rule);border-left:3px solid
  var(--demand);border-radius:3px;padding:13px 16px;margin:0 0 18px;font-size:15.5px;
  line-height:1.6;max-width:100ch}}
.tk{{font-weight:700;font-variant-numeric:tabular-nums;letter-spacing:.01em}}
.muted,.mut{{color:var(--mut)}}
.dot{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;
  vertical-align:1px}}
.dot.demand{{background:var(--demand)}} .dot.supply{{background:var(--supply)}}
.key{{display:flex;gap:18px;flex-wrap:wrap;font-size:12.5px;color:var(--mut);
  margin:0 0 12px}}

/* cross-section */
.xgrid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(268px,1fr))}}
.xc{{background:var(--surface);border:1px solid var(--rule);border-radius:3px;
  padding:13px 15px;display:flex;flex-direction:column;gap:7px}}
.xc header{{display:flex;align-items:baseline;gap:9px;font-size:13px}}
.xc header .tk{{font-size:15px}}
.verdict{{margin-left:auto;font-size:11px;font-weight:700;text-transform:uppercase;
  letter-spacing:.05em}}
.v-bull{{color:var(--bull)}} .v-bear{{color:var(--bear)}}
.xc .capex{{margin:0;font-size:13.5px;font-weight:600;line-height:1.4}}
.xc .react{{margin:0;font-size:22px;font-weight:700;font-variant-numeric:tabular-nums;
  letter-spacing:-.02em}}
.xc .react.up{{color:var(--pos)}} .xc .react.down{{color:var(--neg)}}
.xc .react.flat{{color:var(--ink-2);font-size:18px}}
.rbar{{margin:-2px 0 2px}}
.rtrack{{position:relative;height:6px;background:var(--chip);border-radius:3px;
  overflow:hidden}}
.rzero{{position:absolute;left:50%;top:0;width:1px;height:6px;background:var(--mut);
  opacity:.55}}
.rfill{{position:absolute;top:0;height:6px}}
.rfill.pos{{left:50%;background:var(--pos);border-radius:0 3px 3px 0}}
.rfill.neg{{right:50%;background:var(--neg);border-radius:3px 0 0 3px}}
.rscale{{display:flex;justify-content:space-between;font-size:10px;color:var(--mut);
  font-variant-numeric:tabular-nums;margin-top:2px}}
.xc .why{{margin:0;font-size:12.5px;color:var(--ink-2);line-height:1.5}}

/* small multiples */
.sgrid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(272px,1fr))}}
.sc{{background:var(--surface);border:1px solid var(--rule);border-radius:3px;
  padding:12px 14px 10px}}
.sc h3{{margin:0;font-size:14px;display:flex;align-items:baseline;gap:7px}}
.sc .metric{{margin:2px 0 0;font-size:12px;color:var(--mut)}}
.sc .figs{{display:flex;align-items:flex-end;gap:8px;margin:7px 0 2px}}
.sc .last{{font-size:26px;font-weight:700;letter-spacing:-.025em;line-height:1;
  font-variant-numeric:tabular-nums}}
.sc .unit{{font-size:12px;color:var(--mut);padding-bottom:2px}}
.sc.demand .last{{color:var(--demand)}} .sc.supply .last{{color:var(--supply)}}
.spark{{width:100%;height:62px;display:block;overflow:visible}}
.sc .qs{{display:flex;justify-content:space-between;font-size:10.5px;color:var(--mut);
  font-variant-numeric:tabular-nums;margin-top:1px}}
.sc .note{{margin:7px 0 0;font-size:11.5px;color:var(--ink-2);line-height:1.45;
  border-top:1px solid var(--rule);padding-top:7px}}
.stale{{display:inline-block;font-size:10px;font-weight:700;text-transform:uppercase;
  letter-spacing:.05em;color:var(--mut);border:1px solid var(--rule-2);
  border-radius:2px;padding:1px 5px}}

/* tables */
.scroll{{overflow-x:auto;-webkit-overflow-scrolling:touch}}
table{{border-collapse:collapse;width:100%;font-size:13px;background:var(--surface)}}
th,td{{border:1px solid var(--rule-2);padding:7px 9px;text-align:left;
  vertical-align:top}}
thead th{{background:var(--chip);font-weight:700;white-space:nowrap;font-size:12.5px}}
tbody tr:nth-child(even) td{{background:var(--zebra)}}
tbody th[scope=row]{{background:var(--zebra);font-weight:600;white-space:nowrap}}
td.nowrap{{white-space:nowrap;font-weight:600}}
.dircell{{white-space:nowrap;font-weight:600}}
.dircell .arrow{{margin-right:5px}}
.d-up .arrow{{color:var(--pos)}} .d-flat .arrow{{color:var(--mut)}}
.d-basis .arrow{{color:var(--supply)}} .d-na .arrow{{color:var(--mut)}}
.rank{{display:block;font-size:10.5px;font-weight:600;text-transform:uppercase;
  letter-spacing:.04em;color:var(--mut);margin-top:3px}}
.rank.r-best{{color:var(--pos)}} .rank.r-worst{{color:var(--neg)}}
/* 7-quarter tables scroll sideways, so the theme label stays pinned */
table.evo th[scope=row]{{position:sticky;left:0;z-index:2;min-width:148px;
  max-width:180px;white-space:normal;background:var(--chip);
  box-shadow:1px 0 0 var(--rule-2)}}
table.evo td{{min-width:190px;max-width:290px}}
table.evo thead th:first-child{{position:sticky;left:0;z-index:3;background:var(--chip);
  box-shadow:1px 0 0 var(--rule-2)}}
.scroll.pinned{{max-height:none}}
.xref{{font-weight:600;color:var(--ink-2)}}
code{{background:var(--chip);padding:1px 5px;border-radius:3px;font-size:85%;
  font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}

/* tabs */
.tabs{{display:flex;flex-wrap:wrap;gap:5px;margin:0 0 12px}}
.tab{{font:inherit;font-size:13px;font-weight:600;color:var(--ink-2);
  background:var(--surface);border:1px solid var(--rule-2);border-radius:3px;
  padding:5px 11px;cursor:pointer}}
.tab:hover{{border-color:var(--mut)}}
.tab[aria-selected=true]{{background:var(--header);color:#fff;border-color:var(--header)}}
.tab[aria-selected=true] .dot{{outline:1px solid rgba(255,255,255,.5)}}
.pane h3{{margin:0 0 9px;font-size:15px}}
.pane .src{{margin:8px 0 0;font-size:11.5px;color:var(--mut);line-height:1.5;
  max-width:120ch}}
:focus-visible{{outline:2px solid var(--demand);outline-offset:2px}}

/* tooltip */
#tip{{position:fixed;z-index:20;pointer-events:none;opacity:0;transition:opacity .08s;
  background:var(--header);color:#fff;font-size:12px;padding:5px 9px;border-radius:3px;
  white-space:nowrap;font-variant-numeric:tabular-nums;
  box-shadow:0 2px 10px rgba(0,0,0,.28)}}
ul.caveats{{margin:6px 0 0;padding-left:20px;font-size:13px;color:var(--ink-2);
  line-height:1.6;max-width:104ch}}
ul.caveats li{{margin-bottom:7px}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
@media (max-width:640px){{
  main{{padding:18px 15px 70px}} header.top{{padding:15px 16px}}
  .sc .last{{font-size:22px}} .xc .react{{font-size:19px}}
}}
</style></head>
<body>
<header class="top">
  <h1>Management communication — cross-company</h1>
  <p>How eight managements have changed what they say, quarter by quarter, and what
  the market did with it. Built from each page's own commentary-evolution table
  plus the outcomes ledger · as of {asof}</p>
  <nav>
    <a href="index.html">&larr; dashboard hub</a>
    <a href="#detail">Per-company detail</a>
    <a href="#cross">The print cross-section</a>
    <a href="#growth">Growth trajectories</a>
    <a href="#posture">Investment posture</a>
    <a href="#disclosure">Disclosure posture</a>
    <a href="#caveats">Sourcing &amp; caveats</a>
  </nav>
</header>
<main>

<h2 id="detail">Per-company detail — the source tables</h2>
<p class="lede">Read straight off each wiki page's <em>Management commentary —
evolution</em> section at build time, so this never drifts from the page. The theme
column stays pinned while the quarters scroll sideways.</p>
<div class="tabs" role="tablist">{tabs}</div>
{panes}

<h2 id="cross">The print cross-section — 22 to 30 July 2026</h2>
<div class="finding">{finding}</div>
<div class="xgrid">{cross_cards}</div>

<h2 id="growth">Growth trajectories</h2>
<p class="lede">Each panel is that company's own lead metric on its own scale — these
are small multiples, not one chart. Hover any point for the quarter and value.</p>
<div class="key">
  <span><span class="dot demand"></span>Buys compute — sells AI services</span>
  <span><span class="dot supply"></span>Sells compute — tools, silicon, capacity</span>
</div>
<div class="sgrid" id="sgrid"></div>

<h2 id="posture">Investment posture — what moved and how it was framed</h2>
<p class="lede">The FY26 guide as it stands after this print, against what it was, plus
the forward stance. Direction markers carry a word as well as a colour.</p>
<div class="scroll"><table>
<thead><tr><th>Name</th><th>FY26 capex / capacity</th><th>Move</th>
<th>What the move actually was</th><th>Forward stance</th></tr></thead>
<tbody>{posture_rows}</tbody></table></div>

<h2 id="disclosure">Disclosure posture — what they will and will not put a number on</h2>
<p class="lede">The sharpest lens on this cycle: the four demand-side names spent
comparable money and were treated very differently, and the gap tracks how much they
were willing to quantify.</p>
<div class="scroll"><table>
<thead><tr><th>Name</th><th>Quantified this print</th><th>Withheld</th>
<th>What stands out</th></tr></thead>
<tbody>{disc_rows}</tbody></table></div>

<h2 id="caveats">Sourcing &amp; caveats</h2>
<ul class="caveats">{caveats}</ul>
</main>
<div id="tip" role="status" aria-live="polite"></div>
<script>
const D = {payload};

/* ── small multiples ─────────────────────────────────────────────────────── */
const grid = document.getElementById('sgrid');
const tip = document.getElementById('tip');
const order = ['MSFT','AMZN','GOOG','META','NVDA','TSM','ASML','AVGO'];
const STALE = {{NVDA:1, AVGO:1}};

function fmt(v){{
  if (v === null) return '—';
  return (Math.round(v * 10) / 10).toLocaleString('en-US',
    {{minimumFractionDigits: Number.isInteger(v) ? 0 : 1}});
}}

for (const tk of order){{
  const s = D.series[tk], side = D.side[tk];
  const vals = s.pts.map(p => p[1]);
  const known = vals.filter(v => v !== null);
  const last = known[known.length - 1];
  const card = document.createElement('article');
  card.className = 'sc ' + side;
  card.innerHTML =
    '<h3><span class="tk">' + tk + '</span>'
    + '<span class="muted">' + D.names[tk] + '</span>'
    + (STALE[tk] ? '<span class="stale" title="Has not reported in this cycle">'
        + 'pre-cycle</span>' : '')
    + '</h3>'
    + '<p class="metric">' + s.metric + '</p>'
    + '<div class="figs"><span class="last">' + fmt(last) + '</span>'
      + '<span class="unit">' + s.unit + '</span></div>';
  const svg = spark(s, side, tk);
  card.appendChild(svg);
  const qs = document.createElement('div');
  qs.className = 'qs';
  qs.innerHTML = '<span>' + s.pts[0][0] + '</span><span>'
    + s.pts[s.pts.length - 1][0] + '</span>';
  card.appendChild(qs);
  if (s.note){{
    const n = document.createElement('p');
    n.className = 'note'; n.textContent = s.note;
    card.appendChild(n);
  }}
  grid.appendChild(card);
}}

function spark(s, side, tk){{
  const NS = 'http://www.w3.org/2000/svg';
  const W = 260, H = 62, PAD = 7;
  const vals = s.pts.map(p => p[1]).filter(v => v !== null);
  let lo = Math.min(...vals), hi = Math.max(...vals);
  if (hi === lo){{ hi += 1; lo -= 1; }}
  const span = hi - lo, n = s.pts.length;
  const x = i => PAD + (W - 2 * PAD) * (n === 1 ? 0.5 : i / (n - 1));
  const y = v => H - PAD - (H - 2 * PAD) * ((v - lo) / span);
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('class', 'spark');
  svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
  svg.setAttribute('preserveAspectRatio', 'none');
  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-label', s.metric + ' by quarter, ' + s.pts
    .filter(p => p[1] !== null).map(p => p[0] + ' ' + fmt(p[1])).join(', '));
  const colour = side === 'demand' ? 'var(--demand)' : 'var(--supply)';

  /* baseline */
  const base = document.createElementNS(NS, 'line');
  base.setAttribute('x1', PAD); base.setAttribute('x2', W - PAD);
  base.setAttribute('y1', H - PAD + 0.5); base.setAttribute('y2', H - PAD + 0.5);
  base.setAttribute('stroke', 'var(--rule)'); base.setAttribute('stroke-width', '1');
  svg.appendChild(base);

  /* split into runs so a null BREAKS the line instead of interpolating it */
  const runs = []; let run = [];
  s.pts.forEach((p, i) => {{
    if (p[1] === null){{ if (run.length) runs.push(run); run = []; }}
    else run.push([i, p[1]]);
  }});
  if (run.length) runs.push(run);

  for (const r of runs){{
    if (r.length > 1){{
      const area = document.createElementNS(NS, 'path');
      area.setAttribute('d',
        'M' + x(r[0][0]) + ',' + (H - PAD) + ' '
        + r.map(([i, v]) => 'L' + x(i) + ',' + y(v)).join(' ')
        + ' L' + x(r[r.length - 1][0]) + ',' + (H - PAD) + ' Z');
      area.setAttribute('fill', colour); area.setAttribute('opacity', '.10');
      svg.appendChild(area);
      const line = document.createElementNS(NS, 'path');
      line.setAttribute('d', 'M' + r.map(([i, v]) => x(i) + ',' + y(v)).join(' L'));
      line.setAttribute('fill', 'none'); line.setAttribute('stroke', colour);
      line.setAttribute('stroke-width', '2');
      line.setAttribute('stroke-linejoin', 'round');
      line.setAttribute('stroke-linecap', 'round');
      svg.appendChild(line);
    }}
  }}

  /* markers — endpoint emphasised, 2px surface ring so it reads over the line */
  s.pts.forEach((p, i) => {{
    if (p[1] === null) return;
    const isLast = i === s.pts.length - 1
      || s.pts.slice(i + 1).every(q => q[1] === null);
    const c = document.createElementNS(NS, 'circle');
    c.setAttribute('cx', x(i)); c.setAttribute('cy', y(p[1]));
    c.setAttribute('r', isLast ? 4.5 : 2.6);
    c.setAttribute('fill', colour);
    c.setAttribute('stroke', 'var(--surface)');
    c.setAttribute('stroke-width', isLast ? 2 : 1.5);
    svg.appendChild(c);
    /* hit target larger than the mark */
    const hit = document.createElementNS(NS, 'circle');
    hit.setAttribute('cx', x(i)); hit.setAttribute('cy', y(p[1]));
    hit.setAttribute('r', 12); hit.setAttribute('fill', 'transparent');
    hit.style.cursor = 'crosshair';
    const label = tk + ' · ' + p[0] + ' · ' + fmt(p[1]) + ' ' + s.unit;
    hit.addEventListener('pointerenter', e => show(e, label));
    hit.addEventListener('pointermove', e => show(e, label));
    hit.addEventListener('pointerleave', hide);
    svg.appendChild(hit);
  }});
  return svg;
}}

function show(e, text){{
  tip.textContent = text;
  tip.style.opacity = '1';
  const r = tip.getBoundingClientRect();
  let left = e.clientX + 12, top = e.clientY - r.height - 10;
  if (left + r.width > innerWidth - 8) left = e.clientX - r.width - 12;
  if (top < 8) top = e.clientY + 14;
  tip.style.left = left + 'px'; tip.style.top = top + 'px';
}}
function hide(){{ tip.style.opacity = '0'; }}

/* ── tabs ────────────────────────────────────────────────────────────────── */
const tabs = [...document.querySelectorAll('.tab')];
const panes = [...document.querySelectorAll('.pane')];
function select(tk){{
  tabs.forEach(t => t.setAttribute('aria-selected', String(t.dataset.tab === tk)));
  panes.forEach(p => {{ p.hidden = p.id !== 'pane-' + tk; }});
  /* a pane inherits the previous one's sideways scroll otherwise, so the theme
     column opens off-screen */
  const pane = document.getElementById('pane-' + tk);
  const sc = pane && pane.querySelector('.scroll');
  if (sc) sc.scrollLeft = 0;
}}
tabs.forEach(t => t.addEventListener('click', () => select(t.dataset.tab)));
tabs.forEach((t, i) => t.addEventListener('keydown', e => {{
  const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
  if (!d) return;
  e.preventDefault();
  const nxt = tabs[(i + d + tabs.length) % tabs.length];
  nxt.focus(); select(nxt.dataset.tab);
}}));
if (tabs.length) select(tabs[0].dataset.tab);
</script>
</body></html>
"""

if __name__ == "__main__":
    build()
