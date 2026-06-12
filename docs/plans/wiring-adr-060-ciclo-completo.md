# Plano — Wiring de ADR-060 (`## Status` field) em `/triage` + `/run-plan`

## Contexto

**ADRs candidatos:** ADR-060 (decisão central — § Wiring nas skills prescreve `/triage` step 4 cria `Pendente` + `/run-plan §3.4` remove no done), ADR-049 (fronteira § Decisão (a) state-em-git preservada — wiring respeita); ADR-022 (cadeia editorial preservada — mutação em plano body não toca BACKLOG cadeia).

**Linha do backlog:** plugin: wiring residual de ADR-060 — `/triage` step 4 cria `## Status: Pendente` em planos novos do caminho-com-plano; `/run-plan §3.4` remove o bloco integralmente no done. Fecha o ciclo do Status field (escrita na criação + limpeza no done). Resolve drift empírico em `docs/plans/next-varrer-planos-em-aberto.md` (Status: Pendente stale pós-merge PR #117).

ADR-060 § Wiring nas skills define os 2 pontos canonical de mutação:

- `/triage` step 4 (caminho-com-plano): copia template + preenche `## Status` com `Pendente`. Single mutation no momento de criação (plano não existe em git ainda; sem worktree, sem race).
- `/run-plan §3.4` (done): edit cirúrgico **remove** o bloco `## Status` (header + linha de valor) do plan body. Mesma sequência atômica do mark em `## Concluídos` do BACKLOG.

Sem essas 2 edições, ADR-060 fica em estado "consumer wired mas producer ausente": `/next varrer planos em aberto` lê o field mas (a) novos planos não recebem field automaticamente (false-negatives — novo plano `Pendente` invisível ao `/next`); (b) planos shippados mantêm field stale (false-positives — caso `next-varrer-planos-em-aberto` aparece como Pendente mesmo concluído). Wiring fecha as 2 pontas.

Escopo: edits cirúrgicos em `skills/triage/SKILL.md` (passo 4 § "Plano (papel: `plans_dir`)") + `skills/run-plan/SKILL.md` (passo §3.4 "Registro em Concluídos"). **Fora-de-escopo:** `templates/plan.md` — campo `## Status` permanece opcional no template; `/triage` insere o bloco programaticamente após copiar o template, não pela presença do bloco no esqueleto. Esta separação preserva `templates/plan.md` agnóstico para planos hand-written que adotem ADR-060 manualmente.

## Resumo da mudança

**Bloco 1 — `/triage` step 4 cria field:**

Em `skills/triage/SKILL.md`, na subseção "Plano (papel: `plans_dir`)" do passo 4, adicionar prosa após o parágrafo de copy-do-template explicitando que skill insere `## Status\n\nPendente` no plano logo após o `# Plano — <Título>` (antes de `## Contexto`). Posicionamento per ADR-060 § Localização do campo.

**Bloco 2 — `/run-plan §3.4` remove field no done:**

Em `skills/run-plan/SKILL.md`, no parágrafo do passo §3.4 "Registro em Concluídos", adicionar que o **bloco extra** (atualizar `backlog` → revisor `code` → micro-commit) também **remove o bloco `## Status` do plan body** na mesma sequência atômica do mark em `## Concluídos`. Em modo `local`, edit no plan local (gitignored, sem trace).

Sem mudança no template, sem mudança em outros passos. Idioma PT-BR preservado em ambas edições.

## Arquivos a alterar

### Bloco 1 — `/triage` step 4 cria `## Status: Pendente` {reviewer: code}

- `skills/triage/SKILL.md`: na subseção "Plano (papel: `plans_dir`)" do passo 4 (atual linha ~105), adicionar 1-2 frases após o parágrafo de cópia do template explicitando que `/triage` insere `## Status\n\nPendente` logo após `# Plano — <Título>` e antes de `## Contexto`. Citar ADR-060 § Localização do campo inline.

### Bloco 2 — `/run-plan §3.4` remove `## Status` no done {reviewer: code}

- `skills/run-plan/SKILL.md`: no parágrafo do passo §3.4 "Registro em Concluídos" (atual linha ~157), estender a descrição do **mesmo bloco extra** (atualizar `backlog` → revisor `code` → micro-commit) de modo que **o mesmo commit edite 2 arquivos**: `BACKLOG.md` (mark Concluídos) **+** plan body (remove bloco `## Status` integralmente). Sequência atômica preservada; reviewer code cobre os 2 edits; micro-commit unificado. Citar ADR-060 § Wiring nas skills inline. Em modo `local`, edit no plan local (gitignored).

### Bloco 3 — limpeza retroativa do drift em `next-varrer-planos-em-aberto.md` {reviewer: code}

- `docs/plans/next-varrer-planos-em-aberto.md`: remover o bloco `## Status\n\nPendente` (linhas 3-5 do arquivo) — field stale pós-merge PR #117, residual do programa que precedeu o wiring desta sessão. Edit cirúrgico isolado; sem mudança no resto do conteúdo. Operação dogfood — exercita Bloco 2 retroativamente sobre o plano pioneiro do consumer (a `/next` SKILL editada em PR #117).

## Verificação end-to-end

1. **Bloco 1 citação literal do field:** `grep -c "## Status" skills/triage/SKILL.md` retorna ≥1 (header do bloco mencionado em prosa) AND `grep -c "Pendente" skills/triage/SKILL.md` retorna ≥1 (valor inicial).
2. **Bloco 1 ancorada em ADR-060:** `grep -c "Localização do campo" skills/triage/SKILL.md` retorna ≥1 (citação literal da seção ADR no parágrafo editado).
3. **Bloco 2 ancorada em ADR-060:** `grep -c "Wiring nas skills" skills/run-plan/SKILL.md` retorna ≥1 (citação literal da seção ADR no parágrafo editado).
4. **Bloco 3 drift removido:** `grep -c "^## Status$" docs/plans/next-varrer-planos-em-aberto.md` retorna `0` (header inteiramente removido).
5. **Edits aditivos nos SKILLs + cirúrgico no plano histórico:** `git diff --stat <base>..HEAD skills/triage/SKILL.md skills/run-plan/SKILL.md` mostra apenas additions (sem `-` lines fora dos parágrafos editados); `git diff --stat <base>..HEAD docs/plans/next-varrer-planos-em-aberto.md` mostra removal de 4 linhas (header + blank + valor + blank).

## Verificação manual

1. **Cenário 1 (criação canônica):** invocar `/triage <intent>` em consumer que vá produzir plano (caminho-com-plano). Esperado: plano novo em `docs/plans/<slug>.md` contém bloco `## Status\n\nPendente` logo após `# Plano — <Título>` e antes de `## Contexto`. Verificável via `awk '/^## Status$/{flag=1; next} flag && NF{print; exit}' docs/plans/<slug>.md` retornar `Pendente`.

2. **Cenário 2 (done remove field):** invocar `/run-plan <slug>` em plano com `## Status: Pendente` criado no Cenário 1. Esperado: após `§3.4 Registro em Concluídos`, plano não contém mais bloco `## Status` no body. Verificável via `grep -c "^## Status$" docs/plans/<slug>.md` retornar `0`.

3. **Cenário 3 (ciclo completo `/triage` → `/run-plan` → `/next`):** sequenciar Cenário 1 + Cenário 2 em consumer; após Cenário 2 (done), invocar `/next`. Esperado: plano não aparece no bloco "Planos em aberto" (field removido + presença em `archive/` pendente OU linha em `## Concluídos`).

4. **Cenário 4 (drift histórico — `next-varrer-planos-em-aberto`):** Bloco 3 deste plano remove o field stale como parte do escopo. Após shipping, verificar via `awk '/^## Status$/{flag=1; next} flag && NF{print; exit}' docs/plans/next-varrer-planos-em-aberto.md` retornar vazio (zero output) — confirmando dogfood retroativo do Bloco 2 sobre o plano pioneiro do consumer.

5. **Cenário 5 (caminho ADR-only não cria field):** `/triage` que produz ADR-only (sem plano) **não** cria field — só caminho-com-plano. Verificável: SKILL prescreve insertion só na subseção "Plano (papel: `plans_dir`)" do passo 4, não em outras subseções.

6. **Cenário 6 (modo `local` — `paths.plans_dir: local`):** plano em `.claude/local/plans/<slug>.md` recebe field na criação + remove no done. Mesma mecânica do canonical; sem trace em commit (per ADR-047 regra de não-referenciar). Não exercitável agora sem fixture local; documentado como pendência se necessário.

7. **Cenário 7 (modo `runbook`):** plano com `**Modo:** runbook` em `## Contexto`. Per ADR-049 § Decisão (d), §3.4 do `/run-plan` aplica em runbook (último item da tabela "Em modo runbook"). Field removal acompanha o bloco extra do backlog mark. **Nota:** plano runbook típico é hand-written sem field `## Status` (não passa por `/triage` step 4 que insere automaticamente); se operador inclui manualmente, §3.4 remove na mesma sequência atômica. Cenário cobre interoperabilidade defensiva, não wiring automático canonical.

## Notas operacionais

- **Plano dogfood:** este próprio plano carrega `## Status: Pendente` no body (linhas 3-5 acima). Pós-execução, o `/run-plan §3.4` editado por este mesmo plano remove o field. Auto-aplicação editorial — o wiring se prova ao se executar.

- **Drift histórico endereçado via Bloco 3.** Field stale em `next-varrer-planos-em-aberto.md` removido como parte do escopo (decisão design-reviewer 2026-06-12, finding F2 absorvido). Dogfood retroativo — exercita Bloco 2 sobre o plano pioneiro do consumer.

- **Ordering de execução:** Bloco 1 (`/triage`) edita o producer; Bloco 2 (`/run-plan`) edita o consumer do field; Bloco 3 cleanup histórico. Ordem não-crítica para o resultado final; testabilidade do Cenário 3 depende dos 3 blocos shippados antes do smoke real.

- **Wiring posterior:** este plano fecha o último wiring de ADR-060 vis-à-vis o producer + consumer mecânico. Editorial follow-up restante: CLAUDE.md cross-ref pra ADR-060 em § Editing conventions (separado deste plano per Ockham — esses cross-refs são listáveis manualmente quando o operador editar CLAUDE.md por outras razões).

## Pendências de validação

- Smoke comportamental real dos Cenários 1+2+3 pós-`/reload-plugins` em consumer: (a) invocar `/triage` em consumer pra verificar criação do field; (b) `/run-plan` em plano com field pra verificar removal; (c) ciclo completo `/triage` → `/run-plan` → `/next`. Validação textual passou via gate `/run-plan §3.2` desta sessão; comportamental fica pendente até reload + invocações reais. Cenário 2 foi exercitado empiricamente como dogfood circular no §3.4 desta execução (este próprio plano teve `## Status` removido).

## Decisões absorvidas

- Verificação end-to-end critério 1: substituído `grep` multilinha mal-formado (`"## Status\\n\\nPendente"`) por dois greps separados (`## Status` + `Pendente`) per diretriz canonical de `templates/plan.md` §2/§3 (fidelidade ao texto-alvo + Read antes de hardcode) — caminho-único.
- Verificação manual Cenário 7: adicionada nota inline esclarecendo que plano runbook típico é hand-written sem field; cenário cobre interoperabilidade defensiva, não wiring automático — caminho-único.
- Bloco 2 wording: explicitado que **mesmo bloco extra** edita 2 arquivos (`backlog` + plan body) no mesmo commit; reduz risco de implementador entender como sequência de 2 micro-commits — caminho-único.
