# PsychoAnalyze - Copilot Instructions

## Project Overview

PsychoAnalyze is a Python library for interactive data simulation and analysis in psychophysics research. It models psychometric functions using logistic regression to estimate detection thresholds from experimental trial data.

## Architecture

PsychoAnalyze is organized around **three loosely-coupled pillars** (see `docs/architecture.md`):
1. **Data processing** (deterministic transforms + validation)
2. **Interactive dashboard** (Marimo UI that orchestrates and visualizes)
3. **Ergonomic Python package** (stable API/CLI for scripting + automation)

### Data Hierarchy (core concept)
The codebase follows a strict hierarchical data model where each level aggregates the one below:
1. **Trials** (raw table) - Individual stimulus presentations (e.g., `Intensity`, `Result`, `Block`)
2. **Points** (`src/psychoanalyze/data/points.py`) - Aggregated trial counts at each intensity (Hit Rate = Hits / n trials)
3. **Blocks** (`src/psychoanalyze/data/blocks.py`) - Fitted psychometric curves (threshold + slope from logistic regression)
4. **Sessions/Subjects** (`src/psychoanalyze/data/sessions.py`, `src/psychoanalyze/data/subjects.py`) - Longitudinal groupings

Each module in `src/psychoanalyze/data/` corresponds to one level. Functions typically transform data upward (e.g., `psychoanalyze.data.points.from_trials()` aggregates trials into points).

### Key Components
- **`app.py`** - Marimo app serving as the interactive dashboard UI (orchestration + visualization; keep transforms in `src/psychoanalyze/`)
- **`src/psychoanalyze/`** - Core library
  - `data/` - Data manipulation per hierarchy level
  - `analysis/` - Statistical analysis (Bayesian, ECDF, Weber, strength-duration)
  - `sigmoids.py` - Psychometric link functions (Weibull, Gumbel, Quick)
  - `plot.py` - Plotly template and axis settings
- **`models/`** - dbt SQL models and Stan models for Bayesian fitting

### The Psychometric Function (ψ)
Core formula used throughout: `ψ(x) = γ + (1 - γ - λ) * F(x; x₀, k)`
- `x₀` = threshold (50% point), `k` = slope (steepness)
- `γ` = guess rate, `λ` = lapse rate
- `F` = link function (typically logistic sigmoid)

## Development Workflow

**Shell:** Nushell is the default shell for this project. All commands should be written in Nushell syntax unless explicitly running bash/sh scripts.

**MCP-first:** Prefer MCP tools over shell commands when available (see `.github/instructions/prefer-mcp-tools.instructions.md`). Check for `mcp_jj_*`, `mcp_marimo_*`, `runTests`, and dependency management tools before falling back to `run_in_terminal`. Always call `configure_python_environment` before any Python-related tool.

```bash
# Package management (uv only, not pip)
uv sync                      # Install all dependencies from lock file
uv add <package>             # Add/install a new package to dependencies
uv add --dev <package>       # Add/install a new dev dependency
uv run ruff format           # Format
uv run ruff check --fix      # Lint and autofix
uv run ty check              # Type check (uses ty, not mypy)
uv run pytest                # Run tests (writes Allure results to allure-results/)
uv run ptw . --now           # Test watcher (tight TDD loop)

# Run the dashboard
uv run marimo edit app.py
# or via CLI:
uv run psychoanalyze marimo
```

## Specs, Contracts, and Diagrams

This repo treats implementation as downstream of declarative artifacts (see `docs/plan-engineeringApproach.prompt.md`):

- **System map**: `docs/plan.d2` is the top-level dependency/order graph.
- **Data contract**: `data-contract.odcs.yaml` is the schema-level boundary (validated via `datacontract-cli`, wired through `prek.toml`).
- **Acceptance specs (BDD)**:
  - Source specs live in `features/*.feature` and `docs/*.feature`.
  - Executable pytest-bdd step definitions live under `tests/bdd-features/`.
