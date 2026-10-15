import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const require = createRequire('C:/Users/Felipe.monteiro/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/package.json');
const {Workbook, SpreadsheetFile} = await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const dir=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(dir,'../../../..');
const outputDir=path.join(root,'_wiki/_data/outputs/anthropic-2026-10-15');
await fs.mkdir(outputDir,{recursive:true});
const src=JSON.parse(await fs.readFile(path.join(dir,'source_extract.json'),'utf8'));
let nativeValidation=null;try{nativeValidation=JSON.parse((await fs.readFile(path.join(dir,'native_excel_checks.json'),'utf8')).replace(/^\uFEFF/,''));}catch{}
const srcA=src.sheets.Anthropic, srcT=src.sheets['ARR Tracker'];
const val=(s,c)=>s[c]?.value ?? null;
const cols=['E','F','G','H','I','J'], scols=['AA','AB','AC','AD','AE','AF'];
const years=[2025,2026,2027,2028,2029,2030];
const mc=['P','Q','R','S','T','U','V','W','X','Y','Z','AA'];
const wb=Workbook.create();
const sheets={};
for(const n of ['Summary','Drivers','Operating','ARR 2026','Compute','Cash flow','Sources','Review']) sheets[n]=wb.worksheets.add(n);
const C={ink:'#203246',navy:'#233D53',blue:'#0000FF',link:'#008000',light:'#EAF0F4',hard:'#E4EFDF',partial:'#E4EDF8',estimate:'#FFF0CB',red:'#F9DDDB',gray:'#687684'};
const num='#,##0.0;(#,##0.0);"-"', money='$#,##0.0;($#,##0.0);"-"', pct='0.0%;(0.0%);"-"', diff='#,##0.00;(#,##0.00);0.00';
function set(n,a,v){sheets[n].getRange(a).values=[[v]];}
function formula(n,a,f){sheets[n].getRange(a).formulas=[[f]];sheets[n].getRange(a).format.font.color=(n==='Summary'?'#203246':f.includes('!')?C.link:'#000000');}
function row(n,r,label,vs,format=num){set(n,'C'+r,label);if(vs){sheets[n].getRange(`E${r}:J${r}`).values=[vs];sheets[n].getRange(`E${r}:J${r}`).setNumberFormat(format);}}
function fill(n,r,fn,format=num){cols.forEach((c,i)=>formula(n,c+r,fn(c,i)));sheets[n].getRange(`E${r}:J${r}`).setNumberFormat(format);}
function band(n,r,label){set(n,'C'+r,label);sheets[n].getRange(`C${r}:J${r}`).format={fill:C.navy,font:{color:'#FFFFFF',bold:true},rowHeight:24};}
function total(n,r){sheets[n].getRange(`C${r}:J${r}`).format={font:{bold:true},borders:{top:{style:'thin',color:'#7A8B98'}}};}
function note(n,r,text){set(n,'C'+r,text);sheets[n].getRange('C'+r).format.font={color:C.gray,size:10};}
function tag(n,a,type){set(n,a,type);sheets[n].getRange(a).format.fill=type==='HARD'?C.hard:type==='ESTIMATE'?C.estimate:C.partial;}
function ratio(n,r){sheets[n].getRange(`C${r}:J${r}`).format.font.italic=true;}
function setup(n,last=80){const s=sheets[n];s.showGridLines=false;s.getRange(`A1:O${last}`).format={font:{name:'Arial',size:10,color:C.ink},rowHeight:20,verticalAlignment:'center'};s.getRange(`A1:B${last}`).format.columnWidth=2;s.getRange(`C1:C${last}`).format.columnWidth=44;s.getRange(`D1:D${last}`).format.columnWidth=12;s.getRange(`E1:J${last}`).format.columnWidth=15;s.getRange(`K1:K${last}`).format.columnWidth=3;s.getRange(`L1:L${last}`).format.columnWidth=46;s.getRange(`M1:O${last}`).format.columnWidth=18;s.getRange(`E9:J${last}`).format.horizontalAlignment='right';s.getRange(`E9:J${last}`).setNumberFormat(num);set(n,'C2',n==='Summary'?'Anthropic financial model':n);s.getRange('C2:J2').format={font:{size:16,bold:true},rowHeight:30,borders:{bottom:{style:'thin',color:C.ink}}};if(n!=='Drivers'){set(n,'C4','Case selected');formula(n,'E4',"=CHOOSE('Drivers'!$E$4,\"House base\",\"Downside\",\"Upside\")");s.getRange('E4').format={font:{color:C.link},borders:{preset:'outside',style:'dotted',color:C.gray},horizontalAlignment:'center'};}s.getRange('E8:J8').values=[years];s.getRange('E8:J8').setNumberFormat('0');s.getRange('C8:J8').format={fill:C.navy,font:{color:'#FFFFFF',bold:true},horizontalAlignment:'center',rowHeight:24};set(n,'C8','USD million, calendar years');set(n,'D8','Basis');if(n!=='Summary')s.freezePanes.freezeRows(8);s.freezePanes.freezeColumns(4);}
for(const n of Object.keys(sheets))setup(n,n==='Sources'?90:n==='Drivers'?85:n==='Review'?65:65);
sheets.Summary.tabColor=C.navy;sheets.Drivers.tabColor='#668398';sheets.Sources.tabColor='#D2BEA0';

