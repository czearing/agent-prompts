# Pull Request Review Report Template

Use this format when generating automated pull request review reports.

---

## Pull Request Review Summary

| Field | Value |
|---|---|
| **PR Title** | `<Pull Request Title>` |
| **PR Number / URL** | `<#1234 or PR Link>` |
| **Author** | `<Author Username or Agent Name>` |
| **Review Verdict** | `APPROVE` \| `REQUEST_CHANGES` \| `COMMENT` |
| **Risk Assessment** | `LOW` \| `MEDIUM` \| `HIGH` \| `CRITICAL` |

---

## 1. Executive Summary
`<One to two concise sentences summarizing what the PR achieves and the primary review verdict.>`

---

## 2. Issues & Findings Table

| # | Severity | Category | File & Location | Description | Recommendation |
|---|---|---|---|---|---|
| 1 | `CRITICAL` | Security | `src/auth/jwt.ts:45` | Missing token expiration validation | Validate `exp` claim before decoding payload |
| 2 | `HIGH` | Correctness | `src/api/handler.ts:112` | Unhandled Promise rejection on database timeout | Wrap in try/catch block and return 504 status |
| 3 | `MEDIUM` | Performance | `src/data/loader.ts:28` | N+1 database queries in list rendering | Batch queries using `IN (...)` or DataLoader |
| 4 | `LOW` | Code Quality | `src/utils/format.ts:8` | Redundant type cast | Remove unnecessary `as string` cast |

---

## 3. Detailed Review Feedback

### Finding 1: [Issue Title]
- **Severity**: `CRITICAL` | `HIGH` | `MEDIUM` | `LOW`
- **File & Line**: `path/to/file.ts:123`
- **Observation**: [Detailed explanation of the issue or risk]
- **Suggested Fix**:
  ```typescript
  // Before
  const result = await unsafeOperation();

  // After
  try {
    const result = await safeOperation();
  } catch (error) {
    logger.error("Operation failed", { error });
    throw new ServiceError("Operation failed gracefully");
  }
  ```

---

## 4. Verification & Testing Checklist
- [ ] Automated CI tests pass
- [ ] New unit or integration tests cover the changed functionality
- [ ] No performance regressions or bundle size anomalies
- [ ] Documentation updated to reflect changes

---

## 5. Next Steps
- **For Author**: [Specific action items needed to address findings]
- **For Reviewer**: [Follow-up verification once changes are pushed]
