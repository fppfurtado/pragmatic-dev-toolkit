---
name: next
description: Lê o backlog, descarta itens já implementados e sugere top 3 candidatos por impacto estratégico. Invocável direto ou como pré-passo de /triage sem argumento.
disable-model-invocation: false
roles:
  required: [backlog]
  informational: [product_direction, plans_dir]
---

# next

Skill de orientação de sessão: lê o backlog, limpa itens já implementados e indica os três candidatos de maior impacto — alimentando o fluxo de `/triage` a seguir.

## Argumentos

Inteiro positivo opcional `N` — número de itens lidos do topo de `## Próximos` (modo arquivo) ou da lista de issues (modo forge) no passo 2. Default `10`. Input inválido (não-inteiro, ≤ 0) → reportar e usar default.

## Passos

### 1. Ler o backlog

**Em modo arquivo** (canonical ou `local`): ler o arquivo na íntegra. Extrair `## Próximos` — candidatos a analisar. Em modo `local` (`paths.backlog: local`), arquivo é `.claude/local/BACKLOG.md` (resolvido pelo Resolution protocol do CLAUDE.md); skill segue agnóstica ao path.

**Em modo `forge`** (`paths.backlog: forge`, per [ADR-058](../../docs/decisions/ADR-058-role-backlog-aceitar-forge.md)): seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md`. Output `gh` → `gh issue list --state open --search "no:assignee" --json number,title,createdAt --jq '.[]'`; output `glab` → `glab issue list --opened --not-assignee --output json | jq -r '.[] | {number: .iid, title, createdAt: .created_at}'`. Output `no-detection` ou `unsupported-host` → **parar com erro explícito** orientando setup (`gh auth login` / `glab auth login` / `dnf install jq`) ou declarar `paths.backlog: null` ou path canonical — role declarado depende inteiramente do CLI per ADR-058 § (d) policy do caller. Lista retornada substitui `## Próximos` no fluxo subsequente; itens formatados como `#<número>: <título>`.

`## Próximos` (modo arquivo) ou lista de issues (modo forge) vazia → informar e interromper.

