# Staffing and Communication Decision Log

## 1. Context and Problem Understanding

### Request as Stated
What was literally asked for:

### Outcome Actually Wanted
The result the requester needs, stated without naming any org change:

### Current Roster
Pull with GET /api/companies/{companyId}/agents and the recent issue history for each agent.

| Agent | Owns today | Spend / budget | Last heartbeat | Issues closed recently |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### Constraints
Budget, approval gates, write authority limits, and anything already in flight that touches this:

## 2. Escalation Ladder

Walk in order. Record a verdict and a reason for every rung before moving to the next. Stop at the
first rung that produces the outcome.

| Rung | Verdict | Reason | Owner if chosen |
| --- | --- | --- | --- |
| Deterministic script or hook |  |  |  |
| Edit an existing agent's prompt |  |  |  |
| New skill on an existing agent |  |  |  |
| New agent |  |  |  |

### Chosen Rung
Which rung produces the outcome, and why the cheaper rungs above it do not:

## 3. Communication Path

### Path
Draw the path end to end and count the hops:

### Who Absolutely Must Be Told
List only the agents that have to act. Anyone who only needs to know reads the artifact instead.

| Agent | Must act on what | Why an artifact is not enough |
| --- | --- | --- |
|  |  |  |

### Round Trip Check
For each adjacent pair on the path, how many round trips does one unit of work need? Any pair above
one is a merge candidate. Record the merge decision.

## 4. Cost and Risk

[] Is the recurring cost of this verdict lower than the cost it removes?
[] Does this add a hop to any path that already worked?
[] Does this create a second writer on any artifact or surface?
[] Does any agent now have to report status that nobody acts on?
[] Can this be enforced deterministically instead of judged by an agent?

### Cost Line
Recurring cost of the chosen verdict, and what it replaces:

## 5. Role Brief

Fill this section only when the verdict is hire. All seven fields are required.

- Owned decision:
- Write authority:
- Workspace:
- Inputs:
- Single upstream contact:
- Single downstream contact:
- Success metric:
- Retire condition:

## 6. Validation and Evidence

### Test and Evaluation Plan
Test 1:
1.

Test 2:
1.

### Evidence and Results
Baseline:

Outcome:

## 7. Execution Checklist

[] Outcome restated without naming an org change
[] Live roster pulled with real spend and heartbeat data
[] Every ladder rung above the chosen one rejected in writing with a reason
[] Communication path drawn with a hop count
[] Round trip check run on every adjacent pair
[] Cost line filled in
[] Role brief complete with all seven fields, or marked not applicable
[] Exactly one issue filed to the owning agent, with the blocker edge set
[] Success metric and retire condition recorded
[] All placeholder text removed and the summary block reported
