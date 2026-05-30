# Plano — Redesign da camada doutrinal (charter)

## Contexto

**ADRs candidatos:** ADR-043 (apex doutrinal vigente, este charter codifica sucessor parcial), ADR-034 (critério adendo vs novo ADR, estendido pela admission policy), ADR-024 (categoria `docs/procedures/`, preservada), ADR-009 (design-reviewer pré-fato, preservado), ADR-011 (wiring automático, preservado), ADR-021 (curadoria free-read, preservado), ADR-044 (scan medium + always-include, preservado), ADR-035 (referência histórica de exceção interna ao YAGNI, já Substituído por ADR-043), ADR-036 (exemplo de Ockham operacionalizado puro — invertido).

**Linha do backlog:** plugin: **redesign da camada doutrinal** — consolidar 45 ADRs em ~10-12 temáticos sob hierarquia invertida pós-v2.14.0 + condensar `philosophy.md` (princípios + mapping operacional + ≥3 pattern como condição geral de YAGNI terminar; cortar § Codificação estrutural overhead) + codificar **política de admissão going forward** (*"isto é decisão reversível ou entendimento estabilizado?"*) como mecanismo de prevenção de re-acúmulo.

A camada doutrinal do toolkit (`philosophy.md` + 45 ADRs em `docs/decisions/` + cross-refs em `CLAUDE.md`/skills/agents) cresceu via refinamento incremental sem consolidação periódica desde o início do projeto. O estado pós-v2.14.0 confirma estabilização semântica (Verdade/Excelência/Ockham operando como *thinking-with* em decisões internas — sinal empírico registrado em NOTES 2026-05-30T05:08:52Z e replicado nesta sessão) e operacional (free-read curado via ADR-044). A janela é propícia para refazer a camada com o conhecimento acumulado, mantendo o mecanismo (skills/agents/hooks/`CLAUDE.md` como contrato) intocado.

**Inversão do ônus da prova aceita** durante sessão `tres-principios` (toolkit 2026-05-30): a estrutura é empiricamente desordenada (acumulação ≠ design); os 3 princípios aplicados ao próprio inventário endossam consolidação. **Verdade** nomeia a desordem; **Excelência** aplica o padrão do mecanismo à doutrina; **Ockham** — se ~10-12 ADRs temáticos carregam mesma carga que 45 fragmentados, versão enxuta é melhor por construção (ônus passa para mostrar perda de carga doutrinal, não ganho de organização).

**Precedente empírico no projeto:** Onda 3 cluster index Addenda em ADR-005 (modo local) e ADR-017 (cutucadas) são provas de conceito do mesmo movimento aplicado a 2 clusters; esta redesign generaliza para o inventário inteiro.

**Convergência empírica entre 2 ângulos:** crítica externa (web chat Claude turno 4) — *"ADRs como memória de trabalho, não registro de decisões"* — rima com observação independente de NOTES 2026-05-30T05:08:52Z — *"princípios funcionam como thinking-with, não labeling-against"*. Os ADRs estão fazendo função dupla; o toolkit não desenhou a linha; **política de admissão going forward** é essa linha.

**Arco completo da conversa que produziu a direção** + sketch detalhado da estrutura-alvo (11 ADRs) + anti-regression checklist completo + intent da prevenção + 8 riscos identificados: ler `.claude/local/NOTES.md` entry 2026-05-30T06:08:04Z. Este charter materializa decomposição operacional; NOTES carrega substância da decisão.

## Resumo da mudança

**Escopo desta Onda A (charter):**

1. **Charter plan** (este arquivo) — documenta decomposição da redesign em ondas B-X subsequentes, **anti-regression checklist** como critério de sucesso operacional cross-onda, e cross-refs aos artefatos foundational. Vive como documento de referência durante toda a redesign; atualizado progressivamente quando cada onda fecha.

