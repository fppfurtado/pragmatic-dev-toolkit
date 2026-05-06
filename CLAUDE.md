# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **Claude Code plugin** (not an app, not a library). It ships skills, agents, and hooks that codify the "flat & pragmatic" workflow described in `docs/philosophy.md`. There is no build step and no test suite — the artifacts are markdown frontmatter (skills/agents) and short Python scripts (hooks). Validation is manual: install the plugin into a consumer project and smoke-test the components.

The companion repo is [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit), a Copier template that generates the canonical default layout the skills assume. They are designed to be used together but are independently usable — projects with a different layout declare role variants in their `CLAUDE.md` (see `docs/philosophy.md` → "Resolução de papéis").

## Plugin layout (what loads what)

Three component types, each with its own discovery mechanism:

- **Skills** — `skills/<name>/SKILL.md` with `name:` and `description:` frontmatter. Slash commands (`/triage`, `/new-adr`, `/run-plan`, `/debug`, `/gen-tests-python`, `/release`). Skills only act when invoked by the user.
- **Agents** — `agents/<name>.md` with frontmatter. Subagents called by name (`code-reviewer`, `qa-reviewer`, `security-reviewer`). Reviewers analyze a diff and return findings.
- **Hooks** — `hooks/hooks.json` declares lifecycle bindings; the bound scripts (`hooks/*.py`) run on every matching tool call in any project that has the plugin installed. Therefore hooks **must auto-gate**. `PostToolUse` exits 0; `PreToolUse` uses exit 2 to block (see `block_env.py`).

Manifests:
- `.claude-plugin/plugin.json` — plugin name/version/description.
- `.claude-plugin/marketplace.json` — exposes the plugin to `/plugin marketplace add fppfurtado/pragmatic-dev-toolkit`.

From v1.11.0 onward, version bumps go through `/release` (dogfood). The skill resolves `version_files` from this repo's config to update **both** manifests, composes the `CHANGELOG.md` entry from the CC log since the last tag, commits and tags locally. Push remains manual.

Release cadence: accumulate merges in `main` and trigger `/release` when there's a coherent set to publish (feature complete, urgent fix, or a deliberate cadence drop) — not after every PR. The skill already groups commits since the last tag; bumping per-PR generates noisy changelog entries and version churn without proportionate value.

## The role contract (load-bearing)

Skills consume **roles**, not literal paths. Each role has a canonical default; consumer projects declare variants via the `<!-- pragmatic-toolkit:config -->` YAML block in their `CLAUDE.md`. Full protocol in `docs/philosophy.md` → "Resolução de papéis".

Roles and canonical defaults: `product_direction` → `IDEA.md`, `ubiquitous_language` → `docs/domain.md`, `design_notes` → `docs/design.md`, `decisions_dir` → `docs/decisions/`, `plans_dir` → `docs/plans/`, `backlog` → `BACKLOG.md`, `version_files` → _(no default — opt-in list)_, `changelog` → `CHANGELOG.md`, `test_command` → `make test`. Plugin-internal: `.worktreeinclude` (consumed by `/run-plan`). Reviewers `qa-reviewer` and `security-reviewer` ship as plugin agents — consumer projects can shadow either with a project-level `.claude/agents/<name>.md` (Claude Code convention; project-level wins on name collision).

Resolution order (per role): probe canonical → consult config block in consumer's `CLAUDE.md` → ask the operator with tri-state response (`path | "não temos" | <other path>`). Skills must **report a gap rather than guess** when a required role resolves to "não temos". This is non-negotiable — fabricating context defeats the alignment-first workflow.

## Editing conventions

- The plugin adapts to the consumer project's language at runtime (see `docs/philosophy.md` → "Convenção de idioma"). For **this** repo specifically the canonical default applies: documentation and skill/agent prose are in **Portuguese**; mechanism stays in English — agent names, frontmatter keys, file paths, code, and `CLAUDE.md` itself (it's agent operating instructions, not user-facing prose). Don't translate cosmetically.
- Commit messages follow the consumer project's commit convention (see `docs/philosophy.md` → "Convenção de commits"). For **this** repo the git log shows a stable pattern of Conventional Commits in English — keep it.
- Skills/agents end with an explicit `## O que NÃO fazer` section listing scope guards. Preserve that section when editing — it's load-bearing for tight skill focus.
- Don't introduce a build system, package manager, or test runner for this repo itself. The hooks are runnable Python scripts (`python3 ${CLAUDE_PLUGIN_ROOT}/hooks/<script>.py`); the rest is markdown.
- From v1.11.0 onward, version bumps in **this** repo go through `/release` — keep the loop closed by dogfooding rather than editing manifests by hand.

## Pragmatic Toolkit
<!-- pragmatic-toolkit:config -->
```yaml
paths:
  version_files: [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"]
test_command: null  # repo has no test suite; /run-plan falls back to plan's `## Verificação manual`
```

## Local install for iteration

```
/plugin install /path/to/pragmatic-dev-toolkit --scope project
```

Then smoke-test in a consumer project per the checklist in `docs/install.md` (each skill appears, `.env` edits are blocked, pytest hook fires on `.py` edits inside a `pyproject.toml` ancestor, reviewers flag canonical violations).
