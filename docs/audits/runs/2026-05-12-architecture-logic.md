# Auditoria — arquitetura & lógica — 2026-05-12

Modo: diagnóstico + propostas, **zero alteração**. Prompt: `docs/audits/architecture-logic.md`. Pré-checagem: `BACKLOG.md ## Concluídos` + `docs/decisions/` (ADR-001 a ADR-019, último datado 2026-05-12 — o próprio ADR-019 fechou parte da duplicação reviewer↔gen-tests).

Estado do repo no momento da auditoria: v2.4.0, 8 skills, 5 agents, 3 hooks, 19 ADRs, ~3 itens em `## Próximos`, ~55 planos em `docs/plans/`, CI lint mínimo ativo (`.github/workflows/validate.yml` per ADR-013).

---

## 1. Mapa de componentes & relações

### Skills (8)

| Skill | Linhas | `roles.required` | `roles.informational` | Cutucada descoberta | Invoca |
|---|---|---|---|---|---|
| `/triage` | 197 | `plans_dir` | `backlog`, `ubiquitous_language`, `design_notes`, `decisions_dir`, `product_direction` | sim | `/new-adr` (Skill tool), `@design-reviewer` (auto, ADR-011) |
| `/run-plan` | 170 | `plans_dir` | `backlog`, `test_command` | sim | `code-reviewer` (default), `qa-reviewer`, `security-reviewer`, `doc-reviewer` por anotação |
| `/new-adr` | 99 | `decisions_dir` | — | sim | `@design-reviewer` (auto, ADR-011) |
| `/next` | 86 | `backlog` | `product_direction`, `plans_dir` | sim | `/triage` (step 7); auto-detect forge (`gh`/`glab`) para filtrar PRs em curso |
| `/debug` | 115 | — | `test_command`, `ubiquitous_language`, `decisions_dir`, `design_notes` | não | nenhuma; usa `TaskCreate` (ADR-010) e `Monitor` |
| `/gen-tests` | 169 | — | `ubiquitous_language`, `design_notes` | não | nenhuma; sub-blocos Python + Java (ADR-008) |
| `/release` | 159 | — | `version_files`, `changelog` | não | referência cruzada a `/triage §0` (cleanup pós-merge); auto-detect forge |
| `/init-config` | 127 | (sem `roles:` — **define** o bloco config) | — | **não emite** (ADR-017 exceção) | nenhuma; passo 4.5 mexe em `.worktreeinclude` (ADR-018) |

### Agents (5)

| Agent | Linhas | Quem invoca | Quando | Free-read |
|---|---|---|---|---|
| `code-reviewer` | 77 | `/run-plan` default | sem anotação `{reviewer:}` no bloco | não |
| `qa-reviewer` | 58 | `/run-plan` | `{reviewer: qa}` ou bloco com testes | sub-bloco `/gen-tests` da stack detectada (ADR-019, lazy) |
| `security-reviewer` | 53 | `/run-plan` | `{reviewer: security}` | não |
| `doc-reviewer` | 61 | `/run-plan` | `{reviewer: doc}` ou bloco doc-only | varre `*.md`/`*.rst`/`*.txt` do repo (única exceção entre diff-level) |
| `design-reviewer` | 76 | `/triage` (auto), `/new-adr` (auto), `@-mention` | pré-fato em plano/ADR draft (ADR-011) | **todos os ADRs + `philosophy.md` por invocação** (ADR-009) |

### Hooks (3) — `hooks/hooks.json`

| Hook | Evento | Gates | ADR aplicável |
|---|---|---|---|
| `block_env.py` | PreToolUse Edit\|Write | sufixo `.env`/`<x>.env`, exceção `.env.example` + `TEMPLATE_SUFFIXES` | ADR-015 |
| `block_gitignored.py` | PreToolUse Edit\|Write | triplo (file_path vazio / não-git / `git` ausente) + allowlist `<repo>/.claude/` | ADR-005, ADR-016 |
| `run_pytest_python.py` | PostToolUse Edit\|Write | triplo (extensão `.py` / `pyproject.toml` ancestral / `uv` ou `python -m pytest`) | (sem ADR — invariante histórica) |

### Doctrine sources + estado

