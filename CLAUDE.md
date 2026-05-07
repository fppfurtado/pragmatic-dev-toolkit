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

Skills consume **roles**, not literal paths. Each role has a canonical default; consumer projects declare variants via the `<!-- pragmatic-toolkit:config -->` YAML block in their `CLAUDE.md` (see "Pragmatic Toolkit" section below for schema and semantics). Conceptual rationale (papéis vs paths) in `docs/philosophy.md` → "Path contract".

| Role | Default | Description |
|------|---------|-------------|
| `product_direction` | `IDEA.md` | What we're building and why. Product direction. |
| `ubiquitous_language` | `docs/domain.md` | Bounded contexts, ubiquitous language, aggregates/entities, invariants (RNxx) — when the domain warrants formalization. |
| `design_notes` | `docs/design.md` | Quirks of external integrations not covered by official docs. |
| `decisions_dir` | `docs/decisions/` | Directory of immutable structural decisions. Numbering and slug owned by `/new-adr`. |
| `plans_dir` | `docs/plans/<slug>.md` | Multi-phase plans for changes that require upfront alignment. |
| `backlog` | `BACKLOG.md` | Short exploratory list — `## Próximos` (curatorial) and `## Concluídos` (editorial registry, append-only). State of in-flight work lives in git/forge per ADR-004. |
| `version_files` | _(no default — opt-in)_ | Paths whose version string is updated on each release. Empty or absent = role disabled. Consumed by `/release`. |
| `changelog` | `CHANGELOG.md` | Release history. `/release` prepends a new block at each bump. |
| `test_command` | `make test` (with `Makefile`) | Automatic gate at execution steps. |
| (plugin-internal) | `.worktreeinclude` | Optional gitignored paths to replicate in fresh worktrees. Consumed by `/run-plan`. |
| (agents shipped by the plugin) | `qa-reviewer`, `security-reviewer`, `doc-reviewer` | Generic baseline invoked by `/run-plan` per `{reviewer: qa\|security\|doc}` annotation on the plan block. Consumer projects can shadow with project-level `.claude/agents/<name>.md` (project-level wins on collision). |

### Resolution protocol

Each skill declares its roles in `roles.required` and `roles.informational` in the frontmatter (ADR-003). The resolution protocol applies to each declared role: required absent follows one of the 3 default behavior tracks below; informational absent → skill proceeds silently (reduces context/hypotheses, never blocks). Special sub-flows (canonical creation via enum, conditionals like `test_command` in `/run-plan`, stack contradiction in `/gen-tests-python`) live in skill prose.

1. **Probe canonical.** Test if the default filename exists (e.g., `docs/domain.md` for `ubiquitous_language`). Probe is exact, no fuzzy matching: `README.md` is not assumed to be `IDEA.md`.
2. **Consult CLAUDE.md.** If canonical is absent, read consumer's `CLAUDE.md` looking for the `<!-- pragmatic-toolkit:config -->` block. Declared value beats absent canonical.
3. **Ask the operator.** If still absent and the role is needed, ask with tri-state response: **concrete path** (skill uses it) | **`não temos`** (skill proceeds without input if role is informational, or stops with gap report if required) | **other path** (operator points to equivalent file). Mode: enum via `AskUserQuestion` with two named options (`Não usamos esse papel`, `Existe em outro path`) plus auto-`Other` receiving the concrete path; header = role name.
4. **One-shot memoization offer.** At the end of the invocation, propose once to record the resolution in the `<!-- pragmatic-toolkit:config -->` block. `n` = ask again next time. Mode: binary enum (`Sim, registrar` / `Não, perguntar de novo`).

**Drift detection.** If canonical exists AND CLAUDE.md declares a different variant, the skill flags the inconsistency to the operator before proceeding — likely a forgotten rename.

### Required vs informational roles

**Required** = skill cannot proceed without the role; **informational** = reduces context/hypotheses, never blocks. Each SKILL declares in frontmatter which role belongs to which category (the same role may have different criticalities in different skills — see ADR-003).

**Default behavior for absent required role** (3 tracks; each SKILL declares in prose which one applies when it differs from the default `inform and stop`):

