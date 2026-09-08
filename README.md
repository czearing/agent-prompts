# Autonomous Agent Prompts, Roles & Templates

A production-grade, reusable collection of system prompts (`AGENTS.md` / `PROMPT.md`), persona specifications, communication skills, and operational templates for autonomous multi-agent software engineering organizations.

Designed for use with **[Paperclip](https://github.com/paperclipai/paperclip)**, **GitHub Copilot CLI**, and autonomous agent runtimes.

---

## Repository Structure

```text
.
├── LICENSE
├── README.md
├── roles/
│   ├── chief-of-staff/             # Executive governance, roster oversight, and triage
│   │   ├── PROMPT.md
│   │   ├── template.md
│   │   └── README.md
│   ├── prompt-engineer/            # Agent prompt design, optimization, and evaluation
│   │   ├── PROMPT.md
│   │   ├── agent-research-spec.md
│   │   ├── problem-solving-template.md
│   │   └── README.md
│   ├── engineering-manager/        # Epic decomposition, subtask planning, dependency graphs
│   │   ├── PROMPT.md
│   │   ├── template.md
│   │   └── README.md
│   ├── software-engineer/          # Full-stack implementation, bug fixing, unit testing
│   │   ├── PROMPT.md
│   │   ├── template.md
│   │   └── README.md
│   ├── pr-reviewer/                # Automated code review, security audits, severity reports
│   │   ├── PROMPT.md
│   │   ├── template.md
│   │   └── README.md
│   ├── pr-updater/                 # PR feedback resolution, CI failure fixes, conflict resolution
│   │   ├── PROMPT.md
│   │   ├── template.md
│   │   └── README.md
│   └── tech-writer/                # Comprehensive documentation, API references, architecture guides
│       ├── PROMPT.md
│       ├── template.md
│       └── README.md
├── skills/
│   └── roster-and-communication-design/  # Multi-agent coordination protocols & communication skills
│       └── SKILL.md
└── templates/
    ├── agent-design-spec.md        # Standard specification template for authoring new agent personas
    ├── decision-log-template.md    # Organizational & architectural decision record template
    ├── parking-contract-block.md   # Non-polling parking & execution contract block
    ├── problem-solving-template.md # Structured investigation & bug diagnosis template
    └── pr-review-template.md       # High-signal pull request review report template
```

---

## Agent Roles Overview

| Role | Hierarchy Level | Primary Charter | Recommended Models |
|---|---|---|---|
| **[Chief of Staff](roles/chief-of-staff/)** | Executive Orchestrator | Roster management, organization health, capacity allocation, cross-team triage | `claude-opus-5`, `gpt-5.6-sol`, `gemini-3.8-flash` |
| **[Prompt Engineer](roles/prompt-engineer/)** | Agent Architect | Prompt authoring, benchmark optimization, skill and tool design | `claude-opus-5`, `gpt-5.6-sol`, `gemini-3.8-flash` |
| **[Engineering Manager](roles/engineering-manager/)** | Team Manager | Epic decomposition, dependency graph design (`blockedByIssueIds`), milestone tracking | `gpt-5.6-sol`, `claude-sonnet-5`, `gemini-3.8-flash` |
| **[Software Engineer](roles/software-engineer/)** | Individual Contributor | Feature development, bug fixing, refactoring, targeted testing | `claude-sonnet-5`, `gpt-5.6-sol`, `gemini-3.8-flash` |
| **[PR Reviewer](roles/pr-reviewer/)** | Individual Contributor | Objective code reviews, security analysis, severity ranking, before/after fixes | `claude-opus-5`, `gpt-5.6-sol`, `gemini-3.8-flash` |
| **[PR Updater](roles/pr-updater/)** | Individual Contributor | Resolving review comments, addressing CI/test failures, merge conflict resolution | `claude-sonnet-5`, `gpt-5.6-sol`, `gemini-3.8-flash` |
| **[Tech Writer](roles/tech-writer/)** | Individual Contributor | High-volume documentation passes, API references, onboarding guides | `claude-sonnet-5`, `gpt-5.6-sol`, `gemini-3.8-flash` |

---

## Core Invariants & Operating Rules

All agent prompts in this repository adhere to standard autonomy principles:

1. **Rule #1: Never ask a human to do what an agent can do.** Decompose, delegate, and execute autonomously. Escalate to human operators only for security permissions, credentials, or public commitments.
2. **Heartbeat Lifecycle Discipline**: Every agent operates within a bounded execution window:
   ```
   [Wake] -> [Read Identity & Context] -> [Checkout Task] -> [Investigate / Plan] -> [Execute Work] -> [Verify] -> [Update Status] -> [Park / Exit]
   ```
3. **No Busy-Polling**: Agents never sleep or loop waiting for external events. Long-running or asynchronous dependencies are managed via first-class `blockedByIssueIds`, waking agents upon completion (`issue_blockers_resolved` / `issue_children_completed`).
4. **Targeted Verification**: Every code modification must be verified using the smallest targeted test or lint command before concluding the task.
5. **Commit Attribution**: All Git commits include the standardized attribution trailer:
   ```text
   Co-Authored-By: Paperclip <noreply@paperclip.ing>
   ```

---

## Multi-Agent Coordination Protocols

Detailed in `skills/roster-and-communication-design/SKILL.md`:

- **The Courier Pattern (Lateral Coordination)**: Agents communicate across boundaries by creating self-contained subtasks for peer agents, linking dependencies via `blockedByIssueIds`.
- **The Delegated Review Pattern**: PR reviewers post findings and verdicts directly on their assigned subtasks and mark them `done`, waking the author agent to apply remedies.
- **Vertical Escalation**: When unrecoverable blockers or missing credentials arise, agents document the blocker in task comments and reassign the issue to their direct manager.

---

## Using These Prompts in Paperclip

To attach a role to an agent in Paperclip:

1. Copy the corresponding `PROMPT.md` content into your agent's configuration or point `instructions-path` to the file.
2. Ensure the agent has the `paperclip` skill attached in its configuration.
3. Configure the agent's chain of command (e.g. `software-engineer` -> `engineering-manager` -> `chief-of-staff`).

---

## License

This repository is licensed under the [MIT License](LICENSE).
