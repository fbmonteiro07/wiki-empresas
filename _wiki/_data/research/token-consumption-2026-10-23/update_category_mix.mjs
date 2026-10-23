import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';

const here=path.dirname(fileURLToPath(import.meta.url));
const dir='E:/Wiki Felipe empresas/outputs/01a168b5-7786-7582-8082-7cd6bd45fd69';
const source=path.join(dir,'AI_Token_Consumption_and_Minimum_Price_with_References.xlsx');
const output=path.join(dir,'AI_Token_Consumption_Price_and_Mix.xlsx');
const data=JSON.parse(await fs.readFile(path.join(here,'category_mix_inputs.json'),'utf8'));
const original=JSON.parse(await fs.readFile(path.join(here,'model_inputs.json'),'utf8'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(source));
const inp=wb.worksheets.getItem('Inputs'),cons=wb.worksheets.getItem('Consumption');
const min=wb.worksheets.getItem('Minimum price'),mix=wb.worksheets.getItem('Token mix');
const refs=wb.worksheets.getItem('Price references');
const s=wb.worksheets.add('Price build');
const C={navy:'#173451',ink:'#142D4E',pale:'#EAF0F6',gray:'#65758B',hard:'#E2F0D9',partial:'#DDEBF7',estimate:'#FFF2CC',red:'#FCE4D6'};
const cols=Array.from({length:12},(_,i)=>String.fromCharCode(68+i));
const pct='0.00%;(0.00%);"-"',price='$0.0000;($0.0000);"-"';
const v=(sh,a,x)=>sh.getRange(a).values=[[x]];
const f=(sh,a,x)=>sh.getRange(a).formulas=[[x]];
function section(sh,r,title){v(sh,'C'+r,title);sh.getRange(`C${r}:O${r}`).format.fill=C.pale;sh.getRange(`C${r}:O${r}`).format.font.bold=true;sh.getRange(`C${r}:O${r}`).format.borders={bottom:{style:'thin',color:'#B3C1D0'}};}
function note(sh,r,text,height=30){sh.getRange(`C${r}:O${r}`).merge();v(sh,'C'+r,text);sh.getRange(`C${r}:O${r}`).format.wrapText=true;sh.getRange(`C${r}:O${r}`).format.rowHeight=height;sh.getRange(`C${r}:O${r}`).format.font.color=C.gray;}
function format(sh,start,end,labelWidth=46){sh.getRange(`A${start}:P${end}`).format.font={name:'Arial',size:10,color:C.ink};sh.getRange(`A${start}:P${end}`).format.verticalAlignment='center';sh.getRange(`A${start}:P${end}`).format.rowHeight=22;sh.getRange(`A${start}:B${end}`).format.columnWidth=2.5;sh.getRange(`C${start}:C${end}`).format.columnWidth=labelWidth;sh.getRange(`D${start}:O${end}`).format.columnWidth=12;sh.getRange(`P${start}:P${end}`).format.columnWidth=3;}
format(s,1,115);s.showGridLines=false;s.tabColor='#7894B0';s.freezePanes.freezeRows(7);s.freezePanes.freezeColumns(3);
v(s,'C2','Average price and explicit token-category mix');s.getRange('C2').format.font={name:'Arial',size:15,bold:true,color:C.ink};
s.getRange('C3:O3').format.borders={bottom:{style:'thin',color:C.navy}};
note(s,4,'Base choice: Ramp published price-series benchmark, reconstructed below. PARTIAL as a proxy for company ASP; no independent company-volume validation.');
note(s,5,'Cache is not directly reported here. The unclassified remainder is shown as a possible cache / other proxy; it is not a measured cache-read share.');
note(s,6,'Price = sum of category share × effective category rate. October is partial; November/December are ESTIMATE forecasts. Amber cells allow forecast mix overrides.');
v(s,'C7','2026');s.getRange('C7:O7').format.fill=C.navy;s.getRange('C7:O7').format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};
for(const c of cols)f(s,c+'7',`=Consumption!${c}7`);s.getRange('D7:O7').setNumberFormat('mmm-yy');s.getRange('D7:O7').format.horizontalAlignment='center';

