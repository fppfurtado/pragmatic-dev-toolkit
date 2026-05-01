# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **Claude Code plugin** (not an app, not a library). It ships skills, agents, and hooks that codify the "flat & pragmatic" workflow described in `docs/philosophy.md`. There is no build step and no test suite — the artifacts are markdown frontmatter (skills/agents) and short Python scripts (hooks). Validation is manual: install the plugin into a consumer project and smoke-test the components.

The companion repo is [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit), a Copier template that generates the project layout these skills assume. They are designed to be used together but are independently usable.

## Plugin layout (what loads what)

Three component types, each with its own discovery mechanism:

- **Skills** — `skills/<name>/SKILL.md` with `name:` and `description:` frontmatter. Slash commands (`/new-feature`, `/new-adr`, `/run-plan`, `/gen-tests-python`). Skills only act when invoked by the user.
- **Agents** — `agents/<name>.md` with frontmatter. Subagents called by name (`code-reviewer`, `qa-reviewer`, `security-reviewer`). Reviewers analyze a diff and return findings.
- **Hooks** — `hooks/hooks.json` declares lifecycle bindings; the bound scripts (`hooks/*.py`) run on every matching tool call in any project that has the plugin installed. Therefore hooks **must auto-gate** (see below).

Manifests:
- `.claude-plugin/plugin.json` — plugin name/version/description (currently `0.3.0`).
- `.claude-plugin/marketplace.json` — exposes the plugin to `/plugin marketplace add fppfurtado/pragmatic-dev-toolkit`.

When bumping a release, update the version in **both** manifests **and** add a `CHANGELOG.md` entry in the existing format.

## The path contract (load-bearing)

Skills here assume the consumer project follows the path contract in `docs/philosophy.md`:

`IDEA.md`, `BACKLOG.md`, `docs/domain.md`, `docs/design.md`, `docs/decisions/ADR-NNN-*.md`, `docs/plans/<slug>.md`, `Makefile` with a `test` target, optional `.worktreeinclude`, optional project-level `.claude/agents/qa-reviewer.md` / `security-reviewer.md`.

Skills must **report a gap rather than guess** when an expected file is missing. This is non-negotiable — fabricating context defeats the alignment-first workflow.

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

1. **`/new-feature <intent>`** — alignment only, no implementation. Reads `IDEA.md` → `docs/domain.md` → `BACKLOG.md` → `docs/design.md` → `docs/decisions/`. Decides which artifact to produce (backlog line / plan / ADR / domain update) and stops. Plan blocks may be annotated `{revisor: code|qa|security}` to direct `/run-plan`.
2. **`/new-adr "<title>"`** — auto-numbers from existing `ADR-NNN-*.md` files (3-digit zero-padded), generates slug, writes template skeleton with placeholders. Has `disable-model-invocation: true` — only invoked explicitly.
3. **`/run-plan <slug>`** — the only execution skill. Creates `.worktrees/<slug>/`, replicates files listed in `.worktreeinclude`, requires green `make test` baseline, then loops per `## Arquivos a alterar` block: implement → `make test` → invoke the block's reviewer (default `code-reviewer`; `qa`/`security` annotations resolve to project-level agents in `.claude/agents/`) → micro-commit (Conventional Commits, English, no `--amend`). Blocks final "done" until the operator confirms `## Verificação manual` if the plan has that section.

When editing these skills, preserve the **alignment → plan → execute** separation. Don't let `/new-feature` start writing code; don't let `/run-plan` skip the reviewer.

## Reviewer agents

All three are invoked on a diff and report only real problems (no "consider" hedging):

- **`code-reviewer`** — YAGNI rubric: premature abstractions, redundant comments, unnecessary defensiveness, phantom backwards-compat.
- **`qa-reviewer`** — coverage of happy path + invariants from `docs/domain.md` (RNxx) + edge cases declared in `docs/design.md`; flags mocked persistence layer in integration tests.
- **`security-reviewer`** — credentials/tokens, input validation at boundaries, external HTTP timeouts, sensitive data in logs, ADR-defined post-error invariants.

The two reviewers added in 0.3 are intentionally **stack-agnostic** — they read principles from the diff. Don't add stack suffixes unless the principles themselves change.

## Editing conventions

- Documentation and skill prose are written in **Portuguese**; agent names, frontmatter keys, file paths, code, and commit messages stay in English. Don't translate cosmetically.
- Skills/agents end with an explicit `## O que NÃO fazer` section listing scope guards. Preserve that section when editing — it's load-bearing for tight skill focus.
- Don't introduce a build system, package manager, or test runner for this repo itself. The hooks are runnable Python scripts (`python3 ${CLAUDE_PLUGIN_ROOT}/hooks/<script>.py`); the rest is markdown.

## Local install for iteration

```
/plugin install /path/to/pragmatic-dev-toolkit --scope project
```

Then smoke-test in a consumer project per the checklist in `docs/install.md` (each skill appears, `.env` edits are blocked, pytest hook fires on `.py` edits inside a `pyproject.toml` ancestor, reviewers flag canonical violations).
