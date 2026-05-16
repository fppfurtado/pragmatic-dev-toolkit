# Auditoria — arquitetura & lógica — 2026-05-15

Modo: diagnóstico + propostas, **zero alteração**. Prompt: `docs/audits/architecture-logic.md`. Pré-checagem: `BACKLOG.md ## Concluídos` (até v1.25.0, em progresso) + índice de `docs/decisions/` (ADR-001 a ADR-032).

Estado do repo no momento da auditoria: **v2.8.1**, 10 skills, 5 agents, 3 hooks, 30 ADRs (24 Aceitos, 7 Propostos, ADR-032 stub vazio), ~12 itens em `## Próximos`, ~78 planos em `docs/plans/` (sem archival), 2 templates, 1 procedure, CI lint mínimo ativo (ADR-013), `.worktreeinclude` tracked (com `.claude/`).

**Delta desde auditoria 2026-05-12** (v2.4.0 → v2.8.1, em 3 dias): +2 skills (`/draft-idea`, `/archive-plans`), +11 ADRs, +23 planos, `docs/procedures/` criada, `templates/` ganhou `IDEA.md`. Doutrina parcial de `disable-model-invocation` (proposta A 2026-05-12) fechada via ADR-023. Curadoria de free-read do `design-reviewer` (B) fechada via ADR-021. Critério de admissão de warnings pré-loop (C) fechada via ADR-020. Cleanup pós-merge extraído para `docs/procedures/` (G) — sob ADR-024 (Proposto). Cross-mode `backlog/plans_dir` (H) recusado upstream via ADR-025 (Proposto). Propostas A/B/C **shippadas e aceitas**; propostas G/H **shippadas como mecânica em vigor mas com ADR ainda em Proposto** — fonte do ponto-mãe desta auditoria.

---

## 1. Mapa de componentes & relações

### Skills (10)

| Skill | Linhas | `roles.required` | `roles.informational` | `disable-model-invocation` | Cutucada descoberta | Invoca |
|---|---|---|---|---|---|---|
| `/triage` | 191 | `plans_dir` | `backlog`, `ubiquitous_language`, `design_notes`, `decisions_dir`, `product_direction` | false | sim | `/new-adr` (Skill tool), `@design-reviewer` (auto, ADR-011) |
| `/run-plan` | 191 | `plans_dir` | `backlog`, `test_command` | false | sim | `code-reviewer` default + `qa/security/doc-reviewer` por anotação `{reviewer:…}` |
| `/new-adr` | 110 | `decisions_dir` | — | false | sim | `@design-reviewer` (auto, ADR-011) |
| `/next` | 91 | `backlog` | `product_direction`, `plans_dir` | false | sim | `/triage` (step 7); auto-detect forge |
| `/draft-idea` | 137 | `product_direction` | — | false | sim | nenhuma; sugere `/triage` no relatório |
| `/debug` | 116 | — | `test_command`, `ubiquitous_language`, `decisions_dir`, `design_notes` | false | não | sugere `/triage` no relatório (sem auto-dispatch) |
| `/gen-tests` | 170 | — | `ubiquitous_language`, `design_notes` | false | não | nenhuma; sub-blocos Python + Java (ADR-008) |
| `/release` | 167 | — | `version_files`, `changelog` | false | não | referencia `docs/procedures/cleanup-pos-merge.md`; auto-detect forge |
| `/archive-plans` | 96 | — | `backlog`, `plans_dir` | false | não | auto-detect forge para critério 6 (PR aberto) |
| `/init-config` | 148 | (sem `roles:` — **define** o bloco config) | — | **não emite** (ADR-017 exceção) | não | passo 4.5 mexe em `.worktreeinclude` (ADR-018); ADR-030 Proposto estende a `CLAUDE.md` gitignored |

### Agents (5)

| Agent | Linhas | Quem invoca | Quando | Free-read |
|---|---|---|---|---|
| `code-reviewer` | 77 | `/run-plan` default | sem anotação `{reviewer:…}` no bloco | não |
| `qa-reviewer` | 58 | `/run-plan` | `{reviewer: qa}` ou bloco com testes | sub-bloco `/gen-tests` da stack detectada (ADR-019, lazy) |
| `security-reviewer` | 53 | `/run-plan` | `{reviewer: security}` | não |
| `doc-reviewer` | 61 | `/run-plan` | `{reviewer: doc}` ou bloco doc-only | varre `*.md`/`*.rst`/`*.txt` do repo |
| `design-reviewer` | 109 | `/triage` (auto, caminho-com-plano), `/new-adr` (auto), `@-mention` | pré-fato em plano/ADR draft (ADR-011) | **`**ADRs candidatos:**` priorizados + scan keyword dos demais (ADR-021, threshold N=15)** |

