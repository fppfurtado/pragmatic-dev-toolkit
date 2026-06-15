# Plano — Onda G da redesign da camada doutrinal (migração cluster componentes plugin)

## Contexto

**ADRs candidatos:** ADR-008 (skills geradoras stack-agnósticas via dispatch interno por marker; sub-blocos canonical por stack; gatilho de revisão "stack nova adicionada"), ADR-013 (CI lint mínimo permitido como categoria distinta das 3 vetadas pela frase canonical; 4 critérios cumulativos), ADR-015 (hook block_env por sufixo `.env`; defesa universal por filename; primeiro PreToolUse block hook), ADR-016 (hook block_gitignored por sinal do consumer `.gitignore`; postura "consumer signal first, escape hatch documentado"; pattern do consumer não-acomodado no plugin), ADR-023 (critério mecânico cumulativo para `disable-model-invocation` explícito em SKILLs; 3 critérios cumulativos; tabela retroativa às 9 skills), ADR-040 (hook block_settings_drift por content regex em `.claude/settings.json`; sucessor parcial lateral de ADR-015 família PreToolUse block hooks), ADR-045 (apex redesign — esta onda materializa § Decisão parte 1 § Implementação literal), ADR-046+ADR-047+ADR-048+ADR-049 (templates do pattern de migração validado em Ondas C+D+E+F; F4 lessons cond 5 isolada + F1 link rot 2 categorias reaplicadas), ADR-034 (critério adendo vs novo ADR — cond 5 sucessor parcial primário absorvendo 6 ADRs; cond 4 NÃO aplica per F4 Onda C; cond 1 NÃO aplica — ADR-045/-046/-047/-048/-049 ancestrais codificados), ADR-019 (qa-reviewer ↔ /gen-tests cross-ref; preservado vigente; categoria-b link rot doutrinal ativa identificada — substância "single source of truth, per ADR-008" deve estar em ADR-050 § Decisão (a)), ADR-020 + ADR-022 (preservados vigentes; citam ADR-013 como pattern "critério mecânico cumulativo" reusado — substância preservada em ADR-050 § Decisão (b)), ADR-027 (preservado vigente; cita ADR-008 + ADR-023 como decisões base — substância preservada), ADR-024 (categoria `docs/procedures/` — relevante por **ausência** aqui: cluster componentes plugin **não tem procedure file**; toda mecânica vive em SKILLs/agents/hooks + CLAUDE.md + philosophy.md).

Onda G (sétima) da redesign da camada doutrinal coordenada por `docs/plans/redesign-camada-doutrinal-charter.md`. **Quinta migração cluster temático** per ADR-045 § Decisão parte 1 § Implementação literal — Ondas C+D+E+F precederam (cutucadas, modo local, reviewers/curadoria, execução/run-plan).

Cluster componentes plugin é candidato natural pós-Onda F:

1. **Scope máximo ascendente** — 6 ADRs (vs 4 em D+F; 2 em C+E). Testa pattern em scope maior já tentado. Recomendado em NOTES 2026-05-31T10:31:48Z como teste de capacidade.
2. **Cluster coeso semanticamente em 3 sub-dimensões** — todos os 6 ADRs cobrem dimensões dos tipos canônicos do plugin (skills/agents/hooks + infra de validação):
   - **Skills convention** (ADR-008 + ADR-023) — naming + frontmatter convention; skills geradoras stack-agnósticas + declaração explícita `disable-model-invocation`.
   - **Hooks defensivos** (ADR-015 + ADR-016 + ADR-040) — 3 PreToolUse block hooks; sufixo `.env` + sinal do consumer `.gitignore` + content regex em `settings.json`; defesa em camadas.
   - **Infra do plugin** (ADR-013) — CI lint mínimo como categoria permitida; fronteira da frase canonical "no build/test/package" sem revogá-la.
3. **Cluster sem procedure file** — reaplica F9 lesson D+E+F (fronteira ADR-024 não aplica antecipadamente). Mecânica vive em SKILLs/agents/hooks + CLAUDE.md + philosophy.md + install.md.
4. **F4 lessons reaplicadas literal** — cond 5 primária isolada (sucessor parcial absorvendo 6 ADRs); cond 4 NÃO aplica (ADR-045 carrega categoria meta; ADR-050 é quinta instância); cond 1 NÃO aplica (ADR-045/-046/-047/-048/-049 ancestrais codificados); cond 2 NÃO aplica — regra central de cada ADR absorvido preservada integralmente; nenhum marcado como `Substituído`.
5. **F1 lesson reaplicada literal** — link rot em 2 categorias identificado pré-execução: (a) histórica via archive blockquote redirect; (b) doutrinal ativa via absorção no consolidado. ADR-019/-020/-022/-027 vigentes citam membros do cluster como autoridade — substância absorvida em ADR-050 fecha gap; ADRs vigentes mantêm-se imutáveis (link via archive resolve para ADR-050).

### Composição do cluster vs sketch original do charter

Charter sketch linha 238 (NOTES 2026-05-30T06:08:04Z, replicada em ADR-045 § Decisão parte 1 § Implementação):

```
ADR-001-componentes-plugin.md         # skills/agents/hooks como tipos canônicos,
                                      # naming + auto-gating triplo
                                      # (absorve atual: 008, 013, 016, 023, 040)
```

**Sketch absorvia 5 ADRs; Onda G inclui 6** (ADR-015 adicionado ao cluster). Inclusão cabe em ADR-045 § Decisão linha 56 fronteira *"absorção de ADR em consolidado diferente do sketch original"* como ajuste editorial — categoria livre durante execução das ondas.

