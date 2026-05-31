# ADR-049: Execução/run-plan consolidado (state em git/forge + campo Branch + Task tool state-keeping + campo Modo runbook)

**Data:** 2026-05-31
**Status:** Aceito

## Origem

- **Decisão base:** [ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) (apex da redesign — § Decisão parte 1 § Implementação literal: *"Ondas C-X — migração de ADRs por cluster temático. Cada onda absorve 3-6 ADRs antigos em 1 consolidado..."*). Este ADR é a quarta instância concreta dessa migração (Onda F) consolidando o cluster execução/run-plan.
- **ADRs absorvidos:** ADR-004 (foundational — state-tracking em git/forge, não em markdown — agora absorvido e arquivado nesta onda em `docs/decisions/archive/`) + ADR-028 (sucessor parcial lateral — campo `**Branch:**` opcional no `## Contexto` do plano; fluxo issue-first; opt-in por plano — agora absorvido e arquivado) + ADR-039 (sucessor parcial de ADR-010 — Task tool como state-keeping em fluxo longo; categoria nova paralela a progress display; lifecycle 2-estados; marker convention `[capture:*]` — agora absorvido e arquivado) + ADR-041 (sucessor parcial lateral de ADR-002 — campo `**Modo:** runbook` opt-in para system-surgery; bypass 4 dimensões do canonical; defensividade dura `**Branch:** + **Modo:** runbook incompatíveis` — agora absorvido e arquivado).
- **Decisões template:** [ADR-046](ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) (primeira instância de migração cluster — Onda C) + [ADR-047](ADR-047-modo-local-paths-replicacao-cross-mode.md) (segunda instância — Onda D, primeira sem procedure file) + [ADR-048](ADR-048-free-read-design-reviewer-consolidado.md) (terceira instância — Onda E, calibração descendente). Pattern validado: header redirect canonical, archive index incremental, propagação de cross-refs em docs vivos, link rot em 2 categorias, cond 5 primária isolada. F4 lesson Onda C reaplicada literal (cond 4 NÃO aplica; cond 1 NÃO aplica). F4 cond 2 lesson Onda D ("absorção consolidatória vs revogação") aplicada diretamente.
- **Decisões paralelas preservadas (NÃO absorvidas):** [ADR-010](ADR-010-instrumentacao-progresso-skills-multi-passo.md) (instrumentação de progresso multi-passo Task tool — decisão base de ADR-039 absorvido; preservada como ADR clássico vigente per refinamento editorial); [ADR-002](ADR-002-eliminar-gates-pre-loop.md) (eliminar gates pré-loop — decisão base de ADR-041 absorvido; preservada como ADR clássico vigente; tensão com ADR-049 § Decisão (d) resolvida em § Tensões abaixo). Estas decisões coexistem com ADR-049 codificando categorias semanticamente distintas; absorção parcial preserva substância sem revogar ancestrais.
- **Investigação:** Onda F codificada em `docs/plans/onda-f-migracao-cluster-execucao-run-plan.md`. Cluster execução escolhido como quarta migração por: (1) cluster coeso semanticamente máximo (4 ADRs cobrem dimensões da mecânica do `/run-plan`); (2) 4 ADRs com refinamento editorial documentado (exclusão de ADR-037 do sketch + preservação de ADR-010 fora do cluster); (3) cluster sem procedure file (reaplica F9 lesson D+E); (4) cluster com trade-offs vivos preservados (campos `**Branch:**` e `**Modo:**` revertíveis); (5) F4 lessons reaplicadas literal.

## Contexto

A camada doutrinal pós-v2.14.0 inclui 4 ADRs codificando dimensões da mecânica do `/run-plan`:

- **ADR-004 (foundational, 2026-05-06)** — estabeleceu state-tracking em git/forge (não em markdown). BACKLOG editorial sem `## Em andamento`; state vivo = branches/PRs abertos; `## Concluídos` append-only via `/run-plan §3.4`. -5 mecanismos defensivos obsoletos. Origem: revisão arquitetural pós-v1.20.0 contando 5 mecanismos defensivos protegendo o mesmo problema estrutural (merge artifact em `BACKLOG.md` com 2 PRs concorrentes mutando seções `## Em andamento` + `## Concluídos`).
- **ADR-028 (sucessor parcial lateral, 2026-05-14)** — campo `**Branch:**` opcional no `## Contexto` do plano para fluxo issue-first (GitLab, retrabalho de PR). `/run-plan §1.1` faz checkout em vez de criar; cutucada em `/triage` step 4 quando branch atual ≠ default (via `git symbolic-ref refs/remotes/origin/HEAD`). Opt-in por plano. Origem: operador questionou 2026-05-14 por que plugin não acomoda fluxo GitLab issue-first onde branch já existe quando trabalho começa (3 caminhos ruins atuais).
- **ADR-039 (sucessor parcial de ADR-010, 2026-05-26)** — Task tool como state-keeping em fluxo longo (categoria nova paralela a progress display de ADR-010). Lifecycle 2-estados `pending → completed` (skipping `in_progress`). Marker convention `[capture:<tipo>]` no subject. Aplicação canonical: `/run-plan §3.5` captura automática unificada (pré-loop warnings ADR-002 + passo 2 loop + passo 3.2 validação manual). Origem: Onda 2 ROADMAP item 8 (commit `25d0daf`) — fragilidade latente em `/run-plan §3.5` (lista mental do agente em fluxo longo).
- **ADR-041 (sucessor parcial lateral de ADR-002, 2026-05-27)** — campo `**Modo:** runbook` opcional no `## Contexto` do plano para system-surgery. Único valor aceito `runbook`. Bypass 4 dimensões do canonical (sem worktree + sem commit-per-bloco + gate confirmação por bloco + validação intercalada). Incompatibilidade dura `**Branch:** + **Modo:** runbook`. Materialização de capturas no `Falhou`. Origem: caso empírico `onda-1-fs-migration` do consumer `meta-system` 2026-05-27 — 5 mismatches estruturais entre `/run-plan` canonical e runbook plan.

