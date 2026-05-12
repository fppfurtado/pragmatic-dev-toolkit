# Auditoria — prosa & tokens — 2026-05-12 (re-run pós-Ondas 1-3b)

Modo: diagnóstico + propostas, **zero alteração**. Prompt: `docs/audits/prose-tokens.md`.

**Contexto.** Re-execução solicitada após fechamento das Ondas 1-3b do roadmap `2026-05-12-execution-roadmap.md`. Recalibra alvos depois que 5 ADRs (020-024) e bundles editoriais shipparam — G_arch removeu ~200 palavras de `/triage §0`; A_prose/C_prose compactaram CLAUDE.md/frontmatters; B_prose/D_prose consolidaram doutrina hub-and-spoke. Run anterior em `2026-05-12-prose-tokens.md` (manhã do mesmo dia, pré-implementação).

**Pré-checagem:** BACKLOG.md `## Concluídos` lido; memory `project_artifact_review_v1_18` (onda 2026-05-06) registrado. Propostas A-G da run anterior shippadas via PRs #54-#58 (cobertura completa do escopo enumerado). Esta run opera em **resíduos residuais pós-onda + cicatrizes introduzidas pela nova prosa shippada**.

---

## 1. Inventário & métricas

### Artefatos de runtime do plugin (delta vs run anterior)

| Artefato | Linhas | Palavras | Δ palavras | Modo |
|---|---:|---:|---:|---|
| `CLAUDE.md` | 175 | 2.613 | **+28** | Auto-loaded a cada turn |
| `docs/philosophy.md` | 77 | 1.379 | **-30** | Por invocação (cross-ref) |
| `templates/plan.md` | 62 | 408 | **+42** | Por invocação (Read em `/triage`) |
| **Skills** (9, +1 nova) | — | — | — | — |
| `skills/triage/SKILL.md` | 172 | 2.357 | **-282** | Por invocação |
| `skills/run-plan/SKILL.md` | 170 | 2.888 | 0 | Por invocação |
| `skills/gen-tests/SKILL.md` | 170 | 1.426 | **-11** | Por invocação |
| `skills/release/SKILL.md` | 159 | 1.722 | **-10** | Por invocação |
| `skills/init-config/SKILL.md` | 128 | 1.330 | **-13** | Por invocação |
| `skills/debug/SKILL.md` | 116 | 1.039 | **+2** | Por invocação |
| `skills/new-adr/SKILL.md` | 99 | 828 | 0 | Por invocação |
| `skills/next/SKILL.md` | 87 | 982 | **+2** | Por invocação |
| **`skills/archive-plans/SKILL.md`** | 96 | 725 | **NEW** | Por invocação (E_arch/ADR-022) |
| **Agents (5)** | — | — | — | — |
| `agents/code-reviewer.md` | 77 | 930 | **-15** | Por invocação |
| `agents/design-reviewer.md` | 109 | 1.022 | **+354** | Por invocação (B_arch/ADR-021) |
| `agents/doc-reviewer.md` | 61 | 578 | **-9** | Por invocação |
| `agents/qa-reviewer.md` | 58 | 659 | **-9** | Por invocação |
| `agents/security-reviewer.md` | 53 | 660 | **-24** | Por invocação |
| **Demais** | — | — | — | — |
| `README.md` | 54 | 722 | **+38** | Pré-adoção |
| `docs/install.md` | 80 | 1.102 | **+50** | On-demand pós-adoção |
| **`docs/procedures/cleanup-pos-merge.md`** | 43 | 539 | **NEW** | Por invocação (G_arch/ADR-024) |
| `.claude-plugin/plugin.json` | 11 | 61 | **-3** | Marketplace + roteador |
| `.claude-plugin/marketplace.json` | 30 | 102 | **+6** | Marketplace |
| **Corpus runtime estimado** | **~1.987** | **~24.072** | **+~1.540** | — |

**Delta auto-loaded.** CLAUDE.md +28 palavras; descriptions de frontmatter agora somam **~403 palavras** (vs ~465 antes — -62). Net auto-loaded por turn: **-34 palavras** apesar de CLAUDE.md crescer, porque C_prose cortou mais nas descriptions do que A_prose adicionou em CLAUDE.md.

**Onde o corpus cresceu (+~1.540).** Atribuível a 3 ADRs estruturais shippados; toda a expansão é **on-demand**, não auto-loaded:

