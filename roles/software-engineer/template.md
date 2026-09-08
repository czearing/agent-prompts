# Software Engineer Task Completion Template

Use this format when updating an issue after implementing a fix, feature, or refactoring.

---

## Task Completion Summary

| Field | Value |
|---|---|
| **Issue** | `[PREFIX-123](/PREFIX/issues/PREFIX-123)` |
| **Branch** | `feature/example-branch` |
| **Commit SHA** | `abc1234def5678` |
| **Status** | `done` \| `in_review` \| `blocked` |

---

## 1. Summary of Changes
`<One to two concise sentences describing the problem solved and the implementation approach.>`

---

## 2. Modified Files
- `src/core/handler.ts`: Added error boundary and graceful timeout handling.
- `src/utils/validate.ts`: Fixed schema validation for null/undefined payload attributes.
- `tests/unit/handler.test.ts`: Added regression test coverage for timeout edge cases.

---

## 3. Verification & Test Results

```bash
# Test command executed:
npm test -- tests/unit/handler.test.ts
```

- **Result**: PASSED (6 passed, 0 failed, 0 skipped)
- **Duration**: 1.2s
- **Linter / Typecheck**: Clean (0 errors, 0 warnings)

---

## 4. Work Products & Next Steps
- **Pull Request**: `[PR #45](/PREFIX/pulls/45)` (Work Product attached)
- **Reviewer**: Assigned to `[pr-reviewer](/PREFIX/agents/pr-reviewer)`
- **Next Action**: Subtask `[PREFIX-124](/PREFIX/issues/PREFIX-124)` opened for automated review.
