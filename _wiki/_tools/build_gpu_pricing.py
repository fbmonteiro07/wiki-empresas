"""Render cached GPU prices as an offline page and an embeddable dashboard tab."""
import html
import json
from pathlib import Path

from gpu_pricing import ROOT, SA_URL, SD_URL, read

DASH = Path(__file__).resolve().parents[1] / '_dashboards'

CSS = """
.gpu-monitor{--gp-bg:#0d1422;--gp-card:#141f30;--gp-line:#2b3c52;--gp-ink:#e9eff8;--gp-muted:#adbed2;color:var(--gp-ink);background:var(--gp-bg);padding:28px;border-radius:12px;font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif;scroll-margin-top:90px}
.gpu-monitor *{box-sizing:border-box}.gpu-monitor h2{font-size:26px;margin:0;color:var(--gp-ink)}.gpu-monitor h3{font-size:19px;margin:0 0 8px;color:var(--gp-ink)}
.gpu-monitor p{margin:8px 0}.gpu-monitor a{color:#83bbff}.gpu-monitor .gp-muted{color:var(--gp-muted);font-size:14px}.gpu-monitor .gp-kicker{font-size:13px;letter-spacing:.12em;color:#68d6cb;margin-bottom:8px}
.gpu-monitor .gp-header{display:flex;justify-content:space-between;gap:16px;align-items:start}.gpu-monitor .gp-unit{color:#68d6cb;white-space:nowrap;font-size:14px;padding:6px 10px;border:1px solid var(--gp-line);border-radius:5px}
.gpu-monitor .gp-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:24px 0}
.gpu-monitor .gp-card,.gpu-monitor .gp-panel{background:var(--gp-card);border:1px solid var(--gp-line);border-radius:9px;padding:20px;min-width:0}
.gpu-monitor .gp-panel{margin-top:18px}.gpu-monitor .gp-price-row{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding-top:12px}.gpu-monitor .gp-price{font:600 26px/1.2 ui-monospace,Consolas,monospace;letter-spacing:-1px;white-space:nowrap}
.gpu-monitor .gp-sd{color:#73b6ff}.gpu-monitor .gp-sa{color:#68d6cb}.gpu-monitor .gp-warning{color:#ffd78e;border-left:3px solid #d7a644;padding:9px 13px;background:#302a1e;margin:14px 0;font-size:14px}
.gpu-monitor .gp-controls{display:flex;gap:16px;flex-wrap:wrap;align-items:end;margin-bottom:16px}.gpu-monitor label{display:flex;flex-direction:column;gap:6px;color:var(--gp-muted);font-size:14px}
.gpu-monitor select,.gpu-monitor button{font:inherit;color:var(--gp-ink);background:#0e1725;border:1px solid #40546e;border-radius:6px;padding:9px 12px;min-height:42px}.gpu-monitor button{cursor:pointer;margin-left:auto;font-size:14px}.gpu-monitor select:focus-visible,.gpu-monitor button:focus-visible{outline:2px solid #73b6ff;outline-offset:3px}
.gpu-monitor .gp-chart{width:100%;min-height:230px}.gpu-monitor svg{display:block;width:100%;height:auto}.gpu-monitor .gp-legend{display:flex;gap:20px;flex-wrap:wrap;font-size:14px;margin:12px 0}.gpu-monitor .gp-dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px}
.gpu-monitor .gp-scroll{overflow-x:auto}.gpu-monitor table{width:100%;border-collapse:collapse;font-size:14px;white-space:nowrap;color:var(--gp-ink);background:none}.gpu-monitor th,.gpu-monitor td{text-align:left;padding:12px 10px;border-bottom:1px solid var(--gp-line);background:none}.gpu-monitor th{font-size:13px;color:var(--gp-muted)}.gpu-monitor tbody tr:hover{background:#1b2b40}.gpu-monitor .gp-num{text-align:right;font-variant-numeric:tabular-nums}.gpu-monitor details{margin-top:18px}.gpu-monitor summary{cursor:pointer;color:#83bbff;font-size:15px}.gpu-monitor .gp-hover{min-height:26px;color:var(--gp-muted);font-size:14px;overflow-wrap:anywhere}.gpu-monitor .gp-method{max-width:1000px}
@media(max-width:760px){.gpu-monitor{padding:16px}.gpu-monitor .gp-grid{grid-template-columns:1fr}.gpu-monitor .gp-header{display:block}.gpu-monitor .gp-unit{display:inline-block;margin-top:10px}.gpu-monitor .gp-panel{padding:12px}.gpu-monitor button{margin-left:0}.gpu-monitor .gp-controls{gap:12px}.gpu-monitor h2{font-size:23px}}
"""

