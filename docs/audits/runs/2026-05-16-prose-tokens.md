# Auditoria — prosa & tokens — 2026-05-16

Modo: diagnóstico + propostas, **zero alteração**. Prompt: `docs/audits/prose-tokens.md`. Pré-checagem: `BACKLOG.md ## Concluídos` (até v1.25.0 em progresso) + runs anteriores em `docs/audits/runs/2026-05-12-prose-tokens.md` e `docs/audits/runs/2026-05-12b-prose-tokens.md`.

**Estado das auditorias anteriores:** todas as propostas (7 da run-1 + 4 da run-2) shippadas via execution-roadmap 2026-05-12 (Ondas 1-4 + Diferida). Zero pendências de prosa do ciclo anterior. Auditoria corrente roda sobre corpus pós-ondas + delta v2.4.0→v2.8.1 (+2 skills, ADRs 026-031, refator cleanup→procedure).

**Auditoria complementar arquitetural** (`docs/audits/runs/2026-05-15-architecture-logic.md`): identifica ponto-mãe novo — drift entre 7 ADRs Proposto e implementação shippada. Pontos arquiteturais (`/triage roles.required`, ADR-032 stub, templates/IDEA.md single-consumer) ficam fora desta auditoria; propostas G_arch (helper cutucada descoberta) ressurgem aqui pelo eixo prosa (medida em palavras).

---

## 1. Inventário & métricas

### Artefatos auto-loaded (carregados a cada turn)

| Path | Linhas | Palavras | Carregamento |
|---|---|---|---|
| `CLAUDE.md` | 178 | 2755 | auto-loaded |
| `MEMORY.md` (user) | (~30) | (~700) | auto-loaded |

CLAUDE.md cresceu de 171→178 linhas desde 2026-05-12 (+4%). Cap nominal mencionado em `MEMORY.md` (200 linhas) — margem 12%. Adições recentes: seção "Cutucada de descoberta" estendida por ADR-029 (cobertura `CLAUDE.md` ausente), referência a ADR-026 em "AskUserQuestion mechanics".

### Doctrine sources (lidos por skills/agents via referência cruzada)

| Path | Linhas | Palavras | Carregamento |
|---|---|---|---|
| `docs/philosophy.md` | 77 | 1379 | sob demanda (referenciado por skills/agents) |
| `docs/procedures/cleanup-pos-merge.md` | 43 | 539 | sob demanda (`/triage §0`, `/release § Cleanup`) |

### Templates (lidos por skill correspondente em runtime)

| Path | Linhas | Palavras | Carregamento |
|---|---|---|---|
| `templates/plan.md` | 55 | 379 | por invocação (`/triage` caminho-com-plano; `/run-plan` headers) |
| `templates/IDEA.md` | 43 | 225 | por invocação (`/draft-idea` passo 4) |

### Skills (10)

| Path | Linhas | Palavras | W/L | Carregamento |
|---|---|---|---|---|
| `skills/triage/SKILL.md` | 191 | 2707 | 14.2 | por invocação |
| `skills/run-plan/SKILL.md` | 191 | 3258 | 17.1 | por invocação |
| `skills/gen-tests/SKILL.md` | 170 | 1426 | 8.4 | por invocação |
| `skills/release/SKILL.md` | 167 | 1729 | 10.4 | por invocação |
| `skills/init-config/SKILL.md` | 148 | 1655 | 11.2 | por invocação |
| `skills/draft-idea/SKILL.md` | 137 | 1539 | 11.2 | por invocação |
| `skills/debug/SKILL.md` | 116 | 1039 | 9.0 | por invocação |
| `skills/new-adr/SKILL.md` | 110 | 1013 | 9.2 | por invocação |
| `skills/archive-plans/SKILL.md` | 96 | 725 | 7.6 | por invocação |
| `skills/next/SKILL.md` | 91 | 1030 | 11.3 | por invocação |
| **Total** | **1417** | **15121** | média 11.4 | — |

