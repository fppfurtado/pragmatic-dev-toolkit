# Plano — Embedar `## Decisões absorvidas` no body do plano para code-reviewer consumir

## Contexto

ROADMAP item 6 (commit `ec9f248`). Resolve fragilidade observada no item 1 (sessão de 2026-05-26): `code-reviewer` mid-execução flaggou estrutura que `design-reviewer` pré-commit havia aprovado (3 boundaries enumeradas + cross-ref Escopo↔Tamanho). Sem perspicácia do agente para citar ADR-035 e cutucar via `AskUserQuestion`, o default-absorber teria revertido silenciosamente a decisão aprovada pelo operador.

[ADR-035](../decisions/ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) prescreve "override por inação" mas só funciona se o agente reconhecer o conflito. Mecânica atual: findings absorvidos vivem **só no commit message** do plano ([ADR-026](../decisions/ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md) § Forma); `code-reviewer` não lê commit messages, só o diff — gap de informação estrutural alto-impacto (regressão silenciosa de decisão aprovada).

**Mecanismo (opção B confirmada; mirror confirmado em gap-clarification):** plano carrega `## Decisões absorvidas` em **ambos** locais — commit message (preserva ADR-026 vigente, greppability via `git log -p`) + body do plano (nova seção opcional, consumível por `/run-plan` em runtime). `/run-plan` lê do plan body e passa como contexto na invocação de cada reviewer por bloco (paralelo a `**Termos ubíquos tocados:**` da [ADR-021](../decisions/ADR-021-curadoria-free-read-design-reviewer.md)). `code-reviewer` agent def ganha cláusula explícita: "se invocador passa Decisões absorvidas, trate as estruturas listadas como out-of-scope da rubrica YAGNI per ADR-035 override-by-inaction explícito".

**Refinamento doutrinário toca 2 ADRs vigentes** (confirmado em design-reviewer findings 2+3, absorbed via cutucada — operador escolheu novo ADR sucessor parcial):

- [ADR-026](../decisions/ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md) § Forma é estendida (mirror no plan body além do commit message).
- [ADR-035](../decisions/ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) § Decisão (subseção "Escopo do princípio para consumidores preservado") afirma literalmente *"code-reviewer mantém rubrica YAGNI universal no diff ... não tem context-aware switch nem free-read de ADRs"*. Bloco 4 deste plano introduz exatamente um context-aware switch (via mensageiro upstream, não free-read autônomo) — refinamento doutrinário que toca essa subseção.

[ADR-034](../decisions/ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) § "Novo ADR quando ≥1 das condições aplica" 5ª condição ("sucessor parcial — estende, refina ou condiciona ADR Aceito sem revogar") aplica → **novo ADR-038** sucessor parcial, cobrindo a extensão de ADR-026 + refinamento de ADR-035 num único artefato (pattern paralelo a ADR-029→ADR-017, ADR-025→ADR-005, ADR-030→ADR-005).

**Escopo do mensageiro** (após F1 absorvido): `/run-plan` passa Decisões absorvidas como contexto a **todos** os reviewers (uniform protocol — cheap, ~poucas centenas de tokens). Cláusula de uso explícita só em `code-reviewer` (incidente observado). Alternativa simétrica considerada — "passar só ao `code-reviewer`" — descartada porque custo é simétrico ao uniform-protocol e este último permite extensão futura ao doc/qa/security só editando o agent def (sem tocar `/run-plan`).

**ADRs candidatos:** [ADR-026](../decisions/ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md) (base estendida), [ADR-035](../decisions/ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) (subseção code-reviewer refinada), [ADR-021](../decisions/ADR-021-curadoria-free-read-design-reviewer.md) (pattern paralelo de mensageiro), [ADR-034](../decisions/ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) (justifica novo ADR sucessor parcial via 5ª condição), [ADR-011](../decisions/ADR-011-wiring-design-reviewer-automatico.md) (wiring de design-reviewer adjacente).

**Linha do backlog:** plugin: embedar Decisões absorvidas no body do plano para code-reviewer consumir

## Resumo da mudança

5 edits coordenados, organizados em **ordem editorial** (cada commit deixa sistema funcionalmente consistente; writer é o último a ativar mecanismo completo):

1. **`templates/plan.md`** — adicionar seção opcional `## Decisões absorvidas` (após `## Notas operacionais` existente). Comentário-guia descreve origem (mirror do bloco `## design-reviewer findings absorvidos` do commit message, per ADR-026 + ADR-038) e formato esperado.

