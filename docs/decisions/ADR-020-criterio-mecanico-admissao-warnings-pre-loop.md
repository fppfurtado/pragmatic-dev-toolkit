# ADR-020: Critério mecânico de admissão de warnings pré-loop em /run-plan

**Data:** 2026-05-12
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-002](ADR-002-eliminar-gates-pre-loop.md) — eliminação de gates de cutucada na fase pré-loop do `/run-plan`. Gatilho § "Gatilhos de revisão": *"Surge um 5º+ warning na fase pré-loop com natureza distinta dos atuais → reavaliar se cabe nos trilhos existentes ou exige nova categoria."* ADR-020 exerce o gatilho **preventivamente** — hoje 5/5 warnings; formalizar o critério antes do 6º bater evita decisão caso-a-caso pressionada.
- **Investigação:** Auditoria arquitetural 2026-05-12 (`docs/audits/runs/2026-05-12-architecture-logic.md`, achado E3 + proposta C_arch). Modelo de critério mecânico inspirado em [ADR-013](ADR-013-ci-lint-minimo-no-build-runner.md) — critérios cumulativos para classificar gate de CI lint.

## Contexto

ADR-002 estabeleceu 3 trilhos para findings da fase pré-loop:

- **Aviso informativo + segue** — reportado in situ, não alimenta o gate final.
- **Backlog** — entrada em `## Próximos` do papel `backlog`.
- **Validação** — entrada em `## Pendências de validação` do plano corrente.

5 warnings concretos hoje (`skills/run-plan/SKILL.md:46-52`):

| Warning | Trilho atual |
|---|---|
| Alinhamento dirty | Aviso |
| `.worktreeinclude` ausente | Backlog |
| Credencial não coberta | Validação |
| Escopo divergente | Validação |
| Cobertura ausente | Validação |

