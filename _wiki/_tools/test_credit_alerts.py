"""Rule-engine checks for credit_alerts.py: units, sigma, highs, level lines, mail proximity, de-dup inputs."""
import datetime as dt
import json
import unittest
from pathlib import Path

import credit_alerts as ca

CFG = json.loads((Path(__file__).resolve().parents[1] / "_data" / "credit_watch_config.json").read_text(encoding="utf-8"))


def mk(vals, group="cds", unit="bp", start=dt.date(2026, 7, 1), rules=None, sid="X"):
    pts, d = [], start
    for v in vals:
        while d.weekday() >= 5:
            d += dt.timedelta(days=1)
        pts.append([d.isoformat(), v]); d += dt.timedelta(days=1)
    return {"id": sid, "label": sid, "group": group, "unit": unit, "points": pts, "status": "ok", "rules": rules or {}}


class MarketRules(unittest.TestCase):
    def test_cds_blowout_is_high(self):
        base = [850 + (i % 3) * 4 - 4 for i in range(70)]            # quiet ±4bp
        s = mk(base + [1010], rules={"d1_abs": 50, "d1_z": 2.5, "d5_abs": 150, "high_60d": True, "high_1y": True})
        st = ca.series_stats(s)
        self.assertAlmostEqual(st["d1"], 1010 - base[-1])
        self.assertGreater(st["z1"], 2.5)
        sev, reasons = ca.evaluate(st, s["rules"])
        self.assertEqual(sev, "high")
        self.assertTrue(any("60-day high" in r for r in reasons))

    def test_quiet_series_is_none(self):
        s = mk([850 + (i % 3) * 4 - 4 for i in range(70)], rules={"d1_abs": 50, "d1_z": 2.5})
        self.assertEqual(ca.evaluate(ca.series_stats(s), s["rules"])[0], "none")

    def test_tightening_does_not_fire(self):
        base = [850 + (i % 3) * 4 - 4 for i in range(70)]
        s = mk(base + [700], rules={"d1_abs": 50, "d1_z": 2.5})
        self.assertEqual(ca.evaluate(ca.series_stats(s), s["rules"])[0], "none")

    def test_oas_pct_series_changes_in_bp(self):
        base = [3.00 + (i % 2) * 0.01 for i in range(70)]
        s = mk(base + [3.30], group="index", unit="%", rules={"d1_abs": 15, "d1_z": 2.5})
        st = ca.series_stats(s)
        self.assertAlmostEqual(st["d1"], (3.30 - base[-1]) * 100, places=6)
        self.assertEqual(st["alert_unit"], "bp")
        self.assertEqual(ca.evaluate(st, s["rules"])[0], "high")

    def test_equity_down_move_fires_up_move_does_not(self):
        base = [100 * (1.002 ** i) for i in range(70)]
        down = mk(base + [base[-1] * 0.92], group="equity", unit="%", rules={"d1_abs": 6, "d1_z": 2.5})
        up = mk(base + [base[-1] * 1.08], group="equity", unit="%", rules={"d1_abs": 6, "d1_z": 2.5})
        self.assertEqual(ca.evaluate(ca.series_stats(down), down["rules"])[0], "high")
        self.assertEqual(ca.evaluate(ca.series_stats(up), up["rules"])[0], "none")
        self.assertAlmostEqual(ca.series_stats(down)["d1"], -8.0, places=6)

    def test_level_line_cross_is_high_even_on_small_move(self):
        base = [780 + (i % 3) * 4 - 4 for i in range(70)]
        s = mk(base + [805], rules={"d1_abs": 50, "d1_z": 2.5, "level_line": 800})
        st = ca.series_stats(s)
        self.assertEqual(st["line_cross"], "up")
        self.assertEqual(ca.evaluate(st, s["rules"])[0], "high")

    def test_slow_bleed_five_obs(self):
        base = [850 + (i % 3) * 4 - 4 for i in range(70)]
        s = mk(base + [880, 910, 945, 975, 1000], rules={"d1_abs": 50, "d1_z": 2.5, "d5_abs": 120})
        sev, reasons = ca.evaluate(ca.series_stats(s), s["rules"])
        self.assertIn(sev, ("medium", "high"))
        self.assertTrue(any("5-obs" in r for r in reasons))

    def test_short_history_has_no_sigma_and_no_crash(self):
        s = mk([850, 860, 1010], rules={"d1_abs": 50, "d1_z": 2.5})
        st = ca.series_stats(s)
        self.assertIsNone(st["sigma"])
        self.assertEqual(ca.evaluate(st, s["rules"])[0], "medium")   # abs trigger alone = medium

    def test_asof_excludes_later_observations(self):
        s = mk([850] * 70 + [1010], rules={"d1_abs": 50, "d1_z": 2.5})
        st = ca.series_stats(s, asof_iso=s["points"][-2][0])
        self.assertEqual(st["last"], 850)


class MailRules(unittest.TestCase):
    def mails(self):
        return [
            {"id": "m1", "subject": "TMT Daily | Rothschild & Co - CRWV debt selloff, ASML", "sender": "tmtspecsales@spec-sales.gms.rothschildandco.com",
             "sender_name": "Rowan & George", "date": "2026-10-14T07:58:56Z",
             "body": "What caught our eye? CoreWeave's CDS is back to late July high's of c1000 bp as bonds continue to sell off. Market colour: SOX -23bps."},
            {"id": "m2", "subject": "GS - What Matters Today", "sender": "nelson.armbrust@gs.com", "sender_name": "Armbrust, Nelson", "date": "2026-10-14T12:12:24Z",
             "body": "CRWV -4% on social media focus on bond yields spiking (Chamath warned of a private credit bubble)."},
            {"id": "m3", "subject": "Meta launches glasses", "sender": "x@y.com", "sender_name": "X", "date": "2026-10-14T10:00:00Z",
             "body": "Meta's new glasses cost $349. Elsewhere, a CDS index was flat."},
            {"id": "m4", "subject": "Sentiment Radar | 2026-10-14", "sender": "felipe.monteiro@capstone.com.br", "sender_name": "Felipe", "date": "2026-10-14T13:00:00Z",
             "body": "CoreWeave CDS widening noted by desks."},
        ]

    def test_hits_and_grouping(self):
        hits = ca.mail_hits(CFG["mail"], self.mails(), set())
        comps = {(h["id"], h["company"]) for h in hits}
        self.assertIn(("m1", "CRWV"), comps)
        self.assertIn(("m2", "CRWV"), comps)
        self.assertNotIn(("m4", "CRWV"), comps)           # our own automated mail is ignored
        self.assertTrue(any(h["id"] == "m1" and h["in_subject"] for h in hits))
        narr = ca.narrative_layer(CFG["mail"], hits)
        crwv = next(n for n in narr if n["company"] == "CRWV")
        self.assertEqual(crwv["severity"], "high")        # subject-level hit + 2 firms
        self.assertEqual(sorted(crwv["firms"]), ["Goldman Sachs", "Rothschild & Co"])
        meta = [n for n in narr if n["company"] == "META"]
        self.assertEqual(meta, [])                         # one weak mention, META needs 2 firms

    def test_seen_ids_are_skipped(self):
        hits = ca.mail_hits(CFG["mail"], self.mails(), {"m1", "m2"})
        self.assertFalse(any(h["company"] == "CRWV" for h in hits))


if __name__ == "__main__":
    unittest.main()
