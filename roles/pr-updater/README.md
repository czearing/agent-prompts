# Role: Autonomous Pull Request Updater

The **Pull Request Updater** is an individual contributor agent specialized in resolving review comments, fixing CI/test breaks, resolving merge conflicts, and updating pull request branches.

## Key Files
- `PROMPT.md`: Complete system prompt for the PR Updater role.
- `template.md`: Standard resolution summary template.

## Responsibilities
- Parse and address reviewer feedback directly on PR source branches.
- Fix broken test suites, lint errors, and compiler failures.
- Resolve Git merge conflicts cleanly.
- Re-verify changes locally, push updated commits with proper trailers, and notify reviewers.
