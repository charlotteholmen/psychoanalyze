---
description: "Guidance for writing maintainable Gherkin feature files (avoid Cucumber anti-patterns)."
applyTo: "**/*.feature"
---

# Gherkin feature file guidelines

Use these rules when writing or editing `.feature` files.

## Write declarative behavior
- Describe what the system does, not how the UI or implementation works.
- Prefer domain language and outcomes (behavior) over click/type steps.
- If the wording would change when the UI changes, rewrite it.

## Keep steps reusable
- Avoid feature-coupled wording that cannot be reused across features.
- Phrase steps around domain concepts, not specific screens or flows.
- Keep step sentences generic enough to share with other scenarios.

## Avoid conjunction steps
- Do not combine multiple actions or conditions in one step.
- Split steps with `And` / `But` instead of "and" inside a step.
- Keep steps atomic so they remain composable and easy to reuse.

## Structure scenarios for clarity
- Each scenario should show a single behavior.
- Use Given/When/Then roles consistently (setup, action, outcome).
- Keep scenarios short and focused; move detail into step definitions.

## Naming and formatting
- Use clear, user-centric scenario titles.
- Prefer concrete example data only when it clarifies the behavior.
- Avoid implementation details like element IDs, routes, or button labels.
