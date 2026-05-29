# ADR-036: Brainstorm intencionalmente não-codificado em skill

**Data:** 2026-05-19
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) — critério "isso paga seu custo de manutenção pela clareza/coerência?" aplicado aqui na direção oposta (NÃO adicionar estrutura).
- **Precedente de forma:** [ADR-014](ADR-014-inventario-editorial-main-unico.md) — primeiro ADR do plugin formalizando decisão de não-mudança ("refatoração descartada por YAGNI" sobre inventário em `main` único); este aplica forma equivalente para "decisão de NÃO codificar skill" (status quo + alternativas analisadas + gatilhos de revisão concretos).
- **Investigação:** Sessão de análise comparativa entre `/draft-idea` do toolkit e skill `brainstorming` do plugin superpowers (2026-05-19).

## Contexto

Pergunta levantada na sessão: o plugin precisa de uma skill estilo `brainstorming` (do superpowers) que conduza diálogo exploratório sobre ideias de projetos ou abordagens para resolver problemas? Análise inicial sugeriu que `/draft-idea` seria upstream natural de `/triage` nesse papel — mas verificação concreta da SKILL.md mostrou que `/draft-idea` faz **entrevista estruturada** (5 seções fixas para preencher `IDEA.md`, papel `product_direction`), não brainstorm.

Gap real (mais estreito que o enquadramento inicial):

- **Borda A:** feature-scope com intenção vaga não tem porta de entrada no pipeline. `/triage` step 2 faz clarificação leve (1-3 gaps bloqueantes) com guardrail "não fazer entrevista exaustiva" — não é o lugar de exploração de design via 2-3 abordagens.
- **Borda B:** `/draft-idea` passo 1.5 (per [ADR-031](ADR-031-cutucada-condicional-draft-idea-projeto-maduro.md)) redireciona feature-em-projeto-maduro para `/triage` — assume que a intenção da feature já está formada, o que muitas vezes não está. Landing fraco.

Cenários já cobertos (não são gap):

- Ideia vaga de projeto novo → `/draft-idea` (papel `product_direction`).
- Bug intermitente → `/debug` (método científico).
- Decisão estrutural em formação → `/triage` step 2 (bifurcação arquitetural) → `/new-adr`.

## Decisão

**Brainstorm/exploração é intencionalmente NÃO codificado como skill no plugin.** Raw-chat com Claude é a ferramenta primária; o operador conduz diálogo informal até intenção cristalizar, depois entra no pipeline estruturado (`/draft-idea`, `/triage`, `/debug`, `/new-adr`).

Razões:

- **Filosofia do plugin é distribuir narrow, não codificar wide.** As skills existentes cobrem cenários específicos com fronteiras nítidas. Adicionar `/brainstorm` para preencher o gap "feature-scope vague intention" introduz uma skill cuja função se sobrepõe a `/triage` step 2 (bifurcação arquitetural) e cujo output (declaração-de-intenção transiente) não materializa artefato — sinal de que a estrutura interna não paga seu custo.
- **Evidência empírica do gap é fraca.** Nenhum incidente recorrente documentado (memory ou git log). [ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) codifica os 4 critérios como condição **suficiente** para adicionar estrutura; este ADR aplica a leitura editorial natural de que ausência deles é sinal forte (não prova mecânica) de que NÃO criar é o caminho. Verificando: não há (1) incidente recorrente, nem (3) refinamento de doutrina existente, nem (4) pattern emergente ≥3x ad hoc. O critério (2) "fronteira doutrinal borrada" aplicaria fracamente apenas à Borda B (landing do passo 1.5), mas o custo da skill nova (fronteira interna com `/triage` step 2 + manutenção + discoverability) supera o ganho marginal de cobrir só essa borda.
- **Raw-chat já entrega o trabalho.** Claude em diálogo livre é capaz de propor 2-3 abordagens com trade-offs quando solicitado. A codificação como skill agregaria valor real apenas em (a) discoverability nominal e (b) hand-off codificado para `/triage` — ganhos marginais que não justificam skill nova.
- **Reversibilidade explícita.** Se em uso real surgir incidente recorrente de operador travado pré-`/triage` com intenção feature-scope vaga, este ADR é revisitado (ver `## Gatilhos de revisão`).

A decisão materializa-se em três refinamentos não-criativos:

