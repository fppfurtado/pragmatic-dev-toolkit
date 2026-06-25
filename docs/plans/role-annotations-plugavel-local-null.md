# Plano — Role `annotations` plugável (backends local/null)

## Status

Pendente

## Contexto

Materializa [ADR-072](../decisions/ADR-072-role-annotations-plugavel-backend-por-projeto.md): promover o store de anotações de *non-role* (ADR-054 § Decisão (a)) → role `annotations` de primeira classe, com backend plugável por projeto. Escopo deste plano = backends `local` (default, = comportamento atual) + `null` (desliga); backend `logseq` **fora de escopo**, deferido a meta-bridge#41 (write-path v2 não-construído) — skill degrada graceful quando `logseq` declarado sem o write-path.

Operacionaliza no toolkit o contrato pai meta-system ADR-025 (coerência de pendências cross-store, Aceito). Filho rastreado como issue #154.

**ADRs candidatos:** ADR-072 (a decisão que este plano materializa), ADR-054 (classificação non-role revisada — preservar demais sub-decisões), ADR-058 (precedente do eixo `paths.<role>: <modo>` para `backlog: forge`), ADR-047 (modo local / regra de não-referenciar — já cobre backend `local`), ADR-003 (schema `roles:` no frontmatter).

**Prior-art scan:** construir — plumbing de role-contract interno sem equivalente de mercado; o backend `logseq` (adotar Logseq HTTP API) está fora de escopo e já rastreado em meta-bridge#41 per ADR-025 § Prior-art.

**Linha do backlog:** #154: Role `annotations` (backends local/logseq/null) — revisar non-role do ADR-054

## Resumo da mudança

**Entra:** role `annotations` documentado no role-contract (CLAUDE.md) + resolvido pelas 5 skills consumidoras (`/note` write; `/next`, `/triage`, `/session-audit`, `/curate-backlog` read) via Resolution protocol, com backends `local` (default → `.claude/local/NOTES.md`, comportamento idêntico ao atual) e `null` (skip silente).

