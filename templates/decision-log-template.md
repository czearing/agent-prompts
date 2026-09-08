# Staffing & Architectural Decision Log

Use this template to record organizational structure, agent staffing, role definitions, and system architecture decisions.

---

## 1. Decision Metadata

| Field | Value |
|---|---|
| **Decision ID** | `DEC-<YYYYMMDD>-<SHORT-SLUG>` |
| **Date** | `<YYYY-MM-DD>` |
| **Author / Agent** | `<Agent Name or Role>` |
| **Status** | `PROPOSED` \| `APPROVED` \| `SUPERSEDED` \| `REJECTED` |
| **Related Issues / PRs** | `<Link to relevant tickets>` |

---

## 2. Context & Problem Statement
*Describe the situation, challenge, or organizational bottleneck that requires a decision.*

### Problem Summary
- What is currently inefficient, broken, or ambiguous?
- What triggered this evaluation?
- What are the constraints (budget, latency, accuracy, safety)?

---

## 3. Evaluated Options

### Option 1: [Short Title]
- **Description**: [How this option works]
- **Pros**:
  - Point 1
  - Point 2
- **Cons**:
  - Point 1
  - Point 2
- **Estimated Cost / Complexity**: [Low / Medium / High]

### Option 2: [Short Title]
- **Description**: [How this option works]
- **Pros**:
  - Point 1
  - Point 2
- **Cons**:
  - Point 1
  - Point 2
- **Estimated Cost / Complexity**: [Low / Medium / High]

---

## 4. Decision & Rationale

### Chosen Option
**Option [Number]: [Title]**

### Rationale
*Explain why this option was chosen over alternatives. Detail trade-offs accepted and expected benefits.*

---

## 5. Implementation & Delegation Plan

| Task ID | Action Item | Assignee Agent | Expected Outcome |
|---|---|---|---|
| 1 | Create new agent role specification | Prompt Engineer | New `AGENTS.md` committed |
| 2 | Provision agent in control plane | Chief of Staff | Agent active with budget & skills |
| 3 | Seed initial project backlog | Engineering Manager | Epics broken into prioritized tasks |

---

## 6. Follow-Up & Review Criteria
- How will success be measured?
- When should this decision be re-evaluated?
