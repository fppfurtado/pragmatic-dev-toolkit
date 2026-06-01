# ADR-043: Hierarquia doutrinal — fundamentais como raiz, pragmáticos como consequência operacional

**Data:** 2026-05-29
**Status:** Aceito (2026-06-01)

## Origem

- **Decisão base:** [ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) (substituído por este ADR; conteúdo essencial absorvido em § "Ockham operacionalizado em decisões internas do plugin").
- **Investigação:** PR #84 (commit `d6369ac`, mergeado 2026-05-29) shippou `docs/philosophy.md` § "Princípios fundamentais" introduzindo Verdade, Excelência sem over-engineering, e Navalha de Ockham como princípios epistêmicos do toolkit. Sessão CC 2026-05-29 (esta) identificou que "YAGNI por padrão" + "flat sobre cerimônia" + "sem defensividade ornamental" eram apex doutrinal implícito da fase anterior do plugin — não axiomas paralelos, mas consequências operacionais que precisam ser fundamentadas nos 3 princípios recém-introduzidos. Inversão estrutural impacta ADR-035, cuja existência standalone (codificar exceção interna ao YAGNI) perde substrato sob a nova raiz.

## Contexto

`docs/philosophy.md` agora abre com § "Princípios fundamentais" (3 raízes epistêmicas: Verdade, Excelência, Ockham) seguida de § "A filosofia em uma frase" (regra pragmática operacional: YAGNI/flat/sem-defensividade-ornamental). A relação entre as duas seções é articulada em prosa via "Triangulação" e "Mapping para a doutrina pragmática abaixo" (philosophy.md linha 25), mas não é codificada como decisão estrutural com efeito sobre o resto da doutrina.

A doutrina pragmática (YAGNI etc.) foi codificada antes dos fundamentais — historicamente operou como apex implícito durante a fase formativa do plugin. ADR-035 ("Escopo de aplicação de YAGNI ao próprio plugin") foi articulado precisamente para resolver a tensão emergente quando esse apex se tornou problemático: como um plugin que prega YAGNI articula sua própria doutrina sem ser auto-vetado? A resposta foi codificar uma "exceção interna" — YAGNI para consumers, 4 critérios positivos para decisões internas do plugin (incidente, fronteira, contradição, ≥3 pattern).

Com os 3 fundamentais agora explicitados como raiz, a tensão original dissolve. Ockham (não multiplicar entidades além do necessário) é universal — aplica-se integralmente tanto a código de domínio do consumer quanto a doutrina interna do plugin; varia apenas a entidade ponderada (linha-de-código, módulo, abstração de código no caso consumer; ADR, role, mecanismo, regra editorial no caso plugin). "YAGNI por padrão" é a operacionalização concreta de Ockham aplicada ao espaço-entidade consumer; os 4 critérios de ADR-035 são a operacionalização concreta de Ockham aplicada ao espaço-entidade plugin. Não há mais "exceção" — há "aplicação contextual do mesmo princípio".

Sem doutrina explícita codificando a inversão, próximas decisões doutrinais podem novamente operar sob apex-pragmático implícito (especialmente em sessões longas onde o agente não revisita os fundamentais), reproduzindo aplicação reflexa de YAGNI a decisões doutrinais — o anti-padrão que ADR-035 tentou resolver pela rota errada (exceção em vez de hierarquia).

## Decisão

**Os 3 princípios fundamentais (Verdade, Excelência sem over-engineering, Navalha de Ockham) são raiz epistêmica do toolkit. "YAGNI por padrão", "flat sobre cerimônia", "sem defensividade ornamental" são consequências operacionais derivadas — não princípios paralelos.**

Mapping (codificado em philosophy.md linha 25; este ADR o promove a decisão estrutural):

| Regra pragmática | Princípio fundamental | Como deriva |
| --- | --- | --- |
| YAGNI por padrão / flat sobre cerimônia | **Ockham** | Parsimônia dimensional aplicada ao espaço-entidade |
| Sem defensividade ornamental | **Verdade** | Validar onde há risco real observado, não onde imaginamos |
| Pragmática sem aspiracional schema-perfeição | **Excelência** | Qualidade dentro do escopo, sem virar perfeccionismo |

