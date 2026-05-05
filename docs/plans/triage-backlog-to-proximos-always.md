# triage-backlog-to-proximos-always

## Contexto

O merge artifact no BACKLOG.md ocorre porque o commit de triage (que move o item para Em andamento em `main`) não era empurrado ao remote antes da criação do branch da feature. O GitHub mergeava o PR sem conhecer esse commit — quando o operador fazia `git pull`, o git reconciliava dois estados divergentes e mantinha a linha de Em andamento como artefato.

Fix (Opção B): manter a semântica atual (triage escreve Em andamento em `main`), mas garantir que main seja empurrado ao remote antes de o `/run-plan` criar a worktree. Toda a movimentação do backlog continua acontecendo nos dois lados, mas o GitHub sempre tem o estado correto como base.

**Linha do backlog:** /triage + /run-plan: merge artifact no BACKLOG.md — transição Em andamento gravada no commit de triage (main) reaparece após merge do PR; investigar postergação da transição para o branch da feature

## Resumo da mudança

Três adições coordenadas:

1. `/triage` passo 6 — após commit confirmado com caminho-plano, empurrar main ao remote antes de sugerir o próximo passo.
2. `/run-plan` pré-condições — verificar se main está à frente do remote quando BACKLOG.md contém linha em `## Em andamento`; bloquear e orientar o operador a empurrar antes de criar a worktree.
3. `docs/philosophy.md` → "Ciclo de vida do backlog" — adicionar nota sobre o push requirement na transição Próximos → Em andamento.

## Arquivos a alterar

### Bloco 1 — `skills/triage/SKILL.md` {reviewer: code}

No **passo 6** (Reportar, propor commit e devolver controle), após o commit ser confirmado e executado:

Adicionar etapa: se o caminho incluiu plano (e portanto gravou a linha em `## Em andamento`), empurrar main ao remote imediatamente — `git push origin <branch-atual>`. Sem o push, o `/run-plan` criará o branch da feature a partir de um estado que o remote não conhece, e o merge do PR produzirá merge artifact no BACKLOG.md.

Posicionamento: após a confirmação do commit e antes de sugerir o próximo passo. O push é obrigatório nesse caminho — não é proposta ao operador.

### Bloco 2 — `skills/run-plan/SKILL.md` {reviewer: code}

Na **pré-condição 2** (Estado git dos artefatos de alinhamento), adicionar terceira camada de verificação após as duas existentes:

**Bloquear** se `git status --porcelain` estiver limpo mas `git log origin/<branch>..HEAD` mostrar commits à frente do remote E o arquivo do papel `backlog` contiver linha em `## Em andamento` — sinal de que o triage commit não foi empurrado. Mensagem ao operador: empurrar main antes de criar a worktree (`git push`) para evitar merge artifact no BACKLOG.md após integração do PR. Não contornar criando a worktree mesmo assim.

### Bloco 3 — `docs/philosophy.md` {reviewer: code}

Na seção **"Ciclo de vida do backlog"**, bullet `Próximos → Em andamento`:

Acrescentar ao final: "Para que o merge do PR seja limpo, o commit de triage deve ser empurrado ao remote antes da criação do branch da feature — `/triage` faz esse push automaticamente no passo 6 após confirmação do commit."

## Verificação end-to-end

Verificação textual (sem test suite):

1. Confirmar que o passo 6 de `/triage` inclui o push obrigatório após commit com caminho-plano.
2. Confirmar que a pré-condição 2 de `/run-plan` bloqueia quando main está à frente do remote com Em andamento no backlog.
3. Confirmar que `docs/philosophy.md` menciona o push requirement no bullet Próximos → Em andamento.
4. Verificar que nenhuma outra parte dos skills foi alterada fora do escopo.