- `skills/archive-plans/SKILL.md` (+725) — skill nova de ADR-022.
- `docs/procedures/cleanup-pos-merge.md` (+539) — extração de G_arch/ADR-024 (compensa o -282 em `/triage`, líquido +257; bom trade-off — agora dois sites lêem o mesmo procedimento sob demanda).
- `agents/design-reviewer.md` (+354) — seção "Curadoria do free-read" de B_arch/ADR-021.
- Soma: ~1.618 (resto é ruído editorial cross-arquivo).

**Frontmatter descriptions — palavras por skill/agent (atualizado):**

| Componente | Palavras | Δ vs run anterior |
|---|---:|---:|
| `doc-reviewer` | 48 | (não tocado) |
| `security-reviewer` | 39 | **-12** (C_prose cortou stack list) |
| `design-reviewer` | 33 | **-38** (C_prose) |
| `code-reviewer` | 32 | (não tocado) |
| `triage` | 29 | -2 |
| `init-config` | 29 | **-12** (C_prose) |
| `qa-reviewer` | 29 | +1 |
| `run-plan` | 27 | -3 |
| `gen-tests` | 27 | **-11** (C_prose; preserva anchors Python/Java) |
| `next` | 24 | -3 |
| `release` | 24 | -3 |
| `archive-plans` | 23 | **NEW** |
| `new-adr` | 21 | -1 |
| `debug` | 18 | **-8** |
| Total | **403** | **-62** vs run anterior |

Topo da lista agora é `doc-reviewer` (48) — único description **>40 palavras** não-tocado pelo C_prose. Resto convergiu para faixa 18-33 palavras.

---

## 2. Diagnóstico por critério

### 2.1 Coesão & coerência interna/externa

**Forte.** Hub-and-spoke de doutrina consolidado: `CLAUDE.md → philosophy.md` define regra-mãe ("Convenção de idioma"), `CLAUDE.md ## Reviewer/skill report idioma` operacionaliza para 5 reviewers + `/triage`, spokes referenciam via `per CLAUDE.md → 'Reviewer/skill report idioma'`. Funcionou.

**Cicatriz residual nova (não flagada na run anterior):**

- **(C1-NEW) Duplicação cross-tabela em CLAUDE.md sobre dispatch de reviewers.** Linhas 15-17 (Plugin layout / **Agents**) descrevem dispatch: *"design-reviewer operates on a document pre-fact (plan or ADR draft) — invoked automatically by /triage (when producing a plan) and /new-adr (standalone or delegated) per ADR-011; manually via @design-reviewer for other entry points. Not invoked by /run-plan."* Linha 43 (última row da tabela "The role contract") repete: *"qa-reviewer, security-reviewer, doc-reviewer are invoked by /run-plan per `{reviewer: qa|security|doc}` annotation on the plan block. design-reviewer operates on documents pre-fact (plan/ADR draft); invoked automatically by /triage (plan-producing path) and /new-adr (standalone or delegated) per ADR-011, or manually via @design-reviewer. Consumer projects can shadow any of them with project-level `.claude/agents/<name>.md` (project-level wins on collision)."* Mesma informação dispatch automático + paths de invocação. Diferença real: linha 43 acrescenta (a) `/run-plan` annotation schema, (b) shadow override consumer-level. Conteúdo real único da linha 43 ≈ 30 palavras; resto é duplicação de ~50 palavras. CLAUDE.md auto-loaded; custo amortizado por turn.

### 2.2 Clareza & desambiguação

**Forte em geral.** Tabelas bem aplicadas. Cicatriz residual da run anterior:

- **(D1) `/run-plan §3.3` sanity check de docs** segue em prosa contínua (linhas 99-103, ~15 linhas em prosa contínua, 3 skip + 1 cutucada). **E_prose do roadmap pendente** — não foi atacado nas Ondas 1-3.

**Nova:**

- **(D3-NEW) `/release §4.5 item 5 "Aplicar"`** (linha 126) é uma **única sentença ~250 palavras** descrevendo o recovery proativo + sequência (a)-(e). Subordinadas encadeadas dificultam parse em uma passada. Tabela ou enumeração faria muito melhor:
  ```
  | Estado | Ação | Sub-ações |
  | HEAD detached/divergente | Recovery proativo | symbolic-ref → status → stash → checkout |
  | Behind upstream | Sync | fetch → rev-list → pull --ff-only |
  | Sync OK | Aplicar sequência | (a)-(e) |
  ```

