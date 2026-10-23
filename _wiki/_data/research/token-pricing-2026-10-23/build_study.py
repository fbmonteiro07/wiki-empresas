"""Reproduce the dated Ramp panel study. Python standard library only.

Outputs are confined to this study directory. Never updates company pages.
Two Ramp denominators are deliberately preserved, not calibrated into each other.
"""
import collections
import hashlib
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1]
RAW = HERE / 'raw'
RAW.mkdir(exist_ok=True)
for name in ('tokenPrices.json', 'tokenVolumes.json', 'fetch_meta.json'):
    src = DATA / 'ramp-ai-index' / ('raw' if name != 'fetch_meta.json' else '') / name
    dst = RAW / name
    if not dst.exists():
        shutil.copyfile(src, dst)

prices = json.loads((RAW / 'tokenPrices.json').read_text(encoding='utf-8'))
volumes = json.loads((RAW / 'tokenVolumes.json').read_text(encoding='utf-8'))
meta = json.loads((RAW / 'fetch_meta.json').read_text(encoding='utf-8'))
MAKERS = ('anthropic', 'openai')
SELECTED = ('2026-01-25','2026-02-22','2026-03-29','2026-04-26',
            '2026-05-31','2026-06-28','2026-07-26','2026-08-30',
            '2026-09-27','2026-10-11')

def family(maker, name):
    name = name.lower()
    if maker == 'anthropic':
        return next((f.title() for f in ('opus','sonnet','haiku','fable','mythos') if f in name), 'Other/unmapped')
    if 'embedding' in name or 'moderation' in name:
        return 'Embedding/moderation'
    if any(x in name for x in ('realtime','audio','tts','whisper','transcribe','image','sora','dall')):
        return 'Media/audio'
    if 'astra' in name:
        return 'Astra'
    if any(x in name for x in ('luna','mini','nano')):
        return 'Luna/mini/nano'
    if 'sol' in name:
        return 'Sol'
    if 'terra' in name:
        return 'Terra'
    return 'Other text/legacy'

def ratio(cost, tokens):
    return cost / tokens * 1e6 if tokens else None

keys = [(r['period_end'],r['model_maker'],r['series_key'],r['metric_key']) for r in volumes]
assert len(keys) == len(set(keys)), 'Duplicate volume rows'
assert all(r['metric_key'] in ('token_volume','token_spend') for r in volumes)
assert all(r['metric_value'] >= 0 for r in volumes)
price_index = {(r['usage_date'],r['model_maker'],r['token_type']):r for r in prices}
assert len(price_index) == len(prices), 'Duplicate price rows'

