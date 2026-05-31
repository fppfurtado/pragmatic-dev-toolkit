# ADR-053: Alinhamento /triage e ecosistema do design-reviewer (consolidado)

**Data:** 2026-05-31
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) § Decisão parte 1 § Implementação literal — Onda I (nona) da redesign da camada doutrinal. Sétima migração cluster temático após Ondas C+D+E+F+G+H (cutucadas, modo local, reviewers/curadoria, execução/run-plan, componentes plugin, convenções editoriais).
- **Decisão base:** [ADR-052](ADR-052-codificacao-3-modos-editoriais-refinamento-consolidacao.md) — meta-pattern editorial canonical com 3 modos (a/b/c). **Primeira aplicação formal de ADR-052 com 2 modos simultaneamente:** modo (c) PRESERVAÇÃO POR CONSTRAINT MECÂNICO PURO sobre ADR-009 + modo (a) EXCLUSÃO sobre ADR-042.
- **Decisão base:** [ADR-046](ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) + [ADR-047](ADR-047-modo-local-paths-replicacao-cross-mode.md) + [ADR-048](ADR-048-free-read-design-reviewer-consolidado.md) + [ADR-049](ADR-049-execucao-run-plan-consolidado.md) + [ADR-050](ADR-050-componentes-plugin-consolidado.md) + [ADR-051](ADR-051-convencoes-editoriais-consolidado.md) — templates do pattern de migração validado em 6 ondas precedentes (F1 link rot 2 categorias; F4 cond 5 primária isolada; F9 fronteira ADR-024 procedure file; refinamento editorial 3 modos canonical).
- **Decisão base:** [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) — critério mecânico adendo vs novo ADR. **Cond 5 primária isolada** (sucessor parcial absorvendo 4 ADRs com substância preservada integralmente); cond 4 NÃO aplica (ADR-045 carrega categoria meta; ADR-053 é sétima instância de migração); cond 1 NÃO aplica (ADR-045/-046/-047/-048/-049/-050/-051/-052 ancestrais codificados); cond 2 NÃO aplica (regra central de cada ADR absorvido preservada integralmente; nenhum marcado como Substituído).
- **Decisões absorvidas:** ADR-011 (wiring automático do design-reviewer em `/triage` plan-producing + `/new-adr`; sucessor parcial de ADR-009), ADR-026 (critério mecânico de absorção de findings do design-reviewer pré-commit — 3 condições + default absorvedor; sucessor parcial de ADR-011), ADR-027 (skill `/draft-idea` para elicitação estruturada de `product_direction`/IDEA.md; alinhamento upstream de `/triage`), ADR-038 (mirror das Decisões absorvidas no plan body + consumo runtime por reviewers via `/run-plan` §2.3; sucessor parcial de ADR-026). Substância completa preservada em § Decisão (a-d).
- **Decisões preservadas vigentes fora do cluster:** [ADR-009](ADR-009-revisor-design-pre-fato.md) (revisor design pré-fato + free-read de doctrine sources — apex foundational do design-reviewer) preservado **modo (c) ADR-052** por constraint mecânico — hardcoded na always-include de ADR-048 § Decisão `[ADR-009, ADR-034, ADR-043]`. Critério mecânico verificável: `grep "ADR-009" docs/decisions/ADR-048-*.md` → match em § Decisão vigente. Análogo a ADR-034 em Onda H. ADR-042 (`/note --to` cross-project write) excluído **modo (a) ADR-052** por desalinhamento semântico do sketch — pertence ao cluster bridge/discoverability futuro junto com ADR-032, não a design-reviewer ecosystem. Análogo a ADR-039 em Onda F.
- **Plano coordenador:** `docs/plans/onda-i-migracao-cluster-alinhamento-triage.md` (este charter-execution).

## Contexto

O ecosistema do `design-reviewer` pré-fato cresceu em 4 movimentos sucessivos entre 2026-05-07 e 2026-05-26, cada um materializando refinamento empírico:

1. **ADR-009 (2026-05-07)** estabeleceu a categoria foundational: reviewers podem operar em documento pré-fato ao lado do padrão diff pós-fato; reviewer document-level cuja função inclui detecção de contradição doutrinária faz free-read em runtime de doctrine sources (`docs/decisions/*.md` + `docs/philosophy.md`) — autor do plano NÃO cura essa lista. Categoria apex preservada vigente standalone (modo (c) ADR-052 — hardcoded na always-include de ADR-048).

2. **ADR-011 (2026-05-08)** exerceu gatilho hipotético de ADR-009 ("wiring automático em /run-plan pré-loop ou /new-adr pré-commit materializa") com evidência cumulativa de dogfood deliberado: 3 invocações reais + 7 findings cumulativos (5 editoriais + 1 estrutural ADR-010 emergente). Padrão observado: todas em `/triage` que produziu plano (caminho-com-plano), antes do commit do plano. `/run-plan` pré-loop seria gate tarde (plano já commitado e pushed); `/triage` pós-plano/pré-commit é ponto natural.

