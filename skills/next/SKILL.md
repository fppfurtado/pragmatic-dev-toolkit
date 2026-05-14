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

## Passos

### 1. Ler o backlog

Ler o arquivo na íntegra. Extrair `## Próximos` — candidatos a analisar. Em modo `local` (`paths.backlog: local`), arquivo é `.claude/local/BACKLOG.md` (resolvido pelo Resolution protocol do CLAUDE.md); skill segue agnóstica ao path.

`## Próximos` vazio → informar e interromper.

### 2. Selecionar candidatos

Pegar os **seis primeiros** itens de `## Próximos` em ordem de aparição (topo = mais antigo). Seis dá margem para descartar implementados e ainda chegar a três finais.

### 3. Verificar implementação no código

Para cada candidato, buscar evidência no repo (funções, endpoints, modelos, comandos, fluxos correspondentes). Classificar:

- **Evidência forte** — código claro e diretamente mapeável (ex.: item "exportar movimentos em CSV" → handler de export CSV presente e funcional). Preparar movimentação da linha para `## Concluídos` (escrever no arquivo) e reportar com justificativa de 1 linha. Commit fica para o passo 6.
- **Evidência fraca** — código parcial, feature similar com escopo diferente, ou inferência incerta. Reportar o que foi encontrado; **não mover** — operador decide.
- **Sem evidência** — segue como candidato normal.

### 4. Avaliar e classificar os restantes

Para cada item que sobrou:

- **Alinhamento estratégico** vs `product_direction`: `alto` (menção direta ou relação clara) / `médio` (contexto geral) / `baixo` (não conectado).
- **Amplitude de toque** inferida da descrição + código existente: `ampla` (múltiplos módulos ou integração externa) / `média` (um módulo com ramificações) / `restrita` (localizada).

Combinar os dois critérios para ranking. Empate → ordem de aparição (mais antigo sobe). Mostrar o raciocínio por item — operador deve poder discordar sem aceitar caixa-preta.

### 4.5. Varrer pendências de validação em planos

Independente do ranking do top 3 (rationale diferente: fechamento de plano específico, não estratégia × amplitude). Resultado é exibido em bloco separado no passo 5; não compete no enum.

1. **Listar planos:** papel `plans_dir` resolvido (default `docs/plans/`); modo local lê de `.claude/local/plans/`. Sem planos → skip silente desta seção.
2. **Filtrar planos em curso:**
   - **Worktree ativa:** `git worktree list --porcelain` → paths sob `.worktrees/`; extrair slug do basename. Plano cujo slug bate é "em curso" (pendência ainda em escopo de `/run-plan` corrente).
   - **PR/MR aberto via forge auto-detect** (mesmo padrão do `/run-plan §3.7`): parse `git remote get-url origin`. `github.com` → `gh pr list --state open --json headRefName --jq '.[].headRefName'`. Host casando regex `^gitlab\.` → `glab mr list --opened`. Outros hosts ou CLI ausente → fallback (só worktree). Plano cujo slug bate em qualquer fonte ativa é "em curso".
   - Sem flag, sem cutucada — degradação silenciosa quando CLI ausente porque a filtragem é heurística informativa, não invariante crítica.
3. **Extrair `## Pendências de validação`** dos planos restantes (não-em-curso): conteúdo entre o header e o próximo `##` ou EOF. Sem seção, ou seção vazia/sem bullets ativos → pular o plano.
4. **Acumular** pares `(slug, texto-da-linha)` para cada bullet extraído. Lista vazia → omitir o bloco no passo 5.

### 5. Apresentar resultado e colher escolha

Reportar em formato curto:

- **Movidos para `## Concluídos`** (evidência forte): listar com justificativa.
- **Evidência fraca:** listar com o que foi encontrado.
- **Top 3 candidatos** em ordem decrescente de impacto, com raciocínio de alinhamento + amplitude.
- **Pendências de validação em planos** (lista do passo 4.5, quando não-vazia): bloco separado listando `<slug>: <texto da linha>` por entrada. Lista vazia → omitir o bloco. Pendências **não competem** no enum a seguir — top 3 continua sendo do BACKLOG; operador escolhe via `Other` se quiser endereçar uma pendência específica.

**Cutucada de descoberta** (per [ADR-017](../../docs/decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md) + [ADR-029](../../docs/decisions/ADR-029-cutucada-descoberta-cobre-claude-md-ausente.md)). Antes do enum a seguir, escolher caminho conforme estado de `CLAUDE.md`:

- **`CLAUDE.md` ausente** + a string abaixo não aparece no contexto visível desta conversa CC → emitir como última linha do relatório (antes do enum):
  > Dica: este projeto não tem `CLAUDE.md`. Crie o arquivo e rode `/init-config` para configurar os papéis do plugin.
- **`CLAUDE.md` presente** + `grep -q '<!-- pragmatic-toolkit:config -->' CLAUDE.md` retorna não-zero (marker ausente) + a string abaixo não aparece no contexto visível → emitir como última linha do relatório (antes do enum):
  > Dica: este projeto não declara o bloco `pragmatic-toolkit:config` no CLAUDE.md. Rode `/init-config` para configurar todos os papéis de uma vez.
- **`CLAUDE.md` presente com marker** OU **dedup hit na string aplicável** → suprimir silenciosamente.

Em seguida, enum (`AskUserQuestion`, header `Próximo`) com as 3 opções nomeadas pelo texto exato da linha + Other (operador digita intenção diferente). Escolha alimenta diretamente `/triage`.

### 6. Commit das movimentações automáticas

Disparar **apenas** se o passo 3 moveu pelo menos uma linha para `## Concluídos`. Sem movimentações → skip silente.

Mostrar ao operador a lista das linhas movidas e perguntar via enum (`AskUserQuestion`, header `Movimentações`, opções `Confirmar e commitar` / `Reverter movimentações`):

- **`Confirmar e commitar`** → em modo canonical: `git commit -m "chore(backlog): mark <N> concluded item(s)"` (mensagem segue a convenção do projeto consumidor; default canonical Conventional Commits em inglês); push não é forçado — operador pusha quando achar oportuno. Em modo `local` (`paths.backlog: local`): skip do commit (arquivo gitignored não é versionado); apenas confirmar a mutação no arquivo e seguir.
- **`Reverter movimentações`** → em modo canonical: restaurar o arquivo do papel `backlog` ao estado pré-passo-3 (`git restore <path>`). Em modo `local`: reescrever o arquivo a partir do snapshot mantido em memória pela skill (capturado no passo 1 — `git restore` não aplica a arquivo gitignored). Operador segue para o passo 7 sem mutação persistida.
- **Other** → equivalente a `Reverter movimentações` (default conservador — operador descreve intenção em prosa subsequente).

### 7. Continuar com `/triage`

Com a intenção confirmada (item escolhido ou texto livre), executar o fluxo de `/triage` a partir do passo 1 — tratando a intenção como argumento. Reaproveitar papéis já resolvidos neste fluxo.

## O que NÃO fazer

- Não apresentar mais de 3 sugestões no top.
- Não iniciar `/triage` sem escolha explícita do operador.
