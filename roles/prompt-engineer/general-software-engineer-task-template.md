# General Software Engineer Task Log

Replace the guidance in each required field with task-specific facts and evidence. Remove a
non-applicable field only after recording why it does not apply.

## Task Identity

- Assigned issue: Record the exact issue identifier and title.
- Requesting owner: Record the issue owner who receives the completed work.
- Repository: Record the exact repository path named by the issue.
- Task-log path: Record the exact saved path of this log.
- Started: Record the start date and time.
- Working state: Record the branch and any pre-existing modified or untracked files.

## 1. Repository Discovery

### Local Instructions
List every repository-local instruction file that governs the affected area and summarize the
constraint it adds.

| Instruction path | Scope | Constraint applied |
| --- | --- | --- |

### Package and Ownership Boundaries
Record the package, module, service, or other repository boundary that owns the behavior. State why
the task belongs there and whether the change crosses a boundary.

### Existing Commands and Conventions
Record only commands and conventions discovered in repository files or existing automation.

| Purpose | Exact command or convention | Source in repository |
| --- | --- | --- |

### Existing Code to Reuse
Identify established helpers, abstractions, patterns, fixtures, and test utilities that apply.

| Path and symbol | Existing responsibility | How this task reuses it |
| --- | --- | --- |

### Pre-existing Change Ownership
List modified or untracked files that existed before this task. State how the implementation avoids
overwriting, reverting, or claiming them.

| Path | Existing state | Ownership decision |
| --- | --- | --- |

## 2. Behavior and Acceptance Criteria

### Observable Outcome
State what a user, caller, operator, or external system can observe when the task is complete.

### Reproduction or Current Behavior
For a bug, record the exact reproduction performed before editing, including setup, action, and
observed result. If direct reproduction is unavailable, record the current behavior from concrete
evidence and explain why a direct reproduction cannot be run.

For new behavior, record the current limitation and what becomes possible after the change.

### Acceptance Criteria Map
Map every acceptance criterion to an assertion and validation source.

| Acceptance criterion | Observable proof | Assertion or check | Validation source |
| --- | --- | --- | --- |

## 3. Root Cause and Approach

### Root Cause or Implementation Approach
For a defect, state one precise cause that explains the observed behavior. For new behavior, state
the implementation approach and why it fits the owning boundary.

### Narrowest Safe Change
Describe the smallest complete change that removes the cause or adds the behavior. Identify what will
not change.

### Error Handling
List expected failure modes and how each is surfaced or propagated explicitly. Explain any retained
fallback using an existing repository contract.

| Failure mode | Expected handling | Existing contract followed |
| --- | --- | --- |

### Alternatives Rejected
Record credible alternatives and the concrete scope, duplication, compatibility, or correctness
reason each was rejected.

| Alternative | Reason rejected |
| --- | --- |

## 4. Changed Surfaces

List every file changed for the task. Every row must connect directly to the observable outcome,
assertion strategy, required documentation, or required configuration.

| Path | Surface type | Purpose of change | Ownership basis |
| --- | --- | --- | --- |

State whether a branch, commit, or pull request is required by repository workflow and record the
chosen delivery boundary.

## 5. Risk and Impact

Record realistic regressions, affected callers, compatibility concerns, data or state transitions,
and operational failure paths relevant to this change.

| Risk or boundary | Affected behavior or caller | Prevention | Detection before delivery |
| --- | --- | --- | --- |

### Scope Decision
State why the diff is the narrowest safe change. Account for all affected callers and explain why no
unrelated cleanup or second behavior is included.

## 6. Assertion Design

Each assertion must name an exact value, state, event, error, or externally visible effect. Do not
use vague truthiness when a precise expectation is available.

| Behavior proved | Test or check location | Exact assertion | Pre-change result | Expected result |
| --- | --- | --- | --- | --- |

### Failure and Boundary Cases
Record the cases relevant to the change, including invalid input, empty or limiting values,
dependency failure, repeated operation, ordering, concurrency, or compatibility only when those
risks exist.

| Case | Why relevant | Expected behavior | Assertion |
| --- | --- | --- | --- |

### Assertion Sufficiency
Explain why reverting the implementation would make the primary assertion fail when applicable.
Identify any acceptance criterion that cannot be automated and give its concrete manual proof.

## 7. Code-Quality Review

Record a finding and evidence for every review area. Use `not applicable` only with a reason.

| Review area | Finding | Evidence |
| --- | --- | --- |
| Observable correctness |  |  |
| Repository conventions and reuse |  |  |
| Scope and unrelated changes |  |  |
| Explicit error handling |  |  |
| Affected callers and compatibility |  |  |
| Failure and boundary behavior |  |  |
| Documentation and configuration accuracy |  |  |
| Pre-existing change preservation |  |  |

### Final Diff Inventory
Record the final changed-file list and confirm that each change belongs to this task. Distinguish
task-owned changes from pre-existing work.

## 8. Validation Evidence

Run the smallest existing targeted validation first. Run broader or repository-required gates after
the targeted result when the change or local workflow requires them. Record actual results only.

| Order | Validation purpose | Exact command or steps | Exit result | Relevant output | Disposition |
| --- | --- | --- | --- | --- | --- |

### Before and After Evidence
For a bug or changed behavior, record the failing or differing pre-change result and the passing
post-change result. If a pre-change command could not run, connect the stated current behavior to the
concrete evidence used instead.

### Validation Limits
Name every required or relevant check that did not run, the exact reason, and its effect on final
disposition. Do not describe an unrun check as passing.

## 9. Delivery

- Branch: Record the branch when repository workflow requires one.
- Commit: Record the commit identifier when repository workflow requires one.
- Pull request: Record the link and review state when repository workflow requires one.
- Issue update: Record the final update sent directly to the requesting owner.

## 10. Final Disposition

Choose and record exactly one disposition:

- Completed: The observable outcome, assertions, and required validation are complete.
- In review: The reviewable change is delivered through a real pending review path.
- Blocked: A named owner and concrete unblock action are recorded, and no unsupported completion
  claim is made.

### Completion Evidence
Summarize the evidence that supports the disposition.

| Claim | Exact supporting assertion, command result, or delivery artifact |
| --- | --- |

### Scope Confirmation
Record that only task-owned files inside the assigned repository and this task log were written.
Name any exception as a blocker rather than treating the task as complete.
