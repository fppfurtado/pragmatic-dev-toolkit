---
name: migrate-backlog-to-forge
description: Migra `BACKLOG.md` `## Próximos` → forge issues batched e flipa `paths.backlog: forge` em `CLAUDE.md`. Use quando o operador quer migrar role backlog de file→forge num repo com entries pré-existentes. v0 gh-only (boundary glab clara). Não dispara automaticamente — invocação explícita.
disable-model-invocation: true
roles:
  required: [backlog]
---

# migrate-backlog-to-forge

Helper canonical do switch `paths.backlog: file → forge` quando consumer tem `BACKLOG.md` com entries pré-existentes em `## Próximos`. Substitui o pattern empírico de script ad-hoc Python validado em 3 migrações (meta-system 19 entries + logseq-notes 1 + pragmatic-dev-toolkit 7, todas 2026-06-19).

Operação canonical sob modo forge per [ADR-058](../../docs/decisions/ADR-058-role-backlog-aceitar-forge.md) — modelo de cutucada **batched-com-confirmação** per [ADR-066](../../docs/decisions/ADR-066-migracao-inicial-cutucada-batched-modo-forge.md) (3ª categoria editorial). Decomposição hybrid orquestrador + sub-tool determinístico per pattern `skills/*/sub-tools/<f>.py` (formalizado em `CLAUDE.md` § Plugin component naming + § Editing conventions).

## Argumentos

Sem argumentos. Skill opera sobre `BACKLOG.md` resolvido pelo papel `backlog`.

## Boundary

**gh-only em v0.** N=3 empíricas todas gh (operador-owned repos). glab N=0 estrutural — repos TJPA não têm `BACKLOG.md` (canonical já era issues GitLab). Implementação cross-forge speculative violaria YAGNI. Helper para com mensagem clara quando `forge-auto-detect` resolve glab; operador replica manualmente o pattern do sub-tool adaptando `gh issue create` → `glab issue create` se materialização emergir.

**Pré-condição operacional:** skill recém-instalada/atualizada via plugin update (e.g., toolkit `3.11.x → 3.12.0`) numa sessão CC já em curso requer `/reload-plugins` para aparecer no dispatcher. Sintoma: invocação via `Skill` tool retorna `unknown skill`. Recovery: rodar `/reload-plugins`. Comportamento canonical do Claude Code runtime; detalhes em [`docs/install.md` § Recovery em sessão CC já em curso](../../docs/install.md).

## Passos

### 1. Pre-flight forge-auto-detect

Seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md`. Output → tratar conforme:

- **`gh`**: segue para passo 2.
- **`glab`**: para com mensagem: `"glab support deferred until empirical anchor — migração manual via replay do pattern em sub-tool com gh issue create → glab issue create. Detalhes em ADR-066 § Limitações."`. Exit clean.
- **`no-detection`**: para com mensagem orientando setup (`gh auth login` para repos GitHub).
- **`unsupported-host`**: para com mensagem orientando (Bitbucket/Codeberg/host customizado fora de v0).

### 2. Pré-condição role estado

Probar bloco `<!-- pragmatic-toolkit:config -->` em `CLAUDE.md` do projeto consumidor:

- **`paths.backlog: forge` já declarado** → probar `## Próximos` em `BACKLOG.md`. Vazio/marker-presente → para com `"modo já flippado + state consistente — migração não aplicável"`; populado → para com `"paths.backlog: forge declarado MAS ## Próximos contém entries — state parcial pós-falha anterior? Re-executar passos 3-7 manualmente OR consolidar via /init-config"` (idempotência ADR-066 § Trade-offs aplicada).
- **`paths.backlog: null`** → para com `"papel backlog desativado em CLAUDE.md — sem o que migrar"`. Exit clean.
- **Ausente OR file mode (canonical/local)** → segue para passo 3.

**Nota:** passos 2-3 implementam fast-paths específicos da skill com mensagens contextualizadas, em vez da track-3 default "inform and stop" genérica do Resolution protocol (per ADR-003 § Required vs informational roles + CLAUDE.md § The role contract). Cada sub-caso (forge já flippado, null, BACKLOG.md ausente) recebe orientação concreta apropriada.

