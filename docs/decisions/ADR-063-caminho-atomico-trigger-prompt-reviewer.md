# ADR-063: Caminho atômico em path-set com trigger prompt-reviewer pré-commit

**Data:** 2026-06-13
**Status:** Proposto

## Origem

- **Investigação:** sessão CC 2026-06-13 — dogfood recursive de `@prompt-reviewer` sobre `skills/triage/SKILL.md` gerou 3 iterações sucessivas (commits `d24cd1f` + `f9e3814` + `9f78aa7`) com 6 findings substantivos totais; gap de wiring evidenciado durante explicação da fronteira auto-trigger vs. manual invoke (mensagem do operador "A invocação de @agents/prompt-reviewer.md foi incluída no workflow do plugin ou roda apenas manualmente?").
- **Decisão base:** Sucessor parcial de [ADR-053](ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (b) — refina a escolha original de NÃO disparar reviewer em caminho-atômico ("cirúrgico") expandindo cobertura para o sub-conjunto path-set narrow algorithmic-bearing onde o custo empírico da omissão supera o overhead do trigger. Estende mecanismo de auto-trigger gateado por path-set narrow de [ADR-062](ADR-062-criar-subagent-prompt-reviewer.md) § Pattern de dispatch para 2ª trajetória (`/triage` step 5 caminho-atômico) além da 1ª (`/run-plan` §2 item 3 per-bloco).
- **Substrato categórico:** [ADR-009](ADR-009-revisor-design-pre-fato.md) § Escopo da inversão — foundational do regime reviewer document-level pré-commit. `prompt-reviewer` instancia o caso "eixo independente de doutrina escrita, document-level" que ADR-009 explicitamente deixou em aberto; ADR-063 codifica a 2ª trajetória dessa instanciação.

## Contexto

Edit cirúrgico atômico via `/triage` em arquivos do path-set narrow — pattern operacional usado em refinamentos pequenos de SKILL.md/agent.md/plan body sem produzir plano novo — **escapa todos os auto-triggers de reviewers**:

- `@design-reviewer` dispara apenas em `/triage` step 5 caminho-com-plano (linhas 162-167 do `skills/triage/SKILL.md`).
- `@prompt-reviewer` dispara apenas dentro de `/run-plan` §2 item 3 per-bloco baseado nos paths em `## Arquivos a alterar` de um plano.

`/triage` step 3 tabela canonical (5 caminhos: linha BACKLOG / plano / ADR / domain / design) não nomeia caminho-atômico explicitamente — operador o trata implicitamente como variante da "linha BACKLOG" ou da "atualização cirúrgica de domain/design" para refinamentos pequenos. Pré-fato esse caminho escorrega para commit sem scrutiny algorítmica.

Sessão atual demonstrou empiricamente que esse caminho gera substância flaggable: 6 findings reais (ambiguidades, antecedentes vagos, contradições com state declarado em ADRs/CLAUDE.md, dispatch ambíguo) emergiram em 3 iterações via manual invoke deliberado. N=1 sessão dogfood-recursive (não evidência de uso real) com volume substantivo suficiente para sinalizar gap conceitual.

## Decisão

**Hoje, caminho-atômico em path-set narrow via `/triage` (variante dos caminhos 1-5 da tabela do step 3) escapa todos os auto-triggers de reviewers** — `@prompt-reviewer` só dispara em `/run-plan` per-bloco (ADR-062), e `@design-reviewer` só em caminho-com-plano (ADR-053 § Decisão (b)). **Pós-ADR-063:** caminho-atômico em path-set narrow é categoria explícita da tabela do step 3 que dispara `@prompt-reviewer` automaticamente pré-commit no step 5.

Operacionalmente:

1. Adicionar **6ª linha** na tabela do `## 3. Decidir o artefato` do `skills/triage/SKILL.md` nomeando o caminho **"Edit atômico em SKILL/agent/plano"** com escopo path-set narrow (`agents/*.md` ∪ `skills/**/SKILL.md` ∪ `docs/plans/*.md`).

2. **Critério mecânico de discriminação da 6ª linha** vs. linhas 4-5 (domain/design) da tabela atual: linha 6 dispara quando todos os 3 critérios aplicam — (i) paths editados ⊆ path-set narrow (`agents/*.md` ∪ `skills/**/SKILL.md` ∪ `docs/plans/*.md`); (ii) edit cirúrgico (1-N edits localizados sem multi-fase nem decisão estrutural); (iii) substância **não** captura por linhas 4-5 (não é update de `docs/domain.md` nem de `docs/design.md` — paths literais). Edits que tocam domain/design literalmente preservam linhas 4-5; edits no path-set narrow caem em linha 6.

   **Path misto (path-set narrow ∪ domain/design no mesmo `/triage`):** predicado ⊆-strict prevalece → linha 6 **não** dispara; substância cai em linhas 4-5; trigger automático não roda. Operador que queira scrutiny algorítmica de SKILL/agent tocada no cross-fronteira invoca `@prompt-reviewer` manualmente. Justificativa: cross-fronteira é caso de borda; auto-trigger em cross-fronteira força reviewer document-level em arquivos não-prompt (domain/design) — viola escopo de [ADR-009](ADR-009-revisor-design-pre-fato.md) § Escopo da inversão.

3. `/triage` step 5 ganha **parágrafo de Revisão pré-commit (caminho-atômico em path-set narrow)** análogo ao parágrafo da Revisão pré-commit (caminho-com-plano) que já existe (linhas 162-167): invoca `@prompt-reviewer` apontando para arquivos editados antes do commit; aplica critério de [ADR-053](ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (c) para cada finding (cutucar via `AskUserQuestion` se satisfaz ≥1 das 3 condições; absorber pré-commit caminho-único). Cláusula default-conservadora preserva ("dúvida na classificação → cutucar").

4. **Fit semântico das 3 condições de ADR-053 sobre findings do `prompt-reviewer`** (calibradas originalmente para shape do `design-reviewer`): mapeamento por analogia explícito — condição 1 (≥2 alternativas legítimas competindo) ≈ heurística "passo ambíguo" do [ADR-062](ADR-062-criar-subagent-prompt-reviewer.md) § 4 heurísticas seed; condição 2 (contradiz decisão documentada em ADR/`philosophy.md`/`CLAUDE.md`) ≈ heurística "passo contraditório em estado global"; condição 3 (exige contexto fora do diff/plano/ADR) raramente aplica a findings algorítmicos. Refinamento futuro do mapeamento via gatilho de revisão se imprecisão materializar.

Razões:

- **Cobertura conceitual:** edit em files do path-set é categoria semântica distinta — algoritmo-bearing (instrução ao agente) vs. domain/design (documentação de domínio) vs. backlog (registro). `prompt-reviewer` é o reviewer especializado para algorithmic consistency em prompts; estender trigger preserva o invariante de que path-set narrow gateia consistentemente esse reviewer (mesmo gate que ADR-062 § Pattern de dispatch usa em `/run-plan`).
- **Discoverability:** caminho explícito na tabela torna o trigger visível para operador no ponto de decisão (step 3) — não-trivial vs. trigger implícito acoplado ao step 5.
- **Coerência cross-skill + sucessor parcial declarado:** `prompt-reviewer` ganha 2ª trajetória de auto-trigger (`/run-plan` per-bloco + `/triage` caminho-atômico) gateadas pelo mesmo path-set narrow; assimetria com `design-reviewer` (que tem 1 trajetória só, caminho-com-plano) é principled — ADR-053 § Decisão (b) deliberadamente deixou caminho-atômico (cirúrgico) sem reviewer pré-fato; ADR-063 refina aquela escolha para o **sub-conjunto path-set narrow** algorithmic-bearing onde o custo empírico da omissão (6 findings substantivos em 3 iterações) supera o overhead do trigger. Caminho-atômico em outros paths (`docs/domain.md`, `docs/design.md`, paths não-prompt) preserva o regime ADR-053 (sem reviewer pré-fato).

## Consequências

### Benefícios

- Cobertura de scrutiny algorítmica em refinamentos pequenos de SKILL.md/agent.md/plan body, mesmo em caminho-sem-plano.
- Pattern uniforme: path-set narrow é o gate consistente para `prompt-reviewer` cross-skill.
- Sinalização explícita do caminho-atômico na tabela do step 3 — operador vê o trigger no ponto de decisão.

### Trade-offs

- Custo de tokens em refinamento trivial (typo em SKILL.md, reordenação editorial sem substância algorítmica) — reviewer roda mesmo nesses casos.
- Risco de trigger fadigoso se edits em path-set virarem pattern frequente; mitigado pela cláusula default-conservadora de ADR-053 § Decisão (c) (absorção pré-commit em finding caminho-único trivial).
- Operador editor que invoca `/triage` para registrar linha de backlog mas que tangencialmente toca SKILL.md ad-hoc tem trigger disparado.

### Limitações

- Escopo restrito ao path-set v1 de ADR-062 (`agents/*.md`/`skills/**/SKILL.md`/`docs/plans/*.md`). Outros files prompt-bearing (templates/, hooks/) não cobertos; gatilho de revisão de ADR-062 § Escopo v1 governa expansão futura.
- Override mechanism (caminho-atômico que ignora trigger por decisão do operador) não codificado nesta v1 — depende de incidente concreto de trigger fadigoso para materializar.

### Mitigações

- Cláusula default-conservadora de ADR-053 § Decisão (c) ("dúvida na classificação → cutucar") preserva controle do operador sobre absorção vs. cutucada.
- Mirror no commit message (per ADR-053 § Decisão (d)) preserva auditoria pós-fato de findings absorvidos.

## Override do critério N=3

Per [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § Ockham operacionalizado #4 (N=3 instâncias antes de codificar), substância de ADR-063 carrega Override análogo a precedentes ADR-057, ADR-061 e ADR-062 (todos com gatilho de revisão concreto registrado). Esta é a **4ª aplicação consecutiva** do Override em < 4 dias — material que acelera o gatilho #7 de ADR-062 ("5ª aplicação ad hoc do pattern... reabrir o próprio Override como meta-pattern para codificação").

Calibração da fragilidade empírica:

- **ADR-057, ADR-061:** ≥1 incidente real registrado motivando a categoria.
- **ADR-062:** 1 instância materializada em projeto consumer (smoke-test pós-shipping).
- **ADR-063:** N=1 sessão dogfood-recursive (não uso real) — evidência mais frágil que precedentes.

Override aceito aqui pelo peso primário de **coerência cross-skill com ADR-062** (não pela recorrência empírica): o invariante "path-set narrow gateia `prompt-reviewer` automaticamente" cobre 1 trajetória (`/run-plan`) pós-ADR-062 mas escapa a outra (`/triage` caminho-atômico) que é categoricamente análoga. ADR-063 fecha a assimetria. Gatilho de revisão #1 cobre over-correção (≥2 sessões reais com flag trivial → reabrir).

## Auto-aplicação

Aplicação dos critérios de admissão sobre o próprio ADR-063:

- **[ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) § critério mecânico para novo ADR vs. adendo:**
  - Cond 4 (introduz categoria nova): **NÃO aplica** — categoria "auto-trigger de reviewer gateado por path-set narrow" já existe via ADR-062.
  - Cond 5 (sucessor parcial): **APLICA** — sucessor parcial primário de ADR-053 § Decisão (b) refinando o tratamento de caminho-atômico em path-set narrow; sucessor parcial lateral de ADR-062 estendendo pattern de dispatch para 2ª trajetória.
  - ≥1 cond aplica → novo ADR (não adendo).

- **ADR-043 § Ockham operacionalizado:**
  - Critério 3 (refinamento de doutrina existente): **APLICA** — refina ADR-053 + estende ADR-062.
  - Critério 1 (cenário concreto de reversão): **APLICA parcial** via gatilho #1 da § Gatilhos.
  - Critério 4 (pattern emergente ≥3 aplicações ad hoc): **NÃO APLICA** — N=1 sessão dogfood; Override registrado em § Override do critério N=3.

- **[ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) § Decisão parte 2 (filtro de admissão):** passou no filtro mecânico de 3 saídas — categoria nova de caminho + trigger; cenário de reversão nomeável (gatilho #1); sucessor parcial de ADR-053. Operador escolheu `ADR` em cutucada explícita do step 3.5 do `/new-adr`.

**Fragilidade epistêmica reconhecida:** Override do critério N=3 mais frágil que ADR-057/-061 (ambos ≥1 incidente real) e que ADR-062 (1 instância materializada em projeto distinto). ADR-063 aceita o débito empírico explicitamente — gatilho #1 da § Gatilhos é o teste empírico forward; se materializa over-correção em ≤6 meses, depreciar para CLAUDE.md como variante operacional ou reverter via ADR sucessor.

## Alternativas consideradas

### (α) Status quo — manual @prompt-reviewer permanece pattern

Manter `@prompt-reviewer` como manual invoke para caminho-atômico em path-set. Descartado: N=1 sessão demonstrou substância flaggable em volume relevante (6 findings em 3 iterações); ergonomic friction de manual invoke desincentiva uso recorrente — gap fica permanente. Cobertura assimétrica vs. ADR-062 dispatch dentro de `/run-plan` é inconsistente conceitualmente.

### (β) Estender trigger sem nomear caminho na tabela do step 3

Adicionar trigger em `/triage` step 5 sem 6ª linha na tabela. Descartado: torna o trigger implícito (operador não vê no ponto de decisão quando o trigger dispara). Contradiz princípio de discoverability + estado explícito + pattern atual da tabela (rows 1-5 cada uma carrega seu próprio mecanismo).

### (δ) ADR documentando NÃO-cobertura como decisão deliberada

Registrar o gap como decisão de não-ação ("caminho-atômico permanece sem auto-trigger por design"). Descartado: ADR pressupõe "X é a regra" com critério ativo; aqui o pattern empírico (6 findings em sessão dogfood) sinaliza que cobertura é mais valiosa que aceitação. Substância da sessão pesa contra a tese de "manual invoke é suficiente".

## Gatilhos de revisão

- **Trigger fadigoso em uso real:** ≥2 sessões CC reais (não dogfood) onde `@prompt-reviewer` em `/triage` caminho-atômico flagra apenas drift trivial (typo, reordenação, cosmético) sem substância algorítmica → reabrir para considerar override mechanism (anotação `{review: skip}` ou similar no commit message ou plano body).
- **Escopo v1 do path-set expandido:** se ADR-062 § Gatilhos disparar expansão (ex.: incluir `templates/`, `hooks/`) → revisar consistência cross-trigger (auto-trigger em `/triage` step 5 deve manter paridade com dispatch em `/run-plan` §2 item 3).
- **Pattern empírico forward:** 2 incidentes adicionais em uso real (não dogfood) de caminho-atômico em path-set gerando findings substantivos confirma N≥3; promove decisão de "estatisticamente estável" e pode reduzir escopo de revisão futura.
- **Fit semântico das 3 condições para `prompt-reviewer` insuficiente:** se ≥2 sessões reais mostram operador classificando errado (cutucar vs absorber) por ambiguidade do mapeamento por analogia codificado em § Decisão #4 → codificar mapeamento explicitamente ou refatorar critério.
