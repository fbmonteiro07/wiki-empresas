from pathlib import Path
import hashlib,json,re
r=Path.cwd();d=r/'_wiki/_data/financials';rev=d/'email_review_2026-11-01';live=json.loads((d/'live_email_manifest.json').read_text(encoding='utf-8'))
checks={};issues=[]
companies=['JPM','SPGI','MCO','BX','KKR','GS','V','MA','APO','HOOD','COIN']
for tk in companies:
 old=(rev/'before/_wiki'/f'{tk}.md').read_text(encoding='utf-8-sig');new=(r/'_wiki'/f'{tk}.md').read_text(encoding='utf-8-sig')
 missing=[ln for ln in old.splitlines() if ln.strip() and not ln.startswith('_Wiki') and ln not in new]
 if missing:issues.append({'ticker':tk,'old_lines_changed':missing})
 if len(re.findall(r'^\| [123]\. ',new,re.M))!=3:issues.append({'ticker':tk,'debate_rows':'not three'})
 if '2026-11-01 — Live Outlook review' not in new:issues.append({'ticker':tk,'changelog':'missing'})
checks['all_11_have_three_dated_debates']=not issues
checks['prior_company_research_lines_preserved']=not any('old_lines_changed' in x for x in issues)
checks['33_unique_messages_36_company_copies']=len({x['graph_message_id'] for x in live['records']})==33 and len(live['records'])==36
checks['live_source_file_hashes']=all(hashlib.sha256((r/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in live['records'])
checks['all_live_sources_cited']=all(x['path'] in (r/'_wiki'/f'{x["ticker"]}.md').read_text(encoding='utf-8') for x in live['records'])
checks['headline_only_limits_preserved']=sum('headline and author' in x['quality'] for x in live['records'])==2
checks['redburn_volume_conflict_flagged']=any(x['quality_flags'] for x in live['records'] if x['ticker']=='HOOD')
checks['source_report_date_and_received_time_separate']=all(x.get('report_date') and x.get('received_utc') for x in live['records'])
old=(rev/'before/_wiki/themes/ai-compute-deals.md').read_text(encoding='utf-8-sig');new=(r/'_wiki/themes/ai-compute-deals.md').read_text(encoding='utf-8-sig')
checks['existing_compute_history_preserved']=all(ln in new for ln in old.splitlines() if ln.strip())
for k,v in checks.items():
 if not v:issues.append({'check':k})
result={'as_of':'2026-11-01','checks':checks,'issues':issues}
(rev/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
raise SystemExit(bool(issues))
