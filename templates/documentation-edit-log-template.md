# Documentation Edit Log

Targets under edit: <repo-relative paths, documents or source files>
Date: <yyyy-mm-dd>
Assignment: <one line, from the docs engine issue that triggered this edit>
Metric: <metric name, current number, budget number, per file>
Reproduction command: <the command from the issue>
Acceptance number: <the number that closes the task>

Sections 1 to 7 are required for every edit. Sections 8 and 9 are required for every edit that ends
in a pull request. Sections 4a and 4b are required for every edit from the commands and comments
revision forward. Logs written before the pull request path are valid without sections 8 and 9, and
logs written before the commands and comments revision are valid without sections 4a and 4b.

## 1. Context and Problem Understanding

### Reader and Job
Who reads these targets and what do they need to do after reading them:
Example: An engineer touching packages/views for the first time who needs to know where the view layer ends and the model begins before adding a column feature.

### Current State
Length before, structure, and the obvious symptoms:
Example: 412 lines, 9 headings, 3 sections restate function bodies from src/columns/, 2 sections describe a migration that shipped 8 months ago.
Example for a source target: src/columns/registry.ts, 6 exported members, 4 doc comments, 2 of them restate the signature and 1 names a removed option.

### Source of Truth
Which files, declarations and manifests the targets claim to describe:
Example: packages/views/src/columns/, packages/views/src/TableView.tsx, package.json scripts.

## 2. Thesis and Strategy

### Core Thesis
What is actually wrong with this document, in one sentence:
Example: The document tries to be a code reference, so it goes stale on every refactor and buries the three rules a new engineer actually needs.

### Proposed Strategy
The shape the document should take and the target length:
Example: Cut to a purpose paragraph, a routing table of paths, four non-negotiable rules, and the build and test commands. Target 90 lines.

Alternatives considered and why rejected:
Example: Splitting into three files was rejected because each part would be under 30 lines and the reader would have to open all three anyway.

## 3. Content Inventory

One row per section, doc comment or claim. Every row needs a verdict and a reason.

| Section or claim | Verdict (keep, compress, relocate, delete) | Reason |
|---|---|---|
| Example: "Column resize algorithm" walkthrough | delete | Restates src/columns/resize.ts line by line and already disagrees with it |
| Example: "The grid is designed to be flexible and performant" | delete | Padding, carries no path, no command, no number and no rule |
| Example: "Register the column before first paint" | compress | Real rule but unusable without the path, keep it with src/columns/registry.ts named |
| Example: "Do not mutate the row model directly" | keep | Durable rule, not visible from any single file |
| Example: "2024 grid migration notes" | delete | One past task, no reader acts on it now |
| Example: "Build and test commands" | compress | Correct but spread over 3 paragraphs, belongs in one code block |
| Example: doc comment on ColumnOptions, "Options object for a column" | delete | Restates the signature the reader can already see |
| Example: doc comment on registerColumn, "pass sortMode to control ordering" | compress | Real usage rule but sortMode is no longer on the declaration, keep the rule against the current members |

## 4. Verification

Every kept or compressed claim must be checked against current source. Record the check.

| Claim | Checked against | Result (accurate, corrected, removed) |
|---|---|---|
| Example: "TableView owns selection state" | src/TableView.tsx | accurate |
| Example: "yarn test:grid runs the suite" | package.json | corrected, script is yarn test --to views |

Unverifiable claims are removed, not softened.

## 4a. Commands Checked

Every command stated in a target, in prose or in a doc comment, is checked against the manifest or
the tool that owns it. A command that does not resolve is corrected or cut. It is never left
standing and never softened.

Commands checked: <count>
Commands corrected: <count>
Commands cut: <count>

| Command as stated | Checked against | Result (resolves, corrected to, cut) |
|---|---|---|
| Example: yarn test:grid | package.json scripts | corrected to yarn test --to views |
| Example: yarn build | package.json scripts | resolves |
| Example: yarn lint:columns | package.json scripts | cut, no script or tool owns this name |

## 4b. Doc Comments Checked

