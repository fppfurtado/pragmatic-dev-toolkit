# Plano — Skill /archive-plans

## Contexto

Implementação da skill `/archive-plans` codificada em [ADR-022](../decisions/ADR-022-politica-archival-docs-plans.md). Operação editorial periódica do mantenedor: archival não-destrutivo de planos antigos de `docs/plans/` para `docs/plans/archive/<YYYY-Qx>/<slug>.md`, com preview obrigatório antes do `git mv`.

Origem: proposta E_arch da auditoria arquitetural 2026-05-12 (`docs/audits/runs/2026-05-12-architecture-logic.md`, achado E2), terceiro item da Onda 1 do roadmap `docs/audits/runs/2026-05-12-execution-roadmap.md`.

**ADRs candidatos:** ADR-022 (matéria deste plano), ADR-014 (decisão base — main único, archival não-destrutivo), ADR-004 (pipeline `**Linha do backlog:**` que o critério (2) consome), ADR-021 (pattern de skill periódica low-frequency com gate preview-style), ADR-013 (precedente de critério mecânico cumulativo), ADR-020 (paralelo direto: critério cumulativo recente em `/run-plan`).

## Resumo da mudança

Criar skill nova `/archive-plans` per spec do ADR-022:
- 6 critérios cumulativos de elegibilidade (linha BACKLOG presente + matchável + em Concluídos + ≥4 semanas + sem worktree + sem PR aberto).
- Layout `docs/plans/archive/<YYYY-Qx>/<slug>.md`.
- Operação preview-first com gate `Aplicar / Cancelar` (paralelo a `/release §4`).
- `git mv` preserva blame e `--follow`.
- Skill **não pusha** (operação visível é decisão deliberada do operador).

2 blocos doc-only — skill nova + atualização de discoverability.

## Arquivos a alterar

### Bloco 1 — Criar `skills/archive-plans/SKILL.md` {reviewer: doc}

Skill nova seguindo formato canonical do toolkit. Estrutura:

- **Frontmatter (literal):**
  ```yaml
  ---
  name: archive-plans
  description: Periodic editorial archival of historical plans from docs/plans/ to docs/plans/archive/<YYYY-Qx>/, preview-first, non-destructive (git mv). Use when the maintainer wants to archive aged plans.
  disable-model-invocation: false
  roles:
    informational: [backlog, plans_dir]
  ---
  ```
  Sem `roles.required` (skill opera mesmo sem `**Linha do backlog:**` em algum plano — gera relatório editorial em vez de falha).
- **Argumentos:** opcional `--quarter <YYYY-Qx>` para filtrar archival a um quarter específico (default: todos os quarters elegíveis). Sem argumento é o caso comum.
- **Pré-condições:**
  - Working tree limpo (`git status --porcelain` vazio) — bloqueia para não misturar archival com mudança não-revisada.
  - **Não** bloqueia por branch — operador pode legitimamente rodar `/archive-plans` em hotfix branch antes de mergeear. Paralelo a `/release` (que cutuca branch via enum mas não bloqueia).