2. **Meta-ADR (ADR-045 no inventário atual; conceitualmente ADR-011 da nova estrutura-alvo)** — sucessor parcial de ADR-043 codificando: (a) decisão de consolidar 45 ADRs em ~10-12 temáticos sob hierarquia invertida; (b) **política de admissão going forward** — filtro mecânico para novos ADRs com 3 saídas (ADR reversível / `CLAUDE.md` ou `philosophy.md` / git log); (c) sketch da estrutura-alvo preservada como § Implementação; (d) reconhecimento explícito de ADR-043 como ancestral que ESTE ADR não revoga (estende o trabalho dele para o inventário). Criado por `/triage` step 4 via delegação a `/new-adr`.

3. **`CLAUDE.md` § Editing conventions** — bullet cross-ref a ADR-045 no padrão dos bullets meta-doutrinais existentes (ADR-010/-011/-023/-026/-034/-043). Executado como Bloco 1 deste plano via `/run-plan` (não consolidado no commit do `/triage` para preservar a unitariedade do mecanismo de execução — operador escolheu o caminho-com-plano-padrão sobre o caminho-Onda-1-style para validar /run-plan em multi-onda longo).

**Decomposição prevista para ondas subsequentes** (NÃO escopo desta onda — cada onda terá seu próprio `/triage` downstream):

- **Onda B** — `philosophy.md` condensado em ~150 linhas: cortar § Codificação estrutural (overhead editorial identificado durante crítica externa); promover critério 4 do § Ockham operacionalizado (≥3 pattern emergente) como condição geral de quando YAGNI termina (de internal-plugin a regra universal, já conceitualmente preparado em ADR-043 § Universalidade); manter triangulação, mapping, audience-aware framing; opcionalmente codificar ordem operacional Verdade→Ockham→Excelência com Ockham veto como rubric procedimental para reviewers.

- **Ondas C-X** — migração de ADRs por cluster temático. Cada onda absorve 3-6 ADRs antigos em 1 consolidado, atualiza cross-refs em skills/agents/`CLAUDE.md`, arquiva os antigos sob `docs/decisions/archive/` com mensagem de redirect (`# ADR-NNN: ARCHIVED — content absorbed into ADR-MMM in new structure`). Cluster sequence sugerida (sujeita a refinamento per ondas anteriores): componentes plugin → path contract & roles → modo local → alinhamento (`/triage` + reviewer pré-fato) → execução (`/run-plan`) → reviewers curadoria → convenções editoriais → trade-offs vivos isolados → bridge & discoverability → instrumentação progresso → meta-ADR apex (este, renumerado).

- **Onda final** — admission policy enforcement em `/new-adr` (step novo surfacing do filtro como prompt informativo antes da criação); archive index em `docs/decisions/archive/README.md`; propagação final de cross-refs cross-skills/agents; bump major **v3.0.0** com /release dedicado.

Cada onda subsequente é seu próprio `/triage` downstream → `/run-plan` ou `/new-adr` per artefato. Esta Onda A é multi-artefato em commit único (parcialmente — plano + ADR via /triage step 5; CLAUDE.md via /run-plan Bloco 1).

**Decisões prévias confirmadas (sem bifurcação no /triage):**

- ADR-045 carrega admission policy em § Decisão integrada (NÃO ADR separado) — admission policy É parte do redesign decision; codificar redesign sem codificar prevenção deixaria gap.
- ADRs antigos serão **arquivados** sob `docs/decisions/archive/`, NÃO deletados — preserva trilha empírica acessível + permite link rot mitigation via redirects estruturados.
- Bump **major v3.0.0** esperado — redesign justifica major semver mesmo com mecanismo preservado; audience-aware framing pra consumer terceiro que faz `/plugin update` precisa do sinal estrutural.
- ADR-045 mantém numeração atual (próximo na sequência); renumeração para ADR-011 da nova estrutura acontece durante a última onda de migração (parte do archive + redirect propagation).

## Arquivos a alterar

### Bloco 1 — CLAUDE.md § Editing conventions {reviewer: doc}