### Hooks (3) — `hooks/hooks.json`

| Hook | Evento | Gates | ADR aplicável |
|---|---|---|---|
| `block_env.py` | PreToolUse Edit\|Write | sufixo `.env`/`<x>.env`, exceção `.env.example` + `TEMPLATE_SUFFIXES` | ADR-015 |
| `block_gitignored.py` | PreToolUse Edit\|Write | triplo (file_path vazio / não-git / `git` ausente) + allowlist `<repo>/.claude/` | ADR-005, ADR-016 |
| `run_pytest_python.py` | PostToolUse Edit\|Write | triplo (extensão `.py` / `pyproject.toml` ancestral / `uv` ou `python -m pytest`) | (sem ADR — invariante histórica) |

### Doctrine sources + estado

- `philosophy.md` (77 linhas) — princípios. Cabeçalhos: filosofia em uma frase / bifurcações arquiteturais / path contract / convenção de naming / convenção de idioma / convenção de commits / convenção de pergunta ao operador / linguagem ubíqua na implementação.
- `CLAUDE.md` (estável) — operating instructions, role contract, Resolution protocol, AskUserQuestion mechanics, naming + auto-gating, cutucada de descoberta, Pragmatic Toolkit schema. Auto-loaded a cada turn.
- `templates/` — agora **2 artefatos**: `plan.md` (consumido por `/triage` e `/run-plan`), `IDEA.md` (consumido por `/draft-idea` apenas). ADR-001 § Limitações previa expansão "sob este mesmo protocolo"; expansão aconteceu via ADR-027 sem reabrir critério.
- `docs/procedures/cleanup-pos-merge.md` — nova categoria. Consumido por `/triage §0` e `/release § Cleanup pós-merge` (refator do L1 da auditoria 2026-05-12). Categoria formalizada por **ADR-024 (Proposto)** — drift ADR/implementação.
- `docs/decisions/ADR-001..032` — registro estrutural. **7 Propostos** (022, 024, 025, 027, 028, 029, 030, 031). **ADR-032 stub** (`## Contexto`/`## Decisão`/`## Consequências` ainda com placeholders `<...>`).
- `docs/plans/` — **78 planos históricos** (gatilho ADR-014 = 100; ~22 de margem). `/archive-plans` shippada, ADR-022 ainda Proposto.
- `docs/audits/` — prompts reutilizáveis + `runs/` (4 runs anteriores em 2026-05-12 — 2 architecture-logic + 2 prose-tokens, mais 1 execution-roadmap).
- `BACKLOG.md` — `## Próximos` (12 linhas) + `## Concluídos` (registro editorial append-only). State of in-flight em git/forge (ADR-004).

### Cadeias notáveis (atualizadas)

- **`/triage` → `/new-adr` → `@design-reviewer`** (ADR-011): wiring automático preservado; ADR-026 adicionou critério mecânico de absorção pré-commit dos findings (default invertido para absorver caminho-único).
- **`/next` → `/triage`** (step 7): orientação de sessão alimenta alinhamento.
- **`/draft-idea` → sugere `/triage`** (passo 5): upstream do pipeline; sem auto-dispatch (decisão do operador). ADR-031 (Proposto) adiciona gate de cutucada em projeto maduro para evitar regressão "feature gravada em IDEA.md".
- **`/debug` → sugere `/triage`**: handoff cross-skill; BACKLOG `## Próximos` registra "/debug → /triage handoff [contexto perde em sessão longa]" como pendência aberta.
- **`/triage §0` ↔ `/release` cleanup** agora desacoplados via `docs/procedures/cleanup-pos-merge.md` (L1 da auditoria 2026-05-12 resolvido por extração). Ambos referenciam o procedure por path.
- **Plano grava → `/run-plan` repassa → reviewer valida**: pipeline `**Termos ubíquos tocados:**` + `**ADRs candidatos:**` (ADR-021).
- **`qa-reviewer` lê sub-bloco `/gen-tests`** (ADR-019, lazy).
- **`/archive-plans` é folha** — operação isolada sob demanda do operador.