`run-plan` é a skill mais densa (17.1 W/L); cresceu de 170L→191L (+12%) desde 2026-05-12 sobretudo por mecânica de stderr matching em §1.1 e branch dedicado em §3.7. `triage` empata em linhas mas é menos densa (14.2 W/L).

### Agents (5)

| Path | Linhas | Palavras | Carregamento |
|---|---|---|---|
| `agents/design-reviewer.md` | 109 | 1022 | por invocação |
| `agents/code-reviewer.md` | 77 | 930 | por invocação |
| `agents/qa-reviewer.md` | 58 | 659 | por invocação |
| `agents/security-reviewer.md` | 53 | 660 | por invocação |
| `agents/doc-reviewer.md` | 61 | 552 | por invocação |
| **Total** | **358** | **3823** | — |

### Hooks (3) + manifests + landing

| Path | Linhas | Palavras | Carregamento |
|---|---|---|---|
| `hooks/block_gitignored.py` | 91 | 390 | runtime (não-prosa) |
| `hooks/run_pytest_python.py` | 78 | 292 | runtime (não-prosa) |
| `hooks/block_env.py` | 46 | 179 | runtime (não-prosa) |
| `hooks/hooks.json` | 42 | 126 | runtime (não-prosa) |
| `.claude-plugin/plugin.json` | 11 | 61 | marketplace |
| `.claude-plugin/marketplace.json` | 30 | 102 | marketplace |
| `README.md` | 57 | 863 | landing (EN, ADR-012) |
| `docs/install.md` | 80 | 1118 | sob demanda |

### Frontmatter descriptions auto-loaded (10 skills + 5 agents)

| Artefato | Palavras | Description literal |
|---|---|---|
| `debug` | 18 | Diagnostica causa-raiz de sintoma (teste falhando, erro inesperado, comportamento divergente) por método científico. Produz diagnóstico, não fix. Stack-agnóstico. |
| `new-adr` | 21 | Cria novo ADR no decisions_dir com numeração inferida e template padronizado. Use quando o operador pedir registro de decisão estrutural duradoura. |
| `archive-plans` | 23 | Periodic editorial archival of historical plans from docs/plans/ to docs/plans/archive/<YYYY-Qx>/, preview-first, non-destructive (git mv). Use when the maintainer wants to archive aged plans. |
| `draft-idea` | 24 | Elicita IDEA.md (papel product_direction) via interview estruturado quando o operador tem ideia vaga. Use upstream de /triage, quando a intenção ainda não está formada. |
| `next` | 24 | Lê o backlog, descarta itens já implementados e sugere top 3 candidatos por impacto estratégico. Invocável direto ou como pré-passo de /triage sem argumento. |
| `release` | 24 | Bump de versão em version_files, entrada de changelog, commit unificado e tag anotada local (não faz push). Use quando o operador autorizou publicar release. |
| `run-plan` | 27 | Executa plano de docs/plans/<slug>.md em worktree isolada, com micro-commits, revisor por bloco e gate de validação manual. Use quando há plano pronto e o operador autorizou implementar. |
| `gen-tests` | 27 | Gera arquivo de teste para módulo, função ou descrição livre, com idioms da stack do projeto consumidor (Python e Java suportadas). Use quando o operador pedir testes. |
| `init-config` | 29 | Wizard interativo para configurar o bloco `<!-- pragmatic-toolkit:config -->` no `CLAUDE.md`. Use quando o operador quer configurar o plugin de uma vez em projeto novo ou reconfigurar bloco existente. |
| `triage` | 29 | Alinha intenção e decide artefato (backlog, plano, ADR, atualização de domain/design) antes de implementar. Use quando o operador propuser feature, fix ou refactor sem plano nem linha de backlog. |
| `doc-reviewer` | 24 | Revisor de drift entre documentação e código no diff. Stack-agnóstico. Acionar quando o diff toca `.md`/`.rst`/`.txt` ou renomeia/remove identificadores referenciados em docs. |
| `code-reviewer` | 33 | Revisor de estilo e arquitetura focado na filosofia flat e pragmática (YAGNI, sem abstrações prematuras, sem comentários redundantes, sem defensividade desnecessária). Acionar antes de PR para flagrar violações de YAGNI no diff. |
| `qa-reviewer` | 33 | Revisor de qualidade de testes focado em cobertura de invariantes documentadas, edge cases declarados e separação mock-vs-real. Acionar antes de PR para verificar se a mudança tem testes alinhados. |
| `design-reviewer` | 37 | Revisor de decisões arquiteturais e de design em documento pré-fato (plano ou ADR draft). Acionado automaticamente em `/triage` que produz plano e em `/new-adr` (standalone ou delegada) per ADR-011; manualmente via `@design-reviewer`. Stack-agnóstico. |
| `security-reviewer` | 42 | Revisor de segurança focado em segredos, validação de entrada em fronteiras, I/O externo, dados sensíveis, privilégios e invariantes documentadas em ADRs. Stack-agnóstico. Acionar antes de PR quando a mudança envolver segredos, handlers de fronteira ou persistência de dados sensíveis. |

