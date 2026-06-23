# ADR-069: Gate de verificação de estado real antes de materializar captura originada de entry pré-existente do NOTES.md

**Data:** 2026-06-23
**Status:** Proposto

**Próxima revisão:** 2026-12-23
**Cadência:** trimestral
**Critério de erosão auditável:** ≥2 falsos-negativos observados (probe do gate pulou filing de pendência que ainda era real, detectados a jusante no `/next` ou por re-abertura manual) OR o shared procedure `verify-state-before-materialize.md` registrar override do default-conservador (passar a filar-sempre / probar-sempre) em qualquer SKILL consumidora OR taxa de ramo-indeterminado (entry NOTES.md sem artefato concreto citável → default-conservador filar) >50% das capturas NOTES-sourced em ≥3 sessões — gate majoritariamente no-op, reavaliar custo/escopo.

## Origem

- **Decisão base:** [ADR-064](ADR-064-gate-com-executor-validacao-2-sites.md) (gate-com-executor-validacao — "verificar/executar antes de cerimônia" como shared procedure cross-skill) — este ADR estende o princípio do gate de validação para o caminho de captura/filing.
- **Incidente:** Sessão `kl-score` 2026-06-23 criou 2 issues forge a partir de entries do `.claude/local/NOTES.md` que já estavam resolvidas (#4 cross-refs upstream já materializados; #5 reports já commitados) — ambas fechadas no `/next` seguinte sem nenhuma linha de código. Trabalho-fantasma: issue criada + cutucada + close.

## Contexto

`/session-audit` (tipo `captura_backlog`) e `/triage` (filing de linha de backlog) tratam o `.claude/local/NOTES.md` como contexto de input e materializam gaps **sem re-verificar** se a pendência descrita ainda é real. O store de handoff cross-sessão ([ADR-054](ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (b)) decai mais rápido que o ciclo de trabalho — entries afirmam "pendente" depois do trabalho ter sido feito em outra sessão ou outro repo.

Resultado empírico (incidente kl-score): captura materializada de entry stale vira issue-fantasma. `/next` já é a rede de segurança a jusante (verifica evidência e fecha), mas o custo do trabalho-fantasma (criação remota + cutucada + close) se paga **no momento do filing**, não depois.

A dor é específica de capturas cuja **origem é uma entry pré-existente do NOTES.md** (store que persiste entre sessões e decai). Substância gerada na própria sessão corrente é fresca por construção — não tem o risco de staleness, não precisa do probe.

## Decisão

Quando uma captura — gap `captura_backlog` em `/session-audit` OU linha de backlog em `/triage` — **origina de uma entry pré-existente do `.claude/local/NOTES.md`** (não de substância gerada na sessão corrente), probar o artefato concreto que a entry cita **antes de filar**:

- **Probe por tipo de artefato citado:** `git ls-files <path>` / `git log --grep` / `grep` em arquivo / `gh issue view` conforme o que a entry referencia (commit, arquivo, cross-ref, issue).
- **Já resolvido** (probe confirma que o trabalho foi feito) → **registrar a baixa via append** de nova entry no NOTES.md (`Resolvido <data>: <evidência> — refere entry de <data-da-original>`, mecânica idêntica ao `captura_notes` de `session-audit`) e **pular o filing**. Sem criar issue/linha. Append preserva o invariante append-only de [ADR-054](ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (a/b) — a entry stale original permanece auditável; re-disparo do probe sobre ela em sessão futura confirma resolvido a custo de re-probe barato, não issue-fantasma (a entry de baixa também sinaliza "já tratado" ao scan).
- **Ainda pendente** (probe não encontra evidência de conclusão) → filing normal segue.
- **Indeterminado** (entry sem artefato concreto citável, ou probe inconclusivo) → cláusula default-conservadora: filar normalmente (preserva o comportamento atual; `/next` continua sendo a rede a jusante).

**Mecânica compartilhada cross-skill** num shared procedure (`docs/procedures/verify-state-before-materialize.md`, paralelo editorial a `gate-com-executor-validacao.md` de ADR-064 e `forge-auto-detect.md`): heurística de probe por tipo + cláusula de baixa-na-nota + cláusula default-conservadora vivem no procedure; `session-audit/SKILL.md` e `triage/SKILL.md` referenciam, não duplicam.

**Escopo restrito a origem NOTES.md.** O gate só dispara quando a `citação_transcript` (session-audit) ou o material de gap-clarification (triage step 1) aponta para uma entry pré-existente do NOTES.md. Substância gerada na sessão corrente fila direto, sem probe.

**Fronteira com [ADR-058](ADR-058-role-backlog-aceitar-forge.md) § (e) e #145** (filar direto quando substância cristalizada): ortogonal. ADR-058/#145 decidem **o canal** (filar via forge vs deferir a /triage). Este ADR adiciona um **gate de verificação antes do filing**, independente do canal — aplica-se a captura para arquivo, forge, ou deferida.

## Auto-aplicação (ADR-034)

Varredura das 5 condições:

- **Cond 1 (estrutural sem ancestral):** não — ancestral direto é ADR-064 (gate-com-executor) + ADR-054 (NOTES.md store).
- **Cond 2 (substitui/inverte ancestral):** não — ADR-064 permanece vigente para o gate de validação; ADR-069 adiciona eixo paralelo, não revoga.
- **Cond 3 (restrição externa):** não.
- **Cond 4 (categoria nova) — PESO PRIMÁRIO:** sim — introduz "gate de verificação de staleness de origem NOTES.md" como categoria distinta do gate-de-validação de ADR-064, materializada num shared procedure novo (`verify-state-before-materialize.md`) wired cross-skill. A natureza ("probe de artefato citado antes de filar") difere de "executar cenário de validação" o suficiente para ser eixo conceitual paralelo, não refinamento do mesmo.
- **Cond 5 (sucessor parcial) — reforço:** sim — estende o princípio "verificar/executar antes de cerimônia" de ADR-064 ao caminho de captura/filing, sem revogá-lo.

Peso primário cond 4 (categoria nova: shared procedure + gate de staleness) + reforço cond 5 (linhagem ADR-064) → ADR justificado.

## Consequências

### Benefícios

- Elimina trabalho-fantasma no momento do filing (issue criada + cutucada + close a jusante) para capturas de entries NOTES.md stale.
- Registra a baixa via append — o store de handoff ganha o marcador de resolução visível ao scan futuro (entry de baixa sinaliza "já tratado"; re-disparo do probe sobre a entry stale original confirma resolvido a custo de re-probe, sem issue-fantasma).
- Reforça a doutrina "verificar estado real antes de agir" (ADR-064) no caminho de captura, fechando o complemento do gate de validação.

### Trade-offs

- Custo de probe por captura NOTES.md-sourced (1 `git`/`grep`/`gh` por entry). Aceitável: probe mecânico barato vs criação remota + close.
- Default-conservador (indeterminado → filar) preserva a rede `/next` a jusante — o gate reduz, não elimina, issues-fantasma.

### Limitações

- Não cobre capturas cuja origem não é citável a um artefato concreto (entry NOTES.md vaga). Essas caem no default-conservador (filar).
- Side-effects já executados (issue já criada antes do gate) ficam fora — o gate é preventivo no filing, não corretivo.
- **Ordem de composição com #145** (filar direto no forge quando substância cristalizada — proposta ainda não-aceita): se #145 for implementado, o gate de ADR-069 precisa rodar **antes** do filing direto, senão #145 cria a issue-fantasma que este ADR previne (exatamente o incidente kl-score). Gate precede canal — forward-compat registrado.

## Alternativas consideradas

### Mutação inline da entry stale (rebatida)

Anotar a baixa **na própria entry** original do NOTES.md (em vez de append de nova entry). Beneficio: corta o re-disparo do probe na fonte (entry resolvida não re-aparece no scan futuro). Rebatida: seria a **primeira mutação não-append** do NOTES.md no toolkit, abrindo exceção ao invariante append-only de [ADR-054](ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (a/b) — exigiria argumentar que o append-only é propriedade da skill `/note`, não do arquivo. O append (decisão adotada) preserva o invariante sem exceção, mantém o histórico auditável, e é a mecânica que `captura_notes` (`session-audit`) já usa; o custo (re-probe barato da entry stale em sessão futura) é o mesmo tipo de erro barato que o default-conservador já aceita absorver. Trade-off resolvido a favor do append.

## Gatilhos de revisão

- Probe gerar falso-negativo (pular filing de pendência ainda real) ≥1 vez observada → reavaliar a heurística de "já resolvido".
- Custo de probe percebido como cerimônia (operador reporta overhead sem ghost-catch) em ≥2 sessões → reavaliar o escopo NOTES.md-only.
