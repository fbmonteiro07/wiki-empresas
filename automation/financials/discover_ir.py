import concurrent.futures,json,re,urllib.parse
from collect_sources import ROOT,DATA,fetch,write_json,strip
PAGES={'JPM':'https://www.jpmorganchase.com/ir/quarterly-earnings','SPGI':'https://investor.spglobal.com/quarterly-earnings/default.aspx','MCO':'https://ir.moodys.com/financials/quarterly-results/default.aspx','BX':'https://ir.blackstone.com/financials/quarterly-results/default.aspx','KKR':'https://ir.kkr.com/financial-information/quarterly-results','GS':'https://www.goldmansachs.com/investor-relations/financials/','V':'https://investor.visa.com/financial-information/quarterly-earnings/default.aspx','MA':'https://investor.mastercard.com/financials-and-sec-filings/quarterly-results/default.aspx','APO':'https://ir.apollo.com/financial-results','HOOD':'https://investors.robinhood.com/financials/quarterly-results','COIN':'https://investor.coinbase.com/financials/quarterly-results/default.aspx'}
def one(t,u):
    try:
        s=fetch(u).decode('utf-8','replace')
        p=DATA/'discovery'/f'{t}_ir.html'; p.parent.mkdir(exist_ok=True); p.write_text(s,encoding='utf-8')
        links=[{'url':urllib.parse.urljoin(u,m[0]),'title':strip(m[1])} for m in re.findall(r'<a\b[^>]*href=["\x27]([^"\x27]+)["\x27][^>]*>(.*?)</a>',s,re.S|re.I) if re.search(r'transcript|earnings|quarterly|financial',m[0]+' '+m[1],re.I)]
        write_json(DATA/'discovery'/f'{t}_ir_links.json',{'url':u,'links':links})
        trans=[x for x in links if re.search('transcript',x['url']+' '+x['title'],re.I)]
        print(t,len(s),'links',len(links),'transcripts',len(trans),json.dumps(trans[:2]),flush=True)
    except Exception as e: print('IR_FAILED',t,str(e),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(lambda x:one(*x),PAGES.items()))

