# Plano — Onda H da redesign da camada doutrinal (migração cluster convenções editoriais)

## Contexto

**ADRs candidatos:** ADR-007 (idioma de artefatos informativos — CHANGELOG/tag/PR descriptions seguem convenção de commits do projeto), ADR-012 (idioma de artefatos discoverability/landing — README/manifest descriptions seguem público alvo do canal; sucessor parcial de ADR-007), ADR-024 (categoria `docs/procedures/` para procedimentos operacionais compartilhados — sucessor parcial de ADR-001; 3 critérios cumulativos; categoria paralela a `templates/`), ADR-045 (apex redesign — esta onda materializa § Decisão parte 1 § Implementação literal), ADR-046+ADR-047+ADR-048+ADR-049+ADR-050 (templates do pattern de migração validado em Ondas C+D+E+F+G; F4 lessons cond 5 isolada + F1 link rot 2 categorias + refinamento editorial bidirecional reaplicados), ADR-034 (critério adendo vs novo ADR — cond 5 sucessor parcial primário absorvendo 3 ADRs; cond 4 NÃO aplica per F4 Onda C; cond 1 NÃO aplica — ADR-045/-046/-047/-048/-049/-050 ancestrais codificados; **constraint: ADR-034 PRESERVADO fora do cluster** per always-include de ADR-048 — análogo a ADR-010 em F), ADR-001 (preservado vigente — sucessor parcial relationship com ADR-024 absorvido; cross-ref a ADR-001 em § Addendum 2026-05-12 fica como categoria histórica resolvendo via redirect), ADR-014 + ADR-026 + ADR-033 (preservados vigentes; categoria-b link rot doutrinal ativa identificada — citações de ADR-007/-012/-024 cobertas via substância em ADR-051 § Decisão), ADR-040+ADR-041+ADR-043+ADR-046+ADR-047+ADR-048+ADR-049+ADR-050 (preservados vigentes; citam ADR-007 como autoridade do idioma de commits — substância preservada).

Onda H (oitava) da redesign da camada doutrinal coordenada por `docs/plans/redesign-camada-doutrinal-charter.md`. **Sexta migração cluster temático** per ADR-045 § Decisão parte 1 § Implementação literal — Ondas C+D+E+F+G precederam (cutucadas, modo local, reviewers/curadoria, execução/run-plan, componentes plugin).

Cluster convenções editoriais é candidato natural pós-Onda G:

1. **Cluster de calibração editorial complexa** — 3 ADRs com **baixa coesão semântica** unificados pela função "regras editoriais do toolkit" (idioma artefatos informativos + idioma discoverability + categoria `docs/procedures/`). Antecipado em charter linha 182 como "convenções editoriais (ADR-007+012+024+034, 4 heterogêneos)".
2. **Constraint mecânico estrutural — ADR-034 preservado fora do cluster** — ADR-034 (critério adendo vs novo ADR) está hardcoded na always-include curated list de ADR-048 (`always-include hardcoded ADR-009/-034/-043`). Absorvê-lo desalinharia a always-include (categoria apex doutrinal vs estrutural de convenções editoriais), e a leitura de ADR-034 (archived com redirect) em vez do consolidado quebra parcialmente o caminho mecânico do design-reviewer. **Solução:** análogo a ADR-010 em F (preservação de ADR ancestral fora do cluster por categoria distinta). ADR-034 fica vigente como ADR clássico standalone codificando meta-doutrina apex; substância NÃO precisa estar em ADR-051 (decisão editorial separada). Cluster Onda H absorve apenas **3 ADRs** (007+012+024) em vez de 4 do sketch original.
3. **Cluster sem procedure file** — reaplica F9 lesson D+E+F+G (fronteira ADR-024 não aplica antecipadamente — mas observação especial: ADR-024 É a própria decisão sobre a categoria `docs/procedures/`; 4 procedures existentes consomem ADR-024 como autoridade vigente — link rot doutrinal ativa categoria-b a fechar).
4. **F4 lessons reaplicadas literal** — cond 5 primária isolada (sucessor parcial absorvendo 3 ADRs); cond 4 NÃO aplica (ADR-045 carrega categoria meta; ADR-051 é sexta instância); cond 1 NÃO aplica (ADR-045/-046/-047/-048/-049/-050 ancestrais codificados); cond 2 NÃO aplica — regra central de cada ADR absorvido preservada integralmente; nenhum marcado como `Substituído`.
5. **F1 lesson reaplicada literal** — link rot em 2 categorias identificado pré-execução: (a) histórica via archive blockquote redirect; (b) **doutrinal ativa hot spot** via absorção no consolidado. 4 procedures + README.md citam ADR-024 como "categoria estabelecida" — substância absorvida em ADR-051 § Decisão (c) fecha gap; cross-refs em procedures e README atualizam para ADR-051; ADRs vigentes mantêm-se imutáveis.

