# Plano — handoff /debug → /triage via snippet pronto

## Contexto

Item registrado em `## Próximos` do BACKLOG: "/debug → /triage handoff perde contexto em sessão longa". Operador autorizou implementar (apesar da nota YAGNI original) **com escopo restrito ao snippet pronto**, sem cache em arquivo nem ADR — caminho mais flat possível.

`/debug` passo 6 atualmente sugere `/triage <intent>` em uma frase genérica. Mudança: emitir bloco-comando **literal pronto** com a invocação completa preenchida a partir do diagnóstico, para o operador copiar/colar diretamente.

**Linha do backlog:** /debug → /triage: handoff perde contexto em sessão longa — /debug produz diagnóstico (incluindo ledger de hipóteses) em conversa que cai do contexto antes do operador invocar /triage. Direção possível: /debug passo 6 grava sumário em `.cache/debug-<timestamp>.md` (gitignored) que /triage lê se existir e recente (<24h); ou enriquecer a sugestão final do /debug com snippet pronto de invocação /triage. YAGNI até o pain ser reportado em uso real — registrar para reavaliar. Flagado na revisão arquitetural pós-v1.20.0.

**Escopo escolhido:** apenas snippet, **sem persistência**. Operador aceita que o handoff só ajuda em sessão curta (operador copia/cola na hora); sessão longa onde contexto cai continua exigindo o operador reproduzir manualmente o diagnóstico ou abrir conversa nova. Avaliação técnica de variável de ambiente como handoff descartada — Bash subshells em Claude Code não persistem env vars entre invocações; cache em arquivo seria a única forma viável de handoff persistente, mas escopo restrito a snippet por escolha do operador.

**Sem ADR**: snippet é mudança trivial em 1 SKILL — não introduz superfície estrutural nova nem categoria de decisão duradoura.

## Resumo da mudança

Refactor textual em `skills/debug/SKILL.md` passo 6 — substituir a sugestão genérica `/triage <intent>` por bloco-comando literal pronto, preenchido a partir dos campos do passo 5 (Causa-raiz, Caminhos de correção). Passo 6 continua sugerindo os 3 caminhos (Revert / Patch / `/triage`); só a forma do `/triage` muda — de frase descritiva para bloco-comando copiável.

Sem mudança em outras skills/agents/hooks/docs. Sem CLI/flag/env nova. Sem comportamento perceptível além de UX bonus na sugestão final do `/debug`.

## Arquivos a alterar

### Bloco 1 — `/debug` passo 6 emite snippet pronto {reviewer: code}

- `skills/debug/SKILL.md` passo 6 ("Reportar e devolver controle"):
  - Substituir o bullet atual `**`/triage <intent>`** — fix é mudança maior (...)` por instrução de **emitir bloco-comando pronto** quando o caminho for `/triage`. Formato:
    ```
    /triage <intent composta a partir da causa-raiz + caminho de correção>
    ```
    onde `<intent composta>` resume em uma frase de invocação prática (ex.: `corrigir AssertionError em test_export_csv.py:42 — fixture stale`).
  - Manter os bullets de Revert e Patch local sem mudança.
  - Manter a frase "Diagnóstico completo (incluindo *Hipóteses testadas* quando presente) entra como insumo do `## Contexto` do plano." — explicação semântica de quem consome o snippet.
  - Reportar nota explícita: snippet só ajuda em sessão curta; sessão longa onde contexto cai exige operador reproduzir manualmente.

## Verificação end-to-end

Refactor textual sem suite executável; gate é inspeção dirigida:

1. **Snippet pronto presente em /debug passo 6**:
   - `grep -n "bloco-comando\|snippet pronto\|/triage <intent" skills/debug/SKILL.md` retorna a referência.
   - Passo 6 mantém os 3 caminhos (Revert / Patch / `/triage`).
   - Passo 6 cita formato literal copiável.

2. **Sem persistência introduzida**:
   - `ls .cache/ 2>&1` retorna "No such file or directory" (cache não criado).
   - `.gitignore` não menciona `.cache/`.
   - Nenhum ADR criado para esta mudança.

3. **Cross-cutting**:
   - `/triage` SKILL.md inalterado (sem leitura de cache).
   - Outras skills inalteradas.

## Notas operacionais

- Plano fica intencionalmente pequeno. Bloco único. Sem ADR. Disciplina de /run-plan mantida (worktree, reviewer, micro-commit, gate) para coerência com o workflow do plugin, mesmo que a mudança caiba num commit cirúrgico em main.
- Linha do handoff em `## Próximos` do BACKLOG: sob D2, /run-plan 3.4 adiciona em `## Concluídos` no done. Linha continuará em `## Próximos` (gap conhecido do D2 capturado em outra linha de Próximos). Cleanup pós-merge: remover linha duplicada de Próximos manualmente, **ou** atacar o item "/run-plan 3.4 mover vs adicionar" antes do release de v1.21.0 para que o problema não recorra.
