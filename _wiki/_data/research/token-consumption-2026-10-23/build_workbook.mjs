import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';

const here=path.dirname(fileURLToPath(import.meta.url));
const data=JSON.parse(await fs.readFile(path.join(here,'model_inputs.json'),'utf8'));
const outDir='E:/Wiki Felipe empresas/outputs/01a168b5-7786-7582-8082-7cd6bd45fd69';
await fs.mkdir(outDir,{recursive:true});
const wb=Workbook.create();
const names=['Consumption','Minimum price','Token mix','Inputs'];
const sheets=Object.fromEntries(names.map(n=>[n,wb.worksheets.add(n)]));
const C={navy:'#173451',pale:'#EAF0F6',ink:'#142D4E',blue:'#0000FF',green:'#008000',amber:'#FFF2CC',red:'#FCE4D6',gray:'#65758B'};
const num='#,##0.00;(#,##0.00);"-"';
const price='$0.0000;($0.0000);"-"';
const pct='0.0%;(0.0%);"-"';
const cols=Array.from({length:12},(_,i)=>String.fromCharCode(68+i));
const val=(s,a,v)=>s.getRange(a).values=[[v]];
const formula=(s,a,f,output=false)=>{s.getRange(a).formulas=[[f]];s.getRange(a).format.font.color=output?C.ink:f.includes('!')?C.green:'#000000';};
const label=(s,r,t)=>val(s,`C${r}`,t);
function section(s,r,t){label(s,r,t);const rg=s.getRange(`C${r}:O${r}`);rg.format.fill=C.pale;rg.format.font.bold=true;rg.format.borders={bottom:{style:'thin',color:'#B3C1D0'}};}
function emphasis(s,r){s.getRange(`C${r}:O${r}`).format.fill='#F0F4F8';s.getRange(`C${r}:O${r}`).format.font.bold=true;}
function header(s,r){label(s,r,'2026');s.getRange(`C${r}:O${r}`).format.fill=C.navy;s.getRange(`C${r}:O${r}`).format.font.color='#FFFFFF';s.getRange(`C${r}:O${r}`).format.font.bold=true;for(let i=0;i<12;i++)val(s,cols[i]+r,new Date(Date.UTC(2026,i,1)));s.getRange(`D${r}:O${r}`).setNumberFormat('mmm-yy');s.getRange(`D${r}:O${r}`).format.horizontalAlignment='center';}
function note(s,r,t){label(s,r,t);s.getRange(`C${r}`).format.font.color=C.gray;}
for(const n of names){const s=sheets[n];s.showGridLines=false;s.getRange('A1:P310').format.font={name:'Arial',size:10,color:C.ink};s.getRange('A1:P310').format.verticalAlignment='center';s.getRange('A1:B310').format.columnWidth=2.5;s.getRange('C1:C310').format.columnWidth=43;s.getRange('D1:O310').format.columnWidth=12;s.getRange('P1:P310').format.columnWidth=3;s.getRange('A1:P310').format.rowHeight=21;s.getRange('D7:O310').setNumberFormat(num);s.getRange('D7:O310').format.horizontalAlignment='right';s.tabColor=n==='Inputs'?'#B7C9DB':n==='Consumption'?C.navy:'#7894B0';label(s,2,n==='Consumption'?'Anthropic and OpenAI token consumption':n==='Minimum price'?'Minimum price reference':n==='Token mix'?'Product mix and implied token allocation':'Source inputs');s.getRange('C2').format.font={name:'Arial',size:15,bold:true,color:C.ink};s.getRange('C3:O3').format.borders={bottom:{style:'thin',color:C.navy}};header(s,7);s.freezePanes.freezeRows(7);s.freezePanes.freezeColumns(3);}