### Gates ativos por skill (10)

| Skill | Gates `AskUserQuestion` (caminho-comum) |
|---|---|
| `/triage` | Cleanup (via procedure) → gaps unificados (até 4) → Backlog (consolidação só com flag) → Branch (só se branch ≠ principal, ADR-028 Proposto) → Commit |
| `/run-plan` | Validação manual → Docs sanity (só se não-skip) → Publicar (Push/PR + Renomear se modo local sem Branch) → Forge confirmação |
| `/new-adr` | Numeração (só se mista) — caso raro |
| `/next` | Próximo (3 + Other) → Movimentações (só se moveu) |
| `/draft-idea` | (cutucada cond. projeto maduro) Direção → (modo update) Seções (multi-select) → Restrições (multi-select) |
| `/debug` | Onde/Reprod/Mudou (unificado, só se sintoma vago) |
| `/gen-tests` | Stack (só se marker ausente) → Fixture/Mock (decisões locais por stack) |
| `/release` | Branch (só se ≠ default) → Release (bump) → Release (Aplicar/Editar/Cancelar) → Forge (após push) |
| `/archive-plans` | Archive (Aplicar/Cancelar) — preview-first |
| `/init-config` | Config (Editar/Cancelar se bloco existe) → 4 questions unificadas |

---

## 2. Diagnóstico por critério

### 2.1 Funcionalidade & simplicidade arquitetural

**Forte.** Onda editorial 2026-05-12→05-15 fechou 4 das 8 propostas da auditoria anterior via ADRs concretos (020, 021, 023, 024+procedures). Crescimento controlado: +2 skills com responsabilidade nítida e folha (`/draft-idea` upstream do pipeline; `/archive-plans` operação editorial periódica). Hubs preservados (`/triage` continua único orquestrador downstream).

**Pontos de atenção:**

- **(F1) `/triage roles.required = [plans_dir]` é semanticamente impreciso.** A skill decide entre **4 saídas** (linha de backlog, plano, ADR delegado, atualização de domain/design). `plans_dir` só é necessário no caminho-com-plano — caminhos "só linha de backlog" e "ADR-only delegado" e "atualização domain/design" não consomem o papel. Declarar como `required` força resolution protocol step 3 (perguntar ao operador) em situações onde a skill prosseguiria sem o papel. Comportamento atual depende do operador resolver `plans_dir` antecipadamente (geralmente ok), mas o frontmatter mente sobre a dependência real. Análogo a `/debug` que não declara nada `required` apesar de ler `decisions_dir`. Reclassificar como `informational` resolveria.
- **(F2) ADR-032 stub vazio** (status Proposto, mas `## Contexto`/`## Decisão`/`## Consequências` com placeholders `<...>`). Skill `/note` referenciada não existe ainda; só plano `docs/plans/skill-note-contexto-compartilhado.md` (não auditado). ADR funciona como mensageiro do plano sem decisão concreta — viola formato canonical do template ADR e cria ruído no índice de decisões.
- **(F3) `templates/` ganhou consumidor único.** ADR-001 estabeleceu critério "centralizar quando 3+ skills consomem ou critério explicitado". `IDEA.md` foi adicionado via ADR-027 com **1 consumidor** (`/draft-idea`). Não há ADR sucessor explicitando que single-consumer também justifica `templates/` — ADR-001 § Limitações registra expansão como "decisão futura sob este mesmo protocolo", e ADR-027 não cita ADR-001. Drift implícito: critério editorial de templates/ foi relaxado sem reabertura formal.
- **(F4) Onda editorial 2026-05-15 em progresso (v1.25.0).** 7 ADRs em Proposto com mecânica já implementada nas skills/CLAUDE.md: ADR-022 (archive — skill já existe), ADR-024 (procedures — procedure já criada e referenciada), ADR-025 (cross-mode — recusa implementada em /init-config + /triage), ADR-027 (/draft-idea — skill já existe), ADR-028 (campo `**Branch:**` — implementado em /triage step 4 + /run-plan §1.1), ADR-029 (cutucada CLAUDE.md ausente — implementada em 5 skills), ADR-030 (CLAUDE.md gitignored — implementação em curso), ADR-031 (cutucada projeto maduro — passo 1.5 da /draft-idea implementado). Status Proposto + código Aceito = **falsa pendência**. Onda registrada no BACKLOG v1.25.0 menciona "promover 7 ADRs Strong de Proposto→Aceito" — operação meta editorial em curso; auditoria captura o snapshot.