**Fica de fora:** backend `logseq` (deferido a meta-bridge#41) — declarável mas não-funcional (graceful-degrade como backend ausente, padrão `backlog: forge` sem `gh`); o *reconciler* (meta-bridge#42) é ortogonal. **Signal-queue de coordenação fora do role (escopo (a)):** a fila worktree-defer de `/curate-backlog`/`/session-audit` + a baixa do gate ADR-069 permanecem sempre em `.claude/local/NOTES.md`, qualquer backend — são mecanismo de concorrência local, não conteúdo de anotação. A separação física da fila num arquivo próprio (escopo (c)) foi **deferida a issue #157**.

**Decisões-chave:**
- **`/note` mantém usabilidade standalone.** Hoje ADR-054 § (a) declara `/note` "independente do role contract". Com o role, `/note` passa a declarar `annotations` no frontmatter, mas o **default `local` resolve sem exigir config** — `/note` segue usável em qualquer git repo sem `CLAUDE.md`. Preserva-se a cláusula ADR-054 de que `/note` **não emite a cutucada de descoberta** (default local silencioso; o role degrada para o path fixo histórico quando não declarado).
- **Backend `null` em `/note`:** quando `paths.annotations: null`, `/note` informa em prosa que anotações estão desabilitadas no projeto e não grava (paralelo a papel `backlog` "não temos").
- **Âncoras non-role de `/curate-backlog` reformuladas:** linhas 92/190 citam "ADR-054 § (a) NOTES non-role" como justificativa de H4 informacional — reformular para "role `annotations` backend `local` (ADR-072)"; o caráter informacional de H4 **não muda** (a justificativa muda de "non-role" para "role read-only neste consumidor").

## Arquivos a alterar

### Bloco 1 — Role contract `annotations` em CLAUDE.md {reviewer: doc}

- `CLAUDE.md`: adicionar linha `annotations` à tabela "The role contract" (default `.claude/local/NOTES.md`; descrição = store de anotações de sessão, backend plugável). Mover a entrada hoje listada como `(plugin-internal) | .claude/local/NOTES.md` para a nova linha de role, cross-ref a ADR-072 e ADR-054.
- `CLAUDE.md` § "Pragmatic Toolkit": documentar `paths.annotations: <local|logseq|null>` no schema — `local` default, `logseq` deferido (graceful-degrade até meta-bridge#41), `null` desliga, **sem `forge`** (anotação ≠ tarefa). Nota de que `logseq` é v-futuro.
- `CLAUDE.md` § Resolution protocol / Local mode: `annotations` aceita modo `local` (já é o default); incluir na lista de roles que aceitam `local`.

### Bloco 2 — `/note` consome role `annotations` (write-side) {reviewer: prompt}

- `skills/note/SKILL.md` **frontmatter:** declarar `annotations` em `roles.informational` (não `required`) — o default `local` sempre resolve, nunca bloqueia, nunca dispara o Resolution protocol step 3 (ask/memoization). `required` arrastaria a maquinaria de cutucada que contradiz a decisão standalone (Resumo). Coerência com ADR-003 § Schema (criticidade obrigatória por lista).
- `skills/note/SKILL.md` **ordem de resolução no passo 1** (resolve finding design-reviewer #2): resolver `annotations` **no topo do passo 1, antes dos gates**. `local`/ausente → fluxo de gates atual intacto (Gitignore → `.worktreeinclude`, `note:45`) + append timestampado em `.claude/local/NOTES.md`. `null` → informar desabilitado e **retornar antes de ambos os gates** — nenhuma mutação FS; o 2º dispatcher `.worktreeinclude` **não roda** (exceção consciente à universalidade de ADR-047 § (b), justificada: não há store a replicar). `logseq` → graceful-degrade (reportar backend não-construído, cross-ref meta-bridge#41).
- `skills/note/SKILL.md` **reformular âncora `note:13`** (resolve finding design-reviewer #4): hoje diz "skill não consome papel → cutucada não aplica" — vira factualmente falso (passa a consumir `annotations`). Reformular para: "`/note` consome `annotations` (informational), mas o default `local` resolve sem config e a skill não traversa o step 3 de ask; a cutucada de descoberta continua **não-aplicável** — isenção preservada por ergonomia standalone, não mais por ausência de papel." Análogo à reformulação de âncoras do Bloco 4.
- Preservar toda a demais mecânica `/note` de ADR-054 § (a)/(b) (`--to`, discovery `$PROJECTS_DIR`).

### Bloco 3 — read-consumers `/next`, `/triage`, `/session-audit` {reviewer: prompt}

- `skills/next/SKILL.md`: o passo que lê `.claude/local/NOTES.md` para contexto de ranking resolve via role `annotations` (`local`/ausente → read atual; `null` → skip silente; `logseq` → graceful-degrade read vazio). Semântica informational preservada.
- `skills/triage/SKILL.md`: idem nos sites que leem NOTES (step 1 contexto + gate verify-state-before-materialize do step 4).
- `skills/session-audit/SKILL.md`: resolução do role nos reads de NOTES **e** no write-side `captura_notes` (linha 131, `Edit` append) — `local`/ausente → append atual; `null` → skip silente do append (sem store, paralelo ao read); `logseq` → graceful-degrade. **Fora do role (escopo (a)):** o write-side de **coordenação** — defer signal-queue (127) + baixa do gate ADR-069 (127/129) — permanece sempre em `.claude/local/NOTES.md`, qualquer backend; é mecanismo de concorrência local, não conteúdo de anotação (separação física deferida a issue própria — ver Notas operacionais).

### Bloco 4 — `/curate-backlog` resolve role (H4 read) + reformula âncoras non-role {reviewer: prompt}

- `skills/curate-backlog/SKILL.md`: **H4 (read de sinais)** resolve via role `annotations` (conteúdo de anotação — `local`/ausente → read atual; `null` → H4 no-op silente; `logseq` → graceful-degrade). **Fora do role (escopo (a)):** a signal-queue worktree-deferred (write linha 151 + drain linha 180) permanece sempre em `.claude/local/NOTES.md`, qualquer backend — mecanismo de coordenação local, não conteúdo de anotação.
- Reformular as duas âncoras textuais "NOTES.md non-role (ADR-054 § (a))" (linhas ~92 e ~190) para "role `annotations` backend `local` (ADR-072)" — o caráter informacional de H4 permanece; só a justificativa doutrinária é atualizada para a classificação vigente.

## Verificação end-to-end

- Cada um dos 5 SKILLs consumidores ganha cross-ref a `annotations` na vizinhança dos sites de NOTES: `grep -c "annotations" skills/<skill>/SKILL.md ≥ 1` para `note`, `next`, `triage`, `session-audit`, `curate-backlog` (predicado mecânico que substitui o julgamento "fora do caminho de resolução" — finding design-reviewer #6).
- `grep -n "não consome papel\|status non-role\|NOTES.md non-role" skills/note/SKILL.md skills/curate-backlog/SKILL.md` retorna 0 (âncoras non-role reformuladas para role).
- `grep -c "annotations" CLAUDE.md` ≥ 3 (tabela + schema + Resolution protocol).
- Frontmatter de `skills/note/SKILL.md` declara `annotations` em `roles.informational` (lista correta, não só presença da string).
- Nenhuma das 5 skills referencia backend `forge` para `annotations`.

A inspeção "nenhum site ignora a resolução do role" (exige julgamento linha-a-linha) move-se para `## Verificação manual` C5 abaixo, não como gate grep.

## Verificação manual

Surface não-determinística (comportamento de skill resolvendo role em runtime) → smoke pós-`/reload-plugins` em sessão CC real:

- **C1 — default local:** projeto sem `paths.annotations` declarado. `/note "teste"` grava em `.claude/local/NOTES.md` exatamente como hoje; `/next`/`/triage` leem o store. Comportamento idêntico ao pré-ADR-072.
- **C2 — null:** `paths.annotations: null` no `CLAUDE.md` consumidor. `/note "x"` informa anotações desabilitadas e não grava; `/next`/`/triage`/`/session-audit`/`/curate-backlog` H4 pulam o read silentemente.
- **C3 — logseq graceful:** `paths.annotations: logseq` declarado (write-path #41 não-construído). `/note` reporta backend não-construído (cross-ref #41) sem crashar; reads degradam para vazio.
- **C4 — standalone:** `/note` em git repo sem `CLAUDE.md` → default local funciona, sem cutucada de descoberta.
- **C5 — write sob null:** `paths.annotations: null` + acionar `/session-audit` com finding `captura_notes` → append é pulado silentemente (sem store), captura reportada como desabilitada. Inspeção textual: nenhum dos 5 SKILLs grava/lê NOTES ignorando a resolução do role (item movido do gate grep da Verificação end-to-end — exige julgamento linha-a-linha).

## Pendências de validação

- `[capture:validacao]` Smoke comportamental C1–C5 do `## Verificação manual` pós-`/reload-plugins` em sessão CC real — exige plugin recarregado + julgamento sobre o fluxo das 5 skills; não exercitável na execução do `/run-plan`. Operador roda manual; promover ADR-072 `Proposto` → `Aceito (YYYY-MM-DD)` após ≥1 invocação real bem-sucedida (default-local idêntico + null skip).

## Notas operacionais

- **Ordem dos blocos:** Bloco 1 (CLAUDE.md role contract) primeiro — estabelece o contrato que os Blocos 2-4 consomem. Blocos 2-4 independentes entre si depois.
- **Escopo (c) deferido:** a separação física da signal-queue de coordenação num arquivo próprio (fora de NOTES.md) é **issue #157**, refactor independente do mecanismo ADR-057. Este plano mantém escopo (a): role governa só conteúdo de anotação; coordenação fica always-local. Não bundlar #157 aqui.
- **Atenção para reviewers (`prompt-reviewer` Blocos 2-4):** o fio condutor é "resolver `annotations` no site de conteúdo, deixar a signal-queue de coordenação intacta/local". Confundir os dois usos de NOTES.md é o erro provável a vigiar.

## Decisões absorvidas

- Bloco 3/4 (write-paths NOTES): `/session-audit` e `/curate-backlog` reconhecidos como write-consumers, não só read; `captura_notes` resolve via role (`null` → skip), coordenação worktree-defer fica fora do role (escopo (a)) (caminho-único na parte de conteúdo; bifurcação de escopo (b)/(c) cutucada ao operador → (a) + issue #157).
- Bloco 2 (ordem gates `/note` sob `null`): resolver `annotations` no topo do passo 1; `null` aborta antes dos gates Gitignore/`.worktreeinclude`, sem mutação FS (caminho-único).
- Bloco 2 (frontmatter): `annotations` declarado em `roles.informational`, não `required` — default `local` sempre resolve, coerente com a decisão standalone-sem-cutucada (caminho-único).
- Bloco 2 (âncora `note:13`): reformulada de "skill não consome papel" para isenção da cutucada por ergonomia standalone (caminho-único).
- Verificação end-to-end: critério grep não-mecânico substituído por `grep -c annotations` por skill + inspeção de julgamento movida para C5 manual (caminho-único).