- **Capture immediately + stop** — when the issue is project/setup state. E.g., `/run-plan` precondition 3 (red baseline), 4 (orphan worktree).
- **Offer canonical creation via enum** — when the role has a clear canonical default and the skill can create it. E.g., `/triage` step 4; `/new-adr` creating `docs/decisions/` on first invocation.
- **Inform and stop** (default) — when the role is BACKLOG itself (paradox of where to capture) or the skill cannot resolve and the operator must create manually. E.g., `/next` without `backlog`.

### Local mode (`paths.<role>: local`)

Activated at step 2 of the resolution protocol when CLAUDE.md declares the role as `local` (instead of a path or null) — bypasses the absent-role tracks above. Defined by [ADR-005](docs/decisions/ADR-005-modo-local-gitignored-roles.md). Applies to `decisions_dir`, `backlog`, `plans_dir` (`version_files` and `changelog` reject local mode — `/release` stops with a clear message).

On first resolution per invocation:

1. **Ensure directory:** `mkdir -p .claude/local/<role>/` if absent. Silent operation. Plugin **never touches `.claude/` root** — Claude Code's territory, out of the plugin's scope.
2. **Probe gitignore:** `git check-ignore -q .claude/local/<role>/.probe`. Covered → proceed silent. Uncovered → trigger gate.
3. **Gate `Gitignore`:** propose adding `.claude/local/` entry to the project's `.gitignore`. Options: `Adicionar entrada` / `Cancelar`. Cancel → refuse local mode for this invocation + report risk. Creates `.gitignore` if absent (first-time setup in the project); aborts with clear message if not a git repo (`git rev-parse` returns non-zero).

Skills that generate commit messages, PR descriptions, or branch metadata (`/triage`, `/run-plan`) **do not reference any identifier of the artifact** in local mode (ADR ID, plan slug, backlog line text) in external messages. In canonical mode (default), current reference behavior is preserved.

Concrete paths: `.claude/local/decisions/`, `.claude/local/BACKLOG.md`, `.claude/local/plans/<slug>.md`.

## Editing conventions

- The plugin adapts to the consumer project's language at runtime (see `docs/philosophy.md` → "Convenção de idioma"). For **this** repo specifically the canonical default applies: documentation and skill/agent prose are in **Portuguese**; mechanism stays in English — agent names, frontmatter keys, file paths, code, and `CLAUDE.md` itself (it's agent operating instructions, not user-facing prose). Don't translate cosmetically.
- Commit messages follow the consumer project's commit convention (see `docs/philosophy.md` → "Convenção de commits"). For **this** repo the git log shows a stable pattern of Conventional Commits in English — keep it.
- Skills end with an explicit `## O que NÃO fazer` section listing scope guards. Preserve that section when editing — it's load-bearing for tight skill focus. **Critério editorial:** lista apenas guardas que documentam anti-padrão não-óbvio. Item que apenas reafirma prosa anterior do skill é ruído — se sua remoção não confundiria um leitor razoável que leu o resto do skill, não pertence aqui. Itens vindos de incidentes ou de anti-padrões sutis (modelo tem viés de autoinvocação, gatilho condicional facilmente esquecido, exceção localizada que não é óbvia) são não-óbvios e devem permanecer.
- Don't introduce a build system, package manager, or test runner for this repo itself. The hooks are runnable Python scripts (`python3 ${CLAUDE_PLUGIN_ROOT}/hooks/<script>.py`); the rest is markdown.
- From v1.11.0 onward, version bumps in **this** repo go through `/release` — keep the loop closed by dogfooding rather than editing manifests by hand.

## AskUserQuestion mechanics

Concrete shape for the `AskUserQuestion` tool when used by skills (philosophy and choice criterion in `docs/philosophy.md` → "Convenção de pergunta ao operador"):