- `CLAUDE.md`: adicionar bullet "Redesign da camada doutrinal" na seção `## Editing conventions`, posicionado adjacente ao bullet existente "Hierarquia doutrinal" (cross-ref a ADR-043). Padrão paralelo aos bullets meta-doutrinais existentes (ADR-010/-011/-023/-026/-034/-043/-044). Texto sugerido (refinar pelo doc-reviewer no Bloco 1 se necessário): "**Redesign da camada doutrinal**: consolidar 45 ADRs em ~10-12 temáticos sob hierarquia invertida + codificar política de admissão going forward (filtro decisão reversível vs entendimento estabilizado) per [ADR-045](docs/decisions/ADR-045-<slug-from-new-adr>.md) — sucessor parcial de ADR-043 que estende o trabalho da hierarquia invertida para o inventário, codificando a estrutura-alvo da camada doutrinal e o mecanismo de prevenção de re-acúmulo. Ondas B-X migram conteúdo per `docs/plans/redesign-camada-doutrinal-charter.md`."

## Verificação end-to-end

**Critério de sucesso desta Onda A:**

1. Charter (este arquivo) commitado em `docs/plans/` via /triage step 5.
2. ADR-045 criado por `/new-adr` (delegado por /triage step 4); § Decisão integra redesign + admission policy; § Implementação inclui sketch da estrutura-alvo (referência ao mapping em NOTES); design-reviewer auto-fire valida sem findings de cutucada (ou com findings absorvidos).
3. Bloco 1 (CLAUDE.md edit) executado por `/run-plan` em onda separada (ou inline pós-/triage se operador preferir collapse manual); doc-reviewer valida bullet sem drift cross-doc.
4. Commit message do /triage estruturado com seção `## design-reviewer findings absorvidos` (mirror em § Decisões absorvidas) se há findings absorvidos pré-commit.
5. Push do branch ocorre como unidade atômica com commit (per /triage step 5 caminho-com-plano).

**Anti-regression checklist** (carga doutrinal que NÃO pode ser perdida em ondas subsequentes — material consolidado de NOTES 2026-05-30T06:08:04Z; consultado por design-reviewer em cada onda C-X para flagrar se alguma absorção dilui carga):

*Princípios e doutrina apex:*
- 3 princípios fundamentais (Verdade, Excelência sem over-engineering, Navalha de Ockham) como raiz epistêmica
- Triangulação (3 condições atuam juntas; isoladas deteriora cada uma)
- Mapping fundamentais → pragmáticos (YAGNI/flat ↔ Ockham; sem defensividade ornamental ↔ Verdade; pragmática sem aspiracional schema-perfeição ↔ Excelência)
- 4 critérios de Ockham operacionalizado (incidente recorrente, fronteira doutrinal borrada, contradição/refinamento, ≥3 pattern emergente) — generalizados na Onda B para regra de quando YAGNI termina
- Universalidade do princípio (mesma instância em código consumer e doutrina plugin, vocabulário diferente)
- Polaridade default-restritiva (consumer) vs default-condicional (plugin) como **consequência** da entidade ponderada
- Brainstorm intencionalmente não-codificado como skill (raw-chat cobre — exemplo apex de Ockham puro)

*Path contract e mecanismo:*
- Tabela de roles + canonical defaults + role contract
- Resolution protocol 4-step (probe canonical → consultar `CLAUDE.md` → ask operator tri-state → memoization offer)
- Required vs informational distinction
- 3 default behavior tracks para required absent (capturar+stop; oferta canonical via enum; inform+stop)
- Drift detection (canonical existe + `CLAUDE.md` declara diferente)
- Local mode (mkdir + probe gitignore + gate Gitignore + recusa cross-mode + regra de não-referenciar)
- Sub-fluxo de criação canonical via enum

*Componentes do plugin:*
- Skills/agents/hooks como tipos canônicos
- Naming canonical (`<verb>` quando artefato emerge da decisão; `<verb>-<artifact>` quando fixo; skills geradoras stack-agnósticas)
- Auto-gating triplo de hook (file extension → stack marker → toolchain)
- `disable-model-invocation` critério mecânico cumulativo
- `block_gitignored` hook + gap recém-descoberto (NOTES 2026-05-30T05:26:59Z) — endereçamento pendente, NÃO consolidar como decidido na redesign; reservar espaço de extensão em ADR consolidado equivalente de componentes/hooks (estrutura-alvo descobrível durante migração per ADR-045 § Implementação)

