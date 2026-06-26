r"""
FEATURE 7 — Catalyst Gantt / forward timeline.

Reuses build_catalysts' bullet parser, but instead of an exact-date-only table
it RESOLVES the fuzzy time references that dominate real catalysts
("Q3", "2H26", "mid-July", "Q2 FY27", "CMD early 2027", "cal-27") into an
approximate window with a precision flag, then lays every upcoming catalyst on a
single horizontal time axis (today -> end of next year). Honesty-by-design:

    exact date  -> a point marker  (◆)
    quarter/half/year -> a BAR whose WIDTH = the date uncertainty

So a vague "FY27" reads as a wide bar and a hard "2026-08-26 print" reads as a
sharp point — the picture never overstates how precise a date is. Lanes = tickers
(sorted by next catalyst), colour = catalyst type, click the ticker to open its page.

    py "E:/Wiki Felipe empresas/_wiki/_tools/build_gantt.py"

Writes _dashboards/gantt.html. Read-only on company pages. Nothing is silently
dropped: catalysts beyond the horizon or with no resolvable date are listed in a
footnote so the axis can't masquerade as the full calendar.
"""
import sys, re, html, datetime as dt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _wlib import DASH, TODAY, company_pages, read, html_head
from build_catalysts import catalyst_bullets
sys.stdout.reconfigure(encoding="utf-8")

# Fiscal-year offset (FY label - calendar year). Only names whose FY is materially
# shifted; everyone else is FY≈CY (offset 0). NVDA FY ends ~late Jan, so FY27≈CY2026.
FY_OFFSET = {"NVDA": -1}

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
MONTH_RE = r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"

PREC_RANK = {"day": 0, "month": 1, "quarter": 2, "half": 3, "year": 4}


def _y4(y):
    y = int(y)
    return y if y >= 100 else 2000 + y


def _eom(year, month):
    """Last day of (year, month)."""
    if month == 12:
        return dt.date(year, 12, 31)
    return dt.date(year, month + 1, 1) - dt.timedelta(days=1)


def _q_window(q, year):
    sm = (q - 1) * 3 + 1
    return dt.date(year, sm, 1), _eom(year, sm + 2)


def _h_window(h, year):
    return (dt.date(year, 1, 1), dt.date(year, 6, 30)) if h == 1 else (dt.date(year, 7, 1), dt.date(year, 12, 31))


def candidates(clause, ticker):
    """Yield (start, end, precision) for every time reference found in `clause`."""
    out = []
    foff = FY_OFFSET.get(ticker, 0)

    # 1) ISO exact date
    for m in re.finditer(r"(20\d\d)-(\d\d)-(\d\d)", clause):
        try:
            d = dt.date(int(m[1]), int(m[2]), int(m[3]))
            out.append((d, d, "day"))
        except ValueError:
            pass

    # 2) Month name + day + year  ("Sep 2, 2026")
    for m in re.finditer(MONTH_RE + r"\.?\s+(\d{1,2}),?\s+(20\d\d)", clause, re.I):
        mo = MONTHS[m[1][:3].lower()]
        try:
            d = dt.date(int(m[3]), mo, int(m[2]))
            out.append((d, d, "day"))
        except ValueError:
            pass

    # 3) [mid/early/late] Month + year  ("mid-July 2026", "August 2026")
    for m in re.finditer(r"(?:(mid|early|late)[-\s])?" + MONTH_RE + r"\.?\s+(20\d\d)", clause, re.I):
        mo = MONTHS[m[2][:3].lower()]
        y = int(m[3])
        out.append((dt.date(y, mo, 1), _eom(y, mo), "month"))

    # 4) Fiscal quarter  ("Q2 FY27", "F3Q26", "Q3 FY 27")
    for m in re.finditer(r"\bF?Q([1-4])\s*FY\s?(\d{2,4})", clause, re.I):
        s, e = _q_window(int(m[1]), _y4(m[2]) + foff)
        out.append((s, e, "quarter"))
    for m in re.finditer(r"\bF([1-4])Q\s?(\d{2,4})", clause, re.I):
        s, e = _q_window(int(m[1]), _y4(m[2]) + foff)
        out.append((s, e, "quarter"))

    # 5) Calendar quarter  ("CQ2 2026", "Q2 2026", "3Q26", "Q3'26")
    for m in re.finditer(r"\bC?Q([1-4])\s*['\s]?\s*(20\d\d|\d{2})\b", clause):
        s, e = _q_window(int(m[1]), _y4(m[2]))
        out.append((s, e, "quarter"))
    for m in re.finditer(r"\b([1-4])Q\s*['\s]?\s*(20\d\d|\d{2})\b", clause):
        s, e = _q_window(int(m[1]), _y4(m[2]))
        out.append((s, e, "quarter"))

    # 6) Half  ("2H26", "1H FY27", "2H 2027")
    for m in re.finditer(r"\b([12])H\s*(?:FY)?\s?(20\d\d|\d{2})\b", clause):
        fy = "FY" in clause[max(0, m.start() - 1):m.end()].upper()
        s, e = _h_window(int(m[1]), _y4(m[2]) + (foff if fy else 0))
        out.append((s, e, "half"))

    # 7) Year  ("FY27", "CY2027", "cal-27", "calendar 2027")
    for m in re.finditer(r"\b(?:FY|CY|cal-?|calendar\s)(\d{2,4})\b", clause, re.I):
        fy = clause[m.start():m.start() + 2].upper() == "FY"
        y = _y4(m[1]) + (foff if fy else 0)
        out.append((dt.date(y, 1, 1), dt.date(y, 12, 31), "year"))

    return out


