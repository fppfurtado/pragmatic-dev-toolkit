# ADR-071: Passo de prior-art scan no /triage (operacionaliza meta-system ADR-023)

**Data:** 2026-06-24
**Status:** Proposto

**Próxima revisão:** 2026-12-24
**Cadência:** trimestral
**Critério de erosão auditável:** ≥3 prior-art scans registrados no trail com zero adoção/extensão/inspiração (sinal de scan ritualístico) OU ≥3 builds custom não-triviais que passaram pelo `/triage` com scan evadido/não-registrado no trail → reabre a forma/placement do passo. Alimenta o `§ Critério de erosão` do meta-system ADR-023.

## Origem

- **Decisão base:** meta-system ADR-023 (`prior-art scan canonical pré-build — build-vs-adopt no inception`, commit `a4fa8bb`) — fixa a doutrina cross-cutting (what/why); este ADR materializa a faceta mecânica A2 (how) no repo dono do `/triage`.
- **Backlog:** issue #155 (forge).
- **Exemplar:** meta-system #49 (estávamos prestes a reinventar o Backstage Software Catalog); epic meta-system #50.

## Contexto

Meta-system ADR-023 fixou a doutrina cross-cutting de que um prior-art scan (varredura de soluções de mercado validadas + comparação build-vs-adopt) deve preceder a decisão de construir algo não-trivial — no inception, não pós-fato. Pela regra cross-cutting-vs-mechanical, a doutrina (what/why) mora no meta-system; a mecânica (how) mora no repo que possui o ponto de decisão. No toolkit, esse ponto é o `/triage`: é onde a intenção cristaliza e o artefato (linha de backlog, plano, ADR, atualização de domínio) é decidido.

