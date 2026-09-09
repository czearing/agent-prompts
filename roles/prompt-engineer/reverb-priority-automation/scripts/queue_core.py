import html
import hashlib
import json
from pathlib import Path

from report_schema import report_cases


METRICS = {"pu", "null_depth_db", "runtime_seconds", "negative_control"}
EVIDENCE_STATES = {"pass", "fail", "missing", "error"}
FAILURE_STATES = {"fail", "missing", "error"}
TARGETS = {
    "pu": 1.0,
    "null_depth_db": 40.0,
    "runtime_seconds": 5.0,
    "negative_control": True,
}


def assignment_key(commit, case_id):
    raw = f"{commit}:{case_id}".encode()
    return hashlib.sha256(raw).hexdigest()[:20]


def _gap(case):
    metric = case["metric"]
    status = case["status"]
    if status in {"missing", "error"}:
        return None
    value = case.get("value")
    target = case["target"]
    if metric not in METRICS:
        raise ValueError(f"unsupported metric: {metric}")
    if target != TARGETS[metric]:
        raise ValueError(f"{case['id']} target must be {TARGETS[metric]}")
    if metric == "negative_control":
        if not isinstance(value, bool) or target is not True:
            raise ValueError("negative controls require boolean value and true target")
        return 0 if value else 1
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{case['id']} requires an actual numeric value")
    if not isinstance(target, (int, float)) or isinstance(target, bool):
        raise ValueError(f"{case['id']} requires a numeric target")
    if metric in {"pu", "runtime_seconds"}:
        return round(max(0, value - target), 7)
    return round(max(0, target - value), 7)


def _reason(case, gap):
    if case["status"] == "missing":
        return "missing ship-gate evidence"
    if case["status"] == "error":
        return "repository metric entrypoint failed"
    labels = {
        "pu": "perceptual gate failure",
        "null_depth_db": "null-depth gate failure",
        "runtime_seconds": "runtime gate failure",
        "negative_control": "unsupported evidence was accepted",
    }
    return labels[case["metric"]] if gap else "ship gate satisfied"


def normalize(report, repository, commit):
    if report.get("commit") not in (None, commit):
        raise ValueError("report commit does not match the checked repository commit")
    cases, report_evidence = report_cases(report)
    rows = []
    seen = set()
    for case in cases:
        required = {
            "id", "repository_case", "metric", "status", "target", "command",
            "files", "evidence", "done_gate",
        }
        missing = required.difference(case)
        if missing:
            raise ValueError(f"{case.get('id', 'case')} missing fields: {sorted(missing)}")
        if case["id"] in seen:
            raise ValueError(f"duplicate case id: {case['id']}")
        if case["status"] not in EVIDENCE_STATES:
            raise ValueError(f"unsupported evidence status: {case['status']}")
        seen.add(case["id"])
        gap = _gap(case)
        current = "missing" if case["status"] == "missing" else case.get("value")
        actionable = case["status"] in FAILURE_STATES or bool(gap)
        rows.append({
            "case_id": case["id"],
            "repository_case": case["repository_case"],
            "metric": case["metric"],
            "evidence_status": case["status"],
            "current_metric": current,
            "target": case["target"],
            "gap": gap,
            "priority_reason": _reason(case, gap),
            "task_status": "queued" if actionable else "satisfied",
            "issue_identifier": "",
            "reproduction_command": case["command"],
            "relevant_files": case["files"],
            "done_gate": case["done_gate"],
            "evidence": case["evidence"],
        })

    def key(row):
        failure = 1 if row["task_status"] == "queued" else 0
        gap = row["gap"] or 0
        return (
            -failure,
            -gap if row["metric"] == "pu" else 0,
            -gap if row["metric"] == "null_depth_db" else 0,
            -gap if row["metric"] == "runtime_seconds" else 0,
            row["case_id"],
        )

    rows.sort(key=key)
    for rank, row in enumerate(rows, 1):
        row["rank"] = rank
        row["assignment_key"] = assignment_key(commit, row["case_id"])
    if not rows:
        raise ValueError("supported report normalized to zero rows")
    return {
        "schema_version": 1,
        "repository": repository,
        "commit": commit,
        "report_evidence": report_evidence,
        "rows": rows,
    }


def _display(value):
    if value is None:
        return "not available"
    if isinstance(value, float):
        return f"{value:.6g}"
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def render_html(queue):
    headings = [
        ("rank", "Rank"), ("repository_case", "Repository case"),
        ("metric", "Metric"),
        ("current_metric", "Current metric"), ("target", "Target"),
        ("gap", "Gap"), ("priority_reason", "Priority reason"),
        ("task_status", "Task status"), ("issue_identifier", "Issue identifier"),
    ]
    body = []
    for row in queue["rows"]:
        cells = "".join(
            f"<td>{html.escape(_display(row[key]))}</td>" for key, _ in headings
        )
        case_id = html.escape(row["case_id"], quote=True)
        body.append(f'<tr data-case-id="{case_id}">{cells}</tr>')
    headers = "".join(f"<th>{label}</th>" for _, label in headings)
    repository = html.escape(queue["repository"])
    commit = html.escape(queue["commit"])
    evidence = queue.get("report_evidence", {})
    runtimes = "".join(
        f"<li>{html.escape(item['scenario'])}: budget "
        f"{html.escape(_display(item['budget_seconds']))} seconds, passed "
        f"{html.escape(_display(item['passed']))}</li>"
        for item in evidence.get("runtimes", [])
    )
    controls = "".join(
        f"<li>{html.escape(item['room'])}: passed "
        f"{html.escape(_display(item['passed']))}</li>"
        for item in evidence.get("negative_controls", [])
    )
    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        "<title>Reverb priority queue</title><style>"
        "body{font:14px system-ui;margin:24px;color:#1f2328}"
        "table{border-collapse:collapse;width:100%}th,td{border:1px solid #d0d7de;"
        "padding:6px 8px;text-align:left}th{background:#f6f8fa}tr:nth-child(even){"
        "background:#fbfcfd}</style></head><body><h1>Reverb priority queue</h1>"
        f"<p>Repository: <code>{repository}</code><br>Evaluated commit: "
        f"<code>{commit}</code></p><h2>Runtime gate evidence</h2><ul>{runtimes}</ul>"
        f"<h2>Negative-control evidence</h2><ul>{controls}</ul><table>"
        f"<thead><tr>{headers}</tr></thead><tbody>{''.join(body)}</tbody>"
        "</table></body></html>\n"
    )


def write_artifacts(queue, directory):
    output = Path(directory)
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "reverb-queue.json"
    html_path = output / "reverb-queue.html"
    json_path.write_text(
        json.dumps(queue, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )
    html_path.write_text(render_html(queue), encoding="utf-8")
    return json_path, html_path
