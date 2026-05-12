# Auditoria — prosa & tokens — 2026-05-12

Modo: diagnóstico + propostas, **zero alteração**. Prompt: `docs/audits/prose-tokens.md`. Pré-checagem: `BACKLOG.md ## Concluídos` + memory `project_artifact_review_v1_18` (onda 2026-05-06 já shippou 5 propostas A-F na revisão arquitetural pós-v1.20.0, incluindo "Skills: compactar prosa e enxugar `## O que NÃO fazer`", "CLAUDE.md: cortar paráfrases", "philosophy.md: refatorar para conter apenas princípios"). Esta auditoria opera em **resíduos cirúrgicos** pós-onda, não em compactação ampla.

Cruzamento com `2026-05-12-architecture-logic.md` (auditoria companion rodada na mesma sessão) anotado nas propostas — eixo estrutural lá; aqui só prosa e tokens.

---

## 1. Inventário & métricas

### Artefatos de runtime do plugin

| Artefato | Linhas | Palavras | Modo de carregamento |
|---|---:|---:|---|
| `CLAUDE.md` | 171 | 2.585 | **Auto-loaded** a cada turn (cap nominal 200 per `MEMORY.md`) |
| `docs/philosophy.md` | 77 | 1.409 | Por invocação — referenciado por skills/agents |
| `templates/plan.md` | 57 | 366 | Por invocação — Read runtime no /triage |
| **Skills (8)** | — | — | — |
| `skills/triage/SKILL.md` | 197 | 2.639 | Por invocação |
| `skills/run-plan/SKILL.md` | 170 | 2.888 | Por invocação |
| `skills/gen-tests/SKILL.md` | 169 | 1.437 | Por invocação |
| `skills/release/SKILL.md` | 159 | 1.732 | Por invocação |
| `skills/init-config/SKILL.md` | 127 | 1.343 | Por invocação |
| `skills/debug/SKILL.md` | 115 | 1.037 | Por invocação |
| `skills/new-adr/SKILL.md` | 99 | 828 | Por invocação |
| `skills/next/SKILL.md` | 86 | 980 | Por invocação |
| **Agents (5)** | — | — | — |
| `agents/code-reviewer.md` | 77 | 945 | Por invocação (subagent) |
| `agents/design-reviewer.md` | 76 | 668 | Por invocação |
| `agents/doc-reviewer.md` | 61 | 587 | Por invocação |
| `agents/qa-reviewer.md` | 58 | 668 | Por invocação |
| `agents/security-reviewer.md` | 53 | 684 | Por invocação |
| **Demais** | — | — | — |
| `README.md` | 54 | 684 | Pré-adoção (público anglófono, ADR-012) |
| `docs/install.md` | 80 | 1.052 | Pós-adoção on-demand |
| `.claude-plugin/plugin.json` | 12 | 64 | Marketplace + roteador |
| `.claude-plugin/marketplace.json` | 31 | 96 | Marketplace (descoberta pré-adoção) |
| **Corpus runtime estimado** | **~1.752** | **~22.532** | — |

**Sinal auto-loaded forte:** `CLAUDE.md` (2.585 palavras) + descriptions de frontmatter de 8 skills + 5 agents (lidas pelo roteador da harness antes de qualquer invocação). Total auto-loaded por turn: ~3.000-3.500 palavras (CLAUDE.md + frontmatters somados).

**Descriptions de frontmatter — palavras por skill/agent (auto-loaded por roteador):**

| Skill / Agent | Palavras do `description` |
|---|---:|
| `/gen-tests` | 38 (lista stacks: Python + Java) |
| `/init-config` | 41 (descreve mecânica passo-a-passo) |
| `design-reviewer` | 71 (lista findings + escopo + dispatch automático + manual) |
| `security-reviewer` | 51 (lista contextos aplicáveis: web/CLI/desktop/...) |
| `doc-reviewer` | 43 |
| `code-reviewer` | 30 |
| `qa-reviewer` | 28 |
| `/run-plan` | 30 |
| `/triage` | 31 |
| `/release` | 27 |
| `/new-adr` | 22 |
| `/debug` | 26 |
| `/next` | 27 |

