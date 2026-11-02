from pathlib import Path
p=Path('_wiki/_tools/build_financials_sources.py');s=p.read_text(encoding='utf-8')
s=s.replace('th{background:var(--panel);position:sticky;top:0}','th{background:var(--panel);position:sticky;top:0}td:first-child{white-space:nowrap}')
old="   parts.append('<tr><td>'+esc(x['date'])"
new="   fidelity={'cache_at_length_limit':'Cached email excerpt; reached the 9,000-character limit','cached_email_body':'Cached email body; linked report may not be included'}.get(x.get('fidelity',''),x.get('fidelity',''))\n   review=x['review_status'].replace('Selected passage emitted for review','Excerpt extracted; analytical review not confirmed')\n"+old
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace("esc(x.get('fidelity',''))","esc(fidelity)").replace("esc(x['review_status'])","esc(review)")
p.write_text(s,encoding='utf-8')
p=Path('automation/financials/build_inventory.py');s=p.read_text(encoding='utf-8');s=s.replace('Third-party transcription; numbers checked against primary releases','Third-party transcription; consult company releases for reported figures');p.write_text(s,encoding='utf-8')
print('Made source-quality labels readable and distinguished transcription fidelity from analytical verification.')
