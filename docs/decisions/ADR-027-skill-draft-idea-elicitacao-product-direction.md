# ADR-027: Skill /draft-idea para elicitação estruturada de product_direction

**Data:** 2026-05-13
**Status:** Proposto

## Origem

- **Investigação:** <conversa que originou este ADR — operador propôs caminho upstream de `/triage` para casos de ideia vaga, com IDEA.md como output>
- **Decisão base:** [ADR-008](ADR-008-skills-geradoras-stack-agnosticas.md) (skill geradora cujo output é produto, não código → opera no caminho stack-agnóstico que ADR-008 carva para artefatos não-código; sem sub-blocos por stack).
- **Decisão base:** [ADR-023](ADR-023-criterio-mecanico-disable-model-invocation-skills.md) (skill nova deve declarar `disable-model-invocation` explicitamente com critério mecânico; perfil esperado: blast radius local + sem autoinvocação cross-turn → `false`).

## Contexto

Hoje o toolkit cobre o eixo "alinhar intenção concreta → registrar artefato" via `/triage`. O passo 2 de `/triage` explicitamente diz "não fazer entrevista exaustiva" e "perguntar só o que for bloqueante" — opera sobre intenção já formada, não sobre ideação aberta. Operador que chega com ideia vaga (sem problema bem-definido, sem persona clara, sem critério de sucesso) não tem onde aterrissar: o caminho disponível é conversa livre com Claude até virar coisa concreta, sem estrutura nem artefato persistido.

O papel `product_direction` (canonical `IDEA.md`) é declarado **informational** em todas as 7 skills atuais por ADR-005. Nenhuma skill **produz** o artefato — só consomem (ou silenciam quando ausente). Isso deixa um gap: o artefato existe na doutrina, mas o caminho de criação assistida não. Operador escreve IDEA.md à mão ou não escreve.

## Decisão

Adicionar ao toolkit a skill `/draft-idea`, geradora de `IDEA.md` (papel `product_direction`) via elicitação estruturada multi-turn.

- **Naming:** `/draft-idea` — convenção `<verb>-<artifact>` (per `CLAUDE.md` → "Plugin component naming"), alinhada ao filename canonical `IDEA.md` (concept-facing, consistente com `/new-adr` ↔ `ADR-NNN.md` e `/run-plan` ↔ `<slug>.md`).
- **Escopo:** elicitação estruturada multi-turn cobrindo problema, persona/usuário, restrições, critérios de sucesso e alternativas descartadas. Skeleton-only é rejeitado (ver § Alternativas).
- **Modo de operação:** probe canonical + dual.
  - `IDEA.md` ausente → modo **one-shot full** (skill conduz interview completo do zero e grava o artefato).
  - `IDEA.md` presente → modo **update seção-a-seção** via enum (`AskUserQuestion` lista as seções; operador escolhe quais revisar; skill reconduz elicitação só nessas).
- **Fronteira com `/triage`:** upstream. `/draft-idea` opera quando intenção ainda é vaga (sem problema bem-definido); `/triage` opera quando intenção já é concreta. Skill **sugere `/triage` como próximo passo** ao concluir (registro de continuidade do pipeline mental, paralelo à cutucada de `/init-config` em ADR-017).
- **Stack-agnóstica:** sem auto-detection por marker, sem sub-blocos por stack — `IDEA.md` é produto, não código (per ADR-008, caminho dos artefatos não-código).
- **`disable-model-invocation: false`** esperado per critério mecânico de ADR-023 (blast radius local; pushes/PRs gateados upstream pelo operador; sem autoinvocação cross-turn).

## Consequências

### Benefícios

- Fecha o gap entre o papel `product_direction` declarado na role contract e a ausência de caminho de criação assistida (incoerência interna atual do toolkit).
- Continuidade explícita upstream → downstream (`/draft-idea` → `/triage` → `/run-plan`) materializa o pipeline para operador novo.
- Estrutura de elicitação força o operador através de bifurcações que viram dívida silenciosa quando ideação fica em chat livre (persona ausente, critério de sucesso implícito, alternativa descartada sem rastro).