- `philosophy.md` (77 linhas) — princípios.
- `CLAUDE.md` (171 linhas) — operating instructions, role contract, Resolution protocol, AskUserQuestion mechanics, naming + auto-gating, cutucada de descoberta, Pragmatic Toolkit schema. Auto-loaded a cada turn.
- `templates/plan.md` (57 linhas) — único template centralizado (ADR-001 escopo limitado).
- `docs/decisions/ADR-001..019` — registro estrutural.
- `docs/plans/` — ~55 planos históricos (gatilho ADR-014 ≥100).
- `docs/audits/` — prompts de auditoria reutilizáveis (categoria fora da taxonomia formal skills/agents/hooks).
- `BACKLOG.md` — `## Próximos` (curadoria) + `## Concluídos` (registro editorial append-only). State of in-flight em git/forge (ADR-004).
- `.worktreeinclude` — tracked aqui, contém `.claude/` (consumer self-host de modo local).
- `.github/workflows/validate.yml` — CI lint mínimo (ADR-013).

### Cadeias notáveis

- **`/triage` → `/new-adr` → `@design-reviewer`** (ADR-011): `/triage` passo 6 reconhece que `/new-adr` já cobriu o reviewer no caminho ADR-only delegado; evita dispatch duplo.
- **`/next` → `/triage`** (step 7): orientação de sessão alimenta alinhamento.
- **Plano grava → `/run-plan` repassa → reviewer valida** (`philosophy.md:75`): pipeline `**Termos ubíquos tocados:**`.
- **`qa-reviewer` lê sub-bloco `/gen-tests`** (ADR-019, lazy): cross-reference em vez de duplicar idioms.
- **`/triage §0` ↔ `/release` cleanup**: `/release` referencia textualmente o passo 0 do `/triage`. Cross-reference inter-skill.

### Gates ativos por skill

| Skill | Gates `AskUserQuestion` (caminho-comum) |
|---|---|
| `/triage` | Cleanup (multi por candidato) → Commit (caminho-com-plano cobre push) → Backlog (consolidação só com flag) → opcional Editar bifurcação |
| `/run-plan` | Validação manual → Docs sanity (só se não-skip) → Publicar → Forge confirmação (se push+PR) |
| `/new-adr` | Numeração (só se mista) — caso raro |
| `/next` | Próximo (3 + Other) → Movimentações (só se moveu) |
| `/debug` | Onde/Reprod/Mudou (unificado, só se sintoma vago) |
| `/gen-tests` | Stack (só se marker ausente) → Fixture/Mock (decisões locais por stack) |
| `/release` | Branch (só se ≠ default) → Release (bump) → Release (Aplicar/Editar/Cancelar) → Forge (após push) |
| `/init-config` | Config (Editar/Cancelar se bloco existe) → 4 questions unificadas |

---

## 2. Diagnóstico por critério

### 2.1 Funcionalidade & simplicidade arquitetural

**Forte.** Cluster de 19 ADRs em ~6 dias úteis (2026-05-06 a 2026-05-12) consolidou doutrina: state em git/forge (ADR-004), frontmatter `roles:` (ADR-003), modo local (ADR-005), enum-first (ADR-006), idioma por audiência (ADR-007/012), skills geradoras stack-agnósticas (ADR-008), design-reviewer pré-fato (ADR-009/011), Tasks (ADR-010), cutucada de descoberta uniforme (ADR-017), `.worktreeinclude` proativo (ADR-018), reviewer↔skill cross-ref (ADR-019). Cobertura ampla; cada ADR fecha classe de problema com gatilhos de reabertura concretos.

**Pontos de atenção:**

- **(F1) `/triage` passo 5 (Consolidação do backlog)** é um passo dedicado que faz skip silente quando não detecta flags de duplicata/obsolescência. Frequência real de ativação plausivelmente baixa (depende de operador gravar item que sobrepõe item pré-existente). Anatômico: é sub-fluxo do passo 4 (gravar BACKLOG), não fase própria. Custo: ~13 linhas de prosa que poucos runs exercitam.
- **(F2) `/triage` step 0 Cleanup pós-merge** (~30 linhas detalhadas) referenciado por `/release § Cleanup pós-merge`. Cross-reference em vez de duplicar — bom — mas /release agora depende textualmente da localização precisa em `/triage`. Acoplamento editorial: mover passo 0 em /triage exige acompanhar /release.
- **(F3) `/run-plan` cross-mode `backlog: local + plans_dir: canonical`** carrega branch dedicado em /triage step 4 (omitir `**Linha do backlog:**`) e /run-plan 3.4 (skip + mensagem `"backlog em modo local com plano canonical — registro em ## Concluídos pulado para evitar leak"`). Caso edge altamente improvável (operador deliberadamente combinou modos divergentes). Defesa contra cenário raro custa ~10 linhas de prosa cross-skill + risco de drift se um lado mudar e outro não.
- **(F4) `/init-config` é único skill que muta arquivos do consumer sem produzir artefato declarado em `roles:`** (modifica `CLAUDE.md` para gravar config + `.worktreeinclude` para invariante de modo local per ADR-018). Categoria implícita "skill de setup" não tem doutrina formal — funciona hoje como single data point.

