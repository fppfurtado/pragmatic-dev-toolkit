# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **Claude Code plugin** (not an app, not a library). It ships skills, agents, and hooks that codify the "flat & pragmatic" workflow described in `docs/philosophy.md`. There is no build step and no test suite — the artifacts are markdown frontmatter (skills/agents) and short Python scripts (hooks). Validation is manual: install the plugin into a consumer project and smoke-test the components.

The companion repo is [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit), a Copier template that generates the canonical default layout the skills assume. They are designed to be used together but are independently usable — projects with a different layout declare role variants in their `CLAUDE.md` (see `docs/philosophy.md` → "Resolução de papéis").

## Plugin layout (what loads what)

Three component types, each with its own discovery mechanism:

- **Skills** — `skills/<name>/SKILL.md` with `name:` and `description:` frontmatter. Slash commands (`/new-feature`, `/new-adr`, `/run-plan`, `/gen-tests-python`). Skills only act when invoked by the user.
- **Agents** — `agents/<name>.md` with frontmatter. Subagents called by name (`code-reviewer`, `qa-reviewer`, `security-reviewer`). Reviewers analyze a diff and return findings.
- **Hooks** — `hooks/hooks.json` declares lifecycle bindings; the bound scripts (`hooks/*.py`) run on every matching tool call in any project that has the plugin installed. Therefore hooks **must auto-gate** (see below).

Manifests:
- `.claude-plugin/plugin.json` — plugin name/version/description.
- `.claude-plugin/marketplace.json` — exposes the plugin to `/plugin marketplace add fppfurtado/pragmatic-dev-toolkit`.

When bumping a release, update the version in **both** manifests **and** add a `CHANGELOG.md` entry in the existing format.

## The role contract (load-bearing)

Skills consume **roles**, not literal paths. Each role has a canonical default; consumer projects declare variants via the `<!-- pragmatic-toolkit:config -->` YAML block in their `CLAUDE.md`. Full protocol in `docs/philosophy.md` → "Resolução de papéis".

Roles and canonical defaults: `product_direction` → `IDEA.md`, `ubiquitous_language` → `docs/domain.md`, `design_notes` → `docs/design.md`, `decisions_dir` → `docs/decisions/`, `plans_dir` → `docs/plans/`, `backlog` → `BACKLOG.md`, `test_command` → `make test`. Plugin-internal: `.worktreeinclude` (consumed by `/run-plan`) and project-level `.claude/agents/qa-reviewer.md` / `security-reviewer.md` follow Claude Code conventions.

Resolution order (per role): probe canonical → consult config block in consumer's `CLAUDE.md` → ask the operator with tri-state response (`path | "não temos" | <other path>`). Skills must **report a gap rather than guess** when a required role resolves to "não temos". This is non-negotiable — fabricating context defeats the alignment-first workflow.

## Naming convention (stack-specific vs generic)

Documented in `docs/philosophy.md` and enforced by review:

| Type | Generic | Stack-specific |
|------|---------|----------------|
| Hook script | `<purpose>.py` | `<purpose>_<stack>.py` (e.g. `run_pytest_python.py`) |
| Skill | `<verb>-<artifact>` | `<verb>-<artifact>-<stack>` (e.g. `gen-tests-python`) |
| Agent | `<role>` | `<role>-<stack>` (only if principles change with stack) |

**Components that generate or execute stack-specific things require the suffix** (concrete syntax/commands have no neutral form). **Components that review principles from a diff do not** (the stack is in the diff itself) — that's why `qa-reviewer` and `security-reviewer` ship without suffixes.

## Hook auto-gating triple (mandatory)

Hooks fire in every project where the plugin is installed, so a stack-specific hook must silently no-op outside its stack. Triple gate (see `hooks/run_pytest_python.py` for the canonical example):