- **ADR-015 (hook block_env por sufixo `.env`) INCLUÍDO** — omitido do sketch original aparentemente por descuido editorial. Pertence semanticamente à família PreToolUse block hooks (ADR-015 ancestral; ADR-016 + ADR-040 sucessores parciais laterais per ADR-034 cond 5). ADR-040 § Origem explícitamente cita "ADR-015 é o ancestral direto — primeiro PreToolUse block hook do plugin, estabelece pattern de gate por filename match com escape hatch documentado". Excluir ADR-015 do cluster componentes deixaria órfão um membro da família coesa.
- **Cluster mantém os outros 5 do sketch literal** (008+013+016+023+040) — composição não altera; apenas ADR-015 adicionado.

**Saldo:** Onda G absorve 6 ADRs (vs 5 do sketch). Inventário pós-Onda G: 37 - 6 archivados + 1 ADR-050 = **32 vigentes** (drop líquido de 5 nesta onda — maior drop até hoje; alinha com scope máximo do cluster). Documentação editorial post-merge consolida em charter § Atualização pós-execução conforme Notas operacionais abaixo.

**Linha do backlog:** Onda G é sub-scope da umbrella multi-onda em `## Próximos`; não corresponde a linha distinta. Per ADR-049 § Decisão (a) + precedente Ondas A+B+C+D+E+F, umbrella é atualizada in-place post-merge.

## Resumo da mudança

**Esta Onda G produz:**

1. **ADR-050 consolidado** (criado via `/new-adr` no /triage step 4) — absorve substância de ADR-008 + ADR-013 + ADR-015 + ADR-016 + ADR-023 + ADR-040 num único ADR temático "componentes plugin". § Decisão integra:
   - (a) **Skills geradoras stack-agnósticas via dispatch interno** (de ADR-008): skills geradoras (não hooks) perdem sufixo de stack; idioms vivem em sub-blocos por stack dentro do mesmo SKILL.md; skill detecta stack por marker (`pyproject.toml`/`build.gradle*`/`pom.xml`/`package.json`/`Cargo.toml`/`go.mod`); mecânica de detecção e fallback (marker único / ausente / múltiplos / stack sem sub-bloco); aplicação atual a `/gen-tests` (Python sub-bloco); **single source of truth** preservado per ADR-019 (qa-reviewer referencia sub-blocos canonical, não duplica).
   - (b) **CI lint mínimo como categoria distinta das 3 vetadas pela frase canonical** (de ADR-013): "Don't introduce a build system, package manager, or test runner" preservada intacta; CI lint mínimo de invariantes sintáticas/estruturais NÃO cabe em nenhuma das 3 categorias vetadas (não compila, não instala deps, não roda testes); 4 critérios cumulativos para classificar gate como permitido (sintático/estrutural; sem deps externas além do runtime base; sem behavior de produção; <30s wall-clock); cobertura positiva (`python -m json.tool` em manifests + `ast.parse` em hooks + assertions inline) vs negativa (suite testes; package install; build pipeline; schema validation completa; lint de estilo); pattern "critério mecânico cumulativo" reusado em ADR-020 + ADR-022 (preservados vigentes).
   - (c) **Hook PreToolUse block_env por sufixo `.env`** (de ADR-015): primeiro PreToolUse block hook do plugin; defesa universal por filename match — qualquer arquivo cujo nome termine em `.env` é bloqueado (cobre `.env`/`.env.production`/`1g.env`/`production.env`/`1g.integ.env`); exceção literal para `*.env.example` e templates após strip de `TEMPLATE_SUFFIXES`; política universal (não inspeciona conteúdo; não respeita carve-out de `.claude/` que aplica a block_gitignored); escape hatch documentado (template `*.env.example` + override fora do Claude).
   - (d) **Hook PreToolUse block_gitignored por sinal do consumer** (de ADR-016): segundo PreToolUse block hook; postura "consumer signal first" — `.gitignore` do consumer é fonte; sem heurística codificada substituindo o sinal; 7 alternativas rejeitadas (allowlist via config / `!entry` no gitignore / liberação por raiz / opt-in via env var / parser de padrões / lista hardcoded de extensões); pattern do consumer (script gitignored como entrypoint de workflow) **não-acomodado no plugin** — responsabilidade do consumer refatorar via Makefile/Docker/compose; carve-out de `.claude/` allowlisted (território do harness; load-bearing para modo local-gitignored per ADR-047).
   - (e) **Critério mecânico cumulativo para `disable-model-invocation` explícito em SKILLs** (de ADR-023): toda SKILL.md declara `disable-model-invocation` explicitamente no frontmatter (sem omissão) com valor dado por 3 critérios cumulativos para `false` (blast radius estritamente local pela ação direta; pushes/PRs gateados por enum upstream contam como local; sem risco de autoinvocação recursiva destrutiva cross-turn pelo modelo); `true` quando qualquer critério falha (ação direta cross-team; loop autoinvocado cross-turn); tabela retroativa às 9 skills shippadas — resultado universe: 9 declaram `false`, zero declaram `true`; herança editorial (skill nova esquecendo declaração herda critério via `code-reviewer` em PRs).
   - (f) **Hook PreToolUse block_settings_drift por content regex em `.claude/settings.json`** (de ADR-040): terceiro PreToolUse block hook; sucessor parcial lateral de ADR-015 (família PreToolUse block hooks); target file específico (`.claude/settings.json` only; `.claude/settings.local.json` fora de escopo); content patterns via regex bruta (`/home/[^/]+/` ou `/Users/[^/]+/`); escape hatch documentado (mover para `settings.local.json` / substituir por `$HOME`/`~` / editar fora do Claude); Windows fora de escopo desta versão (cláusula 4); friction recorrente empírica confirmada (`/insights` report 166 sessões); tensões com ADR-018 (território `.claude/`) + ADR-016 (consumer signal first) + ADR-015 § Alt (d) (content inspection no hot path) — defendidas em § Origem de ADR-040.
   - (g) **Pattern "critério mecânico cumulativo" como meta-doutrina herdada** — ADR-013 estabeleceu precedente; ADR-020 (warnings pré-loop, 3 cumulativos + 1 pré-requisito) e ADR-022 (archival docs/plans, 6 critérios cumulativos) reusaram pattern; ADR-023 (disable-model-invocation, 3 cumulativos) também reusa. ADR-050 § Decisão (b) preserva pattern editorial; ADR-020/-022/-027 vigentes seguem citando como referência.

   § Origem histórica preserva 6 incidentes empíricos: investigação cobertura teste multi-arquivo 2026-05-07 → ADR-008 (2 dores em gen-tests-python); auditoria + design-review batch 1 marketplace prep 2026-05-10 → ADR-013 (erros `$schema` 404 + `description` top-level rejeitada); smoke-test PJe TJPA fase 1 achado #1 → ADR-015 (`1g.env` com credenciais reais passando sem bloqueio); smoke-test PJe TJPA fase 1 achado #12 → ADR-016 (`build_pje.sh` falso-positivo); auditoria editorial 2026-05-12 + design-review plano tightening-editorial → ADR-023 (drift editorial em 5 skills omissas + 3 ambiguidades de wording); `/insights` report 2026-05-26 (166 sessões) → ADR-040 (cleanup cycles recorrentes em `.claude/settings.json`). § Gatilhos consolida triggers das 6 decisões. § Auto-aplicação cond 5 primária isolada per F4 Onda C/D/E/F.

   **Substância preservada para link rot doutrinal ativa categoria-b** — gap fechado quando ADRs vigentes citam membros do cluster archived:
   - ADR-019 cita "single source of truth, per ADR-008" → ADR-050 § Decisão (a) preserva "sub-blocos canonical no SKILL.md como single source of truth para idioms por stack; qa-reviewer referencia, não duplica".
   - ADR-020 + ADR-022 citam "pattern critério mecânico cumulativo de ADR-013" → ADR-050 § Decisão (b) + § Decisão (g) preserva pattern editorial herdado.
   - ADR-027 cita "decisão base ADR-008 (skill geradora cujo output é produto)" + "decisão base ADR-023 (disable-model-invocation explícito)" → ADR-050 § Decisão (a) preserva caminho stack-agnóstico para artefatos não-código + § Decisão (e) preserva critério mecânico cumulativo.
   - ADR-046 § Razões cita "ADR-023:53/67 cita ADR-017 § Editorial inheritance" — categoria histórica (ADR-017 archived, ADR-023 archived após Onda G; substância de herança editorial já em ADR-046).
   - ADR-047 § Origem cita "ADR-016 como autoridade para escopo literal preservado" — categoria histórica preserved (ADR-047 imutável; redirect ADR-016 → ADR-050 resolve).

