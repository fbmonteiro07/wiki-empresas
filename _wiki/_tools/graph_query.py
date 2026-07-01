r"""
Context cards from the knowledge graph (graph_full.json).

Give it a ticker — or any free-text question — and it prints a compact card:
thesis, book membership, supply chain (suppliers/customers/competitors), themes
exposed, the canonical number for every debate the name touches, consensus
snapshot, docs on disk, next catalyst. This is what should sit in front of
every research answer.

    py graph_query.py NVDA                      # card for one node
    py graph_query.py hbm-memory               # theme / assumption card
    py graph_query.py --prompt "vale comprar mais COHR aqui?"   # scan free text
    py graph_query.py --hook                    # UserPromptSubmit hook mode
                                                # (reads {prompt} JSON on stdin)

Rebuild the graph first: py build_graph.py (wired into refresh_features.py).
"""
import sys, json, re
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from _wlib import DATA, load_estimates
sys.stdout.reconfigure(encoding="utf-8")

MAX_TICKER_CARDS = 3
MAX_THEME_CARDS = 2

# common-name aliases -> ticker (case-insensitive, for free-text scanning)
ALIASES = {
    "nvidia": "NVDA", "micron": "MU", "broadcom": "AVGO", "marvell": "MRVL",
    "samsung": "SAMSUNG", "hynix": "SKHYNIX", "sk hynix": "SKHYNIX", "tsmc": "TSM",
    "apple": "AAPL", "google": "GOOG", "alphabet": "GOOG", "microsoft": "MSFT",
    "amazon": "AMZN", "aws": "AMZN", "oracle": "ORCL", "tesla": "TSLA",
    "corning": "GLW", "coherent": "COHR", "lumentum": "LITE", "kioxia": "KIOXIA",
    "sandisk": "SNDK", "seagate": "STX", "vertiv": "VRT", "anthropic": "ANTHROPIC",
    "openai": "OPENAI", "intel": "INTC", "qualcomm": "QCOM", "arista": "ANET",
    "ciena": "CIEN", "cloudflare": "NET", "palantir": "PLTR", "cerebras": "CEREBRAS",
    "salesforce": "CRM", "servicenow": "NOW", "netflix": "NFLX", "spotify": "SPOT",
    "uber": "UBER", "booking": "BKNG", "toyota": "TM", "infineon": "IFX",
    "onsemi": "ON", "wolfspeed": "WOLF", "navitas": "NVTS", "mediatek": "MEDIATEK",
    "spacex": "SPCX", "coreweave": "CRWV", "nebius": "NBIS", "supermicro": "SMCI",
}


def load():
    g = json.loads((DATA / "graph_full.json").read_text(encoding="utf-8"))
    id2n = {n["id"]: n for n in g["nodes"]}
    adj = {}
    for e in g["edges"]:
        adj.setdefault(e["u"], []).append(e)
        adj.setdefault(e["v"], []).append(e)
    return g, id2n, adj


def kw_index(id2n):
    """slug-token -> node id, for free-text matching of themes/assumptions."""
    out = {}
    for nid, n in id2n.items():
        if n["type"] in ("theme", "assumption"):
            for tok in re.split(r"[-_]", n["label"]):
                if len(tok) >= 3 and tok not in ("memory",):   # 'memory' too generic
                    out.setdefault(tok.lower(), set()).add(nid)
    return out


def fmt_n(v, nd=1):
    return "—" if v is None else f"{v:,.{nd}f}"


def cons_line(tk):
    c = (load_estimates().get("companies") or {}).get(tk) or {}
    if not c or "error" in c:
        return ""
    p = (c.get("periods") or {}).get("CY2026") or {}
    p7 = (c.get("periods") or {}).get("CY2027") or {}
    ccy = c.get("ccy", "USD")
    return (f"Consensus (BBG, {ccy}): px {fmt_n(c.get('px'),2)} · CY26 rev {fmt_n(p.get('rev'),0)}m "
            f"eps {fmt_n(p.get('eps'),2)} · CY27 rev {fmt_n(p7.get('rev'),0)}m eps {fmt_n(p7.get('eps'),2)}")


