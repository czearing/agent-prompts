# Autonomous Agent Prompts, Roles & Templates

A production-grade, 1:1 collection of autonomous system prompts (`AGENTS.md` / `PROMPT.md`), persona specifications, communication skills, and operational companion templates for autonomous multi-agent software engineering organizations.

Designed for use with **[Paperclip](https://github.com/paperclipai/paperclip)**, **GitHub Copilot CLI**, and autonomous agent runtimes.

---

## Repository Structure

```text
.
├── LICENSE
├── README.md
├── roles/
│   ├── designer/                   # UI/UX design specs, design tokens, HTML/CSS component mockups
│   │   ├── PROMPT.md
│   │   └── templates/
│   │       ├── design-spec-template.md
│   │       └── component-spec-template.md
│   ├── food-scientist/             # DP recipe prediction, chemical compound balance, food science testing
│   │   ├── PROMPT.md
│   │   └── templates/
│   │       └── implementation-template.md
│   ├── chief-of-staff/             # Executive governance, roster oversight, and escalation ladder
│   │   ├── PROMPT.md
│   │   ├── template.md
│   │   └── README.md
│   ├── prompt-engineer/            # Agent prompt design, optimization, and companion specs
│   │   ├── PROMPT.md
│   │   ├── agent-research-template.md
│   │   ├── problem-solving-template.md
│   │   ├── park-contract-block.md
│   │   └── README.md
│   ├── software-engineer/          # General software implementation, bug fixes, targeted validation
│   │   ├── PROMPT.md
│   │   ├── template.md
│   │   └── README.md
│   ├── tech-writer/                # Documentation quality, verification against current source
│   │   ├── PROMPT.md
│   │   ├── template.md
│   │   └── README.md
│   ├── perf-engine-manager/        # Performance candidate selection, triage, and defect settlement
│   │   ├── PROMPT.md
│   │   └── template.md
│   ├── perf-reviewer/              # Performance review checklist, task brief checks, risk analysis
│   │   └── template.md
│   ├── pr-reviewer/                # Code review checklist, validation candidate lists
│   │   ├── PROMPT.md
│   │   ├── template.md
│   │   └── README.md
│   ├── pr-updater/                 # PR feedback resolution, CI failure fixes, conflict resolution
│   │   ├── PROMPT.md
│   │   ├── template.md
│   │   └── README.md
│   ├── tooling-engineer/           # Shared tooling scaffold, protocol surfaces, and handover gates
│   │   ├── PROMPT.md
│   │   └── template.md
│   ├── workflow-auditor/           # Measuring operator surfaces, 5-part test plans, minimal edits
│   │   ├── PROMPT.md
│   │   └── template.md
│   └── engineering-manager/        # Epic decomposition, subtask planning, dependency graphs
│       ├── PROMPT.md
│       ├── template.md
│       └── README.md
├── skills/
│   └── roster-and-communication-design/  # Multi-agent coordination protocols & communication skills
│       └── SKILL.md
└── templates/
    ├── design-spec-template.md           # 1:1 Book Cook Design Specification Template
    ├── component-spec-template.md        # 1:1 Book Cook Component Specification Template
    ├── food-science-implementation-template.md # 1:1 Book Cook AI Food Science Implementation & Testing Template
    ├── decision-log-template.md          # 1:1 Staffing & Architectural Decision Log
    ├── agent-research-template.md        # 1:1 Agent Design & Research Spec
    ├── problem-solving-template.md       # 1:1 Task Problem-Solving & Execution Log
    ├── park-contract-block.md            # 1:1 Agent Parking & Blocker Contract Block
    ├── task-template.md                  # 1:1 Engineering Task Log Template
    ├── documentation-edit-log-template.md# 1:1 Documentation Edit Log Template
    ├── pr-review-checklist.md            # 1:1 PR Review Checklist Template
    ├── perf-review-checklist.md          # 1:1 Perf Review Checklist Template
    ├── tooling-task-log.md               # 1:1 Tooling Task Log Template
    ├── workflow-audit-cycle-log.md       # 1:1 Workflow Audit Cycle Log Template
    └── perf-engine-cycle-log.md          # 1:1 Perf Engine Cycle Log Template
```

---

## Agent Roles & Methodologies

| Role | Hierarchy Level | Primary Charter | Companion Template |
|---|---|---|---|
| **[Designer (Book Cook)](roles/designer/)** | Individual Contributor | UI/UX design specifications, HTML/CSS component mocks, strict design tokens | `design-spec-template.md`, `component-spec-template.md` |
| **[Food Scientist (Book Cook AI)](roles/food-scientist/)** | Individual Contributor | DP recipe prediction, chemical compound balance, food science testing invariants | `implementation-template.md` |
| **[Chief of Staff](roles/chief-of-staff/)** | Executive Orchestrator | Roster decisions, escalation ladder (script -> prompt edit -> skill -> hire), message path design | `template.md` (Decision Log) |
| **[Prompt Engineer](roles/prompt-engineer/)** | Agent Architect | Authoring `AGENTS.md` & companion templates (Role, Methodology, Instructions, Output, Rules) | `agent-research-template.md`, `problem-solving-template.md`, `park-contract-block.md` |
| **[Software Engineer](roles/software-engineer/)** | Individual Contributor | Narrowest fix for root cause, pre-reproduction, performance expectation checks | `template.md` (Task Log) |
| **[Tech Writer](roles/tech-writer/)** | Individual Contributor | Documentation rewrites, commands & comments verification, exclusion checks | `template.md` (Doc Edit Log) |
| **[Perf Engine Manager](roles/perf-engine-manager/)** | Queue Owner | User-first candidate selection, rollup inspection, task defect settlement | `template.md` (Perf Cycle Log) |
| **[Tooling Engineer](roles/tooling-engineer/)** | Tool Architect | Shared tooling scaffold, protocol surface tests, 4 communication channels, handover gates | `template.md` (Tooling Task Log) |
| **[Workflow Auditor](roles/workflow-auditor/)** | Operations Auditor | Operator bottleneck measurement, 5-part test plans, minimal edits | `template.md` (Audit Cycle Log) |
| **[PR Reviewer](roles/pr-reviewer/)** | Quality Reviewer | Behavior, interaction, performance, and accessibility checks with pass/fail candidate lists | `template.md` (PR Review Checklist) |
| **[PR Updater](roles/pr-updater/)** | Individual Contributor | Resolving review feedback, addressing CI failures, merge conflict resolution | `template.md` |
| **[Engineering Manager](roles/engineering-manager/)** | Team Manager | Epic decomposition, dependency graphs (`blockedByIssueIds`), milestone tracking | `template.md` |

---

## Core Invariants & Operating Rules

All agent prompts in this repository adhere to standard Paperclip autonomy rules:

1. **Escalation Ladder Before Hiring**: The default answer to a hire request is no. A hire is only correct after a script, a hook, and a prompt edit have each been rejected in writing for a stated reason.
2. **Deterministic Rules in Scripts**: If a rule can be checked deterministically, it belongs in a script or hook, not in an agent prompt.
3. **No Busy-Polling & Explicit Parking**: Agents never loop or sleep waiting for asynchronous processes. When blocked, agents set `blockedByIssueIds` with an `unblockDescriptor` or schedule an explicit monitor.
4. **Verifiable Claims & Reproductions**: A bug fix requires reproducing current behavior before code is touched. A doc edit requires verifying every stated command and comment against current declarations.
5. **Zero Em Dashes**: Clean, standard punctuation across all prompts, templates, logs, and outputs.

---

## License

This repository is licensed under the [MIT License](LICENSE).
