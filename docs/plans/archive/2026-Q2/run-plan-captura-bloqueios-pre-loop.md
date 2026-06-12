# run-plan: captura automática de bloqueios em pré-condição de worktree

## Contexto

**Linha do backlog:** /run-plan: captura automática de bloqueios em pré-condição de worktree (fase anterior ao loop de arquivos)

O mecanismo de captura automática do `/run-plan` (passo 4.5) cobre gatilhos detectados durante o loop de arquivos (passo 3) e durante a validação manual (passo 4.2). A captura nesses casos é **deferida** — o agente acumula uma lista durante a execução e a materializa no gate final.

Bloqueios detectados antes do loop — nas pré-condições e no passo 1 de setup da worktree — não geram nenhuma captura: a skill para, reporta ao operador, e o contexto se perde.

Exemplos de bloqueios não capturados hoje:
- **Baseline vermelho** (pré-condição 3): testes falham no branch atual → problema independente que merece linha no backlog.
- **Worktree órfã** (pré-condição 4): `.worktrees/<slug>` já existe de run anterior abandonado → cleanup necessário.
- **Falha no setup da worktree** (passo 1): `git worktree add` falha, install de dependências falha, ou baseline falha após sync → problema de ambiente.

Diferença estrutural: esses bloqueios interrompem a skill antes do gate final, portanto a captura precisa ser **imediata** (escrever no backlog antes de parar), não deferida para o passo 4.5.

Bloqueios por erro do operador — plano sujo (pré-condição 2a) e push pendente (pré-condição 2b) — **não geram captura**: são estados esperados que o operador corrige e retenta. Mesma exclusão para plano inexistente (pré-condição 1) — é input missing, não imprevisto.

## Resumo da mudança

1. `skills/run-plan/SKILL.md`: adicionar captura imediata nos bloqueios das pré-condições 3 e 4 e no passo 1; atualizar a nota de abertura do passo 3 para distinguir captura imediata (pre-loop) de captura deferida (execução + gate); mencionar o novo tipo no passo 4.5 para completude; adicionar bullet em `## O que NÃO fazer`.
2. `docs/philosophy.md`: adicionar um terceiro tipo à seção "Classificação de capturas automáticas" — "Bloqueio de pré-condição ou setup" — com destino, mecanismo (imediato) e exclusões.

## Arquivos a alterar

### Bloco 1 — `skills/run-plan/SKILL.md` {reviewer: code}

Edits cirúrgicos em quatro pontos do arquivo:

**1. Pré-condição 3** (gate de testes no branch atual)

Após a última frase da pré-condição 3 ("...caso de exceção, sinalizado pela ausência de `test_command` resolvido **e** por o plano explicitar essa verificação textual."), adicionar:

> Se o gate falha: escrever linha `baseline vermelho no branch ao iniciar /run-plan <slug> — investigar antes de re-executar` em `## Próximos` do papel `backlog`; informar o operador; parar. Papel `backlog` = "não temos" → só informar, sem escrita.

**2. Pré-condição 4** (worktree não deve existir)

Substituir a frase atual `4. A worktree `.worktrees/<slug>/` ainda não existe.` por:

> 4\. A worktree `.worktrees/<slug>/` ainda não existe. Se já existir: escrever linha `worktree .worktrees/<slug> existe de run anterior — remover antes de re-executar` em `## Próximos` do papel `backlog`; informar o operador; parar. Papel `backlog` = "não temos" → só informar, sem escrita.

**3. Passo 1.3** (sync + baseline na worktree)

A frase "**Abortar se falhar** — o plano não roda em cima de testes vermelhos." cobre tanto falha de sync quanto baseline vermelho na worktree. Estender com:

> Ao abortar (falha de install ou baseline vermelho): escrever linha descritiva em `## Próximos` do papel `backlog` antes de parar — ex.: `install de dependências falhou na worktree de <slug> — verificar ambiente` ou `baseline vermelho na worktree de <slug> ao iniciar — investigar`. Papel `backlog` = "não temos" → só informar, sem escrita.

**4. Passo 3 — nota de abertura**

Substituir a nota atual:

> **Captura automática durante a execução:** ao longo de todo o passo 3 (e estendendo-se ao passo 4.2), o agente observa gatilhos de **imprevistos detectados automaticamente**. Lista, gatilhos e materialização final em 4.5.

