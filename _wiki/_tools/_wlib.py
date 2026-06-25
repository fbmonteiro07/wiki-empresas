r"""
Shared helpers for the empresas-wiki feature tools (E:\Wiki Felipe empresas\_wiki\_tools).

Pure-stdlib (the machine sits behind a TLS proxy — no pip). Everything here is
READ-ONLY against the wiki pages; the feature scripts only ever WRITE to
_wiki/_meta, _wiki/_data and _wiki/_dashboards (never mutate a company page).
"""
from pathlib import Path
import re
import json
import datetime as dt

WIKI = Path("E:/Wiki Felipe empresas/_wiki")
META = WIKI / "_meta"
DATA = WIKI / "_data"
DASH = WIKI / "_dashboards"
TOOLS = WIKI / "_tools"

TODAY = dt.date.today()
DATE_RE = re.compile(r"(20\d\d-\d\d-\d\d)")


def company_pages():
    """Yield (ticker, Path) for every real company page (skips _TEMPLATE, 00_INDEX, etc.)."""
    for p in sorted(WIKI.glob("*.md")):
        if p.name.startswith(("_", "00_")):
            continue
        yield p.stem, p


def read(p):
    return Path(p).read_text(encoding="utf-8", errors="replace")


def load_estimates():
    p = DATA / "estimates.json"
    if p.is_file():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def section(md, heading_regex):
    """Return the body text of the first '## ...' section whose title matches
    heading_regex (case-insensitive), up to the next '## ' or EOF. '' if absent."""
    lines = md.split("\n")
    rx = re.compile(heading_regex, re.I)
    out, capturing = [], False
    for ln in lines:
        h = re.match(r"^##\s+(.*)$", ln)
        if h:
            if capturing:
                break
            if rx.search(h.group(1)):
                capturing = True
            continue
        if capturing:
            out.append(ln)
    return "\n".join(out).strip()


def parse_md_table(block):
    """Parse the first GitHub pipe-table found in `block`.
    Returns (header:list[str], rows:list[list[str]]) or (None, [])."""
    lines = [l for l in block.split("\n")]
    for i in range(len(lines) - 1):
        if lines[i].strip().startswith("|") and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            header = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
                j += 1
            return header, rows
    return None, []


_NUM = re.compile(r"-?\$?\s*([\d,]+(?:\.\d+)?)")


def num(cell):
    """Best-effort first number out of a markdown cell ('$9.26' -> 9.26, '+89%' -> 89.0).
    Strips markdown emphasis and &nbsp;. Returns float or None."""
    if cell is None:
        return None
    s = cell.replace("&nbsp;", " ").replace("*", "").replace("`", "").strip()
    s = s.lstrip("—-– ").strip()
    m = _NUM.search(s)
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except ValueError:
        return None


def changelog_entries(md):
    """Yield (date:str, text:str) dated bullets from a page's '## Changelog' section."""
    body = section(md, r"^Changelog\b")
    for ln in body.split("\n"):
        m = re.match(r"^\s*[-*]\s+(20\d\d-\d\d-\d\d)\s*[—\-–:]\s*(.*)$", ln)
        if m:
            yield m.group(1), m.group(2).strip()


def html_head(title, subtitle=""):
    """Self-contained dark/light dashboard chrome matching the wiki look. Returns (head, foot)."""
    head = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;font:15px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#1a1f29;background:#f5f6f8}}
header{{background:#0f1729;color:#fff;padding:18px 28px}}
header h1{{margin:0;font-size:20px}} header p{{margin:4px 0 0;color:#8492ad;font-size:13px}}
header a{{color:#7fb0ff;text-decoration:none}}
main{{max-width:1180px;margin:0 auto;padding:24px 28px 80px}}
h2{{font-size:17px;margin:26px 0 8px;color:#0f1729;border-bottom:1px solid #e3e7ee;padding-bottom:6px}}
table{{border-collapse:collapse;width:100%;margin:10px 0;font-size:13px}}
th,td{{border:1px solid #dde2ea;padding:6px 9px;text-align:left;vertical-align:top}}
th{{background:#eef1f6;font-weight:700;cursor:pointer;user-select:none;white-space:nowrap;position:sticky;top:0}}
th:hover{{background:#e2e7f0}}
tr:nth-child(even) td{{background:#fafbfc}}
td.r,th.r{{text-align:right;white-space:nowrap}}
.tk a{{font-weight:700;color:#1c5fd6;text-decoration:none}}
.pos{{color:#1c7d3f;font-weight:600}} .neg{{color:#c0392b;font-weight:600}} .mut{{color:#6b7280}}
.byline{{color:#6b7280;font-size:12.5px}}
.pill{{display:inline-block;padding:1px 7px;border-radius:10px;font-size:11px;font-weight:600}}
.pill.up{{background:#e7f6ec;color:#1c7d3f}} .pill.dn{{background:#fdecea;color:#c0392b}} .pill.due{{background:#fff3cd;color:#8a6d1b}}
code{{background:#eef1f6;padding:1px 5px;border-radius:4px;font-size:85%;font-family:ui-monospace,Consolas,monospace}}
</style></head><body>
<header><h1>{title}</h1><p>{subtitle} · <a href="../index.html">← back to wiki</a></p></header><main>"""
    foot = """</main>
<script>
function sortT(t,col,numeric){var tb=t.tBodies[0];var rows=[].slice.call(tb.rows);
var asc=t.getAttribute('data-c')==col?!(t.getAttribute('data-a')=='1'):true;
t.setAttribute('data-c',col);t.setAttribute('data-a',asc?'1':'0');
rows.sort(function(a,b){var x=a.cells[col],y=b.cells[col];
var av=numeric?parseFloat(x.getAttribute('data-v')||x.textContent):x.textContent.trim().toLowerCase();
var bv=numeric?parseFloat(y.getAttribute('data-v')||y.textContent):y.textContent.trim().toLowerCase();
if(numeric){av=isNaN(av)?-1e15:av;bv=isNaN(bv)?-1e15:bv;}
return asc?(av>bv?1:av<bv?-1:0):(av<bv?1:av>bv?-1:0);});
rows.forEach(function(r){tb.appendChild(r);});}
document.querySelectorAll('table.sortable').forEach(function(t){
[].forEach.call(t.tHead.rows[0].cells,function(th,i){th.onclick=function(){sortT(t,i,th.classList.contains('r'));};});});
</script></body></html>"""
    return head, foot
