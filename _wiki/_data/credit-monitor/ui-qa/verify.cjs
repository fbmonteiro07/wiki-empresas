
const fs=require('fs'),path=require('path'),assert=require('assert'),crypto=require('crypto');
const {chromium}=require('C:/Users/Felipe.monteiro/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const root=process.cwd(),folder=path.join(root,'_wiki/_data/credit-monitor/ui-qa');
 fs.mkdirSync(folder,{recursive:true});
 const html=fs.readFileSync(path.join(root,'_wiki/_dashboards/credit-monitor.html'),'utf8');
 const live='http://ds-cap-33:8080/wiki/_dashboards/credit-monitor.html';
 const results={verifiedAt:new Date().toISOString()};
 const actual=JSON.parse(html.match(/<script id="credit-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
 try{const response=await fetch(live,{signal:AbortSignal.timeout(15000)});const body=await response.text();results.live={status:response.status,matches:body===html};}catch(e){results.live={error:e.message};}
 assert.equal(results.live.status,200);assert.equal(results.live.matches,true);
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const page=await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 try{
  await page.route('http://credit-monitor.test/**',route=>route.fulfill({status:200,contentType:'text/html',body:html}));
  await page.goto(live+'#spreads');
  await page.waitForSelector('.issuer-row');
  assert.equal(await page.locator('.issuer-row').count(),8);
  assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
  assert.equal(await page.locator('body').evaluate(e=>getComputedStyle(e).backgroundColor),'rgb(11, 16, 24)');
  await page.locator('#theme-toggle').click();
  assert.equal(await page.locator('html').getAttribute('data-theme'),'light');
  assert.equal(await page.locator('#theme-toggle').getAttribute('aria-label'),'Switch to dark theme');
  await page.reload();await page.waitForSelector('.issuer-row');
  assert.equal(await page.locator('html').getAttribute('data-theme'),'light');
  await page.screenshot({path:path.join(folder,'light-theme.png'),fullPage:true});
  await page.locator('#theme-toggle').click();await page.reload();await page.waitForSelector('.issuer-row');
  assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
  results.theme='passed: dark default, light/dark toggle, saved preference after reload';
  assert.equal(await page.locator('[data-period="1Y"]').getAttribute('aria-pressed'),'true');
  assert.equal(await page.locator('#research-view').isVisible(),false);
  assert.equal(new URL(page.url()).hash,'#monitor');
  assert.equal(await page.locator('.series-line').count(),5);
  assert((await page.locator('#feed-status').innerText()).includes('13 of 14 main instruments'));
  assert((await page.locator('#feed-status').innerText()).includes('under review'));
  assert(!(await page.locator('#feed-status').evaluate(e=>e.classList.contains('current'))));
  for(const c of actual.issuers.filter(c=>c.focus)){
   const row=page.locator('.issuer-row[data-company="'+c.id+'"]');
   const b=c.bonds.find(b=>b.id===c.main);
   assert.equal(b.date,'2026-10-14');assert.equal(b.status,'available');
   assert.equal(await row.locator('td').nth(6).locator('.quote').innerText(),b.last.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}));
   if(c.cds?.validationWarning){
    assert((await row.innerText()).includes('Under review'));
    assert.equal(await page.locator('.series-line[data-issuer="'+c.id+'"]').count(),0);
   } else if(c.cds){
    assert.equal(c.cds.date,'2026-10-14');assert.equal(c.cds.status,'available');
    assert.equal(await row.locator('td').nth(1).locator('.quote').innerText(),c.cds.last.toLocaleString('en-US',{minimumFractionDigits:1,maximumFractionDigits:1}));
    for(const [i,days] of [1,7,30].entries()){
     const shown=(await row.locator('td').nth(i+2).innerText()).trim();
     if(c.cds.changes[String(days)])assert.notEqual(shown,'\u2014');else assert.equal(shown,'\u2014');
    }
   }
  }
  assert((await page.locator('.issuer-row[data-company="CRWV"] .bond-daily').innerText()).includes('bp'));
  results.currentQuotes='5 usable CDS and 8 main bond yields match Bloomberg observations dated 2026-10-14; CRWV CDS explicitly under review; main-bond 1D yield moves visible';
  await page.screenshot({path:path.join(folder,'desktop.png'),fullPage:true});
  await page.locator('#toggle-CRWV').click();
  assert.equal(await page.locator('#detail-CRWV .bond-table tbody tr').count(),8);
  assert.equal(await page.locator('#detail-CRWV input:checked').count(),1);
  await page.locator('#detail-CRWV input[value="CRWV_9.25_2030"]').check();
  assert((await page.locator('[data-company="CRWV"] .bond-name').innerText()).includes('9.25%'));
  await page.locator('#toggle-CRWV').click();
  await page.locator('#company-search').fill('oracle');
  assert.equal(await page.locator('.issuer-row').count(),1);
  await page.locator('#company-search').fill('no such issuer');
  assert(await page.locator('#no-companies').isVisible());
  await page.locator('#company-search').fill('');
  await page.locator('[data-metric="yield"]').click();
  assert(await page.locator('#convert-control').isVisible());
  assert.equal(await page.locator('.series-line').count(),6);
  assert(await page.locator('[data-select="NBIS"]').isDisabled());
  await page.locator('#include-convertibles').check();
  assert(!(await page.locator('[data-select="NBIS"]').isDisabled()));
  assert.equal(await page.locator('.series-line').count(),8);
  await page.screenshot({path:path.join(folder,'recovered-bond-yields.png'),fullPage:true});
  await page.locator('[data-period="1M"]').click();
  assert.equal(await page.locator('[data-period="1M"]').getAttribute('aria-pressed'),'true');
  await page.locator('[data-view="research"]').click();
  assert(await page.locator('#research-view').isVisible());
  await page.locator('#ledger>summary').click();
  assert(await page.locator('#deal-search').isVisible());
  await page.screenshot({path:path.join(folder,'dark-research.png'),fullPage:true});
  assert.equal(await page.locator('#alerts #deal-search').count(),0);
  await page.locator('#deal-search').fill('no matching deal');
  assert.equal(await page.locator('#deal-table tr[data-category]:visible').count(),0);
  await page.locator('[data-view="monitor"]').click();
  await page.locator('#universe').selectOption('all');
  assert.equal(await page.locator('.issuer-row').count(),18);
  assert((await page.locator('.issuer-row[data-company="SOFTBK"] .bond-name').innerText()).includes('EUR'));
  await page.locator('[data-metric="yield"]').click();
  assert(await page.locator('[data-select="SOFTBK"]').isDisabled());
  await page.locator('#universe').selectOption('focus');
  await page.locator('[data-metric="cds"]').click();
  await page.locator('[data-period="1Y"]').click();
  await page.setViewportSize({width:390,height:844});
  await page.waitForTimeout(250);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.screenshot({path:path.join(folder,'mobile.png'),fullPage:true});
  results.realDataUI='passed: watchlist, expansion, main selection, filters, periods, research, mobile overflow';

  // Synthetic observations exist only in this isolated browser test.
  // The dashboard, source JSON files and research are never modified.
  const fixture=JSON.parse(html.match(/<script id="credit-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
  fixture.today='2026-10-14';fixture.latest='2026-10-14';fixture.feed={state:'ok'};
  const start=Date.parse('2025-10-14T00:00Z'),end=Date.parse('2026-10-14T00:00Z');
  fixture.issuers.forEach((c,ci)=>{
   [c.cds,...c.bonds].filter(Boolean).forEach((s,si)=>{
    const pts=[];for(let t=start,i=0;t<=end;t+=86400000,i++){
     if([0,6].includes(new Date(t).getUTCDay()))continue;
     const v=s.group==='cds'?(ci===0?400:55+ci*12)+(Math.sin(i/24+ci)*12+i*.09)*(ci===0?4:1):4+ci*.6+si*.05+Math.sin(i/30+ci)*.3+i*.001;
     pts.push([new Date(t).toISOString().slice(0,10),Number(v.toFixed(3))]);
    }
    s.validationWarning='';s.points=pts;s.last=pts.at(-1)[1];s.date=pts.at(-1)[0];s.status='available';s.ticker=s.candidate;s.error='';
    for(const days of [1,7,30]){const target=end-days*86400000,b=pts.filter(p=>Date.parse(p[0]+'T00:00Z')<=target).at(-1);s.changes[days]={value:(s.last-b[1])*(s.unit==='%'?100:1),start:b[0],end:s.date,unit:'bp'};}
   });
  });
  let testHtml=html.replace(/(<script id="credit-data" type="application\/json">)[\s\S]*?(<\/script>)/,(_,open,close)=>open+JSON.stringify(fixture)+close);
  testHtml=testHtml.replace('CREDIT / AI INFRASTRUCTURE','UI TEST · SYNTHETIC OBSERVATIONS');
  await page.unroute('http://credit-monitor.test/**');
  await page.route('http://credit-monitor.test/**',route=>route.fulfill({status:200,contentType:'text/html',body:testHtml}));
  await page.setViewportSize({width:1440,height:1100});
  await page.goto('http://credit-monitor.test/');
  assert.equal(await page.locator('.series-line').count(),6);
  assert.equal(await page.evaluate(()=>CreditChart.windowStart('2024-03-31','1M')),'2024-02-29');
  assert.equal(await page.evaluate(()=>CreditChart.prepare({unit:'bp',points:[['2026-01-01',20]]},'2026-09-14','2026-10-14','change')),null);
  assert.equal(await page.evaluate(()=>CreditChart.prepare({unit:'bp',points:[['2026-09-14',0],['2026-10-14',10]]},'2026-09-14','2026-10-14','change').points.at(-1)[1]),10);
  await page.locator('[data-sort="cds"]').click();
  assert.equal(await page.locator('.issuer-row').first().getAttribute('data-company'),'CRWV');
  await page.locator('[data-period="1M"]').click();
  assert((await page.locator('#chart-range').innerText()).startsWith('Sep 14, 2026'));
  await page.locator('[data-mode="change"]').click();
  const changes=await page.locator('.series-line').count();assert.equal(changes,6);
  await page.locator('[data-metric="yield"]').click();
  assert.equal(await page.locator('.series-line').count(),6);
  await page.locator('#include-convertibles').check();
  assert.equal(await page.locator('.series-line').count(),8);
  await page.locator('[data-mode="level"]').click();
  assert((await page.locator('#chart-source').innerText()).includes('%'));
  await page.locator('[data-metric="cds"]').click();
  await page.locator('[data-period="1Y"]').click();
  const svg=page.locator('#comparison-svg');await svg.focus();await page.keyboard.press('ArrowRight');
  assert(await page.locator('#chart-tooltip').isVisible());
  assert((await page.locator('#chart-tooltip').innerText()).includes('PX_LAST'));
  await page.locator('[data-metric="cds"]').focus(); // dismiss tooltip
  await page.screenshot({path:path.join(folder,'synthetic-chart-test.png'),fullPage:true});
  await page.setViewportSize({width:390,height:844});await page.waitForTimeout(250);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  assert.equal(await page.locator('.series-line').count(),6);
  await page.screenshot({path:path.join(folder,'synthetic-mobile-test.png'),fullPage:true});
  assert.deepEqual(errors,[]);
  results.fixtureUI='passed: nonempty chart, shared lookbacks, zero baseline, bp conversion, currency/convertible eligibility, sort, keyboard tooltip, resize';
  const storageBlocked=await browser.newPage({viewport:{width:1280,height:900}});
  await storageBlocked.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError');}}));
  await storageBlocked.goto(live+'#monitor');
  assert.equal(await storageBlocked.locator('html').getAttribute('data-theme'),'dark');
  await storageBlocked.locator('#theme-toggle').click();
  assert.equal(await storageBlocked.locator('html').getAttribute('data-theme'),'light');
  await storageBlocked.close();
  results.theme+='; works with browser storage disabled';
  results.consoleErrors=errors;results.screenshots=folder;
  fs.writeFileSync(path.join(folder,'results.json'),JSON.stringify(results,null,2));
  console.log(JSON.stringify(results,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
