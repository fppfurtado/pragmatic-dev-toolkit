> **ARCHIVED 2026-05-31** — content absorbed into [ADR-049](../ADR-049-execucao-run-plan-consolidado.md); see that ADR for current authority. Body below preserved verbatim for historical record.

# ADR-039: Task tool como state-keeping em fluxo longo

**Data:** 2026-05-26
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-010](ADR-010-instrumentacao-progresso-skills-multi-passo.md) — sucessor parcial. Estende uso do Task tool de "progress display" (cursor de qual passo está rodando) para também "state-keeping em fluxo longo" (buffer de pendências a materializar entre passos não-contíguos). Decisão central de ADR-010 (instrumentação multi-passo com lifecycle triplo) **preservada**; categoria nova adicionada paralela.
- **Investigação:** Sessão de 2026-05-26 (ROADMAP item 8 / commit `25d0daf`). Onda 2 identificou fragilidade latente em `/run-plan §3.5 captura automática`: spec atual diz "agente acumula gatilhos e materializa no gate final" sem mecanismo de tracking — depende de lista mental. Em `/run-plan` longo (≥3 blocos com triggers reais), risco de esquecer parte da lista entre passo 2 e §3.5.
- **Classificação editorial:** Pelo [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) § "Novo ADR quando ≥1 das condições aplica": condição (4) "introduz categoria nova" aplica (state-keeping ≠ progress display — eixos conceituais distintos: queue persistente vs cursor de execução); condição (5) "sucessor parcial — estende ADR Aceito sem revogar" aplica. Lifecycle 2-estados (`pending → completed` skipping `in_progress`) diverge de ADR-010 § Mecânica triplo — prescrição mecânica nova, não anotação descritiva, falha critério (4) "caráter explicativo" de adendo. Default editorial por novo ADR sucessor parcial — paralelo a [ADR-038](ADR-038-mirror-decisoes-absorvidas-runtime.md) (mesma onda, mesmo critério).
- **Precedente recente:** [ADR-038](ADR-038-mirror-decisoes-absorvidas-runtime.md) — sucessor parcial de ADR-026 + refina ADR-035; mesma onda 2026-05-26; mesma aplicação de ADR-034 condição (5).

## Contexto

[ADR-010](ADR-010-instrumentacao-progresso-skills-multi-passo.md) estabeleceu instrumentação de progresso multi-passo via Task tool. § Decisão central: *"Skills com ≥3 passos sequenciais discretos instrumentam progresso via TaskCreate + TaskUpdate"*. § Mecânica prescreve lifecycle triplo `pending → in_progress → completed`. § Escopo lista skills cobertas (progress display em fluxos multi-passo conhecidos).

**Gap observado em uso real (latente, não-incidente):** `/run-plan §3.5 captura automática` acumula gatilhos emergentes ao longo do fluxo (fase pré-loop com warnings ADR-002; passo 2 do loop com falha contornada / finding fora-do-escopo / hook bloqueando; passo 3.2 validação manual com divergência do plano / bug colateral) e materializa todos no gate final (§3.5). Spec atual: *"agente acumula gatilhos e materializa no gate final"* — **lista mental, sem mecanismo de tracking**.

Risco: em fluxo longo (≥3 blocos × múltiplos triggers possíveis), agente pode esquecer parte da lista entre o passo onde o trigger emergiu e §3.5 materialização. Mesma classe de fragilidade silent regression que ROADMAP itens 6 (reviewer-vs-reviewer) e 7 (stale-view) endereçaram nesta mesma onda — agente mantém state mentalmente em fluxo multi-passo sem persistência verificável.

Causa raiz arquitetural: Task tool já existe e é usado para progresso (ADR-010), mas seu **lifecycle e semântica como cursor de execução** ("qual passo está rodando agora") não cobre o caso de **buffer de pendências** ("que captures emergiram que ainda preciso materializar"). Estender o uso do Task tool resolve sem introduzir mecanismo novo, mas exige codificar a categoria distinta — caso contrário, leitor futuro lê ADR-010 e infere que progress instrumentation é o ÚNICO uso.

