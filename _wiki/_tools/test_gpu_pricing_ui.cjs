// Offline checks of chart/filter/export logic; no browser or external libraries.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const page = fs.readFileSync(path.join(__dirname, '../_dashboards/gpu-pricing.html'), 'utf8');
const data = page.match(/<script type="application\/json" class="gp-data">([\s\S]*?)<\/script>/)[1];
const source = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].at(-1)[1];
function element(value='') {
  return {value, innerHTML:'', textContent:'', events:{}, addEventListener(k,f){this.events[k]=f;}};
}
const nodes = new Map([
  ['.gp-data', {textContent:data}], ['[data-filter="gpu"]',element('H100')],
  ['[data-filter="source"]',element('both')], ['[data-filter="range"]',element('365')],
  ['.gp-chart',element()], ['.gp-legend',element()], ['.gp-hover',element()],
  ['.gp-chart svg',element()], ['.gp-contract-chart',element()], ['[data-export]',element()]
]);
const filters=['gpu','source','range'].map(k=>nodes.get(`[data-filter="${k}"]`));
const root={querySelector:s=>{assert(nodes.has(s),'Unexpected selector: '+s);return nodes.get(s);},querySelectorAll:s=>s==='[data-filter]'?filters:[]};
let downloaded=false;
const document={getElementById:id=>id==='gpu-pricing'?root:null,createElement:()=>({click(){downloaded=true;}})};
vm.runInNewContext(source,{document,Date,console,Blob,URL,setTimeout:f=>f()});
let combinations=0;
for(const gpu of ['H100','A100','B200'])for(const source of ['both','bbg','public'])for(const range of ['90','180','365','all']){
  filters[0].value=gpu;filters[1].value=source;filters[2].value=range;filters[0].events.change();
  assert(nodes.get('.gp-chart').innerHTML.includes('<svg'),'Missing chart for '+[gpu,source,range]);
  assert(!/NaN|undefined|Infinity/.test(nodes.get('.gp-chart').innerHTML));combinations++;
}
assert(nodes.get('.gp-contract-chart').innerHTML.includes('Aug 2026'));
nodes.get('[data-export]').events.click();assert(downloaded);
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
console.log(`PASS: ${combinations} chart selections, contract chart, CSV export and ${redirects.length*4} navigation cases`);