// Append exact source observations without editing the existing input tables.
const first=286,last=first+data.weekly.length-1;
format(inp,281,last,43);
section(inp,281,'HARD source observations — Ramp tokenPrices, captured October 23, 2026');
note(inp,282,'Each row uses the same week-ending date for all_tokens, uncached_input and output. Source definitions do not prove matched cohorts or an exhaustive partition.');
note(inp,283,'https://ramp.com/data/ai-index/chart-data/tokenPrices?version=b1ACnM4ULJjULGFdkttsRs');
inp.getRange('C285:K285').values=[['Week ending','Provider','Month','All tokens','All cost $','Uncached input tokens','Uncached input cost $','Output tokens','Output cost $']];
inp.getRange('C285:K285').format.fill=C.navy;inp.getRange('C285:K285').format.font.color='#FFFFFF';inp.getRange('C285:K285').format.wrapText=true;inp.getRange('C285:K285').format.rowHeight=44;
inp.getRange(`C${first}:K${last}`).values=data.weekly.map(r=>[new Date(r.date+'T00:00:00Z'),r.provider,r.month,r.all_tokens,r.all_cost,r.input_tokens,r.input_cost,r.output_tokens,r.output_cost]);
inp.getRange(`C${first}:K${last}`).format.fill=C.hard;inp.getRange(`C${first}:C${last}`).setNumberFormat('dd-mmm-yy');inp.getRange(`E${first}:E${last}`).setNumberFormat('0');inp.getRange(`F${first}:K${last}`).setNumberFormat('0.0000E+00');