weeks = sorted({r['period_end'] for r in volumes if '2026-01-11' <= r['period_end'] <= '2026-10-11'})
results = []
for week in weeks:
    for maker in MAKERS:
        rows = [r for r in volumes if r['period_end']==week and r['model_maker']==maker]
        models = collections.defaultdict(lambda: {'token_volume':0.,'token_spend':0.})
        present = collections.defaultdict(set)
        for r in rows:
            models[r['series_key']][r['metric_key']] += r['metric_value']
            present[r['series_key']].add(r['metric_key'])
        assert all('token_volume' in p for p in present.values()), 'Spending-only record requires investigation'
        groups = collections.defaultdict(lambda: {'token_volume':0.,'token_spend':0.,'matched_tokens':0.,'matched_spend':0.,'spend_record_count':0})
        for name,m in models.items():
            m['family'] = family(maker,name)
            m['spend_reported'] = 'token_spend' in present[name]
            m['price_usable'] = m['spend_reported'] and m['token_volume']>0
            groups[m['family']]['spend_record_count'] += int(m['spend_reported'])
            m['usd_per_million_model_series_tokens'] = ratio(m['token_spend'],m['token_volume']) if m['price_usable'] else None
            for metric in ('token_volume','token_spend'):
                groups[m['family']][metric] += m[metric]
            if m['price_usable']:
                groups[m['family']]['matched_tokens'] += m['token_volume']
                groups[m['family']]['matched_spend'] += m['token_spend']
            if not m['spend_reported']:
                m['token_spend'] = None
        total_tokens = sum(m['token_volume'] for m in models.values())
        total_spend = sum(m['token_spend'] or 0 for m in models.values())
        matched_tokens = sum(g['matched_tokens'] for g in groups.values())
        matched_spend = sum(g['matched_spend'] for g in groups.values())
        for group in groups.values():
            group['token_share'] = group['token_volume']/total_tokens
            group['spend_share'] = group['token_spend']/total_spend if group['spend_record_count'] else None
            group['matched_token_share'] = group['matched_tokens']/matched_tokens
            group['usd_per_million_model_series_tokens'] = ratio(group['matched_spend'],group['matched_tokens'])
        observed = {}
        for kind in ('all_tokens','uncached_input','output'):
            r = price_index[(week,maker,kind)]
            observed[kind] = {**r, 'usd_per_million':ratio(r['token_cost_usd_7d'],r['token_count_7d'])}
        baseline = observed['all_tokens']
        direct_price = ratio(matched_spend,matched_tokens)
        weighted = sum(g['matched_token_share']*(g['usd_per_million_model_series_tokens'] or 0) for g in groups.values())
        checks = {
            'shares_sum_to_one':abs(sum(g['token_share'] for g in groups.values())-1)<1e-10,
            'weighted_identity_reconciles':abs(direct_price-weighted)<1e-10,
            'matched_token_coverage':matched_tokens/total_tokens,
            'matched_spend_coverage':matched_spend/total_spend,
            'models_without_spend_record':sum(not m['spend_reported'] for m in models.values()),
            'spend_with_zero_tokens':total_spend-matched_spend,
            'weekly_spend_gap_fraction':total_spend/baseline['token_cost_usd_7d']-1,
            'weekly_token_gap_fraction':total_tokens/baseline['token_count_7d']-1,
            'price_gap_fraction':direct_price/baseline['usd_per_million']-1,
            'external_validation':'Unavailable; these are two tables from the same provider, not independent anchors',
        }
        checks['cross_table_token_status'] = 'RED' if abs(checks['weekly_token_gap_fraction']) > .25 else 'AMBER' if abs(checks['weekly_token_gap_fraction']) > .01 else 'GREEN'
        results.append({'week_end':week,'provider':maker,'published_price_series':observed,
                        'model_series_tokens':total_tokens,'model_series_spend_usd':total_spend,
                        'matched_tokens':matched_tokens,'matched_spend_usd':matched_spend,
                        'all_row_diagnostic_spend_over_tokens':ratio(total_spend,total_tokens),
                        'model_series_usd_per_million':direct_price,'families':dict(groups),
                        'models':dict(models),'checks':checks})

last = {r['provider']:r for r in results if r['week_end']=='2026-10-11'}
first = {r['provider']:r for r in results if r['week_end']=='2026-01-25'}
sensitivities = []
for maker,from_group,to_group in [('openai','Luna/mini/nano','Astra'),('anthropic','Sonnet','Opus')]:
    r = last[maker]
    p0=r['families'][from_group]['usd_per_million_model_series_tokens']
    p1=r['families'][to_group]['usd_per_million_model_series_tokens']
    delta=.10*(p1-p0)
    sensitivities.append({'provider':maker,'tag':'ESTIMATE: hypothetical shift; not a forecast',
                         'from':from_group,'to':to_group,'token_share_shift':.10,
                         'fixed_observed_family_prices':[p0,p1], 'usd_per_million_delta':delta,
                         'relative_change':delta/r['model_series_usd_per_million'],
                         'basis':'10pp of MATCHED model-volume tokens only. Do not apply this to the published-price table or all-token mix.'})