### 2.2 Alinhamento à `philosophy.md`

**Forte.** Doutrina parcial de `disable-model-invocation` (A1 da auditoria 2026-05-12) fechada via ADR-023 com critério mecânico cumulativo. Drift editorial das 5 skills sem declaração eliminado: 10/10 skills agora declaram explicitamente `false`. Cadeia design-reviewer (ADR-009 → 011 → 021 → 026) consolida 4 ADRs sobre o mesmo agent — coerente com YAGNI por incremento iterativo, mas tema cresceu.

**Pontos de atenção:**

- **(A1) Cadeia design-reviewer com 4 ADRs em 7 dias.** Cada ADR é incremento legítimo (ADR-009 = doutrina pré-fato; ADR-011 = wiring auto; ADR-021 = curadoria free-read; ADR-026 = absorção pré-commit). Mas ritmo sugere que próximos refinamentos podem virar adendo de ADR existente em vez de novo (vide memória "Limiar de ADR para mudanças em doutrina" — refinar critério documentado → default ADR é regra geral; preferência por **`## Implementação` em ADR existente** quando refinamento não altera decisão estrutural mas sim mecânica). Hoje não é problema; vale registrar como atenção editorial preventiva.
- **(A2) `docs/audits/` ainda fora da taxonomia formal.** Item A2 da auditoria anterior persiste. Hoje 2 prompts + 4 runs. Convive bem; YAGNI.
- **(A3) `/draft-idea` introduz nova classe "skill geradora com cutucada condicional pré-conteúdo".** Passo 1.5 (cutucada de projeto maduro) é gate de **classificação** (direção-do-projeto vs feature) anterior à elicitação. Outras skills geradoras (`/gen-tests`, `/new-adr`) não têm equivalente — assume-se que o operador invoca pelo motivo certo. ADR-031 (Proposto) formaliza a exceção. Risco: futuras skills geradoras importarem o padrão sem critério mecânico — vide A1 da cadeia design-reviewer.

### 2.3 Efetividade das funcionalidades

**Forte:**

- ADR-020 admissão de warnings pré-loop fechou E3 da auditoria anterior — 5 warnings hoje, próximo entra por critério mecânico.
- ADR-021 curadoria de free-read fechou E1 — `**ADRs candidatos:**` + scan com threshold N=15 mitiga crescimento de ADRs.
- ADR-024 + `docs/procedures/cleanup-pos-merge.md` fechou L1 (acoplamento /triage↔/release).
- Forge auto-detect agora consistente em **5 sites** (`/triage §0` via procedure, `/run-plan §3.7`, `/release §5`, `/next §4.5`, `/archive-plans §1` critério 6) — coerência cross-skill.

**Pontos de atenção:**

- **(E1) `docs/plans/` em 78 — 22 de margem para gatilho ADR-014 (≥100).** `/archive-plans` pronta. Mas ADR-022 (que define a política) ainda Proposto, e a skill nunca foi exercida em produção do toolkit (toda a árvore de planos da v1.x está intocada). Risco: descobrir bug operacional da skill no momento que mais conta (volume crescente). Antecipar primeira execução real (mesmo seca, com `Cancelar` no gate) valida a mecânica de coleta+preview sem custo.
- **(E2) 30 ADRs em 9 dias (2026-05-06 → 2026-05-14).** Ritmo extremo; gatilho original do free-read (ADR-011, "≥30") atingido mas mitigado por ADR-021 antes do impacto material. Próxima vigilância: scan keyword com 15 ADRs candidatos quando o universo total passa de 50 começa a perder seletividade. Threshold N=15 do ADR-021 vale revalidar quando ADRs totais > 50 (margem similar à de planos).
- **(E3) `/draft-idea` regressão observada em 2026-05-15.** ADR-031 § Origem registra: skill rodou no próprio toolkit (v2.8.1) com argumento descrevendo feature e gravou `IDEA.md` monograficamente sobre a feature, regredindo descoberta do papel `product_direction`. Passo 1.5 já corrige (cutucada de maturidade). Mas o incidente expõe que o sub-fluxo de presença da skill (ADR-027) não tinha defesa contra uso fora de contexto — pattern recorrente quando skill nova é lançada sem dogfood completo. Vide memória "Correção de tooling antes de feature nova".
- **(E4) ADR-026 absorção pré-commit funcional, mas commit message pode crescer.** Quando ≥1 finding absorvido, commit message inclui `## design-reviewer findings absorvidos` com bullets. Em plano grande com muitos blocos, vários commits podem carregar esta seção. Não vi caso real ainda; vale monitorar se commit messages ficam ruidosos em changelog.
- **(E5) `/note` skill referenciada por ADR-032 ainda não existe.** Plano correspondente (`docs/plans/skill-note-contexto-compartilhado.md`) existe; skill não foi criada. Stub Proposto + plano sem skill = inventário de decisão antes da implementação. Se essa for a sequência canônica (decisão antes do código), ok; mas ADR-032 está com placeholders, então nem a decisão está fechada.