JS = r"""
(()=>{'use strict';
const root=document.getElementById('gpu-pricing');if(!root)return;
const data=JSON.parse(root.querySelector('.gp-data').textContent);
const query=s=>root.querySelector(s), esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const dollar=v=>'$'+v.toFixed(2), stamp=d=>Date.parse(d+'T00:00:00Z');
const colors=['#73b6ff','#68d6cb','#e4b9ff'];
function selected(){
 const gpu=query('[data-filter="gpu"]').value, channel=query('[data-filter="source"]').value;
 return data.series.filter(s=>s.gpu===gpu && (channel==='bbg'?s.channel==='Bloomberg Desktop API':channel==='public'?s.channel==='Public API':s.publisher==='Silicon Data'||s.channel==='Public API'));
}
function name(s){return s.publisher+' · '+(s.channel==='Public API'?'public':s.ticker);}
function windowed(series){
 const range=query('[data-filter="range"]').value;
 const dates=series.flatMap(s=>s.points.map(p=>stamp(p[0])));
 const last=Math.max(...dates), first=range==='all'?Math.min(...dates):last-Number(range)*86400000;
 return {first,last,series:series.map(s=>({...s,points:s.points.filter(p=>stamp(p[0])>=first)}))};
}
function draw(){
 const chosen=selected();
 if(!chosen.length){query('.gp-chart').innerHTML='<p>No observations are available for this selection.</p>';query('.gp-legend').innerHTML='';query('.gp-hover').textContent='';return;}
 const w=windowed(chosen), values=w.series.flatMap(s=>s.points.map(p=>p[1]));
 if(!values.length){query('.gp-chart').innerHTML='<p>No observations in this window.</p>';return;}
 const W=1080,H=340,L=60,R=25,T=18,B=42, hi=Math.max(...values)*1.12;
 const X=d=>L+(stamp(d)-w.first)/Math.max(w.last-w.first,86400000)*(W-L-R),Y=v=>H-B-v/hi*(H-T-B);
 let svg=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="GPU rental price history in US dollars per GPU-hour"><title>${esc(query('[data-filter="gpu"]').value)} GPU rental benchmarks</title>`;
 for(let k=0;k<=4;k++){let v=hi*k/4,y=Y(v);svg+=`<line x1="${L}" x2="${W-R}" y1="${y}" y2="${y}" stroke="#2b3c52"/><text x="${L-12}" y="${y+5}" fill="#adbed2" font-size="14" text-anchor="end">${dollar(v)}</text>`;}
 for(let k=0;k<=4;k++){const d=new Date(w.first+(w.last-w.first)*k/4).toISOString().slice(0,10),x=X(d);svg+=`<text x="${x}" y="${H-10}" fill="#adbed2" font-size="14" text-anchor="${k===0?'start':k===4?'end':'middle'}">${d}</text>`;}
 w.series.forEach((s,i)=>{let path='',prev=null;for(const p of s.points){const gap=prev && stamp(p[0])-stamp(prev)>7*86400000;path+=(!prev||gap?'M':'L')+X(p[0]).toFixed(2)+','+Y(p[1]).toFixed(2)+' ';prev=p[0];}svg+=`<path d="${path}" fill="none" stroke="${colors[i]}" stroke-width="2.5" ${i===2?'stroke-dasharray="5 4"':''}/>`;if(s.points.length){const p=s.points.at(-1);svg+=`<circle cx="${X(p[0])}" cy="${Y(p[1])}" r="4" fill="${colors[i]}"><title>${esc(name(s)+' · '+p[0]+' · '+dollar(p[1]))}</title></circle>`;}});
 svg+='</svg>';query('.gp-chart').innerHTML=svg;
 query('.gp-legend').innerHTML=w.series.map((s,i)=>`<span><i class="gp-dot" style="background:${colors[i]}"></i>${esc(name(s))}</span>`).join('');
 query('.gp-hover').textContent='Move over the chart for dated observations. Gaps over seven days are left open.';
 query('.gp-chart svg').addEventListener('pointermove',event=>{const rect=event.currentTarget.getBoundingClientRect(),fraction=Math.max(0,Math.min(1,((event.clientX-rect.left)/rect.width*W-L)/(W-L-R))),when=w.first+fraction*(w.last-w.first);query('.gp-hover').textContent=w.series.map(s=>{const closest=s.points.reduce((a,b)=>!a||Math.abs(stamp(b[0])-when)<Math.abs(stamp(a[0])-when)?b:a,null);return closest?name(s)+': '+dollar(closest[1])+' ('+closest[0]+')':name(s)+': no observations';}).join(' | ');});
}
function contracts(){
 const rows=data.contracts;if(!rows.length)return;
 const W=1080,H=280,L=60,R=25,T=20,B=45, hi=Math.max(...rows.flatMap(r=>r.one_year||[]))*1.15;
 const X=i=>L+(i+.5)/rows.length*(W-L-R),Y=v=>H-B-v/hi*(H-T-B);
 let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="H100 one-year contract price ranges by reported period"><title>SemiAnalysis H100 one-year contract survey, 25th to 75th percentile</title>`;
 for(let k=0;k<=4;k++){const v=hi*k/4,y=Y(v);s+=`<line x1="${L}" x2="${W-R}" y1="${y}" y2="${y}" stroke="#2b3c52"/><text x="${L-12}" y="${y+5}" fill="#adbed2" font-size="14" text-anchor="end">${dollar(v)}</text>`;}
 rows.forEach((r,i)=>{const x=X(i);if(r.one_year){const [lo,hi]=r.one_year;s+=`<g><title>${esc(r.period+': '+dollar(lo)+'–'+dollar(hi)+' / GPU-hour')}</title><line x1="${x}" x2="${x}" y1="${Y(lo)}" y2="${Y(hi)}" stroke="#68d6cb" stroke-width="10" stroke-linecap="round"/></g>`;}else{s+=`<text x="${x}" y="${H-B-8}" fill="#adbed2" font-size="16" text-anchor="middle">—</text>`;}if(i%3===0||i===rows.length-1)s+=`<text x="${x}" y="${H-10}" fill="#adbed2" font-size="13" text-anchor="middle">${esc(r.period)}</text>`;});
 query('.gp-contract-chart').innerHTML=s+'</svg>';
}
query('[data-export]').addEventListener('click',()=>{
 const rows=[['Date','GPU','Publisher','Channel','Bloomberg ticker','Pricing basis','USD per GPU-hour','Retrieved UTC','Source URL']];
 for(const s of windowed(selected()).series)for(const p of s.points)rows.push([p[0],s.gpu,s.publisher,s.channel,s.ticker||'',s.basis,p[1],s.fetched_at,s.source_url]);
 const csv=rows.map(r=>r.map(v=>'"'+String(v).replace(/"/g,'""')+'"').join(',')).join('\r\n');
 const url=URL.createObjectURL(new Blob(['\ufeff'+csv],{type:'text/csv;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download='gpu-pricing-'+query('[data-filter="gpu"]').value+'.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
root.querySelectorAll('[data-filter]').forEach(e=>e.addEventListener('change',draw));
// Age is evaluated when opened, including offline copies retained for weeks.
root.querySelectorAll('[data-asof]').forEach(el=>{const age=Math.floor((Date.now()-stamp(el.dataset.asof))/86400000),limit=Number(el.dataset.limit||7);if(age>limit){el.classList.add('gp-warning');el.textContent+=' · '+age+' days old';}});
draw();contracts();
})();
"""