Sob a redesign da camada doutrinal codificada em ADR-045, o cluster execução/run-plan é candidato natural para consolidação:

- **Decisão central estável** — state em git/forge + campos opcionais no plano + Task tool 2 modos + modo runbook sem revisão pendente. Trade-offs absorvidos editorialmente nas ondas históricas.
- **Mecanismos co-utilizados** — ADR-028 (`**Branch:**`) e ADR-041 (`**Modo:**`) são campos paralelos no `## Contexto` do plano com incompatibilidade dura explícita. Pattern editorial dos 2 campos opcionais reconhecido em ADR-028 § Razões "mesma família de `**Linha do backlog:**`".
- **Sem procedure file equivalente** — diferente de cutucadas (Onda C tinha `docs/procedures/cutucada-descoberta.md`), cluster execução tem toda mecânica em `skills/run-plan/SKILL.md` (executor primário; concentra ~9 ocorrências) + `skills/triage/SKILL.md` (caminho-com-plano + campo `**Branch:**` upstream) + CLAUDE.md (bullet meta-doutrinal) + templates/plan.md (campos opcionais). F9 lesson Onda D reaplicada — fronteira ADR-024 não aplica antecipadamente.
- **Calibração próxima à Onda D** (4 ADRs) — sequência C→D→E→F exerce 2→4→2→4 ADRs (scope variado). Pattern de propagation validado em 4 cenários.

Esta consolidação valida o pattern de migração em quarto caso (calibração para ondas G-X). Primeira onda onde refinamento editorial do sketch é documentado — pattern para ondas G-X que enfrentarem composição imperfeita do sketch original.

## Refinamento editorial ao sketch original do charter

Charter sketch linha 252:

```
ADR-005-skill-execucao-run-plan.md    # worktree + micro-commit + gates +
                                      # runbook mode + captura automática
                                      # (absorve atual: 004, 028, 037, 039, 041)
```

**Sketch absorvia 5 ADRs; Onda F refina para 4** per ADR-045 fronteira *"ajuste editorial do charter vs revisão de ADR-045"* (categoria editorial sem mudança estrutural na regra de consolidação):

- **ADR-037 (README framing "Product Engineer harness") EXCLUÍDO** — pertence semanticamente a cluster discoverability/branding (paralelo a ADR-012 idioma artefatos discoverability + ADR-007 README), não a mecânica do `/run-plan`. Sketch agrupou por proximidade numérica, não por coesão semântica. ADR-037 fica órfão para futuro cluster discoverability OU permanece como ADR clássico standalone se nenhum cluster afim emergir (per ADR-045 admission policy aplicada retroativamente: ADR-037 É decisão estrutural reversível documentando posicionamento editorial).
- **ADR-010 (instrumentação progresso Task tool) NÃO absorvido** — ADR-010 é decisão base de ADR-039 (ADR-039 § Origem cita ADR-010 como decisão base + categoria nova paralela). Charter sketch original linha 265 listou cluster "instrumentação progresso" separado (`ADR-010-instrumentacao-progresso.md (absorve atual: 010, 039)`). Sketch tinha **contradição interna** (ADR-039 listado em DOIS clusters: execução E instrumentação). Resolução per ADR-045 fronteira: ADR-039 fica no cluster execução (aplicação canonical `/run-plan §3.5` é mecânica de execução); ADR-010 permanece como ADR clássico vigente codificando progress display Task tool (categoria distinta com potencial consumers futuros além de `/run-plan`).

**Saldo do refinamento:**
- Onda F absorve 4 ADRs (vs 5 do sketch); ADR-037 + ADR-010 permanecem vigentes como ADRs clássicos standalone.
- Substância de ADR-010 preservada via referência cruzada em ADR-049 § Decisão (c) ("categoria nova paralela a progress display de ADR-010 — ambos modos coexistem"). Cross-ref textual mantém ADR-010 como autoridade ativa para seu escopo.
- Inventário pós-Onda F: 40 - 4 archivados + 1 ADR-049 = **37 vigentes** (drop líquido de 3 nesta onda, paralelo a Onda D).

**Pattern editorial para ondas G-X:** Esta é a primeira onda onde composição do cluster é refinada vs sketch literal. Ondas C+D+E seguiram sketch literal. Onda F estabelece pattern de refinamento documentado: (a) exclusão de ADR semanticamente desalinhado do sketch original; (b) preservação de ADR ancestral fora do cluster quando categoria conceitual distinta justifica standalone. Ambos refinamentos vivem em § Refinamento editorial do ADR consolidado + § Atualização pós-execução do charter (sem revisão estrutural de ADR-045 § Decisão parte 1). Ondas G-X podem aplicar refinamento similar se composição do sketch não alinhar com coesão semântica.

## Decisão

**Consolidar a doutrina sobre execução/run-plan em ADR único (este ADR-049), absorvendo substância de ADR-004 (foundational — state em git/forge) + ADR-028 (sucessor parcial — campo `**Branch:**`) + ADR-039 (sucessor parcial — Task tool state-keeping) + ADR-041 (sucessor parcial — campo `**Modo:** runbook`) sob narrativa única. Sem procedure file complementar — cluster sem split ADR/procedure per ausência de pré-existência (fronteira ADR-024 não aplica antecipadamente; F9 lesson Onda D reaplicada). Refinamento editorial documentado: ADR-037 excluído do cluster; ADR-010 preservado fora do cluster como ADR clássico vigente.**

### Escopo e mecanismo unificado

**6 dimensões integradas em narrativa única:**

#### (a) State-tracking em git/forge (não em markdown)

`BACKLOG.md` cumpre **2 papéis** num único arquivo: `## Próximos` (curadoria editorial) + `## Concluídos` (registro editorial append-only). `## Em andamento` removida — state vivo de in-flight work = branches/PRs abertos descobríveis via `git branch`/`gh pr list`/equivalente.

`/run-plan §3.4` apenas **adiciona** em `## Concluídos` (sem mover de outra seção). Linha do backlog capturada do plano via campo `**Linha do backlog:**` alimenta a entrada.