### 2.2 Alinhamento à `philosophy.md`

**Forte.** Flat & pragmático honrado em decisões consistentes:

- Hooks sem flags nem env vars (ADR-016 reforçou descartando 7 alternativas).
- YAGNI sobre helper compartilhado de cutucada (ADR-017 § Alternativa g, aceito 4× duplicação).
- ADR-014 descartou refatoração `main`/`dev`/orphan publish por custo desproporcional.
- ADR-013 abriu fronteira de CI lint sem editar frase canonical do CLAUDE.md (cross-ref, não exceção).
- `/init-config` modifica `.worktreeinclude` automaticamente sem `AskUserQuestion` (ADR-018: operação tem resultado óbvio, sem trade-off cross-team).
- Postura editorial não-reparativa do `/init-config`: não cria `CLAUDE.md`, não toca `.gitignore` automaticamente (ADR-018 critério distintivo).

**Pontos de atenção:**

- **(A1)** Frontmatter `disable-model-invocation`: declarado `false` em /run-plan, /new-adr, /release. **Ausente** em /triage, /debug, /gen-tests, /next, /init-config. BACKLOG ## Concluídos registrou a doutrina parcial ("blast radius real é baixo... troca para false") apenas para as 3 primeiras. As outras 5 ficaram sem doutrina formalizada — drift editorial entre frontmatters do mesmo plugin.
- **(A2)** `docs/audits/` como categoria — prompts reutilizáveis fora da taxonomia formal (skills/agents/hooks). Convivem bem hoje (2 prompts + diretório `runs/`), mas sem doutrina (ADR ou seção CLAUDE.md) explicando quando justifica criar um audit novo vs ADR vs skill. Single data point — YAGNI.

### 2.3 Efetividade das funcionalidades

**Forte:**

- ADR-013 CI lint funcional via `.github/workflows/validate.yml` — JSON parse + chaves obrigatórias + Python AST. Fechou classe "release quebrada por typo" sem suite de testes.
- ADR-018 `/init-config` passo 4.5 + safety net `/run-plan` SKILL.md:36 — defesa em camadas mínima, atrito do PJe resolvido.
- ADR-019 carregamento lazy `qa-reviewer` ↔ `/gen-tests` — sem inflação de tokens.
- ADR-010 Tasks aplicado a `/run-plan` loop + `/debug` ledger; outros skills isentos por critério "<10s típicos".

**Pontos de atenção:**