Razões:

- **Coerência interna.** Regras pragmáticas explicitamente derivadas dos fundamentais eliminam ambiguidade sobre o que é princípio e o que é consequência. Reviewers e o próprio agente operam com hierarquia clara: aplicar YAGNI/flat/sem-defensividade é aplicar os fundamentais via operacionalização específica; conflito aparente entre regra pragmática e princípio fundamental resolve-se em favor do fundamental.
- **Universalidade do princípio.** Ockham aplica-se integralmente a ambos os contextos (consumer e plugin), variando apenas a entidade ponderada. "YAGNI" deixa de precisar exceção interna — passa a ser instância contextual de Ockham, paralela à instância "4 critérios para decisões internas do plugin". Isso dissolve a tensão que ADR-035 codificou como exceção e absorve seu conteúdo essencial como instanciação contextual (ver § Ockham operacionalizado em decisões internas do plugin abaixo).
- **Auditabilidade pelo design-reviewer.** Princípios fundamentais como raiz dão ao reviewer benchmark estável para auditar drift. Reframings retroativos das ondas 2-4 (ADRs reframed/consolidated) terão referência fixa.

## Ockham operacionalizado em decisões internas do plugin

Esta seção absorve o conteúdo essencial de ADR-035 § "Filtro para decisões internas do plugin", reframado sob a hierarquia invertida.

**Pergunta-filtro umbrella (Ockham aplicado a doutrina/mecanismo):**

> Isso paga seu custo de manutenção pela clareza/coerência que adiciona?

Aplica-se a decisões sobre adicionar ADR, role, mecanismo de skill, formalização doutrinal em `CLAUDE.md`/`philosophy.md`, agent novo. O filtro **não é** o YAGNI consumer ("precisamos disso agora?") — é Ockham aplicado ao espaço-entidade de doutrina/mecanismo.

**Critérios legítimos para Ockham endossar adicionar entidade doutrinal** (≥1 basta):

1. **Incidente recorrente ou padrão observado** em uso real (não hipótese). Operacionaliza **Verdade** — empírico vence especulação.
2. **Fronteira doutrinal borrada** — categoria nova com fronteira nítida supera churn de refactor. Operacionaliza **Ockham** — modelar essa fronteira distingue conceitos que se confundiriam sem ela.
3. **Contradição/refinamento de doutrina** existente em ADR/`philosophy.md`/`CLAUDE.md`. Operacionaliza **Verdade** — corrigir drift entre doutrina vigente e descoberta posterior.
4. **Codificação de pattern emergente** já aplicado ≥3 vezes ad hoc em decisões anteriores do plugin (auditável retroativamente). Operacionaliza **Verdade + Ockham** — pattern empiricamente recorrente ganhou seu custo de abstração.

**Universalidade.** Os mesmos 4 critérios aplicam-se conceitualmente a decisões sobre entidades em código consumer (linha-de-código, módulo, abstração), só que o vocabulário operacional é "YAGNI por padrão" + heurísticas de gaps de `/triage` + rubrica de `code-reviewer`. A unidade subjacente é Ockham; as instanciações específicas (4 critérios doutrinais; YAGNI consumer) diferem pela entidade ponderada e pelo vocabulário herdado.

**Polaridade.** A operacionalização consumer é **default-restritiva** (YAGNI ortodoxo: não construir até dor real); a operacionalização plugin é **default-condicional** (≥1 dos 4 critérios basta para Ockham endossar). A diferença de polaridade é **consequência** da entidade ponderada — código consumer multiplica peso morto barato-de-acumular em execução/manutenção; doutrina plugin multiplica ambiguidade/incoerência só auditável retroativamente, mais cara de detectar. Polaridades opostas instanciam o mesmo Ockham; não são inconsistência entre instanciações.

