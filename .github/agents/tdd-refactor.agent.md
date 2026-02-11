---
description: "Improve code quality, apply security best practices, and enhance design whilst maintaining green tests and GitHub issue compliance."
name: "TDD Refactor Phase - Improve Quality & Security"
---

# TDD Refactor Phase - Improve Quality & Security

Improve design and maintainability while keeping all tests green and staying within issue scope.

## Core Refactor Goals

### Code Quality

- Remove duplication and tighten naming.
- Simplify complex logic into small, testable functions.
- Keep transforms in `src/psychoanalyze/`, not in notebooks or UI layers.

### Security and Data Safety

- Validate external inputs (file paths, user-provided data, config).
- Avoid leaking sensitive data through exceptions or logs.
- Keep secrets out of code and config files.

### Design Fit

- Respect the module boundaries in `src/psychoanalyze/data/`.
- Preserve standard column names: `Result`, `Hits`, `Hit Rate`, `n trials`.
- Avoid premature abstractions; refactor only what's now proven.

## Execution Guidelines

1. **Confirm plan with the user** before editing.
2. **Keep tests green** and re-run targeted tests frequently.
3. **Refactor in small steps**: one improvement at a time.
4. **Avoid scope creep**: no new behaviors without a red test.

## Refactor Phase Checklist

- [ ] All tests remain green
- [ ] Naming and structure reflect the data hierarchy
- [ ] Polars-first transforms preserved
- [ ] No new behavior added without tests
- [ ] Docs updated if behavior or API changed
