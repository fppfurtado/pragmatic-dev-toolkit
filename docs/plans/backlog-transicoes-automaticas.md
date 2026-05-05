# backlog: transições de estado automáticas sem cutucada ao operador

## Contexto

**Linha do backlog:** backlog: transições de estado automáticas sem cutucada ao operador

O v1.13 implementou o ciclo de vida do backlog (`Próximos → Em andamento → Concluídos`) com cutucadas explícitas via `AskUserQuestion` a cada transição — decisão documentada no plano `v1.13-transicao-estado-backlog.md` linha 20: "Toolkit cutuca, não decide." O argumento era risco de mover linha errada; o matching, porém, já é por texto exato (`**Linha do backlog:**`), não heurístico — o risco real é baixo.

O operador decide agora reverter essa política: as transições passam a ser automáticas, o plugin apenas informa a mudança sem pedir confirmação.

## Resumo da mudança

Remoção das três chamadas de `AskUserQuestion` ligadas a transições de estado do backlog:

1. `/triage` passo 4 — caminho com plano: em vez de enum `Próximos / Em andamento`, linha vai direto para `## Em andamento` + informe.
2. `/run-plan` passo 3 (antes do primeiro bloco) — `Próximos → Em andamento`: mover automaticamente + informe.
3. `/run-plan` passo 4.4 — `Em andamento → Concluídos`: mover automaticamente + informe.

`docs/philosophy.md` atualizado para refletir o novo contrato.

## Arquivos a alterar

### Bloco 1 — `docs/philosophy.md` {reviewer: code}

Seção "Ciclo de vida do backlog":

- Alterar abertura do parágrafo de transições: substituir "via cutucada explícita ao operador, nunca por inferência textual" por "**automaticamente**, apenas informando o operador — nunca por inferência textual".
- Nos dois bullets de transição, substituir "cutucado por" → "aplicado automaticamente por".

### Bloco 2 — `skills/triage/SKILL.md` {reviewer: code}

Passo 4, sub-bullet BACKLOG, caminho com plano:

- Substituir: "cutucar via enum (`AskUserQuestion`, header `Backlog`, opções `Próximos` (recomendado) / `Em andamento`). Operador escolhe; linha é gravada na seção escolhida."
- Por: "gravar diretamente em `## Em andamento` e informar o operador."

`## O que NÃO fazer`, último bullet:

- Substituir: "Não cutucar a escolha de seção (`Próximos` / `Em andamento`) quando o caminho não inclui plano — sem decisão de execução iminente, default `Próximos` direto."
- Por: "Não cutucar escolha de seção — caminho com plano vai direto para `## Em andamento`; caminho sem plano vai direto para `## Próximos`."

### Bloco 3 — `skills/run-plan/SKILL.md` {reviewer: code}

Passo 3, antes do primeiro bloco — cutucada `Próximos → Em andamento`:

- Substituir: "cutucar via enum (`AskUserQuestion`, header `Backlog`, opções `Mover para Em andamento` (recomendado) / `Deixar em Próximos`). Mover aplica edit no arquivo do backlog antes do primeiro bloco; edit entra no commit do primeiro bloco."
- Por: "mover automaticamente para `## Em andamento`, informar o operador, e aplicar o edit no arquivo do backlog antes do primeiro bloco (edit entra no commit do primeiro bloco)."

Passo 4.4, transição final — `Em andamento → Concluídos`:

- Substituir: "cutucar via enum (`AskUserQuestion`, header `Backlog`, opções `Mover para Concluídos` (recomendado) / `Deixar onde está`). Mover aplica edit como **bloco extra**"
- Por: "mover automaticamente para `## Concluídos`, informar o operador, e aplicar como **bloco extra**"
- Na mesma frase, substituir "(ou ainda em `## Próximos`, caso a transição inicial tenha sido recusada)" por "(ou ainda em `## Próximos`, caso a transição inicial não tenha ocorrido)".

`## O que NÃO fazer`, bullet sobre transição final:

- Substituir: "Não silenciar a transição final (passo 4.4) quando a linha está presente e localizada — cutucar é regra; resposta `Deixar onde está` é fechamento válido."
- Por: "Não silenciar a transição final (passo 4.4) quando a linha está presente e localizada — a transição é automática; informar o operador é obrigatório."

## Verificação end-to-end

Inspeção textual (repo não tem suite automatizada):

- `docs/philosophy.md`: seção "Ciclo de vida do backlog" descreve transições automáticas; nenhuma ocorrência de "cutucada" permanece nos dois bullets de transição.
- `skills/triage/SKILL.md`: passo 4 caminho-com-plano não referencia `AskUserQuestion` para escolha de seção; `## O que NÃO fazer` atualizado.
- `skills/run-plan/SKILL.md`: passo 3 e passo 4.4 não referenciam `AskUserQuestion` para transições de backlog; `## O que NÃO fazer` atualizado.
- Diff não introduz comentários redundantes, defensividade nova ou abstrações desnecessárias (rubrica `code-reviewer`).

## Verificação manual

Smoke test em consumer project com `BACKLOG.md` populado. Instalar o plugin localmente via `/plugin install /storage/3. Resources/Projects/h3/pragmatic-dev-toolkit --scope project`.

**Cenário 1 — `/triage` com plano: linha vai para `## Em andamento` automaticamente**

- Invocar `/triage exportar movimentos do mês em CSV`. Caminho escolhido: plano + linha no backlog.
- Esperado: nenhum enum de seção é exibido; skill informa diretamente "Linha gravada em `## Em andamento`". Plano produzido com `**Linha do backlog:**` no `## Contexto`.

**Cenário 2 — `/run-plan` início: `Próximos → Em andamento` automático**

- Consumer project com linha em `## Próximos` e plano com `**Linha do backlog:**`.
- Invocar `/run-plan <slug>`. Esperado: skill informa "Movendo linha para `## Em andamento`" e aplica o edit sem pedir confirmação. Execução prossegue.

**Cenário 3 — `/run-plan` gate final: `Em andamento → Concluídos` automático**

- Continuação do Cenário 2. No gate final (passo 4.4).
- Esperado: skill informa "Movendo linha para `## Concluídos`" e aplica como bloco extra sem pedir confirmação. Done declarado após harvest.

**Cenário 4 — `/triage` sem plano: linha vai para `## Próximos` (comportamento inalterado)**

- Invocar `/triage renomear coluna`. Caminho: só linha no backlog.
- Esperado: linha vai direto para `## Próximos`; nenhum enum exibido. Comportamento idêntico ao anterior.

**Cenário 5 — plano sem `**Linha do backlog:**`: skip silente (comportamento inalterado)**

- Invocar `/run-plan` sobre plano sem o campo.
- Esperado: nenhuma transição ocorre, nenhum informe exibido.

**Critério de aprovação:** Cenários 1–3 confirmam transições automáticas sem prompt. Cenários 4–5 confirmam que o comportamento de skip e default direto permanecem corretos.

## Notas operacionais

- Antes de `/run-plan`, reverter os edits diretos feitos fora do fluxo (aplicados na sessão anterior antes da triagem): `git restore docs/philosophy.md skills/triage/SKILL.md skills/run-plan/SKILL.md`. A worktree parte do HEAD limpo.
- Reviewer `code` em todos os blocos — mudança editorial em prosa de skills; rubricas `qa` e `security` não se aplicam.
- Mudança é cirúrgica: não altera lógica de matching, skip silente, harvest, nem comportamento de projetos sem backlog. Apenas remove os três `AskUserQuestion` de transição de estado.