1. **Extension** — `if not file_path.endswith(".py"): return 0`.
2. **Stack marker** — walk ancestors looking for `pyproject.toml` (or equivalent). No marker → exit 0.
3. **Toolchain** — prefer the modern tool (e.g. `uv run pytest`), fall back to `python -m pytest`. If the toolchain is missing, exit 0.

`PostToolUse` hooks must always exit 0 (do not block subsequent hooks). Use exit 2 only for `PreToolUse` blocking (see `block_env.py`).

## Skill workflow contract

The three workflow skills compose in a deliberate order:

1. **`/new-feature <intent>`** — alignment only, no implementation. Reads roles in order: `product_direction` → `ubiquitous_language` → `backlog` → `design_notes` → `decisions_dir`. Decides which artifact to produce (backlog line / plan / ADR / domain update) and stops. Plan blocks may be annotated `{revisor: code|qa|security}` to direct `/run-plan`.
2. **`/new-adr "<title>"`** — auto-numbers within the resolved `decisions_dir` by **inferring** the format from existing ADRs (3-digit padded canonical, 4-digit padded, or no padding); generates slug, writes template skeleton with placeholders. Has `disable-model-invocation: true` — only invoked explicitly.
3. **`/run-plan <slug>`** — the only execution skill. Creates `.worktrees/<slug>/`, replicates files listed in `.worktreeinclude`, requires the resolved `test_command` (default `make test`) to be green as baseline, then loops per "files to change" block (canonical PT-BR `## Arquivos a alterar`, matched semantically): implement → run `test_command` → invoke the block's reviewer (default `code-reviewer`; `qa`/`security` annotations resolve to project-level agents in `.claude/agents/`) → micro-commit following the project's commit convention (see `docs/philosophy.md` → "Convenção de commits"; canonical default is Conventional Commits in English; never `--amend`). Blocks final "done" until the operator confirms the manual-verification section if the plan has one.

When editing these skills, preserve the **alignment → plan → execute** separation. Don't let `/new-feature` start writing code; don't let `/run-plan` skip the reviewer.

## Reviewer agents

All three are invoked on a diff and report only real problems (no "consider" hedging):

- **`code-reviewer`** — YAGNI rubric: premature abstractions, redundant comments, unnecessary defensiveness, phantom backwards-compat.
- **`qa-reviewer`** — coverage of happy path + invariants documented by the project's `ubiquitous_language` role (RNxx) + edge cases declared by the `design_notes` role; flags mocked persistence layer in integration tests.
- **`security-reviewer`** — credentials/tokens, input validation at boundaries, external HTTP timeouts, sensitive data in logs, post-error invariants defined by ADRs in the `decisions_dir` role.

The two reviewers added in 0.3 are intentionally **stack-agnostic** — they read principles from the diff. Don't add stack suffixes unless the principles themselves change.

## Editing conventions

- The plugin adapts to the consumer project's language at runtime (see `docs/philosophy.md` → "Convenção de idioma"). For **this** repo specifically the canonical default applies: documentation and skill/agent prose are in **Portuguese**; mechanism stays in English — agent names, frontmatter keys, file paths, code, and `CLAUDE.md` itself (it's agent operating instructions, not user-facing prose). Don't translate cosmetically.
- Commit messages follow the consumer project's commit convention (see `docs/philosophy.md` → "Convenção de commits"). For **this** repo the git log shows a stable pattern of Conventional Commits in English — keep it.
- Skills/agents end with an explicit `## O que NÃO fazer` section listing scope guards. Preserve that section when editing — it's load-bearing for tight skill focus.
- Don't introduce a build system, package manager, or test runner for this repo itself. The hooks are runnable Python scripts (`python3 ${CLAUDE_PLUGIN_ROOT}/hooks/<script>.py`); the rest is markdown.

## Local install for iteration

```
/plugin install /path/to/pragmatic-dev-toolkit --scope project
```

Then smoke-test in a consumer project per the checklist in `docs/install.md` (each skill appears, `.env` edits are blocked, pytest hook fires on `.py` edits inside a `pyproject.toml` ancestor, reviewers flag canonical violations).
