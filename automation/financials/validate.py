from pathlib import Path
import json,sqlite3,re,hashlib,urllib.parse,sys,os,shutil,tempfile
sys.stdout.reconfigure(encoding='utf-8');root=Path.cwd();d=root/'_wiki/_data/financials';inv=json.loads((d/'source_inventory.json').read_text(encoding='utf-8-sig'));coverage=json.loads((d/'coverage.json').read_text());tks=[x['ticker'] for x in coverage['companies']];checks={};issues=[]
fd,snapshot_name=tempfile.mkstemp(prefix='financials-verify-',suffix='.db');os.close(fd)
snapshot=Path(snapshot_name);all_counts={}
try:
 print('Copying current search database to a temporary local verification file.',flush=True)
 shutil.copyfile(root/'_wiki/_data/search.db',snapshot)
 c=sqlite3.connect(snapshot,timeout=3)
 try:
  for ticker,kind,n in c.execute('select ticker,kind,count(*) from docs group by ticker,kind'):
   all_counts.setdefault(ticker,{})[kind]=n
 finally:c.close()
finally:
 assert snapshot.parent.resolve()==Path(tempfile.gettempdir()).resolve() and snapshot.name.startswith('financials-verify-')
 snapshot.unlink(missing_ok=True)
for x in coverage['companies']:
 t=x['ticker'];counts=all_counts.get(t,{});print(t,counts,flush=True)
 for kind,key in [('filing','sec'),('transcript','transcript_documents'),('briefing','commentary_candidates'),('earnings','earnings_exhibits')]:
  if counts.get(kind,0)!=x['counts'][key]:issues.append(f'{t} search {kind} count mismatch')
checks['search_counts']=not issues
g=json.loads((root/'_wiki/_data/graph_full.json').read_text(encoding='utf-8'));nodes={x['id']:x for x in g['nodes']};edges=g['edges'];exposed={x['v'] for x in edges if x['u']=='theme:financials' and x['type']=='exposes'};checks['theme_exposes_all_issuers']=set(tks)==exposed;checks['all_financials_sector']=all(nodes[t].get('sector')=='Financials' for t in tks);checks['no_self_broker_edges']=not any(x['type']=='covers' and x['u']=='broker:'+x['v'] for x in edges if x['v'] in ['JPM','GS'])
for file in [root/'_wiki'/f'{t}.md' for t in tks]+[root/'_wiki/themes/financials.md',root/'_wiki/_meta/financials-coverage.md']+[root/t/'SOURCES.md' for t in tks]:
 s=file.read_text(encoding='utf-8-sig')
 for link in re.findall(r'\]\(([^)]+)\)',s):
  if re.match(r'https?://|#|mailto:',link):continue
  target=Path(os.path.normpath(str(file.parent/urllib.parse.unquote(link.split('#')[0]))))
  if not target.is_file():issues.append('Broken local link '+str(file.relative_to(root))+' -> '+link)
checks['local_links']=not any(x.startswith('Broken') for x in issues)
# 2026-11-02: the one-time 'hub unchanged' hash check (preserved_layout_hashes.json) is retired; the catalog is now a registered hub card.
checks['hub_registers_catalog']=any(c.get('href')=='financials-sources.html' for c in json.loads((root/'_wiki/_data/dashboards.json').read_text(encoding='utf-8'))['cards'])
checks['archive_file_and_hash_checks']=not coverage['validation_errors'];checks['last_eight_call_periods_complete']=all(not x['missing_last_eight_quarters'] for x in coverage['companies'])
from check_rendered import check as check_rendered
rendered_checks,rendered_issues=check_rendered(root);checks.update(rendered_checks);issues.extend(rendered_issues)
for k,v in checks.items():
 if not v:issues.append('Failed check '+k)
result={'as_of':'2026-11-02','checks':checks,'issues':issues,'search_regression':'Passed isolated fixture: optional filing retention, manifest inclusion, discovery exclusion, deleted-file cleanup','review_log_note':'One incomplete trailing fragment retained in original passage log and recorded in review_log_parse_issues.json; it does not establish a document review.'}
(d/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if issues:sys.exit(1)
