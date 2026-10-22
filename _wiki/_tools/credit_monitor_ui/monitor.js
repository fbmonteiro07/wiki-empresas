
(() => {
'use strict';
const day = s => Date.parse(s + 'T00:00:00Z') / 86400000;
const iso = n => new Date(n * 86400000).toISOString().slice(0, 10);
function windowStart(end, period) {
  const d = new Date(end + 'T00:00:00Z'), originalDay = d.getUTCDate();
  d.setUTCDate(1);
  d.setUTCMonth(d.getUTCMonth() - ({'1M':1,'3M':3,'6M':6,'1Y':12}[period] || 12));
  const last = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth()+1, 0)).getUTCDate();
  d.setUTCDate(Math.min(originalDay, last));
  return d.toISOString().slice(0, 10);
}
function prepare(s, start, end, mode) {
  if (!s) return null;
  const points = s.points.filter(p => p[0] <= end && Number.isFinite(p[1]));
  const visible = points.filter(p => p[0] >= start);
  if (!visible.length) return null;
  let base = null;
  if (mode === 'change') {
    base = points.filter(p => p[0] <= start).at(-1);
    if (!base || day(start) - day(base[0]) > 4) return null;
  }
  return {instrument:s, baseDate:base && base[0], points:visible.map(p =>
    [p[0], mode === 'change' ? (p[1] - base[1]) * (s.unit === '%' ? 100 : 1) : p[1], p[1]])};
}
globalThis.CreditChart = {windowStart, prepare};
if (typeof document === 'undefined') return;
const data = JSON.parse(document.getElementById('credit-data').textContent);
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const format = (v, digits=1) => v == null ? '—' : Number(v).toLocaleString('en-US', {minimumFractionDigits:digits, maximumFractionDigits:digits});
const signed = v => (v > 0 ? '+' : v < 0 ? '−' : '') + format(Math.abs(v),1);
const dateLabel = (v, year=false) => v ? new Date(v+'T00:00Z').toLocaleDateString('en-US',{month:'short',day:'numeric',...(year?{year:'numeric'}:{}),timeZone:'UTC'}) : '';
const tone = v => v > 0 ? 'up' : v < 0 ? 'down' : 'muted';
const issuers = data.issuers;
issuers.forEach((issuer, index) => { issuer.color = 'var(--series-'+(index%8+1)+')'; });
function syncTheme() {
  const dark=document.documentElement.dataset.theme==='dark';
  $('#theme-toggle').setAttribute('aria-pressed',String(dark));
  $('#theme-toggle').setAttribute('aria-label','Switch to '+(dark?'light':'dark')+' theme');
  $('#theme-label').textContent=dark?'Light mode':'Dark mode';
}
$('#theme-toggle').addEventListener('click',()=>{
  const theme=document.documentElement.dataset.theme==='dark'?'light':'dark';
  document.documentElement.dataset.theme=theme;
  try{localStorage.setItem('capstone-credit-theme',theme);}catch{}
  syncTheme();
});
syncTheme();
const state = {metric:'cds', mode:'level', period:'1Y', universe:'focus', search:'', sort:null, direction:-1, expanded:null,
  selected:new Set(issuers.filter(x=>x.focus).map(x=>x.id)), main:Object.fromEntries(issuers.map(x=>[x.id,x.main])), converts:false};
