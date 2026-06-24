# Plano — Passo de prior-art scan no /triage

## Status

Pendente

## Contexto

Materializa a faceta mecânica A2 da doutrina cross-cutting do meta-system ADR-023 (`prior-art scan canonical pré-build — build-vs-adopt no inception`) no repo dono do `/triage`, conforme decidido em ADR-071. A doutrina (what/why) mora upstream; este plano wira só a mecânica (how) no fluxo do `/triage`, na forma inline-prosa (target-aware per meta-system ADR-016 — scan é heurístico-semântico dominante; sub-tool determinístico foi descartado por Ockham).

**ADRs candidatos:** ADR-071 (decisão que este plano materializa), ADR-053 (família triage-ecosystem wiring; rebate de simetria de gatilho em ADR-071 § Alternativas), ADR-063 (família; caminho-atômico → prompt-reviewer), ADR-067 (filtro skip-silente doc-reviewer, relevante ao Bloco 2).

**Linha do backlog:** #155: Passo de prior-art scan no /triage (operacionaliza meta-system ADR-023; forma target-aware)

## Resumo da mudança

Adicionar um sub-passo de **prior-art scan** ao step 2 do `/triage` (`skills/triage/SKILL.md`), na forma de gate prosa-heurística (não enum), seguindo a decisão de ADR-071:

- **Posição:** sub-passo dentro do step 2, após os gates de intenção-vaga / escopo / decomposição (pressupõe intenção cristalizada), **antes da resolução de bifurcação arquitetural** e antes do step 3 (decidir o artefato — o resultado do scan informa build-vs-adopt, que molda o artefato). Ordem scan→bifurcação deliberada (ADR-071 § Placement): "adotar inteiro/inspirar" pode tornar a bifurcação moot.
- **Gatilho proporcional:** dispara em nova capacidade / novo formato-protocolo / build custom não-trivial; não dispara em bugfix / refactor interno / doc / glue acoplado ao setup pessoal. Zona cinzenta → default conservador (na dúvida, escanear; registrar a decisão de pular quando se pula). Discriminado por **natureza do trabalho**, não por tipo de artefato (rebate de simetria com ADR-053 em ADR-071 § Alternativas).
- **Resposta em espectro:** construir / adotar inteiro / estender parcial / inspirar-se em parte — aprender com partes é resultado de 1ª classe.
- **Trail auditável:** registra scan feito? decisão keep/adopt/extend/inspire? por quê? — no `## Contexto` do plano quando há plano, ou na prosa do report nos demais caminhos. Alimenta o `§ Critério de erosão` do meta-system ADR-023.
- **Goodhart guard:** gate raciocinado in-line (prosa, não enum/checkbox); não compete na chamada `AskUserQuestion` unificada do step 2 nem sequencia prompt adicional (step 2 é checklist mental, não questionário).

Fora de escopo: alterar a forma para sub-tool/MCP (descartado em ADR-071); tocar o `/new-adr`, `/run-plan` ou outros reviewers (ortogonal); duplicar a doutrina de ADR-023 no SKILL (referenciar, não copiar).

## Arquivos a alterar

### Bloco 1 — sub-passo prior-art scan no step 2 do /triage {reviewer: prompt}

- `skills/triage/SKILL.md`: adicionar um bullet de gate no checklist mental do step 2 (`### 2. Esclarecer gaps com o usuário`), posicionado **antes** do bullet "Bifurcação arquitetural" (linha ~63) — após os gates de intenção-vaga / escopo / decomposição e antes da bifurcação (per F2 / ADR-071 § Placement: o scan precede a bifurcação porque decide build-vs-adopt; "adotar inteiro" pode tornar a bifurcação moot). Roda antes do step 3. Conteúdo do bullet (`**Prior-art scan (build-vs-adopt):**`):
  - Gatilho proporcional (dispara em nova capacidade / novo formato-protocolo / build custom não-trivial; não dispara em bugfix/refactor/doc/glue-pessoal; zona cinzenta → default conservador escanear + registrar decisão de pular quando pula).
  - Quando dispara: varredura de soluções de mercado validadas + comparação build-vs-adopt; resposta em espectro (construir / adotar inteiro / estender parcial / inspirar-se em parte).
  - Forma: gate prosa-heurística raciocinado in-line — **não** enum, **não** compete na chamada `AskUserQuestion` unificada do step 2, **não** sequencia prompt adicional.
  - Trail auditável: registrar scan feito + decisão de espectro + razão no `## Contexto` do plano (caminho-com-plano) ou na prosa do report (demais caminhos). Referenciar ADR-071 (mecânica local) e meta-system ADR-023 (doutrina) — não duplicar a doutrina.
  - Fronteira/precedência: precede o step 3 e a resolução de bifurcação; pressupõe intenção cristalizada (precedência da gate de intenção-vaga).
- `skills/triage/SKILL.md`: no caminho-com-plano, o trail do scan vai para o `## Contexto` do plano via **campo nomeado** `**Prior-art scan:**` carregando a decisão de espectro (construir/adotar/estender/inspirar) — grepável, porque o critério de erosão de ADR-071/ADR-023 depende de auditar "≥3 scans zero-adoção" (auditabilidade > Ockham marginal aqui). O "por quê" pode seguir em prosa curta após a decisão. Adicionar menção ao campo no step 4 (`**Plano (papel: plans_dir)**`, região do `## Contexto`), coerente com os demais campos nomeados (`**Termos ubíquos tocados:**`, `**ADRs candidatos:**`). Atualizar `templates/plan.md` (comentário dos campos especiais do `## Contexto`) com o campo opcional `**Prior-art scan:**`.

