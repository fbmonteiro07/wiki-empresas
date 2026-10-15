const fs=require('fs'),path=require('path'),assert=require('assert');
const {chromium}=require('C:/Users/Felipe.monteiro/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const dir=path.join(process.cwd(),'_wiki/_data/dashboard-hub-ui-qa');
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const errors=[],results={verifiedAt:new Date().toISOString(),mode:process.argv.includes('--live')?'both published pages':'wiki live / Capstone preview'};
 const page=await browser.newPage({viewport:{width:1440,height:1050}});page.on('pageerror',e=>errors.push(e.message));
 try{
 for(const name of ['wiki','capstone']){
  const wiki=name==='wiki',selector=wiki?'.hub-card':'a.card',theme=wiki?'.or-theme':'#theme-toggle';
  await page.setContent(fs.readFileSync(path.join(dir,name+'-hub-before.html'),'utf8'));
  const before=await page.locator(selector).evaluateAll(es=>es.map(e=>e.getAttribute('href')));
  if(wiki)await page.goto('http://ds-cap-33:8080/wiki/_dashboards/index.html');
  else if(process.argv.includes('--live'))await page.goto('http://ds-cap-33:8080/dashboards/');
  else{await page.route('http://capstone-preview.test/**',r=>r.fulfill({status:200,contentType:'text/html',body:fs.readFileSync(path.join(dir,'capstone-preview.html'),'utf8')}));await page.goto('http://capstone-preview.test/');}
  await page.waitForSelector(selector);
  assert.deepEqual(before.sort(),(await page.locator(selector).evaluateAll(es=>es.map(e=>e.getAttribute('href')))).sort());
  assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
  assert.equal(await page.locator('body').evaluate(e=>getComputedStyle(e).backgroundColor),'rgb(11, 16, 24)');
  assert(await page.locator('#q').evaluate(e=>e.getBoundingClientRect().bottom<innerHeight));
  await page.locator('#q').fill(wiki?'credit monitor':'comp sheet');assert((await page.locator(selector+':visible').count())>0);
  await page.locator('#q').fill('zzzz_no_match_874');assert.equal(await page.locator(selector+':visible').count(),0);assert(await page.locator('#no-results').isVisible());
  await page.locator('#clear-search').click();
  if(wiki){await page.locator('#q').fill('snapshot');assert(await page.locator('#archive').evaluate(e=>e.open));await page.locator('#clear-search').click();assert(!(await page.locator('#archive').evaluate(e=>e.open)));}
  else{assert.equal(await page.locator('a[data-internal-process]').count(),2);assert.equal(await page.locator('.market-section').count(),4);}
  await page.locator('#show-details').click();assert.equal(await page.locator('#show-details').getAttribute('aria-pressed'),'true');await page.locator('#show-details').click();
  await page.locator('#q').blur();await page.keyboard.press('/');assert(await page.locator('#q').evaluate(e=>e===document.activeElement));
  await page.locator('#q').fill('foo');await page.keyboard.press('Escape');assert.equal(await page.locator('#q').inputValue(),'');await page.locator('#q').blur();
  await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(dir,name+'-dark-desktop.png')});
  await page.locator(theme).click();await page.reload();await page.waitForSelector(selector);assert.equal(await page.locator('html').getAttribute('data-theme'),'light');
  await page.screenshot({path:path.join(dir,name+'-light-desktop.png')});
  await page.locator(theme).click();await page.reload();await page.waitForSelector(selector);assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
  for(const width of [390,768,1024]){await page.setViewportSize({width,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),name+' overflow '+width);if(width===390){await page.screenshot({path:path.join(dir,name+'-dark-mobile.png')});await page.locator('#show-details').click();assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await page.locator('#show-details').click();}}
  await page.setViewportSize({width:1440,height:1050});results[name]={links:before.length,checks:'links, themes, persistence, search, details, keyboard, responsive layout'};
 }
 assert.deepEqual(errors,[]);results.errors=errors;fs.writeFileSync(path.join(dir,'results.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});

