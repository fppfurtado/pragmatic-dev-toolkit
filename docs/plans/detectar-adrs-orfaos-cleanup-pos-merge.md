# Plano — Detectar ADRs órfãos no cleanup pós-merge

## Contexto

Durante `/run-plan` Onda K (2026-06-01) foram detectados 6 ADRs órfãos no FS de `docs/decisions/` — versões pré-archive das Ondas I+J (ADR-011, 026, 027, 032, 038, 042) bloqueando setup da worktree. Causa-raiz suspeita: **drive-sync (rclone bisync) ressuscitando arquivos pós-merge** — quando uma onda arquiva um ADR via `git mv`, drive-sync replica o arquivo arquivado no FS local da máquina secundária, e numa próxima sincronização re-introduz a versão pré-archive como untracked. Investigação primária da causa-raiz vive em `meta-system/drive-sync` config (filters/excludes para archive paths git-managed); este plano cobre apenas a mitigação no toolkit lado, independente da causa-raiz.

**Mitigação manual atual:** `systemctl --user stop drive-sync.service` + `rm` dos órfãos antes de prosseguir. Funciona mas exige diagnóstico ad-hoc do operador a cada vez. Operador autorizou quebrar gating editorial "2º incidente" da linha BACKLOG por fragilidade latente (drive-sync.service segue parado desde a Onda K).

**Decisões fechadas neste plano:**

- **Placement (a):** adicionar detecção ao procedure `docs/procedures/cleanup-pos-merge.md`. Consumido automaticamente por `/triage` step 0 e `/release` pré-condições. `/run-plan` fica fora desta iteração — opt-in via plano-PR separado se 2º incidente emergir em runs que pulem `/triage`/`/release`. Caminho (b) (`/run-plan` pré-cond direta) e caminho (c) (ambos) rejeitados por YAGNI: procedure já existe e tem placement semântico óbvio (órfãos pós-merge = cleanup pós-merge).
- **Remediation (i):** aviso informativo + cutucada de remoção (paralelo ao pattern existente de cleanup-pos-merge.md cutucada por candidato). Caminho (ii) "bloquear + escrever em backlog" rejeitado: forte demais para `/triage` (pode bloquear triagem por algo recuperável); (i) mantém fluxo + dá visibilidade. Caminho (iii) auto-`rm` descartado upstream — risco material se órfão for ADR substantivo (não-archive) que operador esqueceu de trackear.
- **Cutucada batched (não sequencial):** uma cutucada inicial com opções `Remover todos os <N>` / `Cutucar individualmente` / `Manter todos (investigar)`. Constraint AskUserQuestion (2-4 opções) impede listar 6 órfãos como opções multi-select diretamente; batched scale para qualquer N. **Sem `(Recommended)` em nenhuma das 3 opções** — per CLAUDE.md AskUserQuestion mechanics ("Recommended só quando default estatisticamente estável"), 1 incidente fundador é sinal insuficiente para fixar dominância; postura epistemicamente honesta mitiga risco operador-por-reflexo.
- **Mitigação edge case `/new-adr` cross-turn:** aviso informativo lista **filenames concretos** dos órfãos detectados antes da cutucada (paralelo ao pattern cutucada-com-referrer concreto do `/run-plan` §3.3) — operador vê `ADR-NNN-recem-criado.md` e reconhece se algum é ADR válido criado em sessão prévia, não confunde com órfão archive. Caminho (a) cross-ref textual e caminho (c) timestamp check rejeitados — (b) listagem de filenames é mecânica robusta de baixíssimo custo.

**Scope fixo:** detecção pelo pattern `^\?\? <decisions_dir>/ADR-` (ADRs untracked no decisions_dir resolvido). Sem expansão para outros paths arquivados (escopo do incidente observado).

**Linha do backlog:** plugin: avaliar step preventivo de detecção de ADRs órfãos em `docs/decisions/` em `/run-plan` pré-loop ou `/triage` step 0 cleanup pós-merge — durante `/run-plan` Onda K (2026-06-01) detectados 6 ADRs órfãos do FS (versões pré-archive das Ondas I+J: 011/026/027/032/038/042) bloqueando setup. Causa-raiz suspeita: **drive-sync (rclone bisync) ressuscitando arquivos pós-merge** (ondas C-H sem registro; investigação primária vive no meta-system/drive-sync config — filters/excludes para archive paths git-managed). Mitigação imediata: `systemctl --user stop drive-sync.service` + `rm` dos órfãos antes de prosseguir. Toolkit pode prevenir bloqueio em runs futuros independente da causa-raiz via detecção `git status --porcelain | grep -E '^\?\? <decisions_dir>/ADR-'` no `/run-plan` setup ou `/triage` step 0. Reavaliar se segundo incidente em outra onda emergir; sem ele, editorial pendente.

