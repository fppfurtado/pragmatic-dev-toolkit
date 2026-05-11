---
name: triage
description: Alinha intenção e decide artefato (backlog, plano, ADR, atualização de domain/design) antes de implementar. Use quando o operador propuser feature, fix ou refactor sem plano nem linha de backlog.
roles:
  required: [plans_dir]
  informational: [backlog, ubiquitous_language, design_notes, decisions_dir, product_direction]
---

# triage

Workflow de **alinhamento prévio** para mudança não-trivial — feature, fix com plano (saída de `/debug`), refactor com bifurcação, alteração que toca invariante. Produz artefato de alinhamento (linha de backlog, plano, ADR, atualização de `docs/domain.md`/`docs/design.md`) e devolve controle.

## Sub-fluxo de criação canonical

Quando o passo 3 escolher "atualizar `ubiquitous_language`/`design_notes`" e o papel resolveu "não temos": propor criação no path canonical via enum (`Criar em <path>` / `Não usamos esse papel`). Segunda opção registra `paths.<role>: null` (oferta única de memorização). Mesmo mecanismo para `backlog` quando o passo 4 vai gravar linha (`Criar em BACKLOG.md` / `Não usamos esse papel`; segunda registra `paths.backlog: null`).

**Modo local** (`paths.<role>: local` declarado): skill cria/lê em `.claude/local/<role>/` em vez de path canonical, sem disparar enum de criação. Mecânica de inicialização (`mkdir`, probe gitignore, gate `Gitignore`) coberta pela seção "Local mode" do CLAUDE.md.

## Argumentos

Intenção em linguagem natural — frase curta (`/triage exportar movimentos em CSV`), descrição com contexto, ou vaga. Input vazio ou genericamente "o que vamos fazer hoje?" → seguir `skills/next/SKILL.md`.

## Passos

### 0. Cleanup pós-merge

Antes de carregar contexto, varrer worktrees mergeadas em `.worktrees/` e oferecer cleanup. Skip silente quando nada a limpar; nunca incomoda no caminho-comum.

**Detecção de candidatos:**

1. `git worktree list --porcelain` → filtrar entradas cujo `worktree` está sob `.worktrees/` (excluir worktree principal).
2. Para cada candidato, extrair branch (`branch refs/heads/<slug>` da saída porcelain).
3. Verificar merge status: `gh pr list --state merged --head <branch> --json number --jq '.[0].number'` (squash-aware). Saída numérica → mergeado, capturar PR number. Saída vazia / `gh` ausente → fallback `git branch -r --merged origin/<main>` checando se `<branch>` está listada (perde squash). Sem detecção em nenhum dos dois → não é candidato; pular.
4. Lista de candidatos mergeados vazia → **skip silente**; segue para o passo 1.

**Cutucada por candidato.** Para cada candidato, `AskUserQuestion`:

- `header`: `Cleanup`
- `question`: `"Worktree '<slug>' (PR #<num> mergeado): limpar o quê?"` (omitir `PR #<num>` no fallback git-only)
- `multiSelect`: `true`
- Opções:
  - `Worktree` — `description`: `"git worktree remove .worktrees/<slug>"`
  - `Branch local` — `description`: `"git branch -d <slug>; squash detectado força -D com nota"`
  - `Branch remota` — `description`: `"git push origin --delete <slug>"`

Sem seleção (todas desmarcadas + confirmar) → skip esse candidato; segue para o próximo.

**Execução das seleções.** Ordem importa para isolamento — `worktree remove` antes de `branch -d` (worktree em uso bloqueia delete). Ordem padrão: Worktree → Branch local → Branch remota.

- `Branch local`: tentar `git branch -d <slug>` primeiro. Falha com "not fully merged" → executar `git branch -D <slug>` e reportar `"branch <slug> não mergeada via fast-forward — squash detectado via gh; usando -D"` (caso real para PRs squash-merged onde ancestry local não bate).
- `Branch remota`: tentar `git push origin --delete <slug>`. Falha com `remote ref does not exist` no stderr → branch já estava apagada no remoto (auto-delete pós-merge do GitHub, etc.); reportar `"branch <slug> já estava apagada no remoto"` e seguir.
- Falha em qualquer comando após o primeiro → reportar erro literal e parar (sem `--force` adicional, sem retry). Comandos já executados permanecem aplicados; operador resolve o resto manual.

**Após todos os candidatos:** `git fetch origin --prune` para limpar refs remotos órfãos.

### 1. Carregar contexto mínimo

Ler **só o que o pedido tocar**, nesta ordem:

1. `product_direction` — alinhamento à direção de produto.
2. `ubiquitous_language` — bounded contexts, agregados/entidades, RNxx tocadas.
3. `backlog` — verificar item equivalente em **Próximos** ou **Concluídos**. Se existir, parar e reportar. (Sob ADR-004, "em andamento" é state em git/forge; se a intenção corresponde a branch/worktree já em curso, `/run-plan` precondição 4 bloqueia ao tentar criar worktree com slug colidente.)
4. `design_notes` — só se a feature toca uma das integrações listadas.
5. `decisions_dir` — listar ADRs relacionados; ler na íntegra apenas os que o pedido contradiz/estende.

Não ler código aqui — é alinhamento de intenção, não design técnico.

### 2. Esclarecer gaps com o usuário

Identificar lacunas e perguntar **só o que for bloqueante**. Checklist mental (não questionário):

- **Escopo:** o que entra e o que fica de fora? Há caso menor que resolve 80%?
- **Superfícies além do código:** runtime config (env, segredos, templates), infraestrutura (compose, deploy, CI), docs operacionais, automação do projeto (skills/rules/hooks). Se sim, listar em `## Arquivos a alterar`. Anti-padrão: feature "código-completa" mas "em-produção-quebrada".
- **Invariantes:** alguma RN do `ubiquitous_language` é tocada?
- **Integrações:** alguma do `design_notes` entra?
- **Decisão estrutural duradoura?** Gatilho de ADR. Sinais: (i) muda forma/lugar de persistência ou schema; (ii) inverte/contradiz decisão registrada em `decisions_dir` (probe via passo 1.5); (iii) codifica restrição externa de longa duração (regulatória, contratual, integração estável).
- **Aprendizado de domínio:** bounded context novo, aggregate/entity novo, RN nova, conceito ubíquo novo, ou semântica alterada?
- **Validação manual?** Comportamento perceptível, fluxo crítico, ou integração frágil → plano inclui `## Verificação manual`. Refactor/internal/doc-only não precisa — `make test` basta.
  - **Surface não-determinística** (parsing, matching de strings contra dado real, comportamento de agente LLM): exigir antes do plano (a) **forma do dado real** — 1-2 exemplos concretos do formato em produção (separadores, prefixos, capitalização, ids internos que não devem vazar); (b) **cenários enumerados** em `## Verificação manual` — passos concretos que exercitem essas formas, não direção genérica. Sem enumeração, validação manual vira improvisação. Sub-bullet não dispara se a primeira pergunta resolveu "não".
- **Cobertura de teste?** Heurística: (i) bloco `{reviewer: qa}` quando toca invariante, integração, persistência, comportamento observável novo, ou é bug fix com risco de regressão; (ii) só `## Verificação end-to-end` textual quando gate automático cobre e nada de invariante novo entra; (iii) nada novo em testes para refactor puro / doc-only.
- **Bifurcação arquitetural:** dois caminhos com custo/manutenção/UX significativamente diferentes? Heurística: você consegue redigir dois planos distintos que ambos satisfazem a frase? Verbos abertos ("registrar", "validar", "notificar", "processar", "armazenar", "interagir") são sintoma frequente.

Se o operador já forneceu o necessário, pular as perguntas. Se houver 1–3 gaps reais, perguntar direto e curto. **Não fazer entrevista exaustiva.** Modo: gaps de escolha discreta via `AskUserQuestion`; gaps que pedem explicação livre (forma do dado real, justificativa de escopo) em prosa **separada** após a chamada. **Quando ≥2 gaps são enum-áveis, agrupar numa única chamada** (até 4 questions, regra de unificação em `CLAUDE.md` → "AskUserQuestion mechanics") — sequenciar prompts fragmenta foco.

**Itens fora de escopo emergidos.** Coisas que o operador menciona mas não pertencem a esta feature (TODO adjacente, tech-debt revelado, bug menor avistado): capturar como candidatos. Papel `backlog` resolvido normalmente → linhas separadas em `## Próximos`. Papel "não temos" → reportadas no passo 6. "Deixa pra lá" → descartar.

**Bifurcação detectada → pergunta nominal-comparativa obrigatória antes do plano.** Modo: enum com opções `(a) caminho-default-barato` e `(b) caminho-rico`, `description` carregando o trade-off concreto. Operador escolhe ou usa "Other". Escolha vai para `## Contexto` ou `## Resumo da mudança`. Se o operador já citou explicitamente uma opção na frase original (`/triage exportar CSV usando streaming`), pular a pergunta e registrar direto.

### 3. Decidir o artefato

Escolher **um** caminho. Em dúvida, preferir o mais leve.

| Caminho | Quando usar |
| --- | --- |
| **Só linha no BACKLOG** | Mudança pequena, foco claro, sem decisão estrutural nem integração nova. Maioria dos casos. |
| **Plano em `docs/plans/`** | Multi-arquivo, multi-fase, ou exige alinhamento prévio sobre a abordagem. |
| **ADR via `/new-adr`** | Decisão estrutural duradoura (persistência, biblioteca core, contrato de integração, política do sistema). |
| **Atualizar `docs/domain.md`** | Bounded context novo, aggregate/entity novo, RN nova, conceito ubíquo novo, ou semântica alterada. **Antes** de implementar. |
| **Atualizar `docs/design.md`** | Peculiaridade nova de integração descoberta na conversa. |

