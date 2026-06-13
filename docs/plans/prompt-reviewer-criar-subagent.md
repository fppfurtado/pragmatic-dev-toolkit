# Plano — Criar subagent reviewer `prompt-reviewer`

## Contexto

Substância capturada em sessão CC `prompts` do `h3-finance-agent` (2026-06-13): em projetos agentic, inconsistências de algoritmo em prompts (passos conflitantes, vagos, ambíguos, contraditórios) tornam a resposta do modelo imprecisa/imprevisível. Classe nomeável, recorrente, e ortogonal aos 5 reviewers existentes (`code/design/qa/security/doc-reviewer`) — nenhum cobre o eixo "consistência interna do algoritmo prompt-como-instrução-ao-agente".

Decisão de promoção direta (vs incubação local no `h3-finance-agent`): operador articulou o gap como classe nomeável com substância universal stack-agnóstica, e formalmente requisitou Override do critério N=3 (ADR-043 § Ockham operacionalizado #4) análogo aos precedentes ADR-057 e ADR-061. Ambos os precedentes registraram override com gatilho de revisão concreto pós-shipping (cenário de reversão nomeável + janela temporal).

Decisões de design resolvidas no `/triage` upstream (2026-06-13):

- **Nome canonical:** `prompt-reviewer` (pattern `<noun>-reviewer` paralelo aos 5 existentes).
- **Escopo v1 do auto-trigger:** paths `agents/*.md`, `skills/**/SKILL.md`, e `docs/plans/*.md`. Strings de prompt embutidas em código (`.py`, `.ts` etc.) ficam para v2 — escopo reaberto via gatilho registrado no ADR.
- **Pattern de dispatch:** `prompt-reviewer` substitui `doc-reviewer` como default para os paths do escopo v1. Resto do `.md` (README, ADRs, philosophy.md, CLAUDE.md, BACKLOG.md) preserva `doc-reviewer` como default. Default mais específico vence.

Precedente histórico endereçado: ADR-035 (Substituído por ADR-043) absorveu plano `v1.8-cenarios-validacao-manual.md` rejeitando `prompt-reviewer` por YAGNI reflexo interno. ADR-043 inverteu a hierarquia doutrinal — YAGNI consumer ≠ filtro autoaplicado a decisões internas do plugin; critério interno é Ockham operacionalizado (4 critérios; ≥1 basta). Critério 2 (fronteira doutrinal borrada — "qualidade algorítmica de prompts" não cabe em nenhum dos 5 reviewers existentes) aplica concretamente; critério 4 (≥3 instâncias ad hoc) recebe Override registrado paralelo a ADR-057/ADR-061.

**ADRs candidatos:** ADR-057 (precedente direto de override N=3 + categoria nova de skill editorial), ADR-061 (precedente direto de override N=3 + sucessor parcial lateral), ADR-050 (componentes plugin — naming canonical de agents stack-agnósticos + critério `disable-model-invocation`).

**Linha do backlog:** plugin: novo subagent reviewer `prompt-reviewer` — detecção semântica de inconsistências de algoritmo em prompts (passos conflitantes, vagos, ambíguos, contraditórios) que tornam resposta do modelo imprecisa/imprevisível. Classe recorrente em projetos agentic, capturada empiricamente em sessão CC `prompts` do `h3-finance-agent` (2026-06-13). Substância semântica per ADR-011 § "Skill = pensamento" do meta-system: skill markdown, não MCP/CLI. Forma técnica: subagent reviewer paralelo aos 5 existentes (`code-reviewer`/`design-reviewer`/`qa-reviewer`/`doc-reviewer`/`security-reviewer`). Auto-trigger natural em diff que toca `SKILL.md`/`agents/*.md`; invocação manual `@prompt-reviewer` para strings de prompt em código (escopo v2 a discutir no /triage). Stack-agnóstico (qualquer prompt em qualquer harness). Decisão de promoção direta (vs incubação local no h3-finance-agent): operador articulou gap como classe nomeável, substância universal suficiente — override do critério N=3 (ADR-043 § Ockham operacionalizado #4) análogo aos precedentes ADR-057/ADR-061. Decisões pendentes pro `/triage` aqui: nome canonical, checklist de heurísticas, auto-trigger scope, template de output paralelo aos reviewers existentes. Origem do gap: sessão CC `prompts` do h3-finance-agent (2026-06-13).

## Resumo da mudança

Cria-se o 6º reviewer do plugin (`agents/prompt-reviewer.md`) com escopo de qualidade algorítmica de prompts markdown. Wiring de dispatch em `CLAUDE.md` registra paths sob default automático novo, mantendo `doc-reviewer` para o resto. ADR delegada via `/new-adr` codifica a decisão estrutural, Override do critério N=3 registrado com gatilho de revisão concreto, e endereçamento do precedente histórico ADR-035.

Escopo v1 fora: análise de strings de prompt embutidas em código (`.py`, `.ts` etc.); auto-trigger via hook; checklist refinada além das 4 heurísticas seed.

## Arquivos a alterar

### Bloco 1 — Agent file canonical {reviewer: code}

- `agents/prompt-reviewer.md`: novo arquivo seguindo o pattern de `agents/code-reviewer.md` e `agents/design-reviewer.md`.
  - Frontmatter `name: prompt-reviewer` + `description:` com gatilho de acionamento (auto-trigger por path + invocação manual).
  - Prosa de abertura: "Você é um revisor de **qualidade algorítmica de prompts markdown**" + escopo (SKILL.md / agents/*.md / docs/plans/*.md).
  - Diferença operacional vs reviewers existentes (eixo prompt-como-instrução-ao-agente, não código nem doutrina).
  - `## O que flagrar` com 4 sub-headings canonical (4 heurísticas seed do BACKLOG):
    - **Passos conflitantes** — passo N afirma A, passo M afirma ¬A; condições mutuamente exclusivas no mesmo gate.
    - **Passos vagos** — instrução sem gatilho concreto, ação implícita ("considere", "avalie" sem critério mecânico).
    - **Passos ambíguos** — múltiplas interpretações válidas para o mesmo passo; ordem de operações implícita.
    - **Passos contraditórios em estado global** — passo K mantém invariante, passo L viola sem reconhecer.
  - `## O que NÃO flagrar` — sub-bullets canonical seguindo pattern de code/design-reviewer (estilo de prosa, decisão tática reversível, escolha cosmética de ordem).
  - `## Como reportar` — template 4-field (Localização / Problema / Heurística violada / Sugestão), idioma per `CLAUDE.md` → 'Reviewer/skill report idioma', close-clean wording paralelo aos existentes ("Prompt alinhado — nenhuma inconsistência algorítmica.").

> **Nota de reviewer**: o bloco contém o novo agent.md mas o `prompt-reviewer` ainda não existe na invocação de `/run-plan`. `code-reviewer` é default explícito aqui — não passar via `doc-reviewer` default automático para o bloco pois o arquivo é a especificação do próprio agente (eixo qualidade-de-prompt aplica-se reflexivamente; `code-reviewer` cobre como rubrica genérica YAGNI/anti-padrão).

### Bloco 2 — Wiring em `CLAUDE.md` + `skills/run-plan/SKILL.md` {reviewer: doc}

- `CLAUDE.md`: 3 edits cirúrgicos.
  - Linha ~16 (`Agents — agents/<name>.md ...`): atualizar inventário "Five reviewers shipped" → "Six reviewers shipped" + adicionar `prompt-reviewer` à enumeração.
  - Linha ~44 (tabela "(agents shipped by the plugin)"): adicionar `prompt-reviewer` à lista com descrição curta do escopo v1.
  - Linha ~119 ("Reviewer/skill report idioma"): adicionar `prompt-reviewer` à lista dos 5 reviewers shippados (5 → 6).
  - Linha ~129 (tabela Agent naming): adicionar `prompt-reviewer` à enumeração.
  - Bullet novo em `## Editing conventions` cross-ref ao ADR-062 (paralelo aos bullets de ADR-010/-011/-023/-026/-034/-043/-046/-049/-050/-053/-057/-061): "**Reviewer `prompt-reviewer`**: 6º reviewer paralelo aos 5 shippados; auto-trigger nos paths `agents/*.md`/`skills/**/SKILL.md`/`docs/plans/*.md` substituindo `doc-reviewer` como default neles per [ADR-062](docs/decisions/ADR-062-criar-subagent-prompt-reviewer.md); resto do `.md` preserva `doc-reviewer`. Regra de dispatch path-set extendida em `skills/run-plan/SKILL.md:129`. Override do critério N=3 (ADR-043 § Ockham operacionalizado #4) registrado análogo aos precedentes ADR-057/ADR-061; fronteira prompt-reviewer ↔ design-reviewer em `docs/plans/*.md` codificada em ADR-062 § Decisão § Fronteira."
- `skills/run-plan/SKILL.md` linha 129 (dispatch logic): extender a regra atual "Sem anotação → default code-reviewer. Exceção: paths do bloco não-vazios e todos com extensão .md/.rst/.txt → default vira doc-reviewer" para incluir a exceção doc-only narrow (paths em `agents/*.md` ∪ `skills/**/SKILL.md` ∪ `docs/plans/*.md` → default vira `prompt-reviewer`). Texto literal sugerido per ADR-062 § Pattern de dispatch (hierarquia 3-nível com `prompt-reviewer` como exceção narrow, `doc-reviewer` como exceção ampla).

ADR já criado upstream via `/new-adr` no `/triage`; não vira bloco do plano (precedente em `curate-backlog.md` linha 39 + ADR-057). `/run-plan` parte direto da criação do agent + wiring.

## Verificação end-to-end

Inspeção textual passo-a-passo (papel `test_command` resolvido como `null` no `<!-- pragmatic-toolkit:config -->` deste repo — sem suite automatizada per ADR-050 § Decisão (b)):

1. `ls agents/prompt-reviewer.md` retorna o arquivo criado.
2. `head -4 agents/prompt-reviewer.md` mostra frontmatter `name: prompt-reviewer` + `description:` no pattern dos demais reviewers.
3. `grep -n "prompt-reviewer" CLAUDE.md` retorna ≥3 matches (inventário Agents, lista de reviewer idioma, bullet Editing conventions cross-ref ao ADR).
4. `grep -n "prompt-reviewer\|agents/\*\.md\|SKILL\.md" skills/run-plan/SKILL.md` retorna match na linha 129 (dispatch logic extendida).
5. `git status --porcelain` mostra apenas os 3 arquivos modificados/criados (`agents/prompt-reviewer.md`, `CLAUDE.md`, `skills/run-plan/SKILL.md`) e nada mais.

## Verificação manual

Smoke-test do agent em invocação manual:

1. Selecionar prompt-target real do plugin com candidato a inconsistência conhecida (sugestão: `skills/triage/SKILL.md` passo 2 — checklist mental com 8 bullets de "gaps reais" + ordem implícita).
2. Invocar `@prompt-reviewer <path>` em sessão CC nova.
3. Validar: agent retorna findings categorizados nas 4 heurísticas (passos conflitantes/vagos/ambíguos/contraditórios) ou close-clean wording explícito.
4. Validar: findings carregam template 4-field; sem narrativa solta.
5. Validar: nenhum finding sobrepõe escopo de `code-reviewer` (YAGNI/abstração) ou `doc-reviewer` (drift doc-código).

Surface não-determinística (LLM judging prompts) — re-rodar smoke-test 2× se primeira passagem não converge nas 4 heurísticas, e flagrar drift para refinamento.

## Notas operacionais

- **Ordem dos blocos importa.** Bloco 1 (agent file) precede Bloco 2 (wiring `CLAUDE.md` + `skills/run-plan/SKILL.md`). Wiring sem agent file = referência morta; dispatch logic estendida sem agent file = invocação de agent inexistente.
- **Reviewer per bloco:**
  - Bloco 1: `code-reviewer` (override do default doc-reviewer doc-only) — meta-circular justificado em nota inline; o próprio agente ainda não existe na invocação.
  - Bloco 2: `doc-reviewer` (override do default que seria `prompt-reviewer` na resolução de paths mistos — `CLAUDE.md` fora do escopo + `skills/run-plan/SKILL.md` no escopo; anotação explícita evita ambiguidade enquanto a regra está sendo aplicada no próprio bloco). Pós-merge deste plano, edits subsequentes a `skills/run-plan/SKILL.md` em outros PRs cairão sob `prompt-reviewer` default.
- **ADR-062 já em disco.** Bloco 2 referencia ADR-062 já criado upstream via `/new-adr` no `/triage`. Commit unificado plano + ADR.
- **Push pós-merge dos blocos.** Plano canonical em `main` cwd; `/run-plan` cria worktree própria + branch `prompt-reviewer-criar-subagent`. PR review esperado.

## Decisões absorvidas

- ADR-062 § Override do critério N=3: Reconhecimento de assimetria com precedentes ADR-057/-061 adicionado; peso primário recai sobre critério 2 (fronteira), não sobre critério 1 (recorrência) (caminho-único).
- ADR-062 § Contexto + § Consequências Benefícios: parágrafo "Precedente histórico endereçado" compactado para 1 linha; benefício "rastreabilidade epistêmica via ADR-035" removido — substância preserva-se em § Origem sem cerimônia (caminho-único).
- ADR-062 § Trade-offs: contagem "4ª aplicação de pattern editorial" corrigida para "3ª aplicação consecutiva em categoria doutrinal de Override N=3 (ADR-057→-061→-062, cadência <4 dias)"; nota explícita de que contadores editoriais de memory `feedback_editorial_patterns_emergentes` são categoria distinta (caminho-único).
- ADR-062 § Auto-aplicação: seções duplicadas "## Auto-aplicação per ADR-034" + "## Auto-aplicação coerente" unificadas em "## Auto-aplicação" com sub-headers per ADR-034 + per ADR-043 § Ockham operacionalizado (pattern editorial paralelo a ADR-053 § Auto-aplicação) (caminho-único).
- ADR-062 § Alternativas: alternativa (f) "Incubação local no h3-finance-agent antes de promoção ao toolkit" adicionada com rebut honesto — bifurcação nomeada no BACKLOG original passou a ter cobertura formal em § Alternativas (caminho-único).
