import hashlib
import json
from pathlib import Path

from html_report import render_html
from report_schema import report_cases


METRICS = {"pu", "null_depth_db", "runtime_seconds", "negative_control", "wet_only_matrix"}
EVIDENCE_STATES = {"pass", "fail", "missing", "error"}
FAILURE_STATES = {"fail", "missing", "error"}
TARGETS = {
    "pu": 1.0,
    "null_depth_db": 40.0,
    "runtime_seconds": 5.0,
    "negative_control": True,
}


def assignment_key(commit, case_id):
    return hashlib.sha256(f"{commit}:{case_id}".encode()).hexdigest()[:20]


def _matrix_gap(case):
    if case["status"] in {"missing", "error"}:
        return None
    value = case["value"]
    if not isinstance(value, dict):
        raise ValueError(f"{case['id']} matrix value must be an object")
    pu = value.get("pu")
    null_depth = value.get("paired_rendered_output_null_depth_db")
    runtime = value.get("runtime_seconds")
    if pu is None or null_depth is None:
        return None
    numbers = (pu, null_depth, runtime)
    if any(not isinstance(item, (int, float)) or isinstance(item, bool) for item in numbers):
        raise ValueError(f"{case['id']} matrix metrics must be numeric")
    return round(max(0, pu - 1.0, (40.0 - null_depth) / 40.0, (runtime - 5.0) / 5.0), 7)


def _gap(case):
    metric, status = case["metric"], case["status"]
    if metric == "wet_only_matrix":
        return _matrix_gap(case)
    if status in {"missing", "error"}:
        return None
    value, target = case.get("value"), case["target"]
    if metric not in METRICS:
        raise ValueError(f"unsupported metric: {metric}")
    if target != TARGETS[metric]:
        raise ValueError(f"{case['id']} target must be {TARGETS[metric]}")
    if metric == "negative_control":
        if not isinstance(value, bool):
            raise ValueError("negative controls require a boolean value")
        return 0 if value else 1
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{case['id']} requires an actual numeric value")
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
        "wet_only_matrix": "wet-only matrix gate failure",
    }
    return labels[case["metric"]] if gap or case["status"] == "fail" else "ship gate satisfied"


def _row(case, commit):
    required = {
        "id", "repository_case", "metric", "status", "target", "command",
        "files", "evidence", "done_gate",
    }
    missing = required.difference(case)
    if missing:
        raise ValueError(f"{case.get('id', 'case')} missing fields: {sorted(missing)}")
    if case["status"] not in EVIDENCE_STATES:
        raise ValueError(f"unsupported evidence status: {case['status']}")
    gap = _gap(case)
    actionable = case["status"] in FAILURE_STATES or bool(gap)
    row = {
        "case_id": case["id"],
        "repository_case": case["repository_case"],
        "metric": case["metric"],
        "evidence_status": case["status"],
        "current_metric": "missing" if case["status"] == "missing" else case.get("value"),
        "target": case["target"],
        "gap": gap,
        "priority_reason": _reason(case, gap),
        "task_status": "queued" if actionable else "satisfied",
        "issue_identifier": "",
        "reproduction_command": case["command"],
        "relevant_files": case["files"],
        "done_gate": case["done_gate"],
        "evidence": case["evidence"],
        "assignment_key": assignment_key(commit, case["id"]),
    }
    for field in (
        "reference_source", "target_source", "room", "reference_mode", "pu",
        "paired_rendered_output_null_depth_db", "runtime_evidence",
    ):
        if field in case:
            row[field] = case[field]
    return row


def _sort_key(row):
    missing = row["gap"] is None
    return (-int(missing), -(row["gap"] or 0), row["case_id"])


def normalize(report, repository, commit):
    if report.get("commit") not in (None, commit):
        raise ValueError("report commit does not match the checked repository commit")
    cases, report_evidence = report_cases(report)
    seen = set()
    rows = []
    for case in cases:
        if case.get("id") in seen:
            raise ValueError(f"duplicate case id: {case.get('id')}")
        seen.add(case.get("id"))
        rows.append(_row(case, commit))
    if not rows:
        raise ValueError("supported report normalized to zero rows")
    actionable = sorted(
        (row for row in rows if row["task_status"] == "queued"), key=_sort_key
    )
    completed = sorted(
        (row for row in rows if row["task_status"] == "satisfied"),
        key=lambda row: row["case_id"],
    )
    for rank, row in enumerate(actionable, 1):
        row["rank"] = rank
    for rank, row in enumerate(completed, 1):
        row["rank"] = rank
    return {
        "schema_version": 2,
        "repository": repository,
        "commit": commit,
        "report_evidence": report_evidence,
        "counts": {
            "actionable": len(actionable),
            "completed": len(completed),
            "total": len(rows),
        },
        "rows": actionable,
        "completed_rows": completed,
    }


def write_artifacts(queue, directory):
    output = Path(directory)
    output.mkdir(parents=True, exist_ok=True)
    json_path, html_path = output / "reverb-queue.json", output / "reverb-queue.html"
    json_path.write_text(json.dumps(queue, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    html_path.write_text(render_html(queue), encoding="utf-8")
    return json_path, html_path