Total descriptions: ~465 palavras auto-loaded a cada turn de roteador. Topo da lista é `design-reviewer` (71); fundo é `/new-adr` (22) — 3× variação.

---

## 2. Diagnóstico por critério

### 2.1 Coesão & coerência interna/externa

**Forte.** Cada artefato tem foco. Cross-refs documentam coerência (ADR-019, ADR-011 invocados em pontos exatos).

**Pontos de atenção:**

- **(C1) `CLAUDE.md` mistura mecânica operacional com cicatrizes históricas.** Linha 23: *"From v1.11.0 onward, version bumps go through `/release` (dogfood)..."* — referência específica a versão num documento auto-loaded eternamente. Operador externo ou contribuidor futuro não precisa saber a história; relevante é o estado atual.
- **(C2) `CLAUDE.md` "Release cadence" parágrafo** (linhas 25-28, ~50 palavras) é doutrina operacional do mantenedor único, não instrução à agent. Defensiva contra prática observada uma vez; auto-loaded em todo turn.

### 2.2 Clareza & desambiguação

**Forte.** Tabelas em `/run-plan §0` (warnings), `/release §1` (sub-caminhos), `/gen-tests` (markers), `/triage §3` (escolher artefato), CLAUDE.md "Plugin component naming" — bem aplicadas.

**Pontos de atenção:**

- **(D1) `/run-plan §3.3` sanity check de docs** tem 3 condições de skip + critério de cutucada em **prosa contínua** (~15 linhas). Tri-state cabe em tabela `Condição | Skip silente? | Ação`.
- **(D2) `/triage` step 4 "BACKLOG (papel: `backlog`)"** subdivide em 3 casos (resolvido normal / "não temos" / modo local) em prosa de ~25 linhas. Tabela compactaria.

### 2.3 Alinhamento à `docs/philosophy.md`

**Forte.** "Cerimônia tática não" honrado.

**Pontos de atenção:**

- **(P1) Seção "Linguagem ubíqua na implementação"** descreve **pipeline operacional concreto** (`/triage` grava → `/run-plan` repassa → `code-reviewer` valida). Esse nível de detalhe **operacional** num arquivo de **princípio** mistura registros. Pipeline já vive nas próprias skills + ADR-019; `philosophy.md` deveria fixar só o princípio ("vocabulário registrado em domínio mas ausente em identificadores vira ornamento").

### 2.4 Inflação de tokens — input recorrente e por invocação

**Forte.** Volume controlado pós-onda de 2026-05-06.

**Pontos de atenção:**

- **(T1) `CLAUDE.md` próximo ao cap nominal (171/200).** Auto-loaded em todo turn. Cicatrizes específicas (C1, C2) + "Critério editorial" expandido (J3 abaixo) somam ~80 palavras compactáveis sem perda funcional.
- **(T2) Frontmatter `description` de `/gen-tests` lista stacks inline** ("Python (pytest + respx + tmp_path) e Java (JUnit 5 + Mockito + Maven)"). Cresce **O(stacks)**. Cada stack futura adiciona ~10 palavras ao routing payload, sem que o roteador precise da info para decidir invocação.
- **(T3) `description` de `design-reviewer` (71 palavras)** é maior que o do agent que ele invoca (`code-reviewer`, 30 palavras). Descreve findings + escopo + dispatch automático + manual — todos detalhes que pertencem ao corpo do agent, não ao routing payload.
- **(T4) `security-reviewer` description lista contextos aplicáveis** ("web, CLI, desktop, mobile, embedded, library, pipeline, IaC"). Stack-agnóstico já está dito; lista é exemplificação que infla payload.

### 2.5 Duplicação cross-artifact