2. **Archive de ADR-008, ADR-013, ADR-015, ADR-016, ADR-023, ADR-040** — `git mv` para `docs/decisions/archive/` + header redirect canonical (format de ADR-046): blockquote `> **ARCHIVED 2026-05-31** — content absorbed into [ADR-050](../ADR-050-<slug>.md); see that ADR for current authority.` + header H1 original preservado intacto abaixo.

3. **Archive index update** — `docs/decisions/archive/README.md` ganha 6 linhas novas na tabela (Onda G). Cada onda C-X estende a tabela como invariante codificada em ADR-046.

4. **Propagação de cross-refs em docs vivos** (7 arquivos; 9 ocorrências em 9 linhas distintas):
   - `CLAUDE.md` (3 linhas, 3 ocorrências; **hot spot meta-doutrinal**) — linha 86 (footnote "CI lint distinct category" → ADR-013) + linha 89 (bullet "disable-model-invocation em SKILL.md" → ADR-023) + linha 121 (tabela "Plugin component naming and hook auto-gating" → ADR-008). Bullets meta-doutrinais paralelos a ADR-010/-011/-026/-034/-043/-045/-048/-049 — reformulação narrativa preservando substância integralmente.
   - `docs/philosophy.md` (1 linha, 1 ocorrência) — linha 62 (§ Convenção de naming "Skills geradoras... per ADR-008") → ADR-050 § Decisão (a).
   - `docs/install.md` (1 linha, 1 ocorrência) — linha 73 (descrição do hook `block_settings_drift` "Per ADR-040") → ADR-050 § Decisão (f).
   - `skills/gen-tests/SKILL.md` (1 linha, 1 ocorrência) — linha 11 (descrição da skill "per ADR-008 — geradores stack-agnósticos via dispatch interno") → ADR-050 § Decisão (a).
   - `agents/design-reviewer.md` (1 linha, 1 ocorrência) — linha 100 (rubric "ADR-008 separou skills (genéricas) de hooks (suffixadas)") → ADR-050 § Decisão (a) + § Decisão (c-d-f) [hooks suffixados preservados].
   - `hooks/block_env.py` (1 linha, 1 ocorrência) — linha 9 (docstring "per ADR-015") → ADR-050 § Decisão (c).
   - `hooks/block_settings_drift.py` (1 linha, 1 ocorrência) — linha 9 (docstring "Per ADR-040") → ADR-050 § Decisão (f).

