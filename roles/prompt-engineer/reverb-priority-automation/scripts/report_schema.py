PRODUCTION_KEYS = {"matrix", "cells", "negative_controls"}
REPORT_COMMAND = "cargo run -q -p audio-effects --bin reverb_corpus_report"
REPORT_FILES = [
    "crates/audio-effects/src/reverb/corpus_report.rs",
    "crates/audio-effects/src/reverb/corpus_report/matrix.rs",
    "crates/audio-effects/src/reverb/corpus_report/controls.rs",
    "crates/audio-effects/tests/reverb_corpus_report.rs",
]
DONE_GATE = (
    "Wet-only PU is at most 1.0, paired rendered-output null depth is at least "
    "40 dB, and runtime is at most 5 seconds."
)


def _mapping(value, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _list(value, label):
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return value


def _text(value, label):
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a nonempty string")
    return value


def _number(value, label):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{label} must be numeric")
    return value


def _names(matrix, field):
    names = [_text(value, f"matrix.{field}") for value in _list(
        matrix.get(field), f"matrix.{field}"
    )]
    if not names or len(names) != len(set(names)):
        raise ValueError(f"matrix.{field} must contain unique names")
    return names


def _cell_case(raw, expected_id, room, reference, target):
    cell = _mapping(raw, f"cells[{expected_id}]")
    for field, value in (
        ("id", expected_id),
        ("room", room),
        ("reference_source", reference),
        ("target_source", target),
        ("reference_mode", "wet-only"),
        ("done_gate", DONE_GATE),
    ):
        if cell.get(field) != value:
            raise ValueError(f"{expected_id} has invalid {field}")
    runtime = _mapping(cell.get("runtime"), f"{expected_id}.runtime")
    elapsed = _number(runtime.get("elapsed_seconds"), f"{expected_id}.runtime.elapsed_seconds")
    if _number(runtime.get("budget_seconds"), f"{expected_id}.runtime.budget_seconds") != 5.0:
        raise ValueError(f"{expected_id} runtime budget must be 5.0")
    runtime_passed = runtime.get("passed")
    if not isinstance(runtime_passed, bool) or runtime_passed != (elapsed <= 5.0):
        raise ValueError(f"{expected_id} runtime passed flag disagrees with elapsed time")
    pu = cell.get("pu")
    pu_mapping = None if pu is None else _mapping(pu, f"{expected_id}.pu")
    pu_value = None if pu_mapping is None else pu_mapping.get("pu_total")
    pu_total = (
        None
        if pu_value is None
        else _number(pu_value, f"{expected_id}.pu.pu_total")
    )
    null_depth = cell.get("paired_rendered_output_null_depth_db")
    if null_depth is not None:
        null_depth = _number(null_depth, f"{expected_id}.paired_rendered_output_null_depth_db")
    passed = (
        pu_total is not None
        and pu_total <= 1.0
        and null_depth is not None
        and null_depth >= 40.0
        and runtime_passed
    )
    if cell.get("passed") is not passed:
        raise ValueError(f"{expected_id} passed flag disagrees with its gate evidence")
    return {
        "id": expected_id,
        "repository_case": f"{room}: {reference} to {target}",
        "metric": "wet_only_matrix",
        "status": "pass" if passed else "fail",
        "value": {
            "pu": pu_total,
            "paired_rendered_output_null_depth_db": null_depth,
            "runtime_seconds": elapsed,
        },
        "target": {"pu": 1.0, "null_depth_db": 40.0, "runtime_seconds": 5.0},
        "command": REPORT_COMMAND,
        "files": REPORT_FILES,
        "evidence": (
            f"wet-only {cell.get('recovery_tier')} recovery; PU {pu_total}; "
            f"paired rendered-output null depth {null_depth} dB; runtime {elapsed} seconds"
        ),
        "done_gate": DONE_GATE,
        "reference_source": reference,
        "target_source": target,
        "room": room,
        "reference_mode": "wet-only",
        "pu": pu_total,
        "paired_rendered_output_null_depth_db": null_depth,
        "runtime_evidence": runtime,
    }


def _missing_case(case_id, room, reference, target):
    return {
        "id": case_id, "repository_case": f"{room}: {reference} to {target}",
        "metric": "wet_only_matrix", "status": "missing", "value": None,
        "target": {"pu": 1.0, "null_depth_db": 40.0, "runtime_seconds": 5.0},
        "command": REPORT_COMMAND, "files": REPORT_FILES,
        "evidence": "expected wet-only matrix cell is absent", "done_gate": DONE_GATE,
        "reference_source": reference, "target_source": target, "room": room,
        "reference_mode": "wet-only", "pu": None,
        "paired_rendered_output_null_depth_db": None, "runtime_evidence": None,
    }


def _control_cases(raw_controls):
    expected = {"wrong-room-input", "dry-input"}
    supplied = {}
    for index, raw in enumerate(_list(raw_controls, "negative_controls")):
        control = _mapping(raw, f"negative_controls[{index}]")
        name = _text(control.get("control"), f"negative_controls[{index}].control")
        if name in supplied:
            raise ValueError(f"duplicate negative control: {name}")
        if name not in expected:
            raise ValueError(f"unexpected negative control: {name}")
        supplied[name] = control
    cases = []
    for name in sorted(expected):
        control = supplied.get(name)
        if control is None:
            status, value, evidence = "missing", None, f"{name} evidence is absent"
        else:
            _text(control.get("expected_room"), f"{name}.expected_room")
            _text(control.get("input"), f"{name}.input")
            value = control.get("passed")
            if not isinstance(value, bool):
                raise ValueError(f"{name}.passed must be boolean")
            status = "pass" if value else "fail"
            evidence = f"{name} passed: {value}"
        if status != "pass":
            cases.append({
                "id": f"negative-control--{name}",
                "repository_case": name,
                "metric": "negative_control",
                "status": status,
                "value": value,
                "target": True,
                "command": REPORT_COMMAND,
                "files": REPORT_FILES,
                "evidence": evidence,
                "done_gate": f"{name} does not satisfy the wet-only ship gate.",
            })
    return cases, [supplied[name] for name in sorted(supplied)]


def _production_cases(report):
    matrix = _mapping(report["matrix"], "matrix")
    rooms, sources = _names(matrix, "rooms"), _names(matrix, "sources")
    expected_total = len(rooms) * len(sources) * (len(sources) - 1)
    if matrix.get("expected_cells") != expected_total:
        raise ValueError("matrix expected_cells disagrees with declared dimensions")
    supplied = {}
    for raw in _list(report["cells"], "cells"):
        cell = _mapping(raw, "cell")
        case_id = _text(cell.get("id"), "cell.id")
        if case_id in supplied:
            raise ValueError(f"duplicate matrix cell: {case_id}")
        supplied[case_id] = cell
    cases = []
    for room in rooms:
        for reference in sources:
            for target in sources:
                if reference == target:
                    continue
                case_id = f"{room}--{reference}-to-{target}"
                raw = supplied.pop(case_id, None)
                cases.append(
                    _missing_case(case_id, room, reference, target)
                    if raw is None else _cell_case(raw, case_id, room, reference, target)
                )
    if supplied:
        raise ValueError(f"unexpected matrix cells: {sorted(supplied)}")
    control_cases, controls = _control_cases(report["negative_controls"])
    cases.extend(control_cases)
    evidence = {
        "matrix": {
            "expected": expected_total,
            "reported": len(report["cells"]),
            "complete": len(report["cells"]) == expected_total,
        },
        "negative_controls": controls,
    }
    return cases, evidence


def report_cases(report):
    if not isinstance(report, dict):
        raise ValueError("report must be an object")
    if "cases" in report and not PRODUCTION_KEYS.intersection(report):
        return _list(report["cases"], "report cases"), {}
    missing = PRODUCTION_KEYS.difference(report)
    if missing:
        raise ValueError(f"production report missing fields: {sorted(missing)}")
    if report.get("schema_version") != 2:
        raise ValueError(f"unsupported production schema version: {report.get('schema_version')}")
    return _production_cases(report)
