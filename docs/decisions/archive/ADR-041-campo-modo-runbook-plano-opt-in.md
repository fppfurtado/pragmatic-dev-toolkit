> **ARCHIVED 2026-05-31** — content absorbed into [ADR-049](../ADR-049-execucao-run-plan-consolidado.md); see that ADR for current authority. Body below preserved verbatim for historical record.

# ADR-041: Campo `**Modo:** runbook` opt-in em planos para `/run-plan` cobrir system-surgery

**Data:** 2026-05-27
**Status:** Proposto

## Origem

- **Investigação:** Caso empírico observado em 2026-05-27 com plano `onda-1-fs-migration` do consumer `meta-system` (migração de filesystem PARA→functional, ~38 repos + drive-sync + chezmoi + ~/.claude + XDG + IDE workspaces). Cinco mismatches estruturais entre `/run-plan` canonical e o plano-real: (1) worktree estaria dentro do FS sendo migrado — `Bloco 3` move `.worktrees/<slug>` mid-execução; (2) 11 de 12 blocos não produzem diff git (operações `mv`, `systemctl`, `xdg-user-dirs-update`, edits em `~/.config/`, `~/.local/share/chezmoi/`, `~/.claude/*.json`, `CLAUDE.md` em N outros repos, `VBoxManage`); (3) rollback é btrfs snapshot + tarball, não `git revert` — micro-commits-per-bloco não desfazem `mv`; (4) reviewer per bloco trabalha sobre diff que não existe; (5) validação corre DURANTE (smoke tests gateiam Bloco 10 resume-drive-sync; bootstrap test em VM gateia Bloco 12), não no gate final.
- **Decisão base:** `BACKLOG.md ## Próximos` linha de 2026-05-27 registrou o mismatch com critério explícito "segundo plano-runbook em meta-system (Ondas 2/3/4) ou em outro consumer; sem 2ª evidência, fica como editorial". Operador overrode esse critério em `/triage` desta sessão (2026-05-27) escolhendo direção (b) "modo opt-in via campo `**Modo:** runbook`" sobre (a) "recusar runbook plans" e (c) "só ADR sem código", devido a critério (2) do ADR-035 "fronteira doutrinal nítida" (status quo: `/run-plan` aceita silenciosamente plano cuja semântica não bate, corrompendo working tree do operador sem mensagem).
- **Critério editorial:** [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) Condição (5) "sucessor parcial lateral — estende ADR Aceito sem revogar" aplica em relação a [ADR-002](ADR-002-eliminar-gates-pre-loop.md) (regime de warnings/trilhos pré-loop) e ao contrato implícito do `/run-plan` (worktree + diff git + reviewer per bloco). Paralelo aos precedentes ADR-029→ADR-017, ADR-030→ADR-005, ADR-038→ADR-026, ADR-039→ADR-010.
- **Qualificação YAGNI interna:** [ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) critério (2) "fronteira doutrinal borrada — categoria nova com fronteira nítida supera churn de refactor" aplica. Critério (1) "incidente recorrente" **não** dispara (1 caso empírico, não recorrente); operador absorveu o trade-off em `/triage` com awareness explícito da tensão.

## Contexto

`/run-plan` codifica contrato implícito: planos cuja semântica é diff git no repo, executados em worktree isolada com micro-commit por bloco e reviewer automático sobre o diff. Esse contrato cobre **mudança de código + docs do projeto** — feature, fix, refactor, atualização documental.

Há classe legítima de plano que não cabe nesse contrato: **system-surgery / runbook plans** — operações fora de diff git que mutam state do ambiente (filesystem migration, infra reconfig, dotfiles sync coordenado, multi-repo edits). Plano `onda-1-fs-migration` do `meta-system` é o primeiro caso empírico:

| `/run-plan` canonical assume | Runbook plan oferece |
|---|---|
| Worktree isolada em `.worktrees/<slug>` | Operações **no** working tree principal porque ambiente é o escopo |
| Cada bloco gera diff git | 11/12 blocos sem diff (operações `mv`, `systemctl`, edits em `~/`) |
| Rollback via `git revert` em micro-commits | Rollback via btrfs snapshot + tarball + manual |
| Reviewer per bloco sobre o diff | Diff inexistente → reviewer sem matéria-prima |
| Validação centralizada no gate final | Validação intercalada DURANTE (smoke tests gateiam blocos) |

