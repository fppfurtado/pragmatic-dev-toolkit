# Plano — Campo `**Modo:** runbook` opt-in em planos para `/run-plan`

## Contexto

Primeiro caso empírico em 2026-05-27 com plano `onda-1-fs-migration` do consumer `meta-system` (migração de filesystem PARA→functional, ~38 repos + drive-sync + chezmoi + ~/.claude + XDG + IDE workspaces) expôs cinco mismatches estruturais entre `/run-plan` e planos de "system-surgery / runbook":

1. **Worktree dentro do escopo da migração** — Bloco 3 do plano-real move `/storage/3. Resources/Projects/meta-system/.worktrees/<slug>` mid-execução; `/run-plan §1.1` cria worktree justamente em path que o próprio plano vai mover.
2. **11 de 12 blocos sem diff git** — operações são `mv`, `systemctl`, `xdg-user-dirs-update`, edits em `~/.config/`, `~/.local/share/chezmoi/`, `~/.claude/*.json`, `CLAUDE.md` em N outros repos, `VBoxManage`. Micro-commit por bloco (§2.5) não tem matéria-prima.
3. **Rollback fora do git** — btrfs snapshot + tarball, não `git revert`. Micro-commits revertíveis (premissa de ADR-002 + §2.5) não desfazem `mv`/`systemctl`/edits em `~/`.
4. **Reviewer per bloco sobre diff inexistente** — `code-reviewer` (default §2.3) avalia diff git; 11/12 blocos não geram diff.
5. **Validação intercalada, não no done** — smoke tests gateiam Bloco 10 (resume-drive-sync); bootstrap test em VM gateia Bloco 12. `## Verificação manual` única no gate final (§3.2) chega tarde.

Forçar `/run-plan` no plano-real resultaria em worktree órfã + commits artificiais + ainda exigir execução manual fora da skill. Workaround atual: skill loaded mas operador escolheu execução supervisionada manual.

**Bifurcação resolvida via `/triage`:** operador escolheu direção (b) — modo opt-in via campo `**Modo:** runbook` no `## Contexto` do plano, ao invés de (a) recusar runbook plans com mensagem ou (c) só ADR documentando fronteira sem código. Trade-off de codificação prematura (1 evidência) absorvido sob ADR-035 critério 2 (fronteira doutrinal nítida) — `/run-plan` hoje silenciosamente aceita planos cuja semântica não bate, corrompendo working tree do operador sem mensagem.

**ADRs candidatos:** [ADR-002](../decisions/ADR-002-eliminar-gates-pre-loop.md) (warnings vs gates pré-loop — modo runbook redefine quando warnings disparam); [ADR-004](../decisions/ADR-004-state-tracking-em-git.md) (state em git — modo runbook bypassa parte do contrato porque ambiente é o escopo, não o repo); [ADR-028](../decisions/ADR-028-campo-branch-opcional-plano-fluxo-issue-first.md) (precedente de campo opcional no `## Contexto` que altera fluxo); [ADR-035](../decisions/ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) (critério 2 fronteira doutrinal nítida — justificativa para codificar com 1 evidência); [ADR-034](../decisions/ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) (condição 5 sucessor parcial lateral de ADR-002 — estende regime de warnings/trilhos pré-loop, condiciona contrato implícito do `/run-plan` sobre worktree + diff git + reviewer per bloco; paralelo aos precedentes ADR-029→ADR-017, ADR-030→ADR-005, ADR-038→ADR-026, ADR-039→ADR-010).

**Linha do backlog:** plugin: avaliar fronteira `/run-plan` vs planos "runbook / system-surgery" — primeiro caso empírico observado em 2026-05-27 com plano `onda-1-fs-migration` do consumer `meta-system`

## Resumo da mudança

Introduzir campo opcional `**Modo:** runbook` no `## Contexto` do plano. Presença ativa fluxo alternativo em `/run-plan` que bypassa 4 dimensões do fluxo canonical, mapeadas 1:1 aos mismatches:

| Dimensão (modo runbook) | Mismatch resolvido | Comportamento |
|---|---|---|
| Sem worktree | (1) worktree dentro do escopo | Pula §1 inteiro (setup, replicação `.worktreeinclude`, sync, baseline). Executa no working tree principal. |
| Sem commit-per-bloco | (2) blocos sem diff + (3) rollback fora do git | Pula §2.5 (micro-commit). Rollback é responsabilidade do operador (snapshot/tarball/manual). |
| Gate de confirmação por bloco | (4) reviewer sobre diff inexistente | Substitui §2.3-2.4 (escolher revisor + aplicar correções) por `AskUserQuestion` (header `Bloco N`, opções `Validei e seguir` / `Falhou — descrever`). |
| Validação intercalada | (5) validação durante, não no done | Cada bloco descreve sua própria validação inline; §3 (gate final) reduz a §3.4 (Concluídos) e relato final. Pula §3.1 (gate automático), §3.2 (validação manual centralizada), §3.3 (sanity check docs), §3.7 (publicação). |