CATS = [
    ("regulatory", "#c0392b", ["export", "china", "tariff", "antitrust", "regulat", "ban ",
                                "license", "doj", "ftc", "negotiation", "permit", "sanction"]),
    ("event",      "#7c4dff", ["capital markets", "investor day", "analyst day", "cmd",
                                " ipo", "buyback", "dividend", "spin"]),
    ("print",      "#1c5fd6", ["print", "earnings", "results", " report", "quarter", "guide", "guidance"]),
    ("product",    "#1c7d3f", ["ramp", "launch", "tape-out", "tapeout", "production", "shipping",
                                "volume", "node", "yield", "qual", "design win", "deploy", "milestone"]),
]


def categorize(text):
    t = text.lower()
    for name, _, kws in CATS:
        if any(k in t for k in kws):
            return name
    return "other"


CAT_COLOR = {name: color for name, color, _ in CATS}
CAT_COLOR["other"] = "#8492ad"


def pick_window(text, ticker, horizon_end):
    """Best forward window for a bullet: earliest start within the visible horizon
    (ties broken toward the more precise reference). None if nothing resolvable."""
    clause = re.sub(r"\([^)]*\)", "", text)        # drop (source, date) citations
    cands = candidates(clause, ticker)
    if not cands:
        return None
    floor = TODAY - dt.timedelta(days=31)          # allow the just-passed month to show
    fwd = [c for c in cands if c[1] >= floor]
    if not fwd:
        return ("beyond_past", max(c[1] for c in cands))   # everything already resolved in the past
    if all(c[0] > horizon_end for c in fwd):
        return ("beyond_future", min(c[0] for c in fwd))
    fwd = [c for c in fwd if c[0] <= horizon_end]
    fwd.sort(key=lambda c: (c[0], PREC_RANK[c[2]]))
    return fwd[0]


def short(text, n=110):
    s = re.sub(r"\s+", " ", re.sub(r"[*`]", "", text)).strip()
    return s[:n] + ("…" if len(s) > n else "")