const cfg={anthropic:{b:9,cr:9,pr:9},openai:{b:49,cr:27,pr:25}};
const sum=(col,provider,c)=>`SUMIFS(Inputs!$${col}$${first}:$${col}$${last},Inputs!$D$${first}:$D$${last},"${provider}",Inputs!$E$${first}:$E$${last},MONTH(${c}$7))`;
for(const [provider,{b,cr,pr}]of Object.entries(cfg)){
 section(s,b,provider==='anthropic'?'Anthropic — published-panel base':'OpenAI — published-panel base');
 const labels={1:'Selected average price ($/M)',2:'ANCHOR: published benchmark ($/M)',3:'Selected price / anchor difference',5:'Uncached input share',6:'Output share',7:'Unclassified share (cache / other proxy)',8:'Total category share',10:'Effective uncached input rate ($/M)',11:'Effective output rate ($/M)',12:'Residual effective rate ($/M)',14:'Input contribution to price ($/M)',15:'Output contribution to price ($/M)',16:'Residual contribution to price ($/M)',18:'ESTIMATE: input share override',19:'ESTIMATE: output share override',20:'ESTIMATE: residual share override',22:'Mix input validity',23:'Company price / mix evidence',25:'Source all tokens (N)',26:'Source all cost ($)',27:'Source uncached input tokens (U)',28:'Source uncached input cost ($)',29:'Source output tokens (O)',30:'Source output cost ($)',31:'Residual tokens: N − U − O',32:'Residual cost: all − input − output',34:'CHECK: residual nonnegative',35:'CHECK: source bridge error ($/M)',36:'Lower-price reference ($/M)',37:'Model / price token denominator gap'};
 for(const [off,label]of Object.entries(labels))v(s,'C'+(b+Number(off)),label);
 s.getRange(`C${b+7}`).format.wrapText=true;s.getRange(`C${b+7}:O${b+7}`).format.rowHeight=32;
 for(const off of [1,2,10,11,12,14,15,16,35,36])s.getRange(`D${b+off}:O${b+off}`).setNumberFormat(price);
 for(const off of [3,5,6,7,8,18,19,20,37])s.getRange(`D${b+off}:O${b+off}`).setNumberFormat(pct);
 s.getRange(`D${b+25}:O${b+32}`).setNumberFormat('0.0000E+00');
 s.getRange(`D${b+2}:M${b+2}`).format.fill=C.partial;
 s.getRange(`D${b+7}:M${b+7}`).format.fill=C.partial;s.getRange(`D${b+12}:M${b+12}`).format.fill=C.partial;
 s.getRange(`N${b+5}:O${b+7}`).format.fill=C.estimate;s.getRange(`N${b+10}:O${b+12}`).format.fill=C.estimate;
 for(const off of [1,8,16]){s.getRange(`C${b+off}:O${b+off}`).format.font.bold=true;s.getRange(`C${b+off}:O${b+off}`).format.borders={top:{style:'thin',color:'#B3C1D0'}};}
 for(let i=0;i<12;i++){
  const c=cols[i],prev=cols[i-1];
  f(s,c+(b+2),`='Minimum price'!${c}${pr+1}`);
  f(s,c+(b+1),`=IF(AND(COUNT(${c}${b+5}:${c}${b+7})=3,MIN(${c}${b+5}:${c}${b+7})>=0,MAX(${c}${b+5}:${c}${b+7})<=1,ABS(SUM(${c}${b+5}:${c}${b+7})-1)<0.00000001,COUNT(${c}${b+10}:${c}${b+12})=3,MIN(${c}${b+10}:${c}${b+12})>=0),SUMPRODUCT(${c}${b+5}:${c}${b+7},${c}${b+10}:${c}${b+12}),"n.a.")`);
  f(s,c+(b+3),`=IF(AND(ISNUMBER(${c}${b+1}),ISNUMBER(${c}${b+2}),${c}${b+2}>0),${c}${b+1}/${c}${b+2}-1,"n.a.")`);
  f(s,c+(b+8),`=IF(COUNT(${c}${b+5}:${c}${b+7})=3,SUM(${c}${b+5}:${c}${b+7}),"n.a.")`);
  for(let k=0;k<3;k++)f(s,c+(b+14+k),`=IF(AND(ISNUMBER(${c}${b+5+k}),ISNUMBER(${c}${b+10+k})),${c}${b+5+k}*${c}${b+10+k},"n.a.")`);
  f(s,c+(b+22),`=IF(AND(COUNT(${c}${b+5}:${c}${b+7})=3,MIN(${c}${b+5}:${c}${b+7})>=0,MAX(${c}${b+5}:${c}${b+7})<=1,ABS(SUM(${c}${b+5}:${c}${b+7})-1)<0.00000001),"PASS","INVALID")`);
  v(s,c+(b+23),i<10?'PARTIAL':'ESTIMATE');
  s.getRange(c+(b+23)).format.fill=i<10?C.partial:C.estimate;
  f(s,c+(b+36),`='Minimum price'!${c}${pr+3}`);
  f(s,c+(b+37),`='Minimum price'!${c}${pr+9}`);
  if(i<10){
   for(const [off,col]of [[25,'F'],[26,'G'],[27,'H'],[28,'I'],[29,'J'],[30,'K']])f(s,c+(b+off),`=${sum(col,provider,c)}`);
   f(s,c+(b+31),`=${c}${b+25}-${c}${b+27}-${c}${b+29}`);f(s,c+(b+32),`=${c}${b+26}-${c}${b+28}-${c}${b+30}`);
   for(const [off,tokens,cost]of [[5,27,28],[6,29,30],[7,31,32]]){
    f(s,c+(b+off),`=IF(${c}${b+25}>0,${c}${b+tokens}/${c}${b+25},"n.a.")`);
    f(s,c+(b+off+5),`=IF(${c}${b+tokens}>0,${c}${b+cost}/${c}${b+tokens}*1000000,"n.a.")`);
   }
   for(const off of [18,19,20])v(s,c+(b+off),'n.a.');
   f(s,c+(b+34),`=IF(AND(${c}${b+31}>=0,${c}${b+32}>=0),"PASS","FAIL")`);
   f(s,c+(b+35),`=${c}${b+14}+${c}${b+15}+${c}${b+16}-${c}${b+26}/${c}${b+25}*1000000`);
  }else{
   for(let k=0;k<3;k++){
    f(s,c+(b+5+k),`=IF(${c}${b+18+k}="",${prev}${b+5+k},${c}${b+18+k})`);
    f(s,c+(b+10+k),`=IF(AND(ISNUMBER(Inputs!$D$5),Inputs!$D$5>=-1,ISNUMBER(${prev}${b+10+k})),${prev}${b+10+k}*(1+Inputs!$D$5),"n.a.")`);
   }
   for(const off of [25,26,27,28,29,30,31,32,34,35])v(s,c+(b+off),'n.a.');
  }
  f(cons,c+(cr+7),`='Price build'!${c}${b+1}`);
 }
 const overrides=s.getRange(`N${b+18}:O${b+20}`);overrides.format.fill=C.estimate;overrides.format.font.color='#0000FF';overrides.dataValidation={rule:{type:'decimal',operator:'between',formula1:0,formula2:1},ignoreBlanks:true,errorAlert:{style:'stop',title:'Mix share',message:'Enter a share from 0% to 100%, or leave blank to carry the prior month. The three active shares must total 100%.'}};
 s.getRange(`D${b+22}:O${b+22}`).conditionalFormats.add('cellIs',{operator:'equal',formula:'"INVALID"',format:{fill:C.red,font:{color:'#9C0006',bold:true}}});
 s.getRange(`D${b+34}:M${b+34}`).conditionalFormats.add('cellIs',{operator:'equal',formula:'"FAIL"',format:{fill:C.red,font:{color:'#9C0006',bold:true}}});
 s.getRange(`D${b+37}:O${b+37}`).conditionalFormats.add('cellIs',{operator:'greaterThan',formula:.01,format:{fill:C.red,font:{color:'#9C0006',bold:true}}});
}

