r"""
FEATURE 3 — Read-through / supply-chain graph.

The wiki is per-ticker; this adds the cross-company axis. From a curated
high-confidence edge set (_data/graph.json) it builds, for every name, its
upstream suppliers + downstream customers + competitors, plus the read-through
statement (a datapoint on a supplier reads through to its customers and back).

Writes _meta/readthrough.md + _dashboards/readthrough.html. Read-only on pages.

    py "E:/Wiki Felipe empresas/_wiki/_tools/build_readthrough.py"
"""
import sys, json, html
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from _wlib import DATA, META, DASH, company_pages, html_head, TODAY
sys.stdout.reconfigure(encoding="utf-8")


def main():
    g = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    supplies = g.get("supplies", [])
    competes = g.get("competes", [])

    known = {tk for tk, _ in company_pages()} | {"ANTHROPIC", "OPENAI"}

    # adjacency
    customers = {}   # u -> [(d, what)]   (who u sells to / downstream)
    suppliers = {}   # d -> [(u, what)]   (who supplies d / upstream)
    peers = {}       # t -> [(other, what)]
    for u, d, what in supplies:
        customers.setdefault(u, []).append((d, what))
        suppliers.setdefault(d, []).append((u, what))
    for a, b, what in competes:
        peers.setdefault(a, []).append((b, what))
        peers.setdefault(b, []).append((a, what))

    nodes = sorted(set(customers) | set(suppliers) | set(peers))
    unknown = sorted(n for n in nodes if n not in known)

    def chips(pairs):
        return ", ".join(f"{t} ({w})" for t, w in sorted(pairs)) if pairs else "—"

    # ---------- markdown ----------
    md = [f"# Read-through map — supply chain & substitutes\n",
          f"_Generated {TODAY.isoformat()} · curated high-confidence edges from "
          f"`_data/graph.json` ({len(supplies)} supply links, {len(competes)} compete links). "
          f"A datapoint on a **supplier** reads through to its **customers** (and vice-versa). "
          f"Edit the JSON to extend; rebuild: `py _wiki/_tools/build_readthrough.py`._\n",
          "| Ticker | ⬆ Suppliers (upstream) | ⬇ Customers (downstream) | ⚔ Competes |",
          "|---|---|---|---|"]
    for t in nodes:
        md.append(f"| **{t}** | {chips(suppliers.get(t, []))} | {chips(customers.get(t, []))} | "
                  f"{chips(peers.get(t, []))} |")
    if unknown:
        md.append(f"\n> ⚠️ Edge endpoints with no wiki page yet: {', '.join(unknown)}.\n")
    md.append("\n## How to use\n")
    md.append("- A **supplier beat/miss** (e.g. an HBM price step at MU/SKHYNIX) reads through to "
              "its **customers** (NVDA/AMD/AVGO) — margin/BOM.")
    md.append("- A **customer capex change** (hyperscaler) reads back to its **suppliers** "
              "(NVDA → TSM/SKHYNIX/COHR → ASML/AMAT).")
    META.mkdir(parents=True, exist_ok=True)
    (META / "readthrough.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # ---------- html ----------
    head, foot = html_head("Read-through map — supply chain & substitutes",
                           f"{TODAY.isoformat()} · {len(supplies)} supply + {len(competes)} compete links")
    h = [head]
    h.append("<p class='byline'>Pick a name to highlight its neighbourhood. A datapoint on a "
             "<b>supplier</b> reads through to its <b>customers</b> and back. "
             "Edges are curated (<code>_data/graph.json</code>).</p>")
    # selector
    opts = "".join(f"<option value='{t}'>{t}</option>" for t in nodes)
    h.append(f"<p>Focus: <select id='focus' onchange='hl()'><option value=''>— all —</option>{opts}</select></p>")
    h.append("<table id='rt'><thead><tr><th>Ticker</th><th>⬆ Suppliers (upstream)</th>"
             "<th>⬇ Customers (downstream)</th><th>⚔ Competes</th></tr></thead><tbody>")
    for t in nodes:
        def cell(pairs):
            return ", ".join(f"<span class='nb' data-n='{x}'>{x}</span> "
                             f"<span class='mut'>({html.escape(w)})</span>" for x, w in sorted(pairs)) or "—"
        h.append(f"<tr data-t='{t}'><td class='tk' data-n='{t}'><b>{t}</b></td>"
                 f"<td>{cell(suppliers.get(t, []))}</td><td>{cell(customers.get(t, []))}</td>"
                 f"<td>{cell(peers.get(t, []))}</td></tr>")
    h.append("</tbody></table>")
    if unknown:
        h.append(f"<p class='byline'>⚠️ Endpoints without a wiki page yet: {', '.join(unknown)}.</p>")
    h.append("""<script>
function hl(){var f=document.getElementById('focus').value;
var rows=document.querySelectorAll('#rt tbody tr');
rows.forEach(function(r){
 var t=r.getAttribute('data-t');
 if(!f){r.style.display='';r.style.background='';return;}
 var names=[].map.call(r.querySelectorAll('[data-n]'),function(s){return s.getAttribute('data-n');});
 var hit=(t===f)||names.indexOf(f)>-1;
 r.style.display=hit?'':'none';
 r.style.background=(t===f)?'#fff7e6':'';
});}
</script>""")
    h.append(foot)
    DASH.mkdir(parents=True, exist_ok=True)
    (DASH / "readthrough.html").write_text("\n".join(h), encoding="utf-8")

    print(f"read-through: {len(nodes)} nodes, {len(supplies)} supply + {len(competes)} compete edges")
    if unknown:
        print(f"  edges to non-page nodes: {', '.join(unknown)}")
    print(f"  -> {META/'readthrough.md'}\n  -> {DASH/'readthrough.html'}")


if __name__ == "__main__":
    main()
