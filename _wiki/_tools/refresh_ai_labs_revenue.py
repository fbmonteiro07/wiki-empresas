"""Refresh AI Labs on saved-workbook changes, then publish only its two artifacts.

Run: py _wiki/_tools/refresh_ai_labs_revenue.py --publish
Validate without publication: add --check (creates an audited candidate only).
The hourly Codex heartbeat calls this entry point. No workbook writes or recalculation.
"""
import argparse
import contextlib
import datetime as dt
import hashlib
import io
import json
import math
import os
from pathlib import Path
import subprocess
import time
import urllib.request

import build_ai_labs_revenue as builder

DATA=builder.DATA
TEAM=Path('P:/Felipe Monteiro/US Equities/Capstone-Wiki')
MIRROR=builder.ROOT/'_dashboards'/'ai-labs'
PUBLIC='https://fbmonteiro07.github.io/Capstone-Wiki/ai-labs/'
FILES=('index.html','revenue-data.json')
REL_FILES=tuple('ai-labs/'+name for name in FILES)
STATE=DATA/'auto-refresh-state.json'
SAO_PAULO=dt.timezone(dt.timedelta(hours=-3))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def artifact_hash(path):
    return digest(path.read_text(encoding='utf-8-sig').replace('\r\n','\n').encode('utf-8'))


def atomic_write(path,raw):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+'.ai-labs-tmp')
    temporary.write_bytes(raw)
    os.replace(temporary,path)


def save_state(state):
    atomic_write(STATE,(json.dumps(state,indent=2)+'\n').encode('utf-8'))


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


@contextlib.contextmanager
def exclusive_lock():
    DATA.mkdir(parents=True,exist_ok=True)
    with (DATA/'auto-refresh.lock').open('a+b') as handle:
        if handle.tell()==0: handle.write(b'0'); handle.flush()
        handle.seek(0)
        if os.name=='nt':
            import msvcrt
            try: msvcrt.locking(handle.fileno(),msvcrt.LK_NBLCK,1)
            except OSError as exc: raise RuntimeError('Another AI Labs refresh is already running') from exc
            try: yield
            finally:
                handle.seek(0); msvcrt.locking(handle.fileno(),msvcrt.LK_UNLCK,1)
        else:
            import fcntl
            fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
            try: yield
            finally: fcntl.flock(handle,fcntl.LOCK_UN)


def input_identity(workbook):
    before=workbook.stat()
    if time.time()-before.st_mtime<30:
        raise RuntimeError('AI Model was saved less than 30 seconds ago; retry after the save settles')
    raw=workbook.read_bytes(); after=workbook.stat()
    if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
        raise RuntimeError('AI Model changed while being read; keep the published version and retry')
    inputs={'workbook_sha256':digest(raw),'workbook_mtime_ns':after.st_mtime_ns}
    for path in [Path(__file__),Path(builder.__file__),DATA/'sources.json',DATA/'legacy-wfs-2026-06-11.html',*sorted(builder.UI.glob('revenue.*'))]:
        inputs[path.name]=digest(path.read_bytes())
    return digest(json.dumps(inputs,sort_keys=True).encode()),inputs


def validate(payload):
    expected={'openai_net':('OpenAI','net'),'openai_gross':('OpenAI','gross'),
              'anthropic_net':('Anthropic','net'),'anthropic_gross':('Anthropic','gross')}
    series={s['id']:s for s in payload['series']}
    if len(payload['series'])!=len(expected) or set(series)!=set(expected): raise ValueError('Missing or duplicate company series')
    for key,(company,basis) in expected.items():
        s=series[key]
        if (s['company'],s['basis'])!=(company,basis): raise ValueError('Company/basis mismatch')
        if not s['points'] or len({p['date'] for p in s['points']})!=len(s['points']): raise ValueError('Empty or duplicate monthly series')
        for p in s['points']:
            if not isinstance(p['value'],(int,float)) or not math.isfinite(p['value']) or p['value']<0: raise ValueError('Invalid revenue value')
            if p['status'] not in ('Forecast','Model estimate'): raise ValueError('Invalid model classification')
    for basis in ('reported','net','gross'):
        parts=[s for s in series.values() if s['reported_basis']] if basis=='reported' else [s for s in series.values() if s['basis']==basis]
        if len(parts)!=2: raise ValueError('Combined system requires two companies')
        maps=[{p['date']:p for p in s['points']} for s in parts]
        total=payload['combined']['monthly'][basis]['points']
        expected_dates=set(maps[0])&set(maps[1])
        if len(total)!=len(expected_dates) or {p['date'] for p in total}!=expected_dates: raise ValueError('Combined monthly join is incomplete')
        for p in total:
            components=[m[p['date']] for m in maps]
            if not math.isclose(p['value'],sum(c['value'] for c in components),abs_tol=1e-7,rel_tol=1e-12): raise ValueError('Combined monthly sum failed')
            if {c['cell'] for c in p['components']}!={c['cell'] for c in components}: raise ValueError('Combined source cells mismatch')
    annual=payload['annual']; expected_periods={a['period'] for a in annual if a['company']=='OpenAI'} & {a['period'] for a in annual if a['company']=='Anthropic'}
    totals=payload['combined']['annual']
    if len(totals)!=len(expected_periods) or {a['period'] for a in totals}!=expected_periods: raise ValueError('Combined annual periods mismatch')
    for a in totals:
        parts=[p for p in annual if p['period']==a['period']]
        if len(parts)!=2 or not math.isclose(a['value'],sum(p['value'] for p in parts),abs_tol=1e-7,rel_tol=1e-12): raise ValueError('Combined annual sum failed')
    for row in [*annual,*payload['quarterly']]:
        if not isinstance(row['value'],(int,float)) or not math.isfinite(row['value']) or row['value']<0: raise ValueError('Invalid period revenue')
    if any(s['published']>payload['checked'] for s in payload['sources'].values()): raise ValueError('Source review date predates source')