def main():
    t0 = TODAY.replace(day=1)
    t1 = dt.date(TODAY.year + 1, 12, 31)
    span = (t1 - t0).days

    def xpct(d):
        d = min(max(d, t0), t1)
        return round((d - t0).days / span * 100, 3)

    events, beyond, undated = [], [], []
    for tk, pf in company_pages():
        for wd, txt in catalyst_bullets(read(pf)):
            win = pick_window(txt, tk, t1)
            if win is None:
                continue
            if win[0] in ("beyond_future", "beyond_past"):
                if win[0] == "beyond_future":
                    beyond.append((tk, win[1], short(txt, 90)))
                continue
            s, e, prec = win
            events.append({"tk": tk, "start": s, "end": e, "prec": prec,
                           "cat": categorize(txt), "text": short(txt)})

    # lanes per ticker, sorted by earliest upcoming catalyst
    lanes = {}
    for ev in events:
        lanes.setdefault(ev["tk"], []).append(ev)
    order = sorted(lanes, key=lambda tk: min(e["start"] for e in lanes[tk]))

    # quarter gridlines across the horizon
    grid = []
    qy, qq = t0.year, (t0.month - 1) // 3 + 1
    while True:
        qs, _ = _q_window(qq, qy)
        if qs > t1:
            break
        grid.append((qs, f"Q{qq} '{str(qy)[2:]}"))
        qq += 1
        if qq > 4:
            qq, qy = 1, qy + 1

    ROWH = 30
    head, foot = html_head(
        "📌 Catalyst timeline (Gantt)",
        f"{TODAY.isoformat()} · {len(events)} catalysts across {len(order)} names · "
        f"horizon {t0.isoformat()} → {t1.isoformat()}")

    h = [head]
    h.append("<p class='byline'>Each bar's <b>width = date precision</b>: a point ◆ is an exact "
             "date, a wide bar is a quarter/half/year reference (honest about vagueness). Dates are "
             "heuristic — resolved from the words in each catalyst bullet; fiscal years approximated "
             "(NVDA FY=CY−1). Hover a bar for the full text; click a ticker to open its page.</p>")

    # legend + filter toggles
    h.append("<div class='legend'>")
    for name, color, _ in CATS + [("other", CAT_COLOR["other"], [])]:
        h.append(f"<button class='lg' data-cat='{name}' style='--c:{color}'>"
                 f"<span class='sw'></span>{name}</button>")
    h.append("</div>")

    # chart
    h.append("<div class='tl'>")
    # axis header
    h.append("<div class='row head'><div class='lab'></div><div class='axis'>")
    for qs, lbl in grid:
        h.append(f"<span class='qlbl' style='left:{xpct(qs)}%'>{lbl}</span>")
    h.append("</div></div>")
    # body with gridline overlay
    h.append("<div class='tlbody'>")
    h.append("<div class='grid'>")
    for qs, _ in grid:
        h.append(f"<i class='gl' style='left:{xpct(qs)}%'></i>")
    if t0 <= TODAY <= t1:
        h.append(f"<i class='today' style='left:{xpct(TODAY)}%'></i>"
                 f"<span class='todaylbl' style='left:{xpct(TODAY)}%'>today</span>")
    h.append("</div>")

    for tk in order:
        evs = sorted(lanes[tk], key=lambda e: e["start"])
        # greedy sub-row packing so overlapping catalysts in one name don't collide
        rows = []
        for ev in evs:
            placed = False
            for r in rows:
                if ev["start"] > r[-1]["end"]:
                    r.append(ev)
                    placed = True
                    break
            if not placed:
                rows.append([ev])
        lane_h = ROWH * len(rows)
        h.append(f"<div class='row' style='height:{lane_h}px'>")
        h.append(f"<div class='lab'><a href='../{tk}.html'>{tk}</a></div>")
        h.append("<div class='track'>")
        for ri, r in enumerate(rows):
            for ev in r:
                left = xpct(ev["start"])
                color = CAT_COLOR[ev["cat"]]
                tip = html.escape(f"{ev['tk']} · {ev['start'].isoformat()}"
                                  f"{'' if ev['prec']=='day' else '–'+ev['end'].isoformat()}"
                                  f" ({ev['prec']}) · {ev['text']}", quote=True)
                top = ri * ROWH + 6
                if ev["prec"] == "day":
                    h.append(f"<span class='pt' data-cat='{ev['cat']}' title=\"{tip}\" "
                             f"style='left:{left}%;top:{top}px;--c:{color}'>"
                             f"<i></i><b>{ev['tk']}</b> {html.escape(ev['text'][:42])}</span>")
                else:
                    w = max(xpct(ev["end"]) - left, 1.2)
                    h.append(f"<span class='bar' data-cat='{ev['cat']}' title=\"{tip}\" "
                             f"style='left:{left}%;width:{w}%;top:{top}px;--c:{color}'>"
                             f"<b>{ev['tk']}</b> {html.escape(ev['text'][:48])}</span>")
        h.append("</div></div>")
    h.append("</div></div>")  # tlbody, tl

    if beyond:
        h.append(f"<h2>Beyond the horizon — &gt;{t1.year} ({len(beyond)})</h2>")
        h.append("<ul class='far'>")
        for tk, d, txt in sorted(beyond, key=lambda x: x[1]):
            h.append(f"<li><a href='../{tk}.html'>{tk}</a> · <span class='mut'>{d.isoformat()}+</span> — {html.escape(txt)}</li>")
        h.append("</ul>")

    h.append("""<style>
.legend{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 14px}
.lg{display:inline-flex;align-items:center;gap:6px;border:1px solid #dde2ea;background:#fff;border-radius:14px;
    padding:3px 11px;font-size:12px;cursor:pointer;color:#33405c;text-transform:capitalize}
.lg .sw{width:11px;height:11px;border-radius:3px;background:var(--c)}
.lg.off{opacity:.32;text-decoration:line-through}
.tl{background:#fff;border:1px solid #e3e7ee;border-radius:10px;padding:8px 14px 14px;overflow:hidden}
.row{display:flex;align-items:stretch}
.row.head{height:24px;margin-bottom:2px}
.lab{flex:0 0 72px;font-size:11.5px;font-weight:700;display:flex;align-items:flex-start;padding-top:6px}
.lab a{color:#1c5fd6;text-decoration:none}.lab a:hover{text-decoration:underline}
.axis{position:relative;flex:1}
.qlbl{position:absolute;font-size:11px;color:#8492ad;transform:translateX(3px);white-space:nowrap}
.tlbody{position:relative}
.grid{position:absolute;left:72px;right:0;top:0;bottom:0;pointer-events:none}
.gl{position:absolute;top:0;bottom:0;width:1px;background:#eef1f6}
.today{position:absolute;top:0;bottom:0;width:2px;background:#f0a020;opacity:.7}
.todaylbl{position:absolute;top:-2px;font-size:10px;color:#b8801a;transform:translateX(-50%);font-weight:600}
.track{position:relative;flex:1}
.bar{position:absolute;height:18px;line-height:18px;border-radius:4px;background:var(--c);color:#fff;
     font-size:11px;padding:0 6px;white-space:nowrap;overflow:hidden;box-shadow:0 1px 2px #0f172926;cursor:default}
.bar b{font-weight:700}
.pt{position:absolute;height:18px;line-height:18px;font-size:11px;color:#33405c;white-space:nowrap;
    cursor:default;display:flex;align-items:center;gap:5px}
.pt i{flex:0 0 11px;width:11px;height:11px;background:var(--c);transform:rotate(45deg);border-radius:2px;
    box-shadow:0 1px 2px #0f172940}
.pt b{font-weight:700;color:var(--c)}
.bar.hide,.pt.hide{display:none}
.far{font-size:13px;columns:2;column-gap:30px}.far li{margin:2px 0;break-inside:avoid}
.far a{color:#1c5fd6;text-decoration:none;font-weight:700}
</style>""")

    h.append("""<script>
document.querySelectorAll('.lg').forEach(function(b){b.onclick=function(){
  var c=b.dataset.cat;b.classList.toggle('off');
  document.querySelectorAll('[data-cat=\"'+c+'\"]').forEach(function(el){el.classList.toggle('hide');});
};});
</script>""")
    h.append(foot)

    DASH.mkdir(parents=True, exist_ok=True)
    (DASH / "gantt.html").write_text("\n".join(h), encoding="utf-8")
    print(f"gantt: {len(events)} catalysts plotted across {len(order)} names; "
          f"{len(beyond)} beyond {t1.year}")
    print(f"  -> {DASH/'gantt.html'}")


if __name__ == "__main__":
    main()
