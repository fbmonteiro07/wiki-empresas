"""Refresh both public gateways and write the weekly brief. No messages sent here."""
import argparse
import datetime as dt
import html
import json
import subprocess
import sys
from pathlib import Path
import vercel_gateway as vg
import gateway_charts as gc

TOOLS=Path(__file__).resolve().parent
WIKI=TOOLS.parent
OR=WIKI/'_data'/'openrouter'
REPORTS=WIKI/'_data'/'ai-gateways'
DASH=WIKI/'_dashboards'

def run(name):
    subprocess.run([sys.executable,str(TOOLS/name)],check=True)

def build_brief(errors=None):
    errors=errors or []
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    od=vg.read_json(OR/'dashboard.json')
    vd=vg.read_json(vg.ROOT/'dashboard.json') if (vg.ROOT/'dashboard.json').exists() else None
    chart_fragment=gc.publish(WIKI)
    chart_report=vg.read_json(REPORTS/'charts.json')
    errors.extend(w for w in chart_report['warnings'] if w not in errors)
    date=dt.date.fromisoformat(od['asof'])
    history=[json.loads(line) for line in (OR/'history.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    candidates=[r for r in history if r['date']<od['asof']]
    prior=min(candidates,key=lambda r:abs((date-dt.date.fromisoformat(r['date'])).days-7)) if candidates else None
    p=od['platform']
    lines=['# OpenRouter + Vercel — weekly research brief', '', 'Generated: '+now, '',
           '## OpenRouter (existing text-model scope)', '', 'Source: https://openrouter.ai/rankings · snapshot '+od['asof']+' · trailing 7-day totals.', '',
           f"- Token volume: {p['tokens_week']/1e12:.2f}T/week; requests: {p['requests_week']/1e9:.2f}B/week; free-token mix: {p['free_token_pct']*100:.1f}%.",
           f"- Estimated spend at current list prices, caching off: ${p['revenue_week']/1e6:.1f}M/week. This is a ceiling, not realized revenue."]
    oc=vg.read_json(OR/'open_closed.json') if (OR/'open_closed.json').exists() else None
    lf=(oc or {}).get('latest_full')
    if lf:
        lines.append(f"- Open-weight vs proprietary (full feed, calendar week of {lf['x']}): open-weight {lf['open']*100:.1f}%, proprietary {lf['closed']*100:.1f}%, stealth/unattributed {lf['unattributed']*100:.1f}% of tokens. Classification: Hugging Face link on the OpenRouter listing; stealth previews unattributed.")
    if prior:
        gap=(date-dt.date.fromisoformat(prior['date'])).days
        lines.append(f"- Token change versus {prior['date']}: {(p['tokens_week']/prior['tokens_week']-1)*100:+.2f}%. Snapshot interval: {gap} days"+('.' if gap==7 else '; not a strict week-over-week comparison.'))
        moves=[]
        for lab in od['labs']:
            before=prior['labs'].get(lab['author'])
            if before:
                delta=lab['token_share']*100-before['tok_wk']/prior['tokens_week']*100
                moves.append((abs(delta),lab['display'],delta,lab['token_share']*100))
        for _,name,delta,share in sorted(moves,reverse=True)[:5]:
            lines.append(f'- {name}: token share {share:.2f}%, change {delta:+.2f} pp versus {prior["date"]}.')
    else:
        lines.append('- First baseline: no prior comparable snapshot. Weekly changes are unavailable.')
    lines+=['', 'Largest models by token volume:']
    for model in sorted(od['models'],key=lambda r:r['tokens_week'],reverse=True)[:5]:
        lines.append(f"- {model['name']}: {model['tokens_week']/1e12:.2f}T tokens/week.")
    lines+=['','## Vercel AI Gateway','']
    if vd:
        lines+=['Source: '+vg.SOURCE+' · data through '+vd['asof']+' · all modalities.',
                'Comparison: '+' to '.join(vd['current_period'])+' versus '+' to '.join(vd['previous_period'])+'.',
                'Figures are unweighted means of daily shares, not shares of total weekly volume. Missing top-list rows are not zero.','']
        for dataset in ('labs','models'):
            for metric,label in vg.METRICS.items():
                rows=vd['datasets'][dataset][metric]
                covered=[r for r in rows if r['mean_7d'] is not None and r['name'].lower()!='other']
                leaders=sorted(covered,key=lambda r:r['mean_7d'],reverse=True)[:3]
                lines.append(f"{dataset.title()} — {label}: "+'; '.join(vg.display(r['name'])+' '+vg.number(r['mean_7d'])+'% ('+vg.number(r['change_pp'],True)+' pp)' for r in leaders)+'.')
                movers=sorted([r for r in covered if r['change_pp'] is not None],key=lambda r:abs(r['change_pp']),reverse=True)[:3]
                lines.append('Largest changes: '+'; '.join(vg.display(r['name'])+' '+vg.number(r['change_pp'],True)+' pp' for r in movers)+'.')
        lines+=['','Reach and Preference are not in the JSON export. Consult the source page for those adoption measures; do not infer them from token shares.']
    else:
        lines+=['No successful Vercel snapshot is available.']
    pulse=chart_report['openrouter']
    lines+=['','## Token growth and share charts (all public-feed tokens)','',
            f"- Trailing 7-day tokens: {pulse['tokens_7d']/1e12:.2f}T, window ending {pulse['asof']}; growth {gc.fmt(pulse['growth_pct'],'%',True)} versus {pulse['baseline']} ({pulse['interval_days']} days).",
            f"- Free-tagged share: {pulse['free_share_pct']:.2f}%. Other variants are not necessarily paid. This scope includes all feed tokens; text-only figures above can differ.",
            '- Ten charts: demand, growth, free mix, lab share history, lab/model movers and Vercel token-versus-estimated-spend shares.',
            '- Chart pack: '+gc.LIVE+'ai-gateways-charts.html',
            '- Email attachment: '+str(REPORTS/'exports'/(dt.date.today().isoformat()+'-ai-gateways-charts.html'))]
    lines+=['','## Interpretation and data quality','',
            '- Compare direction within each source. Neither gateway is the overall AI market; the user and workload mix differs.',
            '- Vercel spend is estimated using labs’ published list prices (actual bills may differ); OpenRouter spend is our own list-price/cache-off estimate. Neither is realized lab revenue. Methodology: https://vercel.com/blog/ai-gateway-production-index-september-2026',
            '- A new top-list appearance is not necessarily a new model launch. Verify launch and price-change claims against primary sources.',
            '- Attribution: OpenRouter public APIs and Vercel AI Gateway (CC BY 4.0); transformations are ours.']
    if (dt.date.today()-date).days>2:
        errors.append('OpenRouter snapshot is stale: '+od['asof'])
    if vd and (dt.date.today()-dt.date.fromisoformat(vd['asof'])).days>2:
        errors.append('Vercel snapshot is stale: '+vd['asof'])
    if errors:
        lines+=['','Collection issues (last good data retained):']+['- '+s for s in errors]
    md='\n'.join(lines)+'\n'
    REPORTS.mkdir(parents=True,exist_ok=True)
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')
    (REPORTS/'weekly-latest.md').write_text(md,encoding='utf-8')
    (REPORTS/(stamp+'.md')).write_text(md,encoding='utf-8')
    vg.write_json(REPORTS/'status.json',{'generated_at':now,'openrouter_asof':od['asof'],'vercel_asof':vd['asof'] if vd else None,'errors':errors})
    vg.write_json(REPORTS/'snapshots'/(od['asof']+'.json'),od)
    body=[]
    for line in lines:
        if line.startswith('# '): body.append('<h1>'+html.escape(line[2:])+'</h1>')
        elif line.startswith('## '): body.append('<h2>'+html.escape(line[3:])+'</h2>')
        elif line: body.append('<p>'+html.escape(line)+'</p>')
    page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OpenRouter + Vercel weekly brief</title><style>body{max-width:1000px;margin:40px auto;padding:0 24px;background:#0d1422;color:#e6edf7;font:16px/1.65 system-ui}h1{font-size:28px}h2{color:#81b3ff;margin-top:36px}a{color:#81b3ff}p{overflow-wrap:anywhere}</style><a href="openrouter.html">← OpenRouter + Vercel dashboard</a>'+''.join(body)+'</html>'
    page=page.replace(body[0],body[0]+chart_fragment,1)
    (DASH/'gateway-weekly.html').write_text(page,encoding='utf-8')
    return errors

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--offline',action='store_true');args=parser.parse_args()
    errors=[]
    if not args.offline:
        old_pointer=(OR/'latest.txt').read_text(encoding='utf-8')
        try:
            run('or_fetch.py')
            today=dt.date.today().isoformat()
            manifest=vg.read_json(OR/'raw'/today/'_manifest.json')
            required=('models','catalog','rank_week','rank_month','apps')
            if any(not manifest['endpoints'].get(k,{}).get('ok') for k in required):
                raise ValueError('Incomplete OpenRouter snapshot; retaining last good dashboard')
            run('or_build.py')
        except Exception as exc:
            (OR/'latest.txt').write_text(old_pointer,encoding='utf-8')
            errors.append('OpenRouter refresh: '+str(exc))
        try:
            vg.build(vg.fetch())
        except Exception as exc:
            errors.append('Vercel refresh: '+str(exc))
    if not args.offline:
        try:
            run('gpu_pricing.py')
        except Exception as exc:
            errors.append('GPU pricing refresh: '+str(exc))
    run('build_gpu_pricing.py')
    errors=build_brief(errors)
    run('build_openrouter_dash.py')
    print('Weekly brief:',REPORTS/'weekly-latest.md')
    if errors:
        print('\n'.join(errors),file=sys.stderr)
        return 1
    return 0

if __name__=='__main__':
    sys.exit(main())
