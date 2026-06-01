# ADR-045: Redesign da camada doutrinal — consolidação sob hierarquia invertida e política de admissão going forward

**Data:** 2026-05-30
**Status:** Aceito (2026-06-01)

## Origem

- **Decisão base:** [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) (apex doutrinal — Verdade/Excelência/Ockham como raiz; pragmáticos como consequência operacional). Este ADR estende o trabalho de ADR-043 ao inventário doutrinal acumulado: aplica a hierarquia ao próprio `docs/decisions/` para organizá-lo sob essa raiz + codifica mecanismo de prevenção de re-acúmulo. Não revoga ADR-043 — opera sobre seu conteúdo.
- **Investigação:** sessão `tres-principios` (toolkit 2026-05-30) recebeu crítica externa via web chat Claude em 4 turnos analisando `philosophy.md` v2.14.0 + inventário de 45 ADRs. Crítica turno 4: *"ADRs como memória de trabalho, não como registro de decisões"*; aposta 5-8 ADRs sobreviventes; estrutura proposta em 3 camadas (`philosophy.md` porquê duradouro + `CLAUDE.md` como mecânico + `decisions/` apenas reversíveis) + política de admissão going forward. Operador propôs **inversão do ônus da prova**: *"já que a estrutura doutrinária cresceu de forma desordenada com os ciclos de refinamento, o redesign aproveitando o que já foi refinado, desenhando a arquitetura como se já soubéssemos de todo o conhecimento acumulado hoje desde o dia 0, não melhoraria o projeto ou ao menos a legibilidade?"* Inversão se sustenta sob aplicação dos próprios 3 princípios ao inventário doutrinal. Arco completo + sketch da estrutura-alvo (11 ADRs) + anti-regression checklist + 8 riscos identificados registrados em `.claude/local/NOTES.md` entry 2026-05-30T06:08:04Z (informational store per [ADR-032](ADR-032-skill-note-contexto-compartilhado.md) e [ADR-005](ADR-005-modo-local-gitignored-roles.md)).
- **Convergência empírica independente:** NOTES 2026-05-30T05:08:52Z (sessão `meta-system-tres-principios`) registrou que os 3 princípios fundamentais *"funcionam como thinking-with, não labeling-against"* durante refinamento iterativo de ADR-008 do meta-system — sinal empírico pós-shipping que os ADRs também fazem função dupla análoga (working-memory vs decision-record). Convergência com crítica externa turno 4 (*"ADRs como memória de trabalho, não registro de decisões"*) por 2 ângulos independentes confirma fronteira real — política de admissão going forward é essa linha codificada.
- **Plano coordenador:** `docs/plans/redesign-camada-doutrinal-charter.md` decompõe operacionalização em ondas A (esta, foundational) → B (`philosophy.md` condensado) → C-X (migração cluster-by-cluster com design-reviewer validando cada absorção) → final (admission policy enforcement em `/new-adr` + archive index + propagação cross-refs + release `v3.0.0`). Charter é par operacional deste ADR; estrutura-alvo sketch (11 ADRs) + anti-regression checklist vivem no charter como artefato refinável durante execução das ondas.

## Contexto

A camada doutrinal do toolkit — `docs/philosophy.md` + 45 ADRs em `docs/decisions/` + cross-refs em `CLAUDE.md`/skills/agents — cresceu via refinamento incremental sem consolidação periódica desde o início do projeto. Inventário ADRs por fases históricas:

- **Fase formativa** (ADRs 001-016): mecanismo core + auto-gating + skills primárias.
- **Fases de refinamento** (ADRs 017-034): incidentes empíricos cumulados (PJe, smoke-tests), cutucadas, modo local, [ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) (exceção interna ao YAGNI — agora Substituído).
- **Reforma doutrinária Ondas 1-4** (ADRs 035→043 reframado, 044): hierarquia invertida + cluster index Addenda + free-read curado.

Resultado em 2026-05-30: 45 ADRs, dos quais ~6 são **meta-doutrinais** ([ADR-021](ADR-021-curadoria-free-read-design-reviewer.md), [ADR-026](ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md), [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md), ADR-035 Substituído, ADR-043, [ADR-044](ADR-044-scan-medium-always-include-free-read-design-reviewer.md)) e o restante agrupável em clusters semânticos coerentes (modo local: 005/018/025/030; cutucadas: 017/029; alinhamento: 009/011/026/027; execução: 004/028/037/039/041; convenções editoriais: 007/012/024/034; trade-offs vivos: 002/014/016/038/041).

