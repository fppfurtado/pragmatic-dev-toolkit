# ADR-060: Heurística de completude de planos via campo `## Status` complementar a git/forge

**Data:** 2026-06-12
**Status:** Proposto

## Origem

- **Investigação:** plano `docs/plans/session-audit-skill.md` committed em `6e6b5b7` + `/run-plan` abortado por cross-cwd; órfão pré-execução invisível ao `/next` que sugeriu top 3 do BACKLOG sem mencionar o plano pendente (sessão CC 2026-06-12). Demais 56 planos vigentes pós-`/archive-plans 2026-Q2` (commit `6e8fed5`) caem em estado indistinguível: `Concluído`-com-gap-editorial vs `Pendente` vs órfão.
- **Decisão base:** [ADR-022](ADR-022-politica-archival-docs-plans.md) — estabelece signal de completude via cadeia editorial (`**Linha do backlog:**` × `BACKLOG.md ## Concluídos` + age). Cobre 57/125 planos hoje (caso feliz); falha em 56 por gap editorial.
- **Decisão fronteira:** [ADR-049](ADR-049-execucao-run-plan-consolidado.md) § Decisão (a) — state-tracking de in-flight work vive em git/forge (branches/PRs), explicitamente removido de markdown. Fronteira deste ADR: complementa pro que git/forge **não** captura, sem reintroduzir em markdown o que git já carrega.
- **Linha do backlog:** "plugin: heurística mecânica de completude pra planos em `plans_dir` (vigentes + arquivados)" — introduzida em `BACKLOG.md ## Próximos` no commit `5f1d6f7` (2026-06-12).

## Contexto

`docs/plans/` deste repo tem hoje (pós-`/archive-plans 2026-Q2` em `6e8fed5`):

- **57 arquivados** em `archive/2026-Q2/` — passaram nos 6 critérios cumulativos de ADR-022; semanticamente concluídos.
- **68 vigentes** em `docs/plans/` (não-arquivados) — heterogêneos:
  - 30 sem campo `**Linha do backlog:**` (convenção pré-padronização do ADR-022).
  - 26 com campo mas linha não localizada no BACKLOG (edição posterior).
  - 12 silentes (< 2 semanas; re-elegíveis automaticamente).
  - 1 órfão pré-execução documentado (`session-audit-skill.md`).
  - Saldo: misturado entre `Pendente` / `Em execução` / `Abortado` / `Concluído-com-gap`.

`/next` passo 4.5 (varredura de `## Pendências de validação`) cobre **pendências post-validation** dos planos concluídos. **Não cobre** planos `Pendente`/`Em execução`/`Abortado`/órfãos.

Signal de completude de ADR-022 é heurístico: depende de cadeia editorial intacta. Falha em 56/125 por elos quebrados. Casos `Concluído-com-gap-editorial` e `Pendente real` caem ambos em "editorial reportable" — semanticamente diferentes, operacionalmente indistinguíveis.

ADR-049 § Decisão (a) cobre **state vivo de in-flight work** via branches/PRs descobríveis em git/forge. Reintroduzir state-tracking em markdown é regressão doutrinal. Mas dois estados não são capturados por git/forge:

- **`Pendente`** — plano committed sem execução iniciada (zero worktree, zero PR, zero commits após o de criação). Caso `session-audit-skill`.
- **`Abortado`** — abandono deliberado. Git/forge tem signal fraco (PR fechado-sem-merge confunde iteração natural com abandono).

Necessário: signal mecânico **complementar** que distinga esses dois estados sem reintroduzir redundância com git/forge.

## Decisão

**Adicionar campo `## Status` no body do plano carregando apenas estados que git/forge não captura: `Pendente` ou `Abortado`. Os estados `Em execução` e `Concluído` continuam derivados de git/forge (worktree-active/PR-aberto e `archive/` presence/linha em `## Concluídos` respectivamente) per ADR-049 § Decisão (a) e ADR-022 § critério 3. Field ausente significa "git/forge state é canonical" — válido tanto para legacy sem field quanto para planos em transição.**

