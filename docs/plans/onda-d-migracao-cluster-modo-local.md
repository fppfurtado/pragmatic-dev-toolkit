# Plano — Onda D da redesign da camada doutrinal (migração cluster modo local)

## Contexto

**ADRs candidatos:** ADR-005 (foundational do cluster — modo `local` para `decisions_dir`/`backlog`/`plans_dir`, regra de não-referenciar, mecânica `mkdir` + probe gitignore + gate `Gitignore`, recusa em `version_files`/`changelog`), ADR-018 (sucessor parcial — `/init-config` step 4.5 garante `.claude/` em `.worktreeinclude` quando ≥1 role local; Addendum 2026-05-27 reconhece `/note` como 2º dispatcher universal), ADR-025 (sucessor parcial — recusa assimétrica de `backlog: local + plans_dir: canonical` em `/init-config` step 3 + defensividade em `/triage` step 1; critério "direção do leak"), ADR-030 (sucessor parcial — `/init-config` aceita `CLAUDE.md` gitignored e replica via `.worktreeinclude` no step 4.5 com cláusula OR), ADR-045 (apex redesign — esta onda materializa § Decisão parte 1 § Implementação literal), ADR-046 (template do pattern de migração validado na Onda C — F1 link rot em 2 categorias, F4 cond 5 primária isolada, F9 fronteira ADR vs procedure per ADR-024), ADR-043 (apex doutrinal — Ockham operacionalizado critério 4 governa criação do consolidado), ADR-034 (critério adendo vs novo ADR — orienta criação: cond 5 sucessor parcial primário absorvendo 4 ADRs; cond 4 NÃO aplica per F4 de Onda C; cond 1 NÃO aplica — ADR-045 é ancestral codificado), ADR-024 (categoria `docs/procedures/` — relevante por **ausência** aqui: cluster modo local **não tem procedure file**; toda substância vive em CLAUDE.md "Local mode" section + ADRs).

Onda D (quarta) da redesign da camada doutrinal coordenada por `docs/plans/redesign-camada-doutrinal-charter.md`. **Segunda migração cluster temático** per ADR-045 § Decisão parte 1 § Implementação literal — primeira foi Onda C (cutucadas). Cluster modo local é candidato natural pós-Onda C:

