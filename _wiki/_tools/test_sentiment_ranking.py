import unittest
import datetime as dt
import sentiment_indicator_ranking as rank
import sentiment_relative_backtest as rel


def events(n=40,year='2026'):
    out=[]
    for i in range(n):
        p=[.1,.5,.9][i%3]
        out.append({'signal':(dt.date(int(year),1,2)+dt.timedelta(days=i*5)).isoformat(),
                    'return':.02*p+(.03 if i%4==0 else -.01),'qqq_return':.002,
                    'raw_percentiles':{f:{'own':p,'peer':p} for f in rank.FEATURES},'own_n':30,'peer_n':4})
    return out


class RankingTests(unittest.TestCase):
    def test_holm_fixed_family_and_monotonicity(self):
        self.assertEqual(rank.holm([.01,.04,.03,1]),[.04,.09,.09,1.])
        self.assertEqual(rank.holm([.001]+[1.]*15),[.016]+[1.]*15)

    def test_block_optimization_matches_full_row_resampling(self):
        es=rank.matched(events(43),'rsi14','own')
        es[8]['own']=None;es[15]['return']=None
        for multiplier in [1,2]:
            actual=rank.ranking_bootstrap(es,'own',5,'absolute',multiplier)
            lengths,starts=rank.draw_starts(len(es),5,multiplier);dist=[]
            for row in starts:
                sample=[es[(i+j)%len(es)] for i,length in zip(row,lengths) for j in range(length)]
                v=rel.spread(sample,'own')
                if v is not None:dist.append(v)
            dist.sort();observed=rel.spread(es,'own')
            tails=sum(abs(v-observed)+1e-12>=abs(observed) for v in dist)
            self.assertEqual(actual['valid_draws'],len(dist))
            self.assertEqual(actual['tail_count'],tails)
            self.assertAlmostEqual(actual['p'],(1+tails)/(len(dist)+1))
            for a,b in zip(actual['ci'],[dist[int(len(dist)*.025)],dist[int(len(dist)*.975)]]):self.assertAlmostEqual(a,b)

    def test_matching_preserves_schedule_and_missing_outcome(self):
        es=events();es[0]['raw_percentiles']['eps28']['own']=None;es[1]['return']=None
        summaries=[rel.summarize(rank.matched(es,f,'own'),'own',5,interval=False) for f in rank.FEATURES]
        self.assertTrue(all(s['n']==38 and s['scheduled']==40 and s['missing_returns']==1 and s['unavailable_signal']==1 for s in summaries))

    def test_no_future_year_diagnostics(self):
        es=events(40,'2024')+events(40,'2025')+events(40,'2026')
        r=rank.one_result(es,'2024','own','rsi14',5,'absolute','2026-10-26')
        self.assertEqual(list(r['years']),['2024']);self.assertEqual(r['temporal']['train_n'],0)
        self.assertFalse(r['checks']['years']);self.assertFalse(r['checks']['prior_direction'])

    def test_loo_tests_extremes_even_with_larger_middle_outlier(self):
        es=events(40)
        for e in es:e['return']=0 if e['raw_percentiles']['rsi14']['own']==.1 else .01
        es[0]['return']=.5;es[1]['return']=10.
        r=rank.one_result(es,'2026','own','rsi14',5,'absolute','2026-10-26')
        self.assertLess(r['loo']['same_sign'],r['loo']['tested']);self.assertFalse(r['checks']['outlier'])
        self.assertEqual(r['loo']['tested'],r['buckets'][0]['n']+r['buckets'][2]['n'])

    def test_small_sample_has_no_inference(self):
        r=rank.one_result(events(10),'2026','own','rsi14',20,'absolute','2026-10-26')
        self.assertEqual(r['p_raw'],1.);self.assertIsNone(r['bootstrap']['ci']);self.assertFalse(r['checks']['sample'])

    def test_wilson_plus_one_no_zero_tail_probability(self):
        lo,hi=rank.wilson(0,2000)
        self.assertGreaterEqual(lo,1/2001);self.assertGreater(hi,lo)

    def test_common_reference_rows_and_peers(self):
        dates=[(dt.date(2026,1,2)+dt.timedelta(days=7*i)).isoformat() for i in range(9)]
        snapshots={d:[{'ticker':'A','scores':{'tes':.5},**{f:i for f in rank.FEATURES}}] for i,d in enumerate(dates)}
        # Current-day reference must not enter history; incomplete peer never enters any raw rank.
        snapshots['2026-03-06']=[{'ticker':'A','scores':{'tes':.9},**{f:999 for f in rank.FEATURES}}]
        raw={t:{f:v for f in rank.FEATURES} for t,v in [('A',5),('B',1),('C',10)]};raw['C']['eps28']=None
        e={'signal':'2026-03-06','cutoff':'2026-03-05','entry':'2026-03-09','exit':'2026-03-16','qqq_return':.01}
        p={'snapshots':snapshots,'names':{'A':{},'B':{},'C':{}},'relative_context':{'2026-03-06':{'scores':{'A':{'tes':.5}},'raw':raw,'horizons':{'5':e}}},'company_studies':{'A':{'2026':{'5':[{**e,'return':.02}]}}}}
        row=rank.RawContext(p).raw_events('A',5,peers=['A','B','B','C','unknown'])[0]
        self.assertEqual(row['own_n'],9);self.assertEqual(row['peer_n'],1)
        for f in rank.FEATURES:self.assertEqual(row['raw_percentiles'][f]['peer'],1.)
        snapshots[dates[0]][0]['eps28']=None
        row=rank.RawContext(p).raw_events('A',5,peers=['B'])[0];self.assertEqual(row['own_n'],8)
        self.assertEqual(rank.RawContext(p).raw_events('A',5,peers=['B'],cutoff='2026-03-15'),[])


if __name__=='__main__':unittest.main()
