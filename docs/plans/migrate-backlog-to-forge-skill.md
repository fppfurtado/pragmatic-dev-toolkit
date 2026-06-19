# Plano — `/migrate-backlog-to-forge` v0

## Status

Pendente

## Contexto

Materializa o helper canonical anchored em [#125](https://github.com/fppfurtado/pragmatic-dev-toolkit/issues/125). N=3 da fricção do gap foi materializada em 2026-06-19:

1. **meta-system** (sessão `backlog-forge-migration`) — 19 entries → gh issues #18–#36
2. **logseq-notes** (sessão setup operacional) — 1 entry → gh issue #1
3. **pragmatic-dev-toolkit** (esta sessão, commit `28c92a9`) — 7 entries → gh issues #127–#133

Cobertura forge atual: **gh N=3, glab N=0 estrutural** — repos TJPA não têm BACKLOG.md (canonical já era issues GitLab; operador confirmou ausência de demanda glab natural). Implementação speculative cross-forge violaria YAGNI doutrinal; helper para com mensagem clara quando forge-auto-detect resolve glab até empírica emergir.

Script ad-hoc preservado em `/tmp/migrate-backlog-to-forge.py` (~50 linhas) é a base concreta: parse `## Próximos`, batched `gh issue create` com título + body integral + footer migração, captura issue numbers. As 3 invocações desta sessão validaram o algoritmo end-to-end.

**ADRs candidatos:** [ADR-066](../decisions/ADR-066-migracao-inicial-cutucada-batched-modo-forge.md) (3ª categoria editorial de cutucada por mutação — modelo canonical da migração; sucessor parcial de ADR-058 § (e); criado neste /triage), [ADR-058](../decisions/ADR-058-role-backlog-aceitar-forge.md) (modo forge do role backlog — operação canonical sob este modo), [ADR-017](../decisions/ADR-017-decomposicao-skill-orquestrador-sub-tool.md) (orquestrador heurístico + sub-tool determinístico — *cross-project precedent em meta-bridge*, não ADR vigente neste repo; padrão formalizado neste repo via adendo CLAUDE.md no Bloco 1), [ADR-011](../decisions/ADR-011-skill-vs-funcao-utilitaria.md) (skill ≠ função utilitária — informa por que skill markdown + sub-tool em vez de script-só), [ADR-050](../decisions/ADR-050-componentes-plugin-consolidado.md) (componentes plugin — informa naming + `disable-model-invocation` per § (e)).

**Linha do backlog:** `#125: \`/init-config\` migration helper pra forge switch — gap descoberto in vivo`

## Resumo da mudança

Cria skill `/migrate-backlog-to-forge` como **orquestrador hybrid + sub-tool Python determinístico** per [ADR-017](../decisions/ADR-017-decomposicao-skill-orquestrador-sub-tool.md) § decomposição (precedent em meta-bridge; pattern formalizado neste repo via adendo CLAUDE.md no Bloco 1). Skill prosa decide cutucadas + AskUserQuestion (heurístico-semantico, agentic); sub-tool faz parse + `gh issue create` + drain marker + config flip + commit (mecânico, determinístico). Pattern paralelo a `/wiki-compile` em meta-bridge.

**Decisões pré-tomadas (deste /triage):**

- **Forma**: hybrid SKILL.md + sub-tool Python (ADR-017 + precedent meta-bridge; pattern formalizado via adendo CLAUDE.md no Bloco 1 deste plano).
- **Geração de títulos**: LLM propõe N títulos batched a partir das entries; operador aprova/edita via enum unificado (pattern empírico replicado das 3 migrações de hoje). Alternativa "trim determinístico ≤80 chars" rebatida: produz títulos cosméticos em entries multi-frase (e.g. `#125` daria `"\`/init-config\` migration helper pra forge switch — gap descob"`); LLM batched preserva substância semântica com custo proporcional (N tokens em vez de N×K).
- **Escopo**: end-to-end. Helper parsea entries + cria N issues + drena BACKLOG `## Próximos` + flipa `paths.backlog: forge` em `CLAUDE.md` + commit unificado + push + comment automático em #125 se aberta.
- **Modelo de cutucada**: **batched-com-confirmação** — 1 cutucada unificada `AskUserQuestion` antes da 1ª mutação remota autoriza TODAS as N mutações + side-effects (drain + config + commit + push). Codificado em [ADR-066](../decisions/ADR-066-migracao-inicial-cutucada-batched-modo-forge.md) como 3ª categoria editorial paralela ao default per-mutação de ADR-058 § (e) e ao sub-caso batched-com-seleção de `/run-plan §3.5`. Sucessor parcial editorial de ADR-058 § (e), reconhece divergência empírica disciplinadamente.
- **Integração `/init-config`**: standalone v0. Sem auto-trigger; operador invoca manualmente após `/init-config`. 3/3 migrações de hoje foram standalone ad-hoc — empírica forte pra desacoplamento.
- **Boundary glab**: pre-flight `forge-auto-detect`; output `glab` → para com mensagem clara orientando operador (e.g., "glab support deferred until empirical anchor — para migrar manualmente, replicar script `/tmp/migrate-backlog-to-forge.py` adaptando `gh issue create` → `glab issue create`"). Sem implementação speculative.
- **Naming**: `/migrate-backlog-to-forge` per CLAUDE.md `<verb>-<artifact>` convention (output fixo: forge issues).
- **Sub-tool path**: `skills/migrate-backlog-to-forge/sub-tools/migrate.py` — 1ª instância do pattern `skills/*/sub-tools/<f>.py` neste repo; **adendo em CLAUDE.md § Plugin component naming (Bloco 1)** formaliza tabela + bullet em § Editing conventions com cross-ref a precedent meta-bridge.
- **`disable-model-invocation: true`** per critério cumulativo ADR-050 § (e): blast radius local + push gated por enum upstream + sem autoinvocação cross-turn.

## Arquivos a alterar

### Bloco 1 — Adendo CLAUDE.md § Plugin component naming + § Editing conventions {reviewer: doc}

- `CLAUDE.md`: 2 edits cirúrgicos
  - **(i) § Plugin component naming**: tabela ganha 4ª linha "**Sub-tool (em skill)**: `skills/<name>/sub-tools/<f>.py` — Python standalone CLI invocado pela skill prosa via `Bash`; JSON-over-stdout + exit codes; sem stack-specific variant em v0".
  - **(ii) § Editing conventions**: bullet curto cross-ref a precedent meta-bridge `/wiki-compile` + ADR-017 do meta-bridge (cross-project precedent reconhecido; **não doutrina vigente neste repo** — formalização canonical fica no adendo (i) acima).
- Formaliza 1ª instância pattern; sem ADR (paralelo ao bullet `disable-model-invocation` editorial pattern — adendos CLAUDE.md sem ADR cobrem padrões empíricos mecânicos per § Editing conventions).

### Bloco 2 — SKILL.md (orquestrador) {reviewer: prompt}

- `skills/migrate-backlog-to-forge/SKILL.md`: NEW. Frontmatter (`name: migrate-backlog-to-forge`, `description: ...`, `roles.required: [backlog]`, `disable-model-invocation: true`). Body com 7 passos:
  1. **Pre-flight forge-auto-detect**: output ≠ `gh` (no-detection / unsupported-host / glab) → para com mensagem específica (cada caso) orientando operador.
  2. **Pre-condição role estado**: probar bloco `<!-- pragmatic-toolkit:config -->` em `CLAUDE.md`. Se `paths.backlog: forge` já declarado → para com "modo já flippado — migração não aplicável"; se ausente OR file mode → segue. Se `paths.backlog: null` → para com "papel desativado — sem o que migrar".
  3. **Probar BACKLOG.md**: ausente → para com mensagem ("sem BACKLOG.md, sem entries a migrar"); presente → segue.
  4. **Parse `## Próximos` via sub-tool**: sub-tool retorna JSON com {entries: [text]}. Zero entries → para com mensagem ("`## Próximos` vazio — config flip suficiente, sem entries pra migrar"; remete operador a editar `CLAUDE.md` manual). N entries → mostra contagem + entries em prosa.
  5. **Gerar títulos batched**: LLM propõe N títulos curtos (≤80 chars) a partir das entries. Sintetiza cada de primeira sentence + objeto-substância. Mostra títulos propostos em prosa (1 linha por entry: `#1: <title> — <entry preview 80 chars>`).
  6. **Cutucada AskUserQuestion unificada** (header `Migração`, antes da 1ª mutação remota per [ADR-066](../decisions/ADR-066-migracao-inicial-cutucada-batched-modo-forge.md) § Mecânica — batched-com-confirmação como 3ª categoria editorial): `Aplicar batch completo (Recommended)` / `Revisar antes (loop per-item)` / `Cancelar`. Cobre título + mutação juntos. `Aplicar batch completo` autoriza TODAS as N mutações + side-effects (drain + config + commit + push) em 1 fluxo. `Revisar antes` cai em loop granular per-item ainda gateado por confirmação final batched (combinação 1ª + 3ª categorias). `Cancelar` aborta sem mutações remotas.
  7. **Execução via sub-tool**: cria N issues + dreno + config flip; captura number list. Commit unificado `feat(config): migrar backlog para paths.backlog: forge` (template fixo + N entries listadas no body). Push imediato. Comment em #125 se aberta (gh issue list --state open detecta).
- `## O que NÃO fazer`: bullets sobre (a) não rodar sem `## Próximos` populado; (b) não pular cutucada batched (blast radius — ADR-066 § Mecânica explícita); (c) não tentar glab inline; (d) não mutar `## Concluídos` (registro histórico append-only).

### Bloco 3 — sub-tool Python `migrate.py` {reviewer: code}

- `skills/migrate-backlog-to-forge/sub-tools/migrate.py`: NEW. CLI standalone (executado via `python3 ${CLAUDE_PLUGIN_ROOT}/skills/migrate-backlog-to-forge/sub-tools/migrate.py`):
  - **Subcomando `parse`**: input `--backlog <path>`. Parsea `## Próximos`, output JSON em stdout: `{"entries": [{"text": "..."}, ...]}`. Stripa prefix `- plugin: ` para limpar.
  - **Subcomando `migrate`**: input `--backlog <path>` `--titles <titles.json>` (lista de strings, ordem = ordem entries). Executa em ordem:
    1. Pre-flight: re-verifica forge-auto-detect == `gh` (defesa em profundidade contra race entre skill check e sub-tool exec)
    2. Idempotência: se ## Próximos já drenado (marker presente) → exit 2 com mensagem
    3. Para cada (title, entry): `gh issue create --title <title> --body <entry + footer>` capturando number
    4. Drena ## Próximos com marker + header note (template fixo)
    5. Flipa `paths.backlog: forge` em CLAUDE.md (edit cirúrgico no bloco `<!-- pragmatic-toolkit:config -->`)
    6. Imprime JSON em stdout: `{"issues": [{"number": N, "title": T}, ...]}` para skill montar commit body
  - **Auto-gate**: file_path resolução usa `os.path.realpath` (lição de #126 — consumer pode ter layout symlink-mediated).
  - **Boundary glab**: se `forge-auto-detect` resolver glab no pre-flight do subcomando `migrate`, exit 2 com mensagem específica.
  - Sem dependências externas além de stdlib + `gh` CLI no PATH (gate: comando `gh --version` verificado, falha → exit 2 com mensagem).
- Comment 1-line no topo explica pattern parse→batch→drain + cross-ref ADR-017 (meta-bridge precedent) + adendo CLAUDE.md (Bloco 1 deste plano).

### Bloco 4 — README.md + docs/install.md cross-refs {reviewer: doc}

- `README.md`: entry pra `/migrate-backlog-to-forge` em § What's inside paralela aos siblings (`/init-config:NN`, `/note:NN`, etc.). 1-2 linhas descritivas.
- `docs/install.md`: nota curta sobre quando usar — após `/init-config` flippa role.backlog file→forge **com BACKLOG.md pré-existente** populado em `## Próximos`. Mencionar boundary gh-only explícito.

## Verificação end-to-end

- `test -f skills/migrate-backlog-to-forge/SKILL.md`
- `test -f skills/migrate-backlog-to-forge/sub-tools/migrate.py`
- `python3 skills/migrate-backlog-to-forge/sub-tools/migrate.py --help` exit 0 (CLI parseia args)
- `grep -nE 'Sub-tool \(em skill\)' CLAUDE.md` retorna 1 match (adendo § Plugin component naming)
- `grep -nE '^- \[`/migrate-backlog-to-forge`' README.md` retorna 1 match (entry shippada)
- `grep -nE 'migrate-backlog-to-forge' docs/install.md` retorna ≥1 match
- `test -f docs/decisions/ADR-066-migracao-inicial-cutucada-batched-modo-forge.md` (já criado neste /triage)

## Verificação manual

Smoke determinístico em paths offline (sem mutação remota):

- **C1 parse**: criar `/tmp/fake-backlog.md` com 3 entries em `## Próximos`. Rodar `python3 skills/migrate-backlog-to-forge/sub-tools/migrate.py parse --backlog /tmp/fake-backlog.md`. Esperado: JSON em stdout com `entries: [...]` len 3, prefix `- plugin: ` strippado.
- **C2 parse vazio**: `## Próximos` vazio → JSON `entries: []`, exit 0.
- **C3 parse drenado**: `## Próximos` com marker drain pre-existente → exit 2 com mensagem ("já drenado").
- **C4 boundary glab simulado**: rodar sub-tool em repo com `origin` URL containing `gitlab.com` (qualquer repo TJPA via cd temporário) → exit 2 com mensagem específica.
- **C5 gate gh ausente simulado**: rodar sub-tool com `PATH=` vazio (`gh` indisponível) → exit 2 com mensagem.

Sem mutação remota nestes — verificação fica em parse + boundary + gates, lições de defesa em profundidade preservadas.

## Pendências de validação

- `[capture:validacao]` Smoke real cross-repo pós-shipping: próximo consumer que migrar de file→forge invoca `/migrate-backlog-to-forge`, observa N issues criadas + drain + config + commit + comment em #125. Captura experiência (UX da cutucada batched-com-confirmação, tempo de execução, fricção residual, comportamento da geração de títulos LLM em entries arbitrárias). Operador escolhe consumer real ou inventa fixture (repo descartável + BACKLOG.md sintético).
- `[capture:validacao]` Smoke da opção `Revisar antes (loop per-item)`: ADR-066 § Override calibração específica reconhece que esta opção é forward-looking sem cobertura empírica em 2026-06-19; próxima invocação que escolher esta opção materializa teste empírico forward. Captura fricção UX residual (Gatilho de revisão #1 do ADR-066 codifica reabertura).
- `[capture:validacao]` Smoke comportamental do auto-trigger desabilitado: rodar `/triage` em sessão CC nova num repo com substância tangencial ao escopo do helper (e.g., entry sobre "criar BACKLOG.md") e verificar que `/migrate-backlog-to-forge` NÃO é proposto como sugestão (`disable-model-invocation: true` honrado).

## Notas operacionais

- Discoverability de `/migrate-backlog-to-forge` vive em README + docs/install.md (Bloco 4) por design — `/init-config` **não** cita o helper para preservar atomicidade da skill setup (concerns desacoplados per decisão standalone v0 deste /triage). Revisita se sinal empírico de fricção de descoberta emergir (operadores rodando `/init-config` + esquecendo de migrar manualmente quando BACKLOG.md pré-existente).
- Ordem dos blocos: 1 antes de 2-3 (adendo CLAUDE.md formaliza pattern sub-tools/ antes da 1ª instância materializar); 2 antes de 3 (SKILL.md define interface, sub-tool implementa); 4 depois (doc cross-refs após substância shipada).
- Sub-tool é 1ª instância do pattern `skills/*/sub-tools/` neste repo — formalizada no Bloco 1 (adendo CLAUDE.md). Não cria ADR novo (refinement de skill consumer-side existente per ADR-058 + adendo CLAUDE.md; ADR-017 cross-project precedent reconhecido como meta-bridge).
- `/run-plan §3.5` no done: `[capture:validacao]` markers permanecem no plan body (sem materialização em forge issue — operador executa manualmente em sessão futura).
- `/run-plan §3.4` no done: BACKLOG mark + plan body Status removal. Em modo forge, BACKLOG ## Próximos já drenado — `/run-plan` precisa fechar a issue `#125` em vez de mover linha (linha do backlog é `#125: ...` per Contexto). Closes #125 via comment ou via `gh issue close` — operador valida no done.

## Decisões absorvidas

- design-reviewer F4 (revisão plano 2026-06-19): alternativa "trim determinístico ≤80 chars" para geração de títulos rebatida em § Resumo da mudança com exemplo concreto (caminho-único).
- design-reviewer F5 (revisão plano 2026-06-19): discoverability via README + docs/install.md por design declarada em § Notas operacionais (caminho-único).
