# Plano — Captura automática `/run-plan` §3.5 via TaskCreate com marker

## Contexto

ROADMAP item 8 (commit `25d0daf`). Resolve fragilidade latente — não observada nesta onda, mas estruturalmente presente. Spec atual de `/run-plan` §3.5 diz "agente acumula gatilhos e materializa no gate final" **sem mecanismo de tracking** — depende de lista mental do agente. Em `/run-plan` longo (≥3 blocos com triggers reais), risco de esquecer parte da lista entre passo 2 e §3.5. Mesma classe de fragilidade que itens 6 (reviewer-vs-reviewer silent regression) e 7 (stale-view silent regression) endereçaram — agente mantém state mentalmente em fluxo multi-passo sem persistência.

**Mecanismo:** cada captura emergente em `/run-plan` dispara `TaskCreate` com prefixo marker no subject:

- `[capture:validacao] <linha>` — destino `## Pendências de validação` no plano corrente.
- `[capture:backlog] <linha>` — destino `## Próximos` do papel `backlog`.

Cobertura unificada das **3 superfícies emissoras** (F3 absorved): fase pré-loop (warnings per ADR-002: alinhamento dirty é só aviso e não captura; `.worktreeinclude` ausente / credencial não coberta / escopo divergente / cobertura ausente emitem TaskCreate); passo 2 do loop (falha contornada / finding fora-do-escopo / hook bloqueando); passo 3.2 validação manual (divergência do plano / bug colateral). Todas as 3 superfícies passam a usar mesma mecânica de marker — antes do edit, as 3 vinham para a mesma "lista mental" sem tracking; pós-edit, as 3 emitem TaskCreate. §3.5 materialização lê `TaskList` filtrada por marker (`[capture:*]`) para gerar as escritas.

**Lifecycle pending → completed (skipping `in_progress`).** Diverge intencionalmente do triplo `pending → in_progress → completed` de ADR-010. Razão semântica: captures são **buffer de pendências a materializar**, não cursor de execução — `in_progress` seria não-semântico (não há "executando agora" entre criação no trigger e materialização batch em §3.5). Justificativa central vive no novo ADR-039 (criado neste plano), que codifica a categoria "Task tool como state-keeping" distinta da "progress display" de ADR-010.

**Classificação editorial — novo ADR-039 sucessor parcial de ADR-010** (F1 absorbed via cutucada — operador escolheu novo ADR sobre adendo). Razões confirmadas pelo design-reviewer:

- ADR-010 § Escopo (skills com ≥3 passos sequenciais, instrumentação progresso) **não cobre** state-keeping cross-passo — categoria conceitual nova (Task como queue persistente vs. Task como cursor de execução). ADR-034 Condição (4) "introduz categoria nova" aplica.
- Lifecycle `pending → completed` skipping `in_progress` **diverge** de ADR-010 § Mecânica triplo — prescrição mecânica nova, não anotação descritiva. ADR-034 Condição (4) "caráter explicativo" do lado adendo **falha**.
- ADR-034 Condição (5) "sucessor parcial — estende ADR Aceito sem revogar" aplica. Precedente ADR-038 (mesma onda, item 6) escolheu novo ADR via mesma condição.
- Memory `feedback_adr_threshold_doctrine` ("refinar/inverter critério documentado → default ADR") milita por ADR.

ADR-039 § Origem cita ADR-010 (base estendida) + ROADMAP item 8 (investigação) + ADR-034 (classificação editorial). § Decisão estabelece (a) Task tool serve também state-keeping em fluxo longo; (b) marker convention `[capture:<tipo>]`; (c) lifecycle 2-estados `pending → completed` para state-keeping; (d) `/run-plan` §3.5 é primeiro caso de uso.