Combinações são comuns (linha de backlog + ADR; plano + atualização de domain).

### 4. Produzir os artefatos

Idioma de saída: espelhar o do projeto consumidor (default canonical PT-BR; ver "Convenção de idioma" em `docs/philosophy.md`).

**BACKLOG (papel: `backlog`):**

- **Papel resolvido normalmente:** uma linha para a feature em curso (frase de intenção, sem detalhamento).
  - Caminho com plano → não grava no BACKLOG (state vivo é a worktree/PR aberto, ADR-004); a linha em `**Linha do backlog:**` no `## Contexto` do plano alimenta `/run-plan` para registrar conclusão em `## Concluídos` no done.
  - Caminho sem plano (linha pura, ADR-only, atualização de domínio) → grava em `## Próximos`.
  - Itens fora-de-escopo capturados no passo 2 → linhas separadas em `## Próximos`, mesmo quando o artefato principal é plano/ADR.
- **Papel "não temos":** disparar enum (`AskUserQuestion`, header `Backlog`). `Criar em BACKLOG.md` cria com cabeçalho mínimo (`# Backlog\n\n## Próximos\n\n## Concluídos\n`) e prossegue; `Não usamos esse papel` registra `paths.backlog: null` e prossegue **sem gravar** (itens reportados no passo 6).
- **Papel em modo `local`:** linha gravada em `.claude/local/BACKLOG.md`. `**Linha do backlog:**` no plano depende do modo cruzado:
  - Ambos `backlog` e `plans_dir` em modo `local`: linha presente (matching textual entre arquivos locais).
  - `backlog` canonical + `plans_dir` local: linha presente no plano local (não vaza para git).
  - `backlog` local + `plans_dir` canonical: **omitir** `**Linha do backlog:**` (texto local não pode vazar para plano commitado); `/run-plan` neste cenário não faz transição automática — operador move manualmente.
  - Ambos canonical: caso default.

**Plano (papel: `plans_dir`):** ler `${CLAUDE_PLUGIN_ROOT}/templates/plan.md` como esqueleto canônico, copiar para `<plans_dir>/<slug>.md`, adaptar headers ao idioma do projeto consumidor (per `docs/philosophy.md` → "Convenção de idioma"), preencher placeholders com o conteúdo decidido nos passos 2-3. Em modo `local` (`paths.plans_dir: local`), copia para `.claude/local/plans/<slug>.md`; resto idêntico.

No `## Contexto`:

- Se o passo 1 identificou termos do `ubiquitous_language` tocados, incluir `**Termos ubíquos tocados:** <Termo> (<categoria>), ...` — categorias: `bounded context`, `agregado`, `entidade`, `RN`, `conceito ubíquo`. Pedidos que não tocam o domínio → omitir.
- Se a feature foi gravada como linha no backlog, incluir `**Linha do backlog:** <texto exato>` — mensageiro de matching para `/run-plan` operar transições de estado.

`BACKLOG.md` **não aparece** em `## Arquivos a alterar` — transições são geridas pelo campo acima e pelo mecanismo do `/run-plan`.

Em `## Arquivos a alterar`, anotação `{reviewer: <perfil>}` no fim do header da subseção orienta o `/run-plan`. Palavra-chave em inglês (mecânica do toolkit). **Single-reviewer é o caso normal** — um bloco, um eixo de revisão, um agent. Schema:

- **Sem anotação** → default `code-reviewer` (exceção: blocos doc-only — ver regra abaixo).
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

**ADR:** chamar a tool `Skill` com `name="pragmatic-dev-toolkit:new-adr"` e `args=<título>` (não duplicar lógica nem criar arquivo manualmente). Reportar e seguir. `/new-adr` aplica o modo do `decisions_dir` automaticamente — em modo `local`, ADR criado em `.claude/local/decisions/`.

**`docs/domain.md` / `docs/design.md`:** edit cirúrgico, preservar tom e estrutura.

Slug de plano: lowercase, espaços/acentos→hífens, curto e descritivo (ex.: `exportar-movimentos-csv`).

### 5. Consolidação do backlog

Se o passo 4 modificou o arquivo do papel `backlog` (linha da feature, linhas fora-de-escopo, ou ambas), consolidar antes de fechar:

1. **Reler** o backlog na íntegra após edits.
2. **Flagar** (não decidir):
   - **Duplicatas** entre linhas recém-adicionadas e linhas pré-existentes em qualquer seção.
   - **Obsolescência:** linha em `## Próximos` que vira redundante pela nova (ex.: nova "exportar movimentos em CSV" cobre antiga "exportar movimentos como planilha"). Critério conservador — só flagar quando a sobreposição é nítida no texto, não em similaridade vaga.
