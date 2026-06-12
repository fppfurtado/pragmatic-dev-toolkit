# Agent doc-reviewer (genérico)

## Contexto

Quarto reviewer ao lado de `code-reviewer`, `qa-reviewer`, `security-reviewer` — foco em **drift entre documentação e código** detectável no diff. Genérico, reusável em qualquer projeto consumidor (não acoplado às convenções do toolkit).

Lane defendida: identificadores citados em docs (paths, flags, env vars, comandos, símbolos) que não existem no estado atual do repo; cross-refs e anchors quebrados; exemplos/snippets que contradizem o código atual. **Fora de escopo deliberadamente**: estilo, voz, gramática, completude — subjetivos demais para reviewer genérico, sobreporiam ao `code-reviewer`.

Escopo do diff: **cross-cutting** — analisa `.md` alteradas E também varre docs não-tocadas que referenciam identificadores afetados por mudanças em código (rename, deleção, mudança de assinatura).

Acionamento em `/run-plan`: **default em blocos cujos paths são todos `.md`/`.rst`/`.txt`** (substitui `code-reviewer` como default neste recorte); opt-in explícito via `{reviewer: doc}`; combinado via `{reviewer: code,doc}`.

**Linha do backlog:** agent doc-reviewer: revisor genérico de drift entre doc e código (identificadores, cross-refs, exemplos) — quarto reviewer ao lado de code/qa/security; cross-cutting (código+doc); default em blocos .md-only no /run-plan.

## Resumo da mudança

1. Criar `agents/doc-reviewer.md` espelhando a estrutura dos reviewers existentes (frontmatter, identidade, divisão de trabalho, categorias, formato de relatório, `## O que NÃO fazer`).
2. Atualizar `skills/triage/SKILL.md` para aceitar `doc` no schema de `{reviewer:}` e registrar a heurística de atribuição em blocos doc-only.
3. Atualizar `skills/run-plan/SKILL.md` para reconhecer `{reviewer: doc}` e aplicar default em blocos cujos paths são todos `.md`/`.rst`/`.txt`.
4. Atualizar `CLAUDE.md` deste repo (lista de subagents do plugin e regra de shadow override em projetos consumidores).

## Arquivos a alterar

### Bloco 1 — novo agent doc-reviewer {reviewer: code}

- `agents/doc-reviewer.md` (novo). Frontmatter: `name: doc-reviewer` + `description` curta enfatizando "drift entre doc e código" e "stack-agnóstico". Corpo:
  - Identidade + filosofia: "drift detectável, não opinar sobre estilo/voz/gramática/completude".
  - Divisão de trabalho com `code-reviewer`/`qa-reviewer`/`security-reviewer`.
  - **Aplicabilidade**: se o diff não toca `.md`/`.rst`/`.txt` E não renomeia/remove identificadores referenciados em docs do repo, retornar `"Nenhum drift identificado neste diff."`.
  - **`## O que flagrar`** com 3 categorias:
    1. **Identificadores inexistentes** — paths, flags, env vars, comandos shell, símbolos (`função()`, `Class.method`) citados em docs que não existem no estado atual do repo.
    2. **Cross-refs e anchors quebrados** — links internos `[txt](#anchor)` para anchor inexistente; `[txt](path)` para path ausente.
    3. **Exemplos/snippets contraditórios** — code fences ou comandos cujos identificadores divergem do código atual (assinatura mudou, flag renomeada, env var diferente).
  - **`## O que NÃO flagrar`**: estilo, voz, gramática, completude, "could be clearer", typos não-funcionais, exemplos didáticos com placeholders genéricos (`bin/exemplo`, `<sua-coisa>`, `foo/bar`).
  - **`## Como reportar`**: idioma espelha consumidor (default canonical PT-BR); formato `Localização` / `Problema` / `Tipo de drift` / `Sugestão`.
  - Encerrar com seção `## O que NÃO fazer` (load-bearing por convenção do repo).

### Bloco 2 — triage aceita reviewer doc {reviewer: code}

- `skills/triage/SKILL.md`:
  - No schema de anotação `{reviewer: ...}` (passo 4, "Plano"), adicionar `doc` ao enum (`code|qa|security|doc`) e ao exemplo de múltiplos perfis (`code,doc`).
  - Na heurística de cobertura de teste / atribuição de reviewer, registrar: "blocos cujos paths são todos `.md`/`.rst`/`.txt` → omitir anotação (default já vira `doc-reviewer` no `/run-plan`); ou anotar `{reviewer: doc}` explicitamente para deixar visível".
  - Adicionar exemplo no bloco de exemplos: `### Bloco — atualizar README {reviewer: doc}`.

