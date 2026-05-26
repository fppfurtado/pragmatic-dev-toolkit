# Plano — Hook `block_settings_drift.py` para auto-bloquear paths absolutos e session perms em `.claude/settings.json`

## Contexto

ROADMAP item 5 (commit `d9e8896`), último pendente do plugin todo (Onda 1; Onda 2 fechou completa). Friction recorrente confirmada pelo `/insights` report da sessão: `.claude/settings.json` acumula entradas de permissão session-scoped ou paths absolutos contendo `/home/<user>/` ou `/Users/<user>/`, exigindo cleanup commits repetidos. Diferente da fragilidade silent regression dos itens da Onda 2 — aqui o pain é **visível** (operador vê a poluição e corrige) mas **recorrente** (mesma classe de erro retorna).

Mecanismo paralelo a `block_env.py` (ADR-015) e `block_gitignored.py` (ADR-016) — terceiro PreToolUse block hook no plugin. Diferencial vs `block_gitignored.py`: `settings.json` é **tracked** (committed); `settings.local.json` é **gitignored**. Hook foca no risco do tracked, que `block_gitignored.py` não cobre (passa por não estar gitignored).

**Auto-gating triplo per CLAUDE.md `## Plugin component naming and hook auto-gating`:**

1. **File extension / path match:** só dispara quando `tool_input.file_path` termina em `.claude/settings.json` exatamente (NÃO `.claude/settings.local.json` — esse é pessoal/gitignored, paths absolutos lá são esperados; outros paths totalmente fora de escopo).
2. **Content pattern match:** scan do conteúdo novo (campo `content` para `Write`, `new_string` para `Edit`) por regex `/home/[^/]+/` ou `/Users/[^/]+/`. Sem match → exit 0 (pass through legitimate edits que não introduzem drift). Windows `C:\Users\` fica de fora por YAGNI — plugin é primariamente Linux/macOS; reabrir se incidente Windows aparecer.
3. **PreToolUse exit 2 quando match:** mensagem clara identificando o pattern detectado + sugestão (mover para `settings.local.json` ou remover) + escape hatch (bypass via edit direto fora do Claude Code).

**Escopo restrito a paths absolutos** (session perms fora do escopo desta versão). `/insights` reportou duas classes de drift recorrente em `settings.json`: paths absolutos AND session-scoped permissions. ADR-040 cobre **só** paths absolutos — regex simples no hot path. Session perms exigiria parse JSON + schema knowledge dos campos `permissions.allow/deny/ask` (frágil a mudanças no formato Claude Code settings). § Gatilho de revisão do ADR-040: reabrir se incidentes de session perms recorrerem após esta versão (sinal: 2+ cleanup commits por session-perm drift em 30 dias após release).

**Classificação editorial — novo ADR-040 sucessor parcial lateral de ADR-015:** pattern paralelo a ADR-015 (block env files via hook) e ADR-016 (block_gitignored scripts no consumer) — ambos PreToolUse block hooks com ADRs próprios codificando critério de bloqueio + retroatividade. Novo ADR-040 fecha a tríade. Per ADR-034 Condição (5) "sucessor parcial — estende ADR Aceito sem revogar": ADR-015 é ancestral direto da família PreToolUse block hooks; ADR-040 estende lateralmente sem revogar. Per ADR-035 critério (1) "incidente recorrente" basta — `/insights` report confirma múltiplos cleanup cycles em `.claude/settings.json`.

**ADRs candidatos:** [ADR-015](../decisions/ADR-015-bloquear-env-files-por-sufixo.md) (ancestral direto — primeiro block hook da família PreToolUse), [ADR-016](../decisions/ADR-016-manter-block-gitignored-scripts-no-consumer.md) (referência metodológica — postura "consumer signal first, escape hatch documentado"), [ADR-034](../decisions/ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) (Condição 5 sucessor parcial lateral), [ADR-035](../decisions/ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) (critério 1 incidente recorrente).

**Linha do backlog:** plugin: hook block_settings_drift para auto-bloquear paths absolutos e session perms em .claude/settings.json

## Resumo da mudança

3 edits coordenados — doctrine first (ADR-040) + mechanism (hook script + registry):

1. **Criar `docs/decisions/ADR-040-block-settings-drift-paths-absolutos-via-hook.md`** — terceiro block hook do plugin, sucessor parcial lateral de ADR-015. § Origem cita ADR-015 (ancestral direto) + ADR-016 (referência metodológica) + ADR-034 (Condição 5 sucessor parcial lateral) + ADR-035 (critério 1 incidente recorrente) + ROADMAP item 5 (insights report como evidência empírica). § Decisão estabelece (a) hook bloqueia edits a `.claude/settings.json` que introduzam `/home/<user>/` ou `/Users/<user>/`; (b) `.claude/settings.local.json` fora do escopo (gitignored, paths absolutos esperados); (c) escape hatch — operador pode editar diretamente via outras ferramentas se necessário; (d) Windows `C:\Users\` fora de escopo (YAGNI; reabrir com incidente).

2. **Criar `hooks/block_settings_drift.py`** — script Python paralelo a `block_env.py`. Lê event JSON de stdin; extrai `file_path` e `content`/`new_string` de `tool_input`. Auto-gating triplo per ADR-040 § Decisão. Mensagem de erro explicativa em stderr quando bloqueia.

3. **Atualizar `hooks/hooks.json`** — adicionar entrada `PreToolUse` para o novo hook (matcher `Edit|Write`, timeout 10s paralelo aos outros block hooks). Atualizar `description` do arquivo para refletir o terceiro block hook.

## Arquivos a alterar

### Bloco 1 — docs/decisions/ADR-040 novo (paralelo ADR-015/ADR-016) {reviewer: doc}

- `docs/decisions/ADR-040-block-settings-drift-paths-absolutos-via-hook.md`: criar via Write (paralelo ADR-038/ADR-039 desta sessão). Estrutura: # Título + Data + Status Proposto + § Origem (ADR-015 ancestral direto + ADR-016 referência metodológica + ADR-034 Cond 5 + ADR-035 critério 1 + ROADMAP item 5 + insights report como evidência) + § Contexto (gap não-coberto por block_gitignored porque settings.json é tracked; rebuttal de ADR-015 § Alternativa (d) — content-inspection viável aqui por escopo restrito a 1 file único + formato JSON estável + regex curto baixo-custo) + § Decisão (4 cláusulas: target file específico, content patterns regex bruta, escape hatch, Windows fora) + § Consequências (benefícios/trade-offs/limitações) + § Alternativas: (a) status quo cleanup pós-fato; (b) CI lint pós-fato (loop feedback lento, cleanup ainda exigido); (c) JSON parse + key-targeted em `permissions.*` (mais preciso vs falso-positivo em strings não-perm, mas dep parse + schema-awareness frágil a mudanças futuras do formato); (d) cobertura de session perms (parse JSON + schema knowledge — fora desta versão, reabre via Gatilho de revisão) + § Gatilhos de revisão (incidente Windows recorrente; recorrência de session perms 2+ vezes em 30 dias pós-release; mudança no formato settings.json Claude Code). Manual `@design-reviewer` invocado para review pré-retorno (simula /new-adr step 5).

### Bloco 2 — hooks/block_settings_drift.py novo script Python {reviewer: code}

- `hooks/block_settings_drift.py`: criar script paralelo a `block_env.py`. Shebang + docstring referenciando ADR-040. Lê stdin JSON, extrai `tool_input.file_path` e conteúdo novo (`content` ou `new_string`). Gate 1: filename exatamente `.claude/settings.json` (não settings.local.json, não outros). Gate 2: regex search por `/home/[^/]+/` OU `/Users/[^/]+/` no conteúdo novo. Sem match em ambos → exit 0. Match → stderr explicativa + exit 2. Edge case: malformed JSON event → exit 0 (não bloqueia por falha de parsing). **Mensagem stderr em inglês** (philosophy.md → Convenção de idioma; hooks são exceção universal, precedente `block_env.py`).

### Bloco 3 — hooks/hooks.json registry update {reviewer: code}

- `hooks/hooks.json`: adicionar nova entrada em `PreToolUse` paralela às existentes (matcher `Edit|Write`, timeout 10s, description curta paralela ao tom das outras). Atualizar top-level `description` do arquivo de "Block direct edits to .env files and gitignored paths; run pytest after Python edits..." para incluir o novo hook ("...; block drift in tracked .claude/settings.json...").

## Verificação end-to-end

- `ls docs/decisions/ADR-040-*.md` retorna 1 arquivo.
- `ls hooks/block_settings_drift.py` retorna o script (executable bit não necessário — invocado via `python3` per hooks.json convention).
- `grep -n "block_settings_drift" hooks/hooks.json` retorna match em PreToolUse + match na description top-level.
- `python3 -c "import json; json.load(open('hooks/hooks.json'))"` retorna sem erro (JSON válido).
- `python3 hooks/block_settings_drift.py <<< '{}'` (event vazio) retorna exit 0 (gate 1 não passa — sem file_path).
- `python3 hooks/block_settings_drift.py <<< '{"tool_input":{"file_path":".claude/settings.json","content":"clean content"}}'` retorna exit 0 (gate 2 não dispara).
- `python3 hooks/block_settings_drift.py <<< '{"tool_input":{"file_path":".claude/settings.json","content":"some /home/user/path here"}}'` retorna exit 2 + stderr explicativa (gates 1+2 disparam).
- `python3 hooks/block_settings_drift.py <<< '{"tool_input":{"file_path":".claude/settings.local.json","content":"some /home/user/path here"}}'` retorna exit 0 (gate 1 exclui settings.local.json).

## Verificação manual

- Em projeto consumidor com o plugin instalado, tentar editar `.claude/settings.json` adicionando uma permissão tipo `"Bash(touch /home/operator/test)"` → hook bloqueia com mensagem clara antes do edit ser aplicado.
- Editar `.claude/settings.local.json` com mesma permissão → hook não dispara, edit prossegue normal.
- Editar `.claude/settings.json` adicionando permissão "clean" (sem path absoluto, ex.: `"Bash(git status)"`) → hook não dispara, edit prossegue.

## Notas operacionais

- Plano 3 blocos, ordem editorial: doutrina primeiro (ADR-040) → mecanismo (script) → registry (hooks.json). Bloco 2 referencia ADR-040 do Bloco 1 em docstring; Bloco 3 referencia o script do Bloco 2 no command path.
- design-reviewer dispatcha automaticamente pré-commit (ADR-011); free-read prioriza ADRs candidatos em `## Contexto`. Vai adjudicar classificação editorial novo-ADR-040 vs alternativas; pattern paralelo a ADR-015/016 é defesa primária.
- Manual `@design-reviewer` invocado no Bloco 1 (simula /new-adr step 5 pré-retorno).
- Script Python segue convenção do plugin: shebang `#!/usr/bin/env python3`, stdlib only (sem deps), tipos básicos. Invocado via `python3 ${CLAUDE_PLUGIN_ROOT}/hooks/<script>.py` em hooks.json.
- Backward-compat: hook só dispara quando file matches `.claude/settings.json`. Consumer projects sem esse file ou que nunca editam settings.json não sentem efeito. Hook é silente em 99% dos contextos.