**Bifurcação descartada — (a) Total** (também remover `## Concluídos`): mais flat, mas perde **valor editorial** (notas de captura tipo "Flagado pelo X durante Y" não cabem em commits/PRs).

**-5 mecanismos defensivos obsoletos** (cada um adicionado a uma ocorrência do merge artifact em ondas históricas):
1. `/triage` push pós-commit determinístico (preservado por outras razões — visibilidade/recovery, não merge artifact)
2. `/run-plan` precondição 2 segunda metade (bloqueio em divergência) — removido
3. `/run-plan §3.7` auto-rebase com resolução programática — removido
4. Action `validate-backlog` GitHub workflow — removida
5. Skill `/heal-backlog` — removida

#### (b) Campo `**Branch:**` opcional para fluxo issue-first

Campo `**Branch:**` opcional no `## Contexto` do plano via template:

```markdown
**Branch:** <nome-da-branch> — incluir quando a branch já existe (issue-first GitLab, retrabalho de PR, etc.); ausência = /run-plan cria <slug> a partir do HEAD.
```

##### Mecânica

**`/triage` (caminho-com-plano).** No passo 4 (Produzir plano), após `git branch --show-current` retornar nome ≠ default (resolvido via `git symbolic-ref refs/remotes/origin/HEAD`; fallback `main`), perguntar via `AskUserQuestion`:

- `header`: `Branch`
- `question`: `"Usar '<branch-atual>' como branch de execução do plano?"`
- Opções: `Sim, usar essa branch` (Recommended) / `Não, /run-plan cria <slug>`

Branch atual == default → omitir pergunta (silêncio).

**`/run-plan §1.1` (setup da worktree).** Após ler o plano, detectar campo `**Branch:**`:
- Presente → `git worktree add .worktrees/<slug> <branch>` (sem `-b`). git resolve nome em ordem natural.
- Ausente → comportamento atual: `git worktree add .worktrees/<slug> -b <slug>`.
- Falha em criar worktree → discriminar pela stderr (branch inexistente / já checked out / diretório existe sem registro git / outras) e escrever em `## Próximos` do `backlog` linha específica para cada motivo (informar; parar).

##### Modo local

Campo aceito normalmente em modo local. Plano em modo local é gitignored, mas o **nome da branch** já é metadata pública (visível em `git push`, refs remotas) — registrar a branch existente no plano local não viola a regra de não-referenciar do ADR-047 (que protege referências **geradas pelo plugin** em commits/PRs/branches a partir de artefatos privados, não referências internas do plano local a metadata já pública).

`/run-plan §3.7` em modo local oferece `Renomear branch antes` apenas quando a branch foi **criada pelo plugin** (campo `**Branch:**` ausente). Branch pré-existente passa direto sem oferta de rename.

#### (c) Task tool como state-keeping em fluxo longo (categoria paralela a progress display de ADR-010)

Task tool serve, além de **progress display** ([ADR-010](ADR-010-instrumentacao-progresso-skills-multi-passo.md), preservado vigente), também como **state-keeping em fluxo longo** — buffer de pendências emergentes a materializar em ponto posterior do mesmo fluxo.

**2 modos coexistem sem fricção:**

| Modo | Decisão | Lifecycle | Reflete ao operador |
|---|---|---|---|
| Progress display | ADR-010 | `pending → in_progress → completed` triplo | Continuamente (cursor de execução) |
| State-keeping | ADR-049 § Decisão (c) | `pending → completed` 2-estados (skipping `in_progress`) | Batch em ponto posterior |

Mesmo SKILL pode usar ambos (progress Tasks para passos do loop + state-keeping Tasks para captures emergentes).

##### Marker convention

State-keeping Tasks têm prefixo marker no subject identificando tipo e destino. Convention canonical para captures de `/run-plan §3.5`:

- `[capture:validacao] <linha>` — destino `## Pendências de validação` no plano corrente.
- `[capture:backlog] <linha>` — destino `## Próximos` do papel `backlog`.

Outras skills que adotem state-keeping no futuro escolhem marker próprio com formato livre (recomendado: `[<contexto>]` curto e greppável). Schema 2-níveis `[<categoria>:<subtipo>]` emerge se ≥2 skills exercitarem dimensões distintas (gatilho de revisão).

##### Aplicação canonical: `/run-plan §3.5` captura automática unificada

Cobertura unificada das 3 superfícies emissoras:
- **Pré-loop warnings** (ADR-002 — preservado vigente): alinhamento dirty / `.worktreeinclude` ausente / credencial não coberta / escopo divergente / cobertura ausente.
- **Passo 2 loop** (durante execução de blocos): falha contornada / finding fora-do-escopo / hook bloqueando.
- **Passo 3.2 validação manual**: divergência do plano / bug colateral.

Materialização em §3.5: ler `TaskList` filtrada por marker `[capture:*]`, escrever cada Task pending no destino correto (validação no plano / backlog no role), marcar como completed via `TaskUpdate`. TaskList vazia (nenhum capture emergiu) → skip silente.

#### (d) Campo `**Modo:** runbook` opcional para system-surgery

Campo opcional `**Modo:**` no `## Contexto` do plano com **único valor aceito `runbook`**:

```markdown
**Modo:** runbook — incluir em planos de system-surgery (operações fora de diff git: `mv`, `systemctl`, edits em `~/`, ops em múltiplos repos coordenados, etc.); **tipicamente hand-written, não derivado de /triage**; bypassa worktree + micro-commit + reviewer per bloco + validação centralizada do /run-plan. Ausência = fluxo default. Único valor aceito: `runbook`.
```

##### Bypass de 4 dimensões do canonical