study = {
    'prepared_on':'2026-10-23','source':'Ramp Economics Lab / Ara Kharazian',
    'model_use_status':{'updated_on':'2026-10-23','ready':False,'status':'HOLD',
                        'reason':'Live-source reconciliation confirms unresolved token denominators and unvalidated billed-revenue semantics.',
                        'evidence':'reconciliation/reconciliation.md'},
    'source_url':'https://ramp.com/data/ai-index','fetched_at':meta['fetched_at'],
    'latest_week':'2026-10-11','tags':{
        'HARD':'Raw Ramp panel numerators and denominators; exact within the published source',
        'ANCHOR':'Reported model volumes directly determine mix; reported cost directly determines panel ratios. Actual billed revenue is unvalidated.',
        'PARTIAL':'Family mappings and using the Ramp TSM business sample as a proxy for provider-wide paid API demand',
        'ESTIMATE':'A hypothetical 10pp mix shift; no claim this shift occurred or will occur'},
    'calibration':'No unknown rate guessed or arbitrary scale factor fitted. Mix is solved directly from observed model volumes. Company-wide API mix is not disclosed and cannot be calibrated independently.',
    'scope':'Ramp TSM connected-provider usage/reported-cost sample, not all Ramp customers and not either provider consolidated revenue. Includes historical data as restated in the October 14 capture; no stable-cohort claim.',
    'source_hashes':{n:hashlib.sha256((RAW/n).read_bytes()).hexdigest() for n in ('tokenPrices.json','tokenVolumes.json','fetch_meta.json')},
    'selected_week_ends':SELECTED,'history':results,'sensitivities':sensitivities,
    'selected_period_price_change':{m:last[m]['published_price_series']['all_tokens']['usd_per_million']/first[m]['published_price_series']['all_tokens']['usd_per_million']-1 for m in MAKERS},
    'limitations':[
        'Published-price denominator differs from the model-volume sum. Cause unknown; no caching, discount or tokenizer residual is inferred.',
        'No global API revenue or token-volume anchor; these outputs cannot establish company ASPs.',
        'Subscriptions, API-equivalent allowances, enterprise contracts, and revenue shares cannot be converted to dollars per token without matched usage and recognized revenue.',
        'A weighted-price identity verifies arithmetic only. It is not independent economic validation.',
        'Different model tokenizers and changing workloads mean tokens are not constant compute or constant successful tasks.',
        'Missing model spending is null, not zero: price calculations exclude unpaired volume and zero-token rows. Full token-mix calculations retain all observed volumes.',
        'Explicit zero model spending is retained as reported; it is not interpreted as a free list price.',
        'The 10pp sensitivity fixes all within-family billing rates and is a partial-equilibrium scenario.'
    ]
}
(HERE/'study.json').write_text(json.dumps(study,indent=2,ensure_ascii=False),encoding='utf-8')

md = ['# Anthropic and OpenAI token pricing: 2026 through October 23',
      '', '**2026-10-23 FOLLOW-UP — MODEL USE: HOLD.** See [denominator reconciliation](reconciliation/reconciliation.md). The initial panel observations below are preserved. Neither blended ratios nor earlier 10pp sensitivities are validated economic model inputs; reported cost is not established actual billed revenue.',
      '', 'Source: Ramp Economics Lab / Ara Kharazian, https://ramp.com/data/ai-index. Raw capture: '+meta['fetched_at']+'. Latest complete token week: October 5-11, 2026.',
      '', '**HARD:** raw source records. **ANCHOR:** reported model volumes and cost (actual billed revenue unvalidated). **PARTIAL:** provider-wide representativeness and family mapping. **ESTIMATE:** hypothetical sensitivity.',
      '', 'There is no invented input/output ratio, cache rate or discount factor. Model mix is directly anchored to observed volumes. No independent company-wide validation is available.',
      '', '## Published blended-price series', '', 'USD per million tokens; trailing seven days at selected month-end Sundays. October is partial. These are snapshots, not monthly averages.',
      '', '| Week ending | Anthropic | OpenAI |', '|---|---:|---:|']
for week in SELECTED:
    cells = [next(r for r in results if r['week_end']==week and r['provider']==m)['published_price_series']['all_tokens']['usd_per_million'] for m in MAKERS]
    md.append(f'| {week} | {cells[0]:.4f} | {cells[1]:.4f} |')
