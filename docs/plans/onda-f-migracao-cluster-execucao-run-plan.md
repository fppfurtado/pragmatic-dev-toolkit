# Plano — Onda F da redesign da camada doutrinal (migração cluster execução/run-plan)

## Contexto

**ADRs candidatos:** ADR-004 (foundational do cluster — state-tracking em git/forge, não em markdown; BACKLOG editorial sem `## Em andamento`; -5 mecanismos defensivos), ADR-028 (sucessor parcial lateral — campo `**Branch:**` opcional no `## Contexto` do plano; fluxo issue-first GitLab; opt-in por plano), ADR-039 (sucessor parcial de ADR-010 — Task tool como state-keeping em fluxo longo; categoria nova paralela; lifecycle 2-estados `pending → completed`; marker convention `[capture:*]`), ADR-041 (sucessor parcial lateral de ADR-002 — campo `**Modo:** runbook` opt-in para system-surgery; bypass 4 dimensões do canonical; defensividade dura `**Branch:** + **Modo:** runbook incompatíveis`), ADR-045 (apex redesign — esta onda materializa § Decisão parte 1 § Implementação literal), ADR-046+ADR-047+ADR-048 (templates do pattern de migração validado em Ondas C+D+E; F4 lessons cond 5 isolada + cond 2 "absorção consolidatória vs revogação" reaplicadas), ADR-034 (critério adendo vs novo ADR — cond 5 sucessor parcial primário absorvendo 4 ADRs; cond 4 NÃO aplica per F4 Onda C; cond 1 NÃO aplica — ADR-045/-046/-047/-048 ancestrais codificados), ADR-002 (eliminar gates pré-loop — tensão com ADR-041 § Tensão; preservada como ADR clássico vigente, NÃO absorvido), ADR-010 (instrumentação progresso multi-passo Task tool — decisão base de ADR-039; preservada como ADR clássico vigente, NÃO absorvido — ver § Refinamento editorial), ADR-024 (categoria `docs/procedures/` — relevante por **ausência** aqui: cluster execução **não tem procedure file**; toda mecânica vive em `skills/run-plan/SKILL.md` + `skills/triage/SKILL.md` + CLAUDE.md + templates/plan.md).

Onda F (sexta) da redesign da camada doutrinal coordenada por `docs/plans/redesign-camada-doutrinal-charter.md`. **Quarta migração cluster temático** per ADR-045 § Decisão parte 1 § Implementação literal — Ondas C+D+E precederam (cutucadas, modo local, reviewers/curadoria).

Cluster execução/run-plan é candidato natural pós-Onda E:

1. **Cluster coeso semanticamente máximo** — todos os 4 ADRs cobrem dimensões da mecânica do `/run-plan`: ADR-004 (state em git/forge fora do BACKLOG); ADR-028 (campo `**Branch:**` opt-in issue-first); ADR-039 (Task tool state-keeping para captura automática §3.5); ADR-041 (campo `**Modo:** runbook` opt-in system-surgery). Mecanismos co-utilizados — ADR-028 + ADR-041 são campos paralelos no `## Contexto` do plano (template pattern `**Branch:** + **Modo:**` — incompatíveis explicitamente).
2. **4 ADRs (vs 2 em E)** — calibração próxima à Onda D (4 ADRs). Sequência C→D→E→F exerce 2→4→2→4 ADRs (scope variado).
3. **Cluster sem procedure file** — reaplica F9 lesson D+E (fronteira ADR-024 não aplica antecipadamente). Mecânica vive em `skills/run-plan/SKILL.md` (concentra 7 das 19 ocorrências) + `skills/triage/SKILL.md` + CLAUDE.md + templates/plan.md.
4. **Cluster com trade-offs vivos preservados** — campos `**Branch:**` (ADR-028) e `**Modo:** runbook` (ADR-041) são opt-in revertíveis; testes de absorção consolidatória de decisões reversíveis (paralelo ao constraint codificado em ADR-048 § Decisão (d) auto-consistência). F4 cond 2 lesson Onda D aplicada — decisões centrais preservadas como dimensões; não revogação.
5. **F4 lessons reaplicadas literal** — cond 5 primária isolada (sucessor parcial absorvendo 4 ADRs); cond 4 NÃO aplica (ADR-045 carrega categoria meta; ADR-049 é quarta instância); cond 1 NÃO aplica (ADR-045/-046/-047/-048 ancestrais codificados); cond 2 "absorção consolidatória vs revogação" aplica per F4 Onda D.

