"""Vintage-matched OpenRouter token volumes, catalogue prices, WAP and spend.

Observed inputs are HARD; applying snapshot list prices to a trailing week's
usage is a PARTIAL estimate. No rate is backfilled from a later snapshot.
"""
import datetime as dt
import hashlib
import json
import math
import re
import statistics
from pathlib import Path

WIKI = Path(__file__).resolve().parents[1]
SOURCE = 'https://openrouter.ai/rankings'
PRICE_SOURCE = 'https://openrouter.ai/api/v1/models'
BANDS = ('open', 'closed', 'unknown')
LABELS = {'open': 'Open-weight', 'closed': 'Closed-weight proxy', 'unknown': 'Unclassified', 'total': 'Total'}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(path)


def nonnegative(value):
    try:
        n = float(value)
        return n if math.isfinite(n) and n >= 0 else None
    except (TypeError, ValueError):
        return None


def variant(key):
    base, _, tag = (key or '').partition(':')
    return base, tag or 'standard'


def indexes(models, catalog):
    """Only exact aliases from the same vintage; ambiguous aliases stay unknown."""
    prices, classes, average = {}, {}, {}
    def add(index, key, value):
        if key not in index:
            index[key] = value
        elif index[key] != value:
            index[key] = None
    for entry in catalog:
        slug = entry.get('permaslug') or entry.get('slug') or ''
        routing = entry.get('router') or slug.startswith(('openrouter/', 'stealth/'))
        band = 'unknown' if routing else ('open' if entry.get('hf_slug') else 'closed')
        for key in (entry.get('permaslug'), entry.get('slug')):
            if key:
                add(classes, variant(key)[0], band)
    for model in models:
        mid = model.get('id') or ''
        canonical = model.get('canonical_slug') or mid
        base, tag = variant(mid)
        arch = model.get('architecture') or {}
        router = arch.get('tokenizer') == 'Router' or base.startswith(('openrouter/', 'stealth/'))
        band = 'unknown' if router else ('open' if model.get('hugging_face_id') else 'closed')
        for key in (base, variant(canonical)[0]):
            if key:
                add(classes, key, band)
        raw = model.get('pricing') or {}
        pin, pout = nonnegative(raw.get('prompt')), nonnegative(raw.get('completion'))
        if router and (pin is None or pout is None):
            continue
        if pin is None or pout is None or 'text' not in arch.get('output_modalities', []):
            continue
        rec = {'input': pin, 'output': pout, 'cache_read': nonnegative(raw.get('input_cache_read')),
               'cache_write': nonnegative(raw.get('input_cache_write')), 'price_model_id': mid}
        # Canonical slugs can omit variant suffixes; never let :free overwrite standard.
        for key in (base, variant(canonical)[0]):
            if key:
                existing = prices.get((key, tag))
                if existing is None and (key, tag) not in prices:
                    prices[(key, tag)] = rec
                elif existing and any(existing[k] != rec[k] for k in ('input', 'output', 'cache_read')):
                    prices[(key, tag)] = None
        if tag == 'standard' and not router:
            add(average, canonical, (pin, pout))
    return prices, classes, [p for p in average.values() if p is not None]


