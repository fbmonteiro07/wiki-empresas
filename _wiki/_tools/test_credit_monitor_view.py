"""Credit view regressions: units, incomplete coverage, stale marks and stable benchmarks."""
import datetime as dt
import unittest
from credit_monitor_view import model, json_script

TODAY = dt.date(2026, 10, 14)


class CreditViewTests(unittest.TestCase):
    def config(self):
        return {'board': {'issuers': [
            {'company': 'ORCL', 'name': 'Oracle', 'cds': 'ORCLCP CDS USD SR 5Y D14 Corp',
             'bonds': [{'cpn': 6.7, 'mty': '2056-02-04', 'headline': True},
                       {'cpn': 5.7, 'mty': '2036-02-04', 'headline': True}]},
            {'company': 'NBIS', 'name': 'Nebius', 'cds': None,
             'bonds': [{'cpn': 4.5, 'mty': '2034-02-15', 'type': 'convertible', 'headline': True}]},
            {'company': 'CRWV', 'name': 'CoreWeave', 'cds': 'CRWV CDS USD SR 5Y D14 Corp',
             'bonds': [{'cpn': 9.625, 'mty': '2032-07-15', 'headline': True}]},
        ]}}

    def view(self, series=()):
        return model(self.config(), {'series': list(series)}, TODAY)

    def test_empty_feed_does_not_turn_coupon_into_yield(self):
        data = self.view()
        self.assertEqual([c['id'] for c in data['issuers']], ['CRWV', 'ORCL', 'NBIS'])
        self.assertIsNone(data['latest'])
        for c in data['issuers']:
            for b in c['bonds']:
                self.assertIsNone(b['last'])
                self.assertEqual(b['points'], [])
                self.assertTrue(all(v is None for v in b['changes'].values()))
        self.assertIsNone(data['issuers'][2]['cds'])

    def test_stable_single_benchmark_uses_shorter_headline(self):
        data = self.view([{'id':'ORCL_6.7_2056', 'points':[['2026-10-14', 7.2]]}])
        self.assertEqual(data['issuers'][1]['main'], 'ORCL_5.7_2036')

    def test_cds_and_yield_changes_keep_bp_units(self):
        data = self.view([
            {'id':'CRWV_CDS5Y', 'points':[['2026-10-07',400],['2026-10-13',420],['2026-10-14',450]]},
            {'id':'CRWV_9.625_2032', 'points':[['2026-10-07',10],['2026-10-13',10.2],['2026-10-14',10.5]]},
        ])
        c = data['issuers'][0]
        self.assertEqual(c['cds']['changes']['1']['value'],30)
        self.assertEqual(c['bonds'][0]['changes']['1']['value'],30)
        self.assertEqual(c['cds']['changes']['7']['value'],50)
        self.assertEqual(c['bonds'][0]['last'],10.5)
        self.assertIsNone(c['cds']['changes']['30'])

    def test_weekend_daily_change_uses_prior_session(self):
        data = self.view([{'id':'CRWV_CDS5Y','points':[['2026-10-09',100],['2026-10-12',110]]}])
        d=data['issuers'][0]['cds']['changes']['1']
        self.assertEqual((d['start'],d['end'],d['value']),('2026-10-09','2026-10-12',10))

    def test_invalid_future_and_duplicate_points(self):
        data = self.view([{'id':'CRWV_CDS5Y','last':999,'points':[
            ['2026-10-14',0],['2026-10-14',12],['2026-10-15',99],
            ['bad',50],['2026-10-13',float('nan')]]}])
        self.assertEqual(data['issuers'][0]['cds']['last'],12)
        self.assertEqual(data['issuers'][0]['cds']['date'],'2026-10-14')
        self.assertEqual(len(data['issuers'][0]['cds']['points']),1)

    def test_retained_recent_data_and_old_ok_data_are_stale(self):
        for attrs in ({'status':'stale','points':[['2026-10-14',100]]},
                      {'status':'ok','points':[['2026-10-01',100]]},
                      {'status':'ok','error':'fetch failed','points':[['2026-10-14',100]]}):
            c=self.view([{'id':'CRWV_CDS5Y',**attrs}])['issuers'][0]['cds']
            self.assertEqual(c['status'],'stale')
            self.assertEqual(c['last'],100)

    def test_mismatched_field_or_units_are_not_plotted(self):
        for attrs in ({'unit':'%'},{'field':'YLD_YTM_MID'}):
            c=self.view([{'id':'CRWV_CDS5Y','points':[['2026-10-14',4]],**attrs}])['issuers'][0]['cds']
            self.assertEqual(c['status'],'missing')
            self.assertIsNone(c['last'])

    def test_unreconciled_cds_is_withheld_without_destroying_history_or_bonds(self):
        cfg=self.config()
        crwv=next(c for c in cfg['board']['issuers'] if c['company']=='CRWV')
        crwv['cds_validation_warning']='Conflicting Bloomberg fields'
        watch={'series':[
            {'id':'CRWV_CDS5Y','points':[['2026-10-13',434],['2026-10-14',440]]},
            {'id':'CRWV_9.625_2032','points':[['2026-10-13',14.469],['2026-10-14',15.470]]}]}
        row=model(cfg,watch,TODAY)['issuers'][0]
        self.assertEqual(row['cds']['status'],'unverified')
        self.assertEqual(row['cds']['points'],[])
        self.assertIsNone(row['cds']['last'])
        self.assertTrue(all(v is None for v in row['cds']['changes'].values()))
        self.assertIn('Conflicting',row['cds']['validationWarning'])
        self.assertEqual(row['bonds'][0]['changes']['1']['value'],100.1)
        del crwv['cds_validation_warning']
        self.assertEqual(model(cfg,watch,TODAY)['issuers'][0]['cds']['last'],440)

    def test_convertibles_are_explicit(self):
        c=self.view()['issuers'][2]
        self.assertEqual(c['bonds'][0]['board']['kind'],'convertible')
        self.assertIn('(convertible)',c['bonds'][0]['label'])

    def test_flat_spread_stays_on_its_own_basis(self):
        wb={'refreshed_at':'2026-10-14T09:34','cds':[{'name':'ORCL CDS 5Y','bbg':'ORCLCP CDS USD SR 5Y D14 Corp',
            'spread_bp':320.0,'spread_snapshot_bp':300.0,'d_snapshot_bp':20.0,'ms_desk_0824_bp':217.0,'d_vs_ms_bp':103.0}]}
        hist=[{'kind':'cds','id':'ORCLCP CDS USD SR 5Y D14 Corp','date':'2026-10-13','time':'09:34','spread':300.0},
              {'kind':'cds','id':'ORCLCP CDS USD SR 5Y D14 Corp','date':'2026-10-13','time':'18:34','spread':310.0},
              {'kind':'cds','id':'ORCLCP CDS USD SR 5Y D14 Corp','date':'2026-10-14','time':'09:34','spread':320.0},
              {'kind':'bond','id':'ORCLCP CDS USD SR 5Y D14 Corp','date':'2026-10-14','time':'09:34','spread':1.0}]
        watch={'series':[{'id':'ORCL_CDS5Y','points':[['2026-10-13',240],['2026-10-14',245]]}]}
        rows={c['id']:c for c in model(self.config(),watch,TODAY,workbook=wb,history=hist)['issuers']}
        f=rows['ORCL']['flat']
        self.assertEqual((f['last'],f['field'],f['msDesk']),(320.0,'CDS_FLAT_SPREAD',217.0))
        self.assertEqual(f['points'],[('2026-10-13',310.0),('2026-10-14',320.0)])  # last pull of the day
        carried=model(self.config(),watch,TODAY,workbook=wb,history=hist+[
            {'kind':'cds','id':'ORCLCP CDS USD SR 5Y D14 Corp','date':'2026-10-15','time':'09:34','spread':320.0}])
        self.assertEqual(next(c for c in carried['issuers'] if c['id']=='ORCL')['flat']['markDate'],'2026-10-14')
        self.assertEqual(f['change1']['value'],10)
        self.assertEqual(rows['ORCL']['cds']['last'],245)  # board PX_LAST untouched
        self.assertIsNone(rows['CRWV']['flat'])

    def test_identical_cds_histories_are_flagged(self):
        cfg={'board':{'issuers':[{'company':c,'name':c,'tier':'hyperscaler · IG','cds':c+' CDS','bonds':[]} for c in ('META','GOOGL','MSFT')]}}
        same=[[f'2026-09-{d:02d}',22.5+d] for d in range(1,13)]
        watch={'series':[{'id':'META_CDS5Y','points':same},{'id':'GOOGL_CDS5Y','points':same},
                         {'id':'MSFT_CDS5Y','points':[[d,v+1] for d,v in same]}]}
        twins=model(cfg,watch,TODAY)['twins']
        self.assertEqual([sorted(t['pair']) for t in twins],[['GOOGL','META']])
        self.assertEqual((twins[0]['days'],twins[0]['first']),(12,'2026-09-01'))

    def test_one_day_cds_step_is_flagged(self):
        cfg={'board':{'issuers':[{'company':'ORCL','name':'Oracle','tier':'hyperscaler · IG (BBB)','cds':'X','bonds':[]}]}}
        watch={'series':[{'id':'ORCL_CDS5Y','points':[['2026-08-10',88.433],['2026-08-11',203.433],['2026-08-12',210]]}]}
        steps=model(cfg,watch,TODAY)['steps']
        self.assertEqual([(s['id'],s['to'][0]) for s in steps],[('ORCL','2026-08-11')])

    def test_script_data_cannot_break_out(self):
        text=json_script({'name':'</script><script>alert(1)</script>'})
        self.assertNotIn('<',text)
        self.assertIn('\\u003c',text)


if __name__ == '__main__':
    unittest.main()