### 2.4 Redução de gates & verbosidade desnecessários

**Forte:** Sem regressão desde 2026-05-12. ADR-020 + ADR-026 estabilizam critérios mecânicos onde antes havia gates caso-a-caso.

**Pontos de atenção:**

- **(G1) `/run-plan §3.3` sanity check de docs** com 3 condições de skip persiste como mecânica densa. G1 da auditoria anterior segue válido; sem incidente real ainda.
- **(G2) Cutucada de descoberta agora em 5 skills** (5ª = `/draft-idea`). Gating com triple-outcome (CLAUDE.md ausente / marker ausente / dedup) duplicado em 5 sites. ADR-017 § Alternativa (g) aceitou 4× duplicação; ADR-029 § Gatilhos recalibrou para "6º site reabre". Próxima skill `roles.required` (ADR-032 fala em `/note`?) bate no gatilho. Se materializar, helper compartilhado vira menos custoso do que continuar duplicando.

### 2.5 Otimização de tokens (input/output) — arquitetural

**Forte:** ADR-021 reduziu materialmente o custo de `design-reviewer` por invocação (curadoria + scan keyword vs free-read completo). Auto-loaded continua só `CLAUDE.md` + `MEMORY.md`.

**Pontos de atenção:**

- **(T1) `templates/IDEA.md` lido por `/draft-idea` mesmo em modo update sem nenhuma seção escolhida** (passo 4 do SKILL.md instrui `Read` do esqueleto). Otimização marginal; skill curta (137 linhas).
- **(T2) `docs/procedures/cleanup-pos-merge.md` lido por `/triage §0` e `/release` § Cleanup**. Procedure auto-loaded em runtime via `Read`. Não auto-loaded como o `CLAUDE.md`; custo amortizado.
- **(T3) Crescimento de ADRs (30 hoje) + crescimento de planos (78 hoje) ainda dentro de orçamento.** Free-read scan keyword (ADR-021 N=15) e `/archive-plans` (uma vez exercido) absorvem a curva.

### 2.6 Lógica e relações entre artefatos

**Forte:**

- Cadeias de ADR sucessores agora explícitas via campo "Origem" em cada ADR proposto (027 referencia 005; 029 referencia 017; 031 referencia 027). Pattern consistente.
- `templates/IDEA.md` carrega comentários HTML como guias-de-conteúdo, perguntas vivem em `/draft-idea` SKILL.md (decisão F2 do design-reviewer no plano). Separação template (estrutura) vs skill (interview) preservada.
- Forge auto-detect agora padrão claro em 5 sites com mesma estrutura (parse → CLI → fallback textual).

**Pontos de atenção:**

