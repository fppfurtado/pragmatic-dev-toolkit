# Plano — `/note --to` para cross-project write

## Contexto

Implementa [ADR-042](../decisions/ADR-042-note-flag-to-cross-project-write.md) — flag opcional `--to <projeto-ou-path>` em `/note` para registrar nota em outro projeto sem trocar de sessão. Sucessor parcial de [ADR-032](../decisions/ADR-032-skill-note-contexto-compartilhado.md) § Decisão e § Limitações.

Pain motivador: varredura empírica de 6 `NOTES.md` em `$PROJECTS_DIR/*/` confirmou cross-project coordination recorrente (`dotfiles` ↔ `loadout` com ≥6 entradas; `drive-sync` ← `chezmoi`; `meta-system` como doctrine container; `pragmatic-dev-toolkit/.claude/local/NOTES.md` linha 4 marcada literalmente como *"Sessão CC: meta-system (cross-repo registration)"*). Hoje o operador switch de sessão ou faz `Write` manual no path absoluto. Flag mecaniza o uso já estabelecido.

**ADRs candidatos:** ADR-042 (decisão central — discovery 2 níveis, pré-condição target inicializado, gate `Worktree replication` não roda em cross-write), ADR-032 (base estendida), ADR-018 (Addendum sobre `/note` como dispatcher de `.worktreeinclude` — relevante para entender por que o gate NÃO replica em cross-write), ADR-005 (modo local base remoto).

**Linha do backlog:** plugin: skill `/note` aceita flag `--to <projeto-ou-path>` para write cross-project (per ADR-042; discovery via `$PROJECTS_DIR` com fallback a path absoluto; pré-condição de target inicializado preserva blast-radius; gate `Worktree replication` não roda em cross-write).

## Resumo da mudança

Adiciona flag opcional `--to <projeto-ou-path>` à skill `/note`. Sem `--to` → comportamento atual preservado intacto (append no repo corrente). Com `--to`:

1. **Resolução do target em 2 níveis**: nome (não contém `/`) → `$PROJECTS_DIR/<nome>/.claude/local/NOTES.md`; path absoluto (começa com `/`) → bypass discovery.
2. **Pré-condição de target inicializado**: `.claude/local/` existe E `git -C <target> check-ignore -q .claude/local/.probe` cobre. Falha → recusa orientando rodar `/note` na sessão local do target.
3. **Gate `Gitignore` opera como read-only probe no target**; **gate `Worktree replication` não roda** em cross-write (assimetria por blast-radius — replicação fica com sessão local do target).
4. **Append timestampado idêntico** ao formato atual.
5. **Output reporta path absoluto** do arquivo escrito + bytes adicionados.

Sem `--to` → caminho atual zero-change. Com `--to` → 1 trilho mecanizado para pattern empírico recorrente.

**Fora de escopo** (por ADR-042 § Limitações; reabertura via § Gatilhos de revisão lá):

- Broadcast multi-target (`--to a,b,c`) — 1-to-1 por invocação.
- Registro de origem mecânico no NOTES.md do target — convenção de prosa-prefácio fica com o operador.
- Modo `--init-target` que inicializa target remotamente — first-time setup requer sessão CC local no target.

## Arquivos a alterar

### Bloco 1a — Argument parsing e target resolution {reviewer: code}

- `skills/note/SKILL.md`:
  - `## Argumentos`: reescrever para descrever 2 modos (sem flag = local; com `--to <projeto-ou-path>` = cross-write). Parsing simples: primeiro token `--to <valor>` se presente; restante = conteúdo.
  - `## Passos` step 1 sub-fluxo de resolução do target:
    - `<valor>` contém `/` → path absoluto direto; senão → `$PROJECTS_DIR/<valor>/.claude/local/NOTES.md`.
    - `$PROJECTS_DIR` ausente + nome → recusar: *"`/note --to <nome>` requer `$PROJECTS_DIR` definido apontando a raiz canonical de projetos. Defina a env var ou use path absoluto."*
    - Target inexistente em `$PROJECTS_DIR` → recusar listando até 10 entradas detectadas em `$PROJECTS_DIR/*/`.
  - `## Passos` step 2: ramo `--to` faz append em `<target>/.claude/local/NOTES.md` (formato idêntico ao local); ramo sem `--to` permanece intacto.
  - `## Passos` step 3 (Reportar): cross-write reporta path absoluto do target + bytes adicionados; sem `--to` segue como hoje.
  - `## O que NÃO fazer`: adicionar bullet — *"Não inferir candidatos para `$PROJECTS_DIR` ausente (não tentar `~/Projects/`, `$HOME/dev/`, glob heurístico). Critério mecânico contrato-declarado-vs-heurística (ADR-042 § Contexto) exige recusa explícita orientando definir env var ou usar path absoluto — fallback silencioso fere a doutrina de ADR-032 § F4 alternativa b."*