*Skills e fluxo:*
- `/triage` decision tree (linha backlog / plano / ADR / domain update / design notes)
- `/run-plan` worktree + micro-commit + reviewer per bloco + gate final + captura automática + runbook mode opt-in
- `/new-adr` (template + numeração inferida + design-reviewer auto-fire)
- `/next` ranking (alinhamento × amplitude)
- `/debug` reprodução antes de hipotetizar
- `/note` cross-project write + informational store
- `/release` commit local + tag annotated + sem push automático
- `/init-config` + recusa cross-mode

*Reviewers:*
- 5 reviewers shippados (code, qa, security, doc, design)
- design-reviewer dispara automaticamente em `/triage` e `/new-adr` (ADR-011 antigo wiring)
- Critério de absorção de findings (3 condições; default conservador cutucar)
- Free-read curado (anotação + always-include + scan medium; threshold N=15)
- Read defensivo antes de análise
- Reviewer report idioma (espelha consumer)
- Mirror de Decisões absorvidas runtime (ADR-038 antigo)

*Convenções editoriais:*
- Idioma por audiência (3 categorias: prosa operativa, artefatos informativos, discoverability)
- Convenção de commits (espelhar projeto consumidor; default Conventional Commits)
- Convenção de naming
- Adendo vs novo ADR (5 condições para novo; 4 para adendo) — base do filtro de admission policy generalizado
- AskUserQuestion mechanics (header ≤12 chars; 2-4 opções; trade-off em description; Recommended só com default estável; unificação preferida sobre sequência)
- Instrumentação de progresso multi-passo via Tasks

*Discoverability e bridge:*
- Cutucada uniforme em skills com `roles.required` (2 strings canonical; gating tri-state; dedup conversation-scoped)
- Herança editorial para nova SKILL traversa step 3
- `/note --to` cross-project write
- `$PROJECTS_DIR` discovery + absolute-path fallback
- Categoria `docs/procedures/` para procedimentos compartilhados

*Trade-offs vivos e reversíveis (especificamente — categoria que sobrevive como ADR clássico):*
- Issue-first GitLab via campo `**Branch:**` opcional no plano (ADR-002 + ADR-028 antigos)
- Block-gitignored manter no consumer, não plugin (ADR-016 antigo)
- Main único (ADR-014 antigo)
- Modo runbook opt-in via campo `**Modo:**` (ADR-041 antigo)
- Mirror de decisões absorvidas (ADR-038 antigo)

*Gatilhos de revisão por categoria* — cada decisão preservada mantém suas condições de reabertura empíricas (NÃO descartar; são o que distingue "decisão deliberada" de "regra arbitrária"). Pode consolidar gatilhos por consolidação de ADR (vários gatilhos relacionados num só `## Gatilhos de revisão` do consolidado), mas a substância (quando reabrir?) deve sobreviver inteira.

**Validação operacional do checklist em ondas C-X:** cada onda de migração compara o content da consolidação contra a categoria relevante do checklist; design-reviewer aplica o checklist como rubric extra além do scan padrão; se algum item não tem lar claro na nova estrutura ao final da migração, redesign está incompleta e onda final inclui passo de retrofit.

## Verificação manual

Não aplica para esta Onda A — produtos são doc-only (charter + ADR + CLAUDE.md bullet pendente). Validação manual emerge nas ondas que tocam mecanismo runtime (Onda final, quando admission policy é enforced em `/new-adr`).

## Notas operacionais

**Ordem dos blocos:** Bloco 1 (CLAUDE.md edit) executado por `/run-plan` em onda separada (não inline neste /triage commit). Cria 2 commits separados:
1. /triage commit: plano + ADR-045 + push (caminho-com-plano padrão).
2. /run-plan commit (futuro): edit do CLAUDE.md (single block) + push.