3. **ADR-026 (2026-05-13)** refinou trilho operacional de ADR-011 § Decisão #1 ("operador decide aplicar"). Prática empírica nas 11 sessões pós-ADR-011 (PRs #54-#60 + commits cirúrgicos) divergiu: assistente passou a absorver findings triviais pré-commit em vez de cutucar para cada um. Análise retroativa de ~17 findings absorvidos (caminho-único, zero retrabalho) + ~4 findings cutucados (todos via Cond 1 — alternativas legítimas competindo) revelou eixo discriminante: **shape do finding** (alternativas / contradição com doutrina / contexto externo), não conteúdo nem stack.

4. **ADR-027 (2026-05-13)** materializou alinhamento upstream do pipeline: gap no toolkit entre papel `product_direction` declarado na role contract (canonical `IDEA.md`) e ausência de caminho de criação assistida — operador escrevia IDEA.md à mão ou não escrevia. Skill `/draft-idea` cobre via elicitação estruturada multi-turn (problema, persona, restrições, critérios, alternativas). Fronteira nítida com `/triage`: `/draft-idea` opera quando intenção ainda é vaga; `/triage` quando intenção já é concreta. Sugere `/triage` como próximo passo ao concluir.

5. **ADR-038 (2026-05-26)** fechou gap operacional descoberto via ROADMAP item 1: `code-reviewer` (invocado mid-execução por `/run-plan`) flaggou estrutura aprovada pelo `design-reviewer` pré-commit; sem perspicácia do agente para citar ADR-035 e cutucar, default-absorber regrediria silenciosamente decisão aprovada. Causa raiz: `code-reviewer` sem acesso ao registro das decisões absorvidas pelo design-reviewer pré-commit (commit messages só lidas por humanos, não por reviewer agent runtime). Mecanismo: mirror da seção `## design-reviewer findings absorvidos` entre commit message (preservada por ADR-026) e plan body (introduzida por ADR-038) com mecânica runtime de consumo pelos reviewers via mensageiro upstream.

Pós-Onda H da redesign (convenções editoriais consolidadas em ADR-051; gatilho de ADR-045 disparado e codificado via ADR-052), cluster alinhamento/triage é candidato natural para sétima migração — coesão semântica alta sob narrativa única "alinhamento upstream → wiring reviewer → critério de absorção → propagação runtime".

## Decisão

Consolidar substância de ADR-011 + ADR-026 + ADR-027 + ADR-038 em ADR temático único sob 4 dimensões coerentes. ADR-009 preservado vigente standalone (modo (c) ADR-052). ADR-042 excluído do cluster (modo (a) ADR-052).

### (a) Skill `/draft-idea` upstream — elicitação estruturada de `product_direction`/IDEA.md (de ADR-027)

Skill geradora do toolkit que materializa caminho de criação assistida para `IDEA.md` (papel `product_direction`).

- **Naming:** `/draft-idea` — convenção `<verb>-<artifact>` (per `CLAUDE.md` → "Plugin component naming"), alinhada ao filename canonical `IDEA.md` (paralelo a `/new-adr` ↔ `ADR-NNN.md` e `/run-plan` ↔ `<slug>.md`).
- **Escopo:** elicitação estruturada multi-turn cobrindo problema, persona/usuário, restrições, critérios de sucesso e alternativas descartadas. Skeleton-only é rejeitado — valor real da skill está na **estrutura de elicitação** (perguntas dirigidas que forçam o operador a articular bifurcações silenciosas); skeleton-only seria wrapper fino sobre `touch IDEA.md` + chat livre, sem ganho semântico.
- **Modo de operação:** probe canonical + dual.
  - `IDEA.md` ausente → modo **one-shot full** (skill conduz interview completo do zero e grava o artefato).
  - `IDEA.md` presente → modo **update seção-a-seção** via enum (`AskUserQuestion` lista as seções; operador escolhe quais revisar; skill reconduz elicitação só nessas).
- **Fronteira com `/triage`:** upstream. `/draft-idea` opera quando intenção ainda é vaga (sem problema bem-definido); `/triage` opera quando intenção já é concreta. Skill **sugere `/triage` como próximo passo** ao concluir (registro de continuidade do pipeline mental).
- **Stack-agnóstica:** sem auto-detection por marker, sem sub-blocos por stack — `IDEA.md` é produto, não código (per ADR-050 § Decisão (a) caminho dos artefatos não-código).
- **`disable-model-invocation: false`** esperado per critério mecânico de ADR-050 § Decisão (e) — blast radius local; pushes/PRs gateados upstream pelo operador; sem autoinvocação cross-turn.

Limitações específicas de `/draft-idea` consolidadas em § Limitações global (pattern editorial das 6 consolidações precedentes — § Limitações única no final).

### (b) Wiring automático do design-reviewer pré-fato em `/triage` plan-producing + `/new-adr` (de ADR-011, sucessor parcial de ADR-009)