- **(R1) Fórmula "Idioma do relatório: espelhar o idioma do projeto consumidor (ver 'Convenção de idioma' em `docs/philosophy.md`). Default canonical PT-BR."** aparece em **6 sites** com prosa quase idêntica (~25 palavras cada):
  - `agents/code-reviewer.md:69`, `qa-reviewer.md:51`, `security-reviewer.md:45`, `doc-reviewer.md:52`, `design-reviewer.md:67`, `skills/triage/SKILL.md:105`.
  - Único elemento variável: `code-reviewer` adiciona "rótulos abaixo traduzidos"; `design-reviewer` é mais curta. Os outros 4 são idênticos.
  - Custo agregado: ~125 palavras de duplicação textual.
- **(R2) Bloco da "Cutucada de descoberta"** em **4 SKILLs** + descrição completa em `CLAUDE.md`. Cada SKILL repete (i) o triple-gate em prosa (~5 linhas) e (ii) a string canonical literal:
  > "Dica: este projeto não declara o bloco `pragmatic-toolkit:config` no CLAUDE.md. Rode `/init-config` para configurar todos os papéis de uma vez."
  - ADR-017 § Alternativa (g) **explicitamente** aceitou a duplicação por YAGNI sobre helper. Mas custo cumulativo agregado é ~240 palavras em sites runtime. Skill nova com `roles.required` herda mais um site.
  - **Não-mecanismo:** aceitar como está (decisão ADR formalizada).
- **(R3) Referência à "Convenção de commits"** repetida com prosa similar em `/run-plan §2.5`, `/release §3/§3.5`, `/triage §6`, `/next §6`, `CLAUDE.md`. Cada uso é em contexto distinto (não pura duplicação) mas a frase "default canonical Conventional Commits em inglês" aparece ~5 vezes. Aceitável — cada SKILL precisa lembrar localmente.

### 2.6 Justificativas-cicatriz

- **(J1) `CLAUDE.md:23`** "**From v1.11.0 onward**, version bumps go through `/release` (dogfood). The skill resolves `version_files` from this repo's config to update **both** manifests, composes the `CHANGELOG.md` entry from the CC log since the last tag, commits and tags locally. Push remains manual." — cicatriz histórica (a frase "From v1.11.0 onward" indica resposta a uma transição específica). Conteúdo informativo é "Version bumps go through `/release`"; resto é histórico que polui o footprint.
- **(J2) `CLAUDE.md:25-28`** "Release cadence: accumulate merges in `main` and trigger `/release` when there's a coherent set to publish (feature complete, urgent fix, or a deliberate cadence drop) — not after every PR. The skill already groups commits since the last tag; bumping per-PR generates noisy changelog entries and version churn without proportionate value." — doutrina operacional defensiva contra prática observada (bumping per-PR). Mantenedor único; auto-loaded eternamente.
- **(J3) `CLAUDE.md:84`** "**Critério editorial:** lista apenas guardas que documentam anti-padrão não-óbvio. Item que apenas reafirma prosa anterior do skill é ruído — se sua remoção não confundiria um leitor razoável que leu o resto do skill, não pertence aqui. Itens vindos de incidentes ou de anti-padrões sutis (modelo tem viés de autoinvocação, gatilho condicional facilmente esquecido, exceção localizada que não é óbvia) são não-óbvios e devem permanecer." — 4 sentenças onde 2 bastariam. Critério editorial detalhado é cicatriz da própria onda v1.18.
- **(J4) `/init-config:12`** "Diferente das demais skills do toolkit, `/init-config` **não** consome roles via Resolution protocol — ela **define** o bloco que o protocol lê. Frontmatter sem `roles:` por design (per [ADR-003](...) § Schema, listas vazias podem ser omitidas). Cutucada de descoberta do [ADR-017](...) **não dispara dentro de `/init-config`**." — doutrina interna explicada na skill. Operador no momento da invocação não precisa saber por que outras skills consomem roles e essa não; pertence a ADR-017/ADR-003.

### 2.7 Frontmatter `description`

Foco no gatilho de invocação, não na descrição do output.