const universe = () => issuers.filter(x=>state.universe==='all' || x.focus);
const mainBond = c => c.bonds.find(b=>b.id===state.main[c.id]) || null;
const source = s => s ? 'Bloomberg · '+(s.ticker || 'configured ticker: '+s.candidate)+' · '+s.field+(s.date?' · observation '+s.date:' · no observation') : 'No 5Y CDS configured';
function bondLabel(b) {
  if (!b) return 'No bond configured';
  const a=b.board;
  return format(a.cpn, Math.min(3,(String(a.cpn).split('.')[1]||'').length))+'% · '+dateLabel(a.mty,true);
}
function quote(s, isCDS=false) {
  if(s?.validationWarning)return '<span class="quote missing" title="'+esc(s.validationWarning)+'">—</span><small class="quote-date stale" title="'+esc(s.validationWarning)+'">Under review</small>';
  if (!s || s.last == null) return '<span class="quote missing">—</span><small class="quote-date">'+(!s?'Not configured':'No quote')+'</small>';
  return '<span class="quote" title="'+esc(source(s))+'">'+format(s.last,isCDS?1:2)+'</span><small class="quote-date '+(s.status==='stale'?'stale':'')+'">'+dateLabel(s.date)+(s.status==='stale'?' · stale':'')+'</small>';
}
function delta(s, days) {
  const d=s && s.changes[String(days)];
  if (!d) return '<span class="muted" title="Insufficient matching history">—</span>';
  return '<span class="delta '+tone(d.value)+'" title="'+esc(source(s)+' · '+d.start+' → '+d.end)+'">'+signed(d.value)+'</span>';
}
function bondDaily(b) {
  const change=b?.changes['1'];
  return change?'<small class="quote-date bond-daily">'+delta(b,1)+' bp · 1D</small>':'';
}
function kind(b) {
  const k=b.board.kind;
  return ({senior:'Senior unsecured',secured:'Senior secured',project:'Project bond',convertible:'Convertible'}[k]||k)+' · '+(b.board.ccy||'USD');
}
function details(c) {
  const rows=c.bonds.map(b=>'<tr class="'+(b.id===state.main[c.id]?'selected':'')+'"><td><input type="radio" name="main-'+esc(c.id)+'" data-bond-company="'+esc(c.id)+'" value="'+esc(b.id)+'" aria-label="Use '+esc(b.label)+' as main bond" '+(b.id===state.main[c.id]?'checked':'')+'></td><td><b>'+esc(bondLabel(b))+'</b><small class="quote-date">'+esc(kind(b))+'</small></td><td class="number">'+quote(b)+'</td><td class="number">'+delta(b,1)+'</td><td class="number">'+delta(b,7)+'</td><td class="number">'+delta(b,30)+'</td><td class="bond-source">'+esc(source(b))+'</td></tr>').join('');
  return '<tr class="detail-row" id="detail-'+esc(c.id)+'"><td colspan="8"><div class="issuer-detail"><div class="detail-heading"><div><h3>'+esc(c.name)+' · '+c.bonds.length+' bonds</h3><p>'+esc(c.cds?source(c.cds):'No 5-year CDS is configured for this company.')+'</p></div><button type="button" data-compare="'+esc(c.id)+'">Show company in chart ↑</button></div><div class="table-scroll"><table class="bond-table"><thead><tr><th>Main</th><th>Bond · maturity</th><th class="number">YTM %</th><th class="number">Δ 1D bp</th><th class="number">Δ 1W bp</th><th class="number">Δ 1M bp</th><th>Source · observation</th></tr></thead><tbody>'+rows+'</tbody></table></div><p class="detail-note">Choose a main bond to update the watchlist and comparison. '+(c.bonds.some(b=>b.board.kind==='convertible')?'Convertible yields include an equity option and are labeled separately.':'')+'</p></div></td></tr>';
}
function sortValue(c) {
  if(state.sort==='name') return c.name;
  if(state.sort==='cds') return c.cds?.last ?? null;
  if(state.sort==='yield') return mainBond(c)?.last ?? null;
  return c.cds?.changes[state.sort]?.value ?? null;
}
function renderTable() {
  let rows=universe().filter(c=>(c.id+' '+c.name).toLowerCase().includes(state.search.toLowerCase().trim()));
  if(state.sort) rows.sort((a,b)=>{
    const va=sortValue(a),vb=sortValue(b);
    if(va==null && vb==null)return 0;if(va==null)return 1;if(vb==null)return -1;
    return (typeof va==='string'?va.localeCompare(vb):va-vb)*state.direction;
  });
  $('#company-count').textContent=rows.length;
  $('#no-companies').hidden=rows.length>0;
  $('#issuer-rows').innerHTML=rows.map(c=>{
    const b=mainBond(c),open=state.expanded===c.id;
    const badge=b?.board.kind==='convertible'?'<span class="bond-tag">CONVERT.</span>':'';
    return '<tr class="issuer-row '+(open?'open':'')+'" data-company="'+esc(c.id)+'"><td><div class="issuer-name"><span class="issuer-avatar" style="--series:'+c.color+'">'+esc(c.id.slice(0,2))+'</span><div><b>'+esc(c.name)+'</b><small>'+esc(c.id)+'</small></div></div></td><td class="number">'+quote(c.cds,true)+'</td><td class="number">'+delta(c.cds,1)+'</td><td class="number">'+delta(c.cds,7)+'</td><td class="number">'+delta(c.cds,30)+'</td><td class="bond-column"><div class="bond-name">'+esc(bondLabel(b))+badge+'<small>'+esc(b?kind(b):'')+'</small></div></td><td class="number">'+quote(b)+bondDaily(b)+'</td><td><button type="button" id="toggle-'+esc(c.id)+'" class="row-toggle" aria-label="'+(open?'Collapse':'Expand')+' '+esc(c.name)+' bonds" aria-expanded="'+open+'" '+(open?'aria-controls="detail-'+esc(c.id)+'"':'')+'>'+(open?'−':'+')+'</button></td></tr>'+(open?details(c):'');
  }).join('');
  $$('[data-sort]').forEach(button=>{
    const active=button.dataset.sort===state.sort;
    button.closest('th').setAttribute('aria-sort',active?(state.direction===1?'ascending':'descending'):'none');
    button.querySelector('span').textContent=active?(state.direction===1?'↑':'↓'):'↕';
  });
}
function eligibility(c) {
  const s=state.metric==='cds'?c.cds:mainBond(c);
  if(!s)return {s:null,reason:state.metric==='cds'?'No CDS configured':'No main bond'};
  if(s.validationWarning)return {s,reason:s.validationWarning};
  if(state.metric==='yield' && s.board.ccy!=='USD')return {s,reason:'USD comparison only'};
  if(state.metric==='yield' && s.board.kind==='convertible' && !state.converts)return {s,reason:'Enable convertible bonds to compare'};
  return {s,reason:null};
}
function renderChips() {
  $('#company-filters').innerHTML=universe().map(c=>{
    const {s,reason}=eligibility(c),active=state.selected.has(c.id),missing=!s?.points.length;
    return '<button type="button" class="company-chip" data-select="'+esc(c.id)+'" style="--series:'+c.color+'" aria-pressed="'+(active&&!reason)+'" '+(reason?'disabled':'')+' title="'+esc(reason||((missing?'Awaiting history · ':'')+(s?source(s):'')))+'"><i></i>'+esc(c.id)+(reason?'<small>—</small>':missing?'<small>pending</small>':'')+'</button>';
  }).join('');
}
let chartState=null;
function hideTooltip() { $('#chart-tooltip').hidden=true; $('#chart-cross')?.setAttribute('visibility','hidden'); }
function renderChart() {
  hideTooltip();
  renderChips();
  $('#convert-control').hidden=state.metric!=='yield';
  $('#comparison-title').textContent=state.metric==='cds'?'5-year CDS spreads':'Main bond yields';
  $$('[data-metric]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.metric===state.metric)));
  $$('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===state.mode)));
  $$('[data-period]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.period===state.period)));
  const start=windowStart(data.today,state.period),end=data.today;
  const candidates=universe().filter(c=>state.selected.has(c.id)).map(c=>({c,...eligibility(c)})).filter(x=>!x.reason);
  const lines=candidates.map(x=>({c:x.c,...(prepare(x.s,start,end,state.mode)||{})})).filter(x=>x.points);
  const unit=state.metric==='yield' && state.mode==='level'?'%':'bp';
  const omitted=candidates.length-lines.length;
  $('#chart-range').textContent=dateLabel(start,true)+' — '+dateLabel(end,true)+' · '+lines.length+' plotted'+(omitted?' · '+omitted+' without matching history':'');
  $('#chart-source').textContent='Bloomberg · '+unit+(state.mode==='change'?' · change from '+dateLabel(start,true):'')+(lines.some(l=>l.instrument.status==='stale')?' · dashed = stale':'');
  if(!lines.length) {
    chartState=null;
    let title='Awaiting '+(state.metric==='cds'?'CDS':'bond yield')+' history';
    let note='The comparison will appear when Bloomberg observations are available.';
    if(!candidates.length){title='Select companies to compare';note='Use the company chips above. Convertible bonds can be included separately.';}
    else if(state.mode==='change' && candidates.some(x=>x.s.points.length)){title='No matching start-date observations';note='Try a shorter period or switch to Level to see the available history.';}
    else if(candidates.some(x=>x.s.points.length)){title='No observations in this period';note='Try a longer period to see the retained history.';}
    else if(data.feed.state==='blocked'){note=/WORKFLOW_REVIEW_NEEDED/i.test(data.feed.detail||'')?'Bloomberg has requested a workflow review. Quotes will appear after API access is restored.':'The Bloomberg refresh is blocked. No CDS or bond values have been substituted.';}
    $('#chart').innerHTML='<div class="empty-chart"><div><span class="empty-icon" aria-hidden="true">⌁</span><h3>'+title+'</h3><p>'+note+'</p></div></div>';
    return;
  }
  const W=Math.max(360,$('#chart').clientWidth),H=250,L=52,R=18,T=18,B=28,iw=W-L-R,ih=H-T-B;
  const vals=lines.flatMap(l=>l.points.map(p=>p[1]));
  let lo=Math.min(...vals),hi=Math.max(...vals);
  if(state.mode==='change'){lo=Math.min(lo,0);hi=Math.max(hi,0);}
  const pad=(hi-lo)*.12 || (unit==='%'?.15:2);lo-=pad;hi+=pad;
  const x=d=>L+(day(d)-day(start))/Math.max(1,day(end)-day(start))*iw;
  const y=v=>T+(hi-v)/(hi-lo)*ih;
  let svg='<svg id="comparison-svg" viewBox="0 0 '+W+' '+H+'" role="img" aria-label="'+esc($('#comparison-title').textContent+', '+state.period+', '+state.mode+', '+unit)+'. Use left and right arrow keys for observations." tabindex="0">';
  for(let k=0;k<5;k++){const v=lo+(hi-lo)*k/4,yy=y(v);svg+='<line x1="'+L+'" x2="'+(W-R)+'" y1="'+yy+'" y2="'+yy+'" stroke="var(--grid)"/><text x="'+(L-12)+'" y="'+(yy+4)+'" text-anchor="end">'+format(v,unit==='%'?1:0)+(unit==='%'?'%':'')+'</text>';}
  for(let k=0;k<5;k++){const d=iso(day(start)+(day(end)-day(start))*k/4);svg+='<text x="'+x(d)+'" y="'+(H-7)+'" text-anchor="'+(k===0?'start':k===4?'end':'middle')+'">'+esc(dateLabel(d))+'</text>';}
  if(state.mode==='change')svg+='<line x1="'+L+'" x2="'+(W-R)+'" y1="'+y(0)+'" y2="'+y(0)+'" stroke="var(--axis)" stroke-dasharray="3 4"/>';
  for(const line of lines) {
    const path=line.points.map((p,i)=>((i===0 || day(p[0])-day(line.points[i-1][0])>7)?'M':'L')+x(p[0]).toFixed(2)+','+y(p[1]).toFixed(2)).join(' ');
    svg+='<path class="series-line" data-issuer="'+esc(line.c.id)+'" d="'+path+'" fill="none" stroke="'+line.c.color+'" stroke-width="2.1" stroke-linejoin="round" stroke-linecap="round" '+(line.instrument.status==='stale'?'stroke-dasharray="5 4"':'')+'><title>'+esc(line.c.name+' · '+source(line.instrument)+(line.baseDate?' · baseline '+line.baseDate:''))+'</title></path>';
    const p=line.points.at(-1);svg+='<circle cx="'+x(p[0])+'" cy="'+y(p[1])+'" r="3" fill="'+line.c.color+'"/>';
  }
  svg+='<line id="chart-cross" y1="'+T+'" y2="'+(H-B)+'" stroke="var(--axis)" stroke-dasharray="3 4" visibility="hidden"/></svg>';
  $('#chart').innerHTML=svg;
  chartState={lines,start,end,unit,x,L,R,W,dates:[...new Set(lines.flatMap(l=>l.points.map(p=>p[0])))].sort(),cursor:0};
  const element=$('#comparison-svg');
  element.addEventListener('pointermove',ev=>{
    const point=new DOMPoint(ev.clientX,ev.clientY).matrixTransform(element.getScreenCTM().inverse());
    const n=Math.round(day(start)+Math.max(0,Math.min(1,(point.x-L)/iw))*(day(end)-day(start)));
    showTooltip(iso(n),ev.clientX,ev.clientY);
  });
  element.addEventListener('pointerleave',hideTooltip);
  element.addEventListener('blur',hideTooltip);
  element.addEventListener('keydown',ev=>{
    if(!['ArrowLeft','ArrowRight'].includes(ev.key))return;
    ev.preventDefault();chartState.cursor=Math.max(0,Math.min(chartState.dates.length-1,chartState.cursor+(ev.key==='ArrowRight'?1:-1)));
    const r=element.getBoundingClientRect();showTooltip(chartState.dates[chartState.cursor],r.left+r.width/2,r.top+40);
  });
}
function showTooltip(date,clientX,clientY) {
  if(!chartState)return;
  const {lines,x,unit}=chartState;
  const rows=lines.map(l=>{
    const p=l.points.filter(p=>p[0]<=date).at(-1);
    if(!p || day(date)-day(p[0])>4)return '';
    return '<div class="tooltip-row"><i style="background:'+l.c.color+'"></i><span>'+esc(l.c.name)+'<small>'+esc(p[0]+' · '+(state.metric==='yield'?bondLabel(l.instrument):'5Y CDS'))+'</small><small>'+esc((l.instrument.ticker||l.instrument.candidate)+' · '+l.instrument.field)+'</small>'+(l.baseDate?'<small>Baseline '+esc(l.baseDate)+'</small>':'')+'</span><b>'+esc((state.mode==='change'?signed(p[1]):format(p[1],unit==='%'?2:1))+' '+unit)+'</b></div>';
  }).join('');
  const tip=$('#chart-tooltip');
  tip.innerHTML='<strong>'+esc(dateLabel(date,true))+'</strong>'+(rows||'<span class="muted">No nearby observations</span>');
  tip.hidden=false;
  const r=tip.getBoundingClientRect();
  tip.style.left=Math.max(8,Math.min(clientX+16,innerWidth-r.width-10))+'px';
  tip.style.top=Math.max(8,Math.min(clientY+16,innerHeight-r.height-10))+'px';
  $('#chart-cross').setAttribute('x1',x(date));$('#chart-cross').setAttribute('x2',x(date));$('#chart-cross').setAttribute('visibility','visible');
}
function renderStatus() {
  const focus=issuers.filter(c=>c.focus),all=focus.flatMap(c=>[c.cds,mainBond(c)]).filter(Boolean);
  const available=all.filter(s=>s.last!=null),stale=available.filter(s=>s.status==='stale');
  const reviews=all.filter(s=>s.validationWarning);
  const blocked=data.feed.state==='blocked';
  const review=blocked && /WORKFLOW_REVIEW_NEEDED/i.test(data.feed.detail||'');
  const title=review?'Bloomberg workflow review required':blocked?'Bloomberg refresh blocked':reviews.length?'CDS quote validation pending':!available.length?'Issuer quotes unavailable':stale.length?'Retained quotes include stale observations':available.length<all.length?'Partial quote coverage':'Issuer quotes available';
  const note=(available.length?available.length+' of '+all.length+' main instruments have usable observations.':'CDS and bond histories are pending.')+(reviews.length?' '+reviews.map(s=>s.label).join(', ')+' under review.':'');
  $('#feed-status').classList.toggle('current',!blocked&&available.length===all.length&&!stale.length&&all.length>0);
  $('#feed-status').innerHTML='<b>'+title+'</b><span>'+note+'</span><a href="#data-details">Data details</a>';
  $('#observation-date').textContent=data.latest?'Latest quote · '+dateLabel(data.latest,true):'No issuer quotes yet';
  const missing=focus.filter(c=>!c.cds).map(c=>c.name);
  $('#coverage-detail').textContent='Source: Bloomberg PX_LAST for 5Y CDS; YLD_YTM_MID for bond yields. '+(missing.length?'No CDS is configured for '+missing.join(' and ')+'. ':'')+'Missing observations remain blank. '+reviews.map(s=>s.validationWarning).join(' ');
  $('#feed-detail').textContent='Latest refresh attempt: '+(data.fetched||'not recorded')+'. '+(data.feed.detail||'Instrument source and observation dates appear in each company’s expanded rows.');
}
// Hyperscaler CDS view: the official workbook basis (CDS_FLAT_SPREAD) and the issuer board (PX_LAST) are shown apart, never netted.
const hyper=issuers.filter(c=>/^hyperscaler/.test(c.tier||'')).sort((a,b)=>(a.flat?.last??a.cds?.last??1e9)-(b.flat?.last??b.cds?.last??1e9));
const rating=c=>(c.tier.match(/\(([^)]+)\)/)||[])[1]||'';
// BBB names (ORCL) trade at several times the AA spreads and flatten them on a common axis: one click adds them back
const hs={mode:'level',period:'6M',selected:new Set(hyper.filter(c=>!/^BBB/.test(rating(c))).map(c=>c.id)),chart:null};
const flatDelta=v=>v==null?'<span class="muted">—</span>':'<span class="delta '+tone(v)+'">'+signed(v)+'</span>';
function sparkline(points,color) {
  if(!points || points.length<2)return '<span class="muted">—</span>';
  const vals=points.map(p=>p[1]),lo=Math.min(...vals),hi=Math.max(...vals),w=96,h=26;
  const path=points.map((p,i)=>(i?'L':'M')+(i/(points.length-1)*(w-4)+2).toFixed(1)+','+(h-3-(p[1]-lo)/((hi-lo)||1)*(h-6)).toFixed(1)).join(' ');
  return '<svg class="hs-spark" viewBox="0 0 '+w+' '+h+'" width="'+w+'" height="'+h+'" role="img" aria-label="'+esc(points[0][0]+' '+format(vals[0])+' bp to '+points.at(-1)[0]+' '+format(vals.at(-1))+' bp')+'"><title>'+esc(points.map(p=>p[0]+' · '+format(p[1])+' bp').join('\n'))+'</title><path d="'+path+'" fill="none" stroke="'+color+'" stroke-width="1.6" stroke-linejoin="round"/></svg>';
}
function renderHyperTables() {
  const max=Math.max(...hyper.map(c=>c.flat?.last||0),1);
  $('#hs-count').textContent=hyper.length;
  $('#hs-official-rows').innerHTML=hyper.map(c=>{
    const f=c.flat,name='<td><div class="issuer-name"><span class="issuer-avatar" style="--series:'+c.color+'">'+esc(c.id.slice(0,2))+'</span><div><b>'+esc(c.name)+'</b><small>'+esc(c.id+' · '+rating(c))+'</small></div></div></td>';
    if(!f)return '<tr>'+name+'<td class="number" colspan="7"><span class="muted">Not in the official workbook</span></td></tr>';
    const d1=f.change1;
    return '<tr>'+name+'<td class="number"><span class="quote" title="'+esc('Bloomberg · '+f.bbg+' · CDS_FLAT_SPREAD')+'">'+format(f.last)+'</span><small class="quote-date '+(f.stale?'stale':'')+'" title="'+esc('Workbook refresh '+(f.quoted||'—').replace('T',' ')+'; the value was last changed on '+(f.markDate||'—'))+'">mark '+esc(dateLabel(f.markDate))+(f.stale?' · stale':'')+'</small></td>'
      +'<td class="number">'+(d1?'<span class="delta '+tone(d1.value)+'" title="'+esc(d1.start+' → '+d1.end)+'">'+signed(d1.value)+'</span>':'<span class="muted">—</span>')+'</td>'
      +'<td class="number">'+flatDelta(f.dSnapshot)+'</td><td class="number">'+format(f.msDesk,0)+'</td><td class="number">'+flatDelta(f.dMsDesk)+'</td>'
      +'<td class="hs-bar-column"><div class="hs-bar"><i style="width:'+(100*(f.last||0)/max).toFixed(1)+'%;background:'+c.color+'"></i></div></td>'
      +'<td>'+sparkline(f.points,c.color)+'</td></tr>';
  }).join('');
  const quoted=hyper.map(c=>c.flat?.quoted).filter(Boolean).sort().at(-1);
  $('#hs-official-source').textContent='Source: Bloomberg CDS_FLAT_SPREAD via AI_Credit_Live.xlsx'+(quoted?' · refreshed '+quoted.replace('T',' '):'')+' · MS desk marks 24-Aug-2026';
  $('#hs-board-rows').innerHTML=hyper.map(c=>'<tr><td><div class="issuer-name"><span class="issuer-avatar" style="--series:'+c.color+'">'+esc(c.id.slice(0,2))+'</span><div><b>'+esc(c.name)+'</b><small>'+esc(c.id)+'</small></div></div></td><td class="number">'+quote(c.cds,true)+'</td><td class="number">'+delta(c.cds,1)+'</td><td class="number">'+delta(c.cds,7)+'</td><td class="number">'+delta(c.cds,30)+'</td><td class="bond-source">'+esc(source(c.cds))+'</td></tr>').join('');
  const steps=(data.steps||[]).map(s=>'<li><b>'+esc(s.id)+'</b> PX_LAST jumps from '+format(s.from[1])+' to '+format(s.to[1])+' bp on '+esc(dateLabel(s.to[0],true))+' ('+signed(s.to[1]-s.from[1])+' bp in one session). That is more likely a ticker or quote-convention break than a market move: Change mode across that date overstates the widening.</li>').join('');
  const twins=(data.twins||[]).map(t=>'<li><b>'+esc(t.pair.join(' and '))+'</b> PX_LAST histories print the same value on '+t.days+' days ('+esc(dateLabel(t.first,true))+' — '+esc(dateLabel(t.last,true))+'). That looks like a shared proxy curve, not two traded markets, so read those stretches of the chart with caution.</li>').join('');
  $('#hs-notes').innerHTML='<h3>Reading the two bases</h3><ul><li>The <b>official base</b> (top table) is CDS_FLAT_SPREAD from the AI_Credit_Live workbook. The MS desk marks of 24-Aug-2026 are on the same basis.</li><li>The <b>issuer board</b> (chart and lower table) is PX_LAST on the same Bloomberg tickers. Its levels can sit well below the flat spread, so the two are never netted or charted together.</li><li>Δ 1D on the official base compares the last two distinct marks. A morning pull that repeats the prior close counts as a carried mark, not a new print.</li>'+steps+twins+'</ul>';
}
function hideHyperTip() { $('#hs-tooltip').hidden=true; $('#hs-cross')?.setAttribute('visibility','hidden'); }
function renderHyperChart() {
  hideHyperTip();
  $$('[data-hs-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.hsMode===hs.mode)));
  $$('[data-hs-period]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.hsPeriod===hs.period)));
  $('#hs-filters').innerHTML=hyper.map(c=>{
    const reason=!c.cds?'No 5Y CDS configured':c.cds.validationWarning||null;
    return '<button type="button" class="company-chip" data-hs-select="'+esc(c.id)+'" style="--series:'+c.color+'" aria-pressed="'+(hs.selected.has(c.id)&&!reason)+'" '+(reason?'disabled':'')+' title="'+esc(reason||source(c.cds))+'"><i></i>'+esc(c.id)+'</button>';
  }).join('');
  const start=windowStart(data.today,hs.period),end=data.today,unit='bp';
  const lines=hyper.filter(c=>hs.selected.has(c.id)&&c.cds&&!c.cds.validationWarning).map(c=>({c,...(prepare(c.cds,start,end,hs.mode)||{})})).filter(l=>l.points);
  const off=hyper.filter(c=>!hs.selected.has(c.id)).map(c=>c.id);
  $('#hs-range').textContent=dateLabel(start,true)+' — '+dateLabel(end,true)+' · '+lines.length+' plotted'+(hs.mode==='change'?' · change from '+dateLabel(start,true):'')+(off.length?' · '+off.join(', ')+' off (select above)':'');
  if(!lines.length){hs.chart=null;$('#hs-chart').innerHTML='<div class="empty-chart"><div><span class="empty-icon" aria-hidden="true">⌁</span><h3>No matching history</h3><p>Select a company or try a shorter period. New series have no baseline for Change mode.</p></div></div>';return;}
  const W=Math.max(360,$('#hs-chart').clientWidth),H=250,L=52,R=18,T=18,B=28,iw=W-L-R,ih=H-T-B;
  const vals=lines.flatMap(l=>l.points.map(p=>p[1]));
  let lo=Math.min(...vals),hi=Math.max(...vals);
  if(hs.mode==='change'){lo=Math.min(lo,0);hi=Math.max(hi,0);}
  const pad=(hi-lo)*.12||2;lo-=pad;hi+=pad;
  const x=d=>L+(day(d)-day(start))/Math.max(1,day(end)-day(start))*iw;
  const y=v=>T+(hi-v)/(hi-lo)*ih;
  let svg='<svg id="hs-svg" viewBox="0 0 '+W+' '+H+'" role="img" aria-label="'+esc('Hyperscaler 5Y CDS PX_LAST, '+hs.period+', '+hs.mode+', bp')+'">';
  for(let k=0;k<5;k++){const v=lo+(hi-lo)*k/4,yy=y(v);svg+='<line x1="'+L+'" x2="'+(W-R)+'" y1="'+yy+'" y2="'+yy+'" stroke="var(--grid)"/><text x="'+(L-12)+'" y="'+(yy+4)+'" text-anchor="end">'+format(v,0)+'</text>';}
  for(let k=0;k<5;k++){const d=iso(day(start)+(day(end)-day(start))*k/4);svg+='<text x="'+x(d)+'" y="'+(H-7)+'" text-anchor="'+(k===0?'start':k===4?'end':'middle')+'">'+esc(dateLabel(d))+'</text>';}
  if(hs.mode==='change')svg+='<line x1="'+L+'" x2="'+(W-R)+'" y1="'+y(0)+'" y2="'+y(0)+'" stroke="var(--axis)" stroke-dasharray="3 4"/>';
  const labels=[];
  for(const line of lines){
    const path=line.points.map((p,i)=>((i===0||day(p[0])-day(line.points[i-1][0])>7)?'M':'L')+x(p[0]).toFixed(2)+','+y(p[1]).toFixed(2)).join(' ');
    svg+='<path d="'+path+'" fill="none" stroke="'+line.c.color+'" stroke-width="2.1" stroke-linejoin="round" stroke-linecap="round" '+(line.instrument.status==='stale'?'stroke-dasharray="5 4"':'')+'/>';
    const p=line.points.at(-1);svg+='<circle cx="'+x(p[0])+'" cy="'+y(p[1])+'" r="3" fill="'+line.c.color+'"/>';
    labels.push({c:line.c,x:x(p[0])-8,y:y(p[1])+3.5});
  }
  labels.sort((a,b)=>a.y-b.y).forEach((l,i,all)=>{if(i&&l.y-all[i-1].y<11)l.y=all[i-1].y+11;});  // stack end labels that would collide
  svg+=labels.map(l=>'<text x="'+l.x+'" y="'+l.y+'" text-anchor="end" class="hs-endlabel" fill="'+l.c.color+'">'+esc(l.c.id)+'</text>').join('');
  svg+='<line id="hs-cross" y1="'+T+'" y2="'+(H-B)+'" stroke="var(--axis)" stroke-dasharray="3 4" visibility="hidden"/></svg>';
  $('#hs-chart').innerHTML=svg;
  hs.chart={lines,x};
  const element=$('#hs-svg');
  element.addEventListener('pointermove',ev=>{
    const point=new DOMPoint(ev.clientX,ev.clientY).matrixTransform(element.getScreenCTM().inverse());
    const date=iso(Math.round(day(start)+Math.max(0,Math.min(1,(point.x-L)/iw))*(day(end)-day(start))));
    const rows=hs.chart.lines.map(l=>{
      const p=l.points.filter(p=>p[0]<=date).at(-1);
      if(!p||day(date)-day(p[0])>4)return '';
      return '<div class="tooltip-row"><i style="background:'+l.c.color+'"></i><span>'+esc(l.c.name)+'<small>'+esc(p[0]+' · PX_LAST')+'</small>'+(l.baseDate?'<small>Baseline '+esc(l.baseDate)+'</small>':'')+'</span><b>'+esc((hs.mode==='change'?signed(p[1]):format(p[1]))+' bp')+'</b></div>';
    }).join('');
    const tip=$('#hs-tooltip');
    tip.innerHTML='<strong>'+esc(dateLabel(date,true))+'</strong>'+(rows||'<span class="muted">No nearby observations</span>');
    tip.hidden=false;
    const r=tip.getBoundingClientRect();
    tip.style.left=Math.max(8,Math.min(ev.clientX+16,innerWidth-r.width-10))+'px';
    tip.style.top=Math.max(8,Math.min(ev.clientY+16,innerHeight-r.height-10))+'px';
    $('#hs-cross').setAttribute('x1',x(date));$('#hs-cross').setAttribute('x2',x(date));$('#hs-cross').setAttribute('visibility','visible');
  });
  element.addEventListener('pointerleave',hideHyperTip);
}
function showView(view) {
  $('#monitor-view').hidden=view!=='monitor';$('#research-view').hidden=view!=='research';$('#hyperscalers-view').hidden=view!=='hyperscalers';
  $$('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));
  hideTooltip();hideHyperTip();
  if(view==='hyperscalers')renderHyperChart();
}
function handleHash() {
  const id=location.hash.slice(1);
  if(id==='spreads'||id==='overview'||id==='monitor'||id==='comparison'){
    showView('monitor');
    if(id==='spreads'||id==='overview')history.replaceState(null,'',location.pathname+location.search+'#monitor');
  } else if(id==='yields') {
    showView('monitor');state.metric='yield';renderChart();
  } else if(id==='data-details') {
    showView('monitor');$('#data-details').open=true;$('#data-details').scrollIntoView();
  } else if(id==='research')showView('research');
  else if(id==='hyperscalers')showView('hyperscalers');
  else if(id && document.getElementById(id)?.classList.contains('research-item')){
    showView('research');document.getElementById(id).open=true;document.getElementById(id).scrollIntoView();
  }
}
document.addEventListener('click',ev=>{
  const button=ev.target.closest('button');
  if(button?.dataset.view){showView(button.dataset.view);history.replaceState(null,'',location.pathname+location.search+'#'+button.dataset.view);}
  if(button?.dataset.metric){state.metric=button.dataset.metric;renderChart();}
  if(button?.dataset.mode){state.mode=button.dataset.mode;renderChart();}
  if(button?.dataset.period){state.period=button.dataset.period;renderChart();}
  if(button?.dataset.select){const id=button.dataset.select;state.selected.has(id)?state.selected.delete(id):state.selected.add(id);renderChart();$('[data-select="'+id+'"]')?.focus();}
  if(button?.dataset.hsMode){hs.mode=button.dataset.hsMode;renderHyperChart();}
  if(button?.dataset.hsPeriod){hs.period=button.dataset.hsPeriod;renderHyperChart();}
  if(button?.dataset.hsSelect){const id=button.dataset.hsSelect;hs.selected.has(id)?hs.selected.delete(id):hs.selected.add(id);renderHyperChart();$('[data-hs-select="'+id+'"]')?.focus();}
  if(button?.dataset.sort){const key=button.dataset.sort;state.direction=key===state.sort?-state.direction:key==='name'?1:-1;state.sort=key;renderTable();}
  if(button?.dataset.compare){const c=issuers.find(c=>c.id===button.dataset.compare);state.selected=new Set([c.id]);if(!c.cds)state.metric='yield';if(state.metric==='yield' && mainBond(c)?.board.kind==='convertible'){state.converts=true;$('#include-convertibles').checked=true;}renderChart();$('#comparison').scrollIntoView({behavior:'smooth'});}
  const row=ev.target.closest('.issuer-row');
  if(row){const id=row.dataset.company;state.expanded=state.expanded===id?null:id;renderTable();$('#toggle-'+id)?.focus({preventScroll:true});}
});
document.addEventListener('change',ev=>{
  const t=ev.target;
  if(t.id==='universe'){state.universe=t.value;state.expanded=null;renderTable();renderChart();}
  if(t.id==='include-convertibles'){state.converts=t.checked;renderChart();}
  if(t.dataset.bondCompany){
    const c=issuers.find(c=>c.id===t.dataset.bondCompany);
    if(c?.bonds.some(b=>b.id===t.value)){state.main[c.id]=t.value;renderTable();renderChart();renderStatus();$('input[data-bond-company="'+c.id+'"][value="'+t.value+'"]')?.focus({preventScroll:true});}
  }
});
$('#company-search').addEventListener('input',ev=>{state.search=ev.target.value;renderTable();});
$('#deal-search')?.addEventListener('input',ev=>{
  const q=ev.target.value.toLowerCase().trim();
  $$('#deal-table tr[data-category]').forEach(r=>r.hidden=q && !r.textContent.toLowerCase().includes(q));
  $$('#deal-table tr.cat').forEach(r=>{let n=r.nextElementSibling,any=false;while(n && !n.classList.contains('cat')){if(!n.hidden)any=true;n=n.nextElementSibling;}r.hidden=!any;});
});
window.addEventListener('hashchange',handleHash);
let resizeTimer;window.addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{renderChart();if(!$('#hyperscalers-view').hidden)renderHyperChart();},120);});
renderStatus();renderTable();renderChart();renderHyperTables();handleHash();
})();
