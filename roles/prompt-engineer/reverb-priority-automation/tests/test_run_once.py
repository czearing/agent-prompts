import sys
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import cli
from issue_api import ALLOWED_ENGINEER_IDS


ENGINEER_ID = next(iter(ALLOWED_ENGINEER_IDS))


class FakeClient:
    def __init__(self, issues):
        self._issues = issues
        self.create = unittest.mock.Mock()

    def engineer_id(self):
        return ENGINEER_ID

    def issues(self):
        return self._issues


class RunOnceTests(unittest.TestCase):
    def setUp(self):
        self.args = SimpleNamespace()

    def test_todo_and_in_progress_exit_before_side_effects(self):
        for status in ("todo", "in_progress"):
            with self.subTest(status=status):
                client = FakeClient([{
                    "assigneeAgentId": ENGINEER_ID,
                    "status": status,
                }])
                with patch.object(cli, "_client", return_value=client), patch.object(
                    cli, "refresh"
                ) as refresh, patch.object(
                    cli, "write_artifacts"
                ) as write_artifacts, patch.object(cli, "dispatch") as dispatch:
                    result = cli.run_once(self.args)
                self.assertEqual("runnable_work_exists", result["result"])
                self.assertIsNone(result["created"])
                refresh.assert_not_called()
                write_artifacts.assert_not_called()
                dispatch.assert_not_called()
                client.create.assert_not_called()

    def test_in_review_alone_does_not_block_dispatch(self):
        client = FakeClient([{
            "assigneeAgentId": ENGINEER_ID,
            "status": "in_review",
        }])
        created = {"id": "created"}
        with patch.object(cli, "_client", return_value=client), patch.object(
            cli, "refresh_and_dispatch", return_value=created
        ) as refresh_and_dispatch:
            result = cli.run_once(self.args)
        self.assertEqual("dispatched", result["result"])
        self.assertEqual(created, result["created"])
        refresh_and_dispatch.assert_called_once_with(self.args, client)

    def test_overlapping_invocations_dispatch_at_most_once(self):
        entered = threading.Event()
        release = threading.Event()
        client = FakeClient([])

        def dispatch_once(args, supplied_client):
            entered.set()
            self.assertTrue(release.wait(2))
            return {"id": "created"}

        first_result = []
        with patch.object(cli, "_client", return_value=client), patch.object(
            cli, "refresh_and_dispatch", side_effect=dispatch_once
        ) as refresh_and_dispatch:
            thread = threading.Thread(
                target=lambda: first_result.append(cli.run_once(self.args))
            )
            thread.start()
            self.assertTrue(entered.wait(2))
            second_result = cli.run_once(self.args)
            release.set()
            thread.join(2)

        self.assertFalse(thread.is_alive())
        self.assertEqual("already_running", second_result["result"])
        self.assertEqual("dispatched", first_result[0]["result"])
        self.assertEqual(1, refresh_and_dispatch.call_count)


if __name__ == "__main__":
    unittest.main()
