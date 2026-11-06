export async function build({presentation,input}) {
 const n=input.slide;
 const s=n===0?presentation.slides.getItem(0):presentation.slides.add({width:1280,height:720});
 s.setViewportSize(1280,720);s.shapes.deleteAll();s.background.fill='#FFFFFF';
 presentation.theme.defaultFont='Segoe UI';
 const text=(t,x,y,w,h,size=22,color='#002231',bold=false)=>{const q=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});q.text=t;q.text.style={fontFamily:'Segoe UI',fontSize:size,color,bold};return q;};
 const title=['US leads SemiAnalysis’s 2027 buildout','Morgan Stanley models a larger RoW contribution','The 2027 delivery forecasts remain far apart'][n];
 s.shapes.add({geometry:'rect',position:{left:0,top:0,width:1280,height:84.48},fill:'#002231',line:{fill:'none',width:0}});
 text(title,36.5,17.3,1095,58,29,'#FFFFFF',true);
 s.images.add({path:'E:/Wiki Felipe empresas/_wiki/_data/gw-deck-build/image1.png',position:{left:1164.5,top:4.8,width:106.56,height:76.8},fit:'contain'});
 text(String(n+1),1210,680,32,20,10,'#6B7480');
 const table=(values,x,y,w,h,widths)=>{const t=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,columnWidths:widths,values});t.borders.assign({fill:'#E3E6EA',width:1});for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){const a=t.getCell(r,c);a.fill=r===0?'#002231':r%2?'#F2F5F7':'#FFFFFF';a.text.style={fontFamily:'Segoe UI',fontSize:r===0?18:23,color:r===0?'#FFFFFF':'#002231',bold:r===0||c===0};}return t;};
 if(n===0){
 text('Annual net additions of IT capacity, excluding China',38,109,1120,36,24,'#002231',true);
 s.charts.add('bar',{position:{left:38,top:168,width:790,height:410},categories:['2024','2025','2026E','2027E'],series:[{name:'US',values:[6.2,10.2,18.1,38],fill:'#002231'},{name:'RoW excluding China',values:[3.6,5.5,6.9,13.2],fill:'#ED9D2D'}],barOptions:{direction:'column',grouping:'stacked',gapWidth:110,overlap:100},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:17}},dataLabels:{showValue:true,position:'center',textStyle:{fontSize:19,fill:'#FFFFFF',bold:true},numberFormatCode:'0.0'},xAxis:{textStyle:{fontSize:18}},yAxis:{min:0,max:60,majorUnit:10,numberFormatCode:'0" GW"',textStyle:{fontSize:15},majorGridlines:{fill:'#E3E6EA',width:1}},chartFill:'#FFFFFF',plotAreaFill:'#FFFFFF'});
 text('51.2 GW',880,175,340,74,48,'#002231',true);
 text('2027E total excluding China',882,252,340,60,22);
 text('38.0 US + 13.2 RoW',882,323,340,44,23,'#002231',true);
 text('74.2% US share',882,388,340,46,28,'#B57519',true);
 text('Scheduled additions include planned and under-construction buildings.',882,457,337,100,20,'#596674');
 text('China sits outside this series. Capacity ready for equipment does not establish actual chip deployment.',38,601,1180,52,19,'#596674');
 text('Source: SemiAnalysis / Ontiveros, Knuhtsen & Patel, 19 Oct 2026. 2024–25: historical model estimates. 2025 components sum to 15.7 vs 15.6 reported total.',38,665,1125,36,11,'#6B7480');
 s.speakerNotes.text='SemiAnalysis October model. https://newsletter.semianalysis.com/p/datacenters-2027-the-year-of-acceleration . Original chart: https://substack-post-media.s3.amazonaws.com/public/images/7d297773-64db-4139-964b-8a2ec8f7a982_2700x1440.png . HARD means directly sourced model figures, not verified delivery. US share=38/51.2=74.21875%. 2025 source total15.6 versus regional sum15.7 is rounding. Design reference and original logo: Capstone Recap AI 3Q26.pptx.';
 }
 if(n===1){
 text('Annual energised additions, facility-power GW, global scope',38,109,1170,36,24,'#002231',true);
 table([['Year','US, derived','RoW, residual','Global, published'],['2026E','13','10','23'],['2027E','25','26','51'],['2028E','27','41','68'],['2029E','28','61','89']],38,177,770,338,[155,190,210,215]);
 text('2027 bridge',866,178,345,44,27,'#002231',true);
 text('US: 30 − 5 = 25 GW',866,247,345,52,25,'#002231',true);
 text('US demand less US shortfall',866,301,345,48,18,'#596674');
 text('RoW: 51 − 25 = 26 GW',866,371,355,54,25,'#B57519',true);
 text('Global energised less US energised',866,429,345,68,18,'#596674');
 text('RoW is the residual in a model that subtracts US shortages only. It is not an independent regional delivery forecast.',38,552,1180,66,22,'#002231',true);
 text('Facility-power GW and global scope differ from SemiAnalysis’s IT GW and ex-China scope.',38,624,1180,32,18,'#596674');
 text('Source: Morgan Stanley / Byrd, Moore & Nowak, 5 Oct 2026, Exhibits 1 and 5. US and RoW columns: Capstone arithmetic from MS inputs.',38,672,1125,30,11,'#6B7480');
 s.speakerNotes.text='Morgan Stanley, What Does the Power Shortfall Mean for Semis?, 2026-10-05. E:/Wiki Felipe empresas/relatórios bons/GLOBAL_20261005_0401.html . Ex1 p004.jpg: incremental global demand32/56/86/124 less US shortfall9/5/18/35 gives global energised23/51/68/89. Ex5 p007.jpg annual table: US demand22/30/45/63. Derived US13/25/27/28. Derived RoW10/26/41/61. RoW is residual with no separate non-US shortage. Do not use55% compute share to allocate energised capacity. Figures rounded as published.';
 }
 if(n===2){
 text('2027E annual IT-capacity additions',38,109,1170,36,24,'#002231',true);
 table([['Source / vintage','Geography','IT GW'],['SemiAnalysis / 19 Oct','US','38.0'],['Bernstein / 1–2 Oct','US','19.5*'],['Jefferies / 9 Oct','North America','18.0']],38,170,1204,232,[635,355,214]);
 text('China remains outside the comparable total',38,443,575,40,24,'#002231',true);
 text('Patel’s 24 Oct remarks give 7–8 GW for 2027, with a different US/global framing and no explicit IT basis. Keep that estimate separate.',38,495,575,112,21,'#596674');
 text('2028 RoW still lacks an absolute figure',672,443,568,40,24,'#002231',true);
 text('SemiAnalysis gives 62.2 GW of US net additions on 1 Nov. Its October chart shows a 35% ex-US share, but a different vintage prevents a clean RoW bridge.',672,495,568,112,21,'#596674');
 text('*Bernstein: archived annual-additions series. Its stock changes imply 19.7 GW for 2027. This discrepancy remains unresolved.',38,623,1180,35,16,'#596674');
 text('Sources: SemiAnalysis / Ontiveros et al., 19 Oct; Patel, CASPA, 24 Oct; Barkin et al., 1 Nov 2026. Bernstein / Rezaei et al., 1–2 Oct. Jefferies / Petersen et al., 9 Oct.',38,672,1125,32,11,'#6B7480');
 s.speakerNotes.text='Source dates all2026. SA chart direct38US IT2027. Bernstein secondary archive extraction: E:/Wiki Felipe empresas/_wiki/themes/ai-datacenter-power.md, annual additions19.5 vs stock67.0−47.3=19.7; no reconciliation. Jefferies primary Exhibit1 p2 in relatórios bons/_assets/7913a58c-eb91-4769-8994-eb43cb2104d5/p002.jpg gives18.0North America IT2027. CASPA transcript at _podcasts/adhoc/2026-10-24 - Semiconductor Industry Outlook Panel CASPA 2026 CEO Summit.md 12:56–14:00. SA Nov1 https://newsletter.semianalysis.com/p/the-datacenter-backlash-goes-bipartisan US2028 62.2GW, basis not restated. 35% from October geographic chart global exChina. Do not combine vintages. Full research report: E:/Wiki Felipe empresas/_wiki/_meta/gw-us-row-breakdown-2026-11-06.md.';
 }
 await presentation.render({slide:n});
 return {slides:presentation.slides.items.length};
}
