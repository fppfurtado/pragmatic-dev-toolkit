# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **Claude Code plugin** (not an app, not a library). It ships skills, agents, and hooks that codify the "flat & pragmatic" workflow described in `docs/philosophy.md`. There is no build step and no test suite — the artifacts are markdown frontmatter (skills/agents) and short Python scripts (hooks). Validation is manual: install the plugin into a consumer project and smoke-test the components.

The companion repo is [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit), a Copier template that generates the canonical default layout the skills assume. They are designed to be used together but are independently usable — projects with a different layout declare role variants in their `CLAUDE.md` (see "The role contract" below).

## Plugin layout (what loads what)

Three component types, each with its own discovery mechanism:

- **Skills** — `skills/<name>/SKILL.md` with `name:` and `description:` frontmatter. Slash commands (`/triage`, `/new-adr`, `/run-plan`, `/debug`, `/gen-tests-python`, `/release`). Skills only act when invoked by the user.
- **Agents** — `agents/<name>.md` with frontmatter. Subagents called by name (`code-reviewer`, `qa-reviewer`, `security-reviewer`, `doc-reviewer`). Reviewers analyze a diff and return findings.
- **Hooks** — `hooks/hooks.json` declares lifecycle bindings; the bound scripts (`hooks/*.py`) run on every matching tool call in any project that has the plugin installed. Therefore hooks **must auto-gate**. `PostToolUse` exits 0; `PreToolUse` uses exit 2 to block (see `block_env.py`).

Manifests:
- `.claude-plugin/plugin.json` — plugin name/version/description.
- `.claude-plugin/marketplace.json` — exposes the plugin to `/plugin marketplace add fppfurtado/pragmatic-dev-toolkit`.

From v1.11.0 onward, version bumps go through `/release` (dogfood). The skill resolves `version_files` from this repo's config to update **both** manifests, composes the `CHANGELOG.md` entry from the CC log since the last tag, commits and tags locally. Push remains manual.

Release cadence: accumulate merges in `main` and trigger `/release` when there's a coherent set to publish (feature complete, urgent fix, or a deliberate cadence drop) — not after every PR. The skill already groups commits since the last tag; bumping per-PR generates noisy changelog entries and version churn without proportionate value.

## The role contract (load-bearing)

Skills consume **roles**, not literal paths. Each role has a canonical default; consumer projects declare variants via the `<!-- pragmatic-toolkit:config -->` YAML block in their `CLAUDE.md` (see "Pragmatic Toolkit" section below for schema and semantics).

Roles and canonical defaults: `product_direction` → `IDEA.md`, `ubiquitous_language` → `docs/domain.md`, `design_notes` → `docs/design.md`, `decisions_dir` → `docs/decisions/`, `plans_dir` → `docs/plans/`, `backlog` → `BACKLOG.md`, `version_files` → _(no default — opt-in list)_, `changelog` → `CHANGELOG.md`, `test_command` → `make test`. Plugin-internal: `.worktreeinclude` (consumed by `/run-plan`). Reviewers `qa-reviewer`, `security-reviewer`, and `doc-reviewer` ship as plugin agents — consumer projects can shadow any of them with a project-level `.claude/agents/<name>.md` (Claude Code convention; project-level wins on name collision).

### Resolution protocol

Each skill resolves the roles it needs before acting, following a single protocol to avoid drift:

1. **Probe canonical.** Test if the default filename exists (e.g., `docs/domain.md` for `ubiquitous_language`). Probe is exact, no fuzzy matching: `README.md` is not assumed to be `IDEA.md`.
2. **Consult CLAUDE.md.** If canonical is absent, read consumer's `CLAUDE.md` looking for the `<!-- pragmatic-toolkit:config -->` block. Declared value beats absent canonical.
3. **Ask the operator.** If still absent and the role is needed, ask with tri-state response: **concrete path** (skill uses it) | **`não temos`** (skill proceeds without input if role is informational, or stops with gap report if required) | **other path** (operator points to equivalent file). Mode: enum via `AskUserQuestion` with two named options (`Não usamos esse papel`, `Existe em outro path`) plus auto-`Other` receiving the concrete path; header = role name.
4. **One-shot memoization offer.** At the end of the invocation, propose once to record the resolution in the `<!-- pragmatic-toolkit:config -->` block. `n` = ask again next time. Mode: binary enum (`Sim, registrar` / `Não, perguntar de novo`).

