import os
import sys
import unittest
import logging

current = os.path.dirname(os.path.abspath(__file__))
while current and current != os.path.dirname(current):
    if os.path.isdir(os.path.join(current, "src")):
        sys.path.insert(0, current)
        break
    current = os.path.dirname(current)

from src.analytics.ratios import (
    compute_net_profit_margin,
    compute_operating_profit_margin,
    compute_return_on_equity,
    compute_roce,
    compute_return_on_assets,
    compute_debt_to_equity,
    compute_interest_coverage_ratio,
    compute_asset_turnover
)

class TestFinancialRatios(unittest.TestCase):
    def setUp(self):
        if not os.path.exists("output"):
            os.makedirs("output")

    def test_npm_normal(self):
        self.assertEqual(compute_net_profit_margin(15, 100), 15.0)

    def test_npm_zero_sales(self):
        self.assertIsNone(compute_net_profit_margin(15, 0))

    def test_opm_mismatch_logging(self):
        logging.getLogger().setLevel(logging.INFO)
        with self.assertLogs(level="INFO") as log_capture:
            compute_operating_profit_margin(20, 100, source_opm_pct=15.0, company_id="TEST_CO")
            self.assertTrue(any("OPM Mismatch" in line for line in log_capture.output))

    def test_roe_normal(self):
        self.assertEqual(compute_return_on_equity(20, 100, 0), 20.0)

    def test_roe_negative_equity(self):
        self.assertIsNone(compute_return_on_equity(20, -50, 10))

    def test_roce_financials_sector(self):
        with self.assertLogs(level="INFO") as log_capture:
            compute_roce(30, 40, 40, 20, broad_sector="Financials", company_id="BANK_CO")
            self.assertTrue(any("Financials sector detected" in line for line in log_capture.output))

    def test_roa_zero_assets(self):
        self.assertIsNone(compute_return_on_assets(10, 0))

    def test_de_debt_free(self):
        ratio, flag = compute_debt_to_equity(0, 50, 50)
        self.assertEqual(ratio, 0.0)
        self.assertFalse(flag)

    def test_de_high_leverage_flag(self):
        ratio, flag = compute_debt_to_equity(600, 50, 50, broad_sector="Infra")
        self.assertGreater(ratio, 5.0)
        self.assertTrue(flag)

    def test_de_high_leverage_financials_suppressed(self):
        ratio, flag = compute_debt_to_equity(600, 50, 50, broad_sector="Financials")
        self.assertFalse(flag)

    def test_icr_debt_free(self):
        val, label, warning = compute_interest_coverage_ratio(50, 10, 0)
        self.assertIsNone(val)
        self.assertEqual(label, "Debt Free")
        self.assertFalse(warning)

    def test_icr_warning_flag(self):
        val, label, warning = compute_interest_coverage_ratio(2, 2, 10)
        self.assertLess(val, 1.5)
        self.assertTrue(warning)

    def test_asset_turnover_zero_assets(self):
        self.assertIsNone(compute_asset_turnover(100, 0))

if __name__ == "__main__":
    unittest.main()