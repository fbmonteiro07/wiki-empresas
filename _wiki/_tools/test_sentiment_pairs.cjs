const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const D=JSON.parse(fs.readFileSync(path.join(__dirname,'../_data/sentiment_research/dashboard.json'),'utf8'));
assert.ok(D.pair_tests,'Build pair tests first');
const frozen=JSON.parse(fs.readFileSync(path.join(__dirname,'../_data/sentiment_research/pair_frozen_rules.json'),'utf8'));
assert.equal(frozen.selection_hash,D.pair_tests.selection_hash);assert.deepEqual(frozen.selections,D.pair_tests.selections);
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-7,`${a} != ${b}`);
let assessed=0;
for(const [t,c]of Object.entries(D.pair_tests.companies))for(const e of c.experiments){
 const pairs=e.selection.pairs;
 for(let i=1;i<pairs.length;i++)assert.ok(pairs[i-1].train.net>=pairs[i].train.net-1e-7);
 if(!e.test)continue;assessed++;
 assert.deepEqual(e.selection.winner.rule,pairs[0].rule);
 const test=e.ledger.filter(r=>r.period==='validation'&&r.eligible);
 assert.equal(test.length,e.test.n);assert.ok(test.every(r=>r.signal.startsWith('2026')&&r.exit<=c.cutoff));
 assert.ok(e.ledger.filter(r=>r.period==='train').every(r=>r.exit<'2026-01-01'));
 const mean=a=>a.length?a.reduce((s,x)=>s+x,0)/a.length:null;
 if(test.length){
  close(mean(test.map(r=>r.pair_net)),e.test.net);
  close(mean(test.map(r=>r.pair_net-r.single_net)),e.contrasts[0].increment);
  for(let j=0;j<2;j++)close(mean(test.map(r=>r.pair_net-r.component_positions[j]*((1+r.return)*.999/1.001-1))),e.contrasts[j+1].increment);
 }
 if(e.horizon===20){assert.ok(e.test.n<=10);assert.equal(e.passes,false);assert.ok(e.contrasts.every(c=>!c.support&&c.bootstrap.ci===null));}
 assert.ok(e.contrasts.every(c=>c.p_holm>=c.p_raw-1e-7));
}
let exported;const ctx=vm.createContext({D,state:{ticker:'NVDA',date:D.meta.signal_asof},csv:(name,rows)=>exported={name,rows}});
vm.runInContext(fs.readFileSync(path.join(__dirname,'sentiment_pair_ui.js'),'utf8'),ctx);
ctx.rankFeatures=D.indicator_rankings.features;
vm.runInContext('pairExport(D.pair_tests.companies.NVDA)',ctx);assert.equal(exported.rows.length,5);for(const f of ['cutoff','cost_per_side','reference_days','default_peers'])assert.ok(exported.rows[0].includes(f));assert.ok(exported.rows.every(r=>r.length===exported.rows[0].length));
vm.runInContext('pairLedger(D.pair_tests.companies.NVDA)',ctx);assert.ok(exported.rows.length>100);assert.ok(exported.rows.every(r=>r.length===exported.rows[0].length));
for(const field of ['cost_per_side','reference_days','default_peers','selection_hash'])assert.ok(exported.rows[0].includes(field));
// Historical replay must render no stored future result, even though payload contains it.
const target={innerHTML:''};ctx.$=()=>target;ctx.state.date='2025-06-13';vm.runInContext('renderPairs()',ctx);
assert.ok(target.innerHTML.includes('hidden during historical replay'));assert.ok(!target.innerHTML.includes('2026 pair'));
console.log(`Pair integration passed:384 training orders,${assessed} frozen validation ledgers and all component increments;20d inference suppression;freeze file,exports,replay.`);