- **Header** (chip/tag): ≤ 12 chars. Examples: `Commit`, `Backlog`, `Publicar`, `Branch`.
- **Options**: 2-4 per question. `Other` is automatic — never list it explicitly. Each option carries a concrete trade-off in `description` (cost, maintenance, virtue delivered); description-obvious like "choose A" signals a cosmetic enum.
- **Bifurcação discreta presente → enum, mesmo com Other comum** (ADR-006). Quando há ≥1 resposta comum **discreta** identificável, prefira enum — o `Other` automático cobre as livres com 1 toque a menos no caminho discreto. Prosa só é o modo certo quando **todas** as respostas comuns são livres (descrição de bug, justificativa de escopo, exemplo de dado real).
- **Multiple related questions** in a single call: up to 4 (`questions` array).
- **Unificação preferida sobre sequência.** Quando ≥2 perguntas relacionadas no mesmo passo são enum-áveis, **agrupar numa única chamada** em vez de sequenciar — fragmentação tira foco do operador.
- **`multiSelect: true`** when the choices are not mutually exclusive (e.g., picking gitignored files to replicate into a worktree).
- **Recommended option**: place first and append "(Recommended)" to the label.
- **`(Recommended)` só quando o default é estatisticamente estável.** Marcar apenas quando uma resposta é dominante na maioria das invocações da skill. Quando o "recomendado" depende de contexto runtime (modo, estado, decisão anterior), o SKILL deve **construir opções dinamicamente** em vez de fixar `(Recommended)` na prosa — ex.: `/run-plan` §3.7 escolhe Recommended por `plans_dir` mode. Recommended sem default real é viés enganoso.

## Plugin component naming and hook auto-gating

Skills and hooks stack-specific coexist with generic components in the same plugin. The name carries the contract:

| Type | Generic | Stack-specific |
|------|---------|----------------|
| Hook (script) | `<purpose>.py\|.sh` (e.g., `block_env.py`) | `<purpose>_<stack>.py\|.sh` (e.g., `run_pytest_python.py`) |
| Skill (frontmatter `name`) | `<verb>-<artifact>` (e.g., `new-adr`) **or** `<verb>` when the artifact emerges from the skill's decision (e.g., `triage`) | `<verb>-<artifact>-<stack>` (e.g., `gen-tests-python`) |
| Agent (frontmatter `name`) | `<role>` (e.g., `code-reviewer`, `qa-reviewer`, `security-reviewer`) | `<role>-<stack>` (only if principles change with the stack) |

Skill whose output is fixed (always produces an ADR, always executes a plan) carries `<verb>-<artifact>` — the name promises the output. Skill whose output is decided per invocation among multiple options (e.g., `/triage` decides among backlog line, plan, ADR, or domain update) carries only `<verb>` — a fixed suffix would lie about what comes out.

**Hook auto-gating triplo** (a hook fires in every project where the plugin is installed, so the gating is non-negotiable for safe shipping):

1. **File extension** — `if not file_path.endswith(".py"): exit 0` filters most cases at zero cost.
2. **Stack marker** — walk ancestors looking for `pyproject.toml` (Python), `build.gradle*`/`pom.xml` (JVM), etc. No marker → `exit 0`.
3. **Toolchain** — only run the tool (`uv run pytest`, `gradle test`) with reasonable fallback; if the toolchain isn't installed, `exit 0`.

This makes it safe to ship `run_pytest_python.py` alongside `run_gradle_test_java.sh` in the same plugin: each hook is silent in projects outside its stack, with no flags or env vars to disable.

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
- `local` (string literal) → local-gitignored mode. Skill creates/reads under `.claude/local/<role>/`, artifact is not committed, commit/PR/branch metadata do not reference it (see "Local mode" section above; full rationale in [ADR-005](docs/decisions/ADR-005-modo-local-gitignored-roles.md)). Applies to `decisions_dir`, `backlog`, `plans_dir`; `version_files`/`changelog` reject this value.
- Unknown keys are ignored (forward-compat for releases that add new roles).
- Keys live under `paths.<role>` (top-level `test_command` as exception); reference list in "Roles and canonical defaults" above.
- The HTML marker `<!-- pragmatic-toolkit:config -->` is what the skill looks for — without it, the YAML block is not interpreted even if under the `## Pragmatic Toolkit` heading.

## Local install for iteration

```
/plugin install /path/to/pragmatic-dev-toolkit --scope project
```

Then smoke-test in a consumer project per the checklist in `docs/install.md` (each skill appears, `.env` edits are blocked, pytest hook fires on `.py` edits inside a `pyproject.toml` ancestor, reviewers flag canonical violations).
