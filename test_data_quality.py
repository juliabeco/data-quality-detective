
import unittest
import pandas as pd

import data_quality as dq


class TestDataQuality(unittest.TestCase):

    def setUp(self):
        self.valid_df = pd.DataFrame({
            "customer_id": [201, 202],
            "age": [25, 40],
            "city": ["Valencia", "Madrid"],
            "monthly_spend": [30.0, 55.0]
        })

    def test_valid_dataset_has_no_issues(self):
        issues = dq.validate_data(self.valid_df)
        self.assertTrue(issues.empty)

    def test_empty_dataset_has_no_issues(self):
        empty_df = pd.DataFrame(columns=[
            "customer_id", "age", "city", "monthly_spend"
        ])

        issues = dq.validate_data(empty_df)
        self.assertTrue(issues.empty)

        summary = dq.build_quality_report(empty_df, issues)
        self.assertEqual(summary["rows_with_issues_pct"], 0)

    def test_missing_required_column_raises_error(self):
        incomplete_df = pd.DataFrame({
            "customer_id": [301],
            "age": [35]
        })

        with self.assertRaises(ValueError):
            dq.validate_data(incomplete_df)

    def test_detects_expected_validation_issues(self):
        issues = dq.validate_data(self.valid_df)

        self.assertEqual(len(issues), 0)

        problematic_df = pd.DataFrame({
            "customer_id": [401, 402, 403],
            "age": [150, 30, "unknown"],
            "city": ["Valencia", "Madrid", "Sevilla"],
            "monthly_spend": [20.0, -10.0, 35.0]
        })

        issues = dq.validate_data(problematic_df)

        self.assertEqual(len(issues), 3)
        self.assertSetEqual(
            set(issues["rule"]),
            {
                "AGE_OUT_OF_RANGE",
                "NEGATIVE_SPENDING",
                "AGE_NOT_NUMERIC"
            }
        )


if __name__ == "__main__":
    unittest.main()