**`design-reviewer` é o auditor designado para decisões internas do plugin** (free-read de `docs/decisions/` e `philosophy.md` per [ADR-009](ADR-009-revisor-design-pre-fato.md)/[ADR-011](ADR-011-wiring-design-reviewer-automatico.md)). Reviewer aplica os 4 critérios em planos/ADRs internos do plugin pré-commit.

**`code-reviewer` mantém rubrica YAGNI universal no diff** (independente de o diff ser plugin ou consumer). Quando flagrar estrutura doutrinal legítima do plugin no dogfood, override por inação do operador citando este ADR (pattern já estabelecido para reviewers — ver [ADR-026](ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md)).

## Efeito retroativo declarado

**Para `design-reviewer` durante review deste ADR:** ADR-035 ainda aparece como `Proposto` no momento desta review. Durante o free-read de `docs/decisions/`, ler ADR-035 como **referência histórica** (framing pré-inversão), não como doutrina vigente. Os 4 critérios de ADR-035 § "Filtro para decisões internas do plugin" permanecem válidos, mas reframados sob § "Ockham operacionalizado em decisões internas do plugin" deste ADR. Mitiga meta-loop espúrio (reviewer flagar incoerência "ADR-035 ainda Proposto enquanto ADR-043 declara substituição").

**Para `design-reviewer` em invocações futuras:** após a Implementação deste ADR ser aplicada, ADR-035 estará marcado `Substituído por ADR-043`. Reviewer trata ADR-035 como histórico em todas as invocações subsequentes.

**Para `code-reviewer` durante o dogfood da reforma doutrinária (ondas 2-4):** quando reframings/consolidações dispararem flags YAGNI no diff (ex.: adendos cross-ref em ADR-014/-016/-032/-036 da Onda 2; absorções em ADRs do cluster modo local da Onda 3), override por inação citando este ADR como justificativa. Não codificar nova exceção — a hierarquia que este ADR estabelece já cobre.

**Pattern editorial — exceção localizada, não precedente.** A instrução in-ADR ao reviewer durante a própria review (codificada nesta seção) é exceção localizada ao pattern normal do toolkit ([ADR-026](ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md) + [ADR-011](ADR-011-wiring-design-reviewer-automatico.md): reviewer forma juízo independente; operador absorve ou cutuca pós-fato). Justificada aqui pela coincidência temporal — ADR-035 aparece como `Proposto` apenas na janela narrow desta review específica; em invocações subsequentes ele já estará marcado `Substituído por ADR-043` e a tensão dissolve sem instrução. Pattern normal preserva juízo independente do reviewer; ver gatilho de revisão correspondente.

## Consequências

### Benefícios

- Hierarquia explícita elimina ambiguidade entre princípio e consequência operacional. Próximo dogfood (ondas 2-4) opera sob raiz estável.
- ADR-035 deixa de ser "exceção" e seu conteúdo essencial vira "instanciação contextual" — mais coerente com universalidade de Ockham.
- `design-reviewer` ganha benchmark fixo para auditar drift doutrinal cross-ADR — útil para a Onda 2 (reframings) e Onda 3 (consolidações).
- Mapping de regras pragmáticas → princípios fundamentais codificado como decisão estrutural, não só prosa em philosophy.md.

### Trade-offs

- 1 ADR adicional no inventário (atual 42 + este = 43). Mitigação: codifica relação estrutural emergente; ADR-035 fica Substituído (não removido), então o saldo líquido sobre doutrina **vigente** é 0 (1 entra, 1 sai como histórico). Cross-refs existentes a ADR-035 (philosophy.md linha 25 hoje; menções futuras absorvidas pela Onda 2 de reframings) ganham 1 hop indireto de leitura — custo cognitivo absorvido pelo trabalho de propagação da Onda 2, não eliminado.
- "Aplicação contextual do mesmo princípio" tem zona cinzenta na fronteira plugin/consumer — borderline cases (ex.: skill que é doutrinal e consumer-facing simultaneamente) ficam para `design-reviewer` julgar. Mitigação: os 4 critérios + pergunta umbrella são concretos o bastante para ancorar julgamento; cap restrito a "decisões doutrinais internas do plugin".