const inp=sheets.Inputs;
label(sheets.Consumption,2,'Implied token consumption scenarios');
label(inp,4,'ARR basis: 1 Gross / 2 Net');val(inp,'D4',1);inp.getRange('D4').format.font.color=C.blue;inp.getRange('D4').format.fill=C.amber;inp.getRange('D4').dataValidation={rule:{type:'whole',operator:'between',formula1:1,formula2:2}};
label(inp,5,'Nov/Dec price change per month');val(inp,'D5',0);inp.getRange('D5').setNumberFormat(pct);inp.getRange('D5').format.font.color=C.blue;inp.getRange('D5').format.fill=C.amber;val(inp,'F5','ESTIMATE: 0% holds October prices flat.');
inp.getRange('D5').dataValidation={rule:{type:'decimal',operator:'greaterThanOrEqual',formula1:-1},errorAlert:{style:'stop',title:'Invalid price change',message:'Enter a numeric change of -100% or above. A zero price produces n.a. consumption.'}};
const arrRows={anthropic:{gross:8,net:9,api_share:10},openai:{gross:14,net:15,api_share:16}};
for(const m of ['anthropic','openai']){const rr=arrRows[m];for(const k of ['gross','net']){label(inp,rr[k],`${m==='anthropic'?'Anthropic':'OpenAI'} ${k} ARR ($m)`);inp.getRange(`D${rr[k]}:O${rr[k]}`).values=[data.arr[m][k]];inp.getRange(`D${rr[k]}:O${rr[k]}`).format.font.color=C.blue;}label(inp,rr.api_share,m==='anthropic'?'API share of gross revenue':'API share of net revenue');inp.getRange(`D${rr.api_share}:O${rr.api_share}`).values=[Array(12).fill(data.arr[m].api_share)];inp.getRange(`D${rr.api_share}:O${rr.api_share}`).setNumberFormat(pct);inp.getRange(`D${rr.api_share}:O${rr.api_share}`).format.font.color=C.blue;}
label(inp,20,'Calendar days');label(inp,21,'Price observation month');label(inp,22,'Price / mix status');
for(let i=0;i<12;i++){const c=cols[i];formula(inp,c+'20',`=DAY(EOMONTH(${c}$7,0))`);val(inp,c+'21',Math.min(i+1,10));val(inp,c+'22',i<9?'Observed':i===9?'Partial':'Estimate');}
inp.getRange('D20:O21').setNumberFormat('0');inp.getRange('M22:O22').format.fill=C.amber;
note(inp,25,'ARR and API shares: Capstone house model, AI Model.xlsx, saved October 23, 2026. All are ESTIMATE inputs, not audited company actuals.');
note(inp,26,'ARR Tracker: Anthropic gross P98:AA98 / net P84:AA84; OpenAI gross P95:AA95 / net P81:AA81. Values are annualized USD millions.');
note(inp,27,'API shares: Anthropic!AB11 (gross basis) and OpenAI!AB29 (net basis), CY2026. Held across the months as a house-estimate scenario.');
note(inp,28,'Gross API revenue assumes all gross/net differences arise in API channels; subscriptions and other revenue are unchanged.');
note(inp,30,'HARD: Ramp raw observations. DERIVED: sums and ratios. PARTIAL: company representativeness and family mappings. ESTIMATE: ARR and extrapolation.');
note(inp,31,'Ramp Economics Lab / Ara Kharazian. Captured October 23, 2026. https://ramp.com/data/ai-index');
note(inp,32,'Monthly prices are token-weighted averages of nonoverlapping weeks ending in that month; they are not exact calendar-month billing averages.');
note(inp,33,'October covers weeks ending October 4 and 11. November/December price and mix assumptions carry October forward; ARR follows the source forecast.');
note(inp,34,'Minimum reference = lower monthly published ratio or matched-model ratio. Denominators remain unresolved; neither is a validated company ASP.');
note(inp,35,'Full ARR conversion is API-equivalent demand. It does not measure subscription usage, free users, training tokens or actual company token consumption.');
note(inp,36,'Matched models have positive tokens and a reported spending record. Missing spending remains unknown; unmatched volume is excluded from matched prices.');
note(inp,37,'Net ARR mode is a revenue-equivalent scenario. Ramp spend ratios are not automatically net of cloud revenue sharing or discounts.');
note(inp,38,'Raw observations: tokenPrices and tokenVolumes, Ramp chart-data version b1ACnM4ULJjULGFdkttsRs.');
note(inp,39,'Family allocation is an illustrative transfer of Ramp mix to company-level implied demand, not an independent estimate of actual product traffic.');
note(inp,41,'Gross/net alternatives and forecasts in the source are preserved. No official ARR marks are substituted and no source-workbook errors are repaired.');

