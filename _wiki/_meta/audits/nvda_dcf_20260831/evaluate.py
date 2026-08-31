import json,re,math,datetime,zipfile,xml.etree.ElementTree as ET,collections
from pathlib import Path
P=Path(__file__).parent
W=json.loads((P/'workbook.json').read_text(encoding='utf-8'))
B='Capa DCF - Base'; R='ROIC Cloud'
def ci(s):
    n=0
    for c in s: n=n*26+ord(c)-64
    return n
def cl(n):
    s=''
    while n:
        n,r=divmod(n-1,26);s=chr(65+r)+s
    return s
def split(a):
    m=re.fullmatch(r'([A-Z]+)(\d+)',a.replace('$',''));return ci(m[1]),int(m[2])
def v(s,a):return W['sheets'][s]['cells'].get(a,{}).get('v',0) or 0
EXT={}
N={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(W['source']) as z:
    root=ET.fromstring(z.read('xl/externalLinks/externalLink90.xml'))
    sheetnames=[x.get('val') for x in root.findall('m:externalBook/m:sheetNames/m:sheetName',N)]
    for sh in root.findall('m:externalBook/m:sheetDataSet/m:sheetData',N):
        name='[90]'+sheetnames[int(sh.get('sheetId'))]
        for cell in sh.findall('m:row/m:cell',N):
            val=cell.find('m:v',N)
            if val is not None:
                try: EXT[(name,cell.get('r'))]=float(val.text)
                except: EXT[(name,cell.get('r'))]=val.text
TOKEN=re.compile(r"\s*('(?:[^']|'')+'!\$?[A-Z]{1,3}\$?\d+|\$?[A-Z]{1,3}\$?\d+|(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?|[A-Za-z_][\w.]*|[+\-*/^%():,])")
class Ref:
    def __init__(self,sheet,addrs,ev):self.sheet=sheet;self.addrs=addrs;self.ev=ev
    def values(self):return [self.ev.cell(self.sheet,a) for a in self.addrs]
    def scalar(self):return self.values()[0]
def scalar(x):return x.scalar() if isinstance(x,Ref) else x
def flatten(args):
    return [val for x in args for val in (x.values() if isinstance(x,Ref) else [x])]
class Eval:
    def __init__(self,overrides=None):self.cache={};self.active=set();self.overrides=overrides or {};self.deps=collections.defaultdict(set)
    def cell(self,s,a):
        key=(s,a)
        if self.active:self.deps[next(reversed(list(self.active)))].add(key)
        if key in self.overrides:return self.overrides[key]
        if key in EXT:return EXT[key]
        if key in self.cache:return self.cache[key]
        if key in self.active:raise ValueError('CYCLE '+str(key))
        if s not in W['sheets']:raise ValueError('MISSING SHEET '+s)
        d=W['sheets'][s]['cells'].get(a,{})
        f=d.get('f')
        if f:
            self.active.add(key)
            try: result=Parser(f,s,a,self).run()
            finally:self.active.remove(key)
        else:result=d.get('v',0) or 0
        self.cache[key]=result;return result
class Parser:
    def __init__(self,formula,sheet,addr,ev):
        self.f=formula;self.s=sheet;self.a=addr;self.ev=ev;self.i=0;self.ts=[]
        pos=0
        while pos<len(formula):
            m=TOKEN.match(formula,pos)
            if not m:raise ValueError('TOKEN '+formula[pos:])
            self.ts.append(m[1]);pos=m.end()
    def take(self):x=self.ts[self.i];self.i+=1;return x
    def peek(self):return self.ts[self.i] if self.i<len(self.ts) else ''
    def run(self):
        out=scalar(self.expr())
        if self.i!=len(self.ts):raise ValueError('UNCONSUMED '+self.f)
        return out
    def expr(self,minbp=0):
        token=self.take()
        if token in ('+','-'):
            left=scalar(self.expr(40));left=left if token=='+' else -left
        elif token=='(':
            left=self.expr();assert self.take()==')'
        elif re.fullmatch(r'(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?',token):left=float(token)
        elif re.search(r'\$?[A-Z]{1,3}\$?\d+$',token):
            s,a=token.rsplit('!',1) if '!' in token else (self.s,token)
            if s.startswith("'"):s=s[1:-1].replace("''","'")
            a=a.replace('$','');addrs=[a]
            if self.peek()==':':
                self.take();last=self.take().replace('$','');c1,r1=split(a);c2,r2=split(last)
                addrs=[cl(c)+str(r) for r in range(r1,r2+1) for c in range(c1,c2+1)]
            left=Ref(s,addrs,self.ev)
        else:
            name=token.upper();assert self.take()=='('
            args=[]
            if self.peek()!=')':
                while True:
                    args.append(self.expr())
                    if self.peek()!=',':break
                    self.take()
            assert self.take()==')'
            if name in ('SUM','MIN','MAX'):
                vs=flatten(args);left={'SUM':sum,'MIN':min,'MAX':max}[name](vs)
            elif name=='NPV':
                rate=scalar(args[0]);vs=flatten(args[1:]);left=sum(n/(1+rate)**(i+1) for i,n in enumerate(vs))
            elif name=='INDEX':left=args[0].values()[int(scalar(args[1]))-1]
            elif name in ('COLUMN','ROW'):
                a=args[0].addrs[0] if args else self.a;c,r=split(a);left=c if name=='COLUMN' else r
            elif name=='DATE':
                y,m,d=[int(scalar(a)) for a in args];left=(datetime.date(y,m,d)-datetime.date(1899,12,30)).days
            else:raise ValueError('FUNCTION '+name)
        while self.peek():
            op=self.peek()
            if op=='%':
                if 50<minbp:break
                self.take();left=scalar(left)/100;continue
            bp={'+':10,'-':10,'*':20,'/':20,'^':30}.get(op,-1)
            if bp<minbp:break
            self.take();right=scalar(self.expr(bp+(0 if op=='^' else 1)));left=scalar(left)
            if op=='+':left+=right
            elif op=='-':left-=right
            elif op=='*':left*=right
            elif op=='/':left/=right
            elif op=='^':left**=right
        return left
e=Eval();diffs=[];errors=[];n=0
for s,sh in W['sheets'].items():
    for a,d in sh['cells'].items():
        if not d.get('f'):continue
        try:
            actual=e.cell(s,a);expected=d['v'];n+=1
            if isinstance(expected,(int,float)) and not math.isclose(actual,expected,rel_tol=1e-11,abs_tol=1e-7):diffs.append([s,a,expected,actual])
        except Exception as ex:errors.append([s,a,str(ex)])
data={'formula_recalculation':{'calculated':n,'mismatches':diffs,'errors':errors}}
dt=[]
for row in range(97,103):
    for col in range(5,11):
        ev=Eval({(B,'D92'):v(B,'D'+str(row)),(B,'D93'):v(B,cl(col)+'96')})
        expected=ev.cell(B,'E88');saved=v(B,cl(col)+str(row))
        dt.append({'cell':cl(col)+str(row),'saved':saved,'recalc':expected,'diff':expected-saved})
data['data_table']=dt
r=v(B,'D81');g=v(B,'D83');shares=v(B,'D86');flows=[v(B,cl(c)+'79') for c in range(7,27)]
pv=sum(x/(1+r)**(t+1) for t,x in enumerate(flows))
tv=flows[-1]*(1+g)/(r-g);pvtv=tv/(1+r)**20
roll=lambda date:(1+r)**((date-datetime.date(2026,1,1)).days/365)
dt27=roll(datetime.date(2026,8,27));dt31=roll(datetime.date(2026,8,31))
data['valuation']={'forecast_periods':len(flows),'pv_forecast':pv,'terminal_value':tv,'pv_terminal_year20':pvtv,'pv_terminal_year21':tv/(1+r)**21,'old_value':(pv+tv/(1+r)**21)/shares,'correct_timing_jan1':(pv+pvtv)/shares,'aug27_value':(pv+pvtv)*dt27/shares,'aug31_value':(pv+pvtv)*dt31/shares,'tv_only_delta_per_share':(pvtv-tv/(1+r)**21)/shares,'old_vs_corrected':v(B,'E88')/v(B,'D88')-1,'correct_pe27':v(B,'E88')/v(B,'H76'),'correct_pe28':v(B,'E88')/v(B,'I76'),'terminal_payout80_value':Eval({(B,'Z78'):0.8}).cell(B,'E88')}
scenarios=[]
for row in range(118,143):
    vals=[v(B,cl(c)+str(row)) for c in range(6,23)]
    rev_end=vals[-1]/((v(B,'Z61')-v(B,'Z67'))*(1-v(B,'Z71'))*v(B,'Z78'))
    target=v(B,'I59')*(1+v(B,'C'+str(row)))**17
    allflows=flows[:3]+vals;tv_s=v(B,'W'+str(row))
    pv_s=sum(n/(1+r)**(i+1) for i,n in enumerate(allflows))
    corr=(pv_s+tv_s/(1+r)**20)*dt27/shares
    scenarios.append({'row':row,'cagr':v(B,'C'+str(row)),'share':v(B,'D'+str(row)),'capex_growth':v(B,'E'+str(row)),'endpoint_diff':rev_end-target,'saved_value':v(B,'X'+str(row))/shares,'corrected_aug27_value':corr})
data['scenarios']=scenarios
recs=[]
for c in range(4,10):
    C=cl(c)
    for label,total,parts in [('Capex split',6,[7,8,9]),('Hyper models',16,[17,18,19,20]),('Hyper AI',22,[23,24,25,26]),('Other players',30,[31,32,33,34,35,36]),('Total AI capex',6,[22,30]),('Designer top-level',40,[41,42,46,49,50,51]),('AVGO subtotal',42,[43,44,45]),('MRVL subtotal',46,[47,48])]:
        recs.append({'year':v(B,C+'4'),'label':label,'total_cell':C+str(total),'total':v(B,C+str(total)),'parts':sum(v(B,C+str(p)) for p in parts),'diff':v(B,C+str(total))-sum(v(B,C+str(p)) for p in parts)})
data['subtotal_reconciliation']=recs
# Compare exactly specified component lives vs the workbook's blended-life approximation.
weights=[v(B,'H12'),v(B,'H13'),v(B,'H14')];lives=[5,6,15];blend=v(R,'D9')
fleet=[];lag=[]
for c in range(6,27):
    cap_net=da=mid_net=0
    for vintage in range(4,c-1):
        age=c-vintage-2;cap=v(R,cl(vintage)+'15')
        for weight,life in zip(weights,lives):
            start=max(0,1-age/life);end=max(0,1-(age+1)/life)
            cap_net+=cap*weight*(start+end)/2
            da+=cap*weight*(start-end)
        start=max(0,1-age*blend);end=max(0,1-(age+1)*blend)
        mid_net+=cap*(start+end)/2
    tax=v(R,'D8');margin=v(R,'D7');demand=v(R,cl(c)+'25')
    fleet.append({'year':v(B,cl(c)+'4'),'net_cap_saved':v(R,cl(c)+'20'),'net_cap_true_tiered':cap_net,'net_cap_blend_avg':mid_net,'da_saved':v(R,cl(c)+'21'),'da_true_tiered':da,'rev15_saved':v(R,cl(c)+'22'),'rev15_true_tiered':(v(R,'D10')*cap_net/(1-tax)+da)/margin,'roic_saved':v(R,cl(c)+'27') if demand else None,'roic_true_tiered':(margin*demand-da)*(1-tax)/cap_net if demand else None})
    if c>=7 and c<=14:
        t1=v(R,cl(c-1)+'15');t2=v(R,cl(c-2)+'15')
        lag.append({'year':v(B,cl(c)+'4'),'capex_t1':t1,'capex_t2':t2,'rev15_t1':v(R,'D12')*t1,'rev15_t2':v(R,'D12')*t2,'roic_saved':v(R,cl(c)+'26'),'roic_t2':(margin*demand/t2-blend)*(1-tax)})
data['cloud_lag']=lag;data['cloud_fleet']=fleet
data['notes_check']={'margin':v(R,'D7'),'M15':v(R,'D12'),'M20':v(R,'D13'),'M15_at50margin':(v(R,'D10')/(1-v(R,'D8'))+blend)/.5,'M15_at70margin':(v(R,'D10')/(1-v(R,'D8'))+blend)/.7,'M15_flat5years':(v(R,'D10')/(1-v(R,'D8'))+.2)/v(R,'D7'),'M15_pretax':(v(R,'D10')+blend)/v(R,'D7')}
names=W['names']
data['metadata_audit']={'defined_names':len(names),'broken_defined_names':sum('#REF!' in (x.get('value') or '') for x in names),'active_external_formulas':[(s,a,d['f']) for s,sh in W['sheets'].items() for a,d in sh['cells'].items() if re.search(r'\[\d+\]',d.get('f',''))],'link90':W['links'].get('xl/externalLinks/_rels/externalLink90.xml.rels'),'comments':W['comments']}
(P/'checks.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
summary={k:val for k,val in data.items() if k not in ['data_table','scenarios','subtotal_reconciliation','cloud_fleet','metadata_audit']}
summary['data_table_max_abs_diff']=max(abs(d['diff']) for d in dt)
summary['scenario_max_endpoint_diff']=max(abs(s['endpoint_diff']) for s in scenarios)
summary['scenario_example']=scenarios[11]
summary['subtotal_exceptions']=[x for x in recs if abs(x['diff'])>1e-5]
summary['fleet_selected']=[x for i,x in enumerate(fleet) if i in [4,5,8,10,20]]
summary['metadata_audit']={k:v for k,v in data['metadata_audit'].items() if k!='comments'}
print(json.dumps(summary,indent=2,ensure_ascii=False))

