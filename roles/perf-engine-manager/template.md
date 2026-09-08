# Perf Engine Cycle Log

Cycle: <timestamp of this wake>
Wake reason: <timer | engine defect issue | task defect issue>
Workspace: <perf_tool_workspace>
Date: <date>

## 1. Context From the Rollup

Read the derived rollup. Do not reconstruct history by asking anyone.

### Rollup Summary
Last cycle and what it did:
Example: Previous cycle wrote one task on cold start time and recorded the transition.

### Open Tasks Previously Written
| Issue | Metric | Current number written | Target number | Status now |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### Results Read From Issue State
| Issue | Before number | After number | Accepted, rescoped, or task defect filed | Note |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Acceptance rate so far, share of written tasks accepted and closed without rescoping:
Target is above 80 percent.

Task defects received so far, counted the same way a rescope is:

## 2. Defect Triage

Fill this section only when a defect issue is waiting.

### What Was Reported
What happened:

What should have happened:

Surface reported: <engine surface, or task-brief>

### Verdict
Perf tool fix, scaffold fault, or task defect, and the reason:
Example: The issue writer dropped the reproduction command, which lives in the perf tool configuration,
so this is a perf tool fix.

| Check | Answer |
| --- | --- |
| Does the fault live in code this agent owns? |  |
| Does the fault live in the shared scaffold? |  |
| Does the fault live in a task this agent wrote? |  |
| Was it fixed this wake, or filed up and blocked on? |  |

Scaffold issue filed: <id, or not applicable>

### Task Defect Verdict
Fill this only when the surface reported is task-brief. Exactly one outcome per task defect.

| Defect issue | Task issue | Field reported wrong | Outcome | Number behind the outcome |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Outcome is one of corrected in place, withdrawn, or rejected.
Example: Rejected. The reproduction command produced 1420 ms, which is the current number the task
states, so the brief was right.

[] Exactly one outcome was recorded for each task defect received
[] A corrected task was updated in place and its defect closed, which cleared the blocker
[] A withdrawn task was cancelled and its slot left to the next cycle, with no replacement hand written
[] A rejected defect was closed carrying the number that shows the brief was right
[] No comment was left on the task and no ping was sent to the engineer

## 3. Collection and Selection

### Engine Run
Command: <command>
Hand edits to numbers, telemetry, or the acceptance check: none

### Candidates Collected
| Metric | Current number | Target number | Reproduction command | Gap |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### What the User Experiences
Answer these before ranking. Do not stop at the numbers already produced.
- Does the page load fast, and does it feel instant once it does?
- Does anything jitter, lag, or stall when someone interacts with a component?
- What part of that real experience does each candidate above actually stand in for?
- Is there a part of that experience nothing here measures at all?

### Coverage Gap
Fill this only when a real gap surfaced above, between what is collected and what the user experiences.
| What the user would notice | What is measured instead | Gap filed as |
| --- | --- | --- |
|  |  |  |

Scaffold issue filed for the gap: <id, or not applicable>

### Selection
Chosen candidate and why it is worth one unit of engineer time this cycle:
Example: Cold start regressed the furthest against its target and has a one command reproduction, so
one unit of time closes it.

| Passed over | Reason |
| --- | --- |
|  |  |

### Empty Cycle
Fill this only when no candidate cleared the threshold.

[] No candidate cleared the threshold
[] Telemetry record still written
[] No issue written
[] No work invented to fill the cycle
[] User experience questions were still answered and a coverage gap was still checked for

## 4. Task Written

Exactly one issue, assigned to SoftwareEngineerPerformance, no prose beyond these fields.

| Field | Value |
| --- | --- |
| Metric name |  |
| Current number |  |
| Target number |  |
| Reproduction command |  |
| Acceptance number that closes it |  |

Issue: <id>

[] The task carries a current number, so it was allowed to be written
[] Only one task was written this cycle
[] No status report was requested and no ping was sent

## 5. Telemetry

| Record | Written by | Confirmed |
| --- | --- | --- |
| Cycle record |  |  |
| Task transition records |  |  |

[] Every record was appended by the engine script, never by hand
[] A missing record was treated as an engine defect and fixed this wake

## 6. Boundary Review

[] Writes this cycle stayed inside the perf tool workspace
[] No write landed in the shared tooling scaffold
[] No performance fix was written in the product monorepo
[] No roster change and no agent creation
[] Only the four channels were used, with no fifth

## 7. Execution Checklist

[] Rollup read before anything else
[] Results read from issue state, with after numbers recorded
[] Defect triaged and routed, or marked not applicable
[] Every task defect settled with one outcome and the number behind it, or marked not applicable
[] Engine run with no hand edits
[] User experience questions answered and checked against every candidate
[] A real coverage gap was filed as a scaffold fault, or none was found
[] Selection recorded with runners up and reasons, or the empty cycle recorded
[] One conforming task written, or none written and the reason recorded
[] Telemetry confirmed for the cycle and every transition
[] Boundary review completed
[] All placeholder text removed and the summary block reported
