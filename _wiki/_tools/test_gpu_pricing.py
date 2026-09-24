"""Data integrity checks for the two GPU pricing feeds; no live connections."""
import copy
import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

import gpu_pricing as gp


class PricingDataTests(unittest.TestCase):
    def payload(self):
        return {'status': 'ok', 'index': [
            {'date': '2026-09-21', 'h100': 3.29, 'a100': 1.85, 'b200': None},
            {'date': '2026-09-22', 'h100': 3.29, 'a100': None, 'b200': 5.76}],
            'contract': [{'sku': 'H100', 'data': [
                {'period': 'Aug 2026', 'period_start': '2026-08-01', '1y': [2.4, 3.2], 'onDemand': None}],
                'soldOutPeriods': {'onDemand': ['Aug 2026']}}]}

    def test_nulls_and_sold_out_are_not_zero_prices(self):
        data = gp.normalize_public(self.payload(), '2026-09-23')
        self.assertEqual(data['series'][1]['points'], [['2026-09-21', 1.85]])
        self.assertTrue(data['contracts'][0]['sold_out'])
        self.assertIsNone(data['contracts'][0]['on_demand'])

    def test_missing_contract_period_not_interpolated(self):
        payload = self.payload()
        payload['contract'][0]['data'].append({'period': 'Sep 2026', 'period_start': '2026-09-01'})
        self.assertIsNone(gp.normalize_public(payload, 'now')['contracts'][-1]['one_year'])

    def test_reject_bad_prices_ranges_and_duplicate_days(self):
        for bad in [float('nan'), float('inf'), 0, -1, True]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                gp.positive(bad)
        payload = self.payload(); payload['contract'][0]['data'][0]['1y'] = [3.2, 2.4]
        with self.assertRaises(ValueError): gp.normalize_public(payload, 'now')
        payload = self.payload(); payload['index'].append({**payload['index'][0], 'h100': 5})
        with self.assertRaises(ValueError): gp.normalize_public(payload, 'now')

    def test_reject_future_dates(self):
        with self.assertRaises(ValueError): gp.source_date('2099-01-01')

    def test_merge_retains_failed_instruments_and_applies_revisions(self):
        old = [{'id': 'a', 'points': [['2026-09-21', 2], ['2026-09-22', 3]]},
               {'id': 'b', 'points': [['2026-09-22', 8]]}]
        fresh = [{'id': 'a', 'points': [['2026-09-22', 4], ['2026-09-23', 5]]}]
        merged = gp.merge_series(old, fresh)
        self.assertEqual(merged[0]['points'], [['2026-09-21', 2], ['2026-09-22', 4], ['2026-09-23', 5]])
        self.assertEqual(merged[1], old[1])
        self.assertEqual(old[0]['points'][-1][1], 3)
        with self.assertRaises(ValueError):
            gp.merge_series(old, [{'id': 'a', 'points': [['2026-09-20', 1]]}])

    def test_bbg_partial_response_and_entitlement_failure(self):
        history = [{'securityData': {'security': 'SDH100RT Index', 'fieldData': [{'date': '2026-09-21', 'PX_LAST': 2.6}]}},
                   {'securityData': {'security': 'SDH100RT Index', 'fieldData': [{'date': '2026-09-22', 'PX_LAST': 2.61}]}},
                   {'securityData': {'security': 'SDA100RT Index', 'securityError': {'message': 'Not entitled'}}}]
        series, errors = gp.normalize_bbg(history, [], 'now')
        self.assertEqual(len(series[0]['points']), 2)
        self.assertEqual(len(errors), 3)
        self.assertTrue(any('Not entitled' in err for err in errors))

    def test_failed_refresh_preserves_last_good_files(self):
        with TemporaryDirectory() as tmp, patch.object(gp, 'ROOT', Path(tmp)):
            gp.write(gp.ROOT/'bloomberg.json', {'series': [{'id': 'old', 'points': [['2026-09-22', 2.6]]}]})
            gp.write(gp.ROOT/'semianalysis.json', {'series': [], 'contracts': []})
            before = (gp.ROOT/'bloomberg.json').read_bytes()
            with patch.object(gp, 'fetch_bbg', side_effect=ConnectionError('Terminal offline')), patch.object(gp, 'fetch_public', side_effect=ValueError('Invalid public feed')):
                errors = gp.refresh()
            self.assertEqual(len(errors), 2)
            self.assertEqual((gp.ROOT/'bloomberg.json').read_bytes(), before)
            self.assertEqual(len(gp.read(gp.ROOT/'status.json')['errors']), 2)


if __name__ == '__main__':
    unittest.main()
