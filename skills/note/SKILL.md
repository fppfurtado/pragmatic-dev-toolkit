---
name: note
description: Append uma nota com timestamp no store do role annotations (default .claude/local/NOTES.md, local-gitignored, append-only)
disable-model-invocation: false
roles:
  informational: [annotations]
---

# note

Append uma nota timestampada no store do role `annotations` (default backend `local` → `.claude/local/NOTES.md`) — captura de contexto compartilhado entre sessões CC paralelas, intra-projeto e cross-project (este último via referência conversacional, sem auto-discovery). Per [ADR-072](../../docs/decisions/ADR-072-role-annotations-plugavel-backend-por-projeto.md) o store é o role `annotations` (sucessor parcial de [ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (a), que o estabeleceu sobre [ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md)); backends `local` (default), `logseq` (deferido a meta-bridge#41), `null` (desabilitado).

Esta skill executa o append e devolve controle ao operador. **Não faz commit** — `.claude/local/` é gitignored por design.

Skill opera **standalone** — o default `local` resolve sem `CLAUDE.md` nem config, usável em qualquer git repo. Consome o role `annotations` (`informational`), mas não traversa o step 3 do Resolution protocol (default sempre resolve); a cutucada de descoberta ([ADR-046](../../docs/decisions/ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md)) **não aplica** — isenção preservada por ergonomia standalone (não mais por ausência de papel, per [ADR-072](../../docs/decisions/ADR-072-role-annotations-plugavel-backend-por-projeto.md)).

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

**Resolução do backend `annotations`** (per [ADR-072](../../docs/decisions/ADR-072-role-annotations-plugavel-backend-por-projeto.md)) — resolver logo após o check de git repo acima (que permanece a pré-condição inicial do caminho local) e **antes dos gates de privacidade/replicação (Gitignore/Worktree) e de qualquer mutação FS**:

- **`local` ou ausente** (default) → seguir o fluxo abaixo (`mkdir`, gates, append em `.claude/local/NOTES.md`). Comportamento idêntico ao pré-ADR-072.
- **`null`** → informar que anotações estão desabilitadas no projeto (`paths.annotations: null`) e **retornar sem gravar, antes dos gates Gitignore/Worktree** — nenhuma mutação FS; o 2º dispatcher `.worktreeinclude` **não roda** (exceção consciente à universalidade de ADR-047 § Decisão (b): não há store a replicar).
- **`logseq`** → backend deferido (write-path v2 não construído, meta-bridge#41); graceful-degrade — reportar que o backend `logseq` ainda não está disponível e **retornar sem gravar, antes dos gates Gitignore/Worktree** (mesmo tratamento de `null`: o 2º dispatcher `.worktreeinclude` **não roda** — não há store local a replicar).

Criar diretório com `mkdir -p .claude/local/` se ausente.

**Ordem dos gates determinística (caminho local apenas)** — gate `Gitignore` (per ADR-047 § Decisão (a)) executa **primeiro**; gate `Worktree replication` (per [ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md) § Decisão (b) `/note` 2º dispatcher) executa **em seguida**. Cancel no gate `Gitignore` aborta antes do segundo gate — evita estado inconsistente onde `.worktreeinclude` referencia path que o operador acabou de recusar versionar.

**Gate `Gitignore`** — probe `git check-ignore -q .claude/local/.probe`. Sem cobertura → disparar gate per ADR-047 § "Local mode" (mecânica já no CLAUDE.md → "Local mode"). Cancel → recusa silenciosa, exit clean. Confirmação → seguir.

**Gate `Worktree replication`** — operação silente, sem `AskUserQuestion`. Probe `grep -qE "^\.claude(/|$)" .worktreeinclude`:

- **`.worktreeinclude` ausente** → criar com header de comentário (`# Gitignored paths to replicate into worktrees created by /run-plan.`) + linha em branco + linha `.claude/`.
- **Presente, probe retorna não-zero** (`.claude/` ausente) → adicionar linha `.claude/` ao fim.
- **Presente, probe retorna zero** (`.claude/` já listado) → skip silente (idempotência).

Mecânica idêntica ao step 4.5 do `/init-config` SKILL.md (linha `.claude/` da tabela composta) — `/note` é segundo dispatcher para a mesma invariante (per ADR-047 § Decisão (b)). Sincronizar mudanças manualmente se a mecânica evoluir num dos lados.

**Caminho cross-write** (com `--to`, per [ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (b)): blast-radius compartilhado proíbe mutar `.gitignore`/`.worktreeinclude` do target a partir de sessão não-contextual — pré-condição substitui gates. **Backend (per [ADR-072](../../docs/decisions/ADR-072-role-annotations-plugavel-backend-por-projeto.md)):** cross-write opera sobre o backend `local` do target por construção (escreve em `<target>/.claude/local/NOTES.md`); a pré-condição de target inicializado abaixo já pressupõe modo local. O backend da origem (projeto corrente) **não é consultado** em `--to` — cross-write é governado exclusivamente pelo backend do target. Resolução de backend `null`/`logseq` do target é fora de escopo deste v1 — o caminho `--to` é local-NOTES-específico.

**Pré-condição de target inicializado**: `.claude/local/` no target existe E `git -C <target-repo> check-ignore -q .claude/local/.probe` retorna 0. **Probe idêntico ao usado no caminho local** acima (mesma invariante de ADR-047 § Decisão (b) + § Decisão (a) mecânica — implementador **não deve inventar probe alternativo** tipo `.claude/local/NOTES.md.probe`).

Falha (qualquer um dos checks) → recusar com mensagem: `target <path> não inicializado para modo local; abra sessão CC em <target> e rode /note <msg> uma vez para inicializar gates.`

**Bootstrap moment** — quando o target é repo recém-criado onde `.claude/local/` ainda não existe e o operador não tem sessão CC aberta nele (deadlock: `/note` exige init, mas init exige sessão no target), inicializar manualmente **antes** do primeiro cross-write (executado pelo operador, não pela skill — skill nunca muta `.gitignore` do target):

```sh
mkdir -p <path-absoluto-do-target>/.claude/local/
echo '.claude/local/' >> <path-absoluto-do-target>/.gitignore
```

Após isso, `/note --to <target> <conteúdo>` passa a pré-condição. Ato one-time de bootstrap; mutação do `.gitignore` do target pela skill continua proibida per `§ O que NÃO fazer`.

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
