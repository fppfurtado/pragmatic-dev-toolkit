---
name: archive-plans
description: Periodic editorial archival of historical plans from docs/plans/ to docs/plans/archive/<YYYY-Qx>/, preview-first, non-destructive (git mv). Use when the maintainer wants to archive aged plans.
disable-model-invocation: false
roles:
  informational: [backlog, plans_dir]
---

# archive-plans

Archival editorial periódico de planos antigos do papel `plans_dir` (default `docs/plans/`). Move plano elegível para `docs/plans/archive/<YYYY-Qx>/<slug>.md` via `git mv` (preserva blame, `git log --follow` funcional). **Não-destrutivo, preview-first, sob demanda.**

Mecânica per [ADR-022](../../docs/decisions/ADR-022-politica-archival-docs-plans.md).

## Argumentos

- `--quarter <YYYY-Qx>` (opcional) — filtra archival a um quarter específico (ex.: `--quarter 2026-Q1`). Default: todos os quarters elegíveis.
- Sem argumento é o caso comum.

## Pré-condições

1. **Working tree limpo** (`git status --porcelain` vazio). Archival mistura mal com mudança não-revisada; bloquear preserva isolamento.
2. **Não bloqueia por branch.** Operador pode legitimamente rodar `/archive-plans` em hotfix branch antes de mergeear; paralelo a `/release` que cutuca branch via enum mas não bloqueia.

## Passos

### 1. Coletar candidatos

`ls docs/plans/*.md` (excluindo `docs/plans/archive/**`). Para cada plano `<slug>.md`, avaliar os **6 critérios cumulativos** per ADR-022:

1. **`**Linha do backlog:**` presente** — `grep -E "^\*\*Linha do backlog:\*\*" docs/plans/<slug>.md` retorna não-vazio. Ausente → **editorial** (`not eligible: <slug>.md — sem **Linha do backlog:**; archival manual`).
2. **Linha matchável** em `BACKLOG.md` (qualquer seção) — extrair `<texto>` do campo, `grep -F "<texto>" BACKLOG.md` retorna não-vazio. Não localizada → **editorial** (`not eligible: <slug>.md — **Linha do backlog:** não localizada; verificar matching`).
3. **Linha está em `## Concluídos`, não em `## Próximos`.** Varrer BACKLOG.md de `## Concluídos` até EOF (ou próximo `##`); verificar `<texto>` aparece. Em Próximos → **silente** (item não terminou; sem reporte).
4. **Idade ≥ 2 semanas** — `git log -S "<texto>" --diff-filter=A --reverse BACKLOG.md | head -1` → primeiro commit que adicionou o texto (pickaxe; robusto a reedições in-place). Comparar timestamp com `date -d '2 weeks ago' +%s`. Mais recente → **silente**.
5. **Sem worktree** — `git worktree list --porcelain | grep -q "\.worktrees/<slug>$"` E `test -d .worktrees/<slug>` ambos falsos. Worktree registrada OU órfã → **aviso** (`not eligible: <slug>.md — worktree em .worktrees/<slug> (registrada/órfã); trabalho em curso`).
6. **Sem PR aberto referenciando o slug** — seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md` para detectar forge:
   - Output `gh` → `gh pr list --search <slug> --state open --json number --jq 'length'`.
   - Output `glab` → `glab mr list --search <slug>`.
   - Output `no-detection` ou `unsupported-host` → **plano não-elegível nesta invocação** (`degraded: <slug>.md — forge não-mapeado ou CLI ausente; not eligible this run, retry após restaurar gh/glab`). **Não** assume seguro — vetor do risco é arquivar plano com PR aberto durante trabalho em curso.
   - PR encontrado → **aviso** (`not eligible: <slug>.md — PR/MR aberto referenciando <slug>; trabalho em curso`).

Filtrar candidatos por `--quarter` quando especificado: elegíveis cujo `<YYYY-Qx>` (derivado do critério 4) bate.

### 2. Detectar cross-refs por elegível

Para cada plano elegível: `grep -rn "docs/plans/<slug>.md" docs/decisions/` — lista links em prosa de ADRs (incluindo `## Implementação` e referências cruzadas).

### 3. Apresentar preview estruturado

Reportar ao operador:

- **Elegíveis** (N): cada um como `<slug>.md → archive/<YYYY-Qx>/`.
- **Cross-refs detectados** (M): por plano elegível, listar `ADR-NNN:<linha>: <trecho>` (informação ao operador; não bloqueia).
- **Não-elegíveis reportados** (K): mensagem por categoria — `Editorial` (ausência do campo / linha não localizada), `Aviso` (worktree ativa, PR aberto), `Degraded` (forge inacessível). Silentes (linha em Próximos, idade < 2 semanas) omitidos do reporte.
- **Resumo final:** `N planos elegíveis; M cross-refs detectados; K não-elegíveis reportados; <Q> silentes.`

### 4. Gate `AskUserQuestion`

Header `Archive`, opções:

- **`Aplicar`** — description: `executa N git mv + commit chore unificado; sem push.`
- **`Cancelar`** — description: `nada a aplicar; relatório fica como referência editorial.`

Sem `Recommended` — operador decide após ver preview; ambos os caminhos são legítimos.

### 5a. Aplicar

Para cada elegível, em ordem:

1. `mkdir -p docs/plans/archive/<YYYY-Qx>/` (idempotente).
2. `git mv docs/plans/<slug>.md docs/plans/archive/<YYYY-Qx>/<slug>.md`.

Commit unificado:

```
chore: archive <N> historical plans

archive/<YYYY-Qx>/<slug-1>.md
archive/<YYYY-Qx>/<slug-2>.md
...
```

Skill **não pusha** — operador decide quando publicar (paralelo a `/release`).

### 5b. Cancelar

Abort silente; nada a reverter (nenhum `git mv` aconteceu).

## Sub-fluxo: des-arquivar

Operador querendo retomar plano arquivado: `git mv docs/plans/archive/<YYYY-Qx>/<slug>.md docs/plans/<slug>.md` manualmente. **Sem comando dedicado nesta skill** (YAGNI per ADR-022 § Limitações).

## O que NÃO fazer

- **Não modificar conteúdo do plano arquivado** — só `git mv` move; `**Linha do backlog:**` deve permanecer intacto para archeology cruzar com BACKLOG `## Concluídos`.
- **Não modificar ADRs com cross-refs detectados** — preview apenas reporta; operador decide se atualiza paths em prosa antes de `Aplicar`. Skill nunca edita ADRs.
