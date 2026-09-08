# Engineering Task Log

Task: <task title or id>
Branch: <user/alias/task-slug>
Packages in scope: <package names>
Date started: <date>

## 1. Context and Problem Understanding

### Problem Statement
What must be true when this task is done, stated as behavior a user or caller can observe:
Example: Pasting a table into a page keeps cell borders instead of flattening to plain text.

### Reproduction or Current Behavior
Exact steps, command, or test that shows the current behavior. A bug fix needs a reproduction before
a fix is written:
Example: yarn start --to app, open a page, paste a table copied from Excel, borders are lost.

### Repository Discovery
Where the behavior actually lives. List the real files, not guesses.

| Path | Role in this task |
| --- | --- |
| packages/<package>/src/<file>.ts | <what it does and why it matters here> |

Package instruction files read before editing (repo root AGENTS.md plus every package AGENTS.md in
scope):
Example: AGENTS.md, packages/scriptor/AGENTS.md

Existing code that already does part of this job and should be reused instead of rewritten:
Example: normalizeClipboardHtml in packages/scriptor/src/clipboard/normalize.ts

Constraints found in the repo that bound the change:
Example: app-main bundles page-container, so this change must not span both.

## 2. Thesis and Strategy

### Root Cause
One sentence naming the cause, not the symptom:
Example: The paste sanitizer drops style attributes before the table handler runs, so the handler
never sees the border values.
For an intermittent or flaky failure, name the exact nondeterministic mechanism (a race, an unhandled
async wait, shared state between tests), not the point where it happened to fail this run. "The test
is flaky" or "it sometimes times out" is not a root cause.

### Narrowest Fix
The smallest change that removes the cause, and the layer it belongs in:
Example: Move the table handler ahead of the attribute filter and allow the border properties through
the existing allow list. One file, no new module.

### Alternatives Considered and Rejected
Example: Adding a second sanitizer pass in page-container was rejected because it duplicates
logic that already exists upstream and would drift from it.

### Scope Check
[] Does this change stay inside one package boundary, or is the split justified and safe?
[] Does it avoid spanning app-main and page-container in one pull request?
[] Does it avoid duplicating logic that already exists elsewhere in the repo?
[] Does it avoid a public API break, or is the break required and versioned correctly?
[] Does every touched file stay under roughly 200 lines, or is a split needed?
[] For an intermittent or flaky failure, does the fix remove the nondeterministic mechanism instead of
   adding a wait, timeout, retry, or sleep around it?
[] Does the same mechanism appear at other call sites or test files, and if so was a shared fix applied
   there instead of a one-off patch?

## 3. Risk and Impact Analysis

| Risk | Who it affects | How it is caught before merge |
| --- | --- | --- |
| <risk> | <consumers, hosts, or packages> | <the exact test, command, or manual check> |

[] Are there other callers of every function or component changed, and were they checked?
[] Does the change affect accessibility, localization, or keyboard behavior?
[] Does the change alter collaborative or persisted data in a way older clients cannot read?
[] Is every user visible string localized?
[] Are error and empty states still handled?

## 4. Performance Expectations Check

Every general code change carries this check, whether or not a regression was ever measured.

[] Does the change avoid adding a new pass over a large collection in a hot path?
[] Does the change avoid adding render cost to a component that already runs often?
[] Does the change avoid bundle growth beyond what the fix requires?
[] Does the change avoid re-acquiring or re-querying the same handle, selector, or resource on every
   iteration of a poll, retry, or wait loop when the result could be captured once and reused?
[] Does every retry, poll, or wait loop use the fastest correct polling primitive for its context
   (Playwright's expect(...).toPass, Jest's waitFor with a short interval, or an existing event or
   promise in application code) instead of a hand written loop around one long fixed wait, in this
   change and in any other framework or production code it touches, not only Playwright?
   Slow, avoid (any context): for (attempt) { await trigger(); try { await result.waitFor({ timeout:
   20000 }); break; } catch { await reset(); } } - up to a minute of dead waiting on a real failure.
   Fast, prefer (Playwright): await expect(async () => { await trigger(); await expect(result).toBeVisible({
   timeout: 1500 }); }).toPass({ timeout: 8000 }); - polls in under two seconds per attempt.
   Fast, prefer (Jest): await waitFor(() => expect(result).toBe(expected), { timeout: 8000, interval: 250 });
   - the same short-interval polling, not a Playwright specific fix.
[] If a measured regression shows up during this check, is it handed to SoftwareEngineerPerformance
   instead of fixed here?

Result: <pass, or the one regression found and who it was handed to>

## 5. Validation and Evidence

### Test Plan
Automated tests added or updated:
Example: packages/scriptor/src/clipboard/normalize.test.ts gains a case asserting border styles
survive a table paste. It fails before the fix and passes after.

Manual verification steps for anything a user can see:
1. Example: yarn start --to app
2. Example: Open a page and paste a bordered table
3. Example: Capture a screenshot of the result and record it below

### Evidence

| Check | Command or steps | Before | After |
| --- | --- | --- | --- |
| Failing test proves the bug | yarn test --to <package> | <fails> | <passes> |
| Targeted unit tests | yarn test --to <package> | <result> | <result> |
| Visual check | <steps> | <screenshot path> | <screenshot path> |
| Full gate | repo check | <result> | <result> |

Screenshots or artifacts saved to:
Example: C:\Code\agent-prompts\roles/software-engineer/<task-slug>-after.png

## 6. Review of the Completed Diff

[] Every changed line serves the stated root cause, with no unrelated cleanup
[] No `as` casts, `any` types, or `!` non null assertions were introduced
[] No hand written useMemo, useCallback, or React.memo in a React Compiler package
[] Descriptive names used everywhere, including callback parameters
[] Comments limited to one or two sentences and only where the code is not self explanatory
[] Design tokens used instead of raw hex values
[] Logging goes through the package logger, not console
[] No credentials, secrets, or internal identifiers added to source or pull request text
[] No em dashes anywhere in code, comments, commits, or pull request text

## 7. Execution Checklist

[] Reproduction or current behavior recorded before any code was written
[] Repository discovery table filled with real paths
[] Root cause and rejected alternative recorded
[] Branch created with branch creation tool
[] A test that fails before the fix and proves the stated behavior after it, not just coverage, was
   added or updated
[] Performance expectations check completed with a recorded result
[] Manual and visual verification done and evidence recorded
[] Change file generated with repo tool, never written by hand
[] repo check passed on the branch
[] Pushed with git push or repo tool
[] Pull request opened with PR creation tool and the link recorded here
[] Pull request merged, or this issue left in_review naming the open pull request as the pending
   reviewer path
[] All placeholder text removed from this log

Pull request: <url>
Merge status: <merged, or in_review pending reviewer path>