Alternativa (operador pode escolher manual): collapse manual num único commit pós-/triage. Não recomendado para Onda A — preferir testar o pipeline canonical em ondas longas.

**Cross-refs propagação deferida:** Onda A não atualiza cross-refs nas skills/agents/`philosophy.md` apontando para ADRs antigos — propagação acontece durante ondas C-X conforme cada ADR antigo é absorvido. Esta onda apenas estabelece a referência foundational (`CLAUDE.md` → ADR-045).

**Risco a vigiar nesta onda:** ADR-045 sendo o caminho preferido pra "achei interessante essa observação, vai virar refinamento de ADR-045" — recursão. Mitigação registrada em NOTES + codificada em ADR-045 § Limitações: ADR-045 é **congelado** depois da redesign; refinamento de doutrina pós-redesign segue o filtro normal (admission policy aplicada).

**Pós-merge:** atualizar BACKLOG umbrella line marcando Onda A shippada (paralelo aos updates progressivos das Ondas 1-2-3-4 da reforma doutrinária); `/triage` subsequente para Onda B (`philosophy.md` condensado).

**Cap de ondas:** estimativa 6-10 ondas (incluindo esta A); revisitar em meio à migração se cluster sequence mudar.

**Sinal de saúde:** se 2 ondas consecutivas precisarem absorver ≥10 findings cada do design-reviewer (cutucadas ou absorções), pausar redesign e revisitar charter — sinal de que a estrutura-alvo precisa refinamento.

## Decisões absorvidas

- § Origem (ADR-045): bullet "Convergência empírica independente" adicionado ancorando NOTES 2026-05-30T05:08:52Z (caminho-único).
- § Origem (ADR-045): bullet "Plano coordenador" adicionado anunciando este charter como par operacional (caminho-único).
- § Decisão parte 2 (ADR-045): bloco "Critério de desempate na zona cinzenta" adicionado (3 heurísticas: `CLAUDE.md` vs `philosophy.md`; não-ADR vs git log; reversibilidade positiva substituindo critério circular) (caminho-único).
- § Decisão parte 2 (ADR-045): "Condição de validade do enforcement" adicionada — política não shippada sem enforcement em ≥1 superfície runtime; bump v3.0.0 condiciona (caminho-único).
- § Decisão parte 2 Risco a vigiar (ADR-045): cross-ref a § Gatilhos "Categoria nova emerge durante execução" adicionado (caminho-único).
- § Decisão parte 1 (ADR-045): parágrafo "Fronteira 'ajuste editorial do charter' vs 'revisão de ADR-045'" delimitando o que é mutável editorial vs o que vincula formalmente (caminho-único).
- § Razões (ADR-045): justificativa bump v3.0.0 ampliada com trade-off de signaling explicitado (minor + release note destacada rebatido por assimetria de discovery) (caminho-único).
- § Alternativa (e) (ADR-045): redação do descarte reescrita removendo minimização de ADR-043 ("apenas substituiu ADR-035"); argumento real é escopo distinto + 2 categorias operacionais novas não comportáveis em adendo (caminho-único).
- § Mitigações (ADR-045): bullet "Anti-regression checklist só pode crescer" adicionado — remoção exige justificativa explícita no commit (caminho-único).
- § Auto-aplicação cond 1 (ADR-045): "aplica parcial" → "aplica" com esclarecimento que precedente operacional pontual de Onda 3 reforça cond 4 mas não constitui ancestral codificado direto no sentido de cond 1 (interpretação divergente da sugestão do reviewer — rationale: ADR-034 cond 1 fala em ancestral direto que conota ADR codificado; cond 4 captura novidade reforçada pelo precedente) (caminho-único).
- Charter linha 87 (este arquivo): forward-reference "ADR-001 consolidado" trocada por "ADR consolidado equivalente de componentes/hooks" preservando flexibilidade da estrutura-alvo descobrível durante migração (caminho-único).
