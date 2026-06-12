# Plano — Skill `/session-audit` (audit de captura pendente pré-encerramento)

## Contexto

Pedido recorrente do operador: "verifique se todos os itens de backlog e respectivos contextos necessários foram devidamente registrados nos artefatos adequados" antes de invocar `/journal-close`. Substância universal cross-projeto (meta-system, h3-finance-agent, TJPA workflows, etc.). Cristaliza pattern editorial novo: **audit de captura pendente sessional** (não periódica como `/curate-backlog`).

Substância da skill: (a) lê transcript da sessão CC corrente identificando substância gerada (decisões tomadas, classifications, findings emergidos sem persistência, drift conhecido, side-effects substantivos); (b) audita se cada peça está em artefato adequado per Resolution Protocol (`paths.backlog`, `paths.decisions_dir`, `paths.plans_dir`, `.claude/local/NOTES.md`); (c) classifica gaps por tipo + artefato sugerido; (d) reporta relatório markdown agrupado; (e) cutucada batched single-call paralelo a `/curate-backlog` §3.5 forge.

Substância de raciocínio dominante (julgamento "vale persistir?", "onde mora?", "essa decisão é matéria de ADR ou só commit?") — Cond 1 ADR-011 do meta-system falha por design → skill markdown per § "Skill = pensamento" (revisado por ADR-016 do meta-system target-aware). Per ADR-008 do meta-system (homing arquitetural per necessidade): necessidade universal stack-agnóstica → toolkit universal.

**ADRs candidatos:** ADR-045 (filtro de admissão — categoria editorial nova passa por critério "padrão emergente em 3+ instâncias OU mecânica repetida quase-toda-sessão" — operator pediu múltiplas sessões = sinal de padrão emergente); ADR-057 (`/curate-backlog` paralelo a ADR-022 — precedente cristalização ADR per skill editorial); ADR-022 (archive-plans — precedente categoria editorial periódica); ADR-009 (revisor design pré-fato — design-reviewer audita este plano).

**Linha do backlog:** Skill `/session-audit` — audit de captura pendente sessional (universal cross-projeto; cristaliza pedido recorrente do operador antes de /journal-close)

## Resumo da mudança