| Dimensão (modo runbook) | Comportamento |
|---|---|
| Sem worktree | Pula §1 inteiro do `/run-plan` (setup, replicação `.worktreeinclude`, sync, baseline). Executa no working tree principal. |
| Sem commit-per-bloco | Pula §2.5 (micro-commit). Rollback é responsabilidade do operador (snapshot/tarball/manual). |
| Gate de confirmação por bloco | Substitui §2.3-2.4 (escolher revisor + aplicar correções) por `AskUserQuestion` (header `Bloco N`, opções `Validei e seguir` / `Falhou — descrever`). Pattern paralelo a §3.2 do canonical. |
| Validação intercalada | Cada bloco descreve sua própria validação inline. §3 (gate final) reduz a §3.4 (Concluídos via `**Linha do backlog:**`) + §3.5 (captura automática) + §3.6 (declarar done). §3.1, §3.2, §3.3, §3.7 pulados. |

##### Incompatibilidades duras

- `**Branch:** + **Modo:** runbook` → `/run-plan` para na pré-condição 0 com mensagem `"**Modo:** runbook + **Branch:** incompatíveis — runbook executa no working tree principal, sem worktree"`.
- Valor `**Modo:**` diferente de `runbook` → para com mensagem citando único valor aceito.

##### Materialização de capturas no `Falhou`

Ao operador escolher `Falhou — descrever`, antes de a skill parar, materializar capturas acumuladas (ler `TaskList` por `[capture:*]`, escrever em destinos corretos) — paralelo a §3.5 do canonical, disparado pelo `Falhou` ao invés do gate final. Evita perda de capturas dos blocos anteriores quando execução para mid-plano.

##### Mitigação ao gap de reviewer per bloco ausente

Modo runbook bypassa `code-reviewer`/`doc-reviewer` per bloco. Invariantes ficam por conta de **gate humano de confirmação inline + revisão upstream manual** por `@design-reviewer` ([ADR-009](ADR-009-revisor-design-pre-fato.md), [ADR-011](ADR-011-wiring-design-reviewer-automatico.md)) sobre o plano-documento antes de invocar `/run-plan`. Operador é responsável por executar essa revisão fora da skill.

#### (e) Pattern paralelo de campos opcionais no `## Contexto`

Campos `**Branch:**` (dimensão b) e `**Modo:**` (dimensão d) seguem **pattern editorial unificado**:
- Campo opcional no `## Contexto` do plano.
- Ausência = comportamento default total.
- Presença = opt-in revertível por plano.
- Documentação canonical em `templates/plan.md` bloco "campos especiais".
- Mensageiros para `/run-plan` consumir no setup (§1.1 detecção + pré-condição 0 detecção).
- Pattern paralelo a `**Linha do backlog:**` (mensageiro de matching para transições de estado) + `**Termos ubíquos tocados:**` (mensageiro para reviewer) + `**ADRs candidatos:**` (mensageiro para curadoria de free-read — ADR-048).

**Critério de promoção a campo opcional canonical** (gatilho de admissão futura, paralelo ao admission policy de ADR-045): nova dimensão de execução-do-plano que (i) afeta `/run-plan` ou `/triage`, (ii) tem comportamento default natural, (iii) é revertível por plano sem cerimônia, (iv) cabe em 1 linha de `## Contexto`.

#### (f) Tensões resolvidas com decisões paralelas preservadas

##### Tensão com ADR-002 (eliminar gates pré-loop) — preservada vigente

ADR-002 § Decisão estabelece *"Skill nunca interrompe por cutucada na fase pré-loop. Warning detectado é classificado e materializado no trilho Aviso/Backlog/Validação"*. ADR-049 § Decisão (d) introduz incompatibilidade dura (`**Branch:** + **Modo:** runbook` → informa e para) que tem natureza de gate.

**Resolução:** ADR-002 cobre warnings de **qualidade-de-mudança** (alinhamento dirty, escopo divergente, credencial não coberta) onde decisão majoritária é "Continuar" e a pergunta vira ritual. ADR-049 § Decisão (d) cobre **incompatibilidade semântica de campos no plano** — operador escreveu dois campos com semânticas contraditórias por engano. Categoria distinta: não é warning de qualidade ambiente, é erro de plano. Gate dura aqui não é cerimônia — é defesa contra plano-author errado em contexto que toca state do sistema (alto custo de mutação errada). ADR-002 § Limitações reconhece: *"warnings que exijam decisão imediata e irreversível voltam para gate explícito"*. ADR-049 opera nessa exceção.

ADR-002 preservado como ADR clássico vigente codificando escopo intencional (warnings de qualidade-de-mudança).

##### Tensão com ADR-004 (state em git para mudança de código) — absorvida nesta § Decisão (a)

ADR-049 § Decisão (a) absorve substância integral de ADR-004 (state em git/forge para mudança de código + BACKLOG editorial). ADR-049 § Decisão (d) modo runbook executa sem branch dedicada — aparentemente quebra o contrato.

**Resolução:** ADR-049 § Decisão (a) cobre state de **mudança de código** (onde branch é o vehicle natural). Runbook plan (§ Decisão d) não é mudança de código — é execução supervisionada de operações sistêmicas. Working tree principal já é o "lugar onde o trabalho acontece"; criar branch para state-tracker de operações `mv`/`systemctl` seria cerimônia vazia. Categorias distintas dentro do mesmo consolidado; ADR-049 § Decisão (a) e (d) coexistem sem fricção (campo `**Modo:** runbook` opt-in identifica a categoria distinta).

##### Tensão com ADR-010 (progress display Task tool) — preservada vigente

ADR-010 codifica progress display Task tool (lifecycle triplo, cursor de execução). ADR-049 § Decisão (c) introduz state-keeping (lifecycle 2-estados, buffer de pendências). Ambos modos coexistem sem fricção — marker no subject distingue (progress Tasks tipicamente sem marker; state-keeping Tasks com `[<categoria>:<subtipo>]`).

ADR-010 preservado como ADR clássico vigente codificando categoria distinta (progress display) com potencial consumers futuros além de `/run-plan`.

### Razões