### Composição do cluster vs sketch original do charter

Charter sketch original (NOTES 2026-05-30T06:08:04Z) / ADR-045 § Decisão parte 1 § Implementação:

```
ADR-007-convencoes-editoriais.md      # idioma por audiência (3) + commits +
                                      # adendo vs novo ADR + categoria
                                      # docs/procedures/
                                      # (absorve atual: 007, 012, 024, 034)
```

**Sketch absorvia 4 ADRs; Onda H inclui 3** (ADR-034 preservado fora do cluster). **Refinamento editorial 3ª instância** vs Ondas F (exclusão) + G (inclusão):

- **(a) Onda F: EXCLUSÃO** de ADRs semanticamente desalinhados (ADR-037 + ADR-010 fora do cluster execução/run-plan).
- **(b) Onda G: INCLUSÃO** de ADR omitido do sketch quando coesão semântica justifica (ADR-015 dentro do cluster componentes plugin).
- **(c) Onda H: PRESERVAÇÃO de ADR ancestral fora do cluster** quando constraint mecânico justifica (ADR-034 preservado vigente por hardcode na always-include de ADR-048). Análogo a ADR-010 em F (categoria distinta com consumers vigentes diretos), mas com **constraint mecânico explícito** adicional. 

**Gatilho de revisão de ADR-045 disparado** conforme charter § "Refinamento editorial documentado" sinal a observar: 3 aplicações editoriais (F exclusão + G inclusão + H preservação por constraint) sugerem que merece consideração de codificação explícita via ADR sucessor de ADR-045 antes da Onda I. NÃO escopo desta Onda H; sinal a registrar no charter pós-merge para decisão de operador.

Detalhamento do constraint ADR-034:

- ADR-048 (free-read design-reviewer consolidado) § Decisão "always-include curated list" lista hardcoded `[ADR-009, ADR-034, ADR-043]` como sempre lidos integralmente pelo design-reviewer paralelo a `philosophy.md`. Reasoning: 3 apex doutrinais (revisor design pré-fato; critério meta-editorial; hierarquia doutrinal).
- Se ADR-034 fosse archived → consolidado (ADR-051), reader caía em archive com redirect blockquote canonical apontando para ADR-051. Reader chegaria à substância via 1 hop adicional — mecanicamente funciona, mas:
  1. Always-include hardcoded teria que ser atualizada `[ADR-009, ADR-051, ADR-043]` (edit em ADR-048 Aceito — questionável; mexer ADR-classical é antipattern).
  2. ADR-051 sub-dimensões (a/b/c) são editoriais sintáticas (idioma/categoria); ADR-034 é meta-doutrina (critério adendo vs novo ADR) — não cabe semanticamente no consolidado editorial. ADR-034 pertence ao cluster apex meta-doutrinal hipotético (charter linha 182 "apex meta-cluster"), não a convenções editoriais.
- Preservar ADR-034 vigente standalone é solução conservadora alinhada com pattern F (ADR-010 ancestral preservado) sem custo mecânico em ADR-048 imutável.

- **Cluster mantém 3 do sketch:** 007 + 012 + 024.
- **ADR-034 fora do cluster** por constraint mecânico (always-include ADR-048) + categoria semântica distinta (meta-doutrina apex vs convenções editoriais estruturais).

**Saldo:** Onda H absorve 3 ADRs (vs 4 do sketch). Inventário pós-Onda H: 32 - 3 archivados + 1 ADR-051 = **30 vigentes** (drop líquido de 2 nesta onda; menor que Onda G por scope reduzido). Documentação editorial post-merge consolida em charter § "Atualização pós-execução" conforme Notas operacionais abaixo.

**Linha do backlog:** Onda H é sub-scope da umbrella multi-onda em `## Próximos`; não corresponde a linha distinta. Per ADR-049 § Decisão (a) + precedente Ondas A-G, umbrella é atualizada in-place post-merge.

## Resumo da mudança

**Esta Onda H produz:**

