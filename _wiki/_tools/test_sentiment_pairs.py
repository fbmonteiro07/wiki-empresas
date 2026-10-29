import unittest
import copy
import datetime as dt
import sentiment_pair_backtest as p
import sentiment_indicator_ranking as raw


def fixture():
    events=[]
    for year in [2024,2025,2026]:
        for i in range(40):
            date=dt.date(year,1,5)+dt.timedelta(days=i*6)
            ranks={f:{'own':((i*(j+1)+j*3)%11)/10,'peer':((i*(j+1)+j*3)%11)/10} for j,f in enumerate(p.FEATURES)}
            events.append({'signal':date.isoformat(),'exit':(date+dt.timedelta(days=3)).isoformat(),'entry':(date+dt.timedelta(days=1)).isoformat(),
                'cutoff':(date-dt.timedelta(days=1)).isoformat(),'return':.08*ranks['rsi14']['own']-.02,'raw_percentiles':ranks,'peer_n':4})
    return events


class PairTests(unittest.TestCase):
    def test_six_pairs_four_orientations_eight_singles(self):
        self.assertEqual(len(p.rules()),24);self.assertEqual(len(p.singles()),8)
        self.assertEqual(len({tuple(r['features']) for r in p.rules()}),6)

    def test_oriented_blend_not_and(self):
        e=fixture()[0];e['raw_percentiles']['rsi14']['own']=.9;e['raw_percentiles']['eps28']['own']=.5
        self.assertEqual(p.position(e,{'features':['rsi14','eps28'],'signs':[1,1]},'own'),1)
        e['raw_percentiles']['rsi14']['own']=.3
        self.assertEqual(p.position(e,{'features':['rsi14'],'signs':[-1]},'own'),1)

    def test_exact_entry_exit_cost_and_missing_not_cash(self):
        e=fixture()[0];e['raw_percentiles']['rsi14']['own']=1;e['return']=.20
        r=p.singles()[0];self.assertAlmostEqual(p.outcome(e,r,'own'),1.2*.999/1.001-1)
        e['return']=None;self.assertIsNone(p.outcome(e,r,'own'))
        e['return']=.2;e['raw_percentiles']['tone7']['own']=None;self.assertIsNone(p.position(e,r,'own'))

    def test_cash_only_resamples_remain_valid(self):
        b=p.mean_bootstrap([0.]*40,5,1)
        self.assertEqual(b['valid_draws'],2000);self.assertEqual(b['ci'],[0.,0.]);self.assertEqual(b['p'],1.)

    def test_optimized_bootstrap_against_direct_resampling(self):
        v=[None if i%13==0 else (i%7-2)/100 for i in range(40)]
        for mult in [1,2]:
            b=p.mean_bootstrap(v,5,mult);lengths,starts=raw.draw_starts(40,5,mult);dist=[]
            for row in starts:
                sample=[v[(i+j)%40] for i,l in zip(row,lengths) for j in range(l) if v[(i+j)%40] is not None]
                if sample:dist.append(sum(sample)/len(sample))
            dist.sort();self.assertAlmostEqual(b['ci'][0],dist[50]);self.assertAlmostEqual(b['ci'][1],dist[1950])

    def test_selection_forbids_2026(self):
        with self.assertRaises(AssertionError):p.choose(fixture(),'own')

    def test_test_returns_and_features_cannot_change_selection(self):
        es=fixture()
        class Context:
            def raw_events(self,*args):return es
        payload={'meta':{'signal_asof':'2026-10-27'},'snapshots':{'2026-10-27':[{'cutoff':'2026-10-26'}]}}
        first=p.company(payload,'T',Context());choices=p.selection_document({'T':first})
        for e in es:
            if e['signal'].startswith('2026'):
                e['return']=100-e['return'];e['raw_percentiles']={f:{'own':1,'peer':0} for f in p.FEATURES}
        second=p.company(payload,'T',Context())
        self.assertEqual(choices,p.selection_document({'T':second}))
        self.assertTrue(all(e['selection']['winner'] for e in first['experiments']))

    def test_twenty_day_validation_too_short(self):
        es=fixture();train=[e for e in es if e['signal']<'2026'];selection=p.choose(train,'own')
        c=p.contrast(es[-10:],selection['winner']['rule'],selection['single']['rule'],'own',20)
        self.assertFalse(c['support']);self.assertIsNone(c['bootstrap']['ci']);self.assertEqual(c['p_raw'],1.)


if __name__=='__main__':unittest.main()