### 2.3 Alinhamento à `docs/philosophy.md`

**Forte.** D_prose deixou philosophy.md em princípio puro (3 frases enxutas). Hub-and-spoke evitou novas duplicações.

Nada a flagar.

### 2.4 Inflação de tokens — input recorrente e por invocação

**Volume CLAUDE.md cresceu ligeiramente (+28 palavras) apesar de A_prose ter cortado.** Adição "## Reviewer/skill report idioma" (~85 palavras) + bullet "disable-model-invocation" referenciando ADR-023 (~25 palavras) > os cortes de A_prose (~68 palavras).

**Pontos de atenção:**

- **(T1-NEW) `doc-reviewer` description (48 palavras) — único acima de 40.** *"Revisor genérico de drift entre documentação e código no diff — identificadores citados em docs que não existem no repo, cross-refs/anchors quebrados, exemplos/snippets que contradizem o código atual. Stack-agnóstico — aplicável a qualquer tipo de projeto. Acionar quando o diff toca `.md`/`.rst`/`.txt` ou renomeia/remove identificadores referenciados em docs."* Enumeração de 3 tipos de drift (identificadores, cross-refs, exemplos) duplica `## O que flagrar` do body. Possível redução para ~25 palavras: "Revisor de drift entre docs e código no diff. Stack-agnóstico. Acionar quando diff toca .md/.rst/.txt ou renomeia/remove identificadores referenciados em docs."
- **(T2) Auto-loaded por turn permanece próximo do estado pós-A_prose** (~3.000 palavras) — espaço pequeno para redução adicional sem perda de informação operacional.
- **(T3) Template `templates/plan.md` ganhou +42 palavras** com novo campo `**ADRs candidatos:**` (necessário per B_arch/ADR-021). Comentário explicativo de 3 linhas por campo (Termos ubíquos, ADRs candidatos, Linha do backlog). Compactação possível: 1 linha por campo:
  ```
  **Termos ubíquos tocados:** <Termo> (<categoria>) — bounded context|agregado|entidade|RN|conceito; omitir se refactor/doc-only.
  **ADRs candidatos:** ADR-NNN (motivo) — opcional; reviewer prioriza esses, scan cobre os demais (ADR-021).
  **Linha do backlog:** <texto exato> — incluir quando há linha no BACKLOG; mensageiro pra /run-plan operar transições.
  ```
  Redução estimada: ~40 palavras no `templates/plan.md` (lido por invocação `/triage`).

### 2.5 Duplicação cross-artifact

**B_prose endereçou a duplicação principal** (idioma do relatório). Verificação concreta dos 6 sites:
- 4 reviewers (qa, security, design, doc) usam linha curta de referência idêntica.
- `code-reviewer` mantém a linha + rótulos estruturados (`Localização`/`Problema`/`Filosofia violada`/`Sugestão`) — assimetria intencional documentada (subagent isolado sem CLAUDE.md auto-loaded).
- `/triage` step 4 usa "Idioma de saída: per `CLAUDE.md` → 'Reviewer/skill report idioma'."

Funcionou. **Não há novas duplicações cross-artifact emergidas das Ondas 1-3b.**

- **(R1) Cutucada de descoberta** segue em 4 SKILLs (`/triage`, `/new-adr`, `/run-plan`, `/next`) + descrição em CLAUDE.md. Estado **inalterado vs run anterior**. ADR-017 § Alternativa (g) já aceitou explicitamente; **não-mecanismo** (decisão formalizada, registrada como tal antes).

### 2.6 Justificativas-cicatriz

A_prose comprimiu as 3 principais (From v1.11.0 onward, Release cadence, Critério editorial). Pendentes do roadmap:

- **(J1) `/init-config:13`** — F_prose do roadmap. Linha 12-13 explica em ~50 palavras que `/init-config` define o bloco em vez de consumir + cutucada de ADR-017 não dispara. Cicatriz auto-explicativa removível para 1 frase.
- **(J2) `/init-config:128`** — G_prose do roadmap. Bullet em `## O que NÃO fazer` recapitula o preâmbulo (linha 13).

Ambos shippáveis na Onda 4 sem trade-off.