Forçar `/run-plan` num runbook plan resulta em: worktree órfã + commits artificiais + execução ainda manual fora da skill. Workaround empírico atual: operador carregou a skill mas escolheu execução supervisionada manual, contornando-a.

Sem mecanismo explícito, o operador novato (sem awareness do mismatch) tentará `/run-plan` num plano de system-surgery e descobrirá só pós-fato que o working tree ficou corrupted (worktree dentro do FS migrado, commits que rollback btrfs vai sobrescrever).

### Tensão com ADR-002 (eliminação de gates pré-loop)

[ADR-002](ADR-002-eliminar-gates-pre-loop.md) § Decisão estabelece "Skill nunca interrompe por cutucada na fase pré-loop. Warning detectado é classificado e materializado no trilho Aviso/Backlog/Validação". ADR-041 introduz incompatibilidade dura (`**Branch:** + **Modo:** runbook` → informa e para) que tem natureza de gate.

Defesa: ADR-002 cobre warnings de **qualidade-de-mudança** (alinhamento dirty, escopo divergente, credencial não coberta) onde decisão majoritária é "Continuar" e a pergunta vira ritual. ADR-041 cobre **incompatibilidade semântica de campos no plano** — operador escreveu dois campos com semânticas contraditórias por engano. Categoria distinta: não é warning de qualidade ambiente, é erro de plano. Gate dura aqui não é cerimônia — é defesa contra plano-author errado em contexto que toca state do sistema (alto custo de mutação errada). ADR-002 § Limitações reconhece: "warnings que exijam decisão imediata e irreversível voltam para gate explícito". ADR-041 opera nessa exceção.

### Tensão com ADR-004 (state em git, BACKLOG editorial)

[ADR-004](ADR-004-state-tracking-em-git.md) estabelece que state de in-flight work vive em git/forge (branches, PRs); BACKLOG é registro editorial, não state-tracker. ADR-041 modo runbook executa sem branch dedicada (sem worktree) — aparentemente quebra o contrato.

Defesa: ADR-004 cobre state de **mudança de código** (onde branch é o vehicle natural). Runbook plan não é mudança de código — é execução supervisionada de operações sistêmicas. Working tree principal já é o "lugar onde o trabalho acontece"; criar branch para state-tracker de operações `mv`/`systemctl` seria cerimônia vazia. ADR-004 preservado em escopo intencional (canonical mode); ADR-041 reconhece categoria distinta onde state-tracker é o próprio sistema (snapshots/tarballs/logs do consumer), não git.

## Decisão

Adicionar campo opcional `**Modo:**` no `## Contexto` do plano com **único valor aceito `runbook`**; ausência = fluxo canonical (default total).

### Cláusulas

1. **Campo opcional, único valor aceito**: `**Modo:** runbook` ativa fluxo alternativo descrito abaixo. Ausência do campo = fluxo canonical (default total). Qualquer outro valor (`canonical`, `default`, etc.) → `/run-plan` para na pré-condição 0 com mensagem `"valor do campo **Modo:** desconhecido: <valor> — valor aceito: runbook (omitir campo para fluxo canonical)"`. Pattern paralelo a [ADR-028](ADR-028-campo-branch-opcional-plano-fluxo-issue-first.md) `**Branch:**` (campo presente = opt-in, ausência = default total).

2. **Bypass de 4 dimensões do canonical** (tabela v1 derivada do caso `meta-system onda-1-fs-migration`):

   | Dimensão (modo runbook) | Mismatch resolvido | Comportamento |
   |---|---|---|
   | Sem worktree | (1) worktree dentro do escopo de migração | Pula §1 inteiro do `/run-plan` (setup, replicação `.worktreeinclude`, sync, baseline). Executa no working tree principal. |
   | Sem commit-per-bloco | (2) blocos sem diff + (3) rollback fora do git | Pula §2.5 (micro-commit). Rollback é responsabilidade do operador (snapshot/tarball/manual). |
   | Gate de confirmação por bloco | (4) reviewer sobre diff inexistente | Substitui §2.3-2.4 (escolher revisor + aplicar correções) por `AskUserQuestion` (header `Bloco N`, opções `Validei e seguir` / `Falhou — descrever`). Pattern paralelo a §3.2 do canonical (validação manual). |
   | Validação intercalada | (5) validação durante, não no done | Cada bloco descreve sua própria validação inline. §3 (gate final) reduz a §3.4 (Concluídos via `**Linha do backlog:**`) + §3.5 (captura automática) + §3.6 (declarar done). §3.1 (gate automático), §3.2 (validação manual centralizada), §3.3 (sanity check docs), §3.7 (publicação) pulados. |

