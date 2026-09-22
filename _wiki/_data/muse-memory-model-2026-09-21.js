/* Exhibit received 2026-09-21; original author/date and supply years unconfirmed.
   Decimal units: one billion people * GB/person = EB of capacity.
   These percentages compare a stock with one year's output as a scale benchmark. */
(function (root) {
  'use strict';
  const defaults = Object.freeze({people:3.6, awake:25, ram:2, idle:0, files:5, copies:2, dram:35, nand:1000, fullRam:8, fullStorage:100});
  const adoptions = [5,10,25,50];
  const targets = [['4.1','0.26','1.8','0.18'],['8.2','0.51','3.6','0.36'],['20.6','1.3','9.0','0.90'],['41.1','2.6','18.0','1.8']];
  function validate(p) {
    const errors=[];
    for(const k of Object.keys(defaults)) if(!Number.isFinite(p[k])) errors.push(k+' must be a number.');
    for(const k of ['people','dram','nand']) if(p[k]<=0) errors.push(k+' must be greater than zero.');
    for(const k of ['ram','idle','files','fullRam','fullStorage']) if(p[k]<0) errors.push(k+' cannot be negative.');
    if(p.awake<0||p.awake>100) errors.push('Resident fraction must be between 0 and 100%.');
    if(p.copies<1) errors.push('Total copies must be at least one (including the original).');
    return errors;
  }
  function calculate(p, adoption) {
    const errors=validate(p);
    if(!Number.isFinite(adoption)||adoption<0||adoption>100) errors.push('Adoption must be between 0 and 100%.');
    if(errors.length) throw new Error(errors.join(' '));
    const users=p.people*adoption/100;
    const dramPerUser=p.awake/100*p.ram+(1-p.awake/100)*p.idle;
    const nandPerUser=p.files*p.copies;
    const stocks=[users*p.fullRam,users*dramPerUser,users*p.fullStorage,users*nandPerUser];
    return {adoption, users, dramPerUser,nandPerUser,stocks,shares:stocks.map((v,i)=>100*v/(i<2?p.dram:p.nand))};
  }
  function chartCheck(p) {
    let matches=0;
    adoptions.forEach((a,i)=>calculate(p,a).shares.forEach((v,j)=>{
      const decimals=targets[i][j].split('.')[1].length;
      if(v.toFixed(decimals)===targets[i][j]) matches++;
    }));
    return matches;
  }
  const api={defaults,adoptions,targets,validate,calculate,chartCheck};
  if(typeof module==='object'&&module.exports) module.exports=api;
  else root.MuseMemory=api;
})(typeof window==='object'?window:this);
