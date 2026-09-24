import json, re
from pathlib import Path

BASE=Path(__file__).resolve().parent
OUT=BASE/'sources'
OUT.mkdir(exist_ok=True)
live=[json.loads(x) for x in (BASE/'emails_live.jsonl').read_text(encoding='utf-8-sig').splitlines()]
archive=json.loads((BASE/'emails_archive_sorted.json').read_text(encoding='utf-8'))
tweets=sorted(json.loads((BASE/'tweets.json').read_text(encoding='utf-8')),key=lambda x:x['created_at'],reverse=True)
L=[13,27,48,65,96,134,147,148,170,176,190,193,194,199,207,208,209,251,254,255,256]
A=[42,151,221,231,266,348,754,899]
T=[1,2,6,12,18,25,31,41,43,44,46,48,56,62,77,81,86,89,97,99,109,111,117,121,135,140,143,146,150,156,161,166,179,195,205,208,210,214,219,224,231,239,245,247,248,251,259,263,266,268,274,276,297,304,305,306,308]
manifest=[]
for prefix,rows,indices in [('L',live,L),('A',archive,A)]:
    for i in indices:
        m=rows[i];code=f'{prefix}{i:03d}' if prefix=='L' else f'A{i:04d}'
        body=m['body'].replace('\r','')
        body=re.sub(r'https?://\S+','[original URL omitted; available in raw archive]',body)
        body=re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+','\n\n',body)
        txt=f"# {code} — {m['subject']}\n\nReceived: {m['d']} {m.get('t','')} (Outlook local date).\n\nSender: {m.get('sender',m['from'])}.\n\nSource: {'Live Outlook, complete message body' if prefix=='L' else 'Saved Outlook archive; body may be limited to 9,000 characters'}. Retrieved 2026-09-23. The report publication date inside the message takes precedence over the received date. Quoted historical messages retain their original dates. Tracking URLs omitted from this readable copy.\n\n```text\n{body}\n```\n"
        (OUT/f'{code}.md').write_text(txt,encoding='utf-8')
        manifest.append({'code':code,'date_received':m['d'],'sender':m.get('sender',m['from']),'subject':m['subject'],'entry_id':m['id'],'file':f'sources/{code}.md'})
for i in T:
    t=tweets[i];code=f'T{i:03d}'
    txt=f"# {code} — @{t['handle'].strip()} — {t['created_at'][:10]}\n\n[Original post]({t['url']})\n\nSaved timestamp (UTC): {t['created_at']}. Retweet: {bool(t['is_retweet'])}. Retrieved from the saved feed on 2026-09-23. Statements are those of the account; a media or broker relay is not independent confirmation.\n\n{t['text']}\n"
    (OUT/f'{code}.md').write_text(txt,encoding='utf-8')
    manifest.append({'code':code,'date':t['created_at'][:10],'handle':t['handle'].strip(),'url':t['url'],'file':f'sources/{code}.md'})
(BASE/'source_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
coverage=json.loads((BASE/'coverage_initial.json').read_text(encoding='utf-8'))
coverage.update({'live_subject_search_raw_hits':len(live),'live_search_folder_errors':0,'selected_email_source_copies':len(L)+len(A),'selected_tweet_source_copies':len(T),'supplemental_tweet_hits':2,'limitations':['Saved curated feed, not all of X; latest saved tweet September 22.','Archive body search covers broker-domain messages, through September 22; stored bodies may be truncated at 9000 characters.','Live all-sender search covers received-mail folder subjects through retrieval on September 23, excluding deleted, junk, sent and drafts. It is not a full live body search of every non-broker email.','Raw keyword matches include invitations, duplicates and false positives; these counts are not substantive research counts or independent observations.','Selected full live messages were read; linked reports, attachments and paywalled articles were not all opened.','Publication dates inside messages are distinguished from local receipt dates.']})
(BASE/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# Battery review — source register','', 'Retrieved 2026-09-23. L = complete Outlook body; A = saved broker archive body; T = saved tweet. Publication date can differ from receipt date.','']
for m in manifest:
    label=f"{m['code']} | {m.get('date_received',m.get('date'))} | {m.get('sender',m.get('handle'))} | {m.get('subject','Saved post')}"
    lines.append(f"- [{label}](<{(BASE/m['file']).as_posix()}>)")
(BASE/'source_register.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'selected_emails':len(L)+len(A),'selected_tweets':len(T),'source_files':len(manifest)},indent=2))
