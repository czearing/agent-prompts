# Problem-Solving & Execution Log

Use this structured log template during complex investigation, bug diagnosis, and feature execution. Keep this document updated in the agent's scratchpad or issue document.

---

## 1. Issue Overview
- **Issue ID**: `<PREFIX-123>`
- **Title**: `<Issue Title>`
- **Assignee**: `<Agent Name>`
- **Goal**: `<One to two sentence definition of what success looks like>`

---

## 2. Initial Assessment & Diagnostic Plan

### 2.1 Symptom Analysis
- What failed or is behaving unexpectedly?
- What is the expected behavior?
- Error messages, stack traces, or relevant telemetry:
  ```text
  <Paste error snippets, stack traces, or logs here>
  ```

### 2.2 Working Hypotheses
1. **Hypothesis A**: [Explanation of potential root cause]
2. **Hypothesis B**: [Alternative explanation]

### 2.3 Diagnostic Plan
- [ ] Inspect relevant source files: `path/to/source.ts`
- [ ] Reproduce issue using targeted test command
- [ ] Inspect runtime logs and environment configuration

---

## 3. Findings & Root Cause Analysis

### 3.1 Investigation Notes
- **Source Analysis**: [What was found in the code]
- **Reproduction Output**: [Result of reproducing test or command]
- **Key Evidence**: [Lines of code, commit diffs, or API responses confirming the cause]

### 3.2 Confirmed Root Cause
`<Concise, technical description of the exact root cause>`

---

## 4. Implementation Plan

### 4.1 Surgical Changes Required
| File | Action | Summary of Changes |
|---|---|---|
| `src/core/example.ts` | Edit | Fix null check and validate input schema |
| `tests/unit/example.test.ts` | Edit / Create | Add regression unit test |

### 4.2 Potential Side Effects & Mitigations
- **Risk**: [Possible regression or edge case]
- **Mitigation**: [How the fix or test ensures safety]

---

## 5. Execution & Verification

### 5.1 Verification Commands Run
```bash
# Targeted test command
npm test -- tests/unit/example.test.ts

# Targeted typecheck / lint
npm run typecheck
```

### 5.2 Test Results
- Status: **PASSED** (or **FAILED** with follow-up action)
- Output Summary: `All 12 unit tests passed in 1.4s.`

---

## 6. Disposition & Handoff Summary

- **Status**: `done` | `in_review` | `blocked`
- **Work Products Created**:
  - Commit SHA: `<commit-sha>`
  - PR Link / Work Product: `<PR URL or Work Product ID>`
- **Next Steps**: [Handoff notes for reviewers, operators, or dependent tasks]
