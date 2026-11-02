r"""
Build a self-contained navigable HTML on top of the per-company wiki
(E:\Wiki Felipe\_wiki\*.md). Output: E:\Wiki Felipe\_wiki\index.html — one file,
opens offline by double-click, no server. Left sidebar grouped by theme (parsed
from 00_INDEX.md) + live full-text search; main pane renders each page.

Markdown is converted in-Python (no external lib — machine is behind a TLS proxy).
Handles the constructs the wiki uses: headings, bold/italic, inline code, links,
nested '- ' lists, pipe tables, blockquotes, hr, paragraphs.

    py E:/.claude/scripts/build_wiki_html.py
"""
from pathlib import Path
import datetime
import html
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
WIKI = Path("E:/Wiki Felipe empresas/_wiki")


# ---------- minimal markdown -> html ----------
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
               lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def md_to_html(md):
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)   # drop HTML comments (e.g. template placeholders)
    lines = md.split("\n")
    out, i, n = [], 0, len(lines)
    while i < n:
        ln = lines[i]
        st = ln.strip()
        # blank
        if not st:
            i += 1
            continue
        # raw inline SVG passthrough (supply-chain infographics) — emit verbatim, don't escape
        if st.startswith("<svg"):
            buf = []
            while i < n:
                buf.append(lines[i])
                if "</svg>" in lines[i]:
                    i += 1
                    break
                i += 1
            out.append("\n".join(buf))
            continue
        # table: current line starts with | and next line is a |---| separator
        if st.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            header = [c.strip() for c in st.strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ["<table><thead><tr>"] + [f"<th>{inline(h)}</th>" for h in header] + ["</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue
        # heading
        m = re.match(r"^(#{1,6})\s+(.*)$", st)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue
        # hr
        if re.match(r"^-{3,}$", st):
            out.append("<hr>")
            i += 1
            continue
        # blockquote (possibly multi-line)
        if st.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(inline(lines[i].strip().lstrip(">").strip()))
                i += 1
            out.append("<blockquote>" + "<br>".join(buf) + "</blockquote>")
            continue
        # list (supports one level of nesting via indentation)
        if re.match(r"^\s*[-*]\s+", ln):
            out.append("<ul>")
            stack = 1
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                indent = len(lines[i]) - len(lines[i].lstrip())
                mm = re.match(r"^\s*[-*]\s+(.*)$", lines[i])
                if indent >= 2 and stack == 1:
                    out.append("<ul>")
                    stack = 2
                elif indent < 2 and stack == 2:
                    out.append("</ul>")
                    stack = 1
                out.append(f"<li>{inline(mm.group(1))}</li>")
                i += 1
            if stack == 2:
                out.append("</ul>")
            out.append("</ul>")
            continue
        # italic-only whole line (header byline _..._)
        if st.startswith("_") and st.endswith("_") and len(st) > 2:
            out.append(f"<p class='byline'>{inline(st[1:-1])}</p>")
            i += 1
            continue
        # paragraph: gather consecutive plain lines
        buf = [st]
        i += 1
        while i < n and lines[i].strip() and not re.match(r"^\s*([-*]\s+|#{1,6}\s+|\||>|_.*_$|-{3,}$)", lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>" + inline(" ".join(buf)) + "</p>")
    return "\n".join(out)


# ---------- parse 00_INDEX.md for theme grouping + one-liners ----------
def parse_index():
    idx = (WIKI / "00_INDEX.md").read_text(encoding="utf-8")
    groups, cur = [], None
    for ln in idx.split("\n"):
        h = re.match(r"^##\s+(.*)$", ln)
        if h:
            cur = {"theme": h.group(1).strip(), "items": []}
            groups.append(cur)
            continue
        row = re.match(r"^\|\s*([A-Z]{1,10})\s*\|\s*\[[^\]]+\]\(([^)]+)\)\s*\|\s*(.*?)\s*\|$", ln)
        if row and cur is not None:
            cur["items"].append({"ticker": row.group(1), "thesis": row.group(3)})
    return [g for g in groups if g["items"]]


def load_estimates():
    p = WIKI / "_data" / "estimates.json"
    if p.is_file():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def render_financials(t, est):
    """HTML block of BBG consensus + street-high estimates for ticker t (or '' if none)."""
    c = (est.get("companies") or {}).get(t)
    if not c or "error" in c or not c.get("periods"):
        return ""
    ccy = c.get("ccy", "USD")
    big = ccy in ("JPY", "TWD", "KRW")
    div, unit = (1e6, "tn") if big else (1e3, "bn")
    cur = {"USD": "$", "EUR": "€", "JPY": "¥", "TWD": "NT$", "GBP": "£"}.get(ccy, ccy + " ")
    mny = lambda v: "—" if v is None else f"{cur}{v/div:,.1f}{unit}"
    eps = lambda v: "—" if v is None else f"{cur}{v:,.2f}"
    pct = lambda v: "—" if v is None else f"{v:,.1f}%"
    P = c["periods"]
    cols = []
    for key in ("1FQ", "2FQ", "CY2026", "CY2027"):
        p = P.get(key) or {}
        lbl = p.get("label", key)
        if key.startswith("CY") and p.get("n_actual") is not None:
            lbl += f'<br><span class="hi">{p["n_actual"]}/4 act</span>'
        cols.append((lbl, p))
    METRICS = [("Revenue", "rev", mny, True), ("Gross margin", "gm", pct, False),
               ("Op. income (EBIT)", "ebit", mny, True), ("EBITDA", "ebitda", mny, True),
               ("Net income", "ni", mny, False), ("EPS", "eps", eps, True), ("Capex", "capex", mny, True)]
    rows = []
    for name, k, fmt, hi in METRICS:
        cells = [f"<td>{name}</td>"]
        for lbl, p in cols:
            mv = p.get(k)
            cell = fmt(mv)
            hv = p.get(k + "_hi") if hi else None
            if hv is not None and mv is not None:
                cell += f'<br><span class="hi">hi {fmt(hv)}</span>'
            cells.append(f"<td>{cell}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    head = "<tr><th>Metric</th>" + "".join(f"<th>{lbl}</th>" for lbl, _ in cols) + "</tr>"
    a = c.get("actual") or {}
    act = ""
    if a.get("ocf") is not None or a.get("capex") is not None:
        act = (f'<p class="byline">Last reported FY (actual): OCF {mny(a.get("ocf"))} · '
               f'Capex {mny(a.get("capex"))} · FCF {mny(a.get("fcf"))}.</p>')
    # valuation multiples — fwd P/E from px+EPS (always); EV multiples when mktcap/EV present
    px = c.get("px"); ev = c.get("ev")
    cy26 = P.get("CY2026") or {}; cy27 = P.get("CY2027") or {}

    def mult(num, den):
        if not num or den is None or den <= 0:
            return "—"
        r = num / den
        return f"{r:,.1f}x" if r < 100 else "n/m"

    vbits = []
    if px:
        vbits.append(f"Fwd P/E: CY26 <b>{mult(px, cy26.get('eps'))}</b> · CY27 <b>{mult(px, cy27.get('eps'))}</b>")
    if ev:
        vbits.append(f"EV/EBITDA CY26 <b>{mult(ev, cy26.get('ebitda'))}</b> · EV/Sales CY26 <b>{mult(ev, cy26.get('rev'))}</b>")
    pxs = (f"{cur}{px:,.2f}" if px and px < 1000 else f"{cur}{px:,.0f}") if px else "—"
    val = (f'<p class="byline">Valuation (last px {pxs}): {" · ".join(vbits)}.'
           + ("" if ev else " <span class=\"hi\">EV multiples pending BBG.</span>") + "</p>") if vbits else ""
    note = (f'<p class="byline">BBG consensus, as of {est.get("asof","")} · figures in {cur}{unit} '
            f'(EPS in {cur}, margin %). <span class="hi">Green = street-high</span> (capex high = max spend). '
            f'CY = calendar-year (BBG actuals for reported quarters + consensus for the rest; fiscal quarters '
            f'snapped to nearest calendar quarter).</p>')
    # consensus estimate-revision momentum (EPS / Revenue, 1M/3M/6M)
    rv = c.get("revisions") or {}
    rev_html = ""
    if rv:
        def _w(d):
            return d if isinstance(d, dict) and "err" not in d else {}
        def revcell(v):
            if v is None:
                return "<td>—</td>"
            col = "#4ade80" if v > 0 else ("#f87171" if v < 0 else "#9aa0ad")
            return f'<td><span style="color:{col}">{v:+.1f}%</span></td>'
        specs = [("EPS · FY1", _w(rv.get("eps", {}).get("fy1"))),
                 ("EPS · FY2", _w(rv.get("eps", {}).get("fy2"))),
                 ("Revenue · FY1", _w(rv.get("rev", {}).get("fy1"))),
                 ("Revenue · FY2", _w(rv.get("rev", {}).get("fy2")))]
        rr = ["<tr><td>" + nm + "</td>" + revcell(d.get("1m")) + revcell(d.get("3m")) + revcell(d.get("6m")) + "</tr>"
              for nm, d in specs]
        rev_html = ('<p class="byline" style="margin-top:10px">Consensus estimate revisions '
                    '(FY1 = current fiscal year, FY2 = next; % change in the mean estimate; '
                    '<span style="color:#4ade80">green up</span> / <span style="color:#f87171">red down</span>):</p>'
                    '<table class="fin"><thead><tr><th>Revision</th><th>1M</th><th>3M</th><th>6M</th></tr></thead><tbody>'
                    + "".join(rr) + "</tbody></table>")
    return ('<h2>Consensus estimates (BBG)</h2>' + note +
            '<table class="fin"><thead>' + head + '</thead><tbody>' + "".join(rows) + '</tbody></table>'
            + val + rev_html + act)


ROOT = WIKI.parent
INTRA_RE = re.compile(r"intra-quarter|in the inbox", re.I)
TRANS_RE = re.compile(r"management commentary", re.I)


def _transcript_list(tk):
    d = ROOT / tk / "transcripts"
    if not d.is_dir():
        return ""
    files = []
    for f in d.glob("*.md"):
        m = re.search(r"(20\d\d-\d\d-\d\d)", f.name)
        files.append((m.group(1) if m else "", f))
    if not files:
        return ""
    rows = []
    for date, f in sorted(files, reverse=True):
        label = re.sub(r"_20\d\d-\d\d-\d\d.*$", "", f.name).replace("_", " ")
        rows.append('<tr><td>%s</td><td>%s</td><td><a href="../%s/transcripts/%s">open ↗</a></td></tr>'
                    % (date, html.escape(label), tk, f.name))
    return ("<h3>Source calls</h3><table><thead><tr><th>Date</th><th>Call</th><th></th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table>")


def _briefings_drawer(tk):
    bf = ROOT / "_briefings" / "by-ticker" / (tk + ".md")
    if not bf.is_file():
        return ""
    return ("<details><summary>Raw email / FinTwit feed (briefings roll-up)</summary>"
            + md_to_html(bf.read_text(encoding="utf-8", errors="replace")) + "</details>")


# ---------- TSM-only interactive N3 supply/demand widget (rendered into a dedicated tab) ----------
N3_RE = re.compile(r"N3 .*supply/demand|N3 bottoms-up", re.I)
N3_WIDGET = r"""<style>
#p-TSM .n3toggle{display:inline-flex;gap:2px;border:1px solid var(--border);border-radius:8px;overflow:hidden;margin:6px 0 12px}
#p-TSM .n3btn{background:transparent;border:0;color:var(--ink-soft);padding:6px 15px;font-size:12.5px;font-weight:600;cursor:pointer;font-family:var(--bfont)}
#p-TSM .n3btn.on{background:var(--accent);color:#fff}
#p-TSM .n3legend{display:flex;flex-wrap:wrap;gap:6px 16px;margin:10px 0 2px;font-size:12px;color:var(--ink-soft)}
#p-TSM .n3legend span{display:inline-flex;align-items:center;gap:6px}
#p-TSM .n3legend i{width:11px;height:11px;border-radius:3px;display:inline-block}
#p-TSM #n3chart svg{width:100%;height:auto}
</style>
<h2>N3 demand — interactive</h2>
<div class="n3toggle">
  <button class="n3btn on" data-m="client">By client</button>
  <button class="n3btn" data-m="demand">By demand type</button>
</div>
<div id="n3chart"></div>
<div class="n3legend" id="n3legend"></div>
<p class="byline">Stacked columns = N3 wafer demand (kwpm) by quarter; dashed red line = TSMC's N3 capacity; % above each column = implied utilisation. Toggle splits demand by end customer or by Cloud-AI-vs-consumer. Client-view series are summed from the per-product rows (may differ ±1-2 kwpm from the published subtotals due to rounding). (UBS / Sunny Lin, Randy Abrams, 2026-06-28)</p>
<script>
(function(){
  if(!document.getElementById('n3chart'))return;
  var Q=['Q1 26','Q2 26','Q3 26','Q4 26','Q1 27','Q2 27','Q3 27','Q4 27'];
  var CAP=[120,130,150,170,175,180,185,190];
  var UTIL=[107,107,110,106,101,106,104,102];
  var COLORS=['#74a8ff','#4ade80','#fbbf24','#a78bfa','#f472b6','#fb923c','#34d399','#60a5fa','#c084fc','#94a3b8'];
  var VIEWS={
    client:{order:['NVIDIA','Broadcom','Alchip·AWS Trn3','Marvell·AWS Trn2.5','AMD','Apple','Qualcomm','MediaTek','Intel','Other'],
      data:{'NVIDIA':[0,5,20,37,45,56,61,63],'Broadcom':[6,11,18,28,25,30,37,39],'Alchip·AWS Trn3':[0,4,11,22,20,17,10,2],'Marvell·AWS Trn2.5':[0,0,0,2,0,0,0,0],'AMD':[2,2,1,1,1,1,0,0],'Apple':[69,67,60,38,34,29,25,26],'Qualcomm':[17,13,9,3,5,5,4,3],'MediaTek':[5,4,4,5,9,12,11,8],'Intel':[19,19,11,4,8,8,8,5],'Other':[12,14,30,39,30,33,38,48]}},
    demand:{order:['Cloud AI','Consumer & other'],
      data:{'Cloud AI':[9,26,61,114,117,138,140,139],'Consumer & other':[120,113,104,65,60,53,53,55]}}
  };
  var W=760,H=380,ml=40,mr=14,mt=18,mb=44,pw=W-ml-mr,ph=H-mt-mb,ymax=220;
  function y(v){return mt+ph*(1-v/ymax);}
  function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;');}
  function draw(mode){
    var V=VIEWS[mode],n=Q.length,step=pw/n,bw=step*0.62,i,k;
    var s='<svg viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg">';
    for(var g=0;g<=ymax;g+=50){var gy=y(g);s+='<line x1="'+ml+'" y1="'+gy+'" x2="'+(W-mr)+'" y2="'+gy+'" stroke="var(--border)" stroke-width="1"/><text x="'+(ml-6)+'" y="'+(gy+3)+'" font-size="10" text-anchor="end" fill="var(--ink-soft)">'+g+'</text>';}
    for(i=0;i<n;i++){
      var cx=ml+step*i+step/2,x0=cx-bw/2,acc=0;
      for(k=0;k<V.order.length;k++){var key=V.order[k],val=V.data[key][i];if(!val)continue;var yt=y(acc+val),yb=y(acc);s+='<rect x="'+x0.toFixed(1)+'" y="'+yt.toFixed(1)+'" width="'+bw.toFixed(1)+'" height="'+(yb-yt).toFixed(1)+'" fill="'+COLORS[k%COLORS.length]+'"><title>'+esc(key)+': '+val+' kwpm</title></rect>';acc+=val;}
      s+='<text x="'+cx.toFixed(1)+'" y="'+(y(acc)-5).toFixed(1)+'" font-size="10" font-weight="700" text-anchor="middle" fill="var(--ink)">'+UTIL[i]+'%</text>';
      s+='<text x="'+cx.toFixed(1)+'" y="'+(mt+ph+16)+'" font-size="10.5" text-anchor="middle" fill="var(--ink-soft)">'+Q[i]+'</text>';
    }
    var pts='';for(i=0;i<n;i++){pts+=(i?' ':'')+(ml+step*i+step/2).toFixed(1)+','+y(CAP[i]).toFixed(1);}
    s+='<polyline points="'+pts+'" fill="none" stroke="var(--bear)" stroke-width="2" stroke-dasharray="5 4"/>';
    for(i=0;i<n;i++){s+='<circle cx="'+(ml+step*i+step/2).toFixed(1)+'" cy="'+y(CAP[i]).toFixed(1)+'" r="2.5" fill="var(--bear)"/>';}
    s+='<text x="'+(W-mr)+'" y="'+(y(CAP[n-1])-8).toFixed(1)+'" font-size="10" text-anchor="end" fill="var(--bear)">N3 capacity</text>';
    s+='<text x="'+ml+'" y="'+(mt-5)+'" font-size="10" fill="var(--ink-soft)">kwpm</text></svg>';
    document.getElementById('n3chart').innerHTML=s;
    var lg='';for(k=0;k<V.order.length;k++){lg+='<span><i style="background:'+COLORS[k%COLORS.length]+'"></i>'+esc(V.order[k])+'</span>';}
    document.getElementById('n3legend').innerHTML=lg;
  }
  var btns=document.querySelectorAll('#p-TSM .n3btn');
  btns.forEach(function(b){b.onclick=function(){btns.forEach(function(x){x.classList.toggle('on',x===b);});draw(b.dataset.m);};});
  draw('client');
})();
</script>"""


def n3_widget(section_html):
    return N3_WIDGET + section_html


def tabbed(body, tk):
    """Wrap a rendered company page into Overview (full dossier + sticky TOC) / Intra-quarter
    / Transcripts tabs. Overview keeps ALL sections; the other two surface copies of the
    relevant curated sections (+ raw briefings drawer / source-call list)."""
    m = re.match(r"\s*(<h1>.*?</h1>)", body, re.S)
    h1 = m.group(1) if m else ""
    rest = body[m.end():] if m else body
    parts = [p for p in re.split(r"(?=<h2)", rest) if p.strip()]
    sections = []
    for p in parts:
        hm = re.match(r"<h2[^>]*>(.*?)</h2>", p, re.S)
        title = re.sub(r"<[^>]+>", "", hm.group(1)).strip() if hm else ""
        sections.append((title, p))
    intra = [s for s in sections if INTRA_RE.search(s[0])]
    trans = [s for s in sections if TRANS_RE.search(s[0])]
    cnt, items = [0], []

    def anchor(mm):
        cnt[0] += 1
        sid = "%s-s%d" % (tk, cnt[0])
        items.append((sid, re.sub(r"<[^>]+>", "", mm.group(1)).strip()))
        return '<h2 id="%s">%s</h2>' % (sid, mm.group(1))

    doc = "".join(re.sub(r"<h2[^>]*>(.*?)</h2>", anchor, sec, count=1, flags=re.S) for _, sec in sections)
    toc = "".join('<a href="#%s">%s</a>' % (sid, html.escape(t)) for sid, t in items if t)
    ov = ('<div class="ov"><nav class="toc"><div class="toc-h">On this page</div>%s</nav>'
          '<div class="doc">%s</div></div>' % (toc, doc))
    drawer = _briefings_drawer(tk)
    iq = ("".join(s[1] for s in intra) + drawer) if intra else \
        (drawer or "<p class='byline'>No separate intra-quarter section for this name.</p>")
    tl = _transcript_list(tk)
    tr = ("".join(s[1] for s in trans) + tl) if trans else \
        (tl or "<p class='byline'>No transcripts on disk.</p>")
    # optional extra tab: TSM N3 interactive supply/demand model
    n3secs = [s for s in sections if N3_RE.search(s[0])]
    n3_tab = n3_pane = ""
    if tk == "TSM" and n3secs:
        n3_tab = '<button class="tab" data-p="n3">N3 model</button>'
        n3_pane = '<section class="cpane" data-pane="n3">%s</section>' % n3_widget("".join(s[1] for s in n3secs))
    return (h1
            + '<div class="tabs"><button class="tab on" data-p="ov">Overview</button>'
            + '<button class="tab" data-p="iq">Intra-quarter</button>'
            + '<button class="tab" data-p="tr">Transcripts</button>'
            + n3_tab + '</div>'
            + '<section class="cpane on" data-pane="ov">%s</section>' % ov
            + '<section class="cpane" data-pane="iq">%s</section>' % iq
            + '<section class="cpane" data-pane="tr">%s</section>' % tr
            + n3_pane)


# ---------- home (cover) ----------
def _md_plain(s, limit=None):
    """Strip markdown emphasis / links / code down to a compact one-liner."""
    s = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s)              # [[TICKER]] wiki links
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)          # [text](url)
    s = s.replace("**", "").replace("__", "").replace("`", "")
    s = re.sub(r"(?<!\w)[*_]([^*_]+)[*_](?!\w)", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"^[^\w$(\"'À-ɏ]+", "", s)          # leading emoji / arrows / bullets
    if limit and len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0].rstrip(" ,;:—-") + "…"
    return s


def load_diff_rows(max_rows=8):
    """_meta/diff-latest.md (7-day changelog roll-up) -> substantive rows first (⭐ / Superseded / Drift)."""
    p = WIKI / "_meta" / "diff-latest.md"
    if not p.is_file():
        return {"since": None, "n_pages": 0, "n_rows": 0, "rows": []}
    txt = p.read_text(encoding="utf-8")
    m = re.search(r"since (\d{4}-\d{2}-\d{2})", txt)
    rows = []
    for ln in txt.split("\n"):
        r = re.match(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$", ln)
        if not r:
            continue
        date, tk, change = r.groups()
        star = "⭐" in tk
        tk = tk.replace("⭐", "").strip()
        change = re.sub(r"^\([^)]*\)\*{0,2}\s*[—–-]\s*", "", change.strip())   # "(/wiki-ingest 21h, scheduled)** — "
        sup = re.search(r"\*\*((?:Superseded|Drift)[^*]*)\*\*", change)
        if sup:
            text = sup.group(1)
        else:   # "3 log rows + Sinal note (what was ingested…). Nothing superseded." -> keep the parenthetical
            par = re.search(r"\(([^()]{25,})\)", change)
            text = par.group(1) if par else change
        rows.append({"date": date, "t": tk, "star": star, "sub": bool(star or sup), "text": _md_plain(text, 170)})
    n_pages = len({r["t"] for r in rows})
    rows.sort(key=lambda r: r["date"], reverse=True)
    rows.sort(key=lambda r: (not r["sub"], not r["star"]))
    return {"since": m.group(1) if m else None, "n_pages": n_pages, "n_rows": len(rows), "rows": rows[:max_rows]}


def load_catalyst_rows(max_rows=8, today=None):
    """_meta/catalysts.md 'Upcoming' table -> next dated catalysts from today on."""
    p = WIKI / "_meta" / "catalysts.md"
    if not p.is_file():
        return []
    today = today or datetime.date.today().isoformat()
    out, in_up = [], False
    for ln in p.read_text(encoding="utf-8").split("\n"):
        if ln.startswith("## "):
            in_up = "Upcoming" in ln
            continue
        if not in_up:
            continue
        r = re.match(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([A-Z0-9.\-]{1,12})\s*\|\s*(.*?)\s*\|$", ln)
        if not r or r.group(1) < today:
            continue
        text = _md_plain(r.group(3), 150)
        text = re.sub(r"^(?:By |~)?\d{4}-\d{2}-\d{2}\s*(?:\([A-Za-z]+\)\s*)?[—–-]?\s*", "", text)   # the date column already says it
        out.append({"date": r.group(1), "t": r.group(2), "text": text})
    out.sort(key=lambda r: r["date"])
    return out[:max_rows]


def render_home(groups, themes, est, pages, diff, cats, today):
    """Cover page: hero + stats strip + quick links + what changed / upcoming catalysts + sector cards + theme chips."""
    def badge(t):   # SPA link only for tickers that have a page; show('X') on a missing id would blank the pane
        return (f'<a class="tkb" onclick="show(\'{t}\')">{t}</a>' if t in pages
                else f'<span class="tkb plain">{html.escape(t)}</span>')
    asof = est.get("asof") or "—"
    h = ['<div class="home-hero"><h1>Research Wiki</h1>'
         '<p class="lead">Buy-side synthesis of filings, transcripts, decks, equity calls, broker notes and briefings — '
         'one page per name, one per theme, every datapoint attributed to broker / analyst + date. '
         'Pick a name on the left or search.</p></div>']
    h.append('<div class="stats">'
             f'<div class="stat"><b>{len(pages)}</b><span>companies</span></div>'
             f'<div class="stat"><b>{len(themes)}</b><span>themes</span></div>'
             f'<div class="stat"><b>{diff["n_pages"]}</b><span>pages changed · 7d</span></div>'
             f'<div class="stat"><b>{html.escape(str(asof))}</b><span>BBG consensus as of</span></div>'
             f'<div class="stat"><b>{today}</b><span>built</span></div></div>')
    ql = [("📊", "Screener", "valuation &amp; estimates, sortable", "onclick=\"show('SCREENER')\""),
          ("⏱", "Timeline", "equity calls &amp; mgmt commentary, intra-quarter", 'href="timeline.html"'),
          ("🧭", "Dashboards hub", "edge, read-through, graph, book, labs…", 'href="_dashboards/index.html"'),
          ("📅", "Catalysts", "calendar + outcome loop", 'href="_dashboards/catalysts.html"'),
          ("🔥", "Sentiment", "hot/cold × bull/bear weekly ranking", 'href="_dashboards/sentiment.html"'),
          ("🔀", "What changed", "7-day changelog roll-up", 'href="_dashboards/diff.html"'),
          ("🎯", "Edge", "house vs Street — where we differ", 'href="_dashboards/edge.html"'),
          ("📐", "Assumptions", "canonical cross-page numbers", 'href="_dashboards/assumptions.html"')]
    h.append('<div class="ql">' + "".join(
        f'<a class="qlc" {attr}><span class="ic">{ic}</span><b>{t}</b><small>{d}</small></a>' for ic, t, d, attr in ql) + '</div>')
    ch = "".join(f'<li><span class="d">{r["date"][5:]}</span>{badge(r["t"])}'
                 f'<span class="tx">{"⭐ " if r["star"] else ""}{html.escape(r["text"])}</span></li>' for r in diff["rows"])
    ct = "".join(f'<li><span class="d">{r["date"][5:]}</span>{badge(r["t"])}<span class="tx">{html.escape(r["text"])}</span></li>'
                 for r in cats)
    h.append('<div class="cols2">'
             f'<div class="card"><div class="card-h">What changed<small>{diff["n_rows"]} changelog rows on {diff["n_pages"]} pages '
             f'since {diff["since"] or "—"} · rating / PT moves and superseded numbers first · <a href="_dashboards/diff.html">full list</a></small></div>'
             f'<ul class="feed">{ch or "<li>No changes logged.</li>"}</ul></div>'
             f'<div class="card"><div class="card-h">Upcoming catalysts<small>next {len(cats)} dated events from every page\'s '
             f'"Catalysts / what to watch" · <a href="_dashboards/catalysts.html">calendar</a></small></div>'
             f'<ul class="feed">{ct or "<li>No dated catalysts.</li>"}</ul></div></div>')
    sec = []
    for g in groups:
        items = "".join(f'<li>{badge(it["ticker"])}<span class="tx">{inline(it["thesis"])}</span></li>' for it in g["items"])
        sec.append(f'<section class="sec"><h3>{html.escape(g["theme"])}<small>{len(g["items"])}</small></h3><ul class="feed">{items}</ul></section>')
    h.append('<h2 class="home-h2">Coverage by sector — one-line theses</h2><div class="sec-grid">' + "".join(sec) + '</div>')
    if themes:
        chips = "".join(f'<a class="chip" onclick="show(\'TH-{slug}\')">◆ {html.escape(th["short"])}</a>' for slug, th in themes.items())
        h.append(f'<h2 class="home-h2">Themes — cross-company</h2><div class="chips">{chips}</div>')
    return "".join(h)


def main():
    groups = parse_index()
    est = load_estimates()
    pages = {}   # ticker -> {title, html, text}
    for g in groups:
        for it in g["items"]:
            t = it["ticker"]
            md = (WIKI / f"{t}.md").read_text(encoding="utf-8")
            h1 = re.search(r"^#\s+(.*)$", md, re.M)
            title = h1.group(1).strip() if h1 else t
            body = md_to_html(md)
            text = re.sub(r"<[^>]+>", " ", body)
            text = html.unescape(re.sub(r"\s+", " ", text)).lower()
            pages[t] = {"title": title, "html": body, "text": text, "thesis": it["thesis"]}

    # themes (cross-company pages in _wiki/themes/)
    themes = {}
    tdir = WIKI / "themes"
    if tdir.is_dir():
        for tf in sorted(tdir.glob("*.md")):
            if tf.name in ("_TEMPLATE.md", "00_THEMES.md"):
                continue
            slug = tf.stem
            md = tf.read_text(encoding="utf-8")
            h1 = re.search(r"^#\s+(.*)$", md, re.M)
            ttl = h1.group(1).strip() if h1 else slug
            b = md_to_html(md)
            txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", b))).lower()
            themes[slug] = {"title": ttl, "short": ttl.split("—", 1)[-1].strip(), "html": b, "text": txt}

    # rewrite intra-wiki links (../TICKER.md, themes/slug.md, sibling slug.md) -> SPA navigation
    id_for = {f"{t}.md": t for t in pages}
    id_for["00_INDEX.md"] = "HOME"      # theme pages link these as index/overview
    id_for["00_THEMES.md"] = "HOME"
    for slug in themes:
        id_for[f"themes/{slug}.md"] = f"TH-{slug}"
        id_for[f"{slug}.md"] = f"TH-{slug}"

    def rewrite(b):
        def repl(m):
            tgt = id_for.get(m.group(1).lstrip("./"))   # exact match only (won't touch ../_briefings/X.md etc.)
            return f'<a onclick="show(\'{tgt}\')" style="cursor:pointer">{m.group(2)}</a>' if tgt else m.group(0)
        return re.sub(r'<a href="([^"]+)">(.*?)</a>', repl, b, flags=re.S)

    for t in pages:
        pages[t]["html"] = rewrite(pages[t]["html"])
    for s in themes:
        themes[s]["html"] = rewrite(themes[s]["html"])

    # theme back-links: company -> themes that reference it (parse rewritten theme HTML for show('TICKER'))
    comp2themes = {}
    for slug, th in themes.items():
        for tk in sorted(set(re.findall(r"show\('([A-Z]{1,10})'\)", th["html"]))):
            if tk in pages:
                comp2themes.setdefault(tk, []).append((slug, th["short"]))
    for t in pages:
        ls = comp2themes.get(t)
        if ls:
            tl = " · ".join(f'<a onclick="show(\'TH-{s}\')" style="cursor:pointer">{html.escape(sh)}</a>' for s, sh in ls)
            line = f'<p class="byline">🔖 <b>Themes:</b> {tl}</p>'
            h2i = pages[t]["html"].find("<h2>")
            pages[t]["html"] = (pages[t]["html"][:h2i] + line + pages[t]["html"][h2i:]) if h2i >= 0 else pages[t]["html"] + line

    # screener: sortable valuation/estimates table across all companies
    comps_est = est.get("companies") or {}
    g_of = {it["ticker"]: g["theme"] for g in groups for it in g["items"]}
    cur_sym = {"USD": "$", "EUR": "€", "JPY": "¥", "TWD": "NT$", "GBP": "£", "KRW": "KRW "}
    scr_rows = []
    for t in pages:
        c = comps_est.get(t) or {}
        err = "error" in c
        per = (c.get("periods") or {}) if not err else {}
        cy26 = per.get("CY2026") or {}; cy27 = per.get("CY2027") or {}
        rev26 = cy26.get("rev"); rev27 = cy27.get("rev"); gm = cy26.get("gm"); e26 = cy26.get("eps")
        px = None if err else c.get("px"); ccy = c.get("ccy", "")
        big = ccy in ("JPY", "TWD", "KRW"); dv = 1e6 if big else 1e3; un = "tn" if big else "bn"
        growth = (rev27 / rev26 - 1) * 100 if (rev26 and rev27) else None
        pe = px / e26 if (px and e26 and e26 > 0) else None
        ups = (cy26.get("rev_hi") / rev26 - 1) * 100 if (cy26.get("rev_hi") and rev26) else None
        comp = pages[t]["title"].split("—", 1)[-1].strip() if "—" in pages[t]["title"] else ""

        def C(v, txt):
            return f'<td data-v="{v if v is not None else -1e12:.6f}">{txt}</td>'
        revtxt = f"{cur_sym.get(ccy, ccy)}{rev26/dv:,.1f}{un}" if rev26 else "—"
        scr_rows.append(
            f'<tr><td class="htk"><a onclick="show(\'{t}\')">{t}</a></td>'
            f'<td>{html.escape(comp)[:26]}</td><td class="grp-c">{html.escape(g_of.get(t,""))}</td>'
            + C(rev26, revtxt)
            + C(growth, f"{growth:+.0f}%" if growth is not None else "—")
            + C(gm, f"{gm:.1f}%" if gm is not None else "—")
            + C(e26, f"{e26:,.2f}" if e26 is not None else "—")
            + C(pe, (f"{pe:,.1f}x" if pe < 100 else "n/m") if pe is not None else "—")
            + C(ups, f"{ups:+.0f}%" if ups is not None else "—") + "</tr>")
    scr_head = "<tr>" + "".join(f'<th onclick="sortScr({i})">{h} ⇅</th>' for i, h in enumerate(
        ["Ticker", "Company", "Group", "CY26 Rev", "Rev gr.26→27", "GM CY26", "EPS CY26", "Fwd P/E", "St-high rev"])) + "</tr>"
    screener_html = (
        '<h1>Screener — valuation &amp; estimates</h1>'
        '<p class="byline">Click any column header to sort. BBG consensus (<code>_data/estimates.json</code>). '
        'Revenue is native reporting currency (not cross-comparable); growth / margin / P/E / upside are unitless and comparable. '
        'Fwd P/E = last px ÷ CY26 EPS. "St-high rev" = street-high vs mean CY26 revenue. Blank = awaiting BBG.</p>'
        f'<table class="scr" id="scrTbl"><thead>{scr_head}</thead><tbody>{"".join(scr_rows)}</tbody></table>')

    # sidebar
    side = ['<a class="nav" data-t="SCREENER" onclick="show(\'SCREENER\')">'
            '<span class="tk">📊</span> <span class="co">Screener (valuation)</span></a>',
            '<a class="nav" data-t="TIMELINE" href="timeline.html">'
            '<span class="tk">⏱</span> <span class="co">Equity-calls timeline</span></a>']
    for g in groups:
        side.append(f'<div class="grp"><div class="grp-h">{html.escape(g["theme"])}</div>')
        for it in g["items"]:
            t = it["ticker"]
            comp = pages[t]["title"].split("—", 1)[-1].strip() if "—" in pages[t]["title"] else ""
            side.append(f'<a class="nav" data-t="{t}" onclick="show(\'{t}\')">'
                        f'<span class="tk">{t}</span> <span class="co">{html.escape(comp)}</span></a>')
        side.append("</div>")
    if themes:
        side.append('<div class="grp"><div class="grp-h">Themes</div>')
        for slug, th in themes.items():
            side.append(f'<a class="nav" data-t="TH-{slug}" onclick="show(\'TH-{slug}\')">'
                        f'<span class="tk">◆</span> <span class="co">{html.escape(th["short"])}</span></a>')
        side.append("</div>")
    sidebar = "\n".join(side)

    # home (cover): hero + stats + quick links + what changed / catalysts + sector cards + theme chips
    today = datetime.date.today().isoformat()
    home_html = render_home(groups, themes, est, pages, load_diff_rows(), load_catalyst_rows(today=today), today)

    page_divs = [f'<div class="page" id="p-HOME">{home_html}</div>',
                 f'<div class="page" id="p-SCREENER" style="display:none">{screener_html}</div>']
    for t, p in pages.items():
        body = p["html"]
        fin = render_financials(t, est)
        if fin:
            body = (body.replace("<h2>Sources</h2>", fin + "<h2>Sources</h2>", 1)
                    if "<h2>Sources</h2>" in body else body + fin)
        page_divs.append(f'<div class="page" id="p-{t}" style="display:none">{tabbed(body, t)}</div>')
    for slug, th in themes.items():
        page_divs.append(f'<div class="page" id="p-TH-{slug}" style="display:none">{th["html"]}</div>')

    tpl = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research Wiki — by company</title>
<style>
*{box-sizing:border-box}
:root{ /* Midnight (default) */
  --bg:#13151b;--surface:#1b1e27;--surface-alt:#20242f;--ink:#d7dce6;--ink-soft:#8b94a7;
  --accent:#74a8ff;--border:#2a2f3c;--side-bg:#0d0f14;--side-ink:#cdd6e6;--side-soft:#7e8aa3;
  --side-hover:#1b2540;--code-bg:#222735;--hd:#f2f5fa;--th-bg:#222735;--zebra:#20242f;
  --bull:#4ade80;--bear:#f87171;--plate:#fbfaf6;
  --bfont:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;--hfont:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
[data-theme="paper"]{
  --bg:#f4efe4;--surface:#fffdf8;--surface-alt:#f6f1e6;--ink:#2b2925;--ink-soft:#736d62;
  --accent:#136f63;--border:#e3dccc;--side-bg:#2b2925;--side-ink:#e9e2d3;--side-soft:#b6ac99;
  --side-hover:#3a3630;--code-bg:#efe8d8;--hd:#2b2925;--th-bg:#efe8d8;--zebra:#f6f1e6;
  --bull:#1c7d3f;--bear:#b3402f;--plate:transparent;
  --bfont:Iowan Old Style,Palatino,Georgia,'Times New Roman',serif;--hfont:Iowan Old Style,Palatino,Georgia,serif}
[data-theme="slate"]{
  --bg:#f6f7f9;--surface:#ffffff;--surface-alt:#f4f6f9;--ink:#1f2733;--ink-soft:#6b7686;
  --accent:#4f46e5;--border:#e6e9ef;--side-bg:#141925;--side-ink:#cdd6e6;--side-soft:#94a0b8;
  --side-hover:#1b2540;--code-bg:#eef1f6;--hd:#0f1729;--th-bg:#eef1f6;--zebra:#f4f6f9;
  --bull:#15803d;--bear:#c0392b;--plate:transparent;
  --bfont:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;--hfont:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
body{margin:0;font:15.5px/1.6 var(--bfont);color:var(--ink);background:var(--bg);font-variant-numeric:tabular-nums}
#wrap{display:flex;min-height:100vh}
#side{width:290px;flex:0 0 290px;background:var(--side-bg);color:var(--side-ink);height:100vh;overflow-y:auto;position:sticky;top:0;padding:14px 0}
#side .brand{font-weight:700;font-size:16px;color:#fff;padding:4px 16px 10px}
#side .brand small{display:block;font-weight:400;color:var(--side-soft);font-size:11px;margin-top:2px}
.themes{display:flex;gap:5px;padding:0 14px 12px}
.thbtn{flex:1;background:transparent;border:1px solid var(--side-soft);color:var(--side-soft);border-radius:12px;padding:4px 0;font-size:11px;font-weight:600;cursor:pointer}
.thbtn:hover{color:#fff;border-color:#fff}
.thbtn.on{background:var(--accent);border-color:var(--accent);color:#fff}
#q{width:calc(100% - 24px);margin:0 12px 12px;padding:8px 10px;border:1px solid var(--side-hover);border-radius:7px;background:var(--side-hover);color:#fff;font-size:13px}
#q::placeholder{color:#9aa6c080}
.grp{margin:2px 0 10px}
.grp-h{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--side-soft);padding:8px 16px 4px;font-weight:700}
a.nav{display:flex;align-items:baseline;gap:8px;padding:5px 16px;cursor:pointer;color:var(--side-ink);text-decoration:none;border-left:3px solid transparent}
a.nav:hover{background:var(--side-hover)}
a.nav.active{background:var(--side-hover);border-left-color:var(--accent);color:#fff}
a.nav .tk{font-weight:700;font-size:13px;min-width:42px}
a.nav .co{font-size:11.5px;color:var(--side-soft);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
a.nav.hide{display:none}
.grp.hide{display:none}
#main{flex:1;min-width:0;max-width:1040px;margin:0 auto;padding:30px 46px 80px}
.page h1{font-size:25px;margin:0 0 6px;border-bottom:2px solid var(--border);padding-bottom:10px;color:var(--hd);font-family:var(--hfont)}
.page h2{font-size:18px;margin:26px 0 8px;color:var(--hd);font-family:var(--hfont)}
.page h3{font-size:15px;margin:18px 0 6px;color:var(--ink)}
.byline{color:var(--ink-soft);font-size:12.5px}
.page p{margin:9px 0}
.page ul{margin:8px 0;padding-left:22px}
.page li{margin:5px 0}
.page code{background:var(--code-bg);padding:1px 5px;border-radius:4px;font-size:85%;font-family:ui-monospace,Consolas,monospace;color:var(--ink)}
.page a{color:var(--accent);text-decoration:none}
.page a:hover{text-decoration:underline}
.page table{border-collapse:collapse;width:100%;margin:10px 0;font-size:13.5px;display:block;overflow-x:auto;background:var(--surface)}
.page th,.page td{border:1px solid var(--border);padding:6px 9px;text-align:left;vertical-align:top}
.page th{background:var(--th-bg);font-weight:700;color:var(--ink)}
.page tr:nth-child(even) td{background:var(--zebra)}
.htk a{font-weight:700;cursor:pointer}
.page blockquote{border-left:3px solid var(--accent);margin:10px 0;padding:4px 14px;background:var(--surface-alt);color:var(--ink-soft)}
.page hr{border:0;border-top:1px solid var(--border);margin:18px 0}
.page svg{background:var(--plate);border-radius:6px}
.page table.fin th,.page table.fin td{text-align:right;white-space:nowrap}
.page table.fin td:first-child,.page table.fin th:first-child{text-align:left}
.page table.fin .hi{color:var(--bull);font-size:11px;font-weight:600}
.page table.scr{font-size:12.5px;border-collapse:collapse;width:100%}
.page table.scr th{cursor:pointer;position:sticky;top:0;background:var(--th-bg);user-select:none;white-space:nowrap;font-size:11.5px}
.page table.scr th:hover{filter:brightness(1.12)}
.page table.scr td{white-space:nowrap;text-align:right;border:1px solid var(--border);padding:4px 8px}
.page table.scr td:first-child,.page table.scr td:nth-child(2),.page table.scr td:nth-child(3){text-align:left}
.page table.scr td.grp-c{color:var(--ink-soft);font-size:10.5px}
/* home / cover */
.home-hero h1{border-bottom:0;padding-bottom:0;font-size:30px;margin-bottom:2px}
.home-hero .lead{color:var(--ink-soft);font-size:14px;max-width:780px;margin:4px 0 0}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:18px 0 12px}
.stat{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px 14px;min-width:0}
.stat b{display:block;font-size:22px;color:var(--hd);font-family:var(--hfont);line-height:1.15;white-space:nowrap}
.stat span{font-size:10.5px;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-soft)}
.ql{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:10px;margin:0 0 20px}
.qlc{display:grid;grid-template-columns:auto 1fr;column-gap:11px;align-items:center;background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:11px 13px;cursor:pointer;color:var(--ink)!important;text-decoration:none!important;transition:border-color .15s;min-width:0}
.qlc:hover{border-color:var(--accent);text-decoration:none!important}
.qlc .ic{grid-row:1/3;font-size:21px;line-height:1}
.qlc b{color:var(--hd);font-size:13.5px;line-height:1.25}
.qlc small{color:var(--ink-soft);font-size:11.5px;line-height:1.3}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:0 0 6px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px 14px;min-width:0}
.card-h{font-weight:700;color:var(--hd);font-size:14.5px;margin:0 0 8px;font-family:var(--hfont)}
.card-h small{display:block;font-weight:400;color:var(--ink-soft);font-size:11.5px;font-family:var(--bfont);line-height:1.4;margin-top:2px}
ul.feed{list-style:none;margin:0;padding:0}
ul.feed li{display:grid;grid-template-columns:auto auto 1fr;gap:9px;align-items:baseline;padding:6px 0;border-top:1px solid var(--border);font-size:12.5px;line-height:1.45;margin:0}
ul.feed li:first-child{border-top:0}
ul.feed .d{color:var(--ink-soft);font-size:11px;white-space:nowrap}
ul.feed .tx{color:var(--ink);min-width:0;overflow-wrap:anywhere}
.tkb{display:inline-block;font-weight:700;font-size:11.5px;letter-spacing:.02em;padding:1px 7px;border-radius:6px;background:var(--code-bg);color:var(--accent)!important;cursor:pointer;white-space:nowrap;text-decoration:none!important}
.tkb:hover{filter:brightness(1.15)}
.tkb.plain{cursor:default;color:var(--ink-soft)!important}
.home-h2{font-size:12.5px!important;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-soft)!important;margin:24px 0 10px!important;border-bottom:1px solid var(--border);padding-bottom:6px;font-family:var(--bfont)!important}
.sec-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:14px}
.sec{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px 14px 6px;min-width:0}
.sec h3{margin:0 0 4px!important;font-size:14px!important;color:var(--hd)!important;font-family:var(--hfont)}
.sec h3 small{color:var(--ink-soft);font-weight:400;font-size:11.5px;margin-left:7px}
.sec ul.feed li{grid-template-columns:auto 1fr}
.chips{display:flex;flex-wrap:wrap;gap:7px}
.chip{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:4px 11px;font-size:12.5px;cursor:pointer;color:var(--ink)!important;text-decoration:none!important}
.chip:hover{border-color:var(--accent);color:var(--accent)!important}
@media(max-width:900px){.cols2{grid-template-columns:1fr}.sec-grid{grid-template-columns:1fr}}
/* company-page tabs + sticky TOC */
.tabs{display:flex;gap:2px;border-bottom:1px solid var(--border);margin:2px 0 18px}
.tab{background:transparent;border:0;color:var(--ink-soft);padding:9px 16px;font-size:13.5px;font-weight:600;cursor:pointer;border-bottom:3px solid transparent;font-family:var(--bfont)}
.tab:hover{color:var(--ink)}
.tab.on{color:var(--ink);border-bottom-color:var(--accent)}
.cpane{display:none}.cpane.on{display:block}
.ov{display:grid;grid-template-columns:200px 1fr;gap:34px;align-items:start}
.toc{position:sticky;top:14px;font-size:12.5px;border-left:1px solid var(--border);padding-left:13px;max-height:92vh;overflow:auto}
.toc-h{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);font-weight:700;margin-bottom:6px}
.toc a{display:block;color:var(--ink-soft);text-decoration:none;padding:3px 0;border-left:2px solid transparent;margin-left:-14px;padding-left:12px;line-height:1.4}
.toc a:hover{color:var(--accent)}.toc a.act{color:var(--ink);font-weight:700;border-left-color:var(--accent)}
.doc{max-width:780px;min-width:0}.doc h2{scroll-margin-top:14px}
details{margin:16px 0;border:1px solid var(--border);border-radius:8px;background:var(--surface)}
details summary{cursor:pointer;padding:9px 13px;font-weight:600;font-size:13px;color:var(--ink-soft)}
details[open] summary{border-bottom:1px solid var(--border);color:var(--ink)}
details>*:not(summary){padding:0 13px}
#nohit{display:none;color:var(--side-soft);padding:10px 16px;font-size:13px}
@media(max-width:760px){#side{position:fixed;z-index:9;transform:translateX(-100%);transition:.2s}#side.open{transform:none}#main{padding:20px}#burger{display:block!important}.ov{grid-template-columns:1fr}.toc{position:static;max-height:none;border-left:0;padding-left:0}.doc{max-width:none}}
#burger{display:none;position:fixed;top:10px;left:10px;z-index:10;background:var(--side-bg);color:#fff;border:0;border-radius:6px;padding:8px 11px;cursor:pointer}
</style></head><body>
<button id="burger" onclick="document.getElementById('side').classList.toggle('open')">☰</button>
<div id="wrap">
<nav id="side">
<div class="brand">📊 Research Wiki<small>__SUBTITLE__</small></div>
<div class="themes"><button class="thbtn" data-th="paper">Paper</button><button class="thbtn" data-th="slate">Slate</button><button class="thbtn on" data-th="midnight">Midnight</button></div>
<input id="q" placeholder="Search (ticker, company, or content…)" oninput="filt(this.value)">
<a class="nav active" data-t="HOME" onclick="show('HOME')"><span class="tk">★</span> <span class="co">Overview</span></a>
__SIDEBAR__
<div id="nohit">Nothing found.</div>
</nav>
<main id="main">__PAGES__</main>
</div>
<script>
// Search index. The full text of every page is ALREADY inlined below as
// <div class="page" id="p-...">, so shipping a second copy as a JSON literal
// doubled the file for nothing (~30 MB of 76 MB) and pushed index.html toward
// GitHub's hard 100 MB per-file reject. Derive it from the DOM, lazily, and
// cache. No runtime fetch -- the offline P:/R: copies keep working.
var IDX = {};
function idx(t){
  var v = IDX[t];
  if(v !== undefined) return v;
  var el = document.getElementById('p-' + t);
  if(!el) return (IDX[t] = '');
  // Mirror the old server-side pipeline exactly, or search results would drift:
  // each TAG becomes a SPACE (textContent would join '<td>a</td><td>b</td>' into
  // 'ab' and lose phrase matches across cells), then decode entities, collapse
  // whitespace, lowercase. The textarea decodes entities without parsing tags.
  var ta = document.createElement('textarea');
  ta.innerHTML = el.innerHTML.replace(/<[^>]+>/g, ' ');
  return (IDX[t] = ta.value.replace(/\s+/g, ' ').toLowerCase());
}
// warm the cache while the browser is idle so the first keystroke is instant
(function(){
  var ids = [].map.call(document.querySelectorAll('a.nav'), function(a){return a.dataset.t;});
  var i = 0;
  var idle = window.requestIdleCallback || function(f){return setTimeout(function(){f({timeRemaining:function(){return 8;}});}, 200);};
  function step(dl){
    while(i < ids.length && dl.timeRemaining() > 2){ idx(ids[i++]); }
    if(i < ids.length) idle(step);
  }
  idle(step);
})();
function show(t){
  document.querySelectorAll('.page').forEach(function(p){p.style.display='none'});
  var el=document.getElementById('p-'+t);
  if(el){el.style.display='block';
    if(location.hash !== '#'+t){history.replaceState(null,'','#'+encodeURIComponent(t));}
    // reset this page's tabs to the first (Overview) on navigation
    var tabs=el.querySelectorAll('.tab'),panes=el.querySelectorAll('.cpane');
    tabs.forEach(function(b,i){b.classList.toggle('on',i===0)});
    panes.forEach(function(s,i){s.classList.toggle('on',i===0)});
  }
  document.querySelectorAll('a.nav').forEach(function(a){a.classList.toggle('active',a.dataset.t===t)});
  document.getElementById('main').scrollTo(0,0); window.scrollTo(0,0);
  if(window.innerWidth<=760)document.getElementById('side').classList.remove('open');
}
// theme switch (Midnight default; persisted)
function setTheme(th){
  if(th==='midnight')document.documentElement.removeAttribute('data-theme');
  else document.documentElement.setAttribute('data-theme',th);
  document.querySelectorAll('.thbtn').forEach(function(x){x.classList.toggle('on',x.dataset.th===th)});
  try{localStorage.setItem('wikitheme',th)}catch(e){}
}
document.querySelectorAll('.thbtn').forEach(function(b){b.onclick=function(){setTheme(b.dataset.th)}});
setTheme((function(){try{return localStorage.getItem('wikitheme')}catch(e){return null}})()||'midnight');
// in-page tab switching (delegated, scoped to the page)
document.addEventListener('click',function(e){
  var b=e.target.closest?e.target.closest('.tab'):null; if(!b)return;
  var page=b.closest('.page'); if(!page)return;
  page.querySelectorAll('.tab').forEach(function(x){x.classList.toggle('on',x===b)});
  page.querySelectorAll('.cpane').forEach(function(s){s.classList.toggle('on',s.dataset.pane===b.dataset.p)});
  window.scrollTo(0,0);
});
// sticky-TOC active-section highlight (visible page only)
window.addEventListener('scroll',function(){
  var pg=[].slice.call(document.querySelectorAll('.page')).filter(function(p){return p.style.display!=='none'})[0];
  if(!pg)return; var links=pg.querySelectorAll('.toc a'); if(!links.length)return;
  var y=window.scrollY+90,cur=-1;
  links.forEach(function(a,i){var h=document.getElementById(a.getAttribute('href').slice(1));if(h&&h.offsetTop<=y)cur=i;});
  links.forEach(function(a,i){a.classList.toggle('act',i===cur);});
},{passive:true});
function filt(q){
  q=q.trim().toLowerCase();
  var any=false;
  document.querySelectorAll('a.nav').forEach(function(a){
    var t=a.dataset.t;
    if(t==='HOME'){return}
    var hay=(t+' '+(a.querySelector('.co').textContent||'')).toLowerCase()+' '+idx(t);
    var hit=!q||hay.indexOf(q)>-1;
    a.classList.toggle('hide',!hit); if(hit)any=true;
  });
  document.querySelectorAll('.grp').forEach(function(g){
    var vis=g.querySelectorAll('a.nav:not(.hide)').length;
    g.classList.toggle('hide',vis===0);
  });
  document.getElementById('nohit').style.display=(q&&!any)?'block':'none';
}
function sortScr(col){
  var tb=document.querySelector('#scrTbl tbody'); if(!tb)return;
  var rows=[].slice.call(tb.rows);
  var asc=tb.getAttribute('data-asc')==col?false:true;
  tb.setAttribute('data-asc',asc?col:'-1');
  rows.sort(function(a,b){
    if(col<=2){var av=a.cells[col].textContent.trim().toLowerCase(),bv=b.cells[col].textContent.trim().toLowerCase();
      return asc?(av<bv?-1:av>bv?1:0):(av>bv?-1:av<bv?1:0);}
    var x=parseFloat(a.cells[col].getAttribute('data-v')),y=parseFloat(b.cells[col].getAttribute('data-v'));
    return asc?x-y:y-x;
  });
  rows.forEach(function(r){tb.appendChild(r);});
}
// Direct page links preserve the existing layout and let source inventories return to an issuer.
function openLinkedPage(){
  var t;
  try{t=decodeURIComponent(location.hash.slice(1));}catch(e){return;}
  if(t && document.getElementById('p-'+t)){show(t);}
}
window.addEventListener('hashchange',openLinkedPage);
openLinkedPage();
</script></body></html>"""
    out = (tpl.replace("__SIDEBAR__", sidebar)
              .replace("__SUBTITLE__", f"{len(pages)} companies · {len(themes)} themes")
              .replace("__PAGES__", "\n".join(page_divs)))
    (WIKI / "index.html").write_text(out, encoding="utf-8")
    print(f"index.html written: {len(pages)} companies + {len(themes)} themes, "
          f"{(WIKI / 'index.html').stat().st_size//1024} KB")


if __name__ == "__main__":
    main()
