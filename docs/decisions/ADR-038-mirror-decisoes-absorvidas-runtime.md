# ADR-038: Mirror de Decisões absorvidas no plan body + consumo runtime por reviewers

**Data:** 2026-05-26
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-026](ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md) — sucessor parcial; estende § Forma do reporte com mirror no plan body sem revogar a regra do commit message.
- **Decisão base:** [ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) — refina § Decisão (subseção "Escopo do princípio para consumidores preservado") sobre `code-reviewer`: introduz categoria nova "context-aware via messenger upstream", distinta da rejeitada "free-read autônomo de ADRs".
- **Investigação:** Sessão de 2026-05-26 (ROADMAP item 6). Item 1 da mesma onda evidenciou regressão silenciosa: `code-reviewer` flaggou estrutura que `design-reviewer` pré-commit havia aprovado; sem perspicácia do agente para citar ADR-035 e cutucar via `AskUserQuestion`, o default-absorber teria revertido decisão aprovada pelo operador.
- **Classificação editorial:** Por [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) § "Novo ADR quando ≥1 das condições aplica", 5ª condição ("sucessor parcial — estende, refina ou condiciona ADR Aceito sem revogar") aplica → novo ADR (pattern paralelo a ADR-029→ADR-017, ADR-025→ADR-005, ADR-030→ADR-005). Adendo a ADR-026 sozinho não cobriria — refinamento toca também § Decisão de ADR-035.

## Contexto

[ADR-026](ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md) § Forma prescreve que findings absorvidos pré-commit pelo `design-reviewer` vivem em seção dedicada `## design-reviewer findings absorvidos` no **commit message** do plano. Auditoria via `git log -p`. Funciona para reconstrução histórica + revisão pós-fato pelo operador.

[ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) § Decisão (subseção "Escopo do princípio para consumidores preservado") explicita que `code-reviewer` mantém rubrica YAGNI universal sem context-aware switch nem free-read autônomo de ADRs. Override por inação do operador citando este ADR é o mecanismo prescrito quando `code-reviewer` flagga estrutura doutrinal legítima do plugin.

Gap observado em uso real (sessão 2026-05-26, ROADMAP item 1): `code-reviewer` invocado mid-execução por `/run-plan` flaggou estrutura aprovada pré-commit pelo `design-reviewer` (3 boundaries enumeradas + cross-ref Escopo↔Tamanho). Default-absorber acionaria reversão silenciosa. O agente precisa reconhecer o conflito + citar ADR-035 + cutucar via `AskUserQuestion` para que override-por-inação se materialize. Sem perspicácia explícita, regressão silenciosa de decisão aprovada — alto-impacto.

A causa raiz: **`code-reviewer` não tem acesso ao registro das decisões já absorvidas pelo design-reviewer pré-commit**. Commit messages só são lidos por humanos via `git log`, não pelo reviewer agent durante invocação por bloco. Override-por-inação prescrito por ADR-035 depende inteiramente do agente coordenador reconhecer o conflito — fragilidade observada.

## Decisão

**Mirror de Decisões absorvidas** entre commit message (preservado per ADR-026) e plan body (introduzido por este ADR), com mecânica runtime de consumo pelos reviewers via mensageiro upstream.

1. **Mirror no plan body.** A seção `## design-reviewer findings absorvidos` do commit message (ADR-026 § Forma) tem **espelho idêntico** no body do plano (seção opcional `## Decisões absorvidas`, após `## Notas operacionais`). Mesmo formato de bullets:

   ```
   - <localização breve>: <correção aplicada> (caminho-único).
   ```

   `/triage` step 5 escreve em ambos os locais (mesma sequência atômica antes do commit). Seção omitida no plan body quando não há findings absorvidos (zero overhead no caso comum, paralelo ao tratamento do commit message).

2. **Consumo runtime por `/run-plan` §2.3 (reader).** Antes da invocação de cada reviewer por bloco, `/run-plan` lê `## Decisões absorvidas` do plan body (se existir) e passa o conteúdo como contexto adicional na prompt do reviewer. Mecanismo paralelo a `**Termos ubíquos tocados:**` ([ADR-021](ADR-021-curadoria-free-read-design-reviewer.md)) — plano é o ponto único de transferência entre alinhamento e execução. Plano sem a seção → nada a passar (skip silente).

3. **Uniform protocol — contexto passa a todos os reviewers.** `/run-plan` §2.3 passa Decisões absorvidas a **todos** os reviewers invocados (code/doc/qa/security), não só ao `code-reviewer`. Custo simétrico (~poucas centenas de tokens); permite extensão futura a outros reviewers só editando o agent def (sem tocar `/run-plan`).

4. **`code-reviewer` cláusula consumer — context-aware via messenger upstream.** `agents/code-reviewer.md` ganha cláusula explícita: "se invocador passa `## Decisões absorvidas` como contexto, trate as estruturas listadas como **out-of-scope da rubrica YAGNI** — design-reviewer aprovou pré-commit + operador absorveu via ADR-026; flagar essas estruturas viola 'override por inação' de ADR-035. Reporte apenas violações em estruturas **fora** da lista absorvida."