### Limitações

- ADR cobre apenas Ockham operacionalizado para decisões internas; § Decisão mapeia Verdade e Excelência mas não detalha sua operacionalização equivalente. Critérios concretos análogos para Verdade (verificação empírica) e Excelência (qualidade no escopo) emergirão organicamente — ou via gatilho de revisão "padrão de aplicação reflexa com OUTRO princípio" abaixo.
- Cross-refs retroativos em ADRs antigos (ADR-014, ADR-016, ADR-032, ADR-036) ficam para Onda 2 — este ADR codifica a inversão mas não propaga editorialmente para os ADRs reframáveis. Onda 2 da reforma cobre.

## Implementação

Edits cirúrgicos cobertos pela criação deste ADR + 3 follow-up edits no mesmo commit unificado (caminho ADR-only delegado por `/triage`):

1. **Este ADR** criado com Status: Proposto.
2. **ADR-035 Status edit:** header passa de "**Status:** Proposto" para "**Status:** Substituído por [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) (2026-05-29)" + nota inline curta no topo de § "Decisão" e § "Filtro para decisões internas do plugin" apontando para este ADR como sucessor que absorve. Conteúdo do ADR-035 preservado para referência histórica.
3. **`docs/philosophy.md` § Princípios fundamentais:** parágrafo curto ao final da seção (após "Mapping para a doutrina pragmática abaixo") com cross-ref a este ADR como codificação estrutural da hierarquia invertida. Substância: "A relação entre raízes epistêmicas e regras pragmáticas operacionais (incluindo aplicação contextual de Ockham a decisões internas do plugin, anteriormente codificada como exceção em [ADR-035](decisions/ADR-035-escopo-aplicacao-yagni-proprio-plugin.md), agora reframada como instanciação contextual em [ADR-043](decisions/ADR-043-hierarquia-doutrinal-fundamentais-raiz.md)) é codificada em [ADR-043]."
4. **`CLAUDE.md` § Editing conventions:** bullet cross-ref a este ADR no padrão dos bullets de ADR-010/-011/-023/-026/-034. Substitui o bullet atual de ADR-035 (que ficou obsoleto sob inversão; ADR Substituído não pertence a `Editing conventions`). **Sub-decisão:** entre (e1) substituir o bullet de ADR-035 vs (e2) manter ADR-035 como ponteiro histórico + adicionar ADR-043 — escolhida (e1) porque bullets em `Editing conventions` apontam para doutrina vigente, não Substituída; manter ADR Substituído violaria também o cap nominal de 200 linhas estabelecido em [ADR-024](ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md). Texto literal: "**Hierarquia doutrinal**: 3 princípios fundamentais (Verdade, Excelência sem over-engineering, Navalha de Ockham) são raiz epistêmica do toolkit; YAGNI/flat/sem-defensividade-ornamental são consequência operacional derivada per [ADR-043](docs/decisions/ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) — substitui ADR-035 absorvendo seus 4 critérios como § Ockham operacionalizado em decisões internas do plugin."

## Alternativas consideradas

### (a) Arquivar `pragmatic-dev-toolkit` e criar novo plugin com a doutrina refinada desde o início

Proposta original do operador na sessão upstream (turn 2 de 2026-05-29). Reset crisp das 42 ADRs + skills + agents + hooks; novo repo livre do "viés YAGNI antigo".

Descartada via análise dos próprios 3 princípios:

- **Verdade:** sampling dos ADRs mostrou que doutrina existente já opera implicitamente nos fundamentais (ADR-035 rejeita YAGNI reflexo interno; ADR-036 aplica Ockham puro; ADR-026 inverte default para absorver; gates de validação em `/run-plan`/`/debug` materializam Verdade). Alegação "várias ADRs no viés antigo" não passou crivo empírico — falta cross-ref explícito, não rewrite estrutural.
- **Excelência:** refactor in-place serve o problema concreto (codificar inversão + cross-ref retroativo) com edits cirúrgicos (1 ADR + 3 follow-up edits + adendos seletivos nas ondas 2-3). Archive-and-restart custaria semanas pra recuperar paridade, descartando 42 ADRs de incidentes empíricos codificados.
- **Ockham:** 1 plugin com hierarquia explícita > 2 instâncias do mesmo mecanismo (archived + new). Inversão de doutrina apex não cria entidade nova — refina relação entre princípios já existentes.

Custo-benefício ~10:1 contra archive. Decisão registrada na conversa upstream (commit `bebc34d` capturou decomposição da reforma).

### (b) Manter ADR-035 como Aceito com adendo cross-ref a este novo ADR (em vez de Substituído)

Sucessor parcial sem revogação — pattern usado em ADR-005 (parágrafo cross-ref em § Limitações para ADR-025) e ADR-011 (cross-ref em § Decisão para ADR-026).

Descartada: o objeto central de ADR-035 (codificar "exceção interna ao YAGNI") dissolve sob inversão. Não há mais "exceção" — há "aplicação contextual do mesmo princípio". Manter ADR-035 como Proposto/Aceito com adendo perpetuaria framing obsoleto e introduziria 2 leituras concorrentes sobre o que é a doutrina vigente. Os 4 critérios são absorvidos diretamente em § Ockham operacionalizado deste ADR; ADR-035 inteiro fica como referência histórica via Status: Substituído + nota inline em § Decisão.

### (c) Não criar ADR; só editar philosophy.md + bullet CLAUDE.md

Mais conciso; evita 1 ADR no inventário.

Descartada per [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) cond 1 (decisão estrutural sem ancestral direto — inversão de hierarquia doutrinal nunca codificada) + cond 5 (sucessor parcial de ADR-035 com supersedeção). Bullet em CLAUDE.md sem ADR perde Origem/Contexto/Alternativas/Gatilhos que justificam a inversão. Pattern simétrico ao descarte de "Só CLAUDE.md prosa, sem ADR" em ADR-034 § Alternativas (b) e ADR-035 § Alternativas (d).

### (d) Plano em `docs/plans/` coordenando ADR + edits cross-files

Plano com 1-2 blocos: bloco 1 cria ADR; bloco 2 aplica edits cross-files (ADR-035 Status, philosophy.md cross-ref, CLAUDE.md bullet). `/run-plan` orquestra com reviewer por bloco.

Descartada pelo próprio princípio que este ADR codifica (Ockham operacionalizado para decisões internas): edits cirúrgicos (3 follow-up touches) são cobertos pela seção § Implementação do próprio ADR; plano adicional não paga seu custo de manutenção pela clareza adicionada — alinhamento já feito em `/triage` upstream, edits diretos via Edit tool após `/new-adr` retornar.

## Gatilhos de revisão