// Frozen source observations. HARD refers to exact extraction, not forecast certainty.
note('Sources',3,'Capstone / Felipe Monteiro, AI Model.xlsx saved 15-Oct-2026. Values are frozen from the supplied house model.');
note('Sources',6,'HARD = exact sourced input. Forecasts remain house assumptions; PARTIAL = derived/incomplete; ESTIMATE = new stress.');
const sourceRows={8:3,9:15,10:30,11:19,12:70,13:47,14:36,15:65,16:136,17:33,20:107,21:88,23:146,24:71,25:85,26:8,27:34};
const labels={8:'Gross revenue',9:'Direct API / gross revenue',10:'Subscriptions / gross revenue',11:'Cloud API / gross revenue',12:'Inference GM before revenue share',13:'Training compute cost',14:'Compute / total operating costs',15:'Inference compute cost',16:'Other costs: source residual',17:'Total operating costs, before revshare',18:'Cloud revenue-share rate: annual model',19:'Cloud revenue-share rate: ARR tracker',20:'Average 1P capacity, GW',21:'Rental equivalent, USDm / GW-year',22:'1P compute allocated to training',23:'Source line labelled EBIT',24:'Post-share GM / gross revenue',25:'Average direct capacity, house GW',26:'Source revenue / inference GW-year',27:'Source compute cost / direct GW-year'};
for(const [r,sr] of Object.entries(sourceRows)){const rn=Number(r);row('Sources',rn,labels[rn],scols.map(c=>val(srcA,c+sr)),[9,10,11,12,14,24].includes(rn)?pct:num);tag('Sources','D'+rn,'HARD');set('Sources','L'+rn,`Capstone 15-Oct-26: Anthropic!AA${sr}:AF${sr}`);sheets.Sources.getRange(`E${rn}:J${rn}`).format.font.color=C.blue;sheets.Sources.getRange(`E${rn}:J${rn}`).format.fill=C.hard;}
set('Sources','C25','Average direct GW demand, cloud + 1P');
row('Sources',18,labels[18],Array(6).fill(.25),pct);tag('Sources','D18','HARD');set('Sources','L18','Capstone 15-Oct-26: AA71 shared formula, 0.25');
row('Sources',19,labels[19],[null,.2,null,null,null,null],pct);tag('Sources','D19','HARD');set('Sources','L19','Capstone 15-Oct-26: ARR Tracker!P48; 2026 only');
row('Sources',22,labels[22],[null,...scols.slice(1).map(c=>val(srcA,c+'50'))],pct);tag('Sources','D22','HARD');set('Sources','L22','Capstone 15-Oct-26: Anthropic!AB50:AF50');
for(const r of [18,19,22]){sheets.Sources.getRange(`E${r}:J${r}`).format.fill=C.hard;sheets.Sources.getRange(`E${r}:J${r}`).format.font.color=C.blue;}
// Put year headers above source data because row 8 is a numeric input.
sheets.Sources.getRange('E7:J7').values=[years];sheets.Sources.getRange('E7:J7').setNumberFormat('0');sheets.Sources.getRange('C8:J8').format={fill:'#FFFFFF',font:{color:C.ink,bold:false},horizontalAlignment:'left'};sheets.Sources.getRange('E8:J8').format={font:{color:C.blue},fill:C.hard,horizontalAlignment:'right'};sheets.Sources.freezePanes.freezeRows(7);
row('Sources',28,'2026 Q1–Q3 gross revenue',[null,['P','Q','R'].reduce((a,c)=>a+val(srcA,c+'3'),0),null,null,null,null]);tag('Sources','D28','HARD');set('Sources','L28','Capstone 15-Oct-26: Anthropic!P3:R3');
row('Sources',29,'2026 Q4 gross revenue',[null,val(srcA,'S3'),null,null,null,null]);tag('Sources','D29','HARD');set('Sources','L29','Capstone 15-Oct-26: Anthropic!S3');
row('Sources',30,'2025 sum of quarterly revenue',[['L','M','N','O'].reduce((a,c)=>a+val(srcA,c+'3'),0),null,null,null,null,null]);tag('Sources','D30','HARD');set('Sources','L30','Capstone 15-Oct-26: Anthropic!L3:O3');
set('Sources','C34','2026 monthly house inputs');sheets.Sources.getRange('E35:P35').values=[Array.from({length:12},(_,i)=>new Date(Date.UTC(2026,i,1)))];sheets.Sources.getRange('E35:P35').setNumberFormat('mmm-yy');
for(const [r,sr,label] of [[36,40,'Average monthly annualized gross revenue'],[37,44,'Monthly gross revenue'],[38,41,'Monthly growth'],[39,47,'Average monthly net ARR, tracker basis']]){set('Sources','C'+r,label);tag('Sources','D'+r,'HARD');sheets.Sources.getRange(`E${r}:P${r}`).values=[mc.map(c=>val(srcT,c+sr))];sheets.Sources.getRange(`E${r}:P${r}`).format={fill:C.hard,font:{color:C.blue}};sheets.Sources.getRange(`E${r}:P${r}`).setNumberFormat(r===38?pct:num);}
note('Sources',41,'Monthly inputs: Capstone 15-Oct-26, ARR Tracker!P40:AA49. Jan–Sep are model estimates; Oct–Dec are forecasts.');
note('Sources',42,'Row 40 is labelled Average Monthly Reported ARR Gross. December is a monthly average proxy, not verified exit ARR.');
band('Sources',44,'Observed comparison data');
sheets.Sources.getRange('E45:H45').values=[['Q1:26','Q2:26','Q3:26','Jul-26 run-rate']];
sheets.Sources.getRange('E46:H46').values=[[4730,11500,16800,65000]];sheets.Sources.getRange('E46:H46').format={fill:C.partial,font:{color:C.blue}};set('Sources','C46','Reported revenue / run-rate, USDm');tag('Sources','D46','ANCHOR');
note('Sources',48,'Q1: approximately $4.73bn. Q2: more than $11.5bn; the numeric value is a lower bound, not an exact actual.');
note('Sources',49,'Q3: $16.8bn press-reported investor disclosure. July run-rate: about $65bn. Neither is audited here.');
const refs=[
['H1','Capstone / Felipe Monteiro','2026-10-15','House projections','AI Model.xlsx; Anthropic, ARR Tracker',src.source],
['B1','Bloomberg / Bailey Lipschultz, Rachel Metz','2026-08-14','Q1 $4.73bn; Q2 >$11.5bn','Primary reporting, live page checked','https://news.bloomberglaw.com/artificial-intelligence/anthropic-revenue-surges-to-over-11-5-billion-in-second-quarter'],
['B2','The Information / Cory Weinberg','2026-10-14','Q3 $16.8bn','Public indexed excerpt verified; body unavailable','https://www.theinformation.com/briefings/anthropic-reports-16-8-billion-third-quarter-revenue'],
['B3','CNBC / Kate Rooney','2026-08-18','July annualized revenue ~$65bn','Saved observation; not newly fetched','https://www.youtube.com/watch?v=3U_0AKZhi_I'],
['B4','Anthropic company announcement','2026-05-28','>$47bn run-rate earlier in May','Primary page checked; date precision approximate','https://www.anthropic.com/news/series-h'],
['S1','SemiAnalysis / Brookhart, Huang, Patel','2026-07-08','2026 quarterly P&L comparison','Archived figure transcription; estimates, not reported actuals','_wiki/_data/figures/Semianalysis_Anthropic_IPO_Financials_Sneak_Peek.md']
];
set('Sources','C52','Source register');
refs.forEach((r,i)=>{const rr=54+i*4;set('Sources','C'+rr,r[0]+' '+r[1]);set('Sources','G'+rr,r[2]);set('Sources','C'+(rr+1),r[3]+' — '+r[4]);set('Sources','C'+(rr+2),r[5]);sheets.Sources.getRange(`C${rr+2}:P${rr+2}`).format.font={size:9,color:C.gray};});
note('Sources',80,'Archived source fingerprint: '+src.sha256);
note('Sources',81,'Source workbook saved 2026-10-15 13:15:32 UTC. All figures extracted without recalculating or changing it.');
note('Sources',83,'GM scope: Anthropic!AB70 comment, 14-Sep-26, cites FT >80% before distribution share and training; 82% is the house point.');
note('Sources',84,'The compute/total-cost fraction has no independent observed cost anchor. Exact extraction does not validate the assumption.');

