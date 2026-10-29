const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const D=JSON.parse(fs.readFileSync(path.join(__dirname,'../_data/sentiment_research/dashboard.json'),'utf8'));
assert.ok(D.indicator_rankings,'Build raw-indicator rankings first');
const ctx=vm.createContext({D,state:{ticker:'NVDA',date:D.meta.signal_asof,key:'tes'}});
for(const file of ['sentiment_company_ui.js','sentiment_relative_ui.js','sentiment_ranking_ui.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,file),'utf8'),ctx);
const run=s=>JSON.parse(JSON.stringify(vm.runInContext(s,ctx)));
function close(a,b,label){
 if(typeof b==='number'){assert.ok(Math.abs(a-b)<1e-7,label+': '+a+' != '+b);return;}
 if(b===null||typeof b!=='object'){assert.equal(a,b,label);return;}
 if(Array.isArray(b))assert.equal(a.length,b.length,label);
 for(const[k,v]of Object.entries(b))close(a[k],v,label+'/'+k);
}
for(const t of ['NVDA','AMD','AAPL','MU']){
 const p=D.indicator_rankings.companies[t];
 close(run(`rankCalculate('${t}','all','364',comparisonPeers('${t}'),'absolute','${p.cutoff}')`),p,t);
}
for(const [t,p]of Object.entries(D.indicator_rankings.companies))for(const h of [5,20])for(const axis of ['own','peer']){
 const rows=p.rows.filter(r=>r.axis===axis&&r.horizon===h).sort((a,b)=>Math.abs(b.spread||0)-Math.abs(a.spread||0));
 assert.equal(new Set(rows.map(r=>r.n)).size,1,t+' common n');
 assert.equal(new Set(rows.map(r=>r.sample_first)).size,1,t+' common first');
 assert.equal(new Set(rows.map(r=>r.sample_last)).size,1,t+' common last');
 assert.ok(rows.every(r=>r.p_holm>=r.p_raw&&r.p_raw>0));
 rows.forEach((r,i)=>assert.equal(r.rank,r.spread==null?null:i+1));
}
const replay=run("rankCalculate('NVDA','2024','182',['AMD','AVGO'],'relative','2024-11-01')");
for(const r of replay.rows){assert.deepEqual(Object.keys(r.years),['2024']);assert.equal(r.temporal.train_n,0);assert.ok(!r.checks.prior_direction);assert.ok(!r.sample_last||r.sample_last<='2024-11-01');}
assert.ok(run("rankRawEvents('NVDA',20,'364',['AMD'],'2025-06-12')").every(e=>e.exit<='2025-06-12'));
let exported;ctx.csv=(name,rows)=>exported={name,rows};
vm.runInContext("rankExport(D.indicator_rankings.companies.NVDA)",ctx);
assert.equal(exported.rows.length,17);
for(const key of ['return_basis','history_window','selected_peers','period','cutoff'])assert.ok(exported.rows[0].includes(key));
assert.ok(exported.rows.every(r=>r.length===exported.rows[0].length));
vm.runInContext("rankLedger(D.indicator_rankings.companies.NVDA)",ctx);
assert.equal(exported.rows.length,1377);assert.ok(exported.rows.every(r=>r.length===exported.rows[0].length));
for(const key of ['return_basis','history_window','selected_peers','period','information_cutoff','vendor_observed_days7'])assert.ok(exported.rows[0].includes(key));
assert.ok(exported.rows.slice(1).every(r=>r[exported.rows[0].indexOf('vendor_observed_days7')]>=4));
console.log('Raw rankings passed: 64 Python/JS results including bootstrap p, Holm and MC bounds, all96 matched samples/ranks, replay and custom peers.');
