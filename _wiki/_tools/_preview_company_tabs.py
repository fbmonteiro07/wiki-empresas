r"""
PROTOTYPE — hybrid tabbed company view (one ticker, standalone HTML).

Does NOT touch the .md source or the main index.html. Reuses build_wiki_html's
markdown renderer so the look matches. Layout chosen with Felipe (2026-06-26):
  - ONE 'Overview' tab = the full dossier in a single readable scroll + a sticky
    in-page table of contents (Ctrl-F / print stay intact).
  - 'Intra-quarter' tab = the sibling _briefings/by-ticker/<TICKER>.md roll-up.
  - 'Transcripts' tab = the raw earnings transcripts (list + links; summaries are
    a later phase — they need a generation step, not just rendering).

    py "E:/Wiki Felipe empresas/_wiki/_tools/_preview_company_tabs.py" NVDA

Writes _wiki/_preview_<TICKER>_tabs.html.
"""
import sys, re, html
from pathlib import Path

ROOT = Path("E:/Wiki Felipe empresas")
WIKI = ROOT / "_wiki"
sys.path.insert(0, str(Path("E:/.claude/scripts")))
import build_wiki_html as B   # md_to_html, render_financials, load_estimates
sys.stdout.reconfigure(encoding="utf-8")


def split_sections(body):
    """Split rendered body into [(title, inner_html), ...] on <h2> boundaries.
    Anything before the first <h2> is returned under title '' (intro/byline)."""
    parts = re.split(r"(?=<h2)", body)
    out = []
    for p in parts:
        if not p.strip():
            continue
        m = re.match(r"<h2[^>]*>(.*?)</h2>", p, flags=re.S)
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
        out.append((title, p))
    return out


# which dossier sections feed which tab (everything else stays in Overview)
INTRA_RE = re.compile(r"intra-quarter|in the inbox", re.I)
TRANS_RE = re.compile(r"management commentary", re.I)


def build_overview(sections):
    """Concat overview sections, inject <h2> ids, and build the sticky TOC from them."""
    items, n, html_parts = [], [0], []

    def anchor(m):
        n[0] += 1
        sid = f"s{n[0]}"
        items.append((sid, re.sub(r"<[^>]+>", "", m.group(1)).strip()))
        return f'<h2 id="{sid}">{m.group(1)}</h2>'

    for _, sec in sections:
        html_parts.append(re.sub(r"<h2[^>]*>(.*?)</h2>", anchor, sec, count=1, flags=re.S))
    toc = "".join(f'<a href="#{sid}">{html.escape(t)}</a>' for sid, t in items if t)
    toc_html = f'<nav class="toc"><div class="toc-h">On this page</div>{toc}</nav>'
    return toc_html, "".join(html_parts)


def transcript_list(ticker):
    tdir = ROOT / ticker / "transcripts"
    if not tdir.is_dir():
        return ""
    files = []
    for f in tdir.glob("*.md"):
        m = re.search(r"(20\d\d-\d\d-\d\d)", f.name)
        files.append((m.group(1) if m else "", f))
    if not files:
        return ""
    rows = []
    for date, f in sorted(files, reverse=True):
        label = re.sub(r"_20\d\d-\d\d-\d\d.*$", "", f.name).replace("_", " ")
        rows.append(f'<tr><td>{date}</td><td>{html.escape(label)}</td>'
                    f'<td><a href="../{ticker}/transcripts/{f.name}">open ↗</a></td></tr>')
    return ("<h3>Source calls</h3><table><thead><tr><th>Date</th><th>Call</th><th></th></tr>"
            "</thead><tbody>" + "".join(rows) + "</tbody></table>")


