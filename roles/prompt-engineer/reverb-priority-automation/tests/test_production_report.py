import json
import re
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from queue_core import normalize, write_artifacts


class ProductionReportTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads(
            (ROOT / "fixtures" / "production-report.json").read_text(encoding="utf-8")
        )
        self.queue = normalize(self.report, r"C:\Code\mix-tool", "origin-commit")

    def test_all_numeric_rows_have_stable_priority_and_exact_gaps(self):
        expected = [
            ("cathedral-pu", 7.029184, 1.0, 6.029184),
            ("plate-pu", 2.480504, 1.0, 1.480504),
            ("medium-room-pu", 2.286499, 1.0, 1.286499),
            ("concert-hall-pu", 1.2151996, 1.0, 0.2151996),
            ("concert-hall-paired-null-depth-db", -5.356182, 40.0, 45.356182),
            ("medium-room-paired-null-depth-db", -4.3943944, 40.0, 44.3943944),
            ("plate-paired-null-depth-db", -4.0800796, 40.0, 44.0800796),
            ("cathedral-paired-null-depth-db", -3.5703897, 40.0, 43.5703897),
            ("small-room-paired-null-depth-db", -0.6024662, 40.0, 40.6024662),
            ("small-room-pu", 0.7432695, 1.0, 0),
        ]
        actual = [
            (
                row["case_id"], row["current_metric"], row["target"], row["gap"]
            )
            for row in self.queue["rows"]
        ]
        self.assertEqual(expected, actual)
        self.assertEqual(10, len(self.queue["rows"]))

    def test_boolean_gate_evidence_is_preserved_without_runtime_measurement(self):
        self.assertEqual(
            [
                {
                    "scenario": "recovery_and_transfer",
                    "budget_seconds": 5.0,
                    "passed": True,
                },
                {
                    "scenario": "phrase_render",
                    "budget_seconds": 5.0,
                    "passed": True,
                },
            ],
            self.queue["report_evidence"]["runtimes"],
        )
        self.assertTrue(all(
            item["passed"]
            for item in self.queue["report_evidence"]["negative_controls"]
        ))
        self.assertNotIn("runtime_seconds", {
            row["metric"] for row in self.queue["rows"]
        })

    def test_json_and_html_share_order_and_show_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            json_path, html_path = write_artifacts(self.queue, directory)
            persisted = json.loads(json_path.read_text(encoding="utf-8"))
            html = html_path.read_text(encoding="utf-8")
        json_order = [row["case_id"] for row in persisted["rows"]]
        html_order = re.findall(r'<tr data-case-id="([^"]+)">', html)
        self.assertEqual(json_order, html_order)
        self.assertIn("origin-commit", html)
        self.assertIn("recovery_and_transfer: budget 5 seconds, passed true", html)
        self.assertIn("small-room: passed true", html)

    def test_supported_empty_report_fails(self):
        report = {
            "schema_version": 1,
            "rooms": [],
            "runtimes": [{"scenario": "transfer", "budget_seconds": 5.0, "passed": True}],
            "negative_controls": [{"room": "dry", "passed": True}],
        }
        with self.assertRaisesRegex(
            ValueError, "production report normalized to zero rows"
        ):
            normalize(report, r"C:\Code\mix-tool", "origin-commit")

    def test_unsupported_schema_fails(self):
        with self.assertRaisesRegex(ValueError, "unsupported report schema"):
            normalize({"schema_version": 1, "measurements": []}, "repo", "commit")


if __name__ == "__main__":
    unittest.main()