- **Diagrams**: D2 sources in `docs/*.d2`, rendered into `docs/figures/`.
  - Prefer VS Code tasks for watch/render workflows (e.g. “D2: Watch all diagrams”).

## Testing and Reporting

- **Allure**: pytest is configured with `--alluredir=allure-results`.
- **Local dashboard**: run `allure serve` (or the workspace task) to browse results.
- **Markers**: prefer pytest markers (`unit`, `integration`, `slow`, `data`, `analysis`, etc.) for test organization.

## Code Conventions

### Type Annotations
- Prefer broad input types, narrow output types
- Use builtin generics: `list[str]`, `dict[str, int]`, not `List`, `Dict`
- Use `|` for unions, not `Optional` or `Union`

### Tabular Data Patterns
- Prefer **Polars** (`polars.DataFrame`) for core transforms; convert to Pandas only at presentation boundaries (e.g., Plotly Express).
- Validation/type-shapes live primarily in `src/psychoanalyze/types.py` (Patito + Pydantic models).
- Index columns: `Intensity`, `Block`, multi-indexes for sessions
- Standard column names: `Result` (0/1), `Hits`, `Hit Rate`, `n trials`

### Plotly Usage
- Use global template from `plot.template` for consistent styling
- Subject colormap: `{"U": "#e41a1c", "Y": "#377eb8", "Z": "#4daf4a"}`
- Return `go.Figure` objects, use `px` for quick plots

### Testing
Tests mirror source structure in `tests/`. Use pytest fixtures for common data:
```python
import polars as pl

@pytest.fixture()
def trials_df() -> pl.DataFrame:
  return pl.DataFrame({"Intensity": [...], "Result": [...], "Block": [...]})
```

## Key Formulas Reference

```python
# Threshold from logistic fit params
threshold = -intercept / slope  # x₀ = -b₀/b₁

# Generate stimulus range from model params
min_x = (logit(0.01) - intercept) / slope
max_x = (logit(0.99) - intercept) / slope
```

## Custom Agents

This repo includes custom agents with focused workflows and tool constraints. Use these when you need strict enforcement or specialized help.

### TDD Workflow Agents

#### tdd-red

**File:** `.github/agents/tdd-red.agent.md`

**Purpose:** Enforces strict one-test-per-cycle TDD discipline during red phases. Prevents writing multiple tests, validates test atomicity, and guides revision splitting when violations occur.

**When to use:**
- Writing failing tests (red phase)
- Splitting oversized revisions
- Validating TDD atomicity
- Updating d2 diagrams after splits

**Example invocation:**
```
Use the tdd-red agent to write a test for hit rate calculation
```

**Constraints:**
- Writes exactly ONE test per invocation
- Blocks notebook edits
- Enforces atomic behavior testing
- Auto-detects and splits violations

#### d2-tdd

**File:** *To be created*

**Purpose:** TDD translator - converts verbose natural language requests into atomic TDD cycles.

**Status:** Stub (listed in global agents but not yet implemented)

### Version Control Agents

#### jj-parallel-splitter

**File:** `.github/agents/jj-parallel-splitter.agent.md`

**Purpose:** Splits oversized jj revisions into parallel branches, optionally enforcing TDD cycles.

**When to use:**
- Splitting a revision with multiple concerns (e.g., dev environment vs application code)
- Enforcing one-test-per-cycle discipline when requested
- Creating parallel branches for independent change groups

**Example invocation:**
```
Use the jj-parallel-splitter agent to split revision @ into parallel branches
```

#### jj-helper

**File:** Global agent (not workspace-specific)

**Purpose:** Jujutsu (jj) version control expert for advanced revision operations.

**When to use:**
- Rebasing revisions
- Resolving conflicts
- Analyzing revision evolution (`jj evolog`)
- Complex revision surgery

**Example invocation:**
```
Use the jj-helper agent to rebase these 3 revisions onto main
```

### Marimo Workflow Agents

#### marimo-helper