Hoje o `/triage` decide o artefato sem nenhum passo que force a pergunta build-vs-adopt antes de comprometer com build custom. O risco é concreto e já materializado upstream (exemplar #49). Falta operacionalizar localmente a faceta mecânica A2 de ADR-023 — sem duplicar a doutrina, apenas portando o gatilho proporcional, a resposta-em-espectro e o trail auditável para dentro do fluxo do `/triage`.

A forma técnica é decisão local per meta-system ADR-016 (target-aware packaging): o scan pode ser passo inline na skill (prosa/heurística), util determinístico, ou outra forma.

## Decisão

Adicionar um passo de **prior-art scan** ao `/triage`, na forma **inline-prosa** (sub-passo heurístico na própria skill).

- **Forma = inline-prosa (target-aware per meta-system ADR-016).** Um prior-art scan é julgamento heurístico-semântico dominante (avaliar fit de solução de mercado, raciocinar build-vs-adopt, decidir espectro keep/adopt/extend/inspire) — classificação NEGATIVA para mecanização sob a própria `/scan-mechanicality` do toolkit. Sub-tool determinístico forçaria mecânica sobre núcleo semântico (contraria Ockham); MCP/CLI não se justifica a priori. A forma canonical é a mesma das demais gates do `/triage` (intenção-vaga, escopo, decomposição, bifurcação): prosa-heurística operada pelo agente.

- **Placement.** Sub-passo dentro do step 2 (esclarecer gaps), posicionado **após** os gates de intenção-vaga / escopo / decomposição (pressupõe intenção cristalizada — não faz sentido escanear prior-art de uma intenção que ainda não tem objeto), **antes da resolução de bifurcação arquitetural** e **antes** do step 3 (decidir o artefato). O resultado do scan informa a decisão build-vs-adopt, que molda qual artefato é produzido. A ordem scan→bifurcação é deliberada: o scan decide build-vs-adopt, e uma conclusão de "adotar inteiro" / "inspirar-se em parte" pode tornar a bifurcação (qual caminho **construir**) irrelevante — não faz sentido resolver "como construir" antes de decidir "construir afinal". O scan é **gate prosa-heurística** (como a gate de intenção-vaga), não enum: **não compete na chamada `AskUserQuestion` unificada do step 2 nem sequencia um prompt adicional** — o step 2 é checklist mental, não questionário sequenciado, e a unificação de prompts enum-áveis é preservada. Raciocínio in-line em prosa também blinda o Goodhart guard (gate raciocinado é mais difícil de virar checkbox que um enum).

- **Gatilho proporcional (portado de ADR-023).** Dispara em: nova capacidade / novo formato-protocolo / build custom não-trivial. Não dispara em: bugfix, refactor interno, doc, glue acoplado ao setup pessoal. Zona cinzenta → default conservador: na dúvida, escanear (é barato); registrar a decisão de pular quando se pula.

- **Resposta em espectro (portada de ADR-023).** O scan informa um espectro, não binário: construir / adotar inteiro / estender parcial / inspirar-se em parte (emprestar modelo, vocabulário, pattern). Aprender com partes é resultado de primeira classe.

- **Trail auditável.** O passo deixa registro de: scan feito? decisão keep/adopt/extend/inspire? por quê? — registrado no artefato produzido (`## Contexto` do plano quando há plano; prosa do report nos demais caminhos). O trail alimenta o `§ Critério de erosão` do meta-system ADR-023 (≥3 scans zero-adoção OU ≥3 builds com scan evadido).

- **Goodhart guard.** Evitar scan ritualístico — o gatilho proporcional (não dispara em bugfix/refactor/doc/glue) é a primeira linha de defesa; o trail auditável é a segunda (torna o scan ritualístico detectável).

Razões:

- Operacionaliza a faceta mecânica A2 de ADR-023 sem duplicar a doutrina — separação cross-cutting (meta-system) vs mechanical (repo dono).
- Forma coerente com o resto do `/triage` (todas as gates são prosa-heurística) — zero mecanismo novo, custo de manutenção marginal.
- Ataca um risco concreto e já materializado (reinventar solução de mercado validada) no único ponto do fluxo onde a decisão build-vs-adopt ainda é barata de reverter (inception).

## Consequências

### Benefícios

- Build-vs-adopt entra no inception do `/triage`, quando reverter a decisão custa menos.
- Trail auditável alimenta o critério de erosão de ADR-023 — o mecanismo se monitora.
- Forma inline-prosa não adiciona superfície de manutenção nova (sem sub-tool, sem dependência externa, sem toolchain).

### Trade-offs

- Aumenta o step 2 do `/triage` com mais um gate condicional. Mitigação: gatilho proporcional restringe o disparo a build não-trivial; bugfix/refactor/doc/glue não pagam o custo.
- Risco de scan ritualístico (cerimônia que sempre conclui "construir"). Mitigação dupla: gatilho proporcional + trail auditável que torna o ritualismo detectável e alimenta o critério de erosão.

### Limitações

- A qualidade do scan depende do julgamento do agente e do acesso a fontes (WebSearch / conhecimento) no momento do `/triage`. Não há garantia determinística de cobertura de mercado — é heurística por construção, consistente com a forma escolhida.

### Relação com a família triage-ecosystem

4ª trajetória de wiring no `/triage` além de ADR-036 (brainstorm intencionalmente não-codificado — upstream do `/triage`), ADR-053 (wiring do design-reviewer) e ADR-063 (caminho-atômico → prompt-reviewer). Ortogonal aos reviewers: o scan é um gate de decisão pré-artefato, não um eixo de revisão pós-fato.

## Alternativas consideradas

### Sub-tool determinístico (`skills/triage/sub-tools/prior-art-scan.py`)

Descartada. O núcleo de um prior-art scan é semântico (julgar fit de mercado, decidir espectro build-vs-adopt). A parcela determinística (e.g., consultar um registry) é mínima e não cobre a decisão. Forçar um util sobre substância heurística contraria a Navalha de Ockham e a classificação target-aware (meta-system ADR-016) — confirmado pela `/scan-mechanicality` do próprio toolkit (NEGATIVO para mecanização).

### Plano-só, sem ADR local

Descartada no `/triage`. Registraria forma/gatilho/trail no `## Contexto` do plano referenciando ADR-023, sem ADR local. Perde o registro estrutural da decisão de forma (target-aware) e da relação com a família triage-ecosystem (ADR-053/-063) — exatamente o que ADR-034 § condições (nova categoria de gate + operacionaliza restrição externa de longa duração) prescreve registrar como ADR.

### Restringir o gatilho ao caminho-com-plano/ADR (simetria com ADR-053)

Descartada. ADR-053 § Decisão (b) poupa deliberadamente o caminho-leve (não dispara design-reviewer em linha de backlog pura), e por simetria poderia-se restringir o scan aos caminhos pesados (plano/ADR). Mas a simetria é incoerente aqui: o scan roda no **step 2, antes do step 3 decidir o artefato** — o tipo de artefato ainda não existe quando o scan dispararia, então gatear por "é plano/ADR?" exigiria mover o scan para depois da decisão do artefato, invertendo a relação causal (o scan **informa** a escolha do artefato, não o contrário). O discriminador coerente é a **natureza do trabalho** (build não-trivial), não o tipo de artefato; e o gatilho proporcional por natureza-do-trabalho já poupa exatamente os casos leves que ADR-053 poupa (bugfix/refactor/doc/glue), apenas discriminados por outro eixo. A ortogonalidade com os reviewers (gate pré-artefato vs eixo de revisão pós-fato) é preservada.

## Auto-aplicação (critério ADR-034)

Novo ADR (não adendo) justificado por ≥1 das 5 condições de ADR-034:

- **Cond 4 (introduz categoria nova) — primária.** O prior-art scan é uma categoria de gate nova no `/triage` (decisão build-vs-adopt pré-artefato), distinta dos gates existentes (intenção-vaga, escopo, decomposição, bifurcação) e dos eixos de revisão pós-fato.
- **Cond 3 (codifica restrição externa de longa duração) — secundária.** Operacionaliza localmente a doutrina cross-cutting do meta-system ADR-023 — restrição doutrinal estável que mora upstream.

Demais condições não aplicam: não há ancestral local substituído (cond 2) nem sucessão parcial de ADR local vigente (cond 5). A § Override do critério N=3 **não** se aplica: este ADR não cria abstração interna prematura (o gatilho de N=3 governa codificação de pattern com <3 instâncias ad hoc) — é decisão de wiring justificada pelas condições acima, independente do eixo N=3. O débito de meta-avaliação da onda Override (vencido na 8ª aplicação, ADR-070; deferido a `/triage`) permanece aberto e fora do escopo deste ADR.

## Gatilhos de revisão

Dois eixos distintos, que não devem colapsar num só (evita falso negativo onde o gate local nunca dispara por ser lido como responsabilidade upstream):

- **Eixo local** — reabre a **forma/placement deste passo no `/triage`** (decisão deste ADR):
  - **Empírico forward (forma):** ≥3 prior-art scans registrados no trail com zero adoção/extensão/inspiração (scan ritualístico) → reabre forma/placement.
  - **Empírico forward (evasão):** ≥3 builds custom não-triviais que passaram pelo `/triage` com scan evadido/não-registrado no trail → reabre o gatilho ou o enforcement.
- **Eixo upstream** — o trail **alimenta, mas não substitui**, o `§ Critério de erosão` do meta-system ADR-023 (quando reabrir a doutrina cross-cutting). A forma local pode erodir sem a doutrina upstream erodir, e vice-versa.