def git(team,*args,check=True):
    result=subprocess.run(['git',*args],cwd=team,text=True,encoding='utf-8',errors='replace',capture_output=True,timeout=120)
    if check and result.returncode:
        raise RuntimeError('git '+args[0]+': '+result.stderr.strip()[-1500:])
    return result.stdout.rstrip('\r\n') if check else result


def check_owned_commit(team,pending):
    subject=git(team,'show','-s','--format=%s','HEAD')
    paths=set(git(team,'diff-tree','--no-commit-id','--name-only','-r','HEAD').splitlines())
    if subject!='ai-labs: automatic refresh '+pending['fingerprint'][:12] or not paths or not paths<=set(REL_FILES):
        raise RuntimeError('Unpublished commits are not exclusively this AI Labs refresh')
    for name in FILES:
        result=subprocess.run(['git','show','HEAD:ai-labs/'+name],cwd=team,capture_output=True,check=True,timeout=30)
        raw=result.stdout.decode('utf-8-sig').replace('\r\n','\n').encode('utf-8')
        if digest(raw)!=pending['artifact_hashes'][name]:
            raise RuntimeError('Pending commit artifacts changed')


def publish(team,pending,state):
    if git(team,'branch','--show-current')!='main': raise RuntimeError('Team repository must be on main')
    # Only our exact pending artifacts can be dirty; never include other work.
    status=git(team,'status','--porcelain','--untracked-files=all')
    for line in status.splitlines():
        rel=line[3:]
        if rel not in REL_FILES or artifact_hash(team/rel)!=pending['artifact_hashes'][Path(rel).name]:
            raise RuntimeError('Team repository has other changes; publication deferred: '+rel)
    git(team,'fetch','origin','main')
    behind,ahead=map(int,git(team,'rev-list','--left-right','--count','origin/main...HEAD').split())
    if ahead:
        if ahead!=1: raise RuntimeError('Other unpublished commits exist; publication deferred')
        check_owned_commit(team,pending)
        if status: raise RuntimeError('Pending commit has extra working changes')
        if behind:
            result=git(team,'rebase','origin/main',check=False)
            if result.returncode:
                git(team,'rebase','--abort')
                raise RuntimeError('Concurrent changes conflict with this AI Labs refresh; previous commit retained')
    elif behind:
        if status: raise RuntimeError('Remote advanced while pending files were dirty; publication deferred')
        git(team,'merge','--ff-only','origin/main')
    head=git(team,'rev-parse','HEAD')
    candidate=Path(pending['candidate'])
    for name in FILES:
        if artifact_hash(candidate/name)!=pending['artifact_hashes'][name]: raise RuntimeError('Candidate artifact changed after validation')
        atomic_write(team/'ai-labs'/name,(candidate/name).read_bytes())
    if git(team,'rev-parse','HEAD')!=head: raise RuntimeError('Another writer committed during publication; retry required')
    difference=git(team,'diff','--quiet','HEAD','--',*REL_FILES,check=False)
    untracked=git(team,'ls-files','--others','--exclude-standard','--',*REL_FILES)
    if difference.returncode not in (0,1): raise RuntimeError('Cannot inspect publication diff')
    if difference.returncode or untracked:
        git(team,'add','--',*REL_FILES)
        git(team,'commit','--only','-m','ai-labs: automatic refresh '+pending['fingerprint'][:12],'--',*REL_FILES)
    commit=git(team,'rev-parse','HEAD'); pending['commit']=commit; save_state(state)
    behind,ahead=map(int,git(team,'rev-list','--left-right','--count','origin/main...HEAD').split())
    if ahead:
        if ahead!=1: raise RuntimeError('Publication would include unrelated commits')
        check_owned_commit(team,pending)
        git(team,'push','origin','HEAD:main')
    for name in FILES:
        atomic_write(MIRROR/name,(candidate/name).read_bytes())
    builder.save_snapshot((candidate/'revenue-data.json').read_text(encoding='utf-8'))
    return commit


