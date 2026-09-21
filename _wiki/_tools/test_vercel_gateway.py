import datetime as dt
import unittest
import vercel_gateway as vg

class ShareTests(unittest.TestCase):
    def payload(self,missing=None):
        rows=[]
        for n in range(14):
            for metric in vg.METRICS:
                if n==missing: continue
                rows.append({'date':(dt.date(2026,9,1)+dt.timedelta(days=n)).isoformat(),'name':'Example','metric':metric,'modality':'all','share_percent':10 if n<7 else 20})
        return {'dataset':'models','rows':rows}

    def test_weekly_pp_change(self):
        row=vg.summarize(self.payload(),'2026-09-14')['tokens'][0]
        self.assertEqual((row['mean_7d'],row['previous_mean_7d'],row['change_pp']),(20,10,10))

    def test_missing_is_not_zero(self):
        row=vg.summarize(self.payload(missing=8),'2026-09-14')['tokens'][0]
        self.assertIsNone(row['mean_7d']);self.assertIsNone(row['change_pp']);self.assertEqual(row['days'],6)

    def test_missing_previous_suppresses_change(self):
        row=vg.summarize(self.payload(missing=1),'2026-09-14')['tokens'][0]
        self.assertEqual(row['mean_7d'],20);self.assertIsNone(row['change_pp'])

    def test_duplicate_rejected(self):
        p=self.payload();p['rows'].append(p['rows'][0])
        with self.assertRaises(ValueError):vg.validate(p,'models')

    def test_invalid_share_rejected(self):
        for value in (-1,101,float('nan')):
            p=self.payload();p['rows'][0]['share_percent']=value
            with self.assertRaises(ValueError):vg.validate(p,'models')

if __name__=='__main__': unittest.main()
