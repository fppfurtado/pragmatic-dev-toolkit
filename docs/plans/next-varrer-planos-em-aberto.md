# Plano — `/next` varrer planos em aberto via ADR-060

## Status

Pendente

## Contexto

**ADRs candidatos:** ADR-060 (decisão central que codifica state machine `Pendente`/`Abortado` + signal canonical field-or-git cross-reference), ADR-049 (fronteira § Decisão (a) state-em-git preservada — `Em execução` derivado de worktree+PR, não de markdown), ADR-022 (cadeia preservada como fallback de `Concluído`).

**Linha do backlog:** plugin: `/next` varrer planos em aberto paralelo ao passo 4.5 — bloco informativo separado análogo ao "Pendências de validação em planos", mas filtrando por heurística de completude (depende do ADR do item anterior — dependência editorial). Detecção: listar `plans_dir` excluindo `archive/`, filtrar não-em-curso (worktree-active + PR/MR aberto, mesma lógica do 4.5), classificar restante via heurística cristalizada. Trade-off: sem heurística boa, lista vem poluída (125 planos hoje em `docs/plans/` deste repo; muitos prováveis pós-execução sem `/archive-plans` aplicado) e o sinal perde valor. Forma: plano (mudança em `skills/next/SKILL.md` + possivelmente `templates/plan.md` per heurística escolhida).

ADR-060 cristalizou o signal canonical. `/next` hoje passo 4.5 cobre **pendências post-validation**; planos em estado `Pendente`/`Abortado` ficam invisíveis. Caso empírico desta sessão: `session-audit-skill.md` recebeu `## Status: Pendente` (commit `c75c040`); operador invocando `/next` em sessão futura precisa vê-lo listado.

Escopo deste plano: edit cirúrgico em `skills/next/SKILL.md` adicionando passo 4.6 (paralelo ao 4.5) + extensão do passo 5 incluindo o novo bloco no relatório. **Fora-de-escopo:** `templates/plan.md` (campo `## Status` é opcional — operador inclui em planos novos via `/triage` step 4 quando ADR-060 for promovido; convenção forward-only sem necessidade de mexer no template agora), `CLAUDE.md` cross-ref para ADR-060 (editorial follow-up registrável em sessão futura), ADR-022 cross-ref parágrafo em § Decisão crit 3 (editorial follow-up registrado em ADR-060 § Auto-aplicação; `/new-adr § O que NÃO fazer` proibiu edit cross-ADR durante criação).

## Resumo da mudança

**Novo passo 4.6 "Varrer planos em aberto" em `skills/next/SKILL.md`** paralelo ao 4.5 (rationale análogo — orientação sessional sobre planos que não estão em fluxo de validação, não compete no enum):

- Reusa listagem e filtro do 4.5 (papel `plans_dir` resolvido + exclusão de em-curso via worktree-active + PR/MR aberto).
- Classifica restante por estado per ADR-060 § Modelo de signal:
  - **`Pendente`** — plano contém bloco `## Status` com valor `Pendente` (matching textual via `grep -A1 "^## Status$" docs/plans/<slug>.md | tail -1`).
  - **`Abortado`** — mesmo grep, valor `Abortado`.
  - **Outros** (field ausente OR valor não-canonical OR plano arquivado) — skip silente. `Concluído` via `archive/` presence + ADR-022 cadeia ortogonal; `Em execução` filtrado em-curso.
- Acumula pares `(slug, estado)`.

**Extensão do passo 5 "Apresentar resultado":**

- Adiciona bullet "**Planos em aberto**" entre "Pendências de validação em planos" e a cutucada de descoberta. Lista `<slug>: <Pendente|Abortado>`. Lista vazia → omitir bloco (mesma convenção do 4.5).
- Não compete no enum top-3 (mesma convenção): operador endereça via `Other` se quiser priorizar um plano específico.

Sem mudança em frontmatter (papel `plans_dir` segue `informational`). Idioma PT-BR preservado.

## Arquivos a alterar

### Bloco 1 — passo 4.6 + extensão do passo 5 em `/next` SKILL {reviewer: code}

- `skills/next/SKILL.md`: 
  - Inserir seção `### 4.6. Varrer planos em aberto` após `### 4.5. Varrer pendências de validação em planos` com estrutura paralela (header + 3 sub-steps: listar planos não-em-curso reusando 4.5, classificar por estado, acumular pares); referenciar ADR-060 inline para o critério de classificação.
  - Estender passo 5 incluindo bullet "**Planos em aberto**" como bloco separado análogo a "Pendências de validação em planos"; preservar prosa "não compete no enum" da convenção existente.
  - Eventualmente atualizar bullet de `## O que NÃO fazer` se algum guard novo emergir do design-reviewer.

## Verificação end-to-end

