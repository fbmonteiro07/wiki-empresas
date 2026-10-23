import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const here=path.dirname(fileURLToPath(import.meta.url));
const dir='E:/Wiki Felipe empresas/outputs/01a168b5-7786-7582-8082-7cd6bd45fd69';
const source=path.join(dir,'AI_Token_Consumption_Price_and_Mix.xlsx');
const output=path.join(dir,'AI_Token_Consumption_Price_and_Mix_Audited.xlsx');
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(source));
const inp=wb.worksheets.getItem('Inputs'),cons=wb.worksheets.getItem('Consumption'),pb=wb.worksheets.getItem('Price build'),min=wb.worksheets.getItem('Minimum price'),refs=wb.worksheets.getItem('Price references');
const data=JSON.parse(await fs.readFile(path.join(here,'model_inputs.json'),'utf8'));
const cols='DEFGHIJKLMNO'.split('');
const C={ink:'#142D4E',navy:'#173451',pale:'#EAF0F6',gray:'#65758B',blue:'#DDEBF7',red:'#FCE4D6'};
const val=(s,a,v)=>s.getRange(a).values=[[v]],form=(s,a,f)=>s.getRange(a).formulas=[[f]],get=(s,a)=>s.getRange(a).values[0][0];
const close=(a,b,k)=>{if(typeof a!=='number'||Math.abs(a-b)>1e-9*Math.max(1,Math.abs(b)))throw Error(`${k}: ${a} != ${b}`);};
function format(s,start,end){s.getRange(`C${start}:O${end}`).format.font={name:'Arial',size:10,color:C.ink};s.getRange(`C${start}:O${end}`).format.verticalAlignment='center';s.getRange(`C${start}:O${end}`).format.rowHeight=22;}
function note(s,row,text,height=32,last='O'){s.getRange(`C${row}:${last}${row}`).merge();val(s,'C'+row,text);s.getRange(`C${row}:${last}${row}`).format.wrapText=true;s.getRange(`C${row}:${last}${row}`).format.rowHeight=height;s.getRange(`C${row}:${last}${row}`).format.font.color=C.gray;}
function section(s,row,text,last='O'){val(s,'C'+row,text);s.getRange(`C${row}:${last}${row}`).format.fill=C.pale;s.getRange(`C${row}:${last}${row}`).format.font.bold=true;s.getRange(`C${row}:${last}${row}`).format.borders={bottom:{style:'thin',color:'#B3C1D0'}};}

// Distinguish an explicit zero override from a truly blank cell in every engine.
for(const b of [9,49])for(const c of ['N','O'])for(let k=0;k<3;k++){
 const prev=c==='N'?'M':'N';form(pb,c+(b+5+k),`=IF(ISBLANK(${c}${b+18+k}),${prev}${b+5+k},${c}${b+18+k})`);
}

