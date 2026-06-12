# Plano — Gate Worktree replication no /note

## Contexto

ADR-032 introduziu `/note` em 2026-05-15 como skill independente de role contract: NOTES.md é "store doutrinário fixo non-role" sob `.claude/local/NOTES.md`, gravado em qualquer git repo, sem precisar declarar `paths.<role>: local`. ADR-018 (2026-05-11) atribuiu a `/init-config` a responsabilidade proativa pela invariante "`.claude/` listado em `.worktreeinclude`" — mas o gate só dispara quando ≥1 role foi configurada como `local`. Resultado: operador que usa `/note` num projeto sem role local fica com `NOTES.md` fora da worktree quando `/run-plan` executa em modo canonical (worktree não enxerga o arquivo).

ADR-018 § Gatilhos de revisão antecipou exatamente este caso: *"Plugin ganhar segundo path canonical que precise replicação (além de `.claude/local/`) — re-avaliar se `/init-config` é o lugar certo para gerenciar"*. ADR-032 caiu nesse gatilho mas não reabriu ADR-018, criando inconsistência editorial silenciosa.

A linha 23 do atual `skills/note/SKILL.md` já menciona *"Plus gate 'Worktree replication' via ADR-018 se aplicável (`.claude/` listado no `.worktreeinclude`)"* — mas a redação é ambígua: não especifica probe, ramificações, nem quando "aplicável" dispara. O plano materializa a wiring intencional explicitando a mecânica e sela a doutrina via adendo em ADR-018 + cross-ref em ADR-032.

Decisões-chave (alinhadas em raw-chat 2026-05-27):

- **Disparo:** sempre, idempotente. Probe a cada invocação; skip silente se invariante satisfeita. Sem state-keeping.
- **Combinação com gate Gitignore:** não combinar. Gate Gitignore (ADR-005) continua `AskUserQuestion` (política git do consumer); gate Worktree replication permanece silent + determinístico (semântica instrumental, per ADR-018 § Decisão).
- **Forma do registro doutrinário:** adendo em ADR-018 + cross-ref em ADR-032 § Limitações. Critério ADR-034 de adendo aplicado (decisão central intacta + sem nova categoria + sem restrição externa + caráter explicativo de extensão de dispatcher).

**ADRs candidatos:** ADR-018 (recebe adendo registrando segundo dispatcher), ADR-032 (recebe cross-ref em § Decisão), ADR-005 (recebe cross-ref em § Decisão linha 48 e § Benefícios linha 75 para refletir segundo dispatcher do gate worktree replication, paralelo a ADR-025/87 → ADR-018).

**Linha do backlog:** plugin: gate Worktree replication no /note via probe-and-add idempotente — fecha gap ADR-018/ADR-032 (NOTES.md como store non-role, independente de role local declarada).

## Resumo da mudança

`skills/note/SKILL.md` passo 1 ganha mecânica explícita do gate Worktree replication: probe regex `^\.claude(/|$)` em `.worktreeinclude` com 3 ramos (criar arquivo com header + `.claude/`; adicionar linha `.claude/`; skip silente). Operação silente, sem `AskUserQuestion`. Espelha o sub-bloco já presente em `skills/init-config/SKILL.md` step 4.5 tabela linha `.claude/`, mas com trigger universal (toda invocação do `/note`) em vez de condicional a role local.

`docs/decisions/ADR-018-...md` ganha seção `## Addendum (2026-05-27)` registrando: (a) `/note` se torna segundo dispatcher para a mesma invariante; (b) decisão central preservada; (c) trigger universal no `/note` independente de role local; (d) `/init-config` permanece dono no caminho setup-driven.

`docs/decisions/ADR-032-...md` § Limitações ganha bullet cross-ref ao adendo do ADR-018.

`/init-config` step 4.5 **não** é alterado — continua disparando quando ≥1 role local. Os dois gates são independentes e idempotentes (cobertura defensiva sem conflito). `docs/decisions/ADR-005-modo-local-gitignored-roles.md` § Decisão linha 48 e § Benefícios linha 75 recebem cross-ref ao adendo de ADR-018, paralelo ao pattern de ADR-005:87 → ADR-025.

## Arquivos a alterar

### Bloco 1 — gate Worktree replication explícito no /note SKILL.md {reviewer: code}