**File:** Global agent (not workspace-specific)

**Purpose:** Marimo notebook translation and management.

**When to use:**
- Converting Jupyter to Marimo
- Managing Marimo dashboard
- Troubleshooting reactive execution

### Development Workflow Agents

#### SE: Architect

**File:** Global agent

**Purpose:** System architecture review specialist with Well-Architected frameworks, design validation, and scalability analysis.

**When to use:**
- Reviewing system design
- Validating architectural decisions
- Scalability analysis

#### SE: Tech Writer

**File:** Global agent

**Purpose:** Technical writing specialist for documentation, blogs, tutorials, and educational content.

**When to use:**
- Writing API documentation
- Creating tutorials
- Documenting architecture decisions

#### SE: DevOps/CI

**File:** Global agent

**Purpose:** DevOps specialist for CI/CD pipelines, deployment debugging, and GitOps workflows.

**When to use:**
- Setting up GitHub Actions
- Debugging CI/CD pipelines
- Deployment automation

### Agent Development

#### Creating New Agents

1. **Create agent file:** `.github/agents/<name>.agent.md`
2. **Define YAML frontmatter:**
   ```yaml
   ---
   name: agent-name
   description: Brief description of purpose
   toolRestrictions:
     - name: tool_name
       restriction: allowed|blocked
   ---
   ```
3. **Document in this file** under appropriate section
4. **Test invocation:** `Use the <name> agent to...`

#### Agent Design Principles

- **Single Responsibility:** Each agent has ONE clear purpose
- **Tool Constraints:** Restrict tools to prevent scope creep
- **Clear Invocation:** Description makes it obvious when to use
- **Integration:** Agents should hand off to each other when appropriate

#### Tool Restrictions

Common patterns:

```yaml
# Read-only agent (research, analysis)
toolRestrictions:
  - name: replace_string_in_file
    restriction: blocked
  - name: create_file
    restriction: blocked

# Workflow enforcer (strict rules)
toolRestrictions:
  - name: edit_notebook_file
    restriction: blocked
  - name: run_in_terminal
    restriction: allowed

# Full-spectrum (general purpose)
toolRestrictions: []
```

### Usage Guidelines

#### When to Use an Agent

Use agents when:
- You need **strict enforcement** of a workflow rule
- You want **constrained tooling** for safety
- You need **specialized expertise** in one domain
- You want **consistent behavior** across sessions

#### When NOT to Use an Agent

Don't use agents when:
- General Copilot is sufficient
- You need flexibility across domains
- Constraint overhead > benefit
- Agent isn't well-suited to task

#### Agent Chaining

Agents can hand off to each other:

```
[tdd-red] → Write failing test
[default]  → Implement code to pass test
[tdd-red] → Write next failing test
[jj-helper] → Rebase revisions
```

## Metrics and Improvement

Track agent effectiveness:

```nushell
# How often do you invoke agents?
def agent-usage [] {
    git log --since="1 month ago" --grep="agent" --oneline | lines | length
}

# Which agents are most used?
def agent-frequency [] {
    git log --since="1 month ago" --grep="agent" --oneline
    | parse "{commit} {rest}"
    | get rest
    | str downcase
    | where ($it | str contains "agent")
    | parse --regex '(?P<agent>\w+-\w+) agent'
    | get agent
    | uniq -c
}

# What's the violation rate with tdd-red?
def tdd-violations [] {
    jj log --limit 100
    | grep "red phase"
    | each {|line|
        let tests = (jj diff -r ... | grep "^+def test_" | lines | length)
        if $tests > 1 { 1 } else { 0 }
    }
    | math sum
}
```

Review metrics monthly and refine agents based on actual usage patterns.

## References

- **Agent Customization Skill:** `copilot-skill:/agent-customization/SKILL.md`
- **JJ TDD Revisions Skill:** `.github/skills/jj-tdd-revisions/SKILL.md`
- **TDD Enforcement Strategy:** `.github/docs/tdd-enforcement-strategy.md`
- **Revision Splitting Instructions:** `.github/instructions/jj-revision-splitting.instructions.md`