**ADRs candidatos:** [ADR-010](../decisions/ADR-010-instrumentacao-progresso-skills-multi-passo.md) (base estendida — sucessor parcial), [ADR-002](../decisions/ADR-002-eliminar-gates-pre-loop.md) (warnings pré-loop unificados sob mesmo mecanismo), [ADR-034](../decisions/ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) (justifica novo ADR via condições 4+5), [ADR-038](../decisions/ADR-038-mirror-decisoes-absorvidas-runtime.md) (precedente recente de sucessor parcial via mesmo critério).

**Linha do backlog:** plugin: captura automática /run-plan §3.5 via TaskCreate com marker

## Resumo da mudança

2 edits coordenados — doctrine first (novo ADR) + mechanism (SKILL):

1. **Criar `docs/decisions/ADR-039-task-tool-state-keeping-fluxo-longo.md`** — sucessor parcial de ADR-010. § Origem cita ADR-010 base + ROADMAP item 8 + ADR-034 condições 4+5 + precedente ADR-038. § Decisão estabelece: Task tool serve também state-keeping em fluxo longo (categoria nova vs progress display de ADR-010); marker convention `[capture:<tipo>]` no subject; lifecycle 2-estados `pending → completed` (skip `in_progress` justificado por semântica de queue não-cursor); `/run-plan` §3.5 captura automática como primeiro caso de uso (canonical example). § Consequências cobre backward-compat com ADR-010 progress instrumentation.

2. **`skills/run-plan/SKILL.md`** — editar 3 locais (cobertura unificada per F3):
   - **Detecção de warnings pré-loop** (tabela existente): cada warning de Backlog/Validação emite `TaskCreate` com marker apropriado (aviso informativo de alinhamento dirty continua sem TaskCreate — não alimenta lista per spec atual).
   - **"Captura automática" prelúdio do passo 2 loop**: substituir descrição "agente acumula gatilhos" por "cada captura emergente cria `TaskCreate` com marker `[capture:validacao]` ou `[capture:backlog]` no subject; line text como description. Lifecycle pending até materialização em §3.5 (per [ADR-039](../../docs/decisions/ADR-039-task-tool-state-keeping-fluxo-longo.md))."
   - **§3.5 "Captura automática de imprevistos"** (gate final): substituir "Materializar a lista mantida desde o passo 2" por mecânica concreta — ler `TaskList` filtrada por marker `[capture:*]`; cada Task pendente vira escrita no destino correto (validação em `## Pendências de validação` do plano / backlog em `## Próximos` do role); marcar Tasks `completed` após escrita. Materialização vazia (TaskList sem matches) → skip silente.

Backward-compat: pré-edit, captura ficava mental. Pós-edit, captura é `TaskCreate`. Nenhum plano antigo em execução é afetado (cada `/run-plan` é invocação isolada).

## Arquivos a alterar

### Bloco 1 — docs/decisions/ADR-039 novo (sucessor parcial ADR-010) {reviewer: doc}

- `docs/decisions/ADR-039-task-tool-state-keeping-fluxo-longo.md`: criar arquivo novo via Write (mecânica simplificada vs Skill /new-adr — substância idêntica, paralelo ao Bloco 2 do plano item 6). Estrutura: # Título + Data + Status Proposto + § Origem (ADR-010 base + ROADMAP item 8 + ADR-034 4+5 + ADR-038 precedente) + § Contexto (gap state-keeping não-coberto por ADR-010 § Escopo) + § Decisão (4 cláusulas: state-keeping use; marker convention; lifecycle 2-estados; /run-plan §3.5 primeiro caso) + § Consequências (benefícios + trade-offs + limitações) + § Alternativas (adendo descartado per F1; lista mental status quo descartada por fragilidade do item 8) + § Gatilhos de revisão. Manual `@design-reviewer` invocado para review pré-retorno (simula /new-adr step 5).

### Bloco 2 — skills/run-plan/SKILL.md captura unificada via TaskCreate {reviewer: code}

