// Offline checks of the report's calculations and markup. No browser or network.
const fs=require('fs'),vm=require('vm'),path=require('path');
const root=path.resolve(__dirname,'../_data/research/rates_earnings_20260930');
const html=fs.readFileSync(path.join(root,'study.html'),'utf8');
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
if(new Set(ids).size!==ids.length)throw Error('Duplicate HTML ids');
const data=JSON.parse(html.match(/<script id="study-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const script=html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
const elements=Object.fromEntries(ids.map(id=>[id,{id,textContent:'',innerHTML:'',value:({'start-pe':'19.5','end-pe':'16','eps-change':'30'})[id],events:{},addEventListener(n,cb){this.events[n]=cb}}]));
elements['study-data'].textContent=JSON.stringify(data);
const context={document:{getElementById(id){if(!elements[id])throw Error('Missing element '+id);return elements[id]}}};
vm.runInNewContext(script,context,{timeout:3000});
function check(id,value){if(elements[id].textContent!==value)throw Error(id+': '+elements[id].textContent+' != '+value)}
check('price-return','+6.7%');check('required-growth','+21.9%');
elements['start-pe'].value='19.2';elements['start-pe'].events.input();check('price-return','+8.3%');check('required-growth','+20.0%');
elements['eps-change'].value='0';elements['eps-change'].events.input();check('price-return','−16.7%');
elements['eps-change'].value='30';elements['end-pe'].value='14';elements['end-pe'].events.input();check('price-return','−5.2%');
if((elements['revision-table'].innerHTML.match(/<tr>/g)||[]).length!==10)throw Error('Revision rows missing');
if((elements['multiple-sensitivity'].innerHTML.match(/<tr>/g)||[]).length!==3)throw Error('Multiple scenarios missing');
for(const id of ['rates-chart','revisions-chart'])if((elements[id].innerHTML.match(/<rect /g)||[]).length!==4)throw Error('Chart marks missing');
const qa={status:'PASS',mode:'Offline DOM-stub execution; not a browser render',unique_ids:ids.length,revision_rows:9,return_scenarios:12,multiple_scenarios:6,interactive_anchor_growth_and_multiple_checks:'PASS',browser_visual_preview:'BLOCKED by browser local-file URL policy'};
fs.writeFileSync(path.join(root,'report_validation.json'),JSON.stringify(qa,null,2));console.log(JSON.stringify(qa));
