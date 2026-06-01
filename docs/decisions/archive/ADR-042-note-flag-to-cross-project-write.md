> **ARCHIVED 2026-06-01** — content absorbed into [ADR-054](../ADR-054-bridge-cross-project-note-consolidado.md); see that ADR for current authority. Body below preserved verbatim for historical record.

# ADR-042: Flag `--to` em /note para cross-project write com discovery via `$PROJECTS_DIR`

**Data:** 2026-05-28
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-032](ADR-032-skill-note-contexto-compartilhado.md) — definiu `/note` como skill intra-projeto, com cross-project explicitamente coberto **só no eixo read** ("fenômeno conversacional via Read nativo + path absoluto"). Write cross-project ficou implicitamente fora — step 1 ancora em `git rev-parse` do repo corrente. Este ADR é **sucessor parcial** estendendo § Decisão e § Limitações de ADR-032 para cobrir cross-project write via flag opcional, sem alterar comportamento default intra-projeto.
- **Investigação:** sessão CC 2026-05-28 — operador pediu desenho de mecanismo para "enviar informação/contexto para outros projetos quando necessário". Varredura empírica de `$PROJECTS_DIR/*/.claude/local/NOTES.md` (6 NOTES.md ativos) confirmou pain real recorrente: `dotfiles` ↔ `loadout` com ≥6 entradas explicitando trabalho coordenado cross-repo e cross-refs `file://` a ADRs do outro lado; `drive-sync` registrando "findings vindos de sessão Claude Code no repo irmão chezmoi"; `meta-system` como doctrine container cross-repo; o próprio `pragmatic-dev-toolkit/.claude/local/NOTES.md` linha 4 marcada literalmente como *"Sessão CC: meta-system (cross-repo registration)"* — operador escrevendo manualmente a partir de outra sessão. ADR-035 critério 1 (incidente recorrente documentado) e critério 4 (pattern ad hoc emergente ≥3x) ambos disparados.

## Contexto

Operador opera regularmente ≥3 sessões CC em projetos distintos com trabalho coordenado entre eles (ex.: decisão sobre `bw` no `dotfiles` que exige ação correspondente no `loadout`; finding em `drive-sync` que origina em revisão feita no `chezmoi`). O canal de handoff cross-session intra-projeto (`.claude/local/NOTES.md` via `/note`) funciona, mas a comunicação cross-project é feita manualmente — operador switch de sessão para o target ou faz `Write` direto no path absoluto do outro repo.

ADR-032 § Limitações lista `Per-project store sem index global` com gatilho de reabertura: *"reabertura legítima se atrito real surgir"*. O atrito surgiu — não como demanda de index global, mas como demanda de **send-side ergonômico** (operador na sessão A precisa registrar nota no projeto B sem trocar de sessão).

Evidência adjacente do uso real: operador merge cross-source no mesmo `NOTES.md` do target (não segrega por origem em arquivos diferentes), apenas prosa-prefaceia "*vindo de sessão X*". Implica que **o store-target é o `NOTES.md` existente do projeto receptor**, não um inbox separado. Mantém compatibilidade total com o read-side (operador e Claude lêem NOTES.md do outro projeto via Read nativo do mesmo jeito).

A env var `$PROJECTS_DIR` (`/home/fppfurtado/Projects` neste setup) é contrato declarado pelo operador apontando a raiz canonical de projetos. Discovery por nome (`$PROJECTS_DIR/<nome>/.claude/local/NOTES.md`) é determinística e barata — não é a heurística filesystem-wide rejeitada por ADR-032 § F4 alternativa b (que descartava `find /storage/.../`); é resolução via contrato explícito do ambiente.

**Critério mecânico que separa contrato de heurística** (load-bearing para preservar a doutrina ampla de ADR-032 § F4 alt b sem inflar): *contrato declarado* = sinal explícito do operador para o ambiente (env var, config file declarativo no escopo do operador, registry); *heurística* = inferência sobre o filesystem sem sinal declarado (glob ad hoc, `find /storage/...`, `~/Projects/*/` hardcoded). `$PROJECTS_DIR` ausente → recusa explícita com mensagem (operador percebe o gap); ADR-032 § F4 alt b inferiria silenciosamente. Esse critério também estende `~/.claude/projects-registry.yml` ou similar para a categoria *contrato* caso o gatilho de revisão 3 dispare.

## Decisão

**Estender `/note` com flag opcional `--to <projeto-ou-path>` para write cross-project**, preservando o comportamento default intra-projeto e a doutrina de privacy-by-design / non-role / local-gitignored.

Razões objetivas:

- **`--to` opcional, sem mudança default**. Invocação sem `--to` permanece idêntica à v1: append em `<repo-corrente>/.claude/local/NOTES.md`. Cross-project write é opt-in explícito. Preserva ergonomia do uso intra-projeto majoritário.
- **Discovery em 2 níveis**:
  1. `--to <nome>` (não contém `/`) → resolve via `$PROJECTS_DIR/<nome>/.claude/local/NOTES.md`. `$PROJECTS_DIR` ausente → recusa com mensagem orientando definir env var ou usar path absoluto. Target inexistente → recusa com mensagem listando projetos detectados em `$PROJECTS_DIR`.
  2. `--to <path-absoluto>` (começa com `/`) → bypass discovery, escrita direta no path. Caminho para casos fora de `$PROJECTS_DIR`.
- **Pré-condição de target inicializado.** Cross-write requer que o target já tenha `.claude/local/` existente E `git -C <target> check-ignore -q .claude/local/.probe` cobrindo. Faltando qualquer um → recusa com mensagem: *"target não inicializado para modo local; abra sessão CC em `<target>` e rode `/note` uma vez para inicializar gates"*. Move first-time setup para sessão do target onde o operador tem contexto para aprovar mudanças em `.gitignore`/`.worktreeinclude` do repo dele.
- **Gate `Gitignore` opera como read-only probe no target; gate `Worktree replication` não roda em cross-write, em modo algum** (nem probe, nem mutação). Replicação para worktrees do target é responsabilidade exclusiva da sessão local do target via `/note` ou `/run-plan` quando o operador trabalhar lá. Mutações em `.gitignore`/`.worktreeinclude` de outro repo a partir de sessão não-contextual ferem o critério de blast-radius compartilhado (paralelo doutrinal com `/run-plan §1.1`). Pré-condição de target (acima) checa `.claude/local/` existente E `git check-ignore` cobrindo — **não** estende para `.worktreeinclude` do target (assimetria deliberada: gitignore é invariante de privacidade da gravação corrente, worktree-replication é invariante de execução futura no target).
- **Mesmo formato de append**. Conteúdo gravado segue o formato canonical de ADR-032: timestamp UTC + corpo literal. Receptor não distingue origem mecanicamente — operador prefaceia em prosa quando relevante (pattern observado em uso real).
- **Reporta path do target no output**. Mensagem de retorno cita o path absoluto do arquivo escrito + bytes adicionados, para auditabilidade e desambiguação visual.
- **Extensão de ADR-032 sem violar non-role e sem inflar schema**. `.claude/local/NOTES.md` continua sendo store doutrinário fixo non-role; flag `--to` é parâmetro de target da mesma operação, não papel novo no path contract. Sem schema declarável; sem entrada nova na tabela "The role contract".
- **Coerência com read-side**. ADR-032 já legitima cross-project read via Read nativo. Adicionar write-side simétrico fecha o loop sem introduzir nova categoria conceitual: cross-project é apenas operação de target ≠ corrente, não mecanismo paralelo.

## Consequências

### Benefícios

- Caminho mecânico para o pattern empírico recorrente cross-repo coordination (dotfiles↔loadout, drive-sync←chezmoi, meta-system↔consumers). Operador na sessão A registra para B sem context-switch.
- Discovery por nome via `$PROJECTS_DIR` é ergonômica (`/note --to loadout "fix x"` vs typar path absoluto), barata e não-heurística — contrato explícito do ambiente.
- Pré-condição de target inicializado preserva ADR-005 § Gate `Gitignore` (operador aprova mudança no contexto do repo) sem replicar mecânica cross-contextual.
- Compatibilidade total com read-side (Read nativo em NOTES.md de outros projetos) — sem mudança em fluxo de consumo cross-project existente.
- Zero impacto em consumers sem `$PROJECTS_DIR` ou que não usam `--to`: comportamento default preservado.

### Limitações

- **Discovery acoplada a `$PROJECTS_DIR`**. Sem env var, só path absoluto funciona. Aceitável — operadores sem `$PROJECTS_DIR` usam o fallback explícito; documentação aponta o contrato.
- **First-time cross-write em target não inicializado falha hard**. Operador precisa abrir sessão CC no target uma vez para inicializar. Aceitável — torna explícita a fronteira de blast-radius e evita gates cross-contextuais.
- **Sem registro de origem mecânico**. NOTES.md do target não marca "veio de --to a partir de <sessão>"; convenção de prosa-prefácio fica com o operador. Coerente com o padrão observado em uso real; reabertura legítima se attrito surgir (campo opcional `[from: <src>]` no header do timestamp).
- **Sem broadcast (`--to a,b,c`)**. Cross-write é 1-to-1 por invocação. Multi-target ad hoc reabre em uso real se ≥3 casos surgirem; YAGNI hoje.

