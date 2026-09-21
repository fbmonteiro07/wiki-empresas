"""Public Vercel AI Gateway daily shares; stdlib only, reproducible snapshots."""
import datetime as dt
import html
import json
import math
import ssl
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / '_data'
ROOT = DATA / 'vercel'
SOURCE = 'https://vercel.com/ai-gateway/leaderboards/models'
DOCS = 'https://vercel.com/docs/ai-gateway/leaderboards'
API = 'https://vercel.com/api/ai/leaderboard-export'
METRICS = {'tokens': 'Tokens', 'requests': 'Requests', 'spend': 'Estimated spend (list prices)'}
NAMES = {'openai': 'OpenAI', 'anthropic': 'Anthropic', 'google': 'Google', 'deepseek': 'DeepSeek', 'zai': 'Z.ai', 'z-ai': 'Z.ai', 'moonshotai': 'Moonshot', 'xai': 'xAI', 'x-ai': 'xAI'}

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Capstone-research-public-gateway-monitor/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            return json.load(response)
    except urllib.error.URLError as exc:
        # Existing workstation's TLS proxy lacks a valid authority key identifier.
        # This fallback is restricted to this unauthenticated, public data origin.
        if not isinstance(exc.reason, ssl.SSLCertVerificationError) or not url.startswith(API + '?'):
            raise
        with urllib.request.urlopen(req, timeout=45, context=ssl._create_unverified_context()) as response:
            return json.load(response)

def validate(payload, dataset):
    if payload.get('dataset') != dataset or not payload.get('rows'):
        raise ValueError('Missing or wrong Vercel dataset: ' + dataset)
    seen = set()
    for row in payload['rows']:
        dt.date.fromisoformat(row['date'])
        value = row['share_percent']
        if not isinstance(value, (float, int)) or not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError('Invalid share_percent')
        key = (row['date'], row['metric'], row['name'])
        if key in seen or row.get('modality') != 'all':
            raise ValueError('Duplicate or wrong-modality Vercel row')
        seen.add(key)
    metrics = {r['metric'] for r in payload['rows']}
    if not set(METRICS).issubset(metrics):
        raise ValueError('Vercel export is missing required metrics')