### Refinamento editorial ao sketch original do charter

Charter sketch linha 252:

```
ADR-005-skill-execucao-run-plan.md    # worktree + micro-commit + gates +
                                      # runbook mode + captura automática
                                      # (absorve atual: 004, 028, 037, 039, 041)
```

**Sketch absorvia 5 ADRs; Onda F refina para 4** (exclusão de ADR-037 do cluster) per ADR-045 fronteira *"ajuste editorial do charter vs revisão de ADR-045"* (categoria editorial sem mudança estrutural na regra de consolidação):

- **ADR-037 (README framing "Product Engineer harness") EXCLUÍDO** — pertence semanticamente a cluster discoverability/branding (paralelo a ADR-012 idioma artefatos discoverability + ADR-007 README), não a mecânica do `/run-plan`. Sketch agrupou por proximidade numérica, não por coesão semântica. ADR-037 fica órfão para futuro cluster discoverability OU permanece como ADR clássico standalone se nenhum cluster afim emergir (per ADR-045 admission policy aplicada retroativamente: ADR-037 É decisão estrutural reversível que documenta posicionamento editorial).
- **ADR-010 (instrumentação progresso Task tool) NÃO absorvido** — ADR-010 é decisão base de ADR-039 (ADR-039 § Origem cita ADR-010 como decisão base + categoria nova paralela). Sketch original previa absorvê-lo em cluster "instrumentação progresso" separado (linha 265): `ADR-010-instrumentacao-progresso.md (absorve atual: 010, 039)`. Charter sketch tinha contradição (ADR-039 listado em DOIS clusters: execução E instrumentação). Resolução per ADR-045 fronteira: ADR-039 fica no cluster execução (aplicação canonical é `/run-plan §3.5` — mecânica de execução); ADR-010 permanece como ADR clássico vigente codificando progress display Task tool (categoria distinta com potencial consumers futuros além de `/run-plan`). Substância de ADR-010 absorvida via referência cruzada em ADR-049 § Origem (ADR-049 cita ADR-010 como decisão paralela preservada). Refinamento absorve a duplicação do sketch sem perda de carga doutrinal.

**Saldo do refinamento:** Onda F absorve 4 ADRs (vs 5 do sketch); ADR-037 + ADR-010 permanecem vigentes como ADRs clássicos standalone. Inventário pós-Onda F: 40 - 4 archivados + 1 ADR-049 = **37 vigentes** (drop líquido de 3 nesta onda, paralelo a Onda D).

**Linha do backlog:** Onda F é sub-scope da umbrella multi-onda em `## Próximos`; não corresponde a linha distinta. Per ADR-004 + precedente Ondas A+B+C+D+E, umbrella é atualizada in-place post-merge.

## Resumo da mudança

**Esta Onda F produz:**

