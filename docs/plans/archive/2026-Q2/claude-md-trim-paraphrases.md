# Reduzir CLAUDE.md cortando paráfrases de philosophy.md/skills/agents

## Contexto

CLAUDE.md é auto-loaded pelo Claude Code em **toda interação** neste repo — cada palavra é input recorrente. Hoje: ~1407 palavras. Cinco seções parafraseiam fonte primária (philosophy.md ou bodies de skills/agents) sem agregar guidance que o LLM não acharia ao ler o destino real. Análise prévia (revisão geral dos artefatos) identificou o recorte; este plano executa.

**Linha do backlog:** CLAUDE.md: cortar paráfrases de philosophy.md/skills/agents para reduzir input tokens auto-loaded a cada interação

## Resumo da mudança

**Manter** (6 seções de guidance específicas a este repo):

- "What this repo is"
- "Plugin layout (what loads what)"
- "The role contract (load-bearing)"
- "Editing conventions"
- "Pragmatic Toolkit" (bloco YAML de config)
- "Local install for iteration"

**Cortar** paráfrases (5 seções):

- "Naming convention (stack-specific vs generic)" — só aponta philosophy.md
- "Hook auto-gating triple (mandatory)" — só aponta philosophy.md
- "Skill workflow contract" — re-explica cada skill body em 5 itens
- "Asking the operator (enum vs prose)" — paráfrase de 1 frase
- "Reviewer agents" — paráfrase dos 3 agents

**Salvar guidance embutida** antes de deletar — nem tudo nas seções a cortar é paráfrase pura. Migrar para "Editing conventions" (ou referência inline na seção remanescente apropriada):

- De "Reviewer agents": frase final ("stack-agnostic; don't add stack suffixes unless the principles themselves change") — convenção de edição do plugin.
- De "Skill workflow contract": frase final ("preserve the separations: alignment → plan → execute, diagnose ≠ fix, release ≠ publish") — convenção de edição.
- De "Hook auto-gating triple": "PostToolUse hooks must always exit 0" — constraint operacional do repo.
- Critério de extração: frase é guidance editorial específica deste repo (não paráfrase de fonte primária) e não está em outra seção da CLAUDE.md.

Alvo: 1407 → ~900 palavras (−36%).

## Arquivos a alterar

### Bloco 1 — CLAUDE.md

- Remover headers e corpo das 5 seções listadas em "Resumo da mudança".
- Antes de remover cada seção, identificar guidance editorial embutida (lista acima) e migrar como bullet único em "Editing conventions".
- Preservar literalmente as 6 seções da keep list e o bloco `<!-- pragmatic-toolkit:config -->` com as chaves atuais (`paths.version_files`, `test_command: null`).
- Manter a frase introdutória "This file provides guidance to Claude Code...".
- Não adicionar conteúdo informacional novo — apenas remoções e migração das frases extraídas.

## Verificação end-to-end

Repo tem `test_command: null`. Substituto textual:

1. `wc -w CLAUDE.md` retorna ≤950 palavras.
2. Cada uma das 6 seções da keep list permanece como header de mesmo nome.
3. As 5 seções da cut list não aparecem mais como header.
4. Bloco `<!-- pragmatic-toolkit:config -->` intacto: chaves `paths.version_files` e `test_command: null` presentes literalmente.
5. As 3 frases editoriais extraídas (stack-agnostic suffix; separations between skills; hooks exit 0) presentes em "Editing conventions" como bullets.
6. `git diff` mostra apenas remoções e migrações cirúrgicas — nenhuma linha de conteúdo informacional novo.