md += ['', '## Product family mix: observed panel proxy', '', 'All shares use model-volume records only. The tables are not blended with the published-price denominator. Zero-cost rows remain in the volume mix.']
for maker in MAKERS:
    md += ['', '### '+maker.title(), '', '| Family | Jan 25 token % | Jun 28 token % | Oct 11 token % | Oct 11 observed spending % | Oct 11 matched-model USD/M |','|---|---:|---:|---:|---:|---:|']
    fams = sorted(last[maker]['families'],key=lambda k:-last[maker]['families'][k]['token_share'])
    for fam in fams:
        shares=[]
        for week in ('2026-01-25','2026-06-28','2026-10-11'):
            r=next(r for r in results if r['week_end']==week and r['provider']==maker)
            shares.append(r['families'].get(fam,{}).get('token_share',0)*100)
        f=last[maker]['families'][fam]
        rate = f"{f['usd_per_million_model_series_tokens']:.4f}" if f['usd_per_million_model_series_tokens'] is not None else 'N/A'
        spend_share = f"{f['spend_share']*100:.2f}" if f['spend_share'] is not None else 'N/A: missing'
        md.append(f"| {fam} | {shares[0]:.2f} | {shares[1]:.2f} | {shares[2]:.2f} | {spend_share} | {rate} |")
md += ['', '## Reconciliation: material unresolved denominator difference', '', '| Provider, Oct 11 | Published tokens, trillion | Model-series tokens, trillion | Token difference | Published USD/M | Model-series USD/M |','|---|---:|---:|---:|---:|---:|']
for m,r in last.items():
    p=r['published_price_series']['all_tokens']
    md.append(f"| {m} | {p['token_count_7d']/1e12:.6f} | {r['model_series_tokens']/1e12:.6f} | {r['checks']['weekly_token_gap_fraction']*100:.2f}% | {p['usd_per_million']:.4f} | {r['model_series_usd_per_million']:.4f} |")
md += ['', 'Cross-table spending differs by less than 0.1% in the latest week, but token denominators do not reconcile. Anthropic is RED (>25% gap); OpenAI is AMBER (>1% gap). Do not blend the two bases or infer caching from the residual. Model-series prices use matched positive-token records; mix uses all model-volume records.',
       '', '## Worked calculation and sensitivity', '', 'For each matched model: P_i = 1,000,000 x spending_i / tokens_i. Matched-model weight w_i = tokens_i / sum(matched tokens_i). Therefore sum(w_i x P_i) = 1,000,000 x matched spending / matched tokens. This is an accounting identity, not external validation.']
for m,r in last.items():
    p=r['published_price_series']['all_tokens']
    md.append(f"\n{m}: published-price basis = ${p['token_cost_usd_7d']:,.2f} / {p['token_count_7d']:,.0f} tokens x 1,000,000 = ${p['usd_per_million']:.6f}/M. Separately, matched-model basis = ${r['matched_spend_usd']:,.2f} / {r['matched_tokens']:,.0f} x 1,000,000 = ${r['model_series_usd_per_million']:.6f}/M. Matched token coverage = {r['checks']['matched_token_coverage']*100:.3f}%; spending with zero tokens = ${r['checks']['spend_with_zero_tokens']:.2f}.")
for s in sensitivities:
    md.append(f"\nESTIMATE scenario, {s['provider']}: move 10 percentage points of MATCHED model-series tokens from {s['from']} to {s['to']}, fixed observed family rates. Delta = 0.10 x ({s['fixed_observed_family_prices'][1]:.6f} - {s['fixed_observed_family_prices'][0]:.6f}) = ${s['usd_per_million_delta']:.6f}/M ({s['relative_change']*100:.2f}%).")
md += ['', '## Guardrails', '', '- PASS: row uniqueness, nonnegative quantities, weights sum to 100%, weighted-price identity on matched records. Missing price records are excluded explicitly.',
       '- RED/AMBER: cross-table token denominators; cause unresolved.',
       '- UNAVAILABLE: independent company-wide realized-ASP and stable-cohort validation.',
       '- No stock/flow comparison: all calculations use matching seven-day flows.',
       '', '## Limitations']
md += ['- '+x for x in study['limitations']]
md += ['', '## Changelog', '', '- 2026-10-23 follow-up: original rates, mix and scenario arithmetic preserved. Updated status from qualified panel study to explicit HOLD for economic model use after live-source reconciliation. Replaced ambiguous billing terminology with reported cost; no original numerical observation overwritten. See reconciliation/reconciliation.md.']
(HERE/'calculations.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({'selected_period_price_change':study['selected_period_price_change'],'sensitivities':sensitivities,'weeks':len(weeks),'files':['study.json','calculations.md']},indent=2))