Modo ausente → fluxo default preservado (regressão). Apenas `**Modo:** runbook` aceito — qualquer outro valor (`canonical`, `default`, etc.) → informa e para com mensagem `"valor do campo **Modo:** desconhecido: <valor> — valor aceito: runbook (omitir campo para fluxo canonical)"`. Pattern paralelo a `**Branch:**` de ADR-028 (campo presente = opt-in, ausência = default total).

Combinação com outros campos especiais:
- **`**Branch:**` + `**Modo:** runbook`**: incompatível (sem worktree, branch não é checked out). Informar e parar.
- **`**Linha do backlog:**`**: aplica normalmente — §3.4 (Concluídos) preservado, único passo do gate final em modo runbook.
- **Modo local** (`paths.plans_dir: local`): ortogonal — modo runbook funciona em ambos.

Mecânica codificada em ADR-041 (novo, sucessor parcial lateral de ADR-002 e paralelo a ADR-028 § Mecânica).

## Arquivos a alterar

### Bloco 1 — docs/decisions/ADR-041 novo (paralelo ADR-028) {reviewer: doc}

- `docs/decisions/ADR-041-campo-modo-runbook-plano-opt-in.md`: criar via Write (paralelo ADR-040). Estrutura:
  - **# Título + Data 2026-05-27 + Status Proposto**
  - **§ Origem:** caso meta-system `onda-1-fs-migration` (5 mismatches enumerados); decisão base: `BACKLOG.md ## Próximos` linha de 2026-05-27 (item 1 com critério explícito "segundo plano-runbook" — overridden por operador em /triage devido a critério 2 do ADR-035); classificação editorial ADR-034 condição 5 (sucessor parcial lateral de ADR-002 — modo runbook bypassa o regime de warnings pré-loop e trilhos Aviso/Backlog/Validação; e condiciona o contrato implícito do `/run-plan` sobre worktree + diff git + reviewer per bloco; paralelo aos precedentes ADR-029→ADR-017, ADR-030→ADR-005, ADR-038→ADR-026, ADR-039→ADR-010).
  - **§ Contexto:** doutrina implícita "/run-plan aplica-se a planos cuja semântica é diff git no repo" não está codificada; runbook plans corrompem working tree silenciosamente; ADR-035 critério 2 (fronteira doutrinal nítida) justifica codificação com 1 evidência; rebut explícito ao critério "sem 2ª evidência fica como editorial" do backlog — operador absorveu trade-off em /triage com awareness explícito. **Tabela das 4 dimensões em § Decisão prefaciada como v1, derivada do caso `meta-system onda-1-fs-migration`** — codifica estrutura conceitual (campo opt-in, ADR formal) com 1 evidência, mas não fecha schema mecânico contra 2º caso: expansão sob gatilhos de revisão.
  - **§ Decisão:** 4 cláusulas — (a) campo `**Modo:**` opcional em `## Contexto` com **único valor aceito `runbook`**; ausência = fluxo canonical (default total), pattern paralelo a `**Branch:**` de ADR-028; (b) presença de `runbook` bypassa §1 / §2.5 / §2.3-2.4 / §3.1-3.3 / §3.7 do `/run-plan` — tabela v1 derivada do caso meta-system; (c) gate de confirmação por bloco substitui reviewer (pattern paralelo a §3.2 do canonical — validação manual); (d) incompatibilidades duras: `**Branch:** + **Modo:** runbook` → informa e para (defensividade pela clareza doutrinal, ADR-035 critério 2 — fronteira nítida em campo que toca state do sistema); valor `**Modo:**` diferente de `runbook` → informa e para com mensagem citando único valor aceito.
  - **§ Consequências:** benefícios (skill cobre genuinamente runbook plans + fronteira nítida visível); trade-offs (campo novo no template + lógica condicional no `/run-plan`); limitações (rollback é responsabilidade do operador, sem mecanismo formal; modo runbook não tem reviewer per bloco — invariantes ficam por conta do gate humano + revisão upstream manual por `@design-reviewer` sobre o plano antes do `/run-plan`).
  - **§ Alternativas consideradas:** (a) recusar runbook plans com mensagem clara (custo baixo mas inutiliza skill em classe legítima de uso); (c) só ADR sem código (sem enforcement, drift volta sem ajuda); (d) campo no plano + sub-skill `/run-runbook` separada (fragmenta superfície sem ganho — overhead de slash command dedicado pequeno); (e) degradar combinação `**Branch:** + **Modo:** runbook` para aviso informativo paralelo a ADR-020/ADR-002 — descartada pela natureza ambient-touching do modo runbook (defensividade contra plano-author errado pesa mais que ceremonia eliminada; ADR-035 critério 2 supera economia de mensagem); (f) aceitar `**Modo:** canonical` como valor explícito noop — descartada pelo precedente ADR-028 (campo opt-in = presente, ausência = default total) e por convidar ambiguidade lexical (`default`/`standard`/`canonical`).
  - **§ Gatilhos de revisão:** 2º caso real expor dimensão não coberta pelas 4 atuais → revisitar **estrutura** do schema (não só ampliar tabela), considerar se incompatibilidades duras se mantêm; rollback formal exigido por incidente real → adicionar mecanismo (até lá, responsabilidade do operador); reviewer-on-confirmation pattern aparecer em outra skill → promover para mecanismo compartilhado (precedente: §3.2 do `/run-plan` canonical já usa o mesmo pattern para validação manual).