Total auto-loaded de descriptions: **~480 palavras** (~640 tokens) por turn. `security-reviewer` é a mais longa (42 w); `debug` a mais curta (18 w). 5 descriptions ≥27 w são candidatas a aperto.

---

## 2. Diagnóstico por critério

### 2.1 Coesão & coerência interna/externa

**Forte.** Hub-and-spoke editorial de "Reviewer/skill report idioma" criado por ADR-007 (B_prose shippado) reduziu 6 sites a um único em `CLAUDE.md` § "Reviewer/skill report idioma". Sub-fluxo de presença das skills geradoras (criação canonical via enum) descrito em `CLAUDE.md` § "Required vs informational roles" e referenciado por `/triage` step 4, `/new-adr`, `/draft-idea` — pattern consistente.

**Pontos de atenção:**

- **(C1) `templates/IDEA.md` (43 L / 225 W) lido por invocação de `/draft-idea` mesmo em modo update sem nenhuma seção escolhida.** Passo 4 do SKILL.md instrui `Read` do esqueleto sempre. Em modo update com zero seções escolhidas (skip silente, ver passo 3), Read poderia ser pulado. Custo: 225 W por invocação ociosa, raro (skip silente já é caminho de exceção).
- **(C2) `description` do `security-reviewer` (42 w) tem auto-overlap.** Primeira frase enumera categorias ("segredos, validação de entrada em fronteiras, I/O externo, dados sensíveis, privilégios"); segunda frase repete subset ("envolver segredos, handlers de fronteira ou persistência de dados sensíveis"). Categorias recitadas 2×. Comparar com `code-reviewer` (33 w sem repetição interna) e `debug` (18 w focado em gatilho).

### 2.2 Clareza & desambiguação

**Forte.** ADR-020 + ADR-026 trouxeram critérios mecânicos em tabela/enum em vez de prosa contínua. `/run-plan §3.3` sanity check de docs já está em tabela (E_prose shippado).

**Pontos de atenção:**

- **(D1) `/run-plan §1.1` (Setup da worktree → Falha de criação)** descreve 4 sub-casos de discriminação por stderr em prosa contínua (~25 linhas, ~300 palavras). Cada caso tem (a) regex de identificação, (b) linha-tipo a gravar no backlog, (c) ação. Estrutura tabular reduziria leitura: `| Caso | Detecção (stderr) | Linha-tipo | Ação |`. Padrão paralelo a `/run-plan §3.3` (sanity docs) e tabela de warnings pré-loop (§ Detecção de warnings).
- **(D2) `## O que NÃO fazer` do `/init-config` tem 7 bullets** — maior número entre 10 skills (média 4). Todos parecem genuínos (postura editorial não-reparativa, exceções ADR-005/017/025/030); recapitular para confirmar que cada um é não-óbvio ou pós-incidente. Comparar com `/gen-tests` que tem 1 bullet enxuto ("Não testar invariantes que o código alvo não exerce — só comportamento real do código.") e `/archive-plans` com 2.

