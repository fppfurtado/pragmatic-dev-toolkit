# ADR-010: Instrumentação de progresso em skills multi-passo via Tasks

**Data:** 2026-05-08
**Status:** Aceito

## Origem

- **Investigação:** Tools `TaskCreate`/`TaskUpdate` do harness Claude Code podem tornar progresso de skills multi-passo visível ao operador (UI da harness) e resiliente a context compression em sessões longas. Padrão atual (prosa-only + commits) torna o progresso invisível e dependente de releitura do diff.
- **Decisão base:** padrão emergente até v2.0.0 — skills do plugin tracking de progresso implícito via prosa de execução + commits. Sem mecanismo estruturado de "qual passo discreto está rodando agora?".

## Contexto

Estado anterior:

- `/run-plan` executa loop por bloco + gate final em ≥4 sub-passos. Operador acompanha via output do agent linha a linha.
- `/debug` mantém ledger de hipóteses em prosa narrativa, com status implícito ("testei X, falhou; vou testar Y").
- Sem estado estruturado, recovery pós-context-loss é frágil — modelo precisa releer todo o diff/conversa para recompor "onde paramos".

Pressões para instrumentação:

1. **Sessões longas**: `/run-plan` em planos com 5+ blocos pode rodar dezenas de minutos. Progresso silencioso obscurece "está travado?" vs "está executando bloco X".
2. **Context compression**: harness comprime mensagens antigas. Progresso codificado só em prosa cai do contexto; Tasks são metadata estruturada que sobrevive.
3. **Investigação multi-hipótese em `/debug`**: ledger-prosa fica disperso ao longo do diálogo; status de cada hipótese exige releitura.

Pressões contra instrumentação universal:

1. **Skills shot-output** (`/triage` end-to-end, `/new-adr` cria-arquivo, `/gen-tests` gera teste) executam ~1 passo perceptível — Tasks aparecem só para fechar imediatamente, ruído visual.
2. **`/release`** tem 4 sub-passos, mas cada um é <10s em uso típico — overhead de Task supera valor.
3. **Acoplamento ao harness**: `TaskCreate`/`TaskUpdate` são contrato Claude Code-specific; runtime alternativo quebra.

## Decisão

**Skills com ≥3 passos sequenciais discretos instrumentam progresso via `TaskCreate` + `TaskUpdate`.** Skills shot-output ou com sub-passos triviais (<10s típicos) **não** instrumentam.

**Tasks são conversation-scoped**: lifecycle dura uma invocação da skill; não persistem entre sessões. State de longa duração permanece em git/forge per ADR-004 — Tasks complementam, não substituem.

### Escopo de aplicação

- **Aplica-se:** `/run-plan` (loop por bloco + sub-passos do gate final); `/debug` (ledger de hipóteses).
- **Não aplica-se:** `/triage`, `/new-adr`, `/gen-tests` (shot-output); `/release` (sub-passos <10s típicos — caso-limite, reabrir se release ficar lento).
- **Skills futuras:** aplicar critério "≥3 passos sequenciais discretos" como heurística; em dúvida, preferir não-instrumentar (overhead silencioso supera ruído visível).

### Mecânica

- `TaskCreate(content="<descrição>", status="pending")` ao identificar passo. **Avaliar condição de skip antes de `TaskCreate`** — evitar Tasks que abrem só para fechar.
- `TaskUpdate(status="in_progress")` ao iniciar execução do passo.
- `TaskUpdate(status="completed")` ao concluir.
- Status semântico (sucesso/falha/descarte) vai em prosa do report ao operador, não na Task.

## Consequências

### Benefícios

- **Progresso visível**: operador vê em UI da harness qual passo está rodando, sem releitura de logs.
- **Resiliência a context compression**: Tasks sobrevivem a compactação; recovery pós-context-loss usa Tasks como ponto de retomada.
- **Complementa narrativa**: `/debug` mantém ledger-prosa para raciocínio causal; Tasks substituem só o tracking de status.

### Trade-offs

- **Acoplamento ao harness**: `TaskCreate`/`TaskUpdate` são tools Claude Code-specific; runtime alternativo quebra sem fallback graceful. Aceito por construção do toolkit (análogo a `git`/`gh` per ADR-005).
- **Critério "≥3 passos discretos" tem zona cinza**: skill nova com workflow misto (parte discreta + parte streaming) precisará nova categoria; gatilho de revisão.
- **Ruído visual em planos triviais**: mitigado por escopo restrito a `/run-plan`/`/debug` + skip de Tasks que abrem só para fechar (ver Mecânica).

## Alternativas consideradas

- **Status quo (prosa-only + commits)** — descartado: progresso invisível, recovery pós-context-loss frágil, ledger de `/debug` disperso.
- **Tasks para todas as skills (incluindo shot-output)** — descartado: `/triage`/`/new-adr`/`/gen-tests` produzem ~1 Task que aparece só para fechar; ruído visual sem ganho.
- **Tasks com persistência cross-session** — descartado: git/forge já é fonte de verdade para state-of-work per ADR-004; duplicaria mecanismo e exigiria reconciliação.
- **Hook de SessionStart cutucando "tarefas em aberto"** — descartado: hook não acessa state estruturado de Tasks (são conversation-scoped); auto-gating por projeto consumidor torna heurística complexa para ganho marginal.

## Gatilhos de revisão

- **Operador reporta Tasks atrapalham fluxo** — reabrir critério "≥3 passos sequenciais discretos"; talvez subir o threshold ou tornar opt-in.
- **Skill nova surge com workflow misto** (passos discretos + execução streaming) — reabrir para definir nova categoria de instrumentação.
- **Harness muda contrato de Tasks** (renomeia, remove, ou refatora API) — reabrir acoplamento; avaliar shim ou abandono.
- **`/release` fica lento** (passos discretos chegando a >30s) — reabrir caso-limite excluído; pode entrar no escopo.
