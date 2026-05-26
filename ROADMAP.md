# Roadmap

Sequência de melhorias propostas durante 4 análises conversacionais (2026-05-25):

1. Vídeo "Voltei do Vale do Silício: Esse é o Dev que QUEREM em 2026" — Waldemar Neto.
2. Contraste com [github/spec-kit](https://github.com/github/spec-kit).
3. Gap de decomposição multi-plano (≥3 ocasiões históricas confirmadas pelo operador).
4. Relatório `/insights` (166 sessões analisadas): friction recorrente em `.claude/settings.json`.

Artefato **plugin-internal** — não é role, não propagado a projetos consumidores. Guia de ordenação para próximas sessões CC; cada item resolve via skill apontada em "Próximo passo".

## Ordem proposta

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

### 4. README.md EN: framing "Product Engineer harness" — pendente

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

## Deferido — reabrir com gatilho concreto

| Item | Gatilho de reabertura |
|---|---|
| Campos `**Sucessor:**` / `**Predecessor:**` opcionais em `## Contexto` do plano + coordenação inter-plano em `/run-plan` | Item 1 implementado + ≥2 features multi-plano onde dor persiste (operador relata "lembrei tarde demais que tinha planos coordenados") |
| Rubrica "bloco agent-sized" em `design-reviewer` | Item 1 implementado + ≥1 plano grande passa a cutucada de `/triage` e chega ao design-reviewer maior do que deveria ser |
| Seção opcional `## Premissas e incertezas` no plan template (inspirada em `[NEEDS CLARIFICATION]` do spec-kit) | Autor de plano reporta perda de assumptions implícitas em ≥2 invocações |

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