`design-reviewer` dispara automaticamente em:

1. **`/triage` que produz plano** (caminho-com-plano, com ou sem ADR delegada), no passo 5 (antes do commit unificado). Findings reportados ao operador, que decide aplicar antes de commitar ou seguir como está. Sem cutucada de pré-execução — gate é a presença dos findings, não pergunta binária. **Não dispara** em `/triage` que fecha em linha de backlog pura, atualização cirúrgica de `docs/domain.md`/`docs/design.md`, ou ADR-only delegada sem plano (último coberto via #2 abaixo).

   Refinado por § Decisão (c) abaixo: default da aplicação invertido para absorção pré-commit + commit message estruturado; cutucada do operador via `AskUserQuestion` reservada para findings que satisfazem ≥1 das 3 condições. Mecânica do wiring (quando dispara, override por inação) preservada.

2. **`/new-adr`** (standalone OU delegada por `/triage`), antes de retornar controle. Cobre tanto ADR criada diretamente pelo operador quanto ADR criada pelo `/triage` no caminho ADR-only — evita dispatch duplo no caminho `/triage` → `/new-adr` → reviewer (passo 5 do `/triage` reconhece que `/new-adr` já cobriu o ADR; dispatch sobre o plano permanece).

`/run-plan` permanece sem wiring de `design-reviewer` — gate seria tarde (plano já no remote) e a frequência alta multiplicaria o custo de tokens sem ganho proporcional.

Razões objetivas:

- **Empíricas:** 7 findings cumulativos em 3 invocações no `/triage` pré-commit confirmam o ponto natural (dogfood deliberado registrado em § Origem histórica). Zero findings exercitados em `/run-plan` (não houve invocação ali no dogfood).
- **Custo aceitável:** `/triage` que produz plano/ADR é frequência **média**; `/new-adr` standalone é frequência **rara**. Free-read curado (per ADR-048 scan medium + always-include `[ADR-009, ADR-034, ADR-043]`) cabe nesse perfil.
- **Sem cutucada inicial:** perguntar `Rodar reviewer?` antes de toda invocação é cerimônia (resposta majoritária seria "Sim" durante dogfood). Findings reportados são o trilho automático.
- **Override por inação:** operador pode ignorar findings (commitar mesmo assim). `design-reviewer` reporta, não bloqueia.

### (c) Critério mecânico de absorção de findings do `design-reviewer` pré-commit (de ADR-026, sucessor parcial de § Decisão (b))

Default **invertido**: `design-reviewer` reporta findings → assistente **absorve pré-commit + reporta absorção no commit message em seção estruturada dedicada**. Operador inspeciona via diff/commit message e pode reverter se discordar (override por inspeção pós-fato).

**Forma do reporte.** Quando ≥1 finding é absorvido pré-commit, commit message inclui seção `## design-reviewer findings absorvidos` (idioma da convenção de commits do projeto consumidor per ADR-051 § Decisão (a)) com bullets curtos — 1 linha por finding no formato:

```
- <localização breve>: <correção aplicada> (caminho-único).
```

Auditoria pós-fato via `git log -p | grep "## design-reviewer"` lista todas as absorções para revisão. Seção é omitida quando não há findings absorvidos (zero overhead no caso comum). Findings que dispararam ≥1 das 3 condições e foram cutucados via `AskUserQuestion` não entram nesta seção — viram parte do trace narrativo normal do commit message (decisão do operador descrita).

**Cutucar operador via `AskUserQuestion` somente quando** o finding satisfaz **qualquer** das 3 condições:

1. **≥2 alternativas legítimas competindo.** Sugestão do reviewer admite 2+ caminhos válidos com trade-offs distintos. Operador escolhe. **Calibração:** alternativa apresentada pelo reviewer e descritivamente rebatida no próprio finding conta como **1 caminho** (reviewer assumiu a decisão); só conta como ≥2 quando o reviewer apresenta caminhos competindo sem rebater.
2. **Contradiz decisão documentada.** Finding rebate algo em ADR, `docs/philosophy.md` ou `CLAUDE.md`. Operador decide manter (honrar documentação) ou inverter (refinar documentação como passo separado).
3. **Exige contexto fora do diff/plano/ADR.** Intenção de produto, restrição externa, política organizacional do consumer — informação que o assistente não pode inferir dos artefatos visíveis.

**Cláusula default-conservadora.** Se o assistente não consegue classificar com confiança em qualquer das 3 condições (domínio desconhecido, shape ambíguo do finding), cutucar. Dúvida → cutucada.

Critério é **stack-agnóstico** — opera sobre shape do finding (alternativas / contradição / contexto externo), não sobre conteúdo da correção ou stack do projeto consumidor. Funciona em Python, Java, ou qualquer stack futura. Estável sob recursão — `design-reviewer` revisando ADR sobre seu próprio dispatching passa pelo mesmo critério.

Razões:

- **Empíricas:** 100% dos findings absorvidos previamente (~17) caem em "caminho-único" (nenhuma das 3 condições disparou); 100% dos findings perguntados via enum (~4) satisfizeram ≥1 condição. Critério é descritivo, não prescritivo.
- **Pragmáticas:** operador expressou preferência direta ("não quero ficar aprovando findings óbvios, ou de baixo custo/benefício").
- **Defensivas:** as 3 condições preservam o ponto crítico do `design-reviewer` — decisões estruturais com alternativas legítimas, contradição com doutrina, ou dependência de contexto externo **sempre** passam pelo operador.
- **Auditáveis:** commit message lista findings absorvidos — operador pode revisar e reverter via novo commit ou amend.
- **Override por inspeção pós-fato substitui parcialmente "override por inação" de § Decisão (b)** para findings classificados como caminho-único. Para findings que satisfazem ≥1 das 3 condições, "override por inação" segue vigente.

### (d) Mirror runtime das Decisões absorvidas: plan body + consumo por reviewers via `/run-plan` §2.3 (de ADR-038, sucessor parcial de § Decisão (c))

**Mirror de Decisões absorvidas** entre commit message (preservado por § Decisão (c)) e plan body, com mecânica runtime de consumo pelos reviewers via mensageiro upstream.

1. **Mirror no plan body.** A seção `## design-reviewer findings absorvidos` do commit message (§ Decisão (c)) tem **espelho idêntico** no body do plano (seção opcional `## Decisões absorvidas`, após `## Notas operacionais`). Mesmo formato de bullets:

   ```
   - <localização breve>: <correção aplicada> (caminho-único).
   ```

   `/triage` step 5 escreve em ambos os locais (mesma sequência atômica antes do commit). Seção omitida no plan body quando não há findings absorvidos (zero overhead no caso comum, paralelo ao tratamento do commit message).

2. **Consumo runtime por `/run-plan` §2.3 (reader).** Antes da invocação de cada reviewer por bloco, `/run-plan` lê `## Decisões absorvidas` do plan body (se existir) e passa o conteúdo como contexto adicional na prompt do reviewer. Mecanismo paralelo a `**Termos ubíquos tocados:**` (per ADR-048 free-read curado) — plano é o ponto único de transferência entre alinhamento e execução. Plano sem a seção → nada a passar (skip silente).

3. **Uniform protocol — contexto passa a todos os reviewers.** `/run-plan` §2.3 passa Decisões absorvidas a **todos** os reviewers invocados (code/doc/qa/security), não só ao `code-reviewer`. Custo simétrico (~poucas centenas de tokens); permite extensão futura a outros reviewers só editando o agent def (sem tocar `/run-plan`).

4. **`code-reviewer` cláusula consumer — context-aware via messenger upstream.** `agents/code-reviewer.md` carrega cláusula explícita: "se invocador passa `## Decisões absorvidas` como contexto, trate as estruturas listadas como **out-of-scope da rubrica YAGNI** — design-reviewer aprovou pré-commit + operador absorveu via § Decisão (c); flagar essas estruturas viola 'override por inação' de [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § Ockham operacionalizado em decisões internas do plugin (ex-ADR-035 Substituído por ADR-043 em 2026-05-29). Reporte apenas violações em estruturas **fora** da lista absorvida."

5. **Refinamento à [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § Ockham operacionalizado em decisões internas do plugin** (substância herdada de ADR-035 Substituído por ADR-043 em 2026-05-29). A afirmação *"code-reviewer mantém rubrica YAGNI universal no diff ... não tem context-aware switch nem free-read de ADRs"* (ADR-043 linha 62, preserved verbatim do ancestral) é refinada: introduz-se **categoria nova** "context-aware via messenger upstream" — `code-reviewer` reage a contexto **explicitamente passado pelo invocador** (não a contexto auto-lido). Distinção crítica: "free-read autônomo de ADRs" (`code-reviewer` lê ADRs por conta própria) **continua rejeitado** per ADR-043; "messenger upstream" (caller passa contexto pré-resolvido) é aceito.

Decisão é **plugin-internal** (governa componentes do próprio plugin). Não prescreve comportamento para consumer projects que adotem outros patterns de review.

## Origem histórica

Incidentes empíricos preservados que motivaram as decisões absorvidas (cada um materializa critério 1 ou 4 de ADR-034):

1. **2026-05-07 — Origem categoria foundational (ADR-009 preservado vigente standalone):** `/triage` do agent `design-reviewer` levantou que todos os reviewers atuais operam em diff pós-fato e consomem insumo curado pelo autor do plano; adicionar revisor que critique decisões estruturais antes de virarem código exige formalizar divergência do padrão atual + free-read autônomo de doctrine sources (porque autor não pode curar contradições com ADRs que não conhece). Categoria apex preservada vigente em ADR-009 (modo (c) ADR-052 — hardcoded na always-include de ADR-048; cross-ref preserved como autoridade).

2. **2026-05-07 → 2026-05-08 — Dogfood deliberado motivando wiring automático:** janela de dogfood deliberada acumulou **3 invocações reais** e **7 findings cumulativos**:

| # | Data | Plano/ADR | Findings |
|---|---|---|---|
| 1 | 2026-05-07 | `instrumentar-skills-multi-passo.md` (PR #44) | 4 — ADR-worthiness do critério "≥3 passos" → ADR-010 (estrutural); alternativa Monitor; acoplamento harness; cerimônia gate sub-steps |
| 2 | 2026-05-08 | `triage-step0-already-deleted-remote.md` (PR #45) | 1 — alternativa "abrandar regra inteira" |
| 3 | 2026-05-08 | `run-plan-3-3-skip-empirico.md` (PR #46) | 2 — alternativa "memory paliativa"; nota lexical vs semântico |

Padrão observado: todas as 3 invocações ocorreram em `/triage` que produziu plano (caminho-com-plano), antes do commit do plano. 5/7 findings foram editoriais; 1 foi estrutural (ADR-010 emergiu). Nenhum gerou retrabalho — todos couberam em ajustes pré-commit. Implicação para wiring: `/run-plan` pré-loop seria gate **tarde** (plano já commitado e pushed); `/triage` pós-plano/pré-commit é ponto natural; `/new-adr` standalone cobre ADRs criados fora do `/triage`.

3. **2026-05-08 → 2026-05-13 — Prática divergindo de ADR-011 literal:** prática empírica nas 11 sessões pós-ADR-011 (PRs #54-#60 + commits cirúrgicos F_arch/H_arch + sessões da release v2.6.0) divergiu do default literal "operador decide aplicar". Assistente passou a absorver findings triviais pré-commit em vez de cutucar para cada um. Análise retroativa identificou eixo discriminante (shape do finding) e calibrou as 3 condições mecânicas. Operador sinalizou expressamente preferência por absorção dos óbvios. Convenção empírica precisou virar regra escrita — caso contrário (i) fica frágil entre sessões (não documentada → reverte ao default literal de ADR-011), (ii) não generaliza, (iii) erro de classificação não tem critério de auditoria. Total empírico pré-codificação: ~17 findings absorvidos (caminho-único, zero retrabalho); ~4 findings cutucados (Cond 1 disparou em todos).

4. **2026-05-13 — Skill /draft-idea origem (alinhamento upstream):** operador propôs caminho upstream de `/triage` para casos de ideia vaga, com IDEA.md como output. Gap identificado: papel `product_direction` declarado na role contract sem caminho de criação assistida — operador escreve IDEA.md à mão ou não escreve, incoerência interna entre "declarado como role" e "sem produtor assistido". Substância (probe canonical + dual; elicitação multi-turn vs skeleton-only; fronteira nítida com `/triage`) decidida nesta sessão.

5. **2026-05-26 — Regressão silenciosa fechando gap operacional (ROADMAP item 1):** `code-reviewer` invocado mid-execução por `/run-plan` flaggou estrutura aprovada pré-commit pelo `design-reviewer` (3 boundaries enumeradas + cross-ref Escopo↔Tamanho). Default-absorber acionaria reversão silenciosa de decisão aprovada pelo operador via override-por-inação prescrito por ADR-035 (autoridade vigente à época do incidente; Substituído por ADR-043 em 2026-05-29; substância preservada em ADR-043 § Ockham operacionalizado em decisões internas do plugin). Sem perspicácia do agente para citar ADR-035/ADR-043 e cutucar via `AskUserQuestion`, regressão silenciosa — alto-impacto. Causa raiz: `code-reviewer` sem acesso ao registro das decisões já absorvidas pelo design-reviewer pré-commit (commit messages só são lidas por humanos via `git log`, não pelo reviewer agent durante invocação por bloco). Mecanismo: mirror entre commit message (preservado por § Decisão (c)) e plan body (introduzido por § Decisão (d)) com consumo runtime via mensageiro upstream.

## Consequências

### Benefícios

- **Camada doutrinal consolidada:** 4 ADRs absorvidos sob narrativa única coerente — pipeline `alinhamento upstream → wiring reviewer → critério de absorção → propagação runtime` legível em 1 ADR temático em vez de 4 fragmentados.
- **Cobertura sem ônus de memória:** decisões estruturais em planos/ADRs revisadas sem operador precisar lembrar de `@-mention`.
- **Ponto temporal correto:** findings chegam quando plano/ADR ainda está editável (pré-commit), maximizando ROI de cada finding.
- **Menos friction:** `/triage` caminho-com-plano e `/new-adr` deixam de gerar prompt para cada finding trivial. Operador é cutucado apenas para decisões reais.
- **Sinal mais nítido ao reviewer:** absorção automática reforça que findings devem ser substantivos. Falsos positivos viram drag mais visível.
- **Elimina dependência da perspicácia do agente** para detectar conflito reviewer-vs-reviewer (mecanismo (d) fecha gap operacional materializado em ROADMAP item 1).
- **Greppability dupla.** `git log -p | grep "## design-reviewer"` (commit messages) + greps em planos vivos (plan bodies). Auditoria histórica + estado-corrente.
- **Backward-compat completa.** Planos antigos sem `## Decisões absorvidas` continuam executáveis (reader skip silente); commits antigos com só commit message permanecem auditáveis.
- **Uniform protocol simplifica extensão futura.** Adicionar cláusula em `doc-reviewer` / `qa-reviewer` / `security-reviewer` (se manifestarem mesmo problema) só edita o agent def.
- **Gap entre role contract declarado e caminho de criação assistida fechado** (§ Decisão (a) materializa `/draft-idea` cobrindo `IDEA.md`).
- **Continuidade explícita upstream → downstream** (`/draft-idea` → `/triage` → `/run-plan`) materializa pipeline para operador novo.

### Trade-offs

- **`/triage` que produz plano/ADR fica mais caro por invocação** devido ao free-read curado (per ADR-048 ~15k tokens média pós-Onda 4 da reforma doutrinária). Aceitável dado o ROI empírico.
- **Classificação fica com o assistente.** Erro de classificação (finding com 2 alternativas tratado como caminho-único) gera absorção indevida sem cutucar. Mitigação: commit message expõe; operador revisa.
- **Volume do commit message cresce** quando há findings absorvidos. Trade aceitável — operador prefere texto a prompt.
- **Redundância textual.** Mesma seção em 2 locais (commit + plan body). Custo editorial; aceito por preservação de greppability histórica.
- **Risco de drift entre mirror locations.** Se `/triage` escrever em commit mas pular plan body (bug), agente coordenador depende do código de `/triage` estar correto. Mitigação: edits cirúrgicos do `/triage` step 5 são simétricos.
- **Refinamento à ADR-043 § Ockham operacionalizado sutil** (substância herdada de ADR-035 Substituído). Categoria "context-aware via messenger upstream" vs "free-read autônomo" exige leitura atenta. Mitigação: cláusula em `code-reviewer` agent def é explícita sobre o critério.
- **+1 skill no toolkit** (`/draft-idea`). Mitigação: skill simétrica a `/new-adr` (template já internalizado).

### Limitações

- **Free-read continua dependendo de ADRs granulares:** ADR vago não captura contradição (limitação herdada de ADR-009).
- **Paths não-canonicais:** se consumidor declara `decisions_dir` em modo local, free-read precisa enxergar `.claude/local/decisions/`. Tratado pelo Resolution protocol — `design-reviewer` lê `<decisions_dir>` resolvido, não path literal.
- **Domínios desconhecidos podem confundir classificação.** Stack nova com vocabulário específico — assistente pode não reconhecer alternativas legítimas. Coberto pela cláusula default-conservadora em § Decisão (c).
- **Não cobre decisões implícitas de conversa.** Operador respondendo X em `AskUserQuestion` sem registro no plano continua dependendo do agente coordenador. Coberto apenas o que entra no mirror via `/triage` step 5.
- **Cláusula só em `code-reviewer` por enquanto.** doc/qa/security recebem contexto mas não têm cláusula explícita de uso. Incremental — adicionar quando/se manifestarem mesmo problema (incidente-driven).
- **Falsos negativos persistem em casos-limite.** Finding crítico classificado erroneamente como "caminho-único" some — risco semelhante ao já reconhecido por ADR-011 § Trade-offs ("prosa volátil").
- **Skill `/draft-idea` assume operador minimamente capaz de articular** problema/persona — não é Q&A guiado para non-technical stakeholder; é estruturação para quem já tem intuição.
- **Skill `/draft-idea` modo update opera seção-a-seção;** não detecta inconsistências cross-seção (ex.: critério de sucesso que não bate com persona declarada). Operador é responsável pela coerência global.
- **Critério (c) não substitui revisão editorial humana de qualidade do reviewer.** Se `design-reviewer` produzir findings sistematicamente vagos ou off-target, absorção automática multiplica o problema. Refinar critério editorial do reviewer é decisão separada (herdada de ADR-026 § Limitações).

## Alternativas consideradas

### (a) Manter 4 ADRs fragmentados (status quo pré-Onda I)

Descartada. Pipeline alinhamento → wiring → absorção → propagação tem coesão semântica alta; manter fragmentado força leitor a percorrer 4 ADRs para entender ecosistema. Consolidação é exatamente o movimento que ADR-045 § Decisão parte 1 materializa.

### (b) Absorver ADR-009 no consolidado (sem aplicar modo (c) ADR-052)

Descartada. ADR-009 está hardcoded na always-include de ADR-048 § Decisão `[ADR-009, ADR-034, ADR-043]` — absorvê-lo exigiria editar ADR-048 Aceito (mexer ADR-classical é antipattern) + leitura mecânica do design-reviewer cairia em ADR-009 archived com redirect em vez do consolidado. Critério mecânico verificável de ADR-052 § Decisão (c) PRESERVAÇÃO POR CONSTRAINT MECÂNICO PURO aplica: `grep "ADR-009" docs/decisions/ADR-048-*.md` → match em § Decisão de ADR Aceito vigente. Pattern análogo a ADR-034 em Onda H reaplicado.

### (c) Incluir ADR-042 no consolidado (sketch literal sem aplicar modo (a) ADR-052)

Descartada. ADR-042 (`/note --to` cross-project write) tem categoria semântica distinta (skill `/note` bridge/cross-project, não design-reviewer ecosystem). Sketch original do charter listava ADR-042 em 2 clusters distintos (alinhamento E bridge-meta-system) — contradição interna análoga a ADR-039 em Onda F. Critério mecânico verificável de ADR-052 § Decisão (a) bullet 1 EXCLUSÃO aplica (desalinhamento semântico).

Trade-off honesto: ADR-042 carrega carga doutrinária autônoma (`/note --to` semantics, `$PROJECTS_DIR` discovery contract, target inicializado pré-condição) que não se reduz a sub-dimensão do design-reviewer ecosystem. Forçar inclusão exigiria ampliar narrativa única do consolidado para abarcar bridge/cross-project, dilatando coesão semântica do cluster. Preservação standalone aguarda Onda bridge com critério editorial próprio (ADR-042 pertence ao futuro cluster bridge/discoverability junto com ADR-032 — preservado vigente standalone aguardando onda própria).

### (d) Adendo em ADR-011 absorvendo ADR-026 + ADR-038 (sem ADR consolidado novo)

Descartada per ADR-034 cond 5 (sucessor parcial primária) + cond 4 (introdução de categoria nova de meta-decisão "consolidado temático"; precedente em ADR-046+047+048+049+050+051). Adendo em ADR-011 seria incoerente — ADR-011 é trade-off vivo histórico (mecânica do wiring); consolidado integra ecosistema sob narrativa única. Pattern editorial do charter (cluster temático em consolidado novo) prevalece.

### (e) Splittar consolidado em 2 ADRs (alinhamento upstream + reviewer ecosystem)

Descartada. Coesão pipeline `/draft-idea → /triage com design-reviewer wiring → absorção → mirror runtime` é load-bearing — splitar empobreceria narrativa unitária. Sub-dimensões (a-d) acomodam separação editorial sem fragmentar ADRs.

## Gatilhos de revisão

- **Operador frequentemente ignora findings sem aplicar (ou reporta findings importantes perdidos):** sinal de que `design-reviewer` está sensível demais, tokens não compensam, ou a prosa volátil falha em capturar findings sérios. Reabrir critério editorial do reviewer, voltar para opt-in, ou introduzir trilho persistente análogo a `## Pendências de validação` de ADR-020.
- **Tokens de `/triage` superam ROI mensurável:** se ADRs crescerem além de target charter (~13-15 pós-redesign) ou `philosophy.md` dobrar de tamanho, free-read fica caro mesmo em frequência média. Reabrir per ADR-048 gatilho de revisão.
- **Falsos positivos crescem:** reviewer flaga findings que operador descarta sistematicamente — sinal de que ADRs estão vagos ou critério do reviewer precisa refinamento.
- **Operador reverter findings absorvidos sistematicamente** via commits subsequentes. Sinal de classificação errônea recorrente — reabrir critério, possivelmente adicionar 4ª condição ou refinar definição de "alternativas legítimas".
- **Reviewer começar produzindo findings repetidamente classificáveis como "alternativas competindo" que operador descarta sempre.** Sinal de critério editorial do reviewer para refinar.
- **Skill nova introduzir reviewer pre-fact com semântica diferente do `design-reviewer`** (ex.: revisor de produto pre-fact). Revisar escopo deste ADR — critério (c) aplica apenas a `design-reviewer` por design.
- **Operador reportar findings importantes perdidos no commit message** (volume cresce demais, operador deixa de inspecionar). Reabrir formato — possivelmente persistir absorções em `## Pendências de validação`.
- **Drift entre mirror locations observado em uso real:** ≥2 ocasiões em que `/triage` escreveu em commit message mas pulou plan body (ou vice-versa). Reabrir mecanismo de write-coupling (transação atômica explícita).
- **Outro reviewer manifesta mesmo problema de incompatibilidade context vs YAGNI:** se doc/qa/security ganharem incidentes análogos ao item 5 da § Origem histórica, estender cláusula consumer.
- **Decisões conversacionais avulsas demandam mirror análogo:** se operador responder via `AskUserQuestion` mid-execução de `/run-plan` revertendo ou refinando estrutura aprovada em plano pré-existente, esse trace conversacional precisa virar registro consumível por reviewer subsequente. Hoje apenas absorvidos automáticos do `design-reviewer` via `/triage` step 5 alimentam o mirror. Reabrir escopo do mirror se ≥2 incidentes desse tipo materializarem regressão silenciosa análoga à originária (item 5).
- **Modo update seção-a-seção via enum mostra-se cerimonial na prática** (operador escapa repetidamente para "Other" prosa livre) — reabrir decisão de modo de operação de `/draft-idea`.
- **Skill `/draft-idea` criada mas operadores usam diretamente chat livre + `Write` para `IDEA.md`** sem invocar `/draft-idea` em >50% dos casos detectáveis — sinal de que estrutura de elicitação não está agregando valor; reabrir escopo (skeleton-only? remover?).
- **Pipeline `/draft-idea` → `/triage` mostra-se ruidoso** (operador raramente segue a sugestão) — reabrir decisão de "sugerir próximo passo".

## Auto-aplicação

**ADR-034 critério mecânico (adendo vs novo ADR — 5 condições para novo; 4 para adendo):**

- **Cond 5 (sucessor parcial — estende, refina ou condiciona ADR Aceito sem revogar):** **APLICA** — primária isolada. ADR-053 absorve substância de ADR-011 + ADR-026 + ADR-027 + ADR-038 (4 ADRs Aceito vigentes) preservando regra central de cada um integralmente. Nenhum marcado como `Substituído` — categoria editorial "absorção consolidatória" (per F4 lesson Onda D refinada) vs "revogação" (que inverteria doutrina central; ex.: ADR-043 → ADR-035). ADR-009 preservado vigente fora do cluster (modo (c) ADR-052 — constraint mecânico hardcoded em ADR-048 always-include). ADR-042 preservado vigente excluído (modo (a) ADR-052 — desalinhamento semântico do sketch). Pattern editorial 7ª aplicação consecutiva (Ondas C+D+E+F+G+H + Onda I) consolidando integridade da regra mecânica.

- **Cond 4 (codificação de pattern emergente — N≥3 incidentes recorrentes):** **NÃO APLICA** — ADR-045 carrega categoria meta "consolidação editorial sob redesign" desde Onda A; ADR-053 é sétima instância de migração temática (após ADR-046+047+048+049+050+051), não categoria nova. Aplicar cond 4 inflaria critério em cada onda diluindo ADR-034. Cond 4 também foi borderline em [ADR-052](ADR-052-codificacao-3-modos-editoriais-refinamento-consolidacao.md) § Auto-aplicação (primeira instância de codificação de meta-pattern editorial); ADR-053 herda o mesmo critério conservador — estreia editorial (combinação inédita modos a+c simultâneos) NÃO equivale a categoria conceitual nova de artefato. Pattern editorial reconhecido em ADR-052 reaplicado literal.

- **Cond 1 (decisão estrutural sem ancestral codificado):** **NÃO APLICA** — ADR-045 § Decisão parte 1 (consolidação 45 → ~13-15 ADRs sob hierarquia invertida) + ADR-046+047+048+049+050+051 (templates do pattern de migração) + ADR-052 (meta-pattern editorial canonical) são ancestrais codificados diretos. Ondas C+D+E+F+G+H validaram pattern empíricamente.

- **Cond 2 (substitui ADR ancestral revogando doutrina central):** **NÃO APLICA** — regra central de cada ADR absorvido preservada integralmente em § Decisão (a-d). Ondas C-H reaplicaram literal a distinção "absorção consolidatória vs revogação" (per F4 lesson Onda D).

- **Cond 3 (codificação de restrição externa de longa duração):** **NÃO APLICA** — esta é decisão interna do plugin sobre composição editorial da camada doutrinal.

**ADR-052 critério mecânico de modos editoriais (3 modos canonical):**

- **Modo (a) EXCLUSÃO bullet 1 (desalinhamento semântico do sketch):** **APLICA sobre ADR-042**. Critério mecânico verificável: ADR-042 cita `/note`/`$PROJECTS_DIR`/`.claude/local/NOTES.md` cross-project como decisão central — zero overlap semântico com design-reviewer wiring/absorção. Sketch original do charter listava ADR-042 em 2 clusters distintos (contradição interna análoga a ADR-039 em Onda F). Pattern editorial Onda F EXCLUSÃO reaplicado.

- **Modo (b) INCLUSÃO:** **NÃO APLICA** — nenhum ADR foi incluído ao cluster além do sketch original (4 absorvidos = 4 dos 8 originais menos ADR-009 modo (c) + ADR-042 modo (a) + ADR-017+ADR-029 já archived em Onda C).

- **Modo (c) PRESERVAÇÃO POR CONSTRAINT MECÂNICO PURO:** **APLICA sobre ADR-009**. Critério mecânico verificável: `grep "ADR-009" docs/decisions/ADR-048-*.md` → match em § Decisão de ADR Aceito vigente (always-include curated list `[ADR-009, ADR-034, ADR-043]`). Análogo a ADR-034 em Onda H reaplicado. Categoria semântica distinta adicional: ADR-009 é foundational (revisor document-level pré-fato + free-read de doctrine), não ecosistema operacional wired sobre ele.

**Status:** Proposto (default per template). Promoção a Aceito após design-reviewer auto-fire (5 do plano `/triage` step 5) sem findings absorvíveis que mudem substância central.