2. **`/new-adr` ADR-038** — sucessor parcial de ADR-026 + refina § Decisão de ADR-035 sobre `code-reviewer`. Doutrina central de ADR-026 (default invertido + 3 condições + cláusula default-conservadora) preservada; estende **Forma do reporte** com mirror no plan body + introduz mecanismo runtime de consumo. ADR-035 § Decisão sobre code-reviewer ganha categoria nova distinguindo "context-aware via messenger upstream" (introduzido) vs "free-read autônomo" (continua rejeitado).

3. **`skills/run-plan/SKILL.md` §2.3** — antes da invocação do reviewer por bloco, ler `## Decisões absorvidas` do plan body (se existir). Passar como contexto na prompt do reviewer (paralelo ao mecanismo de `**Termos ubíquos tocados:**`). Plano sem a seção → nada a passar (skip silente). Silente em runs sem ADR-038 in place (backward-compat).

4. **`agents/code-reviewer.md`** — adicionar cláusula nova (após bloco "Identificadores") materializando ADR-038: "Se o invocador passa `## Decisões absorvidas` como contexto, trate as estruturas listadas como **out-of-scope da rubrica YAGNI** — design-reviewer aprovou pré-commit + operador absorveu via ADR-026; flagar essas estruturas viola 'override por inação' de ADR-035 (refinada por ADR-038 para context-aware via messenger). Reporte apenas violações em estruturas **fora** da lista absorvida."

5. **`skills/triage/SKILL.md` step 5** — estender "Forma do commit message com findings absorvidos" para incluir mirror no plan body. Mesma seção `## Decisões absorvidas` (formato idêntico ao commit message) escrita no body do plano (após `## Notas operacionais`) antes do commit. Último commit do plano — uma vez shipado, mirror começa a ser escrito; mecanismo runtime (Blocos 3+4) ativa-se completo.

## Arquivos a alterar

### Bloco 1 — templates/plan.md nova seção opcional {reviewer: doc}

- `templates/plan.md`: após `## Notas operacionais` existente (último opcional listado no template), adicionar entry `## Decisões absorvidas` no bloco de opcionais com comentário-guia descrevendo origem (mirror do commit message bloco prescrito por ADR-026 + ADR-038) e formato esperado (bullets curtos `- <localização>: <correção> (caminho-único).`).

### Bloco 2 — docs/decisions/ADR-038 via /new-adr (sucessor parcial ADR-026 + refina ADR-035) {reviewer: doc}

- **Implementar:** invocar `Skill('pragmatic-dev-toolkit:new-adr', args='mirror de Decisões absorvidas no plan body e consumo runtime por reviewers')`. /new-adr cria ADR-038 + fira design-reviewer pre-return (per /new-adr spec). ADR-038 § Origem cita ADR-026 (sucessor parcial — estende Forma), ADR-035 (refina subseção code-reviewer), ADR-034 (5ª condição justifica novo ADR), ADR-021 (pattern paralelo de mensageiro).
- ADR-038 § Decisão: (a) Mirror de `## Decisões absorvidas` no plan body além do commit message (preserva ADR-026 vigente; greppability dupla); (b) `/run-plan` §2.3 lê e passa como contexto a todos os reviewers (uniform protocol); (c) `code-reviewer` ganha cláusula "out-of-scope da rubrica YAGNI quando há messenger upstream" — categoria nova distinguindo context-aware via messenger (introduzido) vs free-read autônomo (continua rejeitado per ADR-035).
- Doc-reviewer no /run-plan Bloco 2 verifica drift apenas (design-reviewer dentro do /new-adr já cobriu estrutural).

### Bloco 3 — skills/run-plan/SKILL.md §2.3 ler + passar contexto {reviewer: code}

- `skills/run-plan/SKILL.md`: em §2.3 (loop por bloco, item 3 "Escolher revisor"), adicionar sub-passo antes da invocação: "Ler `## Decisões absorvidas` do plan body se existir (paralelo a `**Termos ubíquos tocados:**`); passar conteúdo da seção como contexto adicional na prompt do reviewer escolhido. Plano sem a seção → nada a passar (skip silente). Mecanismo prescrito por ADR-038."
- Silente em planos antigos (backward-compat).

### Bloco 4 — agents/code-reviewer.md cláusula respeitar Decisões absorvidas {reviewer: doc}

- `agents/code-reviewer.md`: após bloco "## O que flagrar → ### Identificadores" (penúltimo), adicionar nova seção `### Respeito a Decisões absorvidas (context-aware via messenger upstream)` com cláusula: (a) quando contexto passa Decisões absorvidas, tratar estruturas listadas como out-of-scope da rubrica YAGNI; (b) cross-ref a ADR-026 (origem do mecanismo) + ADR-035 (override-by-inaction principle) + ADR-038 (refinamento que introduz context-aware switch via messenger); (c) ainda reportar violações em estruturas **fora** da lista absorvida.
- Reviewer escolhido = doc-reviewer (path `.md`) para evitar code-reviewer revisando seu próprio def na mesma execução; drift check é o eixo apropriado para esta edit (estrutural foi coberto por design-reviewer no plano via /triage step 5).