// One case selector and one set of active assumptions.
set('Drivers','C4','Case: 1 House / 2 Down / 3 Up');set('Drivers','E4',1);sheets.Drivers.getRange('E4').dataValidation={rule:{type:'list',values:['1','2','3']}};
set('Drivers','G3','Revenue multiplier');set('Drivers','G4',1);set('Drivers','J3','Inference GM delta');set('Drivers','J4',0);
set('Drivers','G5',0);set('Drivers','J5',0);set('Drivers','G6','Revenue-share delta');set('Drivers','J6','Compute-share delta');
for(const a of ['E4','G4','J4','G5','J5'])sheets.Drivers.getRange(a).format={fill:C.estimate,font:{color:C.blue},borders:{preset:'outside',style:'dotted',color:C.gray}};
sheets.Drivers.getRange('J4:J5').setNumberFormat(pct);sheets.Drivers.getRange('G5').setNumberFormat(pct);sheets.Drivers.getRange('G4').setNumberFormat('0.00x');
note('Drivers',7,'Amber controls are ESTIMATE stresses, dated 15-Oct-26. Neutral multipliers preserve the house base.');
const groups=[
{r:10,label:'Gross revenue',sr:8,fmt:num,down:.8,up:1.2,mode:'revenue'},
{r:16,label:'Inference GM before revenue share',sr:12,fmt:pct,down:-.05,up:.05,mode:'margin'},
{r:22,label:'Training compute cost',sr:13,fmt:num,down:1.2,up:.9,mode:'training'},
{r:28,label:'Compute / total operating costs',sr:14,fmt:pct,down:-.05,up:.05,mode:'costshare'},
{r:34,label:'Cloud revenue share',sr:18,fmt:pct,down:0,up:0,mode:'share'}
];
for(const g of groups){row('Drivers',g.r,g.label);tag('Drivers','D'+g.r,'ACTIVE');for(const [off,name]of [[1,'House base'],[2,'Downside'],[3,'Upside']]){row('Drivers',g.r+off,name);tag('Drivers','D'+(g.r+off),off===1?'HARD':'ESTIMATE');}
 cols.forEach((c,i)=>{formula('Drivers',c+(g.r+1),`='Sources'!${c}${g.sr}`);for(const [off,shock]of [[2,g.down],[3,g.up]]){let f=`=${c}${g.r+1}`;if(i>0){if(g.mode==='revenue')f=i===1?`='Sources'!F28+'Sources'!F29*${shock}`:`=${c}${g.r+1}*${shock}`;if(g.mode==='training')f=`=${c}${g.r+1}*${shock}`;if(['margin','costshare'].includes(g.mode))f=`=${c}${g.r+1}+(${shock})`;}formula('Drivers',c+(g.r+off),f);}
 let choose=`CHOOSE($E$4,${c}${g.r+1},${c}${g.r+2},${c}${g.r+3})`;
 let f=`=${choose}`;if(i>0){if(g.mode==='revenue')f=i===1?`='Sources'!F28+(${choose}-'Sources'!F28)*$G$4`:`=${choose}*$G$4`;if(g.mode==='margin')f=`=${choose}+$J$4`;if(g.mode==='costshare')f=`=${choose}+$J$5`;if(g.mode==='share')f=`=${choose}+$G$5`;}
 // The selected case must be complete; blank and genuine zero stay distinct.
 const chosenRange=[c+(g.r+1),c+(g.r+2),c+(g.r+3)];
 formula('Drivers',c+g.r,`=IF(CHOOSE($E$4,${chosenRange.map(a=>'ISNUMBER('+a+')').join(',')}),${f.slice(1)},"n.a.")`);
 });sheets.Drivers.getRange(`E${g.r}:J${g.r+3}`).setNumberFormat(g.fmt);sheets.Drivers.getRange(`C${g.r}:J${g.r}`).format.fill=C.light;sheets.Drivers.getRange(`C${g.r}:J${g.r}`).format.font.bold=true;set('Drivers','L'+g.r,`House: Sources row ${g.sr}; as of 15-Oct-26`);}
for(const [r,sr,label,fmt]of [[40,9,'Direct API / gross revenue',pct],[41,10,'Subscriptions / gross revenue',pct],[42,20,'Average 1P capacity, GW',num],[43,21,'Rental equivalent, USDm / GW-year',num],[44,22,'1P training allocation',pct]]){row('Drivers',r,label);fill('Drivers',r,(c,i)=>r===44&&i===0?'="n.a."':`='Sources'!${c}${sr}`,fmt);tag('Drivers','D'+r,'HARD');set('Drivers','L'+r,`Capstone 15-Oct-26: Sources row ${sr}`);}
note('Drivers',46,'HARD means exact house input, not proven economics. Other costs are derived from the compute-share assumption.');
note('Drivers',47,'25% revenue share follows the annual model. The ARR tracker uses 20%; adjust G5 to -5.0% to test it.');
note('Drivers',48,'2025 inputs do not change with cases. 2026 revenue stress affects Q4 only; costs have annual assumptions.');
note('Drivers',49,'Stress amounts are editable scenarios, not calibrated forecasts. Invalid economic ranges are flagged in Review.');
set('Drivers','C52','2030 operating surplus: revenue and inference margin');set('Drivers','C53','Rows: GM delta. Columns: revenue multiplier. USDm.');
formula('Drivers','F54',"=IF(AND('Compute'!J19>=0,'Compute'!J20>=0),'Operating'!J31,\"n.a.\")");sheets.Drivers.getRange('G54:K54').values=[[.8,.9,1,1.1,1.2]];sheets.Drivers.getRange('F55:F59').values=[[-.1],[-.05],[0],[.05],[.1]];sheets.Drivers.getRange('G54:K54').setNumberFormat('0.00x');sheets.Drivers.getRange('F55:F59').setNumberFormat(pct);
sheets.Drivers.dataTables.add('F54:K59',{rowInput:'G4',columnInput:'J4'});
set('Drivers','C62','2030 operating surplus: revenue share and other costs');set('Drivers','C63','Rows: compute-share delta. Columns: revenue-share delta. USDm.');
formula('Drivers','F64',"=IF(AND('Compute'!J19>=0,'Compute'!J20>=0),'Operating'!J31,\"n.a.\")");sheets.Drivers.getRange('G64:K64').values=[[-.05,-.025,0,.025,.05]];sheets.Drivers.getRange('F65:F69').values=[[-.1],[-.05],[0],[.05],[.1]];sheets.Drivers.getRange('G64:K64').setNumberFormat(pct);sheets.Drivers.getRange('F65:F69').setNumberFormat(pct);
sheets.Drivers.dataTables.add('F64:K69',{rowInput:'G5',columnInput:'J5'});
for(const r of ['G55:K59','G65:K69']){sheets.Drivers.getRange(r).setNumberFormat(num);sheets.Drivers.getRange(r).conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:C.red,font:{color:'#9C2727'}}});}
sheets.Drivers.getRange('K54:K69').format.columnWidth=15;note('Drivers',72,'Native two-variable Excel tables recalculate the same operating model. All other active assumptions stay constant.');
note('Drivers',73,'n.a. = cost below the embedded 1P capacity equivalent; infeasible while the house capacity assumptions stay fixed.');

