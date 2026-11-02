"""Targeted regression checks for Financials search integration, using an isolated temporary corpus."""
import importlib.util,json,tempfile,sqlite3,sys
from pathlib import Path
root=Path.cwd();spec=importlib.util.spec_from_file_location('financials_search_test',root/'_wiki/_tools/build_search_index.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory(prefix='financials-search-',dir=root/'_wiki/_data/financials') as temp:
 base=Path(temp).resolve();assert base.is_relative_to((root/'_wiki/_data/financials').resolve())
 m.ROOT=base;m.WIKI=base/'_wiki';m.DATA=m.WIKI/'_data';m.DB=m.DATA/'search.db';m.REBUILD=False
 m.DATA.mkdir(parents=True);t=base/'V';t.mkdir();p=t/'V_10-K_2026-02-01.html';p.write_text('<html><body>Payment network retention test</body></html>',encoding='utf-8')
 m.FILINGS=True;m.main();m.FILINGS=False;m.main()
 c=sqlite3.connect(m.DB);assert c.execute("SELECT count(*) FROM docs WHERE kind='filing'").fetchone()[0]==1;c.close()
 md=m.DATA/'financials';md.mkdir();p2=t/'V_10-Q_2026-05-01.html';p2.write_text('<html><body>Payment incentive manifest test</body></html>',encoding='utf-8');(md/'V_filings.json').write_text(json.dumps({'records':[{'status':'archived','path':'V/V_10-Q_2026-05-01.html','ticker':'V'}]}))
 com=t/'commentary';com.mkdir();(com/'2026-06-01_research.md').write_text('Attributed Visa analyst commentary');ex=com/'_discovery';ex.mkdir();(ex/'invite.md').write_text('Invitation should not be indexed')
 m.main();c=sqlite3.connect(m.DB);assert c.execute("SELECT count(*) FROM docs WHERE kind='filing'").fetchone()[0]==2;assert c.execute("SELECT count(*) FROM docs WHERE kind='briefing' and ticker='V'").fetchone()[0]==1;assert c.execute("SELECT count(*) FROM docs WHERE path LIKE '%_discovery%'").fetchone()[0]==0;c.close()
 p.unlink();m.main();c=sqlite3.connect(m.DB);assert c.execute("SELECT count(*) FROM docs WHERE kind='filing'").fetchone()[0]==1;c.close()
 print('PASS: default refresh retains optional filings, adds manifest filings and commentary, excludes discovery leads, and purges deleted files.')
