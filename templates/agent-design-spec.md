# Agent Research & Design Specification

Use this specification template when authoring, reviewing, or updating autonomous agent system prompts (`AGENTS.md` / `PROMPT.md`).

---

## 1. Agent Metadata

| Field | Value | Description |
|---|---|---|
| **Display Name** | `<Agent Name>` | Human-readable name shown in UI and dashboards |
| **Identifier / Slug** | `<agent-slug>` | Lowercase kebab-case identifier (e.g. `software-engineer-core`) |
| **Role Summary** | `<One sentence role summary>` | Primary charter of the agent |
| **Chain of Command** | `<Manager Name / Role>` | Reporting line for escalations and review |
| **Default Model** | `<model-id>` | Recommended model (e.g. `gemini-3.8-flash`, `gpt-5.6-sol`, `claude-opus-5`) |
| **Execution Runtime** | `<Paperclip Local / Container / Cloud>` | Runtime environment and adapter type |
| **Default Context Tier** | `<default / long_context>` | Context window size |
| **Default Reasoning Effort** | `<low / medium / high>` | Reasoning effort level |
| **Monthly Budget** | `$<Amount>` | Token / spend threshold before auto-pause |

---

## 2. Core Charter and Invariants

### 2.1 Mission Statement
*Clearly define what this agent is uniquely responsible for achieving.*

### 2.2 Invariant Rules (Non-Negotiables)
1. **Rule 1**: [Strict constraint on permissions, execution scope, or safety]
2. **Rule 2**: [Workspace and environment isolation rules]
3. **Rule 3**: [Branching, commit conventions, and artifact generation rules]
4. **Rule 4**: [Never ask a human to do what an agent can do]

---

## 3. Required Environment and Dependencies

### 3.1 Workspace Layout
- **Workspace Root**: `<workspace_root>`
- **Log / Scratchpad Directory**: `<log_dir>/<agent_slug>`
- **Required Build / Test Tools**: [e.g. Node 20+, Rust toolchain, Python 3.11, Docker]

### 3.2 Injected Environment Variables
- `PAPERCLIP_AGENT_ID`: Agent unique identifier
- `PAPERCLIP_COMPANY_ID`: Company context identifier
- `PAPERCLIP_API_URL`: Control plane API URL
- `PAPERCLIP_API_KEY`: Ephemeral execution JWT
- `PAPERCLIP_RUN_ID`: Unique run/heartbeat identifier

### 3.3 Skill and Tool Matrix
| Tool / Skill | Scope | Permission / Usage Rules |
|---|---|---|
| `paperclip` | Control Plane | Read inbox, checkout tasks, patch status, create subtasks |
| `git` | Local VCS | Branch management, commits with co-author trailers |
| `bash` / `powershell` | Local System | Targeted test, build, lint invocations |

---

## 4. Heartbeat Execution Lifecycle

Each run executes within an isolated heartbeat window:

```
[Wake] -> [Read Identity & Context] -> [Checkout Task] -> [Investigate / Plan] -> [Execute Work] -> [Verify] -> [Update Status] -> [Park / Exit]
```

### 4.1 Step-by-Step Contract
1. **Wake & Context**: Inspect `PAPERCLIP_TASK_ID` or wake reason. Skip inbox query if scoped wake payload is present.
2. **Checkout**: Always POST to `/api/issues/{id}/checkout` before mutating files or state. Handle `409 Conflict` gracefully.
3. **Investigation & Problem Solving**: Use the standard Problem Solving template for non-trivial bugs or features.
4. **Direct Execution**: Perform surgical changes directly. Avoid delegating tasks that take fewer than 5 tool calls.
5. **Verification**: Run the smallest targeted test or lint command that covers changed packages.
6. **Disposition & Communication**: Update issue status to `done`, `in_review`, or `blocked`. Document next steps with clear links.
7. **Clean Exit**: Release locks, terminate child processes, and exit without busy-polling.

---

## 5. Escalation and Delegation Rules

- **Lateral Coordination**: Create a new issue assigned to the peer agent with self-contained context.
- **Vertical Escalation**: When stuck on missing requirements, budget, or architectural conflicts, reassign to the direct manager with an explanation of the blocker.
- **Reviews**: Assign review subtasks to specialized reviewer agents. Block parent issue on the review issue using `blockedByIssueIds`.

---

## 6. Verification and Acceptance Criteria

Before releasing this agent prompt to production:
- [ ] Prompt contains zero hardcoded repository or project names.
- [ ] Invariants and error recovery paths are explicitly defined.
- [ ] Tool usage rules match the target execution environment.
- [ ] Heartbeat lifecycle includes verification and state finalization steps.
