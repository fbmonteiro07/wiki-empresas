"""Economic invariants for the token study, with deliberately adversarial data."""
import json
from pathlib import Path
import tempfile
import unittest
from or_token_economics import digest, indexes, collect


def model(mid='lab/model', canonical='lab/model-20260101', pin='0.000002', pout='0.000008', hf='lab/weights'):
    return {'id': mid, 'canonical_slug': canonical, 'hugging_face_id': hf,
            'architecture': {'output_modalities': ['text']},
            'pricing': {'prompt': pin, 'completion': pout, 'input_cache_read': '0.0000002'}}


def row(slug='lab/model-20260101', tag='standard', pin=3000000, pout=1000000):
    return {'model_permaslug': slug, 'variant': tag, 'date': '2026-09-27 00:00:00',
            'total_prompt_tokens': pin, 'total_completion_tokens': pout}


class TokenEconomicsTests(unittest.TestCase):
    def point(self, models, rows, catalog=None):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / 'openrouter/raw/2026-09-28'
            folder.mkdir(parents=True)
            for name, data in [('models', models), ('rank_week', rows), ('catalog', catalog or [])]:
                (folder / (name + '.json')).write_text(json.dumps({'data': data}))
            return digest(folder)

    def test_spend_and_weighted_price_use_actual_mix(self):
        p = self.point([model()], [row()])
        self.assertAlmostEqual(p['buckets']['total']['spend'], 14)
        self.assertAlmostEqual(p['buckets']['total']['wap'], 3.5)
        self.assertAlmostEqual(p['average']['blend'], 5)
        self.assertAlmostEqual(p['buckets']['total']['cache50'], 11.3)

    def test_catalogue_average_includes_no_volume_models(self):
        p = self.point([model(), model('lab/unused', 'lab/unused', '0.000004', '0.000012')], [row()])
        self.assertEqual(p['average']['models'], 2)
        self.assertAlmostEqual(p['average']['blend'], 6.5)
        self.assertAlmostEqual(p['buckets']['total']['wap'], 3.5)

    def test_free_alias_does_not_contaminate_standard_price(self):
        p = self.point([model(), model('lab/model:free', pin='0', pout='0')], [row(), row(tag='free')])
        self.assertAlmostEqual(p['buckets']['total']['spend'], 14)
        self.assertAlmostEqual(p['buckets']['total']['wap'], 1.75)
        self.assertAlmostEqual(p['average']['blend'], 5)

    def test_negative_price_is_missing_not_zero(self):
        p = self.point([model(pin='-1')], [row()])
        self.assertIsNone(p['buckets']['total']['spend'])
        self.assertIsNone(p['buckets']['total']['wap'])
        self.assertEqual(p['buckets']['total']['coverage_pct'], 0)

    def test_batch_without_exact_price_is_not_standard(self):
        p = self.point([model()], [row(), row(tag='batch')])
        self.assertEqual(p['buckets']['total']['coverage_pct'], 50)
        self.assertAlmostEqual(p['buckets']['total']['spend'], 14)

    def test_missing_price_does_not_dilute_wap(self):
        p = self.point([model()], [row(), row(slug='missing/model')])
        self.assertEqual(p['buckets']['total']['coverage_pct'], 50)
        self.assertAlmostEqual(p['buckets']['total']['wap'], 3.5)
        self.assertEqual(p['buckets']['unknown']['tokens'], 4000000)

    def test_classification_uses_the_given_vintage(self):
        old = self.point([model(hf=None)], [row()])
        new = self.point([model(hf='lab/weights')], [row()])
        self.assertEqual(old['buckets']['closed']['tokens'], 4000000)
        self.assertEqual(new['buckets']['open']['tokens'], 4000000)

    def test_duplicate_rows_fail_closed(self):
        with self.assertRaises(ValueError):
            self.point([model()], [row(), row()])

    def test_ambiguous_alias_not_arbitrarily_priced(self):
        p = self.point([model(), model('lab/alias', pin='0.000010')], [row()])
        self.assertIsNone(p['buckets']['total']['spend'])

    def test_nonfinite_tokens_rejected(self):
        with self.assertRaises(ValueError):
            self.point([model()], [row(pin=float('inf'))])

    def test_stale_duplicate_window_keeps_earliest_prices(self):
        with tempfile.TemporaryDirectory() as temp:
            wiki=Path(temp)
            root=wiki/'_data/openrouter'
            for date,price in [('2026-09-28','0.000002'),('2026-09-29','0.000100')]:
                folder=root/'raw'/date
                folder.mkdir(parents=True)
                for name,data in [('models',[model(pin=price)]),('catalog',[]),('rank_week',[row()])]:
                    (folder/(name+'.json')).write_text(json.dumps({'data':data}))
            (root/'latest.txt').write_text('2026-09-29')
            report=collect(wiki)
            self.assertEqual(len(report['history']),1)
            self.assertEqual(report['latest_snapshot'],'2026-09-28')
            self.assertAlmostEqual(report['history'][0]['buckets']['total']['spend'],14)
            self.assertTrue(any('duplicate window' in w for w in report['warnings']))

    def test_raw_usage_is_retained_without_claiming_dollars(self):
        free=row(tag='free')
        free['total_usage']=7.25
        p=self.point([model()],[row(),free])
        self.assertEqual(p['raw_diagnostics']['total_usage_raw_sum'],7.25)
        self.assertEqual(p['raw_diagnostics']['positive_usage_free_rows'],1)
        self.assertAlmostEqual(p['buckets']['total']['spend'],14)


if __name__ == '__main__':
    unittest.main()
