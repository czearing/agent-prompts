# Agent Parking & Execution Contract Block

Include this standard contract block in agent prompts (`AGENTS.md`) to govern how the agent safely halts, parks, or delegates work without wasting runs or busy-polling.

---

## Agent Execution & Parking Contract

### 1. Invariants
- **No Busy-Polling**: Never stay in a loop sleeping or polling for asynchronous external tasks, builds, child issues, or reviewer comments.
- **Explicit Blockers**: If an issue is waiting on external dependencies or subtasks, set `blockedByIssueIds` with the blocking issue IDs and change status to `blocked`. Paperclip automatically wakes you when blockers resolve (`PAPERCLIP_WAKE_REASON=issue_blockers_resolved`).
- **Explicit Review Paths**: When work requires external review or human sign-off, transition the issue to `in_review`, provide clear review artifacts, and exit the heartbeat.
- **Clean Heartbeat Termination**: Every run must end cleanly by updating the checked-out issue to its final disposition (`done`, `in_review`, `blocked`, or re-assigned) and shutting down child processes.

### 2. State Transition Rules

| Current State | Condition | Next State | Action Required |
|---|---|---|---|
| `in_progress` | All work complete and verified | `done` | Update issue with summary of changes, commit SHAs, and test results. |
| `in_progress` | Dependent subtasks created and running | `blocked` | Set `blockedByIssueIds: [child_id]` so runtime auto-resumes upon child completion. |
| `in_progress` | Awaiting human approval or PR review | `in_review` | Link PR / work product and post review request. |
| `in_progress` | Hit unrecoverable blocker or missing permission | `blocked` | Reassign or escalate to manager with exact blocker details. |
| `todo` | Picked up during heartbeat | `in_progress` | Checkout task via `/api/issues/{id}/checkout` before making changes. |

### 3. Review Delegation Contract
When delegating reviews to peer agents:
1. Create a self-contained subtask assigned to the reviewer agent.
2. Instruct the reviewer to post findings directly on their assigned subtask and mark it `done`.
3. Block your parent issue on the reviewer's subtask.
4. When the subtask is marked `done`, Paperclip wakes the parent assignee automatically to process findings.
