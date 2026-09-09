import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from issue_api import ALLOWED_ENGINEER_IDS, IssueClient, MARKER, dispatch
from queue_core import assignment_key, normalize, write_artifacts


ENGINEER_ID = next(iter(ALLOWED_ENGINEER_IDS))


class FakeClient:
    def __init__(self, issues=None):
        self._issues = list(issues or [])
        self.created = []

    def engineer_id(self):
        return ENGINEER_ID

    def issues(self):
        return self._issues

    def create(self, body):
        issue = {
            **body,
            "id": f"issue-{len(self.created) + 1}",
            "identifier": f"MUS-{len(self.created) + 1}",
        }
        self.created.append(issue)
        self._issues.append(issue)
        return issue


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return json.dumps(self.payload).encode()


class SkillTests(unittest.TestCase):
    def setUp(self):
        report = json.loads(
            (ROOT / "fixtures" / "ranking-report.json").read_text(encoding="utf-8")
        )
        self.queue = normalize(report, r"C:\Code\mix-tool", "fixture-commit")

    def test_ranking_and_artifacts_are_deterministic(self):
        expected = ["pu-a", "pu-z", "null", "runtime", "missing", "negative"]
        self.assertEqual(expected, [row["case_id"] for row in self.queue["rows"]])
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_paths = write_artifacts(self.queue, first)
            second_paths = write_artifacts(self.queue, second)
            self.assertEqual(first_paths[0].read_bytes(), second_paths[0].read_bytes())
            self.assertEqual(first_paths[1].read_bytes(), second_paths[1].read_bytes())
            html_order = re.findall(
                r'<tr data-case-id="([^"]+)">', first_paths[1].read_text(encoding="utf-8")
            )
            self.assertEqual(expected, html_order)

    def test_dispatch_creates_one_then_no_duplicate(self):
        client = FakeClient()
        first = dispatch(self.queue, client)
        first["status"] = "in_progress"
        second = dispatch(self.queue, client)
        self.assertIsNotNone(first)
        self.assertIsNone(second)
        self.assertEqual(1, len(client.created))
        self.assertIn("hall transfer", client.created[0]["title"])
        key = assignment_key("fixture-commit", "pu-a")
        self.assertIn(f"{MARKER} {key}", client.created[0]["description"])
        self.assertEqual("in_progress", self.queue["rows"][0]["task_status"])
        self.assertEqual("MUS-1", self.queue["rows"][0]["issue_identifier"])

    def test_active_reverb_issue_blocks_dispatch(self):
        client = FakeClient([{
            "assigneeAgentId": ENGINEER_ID,
            "status": "in_progress",
            "title": "Reverb work",
            "description": f"{MARKER} existing-key",
        }])
        self.assertIsNone(dispatch(self.queue, client))
        self.assertEqual([], client.created)

    def test_issue_client_uses_supplied_bearer_credential(self):
        client = IssueClient(
            "https://runtime.invalid", "secret-key", "company", "run", ENGINEER_ID
        )
        with patch(
            "urllib.request.urlopen", return_value=FakeResponse({"value": []})
        ) as urlopen:
            client.issues()
        request = urlopen.call_args.args[0]
        self.assertEqual("Bearer secret-key", request.get_header("Authorization"))

    def test_issue_client_accepts_live_value_envelope(self):
        client = IssueClient(
            "https://runtime.invalid", "key", "company", "run", ENGINEER_ID
        )
        with patch(
            "urllib.request.urlopen",
            return_value=FakeResponse({"value": [{"id": "issue", "status": "todo"}]}),
        ):
            self.assertEqual(ENGINEER_ID, client.engineer_id())
            self.assertEqual([{"id": "issue", "status": "todo"}], client.issues())

    def test_non_allowed_identifiers_fail_without_creating(self):
        denied = [
            None,
            "",
            "unknown",
            "d2da64f1-273c-4a36-8b52-ad8c441e903c",
            "a32dfbb1-f798-42dc-b8a8-4c06b32a2e73",
            "11111111-1111-1111-1111-111111111111",
        ]
        for identifier in denied:
            with self.subTest(identifier=identifier):
                client = IssueClient(
                    "https://runtime.invalid", "key", "company", "run", identifier
                )
                with patch.object(client, "create") as create:
                    with self.assertRaisesRegex(ValueError, "exact-id allowlist"):
                        dispatch(self.queue, client)
                    create.assert_not_called()

    def test_successful_negative_control_is_not_queued(self):
        report = {
            "cases": [{
                "id": "dry", "repository_case": "dry reference",
                "metric": "negative_control", "status": "pass", "value": True,
                "target": True, "command": "run dry case", "files": ["test.rs"],
                "evidence": "declined", "done_gate": "Dry input is declined.",
            }]
        }
        queue = normalize(report, r"C:\Code\mix-tool", "commit")
        self.assertEqual(1, len(queue["rows"]))
        self.assertEqual("satisfied", queue["rows"][0]["task_status"])
        self.assertEqual(0, queue["rows"][0]["gap"])


if __name__ == "__main__":
    unittest.main()
