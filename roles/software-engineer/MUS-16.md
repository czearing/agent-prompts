# Engineering Task Log

Task: MUS-16 Make wet-only reverb reliability queue complete
Branches: `mus-16-wet-only-matrix`; `mus-16-wet-only-queue`
Packages in scope: `mix-tool/audio-effects`; `reverb-priority-automation`
Date started: 2026-09-08

## 1. Context and Problem Understanding

### Problem Statement
The production reverb report must gate every supported oracle room and ordered pair of distinct
oracle sources using only an isolated wet reference during recovery. Incomplete and failed evidence
must keep the queue actionable. JSON and HTML must expose the same descending actionable order,
with satisfied evidence separate. One live idle run must create one exact-id assignment and a
repeat run must create none.

### Reproduction or Current Behavior
Before editing, this command ran successfully:

`cargo run -q -p audio-effects --bin reverb_corpus_report`

It emitted schema version 1 with exactly five room rows. Every row used one organ reference, one
piano target, and `Reference::Pair` built from both `dry_reference` and `wet_reference`. All five
rows passed PU and paired-null gates. No row identified an ordered source pair or wet-only mode.
The automation fixture had the same five-room shape, and `render_html` rendered actionable and
satisfied rows together in one table.

### Repository Discovery

| Path | Role in this task |
| --- | --- |
| `C:\Code\mix-tool\crates\audio-effects\src\reverb\corpus_report.rs` | Versioned production report and matrix declaration |
| `C:\Code\mix-tool\crates\audio-effects\src\reverb\corpus_report\matrix.rs` | Wet-only recovery and source-pair scoring |
| `C:\Code\mix-tool\crates\audio-effects\src\reverb\corpus_report\controls.rs` | Wrong-room and dry-input negative controls |
| `C:\Code\mix-tool\crates\audio-effects\tests\reverb_corpus_report.rs` | Exact matrix, mode, and control assertions |
| `C:\Code\agent-prompts\roles\prompt-engineer\reverb-priority-automation\scripts\report_schema.py` | Schema validation and missing-cell synthesis |
| `C:\Code\agent-prompts\roles\prompt-engineer\reverb-priority-automation\scripts\queue_core.py` | Gap calculation, ordering, and queue partition |
| `C:\Code\agent-prompts\roles\prompt-engineer\reverb-priority-automation\scripts\html_report.py` | Actionable and completed HTML tables |
| `C:\Code\agent-prompts\roles\prompt-engineer\reverb-priority-automation\scripts\issue_api.py` | Existing exact-id, one-at-a-time dispatch |

Instructions read: `C:\Code\mix-tool\AGENTS.md`. No additional instruction file exists in the
automation package or its repository root.

Reused code: `oracle::reverbs`, `oracle::sources`, `oracle::wet`, roommatch `analyze` and `apply`,
the existing report entrypoint, queue `normalize` and `write_artifacts`, and `dispatch`/`run_once`.

Owned files were limited to the report implementation and test, the automation package, generated
queue artifacts, and this task log. Unrelated dirty files in `C:\Code\agent-prompts` were untouched.

## 2. Thesis and Strategy

### Root Cause
The report hardcoded five room-level exact paired recoveries instead of enumerating the oracle
corpus and exercising the blind wet-only path, while the HTML treated all normalized evidence as
pending queue work.

### Narrowest Fix
Schema version 2 declares the oracle dimensions and emits one wet-only result for each
room/reference/target tuple. Recovery receives only `Reference::WetOnly`; truth IR and target truth
audio are used afterward for PU and rendered-output null scoring. The normalizer checks the
cartesian product, creates actionable missing rows, validates measured pass flags, and partitions a
single stable ordering into actionable and completed output. Existing dispatch remains unchanged.

### Alternatives Considered and Rejected
Expanding the old five room rows in Python was rejected because it would invent source-pair
evidence not measured by the repository. Keeping one PU and one null row per cell was rejected
because the requested atomic done gate includes PU, rendered-output null depth, and runtime
together. Aborting refresh on a measured negative-control failure was rejected after review because
it would leave stale artifacts instead of creating repair work.

### Scope Check
[x] The required cross-repository boundary is only versioned JSON.
[x] Existing report, queue, scheduler, and dispatch functions are reused.
[x] Schema meaning changed intentionally and the version was incremented.
[x] Every new or materially expanded authored source file is below 200 lines.
[x] No wait, retry, sleep, poll, heartbeat, or status-report path was added.
[x] Report generation, normalization, rendering, and dispatch callers were inspected.

## 3. Risk and Impact Analysis

| Risk | Who it affects | Evidence |
| --- | --- | --- |
| Missing or duplicate matrix cells hide work | Queue consumers | Omitted cell becomes the first actionable `missing` row; duplicate IDs reject |
| Dry source or truth IR leaks into recovery | Reverb users | Ship-gate implementation contains only `Reference::WetOnly`; truth scoring occurs after `analyze` |
| Runtime or pass flags disagree with values | Queue consumers | Schema rejects inconsistent runtime and aggregate pass flags |
| Completed rows appear pending | General Software Engineer | JSON/HTML order and table partition assertions |
| Failed controls stop refresh | General Software Engineer | Failed negative control becomes an actionable row |
| Duplicate work is created | General Software Engineer | Live first run created one issue; immediate repeat created zero |