section(s,89,'Interpretation, sources and limits');
const notes=[
 'ANCHOR: Ramp Economics Lab / Ara Kharazian, tokenPrices vintage captured October 23, 2026. Monthly sum of costs / sum of counts; no equal-weight average of daily or weekly prices.',
 'HARD (green) = exact source observations in Inputs. Blue = ANCHOR / PARTIAL panel transfer or residual. Amber = ESTIMATE forecast and editable assumptions. Derived ratios retain their source limitations.',
 'The input and output series are individually reported; residual counts and costs are subtraction results. Calling that remainder cache is a modeling proxy, conditional on common cohort and exhaustive definitions.',
 'Actual cache-read and cache-write volumes are unavailable. Residual effective rates are not cache-read list prices; they may absorb writes, legacy model mix, other usage or source-definition differences.',
 'October includes weeks ending October 4 and 11 (September 28–October 11). Jan–Sep use contemporaneous samples. November/December carry prior mix and apply Inputs!D5 to category rates each month.',
 'Forecast overrides: leave amber cells blank to carry the prior month, or enter shares that sum to 100%. Changes flow into average price, token consumption and illustrative product allocations.',
 'Official vendor rate cards (Price references; verified October 23) provide context, not an independent company ASP anchor. Model-family weights use a different Ramp denominator and are not multiplied into this bridge.',
 'The lower reference remains a separate scenario. No 70% adjustment is applied to the published benchmark; the denominator gap is unresolved and the two samples cannot be interchanged.',
 'Validation verdict: PARTIAL. Arithmetic, source matching and input guards are checked. No independent company token stock or monthly flow is disclosed here; calibration is internal, not external validation.',
 'Unit conversion: monthly revenue in $bn divided by price in $/million = quadrillion tokens/month. API-only is the closer revenue basis; full ARR is a subscription-inclusive API-equivalent scenario.'
];
notes.forEach((x,i)=>note(s,90+i,x,32));
section(s,102,'October sensitivity — fixed category rates; diagnostic shocks, not a forecast interval');
v(s,'C103','Residual → input shift (pp)');v(s,'D103',.05);v(s,'F103','Residual → output shift (pp)');v(s,'I103',.01);for(const a of ['D103','I103']){s.getRange(a).setNumberFormat(pct);s.getRange(a).format.fill=C.estimate;}
s.getRange('F103:H103').merge();s.getRange('F103:H103').format.wrapText=true;s.getRange('C103:O103').format.rowHeight=32;
s.getRange('C105:G105').values=[['Company','Base $/M','Input shift $/M','Output shift $/M','Output-shift volume change']];s.getRange('C105:G105').format.fill=C.navy;s.getRange('C105:G105').format.font.color='#FFFFFF';s.getRange('C105:G105').format.wrapText=true;s.getRange('C105:G105').format.rowHeight=44;
for(const [row,b,name]of [[106,9,'Anthropic'],[107,49,'OpenAI']]){
 v(s,'C'+row,name);f(s,'D'+row,`=M${b+1}`);
 f(s,'E'+row,`=IF(AND(ISNUMBER($D$103),$D$103>=0,$D$103<=M${b+7}),D${row}+$D$103*(M${b+10}-M${b+12}),"n.a.")`);
 f(s,'F'+row,`=IF(AND(ISNUMBER($I$103),$I$103>=0,$I$103<=M${b+7}),D${row}+$I$103*(M${b+11}-M${b+12}),"n.a.")`);
 f(s,'G'+row,`=IF(AND(ISNUMBER(F${row}),F${row}>0),D${row}/F${row}-1,"n.a.")`);
}s.getRange('D106:F107').setNumberFormat(price);s.getRange('G106:G107').setNumberFormat(pct);
note(s,109,'A small output-share shift matters because output costs more per token. This sensitivity reallocates residual share and holds rates/revenue fixed; it does not claim a verified cache split.');
note(s,111,'Ramp source: https://ramp.com/data/ai-index');
note(s,112,'Claude rate cards: https://platform.claude.com/docs/en/about-claude/pricing');
note(s,113,'OpenAI rate cards: https://developers.openai.com/api/docs/pricing');

