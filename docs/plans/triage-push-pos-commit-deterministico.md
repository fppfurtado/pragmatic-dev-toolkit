# /triage: push pós-commit determinístico no caminho-com-plano

## Contexto

`/debug` no item de backlog isolou a causa-raiz da não-confiabilidade do push automático em `/triage`: o passo 6 da skill (`skills/triage/SKILL.md:115`) prescreve o push em **prosa intercalada**, sem amarra mecânica ao commit. Concretamente:

- O gate `AskUserQuestion` (header `Commit`, opções `Confirmar e commitar` / `Editar mensagem`) na linha 111 cobre apenas o commit.
- O parágrafo da linha 115 ("Quando o caminho incluiu plano… empurrar main ao remote") fica entre dois parágrafos prosaicos ("Por que o commit importa" linha 113 e "Por fim, sugerir o próximo passo" linha 117).
- Não há (a) chamada `Bash` única `git commit … && git push …`, (b) gate `AskUserQuestion` específico para o push, (c) hook `PostToolUse` que dispare por inferência de estado.

Confiabilidade depende inteiramente de o agente reconhecer a condição em runtime e lembrar do parágrafo após o gate de commit. Falha visível é merge artifact em `BACKLOG.md` após PR (já flagado nos commits c176ac4 e 17e4d26 da árvore). Mitigação parcial existente: `/run-plan` bloqueia se `main` está à frente do `origin` com linha em `## Em andamento` (`docs/philosophy.md:182`), mas só pega o sintoma após o salto para execução.

Decisão técnica (do `/debug`): consolidar commit+push num único `Bash` com `git commit -m "…" && git push origin <branch-atual>` quando o caminho inclui plano. O gate `Commit` continua sendo o único ponto de confirmação — o operador confirma a unidade `commit+push`, não duas decisões. Caminhos sem plano (linha-só, ADR-only, atualização pura de domain/design) seguem fazendo só o commit, sem push.

**Linha do backlog:** /triage: push automático pós-commit não é executado de forma confiável — verificar condições de disparo

## Resumo da mudança

1. Em `skills/triage/SKILL.md` passo 6: reescrever a descrição do gate `Commit` e remover o parágrafo separado da linha 115. Texto novo deve declarar explicitamente que (a) caminho-com-plano consolida commit+push num único shell call, (b) caminho-sem-plano executa só o commit, (c) o gate `Commit` cobre a unidade composta no caminho-com-plano. A confirmação `Confirmar e commitar` é o único ponto de cerimônia.
2. Em `docs/philosophy.md`: ajustar a frase da linha 182 ("`/triage` faz esse push automaticamente no passo 6") para refletir a nova mecânica de unidade atômica commit+push, mantendo a invariante operacional ("commit de triage com transição Próximos → Em andamento deve estar empurrado antes da criação do branch da feature").

Sem mudança de comportamento para `/run-plan`, hooks ou outras skills.

## Arquivos a alterar

### Bloco 1 — skills/triage/SKILL.md {reviewer: code,security}

- Reescrever os parágrafos do passo 6 que tratam de commit e push (linhas 111–115).
- Texto novo deve preservar o gate `AskUserQuestion` (header `Commit`, opções `Confirmar e commitar` / `Editar mensagem`).
- Texto novo deve declarar explicitamente: caminho-com-plano → single shell call `git commit -m "…" && git push origin <branch-atual>`; caminho-sem-plano → só `git commit`.
- Texto novo deve preservar a justificativa atual ("`/run-plan` cria worktree a partir do HEAD…") e acrescentar a justificativa do push consolidado (eliminar a janela de esquecimento entre commit e push, evitar merge artifact em `BACKLOG.md`).
- Atualizar a seção `## O que NÃO fazer` se a regra atual ("Não commitar os artefatos de alinhamento sem confirmação explícita do operador — propor mensagem e aguardar") precisar de ajuste para refletir que a confirmação cobre commit+push no caminho-com-plano.

Revisor `security` é solicitado por causa do I/O externo (autenticação remota, possível leak de credencial em mensagens de erro, post-error invariants quando push falha após commit já feito).

### Bloco 2 — docs/philosophy.md {reviewer: code}

- Linha 182, sub-item `Próximos → Em andamento`: trocar a frase "`/triage` faz esse push automaticamente no passo 6" por descrição precisa do gate consolidado ("`/triage` consolida commit + push num único shell call no passo 6 quando o caminho inclui plano; a confirmação do gate `Commit` cobre a unidade").
- Não tocar o resto do parágrafo (mecânica do `/run-plan` que bloqueia se main está à frente do remote permanece igual).

## Verificação manual

Repo não tem `test_command` (`CLAUDE.md` declara `test_command: null`). Validação é dogfood — exercitar a skill modificada em cenários concretos. Como a mudança toca **comportamento de agente LLM** (instruções na skill markdown), os cenários a exercitar são enumerados:

1. **Caminho-com-plano (caso golden):** rodar `/triage` numa próxima intenção que produza plano. Observar: o gate `Commit` aparece com mensagem indicando que a confirmação cobre commit+push; após `Confirmar e commitar`, o agente executa **um único** `Bash` cujo comando contém `git commit -m "…" && git push origin <branch-atual>`; output mostra ambos os passos com sucesso; `git log origin/main..main` retorna vazio imediatamente após. Verificar que `/run-plan <slug>` subsequente não dispara o guard "main à frente do remote".
2. **Caminho-sem-plano (linha-só):** rodar `/triage` numa intenção pequena que vire só linha em `## Próximos`. Observar: gate `Commit` aparece sem menção a push; após confirmação, só o commit é feito; `git log origin/main..main` mostra o commit local não-empurrado. Operador empurra manualmente depois (ou não — caminho-sem-plano não exige push).
3. **Caminho ADR-only delegado a `/new-adr`:** confirmar que nada do passo 6 dispara commit ou push (a skill já pula esta etapa quando delega para `/new-adr`, que faz seu próprio commit).
4. **Cenário negativo — push falha:** num clone temporário, configurar `git remote set-url origin <url-inválida>` e rodar `/triage` num caminho-com-plano. Observar: o `Bash` único reporta o commit com sucesso e o push com falha (rede/auth); o agente comunica visivelmente a falha; operador pode `git push` manual quando o problema for resolvido. Verificar que **não há retry silente** nem mascaramento do erro do push.

## Notas operacionais

- A linha em `## Próximos` que motivou este plano é movida para `## Em andamento` por `/triage` no passo 4 (transição automática do caminho-com-plano).
- **Ironia consciente:** o commit deste próprio plano ainda passa pelo passo 6 atual da skill (push em prosa, não consolidado). O agente desta sessão precisa **lembrar** de empurrar manualmente após o commit. Após o merge do PR que aplicar este plano, o próximo `/triage` em caminho-com-plano já usará o gate consolidado.