- **Passos:**
  - **1. Coletar candidatos.** `ls docs/plans/*.md` (excluindo `docs/plans/archive/**`). Para cada plano, avaliar os 6 critérios cumulativos:
    - **(1) `**Linha do backlog:**`** presente — `grep -E "^\\*\\*Linha do backlog:\\*\\*" docs/plans/<slug>.md` retorna não-vazio. Ausente → editorial.
    - **(2) Linha matchável** em `BACKLOG.md` (qualquer seção) — `grep -F "<texto>" BACKLOG.md` retorna não-vazio. Não localizada → editorial.
    - **(3) Linha em `## Concluídos`** — varrer BACKLOG.md de `## Concluídos` até EOF ou próximo `##`; verificar se `<texto>` aparece. Em Próximos → silente (item não terminou).
    - **(4) Idade ≥ N=4 semanas** — `git log -S "<texto>" --diff-filter=A --reverse BACKLOG.md | head -1` → primeiro commit que adicionou o texto. Comparar timestamp com `date -d '4 weeks ago' +%s`. Mais recente → silente.
    - **(5) Sem worktree** — `git worktree list --porcelain | grep -q ".worktrees/<slug>$"` E `test -d .worktrees/<slug>` ambos falsos. Worktree registrada OU órfã → aviso.
    - **(6) Sem PR aberto** — auto-detect forge per `/run-plan §3.7` (parse `git remote get-url origin`; `github.com` → `gh pr list --search <slug> --state open`; regex `^gitlab\.` → `glab mr list --search <slug>`). PR encontrado → aviso. Forge inacessível (CLI ausente, host não-mapeado) → `degraded:` reportado (plano não-elegível nesta invocação).
  - **2. Detectar cross-refs por elegível.** `grep -rn "docs/plans/<slug>.md" docs/decisions/` — lista links em prosa de ADRs.
  - **3. Apresentar preview estruturado** ao operador:
    - **Elegíveis** (N): cada um com `<slug>.md → archive/<YYYY-Qx>/`.
    - **Cross-refs detectados** (M): por plano elegível, listar `ADR-NNN:<linha>: <trecho>`.
    - **Não-elegíveis com reporte** (K): mensagem por categoria — Editorial (`not eligible: <slug>.md — <razão>`), Aviso (`not eligible: <slug>.md — <razão> em curso`), Degraded (`degraded: <slug>.md — forge inacessível, retry após restaurar`). Silentes omitidos.
    - **Resumo final:** `N planos elegíveis; M cross-refs detectados; K não-elegíveis reportados; <Q> silentes (idade ou Próximos)`.
  - **4. Gate `AskUserQuestion`** (header `Archive`):
    - `Aplicar` — descrição: `executa N git mv + commit chore unificado; sem push.`
    - `Cancelar` — descrição: `nada a aplicar; relatório fica como referência editorial.`
  - **5a. Aplicar:** para cada elegível: `mkdir -p docs/plans/archive/<YYYY-Qx>/` + `git mv docs/plans/<slug>.md docs/plans/archive/<YYYY-Qx>/<slug>.md`. Commit unificado:
    ```
    chore: archive <N> historical plans

    archive/<YYYY-Qx>/<slug-1>.md
    archive/<YYYY-Qx>/<slug-2>.md
    ...
    ```
    Skill **não pusha**.
  - **5b. Cancelar:** abort silente; nada a reverter (nenhum `git mv` aconteceu).
- **O que NÃO fazer** (apenas guards não-óbvios per `CLAUDE.md` § Editing conventions — critério editorial):
  - Não modificar conteúdo de plano arquivado — só `git mv` move o arquivo; `**Linha do backlog:**` deve permanecer intacto para archeology cruzar com BACKLOG `## Concluídos`.
  - Não modificar ADRs com cross-refs detectados — apenas reportar no preview; operador decide se atualiza paths em prosa antes de `Aplicar`.

### Bloco 2 — `README.md` + `docs/install.md` {reviewer: doc}

**`README.md`:** adicionar linha na tabela "What's inside" após `/release`:

```markdown
| `/archive-plans [--quarter <YYYY-Qx>]` | Skill | Periodic editorial archival: moves plans in `docs/plans/` whose backlog line entered `## Concluídos` ≥4 weeks ago to `docs/plans/archive/<YYYY-Qx>/`. Preview-first with `Apply / Cancel` gate; non-destructive (`git mv` preserves history). Doesn't push. |
```

EN per ADR-012 (artefato de discoverability/landing).

**`docs/install.md`:** adicionar item ao smoke checklist (após o item 10 do `/release`), exercitando preview + cancel:

```markdown
11. Em projeto com ≥1 plano em `docs/plans/` cuja `**Linha do backlog:**` está em `BACKLOG.md ## Concluídos` há ≥4 semanas, invocar `/archive-plans` → confirmar preview lista o plano com destino `archive/<YYYY-Qx>/`; ao selecionar `Cancelar`, confirmar que nenhum `git mv` foi executado (`git status` limpo). Ao re-invocar e selecionar `Aplicar`, confirmar `git mv` + commit `chore: archive <N> historical plans`, **sem push**.
```

PT-BR (install.md é operativo per ADR-012).

## Verificação end-to-end

Sem `test_command` neste repo (per `CLAUDE.md`). Inspeção textual:

1. **Bloco 1 (skill):** `ls skills/archive-plans/SKILL.md` presente; `grep -E "^(name|description):" skills/archive-plans/SKILL.md` retorna 2 linhas (frontmatter parse manual — CI lint atual do ADR-013 não cobre frontmatter de skills/agents per cobertura positiva diferida); seções `## Argumentos`, `## Pré-condições`, `## Passos`, `## O que NÃO fazer` presentes; mecânica dos 6 critérios + preview gate descrita em prosa com comandos shell concretos.
2. **Bloco 2 (docs):** `grep -n "/archive-plans" README.md docs/install.md` retorna ≥2 sites (tabela do README + smoke checklist do install). Linguagem EN no README, PT-BR no install.

