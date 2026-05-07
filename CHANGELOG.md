# Changelog

All notable changes to this plugin are documented here. Format inspired by [Keep a Changelog](https://keepachangelog.com/).

## [1.23.0] - 2026-05-07

### Added
- Conversions of prose-with-bifurcation to `AskUserQuestion` enums in 5 SKILLs (ADR-006, #37): `/run-plan` §3.2 (`Validação`: `Validei` Recommended / `Falhou — descrever`), §3.3 (`Docs`: `Consistente` / `Listar arquivos a atualizar`), §3.7 (`Publicar` absorbs `Renomear branch antes` in local mode); `/debug` §1 unified into a single call with 3 enum questions (`Onde`/`Reprod`/`Mudou`) + 1-2 prose follow-ups; `/release` §1b ambiguous (`patch`/`minor`/`major`); `/gen-tests-python` §6 fixture/conftest (`No próprio arquivo` Recommended / `Em conftest.py`).
- ADR-006 (Accepted): preference for enum when there is a discrete bifurcation in the operator question — criterion "all-Other → prose" replaces "majority-Other → prose". `philosophy.md` and `CLAUDE.md` "AskUserQuestion mechanics" refined (discrete bifurcation → enum even with common Other; unification preferred over sequencing; `(Recommended)` only with statistically stable default, otherwise options built dynamically).

### Changed
- `/triage` §2: unification of enum-able gaps becomes a preference (≥2 → group into a single call) instead of a permission.

### Fixed
- `(Recommended)` removed from `/run-plan` §3.3: trigger heuristic does not favor a dominant path when it fires; `Consistente` and `Listar` are equally likely.

### Notes
- 7 conversions + 1 cross-cutting fix in plan `forma-perguntas-enum-first` across 9 granular commits; squashed into main as PR #37.

## [1.22.0] - 2026-05-07

### Added
- Forge auto-detect in `/run-plan` (step 7) and `/release` (final phrase): parsing `git remote get-url origin` maps `github.com → gh` / `^gitlab\. → glab` → `Forge` gate before running `gh pr create --fill` / `glab mr create --fill` / `gh release create --generate-notes` / `glab release create --notes <body>`; falls back to a textual hint when the CLI is missing or the host is unknown (#35).
- Local-gitignored mode in the path contract (ADR-005): `paths.<role>: local` for `decisions_dir`, `backlog`, `plans_dir` activates an artifact under `.claude/local/<role>/`, with a no-reference rule (ADR / plan slug / backlog line do not appear in commit / PR / branch metadata). Initialization mechanics: `mkdir -p` + `git check-ignore` probe + `Gitignore` gate when the entry is missing. `/release` rejects local mode for `version_files`/`changelog` (#36).
- Optional `## Implementação` section in the `/new-adr` template — a list of commits that materialized the decision (format `[\`hash\`](url) subject`); applied manually in ADR-005.

### Changed
- `disable-model-invocation: true → false` in `/release`, `/run-plan` and `/new-adr` — model auto-invocation enabled; blast radius is low (release stays local until manual push; run-plan operates in an isolated worktree; new-adr only creates markdown).
- `/triage` step 2: ADR-worthy heuristic expanded — bullet "Persistência" (potential trigger) replaced by "Decisão estrutural duradoura?" with 3 explicit signals (persistence/schema; reversal of a decision recorded in `decisions_dir`; long-lived external constraint).

### Notes
- ADR-005 introduces local mode as a parallel track to the 3 default behaviors of ADR-003 (cross-ref applied in § Limitações).
- Captured in the backlog: initial role-configuration wizard; `## Implementação` convention in ADRs (retrofit of ADRs 001-004 as follow-up).

## [1.21.0] - 2026-05-07

### Added
- Skill `/debug` step 6 emits a paste-ready `/triage` invocation snippet — handoff in short sessions (#34).
- `templates/plan.md` — canonical plan skeleton consumed by `/triage` and `/run-plan` (ADR-001, #30).
- ADRs 001 (templates), 002 (zero-gate), 003 (frontmatter roles), 004 (state in git/forge) recording the structural decisions of the post-v1.20.0 architectural roadmap.

### Changed
- `BACKLOG.md` schema: `## Em andamento` section removed. State of work in progress lives in git/forge (branches/PRs); `## Próximos` preserves curation; `## Concluídos` preserves the editorial registry. ADR-004 (#33).
- `/run-plan`: 4 nudge enums in the pre-loop phase eliminated — detected warnings are classified into tracks (Notice/Backlog/Validation) and materialized via automatic capture. ADR-002 (#31).
- `/run-plan` step 3.4: returns to **moving** the line from `## Próximos` to `## Concluídos` (with a fallback "only add" when the line is not in Próximos).
- SKILLs: declarative frontmatter `roles.required` / `roles.informational` in all 8 skills; `CLAUDE.md` "Resolution protocol" absorbs the auto-dispatch rule and the 3 default-behavior tracks. ADR-003 (#32).
- `philosophy.md` ↔ `CLAUDE.md` boundary refactored: roles table consolidated in `CLAUDE.md` (single source of truth); residual mechanics (naming, AskUserQuestion, ubiquitous language) migrated to consumers; `code-reviewer` gains conditional applicability in infra/settings subsections (#29).
- Editorial tightening: docs sanity check as prose (instead of cosmetic enum); disciplined trim of `## O que NÃO fazer` in skills + editorial criterion in `CLAUDE.md`; `disable-model-invocation: true` in `/release` and `/run-plan`; single-reviewer as the normal case; `/next` proposes commit of automatic movements (#28).

### Fixed
- `/run-plan` 3.4 under ADR-004: gap where a pre-existing line in `## Próximos` got duplicated in Concluídos post-merge — fix returns to moving.

### Removed
- Skill `/heal-backlog` — obsolete under ADR-004 (state-tracking left the markdown, no merge artifact to heal).
- Action `validate-backlog` (`.github/workflows/validate-backlog.yml` + `.github/scripts/validate_backlog.py`) — obsolete under ADR-004.

### Notes
- Post-v1.20.0 architectural roadmap closed: 6 structural PRs (Batch 1/2/3/E3/C1/B2 + D2) + 2 polishing commits (handoff snippet, fix 3.4) + 4 ADRs established.
- Defensive mechanisms against merge artifact in `BACKLOG.md`: 5 → 0 (structural problem removed by ADR-004).
- Validation pendings recorded in the corresponding plans — resolved via direct post-merge inspection or deferred to a subsequent skill invocation.

## [1.20.0] - 2026-05-06

### Added
- Generic `doc-reviewer` agent for drift detection between code and docs (`CLAUDE.md`, ADRs, `docs/philosophy.md`, skills/agents prose) (#26).

### Changed
- `/run-plan` and `/release` skills made forge-agnostic — push, PR opening and GitHub Release are handed off to the operator; skills deliver a ready local state (#27).

### Notes
- `docs/philosophy.md`: convention clarified — `## O que NÃO fazer` is specific to skills.
- Plans consolidated in `docs/plans/` for the forge-agnostic refactors and for the generic `doc-reviewer`.
- BACKLOG: forge-agnostic decoupling item recorded.

## [1.19.0] - 2026-05-06

### Added
- `/release` 4.5.Aplicar: HEAD-branch verification before commit, with proactive recovery (stash uncommitted + checkout to the branch from precondition 2) when HEAD is detached or on the wrong ref — guards against HEAD changing due to a concurrent session in another terminal (#24).
- `/release` 4.5.Aplicar: upstream auto-sync (`git fetch` + `git pull --ff-only`) after the recovery checkout and before the (a)-(e) sequence — avoids tagging a stale SHA in concurrent windows where remote merge/push happened during release prep (#25).
- Action `validate-backlog`: detects merge artifacts in `BACKLOG.md` (line duplicated across Em andamento + Concluídos) on push to `main` and opens an issue with label `backlog-merge-artifact` (with dedup) (#23, #24).
- Skill `/heal-backlog`: detects the duplicate pattern in `BACKLOG.md` and proposes a healing edit via Apply/Cancel gate; supports manual insertion of a "missing line" via operator prose (#23).

## [1.18.0] - 2026-05-06

### Changed
- `docs/philosophy.md` refactored to principles only — mechanics migrated to the actual consumers (`CLAUDE.md`, skills, README); 4170 → 1792 words; 18 → 8 sections (#22).
- Skills compacted and `## O que NÃO fazer` trimmed to genuine scope guards — aggregate of 7 skills from 11070 → 7200 words; `/run-plan` 18 → 7 items, `/triage` 13 → 4, `/release` 10 → 5 (#21).
- `CLAUDE.md` cut paraphrases of `docs/philosophy.md`/skills/agents — 1407 → 740 words (#20).
- Frontmatter `description` of the 7 skills trimmed to an invocation gateway — −34% chars on average.

### Notes
- `.worktreeinclude` added listing `.claude/` for new `/run-plan` worktrees.
- `BACKLOG.md` healed after the merge artifact from #20+#21 fan-out (3rd occurrence; captured in `## Próximos` for a subsequent fix).

## [1.17.0] - 2026-05-05

### Added
- `/run-plan`: detect `BACKLOG.md` divergence and auto-rebase before publish (#19).
- `/run-plan`: auto-capture pre-loop blockers before stopping (#17).
- `/run-plan`: suggest push and PR opening after done (#16).
- `/run-plan`: classify auto-captures as validation or backlog at detection time (#15).
- `/next`: new session-orientation skill; `/triage` delegates to it when invoked without arguments.

### Fixed
- `/triage`: deterministic post-commit push via atomic shell call (#18).
- Eliminate `BACKLOG.md` merge artifact via push-after-triage (#14).
- `/triage`: guard against `BACKLOG.md` in plan's `## Arquivos a alterar` (#12).
- `/run-plan`: restrict docs gate skip to user-facing `.md` patterns (#11).

### Changed
- `/run-plan`: simplifies the documentation sanity check at the final gate (#10).
- `/release`: collapses `version_files`, `changelog` and commit/tag gates into a single review (#9).

### Notes
- Plans in `docs/plans/` covering each feat/fix/refactor of this release.
- `BACKLOG.md`: recurring captures (merge conflict, Em andamento transition, reliability gap of `/triage` push); executed items moved to Concluídos.
- `docs/philosophy.md`: release cadence convention recorded.
- `README.md` + backlog: `/next` skill listed.

## [1.16.0] - 2026-05-05

### Added
- `/run-plan` gains **automatic capture of unforeseen items** (step 4.5, replaces "backlog harvest"): six prescribed triggers — four during execution (worked-around failure, out-of-scope finding, hook blocking, missing surface) and two during manual validation (plan divergence, collateral bug). Unified policy: agent informs the operator at each detection and materializes the lines as an extra block before `done` — without an `AskUserQuestion` confirmation. Override window in prose between the notice and materialization. An explicit operator signal continues to count as input on the same axis.

### Changed
- `docs/philosophy.md` gains a `## Consolidação do backlog` section extracted from `/triage` step 5. Single mechanic (re-read + flagging duplicates/obsolescence + single conditional question when there are flags) consumed by `/triage` step 5 and `/run-plan` step 4.5 — DRY between the two skills.
- `docs/philosophy.md` → "Ciclo de vida do backlog": reference to "backlog harvest" replaced by "automatic capture of unforeseen items"; "capture of new deferred items" becomes "capture of unforeseen items detected by the agent".

### Notes
- `skills/triage/SKILL.md`: step 5 ("Consolidação do backlog") shortened to reference `philosophy.md` instead of duplicating the rule inline.
- `docs/plans/captura-automatica-imprevistos.md`: plan that motivated the release. 4 blocks (philosophy, triage SKILL, run-plan SKILL, `CLAUDE.md` guard) with `code` reviewer (and `qa` where applicable). Earned a `## Pendências de validação` section listing the 13 scenarios not yet exercised in a fixture project and the `qa-reviewer` coverage skipped due to usage limit — validation pendings stay in the plan, not in the backlog.

## [1.15.1] - 2026-05-05

### Changed
- `/debug` step 5 gains a conditional **Hipóteses testadas** field — ledger format `H<n> (<status>): <hypothesis>. <evidence>` (status `confirmada` / `refutada` / `inconclusiva`), emitted only when ≥2 hypotheses passed through step 4. Single hypothesis confirmed → field omitted (mirrors "empty list → silent skip" of `/run-plan` 4.5). Position: between *Sintoma* and *Causa-raiz* — operator sees the path, not just the destination. Auditable anti-confirmation-bias + input for `/triage` when the correction path is a larger change.
- `/debug` gains an explicit step 6 ("Reportar e devolver controle") mirroring the closing of `/triage` and `/release` — short synthesis + next-step suggestion in one phrase (revert / local patch / `/triage <intent-do-fix>`). Handoff was previously diluted between step 5 and the `## O que NÃO fazer` section.
- `/debug` step 1 cites "Convenção de pergunta ao operador" — precision questions are free prose, not enum. Editorial standardization aligned with the other skills.
- `/debug` step 5 *Caminhos de correção* names `/triage <intent-do-fix>` as the structured handoff: the diagnosis (including *Hipóteses testadas* when present) becomes a natural input for the plan's `## Contexto`.

### Notes
- `docs/install.md` validation item 6 mentions the optional *hipóteses testadas* field in the structured diagnosis.
- `docs/plans/debug-trilha-hipoteses-e-handoff.md`: plan that motivated the release. Single block with 4 coordinated edits in `skills/debug/SKILL.md` plus a sanity tweak in `docs/install.md`, `code` reviewer.
- Backlog state transitions (`Próximos → Em andamento → Concluídos`) become **automatic** — `/triage` writes directly to `## Em andamento` when the path includes a plan; `/run-plan` applies both transitions without prompting, only informing the operator. Reverts the v1.13 "toolkit nudges, does not decide" decision — exact-text matching already eliminates the risk of moving the wrong line that had motivated the nudge.

## [1.15.0] - 2026-05-05

### Changed
- `/release` steps 4 (commit) and 5 (tag) merged into a single step "Aplicar commit + tag (gate único)". Commit and tag messages are mechanical derivatives of the bump confirmed in step 1 — confirming separately is ceremony. Renumbers "Reportar" step 6 → 5.
- `/run-plan` step 4.5 (Backlog harvest): question becomes conditional. Skill keeps a list of items emerged during execution via explicit operator signal ("isso fica pra depois") or out-of-scope reviewer finding. Empty list → silent skip; non-empty list → shows the items in prose.
- `/triage` step 5 (Backlog review): question becomes conditional. Re-read + flagging duplicates/obsolescence always run. No flags → silent skip (lines added in step 4 do not need re-confirmation); with flags → enum fires showing the synthesis.

### Notes
- `docs/philosophy.md`: new paragraph "Não perguntar por valor único derivado" in "Convenção de pergunta ao operador". Principle: when the value is 100% derived from a decision already confirmed upstream, skip the confirm; the "late abort" window comes from making things visible before applying (`git status` before commit, diff before write), not from extra ceremony. Skills that apply N derived values consolidate into a single gate.
- `docs/plans/reduce-ceremonial-prompts.md`: plan that motivated the release. Built via dogfooding — `/triage` produced the plan, `/run-plan` executed the 4 blocks with a `code` reviewer in each one and micro-commits. First release that dogfoods the `/release` single gate itself.

## [1.14.0] - 2026-05-04

### Changed
- `/new-feature` renamed to `/triage`. Breaking change (slash command visible to the operator, no compat alias — flat philosophy). The old name suggested a scope restricted to new features; the real one is triage of the operator's intent (feature, fix coming out of `/debug`, refactor with bifurcation, point change that touches an invariant). Pairs with `/debug` on the "think before acting" axis (diagnose ↔ triage). Frontmatter `description` rewritten for the broader scope. `git mv skills/new-feature skills/triage` preserves history.

### Notes
- `docs/philosophy.md`: naming convention relaxed — skills accept `<verb>` (without artifact suffix) when the output emerges from the skill's decision (the `triage` case); skills whose artifact is fixed (`new-adr`) keep `<verb>-<artifact>`. Table gains an explanatory note below.
- Mechanical references updated in `CLAUDE.md`, `README.md`, `docs/install.md`, `skills/run-plan/SKILL.md`, `skills/debug/SKILL.md`, `skills/release/SKILL.md`. Historical `CHANGELOG.md` and `docs/plans/*.md` are not touched (record of what existed at the time of each release).
- `CLAUDE.md`: `<!-- pragmatic-toolkit:config -->` block declares `version_files: [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"]` and `test_command: null` (repo without a suite — `/run-plan` falls back to the plan's `## Verificação manual`).
- `docs/plans/rename-new-feature-to-triage.md`: plan that motivated the release. First release that dogfoods `/triage` (the next invocation will be under the new name).

## [1.13.0] - 2026-05-04

### Added
- `BACKLOG.md`: lifecycle formalized — `## Próximos`, `## Em andamento` and `## Concluídos` become real states with nudges at natural transition points. `/new-feature` decides the initial section when the feature generates a plan (enum `Próximos` (recommended) / `Em andamento`); without a plan, it goes straight to `## Próximos`. `/run-plan` nudges `Próximos → Em andamento` before the first block and `Em andamento → Concluídos` at the final gate, before the harvest. The `**Linha do backlog:** <text>` annotation in the plan's `## Contexto` is the matching mechanism between alignment and execution; absence (plan without the field, `backlog` role "não temos", line not located) is a silent skip — additive change, old plans without the annotation continue running with no behavior change.

### Notes
- `docs/philosophy.md`: new "Ciclo de vida do backlog" section between "Cobertura de teste em planos" and "Linguagem ubíqua na implementação", with subsections "Anotação de matching" and "Quando o ciclo silencia".
- `skills/new-feature/SKILL.md`: step 4 sub-bullet `backlog` distinguishes path-with-plan (section enum) vs path-without-plan (default `Próximos`); sub-bullet `plans_dir` records `**Linha do backlog:**` in `## Contexto` when applicable; `## O que NÃO fazer` gains two guards.
- `skills/run-plan/SKILL.md`: step 3 captures the reference before the first block and nudges the initial transition; step 4.4 new "Transição final do backlog" before the harvest (renumberings 4.4→4.5, 4.5→4.6); `## O que NÃO fazer` gains three guards (no heuristic matching, no silencing of the final transition, no inversion of order 4.4↔4.5).
- `docs/plans/v1.13-transicao-estado-backlog.md`: plan that motivated the release.

## [1.12.1] - 2026-05-04

### Notes
- `CLAUDE.md`, `docs/philosophy.md`, `skills/run-plan/SKILL.md`: description of the `qa-reviewer`/`security-reviewer` reviewers aligned with reality — agents shipped by the plugin with project-level override via `.claude/agents/<name>.md` (Claude Code convention, project-level wins on name collision). Phrases correct the drift that described the reviewers as "project-level only" and contradicted `CLAUDE.md:16`, which already listed the three reviewers as plugin agents.
- `README.md`: added a `/release` line in the "O que vem" table. The skill arrived in v1.11.0; the table had fallen behind.
- `docs/plans/corrigir-docs-reviewers-e-release-no-readme.md`: plan that motivated the release.

## [1.12.0] - 2026-05-04

### Changed
- `/new-feature`: `backlog` role reclassified from required to informational. A project without `BACKLOG.md` at the canonical path and without a declaration in the `<!-- pragmatic-toolkit:config -->` block stops getting a gap report and starts using the skill normally — the blocking precondition now mentions only `plans_dir` (the only non-fungible output of the skill). The enum creation offer (header `Backlog`, options `Criar em BACKLOG.md` / `Não usamos esse papel`) fires only at step 4 when a line is about to be recorded; mirrors the pattern already used by `ubiquitous_language`/`design_notes`. The second option records `paths.backlog: null` in the config block — role disabled for future invocations. Out-of-scope items captured at step 2 are reported to the operator at step 6 under "Itens não registrados (papel backlog desativado):" when the role resolves to "não temos", without further editorialization.

### Notes
- `docs/philosophy.md`: `backlog` moved from the Required list to the Informational list; short note explaining the `/new-feature` behavior when the role resolves to "não temos".
- `docs/install.md`: gap-report list in the `<!-- pragmatic-toolkit:config -->` block example now mentions only `plans_dir` for `/new-feature`/`/run-plan` and `decisions_dir` for `/new-adr`.
- `docs/plans/v1.12-backlog-informacional-new-feature.md`: plan that motivated the release.

## [1.11.0] - 2026-05-04

### Added
- New skill `/release`: coordinated version bump in `version_files`, changelog entry in `changelog`, unified commit and local annotated tag. Mechanizes release from the Conventional Commits log since the last tag — bump inference (≥70% CC), enum proposal, bifurcation for ambiguous history / first release / explicit argument (`/release minor|patch|major|X.Y.Z`). Preconditions: clean working tree (blocks), default branch (nudges). Tag-format detection at three levels (policy → observed pattern ≥70% → SemVer canonical `vX.Y.Z`). The skill **does not** push — release is local; publication is a deliberate decision (`git push --follow-tags`).

### Changed
- `/release`: `code-reviewer` feedback applied to the initial draft (redundant justifications removed; per-file path of the diff confirmation restored with batch as an optimization; alternative `git push && git push origin <tag>` added to the handoff).

### Notes
- `docs/philosophy.md`: new roles `version_files` (opt-in, no canonical default) and `changelog` (canonical `CHANGELOG.md`) in the role contract.
- `CLAUDE.md`: description of `/release` and dogfood note — the repo itself starts using `/release` to bump versions from v1.11.0 onward.
- `docs/install.md`: smoke test for `/release` (scenario 10) and updated role enumeration.
- `docs/plans/v1.11-skill-release-tagueamento.md`: plan that motivated the release.

## [1.10.0] - 2026-05-04

### Added
- `docs/philosophy.md`: new section **"Convenção de pergunta ao operador"** defines the two complementary input-collection modes — `AskUserQuestion` (discrete choices) and free prose (explanation/justification) — with a mechanical criterion to choose between them.
- Skills migrated to `AskUserQuestion` at enum-natural points: tri-state role resolution and memoization offer (philosophy + all skills); architectural bifurcation (`/new-feature` step 2); `/new-feature` steps 5 (backlog review), 6 (commit) and creation proposal of `domain.md`/`design.md`; `/new-adr` step 2 (atypical/mixed format); `/run-plan` precondition 2 (dirty alignment), step 1.2 (`.worktreeinclude` multiSelect + cross-trigger for credentials), step 2 (scope sanity), step 4.3 (docs sanity), step 4.4 (backlog harvest).
- `CLAUDE.md`: pointer to the new convention to preserve the mode of each touchpoint when editing skills.



### Added
- `/new-feature`: new **step 5 "Revisão do backlog"** between step 4 (artifact production) and the commit step (renumbered to step 6). Conditional gate — fires only when step 4 modified the `backlog` role's file (line for the current feature, out-of-scope lines captured at step 2, or both); a path that did not touch the backlog (pure update of `domain.md`/`design.md`, ADR delegated without an accompanying backlog line, `backlog` role resolved to "não temos") skips silently. When it fires: re-reads the backlog file after step 4 edits, flags duplicates between newly-added lines (including out-of-scope items from step 2) and pre-existing lines across the three sections, flags conservative obsolescence (clear text overlap, not vague similarity), shows the operator the current state of `## Próximos` (with `## Em andamento`/`## Concluídos` only if a flag touches those sections) and asks once whether anything needs to be consolidated, reordered or removed before the commit. Minimum question version in the frequent case (no flags + one line added): "Backlog atualizado com `<linha>`. Ok?". Operator-approved edits go into the same unified commit proposed at step 6. Two new entries in `## O que NÃO fazer` codify: do not skip the gate when step 4 modified the backlog, and do not consolidate/remove/reorder lines without explicit operator confirmation.

### Notes
- Additive change. Closes the symmetry of the **end-of-flow quality gates** axis: `/run-plan` 4.4 (Backlog harvest, 1.7.0) captures **new** items emerged during execution; `/new-feature` 5 validates items **just-recorded** during alignment. Full sequence on the axis: 1.4 (commit of artifacts), 1.5 (git gate in `/run-plan`), 1.6 (documentation sanity check), 1.7 (backlog harvest + out-of-scope capture), 1.8 (enumerated scenarios in manual validation), 1.9 (backlog review in `/new-feature`). The heuristic acts **starting from** the next invocation of the skill.

## [1.8.0] - 2026-05-03

### Added
- `/run-plan` step 1.2: new **manual-validation cross-trigger**, independent of the prior state of `.worktreeinclude`. When the current plan has `## Verificação manual` (semantic matching) AND the repo root has typical credential/local-config gitignored files (`.env`, `*.local.yaml`, `*.local.yml`, `secrets.*`) **not covered** by the applied `.worktreeinclude`, the skill nudges the operator before the baseline: *"Plano tem `## Verificação manual` e `<credencial>` não está replicada na worktree. Validação manual provavelmente vai precisar do serviço real. Replicar agora? (s/n)"*. The 3 real-world cases (`.worktreeinclude` absent / present but missing the credential / empty because the operator said "I don't need it" before) become instances of the same clause — the through-line is "credential needed for manual validation is not replicated", not prior state. New entry in `## O que NÃO fazer` codifies that the nudge **cannot be silenced** by an old "I don't need it" answer when context has changed (current plan requires the real service). Closes the gap of "worktree comes up without the needed credential and manual validation breaks on the first try".
- `/new-feature` step 2: existing gap *"Validação manual necessária?"* gains a **conditional sub-bullet** (not a top-level item — heuristic refinement > list expansion, aligned with YAGNI). When the gap's "yes" comes from a **non-deterministic surface** (parsing, string matching, or LLM agent behavior), require before the plan: (a) **shape of the real data** — ask for 1-2 concrete examples of the production format (separators, prefixes, inconsistent capitalization, internal IDs that must not leak); (b) **enumerated scenarios** — `## Verificação manual` must list concrete steps that exercise those shapes, not generic guidance like "validate via real interface". Sub-bullet **does not fire** when the gap's first question resolved to "no" (pure refactor, doc-only). Closes the gap of "matching against synthetic data passes, real data does not" and "prompt leaks an internal ID found by luck".

### Notes
- Additive change. Closes the quartet of consecutive releases on the **manual-validation gate** axis: 1.5 (git gate of alignment artifacts), 1.6 (documentation sanity check), 1.7 (backlog harvest), 1.8 (enumerated scenarios + replicated credentials). Two real bugs motivated 1.8 (matching failed in production format; LLM agent leaked an internal ID) — both passed the automatic reviewers and were caught only by manual validation after the operator improvised scenarios by luck. Deliberate decisions to **not** propose: a new `prompt-reviewer` agent (one session does not justify a role — YAGNI), a `## Cenários do agente` section in the plan template (would set a precedent for one section per feature type), changing the `qa-reviewer` mandate (reviewer acts on the diff, does not know "real data"; defense stays upstream in `/new-feature`). The heuristic acts **starting from** the next invocation of the skills.

## [1.7.0] - 2026-05-03

### Added
- `/new-feature` step 2 (gap clarification): new directive **"Itens fora de escopo emergidos na conversa"** instructs the skill to keep attention for things the operator mentions that do not belong to the current feature scope (adjacent TODO, revealed tech-debt, minor bug spotted, non-essential improvement). Captured items are proposed as separate lines in `## Próximos` of the backlog, distinct from the main artifact. The operator can discard with "deixa pra lá" — capture is a suggestion, not an imposition. Step 4 (production) clarifies that the backlog gains lines independent of the main artifact choice: a feature with plan/ADR/domain update also gets out-of-scope lines in `## Próximos`.
- `/run-plan`: new **step 4.4 "Backlog harvest"** between the documentation sanity check and declaring done. Asks the operator directly whether anything emerged during execution that should become a separate backlog item (adjacent TODO, tech-debt revealed by reading, minor bug in passing, non-essential improvement). Listed items are treated as an **extra block** (update `backlog` → `code` reviewer → micro-commit) before done. Answer "nada" closes the gate. Scope creep already absorbed by the plan **does not** enter here — harvest is for deliberate deferral. Two new entries in `## O que NÃO fazer` codify: do not skip the harvest (always ask), and do not capture items already absorbed by the current plan.

### Notes
- Additive change. Symmetrically complements previous bumps: 1.4.0 (commit of alignment artifacts in `/new-feature`), 1.5.0 (git gate in `/run-plan`), 1.6.0 (documentation sanity check). Closes the **silent loss of adjacent items** gap that emerges during the flow. The added ceremony is one question at the end of `/run-plan` ("nada" as a valid answer) and passive attention during `/new-feature`'s gap analysis — negligible cost compared to the loss avoided. The heuristic acts **starting from** the next invocation of the skills.

## [1.6.0] - 2026-05-03

### Added
- `/run-plan`: new **step 4.3 "Sanity check de documentação"** at the final gate, between `## Verificação manual` confirmation and declaring done. Validates consistency of user-facing `.md` docs (README, install, CHANGELOG, other `.md`) with what was implemented. Tri-state heuristic: (i) **silent skip** when the plan already listed `.md` in `## Arquivos a alterar` and the aggregated diff touched them — gate fulfilled by the plan; (ii) **silent skip** in pure refactor / internal-only — signaled by the absence of `## Verificação manual` AND absence of any user-facing surface mention in `## Resumo da mudança`; (iii) otherwise, **nudge** (don't block) with a direct question to the operator. Updates raised by the operator are treated as an **extra block** (implement → `test_command` → `code` reviewer → micro-commit) before declaring done. New entry in `## O que NÃO fazer` forbids skipping the check outside the two prescribed skip conditions.

### Notes
- Additive change. A plan that naturally does not touch user-facing surface (refactor, doc-only, internal cleanup) still declares done without an extra question — no ceremony where it clearly does not apply. The heuristic acts **starting from** the next `/run-plan` invocation.

## [1.5.0] - 2026-05-03

### Added
- `/run-plan`: new **precondition 2** with a two-layer check via `git status --porcelain` over the git state of alignment artifacts. **Blocks** when the plan itself (`<plans_dir>/<slug>.md`) is modified or untracked — broken-by-construction, since the worktree branched from HEAD would not see the plan it should execute; the message points to the explicit commit (and references step 5 of `/new-feature`). **Nudges** (does not block) when alignment roles (`backlog`, `ubiquitous_language`, `design_notes`, files under `decisions_dir`) have uncommitted changes — the worktree loses that context and reviewers may not see invariants/ADRs the plan assumes documented; the operator decides to commit now or proceed. Other uncommitted changes in the working tree (exploration/debug code) **do not** generate a notice — the operator isolated them intentionally, that's the point of the worktree. New entry in `## O que NÃO fazer` forbids bypassing the block by manually copying the plan into the worktree.

### Notes
- Symmetrical complement to the 1.4.0 bump: `/new-feature` proposes the artifact commit at step 5; `/run-plan` now validates that this commit happened (or forces an explicit decision) before creating the worktree. The heuristic acts **starting from** the next `/run-plan` invocation.

## [1.4.0] - 2026-05-03

### Changed
- `/new-feature`: step 5 renamed to **"Reportar, propor commit e devolver controle"**. After reporting the produced artifacts, the skill now **proposes a unified commit** grouping backlog line, plan, `domain.md`/`design.md` updates, etc. — message follows the consumer project's commit convention (default canonical Conventional Commits in English, `docs:`/`chore:` type). Explicit operator confirmation is required before the commit; the step is skipped when there are no new changes (e.g., the path was to delegate to `/new-adr`, which already made its own commit). Closes the operational gap where `/run-plan`, by creating a worktree from HEAD, did not find the plan it should execute because the alignment artifacts had stayed uncommitted. New entry in `## O que NÃO fazer` codifies the guard ("do not commit without confirmation").

### Notes
- Additive change in the skill's behavior. Operators who prefer to commit manually can still decline the proposal; the skill only makes the step explicit instead of silent. The heuristic acts **starting from** the next `/new-feature` invocation.

## [1.3.0] - 2026-05-02

### Added
- `/new-feature`: step 4 (plan production) now prescribes a **"Termos ubíquos tocados"** line in `## Contexto` when step 1 identified terms from `ubiquitous_language` that the request touches (bounded context, aggregate/entity, RN, ubiquitous concept). The plan becomes the explicit messenger of the vocabulary between alignment and execution, without burdening `/run-plan` with re-reading `docs/domain.md`. Plans for changes that do not touch the domain (pure refactor, doc-only, role resolved to "não temos") proceed without the line — silent.
- `agents/code-reviewer.md`: new prescriptive rule in the "Identificadores" section — a new identifier representing a concept declared in `ubiquitous_language` must use the declared term, not an improvised synonym. Complements the pre-existing defensive rule ("cosmetic renaming no"); reviewer flags only when there is a declared term AND a divergent new identifier, gracefully silent in projects without `docs/domain.md`.
- `docs/philosophy.md`: short new section **"Linguagem ubíqua na implementação"** (between "Cobertura de teste em planos" and "Convenção `.worktreeinclude`") codifying the `domain.md` → plan → review pipeline in three stages and the deliberate decision not to touch `/run-plan` (the plan is the messenger, re-reading would duplicate responsibility). Mirrors the `qa-reviewer` invariants pipeline.

### Notes
- Additive change. Pre-existing plans remain valid; reviewer flags only on real divergence. The heuristic acts **starting from** the next `/new-feature` invocation.

## [1.2.0] - 2026-05-02

### Changed
- `/new-feature`: step 1 (reading the `ubiquitous_language` role), step 2 (gap "Aprendizado de domínio") and step 3 (decision table "Atualizar `docs/domain.md`") now explicitly prompt for bounded contexts and aggregates/entities, in addition to ubiquitous language and invariants (RNxx). Aligns the skill with the philosophy's thesis sentence (`docs/philosophy.md` line 7) — bounded contexts and strategic DDD are pillars and deserve to be recorded in `docs/domain.md` on equal footing with the other elements.
- `docs/philosophy.md`: description of the `ubiquitous_language` role in the path-contract table broadens to cover bounded contexts and aggregates/entities, closing the gap between the thesis sentence and the role contract.

### Notes
- Additive change. Projects whose `docs/domain.md` today contains only ubiquitous language and invariants remain valid — recording bounded contexts and aggregates/entities is guidance, not a requirement. The heuristic acts **starting from** the next `/new-feature` invocation.

## [1.1.0] - 2026-05-02

### Added
- `/new-feature`: new "Cobertura de teste necessária?" bullet in the gap checklist (step 2), with a tri-state heuristic codified in `docs/philosophy.md` → "Cobertura de teste em planos". Raises the probability that plans prescribe a test block with `{reviewer: qa}` when the feature touches invariants (RNxx), external integrations, persistence or new observable behavior — without mandatory TDD, keeping ceremony proportional to risk. Pure refactor and doc-only continue without extra ceremony.
- `docs/philosophy.md`: new "Cobertura de teste em planos" section between "Anotação de revisor em planos" and "Convenção `.worktreeinclude`". Codifies principle (tests serve confidence, not metrics; absence is fragility amplified in AI-assisted flow), tri-state heuristic operationalized by `/new-feature`, and relation with `qa-reviewer` (review of the block containing the tests) and stack-specific scaffolders (`/gen-tests-python` complements, does not replace).
- `docs/install.md`: smoke test covering the test-block prescription in a project with a declared RNxx.

### Notes
- Minor bump: convention is additive — consumer projects do not need to change anything to keep working as before; pre-existing plans remain valid. The heuristic acts **starting from** the next `/new-feature` invocation.

## [1.0.0] - 2026-05-02

### Removed
- Deprecated `{revisor: ...}` (PT) alias in plan-block headers. `/run-plan` now refuses this annotation before starting the block, indicating the offending block and annotation. Migrate to `{reviewer: ...}` (EN).

### Fixed
- `docs/philosophy.md` (path-contract table, "convenção Claude Code" line): annotation example migrated from `{revisor: qa}` / `{revisor: security}` to `{reviewer: qa}` / `{reviewer: security}` — escaped the v0.11.0 migration.

### Notes
- The coexistence promised in v0.11.0 (`v0.11–v0.12`) was reduced to `v0.11.x` only. Direct cutover v0.11.x → v1.0 without shipping a v0.12 sentinel. Rationale: v0.12 with no real changes would be overhead without gain, given the low expected external use of the alias.
- Operators with external plans containing `{revisor:}` need to edit to `{reviewer:}` before invoking `/run-plan` (trivial find/replace).
- Major bump: first release with a breaking removal. The entire prior history (v0.1.0–v0.11.1) was additive.

## [0.11.1] - 2026-05-01

### Changed
- `skills/new-feature/SKILL.md`: gap-clarification limit relaxed from "1–2" to "1–3" — two questions could be too few in requests with more than one real gap area.

## [0.11.0] - 2026-05-01

### Changed
- `docs/philosophy.md` consolidated as single source of truth: covers all skills under "Papel obrigatório vs informacional"; mechanical criteria for "clear signal" (language) and "clear predominance" (commits) — both at ≥70%; `{reviewer: ...}` contract formalized with schema, language and multi-profile support; `.worktreeinclude` centralized here; hooks-vs-language policy declared (universal mechanic, always in English).
- `/run-plan` invokes **all** profiles listed in `{reviewer: ...}` (was "most sensitive wins"); accepts `{reviewer: code,qa,security}` aggregating reports.
- `agents/qa-reviewer.md` no longer assumes a `tests/unit/`+`tests/integration/` layout; reviewer infers category by marker, not by path. New "Qualidade dos testes" section with a mechanical happy-path criterion.
- `agents/code-reviewer.md` gains examples per category in the `.claude/settings*.json` rubric; the `application/`/`domain/`/`infrastructure/` rule applies only to new code introduced by the diff (legacy is not flagged); trivial typing leaves the pure "do NOT flag" and gains an exception criterion (explainable reason).
- `skills/new-adr/SKILL.md` template default `**Status:** Proposto` (was `Aceito`); reflects real workflows — an approved ADR becomes `Aceito` after review.
- `CLAUDE.md` stops duplicating "Naming convention" and "Hook auto-gating triple" — becomes a pointer to `docs/philosophy.md`.

### Added
- `{reviewer: ...}` annotation in English as the canonical mechanic; alias `{revisor: ...}` accepted with a warning during v0.11–v0.12, removed in v1.0.
- Reserved `language` key in the YAML config block (`<!-- pragmatic-toolkit:config -->`) to force the consumer project's language.
- `qa-reviewer` and `security-reviewer` declare an explicit division of labor with `code-reviewer` (settings hygiene) and with each other.
- `security-reviewer` gains a fast-path for doc-only diffs and a heuristic fallback when `decisions_dir` resolves to "não temos".
- `/debug` gains a mechanical stop criterion (two consecutive refuted hypotheses without evidence gain) and a dedicated path for intermittent symptoms (statistical reproduction).
- `/new-adr` and `/gen-tests-python` explicitly declare that they **do not commit** — handoff to the operator.

### Fixed
- Path-contract table — `decisions_dir` is a directory, not a pattern (filename pattern migrated to `/new-adr`).
- Repetitions removed in `/new-feature`, `/run-plan`, `/debug`, `/gen-tests-python`.
- Keywords synced between `plugin.json` and `marketplace.json`.
- `block_env` accepts an expanded list of template suffixes (`.j2`, `.erb`, `.mustache`, in addition to the older `.jinja`, `.tmpl`); constant `TEMPLATE_SUFFIXES` documented.
- `run_pytest_python` extracts a `TAIL_LINES` constant with empirical rationale; the literal `10` is no longer magical.
- `hooks.json` gains a `description` per entry with rationale for the timeouts (10s pre, 60s post).
- Manifest description decoupled from skill names.
- Removed orphan "sub-plugin" mention from the introductory paragraph of "Convenção de naming".

### Notes
- Minor bump: formalizes the schema of the `{reviewer: ...}` annotation (was an implicit convention), introduces the reserved `language` key and marks `{revisor: ...}` as a deprecated alias. Mechanical backwards-compat preserved during v0.11–v0.12.
- v1.0 is reserved for the release that **removes** the `{revisor: ...}` alias.
- Plugin is a meta-tool (does not strict-mode-apply its own preconditions to itself) — `CLAUDE.md` stays in English as operating instructions.

## [0.10.0] - 2026-05-01

### Changed
- `code-reviewer` agent gains a specific rubric for `.claude/settings.json` and `.claude/settings.local.json` in the "Infra e configuração" section: flags drift/duplication between shared and local files, leakage of personal entries into shared, hooks with non-portable paths, literal env vars instead of `${VAR}`, and `permissions.allow` only-in-local without explicit rationale. Reuses the default `/run-plan` reviewer — any block touching `.claude/settings*.json` is covered without needing a `{revisor: ...}` annotation.

### Notes
- `security-reviewer` was not extended: broad capability grants in `permissions.allow` already fall under "Privilégios e permissões" (broad ACL / manifest permissions) — duplicating would be noise.
- No new principle in `docs/philosophy.md`: settings hygiene is a mechanical checklist, not a durable design tension.

## [0.9.0] - 2026-05-01

### Added
- Skill `/debug <sintoma>` — diagnoses root cause via the scientific method (precise the symptom → reproduce → isolate → test hypotheses → root cause with evidence). Produces **diagnosis, not a fix**: the operator chooses the correction path afterwards (revert, direct patch, or `/new-feature` if it grows into a larger change). Stack-agnostic — orchestrates method, not debugger toolchain. Roles consumed (all informational): `test_command`, `ubiquitous_language`, `decisions_dir`, `design_notes`.

### Notes
- Skill enforces the `/new-feature` parallel on the bug-fixing axis: "do not fix without isolating the cause". Without this explicit discipline, free-form chat debugging skips steps and regressions return.
- Does not create a worktree, does not write artifacts in the repo, does not apply instrumentation. Proposing instrumentation to the operator is part of the "hypothesize and test" step; applying stays with the operator in their workspace.

## [0.8.0] - 2026-05-01

### Changed
- `security-reviewer` agent generalized to any kind of system (web, CLI, desktop, mobile, embedded, library, pipeline, IaC). Criteria become **principles** that manifest differently per stack: "Chamadas HTTP externas" becomes "I/O externo" (any blocking I/O — RPC, DB, file lock, socket, subprocess); "Tokens em URLs em vez de headers" generalizes to secrets in any insecure channel (visible argv, inherited env, query string); input validation covers additional boundaries (IPC, deserialization, SDK callback, stdin) and injection classes beyond SQL (shell, path traversal, format string, unsafe deserialization, log injection).

### Added
- New "Privilégios e permissões" section in `security-reviewer`: least-privilege in escalation, capability grants, OAuth scopes, IAM roles, manifest permissions, ACLs and entitlements.
- The agent's frontmatter `description` gains an explicit applicability hint ("any kind of system") to avoid being read as a web-only agent. `CLAUDE.md` updated in parallel.

### Notes
- Backwards compat preserved: previously covered diffs remain covered. The detection surface only expanded.

## [0.7.0] - 2026-05-01

### Changed
- Skill `/run-plan` now follows the **consumer project's commit convention** when generating micro-commits. Three-level detection: explicit policy in the project (`CLAUDE.md`, `CONTRIBUTING.md`, etc.) → pattern observed in `git log` → canonical default Conventional Commits in English. Backwards compat preserved: projects without an explicit policy and with history already in CC English keep behavior identical to v0.6.0.

### Added
- Principle "Convenção de commits" in `docs/philosophy.md`: three-level detection protocol, mirroring the "Convenção de idioma" pattern.

### Notes
- "One micro-commit per block" policy stays invariant. `--amend`/rebase of commits from already-closed blocks remain forbidden; amending the last commit of the current block becomes a localized exception (typo, forgotten file), not a rule.

## [0.6.0] - 2026-05-01

### Changed
- Skills (`/new-feature`, `/new-adr`, `/run-plan`, `/gen-tests-python`) and agents (`code-reviewer`, `qa-reviewer`, `security-reviewer`) now **adapt to the consumer project's language** — prose, template headers, test names and review reports mirror the language already in use. Canonical default: PT-BR (toolkit's origin). Backwards compat preserved for PT-BR projects.
- `/run-plan` performs semantic matching of plan headers instead of requiring PT-BR literals (`## Files to change` / `## Arquivos a alterar`, etc., accepted as equivalents).

### Added
- Principle "Convenção de idioma" in `docs/philosophy.md`: project language defines prose; agent names, frontmatter, paths, code and commits remain in English.

### Notes
- This repo's `CLAUDE.md` still says PT-BR — the plugin rule is "mirror the consumer project", and the consumer project in this case (the plugin's own repo) operates in PT.

## [0.5.0] - 2026-05-01

### Changed
- Skill `/new-adr` now consumes the `decisions_dir` role (default: `docs/decisions/`) instead of a literal path.
- Skill `/new-adr` now **infers the numbering format** of existing ADRs in the resolved directory: 3-digit padded (canonical), 4-digit padded or no padding. An empty directory keeps the canonical default (3-digit). Mixed formats in the directory are flagged to the operator before creating the new ADR.

### Notes
- Minor bump: numbering behavior changes in projects that use variants (4-digit or no padding) — before the skill would force 3-digit. Backwards compat preserved for 3-digit projects.

## [0.4.1] - 2026-05-01

### Changed
- Skill `/gen-tests-python` and agents `qa-reviewer`, `security-reviewer`, `code-reviewer` now reference **roles** (`ubiquitous_language`, `design_notes`, `decisions_dir`) instead of literal paths (`docs/domain.md`, `docs/design.md`, `docs/decisions/`). Canonical default cited in parentheses for readability. Backwards compat preserved.

## [0.4.0] - 2026-05-01

### Changed
- Path contract reframed as a **default-per-role convention** (`docs/philosophy.md`). Skills consume roles (`product_direction`, `ubiquitous_language`, `design_notes`, `decisions_dir`, `plans_dir`, `backlog`, `test_command`), not literal paths. Backwards compat 100% preserved for projects following canonical paths.

### Added
- "Resolução de papéis" mechanism in `docs/philosophy.md`: protocol `probe canonical → consult block in CLAUDE.md → ask the operator (tri-state)`, with a fenced YAML block under HTML marker `<!-- pragmatic-toolkit:config -->` as the variant-declaration mechanism.
- Drift detection: skill flags inconsistency to the operator when canonical exists AND `CLAUDE.md` declares a different variant.
- Skills `/new-feature` and `/run-plan` ported to the protocol. `/run-plan`'s test gate now accepts the declared `test_command` (e.g., `uv run pytest`, `npm test`, `cargo test`).
- `docs/install.md` and `README.md` document the config block with examples of typical variants.

### Notes
- `/gen-tests-python`, agents (`qa-reviewer`, `security-reviewer`, `code-reviewer`) and `/new-adr` keep literal references to the path contract — will be ported in v0.4.1 (skills/agents) and v0.5.0 (inferred numbering in `/new-adr`).
- Hooks (`block_env`, `run_pytest_python`) unchanged — `.env*` and `pyproject.toml` are universal markers per ecosystem, not project-config.

## [0.3.1] - 2026-05-01

### Added
- Skill `/new-feature`: "Bifurcação arquitetural" gap in the checklist + exception to the "1-2 questions" rule when the request admits multiple materially different implementations.
- Principle "Nomear bifurcações arquiteturais" in `docs/philosophy.md`.

## [0.3.0] - 2026-04-30

### Added
- Agent: `qa-reviewer` — test coverage principles (happy path, invariants, edge cases, mock vs real). Stack-agnostic.
- Agent: `security-reviewer` — credentials, input validation, external HTTP, sensitive data, invariants in ADRs. Stack-agnostic.
- Naming convention for agents documented in `docs/philosophy.md` (criterion: generates/runs = forces suffix; reviews principles = does not force).

## [0.2.1] - 2026-04-30

### Changed
- `plugin.json` and `marketplace.json` metadata refreshed to mention `/gen-tests-python` and the pytest hook; keywords/tags now include `python`, `pytest`, `testing` for marketplace discovery.

## [0.2.0] - 2026-04-30

### Added
- Skill: `/gen-tests-python` — generates pytest tests for modules/functions of a Python project.
- Hook: `run_pytest_python` — auto-gated PostToolUse (`.py` extension + `pyproject.toml` ancestor); runs pytest and prints output only on failure.
- Naming convention for stack-specific skills and hooks (in `docs/philosophy.md`).

## [0.1.0] - 2026-04-30

Initial release.

### Added
- Skills: `/new-feature`, `/new-adr`, `/run-plan`.
- Agent: `code-reviewer` (YAGNI rubric).
- Hook: `PreToolUse` blocking direct edits to `.env` files (standalone Python script).
- Marketplace manifest for install via `/plugin marketplace add fppfurtado/pragmatic-dev-toolkit`.
- Documentation: philosophy, path contract, install guide.
