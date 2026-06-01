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

**Cap de ondas:** estimativa 6-10 ondas (incluindo esta A); revisitar em meio à migração se cluster sequence mudar. **Recalibrado pós-Onda K (2026-06-01):** target empírico **23-25 ADRs final** em ~3-4 ondas adicionais (K' editorial canonical templates + L discoverability/branding + Promoção II tactical-only + opcional M foundational templates), com **apex meta-cluster SKIP recomendado** per NOTES *"risco alto auto-referência"* + auto-referência problemática (ADR-045 absorvido por consolidado que ele autorizou). Substitui projeção sketch original 13-15 por evidência empírica pós-auditoria mecânica do inventário 27 entradas (= 26 vigentes substantivos + ADR-035 Substituído preservado in-place per ADR-045 § Decisão parte 1).

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

**Ondas A+B+C+D+E+F+G+H + ADR-052 + Onda Promoção + Onda I + Onda J shipped (2026-05-30 → 2026-06-01).** Acompanhamento progressivo das ondas materializadas:

| Onda | Status | Commit/PR | Substância |
|---|---|---|---|
| **A** — Foundational | ✓ | `715f455` + PR #88 (`91d3f70`) | Charter + ADR-045 + CLAUDE.md bullet |
| **B** — `philosophy.md` condensado | ✓ | `a09a16c` + PR #89 (`f758c8d`) | 5 ops § Princípios fundamentais; bifurcação (γ) plugin/consumer dissolvida |
| **C** — Migração cluster cutucadas | ✓ | `2b147ca` + PR #90 (`dbac4d6`) | ADR-046 absorve ADR-017+ADR-029; archive/ + README inicial; pattern validado |
| **D** — Migração cluster modo local | ✓ | `1500c17` + PR #91 (`cd0b533`) | ADR-047 absorve ADR-005+018+025+030; **primeiro cluster sem procedure file** (testa transferibilidade); ~58 ocorrências em 9 docs vivos; 5 findings absorvidos no /new-adr + 1 caminho-único no Bloco 3 |
| **E** — Migração cluster reviewers/curadoria | ✓ | `bf55199` + PR #92 (`2858005`) | ADR-048 absorve ADR-021+ADR-044; **calibração descendente** (2 ADRs vs 4 da Onda D); pattern auto-consistente da always-include preservado (ADR-048 não se inclui); ~11 ocorrências em 6 docs vivos; 3 findings absorvidos caminho-único no /new-adr |
| **F** — Migração cluster execução/run-plan | ✓ | `154a4f0` + PR #93 (`f55e2a4`) | ADR-049 absorve ADR-004+028+039+041; **primeira onda com refinamento editorial documentado** (ADR-037 excluído + ADR-010 preservado fora do cluster); ~19 ocorrências em 5 docs vivos com hot spot 9 em skills/run-plan/SKILL.md; 0 findings absorvíveis pré-commit (nano-flag inline); pendência registrada: Bloco 1 commitado sem doc-reviewer (violação doutrina explícita) |
| **G** — Migração cluster componentes plugin | ✓ | `d298ced` + PR #94 (`376a755`) | ADR-050 absorve ADR-008+013+015+016+023+040; **scope máximo até hoje** (6 ADRs vs 4 em D+F; 2 em C+E); **inclusão de ADR-015 vs sketch** que o omitia (segunda instância de refinamento editorial — Onda F excluiu; Onda G incluiu); 9 cross-refs em 7 docs vivos com hot spot 3 em CLAUDE.md (bullets meta-doutrinais paralelos); 4/4 blocos com doc-reviewer obrigatório invocado (pendência operacional Onda F endereçada); 7 findings absorvidos caminho-único pré-commit no /new-adr + 1 cutucada (F4 bidirecionalidade) absorvida opção (a) + 1 finding caminho-único no Bloco 3 (sub-ref categoricamente imprecisa removida); 1 captura §3.5 materializada (cobertura ausente warning conservador; AST parse OK nos 3 hooks confirma comportamento intacto) |
| **H** — Migração cluster convenções editoriais | ✓ | `f0dbcb2` + PR #95 (`7991fdb`) | ADR-051 absorve ADR-007+012+024 (3 ADRs vs 4 do sketch); **ADR-034 preservado vigente** fora do cluster por **constraint mecânico** (hardcoded na always-include de ADR-048) + categoria semântica distinta (meta-doutrina apex); **3ª instância de refinamento editorial — gatilho de revisão de ADR-045 disparado** (Onda F exclusão + Onda G inclusão + Onda H preservação por constraint); 12 cross-refs em 9 docs vivos (vs 8 estimados no plano — 4 gaps adicionais descobertos no Bloco 3 via F1 reviewer + grep final: CLAUDE.md:83 + CLAUDE.md:112 + skills/new-adr:55 + skills/triage:169); 3/3 blocos com doc-reviewer obrigatório (invariante 6 ondas consecutivas); 2 findings absorvidos caminho-único no /new-adr (F1 trade-off migração retroativa CHANGELOG; F2 invariante cross-ref bilateral ADR-001↔ADR-051) + 1 F3 informativo registrado (fragment-link user-facing README); F2 Bloco 1 absorvido per precedente Ondas C-G (link interno em ADR-024 archived; "body verbatim" aceito); F1 Bloco 3 expandido para 4 gaps consistência editorial — todos caminho-único |
| **ADR-052** — Meta-pattern editorial (entre H e I) | ✓ | `7d26dc8` + PR #96 (`fdba1aa`) | Sucessor parcial primário de ADR-045 (per ADR-034 cond 5) promovendo 3 modos editoriais emergentes (F+G+H) para meta-pattern canonical com critério mecânico verificável: (a) EXCLUSÃO + (b) INCLUSÃO + (c) PRESERVAÇÃO POR CONSTRAINT MECÂNICO PURO. NÃO é onda de migração — meta-decisão editorial apex pontual em resposta ao gatilho disparado pós-Onda H. Operador escolheu Opção B (codificação preventiva) sobre Opção A (status quo) e Opção C (aguardar 4ª instância). 3 findings absorvidos no /new-adr (F1 justificativa cond 4 reforçada; F2 opção (A) — modo (c) restrito a constraint mecânico puro, sub-caso 2 colapsado em modo (a) bullet 2; F3 linguagem "promove" vs "cabem dentro"); 1 bloco (CLAUDE.md bullet) com doc-reviewer 0 findings; +1 ADR no inventário (primeiro acréscimo líquido desde Onda A) |
| **Onda Promoção** — Batch promotion 7 consolidados Proposto → Aceito (entre ADR-052 e I) | ✓ | `0548130` (plano) + `8ab6a8f` (Bloco 1) + `0c06bde` (captura §3.5) + PR #97 (`c614d6c`) | Tactical-only onda dedicada pré-Onda I gating por F10 cutucada absorvida na sessão de /triage Onda I. 7 ADRs consolidados (ADR-046+047+048+049+050+051+052) promovidos de Status: Proposto → Aceito em batch. Critério de promoção (4 cumulativos): shipped + effective + referenciado como autoridade + sem Substituído marker. Auto-bootstrap mecânico: ADR-052 (definidor do critério modo (c)) e ADR-048 (alvo da verificação mecânica) promovidos juntos sem circularidade lógica. NÃO é onda de migração — promoção formal alinha Status com state real (effective em produção há semanas, referenciado por CLAUDE.md/skills/agents como autoridade). 6 findings absorvidos caminho-único no /triage (awk semântico; verificação inversa drift transversal; nota limiar critério 3 ADR-052; substituição cross-ref antecipada; refinamento tactical-only; nota auto-bootstrap); 1 captura §3.5 materializada (critério 6 lexical bug — `grep "Substituído"` falso-positivo casando narrativa histórica em § Origem; refinamento para `^\*\*Status:\*\*` registrado); 1 bloco principal + 1 bloco extra captura ambos com doc-reviewer 0 findings. Saldo inventário pós-promoção: 31 vigentes preservado (zero archived, zero novos); apenas Status formal alinha com state real. Pós-merge: critério mecânico de ADR-053 § Decisão (c) sobre ADR-009 via ADR-048 passa a ser estritamente satisfeito — pré-condição para Onda I retomar (branch `onda-i-draft-pending-promotion` aguardando rebase + re-validação F10) |
| **I** — Migração cluster alinhamento/triage | ✓ | `9540a8f`+`3292242` (draft) → PR #98 (`104a24a`); `1c9cd9a`+`4b3ce06`+`344c5ab` (execução) → PR #99 (`8b86960`) | **Sétima migração cluster** da redesign. ADR-053 absorve ADR-011+026+027+038 (4 dimensões a-d: /draft-idea upstream + wiring design-reviewer + critério mecânico absorção + mirror runtime). **Primeira aplicação formal de ADR-052 com 2 modos simultâneos:** modo (c) sobre ADR-009 (constraint mecânico hardcoded ADR-048 always-include); modo (a) bullet 1 sobre ADR-042 (desalinhamento semântico do sketch); modo (a) bullet 2 sobre ADR-031 (categoria semântica distinta sem constraint mecânico). **Pattern editorial inédito:** /triage gerou draft em branch dedicado pré-promoção (F10 cutucado revelou gap mecânico de ADR-052 § (c) sobre Proposto-shipped); Onda Promoção precedeu (PR #97); rebase + re-validação automática pós-promoção; PR #98 mergeou plan+ADR; /run-plan executou em worktree separada (3 blocos doc-reviewer 0 findings cumulativos: archive 4 ADRs + extensão archive index 25 linhas; 10 substituições hot spot mecanismo skills/agents incluindo F4 ADR-035→ADR-043 em code-reviewer.md:64 evitando drift Frankenstein; 5 substituições foundation+templates mistura categorial intencional per F6). Cutucadas F4/F6/F9 absorvidas durante /triage; F10 resolvida automaticamente pós-Onda Promoção. Saldo: 28 vigentes (52+1 criados - 25 archived; net -3 nesta onda completa: ADR-053 criado, 4 ADRs archived). |
| **J** — Migração cluster bridge cross-project | ✓ | `5aa5abd` (plan + ADR-054) + PR #100 (`1aa7933`) [`12b350f` archive + `cca8192` skills + `ab90770` foundation + `e09b833` captura §3.5] | **Oitava migração cluster** (décima onda total). ADR-054 absorve ADR-032+ADR-042 (2 dimensões a+b: skill /note foundational + store doutrinário non-role + flag --to cross-project write + discovery $PROJECTS_DIR + pré-condição target inicializado + blast-radius preserved + critério contrato-declarado-vs-heurística). **Calibração mínima — primeira onda pós-codificação de ADR-052 sem aplicação formal de modos a/b/c** (sketch literal aplicado; 2 ADRs absorvidos cleanly; pendência editorial de ADR-042 preservado standalone desde Onda I encerrada). Cross-ref para ADR-047 § Decisão como autoridade vigente da invariante `.worktreeinclude` preservada. 2 findings absorvidos caminho-único no /new-adr (F1 restauração da distinção gate Gitignore/Worktree replication; F2 expansão nota histórica ADR-035→ADR-043 mapping critérios homólogos) + 5 absorvidos no /triage (F1 typo shell + F2 invariante reviewer-per-bloco "10 instâncias" + F3 critério 3 ambiguidade temporal + F6 consolidação cite CLAUDE.md F6 Ockham + F7 nota obsoleta slug) + 1 cutucada F3 § Cap de ondas absorvida opção (a) reduzir escopo da projeção; 4/4 blocos com doc-reviewer 0 findings; 1 captura §3.5 (critério 6.4 typo lexical "contrato-declarado" vs "contrato declarado" canonical paralelo à captura de Onda Promoção). Saldo: **27 vigentes** (53+1 criados - 27 archived; drop líquido de 1; calibração mínima paralela a Onda E). |
| **K** — Auditoria do inventário vigente (tactical-only paralelo a Onda Promoção) | ✓ | `899a130` (plano /triage) + `d5e6102` (cleanup pré-loop órfãos FS) + PR #101 (`17b109a`) [3 commits worktree: `7bf3dc0` Bloco 2 charter + `a11bb39` Bloco 3 BACKLOG + `e87ddcb` §3.5 captura] | **Décima primeira onda.** Auditoria mecânica 27 entradas: **26 vigentes substantivos + 1 Substituído preservado in-place (ADR-035)** — refuta saldo declarado anterior 27 vigentes (drift cross-doc cascateava NOTES + BACKLOG + charter). Mapeamento: 10 consolidados shippados (ADR-045..054) + 3 apex doutrinais standalone (ADR-009/-034/-043 hardcoded always-include ADR-048) + 3 standalone preservados por decisão de onda anterior (instâncias de preservação codificadas em ondas anteriores: ADR-010 Onda F precedente retroativamente formalizado em ADR-052 linha 87; ADR-031 Onda I via ADR-052 modo (a) bullet 2 — categoria semântica distinta sem constraint mecânico; ADR-014 precedente de forma citado por ADR-036; trade-off vivo categoria charter linha 126) + 1 Substituído (ADR-035) + 10 candidatos cluster (ADR-001/002/003/006/019/020/022/033/036/037). **Cluster sequence recalibrada:** K → K' editorial canonical templates (promovida em /triage; 4 evidências empíricas) → L discoverability/branding (ADR-037) → Promoção II tactical-only (10 candidatos com critério explícito) → opcional M foundational templates (ADR-001+033) → apex meta-cluster SKIP recomendado per auto-referência. **Pré-loop bloqueio:** 6 ADRs órfãos do FS (drive-sync ressuscitando pós-merge Ondas I+J); cleanup `systemctl --user stop drive-sync.service` + `rm` (commit `d5e6102`); captura BACKLOG. **Target empírico revisado: 23-25 ADRs final.** 7 descobertas materializadas; 7 findings doc-reviewer absorvidos caminho-único + 1 cutucada ADR-020 absorvida opção (c) preservar standalone; 3/3 blocos doc-reviewer obrigatório. |
| **K'** — Editorial canonical templates (tactical-only paralelo a Onda Promoção) | ✓ | `90b3f7f` (plano /triage) + PR #<NN> (`<hash>`) [Bloco 1 worktree: `9e4eab6` templates/plan.md + commits Bloco 2 charter + Bloco 3 BACKLOG pendentes] | **Décima segunda onda.** Refinamento de `templates/plan.md` § Verificação end-to-end com comentário HTML inline contendo 4 diretrizes canonical: (1) prefixar `^\*\*Status:\*\*` em greps de Status field; (2) preferir `git status --porcelain -- <paths>` git-based vs counts lexicais; (3) fidelidade ao texto-alvo (preservar espaços/hífens via Read antes de hardcodar grep); (4) counts como variável ou condição inversa (aplicação forward apenas — planos mergeados não tocados retroativamente). **5 evidências empíricas** do pattern lexical (Onda Promoção crit 6 `Substituído` sem prefixo Status field + Onda J crit 6.4 `contrato-declarado` com hífen + Onda K crit 1 pré-absorção `wc -l` esperando 33+27 + Onda K crit 6 pré-absorção count==27 esperado + Onda K crit 1 pós-absorção raw 27+filtrado 26 vs esperado 33+27) — Onda K crit 1 pós-absorção qualitativamente distinta (gap editorial pós-substantia cumprida vs typo lexical); "cleanup órfãos FS pré-loop" não codificado como evidência do pattern lexical (vive como item BACKLOG separado em categoria distinta — drive-sync ressuscitação pós-merge — registrado durante Onda K commit `d5e6102`). Promovida via cutucada resolvida no /triage Onda K precedendo Onda L. Tactical-only; sem ADR criado per intent + decisão /triage opção (a) + auto-aplicação cond 4 ADR-034 leitura estreita ADR-052 (sub-estrutura do eixo templates canonical sem 4º eixo conceitual). 6 findings doc-reviewer absorvidos caminho-único pré-commit no /triage + 1 cutucada count 4 vs 5 absorvida opção (a) padronizar 5 + 1 [FORTE] Bloco 1 + 1 [MÉDIO] Bloco 2 absorvidos caminho-único (§ Origem dos ADRs absorvidos → § Origem histórica canonical real); 3/3 blocos doc-reviewer obrigatório (invariante mantido). Saldo inventário 27 entradas preservado. |
| **Promoção II** — Batch promotion 10 Proposto-shipped vigentes (tactical-only) | Pendente | — | Critério explícito: **Proposto-shipped + efetivo (referenciado como autoridade em CLAUDE.md/skills/agents) + sem decisão pendente de cluster**. Candidatos: ADR-022, 031 (decidido standalone Onda I), 033, 034, 036, 037, 043, 045, 053, 054. Inclui apex doutrinais não-promovidos na Promoção I (ADR-043 + ADR-045) + consolidados Onda I+J (ADR-053 + ADR-054) + standalone preservados (ADR-031). Pattern paralelo a Onda Promoção; saldo inalterado. |
| **L** — Cluster discoverability/branding | Pendente | — | ADR-037 standalone candidato (Code-as-truth vs intent-as-truth — Product Engineer framing). Cluster pequeno; pode consolidar em 1 ADR ou permanecer standalone via ADR-052 modo (a) bullet 2 se cluster minúsculo (≤1 ADR). |
| **M (opcional)** — Cluster foundational templates | Pendente | — | ADR-001 (protocolo templates) + ADR-033 (templates single-consumer) → 1 consolidado. Saldo -1 líquido. Coesão semântica clara dentro de família templates; decisão pendente: justifica consolidação vs preservar standalone. |
| **Apex meta-cluster (Onda final)** | **SKIP recomendado** | — | Per NOTES *"risco alto auto-referência"* — ADR-045 (admission policy) seria absorvido por consolidado que ele autorizou; ADR-052 (modos editoriais) idem. Apex vive como camada vigente sem necessidade de consolidação. Reabrir SKIP se inadequação for empiricamente flagada em ondas futuras (charter § Sinal de saúde linha 154). |

**Calibração emergente da estrutura-alvo** (per ADR-046 § Trade-offs):

- **Sketch original era subestimativa** — cutucadas saiu como cluster próprio standalone (vs sub-cluster de "ADR-004-skill-alinhamento-triage" absorvendo 8 ADRs no sketch).
- **Target realista 13-15 consolidados** (projeção histórica pós-Onda C) em vez de 11 — refinamento editorial per ADR-045 fronteira *"ajuste editorial do charter vs revisão de ADR-045"* (operador escolheu opção a — aceitar 13-15 como target realista após cutucada). **Recalibrado pós-Onda K (2026-06-01)** para target empírico **23-25 ADRs final** com base em auditoria mecânica do inventário 27 entradas (= 26 vigentes substantivos + ADR-035 Substituído preservado in-place); ver § Cap de ondas linha 152 e tabela § Atualização pós-execução linha 188 para projeção empírica detalhada. Spírito da consolidação preservado (45 → ~23-25, redução de ~45-50%; ou 54 criados → ~23-25 = redução ~55-58% do inventário criado).
- **Cada onda contribui para refinamento incremental do sketch** — charter é artefato vivo. Pattern para ondas D-X: descoberta empírica de cluster shape é editorial (não estrutural); revisão de ADR-045 só se cluster sequence falhar materialmente.

**Pattern de migração validado empíricamente na Onda C** (template para D-X) — reaplicado e estendido na Onda D:

- ✓ Archive + redirect header canonical (blockquote `> **ARCHIVED <data>**` + cross-ref + H1 original preservado) — reaplicado em 4 ADRs.
- ✓ Archive index incremental — estendido com 4 linhas D (paralelo às 2 da Onda C).
- ✓ Cross-refs em docs vivos atualizados — escala ~5× maior (~58 ocorrências em 9 docs vs ~12 em 5 na Onda C).
- ✓ Link rot em ADRs imutáveis aceito como categoria histórica.
- ✓ Procedure preservation per ADR-024 — **NÃO aplica em Onda D** (cluster sem procedure pré-existente); F9 fronteira só ativa quando procedure pré-existe.
- ✓ Cond 5 primária isolada em auto-aplicação — F4 lesson Onda C reaplicada literal (cond 4 NÃO aplica; cond 1 NÃO aplica).
- ✓ Cond 2 refinada na Onda D (F4 do design-reviewer absorvido): "absorção consolidatória" (preserva substância integralmente) vs "revogação" (inverte doutrina central; ex.: ADR-043 → ADR-035). Pattern editorial para ondas E-X.

**Saldo inventário pós-ADR-052:** 52 ADRs criados (001-052) - 21 arquivados (017, 029, 005, 018, 025, 030, 021, 044, 004, 028, 039, 041, 008, 013, 015, 016, 023, 040, 007, 012, 024) = **31 vigentes** *(refutado pela auditoria da Onda K — ver tabela § Atualização pós-execução linha 188; saldo pré-auditoria não distinguia Substituídos preservados in-place; saldo pós-K equivalente seria "30 vigentes substantivos + 1 Substituído")*. Acréscimo líquido de 1 (ADR-052 meta-doutrinal apex pontual; primeiro acréscimo líquido desde Onda A; natural para meta-decisão editorial). Trajetória esperada para target 13-15 em 3-5 ondas adicionais (ADR-052 + ADRs apex preservados — ADR-009/-011/-026/-034/-038/-042/-043/-045/-046/-047/-048/-049/-050/-051/-052 + outros — convergem em meta-cluster final ou permanecem standalone).

### Refinamento editorial documentado (Ondas F + G + H — 3 modos emergentes; gatilho ADR-045 disparado)

**Onda F** estabeleceu refinamento editorial por **exclusão** vs sketch literal (Ondas C+D+E seguiram sketch literal):

- **(a) Exclusão de ADRs semanticamente desalinhados** do sketch original — ADR-037 (README framing) excluído do cluster execução/run-plan por pertencer semanticamente a discoverability/branding. Sketch agrupou por proximidade numérica, não coesão semântica. Refinamento corrige sem revisão estrutural de ADR-045 § Decisão parte 1.
- **(b) Preservação de ADRs ancestrais fora do cluster** quando categoria conceitual distinta justifica standalone — ADR-010 (progress display Task tool) NÃO absorvido apesar de ser decisão base de ADR-039. Categoria distinta com potencial consumers futuros além de `/run-plan`. Charter sketch tinha contradição interna (ADR-039 listado em 2 clusters); resolução favorece preservar categoria distinta de ADR-010.

**Onda G** aplicou refinamento editorial por **inclusão** vs sketch literal:

- **(c) Inclusão de ADRs omitidos do sketch** quando coesão semântica de família justifica — ADR-015 (hook block_env por sufixo `.env`) **incluído** apesar de omitido no sketch original do cluster componentes plugin (5 ADRs listados; ADR-015 omisso aparentemente por descuido editorial). ADR-040 § Origem explicitamente cita ADR-015 como "ancestral direto — primeiro PreToolUse block hook do plugin"; excluir deixaria órfão um membro da família coesa de 3 hooks defensivos (block_env + block_gitignored + block_settings_drift). Inclusão cabe em ADR-045 § Decisão linha 56 fronteira *"absorção de ADR em consolidado diferente do sketch original"* como ajuste editorial — categoria livre durante execução das ondas.

**Onda H** aplicou refinamento editorial por **preservação por constraint mecânico** vs sketch literal:

- **(d) Preservação de ADR ancestral fora do cluster por constraint mecânico** quando hardcode em decisão Aceito + categoria semântica distinta justificam — ADR-034 (critério adendo vs novo ADR) **preservado vigente** apesar de pertencer ao sketch original do cluster convenções editoriais (4 ADRs listados; Onda H absorveu apenas 3 — 007+012+024). Constraint mecânico: ADR-034 está hardcoded na always-include curated list de ADR-048 § Decisão `[ADR-009, ADR-034, ADR-043]`; absorvê-lo exigiria editar ADR-048 Aceito (mexer ADR-classical é antipattern) + leitura mecânica do design-reviewer cairia em ADR-034 archived com redirect em vez do consolidado. Categoria semântica distinta: ADR-034 é meta-doutrina apex (critério meta-editorial), não convenção editorial estrutural (idiomas + categoria de artefato). Análogo a (b) Onda F (preservação de ancestral por categoria distinta) com constraint mecânico explícito adicional. ADR-034 fica como ADR clássico standalone codificando meta-doutrina apex; substância NÃO absorvida em ADR-051.

**Gatilho de revisão de ADR-045 disparado pós-Onda H + codificado formalmente via ADR-052** (commit `7d26dc8` + PR #96 merge `fdba1aa`). Operador escolheu Opção B (ADR sucessor codificando preventivamente antes da Onda I) sobre Opção A (status quo) e Opção C (aguardar 4ª instância). **Meta-pattern editorial canonical das ondas de migração estabelecido:**

- **Modo (a) EXCLUSÃO** — desalinhamento semântico do sketch (ADR-037) OU ancestralidade codificada com categoria distinta sem constraint mecânico (ADR-010 Onda F).
- **Modo (b) INCLUSÃO** — ADR omitido do sketch quando coesão semântica de família justifica (ADR-015 Onda G).
- **Modo (c) PRESERVAÇÃO POR CONSTRAINT MECÂNICO PURO** — ADR hardcoded em § Decisão de outro ADR Aceito vigente (ADR-034 Onda H). Critério `grep <ADR-ID>` objetivamente verificável.

ADR-052 promoveu o terceiro item da fronteira de ADR-045 § Decisão linha 56 ("absorção em consolidado diferente do sketch") de categoria não-codificada para sub-modos canonical com critério mecânico verificável. Decisão central de ADR-045 preservada (consolidação 45 → ~13-15 ADRs sob hierarquia invertida + filtro de admissão). Modo (c) restrito a constraint mecânico puro per F2 absorvido (opção A recomendada pelo design-reviewer) — caso ADR-010 ficou em modo (a) bullet 2 em vez de modo (c) sub-caso 2 colapsado.

**Ondas I-X aplicam modos editoriais com referência formal a ADR-052** — escala mecanismo sem reabrir doutrina por onda. **Escalação se 4º modo emergir** (categoria editorial nova não-coberta por exclusão/inclusão/preservação por constraint) — reabertura de ADR-052 (gatilho próprio).

### Anti-regression checklist — itens preservados em ADR-046 (Onda C), ADR-047 (Onda D), ADR-048 (Onda E), ADR-049 (Onda F), ADR-050 (Onda G), ADR-051 (Onda H), ADR-052 (meta-pattern editorial)

- § Discoverability: gating tri-state ✓, 2 strings canonical ✓, dedup ✓, herança editorial ✓ (ADR-046).
- § Path contract: 3 paths suportados ✓, sintaxe ✓, regra de não-referenciar ✓, mecânica mkdir+probe+gate ✓, replicação `.claude/` ✓, `/note` 2º dispatcher com assimetria de trigger codificada ✓ (substância ADR-018 Addendum absorvida via F2 do design-reviewer), recusas cross-mode + critério "direção do leak" ✓, aceitar CLAUDE.md gitignored + cláusula OR ✓, rejeições version_files/changelog ✓ (ADR-047).
- § Reviewers: free-read curado modo híbrido ✓, threshold N=15 + modo legacy ✓, anotação `**ADRs candidatos:**` ✓, scan medium prescritivo ✓, always-include hardcoded ADR-009/-034/-043 ✓, cap nominal 5 + critério promoção ≥3 anotações ✓, reporte invariante ✓, rebatimento de não-incluídos com critério "escopo de aplicação" ✓, pontos cegos cobertos vs não-cobertos ✓, pattern auto-consistente (ADR-048 não se inclui na lista) ✓ (ADR-048).
- § Skills e fluxo: state-tracking em git/forge ✓, BACKLOG editorial sem `## Em andamento` ✓, `## Concluídos` append-only via `/run-plan §3.4` ✓, -5 mecanismos defensivos obsoletos ✓, campo `**Branch:**` opcional + probe `git symbolic-ref` + cutucada header Branch + 4 discriminações stderr ✓, Task tool 2 modos (progress display ADR-010 + state-keeping ADR-049 § Decisão (c)) com lifecycle 2-estados + marker convention `[capture:*]` ✓, `/run-plan §3.5` captura unificada cross-superfícies (pré-loop + passo 2 loop + passo 3.2 validação) ✓, campo `**Modo:** runbook` + único valor aceito + bypass 4 dimensões + incompatibilidade dura `**Branch:** + **Modo:** runbook` + materialização Falhou ✓, pattern paralelo de 5 campos opcionais (`**Branch:**` + `**Modo:**` + `**Linha do backlog:**` + `**Termos ubíquos tocados:**` + `**ADRs candidatos:**`) com critério de promoção registrado ✓, tensões resolvidas com ADR-002 + ADR-010 (preservados vigentes) ✓ (ADR-049).
- § Componentes do plugin: skills/agents/hooks como tipos canônicos ✓, naming convention (skills geradoras stack-agnósticas via sub-blocos por marker; hooks suffixados + auto-gating triplo) ✓, single source of truth para idioms (substância de ADR-008 que ADR-019 cita preservada via cross-ref) ✓, CI lint mínimo como categoria distinta das 3 vetadas (4 critérios cumulativos; cobertura positiva/negativa explícita; frase canonical preservada intacta) ✓, 3 hooks PreToolUse defensivos (block_env por sufixo `.env` universal; block_gitignored por sinal do consumer com 7 alternativas rejeitadas; block_settings_drift por content regex em settings.json) ✓, critério mecânico cumulativo `disable-model-invocation` explícito + tabela retroativa às 9 skills reproduzida literal ✓, pattern editorial "critério mecânico cumulativo" como meta-doutrina herdada (ADR-020/-022/-023 reusos preservados) ✓ (ADR-050).
- § Convenções editoriais: 3 audiências distintas (operativa / informativa / discoverability) como pattern editorial canonical ✓, idioma artefatos informativos segue convenção de commits do projeto + cobertura positiva (CHANGELOG/tag/PR) e negativa (operativos `.md`) explícita + trade-off migração retroativa CHANGELOG preservado ✓, idioma artefatos discoverability segue público alvo do canal com critério mecânico "lido antes/depois adoção" ✓, categoria `docs/procedures/` paralela a `templates/` com 3 critérios cumulativos para criação + invariante de cross-ref bilateral ADR-001↔ADR-051 ✓, hooks exceção universal preservada em philosophy.md operativa (não absorvida — doutrina pragmática base) ✓ (ADR-051). **ADR-034 (critério adendo vs novo ADR) preservado vigente standalone** por constraint mecânico (always-include ADR-048) + categoria semântica distinta (meta-doutrina apex) — substância NÃO absorvida em ADR-051; reader consulta ADR-034 vigente diretamente para meta-critério editorial.
- § Meta-pattern editorial das ondas de migração: 3 modos editoriais canonical (a) EXCLUSÃO + (b) INCLUSÃO + (c) PRESERVAÇÃO POR CONSTRAINT MECÂNICO PURO ✓, critério mecânico verificável de cada modo + exemplos canonical literais (ADR-037+ADR-010 modo (a); ADR-015 modo (b); ADR-034 modo (c)) ✓, modo (c) restrito a constraint mecânico puro com grep ID em § Decisão de ADR Aceito vigente (preservação por categoria distinta sem constraint cai em modo (a) bullet 2) ✓, aplicação à fronteira ADR-045 § Decisão linha 56 explícita (refinamento de escopo, não revisão estrutural) ✓, gatilho de revisão para 4º modo emergente ✓ (ADR-052). Promoção de "categoria não-codificada de ajuste editorial livre" para "categoria com sub-modos canonical com força normativa" para Ondas I-X.
- Nenhuma carga doutrinal perdida em qualquer onda; gap `block_gitignored.py` (NOTES 2026-05-30T05:26:59Z) preservado como Limitação em ADR-050 § Limitações (endereçamento pendente; reservado espaço de extensão — anteriormente em ADR-047 antes da Onda G).

### Pendência operacional registrada (Onda F) — endereçada na Onda G

**Bloco 1 commitado sem invocação do doc-reviewer** (Onda F) — violação direta de doutrina explícita em `skills/run-plan/SKILL.md` § "## O que NÃO fazer" linha "Não pular revisor, mesmo em bloco trivial". Mitigação pós-fato em Onda F: Read manual + critérios 2-3 do plano confirmaram format archive correto. Lição operacional para ondas G-X: aderir estrito ao reviewer-per-bloco mesmo quando pattern editorial é convergente.

**Onda G endereçou a pendência:** 4/4 blocos (Bloco 1 archive + Bloco 2 hot spot + Bloco 3 docs auxiliares + bloco extra §3.5) invocaram doc-reviewer obrigatório antes do commit. Convergência empírica em 5 ondas (C+D+E+F+G) não admitiu exceção à doutrina explícita. Lição internalizada — pattern operacional para Ondas H-X.
