
(() => {
'use strict';
const d=REVENUE_DATA, colors={OpenAI:'#58a6ff',Anthropic:'#e3b341','Combined system':'#3dccb3'};
const $=id=>document.getElementById(id);
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num=x=>Number(x).toLocaleString('en-US',{maximumFractionDigits:1,minimumFractionDigits:1});
const money=x=>'$'+num(x)+'M';
const source=x=>d.sources[x.source_id];
const link=s=>'<a target="_blank" rel="noopener" href="'+esc(s.url)+'">'+esc(s.publisher)+'</a>';
const qualifier=o=>(o.qualifier==='approximately'?'~':o.qualifier==='close to'?'close to ':o.qualifier==='nearing'?'near ':o.qualifier)+money(o.value);
const basisName=b=>({net:'Net',gross:'Gross',gross_up:'Investor gross-up',company_reported:'Source reporting basis'}[b]||b);
const periodLabel=x=>new Date(x+'T12:00:00Z').toLocaleDateString('en-US',{month:'short',year:'2-digit',timeZone:'UTC'});
const current=d.annual.filter(x=>x.period==='CY26E');
const lastNet=d.observations.find(x=>x.id==='OAI-2026-SEP-NET');
const lastQuarter=d.observations.find(x=>x.id==='ANT-2026-Q3');
$('rev-vintage').textContent='Workbook saved '+new Date(d.workbook_saved).toLocaleString('en-GB',{timeZone:'America/Sao_Paulo',dateStyle:'medium',timeStyle:'short'})+' São Paulo · sources checked '+d.checked+'.';
$('rev-hash').textContent='Source workbook SHA-256: '+d.workbook_sha256;
$('rev-kpis').innerHTML=current.map(x=>'<div class="stat-card"><div class="stat-label">'+esc(x.company)+' · FY2026E revenue</div><div class="stat-value" style="color:'+colors[x.company]+'">'+money(x.value)+'</div><div class="stat-sub">'+esc(x.basis)+' · Capstone estimate<br>'+esc(x.cell)+'</div></div>').join('')+
'<div class="stat-card"><div class="stat-label">OpenAI · latest net run rate</div><div class="stat-value oai">'+qualifier(lastNet)+'</div><div class="stat-sub">September 2026 · press-reported<br>'+link(source(lastNet))+' · '+source(lastNet).published+'</div></div>'+
'<div class="stat-card"><div class="stat-label">Anthropic · Q3 revenue</div><div class="stat-value anth">'+money(lastQuarter.value)+'</div><div class="stat-sub">Quarterly revenue · press-reported<br>'+link(source(lastQuarter))+' · '+source(lastQuarter).published+'</div></div>';
const annualPeriods=[...new Set(d.annual.map(x=>x.period))];
$('rev-annual').innerHTML='<thead><tr><th>Year</th><th>OpenAI · net</th><th>Anthropic · gross</th><th class="rev-total">Combined system<small>Mixed basis</small></th></tr></thead><tbody>'+annualPeriods.map(p=>{
 const total=d.combined.annual.find(a=>a.period===p);
 return '<tr><td>'+esc(p)+'</td>'+['OpenAI','Anthropic'].map(c=>{const x=d.annual.find(a=>a.company===c&&a.period===p);return '<td>'+(x?num(x.value)+'<small>'+esc(x.cell)+'</small>':'—')+'</td>';}).join('')+
 '<td class="rev-total">'+(total?num(total.value)+'<small>'+esc(total.cell)+'</small>':'—')+'</td></tr>';
}).join('')+'</tbody>';
$('rev-quarterly').innerHTML='<thead><tr><th>Company / quarter</th><th>Model</th><th>Reported</th></tr></thead><tbody>'+d.quarterly.map(q=>{const o=d.observations.find(x=>x.company===q.company&&x.event_period===q.period&&x.metric==='quarterly_revenue');return '<tr><td>'+esc(q.company)+' · '+esc(q.period)+'<small>'+esc(q.basis)+'</small></td><td>'+num(q.value)+'<small>'+esc(q.cell)+'</small></td><td>'+(o?qualifier(o)+'<small>'+link(source(o))+' · '+source(o).published+'</small>':'—<small>No source matched in this refresh</small>')+'</td></tr>';}).join('')+'</tbody>';
function renderSources(){
 const company=$('rev-company').value;
 const rows=d.observations.filter(x=>company==='all'||x.company===company).sort((a,b)=>b.event_date.localeCompare(a.event_date)||a.company.localeCompare(b.company));
 $('rev-source-count').textContent=rows.length+' observations · click the publisher to open the original source.';
 $('rev-sources').innerHTML='<thead><tr><th>Company / revenue period</th><th>Value & basis</th><th>Source / publication date</th><th>Interpretation & access</th></tr></thead><tbody>'+rows.map(o=>{
  const s=source(o);
  return '<tr id="news-'+esc(o.id)+'"><td><strong style="color:'+colors[o.company]+'">'+esc(o.company)+'</strong><br>'+esc(o.event_period)+'<small>Recorded '+esc(o.recorded)+'</small></td><td>'+qualifier(o)+'<br><span class="rev-pill">'+(o.metric==='run_rate'?'Annualized run rate':'Quarterly revenue')+'</span><small>'+esc(basisName(o.basis))+'</small></td><td>'+link(s)+' · '+esc(s.published)+'<small>'+esc(s.author)+'<br>'+esc(s.title)+'</small></td><td>'+esc(o.note)+'<small>'+esc(s.access)+(s.verification_url?' · <a target="_blank" rel="noopener" href="'+esc(s.verification_url)+'">Indexed reproduction</a>':'')+'</small></td></tr>';
 }).join('')+'</tbody>';
}
function selectedSeries(){
 const basis=$('rev-basis').value;
 return d.series.filter(s=>basis==='reported'?s.reported_basis:s.basis===basis);
}
function combinedSeries(){
 return d.combined.monthly[$('rev-basis').value];
}
function renderSystemSummary(){
 const s=combinedSeries();
 const historical=s.points.filter(p=>p.status!=='Forecast').at(-1);
 const forecast=s.points.filter(p=>p.status==='Forecast').at(-1);
 $('rev-system-summary').innerHTML=[[historical,'Latest historical model month'],[forecast,'Last forecast month']].map(([p,label])=>
 '<div><div class="stat-label">Combined system · '+esc(label)+'</div><div class="rev-system-value">'+(p?money(p.value):'—')+
 '</div><div class="stat-sub">'+(p?periodLabel(p.date)+' · '+esc(s.basis)+' · '+esc(p.status)+'<br>'+
 p.components.map(c=>esc(c.company)+' '+money(c.value)).join(' + '):'Both companies are required for the same month')+'</div></div>').join('');
}
function renderMonthly(){
 const series=[...selectedSeries(),combinedSeries()];
 const dates=[...new Set(series.flatMap(s=>s.points.map(p=>p.date)))].sort();
 $('rev-monthly').innerHTML='<thead><tr><th>Month</th>'+series.map(s=>'<th>'+esc(s.company+' '+s.basis)+'</th>').join('')+'<th>Classification</th><th>News for that period</th></tr></thead><tbody>'+dates.map(date=>{
  const anchors=d.observations.filter(o=>o.metric==='run_rate'&&o.event_date.slice(0,7)===date.slice(0,7));
  return '<tr><td>'+periodLabel(date)+'</td>'+series.map(s=>{const p=s.points.find(p=>p.date===date);return '<td>'+(p?num(p.value)+'<small>'+esc(p.cell)+'</small>':'—')+'</td>';}).join('')+'<td>'+esc(date.slice(0,7)>=d.asof.slice(0,7)?'Forecast':'Model estimate')+'</td><td>'+(anchors.length?anchors.map(o=>'<a href="#rev-source-card" data-news="'+esc(o.id)+'">'+esc(o.company)+' · '+qualifier(o)+'</a>').join('<br>'):'<small>No discrete disclosure verified for this month</small>')+'</td></tr>';
 }).join('')+'</tbody>';
}
const baseLayout={paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',font:{color:'#9da7b3',size:11},margin:{l:70,r:24,t:46,b:48},xaxis:{type:'date',gridcolor:'#21262d',tickformat:"%b '%y"},yaxis:{title:'USD millions',gridcolor:'#21262d',zerolinecolor:'#30363d',rangemode:'tozero',tickformat:',.0f'},legend:{orientation:'h',y:1.17,font:{size:11}},hovermode:'closest'};
const config={responsive:true,displayModeBar:false};
function renderCharts(){
 const selected=[...selectedSeries(),combinedSeries()], basis=$('rev-basis').value;
 $('rev-basis-note').textContent=basis==='reported'?'Mixed reporting bases: OpenAI net and Anthropic gross. The combined system adds these two bases. Choose Both net or Both gross for a consistent basis.':basis==='net'?'Anthropic net is a Capstone adjustment. The combined system sums both labs on this net model basis.':'OpenAI gross is a Capstone adjustment. The combined system sums both labs on this gross model basis, which differs from the $70bn investor gross-up.';
 renderMonthly();
 renderSystemSummary();
 if(!window.Plotly){
  $('rev-model-chart').innerHTML='<p class="rev-caption">Chart library unavailable. All values remain available in the tables below.</p>';
  $('rev-news-chart').innerHTML='<p class="rev-caption">See News references for the complete observation history.</p>'; return;
 }
 const traces=[];
 for(const s of selected){
  const historic=s.points.filter(p=>p.status!=='Forecast');
  const future=s.points.filter(p=>p.status==='Forecast');
  for(const [points,forecast] of [[historic,false],[historic.length&&future.length?[historic[historic.length-1],...future]:future,true]]){
   if(!points.length)continue;
   traces.push({x:points.map(p=>p.date),y:points.map(p=>p.value),type:'scatter',mode:'lines+markers',
    name:s.company+' '+s.basis+(forecast?' forecast':''),legendgroup:s.id,showlegend:!forecast,
    line:{color:colors[s.company],width:s.company==='Combined system'?3.5:2.5,dash:forecast?'dash':'solid'},marker:{size:5},
    customdata:points.map(p=>[p.cell,p.status,s.company+' '+s.basis]),
    hovertemplate:'%{customdata[2]}<br>%{x|%b %Y}: $%{y:,.1f}M<br>%{customdata[1]}<br>%{customdata[0]}<extra></extra>'});
  }
 }
 Plotly.react('rev-model-chart',traces,{...baseLayout,shapes:[{type:'line',x0:d.asof.slice(0,7)+'-01',x1:d.asof.slice(0,7)+'-01',xref:'x',yref:'paper',y0:0,y1:1,line:{color:'#77818d',dash:'dot',width:1}}]},config);
 const groups=[['OpenAI',false],['Anthropic',false],['OpenAI',true]];
 const news=groups.map(([company,gross])=>{
  const rows=d.observations.filter(o=>o.metric==='run_rate'&&o.company===company&&(o.basis==='gross_up')===gross);
  return {x:rows.map(o=>o.event_date),y:rows.map(o=>o.value),type:'scatter',mode:'markers',name:company+(gross?' investor gross-up':' reporting basis'),
   marker:{color:colors[company],size:10,symbol:gross?'diamond-open':'diamond',line:{width:2}},
   customdata:rows.map(o=>[o.id,o.event_period,qualifier(o),source(o).publisher,source(o).published,basisName(o.basis)]),
   hovertemplate:'%{customdata[1]}<br>%{customdata[2]} · %{customdata[5]}<br>%{customdata[3]} · %{customdata[4]}<br>Click for reference<extra></extra>'};
 });
 Plotly.react('rev-news-chart',news,baseLayout,config).then(()=>{
  const chart=$('rev-news-chart');
  chart.removeAllListeners?.('plotly_click');
  chart.on('plotly_click',event=>showNews(event.points[0].customdata[0]));
 });
}
function showNews(id){
 $('rev-company').value='all';renderSources();
 document.querySelectorAll('.rev-highlight').forEach(r=>r.classList.remove('rev-highlight'));
 const row=$('news-'+id);if(row){row.classList.add('rev-highlight');row.scrollIntoView({behavior:'smooth',block:'center'});}
}
$('rev-company').addEventListener('change',renderSources);
$('rev-basis').addEventListener('change',renderCharts);
$('rev-monthly').addEventListener('click',e=>{const a=e.target.closest('[data-news]');if(a){e.preventDefault();showNews(a.dataset.news);}});
window.renderRevenue=renderCharts;
renderSources();renderCharts();
})();