1. **Edit aplicado:** `grep -c "^### 4\.6\." skills/next/SKILL.md` retorna `1`.
2. **Referência a ADR-060:** `grep -c "ADR-060" skills/next/SKILL.md` retorna ≥1 (citação inline no critério de classificação).
3. **Bloco do passo 5 estendido:** `grep -c "Planos em aberto" skills/next/SKILL.md` retorna ≥2 (passo 4.6 + bullet no passo 5).
4. **Edit aditivo sem reescrita estrutural não-intencional:** `git diff --stat skills/next/SKILL.md` mostra apenas additions (sem `-` lines fora dos blocos editados); inspeção visual confirma que headers existentes (4.5, 5, etc.) preservam ordering original.
5. **Paridade prosaica com 4.5:** `grep -c "não compete no enum" skills/next/SKILL.md` retorna ≥2 (4.5 existente + 4.6 novo) — invariante editorial preservada.

## Verificação manual

1. **Cenário 1 (caso empírico canônico):** consumer com `docs/plans/session-audit-skill.md` contendo bloco `## Status\n\nPendente` (estado real desta sessão pós-`c75c040`), sem worktree para `session-audit-skill`, sem PR referenciando `session-audit-skill`. Invocar `/next 3`. Esperado: bloco "Planos em aberto" no relatório lista `session-audit-skill: Pendente`. Não interfere no enum top-3.

2. **Cenário 2 (`Abortado` explícito):** fixture com plano contendo `## Status\n\nAbortado`. Esperado: aparece no bloco como `<slug>: Abortado`. Operador pode endereçar via `Other` se quiser reabrir.

3. **Cenário 3 (em-curso filtrado mesmo com Status: Pendente):** plano com `## Status: Pendente` E worktree-active (estado anômalo possível durante `/run-plan` se field não removido). Esperado: filtrado pelo critério "em curso" do passo 4.6 (mesma lógica do 4.5); não aparece no bloco. Anomalia editorial (operador deve verificar se `/run-plan §3.4` removeu field corretamente).

4. **Cenário 4 (lista vazia → bloco omitido):** consumer sem nenhum plano com `## Status` field canonical. Esperado: bloco "Planos em aberto" **omitido** do relatório (paridade com 4.5 quando vazio).

5. **Cenário 5 (não compete no enum):** com Cenário 1 ativo, verificar que o enum top-3 do `/next` continua com 3 opções nomeadas pelo texto exato da linha do BACKLOG + `Other`. Nenhuma opção "Planos em aberto" no enum. Operador escolhe `Other` e descreve `/run-plan session-audit-skill` se quiser priorizar.

6. **Cenário 6 (modo local):** consumer com `paths.plans_dir: local`. Passo 4.6 lê de `.claude/local/plans/` em vez de `docs/plans/`. Esperado: bloco "Planos em aberto" presente; slug aparece no relatório (ephemeral — `/next` não persiste mutação). Sem leak risk no scope desta skill; ADR-047 § Decisão (c) aplica apenas a downstream skills mutativas (`/triage`, `/run-plan`).

7. **Cenário 7 (valor não-canonical no field):** plano com `## Status: WIP` (drift textual — valor não-aceito per ADR-060). Esperado: skip silente (não classifica como Pendente nem Abortado; ADR-060 § Localização do campo prescreve reviewer flagar pré-merge; runtime degrada graciosamente).

## Notas operacionais

- **ADR-060 status `Proposto`.** Wiring em produção exercita o ADR; smoke real bem-sucedido do Cenário 1 desbloqueia promoção para `Aceito (2026-06-12)`. Per gatilho de revisão #4 do próprio ADR-060: "Status field não consumido em produção em 2 ondas de migração doutrinal → reabrir". Este plano é o primeiro consumer.

- **Single mutation point preservado.** `/run-plan §3.4` (remoção do field no done) **NÃO é tocado neste plano** — escopo é só `/next` (consumer). Wiring de `/triage` step 4 (criar field=Pendente) também **fora de escopo aqui**. Esses 2 wirings adicionais ficam como follow-up registráveis em BACKLOG após este plano shipar e ADR-060 promovido para `Aceito`.

- **ADR-022 cross-ref pendente.** Per ADR-060 § Auto-aplicação, ADR-022 § Decisão critério 3 deve receber parágrafo cross-ref pra ADR-060 (per ADR-034 § Localização do adendo). Editorial follow-up — fora de escopo deste plano (sucessor parcial precedente foi commitado em `c8675a1`; cross-ref é editorial pós-fato).

- **Plano committed e push como unidade atômica** per `/triage` § 5 — caminho-com-plano em main.

## Pendências de validação

- Smoke real dos 7 cenários do `## Verificação manual` pós-`/reload-plugins` em consumer com fixture (`session-audit-skill` com `## Status: Pendente` já materializado em `c75c040` é candidato natural ao Cenário 1). Cobertura textual passou pelo gate `/run-plan §3.2` desta sessão; comportamental fica pendente até reload + invocação real.

## Decisões absorvidas

- `## Verificação end-to-end` critério 4: substituído `count de \`### \` aumenta exatamente 1` por `git diff --stat` additions-only + inspeção visual — diretriz canonical de `templates/plan.md` §2 (counts como variável ou condição inversa) — caminho-único.
- `## Verificação manual` Cenário 6: simplificado framing do leak risk — `/next` não persiste mutação, ADR-047 § Decisão (c) aplica a downstream mutativas — caminho-único.
