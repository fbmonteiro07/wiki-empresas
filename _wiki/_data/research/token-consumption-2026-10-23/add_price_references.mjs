import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';

const here=path.dirname(fileURLToPath(import.meta.url));
const src='E:/Wiki Felipe empresas/outputs/01a168b5-7786-7582-8082-7cd6bd45fd69/AI_Token_Consumption_and_Minimum_Price.xlsx';
const dest=src.replace('.xlsx','_with_References.xlsx');
const data=JSON.parse(await fs.readFile(path.join(here,'price_references.json'),'utf8'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(src));
const oldNames=['Consumption','Minimum price','Token mix','Inputs'];
const before=Object.fromEntries(oldNames.map(n=>[n,JSON.stringify({values:wb.worksheets.getItem(n).getRange('A1:P310').values,formulas:wb.worksheets.getItem(n).getRange('A1:P310').formulas})]));
const s=wb.worksheets.add('Price references');
const navy='#173451',ink='#142D4E',pale='#EAF0F6',gray='#65758B';
s.showGridLines=false;s.tabColor='#7894B0';
s.getRange('A1:N90').format.font={name:'Arial',size:10,color:ink};
s.getRange('A1:N90').format.verticalAlignment='center';
s.getRange('A1:N90').format.rowHeight=22;
for(const [c,width]of Object.entries({A:2.5,B:2.5,C:13,D:12,E:25,F:23,G:11,H:12,I:11,J:23,K:51,L:2.5,M:35,N:3}))s.getRange(`${c}1:${c}90`).format.columnWidth=width;
const value=(a,v)=>s.getRange(a).values=[[v]];
value('C2','Token price references and dated changes');s.getRange('C2').format.font={name:'Arial',size:15,bold:true,color:ink};
s.getRange('C3:M3').format.borders={bottom:{style:'thin',color:navy}};
value('C4','USD per 1 million tokens. Base input, cached input and output have different rates. Full source URLs are listed below the tables.');
value('C5','Verified October 23, 2026. HARD = published vendor rate or event; transferring list prices to realized company ASP remains PARTIAL.');
value('C6','References document price history and billing terms. The consumption model continues to use its existing Ramp benchmarks.');
s.getRange('C4:M6').format.font.color=gray;
s.freezePanes.freezeRows(9);s.freezePanes.freezeColumns(2);
const headers=['Reference date','Provider','Model / scope','Evidence / event','Input $/M','Cache read $/M','Output $/M','Context / tier','Interpretation',null,'Source / date'];
function section(r,title){value('C'+r,title);s.getRange(`C${r}:M${r}`).format.fill=pale;s.getRange(`C${r}:M${r}`).format.font.bold=true;s.getRange(`C${r}:M${r}`).format.borders={bottom:{style:'thin',color:'#B3C1D0'}};}
function head(r){s.getRange(`C${r}:M${r}`).values=[headers];s.getRange(`C${r}:M${r}`).format.fill=navy;s.getRange(`C${r}:M${r}`).format.font={name:'Arial',size:10,color:'#FFFFFF',bold:true};s.getRange(`C${r}:M${r}`).format.wrapText=true;s.getRange(`C${r}:M${r}`).format.rowHeight=32;}
const sourceKeys=Object.keys(data.sources);
const sourceId=key=>'['+String(sourceKeys.indexOf(key)+1).padStart(2,'0')+']';
function source(r,key){const [title]=data.sources[key];value(`M${r}`,sourceId(key)+' '+title);}
function rows(start,records){
  s.getRange(`C${start}:M${start+records.length-1}`).values=records.map(x=>[new Date(x[0]+'T00:00:00Z'),...x.slice(1,4),...x.slice(4,7).map(v=>v===null?'n.q.':v),x[7],x[8],null,null]);
  s.getRange(`C${start}:C${start+records.length-1}`).setNumberFormat('dd-mmm-yy');
  s.getRange(`C${start}:C${start+records.length-1}`).format.horizontalAlignment='left';
  s.getRange(`G${start}:I${start+records.length-1}`).setNumberFormat('$0.00##');
  s.getRange(`G${start}:I${start+records.length-1}`).format.horizontalAlignment='right';
  s.getRange(`J${start}:J${start+records.length-1}`).format.horizontalAlignment='center';
  s.getRange(`C${start}:M${start+records.length-1}`).format.wrapText=true;
  s.getRange(`C${start}:M${start+records.length-1}`).format.rowHeight=48;
  records.forEach((x,i)=>{source(start+i,x[9]);if(i%2===1)s.getRange(`C${start+i}:K${start+i}`).format.fill='#F7F9FB';});
}
section(8,'Dated historical evidence — launch prices, effective-date lists and announced changes');head(9);rows(10,data.history);
let currentSection=10+data.history.length+2;section(currentSection,'Current rate-card checks — observed October 23; earlier-model cards are not archived historical observations');head(currentSection+1);rows(currentSection+2,data.current);
let modifierSection=currentSection+2+data.current.length+2;section(modifierSection,'Billing terms that affect comparisons');head(modifierSection+1);rows(modifierSection+2,data.modifiers);
let end=modifierSection+2+data.modifiers.length+2;section(end,'How these references relate to the model');
const explanations=[
 ['Published list prices are model- and token-category-specific. A provider blended ASP also needs actual model mix, cache use, output mix and contract terms.','op'],
 ['Ramp Economics Lab / Ara Kharazian: observed sample pricing and model shares. Company-wide representativeness is not validated.','ramp'],
 ['tokenPrices: published all-token cost / count benchmark. Saved vintage through October 11 is the source for the workbook monthly average.','rp'],
 ['tokenVolumes: model-level spend and volume used for the paired-model reference. Its token denominator differs from tokenPrices.','rv'],
 ['The minimum reference remains the lower of the two Ramp benchmarks. Vendor list prices do not resolve that gap or establish a company minimum ASP.','ramp'],
 ['n.q. means not separately quoted in that dated source/row, not zero. Snapshot rows do not prove prices were unchanged since the model launched.','ap']
];
for(const [i,[note,key]]of explanations.entries()){let r=end+2+i;s.getRange(`C${r}:K${r}`).merge();value(`C${r}`,note);s.getRange(`C${r}:K${r}`).format.wrapText=true;s.getRange(`C${r}:M${r}`).format.rowHeight=38;source(r,key);s.getRange(`M${r}`).format.wrapText=true;}
const notesLast=end+1+explanations.length;
const sourceSection=notesLast+3;
section(sourceSection,'Source directory — publisher, dated evidence and exact URLs');
for(const [i,key]of sourceKeys.entries()){const r=sourceSection+2+i;value('C'+r,sourceId(key));s.getRange(`D${r}:F${r}`).merge();value('D'+r,data.sources[key][0]);s.getRange(`G${r}:M${r}`).merge();value('G'+r,data.sources[key][1]);s.getRange(`G${r}:M${r}`).format.font.color='#0563C1';s.getRange(`C${r}:M${r}`).format.wrapText=true;s.getRange(`C${r}:M${r}`).format.rowHeight=34;}
const last=sourceSection+1+sourceKeys.length;
s.getRange(`A${last+1}:N90`).clear({applyTo:'formats'});
wb.recalculate();
for(const n of oldNames){const after=JSON.stringify({values:wb.worksheets.getItem(n).getRange('A1:P310').values,formulas:wb.worksheets.getItem(n).getRange('A1:P310').formulas});if(before[n]!==after)throw Error('Existing content changed: '+n);}
const scan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30},summary:'Reference update error scan'});
await fs.writeFile(path.join(here,'reference_error_scan.jsonl'),scan.ndjson);
const previews=[['references_history',`C1:M${10+data.history.length-1}`],['references_current',`C${currentSection}:M${currentSection+1+data.current.length}`],['references_terms',`C${modifierSection}:M${notesLast}`],['reference_sources',`C${sourceSection}:M${last}`]];
for(const [name,range]of previews){const b=await wb.render({sheetName:'Price references',range,scale:1.3,format:'png'});await fs.writeFile(path.join(here,name+'.png'),new Uint8Array(await b.arrayBuffer()));}
await(await SpreadsheetFile.exportXlsx(wb)).save(dest);
await fs.writeFile(path.join(here,'reference_update_verification.json'),JSON.stringify({source:src,output:dest,history_rows:data.history.length,current_rows:data.current.length,modifier_rows:data.modifiers.length,source_count:Object.keys(data.sources).length,old_tabs_unchanged:true,formula_scan:scan.ndjson,sections:{currentSection,modifierSection,end,last}},null,2));
console.log(JSON.stringify({output:dest,history_rows:data.history.length,current_rows:data.current.length,modifier_rows:data.modifiers.length,old_tabs_unchanged:true,formula_scan:scan.ndjson},null,2));
