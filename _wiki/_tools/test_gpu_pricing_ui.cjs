// Offline checks of chart/filter/export logic; no browser or external libraries.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const page = fs.readFileSync(process.env.GPU_PRICING_TEST_PAGE || path.join(__dirname, '../_dashboards/gpu-pricing.html'), 'utf8');
const data = page.match(/<script type="application\/json" class="gp-data">([\s\S]*?)<\/script>/)[1];
const source = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].at(-1)[1];
function element(value='') {
  return {value, innerHTML:'', textContent:'', events:{}, addEventListener(k,f){this.events[k]=f;}};
}
const nodes = new Map([
  ['.gp-data', {textContent:data}], ['[data-filter="gpu"]',element('H100')],
  ['[data-filter="source"]',element('both')], ['[data-filter="range"]',element('365')],
  ['[data-filter="scale"]',element('fit')], ['.gp-axis-note',element()], ['.gp-contract-axis-note',element()],
  ['.gp-chart',element()], ['.gp-legend',element()], ['.gp-hover',element()],
  ['.gp-chart svg',element()], ['.gp-contract-chart',element()], ['[data-export]',element()]
]);
const filters=['gpu','source','range','scale'].map(k=>nodes.get(`[data-filter="${k}"]`));
const root={querySelector:s=>{assert(nodes.has(s),'Unexpected selector: '+s);return nodes.get(s);},querySelectorAll:s=>s==='[data-filter]'?filters:[]};
let downloaded=false;
const document={getElementById:id=>id==='gpu-pricing'?root:null,createElement:()=>({click(){downloaded=true;}})};
vm.runInNewContext(source,{document,Date,console,Blob,URL,setTimeout:f=>f()});
let combinations=0;
for(const gpu of ['H100','A100','B200'])for(const source of ['both','bbg','public'])for(const range of ['90','180','365','all'])for(const scale of ['fit','zero']){
  filters[0].value=gpu;filters[1].value=source;filters[2].value=range;filters[3].value=scale;filters[0].events.change();
  assert(nodes.get('.gp-chart').innerHTML.includes('<svg'),'Missing chart for '+[gpu,source,range]);
  const svg=nodes.get('.gp-chart').innerHTML;
  assert(!/NaN|undefined|Infinity/.test(svg));
  const lo=Number(svg.match(/data-y-min="([^"]+)"/)[1]),hi=Number(svg.match(/data-y-max="([^"]+)"/)[1]);
  assert(hi>lo,'Non-positive axis span');assert(lo>=0);
  if(scale==='zero')assert.equal(lo,0);
  else if(range==='90')assert(lo>0,'Expected a fitted scale for the recent window');
  // Every line coordinate must fit between the chart's top and bottom edges.
  for(const path of svg.matchAll(/<path d="([^"]*)"/g))for(const point of path[1].matchAll(/[ML]([\d.]+),([\d.]+)/g)){
    assert(Number(point[2])>=17.99 && Number(point[2])<=298.01,'Clipped observation');
  }
  assert(nodes.get('.gp-axis-note').textContent.includes('Grid interval'));
  assert(!/NaN|undefined|Infinity/.test(nodes.get('.gp-contract-chart').innerHTML));combinations++;
}
assert(nodes.get('.gp-contract-chart').innerHTML.includes('Aug 2026'));
nodes.get('[data-export]').events.click();assert(downloaded);
// Flat prices still need a non-zero, tight axis; sparse/empty feeds should be legible.
const fixture=JSON.parse(data);
for(const s of fixture.series)s.points=[['2026-09-24',2.5],['2026-09-25',2.5]];
nodes.get('.gp-data').textContent=JSON.stringify(fixture);
filters[0].value='H100';filters[1].value='both';filters[2].value='all';filters[3].value='fit';
vm.runInNewContext(source,{document,Date,console,Blob,URL,setTimeout:f=>f()});
assert(!/NaN|undefined|Infinity/.test(nodes.get('.gp-chart').innerHTML));
assert(nodes.get('.gp-axis-note').textContent.includes('does not start at zero'));
nodes.get('.gp-data').textContent=JSON.stringify({...fixture,series:[],contracts:[]});
vm.runInNewContext(source,{document,Date,console,Blob,URL,setTimeout:f=>f()});
assert(nodes.get('.gp-chart').innerHTML.includes('No observations'));
assert(nodes.get('.gp-contract-chart').innerHTML.includes('No contract ranges'));
const redirects=process.argv.slice(2);
for(const file of redirects){
 const html=fs.readFileSync(file,'utf8'),script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
 const leaf=file.includes('gpu-pricing')?'gpu-pricing':'openrouter';
 for(const [protocol,port,pathname,expected] of [
  ['http:','8080','/dashboards/link/',`/wiki/_dashboards/${leaf}.html`],
  ['http:','8775','/link/',`http://localhost:8774/_wiki/_dashboards/${leaf}.html`],
  ['file:','','/R:/Wiki/dashboards/link/index.html',`../../_wiki/_dashboards/${leaf}.html`],
  ['https:','','/Capstone-Wiki/link/',`http://DS-CAP-33:8080/wiki/_dashboards/${leaf}.html`]]){
   let dest;vm.runInNewContext(script,{location:{protocol,port,pathname,replace:s=>dest=s},document:{getElementById:()=>({})}});assert.equal(dest,expected);
 }
}
console.log(`PASS: ${combinations} chart selections and fitted axes, flat/empty feeds, contract chart, CSV export and ${redirects.length*4} navigation cases`);
