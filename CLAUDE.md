# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **Claude Code plugin** (not an app, not a library). It ships skills, agents, and hooks that codify the "flat & pragmatic" workflow described in `docs/philosophy.md`. There is no build step and no test suite — the artifacts are markdown frontmatter (skills/agents) and short Python scripts (hooks). Validation is manual: install the plugin into a consumer project and smoke-test the components.

The companion repo is [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit), a Copier template that generates the canonical default layout the skills assume. They are designed to be used together but are independently usable — projects with a different layout declare role variants in their `CLAUDE.md` (see "The role contract" below).

## Plugin layout (what loads what)

Three component types, each with its own discovery mechanism:

- **Skills** — `skills/<name>/SKILL.md` with `name:` and `description:` frontmatter. Slash commands (`/draft-idea`, `/triage`, `/new-adr`, `/run-plan`, `/debug`, `/gen-tests`, `/release`, `/next`, `/init-config`, `/archive-plans`, `/curate-backlog`). Skills only act when invoked by the user.
- **Agents** — `agents/<name>.md` with frontmatter. Five reviewers shipped: `code-reviewer`, `qa-reviewer`, `security-reviewer`, `doc-reviewer`, `design-reviewer`. Dispatch rules in "The role contract" table below.
- **Hooks** — `hooks/hooks.json` declares lifecycle bindings; the bound scripts (`hooks/*.py`) run on every matching tool call in any project that has the plugin installed. Therefore hooks **must auto-gate**. `PostToolUse` exits 0; `PreToolUse` uses exit 2 to block (see `block_env.py`).

Manifests:
- `.claude-plugin/plugin.json` — plugin name/version/description.
- `.claude-plugin/marketplace.json` — exposes the plugin to `/plugin marketplace add fppfurtado/pragmatic-dev-toolkit`.

Version bumps go through `/release` (dogfood). The skill resolves `version_files` from this repo's config to update **both** manifests, composes the `CHANGELOG.md` entry from the CC log since the last tag, commits and tags locally. Push remains manual.

Release cadence: trigger `/release` when there's a coherent set to publish (feature complete, urgent fix, or deliberate cadence drop); per-PR bumps generate noisy changelog entries and version churn.

## The role contract (load-bearing)

Skills consume **roles**, not literal paths. Each role has a canonical default; consumer projects declare variants via the `<!-- pragmatic-toolkit:config -->` YAML block in their `CLAUDE.md` (see "Pragmatic Toolkit" section below for schema and semantics). Conceptual rationale (papéis vs paths) in `docs/philosophy.md` → "Path contract".

