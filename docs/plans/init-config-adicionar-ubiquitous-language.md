# Plano — Adicionar role ubiquitous_language ao wizard /init-config

## Contexto

`/init-config` v1 declara explicitamente (linha 11 da SKILL.md) cobertura de 4 roles com "dor concreta" (`decisions_dir`, `backlog`, `plans_dir`, `test_command`) e exclusão deliberada de informational roles (`product_direction`, `ubiquitous_language`, `design_notes`) + `version_files`/`changelog`, com justificativa "operador edita manualmente quando precisar". Operador (conversa CC 2026-06-02) pede adicionar `ubiquitous_language` ao wizard — dor concreta emergiu (configuração manual repetida do role).

**Escopo (a) escolhido sobre (b) "todos os 3 informational" e (c) "+ version_files com probe"** — incremental empírico: validar utilidade prática da expansão com 1 role antes de comprometer com os outros. A assimetria editorial resultante (cobrimos `ubiquitous_language`, omitimos `product_direction` e `design_notes`) será defendida na linha 11 com framing honesto "adicionar incrementalmente conforme dor concreta emergir" — substitui a doutrina v1 "informational ficam fora" sem revogar a fronteira (outros informational ainda fora até sinal próprio).

`ubiquitous_language` é informational per CLAUDE.md (canonical default `docs/domain.md`; skill segue silenciosamente se ausente; **não aceita modo `local`** — ADR-047 cobre só `decisions_dir`/`backlog`/`plans_dir`). Wizard semantics mais simples que os 3 que aceitam local mode: 2 opções discretas (`Canonical (Recommended)` / `Não usamos`) + auto-`Other`.

Sem ADR — refinamento editorial iterativo per ADR-045 § Risco a vigiar (refinements pós-redesign vão pra `CLAUDE.md` ou git log, não ADR-045 § Decisão); a própria framing "v1"/"v2" na SKILL prose acena para evolução natural.

**ADRs candidatos:** [ADR-046](../decisions/ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) (origem do /init-config), [ADR-003](../decisions/ADR-003-frontmatter-roles.md) § Schema (distinção required vs informational + esquema do bloco config).

## Resumo da mudança

2 trechos editados em `skills/init-config/SKILL.md`:

1. **Linha 11 "Cobertura v1"** — reescrita para refletir 5 roles cobertos + framing incremental honesto sobre os 2 informational ainda fora.
2. **Tabela §3 "Perguntar per role"** — adicionar 1 row para `ubiquitous_language` (header `Domain`; 2 opções discretas + auto-`Other`; canonical default `docs/domain.md`).

Fora de escopo: probe stack-aware (ubiquitous_language não tem default por stack); §4.5 worktree replication (só dispara para roles em modo local; ubiquitous_language não aceita); §5 informational warnings (sem novo warning necessário); cobrir `product_direction` e `design_notes` (escopo (b) — adiado per decisão (a)); cobrir `version_files`/`changelog` (escopo (c) — exige probe novo).

## Arquivos a alterar

### Bloco 1 — adicionar ubiquitous_language ao wizard /init-config {reviewer: doc}

`skills/init-config/SKILL.md`:

- **Linha 11** — reescrever cobertura:
  - Atual: `**Cobertura v1:** 4 roles com dor concreta — \`decisions_dir\`, \`backlog\`, \`plans_dir\` (aceitam local mode per [ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md)) e \`test_command\` (top-level no schema). Informational roles (\`product_direction\`, \`ubiquitous_language\`, \`design_notes\`) e \`version_files\`/\`changelog\` ficam fora — operador edita manualmente quando precisar.`
  - Novo: `**Cobertura:** 5 roles — \`decisions_dir\`, \`backlog\`, \`plans_dir\` (aceitam local mode per [ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md)), \`test_command\` (top-level no schema) e \`ubiquitous_language\` (informational; sem local mode). Outros informational roles (\`product_direction\`, \`design_notes\`) e \`version_files\`/\`changelog\` ficam fora — operador edita manualmente quando precisar; adicionar incrementalmente ao wizard conforme dor concreta emergir.`

- **Tabela §3 (linhas 42-47)** — adicionar 1 row para `ubiquitous_language` após a row de `plans_dir` (antes de `test_command` que é top-level, agrupamento por categoria):
  - Row a inserir: `| \`ubiquitous_language\` | \`Domain\` | \`Canonical\` (\`grava em docs/domain.md — default canonical do toolkit\`) / \`Não usamos\` (\`grava paths.ubiquitous_language: null — skill subsequente trata como absent sem perguntar\`) |`

Demais seções (probe stack-aware, §4 composição YAML, §4.5 worktree replication, §5 informational warnings, § O que NÃO fazer) não são tocadas — `ubiquitous_language` reusa o schema YAML existente (`paths.<role>: <valor>` ou `null`) e não introduz nova condição de disparo.

## Verificação end-to-end

Gates mecânicos:

1. **Linha 11 atualizada** — 2 gates ancorados: `grep -c "Cobertura v1:" skills/init-config/SKILL.md` retorna 0 (doutrina antiga removida); `grep -nE "^\*\*Cobertura:\*\* 5 roles" skills/init-config/SKILL.md` retorna 1 match (nova wording ancorada por prefixo + parte literal).

2. **Row de ubiquitous_language presente** — `grep -nE "\`ubiquitous_language\`" skills/init-config/SKILL.md` retorna ≥2 matches: 1 na linha 11 (rol coberto pós-reescrita) + 1 na nova row da tabela §3.

3. **Header `Domain` presente na tabela §3** — `grep -nE "^\| \`ubiquitous_language\` \| \`Domain\`" skills/init-config/SKILL.md` retorna exatamente 1 match.

4. **Read manual** das linhas 11 + 38-50 — verificar que a linha 11 reescrita tem framing "incremental conforme dor emergir" honesto sobre a exclusão remanescente, e que a nova row da tabela mantém o estilo das rows existentes (2 opções discretas + auto-Other implícito; sem Recommended marcado pois `ubiquitous_language` informational não tem default estatisticamente dominante — `philosophy.md` linha 105 cita o role como exemplo típico de "não temos").

## Decisões absorvidas

- Bloco 1 row de ubiquitous_language: `(Recommended)` removido da opção `Canonical` — contradiz CLAUDE.md → "AskUserQuestion mechanics" ("Recommended sem default real é viés enganoso") e philosophy.md linha 105 que cita ubiquitous_language como exemplo típico de "não temos" (caminho-único).
- Gate 1 da Verificação end-to-end: substituído por 2 gates ancorados (`grep -c "Cobertura v1:"` retorna 0 + `grep -nE "^\*\*Cobertura:\*\* 5 roles"` retorna 1) — gate original ambíguo via substring matching (`Cobertura:` é prefixo de `Cobertura v1:`) (caminho-único).
- Gate 2 da Verificação end-to-end: explicação reescrita removendo parênteses auto-contraditório (linha 11 cita 1x ubiquitous_language pós-reescrita, não 2x) (caminho-único).