3. **Gate de confirmação por bloco com materialização de capturas no `Falhou`**: ao operador escolher `Falhou — descrever`, antes de a skill parar, materializar capturas acumuladas (ler `TaskList` por `[capture:*]`, escrever em `## Pendências de validação` do plano e `## Próximos` do `backlog` conforme tipo) — paralelo a §3.5 do canonical, disparado pelo `Falhou` ao invés do gate final. Skill termina após materialização. Evita perda de capturas dos blocos anteriores quando a execução para mid-plano.

4. **Incompatibilidades duras**:
   - `**Branch:** + **Modo:** runbook` → `/run-plan` para na pré-condição 0 com mensagem `"**Modo:** runbook + **Branch:** incompatíveis — runbook executa no working tree principal, sem worktree"`. Defensividade pela clareza doutrinal (ADR-035 critério 2 — campos com semânticas contraditórias não silenciosamente compatíveis em contexto ambient-touching).
   - Valor `**Modo:**` diferente de `runbook` → para com mensagem citando único valor aceito (cláusula 1).

### Mitigação ao gap de reviewer per bloco ausente

Modo runbook bypassa `code-reviewer`/`doc-reviewer` per bloco. Invariantes do bloco ficam por conta de **gate humano de confirmação inline + revisão upstream manual** por `@design-reviewer` ([ADR-009](ADR-009-revisor-design-pre-fato.md), [ADR-011](ADR-011-wiring-design-reviewer-automatico.md)) sobre o plano-documento antes de invocar `/run-plan`. Operador é responsável por executar essa revisão fora da skill; doc do template e nota operacional do plano sinalizam a recomendação.

## Consequências

### Benefícios

- `/run-plan` cobre genuinamente runbook plans em vez de corromper working tree silenciosamente.
- Fronteira nítida visível ao operador novato — campo no template torna a distinção explícita.
- Reuso de mecanismos existentes: confirmation gate é o mesmo pattern de §3.2 canonical (validação manual); materialização do `Falhou` é o mesmo pattern de §3.5; transição `## Concluídos` (§3.4) preservada.

### Trade-offs

- Campo novo no template + lógica condicional no `/run-plan` (custo de manutenção: 1 campo, 1 ramificação no fluxo, 4 dimensões de bypass).
- Reviewer per bloco ausente em modo runbook: invariantes dependem de gate humano inline + revisão upstream manual. Plugin não força a revisão upstream — confia no operador. Mitigado por nota operacional explícita no template e nas `## Notas operacionais` do plano.
- Codificação com 1 evidência empírica: tabela v1 derivada do caso `meta-system onda-1-fs-migration` pode não cobrir dimensão de 2º caso real (rollback formal? validação cross-stack? checkpointing parcial?). Expansão sob gatilhos de revisão; estrutura conceitual codificada agora, schema mecânico aberto a revisão.

### Limitações

- **Rollback é responsabilidade do operador**: sem mecanismo formal (snapshot, tarball, manual). Plugin não orquestra rollback de operações sistêmicas. Reabrir se incidente real de rollback exigir mecanismo.
- **Reviewer per bloco ausente sem substituto automático**: depende de qualidade pre-fact do plano. Plugin não força revisão upstream — operador é responsável.
- **Modo runbook não tem cobertura cross-skill em `/triage`**: campo é tipicamente hand-written, não derivado de `/triage`. `/triage` step 2 não cutuca "este plano é runbook?". Aceito (YAGNI ADR-035 — pattern emergente <3x ad hoc).

## Alternativas consideradas

### (a) Recusar runbook plans com mensagem clara

`/run-plan` detecta heurística runbook (ex.: `## Arquivos a alterar` lista paths sob `~/`, comandos `systemctl`/`mv` no plan body) e informa-e-para citando ADR. Descartada: inutiliza skill em classe legítima de uso; operador ainda precisa execução supervisionada manual sem disciplina (sem confirmation gate, sem captura de imprevistos). Pior UX que modo opt-in.