### 2.3 Alinhamento à `docs/philosophy.md`

**Forte.** Doutrina "cerimônia tática não" honrada: cleanup pós-merge extraído como procedure compartilhada (vs duplicação em 2 skills); hub-and-spoke de idioma (vs prosa duplicada em 6 sites). `philosophy.md` permanece em 77 L / 1379 W (estável desde D_prose); cabeçalhos enxutos (8 seções).

**Pontos de atenção:**

- **(F1) `release` description duplica output + gatilho (24 w).** "Bump de versão em version_files, entrada de changelog, commit unificado e tag anotada local (não faz push). Use quando o operador autorizou publicar release." — primeira frase enumera saídas (output); segunda repete gatilho usando "operador autorizou publicar release" que é redundante com `release` no name. Comparado com `debug` (18 w, foco gatilho).
- **(F2) Convenções editoriais espalhadas:** `philosophy.md` § "Convenção de naming" + `CLAUDE.md` § "Plugin component naming and hook auto-gating" tratam o mesmo eixo. philosophy.md fala alto-nível ("3 categorias por critério de acoplamento à stack"); CLAUDE.md tem a tabela mecânica + 3-layer gating. Padrão hub-and-spoke já implementado (CLAUDE.md referencia philosophy.md por path). Coerente; sem proposta.

### 2.4 Inflação de tokens

**Forte.** ADR-021 reduziu materialmente custo do design-reviewer por invocação. Auto-loaded estável.

**Pontos de atenção:**

- **(T1) Descriptions auto-loaded total ~480 w (~640 tokens) por turn.** 5 das 15 descriptions têm ≥27 w; 3 têm ≥29 w (`init-config`, `triage`, `security-reviewer`-42w). Aperto seletivo reduz ~60 w (~80 tokens) por turn.
- **(T2) Auto-detect forge inline em 4 SKILLs + 1 procedure** (~30 w/site × 4 sites inline = ~120 w duplicação por invocação respectiva). Cleanup pós-merge precedente — extração para `docs/procedures/forge-auto-detect.md` referenciada por `Read` reduz cada SKILL em ~25 w + concentra mecânica em 1 lugar.
- **(T3) Cutucada de descoberta duplicada em 5 SKILLs** (~30 w/site × 5 = ~150 w por invocação respectiva). Identificado também em arquitetural (proposta G_arch); aqui medido em palavras. Helper documental seguindo padrão de cleanup-pos-merge concentraria as duas strings + tabela tri-state em um único site.
- **(T4) CLAUDE.md em 178 L / 2755 W, cap nominal 200 L.** Margem 12% (vs 17% em 2026-05-12 quando era 171 L). Crescimento iminente se ADRs 029-031 forem promovidos com novas referências.
- **(T5) `/run-plan` cresceu 191 L / 3258 W** desde 2026-05-12 (170 L). +21 linhas / +~400 W em 3 dias. Crescimento concentrado em §1.1 (stderr matching) e §3.7 (modo local + branch). É a maior contribuinte para custo por invocação entre skills.

### 2.5 Duplicação cross-artifact

**Forte.** Hub-and-spoke de idioma + extração de cleanup pós-merge fecharam principais focos da auditoria anterior.

**Pontos de atenção:**

