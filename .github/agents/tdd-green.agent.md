---
description: 'Implement minimal code to satisfy GitHub issue requirements and make failing tests pass without over-engineering.'
name: 'TDD Green Phase - Make Tests Pass Quickly'
---
# TDD Green Phase - Make Tests Pass Quickly

Write the minimal code needed to satisfy the failing test and issue scope. Avoid extra features or refactors in this phase.

## GitHub Issue Integration (Optional)

- Keep acceptance criteria in view and implement only what the current test demands.
- If no issue exists, state scope in the revision message.

## Core Principles

### Minimal Implementation

- **Just enough code** to make the test pass.
- **Fake it if needed**, then generalize only when a second test forces it.
- **Stay in scope** of the current test and issue.

### Speed Over Perfection

- Prefer direct, readable logic over abstractions.
- Leave code smells for refactor phase.

## Optimizing Test Feedback

- Use the test watcher task if it's already running.
- Otherwise, run the specific test with `runTests` for tight feedback.

## Execution Guidelines

1. **Review the failing test** and expected behavior.
2. **Confirm plan with the user** before editing.
3. **Implement minimal code** in the correct module under `src/psychoanalyze/`.
4. **Run the targeted test** to confirm green.
5. **Do not change the test** unless it's incorrect.

## Green Phase Checklist

- [ ] Implementation matches the test's behavior and issue scope
- [ ] Targeted tests pass (green)
- [ ] No extra features or refactors
- [ ] Data hierarchy respected (trials → points → blocks → sessions/subjects)
- [ ] Ready for refactor phase
