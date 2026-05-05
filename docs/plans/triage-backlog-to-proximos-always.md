# triage-backlog-to-proximos-always

## Contexto

O commit de triage grava `BACKLOG.md` em `main` (transição Próximos → Em andamento) antes do branch da feature existir. O `/run-plan`, ao ser executado, move o mesmo item de Em andamento → Concluídos no branch da feature. Quando o PR é mergeado, o git reconcilia duas versões divergentes de `BACKLOG.md` e mantém a linha de Em andamento como "adicionada em main" — gerando um artifact manual de limpeza após cada merge.

Causa-raiz: dupla responsabilidade pela movimentação do backlog — `/triage` escreve Em andamento em `main`, `/run-plan` escreve Concluídos no branch.

Fix: `/triage` para de escrever Em andamento. O item vai sempre para `## Próximos` no commit de triage. O `/run-plan` já faz a transição Próximos → Em andamento no início do passo 3 (o mecanismo que era "defesa contra estado inconsistente" vira o caminho principal). Toda a movimentação do backlog acontece no branch da feature — merge sempre limpo.

**Linha do backlog:** /triage + /run-plan: merge artifact no BACKLOG.md — transição Em andamento gravada no commit de triage (main) reaparece após merge do PR; investigar postergação da transição para o branch da feature

## Resumo da mudança

Remover a distinção de seção "caminho com plano → Em andamento" do passo 4 de `/triage`: ambos os caminhos (com plano e sem plano) gravam em `## Próximos`. Atualizar `## O que NÃO fazer` de `/triage` e a seção "Ciclo de vida do backlog" de `docs/philosophy.md`.

## Arquivos a alterar

### Bloco 1 — `skills/triage/SKILL.md` {reviewer: code}

**Passo 4 — seção BACKLOG, caminho "Papel resolvido normalmente":**

Substituir os dois sub-bullets de escolha de seção por texto unificado:

**Antes:**
```
    - **Caminho com plano** (decisão formal de executar): gravar diretamente em `## Em andamento` e informar o operador. Ver `docs/philosophy.md` → "Ciclo de vida do backlog".
    - **Caminho sem plano** (linha pura, ADR-only, atualização de domínio sem plano associado): default direto em `## Próximos`. Sem cutucada — não há decisão de execução iminente para diferenciar.
```

**Depois:**
```
    - Gravar sempre em `## Próximos`, independente do caminho. A transição Próximos → Em andamento é responsabilidade do `/run-plan` no início da execução — manter em `main` produz merge artifact quando o PR é integrado.
```

**Seção `## O que NÃO fazer`:**

Substituir a linha sobre escolha de seção:

**Antes:**
```
- Não cutucar escolha de seção — caminho com plano vai direto para `## Em andamento`; caminho sem plano vai direto para `## Próximos`.
```

**Depois:**
```
- Não gravar a linha de backlog em `## Em andamento` no commit de triage — toda movimentação de backlog além de `## Próximos` é responsabilidade do `/run-plan` no branch da feature. Gravar Em andamento em `main` produz merge artifact.
```

### Bloco 2 — `docs/philosophy.md` {reviewer: code}

**Seção "Ciclo de vida do backlog" — transição Próximos → Em andamento:**

**Antes:**
```
- **`Próximos → Em andamento`** — aplicado automaticamente por `/triage` no passo 4 quando o caminho escolhido inclui plano (a feature será executada). Aplicado também por `/run-plan` no início, se a linha ainda está em `## Próximos` (defesa contra estado inconsistente — operador pulou a transição no `/triage` ou rodou `/run-plan` sobre plano antigo que recebeu a anotação em sessão posterior).
```

**Depois:**
```
- **`Próximos → Em andamento`** — aplicado automaticamente por `/run-plan` no início do passo 3, sempre que a linha está em `## Próximos`. `/triage` não faz essa transição — registrar Em andamento em `main` antes do branch da feature existir produz merge artifact no momento do merge do PR.
```

## Verificação end-to-end

Verificação textual (sem test suite):

1. Confirmar que o passo 4 de `/triage` não menciona mais `## Em andamento` como destino para o caminho com plano.
2. Confirmar que `## O que NÃO fazer` de `/triage` proíbe explicitamente gravar Em andamento no commit de triage.
3. Confirmar que `docs/philosophy.md` → "Ciclo de vida do backlog" atribui a transição Próximos → Em andamento somente ao `/run-plan`.
4. Verificar que `/run-plan` passo 3 permanece inalterado — já cobre items em Próximos.
