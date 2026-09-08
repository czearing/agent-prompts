# Staffing and Communication Decision Log

## 1. Context and Problem Understanding

### Request as Stated
Create a minimal, clean, project-independent prompt and detailed task template for a general software
engineer, then hire that agent to work on assigned build and coding tasks.

### Outcome Actually Wanted
Assigned software tasks in the current or any later repository are implemented to repository
standards, supported by behavior-focused assertions and validation evidence, and returned without the
requester having to recreate engineering instructions for every task.

### Current Roster
Roster and issue history refreshed on 2026-09-08 at 22:09 UTC with
`GET /api/companies/b79d2ec4-c320-4bb0-b48e-35c0815844c0/agents` and the company issue list.

| Agent | Owns today | Spend / budget | Last heartbeat | Issues closed recently |
| --- | --- | --- | --- | --- |
| Prompt Writer | Prompt, template, and skill design | $0.66 / $0.00 | 2026-09-08 21:38:23 UTC | MUS-5, General Software Engineer prompt and template |
| Chief of Staff | Roster, routing, and staffing decisions | $1.79 / $0.00 | 2026-09-08 21:58:40 UTC | MUS-4, General Software Engineer staffing decision |
| General Software Engineer | Assigned repository implementation, assertions, and validation | $0.00 / $0.00 | No heartbeat yet | None, hired from MUS-4 |

### Constraints
The role must remain portable across repositories, obey each repository's local instructions and
tooling, use a lean prompt plus a detailed companion template, and make only evidence-backed claims.
Prompt Writer owns prompt authoring. The Chief of Staff owns staffing but must not author the prompt.
Neither pre-existing agent owns implementation work or should receive repository write authority.
The Chief of Staff now has agent creation permission. The new engineer has repository write
authority only for work named in assigned issues and cannot create agents.

## 2. Escalation Ladder

| Rung | Verdict | Reason | Owner if chosen |
| --- | --- | --- | --- |
| Deterministic script or hook | Rejected | A hook can enforce mechanical checks, but it cannot interpret an arbitrary task, diagnose a root cause, choose a safe implementation, or judge whether assertions prove behavior. | None |
| Edit an existing agent's prompt | Rejected | Prompt Writer must remain the sole prompt author and Chief of Staff must remain the roster owner. Adding repository implementation to either prompt would combine unrelated write authorities and decisions. | None |
| New skill on an existing agent | Rejected | General software delivery is a persistent ownership area, not a bounded reusable procedure. Granting it as a skill would still give an existing governance role conflicting repository write authority. | None |
| New agent | Chosen | A dedicated engineer is the first rung that can own implementation judgment and repository writes without weakening the two existing roles. | General Software Engineer |

### Chosen Rung
Hire a General Software Engineer. The work is variable and judgment-heavy, so deterministic
enforcement is insufficient. The existing roles have distinct governance and prompt-authoring
authority, and a skill would not resolve that ownership conflict.

## 3. Communication Path

### Path
Requesting issue owner -> General Software Engineer -> requesting issue owner. Two hops and one round
trip per unit of work.

### Who Absolutely Must Be Told

| Agent | Must act on what | Why an artifact is not enough |
| --- | --- | --- |
| General Software Engineer | Implement the assigned behavior in the named repository and return the validated deliverable | The task needs codebase-specific diagnosis, edits, assertions, and validation |

Prompt Writer is told once during setup to create the role artifacts. Chief of Staff consumes those
artifacts to create the roster entry. Neither belongs in the recurring task path.

### Round Trip Check
The requesting issue owner provides one complete issue artifact. The General Software Engineer
returns one completed change artifact through the same issue. This is one round trip. No adjacent
pair exceeds one round trip, so no merge is required.

## 4. Cost and Risk

[x] Is the recurring cost of this verdict lower than the cost it removes? Yes. One engineering
heartbeat per assigned task replaces repeated prompt construction and routing through a non-owner.
[x] Does this add a hop to any path that already worked? No. No implementation path exists in the
live roster.
[x] Does this create a second writer on any artifact or surface? No. The engineer writes only in the
repository assigned by its issue.
[x] Does any agent now have to report status that nobody acts on? No. The engineer returns the
deliverable to the requesting issue and does not send status reports.
[x] Can this be enforced deterministically instead of judged by an agent? No. Mechanical quality
rules can be checked by repository tooling, but task interpretation, design, scope, and assertion
quality require judgment.

### Cost Line
The verdict adds one agent heartbeat for each assigned coding task and maintenance of one prompt and
one template. It replaces repeated one-off engineering instructions and avoids routing coding work
through governance or prompt-authoring roles.

## 5. Role Brief

- Owned decision: For each assigned software task, decide the observable outcome, root cause or
  implementation approach, narrowest safe change, assertion strategy, and validation needed to call
  the task complete.
- Write authority: Read and modify source, tests, documentation, and configuration inside only the
  repository named by the assigned task. Create task branches, commits, and pull requests when the
  repository workflow requires them. Do not modify the roster, agent prompts, or unrelated projects.
- Workspace: The repository named in the assigned issue, beginning with `C:\Code\mix-tool`, plus the
  General Software Engineer task-log directory supplied by the runtime.
- Inputs: One assigned issue containing the desired observable behavior, repository location,
  constraints, and acceptance criteria, plus repository-local instruction files and existing
  build, test, formatting, and review conventions.
- Single upstream contact: The requesting issue owner.
- Single downstream contact: The requesting issue owner, through the completed issue and its code
  change, validation evidence, and pull request when applicable.