### 3. Probar BACKLOG.md

Resolver path do papel `backlog` (canonical `BACKLOG.md` na raiz; modo local `.claude/local/BACKLOG.md`):

- **Ausente** → para com `"sem BACKLOG.md no path resolvido — sem entries a migrar; flip config manual via /init-config"`. Exit clean.
- **Presente** → segue.

### 4. Parse `## Próximos` via sub-tool

Executar `python3 ${CLAUDE_PLUGIN_ROOT}/skills/migrate-backlog-to-forge/sub-tools/migrate.py parse --backlog <path>`. Sub-tool retorna JSON em stdout: `{"entries": [{"text": "<entry literal>"}, ...]}`.

- **Zero entries** (`entries: []`) → para com mensagem: `"## Próximos vazio — config flip suficiente, sem entries pra migrar. Edite CLAUDE.md manualmente para paths.backlog: forge."`. Exit clean.
- **N ≥ 1 entries** → contar (`N`) e prosseguir.

Reportar contagem N + listar entries em prosa (1 linha por entry com preview ≤120 chars).

### 5. Gerar títulos batched

Síntese é trabalho **heurístico-semantico do orquestrador** — pattern abaixo é guia editorial, não algoritmo mecânico (entry sem path/skill no início recai em síntese-livre preservando substância). design-reviewer F4 do plano rebate explicitamente "trim determinístico ≤80 chars" como cosmético.

Para cada entry, sintetizar título curto (≤80 chars) capturando objeto-substância:

- Pattern (guia): `<surface> — <objeto>` (e.g., `/debug step 3 — avaliar sub-bloco "tracing reverso" com mini-exemplo`).
- Heurística (orquestrador exerce julgamento): 1ª sentence + objeto-substância (preserva substância semântica em entries multi-frase; síntese-livre quando pattern não bate).
- Mostrar N títulos propostos em prosa: `#1: <title> — <entry preview 80 chars>` (1 linha por entry).

### 6. Cutucada AskUserQuestion unificada

Per [ADR-066](../../docs/decisions/ADR-066-migracao-inicial-cutucada-batched-modo-forge.md) § Mecânica — 3ª categoria editorial **batched-com-confirmação**.

Disparar `AskUserQuestion`:

- Header: `Migração`
- Opções:
  - **`Aplicar batch completo (Recommended)`** — `description`: `"Criar N issues no forge + drain ## Próximos + flipar paths.backlog: forge em CLAUDE.md + commit unificado + push. 1 fluxo, sem cutucadas adicionais."`
  - **`Revisar antes (loop per-item)`** — `description`: `"Loop granular per-item (cutucada por entry com edit inline do título) + confirmação final batched antes do commit. Combinação 1ª + 3ª categorias per ADR-066."`
  - **`Cancelar`** — `description`: `"Aborta sem mutações remotas. State preserved."`

Cobertura única: título + autorização de mutação remota juntos. Operador escolhe.