1. **ADR-051 consolidado** (criado via `/new-adr` no /triage step 4) — absorve substância de ADR-007 + ADR-012 + ADR-024 num único ADR temático "convenções editoriais". § Decisão integra:
   - (a) **Idioma de artefatos informativos** (de ADR-007): `CHANGELOG.md` + mensagens de tag anotada + descrições de PR seguem idioma da convenção de commits do projeto (default canonical EN). Critério: audiência única (leitor de release inspeciona junto com `git log`); operativa (.md de skill/agent/philosophy/ADR/plan) tem audiência distinta. Fora do escopo: arquivos `.md` operativos/editoriais. Cobertura concreta + razões (coerência narrativa + eliminação de tradução implícita) preservadas literal.
   - (b) **Idioma de artefatos discoverability/landing** (de ADR-012): `README.md` + descrições em manifests de marketplace (`plugin.json`/`marketplace.json`) + `keywords`/`tags` + GitHub repo About seguem idioma do público alvo do canal de descoberta (default canonical EN para Claude Code marketplace). Critério mecânico: "artefato cuja função primária é ser indexado/lido por audiência externa **antes** de a pessoa decidir adotar o plugin". Sucessor parcial de (a) — README sai da categoria "fora do escopo / livre" de (a) via (b). Fora do escopo: `docs/install.md`, `docs/philosophy.md`, `CLAUDE.md`, ADRs/planos/BACKLOG (lidos após adoção).
   - (c) **Categoria `docs/procedures/` para procedimentos operacionais compartilhados** (de ADR-024): paralela a `templates/` (ADR-001, esqueletos canônicos preenchíveis). Distinção semântica: `templates/` = esqueletos preenchíveis (skills leem + preenchem placeholders ao produzir artefato); `docs/procedures/` = procedimentos operacionais (skills leem + executam algoritmo descrito). Critério cumulativo para criação de novo procedure (todos devem se verificar): conteúdo é procedimento operacional (algoritmo executável); ≥2 skills referenciam ou consumiriam; extração resolve acoplamento textual concreto entre skills. Verificação obrigatória no `/triage` ou ADR que propõe novo procedimento. Mecânica de consumo: Read em runtime via path do plugin (embed/copy reintroduz duplicação — descartado). Status: Aceito (promovido Proposto→Aceito 2026-05-16 quando categoria atingiu 3 itens — cleanup-pos-merge + cutucada-descoberta + forge-auto-detect). 4ª e 5ª categorias dentro de `docs/`: `decisions/`, `plans/`, `audits/`, `procedures/` (e templates/ separado em raiz).
   - (d) **Pattern editorial "3 audiências distintas"** — meta-doutrina que conecta dimensões (a) e (b) com Convenção de idioma operativa de `philosophy.md`: **operativa** (prosa do toolkit no projeto; dev escrevendo/lendo durante desenvolvimento) + **informativa** (registro de mudanças; leitor de release inspecionando junto com git log) + **discoverability** (artefato de landing; leitor pré-adoção decidindo se vai instalar). Cada audiência tem critério próprio de idioma — operativa espelha projeto consumidor; informativa segue convenção de commits; discoverability segue público alvo do canal. Pattern editorial estabelecido em ADR-007 (2 audiências) + estendido em ADR-012 (3ª audiência). Preservado em ADR-051 § Decisão (d) como meta-doutrina canonical das convenções editoriais. Aplicação atual ao toolkit: operativa PT-BR + informativa EN (commits EN) + discoverability EN (marketplace anglófono).

   § Origem histórica preserva 3 incidentes empíricos: drift commits EN vs CHANGELOG PT durante /triage de tag synthesis em /release (sessão 2026-05-07) → ADR-007 (faltava convenção explícita para artefatos informativos); análise pré-publicação no Claude Code marketplace (sessão /triage 2026-05-10) → ADR-012 (README PT limita discoverability anglófono majoritário do canal); auditoria 2026-05-12 finding L1 acoplamento textual /release § Cleanup pós-merge ↔ /triage §0 → ADR-024 (extração de procedimento para `docs/procedures/cleanup-pos-merge.md`; ROI confirmado pós-Onda 3 com 3 itens em 4 dias). § Gatilhos consolida triggers das 3 decisões. § Auto-aplicação cond 5 primária isolada per F4 Ondas C-G.

   **Substância preservada para link rot doutrinal ativa categoria-b** — gap fechado quando docs vivos citam membros do cluster archived:
   - 4 procedures (`cleanup-pos-merge.md`, `cutucada-descoberta.md`, `forge-auto-detect.md`, `reviewer-invocation-read.md`) citam "Categoria `docs/procedures/` estabelecida em ADR-024" → ADR-051 § Decisão (c) preserva substância "categoria docs/procedures/ paralela a templates/ + 3 critérios cumulativos para criação".
   - README.md:32 cita "Per ADR-024" no item da tabela sobre `cleanup-pos-merge.md` → ADR-051 § Decisão (c) preserva.
   - `philosophy.md` linha 75 cita ADR-007 + linha 77 cita ADR-012 → ADR-051 § Decisão (a) + (b) preservam substância "3 audiências distintas" e critérios respectivos.
   - `skills/release/SKILL.md` linha 72 cita "ADR-007" como autoridade do idioma das bullets → ADR-051 § Decisão (a) preserva.
   - ADR-001 § Addendum 2026-05-12 cita ADR-024 como sucessor parcial estabelecendo categoria `docs/procedures/` — categoria histórica preserved (ADR-001 imutável; redirect canonical ADR-024 archived → ADR-051 resolve).
   - ADR-033 (templates admite single consumer) cita ADR-024 como pattern — categoria histórica preserved.
   - ADR-034 § Auto-aplicação cita ADR-024 (e outros 4 ADRs meta-doutrinais) como exemplo de meta-doutrina paralela — categoria histórica preserved.
   - Múltiplos ADRs vigentes (-014/-026/-040/-041/-043/-046/-047/-048/-049/-050) citam ADR-007 como autoridade do idioma de commits — categoria histórica preserved via redirect.