// Put the requested mix beside the primary outputs and route the price through the build.
format(cons,49,58,43);section(cons,49,'Explicit token-category mix — shares of all tokens');
for(const [row,b,offset,label]of [[50,9,5,'Anthropic: uncached input'],[51,9,6,'Anthropic: output'],[52,9,7,'Anthropic: cache / other residual'],[54,49,5,'OpenAI: uncached input'],[55,49,6,'OpenAI: output'],[56,49,7,'OpenAI: cache / other residual']]){
 v(cons,'C'+row,label);for(const c of cols)f(cons,c+row,`='Price build'!${c}${b+offset}`);cons.getRange(`D${row}:O${row}`).setNumberFormat(pct);if(offset===7)cons.getRange(`D${row}:M${row}`).format.fill=C.partial;cons.getRange(`N${row}:O${row}`).format.fill=C.estimate;
}
note(cons,58,'Residual is an unclassified possible-cache proxy, not measured cache reads. Price build shows weights, effective rates, formula, forecast overrides and sensitivity.',32);
v(cons,'C6','Base prices now use the explicit weighted bridge on Price build. Historical benchmarks are retained; forecast mix is editable there.');cons.getRange('C6').format.font.color=C.gray;
v(cons,'C46','Minimum price retains the lower benchmark; Price build shows input/output/residual weights; Token mix retains illustrative product allocations.');
v(inp,'C33','October uses weeks ending October 4 and 11. November/December carry prior category mix unless overridden in Price build; Inputs!D5 changes rates.');
v(min,'C43','Monthly samples include cross-month weeks. October is partial. The lower reference remains separate from editable category-mix forecasts on Price build.');
v(refs,'C6','Rate cards document the history. Price build explains the selected Ramp average and explicit input, output and unclassified cache/other residual weights.');
v(mix,'C6','Token-category shares and rates are on Price build. Family shares here use tokenVolumes, a different denominator; do not cross-weight the price build.');mix.getRange('C6').format.font.color=C.gray;
wb.recalculate();