- **(P1) Auto-detect forge:** mecânica idêntica em 5 sites — `skills/release/SKILL.md`, `skills/next/SKILL.md`, `skills/run-plan/SKILL.md`, `skills/archive-plans/SKILL.md`, `docs/procedures/cleanup-pos-merge.md`. Estrutura: parse `git remote get-url origin` → `github.com` → `gh` / regex `^gitlab\.` → `glab` / fallback textual com link CLI. ~25 w por site. Procedure pode ser fonte canonical; 4 SKILLs referenciam via `Read`.
- **(P2) Cutucada de descoberta:** strings canonical (string-A para marker ausente, string-B para CLAUDE.md ausente) + tabela tri-state literalmente duplicadas em 5 SKILLs (`new-adr`, `next`, `run-plan`, `triage`, `draft-idea`). ADR-017 § Alternativa (g) aceitou 4× duplicação como YAGNI; ADR-029 recalibrou para "6º site reabre". Já estamos em 5. Helper documental (~30 w por site × 5) economiza ~120 w líquidos + elimina drift entre sites.
- **(P3) Triple auto-gating em comentário de hook:** `hooks/run_pytest_python.py` linhas 4-7 e `hooks/block_gitignored.py` linhas 9-12 trazem cabeçalho doctrinal mini-replicado em comentário. `CLAUDE.md § Plugin component naming and hook auto-gating` tem a versão canonical. Duplicação curta (~30 w cada hook), aceitável como boa-prática Python (cabeçalho explica intenção do script standalone); sem proposta.

### 2.6 Justificativas-cicatriz

**Forte.** Onda 2026-05-12 (A_prose) removeu cicatrizes obvias ("From v1.11.0 onward", "Release cadence" detalhada). Hoje cicatrizes residuais são pontuais.

**Pontos de atenção:**

- **(J1) `/draft-idea` bullet "Não codificar perguntas em comentários HTML do templates/IDEA.md ... (decisão F2 do design-reviewer no plano)"** — cita decisão F2 de plano específico como justificativa. Cicatriz interna de PR/plano; reader externo não tem contexto. Anti-padrão genuíno (separação template vs interview), mas justificativa "decisão F2" é internamente datada. Remover citação preserva regra: "Não codificar perguntas em comentários HTML do `templates/IDEA.md` — template carrega só guias-de-conteúdo descritivos; perguntas vivem na prosa do passo 2."
- **(J2) `/run-plan` bullet "Não emitir comando que altere estado externo ... incluindo mas não limitado a `git checkout`/`git switch` no principal, `git branch -D`, `git worktree remove`, `git reset --hard`. A doutrina é parar e escrever no backlog (CLAUDE.md global exige confirmação explícita para ações de blast-radius compartilhado; este SKILL não autoriza recovery silenciosa)."** — bullet longo com referência cruzada a "CLAUDE.md global". Doctrine cross-ref é load-bearing (incidente real registrado), mas enumeração `git checkout/switch/branch -D/worktree remove/reset --hard` é exaustiva e pode caber em "comandos destrutivos não-autorizados" + 1 exemplo.

### 2.7 Frontmatter `description` (sempre carregado pelo roteador)

**Forte:** auditoria anterior (C_prose) reduziu 4 descrições; total auto-loaded estável em ~480 w. Padrão "Use quando..." adotado em 9 das 15 entradas.

**Pontos de atenção:**

- **(F-frontmatter-1) `security-reviewer` 42 w**, identificado em C2. Mais longa entre agents.
- **(F-frontmatter-2) `init-config` 29 w** com cauda "para configurar o plugin de uma vez em projeto novo ou reconfigurar bloco existente" — redundante com "Wizard interativo para configurar o bloco" da primeira frase.
- **(F-frontmatter-3) `triage` 29 w** com "Use quando o operador propuser feature, fix ou refactor sem plano nem linha de backlog" — descrição condicional longa. "feature, fix ou refactor" enumera tipos cobertos por "mudança não-trivial" + "sem plano nem linha de backlog" já é o gatilho mecânico canonical.
- **(F-frontmatter-4) `release` 24 w** identificado em F1.

### 2.8 `## O que NÃO fazer` (scope guards)