- **(E1) Free-read do `design-reviewer` em escala perigosa.** 19 ADRs hoje. ADR-011 gatilho explícito: "ADRs ultrapassar ~30" → reabrir trade-off de tokens. Crescimento observado: ADR-001 (2026-05-06) → ADR-019 (2026-05-12) = **19 ADRs em 6 dias**. Ritmo extremo decorre do refactor architectural sweep pós-v1.20.0. No ritmo atual atingiríamos 30 em ~3-5 dias. Mesmo assumindo desaceleração, **antecipar curadoria é prudente antes do gatilho ser exercido em retaguarda**. ADR-009 § Limitações já avisa: "ADR vago deixa espaço para falsos negativos".
- **(E2) `docs/plans/` em escala perigosa.** ADR-014 gatilho: "≥100 arquivos sem rotação". Hoje ~55 planos. Crescimento: gerados via `/triage` caminho-com-plano; ritmo similar ao dos ADRs. Antecipar política de archival (mover planos com Concluído >X semanas para `docs/plans/archive/` ou tag) evita atingir o cap reativamente.
- **(E3) `/run-plan` 5 warnings pré-loop no limiar nominal.** ADR-002 gatilho: "Surge 5º+ warning na fase pré-loop com natureza distinta dos atuais → reavaliar". Hoje exatamente **5 warnings** (alinhamento dirty, `.worktreeinclude` ausente, credencial não coberta, escopo divergente, cobertura ausente). O 5º (cobertura) foi adicionado per BACKLOG concluído. Próxima proposta de warning bate na cláusula de reabertura — critério mecânico de admissão deveria ser formalizado **antes** do 6º.
- **(E4) `design-reviewer` findings em prosa volátil** — ADR-011 já registrou como gatilho de reabertura ("se operador reportar findings importantes perdidos sistematicamente, considerar trilho persistente análogo a `## Pendências de validação`"). Sem incidente reportado.
- **(E5) Auto-detect forge inconsistente entre skills:**
  - `/run-plan §3.7`: `gh` (GitHub) + `glab` (GitLab regex `^gitlab\.`) + fallback textual.
  - `/release §5`: `gh` + `glab` + fallback textual.
  - `/next §4.5`: `gh` + `glab` + fallback (filtragem heurística, sem cutucada).
  - **`/triage §0` Cleanup pós-merge**: apenas `gh` + fallback `git branch -r --merged`. **Não cobre GitLab.** Operador em consumer GitLab fica sem auto-cleanup squash-aware.

### 2.4 Redução de gates & verbosidade desnecessários

**Forte:**

- ADR-002 colapsou 4 gates pré-loop do `/run-plan` em trilhos Aviso/Backlog/Validação.
- ADR-006 enum-first elimina prosa-com-bifurcação onde resposta dominante é discreta.
- `/release` step 4 consolidou gates em `Aplicar / Editar / Cancelar` único.
- `/run-plan §3.5` capturas materializadas sem confirmação adicional.

**Pontos de atenção:**

- **(G1) `/run-plan §3.3` sanity check de docs** tem 3 condições de skip (positive list + `Resumo da mudança` + grep vazio). Quando dispara, cutuca via `AskUserQuestion`. Mecânica densa (~10 linhas de regra). Funcionalmente correto mas alto custo de manutenção se mais skips emergirem (4ª condição vira fragmentação).
- **(G2) Cutucada de descoberta em 4 skills com triple-gate** — gate (3) "string canonical não aparece no contexto visível" depende do modelo julgar visibilidade em prosa, não-determinístico. ADR-017 § Limitações reconhece risco sob context compression. Aceito como pragmático; pode reaparecer.

### 2.5 Otimização de tokens (input/output) — arquitetural

**Forte:**

- `philosophy.md` (77 linhas) lido on-demand, não auto-loaded.
- ADR-019 lazy-load `qa-reviewer` ↔ `/gen-tests` (só se diff toca paths de teste).
- `CLAUDE.md` (171 linhas) dentro do cap nominal de 200 (`MEMORY.md` cap).

**Pontos de atenção:**