### (c) Só ADR documentando fronteira sem código

ADR registra que runbook plans estão fora-do-escopo de `/run-plan`; operador escolhe não invocar a skill manualmente. Descartada: sem enforcement, drift volta sem ajuda — operador novato sem awareness do ADR tenta `/run-plan` e descobre o mismatch pós-fato. Doutrina sem mecanismo é frágil em contexto operacional.

### (d) Sub-skill `/run-runbook` separada

Campo no plano + sub-slash command dedicado para o modo runbook. Descartada: fragmenta superfície sem ganho — overhead de slash command novo (frontmatter, naming, descoberta) supera 1 ramificação condicional dentro do `/run-plan`. Pattern paralelo a `**Branch:**` de ADR-028 (campo no plano dispara fluxo alternativo dentro da mesma skill, não skill nova).

### (e) Degradar combinação `**Branch:** + **Modo:** runbook` para aviso informativo

Paralelo a ADR-020/ADR-002 (warnings não-bloqueantes pré-loop). Descartada pela natureza ambient-touching do modo runbook: defensividade contra plano-author errado pesa mais que ceremonia eliminada; ADR-035 critério (2) "fronteira doutrinal nítida" supera economia de mensagem em contexto que toca state do sistema. Cf. § "Tensão com ADR-002" acima — ADR-002 § Limitações reconhece exceção para "decisão imediata e irreversível".

### (f) Aceitar `**Modo:** canonical` como valor explícito noop

Permitir `**Modo:** canonical` como autodocumentação ("este plano *é* canonical, não esqueci de declarar"). Descartada pelo precedente ADR-028 (`**Branch:**` não aceita valor noop — campo opt-in = presente, ausência = default total) e por convidar ambiguidade lexical (operador erra `default`/`standard`/`canonical`, recebe erro confuso). Mensagem de erro fica mais curta com 1 valor aceito.

## Implementação

- `docs/plans/modo-runbook-plano-opt-in.md` — plano corrente que implementa esta decisão em 3 blocos (ADR + skill + template/CLAUDE.md).
- `skills/run-plan/SKILL.md` — adiciona pré-condição 0 (detecção do modo), prefácios em §1/§2/§3 condicionais, gate de confirmação por bloco com materialização de capturas no `Falhou`, bullet em `## O que NÃO fazer`.
- `templates/plan.md` — entrada `**Modo:** runbook` no comentário de `## Contexto` após `**Branch:**`.
- `CLAUDE.md § Editing conventions` — bullet cross-ref a este ADR paralelo aos de ADR-010/011/023/026/034/035.

## Gatilhos de revisão

- **2º caso real expor dimensão não coberta pelas 4 atuais**: revisitar **estrutura** do schema (não só ampliar tabela), considerar se incompatibilidades duras se mantêm; tabela v1 foi codificada com 1 evidência (operador absorveu trade-off em `/triage`) — schema mecânico aberto à revisão.
- **Rollback formal exigido por incidente real**: operador relata perda de trabalho por ausência de mecanismo de rollback (snapshot, tarball, manual insuficiente) — adicionar mecanismo opcional (`**Rollback:**` field? hook pre-bloco?). Até lá, responsabilidade do operador.
- **Reviewer-on-confirmation pattern aparecer em outra skill**: pattern reviewer-on-confirmation é genérico (state-keeping via `AskUserQuestion` substituindo reviewer automático). Precedente: §3.2 do `/run-plan` canonical já usa o pattern para validação manual. ADR-041 reusa por bloco ao invés de uma vez no done. Se 2ª skill (não `/run-plan`) demandar o pattern, promover para mecanismo compartilhado (`docs/procedures/reviewer-on-confirmation.md`?) per [ADR-024](ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md).
- **Pedido de suporte cross-skill em `/triage`**: operador relata wanting `/triage` step 2 cutucar "este plano é runbook?" — reabrir omissão YAGNI documentada em § Limitações.
- **Falso-positivo de rejeição de valor `**Modo:**`**: operador usa valor não previsto que faria sentido em contexto futuro — ampliar conjunto aceito (mas resistir a `canonical` explícito por precedente ADR-028).
