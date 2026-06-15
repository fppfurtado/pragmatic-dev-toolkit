---
name: triage
description: Alinha intenção e decide artefato (backlog, plano, ADR, atualização de domain/design) antes de implementar. Use quando o operador propuser mudança não-trivial sem plano ou linha de backlog.
disable-model-invocation: false
roles:
  informational: [plans_dir, backlog, ubiquitous_language, design_notes, decisions_dir, product_direction]
---

# triage

Workflow de **alinhamento prévio** para mudança não-trivial — feature, fix com plano (saída de `/debug`), refactor com bifurcação, alteração que toca invariante. Produz artefato de alinhamento (linha de backlog, plano, ADR, atualização de `docs/domain.md`/`docs/design.md`) e devolve controle.

## Sub-fluxo de criação canonical

Quando o passo 3 escolher "atualizar `ubiquitous_language`/`design_notes`" e o papel resolveu "não temos": propor criação no path canonical via enum (`Criar em <path>` / `Não usamos esse papel`). Segunda opção registra `paths.<role>: null` (oferta única de memorização). Mesmo mecanismo para `backlog` quando o passo 4 vai gravar linha (`Criar em BACKLOG.md` / `Não usamos esse papel`; segunda registra `paths.backlog: null`), e para `plans_dir` quando o passo 3 escolhe "plano" e o papel resolveu "não temos" (`Criar em docs/plans/` / `Não usamos esse papel`; segunda registra `paths.plans_dir: null`).

**Modo local** (`paths.<role>: local` declarado): skill cria/lê em `.claude/local/<role>/` em vez de path canonical, sem disparar enum de criação. Mecânica de inicialização (`mkdir`, probe gitignore, gate `Gitignore`) coberta pela seção "Local mode" do CLAUDE.md.

## Argumentos

Intenção em linguagem natural — frase curta (`/triage exportar movimentos em CSV`), descrição com contexto, ou vaga. Input vazio ou genericamente "o que vamos fazer hoje?" → seguir `skills/next/SKILL.md`.

## Passos

### 0. Cleanup pós-merge

Antes de carregar contexto, executar passo de cleanup pós-merge conforme `${CLAUDE_PLUGIN_ROOT}/docs/procedures/cleanup-pos-merge.md`. Skip silente se nada a limpar.

### 1. Carregar contexto mínimo

Ler **só o que o pedido tocar**, nesta ordem:

