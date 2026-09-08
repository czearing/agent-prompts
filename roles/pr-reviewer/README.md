# Role: Autonomous Pull Request Reviewer

The **Pull Request Reviewer** is a dedicated code review agent that conducts structured, multi-dimensional code reviews on pull requests and code diffs.

## Key Files
- `PROMPT.md`: Complete system prompt for the PR Reviewer role.
- `template.md`: Standard review report template with severity ranking.

## Responsibilities
- Evaluate pull requests for logic correctness, security vulnerabilities, performance regressions, and test coverage.
- Generate high-signal, severity-ranked review reports with concrete code remediation blocks.
- Provide objective verdicts (`APPROVE`, `REQUEST_CHANGES`, `COMMENT`).
- Record review completion as a first-class deliverable (`done` state).