// Revenue to profit, with each cost counted once.
note('Operating',3,'2025 is reconstructed model history. 2026–2030 are forecasts. Operating surplus is not verified GAAP EBIT.');
const oplabels={10:'Gross revenue',11:'Year-on-year growth',13:'Direct API revenue',14:'Cloud-distributed API revenue',15:'Subscription revenue',16:'Revenue reconciliation',18:'Cloud revenue-share rate',19:'Cloud distribution fee',20:'Net economic revenue',22:'Inference GM before revenue share',23:'Inference compute cost',24:'Gross profit after revenue share',25:'Gross profit / gross revenue',26:'Gross profit / net economic revenue',28:'Training compute cost',29:'Compute / total operating costs',30:'Other operating costs: residual',31:'Modeled operating surplus',32:'Operating surplus / gross revenue',33:'Operating surplus before training',35:'Total costs before revenue share',36:'Total costs including revenue share',38:'Year-on-year other-cost growth',40:'Gross revenue at operating break-even'};
for(const[r,l]of Object.entries(oplabels))row('Operating',Number(r),l);
fill('Operating',10,c=>`='Drivers'!${c}10`,money);fill('Operating',11,(c,i)=>i?`=${c}10/${cols[i-1]}10-1`:'="n.a."',pct);
fill('Operating',13,c=>`=${c}10*'Drivers'!${c}40`);fill('Operating',15,c=>`=${c}10*'Drivers'!${c}41`);fill('Operating',14,c=>`=${c}10-${c}13-${c}15`);fill('Operating',16,c=>`=SUM(${c}13:${c}15)-${c}10`,diff);
fill('Operating',18,c=>`='Drivers'!${c}34`,pct);fill('Operating',19,c=>`=${c}14*${c}18`);fill('Operating',20,c=>`=${c}10-${c}19`,money);
fill('Operating',22,c=>`='Drivers'!${c}16`,pct);fill('Operating',23,c=>`=${c}10*(1-${c}22)`);fill('Operating',24,c=>`=${c}20-${c}23`,money);fill('Operating',25,c=>`=${c}24/${c}10`,pct);fill('Operating',26,c=>`=${c}24/${c}20`,pct);
fill('Operating',28,c=>`='Drivers'!${c}22`);fill('Operating',29,c=>`='Drivers'!${c}28`,pct);fill('Operating',30,c=>`=(${c}23+${c}28)*(1/${c}29-1)`);fill('Operating',31,c=>`=${c}24-${c}28-${c}30`,money);fill('Operating',32,c=>`=${c}31/${c}10`,pct);fill('Operating',33,c=>`=${c}31+${c}28`);
fill('Operating',35,c=>`=SUM(${c}23,${c}28,${c}30)`);fill('Operating',36,c=>`=${c}35+${c}19`);fill('Operating',38,(c,i)=>i?`=${c}30/${cols[i-1]}30-1`:'="n.a."',pct);
fill('Operating',40,c=>`=IF(1-('Drivers'!${c}34*(1-'Drivers'!${c}40-'Drivers'!${c}41))-(1-${c}22)/${c}29>0,(${c}28/${c}29)/(1-('Drivers'!${c}34*(1-'Drivers'!${c}40-'Drivers'!${c}41))-(1-${c}22)/${c}29),"n.a.")`);
for(const r of [10,20,24,31,33,36])total('Operating',r);for(const r of [11,18,22,25,26,29,32,38])ratio('Operating',r);
note('Operating',43,'Other costs = (inference + training) × (1 / compute share − 1). This preserves the house residual.');
note('Operating',44,'Revenue sharing is deducted once, separately from inference. Whether other costs already embed part of it is unverified.');
note('Operating',45,'SBC, depreciation, leases and one-time charges are not separately identified. Do not treat this surplus as GAAP or FCF.');
note('Operating',46,'Break-even holds training, channel mix, margin and the compute cost fraction constant at each year’s active values.');

// Monthly annualized averages to recognized-revenue proxy; Q1-Q3 remain unchanged.
note('ARR 2026',3,'Monthly average annualized revenue / 12. This is the house recognition proxy, not a disclosed GAAP policy.');
sheets['ARR 2026'].getRange('E8:P8').values=[Array.from({length:12},(_,i)=>new Date(Date.UTC(2026,i,1)))];sheets['ARR 2026'].getRange('E8:P8').setNumberFormat('mmm-yy');sheets['ARR 2026'].getRange('K1:P35').format.columnWidth=15;set('ARR 2026','C8','USD million');
for(const[r,l]of [[10,'House monthly average annualized revenue'],[11,'House monthly revenue'],[12,'Active monthly gross revenue'],[13,'Active monthly annualized average'],[14,'Month-on-month growth'],[15,'Net economic monthly revenue'],[16,'Net annualized monthly average'],[17,'Evidence status']])set('ARR 2026','C'+r,l);
for(let i=0;i<12;i++){const c=String.fromCharCode(69+i);formula('ARR 2026',c+'10',`='Sources'!${c}36`);formula('ARR 2026',c+'11',`='Sources'!${c}37`);formula('ARR 2026',c+'12',i<9?`=${c}11`:`=('Drivers'!F10-SUM($E$11:$M$11))*${c}11/SUM($N$11:$P$11)`);formula('ARR 2026',c+'13',`=${c}12*12`);formula('ARR 2026',c+'14',i?`=${c}13/${String.fromCharCode(68+i)}13-1`:'="n.a."');formula('ARR 2026',c+'15',`=${c}12*(1-(1-'Drivers'!$F$40-'Drivers'!$F$41)*'Drivers'!$F$34)`);formula('ARR 2026',c+'16',`=${c}15*12`);set('ARR 2026',c+'17',i<9?'Model estimate':'Forecast');}
sheets['ARR 2026'].getRange('E10:P16').setNumberFormat(num);sheets['ARR 2026'].getRange('E14:P14').setNumberFormat(pct);
sheets['ARR 2026'].getRange('K8:P8').format={fill:C.navy,font:{color:'#FFFFFF',bold:true},horizontalAlignment:'center'};
set('ARR 2026','C21','Quarter / full-year revenue');sheets['ARR 2026'].getRange('E21:I21').values=[['Q1:26','Q2:26','Q3:26','Q4:26','2026']];
for(const[r,l]of [[22,'Gross revenue'],[23,'Net economic revenue'],[24,'Quarterly gross revenue growth']])set('ARR 2026','C'+r,l);
for(let q=0;q<4;q++){const c=String.fromCharCode(69+q),start=String.fromCharCode(69+3*q),end=String.fromCharCode(71+3*q);formula('ARR 2026',c+'22',`=SUM(${start}12:${end}12)`);formula('ARR 2026',c+'23',`=SUM(${start}15:${end}15)`);formula('ARR 2026',c+'24',q?`=${c}22/${String.fromCharCode(68+q)}22-1`:'="n.a."');}formula('ARR 2026','I22','=SUM(E22:H22)');formula('ARR 2026','I23','=SUM(E23:H23)');sheets['ARR 2026'].getRange('E24:H24').setNumberFormat(pct);total('ARR 2026',22);
note('ARR 2026',27,'Q4 scenarios preserve the house October–December monthly weights; they do not refit earlier months.');
note('ARR 2026',28,'December annualized average is a run-rate proxy. It is not added to annual revenue and is not certified as exit ARR.');
note('ARR 2026',29,'Monthly 2027 source cells are empty and quarterly zeros are mechanical; forecast 2027 onward is annual only.');sheets['ARR 2026'].getRange('I21').setNumberFormat('0');

