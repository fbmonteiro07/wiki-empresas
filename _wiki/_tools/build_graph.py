r"""
FEATURE 10 — Full knowledge graph of the research repo.

Extends the curated supply-chain graph (_data/graph.json) into a graph of the
WHOLE information repository — derived, no hand-curation beyond what exists:

  nodes: tickers (sector from 00_INDEX, thesis, book membership, docs on disk,
         next catalyst) · themes · canonical assumptions · brokers/analysts
  edges: supplies / competes        (from graph.json, curated)
         theme --exposes--> ticker  (from ](../TICKER.md) links in theme pages)
         assumption --cites--> page (from assumptions.json cited_in)
         broker --covers--> ticker  (attribution mentions in the ticker page, n>=2)

Writes _data/graph_full.json + _dashboards/graph.html (self-contained force
layout, no external deps). Query it with graph_query.py. Read-only on pages.

    py "E:/Wiki Felipe empresas/_wiki/_tools/build_graph.py"
"""
import sys, json, re, sqlite3, html
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from _wlib import (WIKI, META, DATA, DASH, read, company_pages, parse_md_table,
                   changelog_entries, TODAY)
sys.stdout.reconfigure(encoding="utf-8")

# Broker / research-shop attribution lexicon (regex -> canonical node id)
BROKERS = {
    "BofA": r"\bBofA\b|Bank of America|\bArya\b", "UBS": r"\bUBS\b|\bArcuri\b",
    "JPM": r"\bJPM\b|J\.?P\.? ?Morgan|\bSur\b(?!\w)", "MS": r"\bMorgan Stanley\b|\bMS\b(?= [A-Z(])",
    "Jefferies": r"\bJefferies\b", "Citi": r"\bCiti\b", "GS": r"\bGS\b|Goldman",
    "DB": r"\bDB\b(?= )|Deutsche Bank", "Barclays": r"\bBarclays\b", "Bernstein": r"\bBernstein\b",
    "Redburn": r"\bRedburn\b", "Nomura": r"\bNomura\b", "Fubon": r"\bFubon\b",
    "SIG": r"\bSIG\b|Susquehanna", "TDCowen": r"TD ?Cowen", "Cantor": r"\bCantor\b",
    "Evercore": r"\bEvercore\b", "Mizuho": r"\bMizuho\b", "KeyBanc": r"\bKeyBanc\b",
    "Wolfe": r"\bWolfe\b", "Melius": r"\bMelius\b", "NewStreet": r"New Street",
    "MoffettNathanson": r"Moffett", "TrendForce": r"\bTrendForce\b",
    "SemiAnalysis": r"\bSemiAnalysis\b", "Stratechery": r"\bStratechery\b|Ben Thompson",
    "650Group": r"650 Group", "Omdia": r"\bOmdia\b", "Barrons": r"Barron'?s",
    "FinTwit": r"\bFinTwit\b|@\w{3,}",
}
BROKER_RX = {k: re.compile(v) for k, v in BROKERS.items()}
MIN_MENTIONS = 2
TICKER_LINK = re.compile(r"\]\(\.\./([A-Z][A-Z0-9.]{0,9})\.md\)")


def index_meta():
    """ticker -> (sector, thesis) from 00_INDEX.md."""
    out, sector = {}, ""
    for ln in read(WIKI / "00_INDEX.md").split("\n"):
        h = re.match(r"^##\s+(.*)$", ln)
        if h:
            sector = h.group(1).strip()
            continue
        m = re.match(r"^\|\s*(\w[\w.]*)\s*\|\s*\[[^\]]+\]\([^)]+\)\s*\|\s*(.+?)\s*\|\s*$", ln)
        if m:
            out[m.group(1).upper()] = (sector, m.group(2))
    return out


def doc_counts():
    """ticker -> {kind: n} from the search index (transcripts, filings, briefings...)."""
    out = {}
    db = DATA / "search.db"
    if not db.exists():
        return out
    con = sqlite3.connect(db)
    for path, kind, tk in con.execute("SELECT path, kind, ticker FROM docs"):
        t = (tk or "").upper()
        if not t:
            m = re.match(r"^([A-Z][A-Z0-9.]{0,9})\\", path)
            t = m.group(1) if m else ""
        if t:
            out.setdefault(t, {}).setdefault(kind, 0)
            out[t][kind] += 1
    con.close()
    return out