### Bloco 3 — run-plan aciona doc-reviewer {reviewer: code}

- `skills/run-plan/SKILL.md`:
  - Schema de reviewers: aceitar `doc` no perfil único e em listas combinadas.
  - Regra de default: hoje "sem anotação → `code-reviewer`". Substituir por: "sem anotação + paths do bloco todos `.md`/`.rst`/`.txt` → `doc-reviewer`; sem anotação + caso contrário → `code-reviewer`".
  - Invocação análoga aos outros: `Agent(subagent_type=doc-reviewer, ...)`. Quando combinado (`{reviewer: code,doc}`), agregar relatórios.

### Bloco 4 — CLAUDE.md atualizado {reviewer: code}

- `CLAUDE.md`:
  - "Plugin layout" → adicionar `doc-reviewer` à lista de subagents (junto com `code-reviewer`, `qa-reviewer`, `security-reviewer`).
  - "Roles and canonical defaults" → estender a regra de shadow override de reviewers para incluir `doc-reviewer` ao lado de `qa-reviewer` e `security-reviewer`.

## Verificação end-to-end

Repo sem suite automatizada (`test_command: null`). Gate manual em consumidor:

1. Bumpar `version` em `.claude-plugin/plugin.json` e `.claude-plugin/marketplace.json` (smoke local; real só na release) e rodar `/plugin install /path/to/pragmatic-dev-toolkit --scope project` num projeto-fixture.
2. Confirmar descoberta: `doc-reviewer` aparece em `/agents` e em `subagent_type` autocomplete.
3. Disparar manualmente com diff sintético (cenários abaixo) e validar que o reviewer responde no formato declarado, em PT-BR.

## Verificação manual

**Forma do dado real**: identificadores em markdown citando símbolos do código. Padrões textuais frequentes que o reviewer deve reconhecer:

- Flags de CLI: `--no-verify`, `-x`, `--scope user`.
- Env vars: `$VAR`, `${VAR:-}`, `CLAUDE_PLUGIN_ROOT`.
- Paths: `agents/code-reviewer.md`, `docs/philosophy.md`, `.claude-plugin/plugin.json`.
- Símbolos: `function()`, `Class.method`, `module.attr`.
- Comandos shell em backticks inline ou code fences (` ```bash ... ``` `).

**Cenários** (executar contra um worktree do próprio toolkit):

1. **Drift verdadeiro — flag inexistente.** Editar `docs/install.md` adicionando "rode `/plugin install --scope user --no-verify`". Esperado: doc-reviewer flagga `Tipo de drift: identificador inexistente — --no-verify não é flag de /plugin install`.

2. **Drift verdadeiro — rename de path em código não tocado.** Simular renomear `agents/code-reviewer.md` → `agents/style-reviewer.md` no diff e deixar `CLAUDE.md` referenciando `code-reviewer`. Esperado: doc-reviewer flagga referência em `CLAUDE.md` **mesmo sem `CLAUDE.md` aparecer no diff** (caso cross-cutting).

3. **Cross-ref quebrado.** Adicionar em `docs/philosophy.md` `[ver seção X](#secao-inexistente)`. Esperado: flagrado como anchor inexistente.

4. **Falso positivo (NÃO flagrar) — exemplo conceitual com placeholder.** Em README adicionar `rode \`bin/exemplo --foo\` para ilustrar`. `bin/exemplo` é placeholder didático genérico. Esperado: doc-reviewer **não flagga** (cobertura do `## O que NÃO flagrar`).

5. **Diff limpo.** Corrigir typo em README sem tocar identificador. Esperado: `"Nenhum drift identificado neste diff."`.

## Notas operacionais

- Reviewer recebe o diff E (quando o diff renomeia/remove identificadores em código) precisa varrer o repo para detectar referências em docs não-tocadas. Implementar via `Grep` sobre `*.md`/`*.rst`/`*.txt` filtrando pelos identificadores afetados — sem parser de markdown formal.
- Diferença operacional vs. outros reviewers: code/qa/security analisam **só o diff**; doc-reviewer cruza com o repo. Documentar essa exceção no próprio agent e na regra de invocação do `/run-plan`.
- Falsos positivos em exemplos didáticos são contidos pela orientação no agent ("o identificador parece referenciar o repo ou é placeholder genérico de tutorial?") — heurística textual, não regra rígida.
- Idioma do relatório espelha o consumidor (PT-BR canonical), seguindo o padrão dos demais reviewers.
