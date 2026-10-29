// Material comparison checks: timing, missing data, ties and basket integrity.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const row = (ticker,score,raw=score) => ({ticker,scores:{tes:score},rsi14:raw});
const ctx = vm.createContext({D:{
  snapshots:{'2025-01-03':[row('A',.1)],'2026-01-02':[row('A',.2)],
    '2026-01-09':[row('A',.3)],'2026-01-16':[row('A',null)],
    '2026-02-06':[row('A',.4)],'2026-03-06':[row('A',.5),row('B',.2)],
    '2026-03-13':[row('A',.99)]},
  names:{A:{},B:{},C:{}},peer_groups:{A:{default_mode:'direct',direct:[{ticker:'B'}],sector:['B','C']}}
},state:{ticker:'A',date:'2026-03-06',key:'tes'}});
vm.runInContext(fs.readFileSync(path.join(__dirname,'sentiment_company_ui.js'),'utf8'),ctx);
const run = text => JSON.parse(JSON.stringify(vm.runInContext(text,ctx)));
assert.deepEqual(run("comparisonHistory('A',state.date,'ytd').map(x=>x[0])"),['2026-01-02','2026-01-09','2026-01-16','2026-02-06']);
assert.deepEqual(run("comparisonHistory('A',state.date,'28').map(x=>x[0])"),['2026-02-06']);
assert.equal(run("comparisonStart('2026-03-06','364')"),'2025-03-07');
assert.deepEqual(run('comparisonStats(.5,[null,undefined,NaN,Infinity,.2,.5,.5,.8])'),{n:4,median:.5,percentile:50});
assert.deepEqual(run('comparisonStats(null,[0,.5,1])'),{n:3,median:.5,percentile:null});
assert.deepEqual(run('comparisonStats(.5,[null,undefined,NaN])'),{n:0,median:null,percentile:null});
assert.equal(run('comparisonStats(0,[0,0,0]).percentile'),50);
assert.equal(run('comparisonStats(.9,[.1,.2,.3,.4,.5,.6,.7],8).percentile'),null);
assert.equal(run('comparisonStats(.9,[.1,.2,.3,.4,.5,.6,.7,.8],8).percentile'),100);
assert.deepEqual(run("comparisonPeers('A')"),['B']);
assert.deepEqual(run("comparisonPeers('A','sector')"),['B','C']);
vm.runInContext("comparisonState.custom.A=['A','B','B','UNKNOWN','C'];comparisonState.modes.A='custom'",ctx);
assert.deepEqual(run("comparisonPeers('A')"),['B','C']);
vm.runInContext('comparisonState.custom.A=[]',ctx);
assert.deepEqual(run("comparisonPeers('A')"),[]);
assert.deepEqual(run("comparisonPeers('B')"),[]);
console.log('Comparison checks passed: no current/future leakage, exact windows, nulls, ties, minimum sample and peer baskets.');
