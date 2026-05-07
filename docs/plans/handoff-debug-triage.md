# Plano — handoff /debug → /triage via cache (ADR-005)

## Contexto

Implementação do ADR-005 ("Cache de handoff entre skills coreografadas"). `/debug` produz diagnóstico em conversa — em sessão longa, cai do contexto antes de o operador invocar `/triage` para o fix. Solução: `/debug` grava sumário estruturado em `.cache/debug-<timestamp>.md` (gitignored); `/triage` passo 1 absorve cache recente (<24h) automaticamente. Adicionalmente, `/debug` passo 6 emite snippet pronto de invocação `/triage` para uso imediato em sessão curta. Caminho **(b) rico** escolhido — cache + snippet.

**Linha do backlog:** /debug → /triage: handoff perde contexto em sessão longa — /debug produz diagnóstico (incluindo ledger de hipóteses) em conversa que cai do contexto antes do operador invocar /triage. Direção possível: /debug passo 6 grava sumário em `.cache/debug-<timestamp>.md` (gitignored) que /triage lê se existir e recente (<24h); ou enriquecer a sugestão final do /debug com snippet pronto de invocação /triage. YAGNI até o pain ser reportado em uso real — registrar para reavaliar. Flagado na revisão arquitetural pós-v1.20.0.

**Escopo escolhido (b):** rico. ADR-005 documenta o trade-off contra (a) só cache.

## Resumo da mudança

Três operações coordenadas:

- **`/debug` passo 6**: antes de "Reportar e devolver controle", gravar sumário estruturado (Sintoma / Hipóteses testadas / Causa-raiz / Evidência / Escopo / Caminhos de correção) em `.cache/debug-<YYYY-MM-DD-HHMMSS>.md`. Em seguida, emitir bloco-comando pronto: `/triage <intent composta a partir do diagnóstico>`. Reportar caminho do arquivo no relatório final.

- **`/triage` passo 1**: novo item — verificar `.cache/debug-*.md` modificado nas últimas 24h (`mtime`); se existir, absorver no `## Contexto` do plano produzido como `**Diagnóstico /debug:**` (resumo curto + path do arquivo para referência completa). Múltiplos arquivos recentes → usar o mais recente; reportar os outros como contexto adicional disponível. Sem cache recente → segue silente.

- **`.gitignore`**: adicionar `.cache/`.

Sem mudança em outras skills/agents/hooks. Sem CLI/flag/env nova. Sem comportamento perceptível ao operador além de continuidade do diagnóstico em sessão longa.

## Arquivos a alterar

### Bloco 1 — `/debug` SKILL: gravar cache + snippet pronto {reviewer: code}

- `skills/debug/SKILL.md` passo 6 ("Reportar e devolver controle"):
  - Adicionar **antes** do parágrafo de reporte: instrução para gravar `.cache/debug-<timestamp>.md` com sumário estruturado dos campos do passo 5. Formato canonical de timestamp: `YYYY-MM-DD-HHMMSS`. Schema do arquivo definido em ADR-005.
  - Adicionar **depois** do parágrafo de reporte: emissão de bloco-comando pronto:
    ```
    /triage <intent composta>
    ```
    onde `<intent composta>` resume o caminho de correção em uma frase de invocação prática (ex.: "corrigir <causa-raiz> em <arquivo:linha> conforme diagnóstico").
  - Reportar path do arquivo de cache no relatório final ("Diagnóstico salvo em `.cache/debug-...md`").

### Bloco 2 — `/triage` SKILL: absorver cache no passo 1 {reviewer: code}

- `skills/triage/SKILL.md` passo 1 ("Carregar contexto mínimo"):
  - Adicionar item após o atual item 5 (`decisions_dir`): "**6. Cache de diagnóstico** — verificar `.cache/debug-*.md` modificado nas últimas 24h (`mtime`). Se existir cache recente, absorver no `## Contexto` do plano produzido como `**Diagnóstico /debug:**` (resumo curto + path do arquivo). Múltiplos arquivos recentes → usar o mais recente; mencionar os outros como contexto adicional disponível. Sem cache recente → segue silente."
- `skills/triage/SKILL.md` passo 4 ("Produzir os artefatos"), seção sobre `## Contexto` do plano:
  - Adicionar bullet documentando o novo campo: "Se passo 1 detectou cache recente em `.cache/debug-*.md`, incluir `**Diagnóstico /debug:** <resumo curto>` com path do arquivo."

### Bloco 3 — `.gitignore` adiciona `.cache/` {reviewer: code}

- `.gitignore`: adicionar `.cache/` após `.claude/` (ou local apropriado). Manter ordem do arquivo.

## Verificação end-to-end

Refactor textual sem suite executável; gate é inspeção dirigida:

1. **Bloco 1 — `/debug` grava cache + emite snippet**:
   - `grep -n ".cache/debug-" skills/debug/SKILL.md` retorna ≥1 ocorrência referenciando o path.
   - Passo 6 cita schema do arquivo (Sintoma / Hipóteses testadas / Causa-raiz / Evidência / Escopo / Caminhos de correção).
   - Bloco-comando pronto `/triage <intent composta>` documentado no passo 6.

2. **Bloco 2 — `/triage` absorve cache**:
   - `grep -n ".cache/debug" skills/triage/SKILL.md` retorna ≥1 ocorrência (item 6 do passo 1 + bullet no passo 4).
   - Item novo em passo 1 menciona `mtime` e expiração 24h.
   - Passo 4 menciona campo `**Diagnóstico /debug:**` no `## Contexto`.

3. **Bloco 3 — `.gitignore` cobre `.cache/`**:
   - `grep -n "^\.cache/$" .gitignore` retorna 1 linha.

4. **Cross-cutting**:
   - ADR-005 referenciado nos blocos onde aplicável.
   - Sem refs penduradas — `.cache/` mencionado em `/debug`, `/triage`, `.gitignore` e ADR-005, lugares coerentes.

## Verificação manual

**Smoke test em uso real** (pós-merge+reload do plugin):

- **Cenário 1 — `/debug` grava cache**: invocar `/debug` num sintoma simples (ex.: teste fictício que falha). Confirmar: skill emite diagnóstico em conversa **e** grava `.cache/debug-<timestamp>.md` com schema completo. Reporta path do arquivo no fim. Bloco-comando `/triage <...>` pronto pra copiar aparece no fim.
- **Cenário 2 — `/triage` absorve cache recente**: imediatamente após cenário 1, invocar `/triage` num pedido qualquer. Confirmar: skill detecta cache recente, absorve no `## Contexto` do plano produzido como `**Diagnóstico /debug:** <resumo curto>` com path do arquivo. Plano gerado tem o campo.
- **Cenário 3 — cache antigo é ignorado**: criar manualmente `.cache/debug-2025-01-01-120000.md` (`touch -t 202501011200 .cache/...`). Invocar `/triage`. Confirmar: skill **não** absorve (mtime > 24h); plano sai sem o campo `**Diagnóstico /debug:**`.

**Critério de aceitação**: os 3 cenários se comportam conforme ADR-005; cache resolve o pain de sessão longa.

## Notas operacionais

- Após merge, todos os 4 itens estruturais do roteiro arquitetural pós-v1.20.0 + handoff /debug → /triage estão entregues. Backlog `## Próximos` fica vazio.
- Próxima `/release` consolida v1.21.0 com 7 PRs mergeados desde v1.20.0 (Batch 1 + Batch 2 + Batch 3/E3 + Batch 3/C1 + Batch 3/B2 + D2 + handoff). Bump minor — várias features perceptíveis (template, gates eliminados, frontmatter declarativo, state em git, cache de handoff).
