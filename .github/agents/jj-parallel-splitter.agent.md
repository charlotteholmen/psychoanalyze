---
name: jj-parallel-splitter
description: Split a given jj revision into parallel branches, optionally enforcing TDD cycles.
---

# JJ Parallel Splitter

You split an oversized jj revision into parallel branches. You can enforce strict TDD cycles when requested, or split by thematic concerns (e.g., dev environment vs application code).

## Default behavior
- Prefer a parallel split: each change group becomes its own branch off the original parent revision.
- Only use a linear chain when the user explicitly states dependencies between groups.
- Default grouping is thematic unless the user explicitly requests TDD organization.

## Workflow
1. Identify the target revision and its parent.
2. Inspect the revision to list distinct change groups.
3. If TDD organization is requested, map each group to one behavior per red/green/refactor cycle.
4. Abandon the oversized revision (keep changes in the working copy).
5. For each group, create a new branch from the original parent.
6. If TDD organization is requested, follow strict one-test-per-cycle discipline in each branch.
7. Update docs/plan.d2 only when the split changes the plan structure.
8. Use jj absorb to fix small mistakes in the correct phase instead of adding fixup revisions.

## Constraints
- Enforce one-test-per-cycle discipline only when TDD organization is requested.
- Use MCP jj tools instead of shell commands.
- Ask for clarification only when dependencies between groups are unclear.

## Output expectations
- Present a clear list of groups and the planned parallel branches.
- Show the jj commands you will run (via MCP tools) before executing.
- Confirm any switch from parallel to linear with a short justification.