**Forte:** 10/10 skills mantêm a seção (load-bearing per CLAUDE.md § Editing conventions). Critério "anti-padrão não-óbvio" honrado na maioria; bullets curtos predominam.

**Pontos de atenção:**

- **(N1) `/init-config` 7 bullets:** todos identificáveis como anti-padrão não-óbvio ou exceção localizada (ADR-005/017/025/030 referenciadas explicitamente). Comprimento da seção espelha número de exceções formalizadas; sem corte óbvio.
- **(N2) `/run-plan` 7 bullets:** denso (~250 w). Bullet (J2) acima é o mais longo. "Não interpretar `{revisor: ...}` (PT)" é cicatriz pós-incidente útil. Demais são pós-ADR ou anti-padrão genuíno.
- **(N3) `/draft-idea` 6 bullets:** identificado em J1; bullet 5 ("Não invocar `/triage` automaticamente — só **sugere** no relatório (passo 5)") repete instrução do passo 5. Viés sutil (modelo tende a invocar Skill em cascata) torna a guarda genuína per critério editorial, mas a parte "(passo 5)" recapitula o body.

---

## 3. Propostas

Cada proposta marca explicitamente **criar/editar/remover**, escopo, estimativa de redução em palavras/tokens e dependências.

### A. **Editar** — Encurtar 4 descriptions auto-loaded longas

**Escopo:** apertar descriptions de `security-reviewer` (42→~28 w), `init-config` (29→~22 w), `triage` (29→~22 w), `release` (24→~18 w). Cortes:

- `security-reviewer`: remover frase final "Acionar antes de PR quando a mudança envolver segredos, handlers de fronteira ou persistência de dados sensíveis" — categorias já enumeradas na primeira frase; "Acionar antes de PR" idem.
- `init-config`: remover "em projeto novo ou reconfigurar bloco existente" — cobertos por "Wizard interativo para configurar o bloco".
- `triage`: condensar "feature, fix ou refactor sem plano nem linha de backlog" → "mudança não-trivial sem plano ou linha de backlog".
- `release`: remover "Use quando o operador autorizou publicar release" — `release` no name já é o gatilho.

**Redução estimada:** ~50 palavras (~65 tokens) auto-loaded por turn. ~10% redução das 4 descriptions afetadas.

**Risco:** baixo. Edição editorial; cobertura mantida pelos primeiros 18-22 w de cada uma.

**Dependências:** nenhuma.

### B. **Criar** — `docs/procedures/forge-auto-detect.md` (extrair mecânica de 4 SKILLs)

**Escopo:** consolidar a mecânica auto-detect forge (parse `git remote get-url origin` → `github.com` → `gh` / regex `^gitlab\.` → `glab` / fallback textual com link CLI) em procedure compartilhada. Padrão paralelo a `docs/procedures/cleanup-pos-merge.md` (já em vigor). Cada SKILL substitui ~25 w inline por 1 linha de referência (`per docs/procedures/forge-auto-detect.md`).

Sites afetados: `skills/release/SKILL.md §5` (Forge), `skills/next/SKILL.md §4.5` (PRs em curso), `skills/run-plan/SKILL.md §3.7` (Publicar), `skills/archive-plans/SKILL.md §1` (critério 6 — PR aberto). `docs/procedures/cleanup-pos-merge.md` já tem versão da mecânica embutida — substituir por referência também.

**Redução estimada:** ~100 palavras (~130 tokens) líquidos cross-skill (4 SKILLs × ~25 w substituídos por ~1 linha, menos ~30 w novos no procedure). Por invocação respectiva, não auto-loaded.

**Risco:** baixo-médio. Refator editorial cross-skill; verifica que cada SKILL preserva contexto local (gate `AskUserQuestion` específico de cada caminho continua na SKILL — só a parte de detecção forge migra). Padrão já validado em cleanup-pos-merge.

**Dependências:** nenhuma. Vale antes de quinta skill consumidora emergir.