- **(L1) ADRs Propostos com mecânica em vigor introduzem ambiguidade de fonte da verdade.** Operador lendo SKILL.md vê comportamento implementado; lendo ADR Proposto vê "decisão ainda não fechada". Se a onda v1.25.0 falhar em promover, drift persiste. Onda em progresso resolve naturalmente; o ponto é gatilho preventivo: ADR-Proposto cuja mecânica foi shippada deve ter promoção próxima (memória "Limiar de ADR para mudanças em doutrina" já registra default ADR para refinos doutrinários — promoção em onda casa com o critério).
- **(L2) `block_gitignored.py:64-66` allowlist `.claude/`** segue hardcoded. L2 da auditoria anterior persiste. Risco baixo (convenção CC estável).
- **(L3) ADR-032 stub vazio é referência cruzada cega.** Plano `docs/plans/skill-note-contexto-compartilhado.md` referencia ADR-032 como base, ADR-032 referencia o plano como mensageiro. Sem decisão concreta, é loop circular de placeholders. Se o operador abandonar o caminho, ADR-032 vira lixo no índice; se prosseguir, decisão precisa ser fechada antes da skill.
- **(L4) `/triage` está com 191 linhas — empatada com `/run-plan` como maior skill.** T3 da auditoria anterior identificou 197 linhas; redução marginal (~6 linhas, refator de §0 → procedure). Crescimento de novas pré-condições (cross-mode ADR-025, campo `**Branch:**` ADR-028) compensou redução. Continua dentro do orçamento, mas seção §4 (Produzir os artefatos) é dominante (~70 linhas).

---

## 3. Propostas

Cada proposta marca explicitamente **criar/editar/remover**, escopo, impacto esperado, risco e dependências.

### A. **Editar** — Promover ADRs Proposto→Aceito da onda v1.25.0

**Escopo:** revisar status dos 7 ADRs Proposto cuja mecânica já está em vigor (022, 024, 025, 027, 028, 029, 030, 031) — promover Aceito quando a implementação confirma a decisão; cancelar/refinar quando dogfood revelar gap. BACKLOG v1.25.0 já registra o item ("promover 7 ADRs Strong de Proposto→Aceito"); auditoria captura o snapshot e formaliza o gatilho preventivo.

**Impacto:** elimina ambiguidade de fonte da verdade (L1 acima). Promove inventário de decisões a refletir o estado real do código. ADR-026 já foi aceito após implementação — replicar pattern.

**Risco:** baixo. Operação editorial; nenhuma mudança comportamental. Confirmação cross-ADR-implementação por design-reviewer no plano de promoção captura discrepâncias.

**Dependências:** nenhuma. Pode rodar como onda editorial única ou ADR-a-ADR conforme conveniência.

### B. **Editar/Criar** — Decidir destino de ADR-032

**Escopo:** ADR-032 (`/note` + store de contexto compartilhado) está como stub: status Proposto, mas `## Contexto`/`## Decisão`/`## Consequências` ainda com placeholders `<...>`. Plano `docs/plans/skill-note-contexto-compartilhado.md` existe mas skill `/note` não foi criada. Duas saídas:

- (b1) **Completar o ADR**: preencher seções, fechar decisão, então implementar skill `/note`.
- (b2) **Rebaixar para draft + esconder do índice canônico** até a decisão maturar (ex.: status "Draft" não-listado no `## Concluídos` do BACKLOG).
- (b3) **Cancelar** se o plano não tem mais viabilidade (descartar a iniciativa, manter o stub como histórico).

**Impacto:** elimina ruído no índice de decisões (L3). ADR vazio é mensageiro sem mensagem.

**Risco:** baixo. Operação editorial; nada compromissado.

**Dependências:** decisão de plano precede edição do ADR (b1). Decisão de plano também decide o destino do plano (`docs/plans/skill-note-contexto-compartilhado.md`).

### C. **Editar** — Reclassificar `/triage roles.required = [plans_dir]` para informational

**Escopo:** mover `plans_dir` de `required` para `informational` no frontmatter de `/triage`. Comportamento atual:
- Caminhos "só linha de backlog", "ADR-only delegado", "atualização domain/design" não consomem `plans_dir`.
- Apenas o caminho-com-plano grava em `<plans_dir>/<slug>.md`.

Tornar informational alinha frontmatter à dependência real (paralelo a `/debug` que declara só informational apesar de ler `decisions_dir`). Skill ganha sub-fluxo: quando passo 3 escolhe "plano" e `plans_dir` resolveu "não temos", aplicar oferta canonical via enum (paralelo ao sub-fluxo de `backlog` no passo 4 — já existe pattern).

**Impacto:** frontmatter passa a refletir dependência real. Caminhos sem plano não são bloqueados por `plans_dir` ausente. Sem regressão de cobertura — sub-fluxo de oferta canonical preserva ergonomia no caminho com plano.

**Risco:** baixo. Edição de frontmatter + ~10 linhas no SKILL.md (sub-fluxo de criação). ADR-003 frontmatter declarativo prevê required vs informational como propriedades-por-papel-por-skill (mesmo papel pode ser required em uma e informational em outra).

