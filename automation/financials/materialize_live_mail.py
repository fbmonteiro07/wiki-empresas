"""Preserve selected live Outlook bodies with provenance; no mail is sent."""
import datetime,hashlib,json,re
from pathlib import Path
ROOT=Path.cwd(); DATA=ROOT/'_wiki/_data/financials'; REVIEW=DATA/'email_review_2026-11-01'
old=json.loads((DATA/'commentary_manifest.json').read_text(encoding='utf-8-sig'))['records']
dates=['2026-10-13','2026-10-06','2026-10-13','2026-10-06','2026-10-27','2026-09-02','2026-06-18','2026-10-21','2026-07-22','2026-10-23','2026-10-22','2026-10-19','2026-09-28','2026-08-31','2026-08-31','2026-10-06','2026-08-04','2026-05-21','2026-10-28','2026-10-28','2026-10-28','2026-10-27','2026-10-30','2026-10-29','2026-10-29','2026-10-29','2026-10-27','2026-10-26','2026-09-07','2026-10-28','2026-10-29','2026-09-09','2026-10-30']
authors=['Barclays / Jason Goldberg','Barclays / Jason Goldberg','Barclays / Jason Goldberg','Barclays / Jason Goldberg','Jefferies / Adam Panzer (FIG sales)','Jefferies / Adam Panzer (FIG sales); Surinder Thind research view distinguished','Rothschild & Co Redburn / US Morning, Information Services research summary','Jefferies / Adam Panzer (FIG sales)','Jefferies / Adam Panzer (FIG sales)','Jefferies / Adam Panzer (FIG sales)','Jefferies / Adam Panzer (FIG sales)','Jefferies / Adam Panzer (FIG sales)','Rothschild & Co Redburn / US Morning','Goldman Sachs / Christian DeGrasse (sector sales)','Jefferies / Adam Panzer (FIG sales)','Rothschild & Co Redburn / US Morning','Rothschild & Co Redburn / US Morning','Rothschild & Co Redburn / Raj Chaudhury (specialist sales)','Rothschild & Co Redburn / Fahed Kunwar and Ellie Hall','Barclays / Nik Cremo','Morgan Stanley / James Faucette, Meryl Thomas, Michael Infante and Shefali Tamaskar','Goldman Sachs / Will Nance','Morgan Stanley / James Faucette, Meryl Thomas, Michael Infante and Shefali Tamaskar','Barclays / Nik Cremo','Goldman Sachs / Will Nance','Rothschild & Co Redburn / Fahed Kunwar and Ellie Hall','Goldman Sachs / James Yaro and team','Rothschild & Co Redburn / Charles Bendit and Tejasvi Muvvala; distributed by Madeleine Falkiner (sales)','Goldman Sachs / James Yaro and team','Bernstein / Gautam Chhugani, Mahika Sapra and Sanskar Chindalia','Goldman Sachs / James Yaro and team','Goldman Sachs / James Yaro and team','Bernstein / Gautam Chhugani, Mahika Sapra and Sanskar Chindalia']
rec=[]; lookup={}
def norm(s):return re.sub(r'\s+',' ',s).strip().casefold()
for i in range(33):
 m=json.loads((REVIEW/f'{i:02d}.json').read_text(encoding='utf-8')); sender=m['sender']['emailAddress']; received=m['receivedDateTime']; date=received[:10]; body=m['body']['content']; suffix=hashlib.sha256(m['id'].encode()).hexdigest()[:12]
 tickers=list(m['tickers'])
 if i==10:tickers+=['JPM','GS']
 candidates=[x for x in old if norm(x['subject'])==norm(m['subject']) and x['sender'].lower()==sender['address'].lower() and abs((datetime.date.fromisoformat(x['date'])-datetime.date.fromisoformat(date)).days)<=1]
 ids={x['source_id'] for x in candidates};canonical=next(iter(ids)) if len(ids)==1 else 'outlook:'+m['id']
 quality='Live Outlook body as returned by connector; selected issuer passages reviewed; linked report not retrieved'
 if i in [26,30]:quality='Live Outlook research alert; headline and author metadata only; linked report not retrieved'
 notes=[]
 if i==27:notes.append('Data-quality flag: sales introduction states $960bn September volume, inconsistent with the same email/research summary stating approximately $379bn for 9M26. Neither volume figure is adopted as a canonical TAM input. Legal assertions are broker characterizations, not independently adjudicated legal findings.')
 for tk in dict.fromkeys(tickers):
  p=ROOT/tk/'commentary'/f'{date}_OUTLOOK_{suffix}.md';p.parent.mkdir(exist_ok=True)
  text=f'# {m["subject"]}\n\n- Source: {authors[i]}\n- Sender: {sender["name"]} <{sender["address"]}>\n- Report / note date: {dates[i]}\n- Received UTC: {received}\n- Retrieved and reviewed: 2026-11-01\n- Original email: {m["web_link"]}\n- Quality: {quality}\n- Canonical source ID: {canonical}\n- Body SHA-256: {hashlib.sha256(body.encode()).hexdigest()}\n'
  if candidates:text+='- Prior cached version(s): '+', '.join(x['path'] for x in candidates if x['ticker']==tk)+'\n'
  if notes:text+='- '+'\n- '.join(notes)+'\n'
  text+='\n## Retrieved email body\n\n'+body+'\n'
  p.write_text(text,encoding='utf-8')
  x={'ticker':tk,'date':dates[i],'received_date':date,'received_utc':received,'report_date':dates[i],'subject':m['subject'],'sender':sender['address'],'analyst_attribution':authors[i],'path':p.relative_to(ROOT).as_posix(),'source_id':canonical,'graph_message_id':m['id'],'source_url':m['web_link'],'body_chars':len(body),'quality':quality,'quality_flags':notes,'recorded':'2026-11-01','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'review_status':'Selected issuer passages reviewed','cached_version_paths':[x['path'] for x in candidates if x['ticker']==tk],'identity_match':'sender + normalized subject + received date within one day' if candidates else 'live Outlook message ID','archive_index':i,'status':'archived'}
  rec.append(x);lookup[f'{i}:{tk}']=x['path']
(DATA/'live_email_manifest.json').write_text(json.dumps({'as_of':'2026-11-01','scope':'Targeted 2026 year-to-date Outlook review; full connector-returned email body retained, not a claim to complete linked reports or all historical email.','unique_live_messages':33,'records':rec},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(REVIEW/'citation_lookup.json').write_text(json.dumps(lookup,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'messages':33,'company_documents':len(rec),'matched_existing_email_documents':sum(bool(x['cached_version_paths']) for x in rec),'report_dates_separate_from_received':True}))
