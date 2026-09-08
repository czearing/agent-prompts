# Roster & Communication Design Skill

This skill defines best practices, interaction patterns, and coordination protocols for multi-agent autonomous organizations operating under Paperclip or similar control plane architectures.

---

## 1. Multi-Agent Roster Topology

An effective autonomous organization consists of a balanced hierarchy of **Executive Orchestrators**, **Engineering Managers**, and **Specialized Individual Contributors (ICs)**:

```
                  +--------------------------------+
                  |        Chief of Staff          |
                  | (Executive Governance/Roster)  |
                  +---------------+----------------+
                                  |
                  +---------------+----------------+
                  |      Engineering Manager       |
                  | (Epic Decomposition/Planning)  |
                  +---------------+----------------+
                                  |
        +-------------------------+-------------------------+
        |                         |                         |
+-------+--------+       +--------+-------+        +--------+-------+
|    Software    |       |   PR Reviewer  |        |  Tech Writer   |
|    Engineer    |       |  & PR Updater  |        | (Documentation)|
| (Implementation|       |  (Quality/CI)  |        |                |
+----------------+       +----------------+        +----------------+
```

---

## 2. Core Communication Patterns

### 2.1 The Courier Pattern (Lateral Coordination)
In subtree-scoped execution models, an agent executing an issue cannot write comments or mutate state on peer tasks outside its boundary.

**The Solution**: Use the Courier Pattern.
1. When Agent A needs assistance from Agent B, Agent A creates a **new issue** assigned to Agent B via `POST /api/companies/{companyId}/issues`.
2. The issue description must be **self-contained**, including all necessary context, requirements, file pointers, and expected deliverables.
3. If Agent A needs to wait for Agent B's result, Agent A sets `blockedByIssueIds: [agent_b_issue_id]` on its own task and transitions to `blocked`.
4. When Agent B completes the task and marks it `done`, the control plane automatically wakes Agent A with `PAPERCLIP_WAKE_REASON=issue_blockers_resolved`.

### 2.2 Delegated Review Pattern
When delegating code or design reviews:
1. Create a review subtask assigned to `pr-reviewer`.
2. Instruct the reviewer: **"Post your findings and verdict on your assigned review task and mark it `done`."**
3. The verdict is the deliverable: a review with change requests is still `done` (not `blocked`), because the review itself was successfully executed.
4. The author agent resumes upon review completion, reads the findings from the review subtask, and acts on them.

### 2.3 Vertical Escalation Pattern
When an IC agent encounters an unrecoverable blocker (e.g. missing permissions, architectural ambiguity, conflicting requirements):
1. Document the exact blocker in a structured task comment.
2. Reassign the task to the direct manager (e.g. `engineering-manager` or `chief-of-staff`).
3. Set status to `blocked` or `in_review`.
4. The manager agent wakes, triages the issue, resolves the ambiguity or provisions resources, and reassigns it back to the IC.

---

## 3. Issue-Thread Interactions vs. Standalone Decisions

| Feature | Issue-Thread Interaction | Standalone Decision |
|---|---|---|
| **Scope** | Confined to a single issue thread | Spans multiple issues, projects, or organization-wide |
| **Typical Use Cases** | Plan confirmation, file deletion confirmation, item verdicts | Reassigning blocked trees, clearing obsolete blockers, organizational restructuring |
| **Resolver Policy** | `anyone`, `not_creator`, `human_only`, `addresseeAgentId` | Board or executive authority |
| **Continuation Policy** | `wake_assignee`, `wake_assignee_on_accept`, `none` | `wake_origin_agent`, `none` |

---

## 4. Heartbeat Execution Invariants

1. **No Busy-Polling**: Never loop or sleep waiting for asynchronous processes. Rely on first-class blocker wakes (`issue_blockers_resolved`, `issue_children_completed`, `issue_commented`).
2. **Checkout Before Execution**: Always acquire task lock via `POST /api/issues/{id}/checkout` before modifying files or state. Handle `409 Conflict` by aborting immediately without retrying.
3. **Structured Ticket Links**: Always format ticket references as clickable internal links: `[PREFIX-123](/PREFIX/issues/PREFIX-123)`.
4. **Clean Heartbeat Termination**: Finalize task state (`done`, `in_review`, `blocked`) and terminate temporary child processes before exiting the heartbeat.
