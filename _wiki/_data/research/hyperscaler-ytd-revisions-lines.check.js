
    (() => {
      const root = document.getElementById('hyperscaler-revision-lines');
      const payload = JSON.parse(root.querySelector('#revision-lines-data').textContent);
      const tickers = ['MSFT','META','GOOG','AMZN'];
      const colors = Object.fromEntries(tickers.map((t,i)=>[t,`var(--viz-series-${i+1})`]));
      const dashes = {MSFT:null,META:'7 3',GOOG:'2 3',AMZN:'10 3 2 3'};
      const saved = window.openai?.widgetState?.privateContent?.visible;
      const visible = new Set(Array.isArray(saved) ? saved.filter(t=>tickers.includes(t)) : tickers);
      const tooltip = root.querySelector('#revision-lines-tooltip');
      const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const series = payload.series.map(s=>({...s,points:s.points.map(p=>({...p,date:new Date(p.date+'T00:00:00Z'),x:Date.parse(p.date+'T00:00:00Z')}))}));
      const xDomain = d3.extent(series.flatMap(s=>s.points),p=>p.date);
      const domains = {};
      ['eps','capex'].forEach(metric=>{
        const extent = d3.extent(series.filter(s=>s.metric===metric).flatMap(s=>s.points),p=>p.index);
        const pad = (extent[1]-extent[0])*.10;
        domains[metric] = d3.scaleLinear().domain([extent[0]-pad,extent[1]+pad]).nice(4).domain();
      });
      const pct = n=>(n>=0?'+':'')+n.toFixed(1)+'%';
      const money = (v,m)=>'$'+v.toFixed(m==='eps'?2:1)+(m==='capex'?'bn':'');
      const fmtDate = d3.utcFormat('%b %d, %Y');
      const legend = root.querySelector('#revision-lines-legend');
      tickers.forEach(t=>{
        const button=document.createElement('button');
        button.type='button';button.className='cursor-interaction';button.dataset.ticker=t;
        button.setAttribute('aria-pressed',String(visible.has(t)));
        button.setAttribute('aria-label','Show or hide '+t+' in all charts');
        button.innerHTML=`<svg class="legend-swatch" aria-hidden="true"><line x1="1" y1="6" x2="25" y2="6" stroke="${colors[t]}" stroke-width="2.5" ${dashes[t]?`stroke-dasharray="${dashes[t]}"`:''}/></svg><span>${t}</span>`;
        button.addEventListener('click',()=>{
          if(visible.has(t)) visible.delete(t); else visible.add(t);
          button.setAttribute('aria-pressed',String(visible.has(t)));drawAll(true);
          window.openai?.setWidgetState?.({modelContent:{visibleCompanies:[...visible],metric:'EPS and capex YTD revisions',years:[2027,2028]},privateContent:{visible:[...visible]}})?.catch(()=>{});
        });
        legend.append(button);
      });
      function draw(metric,year,animate=false) {
        const node=root.querySelector(`#lines-${metric}-${year}`), svg=d3.select(node);
        const W=node.parentElement.getBoundingClientRect().width,H=292;
        const L=64,R=W-10,T=24,B=239,endX=R-102;
        const x=d3.scaleUtc().domain(xDomain).range([L+3,endX]);
        const y=d3.scaleLinear().domain(domains[metric]).range([B-3,T+3]);
        const rows=series.filter(s=>s.metric===metric&&s.year===year&&visible.has(s.ticker));
        const line=d3.line().x(p=>x(p.date)).y(p=>y(p.index));
        const oldPaths=new Map([...node.querySelectorAll('.series-line')].map(n=>[n.dataset.ticker,n.getAttribute('d')]));
        svg.attr('viewBox',`0 0 ${W} ${H}`).attr('height',H);svg.selectAll('*').remove();
        svg.append('title').text(`${year} ${metric==='eps'?'EPS':'capex'} revision history`);
        svg.append('desc').text(rows.map(s=>`${s.ticker}: starts at index 100; October 29 YTD change ${pct(s.latest_revision_pct)}.`).join(' '));
        svg.append('rect').attr('data-chart-frame','').attr('x',L).attr('y',T).attr('width',R-L).attr('height',B-T).attr('fill','none').attr('stroke','var(--border)');
        y.ticks(4).forEach(v=>{
          svg.append('line').attr('class',v===100?'baseline':'grid').attr('x1',L).attr('x2',R).attr('y1',y(v)).attr('y2',y(v));
          svg.append('text').attr('x',L-10).attr('y',y(v)+4).attr('text-anchor','end').attr('class','axis-label tabular-nums').text(v);
        });
        const dates=(W<390?[1,4,7,10]:[1,3,5,7,9]).map(m=>new Date(Date.UTC(2026,m-1,1)));
        dates.forEach(d=>{
          svg.append('line').attr('class','grid').attr('x1',x(d)).attr('x2',x(d)).attr('y1',T).attr('y2',B);
          svg.append('text').attr('x',x(d)).attr('y',B+21).attr('text-anchor','middle').attr('class','axis-label').text(d3.utcFormat('%b')(d));
        });
        svg.append('text').attr('class','axis-title axis-label').attr('data-axis','y').attr('x',L).attr('y',13).text('Revision index');
        svg.append('text').attr('class','axis-title axis-label').attr('data-axis','x').attr('x',(L+endX)/2).attr('y',H-5).attr('text-anchor','middle').text('2026 observation date');
        const endLabels=[];
        rows.forEach(s=>{
          const path=svg.append('path').attr('class','series-line').attr('data-ticker',s.ticker).attr('stroke',colors[s.ticker]).attr('stroke-dasharray',dashes[s.ticker]);
          const target=line(s.points),old=oldPaths.get(s.ticker);
          if(animate&&old&&!reducedMotion) path.attr('d',old).transition().duration(220).attr('d',target); else path.attr('d',target);
          const last=s.points.at(-1);
          svg.append('circle').attr('cx',x(last.date)).attr('cy',y(last.index)).attr('r',3).attr('fill',colors[s.ticker]);
          endLabels.push({s,actualY:y(last.index),labelY:y(last.index)});
        });
        endLabels.sort((a,b)=>a.actualY-b.actualY);
        endLabels.forEach((v,i)=>{v.labelY=Math.max(T+12,v.labelY,i?endLabels[i-1].labelY+19:T+12);});
        for(let i=endLabels.length-1;i>=0;i--) endLabels[i].labelY=Math.min(endLabels[i].labelY,i===endLabels.length-1?B-10:endLabels[i+1].labelY-19);
        endLabels.forEach(({s,actualY,labelY})=>{
          svg.append('path').attr('d',`M${endX+3},${actualY} L${endX+8},${labelY}`).attr('fill','none').attr('stroke','var(--muted-foreground)').attr('stroke-width',1);
          svg.append('text').attr('x',endX+12).attr('y',labelY+4).attr('class','tabular-nums endpoint-label').text(s.ticker+' '+pct(s.latest_revision_pct));
        });
        const hover=svg.append('g').attr('display','none');
        hover.append('line').attr('data-chart-hover-guide','').attr('y1',T).attr('y2',B).attr('stroke','var(--muted-foreground)').attr('stroke-width',1);
        const circles=hover.selectAll('circle').data(rows).join('circle').attr('data-chart-hover-marker','').attr('r',4).attr('fill',s=>colors[s.ticker]).attr('stroke','var(--background)').attr('stroke-width',1);
        let pinned=false;
        function show(event) {
          if(!rows.length)return;
          const mx=Math.max(L+3,Math.min(endX,d3.pointer(event,node)[0])),time=+x.invert(mx);
          hover.attr('display',null);hover.select('line').attr('x1',mx).attr('x2',mx);
          const vals=rows.map(s=>{
            const nearest=d3.bisector(p=>p.x).center(s.points,time);
            let lo=nearest,hi=nearest;
            if(s.points[nearest].x>time)lo=Math.max(0,nearest-1);else hi=Math.min(s.points.length-1,nearest+1);
            const a=s.points[lo],b=s.points[hi],f=b.x===a.x?0:(time-a.x)/(b.x-a.x);
            const value=a.value+(b.value-a.value)*f;
            return {s,value,index:value/s.baseline*100};
          });
          circles.attr('cx',mx).attr('cy',(_,i)=>y(vals[i].index));
          tooltip.innerHTML=`<div>${fmtDate(new Date(time))} · FY${year} ${metric==='eps'?'EPS':'capex'}</div><div class="tip-grid"><span></span><span>Estimate</span><span>YTD</span>${vals.map(v=>`<span>${v.s.ticker}</span><span class="number">${money(v.value,metric)}</span><span class="number">${pct(v.index-100)}</span>`).join('')}</div><div class="text-small" style="margin-top:8px">Interpolated along the lines · Bloomberg BEst</div>`;
          tooltip.hidden=false;
          const box=root.getBoundingClientRect();
          const left=Math.min(Math.max(8,event.clientX-box.left+14),Math.max(8,box.width-tooltip.offsetWidth-8));
          const top=Math.min(Math.max(8,event.clientY-box.top+14),Math.max(8,box.height-tooltip.offsetHeight-8));
          tooltip.style.left=left+'px';tooltip.style.top=top+'px';
        }
        svg.append('rect').attr('data-chart-hit','').attr('data-chart-hover-overlay','cross-series').attr('x',L).attr('y',T).attr('width',endX-L).attr('height',B-T).attr('fill','transparent')
          .on('pointermove',event=>{if(!pinned)show(event);})
          .on('pointerleave',()=>{if(!pinned){hover.attr('display','none');tooltip.hidden=true;}})
          .on('click',event=>{pinned=!pinned;if(pinned)show(event);else{hover.attr('display','none');tooltip.hidden=true;}});
        // Remove optional labels only if actual text bounds cannot fit.
        const bounds=node.getBoundingClientRect();
        [...node.querySelectorAll('.endpoint-label')].forEach(label=>{
          const box=label.getBoundingClientRect();
          if(box.right>bounds.right-2)label.textContent=label.textContent.replace(/\.\d%$/,'%');
        });
      }
      function drawAll(animate=false) {
        tooltip.hidden=true;
        ['eps','capex'].forEach(m=>[2027,2028].forEach(y=>draw(m,y,animate)));
      }
      new ResizeObserver(()=>drawAll()).observe(root);
      window.addEventListener('openai:set_globals',event=>{
        const v=event.detail?.globals?.widgetState?.privateContent?.visible;
        if(!Array.isArray(v))return;
        visible.clear();v.filter(t=>tickers.includes(t)).forEach(t=>visible.add(t));
        legend.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(visible.has(b.dataset.ticker))));
        drawAll(true);
      });
      drawAll();
    })();
  