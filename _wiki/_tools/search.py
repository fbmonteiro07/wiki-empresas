r"""
Query the full-corpus search index (built by build_search_index.py).

    py "E:/Wiki Felipe empresas/_wiki/_tools/search.py" CPO connector attach rate
    py ..../search.py -k call,transcript HBM4 pricing     # restrict to kinds
    py ..../search.py -t NVDA -n 30 Rubin racks           # restrict to a ticker, 30 hits
    py ..../search.py "\"token maxxing\""                 # exact phrase (quote it)

Kinds: wiki, theme, call, briefing, stratechery, report, transcript, filing.
FTS5 syntax works in the query (AND/OR/NEAR, prefix*, "phrases").
"""
import sys, sqlite3
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _wlib import DATA
sys.stdout.reconfigure(encoding="utf-8")

DB = DATA / "search.db"


def main():
    args = sys.argv[1:]
    kinds, ticker, limit, terms = None, None, 15, []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "-k":
            kinds = [k.strip() for k in args[i + 1].split(",")]; i += 2
        elif a == "-t":
            ticker = args[i + 1].upper(); i += 2
        elif a == "-n":
            limit = int(args[i + 1]); i += 2
        else:
            terms.append(a); i += 1
    if not terms:
        print(__doc__); return
    if not DB.exists():
        print("no index — run build_search_index.py first"); return
    q = " ".join(terms)
    con = sqlite3.connect(DB)
    sql = ("SELECT path, kind, ticker, date, title, "
           "snippet(docs, 5, '[', ']', ' … ', 18) AS snip, bm25(docs) AS rank "
           "FROM docs WHERE docs MATCH ?")
    params = [q]
    if kinds:
        sql += f" AND kind IN ({','.join('?' * len(kinds))})"
        params += kinds
    if ticker:
        sql += " AND ticker = ?"
        params.append(ticker)
    sql += " ORDER BY rank LIMIT ?"
    params.append(limit)
    try:
        rows = con.execute(sql, params).fetchall()
    except sqlite3.OperationalError as e:
        print(f"query error: {e}\n(quote phrases, escape special chars)"); return
    if not rows:
        print("no hits"); return
    for path, kind, tk, date, title, snip, rank in rows:
        tag = f"{kind}" + (f"/{tk}" if tk else "") + (f" {date}" if date else "")
        snip = " ".join(snip.split())
        print(f"\n[{tag}]  {path}")
        print(f"  {snip[:400]}")
    print(f"\n{len(rows)} hits (of max {limit}) for: {q}")
    con.close()


if __name__ == "__main__":
    main()
