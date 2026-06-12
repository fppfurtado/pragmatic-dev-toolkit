# run-plan: rebase automático ao detectar divergência de BACKLOG.md antes de publicar

## Contexto

**Linha do backlog:** /run-plan: conflito recorrente em BACKLOG.md ao fundir PR — transição final (Em andamento → Concluídos) conflita com estado divergente de main; ocorreu duas vezes; investigar se guarda pré-condição 2b cobre todos os cenários

Diagnóstico via `/debug` (sessão anterior): o conflito ocorre quando uma segunda sessão de `/triage` move um item para `## Em andamento` no main **enquanto uma feature branch de `/run-plan` está em voo**. O commit de transição final do backlog (Em andamento → Concluídos) na feature branch usa contexto de diff baseado no estado de Em andamento no momento da criação da worktree. Se main avança com outro item nessa seção, o contexto não casa no merge → conflito.

Exemplo concreto: commit `651196a` (18:26) entrou em main 8 minutos após a criação da worktree de `0ac01fc` (18:18) e 3 minutos antes do merge de `9b9c751`. A pré-condição 2b previne o caso de "triage não pushada antes de criar a worktree", mas não previne que main avance depois. A resolução do conflito é determinística quando a skill conhece a linha que está fechando — é justamente o que `**Linha do backlog:**` fornece.

## Resumo da mudança

No passo 4.7 (`Sugestão de publicação`) de `skills/run-plan/SKILL.md`, adicionar etapa de detecção de divergência em `BACKLOG.md` antes de exibir o enum `Publicar`:

1. Verificar se `origin/main` tem commits que tocam `BACKLOG.md` além do ponto de fork da feature branch.
2. Se não houver divergência: prosseguir normalmente.
3. Se houver: tentar `git rebase origin/main` na worktree e seguir o fluxo de decisão:
   - Rebase limpo → informar operador, push usa `--force-with-lease`.
   - Conflito **apenas em BACKLOG.md, seção `## Em andamento`**, e `**Linha do backlog:**` está disponível → resolver programaticamente (manter todos os itens de Em andamento do HEAD exceto a linha que está sendo fechada; mover essa linha para Concluídos), `git rebase --continue`, push usa `--force-with-lease`.
   - Qualquer outro conflito → `git rebase --abort`, aviso ao operador, enum `Publicar` sem force.

Atualizar `## O que NÃO fazer`: bullet de proibição de rebase recebe exceção explícita para este caso.

## Arquivos a alterar

### Bloco 1 — `skills/run-plan/SKILL.md` {reviewer: code}

Dois pontos de edição cirúrgica:

**1. Passo 4.7 — inserir detecção e rebase antes de verificar remote**

No início do passo 4.7, antes da verificação de remote (`git remote -v`), inserir:

> **Detecção de divergência em BACKLOG.md**: executar `git fetch origin` e verificar `git log HEAD..origin/main --oneline -- BACKLOG.md`. Sem commits → prosseguir normalmente (enum `Publicar` inalterado).
>
> Com commits (divergência detectada): tentar `git rebase origin/main` na worktree.
>
> - **Rebase limpo** (sem conflito): informar operador — `"main avançou em BACKLOG.md; rebase aplicado — push usará --force-with-lease"`. Substituir `-u` por `--force-with-lease` nas opções `Push` e `Push + abrir PR` do enum `Publicar`.
> - **Conflito apenas em BACKLOG.md, seção `## Em andamento`**, E `**Linha do backlog:**` foi capturada no início do passo 3: resolver programaticamente — (a) ler arquivo com conflict markers; (b) do lado `<<<<<<< HEAD`, extrair todos os itens de `## Em andamento`; (c) remover o item que casa exatamente com `**Linha do backlog:**`; (d) manter os demais em Em andamento; (e) adicionar o item removido ao topo de `## Concluídos`; (f) `git add BACKLOG.md && git rebase --continue`. Informar operador — `"conflito de BACKLOG.md em Em andamento resolvido automaticamente; push usará --force-with-lease"`. Substituir `-u` por `--force-with-lease` nas opções do enum `Publicar`.
> - **Qualquer outro conflito** (outros arquivos em conflito, BACKLOG.md com conflito fora de Em andamento, ou `**Linha do backlog:**` ausente): `git rebase --abort`; avisar operador — `"main divergiu em BACKLOG.md com conflito não-resolvível automaticamente — resolver manualmente antes de fundir"`. Prosseguir para o enum `Publicar` normalmente (push sem force).

**2. `## O que NÃO fazer` — atualizar bullet de rebase/merge**

Substituir:
> Não tentar resolver merge/rebase no fim — a skill não fecha o branch.

Por:
> Não tentar resolver merge/rebase no fim — a skill não fecha o branch. Exceção: divergência de BACKLOG.md detectada antes da sugestão de publicação (passo 4.7) — nesse caso, `git rebase origin/main` é executado automaticamente e o conflito de `## Em andamento` é resolvido programaticamente quando: (i) o único arquivo em conflito é BACKLOG.md; (ii) o conflito está restrito à seção `## Em andamento`; (iii) `**Linha do backlog:**` foi capturada. Qualquer outra situação: `git rebase --abort` e aviso ao operador.

## Verificação end-to-end

Não aplicável — este repo é o plugin (sem `test_command`). Gate é a `## Verificação manual`.

## Verificação manual

Em projeto-fixture com este plugin instalado:

1. **Sem divergência**: rodar `/run-plan` até done com main limpo. Confirmar: enum `Publicar` sem mensagem de rebase, push usa `-u`.
2. **Divergência sem conflito** (rebase limpo): após criar worktree, adicionar commit em main tocando BACKLOG.md em seção diferente de Em andamento (ex.: nova linha em Próximos). Confirmar: mensagem `"main avançou em BACKLOG.md; rebase aplicado"`, enum `Publicar` usa `--force-with-lease`.
3. **Divergência com conflito em Em andamento resolvível**: simular o cenário do bug — segunda sessão de `/triage` adiciona item em Em andamento enquanto a feature branch está em voo. Confirmar: mensagem de resolução automática; BACKLOG.md resultante tem o item correto em Concluídos e o novo item de Em andamento mantido; push usa `--force-with-lease`.
4. **Divergência com conflito não-resolvível** (outros arquivos): adicionar commit em main que conflita com a feature branch em arquivo não-BACKLOG. Confirmar: `git rebase --abort` executado; aviso ao operador; enum `Publicar` normal (sem force).
5. **`**Linha do backlog:**` ausente**: repetir cenário 3 em plano sem o campo. Confirmar: trata como caso 4 — `git rebase --abort`, aviso ao operador, sem tentativa de resolução automática.

## Notas operacionais

- `--force-with-lease` é seguro: verifica que o branch remoto não foi atualizado por outro processo entre leitura e escrita. Se o branch remoto mudou, o push falha esperadamente — operador resolve.
- Se o PR já foi aberto antes do push (operador escolheu `Push + abrir PR` em run anterior), o `--force-with-lease` atualiza o PR existente no GitHub automaticamente.
- A resolução programática assume que o match com `**Linha do backlog:**` é **exato** (mesma política do passo 3 e 4.4). Match parcial ou fuzzy não é tentado — qualquer ambiguidade cai no caso "não-resolvível".