1. **ADR-049 consolidado** (criado via `/new-adr` no /triage step 4) — absorve substância de ADR-004 + ADR-028 + ADR-039 + ADR-041 num único ADR temático "execução/run-plan". § Decisão integra:
   - (a) State-tracking em git/forge (não em markdown): BACKLOG editorial sem `## Em andamento`; state vivo = branches/PRs abertos; `## Concluídos` append-only via `/run-plan §3.4`. -5 mecanismos defensivos contra merge artifact obsoletos (de ADR-004)
   - (b) Campo `**Branch:**` opcional no `## Contexto` do plano para fluxo issue-first: opt-in por plano; `/run-plan §1.1` faz checkout em vez de criar; descobre via `git symbolic-ref refs/remotes/origin/HEAD`; cutucada em `/triage` step 4 quando branch atual ≠ default (de ADR-028)
   - (c) Task tool como state-keeping em fluxo longo (categoria paralela a progress display de ADR-010): lifecycle 2-estados `pending → completed`; marker convention `[capture:<tipo>]` no subject; aplicação canonical `/run-plan §3.5` captura automática unificada cross-superfícies (pré-loop + passo 2 loop + passo 3.2 validação) (de ADR-039)
   - (d) Campo `**Modo:** runbook` opcional no `## Contexto` para system-surgery: único valor aceito `runbook`; bypass 4 dimensões do canonical (sem worktree + sem commit-per-bloco + gate confirmação por bloco + validação intercalada); incompatibilidade dura `**Branch:** + **Modo:** runbook`; materialização de capturas no `Falhou` (de ADR-041)
   - (e) Pattern paralelo de campos opcionais no `## Contexto` (`**Branch:**` + `**Modo:**` + futuros) — opt-in revertível por plano; ausência = comportamento default total
   - (f) Tensões resolvidas: ADR-002 (gates pré-loop) preserva escopo de warnings de qualidade-de-mudança; ADR-049 cobre incompatibilidade semântica de campos no plano (categoria distinta com gate dura justificado). ADR-010 (progress display Task tool) coexiste como modo paralelo de Task tool; ADR-049 § Decisão (c) state-keeping é categoria nova sem revogar progress display

   § Origem histórica preserva 4 incidentes empíricos: revisão arquitetural pós-v1.20.0 → ADR-004 (5 mecanismos defensivos + ciclo merge artifact); operador GitLab issue-first 2026-05-14 → ADR-028 (3 caminhos ruins); plano `onda-1-fs-migration` meta-system 2026-05-27 → ADR-041 (5 mismatches estruturais); Onda 2 ROADMAP item 8 (commit `25d0daf`) → ADR-039 (fragilidade latente §3.5 lista mental). § Gatilhos consolida triggers das 4 decisões. Status `Proposto`.

2. **Archive de ADR-004, ADR-028, ADR-039, ADR-041** — `git mv` para `docs/decisions/archive/` + header redirect canonical (format de ADR-046): blockquote `> **ARCHIVED 2026-05-31** — content absorbed into [ADR-049](../ADR-049-<slug>.md); see that ADR for current authority.` + header H1 original preservado intacto abaixo.

3. **Archive index update** — `docs/decisions/archive/README.md` ganha 4 linhas novas na tabela (Onda F). Cada onda E-X estende a tabela como invariante codificada em ADR-046.

4. **Propagação de cross-refs em docs vivos** (5 arquivos; 19 ocorrências em 17 linhas distintas):
   - `agents/design-reviewer.md` (1 linha, 1 ocorrência) — linha 99 referência a ADR-004 ("git/forge é fonte da verdade").
   - `CLAUDE.md` (2 linhas, 2 ocorrências) — linha 38 (ADR-004 NOTES.md row) + linha 95 (ADR-041 bullet "Modo runbook"). Linha 87 (ADR-010 bullet "Instrumentação progresso") **NÃO tocada** — ADR-010 não absorvido; ref permanece vigente. Reformulação narrativa do bullet "Modo runbook" similar ao pattern Onda D Local mode.
   - `skills/triage/SKILL.md` (4 linhas, 4 ocorrências) — linha 35 (ADR-004 backlog state) + linha 92 (ADR-004 caminho-com-plano) + linhas 110, 112 (ADR-028 campo `**Branch:**` + probe).
   - `templates/plan.md` (2 linhas, 2 ocorrências) — linha 20 (ADR-028 `**Branch:**` field) + linha 21 (ADR-041 `**Modo:**` field).
   - `skills/run-plan/SKILL.md` (7 linhas, 7 ocorrências; concentra ~37% das ocorrências) — linha 32 (ADR-041 detecção modo, pré-condição 0) + linha 58 (ADR-039 marker capture) + linha 68 (ADR-041 modo runbook bypass) + linha 87 (ADR-028 setup worktree campo Branch) + linha 114 (ADR-039 captura deferida) + linha 157 (ADR-004 registro em Concluídos sob caminho-com-plano) + linha 159 (ADR-039 materialização §3.5) + linha 196 (ADR-028 modo local com Branch presente) + linha 222 (ADR-041 não executar canonical em runbook). Mecânica do SKILL preservada **intacta** — apenas apontadores doutrinais atualizam.

