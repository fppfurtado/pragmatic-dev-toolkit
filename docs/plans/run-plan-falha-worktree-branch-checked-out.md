# Plano — /run-plan §1.1 cobre falha por branch já checked out em outro worktree

## Contexto

`skills/run-plan/SKILL.md` §1.1 (setup da worktree) cobre falha de `git worktree add` com lista parentética exemplificativa (`branch inexistente, digitação errada, refs não-fetchadas`) e mensagem padronizada no backlog em `... não existe — verificar nome ou rodar git fetch antes de re-executar`. A redação não cobre o caso real "branch alvo já está checked out em outro worktree" — caracteristicamente o working tree principal quando o operador editou o plano após fazer checkout da branch da issue (fluxo issue-first do [ADR-028](../decisions/ADR-028-campo-branch-opcional-plano-fluxo-issue-first.md)).

Em sessão real no consumer `connector-pje-mandamus-tjpa` (slug `corrigir-conflito-fallthrough`, 2026-05-14), `git worktree add .worktrees/<slug> <branch>` falhou com `fatal: '<branch>' is already used by worktree at '<principal>'`. O agente leu a lista parentética como exaustiva, **improvisou `git checkout master`** no repo principal **sem `git status` prévio** e re-tentou o `git worktree add` com sucesso — sem escrever no backlog, sem parar. `git checkout` no working tree principal é ação de blast-radius compartilhado: troca o branch ativo do operador, podendo sobrescrever uncommitted work; CLAUDE.md global proíbe esse tipo de improviso ("destructive operations… check with the user before proceeding").

Correção é editorial: refinar §1.1 para discriminar o caso e reforçar "informar e parar, não improvisar" no `## O que NÃO fazer`.

**ADRs candidatos:** ADR-028 (feature do campo `**Branch:**` que tornou o cenário comum); ADR-002 (filosofia de bloqueio in situ vs warning).

**Linha do backlog:** plugin: `/run-plan §1.1` cobre falha de `git worktree add` por branch já checked out em outro worktree — refinar prosa para discriminar caso (mensagem do backlog específica nomeando o worktree onde a branch está) + reforçar "informar e parar, não improvisar `git checkout` no working tree principal" no `## O que NÃO fazer`. Gap detectado em sessão real do consumer `connector-pje-mandamus-tjpa`: agente leu lista parentética como exaustiva e improvisou `git checkout master` sem `git status` prévio (ação de blast-radius compartilhado).

## Resumo da mudança

Reformular o bullet "Falha de criação" do §1.1 do `skills/run-plan/SKILL.md` para listar quatro categorias de causa raiz com mensagem de backlog específica por categoria: (a) branch inexistente / refs não-fetchadas (caso atual); (b) branch já checked out em outro worktree (caso novo); (c) outras falhas (catch-all com `<stderr>` literal); (d) diretório `.worktrees/<slug>/` já existe sem registro git (race com sessão paralela ou execução interrompida — pré-condição 4 cobre o comum upstream, sub-bullet aqui dá simetria editorial). Adicionar bullet em `## O que NÃO fazer` proibindo recovery automática que altere estado externo ao plugin (working tree principal, refs locais).

Sincronizar com [ADR-028](../decisions/ADR-028-campo-branch-opcional-plano-fluxo-issue-first.md) § Mecânica (status `Proposto`, autoriza edit editorial in-place): atualizar o bullet "Falha em criar worktree" para refletir as 4 categorias. ADR e SKILL ficam sincronizados sem ADR sucessor.

Sem mudança de comportamento doutrinário (continua "informar e parar"); o que muda é a discriminação textual dos casos (b) e (d) e a proibição explícita do anti-padrão observado.

**Decisões registradas no plano:**

- Categoria (c) "outras falhas" tem **só verificação textual** em `## Verificação end-to-end` (formatação de `<stderr>` literal é trivial; cenário live em `## Verificação manual` seria over-test).
- Mensagem do backlog para (b) nomeia `<path>` literal extraído da stderr, sem detectar se é working tree principal ou secundária. Granularidade "principal vs secundária" considerada e rejeitada por YAGNI — `<path>` informa suficientemente; operador identifica o contexto.

## Arquivos a alterar

### Bloco 1 — `skills/run-plan/SKILL.md` {reviewer: code}