def next_catalysts():
    """ticker -> 'YYYY-MM-DD' first upcoming, from _meta/catalysts.md."""
    out = {}
    p = META / "catalysts.md"
    if not p.is_file():
        return out
    m = re.search(r"##\s*📅 Upcoming.*?(?=\n##\s)", read(p), re.S)
    if m:
        _, rows = parse_md_table(m.group(0))
        for cells in rows:
            if len(cells) >= 2 and cells[1] not in out:
                out[cells[1]] = cells[0]
    return out


def main():
    meta = index_meta()
    docs = doc_counts()
    ncat = next_catalysts()
    book = {p["tk"].upper() for p in json.loads((DATA / "book.json").read_text(encoding="utf-8"))
            .get("positions", [])} if (DATA / "book.json").is_file() else set()
    supply = json.loads((DATA / "graph.json").read_text(encoding="utf-8"))
    assum = json.loads((DATA / "assumptions.json").read_text(encoding="utf-8")).get("metrics", {})

    nodes, edges = {}, []

    def add_node(nid, ntype, label, **attrs):
        if nid not in nodes:
            nodes[nid] = {"id": nid, "type": ntype, "label": label, **attrs}
        return nodes[nid]

    # ticker nodes
    page_texts = {}
    for tk, p in company_pages():
        page_texts[tk] = read(p)
        sector, thesis = meta.get(tk, ("", ""))
        dates = [d for d, _ in changelog_entries(page_texts[tk])]
        add_node(tk, "ticker", tk, sector=sector, thesis=thesis[:160],
                 in_book=tk in book, docs=docs.get(tk, {}),
                 next_catalyst=ncat.get(tk, ""), last_chg=max(dates) if dates else "")

    # supply / compete edges (curated)
    for u, d, lbl in supply.get("supplies", []):
        if u in nodes and d in nodes:
            edges.append({"u": u, "v": d, "type": "supplies", "label": lbl})
    for a, b, lbl in supply.get("competes", []):
        if a in nodes and b in nodes:
            edges.append({"u": a, "v": b, "type": "competes", "label": lbl})

    # theme nodes + exposure edges
    for p in sorted((WIKI / "themes").glob("*.md")):
        if p.name.startswith(("_", "00_")):
            continue
        tid = f"theme:{p.stem}"
        txt = read(p)
        m = re.search(r"^#\s+(.+)$", txt, re.M)
        add_node(tid, "theme", p.stem, title=(m.group(1) if m else p.stem)[:120])
        for tk in sorted(set(TICKER_LINK.findall(txt))):
            if tk in nodes:
                edges.append({"u": tid, "v": tk, "type": "exposes", "label": ""})

    # assumption nodes + citation edges
    for mid, m in assum.items():
        aid = f"assum:{mid}"
        add_node(aid, "assumption", mid, title=m["title"][:120],
                 status=m.get("status", ""), canonical=m.get("canonical", "")[:400])
        cited = set()
        for v in m.get("variants", []):
            cited.update(v.get("cited_in", []))
        for rel in sorted(cited):
            tgt = (f"theme:{rel.split('/')[1][:-3]}" if rel.startswith("themes/")
                   else rel[:-3].upper())
            if tgt in nodes:
                edges.append({"u": aid, "v": tgt, "type": "cites", "label": ""})

    # broker coverage edges (>= MIN_MENTIONS attributions on the ticker page)
    for tk, txt in page_texts.items():
        for bid, rx in BROKER_RX.items():
            n = len(rx.findall(txt))
            if n >= MIN_MENTIONS:
                add_node(f"broker:{bid}", "broker", bid)
                edges.append({"u": f"broker:{bid}", "v": tk, "type": "covers", "label": "", "w": n})

    out = {"generated": TODAY.isoformat(),
           "counts": {"nodes": len(nodes), "edges": len(edges)},
           "nodes": list(nodes.values()), "edges": edges}
    (DATA / "graph_full.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                          encoding="utf-8")

    # ---------- self-contained interactive viz ----------
    by_type = {}
    for n in nodes.values():
        by_type[n["type"]] = by_type.get(n["type"], 0) + 1
    payload = json.dumps(out, ensure_ascii=False)
    viz = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Knowledge graph</title>
<style>
body{margin:0;font:14px/1.5 -apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#0f1729;color:#dde4f0;overflow:hidden}
#top{position:fixed;top:0;left:0;right:0;background:#0f1729ee;padding:10px 16px;z-index:5;border-bottom:1px solid #232f4a}
#top h1{display:inline;font-size:16px;margin-right:14px}
#top a{color:#7fb0ff;text-decoration:none;font-size:12px}
.f{display:inline-block;margin:0 4px;padding:2px 10px;border:1px solid #33415e;border-radius:12px;font-size:12px;cursor:pointer;user-select:none}
.f.on{background:#2a3a5f;border-color:#5aa2ff}
#q{background:#1a2440;border:1px solid #33415e;color:#dde4f0;border-radius:6px;padding:4px 10px;font-size:13px;width:180px;margin-left:10px}
#panel{position:fixed;right:0;top:52px;bottom:0;width:360px;background:#131d33;border-left:1px solid #232f4a;padding:14px 16px;overflow-y:auto;display:none;z-index:4}
#panel h2{font-size:15px;margin:0 0 4px;color:#fff} #panel .t{color:#8492ad;font-size:11px;text-transform:uppercase}
#panel p{font-size:12.5px;color:#b9c4d8} #panel li{font-size:12.5px;margin:2px 0}
canvas{display:block}
</style></head><body>
<div id="top"><h1>🕸 Knowledge graph</h1><a href="index.html">← dashboards</a>
<span id="filters"></span><input id="q" placeholder="find node… (Enter)">
<span style="color:#8492ad;font-size:12px;margin-left:10px" id="stats"></span></div>
<div id="panel"></div><canvas id="c"></canvas>
<script>
const G = __PAYLOAD__;
const COL = {ticker:"#5aa2ff", theme:"#e8b54d", assumption:"#ff6b7a", broker:"#3ecf8e"};
const R = {ticker:6, theme:9, assumption:9, broker:5};
let show = {ticker:true, theme:true, assumption:true, broker:false};
const cv = document.getElementById("c"), ctx = cv.getContext("2d");
let W, H; function rs(){W=cv.width=innerWidth; H=cv.height=innerHeight;} rs(); onresize=rs;
const nodes = G.nodes.map(n=>({...n, x:Math.random()*W, y:60+Math.random()*(H-60), vx:0, vy:0}));
const id2n = {}; nodes.forEach(n=>id2n[n.id]=n);
const edges = G.edges.map(e=>({...e, a:id2n[e.u], b:id2n[e.v]})).filter(e=>e.a&&e.b);
const deg = {}; edges.forEach(e=>{deg[e.u]=(deg[e.u]||0)+1; deg[e.v]=(deg[e.v]||0)+1;});
let sel=null, drag=null, panX=0, panY=0, zoom=1;
function vis(n){return show[n.type];}
function tick(){
  const vn = nodes.filter(vis);
  for(const n of vn){n.vx*=.6; n.vy*=.6;}
  for(let i=0;i<vn.length;i++)for(let j=i+1;j<vn.length;j++){
    const a=vn[i],b=vn[j]; let dx=a.x-b.x, dy=a.y-b.y; let d2=dx*dx+dy*dy;
    if(d2<1)d2=1; if(d2<40000){const f=900/d2; const d=Math.sqrt(d2);
      a.vx+=f*dx/d; a.vy+=f*dy/d; b.vx-=f*dx/d; b.vy-=f*dy/d;}}
  for(const e of edges){ if(!vis(e.a)||!vis(e.b))continue;
    const dx=e.b.x-e.a.x, dy=e.b.y-e.a.y, d=Math.sqrt(dx*dx+dy*dy)||1, f=(d-90)*.004;
    e.a.vx+=f*dx; e.a.vy+=f*dy; e.b.vx-=f*dx; e.b.vy-=f*dy;}
  for(const n of vn){ n.vx+=(W/2-n.x)*.0004; n.vy+=(H/2+20-n.y)*.0004;
    if(n!==drag){n.x+=n.vx; n.y+=n.vy;}}
}
function draw(){
  ctx.setTransform(1,0,0,1,0,0); ctx.clearRect(0,0,W,H);
  ctx.setTransform(zoom,0,0,zoom,panX,panY);
  const nb = sel? new Set(edges.filter(e=>e.u===sel.id||e.v===sel.id).flatMap(e=>[e.u,e.v])) : null;
  for(const e of edges){ if(!vis(e.a)||!vis(e.b))continue;
    const hot = sel && (e.u===sel.id||e.v===sel.id);
    ctx.strokeStyle = hot? "#7fb0ff" : (e.type==="competes"? "#ff6b7a33":"#33415e66");
    ctx.lineWidth = hot? 1.6 : .7;
    ctx.beginPath(); ctx.moveTo(e.a.x,e.a.y); ctx.lineTo(e.b.x,e.b.y); ctx.stroke();}
  for(const n of nodes){ if(!vis(n))continue;
    const r = R[n.type] + Math.min(6, (deg[n.id]||0)*.15);
    const dim = sel && n!==sel && !(nb&&nb.has(n.id));
    ctx.globalAlpha = dim? .18 : 1;
    ctx.fillStyle = COL[n.type]; ctx.beginPath(); ctx.arc(n.x,n.y,r,0,7); ctx.fill();
    if(n.in_book){ctx.strokeStyle="#ffd700"; ctx.lineWidth=2; ctx.stroke();}
    if(!dim && (zoom>0.7 || n.type!=="ticker" || (deg[n.id]||0)>8 || n===sel)){
      ctx.fillStyle="#dde4f0"; ctx.font="10px Segoe UI";
      ctx.fillText(n.label, n.x+r+3, n.y+3);}
    ctx.globalAlpha=1;}
}
function loop(){tick(); draw(); requestAnimationFrame(loop);} loop();
function pick(mx,my){ const x=(mx-panX)/zoom, y=(my-panY)/zoom;
  return nodes.filter(vis).find(n=>{const dx=n.x-x,dy=n.y-y;return dx*dx+dy*dy<150;});}
cv.onmousedown=e=>{const n=pick(e.clientX,e.clientY); if(n){drag=n; select(n);} else {drag={pan:true,sx:e.clientX-panX,sy:e.clientY-panY};}};
cv.onmousemove=e=>{ if(!drag)return;
  if(drag.pan){panX=e.clientX-drag.sx; panY=e.clientY-drag.sy;}
  else {drag.x=(e.clientX-panX)/zoom; drag.y=(e.clientY-panY)/zoom;}};
cv.onmouseup=()=>drag=null;
cv.onwheel=e=>{e.preventDefault(); const z=zoom*(e.deltaY<0?1.12:.89);
  panX=e.clientX-(e.clientX-panX)*z/zoom; panY=e.clientY-(e.clientY-panY)*z/zoom; zoom=z;};
function select(n){ sel=n; const p=document.getElementById("panel"); if(!n){p.style.display="none";return;}
  const es = edges.filter(e=>e.u===n.id||e.v===n.id);
  const grp = {};
  es.forEach(e=>{const other=e.u===n.id?e.b:e.a; const dir=e.u===n.id?"→":"←";
    (grp[e.type]=grp[e.type]||[]).push(`${dir} <b>${other.label}</b> <span style="color:#8492ad">${e.label||""}</span>`);});
  let h=`<div class="t">${n.type}${n.in_book?" · 📒 in book":""}</div><h2>${n.label}</h2>`;
  if(n.thesis)h+=`<p>${n.thesis}</p>`; if(n.title)h+=`<p>${n.title}</p>`;
  if(n.canonical)h+=`<p style="color:#e8b54d">${n.canonical}</p>`;
  if(n.sector)h+=`<p class="t">${n.sector}</p>`;
  if(n.next_catalyst)h+=`<p>📅 next catalyst: <b>${n.next_catalyst}</b></p>`;
  if(n.docs&&Object.keys(n.docs).length)h+=`<p>📄 ${Object.entries(n.docs).map(([k,v])=>k+": "+v).join(" · ")}</p>`;
  for(const[t,list]of Object.entries(grp)){h+=`<div class="t" style="margin-top:8px">${t} (${list.length})</div><ul style="margin:2px 0;padding-left:16px">`+list.slice(0,30).map(x=>`<li>${x}</li>`).join("")+"</ul>";}
  p.innerHTML=h; p.style.display="block";}
const fl=document.getElementById("filters");
for(const t of Object.keys(COL)){const s=document.createElement("span");
  s.className="f"+(show[t]?" on":""); s.textContent=t; s.style.borderColor=COL[t];
  s.onclick=()=>{show[t]=!show[t]; s.classList.toggle("on"); if(sel&&!vis(sel))select(null);}; fl.appendChild(s);}
document.getElementById("q").onkeydown=e=>{ if(e.key!=="Enter")return;
  const q=e.target.value.toLowerCase(); const n=nodes.find(n=>vis(n)&&n.label.toLowerCase().includes(q));
  if(n){select(n); panX=W/2-n.x*zoom; panY=H/2-n.y*zoom;}};
document.getElementById("stats").textContent = G.counts.nodes+" nodes · "+G.counts.edges+" edges · "+G.generated;
</script></body></html>"""
    viz = viz.replace("__PAYLOAD__", payload)
    (DASH / "graph.html").write_text(viz, encoding="utf-8")

    print(f"graph: {len(nodes)} nodes ({by_type}), {len(edges)} edges")
    print(f"  -> {DATA/'graph_full.json'}")
    print(f"  -> {DASH/'graph.html'}")


if __name__ == "__main__":
    main()
