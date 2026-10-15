const fs=require('fs'),path=require('path'),assert=require('assert');
const {chromium}=require('C:/Users/Felipe.monteiro/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const root=process.cwd(),dir=path.join(root,'_wiki/_data/ramp-ai-index/ui-qa'),url='http://ds-cap-33:8080/wiki/_dashboards/ramp-ai-index.html';
 const before=fs.readFileSync(path.join(dir,'before.html'),'utf8'),after=fs.readFileSync(path.join(root,'_wiki/_dashboards/ramp-ai-index.html'),'utf8');
 const extract=(s,tag)=>[...s.replace(/<script\b[^>]*>[\s\S]*?<\/script>/g,'').matchAll(new RegExp('<'+tag+'\\b[^>]*>[\\s\\S]*?<\\/'+tag+'>','g'))].map(m=>m[0]);
 assert.deepEqual(extract(after,'svg'),extract(before,'svg'),'Chart geometry or annotations changed');
 assert.deepEqual(extract(after,'table'),extract(before,'table'),'Original data tables changed');
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const page=await browser.newPage({viewport:{width:1440,height:1050}}),errors=[],result={verifiedAt:new Date().toISOString()};page.on('pageerror',e=>errors.push(e.message));
 try{
 await page.setContent(before);const original=await page.evaluate(()=>JSON.stringify(CHARTS));
 const response=await page.goto(url);assert.equal(response.status(),200);await page.waitForSelector('.ramp-panel');
 assert.equal(await page.evaluate(()=>JSON.stringify(CHARTS)),original,'Chart observations changed');
 assert.equal(await page.locator('.tile').count(),6);assert.equal(await page.locator('.ramp-panel').count(),12);assert.equal(await page.locator('.ramp-panel:visible').count(),1);assert(await page.locator('#adoption').isVisible());
 assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
 assert.equal(await page.locator('body').evaluate(e=>getComputedStyle(e).backgroundColor),'rgb(11, 16, 24)');
 const snap=await page.locator('.snapshot').evaluateAll(es=>es.map(e=>({id:e.dataset.chart,rows:[...e.querySelectorAll('tbody tr')].map(r=>[...r.cells].map(c=>c.textContent.trim()))})));
 const data=JSON.parse(original);const fv=v=>Number.isFinite(v)?v.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})+'%':'—';
 for(const s of snap){const c=data[s.id],n=c.dates.length-1;for(let i=0;i<c.rows.length;i++){assert.equal(s.rows[i][0],c.rows[i].n);assert.equal(s.rows[i][1],fv(c.rows[i].v[n]));assert.equal(s.rows[i][2],fv(c.rows[i].v[n-1]));const d=Number((c.rows[i].v[n]-c.rows[i].v[n-1]).toFixed(2));const text=(d>0?'+':d<0?'−':'')+Math.abs(d).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});assert.equal(s.rows[i][3],text);}}
 await page.screenshot({path:path.join(dir,'dark-adoption.png'),fullPage:true});
 for(const group of ['models','spending','tokens','sources','adoption']){await page.locator('.ramp-tabs a[data-group="'+group+'"]').click();assert.equal(await page.locator('.ramp-panel:visible').count(),1);assert.equal(await page.locator('.ramp-panel:visible').getAttribute('data-group'),group);}
 for(const id of ['vendor','sshare','prov','ladder','vintage','launch','cross','spend','segments','tokens','basis']){await page.goto(url+'#'+id);assert(await page.locator('#'+id).isVisible());assert.equal(await page.locator('.ramp-panel:visible').count(),1);}
 await page.goto(url+'#vendor');await page.locator('#vendor .tv summary').click();assert(await page.locator('#vendor .tv table').isVisible());
 await page.locator('#vendor .ramp-context summary').click();assert(await page.locator('#vendor .ramp-context p.sub').isVisible());
 await page.screenshot({path:path.join(dir,'dark-vendor.png'),fullPage:true});
 await page.goto(url+'#spend');await page.locator('a[href="#spend-restatement"]').click();assert(await page.locator('#spend-restatement').evaluate(e=>e.open));
 await page.goto(url+'#tokens');await page.screenshot({path:path.join(dir,'dark-tokens.png'),fullPage:true});
 await page.goto(url+'#adoption');const chart=page.locator('#adoption svg.chart').first();await chart.focus();await page.keyboard.press('End');assert(await page.locator('#tt').isVisible());assert((await page.locator('#tt').innerText()).includes('Sep-26'));await page.keyboard.press('Escape');assert(!(await page.locator('#tt').isVisible()));
 await page.locator('#ramp-theme').click();await page.reload();assert.equal(await page.locator('html').getAttribute('data-theme'),'light');await page.screenshot({path:path.join(dir,'light-adoption.png'),fullPage:true});
 await page.locator('#ramp-theme').click();await page.reload();assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
 for(const width of [390,768,1024]){await page.setViewportSize({width,height:844});for(const id of ['adoption','vendor','launch','cross','spend','segments','tokens','basis']){await page.goto(url+'#'+id);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Overflow '+width+' '+id);}if(width===390){await page.goto(url+'#adoption');await page.screenshot({path:path.join(dir,'dark-mobile.png'),fullPage:true});assert(await page.locator('#adoption .chart-wrap').first().evaluate(e=>e.scrollWidth>e.clientWidth&&Math.abs(e.scrollLeft-(e.scrollWidth-e.clientWidth))<2));assert.equal(await page.locator('.skip-link').evaluate(e=>getComputedStyle(e).opacity),'0');assert(await page.locator('#adoption .snapshot').first().evaluate(e=>e.scrollWidth<=e.clientWidth+1));}}
 const blocked=await browser.newPage();await blocked.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError');}}));await blocked.goto(url);await blocked.locator('#ramp-theme').click();assert.equal(await blocked.locator('html').getAttribute('data-theme'),'light');await blocked.close();
 assert.deepEqual(errors,[]);Object.assign(result,{data:'all original chart series, chart geometry, annotations and data tables unchanged',snapshotTables:snap.length,navigation:'12 panels, 5 views, deep links, context/table expansion and restatement link passed',theme:'both themes, persistence and blocked storage passed',layout:'390 / 768 / 1024 / 1440 px passed',tooltips:'keyboard values and dismissal passed',errors});fs.writeFileSync(path.join(dir,'results.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