- `CLAUDE.md`: tabela "The role contract" — entry `(plugin-internal) | .claude/local/NOTES.md` atualizada mencionando cross-project write via `--to` + cross-ref a ADR-042.

### Bloco 1b — Gates e blast-radius (cross-write) {reviewer: security}

- `skills/note/SKILL.md`:
  - `## Passos` step 1 sub-fluxo de pré-condição do target em cross-write:
    - Probe pré-condição: `.claude/local/` no target existe E `git -C <target-repo> check-ignore -q .claude/local/.probe` retorna 0. **Probe idêntico ao usado pela skill no caminho local** (mesma invariante de ADR-018 Addendum + ADR-005 mecânica — implementador não deve inventar probe alternativo tipo `.claude/local/NOTES.md.probe`).
    - Falha → recusar: *"target `<path>` não inicializado para modo local; abra sessão CC em `<target>` e rode `/note <msg>` uma vez para inicializar gates."*
    - Gate `Gitignore`: read-only probe no target (já validado acima); **não escreve** em `.gitignore` do target em modo algum.
    - Gate `Worktree replication`: **não roda** em cross-write (nem probe, nem mutação) — replicação para worktrees do target é responsabilidade exclusiva da sessão local do target via `/note` ou `/run-plan` quando o operador trabalhar lá.
  - `## O que NÃO fazer`: adicionar bullet — *"Não mutar `.gitignore` ou `.worktreeinclude` do target em cross-write — paralelo doutrinal com ADR-005 § Gate `Gitignore` e ADR-018 § Trade-offs (mutações cross-contextuais ferem blast-radius compartilhado)."*

### Bloco 2 — Documentação user-facing {reviewer: doc}

- `README.md`: atualizar bullet/entrada de `/note` em "What's inside" para mencionar cross-write via `--to`.
- `docs/install.md`: smoke checklist ganha cenário cross-write.

## Verificação end-to-end

Sem `make test` (toolkit não tem suite — convenção do repo). Inspeção textual com 4 invariantes ortogonais (cada grep precisa retornar ≥1 match — probe de existência, não verificação semântica; semântica fica com `## Verificação manual`):

```bash
# SKILL.md cobre 4 invariantes ortogonais
grep -q -- "--to" skills/note/SKILL.md && \
grep -q "PROJECTS_DIR" skills/note/SKILL.md && \
grep -qE "não inicializado|inicializar gates" skills/note/SKILL.md && \
grep -qE "path absoluto" skills/note/SKILL.md && \
echo "SKILL.md OK"

# Docs user-facing refletem nova capability
grep -q -- "--to" README.md && \
grep -qE "cross-project|cross-write" docs/install.md && \
echo "Docs OK"

# CLAUDE.md role contract entry atualizado
grep -qE "ADR-042|cross-project write" CLAUDE.md && echo "CLAUDE.md OK"

# ADR-042 referenciado no SKILL.md
grep -q "ADR-042" skills/note/SKILL.md && echo "ADR ref OK"
```

Esperado: 4 linhas `OK` impressas (zero gaps).

## Verificação manual

Cenários para smoke-test pós-release em consumer real:

