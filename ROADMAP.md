# Roadmap

Sequência de melhorias para o plugin organizadas em ondas. Cada onda derivada de uma fonte distinta de sinal; itens dentro da onda ordenados por dor confirmada > independência > doutrina antes de canal.

- **Onda 1** sintetiza 4 análises conversacionais de 2026-05-25: vídeo "Voltei do Vale do Silício 2026" (Waldemar Neto); contraste com [github/spec-kit](https://github.com/github/spec-kit); gap de decomposição multi-plano (≥3 ocasiões históricas confirmadas pelo operador); relatório `/insights` (166 sessões analisadas, friction em `.claude/settings.json`).
- **Onda 2** sintetiza 4 fragilidades observadas em auto-análise durante execução da Onda 1 (2026-05-26): conflito reviewer-vs-reviewer; stale-view de reviewer; captura `§3.5` sem tracking; `/new-adr` skeleton vs filled ambíguo.

Artefato **plugin-internal** — não é role, não propagado a projetos consumidores. Guia de ordenação para próximas sessões CC; cada item resolve via skill apontada em "Próximo passo".

## Onda 1 — propostas conversacionais 2026-05-25

Critérios de ordenação: (1) dor confirmada por uso real precede impacto teórico, (2) itens independentes antes de dependentes, (3) doutrina antes do canal que a vende.

### 1. Cutucada de decomposição multi-plano em `/triage` step 2 — concluído (PR #73 → main `28bbeba`)

Maior dor confirmada das 3 análises. Hoje `/triage` decide artefato singular; feature grande vira plano único gigante OU múltiplos `/triage` manuais sem coordenação.

- Heurística de detecção: ≥3 bounded contexts tocados, ≥4 superfícies em "Superfícies além do código", ou ≥N blocos previstos (calibrar N).
- Cutucada nova em prosa: "feature parece exigir ≥2 planos coordenados — querer enumerar as facetas antes que eu redija um plano único?".
- Intensificar pergunta existente "caso menor que resolve 80%": se não, sinalizar decomposição.
- Sem novo artefato; sem chain mechanism (campos sucessor/predecessor ficam deferidos — ver abaixo).

**Depende de:** —
**Próximo passo:** `/triage cutucada de decomposição multi-plano em step 2`

### 2. `/note` como `informational` role em `/triage` step 1 e `/next` step 1 — concluído (PR #74 → main `c4348b0`)

Fecha o loop write/read do `/note`. Convergência tripla: vídeo (MCP-to-prod feedback), SK (bidirectional feedback prod→spec), uso manual já estabelecido (memória `feedback_parallel_sessions.md`).

- Adicionar `/note` (path `.claude/local/NOTES.md`) ao `roles.informational` das skills.
- Comportamento: ler se existir, considerar contexto recente em decisões; nunca bloqueia.
- Pode ser batched com item 1 (ambos tocam `/triage` em steps diferentes, sem conflito).

**Depende de:** —
**Próximo passo:** `/triage wiring /note como informational role em /triage e /next`

### 3. ADR-037 "código-como-fonte-de-verdade vs intent-as-truth" — concluído (commit `fe97ab6`)

Âncora doutrinal explícita contrastando com tese central do spec-kit ("specifications don't serve code — code serves specifications"). Preventivo: sem ADR, contribuidor futuro propondo "vamos virar spec-first" obriga reconstruir doutrina do zero.

- Escopo **plugin-internal** explícito no `## Decisão` — não prescreve comportamento de consumidor; consumidor pode adotar spec-first próprio sem afetar o plugin.
- Referenciado de `docs/philosophy.md`.
- Critério ADR-034 atendido: decisão estrutural duradoura sem ancestral + codificação de fronteira doutrinal.

**Depende de:** —
**Próximo passo:** `/new-adr doutrina código-como-fonte-de-verdade vs intent-as-truth`

### 4. README.md EN: framing "Product Engineer harness" — concluído (PR #75 → main `a5f0f3c`)

Vídeo dá o framing; SK dá o contraste de posicionamento. README hoje vende componentes (skills/agents/hooks); deveria vender problema primeiro. Absorve item de polimento do backlog ("marketplace prep #7").

- Hook curto no topo do README posicionando o plugin como harness do Product Engineer.
- Contraste curto com abordagens spec-first generativas, referenciando ADR-037.

**Depende de:** item 3 (ADR-037 para contraste crisp).
**Próximo passo:** `/triage atualizar README com framing Product Engineer harness e contraste spec-first`

### 5. Hook `block_settings_drift.py` — pendente

Friction recorrente confirmada pelo `/insights` report: `.claude/settings.json` acumula entradas de permissão session-scoped ou paths absolutos, exigindo cleanup commits repetidos. Paralelo a `block_env.py` e `block_gitignored.py` já shippados.

- **Auto-gating triplo:** (1) só toca `.claude/settings.json` ou `.claude/settings.local.json`; (2) só quando diff introduz padrões problemáticos (paths absolutos com `/home/`, `/Users/`; entradas de sessão); (3) `PreToolUse` `exit 2` quando match.
- **Diferencial vs `block_gitignored.py`:** `settings.json` é tracked (committed); `settings.local.json` é gitignored. Hook foca no risco do tracked, que `block_gitignored.py` não cobre.
- **Independente:** ordem livre vs itens 1-4; pode ser shipado em qualquer momento.

**Depende de:** —
**Próximo passo:** `/triage hook block_settings_drift para auto-bloquear paths absolutos e session perms em .claude/settings.json`

## Onda 2 — fragilidades observadas durante execução da Onda 1 (2026-05-26)

Itens derivados de auto-análise durante implementação dos itens 1-4. Critério de ordenação adicional: risco de regressão silenciosa precede outras dimensões — fragilidade onde a falha passa despercebida ao operador é prioritária.

### 6. Embed `## Decisões absorvidas` no body do plano (resolve conflito reviewer-vs-reviewer) — concluído (PR #76 → main `81707f0`), ADR-038 criado

Resolve fragilidade observada no item 1 (sessão de 2026-05-26): code-reviewer mid-execução flaggou estrutura que design-reviewer pré-commit havia aprovado (3 boundaries enumeradas + cross-ref Escopo↔Tamanho). Sem perspicácia do agente (citar ADR-035 + AskUserQuestion), o default-absorber teria revertido silenciosamente a decisão aprovada pelo operador.

ADR-035 prescreve "override por inação" mas só funciona se o agente reconhecer o conflito. Mecânica atual: findings absorvidos vivem no commit message do plano (ADR-026 § Forma); code-reviewer não lê commit messages, só o diff — gap de informação estrutural alto-impacto.

- **Mecanismo (opção B confirmada pelo operador):** Refinar ADR-026 — `## design-reviewer findings absorvidos` ganha contrapartida estruturada no body do plano (nova seção opcional `## Decisões absorvidas` no `templates/plan.md`). `/run-plan` passa essa seção como contexto na invocação de cada reviewer por bloco (paralelo ao mecanismo de `**Termos ubíquos tocados:**` da ADR-021). `code-reviewer` agent def ganha 1 cláusula: "se invocador passa Decisões absorvidas, trate as estruturas listadas como out-of-scope da rubrica YAGNI per ADR-035 override-by-inaction explícito".
- **Critério ADR-034:** todas as 4 condições aplicam (decisão central de ADR-026 intacta, sem nova categoria, sem restrição externa, caráter operacional) → **adendo a ADR-026**, não novo ADR. Edits em templates/plan.md + /run-plan §2.3 + code-reviewer agent def acompanham.
- **Cobertura:** decisões EXPLICITAMENTE absorvidas pelo design-reviewer. Não cobre decisões implícitas de conversa (operador respondeu X em AskUserQuestion sem registro no plano) — essas continuam dependendo do agente.

**Depende de:** —
**Próximo passo:** `/triage embedar Decisões absorvidas no body do plano para code-reviewer consumir`

### 7. Stale-view de reviewer — `Read` explícito antes de análise — concluído (PR #77 → main `27473af`)

Resolve fragilidade observada no item 4 §3.4 (sessão de 2026-05-26): `code-reviewer` rodou contra estado pré-Edit (git diff mostrava só Bloco anterior); produziu finding moot ("entrada usa texto antigo") quando o Edit já tinha aplicado a linha nova. Eu dismissei como stale e segui.

Risco: se fosse finding legítimo mascarado por timing, eu teria absorvido um falso "tudo OK". Cada invocação assume snapshot consistente — sequência Edit → invoke Agent pode disparar antes do harness sincronizar git stage.

- **Mecanismo:** ajuste editorial nos prompts de invocação dos reviewers em `/run-plan §2.3`, `/triage step 5` e `/new-adr step 5`. Adicionar instrução: "antes de analisar, leia o arquivo alvo via `Read` (não confie em `git diff` — pode estar stale entre Edit recente e invocação)". Custo: 1 frase por skill (3 locais).
- **Cobertura:** ~100% dos casos de stale-view por timing Edit→Agent. Não cobre stale conceitual (reviewer interpretou contexto errado) — esse é outro problema.

**Depende de:** —
**Próximo passo:** `/triage Read explícito antes de análise nos prompts de invocação de reviewer`

### 8. Captura automática `/run-plan §3.5` via TaskCreate (em vez de lista mental) — concluído (PR #78 → main `7b68bd0`), ADR-039 criado

Resolve fragilidade latente — não observada nesta sessão (todas as execuções fizeram skip silente em §3.5), mas estruturalmente presente. Spec atual diz "agente acumula gatilhos e materializa no gate final" sem mecanismo de tracking — depende de lista mental do agente. Em `/run-plan` longo (≥3 blocos com triggers reais), risco de esquecer parte da lista entre passo 2 e §3.5.

- **Mecanismo:** `/run-plan §3.5` ganha — cada captura emergente dispara `TaskCreate` com prefixo marker (ex.: `[capture:backlog] <linha>`, `[capture:validacao] <linha>`); §3.5 lê `TaskList` filtrada por marker para materialização. Paralelo a ADR-010 (que já usa Task para sub-passos do gate).
- **Cobertura:** elimina dependência de memória do agente; lista vira state persistido (conversation-scoped) até materialização ou cleanup explícito.
- **Preventivo:** fragilidade latente sem incidente observado ainda — incluída por classe ("agente mantém estado mentalmente em fluxo multi-passo") que tem precedente em ADR-010.

**Depende de:** —
**Próximo passo:** `/triage captura automática §3.5 via TaskCreate com marker`

### 9. `/new-adr` clarifica spec "Não inventar" vs "preencher com inputs do operador" — concluído (PR #79 → main `6a93d63`)

Resolve zona cinza observada no item 3 (criação de ADR-037): `## O que NÃO fazer` diz "Não inventar conteúdo de Contexto/Decisão — quem decide é o operador". Mas operador tinha decidido substância via ROADMAP item 3 (preventivo, plugin-internal, code-as-truth). Eu julguei e preenchi; design-reviewer auditou. Funcionou nesta invocação mas regra tem zona ambígua que depende de julgamento do agente.

- **Mecanismo:** 1 frase adicional no spec da `/new-adr`: "Preencher com conteúdo derivado de inputs explícitos do operador (ROADMAP, plano upstream, conversa recente). Placeholders apenas quando nenhum input substantivo existir."
- **Cobertura:** clarifica intenção sem novo mecanismo. `design-reviewer` continua auditor de drift entre input do operador e conteúdo gerado.
- **Smallest impact** da Onda 2 — editorial puro; sem mecanismo novo, sem ADR.

**Depende de:** —
**Próximo passo:** `/triage clarificar spec /new-adr sobre preencher vs skeleton`

## Deferido — reabrir com gatilho concreto

| Item | Gatilho de reabertura |
|---|---|
| Campos `**Sucessor:**` / `**Predecessor:**` opcionais em `## Contexto` do plano + coordenação inter-plano em `/run-plan` | Item 1 implementado + ≥2 features multi-plano onde dor persiste (operador relata "lembrei tarde demais que tinha planos coordenados") |
| Rubrica "bloco agent-sized" em `design-reviewer` | Item 1 implementado + ≥1 plano grande passa a cutucada de `/triage` e chega ao design-reviewer maior do que deveria ser |
| Seção opcional `## Premissas e incertezas` no plan template (inspirada em `[NEEDS CLARIFICATION]` do spec-kit) | Autor de plano reporta perda de assumptions implícitas em ≥2 invocações |
| Tracking de Task IDs cross-update via subject matcher (em vez de ID numérico) | ≥3 sessões com off-by-one em TaskUpdate observado — overhead recoverable hoje, considerar se virar pain real |

## Rejeitado — não reabrir sem mudança doutrinal

| Item | Motivo |
|---|---|
| Fan-out paralelo de blocos em `/run-plan` (`parallel: true` ou dependency graph) | Workflow solo + complexidade alta + planos sequenciais editoriais; YAGNI per ADR-035 |
| Constitution unificando `IDEA.md` + `philosophy.md` + ADRs (estilo spec-kit) | Split intencional em PT; categorias com ciclo de vida distinto preservadas |
| Skill `/analyze` cross-artifact consistency (estilo spec-kit) | Já coberto por `design-reviewer` (seção "Contradição com ADRs existentes") + `/triage` step 1 (intent alignment com `product_direction`/domain/design) |
| Skill `/incident` ou cross-source diagnosis (Canvas do vídeo) | Escopo prod-ops, fora do plugin de dev local |
| Pattern MCP-to-prod data (Cursor do vídeo) | Project-specific, não cabe em plugin stack-agnóstico |
| Skill `/retro` ou síntese periódica | YAGNI workflow solo; raw-chat cobre |
| Categoria nova `docs/epics/<slug>.md` com role próprio | Cerimônia alta antitética ao flat & pragmatic |
| Documentação de pattern manual multi-plano (sem mecanismo) | Frágil — humano esquece; preferido item 1 com mecanismo |
| `code-reviewer` ganha free-read de ADRs (estilo `design-reviewer`) | Antitético a ADR-035 que preservou "YAGNI universal sem context-aware switch"; alternativa C ao item 6 |