// Input tables retain source aggregates; all business ratios calculate in Excel.
const wStart=48,wEnd=wStart+data.weekly.length-1;
const wHead=['Week ending','Provider','Month','Price tokens','Price cost $','Model tokens','Model cost $','Missing-cost tokens','Zero-token cost $','Matched tokens','Matched cost $','Published $/M','Matched $/M'];
inp.getRange(`C47:O47`).values=[wHead];inp.getRange('C47:O47').format.fill=C.navy;inp.getRange('C47:O47').format.font.color='#FFFFFF';inp.getRange('C47:O47').format.wrapText=true;inp.getRange('C47:O47').format.rowHeight=38;
inp.getRange(`C${wStart}:K${wEnd}`).values=data.weekly.map(r=>[new Date(r.date+'T00:00:00Z'),r.provider,r.month,r.N,r.C,r.T,r.S,r.missing,r.zero_token_cost]);inp.getRange(`C${wStart}:C${wEnd}`).setNumberFormat('dd-mmm-yy');inp.getRange(`D${wStart}:D${wEnd}`).format.horizontalAlignment='left';inp.getRange(`E${wStart}:E${wEnd}`).setNumberFormat('0');inp.getRange(`F${wStart}:K${wEnd}`).setNumberFormat('#,##0');
for(let r=wStart;r<=wEnd;r++){formula(inp,`L${r}`,`=H${r}-J${r}`);formula(inp,`M${r}`,`=I${r}-K${r}`);formula(inp,`N${r}`,`=G${r}/F${r}*1000000`);formula(inp,`O${r}`,`=M${r}/L${r}*1000000`);}inp.getRange(`L${wStart}:M${wEnd}`).setNumberFormat('#,##0');inp.getRange(`N${wStart}:O${wEnd}`).setNumberFormat(price);
for(const c of ['F','H','J','L'])inp.getRange(`${c}${wStart}:${c}${wEnd}`).setNumberFormat('0.00E+00');
const fStart=135,fEnd=fStart+data.family_rows.length-1;
inp.getRange('C134:K134').values=[['Provider','Month','Family','All tokens','Matched tokens','Matched cost $','Matched $/M','All-token share','Matched share']];inp.getRange('C134:K134').format.fill=C.navy;inp.getRange('C134:K134').format.font.color='#FFFFFF';inp.getRange('C134:K134').format.rowHeight=38;inp.getRange('C134:K134').format.wrapText=true;
inp.getRange(`C${fStart}:H${fEnd}`).values=data.family_rows.map(r=>[r.provider,r.month,r.family,r.total_tokens,r.matched_tokens,r.matched_cost]);inp.getRange(`C${fStart}:E${fEnd}`).format.horizontalAlignment='left';inp.getRange(`D${fStart}:D${fEnd}`).setNumberFormat('0');inp.getRange(`E${fStart}:E${fEnd}`).format.wrapText=true;inp.getRange(`C${fStart}:K${fEnd}`).format.rowHeight=30;inp.getRange(`F${fStart}:H${fEnd}`).setNumberFormat('0.00E+00');
const sumW=(col,m,c)=>`SUMIFS(Inputs!$${col}$${wStart}:$${col}$${wEnd},Inputs!$D$${wStart}:$D$${wEnd},"${m}",Inputs!$E$${wStart}:$E$${wEnd},MONTH(${c}$7))`;
for(let r=fStart;r<=fEnd;r++){formula(inp,`I${r}`,`=IF(G${r}>0,H${r}/G${r}*1000000,"n.a.")`);formula(inp,`J${r}`,`=F${r}/SUMIFS($F$${fStart}:$F$${fEnd},$C$${fStart}:$C$${fEnd},C${r},$D$${fStart}:$D$${fEnd},D${r})`);formula(inp,`K${r}`,`=G${r}/SUMIFS($G$${fStart}:$G$${fEnd},$C$${fStart}:$C$${fEnd},C${r},$D$${fStart}:$D$${fEnd},D${r})`);}inp.getRange(`I${fStart}:I${fEnd}`).setNumberFormat(price);inp.getRange(`J${fStart}:K${fEnd}`).setNumberFormat(pct);