1. **Default preservado**: `/note "msg local"` sem `--to` → append em `<repo-corrente>/.claude/local/NOTES.md`, timestamp UTC, formato canonical inalterado.
2. **Cross-write via nome**: `$PROJECTS_DIR=/home/fppfurtado/Projects`; `/note --to loadout "msg cross"` com `loadout/` existente e inicializado → grava em `/home/fppfurtado/Projects/loadout/.claude/local/NOTES.md`; relatório cita o path absoluto.
3. **Cross-write via path absoluto**: `/note --to /storage/dev/projects/meta-system "msg"` → bypass discovery, grava direto.
4. **Target inexistente em `$PROJECTS_DIR`**: `/note --to nome-inexistente "msg"` → recusa listando entradas detectadas em `$PROJECTS_DIR/*/` (sample dos primeiros 10).
5. **Target sem `.claude/local/`**: `/note --to <projeto-sem-init> "msg"` → recusa orientando inicializar localmente.
6. **`$PROJECTS_DIR` ausente + nome**: `unset PROJECTS_DIR; /note --to loadout "msg"` → recusa orientando definir env var ou usar path absoluto.
7. **Gates do target não mutados**: após cenários 2/3, conferir:
   - `git -C <target> status -- .gitignore` → limpo (cobre caso tracked OU untracked-criado-acidentalmente).
   - `.worktreeinclude` pode estar gitignored no target (decisão do consumer per ADR-018), `git status` é falso-negativo nesse caso → comparar `md5sum <target>/.worktreeinclude` antes e depois da invocação (hash idêntico, ou ambos ausentes).
8. **Cross-write não duplica no corrente**: após cenário 2 (ou 3), conferir que `<repo-corrente>/.claude/local/NOTES.md` permanece com mtime/wc-l inalterado (`stat -c %Y` e `wc -l` antes/depois batem). Cobre regressão "implementação grava em ambos os lugares" / "implementação mirrora no corrente como side-effect".

## Notas operacionais

- **Ordem dos blocos**: 1a → 1b → 2. Mecânica (1a + 1b) precede docs (2) para evitar prosa descrevendo comportamento ainda não implementado.
- **Idioma por arquivo**: `README.md` em EN (per [ADR-012](../decisions/ADR-012-idioma-artefatos-discoverability-landing.md)); `docs/install.md` em PT-BR (canonical do repo); `CLAUDE.md` em EN (mecanismo, não prosa). `skills/note/SKILL.md` em PT-BR (skill prose).
- **Blocos 1a e 1b editam o mesmo arquivo** (`skills/note/SKILL.md`). Reviewers operam sobre eixos diferentes (code: parsing/structure; security: gates/blast-radius) — split de bloco isola revisões; commits separados em `/run-plan` reduzem blast-radius por bloco.

## Decisões absorvidas

- `ADR-042 § Alternativas`: added missing Alt B (chosen path as baseline) — Alt C reference no longer orphan (caminho-único).
- `ADR-042 § Alternativas`: added Alt H (path-only no discovery) with rebuttal anchored on critério mecânico (caminho-único).
- `ADR-042 § Alt C rebuttal`: replaced primary argument with ADR-008 parallel (skill detects stack via marker, not separate skills); `/triage` kept as secondary (caminho-único).
- `ADR-042 § Gatilhos de revisão #4`: refined with mechanical threshold (≥3 sessões em 1 mês) replacing vague "atrito recorrente" (caminho-único).
- `plan § Resumo da mudança`: added explicit OUT scope (broadcast, origin tag, init-target) per ADR-042 § Limitações (caminho-único).
- `plan § Bloco 1a § O que NÃO fazer`: added "não inferir candidatos" bullet enforcing critério mecânico contrato-vs-heurística (caminho-único).
- `plan § Bloco 1b`: load-bearing note that target probe (`.claude/local/.probe`) mirrors the existing local probe — prevents implementer from inventing alternate probe (caminho-único).
- `plan § Bloco 1b § O que NÃO fazer`: replaced unstable `/run-plan §1.1` cross-ref with stable ADR refs (ADR-005, ADR-018) (caminho-único).
- `plan § Verificação end-to-end`: tightened from disjunctive grep (false-positive risk) to 4 orthogonal greps chained with `&&`; explicitly marked as existence probe, not semantic check (caminho-único).
- `plan § Verificação manual cenário 7`: reinforced to cover gitignored `.worktreeinclude` (hash compare instead of only `git status`) (caminho-único).
- `plan § Verificação manual cenário 8`: added (cross-write não duplica no NOTES.md corrente) (caminho-único).
- `plan § Notas operacionais`: added (ordem dos blocos, idioma por arquivo, split rationale) (caminho-único).