5. **Refinamento à ADR-035 § Decisão.** A afirmação de ADR-035 *"code-reviewer mantém rubrica YAGNI universal no diff ... não tem context-aware switch nem free-read de ADRs"* é refinada: introduz-se **categoria nova** "context-aware via messenger upstream" — `code-reviewer` reage a contexto **explicitamente passado pelo invocador** (não a contexto auto-lido). Distinção crítica: "free-read autônomo de ADRs" (`code-reviewer` lê ADRs por conta própria) **continua rejeitado** per ADR-035; "messenger upstream" (caller passa contexto pré-resolvido) é aceito.

Decisão é **plugin-internal** (governa componentes do próprio plugin). Não prescreve comportamento para consumer projects que adotem outros patterns de review.

## Consequências

### Benefícios

- **Elimina dependência da perspicácia do agente** para detectar conflito reviewer-vs-reviewer. Override-por-inação de ADR-035 vira mecânico (`code-reviewer` não flagga em primeiro lugar) em vez de remediativo (agente cita ADR após flag espúria).
- **Greppability dupla.** `git log -p | grep "## design-reviewer"` (commit messages) + greps em planos vivos (plan bodies). Auditoria histórica + estado-corrente.
- **Backward-compat completa.** Planos antigos sem `## Decisões absorvidas` continuam executáveis (reader skip silente). Commits antigos com só commit message permanecem auditáveis.
- **Uniform protocol simplifica extensão futura.** Adicionar cláusula em `doc-reviewer` / `qa-reviewer` / `security-reviewer` (se manifestarem mesmo problema) só edita o agent def — `/run-plan` mensageiro já cobre.

### Trade-offs

- **Redundância textual.** Mesma seção em 2 locais (commit + plan body). Custo editorial; aceito por preservação de greppability histórica (alternativa "move" — descartada — perderia commit message section).
- **Risco de drift entre mirror locations.** Se `/triage` escrever em commit mas pular plan body (bug), agente coordenador depende do código de `/triage` estar correto. Mitigação: edits cirúrgicos do `/triage` step 5 são simétricos — mesmo bloco escreve nos dois locais.
- **Refinamento à ADR-035 sutil.** A categoria "context-aware via messenger upstream" vs "free-read autônomo" exige leitura atenta. Mitigação: cláusula em `code-reviewer` agent def é explícita sobre o critério.

### Limitações

- **Não cobre decisões implícitas de conversa.** Operador respondendo X em `AskUserQuestion` sem registro no plano continua dependendo do agente coordenador. Coberto apenas o que entra no mirror via `/triage` step 5 (que registra absorvidos automáticos do design-reviewer, não decisões conversacionais avulsas).
- **Cláusula só em `code-reviewer` por enquanto.** doc/qa/security recebem contexto mas não têm cláusula explícita de uso. Incremental — adicionar quando/se manifestarem mesmo problema (incidente-driven).

## Alternativas consideradas

### (a) Status quo — só commit message (ADR-026 atual)

Descartado. Incidente observado em ROADMAP item 1 demonstra que mecânica atual depende inteiramente da perspicácia do agente para detectar conflito reviewer-vs-reviewer. Fragilidade alto-impacto que regride silenciosamente decisões aprovadas pelo operador.

### (b) Move da seção (commit → plan body, sem mirror)

Descartado em gap-clarification pelo operador. Perderia greppability histórica via `git log -p`. Refinamento mais agressivo de ADR-026 (deletaria regra atual). Operador escolheu mirror para preservar backward-compat com 14+ commits existentes que já usam o pattern.

### (c) `code-reviewer` ganha free-read autônomo de ADRs

Rejeitado per ADR-035 (alternativa C ao mecanismo original). Antitético a ADR-035 § Decisão "não tem context-aware switch nem free-read de ADRs". Custo de tokens significativo por invocação. Borra fronteira doutrinária entre `code-reviewer` (universal) e `design-reviewer` (free-read de doutrina).

### (d) Pass context só ao `code-reviewer`, não uniform

Descartado em design-reviewer finding F1 do plano `decisoes-absorvidas-plan-body`. Custo simétrico ao uniform-protocol; uniform permite extensão futura a outros reviewers só editando o agent def, sem tocar `/run-plan`.

## Gatilhos de revisão

- **Drift entre mirror locations observado em uso real:** ≥2 ocasiões em que `/triage` escreveu em commit message mas pulou plan body (ou vice-versa). Reabrir mecanismo de write-coupling (transação atômica explícita).
- **Outro reviewer manifesta mesmo problema de incompatibilidade context vs YAGNI:** se doc/qa/security ganharem incidentes análogos ao item 1, estender cláusula consumer (não revisitar mecanismo central).
- **NOTES.md ou outros stores não-role demandam mesma mecânica:** se `/note` (ou store futuro) precisar passar contexto explícito a reviewers, reabrir para padrão geral "messenger upstream" cobrindo múltiplas fontes — ADR-038 cobre só plan body hoje.
- **Decisões conversacionais avulsas demandam mirror análogo:** se operador responder via `AskUserQuestion` mid-execução de `/run-plan` revertendo ou refinando estrutura aprovada em plano pré-existente, esse trace conversacional precisa virar registro consumível por reviewer subsequente. Hoje apenas absorvidos automáticos do `design-reviewer` via `/triage` step 5 alimentam o mirror; decisão conversacional fica fora. Reabrir escopo do mirror se ≥2 incidentes desse tipo materializarem regressão silenciosa análoga à originária (item 1 desta onda).