5. **Link rot consciente em docs imutáveis** — outros ADRs imutáveis e planos históricos citam ADR-008/-013/-015/-016/-023/-040 em § Origem como precedente ou cross-ref doutrinal (categoria (a) histórica de F1 lesson Onda C). Subset suspeito de categoria (b) doutrinal ativa identificado pré-execução (todos com substância absorvida em ADR-050; link via archive resolve):
   - ADR-019 § Decisão base + § Decisão (single source of truth, per ADR-008) + § Trade-offs + § Alternativas + § Gatilhos — substância em ADR-050 § Decisão (a).
   - ADR-020 § Investigação + § Contexto + § Razões + § Alternativas — substância "critério mecânico cumulativo" em ADR-050 § Decisão (b) + (g).
   - ADR-022 § Razões — substância em ADR-050 § Decisão (b) + (g).
   - ADR-027 § Decisão base (2 ocorrências) + § Decisão (stack-agnóstica) + § Decisão (disable-model-invocation) — substância em ADR-050 § Decisão (a) + (e).
   - ADR-034 + ADR-035 citam ADR-023 como meta-doutrina paralela — substância em ADR-050 § Decisão (e); ADR-034/-035 mantêm-se citando precedente editorial preservado.
   - ADR-042 § Alternativa B — substância "variação de runtime via parâmetro, não por verbo" em ADR-050 § Decisão (a).
   Hipótese de zero substância "doutrinal ativa" perdida — design-reviewer valida.

6. **Charter atualização** (post-merge, manual) — `docs/plans/redesign-camada-doutrinal-charter.md` § "Atualização pós-execução" tabela adiciona linha "Onda G — Migração cluster componentes plugin" + pattern editorial das Ondas F+G (Onda F exclusão de ADR-037+ADR-010; Onda G inclusão de ADR-015 vs sketch) como sinal a observar para ondas H-X; anti-regression checklist § Componentes do plugin + § Skills e fluxo + § Convenções editoriais atualizadas refletindo ADR-050 como nova autoridade. NÃO escopo desta Onda G; commit separado post-merge per precedente Ondas A-F.

**Pattern de migração validado nesta onda** (quinta aplicação):
- Cluster de 6 ADRs sem procedure file — **scope máximo até hoje** (vs 4 em D+F; 2 em C+E).
- **Inclusão de ADR-015 ao cluster vs sketch original** que o omitia — cabe em ADR-045 § Decisão linha 56 fronteira "absorção de ADR em consolidado diferente do sketch" como ajuste editorial livre.
- Hot spot meta-doutrinal em CLAUDE.md (3 ocorrências em 3 bullets paralelos a ADR-010/-011/-026/-034/-043/-045/-048/-049). Spread em 7 docs vivos (vs 5 em F; 6 em E; 9 em D — calibração intermediária).
- F4 lessons reaplicadas literal (cond 5 isolada; cond 4 NÃO aplica; cond 1 NÃO aplica; cond 2 NÃO aplica — regra central de cada ADR absorvido preservada integralmente; nenhum marcado como `Substituído`).
- F1 lesson reaplicada literal (link rot 2 categorias; categoria-b doutrinal ativa identificada pré-execução; substância absorvida em ADR-050).
- **Pendência operacional Onda F endereçada:** aderir reviewer-per-bloco estrito mesmo com pattern editorial convergente. Bloco 1 (archive) com `{reviewer: doc}` invocado obrigatoriamente — convergência empírica em Ondas C+D+E+F não admite exceção à doutrina explícita "Não pular revisor".

## Arquivos a alterar

### Bloco 1 — Archive 6 ADRs + archive index extension {reviewer: doc}

**Instrução para data dinâmica:** substituir `2026-05-31` no template do blockquote pela data de execução (formato `YYYY-MM-DD` do dia de aplicação) ao replicar em cada um dos 6 arquivos arquivados — pattern Ondas C+D+E+F. Hardcode abaixo é placeholder.

- `git mv docs/decisions/ADR-008-skills-geradoras-stack-agnosticas.md docs/decisions/archive/`
- Editar topo do arquivo movido inserindo blockquote redirect **antes** do `# ADR-008: <título original>`:

  ```markdown
  > **ARCHIVED 2026-05-31** — content absorbed into [ADR-050](../ADR-050-componentes-plugin-consolidado.md); see that ADR for current authority. Body below preserved verbatim for historical record.

  # ADR-008: Skills geradoras stack-agnósticas via dispatch interno
  ```

