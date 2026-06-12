# Plano — Batch 2: refactor de fronteira documental

## Contexto

Continuação do roteiro arquitetural pós-v1.20.0. v1.18.0 anunciou "philosophy.md princípios apenas" e cortou paráfrases em CLAUDE.md, mas o refactor ficou parcial: papéis ainda duplicados entre os dois arquivos, mecânica residual em philosophy.md, e o agente mais invocado (`code-reviewer`) traz subseções genéricas que viram ruído quando o diff é só código de aplicação. Eixo do batch: **redistribuir mecânica entre `philosophy.md` / `CLAUDE.md` / agents** mantendo single source of truth por tipo de conteúdo (princípio vs mecânica vs critério de revisor).

**Linha do backlog:** plugin: batch 2 de refactor de fronteira documental — A1 desduplica papéis philosophy.md ↔ CLAUDE.md, A2 continua mecânica residual de philosophy.md para consumers, B1 declara aplicabilidade condicional em code-reviewer settings.json/infra

**Bifurcação resolvida (B1):** caminho (a) conservador — aplicabilidade condicional inline no `code-reviewer`, sem extrair para agente dedicado. Trade-off: reduz ruído sem fragmentar; alinha com D1 do batch 1 (single-reviewer como caso normal). Caminho (b) — extração para `agents/settings-reviewer.md` — descartado por inverter o eixo D1.

## Resumo da mudança

Três eixos:

- **A1 — desduplica listagem de papéis.** `docs/philosophy.md` "Path contract" tem tabela completa (papel + default + descrição); `CLAUDE.md` "The role contract" tem o mesmo conteúdo no parágrafo "Roles and canonical defaults". Decisão: **CLAUDE.md vira fonte completa** (always-loaded; agente precisa dos defaults em runtime para resolver papéis). **philosophy.md fica conceitual** — descreve "papéis, não paths" como princípio e remete à tabela em CLAUDE.md, sem replicar defaults.

- **A2 — mecânica residual de philosophy.md → consumers.** Três subseções com mistura princípio+mecânica:
  - **(i) "Convenção de naming"** — tabela de naming (skill/agent/hook) + 3 camadas de auto-gating de hooks são mecânica de design para quem cria componentes deste plugin. Mover para `CLAUDE.md` "Editing conventions" (este repo é plugin; install.md é consumer-facing — não cabe lá). philosophy.md retém o princípio compacto: "skill/agent stack-specific carrega sufixo; hooks auto-gated em todo projeto que tenha o plugin".
  - **(ii) "Convenção de pergunta ao operador"** — princípio (modo certo p/ resposta certa, "não perguntar por valor único derivado") fica em philosophy.md; mecânica concreta (`header ≤12 chars`, 2-4 opções, modo enum/prosa por tipo de resposta) move para CLAUDE.md.
  - **(iii) "Linguagem ubíqua na implementação"** — princípio (linguagem ubíqua deve chegar ao código) fica em philosophy.md; pipeline de 3 estágios (/triage extrai → /run-plan repassa → code-reviewer valida) move para os consumidores que executam — cada SKILL/agent que participa absorve o trecho relevante. CLAUDE.md ganha a forma agregada como referência cruzada.

- **B1 — aplicabilidade condicional no `code-reviewer`.** Subseções "Infra e configuração" (linhas 45-47) e ".claude/settings.json" (linhas 49-54) ficam inline no agente, mas declaram explicitamente "Acionar só se o diff toca <superfície>" no topo de cada uma. Reduz ruído quando o diff é só código de aplicação (caso comum) sem fragmentar em agente novo.

Refactor sem mudança de comportamento — redistribui texto entre arquivos para single source of truth e reduz ruído de input recorrente. Sem CLI/flag/env nova, sem integração nova.

## Arquivos a alterar

### Bloco 1 — A1: CLAUDE.md absorve fonte de papéis; philosophy.md fica conceitual {reviewer: code,doc}

- `CLAUDE.md` — seção "The role contract" (linha 31):
  - Substituir o parágrafo único "Roles and canonical defaults: ..." por tabela completa (papel | default | descrição compacta), espelhando o que está em philosophy.md hoje.
  - Manter "Resolution protocol" e "Required vs informational roles" — já estão no escopo certo.
  - Adicionar nota: "Princípios sobre o conceito de papéis (vs paths literais) em `docs/philosophy.md` → 'Path contract'."

- `docs/philosophy.md` — seção "Path contract" (linhas ~21-39):
  - Remover a tabela completa. Manter parágrafo conceitual: "papéis, não paths literais — projeto declara variantes uma vez via bloco de config."
  - Adicionar pointer: "Tabela canônica (papel | default | descrição) em `CLAUDE.md` → 'The role contract'."
  - Manter o parágrafo final mencionando scaffold-kit.

### Bloco 2 — A2: mecânica residual de philosophy.md migrada {reviewer: code,doc}

A2 toca 3 arquivos com referências cruzadas sensíveis. Operações por subseção:

