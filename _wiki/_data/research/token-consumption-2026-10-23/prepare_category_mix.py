"""Read-only source preparation; XLSX authoring is performed by artifact-tool."""
import collections, datetime, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
source = HERE.parent / 'token-pricing-2026-10-23/raw/tokenPrices.json'
raw = json.loads(source.read_text(encoding='utf8'))
base = json.loads((HERE / 'model_inputs.json').read_text(encoding='utf8'))
lookup = {(r['usage_date'], r['model_maker'], r['token_type']): r for r in raw}
weekly = []
for old in base['weekly']:
    row = {'date': old['date'], 'provider': old['provider'], 'month': old['month']}
    for category, prefix in [('all_tokens', 'all'), ('uncached_input', 'input'), ('output', 'output')]:
        q = lookup[old['date'], old['provider'], category]
        row[prefix+'_tokens'] = q['token_count_7d']
        row[prefix+'_cost'] = q['token_cost_usd_7d']
    assert row['all_tokens'] == old['N'] and row['all_cost'] == old['C']
    row['residual_tokens'] = row['all_tokens'] - row['input_tokens'] - row['output_tokens']
    row['residual_cost'] = row['all_cost'] - row['input_cost'] - row['output_cost']
    assert min(row[k] for k in row if k.endswith(('_tokens', '_cost'))) >= 0, row
    weekly.append(row)

monthly = []
for provider in ('anthropic', 'openai'):
    for month in range(1, 13):
        selected = [r for r in weekly if r['provider'] == provider and r['month'] == min(month, 10)]
        d = {'provider': provider, 'month': month, 'source_month': min(month, 10), 'weeks': len(selected)}
        for prefix in ('all', 'input', 'output', 'residual'):
            for unit in ('tokens', 'cost'):
                key = prefix+'_'+unit
                d[key] = sum(r[key] for r in selected)
        for prefix in ('input', 'output', 'residual'):
            d[prefix+'_share'] = d[prefix+'_tokens']/d['all_tokens']
            d[prefix+'_rate'] = d[prefix+'_cost']/d[prefix+'_tokens']*1e6
            d[prefix+'_contribution'] = d[prefix+'_share']*d[prefix+'_rate']
        d['base_price'] = sum(d[p+'_contribution'] for p in ('input', 'output', 'residual'))
        assert abs(d['base_price']-d['all_cost']/d['all_tokens']*1e6) < 1e-12
        d['five_pp_residual_to_input_price'] = d['base_price'] + .05*(d['input_rate']-d['residual_rate'])
        d['one_pp_residual_to_output_price'] = d['base_price'] + .01*(d['output_rate']-d['residual_rate'])
        monthly.append(d)

data = {'asof': '2026-10-23', 'source': str(source), 'weekly': weekly, 'monthly': monthly,
        'tags': {'raw': 'HARD: exact Ramp panel observations, not company traffic',
                 'benchmark': 'ANCHOR: Ramp panel cost / all-token count',
                 'residual': 'PARTIAL: cache / other residual, not verified cache reads',
                 'company_transfer': 'PARTIAL: panel representativeness and recognized revenue unvalidated',
                 'forecast': 'ESTIMATE: October held flat for November/December'},
        'method': 'Price = input share * input rate + output share * output rate + residual share * residual rate. Residual counts = all - input - output; residual cost = all - input - output. This is an internal accounting bridge, not independent validation or evidence of a physical cache hit rate.'}
(HERE/'category_mix_inputs.json').write_text(json.dumps(data, indent=2), encoding='utf8')
print(json.dumps({'weekly_rows': len(weekly), 'monthly_rows': len(monthly), 'october': [r for r in monthly if r['month'] == 10]}, indent=2))