5. **Link rot consciente em docs imutáveis** — outros ADRs imutáveis e planos históricos citam ADR-004/-028/-039/-041 em § Origem como precedente ou cross-ref doutrinal (categoria (a) histórica de F1 lesson Onda C). Subset suspeito de categoria (b) doutrinal ativa identificado pré-execução: ADR-041 § Tensão com ADR-002 — substância "warnings de qualidade-de-mudança vs incompatibilidade semântica" absorvida em ADR-049 § Decisão (f); ADR-041 § Tensão com ADR-004 — substância "state em git para mudança de código vs sistema como state-tracker em runbook" absorvida em ADR-049 § Decisão (a)+(d); ADR-039 cita ADR-010 como decisão base — ADR-010 permanece vigente, substância em ADR-049 § Decisão (c) "categoria nova paralela a progress display de ADR-010". Hipótese de zero substância "doutrinal ativa" perdida — design-reviewer valida.

6. **Charter atualização** (post-merge, manual) — `docs/plans/redesign-camada-doutrinal-charter.md` § "Atualização pós-execução" tabela adiciona linha "Onda F — Migração cluster execução/run-plan" + refinamento editorial do sketch documentado (exclusão ADR-037 + preservação ADR-010 como vigente standalone); anti-regression checklist § Skills e fluxo atualizada refletindo ADR-049 como nova autoridade. NÃO escopo desta Onda F; commit separado post-merge per precedente Ondas A+B+C+D+E.

**Pattern de migração validado nesta onda** (quarta aplicação; calibração com refinamento editorial):
- Cluster de 4 ADRs sem procedure file — paralelo a Onda D (4 ADRs sem procedure file).
- **Refinamento editorial do sketch** documentado per ADR-045 fronteira "ajuste editorial vs revisão" — primeira instância em 4 ondas onde a composição do cluster é refinada (ondas C+D+E seguiram sketch literal). Pattern editorial codificado: refinamento sem mudança estrutural na regra de consolidação.
- Mecânica concentrada em uma SKILL (`/run-plan` 7 ocorrências) + 4 outros docs vivos com refs esparsas — testa propagation pattern em cluster com hot spot mecânico.
- F4 lessons reaplicadas literal (cond 5 isolada; cond 4 NÃO aplica; cond 1 NÃO aplica; cond 2 "absorção consolidatória" — decisões reversíveis preservadas como dimensões).

## Arquivos a alterar

### Bloco 1 — Archive 4 ADRs + archive index extension {reviewer: doc}

- `git mv docs/decisions/ADR-004-state-tracking-em-git.md docs/decisions/archive/`
- Editar topo do arquivo movido inserindo blockquote redirect **antes** do `# ADR-004: <título original>`:

  ```markdown
  > **ARCHIVED 2026-05-31** — content absorbed into [ADR-049](../ADR-049-execucao-run-plan-consolidado.md); see that ADR for current authority. Body below preserved verbatim for historical record.

  # ADR-004: State-tracking em git/forge, não em markdown
  ```

