"""Audit Ramp's two public token datasets. Stdlib; writes only beside this script.

Source records are observations, not proof of invoice revenue or token semantics.
No fitted correction factor is used. Run: py <this file>
"""
import collections
import datetime
import hashlib
import json
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / 'raw'
MAKERS = ('anthropic', 'openai')
LATEST = '2026-10-11'
NON_TEXT = ('embedding','moderation','realtime','audio','tts','whisper','transcribe','image','sora','dall')

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

prices = read(RAW / 'tokenPrices.json')
volumes = read(RAW / 'tokenVolumes.json')
px = {(r['usage_date'], r['model_maker'], r['token_type']):r for r in prices}
models = collections.defaultdict(lambda: collections.defaultdict(dict))
for row in volumes:
    models[row['period_end'],row['model_maker']][row['series_key']][row['metric_key']] = row['metric_value']

integrity = {
    'price_rows':len(prices), 'model_metric_rows':len(volumes),
    'unique_price_keys':len(px)==len(prices),
    'unique_model_metric_keys':len({(r['period_end'],r['model_maker'],r['series_key'],r['metric_key']) for r in volumes})==len(volumes),
    'all_periods_seven_calendar_days':all((datetime.date.fromisoformat(r['period_end'])-datetime.date.fromisoformat(r['period_start'])).days==6 for r in volumes),
    'all_periods_weekly_model_grain':all(r['period_grain']=='weekly' and r['dimension_type']=='model' for r in volumes),
    'live_same_as_archived':{n:read(HERE/f'{n}-response.json')==read(RAW/f'{n}.json') for n in ('tokenPrices','tokenVolumes')},
    'source_hashes':{n:hashlib.sha256((HERE/f'{n}-response.json').read_bytes()).hexdigest() for n in ('tokenPrices','tokenVolumes')},
}
assert integrity['unique_price_keys'] and integrity['unique_model_metric_keys']
assert integrity['all_periods_seven_calendar_days']
assert integrity['all_periods_weekly_model_grain']
assert all(integrity['live_same_as_archived'].values())

history = []
for (date,maker), rows in sorted(models.items()):
    if maker not in MAKERS or (date,maker,'all_tokens') not in px:
        continue
    a,u,o = [px[date,maker,k] for k in ('all_tokens','uncached_input','output')]
    N,C = a['token_count_7d'],a['token_cost_usd_7d']
    T = sum(m.get('token_volume',0) for m in rows.values())
    S = sum(m.get('token_spend',0) for m in rows.values())
    missing = {name:m['token_volume'] for name,m in rows.items() if 'token_spend' not in m and m.get('token_volume',0)>0}
    explicit_zero = sum(m.get('token_volume',0) for m in rows.values() if m.get('token_spend')==0)
    zero_token_spend = sum(m.get('token_spend',0) for m in rows.values() if not m.get('token_volume'))
    missing_tokens = sum(missing.values())
    non_text = {name:m.get('token_volume',0) for name,m in rows.items() if any(x in name.lower() for x in NON_TEXT)}
    union = sum(rows[n].get('token_volume',0) for n in set(non_text)|set(missing))
    R=N-u['token_count_7d']-o['token_count_7d']
    G=T-N
    tuples=collections.defaultdict(list)
    for name,m in rows.items():
        if m.get('token_volume',0)>0:
            tuples[(m['token_volume'],m.get('token_spend'))].append(name)
    duplicate_positive_models = [names for names in tuples.values() if len(names)>1]
    history.append({
        'week_end':date,'provider':maker,
        'price_tokens_N':N,'model_tokens_T':T,'price_cost_C':C,'model_cost_S':S,
        'token_gap_G':G,'token_gap_over_N':G/N,'token_gap_over_T':G/T,
        'spend_gap_usd':S-C,'spend_gap_fraction':S/C-1,
        'published_usd_per_million':C/N*1e6,
        'raw_model_usd_per_million':S/T*1e6,
        'matched_model_usd_per_million':(S-zero_token_spend)/(T-missing_tokens)*1e6,
        'missing_spend_tokens':missing_tokens,'models_missing_spend':missing,
        'explicit_zero_spend_tokens':explicit_zero,'zero_token_spend_usd':zero_token_spend,
        'maximum_missing_share_of_gap_if_all_excluded':missing_tokens/G if G else None,
        'gap_after_removing_all_missing_spend_tokens':G-missing_tokens,
        'gap_after_removing_all_missing_spend_tokens_over_N':(G-missing_tokens)/N,
        'non_text_name_matched_tokens':sum(non_text.values()),
        'non_text_or_missing_union_tokens':union,
        'non_text_or_missing_max_share_of_gap':union/G if G else None,
        'uncached_input_tokens_U':u['token_count_7d'], 'output_tokens_O':o['token_count_7d'],
        'unclassified_count_R':R, 'unclassified_fraction_of_N':R/N,
        'G_over_R_not_a_cache_rate':G/R if R else None,
        'duplicate_positive_model_value_pairs':duplicate_positive_models,
        'largest_model':max(rows,key=lambda n:rows[n].get('token_volume',0)),
        'largest_model_tokens':max(m.get('token_volume',0) for m in rows.values()),
        'opus_token_share_T':sum(m.get('token_volume',0) for n,m in rows.items() if 'opus' in n.lower())/T if maker=='anthropic' else None,
        'mismatched_basis_revenue_C_over_N_times_T':C/N*T,
    })