**Dependências:** nenhuma.

### D. **Editar** — Adendo ADR-001 cobrindo single-consumer em `templates/`

**Escopo:** ADR-001 estabeleceu `templates/` como single source of truth para esqueletos consumidos por **múltiplas skills**. `IDEA.md` foi adicionado via ADR-027 com 1 consumidor (`/draft-idea`) sem reabrir critério em ADR-001 § Implementação. Duas saídas:

- (d1) **Adendo ADR-001 § Implementação** registrando que single-consumer também justifica `templates/` quando o artefato é declarativo (esqueleto preenchível) e separar SKILL.md (algoritmo) de template (esqueleto) tem valor editorial — critério "skill geradora com template" relaxa exigência de 3+ consumidores.
- (d2) **Mover `templates/IDEA.md` para `skills/draft-idea/template.md`** (collocated) preservando ADR-001 escopo original.

**Impacto:** elimina drift implícito de critério editorial de `templates/`. Decide se é categoria pura "compartilhado N≥2" (mover IDEA.md) ou categoria "esqueleto declarativo" (mantém + adendo).

**Risco:** baixo. Edição editorial. Nenhuma mudança comportamental se d1; refactor de path em /draft-idea se d2.

**Dependências:** nenhuma direta. Vale resolver antes do 3º template emergir.

### E. **Avaliar** — Critério editorial "refinamento de mecânica → adendo em ADR, não novo ADR"

**Escopo:** registrar em `CLAUDE.md` (ou ADR meta-doutrina) o critério que distingue:
- (e1) **Novo ADR** quando: muda decisão estrutural, contradiz ADR anterior, codifica restrição externa de longa duração, ou introduz categoria nova.
- (e2) **Adendo em ADR existente (§ Implementação ou § Limitações)** quando: refina mecânica sem alterar decisão central, ajusta threshold mecânico, formaliza pattern emergente das skills.

Sustenta as cadeias temáticas (design-reviewer, modo local, cutucada) sem proliferação de ADRs incrementais.

**Impacto:** reduz custo cognitivo de leitura do índice. Cadeia design-reviewer em 4 ADRs é caso atual; cadeia modo local em 4 ADRs é outro. Próximo refinamento dispara critério explícito.

**Risco:** médio. Critério pode ser interpretado como "evitar ADR" — vide memória "Limiar de ADR para mudanças em doutrina" — refinar/inverter critério documentado em philosophy.md/CLAUDE.md (mesmo parcial) → **default ADR**. Adendo é alternativa quando refinamento é mecânico, não doutrinário. Diferenciação delicada; pode requerer próprio ADR meta. Reabrir como ADR talvez seja a saída coerente com a regra-mãe.

**Dependências:** se for ADR, sequenciar como tema mais alto na onda editorial (auto-aplicação).

### F. **Avaliar** — Antecipar primeira execução de `/archive-plans` (dogfood seco)

**Escopo:** rodar `/archive-plans` no toolkit em modo preview (gate `Cancelar` final), apenas para validar:
- coleta dos 78 planos atuais
- aplicação dos 6 critérios cumulativos
- preview estruturado (elegíveis / não-elegíveis / cross-refs)
- comportamento sob `--quarter` opcional

Sem aplicar archival ainda — só validar que a skill funciona em escala real antes de gatilho ADR-014 (≥100) forçar uso reativo.

**Impacto:** captura bugs operacionais da skill antes do volume material. Custo: 1 invocação de ~30s + leitura de preview.

**Risco:** baixo. Modo preview é não-destrutivo por design.

**Dependências:** ADR-022 ainda Proposto; rodar dogfood pode também alimentar a promoção (caso A item ADR-022).

### G. **Editar** — Helper compartilhado para cutucada de descoberta (gatilho ADR-029 atingido com `/draft-idea`)

**Escopo:** ADR-017 aceitou 4× duplicação como YAGNI; ADR-029 recalibrou para "6ª `roles.required` skill reabre". Hoje **5 skills** com `roles.required` emitem a cutucada (5ª = `/draft-idea`). Próxima skill (ex.: `/note` da ADR-032 se materializar) bate gatilho. Antecipar extração para helper documental (procedure em `docs/procedures/cutucada-descoberta.md` referenciado por cada SKILL via `Read`) reduz custo de manutenção e elimina drift de string entre sites.

