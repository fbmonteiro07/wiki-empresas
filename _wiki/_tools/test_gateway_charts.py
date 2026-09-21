"""Checks the data decisions that could manufacture misleading chart signals."""
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
import gateway_charts as gc


class ChartTests(unittest.TestCase):
    def test_exact_week_takes_priority_over_adhoc(self):
        snapshots = [{'date': '2026-09-13'}, {'date': '2026-09-18'}, {'date': '2026-09-20'}]
        self.assertEqual(gc.baseline(snapshots, snapshots[-1])['date'], '2026-09-13')
        self.assertIsNone(gc.baseline(snapshots, {'date': '2026-10-20'}))

    def test_nearest_baseline_and_zero_denominator(self):
        self.assertEqual(gc.baseline([{'date':'2026-09-12'},{'date':'2026-09-15'}], {'date':'2026-09-20'})['date'], '2026-09-12')
        self.assertIsNone(gc.pct(10,0))
        self.assertAlmostEqual(gc.pct(90,100), -10.0)

    def snapshot_fixture(self, folder, duplicate=False):
        # The earlier bucket must still contribute; variants must not merge.
        rows = [{'model_permaslug':'deepseek/test','variant':'standard','date':'2026-09-18 00:00:00','total_prompt_tokens':60,'total_completion_tokens':10},
                {'model_permaslug':'deepseek/test','variant':'free','date':'2026-09-20 00:00:00','total_prompt_tokens':20,'total_completion_tokens':10}]
        if duplicate:
            rows.append(dict(rows[0], date='2026-09-19 00:00:00'))
        (folder/'rank_week.json').write_text(json.dumps({'data':rows}))
        (folder/'catalog.json').write_text(json.dumps({'data':[{'permaslug':'deepseek/test','author':'deepseek','short_name':'Test'}]}))

    def test_full_window_and_separate_variants(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.snapshot_fixture(Path(tmp))
            s = gc.parse_snapshot(Path(tmp))
            self.assertEqual((s['total'],s['standard'],s['free']),(100,70,30))
            self.assertEqual(len(s['models']),2)
            self.assertEqual(s['labs']['deepseek'],100)
            self.assertEqual(s['date'],'2026-09-20')

    def test_duplicates_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.snapshot_fixture(Path(tmp),True)
            with self.assertRaisesRegex(ValueError,'Duplicate'):
                gc.parse_snapshot(Path(tmp))

    def test_missing_is_gap_not_zero_or_connected(self):
        c = {'title':'Test <safe>', 'unit':'%', 'series':[gc.point_series('deepseek','A & B',['2026-09-01','2026-09-02','2026-09-03'],[10,None,30])]}
        svg = gc.line_svg(c)
        root = ET.fromstring(svg)
        ns = {'s':'http://www.w3.org/2000/svg'}
        self.assertEqual(len(root.findall('s:polyline',ns)),2)
        self.assertEqual(len(root.findall('s:circle',ns)),2)
        self.assertIn('n/a',gc.table(dict(c,kind='line')))

    def test_signed_movers_and_safe_labels(self):
        rows = [{'name':'<model & variant>', 'value':2}, {'name':'loser','value':-3}, {'name':'flat','value':0}]
        selected = gc.extremes(rows)
        self.assertEqual([r['value'] for r in selected],[2,-3])
        svg = gc.bars_svg({'title':'Movers','kind':'bars','unit':'pp','signed':True,'rows':selected})
        root = ET.fromstring(svg)
        rects = root.findall('{http://www.w3.org/2000/svg}rect')
        self.assertTrue(all(float(r.attrib['width']) >= 0 for r in rects))
        self.assertIn('&lt;model &amp; variant&gt;',svg)


if __name__ == '__main__':
    unittest.main()