- `git mv docs/decisions/ADR-013-ci-lint-minimo-no-build-runner.md docs/decisions/archive/` + análogo.
- `git mv docs/decisions/ADR-015-bloquear-env-files-por-sufixo.md docs/decisions/archive/` + análogo.
- `git mv docs/decisions/ADR-016-manter-block-gitignored-scripts-no-consumer.md docs/decisions/archive/` + análogo.
- `git mv docs/decisions/ADR-023-criterio-mecanico-disable-model-invocation-skills.md docs/decisions/archive/` + análogo.
- `git mv docs/decisions/ADR-040-block-settings-drift-paths-absolutos-via-hook.md docs/decisions/archive/` + análogo.
- Estender tabela em `docs/decisions/archive/README.md` adicionando 6 linhas (Onda G):

  ```markdown
  | ADR-008 — Skills geradoras stack-agnósticas via dispatch interno | [ADR-050](../ADR-050-componentes-plugin-consolidado.md) | G |
  | ADR-013 — CI lint mínimo como complemento à doutrina no-build/runner | [ADR-050](../ADR-050-componentes-plugin-consolidado.md) | G |
  | ADR-015 — Bloquear env-files por sufixo `.env`, não apenas dotfile | [ADR-050](../ADR-050-componentes-plugin-consolidado.md) | G |
  | ADR-016 — Manter `block_gitignored` como está; falso-positivo em scripts operacionais é problema do consumer | [ADR-050](../ADR-050-componentes-plugin-consolidado.md) | G |
  | ADR-023 — Critério mecânico para declaração explícita de `disable-model-invocation` em skills | [ADR-050](../ADR-050-componentes-plugin-consolidado.md) | G |
  | ADR-040 — Bloquear paths absolutos em `.claude/settings.json` via PreToolUse hook | [ADR-050](../ADR-050-componentes-plugin-consolidado.md) | G |
  ```

### Bloco 2 — CLAUDE.md + philosophy.md cross-refs (hot spot meta-doutrinal) {reviewer: doc}

- `CLAUDE.md` linha 86 (footnote do bullet "Don't introduce a build system"): substituir "see [ADR-013](docs/decisions/ADR-013-ci-lint-minimo-no-build-runner.md)" por "see [ADR-050](docs/decisions/ADR-050-componentes-plugin-consolidado.md) § Decisão (b)".
- `CLAUDE.md` linha 89 (bullet "**`disable-model-invocation` em SKILL.md**"): reformulação narrativa similar a pattern Onda F Modo runbook — "critério mecânico cumulativo em [ADR-023](...)" → "critério mecânico cumulativo em [ADR-050](docs/decisions/ADR-050-componentes-plugin-consolidado.md) § Decisão (e)". Substância (blast radius local + pushes/PRs gateados por enum upstream + sem autoinvocação cross-turn → `false`; tabela retroativa às 9 skills; herança editorial para skills novas com `true` justificado) preservada literal.
- `CLAUDE.md` linha 121 (tabela "Plugin component naming and hook auto-gating", coluna "Stack-specific" para Skills row): substituir "(per [ADR-008](docs/decisions/ADR-008-skills-geradoras-stack-agnosticas.md))" por "(per [ADR-050](docs/decisions/ADR-050-componentes-plugin-consolidado.md) § Decisão (a))".
- `docs/philosophy.md` linha 62 (§ Convenção de naming bullet "Skills geradoras"): substituir "Critério canônico em [ADR-008](decisions/ADR-008-skills-geradoras-stack-agnosticas.md)" por "Critério canônico em [ADR-050](decisions/ADR-050-componentes-plugin-consolidado.md) § Decisão (a)".

### Bloco 3 — install.md + agents/design-reviewer + skills/gen-tests + hooks docstrings {reviewer: doc}

- `docs/install.md` linha 73 (descrição do hook `block_settings_drift`): substituir "Per [ADR-040](decisions/ADR-040-block-settings-drift-paths-absolutos-via-hook.md)" por "Per [ADR-050](decisions/ADR-050-componentes-plugin-consolidado.md) § Decisão (f)".
- `skills/gen-tests/SKILL.md` linha 11 (descrição da skill): substituir "per [ADR-008](../../docs/decisions/ADR-008-skills-geradoras-stack-agnosticas.md) — geradores stack-agnósticos via dispatch interno" por "per [ADR-050](../../docs/decisions/ADR-050-componentes-plugin-consolidado.md) § Decisão (a) — geradores stack-agnósticos via dispatch interno".
- `agents/design-reviewer.md` linha 100 (rubric "Componentes do plugin"): substituir "ADR-008 separou skills (genéricas) de hooks (suffixadas)" por "ADR-050 § Decisão (a) separou skills (genéricas) de hooks (suffixados, per § Decisão (c-d-f))".
- `hooks/block_env.py` linha 9 (docstring): substituir "per ADR-015" por "per ADR-050 § Decisão (c)".
- `hooks/block_settings_drift.py` linha 9 (docstring): substituir "Per ADR-040" por "Per ADR-050 § Decisão (f)".

## Verificação end-to-end

**Critérios de sucesso da Onda G:**

1. **ADR-050 criado** com Status `Proposto` em `docs/decisions/ADR-050-componentes-plugin-consolidado.md`. § Origem cita ADR-008+ADR-013+ADR-015+ADR-016+ADR-023+ADR-040 como decisões absorvidas + ADR-045/-046/-047/-048/-049 como templates + ADR-019/-020/-022/-027 como vigentes preservados citando substância. § Decisão integra as 7 dimensões (a-g) sob narrativa única coerente. § Origem histórica preserva os 6 incidentes empíricos. § Gatilhos consolida triggers das 6 decisões. § Auto-aplicação cond 5 primária isolada; cond 4 NÃO aplica; cond 1 NÃO aplica; cond 2 NÃO aplica (regra central preservada integralmente; nenhum ADR marcado como Substituído).

2. **ADR-008, ADR-013, ADR-015, ADR-016, ADR-023, ADR-040 arquivados:** `ls docs/decisions/ADR-008-*.md docs/decisions/ADR-013-*.md docs/decisions/ADR-015-*.md docs/decisions/ADR-016-*.md docs/decisions/ADR-023-*.md docs/decisions/ADR-040-*.md` → vazio (movidos). `ls docs/decisions/archive/ADR-008-*.md ...` → presentes (6 arquivos). Header redirect canonical no topo de cada arquivo, H1 original intacto abaixo.

