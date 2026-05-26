# ADR-037: Código-como-fonte-de-verdade vs intent-as-truth (contraste spec-driven)

**Data:** 2026-05-25
**Status:** Proposto

## Origem

- **Investigação:** Análise comparativa entre o `pragmatic-dev-toolkit` e [github/spec-kit](https://github.com/github/spec-kit) (sessão de 2026-05-25). Spec-kit articula a tese central oposta — *"Specifications don't serve code — code serves specifications. ... Specifications become the primary artifact, with code as its expression in a particular language and framework, inverting typical AI generation where output is generated first and documentation follows"* (`spec-driven.md`). ROADMAP item 2 sintetizou a antítese e marcou este ADR como âncora doutrinal necessária.
- **Decisão base:** [ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) — critério "isso paga seu custo de manutenção pela clareza/coerência?" qualifica este ADR por (3) refinamento/contradição de doutrina existente (codifica fronteira que vive implícita em `philosophy.md` + ADR-004 + ADR-032 + ADR-035) e (4) codificação de pattern emergente (escolhas editoriais de todas as 12 skills já assumiram code-as-truth ad hoc).
- **Classificação editorial:** Pelo [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md), condição (i) (decisão estrutural duradoura sem ancestral — "código-como-fonte-de-verdade" nunca codificado em ADR) aplica → novo ADR, não adendo. ADR-035 cobre YAGNI scope; ADR-004 cobre state-tracking; nem a decisão central de cada um cobre code/doctrine primacy.

## Contexto

O `pragmatic-dev-toolkit` opera sob uma premissa implícita até hoje não codificada: **código é fonte de verdade**; doutrina (`philosophy.md`, ADRs, planos, backlog, `domain.md`, `design.md`, NOTES) registra intenção, restrições, decisões estruturais e contexto capturado, mas **não gera código**. Toda skill do plugin lê código como fato canônico e produz ou alinha artefatos doutrinais em torno dele. `design-reviewer` audita planos/ADRs contra doutrina existente; `code-reviewer` audita diffs; `/triage` decide qual artefato captura intenção antes de codar; `/run-plan` executa as decisões do operador. A doutrina nunca gera o código, nunca alega regenerá-lo de specs, nunca inverte a primazia.

Essa postura é antitética a spec-driven development (SDD), articulada explicitamente em spec-kit. SDD propõe que specs sejam artefatos executáveis e generativos: o pipeline `constitution → specify → clarify → plan → tasks → implement` regenera código a partir de specs refinadas; `[NEEDS CLARIFICATION]` markers persistem incerteza no próprio spec; bidirectional feedback prod→spec realimenta regeneração; e a afirmação central é que *"specifications must be precise, complete, and unambiguous enough to generate working systems"*.

Hoje a postura "code-as-truth" do plugin aparece **implicitamente** em:

- `philosophy.md` "flat & pragmatic" + YAGNI por padrão.
- [ADR-004](ADR-004-state-tracking-em-git.md) — state in-flight vive em git/forge (código + branches + PRs), não em documentos doutrinais.
- [ADR-027](ADR-027-skill-draft-idea-elicitacao-product-direction.md) — `/draft-idea` elicita `IDEA.md` mas o artefato é lido por humano/agente como contexto de alinhamento, não executado como spec.
- [ADR-032](ADR-032-skill-note-contexto-compartilhado.md) — `/note` captura intenção/contexto cross-session; nunca gera código.
- [ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) — doutrina interna do plugin serve clareza/coerência, não regeneração.
- [ADR-036](ADR-036-brainstorm-intencionalmente-nao-codificado-em-skill.md) — brainstorm/exploração não vira skill porque operador é autor primário do raciocínio criativo; mesma postura aplicada ao polo exploratório.
- Forma de todas as skills shipadas: `/triage` → `/run-plan` (humano/agente escreve código lendo artefatos; artefatos não escrevem código).

Sem codificação explícita, contribuidor futuro propondo "vamos virar spec-first / generativo" força reconstruir a doutrina ad hoc cada vez. O custo de raciocinar o contraste cresce; doutrina vira frágil à drift em direção a abordagens spec-heavy que contradizem o design do plugin.

## Decisão

A doutrina de design do plugin é **código-como-fonte-de-verdade**: código é o fato canônico sobre o sistema; doutrina (`philosophy.md`, ADRs, planos, backlog, domain, design notes, NOTES) registra intenção, decisões estruturais, contexto capturado e linguagem ubíqua — mas **não gera nem regenera código**.

Concretamente:

1. **Nenhuma skill** do plugin trata artefato doutrinal como input para geração de código. `/triage` produz planos que alinham humanos sobre o quê fazer; `/run-plan` executa per plano com humano/agente escrevendo código como autor primário. Plano é scaffolding contextual, não fonte.
2. **Reviewers auditam diffs e artefatos** contra doutrina, mas não produzem código. Doutrina restringe/critica; código responde.
3. **Bidirectional feedback existe** mas é mediado por humanos: realidade de produção, incidentes e aprendizados informam criação de ADRs e atualizações de `philosophy.md` — loop editorial manual, não regeneração automática. (Per `philosophy.md`: flat & pragmatic resiste à automação excessiva.)
4. **Decisões de design do plugin seguem esta doutrina**: novas skills/agents/hooks avaliadas contra 3 sinais mecânicos. Disparo de ≥1 → rejeitar por default:
   - (i) Componente propõe **gerar ou regenerar código** a partir de artefato doutrinal (plano, ADR, `IDEA.md`, etc.) como saída direta.
   - (ii) Componente propõe **substituir autoria humana/agente** por execução automática de spec (pipeline `spec → code`).
   - (iii) Componente propõe **loop bidirecional automático sem ponto de revisão humano** (auto-regeneração doutrina↔código).

   `design-reviewer` é o auditor designado deste filtro em propostas via ADR/plano (per [ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md)).
5. **Distinção entre elicitar doutrina e gerar código.** Skills do plugin (`/draft-idea`, `/triage`, `/new-adr`) elicitam ou estruturam artefatos doutrinais (`IDEA.md`, planos, ADRs) — mas o artefato gerado é **lido por humano/agente como scaffolding cognitivo**, não executado como spec por um pipeline gerador. A fronteira nítida com spec-driven é: "doutrina como contexto consumido por autor primário humano/agente" vs "doutrina como input executável de pipeline de regeneração". Eliciar doutrina ≠ gerar código de spec.

**Esta decisão é de escopo plugin-internal apenas.** Governa como os próprios componentes do plugin são desenhados e como novas skills/agents/hooks são avaliados para inclusão. **Não prescreve como projetos consumidores devem operar.** Um consumer project pode adotar spec-driven development (usando github/spec-kit, pipelines spec→code próprios, etc.) sem conflito — as skills do plugin continuarão operando sobre a separação code/doctrine como desenhadas; workflows consumer-specific vivem ao lado.

## Consequências

### Benefícios

- Doutrina explicitada — futuro contribuidor lê este ADR antes de propor evolução para spec-first generativo; recusa torna-se baseada em referência, não argumento ad hoc.
- Coerência editorial para novas skills — critério claro de admissão ("preserva code-as-truth?").
- Fronteira nítida com spec-kit (e outras ferramentas spec-first) — operador escolhendo entre toolkits sabe o que cada um propõe.
- README pode posicionar o plugin com contraste crisp (ROADMAP item 4 absorve esta âncora).

### Trade-offs

- Plugin não absorve ganhos teóricos de spec-driven development (consistency check automatizado spec↔code, regeneration loops, [NEEDS CLARIFICATION] markers persistentes). Aceito porque doctrine-as-source carrega custo cognitivo e de manutenção que contradiz "flat & pragmatic" (`philosophy.md`).
- Operador consumidor que prefere abordagem spec-first deve compor com outra ferramenta (spec-kit, pipeline custom). Plugin não bloqueia mas não cobre.

### Limitações

- Doutrina é declarada para o **plugin**, não prescritiva para consumer projects. Consumer adotando spec-first não viola este ADR — mas pode ter atrito leve com algumas convenções (ex.: `/triage` assume decisão sobre artefato precede o código, não código gerado de spec). Atrito é tolerado; plugin não tenta cobrir o caso.

## Alternativas consideradas

### (a) Não codificar — manter doutrina implícita

Descartado. Sem ADR explícito, contribuidor futuro reabre a discussão do zero; cada nova skill que toca território cinzento (geração de prompt, template engine, code generator) precisa reconstruir o filtro "isso é doctrine-as-source?". Custo cognitivo recorrente. ADR-035 critério (3) aplica.

### (b) Codificar como adendo em ADR-035 ou ADR-004

Descartado por [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) condição (i) — "código-como-fonte-de-verdade" é decisão estrutural duradoura sem ancestral direto. ADR-035 é sobre YAGNI scope (filtro para decisões internas), ADR-004 sobre state-tracking (where in-flight state lives); nem a decisão central deles cobre code/doctrine primacy. Adendo borraria a fronteira doutrinária de ambos.

### (c) Adotar spec-driven development (espelho parcial ou total do spec-kit)

Descartado. Antítese ao "flat & pragmatic" registrado em `philosophy.md`. Adoção exigiria refactor estrutural de todas as skills (substituir `/triage` por `constitution → specify → clarify → plan → tasks → implement`); contradiz philosophy.md e o critério editorial flat. Skills, agents e hooks deixariam de servir o operador como **auxiliar de raciocínio** para tornarem-se **pipeline de geração** — mudança de identidade do plugin.

### (d) Manter neutralidade explícita (declarar "o plugin não opina sobre spec vs code primacy")

Descartado. Neutralidade é não-decisão; gera o mesmo custo recorrente da alternativa (a). Decisões internas (novas skills, new ADRs) demandariam o filtro caso-a-caso.

### (e) Adotar code-as-source generativo (doutrina derivada do código)

Polo simétrico oposto a spec-first: hooks/reviewers extrairiam doutrina do código (linguagem ubíqua inferida de identifiers, ADRs sugeridos a partir de padrões detectados, drift entre ADR e implementação aberto como PR), invertendo o sentido da geração mas mantendo código como autoridade. Antípoda interno legítimo do spec-kit. Descartado pelo mesmo princípio do item 3 da § Decisão — bidirectional feedback existe mas é mediado por humanos; loop editorial manual resiste à automação per `philosophy.md` ("flat & pragmatic"). Adicionalmente: extração automática de doutrina dispara o sinal #1 do critério da § Decisão item 4 (componente propõe gerar artefato doutrinal a partir de outra fonte como saída direta) e o sinal #3 (loop bidirecional sem ponto de revisão humano).

## Gatilhos de revisão

- **Adoção generalizada de spec-driven em comunidade Claude Code**: evidência editorial via discussions, conferências, ou pedido explícito de consumer relevante — sinal recorrente de que ferramentas spec-first deveriam ser primeiro-classe no plugin (ou que ele permanece nicho code-as-truth). Sem mecanismo de telemetria de consumers, gatilho é qualitativo per pattern [ADR-021](ADR-021-curadoria-free-read-design-reviewer.md).
- **LLM autoral autônomo confiável**: se modelos passarem a gerar código consistente de specs sem necessidade de revisão humana significativa, o trade-off de doctrine-as-source muda. Reavaliar.
- **Solicitação consumer por hook bidirecional**: se ≥3 consumer projects pedirem mecanismo de "spec ↔ code consistency check" como feature do plugin, considerar oferecer como skill complementar (não substituindo o core, alinhado com a limitação aceita na § Limitações).