- `Aplicar batch completo` → passo 7 direto.
- `Revisar antes` → loop granular antes do passo 7 (per-item: mostrar entry + título proposto + cutucada com 4 opções: `Aprovar título` / `Editar título` (input livre via Other do AskUserQuestion) / `Pular esta entry` (drop — não migrar; entry permanece em ## Próximos pós-migração) / `Cancelar tudo` (abort sem mutações remotas; estado preserved)). Ao final do loop com ≥1 entry aprovada, re-disparar `AskUserQuestion` `Aplicar batch revisado` / `Cancelar` antes do passo 7. Loop com zero entries aprovadas (operador pulou todas) → para com mensagem `"loop revisado sem entries aprovadas — abortando sem mutações remotas"`. Confirmação batched revisado → passo 7 entra pelo sub-passo 1 (drift gate aplica em ambos os caminhos `Aplicar batch completo` e `Revisar antes`).
- `Cancelar` → exit clean.

### 7. Execução via sub-tool

Executar `python3 ${CLAUDE_PLUGIN_ROOT}/skills/migrate-backlog-to-forge/sub-tools/migrate.py migrate --backlog <path> --titles <titles.json>`. Sub-tool retorna JSON em stdout: `{"issues": [{"number": N, "title": T, "url": U}, ...]}`.

**Contrato lateral do sub-tool** (side-effects no working tree, pré-commit): além do JSON, sub-tool produz: (a) drain de `## Próximos` em `BACKLOG.md` com marker `_(drenado em <data> — N entries migradas para gh issues #<n1>–#<nN>; ver issues abertas sem assignee)_`; (b) flip de `paths.backlog: forge` em `CLAUDE.md` (edit cirúrgico no bloco `<!-- pragmatic-toolkit:config -->`). Working tree pós-execução contém esses edits unstaged prontos para o commit unificado abaixo.

Pós-execução do sub-tool:

1. **Cutucada de drift na prosa** (pré-commit, gate explícito anti-drift): sub-tool flipa apenas o bloco YAML `<!-- pragmatic-toolkit:config -->`; prosa humana do `CLAUDE.md` (descrições de roles, exemplos, capítulos narrativos) pode conter menções stale a backlog file-mode (`BACKLOG.md` como source-of-truth, `## Próximos` como lista narrativa, `paths.backlog: file`). Disparar `AskUserQuestion`:

   - Header: `Drift`
   - Question: `"Prosa do CLAUDE.md (fora do bloco YAML) revisada por menções stale pós-flip canonical→forge?"`
   - Opções:
     - **`Confirmar prosa OK`** — `description`: `"Prosa revisada / projeto sem prosa custom relevante. Segue para commit unificado."`
     - **`Pausar p/ editar`** — `description`: `"Skill para; operador edita CLAUDE.md inline (mid-turn, mesma sessão CC) preservando edits unstaged do sub-tool; após salvar, responde 'pronto'/'continuar' e skill reentra direto no sub-passo 2 do passo 7."`

   - `Confirmar prosa OK` → segue para sub-passo 2.
   - `Pausar p/ editar` → skill para sem mutar working tree (edits unstaged preservados); operador edita inline mid-turn (mesma sessão CC) e responde com retomada (`pronto`/`continuar` ou equivalente); skill reentra direto no sub-passo 2 do passo 7 sem re-traversar passos 1-6. **Re-invocação via slash command NÃO é o caminho** — cairia no fast-path do passo 2 (`paths.backlog: forge já declarado`) e abortaria incorretamente porque sub-tool já flipou o YAML. Sub-passos 2-3 executam normalmente (commit captura todos os edits unstaged agrupados).

2. **Commit unificado** com mensagem template:
   ```
   feat(config): migrar backlog para paths.backlog: forge

   Materialização do migration helper /migrate-backlog-to-forge. N entries de
   BACKLOG.md ## Próximos migradas para gh issues:
   - #<n1>: <title1>
   - #<n2>: <title2>
   ...

   CLAUDE.md: paths.backlog: forge declarado.
   BACKLOG.md: ## Próximos drenado com marker + cross-ref às issues abertas
   sem assignee. ## Concluídos preservado como histórico append-only.
   ```
   Editorial — ajustar template per convenção do projeto consumidor (idioma + estilo de commits — `docs/philosophy.md` → "Convenção de commits").

3. **Push imediato** (`git push origin HEAD`). Falha (branch protegida, sem upstream, rede etc.) → reportar erro literal; commit local permanece pra operador resolver manualmente (e.g., `git push -u origin <nome-desejado>` ou abrir PR via branch separada).

## O que NÃO fazer

- **Não rodar sem `## Próximos` populado** — gate em passo 4 zero entries para com mensagem clara. Bypass manual via Edit em CLAUDE.md preserva integridade do contrato.
- **Não pular cutucada batched-com-confirmação** — ADR-066 § Mecânica codifica 1 cutucada unificada como invariante editorial. Pular = silent divergence anti-ADR-058 § (e).
- **Não pular cutucada de drift na prosa** (passo 7 sub-passo 1) — gate explícito anti-drift sobre prosa humana do CLAUDE.md que sub-tool não toca; bypass = silent stale prose pós-flip.
- **Não tentar glab inline** — boundary v0 gh-only é explícita per ADR-066 § Limitações. Implementação speculative cross-forge violaria YAGNI doutrinal.