## Prefer MCP Tools Over Shell Commands

### Core Principle

**Always check whether an MCP tool exists for an operation before running it as a shell command.** MCP tools provide structured input/output, better error handling, and integrate directly with the editor - shell commands should be the fallback, not the default.

### Tool Availability Mapping

#### JJ (Jujutsu) - use `mcp_jj_*` tools

| Shell command | MCP tool | Notes |
|---|---|---|
| `jj describe -m "..."` | `mcp_jj_describe` | Set revision message |
| `jj abandon <rev>` | `mcp_jj_abandon` | Discard revisions |
| `jj edit <rev>` | `mcp_jj_edit` | Switch working copy |
| `jj new -m "..."` | activate `revision_management_tools` -> `mcp_jj_new` | Create new revision |
| `jj commit -m "..."` | activate `revision_management_tools` -> `mcp_jj_commit` | Commit current changes |
| `jj rebase ...` | activate `revision_management_tools` -> `mcp_jj_rebase` | Move revisions |
| `jj show` | activate `revision_management_tools` -> `mcp_jj_show` | Inspect revision |
| `jj diff` | activate `diff_and_annotation_tools` -> `mcp_jj_diff` | Compare revisions |
| `jj log` | activate `revision_management_tools` -> `mcp_jj_log` | View history |
| `jj git push` | activate `bookmark_management_tools` -> `mcp_jj_git-push` | Push to remote |
| `jj git import` | `mcp_jj_git-import` | Sync Git -> JJ |
| `jj git export` | `mcp_jj_git-export` | Sync JJ -> Git |
| `jj config set ...` | `mcp_jj_config-set` | Set config option |
| `jj file track ...` | `mcp_jj_file-track` | Track files |
| `jj file chmod ...` | `mcp_jj_file-chmod` | Set executable bit |

Activation pattern: Some jj tools require activation first. Call the appropriate `activate_*_tools`, then use the unlocked tool.

#### UV / Python - use built-in Python tools

| Shell command | Tool | Notes |
|---|---|---|
| `uv run pytest` | `runTests` | Structured test output with pass/fail details |
| `uv add <pkg>` | `activate_dependency_management_tools` -> `add_package` | Adds to pyproject.toml |
| `uv add --dev <pkg>` | `activate_dependency_management_tools` -> `add_dev_package` | Dev dependency |
| `uv sync` | `install_python_packages` | Install from lock file |
| `uv run <tool>` | `run_tool` | Run Python CLI tool via uvx |
| `uv tool install <tool>` | `install_tool` | Install global CLI tool |
| `uv venv` | `activate_python_environment_management_tools` -> `create_venv` | Create virtual env |
| `python --version` | `activate_python_environment_tools` -> `get_python_environment_details` | Env info |
| `uv lock` | `generate_lock` | Generate uv.lock |

Always call `configure_python_environment` before any Python-related tool.

#### Marimo - use `mcp_marimo_*` tools

| Shell command | MCP tool | Notes |
|---|---|---|
| `marimo check app.py` | `mcp_marimo_lint_notebook` | Lint notebook |
| Manual error inspection | `mcp_marimo_get_notebook_errors` | Runtime errors by cell |
| Cell output reading | activate `cell_output_analysis_tools` -> `mcp_marimo_get_cell_outputs` | Cell outputs |
| Cell navigation | `mcp_marimo_get_lightweight_cell_map` | Cell structure overview |

#### GitHub - use `mcp_github_*` tools

| Shell command | MCP tool | Notes |
|---|---|---|
| `gh pr create` | activate `repository_management_tools` -> `create_pull_request` | Create PR |
| `gh issue create` | activate `repository_information_tools` -> create issue tools | Create issue |
| `git push` | `mcp_jj_git-push` (via jj) or `run_in_terminal` | Push changes |

### Decision Checklist

Before running a shell command, ask:

1. Is there a directly available MCP tool? -> Use it.
2. Is there an activatable tool group? -> Call `activate_*_tools`, then use the unlocked tool.
3. Does a built-in VS Code tool cover this? (e.g., `runTests` for pytest) -> Use it.
4. None of the above? -> Fall back to `run_in_terminal`.

### When Shell Commands Are Still Appropriate

- Exploratory commands with complex pipes or filters (e.g., `jj log --limit 5 -T ...` with custom templates)
- Commands with no MCP equivalent (e.g., `d2 render`, `ruff check --fix`)
- Chained multi-step operations where MCP tools would require many sequential calls with no benefit
- Reading command output when `run_in_terminal` gives better visibility than an MCP tool's structured response

### Anti-Patterns

Bad: Shell when MCP exists

```
run_in_terminal: jj describe -m "feature: red phase"
```

Good: Use MCP tool directly

```
mcp_jj_describe(message="feature: red phase")
```

Bad: Shell for tests

```
run_in_terminal: uv run pytest tests/data/test_types.py -v
```

Good: Use runTests

```
runTests(files=["tests/data/test_types.py"])
```

Bad: Shell for package install

```
run_in_terminal: uv add pandas
```

Good: Use dependency tool

```
activate_dependency_management_tools() -> add_package(packageName="pandas")
```

## Self-Explanatory Code Commenting

### Core Principle

Write code that speaks for itself. Comment only when necessary to explain WHY, not WHAT. Most code needs no comments.

### Commenting Guidelines

Avoid these comment types:

- Obvious comments
- Redundant comments
- Outdated comments

Write these comment types:

- Complex business logic (explain WHY the specific calculation)
- Non-obvious algorithms (explain the algorithm choice)
- Regex patterns (explain what the regex matches)
- API constraints or gotchas (external limits or behavior)

### Decision Framework

Before writing a comment, ask:

1. Is the code self-explanatory? -> No comment needed
2. Would a better name eliminate the need? -> Refactor instead
3. Does this explain WHY, not WHAT? -> Good comment
4. Will this help future maintainers? -> Good comment

### Special Cases for Comments

Public APIs

```javascript
/**
 * Calculate compound interest using the standard formula.
 *
 * @param {number} principal - Initial amount invested
 * @param {number} rate - Annual interest rate (as decimal, e.g., 0.05 for 5%)
 * @param {number} time - Time period in years
 * @param {number} compoundFrequency - How many times per year interest compounds (default: 1)
 * @returns {number} Final amount after compound interest
 */
function calculateCompoundInterest(principal, rate, time, compoundFrequency = 1) {
    // ... implementation
}
```

Configuration and constants

```javascript
const MAX_RETRIES = 3;  // Based on network reliability studies
const API_TIMEOUT = 5000;  // AWS Lambda timeout is 15s, leaving buffer
```

Annotations

```javascript
// TODO: Replace with proper user authentication after security review
// FIXME: Memory leak in production - investigate connection pooling
// HACK: Workaround for bug in library v2.1.0 - remove after upgrade
// NOTE: This implementation assumes UTC timezone for all calculations
// WARNING: This function modifies the original array instead of creating a copy
// PERF: Consider caching this result if called frequently in hot path
// SECURITY: Validate input to prevent SQL injection before using in query
// BUG: Edge case failure when array is empty - needs investigation
// REFACTOR: Extract this logic into separate utility function for reusability
// DEPRECATED: Use newApiFunction() instead - this will be removed in v3.0
```

### Anti-Patterns to Avoid

- Dead code comments (commented-out code)
- Changelog comments (history in comments)
- Divider comments (decorative banners)

### Quality Checklist

Before committing, ensure your comments:

- Explain WHY, not WHAT
- Are grammatically correct and clear
- Will remain accurate as code evolves
- Add genuine value to code understanding
- Are placed appropriately (above the code they describe)
- Use proper spelling and professional language

## Update Documentation on Code Change

