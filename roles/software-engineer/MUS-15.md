# Engineering Task Log

Task: MUS-15 Install continuous reverb queue runner
Branch: mus-15-continuous-reverb-runner
Packages in scope: roles/prompt-engineer/reverb-priority-automation
Date started: 2026-09-08
Issue owner: local-board

## 1. Context and Problem Understanding

### Problem Statement
An enabled Windows scheduled task must run deterministic reverb queue code every five minutes. When
General Software Engineer has a `todo` or `in_progress` issue, the tick must stop before metrics,
artifact writes, or issue creation. Otherwise it must evaluate current `origin/master`, refresh both
queue artifacts, and assign exactly one highest-priority gap to exact agent id
`32cdb55f-fa10-40f3-929d-cf50b4dc3e10`.

### Reproduction or Current Behavior
Before editing, `scripts/cli.py` exposes only `refresh`, `dispatch`, and manual `event` commands.
No scheduler installer or run-once command exists. `issue_api.py::engineer_id` queries agents by the
display name `General Software Engineer`, and `ACTIVE` includes `in_review` and `blocked`. Therefore
there is no unattended succession, ownership is not fail-closed by exact id, and unrelated review
work can block dispatch.

### Repository Discovery

| Path | Role in this task |
| --- | --- |
| roles/prompt-engineer/reverb-priority-automation/scripts/cli.py | Existing refresh and manual dispatch orchestration. |
| roles/prompt-engineer/reverb-priority-automation/scripts/issue_api.py | Runtime issue API, ownership lookup, active checks, and issue creation. |
| roles/prompt-engineer/reverb-priority-automation/scripts/queue_core.py | Shared normalization, stable ranking, HTML rendering, and artifact writes. |
| roles/prompt-engineer/reverb-priority-automation/tests/test_skill.py | Existing queue and issue API unit assertions. |
| roles/prompt-engineer/reverb-priority-automation/SKILL.md | Package command and operating contract. |

Package instruction files read before editing: repository `README.md`, package
`roles/prompt-engineer/README.md`, role `roles/software-engineer/README.md`, and
`roles/chief-of-staff/reverb-continuous-dispatch-decision.md`. No `AGENTS.md` or package-specific
build manifest exists.

Existing code to reuse: `_origin_master_checkout`, `_production_report`, `refresh`,
`normalize`, `write_artifacts`, `assignment_key`, `IssueClient`, and `dispatch`.

Constraints: do not modify prompts or templates; treat `C:\Code\mix-tool` as read-only input; never
persist credentials in source, task arguments, artifacts, logs, or fixtures; use deterministic
run-once execution with nonblocking exclusion; keep new or materially expanded authored source files
under 200 lines; preserve pre-existing untracked package work and unrelated repository changes.

## 2. Thesis and Strategy

### Root Cause
The queue implementation has no installed invocation path, and its issue owner is selected by a
mutable display name instead of a fail-closed exact-id gate.

### Narrowest Fix
Add a shared run-once orchestration function around the existing refresh and dispatch functions,
guard it with a nonblocking single-instance lock, make `IssueClient` validate one configured exact
agent id, and add an idempotent scheduled-task installer whose launcher reads credentials only from
the scheduled process environment or an existing secure environment mechanism.

### Alternatives Considered and Rejected
A scheduled agent heartbeat, sleep loop, or polling process is rejected because the decision log
requires deterministic code without token-consuming agent work. Embedding a credential in the task
action is rejected because Task Scheduler arguments are inspectable. Reimplementing normalization or
dispatch in the launcher is rejected because it would create a second writer and divergent behavior.

### Scope Check
- [x] Change remains in the assigned automation package plus this required task log.
- [x] No app-main/page-container boundary applies.
- [x] Existing queue and dispatch behavior will be reused.
- [x] No public API break is intended.
- [x] Every new or materially expanded authored source file remains under 200 lines.
- [x] No wait, sleep, retry, heartbeat, or polling loop will be added.
- [x] All affected callers and duplicate-write boundaries are checked.

## 3. Risk and Impact Analysis

| Risk | Who it affects | How it is caught before merge |
| --- | --- | --- |
| A runnable issue is missed and a duplicate is created | General Software Engineer | Exact todo and in_progress early-exit tests plus overlapping invocation test |
| Wrong agent receives generated work | Company issue queue | Exact-id allowlist matrix with zero-create failure assertions |
| Installer creates duplicate or removes another task | Host operator | Two-install and exact-name uninstall integration test |
| Queue artifacts diverge | Queue consumers | Existing byte/order assertions and scheduled live proof |

- [x] Other callers and failure boundaries reviewed.
- [x] Accessibility, localization, and keyboard behavior do not apply.
- [x] Queue schema and issue description remain backward compatible.
- [x] Error and empty states remain explicit.