`/triage` step 4 (caminho-com-plano) cria o plano com `## Status: Pendente`. `/run-plan §3.4` (done) remove o bloco `## Status` integralmente — plano transiciona para "git/forge canonical" via `archive/` presence + linha em `## Concluídos`. Operador edita manualmente para `Status: Abortado` quando decide abandonar. `/archive-plans` preserva critérios atuais de ADR-022; adiciona "field ausente ou field=Pendente sem worktree há ≥4 semanas" como warning (não bloqueia archival, mas reporta). `/next varrer planos em aberto` (item irmão dependente) consome via cross-reference: field-or-git-state.

### Modelo de signal por estado

| Estado | Signal canonical | Fonte |
|---|---|---|
| `Pendente` | `## Status: Pendente` no body (field explícito) | Markdown |
| `Em execução` | worktree-active OR PR/MR aberto referenciando slug | git/forge (per ADR-049 § Decisão (a)) |
| `Concluído` | presença em `archive/<YYYY-Qx>/` OR (`**Linha do backlog:**` em `## Concluídos` + age threshold per ADR-022) | git/filesystem + BACKLOG |
| `Abortado` | `## Status: Abortado` no body (field explícito) | Markdown |

Field é **complementar**, não substitutivo. Precedência de leitura em consumidores: git signal de in-flight (Em execução) > archive/ presence (Concluído) > field (Pendente/Abortado) > "ambíguo" (legacy ou drift).

### Razões

1. **Field complementar respeita fronteira de ADR-049 § Decisão (a).** State vivo de in-flight permanece em git/forge; Status field só carrega o que git/forge não consegue distinguir (`Pendente` ≠ legacy/drift; `Abortado` ≠ iteração natural). Single source of truth preservado por estado, sem duplicação.

2. **Mutation no plan body reduzida a 2 pontos canonical.** `/triage` step 4 cria field (zero conflito — plano não existe ainda); `/run-plan §3.4` remove field (mesma sequência atômica que muta BACKLOG.md). Sem mutation em `/run-plan §1` (que tem worktree-isolada). F3 do design-reviewer resolvido — pontos de mutação não colidem com worktree/runbook/local.

3. **`/next varrer planos em aberto` ganha signal mecânico pro caso original.** `session-audit-skill.md` materializa `Status: Pendente`; varredura nova lista planos `Pendente` (sem worktree/PR) ou `Em execução` (com worktree/PR) ou `Abortado` (explícito).

4. **Custo de migração bounded e assimétrico.** 57 arquivados: **nenhum backfill** (`archive/` presence basta como Concluído per ADR-022). 68 vigentes: editorial wave per-plano com 4 sub-casos mecânicos + 1 catch-all (estimativa: ~30 planos exigem julgamento individual; ~1-2 min/plano = 30-60 min de trabalho). Coberto pelo passo 3 do programa upstream (2026-06-12).

5. **Sucessor parcial de ADR-022 sem invalidar.** ADR-022 critério 3 (linha em `## Concluídos`) preservado integralmente como signal de Concluído. Field é signal complementar para Pendente/Abortado. ADR-022 § Decisão recebe parágrafo cross-ref pro ADR-060 cobrindo a complementaridade.

6. **Forward-only operator-declarative pros 2 estados novos.** `/triage` cria default; operador override para Abortado quando decide. Sem hooks runtime; sem skill auto-detecção (que precisaria heurística frágil pra distinguir Abortado de natural).

### Localização do campo no body

`## Status` é H2 logo após `# Plano — <Título>` (antes de `## Contexto`). Razões:

- Visibilidade ao abrir o plano (above-the-fold).
- Matching simples: `grep -A1 "^## Status$" docs/plans/<slug>.md` retorna o estado corrente em 1 grep.
- H2 é convenção universal markdown — não exige frontmatter (que precisaria parser).

Forma canonical:

```markdown
## Status

Pendente
```

Valores aceitos (case-sensitive): `Pendente`, `Abortado`. **Não aceitos** no field: `Em execução` (redundante com git), `Concluído` (redundante com archive/+BACKLOG cadeia). Drift textual para valores não-aceitos → reviewer flag pré-merge.