- §1.1 do passo "Setup da worktree": substituir o bullet "Falha de criação (branch inexistente, digitação errada, refs não-fetchadas) → escrever em `## Próximos` do `backlog` linha tipo `branch <nome> referenciada em **Branch:** do plano <slug> não existe — verificar nome ou rodar git fetch antes de re-executar`; informar; parar. Papel `backlog` = "não temos" → só informar." por enumeração discriminando quatro categorias:
  - **Branch inexistente / digitação errada / refs não-fetchadas** (`fatal: invalid reference: <nome>` ou similar): mensagem do backlog mantém o texto atual (`... não existe — verificar nome ou rodar git fetch antes de re-executar`).
  - **Branch já checked out em outro worktree** (`fatal: '<nome>' is already used by worktree at '<path>'`): mensagem do backlog nomeia o worktree concreto e instrui o operador — `branch <nome> referenciada em **Branch:** do plano <slug> está checked out em <path> — fazer checkout de outra branch lá antes de re-executar`.
  - **Diretório `.worktrees/<slug>/` já existe sem registro git** (`fatal: '.worktrees/<slug>' already exists` ou similar; race com sessão paralela ou execução interrompida que escapou da pré-condição 4): mensagem do backlog — `diretório .worktrees/<slug>/ existe mas não está registrado como worktree git — remover manualmente antes de re-executar`.
  - **Outras falhas**: linha descritiva com o erro literal (`falha em git worktree add para <nome> do plano <slug>: <stderr>` — operador investiga manual).
  
  Todos os quatro caminhos: informar; parar. Papel `backlog` = "não temos" → só informar.

- `## O que NÃO fazer`: adicionar bullet proibindo recovery automática em falha do §1.1. Forma: liderar com o critério (não com a enumeração — o gap que motivou este plano foi precisamente lista parentética lida como exaustiva). Redação proposta: *Não emitir comando que altere estado externo ao escopo do plugin (working tree principal, refs locais, branches de terceiros) para contornar falha de `git worktree add` — incluindo mas não limitado a `git checkout`/`git switch` no principal, `git branch -D`, `git worktree remove`, `git reset --hard`. Doutrina é parar e escrever no backlog; CLAUDE.md global exige confirmação explícita para ações de blast-radius compartilhado, e este SKILL não autoriza recovery silenciosa.*

### Bloco 2 — `docs/decisions/ADR-028-...md` {reviewer: code}

- § Mecânica → bullet "Falha em criar worktree (branch inexistente, digitação errada) → ..." (linha 56): substituir por enumeração das 4 categorias idêntica à do SKILL (caminho (a), (b), (c), (d) do Bloco 1). Status `Proposto` autoriza edit editorial in-place sem ADR sucessor. Manter o restante do ADR inalterado (Status, Origem, Decisão, Razões, Trade-offs, Limitações, Alternativas, Gatilhos).

## Verificação end-to-end

- `grep -n "Falha de criação" skills/run-plan/SKILL.md` localiza o header do bullet.
- Logo abaixo, 4 sub-bullets distintos discriminam causas (inexistente / checked out em outro worktree / dir órfão / outras).
- `grep -nE "already used by worktree|checked out em" skills/run-plan/SKILL.md` retorna match em §1.1.
- `grep -nE "already exists|registrado como worktree" skills/run-plan/SKILL.md` retorna match em §1.1.
- `grep -nE "alter[ae] estado externo|blast-radius compartilhado" skills/run-plan/SKILL.md` retorna match em `## O que NÃO fazer`.
- `grep -n "Falha em criar worktree" docs/decisions/ADR-028-*.md` localiza o bullet refinado.
- Abaixo dele, mesma enumeração das 4 categorias do SKILL (texto idêntico aceitável).

## Verificação manual

Cenário único — reproduz o gap original em ambiente controlado:

1. Em consumer com `/run-plan` instalado, criar plano `docs/plans/<slug-de-teste>.md` contendo no `## Contexto` o campo `**Branch:** <branch-existente>`.
2. No working tree **principal** do consumer, `git checkout <branch-existente>` (deixa a branch ocupada).
3. Garantir working tree principal limpo (`git status --porcelain` vazio) para isolar o teste do anti-padrão de uncommitted work.
4. Invocar `/run-plan <slug-de-teste>`.
5. Confirmar:
   - Setup falha com mensagem específica nomeando o working tree principal como dono atual da branch.
   - Linha gravada em `## Próximos` do `backlog` (ou só relato se papel "não temos") segue o template `branch <nome> ... está checked out em <path> — fazer checkout de outra branch lá antes de re-executar`.
   - Skill **para**. Não há `git checkout`, `git branch -D`, retry de `git worktree add` ou qualquer outra ação automática.
   - `git rev-parse --abbrev-ref HEAD` no principal retorna `<branch-existente>` (estado preservado, não trocado para `main`/`master`).

Cenário negativo (regressão do caso atual): plano com `**Branch:** branch-que-nao-existe`. Setup falha; mensagem do backlog usa o texto atual (`... não existe ...`); skill para. Confirma que o refactor não quebrou o caminho original.