**ADRs candidatos:** ADR-047 (resolution protocol — papel `decisions_dir` resolution + modo local), ADR-051 § Decisão (c) (categoria `docs/procedures/` estabelecida).

## Resumo da mudança

Adicionar nova seção `## Detecção de ADRs órfãos no decisions_dir` em `docs/procedures/cleanup-pos-merge.md` como nova top-level (após `## Após todos os candidatos` linha 41-43). Atualizar parágrafo inicial (linha 5) para mencionar que o procedure cobre 2 tipos de cleanup pós-merge: worktrees mergeadas + ADRs órfãos.

**Algoritmo da nova seção:**

1. Resolver papel `decisions_dir` (default `docs/decisions/`; modo `local` resolve para `.claude/local/decisions/`).
2. Executar `git status --porcelain` e filtrar por pattern `^\?\? <decisions_dir-resolvido>/ADR-` (ADRs untracked no decisions_dir resolvido — `<decisions_dir-resolvido>` é placeholder substituído em runtime pelo path concreto via Resolution protocol: canonical `docs/decisions/`, modo `local` `.claude/local/decisions/`, ou custom declarado em `paths.decisions_dir`). Em modo `local`, `.claude/local/decisions/` é gitignored — `git status --porcelain` não emite entries para paths gitignored, então grep retorna vazio sempre; skip silente automático sem branch especial.
3. Sem matches → skip silente.
4. Com matches → emitir aviso informativo listando os **filenames concretos** detectados (ex.: `ADR-011-..., ADR-026-..., ADR-027-...`) — não apenas count abstrato. Operador vê os paths reais e reconhece se algum é ADR válido recém-criado via `/new-adr` em sessão prévia (mitigação do edge case `/new-adr` cross-turn; paralelo ao pattern cutucada-com-referrer concreto do `/run-plan` §3.3). Em seguida, cutucada batched:
   - `AskUserQuestion` header `ADR órfão`
   - question: `"<N> ADR(s) órfão(s) detectado(s) — drive-sync ressuscitou pós-archive? Como resolver?"`
   - opções (sem `(Recommended)` — default estatisticamente instável com 1 incidente fundador apenas): `Remover todos os <N>` (executa `rm` em cada path) / `Cutucar individualmente` (loop com cutucada por órfão `Remover` / `Manter`) / `Manter todos (investigar)` (skip todos)
   - Other → operador descreve em prosa (ad-hoc subset OR investigation)
5. Aplicar seleção; retornar controle à skill consumidora.

Skip silente quando não há ADRs órfãos (caso comum); não incomoda no caminho-feliz.

## Arquivos a alterar

### Bloco 1 — Detecção de ADRs órfãos em cleanup-pos-merge.md procedure {reviewer: doc}

- `docs/procedures/cleanup-pos-merge.md`:
  - Atualizar parágrafo inicial (linha 5 atual) para indicar que procedure cobre 2 tipos de cleanup pós-merge: worktrees mergeadas + ADRs órfãos no `decisions_dir`.
  - Adicionar nova seção H2 `## Detecção de ADRs órfãos no decisions_dir` após `## Após todos os candidatos` (após linha 43 atual).
  - Conteúdo da nova seção: algoritmo per Resumo da mudança (5 passos), incluindo notas sobre modo `local` (skip silente automático via gitignored) e edge case de criação ativa de ADR via `/new-adr` (cobertura em Notas operacionais abaixo).

## Verificação end-to-end

Inspeção textual (sem suite — `test_command: null`):

