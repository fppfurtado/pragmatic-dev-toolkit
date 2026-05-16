---
name: note
description: Append uma nota com timestamp em .claude/local/NOTES.md (store local-gitignored estendendo ADR-005, modo append-only)
disable-model-invocation: false
---

# note

Append uma nota timestampada em `.claude/local/NOTES.md` — store doutrinário non-role para captura de contexto compartilhado entre sessões CC paralelas, intra-projeto e cross-project (este último via referência conversacional, sem auto-discovery). Per [ADR-032](../../docs/decisions/ADR-032-skill-note-contexto-compartilhado.md) — extensão de [ADR-005](../../docs/decisions/ADR-005-modo-local-gitignored-roles.md) para nova categoria *store doutrinário fixo non-role*.

Esta skill executa o append e devolve controle ao operador. **Não faz commit** — `.claude/local/` é gitignored por design.

Skill opera **independente** de `CLAUDE.md` / role contract — usável em qualquer git repo. Cutucada de descoberta ([ADR-017](../../docs/decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md) / [ADR-029](../../docs/decisions/ADR-029-cutucada-descoberta-cobre-claude-md-ausente.md)) **não aplica** (skill não consome papel).

## Argumentos

String com conteúdo da nota. Sem argumento → pedir conteúdo em prosa livre (não enum). Conteúdo final vazio (operador cancela ou submete vazio) → recusa silenciosa, exit clean.

## Passos

### 1. Garantir store

Criar diretório com `mkdir -p .claude/local/` se ausente. Probe gitignore: `git check-ignore -q .claude/local/.probe`. Sem cobertura → disparar gate `Gitignore` per ADR-005 § "Local mode" (mecânica já no CLAUDE.md → "Local mode"). Plus gate "Worktree replication" via [ADR-018](../../docs/decisions/ADR-018-replicacao-claude-em-modo-local-init-config.md) se aplicável (`.claude/` listado no `.worktreeinclude`).

Não é um git repo (`git rev-parse` retorna não-zero) → recusar com mensagem `/note exige git repo (store mora em .claude/local/ relativo à raiz)`.

### 2. Append com timestamp

Conteúdo final vazio → recusa silenciosa, retornar sem escrever.

Caso contrário, gerar timestamp UTC (`date -u +%Y-%m-%dT%H:%M:%SZ`) e fazer append em `.claude/local/NOTES.md` (criar se ausente) no formato:

```

## <timestamp>

<conteúdo>

```

Linha em branco antes do header, linha em branco depois, conteúdo literal do argumento, linha em branco final. Garante separação clara entre entradas; arquivo permanece append-only e legível corrido.

### 3. Reportar

Path do arquivo e bytes adicionados. Operador segue com o trabalho.

## O que NÃO fazer

- Não inferir/sintetizar conteúdo — gravar o argumento literal do operador. A skill não interpreta nem reescreve.
- Não tocar memory nativa CC — `/note` é canal independente; complementa, não substitui. Memory cobre per-project insights conversacionais auto-gravados; `/note` cobre cross-project registro intencional do operador.
- Não auto-buscar contexto em NOTES.md de outros projetos — leitura cross-project é fenômeno conversacional via Read nativo do Claude com path absoluto (operador valida candidato proposto pelo Claude se houver ambiguidade).
- Não fazer commit — `.claude/local/NOTES.md` é gitignored por design; commit acidental quebra o contrato de privacidade.
