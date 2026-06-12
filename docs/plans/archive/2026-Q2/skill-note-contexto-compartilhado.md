# Plano — skill `/note` para contexto compartilhado em `.claude/local/NOTES.md`

## Contexto

Dev solo operando ≥3 sessões Claude Code em paralelo perde frescor mental do contexto entre sessões. Três fricções concretas (elicitação 2026-05-15):

1. **Paralelismo intra-projeto** — manter mentalmente o que cada sessão sabe/decidiu fica complicado com várias sessões ativas no mesmo projeto.
2. **Contexto transversal** — sessão B precisa tratar algo que emergiu na sessão A; operador hoje descreve manualmente (cópia-cola, resumo redigido).
3. **Cross-project pai/dependência** — investigar bug no projeto-pai descobre que se estende à dependência; abrir sessão na dependência exige recarregar à mão o que já foi descoberto. Caso recente: `/storage/3. Resources/Projects/tjpa/pje-2.1` ↔ `/storage/3. Resources/Projects/tjpa/connector-pje-mandamus-tjpa` (sessão `pje-issue-1920`).

Critérios de sucesso (cristalizados na elicitação):

1. Recuperação seletiva de info-chave sem reler N arquivos nem a sessão inteira.
2. Acesso cross-project **referenciável** (não-automático — operador ou Claude pode citar o path durante a conversa).
3. Fricção menor que ganho de re-contextualização.

Decisão central (cutucadas Q1+Q2 do `/triage` 2026-05-15 + F2+F4 do design-reviewer):

- **Q1 = B (modo local-gitignored).** Store mora em `.claude/local/NOTES.md`. Por-projeto, não-versionado.
- **Q2 = A (operador via skill `/note`).** Captura é operador-driven: skill nova `/note <conteúdo>` grava no store. Curadoria sustentável.
- **F2 = (a) Extensão de ADR-005.** ADR-005 cobre 3 roles do path contract com canonical default e modo local opcional. NOTES.md é qualitativamente diferente: local **por design** (canonical committed vazaria privacidade), sem alternativa de path, sem schema declarável. Este plano materializa **extensão** de ADR-005 para nova categoria: *store doutrinário fixo non-role em `.claude/local/`*. Segue precedente da entrada `(plugin-internal) | .worktreeinclude` na tabela "The role contract" — entrada non-role doutrinária.
- **F4 = (c) Fenômeno conversacional.** Skill `/note` é pura gravação. Leitura cross-project não tem mecanismo na skill — Claude resolve com contexto da conversa (cwd, projetos já acessados, menções); quando ambíguo, propõe candidatos via prosa e operador confirma ou fornece path absoluto. Sem auto-discovery, sem skill complementar.
- **Complementa memory nativa CC** (sem substituir). Memory cobre per-project insights conversacionais auto-gravados; `/note` cobre cross-project registro intencional do operador. Outputs distintos, escopos distintos.

**ADRs candidatos:** [ADR-005](../decisions/ADR-005-modo-local-gitignored-roles.md) (sucessor parcial — estende para nova categoria non-role), [ADR-004](../decisions/ADR-004-state-tracking-em-git.md) (tensão a reconciliar — NOTES.md não é work-in-flight state, é registro editorial análogo a `## Concluídos`), [ADR-018](../decisions/ADR-018-replicacao-claude-em-modo-local-init-config.md) (replicação de `.claude/` em worktree), [ADR-003](../decisions/ADR-003-frontmatter-roles.md) (schema de roles — autoriza omitir `roles:` quando ambas listas vazias).

**Linha do backlog:** plugin: skill `/note <conteúdo>` para captura de contexto compartilhado em `.claude/local/NOTES.md` (modo local-gitignored estendendo ADR-005 para store non-role); cobre paralelismo intra-projeto + cross-project via referência conversacional do operador.

## Resumo da mudança