[x] All changed function callers were checked.
[x] No accessibility, localization, keyboard, collaborative-data, or public API surface applies.
[x] Invalid, missing, declined, and failed evidence paths are explicit.

## 4. Performance Expectations Check

[x] Matrix size is bounded by declared oracle rooms and sources.
[x] Recovery is performed once per room/reference pair and reused across distinct targets.
[x] HTML partitions the normalized rows without another repository scan.
[x] No bundle or frequently rendered application component is involved.
[x] No resource polling or wait loop was added.
[x] Every matrix row records its measured recovery-plus-apply runtime against 5 seconds.

Result: pass. The evaluated matrix contains 896 bounded cells; every row carries finite runtime
evidence, and the report test completed in 360.43 seconds before test-level result caching reduced
duplicate generation.

## 5. Validation and Evidence

### Assertions

- `report_declares_and_fills_the_complete_wet_only_matrix` proves
  `16 * 8 * (8 - 1) = 896`, exact tuple membership, distinct sources, and pass-count accuracy.
- `every_ship_gate_cell_is_wet_only_and_has_complete_evidence` proves wet-only mode, runtime budget,
  exact done-gate presence, stable serialization, and passing wrong-room/dry controls.
- `test_omitted_matrix_cell_becomes_highest_priority_failure` removes one cell and proves it becomes
  an actionable `missing` row rather than success.
- Production normalization tests prove exact field values, pass/runtime consistency, counts, and
  that HTML actionable order equals JSON while the completed cell is absent from that table.
- Dispatch tests prove exact-id allowlisting, one creation per invocation, active-work exclusion,
  overlap exclusion, and commit-plus-case duplicate keys.

### Evidence

| Check | Command or steps | Actual result |
| --- | --- | --- |
| Pre-change reproduction | `cargo run -q -p audio-effects --bin reverb_corpus_report` | exit 0; schema 1, five passing paired rows |
| Report compilation | `cargo test -p audio-effects --test reverb_corpus_report --no-run` | exit 0 |
| Report behavior | `cargo test -p audio-effects --test reverb_corpus_report -- --test-threads=1` | exit 0; 2 passed; 360.43 seconds |
| Automation suite | `python -m unittest discover -s tests -p test_*.py -v` | exit 0; 16 passed |
| Scheduler suite | `powershell -NoProfile -ExecutionPolicy Bypass -File tests\test_scheduler.ps1` | exit 0; installer assertions passed |
| Python compile | `python -m compileall -q scripts` | exit 0 |
| Rust lint attempt | `cargo clippy -p audio-effects --lib --bins --tests -- -D warnings` | exit 101 on pre-existing `refmaster-core` `manual_is_multiple_of` and `too_many_arguments` findings |
| Final artifact check | compare actionable HTML IDs with JSON IDs | equal; 896 actionable, 0 completed, 896 total |
| First live run | `python scripts\cli.py run-once --repo C:\Code\mix-tool` | exit 0; `dispatched`, created count 1, `MUS-17` |
| Second live run | same command | exit 0; `runnable_work_exists`, created count 0 |

Final report evidence: evaluated mix-tool commit
`3a3e8fb9ad12716a3340106eeaf0ac77c6a49211`; matrix pass count 0; matrix total 896;
report SHA-256 `c7bf518f2ff37483f4885630604cfd489992f7e571a0037778e62f1085e0adf4`.
The first actionable cell is `cathedral--drums-to-noise-burst`; the live issue is `MUS-17`,
assigned to `32cdb55f-fa10-40f3-929d-cf50b4dc3e10`.

Artifacts:

- `C:\Code\agent-prompts\roles\prompt-engineer\reverb-priority-automation\artifacts\reverb-queue.json`
- `C:\Code\agent-prompts\roles\prompt-engineer\reverb-priority-automation\artifacts\reverb-queue.html`

## 6. Review of the Completed Diff

[x] Every changed line serves the wet-only matrix and actionable queue behavior.
[x] No unsafe casts, type suppression, or broad exception handling was introduced.
[x] No React code or design-token surface is involved.
[x] Names identify rooms, sources, evidence, and gates directly.
[x] Comments are limited to non-obvious behavior.
[x] No credential or secret was added.
[x] No em dash was added.
[x] Independent review finding about failed negative controls was resolved.

## 7. Execution Checklist

[x] Current behavior was recorded before code changes.
[x] Discovery, root cause, narrow fix, and rejected alternatives are recorded.
[x] Dedicated branches were created in both repositories.
[x] Exact regression assertions were added.
[x] Performance expectations and runtime evidence were recorded.
[x] Generated JSON and HTML were manually compared.
[x] No repository change-file convention exists.
[x] Targeted repository and dispatcher gates passed.
[x] Both branches were pushed and pull requests merged.
[x] Live single-dispatch and duplicate-prevention evidence was captured.
[x] No template placeholders remain.

Pull requests:

- `https://github.com/czearing/mix-tool/pull/4`, merged as
  `3a3e8fb9ad12716a3340106eeaf0ac77c6a49211`
- `https://github.com/czearing/agent-prompts/pull/2`, merged as
  `23f4b890a361b0a87a15252c6dd477133225bbcb`

Final disposition: completed. The control-plane rejected two attempted `in_review` transitions
because the already-merged pull requests left no pending review owner. The engineer slot was
temporarily released for the required live dispatch proof; completion is recorded through the
issue comment and runtime disposition channel.