3. **Sem flags → skip silente.** Linhas recém-gravadas já foram decididas no fluxo corrente.
4. **Com flags →** mostrar ao operador o estado tocado (com linhas recém-adicionadas marcadas) e perguntar uma vez via enum (`AskUserQuestion`, header `Backlog`, opções `Está bom, prosseguir` / `Aplicar edits`; Other → operador descreve em prosa quais edits — consolidar duplicatas, remover obsoleta, reordenar). Edits descritos entram no mesmo commit unificado do passo 6.

Caminho que não tocou backlog (atualização pura de `ubiquitous_language`/`design_notes`, ADR delegada sem linha, papel `backlog` "não temos") → skip silente.

### 6. Reportar, propor commit e devolver controle

Reportar em formato curto:

- O que foi registrado (linha, plano, ADR, atualização de domínio).
- Paths dos arquivos criados/alterados.

Quando `backlog` resolveu "não temos", acrescentar **"Itens não registrados (papel `backlog` desativado):"** listando (a) a frase de intenção que teria sido gravada e (b) cada item fora-de-escopo do passo 2.

**Revisão pré-commit (caminho-com-plano).** Quando o passo 4 produziu plano (caminho-com-plano, com ou sem ADR delegada via `/new-adr`), invocar `@design-reviewer` apontando para o plano. Sem cutucada de pré-execução — o reviewer dispara automaticamente conforme [ADR-011](../../docs/decisions/ADR-011-wiring-design-reviewer-automatico.md). Reportar findings ao operador antes de propor commit; findings são informativos, operador aplica ajustes ou segue como está. **Não dispara** quando o caminho fechou em linha de backlog pura, atualização cirúrgica de `docs/domain.md`/`docs/design.md`, ou ADR-only delegada sem plano — ADR-only é coberta pelo wiring de `/new-adr` (evita dispatch duplo no caminho `/triage` → `/new-adr` → reviewer).

Propor commit único agrupando os artefatos. Mensagem segue a convenção do projeto consumidor (default Conventional Commits em inglês, `docs:` ou `chore:`). Confirmação via enum (`AskUserQuestion`, header `Commit`, opções `Confirmar e commitar` / `Editar mensagem`).

Após confirmação:

- **Caminho sem plano:** apenas `git commit -m "…"`. Push não exigido.
- **Caminho com plano:** confirmação cobre **commit + push como unidade atômica**. Verificar `git rev-parse --abbrev-ref HEAD` — se não for branch principal (default `main`), parar e reportar. Se for, **um único** `Bash` com `git commit -m "…" && git push origin <branch-atual>` — sem flags. Push falho → reportar erro literal e parar; commit local permanece, `/run-plan` recusará até o operador resolver. Push imediato materializa o plano como state visível ao restante do sistema — `/run-plan` parte de origin (não local), próximos `/triage` veem o plano em `<plans_dir>` para detectar trabalho em curso, e operador em outra máquina reconcilia. Sem o push, plano existe só localmente e o sistema não tem como reconciliar.
- **Caminho com plano em modo `local`** (regra de não-referenciar, ADR-005, aplicada por-papel): se `plans_dir: local`, omitir slug do plano na mensagem de commit; se `backlog: local`, omitir texto da linha do backlog. Papéis em modo canonical seguem referenciados normalmente. Artefatos em modo local não entram no commit (gitignored).

Se não há alterações para commitar (ADR-only que já commitou via `/new-adr`, ou nada alterado), pular.

Sugerir próximo passo (uma frase): "implementar via /run-plan <slug>", "validar o plano antes de codar", "preencher o ADR".

**Cutucada de descoberta** (per [ADR-017](../../docs/decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md)). Antes de devolver controle, verificar: (a) `CLAUDE.md` existe; (b) `grep -q '<!-- pragmatic-toolkit:config -->' CLAUDE.md` retorna não-zero (marker ausente); (c) string canonical da cutucada não aparece no contexto visível desta conversa CC. Todas as três satisfeitas → emitir como última linha do relatório a string canonical abaixo. Caso contrário → suprimir silenciosamente.

> Dica: este projeto não declara o bloco `pragmatic-toolkit:config` no CLAUDE.md. Rode `/init-config` para configurar todos os papéis de uma vez.

## O que NÃO fazer

- Não duplicar conteúdo de `CLAUDE.md`, `docs/domain.md` ou `docs/design.md` no plano — referenciar.
- Não separar `git commit` e `git push` no caminho-com-plano — a unidade atômica do passo 6 elimina a janela em que push é esquecido.
- Não recuperar push falho via `--force`, `--force-with-lease`, retry automático ou flags equivalentes — parar, reportar erro literal e deixar manual.