def verify_live(pending,wait_seconds):
    deadline=time.monotonic()+wait_seconds; last_error='Deployment has not propagated yet'
    while True:
        try:
            for name in FILES:
                url=PUBLIC+(name if name!='index.html' else '')+'?v='+pending['fingerprint'][:12]
                req=urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'Capstone-AI-Labs-refresh'})
                with urllib.request.urlopen(req,timeout=20) as response:
                    raw=response.read().decode('utf-8-sig').replace('\r\n','\n').encode('utf-8')
                if digest(raw)!=pending['artifact_hashes'][name]: raise ValueError('Public '+name+' is still an older version')
            return True,None
        except (OSError,ValueError) as exc:
            last_error=str(exc)
        if time.monotonic()>=deadline: return False,last_error
        time.sleep(min(10,max(0,deadline-time.monotonic())))


def run(args):
    state=json.loads(STATE.read_text(encoding='utf-8')) if STATE.exists() else {}
    with exclusive_lock():
        state=json.loads(STATE.read_text(encoding='utf-8')) if STATE.exists() else {}
        fingerprint,inputs=input_identity(args.workbook)
        prior=state.get('completed',{})
        intact=all((directory/name).is_file() and artifact_hash(directory/name)==prior.get('artifact_hashes',{}).get(name) for directory in (MIRROR,args.team/'ai-labs') for name in FILES)
        if not args.force and not args.check and not state.get('pending') and prior.get('fingerprint')==fingerprint and intact:
            state['last_checked']=now(); state['last_result']='unchanged'; save_state(state)
            return {'status':'unchanged','workbook_sha256':inputs['workbook_sha256']}
        pending=state.get('pending') if not args.check else None
        if not pending:
            candidate=DATA/'runs'/fingerprint[:16]
            asof=dt.datetime.fromtimestamp(args.workbook.stat().st_mtime,SAO_PAULO).date().isoformat()
            with contextlib.redirect_stdout(io.StringIO()):
                payload=builder.build(args.workbook,asof,builder.DEFAULT_TEMPLATE,candidate,persist=False)
            validate(payload)
            after,_=input_identity(args.workbook)
            if after!=fingerprint or payload['workbook_sha256']!=inputs['workbook_sha256']: raise RuntimeError('Inputs changed during build; previous dashboard retained')
            pending={'fingerprint':fingerprint,'inputs':inputs,'candidate':str(candidate),'artifact_hashes':{name:artifact_hash(candidate/name) for name in FILES},'model_asof':asof,'sources_checked':payload['checked'],'validated_at':now()}
            if args.check: return {'status':'validated','candidate':str(candidate),'fingerprint':fingerprint,'combined_bases':list(payload['combined']['monthly'])}
            state['pending']=pending; save_state(state)
        validate(json.loads((Path(pending['candidate'])/'revenue-data.json').read_text(encoding='utf-8')))
        if not args.publish: return {'status':'validated_pending_publication','candidate':pending['candidate']}
        commit=publish(args.team,pending,state)
        print(json.dumps({'status':'verifying_deployment','commit':commit}),flush=True)
        ok,error=verify_live(pending,args.wait_seconds)
        state['last_checked']=now()
        if not ok:
            state['last_result']='deployment_pending';state['last_error']=error;save_state(state)
            return {'status':'deployment_pending','commit':commit,'detail':error,'retry':'Run the same command to verify or resume; do not create a duplicate commit'}
        pending['published_at']=now();state['completed']=pending;state.pop('pending',None);state.pop('last_error',None);state['last_result']='updated';save_state(state)
        atomic_write(Path(pending['candidate'])/'publication.json',(json.dumps(pending,indent=2)+'\n').encode('utf-8'))
        return {'status':'updated','commit':commit,'workbook_sha256':pending['inputs']['workbook_sha256'],'sources_checked':pending['sources_checked'],'url':PUBLIC}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workbook',type=Path,default=builder.DEFAULT_WB)
    p.add_argument('--team',type=Path,default=TEAM)
    p.add_argument('--publish',action='store_true')
    p.add_argument('--check',action='store_true')
    p.add_argument('--force',action='store_true')
    p.add_argument('--wait-seconds',type=int,default=120)
    args=p.parse_args()
    try: result=run(args)
    except Exception as exc:
        print(json.dumps({'status':'failed','error':str(exc)}),flush=True)
        return 1
    print(json.dumps(result),flush=True)
    return 2 if result['status']=='deployment_pending' else 0


if __name__=='__main__':
    raise SystemExit(main())