1. **Skill nova `/note`** — `skills/note/SKILL.md`. Frontmatter padrão **sem bloco `roles:`** (ADR-003 § Schema autoriza omitir quando ambas listas vazias). Argumento: string com conteúdo da nota. Mecânica: append em `.claude/local/NOTES.md` com timestamp ISO 8601 UTC. Conteúdo final vazio (operador cancela ou submete vazio) → recusa silenciosa, exit clean.
2. **Catálogo `README.md`** — entrada na tabela "What's inside" descrevendo `/note`.
3. **Smoke list `docs/install.md`** — entrada de `/note` na lista de skills disponíveis.
4. **Entrada non-role em `CLAUDE.md`** — linha nova na tabela "The role contract" para `(plugin-internal) | .claude/local/NOTES.md`, seguindo precedente da entrada `.worktreeinclude`.
5. **ADR-032** (stub criado via `/new-adr`; preenchido pelo `/run-plan` Bloco 3) — registra a decisão B+A+F2(a)+F4(c), extensão de ADR-005, reconciliação com ADR-004, opção deliberada de leitura cross-project como fenômeno conversacional.

Fora de escopo:
- Skill de busca/listagem (`/notes-show`, `/notes-grep`).
- Hook de captura automática (Q2 descartou).
- Sincronização cross-project (referência conversacional basta).
- Formato estruturado/schema (markdown corrido com timestamps; YAGNI).
- Promover `notes` a role no path contract (F2 escolheu extensão non-role).

## Arquivos a alterar

### Bloco 1 — criar `skills/note/SKILL.md` {reviewer: code}

- `skills/note/SKILL.md`: skill nova. Estrutura:
  - Frontmatter: `name: note`, `description: Append uma nota com timestamp em .claude/local/NOTES.md (store local-gitignored estendendo ADR-005, modo append-only)`, `disable-model-invocation: false` per ADR-023 (critério 1 — blast radius local em arquivo gitignored sem push/PR — e critério 3 — sem loop autoinvocado cross-turn; critério 2 não-aplicável, skill sem ação cross-team). **Sem bloco `roles:`** per ADR-003 § Schema (ambas listas vazias → omitir).
  - `## Argumentos`: string com conteúdo da nota. Sem argumento → pedir conteúdo em prosa livre (não enum). Conteúdo final vazio (operador cancela ou submete vazio) → recusa silenciosa, exit clean.
  - `## Passos`:
    1. **Garantir store** — `mkdir -p .claude/local/` se ausente; probe `git check-ignore -q .claude/local/.probe`; sem cobertura, disparar gate `Gitignore` per ADR-005 (mecânica já no CLAUDE.md → "Local mode"). Plus gate "Worktree replication" via ADR-018 se aplicável.
    2. **Append com timestamp** — escrever no fim do `.claude/local/NOTES.md`: linha em branco + `## <ISO 8601 UTC timestamp>` (formato `date -u +%Y-%m-%dT%H:%M:%SZ`) + linha em branco + conteúdo do argumento + linha em branco. Criar arquivo se ausente. Conteúdo vazio → não escrever, retornar silente.
    3. **Reportar** — path do arquivo + bytes adicionados.
  - `## O que NÃO fazer`:
    - Não inferir/sintetizar conteúdo — gravar o argumento literal do operador.
    - Não tocar memory nativa CC — `/note` é canal independente; complementa, não substitui.
    - Não auto-buscar contexto em NOTES.md de outros projetos — leitura cross-project é fenômeno conversacional via Read nativo do Claude com path absoluto (operador valida candidato proposto pelo Claude se houver ambiguidade).

  Notas para o autor da skill:
  - Skill opera **independente** de `CLAUDE.md` / role contract; usável em qualquer git repo. Cutucada de descoberta (ADR-017/029) **não aplica** (skill não consome papel).
  - Instrumentação Tasks per ADR-010: 3 passos curtos — Tasks pode ser skip silente (skill marginal para o critério). Decisão final na implementação.

### Bloco 2 — catálogo em `README.md` + `docs/install.md` {reviewer: doc}

- `README.md`: nova linha na tabela "What's inside" após `/draft-idea` ou em posição editorial conveniente. Linha tipo:
  ```
  | `/note <content>` | Skill | Appends a timestamped note to `.claude/local/NOTES.md` (local-gitignored store extending ADR-005 to a non-role category). Captures cross-session and cross-project context for the dev-solo workflow. Cross-project read is conversational — Claude resolves the path from context and operator confirms; no auto-discovery, no companion read skill. Complements the native CC memory; does not replace it. |
  ```