### When to Update Documentation

Automatically check if documentation updates are needed when:

- New features or functionality are added
- API endpoints, methods, or interfaces change
- Breaking changes are introduced
- Dependencies or requirements change
- Configuration options or environment variables are modified
- Installation or setup procedures change
- Command-line interfaces or scripts are updated
- Code examples in documentation become outdated

### Documentation Update Rules

#### README.md Updates

Always update README.md when:

- Adding new features or capabilities
  - Add feature description to "Features" section
  - Include usage examples if applicable
  - Update table of contents if present
- Modifying installation or setup process
  - Update "Installation" or "Getting Started" section
  - Revise dependency requirements
  - Update prerequisite lists
- Adding new CLI commands or options
  - Document command syntax and examples
  - Include option descriptions and default values
  - Add usage examples
- Changing configuration options
  - Update configuration examples
  - Document new environment variables
  - Update config file templates

#### API Documentation Updates

Sync API documentation when:

- New endpoints are added
  - Document HTTP method, path, parameters
  - Include request/response examples
  - Update OpenAPI/Swagger specs
- Endpoint signatures change
  - Update parameter lists
  - Revise response schemas
  - Document breaking changes
- Authentication or authorization changes
  - Update authentication examples
  - Revise security requirements
  - Update API key/token documentation

#### Code Example Synchronization

Verify and update code examples when:

- Function signatures change
  - Update all code snippets using the function
  - Verify examples still compile/run
  - Update import statements if needed
- API interfaces change
  - Update example requests and responses
  - Revise client code examples
  - Update SDK usage examples
- Best practices evolve
  - Replace outdated patterns in examples
  - Update to use current recommended approaches
  - Add deprecation notices for old patterns

#### Configuration Documentation

Update configuration docs when:

- New environment variables are added
  - Add to .env.example file
  - Document in README.md or docs/configuration.md
  - Include default values and descriptions
- Config file structure changes
  - Update example config files
  - Document new options
  - Mark deprecated options
- Deployment configuration changes
  - Update Docker/Kubernetes configs
  - Revise deployment guides
  - Update infrastructure-as-code examples

#### Migration and Breaking Changes

Create migration guides when:

- Breaking API changes occur
  - Document what changed
  - Provide before/after examples
  - Include step-by-step migration instructions
- Major version updates
  - List all breaking changes
  - Provide upgrade checklist
  - Include common migration issues and solutions
- Deprecating features
  - Mark deprecated features clearly
  - Suggest alternative approaches
  - Include timeline for removal

### Documentation File Structure

Maintain these documentation files and update as needed:

- README.md: Project overview, quick start, basic usage
- CHANGELOG.md: Version history and user-facing changes
- docs/: Detailed documentation
  - installation.md: Setup and installation guide
  - configuration.md: Configuration options and examples
  - api.md: API reference documentation
  - contributing.md: Contribution guidelines
  - migration-guides/: Version migration guides
- examples/: Working code examples and tutorials

### Changelog Management

Add changelog entries for:

- New features (under "Added")
- Bug fixes (under "Fixed")
- Breaking changes (under "Changed" with **BREAKING** prefix)
- Deprecated features (under "Deprecated")
- Removed features (under "Removed")
- Security fixes (under "Security")

Changelog format:

```markdown
## [Version] - YYYY-MM-DD

### Added
- New feature description with reference to PR/issue

### Changed
- **BREAKING**: Description of breaking change
- Other changes

### Fixed
- Bug fix description
```

### Documentation Verification

Before applying changes, check documentation completeness:

1. All new public APIs are documented
2. Code examples compile and run
3. Links in documentation are valid
4. Configuration examples are accurate
5. Installation steps are current
6. README.md reflects current state

Include documentation validation where possible:

- Verify code examples in docs compile/run
- Check for broken internal/external links
- Validate configuration examples against schemas
- Ensure API examples match current implementation

Example validation commands:

```bash
npm run docs:check
npm run docs:test-examples
npm run docs:lint
```

