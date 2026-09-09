PRODUCTION_KEYS = {"rooms", "runtimes", "negative_controls"}
REPORT_COMMAND = "cargo run -q -p audio-effects --bin reverb_corpus_report"
REPORT_FILES = [
    r"crates\audio-effects\src\reverb\corpus_report.rs",
    r"crates\audio-effects\src\reverb\metrics.rs",
    r"crates\audio-effects\tests\reverb_corpus_report.rs",
]


def _require_mapping(value, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _require_list(report, field):
    value = report.get(field)
    if not isinstance(value, list):
        raise ValueError(f"production report {field} must be an array")
    return value


def _require_text(value, label):
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a nonempty string")
    return value


def _require_number(value, label):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{label} must be numeric")
    return value


def _require_boolean(value, label):
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be boolean")
    return value


def _room_cases(rooms):
    cases = []
    seen = set()
    for index, raw_room in enumerate(rooms):
        room = _require_mapping(raw_room, f"rooms[{index}]")
        name = _require_text(room.get("room"), f"rooms[{index}].room")
        if name in seen:
            raise ValueError(f"duplicate production room: {name}")
        seen.add(name)
        pu = _require_mapping(room.get("pu"), f"rooms[{index}].pu")
        pu_total = _require_number(pu.get("pu_total"), f"rooms[{index}].pu.pu_total")
        null_depth = _require_number(
            room.get("paired_null_depth_db"),
            f"rooms[{index}].paired_null_depth_db",
        )
        common = {
            "repository_case": f"{name} transfer",
            "command": REPORT_COMMAND,
            "files": REPORT_FILES,
        }
        cases.extend([
            {
                **common,
                "id": f"{name}-pu",
                "metric": "pu",
                "status": "pass" if pu_total <= 1.0 else "fail",
                "value": pu_total,
                "target": 1.0,
                "evidence": f"production schema v1 reports PU {pu_total} for {name}",
                "done_gate": f"{name} PU is at most 1.0 in the production corpus report.",
            },
            {
                **common,
                "id": f"{name}-paired-null-depth-db",
                "metric": "null_depth_db",
                "status": "pass" if null_depth >= 40.0 else "fail",
                "value": null_depth,
                "target": 40.0,
                "evidence": (
                    f"production schema v1 reports paired null depth "
                    f"{null_depth} dB for {name}"
                ),
                "done_gate": (
                    f"{name} paired null depth is at least 40 dB in the "
                    "production corpus report."
                ),
            },
        ])
    return cases


def _gate_evidence(report):
    runtimes = []
    for index, raw_runtime in enumerate(_require_list(report, "runtimes")):
        runtime = _require_mapping(raw_runtime, f"runtimes[{index}]")
        runtimes.append({
            "scenario": _require_text(
                runtime.get("scenario"), f"runtimes[{index}].scenario"
            ),
            "budget_seconds": _require_number(
                runtime.get("budget_seconds"), f"runtimes[{index}].budget_seconds"
            ),
            "passed": _require_boolean(
                runtime.get("passed"), f"runtimes[{index}].passed"
            ),
        })
    controls = []
    for index, raw_control in enumerate(_require_list(report, "negative_controls")):
        control = _require_mapping(raw_control, f"negative_controls[{index}]")
        controls.append({
            "room": _require_text(
                control.get("room"), f"negative_controls[{index}].room"
            ),
            "passed": _require_boolean(
                control.get("passed"), f"negative_controls[{index}].passed"
            ),
        })
    return {"runtimes": runtimes, "negative_controls": controls}


def report_cases(report):
    if not isinstance(report, dict):
        raise ValueError("report must be an object")
    if "cases" in report and not PRODUCTION_KEYS.intersection(report):
        cases = report["cases"]
        if not isinstance(cases, list):
            raise ValueError("report cases must be an array")
        return cases, {}
    if PRODUCTION_KEYS.intersection(report):
        missing = PRODUCTION_KEYS.difference(report)
        if missing:
            raise ValueError(f"production report missing fields: {sorted(missing)}")
        if report.get("schema_version") != 1:
            raise ValueError(
                f"unsupported production schema version: {report.get('schema_version')}"
            )
        rooms = _require_list(report, "rooms")
        cases = _room_cases(rooms)
        if not cases:
            raise ValueError("nonempty production report normalized to zero rows")
        return cases, _gate_evidence(report)
    raise ValueError("unsupported report schema")
