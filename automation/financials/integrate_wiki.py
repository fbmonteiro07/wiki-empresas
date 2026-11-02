from pathlib import Path
import json
r=Path.cwd()
p=r/'_wiki/_tools/build_search_index.py';s=p.read_text(encoding='utf-8-sig')
s=s.replace('import sys, re, sqlite3, html as ihtml','import sys, re, sqlite3, json, html as ihtml')
s=s.replace('SEC filings are opt-in (--filings) — they are big,','SEC filings are opt-in (--filings), except the explicit Financials source manifests — they are big,')
anchor='    for d in ROOT.iterdir():\n'
addition='''    # Explicit research-universe filings stay searchable on normal nightly refreshes.
    # The manifests carry issuer/form/date/provenance; do not infer filings from arbitrary HTML.
    manifest_filings = set()
    for manifest in (DATA / "financials").glob("*_filings.json"):
        obj = json.loads(manifest.read_text(encoding="utf-8-sig"))
        for row in obj.get("records", []):
            if row.get("status") != "archived":
                continue
            p = ROOT / row["path"]
            if p.is_file() and p.resolve().is_relative_to(ROOT.resolve()):
                manifest_filings.add(p)
                yield p, "filing", row["ticker"]
'''
assert anchor in s;s=s.replace(anchor,addition+anchor,1)
old='''        if FILINGS:
            for p in d.glob("*.html"):
                yield p, "filing", d.name
'''
new='''        # Direct children only: _discovery contains invitations and false-positive leads.
        for dirname, pattern, kind in (("commentary", "*.md", "briefing"),
                                       ("earnings", "*.txt", "earnings"),
                                       ("research", "*.md", "report")):
            for p in (d / dirname).glob(pattern):
                if p.name != "SOURCES.md":
                    yield p, kind, d.name
        if FILINGS:
            for p in d.glob("*.html"):
                if p not in manifest_filings:
                    yield p, "filing", d.name
'''
assert old in s;s=s.replace(old,new,1)
s=s.replace('        if p.suffix.lower() == ".html":','        if p.suffix.lower() in {".html", ".htm"}:')
old='''    gone = [r[0] for r in con.execute("SELECT path FROM meta").fetchall() if r[0] not in seen]
'''
new='''    # A default refresh must not silently discard filings added with --filings.
    retained_filings = set()
    if not FILINGS:
        retained_filings = {r[0] for r in con.execute("SELECT path FROM docs WHERE kind='filing'")
                            if (ROOT / r[0]).is_file()}
    gone = [r[0] for r in con.execute("SELECT path FROM meta").fetchall()
            if r[0] not in seen and r[0] not in retained_filings]
'''
assert old in s;s=s.replace(old,new,1);p.write_text(s,encoding='utf-8')
p=r/'_wiki/_tools/graph_query.py';s=p.read_text(encoding='utf-8-sig');anchor='    "spacex": "SPCX", "coreweave": "CRWV", "nebius": "NBIS", "supermicro": "SMCI",\n'
assert anchor in s;s=s.replace(anchor,anchor+'    "jpmorgan chase": "JPM", "j.p. morgan chase": "JPM", "s&p global": "SPGI",\n    "moody\'s": "MCO", "moodys": "MCO", "blackstone": "BX", "goldman sachs": "GS",\n    "visa": "V", "mastercard": "MA", "apollo": "APO", "robinhood": "HOOD", "coinbase": "COIN",\n',1);p.write_text(s,encoding='utf-8')
p=r/'_wiki/_tools/build_graph.py';s=p.read_text(encoding='utf-8-sig');anchor='        for bid, rx in BROKER_RX.items():\n';assert anchor in s;s=s.replace(anchor,anchor+'            # JPM and GS are now covered issuers as well as research shops.\n            if bid == tk and bid in {"JPM", "GS"}:\n                continue\n',1);p.write_text(s,encoding='utf-8')
p=r/'_wiki/_data/index_meta.json';j=json.loads(p.read_text(encoding='utf-8-sig'));assert not any(x['title']=='Financials' for x in j['sections'])
theses={
'JPM':'Diversified banking scale; debate is sustainable NII and capital-markets earnings versus expenses, credit and capital requirements.',
'SPGI':'Ratings, indices and financial data; issuance and AI monetization versus portfolio changes and workflow substitution.',
'MCO':'Ratings franchise plus analytics subscriptions; issuance mix and recurring growth versus credit-cycle sensitivity.',
'BX':'Alternative asset-management scale; fee activation and realizations versus private-wealth liquidity and valuation risk.',
'KKR':'Asset management, insurance and strategic holdings; fee-base growth versus earnings comparability and balance-sheet exposure.',
'GS':'Capital-markets and wealth franchise; advisory recovery and durable fees versus trading cyclicality and expenses.',
'V':'Global payment network; value-added services and new flows versus client incentives and alternative payment rails.',
'MA':'Payment network and services; cross-border activity and service attachment versus incentives and regulatory pressure.',
'APO':'Origination, asset management and Athene; capital formation and spread earnings versus credit, liquidity and funding risk.',
'HOOD':'Retail financial platform; wallet share and new products versus trading dependence, incentives and credit costs.',
'COIN':'Crypto infrastructure and distribution; diversified usage and stablecoins versus transaction cyclicality and investment marks.'}
j['sections'].append({'title':'Financials','entries':[{'ticker':t,'display':t,'thesis':v} for t,v in theses.items()]});p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=r/'_wiki/_data/graph.json';j=json.loads(p.read_text(encoding='utf-8-sig'))
for a,b,label in [('V','MA','Payment networks; FY/Q3 company calls Oct 27/29 2026'),('SPGI','MCO','Ratings and financial information; company calls Oct 27/21 2026'),('BX','KKR','Alternative asset management; company calls Oct 22 / Jul 30 2026'),('BX','APO','Alternative asset management; company calls Oct 22 / Aug 4 2026'),('KKR','APO','Asset management and insurance; company calls Jul 30 / Aug 4 2026'),('HOOD','COIN','Retail crypto distribution; company calls Oct 27/29 2026'),('JPM','GS','Investment banking and markets; company calls Oct 13 2026')]:
 if not any({x[0],x[1]}=={a,b} for x in j['competes']):j['competes'].append([a,b,label])
p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Updated search, aliases, graph broker handling, Financials metadata and competition edges.')
