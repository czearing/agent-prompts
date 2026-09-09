import html
import json


def _display(value):
    if value is None:
        return "not available"
    if isinstance(value, float):
        return f"{value:.6g}"
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def _table(rows):
    headings = [
        ("rank", "Rank"), ("repository_case", "Repository case"),
        ("pu", "PU"), ("paired_rendered_output_null_depth_db", "Null depth (dB)"),
        ("runtime_evidence", "Runtime evidence"), ("gap", "Gap"),
        ("priority_reason", "Priority reason"), ("task_status", "Task status"),
        ("issue_identifier", "Issue identifier"),
    ]
    headers = "".join(f"<th>{label}</th>" for _, label in headings)
    body = []
    for row in rows:
        cells = "".join(
            f"<td>{html.escape(_display(row.get(key)))}</td>" for key, _ in headings
        )
        case_id = html.escape(row["case_id"], quote=True)
        body.append(f'<tr data-case-id="{case_id}">{cells}</tr>')
    return f"<table><thead><tr>{headers}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def render_html(queue):
    repository = html.escape(queue["repository"])
    commit = html.escape(queue["commit"])
    counts = queue["counts"]
    evidence = queue.get("report_evidence", {})
    controls = "".join(
        f"<li>{html.escape(item['control'])}: passed "
        f"{html.escape(_display(item['passed']))}</li>"
        for item in evidence.get("negative_controls", [])
    )
    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        "<title>Reverb priority queue</title><style>"
        "body{font:14px system-ui;margin:24px;color:#1f2328}"
        "table{border-collapse:collapse;width:100%;margin-bottom:24px}"
        "th,td{border:1px solid #d0d7de;padding:6px 8px;text-align:left}"
        "th{background:#f6f8fa}tr:nth-child(even){background:#fbfcfd}"
        "</style></head><body><h1>Reverb priority queue</h1>"
        f"<p>Repository: <code>{repository}</code><br>Evaluated commit: "
        f"<code>{commit}</code><br>Actionable: {counts['actionable']}<br>"
        f"Completed: {counts['completed']}<br>Total: {counts['total']}</p>"
        f"<h2>Actionable priority queue</h2>{_table(queue['rows'])}"
        f"<h2>Satisfied evidence</h2>{_table(queue['completed_rows'])}"
        f"<h2>Negative controls</h2><ul>{controls}</ul></body></html>\n"
    )
