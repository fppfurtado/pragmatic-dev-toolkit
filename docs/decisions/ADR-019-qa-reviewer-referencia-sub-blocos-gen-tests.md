# ADR-019: qa-reviewer referencia sub-blocos canonical de /gen-tests

**Data:** 2026-05-12
**Status:** Aceito

## Origem

- **Decisão base:** [ADR-008](ADR-008-skills-geradoras-stack-agnosticas.md) codificou que idioms de stack vivem em sub-blocos por stack dentro de `skills/gen-tests/SKILL.md` (single source of truth). Não tocou a relação com agents reviewers.
- **Investigação:** revisão da relação `qa-reviewer` ↔ `/gen-tests` durante `/triage` em 2026-05-12 expôs duplicação parcial (regras de mock-vs-real fixadas em dois lugares) e ausência de cross-reference canonical entre os componentes.

## Contexto

`agents/qa-reviewer.md` codifica regras em dois níveis:

1. **Cross-stack genéricas** — caminho feliz, invariantes documentadas pelo `ubiquitous_language`, separação unit vs integration, anti-patterns de mocking (testing mock behavior, test-only methods, mocking without understanding). Aplicam-se a qualquer stack.
2. **Idiom-adjacentes pontuais** — "HTTP externo: usar a ferramenta de mock idiomática da stack, não bibliotecas genéricas tipo `unittest.mock`"; "Camada de persistência mockada em integration → bug". Genéricas na forma, mas o conteúdo concreto vive em `skills/gen-tests/SKILL.md` sub-bloco Python (`respx`, `tmp_path`) e Java (Mockito, H2/Testcontainers).

Sem cross-reference declarado:

- **Drift garantido pelo gatilho de ADR-008.** Stack nova adicionada via sub-bloco em `/gen-tests` (gatilho explícito do ADR-008) não atualiza automaticamente o eixo de revisão do `qa-reviewer`. Operador precisa lembrar de tocar dois arquivos para a nova stack ter cobertura completa do ciclo gerar→revisar.
- **Duplicação parcial.** "Não mockar SQLite — usar `tmp_path`" mora em `gen-tests/SKILL.md:53` (sub-bloco Python, "Stack assumida") e novamente em `:99` ("O que NÃO fazer (Python)"). `qa-reviewer.md:35` diz "Camada de persistência mockada em integration → bug" — mesma regra, forma genérica vs idiomática; quem atualiza um sem o outro causa drift silencioso.
- **Pattern existente em `docs/philosophy.md:75`** já estabelece pipeline análogo para vocabulário ubíquo: `ubiquitous_language` → `/triage` grava `**Termos ubíquos tocados:**` → `/run-plan` repassa ao reviewer → `code-reviewer` valida no diff. Reviewer consome de fonte canonical, não duplica. Padrão não foi replicado para idioms de teste.

Pressão paralela: durante a mesma `/triage` foi avaliado **delegar a criação de teste a `/gen-tests` durante `/run-plan`** (dispatch skill→skill no loop de execução). Descartado por motivos enumerados em "Alternativas" abaixo. Este ADR registra o caminho aprovado (cross-reference do reviewer, não dispatch da skill geradora).

## Decisão

**`qa-reviewer` cita os sub-blocos por stack de `skills/gen-tests/SKILL.md` como fonte canonical de idioms para a stack detectada.** Idioms permanecem fixados no SKILL.md de `/gen-tests` (single source of truth, per ADR-008); o reviewer referencia, não duplica.

Mecânica:

- Stack detectada pelo `qa-reviewer` segue o mesmo critério de marker já implícito no agent ("infere a categoria pelo marker") e formalizado em ADR-008 para `/gen-tests` — `pyproject.toml` → Python, `pom.xml`/`build.gradle*` → JVM, etc.
- Texto do reviewer ganha um parágrafo curto apontando: "Idioms canonical por stack vivem em `skills/gen-tests/SKILL.md` sub-bloco da stack detectada; usar como referência da regra de mock-vs-real, ferramenta HTTP idiomática, layout unit/integration".
- **Carregamento lazy.** Reviewer faz `Read` do sub-bloco da stack detectada como input adicional **sob demanda na invocação** (não em frontmatter; só quando há diff de teste a revisar). Diff sem mudança em paths de teste → sub-bloco não é lido.
- **Stack sem sub-bloco em `/gen-tests`.** Reviewer prossegue com regras conceituais cross-stack e cita a ausência no relatório (não bloqueia revisão; sinaliza gap para o operador considerar contribuir sub-bloco).
- Reviewer mantém o eixo conceitual (caminho feliz, invariantes, edge cases, anti-patterns de mocking, mock-vs-real). Não absorve a tabela de idioms; importa por referência.

Escopo limitado a `qa-reviewer` ↔ `/gen-tests`. Generalização para outros pares reviewer↔skill (hipotéticos) fica como gatilho de revisão — single data point hoje, evitar over-abstraction (alinhado a YAGNI da philosophy.md).

**Não-dispatch.** `/run-plan` continua não delegando criação de teste a `/gen-tests`. O ponto de contato reviewer↔skill é leitura por referência durante revisão pré-PR, não execução durante o loop de implementação.

## Consequências

### Benefícios

- **Single source of truth**: stack nova adicionada em `/gen-tests` (gatilho do ADR-008) ganha automaticamente cobertura do eixo de revisão. Operador toca um arquivo, ciclo gerar→revisar fica completo.
- **Reviewer compacto**: `qa-reviewer.md` não cresce com cada stack adicional — só carrega regras conceituais cross-stack + ponteiro à fonte canonical.
- **Convergência conceitual com o pipeline de domínio** (`philosophy.md:75`): ambos consomem fonte canonical em vez de duplicar. Mecânica é distinta — domínio usa carrier dinâmico no plano (`**Termos ubíquos tocados:**` gravado por `/triage`, repassado por `/run-plan` ao reviewer); idioms de teste usam leitura direta do sub-bloco da stack detectada no momento da invocação. Convergem no princípio (fonte canonical única), divergem na forma (runtime via plano vs lookup estático).
- **Evita coupling de execução**: dispatch `/run-plan` → `/gen-tests` foi rejeitado (ver Alternativas) — cross-reference no reviewer cobre o gap doutrinário sem introduzir o coupling rejeitado.

### Trade-offs

- **Reviewer carrega idioms via leitura durante revisão** — input adicional ao invocar `qa-reviewer` (sub-bloco da stack lido sob demanda). Mitigação: sub-blocos curtos por design (ADR-008 trade-off já assumido); só o sub-bloco da stack detectada é necessário, não todos.
- **Drift se sub-bloco for editado sem revisar texto do reviewer** — duas formas de drift continuam possíveis: (a) sub-bloco ganha regra nova que o reviewer não cita; (b) reviewer mantém regra solta que conflita com o sub-bloco. Mitigação: ambos são editorialmente disciplinados (Critério editorial em CLAUDE.md); gatilhos de revisão deste ADR cobrem desvio recorrente.

## Alternativas consideradas

### Duplicar idioms em `qa-reviewer` (status quo parcial)

Manter regras tipo "Não mockar SQLite" tanto em `qa-reviewer.md` quanto em `gen-tests/SKILL.md`. Descartado: drift garantido pelo gatilho de revisão de ADR-008 (sub-bloco novo de stack); aceitar duplicação é apostar contra o mecanismo já decidido.

### Delegar criação de teste a `/gen-tests` durante `/run-plan` (dispatch)

`/run-plan` invocar `/gen-tests` no bloco `{reviewer: qa}` para gerar testes em vez de o agente implementador escrever inline. Descartado por quatro motivos concretos:

1. **Mismatch de argumentos**: `/gen-tests` consome alvo discreto (`src/.../módulo.py`, `Classe::método`, descrição livre); bloco do plano é `## Arquivos a alterar` com bullets — tradução bloco→alvo é frágil sem mudar schema do plano.
2. **Escopo do bloco**: blocos `{reviewer: qa}` frequentemente misturam prod + teste no mesmo arquivo lógico ("implementar parser e seus testes"); `/gen-tests` só gera teste, sobra metade do bloco.
3. **Fragmentação da continuidade**: `/gen-tests` tem cutucadas internas (`Stack` em fallback, `Fixture` para conftest, `Mock` para mock-vs-real); dispatch dentro do loop §2 do `/run-plan` injeta esses prompts no meio da execução, violando o princípio de caminhos assistidos sem fragmentação.
4. **Contexto morre no dispatch**: agente do bloco tem em working memory o que acabou de implementar, invariantes carregadas, design_notes citados; `/gen-tests` começa frio e re-deriva, com qualidade inferior.

### Sub-bloco "Reviewer rules" em `gen-tests/SKILL.md` espelhando idioms

Adicionar seção em `gen-tests/SKILL.md` listando regras de revisão por stack para o `qa-reviewer` consumir. Descartado: cresce `gen-tests/SKILL.md` sem ganho — reviewer já tem o eixo conceitual certo; o que falta é apontar para a fonte canonical, não criar uma segunda fonte.

### Generalizar regras pontuais a regras conceituais (sem cross-reference)

Manter `qa-reviewer` puramente conceitual — eliminar regras idiom-adjacentes ("não mockar SQLite", "usar ferramenta HTTP idiomática") e deixar só as cross-stack ("persistência mockada em integration → bug"; "usar ferramenta idiomática da stack"). Eliminaria duplicação **e** a necessidade de cross-reference: reviewer fica conceitual, skill fica idiomática, sem ponteiro a manter alinhado. Descartado: regras conceituais sozinhas perdem acionabilidade — "usar a ferramenta idiomática da stack" não diz ao reviewer **qual** ferramenta procurar no diff (`respx` vs `unittest.mock` em Python; `WireMock`/`MockWebServer` vs `unittest.mock` em Java); o reviewer precisa do nome concreto para detectar violação. Cross-reference preserva acionabilidade sem duplicar — eis o ponto.

### Editorial-only (sem ADR), edit direto em `qa-reviewer.md`

Adicionar cross-reference no `qa-reviewer.md` sem registrar ADR. Descartado: mudança altera **relação doutrinária entre dois componentes do plugin** (reviewer ↔ skill geradora), refina pattern implícito de `philosophy.md:75` para outro eixo. Critério editorial do plugin (memory `feedback_adr_threshold_doctrine`) leva mudança de doutrina ao default ADR mesmo quando a implementação é trivial — ADR documenta o porquê, ancora revisão futura, **e serve de referência citável** quando `code-reviewer` (ou contribuidor) precisar rebater duplicação reintroduzida em `qa-reviewer.md` no futuro ("essa regra mora em `/gen-tests`, ver ADR-019").

## Gatilhos de revisão

- **Surge segundo par reviewer↔skill geradora** (hipoteticamente: `doc-reviewer` ↔ skill de geração de doc; `security-reviewer` ↔ skill de scaffolding de segurança) → reabrir para considerar generalização da doutrina ("reviewer agents podem importar canonical conventions de skills geradoras correspondentes") em vez de manter rule específico por par.
- **Sub-bloco de stack em `/gen-tests` ultrapassa volume que cabe carregar como contexto inline em revisão** (≥500 linhas em um único sub-bloco) → reabrir formato de cross-reference (excerto seletivo vs ponteiro integral).
- **`qa-reviewer` detecta gap recorrente em stack X enquanto sub-bloco X existe e codifica a regra** → sinal de que o cross-reference não está sendo eficaz; reabrir mecanismo de transferência.
- **Drift concreto observado**: PR onde sub-bloco e reviewer divergem na regra → sinal de que disciplina editorial não basta; considerar lint ou checagem mecânica.