### Bloco 2 — skills/run-plan/SKILL.md detecção + fluxo condicional {reviewer: code}

- `skills/run-plan/SKILL.md`:
  - **Pré-condições:** adicionar nova pré-condição **0. Detecção de modo** antes da atual #1. Lê `**Modo:**` do `## Contexto` do plano. Ausência = canonical (default total). Presença e valor `runbook` → ativa fluxo alternativo descrito abaixo. Valor diferente de `runbook` → parar com mensagem `"valor do campo **Modo:** desconhecido: <valor> — valor aceito: runbook (omitir campo para fluxo canonical)"`. Combinação `**Modo:** runbook` + `**Branch:** <nome>` → parar com mensagem `"**Modo:** runbook + **Branch:** incompatíveis — runbook executa no working tree principal, sem worktree"`.
  - **Pré-condições 1-4** em modo runbook: #1 aplica (plano existe e tem `## Arquivos a alterar`); #2 aplica (plano commitado — embora worktree não seja criada, `/run-plan` lê o plano-arquivo e edit não-commitado pode dessincronizar entre leitura inicial e blocos posteriores se operador editar mid-execução); #3 não aplica (sem baseline automático — `## Verificação end-to-end` é referência textual no done); #4 não aplica (sem worktree).
  - **Detecção de warnings pré-loop:** em modo runbook, pular tabela inteira — warnings pressupõem fluxo canonical (alinhamento dirty é sobre repo; runbook muta sistema). Skip silente.
  - **§1 Setup da worktree:** prefácio `**Em modo runbook:** pula §1 inteiro — executa no working tree principal.` (operador é responsável por backup/snapshot prévio fora da skill).
  - **§2 Loop por bloco:** captura automática Pré-loop não dispara (warnings pulados). Para cada bloco:
    1. **Implementar** — igual ao canonical (mas pode incluir comandos não-git: `mv`, `systemctl`, edits em `~/`).
    2. **Validação inline** — em modo runbook, ao invés do `test_command` global, ler a sub-seção `## Validação` ou `## Smoke test` do bloco (quando presente no plano) ou usar critério textual descrito no próprio bloco.
    3. **Substitui §2.3-2.4 (reviewer + correções) por gate de confirmação por bloco** (pattern paralelo a §3.2 do canonical — validação manual): `AskUserQuestion` (header `Bloco N`, opções `Validei e seguir` / `Falhou — descrever`). `Falhou` → operador descreve em prosa; captura emergente vira `TaskCreate` `[capture:validacao]`. **Antes de a skill parar, materializar capturas acumuladas:** ler TaskList por `[capture:*]`, escrever em `## Pendências de validação` do plano e `## Próximos` do `backlog` conforme tipo (paralelo a §3.5 do canonical, disparado pelo Falhou ao invés do gate final). Skill para após materialização. `Validei e seguir` → próximo bloco.
    4. **Sem micro-commit** — pula §2.5 (rollback é btrfs snapshot/tarball/manual, não `git revert`).
  - **§3 Gate final em modo runbook:** pula §3.1 (gate automático), §3.2 (validação manual centralizada — já intercalada por bloco), §3.3 (sanity check docs — runbook não toca docs do projeto), §3.7 (publicação — sem branch de feature). Aplica §3.4 (Concluídos) se `**Linha do backlog:**` presente — operador pode editar `backlog` no working tree principal; commit do bloco extra segue padrão canonical. §3.5 (captura automática) aplica para Tasks acumuladas durante §2 (validacao + backlog). §3.6 (declarar done) aplica.
  - **`## O que NÃO fazer`:** adicionar bullet `Não executar fluxo canonical (worktree + micro-commits + reviewer) em plano com **Modo:** runbook — modo runbook reflete que ambiente é o escopo, não o repo; aplicar canonical corrompe working tree silenciosamente.`