- `skills/note/SKILL.md` passo 1 ("Garantir store"): substituir a frase ambígua *"Plus gate 'Worktree replication' via ADR-018 se aplicável (`.claude/` listado no `.worktreeinclude`)"* por mecanismo explícito com:
  - **Ordem dos gates determinística:** probe gitignore + eventual gate `Gitignore` (per ADR-005, `AskUserQuestion`) executa **primeiro**; probe worktree replication + eventual write executa **em seguida**. Cancel no gate `Gitignore` aborta antes do segundo gate (evita estado inconsistente: `.worktreeinclude` referenciando path que o operador recusou versionar).
  - Probe `grep -qE "^\.claude(/|$)" .worktreeinclude` (compatível com presença com/sem trailing slash).
  - **`.worktreeinclude` ausente:** criar com header de comentário (`# Gitignored paths to replicate into worktrees created by /run-plan.`) + linha em branco + `.claude/`.
  - **Presente, probe não-zero (`.claude/` ausente):** adicionar `.claude/` ao final.
  - **Presente, probe zero (`.claude/` já listado):** skip silente.
  - Operação determinística, sem `AskUserQuestion`.
  - Cross-ref textual ao ADR-018 adendo na prosa, declarando explicitamente *"mecânica idêntica ao step 4.5 do `/init-config` SKILL.md, linha `.claude/` da tabela"* como fonte canônica do pattern (drift control editorial).

### Bloco 2 — adendo em ADR-018 + cross-refs em ADR-005 e ADR-032 {reviewer: doc}

- `docs/decisions/ADR-018-replicacao-claude-em-modo-local-init-config.md`: adicionar `## Addendum (2026-05-27)` ao final do arquivo cobrindo:
  - **Origem:** ADR-032 (2026-05-15) introduziu NOTES.md como store non-role sob `.claude/local/`, dissociado de role contract. `/note` opera em projetos sem role local declarada, e a invariante "`.claude/` em `.worktreeinclude`" passou a depender de skill fora do escopo do `/init-config`.
  - **Extensão:** `/note` se torna segundo dispatcher para a mesma invariante; mecânica idêntica (probe regex `^\.claude(/|$)`, 3 ramos: criar/adicionar/skip), idempotente cross-skill.
  - **Trigger no `/note` é universal** (toda invocação) — diferente do `/init-config` step 4.5 (condicional a `≥1 role local`). Não há perda de simetria: invariante é a mesma, `.claude/` cobre `.claude/local/<role>/` e `.claude/local/NOTES.md` simultaneamente.
  - **`/init-config` permanece dono no caminho setup-driven**; safety net do `/run-plan` SKILL.md:36 preservado para casos edge.
  - **Gatilho de revisão de § Gatilhos** ("Plugin ganhar segundo path canonical que precise replicação"): acionado em duas ondas — ADR-030 (`CLAUDE.md`, mesmo dispatcher `/init-config`) e este adendo (`/note`, dispatcher novo para o path `.claude/` pré-existente). Extração para skill própria de setup de worktree avaliada e descartada — dispatchers permanecem distribuídos por skill que tem o sinal de configuração na mão (init-config = role declaration; note = ad-hoc capture), idempotência cross-skill cobre conflito mecânico. Reabrir se 4º dispatcher emergir → extrair pattern para `docs/procedures/worktree-replication-dispatch.md` (paralelo direto com ADR-029 § Gatilhos sobre cutucada-emitting skills).
  - **Justificativa de adendo (vs novo ADR sucessor parcial):** ADR-034 critério 5 (sucessor parcial) é defensável aqui, mas o eixo de extensão é diferente do precedente ADR-030. ADR-030 introduziu **novo path** (`CLAUDE.md`) coberto pelo **mesmo dispatcher** (`/init-config` step 4.5 tabela linha nova) → mecânica composta, novo ADR sucessor justificado. Este adendo introduz **novo dispatcher** (`/note` passo 1) para o **mesmo path** (`.claude/`) → mecânica replicada, decisão central do ADR-018 (probe regex + 3 ramos + idempotência) preservada intacta. ADR-034 critérios de adendo (4/4): decisão central intacta + sem nova categoria conceitual de artefato + sem restrição externa + caráter explicativo da extensão. Assimetria com ADR-030 é deliberada e amarrada ao critério ADR-034.

- `docs/decisions/ADR-005-modo-local-gitignored-roles.md` § Decisão linha 48 e § Benefícios linha 75: adicionar parágrafo cross-ref ao adendo de ADR-018 registrando que `/note` opera como segundo dispatcher independente de role local declarada, mantendo a invariante. Pattern paralelo a ADR-005:87 → ADR-025 (mesma forma de cross-ref inline em ADRs sucessores).

- `docs/decisions/ADR-032-skill-note-contexto-compartilhado.md` § Decisão (após bullet 1 "Store em `.claude/local/NOTES.md`..."): adicionar parágrafo cross-ref ao adendo do ADR-018, registrando que `/note` passo 1 aplica silentemente a invariante `.claude/` em `.worktreeinclude` por probe-and-add idempotente, garantindo que worktrees do `/run-plan` enxerguem `NOTES.md`. Pattern paralelo a ADR-011 § Decisão / ADR-026 (extensão funcional em § Decisão, não § Limitações).

