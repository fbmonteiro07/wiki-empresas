"""Derive import-value shares from captured official UI tables; stdlib only."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))

def num(x):
    return int(x.replace(',', ''))

def data_rows(obj, length, offset):
    return {r[0]: [num(x) for x in r[offset:]] for r in obj['rows']
            if len(r) == length and all(x.replace(',', '').isdigit() for x in r[offset:])}

wide = data_rows(read('lithium_850760_official.json'), 4, 1)
monthly = data_rows(read('bess_8507600030_monthly_official.json'), 8, 2)
annual = data_rows(read('bess_8507600030_annual_view.json'), 2, 1)
checks = {}
for label, d in [('lithium', wide), ('bess_monthly', monthly)]:
    checks[label + '_country_sums'] = all(
        sum(v[i] for k, v in d.items() if k != 'Total:') == total
        for i, total in enumerate(d['Total:']))
checks['bess_monthly_equals_annual_view'] = all(sum(v) == annual[k][0] for k, v in monthly.items())
checks['nonnegative'] = all(x >= 0 for d in [wide, monthly, annual] for v in d.values() for x in v)
out = {'input_grounding': 'HARD: official USITC DataWeb / Census values retrieved 2026-09-23',
       'equation': 'China share (%) = China customs import value / all-country customs import value * 100',
       'calibration': 'No estimated constants. This is descriptive arithmetic on reported flows, not a forecast.',
       'sensitivity': 'No assumed inputs; interpretation is sensitive to HTS scope, customs origin and valuation basis.',
       'checks': checks, 'lithium': [], 'bess_country': [], 'bess_monthly': []}
for i, period in enumerate(['2024', '2025', 'Jan-Jul 2026']):
    total, china = wide['Total:'][i], wide['China'][i]
    out['lithium'].append({'period': period, 'world_usd': total, 'china_usd': china, 'china_share_pct': china / total * 100})
total_bess = sum(monthly['Total:'])
for country, v in sorted(monthly.items(), key=lambda kv: -sum(kv[1])):
    if country != 'Total:':
        out['bess_country'].append({'country': country, 'usd': sum(v), 'share_pct': sum(v) / total_bess * 100})
out['bess_world_usd'] = total_bess
prior_ytd = data_rows(read('lithium_850760_jan_jul_2025_official.json'), 2, 1)
prior_world, prior_china = prior_ytd['Total:'][0], prior_ytd['China'][0]
out['lithium_prior_ytd'] = {'period': 'Jan-Jul 2025', 'world_usd': prior_world, 'china_usd': prior_china, 'china_share_pct': prior_china / prior_world * 100}
checks['prior_ytd_country_sum'] = sum(v[0] for k, v in prior_ytd.items() if k != 'Total:') == prior_world
prior_monthly = data_rows(read('lithium_850760_jan_jul_2025_monthly_official.json'), 9, 2)
checks['prior_ytd_monthly_equals_annual_view'] = set(prior_monthly) == set(prior_ytd) and all(sum(v) == prior_ytd[k][0] for k, v in prior_monthly.items())
checks['prior_ytd_monthly_country_sums'] = all(sum(v[i] for k, v in prior_monthly.items() if k != 'Total:') == total for i, total in enumerate(prior_monthly['Total:']))
for i, month in enumerate(['2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07']):
    total, china = monthly['Total:'][i], monthly['China'][i]
    out['bess_monthly'].append({'month': month, 'world_usd': total, 'china_usd': china, 'china_share_pct': china / total * 100})
out['historical_external_check'] = {'source': 'CRS Michael Alan Havlin, R48538, November 26, 2025; 2024 lithium-ion import share', 'reported_share_pct': 69, 'our_revised_share_pct': out['lithium'][0]['china_share_pct'], 'rounds_to_reported': round(out['lithium'][0]['china_share_pct']) == 69, 'limitation': 'Published independent compilation of the same underlying Census system; not independent customs collection.'}
assert all(checks.values()), checks
(ROOT / 'calculated_shares_and_checks.json').write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
print(json.dumps({**out, 'bess_country': out['bess_country'][:8]}, indent=2))
