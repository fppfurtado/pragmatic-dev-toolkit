# Plano — Wiring automático do design-reviewer no /triage e /new-adr

## Contexto

[ADR-011](../decisions/ADR-011-wiring-design-reviewer-automatico.md) decide o wiring oficial do `design-reviewer`: dispara automaticamente em `/triage` que produz plano ou ADR (passo 6, pré-commit) e em `/new-adr` standalone (pré-retorno). Este plano implementa o wiring nas SKILLs e ajusta artefatos relacionados.

**Janela de dogfood fechada (2026-05-08):** 7 findings cumulativos em 3 invocações reais (memory `project_design_reviewer_dogfood`). Padrão observado: 100% das invocações úteis ocorreram em `/triage` pré-commit. Detalhes em ADR-011 → `## Contexto`.

**Continuidade doutrinária:** ADR-009 estabeleceu o reviewer document-level com free-read; ADR-011 ativa o gate sem alterar mecanismo. ADR-002 ("eliminar gates de cutucada quando trilho automático cobre") aplicado — sem cutucada de pré-execução; findings são o trilho.

**Linha do backlog:** plugin: wiring automático do `design-reviewer` — após dogfood acumular evidência, decidir se vira gate em `/run-plan` pré-loop (revisão obrigatória do plano antes do loop de blocos) e/ou em `/new-adr` pré-commit (revisão do ADR draft). Reavaliar trade-off de tokens em alta frequência (free-read de `docs/decisions/` + `philosophy.md` por invocação). Captura prevista no plano `docs/plans/agent-design-reviewer.md`.

## Resumo da mudança

Materializar a decisão de ADR-011 nas SKILLs e docs:

1. `/triage` passo 6 dispara `design-reviewer` automaticamente quando o caminho produziu plano ou ADR (não em linha-pura, não em atualização de domínio standalone). Findings reportados antes da cutucada de commit; operador aplica ou segue como está.
2. `/new-adr` invoca `design-reviewer` no ADR draft após criar o arquivo, antes de devolver controle. Findings reportados; operador edita antes do commit (que ainda é responsabilidade externa: `/triage` ou comando manual).
3. `agents/design-reviewer.md` `description` atualizada para refletir wiring oficial (não mais só "manual via @-mention").
4. `CLAUDE.md` ganha bullet curto em "Editing conventions" apontando para ADR-011.
5. Memory `project_design_reviewer_dogfood` encerra (operação fora do repo; nota nas Notas operacionais).

Fica de fora:
- Wiring em `/run-plan` (descartado em ADR-011 alternativa (a) — gate tarde).
- Cutucada `Rodar reviewer? Sim/Não` antes do dispatch — descartado em ADR-011 (cerimônia ADR-002).
- Bloqueio do commit por findings — `design-reviewer` reporta, não bloqueia (override por inação).
- Curadoria semi-automática de ADRs lidos pelo free-read — gatilho de revisão registrado em ADR-011 e ADR-009; reavaliar se volume de ADRs ultrapassar ~30.

## Arquivos a alterar

### Bloco 1 — /triage passo 6 dispara design-reviewer (caminho-com-plano apenas) {reviewer: code}

- `skills/triage/SKILL.md`: refinar o passo 6 (Reportar, propor commit e devolver controle).
  - **Antes da cutucada de Commit**, adicionar sub-passo: "Quando o caminho produziu plano (caminho-com-plano, com ou sem ADR delegada via `/new-adr`), invocar `@design-reviewer` apontando para o plano. Reportar findings ao operador (sem cutucada de pré-execução). Findings são informativos; operador aplica ajustes antes do commit ou segue como está."
  - **Não disparar** quando o caminho é ADR-only delegada (sem plano), linha de backlog pura, ou atualização cirúrgica de `docs/domain.md`/`docs/design.md`. ADR-only é coberta pelo wiring do `/new-adr` (Bloco 2) — evita dispatch duplo no caminho `/triage` → `/new-adr` → reviewer.
  - Ajustar `## O que NÃO fazer` se cabível: adicionar item se a reclamação editorial for não-óbvia (e.g., "Não bloquear commit por findings — reviewer reporta, não decide"). Avaliar critério editorial CLAUDE.md → "Critério editorial".

### Bloco 2 — /new-adr invoca design-reviewer pré-retorno {reviewer: code}

- `skills/new-adr/SKILL.md`: adicionar passo após "Validação" (ou novo sub-passo dentro dela): "Invocar `@design-reviewer` no ADR draft recém-criado. Reportar findings ao operador antes de devolver controle. Findings são informativos; operador edita antes do commit (que é responsabilidade externa: `/triage` ou comando manual do operador, conforme a linha de prosa atual da skill)."
  - Manter compatibilidade com modo local: ADR em `.claude/local/decisions/` é lido normalmente pelo reviewer (caminho resolvido pelo Resolution protocol).

### Bloco 3 — agents/design-reviewer.md description {reviewer: doc}