// Capacity cross-check; rental equivalents are not owned capex or a delivered-power forecast.
note('Compute',3,'GW-year equivalents use the house rental benchmark. Facility-vs-IT basis is unconfirmed; do not sum with deal MW.');
for(const[r,l]of [[10,'Average 1P capacity, house GW'],[11,'Rental equivalent / GW-year, USDm'],[12,'Embedded 1P compute equivalent'],[13,'Allocation to training'],[14,'Embedded 1P training equivalent'],[15,'Embedded 1P inference equivalent'],[17,'Total training compute cost'],[18,'Total inference compute cost'],[19,'Remaining rented training cost'],[20,'Remaining rented inference cost'],[21,'Total compute cost'],[23,'Training GW-year equivalent'],[24,'Inference GW-year equivalent'],[25,'Total GW-year equivalent'],[27,'Gross revenue / inference GW-year'],[28,'1P rental equivalent / total compute']])row('Compute',r,l);
fill('Compute',10,c=>`='Drivers'!${c}42`);fill('Compute',11,c=>`='Drivers'!${c}43`);fill('Compute',12,c=>`=${c}10*${c}11`);fill('Compute',13,(c,i)=>i?`='Drivers'!${c}44`:'="n.a."',pct);fill('Compute',14,(c,i)=>i?`=${c}12*${c}13`:'=0');fill('Compute',15,c=>`=${c}12-${c}14`);fill('Compute',17,c=>`='Operating'!${c}28`);fill('Compute',18,c=>`='Operating'!${c}23`);fill('Compute',19,c=>`=${c}17-${c}14`);fill('Compute',20,c=>`=${c}18-${c}15`);fill('Compute',21,c=>`=SUM(${c}17:${c}18)`);fill('Compute',23,c=>`=${c}17/${c}11`);fill('Compute',24,c=>`=${c}18/${c}11`);fill('Compute',25,c=>`=SUM(${c}23:${c}24)`);fill('Compute',27,c=>`='Operating'!${c}10/${c}24`);fill('Compute',28,c=>`=${c}12/${c}21`,pct);for(const r of[12,21,25])total('Compute',r);
row('Compute',29,'Average direct GW demand, cloud + 1P');fill('Compute',29,c=>`='Sources'!${c}25`);tag('Compute','D29','HARD');
row('Compute',30,'Compute cost / avg direct GW-year');fill('Compute',30,c=>`=IF(AND(ISNUMBER(${c}29),${c}29>0),${c}21/${c}29,"n.a.")`);tag('Compute','D30','PARTIAL');tag('Compute','D27','PARTIAL');
for(const r of[27,28,30])ratio('Compute',r);
set('Compute','L27','Capstone 15-Oct-26: Anthropic!AA8:AD8 = revenue / inference GW; extended to 2030.');
set('Compute','L29','Capstone 15-Oct-26: Anthropic!AA85:AF85. Fixed house denominator across scenarios.');
set('Compute','L30','Capstone 15-Oct-26: Anthropic!AB34:AD34 = row 35 / row 85; extended to 2025 and 2029–30.');
note('Compute',32,'The 1P equivalent is already embedded in inference and training costs. It is not added again.');
note('Compute',33,'Row 11 rental benchmark is the simple average of NVIDIA, TPU and Trainium inputs; it differs from row 30 cost/GW.');
note('Compute',34,'Cloud commitments, chip purchases, operator contracts and financing can overlap. No summed deal value enters this model.');
note('Compute',35,'No observed installed-capacity anchor on a matching basis: capacity calculations are internally consistent only.');
note('Compute',36,'Revenue/GW = gross revenue / inference GW. Cost/GW = annual training + inference spend / average direct GW.');
note('Compute',37,'Direct GW is model-implied cloud + 1P demand, fixed to house forecasts in scenarios; cost/GW varies with spending.');
note('Compute',38,'Capstone 15-Oct-26, Anthropic rows 8 and 34: existing ratios reconciled; blank years extended using the same formulas.');
note('Compute',39,'Revenue/inference GW = rental benchmark / (1 - inference GM); revenue cancels. This is not independent monetization evidence.');

