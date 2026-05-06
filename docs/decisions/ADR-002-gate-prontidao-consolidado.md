# ADR-002: Gate de prontidão consolidado em /run-plan

**Data:** 2026-05-06
**Status:** Proposto

## Origem

- **Investigação:** Revisão arquitetural pós-v1.20.0 contou até 4 enums de cutucada em cascata na fase pré-loop do `/run-plan` (pré-condição 2c, passo 1.2 `.worktreeinclude`, passo 1.2 credencial, passo 2 sanity check de escopo). Cada interrupção tira o foco; juntas, fragmentam a entrada num batch onde o operador já decidiu prosseguir. Skill é a mais invocada do plugin — ergonomia da fase de setup tem peso desproporcional.

## Contexto

`/run-plan` distingue dois tipos de finding na fase pré-loop:

- **Bloqueios** — invariantes do estado git/setup quebradas (plano sujo, baseline vermelho, worktree órfã). Skill **para**, não cutuca; operador resolve antes de prosseguir.
- **Cutucadas** — qualidade-de-mudança que merece atenção mas não impede progresso (alinhamento dirty, gitignored não replicado, escopo divergente do plano). Skill **avisa e segue se autorizada**.

Hoje as cutucadas são fragmentadas em 4 enums separados, cada um disparado em momento diferente do fluxo (pré-condição 2c, passo 1.2, passo 2). Isso tem dois custos:

- **Foco fragmentado**: operador é interrompido até 4 vezes em cascata, cada vez mudando contexto cognitivo.
- **Detecção tardia**: warnings de passo 2 só aparecem após worktree criada e dependências sincronizadas — tarde para decidir pausar e voltar ao alinhamento.

A motivação coincide com o princípio "Não perguntar por valor único derivado" registrado em `docs/philosophy.md` → "Convenção de pergunta ao operador": consolidar gates derivados da mesma decisão num único ponto de visibilidade.

## Decisão

**Consolidar todas as cutucadas pré-loop num gate único de prontidão**, executado **antes da worktree ser criada**.

Mecânica:

1. **Detectar todos os warnings cedo** (antes do `git worktree add`):
   - Alterações uncommitted em arquivos de alinhamento (`backlog`, `ubiquitous_language`, `design_notes`, `decisions_dir`).
   - `.worktreeinclude` ausente + gitignored aparente em uso na raiz do repo.
   - Plano com `## Verificação manual` + credencial gitignored típica não coberta pelo `.worktreeinclude` (quando existe).
   - Superfície externa em `## Contexto` ou `## Resumo da mudança` ausente em `## Arquivos a alterar`.

2. **Apresentar em prosa**: listar todos os warnings detectados de uma vez, citando o que cada um significa e a ação sugerida ("commitar antes de prosseguir", "criar `.worktreeinclude`", "ajustar `## Arquivos a alterar`").

3. **Gate único enum binário** (`AskUserQuestion`, header `Prontidão`):
   - **`Prosseguir mesmo assim`** — skill segue, warnings registrados como avisos. Não bloqueia a worktree.
   - **`Pausar para corrigir manualmente`** — skill encerra reportando os warnings; operador resolve fora do skill e relança `/run-plan`.

4. **Sem fix in-place**: skill não aplica correções automaticamente (não cria `.worktreeinclude`, não replica credencial, não commita uncommitted). Manter superfície da skill enxuta — fix in-place exigiria mapping warning→ação que cresce com cada warning novo.

**Casos especiais preservados**:

- **Bloqueios** (plano sujo, baseline vermelho, worktree órfã) ficam fora do gate. Continuam parando in situ com captura imediata em `## Próximos` do backlog.
- **Sem warnings** → gate não dispara. Skill segue direto para criação da worktree.
- **Operador escolhe `Prosseguir`** mas algum warning era de superfície faltante (escopo) → registrar como entrada do passo 4.5 (Captura automática de imprevistos) sob "Superfície faltante" — mantém o trilho atual.

## Consequências

### Benefícios

- **−3 a −4 interrupções** em cascata em runs onde múltiplos warnings disparam.
- **Detecção antecipada**: operador vê warnings de escopo antes de pagar o custo de criar worktree e sincronizar dependências.
- **Visibilidade consolidada**: lista única em prosa torna fácil decidir "pausar e revisar plano" vs "prosseguir, capturei mentalmente".
- **Skill mais simples**: 4 enums viram 1; lógica de despacho centralizada.

### Trade-offs

- **Sem fix in-place**: operador precisa relançar `/run-plan` após corrigir manualmente. Mitigação: o caminho rico (multiSelect com ações) foi avaliado e descartado por aumentar a superfície da skill (mapping warning→ação cresce com cada warning novo); relançar é barato.
- **Plano sem warnings ainda paga uma branch a mais no fluxo**: `if any(warnings): ask_gate else: proceed`. Custo trivial.

### Limitações

- **Bloqueios genuínos** (estado git/setup) continuam fora do gate. Fragmentação restante é justificada — bloqueio exige resolução pré-skill, gate consolidaria itens de natureza diferente.
- ADR não promete que todo warning futuro caiba no gate. Critério da inclusão: warning é (a) detectável antes da worktree e (b) não-bloqueante. Warnings que violem qualquer condição vão para o trilho separado (bloqueio in situ ou captura deferida no passo 4.5).

## Alternativas consideradas

- **(b) Caminho rico — multi-select com fix in-place**: cada warning é um item selecionável; selecionar = aplicar correção (skill replica credencial, cria `.worktreeinclude`, etc.). Mais ergonômico mas adiciona lógica de mapping ação-por-item dentro da skill. Cada warning futuro precisaria especificar "como corrigir automaticamente". YAGNI — relançar `/run-plan` após fix manual é trivial e não há demanda observada.
- **Manter cascata atual**: fragmentação reconhecida como custo de UX já durante a revisão arquitetural; status quo descartado.
- **Detectar warnings depois da worktree**: rejeitado — sanity de escopo já é detectável antes (lê `## Contexto` e `## Resumo da mudança` do plano), e detectar antes evita custo de setup quando o operador decide pausar.

## Gatilhos de revisão

- Pain reportado em "ter que relançar `/run-plan` toda vez" → reabrir para considerar fix in-place seletivo (apenas para warnings de baixa complexidade de correção).
- Surge um 5º+ warning na fase pré-loop com natureza distinta dos atuais → reavaliar se cabe no gate ou em trilho separado.
- Operador frequentemente escolhe `Pausar` apenas para um único warning específico → considerar destacar esse warning em gate dedicado (revisar fragmentação caso a caso).