- **Skill `/session-audit`** em `skills/session-audit/SKILL.md`: nova skill editorial sessional. Trigger manual (operador invoca); extension hint em `/run-plan` §3.6 sugere invocação antes de encerramento. Escopo: **captura pendente só** (substância gerada não-persistida em BACKLOG/NOTES/ADRs/plans) — sem expansão pra cross-refs faltantes ou side-effects executados (YAGNI; reabrir se dor materializar).
- **Interface output**: relatório markdown agrupado + cutucada batched single-call (header `Captura`, opções `Aplicar tudo (Recommended)` / `Aplicar parcial (Other)` / `Cancelar` — pattern paralelo a ADR-022 archive-plans + ADR-057 curate-backlog (write-local non-destructive); NÃO importa pattern ADR-058 § (e) 2ª instância porque não há mutação remota. Operator descreve subset via Other.
- **Extension hint em workflow skills**: `/run-plan` §3.6 ganha sugestão textual 1-linha antes do marker `Plan done. [PRAGMATIC: plan-done]`: "Considere `/session-audit` antes de fechar a sessão" — não-bloqueante, informativo.
- **CLAUDE.md inventário**: nova entry na lista de skills do plugin + descrição breve.
- **ADR cristalizando categoria editorial "audit captura pendente sessional"** via `/new-adr` — pattern paralelo a ADR-057 (categoria editorial periódica `/curate-backlog`). Distinção: ADR-057 cristaliza periódica; este ADR cristaliza sessional. Cross-refs a ADR-022 + ADR-057 + ADR-045 + ADR-009.

**Fora de escopo**:
- Hook automatic CC `Stop` event sugerindo `/session-audit` (rejeitado per F4 cutucada — coupling com CC event lifecycle; pattern análogo a `suggest_journal_close` do meta-bridge ficou em meta-bridge por design).
- Integração tight com meta-bridge `/journal-close` (cross-plugin coupling rejeitado por design; operator invoca skills sequencialmente livre).
- Auto-classify enums no batched output (operator descreve subset via Other — simpler).
- Escopo expandido (side-effects, cross-refs, ADRs sem cross-ref) — fica para revisão futura quando dor materializar (≥3 sessões com gaps deste tipo emergindo).

## Arquivos a alterar

### Bloco 1 — Skill nova `/session-audit` {reviewer: doc}

- `skills/session-audit/SKILL.md` (novo): SKILL.md com frontmatter (description trigger semantics, roles informational), passos numerados:
  - Passo 1: parse argumento (sem args — opcional `--scope <area>` para focar em subset de artefatos);
  - Passo 1.5: detecção de `paths.backlog: forge` (per F5 cutucada) — skill marca findings de tipo `captura_backlog` como **defer pra `/triage`** com nota informativa apontando ADR-058 § (e) 1ª instância policy; não propõe `gh/glab issue create` direto. Forge mode preserved silente, gaps reportados sem ação remota.
  - Passo 2: análise do transcript da sessão — heurísticas detectivas listadas em § Heurísticas:
    - palavras-chave indicativas de substância gerada ("decidi", "classifico", "identifiquei drift", "concluí", "smoke validado");
    - tool calls não-acompanhados de Edit/Write em artefato canonical (decisão tomada inline sem persistência);
    - findings/cutucadas resolvidas sem entry derivada (ADR-style ou BACKLOG-style);
    - cross-refs declarados em commit messages mas não materializados em ADRs/CROSS-INDEX equivalents;
  - Passo 3: resolução de artefatos via Resolution Protocol (paths.* do CLAUDE.md);
  - Passo 4: para cada substância detectada, classifica tipo + artefato sugerido — schema `{tipo, substancia_breve, artefato_sugerido, citação_transcript, ação_sugerida_prosa_curta}`. **`citação_transcript` obrigatória** (não opcional) — substância sem citação concreta do transcript não passa pro relatório (salvaguarda contra hallucination paralela à constraint de `/new-adr` "não inventar Contexto/Decisão sem input explícito"). `tipo` é enum fechado nos 4 destinos do Passo 5; `artefato_sugerido` cita explicitamente: BACKLOG.md (papel `paths.backlog`), NOTES.md (`.claude/local/NOTES.md` per ADR-054), ADR (`docs/decisions/` per `paths.decisions_dir`), CLAUDE.md/philosophy.md (per ADR-045 § Decisão parte 2 filtro tabela);
  - Passo 5: relatório markdown agrupado por tipo (Captura BACKLOG / Captura NOTES / Cristalização ADR / Atualização doutrina canonical) + cutucada batched single-call. Cross-refs faltantes ficam **fora de escopo** (decisão F2 cutucada); essa categoria não aparece nos enums.
  - Passo 6: aplicar capturas conforme escolha (write to artifact via Edit/append; preservar autoria editorial);
  - § O que NÃO fazer: não inventar substância sem base concreta no transcript (paralelo a ADR-053 e à constraint do `/new-adr` "não inventar Contexto/Decisão sem input explícito do operador"); não executar capturas sem cutucada afirmativa; não interpretar side-effects como captura pendente (fora de escopo); não aplicar capturas em projetos sem `paths.*` declarados (papel "não temos") sem oferta de criação canonical paralela ao sub-fluxo do `/triage` step 1; **não tratar Read defensivo (`Read` sem Edit subsequente) como gap de captura** — Read é validação per `philosophy.md` § Busca pela verdade, não decisão pendente; gap requer **decisão emitida** (classification, drift declarado, finding cristalizado em prosa).

### Bloco 2 — Extension hint em `/run-plan` §3.6 {reviewer: doc}

- `skills/run-plan/SKILL.md` §3.6 (Declarar done): adicionar 1-linha textual antes do marker canonical `Plan done. [PRAGMATIC: plan-done]`: "Considere `/session-audit` antes de fechar a sessão pra verificar captura pendente". Não-bloqueante; texto informativo. Linha pode ser opt-out via `paths.session_audit_hint: false` no CLAUDE.md se operator achar ruidoso (YAGNI até dor materializar — não codificar no inicial).

### Bloco 3 — CLAUDE.md inventário + README {reviewer: doc}

- `CLAUDE.md` — adicionar `/session-audit` na lista canonical de skills do plugin (section que enumera workflow skills); descrição alinhada com o pattern editorial existente.
- `README.md` — entry na § What's inside se há padrão de listing das skills.

### Bloco 4 — ADR via `/new-adr` cristalizando 2 categorias editoriais {reviewer: doc}

- `docs/decisions/ADR-NNN-skill-session-audit-categorias-editoriais.md` (via `/new-adr` no toolkit cwd): codifica **2 sub-decisões editoriais**:
  - **Sub-decisão (a) — categoria "audit captura pendente sessional"**: trigger temporal sessional (distinta de periódica como ADR-057 `/curate-backlog` e ADR-022 archive-plans); substância multi-artefato (BACKLOG/NOTES/ADR/plan) vs ADR-057 substância single-artefato (BACKLOG). § Override do critério N=3 do ADR-045 análogo a ADR-057 § Override (operator declaration registra padrão recorrente; valor antecipado cristaliza categoria em <3 instâncias).
  - **Sub-decisão (b) — categoria "extension hint cross-skill no done"**: pattern do hint informativo em `/run-plan` §3.6 sugerindo invocação de skill correlata antes do marker canonical `Plan done. [PRAGMATIC: plan-done]`. Distinto de cutucada de descoberta canonical ADR-046 (config block, gating tri-state); semanticamente "sugestão skill correlata" não-bloqueante. Pavimenta categoria pra futuras hints (≥2 hints similares emergirem reabre como pattern auditável).
- § Origem: ADR-045 (filtro admissão — padrão emergente operador-recorrente; override N=3 documentado); ADR-057 (precedente categoria editorial paralelo com Override N=3); ADR-022 (precedente skill editorial periódica); ADR-049 (consolidação `/run-plan` — superfície §3.6 modificada por sub-decisão (b)); ADR-046 (cutucada de descoberta canonical — semanticamente distinta).
- § Decisão: 2 sub-decisões cristalizadas com critério explícito de admissão (ADR-045 zona cinzenta + Override registrado).
- § Trade-offs: cross-plugin coupling rejeitado (skill autônoma vs hook `/journal-close` pre-event); operator invoca manual + hint não-bloqueante; risco subestimado de parsing fragility no marker `[PRAGMATIC: plan-done]` (linha extra textual antes do marker — mitigação: marker preservado intacto em linha própria; hint vai antes em parágrafo separado).
- § Gatilhos de revisão: (1) ≤2 invocações de `/session-audit` em 6 meses pós-shipping; (2) ≥2 extension hints cross-skill análogos emergirem (categoria editorial nova consolidada — reabrir pra refinar pattern); (3) ruído sustained no hint do `/run-plan` §3.6 (operator silencia frequentemente) — reabrir opt-out via `paths.session_audit_hint: false`.

## Verificação end-to-end

Sem suite formal de testes pra skill markdown (toolkit é docs-only-ish — `test_command: null`). Validação textual + cenários manuais:

1. `skills/session-audit/SKILL.md` existe com frontmatter válido (description não-vazia + roles).
2. `grep -l "/session-audit" CLAUDE.md README.md` retorna ≥1 match.
3. `grep -A2 "Plan done. \[PRAGMATIC" skills/run-plan/SKILL.md` mostra a linha hint informativa.
4. ADR criado via `/new-adr` existe em `docs/decisions/` com status canonical.

## Verificação manual

Surface não-determinística (skill LLM audita transcript) — cenários enumerados:

1. **Cenário positivo (substância pendente detectável)**: invocar `/session-audit` em sessão sintética contendo decisões + classifications sem persistência (cenário-base: sessão atual do meta-system pre-captura dos 3 gaps que fizemos manualmente). Esperado: identifica gaps de captura editorial (smoke real cross-skill não-persistido, classifications novas /mechanical-skills-scan não-NOTES'd, drift snapshot conhecido sem entry no BACKLOG). Cutucada batched dispara.

2. **Cenário negativo (sessão sem substância pendente)**: invocar em sessão recém-iniciada sem substância gerada substantiva (apenas leitura de arquivos, sem decisões). Esperado: relatório enxuto "0 gaps detectados; encerramento limpo". Sem cutucada disparada.

3. **Cenário borderline (tudo persistido)**: invocar pós `/run-plan` completo bem-documentado (todas decisões captured em commit messages + plano bem-fechado). Esperado: 0 gaps OU gaps marginais (escopo "captura pendente só" não cobre side-effects nem ADRs sem cross-ref).

4. **Cenário cross-projeto sem papéis declarados**: invocar em projeto sem `paths.backlog` declarado (caso "não temos"). Esperado: relatório limita-se a NOTES (sempre disponível via ADR-054)/ADRs/plans onde declarados; backlog skipped silente com nota informativa.

5. **Cenário Other (operator descreve subset)**: cutucada batched dispara com 5 gaps; operator escolhe `Aplicar parcial` via Other com prosa "aplicar gaps 1 e 3, cancelar os outros". Esperado: subset aplicado; cancelados ficam no relatório como referência informativa da sessão (sem persistência editorial).

6. **Cenário paths.backlog: forge** (TJPA-style — per F5 cutucada): invocar `/session-audit` em projeto com `paths.backlog: forge` declarado, sessão com substância candidata a BACKLOG entry. Esperado: skill detecta mode forge + marca finding como **pendente para `/triage` subsequent** (`tipo: captura_backlog`, `artefato_sugerido: '/triage step 4 - modo forge cobre mutação remota per ADR-058 § (e) 1ª instância'`); NÃO propõe `gh/glab issue create` direto. YAGNI — `/triage` step 4 já tem policy codificada; skill não duplica mecânica granular per-mutation.

## Pendências de validação

- Smoke comportamental real dos 6 cenários do `## Verificação manual` pós-merge + `/reload-plugins` em sessão CC real exercitando: (1) positivo — substância pendente detectável; (2) negativo — sessão sem substância; (3) borderline — pós-`/run-plan` bem-fechado; (4) sem papéis declarados; (5) Other subset; (6) modo `paths.backlog: forge`. Não simulável mecanicamente nesta execução do `/run-plan` — skill aplica julgamento LLM sobre transcript (paralelo aos demais planos shippados nesta sessão com validação comportamental pendente).

## Notas operacionais

- Modo canonical (sem `**Modo:**` — feature contida em 1 repo toolkit; sem cross-repo system-surgery). `/run-plan` executa em worktree isolada com micro-commits per bloco. **`/run-plan` a partir de cwd `~/Projects/pragmatic-dev-toolkit` (NÃO de meta-system).**
- Bloco 1 (SKILL.md substância editorial) é o bloco mais denso; doc-reviewer audita coerência interna + alinhamento com pattern editorial do toolkit (categoria "skill editorial" estabelecida em ADR-057).
- **Pré-condição forte cross-cwd**: operador valida `pwd` retorna `~/Projects/pragmatic-dev-toolkit` ANTES de invocar `/run-plan` E ANTES de invocar `/new-adr` no Bloco 4. Cross-mismatch produz ADR + commit em repo errado (paralelo nominal à constraint deste `/triage` rodando em meta-system NÃO é mitigação — é nome do mesmo problema). Recovery via `git mv` + reaplicar `/new-adr` no cwd correto. Linha `**Branch:**` recomendada no `## Contexto` per ADR-049 § Decisão (b) se branch já existe no toolkit antes do `/run-plan §1.1`.
- Memory `feedback_meta_status_per_adr_trail` valoriza trail per-finding em /meta-status; este plano adota batched single-call por compromisso (escopo "captura" tipicamente gera 2-5 gaps; per-gap = N cutucadas friction). Trade-off aceito; reabrir se ruído emergir.
- Pattern do hint em /run-plan §3.6: texto **informativo não-bloqueante**, não `AskUserQuestion` (operator decide invocar livre); paralelo à cutucada de descoberta canonical do toolkit mas semanticamente distinto (esta sugere skill, descoberta canonical sugere config block).
- **Plano criado via `/triage` rodando em meta-system cwd mas escrito em `~/Projects/pragmatic-dev-toolkit/docs/plans/` via Write tool absolute path** (operator escolheu "/triage no toolkit"). Commit + push acontecem em `~/Projects/pragmatic-dev-toolkit` cwd manualmente via Bash (não via `/triage` step 5 automation, que opera em meta-system cwd com cd reset).
- `**Linha do backlog:**` declarada no `## Contexto` — `/run-plan` §3.4 ao done adiciona em `## Concluídos` do toolkit BACKLOG.md (não há entrada equivalente em `## Próximos`; caminho-com-plano per ADR-049 § Decisão (a)).

## Decisões absorvidas

- Bloco 1 Passo 4 schema: `citação_transcript` tornada obrigatória (não opcional); `tipo` enum fechado nos 4 destinos; `artefato_sugerido` cita explicitamente BACKLOG/NOTES/ADR/CLAUDE-philosophy; cross-refs marcados fora de escopo no Passo 5 (caminho-único — coerência interna com escopo F2 cutucada).
- Bloco 1 § O que NÃO fazer: adicionado bullet sobre Read defensivo não ser gap de captura (per philosophy.md § Busca pela verdade); previne falso positivo massivo (caminho-único).
- Notas operacionais cross-cwd: pré-condição forte explícita (`pwd` validation antes de `/run-plan` e `/new-adr`); recovery via `git mv` documentado; `**Branch:**` recomendada per ADR-049 § Decisão (b) (caminho-único).
