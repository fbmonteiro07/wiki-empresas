import fs from 'node:fs/promises';
import {Presentation,PresentationFile} from 'file:///C:/Users/Felipe.monteiro/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
import {pathToFileURL} from 'node:url';
const root='E:/Wiki Felipe empresas';
const skill='C:/Users/Felipe.monteiro/.codex/plugins/cache/openai-primary-runtime/presentations/26.1020.11618/skills/presentations';
const build=root+'/_wiki/_data/semianalysis-pptx-build';
const p=Presentation.create({slideSize:{width:1664,height:944}}),s=p.slides.add();
s.images.add({blob:await fs.readFile('C:/Users/Felipe.monteiro/.codex/generated_images/01a1c0d9-58b9-7f71-9177-0d2e778e7e52/exec-79cd456f-0b7e-464e-9fa9-2c525cc2e89c.png'),contentType:'image/png',position:{left:0,top:0,width:1664,height:944}});
s.shapes.add({geometry:'rect',position:{left:0,top:110,width:1664,height:834},fill:'#FFFFFF',line:{fill:'none',width:0}});
function txt(text,x,y,w,h,size=24,color='#002532',bold=false){const q=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});q.text=text;q.text.style={fontFamily:'Arial',fontSize:size,color,bold};return q;}
txt('Annual net capacity additions, excluding China*',56,150,1020,50,28,'#002532',true);
s.charts.add('bar',{position:{left:54,top:223,width:1010,height:506},categories:['2024','2025','2026E','2027E','2028E*'],series:[{name:'US',values:[6.2,10.2,18.1,38,62.2],fill:'#002532'},{name:'RoW excluding China',categories:["2024","2025","2026E","2027E"],values:[3.6,5.5,6.9,13.2],fill:'#F39A23'}],barOptions:{direction:'column',grouping:'stacked',overlap:100,gapWidth:55},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:19,fill:'#222222'}},chartFill:'#FFFFFF',plotAreaFill:'#FFFFFF',xAxis:{textStyle:{fontSize:20,fill:'#555555'},majorGridlines:null},yAxis:{min:0,max:70,majorUnit:10,numberFormatCode:'0" GW"',textStyle:{fontSize:18,fill:'#555555'},majorGridlines:{fill:'#DCE1E6',width:1,style:'solid'}},dataLabels:{showValue:true,position:'center',numberFormatCode:'0.0',textStyle:{fontSize:23,fill:'#FFFFFF',bold:true}},displayBlanksAs:'gap'});
txt('US only',918,235,125,32,20,'#002532',true);
txt('*2028: US only; RoW unavailable. IT vs facility basis not explicit.',280,749,800,30,18,'#333333');
txt('2027E · ex-China IT capacity',1133,180,490,45,28,'#002532',true);
txt('51.2 GW',1133,232,480,72,56,'#002532',true);
txt('38.0 US + 13.2 RoW',1133,309,480,40,28);
txt('74.2% US share',1133,354,480,45,33,'#BC7413',true);
txt('2028E · US net additions',1133,462,490,44,28,'#002532',true);
txt('62.2 GW',1133,513,480,72,56,'#BC7413',true);
txt('SemiAnalysis · 1 Nov 2026',1133,590,490,38,26);
txt('Most projects have not started construction.\nIT vs facility basis not explicit; RoW not verified.',1133,636,490,72,21,'#586777');
txt('China sits outside this series. Capacity ready for equipment does not establish actual chip deployment.',56,800,1500,44,22,'#586777');
txt('2024–27 chart: SemiAnalysis / Ontiveros, Knuhtsen & Patel, 19 Oct 2026. 2024–25: historical model estimates. 2025 components sum to 15.7 vs 15.8 reported total.',56,875,1515,23,13,'#334455');
txt('2028 US: SemiAnalysis / Barkin, Ma, Knuhtsen, Ontiveros & Patel, 1 Nov 2026. Separate source vintage and scope.',56,898,1515,23,13,'#334455');
const ms=p.slides.add();
ms.images.add({blob:await fs.readFile('C:/Users/Felipe.monteiro/.codex/generated_images/01a1c0d9-58b9-7f71-9177-0d2e778e7e52/exec-79cd456f-0b7e-464e-9fa9-2c525cc2e89c.png'),contentType:'image/png',position:{left:0,top:0,width:1664,height:944}});
ms.shapes.add({geometry:'rect',position:{left:0,top:110,width:1664,height:834},fill:'#FFFFFF',line:{fill:'none',width:0}});
ms.shapes.add({geometry:'rect',position:{left:0,top:0,width:1500,height:110},fill:'#002532',line:{fill:'none',width:0}});
function mt(text,x,y,w,h,size=24,color='#002532',bold=false){const q=ms.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});q.text=text;q.text.style={fontFamily:'Arial',fontSize:size,color,bold};return q;}
mt('Morgan Stanley shifts 4.9 GW from 2028 to 2029',56,25,1430,64,36,'#FFFFFF',true);
mt('Annual change in global data center capacity',56,150,1020,50,28,'#002532',true);
ms.charts.add('bar',{position:{left:54,top:223,width:1010,height:506},categories:['2026E','2027E','2028E','2029E','2030E'],series:[{name:'Global GW added y/y',values:[28,39.9,43.3,47,44.8],fill:'#002532'},{name:'Shifted from 2028',values:[0,0,0,4.9,0],fill:'#F39A23',dataLabelOverrides:[0,1,2,4].map(idx=>({idx,showValue:false}))}],barOptions:{direction:'column',grouping:'stacked',overlap:100,gapWidth:55},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:19,fill:'#222222'}},chartFill:'#FFFFFF',plotAreaFill:'#FFFFFF',xAxis:{textStyle:{fontSize:20,fill:'#555555'},majorGridlines:null},yAxis:{min:0,max:75,majorUnit:15,numberFormatCode:'0" GW"',textStyle:{fontSize:18,fill:'#555555'},majorGridlines:{fill:'#DCE1E6',width:1,style:'solid'}},dataLabels:{showValue:true,position:'center',numberFormatCode:'0.0',textStyle:{fontSize:23,fill:'#FFFFFF',bold:true}}});
mt('4.9 GW deferred to 2029',456,215,400,36,20,'#BC7413',true);
mt('2028E',1133,180,490,45,28,'#002532',true);
mt('43.3 GW',1133,232,480,72,56,'#002532',true);
mt('Global annual additions',1133,309,480,40,28);
mt('4.9 GW shifted to 2029',1133,354,490,45,30,'#BC7413',true);
mt('2029E',1133,462,490,44,28,'#002532',true);
mt('51.9 GW',1133,513,480,72,56,'#BC7413',true);
mt('Includes the 4.9 GW shift',1133,590,490,38,26);
mt('2030E unchanged at 44.8 GW',1133,652,490,48,24,'#586777');
mt('Morgan Stanley forecasts a timing shift into 2029, with the 2030 buildout unchanged.',56,800,1500,44,22,'#586777');
mt('Source: Morgan Stanley Research, DC team, Exhibit 5. Report date not provided. Source and team confirmed by the user.',56,875,1515,23,14,'#334455');
mt('Scope: global capacity additions. IT vs facility basis is not specified in the supplied exhibit. Source totals shown to one decimal.',56,901,1515,23,14,'#334455');
await fs.writeFile(build+'/preview-ms.png',new Uint8Array(await (await p.export({slide:ms,format:'png',scale:1})).arrayBuffer()));
const candidatePath=build+'/candidate.pptx';await(await PresentationFile.exportPptx(p)).save(candidatePath);
const {finalizePresentation}=await import(pathToFileURL(skill+'/container_tools/artifact_tool_utils.mjs').href);
console.log(await finalizePresentation({workspaceDir:root,candidatePath,finalPath:root+'/_wiki/_dashboards/exports/SemiAnalysis_and_Morgan_Stanley.pptx',pythonExecutable:'C:/Users/Felipe.monteiro/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:skill+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:skill+'/container_tools/inspect_presentation_layout_geometry.py',materializeLiteralChartWorkbooks:true,explicitTotalSlideCount:2,requiredNativeChartOwnerSlides:[1,2],requiredNativeTableOwnerSlides:[],verifyArtifactToolImport:true,receiptPath:build+'/validation-ms.json'}));




