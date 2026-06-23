# Plano — Bullet `**TestCommand:**` em CLAUDE.md § Editing conventions

## Contexto

`**TestCommand:**` foi implementado em `/run-plan` via PR #147 (ADR-068). O CLAUDE.md § Editing conventions não foi atualizado com o bullet correspondente — gap identificado durante o gate final do plano anterior e capturado como issue #146.

**Linha do backlog:** #146: docs(CLAUDE.md): add editing-conventions bullet for **TestCommand:** field

## Resumo da mudança

- Adicionar 1 bullet em CLAUDE.md § Editing conventions documentando o campo `**TestCommand:**`, paralelo ao bullet `**Modo:** runbook em planos de system-surgery`.
- Sem mudanças em SKILL.md, templates, ou ADR-068.

## Arquivos a alterar

### Bloco 1 — `CLAUDE.md` § Editing conventions {reviewer: doc}

- `CLAUDE.md`: inserir bullet após `**Modo:** runbook em planos de system-surgery: ...` documentando o campo declarativo `**TestCommand:**` — campo opcional no `## Contexto` do plano que substitui o `test_command` resolvido do CLAUDE.md local em todos os 3 sites de gate automático do `/run-plan`; valor `null` literal → skip de gate; ausência = resolve normalmente; no-op em `**Modo:** runbook`. Cross-refs: ADR-068 + ADR-049 § Decisão (e).

## Verificação end-to-end

1. `grep -n "TestCommand" CLAUDE.md` → ≥1 match em § Editing conventions.
2. `grep -n "ADR-068" CLAUDE.md` → ≥1 match com link path correto `docs/decisions/ADR-068-*.md`.