## Decisão

Task tool serve, além de **progress display** (ADR-010), também como **state-keeping em fluxo longo** — buffer de pendências emergentes a materializar em ponto posterior do mesmo fluxo. Categoria nova paralela, não substitui a anterior.

Cláusulas operacionais:

1. **Categoria distinta reconhecida.** Skills podem usar Task tool em 2 modos:
   - **Progress display (ADR-010):** cursor de execução; lifecycle triplo `pending → in_progress → completed`; refletido continuamente ao operador.
   - **State-keeping (ADR-039):** buffer de pendências a materializar; lifecycle 2-estados `pending → completed`; agente materializa em batch em ponto posterior.

   Os 2 modos coexistem sem fricção — mesmo SKILL pode usar ambos (progress Tasks para os passos do loop + state-keeping Tasks para captures emergentes).

2. **Marker convention.** State-keeping Tasks têm prefixo marker no subject identificando tipo e destino. Convention para captures de `/run-plan` §3.5:
   - `[capture:validacao] <linha>` — destino `## Pendências de validação` no plano corrente.
   - `[capture:backlog] <linha>` — destino `## Próximos` do papel `backlog`.

   Outras skills que adotem state-keeping no futuro escolhem marker próprio com formato livre (recomendado: `[<contexto>]` curto e greppável). Schema 2-níveis `[<categoria>:<subtipo>]` emerge se ≥2 skills exercitarem dimensões distintas (ver Gatilhos de revisão). Marker permite filtragem via `TaskList` para localizar pendências do tipo.

3. **Lifecycle 2-estados.** State-keeping Tasks usam `pending → completed` skipping `in_progress`. Razão semântica: state-keeping não tem cursor de execução — não há "executando agora" entre criação no trigger e materialização batch. `in_progress` seria estado não-semântico (Task fica pending criada quando o trigger emerge, é processada em batch em ponto posterior, vira completed após escrita). Diverge intencionalmente do triplo de ADR-010 § Mecânica — coexiste como pattern paralelo. (API do harness aceita transição direta `pending → completed` via `TaskUpdate(status="completed")` sem intermediário — verificada empiricamente durante implementação per [ROADMAP item 8 plano](../plans/captura-3-5-via-taskcreate.md) `## Pendências de validação`.)

4. **Primeiro caso de uso canonical: `/run-plan` §3.5 captura automática.** Cobertura unificada das 3 superfícies emissoras (pré-loop warnings ADR-002 + passo 2 loop + passo 3.2 validação manual). Materialização lê `TaskList` filtrada por marker `[capture:*]`, escreve cada Task pending no destino correto (validação no plano / backlog no role), marca como completed. TaskList vazia (nenhum capture emergiu) → skip silente.

Decisão é **plugin-internal**. Não prescreve comportamento de consumer projects que usem Task tool em outros patterns; documenta os 2 modos do plugin para skills/agents/hooks shipados.

## Consequências

### Benefícios

- **Elimina lista mental do agente** como state-keeping mechanism em fluxo longo. Captures persistem como Task pending até materialização — visível na `TaskList` da sessão, auditável pelo operador.
- **Mesmo Task tool, 2 usos coordenados.** Sem ferramenta nova; reusa mecanismo existente. Skills que combinam progresso + captures usam Task tool de 2 modos simultâneos sem ambiguidade (marker distingue).
- **Marker convention extensível.** Outras skills adotando state-keeping definem seus próprios markers seguindo padrão `[<categoria>:<subtipo>]`. Convention única para grep/filtragem.
- **Lifecycle 2-estados semanticamente nítido.** Não força `in_progress` artificial quando não há execução cursor — buffer simplesmente espera materialização.

### Trade-offs