One row per exported member whose doc comment is a target. Judge the comment by whether the reader
can use the member without opening anything else, whether it names members the declaration no longer
has, and whether it restates a signature the reader can already see.

| Exported member | Declaration checked | Finding | Result (rewritten, cut, left as is) |
|---|---|---|---|
| Example: registerColumn in src/columns/registry.ts | same file, plus 4 call sites under src/ | names a sortMode option the declaration no longer has | rewritten |
| Example: ColumnOptions in src/columns/types.ts | same file | restates the signature in words | cut |

No signature, body, or behavior was changed. Confirmed by:
Example: the diff for src/columns/registry.ts contains comment lines only.

## 5. Risk Checklist

[] Does the rewrite drop a rule that only existed in this document and nowhere in code or lint?
[] Does anything that was cut still need a home, and does it have one?
[] Are all remaining links and file paths valid?
[] Does every command that survives resolve against the manifest or the tool that owns it?
[] Does every surviving doc comment match the declaration it sits on?
[] Is the diff on every source target limited to comment lines?
[] Does the document avoid restating code that a reader can open directly?
[] Is every surviving claim traceable to a file that exists today?
[] Would a new engineer be able to act after one read?
[] Does every surviving sentence carry a path, a command, a number, or a rule?
[] Do all files in this change serve one reader and one thesis?

## 6. Evidence and Results

Before: <line count>, <heading count>
After: <line count>, <heading count>
Removed: <what classes of content were cut>
Added or corrected: <what was wrong and is now right>
Commands: <checked count, corrected count, cut count, from section 4a>
Comments: <exported members rewritten or cut, from section 4b, or none>

Metric result:
Example: markdown line count for docs/guides/auth.md went 412 to 88 against a budget
of 120, using the reproduction command from the issue.

Validation run:
Example: repo check passed on the branch with 0 issues.

## 7. Execution Checklist

[] Reader and job recorded
[] Core thesis recorded
[] Content inventory complete with a verdict on every section
[] Every kept claim verified against current source
[] Every stated command checked and recorded in section 4a
[] Every doc comment target checked against its declaration and recorded in section 4b
[] Risk checklist answered
[] Reproduction command run and the after number recorded against the budget number
[] repo check run on the branch and clean
[] Before and after measurements recorded
[] All placeholder text removed from the rewritten document and from this log

## 8. Scope and Exclusion Confirmation

Required for every edit that ends in a pull request.

Files named by the task:
Example: docs/guides/auth.md, docs/guides/auth-server.md
Example for a source only task: packages/ux/src/columns/registry.ts, packages/ux/src/columns/types.ts

[] No file named AGENTS.md or CLAUDE.md was edited or counted as a target
[] Nothing under .github/skills, .github/prompts, .github/agents or .github/instructions was touched
[] No file named SKILL.md was touched
[] No path containing agent, copilot or prompt was touched
[] git status shows no file outside the list above
[] All files in this change serve one reader and one thesis

No file outside the task was touched. Confirmed by:
Example: git status --short on the branch listed exactly the two files named by the task.

Files discovered mid task that also need work, left out of this branch and noted on the issue:
Example: docs/guides/routing.md, same padding problem, noted on the issue as a
follow up. If none, write none.

## 9. Branch and Pull Request Record

Required for every edit that ends in a pull request. The task is not complete until every line here
is filled.

Clone: <workspace_directory>
Branch: <branch-name>
Cut fresh from: master
Commit pushed: <yes, with the short sha>
Pull request identifier: <id>
Pull request contents: documentation and source comments only

Problem stated in the pull request:
Example: The auth guide states rules without the paths or commands that make them usable, so a
reader has to open three other files before acting.

Solution stated in the pull request:
Example: Each rule now carries the path or command it applies to, code restatement is replaced with
pointers, and padding is removed.

Validation stated in the pull request:
Example: repo check passed on the branch, and every kept claim is traced to a file in section 4.

[] Pull request identifier recorded as a comment on the issue
[] Issue moved to its final disposition
[] No status ping sent and no reviewer polled