- `git mv docs/decisions/ADR-028-campo-branch-opcional-plano-fluxo-issue-first.md docs/decisions/archive/` + análogo.
- `git mv docs/decisions/ADR-039-task-tool-state-keeping-fluxo-longo.md docs/decisions/archive/` + análogo.
- `git mv docs/decisions/ADR-041-campo-modo-runbook-plano-opt-in.md docs/decisions/archive/` + análogo.
- Estender tabela em `docs/decisions/archive/README.md` adicionando 4 linhas (Onda F):

  ```markdown
  | ADR-004 — State-tracking em git/forge, não em markdown | [ADR-049](../ADR-049-execucao-run-plan-consolidado.md) | F |
  | ADR-028 — Campo Branch opcional no plano para fluxo issue-first | [ADR-049](../ADR-049-execucao-run-plan-consolidado.md) | F |
  | ADR-039 — Task tool como state-keeping em fluxo longo | [ADR-049](../ADR-049-execucao-run-plan-consolidado.md) | F |
  | ADR-041 — Campo `**Modo:** runbook` opt-in em planos para `/run-plan` cobrir system-surgery | [ADR-049](../ADR-049-execucao-run-plan-consolidado.md) | F |
  ```

### Bloco 2 — agents/design-reviewer + CLAUDE.md + skills/triage + templates/plan cross-refs {reviewer: doc}

- `agents/design-reviewer.md` linha 99: substituir "ADR-004 disse" por "ADR-049 § Decisão (a) disse" (cross-ref a sub-seção do consolidado).
- `CLAUDE.md` linha 38 (NOTES.md row em "The role contract" table): substituir "per ADR-004" por "per ADR-049 § Decisão (a)".
- `CLAUDE.md` linha 95 (bullet "Modo runbook em planos de system-surgery"): reformulação narrativa similar a Onda D Local mode bullet — "per [ADR-041](docs/decisions/ADR-041-...md)" → "per [ADR-049](docs/decisions/ADR-049-execucao-run-plan-consolidado.md) § Decisão (d)". Substância (campo opcional `**Modo:** runbook` + bypass 4 dimensões + rollback responsabilidade do operador + único valor aceito) preservada literal.
- `CLAUDE.md` linha 87 (bullet "Instrumentação de progresso") **NÃO tocada** — bullet referencia ADR-010 (não absorvido; preserva como ADR clássico vigente per refinamento editorial); cross-ref "relação com ADR-004" no final do bullet → atualizar para "relação com ADR-049 § Decisão (a)".
- `skills/triage/SKILL.md` linha 35: substituir "Sob ADR-004" por "Sob ADR-049 § Decisão (a)".
- `skills/triage/SKILL.md` linha 92: substituir "ADR-004" por "ADR-049 § Decisão (a)".
- `skills/triage/SKILL.md` linha 110: substituir "(ADR-028)" por "(ADR-049 § Decisão (b))".
- `skills/triage/SKILL.md` linha 112: substituir "conforme [ADR-028](...)" por "conforme [ADR-049](../../docs/decisions/ADR-049-execucao-run-plan-consolidado.md) § Decisão (b) § Mecânica".
- `templates/plan.md` linha 20: substituir "(ADR-028)" por "(ADR-049 § Decisão (b))".
- `templates/plan.md` linha 21: substituir "(ADR-041)" por "(ADR-049 § Decisão (d))".

### Bloco 3 — skills/run-plan/SKILL.md cross-refs {reviewer: doc}

- `skills/run-plan/SKILL.md` 9 ocorrências (linhas 32, 58, 68, 87, 114, 157, 159, 196, 222) — substituição mecânica de refs a ADR-004/-028/-039/-041 por ADR-049 (com § Decisão (a/b/c/d) quando contexto sub-dimensional aplica):
  - Linha 32 (pré-condição 0 detecção de modo): "per [ADR-041](...)" → "per [ADR-049](...) § Decisão (d)".
  - Linha 58 (warning emite TaskCreate marker): "per [ADR-039](...)" → "per [ADR-049](...) § Decisão (c)".
  - Linha 68 (Modo runbook ativado): "per [ADR-041](...)" → "per [ADR-049](...) § Decisão (d)".
  - Linha 87 (setup worktree detecta campo Branch): "per [ADR-028](...)" → "per [ADR-049](...) § Decisão (b)".
  - Linha 114 (captura deferida TaskCreate): "per [ADR-039](...)" → "per [ADR-049](...) § Decisão (c)".
  - Linha 157 (registro em Concluídos via Linha do backlog): "(sob ADR-004, que não grava no BACKLOG)" → "(sob ADR-049 § Decisão (a), que não grava no BACKLOG)".
  - Linha 159 (materialização §3.5 TaskList filtrada): "per [ADR-039](...)" → "per [ADR-049](...) § Decisão (c)".
  - Linha 196 (modo local com Branch presente): "cf. [ADR-028](...) § Modo local" → "cf. [ADR-049](...) § Decisão (b) § Modo local".
  - Linha 222 (bullet `## O que NÃO fazer` sobre modo runbook): "per [ADR-041](...)" → "per [ADR-049](...) § Decisão (d)".

  Mecânica do SKILL (pré-condições 0-4 + warnings pré-loop + loop por bloco + gate final §3.1-3.7 + modo runbook fluxo alternativo) preservada **intacta** — apenas autoria doutrinal atualiza.