## 4. Performance Expectations Check

- [x] Active work exits before repository or metric operations.
- [x] No UI render cost applies.
- [x] No bundle applies.
- [x] One issue query is reused for active-work and dispatch decisions.
- [x] No retry, poll, wait, or sleep loop is introduced.

Result: pass. Active-work ticks use one issue request and no repository work; the empty-slot tick
executes one bounded production report with no retry or poll loop.

## 5. Validation and Evidence

### Test Plan
Add exact unit assertions for `todo`, `in_progress`, `in_review`, the complete denied identifier
matrix, and overlapping invocations. Add an installer integration test proving repeated install and
exact uninstall behavior. Run the package unit suite, install the live schedule, then observe two
natural scheduler ticks without manually invoking refresh, dispatch, event, or the task.

### Evidence

| Check | Command or steps | Before | After |
| --- | --- | --- | --- |
| Current command surface | inspect `scripts/cli.py` | no run-once command or scheduler | `run-once` performs exact-id live issue check before refresh and dispatch |
| Exact ownership | `python -m unittest discover -s ...\tests -p "test_*.py" -v` | display-name lookup | missing, empty, unknown, Prompt Writer, Chief of Staff, and another id all fail before create |
| Targeted unit tests | same unittest command | n/a | exit 0, 15 passed |
| Python compilation | compile every package script and Python test with `python -m py_compile` | n/a | exit 0, 8 files compiled |
| Installer integration | `& ...\tests\test_scheduler.ps1` | no installer | exit 0; two installs produced one enabled PT5M task, exact uninstall preserved sibling |
| Source size gate | count all script, scheduler, and test files | n/a | exit 0; all 13 authored files below 200 lines |
| Credential scan | scan package files for the live credential | n/a | exit 0; no package file contains the credential |
| Active-work natural tick | Task Scheduler history and artifact timestamp | no schedule | 2026-09-08T20:27:44-07:00, result 0; queue timestamp remained 2026-09-08T18:24:39.7881843-07:00 |
| Empty-slot natural tick | Task Scheduler history, runtime API, and artifacts | no automatic refresh | 2026-09-08T20:32:45-07:00, result 0; refreshed current origin/master and created zero issues because every row is satisfied |

Installed task: `Paperclip-Reverb-Priority-Queue`; enabled and ready; five-minute interval `PT5M`;
next run observed as 2026-09-08T20:37:44-07:00. Its action contains only the deterministic launcher,
credential target, and Python path, with no API credential.

Empty-slot natural tick evidence: evaluated commit
`393f2cb321b90e571f8d6b49c389a0e6b59d4eac`; report SHA-256
`ad4373953ad52d03e76f80c102a3957655ad6f1deaabca9485a37032374a59c0`; queue SHA-256
`d1a3f1ea0d97e13760b2a2d695e49908361f28ea73ba060ddb63949e36746743`; JSON and HTML row
order identical. The first row is `cathedral-paired-null-depth-db`, current 53.822662 dB, target
40 dB, gap 0. All ten numeric rows are satisfied, both runtime gates pass, and all four negative
controls pass. No successor identifier or assignee exists because dispatching a satisfied row would
violate the queue contract. A following runnable-work tick therefore cannot be observed.

## 6. Review of the Completed Diff

- [x] Every changed line serves the stated root cause, with no unrelated cleanup.
- [x] No unsafe type suppression is introduced.
- [x] React and design-token checks do not apply.
- [x] Descriptive names and limited comments are used.
- [x] Credentials are absent from source, arguments, artifacts, logs, and fixtures.
- [x] No em dash is introduced.

## 7. Execution Checklist

- [x] Reproduction/current behavior recorded before code changes.
- [x] Repository discovery table filled with real paths.
- [x] Root cause and rejected alternative recorded.
- [x] Branch created.
- [x] Regression assertions added and proven.
- [x] Performance expectations check completed.
- [ ] Live scheduler verification blocked after the empty-slot natural tick found zero unsatisfied rows.
- [x] No repository change-file convention was found.
- [x] Required automated gates passed.
- [x] Branch pushed; pull request creation is pending.
- [x] All placeholders removed.

Pull request: pending
Commit: `98da3125efd0d0f3c473a375319a4bf4d60a13af`
Merge status: blocked because current production evidence has no unsatisfied successor to dispatch.

Final disposition: blocked. Unblock owner: issue owner or metric owner. Required action: provide a
real failing production reverb gate on current `origin/master`, or explicitly revise the acceptance
criterion that requires creating an issue when no unsatisfied row exists. The installed task remains
enabled and continues to obey the specified no-invention dispatch contract.
