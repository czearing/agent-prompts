import json
import urllib.error
import urllib.parse
import urllib.request

from queue_core import assignment_key


ALLOWED_ENGINEER_IDS = frozenset({"32cdb55f-fa10-40f3-929d-cf50b4dc3e10"})
RUNNABLE = {"todo", "in_progress"}
MARKER = "Reverb-Queue-Key:"


class IssueClient:
    def __init__(self, base_url, api_key, company_id, run_id, engineer_id):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.company_id = company_id
        self.run_id = run_id
        self.configured_engineer_id = engineer_id

    def _request(self, method, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        if method != "GET":
            headers["X-Paper" + "clip-Run-Id"] = self.run_id
        request = urllib.request.Request(
            self.base_url + path, data=data, headers=headers, method=method
        )
        try:
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as error:
            detail = error.read().decode(errors="replace")
            raise RuntimeError(f"issue API returned {error.code}: {detail}") from error

    def _items(self, path):
        payload = self._request("GET", path)
        if isinstance(payload, list):
            return payload
        if not isinstance(payload, dict):
            raise ValueError(f"unexpected list response from {path}")
        for key in ("items", "issues", "agents", "data", "value"):
            if isinstance(payload.get(key), list):
                return payload[key]
        raise ValueError(f"unexpected list response from {path}")

    def engineer_id(self):
        if self.configured_engineer_id not in ALLOWED_ENGINEER_IDS:
            raise ValueError("engineer id is not in the exact-id allowlist")
        return self.configured_engineer_id

    def issues(self):
        path = f"/api/companies/{self.company_id}/issues"
        return self._items(path)

    def create(self, body):
        path = f"/api/companies/{self.company_id}/issues"
        return self._request("POST", path, body)


def has_runnable_work(issues, engineer_id):
    return any(
        issue.get("assigneeAgentId") == engineer_id
        and issue.get("status") in RUNNABLE
        for issue in issues
    )


def _description(queue, row, key):
    files = "\n".join(f"- `{path}`" for path in row["relevant_files"])
    return (
        f"{MARKER} {key}\n\n"
        f"Repository: `{queue['repository']}`\n"
        f"Commit: `{queue['commit']}`\n"
        f"Metric gap: {row['metric']} for {row['repository_case']}\n"
        f"Baseline: {row['current_metric']}\n"
        f"Target: {row['target']}\n"
        f"Gap: {row['gap']}\n\n"
        f"Reproduce:\n`{row['reproduction_command']}`\n\n"
        f"Relevant files:\n{files}\n\n"
        f"Done gate: {row['done_gate']}\n\n"
        "Reuse existing functions and helpers before adding logic. Extract one shared "
        "implementation instead of duplicating behavior. Keep new or materially expanded "
        "authored source files under 200 lines, splitting at cohesive boundaries. Generated "
        "data and fixtures need a task-log exemption. Do not add timers, sleeps, polling, "
        "scheduled heartbeats, or status-report paths. Land the change on `master` through "
        "the repository's checked branch and review workflow."
    )


def dispatch(queue, client):
    engineer_id = client.engineer_id()
    issues = client.issues()
    for row in queue["rows"]:
        key = assignment_key(queue["commit"], row["case_id"])
        marker = f"{MARKER} {key}"
        existing = next(
            (issue for issue in issues if marker in (issue.get("description") or "")),
            None,
        )
        if existing:
            row["task_status"] = existing.get("status", "existing")
            row["issue_identifier"] = existing.get(
                "identifier", existing.get("id", "")
            )
            return None
    if has_runnable_work(issues, engineer_id):
        return None
    queued = [row for row in queue["rows"] if row["task_status"] == "queued"]
    if not queued:
        return None
    row = queued[0]
    key = assignment_key(queue["commit"], row["case_id"])
    created = client.create({
        "title": f"Reverb gate: {row['repository_case']}",
        "description": _description(queue, row, key),
        "status": "todo",
        "priority": "high",
        "assigneeAgentId": engineer_id,
    })
    row["task_status"] = created.get("status", "todo")
    row["issue_identifier"] = created.get("identifier", created.get("id", ""))
    return created