3. **Archive index estendido:** `docs/decisions/archive/README.md` carrega tabela com 18 linhas (2 Onda C + 4 Onda D + 2 Onda E + 4 Onda F + 6 Onda G), ordem cronológica por onda preservada.

4. **`grep "ADR-008\|ADR-013\|ADR-015\|ADR-016\|ADR-023\|ADR-040" CLAUDE.md docs/philosophy.md` → 0 matches** (4 ocorrências substituídas).

5. **`grep "ADR-008\|ADR-013\|ADR-015\|ADR-016\|ADR-023\|ADR-040" docs/install.md skills/gen-tests/SKILL.md agents/design-reviewer.md hooks/block_env.py hooks/block_settings_drift.py` → 0 matches** (5 ocorrências substituídas).

6. **Substância preservada para link rot doutrinal ativa categoria-b:**
   - `grep "single source of truth" docs/decisions/ADR-050-*.md` → ≥1 match (ADR-019 link rot fechado via absorção em § Decisão (a)).
   - `grep "critério mecânico cumulativo" docs/decisions/ADR-050-*.md` → ≥2 matches (ADR-020/-022 link rot fechado via absorção em § Decisão (b) + (g)).
   - `grep "blast radius\|disable-model-invocation" docs/decisions/ADR-050-*.md` → ≥2 matches (ADR-027 link rot fechado via absorção em § Decisão (e)).

7. **ADR-019, ADR-020, ADR-022, ADR-027, ADR-034, ADR-035, ADR-042 preservados vigentes:** `ls docs/decisions/ADR-019-*.md ADR-020-*.md ADR-022-*.md ADR-027-*.md ADR-034-*.md ADR-035-*.md ADR-042-*.md` → 7 arquivos presentes (não arquivados; mantêm cross-refs a ADRs do cluster como autoridade histórica via redirect canonical).

8. **Mecânica de hooks preservada:** `python3 -c "import ast; ast.parse(open('hooks/block_env.py').read())"` + análogos para `block_gitignored.py` e `block_settings_drift.py` → sem erros (apenas docstrings editadas; comportamento intacto).

9. **Frase canonical do CLAUDE.md preservada intacta:** `grep "Don't introduce a build system, package manager, or test runner" CLAUDE.md` → 1 match (frase canonical preservada literal per ADR-013 → ADR-050 § Decisão (b) fronteira não-revogada).

9.bis **Parêntese-anexo da frase canonical preservado com cross-ref atualizado:** `grep -c "(Manifest/syntax invariant checks via CI lint" CLAUDE.md` → 1 match (sub-cláusula que ancora ponteiro à fronteira codificada em ADR-050 § Decisão (b) não removida por engano). Ponteiro à fronteira é load-bearing — sem ele, leitor futuro entende frase canonical sem a exceção codificada.

10. **Tabela "Plugin component naming and hook auto-gating" preservada:** `grep -E "^\| (Hook|Skill|Agent)" CLAUDE.md` → 3 matches (3 linhas da tabela preservadas; apenas cross-ref de Skills row atualizado).

10.bis **Cross-ref da coluna "Stack-specific" da row Skill atualizado corretamente:** `grep -E "internal stack sub-blocks \(per \[ADR-050\]" CLAUDE.md` → 1 match (substituição do cross-ref preservou estrutura da célula sem remover o ponteiro à fonte canonical da convenção).

11. **Link rot em immutable ADRs aceito explicitamente:** `grep -l "ADR-008\|ADR-013\|ADR-015\|ADR-016\|ADR-023\|ADR-040" docs/decisions/ADR-0*.md docs/plans/*.md` ainda retornará vários arquivos antigos — esses são imutáveis (immutable ADRs + historical plans); cross-refs em immutable docs ficam como registro histórico, NÃO são editados.

12. **CHANGELOG.md intacto** (registro histórico imutável) — `grep "ADR-008\|ADR-013\|ADR-015\|ADR-016\|ADR-023\|ADR-040" CHANGELOG.md` retorna matches preservados como registro de versionamento; NÃO editar.

13. **doc-reviewer audita drift cross-doc:** cross-refs corretos cross-doc; ADR-050 substância fiel a ADR-008+ADR-013+ADR-015+ADR-016+ADR-023+ADR-040 combinados; nenhuma carga doutrinal da § Componentes do plugin + § Skills e fluxo + § Convenções editoriais do anti-regression checklist perdida (skills geradoras stack-agnósticas + CI lint mínimo permitido + 3 hooks defensivos + critério `disable-model-invocation` + pattern "critério mecânico cumulativo" — todas preservadas em ADR-050).

14. **design-reviewer auto-fire em /new-adr step 5 e /triage step 5** valida: padrão de migração coerente com ADR-045 § Decisão parte 1; inclusão de ADR-015 ao cluster coerente per ADR-045 § Decisão linha 56 fronteira "absorção de ADR em consolidado diferente do sketch original"; pattern reusable em cluster com hot spot meta-doutrinal em CLAUDE.md; auto-aplicação per ADR-034 (cond 5 primária; cond 4 NÃO aplica; cond 1 NÃO aplica; cond 2 NÃO aplica — regra central preservada) coerente; gap `block_gitignored.py` (NOTES 2026-05-30T05:26:59Z) preservado como Limitação em ADR-050 § Limitações.