// Cash conversion stays unavailable until real inputs are supplied; zero is a valid entry.
note('Cash flow',3,'Cash flow is unavailable until the amber inputs are completed. Enter actual zeros explicitly where justified.');
row('Cash flow',10,'Modeled operating surplus');fill('Cash flow',10,c=>`='Operating'!${c}31`);
const cashLabels=['Noncash costs already included: add back','Cash taxes paid','Cash interest paid','Increase in working capital, excl. prepayments','Cash capex for assets paid by Anthropic','Increase in compute prepayments, excl. WC','Lease principal not included in operating costs','Other cash adjustments, signed'];
cashLabels.forEach((l,i)=>{const r=12+i;row('Cash flow',r,l,Array(6).fill(null));tag('Cash flow','D'+r,'MISSING');sheets['Cash flow'].getRange(`E${r}:J${r}`).format={fill:C.estimate,font:{color:C.blue}};set('Cash flow','L'+r,'No house schedule supplied as of 15-Oct-26');});
row('Cash flow',21,'Cash flow before financing');fill('Cash flow',21,c=>`=IF(COUNT(${c}12:${c}19)=8,${c}10+${c}12-SUM(${c}13:${c}18)+${c}19,"n.a.")`);
row('Cash flow',23,'Beginning cash');fill('Cash flow',23,(c,i)=>i?`=IF(ISNUMBER(${cols[i-1]}27),${cols[i-1]}27,"n.a.")`:'="n.a."');sheets['Cash flow'].getRange('E23').clear({applyTo:'contents'});sheets['Cash flow'].getRange('E23').format={fill:C.estimate,font:{color:C.blue}};
for(const[r,l]of [[24,'Equity cash raised, net of fees'],[25,'Debt proceeds, net of principal repayments'],[26,'Other financing cash flow, signed']]){row('Cash flow',r,l,Array(6).fill(null));tag('Cash flow','D'+r,'MISSING');sheets['Cash flow'].getRange(`E${r}:J${r}`).format={fill:C.estimate,font:{color:C.blue}};}
row('Cash flow',27,'Ending cash before incremental funding');fill('Cash flow',27,c=>`=IF(AND(ISNUMBER(${c}21),COUNT(${c}23:${c}26)=4),${c}21+SUM(${c}23:${c}26),"n.a.")`);row('Cash flow',28,'Minimum additional funding to reach zero cash');fill('Cash flow',28,c=>`=IF(ISNUMBER(${c}27),MAX(0,-${c}27),"n.a.")`);row('Cash flow',30,'Missing cash-conversion inputs');fill('Cash flow',30,c=>`=8-COUNT(${c}12:${c}19)`,'0');for(const r of [21,27,28])total('Cash flow',r);
note('Cash flow',33,'Do not treat vendor capex, funding announcements, or multi-year commitments as Anthropic cash paid.');
note('Cash flow',34,'Noncash addbacks require evidence they were deducted above. Avoid adding depreciation or SBC twice.');
note('Cash flow',35,'Working capital excludes compute prepayments shown separately. Lease payments must not duplicate operating costs.');
note('Cash flow',36,'Negative ending cash shows a funding need. No automatic debt or equity plug is inserted.');

// Main investment view.
note('Summary',3,'House projections as of 15-Oct-2026. USD million unless noted. Reconstructed economics, with explicit accounting gaps.');
set('Summary','C6','25% annual cloud share is the base. The source ARR tracker uses 20%. Cash-flow inputs remain incomplete.');sheets.Summary.getRange('C6').format.font={color:'#9C2727',bold:true};
for(const[r,l,or]of [[10,'Gross revenue',10],[11,'Revenue growth',11],[13,'Net economic revenue',20],[14,'Inference compute cost',23],[15,'Gross profit after revenue share',24],[16,'Gross profit / gross revenue',25],[18,'Training compute cost',28],[19,'Other operating costs',30],[21,'Modeled operating surplus',31],[22,'Operating surplus / gross revenue',32]]){row('Summary',r,l);fill('Summary',r,c=>`='Operating'!${c}${or}`,[11,16,22].includes(r)?pct:money);}
row('Summary',24,'Cash flow before financing');fill('Summary',24,c=>`='Cash flow'!${c}21`,money);row('Summary',25,'Average compute GW-year equivalent');fill('Summary',25,c=>`='Compute'!${c}25`);for(const r of[10,13,15,21,24])total('Summary',r);
row('Summary',26,'Revenue / inference GW');fill('Summary',26,c=>`='Compute'!${c}27/1000`,'$0.0;($0.0);"-"');
row('Summary',27,'Compute cost / avg direct GW');fill('Summary',27,c=>`=IF(ISNUMBER('Compute'!${c}30),'Compute'!${c}30/1000,"n.a.")`,'$0.0;($0.0);"-"');
for(const r of[26,27]){set('Summary','D'+r,'bn/GW/yr');ratio('Summary',r);}
set('Summary','E9','Model history');sheets.Summary.getRange('F9:J9').values=[Array(5).fill('Forecast')];sheets.Summary.getRange('E9:J9').format.font={color:C.gray,italic:true};
note('Summary',28,'House economics: growth slows as training and residual other costs rise. Review the cost-share assumptions.');
note('Summary',29,'The surplus is not GAAP EBIT or FCF. The cash bridge requires taxes, noncash costs, capex and working capital.');
note('Summary',30,'Use Drivers to change the case or test revenue, inference margin, distribution revenue share and cost composition.');
note('Summary',31,'Validation: source extraction and arithmetic checked. Accounting scope, capacity and cost calibration remain partial.');
// Chart helper (below the visible forecast) has a distinct reshaping purpose.
sheets.Summary.getRange('C51:F51').values=[['Year','Gross revenue','Net economic revenue','Operating surplus']];
cols.slice(1).forEach((c,i)=>{const r=52+i;set('Summary','C'+r,String(years[i+1]));formula('Summary','D'+r,`=${c}10`);formula('Summary','E'+r,`=${c}13`);formula('Summary','F'+r,`=${c}21`);});
const chart=sheets.Summary.charts.add('line',sheets.Summary.getRange('C51:F56'));chart.setPosition('C34','K49');chart.title='House forecast (USD billion)';chart.titleTextStyle.typeface='Arial';chart.titleTextStyle.fontSize=13;chart.legend={position:'top',textStyle:{typeface:'Arial',fontSize:10}};chart.xAxis={axisType:'textAxis',textStyle:{typeface:'Arial',fontSize:10}};chart.yAxis={numberFormatCode:'0,"bn"',numberFormatSourceLinked:false,textStyle:{typeface:'Arial',fontSize:10}};['#254A65','#759CAC','#B05D40'].forEach((color,i)=>{chart.series.items[i].line={fill:color,style:'solid',width:2};chart.series.items[i].fill=color;});