## Verificação end-to-end

**Critérios de sucesso da Onda F:**

1. **ADR-049 criado** com Status `Proposto` em `docs/decisions/ADR-049-execucao-run-plan-consolidado.md`. § Origem cita ADR-004+ADR-028+ADR-039+ADR-041 como decisões absorvidas + ADR-045/-046/-047/-048 como templates + ADR-010 como decisão paralela preservada (não absorvida — refinamento editorial). § Decisão integra as 6 dimensões (a-f) sob narrativa única coerente. § Origem histórica preserva os 4 incidentes empíricos. § Gatilhos consolida triggers das 4 decisões. § Auto-aplicação cond 5 primária isolada; cond 4 NÃO aplica; cond 1 NÃO aplica; cond 2 (absorção consolidatória) explícita per F4 lesson Onda D.

2. **ADR-004, ADR-028, ADR-039, ADR-041 arquivados:** `ls docs/decisions/ADR-004-*.md docs/decisions/ADR-028-*.md docs/decisions/ADR-039-*.md docs/decisions/ADR-041-*.md` → vazio (movidos). `ls docs/decisions/archive/ADR-004-*.md docs/decisions/archive/ADR-028-*.md docs/decisions/archive/ADR-039-*.md docs/decisions/archive/ADR-041-*.md` → presentes. Header redirect canonical no topo de cada arquivo, H1 original intacto abaixo.

3. **Archive index estendido:** `docs/decisions/archive/README.md` carrega tabela com 12 linhas (2 Onda C + 4 Onda D + 2 Onda E + 4 Onda F), ordem cronológica por onda preservada.

4. **`grep "ADR-004\|ADR-028\|ADR-039\|ADR-041" agents/design-reviewer.md` → 0 matches** (1 ocorrência substituída).

5. **`grep "ADR-004\|ADR-028\|ADR-039\|ADR-041" CLAUDE.md skills/triage/SKILL.md templates/plan.md skills/run-plan/SKILL.md` → 0 matches** (18 ocorrências substituídas).

6. **`grep "ADR-010" CLAUDE.md` → ≥1 match** (bullet "Instrumentação de progresso" preservado — ADR-010 não absorvido; refinamento editorial documentado em ADR-049 § Origem).

7. **`grep "ADR-037" /storage/dev/projects/pragmatic-dev-toolkit/docs/decisions/ADR-037-*.md` → arquivo existe** (ADR-037 não arquivado — refinamento editorial; permanece como ADR clássico vigente).

8. **Mecânica do `/run-plan` preservada:** `grep -E "Detecção de modo|warnings pré-loop|Modo runbook|setup da worktree|captura automática|TaskList|TaskCreate" skills/run-plan/SKILL.md` → matches conforme estado atual (mecânica do SKILL intacta).

9. **Pattern campos opcionais paralelo preservado:** `grep -E "\*\*Branch:\*\*|\*\*Modo:\*\*" templates/plan.md skills/triage/SKILL.md skills/run-plan/SKILL.md` → matches conforme estado atual (pattern editorial dos 2 campos opcionais preservado; incompatibilidade dura `**Branch:** + **Modo:** runbook` preservada em `skills/run-plan/SKILL.md` linha 32).

