"""Checks for stale data, unit errors, lookback gaps and failed refreshes."""
import contextlib
import datetime as dt
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

import fetch_funding
from funding_common import change, market_health, observations
from refresh_credit_monitor import summary

TODAY = dt.date(2026, 9, 29)


class CreditMonitorTests(unittest.TestCase):
    def series(self, **extra):
        return {'ticker': 'TEST Index', 'label': 'Test OAS', 'unit': '%',
                'points': [['2026-09-18', 2.0], ['2026-09-21', 2.1], ['2026-09-28', 2.5]], **extra}

    def test_weekly_change_keeps_actual_dates_and_bp_units(self):
        result = change(self.series(), 7, TODAY)
        self.assertEqual(result, {'value': 40.0, 'unit': 'bp', 'start': '2026-09-21', 'end': '2026-09-28'})

    def test_bond_price_change_not_scaled_to_basis_points(self):
        result = change(self.series(unit='price'), 7, TODAY)
        self.assertAlmostEqual(result['value'], .4)
        self.assertEqual(result['unit'], 'price')

    def test_sparse_history_is_unavailable_not_zero(self):
        s = self.series(points=[['2026-08-01', 2.0], ['2026-09-28', 2.5]])
        self.assertIsNone(change(s, 7, TODAY))

    def test_holiday_baseline_within_tolerance(self):
        s = self.series(points=[['2026-09-18', 2.0], ['2026-09-28', 2.5]])
        self.assertEqual(change(s, 7, TODAY)['start'], '2026-09-18')

    def test_invalid_and_future_observations_excluded(self):
        s = self.series(points=[['2026-09-28', 2.0], ['2026-09-28', 2.5],
                                ['bad-date', 7], ['2026-09-30', 9], ['2026-09-29', float('nan')]])
        self.assertEqual(observations(s, TODAY), [('2026-09-28', 2.5)])

    def test_missing_instrument_and_staleness_flagged(self):
        config = {'market_series': [{'ticker': 'TEST Index'}, {'ticker': 'MISSING'}]}
        market = {'series': [self.series(points=[['2026-09-18', 2]])]}
        result = market_health(market, config, TODAY)
        self.assertFalse(result['ok'])
        self.assertEqual(len(result['issues']), 2)

    def test_failed_fetch_preserves_last_valid_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            config = folder / 'config.json'
            config.write_text(json.dumps({'market_series': [{'ticker': 'TEST Index'}]}))
            output = folder / 'market.json'
            previous = b'{"old": "must survive"}'
            output.write_bytes(previous)
            def failed(*args):
                raise RuntimeError('Terminal unavailable')
            with patch.object(fetch_funding, 'DEALS', config), patch.object(fetch_funding, 'OUT', output), \
                 patch.dict('sys.modules', {'bloomberg': types.SimpleNamespace(bdh=failed)}), \
                 contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(fetch_funding.main(), 1)
            self.assertEqual(output.read_bytes(), previous)

    def test_first_brief_not_claimed_as_new_deals(self):
        config = {'asof': '2026-08-24', 'market_series': [{'ticker': 'TEST Index'}], 'deals': []}
        body = summary(config, {'series': [self.series()]}, today=TODAY)
        self.assertIn('Initial retained baseline', body)
        self.assertIn('Research ledger as of 2026-08-24', body)
        self.assertIn('Bloomberg TEST Index', body)


if __name__ == '__main__':
    unittest.main()
