const relativeState={year:'current',basis:'absolute'};
const relativeRankCache=new Map();
function rbtMean(a){return a.length?a.reduce((s,v)=>s+v,0)/a.length:null;}
function rbtBand(p){return !finiteReading(p)?null:p<.3?0:p>=.7?2:1;}
function rbtValue(e,basis){return !finiteReading(e.return)?null:basis==='absolute'?e.return:finiteReading(e.qqq_return)?e.return-e.qqq_return:null;}
function rbtRanks(t,date,key,window,peers){
 const id=[t,date,key,window,...peers].join('|');if(relativeRankCache.has(id))return relativeRankCache.get(id);
 const cross=D.relative_context?.[date]?.scores||{},v=cross[t]?.[key];
 const own=comparisonStats(v,comparisonHistory(t,date,window).map(x=>x[1].scores[key]),8),peer=comparisonStats(v,peers.map(p=>cross[p]?.[key]));
 const result={own:own.percentile==null?null:own.percentile/100,peer:peer.percentile==null?null:peer.percentile/100,own_n:own.n,peer_n:peer.n};relativeRankCache.set(id,result);return result;
}
function rbtEvents(t,year,h,key,window,peers,cutoff){
 const out=[],observed=new Map();Object.entries(D.company_studies?.[t]||{}).forEach(([y,hs])=>{if(year!=='all'&&y!==year)return;(hs[h]||[]).forEach(e=>observed.set(e.signal,e));});
 Object.entries(D.relative_context||{}).forEach(([date,pack])=>{const e=pack.horizons[h];if(!e||e.exit>cutoff||(year!=='all'&&date.slice(0,4)!==year))return;out.push({...observed.get(date)||{...e,return:null,scores:{}},...rbtRanks(t,date,key,window,peers)});});
 return out.sort((a,b)=>a.signal.localeCompare(b.signal));
}
function rbtSpread(events,axis,basis){
 let ln=0,ls=0,hn=0,hs=0;for(const e of events){const b=rbtBand(e[axis]),v=rbtValue(e,basis);if(v==null)continue;if(b===0){ln++;ls+=v;}if(b===2){hn++;hs+=v;}}
 return ln&&hn?hs/hn-ls/ln:null;
}
function rbtBootstrap(events,h,stat,multiplier=1){
 const n=events.length;if(n<20)return {ci:null,draws:0,valid_draws:0};
 let seed=51020+Number(h)+n;const block=(Number(h)===5?4:2)*multiplier,values=[];
 for(let i=0;i<1000;i++){const sample=[];while(sample.length<n){seed=(Math.imul(1664525,seed)+1013904223)>>>0;const start=Math.floor(seed*n/4294967296);for(let j=0;j<block&&sample.length<n;j++)sample.push(events[(start+j)%n]);}const v=stat(sample);if(finiteReading(v))values.push(v);}
 values.sort((a,b)=>a-b);return {ci:values.length>=900?[values[Math.floor(values.length*.025)],values[Math.min(values.length-1,Math.floor(values.length*.975))]]:null,draws:1000,valid_draws:values.length};
}
function rbtSummary(events,axis,h,basis,interval=true){
 const groups=[[],[],[]],eligible=[];let missing=0,thin=0;
 for(const e of events){const b=rbtBand(e[axis]),v=rbtValue(e,basis);if(b==null)continue;if(v==null){missing++;continue;}groups[b].push(v);eligible.push(v);if(axis==='peer'&&e.peer_n<3)thin++;}
 const buckets=groups.map(a=>{const s=a.slice().sort((x,y)=>x-y);return {n:a.length,mean:rbtMean(a),median:s.length?(s[Math.floor((s.length-1)/2)]+s[Math.floor(s.length/2)])/2:null,positive:a.filter(x=>x>0).length,hit_rate:a.length?a.filter(x=>x>0).length/a.length:null};});
 const boot=interval&&eligible.length>=20&&groups[0].length>=5&&groups[2].length>=5?rbtBootstrap(events,h,es=>rbtSpread(es,axis,basis)):{ci:null,draws:0,valid_draws:0};
 const long_block=boot.draws?rbtBootstrap(events,h,es=>rbtSpread(es,axis,basis),2):{ci:null,draws:0,valid_draws:0};
 return {scheduled:events.length,n:eligible.length,missing_returns:missing,unavailable_signal:events.length-eligible.length-missing,thin_peer_events:thin,baseline:rbtMean(eligible),baseline_hit:eligible.length?eligible.filter(x=>x>0).length/eligible.length:null,buckets,spread:rbtSpread(events,axis,basis),...boot,long_block};
}
function rbtBars(s,basis){
 const vals=s.buckets.map(x=>x.mean).filter(finiteReading),lo=Math.min(0,s.baseline||0,...vals),hi=Math.max(0,s.baseline||0,...vals),span=Math.max(.005,hi-lo),mn=lo-span*.17,mx=hi+span*.26,w=320,h=145,top=10,bottom=116,y=v=>bottom-(v-mn)/(mx-mn)*(bottom-top);
 let svg='<svg viewBox="0 0 '+w+' '+h+'" role="img" aria-label="Average subsequent return after low, middle and high percentile readings"><line x1="12" x2="308" y1="'+y(0)+'" y2="'+y(0)+'" stroke="var(--border)"/>';
 if(s.baseline!=null)svg+='<line x1="12" x2="308" y1="'+y(s.baseline)+'" y2="'+y(s.baseline)+'" stroke="var(--blue)" stroke-dasharray="4 3" opacity=".65"><title>Matched baseline '+(basis==='absolute'?pct(s.baseline):pp(s.baseline))+'</title></line>';
 s.buckets.forEach((b,i)=>{const x=60+i*100,v=b.mean;svg+='<text x="'+x+'" y="136" text-anchor="middle">'+['Low','Middle','High'][i]+'</text>';if(v==null){svg+='<text x="'+x+'" y="65" text-anchor="middle">—</text>';return;}svg+='<rect x="'+(x-23)+'" y="'+Math.min(y(0),y(v))+'" width="46" height="'+Math.max(1,Math.abs(y(v)-y(0)))+'" rx="3" fill="'+(v>=0?'var(--green)':'var(--red)')+'" opacity=".6"/><text x="'+x+'" y="'+(v>=0?y(v)-6:y(v)+14)+'" text-anchor="middle" style="fill:var(--text)">'+num(v*100,2)+(basis==='absolute'?'%':'pp')+'</text>';});
 return svg+'</svg>';
}
function rbtStatus(s){return !s.ci?(s.draws?'Insufficient resampling support':'Too few observations'):s.ci[0]>0?'High > low in this sample':s.ci[1]<0?'Low > high in this sample':'No clear high/low separation';}
function rbtCard(axis,h,s,basis){
 return '<article class="card relative-card"><div class="row between"><h3>'+ (axis==='own'?'Versus own history':'Versus peers')+'</h3><span class="comparison-tag">'+h+' sessions</span></div><div class="relative-spread"><strong class="'+cls(s.spread)+'">'+pp(s.spread)+'</strong><span>High − low<br><small>'+s.n+' usable holds</small></span></div><div class="relative-status">'+rbtStatus(s)+'</div><div class="relative-chart">'+rbtBars(s,basis)+'</div><div class="relative-bucket-stats">'+s.buckets.map(b=>'<div title="Median: '+(basis==='absolute'?pct(b.median):pp(b.median))+'"><b>n='+b.n+'</b><small>'+b.positive+' / '+b.n+' positive</small></div>').join('')+'</div><div class="relative-baseline"><span>Matched baseline <b>'+(basis==='absolute'?pct(s.baseline):pp(s.baseline))+'</b></span><span>Baseline positive <b>'+(s.baseline_hit==null?'—':num(s.baseline_hit*100,0)+'%')+'</b></span></div><div class="foot-source">95% interval: '+(s.ci?ci(s.ci):s.draws?'too few valid resamples':'needs 20 holds and 5 in each extreme')+(s.draws?' · '+s.valid_draws+'/'+s.draws+' valid resamples':'')+'</div>'+(s.draws?'<div class="foot-source">Longer blocks: '+(s.long_block.ci?ci(s.long_block.ci):'interval unavailable')+' · '+s.long_block.valid_draws+'/'+s.long_block.draws+' valid</div>':'')+'<div class="foot-source">'+s.unavailable_signal+' unavailable signals · '+s.missing_returns+' missing returns'+(axis==='peer'?' · '+s.thin_peer_events+' holds with fewer than 3 peers':'')+'</div></article>';
}
function rbtJoint(events,h,basis){
 const cells=Array.from({length:9},()=>[]);for(const e of events){const a=rbtBand(e.own),b=rbtBand(e.peer),v=rbtValue(e,basis);if(a!=null&&b!=null&&v!=null)cells[a*3+b].push(v);}
 return '<div class="relative-joint"><h3>'+h+' sessions · both dimensions</h3><div class="tiny muted">Rows: own history · columns: peers</div><div class="joint-grid"><span></span>'+['Low','Middle','High'].map(x=>'<span class="joint-label">'+x+'</span>').join('')+[0,1,2].map(i=>'<span class="joint-label">'+['Low','Middle','High'][i]+'</span>'+[0,1,2].map(j=>{const a=cells[i*3+j],v=rbtMean(a);return '<div class="joint-cell '+(a.length<5?'sparse':'')+'" style="--cell:'+(v==null?'var(--muted)':v>=0?'var(--green)':'var(--red)')+'"><b>'+(basis==='absolute'?pct(v):pp(v))+'</b><small>n='+a.length+(a.length<5?' · sparse':'')+'</small></div>';}).join('')).join('')+'</div></div>';
}
function rbtYearTable(t,key,window,peers,cutoff,basis){
 return '<table class="company-table"><thead><tr><th>Year</th><th>Own · 5d</th><th>Own · 20d</th><th>Peers · 5d</th><th>Peers · 20d</th></tr></thead><tbody>'+['2024','2025','2026'].filter(y=>y<=cutoff.slice(0,4)).map(y=>'<tr><td>'+y+'</td>'+[['own','5'],['own','20'],['peer','5'],['peer','20']].map(([a,h])=>{const s=rbtSummary(rbtEvents(t,y,h,key,window,peers,cutoff),a,h,basis,false);return '<td>'+colored(s.spread,true)+'<small class="cell-sub">Low n='+s.buckets[0].n+' / high n='+s.buckets[2].n+'</small></td>';}).join('')+'</tr>').join('')+'</tbody></table>';
}
function rbtPooled(key,cutoff){
 const series=D.relative_summary?.aggregate?.[key];if(!series)return '';
 const cells=(y,h)=>['own','peer','peer_min3'].map(a=>{
  const es=(series[h]?.[y]?.[a]?.events||[]).filter(e=>e.exit<=cutoff),valid=es.filter(e=>finiteReading(e.spread)),m=rbtMean(valid.map(e=>e.spread));
  const fn=ss=>rbtMean(ss.map(e=>e.spread).filter(finiteReading)),b=valid.length>=20?rbtBootstrap(es,h,fn):{ci:null,draws:0,valid_draws:0},long=valid.length>=20?rbtBootstrap(es,h,fn,2):{ci:null,draws:0,valid_draws:0};
  return '<td>'+colored(m,true)+'<small class="cell-sub">'+valid.length+' dates · 95%: '+(b.ci?ci(b.ci):'unavailable')+(b.draws?'<br>Longer blocks: '+(long.ci?ci(long.ci):'unavailable')+'<br>Valid draws: '+b.valid_draws+'/'+b.draws+'; longer '+long.valid_draws+'/'+long.draws:'')+'</small></td>';
 }).join('');
 return '<div class="tiny muted">Gross high − low, equal-weight stocks within each date; fixed 52-week window and default wiki peers. At least 5 stocks per extreme/date; 20 dates required for an interval. This is a cross-stock check, not evidence specific to '+state.ticker+'.</div><div class="table-wrap"><table class="company-table"><thead><tr><th>Year / hold</th><th>Own history</th><th>Peers</th><th>Peers · at least 3</th></tr></thead><tbody>'+['2024','2025','2026'].filter(y=>y<=cutoff.slice(0,4)).flatMap(y=>['5','20'].map(h=>'<tr><td>'+y+' · '+h+'d</td>'+cells(y,h)+'</tr>')).join('')+'</tbody></table></div>';
}
function renderRelativeBacktest(r){
 const target=$('relative-backtest');if(!target)return;
 if(relativeState.year!=='current'&&relativeState.year!=='all'&&relativeState.year>state.date.slice(0,4))relativeState.year='current';
 if(!D.company_studies?.[state.ticker]){target.innerHTML='<article class="card"><h2>Relative-position backtest</h2><div class="note">No aligned forward-return study for this listing. The test currently covers US listings.</div></article>';return;}
 const year=relativeState.year==='current'?state.date.slice(0,4):relativeState.year,basis=relativeState.basis,t=state.ticker,key=state.key,window=comparisonState.window,peers=comparisonPeers(t),events={},stats={};
 ['5','20'].forEach(h=>{events[h]=rbtEvents(t,year,h,key,window,peers,r.cutoff);stats[h]={own:rbtSummary(events[h],'own',h,basis),peer:rbtSummary(events[h],'peer',h,basis)};});
 const all=Object.values(stats).flatMap(s=>[s.own,s.peer]),withCI=all.filter(s=>s.ci),separated=withCI.filter(s=>s.ci[0]>0||s.ci[1]<0),verdict=!withCI.length?'Too little evidence to judge predictive value':separated.length?'Some historical separation; predictive value unvalidated':'No clear separation in this sample';
 target.innerHTML='<div class="comparison-heading"><div><div class="eyebrow">HISTORICAL VALIDATION</div><h2>'+t+' · relative position → forward return</h2></div><div class="comparison-controls"><label>Test period<select id="relative-year" aria-label="Relative backtest period"><option value="current" '+(relativeState.year==='current'?'selected':'')+'>'+state.date.slice(0,4)+' YTD</option>'+['2025','2024'].filter(y=>y<state.date.slice(0,4)).map(y=>'<option value="'+y+'" '+(relativeState.year===y?'selected':'')+'>'+y+'</option>').join('')+'<option value="all" '+(relativeState.year==='all'?'selected':'')+'>All available years</option></select></label><label>Return basis<select id="relative-basis" aria-label="Relative backtest return basis"><option value="absolute" '+(basis==='absolute'?'selected':'')+'>Stock return</option><option value="relative" '+(basis==='relative'?'selected':'')+'>Stock minus QQQ</option></select></label></div></div>'+
 '<div class="relative-verdict"><strong>'+verdict+'</strong><span>'+esc(signalNames[key])+' · '+(window==='ytd'?'YTD':Number(window)/7+'-week')+' own history · '+peers.length+' selected peers · completed exits through '+r.cutoff+'</span></div>'+
 '<div class="relative-grid">'+['5','20'].flatMap(h=>['own','peer'].map(a=>rbtCard(a,h,stats[h][a],basis))).join('')+'</div>'+
 '<details class="relative-details"><summary>When both readings agree — joint return map</summary><div class="relative-grid">'+['5','20'].map(h=>rbtJoint(events[h],h,basis)).join('')+'</div><div class="foot-source">Only holds with both percentiles available. Cell = average realized return; n = holds. Sparse cells are descriptive.</div></details>'+
 '<details class="relative-details"><summary>Does the direction hold across years?</summary><div class="table-wrap">'+rbtYearTable(t,key,window,peers,r.cutoff,basis)+'</div><div class="foot-source">High − low in percentage points. Each axis uses its own eligible events; these are not matched tests of one axis against the other.</div></details>'+
 '<details class="relative-details"><summary>Cross-stock robustness — default baskets</summary>'+rbtPooled(key,r.cutoff)+'</details>'+
 '<details class="relative-details"><summary>Method, timing & event ledger</summary><div class="foot-source">Low: below P30 · middle: P30–P70 (excluding P70) · high: P70 or above. Each percentile uses only prior observations or same-date peer scores. Own history requires 8 readings; a 52-week window can contain less history early in the dataset. Entry is the next session close, then exactly 5 or 20 trading sessions. Fixed schedules do not overlap within a horizon; year-end incomplete holds are excluded.<br><br>Baseline = mean of this company’s same eligible holds for that axis. Dashed line shows it on the bars. Positive fraction is historical, not a forecast probability. Difference = mean(high) − mean(low); stock-minus-QQQ subtracts each hold’s matching QQQ total return. Gross returns, no trading costs or risk-factor neutralization.<br><br>95% exploratory circular-block intervals resample entire scheduled rows (including unavailable rows), with 4-period blocks at 5 sessions or 2 at 20; 1,000 draws, plus a fixed doubled-block sensitivity (8/4 periods). Need at least 20 valid holds, 5 per extreme and 90% valid draws. No multiple-testing adjustment. Current peer membership and watchlist, fiscal-horizon differences, selective text and uncertified original vintages remain. All years were inspected retrospectively: no untouched holdout. <a href="https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf" target="_blank" rel="noopener">Backtest overfitting reference · Bailey et al., 2015</a>.<br><br>Sources: Bloomberg gross total-return indices and dated vendor observations; Capstone archived text. Windows, bands and sample thresholds are ESTIMATE design rules; vintages/text PARTIAL. Download includes missing signals and outcomes.</div><button id="relative-export" class="section-space">Download '+t+' event ledger</button></details>';
 $('relative-year').onchange=()=>{relativeState.year=$('relative-year').value;renderRelativeBacktest(r);};
 $('relative-basis').onchange=()=>{relativeState.basis=$('relative-basis').value;renderRelativeBacktest(r);};
 $('relative-export').onclick=()=>csv('relative-context-'+t+'-'+year+'.csv',[['ticker','indicator','history_window','selected_peers','horizon_sessions','signal','information_cutoff','entry','exit','own_percentile','own_n','peer_percentile','peer_n','gross_stock_return','qqq_return','stock_minus_qqq'],...['5','20'].flatMap(h=>events[h].map(e=>[t,key,window,peers.join(' '),h,e.signal,e.cutoff,e.entry,e.exit,e.own==null?null:e.own*100,e.own_n,e.peer==null?null:e.peer*100,e.peer_n,e.return,e.qqq_return,rbtValue(e,'relative')]))]);
}