// Terminal review. Nothing elsewhere depends on this sheet.
note('Review',3,'Reconciliations are not independent validation when the house forecast was calibrated to the same disclosure.');
const checks={10:'Revenue lines less gross revenue',11:'2026 monthly bridge less annual',12:'Costs rebuilt less source: house base only',13:'Annual source less quarterly source: 2025',14:'Rebuilt surplus less source EBIT: 2025',16:'Channel shares within 0%–100%',17:'Margin and cost-share ranges valid',18:'1P cost within training / inference totals',19:'Other costs fall while revenue grows >50%',20:'Revenue-share rate less tracker: 2026',22:'Cash-conversion input coverage',23:'Underlying capacity units',24:'External cost calibration'};
for(const[r,l]of Object.entries(checks))row('Review',Number(r),l);
fill('Review',10,c=>`='Operating'!${c}16`,diff);fill('Review',11,(c,i)=>i===1?"='ARR 2026'!I22-'Operating'!F10":'="n.a."',diff);
fill('Review',12,c=>`=IF(AND('Drivers'!$E$4=1,'Drivers'!$G$4=1,'Drivers'!$J$4=0,'Drivers'!$J$5=0),'Operating'!${c}35-'Sources'!${c}17,"n.a.")`,diff);
fill('Review',13,(c,i)=>i===0?"='Sources'!E8-'Sources'!E30":'="n.a."',diff);fill('Review',14,(c,i)=>i===0?"='Operating'!E31-'Sources'!E23":'="n.a."',diff);
fill('Review',16,c=>`=IF(AND('Drivers'!${c}40>=0,'Drivers'!${c}41>=0,'Drivers'!${c}40+'Drivers'!${c}41<=1,'Drivers'!${c}34>=0,'Drivers'!${c}34<=1),"PASS","FAIL")`);
fill('Review',17,c=>`=IF(AND('Drivers'!${c}16<=1,'Drivers'!${c}28>0,'Drivers'!${c}28<=1,'Drivers'!${c}22>=0),"PASS","FAIL")`);
fill('Review',18,c=>`=IF(AND('Compute'!${c}19>=0,'Compute'!${c}20>=0),"PASS","FAIL")`);
fill('Review',19,(c,i)=>i?`=IF(AND('Operating'!${c}38<0,'Operating'!${c}11>0.5),"REVIEW","PASS")`:'="n.a."');
fill('Review',20,(c,i)=>i===1?"='Drivers'!F34-'Sources'!F19":'="n.a."',pct);fill('Review',22,c=>`=IF('Cash flow'!${c}30=0,"COMPLETE","MISSING")`);fill('Review',23,()=> '="UNVERIFIED"');fill('Review',24,()=> '="UNVERIFIED"');
set('Review','C28','Quarterly revenue benchmark');sheets.Review.getRange('E28:G28').values=[['Q1:26','Q2:26','Q3:26']];
set('Review','C29','House quarterly revenue');set('Review','C30','Press-reported comparison');set('Review','C31','Difference / comparison value');set('Review','C32','Level reconciliation, 25% tolerance');
for(let i=0;i<3;i++){const c=cols[i];formula('Review',c+'29',`='ARR 2026'!${c}22`);formula('Review',c+'30',`='Sources'!${c}46`);formula('Review',c+'31',`=${c}29/${c}30-1`);formula('Review',c+'32',`=IF(ABS(${c}31)<=0.25,"WITHIN","REVIEW")`);}sheets.Review.getRange('E31:G31').setNumberFormat(pct);
set('Review','C34','July average annualized / reported late-July');formula('Review','E34',"='ARR 2026'!K13/'Sources'!H46-1");sheets.Review.getRange('E34').setNumberFormat(pct);
note('Review',36,'Q2 comparison is a lower bound. July is a timing-mismatched reasonableness check, not exact ARR reconciliation.');
note('Review',37,'The source historical 2025 EBIT conflicts with its cost build; its 2026+ EBIT formula adds positive costs to revenue.');
note('Review',38,'These source lines are retained in Sources and excluded from the modeled profit calculation.');
note('Review',39,'Source other-cost share may overlap with distribution costs. No source accounting note resolves this risk.');
note('Review',40,'The 2027 decline in other costs requires explicit underwriting; it is inherited from the 90% compute-cost share.');
note('Review',42,'Skeptic verdict: PARTIAL. Source figures and arithmetic verified; costs, accounting basis and cash flow remain unresolved.');
note('Review',44,'Source comments also conflict: Anthropic!A71 (24-Jul) says 20%; ARR Tracker!B48 (09-Oct) says 25%.');
note('Review',45,'The stored formulas use annual 25% and tracker 20%. Neither rate is verified against a contract.');
note('Review',46,'ARR Tracker!R51/U51/X51 comments cite the same quarterly disclosures: these are in-sample reconciliations.');
note('Review',47,nativeValidation?.status==='PASS'?'Excel 16 read-only verification passed: base case, scenarios, both native tables, and blank/zero cash inputs.':'Native Excel verification is pending; calculation tests in Artifact Tool passed.');
row('Review',49,'Revenue/GW less source: base only');row('Review',50,'Compute cost/GW less source: base only');
for(const [rr,cr,sr]of[[49,27,26],[50,30,27]])fill('Review',rr,c=>`=IF(AND('Drivers'!$E$4=1,'Drivers'!$G$4=1,'Drivers'!$J$4=0,ISNUMBER('Sources'!${c}${sr})),'Compute'!${c}${cr}-'Sources'!${c}${sr},"n.a.")`,diff);
note('Review',52,'GW ratios: source reconciliation checks arithmetic only. Blank source ratios are n.a.; extensions retain the source formula.');
note('Review',53,'The source denominators differ. Average direct GW is held fixed across scenarios; inference GW is cost-derived.');
for(const n of['Review']){for(const rg of['E10:J14']){sheets[n].getRange(rg).conditionalFormats.add('cellIs',{operator:'greaterThan',formula:.01,format:{fill:C.red,font:{bold:true,color:'#9C2727'}}});sheets[n].getRange(rg).conditionalFormats.add('cellIs',{operator:'lessThan',formula:-.01,format:{fill:C.red,font:{bold:true,color:'#9C2727'}}});}for(const text of['FAIL','REVIEW','MISSING','UNVERIFIED'])sheets[n].getRange('E16:J34').conditionalFormats.add('containsText',{text,format:{fill:text==='FAIL'?C.red:C.estimate,font:{color:'#87451F'}}});}
for(const n of Object.keys(sheets))sheets[n].getRange('C8:J8').format.rowHeight=24;
sheets.Review.getRange('E10:J34').format.font.color=C.ink;
sheets.Sources.getRange('D8').format.fill=C.hard;
sheets.Sources.getRange('E28:J30').format.font.color=C.blue;
sheets.Sources.getRange('K1:P84').format.columnWidth=15;
for(const a of['F28','F29','E30'])sheets.Sources.getRange(a).format.fill=C.hard;
for(const r of[11,16,22])ratio('Summary',r);
for(const r of[16,17,18,19,28,29,30,31,34,35,36,37,40,41,44])ratio('Drivers',r);
for(const n of ['Drivers','Sources','Compute','Summary']){if(n==='Drivers'){sheets[n].getRange('E42:J42').setNumberFormat('0.00');}else if(n==='Sources'){for(const r of[20,25])sheets[n].getRange(`E${r}:J${r}`).setNumberFormat('0.00');}else if(n==='Compute'){for(const r of[10,23,24,25,29])sheets[n].getRange(`E${r}:J${r}`).setNumberFormat('0.00');}else{sheets[n].getRange('E25:J25').setNumberFormat('0.00');}}
wb.recalculate();

