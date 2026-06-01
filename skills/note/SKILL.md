---
name: note
description: Append uma nota com timestamp em .claude/local/NOTES.md (store local-gitignored estendendo ADR-047, modo append-only)
disable-model-invocation: false
---

# note

Append uma nota timestampada em `.claude/local/NOTES.md` — store doutrinário non-role para captura de contexto compartilhado entre sessões CC paralelas, intra-projeto e cross-project (este último via referência conversacional, sem auto-discovery). Per [ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (a) — extensão de [ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md) para nova categoria *store doutrinário fixo non-role*.

Esta skill executa o append e devolve controle ao operador. **Não faz commit** — `.claude/local/` é gitignored por design.

Skill opera **independente** de `CLAUDE.md` / role contract — usável em qualquer git repo. Cutucada de descoberta ([ADR-046](../../docs/decisions/ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md)) **não aplica** (skill não consome papel).

## Argumentos

Skill aceita 2 modos (per [ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (b)):

- **Sem `--to`** (default, intra-projeto): argumento inteiro = conteúdo da nota. Append em `<repo-corrente>/.claude/local/NOTES.md`.
- **Com `--to <projeto-ou-path>`** (opt-in cross-write): primeiro token literal `--to` seguido do valor; restante após o valor = conteúdo. Append em `<target>/.claude/local/NOTES.md`. Resolução do target em § 1.

Parsing: detectar `--to <valor>` no início do argumento; resto = conteúdo literal. Sem argumento → pedir conteúdo em prosa livre (não enum). Conteúdo final vazio (operador cancela ou submete vazio) → recusa silenciosa, exit clean.

Casos degenerados (recusa silenciosa): `--to` sem valor subsequente (sintaxe inválida); conteúdo restante vazio após `--to <valor>` (mesmo caminho do § 2 — recusa silenciosa).

## Passos

### 1. Garantir store

**Resolução do target** (per [ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (b)):

- **Sem `--to`** → target = repo corrente. Caminho local; seguir para "Caminho local" abaixo.
- **Com `--to <valor>`** → target = outro projeto (cross-write):
  - `<valor>` contém `/` → tratar como path absoluto (bypass discovery).
  - `<valor>` não contém `/` (nome) → resolver via `$PROJECTS_DIR/<valor>/`.
    - `$PROJECTS_DIR` ausente → recusar com mensagem: `/note --to <nome> requer $PROJECTS_DIR definido apontando a raiz canonical de projetos. Defina a env var ou use path absoluto.`
    - Target dir inexistente em `$PROJECTS_DIR` → recusar listando até 10 entradas detectadas em `$PROJECTS_DIR/*/`.

  Seguir para "Caminho cross-write" abaixo.

**Caminho local** (sem `--to`): não é um git repo (`git rev-parse` retorna não-zero) → recusar com mensagem `/note exige git repo (store mora em .claude/local/ relativo à raiz)`.

Criar diretório com `mkdir -p .claude/local/` se ausente.

**Ordem dos gates determinística (caminho local apenas)** — gate `Gitignore` (per ADR-047 § Decisão (a)) executa **primeiro**; gate `Worktree replication` (per [ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md) § Decisão (b) `/note` 2º dispatcher) executa **em seguida**. Cancel no gate `Gitignore` aborta antes do segundo gate — evita estado inconsistente onde `.worktreeinclude` referencia path que o operador acabou de recusar versionar.

**Gate `Gitignore`** — probe `git check-ignore -q .claude/local/.probe`. Sem cobertura → disparar gate per ADR-047 § "Local mode" (mecânica já no CLAUDE.md → "Local mode"). Cancel → recusa silenciosa, exit clean. Confirmação → seguir.

**Gate `Worktree replication`** — operação silente, sem `AskUserQuestion`. Probe `grep -qE "^\.claude(/|$)" .worktreeinclude`:

- **`.worktreeinclude` ausente** → criar com header de comentário (`# Gitignored paths to replicate into worktrees created by /run-plan.`) + linha em branco + linha `.claude/`.
- **Presente, probe retorna não-zero** (`.claude/` ausente) → adicionar linha `.claude/` ao fim.
- **Presente, probe retorna zero** (`.claude/` já listado) → skip silente (idempotência).

Mecânica idêntica ao step 4.5 do `/init-config` SKILL.md (linha `.claude/` da tabela composta) — `/note` é segundo dispatcher para a mesma invariante (per ADR-047 § Decisão (b)). Sincronizar mudanças manualmente se a mecânica evoluir num dos lados.

**Caminho cross-write** (com `--to`, per [ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (b)): blast-radius compartilhado proíbe mutar `.gitignore`/`.worktreeinclude` do target a partir de sessão não-contextual — pré-condição substitui gates.

**Pré-condição de target inicializado**: `.claude/local/` no target existe E `git -C <target-repo> check-ignore -q .claude/local/.probe` retorna 0. **Probe idêntico ao usado no caminho local** acima (mesma invariante de ADR-047 § Decisão (b) + § Decisão (a) mecânica — implementador **não deve inventar probe alternativo** tipo `.claude/local/NOTES.md.probe`).

Falha (qualquer um dos checks) → recusar com mensagem: `target <path> não inicializado para modo local; abra sessão CC em <target> e rode /note <msg> uma vez para inicializar gates.`

**Gates assimétricos em cross-write**:

- **Gate `Gitignore`**: opera como **read-only probe** (já validado na pré-condição acima); **não escreve** em `.gitignore` do target em modo algum.
- **Gate `Worktree replication`**: **não roda** em cross-write (nem probe, nem mutação) — replicação para worktrees do target é responsabilidade exclusiva da sessão local do target via `/note` ou `/run-plan` quando o operador trabalhar lá. Assimetria deliberada: gitignore é invariante de privacidade da gravação corrente; worktree-replication é invariante de execução futura no target.

### 2. Append com timestamp

Conteúdo final vazio → recusa silenciosa, retornar sem escrever.

Caso contrário, gerar timestamp UTC (`date -u +%Y-%m-%dT%H:%M:%SZ`) e fazer append em `<target>/.claude/local/NOTES.md` (criar se ausente no caminho local; em cross-write o arquivo é criado se ainda não existe, mas o diretório `.claude/local/` já tem que estar inicializado per § 1 Caminho cross-write) no formato:

```

## <timestamp>

<conteúdo>

```

Linha em branco antes do header, linha em branco depois, conteúdo literal do argumento, linha em branco final. Garante separação clara entre entradas; arquivo permanece append-only e legível corrido.

### 3. Reportar

Path do arquivo e bytes adicionados. Em cross-write, reportar **path absoluto** do target (auditabilidade e desambiguação visual). Operador segue com o trabalho.

## O que NÃO fazer

- Não inferir/sintetizar conteúdo — gravar o argumento literal do operador. A skill não interpreta nem reescreve.
- Não tocar memory nativa CC — `/note` é canal independente; complementa, não substitui. Memory cobre per-project insights conversacionais auto-gravados; `/note` cobre cross-project registro intencional do operador.
- Não auto-buscar contexto em NOTES.md de outros projetos — leitura cross-project é fenômeno conversacional via Read nativo do Claude com path absoluto (operador valida candidato proposto pelo Claude se houver ambiguidade).
- Não fazer commit — `.claude/local/NOTES.md` é gitignored por design; commit acidental quebra o contrato de privacidade.
- Não inferir candidatos para `$PROJECTS_DIR` ausente em cross-write (não tentar `~/Projects/`, `$HOME/dev/`, glob heurístico de filesystem). Critério mecânico contrato-declarado-vs-heurística ([ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (b)) exige recusa explícita orientando definir env var ou usar path absoluto — fallback silencioso fere a doutrina de ADR-054 § Decisão (a) (F4 alternativa b absorvida da ADR-032 § Alternativas).
- Não mutar `.gitignore` ou `.worktreeinclude` do target em cross-write — paralelo doutrinal com ADR-047 § Decisão (a) gate `Gitignore` e § Trade-offs (mutações cross-contextuais ferem blast-radius compartilhado). Pré-condição de target inicializado move setup para a sessão local do target onde o contexto existe para aprovar mudanças nesses arquivos.
