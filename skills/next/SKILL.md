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

Conteúdo substantivo já carregado na conversa por skills anteriores (ex.: saída de `/journal-load`) ou citado pelo operador entra na análise de ranking com a mesma semântica do `NOTES.md` acima — sem disparar novo `Read` sobre fontes já presentes no contexto. Reportar a fonte concreta (ex.: `journal 2026-06-18`, citação do operador) quando influenciou o ranking. Informational; nunca bloqueia.

### 2. Selecionar candidatos

Pegar os **`N` primeiros** itens de `## Próximos` em ordem de aparição (topo = mais antigo). Default `N = 10` (override por invocação via argumento posicional — ver `## Argumentos`) dá margem para descartar implementados e ainda chegar a três finais. Em modo `forge`, ordem natural é `createdAt` ascendente (lista já vem ordenada do passo 1); filtro `N` aplicado post-hoc sobre a lista do passo 1.

### 3. Verificar implementação no código

Para cada candidato, buscar evidência no repo (funções, endpoints, modelos, comandos, fluxos correspondentes). Classificar em **evidência forte** / **evidência fraca** / **sem evidência** (semântica detalhada abaixo).

**Caminho de verificação por `N`** (per [ADR-059](../../docs/decisions/ADR-059-subagent-em-loop-interno-de-skill-per-item-probe-threshold.md)):

- **`N < 5` (caminho serial):** main thread varre o codebase via grep/glob direto para cada candidato, em ordem. Cold-start de subagent perde para varredura local quando o volume é pequeno.
- **`N ≥ 5` (caminho paralelo):** spawn de **1 subagent `Explore` por candidato** em **único turno** (batch de tool calls paralelas). Cada subagent retorna o verdict do seu candidato. Main thread aguarda todos os retornos antes de classificar. Latência total ≈ max(individual) em vez de soma; cold-start replicado mas amortizado pelo paralelismo.

**Contrato do subagent (caminho paralelo).** Prompt curto e self-contained — subagent é frio, não tem contexto da conversa principal.

- **Input por subagent:**
  - Descrição do plugin/projeto em 1 linha (ex.: "Plugin Claude Code 'pragmatic-dev-toolkit' que ship skills/agents/hooks como markdown + scripts Python curtos.").
  - Linha literal do candidato (texto integral do bullet).
  - Instruções de classificação (3 saídas mutuamente exclusivas):
    - **`forte`** — código diretamente mapeável (handler, função, comando, fluxo concretamente presente e funcional). Exige `path:line` da evidência principal.
    - **`fraca`** — código parcial, feature similar com escopo diferente, inferência incerta. Descrever o que foi encontrado.
    - **`sem`** — busca direcionada não retornou evidência substantiva.
- **Output por subagent** (texto curto estruturado):

  ```
  verdict: <forte|fraca|sem>
  path: <path:line ou vazio>
  justificativa: <1 linha>
  ```

- **Falha do subagent** (timeout, erro, output malformado): main thread assume `verdict: sem` para esse candidato + warning reportado; **não bloqueia** outros candidatos.

**Classificação (mesma semântica em ambos os caminhos):**

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

### 4.6. Varrer planos em aberto

Paralelo ao passo 4.5 (orientação sessional sobre planos em estado `Pendente`/`Abortado`). Planos `Pendente` competem no enum top-3 com BACKLOG sob regra de composição cap-2 (passo 5); planos `Abortado` permanecem visíveis somente no bloco informativo **Planos em aberto** no passo 5. Ortogonal ao bloco de pendências de validação (§4.5). Consome heurística de completude codificada em [ADR-060](../../docs/decisions/ADR-060-heuristica-completude-planos-via-status.md) — campo `## Status` no body do plano complementar a git/forge per ADR-060 § Modelo de signal. `Em execução` e `Concluído` derivados de git/forge não geram entrada aqui (sem ação pendente do operador).

1. **Listar planos não-em-curso:** reusar a saída do passo 4.5 (papel `plans_dir` resolvido + filtro em curso via worktree-active + PR/MR aberto). Sem planos → skip silente desta seção.
2. **Classificar por estado per ADR-060 § Modelo de signal:** para cada plano não-em-curso, ler valor após o header `## Status` no body — `awk '/^## Status$/{flag=1; next} flag && NF{print; exit}' <plans_dir>/<slug>.md` (skip da blank line canonical entre header e valor). Classificar:
   - **`Pendente`** — valor == `Pendente`.
   - **`Abortado`** — valor == `Abortado`.
   - **Outros** (field ausente, valor não-canonical, ou estado derivado `Em execução`/`Concluído` via git/forge) → skip silente (sem ação pendente do operador).
3. **Acumular** tuplas `(slug, estado, mtime)` para Pendente e Abortado, ordenadas por `(estado: Pendente > Abortado, mtime: desc, slug: asc)`. `mtime` lido via `stat -c '%Y' <plans_dir>/<slug>.md` (proxy para "trigger mais quente"; rebase/sync podem resetar — limitação aceitável). Lista vazia → omitir o bloco informativo no passo 5; top-3 segue só do BACKLOG.

### 5. Apresentar resultado e colher escolha

Reportar em formato curto:

- **Movidos para `## Concluídos`** (evidência forte): listar com justificativa.
- **Evidência fraca:** listar com o que foi encontrado.
- **Top 3 candidatos**: composição em ordem decrescente de impacto = primeiros `min(N_Pendente, 2)` planos `Pendente` (ordenação do §4.6) + restante do BACKLOG (ranking do passo 4). N_Pendente=0 → 3 BACKLOG (status quo). N_Pendente=1 → 1 plano + 2 BACKLOG. N_Pendente≥2 → 2 planos + 1 BACKLOG. BACKLOG mantém ≥1 slot sempre. Mostrar o raciocínio por item — operador deve poder discordar sem aceitar caixa-preta. Enum exibe `<slug>` literal como label da opção `/run-plan <slug>` quando vem de plano `Pendente` (`description` da opção carrega `Plano em aberto: Pendente`); texto da linha quando vem do BACKLOG.
- **Pendências de validação em planos** (lista do passo 4.5, quando não-vazia): bloco separado listando `<slug>: <texto da linha>` por entrada. Lista vazia → omitir o bloco. Pendências **não competem** no enum a seguir — top 3 continua sendo do BACKLOG; operador escolhe via `Other` se quiser endereçar uma pendência específica.
- **Planos em aberto** (bloco informativo): lista todos os `Abortado` + planos `Pendente` residuais (além do cap-2 do top-3, quando aplicável), na ordenação do §4.6. Operador escolhe via `Other` se quiser priorizar um `Abortado` ou um `Pendente` residual específico (ex.: `/run-plan <slug>`). Bloco omitido quando lista vazia (nenhum `Abortado` E N_Pendente ≤ 2).

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

- Não apresentar mais de 3 opções nomeadas no enum (Other é automático e fora do cap).
- Não iniciar `/triage` sem escolha explícita do operador.
- Não paralelizar quando `N < 5` — cold-start de subagent perde para grep direto do main thread (per [ADR-059](../../docs/decisions/ADR-059-subagent-em-loop-interno-de-skill-per-item-probe-threshold.md)).
