# Engineering Management Plan & Triage Template

Use this format when breaking down an epic, planning a sprint, or posting a project execution update.

---

## Epic Execution Plan & Triage Summary

| Field | Value |
|---|---|
| **Epic / Goal** | `[PREFIX-200](/PREFIX/issues/PREFIX-200): Next-Gen Authentication Service` |
| **Manager** | `[engineering-manager](/PREFIX/agents/engineering-manager)` |
| **Total Subtasks** | `<Count>` created / `<Count>` completed / `<Count>` in progress |
| **Status** | `in_progress` \| `in_review` \| `done` |

---

## 1. Executive Summary
`<Two to three concise sentences explaining the delivery status of the epic, milestone progress, and current sprint focus.>`

---

## 2. Work Breakdown & Subtask Allocation

| Subtask ID | Title | Assignee Agent | Dependencies | Status |
|---|---|---|---|---|
| `[PREFIX-201](/PREFIX/issues/PREFIX-201)` | Scaffold OAuth2 core service | `software-engineer-core` | None | `done` |
| `[PREFIX-202](/PREFIX/issues/PREFIX-202)` | Implement JWT session token store | `software-engineer-core` | `[PREFIX-201]` | `in_progress` |
| `[PREFIX-203](/PREFIX/issues/PREFIX-203)` | Automated PR review of OAuth service | `pr-reviewer` | `[PREFIX-201]` | `done` |
| `[PREFIX-204](/PREFIX/issues/PREFIX-204)` | Author Auth API documentation | `tech-writer` | `[PREFIX-202]` | `todo` |

---

## 3. Blockers & Dependency Tracking

### Active Blockers
- `[PREFIX-204](/PREFIX/issues/PREFIX-204)` is blocked on `[PREFIX-202]` completion.
- Dependency rule enforced: `blockedByIssueIds: ["PREFIX-202"]`.

### Resolved Blockers
- `[PREFIX-202]` unblocked automatically following `[PREFIX-201]` merge.

---

## 4. Milestone Timeline & Next Actions
1. **Current Priority**: Monitor completion of `[PREFIX-202]`.
2. **Next Trigger**: Auto-wake on child completion to initiate end-to-end integration test pass.
3. **Target Completion**: All subtasks scheduled to complete by milestone deadline.
