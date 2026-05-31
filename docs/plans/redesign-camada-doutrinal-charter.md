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

## Atualização pós-execução

**Ondas A+B+C+D+E+F shipped (2026-05-30 → 2026-05-31).** Acompanhamento progressivo das ondas materializadas:

| Onda | Status | Commit/PR | Substância |
|---|---|---|---|
| **A** — Foundational | ✓ | `715f455` + PR #88 (`91d3f70`) | Charter + ADR-045 + CLAUDE.md bullet |
| **B** — `philosophy.md` condensado | ✓ | `a09a16c` + PR #89 (`f758c8d`) | 5 ops § Princípios fundamentais; bifurcação (γ) plugin/consumer dissolvida |
| **C** — Migração cluster cutucadas | ✓ | `2b147ca` + PR #90 (`dbac4d6`) | ADR-046 absorve ADR-017+ADR-029; archive/ + README inicial; pattern validado |
| **D** — Migração cluster modo local | ✓ | `1500c17` + PR #91 (`cd0b533`) | ADR-047 absorve ADR-005+018+025+030; **primeiro cluster sem procedure file** (testa transferibilidade); ~58 ocorrências em 9 docs vivos; 5 findings absorvidos no /new-adr + 1 caminho-único no Bloco 3 |
| **E** — Migração cluster reviewers/curadoria | ✓ | `bf55199` + PR #92 (`2858005`) | ADR-048 absorve ADR-021+ADR-044; **calibração descendente** (2 ADRs vs 4 da Onda D); pattern auto-consistente da always-include preservado (ADR-048 não se inclui); ~11 ocorrências em 6 docs vivos; 3 findings absorvidos caminho-único no /new-adr |
| **F** — Migração cluster execução/run-plan | ✓ | `154a4f0` + PR #93 (`f55e2a4`) | ADR-049 absorve ADR-004+028+039+041; **primeira onda com refinamento editorial documentado** (ADR-037 excluído + ADR-010 preservado fora do cluster); ~19 ocorrências em 5 docs vivos com hot spot 9 em skills/run-plan/SKILL.md; 0 findings absorvíveis pré-commit (nano-flag inline); pendência registrada: Bloco 1 commitado sem doc-reviewer (violação doutrina explícita) |
| **G** — Migração cluster componentes plugin | ✓ | `d298ced` + PR #94 (`376a755`) | ADR-050 absorve ADR-008+013+015+016+023+040; **scope máximo até hoje** (6 ADRs vs 4 em D+F; 2 em C+E); **inclusão de ADR-015 vs sketch** que o omitia (segunda instância de refinamento editorial — Onda F excluiu; Onda G incluiu); 9 cross-refs em 7 docs vivos com hot spot 3 em CLAUDE.md (bullets meta-doutrinais paralelos); 4/4 blocos com doc-reviewer obrigatório invocado (pendência operacional Onda F endereçada); 7 findings absorvidos caminho-único pré-commit no /new-adr + 1 cutucada (F4 bidirecionalidade) absorvida opção (a) + 1 finding caminho-único no Bloco 3 (sub-ref categoricamente imprecisa removida); 1 captura §3.5 materializada (cobertura ausente warning conservador; AST parse OK nos 3 hooks confirma comportamento intacto) |
| **H-X** | Pendente | — | Candidatos remanescentes naturais: convenções editoriais (ADR-007+012+024+034), alinhamento/triage (ADR-009+011+026+027+038+042 com constraint always-include sobre ADR-009), discoverability/branding (ADR-037 + ?), brainstorm (ADR-036 standalone), apex meta-cluster (ADR-035+043+045+046+047+048+049+050 — opcional) |

**Calibração emergente da estrutura-alvo** (per ADR-046 § Trade-offs):

- **Sketch original era subestimativa** — cutucadas saiu como cluster próprio standalone (vs sub-cluster de "ADR-004-skill-alinhamento-triage" absorvendo 8 ADRs no sketch).
- **Target realista 13-15 consolidados** em vez de 11 — refinamento editorial per ADR-045 fronteira *"ajuste editorial do charter vs revisão de ADR-045"* (operador escolheu opção a — aceitar 13-15 como target realista após cutucada). Spírito da consolidação (45 → ~13-15, redução de ~65-70%) preservado.
- **Cada onda contribui para refinamento incremental do sketch** — charter é artefato vivo. Pattern para ondas D-X: descoberta empírica de cluster shape é editorial (não estrutural); revisão de ADR-045 só se cluster sequence falhar materialmente.