### Documentation Quality Standards

- Use clear, concise language
- Include working code examples
- Provide both basic and advanced examples
- Use consistent terminology
- Include error handling examples
- Document edge cases and limitations

Code example format:

```markdown
### Example: [Clear description of what example demonstrates]

```language
// Include necessary imports/setup
import { function } from 'package';

// Complete, runnable example
const result = function(parameter);
console.log(result);
```

**Output:**
```
expected output
```
```

API documentation format:

```markdown
### `functionName(param1, param2)`

Brief description of what the function does.

**Parameters:**
- `param1` (type): Description of parameter
- `param2` (type, optional): Description with default value

**Returns:**
- `type`: Description of return value

**Example:**
```language
const result = functionName('value', 42);
```

**Throws:**
- `ErrorType`: When and why error is thrown
```

### Automation and Tooling

Use automated tools when available:

- JSDoc/TSDoc for JavaScript/TypeScript
- Sphinx/pdoc for Python
- Javadoc for Java
- xmldoc for C#
- godoc for Go
- rustdoc for Rust

Validate documentation with:

- Markdown linters (markdownlint)
- Link checkers (markdown-link-check)
- Spell checkers (cspell)
- Code example validators

Add pre-commit checks for:

- Documentation build succeeds
- No broken links
- Code examples are valid
- Changelog entry exists for changes

### Common Documentation Patterns

Feature documentation template:

```markdown
## Feature Name

Brief description of the feature.

### Usage

Basic usage example with code snippet.

### Configuration

Configuration options with examples.

### Advanced Usage

Complex scenarios and edge cases.

### Troubleshooting

Common issues and solutions.
```

API endpoint documentation template:

```markdown
### `HTTP_METHOD /api/endpoint`

Description of what the endpoint does.

**Request:**
```json
{
  "param": "value"
}
```

**Response:**
```json
{
  "result": "value"
}
```

**Status Codes:**
- 200: Success
- 400: Bad request
- 401: Unauthorized
```

### Best Practices

Do's:

- Update documentation in the same commit as code changes
- Include before/after examples for changes to be reviewed before applying
- Test code examples before committing
- Use consistent formatting and terminology
- Document limitations and edge cases
- Provide migration paths for breaking changes
- Keep documentation DRY (link instead of duplicating)

Don'ts:

- Commit code changes without updating documentation
- Leave outdated examples in documentation
- Document features that don't exist yet
- Use vague or ambiguous language
- Forget to update changelog
- Ignore broken links or failing examples
- Document implementation details users don't need

### Validation Example Commands

```json
{
  "scripts": {
    "docs:build": "Build documentation",
    "docs:test": "Test code examples in docs",
    "docs:lint": "Lint documentation files",
    "docs:links": "Check for broken links",
    "docs:spell": "Spell check documentation",
    "docs:validate": "Run all documentation checks"
  }
}
```

### Maintenance Schedule

- Monthly: Review documentation for accuracy
- Per release: Update version numbers and examples
- Quarterly: Check for outdated patterns or deprecated features
- Annually: Comprehensive documentation audit

Deprecation process:

1. Add deprecation notice to documentation
2. Update examples to use recommended alternatives
3. Create migration guide
4. Update changelog with deprecation notice
5. Set timeline for removal
6. In next major version, remove deprecated feature and docs

### Review Checklist

- Compiled instructions are based on the sum of constant and configurable instruction sections
- README.md reflects current project state
- All new features are documented
- Code examples are tested and work
- API documentation is complete and accurate
- Configuration examples are up to date
- Breaking changes are documented with migration guide
- CHANGELOG.md is updated
- Links are valid and not broken
- Installation instructions are current
- Environment variables are documented

### Documentation Goal

- Keep documentation close to code when possible
- Use documentation generators for API reference
- Maintain living documentation that evolves with code
- Consider documentation as part of feature completeness
- Review documentation in code reviews
- Make documentation easy to find and navigate