const get=(sh,a)=>sh.getRange(a).values[0][0];
function close(a,b,k){if(typeof a!=='number'||Math.abs(a-b)>1e-9*Math.max(1,Math.abs(b)))throw Error(`${k}: ${a} != ${b}`);}
for(const q of data.monthly){const {b,cr}=cfg[q.provider],c=cols[q.month-1];for(const [off,key]of [[1,'base_price'],[5,'input_share'],[6,'output_share'],[7,'residual_share'],[10,'input_rate'],[11,'output_rate'],[12,'residual_rate']])close(get(s,c+(b+off)),q[key],`${q.provider}/${q.month}/${key}`);close(get(cons,c+(cr+7)),q.base_price,'linked price');}
for(const q of original.monthly_expected){const {cr}=cfg[q.provider],c=cols[q.month-1];close(get(cons,c+(cr+8)),q.base_gross_tokens_Q_month,'baseline volume');close(get(cons,c+(cr+9)),q.api_gross_tokens_Q_month,'baseline API volume');}

// Meaningful edits must propagate, invalid shares must not create credible-looking volumes.
const anth=data.monthly.find(x=>x.provider==='anthropic'&&x.month===10);
v(s,'N27',anth.input_share+.05);v(s,'N29',anth.residual_share-.05);wb.recalculate();
close(get(s,'N10'),anth.five_pp_residual_to_input_price,'input mix sensitivity');close(get(s,'O10'),anth.five_pp_residual_to_input_price,'carry prior mix');
const nov=original.monthly_expected.find(x=>x.provider==='anthropic'&&x.month===11);close(get(cons,'N17'),nov.gross_arr_busd/12/anth.five_pp_residual_to_input_price,'mix alters consumption');
v(s,'N29',.99);wb.recalculate();if(get(s,'N10')!=='n.a.'||get(cons,'N17')!=='n.a.')throw Error('Invalid sum not blocked');
v(s,'N29','invalid');wb.recalculate();if(get(cons,'N17')!=='n.a.')throw Error('Text share not blocked');
s.getRange('N27:O29').clear({applyTo:'contents'});wb.recalculate();
v(inp,'D5',-.1);wb.recalculate();close(get(s,'O10'),anth.base_price*.81,'forecast rate change');v(inp,'D5',-1);wb.recalculate();if(get(cons,'N17')!=='n.a.')throw Error('Zero price not blocked');
for(const bad of [-1.1,'invalid']){v(inp,'D5',bad);wb.recalculate();if(get(cons,'N17')!=='n.a.'||get(cons,'O35')!=='n.a.')throw Error('Invalid price change not blocked');}v(inp,'D5',0);wb.recalculate();
for(const q of data.monthly){const {b}=cfg[q.provider],c=cols[q.month-1];close(get(s,c+(b+1)),q.base_price,'restored base');}
const scan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:50},summary:'Price and mix final formula scan'});
await fs.writeFile(path.join(here,'mix_error_scan.jsonl'),scan.ndjson);
for(const [name,sheet,range]of [['price_build_anthropic','Price build','C1:O32'],['price_build_openai','Price build','C49:O72'],['mix_consumption','Consumption','C49:O58'],['price_build_sensitivity','Price build','C89:O113'],['category_raw','Inputs','C281:K291']]){
 const blob=await wb.render({sheetName:sheet,range,scale:1.3,format:'png'});await fs.writeFile(path.join(here,name+'.png'),new Uint8Array(await blob.arrayBuffer()));
}
await(await SpreadsheetFile.exportXlsx(wb)).save(output);
const report={source,output,tests:['24 monthly prices and category shares/rates match independent Python','24 baseline full-ARR and API volumes preserved','Forecast mix changes propagate to price and consumption; next month inherits mix','Invalid sum and text shares blocked','Forecast price decay, zero-price and invalid-price guards passed'],scan:scan.ndjson,october:data.monthly.filter(x=>x.month===10)};
await fs.writeFile(path.join(here,'mix_update_verification.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