- `docs/install.md`: linha 36 da smoke list — adicionar `/note` na enumeração de skills esperadas após instalação.

### Bloco 3 — preencher `docs/decisions/ADR-032-skill-note-contexto-compartilhado.md` {reviewer: code}

- `docs/decisions/ADR-032-skill-note-contexto-compartilhado.md` (stub criado pelo `/new-adr` no `/triage`; Origem já preenchida):
  - `## Contexto`: descrever o gap (memory CC nativa é per-project; cross-project não-coberto), o caso real (pje-issue-1920), e os critérios do operador (recuperação seletiva, cross-project referenciável, fricção < ganho). **Incluir reconciliação com ADR-004** em parágrafo curto: *"ADR-004 moveu state vivo (in-flight) para git/forge mas preservou `## Concluídos` como registro editorial append-only. NOTES.md cai na mesma categoria preservada — não é state competitivo (sem ciclo de merge artifact), é registro de contexto cognitivo cross-session. Sem fonte em git/forge equivalente (sessões CC paralelas + cross-project não derivam de PRs/branches)."*
  - `## Decisão`: liderar com B+A+F2(a)+F4(c). Bullets:
    - **Store em `.claude/local/NOTES.md` modo local-gitignored** (Q1=B). Path fixo doutrinário, non-role.
    - **Captura operador-driven via skill `/note`** (Q2=A). Curadoria sustentável.
    - **Extensão de ADR-005 para categoria nova "store doutrinário fixo non-role"** (F2=a). ADR-005 § Decisão lista 3 roles; ADR-032 adiciona categoria sem schema declarável. Segue precedente da entrada `(plugin-internal) | .worktreeinclude`.
    - **Cross-project read como fenômeno conversacional** (F4=c). Sem mecanismo na skill; Claude resolve contextualmente, operador valida.
    - **Complementa memory nativa CC.** Outputs distintos (cross-project intencional vs per-project conversational).
    - **Skill independente de CLAUDE.md / role contract.** Usável em qualquer git repo; cutucada de descoberta não aplica.
  - `## Consequências`: subseções `### Benefícios` (cross-session/cross-project resolvido; curadoria sustentável; estende doutrina existente sem inflar schema; entrada non-role discoverable em CLAUDE.md seguindo precedente) e `### Limitações` (cross-project requer referência explícita validada pelo operador — fluxo conversacional pode ser mais longo em projetos com nomes ambíguos; per-project store — não há index global; YAGNI deliberado sobre leitura/busca/sincronização; pode haver drift entre NOTES.md de projetos relacionados sem mecanismo de sincronização).
  - `## Alternativas consideradas`:
    - Q1: A (cross-project `~/.claude/notes/`), C (committed) — descartadas.
    - Q2: B (Claude cutuca), C (hook auto) — descartadas.
    - F2 alternativa: promover `notes` a role no path contract — descartada (schema cerimonial para singular doutrinário; sem alternativa de path).
    - F4 alternativas: path absoluto sempre (atrito alto), Claude infere candidatos via path discovery (frágil, não-documentado) — descartadas.

### Bloco 4 — entrada non-role na tabela "The role contract" do `CLAUDE.md` {reviewer: code}

- `CLAUDE.md`:
  - Na tabela "The role contract" (seção "## The role contract (load-bearing)"), adicionar nova linha imediatamente após `.worktreeinclude` (linha 42 atual) para agrupar entradas `(plugin-internal)`:
    ```
    | (plugin-internal) | `.claude/local/NOTES.md` | Cross-session context store written by `/note` (append-only, local-gitignored per ADR-005 extended; non-role). |
    ```
  - Nenhuma outra mudança no CLAUDE.md.

## Verificação end-to-end

O projeto não tem suite (`test_command: null`). Validação por inspeção textual:

- `ls skills/note/SKILL.md` → arquivo existe.
- `grep -nE "^name: note$" skills/note/SKILL.md` → 1 match.
- `grep -cE "^roles:" skills/note/SKILL.md` → 0 (omitido per ADR-003).
- `grep -n "/note" README.md` → ≥1 match na tabela "What's inside".
- `grep -n "/note" docs/install.md` → ≥1 match na smoke list.
- `grep -n ".claude/local/NOTES.md" CLAUDE.md` → ≥1 match na tabela "The role contract".
- `ls docs/decisions/ADR-032-skill-note-contexto-compartilhado.md` → arquivo existe e tem Contexto/Decisão/Consequências/Alternativas preenchidas (não placeholders).
- `grep -n ".claude/local/NOTES.md" skills/note/SKILL.md docs/decisions/ADR-032-*.md` → matches em ambos.

## Verificação manual

Cenários (smoke mental + pós-release em consumer real):

1. **Primeira invocação em projeto sem `.claude/local/`**: operador chama `/note "primeira nota"` → skill cria `.claude/local/` (mkdir), probe gitignore → ausente → gate `Gitignore` per ADR-005. Operador aceita → adiciona `.claude/local/` ao `.gitignore` → cria `NOTES.md` com primeira entrada timestampada.
2. **Append em store existente**: `/note "segunda nota"` → adiciona ao fim sem tocar a primeira; arquivo permanece append-only.
3. **Cross-project read conversacional**: operador na sessão CC do projeto B menciona "vê NOTES.md de pje-2.1" (sem path absoluto). Claude propõe candidato: *"Você quer dizer `/storage/3. Resources/Projects/tjpa/pje-2.1`? Confirme ou forneça o path."* Operador confirma → Claude faz Read absoluto → cita conteúdo no contexto da conversa.
4. **Ambiguidade cross-project**: operador menciona "pje" em projeto onde há múltiplos diretórios contendo "pje" no path. Claude lista candidatos via prosa, pede clarificação. Sem auto-discovery agressivo.
5. **Sem argumento**: `/note` (vazio) → skill pede conteúdo em prosa livre. Operador descreve → grava. Operador cancela ou submete vazio → recusa silenciosa, exit clean.
6. **Worktree sem replicação**: `.worktreeinclude` declara `.claude/` (per ADR-018) → worktree nova tem NOTES.md replicado; `/note` na worktree append no NOTES.md replicado (cópia, não symlink — operador consolida ao fim ou perde).
7. **Persistência do conteúdo**: `cat .claude/local/NOTES.md` após N invocações lista N entradas em ordem cronológica, separadas por header de timestamp UTC.
8. **Coexistência com memory nativa**: memory de CC em `~/.claude/projects/<encoded>/memory/` permanece intocada por `/note`; gravações são independentes.
9. **Skill independente de CLAUDE.md**: rodar `/note` em projeto **sem** `CLAUDE.md` (greenfield ou repo que ignorou config) → skill grava normalmente (não consome role contract). Cutucada de descoberta ADR-017/029 não dispara.

## Pendências de validação

- Smoke real pós-release em ≥1 consumer com `.claude/local/` já configurado e ≥1 consumer first-run (sem `.claude/local/`). Cenários 1, 2, 3 e 5 do smoke list.
- Validar que a entrada `(plugin-internal) | .claude/local/NOTES.md` na tabela "The role contract" é discoverable para autores de skills futuras sem virar role.

## Notas operacionais

- Ordem dos blocos sugerida: 1 → 3 → 4 → 2 (skill criada, ADR registra doutrina, CLAUDE.md adiciona entrada non-role, depois catálogo expõe ao usuário). Blocos são independentes; `/run-plan` pode reordenar.
- ADR-031 acabou de mergear (PR #68) — `/draft-idea` agora cutuca em projeto maduro. A skill `/note` é **direção de feature** (não direção do projeto), então `/triage` direto era o caminho certo, evitando `/draft-idea` (que abortaria com sugestão `/triage`). Esta `/triage` é dogfood da skill recém-mergeada.
- ADR-032 stub Origem reflete a decisão F2(a) — "estende ADR-005 (sucessor parcial)". Bloco 3 preenche o resto.