def digest(folder):
    models = read(folder / 'models.json')['data']
    catalog = read(folder / 'catalog.json')['data']
    rows = read(folder / 'rank_week.json')['data']
    if not rows:
        raise ValueError('Empty ranking')
    manifest = folder / '_manifest.json'
    if manifest.exists():
        endpoints = read(manifest).get('endpoints', {})
        if any(endpoints.get(k, {}).get('ok') is False for k in ('models', 'catalog', 'rank_week')):
            raise ValueError('Incomplete collection manifest')
    prices, classes, average = indexes(models, catalog)
    buckets = {key: {'tokens': 0., 'priced_tokens': 0., 'input_tokens': 0., 'output_tokens': 0.,
                     'input_cost': 0., 'output_cost': 0., 'spend': 0., 'cache50': 0., 'cache70': 0.,
                     'cache_rate_tokens': 0., 'cache_eligible_input_tokens': 0., 'rows': 0} for key in (*BANDS, 'total')}
    seen, detail = set(), []
    diagnostics = {'total_usage_rows': 0, 'positive_total_usage_rows': 0, 'total_usage_raw_sum': 0.,
                   'positive_usage_free_rows': 0, 'total_usage_free_raw_sum': 0.,
                   'cached_tokens_raw_sum': 0., 'byok_tokens_raw_sum': 0.,
                   'meaning': 'Public ranking total_usage units/scope are unverified. Positive values, including on free variants, are diagnostic only; not labeled USD or used to calibrate spend. All-zero cache/BYOK counters do not establish zero actual caching/BYOK.'}
    for row in rows:
        slug = row['model_permaslug']
        base = variant(slug)[0]
        tag = row.get('variant') or 'standard'
        key = (base, tag)
        if key in seen:
            raise ValueError('Duplicate model/variant across buckets: ' + str(key))
        seen.add(key)
        pin, pout = nonnegative(row.get('total_prompt_tokens')), nonnegative(row.get('total_completion_tokens'))
        if pin is None or pout is None:
            raise ValueError('Invalid token count: ' + slug)
        tokens = pin + pout
        usage = nonnegative(row.get('total_usage'))
        if usage is not None:
            diagnostics['total_usage_rows'] += 1
            diagnostics['total_usage_raw_sum'] += usage
            diagnostics['positive_total_usage_rows'] += int(usage > 0)
            if tag == 'free':
                diagnostics['total_usage_free_raw_sum'] += usage
                diagnostics['positive_usage_free_rows'] += int(usage > 0)
        diagnostics['cached_tokens_raw_sum'] += nonnegative(row.get('total_native_tokens_cached')) or 0
        diagnostics['byok_tokens_raw_sum'] += (nonnegative(row.get('total_byok_prompt_tokens')) or 0) + (nonnegative(row.get('total_byok_completion_tokens')) or 0)
        band = classes.get(base) or 'unknown'
        rate = prices.get(key)
        if tag == 'free':
            rate = {'input': 0., 'output': 0., 'cache_read': 0., 'cache_write': 0., 'price_model_id': 'free-tagged variant'}
        input_cost = pin * rate['input'] if rate else None
        output_cost = pout * rate['output'] if rate else None
        cost = input_cost + output_cost if rate else None
        cached = rate['cache_read'] if rate and rate['cache_read'] is not None else (rate['input'] if rate else None)
        c50 = pin * (.5 * rate['input'] + .5 * cached) + output_cost if rate else None
        c70 = pin * (.3 * rate['input'] + .7 * cached) + output_cost if rate else None
        for target in (band, 'total'):
            b = buckets[target]
            b['tokens'] += tokens
            b['rows'] += 1
            if rate:
                b['priced_tokens'] += tokens
                b['input_tokens'] += pin
                b['output_tokens'] += pout
                b['input_cost'] += input_cost
                b['output_cost'] += output_cost
                b['spend'] += cost
                b['cache50'] += c50
                b['cache70'] += c70
                if rate['cache_read'] is not None:
                    b['cache_rate_tokens'] += pin
                    if rate['cache_read'] < rate['input']:
                        b['cache_eligible_input_tokens'] += pin
        detail.append({'model': slug, 'variant': tag, 'band': band, 'input_tokens': pin, 'output_tokens': pout,
                       'tokens': tokens, 'rates_usd_per_token': rate, 'spend_usd': cost,
                       'price_status': 'observed free tag' if tag == 'free' else ('same-vintage list' if rate else 'unpriced')})
    if buckets['total']['tokens'] <= 0:
        raise ValueError('Zero tokens')
    for b in buckets.values():
        b['wap'] = b['spend'] / b['priced_tokens'] * 1e6 if b['priced_tokens'] else None
        b['coverage_pct'] = b['priced_tokens'] / b['tokens'] * 100 if b['tokens'] else None
        if not b['priced_tokens']:
            b['spend'] = b['cache50'] = b['cache70'] = None
    end = max(row['date'][:10] for row in rows)
    dt.date.fromisoformat(end)
    if end >= folder.name:
        raise ValueError('Ranking includes current/future day; completed window required')
    return {'snapshot': folder.name, 'window_end': end,
            'window_start': (dt.date.fromisoformat(end) - dt.timedelta(days=6)).isoformat(),
            'buckets': buckets, 'raw_diagnostics': diagnostics, 'average': {'models': len(average),
                'input': statistics.fmean(p[0] for p in average) * 1e6 if average else None,
                'output': statistics.fmean(p[1] for p in average) * 1e6 if average else None,
                'blend': statistics.fmean((p[0] + p[1]) / 2 for p in average) * 1e6 if average else None},
            'model_detail': detail,
            'sources': {name: {'file': str((folder / (name + '.json')).relative_to(folder.parents[2])).replace('\\', '/'),
                               'sha256': hashlib.sha256((folder / (name + '.json')).read_bytes()).hexdigest()}
                        for name in ('models', 'catalog', 'rank_week')}}