2. **Archive de ADR-007, ADR-012, ADR-024** — `git mv` para `docs/decisions/archive/` + header redirect canonical (format de ADR-046): blockquote `> **ARCHIVED 2026-05-31** — content absorbed into [ADR-051](../ADR-051-<slug>.md); see that ADR for current authority. Body below preserved verbatim for historical record.` + header H1 original preservado intacto abaixo.

3. **Archive index update** — `docs/decisions/archive/README.md` ganha 3 linhas novas na tabela (Onda H). Cada onda C-X estende a tabela como invariante codificada em ADR-046.

4. **Propagação de cross-refs em docs vivos** (7 arquivos; 8 ocorrências em 8 linhas distintas):
   - `docs/procedures/cleanup-pos-merge.md` linha 3 → ADR-051 § Decisão (c).
   - `docs/procedures/cutucada-descoberta.md` linha 3 → ADR-051 § Decisão (c).
   - `docs/procedures/forge-auto-detect.md` linha 3 → ADR-051 § Decisão (c).
   - `docs/procedures/reviewer-invocation-read.md` linha 3 → ADR-051 § Decisão (c).
   - `README.md` linha 32 → ADR-051 § Decisão (c) (item da tabela sobre `cleanup-pos-merge.md` — hot spot user-facing per ADR-012 → ADR-051 § Decisão (b) discoverability).
   - `docs/philosophy.md` linha 75 → ADR-051 § Decisão (a) (idioma informativos).
   - `docs/philosophy.md` linha 77 → ADR-051 § Decisão (b) (idioma discoverability).
   - `skills/release/SKILL.md` linha 72 → ADR-051 § Decisão (a) (idioma bullets do changelog).

5. **Link rot consciente em docs imutáveis** — outros ADRs imutáveis e planos históricos citam ADR-007/-012/-024 em § Origem como precedente ou cross-ref doutrinal (categoria (a) histórica de F1 lesson Onda C). Subset suspeito de categoria (b) doutrinal ativa já identificado pré-execução (todos com substância absorvida em ADR-051; link via archive resolve):
   - ADR-001 § Addendum (cita ADR-024) — categoria histórica (ADR-001 imutável; redirect resolve para ADR-051 § Decisão (c)).
   - ADR-014 + ADR-026 + ADR-033 + ADR-034 + outros vigentes citam ADR-007/-012/-024 como precedente — categoria histórica preserved.
   - ADR-040+-041+-043+-046+-047+-048+-049+-050 (8 vigentes) citam ADR-007 como autoridade do idioma de artefatos informativos — categoria histórica preserved via redirect canonical.
   Hipótese de zero substância "doutrinal ativa" perdida — design-reviewer valida.

6. **Charter atualização** (post-merge, manual) — `docs/plans/redesign-camada-doutrinal-charter.md` § "Atualização pós-execução" tabela adiciona linha "Onda H — Migração cluster convenções editoriais" + refinamento editorial 3ª instância documentado (preservação ADR-034 fora do cluster por constraint mecânico) + **gatilho de revisão de ADR-045 disparado registrado como sinal explícito**; anti-regression checklist § Convenções editoriais atualizada refletindo ADR-051 como nova autoridade. NÃO escopo desta Onda H; commit separado post-merge per precedente Ondas A-G.

