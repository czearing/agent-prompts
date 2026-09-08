# Staffing and Communication Decision Log

## 1. Context and Problem Understanding

### Request as Stated
Correct the General Software Engineer setup because its prompt does not require use of the template
at `C:\Agent Specs\Software Engineer`, and the required template directory is empty.

### Outcome Actually Wanted
Every assigned engineering task starts from the canonical detailed task template stored under
`C:\Agent Specs\Software Engineer`, while the existing engineer remains portable across repositories.

### Current Roster
Roster and issue history refreshed on 2026-09-08 at 22:27 UTC with
`GET /api/companies/b79d2ec4-c320-4bb0-b48e-35c0815844c0/agents` and agent-filtered company issue
queries.

| Agent | Owns today | Spend / budget | Last heartbeat | Issues closed recently |
| --- | --- | --- | --- | --- |
| Prompt Writer | Prompt, template, and skill design | $1.19 / $0.00 | 2026-09-08 22:17:44 UTC | MUS-6, template location correction; MUS-5, initial artifacts |
| General Software Engineer | Assigned repository implementation, assertions, and validation | $0.00 / $0.00 | No heartbeat yet | None |
| Chief of Staff | Roster, routing, and staffing decisions | $11.28 / $0.00 | 2026-09-08 22:25:21 UTC | MUS-4, active staffing decision |

### Constraints
Prompt Writer remains the sole prompt author. Chief of Staff may apply returned instructions to the
existing roster entry but may not author them. The engineer has not run, so the correction must land
before its first task. The canonical template must be placed at
`C:\Agent Specs\Software Engineer\general-software-engineer-task-template.md`. The prompt must
explicitly require copying that file into the runtime-supplied task-log directory for each task.
The recurring task path must stay project-independent and must not gain another agent.

## 2. Escalation Ladder

| Rung | Verdict | Reason | Owner if chosen |
| --- | --- | --- | --- |
| Deterministic script or hook | Rejected | A copy operation can place a file, but it cannot correct the engineer's operating contract or make the managed instructions require the canonical template on every task. | None |
| Edit an existing agent's prompt | Chosen | The existing engineer has not run. Correcting its prompt and placing its canonical template produces the outcome without a new role, skill, or recurring hop. | Prompt Writer |
| New skill on an existing agent | Not reached | Template initialization is a core instruction for the existing role, not a separate reusable capability. | None |
| New agent | Not reached | The existing General Software Engineer already owns the required implementation decision and write authority. | None |

### Chosen Rung
Edit the existing General Software Engineer prompt. Prompt Writer will author the exact instruction
change and place the canonical template. Chief of Staff will apply the returned prompt to the existing
agent after the child issue completes.

## 3. Communication Path

### Path
Recurring work remains requesting issue owner -> General Software Engineer -> requesting issue owner,
two hops and one round trip. The one-time correction path is Prompt Writer -> Chief of Staff, one
handoff through the completed child issue artifact.

### Who Absolutely Must Be Told

| Agent | Must act on what | Why an artifact is not enough |
| --- | --- | --- |
| Prompt Writer | Correct the prompt and place the canonical task template at the required path | Prompt Writer owns prompt language and template authorship |
| Chief of Staff | Apply the returned prompt to the existing roster entry | Chief of Staff owns roster configuration |

### Round Trip Check
Prompt Writer receives one complete correction issue and returns one corrected prompt plus verified
template artifact. Chief of Staff applies it without a clarification exchange. Recurring engineering
work remains one round trip with no setup role in the path. No merge is required.

## 4. Cost and Risk

[x] Is the recurring cost of this verdict lower than the cost it removes? Yes. It adds no agent and
only maintains the existing prompt and template.
[x] Does this add a hop to any path that already worked? No. The recurring two-hop path is unchanged.
[x] Does this create a second writer on any artifact or surface? No. Prompt Writer authors the
artifacts and Chief of Staff only applies the returned managed instructions.
[x] Does any agent now have to report status that nobody acts on? No.
[x] Can this be enforced deterministically instead of judged by an agent? No. File placement can be
checked mechanically, but the operating contract must first be corrected by its prompt owner.

### Cost Line
The verdict adds one prompt correction and preserves one maintained prompt and template. It replaces
an invalid template-location assumption without adding a roster entry, heartbeat, skill, or recurring
handoff.

## 5. Role Brief

Not applicable. The chosen verdict updates the existing General Software Engineer and does not create
a role.

## 6. Validation and Evidence

### Test and Evaluation Plan
Test 1:
1. Verify `C:\Agent Specs\Software Engineer\general-software-engineer-task-template.md` exists.
2. Verify its content hash matches the canonical template returned by Prompt Writer.