**Estado de estabilização confirmado pós-v2.14.0:**

- **Semântica:** 3 princípios fundamentais (Verdade, Excelência, Ockham) operam empiricamente como *thinking-with* em decisões internas — sinal pós-ship em sessão `meta-system-tres-principios` 2026-05-30T05:08:52Z (refinamento de ADR-008 do meta-system) + reprodução na sessão `tres-principios` (esta).
- **Operacional:** ADR-044 estabilizou o free-read curado do design-reviewer (alavanca de token cost materializada ~58%).
- **Editorial:** ADR-034 codificou critério mecânico adendo vs novo ADR; Onda 3 da reforma demonstrou consolidação cluster-by-cluster como pattern aplicável (ADR-005 + ADR-017 cluster index Addenda).

**Crítica externa convergente com observação independente:** *"ADRs como memória de trabalho, não como registro de decisões"* (crítica externa turno 4) rima com *"princípios funcionam como thinking-with, não labeling-against"* (NOTES 2026-05-30T05:08:52Z). Os ADRs estão fazendo função dupla — alguns são working-memory (think-with do autor durante evolução), outros são decision-records (label-against para revertedor futuro). O toolkit não desenhou a linha. Sem essa linha codificada, o ciclo de re-acúmulo continua: cada refinamento gera ADR; em 6 meses são 60+, em 12 meses 80+.

**Status sob aplicação dos 3 princípios ao próprio inventário:**

- **Verdade:** estrutura é empiricamente desordenada — acumulação ≠ design. Nomear isso é observação verificável.
- **Excelência:** mecanismo do toolkit (skills/agents/hooks/`CLAUDE.md` contrato) tem qualidade alta — precisão, auto-gating triplo, degradação graciosa. Doutrina tem precisão semelhante mas organização inferior. Trazê-la ao padrão do mecanismo é Excelência aplicada a si mesma.
- **Ockham:** se ~10-12 ADRs temáticos carregam mesma carga doutrinal que 45 fragmentados — sem perder informação load-bearing — versão enxuta é melhor por construção. Ônus da prova passa pra mostrar o que se perderia (não o que se ganharia).

**Precedente empírico no próprio projeto:** Onda 3 da reforma doutrinária aplicou cluster index Addenda em ADR-005 (modo local: ADR-018/-025/-030) e ADR-017 (cutucadas: ADR-029 + procedure) — 2 clusters consolidados como prova de conceito de exatamente este movimento. Esta decisão generaliza para o inventário inteiro.

## Decisão

**Refazer a camada doutrinal do toolkit pós-v2.14.0 em duas decisões coordenadas: (1) consolidação editorial do inventário de ADRs sob hierarquia invertida; (2) política de admissão going forward para prevenir re-acúmulo.**

### 1. Consolidação editorial sob hierarquia invertida

Consolidar 45 ADRs atuais em ~10-12 ADRs temáticos absorvendo conteúdo por cluster semântico. Cada ADR consolidado:

- Cobre **uma decisão estrutural reversível** que um eu-futuro pode querer reverter e precisar do contexto (filtro de admissão aplicado retroativamente).
- Absorve 3-6 ADRs antigos relacionados (cluster temático) preservando substância em `## Origem histórica` (incidentes empíricos preservados — PJe 2026-05-11, smoke-tests, etc.).
- Mantém `## Gatilhos de revisão` consolidados das decisões absorvidas.
- Referência adequada a ADRs antigos arquivados (não deletados — preserva trilha empírica).

ADRs antigos vão para `docs/decisions/archive/<slug>.md` com mensagem de redirect (`# ADR-NNN: ARCHIVED — content absorbed into ADR-MMM in new structure; see <path>`). Arquivamento (não deleção) materializa **Verdade** — preserva memória do projeto sobre onde formalização passou do ponto; **Ockham** aplica-se ao espaço de doutrina vigente, não ao arquivo histórico que git já mantém de qualquer jeito.