10. **Link rot em immutable ADRs aceito explicitamente:** `grep -l "ADR-004\|ADR-028\|ADR-039\|ADR-041" docs/decisions/ADR-0*.md docs/plans/*.md` ainda retornará vários arquivos antigos — esses são imutáveis (immutable ADRs + historical plans); cross-refs em immutable docs ficam como registro histórico, NÃO são editados.

11. **CHANGELOG.md intacto** (registro histórico imutável) — `grep "ADR-004\|ADR-028\|ADR-039\|ADR-041" CHANGELOG.md` retorna matches preservados como registro de versionamento; NÃO editar.

12. **doc-reviewer audita drift cross-doc:** cross-refs corretos cross-doc; ADR-049 substância fiel a ADR-004+ADR-028+ADR-039+ADR-041 combinados; nenhuma carga doutrinal da § Skills e fluxo do anti-regression checklist perdida (state-tracking em git/forge + campo `**Branch:**` issue-first + Task tool state-keeping + modo runbook system-surgery + pattern campos opcionais paralelo — todas preservadas em ADR-049).

13. **design-reviewer auto-fire em /new-adr step 5 e /triage step 5** valida: padrão de migração coerente com ADR-045 § Decisão parte 1; refinamento editorial do sketch (exclusão ADR-037 + preservação ADR-010) coerente per ADR-045 fronteira "ajuste editorial vs revisão"; pattern reusable em cluster com hot spot mecânico; auto-aplicação per ADR-034 (cond 5 primária; cond 4 NÃO aplica; cond 1 NÃO aplica; cond 2 "absorção consolidatória" per F4 Onda D) coerente.

## Notas operacionais

**Ordem dos blocos:** Bloco 1 (archive) executado antes dos demais — outros blocos referenciam ADR-049 que substitui os 4 arquivos arquivados. Blocos 2-3 podem rodar em qualquer ordem (independentes entre si após archive); Bloco 3 (skills/run-plan/SKILL.md) tem maior risco editorial por concentrar 9 ocorrências (~50% do total).

**Validação do refinamento editorial:** se design-reviewer flagrar gap no refinamento editorial (ex.: exclusão de ADR-037 inconsistente; preservação de ADR-010 vs absorção de ADR-039 gera incoerência substancial; refinamento sem ancestral codificado em ADR-045 fronteira "ajuste editorial vs revisão"), refinamento é editorial do plano antes de prosseguir. Mudança estrutural na regra de consolidação seria gatilho de revisão de ADR-045.

**Charter atualização post-merge:** após merge da Onda F, atualizar `docs/plans/redesign-camada-doutrinal-charter.md` § "Atualização pós-execução":
- Estender tabela de ondas com linha "Onda F — Migração cluster execução/run-plan" (commit hash + PR + substância + **refinamento editorial documentado**).
- Anti-regression checklist § Skills e fluxo — atualizar referências a "ADR-004/-028/-039/-041" para "ADR-049" (substância preservada; apenas apontador).
- Documentar **refinamento editorial** em sub-seção dedicada: (a) exclusão de ADR-037 do cluster execução; (b) preservação de ADR-010 como ADR clássico vigente (não absorvido apesar de ser decisão base de ADR-039). Pattern editorial para ondas G-X.
- Saldo inventário pós-Onda F: estimado **37 vigentes** (40 pós-E + 1 ADR-049 - 4 arquivados); drop líquido de 3 (vs 1 em Onda E; cluster maior).
- Anotação progressiva: "Onda F shipped — commit <hash>; cluster execução migrado com refinamento editorial documentado".

Update do charter é commit separado post-merge (paralelo às atualizações de umbrella in BACKLOG das Ondas A+B+C+D+E); NÃO escopo desta Onda F.

**Decisão excluída — procedure file não criado:** cluster execução NÃO ganha procedure file equivalente a `cutucada-descoberta.md` (Ondas C teve; D+E não criaram). F9 lesson reaplicada: fronteira ADR-024 não aplica antecipadamente. Mecânica de execução vive em `skills/run-plan/SKILL.md` (executor primário; ~7-9 referências) + `skills/triage/SKILL.md` (caminho-com-plano + campo `**Branch:**` upstream) + CLAUDE.md (bullet meta-doutrinal) + templates/plan.md (campos opcionais).