def dataset():
    bbg = read(ROOT / 'bloomberg.json', {'series': []})
    public = read(ROOT / 'semianalysis.json', {'series': [], 'contracts': []})
    return {'series': bbg['series'] + public['series'], 'contracts': public['contracts'],
            'status': read(ROOT / 'status.json', {'attempted_at': 'Never', 'errors': []})}


def price(value):
    return '${:.2f}'.format(value)


def render_fragment():
    data = dataset()
    e = html.escape
    cards = []
    for gpu in ('H100', 'A100', 'B200'):
        rows = ['<div class="gp-card"><h3>' + gpu + '</h3>']
        for publisher, channel, cls in [('Silicon Data', 'Bloomberg Desktop API', 'gp-sd'),
                                        ('SemiAnalysis', 'Public API', 'gp-sa')]:
            item = next((s for s in data['series'] if s['gpu'] == gpu and s['publisher'] == publisher and s['channel'] == channel), None)
            rows.append('<div class="gp-price-row"><span class="' + cls + '">' + publisher +
                        '</span><span class="gp-price">' + (price(item['points'][-1][1]) if item else '—') + '</span></div>')
            if item:
                rows.append('<p class="gp-muted" data-asof="' + item['points'][-1][0] + '">' +
                            e(item.get('ticker', 'Public composite')) + ' · ' + item['points'][-1][0] + '</p>')
            else:
                rows.append('<p class="gp-muted">No successful collection</p>')
        rows.append('</div>'); cards.append(''.join(rows))
    rows = []
    for item in data['series']:
        date, value = item['points'][-1]
        rows.append('<tr><td>' + e(item['gpu']) + '</td><td><a href="' + e(item['source_url']) + '">' + e(item['publisher']) +
                    '</a></td><td>' + e(item.get('ticker', 'Public API')) + '</td><td>' + e(item['basis']) +
                    '</td><td class="gp-num">' + price(value) + '</td><td data-asof="' + date + '">' + date +
                    '</td><td>' + item['points'][0][0] + '</td></tr>')
    contract_rows = []
    for row in reversed(data['contracts']):
        def band(values):
            return '–'.join(price(x) for x in values) if values else 'Not published'
        contract_rows.append('<tr><td>' + e(row['period']) + '</td><td class="gp-num">' + band(row['one_year']) +
                             '</td><td class="gp-num">' + ('Sold out' if row['sold_out'] else band(row['on_demand'])) + '</td></tr>')
    contracts = [r for r in data['contracts'] if r['one_year']]
    contract_latest = contracts[-1] if contracts else None
    contract_date = ('<p class="gp-muted" data-asof="' + contract_latest['date'] + '" data-limit="100">Latest contract survey: ' +
                     e(contract_latest['period']) + ' · ' + '–'.join(price(x) for x in contract_latest['one_year']) +
                     ' / GPU-hour for one year</p>') if contract_latest else '<p>No contract history available.</p>'
    issues = ''.join('<p class="gp-warning">Last good data retained. ' + e(err) + '</p>' for err in data['status']['errors'])
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':'), allow_nan=False).replace('<', '\\u003c')
    return f'''<style>{CSS}</style><section class="gpu-monitor" id="gpu-pricing">
<div class="gp-header"><div><div class="gp-kicker">COMPUTE MARKETS</div><h2>GPU rental pricing</h2><p class="gp-muted">Bloomberg benchmarks &amp; SemiAnalysis public indices</p></div><span class="gp-unit">USD / GPU-hour</span></div>
<p class="gp-muted">Collection attempted {e(data['status']['attempted_at'])} · <a href="gpu-pricing.html">Open full pricing tab</a> · <a href="index.html">Dashboard hub</a></p>{issues}
<div class="gp-grid">{''.join(cards)}</div>
<p class="gp-muted gp-method"><b>Different pricing baskets.</b> Silicon Data standardizes rental terms and configurations into a non-hyperscale benchmark. SemiAnalysis combines spot and contract inputs with a different provider mix. Compare each series over time; the gap between publishers is not a like-for-like discount.</p>
<div class="gp-panel"><div class="gp-controls">
<label>GPU<select data-filter="gpu"><option>H100</option><option>A100</option><option>B200</option></select></label>
<label>Source<select data-filter="source"><option value="both">Both publishers</option><option value="bbg">Bloomberg only</option><option value="public">SemiAnalysis public</option></select></label>
<label>History<select data-filter="range"><option value="90">3 months</option><option value="180">6 months</option><option value="365" selected>1 year</option><option value="all">All available</option></select></label>
<button type="button" data-export>Download selected data ↓</button></div>
<div class="gp-chart"></div><div class="gp-legend"></div><div class="gp-hover" aria-live="polite"></div>
<noscript><p>Enable JavaScript for charts and filters. Prices and the source tables below remain available.</p></noscript></div>
<div class="gp-panel"><h3>Latest observations</h3><p class="gp-muted">Daily PX_LAST history from Bloomberg; dated observations from the public API. The SemiAnalysis H100 Bloomberg series and public series share a publisher, so they are not independent signals.</p>
<div class="gp-scroll"><table><thead><tr><th>GPU</th><th>Publisher</th><th>Delivery / ticker</th><th>Pricing basis</th><th class="gp-num">$/GPU-hour</th><th>Observation date</th><th>History starts</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></div>
<div class="gp-panel"><h3>H100 · one-year contract ranges</h3>{contract_date}
<p class="gp-muted">SemiAnalysis survey · 25th–75th percentile · typically 25% prepayment. Each bar is one reported period; periods have different lengths. Missing ranges stay blank.</p>
<div class="gp-contract-chart"></div><details><summary>View contract survey observations</summary><div class="gp-scroll"><table><thead><tr><th>Reported period</th><th class="gp-num">One-year range ($/GPU-hour)</th><th class="gp-num">On-demand survey ($/GPU-hour)</th></tr></thead><tbody>{''.join(contract_rows)}</tbody></table></div></details></div>
<details class="gp-method"><summary>Sources and methodology</summary>
<p class="gp-muted"><a href="{SD_URL}">Silicon Data</a> indices are delivered through the local Bloomberg Terminal: SDH100RT, SDA100RT and SDB200RT, field PX_LAST. <a href="{SA_URL}">SemiAnalysis</a> publishes its H100, A100 and B200 spot-contract composites and the public H100 one-year survey. SAH100SC is the H100 composite delivered through Bloomberg.</p>
<p class="gp-muted">The public API supplies dated daily observations. We retain those values without filling missing days or smoothing. Bloomberg and public delivery times can differ. Contract period dates identify the reporting period, not a trading-day close. Older observations and publisher revisions remain in archived source snapshots. No access to subscriber-only GPU contract data is used.</p>
<p class="gp-muted">Snapshots remain available offline. Collection failures retain the last good source and display a warning. Daily observations older than seven calendar days are marked as old when the page opens.</p></details>
<script type="application/json" class="gp-data">{payload}</script></section><script>{JS}</script>'''


def publish():
    fragment = render_fragment()
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GPU pricing | Capstone</title>
<style>body{margin:0;background:#0d1422;color:#e9eff8;font:16px/1.5 system-ui}main{max-width:1320px;margin:0 auto;padding:18px}nav{border-bottom:1px solid #2b3c52;padding:16px 28px;display:flex;gap:24px;flex-wrap:wrap}nav a{color:#adbed2;text-decoration:none;font-size:15px}nav a[aria-current]{color:#68d6cb}nav a:hover{color:white}@media(max-width:600px){main{padding:0}nav{padding:14px 16px;gap:16px}}</style></head><body>
<nav aria-label="AI dashboards"><a href="index.html">All dashboards</a><a href="openrouter.html">OpenRouter</a><a href="openrouter.html#vercel">Vercel</a><a href="gpu-pricing.html" aria-current="page">GPU pricing</a></nav><main>''' + fragment + '</main></body></html>'
    DASH.mkdir(parents=True, exist_ok=True)
    (DASH / 'gpu-pricing.html').write_text(page, encoding='utf-8')
    print('Wrote', DASH / 'gpu-pricing.html')


if __name__ == '__main__':
    publish()