Field ausente é estado válido — significa "git/forge canonical" (legacy sem field, plano em execução, ou pós-done).

### Wiring nas skills

- **`/triage` step 4** (caminho-com-plano): copia template + preenche `## Status` com `Pendente`. Single mutation no momento de criação (plano não existe em git ainda; sem worktree, sem race).
- **`/run-plan §3.4` (done)**: edit cirúrgico **remove** o bloco `## Status` (header + linha de valor) do plan body. Mesma sequência atômica do mark em `## Concluídos` do BACKLOG (já estabelecida em ADR-022 cadeia). Mutação localizada no done, antes de fechar a worktree.
- **`/run-plan §1` (entrada)**: **sem mutation**. Status field permanece `Pendente` durante execução; consumers cross-reference com worktree-active para inferir "Em execução" via precedência git. F3 resolvido — zero mutation point durante execução.
- **Operador (manual)**: edita `Status: Pendente` → `Status: Abortado` quando decide abandonar. Plano permanece em `docs/plans/`; `/next varrer` lista como Abortado; `/archive-plans` reporta como editorial (não arquiva — Abortado não é Concluído).
- **`/archive-plans`**: critérios atuais de ADR-022 preservados integralmente. Adiciona warning informativo "field=Pendente sem worktree há ≥4 semanas → possível órfão pré-execução, considerar editor manual" — não bloqueia, apenas reporta.
- **`/next varrer planos em aberto`** (item irmão a wirear via `/triage` step 4 do programa upstream): varredura paralela ao passo 4.5 lista planos por estado derivado via tabela de signal canonical acima.

### Interação com modos

- **Modo canonical** (default): `/triage` cria field na worktree; `/run-plan §3.4` remove field na worktree, parte do commit final. Sem race.
- **Modo runbook** (ADR-049 § Decisão (d), sem worktree): `/triage` cria field no main; `/run-plan §3.4` remove field no main, parte do commit final do runbook. Operação direta no main aceita por design do modo runbook; sem worktree pra divergir.
- **Modo local** (`paths.plans_dir: local`, ADR-047): plano gitignored em `.claude/local/plans/`; field criado/removido localmente, sem trace cross-session. Compatível com regra de não-referenciar (ADR-047 § Decisão (c)) — field interno ao body, sem leak no commit.
- **Modo forge backlog** (ADR-058): ortogonal. Field carrega state do plano (Pendente/Abortado); issue forge carrega state da feature (open/closed/assigned). Sem interação cruzada.

### Migração retroativa

1. **Arquivados (57 em `docs/plans/archive/2026-Q2/`)**: **nenhum backfill**. Presença em `archive/` já é signal canonical de Concluído per ADR-022 cadeia preservada. Sem mutação.

2. **Vigentes (68 em `docs/plans/`)**: editorial wave per-plano. Critério mecânico:
   - Worktree ativo OU PR aberto referenciando slug → `Em execução` derivado, **sem field**. Sem mutação.
   - Linha do backlog em `## Concluídos` (ADR-022 cadeia ok) → `Concluído` derivado, **sem field**. Sem mutação; `/archive-plans` futuro arquivará.
   - Sem worktree/PR + sem linha do backlog OR linha em `## Próximos` + commit recente referenciando slug → triage: provavelmente `Em execução` ou plano hand-written sem `/run-plan`. Operador decide.
   - Sem worktree/PR + plano sem trabalho em git OR órfão pré-execução (caso `session-audit-skill`) → adicionar `## Status: Pendente`.
   - Operador identifica plano abandonado → adicionar `## Status: Abortado`.

   Estimativa: ~30 planos exigem julgamento individual (30 sem `**Linha do backlog:**` ficam aí); ~1-2 min/plano = 30-60 min de trabalho total. Coberto pelo passo 3 do programa upstream (2026-06-12).

3. **Forward-only após migração**: `/triage` + `/run-plan` mantêm field sincronizado nos 2 pontos de mutação.

## Auto-aplicação per ADR-034

Per ADR-034 § Decisão, este ADR-060 satisfaz **cond 5** (sucessor parcial de ADR Aceito):