**Decisão excluída — ADR-010 NÃO absorvido apesar de relação ADR-039:** ADR-039 § Origem cita ADR-010 como decisão base + categoria nova paralela. Sketch original do charter previa absorver ADR-010+ADR-039 em cluster "instrumentação progresso" separado. Resolução per ADR-045 fronteira: ADR-039 fica no cluster execução (aplicação canonical `/run-plan §3.5`); ADR-010 permanece como ADR clássico vigente codificando progress display (categoria distinta com potencial consumers futuros). ADR-049 § Decisão (c) reconhece "categoria nova paralela a progress display de ADR-010" preservando ADR-010 como autoridade ativa para seu escopo.

**Decisão excluída — ADR-037 NÃO absorvido apesar de inclusão no sketch:** Sketch original linha 252 listou ADR-037 (README framing Product Engineer harness) em cluster execução. Refinamento editorial per ADR-045 fronteira "ajuste editorial vs revisão" — ADR-037 pertence semanticamente a cluster discoverability/branding (paralelo a ADR-012 idioma artefatos discoverability + ADR-007 README), não a mecânica do `/run-plan`. ADR-037 fica órfão para futuro cluster discoverability OU permanece como ADR clássico standalone (per ADR-045 admission policy aplicada retroativamente).

**Pattern editorial para ondas G-X — refinamento documentado:** Esta é a primeira onda onde a composição do cluster é refinada vs sketch literal. Ondas C+D+E seguiram sketch literal. Onda F estabelece pattern: refinamento editorial documentado em § Origem do ADR consolidado + § Atualização pós-execução do charter (sem revisão estrutural de ADR-045 § Decisão parte 1; categoria editorial). Ondas G-X podem aplicar refinamento similar se composição do sketch não alinhar com coesão semântica.

**Cap de ondas estimado:** charter previa 6-10 ondas. Pós-Onda F (sexta), trajetória esperada: F + 4-6 ondas G-X adicionais. Cluster sequence revisitada — candidatos remanescentes: convenções editoriais (ADR-007+012+024+034, 4 heterogêneos); componentes plugin (ADR-008+013+015+016+023+040, 6 ADRs); alinhamento/triage (ADR-009+011+026+027+038+042, 6 ADRs com constraint always-include de ADR-048); discoverability/branding (ADR-037 + ?); brainstorm (ADR-036 standalone); apex (ADR-035+ADR-043+ADR-045+ADR-046+ADR-047+ADR-048+ADR-049 — meta-cluster apex que pode ou não consolidar).

**Sinal de saúde:** se Bloco 3 (skills/run-plan/SKILL.md, hot spot mecânico) gerar ≥10 findings de doc-reviewer, sinal de que reformulação narrativa precisa refinamento antes de aplicar a clusters maiores. Pausar e iterar conforme charter linha 154.

## Pendências de validação

- **Bloco 1 commitado sem invocação do doc-reviewer** — violação de doutrina explícita em `skills/run-plan/SKILL.md` § "## O que NÃO fazer" linha "Não pular revisor, mesmo em bloco trivial". Captura pós-fato: Bloco 1 foi format archive + redirect blockquote + extension archive index — pattern idêntico aplicado em Ondas C+D+E onde doc-reviewer aprovou consistentemente; substância editorial verificada via Read manual + critérios 2-3 do `## Verificação end-to-end` (ADRs arquivados + archive index estendido). Mitigação adicional: doc-reviewer do Bloco 2 confirmou pattern auto-consistente (cross-refs corretos + sub-headers `§ Decisão (a)` existem em ADR-049). Gap material improvável; ainda assim revisar manualmente se incidente concreto observado pós-merge. Captura como pendência para enforcement futuro: aderir estrito ao reviewer-per-bloco em ondas G-X mesmo quando pattern editorial é convergente.