1. **`/draft-idea` passo 1.5 (redirect text):** opção `Direção de feature → /triage` é reformulada para reconhecer que feature-com-intenção-vaga tem como porta natural raw-chat antes de `/triage` (não direto para `/triage`, que pressupõe maturidade que o operador comprovadamente não tem se chegou em `/draft-idea`).
2. **`/triage` step 2 (cutucada de intenção vaga):** novo bullet no checklist mental detectando "intenção vaga demais para triar" (heurística: verbo aberto sem objeto direto + ausência de critério); cutucada em prosa sugerindo exploração raw antes ou pedindo objeto concreto. Fronteira com bifurcação arquitetural (que assume intenção formada com 2 caminhos vs intenção não-formada) explicitada.
3. **Nota em `docs/philosophy.md`:** documenta que brainstorm/exploração é intencionalmente não-codificado como skill — cross-ref para este ADR.

Refinamentos 1 e 2 (em `/draft-idea` e `/triage`) ficam registrados como linha em `## Próximos` do `BACKLOG.md` (artefato público auditável); são edits cirúrgicos doc-only delegáveis a `/triage` em sessão posterior. Refinamento 3 (`docs/philosophy.md`) + bullet em `CLAUDE.md` "Editing conventions" acompanham este ADR no commit unificado.

## Consequências

### Benefícios

- **Surface do plugin permanece igual** — nenhuma skill nova para manter, documentar, ou policiar contra invasão de escopo (especialmente vs `/triage` step 2 e `/draft-idea`).
- **Honestidade doutrinal** — registra explicitamente que raw-chat é a ferramenta certa para trabalho inerentemente exploratório, evita "codificar para codificar".
- **Fronteira nítida** — `/draft-idea` segue scope projeto, `/triage` segue clarificação leve + decisão de artefato; ambos sem competidor com identidade fluida.

### Trade-offs

- **Discoverability:** operador novo pode procurar uma "skill de brainstorm" e não encontrar. Mitigação: nota em `philosophy.md` documenta a ausência intencional + redirect refinado do `/draft-idea` passo 1.5 aponta para raw-chat.
- **Determinismo:** raw-chat tem variabilidade no protocolo (Claude pode ou não propor 2-3 abordagens estruturadas). Mitigação: operador pede explicitamente; quando a dúvida envolve bifurcação concreta, `/triage` step 2 já estrutura via enum nominal-comparativo.
- **Simetria interrompida:** `/draft-idea` cobre projeto-scope vague; não há equivalente para feature-scope vague. Aceito por simetria semântica fraca — direção de projeto tem artefato persistente (`IDEA.md`); feature-scope-vague não teria artefato.

### Limitações

- **Borda B remanescente:** mesmo com refinamento do passo 1.5, operador pode chegar via `/draft-idea` com feature-scope-vague e ter de re-explorar via raw-chat antes de `/triage`. Aceito — o refinamento informa o operador, não automatiza o roteamento.

## Alternativas consideradas

Dez opções enumeradas na análise da sessão; (a)-(j) abaixo cobrem o espaço completo.

### (a) Skill `/brainstorm` thin (~30-50 linhas)

Sem papel, sem artefato; protocolo de 3 passos (re-enquadrar problema, propor 2-3 abordagens, hand-off para `/triage`). Descarte: evidência empírica do gap é fraca, custo de fronteira interna vs `/triage` step 2 não compensa. **Reversibilidade:** se evidência empírica surgir (Gatilhos de revisão), esta é a opção de retomada padrão.

### (b) `/triage` ganha modo "intenção vaga"

Sub-rotina interna de exploração 2-3 abordagens quando step 2 detecta intenção vaga demais. Descarte: complica `/triage` (skill já carregada); guardrail "não fazer entrevista exaustiva" do step 2 vira contradição com sub-modo de exploração.

### (c) Fusão `/draft-idea` + `/brainstorm` em skill única (`/explore`)

Multi-shape anti-padrão — entrevista estruturada 5-seções vs diálogo aberto 2-3 abordagens são máquinas de estado distintas; fronteira interna paga mais que duas skills com fronteira nítida.

### (d) `/brainstorm` substituindo `/draft-idea`

Quebra role contract — papel `product_direction` é load-bearing em `/triage` step 1 (alinhamento à direção de produto); remover o artefato persistente `IDEA.md` exige restruturação do contrato de papéis.

### (e) Refactor de `/triage` step 2 em skill `/align` separada

Refactor massivo de skill central; [ADR-011](ADR-011-wiring-design-reviewer-automatico.md) amarrado a `/triage` plan-producing path. ROI baixo para gap pequeno.