// Type/range guards include both gross and net API revenue. ROUND only removes
// sub-cent floating-point residuals ($bn rounded to 12dp); it does not clamp
// an economically negative revenue or an out-of-range source assumption.
for(const [provider,cr,gr,nr,sr]of [['anthropic',9,8,9,10],['openai',27,14,15,16]])for(const c of cols){
 const G=`${c}${cr+1}`,N=`${c}${cr+2}`,share=`Inputs!${c}${sr}`;
 for(const [out,input]of [[G,`${c}${gr}`],[N,`${c}${nr}`]])form(cons,out,`=IF(AND(ISNUMBER(Inputs!${input}),Inputs!${input}>=0),Inputs!${input}/1000,"n.a.")`);
 form(cons,c+(cr+3),`=IF(AND(ISNUMBER(${G}),ISNUMBER(${N})),IF(AND(${G}>=0,${N}>=0,${G}>=${N}),IF(Inputs!$D$4=1,${G},IF(Inputs!$D$4=2,${N},"n.a.")),"n.a."),"n.a.")`);
 const rawGross=provider==='anthropic'?`${G}*${share}`:`${N}*${share}+${G}-${N}`;
 const rawNet=provider==='anthropic'?`${G}*${share}-(${G}-${N})`:`${N}*${share}`;
 const ag=`ROUND(${rawGross},12)`,an=`ROUND(${rawNet},12)`;
 form(cons,c+(cr+5),`=IF(AND(ISNUMBER(${share}),ISNUMBER(${G}),ISNUMBER(${N})),IF(AND(${G}>0,${N}>0,${G}>=${N},${share}>=0,${share}<=1,${ag}>=0,${an}>=0,${ag}<=ROUND(${G},12),${an}<=ROUND(${N},12)),IF(Inputs!$D$4=1,ROUND(${ag}/${G},12),IF(Inputs!$D$4=2,ROUND(${an}/${N},12),"n.a.")),"n.a."),"n.a.")`);
}
for(const row of [10,16])inp.getRange(`D${row}:O${row}`).dataValidation={rule:{type:'decimal',operator:'between',formula1:0,formula2:1},errorAlert:{style:'stop',title:'Invalid API share',message:'Enter a numeric share between 0% and 100%. Implied gross and net API revenue must both be nonnegative under the stated channel assumption.'}};
for(const range of ['D8:O9','D14:O15'])inp.getRange(range).dataValidation={rule:{type:'decimal',operator:'greaterThanOrEqual',formula1:0},errorAlert:{style:'stop',title:'Invalid ARR',message:'Enter nonnegative numeric ARR in USD millions; gross ARR must be at least net ARR.'}};

// Put limitations and the audited boundary conditions next to the outputs.
note(cons,5,'Conditional API-equivalent scenarios. API-only is the closer revenue basis; full ARR includes subscriptions. Q = 10^15 tokens; T = 10^12.',30);
note(cons,6,'PARTIAL: Ramp cost is not verified as billed/recognized revenue, and its token universe is not reconciled to company traffic. Price build shows the assumptions.',30);
val(cons,'C52','Anthropic: unclassified residual*');val(cons,'C56','OpenAI: unclassified residual*');
note(cons,58,'*Possible cache / other proxy, not measured cache reads or writes. Price build shows the residual arithmetic, effective rates and editable forecast weights.',32);
format(cons,60,74);section(cons,60,'General double-check — October 23, 2026');
for(const [row,api,label]of [[61,14,'Anthropic API allocation validity'],[62,32,'OpenAI API allocation validity']]){
 val(cons,'C'+row,label);for(const c of cols)form(cons,c+row,`=IF(ISNUMBER(${c}${api}),"PASS","INVALID")`);
 cons.getRange(`D${row}:O${row}`).conditionalFormats.add('cellIs',{operator:'equal',formula:'"INVALID"',format:{fill:C.red,font:{color:'#9C0006',bold:true}}});
}
note(cons,64,'Arithmetic PASS at the supplied inputs: 48 ARR values and 24 API-share copies matched the original; 3,278 values and 2,337 pre-fix formula caches independently checked.');
note(cons,65,'Control fixes: negative/over-100% API shares and inconsistent gross/net API revenue now return n.a.; zero mix overrides are honored. Default prices and volumes are unchanged within numerical precision.');
note(cons,66,'Evidence PARTIAL: reported costs may differ from billing. Ramp documents overage-rate estimates for some OpenAI credit plans; applicability to this public Index is unconfirmed.');
note(cons,67,'Unresolved: company representativeness, common token universe, cache-read/write split and an economic minimum price. The price bridge is an accounting identity, not external validation.');
note(cons,68,'Period: October uses September 28–October 11. November/December are forecasts. Historical rate-card evidence and current snapshots were checked separately; all 37 quoted rows are supported.');
note(cons,70,'Original-model ambiguity retained: AI Model.xlsx ARR Tracker!P28 = P7 × (1 + P29 × P30), with P29 = 20% and P30 the net-revenue API/cloud share.');
note(cons,71,'The source labels P29 as CSP take but does not specify whether its denominator is net receipts or gross billings. If the latter, the channel gross-up is 1/(1−20%), not 1+20%.');
note(cons,72,'Conditional implication: OpenAI gross API revenue/volume would be 2.27% higher if the 20% were a share of gross billings. No source assumption has been silently changed; this is not a revised forecast.');
note(cons,74,'Audit sources: original AI Model.xlsx saved October 23; Ramp raw feeds and support documentation; 37 official vendor price/event references. Supporting links are on Price references.');