**Pattern de migração validado nesta onda** (sexta aplicação; calibração com refinamento editorial 3ª instância e gatilho ADR-045):
- Cluster de 3 ADRs sem procedure file — calibração descendente vs Ondas G (6) e D+F (4), próxima a Ondas C+E (2). Operação intermediária menor que F+G.
- **Refinamento editorial 3ª instância** (Onda H preservação por constraint vs F exclusão e G inclusão) — gatilho de revisão de ADR-045 disparado. Pattern editorial bidirecional + preservação por constraint formaliza 3 modos de refinamento. Charter post-merge documenta sinal explícito para decisão operador antes da Onda I.
- Hot spot em **4 procedures + README user-facing** (5 das 8 ocorrências). Spread em 7 docs vivos (vs 7 em G; 5 em F; 6 em E).
- F4 lessons reaplicadas literal (cond 5 isolada; cond 4 NÃO aplica; cond 1 NÃO aplica; cond 2 NÃO aplica — regra central preservada).
- F1 lesson reaplicada literal (link rot 2 categorias; categoria-b doutrinal ativa identificada pré-execução; substância absorvida em ADR-051).
- **Pendência operacional Onda F endereçada em Onda G:** 4/4 blocos com doc-reviewer obrigatório. Onda H mantém invariante — 3 blocos planejados, todos com `{reviewer: doc}`.

## Arquivos a alterar

### Bloco 1 — Archive 3 ADRs + archive index extension {reviewer: doc}

**Instrução para data dinâmica:** substituir `2026-05-31` no template do blockquote pela data de execução (formato `YYYY-MM-DD` do dia de aplicação) ao replicar em cada um dos 3 arquivos arquivados — pattern Ondas C+D+E+F+G.

- `git mv docs/decisions/ADR-007-idioma-artefatos-informativos.md docs/decisions/archive/`
- Editar topo do arquivo movido inserindo blockquote redirect **antes** do `# ADR-007: <título original>`:

  ```markdown
  > **ARCHIVED 2026-05-31** — content absorbed into [ADR-051](../ADR-051-convencoes-editoriais-consolidado.md); see that ADR for current authority. Body below preserved verbatim for historical record.

  # ADR-007: Idioma de artefatos informativos segue convenção de commits
  ```

- `git mv docs/decisions/ADR-012-idioma-artefatos-discoverability-landing.md docs/decisions/archive/` + análogo.
- `git mv docs/decisions/ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md docs/decisions/archive/` + análogo.
- Estender tabela em `docs/decisions/archive/README.md` adicionando 3 linhas (Onda H):

  ```markdown
  | ADR-007 — Idioma de artefatos informativos segue convenção de commits | [ADR-051](../ADR-051-convencoes-editoriais-consolidado.md) | H |
  | ADR-012 — Idioma de artefatos de discoverability/landing | [ADR-051](../ADR-051-convencoes-editoriais-consolidado.md) | H |
  | ADR-024 — Categoria docs/procedures/ para procedimentos operacionais compartilhados | [ADR-051](../ADR-051-convencoes-editoriais-consolidado.md) | H |
  ```

### Bloco 2 — 4 procedures + README cross-refs (hot spot user-facing categoria docs/procedures/) {reviewer: doc}

- `docs/procedures/cleanup-pos-merge.md` linha 3: substituir "Categoria `docs/procedures/` estabelecida em [ADR-024](../decisions/ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md)" por "Categoria `docs/procedures/` estabelecida em [ADR-051](../decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (c)".
- `docs/procedures/cutucada-descoberta.md` linha 3: análogo.
- `docs/procedures/forge-auto-detect.md` linha 3: análogo.
- `docs/procedures/reviewer-invocation-read.md` linha 3: análogo.
- `README.md` linha 32 (item da tabela sobre `cleanup-pos-merge.md`): substituir "Per ADR-024" por "Per [ADR-051](docs/decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (c)". Hot spot user-facing per ADR-012 → ADR-051 § Decisão (b) discoverability — substituição preserva substância integralmente (procedure descrita continua coerente).

### Bloco 3 — philosophy.md + skills/release cross-refs (idioma artefatos a+b) {reviewer: doc}

- `docs/philosophy.md` linha 75 (parágrafo "Artefatos informativos do registro de mudanças"): substituir "Detalhes em [ADR-007](decisions/ADR-007-idioma-artefatos-informativos.md)" por "Detalhes em [ADR-051](decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (a)". Substância do parágrafo (audiência diferente; leitor de release vs dev) preservada literal.
- `docs/philosophy.md` linha 77 (parágrafo "Artefatos de discoverability/landing"): substituir "Detalhes em [ADR-012](decisions/ADR-012-idioma-artefatos-discoverability-landing.md)" por "Detalhes em [ADR-051](decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (b)". Substância preservada literal.
- `skills/release/SKILL.md` linha 72 (item 2 do passo 5): substituir "Idioma das bullets segue o idioma dos commits agrupados (ADR-007)" por "Idioma das bullets segue o idioma dos commits agrupados (ADR-051 § Decisão (a))". Substância (alinhamento commits ↔ changelog bullets) preservada literal.

## Verificação end-to-end

**Critérios de sucesso da Onda H:**