## Notas operacionais

**Ordem dos blocos:** Bloco 1 (archive) executado antes dos demais — outros blocos referenciam ADR-050 que substitui os 6 arquivos arquivados. Blocos 2-3 podem rodar em qualquer ordem (independentes entre si após archive); Bloco 2 (CLAUDE.md + philosophy.md, hot spot meta-doutrinal) tem maior risco editorial por concentrar 4 das 9 ocorrências em bullets meta-doutrinais paralelos a 8 outros bullets cross-ref existentes.

**Aderir reviewer-per-bloco estrito (lição operacional Onda F):** Bloco 1 (archive) DEVE invocar `doc-reviewer` obrigatório — convergência empírica em Ondas C+D+E+F não admite exceção à doutrina explícita "Não pular revisor, mesmo em bloco trivial" de `skills/run-plan/SKILL.md § O que NÃO fazer`. Mesmo pattern editorial validado em 4 ondas anteriores não justifica skip — pendência operacional Onda F (Bloco 1 commitado sem doc-reviewer) endereçada como invariante desta onda.

**Validação da composição do cluster:** se design-reviewer flagrar gap na composição (ex.: inclusão de ADR-015 inconsistente; falta de coesão entre 3 sub-dimensões skills/hooks/infra; inclusão sem caber em ADR-045 § Decisão linha 56 fronteira "absorção de ADR em consolidado diferente do sketch"), composição é editorial do plano antes de prosseguir. Mudança estrutural na regra de consolidação seria gatilho de revisão de ADR-045.

**Charter atualização post-merge:** após merge da Onda G, atualizar `docs/plans/redesign-camada-doutrinal-charter.md` § "Atualização pós-execução":
- Estender tabela de ondas com linha "Onda G — Migração cluster componentes plugin" (commit hash + PR + substância + composição inclui ADR-015 vs sketch original).
- Anti-regression checklist § Componentes do plugin + § Skills e fluxo + § Convenções editoriais — atualizar referências a "ADR-008/-013/-015/-016/-023/-040" para "ADR-050 § Decisão (a/b/c/d/e/f/g)" (substância preservada; apenas apontador).
- Documentar pattern editorial das ondas F+G em sub-seção dedicada: Onda F refinou por exclusão (ADR-037 + ADR-010 fora do cluster); Onda G inclui ADR-015 vs sketch que omitia. Ambos casos cabem em ADR-045 § Decisão linha 56 ("ajuste de cluster sequence, subdivisão, absorção em consolidado diferente do sketch"). Sinal de meta-pattern emergente para considerar em ondas H-X ou em ADR sucessor de ADR-045 se 3ª aplicação aparecer (gatilho de revisão do próprio ADR-045 a observar).
- Saldo inventário pós-Onda G: estimado **32 vigentes** (37 pós-F + 1 ADR-050 - 6 arquivados); drop líquido de 5 (maior drop até hoje; alinha com scope máximo do cluster).
- Anotação progressiva: "Onda G shipped — commit <hash>; cluster componentes plugin migrado com inclusão de ADR-015 vs sketch e pendência operacional Onda F endereçada".

Update do charter é commit separado post-merge (paralelo às atualizações de umbrella in BACKLOG das Ondas A+B+C+D+E+F); NÃO escopo desta Onda G.

**Decisão excluída — procedure file não criado:** cluster componentes plugin NÃO ganha procedure file equivalente a `cutucada-descoberta.md` (apenas Onda C teve). F9 lesson reaplicada: fronteira ADR-024 não aplica antecipadamente. Mecânica de skills/hooks/infra vive em SKILLs + agents + hooks + CLAUDE.md + philosophy.md + install.md.

**Decisão excluída — ADR-019 NÃO absorvido apesar de cross-ref ativo a ADR-008:** ADR-019 (qa-reviewer ↔ /gen-tests cross-ref) cita ADR-008 como "Decisão base" e "single source of truth, per ADR-008" em múltiplas ocorrências. Categoria semântica distinta: ADR-019 codifica relação **inter-componente** (reviewer ↔ skill geradora), não convenção interna do plugin (skills/hooks/infra). Pertenceria a futuro cluster "reviewers/curadoria" se houver expansão; cluster Onda E já consolidou reviewers (ADR-048) sem absorver ADR-019. ADR-019 permanece como ADR clássico vigente; cross-ref a ADR-008 archived resolve via redirect canonical para ADR-050 § Decisão (a).

**Decisão excluída — ADR-027 NÃO absorvido apesar de decisões base ADR-008 + ADR-023:** ADR-027 (`/draft-idea` skill) cita ADR-008 + ADR-023 como decisões base. Categoria semântica distinta: ADR-027 codifica skill **específica** (`/draft-idea`), não convenção interna geral aplicável a todas as skills. Pertenceria a futuro cluster "skills produto" ou permanece standalone. ADR-027 permanece vigente; cross-refs resolvem via redirect canonical.

**Decisão excluída — ADR-020 + ADR-022 NÃO absorvidos apesar de pattern "critério mecânico cumulativo" herdado de ADR-013:** ADR-020 (warnings pré-loop) e ADR-022 (archival docs/plans) reusam pattern editorial de ADR-013 mas codificam decisões **distintas** em domínios distintos. Pertencem a clusters semânticos diferentes (`/run-plan` warnings; `/archive-plans` política). ADR-050 § Decisão (g) preserva pattern editorial; ADR-020/-022 vigentes mantêm-se citando pattern via referência ao consolidado.