### Trade-offs

- +1 skill no toolkit (manutenção, descoberta, espaço cognitivo no entry surface). Mitigação: skill simétrica a `/new-adr` (template já internalizado pelo operador).
- Modo update via enum exige operador decidir seções a revisar — pode parecer cerimonial para refinamentos pequenos. Mitigação: opção "Other" no enum permite override pra prosa livre.
- "Sugerir `/triage`" na saída acrescenta uma linha ao relatório final; risco de ruído baixo dado que é o próximo passo natural.

### Limitações

- Skill assume operador minimamente capaz de articular problema/persona — não é Q&A guiado para non-technical stakeholder; é estruturação para quem já tem intuição.
- Modo update opera seção-a-seção; não detecta inconsistências cross-seção (ex.: critério de sucesso que não bate com persona declarada). Operador é responsável pela coerência global.

## Alternativas consideradas

### Estender `/triage` para aceitar input vago

`/triage` detectaria vaguidade no input e ofereceria criar IDEA.md inline antes de prosseguir com clarificação de intenção, evitando adicionar nova skill.

**Motivo de descarte:**

- (a) O passo 2 de `/triage` SKILL.md declara explicitamente *"não fazer entrevista exaustiva"* e *"perguntar só o que for bloqueante"* — sobrecarregar com elicitação multi-turn quebraria essa invariante semântica.
- (b) A bifurcação "ideia vaga vs intenção formada" tem fronteira nítida que justifica nomes distintos no entry surface — operador escolhe a skill alinhada ao seu estado de maturação, em vez de uma skill com dupla missão decidir internamente o modo.
- (c) Pureza semântica prevalece sobre churn (preferência editorial registrada): o custo de adicionar uma skill é menor que o custo cognitivo de uma skill que mistura "descobrir" e "alinhar". A doutrina favorece fronteira nítida mesmo a custo de superfície.

### Skeleton-only (sem elicitação estruturada)

Skill cria `IDEA.md` com seções vazias (problema, persona, restrições, critérios, alternativas) e devolve controle ao operador, sem conduzir interview multi-turn. Simétrico ao comportamento de `/new-adr` (cria placeholder, operador preenche).

**Motivo de descarte:** o valor real da skill está na **estrutura de elicitação** — perguntas dirigidas que forçam o operador a articular bifurcações silenciosas. Skeleton-only seria wrapper fino sobre `touch IDEA.md` + chat livre, sem ganho semântico sobre "abrir o arquivo no editor e escrever". A simetria com `/new-adr` é superficial: ADR registra uma decisão já tomada (operador chega com a decisão); IDEA.md captura uma direção que pode ainda nem existir (operador chega com névoa).

### Não cobrir elicitação (deixar discovery fora do plugin)

Manter o status quo: `product_direction` é informational em todas as skills, `IDEA.md` segue write-only do operador sem caminho assistido. Argumento de descarte do alternativa: discovery seria scope creep do toolkit de engenharia.

**Motivo de descarte:** o papel `product_direction` está declarado na role contract do toolkit há 26 ADRs sem caminho de criação — gap entre "declarado como role" e "sem produtor assistido" é **incoerência interna**, não expansão de escopo. O toolkit já carrega o conceito; cobrir o caminho de criação fecha o ciclo, não amplia o domínio. Argumento de scope creep só se sustentaria se o papel não estivesse na doutrina; está.

## Gatilhos de revisão

- Modo update seção-a-seção via enum mostra-se cerimonial na prática (operador escapa repetidamente para "Other" prosa livre) — reabrir decisão de modo de operação.
- Skill criada mas operadores usam diretamente chat livre + `Write` para `IDEA.md` sem invocar `/draft-idea` em >50% dos casos detectáveis — sinal de que a estrutura de elicitação não está agregando valor; reabrir escopo (skeleton-only? remover?).
- Pipeline `/draft-idea` → `/triage` mostra-se ruidoso (operador raramente segue a sugestão porque já estava encadeando manualmente) — reabrir decisão de "sugerir próximo passo".