format(inp,370,373);section(inp,370,'Audit of editable source assumptions');
note(inp,371,'API shares must be numeric and 0–100%. Both implied gross and net API revenues must remain between zero and their matching ARR totals; invalid allocations return n.a.');
note(inp,372,'Anthropic gross API share must cover the gross/net difference allocated to API. At the current house assumptions, 11% is the boundary for zero net API revenue.');
note(inp,373,'ARR must be numeric, nonnegative and gross ≥ net. Rounding to 12 decimals removes sub-cent arithmetic residuals at zero/100% boundaries; it does not repair invalid assumptions.');

format(min,45,45);note(min,45,'This reference is the lower of two observed benchmarks, not a floor. An editable forecast mix can produce a selected price below it; the comparison may then reverse.');
format(pb,115,116);note(pb,115,'Audit: zero overrides are explicit values; only blank cells inherit the previous month. Raw-cost and token definitions remain unverified as a company revenue/usage pair.');
note(pb,116,'Source cost warning: Ramp documents overage-rate valuation for some OpenAI credit-plan estimates; whether the public Index uses that calculation is unconfirmed.');

refs.getRange('C90:M97').format.font={name:'Arial',size:10,color:C.ink};refs.getRange('C90:M97').format.verticalAlignment='center';
section(refs,90,'Audit sources and cost-basis qualification','M');
note(refs,92,'Ramp AI Spend Management, Cost calculation; checked October 23, 2026. Some OpenAI credit-plan estimates value consumption at the workspace overage rate and differ from billed spend. Public Index applicability is unconfirmed.',42,'M');
note(refs,93,'https://support.ramp.com/ai-token-spend-management',30,'M');
note(refs,95,'Ramp agent tools distinguish actual vendor payment spend from estimated token usage/cost aggregates. This does not disclose which calculation the public Index uses; cost basis remains PARTIAL.',42,'M');
note(refs,96,'https://agents.ramp.com/docs/reference/agent-tools',30,'M');
wb.recalculate();