// Verification against an independent arithmetic implementation.
function expected(i,revMult=1,gmDelta=0,shareDelta=0,costDelta=0){const c=scols[i],r0=val(srcA,c+'3'),rev=i===0?r0:i===1?val(srcA,'P3')+val(srcA,'Q3')+val(srcA,'R3')+val(srcA,'S3')*revMult:r0*revMult;const gm=val(srcA,c+'70')+(i?gmDelta:0),train=val(srcA,c+'47'),p=val(srcA,c+'36')+(i?costDelta:0),share=.25+(i?shareDelta:0),cloud=1-val(srcA,c+'15')-val(srcA,c+'30');return rev-rev*cloud*share-(rev*(1-gm)+train)/p;}
const get=(n,a)=>sheets[n].getRange(a).values[0][0];
const assertClose=(a,b,msg)=>{if(typeof a!=='number'||Math.abs(a-b)>Math.max(.0001,Math.abs(b)*1e-9))throw Error(msg+': '+a+' vs '+b);};
cols.forEach((c,i)=>assertClose(get('Operating',c+'31'),expected(i),'Base '+c));
cols.forEach((c,i)=>{const sc=scols[i],sourceRevGW=val(srcA,sc+'8'),sourceCostGW=val(srcA,sc+'34');if(sourceRevGW!==null)assertClose(get('Compute',c+'27'),sourceRevGW,'Source revenue/GW '+c);if(sourceCostGW!==null)assertClose(get('Compute',c+'30'),sourceCostGW,'Source cost/GW '+c);assertClose(get('Compute',c+'30'),val(srcA,sc+'35')/val(srcA,sc+'85'),'Compute cost/direct GW '+c);assertClose(get('Summary',c+'26'),get('Compute',c+'27')/1000,'Summary revenue/GW '+c);assertClose(get('Summary',c+'27'),get('Compute',c+'30')/1000,'Summary cost/GW '+c);});
assertClose(get('ARR 2026','I22'),val(srcA,'AB3'),'Annual ARR bridge');
for(const [cell,x,y]of[['G55',.8,-.1],['I57',1,0],['K59',1.2,.1]])assertClose(get('Drivers',cell),expected(5,x,y),'Sensitivity 1 '+cell);
for(const [cell,x,y]of[['G65',-.05,-.1],['I67',0,0],['K69',.05,.1]])assertClose(get('Drivers',cell),expected(5,1,0,x,y),'Sensitivity 2 '+cell);
const houseHistory=get('Operating','E31');set('Drivers','E4',2);if(get('Operating','G31')===expected(2))throw Error('Case selector did not update');assertClose(get('Operating','E31'),houseHistory,'History fixed');set('Drivers','E4',1);
set('Drivers','J35',.3);assertClose(get('Operating','J31'),expected(5,1,0,.05),'Later-year input');formula('Drivers','J35',"='Sources'!J18");
// A blank unselected scenario must not affect the valid selected case.
sheets.Drivers.getRange('J36').clear({applyTo:'contents'});assertClose(get('Operating','J31'),expected(5),'Unselected blank ignored');set('Drivers','E4',2);if(get('Drivers','J34')!=='n.a.')throw Error('Selected missing driver hidden');set('Drivers','E4',1);formula('Drivers','J36','=J35');
if(get('Drivers','G59')!=='n.a.')throw Error('Infeasible sensitivity not flagged');
// Blank cash inputs stay n.a.; explicit zeros unlock just the cash-conversion calculation.
if(get('Cash flow','J21')!=='n.a.')throw Error('Missing cash inputs became numbers');sheets['Cash flow'].getRange('J12:J19').values=Array(8).fill([0]);assertClose(get('Cash flow','J21'),get('Operating','J31'),'Explicit zero cash adjustments');sheets['Cash flow'].getRange('J12:J19').clear({applyTo:'contents'});
wb.recalculate();
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},summary:'Final formula error scan'});
await fs.writeFile(path.join(dir,'formula_scan.jsonl'),errors.ndjson);
console.log(errors.ndjson);
const out={asof:'2026-10-15',source_sha256:src.sha256,years,outputs:{},sensitivity:{revenue_margin:sheets.Drivers.getRange('F54:K59').values,share_cost:sheets.Drivers.getRange('F64:K69').values},verification:'Base, cases, later-year driver, native sensitivity calculations and blank/zero cash checks passed in Artifact Tool'};
out.gw_metrics={source:'Capstone / Felipe Monteiro, AI Model.xlsx, 15-Oct-2026',revenue_per_inference_GW_USDbn:sheets.Summary.getRange('E26:J26').values[0],compute_cost_per_average_direct_GW_USDbn:sheets.Summary.getRange('E27:J27').values[0],house_average_direct_GW:sheets.Compute.getRange('E29:J29').values[0],basis:'Annual gross revenue / cost-derived inference GW; annual training + inference cost / fixed house average direct GW. Existing source ratios reconciled; absent years extended with same formula.'};
for(const r of [10,19,20,23,24,25,26,28,30,31,32,33,35,36,40])out.outputs[r]={label:oplabels[r],values:sheets.Operating.getRange(`E${r}:J${r}`).values[0]};
await fs.writeFile(path.join(dir,'model_results.json'),JSON.stringify(out,null,2));
console.log(JSON.stringify(out.outputs['31']));
await fs.writeFile(path.join(dir,'workbook_inspection.jsonl'),(await wb.inspect({kind:'table',range:'Operating!C8:J40',include:'values,formulas',tableMaxRows:34,tableMaxCols:8,maxChars:18000})).ndjson);
const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(path.join(outputDir,'Anthropic_Financial_Model.xlsx'));
console.log('EXPORTED '+path.join(outputDir,'Anthropic_Financial_Model.xlsx'));
const ranges={'Summary':'C2:J31','Drivers':'C2:J44','Operating':'C2:J40','ARR 2026':'C2:P29','Compute':'C2:J39','Cash flow':'C2:J36','Sources':'C2:J30','Review':'C2:J53'};
for(const[n,range]of Object.entries(ranges)){const p=await wb.render({sheetName:n,range,scale:1,format:'png'});await fs.writeFile(path.join(dir,n.replaceAll(' ','_')+'.png'),new Uint8Array(await p.arrayBuffer()));console.log('RENDERED '+n);}
const p=await wb.render({sheetName:'Summary',range:'C34:K49',scale:1,format:'png'});await fs.writeFile(path.join(dir,'chart.png'),new Uint8Array(await p.arrayBuffer()));
for(const[n,range,file]of[['Drivers','C52:K73','sensitivity.png'],['Sources','C34:P49','source_monthly.png'],['Sources','C52:P84','source_register.png']]){const p=await wb.render({sheetName:n,range,scale:1,format:'png'});await fs.writeFile(path.join(dir,file),new Uint8Array(await p.arrayBuffer()));}
