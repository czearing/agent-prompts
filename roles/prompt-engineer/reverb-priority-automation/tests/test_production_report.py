import copy
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

    def test_complete_matrix_partitions_actionable_and_completed_rows(self):
        self.assertEqual(
            {"actionable": 1, "completed": 1, "total": 2}, self.queue["counts"]
        )
        self.assertEqual(
            ["small-room--piano-to-organ"],
            [row["case_id"] for row in self.queue["rows"]],
        )
        self.assertEqual(
            ["small-room--organ-to-piano"],
            [row["case_id"] for row in self.queue["completed_rows"]],
        )
        row = self.queue["rows"][0]
        self.assertEqual("piano", row["reference_source"])
        self.assertEqual("organ", row["target_source"])
        self.assertEqual("small-room", row["room"])
        self.assertEqual("wet-only", row["reference_mode"])
        self.assertEqual(2.5, row["pu"])
        self.assertEqual(20.0, row["paired_rendered_output_null_depth_db"])
        self.assertEqual(1.5, row["gap"])

    def test_omitted_matrix_cell_becomes_highest_priority_failure(self):
        incomplete = copy.deepcopy(self.report)
        incomplete["cells"].pop()
        queue = normalize(incomplete, r"C:\Code\mix-tool", "origin-commit")
        self.assertFalse(queue["report_evidence"]["matrix"]["complete"])
        self.assertEqual(1, queue["report_evidence"]["matrix"]["reported"])
        self.assertEqual(2, queue["report_evidence"]["matrix"]["expected"])
        self.assertEqual("small-room--piano-to-organ", queue["rows"][0]["case_id"])
        self.assertEqual("missing", queue["rows"][0]["evidence_status"])
        self.assertEqual(1, queue["counts"]["actionable"])

    def test_json_and_html_have_identical_actionable_order_and_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            json_path, html_path = write_artifacts(self.queue, directory)
            persisted = json.loads(json_path.read_text(encoding="utf-8"))
            html = html_path.read_text(encoding="utf-8")
        actionable_html = html.split("<h2>Satisfied evidence</h2>", 1)[0]
        html_order = re.findall(r'<tr data-case-id="([^"]+)">', actionable_html)
        self.assertEqual([row["case_id"] for row in persisted["rows"]], html_order)
        self.assertIn("Actionable: 1", html)
        self.assertIn("Completed: 1", html)
        self.assertNotIn("small-room--organ-to-piano", actionable_html)
        self.assertIn("small-room--organ-to-piano", html)

    def test_inconsistent_pass_flag_is_rejected(self):
        inconsistent = copy.deepcopy(self.report)
        inconsistent["cells"][1]["passed"] = True
        with self.assertRaisesRegex(ValueError, "passed flag disagrees"):
            normalize(inconsistent, r"C:\Code\mix-tool", "origin-commit")

    def test_inconsistent_runtime_flag_is_rejected(self):
        inconsistent = copy.deepcopy(self.report)
        inconsistent["cells"][0]["runtime"]["passed"] = False
        with self.assertRaisesRegex(ValueError, "runtime passed flag disagrees"):
            normalize(inconsistent, r"C:\Code\mix-tool", "origin-commit")

    def test_negative_control_failure_is_rejected(self):
        failed = copy.deepcopy(self.report)
        failed["negative_controls"][0]["passed"] = False
        with self.assertRaisesRegex(ValueError, "negative controls must pass"):
            normalize(failed, r"C:\Code\mix-tool", "origin-commit")


if __name__ == "__main__":
    unittest.main()