def collect(wiki=WIKI):
    root = wiki / '_data/openrouter'
    pointer = (root / 'latest.txt').read_text(encoding='utf-8').strip()
    points, warnings = {}, []
    for folder in sorted((root / 'raw').glob('20*')):
        if folder.name > pointer:
            continue
        try:
            point = digest(folder)
            if point['window_end'] in points:
                warnings.append(f"{folder.name}: duplicate window ending {point['window_end']}; earliest valid price vintage preserved, later prices not substituted.")
            else:
                points[point['window_end']] = point
        except (OSError, KeyError, TypeError, ValueError) as exc:
            warnings.append(f'{folder.name}: {exc}')
    history = sorted(points.values(), key=lambda p: p['window_end'])
    if not history:
        raise ValueError('No valid matched token/price history')
    current = history[-1]
    if current['snapshot'] != pointer:
        warnings.append('Latest raw snapshot could not be processed; retained older valid observations.')
    if (dt.date.today() - dt.date.fromisoformat(current['window_end'])).days > 8:
        warnings.append('Latest token window is more than eight days old.')
    checks = []
    reconciled = all(abs(sum(p['buckets'][b]['tokens'] for b in BANDS) - p['buckets']['total']['tokens']) <= 1 for p in history)
    checks.append({'name': 'Token categories reconcile to the ranking feed', 'status': 'PASS' if reconciled else 'FAIL',
                   'kind': 'internal arithmetic; not independent validation'})
    checks.append({'name': 'Point-in-time prices and classification only', 'status': 'PASS',
                   'kind': 'Each usage window joins its own captured models and catalogue; no future-vintage backfill.'})
    # Separate aggregation endpoint: compare only an identical completed calendar week.
    chart_check = {'name': 'Weekly volume vs OpenRouter chart endpoint', 'status': 'UNAVAILABLE',
                   'kind': 'Separate aggregation from the same provider; not an external spend validation.'}
    chartfile = root / 'raw' / pointer / 'model_chart.json'
    if chartfile.exists():
        payload = read(chartfile)['data']
        for row in payload['data']:
            start = dt.date.fromisoformat(row['x'])
            end = (start + dt.timedelta(days=6)).isoformat()
            if end == current['window_end'] and row['x'] == current['window_start']:
                total = sum(float(v) for v in row['ys'].values())
                difference = (current['buckets']['total']['tokens'] / total - 1) * 100 if total else None
                chart_check.update(status='PASS' if difference is not None and abs(difference) <= 1 else 'REVIEW',
                    chart_tokens=total, ranking_tokens=current['buckets']['total']['tokens'], difference_pct=difference,
                    window_start=row['x'], window_end=end)
    checks.append(chart_check)
    coverage = current['buckets']['total']['coverage_pct']
    checks.append({'name': 'Latest token pricing coverage', 'status': 'PASS' if coverage >= 99 else 'PARTIAL',
                   'value_pct': coverage, 'kind': 'Priced-token subset / all feed tokens. Missing prices are not zero.'})
    checks.append({'name': 'Calibration to billed spend', 'status': 'UNAVAILABLE',
                   'kind': 'No comparable verified bill or realized-spend anchor. The raw total_usage field is disclosed separately with unverified units/scope; it is not silently equated to USD. No calibration factor fitted.'})
    if current['raw_diagnostics']['positive_total_usage_rows']:
        checks.append({'name': 'Raw total_usage needs a public ranking definition', 'status': 'REVIEW',
                       'kind': 'Cost-like field has positive values, including free-tagged rows. Cannot reconcile it to dollars until units, fees, variant attribution and scope are established.',
                       'raw_sum_unverified_units': current['raw_diagnostics']['total_usage_raw_sum']})
    for point in history:
        if point['buckets']['total']['coverage_pct'] < 99:
            warnings.append(f"Window ending {point['window_end']}: incomplete price coverage ({point['buckets']['total']['coverage_pct']:.2f}% of tokens). Dollar totals cover matched tokens only.")
    return {'generated_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'source': SOURCE, 'price_source': PRICE_SOURCE,
            'history_start': history[0]['window_end'], 'asof': current['window_end'], 'latest_snapshot': current['snapshot'],
            'history': history, 'checks': checks, 'warnings': warnings,
            'reference': 'User-supplied four-panel exhibit; user confirmed OpenRouter data consolidated by JPM on 2026-09-29. No report date or exact JPM calculation is assumed.',
            'method': {'volume': 'All prompt + completion tokens across every ranking bucket, by model/variant. Trailing seven-day windows; overlapping snapshots must not be summed.',
                       'scope': 'OpenRouter public traffic only; private models/endpoints and zero-data-retention traffic can be excluded. Upstream tokenizers differ, so tokens are not a constant-compute or constant-task unit.',
                       'classification': 'Same-vintage HF link = open-weight; a listed model without that link = closed-weight proxy. Routers, stealth and absent/ambiguous listings stay unclassified. This is metadata, not a license audit.',
                       'average': 'Unweighted mean of standard text-output catalogue model prices, including models with no observed usage; each model uses (input + output)/2. 50:50 is a declared index convention, not the observed token mix. Free variants, routers, negative sentinels and unavailable prices excluded; zero-price standard listings retained.',
                       'spend': 'Sum of input tokens × input list price + output tokens × output list price, using each snapshot vintage. Free-tagged variants are zero; unmatched and nonstandard variants without exact prices stay unpriced. Base price tiers only; not realized spend or a guaranteed ceiling.',
                       'wap': 'Matched list-price spend / matched prompt+completion tokens × 1,000,000. Priced free tokens remain in the denominator.',
                       'cache_sensitivity': 'Illustrative 50% and 70% input cache-read scenarios using observed cache-read rates; no change where a cache-read rate is absent. These fractions are ESTIMATE scenarios, not measured cache-hit rates. Cache writes, long-context tiers, tool/media fees, discounts and routing mix excluded.',
                       'grounding': 'HARD: captured tokens, listed prices and listing metadata. PARTIAL: snapshot-price application to the preceding week and listing-based weight classification. ESTIMATE: cache-hit scenarios. No unknown scale factor or assumed global market share.',
                       'calibration': 'No verified realized-spend anchor is available. The observable output check is completed-week tokens against the separate OpenRouter chart feed; it validates scope/units, not billing.'}}


def build(wiki=WIKI):
    report = collect(wiki)
    atomic(wiki / '_data/ai-gateways/token-economics.json', report)
    return report


if __name__ == '__main__':
    report = build()
    print(json.dumps({k: report[k] for k in ('history_start', 'asof', 'checks', 'warnings')}, indent=2))
