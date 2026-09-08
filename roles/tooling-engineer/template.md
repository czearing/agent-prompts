# Agent Tooling Task Log

Task: <task title or id>
Repository: <agent_tooling_workspace>
Perf tool surface: <perf_tool_workspace>, writable only until the handover gate
passes
Date started: <date>

## 1. Context and Problem Understanding

### Request as Stated
What was literally asked for:
Example: Build the perf engine so the performance queue fills itself on a cadence.

### Capability That Must Exist
The capability stated without naming a file or a module:
Example: A timed job that collects real numbers, picks one candidate, writes one conforming task, and
records what it did.

### Placement Decision
Shared scaffold or one tool, and the reason:
Example: The wake, the telemetry writer and the issue writer go in the shared scaffold because the next
tool needs the same three. The metric collection goes in the perf tool because only perf measures it.

### Current State of the Surfaces
| Surface | Exists today | What is there | Who may write it |
| --- | --- | --- | --- |
| <agent_tooling_workspace> |  |  | This agent only |
| <perf_tool_workspace> |  |  | This agent until handover, then the tool owner |

## 2. Thesis and Strategy

### Shape of the Tool
The general shape every tool built on this scaffold takes:
Example: A command line entry point that runs wake, collect, select, write issue, append telemetry,
check acceptance, in that order, with each step supplied by configuration.

### What Is Abstracted and What Is Not
| Part | Shared core or tool | Reason |
| --- | --- | --- |
| Wake |  |  |
| Collection interface |  |  |
| Candidate selection interface |  |  |
| Telemetry writer |  |  |
| Issue writer |  |  |
| Acceptance check |  |  |
| Perf metric collection |  |  |

### Alternatives Considered and Rejected
Example: Building the perf engine standalone and extracting a scaffold later was rejected because the
extraction never happens once one tool depends on the concrete code.

### Second Tool Check
[] Would a second tool of this shape need only configuration, with no change to shared core code?
[] Does the shared core stay free of any perf specific name, metric, or path?
[] Does the tool have a command line entry point and no interface?
[] Does the design keep a future view reading the telemetry log rather than sitting in the path?

## 3. Protocol Surfaces and Tests

One test file per protocol surface. A surface with no test is not finished.

| Surface | Test file | What the test proves |
| --- | --- | --- |
| Wake |  |  |
| Collection |  |  |
| Selection |  |  |
| Telemetry append |  |  |
| Issue write |  |  |
| Acceptance check |  |  |

Test command: <command>
Result: <output>

## 4. Communication Channels Implemented

Exactly four. A fifth is a defect.

| Channel | Implemented where | Conforms |
| --- | --- | --- |
| Task out, one issue with metric, current number, target number, reproduction command, acceptance number |  |  |
| Result in, read from issue status and the after number |  |  |
| Defect in, one child issue to the tool owner |  |  |
| Telemetry, append only, one record per cycle and per task transition |  |  |

[] Is a task with no current number impossible to write?
[] Is there no broadcast, no status ping, and no chat thread anywhere in the code?

## 5. Handover Gate

The gate is the condition that ends this agent's ownership of the perf tool.

### Full Cycle Run
Command: <command>
Hand edits made: none
| Check | Evidence |
| --- | --- |
| Collected real numbers |  |
| Selected a candidate |  |
| Wrote one conforming issue |  |
| Appended telemetry |  |

### Empty Cycle Run
Command: <command>
| Check | Evidence |
| --- | --- |
| No candidate cleared the threshold |  |
| Telemetry record still written |  |
| No issue written |  |

Gate verdict: <pass | fail, with the reason>

## 6. Write Boundary Review

[] Every commit this run landed on a surface this agent owns
[] No commit landed in <perf_tool_workspace> after the gate passed
[] No commit landed in the product monorepo
[] The telemetry log was written only by the engine script
[] No roster change, no agent creation, and no work assigned to the performance engineer

## 7. Execution Checklist

[] Capability restated without naming a file
[] Placement decision recorded with a reason
[] Repository created or extended, with the initial commit recorded
[] Every protocol surface touched has its own test file and the tests pass
[] All four channels implemented, and no fifth exists
[] Full cycle and empty cycle both run with no hand edits and evidence recorded
[] Gate verdict recorded
[] Handover issue filed to the tool owner, or marked not yet due
[] Write boundary review completed
[] All placeholder text removed and the summary block reported

Handover issue: <id>