- **4º princípio fundamental emergir empiricamente** (ex.: "Honestidade epistêmica", "Reversibilidade", "Falsificabilidade" como princípio paralelo) — reabre mapping em § Decisão + seção "Princípios fundamentais" de `philosophy.md`.
- **Padrão de aplicação reflexa interna emergir com OUTRO princípio doutrinal** (ex.: "flat por padrão" sendo invocado para vetar estrutura no plugin, paralelo ao gatilho que originou ADR-035 com YAGNI) — generalizar § "Ockham operacionalizado" ou criar ADR análogo dedicado ao novo princípio aplicado, codificando operacionalizações concretas para Verdade e Excelência.
- **Critérios concretos para Verdade e/ou Excelência aplicados a decisões internas do plugin emergirem em ≥2 sessões ad hoc** (ex.: `design-reviewer` exigir evidência empírica como filtro de adição de mecanismo — operacionalização concreta de Verdade; reviewer rebater sobre completude de mapping/cross-ref como filtro de coerência — operacionalização concreta de Excelência) — codificar operacionalização análoga à de Ockham. Sinal: ≥2 invocações ad hoc do princípio como filtro concreto em decisão, não como justificativa retórica. Fecha a parcialidade atual (apenas Ockham operacionalizado nesta v1).
- **5º critério legítimo para Ockham operacionalizado em decisões internas** emergir além dos 4 absorvidos (incidente, fronteira, contradição, ≥3 pattern) — refinar a seção com nova lista.
- **Princípio fundamental ser refutado empiricamente** (caso real onde Verdade/Excelência/Ockham levou a decisão demonstravelmente pior) — reabre o conjunto de raízes. Improvável mas registrado.
- **`code-reviewer` ou `design-reviewer` aplicar mal a hierarquia** em ≥2 PRs (justificar over-engineering como "consequência dos fundamentais" ou vetar estrutura legítima por aplicar YAGNI quando Ockham operacional endossaria) — refinar critério, adicionar guarda ou tornar mais mecânico.
- **≥2 ADRs futuros incluírem instruções direcionadas ao reviewer durante a própria revisão** (paralelo à § "Efeito retroativo declarado" deste ADR, ex.: "para design-reviewer: leia X como Y durante esta review", "para code-reviewer: aceite Z sem flag") — codificar pattern em ADR meta-editorial dedicado ou refinar critério de absorção em ADR-026 para acomodar a categoria. Hoje é exceção localizada justificada pela coincidência temporal específica (ADR-035 ainda Proposto na janela desta review); recorrência sinaliza categoria emergente que merece codificação explícita em vez de exceções ad hoc.

## Auto-aplicação coerente

Este ADR é ele próprio decisão doutrinal estrutural — codifica relação entre princípios já existentes em forma auditável. Pelos critérios de Ockham operacionalizado (esta mesma seção, aplicada retroativamente):

- **Critério 3 (contradição/refinamento de doutrina existente):** aplica — refina implicit-apex de YAGNI codificado nas fases iniciais do plugin sem ADR direto.
- **Critério 2 (fronteira doutrinal borrada):** aplica — partição "princípio fundamental vs regra operacional" estava implícita em philosophy.md; codificar fronteira via ADR distingue conceitos.
- **Critério 4 (codificação de pattern emergente ≥3x ad hoc):** aplica — ADR-035 (1ª aplicação implícita ao codificar exceção interna ao YAGNI); ADR-036 (2ª, aplicação invertida explícita do mesmo critério "paga custo" via Ockham puro — não codificar skill que raw-chat já distingue); decomposição da reforma no commit `bebc34d` (3ª, prep da Onda 1 aplicando os 4 critérios para decidir "codificar inversão agora" vs "adiar com refresh do backlog"). Pattern emergente passou o threshold; codificação como raiz era pendente.
- **ADR-034 cond 5 (sucessor parcial):** aplica — substitui ADR-035 absorvendo conteúdo essencial.
- **ADR-034 cond 1 (decisão estrutural sem ancestral direto):** aplica — inversão de hierarquia nunca codificada.

Cond 4 (categoria nova) **não** aplica — este ADR formaliza relação estrutural entre princípios já existentes em philosophy.md, não introduz categoria conceitual nova de artefato. Auto-consistente com leitura estreita de "categoria nova" estabelecida em ADR-034 § Auto-aplicação.

## Onda 1 da reforma doutrinária

Per umbrella line em `BACKLOG.md ## Próximos` (commit `bebc34d`). Próximas ondas (não escopo deste ADR):

- **Onda 2** — reframing de ADR-014/-016/-032/-036 com adendos cross-ref aos fundamentais (decisões intactas; só vocabulário YAGNI-as-veto modernizado).
- **Onda 3** — consolidação editorial dos clusters densos (modo local ADR-005/-018/-025/-030; cutucadas ADR-017/-029).
- **Onda 4** — refinamento do free-read do `design-reviewer` (ADR sucessor parcial de ADR-021 + edit no agent; alavanca real de token cost).