- **(F1) `/gen-tests`**: "Gera arquivo de teste para módulo, função ou descrição livre, com idioms da stack do projeto consumidor. **Stacks suportadas hoje, Python (pytest + respx + tmp_path) e Java (JUnit 5 + Mockito + Maven).** Use quando o operador pedir testes." — a lista entre asteriscos descreve estado de cobertura, não gatilho. Roteador não usa essa info para decidir invocar.
- **(F2) `/init-config`**: "Wizard de configuração inicial dos papéis do plugin no consumer — **pergunta cada role (canonical/local/null), detecta `test_command` stack-aware, grava o bloco `<!-- pragmatic-toolkit:config -->` no CLAUDE.md**. Use quando..." — passo-a-passo da mecânica no description. Roteador só precisa de "Wizard interativo para configurar o bloco config".
- **(F3) `design-reviewer`** (71 palavras): "...— **abstrações prematuras, alternativas ausentes, acoplamentos que travam mudança futura, ADR-worthiness não-formalizada, contradição com ADRs existentes ou docs/philosophy.md**. Stack-agnóstico — aplicável a qualquer projeto que mantenha ADRs e plano antes de implementar. **Acionado automaticamente em /triage que produz plano e em /new-adr (standalone ou delegada) per ADR-011**; manualmente via @design-reviewer para revisar planos/ADRs em outros pontos." — enumera findings + dispatch. Body do agent já cobre.
- **(F4) `security-reviewer`** (51 palavras): "Stack-agnóstico — **aplicável a qualquer tipo de sistema (web, CLI, desktop, mobile, embedded, library, pipeline, IaC)**." — lista exemplificativa que infla.

### 2.8 `## O que NÃO fazer`

Bem disciplinado em geral (onda de 2026-05-06 fez trim). Items que ainda merecem revisão:

- **(N1) `/run-plan` linha "Não executar push sem confirmação explícita via enum `Publicar`"** recapitula §3.7 ("Sugestão de publicação"). Se o operador não conhece o enum `Publicar`, leu §3.7. Borderline — registra como aviso anti-bypass; pode ficar.
- **(N2) `/init-config` linha "Não emitir cutucada de descoberta de ADR-017 dentro desta skill"** recapitula o preâmbulo (linha 12, já flagado em J4). Item duplica afirmação já feita no body.

---

## 3. Propostas

Cada proposta marca **escopo, redução estimada em palavras/tokens, sequenciamento por leverage**. Conversão palavra→token ~1.3× (corpus técnico/markdown).

### A. Compactar 3 cicatrizes históricas em `CLAUDE.md`

**Escopo:**
- Linha 23 + 86: remover "From v1.11.0 onward" — substituir por "Version bumps go through `/release` (dogfood) — resolves `version_files`, composes the `CHANGELOG.md` entry...". (-8 palavras)
- Linhas 25-28 "Release cadence" — comprimir 2 sentenças em 1: "Trigger `/release` when there's a coherent set to publish (feature complete, urgent fix, deliberate cadence drop); per-PR bumps generate changelog churn." (-25 palavras)
- Linha 84 "Critério editorial" — comprimir 4 sentenças em 2: manter "lista apenas guardas que documentam anti-padrão não-óbvio. Item que apenas reafirma prosa anterior é ruído." (-35 palavras)

**Redução:** ~68 palavras ≈ ~90 tokens, em arquivo **auto-loaded por turn**. Custo amortizado de cada turn na sessão.

**Sequenciamento:** maior leverage (auto-loaded). Executar primeiro.

### B. Consolidar fórmula "Idioma do relatório" em `CLAUDE.md` + referenciar nos 6 sites

**Escopo:** criar seção curta `## Reviewer/skill report idioma` em CLAUDE.md (~3 linhas com a regra + variantes), e em cada agent + `/triage` substituir o parágrafo de ~25 palavras por referência ("Idioma: per `CLAUDE.md` → 'Reviewer/skill report idioma'.").

**Redução:** 6 sites × ~20 palavras → 1 site × ~20 palavras + 6 × ~7 palavras (referência) = ~120 → ~62 palavras. Líquido **~58 palavras** removidas.