# All shifts tested on the same common 2026 weekly sample, avoiding endpoint bias.
timing = {}
for maker in MAKERS:
    sample=[r for r in history if r['provider']==maker and '2026-01-11'<=r['week_end']<='2026-10-04']
    timing[maker]=[]
    for shift in range(-7,8):
        te,ce=[],[]
        for r in sample:
            date=(datetime.date.fromisoformat(r['week_end'])+datetime.timedelta(days=shift)).isoformat()
            q=px[date,maker,'all_tokens']
            te.append(abs(r['model_tokens_T']/q['token_count_7d']-1))
            ce.append(abs(r['model_cost_S']/q['token_cost_usd_7d']-1))
        timing[maker].append({'shift_days':shift,'weeks':len(te),
                              'median_absolute_token_gap':statistics.median(te),
                              'median_absolute_spend_gap':statistics.median(ce)})

latest={r['provider']:r for r in history if r['week_end']==LATEST}
out={
    'prepared_on':'2026-10-23','latest_week_end':LATEST,
    'attribution':'Ramp Economics Lab / Ara Kharazian; public chart datasets fetched October 23, 2026; latest complete week October 5-11, 2026',
    'source_data_version':'b1ACnM4ULJjULGFdkttsRs',
    'independent_review':{'date':'2026-10-23','verdict':'Arithmetic PASS; denominator suitability FAIL; overall PARTIAL; model HOLD','file':'audit.md'},
    'grounding':{'HARD':'Raw published fields; exact as reported, not independently validated billing or token counts',
                 'DERIVED':'All ratios, sums, differences, and conditional exclusion tests use only HARD inputs',
                 'PARTIAL':'Name-based non-text classification; hypotheses about upstream accounting',
                 'ESTIMATE':'No forecast, cache rate, correction factor, or realized ASP is estimated'},
    'integrity':integrity,'latest':latest,'history':history,'timing_tests':timing,
    'guardrails':{
        'arithmetic':'PASS','date_cost_alignment':'Same-day cost alignment beats every +/-7-day shift in median absolute error',
        'same_scope_tokens':'FAIL for model use; no documented reconciliation',
        'billed_revenue_semantics':'UNVALIDATED; provider reported/estimated cost is not established realized revenue',
        'independent_provider_anchor':'UNAVAILABLE; both exports are from the same source',
        'simple_no_cache_identity':'N=U+O is rejected. Interpreting this as all-cache exclusion requires an unverified common universe and exhaustive compatible U/O definitions.',
        'simple_residual_duplication_identity':'G=R is rejected. This does not reject other cache treatments, overlapping source fields or cohort differences.',
        'partial_cache_or_connection_join':'UNRESOLVED; public exports lack necessary dimensions'},
    'model_gate':{'ready':False,'use_published_price_with_model_volume':False,
                  'use_matched_model_ratio_as_company_asp':False,'use_flat_denominator_adjustment':False,
                  'approved_use':'Descriptive source-specific panel observations only; model mix must retain its original universe'},
}
(HERE/'reconciliation.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
md=['# Ramp denominator reconciliation — 2026-10-23','',
    '**MODEL STATUS: HOLD.** Cost numerators nearly reconcile; token denominators do not. Neither published nor matched-model ratios are validated company realized ASPs. No adjustment factor has been fitted. Independent review: arithmetic PASS, denominator suitability FAIL, overall PARTIAL; see [audit](audit.md).','',
    'Source: Ramp Economics Lab / Ara Kharazian, public chart exports re-fetched October 23, 2026. Latest complete week: October 5-11. Data version `b1ACnM4ULJjULGFdkttsRs`.','',
    '**HARD** = source fields as reported. **DERIVED** = exact calculations from them. **PARTIAL** = model-name classification and accounting hypotheses. No assumed cache rate or discount.','',
    '## Same-week bridge','',
    '| Item | Anthropic | OpenAI |','|---|---:|---:|']
for label,key,fmt in [('Price-series tokens N (trillion)','price_tokens_N','T'),('Model-series tokens T (trillion)','model_tokens_T','T'),('Difference G=T-N (trillion)','token_gap_G','T'),('Difference as % of N','token_gap_over_N','pct'),('Difference as % of T','token_gap_over_T','pct'),('Price-series cost C ($)','price_cost_C','cost'),('Model-series cost S ($)','model_cost_S','cost'),('Cost difference (%)','spend_gap_fraction','pct'),('Published price C/N ($/M)','published_usd_per_million','rate'),('Matched-model ratio ($/M)','matched_model_usd_per_million','rate'),('Missing-spend model tokens (trillion)','missing_spend_tokens','T'),('Maximum share of gap these could explain (%)','maximum_missing_share_of_gap_if_all_excluded','pct'),('Gap after removing ALL missing-spend volume (trillion)','gap_after_removing_all_missing_spend_tokens','T')]:
    vals=[]
    for m in MAKERS:
        x=latest[m][key]
        vals.append(f'{x/1e12:.6f}' if fmt=='T' else f'{100*x:.4f}%' if fmt=='pct' else f'{x:,.2f}' if fmt=='cost' else f'{x:.6f}')
    md.append('| '+label+' | '+' | '.join(vals)+' |')
md += ['', 'The missing-volume subtraction is a conditional maximum, not a demonstrated source filter. Absence of spending is not evidence of free consumption. Matched-model ratios exclude those missing-spend models and positive spending with zero reported tokens.','', '## Worked Anthropic arithmetic','']
r=latest['anthropic']
md += [f"- G = {r['model_tokens_T']:,} - {r['price_tokens_N']:,} = {r['token_gap_G']:,} tokens; G/N = {r['token_gap_over_N']:.8%}.",
       f"- Published price = ${r['price_cost_C']:,.8f} / {r['price_tokens_N']:,} x 1,000,000 = ${r['published_usd_per_million']:.9f}/M.",
       f"- Matched tokens = {r['model_tokens_T']:,} - {r['missing_spend_tokens']:,}; matched cost = ${r['model_cost_S']:,.8f} - ${r['zero_token_spend_usd']:,.8f}; ratio = ${r['matched_model_usd_per_million']:.9f}/M.",
       f"- Multiplying the published rate by the model-volume count would imply ${r['mismatched_basis_revenue_C_over_N_times_T']:,.2f}, versus ${r['price_cost_C']:,.2f} of price-series cost: {r['token_gap_over_N']:.2%} excess by construction. This is a basis-error illustration, not revenue.",
       f"- Opus share is separately {r['opus_token_share_T']:.4%} of T. It is not the {r['token_gap_over_N']:.4%} denominator gap.",
       f"- {r['largest_model']} alone has {r['largest_model_tokens']:,} tokens, exceeding the entire price-series denominator N. This demonstrates incompatible totals; it does not identify the faulty series.",
       '', '## Hypotheses tested','',
       '- **Stale or differently dated downloads:** live and archived JSON records are identical, including UTF-8 labels. Both endpoints use the same live dataVersion.',
       '- **Our aggregation / top-N UI filter:** no duplicate row keys; all model records are weekly seven-day flows. Ramp frontend sums all model rows by maker and separately computes price as 1e6*cost/count. Top-N display choices do not reconcile the raw bases.',
       '- **Timing:** +/-7-day shifts on a common 39-week 2026 sample worsen median cost alignment. No shift jointly reconciles cost and tokens. Source timezone and upstream bucket rules still need confirmation.',
       '- **Missing/zero-price models:** no positive-token model has an explicit zero spending record in the latest week. Missing-spend tokens can cover at most 3.4873% of Anthropic and 4.5120% of OpenAI gaps if all are excluded from N.',
       '- **OpenAI non-text models:** removing the union of missing-spend and name-matched embedding/moderation/media models can cover only '+f"{latest['openai']['non_text_or_missing_max_share_of_gap']:.2%}"+' of its latest gap, even if every removal were justified. This is a coverage test, not an approved exclusion rule.',
       '- **Simple no-cache identity N=U+O:** fails numerically. This would reject all-cache exclusion ONLY if the cohorts matched and U/O exhaustively covered compatible non-cache categories. Those assumptions remain unverified, so caching as a broader explanation is not ruled out.',
       '- **Duplicating the entire arithmetic residual once:** G is not equal to N-uncached_input-output. This rejects that identity, not other cache treatments, nested-field overlap or different cohorts.',
       '- **Multiple provider connections, missing price-eligible usage, or upstream joins:** plausible but unverified; the exports contain no connection, customer, token-type-by-model, or inclusion flags to test these. Ramp product documentation supports separate API/Enterprise app connections, but that does not establish subscription inclusion in the Index. The frontend describes model-attributed API spend.',
       '', '## Token-type bridge (do not label the residual a measured cache rate)','',
       '| Provider | N, trillion | Uncached input U | Output O | R=N-U-O | R/N | G/R |','|---|---:|---:|---:|---:|---:|---:|']
for m,r in latest.items():
    md.append(f"| {m} | {r['price_tokens_N']/1e12:.6f} | {r['uncached_input_tokens_U']/1e12:.6f} | {r['output_tokens_O']/1e12:.6f} | {r['unclassified_count_R']/1e12:.6f} | {r['unclassified_fraction_of_N']:.2%} | {r['G_over_R_not_a_cache_rate']:.2%} |")
md += ['', 'The Claude API separately reports uncached input, cache reads, cache creation and output. In the Messages response documented under prompt caching, the cache-creation aggregate overlaps its 5-minute/1-hour subfields, so summing both would double count. The organization Usage Report example instead exposes the nested subfields without that duplicate aggregate. Ramp documents Admin API ingestion but does not disclose the precise transformation behind these exports. This illustrates a schema risk, not evidence that Ramp made that error. The public Ramp all_tokens export provides no comparable partition.','',
       '## Historical instability','', '| Week ending | Anthropic T/N-1 | OpenAI T/N-1 |','|---|---:|---:|']
for d in ('2025-12-28','2026-01-25','2026-03-29','2026-06-28','2026-07-26','2026-09-27','2026-10-11'):
    rr={x['provider']:x for x in history if x['week_end']==d}
    md.append(f"| {d} | {rr['anthropic']['token_gap_over_N']:.2%} | {rr['openai']['token_gap_over_N']:.2%} |")
md += ['', 'A flat 1.6991x correction is contradicted by history. Without a matched cohort and common token definition, the price trend cannot be attributed solely to tariff changes, cache adoption, discounts or family mix.','',
       '## What is needed to release the model hold','',
       '1. A bridge for October 5-11 by provider, model, connection/product and token type, explaining Anthropic 42.724724T -> 25.146006T and OpenAI 27.722837T -> 25.570513T.',
       '2. Exact all_tokens and token_volume definitions, including cache writes/read, aggregate-versus-subfield overlap, reasoning and media tokens, and free/early-access usage.',
       '3. Identical customer/connection filters, timezone/date rules and deduplication keys for the two exports; explicit API versus Enterprise app/Claude Code/Codex treatment.',
       '4. Whether cost means billed net revenue, pre-discount list-equivalent usage, credits valued at overage prices, or another estimate; treatment of tools and zero-token costs.',
       '5. Corrected historical series or a documented reproducible bridge, rather than a one-week factor.','',
       'Until then, retain model-family shares as source-specific volume observations; do not combine them with the published-price denominator, use a blended ASP in revenue forecasts, or carry over the earlier 10pp mix sensitivity as a validated economic result.','',
       '## Primary-source evidence','',
       '- [Ramp AI Index, Ara Kharazian](https://ramp.com/data/ai-index): TSM sample description, published chart figures; checked October 23, 2026.',
       '- [Live price export](https://ramp.com/data/ai-index/chart-data/tokenPrices?version=b1ACnM4ULJjULGFdkttsRs) and [live model export](https://ramp.com/data/ai-index/chart-data/tokenVolumes?version=b1ACnM4ULJjULGFdkttsRs): saved locally with hashes.',
       '- [Ramp public frontend bundle](https://ramp.com/_next/static/immutable/chunks/3esy_8xboh9bh.js): maker sum (offset 18327), direct cost/token price formula (offset 28614), and model-attributed API spend source label; saved locally with hash.',
       '- [Ramp AI Spend Management documentation](https://support.ramp.com/ai-token-spend-management), checked October 23: API and Enterprise app connections are separate; OpenAI API credit-plan estimates may value included/prepaid consumption at overage rates instead of actual billed spend. The documentation does not say whether the public Index uses those estimates.',
       '- [Ramp agent-tool definitions](https://agents.ramp.com/docs/reference/agent-tools): distinguishes estimated usage/cost aggregates from actual vendor spend from payment records.',
       '- [Claude token accounting](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) and [Messages Usage Report](https://platform.claude.com/docs/en/api/beta/organization/usage_report/retrieve_messages): disjoint top-level token categories and nested cache-creation subfields. No Ramp backend lineage disclosed.',
       '', '## Changelog','',
       '- 2026-10-23 follow-up: preserved the initial study and all original raw observations. Extended audit confirms live mismatch; added explicit HOLD for economic model use. Earlier matched-model rates and mix sensitivities remain arithmetic diagnostics, not approved model inputs.']
(HERE/'reconciliation.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({'integrity':integrity,'latest':latest,'files':['reconciliation.json','reconciliation.md']},indent=2))
