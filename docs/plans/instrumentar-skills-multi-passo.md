# Plano — Instrumentar skills multi-passo via tools do harness

## Contexto

Análise sistemática (sessão 2026-05-07) das tools do harness (built-in + deferred) identificou 6 oportunidades concretas de incorporação em skills do plugin para melhorar visibilidade, latência e determinismo. Este plano consolida todas em uma única passagem coordenada.

**Princípio editorial**: priorizar adições mecânicas (TaskCreate em loops, Monitor em comandos longos, paralelismo explícito). O critério de **quando aplicar Tasks** (≥3 passos sequenciais discretos) é estrutural — governa skills futuras e tem trade-off contencioso (ver fora-de-escopo: `/release` admite o caso-limite); é elevado a ADR neste plano (Bloco 1).

**Decisões-chave:**

1. **TaskCreate aplica-se a skills multi-passo (≥3 passos sequenciais discretos)**: `/run-plan` (loop por bloco + sub-steps do gate final) e `/debug` (hypothesis ledger). Skills shot-output (`/triage` end-to-end, `/new-adr` cria-arquivo, `/gen-tests` gera teste) **não** instrumentam — overhead supera valor. Doutrina detalhada elevada a ADR-010 (Bloco 1).
2. **Tasks são conversation-scoped**: lifecycle dura uma invocação da skill. Não persistem entre sessões — não tentar usar como state-tracker de longa duração (esse papel já é git/forge per ADR-004).
3. **Monitor para `test_command`** quando suite é não-trivial. Aplicação atual: sempre que `test_command` está configurado e não-null. Alternativas descartadas: (a) gate por estimativa via path contract (`test_command_streaming: false`) — YAGNI até pain emergir, exige novo campo de schema; (b) gate só em primeira execução por sessão — operador valoriza streaming consistente, não primeira. Reavaliar (a) se overhead aparente em suites rápidas surgir.
4. **Paralelismo explícito** em prosa de skill onde já é independente: `/run-plan` §0 (detecção de candidatos cleanup) e §2.3 (reviewer combinations `{reviewer: code,qa}` etc.). Modelo já tende a paralelizar, mas prosa atual não amarra → serialização acidental possível.
5. **`Skill` tool explícito em `/triage`** (passo 4 ADR e step 1 fallback `/next`): substituir prosa "invocar /new-adr" por chamada Skill direta. Determinismo ↑ (modelo às vezes tenta criar ADR direto, ignorando a skill dedicada).

**Acoplamento ao harness reconhecido**: tools `TaskCreate`/`TaskUpdate`/`Monitor`/`Skill` são contrato do harness Claude Code. Plugin assume disponibilidade. Não há fallback graceful — skill executando em runtime que não exponha essas tools degrada para erro de tool ausente. Aceito porque o toolkit é Claude Code-specific por construção (cf. `.claude-plugin/plugin.json`). Trade-off: análogo ao acoplamento implícito a `git`/`gh` que ADR-005 reconheceu.

**Item deferido (registrado em BACKLOG `## Próximos` separadamente):**
- Paralelização de verificação "já implementado?" em `/next` via Agent (Explore) por candidato. YAGNI até backlog crescer ≥20 itens ou pain real surgir.

**ADRs tocadas:** ADR-002 (eliminar gates pré-loop) — compatível: Tasks adicionam visibilidade sem virar gate ou cutucada nova. ADR-004 (state-tracking em git) — relevante: Tasks são conversation-scoped, não substituem state-tracker. ADR-009 (design-reviewer doc-level) — sem interação direta; este plano não toca reviewers.

**Linha do backlog:** plugin: instrumentar skills multi-passo via tools do harness — TaskCreate em `/run-plan` loop e `/debug` ledger; Monitor para `test_command` longo; explicitar paralelismo em `/run-plan` §0 e §2.3 e Skill tool em `/triage`; convenção em CLAUDE.md.

## Resumo da mudança