1. `product_direction` — alinhamento à direção de produto.
2. `ubiquitous_language` — bounded contexts, agregados/entidades, RNxx tocadas.
3. `backlog` — verificar item equivalente em **Próximos** ou **Concluídos**. Se existir, parar e reportar. (Sob ADR-049 § Decisão (a), "em andamento" é state em git/forge; se a intenção corresponde a branch/worktree já em curso, `/run-plan` precondição 4 bloqueia ao tentar criar worktree com slug colidente.)
4. `design_notes` — só se a feature toca uma das integrações listadas.
5. `decisions_dir` — listar ADRs relacionados; ler na íntegra apenas os que o pedido contradiz/estende.
6. `.claude/local/NOTES.md` — se existir, ler na íntegra como contexto suplementar (store non-role per [ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (a); informational, nunca bloqueia). Notas recentes mencionando trabalho em curso ou observações operacionais podem informar decisão de artefato e gap clarification. Reportar no relato do step 1 se uma nota influenciou a leitura do pedido, ou explicitamente que o store estava presente sem material adjacente. Ausente → skip silente.

Não ler código aqui — é alinhamento de intenção, não design técnico.

**Pre-condição cross-mode ([ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md)).** Após resolver `backlog` e `plans_dir`, se a combinação for `backlog` em modo `local` AND `plans_dir` em modo canonical, parar com mensagem:

> Combinação `backlog: local + plans_dir: canonical` recusada (ADR-047). `**Linha do backlog:**` viraria mensageiro de texto privado para plano público — semanticamente incoerente. Rode `/init-config` para corrigir o bloco config antes de continuar com `/triage`. Combinações suportadas: `ambos canonical`, `ambos local`, `backlog canonical + plans_dir local`.

Demais combinações seguem normalmente.

### 2. Esclarecer gaps com o usuário

Identificar lacunas e perguntar **só o que for bloqueante**. Checklist mental (não questionário):

- **Intenção vaga demais para triar:** input é abordagem aberta sem critério operacional de sucesso (verbos abstratos "melhorar", "modernizar", "aprimorar", "otimizar" sem métrica/cenário; objeto-direto da mudança ausente)? Não é gap pontual — é sinal de que a intenção ainda não cristalizou. Cutucar em **prosa** (não enum): "essa frase descreve abordagem aberta, sem critério operacional — quer explorar comigo aqui antes de eu triar, ou tem objeto/critério mais firme?". Aceita resposta livre; operador conversa raw, refina, volta para `/triage` com intenção cristalizada (per [ADR-036](../../docs/decisions/ADR-036-brainstorm-intencionalmente-nao-codificado-em-skill.md)). Fronteira com **Bifurcação arquitetural** abaixo: bifurcação pressupõe intenção formada com 2 caminhos competindo (critério claro, múltiplos caminhos); aqui o critério ainda não existe.
- **Escopo:** o que entra e o que fica de fora? Há caso menor que resolve 80%? Se não cabe em escopo menor, considerar bullet **Tamanho/decomposição** abaixo (pode ser ≥2 planos coordenados).
- **Tamanho / decomposição:** feature potencialmente grande demais para um único plano? Heurística qualitativa: operador consegue listar ≥3 facetas semanticamente independentes na descrição da intenção (cada faceta seria objeto natural de seu próprio plano)? Se sim, cutucar via `AskUserQuestion` (header `Decomposição`, opções `Enumerar facetas como planos separados` / `Manter como plano único`; Other livre para variantes). Consecução por resposta: `Enumerar` → operador descreve facetas em prosa pós-resposta, cada faceta vira `/triage` futuro isolado; `Manter como plano único` → segue para passo 3 com escopo intacto (escolha consciente de aceitar o tamanho atual — cabe quando facetas são acopladas o suficiente para que enumerar gere planos co-dependentes sem ganho de paralelismo). Fronteira com **Intenção vaga** acima: lá intenção não cristalizou (sem critério operacional); aqui sim, mas escopo amplo. Fronteira com **Bifurcação arquitetural** abaixo: lá 2 caminhos competindo para mesmo objeto; aqui 1 caminho potencialmente dimensionado demais. Fronteira com **Escopo** (bullet imediatamente anterior): lá pergunta "cabe num menor?"; aqui pergunta "precisa partir em ≥2?" como continuação quando a resposta foi "não". **Precedência:** cutucada de Intenção vaga precede esta — decomposição pressupõe intenção cristalizada.
- **Superfícies além do código:** runtime config (env, segredos, templates), infraestrutura (compose, deploy, CI), docs operacionais, automação do projeto (skills/rules/hooks). Se sim, listar em `## Arquivos a alterar`. Anti-padrão: feature "código-completa" mas "em-produção-quebrada".
- **Invariantes:** alguma RN do `ubiquitous_language` é tocada?
- **Integrações:** alguma do `design_notes` entra?
- **Decisão estrutural duradoura?** Gatilho de ADR. Sinais: (i) muda forma/lugar de persistência ou schema; (ii) inverte/contradiz decisão registrada em `decisions_dir` (probe via passo 1.5); (iii) codifica restrição externa de longa duração (regulatória, contratual, integração estável).
- **Aprendizado de domínio:** bounded context novo, aggregate/entity novo, RN nova, conceito ubíquo novo, ou semântica alterada?
- **Validação manual?** Comportamento perceptível, fluxo crítico, ou integração frágil → plano inclui `## Verificação manual`. Refactor/internal/doc-only não precisa — `make test` basta.
  - **Surface não-determinística** (parsing, matching de strings contra dado real, comportamento de agente LLM): exigir antes do plano (a) **forma do dado real** — 1-2 exemplos concretos do formato em produção (separadores, prefixos, capitalização, ids internos que não devem vazar); (b) **cenários enumerados** em `## Verificação manual` — passos concretos que exercitem essas formas, não direção genérica. Sem enumeração, validação manual vira improvisação. Sub-bullet não dispara se a pergunta-pai (`Validação manual?`) resolveu "não".
- **Cobertura de teste?** Heurística: (i) bloco `{reviewer: qa}` quando toca invariante, integração, persistência, comportamento observável novo, ou é bug fix com risco de regressão; (ii) só `## Verificação end-to-end` textual quando gate automático cobre e nada de invariante novo entra; (iii) nada novo em testes para refactor puro / doc-only.
- **Bifurcação arquitetural:** dois caminhos com custo/manutenção/UX significativamente diferentes? Heurística: você consegue redigir dois planos distintos que ambos satisfazem a frase? Verbos abertos ("registrar", "validar", "notificar", "processar", "armazenar", "interagir") são sintoma frequente. **Precedência:** cutucada de Intenção vaga precede esta — bifurcação pressupõe intenção cristalizada com 2 caminhos competindo.

Se o operador já forneceu o necessário, pular as perguntas. Se houver 1–3 gaps reais, perguntar direto e curto. **Não fazer entrevista exaustiva.** Modo: gaps de escolha discreta via `AskUserQuestion`; gaps que pedem explicação livre (forma do dado real, justificativa de escopo) em prosa **separada** após a chamada. **Quando ≥2 gaps são enum-áveis, agrupar numa única chamada** (até 4 questions, regra de unificação em `CLAUDE.md` → "AskUserQuestion mechanics") — sequenciar prompts fragmenta foco.

**Itens fora de escopo emergidos.** Coisas que o operador menciona mas não pertencem a esta feature (TODO adjacente, tech-debt revelado, bug menor avistado): capturar como candidatos. Papel `backlog` resolvido normalmente → linhas separadas em `## Próximos`. Papel "não temos" → reportadas no passo 5. "Deixa pra lá" → descartar.

**Bifurcação detectada → pergunta nominal-comparativa obrigatória antes do plano.** Modo: enum com opções `(a) caminho-default-barato` e `(b) caminho-rico`, `description` carregando o trade-off concreto. Operador escolhe ou usa "Other". Escolha vai para `## Contexto` ou `## Resumo da mudança`. Se o operador já citou explicitamente uma opção na frase original (`/triage exportar CSV usando streaming`), pular a pergunta e registrar direto. **Dispatch:** quando bifurcação coexiste com outros gaps enum-áveis, integra a chamada unificada da regra de agrupamento acima — não sequenciar como chamada separada (preserva a invariante de unificação preferida sobre sequência).

### 3. Decidir o artefato

Escolher **um** caminho. Em dúvida, preferir o mais leve.

| Caminho | Quando usar |
| --- | --- |
| **Só linha no BACKLOG** | Mudança pequena, foco claro, sem decisão estrutural nem integração nova. Maioria dos casos. |
| **Plano em `docs/plans/`** | Multi-arquivo, multi-fase, ou exige alinhamento prévio sobre a abordagem. |
| **ADR via `/new-adr`** | Decisão estrutural duradoura (persistência, biblioteca core, contrato de integração, política do sistema). |
| **Atualizar `docs/domain.md`** | Bounded context novo, aggregate/entity novo, RN nova, conceito ubíquo novo, ou semântica alterada. **Antes** de implementar. |
| **Atualizar `docs/design.md`** | Peculiaridade nova de integração descoberta na conversa. |
| **Edit atômico em SKILL/agent/plano** | Refinamento de 1-N edits cirúrgicos em path-set narrow (`agents/*.md`, `skills/**/SKILL.md`, `docs/plans/*.md`), sem multi-fase nem decisão estrutural; dispara `@prompt-reviewer` pré-commit no step 5 (per [ADR-063](../../docs/decisions/ADR-063-caminho-atomico-trigger-prompt-reviewer.md)). |

**Critério mecânico de discriminação da 6ª linha** vs. linhas 2 (plano novo) e 4-5 (domain/design): linha 6 aplica quando todos os 4 critérios aplicam — (i) paths editados ⊆ path-set narrow (`agents/*.md` ∪ `skills/**/SKILL.md` ∪ `docs/plans/*.md`); (ii) edit cirúrgico (1-N edits localizados sem multi-fase nem decisão estrutural); (iii) substância **não** captura por linhas 4-5 (não é update de `docs/domain.md` nem de `docs/design.md` — paths literais); (iv) não há criação de plano novo no fluxo corrente — edits são exclusivamente em arquivos pré-existentes do path-set (discrimina contra linha 2 da tabela quando alvo é `docs/plans/*.md`: criar plano novo cai na linha 2 e dispara sub-fluxo de criação canonical via template; refinamento de plano pré-existente cai na linha 6). **Path misto** (path-set narrow ∪ domain/design no mesmo `/triage`): predicado ⊆-strict prevalece → linha 6 **não** aplica; substância cai em linhas 4-5; trigger automático não dispara (operador pode invocar `@prompt-reviewer` manualmente).

Combinações são comuns (linha de backlog + ADR; plano + atualização de domain).

### 4. Produzir os artefatos

Idioma de saída: per `CLAUDE.md` → 'Reviewer/skill report idioma'.

**BACKLOG (papel: `backlog`):**

- **Papel resolvido normalmente:** uma linha para a feature em curso (frase de intenção, sem detalhamento).
  - Caminho com plano → não grava no BACKLOG (state vivo é a worktree/PR aberto, ADR-049 § Decisão (a)); a linha em `**Linha do backlog:**` no `## Contexto` do plano alimenta `/run-plan` para registrar conclusão em `## Concluídos` no done.
  - Caminho sem plano (linha pura, ADR-only, atualização de domínio) → grava em `## Próximos`.
  - Itens fora-de-escopo capturados no passo 2 → linhas separadas em `## Próximos`, mesmo quando o artefato principal é plano/ADR.
- **Papel "não temos":** disparar enum (`AskUserQuestion`, header `Backlog`). `Criar em BACKLOG.md` cria com cabeçalho mínimo (`# Backlog\n\n## Próximos\n\n## Concluídos\n`) e prossegue; `Não usamos esse papel` registra `paths.backlog: null` e prossegue **sem gravar** (itens reportados no passo 5).
- **Papel em modo `local`:** linha gravada em `.claude/local/BACKLOG.md`. `**Linha do backlog:**` no plano:
  - Ambos `backlog` e `plans_dir` em modo `local`: linha presente (matching textual entre arquivos locais).
  - `backlog` canonical + `plans_dir` local: linha presente no plano local (não vaza para git).
  - Ambos canonical: caso default.

  Combinação `backlog: local + plans_dir: canonical` recusada upstream por [ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md) (`/init-config` step 3 + `/triage` step 1) — não ocorre.

- **Papel em modo `forge`** (`paths.backlog: forge`, per [ADR-058](../../docs/decisions/ADR-058-role-backlog-aceitar-forge.md)): em vez de gravar linha em `## Próximos` de arquivo, cria issue no forge. Seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md`; output `no-detection` ou `unsupported-host` → **parar com erro explícito** orientando setup (`gh auth login` / `glab auth login` / `dnf install jq`) ou declarar `paths.backlog: null` ou path canonical (policy do caller per ADR-058 § (d)). Para cada linha a gravar (feature em curso no caminho sem plano + cada item fora-de-escopo), disparar cutucada `AskUserQuestion` (header `Forge`, opções `Aplicar no forge` (Recommended) / `Cancelar (não aplicar)`) antes de `gh issue create -t "<linha>" -b "<contexto>" --json number,url` (gh) ou `glab issue create -t "<linha>" -d "<contexto>"` (glab). URL/number retornado registrado para uso downstream — identificador canonical `#<número>: <título>` per § Plano abaixo. Combinação `forge + plans_dir: canonical` é válida (per ADR-058 § (i) — identificador é público por construção).

**Plano (papel: `plans_dir`):** ler `${CLAUDE_PLUGIN_ROOT}/templates/plan.md` como esqueleto canônico, copiar para `<plans_dir>/<slug>.md`, adaptar headers ao idioma do projeto consumidor (per `docs/philosophy.md` → "Convenção de idioma"), preencher placeholders com o conteúdo decidido nos passos 2-3. **Após cópia do template, inserir bloco `## Status` com valor `Pendente` logo após `# Plano — <Título>` e antes de `## Contexto`** (per [ADR-060](../../docs/decisions/ADR-060-heuristica-completude-planos-via-status.md) § Localização do campo — estado inicial do plano pré-execução; `/run-plan §3.4` remove o bloco no done). Em modo `local` (`paths.plans_dir: local`), copia para `.claude/local/plans/<slug>.md`; resto idêntico.

No `## Contexto`:

- Se o passo 1 identificou termos do `ubiquitous_language` tocados, incluir `**Termos ubíquos tocados:** <Termo> (<categoria>), ...` — categorias: `bounded context`, `agregado`, `entidade`, `RN`, `conceito ubíquo`. Pedidos que não tocam o domínio → omitir.
- Se o passo 1 (listar ADRs relacionados em `decisions_dir`) identificou ADRs concretos tocados/contradictados pela mudança, incluir `**ADRs candidatos:** ADR-NNN (motivo curto), ADR-MMM (motivo curto)` — mensageiro para o `design-reviewer` priorizar leitura integral desses ADRs (paralelo a `**Termos ubíquos tocados:**`; mecanismo em [ADR-048](../../docs/decisions/ADR-048-free-read-design-reviewer-consolidado.md)). Campo opcional: operador que não identifica ADR específico omite, e o reviewer faz scan dos demais.
- Se a feature foi gravada como linha no backlog, incluir `**Linha do backlog:** <texto exato>` — mensageiro de matching para `/run-plan` operar transições de estado. Em modo `forge` (`paths.backlog: forge`), texto é `#<número>: <título>` retornado pela `issue create` (per ADR-058 § (c)), não texto livre — identificador estável para `/run-plan §3.4` consumir e fechar issue no done.
- Se a branch corrente é a desejada para execução (caminho issue-first GitLab, retrabalho de PR), incluir `**Branch:** <nome-da-branch>` — mensageiro para `/run-plan` fazer checkout dela em vez de criar `<slug>` (ADR-049 § Decisão (b)). Probe e cutucada descritos abaixo.

**Probe e cutucada do `**Branch:**`.** Executar `git branch --show-current`. Resolver branch principal via `git symbolic-ref refs/remotes/origin/HEAD` (parse final do path: `origin/main` → `main`); falha → fallback `main`. Branch atual == principal → omitir o campo (silêncio, fluxo default preservado). Branch atual ≠ principal → perguntar via `AskUserQuestion` (header `Branch`, opções literais `Sim, usar essa branch (Recommended)` / `Não, checkout principal e /run-plan cria <slug>`; `description` de cada opção conforme [ADR-049](../../docs/decisions/ADR-049-execucao-run-plan-consolidado.md) § Decisão (b) § Mecânica). Resposta `Sim` → preencher `**Branch:** <branch-atual>` no `## Contexto`. Resposta `Não` → executar `git checkout <principal>` antes de prosseguir (efeito carregado no label da opção; click do operador é o consent ao switch) + omitir o campo. Falha do checkout (edits uncommitted incompatíveis, conflict, etc.) → reportar erro literal e parar; operador resolve manualmente e re-invoca `/triage`.

`BACKLOG.md` **não aparece** em `## Arquivos a alterar` — transições são geridas pelo campo acima e pelo mecanismo do `/run-plan`.

Em `## Arquivos a alterar`, anotação `{reviewer: <perfil>}` no fim do header da subseção orienta o `/run-plan`. Palavra-chave em inglês (mecânica do toolkit). **Single-reviewer é o caso normal** — um bloco, um eixo de revisão, um agent. Schema:

- **Sem anotação** → default `code-reviewer` (exceções: doc-only ampla + override do path-set per ADR-062 — ver regras abaixo).
- **Um perfil** (`{reviewer: code|qa|security|doc}`) → indica explicitamente o agent que revisará o bloco.
- **Múltiplos perfis** (`{reviewer: code,qa}` etc.) → exceção rara para quando o mesmo diff genuinamente merece olhares de eixos diferentes que não cabem em blocos separados. **Preferir separar em blocos** quando viável — bloco por arquivo/agrupamento lógico já tende a isolar eixos naturalmente.

Exemplos:

```markdown
### Bloco 1 — autenticação {reviewer: security}
### Bloco 2 — refactor interno
### Bloco 3 — atualizar README {reviewer: doc}
```

Bloco que **contém testes** (saída (i) da heurística de cobertura) recebe `{reviewer: qa}`; reviewer revisa qualidade do teste recém-escrito (caminho feliz, invariantes, edge cases, mock vs real).

Bloco **doc-only** (paths todos `.md`/`.rst`/`.txt`) recebe `doc-reviewer` como default — omitir anotação ou usar `{reviewer: doc}` para deixar explícito. Diff que toca código E doc adjacente — preferir separar em dois blocos (`{reviewer: code}` e `{reviewer: doc}`); `{reviewer: code,doc}` no mesmo bloco continua válido como exceção rara quando a separação não faz sentido lógico.

**Exceção do path-set** (per [ADR-062](../../docs/decisions/ADR-062-criar-subagent-prompt-reviewer.md)): bloco doc-only cujos paths caem em `agents/*.md`/`skills/**/SKILL.md`/`docs/plans/*.md` recebe `prompt-reviewer` como default (regra mais-específico-vence sobre doc-only ampla; dispatch logic literal em `skills/run-plan/SKILL.md` §2 item 3). Usar `{reviewer: prompt}` para explicitar; `{reviewer: doc}` continua válido como override do operador quando a mudança é puramente editorial-doc (typo, reordenação) e não toca substância algorítmica.

**ADR:** chamar a tool `Skill` com `name="pragmatic-dev-toolkit:new-adr"` e `args=<título>` (não duplicar lógica nem criar arquivo manualmente). Reportar e seguir. `/new-adr` aplica o modo do `decisions_dir` automaticamente — em modo `local`, ADR criado em `.claude/local/decisions/`.

**`docs/domain.md` / `docs/design.md`:** edit cirúrgico, preservar tom e estrutura.

Slug de plano: lowercase, espaços/acentos→hífens, curto e descritivo (ex.: `exportar-movimentos-csv`).

**Consolidação (quando há edit em `backlog`).** Após gravar linha da feature ou itens fora-de-escopo:

1. **Reler** o backlog na íntegra após edits. Em modo `forge`, relê via `gh/glab issue list --state open` (todas issues abertas, não só sem assignee — escopo de consolidação inclui pares com issues já assignadas para detectar duplicatas) para detectar duplicatas com issues pré-existentes; consolidação é apenas de duplicatas/obsolescência (sem fechar issues automaticamente), sem cutucadas remotas adicionais nesta etapa. **Issues com assignee detectadas como duplicata** entram no enum de consolidação como informacional (flag visível ao operador) — Aplicar edits do passo 4 abaixo opera apenas sobre issues no escopo do papel (sem assignee); não fecha nem edita issues alheias mesmo quando o operador descreve edit em prosa via Other.
2. **Flagar** (não decidir):
   - **Duplicatas** entre linhas recém-adicionadas e linhas pré-existentes em qualquer seção.
   - **Obsolescência:** linha em `## Próximos` que vira redundante pela nova (ex.: nova "exportar movimentos em CSV" cobre antiga "exportar movimentos como planilha"). Critério conservador — só flagar quando a sobreposição é nítida no texto, não em similaridade vaga.
3. **Sem flags → skip silente.** Linhas recém-gravadas já foram decididas no fluxo corrente.
4. **Com flags →** mostrar ao operador o estado tocado (com linhas recém-adicionadas marcadas) e perguntar uma vez via enum (`AskUserQuestion`, header `Backlog`, opções `Está bom, prosseguir` / `Aplicar edits`; Other → operador descreve em prosa quais edits — consolidar duplicatas, remover obsoleta, reordenar). Edits descritos entram no mesmo commit unificado do passo 5. Em modo `forge`, edits descritos que impliquem mutação remota (fechar/editar issue) **disparam cutucada por mutação** (header `Forge`) — mesma policy do passo 4 de criação.

Caminho que não tocou backlog (atualização pura de `ubiquitous_language`/`design_notes`, ADR delegada sem linha, papel `backlog` "não temos") → skip silente desta etapa.

### 5. Reportar, propor commit e devolver controle

Reportar em formato curto:

- O que foi registrado (linha, plano, ADR, atualização de domínio).
- Paths dos arquivos criados/alterados.

Quando `backlog` resolveu "não temos", acrescentar **"Itens não registrados (papel `backlog` desativado):"** listando (a) a frase de intenção que teria sido gravada e (b) cada item fora-de-escopo do passo 2.

**Revisão pré-commit (caminho-com-plano).** Quando o passo 4 produziu plano (caminho-com-plano, com ou sem ADR delegada via `/new-adr`), invocar `@design-reviewer` apontando para o plano. Sem cutucada de pré-execução — o reviewer dispara automaticamente conforme [ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (b). Ao compor o prompt da invocação, seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/reviewer-invocation-read.md` (instrução defensiva de `Read` do plano antes da análise). Para cada finding, aplicar critério de [ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (c):

- **Cutucar operador** via `AskUserQuestion` se finding satisfaz ≥1 das 3 condições: (i) ≥2 alternativas legítimas competindo (alternativa rebatida descritivamente pelo reviewer conta como 1 caminho; só conta como ≥2 quando o reviewer apresenta caminhos competindo sem rebater); (ii) contradiz decisão documentada em ADR/`philosophy.md`/`CLAUDE.md`; (iii) exige contexto fora do diff/plano/ADR. Cláusula default-conservadora: dúvida na classificação → cutucar.
- **Absorver pré-commit** quando nenhuma condição dispara (caminho-único). Aplicar correção; registrar no commit message conforme regra de forma abaixo.

**Não dispara** quando o caminho fechou em linha de backlog pura, atualização cirúrgica de `docs/domain.md`/`docs/design.md`, ADR-only delegada sem plano, ou edit atômico em SKILL/agent/plano em path-set narrow (coberto pelo `prompt-reviewer` per [ADR-063](../../docs/decisions/ADR-063-caminho-atomico-trigger-prompt-reviewer.md), dispatch ortogonal) — ADR-only é coberta pelo wiring de `/new-adr` (evita dispatch duplo no caminho `/triage` → `/new-adr` → reviewer).

Caminho-atômico em path-set narrow (`agents/*.md` ∪ `skills/**/SKILL.md` ∪ `docs/plans/*.md`) **dispara** `@prompt-reviewer` per ADR-063 — ver parágrafo "Revisão pré-commit (caminho-atômico em path-set narrow)" abaixo.

**Revisão pré-commit (caminho-atômico em path-set narrow).** Quando o passo 4 produziu edits cirúrgicos em arquivos cujos paths satisfazem o critério ⊆-strict da 6ª linha da tabela do step 3 (per [ADR-063](../../docs/decisions/ADR-063-caminho-atomico-trigger-prompt-reviewer.md)), invocar `@prompt-reviewer` apontando para os arquivos editados antes do commit. Ao compor o prompt da invocação, seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/reviewer-invocation-read.md` (instrução defensiva de `Read` antes da análise). Para cada finding, aplicar critério de [ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (c) com **mapeamento por analogia** das 3 condições sobre as 4 heurísticas seed do `prompt-reviewer` (per ADR-063 § Decisão #4):

- Condição 1 (≥2 alternativas legítimas competindo) ≈ heurística "passo ambíguo".
- Condição 2 (contradiz decisão documentada em ADR/`philosophy.md`/`CLAUDE.md`) ≈ heurística "passo contraditório em estado global".
- Condição 3 (exige contexto fora do diff/plano/ADR) raramente aplica a findings algorítmicos.

Cláusula default-conservadora preserva ("dúvida na classificação → cutucar"). Findings absorvidos pré-commit (caminho-único) entram em `## prompt-reviewer findings absorvidos` no commit message (forma análoga ao bloco do `design-reviewer`); findings cutucados via `AskUserQuestion` viram parte do trace narrativo normal.

Propor commit único agrupando os artefatos. Mensagem segue a convenção do projeto consumidor (default Conventional Commits em inglês, `docs:` ou `chore:`). Confirmação via enum (`AskUserQuestion`, header `Commit`, opções `Confirmar e commitar` / `Editar mensagem`).

**Forma do commit message com findings absorvidos.** Quando ≥1 finding foi absorvido pré-commit ([ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (c)), commit message inclui seção `## <reviewer> findings absorvidos` por reviewer disparado — `design-reviewer` no caminho-com-plano (e/ou ADR delegada) e/ou `prompt-reviewer` no caminho-atômico em path-set narrow (per [ADR-063](../../docs/decisions/ADR-063-caminho-atomico-trigger-prompt-reviewer.md)) (idioma da convenção de commits per [ADR-051](../../docs/decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (a)) com bullets curtos no formato `- <localização breve>: <correção aplicada> (caminho-único).`. Seção omitida quando não há findings absorvidos do reviewer respectivo. Findings cutucados via `AskUserQuestion` não entram nesta seção — viram parte do trace narrativo normal (decisão do operador descrita em prosa).

**Mirror no plan body (per [ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (d)).** A mesma seção também é escrita no body do plano sob `## Decisões absorvidas` (após `## Notas operacionais` quando existe; último bloco antes do EOF caso contrário), com formato de bullets idêntico ao do commit message. Edit cirúrgico antes do commit (mesma sequência atômica). Consumida em runtime por `/run-plan` §2.3 que passa o conteúdo como contexto na invocação dos reviewers por bloco. Seção omitida no plan body quando não há findings absorvidos. **Mirror não aplica ao caminho-atômico em path-set narrow** — o caminho não é caminho-com-plano (plan body não é o artefato produzido pelo `/triage` nem o trace de execução do `/run-plan`; mesmo quando o edit toca `docs/plans/*.md`, o plan body sendo editado **é** o diff revisado, não destino de espelhamento). A seção `## prompt-reviewer findings absorvidos` vive apenas no commit message.

Após confirmação:

- **Caminho sem plano:** apenas `git commit -m "…"`. Push não exigido.
- **Caminho com plano:** confirmação cobre **commit + push como unidade atômica**. **Resolver branch designada:** principal (`git symbolic-ref refs/remotes/origin/HEAD`, fallback `main`) OR campo `**Branch:**` do plano (passo 4) quando set. Verificar `git rev-parse --abbrev-ref HEAD`:
  - Branch corrente == designada → **um único** `Bash` com `git commit -m "…" && git push origin <branch-atual>` — sem flags. Regra única cobre fluxo default (designada = principal) e fluxo issue-first (designada = campo Branch, per ADR-049 § Decisão (b)).
  - Branch corrente ≠ designada → parar e reportar drift (caso anômalo: operador moveu de branch entre passo 4 e passo 5; reconciliação manual).

  Push falho → reportar erro literal e parar; commit local permanece, `/run-plan` recusará até o operador resolver. Push imediato materializa o plano como state visível ao restante do sistema — `/run-plan` parte de origin (não local), próximos `/triage` veem o plano em `<plans_dir>` para detectar trabalho em curso, e operador em outra máquina reconcilia. Sem o push, plano existe só localmente e o sistema não tem como reconciliar.
- **Caminho com plano em modo `local`** (regra de não-referenciar, ADR-047, aplicada por-papel): se `plans_dir: local`, omitir slug do plano na mensagem de commit; se `backlog: local`, omitir texto da linha do backlog. Papéis em modo canonical seguem referenciados normalmente. Artefatos em modo local não entram no commit (gitignored).

Se não há alterações para commitar (ADR-only que já commitou via `/new-adr`, ou nada alterado), pular.

Sugerir próximo passo (uma frase): "implementar via /run-plan <slug>", "validar o plano antes de codar", "preencher o ADR".

**Cutucada de descoberta.** Antes de devolver controle, executar a cutucada conforme `${CLAUDE_PLUGIN_ROOT}/docs/procedures/cutucada-descoberta.md`.

## O que NÃO fazer

- Não duplicar conteúdo de `CLAUDE.md`, `docs/domain.md` ou `docs/design.md` no plano — referenciar.
- Não separar `git commit` e `git push` no caminho-com-plano — a unidade atômica do passo 5 elimina a janela em que push é esquecido.
- Não recuperar push falho via `--force`, `--force-with-lease`, retry automático ou flags equivalentes — parar, reportar erro literal e deixar manual.