Por:

> **Captura automática — dois modos:**
> - **Imediata (pre-loop):** bloqueios nas pré-condições 3/4 e no passo 1 geram captura antes de parar — a skill escreve a linha no papel `backlog` e para. Mecânica descrita in situ em cada pré-condição/passo.
> - **Deferida (execução + validação):** ao longo do passo 3 e do passo 4.2, o agente acumula gatilhos de imprevistos detectados automaticamente e materializa tudo no gate final. Lista, gatilhos e materialização em 4.5.

**5. Passo 4.5 — lista de gatilhos**

Ao final da lista "Durante a execução dos blocos (passo 3)", antes do bloco "Durante a validação manual", inserir nota de cross-referência:

> *(Bloqueios de pré-condição e passo 1 — baseline vermelho, worktree órfã, falha de setup — geram captura imediata descrita in situ; não alimentam esta lista deferida.)*

**6. `## O que NÃO fazer`**

Adicionar ao final da seção:

> - Não bloquear sem captura em pré-condição 3 (baseline vermelho), pré-condição 4 (worktree órfã) e passo 1 (falha de setup) — captura imediata no papel `backlog` é obrigatória antes do stop nesses casos. Papel `backlog` = "não temos" → informar operador, não escrever.

### Bloco 2 — `docs/philosophy.md` {reviewer: code}

Na seção "Classificação de capturas automáticas", dois edits:

**1.** Atualizar a primeira linha da seção de:

> Toda captura detectada pelo `/run-plan` (passo 4.5) é classificada em dois tipos antes de ser roteada:

Para:

> Capturas do `/run-plan` são classificadas em três tipos. Capturas do passo 4.5 (execução e validação manual) são deferidas ao gate final. Capturas de bloqueios pre-loop (pré-condições e passo 1) são imediatas — escritas antes de parar. Em ambos os casos, o destino é determinado pelo tipo:

**2.** Após o bloco "Backlog" (antes de "**Sinal explícito do operador**"), adicionar:

> **Bloqueio de pré-condição ou setup** — a skill bloqueou antes de iniciar o loop: baseline vermelho no branch, worktree órfã, install falhando, baseline vermelho na worktree.
>
> Destino: `## Próximos` do papel `backlog`. Captura é imediata (antes do stop), não deferida ao gate final.
> Não se aplica a bloqueios por erro do operador (plano sujo, push pendente) — esses são estados esperados sem captura.

## Verificação end-to-end

Não aplicável — este repo é o plugin (sem `test_command`). Gate é a `## Verificação manual`.

## Verificação manual

Em projeto-fixture com este plugin instalado:

1. **Baseline vermelho** (pré-condição 3): criar branch com testes falhando; invocar `/run-plan <slug>`. Confirmar: linha escrita em `## Próximos` do BACKLOG.md; mensagem ao operador cita a linha; skill não prossegue para setup da worktree.
2. **Worktree órfã** (pré-condição 4): deixar `.worktrees/<slug>/` de run anterior sem remover; invocar `/run-plan <slug>`. Confirmar: linha escrita em `## Próximos`; skill para.
3. **Falha de install** (passo 1): simular falha de `uv sync` / `npm ci` / equivalente na worktree. Confirmar: linha escrita em BACKLOG antes de abortar.
4. **Baseline vermelho na worktree** (passo 1): ambiente ok no branch, mas testes falham após sync na worktree. Confirmar: captura imediata em BACKLOG antes de abortar.
5. **Bloqueios sem captura** (esperados): plano com arquivo sujo (pré-condição 2a); push pendente com linha Em andamento (pré-condição 2b). Confirmar: nenhuma linha escrita no BACKLOG em nenhum dos dois casos — só report e stop.
6. **Papel `backlog` = "não temos"**: repetir cenários 1–4 em projeto com `paths.backlog: null`. Confirmar: skill informa captura ao operador sem escrever arquivo; para normalmente.
7. **Cross-check com captura deferida**: em run que atinge o passo 3 (pré-condições ok), confirmar que a nota de abertura do passo 3 cita os dois modos e que a lista deferida do passo 4.5 não contém entradas de pre-loop.
