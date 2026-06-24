# ADR-070: session-audit cria issue forge direto para substância cristalizada (discriminação cristalizado vs defer)

**Data:** 2026-06-24
**Status:** Proposto

**Próxima revisão:** 2026-12-24
**Cadência:** trimestral
**Critério de erosão auditável:** reabrir se ≥1 das 3 cláusulas bater — (a) ≥2 issues criadas pelo caminho direto fechadas em `/next`/`/curate-backlog` subsequente sem trabalho de código associado (sinal mecânico observável de issue-fantasma, ancorado no predicado do incidente kl-score de [ADR-069](ADR-069-gate-verificacao-estado-antes-materializar-captura-notes.md), não no contrafactual "o que `/triage` teria feito"); (b) override do default-conservador (operador escolhe criar-direto sobre o defer sugerido pela skill) reportado ≥2 vezes em `.claude/local/NOTES.md`; (c) taxa de findings `captura_backlog` classificados `cristalizado` > 80% numa janela de ≥3 sessões com forge ativo (sinal de que a discriminação virou no-op e todo `captura_backlog` vira criação direta, anulando a fronteira editorial que motivou o defer original).

## Origem

- **Decisão base:** [ADR-061](ADR-061-skill-session-audit-categorias-editoriais.md) (categoria editorial `/session-audit`) + [ADR-058](ADR-058-role-backlog-aceitar-forge.md) § (e) (policy de cutucada por mutação remota) — este ADR refina o *defer stance* herdado dessas duas decisões.
- **Investigação:** issue [#145](https://github.com/fppfurtado/pragmatic-dev-toolkit/issues/145); incidente concreto na sessão `triage-chamado` (2026-06-22), onde o finding "GLPI_HOST duplicado" exigiu invocação manual de `gh issue create` após o `/session-audit` deferir pra `/triage`.

## Contexto

`/session-audit` em modo `paths.backlog: forge` sempre defere findings de tipo `captura_backlog` para `/triage` (passo 1.5 + passo 6 da `skills/session-audit/SKILL.md`), com a justificativa de que "duplicar a mecânica de forge quebraria a fronteira editorial" — `/triage` step 4 modo forge já carrega a mecânica de criação de issue (`gh`/`glab issue create` com cutucada por mutação).

Na prática, quando o item é simples e a substância já está clara o suficiente para virar issue diretamente, o defer cria um passo extra desnecessário: o operador encerra o audit, re-invoca `/triage`, repassa a mesma substância. O incidente de 2026-06-22 materializou o custo — `gh issue create` manual fora de qualquer skill, perdendo a cutucada de confirmação e o template de body.

O argumento original da "fronteira editorial" é sobre **evitar side-effects silenciosos** (mutação remota sem confirmação do operador), não sobre evitar duplicação de mecânica em si. A cutucada de confirmação batched do passo 5 (já existente, per ADR-058 § (e) 2ª instância batched-com-seleção) já contém o blast radius — o operador confirma cada mutação remota antes de aplicar.

## Decisão

Discriminar dois casos de `captura_backlog` em modo `forge` no passo 1.5 / passo 6 da `/session-audit`, em vez do defer incondicional atual:

- **Substância cristalizada** — finding cujo `ação_sugerida_prosa_curta` já contém título e contexto suficientes para virar issue como-está, sem necessidade de escopo/labels/decomposição ou bifurcação arquitetural adicional → `/session-audit` oferece **criação direta no forge** dentro da cutucada batched do passo 5. A `description` da opção carrega título + body draft para o operador revisar antes de confirmar. Execução no passo 6 via `gh issue create` / `glab issue create` seguindo `forge-auto-detect.md`.

- **Substância não cristalizada** — finding vago, ou que abre bifurcação de escopo/arquitetura, ou que requer decisão de `/triage` → **comportamento atual preservado**: defer pra `/triage` com nota informativa.

Razões objetivas:

- **A fronteira editorial é preservada pela cutucada, não pelo defer.** A cutucada batched do passo 5 confirma cada mutação remota (policy de ADR-058 § (e) intacta — `Aplicar` é confirmação explícita); o defer era um proxy conservador desnecessário quando a substância já está clara.
- **Replicação parcial da mecânica de `/triage` step 4 é aceitável.** A criação forge é essencialmente um comando (`gh issue create -t -b`); a parte compartilhada (detecção de host) já vive em `forge-auto-detect.md`, consumido por ambas as skills. Extrair procedure dedicada para um comando seria over-engineering (YAGNI).
- **Default-conservador na discriminação preserva `/triage` como rede a jusante.** Ambíguo → tratar como não-cristalizado → defer. A criação direta só dispara quando a skill tem confiança de que a substância está clara; o caminho rico (`/triage`) permanece disponível por inação.
- **Composição com o gate de [ADR-069](ADR-069-gate-verificacao-estado-antes-materializar-captura-notes.md).** Quando o finding cristalizado origina de entry pré-existente do `.claude/local/NOTES.md`, o gate verificar-estado-antes-de-materializar roda **antes** da criação forge: já-resolvido → baixa via append no NOTES.md + pular criação; pendente/indeterminado → criação segue. **Mudança de responsabilidade real, não herança trivial:** o passo 6 modo forge atual *delega* o gate ao `/triage` (a `skills/session-audit/SKILL.md:121` registra que a corretude para capturas forge NOTES-sourced depende do wiring de `/triage` passo 4). O caminho de criação direta **internaliza** o gate localmente no passo 6 forge (paralelo ao que o passo 6 modo *arquivo* já faz na linha 120); o caminho de defer **preserva** a delegação atual ao `/triage`. Isto materializa o forward-compat que ADR-069 § Limitações já registrou ("se #145 for implementado, o gate precisa rodar **antes** do filing direto, senão #145 cria a issue-fantasma que este ADR previne"). O gate precede o canal (forge) per ADR-069.

Esta decisão é a **3ª instância** do sub-caso editorial batched-com-seleção de ADR-058 § (e) (1ª: consolidação `/triage` step 4 granular; 2ª: `/run-plan` §3.5 batched; 3ª: esta — `/session-audit` passo 5 batched para criação direta).

## Auto-aplicação per ADR-034

- **Cond 1 (decisão estrutural sem ancestral):** NÃO aplica — tem ancestral direto em ADR-061 + ADR-058 § (e).
- **Cond 2 (substitui ADR ancestral):** NÃO aplica — ADR-061 e ADR-058 permanecem vigentes; este ADR refina o *defer stance* de uma superfície específica (modo forge da `/session-audit`) sem revogar as decisões centrais.
- **Cond 3 (codifica restrição externa):** NÃO aplica.
- **Cond 4 (introduz categoria nova):** APLICA — a discriminação "substância cristalizada vs não-cristalizada" como gate de filing direto-vs-defer é categoria nova; sem precedente direto no toolkit.
- **Cond 5 (sucessor parcial):** APLICA — sucessor parcial de ADR-061 (escopo forge de `/session-audit`) e de ADR-058 § (e) (3ª instância do sub-caso batched).

Cond 4 + Cond 5 simultâneas — pattern estabelecido por ADRs ≥ADR-045 (ex.: ADR-064, ADR-069).

### § Override do critério N=3 (ADR-043 § Ockham operacionalizado #4)

Esta decisão cristaliza com **1 instância empírica** (incidente `triage-chamado` 2026-06-22), abaixo do piso N=3. **8ª aplicação da onda Override do critério N=3** (após ADR-057→-061→-062→-063→-064→-065→-067, as 7 consecutivas; ADR-068/-069 não invocaram Override — ADR-069 ancorou em incidente empírico próprio, kl-score 2026-06-23). O custo de não-cristalizar é o operador re-derivar a discriminação a cada sessão + recorrer a `gh issue create` manual fora de qualquer skill (perdendo cutucada e template). Fragilidade epistêmica reconhecida: N=1 + auto-relato do operador via issue. O critério de erosão auditável (cláusulas a/b/c acima) é o teste empírico forward — se a discriminação produzir issues-fantasma ou virar no-op, reabre.

**Meta-avaliação de hábito Override pendente.** [ADR-064](ADR-064-gate-com-executor-validacao-2-sites.md) § Override prometeu, após a 5ª aplicação consecutiva, uma avaliação meta-editorial separada (via `/triage "avaliar meta-pattern Override critério N=3"`) sobre se o Override está virando hábito vs. exceção rara. A onda avançou até a 8ª (esta) sem que essa avaliação rodasse — ela permanece deferida e agora vencida. Este ADR não bloqueia a substância (pattern empírico + incidente concreto justificam per-se), mas registra o débito explicitamente para o operador disparar a meta-avaliação.

## Alternativas consideradas

### Defer enriquecido (pré-preenchimento pro `/triage`, mantendo site único de criação)

Em vez de a `/session-audit` ganhar mecânica de criação forge própria, o defer atual poderia ser **enriquecido**: a skill pré-materializa a substância cristalizada (título + body draft) e passa ao `/triage` via handoff (NOTES.md ou contexto de sessão), preservando a regra de ADR-061 § Trade-offs ("categoria editorial sem co-localização") e mantendo um **único site de criação forge** (`/triage` step 4) — sem adicionar a 3ª superfície de mutação forge que esta decisão lista como trade-off.

**Rebatida:** o custo central que o incidente de 2026-06-22 materializou não é só "perder cutucada e template" — é o **passo extra** "encerrar audit → re-invocar `/triage` → repassar substância". O defer enriquecido elimina a perda de template, mas ainda paga esse passo extra (a substância sai do audit e re-entra no `/triage`). A criação direta é o único caminho que elimina o passo extra **e** preserva cutucada+template, dentro da mesma cutucada batched que o operador já está respondendo no fim do audit. O preço — 3ª superfície batched — é contido: a policy de ADR-058 § (e) é compartilhada por referência (não duplicada), e a mecânica de criação é um comando único sobre `forge-auto-detect.md` já compartilhado.

## Consequências

### Benefícios

- Elimina o passo extra (encerrar audit → re-invocar `/triage`) para substância já cristalizada.
- Fecha o gap materializado em 2026-06-22 (criação manual fora de skill, sem cutucada nem template).
- Preserva integralmente o caminho rico (`/triage`) para substância que genuinamente precisa de escopo/bifurcação.

### Trade-offs

- **Replicação parcial da mecânica forge** entre `/session-audit` passo 6 e `/triage` step 4 (criação de issue). Aceito: comando único, parte compartilhada já em procedure.
- **3ª superfície de mutação forge batched** — custo de manutenção (mudança na policy de ADR-058 § (e) agora toca 3 sites).
- **Risco de over-creation** se a discriminação for liberal demais (issue-fantasma que `/triage` teria refinado). Mitigado por: default-conservador (ambíguo → defer) + gate ADR-069 para NOTES-sourced + cutucada de confirmação por mutação. Cláusula (a)/(c) do critério de erosão monitora.

### Limitações

- A discriminação cristalizado-vs-defer é **heurística qualitativa** aplicada pela skill (paralela às heurísticas detectivas do passo 2), não predicado mecânico — sujeita a julgamento do modelo em runtime. A cutucada de confirmação é o cinto de segurança.

## Gatilhos de revisão

- **(a)** ≥2 issues criadas pelo caminho direto fechadas em `/next`/`/curate-backlog` subsequente sem trabalho de código associado (sinal mecânico de fantasma, predicado do incidente kl-score de ADR-069) → discriminação liberal demais; endurecer critério de cristalização ou reverter para defer incondicional.
- **(b)** Override do default-conservador reportado ≥2 vezes → o default está errado (substância "ambígua" estava de fato cristalizada); recalibrar.
- **(c)** Taxa `cristalizado` > 80% em ≥3 sessões → discriminação virou no-op; reavaliar se o defer ainda tem função.
