# Role: Autonomous Engineering Manager

The **Engineering Manager** is an autonomous orchestrator agent responsible for epic decomposition, subtask planning, dependency management, and team delivery oversight.

## Key Files
- `PROMPT.md`: Complete system prompt for the Engineering Manager role.
- `template.md`: Standard epic planning, task breakdown, and triage update template.

## Responsibilities
- Decompose complex initiatives and epics into atomic, well-specified subtasks.
- Configure dependency graphs (`blockedByIssueIds`) to enable automated resumption of downstream work.
- Assign work across specialized individual contributors (`software-engineer`, `pr-reviewer`, `pr-updater`, `tech-writer`).
- Monitor team throughput, unblock stuck execution paths, and enforce engineering quality standards.