## Verificação end-to-end

Plugin sem test suite (`test_command: null` no bloco config). Inspeção textual:

- `grep -n "probe" skills/note/SKILL.md` retorna linha do passo 1 com mecanismo explícito (não a frase "se aplicável" pré-existente).
- `grep -n "grep -qE" skills/note/SKILL.md` confirma probe regex literal.
- `grep -n "Addendum" docs/decisions/ADR-018-*.md` mostra seção nova com data e referência a `/note`.
- `grep -n "ADR-018" docs/decisions/ADR-032-*.md` mostra cross-ref em § Decisão (após bullet 1).
- `grep -n "ADR-018" docs/decisions/ADR-005-*.md` mostra cross-refs adicionadas (linhas 48 e 75 refletindo segundo dispatcher).
- Validador de manifests CI lint continua passando (sem alteração em `.claude-plugin/`).

## Verificação manual

Cenários enumerados (smoke pós-release em consumer real):

1. **Repo sem `.worktreeinclude` + .gitignore cobre `.claude/local/`:** `/note "smoke 1"` → cria `.worktreeinclude` com header + linha `.claude/`; `NOTES.md` gravado em `.claude/local/`; nenhuma `AskUserQuestion` para worktree replication.
2. **Repo com `.worktreeinclude` sem `.claude/`:** `/note "smoke 2"` → adiciona linha `.claude/` ao final do arquivo existente; `NOTES.md` gravado; sem fricção visível.
3. **Repo com `.worktreeinclude` já listando `.claude/`:** `/note "smoke 3"` → skip silente na linha (probe zero); `NOTES.md` gravado.
4. **Repo com `.worktreeinclude` listando apenas `.claude/local/` (falso-negativo benigno do probe):** `/note "smoke 4"` → adiciona linha `.claude/` redundante per ADR-018 § Limitações; sem dano funcional.
5. **Gate Gitignore concorrente:** `.claude/local/` **não** está em `.gitignore`. `/note "smoke 5"` → gate Gitignore (`AskUserQuestion`) dispara primeiro per ADR-005; após confirmação, gate Worktree replication dispara silente. Dois gates separados, semânticas distintas preservadas (operador confirma apenas o gitignore).
6. **Não é git repo:** `/note "smoke 6"` → recusa per mensagem existente (`/note exige git repo...`); nenhum dos gates dispara.
7. **Idempotência cross-skill (`/init-config` → `/note`):** `/init-config` rodado antes adicionou `.claude/` (≥1 role local); `/note "smoke 7"` → probe zero, skip silente. Simétrico (`/note` primeiro, depois `/init-config`): segundo dispatcher também vê linha presente → skip silente.

## Notas operacionais

- **Ordem dos blocos:** Bloco 1 antes do Bloco 2. Bloco 2 referencia mecânica que Bloco 1 introduz — sequência respeita "decisão antes da documentação cross-ref" embora ambos vão no mesmo commit final consolidado pelo `/run-plan`.
- **`/init-config` step 4.5 inalterado:** continuar disparando quando ≥1 role local. Defesa em camadas idempotente; nunca em conflito.
- **`/run-plan` safety net (SKILL.md:36) preservado:** bloqueio per modo local + `.worktreeinclude` ausente é último recurso quando algo apaga a linha entre invocações.
- **Reviewer Bloco 2 = doc-reviewer:** paths todos `.md`, drift cross-ref ADR-018 ↔ ADR-032 ↔ ADR-005 e consistência de format/numbering como critérios primários (não code-reviewer).

## Decisões absorvidas

- ADR-005 (linha 48 e 75): cross-ref ao adendo ADR-018 adicionado ao Bloco 2 — paraleliza pattern de ADR-005:87 → ADR-025 e fecha gap editorial entre cadeia "modo local" (caminho-único).
- ADR-018 adendo: parágrafo endereçando explicitamente gatilho de revisão de § Gatilhos (segundo path canonical), citando ADR-030 + descartando "extrair para skill própria" (caminho-único).
- Bloco 1 SKILL.md: ordem dos gates determinística (Gitignore primeiro, Worktree replication em seguida; cancel aborta) materializada como sub-bullet explícito (caminho-único).
- ADR-032 cross-ref: movido de § Limitações para § Decisão após bullet 1 — pattern paralelo a ADR-011 § Decisão / ADR-026 (extensão funcional, não limitação aberta) (caminho-único).