### C. **Criar** — `docs/procedures/cutucada-descoberta.md` (extrair de 5 SKILLs)

**Escopo:** consolidar tabela tri-state da cutucada (CLAUDE.md ausente / marker ausente / dedup) + strings canonical em procedure. Sites afetados: `skills/triage/SKILL.md`, `skills/run-plan/SKILL.md`, `skills/new-adr/SKILL.md`, `skills/next/SKILL.md`, `skills/draft-idea/SKILL.md` — cada um substitui ~30 w por 1 linha de referência (`Antes de devolver controle, aplicar **cutucada de descoberta** per docs/procedures/cutucada-descoberta.md.`).

Mesma motivação que B, eixo distinto. ADR-029 § Gatilhos recalibrou gatilho de reabertura para "6ª `roles.required` skill" — antecipar extração evita 6ª duplicação se `/note` (ADR-032) materializar. Identificado também na auditoria architecture-logic 2026-05-15 (proposta G_arch); aqui é a mesma proposta pelo eixo prosa, com estimativa quantitativa.

**Redução estimada:** ~120 palavras (~155 tokens) líquidos cross-skill (5 SKILLs × ~30 w substituídos por ~1 linha, menos ~30 w novos no procedure). Por invocação respectiva.

**Risco:** baixo. Refator editorial cross-skill; cada SKILL preserva sua mecânica de "dedup hit" (julgamento de contexto visível) — só a tabela tri-state + 2 strings migram. Test de regressão: confirmar que cutucada continua disparando nos 5 sites após o refactor.

**Dependências:** independente de B. Pode rodar em paralelo. Se A/B/C virarem uma onda, sequenciar 1 PR por extração para revisão mais fácil.

### D. **Editar** — Estruturar `/run-plan §1.1` (4 sub-casos stderr) em tabela

**Escopo:** prosa contínua atual descreve 4 casos de falha de `git worktree add` (branch inexistente, branch já checked out em outro worktree, diretório existe sem registro git, outras falhas) em ~300 palavras com regex inline. Reescrever como tabela `| Detecção (stderr regex) | Linha do backlog | Ação |`. Padrão paralelo a `## Detecção de warnings pré-loop` (mesma skill) e `/run-plan §3.3` (sanity check de docs — E_prose shippado).

**Redução estimada:** ~50 palavras (~65 tokens). Mais ganho em legibilidade que em tokens.

**Risco:** baixo. Edição editorial; comportamento inalterado.

**Dependências:** nenhuma.

### E. **Editar** — Compactar 2 bullets de "O que NÃO fazer" com cicatriz datada

**Escopo:**

- **`/draft-idea` bullet 6** (J1 acima): remover "(decisão F2 do design-reviewer no plano)" — cicatriz interna; regra fica intacta.
- **`/run-plan` bullet 5** (J2 acima): condensar enumeração exaustiva "incluindo mas não limitado a `git checkout`/`git switch` no principal, `git branch -D`, `git worktree remove`, `git reset --hard`" → "comandos destrutivos no working tree principal (ex.: `git reset --hard`, `git worktree remove`)" + manter cross-ref "CLAUDE.md global exige confirmação explícita para ações de blast-radius compartilhado".

**Redução estimada:** ~40 palavras (~50 tokens). Por invocação.

**Risco:** baixo-médio. Bullet do `/run-plan` é pós-incidente; remoção de comandos específicos pode reduzir defesa. Manter pelo menos 1 exemplo + cross-ref doutrinária preserva a regra.

**Dependências:** nenhuma.

### F. **Editar** — `/draft-idea` bullet 5 e `templates/IDEA.md` Read condicional

**Escopo:**

- `/draft-idea` bullet 5 ("Não invocar `/triage` automaticamente — só **sugere** no relatório (passo 5). Operador é quem dispara o próximo passo.") — manter (anti-padrão por viés do modelo de invocar Skill em cascata), mas cortar "(passo 5)" — recapitulação.
- `/draft-idea` passo 4: condicionar `Read` do template a "modo update com ≥1 seção escolhida OR modo one-shot". Modo update com zero seções é skip silente upstream (passo 3) — Read fica órfão.

