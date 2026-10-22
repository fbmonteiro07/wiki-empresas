import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const dataDir='//capsrv01/Users$/felipe.monteiro/Wiki Felipe empresas/_wiki/_data/research/MU_DCF_2026-10-22';
const source=JSON.parse(await fs.readFile(dataDir+'/mu.json','utf8'));
const w=Workbook.create();
const s=w.worksheets.add('DCF Memory');
const stub=w.worksheets.add('MU Model');
const cv=c=>{let n=0; for(const x of c)n=n*26+x.charCodeAt(0)-64;return n;};
const col=n=>{let r='';for(;n;n=Math.floor((n-1)/26))r=String.fromCharCode(65+(n-1)%26)+r;return r;};
const matrix=Array.from({length:361},()=>Array(52).fill(null));
for(const [a,c] of Object.entries(source.sheets['MU Model'].cells)){const m=a.match(/([A-Z]+)(\d+)/);matrix[+m[2]-1][cv(m[1])-1]=c.v;}
stub.getRange('A1:AZ361').values=matrix;
const navy='#1F4E78',blue='#0000FF',green='#008000',amber='#FFF2CC',light='#E7EEF5';
const num='#,##0;(#,##0);"-"',pct='0.0%;(0.0%);"-"',price='$0.00;($0.00);"-"';
s.showGridLines=false;s.tabColor=navy;
s.getRange('A1:AH185').format.font={name:'Arial',size:10,color:'#000000'};
s.getRange('A1:B185').format.columnWidth=2;
s.getRange('C1:C185').format.columnWidth=49;
s.getRange('D1:AH185').format.columnWidth=13;
s.getRange('A1:AH185').format.rowHeight=19;
s.getRange('D1:AH185').setNumberFormat(num);
s.getRange('C1:AH185').format.verticalAlignment='center';
const val=(a,v)=>s.getRange(a).values=[[v]];
const formula=(a,f)=>{s.getRange(a).formulas=[[f]];s.getRange(a).format.font.color=f.includes("'MU Model'!")?green:'#000000';};
const label=(r,t)=>val('C'+r,t);
const band=(r,t,end='AH')=>{label(r,t);s.getRange(`C${r}:${end}${r}`).format={fill:navy,font:{bold:true,color:'#FFFFFF'}};};
const total=(r)=>{s.getRange(`C${r}:AH${r}`).format.font.bold=true;s.getRange(`C${r}:AH${r}`).format.borders={top:{style:'thin',color:navy}};};
val('C2','Micron DCF');s.getRange('C2').format.font={name:'Arial',size:16,bold:true,color:navy};
val('C3','USD millions except per-share amounts. Valuation date: 31-Dec-2026. Calendar years follow the source model quarter convention.');
s.getRange('C3').format.font={size:10,italic:true,color:'#606060'};
label(5,'Value per share (USD)');formula('D5','=D60');s.getRange('D5').setNumberFormat(price);
label(6,'Reference price in source model (USD)');formula('D6','=D61');s.getRange('D6').setNumberFormat(price);
label(7,'Value / reference price - 1');formula('D7','=D62');s.getRange('D7').setNumberFormat(pct);
for(const [range,a,text,cell,f,fmt] of [
 ['G5:I5','G5','Enterprise value','J5','=D54',num],['G6:I6','G6','Net cash after deposits','J6','=SUM(D55:D57)',num],
 ['L5:N5','L5','PV of explicit cash flows','O5','=D52',num],['L6:N6','L6','Terminal value / EV','O6','=D63',pct]]){
 s.mergeCells(range);val(a,text);formula(cell,f);s.getRange(cell).setNumberFormat(fmt);
}
s.getRange('C5:D7').format.font.bold=true;s.getRange('D5').format.font.size=16;s.getRange('C5:O7').format.rowHeight=23;
val('C9','Linked earnings through 2028 and revenue through 2030. Later years fade to editable, historical cycle assumptions.');
val('C10','The source price is a model input, not a live quote. WACC and perpetual growth use the TSM reference as a starting convention.');
s.getRange('C9:C10').format.font={color:'#805B10',italic:true};
label(12,'Calendar year');
for(let y=2025;y<=2054;y++)val(col(y-2021)+'12',y);
val('AH12','Perpetuity');s.getRange('C12:AH12').format={fill:navy,font:{bold:true,color:'#FFFFFF'},horizontalAlignment:'center'};
s.getRange('D12:AG12').setNumberFormat('0');
for(const [r,t] of Object.entries({14:'DRAM ex-HBM revenue',15:'HBM revenue',16:'NAND revenue',17:'Other revenue',18:'Revenue',19:'Revenue growth',21:'EBITDA (GAAP EBIT + D&A)',22:'EBITDA margin',24:'Depreciation & amortization',25:'EBIT (GAAP basis)',26:'EBIT margin',27:'Operating tax rate',28:'Cash operating taxes',29:'NOPAT',31:'Opening PP&E, model roll-forward',32:'Gross capital expenditures',33:'Depreciation & amortization',34:'Closing PP&E, model roll-forward',35:'Capex / revenue',36:'D&A / opening PP&E',38:'Operating working capital',39:'Operating working capital / revenue',40:'Increase in operating working capital',42:'NOPAT',43:'Add: D&A',44:'Less: gross capex',45:'Less: working capital investment',46:'Unlevered free cash flow',47:'FCFF margin',48:'Discount period (year-end)',49:'Present value of FCFF'}))label(+r,t);
const histCols=['AD','AE','AF','AG'];
const mapSeg=[52,41,68,85];
for(let y=2025;y<=2054;y++){
 const c=col(y-2021),p=col(y-2022),src=['AD','AE','AF','AG','AH','AI'][y-2025];
 for(let i=0;i<4;i++){
  const r=14+i;
  if(y<=2030)formula(c+r,`='MU Model'!${src}${mapSeg[i]}`);
  else formula(c+r,`=${p}${r}*(1+${c}19)`);
 }
 formula(c+'18',`=SUM(${c}14:${c}17)`);
 if(y>2025){
  if(y<=2030)formula(c+'19',`=${c}18/${p}18-1`);
  else formula(c+'19',`=$I$19+($D$72-$I$19)*MIN(1,(${c}$12-2030)/($D$73-2030))`);
 }
 if(y<=2028){
  formula(c+'21',`=SUM('MU Model'!${src}139,'MU Model'!${src}88)`);
  formula(c+'22',`=${c}21/${c}18`);
  formula(c+'24',`='MU Model'!${src}88`);
  formula(c+'27',`='MU Model'!${src}147`);
  formula(c+'32',`='MU Model'!${src}169`);
  const qc=['G','K','O','S'][y-2025];
  formula(c+'38',`=SUM('MU Model'!${qc}358:${qc}359)-'MU Model'!${qc}360`);
  formula(c+'39',`=${c}38/${c}18`);
 }else{
  formula(c+'22',`=$G$22+($D$74-$G$22)*MIN(1,(${c}$12-2028)/($D$73-2028))`);
  formula(c+'21',`=${c}18*${c}22`);
  formula(c+'36',`=$G$36+($D$76-$G$36)*MIN(1,(${c}$12-2028)/($D$73-2028))`);
  formula(c+'24',`=${c}31*${c}36`);
  formula(c+'27','=$D$78');
  formula(c+'35',`=$G$35+($D$75-$G$35)*MIN(1,(${c}$12-2028)/($D$73-2028))`);
  formula(c+'32',`=${c}18*${c}35`);
  formula(c+'39',`=$G$39+($D$77-$G$39)*MIN(1,(${c}$12-2028)/($D$73-2028))`);
  formula(c+'38',`=${c}18*${c}39`);
 }
 formula(c+'25',`=${c}21-${c}24`);formula(c+'26',`=${c}25/${c}18`);
 formula(c+'28',`=-MAX(0,${c}25)*${c}27`);formula(c+'29',`=SUM(${c}25,${c}28)`);
 if(y===2025){formula(c+'34',"='MU Model'!G274");val(c+'31','n.a.');val(c+'36','n.a.');}
 else if(y===2026){formula(c+'31',`=${p}34`);formula(c+'34',"='MU Model'!J274+'MU Model'!K156-'MU Model'!K88");formula(c+'36',`=${c}24/${c}31`);}
 else{formula(c+'31',`=${p}34`);formula(c+'34',`=SUM(${c}31:${c}32)-${c}33`);if(y<=2028)formula(c+'36',`=${c}24/${c}31`);}
 formula(c+'33',`=${c}24`);if(y<=2028)formula(c+'35',`=${c}32/${c}18`);
 if(y>2025)formula(c+'40',`=${c}38-${p}38`);
 if(y>=2027){
  formula(c+'42',`=${c}29`);formula(c+'43',`=${c}24`);formula(c+'44',`=-${c}32`);formula(c+'45',`=-${c}40`);
  formula(c+'46',`=SUM(${c}42:${c}45)`);formula(c+'47',`=${c}46/${c}18`);
  formula(c+'48',`=${c}$12-$D$80`);formula(c+'49',`=${c}46/(1+$D$71)^${c}48`);
 }
}
for(let r=14;r<=17;r++)formula('AH'+r,`=AG${r}*(1+$D$72)`);
formula('AH18','=SUM(AH14:AH17)');formula('AH19','=$D$72');formula('AH22','=$D$74');formula('AH21','=AH18*AH22');
formula('AH35','=$D$75');formula('AH32','=AH18*AH35');formula('AH36','=$D$76');
formula('AH31','=AH32/($D$76+$D$72)');formula('AH24','=AH31*AH36');formula('AH33','=AH24');formula('AH34','=SUM(AH31:AH32)-AH33');
formula('AH25','=AH21-AH24');formula('AH26','=AH25/AH18');formula('AH27','=$D$78');formula('AH28','=-MAX(0,AH25)*AH27');formula('AH29','=SUM(AH25,AH28)');
formula('AH39','=$D$77');formula('AH38','=AH18*AH39');formula('AH40','=AH38-AH38/(1+$D$72)');
formula('AH42','=AH29');formula('AH43','=AH24');formula('AH44','=-AH32');formula('AH45','=-AH40');formula('AH46','=SUM(AH42:AH45)');formula('AH47','=AH46/AH18');
for(const r of [19,22,26,27,35,36,39,47]){s.getRange(`D${r}:AH${r}`).setNumberFormat(pct);s.getRange(`C${r}:AH${r}`).format.font.italic=true;}
for(const r of [18,21,25,29,34,38,46,49])total(r);
s.getRange('D14:E49').format.fill='#F3F3F3';s.getRange('H21:AH49').format.fill='#FFFBF1';
s.getRange('F46:AH46').format.fill=light;
band(51,'Enterprise to equity bridge','O');
const bridge={52:['PV of FCFF, 2027-2054','=SUM(F49:AG49)'],53:['PV of terminal value','=IF(AND(COUNT(D71:D78)=8,D71>D72,D73>2030),AH46/(D71-D72)/(1+D71)^(D79-D80),NA())'],54:['Enterprise value','=SUM(D52:D53)'],55:['Add: cash and investments, CY2026E',"='MU Model'!K188"],56:['Less: total debt, CY2026E',"=-'MU Model'!K191"],57:['Less: refundable customer deposits',"=-'MU Model'!K189"],58:['Equity value','=SUM(D54:D57)'],59:['Diluted shares at valuation baseline (m)',"='MU Model'!K150"],60:['Value per share (USD)','=D58/D59'],61:['Reference price in source model (USD)',"='MU Model'!K175"],62:['Value / reference price - 1','=D60/D61-1'],63:['Terminal value / enterprise value','=D53/D54']};
for(const [r,[t,f]] of Object.entries(bridge)){label(+r,t);formula('D'+r,f);}
for(const r of [54,58,60]){s.getRange(`C${r}:D${r}`).format.font.bold=true;s.getRange(`C${r}:D${r}`).format.borders={top:{style:'thin',color:navy}};}
s.getRange('D60:D61').setNumberFormat(price);s.getRange('D62:D63').setNumberFormat(pct);
val('F55','HARD: exact model input. Cash includes short- and long-term investments.');
val('F57','HARD: model liability balance, deducted once at face value. No second repayment deduction in FCFF.');
val('F59','HARD: FQ1 FY27E (K150), inherited from FQ4 FY26 J150; baseline diluted-share proxy. Future buybacks excluded.');
val('F61','HARD: saved model assumption of $1,050, not a current market observation.');
band(70,'Valuation and extension assumptions','O');
const inputs={71:['Discount rate (WACC convention)',0.10,'ESTIMATE','10.0% from TSM DCF!C81 (source labels it Ke); applied to FCFF here. Not a Micron CAPM estimate.'],72:['Perpetual revenue and cash-flow growth',0.025,'ESTIMATE','2.5% from TSM DCF!C83. Same growth for revenue, PP&E and working capital in perpetuity.'],73:['Year normalization is complete',2035,'ESTIMATE','Author assumption, 2026-10-22. EBITDA/capex/WC fade from 2028; revenue growth from 2030.'],74:['Normalized EBITDA / revenue','=N147/N146','PARTIAL','FY2016-25 revenue-weighted EBITDA margin. Historical anchor used as a forward cycle assumption.'],75:['Normalized gross capex / revenue','=N149/N146','PARTIAL','FY2016-25 gross capex / revenue. No additional future incentives assumed.'],76:['Normalized D&A / opening PP&E','=SUM(E148:M148)/SUM(D151:L151)','PARTIAL','FY2017-25 D&A / FY2016-24 closing PP&E. D&A calculated from the asset roll-forward.'],77:['Normalized operating WC / revenue','=N150/N146','PARTIAL','FY2016-25 (receivables + inventory - AP/accruals) / revenue. Excludes cash, debt and deposits.'],78:['Long-run operating tax rate',"='MU Model'!AG147",'HARD','Exact CY2028 source-model assumption, 15.5%; future tax outcome is uncertain.'],79:['Last explicit forecast year',2054,'HARD','Matches the latest TSM DCF explicit horizon.'],80:['Valuation year-end',2026,'HARD','Matches TSM DCF valuation date, 31-Dec-2026. Source Micron CY columns use Nov-ended fiscal quarters.']};
inputs[78][2]='PARTIAL';
inputs[78][3]='CY2028 source-model tax assumption of 15.5%, extended into later years; no new tax forecast.';
inputs[79][1]='=AG12';
for(const [r,[t,v,tag,note]] of Object.entries(inputs)){
 label(+r,t);if(typeof v==='string'&&v.startsWith('='))formula('D'+r,v);else val('D'+r,v);
 val('E'+r,tag);val('F'+r,note);s.getRange('D'+r).format.fill=amber;s.getRange('D'+r).format.font.color=blue;
 s.getRange('E'+r).format.font.color=tag==='HARD'?green:tag==='PARTIAL'?'#0066AA':'#9C6500';
}
s.getRange('D79:D80').format.fill='#FFFFFF';s.getRange('D79:D80').format.font.color='#000000';
s.getRange('D71:D72').setNumberFormat(pct);s.getRange('D74:D78').setNumberFormat(pct);s.getRange('D73').setNumberFormat('0');s.getRange('D79:D80').setNumberFormat('0');
s.getRange('D73').dataValidation={rule:{type:'whole',operator:'between',formula1:2031,formula2:2045}};
for(const a of ['D71','D74:D78'])s.getRange(a).dataValidation={rule:{type:'decimal',operator:'between',formula1:0,formula2:1}};
s.getRange('D72').dataValidation={rule:{type:'decimal',operator:'between',formula1:0,formula2:0.08}};
val('C82','Blue values are editable. PARTIAL = historical calibration used forward. HARD = exact source value, including source forecasts.');
val('C83','SBC remains an expense through GAAP EBIT. Future buybacks do not lower the DCF share denominator.');
const addTable=(row,title,rowInput,colInput,rowValues,colValues)=>{
 band(row,title,'I');formula(`D${row+2}`,'=$D$60');s.getRange(`D${row+2}`).setNumberFormat(';;;');
 rowValues.forEach((f,i)=>typeof f==='number'?val(`${col(5+i)}${row+2}`,f):formula(`${col(5+i)}${row+2}`,f));
 colValues.forEach((f,i)=>typeof f==='number'?val(`D${row+3+i}`,f):formula(`D${row+3+i}`,f));
 const range=`D${row+2}:${col(4+rowValues.length)}${row+2+colValues.length}`;
 s.dataTables.add(range,{rowInput,columnInput:colInput});
 s.getRange(`E${row+2}:${col(4+rowValues.length)}${row+2}`).setNumberFormat(pct);
 s.getRange(`D${row+3}:D${row+2+colValues.length}`).setNumberFormat(colInput==='D73'?'0':pct);
 s.getRange(`E${row+3}:${col(4+rowValues.length)}${row+2+colValues.length}`).setNumberFormat(price);
 s.getRange(range).conditionalFormats.add('colorScale',{colors:['#FCE4D6','#FFFFFF','#DDEBF7'],thresholds:['min','50%','max']});
};
addTable(86,'Value / share: WACC down; perpetual growth across','D72','D71',[.015,.02,.025,.03,.035],[.08,.09,.10,.11,.12]);
addTable(97,'Value / share: EBITDA margin down; capex ratio across','D75','D74',[-.05,-.025,0,.025,.05].map(x=>`=$N$153+(${x})`),[-.10,-.05,0,.05,.10].map(x=>`=$N$152+(${x})`));
addTable(108,'Value / share: normalization year down; WACC across','D71','D73',[.09,.10,.11],[2033,2035,2037]);
val('K88','Live Excel What-If Data Tables, linked to the same DCF.');
val('K89','WACC/g and year axes are fixed editable scenarios. Margin/capex axes use historical anchors N152/N153.');
val('K90','Axes do not follow the tested input cells. This prevents Excel from changing the scenario grid during calculation.');
val('K91','Changing D71:D78 recalculates the model. Excel calculation must include data tables.');
val('K99','Historical normalization is not a prediction that the memory industry returns to its old economics.');
val('K100','This table makes the valuation effect of a structural margin or capital-intensity change explicit.');
band(118,'Checks and limitations','O');
const checks=[
 [120,'2027 revenue vs source control','=F18',"='MU Model'!AF9",'=D120-E120','=IF(ABS(F120)<0.01,"OK","REVIEW")'],
 [121,'2028 EBIT vs source control','=G25',"='MU Model'!AG139",'=D121-E121','=IF(ABS(F121)<0.01,"OK","REVIEW")'],
 [122,'CY2026 net cash after deposits','=SUM(D55:D57)',"='MU Model'!K193",'=D122-E122','=IF(ABS(F122)<0.01,"OK","REVIEW")'],
 [123,'FY2026 cash and investments components',"='MU Model'!J188","=SUM('MU Model'!J265:J266)+'MU Model'!J275",'=D123-E123','=IF(ABS(F123)<0.01,"OK","REVIEW")'],
 [124,'WACC exceeds perpetual growth','=D71','=D72','=D124-E124','=IF(F124>0,"OK","INVALID")'],
 [125,'Terminal FCFF / last FCFF - 1','=AH46/AG46-1','=D72','=D125-E125','=IF(ABS(F125)<0.25,"OK","REVIEW")'],
 [126,'Normalized EBITDA vs historical range','=D74','=MIN(D152:M152)','=MAX(D152:M152)','=IF(AND(D126>=E126,D126<=F126),"IN RANGE","OUTSIDE")'],
 [127,'Normalized capex vs historical range','=D75','=MIN(D153:M153)','=MAX(D153:M153)','=IF(AND(D127>=E127,D127<=F127),"IN RANGE","OUTSIDE")'],
 [128,'Opening and closing PP&E remain positive','=MIN(E31:AH31,D34:AH34)',0,'=D128-E128','=IF(D128>=0,"OK","REVIEW")'],
 [129,'Steady-state terminal ROIC','=AH29/(AH31+AH38/(1+D72))','=D71','=D129-E129','=IF(D129<E129,"BELOW WACC","ABOVE WACC")'],
 [130,'FY2026 EBITDA vs history (holdout)',"=('MU Model'!AV139+'MU Model'!AV88)/'MU Model'!AV9",'=D74','=D130-E130','=IF(ABS(F130)>0.25,"REGIME GAP","IN RANGE")'],
 [131,'FY2026 capex ratio vs history (holdout)',"='MU Model'!AV169/'MU Model'!AV9",'=D75','=D131-E131','=IF(ABS(D131/E131-1)>0.25,"REGIME GAP","IN RANGE")']
];
for(const [r,t,a,b,c,d] of checks){label(r,t);[a,b,c,d].forEach((f,i)=>typeof f==='number'?val(col(4+i)+r,f):formula(col(4+i)+r,f));}
s.getRange('D120:F123').setNumberFormat('0.00');s.getRange('D124:F127').setNumberFormat(pct);s.getRange('D129:F131').setNumberFormat(pct);
s.getRange('G120:G131').conditionalFormats.add('containsText',{text:'REVIEW',format:{fill:'#FCE4D6',font:{color:'#9C0006',bold:true}}});
s.getRange('G120:G131').conditionalFormats.add('containsText',{text:'REGIME GAP',format:{fill:amber,font:{color:'#9C6500',bold:true}}});
s.getRange('G129').conditionalFormats.add('containsText',{text:'BELOW WACC',format:{fill:amber,font:{color:'#9C6500',bold:true}}});
val('I120','Source ties verify extraction and formulas, not forecast accuracy.');val('I125','Terminal D&A is normalized to capex / (depreciation rate + g), with a PP&E roll-forward in explicit years.');
val('I129','ROIC is a diagnostic, not a constraint on terminal value. E is WACC; F is the spread.');
val('I130','FY2026 is held out of the FY2016-25 fit. A regime gap flags the economic importance of the historical normalization.');
val('C134','No independent external validation of the source forecasts. Valuation is an editable model, not an adopted Capstone price target.');
val('C135','Existing D&A!W51:Y51 #DIV/0! cells are retained from the original workbook and are not DCF inputs.');
val('C136','Working capital covers receivables, inventories and AP/accruals only. Other operating balances and future grants are omitted.');
val('C137','CY2026 PP&E starts with fiscal-year actual J274 plus FQ1 FY27 capex minus D&A; later PP&E excludes disposals and other adjustments.');
band(142,'Historical calibration: FY2016-FY2025','N');
label(144,'Fiscal year');for(let i=0;i<10;i++)val(col(4+i)+'144',2016+i);val('N144','Sum / ratio');
s.getRange('D144:M144').setNumberFormat('0');
for(const [r,t] of Object.entries({146:'Revenue',147:'EBITDA (GAAP EBIT + D&A)',148:'Depreciation & amortization',149:'Gross capex',150:'Receivables + inventories - AP/accruals',151:'Closing PP&E',152:'EBITDA / revenue',153:'Gross capex / revenue',154:'Operating WC / revenue',155:'D&A / opening PP&E'}))label(+r,t);
for(let i=0;i<10;i++){
 const c=col(4+i),sc=col(38+i),pc=col(3+i);
 formula(c+'146',`='MU Model'!${sc}9`);formula(c+'147',`=SUM('MU Model'!${sc}139,'MU Model'!${sc}88)`);
 formula(c+'148',`='MU Model'!${sc}88`);formula(c+'149',`='MU Model'!${sc}169`);
 formula(c+'150',`=SUM('MU Model'!${sc}267:${sc}268)-'MU Model'!${sc}284`);formula(c+'151',`='MU Model'!${sc}274`);
 formula(c+'152',`=${c}147/${c}146`);formula(c+'153',`=${c}149/${c}146`);formula(c+'154',`=${c}150/${c}146`);
 if(i>0)formula(c+'155',`=${c}148/${pc}151`);
}
for(let r=146;r<=150;r++)formula('N'+r,`=SUM(D${r}:M${r})`);
for(const [r,f] of [[152,'=N147/N146'],[153,'=N149/N146'],[154,'=N150/N146'],[155,'=SUM(E148:M148)/SUM(D151:L151)']])formula('N'+r,f);
s.getRange('D152:N155').setNumberFormat(pct);s.getRange('C152:N155').format.font.italic=true;
val('C158','HARD source inputs: Capstone / Modelo Micron.xlsx, saved 13-Oct-2026, MU Model!AL:AU (fiscal history).');
val('C159','Linked forecast: same workbook, MU Model!AD:AI (CY revenue), AD:AG (earnings/capex), G/K/O/S (quarter-end WC).');
val('C160','The source model attributes historical results to Micron and certain D&A/bit estimates to UBS. Original labels and notes are preserved.');
val('C161','Valuation convention: Capstone / Modelo Felipe TSM 3Q26 DCF versão final.xlsm, saved 21-Oct-2026, DCF!C81/C83/C92:C107.');
val('C162','Also reviewed Template DCF TSM.xlsx (27-Aug-2026). The newer TSM cash-flow / enterprise-to-equity layout governs this sheet.');
val('C164','Arithmetic: revenue → EBITDA → less D&A → EBIT → less operating taxes → NOPAT + D&A − capex − change in WC → FCFF.');
val('C165','Discount 2027-2054 FCFF at year-end. Terminal FCFF / (WACC − g) is discounted 28 years to 31-Dec-2026.');
val('C166','Add valuation-date cash and investments; deduct debt and customer deposits; divide by baseline diluted shares.');
val('C167','Source snapshot read 22-Oct-2026. The five original worksheets, formulas, links and native features are retained in the delivered copy.');
val('C168','No live market refresh was performed. Source-model forecasts and historical data were not revised.');
val('C170','HARD = copied source figure, not a claim that a forecast is actual. PARTIAL = calibrated extension. ESTIMATE = judgment.');
s.freezePanes.freezeRows(12);s.freezePanes.freezeColumns(3);
w.recalculate();
const inspect=await w.inspect({kind:'table',range:'DCF Memory!C52:G80',include:'values,formulas',tableMaxRows:30,tableMaxCols:5});
await fs.writeFile('inspect.ndjson',inspect.ndjson);
const errors=await w.inspect({kind:'match',range:'DCF Memory!C1:AH170',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!',options:{useRegex:true,maxResults:40},summary:'DCF formula scan'});
console.log(errors.ndjson);
console.log('KEY',JSON.stringify({value:s.getRange('D60').values,ev:s.getRange('D54').values,inputs:s.getRange('D71:D80').values,checks:s.getRange('C120:G131').values}));
const baseValue=s.getRange('D60').values[0][0];
const tests=[];
for(const [cell,replacement,restore] of [['D71',.11,.10],['D72',0,.025],['D73',2033,2035]]){
 val(cell,replacement);w.recalculate();tests.push({cell,replacement,value:s.getRange('D60').values[0][0]});val(cell,restore);
}
w.recalculate();
tests.push({restored:s.getRange('D60').values[0][0],base:baseValue});
await fs.writeFile('tests.json',JSON.stringify(tests,null,2));
await fs.writeFile('dcf_values.json',JSON.stringify(s.getRange('A1:AH170').values));
for(const [range,name] of [['C2:O29','dcf_top'],['C31:L49','dcf_cashflow'],['C51:H80','dcf_bridge'],['C86:J114','dcf_sensitivities'],['C142:N155','dcf_calibration']]){
 const b=await w.render({sheetName:'DCF Memory',range,scale:1.25,format:'png'});await fs.writeFile(name+'.png',new Uint8Array(await b.arrayBuffer()));
}
const out=await SpreadsheetFile.exportXlsx(w);await out.save('dcf_generated.xlsx');
console.log('Exported dcf_generated.xlsx',JSON.stringify(tests));