| Role | Default | Description |
|------|---------|-------------|
| `product_direction` | `IDEA.md` | Why the project exists and what direction it carries — about the project as a whole, not a feature/initiative within it. Features and local initiatives go through `/triage`. |
| `ubiquitous_language` | `docs/domain.md` | Bounded contexts, ubiquitous language, aggregates/entities, invariants (RNxx) — when the domain warrants formalization. |
| `design_notes` | `docs/design.md` | Quirks of external integrations not covered by official docs. |
| `decisions_dir` | `docs/decisions/` | Directory of immutable structural decisions. Numbering and slug owned by `/new-adr`. |
| `plans_dir` | `docs/plans/<slug>.md` | Multi-phase plans for changes that require upfront alignment. |
| `backlog` | `BACKLOG.md` | Short exploratory list — `## Próximos` (curatorial) and `## Concluídos` (editorial registry, append-only). State of in-flight work lives in git/forge per ADR-049 § Decisão (a). Accepts `paths.backlog: forge` mode (per [ADR-058](docs/decisions/ADR-058-role-backlog-aceitar-forge.md)) where the role is sourced from open issues without assignee in the current repo (auto-detect via `gh`/`glab`); item identifier becomes `#<número>: <título>`. |
| `version_files` | _(no default — opt-in)_ | Paths whose version string is updated on each release. Empty or absent = role disabled. Consumed by `/release`. |
| `changelog` | `CHANGELOG.md` | Release history. `/release` prepends a new block at each bump. |
| `test_command` | `make test` (with `Makefile`) | Automatic gate at execution steps. |
| (plugin-internal) | `.worktreeinclude` | Optional gitignored paths to replicate in fresh worktrees. Consumed by `/run-plan`. |
| (plugin-internal) | `.claude/local/NOTES.md` | Cross-session context store written by `/note` (append-only, local-gitignored per [ADR-047](docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md) extended in [ADR-054](docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (a)+(b); non-role). Cross-project write via `/note --to <projeto-ou-path>` — discovery via `$PROJECTS_DIR` with absolute-path fallback; target must be initialized for local mode (refusal otherwise). |
| (agents shipped by the plugin) | `qa-reviewer`, `security-reviewer`, `doc-reviewer`, `design-reviewer` | `qa-reviewer`, `security-reviewer`, `doc-reviewer` are invoked by `/run-plan` per `{reviewer: qa\|security\|doc}` annotation on the plan block. `design-reviewer` operates on documents pre-fact (plan/ADR draft); invoked automatically by `/triage` (plan-producing path) and `/new-adr` (standalone or delegated) per [ADR-053](docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (b), or manually via `@design-reviewer`. Consumer projects can shadow any of them with project-level `.claude/agents/<name>.md` (project-level wins on collision). |

### Resolution protocol

Each skill declares its roles in `roles.required` and `roles.informational` in the frontmatter (ADR-003). The resolution protocol applies to each declared role: required absent follows one of the 3 default behavior tracks below; informational absent → skill proceeds silently (reduces context/hypotheses, never blocks). Special sub-flows (canonical creation via enum, conditionals like `test_command` in `/run-plan`, stack contradiction in `/gen-tests`) live in skill prose.

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

Activated at step 2 of the resolution protocol when CLAUDE.md declares the role as `local` (instead of a path or null) — bypasses the absent-role tracks above. Defined by [ADR-047](docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md). Applies to `decisions_dir`, `backlog`, `plans_dir` (`version_files` and `changelog` reject local mode — `/release` stops with a clear message).

On first resolution per invocation:

1. **Ensure directory:** `mkdir -p .claude/local/<role>/` if absent. Silent operation. Plugin **never touches `.claude/` root** — Claude Code's territory, out of the plugin's scope.
2. **Probe gitignore:** `git check-ignore -q .claude/local/<role>/.probe`. Covered → proceed silent. Uncovered → trigger gate.
3. **Gate `Gitignore`:** propose adding `.claude/local/` entry to the project's `.gitignore`. Options: `Adicionar entrada` / `Cancelar`. Cancel → refuse local mode for this invocation + report risk. Creates `.gitignore` if absent (first-time setup in the project); aborts with clear message if not a git repo (`git rev-parse` returns non-zero).

Skills that generate commit messages, PR descriptions, or branch metadata (`/triage`, `/run-plan`) **do not reference any identifier of the artifact** in local mode (ADR ID, plan slug, backlog line text) in external messages. In canonical mode (default), current reference behavior is preserved.

Concrete paths: `.claude/local/decisions/`, `.claude/local/BACKLOG.md`, `.claude/local/plans/<slug>.md`.

**Coexistência com modo `forge`** ([ADR-058](docs/decisions/ADR-058-role-backlog-aceitar-forge.md)): `paths.backlog: forge` é eixo paralelo a `local` na família `paths.<role>: <modo>` (4 variantes: canonical/local/null/forge). Combinação `paths.backlog: forge` + `paths.decisions_dir: local` é caso válido (time + dev pessoal ortogonais). A recusa cross-mode de ADR-047 § Decisão (c) (`backlog: local + plans_dir: canonical`) **não aplica** em modo forge — identificador é público por construção (issue existe no remote), não há leak privado→público a evitar; combinação `paths.backlog: forge + paths.plans_dir: canonical` é válida.

## Editing conventions

- The plugin adapts to the consumer project's language at runtime (see `docs/philosophy.md` → "Convenção de idioma"). For **this** repo specifically the canonical default applies: documentation and skill/agent prose are in **Portuguese**, except `README.md` (governed by [ADR-051](docs/decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (b), follows discovery channel target audience: EN); mechanism stays in English — agent names, frontmatter keys, file paths, code, and `CLAUDE.md` itself (it's agent operating instructions, not user-facing prose). Don't translate cosmetically.
- Commit messages follow the consumer project's commit convention (see `docs/philosophy.md` → "Convenção de commits"). For **this** repo the git log shows a stable pattern of Conventional Commits in English — keep it.
- Skills end with an explicit `## O que NÃO fazer` section listing scope guards. Preserve that section when editing — it's load-bearing for tight skill focus. **Critério editorial:** lista apenas guardas que documentam anti-padrão não-óbvio. Itens vindos de incidentes ou de vieses sutis (modelo tende a autoinvocar, gatilho condicional facilmente esquecido, exceção localizada) são não-óbvios e devem permanecer.
- Don't introduce a build system, package manager, or test runner for this repo itself. The hooks are runnable Python scripts (`python3 ${CLAUDE_PLUGIN_ROOT}/hooks/<script>.py`); the rest is markdown. (Manifest/syntax invariant checks via CI lint are a distinct category — see [ADR-050](docs/decisions/ADR-050-componentes-plugin-consolidado.md) § Decisão (b).)
- **Instrumentação de progresso em skills multi-passo via Tasks**: ver [ADR-010](docs/decisions/ADR-010-instrumentacao-progresso-skills-multi-passo.md) — critério de aplicação, lifecycle conversation-scoped, relação com ADR-049 § Decisão (a).
- **Wiring automático do design-reviewer**: ver [ADR-053](docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (b) — quando dispara em `/triage` e `/new-adr`, override por inação, custo de tokens.
- **`disable-model-invocation` em SKILL.md**: critério mecânico cumulativo em [ADR-050](docs/decisions/ADR-050-componentes-plugin-consolidado.md) § Decisão (e) — blast radius local + pushes/PRs gateados por enum upstream + sem autoinvocação cross-turn → `false`; tabela retroativa às 9 skills no próprio ADR. Skill nova com `true` justifica explicitamente.
- **Adendo vs novo ADR para refinamento doutrinal**: critério mecânico em [ADR-034](docs/decisions/ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) — novo ADR quando ≥1 das 5 condições aplica (decisão estrutural sem ancestral, substitui ADR ancestral, codifica restrição externa, introduz categoria nova, ou sucessor parcial); adendo em ADR existente quando todas as 4 aplicam (decisão central intacta, sem nova categoria, sem restrição externa, caráter explicativo).
- **Hierarquia doutrinal**: 3 princípios fundamentais (Verdade, Excelência sem over-engineering, Navalha de Ockham) são raiz epistêmica do toolkit; YAGNI/flat/sem-defensividade-ornamental são consequência operacional derivada per [ADR-043](docs/decisions/ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) — substitui ADR-035 absorvendo seus 4 critérios (incidente, fronteira, contradição, ≥3 pattern) como § Ockham operacionalizado em decisões internas do plugin.
- **Redesign da camada doutrinal**: consolidar 45 ADRs em ~10-12 temáticos sob hierarquia invertida + codificar política de admissão going forward (filtro decisão reversível vs entendimento estabilizado) per [ADR-045](docs/decisions/ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) — sucessor parcial de ADR-043 que estende o trabalho da hierarquia invertida para o inventário, codificando a estrutura-alvo da camada doutrinal e o mecanismo de prevenção de re-acúmulo. Ondas B-X migram conteúdo per `docs/plans/redesign-camada-doutrinal-charter.md`.
- **Refinamento editorial das ondas de migração da redesign**: 3 modos editoriais canonical (exclusão + inclusão + preservação por constraint mecânico) per [ADR-052](docs/decisions/ADR-052-codificacao-3-modos-editoriais-refinamento-consolidacao.md) — sucessor parcial de ADR-045 promovendo o terceiro item da fronteira § Decisão linha 56 ("absorção em consolidado diferente do sketch original") de categoria não-codificada para categoria com sub-modos canonical com critério mecânico verificável. Aplicável às Ondas I-X de migração; documentado em § Origem do ADR consolidado da onda + charter § Atualização pós-execução. Modo (c) restrito a constraint mecânico puro (grep ID em § Decisão de ADR Aceito vigente); preservação por categoria distinta sem constraint cai em modo (a) EXCLUSÃO bullet 2.
- **Curadoria do free-read do design-reviewer**: codificada per [ADR-048](docs/decisions/ADR-048-free-read-design-reviewer-consolidado.md). Scan medium (título + Status + Data + § Decisão até próximo `## ` OU 8 linhas, cap 12) + always-include curated list (ADR-009/-034/-043) sempre lida integralmente paralelo a `philosophy.md`. Threshold N=15 + anotação `**ADRs candidatos:**` preservados. Cap nominal 5 ADRs na always-include; expansão futura via gatilho (≥3 anotações sistemáticas).
- **Brainstorm/exploração não-codificado como skill**: raw-chat com Claude cobre trabalho exploratório de ideias/abordagens; pipeline estruturado (`/draft-idea`, `/triage`, `/debug`, `/new-adr`) entra quando intenção cristaliza per [ADR-036](docs/decisions/ADR-036-brainstorm-intencionalmente-nao-codificado-em-skill.md). Aplicação inversa do ADR-035 (ausência dos 4 critérios é sinal forte para NÃO criar skill); reversível via gatilhos de revisão concretos no próprio ADR.
- **Modo runbook em planos de system-surgery**: campo opcional `**Modo:** runbook` no `## Contexto` do plano bypassa worktree + commit-per-bloco + reviewer per bloco + validação centralizada do `/run-plan` per [ADR-049](docs/decisions/ADR-049-execucao-run-plan-consolidado.md) § Decisão (d). Aplica-se a planos cuja semântica não é diff git (FS migration, system surgery, dotfiles sync, multi-repo edits, ops em `~/`). Tipicamente hand-written, não derivado de `/triage`; operador gerencia rollback fora da skill (snapshot/tarball/manual). Único valor aceito: `runbook`; ausência = fluxo canonical (default total).
- **Manutenção editorial periódica do BACKLOG**: skill `/curate-backlog` paralela a `/archive-plans` codificada em [ADR-057](docs/decisions/ADR-057-curate-backlog-manutencao-editorial-periodica.md). Fronteira `/next` (orientação de sessão, top 3) vs `/curate-backlog` (manutenção editorial periódica, arquivo inteiro, mutações cross-seção). 4 heurísticas detectivas (H1 gatilhos temporais — predicado mecânico; H2 redação stale + H3 mergeable items com anti-spam — heurísticas semânticas do agente runtime; H4 NOTES.md sinais — informacional refinado, sem ação direta no gate). Salvaguarda worktree-probe preserva ADR-049 § Decisão (a) mecanicamente — main-só → mutações diretas; ≥1 worktree adicional → defer via NOTES.md como signal queue. Override do critério N=3 (ADR-043 § Ockham operacionalizado #4) registrado em ADR-057 § Override com gatilho de revisão concreto (6 meses pós-shipping / ≤2 invocações OR ≥50% findings inúteis).
- **Heurística de completude de planos via campo `## Status`**: campo opcional no body do plano carregando `Pendente`/`Abortado` (estados que git/forge não captura per ADR-049 § Decisão (a)); `Em execução` e `Concluído` permanecem derivados de git/forge + ADR-022 cadeia. `/triage` step 4 (caminho-com-plano) cria o bloco logo após `# Plano — <Título>`; `/run-plan §3.4` remove no done via bloco extra unificado (BACKLOG mark + plan body em 1 commit, sequência atômica, revisor `code` cobre os 2 edits); `/next` passo 4.6 consome no bloco informativo "Planos em aberto" (não compete no enum top-3) per [ADR-060](docs/decisions/ADR-060-heuristica-completude-planos-via-status.md) — sucessor parcial de ADR-022 (cond 5 ADR-034) com cross-ref inline em ADR-022 § Decisão critério 3.

## AskUserQuestion mechanics

Concrete shape for the `AskUserQuestion` tool when used by skills (philosophy and choice criterion in `docs/philosophy.md` → "Convenção de pergunta ao operador"):

- **Header** (chip/tag): ≤ 12 chars. Examples: `Commit`, `Backlog`, `Publicar`, `Branch`.
- **Options**: 2-4 per question. `Other` is automatic — never list it explicitly. Each option carries a concrete trade-off in `description` (cost, maintenance, virtue delivered); description-obvious like "choose A" signals a cosmetic enum.
- **Bifurcação discreta presente → enum, mesmo com Other comum** (ADR-006). Quando há ≥1 resposta comum **discreta** identificável, prefira enum — o `Other` automático cobre as livres com 1 toque a menos no caminho discreto. Prosa só é o modo certo quando **todas** as respostas comuns são livres (descrição de bug, justificativa de escopo, exemplo de dado real).
- **Multiple related questions** in a single call: up to 4 (`questions` array).
- **Unificação preferida sobre sequência.** Quando ≥2 perguntas relacionadas no mesmo passo são enum-áveis, **agrupar numa única chamada** em vez de sequenciar — fragmentação tira foco do operador.
- **`multiSelect: true`** when the choices are not mutually exclusive (e.g., picking gitignored files to replicate into a worktree).
- **Recommended option**: place first and append "(Recommended)" to the label.
- **`(Recommended)` só quando o default é estatisticamente estável.** Marcar apenas quando uma resposta é dominante na maioria das invocações da skill. Quando o "recomendado" depende de contexto runtime (modo, estado, decisão anterior), o SKILL deve **construir opções dinamicamente** em vez de fixar `(Recommended)` na prosa — ex.: `/run-plan` §3.7 escolhe Recommended por modo `plans_dir` × presença do campo `**Branch:**` no plano. Recommended sem default real é viés enganoso.

## Reviewer/skill report idioma

Reviewer ou skill que produz relatório/texto-de-saída espelha o idioma do projeto consumidor (default canonical PT-BR). Esta seção operacionaliza, para reviewers shippados e `/triage`, a regra-mãe em `docs/philosophy.md` → "Convenção de idioma"; [ADR-051](docs/decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (a) cobre artefatos informativos (changelog, tag messages, commits) fora deste escopo. Aplica-se aos 5 reviewers (`code-reviewer`, `qa-reviewer`, `security-reviewer`, `doc-reviewer`, `design-reviewer`) e ao texto produzido por `/triage`. Cada artefato preserva sua estrutura interna traduzindo-a junto.

## Plugin component naming and hook auto-gating

Skills and hooks stack-specific coexist with generic components in the same plugin. The name carries the contract:

| Type | Generic | Stack-specific |
|------|---------|----------------|
| Hook (script) | `<purpose>.py\|.sh` (e.g., `block_env.py`) | `<purpose>_<stack>.py\|.sh` (e.g., `run_pytest_python.py`) |
| Skill (frontmatter `name`) | `<verb>-<artifact>` (e.g., `new-adr`, `gen-tests`) **or** `<verb>` when the artifact emerges from the skill's decision (e.g., `triage`) | n/a — generators use internal stack sub-blocks (per [ADR-050](docs/decisions/ADR-050-componentes-plugin-consolidado.md) § Decisão (a)) |
| Agent (frontmatter `name`) | `<role>` (e.g., `code-reviewer`, `qa-reviewer`, `security-reviewer`, `doc-reviewer`, `design-reviewer`) | `<role>-<stack>` (only if principles change with the stack) |

Skill whose output is fixed (always produces an ADR, always executes a plan) carries `<verb>-<artifact>` — the name promises the output. Skill whose output is decided per invocation among multiple options (e.g., `/triage` decides among backlog line, plan, ADR, or domain update) carries only `<verb>` — a fixed suffix would lie about what comes out.

**Hook auto-gating triplo** (a hook fires in every project where the plugin is installed, so the gating is non-negotiable for safe shipping):

1. **File extension** — `if not file_path.endswith(".py"): exit 0` filters most cases at zero cost.
2. **Stack marker** — walk ancestors looking for `pyproject.toml` (Python), `build.gradle*`/`pom.xml` (JVM), etc. No marker → `exit 0`.
3. **Toolchain** — only run the tool (`uv run pytest`, `gradle test`) with reasonable fallback; if the toolchain isn't installed, `exit 0`.

This makes it safe to ship `run_pytest_python.py` alongside `run_gradle_test_java.sh` in the same plugin: each hook is silent in projects outside its stack, with no flags or env vars to disable.

## Cutucada de descoberta

Cutucada proativa emitida ao final do reporte pelas 6 skills que reativamente consomem o Resolution protocol step 3 — `/triage`, `/run-plan`, `/new-adr`, `/next`, `/draft-idea`, `/curate-backlog` — surfando `/init-config`. Cobre dois gaps: `CLAUDE.md` ausente e `CLAUDE.md` presente sem o bloco `<!-- pragmatic-toolkit:config -->`. Defined by [ADR-046](docs/decisions/ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) — gating tri-state (marker ausente → string-A; `CLAUDE.md` ausente → string-B; presente com marker → silêncio). The other 3 skills (`/debug`, `/release`, `/gen-tests`) don't traverse step 3 in their flow — they don't emit the hint. `/triage` declara `plans_dir` como `informational` (path requerido apenas no caminho-com-plano, 1 de 4 saídas) mas emite a cutucada por designação editorial — caminho-com-plano traversa step 3 mid-flow.

Mechanics (tri-state gating, dedup conversation-scoped por string, 2 strings canonical literais) live in `docs/procedures/cutucada-descoberta.md` — skills read this procedure at runtime. **Estado do gatilho ADR-046 linha 219 (helper compartilhado):** 6ª skill emissora (`/curate-backlog`) materializa o limiar de 12 sites (6 × 2 strings). Decisão registrada em ADR-057 § Cutucada e gatilho ADR-046: reapply editorial inheritance manual; defer helper compartilhado até **7ª skill emissora** (14 sites, ultrapassa o limiar de 12 onde ADR-046 prescreve avaliar). Reabrir avaliação então.

**Editorial inheritance.** New SKILL que traversa Resolution protocol step 3 (qualquer role como `required` ou consumido mid-flow no caminho-com-plano-style) adota a convenção manualmente — author adds the line-ref to the procedure at the end of the final reporting step, following the existing emitting skills as template. Checklist for human reviewer or `code-reviewer` on PRs introducing such SKILLs. The complementary `/init-config` skill is the proactive setup path.

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
- `local` (string literal) → local-gitignored mode. Skill creates/reads under `.claude/local/<role>/`, artifact is not committed, commit/PR/branch metadata do not reference it (see "Local mode" section above; full rationale in [ADR-047](docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md)). Applies to `decisions_dir`, `backlog`, `plans_dir`; `version_files`/`changelog` reject this value.
- `forge` (string literal) → role sourced from open issues without assignee in the current repo via `gh`/`glab` (per [ADR-058](docs/decisions/ADR-058-role-backlog-aceitar-forge.md)); remote mutations (close/create issue) gated by `AskUserQuestion` cutucada because blast radius is immediate and visible. Canonical item identifier in internal messages: `#<número>: <título>`. Applies to `backlog` only in v1; other roles reject this value. Coexists with `local` orthogonally per-role.
- Unknown keys are ignored (forward-compat for releases that add new roles).
- Keys live under `paths.<role>` (top-level `test_command` as exception); reference list in "Roles and canonical defaults" above.
- The HTML marker `<!-- pragmatic-toolkit:config -->` is what the skill looks for — without it, the YAML block is not interpreted even if under the `## Pragmatic Toolkit` heading.

## Local install for iteration

```
/plugin install /path/to/pragmatic-dev-toolkit --scope project
```

Then smoke-test in a consumer project per the checklist in `docs/install.md` (each skill appears, `.env` edits are blocked, pytest hook fires on `.py` edits inside a `pyproject.toml` ancestor, reviewers flag canonical violations).