1. **ADR-051 criado** com Status `Proposto` em `docs/decisions/ADR-051-convencoes-editoriais-consolidado.md`. § Origem cita ADR-007+ADR-012+ADR-024 como decisões absorvidas + ADR-045/-046/-047/-048/-049/-050 como templates + ADR-034 explicitamente preservado fora do cluster por constraint always-include de ADR-048 + ADRs vigentes preservados citando substância (ADR-001, -014, -026, -033, -040, -041, -043). § Decisão integra as 4 dimensões (a-d) sob narrativa única coerente. § Origem histórica preserva os 3 incidentes empíricos. § Gatilhos consolida triggers das 3 decisões. § Auto-aplicação cond 5 primária isolada; cond 4 NÃO aplica; cond 1 NÃO aplica; cond 2 NÃO aplica (regra central preservada).

2. **ADR-007, ADR-012, ADR-024 arquivados:** `ls docs/decisions/ADR-007-*.md docs/decisions/ADR-012-*.md docs/decisions/ADR-024-*.md` → vazio (movidos). `ls docs/decisions/archive/ADR-007-*.md docs/decisions/archive/ADR-012-*.md docs/decisions/archive/ADR-024-*.md` → 3 arquivos presentes. Header redirect canonical no topo, H1 original intacto abaixo.

3. **ADR-034 preservado vigente:** `ls docs/decisions/ADR-034-*.md` → 1 arquivo presente (NÃO arquivado). ADR-034 mantém-se como ADR clássico standalone codificando meta-doutrina (critério adendo vs novo ADR). Always-include de ADR-048 § Decisão `[ADR-009, ADR-034, ADR-043]` permanece intacta (constraint mecânico preserved).

4. **Archive index estendido:** `docs/decisions/archive/README.md` carrega tabela com 21 linhas (2C + 4D + 2E + 4F + 6G + 3H), ordem cronológica por onda preservada.

5. **`grep "ADR-007\|ADR-012\|ADR-024" docs/procedures/*.md README.md` → 0 matches** (5 ocorrências substituídas).

6. **`grep "ADR-007\|ADR-012\|ADR-024" docs/philosophy.md skills/release/SKILL.md` → 0 matches** (3 ocorrências substituídas; observação: skills/new-adr/SKILL.md linha 37 cita "ADR-007a-" como literal de padding atípico — NÃO é cross-ref doutrinal, NÃO contam como ocorrência).

7. **Substância preservada para link rot doutrinal ativa categoria-b:**
   - `grep -c "categoria.*docs/procedures/" docs/decisions/ADR-051-*.md` → ≥1 match (substância ADR-024 absorvida).
   - `grep -c "audiência\|público alvo" docs/decisions/ADR-051-*.md` → ≥2 matches (3 audiências distintas da § Decisão (d)).
   - `grep -c "convenção de commits\|público alvo do canal" docs/decisions/ADR-051-*.md` → ≥2 matches (idiomas informativos + discoverability).

8. **ADRs vigentes preservados (não arquivados):** `ls docs/decisions/ADR-001-*.md ADR-014-*.md ADR-026-*.md ADR-033-*.md ADR-034-*.md ADR-040-*.md ADR-041-*.md ADR-043-*.md ADR-046-*.md ADR-047-*.md ADR-048-*.md ADR-049-*.md ADR-050-*.md` → 13 arquivos presentes (não arquivados; mantêm cross-refs a ADRs do cluster como autoridade histórica via redirect canonical).

9. **Tabela "Components" do README intacta exceto cross-ref ADR-024:** `grep -cE "^\| (\`/[a-z-]+\`|\`[a-z_-]+\`|\`docs/procedures/" README.md` → mesma contagem pré-edição (estrutura preservada; apenas link atualizado para ADR-051).

10. **§ Convenção de idioma de philosophy.md preservada estrutural:** `grep -c "operativa\|informativa\|discoverability" docs/philosophy.md` → mesma contagem pré-edição (3 audiências preservadas; apenas cross-refs atualizados nas linhas 75+77).

11. **Link rot em immutable ADRs aceito explicitamente:** `grep -l "ADR-007\|ADR-012\|ADR-024" docs/decisions/ADR-0*.md docs/plans/*.md` ainda retornará vários arquivos antigos — esses são imutáveis (immutable ADRs + historical plans); cross-refs em immutable docs ficam como registro histórico, NÃO são editados.

12. **CHANGELOG.md intacto** (registro histórico imutável) — `grep "ADR-007\|ADR-012\|ADR-024" CHANGELOG.md` retorna matches preservados como registro de versionamento; NÃO editar.