// One ARR-basis selector; each build displays the selected basis.
for(const n of names.filter(n=>n!=='Inputs')){label(sheets[n],4,'ARR basis selected');formula(sheets[n],'D4','=IF(Inputs!$D$4=1,"Gross",IF(Inputs!$D$4=2,"Net","Invalid basis"))');sheets[n].getRange('D4').format.font.color=C.green;}
const cons=sheets.Consumption,min=sheets['Minimum price'],mix=sheets['Token mix'];
note(cons,5,'Conditional API-equivalent volumes; pricing denominators and company-wide representativeness remain unvalidated. Q = 10^15 tokens; T = 10^12.');
note(min,5,'Reference = lower of the two monthly averages. It is not a theoretical floor, guaranteed discount or inference break-even price.');
note(mix,5,'Observed family shares use all model-series tokens. Allocations below apply those shares to implied demand as a PARTIAL proxy.');
const cfg={anthropic:{cr:9,pr:9,mr:9},openai:{cr:27,pr:25,mr:20}};
for(const m of ['anthropic','openai']){
 const {cr,pr}=cfg[m],ar=arrRows[m],nm=m==='anthropic'?'Anthropic':'OpenAI';section(cons,cr,nm);section(min,pr,nm);
 const cl={1:'Gross average ARR ($bn)',2:'Net average ARR ($bn)',3:'Selected average ARR ($bn)',4:'Monthly revenue equivalent ($bn)',5:'Estimated API share of selected ARR',6:'API-only monthly revenue ($bn)',7:'Average price ($ / million tokens)',8:'Full-ARR equivalent (Q / month)',9:'API-only equivalent (Q / month)',10:'Full-ARR equivalent (T / day)',11:'Full-ARR token growth MoM',12:'Price observation status'};
 for(const [o,t]of Object.entries(cl))label(cons,cr+Number(o),t);
 const pl={1:'Published monthly average ($/M)',2:'Matched-model monthly average ($/M)',3:'Minimum price reference ($/M)',4:'Reference discount to published',5:'Full-ARR equivalent at reference (Q)',6:'API-only equivalent at reference (Q)',7:'Token uplift versus average-price case',8:'Matched share of model tokens',9:'Model / price token denominator gap',10:'Nonoverlapping weeks in sample',11:'Observation status'};
 for(const [o,t]of Object.entries(pl))label(min,pr+Number(o),t);
 for(let i=0;i<12;i++){const c=cols[i],prev=cols[i-1];
  formula(cons,c+(cr+1),`=Inputs!${c}${ar.gross}/1000`);formula(cons,c+(cr+2),`=Inputs!${c}${ar.net}/1000`);
  formula(cons,c+(cr+3),`=IF(Inputs!$D$4=1,${c}${cr+1},IF(Inputs!$D$4=2,${c}${cr+2},"n.a."))`);
  formula(cons,c+(cr+4),`=IF(ISNUMBER(${c}${cr+3}),${c}${cr+3}/12,"n.a.")`);
  const ag=`${c}${cr+1}`,an=`${c}${cr+2}`,share=`Inputs!${c}${ar.api_share}`;
  const apiGross=m==='anthropic'?`${ag}*${share}`:`${an}*${share}+${ag}-${an}`;
  const apiNet=m==='anthropic'?`${ag}*${share}-(${ag}-${an})`:`${an}*${share}`;
  formula(cons,c+(cr+5),`=IF(Inputs!$D$4=1,(${apiGross})/${ag},IF(Inputs!$D$4=2,(${apiNet})/${an},"n.a."))`);
  formula(cons,c+(cr+6),`=IF(AND(ISNUMBER(${c}${cr+4}),ISNUMBER(${c}${cr+5})),${c}${cr+4}*${c}${cr+5},"n.a.")`);
  formula(cons,c+(cr+7),`='Minimum price'!${c}${pr+1}`);
  for(const [offset,rev]of [[8,4],[9,6]])formula(cons,c+(cr+offset),`=IF(AND(ISNUMBER(${c}${cr+rev}),ISNUMBER(${c}${cr+7}),${c}${cr+7}>0),${c}${cr+rev}/${c}${cr+7},"n.a.")`,true);
  formula(cons,c+(cr+10),`=IF(ISNUMBER(${c}${cr+8}),${c}${cr+8}*1000/Inputs!${c}20,"n.a.")`,true);
  formula(cons,c+(cr+11),i?`=IF(AND(ISNUMBER(${c}${cr+8}),ISNUMBER(${prev}${cr+8}),${prev}${cr+8}>0),${c}${cr+8}/${prev}${cr+8}-1,"n.a.")`:'="n.a."',true);
  formula(cons,c+(cr+12),`=Inputs!${c}22`,true);
  if(i<10){formula(min,c+(pr+1),`=${sumW('G',m,c)}/${sumW('F',m,c)}*1000000`);formula(min,c+(pr+2),`=${sumW('M',m,c)}/${sumW('L',m,c)}*1000000`);formula(min,c+(pr+8),`=${sumW('L',m,c)}/${sumW('H',m,c)}`);formula(min,c+(pr+9),`=${sumW('H',m,c)}/${sumW('F',m,c)}-1`);formula(min,c+(pr+10),`=COUNTIFS(Inputs!$D$${wStart}:$D$${wEnd},"${m}",Inputs!$E$${wStart}:$E$${wEnd},MONTH(${c}$7))`);}
  else {for(const r of [pr+1,pr+2])formula(min,c+r,`=IF(AND(ISNUMBER(Inputs!$D$5),Inputs!$D$5>=-1,ISNUMBER(${prev}${r})),${prev}${r}*(1+Inputs!$D$5),"n.a.")`);for(const r of [pr+8,pr+9])formula(min,c+r,`=$M${r}`);val(min,c+(pr+10),'n.a.');}
  formula(min,c+(pr+3),`=IF(AND(ISNUMBER(${c}${pr+1}),ISNUMBER(${c}${pr+2}),${c}${pr+1}>0,${c}${pr+2}>0),MIN(${c}${pr+1},${c}${pr+2}),"n.a.")`,true);
  formula(min,c+(pr+4),`=IF(ISNUMBER(${c}${pr+3}),1-${c}${pr+3}/${c}${pr+1},"n.a.")`,true);
  for(const [off,rev]of [[5,4],[6,6]])formula(min,c+(pr+off),`=IF(AND(ISNUMBER(Consumption!${c}${cr+rev}),ISNUMBER(${c}${pr+3}),${c}${pr+3}>0),Consumption!${c}${cr+rev}/${c}${pr+3},"n.a.")`,true);
  formula(min,c+(pr+7),`=IF(AND(ISNUMBER(${c}${pr+5}),ISNUMBER(Consumption!${c}${cr+8}),Consumption!${c}${cr+8}>0),${c}${pr+5}/Consumption!${c}${cr+8}-1,"n.a.")`,true);
  formula(min,c+(pr+11),`=Inputs!${c}22`,true);
 }
 cons.getRange(`D${cr+5}:O${cr+5}`).setNumberFormat(pct);cons.getRange(`D${cr+7}:O${cr+7}`).setNumberFormat(price);cons.getRange(`D${cr+11}:O${cr+11}`).setNumberFormat(pct);for(const r of [cr+8,cr+9])emphasis(cons,r);
 min.getRange(`D${pr+1}:O${pr+3}`).setNumberFormat(price);for(const r of [pr+4,pr+7,pr+8,pr+9])min.getRange(`D${r}:O${r}`).setNumberFormat(pct);min.getRange(`D${pr+10}:O${pr+10}`).setNumberFormat('0');emphasis(min,pr+3);emphasis(min,pr+5);
 min.getRange(`D${pr+9}:O${pr+9}`).conditionalFormats.add('cellIs',{operator:'greaterThan',formula:.01,format:{fill:C.red,font:{color:'#9C0006',bold:true}}});
 cons.getRange(`D${cr+5}:O${cr+5}`).conditionalFormats.addCustom(`OR(D${cr+5}<0,D${cr+5}>1)`,{fill:C.red,font:{color:'#9C0006',bold:true}});
}
note(cons,43,'Formula: ARR ($bn) / 12 / price ($ per million) = quadrillion tokens per month. This is a conditional conversion, not measured usage.');
note(cons,44,'Gross mode uses customer-spend-equivalent ARR from the source model. Net mode is a separate revenue-equivalent scenario.');
note(cons,45,'API-only estimates use the house API shares and assume gross/net differences belong to API channels. Full ARR also contains subscription revenue.');
note(cons,46,'Lower-price consumption and pricing details are on Minimum price; observed family shares and illustrative allocation are on Token mix.');
note(min,40,'Price average = sum of weekly source costs / sum of weekly source tokens. Ratios are weighted by their own token denominators.');
note(min,41,'Matched-model average = sum of cost on paired positive-token models / their token volume. The two denominator bases are not reconciled.');
note(min,42,'Minimum reference chooses the lower benchmark as a scenario. It is not a confidence interval and is not a bound on the company actual ASP.');
note(min,43,'Monthly samples include cross-month weeks. October is partial. Forecast months hold October mix and apply the editable price change in Inputs.');

