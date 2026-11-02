"""Check rendered Financials navigation, source provenance and dated call rows."""
from pathlib import Path
from html.parser import HTMLParser
import json,re

class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag=='a':self.links.append(dict(attrs))

def check(root):
 checks={};issues=[]
 source=json.loads((root/'_wiki/_data/financials/source_inventory.json').read_text(encoding='utf-8-sig'))['records']
 tickers=list(dict.fromkeys(x['ticker'] for x in source))
 rendered=(root/'_wiki/index.html').read_text(encoding='utf-8')
 chunks=dict(re.findall(r'<div class="page" id="p-([^"]+)"[^>]*>(.*?)(?=<div class="page" id="p-|<script>\s*// Search index)',rendered,re.S))
 # The final page has no next page delimiter; Financials and all issuers precede it.
 all_links=[];call_count=0
 for tk in tickers:
  body=chunks.get(tk,'')
  if not body:issues.append('Missing rendered page '+tk);continue
  p=Links();p.feed(body);all_links+=p.links
  if not any(x.get('href')=='_dashboards/financials-sources.html#'+tk for x in p.links):issues.append('Missing source catalog link '+tk)
  for x in p.links:
   href=x.get('href','')
   if re.match(r'\.\./(?:'+('|'.join(tickers))+')/',href) and not x.get('data-public-url'):
    issues.append('Source missing LAN target '+tk+' '+href)
  call=re.search(r'<h3>Source calls</h3>(<table>.*?</table>)',body,re.S)
  if not call:issues.append('Missing source-call table '+tk);continue
  dates=re.findall(r'<tr><td>([^<]*)</td>',call[1]);call_count+=len(dates)
  if any(not re.fullmatch(r'20\d\d-\d\d-\d\d',x) for x in dates):issues.append('Undated source call '+tk)
 checks['all_issuer_catalog_links_and_public_source_targets']=not issues
 checks['dated_source_calls_match_archive']=call_count==sum('transcript' in x['kind'] for x in source)
 th=Links();th.feed(chunks.get('TH-financials',''));hrefs={x.get('href') for x in th.links}
 checks['theme_relative_links_rebased']={'_dashboards/financials-sources.html','_meta/financials-coverage.md'}<=hrefs
 cat=(root/'_wiki/_dashboards/financials-sources.html').read_text(encoding='utf-8');checks['catalog_all_inventory_entries']=cat.count('<tr><td>')==len(source)
 checks['catalog_all_issuer_filters']=all(f'href="#{tk}"' in cat for tk in tickers)
 checks['review_metadata_consistent']=all(x.get('analytical_review')==x['review_status'] for x in source)
 for k,v in checks.items():
  if not v:issues.append('Failed rendered check '+k)
 return checks,issues

if __name__=='__main__':
 checks,issues=check(Path.cwd());print(json.dumps({'checks':checks,'issues':issues},indent=2))
 raise SystemExit(bool(issues))
