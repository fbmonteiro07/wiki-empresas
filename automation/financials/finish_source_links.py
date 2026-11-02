from pathlib import Path
import json
root=Path.cwd()
tickers='JPM SPGI MCO BX KKR GS V MA APO HOOD COIN'.split()
for tk in tickers:
 p=root/'_wiki'/f'{tk}.md';s=p.read_text(encoding='utf-8');s=s.replace(f'../{tk}/SOURCES.md',f'_dashboards/financials-sources.html#{tk}');p.write_text(s,encoding='utf-8')
p=root/'automation/financials/build_inventory.py';s=p.read_text(encoding='utf-8');s=s.replace('[Sources](../../{t}/research/SOURCES.html)','[Sources](../_dashboards/financials-sources.html#{t})')
needle="  x['file_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()"
replacement="  x.setdefault('ingestion_review_status',x.get('analytical_review','not_yet_reviewed'))\n  x['analytical_review']=x['review_status']\n  x['review_scope_recorded']='2026-10-31'\n"+needle
assert s.count(needle)==1;s=s.replace(needle,replacement);p.write_text(s,encoding='utf-8')
print('Updated issuer source links and durable inventory review metadata.')