A **estrutura-alvo sketch** (11 ADRs em camadas: componentes plugin, path contract, modo local, alinhamento, execução, reviewers, convenções editoriais, trade-offs isolados, bridge, instrumentação, meta-doutrina) está preservada em `docs/plans/redesign-camada-doutrinal-charter.md` § Resumo da mudança como **artefato para criticar, não decisão imutável** — sequence de cluster absorption refinada por ondas anteriores. Decisão imutável é a regra de consolidação (sob hierarquia invertida + filtro de admissão); a forma exata é descobrível durante execução das ondas.

**Fronteira "ajuste editorial do charter" vs "revisão de ADR-045".** Ajuste de cluster sequence (ordem de migração), subdivisão de consolidado em 2 (ex.: alinhamento + reviewer dispatch), absorção de ADR em consolidado diferente do sketch original → **ajuste editorial livre** do charter durante execução. Mudança estrutural na regra de consolidação (ex.: deixar de usar hierarquia invertida como critério; abandonar filtro de admissão; reverter para 45 fragmentados) → **revisão de ADR-045** via gatilho declarado em § Gatilhos. Limite operacional: design-reviewer flag de "estrutura-alvo revelada inadequada" em ≥2 ondas (§ Gatilhos) marca transição de ajuste editorial para revisão formal.

Implementação em **6-10 ondas subsequentes** coordenadas por `docs/plans/redesign-camada-doutrinal-charter.md`: Onda A (esta, foundational — charter + meta-ADR + bullet em `CLAUDE.md`), B (`philosophy.md` condensado), C-X (migração cluster-by-cluster com design-reviewer validando cada absorção), final (admission policy enforcement em `/new-adr` + archive index + propagação cross-refs + release `v3.0.0`).

### 2. Política de admissão going forward

Codificar filtro mecânico de 3 saídas aplicado **antes** da criação de novo ADR:

| Saída | Quando | Destino |
| --- | --- | --- |
| **ADR** | Decisão estrutural reversível: futuro-eu vai querer reverter e precisa do contexto (trade-off vivo, contrato de integração, política do sistema). | `docs/decisions/ADR-NNN-<slug>.md` clássico, imutável, supersedeção via novo ADR (jamais edita; jamais substitui conteúdo do antigo). |
| **`CLAUDE.md`** ou **`philosophy.md`** | Entendimento estabilizado: refinamento de mecanismo, esclarecimento doutrinal, regra editorial estabilizada. | Absorvido no documento canonical relevante + commit message. Sem ADR. |
| **git log** | Evolução de processo: refactor sem decisão estrutural; iteração editorial. | Apenas commit message. Sem documento. |

**Heurísticas para classificação (primárias):**

- **Reversibilidade positiva**: consigo nomear cenário concreto onde reverteria? (incidente empírico, sinal de uso real divergente da hipótese, mudança de plataforma, restrição externa surgida). Sim → ADR. Não consigo nomear cenário concreto → entendimento estabilizado.
- **Categoria nova**: introduz categoria conceitual que não existe na doutrina vigente? (sim → ADR)
- **Codifica restrição externa**: regulatória, contratual, integração de longa duração? (sim → ADR)
- **Pattern emergente**: pode ser auditado retroativamente como ≥3 aplicações ad hoc? (sim → ADR)

