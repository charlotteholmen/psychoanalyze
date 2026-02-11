---
description: "Create a new jj revision with a description derived from a .d2 diagram"
---

# Create JJ Revision From D2 Diagram

Create a new jj revision whose description summarizes the primary behavior conveyed by a given `.d2` diagram.

## Inputs

- `d2_path`: Workspace-relative path to the `.d2` file.
- `focus`: Optional. A node label or identifier to target if the diagram contains multiple behaviors.

## Available Tools

- `read_file` to inspect the `.d2` file.
- `create_file` to add a new Gherkin feature file.
- `activate_revision_management_tools` then `mcp_jj_new` to create a new revision.

## Workflow

1. Read the diagram at `d2_path`.
2. Determine the primary behavior conveyed by the diagram:
   - If `focus` is provided, use that node/label as the behavior anchor.
   - Otherwise, infer the main behavior from the top-level node or the most central flow.
3. Create a new revision with `mcp_jj_new` using the description "feat: <feature>".
4. Create a Gherkin feature file that describes the diagram's behavior.
    - Place it in `tests/features/` with a slugged name based on the `d2_path` stem.
    - Use `Feature: <behavior>` for a top-level description.

## Notes

- Only create the single Gherkin feature file; do not edit existing files.
- If the diagram does not clearly convey a single behavior, ask the user to specify `focus`.
- Do not implement any Gherkin scenarios just yet.
