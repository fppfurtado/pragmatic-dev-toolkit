> **ARCHIVED 2026-05-31** — content absorbed into [ADR-048](../ADR-048-free-read-design-reviewer-consolidado.md); see that ADR for current authority. Body below preserved verbatim for historical record.

# ADR-044: Scan medium + always-include foundationals no free-read do design-reviewer

**Data:** 2026-05-29
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-021](ADR-021-curadoria-free-read-design-reviewer.md) (curadoria do free-read do design-reviewer — anotação + scan por keyword com threshold N=15). Este ADR é **sucessor parcial** que refina mecânica do scan (medium em vez de cabeçalho ~60 linhas) e adiciona categoria nova "always-include curado" (3 ADRs sempre lidos integralmente paralelo a `philosophy.md`). Threshold N=15, anotação `**ADRs candidatos:**` e `philosophy.md` sempre integral **preservados**.
- **Investigação:** Onda 4 (última) da reforma doutrinária codificada em `BACKLOG.md ## Próximos` (commit `6473a55`; Ondas 1+2+3 shippadas — ADR-043 em `076354f` + PR #85 + PR #86). Plano em `docs/plans/onda-4-free-read-refinement.md` (commit `6d954fe`). Com 43 ADRs em `docs/decisions/` hoje, o scan atual de ADR-021 (~60 linhas/ADR não-anotado até final de § Decisão) consome ~15k tokens só de scan por invocação do reviewer. Custo escala O(#ADRs).

**Recursive moment intencional:** /new-adr disparando design-reviewer auto-fire per [ADR-011](ADR-011-wiring-design-reviewer-automatico.md) sobre este ADR draft aplica mecanismo ATUAL de ADR-021 — não o refinado. Token cost desta invocação serve como **baseline pré-refinamento** para validação empírica pós-merge.

## Contexto

ADR-021 estabeleceu mecanismo híbrido: operador anota `**ADRs candidatos:**` no `## Contexto` do plano (opcional); design-reviewer faz scan por keyword no "cabeçalho" (~60 linhas até final de § Decisão) dos ADRs não-anotados; `philosophy.md` sempre integral; threshold N=15 desliga o mecanismo abaixo do volume.

Custo atual estimado por invocação no plugin meta-toolkit (43 ADRs):
- Scan target: ~60 linhas × 40 ADRs não-anotados = ~2400 linhas ≈ ~15k tokens só de scan.
- Anotados + philosophy.md: ~5-10k tokens adicionais.
- Total free-read: ~20-25k tokens por invocação do design-reviewer.

Custo cresce a cada novo ADR (~+500 tokens/ADR pelo scan). Toolkit projeta atingir 50-60 ADRs em meses — ~22k+ tokens/invocação no scan apenas. Alavanca real de redução de token cost é o ponto da Onda 4 (vs ~10% das ondas 1-3 sozinhas).

Duas dimensões de refinamento emergem naturalmente:
1. **Mecânica do scan target** — atual 60 linhas/ADR contém § Origem + § Contexto (volume alto, sinal médio); subset menor preserva sinal de keyword match (que vive em § Decisão) com fração do volume.
2. **Categoria "always-include"** — ADRs doutrinariamente apex citados em quase toda review merecem leitura integral garantida (paralelo a `philosophy.md`), sem depender de anotação manual em todo plano. Pattern emergente: ADR-034 e ADR-043 citados em TODAS as 3 ondas anteriores da reforma; ADR-009 é doutrina-base do próprio design-reviewer.

ADR-021 § Gatilhos #2 antecipou exatamente este trigger: *"Operador anota sistematicamente os mesmos ADRs em planos diferentes — sinal de que esses ADRs viraram doutrina-base; promover para inclusão automática sempre-lida (paralelo a `philosophy.md` integral)."* Reforma 1-3 ondas confirma empiricamente.

## Decisão

Refinar o mecanismo de curadoria de [ADR-021](ADR-021-curadoria-free-read-design-reviewer.md) em duas dimensões. Threshold N=15, anotação `**ADRs candidatos:**` e `philosophy.md` sempre integral **preservados**.

### 1. Scan medium (substituindo scan de cabeçalho)

Scan target reduzido de "cabeçalho até final de § Decisão" (~60 linhas/ADR) para subset mínimo doutrinariamente significativo.

**Heurística prescritiva (regra única):**

- Título (linha 1).
- Linhas com `**Status:**` e `**Data:**`.
- A partir da linha imediatamente após `## Decisão`, ler até o **primeiro** dos seguintes delimitadores:
  - Próximo header top-level (`## `).
  - 8 linhas lidas.
  - Cap absoluto **12 linhas/ADR**.
- Sub-headers `### ` dentro de `## Decisão` são **incluídos** no scan target (resolução explícita do caso "§ Decisão começa com `### Subseção` sem parágrafo intermediário", pattern presente neste próprio ADR).

Fallback paralelo ao determinístico de ADR-021 (que tinha "ler até o segundo `##` após `## Decisão`, ou primeiras 60 linhas se delimitador não bater"). Regra unidirecional (3 delimitadores em ordem) evita ambiguidade entre unidades distintas (parágrafos vs linhas).

Custo estimado: ~3-5k tokens scan total (vs ~15k atuais). Redução ~70% sobre o scan target.

Critério de match preservado de ADR-021: case-insensitive substring; **≥2 keywords matches** no scan target confirma relevância (1 keyword único = match acidental). ADRs com match entram no input integral; ADRs sem match são descartados.

### 2. Always-include curated list

3 ADRs sempre lidos integralmente, paralelo a `philosophy.md`:

- **[ADR-009](ADR-009-revisor-design-pre-fato.md)** (Revisor design pré-fato e free-read de doctrine sources) — foundational do próprio design-reviewer; doutrina-base de qualquer review.
- **[ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md)** (Critério editorial — adendo em ADR existente vs novo ADR) — critério mecânico citado em quase todo sucessor parcial recente; auditável retroativamente nas Ondas 1-3 da reforma (citado em cada uma).
- **[ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md)** (Hierarquia doutrinal — fundamentais como raiz, pragmáticos como consequência operacional) — apex doutrinal do toolkit; raiz epistêmica que governa todas as decisões sob a hierarquia invertida.

**Pattern emergente confirmado empiricamente.** Ondas 1+2+3 da reforma doutrinária citam ADR-034 e ADR-043 em TODAS — sinal forte de "doutrina-base sempre lida" per [ADR-021](ADR-021-curadoria-free-read-design-reviewer.md) § Gatilhos #2. ADR-009 entra por categoria (qualquer review do design-reviewer pressupõe a doutrina que o instituiu).

**Always-include opera APENAS no modo curado** (`#ADRs > 15`). Modo legacy (consumer pequeno) preserva free-read integral sem distinção — quando tudo é lido, não há subset a curar.

### 3. Rebatimento de candidatos não-incluídos

Para evitar drift posterior, decisão registra explicitamente os candidatos óbvios NÃO-incluídos nesta v1:

- **[ADR-011](ADR-011-wiring-design-reviewer-automatico.md)** (Wiring automático do design-reviewer): cross-cutting mas opera só em `/triage`+`/new-adr` dispatch, não em toda review. Doutrina conhecida pelo agent via convenção operacional; promoção a always-include não passa custo-clareza.
- **[ADR-026](ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md)** (Critério mecânico de absorção de findings): pós-fato, do operador-pós-reviewer; não governa o que o reviewer flagra, governa como o operador processa.
- **[ADR-007](ADR-007-idioma-artefatos-informativos.md)** (Idioma artefatos informativos): específico ao registro de mudanças (CHANGELOG, tag, PR); fora do escopo das reviews de plano/ADR.
- **[ADR-017](ADR-017-cutucada-uniforme-descoberta-config-ausente.md)** (Cutucada uniforme em skills para descoberta de configuração ausente): específico a SKILLs com `roles.required`; doutrina periférica para review de plano.
- **[ADR-038](ADR-038-mirror-decisoes-absorvidas-runtime.md)** (Mirror de Decisões absorvidas runtime): pattern paralelo de "context-aware via messenger upstream" mas governa runtime de outros reviewers (code/qa/doc/security) durante /run-plan, não a curadoria do free-read pré-fato do design-reviewer. Eixos disjuntos; sem ganho de leitura sempre.

**Critério discriminante (carga empírica vs escopo de aplicação).** ADR-011 e ADR-026 têm carga empírica comparável a ADR-034/-043 — ambos citados em sucessores parciais recentes. O critério discriminante é **escopo de aplicação**: ADR-011 governa **quando** o reviewer dispara (`/triage` + `/new-adr` dispatch), não **o que** ele aplica em runtime na review; ADR-026 governa **pós-fato pelo operador** (absorção de findings), não a leitura de doutrina pelo reviewer. Always-include lista doutrina **aplicada em runtime durante a review** — escopo de ADR-009/-034/-043.

**Critério de promoção futura:** ≥3 anotações sistemáticas em planos distintos (paralelo a ADR-021 § Gatilhos #2). **Cap nominal de 5 ADRs.** Acima disso, always-include vira overhead em vez de complemento ao scan.

### Reporte invariante

Format do reporte ao final da review (extensão de ADR-021 § Invariante de relatório):

```
Subset analisado: <N> ADRs lidos integralmente — <ADR-NNN>, <ADR-MMM>, ... (anotados: <K>, always-include: <A>, scan-matched: <L>). <M> filtrados pelo scan.
```

Modo legacy (`#ADRs ≤ 15`) → `Subset analisado: free-read integral (modo legacy; #ADRs ≤ 15)`.

## Consequências

### Benefícios

- Token cost cresce sub-linearmente acima do threshold. Mecanismo escala para 50, 100+ ADRs sem inflar invocações.
- Always-include garante doutrina apex sempre presente — operador não precisa lembrar de anotar ADR-043 em todo plano.
- Pattern reutilizável: rebatimento explícito + cap nominal documenta processo de expansão para futuro skill author.

### Trade-offs

- **Scan medium tem mais false negatives potenciais que scan atual** (menos contexto para keyword match). Mitigação parcial: keywords de § Decisão (1ª frase) ainda são doutrinariamente ricas. ADRs lexicalmente distantes do plano permanecem invisíveis ao scan (mesmo trade-off de ADR-021).
- **Always-include adiciona ~5-10k tokens sempre lidos** mesmo em reviews triviais. Compensado pela redução do scan (~12k economizados); saldo líquido ~5-7k tokens menos por invocação. ROI positivo para inventário ≥30 ADRs.
- **Lista always-include é editorial.** Cap 5 e critério de promoção mitigam, mas inclusão/remoção exige decisão operadora consciente. Risco de drift se operador adicionar ADR à lista sem rebatimento dos não-incluídos.

### Limitações

- Não cobre o caso de doutrina não-escrita (herda limitação de ADR-009/-021).
- Threshold N=15 herdado de ADR-021 § Decisão #3 sem recalibração — mesma observabilidade-zero registrada por ADR-021 § Trade-offs ("Calibração de N=15 não tem observabilidade direta"). Gatilho de recalibração ativo sob mesmo trilho.
- **Valley of meh para inventário 16-29 ADRs.** Always-include adiciona ~5-10k tokens fixos sempre lidos, mas scan medium dos 13-26 não-anotados custa só ~1.5-3k. **Saldo líquido pior que modo legacy desligado** nessa janela. Ganho real materializa-se ≥30 ADRs. Operador consumer chegando em 18 ADRs ativaria mecanismo com piora — aceito como sinal pré-codificado para gatilho de recalibração de N=15 (se recorrer).
- Mecânica do scan medium é prescritiva mas não imutável — refinamento iterativo previsto se false negatives recorrerem.

## Alternativas consideradas

### (a) Manter status quo ADR-021 (scan ~60 linhas/ADR)

Sem refinamento. Token cost continua crescendo O(#ADRs); ~15k atuais → ~22k+ em 60 ADRs.

Descartada: alavanca de token cost é a justificativa primária da reforma; Onda 4 existe para entregá-la.

### (b) Scan minimal (só título + Status, ~2 linhas/ADR)

~5k tokens scan total (redução ~85%). Mais agressivo que medium.

Descartada via cutucada do /triage upstream: título sozinho perde precisão para keyword match (vocabulário ADR vive primariamente em § Decisão). False-negatives sobem materialmente. Verdade puxa contra (perde sinal).

### (c) Always-include expandido (5 ADRs incluindo ADR-011 e ADR-026)

Subset cresce para 5; ADR-011 e ADR-026 entram.

Descartada via cutucada do /triage upstream: Ockham puxa para lista enxuta. 5 ADRs sempre lidos comem ~10-15k tokens — compensa menos o ganho do scan medium. Pattern empírico ≥3x ad hoc é mais forte para ADR-043/-034 que para ADR-011/-026. Promoção futura disponível via gatilho.

### (d) Sub-diretórios por eixo em `docs/decisions/` (re-litigada de ADR-021 § Alt b3)

Reorganizar fisicamente. Rejeitada em ADR-021 por custo de migração + ADRs órfãos cross-eixo. Argumento permanece válido; este ADR não revisita.

### (e) Lista always-include sem cap nominal

Não fixar cap (5 nesta proposta). Operador adiciona conforme entende.

Descartada: sem cap, lista cresce até virar próprio overhead. Cap concreto = critério editorial mecânico; gatilho de recalibração se atrito.

## Auto-aplicação coerente

Aplicação dos critérios per [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) § "Novo ADR quando ≥1 das condições aplica":

- **Cond 5 (sucessor parcial):** aplica primária e captura também a categoria "always-include curado". ADR-021 § Alternativas (e) anteceipou explicitamente esta categoria ("Lista always-include de ADRs doutrina-base") como *"complemento futuro, não alternativa concorrente — pode coexistir com ADR-021 se vier"* — descartada à época por exigir curadoria editorial não-trivial e aguardar sinal empírico via gatilho. ADR-044 executa o gatilho (pattern emergente ≥3x em Ondas 1-3 confirmado).

Cond 1 (decisão estrutural sem ancestral direto) NÃO aplica — ADR-021 § Alternativas (e) é o ancestral conceitual explícito; ADR-044 não introduz categoria sem ancestral. Cond 2 (substitui ADR ancestral) NÃO aplica — ADR-021 permanece `Aceito`. Cond 3 (restrição externa) NÃO aplica. Cond 4 (categoria nova de artefato) NÃO aplica — always-include é mecânica de seleção dentro do mesmo conceito de curadoria, não tipo de artefato novo.

Aplicação dos critérios per [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § "Ockham operacionalizado em decisões internas do plugin":

- **Critério 1** (*"Incidente recorrente ou padrão observado em uso real (não hipótese). Operacionaliza Verdade — empírico vence especulação."*): pattern emergente ≥3x ad hoc (ADR-034 e ADR-043 citados em todas as 3 ondas anteriores; sinal claro de doutrina-base sempre lida).
- **Critério 4** (*"Codificação de pattern emergente já aplicado ≥3 vezes ad hoc em decisões anteriores do plugin (auditável retroativamente). Operacionaliza Verdade + Ockham."*): same pattern, mesma evidência empírica.

Esses 2 critérios fundamentais autorizam o refinamento estrutural; Ockham endossa especificamente a lista enxuta (cap 5).

## Implementação

3 edits no commit unificado do Bloco 1 do plano + 1 edit em commit separado do Bloco 2:

1. **Este ADR** criado com Status: Proposto.
2. **ADR-021 ganha `## Addendum (2026-05-29)`** com cross-ref a este ADR (paralelo a ADR-005/-017 Addenda da Onda 3 da reforma + 2 Addenda históricos de ADR-001). Reconhece sucessor parcial que estende mecânica (scan medium) + adiciona categoria (always-include) sem revogar decisão central de ADR-021 (threshold, anotação, philosophy.md integral). Status `Aceito` preservado.
3. **`agents/design-reviewer.md` § Curadoria do free-read** reescrita no Bloco 2 do plano (commit separado), implementando o protocolo: scan medium concreto, always-include literal (3 ADRs), reporte invariante mantido com nova contagem "always-include: <K>".

## Gatilhos de revisão

- **Always-include list precisa crescer** — ≥3 anotações sistemáticas de algum ADR-NNN (ex.: ADR-011, ADR-026) em planos distintos pós-merge, sinalizando promoção a always-include. Trigger paralelo a ADR-021 § Gatilhos #2. Cap nominal 5 limita expansão.
- **Scan medium subdimensionado** — false negatives recorrentes em invocações reais (operador percebe ADR doutrinariamente relevante não-aparecido no "Subset analisado"). Ampliar para ~15 linhas/ADR (incluindo § Consequências 1ª frase?) ou recalibrar heurística.
- **Threshold N=15 recalibração** — sinal empírico de scan ativando cedo demais ou tarde demais. Mesma régua do gatilho de ADR-021 sobre N=15.
- **Token cost real não cair conforme estimado** (~50-70%) — observação pós-merge via invocações do design-reviewer em ondas/planos subsequentes. Recalibrar scan target ou expandir always-include conforme dado empírico.
- **Cap nominal 5 mal-calibrado** — operador precisa expandir always-include para 6-7 e o cap estorva. Recalibrar.
- **Reviewer reporta inconsistência entre subset lido e ADR não-lido** (auto-validação rara) — confirma necessidade de safety net (talvez always-include cresce automaticamente quando ADR cruza limiar de citação).

## Onda 4 (última) da reforma doutrinária

Per umbrella line em `BACKLOG.md ## Próximos` (commit `4882629`/`6473a55`). Pós-merge desta onda, umbrella line é movida para `## Concluídos` (reforma completa). Avaliação retrospectiva do ganho real de token cost (~50-70% estimado) fica como spec pós-merge — observação via invocações subsequentes do design-reviewer; gatilho de recalibração registrado acima.