**Redução estimada:** ~10 palavras no bullet + ~225 W economizados em invocações ociosas (raro caminho).

**Risco:** baixo. Mudança mecânica trivial em passo 4 (1 condicional); bullet preserva regra.

**Dependências:** nenhuma.

---

## 4. Sequenciamento sugerido

Ordenado por **leverage / risco × tipo de carregamento**:

### Primeira onda — auto-loaded (impacto a cada turn)

1. **A (4 descriptions encurtadas)** — ~50 w / ~65 tokens auto-loaded por turn. Maior ROI de palavras-por-edit no corpus runtime. Risco mínimo.

### Segunda onda — duplicação cross-artifact (impacto por invocação respectiva)

2. **C (cutucada de descoberta → procedure)** — ~120 w líquidos + antecipa gatilho ADR-029. Resolve também proposta G_arch da auditoria architecture-logic.
3. **B (forge auto-detect → procedure)** — ~100 w líquidos. Padrão validado em cleanup-pos-merge. Independente de C.

### Terceira onda — legibilidade e cicatriz

4. **D (`/run-plan §1.1` → tabela)** — ~50 w + maior ganho em legibilidade. Skill é a maior do corpus; cada simplificação compõe.
5. **E (compactar 2 bullets cicatriz-datada)** — ~40 w. Risco baixo-médio (bullet `/run-plan` é pós-incidente).

### Quarta onda — micro-otimização

6. **F (`/draft-idea` bullet 5 + Read condicional)** — ~10 w no bullet + Read condicional em caminho ocioso.

### Propostas que se reforçam mutuamente

- **B + C** seguem o mesmo padrão "extração para procedure" inaugurado por cleanup-pos-merge. Sequenciar B e C como onda dupla valida o padrão como categoria editorial (`docs/procedures/` ganha 2 novos artefatos no mesmo PR — coerência com ADR-024 que formaliza a categoria).
- **A + E + F** são micro-otimizações de cicatriz; podem entrar em 1 PR único (~100 w líquidos).

### Redução total estimada

| Onda | Auto-loaded | Por invocação | Tokens estimados |
|---|---|---|---|
| 1 (A) | ~50 w | — | ~65/turn |
| 2 (B+C) | — | ~220 w | ~285/invocação afetada |
| 3 (D+E) | — | ~90 w | ~115/invocação `/run-plan` |
| 4 (F) | — | ~10 w + Read condicional | trivial |
| **Total** | **~50 w auto** | **~320 w por invocação** | **~465 tokens** |

Comparado com ondas 2026-05-12 a/b combinadas (~580 w / ~755 tokens), esta onda é menor — esperado, pois a anterior limpou os maiores focos. Esta é refinamento incremental.

---

## Encaminhamento

Propostas aceitas pelo operador não viram PR direto. Cada uma entra pelo fluxo padrão: `/triage <proposta>` decide artefato (linha de backlog, plano, ADR, atualização de domain/design) e segue dali. A auditoria produz a lista; o `/triage` faz o alinhamento individual.

**Sugestões de encaminhamento por proposta:**

- **A** → linha de backlog (4 edits cirúrgicos em frontmatter, sem plano).
- **B** → plano + nova entrada em `docs/procedures/`. Pode ser plano único cobrindo B + C (mesma categoria de extração).
- **C** → plano + nova entrada em `docs/procedures/`. Resolve G_arch da auditoria 2026-05-15 (mesma proposta pelo eixo arquitetural).
- **D** → linha de backlog (refactor editorial cirúrgico em /run-plan §1.1).
- **E** → linha de backlog (2 bullets editados).
- **F** → linha de backlog (bullet + condicional em 1 passo).