### Bloco 3 — templates/plan.md + CLAUDE.md cross-ref {reviewer: doc}

- `templates/plan.md`: comentário em `## Contexto` ganha nova entrada após `**Branch:**`: `**Modo:** runbook` — incluir em planos de system-surgery (operações fora de diff git: `mv`, `systemctl`, edits em `~/`, etc.); **tipicamente hand-written, não derivado de `/triage`**; bypassa worktree + micro-commit + reviewer per bloco + validação centralizada (ADR-041). Ausência = fluxo default.
- `CLAUDE.md` § "Editing conventions": adicionar bullet cross-ref a ADR-041 paralelo aos de ADR-010/011/023/026/034/035: `Modo runbook em planos de system-surgery`: per [ADR-041](docs/decisions/ADR-041-campo-modo-runbook-plano-opt-in.md) — campo opcional `**Modo:** runbook` no `## Contexto` do plano bypassa worktree + commit-per-bloco + reviewer per bloco + validação centralizada do `/run-plan`. Aplica-se a planos cuja semântica não é diff git (FS migration, system surgery, ops em `~/`). Operador gerencia rollback fora da skill (snapshot/tarball/manual).

## Verificação end-to-end

- `ls docs/decisions/ADR-041-*.md` retorna 1 arquivo.
- `grep -n "**Modo:**" skills/run-plan/SKILL.md` retorna ≥3 matches (pré-condição 0, prefácio §1, prefácio §2, prefácio §3, bullet `## O que NÃO fazer`).
- `grep -n "**Modo:**" templates/plan.md` retorna ≥1 match (comentário em `## Contexto`).
- `grep -n "ADR-041" CLAUDE.md` retorna 1 match (bullet em "Editing conventions").
- `grep -n "ADR-041" docs/decisions/ADR-041-*.md` retorna ≥0 matches (auto-ref opcional).
- Inspeção textual: pré-condição 0 do `/run-plan` discrimina os 3 caminhos (canonical / runbook / inválido) com mensagens citáveis ao operador.

## Verificação manual

- **Cenário 1 (regressão default):** plano canonical sem campo `**Modo:**` → `/run-plan` executa fluxo completo (worktree + reviewer + micro-commit + gate final). Smoke pós-release rodando `/run-plan` em qualquer plano histórico (ex.: plano fictício `cenario1-canonical-regression.md` com 1 bloco trivial; ou próximo plano real triagado).
- **Cenário 2 (modo runbook ativo):** plano de 2 blocos com `**Modo:** runbook` + cada bloco descreve operação não-git (`echo` ou `touch`/`mv` em diretório temp seguro) → `/run-plan` pula worktree, executa no working tree principal, cutuca gate de confirmação por bloco, pula gate final automático. Aplicar `/run-plan` ao próprio fixture pós-merge+reload do plugin.
- **Cenário 3 (valor inválido):** plano com `**Modo:** foo` → `/run-plan` para na pré-condição 0 com mensagem `"valor do campo **Modo:** desconhecido: foo — valor aceito: runbook (omitir campo para fluxo canonical)"`. Subteste: `**Modo:** canonical` explícito também rejeitado (não há valor noop).
- **Cenário 4 (incompatibilidade Branch + runbook):** plano com `**Modo:** runbook` e `**Branch:** alguma-branch` → `/run-plan` para na pré-condição 0 com mensagem citando incompatibilidade.
- **Cenário 5 (smoke real em consumer meta-system Onda 2/3/4):** spec para o operador rodar manualmente após release do toolkit. Aplicar `/run-plan onda-2-<slug>` (quando existir) com `**Modo:** runbook` no plano; confirmar que skill pula worktree, executa no working tree principal, cutuca gate de confirmação a cada bloco, e validações intercaladas (smoke tests do consumer) funcionam.
- **Cenário 6 (Falhou em modo runbook materializa capturas):** plano fixture de 3 blocos com `**Modo:** runbook`; simular durante bloco 1 captura emergente (operador menciona finding fora-do-escopo → skill emite `TaskCreate [capture:backlog]`); no bloco 2, simular falha (`echo` esperado falha; operador escolhe `Falhou — descrever` com prosa "comando X retornou exit 1"). Confirmar: skill cria `TaskCreate [capture:validacao]` para o Falhou + lê TaskList por `[capture:*]` + materializa **ambos** em destino correto (validacao → `## Pendências de validação`, backlog → `## Próximos`) + skill termina sem completar bloco 3.
- **Cenário 7 (Linha do backlog em runbook):** plano fixture com `**Modo:** runbook` + `**Linha do backlog:** texto-fixture` no `## Contexto`. Confirmar §3.4 transita a linha de `## Próximos` para topo de `## Concluídos` no working tree principal, commit do bloco extra segue padrão canonical Conventional Commits.