## Verificação manual

Cenários **enumerados** (per `/triage` § Surface não-determinística — skill matcha strings contra BACKLOG real). Smoke pós-shipping no plugin meta-toolkit:

1. **Cenário "plano antigo elegível":** invocar `/archive-plans` no plugin (que tem ~55 planos hoje, vários cujo Concluído tem >4 semanas) → confirmar preview lista os elegíveis com destino `archive/<YYYY-Qx>/` correto; confirmar que planos do refactor sweep recente (2026-05-06 → 12) **não** entram (idade < 4 semanas).
2. **Cenário "plano sem `**Linha do backlog:**`":** plantar um plano de teste sem o campo (ou identificar plano histórico sem) → confirmar relatório editorial `not eligible: <slug>.md — sem **Linha do backlog:**`.
3. **Cenário "worktree" em dois sub-casos** — exercitar ambos os ramos do critério (5):
   - **3a (registrada e ativa):** `git worktree add .worktrees/<slug>-test <commit>` onde `<slug>` é plano elegível por idade → confirmar aviso `not eligible: ... — worktree em .worktrees/<slug>`. Cleanup: `git worktree remove .worktrees/<slug>-test`.
   - **3b (órfã):** após 3a, `rm -rf .worktrees/<slug>-test` sem `git worktree remove` (worktree deixa rastro em `.git/worktrees/` mas dir desaparece — ou vice-versa, mantendo dir sem registro). Re-invocar `/archive-plans` → confirmar probe `test -d` cobre o caso e aviso ainda dispara.
4. **Cenário "forge inacessível"** sem destruir setup do dev: `env PATH=/usr/bin:/bin /archive-plans` (PATH temporariamente sem `gh`/`glab`) **ou** invocar a partir de `/tmp/repo` que clone seja sem remote `origin` configurado → confirmar plano com PR check vira `degraded:` e fica em `docs/plans/`.
5. **Cenário "preview + cancel":** após preview com ≥1 elegível, selecionar `Cancelar` no gate → confirmar `git status` permanece limpo (nenhum `git mv` executado).
6. **Cenário "preview + apply":** após cenário 5, re-invocar e selecionar `Aplicar` → confirmar `git mv` + commit; confirmar `git log --follow docs/plans/archive/<YYYY-Qx>/<slug>.md` segue história completa do plano.
7. **Cenário "cross-ref em ADR":** plano elegível cujo slug aparece em `## Implementação` de algum ADR → confirmar preview lista cross-ref como informação ao operador (não bloqueia).

Captura: qualquer divergência entre comportamento observado e ADR-022 vai para `## Pendências de validação` deste plano.

## Notas operacionais

- **Ordem dos blocos:** Bloco 1 (skill) antes do Bloco 2 (docs). Documentar antes da skill existir cria docs órfãos.
- **Reviewer dispatch:** ambos os blocos com `{reviewer: doc}` — paths `.md` apenas; sem código de produção.
- **Roadmap** (`docs/audits/runs/2026-05-12-execution-roadmap.md`) tem entrada `[ ] E_arch` que vira `[~]` em andamento ao commitar este plano (decisão + plano shippados; implementação via `/run-plan` pendente). Atualização manual no commit unificado do `/triage` (mesma convenção de B_arch).
- **Smoke pós-shipping no consumer externo** (PJe ou outro) é gatilho de validação adicional — observar se `/archive-plans` em projeto pequeno (<10 planos) faz sentido, e se forge GitLab-corporativo é detectado corretamente.
- **Cenário 7 (cross-ref em ADR)** pode revelar que ADRs do plugin têm cross-refs em prosa que não foram migrados para path do `archive/`. Captura como Validação se acontecer.
- **N=4 semanas** é heurística; primeira invocação no plugin é o calibrador empírico. Se arquivar planos que deveriam permanecer ativos, gatilho de revisão #1 do ADR-022 aplica.
- **Cross-refs quebrados em ADRs após `Aplicar`** é **comportamento esperado** per ADR-022 § Trade-offs (preview delega a decisão; autor pode aceitar link quebrado como referência histórica). Se o operador quiser atualizar ADR antes do `Aplicar`, faz manualmente fora da skill — `/archive-plans` reporta no preview mas não edita ADRs.
- **CHANGELOG.md é responsabilidade do `/release`** no próximo bump (skill agrupa CC desde a última tag; este plano shippa via `feat: /archive-plans skill` que `/release` classifica como Added). `marketplace.json` description permanece abstract — não exige update por skill nova.
