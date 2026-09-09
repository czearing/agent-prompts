import argparse
import contextlib
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

from issue_api import IssueClient, dispatch, has_runnable_work
from queue_core import normalize, write_artifacts
from single_instance import single_instance


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPO = Path(r"C:\Code\mix-tool")
DEFAULT_ARTIFACTS = ROOT / "artifacts"
RUNTIME_PREFIX = "PAPER" + "CLIP_"
LOCK_NAME = r"Local\PaperclipReverbPriorityQueue"


def _git(repo, *arguments):
    result = subprocess.run(
        ["git", *arguments], cwd=repo, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


@contextlib.contextmanager
def _origin_master_checkout(repo):
    _git(repo, "fetch", "origin", "master", "--quiet")
    commit = _git(repo, "rev-parse", "origin/master")
    if _git(repo, "rev-parse", "HEAD") == commit:
        yield repo, commit
        return
    scratch = os.getenv("PAPERCLIP_RUN_SCRATCH_DIR") or tempfile.gettempdir()
    checkout = Path(tempfile.mkdtemp(prefix="reverb-origin-master-", dir=scratch))
    checkout.rmdir()
    added = False
    try:
        _git(repo, "worktree", "add", "--detach", str(checkout), commit)
        added = True
        yield checkout, commit
    finally:
        if added:
            _git(repo, "worktree", "remove", "--force", str(checkout))


def _production_report(repo):
    command = [
        "cargo", "run", "-q", "-p", "audio-effects", "--bin",
        "reverb_corpus_report",
    ]
    result = subprocess.run(
        command, cwd=repo, text=True, capture_output=True, check=True
    )
    return result.stdout.encode(), json.loads(result.stdout)


def refresh(args):
    repo = Path(args.repo).resolve()
    with _origin_master_checkout(repo) as (checkout, commit):
        if args.report:
            report_bytes = Path(args.report).read_bytes()
            report = json.loads(report_bytes.decode("utf-8"))
        else:
            report_bytes, report = _production_report(checkout)
    queue = normalize(report, str(repo), commit)
    queue["report_sha256"] = hashlib.sha256(report_bytes).hexdigest()
    return queue, write_artifacts(queue, args.artifacts)


def _setting(args, option, suffix):
    value = getattr(args, option)
    if value:
        return value
    generic = os.getenv(f"REVERB_{suffix}")
    runtime = os.getenv(RUNTIME_PREFIX + suffix)
    value = generic or runtime
    if not value:
        raise ValueError(f"missing --{option.replace('_', '-')}")
    return value


def _client(args):
    return IssueClient(
        _setting(args, "api_url", "API_URL"),
        _setting(args, "api_key", "API_KEY"),
        _setting(args, "company_id", "COMPANY_ID"),
        _setting(args, "run_id", "RUN_ID"),
        _setting(args, "engineer_id", "AGENT_ID"),
    )


def dispatch_queue(args, queue=None, client=None):
    if queue is None:
        path = Path(args.artifacts) / "reverb-queue.json"
        queue = json.loads(path.read_text(encoding="utf-8"))
    created = dispatch(queue, client or _client(args))
    write_artifacts(queue, args.artifacts)
    return created


def refresh_and_dispatch(args, client=None):
    queue, _ = refresh(args)
    return dispatch_queue(args, queue, client)


def run_once(args):
    with single_instance(LOCK_NAME) as acquired:
        if not acquired:
            return {"result": "already_running", "created": None}
        client = _client(args)
        engineer_id = client.engineer_id()
        issues = client.issues()
        if has_runnable_work(issues, engineer_id):
            return {"result": "runnable_work_exists", "created": None}
        created = refresh_and_dispatch(args, client)
        return {"result": "dispatched" if created else "no_gap", "created": created}


def _common(parser):
    parser.add_argument("--repo", default=str(DEFAULT_REPO))
    parser.add_argument("--artifacts", default=str(DEFAULT_ARTIFACTS))
    parser.add_argument("--report")


def _api(parser):
    parser.add_argument("--api-url")
    parser.add_argument("--api-key")
    parser.add_argument("--company-id")
    parser.add_argument("--run-id")
    parser.add_argument("--engineer-id")


def main():
    parser = argparse.ArgumentParser(description="Refresh and dispatch the reverb queue")
    commands = parser.add_subparsers(dest="action", required=True)
    refresh_parser = commands.add_parser("refresh")
    _common(refresh_parser)
    dispatch_parser = commands.add_parser("dispatch")
    dispatch_parser.add_argument("--artifacts", default=str(DEFAULT_ARTIFACTS))
    _api(dispatch_parser)
    run_parser = commands.add_parser("run-once")
    _common(run_parser)
    _api(run_parser)
    event_parser = commands.add_parser("event")
    event_parser.add_argument("event", choices=["issue-completed", "merge"])
    _common(event_parser)
    _api(event_parser)
    args = parser.parse_args()
    if args.action == "refresh":
        _, paths = refresh(args)
        print("\n".join(str(path) for path in paths))
    elif args.action == "dispatch":
        created = dispatch_queue(args)
        print(json.dumps({
            "created_count": 1 if created else 0,
            "issue_identifier": (
                created.get("identifier", created.get("id", "")) if created else None
            ),
        }))
    elif args.action == "event":
        created = refresh_and_dispatch(args)
        print(json.dumps({
            "created_count": 1 if created else 0,
            "issue_identifier": (
                created.get("identifier", created.get("id", "")) if created else None
            ),
        }))
    else:
        result = run_once(args)
        created = result["created"]
        print(json.dumps({
            "result": result["result"],
            "created_count": 1 if created else 0,
            "issue_identifier": (
                created.get("identifier", created.get("id", "")) if created else None
            ),
        }))


if __name__ == "__main__":
    main()