13. **doc-reviewer audita drift cross-doc:** cross-refs corretos cross-doc; ADR-051 substância fiel a ADR-007+ADR-012+ADR-024 combinados; nenhuma carga doutrinal da § Convenções editoriais do anti-regression checklist perdida (idioma artefatos informativos + idioma discoverability + categoria docs/procedures/ + pattern 3 audiências — todas preservadas em ADR-051). Verificar especialmente fidelidade dos 3 critérios cumulativos para novo procedure (operacional vs esqueleto; ≥2 skills consumers; resolve acoplamento concreto) — substância load-bearing per ADR-024 § Decisão.

14. **design-reviewer auto-fire em /new-adr step 5 e /triage step 5** valida: padrão de migração coerente com ADR-045 § Decisão parte 1; preservação de ADR-034 fora do cluster coerente com pattern F (ADR-010) + constraint mecânico explícito (always-include ADR-048) per ADR-045 fronteira "ajuste editorial vs revisão"; pattern reusable em cluster com hot spot user-facing em README; auto-aplicação per ADR-034 (cond 5 primária; cond 4 NÃO aplica; cond 1 NÃO aplica; cond 2 NÃO aplica — regra central preservada) coerente; **gatilho de revisão de ADR-045 disparado pela 3ª instância de refinamento editorial** — registrar como sinal explícito no charter post-merge sem ação imediata.

## Notas operacionais

**Ordem dos blocos:** Bloco 1 (archive) executado antes dos demais — outros blocos referenciam ADR-051 que substitui os 3 arquivos arquivados. Blocos 2-3 podem rodar em qualquer ordem (independentes entre si após archive); Bloco 2 (4 procedures + README) tem hot spot user-facing (README per ADR-012 → ADR-051 § Decisão (b)) — sanity check docs user-facing automaticamente cobre via substituição direta no próprio README.

**Aderir reviewer-per-bloco estrito (lição operacional Onda F endereçada em Onda G):** Bloco 1 (archive) DEVE invocar `doc-reviewer` obrigatório — invariante de 5 ondas consecutivas (C+D+E+F+G) sem exceção à doutrina explícita "Não pular revisor, mesmo em bloco trivial". Onda H mantém pattern.

**Validação da preservação de ADR-034 + gatilho ADR-045:** se design-reviewer flagrar gap na preservação de ADR-034 (ex.: substância não-canonical preserved separadamente; constraint always-include não-justificado; refinamento sem ancestral codificado em ADR-045 fronteira), preservação é editorial do plano antes de prosseguir. Quanto ao gatilho de revisão de ADR-045 (3ª instância de refinamento editorial), NÃO disparar ADR sucessor durante esta Onda H — apenas registrar como sinal explícito no charter pós-merge para decisão de operador em sessão subsequente. Mudança estrutural na regra de consolidação seria gatilho de revisão de ADR-045 com escopo próprio.

**Charter atualização post-merge:** após merge da Onda H, atualizar `docs/plans/redesign-camada-doutrinal-charter.md` § "Atualização pós-execução":
- Estender tabela de ondas com linha "Onda H — Migração cluster convenções editoriais" (commit hash + PR + substância + **preservação ADR-034 por constraint mecânico documentada**).
- Anti-regression checklist § Convenções editoriais — atualizar referências a "ADR-007/-012/-024" para "ADR-051 § Decisão (a/b/c/d)" + nota explícita sobre ADR-034 preservado vigente como ADR clássico standalone codificando meta-doutrina.
- § Refinamento editorial documentado: estender com **3ª instância** (Onda H preservação por constraint análoga a ADR-010 em F mas com hardcoded always-include ADR-048 reforçando). Documentar **gatilho de revisão de ADR-045 disparado** — 3 aplicações editoriais (F exclusão + G inclusão + H preservação por constraint) sugerem que merece consideração de codificação explícita via ADR sucessor de ADR-045 antes da Onda I. Sinal explícito para operador decidir em sessão futura.
- Saldo inventário pós-Onda H: estimado **30 vigentes** (32 pós-G + 1 ADR-051 - 3 arquivados); drop líquido de 2 (menor que Onda G por scope reduzido; alinha com calibração escopo médio do cluster).
- Anotação progressiva: "Onda H shipped — commit <hash>; cluster convenções editoriais migrado com preservação ADR-034 por constraint mecânico e gatilho ADR-045 registrado".

Update do charter é commit separado post-merge (paralelo às atualizações de umbrella in BACKLOG das Ondas A-G); NÃO escopo desta Onda H.