ADR-002 § Limitações reconhece: *"ADR não promete que todo warning futuro caiba nos trilhos existentes."* O 5º (cobertura ausente, shippado per BACKLOG ## Concluídos) foi admitido como Validação por analogia, sem critério mecânico explícito.

A próxima proposta de warning bate diretamente no gatilho de reabertura. Sem critério formal, cada admissão vira mini-debate editorial; com candidatos potenciais cabíveis (heurísticas de produção, padrões de stack novos, formas de pendência operacional), o custo de decisão caso-a-caso supera o de codificar o critério.

ADR-013 estabeleceu precedente de **critério mecânico cumulativo** para classificação de fronteira. O padrão se replica quando uma categoria cresce além do data point original.

## Decisão

**Warning candidato é admitido em trilho pré-loop existente (Aviso / Backlog / Validação) quando satisfaz cumulativamente os 3 critérios abaixo. Falha em qualquer um → redirecionamento à superfície adequada (`/triage`, loop interno, bloqueio in situ) ou, em último caso, reabertura formal de ADR-002 com proposta de trilho novo.**

### Pré-requisito: warning, não bloqueio

ADR-020 cobre admissão de **warnings** — qualidade-de-mudança que merece atenção mas não impede progresso. **Bloqueios** (estado git inválido, baseline vermelho, worktree órfã, push esquecido) são categoria pré-existente que **para a skill**; seguem fora deste critério. Reclassificação silenciosa de bloqueio como warning é cenário a vetar antes de aplicar os critérios abaixo: se a presença do candidato torna o `/run-plan` inviável, candidato é bloqueio, não warning.

### Os 3 critérios cumulativos

1. **Detecção determinística antes da worktree.** Warning é identificável por inspeção do estado git/working tree do consumer + plano corrente, sem rodar código de produção, sem invocar toolchain (linters, test runners, builds), sem leitura de remoto. Detecção síncrona no fio principal da skill, sem latência percebível pelo operador.

2. **Mapeável a Aviso / Backlog / Validação por construção:**
   - **Aviso informativo** quando o custo de detecção tardia é **baixo** — reviewer no loop ou gate final cobre eventualmente.
   - **Backlog** quando o warning aponta lacuna **fora do escopo do plano corrente** (infra do consumer ausente, gap genérico) e a resolução pode ser deferida sem comprometer o done.
   - **Validação** quando o warning sinaliza cenário **dentro do escopo do plano corrente** que pode não ser exercitado no done (código tocado sem teste, credencial não disponível, superfície externa não-listada).

3. **Decidível sem perguntar ao operador.** Classificação no trilho é função de (a) inputs determinísticos do critério 1 e (b) inspeção do plano corrente. Sem `AskUserQuestion`, sem prosa interativa. Princípio ADR-002 ("zero gate de cutucada na fase pré-loop") preservado.

### Falha em critério → redirecionamento ou reabertura

Falha em **qualquer** dos 3 critérios sinaliza que o warning candidato não pertence à fase pré-loop. Tratamento por critério falhado:

- **Falha em (1)** — detecção exige toolchain, rede, ou tempo perceptível. Candidato pertence a **gate dentro da worktree** (no loop, não pré-loop). Não admitir pré-loop; considerar como gate por bloco.
- **Falha em (2)** — warning não mapeia naturalmente a Aviso / Backlog / Validação. Único caso que justifica **reabertura formal de ADR-002** com proposta de trilho novo + justificativa de por que os 3 trilhos atuais são insuficientes.
- **Falha em (3)** — warning exige decisão do operador para classificar. **Candidato pertence a outra superfície**, não à fase pré-loop:
  - Bifurcação arquitetural, escopo de feature, escolha de caminho → `/triage` (alinhamento prévio).
  - Decisão sobre artefato gerado, cobertura semântica de teste → loop interno do `/run-plan` (gate no/pós bloco) ou reviewer dedicado (`code-reviewer`, `qa-reviewer`).
  - Reabertura de ADR-002 só se nem `/triage` nem o loop cobrem — sinal real de categoria nova de gate, não falha do critério.

### Aplicação retroativa aos 5 atuais

Verificação de consistência — cada warning hoje atende os 3 critérios:

| Warning | (1) Determinismo | (2) Trilho | (3) Sem pergunta |
|---|---|---|---|
| Alinhamento dirty | `git status --porcelain` | Aviso (custo tardio baixo) | ✓ |
| `.worktreeinclude` ausente | inspeção raiz + plano | Backlog (fora do plano corrente) | ✓ |
| Credencial não coberta | inspeção raiz + `.worktreeinclude` | Validação (cenário do plano não exercitado) | ✓ |
| Escopo divergente | comparação textual no plano | Validação (superfície fora do diff) | ✓ |
| Cobertura ausente | matching de patterns no plano | Validação (cenário sem teste) | ✓ |

Todos passam. Critério formaliza o que já operava implicitamente — não é mudança de comportamento, é codificação da regra editorial **e** gate preventivo para o 6º candidato.

**Observação editorial.** O warning "Cobertura ausente" já tem regra de classificação não-trivial (~10 linhas: positive list de manifestos, exclusões `.github/`/`docs/`/`.claude/`, set de test patterns). Está dentro do orçamento, mas é o data point que mais se aproxima do limite editorial — gatilho de revisão registra (ver § Gatilhos).

**Exemplos hipotéticos de candidatos que falham os critérios** (para validar que o critério discrimina, não só confirma):

- **Falha em (1):** *"warning 'cobertura semântica do teste insuficiente'"* exige mutation testing — toolchain + tempo. Categoria distinta: gate dentro da worktree (no/pós bloco com `{reviewer: qa}`).
- **Falha em (2):** *"warning 'dependência interna obsoleta detectada'"* — não mapeia naturalmente para Aviso (custo tardio alto: dependência quebrada quebra build), Backlog (resolução não é diferível, é parte do escopo) ou Validação (não é cenário a exercitar manualmente). Sinal de trilho novo — reabrir ADR-002.
- **Falha em (3):** *"warning 'mudança candidata a domain refactor'"* exige operador dizer se aceita escopo expandido. Pertence a `/triage` (bifurcação arquitetural), não pré-loop. Não admitir pré-loop.

## Consequências

### Benefícios

- **Próxima proposta de warning** entra com critério explícito de admissão; reabertura de ADR-002 só quando candidato falha o critério (2) especificamente.
- **Decisões de escopo ficam objetivas.** `code-reviewer`/`design-reviewer` ou contribuidor podem flagar candidato que falha critério antes do PR.
- **Categorias distintas** (warning pré-loop / bloqueio in situ / gate dentro da worktree / decisão de triage) ganham fronteira nítida — cada uma com governance própria, sem reabertura de ADR-002 como porta única.
- **Convergência conceitual com ADR-013.** Padrão "critério mecânico cumulativo" se replica quando categoria cresce além do data point original.

### Trade-offs

- **Operador precisa lembrar dos 3 critérios + pré-requisito** ao avaliar candidato. Mitigação: checklist explícito no body + tabela de aplicação retroativa + exemplos de falha servem como referência.
- **Falsa rigidez:** warning aproximadamente válido que falha um critério marginal pode ser rejeitado quando seria admissível com ajuste pequeno. Mitigação: gatilhos de revisão deste ADR cobrem desvio recorrente.

### Limitações

- ADR cobre **admissão**, não saída. Warning admitido continua válido até nova evidência (gatilho ADR-002 sobre `## Pendências de validação` crescendo sistematicamente, etc.). Política de despromoção não está aqui.
- Critério (3) "decidível sem perguntar" exclui categorias úteis que **pertencem a outras superfícies** (bifurcação arquitetural pertence a `/triage`; cobertura semântica de teste pode pertencer a `qa-reviewer` no loop). Por design — § Falha em critério → redirecionamento aponta destinos naturais sem reabertura espúria de ADR-002.
- Critério não cobre admissão de warnings em **outras skills** (`/release` pré-condições, `/triage` checklist do step 2, `/debug` precisar sintoma). Single data point hoje (`/run-plan`); generalização eventual sob ADR sucessor se padrão se repetir.

## Alternativas consideradas

### (a) Edit cirúrgico em ADR-002 (adendo de seção)

Adicionar `## Critério mecânico de admissão` ao ADR-002 in-place. **Caminho sugerido pela auditoria-fonte** (`docs/audits/runs/2026-05-12-architecture-logic.md` § Encaminhamento — proposta C: *"linha de backlog + edit cirúrgico de ADR-002 (adendo de critério)"*).

Descartada com 4 argumentos:

1. **Tensão editorial cronológica.** Mistura decisão original (2026-05-06, eliminar gates) com refinamento posterior (2026-05-12, codificar critério) sem versionamento explícito por datas/status distintos.
2. **Tensão de escopo doutrinário.** Decisão central de ADR-002 é *eliminar* gates; ADR-020 é *gate preventivo de admissão*. Anexar este como seção daquele cria documento com duas decisões diferentes sob mesmo cabeçalho.
3. **Precedente do plugin.** Refinamentos viraram ADRs sucessores: ADR-011 → ADR-009 (wiring automático), ADR-018 → ADR-005 (replicação `.claude/`), ADR-019 → ADR-008 (cross-ref reviewer↔skill). 3 instâncias consolidadas.
4. **Memory `feedback_adr_threshold_doctrine`** — *"refinar/inverter critério documentado em philosophy.md/CLAUDE.md (mesmo parcial) → default ADR"*. Aplicável aqui.

A sugestão da auditoria pesa contra essa rebatida, mas (1)-(4) cumulativamente vencem. Adendo permanece reversível se ADR-020 não exercer o critério em 1-2 admissões reais.

### (b) Linha de backlog sinalizando reabertura futura (sem critério agora)

Adiar decisão até o 6º warning aparecer e capturar a tensão como item de backlog. Descartada:
- C_arch tem como rationale **preempção** — critério antes do gatilho disparar evita decisão caso-a-caso sob pressão. Adiar inverte a proposta.

### (c) Critério não-cumulativo (qualquer um basta)

Em vez de 3 cumulativos, qualquer critério satisfeito autoriza admissão. Descartada:
- Modelo ADR-013 cumulativo provou-se preciso para classificar gates. "Qualquer-um basta" cria zona cinza (warning que satisfaz só (1) mas falha (3) entraria erroneamente).
- Cumulativo força reflexão sobre cada eixo (detecção, mapeamento, decisão) — falha em qualquer um é sinal forte.

### (d) Manter editorial sem critério mecânico

Continuar admitindo warnings por decisão caso-a-caso, sob disciplina do operador. Descartada:
- Disciplina editorial não escala — sem critério, cada candidato vira mini-debate; tensão maior conforme tamanho da fronteira cresce.
- ADR-002 § Limitações já antecipa o gatilho; deixar implícito é dívida formal.

### (e) Manter 4 critérios cumulativos (com "não-bloqueante" como eixo)

Versão anterior do draft tinha 4 critérios, sendo (2) "Não-bloqueante por construção". Descartada após revisão:
- (2) recapitulava a definição de warning vs. bloqueio já vigente em ADR-002 — tautológico, não eixo independente.
- Modelo ADR-013 tem 4 cumulativos por substância, não simetria. Reduzir a 3 cumulativos + pré-requisito explícito é mais honesto.

## Gatilhos de revisão

- **Warning candidato falha critério marginal** mas operador percebe que faria sentido admitir — reabrir o critério específico (não o ADR inteiro).
- **3+ admissões sob estes critérios em curto prazo** — sinal de que a fase pré-loop está absorvendo warnings que pertencem a outra superfície (`/triage`, loop interno). Revisar contornos.
- **Regra de mapeamento do critério (2) crescer >~5 linhas heurísticas** (paralelo ao "Cobertura ausente" hoje, que está no limite) → revisitar critério (2) ou mover warning para outra superfície. Sinal de complexidade saturada.
- **Falha em (2) virar reabertura recorrente** — se 2+ candidatos seguidos reabrem ADR-002 pelo critério (2), sinal de que os 3 trilhos (Aviso/Backlog/Validação) estão insuficientes; aceitar trilho novo.
- **Skill nova introduz warnings pré-loop** (hipotético: skill executora além de `/run-plan`) — reabrir para considerar generalização do critério a outras skills.
- **Próximo warning concreto bater no gatilho** — exercitar o critério em caso real, observar se a admissão flui sem reabertura. Se reabertura virar regra, critério precisa refinamento.
