const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const D=JSON.parse(fs.readFileSync(path.join(__dirname,'../_data/sentiment_research/dashboard.json'),'utf8'));
assert.ok(D.relative_summary,'Build the relative backtest first.');
const ctx=vm.createContext({D,state:{ticker:'NVDA',date:D.meta.signal_asof,key:'tes'}});
for(const file of ['sentiment_company_ui.js','sentiment_relative_ui.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,file),'utf8'),ctx);
const run=s=>JSON.parse(JSON.stringify(vm.runInContext(s,ctx)));
function close(actual,expected,label){
 if(typeof expected==='number'){assert.ok(Math.abs(actual-expected)<1e-7,label+': '+actual+' != '+expected);return;}
 if(expected===null){assert.equal(actual,null,label);return;}
 if(Array.isArray(expected)){assert.equal(actual.length,expected.length,label);expected.forEach((v,i)=>close(actual[i],v,label+'/'+i));return;}
 for(const [k,v]of Object.entries(expected))close(actual[k],v,label+'/'+k);
}
for(const h of ['5','20'])for(const year of ['2024','2025','2026','all'])for(const axis of ['own','peer']){
 const expr=`rbtSummary(rbtEvents('NVDA','${year}','${h}','tes','364',comparisonPeers('NVDA'),'9999-12-31'),'${axis}','${h}','absolute')`;
 close(run(expr),D.relative_summary.audit_sample_nvda[h][year][axis],[h,year,axis].join('/'));
}
const replay=run("rbtEvents('NVDA','all','20','tes','364',comparisonPeers('NVDA'),'2025-06-12')");
assert.ok(replay.length>0&&replay.every(e=>e.exit<='2025-06-12'));
assert.deepEqual(run("[null,0,.2999,.3,.6999,.7,1].map(rbtBand)"),[null,0,0,1,1,2,2]);
assert.equal(run("rbtSummary([{own:.1,return:.1,qqq_return:.03},{own:.9,return:.3,qqq_return:.05},{own:null,return:9}], 'own','5','absolute').baseline"),.2);
assert.ok(Math.abs(run("rbtSummary([{own:.1,return:.1,qqq_return:.03},{own:.9,return:.3,qqq_return:.05}], 'own','5','relative').spread")-.18)<1e-12);
// A missing company row must remain in the fixed master schedule.
const before=run("rbtEvents('NVDA','2026','5','tes','364',comparisonPeers('NVDA'),'9999-12-31')");
const removed=D.company_studies.NVDA['2026']['5'].splice(3,1)[0];
const after=run("rbtEvents('NVDA','2026','5','tes','364',comparisonPeers('NVDA'),'9999-12-31')");
assert.equal(before.length,after.length);
assert.equal(after.find(e=>e.signal===removed.signal).return,null);
D.company_studies.NVDA['2026']['5'].splice(3,0,removed);
for(const h of ['5','20'])for(const y of ['2024','2025','2026'])for(const a of ['own','peer','peer_min3']){
 const p=D.relative_summary.aggregate.tes[h][y][a];
 const b=run(`(()=>{const es=D.relative_summary.aggregate.tes['${h}']['${y}']['${a}'].events;return es.filter(e=>finiteReading(e.spread)).length>=20?rbtBootstrap(es,'${h}',ss=>rbtMean(ss.map(e=>e.spread).filter(finiteReading))):{ci:null,draws:0,valid_draws:0};})()`);
 close(b,{ci:p.ci,draws:p.draws,valid_draws:p.valid_draws},'cluster/'+h+'/'+y+'/'+a);
}
console.log('Relative tests passed: 16 company summaries and bootstrap sensitivities match Python; 18 clustered checks match; replay, baseline, exact bands and missing schedule verified.');