def ticker_card(tk, id2n, adj, lines):
    n = id2n[tk]
    lines.append(f"### {tk} — {n.get('sector','')}".rstrip(" —"))
    if n.get("thesis"):
        lines.append(f"Thesis: {n['thesis']}")
    bits = []
    if n.get("in_book"):
        bits.append("📒 IN BOOK")
    if n.get("next_catalyst"):
        bits.append(f"next catalyst {n['next_catalyst']}")
    if n.get("last_chg"):
        bits.append(f"last changelog {n['last_chg']}")
    if bits:
        lines.append(" · ".join(bits))
    cl = cons_line(tk)
    if cl:
        lines.append(cl)
    sup, cust, comp, themes, assums = [], [], [], [], []
    for e in adj.get(tk, []):
        other = e["v"] if e["u"] == tk else e["u"]
        if e["type"] == "supplies":
            (cust if e["u"] == tk else sup).append(f"{other}({e['label']})")
        elif e["type"] == "competes":
            comp.append(f"{other}({e['label']})")
        elif e["type"] == "exposes":
            themes.append(other.split(":", 1)[1])
        elif e["type"] == "cites":
            assums.append(other)
    if sup:
        lines.append(f"Suppliers ←: {', '.join(sup[:10])}")
    if cust:
        lines.append(f"Customers →: {', '.join(cust[:10])}")
    if comp:
        lines.append(f"Competes ⚔: {', '.join(comp[:6])}")
    if themes:
        lines.append(f"Themes: {', '.join(sorted(themes))}")
    for a in assums[:3]:
        an = id2n[a]
        lines.append(f"Debate [{an['label']}] canonical: {an.get('canonical','')[:220]}")
    d = n.get("docs") or {}
    if d:
        lines.append("Docs on disk: " + " · ".join(f"{k} {v}" for k, v in sorted(d.items())))
    lines.append(f"Page: _wiki/{tk}.md · search: py _wiki/_tools/search.py -t {tk} <query>")
    lines.append("")


def topic_card(nid, id2n, adj, lines):
    n = id2n[nid]
    lines.append(f"### {n['label']} ({n['type']})")
    if n.get("title"):
        lines.append(n["title"])
    if n.get("canonical"):
        lines.append(f"Canonical: {n['canonical'][:400]}")
    tks = sorted(e["v"] if e["u"] == nid else e["u"] for e in adj.get(nid, [])
                 if id2n.get(e["v"] if e["u"] == nid else e["u"], {}).get("type") == "ticker")
    if tks:
        lines.append(f"Exposed tickers: {', '.join(tks)}")
    src = (f"_wiki/themes/{n['label']}.md" if n["type"] == "theme"
           else "_wiki/_meta/assumptions.md")
    lines.append(f"Source: {src}")
    lines.append("")


def scan(text, id2n):
    """Free text -> (tickers, topic node ids)."""
    tickers, topics = [], []
    words = set(re.findall(r"[A-Za-z][\w.]{1,14}", text))
    upper = {w.upper() for w in words}
    for tk in upper:
        if tk in id2n and id2n[tk]["type"] == "ticker" and tk not in tickers:
            tickers.append(tk)
    low = text.lower()
    for alias, tk in ALIASES.items():
        if alias in low and tk in id2n and tk not in tickers:
            tickers.append(tk)
    kws = kw_index(id2n)
    for tok, nids in kws.items():
        if re.search(rf"\b{re.escape(tok)}", low):
            for nid in nids:
                if nid not in topics:
                    topics.append(nid)
    return tickers, topics


def main():
    args = sys.argv[1:]
    g, id2n, adj = load()
    lines = []
    if args and args[0] == "--hook":
        try:
            payload = json.load(sys.stdin)
            text = payload.get("prompt", "")
        except Exception:
            return
        tickers, topics = scan(text, id2n)
        if not tickers and not topics:
            return                      # nothing relevant — inject nothing
        lines.append("[wiki knowledge-graph context — auto-injected, see _wiki/00_INDEX.md]")
        for tk in tickers[:MAX_TICKER_CARDS]:
            ticker_card(tk, id2n, adj, lines)
        for nid in topics[:MAX_THEME_CARDS]:
            topic_card(nid, id2n, adj, lines)
        if len(tickers) > MAX_TICKER_CARDS:
            lines.append(f"(+{len(tickers)-MAX_TICKER_CARDS} more tickers mentioned: "
                         f"{', '.join(tickers[MAX_TICKER_CARDS:])} — cards via graph_query.py)")
        print("\n".join(lines))
        return
    if args and args[0] == "--prompt":
        text = " ".join(args[1:])
        tickers, topics = scan(text, id2n)
        for tk in tickers[:MAX_TICKER_CARDS]:
            ticker_card(tk, id2n, adj, lines)
        for nid in topics[:MAX_THEME_CARDS]:
            topic_card(nid, id2n, adj, lines)
        print("\n".join(lines) if lines else "no graph nodes matched")
        return
    if not args:
        print(__doc__)
        return
    q = args[0]
    if q.upper() in id2n:
        ticker_card(q.upper(), id2n, adj, lines)
    else:
        hits = [nid for nid, n in id2n.items()
                if n["type"] in ("theme", "assumption") and q.lower() in n["label"].lower()]
        if not hits:
            print(f"'{q}' not in graph ({g['counts']['nodes']} nodes)")
            return
        for nid in hits[:3]:
            topic_card(nid, id2n, adj, lines)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