- **(T1) `design-reviewer` free-read** consome ~12k tokens/invocação (estimativa ADR-011). Por invocação cresce O(#ADRs). Em 19 ADRs hoje; tendência alta (ver E1). Pré-curadoria por keyword no plano antes de free-read reduziria custo sem perder cobertura quando ADRs forem tematicamente segmentados.
- **(T2) `/gen-tests` 169 linhas** lidas inteiras em todo turn de invocação. Crescimento O(#stacks). ADR-008 prevê split em "sub-skills delegadas" se ultrapassar 500 linhas com 3+ sub-blocos. Hoje confortável (2 sub-blocos, ~50+67 linhas cada).
- **(T3) `/triage` 197 linhas** é a maior skill; step 0 cleanup (~30 linhas detalhadas) e step 4 (~50 linhas) puxam volume. Extrair partes operacionais (cleanup, dispatch para `/new-adr`) para template-doutrina poderia reduzir, mas ADR-001 limitou escopo a `templates/plan.md` — reabrir prematuramente.

### 2.6 Lógica e relações entre artefatos

**Forte:**

- Quem invoca quem é determinístico e enxuto. Único Skill→Skill: `/triage` → `/new-adr` (ADR-only delegado) e `/next` → `/triage` (orientação de sessão).
- `code-reviewer` lê `ubiquitous_language` via plano, não em runtime (`philosophy.md:75`). Pipeline canonical.
- `design-reviewer` é único reviewer com free-read; padrão formalizado (ADR-009).
- Hooks são isolados (não invocam, não leem skills).
- `qa-reviewer` ↔ `/gen-tests` via ADR-019 estabelece "reviewer importa convenções da skill geradora correspondente" como padrão paralelo ao pipeline de domínio.

**Pontos de atenção:**

- **(L1) `/release` referencia `/triage §0` textualmente** ("Antes das pré-condições, executar passo de cleanup pós-merge conforme `skills/triage/SKILL.md` `### 0. Cleanup pós-merge`. Mesma detecção, mesma cutucada, mesmas execuções."). Acoplamento por path + nome de seção. Refator do step 0 em /triage que renomeie ou mova arquivo exige acompanhar /release.
- **(L2) `block_gitignored.py:64-66` allowlist `.claude/`** é hardcoded — assume convenção do Claude Code. Se Claude Code mudar o root da territorialidade do harness, hook quebra silenciosamente (bloqueia onde antes liberava). Risco baixo (convenção estável), mas ponto de acoplamento implícito plugin↔harness.
- **(L3) `/init-config` modifica 2 arquivos do consumer** (CLAUDE.md + .worktreeinclude condicional). ADR-018 explicitou o critério distintivo (arquivos cujo único propósito é mecânica do plugin). Critério é load-bearing — futura extensão da skill (ex.: criar `docs/decisions/` automaticamente ao escolher canonical) precisa ser rebatida explicitamente contra esse critério para não fragilizar a postura editorial.
- **(L4) `docs/audits/` é fora da taxonomia formal** sem doutrina. Convive com `docs/plans/`, `docs/decisions/`, `docs/philosophy.md` — quando adicionar um terceiro tipo de prompt reutilizável (ex.: `docs/checklists/`), categoria precisaria de critério explícito.

---

## 3. Propostas

Cada proposta marca explicitamente **criar/editar/remover**, escopo, impacto esperado, risco e dependências.

### A. **Editar** — Uniformizar `disable-model-invocation` nos 8 SKILLs + formalizar critério

**Escopo:** declarar `disable-model-invocation: false` nas 5 skills hoje sem declaração (`/triage`, `/debug`, `/gen-tests`, `/next`, `/init-config`) **ou** adicionar à doutrina CLAUDE.md a regra mecânica usada na decisão BACKLOG concluído ("blast radius local até push manual / cria arquivo / não muta state externo → false"). A decisão deve ser uma das duas; hoje convive a doutrina parcial com 5 skills omitindo o campo.

**Impacto:** coerência editorial em 8 frontmatters. Comportamento runtime potencialmente afetado se default do Claude Code for `true` (autoinvocação desligada hoje nas 5 skills).

**Risco:** baixo. Mudança trivial em frontmatter; checagem do default do CC vale ser feita no plano.

**Dependências:** nenhuma.

### B. **Editar** — Antecipar curadoria de free-read do `design-reviewer`

**Escopo:** introduzir filtro de pré-leitura antes do free-read completo dos ADRs. Direções candidatas (cabíveis em /triage caminho-com-plano antes de invocar reviewer):

- (b1) Reviewer faz **scan rápido por keyword** nos títulos/Origem dos ADRs antes do free-read completo (lista N ADRs candidatos); free-read fica restrito ao subset.
- (b2) Operador (via /triage step 4) anota `**ADRs candidatos:**` no plano se sabe quais aplicam — reviewer prioriza esses + scan dos demais.
- (b3) Reorganizar `docs/decisions/` em subdiretórios por eixo (workflow, idioma, hooks, etc.) — reviewer lê apenas o subdiretório relevante ao plano. Custo de migração + acoplamento ao layout.

**Impacto:** alto. Estamos a ~11 ADRs do gatilho explícito do ADR-011 ("≥30"). Ritmo atual sugere atingir em 1-2 semanas. Antecipar evita cenário "reviewer fica caro mesmo em invocação média".

**Risco:** médio. Mexe em agent doutrinariamente estável (ADR-009). Reabertura formal recomendada via `/triage` produzindo ADR sucessor de ADR-009/ADR-011.

**Dependências:** nenhuma direta; emerge de gatilho ADR-011.

### C. **Editar** — Formalizar critério mecânico de admissão de warnings pré-loop em `/run-plan`

**Escopo:** ADR-002 prevê reabertura no 5º+ warning para "reavaliar se cabe nos trilhos existentes ou exige nova categoria". Estamos exatamente em 5. Antes do próximo proposto bater no gatilho, redigir critério mecânico (similar ao critério dos 4 cumulativos de ADR-013) que classifique warning candidato como (a) admissível nos trilhos Aviso/Backlog/Validação, (b) merece trilho novo, (c) merece bloqueio in situ.

**Impacto:** preserva estabilidade da fase pré-loop sem decisões caso-a-caso. Sustenta ADR-002 como invariante de design em vez de doutrina reabrível.

**Risco:** baixo. Edita CLAUDE.md (ou estende ADR-002 com um adendo) sem afetar comportamento atual.

**Dependências:** independente. Pode rodar paralela a B.

### D. **Editar** — Estender auto-detect forge ao `/triage §0` cleanup pós-merge

**Escopo:** hoje `/triage §0` detecta merge status via `gh pr list` + fallback `git branch -r --merged`. Replicar o padrão `/run-plan §3.7` / `/release §5` / `/next §4.5`: parse `git remote get-url origin` → `github.com` → `gh`; regex `^gitlab\.` → `glab mr list`; fallback `git --merged` para hosts não-mapeados. Consumer GitLab ganha cleanup squash-aware.

**Impacto:** coerência cross-skill (4 skills usando o mesmo helper conceitual). Operador GitLab deixa de ter caminho degradado no /triage step 0.

**Risco:** baixo. Padrão já implementado e validado em 3 outros sites.

**Dependências:** se G (extrair helper) for executada antes, esta proposta vira "wire-up" em vez de implementação nova.

### E. **Criar** — Política de archival para `docs/plans/`

**Escopo:** ADR sucessor de ADR-014 (ou edit de ADR-014 com `## Implementação`) que define critério mecânico de archival:

- Plano com linha em BACKLOG `## Concluídos` há ≥ N semanas (N = candidato: 4) **e** sem worktree ativa, **e** sem PR aberto referenciando o slug → move para `docs/plans/archive/<YYYY-Qx>/<slug>.md`.
- Não destrutivo (mantém histórico de planos arquivados em main per ADR-014 doutrina).
- Operação pode rodar via `/triage §0` (cleanup já estabelecido) ou comando dedicado.

**Impacto:** previne atingir o cap ADR-014 (≥100 planos) reativamente. Mantém `docs/plans/` enxuto para descoberta. Convergência conceitual com `## Concluídos` do BACKLOG (registro editorial preserved, but archived).

**Risco:** médio. Mexe em estrutura de planos referenciados pelo `/run-plan` (precondição 1). Mecânica precisa ser robusta a referências cruzadas (ADR `Implementação` que linka commits do plano arquivado).

**Dependências:** nenhuma direta; antecipa gatilho ADR-014.

### F. **Editar** — Reposicionar `/triage` passo 5 (Consolidação do backlog) como sub-fluxo do passo 4

**Escopo:** mover o conteúdo do passo 5 atual para o final do passo 4 (Produzir os artefatos → BACKLOG), com mesmo critério (releitura → flag → enum sob duplicata/obsolescência). Anatômico: consolidação é parte da gravação do BACKLOG, não fase própria.

**Impacto:** -1 passo na anatomia /triage. Skill cai de 7 passos visíveis para 6 (passo 0..6 → 0..5). Reduz ~5 linhas de cabeçalho de passo + 1 transição editorial. Sem mudança comportamental.

**Risco:** baixo. Edição editorial; impacto comportamental nulo.

**Dependências:** nenhuma.

### G. **Criar** (opcional) — Extrair "Cleanup pós-merge" para `templates/cleanup-pos-merge.md` ou helper documental

**Escopo:** mover o algoritmo de detecção+cutucada+execução de cleanup pós-merge de `/triage §0` para `templates/cleanup-pos-merge.md` (ou subpasta `docs/protocols/`). `/triage` e `/release` referenciam o template via Read em runtime, similar a `templates/plan.md` (ADR-001).

**Impacto:** desacopla `/triage` e `/release` (L1 resolvido). Coexiste com a extensão D (forge bilateral) — extração beneficia ambas as skills num único lugar.

**Risco:** médio. Estende escopo de `templates/` além do plan.md — ADR-001 § Limitações prevê expansão como "decisão futura sob este mesmo protocolo". Não criar agora sem 3+ artefatos compartilhados seria YAGNI (ADR-001 critério); 2 consumidores (/triage, /release) é fronteira.

**Dependências:** se decidida, sequenciar antes de D para evitar duplicação.

### H. **Editar** — Reduzir cross-mode `backlog: local + plans_dir: canonical` no /triage e /run-plan

**Escopo:** `/init-config` passo 3 (perguntas per role) detecta tentativa de combinação cross-mode e recusa (cutuca operador para uniformizar). Permite só `ambos canonical` / `ambos local` / `backlog null`. Remove branch dedicado em /triage step 4 e /run-plan 3.4 que cobre apenas esse caso edge.

**Impacto:** ~10 linhas de prosa removidas cross-skill. Reduz superfície de drift entre skills. Operador perde flexibilidade marginal (combinação que provavelmente nunca foi intencional).

**Risco:** médio. Regressão de cobertura — se algum consumer real adotou cross-mode deliberadamente, perde funcionalidade. Sem evidência empírica de uso real desse combo.

**Dependências:** afeta `/init-config`, `/triage`, `/run-plan`. Mudança atômica recomendada.

---

## 4. Sequenciamento sugerido

Ordenado por **leverage / risco × urgência preditiva**:

### Primeira onda — alta urgência (gatilhos próximos)

1. **B (curadoria free-read design-reviewer)** — 11 ADRs do gatilho explícito ADR-011, ritmo atual sugere 1-2 semanas. Antecipar antes do gatilho ser exercido em retaguarda.
2. **E (archival policy `docs/plans/`)** — gatilho ADR-014 (≥100 planos) similar em horizonte. Bookend de B no eixo "inventário cresce".

### Segunda onda — limiar nominal atingido

3. **C (critério mecânico de warnings pré-loop)** — 5/5 warnings hoje; ADR-002 reabre na próxima adição. Formalizar critério **antes** da próxima proposta de warning evita reabertura caso-a-caso.

### Terceira onda — coerência editorial baixo-risco

4. **A (uniformizar `disable-model-invocation`)** — drift de frontmatter em 5 skills; doutrina parcial. Sem urgência mecânica; vale fechar.
5. **F (passo 5 → sub-fluxo do passo 4 em /triage)** — anatomia da skill; sem mudança comportamental.

### Quarta onda — coerência cross-skill

6. **D (estender forge bilateral ao /triage §0)** — coerência com 3 outros sites; impacto direto em consumers GitLab.
7. **G (extrair cleanup pós-merge para templates/)** — só se D justificar fatoração. **Dependência:** sequenciar antes de D para evitar duplicação intermediária. Risco: pode ser YAGNI (2 sites apenas).

### Quinta onda — opcional / sob risco de regressão

8. **H (recusar cross-mode `backlog`/`plans_dir`)** — limpa prosa mas potencial regressão de cobertura. Considerar apenas se algum dogfood confirmar que combinação nunca foi intencional. Adiar para evidência empírica.

### Propostas que destrancam outras

- **G destranca D**: se cleanup for extraído primeiro, D vira wire-up trivial.
- **C destranca futuras propostas de warning**: critério mecânico evita cada proposta nova reabrir ADR-002.
- **B destranca extensão futura do design-reviewer**: curadoria reduz pressão de tokens para wiring adicional (se algum dia /run-plan ganhar gate document-level).

---

## Encaminhamento

Propostas aceitas pelo operador não viram PR direto. Cada uma entra pelo fluxo padrão: `/triage <proposta>` decide artefato (linha de backlog, plano, ADR, atualização de domain/design) e segue dali.

**Sugestões de encaminhamento por proposta:**

- A, F → linha de backlog (mudança editorial direta).
- C → linha de backlog + edit cirúrgico de ADR-002 (adendo de critério).
- D → linha de backlog (replicar mecanismo conhecido).
- E → ADR sucessor de ADR-014 (decisão estrutural sobre archival).
- B → ADR sucessor de ADR-009/ADR-011 (decisão estrutural sobre curadoria).
- G → linha de backlog **ou** edit de ADR-001 § Implementação (se extração for executada).
- H → ADR (recusa de cross-mode contradiz ADR-005 § Limitações implícitas).
