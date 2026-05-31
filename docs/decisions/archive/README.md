# Archived ADRs

Mapping of archived ADRs → current authority (post-redesign per [ADR-045](../ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md)).

ADRs are archived (not deleted) per ADR-045 § Decisão parte 1: *"Arquivamento (não deleção) materializa Verdade — preserva memória do projeto sobre onde formalização passou do ponto"*. Cada arquivo arquivado carrega header redirect canonical (blockquote `> **ARCHIVED <data>**`) + corpo histórico integral preservado abaixo.

Tabela atualizada incrementalmente por cada onda C-X conforme migração avança.

| Archived ADR | Absorbed into | Onda |
|---|---|---|
| ADR-017 — Cutucada uniforme em skills para descoberta de configuração ausente | [ADR-046](../ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) | C |
| ADR-029 — Cutucada de descoberta cobre `CLAUDE.md` ausente | [ADR-046](../ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) | C |
| ADR-005 — Modo local-gitignored para roles do path contract | [ADR-047](../ADR-047-modo-local-paths-replicacao-cross-mode.md) | D |
| ADR-018 — Replicação `.claude/` em modo local: responsabilidade proativa do `/init-config` | [ADR-047](../ADR-047-modo-local-paths-replicacao-cross-mode.md) | D |
| ADR-025 — Recusar cross-mode `backlog: local + plans_dir: canonical` no `/init-config` | [ADR-047](../ADR-047-modo-local-paths-replicacao-cross-mode.md) | D |
| ADR-030 — `/init-config` aceita `CLAUDE.md` gitignored com replicação via `.worktreeinclude` | [ADR-047](../ADR-047-modo-local-paths-replicacao-cross-mode.md) | D |
| ADR-021 — Curadoria do free-read do design-reviewer (anotação + scan) | [ADR-048](../ADR-048-free-read-design-reviewer-consolidado.md) | E |
| ADR-044 — Scan medium + always-include foundationals no free-read do design-reviewer | [ADR-048](../ADR-048-free-read-design-reviewer-consolidado.md) | E |
| ADR-004 — State-tracking em git/forge, não em markdown | [ADR-049](../ADR-049-execucao-run-plan-consolidado.md) | F |
| ADR-028 — Campo Branch opcional no plano para fluxo issue-first | [ADR-049](../ADR-049-execucao-run-plan-consolidado.md) | F |
| ADR-039 — Task tool como state-keeping em fluxo longo | [ADR-049](../ADR-049-execucao-run-plan-consolidado.md) | F |
| ADR-041 — Campo `**Modo:** runbook` opt-in em planos para `/run-plan` cobrir system-surgery | [ADR-049](../ADR-049-execucao-run-plan-consolidado.md) | F |
| ADR-008 — Skills geradoras stack-agnósticas via dispatch interno | [ADR-050](../ADR-050-componentes-plugin-consolidado.md) | G |
| ADR-013 — CI lint mínimo como complemento à doutrina no-build/runner | [ADR-050](../ADR-050-componentes-plugin-consolidado.md) | G |
| ADR-015 — Bloquear env-files por sufixo `.env`, não apenas dotfile | [ADR-050](../ADR-050-componentes-plugin-consolidado.md) | G |
| ADR-016 — Manter `block_gitignored` como está; falso-positivo em scripts operacionais é problema do consumer | [ADR-050](../ADR-050-componentes-plugin-consolidado.md) | G |
| ADR-023 — Critério mecânico para declaração explícita de `disable-model-invocation` em skills | [ADR-050](../ADR-050-componentes-plugin-consolidado.md) | G |
| ADR-040 — Bloquear paths absolutos em `.claude/settings.json` via PreToolUse hook | [ADR-050](../ADR-050-componentes-plugin-consolidado.md) | G |
| ADR-007 — Idioma de artefatos informativos segue convenção de commits | [ADR-051](../ADR-051-convencoes-editoriais-consolidado.md) | H |
| ADR-012 — Idioma de artefatos de discoverability/landing | [ADR-051](../ADR-051-convencoes-editoriais-consolidado.md) | H |
| ADR-024 — Categoria docs/procedures/ para procedimentos operacionais compartilhados | [ADR-051](../ADR-051-convencoes-editoriais-consolidado.md) | H |
| ADR-011 — Wiring automático do design-reviewer no /triage e /new-adr | [ADR-053](../ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) | I |
| ADR-026 — Critério mecânico de absorção de findings do design-reviewer pré-commit | [ADR-053](../ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) | I |
| ADR-027 — Skill /draft-idea para elicitação estruturada de product_direction | [ADR-053](../ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) | I |
| ADR-038 — Mirror de Decisões absorvidas no plan body + consumo runtime por reviewers | [ADR-053](../ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) | I |