def main():
    ticker = (sys.argv[1] if len(sys.argv) > 1 else "NVDA").upper()
    md = (WIKI / f"{ticker}.md").read_text(encoding="utf-8")
    h1 = re.search(r"^#\s+(.*)$", md, re.M)
    title = h1.group(1).strip() if h1 else ticker

    est = B.load_estimates()
    body = B.md_to_html(md)
    fin = B.render_financials(ticker, est)
    if fin:
        body = (body.replace("<h2>Sources</h2>", fin + "<h2>Sources</h2>", 1)
                if "<h2>Sources</h2>" in body else body + fin)
    body = re.sub(r"^\s*<h1>.*?</h1>", "", body, count=1, flags=re.S)  # H1 lives in the header

    # Overview keeps the FULL dossier; the tabs are highlighted shortcuts that surface
    # copies of the relevant curated sections on top (source .md unchanged).
    sections = split_sections(body)
    intra_secs = [s for s in sections if INTRA_RE.search(s[0])]
    trans_secs = [s for s in sections if TRANS_RE.search(s[0])]
    toc, anchored = build_overview(sections)

    # ----- Intra-quarter tab: the curated chronological digest, + raw email feed in a drawer -----
    bf = ROOT / "_briefings" / "by-ticker" / f"{ticker}.md"
    raw_feed = ""
    if bf.is_file():
        raw_feed = ('<details><summary>Raw email / FinTwit feed (briefings roll-up)</summary>'
                    + B.md_to_html(bf.read_text(encoding="utf-8")) + '</details>')
    if intra_secs:
        intra = ('<p class="byline">Chronological digest of the intra-quarter flow — sell-side '
                 'reports, expert/equity calls and email datapoints since the last print, '
                 'summarized & dated (curated in the dossier).</p>'
                 + "".join(s[1] for s in intra_secs) + raw_feed)
    else:
        intra = ('<p class="byline">No curated intra-quarter section yet for this name '
                 '(thin coverage) — showing the raw briefings feed.</p>'
                 + (raw_feed or "<p class='byline'>No briefings roll-up file.</p>"))

    # ----- Transcripts tab: the discourse-evolution table + the source-call list -----
    tlist = transcript_list(ticker)
    if trans_secs:
        trans = ('<p class="byline">How management\'s discourse evolved across the earnings calls '
                 '(quarter-over-quarter), with the source transcripts below.</p>'
                 + "".join(s[1] for s in trans_secs) + tlist)
    else:
        trans = ('<p class="byline">No curated commentary-evolution table yet for this name. '
                 'Source transcripts below.</p>' + (tlist or "<p class='byline'>No transcripts found.</p>"))

    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — tabbed preview</title>
<style>
*{{box-sizing:border-box}}
/* ---- THEME: Paper (default) — warm, editorial, serif headings ---- */
:root{{
  --bg:#f4efe4; --surface:#fffdf8; --surface-alt:#f6f1e6; --ink:#2b2925; --ink-soft:#736d62;
  --accent:#136f63; --accent-2:#b3402f; --border:#e3dccc; --th-bg:#efe8d8;
  --hd-bg:#2b2925; --hd-ink:#f4efe4; --hd-soft:#b6ac99;
  --bull:#1c7d3f; --bear:#b3402f; --code-bg:#efe8d8;
  --flag-bg:#fbf3da; --flag-bd:#e6cf94; --flag-ink:#8a6d1b;
  --bfont:Iowan Old Style,Palatino,Georgia,'Times New Roman',serif;
  --hfont:Iowan Old Style,Palatino,Georgia,serif;
  --plate:transparent;
}}
/* ---- THEME: Slate — clean cool light, sans ---- */
[data-theme="slate"]{{
  --bg:#f6f7f9; --surface:#ffffff; --surface-alt:#f4f6f9; --ink:#1f2733; --ink-soft:#6b7686;
  --accent:#4f46e5; --accent-2:#0ea5a0; --border:#e6e9ef; --th-bg:#eef1f6;
  --hd-bg:#141925; --hd-ink:#ffffff; --hd-soft:#94a0b8;
  --bull:#15803d; --bear:#c0392b; --code-bg:#eef1f6;
  --flag-bg:#eef2ff; --flag-bd:#c7d0f5; --flag-ink:#4338ca;
  --bfont:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
  --hfont:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
  --plate:transparent;
}}
/* ---- THEME: Midnight — dark, terminal feel ---- */
[data-theme="midnight"]{{
  --bg:#13151b; --surface:#1b1e27; --surface-alt:#20242f; --ink:#d7dce6; --ink-soft:#8b94a7;
  --accent:#74a8ff; --accent-2:#5eead4; --border:#2a2f3c; --th-bg:#222735;
  --hd-bg:#0d0f14; --hd-ink:#f2f5fa; --hd-soft:#7e8aa3;
  --bull:#4ade80; --bear:#f87171; --code-bg:#222735;
  --flag-bg:#1f2a2a; --flag-bd:#2f4a45; --flag-ink:#84d8c9;
  --bfont:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
  --hfont:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
  --plate:#fbfaf6;
}}
body{{margin:0;font:16px/1.68 var(--bfont);color:var(--ink);background:var(--bg);
  -webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}}