- **Doutrina consolidada com clareza editorial.** Reader único navega thread completo (state em git/forge + campo `**Branch:**` + Task tool state-keeping + campo `**Modo:** runbook` + pattern campos paralelos + tensões resolvidas) em ADR único; não precisa saltar 4 ADRs nem inferir relações por leitura cruzada.
- **Pattern editorial unificado dos campos opcionais codificado** — § Decisão (e) reconhece pattern paralelo de `**Branch:** + **Modo:** + **Linha do backlog:** + **Termos ubíquos tocados:** + **ADRs candidatos:**` como família coerente; critério de promoção futura registrado.
- **Tensões resolvidas explicitamente** — § Decisão (f) absorve substância de ADR-041 § Tensões com ADR-002 + ADR-004 + integra com ADR-010 (state-keeping vs progress display). Ancestrais preservados vigentes com escopos delimitados sem revogação.
- **Sem procedure file — toda mecânica vive em docs vivos.** Cluster execução não tem procedure pré-existente per ADR-024. Mecânica opera distribuída: `skills/run-plan/SKILL.md` (executor primário; pré-condições + warnings + loop + gate final + modo runbook) + `skills/triage/SKILL.md` (caminho-com-plano + campo `**Branch:**` upstream) + CLAUDE.md (bullet meta-doutrinal) + templates/plan.md (campos opcionais).
- **Pattern de migração validado em quarta instância com refinamento editorial documentado.** Onda F estabelece pattern para ondas G-X que enfrentarem composição imperfeita do sketch original (exclusão de ADR + preservação de ADR ancestral fora do cluster).
- **Trilha empírica preservada.** § Origem histórica deste ADR lista os 4 incidentes empíricos das decisões absorvidas; conteúdo original arquivado em `docs/decisions/archive/` para registro auditável.
- **Saldo inventário:** 40 vigentes pós-Onda E + 1 novo ADR-049 - 4 arquivados = **37 vigentes pós-Onda F** (drop líquido de 3 — paralelo a Onda D).

### Header redirect canonical + archive index — format herdado de ADR-046

Arquivos arquivados sob `docs/decisions/archive/` adotam **format de citação + header H1 original preservado** codificado em ADR-046 § Razões:

```markdown
> **ARCHIVED <YYYY-MM-DD>** — content absorbed into [ADR-MMM](../ADR-MMM-<slug>.md); see that ADR for current authority. Body below preserved verbatim for historical record.

# ADR-NNN: <título original>

<body original integral...>
```

`docs/decisions/archive/README.md` (criado na Onda C, estendido em D+E) **estendido** com 4 linhas novas nesta onda (ADR-004, ADR-028, ADR-039, ADR-041 → ADR-049, Onda F).

## Origem histórica

Incidentes empíricos das 4 decisões absorvidas preservados como contexto para reabertura informada:

### Revisão arquitetural pós-v1.20.0 (origem de ADR-004)