## Decisões absorvidas

- `## Contexto` (classificação editorial ADR-035 critério 4): rebatido per design-reviewer F2 — critério (4) "pattern emergente ≥3x ad hoc" não aplica literalmente (precedentes ADR-015/016 já são codificados, não ad hoc); critério (1) "incidente recorrente" sozinho basta (single-path).
- `## Contexto` (classificação editorial ADR-034): rebatido per design-reviewer F6 — Condição (5) "sucessor parcial lateral" mais limpa que Condição (1) "sem ancestral direto"; ADR-015 é ancestral conceitual da família PreToolUse block hooks (single-path).
- `## Arquivos a alterar` Bloco 2 (idioma stderr): adicionada nota explícita per design-reviewer F5 — mensagem stderr em inglês (philosophy.md Convenção de idioma; hooks como exceção universal; precedente block_env.py); evita drift de PT-BR vindo da prosa do plano (single-path).
- `## Contexto` (escopo session perms): restrito a paths absolutos per cutucada F1 — bifurcação operador-escolheu "só paths absolutos (Recommended)"; session perms vai para Limitações + Gatilho de revisão do ADR-040 (reabrir se incidentes recorrerem); rationale: regex simples no hot path vs parse JSON + schema knowledge frágil.
- `## Arquivos a alterar` Bloco 1 (mecânica detecção): regex bruta no content per cutucada F3+F4 — bifurcação operador-escolheu "regex bruta (Recommended)"; JSON parse + key-targeted vai para § Alternativas do ADR-040 com rationale do trade-off; rebate ADR-015 § Alternativa (d) por escopo restrito (1 file único + formato JSON estável + regex curto baixo-custo).