**Pattern de migração validado empíricamente na Onda C** (template para D-X) — reaplicado e estendido na Onda D:

- ✓ Archive + redirect header canonical (blockquote `> **ARCHIVED <data>**` + cross-ref + H1 original preservado) — reaplicado em 4 ADRs.
- ✓ Archive index incremental — estendido com 4 linhas D (paralelo às 2 da Onda C).
- ✓ Cross-refs em docs vivos atualizados — escala ~5× maior (~58 ocorrências em 9 docs vs ~12 em 5 na Onda C).
- ✓ Link rot em ADRs imutáveis aceito como categoria histórica.
- ✓ Procedure preservation per ADR-024 — **NÃO aplica em Onda D** (cluster sem procedure pré-existente); F9 fronteira só ativa quando procedure pré-existe.
- ✓ Cond 5 primária isolada em auto-aplicação — F4 lesson Onda C reaplicada literal (cond 4 NÃO aplica; cond 1 NÃO aplica).
- ✓ Cond 2 refinada na Onda D (F4 do design-reviewer absorvido): "absorção consolidatória" (preserva substância integralmente) vs "revogação" (inverte doutrina central; ex.: ADR-043 → ADR-035). Pattern editorial para ondas E-X.

**Saldo inventário pós-Onda G:** 50 ADRs criados (001-050) - 18 arquivados (017, 029, 005, 018, 025, 030, 021, 044, 004, 028, 039, 041, 008, 013, 015, 016, 023, 040) = **32 vigentes**. Drop líquido de 5 nesta onda (maior drop até hoje; alinha com scope máximo do cluster — 6 absorvidos em 1 consolidado). Trajetória esperada para target 13-15 em 3-5 ondas adicionais.

### Refinamento editorial documentado (Ondas F + G — pattern emergente bidirecional)

**Onda F** estabeleceu refinamento editorial por **exclusão** vs sketch literal (Ondas C+D+E seguiram sketch literal):

- **(a) Exclusão de ADRs semanticamente desalinhados** do sketch original — ADR-037 (README framing) excluído do cluster execução/run-plan por pertencer semanticamente a discoverability/branding. Sketch agrupou por proximidade numérica, não coesão semântica. Refinamento corrige sem revisão estrutural de ADR-045 § Decisão parte 1.
- **(b) Preservação de ADRs ancestrais fora do cluster** quando categoria conceitual distinta justifica standalone — ADR-010 (progress display Task tool) NÃO absorvido apesar de ser decisão base de ADR-039. Categoria distinta com potencial consumers futuros além de `/run-plan`. Charter sketch tinha contradição interna (ADR-039 listado em 2 clusters); resolução favorece preservar categoria distinta de ADR-010.

**Onda G** aplicou refinamento editorial por **inclusão** vs sketch literal:

- **(c) Inclusão de ADRs omitidos do sketch** quando coesão semântica de família justifica — ADR-015 (hook block_env por sufixo `.env`) **incluído** apesar de omitido no sketch original do cluster componentes plugin (5 ADRs listados; ADR-015 omisso aparentemente por descuido editorial). ADR-040 § Origem explicitamente cita ADR-015 como "ancestral direto — primeiro PreToolUse block hook do plugin"; excluir deixaria órfão um membro da família coesa de 3 hooks defensivos (block_env + block_gitignored + block_settings_drift). Inclusão cabe em ADR-045 § Decisão linha 56 fronteira *"absorção de ADR em consolidado diferente do sketch original"* como ajuste editorial — categoria livre durante execução das ondas.

**Sinal a observar para ondas H-X:** 2 instâncias de refinamento editorial (Onda F exclusão; Onda G inclusão) ainda cabem em ADR-045 § Decisão linha 56 como ajustes editoriais individuais. Se 3ª aplicação aparecer em Ondas H-X, considerar se merece codificação explícita via ADR sucessor de ADR-045 (gatilho de revisão do próprio ADR-045). Por ora, decisões editoriais por onda continuam no charter; não há meta-pattern formal codificado.

### Anti-regression checklist — itens preservados em ADR-046 (Onda C), ADR-047 (Onda D), ADR-048 (Onda E), ADR-049 (Onda F), ADR-050 (Onda G)