### Bloco 5 — skills/triage/SKILL.md step 5 mirror writer (último — ativa mecanismo) {reviewer: code}

- `skills/triage/SKILL.md`: em step 5, seção "Forma do commit message com findings absorvidos" — estender a regra atual para incluir mirror no plan body. Após o bloco que descreve formato do commit message, adicionar parágrafo: "Mirror no plan body (per ADR-038): a mesma seção `## Decisões absorvidas` é escrita no body do plano (após `## Notas operacionais` quando existe), mesmo formato de bullets. Edit cirúrgico antes do commit (mesma sequência atômica). Plano sem `## Notas operacionais` → seção adicionada como último bloco antes do EOF."
- Último commit do plano — depois deste, mirror começa a aparecer em planos novos; mecanismo completo ativo.

## Verificação end-to-end

- `grep -n "## Decisões absorvidas" templates/plan.md` retorna match.
- `ls docs/decisions/ADR-038-*.md` retorna 1 arquivo.
- `grep -nE "(plan body|Decisões absorvidas)" skills/triage/SKILL.md` retorna match na seção "Forma do commit message".
- `grep -nE "(Decisões absorvidas|plan body)" skills/run-plan/SKILL.md` retorna match em §2.3.
- `grep -nE "(Decisões absorvidas|context-aware via messenger|out-of-scope da rubrica YAGNI)" agents/code-reviewer.md` retorna match na cláusula nova.
- Inspeção textual: nenhum dos 5 edits deleta regra anterior — ADR-026 commit message section permanece prescrito; ADR-035 § Decisão sobre code-reviewer permanece (refinada explicitamente por ADR-038 que introduz a categoria messenger).

## Verificação manual

- **Próxima execução `/triage` caminho-com-plano que absorve findings:** verificar que (a) commit message contém `## design-reviewer findings absorvidos` como antes; (b) plan body file contém `## Decisões absorvidas` com o mesmo conteúdo. Mirror funcional.
- **Próxima execução `/run-plan` com plano que tem `## Decisões absorvidas`:** verificar (via observação do trace de invocação dos reviewers) que reviewer recebe o contexto. `code-reviewer` em bloco que toca estrutura listada na seção não deve flagar.
- **Plano antigo sem `## Decisões absorvidas`:** `/run-plan` continua funcionando sem fricção; skip silente da nova mecânica (backward-compat).

## Notas operacionais

- **Ordem editorial dos blocos**: 1 (template, passiva) → 2 (ADR-038 doutrina) → 3 (reader silente sem seção) → 4 (consumer silente sem contexto) → 5 (writer último, ativa mecanismo completo). Cada commit deixa sistema funcionalmente consistente — não há estado intermediário inconsistente. Reordenação confirmada via cutucada (F4 absorbed).
- design-reviewer dispatcha automaticamente pré-commit (ADR-011); free-read prioriza ADRs candidatos em `## Contexto`. Já executado para este plano.
- **Bloco 2 invoca /new-adr (delegação)** — pattern paralelo a /triage step 4 ADR path. /new-adr executa próprio design-reviewer pre-return (ADR-011 wiring); findings tratados lá. /run-plan §2.3 ainda escolhe reviewer block-level (doc-reviewer aqui) para drift check pós-criação do ADR.
- **Recursão controlada Bloco 4:** edita `agents/code-reviewer.md`. Reviewer = doc-reviewer para evitar code-reviewer revisando próprio def na mesma execução. Drift check é eixo apropriado.
- **Backward-compat:** planos antigos sem `## Decisões absorvidas` continuam executáveis (reader skip silente). Commits antigos com só o bloco no commit message permanecem auditáveis via `git log -p`.
- **Não cobre decisões implícitas de conversa:** operador respondendo X em AskUserQuestion sem registro no plano continua dependendo do agente. Coberto apenas o que vai para o mirror via ADR-026 + ADR-038.

## Decisões absorvidas

<!-- Mirror do bloco `## design-reviewer findings absorvidos` do commit message deste plano, per ADR-026 § Forma estendida por ADR-038 (a ser criado no Bloco 2). Para este plano específico — pre-mirror — apenas o commit message carrega a seção; este bloco fica como placeholder editorial mostrando o formato futuro. -->

- `## Resumo da mudança` "Escopo do mensageiro": rebatida alternativa "passar contexto só ao `code-reviewer`" — uniform protocol vence por permitir extensão futura a outros reviewers só editando o agent def (sem tocar `/run-plan`) com custo simétrico (caminho-único, F1 absorbido pré-commit).
