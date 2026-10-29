"""Material accounting, timing and missing-data checks for the research engine."""
import math
import unittest
from types import SimpleNamespace

import build_sentiment_research as lab


class ResearchTests(unittest.TestCase):
    def test_peer_groups_use_only_curated_edges_and_named_sector_fallback(self):
        inp=SimpleNamespace(names=['A','B','C','D'],groups={'A':'Tech','B':'Tech','C':'Other'},
                            peer_graph={'competes':[['A','B','competes'],['A','OUTSIDE','not covered']]})
        p=lab.peer_groups(inp)
        self.assertEqual(p['A']['direct'],[{'ticker':'B','reason':'competes'}])
        self.assertEqual(p['B']['direct'],[{'ticker':'A','reason':'competes'}])
        self.assertEqual(p['A']['default_mode'],'direct')
        self.assertEqual(p['C']['sector'],[])
        self.assertEqual(p['D']['sector'],[])

    def test_midrank_ties(self):
        self.assertEqual(lab.ranks({'B':2,'A':2,'C':5}),{'B':.25,'A':.25,'C':1.})
        self.assertEqual(lab.ranks({'B':2,'A':2}),{'B':.5,'A':.5})

    def test_rsi_uses_only_prefix_and_handles_flat_prices(self):
        prices=[100+i*.3+math.sin(i)*2 for i in range(100)]
        self.assertEqual(lab.rsi(prices)[:50],lab.rsi(prices[:50]))
        self.assertEqual(lab.rsi([100.]*20)[-1],50.)
        self.assertEqual(lab.rsi(list(range(1,30)))[-1],100.)

    def test_observation_is_never_backfilled(self):
        s=lab.Series({'2026-01-05':10,'2026-02-01':20})
        self.assertIsNone(s.at('2026-01-04',35))
        self.assertEqual(s.at('2026-01-20',35),10)
        self.assertIsNone(s.at('2026-01-20',10))
        self.assertEqual(s.window('2026-01-31',30),[('2026-01-05',10.)])

    def test_zero_and_negative_earnings(self):
        self.assertEqual(lab.symmetric_change(0,0),0)
        self.assertEqual(lab.symmetric_change(1,-1),2)
        self.assertAlmostEqual(lab.symmetric_change(-.5,-1),2/3)
        self.assertIsNone(lab.symmetric_change(None,1))

    def test_self_financing_fee_equation(self):
        for old,new in [({}, {'A':1}),({'A':1},{'B':1}),({'A':.6,'B':.4},{'A':.5,'B':.5})]:
            x,trade=lab.execution_scale(new,old,.005)
            self.assertAlmostEqual(x+.005*trade,1.,places=12)
        x,_=lab.execution_scale({'A':1},{},.005)
        self.assertAlmostEqual(x,1/1.005,places=12)
        x,trade=lab.execution_scale({'A':1},{'A':1},.005)
        self.assertAlmostEqual(x,1.)
        self.assertAlmostEqual(trade,0.)

    def test_initial_and_exit_cost_and_daily_drawdown(self):
        cal=['2026-01-02','2026-01-05','2026-01-06','2026-01-07']
        data=SimpleNamespace(calendar=cal,tri={'A':lab.Series(dict(zip(cal,[100,100,80,110])))})
        events=[{'signal':cal[0],'entry':cal[1],'exit':cal[3],'entry_i':1,'exit_i':3,'eligible':['A']}]
        p=lab.portfolio(data,events,'equal',10)
        self.assertAlmostEqual(p['return'],1.1/1.001*.999-1,places=12)
        self.assertAlmostEqual(p['drawdown'],.8/1.001-1,places=12)

    def test_drift_aware_rebalance(self):
        cal=['2026-01-02','2026-01-05','2026-01-06','2026-01-07','2026-01-08']
        data=SimpleNamespace(calendar=cal,tri={'A':lab.Series(dict(zip(cal,[100,100,150,150,150]))),
                                              'B':lab.Series(dict(zip(cal,[100,100,100,100,100])))})
        events=[{'signal':cal[0],'entry':cal[1],'exit':cal[2],'entry_i':1,'exit_i':2,'eligible':['A','B']},
                {'signal':cal[1],'entry':cal[2],'exit':cal[4],'entry_i':2,'exit_i':4,'eligible':['A','B']}]
        p=lab.portfolio(data,events,'equal',0)
        self.assertAlmostEqual(p['periods'][1]['turnover'],.2)
        self.assertAlmostEqual(p['return'],.25)

    def test_cash_gap_liquidates_and_repurchases(self):
        cal=['2026-01-02','2026-01-05','2026-01-06','2026-01-07','2026-01-08','2026-01-09']
        data=SimpleNamespace(calendar=cal,tri={'A':lab.Series(dict(zip(cal,[100,100,110,200,200,220])))})
        events=[{'signal':cal[0],'entry':cal[1],'exit':cal[2],'entry_i':1,'exit_i':2,'eligible':['A']},
                {'signal':cal[3],'entry':cal[4],'exit':cal[5],'entry_i':4,'exit_i':5,'eligible':['A']}]
        p=lab.portfolio(data,events,'equal',10)
        expected=(1.1/1.001*.999)**2-1
        self.assertAlmostEqual(p['return'],expected,places=12)
        self.assertAlmostEqual(math.prod(1+x['net'] for x in p['periods'])-1,expected,places=12)

    def test_bootstrap_null_and_small_samples(self):
        self.assertIsNone(lab.bootstrap([0.]*7,20))
        self.assertEqual(lab.bootstrap([0.]*10,20),[0.,0.])


class SourceIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs=lab.Inputs()

    def test_listing_currency_is_not_reporting_currency(self):
        self.assertNotIn('SMIC',self.inputs.usd)
        self.assertTrue(all(self.inputs.companies[t]['bbg'].endswith(' US Equity') for t in self.inputs.usd))

    def test_future_source_observations_cannot_change_signal(self):
        inp=self.inputs
        signal='2026-04-02'
        before=inp.rows(signal)['AAPL'].copy()
        # Add unmistakably extreme observations strictly after the signal.
        for seq in inp.vendor['AAPL'].values():
            seq.data['2026-12-31']=999999
            seq.dates=sorted(seq.data)
        for seq in inp.estimates[2026]['AAPL'].values():
            seq.data['2026-12-31']=999999
            seq.dates=sorted(seq.data)
        inp.cache.clear()
        after=inp.rows(signal)['AAPL']
        self.assertEqual(before,after)

    def test_fixed_fiscal_estimate_definition_and_core_dates(self):
        self.assertEqual(self.inputs.est[2026]['override'],'2027Y')
        events,skips=lab.select_events(self.inputs,2026,20,'core')
        self.assertGreaterEqual(len(events),8)
        self.assertEqual(skips,[])
        for e in events:
            self.assertLess(e['cutoff'],e['signal'])
            self.assertLess(e['signal'],e['entry'])
            self.assertEqual(e['exit_i']-e['entry_i'],20)
            self.assertNotIn('SMIC',e['eligible'])
        for a,b in zip(events,events[1:]):
            self.assertLessEqual(a['exit'],b['entry'])

    def test_company_outcomes_use_display_ranks_and_exact_forward_window(self):
        study=lab.company_studies(self.inputs)
        self.assertNotIn('SMIC',study)
        events=study['NVDA']['2026']['20']
        self.assertEqual(len(events),10)
        for e in events:
            rows=self.inputs.rows(e['signal'])
            expected=lab.scores(rows,list(rows))['NVDA']
            self.assertEqual(e['scores'],expected)
            self.assertLess(e['cutoff'],e['signal'])
            self.assertLess(e['signal'],e['entry'])
            self.assertEqual(self.inputs.calendar.index(e['exit'])-self.inputs.calendar.index(e['entry']),20)
            self.assertAlmostEqual(e['return'],e['tri_exit']/e['tri_entry']-1)
        for a,b in zip(events,events[1:]):
            self.assertLessEqual(a['exit'],b['entry'])


if __name__=='__main__':
    unittest.main()
