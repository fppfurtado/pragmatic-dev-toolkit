# run-plan: sugerir push e abertura de PR ao final

## Contexto

Ao encerrar o `/run-plan`, o operador precisa decidir manualmente o que fazer com o branch da worktree. A skill hoje declara done e devolve o controle sem oferecer o próximo passo natural de publicação — causando atrito no fluxo normal.

**Linha do backlog:** `/run-plan: sugerir push e abertura de PR ao final, além do commit (quando aplicável)`

## Resumo da mudança

Após o passo 4.6 (declarar done), verificar se há remote configurado para o branch da worktree. Se sim, perguntar ao operador via `AskUserQuestion` (header `Publicar`) com três opções:

- **Push** — empurrar o branch para o remote (`git push -u origin <branch>`).
- **Push + abrir PR** — empurrar e executar `gh pr create`.
- **Nenhum** — encerrar sem ação adicional.

Se não houver remote, pular silenciosamente.

A sentença final atual ("Caminho de fechamento (PR, merge, descarte) é decisão do operador.") é atualizada para refletir o novo comportamento.

## Arquivos a alterar

### Bloco 1 — `skills/run-plan/SKILL.md` {reviewer: code}

**1. Adicionar passo 7** entre `6. **Declarar done**.` e a sentença final:

```
7. **Sugestão de publicação** — verificar se há remote configurado (`git remote -v`). Se houver, perguntar ao operador via `AskUserQuestion` (header `Publicar`) com opções:
   - `Push` — executar `git push -u origin <branch-atual>`.
   - `Push + abrir PR` — executar `git push -u origin <branch-atual>` seguido de `gh pr create`.
   - `Nenhum` — encerrar sem ação.
   Se não houver remote, pular silenciosamente.
```

**2. Substituir a sentença final:**

De: `A skill termina na worktree com branch da feature. Caminho de fechamento (PR, merge, descarte) é decisão do operador.`

Para: `A skill termina na worktree com branch da feature após oferecer publicação ao operador.`

**3. Adicionar ao final de `## O que NÃO fazer`:**

- Não executar push ou abrir PR sem confirmação explícita via enum `Publicar`.
- Não exibir o enum `Publicar` quando não há remote configurado — skip silente.

## Verificação manual

1. Instalar o plugin localmente (`/plugin install /path/to/pragmatic-dev-toolkit --scope project`) num projeto com remote configurado.
2. Rodar `/run-plan` num plano simples de 1 bloco.
3. Após "done", verificar que o enum `Publicar` aparece com as três opções.
4. Escolher `Push` e confirmar que o branch é empurrado ao remote.
5. Repetir escolhendo `Push + abrir PR` e confirmar que `gh pr create` é executado.
6. Escolher `Nenhum` e confirmar que a skill encerra sem ação.
7. Repetir num repositório sem remote configurado e confirmar que o enum não aparece.
