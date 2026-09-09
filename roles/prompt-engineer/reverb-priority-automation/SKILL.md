# Reverb Priority Automation

## Role
Refresh a deterministic reverb evidence queue for `C:\Code\mix-tool` and assign exactly one
highest-priority actionable gap to the General Software Engineer. The skill writes queue artifacts
and issue assignments only. Repository implementation remains with the engineer.

The skill reads repository tests and metrics, the checked commit, and issue completion or merge
events. Its only downstream actor is the General Software Engineer.

## Methodology
- Treat executable repository evidence as authoritative.
- Represent missing evidence explicitly instead of estimating or defaulting a score.
- Derive JSON and HTML from one normalized, stably sorted data set.
- Prefer failed gates and missing evidence, then the largest perceptual, null-depth, and runtime gaps.
- Use the checked commit and stable metric case identity to make assignment repeatable.

## Instructions
1. Install the five-minute runner from an authenticated Paperclip process with:
   `powershell -File scheduler\Install-ReverbQueueTask.ps1`
   The installer stores runtime configuration in Windows Credential Manager and puts no credential
   in the task definition. Repeating installation updates the same enabled task.
2. The scheduled action invokes only `scripts\cli.py run-once`. It first queries live issues for the
   configured exact General Software Engineer id. A `todo` or `in_progress` issue exits successfully
   before repository metrics or artifact writes. An `in_review` or `blocked` issue does not occupy
   the runnable-work slot.
3. Run a manual refresh with:
   `python C:\Code\agent-prompts\roles\prompt-engineer\reverb-priority-automation\scripts\cli.py refresh --repo C:\Code\mix-tool`
4. Refresh fetches `origin/master`, uses a temporary detached worktree when the persistent checkout
   differs, and runs the production `reverb_corpus_report` entrypoint there. It records the evaluated
   commit in JSON and HTML without modifying the persistent checkout.
5. Supply `--report` only for deterministic fixture or replay validation. Production schema version
   1 maps every room's PU and paired null depth to numeric queue rows. Runtime and negative-control
   pass booleans remain report evidence and are never converted to invented runtime measurements.
6. Invoke completion or merge dispatch manually only for diagnostics with:
   `python C:\Code\agent-prompts\roles\prompt-engineer\reverb-priority-automation\scripts\cli.py event issue-completed --repo C:\Code\mix-tool`
   or replace `issue-completed` with `merge`.
7. Dispatch requires API URL, key, company identifier, run identifier, and exact engineer identifier
   through command options, runtime environment, or the scheduler credential. Only agent id
   `32cdb55f-fa10-40f3-929d-cf50b4dc3e10` is allowed.
8. Open `artifacts\reverb-queue.html` directly in a browser. It has no server or external dependency.
9. Uninstall with `powershell -File scheduler\Uninstall-ReverbQueueTask.ps1`.
10. Retire the skill after fewer than eight validated, metric-preserving or metric-improving changes
   in its first ten assignments, or after three incorrect or duplicate assignments. Preserve the
   deterministic metric report and return to manual issue creation.

## Output
Refresh writes:

```text
artifacts\reverb-queue.json
artifacts\reverb-queue.html
```

Each row records rank, repository case, current metric, target, gap, priority reason, task status,
issue identifier, evidence command, relevant files, and done gate. A generated issue carries one
metric gap, baseline, target, exact reproduction command, relevant files, and measurable completion
gate.

## Rules
- Never invent, infer, or silently default a metric.
- Never dispatch while any `todo` or `in_progress` issue is assigned to the General Software
  Engineer.
- Never create more than one issue per dispatch invocation.
- Never repeat an issue for the same repository commit and metric case identity.
- Never change `C:\Code\mix-tool`; generated work belongs to the engineer.
- Never create a sleep loop, polling loop, scheduled heartbeat, agent routine, or status-report path.
  The single five-minute operating-system task may invoke only the deterministic run-once command.
- Never reorder HTML independently from queue JSON.
- Never route generated work to another actor.
- Require changes to land on `master` through the repository's checked branch and review workflow.