Test 2:
1. Verify the corrected prompt names the exact canonical template path.
2. Verify it requires copying that template into the runtime-supplied task-log directory before work.
3. Verify the existing agent's managed instruction bundle contains the corrected prompt before its
   first heartbeat.

### Evidence and Results
Baseline: The live General Software Engineer has no heartbeat and no issue history. Its managed prompt
only says to create a task log from a companion template in a runtime-supplied directory. It does not
name `C:\Agent Specs\Software Engineer`. That directory exists and contains no files.

Outcome: Prompt Writer completed MUS-6. The corrected prompt is stored at
`C:\Code\agent-prompts\roles\prompt-engineer\general-software-engineer-prompt.md`, names the required
canonical path, and requires copying the template before implementation. The canonical source and
destination templates both have SHA-256
`DB934FAE62DA1F7E75BB79CF66A4654C9BFE73A1AEBAF3D5181C90ECD8F16A69`.

Configuration blocker: `PATCH /api/agents/32cdb55f-fa10-40f3-929d-cf50b4dc3e10` with the returned
instructions was rejected with `Missing permission: agents:configure or agents:suggest-changes`.
The engineer remains idle with no heartbeat, so no task has run under the stale configuration. The
board owner must grant Chief of Staff `agents:configure`, or apply the corrected prompt directly,
before the correction can be closed. Interaction `d62ea3c1-97a8-4669-8287-5cf61f6250fa` records
those two unblock actions and wakes the assignee after the completed action is submitted.

Blocker recheck: The completed MUS-6 child issue woke MUS-4 on 2026-09-08 at 22:22 UTC, but the
configuration interaction remained pending. A fresh managed instruction update returned the same
`Missing permission: agents:configure or agents:suggest-changes` denial. The live engineer remained
idle with no heartbeat and an unchanged configuration timestamp, so the corrected prompt was not
claimed as active. MUS-4 was returned to blocked rather than closed on incomplete configuration.

Resolved-blocker wake recheck: MUS-4 woke again on 2026-09-08 at 22:25 UTC because its child issue
blocker was resolved. The separate configuration interaction
`d62ea3c1-97a8-4669-8287-5cf61f6250fa` remained pending. One activation attempt through the general
agent update route returned an internal server error without changing the engineer's configuration.
Direct reads of the managed instruction bundle and configuration revisions both returned
`Missing permission: agents:suggest-changes`. The engineer remained idle, had no heartbeat, and kept
its 2026-09-08 22:09:30 UTC configuration timestamp. The hire is complete, but corrected prompt
activation is not complete and is not claimed as complete.

## 7. Execution Checklist

[x] Outcome restated without naming an org change
[x] Live roster pulled with real spend and heartbeat data
[x] Every ladder rung above the chosen one rejected in writing with a reason
[x] Communication path drawn with a hop count
[x] Round trip check run on every adjacent pair
[x] Cost line filled in
[x] Role brief marked not applicable because this is a prompt edit
[x] Exactly one correction issue specified for the owning agent, with a blocker edge required
[x] Existing success metric and retire condition remain unchanged
[x] All placeholder text removed and the summary block prepared

### Final Disposition

Blocked on the board owner granting Chief of Staff `agents:configure` or applying the corrected
prompt directly to General Software Engineer `32cdb55f-fa10-40f3-929d-cf50b4dc3e10`. No duplicate
agent or second child issue was created. MUS-4 is set to `blocked` on interaction
`d62ea3c1-97a8-4669-8287-5cf61f6250fa`.

## Summary

Request: Every engineering task starts from the canonical detailed template stored under
`C:\Agent Specs\Software Engineer`, with portable instructions across repositories.
Verdict: prompt edit
Rejected: A script or hook cannot correct the operating contract; a new skill is not needed for a
core instruction; a new agent would duplicate the existing unstarted engineer.
Owner: Prompt Writer authors the correction; General Software Engineer remains the recurring owner.
Path: Requesting issue owner -> General Software Engineer -> requesting issue owner, 2 hops. Prompt
Writer -> Chief of Staff is a one-time 1-hop correction.
Cost: One prompt correction with no new heartbeat or recurring hop, replacing the invalid template
location assumption.
Metric: The first engineer heartbeat uses a task log copied from the exact canonical path, and all
first 10 tasks record the required assertion and validation evidence.
Retire: Remove the fixed external template-path requirement if that directory is retired or replaced
by a runtime-enforced canonical template path.
Disposition: Blocked on the board owner applying the corrected managed instructions or granting
Chief of Staff `agents:configure`.
Decision Log:
`C:\Code\agent-prompts\roles\chief-of-staff\general-software-engineer-template-location-correction-decision.md`
