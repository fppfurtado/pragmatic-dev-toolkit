# Plano — Completar tabela "What's inside" do README com templates e procedures faltantes

## Contexto

Revisão completa do `README.md` (conversa CC 2026-06-02) identificou 2 gaps de completude na tabela `## What's inside`:

1. **`templates/IDEA.md` ausente.** Template shipped (consumido por `/draft-idea` para elicitação do papel `product_direction`), análogo direto a `templates/plan.md` que é citado. Assimetria editorial.
2. **3 de 4 procedures ausentes.** Só `cleanup-pos-merge.md` é citado; `cutucada-descoberta.md` (5 skills consomem per [ADR-046](../decisions/ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md)), `forge-auto-detect.md` (consumido por `/run-plan` §3.7 + procedure `cleanup-pos-merge`) e `reviewer-invocation-read.md` (3 skills consomem) são igualmente shipped per [ADR-051](../decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (c) que estabeleceu a categoria `docs/procedures/`. Inconsistente listar 1 procedure e omitir 3.

Demais seções do README revisadas estão a contento (positioning, philosophy ADR-043+045, installation, companion, contributing, license) — sem redesign nem reescrita necessária; substância v3.0.0 alinhada com PR #107 recém-mergeado (vocabulário consumer-agnóstico do filtro de admissão).

**ADRs candidatos:** [ADR-046](../decisions/ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) (origem do `cutucada-descoberta.md` procedure), [ADR-051](../decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (c) (estabelece categoria `docs/procedures/` shipped).

## Resumo da mudança

Adicionar 4 linhas à tabela `## What's inside` do `README.md` mantendo agrupamento por categoria e estilo editorial das linhas existentes (1-2 sentenças + cross-ref ADR):

- 1 linha de template (`templates/IDEA.md`) inserida antes da linha `templates/plan.md` (ordem alfabética dentro da categoria).
- 3 linhas de procedure (`cutucada-descoberta.md`, `forge-auto-detect.md`, `reviewer-invocation-read.md`) inseridas após `cleanup-pos-merge.md` (alfabética dentro da categoria).

Fora de escopo: agrupar a tabela por tipo via sub-headers (Skills / Agents / Hooks / Templates / Procedures); condensar descrições densas de `/new-adr`/`/note`/`design-reviewer`; outras edições editoriais — registrar como item BACKLOG separado se sinal empírico de fricção emergir.

## Arquivos a alterar

### Bloco 1 — completar tabela "What's inside" com templates/IDEA.md + 3 procedures {reviewer: doc}

`README.md`:

- **Inserir antes da linha `templates/plan.md`** (atual linha 31):
  - `| \`templates/IDEA.md\` | Template | Canonical IDEA.md skeleton (consumed by \`/draft-idea\` for structured \`product_direction\` elicitation). Reference for hand-writing the doc. |`

- **Inserir após a linha `docs/procedures/cleanup-pos-merge.md`** (atual linha 32), em ordem alfabética:
  - `| \`docs/procedures/cutucada-descoberta.md\` | Procedure | Shared procedure consumed via \`Read\` by 5 skills (\`/triage\`, \`/run-plan\`, \`/new-adr\`, \`/next\`, \`/draft-idea\`) emitting the \`/init-config\` discovery hint when the config marker or \`CLAUDE.md\` is absent (tri-state gating + 2 canonical literal strings). Per [ADR-046](docs/decisions/ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) + [ADR-051](docs/decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (c). |`
  - `| \`docs/procedures/forge-auto-detect.md\` | Procedure | Shared procedure consumed via \`Read\` by \`/run-plan\` (§3.7 publish enum) and \`cleanup-pos-merge\` (PR/MR merge status). Returns \`gh\` / \`glab\` / \`unsupported-host\` / \`no-detection\`. Per [ADR-051](docs/decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (c). |`
  - `| \`docs/procedures/reviewer-invocation-read.md\` | Procedure | Shared procedure consumed via \`Read\` by 3 skills (\`/run-plan\` §2.3, \`/triage\` step 5, \`/new-adr\` step 5) — caller-side instruction forcing reviewer to \`Read\` target file before analysis (resilience against stale \`git diff\` between Edit and Agent invocation). Per [ADR-051](docs/decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (c). |`

## Verificação end-to-end

Gates mecânicos:

1. **Cobertura completa** — counts esperados via `grep -cE` sobre `README.md`:
   - `templates/(IDEA|plan)\.md`: 2 (templates shipped completos).
   - `docs/procedures/[a-z-]+\.md`: 4 (procedures shipped completos).

2. **Linhas adicionadas no formato canonical da tabela** — `grep -nE "^\| \`(templates|docs/procedures)/" README.md` retorna 6 linhas (2 templates + 4 procedures).

3. **Cross-refs ADR válidos** — `grep -oE "ADR-[0-9]{3}" README.md | sort -u` inclui `ADR-046` e `ADR-051` (cross-refs introduzidos pelos novos procedures); ambos arquivos existem em `docs/decisions/`.

4. **Read manual** da tabela completa para verificar agrupamento alfabético dentro de cada categoria e estilo editorial coerente com linhas pré-existentes.