- `agents/design-reviewer.md`: atualizar `description` no frontmatter para refletir wiring oficial. Frase atual termina com "Acionar manualmente via @-mention apontando o documento, antes de aprovar plano ou finalizar ADR." → reescrever para "Acionado automaticamente em `/triage` que produz plano/ADR e em `/new-adr` standalone (per ADR-011); manualmente via @-mention para revisar planos/ADRs em outros pontos."

### Bloco 4 — CLAUDE.md aponta para ADR-011 {reviewer: doc}

- `CLAUDE.md`: em `## Editing conventions`, adicionar bullet curto na lista existente apontando para ADR-011. Espelhar o estilo do bullet de ADR-010 já presente. Conteúdo proposto: `**Wiring automático do design-reviewer**: ver [ADR-011](docs/decisions/ADR-011-wiring-design-reviewer-automatico.md) — quando dispara, override por inação, custo de tokens.`

## Verificação end-to-end

- `grep -n "design-reviewer\|@design-reviewer" skills/triage/SKILL.md` retorna ao menos 1 linha no passo 6 com a regra de dispatch.
- `grep -n "design-reviewer\|@design-reviewer" skills/new-adr/SKILL.md` retorna ao menos 1 linha no passo de Validação.
- `grep -n "ADR-011" CLAUDE.md` retorna o bullet adicionado em "Editing conventions".
- Releitura textual de `agents/design-reviewer.md` confirma `description` reflete wiring oficial sem perder a possibilidade de invocação manual.
- `git log --oneline` no fim do `/run-plan` mostra 4 micro-commits (um por bloco) na branch da feature.

## Verificação manual

Surface não-determinística (comportamento de agente LLM disparando reviewer com free-read). Forma do dado real: 7 findings cumulativos do dogfood (memory `project_design_reviewer_dogfood`) servem como baseline do que o reviewer reporta. Cenários:

1. **/triage produz plano novo → reviewer dispara automático.** Plano-fixture com decisão estrutural óbvia (e.g., escolha de persistência sem alternativa rebatida). Esperado: `/triage` passo 6 invoca `@design-reviewer`; findings reportados ao operador; cutucada de commit acontece **depois** dos findings (operador aplica ou segue). Sem pergunta `Rodar reviewer? Sim/Não` (default-on).

2. **/triage fecha em linha-pura → reviewer não dispara.** Pedido pequeno que vira só linha em `## Próximos`. Esperado: passo 6 commita sem invocar reviewer (caminho-sem-plano).

3. **/new-adr standalone → reviewer dispara no draft.** Operador chama `/new-adr "<título>"` direto (fora de `/triage`). Esperado: skill cria arquivo, invoca `@design-reviewer` no ADR draft, reporta findings, devolve controle ao operador. Operador edita o ADR antes de commitar manualmente.

4. **/run-plan → reviewer NÃO dispara automaticamente.** Confirmar que o wiring novo não estende inadvertidamente para `/run-plan` pré-loop (gate fora de escopo do ADR-011).

5. **Override por inação.** Operador vê findings, decide ignorar, commita. Confirmar que skill não bloqueia — findings são reportados, fluxo segue.

6. **/triage produz ADR-only via /new-adr (caminho delegado) → reviewer dispara uma vez, não duas.** `/triage` passo 3 escolhe "ADR via /new-adr" e invoca `/new-adr` no passo 4. `/new-adr` invoca `@design-reviewer` no draft (Bloco 2). Esperado: passo 6 do `/triage` **não** redispara o reviewer — caminho ADR-only delegada não qualifica como "produz plano" (não há plano), e o ADR já passou pelo wiring do `/new-adr`. Findings reportados uma única vez. Boundary entre Bloco 1 (`/triage` passo 6) e Bloco 2 (`/new-adr`) é o ponto sutil — fácil regredir para dispatch duplo (ambos disparam) ou nenhum (passo 6 do `/triage` assume `/new-adr` cobriu, mas a regra de "produz plano ou ADR" é interpretada de forma a incluir ADR-only delegada).

## Notas operacionais

- **Memory `project_design_reviewer_dogfood` encerra após este plano mergear** (operação fora do repo, não entra em commit). MEMORY.md remove o pointer; o arquivo `project_design_reviewer_dogfood.md` pode ser arquivado ou deletado conforme convenção do operador. Critério da própria memory: *"Memory encerra quando a linha 'wiring automático do design-reviewer' sair de ## Próximos"*.
- **Memory `feedback_concrete_referrers_before_prompt`** continua válida (independente deste plano); manutenção segue pelas Notas operacionais do plano `run-plan-3-3-skip-empirico`.
- **Ordem dos blocos importa pouco** — blocos 1 e 2 mexem em SKILLs diferentes; blocos 3 e 4 são doc-updates independentes. Único acoplamento: blocos 3 e 4 são doc-only (`{reviewer: doc}`), enquanto 1 e 2 são SKILL de implementação (`{reviewer: code}`).
- **`/triage` passo 6 já tem ramificação por caminho (linha pura / plano / ADR / domain).** O dispatch do reviewer entra como sub-passo dessa ramificação, não como gate global.
- **Trade-off de tokens reconhecido em ADR-011:** `/triage` que produz plano/ADR fica ~12k tokens mais caro. Aceitável dado ROI empírico do dogfood (5+ findings por release).