1. ADR-010 "Instrumentação de progresso em skills multi-passo via Tasks" — formaliza critério "≥3 passos sequenciais discretos", lifecycle conversation-scoped, e relação com ADR-004.
2. `skills/run-plan/SKILL.md`: TaskCreate por bloco do loop §2 + por sub-step do gate final §3 (apenas para sub-passos que efetivamente vão executar); Monitor envolvendo `test_command` em §1.3 e §3.1; paralelismo explícito em §0 e §2.3.
3. `skills/debug/SKILL.md`: TaskCreate por hipótese do ledger; lifecycle (in_progress ao testar, completed ao verificar/descartar).
4. `skills/triage/SKILL.md`: substituir "invocar /new-adr" e fallback `/next` por chamadas Skill explícitas.
5. `CLAUDE.md`: pointer curto em `## Editing conventions` para ADR-010 (não duplicar conteúdo doutrinário).

Fora de escopo (deferido):
- `/next` parallel Explore por candidato — linha separada em `## Próximos`.
- TaskCreate em `/release` 4 sub-passos — passos curtos (<10s cada), valor marginal; reabrir se release ficar lento. Caso-limite que motivou elevação do critério a ADR.
- `mcp__github__*` como tier no auto-detect-forge — depende do item `auto-detect-forge` em `## Próximos`; tratar lá.
- `WebSearch` em `/debug` — escopo grande, consumer-stack-specific, baixo sinal de pain.

## Arquivos a alterar

### Bloco 1 — ADR-010 critério de instrumentação via Tasks {reviewer: code}

- `docs/decisions/ADR-010-*.md` (criar via tool **Skill** com nome **pragmatic-dev-toolkit:new-adr** e args **"Instrumentação de progresso em skills multi-passo via Tasks"**).
  - **Contexto**: até v1.25.0, skills do plugin tracking de progresso via prosa+commits (implícito). Tools `TaskCreate`/`TaskUpdate` do harness oferecem rastreio estruturado conversation-scoped.
  - **Decisão**: skills multi-passo (≥3 passos sequenciais discretos) instrumentam progresso via `TaskCreate`/`TaskUpdate`. Skills shot-output (`/triage`, `/new-adr`, `/gen-tests`) **não** instrumentam.
  - **Justificativa**: visibilidade ↑, sobrevive a context compression, complementa narrativa de prosa em `/debug`. Conversation-scoped: state de longa duração permanece em git/forge per ADR-004 (sem sobreposição).
  - **Consequências**: (a) Benefícios — progresso visível no UI da harness; recovery mais robusto pós-context-loss. (b) Trade-offs — acoplamento ao harness (ver Acoplamento ao harness no plano `instrumentar-skills-multi-passo`); `/release` em ~10s/passo é caso-limite descartado por valor marginal. (c) Limitações — Tasks não substituem git/forge para state cross-session.
  - **Alternativas consideradas**:
    - Status quo (prosa-only) — descartado: progresso invisível, recovery frágil pós-context-loss.
    - Tasks para todas as skills (incluindo shot-output) — descartado: overhead supera valor; UI ruidoso.
    - Tasks com persistência cross-session — descartado: git/forge já é fonte de verdade per ADR-004; duplicaria mecanismo.
  - **Gatilhos de revisão**: (1) operador reporta Tasks atrapalham fluxo → reabrir critério "≥3 passos"; (2) skill nova com workflow misto (parte discreta + parte streaming) → critério precisa nova categoria; (3) harness muda contrato de Tasks → reabrir acoplamento (ver `feedback_adr_threshold_doctrine.md`).

### Bloco 2 — TaskCreate em `/run-plan` loop + gate sub-steps {reviewer: code}

- `skills/run-plan/SKILL.md`:
  - **§2 loop por bloco**: antes do "Para cada subseção do plano", adicionar `TaskCreate` para cada subseção de `## Arquivos a alterar` com `content: "<header do bloco sem anotação>"` e `status: "pending"`. Ao iniciar cada bloco: `TaskUpdate(status="in_progress")`. Após micro-commit do bloco: `TaskUpdate(status="completed")`.
  - **§3 gate final — TaskCreate apenas para sub-passos que efetivamente vão executar** (avaliar condições de skip antes de `TaskCreate`, não criar Task que pulará): "Gate automático" sempre; "Validação manual" só se plano tem `## Verificação manual`; "Sanity check de docs" só quando condições de skip não disparam; "Registro em Concluídos" só se há `**Linha do backlog:**`; "Captura automática" só se há listas não-vazias acumuladas. Status updates idem ao loop.
  - **Skip silente** quando o plano tem 1 bloco único E gate avaliado tem ≤1 sub-step efetivo — instrumentação foi para multi-passo, não single-shot. Aplicação corrigida (Finding 4 do dogfood inicial): evita ruído visual de Tasks que aparecem só para pular.
  - Mensagem ao operador: ao primeiro `TaskCreate` da invocação, prosa curta `"Acompanhando progresso via Tasks."` Sem cutucada subsequente — Tasks são visíveis no UI da harness.

