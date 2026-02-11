---
description: "Write a pytest test for a scenario in a Gherkin feature file"
tools: [vscode, execute, read, agent, edit, search, web, 'jj/*', todo]
---

Write an executable pytest test for a specific scenario defined by the parent jj revision.

Requirements:
- Use plain pytest; not pytest-bdd or other plugins.
- Read the scenario and implement matching test code in `tests/test-features.py`. Use pytest classes to group scenarios by feature.
- Keep step definitions reusable and domain-focused (avoid UI or implementation details).
- Use existing fixtures and data helpers where possible; add new fixtures only if needed.
- Ensure the test fails with a clear assertion if behavior is missing (avoid NameError/ImportError; implement function stubs if needed).
- Map given/when/then to arrange/act/assert structure in the test code.
- Be as concise as possible

Output:
- List files created/edited.
- Provide the test code and step definitions.
- Note any assumptions or missing domain details.