### Bloco 2 — documentar o wiring em CLAUDE.md

- `CLAUDE.md`: adicionar um bullet na seção "Editing conventions" (após o bullet de ADR-070, seguindo o gabarito dos bullets de wiring de ADR existentes) referenciando ADR-071 — o que é (passo de prior-art scan no /triage step 2), forma (inline-prosa target-aware), gatilho proporcional, relação com a família triage-ecosystem (ADR-036/-053/-063) e com a doutrina upstream meta-system ADR-023. Edit predominantemente additive seguindo siblings de mesmo gabarito.

**Sem anotação `{reviewer}` intencional** — `CLAUDE.md` resolve para `doc-reviewer` (doc-only ampla, fora do path-set narrow de ADR-062), e o edit (predominantemente additive + bullet em ≥2 siblings adjacentes de mesmo gabarito `ADR-NNN`) bate o predicado de skip-silente de ADR-067. **Não anotar `{reviewer: doc}`** — anotação explícita é override do operador e desativa o filtro.

## Verificação end-to-end

Repo markdown sem suite (`test_command: null`) — inspeção textual passo-a-passo:

1. `grep -n "Prior-art scan\|prior-art scan" skills/triage/SKILL.md` retorna ≥1 match no step 2. Confirmar por Read que o bullet está posicionado **após** a gate de intenção-vaga e **antes** do bullet "Bifurcação arquitetural" (ordem scan→bifurcação per F2 / ADR-071 § Placement).
2. O bullet adicionado cita o gatilho proporcional (dispara/não-dispara + zona cinzenta) e a resposta em espectro (construir/adotar/estender/inspirar).
3. `grep -n "ADR-071\|ADR-023" skills/triage/SKILL.md` retorna match (referência à mecânica local + doutrina upstream, sem duplicar a doutrina).
4. O bullet declara explicitamente que o scan é gate prosa-heurística e não compete na chamada `AskUserQuestion` unificada do step 2 (Goodhart guard + preservação da unificação de prompts).
5. `grep -n "ADR-071" CLAUDE.md` retorna match no bullet de "Editing conventions".
6. `grep -n "Prior-art scan" templates/plan.md` retorna match no comentário dos campos especiais do `## Contexto`.

## Verificação manual

Surface não-determinística (comportamento de agente LLM no `/triage`). A exigência (a) "forma do dado real" do step 2 não-aplica aqui — o input é intenção em linguagem natural livre, não dado estruturado/parseável; o que se valida é o julgamento do agente via cenários enumerados (b). Smoke pós-`/reload-plugins` em sessão CC, exercitando:

- **C1 — gatilho dispara (build não-trivial):** `/triage` com intenção de nova capacidade/build custom não-trivial (ex.: "adicionar um cache de respostas LLM") → o scan dispara, registra trail (scan feito + decisão de espectro + razão) e o resultado informa a escolha do artefato no step 3.
- **C2 — gatilho não dispara (caso leve):** `/triage` com bugfix/refactor/doc-only → o scan **não** dispara (gatilho proporcional); fluxo do step 2 segue sem o gate.
- **C3 — zona cinzenta:** intenção ambígua entre build trivial e não-trivial → default conservador (escaneia); se decide pular, a decisão de pular fica registrada no trail.
- **C4 — espectro não-binário:** scan que conclui "adotar inteiro" ou "inspirar-se em parte" → o artefato resultante reflete a decisão (ex.: linha de backlog "adotar X" em vez de plano de build).
- **C5 — não-fragmentação do enum:** quando coexistem gaps enum-áveis (escopo + bifurcação), o scan em prosa **não** vira pergunta extra nem fragmenta a chamada `AskUserQuestion` unificada.

## Pendências de validação

- `[capture:validacao]` Smoke comportamental C1-C5 do `## Verificação manual` pós-`/reload-plugins` em sessão CC real — exige o plugin recarregado + julgamento LLM sobre o fluxo do `/triage`; não exercitável na execução do `/run-plan`. Operador roda manual; promover ADR-071 `Proposto` → `Aceito (YYYY-MM-DD)` após ≥1 invocação real bem-sucedida do gate disparando e registrando trail.

## Decisões absorvidas

- Bloco 1 + templates/plan.md: trail do scan via campo nomeado `**Prior-art scan:**` (grepável) em vez de prosa livre — auditabilidade do critério de erosão > Ockham marginal (caminho-único).
- Bloco 2: nota de no-annotation intencional habilitando o skip-silente de doc-reviewer (ADR-067); proíbe `{reviewer: doc}` reflexo (caminho-único).
- Verificação end-to-end item 1: ganha verificação de posicionamento do bullet (após intenção-vaga, antes de bifurcação) (caminho-único).
- Verificação end-to-end: removido o check de `git status BACKLOG.md` (cerimônia — repo em modo forge, nenhum bloco toca BACKLOG); substituído por check de `templates/plan.md` (caminho-único).
- Verificação manual: cláusula explicitando que a exigência "forma do dado real" não-aplica (input é intenção NL livre) (caminho-único).