**Sinal a observar para ondas H-X:** Onda F + Onda G aplicaram refinamentos editoriais à composição do cluster (Onda F exclusão de ADR-037 + ADR-010; Onda G inclusão de ADR-015). Ambos casos cabem em ADR-045 § Decisão linha 56 fronteira "absorção de ADR em consolidado diferente do sketch" como ajuste editorial livre. Se 3ª aplicação aparecer em Ondas H-X, considerar se merece codificação explícita via ADR sucessor de ADR-045 (gatilho de revisão do próprio ADR-045). Por ora, decisões editoriais por onda continuam no charter § Atualização pós-execução; não há meta-pattern formal codificado.

**Gap `block_gitignored.py` preservado como Limitação** — NOTES 2026-05-30T05:26:59Z documentou gap operacional onde mensagem do hook assume 3 categorias enumeradas (dependency, build artifact, local cache) sem reconhecer 4ª categoria (store doutrinário declarado por ADR-047 + ADR-032 — `.claude/local/` como source primária de captura). Endereçamento ainda pendente; preservar espaço de extensão em ADR-050 § Limitações (não consolidar como decidido nesta onda). Charter linha 87 já antecipou esta preservação.

**Cap de ondas estimado:** charter previa 6-10 ondas. Pós-Onda G (sétima), trajetória esperada: G + 3-5 ondas H-X adicionais. Cluster sequence revisitada — candidatos remanescentes após Onda G: convenções editoriais (ADR-007+012+024+034, 4 heterogêneos); alinhamento/triage (ADR-009+011+026+027+038+042, 6 ADRs com constraint always-include de ADR-048 sobre ADR-009); discoverability/branding (ADR-037 + ?); brainstorm (ADR-036 standalone); apex (ADR-035+ADR-043+ADR-045+ADR-046+ADR-047+ADR-048+ADR-049+ADR-050 — meta-cluster apex que pode ou não consolidar).

**Sinal de saúde:** se Bloco 2 (CLAUDE.md + philosophy.md hot spot meta-doutrinal) gerar ≥10 findings de doc-reviewer, sinal de que reformulação narrativa precisa refinamento antes de aplicar a cluster apex meta-cluster (Onda H ou later candidate). Pausar e iterar conforme charter linha 154.

## Decisões absorvidas

- ADR-050 § Decisão (a) "Single source of truth": substância atribuída a ADR-008 (decisão original) em vez de ADR-019; ADR-019 vigente referenciado como preservado via cross-ref que resolve para esta dimensão (caminho-único).
- ADR-050 § Decisão (e): tabela retroativa às 9 skills shippadas reproduzida literal de ADR-023 § Aplicação (não apenas agregado "9 false / 0 true") — preserva template de classificação para skills futuras (caminho-único).
- ADR-050 § Origem critério editorial + § Auto-aplicação cond 2: pseudo-categoria "absorção consolidatória" removida; cond 2 de ADR-034 lida-se literalmente — "regra central preservada; nenhum ADR marcado como Substituído; nenhuma inversão" (caminho-único).
- ADR-050 § Decisão (b) "Frontmatter parse": reescrito removendo ambiguidade temporal de "primeira iteração" — "permanece fora da cobertura atual do CI lint conforme decisão original (escopo controlado da primeira iteração)" (caminho-único).
- Plano Bloco 1: instrução explícita para substituir data hardcoded `2026-05-31` pela data de execução ao replicar blockquote em cada um dos 6 arquivos arquivados (caminho-único).
- Plano Verificações 9.bis + 10.bis adicionadas: parêntese-anexo da frase canonical do CLAUDE.md preservado com cross-ref atualizado + cross-ref da coluna "Stack-specific" da row Skill atualizado corretamente (caminho-único).
- ADR-050 § Refinamento editorial removido + plano referências a "pattern editorial bidirecional para ondas H-X" reformuladas como "sinal a observar" no charter post-merge (operador escolheu opção (a) sobre (b) ADR-051 dedicado / (c) cross-ref a gatilho de revisão; meta-pattern editorial vive no charter, não no ADR temático componentes plugin).

## Pendências de validação

- ~~**Cobertura ausente** (warning pré-loop conservador): `hooks/block_env.py` + `hooks/block_settings_drift.py` listados em `## Arquivos a alterar` (Bloco 3) sem test pattern correspondente. Edit foi **APENAS docstring** (linha 9 dos 2 hooks: `per ADR-015`/`Per ADR-040` → `per ADR-050 § Decisão (c)`/`§ Decisão (f)`); comportamento dos hooks intacto, validado pré-commit via Verificação 8 do plano (`python3 -c "import ast; ast.parse(...)"` em `block_env.py` + `block_gitignored.py` + `block_settings_drift.py` — `all 3 OK`). Plugin sem suite (`test_command: null` per CLAUDE.md "Pragmatic Toolkit"). Captura é defensiva — material improvável. Reabrir se incidente concreto pós-merge observado em comportamento dos hooks.~~ **Encerrada 2026-06-14:** re-validação AST parse executada via Lote 3 do `/session-audit` desta sessão CC — `python3 -c "import ast; ast.parse(open('hooks/block_env.py').read())"` retornou OK; mesmo comando em `block_gitignored.py` e `block_settings_drift.py` retornou OK. Comportamento dos hooks intacto pós-merge confirmado mecanicamente. Captura defensiva validada — material improvável continua a ser improvável.
