import unittest
import sentiment_relative_backtest as lab


class RelativeTests(unittest.TestCase):
    def test_percentile_bands_ties_and_missing(self):
        self.assertEqual(lab.percentile(.5,[None,.2,.5,.5,.8]),(.5,4))
        self.assertEqual(lab.percentile(None,[1,2]),(None,2))
        self.assertEqual(lab.percentile(1,[1]*7,8),(None,7))
        self.assertEqual([lab.band(x) for x in [None,0,.29999,.3,.69999,.7,1]],[None,0,0,1,1,2,2])

    def test_baseline_uses_axis_eligible_rows(self):
        events=[{'own':.1,'peer':.9,'return':.1,'qqq_return':.03,'peer_n':1},
                {'own':.9,'peer':None,'return':.3,'qqq_return':.05,'peer_n':0},
                {'own':None,'peer':.1,'return':1.,'qqq_return':.1,'peer_n':2},
                {'own':.1,'peer':.1,'return':None,'qqq_return':.1,'peer_n':2}]
        own=lab.summarize(events,'own',5)
        self.assertAlmostEqual(own['baseline'],.2)
        self.assertAlmostEqual(own['spread'],.2)
        self.assertEqual((own['n'],own['missing_returns'],own['unavailable_signal']),(2,1,1))
        peer=lab.summarize(events,'peer',5)
        self.assertAlmostEqual(peer['baseline'],.55)
        self.assertEqual(peer['thin_peer_events'],2)
        excess=lab.summarize(events,'own',5,'relative')
        self.assertAlmostEqual(excess['spread'],.18)
        self.assertIsNone(own['ci'])

    def test_bootstrap_retains_placeholders_and_reports_failed_draws(self):
        events=[{'own':None,'return':None} for _ in range(32)]
        events[0]={'own':.1,'return':.1}
        events[16]={'own':.9,'return':.3}
        b=lab.block_interval(events,5,lambda a:lab.spread(a,'own'))
        self.assertEqual(b['draws'],1000)
        self.assertLess(b['valid_draws'],900)
        self.assertIsNone(b['ci'])
        self.assertEqual(b,lab.block_interval(events,5,lambda a:lab.spread(a,'own')))

    def test_master_schedule_and_strict_prior_history(self):
        dates=['2026-01-%02d'%d for d in range(1,10)]
        snapshots={d:[{'ticker':'A','scores':{'tes':i/10}}] for i,d in enumerate(dates)}
        horizons={'5':{'signal':'2026-01-09','cutoff':'2026-01-08','entry':'2026-01-12','exit':'2026-01-19','qqq_return':.1}}
        payload={'names':{'A':{},'B':{},'C':{}},'snapshots':snapshots,
          'peer_groups':{'A':{'default_mode':'direct','direct':[{'ticker':'B'},{'ticker':'C'}],'sector':[]}},
          'relative_context':{'2026-01-09':{'scores':{'A':{'tes':.8},'B':{'tes':.9},'C':{'tes':None}},'horizons':horizons}},
          'company_studies':{'A':{'2026':{'5':[]}}}}
        ctx=lab.Context(payload)
        ranks=ctx.ranks_at('A','2026-01-09','tes')
        self.assertEqual(ranks,{'own':1.,'own_n':8,'peer':0.,'peer_n':1})
        es=ctx.events('A','2026',5,'tes')
        self.assertEqual(len(es),1)
        self.assertIsNone(es[0]['return'])
        self.assertEqual(ctx.events('A','2026',5,'tes',cutoff='2026-01-18'),[])
        payload['snapshots']['2026-12-31']=[{'ticker':'A','scores':{'tes':999}}]
        self.assertEqual(lab.Context(payload).ranks_at('A','2026-01-09','tes'),ranks)


if __name__=='__main__':
    unittest.main()