1. **Cluster index Addendum já existe** em ADR-005 (Onda 3 da reforma doutrinária, PR #86) enumerando os 3 sucessores parciais (ADR-018/-025/-030) — paralelo ao Addendum de ADR-017 que precedeu Onda C; proof-of-concept editorial.
2. **4 ADRs (vs 2 em Onda C)** — scope médio que **calibra pattern em cluster maior** antes de clusters de 5-8 ADRs (design-reviewer ecosystem, componentes plugin).
3. **Primeira aplicação do pattern a cluster sem procedure file** — Onda C tinha `docs/procedures/cutucada-descoberta.md` como par editorial (fronteira ADR vs procedure per ADR-024 codificada em F9). Cluster modo local não tem procedure equivalente; toda substância semântica + canonical defaults vivem no ADR consolidado + CLAUDE.md "Local mode" section. **Testa transferibilidade** do pattern fora de cutucadas (per NOTES 2026-05-30T16:16:00Z "Próximo candidato natural").
4. **Cluster coeso semanticamente** — 4 ADRs cobrem 4 dimensões da mesma decisão: (a) ADR-005 conceito + paths + regra de não-referenciar + mecânica gitignored; (b) ADR-018 invariante `.claude/` em `.worktreeinclude` via `/init-config`; (c) ADR-025 recusa cross-mode `backlog: local + plans_dir: canonical`; (d) ADR-030 aceitar `CLAUDE.md` gitignored e replicar. Cada um estende ADR-005 num eixo distinto (paths, replicação, coerência cross-mode, descoberta).

**Refinamento emergente da estrutura-alvo.** Charter sketch original (11 ADRs) posicionava modo local como `ADR-003-modo-local.md` absorvendo exatamente esses 4 (uma das poucas previsões precisas do sketch). Esta onda materializa fielmente. Calibração emergente da Onda C (target realista 13-15 ADRs em vez de 11) absorvida no charter pós-Onda C; Onda D não introduz refinamento adicional do sketch.

**Linha do backlog:** Onda D é sub-scope da umbrella multi-onda em `## Próximos`; não corresponde a linha distinta. Per ADR-004 + precedente Ondas A+B+C, umbrella é atualizada in-place post-merge.

## Resumo da mudança

**Esta Onda D produz:**

1. **ADR-047 consolidado** (criado via `/new-adr` no /triage step 4) — absorve substância de ADR-005 + ADR-018 + ADR-025 + ADR-030 num único ADR temático "modo local". § Decisão integra (a) paths suportados + sintaxe `paths.<role>: local` + comportamento (`.claude/local/<role>/`); (b) regra de não-referenciar (commit/PR/branch metadata); (c) Resolution protocol trilho paralelo; (d) mecânica de inicialização (mkdir + probe gitignore + gate `Gitignore`); (e) invariante `.claude/` em `.worktreeinclude` via `/init-config` step 4.5 + `/note` como 2º dispatcher (de ADR-018 + Addendum); (f) recusa assimétrica cross-mode `backlog: local + plans_dir: canonical` com critério "direção do leak" (de ADR-025); (g) aceitação de `CLAUDE.md` gitignored com replicação no step 4.5 (de ADR-030); (h) rejeição de `version_files`/`changelog` em modo local. § Origem histórica preserva 4 incidentes empíricos das decisões absorvidas (PJe 2026-05-11 onboarding atrito → ADR-005 + ADR-018; PJe 2026-05-11 follow-up → ADR-018 mecânica; H_arch roadmap 2026-05-12 → ADR-025; PJe 2026-05-11 mid-stream → ADR-030). § Gatilhos de revisão consolida triggers das 4 decisões. Status `Proposto` (vira `Aceito` após pattern de migração validar em onda de tamanho maior — ondas E-X com 5+ ADRs).

2. **Archive de ADR-005, ADR-018, ADR-025, ADR-030** — `git mv` para `docs/decisions/archive/` + header redirect canonical adicionado a cada arquivo movido (format codificado em ADR-046 § Razões): blockquote `> **ARCHIVED 2026-05-30** — content absorbed into [ADR-047](../ADR-047-modo-local-paths-replicacao-cross-mode.md); see that ADR for current authority. Body below preserved verbatim for historical record.` + header H1 original preservado intacto abaixo. Conteúdo original preservado por inteiro per ADR-045 § Decisão parte 1 (*"Arquivamento (não deleção) materializa Verdade"*).

3. **Archive index update** — `docs/decisions/archive/README.md` ganha 4 linhas novas na tabela mapeando ADR-005/-018/-025/-030 → ADR-047 (Onda D). Cada onda D-X estende a tabela como invariante codificada em ADR-046.

4. **Propagação de cross-refs em docs vivos** (9 arquivos; ~58 ocorrências de IDs em ~34 linhas distintas):
   - `CLAUDE.md` (3 linhas, 6 ocorrências) — § "Local mode" + § "Pragmatic Toolkit" + linha NOTES.md row: substitui referências a ADR-005 por ADR-047; preserva mecânica e schema.
   - `skills/init-config/SKILL.md` (13 linhas, 21 ocorrências) — cross-refs a ADR-005/-018/-025/-030 substituídas por ADR-047; mecânica de steps 3, 4.5, 5 e `## O que NÃO fazer` preservadas intactas (apontadores doutrinais apenas).
   - `skills/triage/SKILL.md` (4 linhas, 6 ocorrências) — cross-refs a ADR-005/-025 substituídas por ADR-047; mecânica de step 1 pre-condição cross-mode e step 4 "Caminho com plano em modo local" preservadas.
   - `skills/release/SKILL.md` (1 linha, 1 ocorrência) — ADR-005 (rejeição de modo local para `version_files`/`changelog`) substituída por ADR-047.
   - `skills/new-adr/SKILL.md` (1 linha, 2 ocorrências) — ADR-005 (§ Implementação opcional em modo local) substituída por ADR-047.
   - `skills/note/SKILL.md` (7 linhas, 12 ocorrências) — cross-refs a ADR-005/-018 substituídas por ADR-047; description frontmatter + § O que NÃO fazer + ordem de gates preservados.
   - `skills/run-plan/SKILL.md` (1 linha, 1 ocorrência) — ADR-005 (modo local — regra de não-referenciar em commit message) substituída por ADR-047.
   - `docs/install.md` (3 linhas, 8 ocorrências) — cross-refs a ADR-005/-018/-030 substituídas por ADR-047; tom e estrutura preservados.
   - `README.md` (1 linha, 1 ocorrência) — ADR-005 (NOTES.md row) substituída por ADR-047.

5. **Link rot consciente em docs imutáveis** — ~16 ADRs imutáveis citam ADR-005/-018/-025/-030 em § Origem como precedente histórico ou cross-ref doutrinal (categoria (a) histórica de F1 lesson de Onda C). Estes NÃO são editados per ADR-classical. Subset suspeito de categoria (b) doutrinal ativa identificado pré-execução para verificação durante design-reviewer auto-fire: ADR-032 (cita ADR-005 como base do "store non-role"; substância já interna ao ADR-032), ADR-038 (cita ADR-005 ↔ ADR-025 como precedente do pattern partial-successor com status `Proposto`; substância já interna), ADR-042 (cita ADR-005 mecânica para cross-write; substância delegada), ADR-046 (cita ADR-005/-017 como Addenda precedentes para archive pattern; substância delegada para ADR consolidado). **Hipótese de zero substância "doutrinal ativa" perdida** — pre-existente Addendum de ADR-005 (Onda 3) explicitamente reconheceu ADR-018/-025/-030 como sucessores parciais; consolidação preserva isso ao absorver os 4 num só. design-reviewer valida hipótese.

6. **Charter atualização** (post-merge, manual) — `docs/plans/redesign-camada-doutrinal-charter.md` § "Atualização pós-execução" tabela adiciona linha "Onda D — Migração cluster modo local" com commit hash + PR + substância; anti-regression checklist § Path contract / § Componentes do plugin (linhas referenciando ADR-018 gap do block_gitignored.py) atualizadas refletindo ADR-047 como nova autoridade. NÃO escopo desta Onda D; commit separado post-merge per precedente Ondas A+B+C.

**Pattern de migração testado nesta onda** (fora do escopo de cutucadas, calibração para ondas E-X):
- Cluster sem procedure file — toda substância semântica + canonical defaults vão para o ADR consolidado (sem split ADR/procedure per F9 Onda C — fronteira ADR-024 só aplica quando procedure file pré-existe).
- 4 ADRs absorvidos (vs 2 em Onda C) — calibra pattern em scope médio antes de clusters de 5-8.
- Mais cross-refs cross-cutting (~58 ocorrências em ~34 linhas, 9 arquivos vs ~12 ocorrências em ~7 linhas, 5 arquivos da Onda C) — testa escalabilidade do propagation pattern em ordem de magnitude ~5×.
- F4 lesson de Onda C reaplicada literal: cond 5 primária isolada; cond 4 NÃO aplica (instância vs categoria nova — ADR-045 carrega categoria meta; ondas C-X são instâncias); cond 1 NÃO aplica (ADR-045 § Decisão parte 1 é ancestral codificado direto).

## Arquivos a alterar

### Bloco 1 — Archive ADR-005 + ADR-018 + ADR-025 + ADR-030 + archive index extension {reviewer: doc}

- `git mv docs/decisions/ADR-005-modo-local-gitignored-roles.md docs/decisions/archive/`
- Editar topo do arquivo movido inserindo blockquote redirect **antes** do `# ADR-005: <título original>` (format canonical de ADR-046):

  ```markdown
  > **ARCHIVED 2026-05-30** — content absorbed into [ADR-047](../ADR-047-modo-local-paths-replicacao-cross-mode.md); see that ADR for current authority. Body below preserved verbatim for historical record.

  # ADR-005: Modo local-gitignored para roles do path contract
  ```

- `git mv docs/decisions/ADR-018-replicacao-claude-em-modo-local-init-config.md docs/decisions/archive/` + análogo (ADR-018 + título original).
- `git mv docs/decisions/ADR-025-recusar-cross-mode-backlog-local-init-config.md docs/decisions/archive/` + análogo.
- `git mv docs/decisions/ADR-030-aceitar-claude-md-gitignored-via-worktreeinclude.md docs/decisions/archive/` + análogo.
- Estender tabela em `docs/decisions/archive/README.md` adicionando 4 linhas:

  ```markdown
  | ADR-005 — Modo local-gitignored para roles do path contract | [ADR-047](../ADR-047-modo-local-paths-replicacao-cross-mode.md) | D |
  | ADR-018 — Replicação `.claude/` em modo local via `/init-config` | [ADR-047](../ADR-047-modo-local-paths-replicacao-cross-mode.md) | D |
  | ADR-025 — Recusar cross-mode `backlog: local + plans_dir: canonical` no `/init-config` | [ADR-047](../ADR-047-modo-local-paths-replicacao-cross-mode.md) | D |
  | ADR-030 — Aceitar `CLAUDE.md` gitignored via `.worktreeinclude` | [ADR-047](../ADR-047-modo-local-paths-replicacao-cross-mode.md) | D |
  ```

### Bloco 2 — CLAUDE.md cross-refs (Local mode + Pragmatic Toolkit + NOTES row) {reviewer: doc}

- `CLAUDE.md` linha 43 (NOTES.md row em "The role contract"): substituir `[ADR-005](docs/decisions/ADR-005-modo-local-gitignored-roles.md)` por `[ADR-047](docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md)`. Texto descritivo "local-gitignored per ADR-005 extended in ADR-032" reescrito mantendo sentido — opção concreta: "local-gitignored per [ADR-047](...) extended in [ADR-032](...)".
- `CLAUDE.md` § "Local mode" (linha 69) header — substituir "Defined by [ADR-005](...)" por "Defined by [ADR-047](...)". Mecânica preservada intacta (mkdir + probe + gate `Gitignore` + 3 paths + `version_files`/`changelog` rejeitam).
- `CLAUDE.md` § "Pragmatic Toolkit" config schema (linha 157): substituir `[ADR-005](docs/decisions/ADR-005-modo-local-gitignored-roles.md)` por `[ADR-047](docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md)`. Texto "full rationale in ADR-005" reescrito como "full rationale in ADR-047".

### Bloco 3 — SKILLs herdeiras cross-refs (init-config + triage + release + new-adr + note + run-plan) {reviewer: doc}

- `skills/init-config/SKILL.md` — substituir cross-refs em 13 linhas distintas (linhas 11, 27, 65, 67, 99, 105, 106, 111, 128, 134, 143, 144, 148; 21 ocorrências de IDs no total — algumas linhas contêm múltiplas refs) de ADR-005/-018/-025/-030 por ADR-047. Pontos de atenção: (i) step 3 "CLAUDE.md gitignored?" + step 4.5 tabela composta + step 5 mensagens de aceitação mantêm prosa intacta; só links markdown atualizam; (ii) `## O que NÃO fazer` bullets sobre `.gitignore` automático + reconsider gitignore + cross-mode mantêm o critério, apenas apontador atualiza.
- `skills/triage/SKILL.md` — substituir cross-refs em 4 linhas (42, 44, 101, 177; 6 ocorrências) de ADR-005/-025 por ADR-047. Pre-condição cross-mode no step 1 (linha 42-44) preserva mecânica e mensagem literal; só link atualiza. "Caminho com plano em modo local" no step 5 (linha 177) preserva regra de não-referenciar; só link atualiza.
- `skills/release/SKILL.md` — substituir cross-ref em 1 ocorrência (linha 163) de ADR-005 por ADR-047. Bullet em `## O que NÃO fazer` sobre recusa de `version_files`/`changelog` em modo local preserva critério; só link atualiza.
- `skills/new-adr/SKILL.md` — substituir cross-ref em 1 ocorrência (linha 91) de ADR-005 por ADR-047. Bullet sobre `## Implementação` opcional em modo local preserva critério; só link atualiza.
- `skills/note/SKILL.md` — substituir cross-refs em 7 linhas distintas (3, 9, 45, 47, 55, 59, 95; 12 ocorrências) de ADR-005/-018 por ADR-047. Pontos de atenção: (i) `description:` frontmatter (linha 3) — substância "store local-gitignored estendendo ADR-005" reescrita como "estendendo ADR-047"; (ii) prosa § "Ordem dos gates" mantém referência mecânica ao gate `Gitignore` e `Worktree replication`; apenas autoria doutrinal atualiza; (iii) `## O que NÃO fazer` bullet sobre mutar `.gitignore`/`.worktreeinclude` cross-write preserva critério; só link atualiza.
- `skills/run-plan/SKILL.md` — substituir cross-ref em 1 ocorrência (linha 134) de ADR-005 por ADR-047. Bullet "Modo local" em § "Micro-commit" preserva regra de não-referenciar; só link atualiza.

### Bloco 4 — docs/install.md + README.md cross-refs {reviewer: doc}

- `docs/install.md` — substituir cross-refs em 3 ocorrências (linhas 69, 71, 73) de ADR-005/-018/-030 por ADR-047. Pontos de atenção: (i) linha 69 sobre modo local + paths aceitos + recusas preserva descrição editorial; só link atualiza; (ii) linha 71 sobre `.worktreeinclude` tracked/gitignored + `/init-config` + `/note` como 2º dispatcher preserva mecânica completa; ambos refs (ADR-018 e ADR-030 + ADR-018 Addendum) substituídos por ADR-047 (substância de ambos consolidada); (iii) linha 73 sobre `block_gitignored` allowlist `<repo>/.claude/` preserva descrição; só link atualiza.
- `README.md` linha 12 (NOTES.md row em "What's inside"): substituir cross-ref a ADR-005 por ADR-047. Texto descritivo "local-gitignored store extending ADR-005 to a non-role category" reescrito mantendo sentido.

## Verificação end-to-end

**Critérios de sucesso da Onda D:**

1. **ADR-047 criado** com Status `Proposto` em `docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md`. § Origem cita ADR-005+ADR-018+ADR-025+ADR-030 como decisões absorvidas + esta onda como investigação. § Origem histórica preserva os 4 incidentes empíricos (PJe 2026-05-11 onboarding; PJe 2026-05-11 mid-stream/CLAUDE.md gitignored; PJe 2026-05-11 follow-up worktreeinclude; H_arch roadmap 2026-05-12 cross-mode). § Decisão integra os 4 eixos (paths/regra de não-referenciar/mecânica + replicação `.claude/` + recusa cross-mode + aceitar `CLAUDE.md` gitignored) em narrativa única coerente. § Gatilhos consolida triggers das 4 decisões.

2. **ADR-005/-018/-025/-030 arquivados:** `ls docs/decisions/ADR-005-*.md docs/decisions/ADR-018-*.md docs/decisions/ADR-025-*.md docs/decisions/ADR-030-*.md` → vazio (movidos). `ls docs/decisions/archive/ADR-005-*.md docs/decisions/archive/ADR-018-*.md docs/decisions/archive/ADR-025-*.md docs/decisions/archive/ADR-030-*.md` → presentes. Header redirect canonical (blockquote) presente no topo de cada arquivo, H1 original intacto abaixo.

3. **Archive index estendido:** `docs/decisions/archive/README.md` carrega tabela com 6 linhas (2 da Onda C + 4 novas da Onda D), ordem cronológica por onda preservada.

4. **`grep "ADR-005\|ADR-018\|ADR-025\|ADR-030" CLAUDE.md` → 0 matches** em linhas que não estejam dentro de blocos `<!-- ... -->` (todas as 3 referências de docs vivos substituídas por ADR-047).

5. **`grep "ADR-005\|ADR-018\|ADR-025\|ADR-030" skills/init-config/SKILL.md skills/triage/SKILL.md skills/release/SKILL.md skills/new-adr/SKILL.md skills/note/SKILL.md skills/run-plan/SKILL.md` → 0 matches** (todas as 26 referências substituídas).

6. **`grep "ADR-005\|ADR-018\|ADR-025\|ADR-030" docs/install.md README.md` → 0 matches** (todas as 4 referências substituídas).

7. **Mecânicas preservadas intactas:** (a) `grep -E "mkdir|probe gitignore|gate.Gitignore|/init-config step 4.5|\\.worktreeinclude|Worktree replication|cross-mode|CLAUDE.md gitignored" skills/init-config/SKILL.md` → matches conforme estado atual (mecânica das 4 decisões intacta); (b) "Recusa de cross-mode" no `/triage` step 1 + `/init-config` step 3 + mensagem literal idêntica; (c) `## O que NÃO fazer` bullets cobrindo `version_files`/`changelog` local, `.gitignore` automático, reconsider gitignore, cross-mode hard refusal preservados.

8. **Link rot em immutable ADRs aceito explicitamente:** `grep -l "ADR-005\|ADR-018\|ADR-025\|ADR-030" docs/decisions/ADR-0*.md docs/plans/*.md` retorna ~16 ADRs imutáveis + planos históricos — esses são imutáveis (immutable ADRs + historical plans); cross-refs em immutable docs ficam como registro histórico, NÃO são editados. Documentar essa lista no commit message.

9. **CHANGELOG.md intacto** (registro histórico imutável paralelo a immutable ADRs) — `grep "ADR-005\|ADR-018\|ADR-025\|ADR-030" CHANGELOG.md` retorna matches preservados como registro de versionamento; NÃO editar.

10. **doc-reviewer audita drift cross-doc:** cross-refs corretos cross-doc (CLAUDE.md ↔ skills ↔ install.md ↔ README.md ↔ ADR-047); ADR-047 substância fiel a ADR-005+ADR-018+ADR-025+ADR-030 combinados; nenhuma carga doutrinal da § Path contract do anti-regression checklist perdida (3 paths suportados, sintaxe `paths.<role>: local`, comportamento `.claude/local/<role>/`, regra de não-referenciar, mecânica `mkdir` + probe + gate, recusas cross-mode, invariante `.claude/` em `.worktreeinclude`, aceitar `CLAUDE.md` gitignored — todas preservadas em ADR-047).

11. **design-reviewer auto-fire em /new-adr step 5 e /triage step 5** valida: padrão de migração coerente com ADR-045 § Decisão parte 1; pattern reusable validado em cluster sem procedure file (transferibilidade demonstrada); auto-aplicação per ADR-034 (cond 5 primária isolada; cond 4 NÃO aplica; cond 1 NÃO aplica) coerente; categoria (b) "doutrinal ativa" do link rot examinada e absorvida ou aceita conforme análise.

## Notas operacionais

**Ordem dos blocos:** Bloco 1 (archive) executado antes dos demais — outros blocos referenciam ADR-047 que substitui os 4 arquivos arquivados. Blocos 2-4 podem rodar em qualquer ordem (independentes entre si após archive).

**Validação do pattern em cluster sem procedure file:** esta é a primeira instância da transferibilidade. Se design-reviewer flagrar gap (ex.: substância de algum dos 4 ADRs não cabe limpo num consolidado, requer split editorial; ou link rot em algum ADR imutável citante revela substância "doutrinal ativa" que precisa ser explicitamente absorvida no consolidado), refinamento é editorial do plano antes de prosseguir. Mudança estrutural na regra de consolidação seria gatilho de revisão de ADR-045.

**Charter atualização post-merge:** após merge da Onda D, atualizar `docs/plans/redesign-camada-doutrinal-charter.md` § "Atualização pós-execução":
- Estender tabela de ondas com linha "Onda D — Migração cluster modo local" (commit hash + PR + substância).
- Anti-regression checklist § Path contract — atualizar referências a "ADR-005" para "ADR-047" (substância preservada; apenas apontador).
- Anti-regression checklist § Componentes do plugin — bullet sobre `block_gitignored` hook + gap NOTES 2026-05-30T05:26:59Z (endereçamento pendente) atualizado para citar ADR-047 como autoridade vigente.
- Saldo inventário pós-Onda D: estimado **41 vigentes** (44 pós-Onda C + 1 ADR-047 - 4 arquivados); drop líquido de 3 (vs 2 em Onda C; cluster maior).
- Anotação progressiva: "Onda D shipped — commit <hash>; cluster modo local migrado".

Update do charter é commit separado post-merge (paralelo às atualizações de umbrella in BACKLOG das Ondas A+B+C); NÃO escopo desta Onda D.

**Decisão excluída — procedure file não criado:** cluster modo local NÃO ganha procedure file equivalente a `cutucada-descoberta.md`. Mecânica das 4 decisões (mkdir + probe + gates + step 4.5 tabela composta + recusa cross-mode + aceitar `CLAUDE.md` gitignored) vive em CLAUDE.md § "Local mode" + skills (`/init-config` step 4.5 + `/triage` step 1 + `/note` § Ordem dos gates). Substância semântica vive em ADR-047. Fronteira ADR-024 não aplica porque procedure não pré-existe; aplicação prospectiva de procedure ficaria como ADR separado se gatilho futuro emergir (ex.: ≥3 dispatchers da invariante `.claude/` em `.worktreeinclude` per ADR-018 Addendum gatilho original — extrair para `docs/procedures/worktree-replication-dispatch.md`).

**Decisão excluída — substância "doutrinal ativa" em ADRs imutáveis pré-mapeada:** ADR-032 + ADR-038 + ADR-042 + ADR-046 citam ADR-005/-018/-025/-030 como autoridade ativa em § Origem ou § Decisão. Hipótese inicial: substância já interna a cada um (ADR-032 carrega justificativa do store non-role completa; ADR-038 carrega precedente partial-successor `Proposto` status pattern; ADR-042 delega mecânica cross-write para ADR-005; ADR-046 codifica archive pattern com ADR-005 como Addendum precedent). design-reviewer auto-fire valida no /new-adr step 5; hipótese falsa em algum ponto → finding cutucado para absorção ou refinamento.

**Cap de ondas estimado:** charter previa 6-10 ondas. Pós-Onda D, cluster sequence revisitada conforme calibração emergente — clusters candidatos remanescentes: alinhamento/triage (ADR-009/-011/-026/-027/-038/-042 + ADR-046 já consolidado); reviewers/curadoria (ADR-021/-044); execução/run-plan (ADR-004/-028/-037/-039/-041); convenções editoriais (ADR-007/-012/-024/-034); componentes plugin (ADR-008/-013/-015/-016/-023/-040); instrumentação progresso (ADR-010/-039); bridge/discoverability (ADR-032/-042); apex (ADR-035/-036/-043/-045/-046). Cap atualizado durante execução conforme cluster shape emerge.

**Sinal de saúde:** se Bloco 1 (archive) ou Bloco 3 (SKILLs cross-cutting) gerar ≥10 findings de doc-reviewer, sinal de que pattern de propagation precisa refinamento antes de aplicar a clusters maiores (5-8 ADRs). Pausar e iterar conforme charter linha 154.

## Decisões absorvidas

design-reviewer no /new-adr step 5 sobre ADR-047 produziu 5 findings; 4 absorvidos pré-commit como caminho-único após análise per ADR-026 + 1 cutucado ao operador (F3 sobre rastreabilidade — operador escolheu opção (a) delegar ao archive + bullet explícito):

- ADR-047 § Decisão (b) (`/note` como 2º dispatcher): adicionada frase "Assimetria de trigger é deliberada" codificando critério load-bearing para futuros 3º/4º dispatchers (preserva substância ADR-018 Addendum perdida na absorção inicial) (F2, caminho-único).
- ADR-047 § Auto-aplicação cond 2: refinada distinguindo "absorção consolidatória" (preserva substância integralmente) vs "revogação" (inverte doutrina central; paralelo a ADR-043 → ADR-035) — pattern editorial para ondas E-X (cond 2 reservada para inversões; absorções seguem cond 5 isolada) (F4, caminho-único).
- ADR-047 § Razões + § Trade-offs (volume de cross-refs): números corrigidos de "32 em 8 docs" para "~58 ocorrências em ~34 linhas distintas, 9 docs vivos" — validação empírica via grep; threshold "≥10 findings" preservado como conservador independente do volume (F1, caminho-único).
- ADR-047 § Limitações (cross-write): citações circulares `per ADR-005 § Gate Gitignore` substituídas por auto-referência a `§ Decisão (a) gate Gitignore` e `§ Decisão (b) Worktree replication` — refinamento cosmético (F5, caminho-único).
- ADR-047 § Trade-offs (implementação history): bullet novo delegando implementação history ao archive explícito (paralelo a Onda C com ADR-046 implicitamente); padrão editorial para ondas E-X codificado (F3, decisão do operador via cutucada — opção (a)).
- Plano § Resumo da mudança bullet 4 + Bloco 3 listagem: números corrigidos cross-cutting refletindo contagens empíricas por arquivo (CLAUDE.md 3 linhas/6 ocorrências; init-config 13 linhas/21 ocorrências; etc.) (F1, caminho-único).
