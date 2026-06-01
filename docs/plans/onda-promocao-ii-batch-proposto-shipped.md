# Plano — Onda Promoção II (tactical-only batch promotion 10 ADRs Proposto-shipped → Aceito formal)

## Contexto

Onda Promoção II — tactical-only batch promotion de 10 ADRs Proposto-shipped vigentes para Aceito formal. Critério explícito declarado em charter linha 190 + BACKLOG segmento Onda K':

> **Proposto-shipped + efetivo (referenciado como autoridade em CLAUDE.md/skills/agents) + sem decisão pendente de cluster**

Pattern paralelo a **Onda Promoção I** (PR #97, commits `0548130` + `8ab6a8f` + `0c06bde`) que promoveu 7 consolidados pós-redesign (ADR-046+047+048+049+050+051+052). Onda Promoção II **expande critério** para incluir 3 categorias novas:

1. **Apex doutrinais não-promovidos na Promoção I** — ADR-043 (hierarquia doutrinal vigente; hardcoded always-include ADR-048) + ADR-045 (apex redesign + admission policy + sucessor parcial de ADR-043) — ambos efetivos há semanas como autoridade (referenciados em CLAUDE.md + skills + charter), mas escopo nominal Promoção I "consolidados pós-redesign" excluiu apex pré-redesign.

2. **Consolidados Onda I+J** — ADR-053 (alinhamento/triage Onda I) + ADR-054 (bridge cross-project Onda J) — naturais Proposto recém-criados; agora efetivos em produção; promoção alinha Status com state real.

3. **Standalone preservados por decisão de onda anterior (sub-categoria 3a)** — ADR-031 (standalone preservado per ADR-052 modo (a) bullet 2 — decisão Onda I) + ADR-034 (standalone preservado per ADR-052 modo (c) constraint mecânico — decisão Onda H).

3b. **Candidatos cluster downstream com sequência declarada (sub-categoria 3b)** — ADR-037 (discoverability candidato Onda L) + ADR-033 (foundational templates candidato Onda M). Cluster downstream futuro não invalida promoção atual; se absorvidos em cluster, recebem `Status: Substituído por ADR-XXX` per pattern editorial Ondas C-J.

3c. **Standalone materializados nesta Onda Promoção II por unicidade categórica (sub-categoria 3c — decisão substantiva desta onda)** — ADR-022 (archival editorial — categoria solo sem família plausível: archival policy é categoria única no toolkit; sem cluster downstream sequenciado) + ADR-036 (brainstorm intencionalmente não-codificado — categoria conceitual única: meta-doutrina inversa Ockham apex). Listados como candidatos cluster em charter linha 188 (Onda K mapeamento) sem cluster downstream declarado; Promoção II decide standalone explicitamente registrando justificativa de unicidade categórica. Bloco 2 atualiza charter linha 188 movendo ADR-022 + ADR-036 de "candidatos cluster" para "standalone preservados (decisão Onda Promoção II)" — invariante cross-doc charter ↔ plano preservado.

**Clarificação do critério "sem decisão pendente de cluster":** refere-se ao **Status atual ser definitivo no momento da promoção** (sem subsidência editorial pendente que possa reverter Status: Proposto → Substituído). Cluster downstream futuro (ADR-033 candidato Onda M; ADR-037 candidato Onda L) **não invalida** promoção atual — se um ADR for absorvido em cluster downstream, será marcado `Status: Substituído por ADR-XXX` + archivado per pattern editorial Ondas C-J (substitui Aceito por Substituído sem mexer no histórico). Promoção II alinha state formal com state efetivo atual; decisões futuras seguem fluxo normal de archive + Status update.

**Auto-bootstrap mecânico** (paralelo a Promoção I que promoveu ADR-052 definidor + ADR-048 alvo juntos sem circularidade): ADR-052 (codificador dos 3 modos editoriais) está Aceito desde Promoção I; ADR-052 cita ADR-034 + ADR-031 + ADR-010 como exemplos canonical dos modos a/b/c — promoção desses ADRs reforça o exemplo canonical sem afetar a definição mecânica de ADR-052.

**Saldo quantitativo inalterado (27 entradas); saldo qualitativo alinha distribuição lifecycle** — 10 ADRs Proposto → Aceito; zero archived; zero novos; zero substância editorial mudada. Tactical-only paralelo a Onda Promoção I (PR #97); decisão substantiva pequena materializada na sub-categoria 3c (ADR-022 + ADR-036 standalone por unicidade categórica) atualiza charter linha 188 mas não altera saldo nem substância dos ADRs.

**Linha do backlog:** plugin: **redesign da camada doutrinal** — consolidar 45 ADRs em ~10-12 temáticos sob hierarquia invertida pós-v2.14.0 + condensar `philosophy.md` (princípios + mapping operacional + ≥3 pattern como condição geral de YAGNI terminar; cortar § Codificação estrutural overhead) + codificar **política de admissão going forward** (*"isto é decisão reversível ou entendimento estabilizado?"*) como mecanismo de prevenção de re-acúmulo.

**ADRs candidatos:** ADR-052 (precedente Promoção I + critério mecânico modo (c) que justifica auto-bootstrap); ADR-048 (always-include constraint — ADR-034/043 hardcoded; promoção alinha state formal); ADR-045 (admission policy + fronteira editorial — autoriza categoria editorial livre); ADR-034 (alvo + critério adendo vs novo ADR — promoção não dispara cond 4 ADR-034 pois Status promotion é state alignment, não decisão estrutural nova).

## Resumo da mudança

Tactical-only batch promotion de Status field em 10 ADRs Proposto-shipped vigentes. Decomposta em **3 blocos**: 1 bloco principal (Status edits) + 2 blocos editoriais (charter + BACKLOG).

1. **Status field promotion em 10 ADRs**: substituir `**Status:** Proposto` por `**Status:** Aceito (<data>)` em cada arquivo. Sem outras edições.
2. **Refinar charter § Atualização pós-execução linha 190 (Promoção II Pendente → ✓)**: substituir Status `Pendente` → `✓` + commits/PR + substância expandida (10 ADRs promovidos + categorias + auto-bootstrap + critério clarificado).
3. **Atualizar BACKLOG umbrella linha 5 segmento Promoção II**: substituir segmento Pendente por shipped paralelo ao segmento Onda K'.

**Não-escopo desta onda:**
- Decisões de cluster downstream (Onda L discoverability; Onda M foundational templates — separadas).
- Substância editorial dos 10 ADRs (apenas Status field).
- Cleanup órfãos FS (drive-sync ainda parado; vive como item BACKLOG separado).

## Arquivos a alterar

### Bloco 1 — Status field promotion 10 ADRs Proposto-shipped {reviewer: doc}

Substituir `**Status:** Proposto` por `**Status:** Aceito (2026-06-01)` (data ISO; preserva pattern Onda Promoção I) em cada arquivo:

- `docs/decisions/ADR-022-politica-archival-docs-plans.md`: archival editorial standalone (decisão Promoção II por unicidade categórica — sub-categoria 3c).
- `docs/decisions/ADR-031-cutucada-condicional-draft-idea-projeto-maduro.md`: standalone preservado per ADR-052 modo (a) bullet 2 (decisão Onda I).
- `docs/decisions/ADR-033-templates-admite-single-consumer-declarativo.md`: foundational templates standalone (candidato Onda M downstream — não invalida promoção).
- `docs/decisions/ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md`: meta-doutrina apex hardcoded always-include ADR-048 (decisão Onda H via ADR-052 modo (c)).
- `docs/decisions/ADR-036-brainstorm-intencionalmente-nao-codificado-em-skill.md`: brainstorm standalone (decisão Promoção II por unicidade categórica — sub-categoria 3c).
- `docs/decisions/ADR-037-codigo-como-fonte-de-verdade-vs-intent-as-truth.md`: discoverability standalone (candidato Onda L downstream — não invalida promoção).
- `docs/decisions/ADR-043-hierarquia-doutrinal-fundamentais-raiz.md`: apex doutrinal vigente hardcoded always-include ADR-048 (não-promovido na Promoção I por escopo nominal).
- `docs/decisions/ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md`: apex redesign + admission policy + sucessor parcial ADR-043.
- `docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md`: consolidado Onda I (shipped commit `1c9cd9a`+`4b3ce06`+`344c5ab` + PR #99).
- `docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md`: consolidado Onda J (shipped commit `5aa5abd` + PR #100).

Doc-reviewer revisa: (a) cada ADR teve apenas Status field alterado (zero outras mutações); (b) data ISO usada consistentemente; (c) substância editorial intocada.

### Bloco 2 — Refinar charter § Atualização pós-execução linha 190 + linha 188 (Promoção II shipped + Onda K mapeamento atualizado) {reviewer: doc}

- `docs/plans/redesign-camada-doutrinal-charter.md`:
  - **Linha 190 (Promoção II Pendente → shipped):** substituir Status `Pendente` → `✓` + Commit/PR placeholder → commits reais + Substância expandida (10 ADRs promovidos em 3 categorias com 3 sub-categorias na 3 + auto-bootstrap mecânico + critério clarificado "Status atual definitivo no momento; cluster downstream futuro não invalida"; saldo quantitativo inalterado).
  - **Linha 188 (Onda K mapeamento — invariante cross-doc preservado per decisão Promoção II sub-categoria 3c):** substituir parágrafo "10 candidatos cluster (ADR-001/002/003/006/019/020/022/033/036/037)" por "8 candidatos cluster (ADR-001/002/003/006/019/020/033/037) — ADR-022 e ADR-036 movidos para standalone preservados (decisão Onda Promoção II por unicidade categórica)" + atualizar parágrafo "3 standalone preservados por decisão de onda anterior" para "5 standalone preservados (incluindo ADR-022 + ADR-036 decisão Promoção II)". Edit cirúrgico — preserva snapshot histórico de Onda K com nota retroativa.

Doc-reviewer revisa: (a) coerência cross-doc (charter linha 188 + linha 190 ↔ BACKLOG ↔ ADRs editados); (b) decisão standalone ADR-022 + ADR-036 justificada por unicidade categórica é defensável editorialmente (categoria archival policy + meta-doutrina inversa Ockham apex são únicas no toolkit sem família plausível); (c) nota retroativa em linha 188 segue pattern Ondas A-J snapshot histórico + nota refutação editorial.

### Bloco 3 — Atualizar BACKLOG umbrella linha 5 segmento Promoção II {reviewer: doc}

- `BACKLOG.md` linha 5: substituir segmento `**Onda Promoção II** — tactical-only batch promotion 10 ADRs Proposto-shipped (ADR-022, 031, 033, 034, 036, 037, 043, 045, 053, 054) → Aceito formal (critério: Proposto-shipped + efetivo referenciado como autoridade + sem decisão pendente cluster)` por segmento shipped paralelo ao segmento Onda K' (commits + PR + substância expandida + métricas absorções + 3/3 blocos doc-reviewer + saldo 27 entradas preservado).

Doc-reviewer revisa formato paralelo a updates de Onda anteriores na linha 5.

## Verificação end-to-end

Aplicando diretrizes Onda K' canonical (dogfood):

1. **Bloco 1 cobertura (positiva)**: 10 ADRs com Status: Aceito — `for adr in 022 031 033 034 036 037 043 045 053 054; do grep -l "^\*\*Status:\*\* Aceito" docs/decisions/ADR-$adr*.md; done | wc -l` retorna 10.
2. **Bloco 1 condição inversa (per diretriz 4)**: zero ADRs alvos com Status: Proposto — `for adr in 022 031 033 034 036 037 043 045 053 054; do grep -l "^\*\*Status:\*\* Proposto" docs/decisions/ADR-$adr*.md; done | wc -l` retorna 0.
3. **Bloco 2 charter linha 190 (condição inversa per diretriz 4)**: linha 190 deixa de matchear `Pendente` em Status field — `grep -c "^| \*\*Promoção II\*\* —.*| Pendente |" docs/plans/redesign-camada-doutrinal-charter.md` retorna 0.
4. **Bloco 3 BACKLOG (presença positiva)**: linha 5 contém segmento Promoção II shipped — `grep -c "Onda Promoção II.*Aceito formal" BACKLOG.md` retorna ≥1.
5. **Saldo inventário (git-based per diretriz 2)**: zero novos files + zero deletados + zero archived em `docs/decisions/` — `git status --porcelain -- 'docs/decisions/ADR-*.md' | grep -v "^.M " | wc -l` retorna 0 (apenas modified, zero added/deleted). Verificação pós-merge na branch main; durante execução loop em worktree o teste vale a partir do Bloco 1.
6. **Push imediato pós-commit**: caminho-com-plano padrão (commit + push como unidade atômica via `/run-plan §Publicar`).

## Notas operacionais

**Pattern paralelo a Onda Promoção I (PR #97).** Onda Promoção II herda escopo conceitual de Promoção I — tactical-only batch promotion de Status field. Diferença: Promoção II **expande critério** para 3 categorias novas (apex pré-redesign + consolidados Onda I+J + standalone/candidatos cluster downstream) cobrindo gap deixado pela Promoção I (escopo nominal "consolidados pós-redesign").

**Sem ADR criado.** Auto-aplicação ADR-034 § Decisão (paralelo a Onda Promoção I + Ondas K/K' § Origem):

- **Cond 1 (decisão estrutural sem ancestral):** NÃO aplica — ADR-052 § Auto-aplicação codifica precedente Promoção I como pattern editorial Status field promotion = state alignment.
- **Cond 2 (substitui ADR ancestral):** NÃO aplica — Status promotion preserva substância editorial integralmente; apenas alinha Status formal com state efetivo.
- **Cond 3 (codifica restrição externa):** NÃO aplica.
- **Cond 4 (categoria nova):** NÃO aplica sob **leitura estreita per ADR-034 cond 4 (distinção conceitual de artefato) + precedente operacional aplicado em ADR-052 § Auto-aplicação** — Status field promotion é categoria operacional existente (precedente Promoção I); expansão de critério é refinamento editorial, não 4º eixo conceitual paralelo. Status promotion é state alignment formal, não decisão estrutural.
- **Cond 5 (sucessor parcial):** NÃO aplica — Status promotion é exercício da categoria editorial existente per Onda Promoção I + Onda K critério explícito declarado em charter linha 190.

**Decomposição em 3 blocos.** Razão: doc-reviewer roda per-bloco (invariante mantido pós-Onda K' — 16+ instâncias consecutivas); separação Bloco 1 (Status edits em 10 ADRs) ↔ Bloco 2 (charter) ↔ Bloco 3 (BACKLOG) protege contra drift cross-doc. Paralelo direto à decomposição das Ondas K + K'.

**Risco lexical Bloco 1 (ADR-053 + ADR-054 Status field duplicado).** Empiricamente verificado pré-execução: ADR-053 linha 4 (frontmatter Status canonical) + linha 244 (meta-texto explicando lifecycle "Promoção a Aceito após design-reviewer auto-fire") ambos matcheiam `**Status:** Proposto`; idem ADR-054 linha 4 + linha 168. Edit naïve pelo pattern `**Status:** Proposto` → `**Status:** Aceito (2026-06-01)` falharia por non-uniqueness OU corromperia o meta-texto. **Mitigação:** para ADR-053 e ADR-054 especificamente, usar texto contextual mais amplo no Edit (incluir linha precedente do frontmatter como contexto único — `**Data:** <data>\n**Status:** Proposto` ou similar) garantindo unique match na primeira ocorrência (linha 4 frontmatter). Outros 8 ADRs alvo (022, 031, 033, 034, 036, 037, 043, 045) provavelmente têm apenas 1 ocorrência — verificar pré-Edit via `grep -c "^\*\*Status:\*\* Proposto"` (deve retornar 1; se ≥2, mesma mitigação contextual).

**Captura §3.5 reservada.** Se onda revelar inconsistência editorial (ex.: ADR alvo já com Status Aceito; cross-ref quebrado; auto-bootstrap mecânico precisa registro), capturar via TaskCreate `[capture:auditoria]` materializada em §3.5 do `/run-plan` — pendência para revisão futura. Não bloqueante.

**Pós-Onda Promoção II próxima ação:** `/triage` Onda L — cluster discoverability/branding (ADR-037 standalone candidato; cluster pequeno; possivelmente permanência standalone via ADR-052 modo (a) bullet 2 se cluster minúsculo ≤1 ADR).

## Decisões absorvidas

- § Contexto categoria 3 + Bloco 1 descritores ADR-022/-036: decisão substantiva de standalone por unicidade categórica materializada nesta Onda Promoção II (via cutucada (b) absorvida — drift cross-doc charter linha 188 corrigido por Bloco 2 movendo 2 ADRs de "candidatos cluster" para "standalone preservados decisão Promoção II"). Categoria 3 decomposta em 3a (standalone decidido onda anterior), 3b (candidato cluster sequenciado downstream), 3c (standalone materializado nesta onda por unicidade categórica) preservando honestidade editorial (caminho-único pós-cutucada).
- Bloco 2: ampliado para edit dual em charter linha 190 (Promoção II shipped) + linha 188 (Onda K mapeamento atualizado) preservando invariante cross-doc charter ↔ plano (caminho-único per cutucada (b)).
- § Notas operacionais Cond 4 auto-aplicação: citação corrigida de "leitura estreita per ADR-052 § Auto-aplicação" (citação spuriosa — ADR-052 § Auto-aplicação trata auto-aplicação de ADR-052 a si mesmo, não precedente universal) para "leitura estreita per ADR-034 cond 4 (distinção conceitual de artefato) + precedente operacional aplicado em ADR-052 § Auto-aplicação" — referência editorial precisa ([MÉDIO] caminho-único).
- § Contexto "Saldo inalterado": substituído por "Saldo quantitativo inalterado (27 entradas); saldo qualitativo alinha distribuição lifecycle — 10 ADRs Proposto → Aceito" — reporta honestamente o efeito da onda (state alignment formal preserva count mas muda distribuição lifecycle) ([MÉDIO] caminho-único).
- § Notas operacionais Risco lexical Bloco 1: nota adicionada documentando ADR-053 + ADR-054 com `**Status:** Proposto` duplicado (linha 4 frontmatter + linha 244/168 meta-texto) + mitigação contextual para Edit + verificação pré-Edit `grep -c` para 8 ADRs restantes ([MÉDIO] caminho-único).