.top{{background:var(--hd-bg);color:var(--hd-ink);padding:16px 30px;display:flex;
  justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}}
.top h1{{margin:0;font-size:23px;font-family:var(--hfont);letter-spacing:-.01em}}
.top .by{{color:var(--hd-soft);font-size:12.5px;margin-top:3px}}
.top a{{color:var(--accent);text-decoration:none}}
.themes{{display:flex;gap:6px}}
.thbtn{{background:transparent;border:1px solid var(--hd-soft);color:var(--hd-soft);border-radius:13px;
  padding:4px 12px;font-size:11.5px;font-weight:600;cursor:pointer}}
.thbtn:hover{{color:var(--hd-ink);border-color:var(--hd-ink)}}
.thbtn.on{{background:var(--accent);border-color:var(--accent);color:#fff}}
.tabs{{display:flex;gap:2px;background:var(--hd-bg);padding:0 30px}}
.tab{{background:transparent;border:0;color:var(--hd-soft);padding:11px 18px;font-size:13.5px;font-weight:600;
     cursor:pointer;border-bottom:3px solid transparent}}
.tab:hover{{color:var(--hd-ink)}}
.tab.on{{color:var(--hd-ink);border-bottom-color:var(--accent)}}
main{{max-width:1080px;margin:0 auto;padding:26px 30px 90px}}
.pane{{display:none}} .pane.on{{display:block}}
/* overview = sticky TOC + doc */
.ov{{display:grid;grid-template-columns:210px 1fr;gap:38px;align-items:start}}
.toc{{position:sticky;top:14px;font-size:12.5px;border-left:1px solid var(--border);padding-left:14px;max-height:90vh;overflow:auto}}
.toc-h{{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);font-weight:700;margin-bottom:6px}}
.toc a{{display:block;color:var(--ink-soft);text-decoration:none;padding:3px 0;border-left:2px solid transparent;margin-left:-15px;padding-left:13px;line-height:1.4}}
.toc a:hover{{color:var(--accent)}} .toc a.act{{color:var(--ink);font-weight:700;border-left-color:var(--accent)}}
.doc{{max-width:760px}}
.doc h2{{font-family:var(--hfont);font-size:21px;margin:34px 0 10px;color:var(--ink);scroll-margin-top:14px;
  padding-bottom:6px;border-bottom:1px solid var(--border);letter-spacing:-.01em}}
.doc h2:first-child{{margin-top:4px}}
.doc h3{{font-size:15.5px;margin:18px 0 6px;color:var(--ink);font-weight:700}}
.doc p{{margin:11px 0}} .doc ul{{margin:10px 0;padding-left:22px}} .doc li{{margin:6px 0}}
.byline{{color:var(--ink-soft);font-size:12.5px}}
.doc strong{{color:var(--ink);font-weight:700}}
.doc a,main a{{color:var(--accent);text-decoration:none;border-bottom:1px solid color-mix(in srgb,var(--accent) 30%,transparent)}}
.doc a:hover{{border-bottom-color:var(--accent)}}
code{{background:var(--code-bg);padding:1px 5px;border-radius:4px;font-size:85%;font-family:ui-monospace,Consolas,monospace;color:var(--ink)}}
table{{border-collapse:collapse;width:100%;margin:14px 0;font-size:13.5px;display:block;overflow-x:auto;
  background:var(--surface);border-radius:8px}}
th,td{{border:1px solid var(--border);padding:7px 11px;text-align:left;vertical-align:top}}
th{{background:var(--th-bg);font-weight:700;color:var(--ink)}} tr:nth-child(even) td{{background:var(--surface-alt)}}
table.fin th,table.fin td{{text-align:right;white-space:nowrap}}
table.fin td:first-child,table.fin th:first-child{{text-align:left}}
table.fin .hi{{color:var(--bull);font-size:11px;font-weight:600}}
/* inline snapshot SVG sits on a light plate so its baked-in colors stay legible on any theme */
.doc svg{{background:var(--plate);border-radius:6px}}
blockquote{{border-left:3px solid var(--accent);margin:14px 0;padding:6px 16px;background:var(--surface-alt);color:var(--ink-soft);border-radius:0 6px 6px 0}}
.flag{{background:var(--flag-bg);border:1px solid var(--flag-bd);border-radius:8px;padding:10px 14px;font-size:12.5px;color:var(--flag-ink);margin:4px 0 22px}}
.flag code{{background:color-mix(in srgb,var(--flag-ink) 12%,transparent)}}
.pane>.byline:first-child{{margin-top:0;font-size:13px}}
details{{margin:18px 0;border:1px solid var(--border);border-radius:8px;background:var(--surface)}}
details summary{{cursor:pointer;padding:10px 14px;font-weight:600;font-size:13px;color:var(--ink-soft);user-select:none}}
details[open] summary{{border-bottom:1px solid var(--border);color:var(--ink)}}
details>*:not(summary){{padding:0 14px}}
.pane h3{{font-family:var(--hfont);font-size:16px;margin:22px 0 6px;color:var(--ink)}}
@media(max-width:780px){{.ov{{grid-template-columns:1fr}}.toc{{position:static;max-height:none;border-left:0;padding-left:0}}.doc{{max-width:none}}}}
</style></head><body>
<div class="top"><div><h1>{html.escape(title)}</h1>
<div class="by">Hybrid tabbed preview · prototype on one ticker · <a href="index.html">← back to wiki</a></div></div>
<div class="themes">
  <button class="thbtn on" data-th="paper">Paper</button>
  <button class="thbtn" data-th="slate">Slate</button>
  <button class="thbtn" data-th="midnight">Midnight</button>
</div></div>
<div class="tabs">
  <button class="tab on" data-p="ov">Overview</button>
  <button class="tab" data-p="iq">Intra-quarter</button>
  <button class="tab" data-p="tr">Transcripts</button>
</div>
<main>
  <section class="pane on" id="pane-ov">
    <div class="flag">📐 <b>Prototype.</b> Source stays one <code>{ticker}.md</code>. Overview holds the <b>full dossier</b> (with a sticky table of contents); the <i>Intra-quarter</i> and <i>Transcripts</i> tabs on top are highlighted shortcuts to the same curated sections.</div>
    <div class="ov">{toc}<div class="doc">{anchored}</div></div>
  </section>
  <section class="pane" id="pane-iq">{intra}</section>
  <section class="pane" id="pane-tr">{trans}</section>
</main>
<script>
document.querySelectorAll('.thbtn').forEach(function(b){{b.onclick=function(){{
  document.querySelectorAll('.thbtn').forEach(function(x){{x.classList.remove('on')}});
  b.classList.add('on');
  if(b.dataset.th==='paper')document.documentElement.removeAttribute('data-theme');
  else document.documentElement.setAttribute('data-theme',b.dataset.th);
}};}});
document.querySelectorAll('.tab').forEach(function(b){{b.onclick=function(){{
  document.querySelectorAll('.tab').forEach(function(x){{x.classList.remove('on')}});
  document.querySelectorAll('.pane').forEach(function(x){{x.classList.remove('on')}});
  b.classList.add('on'); document.getElementById('pane-'+b.dataset.p).classList.add('on');
  window.scrollTo(0,0);
}};}});
// active-section highlight in the TOC
var links=[].slice.call(document.querySelectorAll('.toc a'));
var heads=links.map(function(a){{return document.getElementById(a.getAttribute('href').slice(1));}});
window.addEventListener('scroll',function(){{
  var y=window.scrollY+90,cur=-1;
  heads.forEach(function(h,i){{if(h&&h.offsetTop<=y)cur=i;}});
  links.forEach(function(a,i){{a.classList.toggle('act',i===cur);}});
}},{{passive:true}});
</script></body></html>"""

    out = WIKI / f"_preview_{ticker}_tabs.html"
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out}  ({out.stat().st_size//1024} KB)")


if __name__ == "__main__":
    main()