Heurísticas paralelas aos 4 critérios de [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § Ockham operacionalizado em decisões internas do plugin — ADR-045 promove esses critérios de "razões para considerar criar ADR doutrinal" para "saída do filtro de admissão como output mecânico".

**Critério de desempate na zona cinzenta** (fronteira reconhecida em § Limitações):

- **Bifurcação `CLAUDE.md` vs `philosophy.md`**: doutrina cross-cutting (princípio epistêmico, convenção que aplica em múltiplos contextos, regra que ancora outras regras) → `philosophy.md`; mecânica do plugin (lifecycle, naming, gate concreto, cutucada, schema YAML, AskUserQuestion convention) → `CLAUDE.md`.
- **Bifurcação "não-ADR" vs "git log"**: se a mudança altera **doutrina ou mecanismo** que outro agent/skill consulta em runtime (philosophy.md, CLAUDE.md, agent/skill spec) → `CLAUDE.md`/`philosophy.md`/agent-skill prose + commit message; se altera apenas implementação/estilo sem afetar runtime de outros componentes → git log.
- **Fronteira "reversível" vs "estabilizado" (default conservador)**: dúvida → cutucar via `design-reviewer` finding (enforcement na onda final). Não criar ADR por inércia retórica; não suprimir ADR por economia editorial.

**Implementação operacional (escalonada em ondas):**

- **Esta onda (A):** bullet em `CLAUDE.md` § Editing conventions cross-ref a este ADR (executado como Bloco 1 do plano por `/run-plan`).
- **Onda final:** `/new-adr` step novo (provavelmente 3.5) surfa o filtro como prompt informativo antes de criar o arquivo (codificado junto com archive cleanup); `design-reviewer` ganha critério adicional em `## O que flagrar`: candidato a ADR que falha no filtro (entendimento estabilizado que devia ir pra `CLAUDE.md`) é finding pré-criação.

**Condição de validade do enforcement.** Se durante Onda final for descoberto que step 3.5 em `/new-adr` não é viável (ex.: conflito com fluxo de `/triage` step 4 que delega `/new-adr` — cutucar o operador na própria delegação rebaixaria UX da skill primária), enforcement primário **migra para `design-reviewer` `## O que flagrar`** — a política não é shippada sem enforcement codificado em ≥1 superfície runtime. Bump v3.0.0 condiciona a essa garantia: política sem enforcement é decoração doutrinal, exatamente o que ADR-045 quer evitar.

**Risco a vigiar:** ADR-045 sendo o caminho preferido pra "achei interessante essa observação, vai virar refinamento de ADR-045" — recursão. Mitigação: ADR-045 é **congelado** depois do término da redesign (onda final marca status `Aceito` definitivo); refinamento de doutrina pós-redesign segue o filtro normal (admission policy aplicada — refinamentos vão pra `CLAUDE.md` ou git log, não pra ADR-045 § Decisão). Durante a própria redesign (ondas C-X), categorias novas que passem no filtro entram como ADR-046+ — ver § Gatilhos de revisão (*"Categoria nova emerge durante execução"*).

### Razões (cobrindo ambas as partes)

- **Coerência interna sob hierarquia invertida** (Verdade aplicada à doutrina): nomear desordem é primeiro passo. Estrutura organizada em ~10-12 ADRs temáticos espelha a precisão do mecanismo do toolkit (skills/agents/hooks).
- **Mecanismo de prevenção codificado, não confiado** (Excelência sem over-engineering): filtro mecânico de 3 saídas estanca o ciclo de re-acúmulo na origem; sem ele, podaria-se para 12 e em 6 meses seriam 50 de novo (*"se levar a mesma cabeça pro projeto novo, ela vai reconstruir a mesma catedral em 3 meses"* — crítica externa turno 3).
- **Ockham aplicado ao próprio inventário doutrinal**: versão enxuta carrega mesma carga; ônus da prova invertido (mostrar perda, não ganho).
- **Política de admissão é a operacionalização do filtro de [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § Ockham operacionalizado**: os 4 critérios eram "razões para considerar codificar"; o filtro de 3 saídas é "output de admissão como decisão mecânica" — promovendo critérios internos de ADR-043 a saída universal.
- **Trilha empírica preservada via arquivamento**: ADRs antigos sob `docs/decisions/archive/` mantêm acessibilidade ao incidente que motivou cada decisão original (PJe, smoke-tests, etc.); cluster consolidado absorve substância em `## Origem histórica` resumida.
- **Bump major v3.0.0 sinaliza para consumer**: revisão estrutural da camada doutrinal (45 → ~12 ADRs com archive + cross-refs propagados) altera material que consumer terceiro inspeciona ao avaliar atualização — `docs/decisions/` é descoberto durante onboarding e durante `/plugin update`. Mesmo sem breaking change runtime, a estrutura inspecionável muda significativamente. Major é trade-off aceito: custo de signaling (semver convencional sugere breaking) vs benefício de não esconder mudança estrutural sob minor (minor + release note destacada seria opção competidora; rejeitada porque release note discovery é assimétrica — consumer que pula leitura pula sinal). § Gatilhos linhas correspondentes detectam falha do framing pós-bump.

## Consequências

### Benefícios

- **Legibilidade considerada para terceiros e contribuidores**: ~10-12 ADRs temáticos é navegável; 45 fragmentados não é.
- **Token cost adicional reduzido em design-reviewer free-read**: ADR-044 já curou; com inventário menor, scan medium tem menos targets e always-include continua relevante.
- **Filtro de admissão estanca crescimento desordenado**: política going forward é a alavanca real de longo prazo; sem ela, qualquer poda é temporária.
- **Trilha empírica preservada via archive** + `## Origem histórica` em consolidados: nenhuma perda histórica.
- **Estrutura espelha qualidade do mecanismo**: doutrina e mecanismo do toolkit operam no mesmo padrão (Excelência aplicada a si mesma).
- **Pattern reaplicável**: outros consumers do toolkit que enfrentem mesmo problema (ADRs proliferando) podem aplicar este charter como modelo.

### Trade-offs

- **Custo substancial de migração**: 6-10 ondas dedicadas; semanas de trabalho focado. Mitigação: decomposição em ondas individuais (cada uma é entrega cirúrgica); dogfood mantém invariantes.
- **Link rot durante migração**: cross-refs antigos quebram conforme ADRs absorvidos. Mitigação: redirects estruturados nos arquivos arquivados; tabela de mapeamento velho→novo durante migração.
- **Risco de inconsistência editorial cross-ondas**: consolidação cluster A pode interpretar critério ligeiramente diferente de cluster B se ondas espaçadas no tempo. Mitigação: design-reviewer aplica anti-regression checklist como rubric em cada onda; charter explicita critério de absorção.
- **Filtro de admissão going forward depende de enforcement**: se mecanismo apenas surfa como prompt informativo, viola-se por descuido. Mitigação: codificar `design-reviewer` para flagar candidato a ADR que falha no filtro como finding (onda final).

### Limitações

- **Não cobre código consumer**: redesign aplica-se ao inventário doutrinal interno do plugin; skills/agents/hooks/`CLAUDE.md` mecanismo intocado por construção.
- **Estrutura-alvo (11 ADRs sketch) é descobrível, não imutável**: forma exata refinada durante execução; algumas absorções podem precisar de subdivisão (ex.: ADR-004 alinhamento absorve 8 antigos — pode ser muito; pode dividir em alinhamento + reviewer dispatch se design-reviewer flagar).
- **Doutrina ainda fluida em alguma área** sendo congelada antes da hora pode dar retrabalho. Mitigação: estado pós-Onda 4 confirmou estabilização das alavancas; áreas fluidas reconhecidas (gap do `block_gitignored.py` — NOTES 2026-05-30T05:26:59Z — endereçamento pendente; redesign reserva espaço de extensão em ADR consolidado correspondente).
- **Filtro de admissão tem zona cinzenta**: distinguir "decisão reversível" de "entendimento estabilizado" exige julgamento. Mitigação: heurísticas operacionais codificadas; default conservador é cutucar via design-reviewer.

### Mitigações

- **Anti-regression checklist** em `docs/plans/redesign-camada-doutrinal-charter.md` § Verificação end-to-end lista carga doutrinal que NÃO pode ser perdida; design-reviewer aplica como rubric em cada onda. **Checklist só pode crescer** durante a redesign (adicionar itens descobertos) — nunca encolher silente; remoção exige justificativa explícita no commit da onda que remove + cutucada ao operador. Garantia editorial mecânica protege a mitigação central de derivar.
- **Cada onda C-X passa por `/triage` → `/run-plan` → design-reviewer auto-fire**: dogfood end-to-end serve como gate de qualidade per consolidação.
- **Charter atualizado progressivamente** marcando ondas shippadas + ajustes de cluster sequence conforme descobertos (fronteira "ajuste editorial" vs "revisão de ADR-045" delineada em § Decisão parte 1).
- **Onda final inclui audit retroativo**: se algum item do anti-regression checklist não tem lar claro, audit reabre absorção relevante.

## Alternativas consideradas

### (a) Status quo — manter inventário desordenado, contar com curadoria editorial seletiva

Continuar com 45 ADRs (e crescendo); apenas Addenda pontuais quando overhead específico for percebido (paralelo a ADR-005 e ADR-017 da Onda 3 da reforma).

Descartada via aplicação dos 3 princípios:

- **Verdade**: nomear que a estrutura é desordenada e não fazer nada é incoerente; verifica-se que o problema é estrutural, não pontual.
- **Excelência**: doutrina é o output epistêmico do projeto; manter inconsistência entre qualidade do mecanismo e qualidade da doutrina viola padrão.
- **Ockham**: inventário cresce O(#decisões); cada novo ADR aumenta custo de manutenção (cross-refs, free-read tokens, onboarding). Não-decisão é decisão por inação.

### (b) Archive-and-restart — novo plugin com a doutrina refinada desde o início

Proposta original do operador (sessão upstream pré-reforma doutrinária 2026-05-29). Reset crisp das 45 ADRs + skills + agents + hooks; novo repo livre do "viés acumulado".

Descartada via análise dos 3 princípios + crítica externa convergente (turno 2):

- **Verdade**: sampling empírico dos ADRs mostrou que doutrina existente já opera implicitamente nos fundamentais. O que se desejava resetar (ruído doutrinal) é deletável em PRs no projeto atual.
- **Excelência**: refactor in-place serve o problema concreto (codificar redesign + cross-ref retroativo) com edits cirúrgicos. Archive-and-restart custaria semanas pra recuperar paridade do mecanismo.
- **Ockham**: 1 plugin com hierarquia explícita > 2 instâncias do mesmo mecanismo (archived + new). Redesign in-place não cria entidade nova — refina relação dentro de doutrina já existente.
- Crítica externa convergente: *"se você levar a mesma cabeça pro projeto novo, ela vai reconstruir a mesma catedral em 3 meses. Rewrite não cura impulso."*

### (c) Apenas política de admissão going forward (sem consolidação retroativa)

Codificar o filtro de 3 saídas para ADRs futuros; deixar os 45 atuais como estão.

Descartada:

- Não resolve o problema de legibilidade do inventário atual (consumer terceiro abrindo `docs/decisions/` ainda vê 45 ADRs caóticos).
- Política sem aplicação retroativa não enforça si própria — operador continua tendo 45 referências cruzadas a navegar; design-reviewer continua scaneando 45 ADRs (ADR-044 já curou, mas overhead per ADR cresce).
- Half-measure: deixa o problema estrutural enquanto trata apenas o sintoma futuro.

### (d) Apenas consolidação retroativa (sem política de admissão going forward)

Consolidar 45 → ~12 sem codificar filtro pra novos ADRs.

Descartada via convergência crítica externa + observação independente:

- Sem filtro, o ciclo de re-acúmulo continua. Em 6-12 meses, inventário consolidado vira novamente fragmentado.
- *"O caos não é estrutural — é uma política de admissão ausente. Adicione a política e o caos para de se reproduzir"* (crítica externa turno 4).
- Movimento incompleto: trata o sintoma atual (45 ADRs) sem tratar a causa (impulso de formalizar não-filtrado).

### (e) Manter ADR-043 como Aceito + adendo cross-ref a este ADR (em vez de codificar ADR-045 separado)

Pattern usado em ADR-005/-017 (cluster index Addenda da Onda 3 da reforma).

Descartada per [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) cond 4 (categoria nova) + cond 5 (sucessor parcial):

- ADR-043 codifica raiz epistêmica do toolkit (princípios como hierarquia, instanciação contextual em decisões internas via § Ockham operacionalizado).
- ADR-045 introduz categoria nova: **consolidação editorial cross-cluster do inventário inteiro como decisão estrutural** + **filtro de admissão como mecanismo de prevenção**. Categorias distintas com objetos diferentes — somar "consolidação editorial de inventário inteiro" + "política de admissão going forward" como adendo introduziria 2 categorias operacionais novas em ADR cuja decisão central é estrutural-epistêmica, não editorial-operacional.
- Onda 3 da reforma fez Addenda em ADR-005/-017 porque cada um era foundational de um cluster com sucessores parciais auto-evidentes (4 e 3 respectivamente); a consolidação editorial NESSES casos cabia como aglutinador editorial pontual. ADR-043 tem escopo distinto (raiz epistêmica cross-cutting); receber esses 2 objetos operacionais novos como adendo violaria a coesão semântica do ADR base.

### (f) Outras alternativas levantadas mas não competidoras

Crítica externa também tocou: (i) cortar primeira seção de `philosophy.md` (princípios) e confiar que pragmáticos se sustentam; (ii) mover seção epistêmica para RATIONALE.md ou ADR-raiz; (iii) restruturar `philosophy.md` + 45 ADRs como 3 camadas independentes.

Tratadas separadamente:

- (i) Reabre contradição que a própria crítica diagnosticou na versão anterior; NOTES 2026-05-30T05:08:52Z mostra empíricamente os princípios operando como infraestrutura cognitiva.
- (ii) ADR-043 já É o ADR-raiz; ADR-045 (este) é o sucessor parcial que organiza o inventário sob essa raiz.
- (iii) É a forma operacional desta decisão — Onda B condensa `philosophy.md` (~150 linhas), Ondas C-X migram ADRs, `CLAUDE.md` mecânico já está estabilizado pós-v2.14.0.

Cada uma das 3 levanta refinamento operacional, não alternativa estrutural à decisão central.

## Gatilhos de revisão

- **Estrutura-alvo (~10-12 ADRs) revelada inadequada durante migração**: design-reviewer flag em ≥2 ondas que alguma absorção dilui carga doutrinal; charter precisa refinamento. Refinar sequence ou subdividir consolidados.
- **Categoria nova emerge durante execução**: ADR futuro precisa ser criado durante a redesign por nova decisão estrutural empírica (não pelo trabalho desta redesign). Filtro de admissão aplicado mesmo em meio à reforma — se passa no filtro, ADR-046+ é legítimo.
- **Política de admissão tem falsos negativos recorrentes**: filtro classifica como "estabilizado" entendimentos que depois precisam ser reabertos como decisão reversível — sinal de calibração ruim do filtro. Refinar heurísticas.
- **Política de admissão tem falsos positivos recorrentes**: cria ADR-NN reversível para o que deveria ter ficado em `CLAUDE.md` — sinal de que o filtro é permissivo demais. Endurecer.
- **Cap de 5 ADRs no always-include de ADR-044 estourado**: vários consolidados promovidos a always-include — sinal de que estrutura-alvo precisa subdivisão hierárquica (foundational/extended).
- **Bump major v3.0.0 não documentado em release notes**: redesign está sendo encarada como continuação editorial em vez de revisão estrutural. Auditar release narrative.
- **Consumer terceiro reporta confusão pós-bump**: archive index ou redirects insuficientes; melhorar mecânica de archive cleanup na onda final.
- **Crescimento de ADRs reverter para padrão pré-redesign** (≥3 novos ADRs/mês em 3 meses pós-redesign): admission policy enforcement falhou; revisitar mecanismo (talvez precise virar gate hard em vez de prompt informativo).

## Auto-aplicação coerente per ADR-034

- **Cond 5 (sucessor parcial):** aplica primário — estende ADR-043 organizando o inventário sob a hierarquia que ele codificou; não revoga ADR-043 (que continua `Aceito`).
- **Cond 4 (categoria nova):** aplica — "consolidação editorial cross-cluster de inventário doutrinal completo como decisão estrutural" + "política de admissão como mecanismo de prevenção" são categorias conceituais novas, distintas de adendos editoriais como em Onda 3.
- **Cond 1 (decisão estrutural sem ancestral direto):** aplica — não existe ADR ancestral codificando "consolidação cross-cluster do inventário inteiro" como decisão. Onda 3 cluster index Addenda em ADR-005/-017 são **precedente operacional pontual** (pattern aplicado 2x via Addenda em ADRs específicos) mas não constituem "ancestral codificado direto" no sentido de cond 1 — ancestral direto = ADR prévio cujo conteúdo a nova decisão refina/contradiz/substitui. O precedente operacional reforça cond 4 (categoria nova mas auditável retroativamente como pattern emergente) sem caracterizar ancestral codificado.
- **Cond 2 (substitui ADR ancestral):** NÃO aplica — ADR-043 fica `Aceito`; ADR-045 estende, não substitui.
- **Cond 3 (codifica restrição externa):** NÃO aplica — decisão é interna ao processo doutrinal do plugin.

Aplicação coerente com auditoria retroativa: ADRs 035→043 (Substituição), 026→011 (sucessor parcial), 044→021 (sucessor parcial), 029→017 (sucessor parcial cluster), 030→016 (sucessor parcial lateral) seguiram o mesmo pattern de cond 5 + cond 4 quando categoria nova emergia.