- Success metric: At least 9 of the first 10 assigned coding tasks reach a validated, reviewable
  change without reassignment or a clarification round trip, and all 10 record the exact assertions
  and commands that support completion claims.
- Retire condition: Retire or redesign the role if fewer than 8 of its first 10 assigned tasks reach
  a validated, reviewable change without reassignment, or if three consecutive tasks require another
  agent to correct unsupported assertions, repository-scope violations, or unrelated changes.

Prompt and template requirements for Prompt Writer:

1. Keep the prompt minimal and clean with Role, Methodology, Instructions, Output, and Rules.
2. Keep all guidance project-independent. The role must discover and follow the assigned
   repository's local instructions, package boundaries, commands, and conventions.
3. Require reproduction or a stated current behavior before a bug fix, root-cause reasoning,
   narrow scope, reuse of existing code, explicit error handling, and no unrelated cleanup.
4. Require assertions that prove observable behavior, fail for the pre-change behavior when
   applicable, avoid vague truthiness checks, and cover failure and boundary cases relevant to the
   change.
5. Require the smallest existing targeted validation first, followed by the repository's required
   gate when appropriate. Completion claims must cite actual command results.
6. Provide a detailed companion task template covering repository discovery, behavior and acceptance
   criteria, approach, changed surfaces, risk, assertion design, code-quality review, validation
   evidence, and final disposition.
7. Avoid language-specific, framework-specific, vendor-specific, and current-project-specific rules
   unless presented as examples to discover from the repository.
8. Give the engineer direct repository write authority for assigned work while excluding roster,
   prompt, unrelated repository, and pre-existing change ownership.

## 6. Validation and Evidence

### Test and Evaluation Plan
Test 1:
1. Give the role a bug task in `C:\Code\mix-tool`.
2. Confirm its task artifact records reproduction, root cause, a behavior-focused assertion that
   would fail before the fix, the narrowest change, and real validation output.
3. Confirm no unrelated file or repository is modified.

Test 2:
1. Give the same unchanged role a feature task in a repository with a different language and command
   set.
2. Confirm it discovers local instructions and existing tooling instead of assuming commands,
   frameworks, or directory structure.
3. Confirm its assertions map to acceptance criteria and its completion claims cite actual results.

### Evidence and Results
Baseline: The live roster had no software implementation owner. Prompt Writer had $0.66 spend and
completed MUS-5. Chief of Staff had $1.79 spend and owned the active MUS-4 staffing decision.

Outcome: Prompt Writer returned the project-independent role prompt at
`C:\Code\agent-prompts\roles\prompt-engineer\general-software-engineer-prompt.md` and task template at
`C:\Code\agent-prompts\roles\prompt-engineer\general-software-engineer-task-template.md`. The role has
distinct decision and write authority, a two-hop recurring message path, a numeric success metric,
and a retire condition. The Chief of Staff permission grant became active, and
`POST /api/companies/b79d2ec4-c320-4bb0-b48e-35c0815844c0/agent-hires` created General Software
Engineer `32cdb55f-fa10-40f3-929d-cf50b4dc3e10` on 2026-09-08 at 22:09:30 UTC. The new agent reports
to Chief of Staff, has no scheduled heartbeat, and is idle until assigned repository work. A later
verification found that the original managed instructions did not name the required canonical
template path. Prompt Writer corrected the artifact before the engineer's first heartbeat. Activation
of that correction is tracked in
`C:\Code\agent-prompts\roles\chief-of-staff\general-software-engineer-template-location-correction-decision.md`.

### Hire Execution

- Agent ID: `32cdb55f-fa10-40f3-929d-cf50b4dc3e10`
- Reports to: Chief of Staff `a32dfbb1-f798-42dc-b8a8-4c06b32a2e73`
- Scheduled heartbeat: Off
- Retire condition to record on creation: Retire or redesign below 8 successful tasks in the first
  10, or after three consecutive tasks with unsupported assertions, repository-scope violations, or
  unrelated changes.

## 7. Execution Checklist

[x] Outcome restated without naming an org change
[x] Live roster pulled with real spend and heartbeat data
[x] Every ladder rung above the chosen one rejected in writing with a reason
[x] Communication path drawn with a hop count
[x] Round trip check run on every adjacent pair
[x] Cost line filled in
[x] Role brief complete with all required fields
[x] Exactly one issue filed to the owning agent, with the blocker edge set
[x] Success metric and retire condition recorded
[x] All placeholder text removed and the summary block reported

## Summary

Request: Assigned software tasks are implemented across repositories with strong code quality,
behavior-focused assertions, and evidence-backed completion without rewriting instructions each time.
Verdict: hire
Rejected: Script or hook cannot make implementation judgments; prompt edit would merge conflicting
role authority; a new skill would still place repository writes on a governance role.
Owner: General Software Engineer
Path: Requesting issue owner -> General Software Engineer -> requesting issue owner, 2 hops
Cost: One heartbeat per coding task plus one maintained prompt and template, replacing repeated
one-off engineering instructions and misrouted work.
Metric: At least 9 of the first 10 tasks reach a validated, reviewable change without reassignment or
clarification, with assertion and command evidence on all 10.
Retire: Retire or redesign below 8 of 10 successful tasks, or after three consecutive tasks with
unsupported assertions, scope violations, or unrelated changes.
Execution: General Software Engineer `32cdb55f-fa10-40f3-929d-cf50b4dc3e10` was created, reports to
Chief of Staff, and has no scheduled heartbeat. Its corrected canonical-template instructions remain
blocked from activation by the separate configuration permission recorded in the correction log.
Decision Log:
`C:\Code\agent-prompts\roles\chief-of-staff\general-software-engineer-decision.md`