## Alternativas consideradas

### A — Documentação only do caminho atual (switch session ou Write nativo)

Descartada. Foi a hipótese inicial sob ADR-035 conservador, mas varredura empírica de 6 NOTES.md confirmou pattern ad hoc recorrente que justifica codificação (ADR-035 critérios 1 e 4 disparados). Manter como doc apenas perderia ergonomia já demandada pelo uso real.

### B — `/note --to <projeto-ou-path>` (escolha tomada — baseline)

Mantida. Flag opcional em skill existente, com discovery por nome via `$PROJECTS_DIR` e fallback a path absoluto; pré-condição de target inicializado preserva blast-radius doctrine. Substância completa em § Decisão acima — documentada aqui como alternativa-baseline contra a qual C–H se rebatem (simetria para o leitor avaliar os trade-offs).

### C — Skill nova `/send-note <target> "<msg>"` (verbo separado)

Descartada. Mesma mecânica de B (mkdir, gates, append timestampado) trocando apenas o target — duplicaria mecânica por modo de uso. Pattern observado é `/note` com 1 ponto de variação (target = corrente vs `--to`), mais coeso como flag opcional que como skill nova. Paralelo conceitual com [ADR-008](ADR-008-skills-geradoras-stack-agnosticas.md): skills detectam stack do consumer por marker em vez de skills separadas por stack — variação de runtime via parâmetro, não por verbo. Pattern secundário: `/triage` decide saída (linha vs plano vs ADR) sem skills separadas por tipo. Justificaria-se se cross-write ganhasse peso semântico próprio (tipagem do conteúdo, ack, broadcast) — todos YAGNI hoje.

### D — Inbox pattern (`.claude/local/INBOX.md` segregado)

Descartada com base em evidência empírica direta. Varredura de NOTES.md cross-source mostrou operador merge tudo no mesmo arquivo, prefaceiando em prosa a origem — não segrega por arquivo. Inbox separado introduziria store novo, leitor novo (`/triage`/`/next` precisariam ler ambos distinguindo origem), e gate novo, sem ganho que o uso real demande.

### E — Hub central em `~/.claude/cross-project-notes/`

Descartada. Viola restrição doutrinal de ADR-032 alternativa Q1=A ("operador exigiu como restrição" não introduzir convenção fora do repo). Cria infra paralela à memory nativa CC. Receptor perderia descoberta natural (já hoje o NOTES.md local é o store conhecido).

### F — Discovery via path discovery agressiva (`find /storage/`, glob de `~/Projects/`)

Descartada por ADR-032 § F4 alternativa b. Heurística filesystem-wide é frágil e específica de ambiente. `$PROJECTS_DIR` (decisão tomada) é contrato declarado, não heurística — distinção load-bearing.

### G — Gates `Gitignore`/`Worktree replication` rodando no target mesmo cross-write

Descartada. Operador aprovando mudança em `.gitignore` de outro repo sem contexto da sessão dele fere blast-radius compartilhado (paralelo doutrinal com `/run-plan §1.1`). Pré-condição de target inicializado (caminho escolhido) move setup para onde o contexto existe.

### H — `--to` aceita só path absoluto, sem discovery por nome

Descartada. Caminho mais simples doutrinalmente (zero env var, zero fallback, zero risco de borderline com ADR-032 § F4 alt b), mas paga em fricção repetitiva: operador typar `/note --to /home/fppfurtado/Projects/loadout 'fix x'` toda invocação cross-write em ambiente onde 5+ projetos vivem sob mesma raiz. `$PROJECTS_DIR` como contrato explícito do ambiente é ergonomia barata sem heurística (critério mecânico em § Contexto separa contrato declarado de inferência silenciosa). Path absoluto **não** é descartado — é trilho 2 do discovery (caminho complementar para targets fora de `$PROJECTS_DIR` ou para ambientes sem env var declarada).

## Gatilhos de revisão

- **Broadcast multi-target** demandado em ≥3 cenários reais (`--to a,b,c`) → reabrir alternativa.
- **Registro de origem mecânico** demandado para auditabilidade (operador frequentemente perdendo trilha de "de onde veio essa nota") → campo opcional no header do timestamp.
- **Target em path fora de `$PROJECTS_DIR` virar majoritário** (operador adiciona N projetos em locations diversas) → considerar discovery via registry declarado em `~/.claude/projects-registry.yml` ou similar.
- **First-time cross-write recusado em ≥3 sessões distintas dentro de 1 mês** → considerar relaxar pré-condição com modo `--init-target` explícito (skill cria `.claude/local/` no target + gate `Gitignore` cross-contextual com aprovação explícita do operador para o target). Threshold mecânico evita reabertura prematura por casos esporádicos.