const tests=[];
for(const q of data.monthly_expected){const c=cols[q.month-1],cr=q.provider==='anthropic'?9:27;close(get(cons,c+(cr+7)),q.published_price,'baseline price');close(get(cons,c+(cr+8)),q.base_gross_tokens_Q_month,'baseline full volume');close(get(cons,c+(cr+9)),q.api_gross_tokens_Q_month,'baseline API volume');}
tests.push('24 monthly default prices/full-ARR/API volumes remain consistent with independent raw-source calculations');
for(const basis of [1,2]){
 val(inp,'D4',basis);
 for(const [cell,out]of [['N10','N18'],['N16','N36']]){
  const old=get(inp,cell);
  for(const bad of [-.1,1.1,'invalid']){val(inp,cell,bad);wb.recalculate();if(get(cons,out)!=='n.a.')throw Error('Invalid API share guard '+basis+'/'+cell+'/'+bad);}
  val(inp,cell,1);wb.recalculate();close(get(cons,out),get(cons,out==='N18'?'N17':'N35'),'100% share');val(inp,cell,old);
 }
 const old=get(inp,'N10');val(inp,'N10',.10);wb.recalculate();if(get(cons,'N18')!=='n.a.')throw Error('Negative transformed net API not blocked in both modes');val(inp,'N10',.11);wb.recalculate();if(basis===2)close(get(cons,'N18'),0,'exact zero net API boundary');else if(!(get(cons,'N18')>0))throw Error('Valid gross boundary blocked');val(inp,'N10',old);
 const oldO=get(inp,'N16');val(inp,'N16',0);wb.recalculate();if(basis===2)close(get(cons,'N36'),0,'OpenAI zero net API');else if(!(get(cons,'N36')>=0))throw Error('OpenAI zero-share boundary');val(inp,'N16',oldO);
}
val(inp,'D4',1);wb.recalculate();tests.push('Both ARR modes reject invalid shares and negative transformed API; 0/100% and Anthropic exact11% boundary tested');
for(const [sourceCell,out]of [['N8','N17'],['N14','N35']]){
 const old=get(inp,sourceCell);for(const bad of [-1,'invalid']){val(inp,sourceCell,bad);wb.recalculate();if(get(cons,out)!=='n.a.')throw Error('Invalid ARR guard failed');}val(inp,sourceCell,old);
}
const ng=get(inp,'N8');val(inp,'N8',get(inp,'N9')-1);wb.recalculate();if(get(cons,'N17')!=='n.a.'||get(cons,'N18')!=='n.a.')throw Error('Gross below net guard');val(inp,'N8',ng);wb.recalculate();tests.push('Negative/nonnumeric ARR and gross below net rejected');
for(const b of [9,49]){
 for(const [off,x]of [[18,.01],[19,0],[20,.99]])val(pb,'N'+(b+off),x);wb.recalculate();close(get(pb,'N'+(b+6)),0,'zero output override');close(get(pb,'N'+(b+1)),.01*get(pb,'M'+(b+10))+.99*get(pb,'M'+(b+12)),'feasible zero-output mix');close(get(pb,'O'+(b+1)),get(pb,'N'+(b+1)),'forecast carry');
 val(pb,'N'+(b+18),.02);wb.recalculate();if(get(pb,'N'+(b+1))!=='n.a.')throw Error('Mix sum guard');pb.getRange(`N${b+18}:O${b+20}`).clear({applyTo:'contents'});wb.recalculate();
}
tests.push('Explicit zero forecast overrides, carry-forward and unbalanced-mix rejection verified for both companies');
for(const bad of [-1,-1.01,'invalid']){val(inp,'D5',bad);wb.recalculate();if(get(cons,'N17')!=='n.a.'||get(cons,'O35')!=='n.a.')throw Error('Price boundary regression');}val(inp,'D5',0);wb.recalculate();
tests.push('Existing zero/negative/nonnumeric price guards preserved');
for(const q of data.monthly_expected){const c=cols[q.month-1],cr=q.provider==='anthropic'?9:27;close(get(cons,c+(cr+7)),q.published_price,'restored price');close(get(cons,c+(cr+9)),q.api_gross_tokens_Q_month,'restored API volume');}
const scan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:50},summary:'General audit corrected workbook error scan'});
for(const [name,sheet,range]of [['audited_consumption','Consumption','C1:O21'],['audit_findings','Consumption','C49:O74'],['audit_source_controls','Inputs','C370:O373'],['audit_cost_references','Price references','C90:M96']]){const b=await wb.render({sheetName:sheet,range,scale:1.3,format:'png'});await fs.writeFile(path.join(here,name+'.png'),new Uint8Array(await b.arrayBuffer()));}
await(await SpreadsheetFile.exportXlsx(wb)).save(output);
const report={source,output,tests,scan:scan.ndjson,default_price_change:false,default_api_volume_difference:'less than 1e-9 relative; ratio rounding at 12 decimals',limitations:['Unreconciled token universes','Unverified billing basis','Residual not measured cache','Minimum is scenario selection','Original OpenAI20% take denominator unspecified']};
await fs.writeFile(path.join(here,'general_audit_fix_verification.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
