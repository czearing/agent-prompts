# Agent Design & Research Spec

## Behavior

### Purpose
What is the core job of this agent:
Example: This agent investigates rendering regressions and fixes unnecessary component re-renders.

### System Fit & Dependencies
Where does this agent fit in the overall workflow:
Example: Runs after benchmark regressions are detected, fixes the bottleneck, and passes code to PR reviewer.

What directory or workspace does it operate in:
Example: C:\Code\my-project\packages\components

### Human Thought Process & Approach
How does a human expert approach and solve this problem step by step:
Example: Inspect the profiler flamegraph, find the root re-rendering component, form a thesis on why props changed, test a minimal state adjustment, and confirm before and after render counts.

## Performance
How can we make the agents life easier? Are there scripts that we can write to ensure consistent output, quality assertion, etc that the agent can leverage. Are the wholes in the communication chain or reduncies in steps that subsequent agents might run into etc.

[] Testing can be handled through running yarn test
[] We can have the agent run a script with all ci commands to ensure it always has passing prs
[] etc


## Testing
How can we test the prompt can we simulate anything via a subagent to assert that it is handled correctly.

### Risks
[] Is Methodology strictly high-level guidance with no sequential steps?
[] Are Instructions strictly a numbered list (1, 2, 3)?
[] Are Rules strictly hard failure prohibitions?
[] Does the workflow provide a clear stop condition?
[] Does the prompt contain zero em dashes?
[] Is the prompt lean, clear, and free of fluff?

Conclusion: Confirm whether this prompt design is sufficiently constrained and ready for autonomous execution.

### Validation
Test 1:
1. Example: Verify the target agent properly develops a unique and creative thesis

Test 2:
1. Example: Run the target agent on a test task and verify it completes all steps and stops without looping.

### Prompt Review Checklist
[] Does the prompt follow the exact format: Role, Methodology, Instructions, Output, Rules
[] Are Instructions numbered (1, 2, 3)
[] Are Methodology and Rules bulleted with hyphens (-)
[] Are there zero em dashes
[] Does the prompt avoid buzzwords and use plain English
[] Is the companion problem-solving template customized for this agent
[] Are all example placeholders removed

## Design Candidate List
Validation Status - Description
Pass - Moved action steps out of Methodology into numbered Instructions.
Fail - Initial draft lacked an explicit stop condition.

## Final Generated Prompt

### Role
You are...
You work in: <workspace_directory>

### Methodology
- ...
- ...

### Instructions
1. ...
2. ...
3. ...

### Output
...

### Rules
- ...
- ...