**Impacto:** ~30 linhas removidas cross-skill. String canonical em um único lugar. Padrão paralelo a `docs/procedures/cleanup-pos-merge.md`.

**Risco:** baixo. Extração editorial não-comportamental. Test de regressão: confirmar que cutucada continua disparando nos 5 sites após o refactor.

**Dependências:** nenhuma. Vale antes da 6ª skill consumidora.

### H. **Editar** — Documentar dependência implícita `block_gitignored.py` ↔ convenção Claude Code

**Escopo:** L2 da auditoria 2026-05-12 segue válido. Allowlist `.claude/` é hardcoded; depende de Claude Code manter `.claude/` como root de territorialidade do harness. Adicionar comentário no script (ou ADR cirúrgico) explicitando dependência e gatilho de revisão (mudança da convenção CC).

**Impacto:** acoplamento implícito vira explícito. Sem mudança comportamental.

**Risco:** baixo. Cosmético / docs.

**Dependências:** nenhuma. Item pequeno; pode entrar como linha de backlog.

---

## 4. Sequenciamento sugerido

Ordenado por **leverage / risco × urgência preditiva**:

### Primeira onda — fechamento editorial em curso

1. **A (promoção ADRs Proposto→Aceito v1.25.0)** — onda já registrada no BACKLOG; auditoria captura snapshot. Reduz ambiguidade de fonte da verdade (L1) e fecha drift Proposed/implementação imediatamente.
2. **B (destino ADR-032)** — eliminação de ruído no índice; bloqueia A se incluído na onda v1.25.0 (status do 032 indecidido).

### Segunda onda — coerência editorial

3. **C (`/triage roles.required` → informational)** — frontmatter passa a refletir dependência real; alinha com ADR-003. Mudança trivial baixo-risco.
4. **D (single-consumer em `templates/`)** — decisão preventiva antes do 3º template. d1 (adendo ADR-001) parece coerente; d2 (mover IDEA.md) é alternativa.

### Terceira onda — preventivo de escala

5. **F (dogfood seco `/archive-plans`)** — validação antes do gatilho ADR-014. Custo trivial; informa A item ADR-022.
6. **G (helper cutucada descoberta)** — gatilho ADR-029 a 1 skill de distância. Extração editorial preventiva.

### Quarta onda — meta-doutrina

7. **E (critério adendo vs novo ADR)** — sustenta cadeias temáticas. Pode requerer próprio ADR meta dado o limiar canonical "refinar critério documentado → default ADR" (memória feedback). Auto-aplicação coerente.

### Quinta onda — débito conhecido

8. **H (documentar dependência `block_gitignored.py`)** — cosmético; linha de backlog.

### Propostas que destrancam outras

- **B destranca A** quando ADR-032 entra na onda v1.25.0 (decidir status antes de promover).
- **G destranca futuras skills `roles.required`** sem inflação de prosa duplicada.
- **F informa A** (item ADR-022) com evidência empírica.
- **D destranca futuros templates** com critério explícito.

---

## Encaminhamento

Propostas aceitas pelo operador não viram PR direto. Cada uma entra pelo fluxo padrão: `/triage <proposta>` decide artefato (linha de backlog, plano, ADR, atualização de domain/design) e segue dali.

**Sugestões de encaminhamento por proposta:**

- **A** → linha de backlog na v1.25.0 (operação meta editorial; ondas anteriores já têm pattern).
- **B** → `/triage` para decidir destino do ADR-032 (pode virar ADR sucessor, cancelamento documentado, ou status Draft).
- **C** → linha de backlog (mudança de frontmatter + ~10 linhas de SKILL).
- **D** → ADR sucessor de ADR-001 (decisão sobre critério editorial de `templates/`).
- **E** → ADR sucessor de doutrina (alinhado à memória "Limiar de ADR para mudanças em doutrina"; pode ser auto-aplicação do próprio critério).
- **F** → linha de backlog (dogfood seco, sem mudança de código).
- **G** → ADR sucessor de ADR-017/029 (decisão de extrair helper compartilhado) OU edit incremental de ADR-029 § Implementação se for considerado adendo (vide E).
- **H** → linha de backlog (comentário no script + opcional ADR cirúrgico).
