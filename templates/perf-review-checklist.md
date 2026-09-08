# Perf Review Checklist

## Task Brief Check

Fill this before any code analysis. The task carries five fields and they are the brief.

| Field | Value on the task | Measured or confirmed |
| --- | --- | --- |
| Metric name |  |  |
| Current number |  |  |
| Target number |  |  |
| Reproduction command |  |  |
| Acceptance number |  |  |

Reproduction command output and the number it produced:

[] The reproduction command reproduces the stated current number
[] The acceptance number is reachable by a change to the named area
[] The change costs less than the number it recovers
[] The current number is still right when measured again

If every box above is checked, the brief is workable. Continue to Behavior and ignore the Task Defect
section. If any box is unchecked, the task is defective and is not yours to fix. Fill Task Defect and
stop.

## Task Defect

Fill this only when the brief is defective.

Which of the five fields is wrong:

The number that shows it is wrong:

Command run, exactly one and nothing else:
`node <perf_tool_workspace>/report-defect.js --task <taskIssueId> --surface task-brief --summary "<field and number>"`

Defect issue: <id>

[] Exactly one defect was filed for this task
[] The task was set blocked on the defect issue with blockedByIssueIds
[] PerfEngineManager is named as the unblock owner
[] The task was not rescoped, not closed without an after number, and no different work was chosen
[] No comment thread, second issue, or message to the manager was opened, and nothing was polled

## Behavior

### Purpose
What is the intention for the underlying code, how does the consumer use it, what are the upstream deps (is it private or public), etc.

What is the intention of our change to improve the performance.

### Testing
#### Risks
[] Does it add overhead for the long term maintenance of the project?
[] Is there somewhere better we can make the change (example: further upstream) 
[] How it affects accessibility?
[] How it affects upstream deps?
[] How will we catch each risk, and can that check actually see it (example: a warning the build hides by default)?
[] What's the impact here from any added latency from the additional await/network waterfall in the loader. What scenarios get faster from this change vs which get slower?
[] etc

Conclusion: Once we have evaluated and tested we should confirm whether this change is appropriate or too risky.

#### Validation
Test 1:
1. Example: We will ensure risk 1 is addressed by comparing other potential solutions to the status quo to ensure that this is the most effective solution

Test 2:
1. Start the app
2. Navigate to the home page
3. Press the button
4. etc

etc

#### Perf Validation
We will measure the performance by ___.

### Code Review Checklist
[] Is each file cleanly abstracted and using existing functions to do the job
[] Do files cleanly stay under 200 lines or should they be split apart
[] Is there any tools are functions in the repo or parameters elsewhere that we can leverage to minimize our changes
[] Is core functionality being tested
[] Do props of components have doc comments
[] Edge cases
[] Is everything localized
[] Is the change meaningful and worth merging
[] etc add more

## Implementation plan
[] Learn about the upstream consumers
[] Test base case risks before implementation
[] Start coding... etc etc
