# Plano — Onda 4 da reforma doutrinária: refinamento do free-read do design-reviewer

## Contexto

Onda 4 da reforma doutrinária codificada em `BACKLOG.md ## Próximos` (commit `6473a55`; Ondas 1+2+3 shippadas — ADR-043 em `076354f` + PR #85 + PR #86). Refinamento do mecanismo de curadoria do free-read do `design-reviewer` ([ADR-021](../decisions/ADR-021-curadoria-free-read-design-reviewer.md)) para reduzir token cost — **alavanca real (~50-70% redução estimada)** vs ~10% das ondas anteriores.

Mecanismo atual (ADR-021): scan do "cabeçalho" (~60 linhas até final de `## Decisão`) de cada ADR não-anotado; threshold N=15 (ativo hoje com 43 ADRs); `philosophy.md` sempre integral; `**ADRs candidatos:**` mensageiro do operador. Custo atual estimado: ~15k tokens só de scan por invocação do reviewer.

Refinamento (decisões via cutucada do /triage upstream):

1. **(a2) Scan medium**: scan target reduzido para **título + Status + Data + 1ª frase de § Decisão** (~5-10 linhas/ADR vs ~60 atuais). ~3-5k tokens scan total. Redução ~70% sobre o scan. Preserva sinal de keyword match (§ Decisão carrega vocabulário doutrinário; título sozinho é insuficiente).
2. **(b1) Subset always-include curado**: **ADR-009** (design-reviewer foundational), **ADR-034** (critério adendo vs ADR), **ADR-043** (hierarquia doutrinal apex) sempre lidos integralmente, paralelo a `philosophy.md`. Pattern emergente confirmado empiricamente: ADR-043 e ADR-034 citados em TODAS as 3 ondas anteriores da reforma; ADR-009 é doutrina-base de qualquer review. Custo: ~5-10k tokens adicionais sempre lidos. Compensado pela redução do scan.

   **Candidatos óbvios não-incluídos nesta v1** (rebatimento explícito): ADR-011 (wiring automático do design-reviewer — cross-cutting mas opera só em `/triage`+`/new-adr` dispatch, não em toda review), ADR-026 (critério de absorção de findings — pós-fato, do operador-pós-reviewer), ADR-007 (idioma artefatos informativos — específico ao registro de mudanças), ADR-017 (cutucada de descoberta — específico a SKILLs com `roles.required`). Critério de promoção futura: ≥3 anotações sistemáticas em planos distintos (paralelo a ADR-021 § Gatilhos #2). **Cap nominal de 5 ADRs** — acima disso always-include vira overhead em vez de complemento ao scan.

Threshold N=15 mantido (mecanismo já ativo com 43 ADRs; refinamento opera acima do threshold; não recalibro). **Always-include opera apenas no modo curado** (`#ADRs > 15`); modo legacy (`#ADRs ≤ 15`, consumer pequeno) preserva free-read integral sem distinção — quando tudo é lido, não há subset a curar. Assimetria intencional.

Plano produz 2 blocos: Bloco 1 ADR sucessor parcial de ADR-021 via `/new-adr` (caminho-only delegado per ADR-011); Bloco 2 edit em `agents/design-reviewer.md` § "Curadoria do free-read" implementando o protocolo refinado.

**ADRs candidatos:** ADR-021 (sucessor parcial direto, alvo da extensão), ADR-009 (design-reviewer foundational + agora always-include), ADR-034 (critério adendo + agora always-include), ADR-043 (hierarquia apex + agora always-include), ADR-011 (wiring automático), ADR-038 (Decisões absorvidas via messenger upstream — pattern paralelo de "context-aware via curadoria").

Campo `**Linha do backlog:**` intencionalmente omitido deste plano — umbrella line cobre 4 ondas (esta é a última); matching prematuro pelo `/run-plan §3.4` moveria a umbrella prematuramente. Operador moverá manualmente após Onda 4 fechada. Paralelo às ondas 2-3. Detalhamento em § Notas operacionais.

## Resumo da mudança

- **Bloco 1**: ADR sucessor parcial de ADR-021 (provavelmente ADR-044) codificando:
  - **Scan medium**: substituir "cabeçalho até final de § Decisão" (~60 linhas) por "título + Status + Data + 1ª frase de § Decisão" (~5-10 linhas).
  - **Always-include curated list**: ADR-009, ADR-034, ADR-043 sempre lidos integralmente. Paralelo a `philosophy.md`.
  - Threshold N=15 mantido.
  - Mecânica de extração do novo scan target — **heurística prescritiva concreta** (paralelo ao fallback determinístico de ADR-021): título (linha 1) + linhas com `**Status:**` e `**Data:**` + tudo entre `## Decisão` e o próximo `\n\n` (parágrafo único), OU primeiras 8 linhas após `## Decisão`, o que vier antes. **Cap absoluto: 12 linhas/ADR.** Evita ambiguidade em ADRs cuja § Decisão abre com lista/blockquote/parágrafo bold multilinha.
  - Reporte "Subset analisado" preserva format ADR-021 mas inclui contagem de always-include.
  - Gatilhos de revisão: always-include list cresce orgânica (paralelo a ADR-021 § Gatilhos #2); scan medium subdimensionado (false negatives recorrentes → ampliar para ~15 linhas/ADR); threshold recalibração.

- **Bloco 2**: edit em `agents/design-reviewer.md` § "Curadoria do free-read":
  - Reescrever a seção para refletir mecanismo refinado.
  - Always-include list literal (3 ADRs) + cross-ref ao novo ADR.
  - Scan target redefinido (regex/instrução concreta para extrair título + Status + Data + § Decisão 1ª frase).
  - Reporte invariante preserva formato; "always-include: <K>" passa a aparecer.
  - Cross-ref a ADR-021 como predecessor + novo ADR como mecanismo vigente.

Decisões centrais de ADR-021 preservadas (threshold, anotação `**ADRs candidatos:**`, `philosophy.md` sempre integral); só mecânica do scan refinada + categoria nova "always-include" adicionada.

## Arquivos a alterar

### Bloco 1 — ADR sucessor parcial de ADR-021 (via /new-adr) {reviewer: design}

- `docs/decisions/ADR-NNN-*.md`: criar via `/new-adr` com título sugerido "Scan medium + always-include foundationals no free-read do design-reviewer". Sucessor parcial de ADR-021 per [ADR-034](../decisions/ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) cond 5 (estende mecanismo) + cond 1 (categoria nova "always-include" sem ancestral direto). § Decisão concretiza scan medium (regex/sed prescritivo + cap 12 linhas) + always-include list (ADR-009/-034/-043 + justificativa empírica + rebatimento de candidatos óbvios + cap 5 + gatilho de expansão). Status: Proposto. `/new-adr` dispara `@design-reviewer` automaticamente per ADR-011 — reviewer aplica mecanismo ATUAL de ADR-021 (recursive moment intencional).
- `docs/decisions/ADR-021-curadoria-free-read-design-reviewer.md`: append `## Addendum (2026-05-29)` com cross-ref ao novo ADR (paralelo a ADR-005/-017 Addenda da Onda 3 + 2 Addenda em ADR-001). Reconhece sucessor parcial que refina mecânica (scan medium) + adiciona categoria (always-include) sem revogar decisão central. Mesmo commit unificado do Bloco 1 (paralelo a Onda 1 que tocou ADR-035 Status edit no commit `076354f` do ADR-043).

### Bloco 2 — edit agents/design-reviewer.md § Curadoria do free-read {reviewer: doc}

- `agents/design-reviewer.md`: reescrever § "Curadoria do free-read" para refletir mecanismo refinado. Estrutura:
  - § "Threshold de ativação" preservada (N=15).
  - § "Modo curado" reescrita: subseção 1 "Anotação prioritária" intacta; subseção 2 "Scan por keyword" altera target (medium em vez de cabeçalho ~60 linhas); subseção 3 "Always-include curado" nova (ADR-009/-034/-043 + `philosophy.md`).
  - § "Invariante de relatório" preservada; format inclui "always-include: <K>".
  - Cross-refs a novo ADR como mecanismo vigente + ADR-021 como predecessor.

## Verificação end-to-end

- Novo ADR (provavelmente ADR-044) criado em `docs/decisions/`, Status: Proposto, com § Origem citando ADR-021 como Decisão base + ADR-034 cond 5 (sucessor parcial).
- `agents/design-reviewer.md` § "Curadoria do free-read" reescrita: scan medium documentado (título + Status + Data + § Decisão 1ª frase), always-include list literal (ADR-009/-034/-043), threshold N=15 mantido, `philosophy.md` sempre integral preservado.
- Cross-ref bidirecional: novo ADR cita ADR-021 § Decisão como predecessor; design-reviewer agent cita novo ADR como mecanismo vigente.
- Body de ADR-021 preservado + Status `Aceito` intacto (sucessor parcial estende, não revoga; per ADR-034 cond 5).
- Verificação editorial via inspeção visual: `git diff origin/main..HEAD -- agents/design-reviewer.md docs/decisions/ADR-NNN-*.md` mostra ADR novo + edits cirúrgicos no agent dentro do escopo declarado.

## Verificação manual

Surface não-determinística (comportamento de LLM agent — design-reviewer). Cenários enumerados:

1. **Invocação do design-reviewer com `**ADRs candidatos:**` declarados** (ex.: próximo plano de feature com 2-3 ADRs anotados): reviewer reporta `Subset analisado: <N> ADRs lidos integralmente — <lista> (anotados: <K>, always-include: 3, scan-matched: <L>). <M> filtrados pelo scan.` Confirmar:
   - ADRs anotados pelo operador foram lidos.
   - ADR-009/-034/-043 aparecem em "always-include: 3".
   - Scan-matched cobre demais relevantes.
   - Filtrados é a contagem dos ADRs não-relevantes (43 - K - 3 - L).

2. **Invocação sem `**ADRs candidatos:**`** (plano sem o campo): reviewer ainda lê ADR-009/-034/-043 integralmente (always-include). Scan medium dos demais. Confirmar reporte cita "always-include: 3" + "anotados: 0".

3. **Reviewer detecta contradição com ADR fora do scan e fora de always-include** (false negative): documentar como findings perdidos. Operador anota retroativamente em outro plano ou propõe promoção a always-include via gatilho do novo ADR.

4. **Modo legacy (#ADRs ≤ 15)**: cenário sem-op (threshold preserva free-read integral, sem always-include explícito porque tudo é always). Não há projeto consumer com <15 ADRs para testar empiricamente; cenário documentado mas não exercitado nesta onda.

5. **Reviewer durante /run-plan deste próprio plano (Bloco 1 → /new-adr → reviewer auto-fire)**: reviewer aplica mecanismo ATUAL de ADR-021 (não o refinado), porque PR ainda não mergeado. Recursive moment intencional. Reviewer deve reportar `Subset analisado: ~N ADRs lidos integralmente — <lista incluindo ADRs candidatos anotados>, scan-matched: <L>. <M> filtrados pelo scan.` — token cost desta invocação serve como **baseline pré-refinamento** para comparação empírica após merge (gatilho de revisão registrado no novo ADR sobre eficácia real do refinamento).

## Notas operacionais

- **Umbrella line da reforma**: linha em `BACKLOG.md ## Próximos` (commit `6473a55`) cobre 4 ondas; esta é a última. `**Linha do backlog:**` omitido para evitar matching prematuro do `/run-plan §3.4` — operador moverá umbrella para `## Concluídos` manualmente após Onda 4 fechada (paralelo às ondas 2 e 3). Após fechamento da Onda 4, umbrella inteira pode ser movida para Concluídos (reforma completa) ou refeita em formato sumarizado.

- **Sucessor parcial de ADR-021**: ADR-021 permanece `Aceito` (não é Substituído). Novo ADR estende mecanismo (scan medium + always-include) sem revogar (threshold N=15 mantido, anotação `**ADRs candidatos:**` mantida, `philosophy.md` sempre integral mantido). Per [ADR-034](../decisions/ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) § "Novo ADR quando ≥1 das condições aplica": cond 5 (sucessor parcial) aplica primária; cond 1 também (categoria "always-include curado" sem ancestral direto). Cross-ref bidirecional: novo ADR cita ADR-021 § Decisão como predecessor; **ADR-021 ganha `## Addendum (2026-05-29)`** cross-ref ao novo ADR (paralelo ao pattern recém-aplicado em ADR-005/-017 na Onda 3 e a ADR-001 Addenda históricos).

- **Always-include list mantida no agents/design-reviewer.md** (hardcoded literal, com cross-ref ao novo ADR que estabeleceu). Razões: agent é o consumidor (lê e aplica); ADR define mecanismo + lista canônica + justificativa empírica. Expansão futura via gatilho de revisão do novo ADR (paralelo ao gatilho #2 de ADR-021 — "operador anota sistematicamente os mesmos ADRs → sinal para promover").

- **Recursive moment intencional**: o /run-plan deste plano vai invocar /new-adr (Bloco 1), que dispara design-reviewer auto-fire per ADR-011. Reviewer aplica mecanismo ATUAL (ADR-021 inalterado) porque o refinamento não foi mergeado ainda. Após PR mergeado, próximas invocações do reviewer operam sob o mecanismo refinado.

- **Bloco 2 reviewer = doc** (não code) porque edit é em `agents/design-reviewer.md` (doc do agent — frontmatter + prosa). Pattern paralelo aos blocos doc de ondas 2-3.

- **Onda 4 fecha a reforma**: pós-merge desta onda, umbrella line é movida para Concluídos. Próximo /triage descobre clean state (reforma completa). Avaliação retrospectiva (token cost real reduzido? sinal empírico do ganho?) fica como spec pós-merge — observação via tokens em invocações subsequentes do design-reviewer; gatilho de recalibração registrado no novo ADR.

## Decisões absorvidas

- § Resumo + § Arquivos a alterar Bloco 1: mecânica do scan medium ganhou heurística prescritiva concreta (título + Status + Data + § Decisão até `\n\n` OU 8 linhas após `## Decisão`; cap absoluto 12 linhas/ADR) — paralelo ao fallback determinístico de ADR-021; evita ambiguidade em ADRs cuja § Decisão abre com lista/blockquote/parágrafo bold multilinha (caminho-único).
- § Verificação manual cenário 5: adicionado bullet sobre output esperado do reviewer recursive como **baseline pré-refinamento** para comparação empírica pós-merge — token cost da invocação serve como dado empírico do ganho do refinamento (caminho-único).
- § Contexto: clarificação "Always-include opera apenas no modo curado (#ADRs > 15)" — assimetria intencional explícita; modo legacy preserva free-read integral sem subset curado porque tudo é lido (caminho-único).