### Bloco 3 — TaskCreate em `/debug` hypothesis ledger {reviewer: code}

- `skills/debug/SKILL.md`:
  - Onde a skill hoje mantém ledger de hipóteses em prosa, substituir por: cada nova hipótese gerada → `TaskCreate(content="Hipótese: <descrição>", status="pending")`. Ao começar a testar: `TaskUpdate(status="in_progress")`. Ao verificar (confirmada) ou descartar: `TaskUpdate(status="completed")` com nota textual no próximo report ao operador (status semântico — "confirmada" / "descartada" — vai no report, não na Task; Task só carrega progresso).
  - Manter ledger em prosa como complemento (raciocínio causal) — Tasks substituem só o tracking de status, não a narrativa.
  - **Skip silente** se diagnóstico fecha com 1 hipótese (caminho rápido) — instrumentação é para investigação multi-hipótese.

### Bloco 4 — Monitor em `/run-plan` test_command streaming {reviewer: code}

- `skills/run-plan/SKILL.md`:
  - **§1.3 baseline** e **§3.1 gate automático integral**: substituir `Bash(test_command)` por `Bash(test_command, run_in_background=true)` + `Monitor` para streamar stdout em tempo real. Operador vê output linha-a-linha em vez de espera silenciosa.
  - **Skip silente** quando `test_command` é null (já tratado), OU heurística de tempo: skill mantém uma estimativa textual (default "≥5s") embutida na prosa — operador pode override em `<!-- pragmatic-toolkit:config -->` futura via `test_command_streaming: false` (não criar campo agora; deixar prosa indicar quando vale).
  - Aplicação atual: sempre que `test_command` está configurado e não-null. Reavaliar se overhead aparente em suites rápidas.

### Bloco 5 — Paralelismo explícito + Skill tool explícito {reviewer: code}

- `skills/run-plan/SKILL.md`:
  - **§0 cleanup pós-merge**: na "Detecção de candidatos" passo 3 (verificar merge status por candidato via `gh pr list`), adicionar frase: `"Quando há ≥2 candidatos, executar as N chamadas em paralelo via múltiplas Bash calls em uma única mensagem — não serializar."`
  - **§2.3 reviewer combinations**: na descrição de `{reviewer: code,qa}` etc., adicionar: `"Quando combinação tem ≥2 reviewers, invocar todos em paralelo (múltiplas chamadas Agent em uma única mensagem) e agregar relatórios — serializar perde latência sem ganho."`

- `skills/triage/SKILL.md`:
  - **Step 4 ADR**: trocar `"ADR: invocar /new-adr <título>"` por `"ADR: chamar a tool **Skill** com nome **pragmatic-dev-toolkit:new-adr** e args **<título>** — não criar o arquivo manualmente."`
  - **Argumentos / step 1**: trocar `"Input vazio... → seguir skills/next/SKILL.md"` por `"Input vazio... → chamar a tool **Skill** com nome **pragmatic-dev-toolkit:next** sem args."`

### Bloco 6 — CLAUDE.md: pointer para ADR-010 {reviewer: doc}

- `CLAUDE.md`:
  - Em `## Editing conventions`, adicionar bullet curto apontando para ADR-010 (não duplicar conteúdo doutrinário, espelhar estilo dos outros bullets que apontam para `philosophy.md`):
    > - **Instrumentação de progresso em skills multi-passo via Tasks**: ver [ADR-010](docs/decisions/ADR-010-instrumentacao-progresso-skills-multi-passo.md) — critério de aplicação, lifecycle conversation-scoped, relação com ADR-004.

## Verificação end-to-end

Repo sem suite (`test_command: null`). Inspeção textual:

1. `docs/decisions/ADR-010-*.md` existe, status "Aceito", contém `## Decisão` com critério "≥3 passos sequenciais discretos" e seção `## Alternativas consideradas` rebatendo as 3 opções competidoras.
2. `skills/run-plan/SKILL.md` §2 menciona `TaskCreate` por bloco com lifecycle pending → in_progress → completed; §3 idem para sub-passos do gate, **com avaliação de skip antes do `TaskCreate`** (não cria Task que vai pular).
3. `skills/run-plan/SKILL.md` §1.3 e §3.1 mencionam `Monitor` para streaming de `test_command`.
4. `skills/run-plan/SKILL.md` §0 e §2.3 têm frase explícita sobre paralelismo de chamadas.
5. `skills/debug/SKILL.md` substitui ledger-prosa por TaskCreate por hipótese, mantendo prosa como narrativa.
6. `skills/triage/SKILL.md` step 4 e step 1 referenciam tool **Skill** explicitamente em vez de "invocar".
7. `CLAUDE.md` em `## Editing conventions` tem bullet curto apontando para `ADR-010` (não duplica doutrina).

## Verificação manual

**Surface não-determinística**: comportamento de modelo executando skill com Tasks visíveis (impacto em flow) e Monitor streaming (timing de updates). Cenários enumerados:

**Forma do dado real**:
- Tasks aparecem no UI da harness à medida que skill executa.
- Monitor stream produz N updates de stdout (N=número de linhas do test output).

**Cenários** (executar contra `/run-plan` em plano-fixture):

1. **Plano de 4 blocos com TaskCreate**: invocar `/run-plan` em plano com 4 blocos + gate com 3 sub-passos. Esperado: 7 Tasks visíveis, transição visível pending → in_progress → completed conforme execução. Operador valida via UI.
2. **Plano de 1 bloco**: invocar `/run-plan` em plano com 1 bloco único e gate trivial. Esperado: skip silente da instrumentação Tasks (instrumentação é para multi-passo).
3. **`/debug` multi-hipótese**: simular sessão `/debug` com 3+ hipóteses. Esperado: cada hipótese vira Task; status visível; ledger-prosa em paralelo descreve raciocínio causal.
4. **`/debug` single-hipótese**: simular sessão `/debug` com diagnóstico de 1 hipótese. Esperado: skip silente.
5. **Monitor streaming em projeto com suite real**: invocar `/run-plan` em projeto com `test_command` configurado e suite ≥5s (e.g., projeto Python com pytest). Esperado: stdout streamado linha-a-linha em vez de espera silenciosa.
6. **Paralelismo cleanup detection**: forçar 3 worktrees mergeadas em `.worktrees/`. Esperado: detecção via 3 `gh pr list` paralelos em única mensagem; tempo total ~1s em vez de ~3s. Inspecionar tool calls via UI.
7. **Paralelismo reviewer combination**: plano com bloco `{reviewer: code,qa}`. Esperado: code-reviewer e qa-reviewer invocados em paralelo (single message com 2 Agent calls).
8. **Skill explícito em /triage step 4**: triage que decide produzir ADR. Esperado: skill chama Skill tool com `pragmatic-dev-toolkit:new-adr`, NÃO cria arquivo manualmente.

## Notas operacionais

- **Blocos 2, 4 e 5 tocam mesmo arquivo** (`skills/run-plan/SKILL.md`). Sequenciar: Bloco 2 (Tasks) → Bloco 4 (Monitor) → Bloco 5 (paralelismo) — todos editam o mesmo arquivo, mas em seções distintas; conflito de edit improvável.
- **Bloco 5 toca dois arquivos** (`skills/run-plan/SKILL.md` + `skills/triage/SKILL.md`). Tratar como bloco único — eixo de revisão (paralelismo + Skill explícito) é coerente.
- **Bloco 1 (ADR) executa via tool Skill** com nome **pragmatic-dev-toolkit:new-adr** (dogfood imediato do Finding 4 do dogfood inicial — Skill explícito em vez de "invocar"). Conteúdo do ADR escrito conforme rascunho na seção do Bloco 1.
- **Dogfood do design-reviewer (1ª invocação real, 2026-05-07)**: 4 findings substantivos aplicados — (1) ADR-worthiness do critério "≥3 passos" → ADR-010 (Bloco 1); (2) alternativa ausente em Monitor → rebate em Decisão 3; (3) acoplamento ao harness não-reconhecido → parágrafo "Acoplamento ao harness reconhecido" em `## Contexto`; (4) cerimônia em gate sub-steps → refinado para "TaskCreate apenas para sub-passos que vão executar". Findings 2-4 editoriais; Finding 1 estrutural (criou novo bloco).