// Family shares and illustrative baseline-volume allocation; no price causality claimed.
let r=9;const familyShareRows={};
for(const m of ['anthropic','openai']){section(mix,r,m==='anthropic'?'Anthropic observed token mix':'OpenAI observed token mix');r++;familyShareRows[m]=[];for(const f of data.families[m]){label(mix,r,f);familyShareRows[m].push(r);for(let i=0;i<12;i++){const c=cols[i];formula(mix,c+r,`=SUMIFS(Inputs!$F$${fStart}:$F$${fEnd},Inputs!$C$${fStart}:$C$${fEnd},"${m}",Inputs!$D$${fStart}:$D$${fEnd},Inputs!${c}$21,Inputs!$E$${fStart}:$E$${fEnd},$C${r})/SUMIFS(Inputs!$F$${fStart}:$F$${fEnd},Inputs!$C$${fStart}:$C$${fEnd},"${m}",Inputs!$D$${fStart}:$D$${fEnd},Inputs!${c}$21)`,true);}mix.getRange(`D${r}:O${r}`).setNumberFormat(pct);r++;}label(mix,r,'Total share');for(const c of cols)formula(mix,c+r,`=SUM(${c}${familyShareRows[m][0]}:${c}${r-1})`,true);mix.getRange(`D${r}:O${r}`).setNumberFormat(pct);emphasis(mix,r);r+=3;}
const allocationStarts={};
for(const m of ['anthropic','openai']){section(mix,r,`${m==='anthropic'?'Anthropic':'OpenAI'} implied allocation (Q / month)`);r++;allocationStarts[m]=r;let fi=0;for(const f of data.families[m]){label(mix,r,f);for(const c of cols)formula(mix,c+r,`=IF(ISNUMBER(Consumption!${c}${cfg[m].cr+8}),${c}${familyShareRows[m][fi]}*Consumption!${c}${cfg[m].cr+8},"n.a.")`,true);fi++;r++;}label(mix,r,'Total implied allocation');for(const c of cols)formula(mix,c+r,`=IF(COUNT(${c}${allocationStarts[m]}:${c}${r-1})=${data.families[m].length},SUM(${c}${allocationStarts[m]}:${c}${r-1}),"n.a.")`,true);emphasis(mix,r);r+=3;}
note(mix,r,'Family definitions are based on Ramp model names. Other includes unmapped / early-access models; unknown spending is not zero pricing.');
note(mix,r+1,'Minimum-price weighting excludes unpaired models; these all-token mix shares retain them. No additional cache adjustment is applied.');