**Drift detection.** If canonical exists AND CLAUDE.md declares a different variant, the skill flags the inconsistency to the operator before proceeding — likely a forgotten rename.

### Required vs informational roles

Skills treat them differently:

- **Required** — `plans_dir` (where `/run-plan` reads and `/triage` writes plans); `test_command` in `/run-plan` when the plan has no `## Verificação end-to-end`; `decisions_dir` in `/new-adr` (where the ADR is written). Required role absent without alternative → skill must **report a gap rather than guess**. Non-negotiable — fabricating context defeats the alignment-first workflow.
- **Informational** (skill proceeds without): `product_direction`, `ubiquitous_language`, `design_notes`, ADRs, `backlog`, `test_command` when the plan provides `## Verificação end-to-end`. In `/debug`, **all** consumed roles are informational — absence reduces the hypothesis base, never blocks. In `/gen-tests-python`, `ubiquitous_language` and `design_notes` are informational; absence of `pyproject.toml` makes the skill refuse by stack contradiction (not a role gap). In `/release`, `version_files` and `changelog` are informational — absence reduces release scope (degenerate case: just commit + tag). In `/triage`, `backlog` is informational — absence means no line is recorded (one-shot creation offer on first run).

## Editing conventions

- The plugin adapts to the consumer project's language at runtime (see `docs/philosophy.md` → "Convenção de idioma"). For **this** repo specifically the canonical default applies: documentation and skill/agent prose are in **Portuguese**; mechanism stays in English — agent names, frontmatter keys, file paths, code, and `CLAUDE.md` itself (it's agent operating instructions, not user-facing prose). Don't translate cosmetically.
- Commit messages follow the consumer project's commit convention (see `docs/philosophy.md` → "Convenção de commits"). For **this** repo the git log shows a stable pattern of Conventional Commits in English — keep it.
- Skills end with an explicit `## O que NÃO fazer` section listing scope guards. Preserve that section when editing — it's load-bearing for tight skill focus. **Critério editorial:** lista apenas guardas que documentam anti-padrão não-óbvio. Item que apenas reafirma prosa anterior do skill é ruído — se sua remoção não confundiria um leitor razoável que leu o resto do skill, não pertence aqui. Itens vindos de incidentes ou de anti-padrões sutis (modelo tem viés de autoinvocação, gatilho condicional facilmente esquecido, exceção localizada que não é óbvia) são não-óbvios e devem permanecer.
- Don't introduce a build system, package manager, or test runner for this repo itself. The hooks are runnable Python scripts (`python3 ${CLAUDE_PLUGIN_ROOT}/hooks/<script>.py`); the rest is markdown.
- From v1.11.0 onward, version bumps in **this** repo go through `/release` — keep the loop closed by dogfooding rather than editing manifests by hand.

## Pragmatic Toolkit

Consumer projects declare path-contract variants in a fenced YAML block marked by the HTML comment below. Skills search for the marker; absence = all canonical defaults.

<!-- pragmatic-toolkit:config -->
```yaml
paths:
  version_files: [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"]
test_command: null  # repo has no test suite; /run-plan falls back to plan's `## Verificação end-to-end`
```

**Schema and semantics:**

- Missing key → canonical default.
- `null` (or explicit `false`) → "não usamos esse papel". Skill treats as absent without asking again.
- Unknown keys are ignored (forward-compat for releases that add new roles).
- Keys live under `paths.<role>` (top-level `test_command` as exception); reference list in "Roles and canonical defaults" above.
- The HTML marker `<!-- pragmatic-toolkit:config -->` is what the skill looks for — without it, the YAML block is not interpreted even if under the `## Pragmatic Toolkit` heading.

## Local install for iteration

```
/plugin install /path/to/pragmatic-dev-toolkit --scope project
```

Then smoke-test in a consumer project per the checklist in `docs/install.md` (each skill appears, `.env` edits are blocked, pytest hook fires on `.py` edits inside a `pyproject.toml` ancestor, reviewers flag canonical violations).
