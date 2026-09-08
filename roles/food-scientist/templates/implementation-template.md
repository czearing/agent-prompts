You are a working on the book cook brain a tool that is used to create the highest QUALITY recipe possible through food science and prediction through dp.

Workspaces:
Repo: C:\Code\book-cook-ai

## Rules
- You are NEVER allowed to use Regex to do hardcode searches our goal is global compatiblity and NEVER rigidity
- When working on the algorithm ensure that everything is entirely backed by the checmical compounds and not fixed rigid values (example: flour, bread) instead (sugar, glucose, etc)
- Keep code under 200 lines and abstract wherever possible
- Performance is imperative prioritize writting with performacne in mind code should never run longer then a few seconds including the test suite
- Write quality code and tests. Don't write unnessary tests that don't have purpose. Capture the essential core behavior.
- Input for the tool should remain clean and minimal prioritize keeping the cli as clean as possible and scientific.
- Delete ALL dead code you are responsible for keeping the repo clean
- Run tests in isolation we should never run the whole suit when making a small change
- NEVER fabricate data all data in the db must come from real sources

## Instructions

1. Examine the filed bug and the todo list you will directly edit this file
2. Investigate the failing test and implement the complete todo specified in the filed bug.
3. Create or fix the issue in the given food science logic and run the isolated test to confirm that it is fixed.
4. Run the full suit and record the complete time ensure it runs in under a minute. Do not delete tests only improve performance of the tool.
5. Once the fix is confirmed examine your changes and confirm that it is 1. Readable and has minimal lines eg each file should be under 200 lines or whatever the source code is in the scene 2. There should be no duplicate css rules and everything is properly deduped 3. The generated code should be as close as possible to the scenes source code.
Commit and push directly to upstream master.

## Methodology
- Recurring breakage means one logical rule lives in many places, so each fix reaches only one copy. When you find yourself editing a second site to finish one fix, treat that as the real defect and extract the rule into a single owner before continuing.
- Debug by narrowing the stage, not by reading the whole pipeline. Ask at each boundary whether the detail is still present. The first boundary where it is missing is the only place a fix belongs; a fix applied downstream restores one case and leaves the rest broken.
- Prefer deleting a special case over adding one. Each conditional that names a specific input is a future regression, because the next input will not match it.
- Every closed scene stays in the suite permanently. The suite's value is that it fails when a new fix breaks old behavior, which is the failure a single manual check cannot catch.
- Keep the suite fast by keeping each test file cheap. Test files run in parallel across cores, so a slow suite is caused by expensive setup repeated in every file, not by the number of tests.
- Optimize only the stage the measurement names. Re-measure after each change, because the slowest stage moves once the previous one is fixed.
- Report numbers, not adjectives. A fix without a recorded before and after cannot be shown to have helped.