### (f) Estender `design-reviewer` para conversa exploratória

Conflate review (verificação contra doutrina) com geração (exploração criativa) — modos cognitivos opostos.

### (g) Hard-gate estilo superpowers (`brainstorming` como bloqueio antes de qualquer trabalho criativo)

Filosofia incompatível — pragmatic-toolkit distribui narrow, superpowers concentra wide; importar shape estranha distorce o pipeline.

### (h) `/draft-idea` absorvendo brainstorm como sub-modo feature

Mesma armadilha de (c) — multi-shape skill.

### (i) Skill de exploração genérica (qualquer cenário: projeto + feature + problema + decisão)

Re-empacotamento de (c) com escopo ampliado — cada cenário tem dinâmica própria já coberta por skill específica.

### (j) Status quo refinado — **escolhido**

Nenhuma skill nova; refinar `/draft-idea` passo 1.5 + adicionar cutucada de "intenção vaga demais" em `/triage` step 2 + documentar em `philosophy.md`.

## Gatilhos de revisão

Este ADR é reavaliado quando ≥1 das seguintes evidências empíricas surge:

- **Incidente recorrente** (per [ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) critério 1): ≥3 ocorrências documentadas em git log / memory / `.claude/local/NOTES.md` de operador travado pré-`/triage` com feature-scope vague intention, onde raw-chat não chegou a estruturação útil dentro de 5-10 mensagens.
- **Pattern emergente ≥3x ad hoc** (per [ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) critério 4): operador conduzir manualmente o mesmo protocolo "propor 2-3 abordagens com trade-offs, comparar, escolher uma, formar intenção" em ≥3 sessões distintas — sinal de pattern pronto para codificação.
- **Contradição de doutrina:** mudança na filosofia do plugin (e.g., decisão de adotar hard-gate estilo superpowers) que torne brainstorm-como-skill coerente com a doutrina nova.

Em qualquer gatilho, alternativa (a) acima — skill `/brainstorm` thin — é o ponto de retomada padrão.

## Addendum (2026-05-29)

Onda 2 da reforma doutrinária ([ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md)) reframa esta decisão sob a hierarquia invertida: 3 princípios fundamentais (Verdade, Excelência sem over-engineering, Navalha de Ockham) como raiz epistêmica; YAGNI/flat/sem-defensividade ornamental como consequência operacional derivada.

**Fundamentais que endossam esta decisão:** **Ockham operacionalizado em decisões internas do plugin** — não codificar wide quando narrow + raw-chat já entrega; estrutura interna nova (skill `/brainstorm`) não paga seu custo de manutenção pela clareza/coerência adicionada. § Razões "Evidência empírica do gap é fraca" é operacionalização concreta do **critério 1** de [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § "Ockham operacionalizado em decisões internas do plugin" — aplicação **invertida** do critério (incidente recorrente **ausente** em uso real → sinal forte para NÃO criar skill, espelhando a leitura editorial natural do critério).

**Cross-refs body-level a ADR-035.** § Origem cita "**Decisão base:** ADR-035" — esse cross-ref permanece válido factualmente (ADR-036 foi decidido em 2026-05-19; ADR-043 foi shippado em 2026-05-29). ADR-035 está marcado `Substituído por ADR-043` em seu header; o critério "paga seu custo de manutenção pela clareza/coerência?" referenciado no body deste ADR (§ Razões) agora vive em [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § "Ockham operacionalizado em decisões internas do plugin".

**Preservação de numeração dos critérios.** Os critérios 1 e 4 referenciados em § Origem ("**Decisão base:** ADR-035 — critério 'isso paga seu custo de manutenção pela clareza/coerência?' aplicado aqui na direção oposta") e nos bullets de § Gatilhos de revisão (`per ADR-035 critério 1` e `per ADR-035 critério 4`) **preservam numeração idêntica** em ADR-043 § Ockham operacionalizado em decisões internas do plugin:

- **Critério 1** = incidente recorrente ou padrão observado em uso real (não hipótese). Operacionaliza Verdade.
- **Critério 4** = codificação de pattern emergente ≥3 vezes ad hoc em decisões anteriores do plugin (auditável retroativamente). Operacionaliza Verdade + Ockham.

Leitor que segue thread de gatilhos não precisa adivinhar equivalência — a numeração foi preservada por ADR-043 ao absorver os 4 critérios de ADR-035 como instanciação contextual de Ockham. Decisão central — brainstorm intencionalmente não-codificado como skill — permanece intacta sob a nova hierarquia.