### 2.7 Frontmatter `description`

C_prose endereçou 4 dos descriptions inflados (`/gen-tests`, `/init-config`, `design-reviewer`, `security-reviewer`). Resíduo: `doc-reviewer` (48 palavras — ver T1-NEW acima). Demais convergiram para faixa razoável.

### 2.8 `## O que NÃO fazer`

A_prose deixou o critério editorial enxuto. Run anterior identificou:

- **(N1)** `/run-plan` linha sobre push sem confirmação — borderline mas aceito como anti-bypass. Inalterado, decisão permanece válida.
- **(N2)** `/init-config:128` cutucada — duplica preâmbulo (= G_prose pendente).

Sem novas violações observadas.

### 2.9 NOVO — Verbosidade local em ADRs e planos shippados

ADRs 020-024 e planos shippados nas Ondas 1-3b não foram tocados pela run anterior (escopo `## Escopo` da auditoria os trata como **contexto, não alvo de reescrita**). Verificação amostral: prosa coerente com volume previsto para ADR estrutural (template canonical do `/new-adr`). **Nenhum gap acionável.**

---

## 3. Propostas

Conversão palavra→token ~1.3× (corpus técnico/markdown).

### A. Compactar comentário de `templates/plan.md`

**Escopo:** condensar explicações dos 3 campos especiais (Termos ubíquos tocados, ADRs candidatos, Linha do backlog) de 2-3 linhas cada para 1 linha cada (ver T3 acima).

**Redução:** ~40 palavras / ~52 tokens. Auto-loaded **por invocação** de `/triage` que produz plano (frequente).

**Sequenciamento:** baixo leverage de tokens, mas template lido em todo `/triage`-com-plano. Refactor trivial.

### B. Encurtar description de `doc-reviewer`

**Escopo:** description atual (48 palavras) → ~25 palavras. Remover enumeração de 3 tipos de drift do gatilho (vivem em `## O que flagrar` do body).

**Proposta concreta:**
> Revisor de drift entre docs e código no diff. Stack-agnóstico. Acionar quando o diff toca `.md`/`.rst`/`.txt` ou renomeia/remove identificadores referenciados em docs.

**Redução:** ~23 palavras / ~30 tokens. **Auto-loaded por roteador a cada turn.** Risco zero (description é tag de invocação).

**Sequenciamento:** alto leverage por unidade de risco. Único description residual >40 palavras.

### C. Compactar duplicação de dispatch em CLAUDE.md

**Escopo:** linhas 15-17 (Plugin layout) e linha 43 (The role contract) descrevem o mesmo dispatch. Manter linha 43 (única contém annotation schema + shadow rule) e reduzir linhas 15-17 a apenas:

> **Agents** — `agents/<name>.md` with frontmatter. Five reviewers: `code-reviewer`, `qa-reviewer`, `security-reviewer`, `doc-reviewer`, `design-reviewer`. Dispatch rules in "The role contract" table below.

**Redução:** ~40 palavras na linha 15-17 / ~52 tokens. **Auto-loaded por turn.**

**Trade-off:** quem lê linha 15 precisa rolar até linha 43 para entender wiring. Aceitável — wiring é detalhe operacional, primeira leitura precisa apenas saber que 5 reviewers existem.

**Sequenciamento:** alto leverage (auto-loaded). Risco baixo — só remove duplicação.

### D. Trocar prosa por estrutura em `/release §4.5 item 5 "Aplicar"`

**Escopo:** sentença ~250 palavras (linha 126) reescrita como sequência enumerada + tabela de recovery. Ver D3-NEW acima para shape proposta.

**Redução:** ganho **principal de legibilidade**; redução de palavras modesta (~30). Skill por-invocação, custo amortizado em uso de `/release`.

**Sequenciamento:** médio leverage; valor é clareza editorial num caminho crítico.

### E. (E_prose existente — não-incorporada nas Ondas 1-3) Trocar prosa por tabela em `/run-plan §3.3`

**Escopo:** sanity check de docs (3 condições skip + cutucada) vira tabela `Condição | Skip silente? | Ação`. Idêntico à proposta E da run anterior. **Inalterado** — vale entrar na Onda 4.

### F. (F_prose existente) Compactar preâmbulo de `/init-config`