- **A2(i) Naming:**
  - `docs/philosophy.md` "Convenção de naming" (linhas ~41-61): substituir tabela de naming + 3 camadas de auto-gating por princípio compacto (~3 linhas): "componentes que geram/executam stack carregam sufixo; hooks auto-gated triplo (extensão → marker → toolchain) para shipar safely num plugin multi-stack". Pointer para CLAUDE.md.
  - `CLAUDE.md` "Editing conventions": adicionar item "Plugin component naming and hook auto-gating" com a tabela de naming e as 3 camadas de auto-gating na íntegra.

- **A2(ii) Pergunta ao operador:**
  - `docs/philosophy.md` "Convenção de pergunta ao operador" (linhas ~83-90): manter o princípio dos dois modos (enum vs prosa) e o parágrafo "Não perguntar por valor único derivado". Remover detalhes mecânicos (`header ≤12 chars`, "2-4 opções", "Other automático", `multiSelect: true`).
  - `CLAUDE.md`: adicionar seção "AskUserQuestion mechanics" sob "The role contract" com a parte mecânica: limites de header, contagem de opções, modos por tipo de resposta, exemplos.

- **A2(iii) Linguagem ubíqua na implementação:**
  - `docs/philosophy.md` "Linguagem ubíqua na implementação" (linhas ~92-102): manter o parágrafo de princípio (vocabulário registrado deve chegar ao código). Remover o detalhamento do pipeline de 3 estágios.
  - `CLAUDE.md`: nota cruzada — "Pipeline de implementação de linguagem ubíqua: cada skill participante (`/triage`, `/run-plan`) e o `code-reviewer` documentam o passo que executam."
  - Verificar se as descrições do pipeline já estão presentes em `skills/triage/SKILL.md`, `skills/run-plan/SKILL.md` e `agents/code-reviewer.md`. Se sim (provável após v1.18.0), só remover de philosophy.md. Se não, completar nos consumidores ANTES de remover de philosophy.md (preserva conhecimento).

### Bloco 3 — B1: aplicabilidade condicional no code-reviewer {reviewer: code}

- `agents/code-reviewer.md` — subseção "Infra e configuração" (linhas ~45-47):
  - Adicionar prefixo declarativo: `**Aplicabilidade:** acionar apenas quando o diff toca `docker-compose*.yml`, `.env.example`, ou READMEs de infra. Diff de código de aplicação puro → pular esta subseção.`

- `agents/code-reviewer.md` — subseção ".claude/settings.json e .claude/settings.local.json" (linhas ~49-54):
  - Adicionar prefixo declarativo: `**Aplicabilidade:** acionar apenas quando o diff toca `.claude/settings.json`, `.claude/settings.local.json`, ou referências a estes arquivos. Diff fora desse escopo → pular esta subseção.`

- (Opcional) Verificar se outras subseções do code-reviewer mereceriam aplicabilidade explícita (ex.: "Identificadores" só faz sentido se há identificadores novos no diff). Critério: declarar aplicabilidade quando a subseção tem **superfície específica** que o diff pode não tocar; subseções universais (YAGNI, comentários, defensividade) não precisam.

## Verificação end-to-end

Refactor textual sem suite executável; gate é inspeção dirigida:

1. **A1 — desduplica papéis:**
   - `grep -c "IDEA.md\|docs/domain.md\|docs/design.md\|docs/decisions/\|docs/plans/" CLAUDE.md` mostra todos os defaults presentes uma vez.
   - `grep -c "IDEA.md\|docs/domain.md" docs/philosophy.md` retorna 0 ou 1 (apenas pointer/exemplo).
   - philosophy.md mantém "Path contract" como conceito; aponta para CLAUDE.md.

2. **A2 — mecânica residual migrada:**
   - philosophy.md word count cai significativamente (esperado: -300 a -500 palavras).
   - CLAUDE.md ganha as seções "Plugin component naming and hook auto-gating" e "AskUserQuestion mechanics" com o conteúdo migrado.
   - Pipeline de linguagem ubíqua: passos confirmados em `skills/triage/SKILL.md`, `skills/run-plan/SKILL.md`, `agents/code-reviewer.md`. philosophy.md tem só o princípio.

3. **B1 — aplicabilidade condicional:**
   - `grep -B1 "Aplicabilidade:" agents/code-reviewer.md` retorna as duas subseções (Infra, settings.json) com a declaração.
   - Subseções universais (YAGNI, comentários, defensividade, backwards-compat) seguem sem `Aplicabilidade:` — não merecem.

4. **Cross-cutting (referências quebradas):**
   - `grep -rn "philosophy.md.*Path contract\|philosophy.md.*Convenção de naming\|philosophy.md.*Convenção de pergunta\|philosophy.md.*Linguagem ubíqua" --include="*.md" .` — confirmar que pointers em skills/agents/CHANGELOG não ficaram apontando para seções movidas. Atualizar onde necessário.