Se `.claude/local/NOTES.md` existir, ler na íntegra para contexto suplementar de ranking — notas recentes podem revelar mudança de prioridade ou trabalho adjacente aos candidatos. Reportar se uma nota influenciou o ranking, ou explicitamente que o store estava presente sem notas relacionadas aos candidatos. Informational (per [ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (a) store non-role); nunca bloqueia.

### 2. Selecionar candidatos

Pegar os **`N` primeiros** itens de `## Próximos` em ordem de aparição (topo = mais antigo). Default `N = 10` (override por invocação via argumento posicional — ver `## Argumentos`) dá margem para descartar implementados e ainda chegar a três finais. Em modo `forge`, ordem natural é `createdAt` ascendente (lista já vem ordenada do passo 1); filtro `N` aplicado post-hoc sobre a lista do passo 1.

### 3. Verificar implementação no código

Para cada candidato, buscar evidência no repo (funções, endpoints, modelos, comandos, fluxos correspondentes). Classificar:

- **Evidência forte** — código claro e diretamente mapeável (ex.: item "exportar movimentos em CSV" → handler de export CSV presente e funcional). **Em modo arquivo:** preparar movimentação da linha para `## Concluídos` (escrever no arquivo) e reportar com justificativa de 1 linha; commit fica para o passo 6. **Em modo `forge`** (per ADR-058 § (e)): para cada issue com evidência forte, disparar cutucada `AskUserQuestion` (header `Forge`, opções `Aplicar no forge` (Recommended) / `Cancelar (não aplicar)`) com `description` da opção `Aplicar` carregando o(s) comando(s) concreto(s). Uma cutucada por issue. Confirmação → em `gh`, `gh issue close #<número> --reason completed --comment "<justificativa>"` (close + comentário num único comando); em `glab`, dois comandos sequenciais — `glab issue note <número> --message "<justificativa>"` então `glab issue close <número>` (CLI assimétrica: `glab issue close` não aceita `--comment`). Cancelamento → noop, segue como candidato normal. Commit do passo 6 é skip em modo forge (mutação já remota).
- **Evidência fraca** — código parcial, feature similar com escopo diferente, ou inferência incerta. Reportar o que foi encontrado; **não mover** — operador decide. Em modo forge, sem cutucada de fechamento (mesma razão — operador decide manualmente).
- **Sem evidência** — segue como candidato normal.

### 4. Avaliar e classificar os restantes

Para cada item que sobrou:

- **Alinhamento estratégico** vs `product_direction`: `alto` (menção direta ou relação clara) / `médio` (contexto geral) / `baixo` (não conectado).
- **Amplitude de toque** inferida da descrição + código existente: `ampla` (múltiplos módulos ou integração externa) / `média` (um módulo com ramificações) / `restrita` (localizada).

Combinar os dois critérios para ranking. Empate → ordem de aparição (mais antigo sobe). Mostrar o raciocínio por item — operador deve poder discordar sem aceitar caixa-preta.

### 4.5. Varrer pendências de validação em planos

Independente do ranking do top 3 (rationale diferente: fechamento de plano específico, não estratégia × amplitude). Resultado é exibido em bloco separado no passo 5; não compete no enum. **Inalterado em modo `forge`** — passo opera sobre `pr list`/`mr list` para detectar worktree/PR ativo (ortogonal ao role backlog); segue policy local pré-existente (`no-detection` skipa silente — é heurística informativa opcional, não role-declared dependency).

1. **Listar planos:** papel `plans_dir` resolvido (default `docs/plans/`); modo local lê de `.claude/local/plans/`. Sem planos → skip silente desta seção.
2. **Filtrar planos em curso:**
   - **Worktree ativa:** `git worktree list --porcelain` → paths sob `.worktrees/`; extrair slug do basename. Plano cujo slug bate é "em curso" (pendência ainda em escopo de `/run-plan` corrente).
   - **PR/MR aberto via forge auto-detect:** seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md`. Output `gh` → `gh pr list --state open --json headRefName --jq '.[].headRefName'`; output `glab` → `glab mr list --opened --output json | jq -r '.[].source_branch'`. Output `no-detection` ou `unsupported-host` → fallback (só worktree). Plano cujo slug bate em qualquer fonte ativa é "em curso".
   - Sem flag, sem cutucada — degradação silenciosa quando CLI ausente porque a filtragem é heurística informativa, não invariante crítica.
3. **Extrair `## Pendências de validação`** dos planos restantes (não-em-curso): conteúdo entre o header e o próximo `##` ou EOF. Sem seção, ou seção vazia/sem bullets ativos → pular o plano.
4. **Acumular** pares `(slug, texto-da-linha)` para cada bullet extraído. Lista vazia → omitir o bloco no passo 5.

### 5. Apresentar resultado e colher escolha

Reportar em formato curto:

- **Movidos para `## Concluídos`** (evidência forte): listar com justificativa.
- **Evidência fraca:** listar com o que foi encontrado.
- **Top 3 candidatos** em ordem decrescente de impacto, com raciocínio de alinhamento + amplitude.
- **Pendências de validação em planos** (lista do passo 4.5, quando não-vazia): bloco separado listando `<slug>: <texto da linha>` por entrada. Lista vazia → omitir o bloco. Pendências **não competem** no enum a seguir — top 3 continua sendo do BACKLOG; operador escolhe via `Other` se quiser endereçar uma pendência específica.

**Cutucada de descoberta.** Antes do enum a seguir, executar a cutucada conforme `${CLAUDE_PLUGIN_ROOT}/docs/procedures/cutucada-descoberta.md` (emitir como última linha informacional, imediatamente antes do enum).

Em seguida, enum (`AskUserQuestion`, header `Próximo`) com as 3 opções nomeadas pelo texto exato da linha + Other (operador digita intenção diferente). Escolha alimenta diretamente `/triage`.

### 6. Commit das movimentações automáticas

Disparar **apenas** se o passo 3 moveu pelo menos uma linha para `## Concluídos`. Sem movimentações → skip silente. **Skip silente também em modo `forge`** (`paths.backlog: forge`): mutações já foram aplicadas remotamente via `gh/glab issue close` cutucadas no passo 3; sem commit local. Paralelo ao skip em modo `local` (arquivo gitignored).

Mostrar ao operador a lista das linhas movidas e perguntar via enum (`AskUserQuestion`, header `Movimentações`, opções `Confirmar e commitar` / `Reverter movimentações`):

- **`Confirmar e commitar`** → em modo canonical: `git commit -m "chore(backlog): mark <N> concluded item(s)"` (mensagem segue a convenção do projeto consumidor; default canonical Conventional Commits em inglês); push não é forçado — operador pusha quando achar oportuno. Em modo `local` (`paths.backlog: local`): skip do commit (arquivo gitignored não é versionado); apenas confirmar a mutação no arquivo e seguir.
- **`Reverter movimentações`** → em modo canonical: restaurar o arquivo do papel `backlog` ao estado pré-passo-3 (`git restore <path>`). Em modo `local`: reescrever o arquivo a partir do snapshot mantido em memória pela skill (capturado no passo 1 — `git restore` não aplica a arquivo gitignored). Operador segue para o passo 7 sem mutação persistida.
- **Other** → equivalente a `Reverter movimentações` (default conservador — operador descreve intenção em prosa subsequente).

### 7. Continuar com `/triage`

Com a intenção confirmada (item escolhido ou texto livre), executar o fluxo de `/triage` a partir do passo 1 — tratando a intenção como argumento. Reaproveitar papéis já resolvidos neste fluxo.

## O que NÃO fazer

- Não apresentar mais de 3 sugestões no top.
- Não iniciar `/triage` sem escolha explícita do operador.