**Trade-off:** hub-and-spoke em mais um eixo. Precedente já estabelecido com "AskUserQuestion mechanics" e "Convenção de naming"; coerente com a doutrina "regra mecânica em CLAUDE.md, referência nos consumers".

**Sequenciamento:** médio leverage. Bom efeito cumulativo em 6 invocações de subagent.

### C. Encurtar 4 frontmatter `description` para gatilho puro

**Escopo:**

- **`/gen-tests`** (38 → ~20 palavras): remover lista de stacks. Manter "Gera arquivo de teste para módulo, função ou descrição livre, com idioms da stack do projeto consumidor. Use quando o operador pedir testes." Stacks suportadas vão para `# gen-tests` body (já existe a tabela de markers).
- **`/init-config`** (41 → ~22 palavras): "Wizard interativo para configurar o bloco `<!-- pragmatic-toolkit:config -->` no `CLAUDE.md`. Use quando o operador quer configurar o plugin de uma vez ou reconfigurar bloco existente."
- **`design-reviewer`** (71 → ~30 palavras): "Revisor de decisões arquiteturais e de design em documento pré-fato (plano ou ADR draft). Acionado automaticamente em `/triage` que produz plano e em `/new-adr`; manualmente via `@design-reviewer`. Stack-agnóstico." Lista de findings volta para `## O que flagrar` do próprio agent (já existe).
- **`security-reviewer`** (51 → ~30 palavras): remover lista de sistemas aplicáveis ("web, CLI, desktop, mobile, embedded, library, pipeline, IaC"). Stack-agnóstico já está dito; a lista é exemplificativa.

**Redução:** ~99 palavras nos descriptions ≈ ~130 tokens. **Auto-loaded por roteador** a cada turn.

**Sequenciamento:** alto leverage (auto-loaded por roteador), risco zero (descriptions são tags de invocação).

### D. Migrar "Linguagem ubíqua na implementação" de `philosophy.md` para princípio puro

**Escopo:** seção atual (3 frases descrevendo pipeline operacional `/triage` → `/run-plan` → `code-reviewer`) substituída por 1-2 frases de princípio: "Vocabulário registrado em `ubiquitous_language` mas ausente nos identificadores produzidos vira ornamento de alinhamento — exatamente o que a frase-tese rejeita. Pipeline operacional vive em skills/agents; aqui só o princípio."

**Redução:** ~30 palavras em `philosophy.md`. Maior valor: alinhamento de eixos (princípio em philosophy, operacional em skills/CLAUDE.md). Sustenta a onda anterior de refactor ("philosophy.md: refatorar para conter apenas princípios").

**Sequenciamento:** médio leverage, alinha doutrina.

### E. Trocar prosa por tabela em `/run-plan §3.3` (sanity check de docs)

**Escopo:** as 3 condições de skip + a cutucada viram tabela:

```
| Condição | Skip silente? | Ação |
|---|---|---|
| Plano lista `.md` user-facing + diff toca | sim | — |
| `## Resumo da mudança` sem superfície user-facing | sim | — |
| Grep de identificadores tocados retorna vazio | sim (empírico) | — |
| Caso contrário | não | Cutucar enum `Docs` (Consistente / Listar) com referrers concretos |
```

**Redução:** ~5-8 linhas líquidas; ganho principal é **legibilidade em uma passada**.

**Sequenciamento:** baixo leverage de tokens, mas alto valor de clareza.

### F. Compactar preâmbulo de `/init-config`

**Escopo:** linha 12 ("Diferente das demais skills do toolkit, `/init-config` **não** consome roles via Resolution protocol — ela **define** o bloco...") movida em parte para ADR-017 ou ADR-003 (já existem). Skill mantém só 1 frase: "Frontmatter sem `roles:` por design — `/init-config` define o bloco, não consome."

**Redução:** ~30 palavras na skill.

**Sequenciamento:** baixo leverage isolado, mas é cicatriz auto-explicativa removível.

### G. Remover `## O que NÃO fazer` items que recapitulam body