## Notas operacionais

- **Ordem dos blocos importa:** Bloco 1 (ADR) primeiro porque Blocos 2 e 3 referenciam ADR-041 pelo slug; design-reviewer audita ADR antes do mecanismo entrar.
- **Trade-off codificação prematura absorvido em /triage:** backlog item explicita "sem 2ª evidência fica como editorial". Operador escolheu (b) sob ADR-035 critério 2 (fronteira doutrinal nítida supera "esperar 2ª evidência"); design-reviewer deve auditar o critério, não relitigá-lo. § Origem do ADR-041 cita explicitamente o override.
- **Reviewer per bloco em modo runbook ausente é intencional:** invariantes do bloco ficam por conta do gate humano de confirmação. Reviewer automático sobre diff inexistente não tem trabalho a fazer — `code-reviewer` agent def já trata "diff vazio" como N/A, mas semântica fica mais clara explicitando o bypass.
- **Modo runbook recomenda invocação manual de `@design-reviewer` sobre o plano antes do `/run-plan`** — reviewer per bloco bypassed depende de qualidade pre-fact do plano. Decisões estruturais nos blocos (escolhas de path canonical, semântica de templates, ordem de operações sistêmicas) não são cobertas por confirmação humana inline — só por revisão upstream do plano-documento. Operador é responsável por executar essa revisão fora da skill ([ADR-009](../decisions/ADR-009-revisor-design-pre-fato.md), [ADR-011](../decisions/ADR-011-wiring-design-reviewer-automatico.md)).
- **Gate de confirmação por bloco não é invenção — é o mesmo pattern de §3.2 do `/run-plan` canonical** (validação manual: `AskUserQuestion` com `Validei (Recommended)` / `Falhou — descrever`). Modo runbook reusa o pattern por bloco ao invés de uma vez no done. Promoção para mecanismo compartilhado em § Gatilhos de revisão do ADR-041 contempla 2ª skill demandar o pattern.
- **Smoke real do Cenário 5 fica como spec pós-release:** operador rodará no consumer `meta-system` quando Ondas 2/3/4 existirem. Confirmação textual no plano serve de contrato.
- **Compatibilidade com pré-condição 1 (plano sujo) em modo runbook:** preservada — plano modificado/untracked ainda bloqueia. Modo runbook não muda fato de que `/run-plan` lê o plano commitado.

## Decisões absorvidas

- Bloco 1 § Origem: classificação ADR-034 trocada de condição 4 ("categoria nova") para condição 5 (sucessor parcial lateral de ADR-002) — paralelo aos precedentes ADR-029/030/038/039 (caminho-único).
- Bloco 1 § Contexto + § Gatilhos: tabela das 4 dimensões prefaciada como v1 derivada do caso meta-system; gatilho expandido para "revisitar estrutura do schema" em 2º caso real e citar §3.2 do canonical como precedente do pattern reviewer-on-confirmation (caminho-único).
- Bloco 1 § Consequências: limitação acrescenta "revisão upstream manual por `@design-reviewer` sobre o plano antes do `/run-plan`" como mitigação ao gap de reviewer per bloco ausente (caminho-único).
- Bloco 2 pré-condições 1-4 em modo runbook: pré-condição #2 (plano sujo/commitado) aplica — contradiz numeração original "#2 não aplica"; correção de typo editorial (caminho-único).
- Bloco 2 §2 item 3 (gate de confirmação): citado como "pattern paralelo a §3.2 do canonical — validação manual" para honrar precedente ao invés de tratar como invenção (caminho-único).
- Bloco 3 template entry: "tipicamente hand-written, não derivado de `/triage`" acrescentado para clarificar caso de uso e omissão YAGNI-aceitável de suporte cross-skill (caminho-único).
- `## Notas operacionais`: nova entrada recomendando invocação manual de `@design-reviewer` sobre plano antes do `/run-plan`; entrada existente sobre reviewer per bloco ausente cita §3.2 do canonical como precedente do pattern (caminho-único).
