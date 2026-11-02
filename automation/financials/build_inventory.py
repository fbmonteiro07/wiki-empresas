"""Rebuild Financials source inventories from manifests. No financial estimates are calculated."""
import collections,hashlib,html,json,os,re,sys,urllib.parse
from pathlib import Path
from collect_sources import ROOT,DATA,CO,write_json
sys.stdout.reconfigure(encoding='utf-8')
def readj(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def rows(p):return readj(p).get('records',[]) if p.exists() else []
def norm(p):return str(p).replace('\\','/')
log=[]; log_issues=[]
for line_no, line in enumerate((DATA/'review_passages.jsonl').read_text(encoding='utf-8-sig').split('\n'), 1):
    if not line.strip(): continue
    try: log.append(json.loads(line))
    except json.JSONDecodeError as exc: log_issues.append({'line':line_no,'raw':line,'error':str(exc)})
write_json(DATA/'review_log_parse_issues.json',{'issues':log_issues,'policy':'Original log retained; incomplete fragments do not establish source review.'})
reviewed=set()
for x in log:
 p=norm(x['path']);reviewed.add(p)
 if '/filings_text/' in p:reviewed.add(p.replace('/filings_text/','/').removesuffix('.txt')+'.html')
 if '/earnings/' in p and p.endswith('.txt'):reviewed.add(p[:-4]+'.htm')
commentary=rows(DATA/'commentary_manifest.json');live=rows(DATA/'live_email_manifest.json');ir=rows(DATA/'ir_transcripts.json');summary=[];errors=[];all_records=[]
for tk,(name,exchange) in CO.items():
 page=(ROOT/'_wiki'/f'{tk}.md').read_text(encoding='utf-8-sig')
 records=[]
 for manifest,kind in [(f'{tk}_filings.json','SEC filing'),(f'{tk}_predecessor_filings.json','Predecessor SEC filing'),(f'{tk}_transcripts.json','Third-party call transcript'),(f'{tk}_supplemental_transcripts.json','Third-party call transcript'),(f'{tk}_earnings.json','Earnings release / supplement')]:
  for x in rows(DATA/manifest):
   if x.get('status')!='archived':continue
   records.append(dict(x,kind=kind))
 for x in ir:
  if x.get('ticker')==tk and x.get('status')=='archived':records.append(dict(x,kind='Company-hosted '+x.get('material_type','call transcript'),original_path=x['path'],path=x['text_path'],hash_path=x['path']))
 for x in commentary:
  if x['ticker']==tk and x.get('selection_status')!='excluded_from_core':records.append(dict(x,kind='Cached commentary',status='archived'))
 for x in live:
  if x['ticker']==tk:records.append(dict(x,kind='Outlook research email',status='archived'))
 for p in (ROOT/tk/'research').glob('*.md'):
  if p.name=='SOURCES.md':continue
  s=p.read_text(encoding='utf-8-sig');dm=re.search(r'(?:Report date|Publication date|Event and publication date): (20\d\d-\d\d-\d\d)',s);url=re.search(r'Original URL: (https?://\S+)',s)
  records.append(dict(ticker=tk,kind='Research / company announcement',path=p.relative_to(ROOT).as_posix(),date=dm[1] if dm else '',source_url=url[1] if url else '',title=s.splitlines()[0].lstrip('# '),status='archived',quality='Full local source extraction'))
 for x in records:
  p=ROOT/x['path']
  if not p.is_file():errors.append('Missing '+x['path']);continue
  x['date']=x.get('filing_date') or x.get('date') or x.get('call_date') or ''
  x['title']=x.get('title') or x.get('subject') or (' '.join([x.get('form',''),x.get('fiscal_period','')]).strip()) or p.stem
  x['review_status']='Cited in synthesis; selected passages' if x['path'] in page else 'Selected passage emitted for review' if x['path'] in reviewed else 'Archived; no substantive review claimed'
  x.setdefault('ingestion_review_status',x.get('analytical_review','not_yet_reviewed'))
  x['analytical_review']=x['review_status']
  x['review_scope_recorded']='2026-11-01'
  x['file_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
  if x.get('sha256') and x['kind']!='Cached commentary':
   hp=ROOT/x.get('hash_path',x['path']);actual=x['file_sha256'] if hp==p else hashlib.sha256(hp.read_bytes()).hexdigest()
   if actual!=x['sha256']:
    normalized=hashlib.sha256(hp.read_text(encoding='utf-8').encode('utf-8')).hexdigest() if x['kind']=='Third-party call transcript' else None
    if normalized==x['sha256']:x['original_hash_basis']='UTF-8 text with LF line endings; file_sha256 records actual Windows bytes'
    else:errors.append('Hash mismatch '+str(hp.relative_to(ROOT)))
  x['fidelity']=x.get('quality_note') or x.get('quality') or ('Official SEC source' if 'SEC filing' in x['kind'] or x['kind'].startswith('Earnings') else 'Company-hosted PDF extraction; consult original for tables' if x['kind'].startswith('Company-hosted') else 'Third-party transcription; consult company releases for reported figures')
 sec=[x for x in records if 'SEC filing' in x['kind']];calls=[x for x in records if 'transcript' in x['kind']];releases=[x for x in records if x['kind'].startswith('Earnings')];com=[x for x in records if x['kind'] in {'Cached commentary','Outlook research email'}];periods=sorted(set(x.get('fiscal_period','').replace('FY','') for x in calls))
 for x in sec:
  if x['form'] not in {'10-K','10-Q','10-K/A','10-Q/A'}:errors.append('Invalid filing '+x['path'])
  if not '2021-10-31'<=x['date']<='2026-10-31':errors.append('Outside window '+x['path'])
 q=sorted([x for x in sec if x['form']=='10-Q'],key=lambda x:x['date'])[-1];k=sorted([x for x in sec if x['form']=='10-K'],key=lambda x:x['date'])[-1]
 unique_periods=[p for p in periods if p]
 latest=max((int(p.split()[-1])*4+int(p[1]) for p in unique_periods),default=0)
 expected={f'Q{(i-1)%4+1} {(i-1)//4}' for i in range(latest-7,latest+1)}
 missing=sorted(expected-set(unique_periods));
 if missing:errors.append(tk+' missing recent quarters '+str(missing))
 counts=dict(sec=len(sec),transcript_documents=len(calls),unique_quarter_calls=len(unique_periods),earnings_exhibits=len(releases),commentary_candidates=len(com),commentary_unique_source_ids=len(set(x['source_id'] for x in com)),research_sources=sum(x['kind']=='Research / company announcement' for x in records))
 item=dict(ticker=tk,name=name,counts=counts,latest_10q_date=q['date'],latest_10q_period=q['period_end'],latest_10k_date=k['date'],latest_10k_period=k['period_end'],call_periods=unique_periods,missing_last_eight_quarters=missing,cited_sources=sum(x['review_status'].startswith('Cited') for x in records));summary.append(item)
 notes=[f'Filings/results cut-off: 2026-10-31. Live email review: 2026-11-01. {counts["sec"]} SEC filings; {counts["transcript_documents"]} transcript documents covering {counts["unique_quarter_calls"]} distinct quarterly calls; {counts["earnings_exhibits"]} earnings exhibits; {counts["commentary_candidates"]} commentary documents (cached and live-retrieved versions).',
 'SEC scope: all located 10-K/10-Q filings and amendments filed 2021-10-31 through 2026-10-31. Recent-call target: latest eight reported quarters; broader company-hosted history retained when available. Publication dates and fiscal periods are distinct.',
 'Archived does not mean fully read. Review status distinguishes citations/selected excerpts from historical material collected for future research. The extraction log records passages emitted, and is not proof of complete-document reading.',
 'Cached commentary bodies were capped at 9,000 characters in the original email collection. Selected live Outlook messages retrieved on November 1 preserve the connector-returned body; linked reports are not automatically included. Subject relevance screening does not establish that every candidate contains a substantive issuer opinion. Invitations and false matches remain in commentary/_discovery and are excluded from these counts.',
 'Bloomberg consensus is unavailable in the existing cache for this issuer; the local terminal connection did not respond. No current valuation or consensus estimates were manufactured.']
 if tk=='APO':notes.append('Two predecessor filings are separately labeled: pre-combination Apollo is not the combined Apollo/Athene group. Company-hosted transcripts cover Q1 2022 through Q2 2026. Q3 2026 is scheduled for November 3, after this cut-off.')
 if tk=='KKR':notes.append('Q4 2025 call date corrected from the third-party URL date to February 5, 2026 using the company transcript. Q3 2026 is scheduled for November 9, after the cut-off.')
 if tk=='COIN':notes.append('Q3 2026 has a company prepared presentation plus a separately archived public Q&A. A guessed company Q&A PDF URL returned 404; the failure is retained in the manifest.')
 if tk=='JPM':notes.append('The Q3 2026 company PDF carries a stray FEBRUARY 2026 cover label, but explicitly dates the call October 13, 2026 and contains the Q3 results. The source is preserved without silently editing it.')
 if tk=='BX':notes.append('An old MarketBeat November 22, 2024 discovery link served no transcript; it is a failed lead, not one of the eight completed recent quarters.')
 if tk=='HOOD':notes.append('The February 20, 2026 10-K/A is an amendment retained alongside the original; its stated correction concerns formatting, not a revision to the financial results.')
 if tk=='V':notes.append('Visa reports on a September fiscal year-end. FY2026 Q4 earnings are available, while the latest 10-K filed by the cut-off is FY2025.')
 def href(path,base):return urllib.parse.quote(Path(os.path.relpath(ROOT/path,base)).as_posix(),safe='/._-')
 def esc(v):return str(v).replace('|',' / ').replace('\n',' ')
 md=[f'# {tk} — {name}: source inventory','']+['- '+n for n in notes]+['',f'[Wiki synthesis](../_wiki/{tk}.md) · [Financials overview](../_wiki/themes/financials.md) · [Readable browser inventory](research/SOURCES.html)','','| Date | Kind / period | Local source | Publisher / original | Review scope |','|---|---|---|---|---|']
 hs=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+html.escape(tk+' source inventory')+'</title><style>body{font:15px/1.5 system-ui,sans-serif;max-width:1200px;margin:36px auto;padding:0 20px;color:#182b3d;background:#f8fafc}a{color:#1665a6}table{border-collapse:collapse;width:100%;font-size:13px}th,td{padding:9px;border-bottom:1px solid #dbe2e8;text-align:left;vertical-align:top}th{background:#eaf0f5;position:sticky;top:0}p{max-width:95ch}.muted{color:#526474}h2{margin-top:30px}</style><h1>'+html.escape(tk+' — '+name)+'</h1><p><a href="../../_wiki/index.html#'+tk+'">Wiki synthesis</a> · <a href="../../_wiki/index.html#TH-financials">Financials overview</a> · <a href="../SOURCES.md">Markdown inventory</a></p>']
 hs+=['<p class="muted">'+html.escape(n)+'</p>' for n in notes];hs+=['<table><thead><tr><th>Date</th><th>Type / period</th><th>Source</th><th>Provenance / fidelity</th><th>Review scope</th></tr></thead><tbody>']
 for x in sorted(records,key=lambda x:(x['date'],x['kind'],x['path']),reverse=True):
  kind=x['kind']+(' · '+x['fiscal_period'] if x.get('fiscal_period') else '')+(' · period '+x['period_end'] if x.get('period_end') else '')
  pub=x.get('sender') or ('SEC EDGAR' if 'SEC' in x['kind'] or x['kind'].startswith('Earnings') else 'Company IR' if x['kind'].startswith('Company') else x.get('source_url','').split('/')[2] if x.get('source_url') else 'Local research archive')
  original=f'[{esc(pub)}]({x["source_url"]})' if x.get('source_url') else esc(pub)
  md.append(f'| {x["date"]} | {esc(kind)} | [{esc(x["title"])}]({href(x["path"],ROOT/tk)}) | {original} | {x["review_status"]} |')
  src='<a href="'+html.escape(href(x['path'],ROOT/tk/'research'))+'">'+html.escape(x['title'])+'</a>'
  if x.get('original_path'):src+=' · <a href="'+html.escape(href(x['original_path'],ROOT/tk/'research'))+'">original PDF</a>'
  prov=('<a href="'+html.escape(x['source_url'])+'">'+html.escape(pub)+'</a>') if x.get('source_url') else html.escape(pub)
  hs.append('<tr><td>'+html.escape(x['date'])+'</td><td>'+html.escape(kind)+'</td><td>'+src+'</td><td>'+prov+'<br>'+html.escape(x['fidelity'])+'</td><td>'+html.escape(x['review_status'])+'</td></tr>')
 hs.append('</tbody></table><p>Counts and hashes: local ingestion manifests, recorded 2026-11-01. Duplicate source copies do not represent additional quarterly calls.</p></html>')
 (ROOT/tk/'SOURCES.md').write_text('\n'.join(md)+'\n',encoding='utf-8');(ROOT/tk/'research').mkdir(exist_ok=True);(ROOT/tk/'research/SOURCES.html').write_text('\n'.join(hs),encoding='utf-8')
 all_records.extend(records)
totals={key:sum(x['counts'][key] for x in summary) for key in summary[0]['counts']};totals['unique_commentary_emails']=len({x['source_id'] for x in all_records if x['kind'] in {'Cached commentary','Outlook research email'}})
write_json(DATA/'coverage.json',{'as_of':'2026-11-01','filing_window':['2021-10-31','2026-10-31'],'review_scope':'Selected-source synthesis, not a complete-page reading audit','totals':totals,'companies':summary,'validation_errors':errors})
write_json(DATA/'source_inventory.json',{'as_of':'2026-11-01','records':all_records})
ledger=['# Financials — source coverage and remaining gaps','','_Recorded 2026-11-01. Derived from local ingestion manifests and file/hash checks; not a claim that all archived pages were read._','',f'**Archive totals:** {totals["sec"]} SEC filings; {totals["transcript_documents"]} transcript documents covering {totals["unique_quarter_calls"]} distinct issuer-quarter calls; {totals["earnings_exhibits"]} earnings exhibits; {totals["commentary_candidates"]} company-commentary entries from {totals["unique_commentary_emails"]} distinct emails. Cached/live versions and cross-company copies can appear as separate documents; identities are deduplicated for the email count.','', '[Financials overview](../themes/financials.md) · [Machine-readable coverage](../_data/financials/coverage.json) · [Complete source/provenance ledger](../_data/financials/source_inventory.json)','','| Ticker | SEC | Transcript documents / distinct quarters | Earnings exhibits | Commentary candidates | Latest 10-Q period / filing | Inventory |','|---|---:|---:|---:|---:|---|---|']
for x in summary:
 c=x['counts'];t=x['ticker'];ledger.append(f'| [{t}](../{t}.md) | {c["sec"]} | {c["transcript_documents"]} / {c["unique_quarter_calls"]} | {c["earnings_exhibits"]} | {c["commentary_candidates"]} | {x["latest_10q_period"]} / {x["latest_10q_date"]} | [Sources](../_dashboards/financials-sources.html#{t}) |')
ledger+=['','## What the counts mean','','- SEC: original 10-K, 10-Q and amendments filed within 2021-10-31–2026-10-31, including two separately identified Apollo predecessor filings. Source dates, fiscal periods, accessions, original URLs and hashes are preserved.','- Calls: at least the latest eight reported quarters per issuer; duplicate company/third-party copies and Coinbase prepared remarks are counted as documents but not extra quarters. Apollo has company-hosted history back to Q1 2022.','- Earnings: SEC-filed 2026 releases and supplements; multiple exhibits can belong to one result.','- Commentary: subject-screened cached candidates plus 33 selected live Outlook messages reviewed on 2026-11-01 (36 company-specific copies). The old collection truncated long bodies. The live collection preserves the connector-returned body, but neither guarantees the linked report was obtained. False matches and invitations are preserved under _discovery and excluded. This was a targeted 2026 year-to-date search; pagination remains available for broader historical review.','- Reviewed: the synthesis uses the latest result, selected guidance/Q&A, historical management context, relevant filing disclosures and identified sell-side commentary. Cited/selected-passage status is recorded separately from mere availability. [Passage-emission log](../_data/financials/review_passages.jsonl) is a navigation aid, not proof of full-document review.','','## Live email review audit\n\n[Queries, selection and pagination](../_data/financials/email_review_2026-11-01/search_audit.json) and [live source manifest](../_data/financials/live_email_manifest.json) preserve the audit trail. Canonical matches to older cached messages use sender, normalized subject and received date within one day; report dates and received UTC timestamps are separate. Goldman HOOD/COIN result alerts remain headline-only. The Redburn prediction-market volume conflict is flagged rather than adopted.\n\n## Open items','','- Bloomberg consensus/valuation: none of these issuers is in the current estimates cache. A local-terminal connection attempt timed out; no server fallback or invented estimates used.','- Q3 releases for APO (November 3) and KKR (November 9) were future events at the cut-off.','- JPM, GS and BX have Q3 earnings releases but only Q2 10-Qs filed by this cut-off. Visa has FY2026 results but the latest filed 10-K is FY2025.','- Third-party transcript errors, inherited PDF extraction artifacts and cached-email truncation remain possible. Load-bearing current numbers were checked against the company release; original documents remain available.','- Two unsuccessful discovery URLs are retained in the manifests: an old BX MarketBeat link and a guessed Coinbase Q&A PDF. Recent-quarter coverage is complete using the other archived sources.','- Full historical reading, matched-basis valuation models and exhaustive retrieval of every past conference appearance are not claimed.','','## Validation','','- '+('No missing files, hash mismatches or gaps in the latest eight quarterly-call periods were found.' if not errors else 'Issues: '+ '; '.join(errors))]
(ROOT/'_wiki/_meta/financials-coverage.md').write_text('\n'.join(ledger)+'\n',encoding='utf-8')
print(json.dumps({'totals':totals,'errors':errors},indent=2))
if errors:sys.exit(1)