**Escopo:** linhas 12-13 (cicatriz "Diferente das demais skills...") → 1 frase. Idêntico à proposta F da run anterior. Pendente.

### G. (G_prose existente) Remover bullet redundante em `/init-config ## O que NÃO fazer`

**Escopo:** linha 128 que duplica preâmbulo. Idêntico à proposta G da run anterior. Pendente.

---

## 4. Sequenciamento sugerido — leverage por turn

### Alta frequência (auto-loaded por turn)

1. **B (doc-reviewer description)** — ~23 palavras / ~30 tokens. Auto-loaded por roteador.
2. **C (deduplicar dispatch em CLAUDE.md)** — ~40 palavras / ~52 tokens. Auto-loaded.

**Subtotal alta frequência:** ~63 palavras / ~82 tokens em **cada turn**.

### Média frequência (por invocação)

3. **A (compactar comentário de plan.md)** — ~40 palavras. Lido em `/triage`-com-plano.
4. **F (preâmbulo /init-config)** — ~30 palavras (pendente do roadmap original).
5. **G (`## O que NÃO fazer` redundante em /init-config)** — ~12 palavras + 1 bullet.

### Baixa frequência / clareza

6. **D (estrutura em /release §4.5)** — ganho principal é legibilidade.
7. **E (tabela em /run-plan §3.3)** — pendente do roadmap original.

### Total estimado

~210 palavras ≈ ~275 tokens removidos do corpus runtime. Redução **0.9%** — significativamente menor que a run anterior (~370 palavras / 1.6%) porque as cicatrizes principais já foram absorvidas pelas Ondas 1-3b.

**Cobertura editorial alcançada:** o roadmap original endereçou 9 itens (A-G + F_arch + H_arch); 6 prose shippados, 4 pendentes na Onda 4 (E_prose, F_prose, G_prose) + um structural (F_arch). Esta run identifica **3 novos resíduos** (T1-NEW, C1-NEW, D3-NEW) + **1 refinamento** (A — template).

---

## 5. Cruzamento com `2026-05-12-execution-roadmap.md`

| Proposta (esta run) | Status no roadmap | Encaminhamento sugerido |
|---|---|---|
| **A** (plan.md template) | NOVO — não no roadmap | Linha de backlog ou bundle Onda 4 |
| **B** (doc-reviewer desc) | NOVO — não no roadmap | Linha de backlog ou bundle Onda 4 (auto-loaded) |
| **C** (deduplicar dispatch CLAUDE.md) | NOVO — não no roadmap | Linha de backlog ou bundle Onda 4 (auto-loaded) |
| **D** (estrutura /release §4.5) | NOVO — não no roadmap | Linha de backlog isolada |
| **E** (tabela /run-plan §3.3) | **E_prose pendente Onda 4** | Bundle Onda 4 — incluir |
| **F** (preâmbulo /init-config) | **F_prose pendente Onda 4** | Bundle Onda 4 — incluir |
| **G** (`## O que NÃO fazer` /init-config) | **G_prose pendente Onda 4** | Bundle Onda 4 — incluir |

**Recomendação:** ampliar o bundle "trim residual" da Onda 4 para 7 itens (E_prose, F_prose, G_prose + propostas A-D desta run). Todos são edits cirúrgicos baixo-risco; `/triage` único deve produzir plano cobrindo o conjunto. Trade-off: bundle maior aumenta surface do PR; mitigação é manter blocos por arquivo no plano (B em description, C em CLAUDE.md, A em templates, D em /release, E/F/G em skills respectivas).

**Itens B + C juntos** valem alto leverage por serem **auto-loaded** — entram primeiro na ordem do plano para realizar ganho imediato.

---

## Encaminhamento

Cada proposta entra pelo fluxo padrão: `/triage <proposta-ou-bundle>` decide artefato (linha de backlog, plano, ADR, atualização cirúrgica).

**Caminho preferencial:** triage único bundling A-G como **plano** "trim residual editorial Onda 4" — itens são **homogêneos** (edits cirúrgicos de prosa, sem decisão estrutural pendente), enquadram-se no critério "bundle entre auditorias quando a área é a mesma" do roadmap.

**Saída persistente:** este arquivo (`2026-05-12b-prose-tokens.md`). Sufixo `b` distingue da run da manhã. Não-destrutivo — `2026-05-12-prose-tokens.md` preservado para arqueologia.