**Escopo:**
- `/init-config`: remover "Não emitir cutucada de descoberta de ADR-017 dentro desta skill" (J4 + N2 redundantes). Restante mantém — todos não-óbvios.
- `/run-plan`: **manter** "Não executar push sem confirmação explícita via enum `Publicar`" — borderline mas registra anti-bypass; benefício do duplo registro supera o ruído.

**Redução:** ~12 palavras + 1 bullet em `/init-config`.

**Sequenciamento:** baixo leverage; valor é manter a régua editorial do `## O que NÃO fazer` afiada.

### Sobreposição com `2026-05-12-architecture-logic.md`

A auditoria companion já propôs reduções estruturais que **também** cortam prosa. Não há conflito; bundles possíveis:

| Audit-arch | Sobreposição prose-tokens | Redução adicional |
|---|---|---|
| **F_arch** (reposicionar passo 5 do /triage como sub-fluxo do passo 4) | Remove cabeçalho de passo + transição (~50 palavras) | Soma com B/D desta auditoria. |
| **G_arch** (extrair cleanup pós-merge para `templates/cleanup-pos-merge.md`) | Remove ~30 linhas detalhadas de `/triage §0` (~200 palavras) | **Grande**: maior redução pontual no maior SKILL. |
| **D_arch** (estender forge bilateral ao /triage §0) | Adiciona ~5 linhas ao /triage §0 | Anula parte da redução G_arch se executado isolado. |

**Recomendação de sequenciamento cruzado:** se G_arch entrar, ganho de prosa supera o custo de D_arch sobreposto.

---

## 4. Sequenciamento sugerido — leverage por turn

Ordenado por **palavras economizadas × frequência de carregamento**:

### Alta frequência (auto-loaded por turn)

1. **C (encurtar 4 descriptions)** — ~99 palavras / ~130 tokens. Auto-loaded por roteador.
2. **A (cicatrizes CLAUDE.md)** — ~68 palavras / ~90 tokens. Auto-loaded.

**Subtotal alta frequência:** ~167 palavras / ~220 tokens economizados em **cada turn**.

### Média frequência (por invocação)

3. **B (consolidar idioma do relatório)** — ~58 palavras. Toca 6 sites; ganho cumulativo a cada subagent.
4. **D (princípio puro em philosophy.md)** — ~30 palavras. Carregado por skills que cross-referenciam.

### Baixa frequência / clareza

5. **F (preâmbulo /init-config)** — ~30 palavras.
6. **G (`## O que NÃO fazer` redundante)** — ~12 palavras + 1 bullet.
7. **E (tabela em /run-plan §3.3)** — clareza > redução.

### Total estimado

~370 palavras ≈ ~480 tokens removidos do corpus runtime (~22.500 palavras → ~22.130 = **redução ~1.6%**). Quantidade modesta porque a onda de 2026-05-06 já compactou amplamente. Valor: focado em **cicatriz residual** e **auto-loaded payload**.

---

## Encaminhamento

Cada proposta entra pelo fluxo padrão: `/triage <proposta>` decide artefato (linha de backlog, plano, ADR, atualização cirúrgica).

**Sugestões de encaminhamento por proposta:**

- A, C, F, G → linha de backlog (mudanças cirúrgicas em prosa).
- B → linha de backlog (precedente AskUserQuestion mechanics; criar nova seção em CLAUDE.md + edit em 6 sites é multi-arquivo mas plano simples).
- D → linha de backlog + edit cirúrgico de `philosophy.md` (alinha com gatilho previamente registrado de "philosophy.md = só princípios").
- E → linha de backlog (refactor editorial em /run-plan).

**Bundling útil:**
- **A + C** num único PR — ambos atacam auto-loaded payload, complementares.
- **F + G** num único PR — ambos retoques em /init-config.
- **B + D** num único PR — ambos sobre eixo "doutrina em hub-and-spoke".

**Bundling com `2026-05-12-architecture-logic.md`:**
- Propostas F_arch + G_arch (audit-arch) podem rodar antes desta auditoria — eliminam parte do volume que aqui auditamos. Re-rodar prose-tokens após F_arch/G_arch refinaria os alvos.