**Decisão excluída — procedure file não criado (apesar de ADR-024 ser a decisão sobre `docs/procedures/`):** cluster convenções editoriais NÃO ganha procedure file novo. F9 lesson reaplicada: fronteira ADR-024 não aplica antecipadamente. Observação especial: ADR-024 É a própria decisão sobre a categoria `docs/procedures/`; substância "categoria estabelecida + 3 critérios para novos procedimentos" vive em ADR-051 § Decisão (c). 4 procedures existentes mantêm cross-refs atualizados (Bloco 2). Nenhum novo procedure surgir nesta onda — escopo apenas absorção do critério meta.

**Decisão excluída — ADR-034 NÃO absorvido apesar de pertencer ao sketch original do cluster:** constraint mecânico (hardcoded na always-include de ADR-048 § Decisão) + categoria semântica distinta (meta-doutrina apex vs convenções editoriais estruturais) justificam preservação fora do cluster. Análogo a ADR-010 em F (categoria distinta com consumers vigentes diretos) com constraint mecânico adicional. ADR-034 pertenceria a futuro cluster apex meta-doutrinal hipotético (charter linha 182), não a convenções editoriais. ADR-051 § Origem reconhece ADR-034 como meta-doutrina vigente preservada (cross-ref preservada como autoridade).

**Decisão excluída — ADR-001 NÃO absorvido apesar de sucessor parcial relationship com ADR-024:** ADR-001 (protocolo de templates) é ancestral de ADR-024 (sucessor parcial estabeleceu categoria paralela). ADR-001 § Addendum 2026-05-12 cita ADR-024. Absorver ADR-001 expandiria o cluster além do scope "convenções editoriais" — ADR-001 é decisão sobre `templates/` (esqueletos canonical preencheveis), não convenção editorial. Pertenceria a futuro cluster "components/conventions" ou permanece standalone como decisão fundacional. ADR-001 mantém-se vigente; cross-ref ao ADR-024 archived resolve via redirect canonical para ADR-051 § Decisão (c).

**Sinal a observar para ondas I-X — gatilho de revisão de ADR-045 disparado:** Onda F exclusão + Onda G inclusão + Onda H preservação por constraint = 3 instâncias de refinamento editorial. Charter § "Refinamento editorial documentado" sinal a observar atingido. Antes da Onda I, considerar:
- Codificação explícita do meta-pattern editorial bidirecional + preservação por constraint via ADR sucessor parcial de ADR-045 (Opção (b) recomendada pelo design-reviewer da Onda G F4, deferida então para "só charter").
- Refinamento estrutural de ADR-045 § Decisão linha 56 fronteira "absorção em consolidado diferente do sketch" para incluir explicitamente as 3 categorias editoriais (exclusão, inclusão, preservação por constraint).
- Operador decide em sessão futura — não bloqueia Ondas I-X enquanto pattern editorial cabe na fronteira atual.

**Cap de ondas estimado:** charter previa 6-10 ondas. Pós-Onda H (oitava), trajetória esperada: H + 2-4 ondas I-X adicionais. Cluster sequence revisitada — candidatos remanescentes após Onda H: **alinhamento/triage** (ADR-009+011+026+027+038+042, 6 ADRs com constraint always-include de ADR-048 sobre ADR-009 — análogo ao constraint de Onda H sobre ADR-034); **discoverability/branding** (ADR-037 + ?); **brainstorm** (ADR-036 standalone); **apex meta-cluster** (ADR-035+043+045+046+047+048+049+050+051 + ADR-034 preservado — pode ou não consolidar).

**Sinal de saúde:** se Bloco 2 (4 procedures + README) gerar ≥10 findings de doc-reviewer, sinal de que cross-refs em procedures + README precisam refinamento antes de aplicar a clusters com hot spot user-facing maior em ondas futuras. Pausar e iterar conforme charter linha 154.

## Decisões absorvidas

- ADR-051 § Origem histórica dimensão (a): bullet adicional preservando trade-off de migração retroativa do CHANGELOG histórico (entradas PT pré-2026-05-07 → EN como trabalho one-time aceito) — substância de ADR-007 § Trade-offs originalmente não absorvida (caminho-único).
- ADR-051 § Decisão (c): bullet "Invariante de cross-ref bilateral" adicionado preservando invariante de implementação original de ADR-024 (cross-ref bilateral ADR-001 ↔ ADR-051 § Decisão (c)) — substância operacional load-bearing originalmente não absorvida (caminho-único).
- F3 informativo (não absorvida, registro no charter): observação sobre hot spot user-facing README — substituição cabível mas reader cai no topo do consolidado em vez de sub-dimensão. Sugestão opcional de fragment-link para preservar UX. Sinal a observar pós-merge sem ação imediata (decisão editorial do operador em sessão futura se gatilho observable emergir).

## Pendências de validação

(A ser preenchida pelo `/run-plan` se ficarem itens pendentes pós-execução. Reaproveita formato Onda G per template canonical.)
