# ADR-004: State-tracking em git/forge, não em markdown

**Data:** 2026-05-06
**Status:** Proposto

## Origem

- **Investigação:** Revisão arquitetural pós-v1.20.0 contou 5 mecanismos defensivos no plugin protegendo o mesmo problema estrutural: merge artifact em `BACKLOG.md` quando dois PRs concorrentes mutam as seções `## Em andamento` e `## Concluídos` simultaneamente. Cada mecanismo foi adicionado em momento diferente, em resposta a 3+ ocorrências do artefato em uso real (registrado em PR #20+#21 e linhas históricas em `## Concluídos`). Defesa em profundidade legítima dado o histórico, mas sintoma de **design fragility**: o artefato corrente mistura curadoria editorial (Próximos) com state-tracking (Em andamento, Concluídos), e o segundo é o que quebra sob concorrência.

## Contexto

`BACKLOG.md` cumpre hoje **3 papéis** num único arquivo:

| Seção | Função | Atualizado por |
|---|---|---|
| `## Próximos` | Curadoria editorial — fila de "o que fazer depois" | Operador (manual, via `/triage`) |
| `## Em andamento` | State-tracking — branches em execução | `/triage` (insere) e `/run-plan` (move para Concluídos) |
| `## Concluídos` | State-tracking + registro editorial — PRs entregues + notas de captura | `/run-plan` (insere via "Transição final") |

State-tracking em markdown é o que dá problema. O ciclo do merge artifact:

```
T0  main:                Em andamento: [A, B];  Concluídos: []
T1  PR-A baseado em T0
    PR-A move A:         Em andamento: [B];     Concluídos: [A]
T2  PR-B (paralelo) baseado em T0
    PR-B move B:         Em andamento: [A];     Concluídos: [B]   ← ainda vê A em andamento
T3  Merge PR-A → main:   Em andamento: [B];     Concluídos: [A]
T4  Merge PR-B → main → conflito → resolução automática mistura:
                         Em andamento: [A];     Concluídos: [A, B]   ← A duplicada
```

**Os 5 mecanismos defensivos** (cada um adicionado a uma ocorrência do artefato):

1. `/triage` push pós-commit determinístico — push imediato após adicionar em Em andamento.
2. `/run-plan` precondição 2 segunda metade — bloqueia se há commits ahead E linha em Em andamento.
3. `/run-plan` 3.7 auto-rebase — `git fetch` + rebase + resolução programática quando o conflito é só em Em andamento.
4. Action `validate-backlog` — pós-merge no main, detecta linha duplicada Em andamento+Concluídos e abre issue.
5. Skill `/heal-backlog` — cura manual quando o artefato escapa.

Defesa em profundidade pelo problema, não pela natureza dos mecanismos.

## Decisão

**Mover state-tracking para git/forge.** Caminho **(b) parcial**: remover `## Em andamento` do `BACKLOG.md`; preservar `## Próximos` como curadoria editorial e `## Concluídos` como **registro editorial append-only** (notas de captura tipo "Flagado pelo X durante Y" continuam tendo lugar natural).

State vivo:
- "**Em andamento**" = qualquer branch fora de `main` com PR aberto. Descobrível via `git branch`/`gh pr list`/equivalente; ou simplesmente: a worktree corrente quando `/run-plan` está executando.
- "**Concluídos**" = `/run-plan` 3.4 acrescenta (sem mover de lugar nenhum) ao final do done. Linha do backlog capturada do plano alimenta a entrada.

**Os 5 mecanismos defensivos viram obsoletos** porque o ciclo de mutação dupla desaparece — só `## Concluídos` é tocado pós-execução, sem competição com outra seção.

### Bifurcação descartada

(a) Total — também remover `## Concluídos`. Concluídos vira derivado de `git log` / PRs mergeados. Mais flat, mas perde o **valor editorial**: várias linhas atuais em Concluídos têm comentários úteis ("Flagado pelo `code-reviewer` no Bloco 4 do plano X", "Sintoma observado na release v1.18.0...") que não ficam em commits/PRs e ajudam contextualização futura. Caminho (b) preserva esse valor sem reintroduzir o ciclo de merge artifact (Concluídos sozinho não tem competição).

## Consequências

### Benefícios

- **−5 mecanismos defensivos**: skill `/heal-backlog` removida; Action `validate-backlog` removida; pré-condição 2 segunda metade do `/run-plan` removida; transição inicial Próximos→Em andamento do `/run-plan` removida; auto-rebase 3.7 do `/run-plan` removido; push pós-commit do `/triage` mantido por outras razões (visibilidade/recovery, não merge artifact).
- **Skills mais simples**: `/triage` passo 4 caminho-com-plano não grava em Em andamento; `/run-plan` passo 2 (loop) sem transição inicial; passo 3.4 vira "adicionar" em vez de "mover"; passo 3.7 sem detecção de divergência específica em BACKLOG.md.
- **Schema do BACKLOG.md mais focado**: 2 seções em vez de 3 (Próximos curadoria, Concluídos registro editorial).
- **Operador externo entende o backlog mais fácil**: a separação curadoria-vs-registro fica nítida; sem zona ambígua de "Em andamento" que mistura state e curadoria.

### Trade-offs

- **`## Em andamento` sai do BACKLOG**: operador que quer ver "o que está em andamento agora" precisa olhar `git branch` ou PRs abertos. Em prática, o operador que invoca `/run-plan` **é** o autor da branch corrente — sabe sem consultar. Operador externo lendo o repo pelo GitHub vê PRs abertos.
- **`/next` perde uma fonte**: hoje `/next` reporta "Em andamento" como informação ao final. Sob D2: `/next` reporta apenas top 3 de `## Próximos`; "em andamento" não cabe no escopo da skill (foco em "o que fazer depois", não "o que está sendo feito").

### Limitações

- ADR pressupõe que o operador tem acesso a `git`/`gh`/equivalente para descobrir state vivo. Em fluxos com muitos colaboradores onde state em markdown servia como "tabela compartilhada", D2 deslocaria essa coordenação para o forge (PRs abertos). Hoje plugin é mantenedor único — limitação não vincula. Reabrir se equipe maior reportar pain.
- `## Concluídos` continua sendo append-only manual (`/run-plan` adiciona). Sem mecanismo de garbage collection — repos muito longevos podem ter Concluídos volumoso. Aceito por enquanto: registro histórico tem valor; corte por release é decisão futura.

## Alternativas consideradas

- **(a) Total — remover Em andamento e Concluídos**: caminho mais flat. Descartado por perder notas editoriais úteis em Concluídos sem ganho proporcional (Concluídos sozinho não causa o ciclo de merge artifact).
- **Manter BACKLOG.md como está + adicionar 6º mecanismo defensivo**: cada ocorrência adicionou um mecanismo; 6º seria mais defesa em profundidade pelo mesmo problema estrutural. Rejeitado pela revisão arquitetural — o problema é o design, não a robustez de cada mecanismo.
- **Mover Em andamento para arquivo separado** (ex.: `IN_PROGRESS.md`): mantém o problema (state em markdown) só em arquivo diferente. Não resolve o ciclo. Rejeitado.
- **State em PR labels (`status:in-progress` / `status:done`)**: mais formal mas adiciona dependência ao forge para todo o ciclo (não apenas para PR review). YAGNI; descobrível via "PR aberto vs mergeado" simples.

## Gatilhos de revisão

- Equipe maior ou colaboração distribuída onde `## Em andamento` em markdown era coordenação visível → reabrir para considerar caminho explícito (status labels, dashboard externo, ou retorno).
- `## Concluídos` cresce ao ponto de fricção (ex.: 200+ linhas) → considerar política de archival por release ou por trimestre.
- Surge novo padrão de merge artifact em outra superfície do plugin → reabrir critério "state em markdown" para arquivo afetado.
