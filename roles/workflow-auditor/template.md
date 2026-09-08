# Workflow Audit Cycle Log

Cycle: <cycle slug>
Workspace: C:\Code\agent-prompts\roles/workflow-auditor
Date started: <date>
Wake: timed

## 1. Previous Cycle Read Back

Previous cycle log: <path, or none if this is the first cycle>

Every task and finding filed before this cycle, read from issue state and never from a status request.

| Issue | Surface and metric | Before number | Acceptance number | After number | Accepted or rescoped | Quality regression or rollback |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

Running success rate: <closed with a met acceptance number, over closed total>
[] Every previously filed item was read back and recorded
[] No agent was asked for a status
[] Every rescoped item has a one line reason recorded

## 2. Current Numbers

Numbers come from telemetry, timings, and the workspaces on disk.

| Surface | Metric name | Current number | Source or command | Gathered by hand |
| --- | --- | --- | --- | --- |
| Scripts an agent runs |  |  |  |  |
| Tool servers and adapters |  |  |  |  |
| Harness and run mechanics |  |  |  |  |
| Instruction quality |  |  |  |  |

Hand gathered twice check:
[] No number in this table was also gathered by hand in a previous cycle
[] If one was, a deterministic collector task was filed to ToolingEngineer and it is this
   cycle's one filed task

## 3. Candidates

| Candidate | Surface | Metric name | Current number | Target number | In scope |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

Out of scope items seen this cycle and stopped, with the reason:
<product code performance in the product monorepo is owned by PerfEngineManager and
SoftwareEngineerPerformance, and nothing here may write into that queue>

## 4. Selection

Selected candidate: <surface and metric>
Current number: <number>
Target number: <number>
Why it is worth one unit of the owner's time this cycle: <reason>

Passed over:
| Runner up | One line reason |
| --- | --- |
|  |  |

## 5. Exit Path

Exactly one path. Mark the one taken.

[] Path A. One task filed to ToolingEngineer
[] Path B. One instruction level finding handed up to ChiefOfStaff
[] Path C. Empty cycle, nothing filed

### Path A, task filed to ToolingEngineer
| Field | Value |
| --- | --- |
| Metric name |  |
| Current number |  |
| Target number |  |
| Reproduction command |  |
| Acceptance number |  |
| Issue id |  |

### Path B, instruction level finding handed to ChiefOfStaff
Filed only when all five parts below are present. See section 6.
| Field | Value |
| --- | --- |
| Agent and instruction file measured |  |
| Named workflow step |  |
| Proposed minimal edit, as a proposal and not an edit |  |
| Issue id |  |

### Path C, empty cycle
Reason no candidate cleared the threshold: <reason>
[] Nothing was filed
[] No work was invented to fill the cycle

## 6. Five Part Test Plan

Required for every instruction level finding. A finding missing any part is not filed, and the refusal
is recorded here instead.

| Part | Content |
| --- | --- |
| 1. Named workflow | <the exact workflow and step measured> |
| 2. Before measurement | <number, and the count of repeated runs behind it> |
| 3. Smallest possible edit | <the one minimal edit proposed, nothing more> |
| 4. After measurement | <number, over the same run count as the before measurement> |
| 5. Quality gate | <evidence the agent output contract and its issue acceptance are unchanged> |

[] All five parts are present
[] The before and after measurements use the same number of runs
[] The edit is minimal and touches one surface
[] The quality gate shows no regression in the output contract or issue acceptance
[] The proposal does not remove detail, examples, rules, or template sections for length or size
[] If any part is missing, the finding was refused and the missing part is named here

Refusal record, if any: <the finding refused and the part it lacked>

## 7. Write Boundary Review

[] No agent prompt, template, tool, script, configuration file, or repository file was changed
[] The only files written this cycle are this cycle log and the issues filed
[] At most one task was filed this cycle
[] No status was requested from any agent
[] No contact was made outside ChiefOfStaff upstream and ToolingEngineer downstream
[] Any defect inside an already handed over tool was routed on that tool's existing defect channel

Surfaces read this cycle: <paths and sources>
Files written this cycle: <paths>

## 8. Validation Tests

Both tests run every cycle against the record above.

Test 1, the role acts without touching anything:
[] The cycle log names the measured step, the current number, the target number, the reproduction
   command, and the acceptance number
[] Exactly one task was filed to ToolingEngineer
[] No agent instruction, tool, script, or repository file changed in this cycle

Test 2, the limits hold:
[] On a cycle where nothing cleared the threshold, the empty cycle was recorded and nothing was filed
[] A long instruction file that is slow but correct did not produce a size reduction proposal
[] A candidate instruction edit without before and after measurements or without the quality gate was
   refused and not filed

## 9. Execution Checklist

[] New cycle log created from the template, with no existing file overwritten
[] Previous cycle and every previously filed item read back, with after numbers recorded
[] Current numbers collected from telemetry and the workspaces, with a source recorded for each
[] Candidates recorded with numbers and an in scope decision
[] Selection recorded with the reason it is worth one unit of the owner's time
[] Runners up recorded with a one line reason each
[] Exactly one exit path taken and recorded
[] Five part test plan complete, or the finding refused and the refusal recorded
[] Write boundary review completed with no surface changed
[] Both validation tests recorded
[] All placeholder text removed
[] Summary block reported and the issue set to its final disposition

Retire condition check:
[] This is not the second consecutive cycle with no candidate above the threshold while the
   deterministic collectors already catch the same class of bottleneck
[] No proposal this cycle reduced instruction content for size alone
