"""Calendar comparisons for the GPU pricing table; no network."""
import unittest

from build_gpu_pricing import price_changes


class PriceChangeTests(unittest.TestCase):
    def test_week_and_calendar_month_have_distinct_baselines(self):
        changes = price_changes([
            ['2026-08-25', 4], ['2026-08-26', 8],
            ['2026-09-18', 5], ['2026-09-25', 6],
        ])
        self.assertAlmostEqual(changes['wow']['pct'], 20)
        self.assertEqual(changes['wow']['delta'], 1)
        self.assertAlmostEqual(changes['mom']['pct'], 50)
        self.assertEqual(changes['mom']['date'], '2026-08-25')

    def test_month_end_and_leap_year(self):
        for year, feb_end in [(2024, 29), (2025, 28)]:
            with self.subTest(year=year):
                before = f'{year}-02-{feb_end}'
                change = price_changes([[before, 2], [f'{year}-03-31', 3]])['mom']
                self.assertEqual(change['date'], before)
                self.assertEqual(change['pct'], 50)
        year_boundary = price_changes([['2025-12-31', 2], ['2026-01-31', 1]])['mom']
        self.assertEqual(year_boundary['pct'], -50)

    def test_missing_dates_never_use_a_future_baseline(self):
        change = price_changes([
            ['2026-09-15', 2], ['2026-09-19', 4], ['2026-09-25', 3],
        ])['wow']
        self.assertEqual(change['date'], '2026-09-15')
        self.assertEqual(change['target'], '2026-09-18')
        self.assertEqual(change['days'], 10)
        self.assertEqual(change['pct'], 50)

    def test_no_comparison_across_long_gaps_or_short_histories(self):
        self.assertIsNone(price_changes([['2026-09-14', 2], ['2026-09-25', 3]])['wow'])
        self.assertEqual(price_changes([['2026-09-25', 3]]), {'wow': None, 'mom': None})
        self.assertEqual(price_changes([]), {'wow': None, 'mom': None})

    def test_decreases_flat_prices_and_unsorted_inputs(self):
        changes = price_changes([['2026-09-25', 2], ['2026-08-25', 2], ['2026-09-18', 4]])
        self.assertEqual(changes['wow']['pct'], -50)
        self.assertEqual(changes['wow']['delta'], -2)
        self.assertEqual(changes['mom']['pct'], 0)
        self.assertEqual(changes['mom']['delta'], 0)


if __name__ == '__main__':
    unittest.main()