- ✓ **Cond 5 (sucessor parcial):** ADR-022 § Decisão é preservada na decisão central (6 critérios cumulativos de archival permanecem). Critério 3 (linha em `## Concluídos`) preservado integralmente — ADR-060 adiciona signal complementar (`## Status` field) para estados que ADR-022 não cobre (Pendente, Abortado), sem invalidar a cadeia de critérios. ADR-022 não é substituído nem revogado.
- ✗ **Cond 1 (decisão estrutural sem ancestral):** falsa — ADR-022 é ancestral direto.
- ✗ **Cond 2 (substitui ADR ancestral):** falsa — ADR-022 permanece Aceito e operacional.
- ✗ **Cond 3 (codifica restrição externa):** falsa.
- ✗ **Cond 4 (introduz categoria nova):** parcial — Status field é categoria nova, mas serve como complemento sob categoria existente (heurística de completude codificada em ADR-022). Cond 5 captura a substância mais precisamente.

ADR-022 recebe parágrafo cross-ref inline em § Decisão linha "critério 3" apontando para ADR-060 (per ADR-034 § Localização do adendo).

## Consequências

### Benefícios

- **Signal mecânico para órfão pré-execução** — caso `session-audit-skill` materializa em `Status: Pendente`; `/next varrer planos em aberto` torna visível.
- **Fronteira respeitada com ADR-049 § Decisão (a)** — field só carrega o que git/forge não captura. Em execução e Concluído derivados; sem duplicação.
- **Mutation no plan body reduzida a 2 pontos canonical** — criação e done. Sem mutation durante execução; F3 do design-reviewer resolvido. Worktree/runbook/local/forge interagem sem race articulada.
- **ADR-022 § Decisão preservada integralmente** — cadeia de 6 critérios intacta. ADR-060 é complemento, não substituição.
- **Custo de migração assimétrico bounded** — 57 arquivados zero; 68 vigentes ~30-60 min de editorial wave.
- **`/next varrer planos em aberto`** desbloqueado per dependência editorial do BACKLOG.
- **Compatibilidade com 4 modos** (canonical, runbook, local, forge) articulada sem assimetria material.

### Trade-offs

- **+1 campo opcional no template** — H2 + 1 linha de valor; ausente quando estado é derivado. Custo cosmético baixo.
- **Wiring em 2 skills (2 pontos)** — `/triage` step 4 (criar field=Pendente), `/run-plan §3.4` (remover field). Edits cirúrgicos; sem refactor maior.
- **Custo editorial wave bounded** — ~30 planos vigentes exigem julgamento individual; 30-60 min total. Materializado, não escondido.
- **Field stale possível durante execução** — `Status: Pendente` persiste no body com worktree ativo até `§3.4` remover. Aceito: consumers usam precedência git para inferir Em execução; field é leitura final, não state ativo.
- **Drift textual (valor inválido)** — operador pode escrever `Em execução` ou `Concluído` no field. Mitigação: reviewer (code/doc) flag pré-merge; template explicita "Valores aceitos no field: `Pendente`, `Abortado`".
- **Aborto sem ponto canonical** — depende de operador editar manualmente. Aceito; abortos são raros e operator-discretionary (per F3 análise do reviewer).

### Limitações

- **Não cobre transições inválidas no field** — texto livre no markdown. Mitigação via reviewer.
- **`Abortado` exige disciplina manual** — operador esquecer = plano fica `Pendente` indefinidamente. Mitigação: `/curate-backlog` H4 candidata futura (não codificada agora — sem 2ª ocorrência empírica).
- **Field absent é estado válido** — pode mascarar drift (operador removeu field por engano). Trade-off vs exigir field sempre presente: simplicidade do "git canonical quando field absent" supera.

## Alternativas consideradas

### (a-original) Status full state machine no body

State machine completa `Pendente | Em execução | Concluído | Abortado` no field, com `/run-plan §1` transicionando para `Em execução` e `/run-plan §3.4` para `Concluído`. **Descartada pelo design-reviewer** como contradição com ADR-049 § Decisão (a) (state-tracking de in-flight removido de markdown):