```bash
# Nova seção H2 presente
grep -n "^## Detecção de ADRs órfãos" docs/procedures/cleanup-pos-merge.md
# Esperado: 1 match (header H2 da nova seção).

# Parágrafo inicial atualizado para mencionar ambos os tipos
grep -E "worktrees mergeadas|ADRs órfãos" docs/procedures/cleanup-pos-merge.md | head -3
# Esperado: ≥2 matches (parágrafo inicial + nova seção).

# Algoritmo cobre os elementos-chave
grep -E "git status --porcelain|AskUserQuestion|skip silente|decisions_dir" docs/procedures/cleanup-pos-merge.md
# Esperado: cada keyword presente ao menos uma vez na nova seção (e nas seções pré-existentes para skip silente).

# Modo local mencionado explicitamente
grep -E "modo .local.|paths\.decisions_dir|gitignored" docs/procedures/cleanup-pos-merge.md
# Esperado: ≥1 match na nova seção (cobertura do caso local).
```

## Verificação manual

Surface não-determinística — fluxo runtime de `/triage` step 0 / `/release` pré-cond que consome procedure. Cenários:

1. **Sem órfãos (caso comum):** Repositório limpo em `docs/decisions/`. Invocar `/triage <intent>` ou `/release`. Esperado: step 0/pré-cond dispara procedure; nova seção não emite output (skip silente per algoritmo passo 3).

2. **Com órfão único:** Simular órfão via `touch docs/decisions/ADR-999-fixture-orfao.md` (untracked). Invocar `/triage <intent>`. Esperado: aviso "1 ADR órfão detectado" + cutucada batched com 3 opções. Selecionar `Remover todos os 1` → arquivo deletado. Limpar fixture: `rm -f docs/decisions/ADR-999-fixture-orfao.md`.

3. **Múltiplos órfãos batched-remove:** Simular 3 órfãos (ADR-997/998/999). Invocar `/triage <intent>`. Esperado: aviso "3 ADRs órfãos detectados" + cutucada batched. Selecionar `Remover todos os 3` → 3 arquivos deletados em batch.

4. **Múltiplos órfãos individual:** Simular 3 órfãos. Invocar `/triage <intent>`. Esperado: cutucada batched. Selecionar `Cutucar individualmente` → 3 cutucadas sequenciais `Remover` / `Manter`. Misturar selections (1 remover, 1 manter, 1 remover) — esperado aplicação correta de cada.

5. **Múltiplos órfãos manter-todos:** Simular 3 órfãos. Invocar `/triage <intent>`. Esperado: cutucada batched. Selecionar `Manter todos (investigar)` → todos preservados. Operador limpa manualmente após investigar.

6. **Modo local (`paths.decisions_dir: local`):** Configurar CLAUDE.md com `paths.decisions_dir: local`. Simular órfão em `.claude/local/decisions/ADR-999-test.md`. Invocar `/triage <intent>`. Esperado: skip silente (modo local artefatos são gitignored; `^??` pattern não casa por gitignore).

## Notas operacionais

- Cleanup-pos-merge.md procedure também é consumido por `/release` pré-condições (não apenas `/triage` step 0). Mudança propaga automaticamente — sem edit em `/release` SKILL.md.
- `/run-plan` NÃO consome este procedure; fica fora desta iteração. Se 2º incidente emergir em /run-plan-only flow (operador pula /triage e /release antes do /run-plan), abrir plano-PR separado adicionando como pré-condição própria de /run-plan ou estendendo o procedure para uso compartilhado.
- Pattern `^\?\? <decisions_dir>/ADR-` é lexical e pode produzir falso positivo se operador estiver ATIVAMENTE criando novo ADR (untracked durante `/new-adr` flow). Mitigação: durante `/new-adr`, o arquivo é criado mas não há invocação de `/triage`/`/release` no mesmo turno (skill termina + devolve controle); falso positivo só dispara em invocação subsequente de `/triage`/`/release`, onde o operador já confirmou a existência do novo ADR. Custo aceito; alternativas (parsing git log, timestamp checks) são over-engineering.
- Investigação primária da causa-raiz (drive-sync filters/excludes para archive paths git-managed) permanece responsabilidade do `meta-system` config; este plano cobre apenas mitigação toolkit-side independente da causa-raiz.
- Bloco único `{reviewer: doc}` — edit é puramente documental (procedure file `.md`); sem código de produção; sem test pattern envolvido.

## Decisões absorvidas

- algoritmo step 2: clarificado que `<decisions_dir-resolvido>` é placeholder substituído em runtime via Resolution protocol (canonical `docs/decisions/`, local `.claude/local/decisions/`, ou custom declarado em `paths.decisions_dir`) (caminho-único).
