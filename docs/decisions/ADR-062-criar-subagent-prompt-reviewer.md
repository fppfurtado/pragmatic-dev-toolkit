# ADR-062: Subagent `prompt-reviewer` — 6º reviewer paralelo aos shippados

**Data:** 2026-06-13
**Status:** Proposto

## Origem

- **Plano:** `docs/plans/prompt-reviewer-criar-subagent.md` (caminho-com-plano gerado via `/triage` upstream 2026-06-13).
- **Decisão base:** [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § Ockham operacionalizado #4 — substrato doutrinal para Override do critério N=3 em decisões internas do plugin.
- **Decisão base (precedente direto):** [ADR-057](ADR-057-curate-backlog-manutencao-editorial-periodica.md) — precedente canonical de Override do critério N=3 registrado em ADR + gatilho de revisão concreto (6 meses pós-shipping; ≤2 invocações OR findings inúteis ≥50%).
- **Decisão base (precedente direto):** [ADR-061](ADR-061-skill-session-audit-categorias-editoriais.md) — segundo precedente do mesmo Override, sucessor parcial lateral de ADR-057.
- **Decisão base (rejeição histórica endereçada):** [ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) (Substituído por ADR-043 em 2026-05-29) — plano `docs/plans/v1.8-cenarios-validacao-manual.md` rejeitou `prompt-reviewer` por YAGNI reflexo interno em 2026-02. ADR-043 dissolveu a base da rejeição via inversão de hierarquia doutrinal (YAGNI consumer ≠ filtro autoaplicado a decisões internas do plugin).
- **Decisão correlata:** [ADR-050](ADR-050-componentes-plugin-consolidado.md) — naming canonical de agents (`<role>` stack-agnóstico). `prompt-reviewer` segue o pattern.
- **Investigação:** sessão CC `prompts` no `h3-finance-agent` (2026-06-13) registrou o gap empírico — prompts agentic com inconsistências de algoritmo (passos conflitantes, vagos, ambíguos, contraditórios) produzem resposta do modelo imprecisa/imprevisível. Operador articulou o pattern como classe nomeável com substância universal stack-agnóstica.

## Contexto

Os 5 reviewers shippados cobrem eixos disjuntos:

- `code-reviewer` (`agents/code-reviewer.md`) — rubrica YAGNI/anti-padrão em diff de código pós-fato.
- `design-reviewer` (`agents/design-reviewer.md`) — decisão estrutural pré-fato em plano (`docs/plans/`) ou ADR draft.
- `qa-reviewer` (`agents/qa-reviewer.md`) — qualidade de teste recém-escrito (caminho feliz, invariantes, edge cases).
- `security-reviewer` (`agents/security-reviewer.md`) — segredos, validação em fronteiras, I/O externo.
- `doc-reviewer` (`agents/doc-reviewer.md`) — drift entre documentação e código no diff.

Nenhum cobre o eixo **qualidade algorítmica de prompts markdown** — a consistência interna de instruções escritas como prompt para um agente LLM. Esta classe de problema é distinta:

- **Não é código** (sintática de linguagem de programação) — `code-reviewer` não se aplica.
- **Não é decisão estrutural pré-fato** — o prompt já está escrito; `design-reviewer` analisa decisão, não instrução operacional.
- **Não é teste** (qualidade de validação automatizada) — `qa-reviewer` não se aplica.
- **Não é fronteira de segurança** — `security-reviewer` não se aplica.
- **Não é drift doc-código** — `doc-reviewer` analisa correspondência entre dois artefatos; aqui o prompt é monolítico, o gap é interno ao próprio prompt.

A fronteira é nítida — prompt-as-instrução-ao-agente é categoria conceitual nova de revisão, paralela mas distinta às 5 existentes.

A substância foi capturada empiricamente em sessão `prompts` do `h3-finance-agent` (2026-06-13). Operador articulou que o problema é recorrente em projetos agentic — quando o prompt tem passos conflitantes, vagos, ambíguos ou contraditórios, o modelo emite resposta imprecisa/imprevisível, e o pattern é caro de diagnosticar pós-fato (debugging de prompt agentic é problema de "primary diagnosis em sessão diferente" — alta latência de feedback).

Override do critério N=3 (ADR-043 § Ockham operacionalizado #4): 1 instância documentada (sessão `prompts` 2026-06-13), declaração informada de recorrência stack-agnóstica em outros projetos agentic do operador (paralelo direto ao precedente ADR-057 § Override e ADR-061 § Override).

Ockham operacionalizado avalia (ADR-043 § Ockham, ≥1 dos 4 critérios basta):

- **Critério 1 (incidente recorrente):** parcial — 1 instância materializada + declaração informada de instâncias ad hoc não-registradas. Override aplica.
- **Critério 2 (fronteira doutrinal borrada):** sólido — categoria "qualidade algorítmica de prompts" não existe nos 5 reviewers; modelar essa fronteira distingue conceitos que se confundiriam sem ela.
- **Critério 3 (contradição/refinamento de doutrina existente):** parcial — refina inventário canonical de reviewers de 5 para 6.
- **Critério 4 (≥3 pattern emergente ad hoc):** falha materialização explícita — Override registrado para auditoria futura.

Critério 2 endossa diretamente; critério 1+3 reforçam; critério 4 cai sob Override.

A rejeição histórica em `docs/plans/v1.8-cenarios-validacao-manual.md` (citada em § Origem) não é argumento contra este ADR — sua base doutrinal (YAGNI reflexo interno) foi dissolvida por ADR-043.

## Decisão

**Cria-se o 6º reviewer `prompt-reviewer` em `agents/prompt-reviewer.md`, seguindo o pattern canonical dos 5 shippados. Escopo v1 do auto-trigger é restrito a paths de prompt markdown nomeáveis. Pattern de dispatch substitui `doc-reviewer` como default nesses paths via regra "default mais-específico-vence". Override do critério N=3 (ADR-043 § Ockham operacionalizado #4) registrado análogo a ADR-057/-061.**

### Escopo v1 do auto-trigger

Paths sob default automático `prompt-reviewer`:

- `agents/*.md`
- `skills/**/SKILL.md`
- `docs/plans/*.md`

Resto do `.md` (incluindo `README.md`, `docs/decisions/*.md`, `docs/philosophy.md`, `CLAUDE.md`, `BACKLOG.md`, `NOTES.md`, `docs/procedures/*.md`) preserva `doc-reviewer` como default.

Fora do escopo v1: strings de prompt embutidas em código (`.py`, `.ts`, `.go`, etc.). Reabre via gatilho de revisão.

### Pattern de dispatch (regra default mais-específico-vence)

A regra de dispatch atual vive em `skills/run-plan/SKILL.md` linha 129 (operacional) e `agents/doc-reviewer.md` linha 8 (cross-ref informativo). `CLAUDE.md` § Plugin component naming nomeia anotações `{reviewer: <perfil>}` na tabela de componentes mas não codifica explicitamente a regra "bloco doc-only → doc-reviewer default" — fica na skill.

Hoje (pré-ADR-062), `skills/run-plan/SKILL.md` linha 129 prescreve:
- Sem anotação → `code-reviewer` default.
- **Exceção:** paths do bloco não-vazios e todos com extensão `.md`/`.rst`/`.txt` → default vira `doc-reviewer` (bloco vazio, path sem extensão, ou bloco misto caem na regra default).
- `{reviewer: <perfil>}` → override explícito.

Este ADR introduz **regra hierárquica de dispatch path-based** — categoria mecânica nova de path-set matching com resolução por especificidade. A extensão concreta acontece em `skills/run-plan/SKILL.md` linha 129 (localização canonical da dispatch logic; CLAUDE.md ganha cross-ref na tabela de componentes mas não duplica a regra). Pós-ADR-062 a regra fica:

- Sem anotação → `code-reviewer` default.
- **Exceção doc-only narrow**: paths do bloco não-vazios e todos em `agents/*.md` ∪ `skills/**/SKILL.md` ∪ `docs/plans/*.md` → default vira `prompt-reviewer` (este ADR).
- **Exceção doc-only ampla**: paths do bloco não-vazios e todos com extensão `.md`/`.rst`/`.txt` fora dos paths acima → default vira `doc-reviewer` (regra existente preservada).
- `{reviewer: <perfil>}` → override explícito sempre vence.

A regra é hierárquica (mais específico vence o mais genérico). Operador pode forçar via `{reviewer: doc}` em bloco que tocaria `agents/*.md`; e vice-versa.

### Fronteira prompt-reviewer ↔ design-reviewer em `docs/plans/*.md`

`design-reviewer` auto-disparado em `/triage` plan-producing path (per ADR-053 § Decisão (b), pré-commit, sobre o plano recém-criado) opera num momento distinto de `prompt-reviewer` auto-disparado em `/run-plan` per bloco que toca `docs/plans/*.md`. Os dois reviewers cobrem eixos disjuntos sobre o mesmo artefato em momentos diferentes do lifecycle:

- **design-reviewer no `/triage` step 5**: decisão estrutural pré-fato (alternativa ausente, abstração prematura, ADR-worthiness, contradição com doutrina canonical). Plan body como objeto de decisão.
- **prompt-reviewer no `/run-plan` per bloco** que toca `docs/plans/<slug>.md`: qualidade algorítmica do plan body (passos conflitantes/vagos/ambíguos/contraditórios). Plan body como instrução-ao-agente.

Eixos disjuntos por design. Caso findings contraditórios sobre o mesmo plan body emerjam → sinal de fronteira mal calibrada (gatilho de revisão #3.5 abaixo).

### 4 heurísticas seed do `prompt-reviewer`

Codificadas no body do agent (paralelo às sub-headings de `code-reviewer`/`design-reviewer`):

1. **Passos conflitantes** — passo N afirma A, passo M afirma ¬A; condições mutuamente exclusivas no mesmo gate; loop com condição de saída contraditória ao corpo.
2. **Passos vagos** — instrução sem gatilho concreto ("considere", "avalie", "verifique" sem critério mecânico ou enumeração de caso); subjetividade que o modelo terá que resolver arbitrariamente.
3. **Passos ambíguos** — múltiplas interpretações válidas para a mesma instrução; ordem de operações implícita; pronome com antecedente indeterminado.
4. **Passos contraditórios em estado global** — passo K mantém invariante X, passo L viola X sem reconhecer; estado declarado fora do passo (ex.: "se papel resolveu local") inconsistente com estado assumido em outro passo.

### Template de output

Paralelo aos 4 reviewers existentes (Localização / Problema / Heurística violada / Sugestão). Idioma do relatório per `CLAUDE.md` → 'Reviewer/skill report idioma'. Close-clean wording explícito ("Prompt alinhado — nenhuma inconsistência algorítmica.").

### Override do critério N=3 — registrado explicitamente

[ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § Ockham operacionalizado critério 4 prescreve ≥3 aplicações ad hoc auditáveis retroativamente antes de codificar pattern como abstração. BACKLOG line registrava UMA instância materializada (sessão CC `prompts` do `h3-finance-agent`, 2026-06-13). Operador em `/triage` (toolkit, 2026-06-13) sobrescreveu o critério: a substância foi declarada como classe nomeável com material universal stack-agnóstica suficiente.

**Reconhecimento de assimetria com precedentes ADR-057/-061.** O Override aqui é **mais frágil** que ADR-057 e ADR-061:

- ADR-057 (§ Override): operador declarou ≥3 instâncias em outros repos no ato do `/triage` ("essa demanda já ocorreu outras vezes, em outros repos, porém não houve registro").
- ADR-061 (§ Override): substância recorrente cross-projeto em ≥3 sessões nomeadas (meta-system, h3-finance-agent, este plugin).
- ADR-062 (este): 1 instância materializada + universalidade stack-agnóstica do problema declarada como classe nomeável; sem instâncias adicionais nomeadas.

Aceita-se o Override mais frágil porque: (i) **critério 2 (fronteira doutrinal borrada) endossa diretamente** — categoria "qualidade algorítmica de prompts" é singular e ortogonal aos 5 reviewers existentes, modelar essa fronteira distingue conceitos que se confundiriam sem ela; (ii) custo de codificação prematura é deprecação reversível (gatilho 6 meses no § Gatilhos); (iii) custo de não-codificar é re-construir o reviewer em cada sessão de prompt agentic. **Peso primário recai sobre critério 2** (fronteira), não sobre critério 1 (recorrência) — a substância da decisão não depende da analogia com ADR-057/-061, ainda que o registro de Override siga o pattern desses precedentes.

[ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) admission policy aplica via "pattern emergente" satisfeito retroativamente por declaração informada. Este ADR registra o Override explicitamente para auditoria futura; gatilho de revisão concreto (§ Gatilhos) testa empiricamente se foi prematuro.

## Consequências

### Benefícios

- Cobre eixo prompt-quality empiricamente recorrente — fecha gap real que vinha como fricção repetida (debug de prompt agentic é caro pós-fato).
- Fronteira nítida entre os 6 reviewers; cada single-axis preservado.
- Default mais-específico-vence reduz necessidade de anotação explícita em PRs canonical (review automatizado nos paths certos sem dependência de memória do operador para anotar).
- Override registrado com gatilho concreto — drift detectado se override foi prematuro.

### Trade-offs

- **+1 agent no inventário** (5 → 6 reviewers). Custo de manutenção marginal; paralelo aos demais.
- **Custo de tokens em PRs** que tocam paths do escopo v1. Em SKILL.md/agents/*.md, prompt-reviewer adiciona invocação de subagent ao gate de revisão por bloco em `/run-plan`. Mitigação: escopo restrito a paths nomeados (não dispara em README/ADRs/CLAUDE.md/philosophy.md).
- **Override do critério N=3 cria precedent.** Operadores futuros podem invocar o pattern ("já vi N vezes, codificar override") sem registrar instâncias. Mitigação: gatilho de revisão concreto (paralelo a ADR-057/-061). Em categoria doutrinal específica de Override N=3 (codificação de abstração estrutural antes do threshold), este ADR é a **3ª aplicação consecutiva** no toolkit: ADR-057 (2026-06-10) → ADR-061 (2026-06-12) → ADR-062 (2026-06-13). Cadência inferior a 4 dias entre instâncias é sinal forte para acelerar o gatilho #7 (codificar Override N=3 como meta-pattern em ADR sucessor) — gatilho originalmente posto em "5ª aplicação" ganha urgência se a 4ª emergir em janela curta. Note: memory `feedback_editorial_patterns_emergentes` registrava contadores **editoriais** distintos (sub-3c, decimal-retroativa, preservação seletiva) — não se somam à contagem doutrinal acima.
- **4 heurísticas seed dependem de julgamento do agente runtime** (todas semânticas, nenhuma mecânica). Análogo ao `design-reviewer` (julgamento de "abstração prematura" também semântico). Aceito — agentic by nature.

### Limitações

- **Não cobre strings de prompt em código** (`.py`, `.ts` etc.). Escopo v2; reabre via gatilho.
- **Não cobre prompts dinâmicos / templated** (gerados em runtime). Escopo futuro; não materialização clara hoje.
- **Não cobre análise de "qualidade do conteúdo do prompt"** (e.g., "este prompt deveria ter outra heurística") — fronteira distinta, é trabalho de `design-reviewer` se houver decisão estrutural; rebatido nas Alternativas (c).

### Mitigações

- **Gatilho de revisão concreto** (6 meses pós-shipping) cobre Override; gate de under-use/over-correção paralelo aos precedentes.
- **Default mais-específico-vence é hierárquico, não exclusivo** — operador pode forçar `{reviewer: doc}` ou `{reviewer: prompt}` em qualquer bloco. Sem lock-in.
- **Skill review e plan body são lugares dogfooded** — o próprio plugin se beneficia da revisão em SKILL.md e docs/plans/*.md; cobertura de dogfood acelera detecção de drift.

## Alternativas consideradas

### (a) Não codificar — manter raw-chat / ad hoc per ADR-036

Pattern análogo a ADR-036 (brainstorm intencionalmente não-codificado). Operador continua avaliando prompts manualmente em raw-chat com Claude quando sente necessidade; sem agent dedicado.

Descartada: operador articulou explicitamente o gap como classe nomeável e requisitou Override do critério N=3, contrário ao status quo refinado de ADR-036. ADR-036 critério "evidência empírica fraca" não aplica — declaração informada do operador + 1 instância materializada + universalidade stack-agnóstica do problema satisfazem Override paralelo a ADR-057/-061. Raw-chat tem alta latência de feedback em prompts agentic (debug pós-fato em sessão diferente); agent automatizado em paths nomeados reduz latência empiricamente.

### (b) Absorver em `code-reviewer` como sub-rubrica

Adicionar nova subseção em `agents/code-reviewer.md` ("Prompts markdown — passos conflitantes/vagos/ambíguos/contraditórios").

Descartada: viola fronteira do `code-reviewer` (rubrica YAGNI/anti-padrão em diff de código pós-fato; eixo sintático de linguagem de programação). Prompt markdown é eixo distinto — instrução-ao-agente, semântica algorítmica, não código sintático. Mistura de eixos no mesmo reviewer borra a fronteira que CLAUDE.md "Reviewer/skill report idioma" + ADR-050 § Decisão (a) "Single-reviewer é o caso normal" estabelecem. Code-reviewer carrega rubrica universal YAGNI no diff (per CLAUDE.md); adicionar eixo prompt-only acopla rubricas que devem permanecer disjuntas.

### (c) Absorver em `design-reviewer` como sub-rubrica

Adicionar nova subseção em `agents/design-reviewer.md` ("Inconsistências algorítmicas no plano").

Descartada: viola fronteira do `design-reviewer` (decisão estrutural pré-fato em documento — plano/ADR). Prompt-reviewer atua sobre instrução-ao-agente que já está escrita (SKILL.md/agents/*.md/plan body pós-escrita); é pós-fato no diff, não pré-fato em proposta. Os escopos só se sobrepõem temporariamente quando design-reviewer roda em ADR draft que codifica decisão sobre prompts — caso edge, não justifica fusão.

### (d) Skill em vez de agent

Criar `/prompt-review` skill operator-initiated em vez de agent auto-dispatchable.

Descartada: substância do prompt-reviewer é review pós-fato em PR, pattern canonical de agent (paralelo aos 5 existentes). Skill seria menos ergonômica (operador precisaria invocar manualmente em vez de `/run-plan` dispatchar automaticamente por path-based default); perde a propriedade de "review canonical em paths nomeados sem dependência de memória do operador". Categoria semântica é "reviewer" (eixo + dispatch automático), não "skill" (ação operator-initiated, novo artefato).

### (e) Esperar ≥3 instâncias ad hoc antes de codificar

Defer codificação até Override do critério N=3 não ser necessário; coletar 2 instâncias adicionais ad hoc em sessões futuras.

Descartada: paralelo direto ao descarte de Alt (c) em ADR-057. Operador aceita débito empírico explícito; pattern é estável e nomeável; categoria é nova (não risk de over-fitting em micro-padrão); cost de não-codificar é re-construir o reviewer do zero em cada sessão que toca prompt agentic do plugin. Gatilho de revisão concreto testa over-correção em 6 meses (paralelo a ADR-057/-061).

### (f) Incubação local no `h3-finance-agent` antes de promoção ao toolkit

Criar `prompt-reviewer` como agent local do `h3-finance-agent` primeiro (no diretório `.claude/agents/` do projeto consumer), validar empiricamente que cobre o gap em ≥2-3 instâncias cross-projeto, e promover ao toolkit quando recorrência materializar. Pattern canonical do toolkit per ADR-008 do meta-system ("homing arquitetural por necessidade"), citado em ADR-061 linha 20 como precedente: "necessidade universal stack-agnóstica → toolkit universal" exige verificação cross-projeto antes da promoção.

Descartada: a bifurcação canonical/incubação foi nomeada no BACKLOG original ("Decisão de promoção direta (vs incubação local no h3-finance-agent)") e resolvida pelo operador no ato do `/triage` upstream com declaração informada de universalidade stack-agnóstica suficiente — incubação seria cerimônia para coletar instâncias que o operador já declara existir, ao custo de re-implementação na promoção (agent local + wiring local + re-write canonical + edits idempotentes). Override do critério N=3 cobre o risco de promoção prematura via gatilho de revisão #1 (≤2 invocações em 6 meses → deprecação reversível); aceita-se o débito empírico explicitamente. Pattern paralelo a ADR-057/-061 cuja substância também não passou por incubação local.

## Gatilhos de revisão

1. **Over-correção do Override N=3** (gatilho primário) — em **6 meses pós-shipping**, `prompt-reviewer` invocado ≤2× pelo `/run-plan` em blocos do escopo v1 OR findings inúteis em ≥50% das invocações reais. Sinal de codificação precoce. Ação: ADR sucessor deprecia agent + recupera `doc-reviewer` como default para os paths nomeados; reverte para pattern ADR-036 status quo refinado (raw-chat para revisão ad hoc de prompts). Pattern de gatilho composto idêntico a ADR-057 § Gatilhos e ADR-061 § Gatilhos.

2. **Escopo v2 (strings de prompt em código) reabre** — ≥3 instâncias ad hoc registradas em sessões futuras onde operador quer aplicar `prompt-reviewer` em código (`.py`, `.ts`, etc.). Reabre escopo § Decisão § Escopo v1 do auto-trigger.

3. **Drift entre `prompt-reviewer` e `doc-reviewer`** — ≥2 PRs onde operator não consegue decidir qual aplicar (ou ambos disparam com findings contraditórios). Reabrir fronteira de paths em § Pattern de dispatch.

3.5. **Drift entre `prompt-reviewer` e `design-reviewer` em `docs/plans/*.md`** — ≥2 instâncias de findings contraditórios sobre o mesmo plan body (design-reviewer aprovou estrutura; prompt-reviewer flaga ambiguidade na mesma estrutura, ou vice-versa). Sinal de fronteira mal calibrada entre "decisão estrutural pré-fato" (design-reviewer) e "qualidade algorítmica da instrução" (prompt-reviewer) sobre o mesmo artefato. Reabrir § Decisão § Fronteira prompt-reviewer ↔ design-reviewer; alternativa concreta: remover `docs/plans/*.md` do escopo v1 (rebut da bifurcação não-nomeada no § Alternativas atual).

4. **Heurística sub-utilizada** — alguma das 4 heurísticas seed (conflitantes/vagos/ambíguos/contraditórios) com 0 findings em 6 meses. Heurística calibrada errado ou redundante; remover ou refinar.

5. **Falsos positivos sistemáticos de uma heurística** — operador rejeita 5+ findings consecutivos da mesma categoria. Heurística com threshold mal-calibrado; ajustar critério.

6. **Escopo v1 expandido por dor** — paths fora do escopo v1 (e.g., `docs/procedures/*.md`) acumulam ≥3 instâncias onde operator quer `prompt-reviewer` aplicado. Reabre § Decisão § Escopo v1.

7. **Outro pattern editorial análogo de over-correção emerge** — 5ª aplicação ad hoc do pattern "override do critério N=3 com cenário concreto de reversão" (após ADR-057/-061/-062 + sub-3c/decimal-retroativa/preservação seletiva counters de memory `feedback_editorial_patterns_emergentes`) — reabrir o próprio Override como meta-pattern para codificação.

8. **Reviewer canon expands** — 7º reviewer proposto. Reavaliar singularidade do escopo v1 do `prompt-reviewer` vs o novo escopo proposto.

## Auto-aplicação

Este ADR é ele próprio decisão doutrinal estrutural — codifica novo agent paralelo aos 5 shippados + pattern de dispatch refinado + Override do critério N=3 registrado.

### per ADR-034 (critério adendo-vs-novo-ADR)

- **Cond 1 (decisão estrutural sem ancestral direto):** **NÃO aplica isoladamente** — categoria de reviewer tem ancestral foundational em ADR-009 (design-reviewer foundational) e ancestral pattern em ADR-057/-061 (override do critério N=3).
- **Cond 2 (substitui ADR ancestral):** **NÃO aplica** — ADR-009/-057/-061 permanecem vigentes.
- **Cond 3 (codifica restrição externa):** **NÃO aplica** — sem restrição regulatória/contratual.
- **Cond 4 (introduz categoria nova):** **APLICA** — categoria "reviewer de qualidade algorítmica de prompts markdown" é nova; sem precedente nos 5 reviewers existentes.
- **Cond 5 (sucessor parcial):** **APLICA** — sucessor parcial **lateral** de ADR-057/-061 (paralelismo de Override do critério N=3, mesmo pattern de declaração informada + gatilho concreto).

Cond 4 + cond 5 simultâneas aplicam — pattern editorial estabelecido por ADR-053/-054/-061 (sucessor parcial introduzindo categoria nova).

### per ADR-043 § Ockham operacionalizado

- **Critério 2 (fronteira doutrinal borrada):** **APLICA solidamente** — peso primário desta decisão. Categoria "reviewer de qualidade algorítmica de prompts markdown" é nova; modelar essa fronteira distingue conceitos que se confundiriam sem ela (vide rebut Alternativas b+c).
- **Critério 3 (contradição/refinamento de doutrina existente):** **APLICA** — refina inventário canonical de reviewers em CLAUDE.md (5→6).
- **Critério 1 (incidente recorrente):** **PARCIAL** — 1 instância materializada + declaração informada do operador; Override mais frágil que precedentes ADR-057/-061 (vide § Override do critério N=3 — Reconhecimento de assimetria).
- **Critério 4 (≥3 pattern emergente ad hoc):** **FALHA** materialização explícita — Override registrado para auditoria futura via § Gatilhos.

Critério 2 endossa diretamente como peso primário; critério 3 reforça; critério 1 cobre via Override registrado.