- `skills/run-plan/SKILL.md`: 3 edits:
  - Tabela "Detecção de warnings pré-loop": adicionar nota ao final da tabela ou na coluna Trilho indicando que cada classificação Backlog/Validação emite `TaskCreate` com marker apropriado (per ADR-039); alinhamento dirty (aviso informativo) continua sem TaskCreate.
  - "Captura automática" (prelúdio passo 2 loop): substituir descrição da lista mental pela emissão de TaskCreate com marker `[capture:validacao]` / `[capture:backlog]` per ADR-039.
  - §3.5 "Captura automática de imprevistos" (gate final): substituir "Materializar a lista mantida desde o passo 2" por mecânica concreta de leitura `TaskList` filtrada por marker → escritas por tipo → `completed` post-write; skip silente se TaskList vazia.

## Verificação end-to-end

- `ls docs/decisions/ADR-039-*.md` retorna 1 arquivo.
- `grep -n "state-keeping\|state.keeping" docs/decisions/ADR-039-*.md` retorna match em § Decisão.
- `grep -nE "TaskCreate.*\[capture|\[capture:" skills/run-plan/SKILL.md` retorna ≥3 matches (pré-loop tabela + passo 2 prelúdio + §3.5).
- `grep -n "lista mental\|acumula gatilhos" skills/run-plan/SKILL.md` retorna **vazio** (substituído pelo mecanismo TaskCreate).
- `grep -n "ADR-039" skills/run-plan/SKILL.md` retorna ≥1 match (cross-ref doutrinal).
- Inspeção textual: ADR-039 § Origem cita ADR-010 + ADR-034 + ADR-038; SKILL.md cross-refs ADR-039 nos 3 locais editados.
- Backward-compat: ADR-010 não tocado (sucessor parcial não revoga; § Origem do ADR-039 reconhece ADR-010 como base preservada).

## Pendências de validação

- Próxima execução `/run-plan` que dispare captura emergente (passo 2 falha contornada, passo 3.2 divergência, ou warning pré-loop ADR-002) deve emitir `TaskCreate` com marker `[capture:*]` no subject e ser materializada em §3.5 (lista atualizada no plano ou no backlog). Verificar visualmente na `TaskList` da sessão — captures aparecem como Tasks pending até §3.5 marcá-las `completed`.

## Notas operacionais

- Plano 2 blocos, ordem editorial: doutrina primeiro (ADR-039 sucessor parcial), depois mecanismo (SKILL.md edits). Bloco 2 referencia ADR-039 do Bloco 1 — fora de ordem causaria forward-ref.
- design-reviewer dispatcha automaticamente pré-commit (ADR-011); free-read prioriza ADRs candidatos em `## Contexto`. Já adjudicou que classificação correta é novo ADR (F1 cutucada absorbed).
- Manual `@design-reviewer` invocado no Bloco 1 (simula /new-adr step 5 pré-retorno); doc-reviewer no §2.3 do /run-plan como drift check pós-criação.
- Bloco 2 reviewer: code-reviewer (operacional). Os 3 edits no SKILL.md são simétricos (mesma adoção do mecanismo TaskCreate em 3 superfícies); pattern já documentado em ADR-039.

## Decisões absorvidas

- `## Contexto` (cobertura unificada 3 superfícies): rebatida cobertura parcial original (só passo 2 + 3.2) per F3 — warnings pré-loop ADR-002 também emitem TaskCreate; mecanismo unificado em todas as 3 superfícies emissoras de captura (single-path).
- `## Pendências de validação` (nova seção): adicionada per F4 — runtime se valida em próxima execução /run-plan com captura emergente real; rastreado no plano per convenção ADR-002 (single-path).
- `## Contexto` lifecycle justificativa: justificativa semântica explicitada (state-keeping ≠ cursor de execução; `in_progress` não-semântico) — F2 absorvido via reclassificação para novo ADR (F1) que codifica a divergência como decisão central (single-path).
