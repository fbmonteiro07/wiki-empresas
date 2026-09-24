import collections, datetime, json, re, sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
START, END = '2026-06-25', '2026-09-24'
TERMS = r'\bbatter(?:y|ies)\b|\bbateria\w*|\bBESS\b|\bBBUs?\b|\blithium\b|\bLFP\b|\bCATL\b|\bMegapack\w*|\bPowerwall\w*|\bFluence\b|\bFLNC\b|\benergy storage\b|\bsodium.ion\b|\bsolid.state\b|\banode\w*|\bcathode\w*|\bAlbemarle\b|\bQuantumScape\b|\bEnovix\b|\bAmprius\b|\bGotion\b|\bEVE Energy\b|\bSunwoda\b|\bLG Energy\b|\bSamsung SDI\b|\bSK On\b|\bESS\b|\bcapacit(?:or|ors)\b'
RX = re.compile(TERMS, re.I)

def save(name, data):
    (BASE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def excerpts(text, pad=350):
    ranges=[]
    for m in RX.finditer(text):
        lo,hi=max(0,m.start()-pad),min(len(text),m.end()+pad)
        if ranges and lo<=ranges[-1][1]: ranges[-1][1]=hi
        else: ranges.append([lo,hi])
    return [' '.join(text[a:b].split()) for a,b in ranges]

def main():
    stats={'window_start':START,'window_end_exclusive':END,'retrieved_at':datetime.datetime.now().isoformat()}
    con=sqlite3.connect(r'E:\.claude\data\twitter-briefing\tweets.sqlite')
    con.execute('PRAGMA query_only=ON'); con.row_factory=sqlite3.Row
    cols='tweet_id,handle,author_name,category,created_at,text,is_reply,is_retweet,is_quote,retweet_of_handle,url,like_count,view_count'
    scanned=con.execute('SELECT count(*) FROM tweets WHERE created_at>=? AND created_at<?',(START,END)).fetchone()[0]
    fts='battery OR batteries OR bateria* OR BESS OR BBU OR BBUs OR lithium OR LFP OR CATL OR Megapack* OR Powerwall* OR Fluence OR FLNC OR "energy storage" OR "sodium ion" OR "solid state" OR anode* OR cathode* OR Albemarle OR QuantumScape OR Enovix OR Amprius OR Gotion OR "EVE Energy" OR Sunwoda OR "LG Energy" OR "Samsung SDI" OR "SK On" OR ESS OR capacitor*'
    rows=con.execute(f'SELECT {cols} FROM tweets WHERE rowid IN (SELECT rowid FROM tweets_fts WHERE tweets_fts MATCH ?) AND created_at>=? AND created_at<?',(fts,START,END))
    hits=[]
    for r in rows:
        if RX.search(r['text'] or ''): hits.append(dict(r))
    stats['tweets_scanned']=scanned;stats['tweet_keyword_hits']=len(hits)
    stats['tweet_hits_ex_retweets']=sum(not x['is_retweet'] for x in hits)
    stats['tweet_latest']=con.execute('select max(created_at) from tweets').fetchone()[0]
    save('tweets.json',hits)
    print('TWEETS',scanned,len(hits),flush=True)
    mails=json.loads((ROOT/'_wiki/_data/sentiment/sellside_mail_raw.json').read_text(encoding='utf-8-sig'))
    mails={m['id']:m for m in mails if START<=m['d']<END}
    stats['email_headers_in_window']=len(mails)
    print('MAIL HEADERS',len(mails),flush=True)
    matches={}; bodies=0
    with (ROOT/'_wiki/_data/sentiment/sellside_mail_bodies.jsonl').open(encoding='utf-8-sig') as f:
        for line in f:
            row=json.loads(line); key=row.get('id')
            if key not in mails:continue
            bodies+=1; m=mails[key]; body=row.get('body','')
            if RX.search(m['subject']+'\n'+body):
                matches[key]={**m,'body':body,'subject_match':bool(RX.search(m['subject'])),'excerpts':excerpts(body)}
    for key,m in mails.items():
        if key not in matches and RX.search(m['subject']): matches[key]={**m,'body':'','subject_match':True,'excerpts':[]}
    stats['email_bodies_in_window']=bodies;stats['email_keyword_hits']=len(matches)
    stats['email_subject_hits']=sum(x['subject_match'] for x in matches.values())
    save('emails_archive.json',list(matches.values()));save('coverage_initial.json',stats)
    lines=[]
    for i,t in enumerate(sorted(hits,key=lambda x:x['created_at'],reverse=True)):
        lines.append(f"T{i:04d} | {t['created_at'][:10]} | @{t['handle']} | RT={t['is_retweet']} | likes={t['like_count']} | {t['text']}\n")
    (BASE/'tweets_review.txt').write_text('\n'.join(lines),encoding='utf-8')
    lines=[]
    for i,m in enumerate(sorted(matches.values(),key=lambda x:x['d'],reverse=True)):
        lines.append(f"E{i:04d} | {m['d']} | {m['from']} | SUBJECT_MATCH={m['subject_match']} | {m['subject']}\n"+'\n'.join(m['excerpts'])+'\n')
    (BASE/'emails_review.txt').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps(stats,indent=2)); print('Top handles',collections.Counter(t['handle'] for t in hits).most_common(20))

if __name__=='__main__':main()