Revisão arquitetural pós-v1.20.0 contou 5 mecanismos defensivos no plugin protegendo o mesmo problema estrutural: merge artifact em `BACKLOG.md` quando dois PRs concorrentes mutam as seções `## Em andamento` e `## Concluídos` simultaneamente. Cada mecanismo adicionado em momento diferente, em resposta a 3+ ocorrências do artefato em uso real (registrado em PR #20+#21 e linhas históricas em `## Concluídos`). Defesa em profundidade legítima dado histórico, mas sintoma de **design fragility**: artefato corrente mistura curadoria editorial (Próximos) com state-tracking (Em andamento, Concluídos), e o segundo é o que quebra sob concorrência. ADR-004 estabeleceu state-tracking em git/forge eliminando o ciclo.

### Operador GitLab issue-first 2026-05-14 (origem de ADR-028)

Operador questionou 2026-05-14 por que plugin não acomoda fluxo de projetos GitLab onde issue é especificada no forge antes do desenvolvimento e branch já existe (criada via "Create branch" da issue) quando trabalho começa. `/run-plan` no setup da worktree sempre criava branch nova a partir do HEAD, sem caminho para reaproveitar branch pré-existente. Três caminhos ruins atuais: (1) aceitar `/run-plan` cria `<slug>` perdendo link issue↔branch; (2) renomear branch existente para casar com slug (frágil); (3) usar plugin sem `/run-plan` (perde worktree isolada, micro-commits, gates). ADR-028 estabeleceu campo `**Branch:**` opcional opt-in por plano.

### Onda 2 ROADMAP item 8 commit `25d0daf` (origem de ADR-039)

Sessão 2026-05-26 identificou fragilidade latente em `/run-plan §3.5 captura automática`: spec atual dizia *"agente acumula gatilhos e materializa no gate final"* sem mecanismo de tracking — dependia de lista mental. Em `/run-plan` longo (≥3 blocos com triggers reais), risco de esquecer parte da lista entre passo 2 e §3.5. Mesma classe de fragilidade silent regression que ROADMAP itens 6 (reviewer-vs-reviewer) e 7 (stale-view) endereçaram na mesma onda — agente mantém state mentalmente em fluxo multi-passo sem persistência verificável. ADR-039 estabeleceu Task tool como state-keeping (categoria nova paralela a progress display de ADR-010).

### Caso empírico `meta-system onda-1-fs-migration` 2026-05-27 (origem de ADR-041)

Plano `onda-1-fs-migration` do consumer `meta-system` (migração de filesystem PARA→functional, ~38 repos + drive-sync + chezmoi + ~/.claude + XDG + IDE workspaces). Cinco mismatches estruturais entre `/run-plan` canonical e plano-real: (1) worktree estaria dentro do FS sendo migrado; (2) 11 de 12 blocos não produziam diff git (operações `mv`, `systemctl`, etc.); (3) rollback é btrfs snapshot + tarball, não `git revert`; (4) reviewer per bloco trabalha sobre diff que não existe; (5) validação corre DURANTE (smoke tests gateiam blocos), não no gate final. Forçar `/run-plan` num runbook plan resultava em: worktree órfã + commits artificiais + execução ainda manual fora da skill. ADR-041 estabeleceu campo `**Modo:** runbook` opt-in com bypass 4 dimensões do canonical.

## Consequências

### Benefícios

- Reader navega thread completo da mecânica do `/run-plan` em 1 ADR (era 4 ADRs).
- Pattern de migração validado em cluster com hot spot mecânico (`skills/run-plan/SKILL.md` concentra ~50% das ocorrências).
- Refinamento editorial documentado — pattern para ondas G-X que enfrentarem composição imperfeita do sketch original.
- Mecânica preservada distribuída em docs vivos onde executa.
- Trilha empírica preservada via archive + § Origem histórica.
- **-5 mecanismos defensivos** removidos do plugin (herdado de ADR-004).
- **Fluxo issue-first GitLab suportado** sem inverter default ou adicionar configuração paralela (herdado de ADR-028).
- **State-keeping via Task tool elimina lista mental** do agente em fluxo longo (herdado de ADR-039).
- **`/run-plan` cobre genuinamente runbook plans** em vez de corromper working tree silenciosamente (herdado de ADR-041).
- Saldo inventário: **37 vigentes pós-Onda F** (drop líquido de 3 — paralelo a Onda D).

### Trade-offs

- **Link rot em ADRs imutáveis tem 2 categorias distintas (F1 lesson Onda C reaplicada).**
  - **Categoria (a) — referências históricas/precedente** (vasta maioria — ADRs imutáveis citam ADR-004/-028/-039/-041 em § Origem ou cross-refs textuais). **Archive resolve** — `docs/decisions/archive/<slug>.md` carrega corpo histórico completo per format codificado. Cross-refs em ADRs imutáveis ficam como registro histórico, NÃO são editados.
  - **Categoria (b) — referências de substância doutrinal ativa** (subset identificado pré-execução): ADR-041 § Tensão com ADR-002 → substância "warnings de qualidade-de-mudança vs incompatibilidade semântica" absorvida em ADR-049 § Decisão (f); ADR-041 § Tensão com ADR-004 → substância "state em git para mudança de código vs sistema como state-tracker em runbook" absorvida em ADR-049 § Decisão (a)+(d); ADR-039 cita ADR-010 como decisão base → ADR-010 permanece vigente, substância em ADR-049 § Decisão (c) "categoria nova paralela a progress display de ADR-010". **Hipótese: zero substância "doutrinal ativa" perdida.** design-reviewer valida.
- **Custo do refactor de cross-refs menor que Onda D** — 5 docs vivos atualizados (vs 9 em D, 6 em E); ~19 ocorrências em ~17 linhas distintas (vs ~58/34 em D). Hot spot mecânico em `skills/run-plan/SKILL.md` (9 ocorrências) concentra risco editorial; doc-reviewer audita Bloco 3 separadamente.
- **Refinamento editorial introduz overhead** — primeira onda com composição refinada vs sketch literal. Pattern editorial para ondas G-X estabelecido em ADR-049 § Refinamento editorial + § Decisão; futuras ondas com refinamento similar podem reaplicar pattern.
- **Implementação history das 4 decisões absorvidas permanece em archives** — NÃO duplicada em ADR-049 (paralelo aos precedentes Ondas C+D+E; padrão editorial codificado em ADR-047 § Trade-offs).
- **CHANGELOG.md preservado intacto** — registro histórico imutável paralelo a ADRs imutáveis.

### Limitações

- **ADR-049 § Decisão (a) pressupõe que operador tem acesso a `git`/`gh`/equivalente** para descobrir state vivo (herdado de ADR-004 § Limitações). Em fluxos com muitos colaboradores onde state em markdown servia como "tabela compartilhada", consolidação deslocaria coordenação para o forge. Hoje plugin é mantenedor único — limitação não vincula. Reabrir se equipe maior reportar pain.
- **`## Concluídos` continua sendo append-only manual** sem mecanismo de garbage collection (herdado de ADR-004 § Limitações). Repos muito longevos podem ter Concluídos volumoso. Corte por release é decisão futura.
- **State-keeping é conversation-scoped per ADR-010** (herdado de ADR-039 § Limitações). Tasks somem ao fim da sessão. Para state-keeping cross-session, mecanismo diferente (artefato persistido) é necessário — não coberto.
- **Marker convention requer disciplina do skill author** (herdado de ADR-039 § Limitações). Sem marker, Task vira indistinguível de progress display. Mitigação: convention documentada aqui + design-reviewer pode flagar.
- **Mitigação ao gap de reviewer per bloco em modo runbook depende de operador disciplinado** (herdado de ADR-041 § Mitigação). `@design-reviewer` sobre plano-documento antes de invocar `/run-plan` é responsabilidade externa à skill.
- **Refinamento editorial requer ADR-045 § Decisão parte 1 fronteira "ajuste editorial vs revisão" como autoridade** — se refinamento extrapolar (ex.: excluir ADR central de cluster sem ancestral semântico claro), gatilho de revisão de ADR-045 ativa.

### Mitigações

- **Anti-regression checklist do charter** § Skills e fluxo lista os ~12 elementos load-bearing (state em git/forge, BACKLOG sem Em andamento, ## Concluídos append-only, campo `**Branch:**` opcional + probe + cutucada, Task tool 2 modos + marker convention + lifecycle 2-estados, `/run-plan §3.5` captura unificada cross-superfícies, campo `**Modo:** runbook` + bypass 4 dimensões + incompatibilidades duras + materialização Falhou, pattern paralelo campos opcionais) — design-reviewer audita preservação em ADR-049 § Decisão. Plano § Verificação end-to-end critério 12 prescreve audit explícito.
- **Plano § Verificação end-to-end critérios 4-9** prescrevem grep explícito de ADR-004/-028/-039/-041 em paths concretos + grep preservativo de ADR-010 + grep de existência de ADR-037. Pattern reaplicado das Ondas C+D+E.
- **Archive index estendido nesta Onda F** (4 linhas novas em `docs/decisions/archive/README.md`) — link rot mitigation **ativa** desde já para o cluster execução.
- **F4 lessons reaplicadas literal** — cond 5 primária isolada; cond 4 NÃO aplica; cond 1 NÃO aplica. F4 cond 2 lesson Onda D ("absorção consolidatória vs revogação") aplicada diretamente. Evita inflação de critérios em ondas G-X.
- **Refinamento editorial documentado em § Refinamento editorial** — pattern para ondas G-X que enfrentarem composição imperfeita do sketch original.

## Alternativas consideradas

### (a) Manter ADR-004 + ADR-028 + ADR-039 + ADR-041 com Addenda individuais

Continuar com estrutura atual: 4 ADRs vigentes com Addenda históricos isolados.

Descartada per ADR-045 § Decisão parte 1: cluster Addenda foram **prova de conceito** de consolidação editorial; a redesign generaliza esse movimento para **archive + consolidado único**. Manter status quo perde benefício de leitura única do thread + mantém 4 ADRs onde 1 cabe sob a nova estrutura. Cluster execução não tem cluster index Addendum existente (diferente de ADR-005/-017/-021) — ainda assim qualifica per ADR-045 critério coesão semântica + scope médio (4 ADRs).

### (b) Edit in-place em ADR-004 absorvendo ADR-028 + ADR-039 + ADR-041

Reescrever ADR-004 incorporando substância dos 3 sucessores; ADR-028/-039/-041 marcados `Substituído`.

Descartada:

- Viola convenção ADR-classical (ADRs são registros imutáveis; supersedeção via novo ADR).
- Apaga trajetória editorial (ADR-028 documentou 3 caminhos ruins; ADR-041 documentou 5 mismatches do caso `meta-system`; ADR-039 documentou Onda 2 ROADMAP).
- ADR-045 explicitamente prescreve archive + novo ADR consolidado.
- ADR-046 + ADR-047 + ADR-048 já estabeleceram pattern de archive + novo consolidado; mudar pattern em Onda F fere consistência.

### (c) Absorver ADR-010 junto com ADR-039

Incluir ADR-010 no cluster (cluster instrumentação progresso do sketch absorvido em cluster execução).

Descartada via refinamento editorial:

- ADR-010 codifica progress display Task tool (categoria distinta com potencial consumers futuros além de `/run-plan`).
- ADR-049 § Decisão (c) state-keeping é **categoria nova paralela** a progress display — coexistência sem fricção.
- Charter sketch original tinha contradição (ADR-039 listado em DOIS clusters); resolução per ADR-045 fronteira favorece preservar categoria distinta de ADR-010.
- Substância de ADR-010 referenciada em ADR-049 § Decisão (c) mantém ADR-010 como autoridade ativa.

### (d) Absorver ADR-037 (sketch literal)

Incluir ADR-037 no cluster execução conforme sketch original literal.

Descartada via refinamento editorial:

- ADR-037 (README framing "Product Engineer harness") pertence semanticamente a cluster discoverability/branding (paralelo a ADR-012 idioma artefatos discoverability + ADR-007 README), não a mecânica do `/run-plan`.
- Sketch agrupou ADR-037 por proximidade numérica, não por coesão semântica — refinamento editorial corrige.
- ADR-037 fica órfão para futuro cluster discoverability OU permanece como ADR clássico standalone.
- Pattern editorial codificado para ondas G-X em § Refinamento editorial.

### (e) Criar `docs/procedures/run-plan-execution.md` absorvendo a mecânica

Mover mecânica das 4 decisões para procedure file novo; ADR-049 carrega apenas substância doutrinária.

Descartada:

- Cria procedure file **sem necessidade pré-existente** — pattern de Ondas D+E explicita que procedure file separation per ADR-024 aplica quando procedure **pré-existe**.
- Mecânica de execução já está distribuída em `skills/run-plan/SKILL.md` (executor primário) + `skills/triage/SKILL.md` + CLAUDE.md + templates. Mover para procedure cria 5ª localização sem ganho de coesão.
- Procedure file tem categoria conceitual de **algoritmo prescritivo executor cross-skills** (per ADR-024); mecânica do `/run-plan` é **interna ao SKILL** — fit pobre.

### (f) Splits diferentes — separar ADR-004 (state) de ADR-028+039+041 (campos+state-keeping)

Criar 2 ADRs: ADR-049a "State-tracking em git/forge foundational" + ADR-049b "Mecânica de `/run-plan` (campos + state-keeping + runbook)".

Descartada:

- Splits artificiais — os 4 ADRs cobrem dimensões da **mesma decisão estrutural** (execução do `/run-plan`). Pattern editorial paralelo de campos opcionais (§ Decisão e) demonstra família coerente.
- 2 ADRs onde 1 cabe — viola Ockham.
- Pattern Onda C+D+E (1 consolidado por cluster) — mudar em Onda F fere consistência.

### (g) ADR-049 como índice apontando para os 4 ADRs originais (sem archive)

ADR-049 minimalista apontando para os 4 ADRs originais; nada movido para archive.

Descartada (paralelo a Alternativa (e) de ADR-046/-047/-048):

- Não materializa a redesign — ADR-045 prescreve absorção de conteúdo + archive de antigos.
- Pattern Onda C+D+E já estabeleceu absorção + archive; mudar em Onda F fere consistência.

## Gatilhos de revisão

Triggers das 4 decisões absorvidas consolidados + triggers específicos da consolidação:

### Herdados de ADR-004 (state em git/forge)

- **Equipe maior ou colaboração distribuída** onde `## Em andamento` em markdown era coordenação visível → reabrir para considerar caminho explícito (status labels, dashboard externo, ou retorno).
- **`## Concluídos` cresce ao ponto de fricção** (ex.: 200+ linhas) → considerar política de archival por release ou por trimestre.
- **Surge novo padrão de merge artifact** em outra superfície do plugin → reabrir critério "state em markdown" para arquivo afetado.

### Herdados de ADR-028 (campo `**Branch:**`)

- **≥2 consumer projects reportarem confusão** entre branch criada pelo plugin e branch pré-existente do forge → considerar diferenciação UI no relatório do `/run-plan`.
- **Fluxos não-cobertos emergirem** (ex.: GitLab + forge templates com nome de branch derivado de issue): refinar mecânica `git symbolic-ref refs/remotes/origin/HEAD` para cobrir.
- **Modo local + Branch presente gerar confusão** sobre regra de não-referenciar → reabrir critério "metadata pública vs identificador privado".

### Herdados de ADR-039 (Task tool state-keeping)

- **Outras skills adotam state-keeping pattern:** se ≥2 skills além de `/run-plan` adotarem o pattern, considerar (a) refinar marker convention (talvez schema mais formal `[<skill>:<categoria>:<subtipo>]`); (b) adicionar bullet em `CLAUDE.md` § Editing conventions cross-ref a ADR-010 + ADR-049 § Decisão (c).
- **Cross-session state-keeping demandado:** se uso real revelar necessidade de captures que sobrevivem fim de sessão → reabrir para considerar persistência além de conversation-scoped (ADR-047 local-gitignored ou similar).
- **Lifecycle 3-estados ressurge como necessidade** em state-keeping → reabrir lifecycle 2-estados; talvez reconciliar com triplo de ADR-010 num modelo único.
- **Marker convention conflita com progress Tasks sem marker** → reabrir convention (talvez tornar marker obrigatório também para progress Tasks).

### Herdados de ADR-041 (campo `**Modo:** runbook`)

- **Outros valores de `**Modo:**` emergirem** (ex.: `dry-run`, `verbose`, `migration`) → reabrir critério "único valor aceito" — campo pode acomodar enum de valores se categorias distintas justificarem.
- **Runbook plans pequenos em projetos diferentes do `meta-system`** reportarem fricção com bypass 4 dimensões → recalibrar dimensões bypassed (talvez dimensão por dimensão opt-in).
- **Reviewer per bloco ausente gerar incidentes** em runbook plans (`@design-reviewer` upstream esquecido) → reabrir mitigação; talvez gate dura "confirmar revisão upstream" antes de prosseguir.

### Específicos desta consolidação (Onda F)

- **Refinamento editorial gera incoerência substancial** — se exclusão de ADR-037 do cluster execução + preservação de ADR-010 fora do cluster gerar gap doutrinal observável (ex.: futura onda discoverability não consolida ADR-037; futura onda instrumentação progresso não consolida ADR-010), reabrir critério "ajuste editorial vs revisão" — talvez requerer revisão de ADR-045 § Decisão parte 1.
- **Pattern campos opcionais paralelo gera demanda por 3º/4º campo** — se ≥1 nova dimensão de execução-do-plano emergir (gatilho de promoção em § Decisão e), reabrir critério de admissão; talvez requerer skill SKILL para validar campos opcionais.
- **Pattern de migração falhar em outra onda G-X** com cluster maior (5-8 ADRs) — design-reviewer flagrar gap material no pattern. Reabrir ADR-046+ADR-047+ADR-048+ADR-049 como template combinado.
- **Volume de cross-refs (~19 em 5 docs vivos com hot spot 9 em `skills/run-plan/SKILL.md`) gerar ≥10 findings de doc-reviewer no Bloco 3** — pattern de propagation em hot spot mecânico precisa refinamento antes de aplicar a clusters maiores.

## Auto-aplicação coerente per ADR-034

- **Cond 5 (sucessor parcial):** aplica primária — consolidado absorve substância de ADR-004 (foundational) + ADR-028 + ADR-039 + ADR-041 (3 sucessores parciais cobrindo dimensões distintas) sob narrativa única. Os 4 ADRs vão para archive com header redirect canonical a este ADR. **Suficiente per ADR-034** *"novo ADR quando ≥1 das 5 condições aplica"*; cond 5 isolada justifica criação deste ADR.
- **Cond 4 (categoria nova):** **NÃO aplica** — ADR-045 § Decisão parte 1 § Implementação **já codificou a categoria** "consolidação editorial cross-ADR de cluster temático como decisão estrutural" no nível meta-pattern; ADR-046 + ADR-047 + ADR-048 estabeleceram primeira/segunda/terceira instâncias concretas; ADR-049 é **quarta instância concreta** da categoria já estabelecida, não introduz categoria conceitual nova. **F4 lesson de Onda C reaplicada literal** — aplicar cond 4 aqui inflaria o critério em cada onda G-X.
- **Cond 1 (decisão estrutural sem ancestral direto):** **NÃO aplica** — ADR-045 § Decisão parte 1 § Implementação **é ancestral codificado direto** do pattern que ADR-049 instancia. ADR-046 + ADR-047 + ADR-048 são segundas/terceiras/quartas fontes ancestrais codificadas. ADR-049 herda essa ancestralidade.
- **Cond 2 (substitui ADR ancestral):** NÃO aplica — operação é **absorção consolidatória** (substância das 4 decisões codificada integralmente em ADR-049 § Decisão sob narrativa única; archive preserva trajetória), **não revogação** (paralelo a ADR-043 → ADR-035, onde apex doutrinal foi invertido). Diferença pragmática: leitor de ADR-049 obtém regra vigente identicamente equivalente à composição dos 4 absorvidos; leitor de archive vê redirect canonical apontando para autoridade vigente sem ambiguidade. **F4 cond 2 lesson de Onda D aplicada diretamente** — pattern editorial para ondas G-X (cond 2 reservada para inversões/revogações; absorções consolidatórias seguem cond 5 isolada).
- **Cond 3 (codifica restrição externa):** NÃO aplica — decisão interna ao processo doutrinal do plugin.

Pattern editorial para ondas G-X: cada migração cluster aplica **cond 5 primária + outras condições conforme ancestralidade real**, não cond 4 inflada nem cond 1 espúria. ADR-045 + ADR-046 + ADR-047 + ADR-048 são ancestrais codificados de cada migração; ondas instanciam, não criam categoria. **F4 lessons codificadas como pattern para G-X.**

**Adicional para Onda F**: pattern de **refinamento editorial documentado** (§ Refinamento editorial deste ADR) estabelecido para ondas G-X que enfrentarem composição imperfeita do sketch original — exclusão de ADRs semanticamente desalinhados OU preservação de ADRs ancestrais fora do cluster quando categoria conceitual distinta justifica standalone. Refinamento vive em § Refinamento editorial do ADR consolidado + § Atualização pós-execução do charter (sem revisão estrutural de ADR-045 § Decisão parte 1).