// Terminal checks only. They never drive the builds.
section(inp,270,'Reconciliation checks');
label(inp,272,'Anthropic family token total difference');label(inp,273,'OpenAI family token total difference');
for(let i=0;i<10;i++){const c=cols[i];for(const [m,row]of [['anthropic',272],['openai',273]])formula(inp,c+row,`=SUMIFS($F$${fStart}:$F$${fEnd},$C$${fStart}:$C$${fEnd},"${m}",$D$${fStart}:$D$${fEnd},MONTH(${c}$7))-${sumW('H',m,c).replaceAll('Inputs!','')}`);}
inp.getRange('D272:M273').setNumberFormat('0.00');inp.getRange('D272:M273').conditionalFormats.addCustom('ABS(D272)>0.01',{fill:C.red,font:{color:'#9C0006',bold:true}});
note(inp,276,'Independent company token-volume validation: unavailable. The revenue/price identity verifies arithmetic only.');
note(inp,277,'Denominator disagreement remains visible on Minimum price. Source row agreement does not establish recognized revenue or a common customer universe.');

// Keep formatting within the intentional used ranges rather than empty trailing cells.
for(const [n,last]of [['Consumption',46],['Minimum price',43],['Token mix',r+1],['Inputs',277]])sheets[n].getRange(`A${last+1}:P310`).clear({applyTo:'formats'});
wb.recalculate();
const test={};
function get(s,a){return sheets[s].getRange(a).values[0][0];}
function close(actual,expected,key){if(typeof actual!=='number'||Math.abs(actual-expected)>1e-8*Math.max(1,Math.abs(expected)))throw Error(`${key}: ${actual} != ${expected}`);}
for(const e of data.monthly_expected){const c=cols[e.month-1],{cr,pr}=cfg[e.provider];close(get('Consumption',c+(cr+8)),e.base_gross_tokens_Q_month,`${e.provider}/${e.month}/base`);close(get('Minimum price',c+(pr+3)),e.minimum_reference,`${e.provider}/${e.month}/minimum`);close(get('Minimum price',c+(pr+5)),e.reference_gross_tokens_Q_month,`${e.provider}/${e.month}/reference-volume`);close(get('Consumption',c+(cr+9)),e.api_gross_tokens_Q_month,`${e.provider}/${e.month}/api-only`);}
test.baseline='24 provider-month outputs match independent Python calculations';
// Verify alternative ARR basis, a future price edit, and zero-price failure state; restore inputs.
val(inp,'D4',2);wb.recalculate();for(const m of ['anthropic','openai']){const e=data.monthly_expected.find(x=>x.provider===m&&x.month===10);close(get('Consumption','M'+(cfg[m].cr+8)),e.net_arr_busd/12/e.published_price,m+'/net-switch');}val(inp,'D4',1);
val(inp,'D5',-.1);wb.recalculate();for(const m of ['anthropic','openai']){const cr=cfg[m].cr,e=data.monthly_expected.find(x=>x.provider===m&&x.month===12);close(get('Consumption','O'+(cr+8)),e.base_gross_tokens_Q_month/.81,m+'/future-edit');}val(inp,'D5',-1);wb.recalculate();if(get('Consumption','N17')!=='n.a.'||get('Minimum price','N12')!=='n.a.')throw Error('Zero-price guard failed');val(inp,'D5',0);val(inp,'D4',1);wb.recalculate();
for(const bad of [-1.1,'invalid']){val(inp,'D5',bad);wb.recalculate();for(const m of ['anthropic','openai'])for(const c of ['N','O']){if(get('Consumption',c+(cfg[m].cr+8))!=='n.a.'||get('Minimum price',c+(cfg[m].pr+3))!=='n.a.')throw Error('Invalid future-price input guard failed');}}val(inp,'D5',0);wb.recalculate();
test.recalculation='Gross/net basis switch, future -10% price change, zero price, below -100% and nonnumeric input guards passed; original inputs restored';
const scan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},summary:'Final formula error scan'});
await fs.writeFile(path.join(here,'formula_scan.jsonl'),scan.ndjson);
const inspection=await wb.inspect({kind:'table',range:'Consumption!L7:O39',include:'values,formulas',tableMaxRows:33,tableMaxCols:4,maxChars:9000});await fs.writeFile(path.join(here,'workbook_inspection.jsonl'),inspection.ndjson);
for(const [n,range,file]of [['Consumption','C1:O21','consumption_anthropic.png'],['Consumption','C27:O46','consumption_openai.png'],['Minimum price','C1:O20','minimum_anthropic.png'],['Minimum price','C25:O43','minimum_openai.png'],['Token mix','C1:O29','token_mix.png'],['Token mix',`C30:O${r+1}`,'token_allocation.png'],['Inputs','C1:O22','inputs.png'],['Inputs','C47:O53','weekly_source.png'],['Inputs','C134:K141','family_source.png']]){const blob=await wb.render({sheetName:n,range,scale:1.5,format:'png'});await fs.writeFile(path.join(here,file),new Uint8Array(await blob.arrayBuffer()));}
const output=await SpreadsheetFile.exportXlsx(wb);const finalPath=path.join(outDir,'AI_Token_Consumption_and_Minimum_Price.xlsx');await output.save(finalPath);
await fs.writeFile(path.join(here,'verification.json'),JSON.stringify({finalPath,tests:test,october:data.monthly_expected.filter(x=>x.month===10)},null,2));
console.log(JSON.stringify({finalPath,tests:test,formulaScan:scan.ndjson},null,2));
