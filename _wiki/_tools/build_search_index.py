r"""
FEATURE 8 — Full-corpus search index (SQLite FTS5).

The offline wiki search only covers the ~120 synthesized pages. The raw corpus
— 300+ ingested reports (relatórios bons), equity calls, briefings, earnings
transcripts, Stratechery — is only reachable if a page happened to cite it.
This indexes ALL of it into one FTS5 database so "everything anyone said about
CPO connector attach rates" returns primary-source hits.

Incremental: unchanged files (same mtime+size) are skipped, so daily re-runs
after an ingest are fast. SEC filings are opt-in (--filings) — they are big,
boilerplate-heavy, and triple the index size.

    py "E:/Wiki Felipe empresas/_wiki/_tools/build_search_index.py"            # build/update
    py "E:/Wiki Felipe empresas/_wiki/_tools/build_search_index.py --filings"  # also index SEC filings
    py "E:/Wiki Felipe empresas/_wiki/_tools/build_search_index.py --rebuild"  # from scratch

Query it with search.py. DB: _wiki/_data/search.db (gitignored).
"""
import sys, re, sqlite3, html as ihtml
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _wlib import WIKI, DATA
sys.stdout.reconfigure(encoding="utf-8")

ROOT = WIKI.parent
DB = DATA / "search.db"
REBUILD = "--rebuild" in sys.argv
FILINGS = "--filings" in sys.argv

DATE_RE = re.compile(r"(20\d\d)[-_]?(\d\d)[-_]?(\d\d)")
TAG_RE = re.compile(r"<[^>]+>")
SCRIPT_RE = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
WS_RE = re.compile(r"[ \t]+")

# Non-ticker top-level dirs to skip when walking ticker folders
NOT_TICKERS = {"_briefings", "_equity_calls", "_inbox", "_wiki", ".claude", ".git",
               "Modelos oficiais", "relatórios bons", "Stratechery"}


def strip_html(txt):
    txt = SCRIPT_RE.sub(" ", txt)
    txt = TAG_RE.sub(" ", txt)
    txt = ihtml.unescape(txt)
    return WS_RE.sub(" ", txt)


def fdate(name):
    m = DATE_RE.search(name)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""


def corpus():
    """Yield (path, kind, ticker) for every indexable file."""
    for p in WIKI.glob("*.md"):
        if not p.name.startswith(("_", "00_")):
            yield p, "wiki", p.stem
    for p in (WIKI / "themes").glob("*.md"):
        if not p.name.startswith(("_", "00_")):
            yield p, "theme", ""
    for p in (ROOT / "_equity_calls").rglob("*.md"):
        yield p, "call", ""
    for p in (ROOT / "_briefings").rglob("*.md"):
        yield p, "briefing", (p.stem.upper() if p.parent.name == "by-ticker" else "")
    for p in (ROOT / "Stratechery").glob("*.md"):
        yield p, "stratechery", ""
    for p in (ROOT / "relatórios bons").glob("*.html"):
        yield p, "report", ""
    for d in ROOT.iterdir():
        if not d.is_dir() or d.name in NOT_TICKERS or d.name.startswith("."):
            continue
        tdir = d / "transcripts"
        if tdir.is_dir():
            for p in tdir.glob("*.md"):
                yield p, "transcript", d.name
        if FILINGS:
            for p in d.glob("*.html"):
                yield p, "filing", d.name


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    if REBUILD and DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript("""
      CREATE TABLE IF NOT EXISTS meta(path TEXT PRIMARY KEY, mtime REAL, size INTEGER);
      CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts5(
        path UNINDEXED, kind UNINDEXED, ticker UNINDEXED, date UNINDEXED,
        title, body, tokenize='unicode61 remove_diacritics 2');
    """)
    seen, added, skipped = set(), 0, 0
    for p, kind, ticker in corpus():
        rel = str(p.relative_to(ROOT))
        seen.add(rel)
        try:
            st = p.stat()
        except OSError:
            continue
        row = con.execute("SELECT mtime, size FROM meta WHERE path=?", (rel,)).fetchone()
        if row and row[0] == st.st_mtime and row[1] == st.st_size:
            skipped += 1
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if p.suffix.lower() == ".html":
            txt = strip_html(txt)
        title = p.stem.replace("_", " ")
        con.execute("DELETE FROM docs WHERE path=?", (rel,))
        con.execute("INSERT INTO docs(path,kind,ticker,date,title,body) VALUES(?,?,?,?,?,?)",
                    (rel, kind, ticker, fdate(p.name), title, txt))
        con.execute("INSERT OR REPLACE INTO meta(path,mtime,size) VALUES(?,?,?)",
                    (rel, st.st_mtime, st.st_size))
        added += 1
    # purge deleted files
    gone = [r[0] for r in con.execute("SELECT path FROM meta").fetchall() if r[0] not in seen]
    for rel in gone:
        con.execute("DELETE FROM docs WHERE path=?", (rel,))
        con.execute("DELETE FROM meta WHERE path=?", (rel,))
    con.commit()
    n = con.execute("SELECT count(*) FROM meta").fetchone()[0]
    con.execute("INSERT INTO docs(docs) VALUES('optimize')")
    con.commit()
    con.close()
    mb = DB.stat().st_size / 1e6
    print(f"search index: {n} docs ({added} added/updated, {skipped} unchanged, {len(gone)} removed) "
          f"· {mb:.0f} MB -> {DB}")


if __name__ == "__main__":
    main()