- `Em execução` redundante com worktree-active + PR aberto (signal já em git/forge).
- `Concluído` redundante com `archive/` presence + linha em `## Concluídos` (ADR-022 cadeia).
- Recria categoria que ADR-049 eliminou; introduz drift Status × realidade git/forge como trade-off explícito.
- Cria mutation point em `/run-plan §1` que cria race com worktree (cópia divergente do main; commitável; drift entre clones).

Cutucada operacional 2026-06-12: operador escolheu (a1) Status reduzido em vez desta variante.

### (b) Heurística por `git log --grep='plan: <slug>'` no main

Descartada. Pré-requisito: convenção de footer em commits do `/run-plan`. **Não existe hoje** — `skills/run-plan/SKILL.md` linha 134 não prescreve footer. Adoção exigiria edit do `/run-plan §3` + bulk rewrite de commits legacy ou aceitar gap legacy permanente. Mesmo com footer: signal não distingue `Concluído` de `Abortado` (ambos têm commits referenciando slug); recuperar distinção exigiria escrutínio + heurística sobre `done`/`abort` em messages. Frágil. Custo de adoção > ganho material.

### (b refinado) Heurística pura git/forge multi-signal

Descartada por cutucada 2026-06-12. Heurística multi-signal: worktree + PR + `archive/` + Linha do backlog + age. `Pendente` viável (plano committed sem worktree/PR/commits adicionais). `Abortado` **frágil** — sem signal explícito, heurística "age > X + nenhum signal recente" colapsa Abortado com plano simplesmente esquecido. Perde expressividade pra Abortado. Adere maximalmente a ADR-049 mas paga em precisão pra um dos 2 estados que justificam o ADR.

### (c) Presença em `archive/` como único signal

Descartada. Binary collapse: arquivado = `Concluído`; não-arquivado = ¬`Concluído`. Falha empiricamente: pós-`/archive-plans 2026-Q2` (`6e8fed5`), 68 vigentes são mix indistinguível de Concluído-com-gap-editorial + Pendente + Em execução + órfão. `archive/` presence não diferencia. Funcionaria SE `/archive-plans` fosse infalível — impossível sem editorial wave preencher `**Linha do backlog:**` em 30 planos. Mesmo após wave, perde expressividade pros estados `Em execução` e `Abortado`.

## Gatilhos de revisão

- **Drift Status × realidade ≥3 ocorrências em 6 meses** — `Status: Pendente` em plano com trabalho ativo em git por >2 semanas (operador não rodou `/run-plan §3.4`, ou skill falhou em remover). Sinal de que wiring em `/run-plan §3.4` está fraco; revisitar transição.
- **Operador esquece `Abortado` ≥3 ocorrências** — planos abandonados ficam `Pendente` indefinidamente, aparecendo em `/next varrer planos em aberto` como falsos positivos. Sinal de que ponto canonical para Abortado é necessário; revisitar (possibilidade: `/curate-backlog` H4 detectando staleness).
- **Migração retroativa subdimensionada** — se editorial wave do passo 3 do programa upstream (2026-06-12) deixar >10 planos vigentes em estado ambíguo após sessão, revisitar política (cap maior? fallback automático "Pendente" pra todos sem signal claro?).
- **Status field não consumido em produção** — se `/next varrer planos em aberto` (item irmão) **não for shipped** dentro de 2 ondas de migração doutrinal, reabrir ADR: campo sem consumidor real é cosmético; melhor reverter para ADR-022 signal-only.
- **Edits inválidos no field ≥3 ocorrências** — reviewer pega valor não-canonical (ex.: `Em execução`, `Concluído`, `WIP`) pré-merge ≥3 vezes; sinal de que validação leve (comentário inline no template) é insuficiente; considerar enum em frontmatter ou hook validador.
- **Cond 5 ADR-022 reaberta** — se cadeia editorial de ADR-022 (Linha do backlog × ## Concluídos) for substituída integralmente por outro mecanismo, ADR-060 vira ADR sem ancestral preservado; revisitar como sucessor total ou consolidar.