- **2 modos do Task tool exigem doutrina explícita.** Skill author novo precisa entender ambos (progress display vs state-keeping). Mitigação: este ADR (e ADR-010) servem como referência cruzada; SKILL.md de cada consumidor explicita qual modo está usando.
- **Lifecycle 2-estados diverge de ADR-010 § Mecânica triplo.** Skill ou agent que mistura ambos modos sem distinção pode confundir leitor. Mitigação: marker no subject distingue (progress Tasks tipicamente sem marker; state-keeping Tasks com `[<categoria>:<subtipo>]`).
- **TaskList pode crescer em sessão longa com muitas captures.** Materialização batch em §3.5 marca como completed, mas Tasks completed permanecem visíveis (conversation-scoped per ADR-010). Mitigação: completed Tasks são informativas (operador vê o histórico de captures materializadas); não há acúmulo de pending Tasks.

### Limitações

- **State-keeping é conversation-scoped per ADR-010.** Tasks somem ao fim da sessão. Para state-keeping cross-session, mecanismo diferente (artefato persistido, ex.: `.claude/local/`) é necessário — não coberto por este ADR.
- **Marker convention requer disciplina do skill author.** Sem marker, Task vira indistinguível de progress display. Mitigação: convention documentada aqui e em SKILL.md consumidor; design-reviewer pode flagar Tasks sem marker em state-keeping context.

## Alternativas consideradas

### (a) Status quo — manter lista mental (sem mecanismo)

Descartado. Fragilidade latente identificada em ROADMAP item 8 — agent forgetting é silent regression em fluxo longo. Mesma classe de problemas que itens 6+7 endereçaram nesta onda.

### (b) Adendo a ADR-010 (sem novo ADR)

Descartado em F1 cutucada (operador escolheu novo ADR). Razões: categoria nova (state-keeping ≠ progress display), lifecycle divergente do triplo de ADR-010 § Mecânica, ADR-034 condição (5) aplica, precedente ADR-038 estabeleceu pattern paralelo (mesma onda, mesma situação editorial).

### (c) Arquivo intermediário persistido (ex.: `.run-plan-captures.json` na worktree)

Descartado por YAGNI. Conversation-scoped via Task tool já cobre o caso — captures são para materialização no mesmo `/run-plan` invocation, não cross-session. Arquivo persistido adicionaria cleanup overhead (apagar pós-materialização) e contradiz princípio "state vive em git/forge" de ADR-004 (captures não merecem ser tracked).

### (d) Novo store dedicado para captures (categoria nova de role)

Descartado. Captures são effemerais (vivem entre trigger e materialização no mesmo `/run-plan`). Promover a role com canonical path seria over-engineering para state que dura < 1 sessão. Task tool conversation-scoped é o nível certo de persistência.

## Gatilhos de revisão

- **Outras skills adotam state-keeping pattern:** se ≥2 skills além de `/run-plan` adotarem o pattern, considerar (a) refinar ADR-039 com generalização da marker convention (talvez schema mais formal `[<skill>:<categoria>:<subtipo>]`); (b) adicionar bullet em `CLAUDE.md` § Editing conventions cross-ref a ADR-010 + ADR-039 (paralelo aos bullets das demais meta-doutrinas — ADR-010, ADR-011, ADR-023, ADR-026, ADR-034 — todos indexados lá).
- **Cross-session state-keeping demandado:** se uso real revelar necessidade de captures que sobrevivem fim de sessão (operador interrompe `/run-plan` e retoma depois), reabrir para considerar persistência além de conversation-scoped — mecanismo diferente (ADR-005 local-gitignored ou similar).
- **Lifecycle 3-estados ressurge como necessidade:** se state-keeping precisar de fase intermediária visível ao operador ("processando capture X agora"), reabrir lifecycle 2-estados — talvez reconciliar com triplo de ADR-010 num modelo único.
- **Marker convention conflita com progress Tasks sem marker:** se skill autoria gerar progress Tasks com subjects que acidentalmente batam com filter `[capture:*]`, reabrir convention (talvez tornar marker obrigatório também para progress Tasks).
