# triage-no-backlog-in-plan-blocks

## Contexto

Quando `/triage` segue o caminho com plano, já executa a transição Próximos → Em andamento no passo 4 (gravação direta no arquivo do papel `backlog`). O plano gerado carrega `**Linha do backlog:** <texto>` em `## Contexto` — esse campo é o mensageiro que permite ao `/run-plan` operar as transições Em andamento → Concluídos no gate final.

Problema: se o plano gerado também listar `BACKLOG.md` em `## Arquivos a alterar`, o `/run-plan` tratará o backlog como um bloco de execução, tentando aplicar edits explícitos que contradizem ou duplicam as transições automáticas do ciclo de vida. O mecanismo `**Linha do backlog:**` torna esse bloco desnecessário e incorreto.

**Linha do backlog:** /triage: não listar BACKLOG.md como bloco em "Arquivos a alterar" quando a transição Próximos → Em andamento já é executada no passo 4 do triage

## Resumo da mudança

Adicionar guarda explícita em `skills/triage/SKILL.md` — na seção de produção do plano (passo 4) e em `## O que NÃO fazer` — proibindo a inclusão de `BACKLOG.md` em `## Arquivos a alterar` quando o ciclo de vida do backlog é gerenciado pelo campo `**Linha do backlog:**`.

## Arquivos a alterar

### Bloco 1 — `skills/triage/SKILL.md` {reviewer: code}

Duas adições no mesmo arquivo:

**1. Passo 4 — seção Plano**, após a instrução de incluir `**Linha do backlog:**` em `## Contexto`:

Acrescentar nota explícita: `BACKLOG.md` **não deve aparecer** em `## Arquivos a alterar` do plano. As transições de estado do backlog são gerenciadas pelo campo `**Linha do backlog:**` + mecanismo automático do `/run-plan` — não por blocos de execução. Incluir o arquivo como bloco gera redundância e pode produzir edits conflitantes.

**2. Seção `## O que NÃO fazer`**:

Adicionar linha: `Não incluir BACKLOG.md em ## Arquivos a alterar do plano — as transições de estado são gerenciadas pelo campo **Linha do backlog:** no ## Contexto; bloco de execução seria redundante e potencialmente conflitante com o ciclo de vida automático.`

## Verificação end-to-end

Verificação textual (sem test suite):

1. Ler o passo 4 modificado e confirmar que a nota sobre BACKLOG.md está presente e clara após a instrução do `**Linha do backlog:**`.
2. Confirmar que a linha correspondente aparece em `## O que NÃO fazer`.
3. Verificar que nenhuma outra parte do skill foi alterada (escopo restrito).