- § Discoverability: gating tri-state ✓, 2 strings canonical ✓, dedup ✓, herança editorial ✓ (ADR-046).
- § Path contract: 3 paths suportados ✓, sintaxe ✓, regra de não-referenciar ✓, mecânica mkdir+probe+gate ✓, replicação `.claude/` ✓, `/note` 2º dispatcher com assimetria de trigger codificada ✓ (substância ADR-018 Addendum absorvida via F2 do design-reviewer), recusas cross-mode + critério "direção do leak" ✓, aceitar CLAUDE.md gitignored + cláusula OR ✓, rejeições version_files/changelog ✓ (ADR-047).
- § Reviewers: free-read curado modo híbrido ✓, threshold N=15 + modo legacy ✓, anotação `**ADRs candidatos:**` ✓, scan medium prescritivo ✓, always-include hardcoded ADR-009/-034/-043 ✓, cap nominal 5 + critério promoção ≥3 anotações ✓, reporte invariante ✓, rebatimento de não-incluídos com critério "escopo de aplicação" ✓, pontos cegos cobertos vs não-cobertos ✓, pattern auto-consistente (ADR-048 não se inclui na lista) ✓ (ADR-048).
- § Skills e fluxo: state-tracking em git/forge ✓, BACKLOG editorial sem `## Em andamento` ✓, `## Concluídos` append-only via `/run-plan §3.4` ✓, -5 mecanismos defensivos obsoletos ✓, campo `**Branch:**` opcional + probe `git symbolic-ref` + cutucada header Branch + 4 discriminações stderr ✓, Task tool 2 modos (progress display ADR-010 + state-keeping ADR-049 § Decisão (c)) com lifecycle 2-estados + marker convention `[capture:*]` ✓, `/run-plan §3.5` captura unificada cross-superfícies (pré-loop + passo 2 loop + passo 3.2 validação) ✓, campo `**Modo:** runbook` + único valor aceito + bypass 4 dimensões + incompatibilidade dura `**Branch:** + **Modo:** runbook` + materialização Falhou ✓, pattern paralelo de 5 campos opcionais (`**Branch:**` + `**Modo:**` + `**Linha do backlog:**` + `**Termos ubíquos tocados:**` + `**ADRs candidatos:**`) com critério de promoção registrado ✓, tensões resolvidas com ADR-002 + ADR-010 (preservados vigentes) ✓ (ADR-049).
- § Componentes do plugin: skills/agents/hooks como tipos canônicos ✓, naming convention (skills geradoras stack-agnósticas via sub-blocos por marker; hooks suffixados + auto-gating triplo) ✓, single source of truth para idioms (substância de ADR-008 que ADR-019 cita preservada via cross-ref) ✓, CI lint mínimo como categoria distinta das 3 vetadas (4 critérios cumulativos; cobertura positiva/negativa explícita; frase canonical preservada intacta) ✓, 3 hooks PreToolUse defensivos (block_env por sufixo `.env` universal; block_gitignored por sinal do consumer com 7 alternativas rejeitadas; block_settings_drift por content regex em settings.json) ✓, critério mecânico cumulativo `disable-model-invocation` explícito + tabela retroativa às 9 skills reproduzida literal ✓, pattern editorial "critério mecânico cumulativo" como meta-doutrina herdada (ADR-020/-022/-023 reusos preservados) ✓ (ADR-050).
- Nenhuma carga doutrinal perdida em qualquer onda; gap `block_gitignored.py` (NOTES 2026-05-30T05:26:59Z) preservado como Limitação em ADR-050 § Limitações (endereçamento pendente; reservado espaço de extensão — anteriormente em ADR-047 antes da Onda G).

### Pendência operacional registrada (Onda F) — endereçada na Onda G

**Bloco 1 commitado sem invocação do doc-reviewer** (Onda F) — violação direta de doutrina explícita em `skills/run-plan/SKILL.md` § "## O que NÃO fazer" linha "Não pular revisor, mesmo em bloco trivial". Mitigação pós-fato em Onda F: Read manual + critérios 2-3 do plano confirmaram format archive correto. Lição operacional para ondas G-X: aderir estrito ao reviewer-per-bloco mesmo quando pattern editorial é convergente.

**Onda G endereçou a pendência:** 4/4 blocos (Bloco 1 archive + Bloco 2 hot spot + Bloco 3 docs auxiliares + bloco extra §3.5) invocaram doc-reviewer obrigatório antes do commit. Convergência empírica em 5 ondas (C+D+E+F+G) não admitiu exceção à doutrina explícita. Lição internalizada — pattern operacional para Ondas H-X.
