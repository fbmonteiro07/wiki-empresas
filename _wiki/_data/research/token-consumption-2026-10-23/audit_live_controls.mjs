// Read-only stress test: temporary in-memory edits; no workbook is exported.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const here=path.dirname(fileURLToPath(import.meta.url));
const source='R:/AI_Token_Consumption_and_Minimum_Price_with_References.xlsx';
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(source));
const inp=wb.worksheets.getItem('Inputs'),con=wb.worksheets.getItem('Consumption'),pb=wb.worksheets.getItem('Price build'),min=wb.worksheets.getItem('Minimum price');
const get=(s,a)=>s.getRange(a).values[0][0],set=(s,a,v)=>s.getRange(a).values=[[v]];
const snapshot=()=>({anth_price:get(con,'N16'),anth_full:get(con,'N17'),anth_api:get(con,'N18'),oai_price:get(con,'N34'),oai_full:get(con,'N35'),oai_api:get(con,'N36'),anth_dec_price:get(con,'O16'),oai_dec_price:get(con,'O34'),anth_ref:get(min,'N12'),oai_ref:get(min,'N28')});
wb.recalculate();const baseline=snapshot(),out=[];
for(const [name,sheet,cell,changes]of [
 ['ARR basis',inp,'D4',[2,0,3,'invalid']],
 ['Anth API share',inp,'N10',[0,1,-.1,1.1,'invalid']],
 ['OpenAI API share',inp,'N16',[0,1,-.1,1.1,'invalid']],
 ['Forecast price change',inp,'D5',[-1,-1.01,'invalid',-.1,.1]],
 ['Anth input weight',pb,'N27',[0,1,-.1,1.1,'invalid']],
 ['OpenAI output weight',pb,'N68',[0,1,-.1,1.1,'invalid']],
]){
 const old=get(sheet,cell);
 for(const val of changes){set(sheet,cell,val);wb.recalculate();out.push({name,cell,input:val,result:snapshot()});}
 if(old===null||old===undefined||old==='')sheet.getRange(cell).clear({applyTo:'contents'});else set(sheet,cell,old);wb.recalculate();
}
// A feasible low-output/high-residual mix can put selected price below the reference.
for(const [cell,value]of [['N27',.01],['N28',0],['N29',.99],['N67',.01],['N68',0],['N69',.99]])set(pb,cell,value);
wb.recalculate();out.push({name:'Valid residual-heavy forecast mix',active:{anth:pb.getRange('N14:N16').values,oai:pb.getRange('N54:N56').values},result:snapshot()});
for(const b of [9,49])for(const c of ['N','O'])for(let k=0;k<3;k++){
 const prev=c==='N'?'M':'N';pb.getRange(c+(b+5+k)).formulas=[[`=IF(ISBLANK(${c}${b+18+k}),${prev}${b+5+k},${c}${b+18+k})`]];
}
wb.recalculate();out.push({name:'ISBLANK zero override test',active:{anth:pb.getRange('N14:N16').values,oai:pb.getRange('N54:N56').values},result:snapshot()});
for(const range of ['N27:N29','N67:N69'])pb.getRange(range).clear({applyTo:'contents'});wb.recalculate();
const end=snapshot();if(JSON.stringify(baseline)!==JSON.stringify(end))throw Error('Inputs not restored in memory');
const result={source,read_only:true,baseline,cases:out};
await fs.writeFile(path.join(here,'audit_live_controls.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify(result,null,2));
