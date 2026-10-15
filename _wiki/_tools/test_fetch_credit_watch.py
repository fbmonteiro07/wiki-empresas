"""Bounded recovery tests. Bloomberg is mocked; no market data requests are sent."""
import contextlib
import io
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import fetch_credit_watch as fetch


def row(sid, ticker):
    return {'id': sid, 'label': sid, 'group': 'bond', 'company': sid,
            'unit': '%', 'field': 'YLD_YTM_MID', 'candidates': [ticker],
            'board': {'issuer': sid}, 'rules': {}}


class CreditFetchRecoveryTests(unittest.TestCase):
    def run_fetch(self, instruments, previous, args, points=None, error=None):
        bdh, bdp = Mock(), Mock()
        if error:
            bdh.side_effect = error
        config = {'instruments': instruments, 'history_days': 400}
        snapshot = Mock(return_value={})
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            config_path, output = path/'config.json', path/'watch.json'
            config_path.write_text(json.dumps(config), encoding='utf-8')
            original = json.dumps(previous)
            output.write_text(original, encoding='utf-8')
            with patch.object(fetch, 'CONFIG', config_path), patch.object(fetch, 'OUT', output), \
                 patch.object(fetch, 'frame_points', return_value=points or []), \
                 patch.object(fetch, 'bond_snapshot', snapshot), \
                 patch.dict(sys.modules, {'bloomberg': types.SimpleNamespace(bdh=bdh, bdp=bdp)}), \
                 patch.object(sys, 'argv', ['fetch_credit_watch.py'] + args), \
                 contextlib.redirect_stdout(io.StringIO()):
                code = fetch.main()
            saved = output.read_text(encoding='utf-8')
        return code, saved, original, bdh, snapshot

    def test_block_stops_after_one_request_and_retains_old_history(self):
        prior = {'series': [{'id':'A','ticker':'A Corp','status':'ok',
                            'points':[['2026-10-13',5.1]],'fetched_at':'2026-10-13T18:00:00'}]}
        code, saved, _, bdh, snapshot = self.run_fetch(
            [row('A','A Corp'), row('B','B Corp')], prior, [],
            error=RuntimeError('LIMIT / WORKFLOW_REVIEW_NEEDED / Workflow review needed'))
        data = json.loads(saved)
        self.assertEqual(code,1)
        self.assertEqual(bdh.call_count,1)
        self.assertEqual(data['bbg_status']['state'],'blocked')
        self.assertEqual(data['series'][0]['points'],prior['series'][0]['points'])
        self.assertEqual(data['series'][0]['status'],'stale')
        snapshot.assert_not_called()

    def test_probe_with_no_observations_fails_without_writing(self):
        code, saved, original, _, snapshot = self.run_fetch([row('A','A Corp')], {'series':[]}, ['--probe'])
        self.assertEqual(code,1)
        self.assertEqual(saved,original)
        snapshot.assert_not_called()

    def test_targeted_refresh_only_snapshots_newly_fetched_bond(self):
        old = {'id':'B','ticker':'B Corp','group':'bond','board':{'issuer':'B'},
               'status':'ok','points':[['2026-10-13',6.2]]}
        code, saved, _, bdh, snapshot = self.run_fetch(
            [row('A','A Corp'),row('B','B Corp')], {'series':[old]}, ['--ids','A'],
            points=[('2026-10-14',5.1)])
        self.assertEqual(code,0)
        self.assertEqual(bdh.call_count,1)
        self.assertEqual(snapshot.call_args.args[1],['A Corp'])
        self.assertEqual(json.loads(saved)['series'][1],old)

    def test_single_valid_quote_is_displayed_with_short_history(self):
        code, saved, _, _, _ = self.run_fetch([row('A','A Corp')], {'series':[]}, [],
                                               points=[('2026-10-14',5.1)])
        self.assertEqual(code,0)
        self.assertEqual(json.loads(saved)['series'][0]['last'],5.1)

    def test_unknown_id_does_not_report_success(self):
        code, saved, original, bdh, snapshot = self.run_fetch(
            [row('A','A Corp')], {'series':[]}, ['--ids','MISSING'])
        self.assertEqual(code,2)
        self.assertEqual(saved,original)
        bdh.assert_not_called()
        snapshot.assert_not_called()


if __name__ == '__main__':
    unittest.main()