def fetch():
    today = dt.date.today()
    end = today - dt.timedelta(days=1)
    params = {'format': 'json', 'modality': 'all', 'from': (end-dt.timedelta(days=89)).isoformat(), 'to': end.isoformat()}
    result, sources = {}, {}
    for dataset in ('models', 'labs'):
        url = API + '?' + urllib.parse.urlencode(dict(params, dataset=dataset))
        payload = fetch_json(url)
        validate(payload, dataset)
        result[dataset] = payload
        sources[dataset] = url
    # Publish the pointer only after both datasets validate; keep all prior runs.
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')
    folder = ROOT / 'raw' / stamp
    for dataset, payload in result.items():
        write_json(folder / (dataset + '.json'), payload)
    write_json(folder / 'manifest.json', {'fetched_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'sources': sources, 'tls_proxy_fallback': 'Public unauthenticated Vercel origin only, if certificate verification fails'})
    (ROOT / 'latest.txt').write_text(stamp, encoding='utf-8')
    return folder

def summarize(payload, end):
    """Daily share averages, never a volume-weighted weekly share; missing != 0."""
    end_date = dt.date.fromisoformat(end)
    current = [(end_date-dt.timedelta(days=n)).isoformat() for n in range(6,-1,-1)]
    previous = [(end_date-dt.timedelta(days=n)).isoformat() for n in range(13,6,-1)]
    result = {}
    for metric in METRICS:
        by_name = defaultdict(dict)
        for row in payload['rows']:
            if row['metric'] == metric and row['date'] <= end:
                by_name[row['name']][row['date']] = row['share_percent']
        rows = []
        for name, values in by_name.items():
            if end not in values:
                continue
            now = [values[d] for d in current if d in values]
            before = [values[d] for d in previous if d in values]
            avg = sum(now)/7 if len(now) == 7 else None
            old = sum(before)/7 if len(before) == 7 else None
            rows.append({'name': name, 'latest_share': values[end], 'mean_7d': avg, 'previous_mean_7d': old,
                         'change_pp': avg-old if avg is not None and old is not None else None,
                         'days': len(now), 'previous_days': len(before),
                         'series': [{'date': d, 'share': values.get(d)} for d in previous+current]})
        result[metric] = sorted(rows, key=lambda r:r['latest_share'], reverse=True)
    return result

def build(folder=None):
    folder = folder or ROOT / 'raw' / (ROOT / 'latest.txt').read_text(encoding='utf-8').strip()
    payloads = {name: read_json(folder / (name+'.json')) for name in ('models','labs')}
    for name, payload in payloads.items():
        validate(payload, name)
    # Common last day across both datasets and all three key metrics.
    date_sets = [{r['date'] for r in p['rows'] if r['metric']==m} for p in payloads.values() for m in METRICS]
    end = max(set.intersection(*date_sets))
    day = dt.date.fromisoformat(end)
    manifest_path = folder / 'manifest.json'
    manifest = read_json(manifest_path) if manifest_path.exists() else {}
    d = {'source': SOURCE, 'docs': DOCS, 'license': 'CC BY 4.0', 'asof': end,
         'fetched_at': manifest.get('fetched_at'), 'raw_snapshot': folder.name,
         'current_period': [(day-dt.timedelta(days=6)).isoformat(), end],
         'previous_period': [(day-dt.timedelta(days=13)).isoformat(), (day-dt.timedelta(days=7)).isoformat()],
         'method': 'Unweighted mean of seven daily shares. Not share of total weekly volume. A missing row is unknown, never zero; change requires all 14 daily observations.',
         'datasets': {name: summarize(p,end) for name,p in payloads.items()}}
    write_json(ROOT/'dashboard.json',d)
    return d

def display(name):
    return NAMES.get(name,name)

def number(value, signed=False):
    return 'n/a' if value is None else (f'{value:+.2f}' if signed else f'{value:.2f}')

def render(openrouter):
    p = ROOT/'dashboard.json'
    if not p.exists():
        return '<section id="vercel"><h2>Vercel AI Gateway</h2><p>No successful collection yet. <a href="'+SOURCE+'">Open source</a>.</p></section>'
    d=read_json(p)
    e=html.escape
    age=(dt.date.today()-dt.date.fromisoformat(d['asof'])).days
    out=['<section id="vercel"><h2>Vercel AI Gateway</h2>',
         '<p class="sub">Daily shares through <b>'+e(d['asof'])+'</b> · all modalities · <a href="'+SOURCE+'">Models</a> · <a href="https://vercel.com/ai-gateway/leaderboards/labs">Labs</a> · <a href="'+DOCS+'">Methodology</a></p>']
    if age>2:
        out.append('<div class="callout warn">Vercel data is '+str(age)+' days old. Last successful data retained.</div>')
    out.append('<p>Weekly comparison: <b>'+' to '.join(d['current_period'])+'</b> versus '+' to '.join(d['previous_period'])+'. Weekly figures below are the mean of daily shares; they are not volume-weighted weekly shares.</p>')
    for dataset in ('labs','models'):
        out.append('<h3>'+('Lab' if dataset=='labs' else 'Model')+' rankings</h3><div class="grid2">')
        for metric,label in METRICS.items():
            out.append('<div class="card"><h3>'+label+'</h3><div class="scroll"><table><thead><tr><th>Name</th><th class="r">Latest %</th><th class="r">7d mean %</th><th class="r">Δ pp</th></tr></thead><tbody>')
            for row in d['datasets'][dataset][metric][:10]:
                out.append('<tr><td>'+e(display(row['name']))+'</td><td class="r">'+number(row['latest_share'])+'</td><td class="r">'+number(row['mean_7d'])+'</td><td class="r">'+number(row['change_pp'],True)+'</td></tr>')
            out.append('</tbody></table></div></div>')
        out.append('</div>')
    out.append('<p class="note">n/a = incomplete daily coverage, often because a model falls outside the published top list. It does not mean zero usage. Rankings follow the latest day.</p>')
    out.append('<h3>Lab token share across both sources</h3><p class="sub">OpenRouter text-token share (trailing 7 days, snapshot '+e(openrouter['asof'])+') versus Vercel all-modality daily token-share mean ('+' to '.join(d['current_period'])+'). Different populations, windows and aggregation; use as directional evidence.</p><div class="scroll"><table><thead><tr><th>Lab</th><th class="r">OpenRouter %</th><th class="r">Vercel 7d mean %</th></tr></thead><tbody>')
    aliases={'x-ai':'xai','z-ai':'zai','moonshotai':'moonshotai','meta':'meta'}
    vr={r['name']:r for r in d['datasets']['labs']['tokens']}
    for lab in sorted(openrouter['labs'],key=lambda r:r['token_share'],reverse=True)[:10]:
        match=vr.get(lab['author']) or vr.get(aliases.get(lab['author'],''))
        out.append('<tr><td>'+e(lab['display'])+'</td><td class="r">'+number(lab['token_share']*100)+'</td><td class="r">'+number(match['mean_7d'] if match else None)+'</td></tr>')
    out.append('</tbody></table></div><div class="callout"><b>How to read this.</b> Both sources measure traffic routed through their own gateway, not the total AI market. Vercel publishes spend shares estimated at labs’ list prices (actual bills may differ); OpenRouter dollar figures in this dashboard are our own list-price estimates with caching off. Do not combine them as revenue or market share. <b>Reach</b> is the share of teams using a model; <b>Preference</b> is the share of teams using it as their primary model by tokens. Those measures are available on the Vercel leaderboard but are not included in this JSON export.</div>')
    out.append('<p class="note">Source: Vercel AI Gateway · '+e(d['asof'])+' · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Transformed into daily-share averages and percentage-point changes. <a href="../_data/vercel/dashboard.json">Download derived data</a>.</p></section>')
    return ''.join(out)

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--offline',action='store_true');args=parser.parse_args()
    folder=None if args.offline else fetch()
    d=build(folder);print('Vercel data through',d['asof'])
