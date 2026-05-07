# Plano — /run-plan: 5º warning pré-loop (cobertura de teste ausente)

## Contexto

Continuação direta de ADR-002 ("Eliminar gates de cutucada na fase pré-loop"), que documenta como gatilho de revisão:

> Surge um 5º+ warning na fase pré-loop com natureza distinta dos atuais → reavaliar se cabe nos trilhos existentes ou exige nova categoria.

Verificação: o warning proposto é (a) detectável antes da worktree, (b) não-bloqueante, (c) mapeável para Validação. Cabe nos trilhos existentes; **não exige novo ADR**.

Motivação concreta: hoje o fluxo confia 100% no autor do plano para listar arquivos de teste em `## Arquivos a alterar`. Se ele ignora a cutucada de "Cobertura de teste?" do `/triage` step 2, `/run-plan` executa silente e fecha como done sem nunca questionar cobertura. Belt-and-suspenders na fase pré-loop fecha o vazamento.

**Linha do backlog:** /run-plan: 5º warning pré-loop — plano altera código de produção sem listar arquivo de teste em `## Arquivos a alterar` → capturar como Validação ("cenário sem cobertura nova exercitada"). Análogo aos 4 atuais (alinhamento dirty, `.worktreeinclude`, credencial, escopo divergente); ADR-002 prevê 5º como gatilho de revisão. Heurística stack-agnóstica via patterns (`tests/`, `test_*`, `*_test.*`, `*.test.*`, `*.spec.*`, `__tests__/`, `src/test/`). Não gera teste — apenas cutuca via `## Pendências de validação`. Reavaliar se YAGNI: `/triage` step 2 já tem "Cobertura de teste?" no checklist; warning é belt-and-suspenders quando autor do plano ignora.

**Escopo escolhido (a):** sempre cutucar; operador filtra no done. Sem coordenação `/triage` ↔ `/run-plan`, sem extensão de `templates/plan.md`, sem retrofit. Aceita falsos positivos (refactor puro sem teste novo, mudança totalmente coberta por gate automático) tratados pelo operador na materialização do passo 3.5 — sinal explícito "descarta esse" entre aviso e materialização já existe. Caminho (b) descartado: anotar `**Cobertura de teste:** <i|ii|iii>` no `## Contexto` via `/triage` exigiria edição de 3 arquivos (`/triage`, `/run-plan`, `templates/plan.md`) e retrofit dos planos antigos para benefício marginal — falsos positivos esperados são poucos e o descarte é trivial.

## Resumo da mudança

Adição cirúrgica em `skills/run-plan/SKILL.md`:

- **5ª linha na tabela "Detecção de warnings pré-loop"**: "Cobertura ausente" → trilho **Validação**. Mensagem: `"capturei para verificação: cenário sem cobertura nova exercitada — código de produção em ## Arquivos a alterar sem teste correspondente (<paths>)"`.
- **Passo 3.5 — Captura automática**: na enumeração "Gatilhos pré-loop", adicionar 5º bullet `**Cobertura ausente** → entrada de Validação.` no padrão dos 4 anteriores.
- **Heurística stack-agnóstica** documentada na própria célula "Detecção" da tabela:
  - **Código de produção** = path em `## Arquivos a alterar` que NÃO seja: extensão `.md`/`.rst`/`.txt`; test pattern; manifesto/config (lista fixa); paths sob `.github/`/`.gitlab/`/`.circleci/`/`.azuredevops/`/`infra/`/`deploy/`/`.claude/`/`docs/`.
  - **Test patterns aceitos** (qualquer um suficiente para suprimir warning): `tests/`, `**/test_*`, `**/*_test.*`, `**/*.test.*`, `**/*.spec.*`, `__tests__/`, `src/test/`.
  - **Manifestos/config** (exclusão de "código de produção"): `pyproject.toml`, `package.json`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `Gemfile`, `go.mod`, `go.sum`, `requirements*.txt`, `Pipfile*`, `tsconfig*.json`, `.eslintrc*`, `.prettierrc*`, `Dockerfile*`, `compose.y*ml`, `docker-compose.y*ml`, `*.lock`.
  - Ambas as condições (≥1 path de produção E nenhum path de teste) verdadeiras → warning dispara.

Sem mudança em pré-condições, passos 1-3.4, 3.6-3.7, `## O que NÃO fazer`. Sem mudança em outras skills, agents, hooks, templates. Sem CLI/flag/env nova.

## Arquivos a alterar

### Bloco 1 — adicionar 5º warning pré-loop em /run-plan SKILL.md {reviewer: code}

- `skills/run-plan/SKILL.md`:
  - **Tabela "Detecção de warnings pré-loop"**: adicionar 5ª linha "Cobertura ausente" com a heurística completa na célula Detecção (definições de "código de produção" e "test patterns aceitos" inline, no mesmo registro de prosa densa das linhas 2-4) e mensagem-padrão de Validação na célula Trilho.
  - **Passo 3.5, sub-seção "Gatilhos pré-loop"**: adicionar 5º bullet "**Cobertura ausente** → entrada de Validação." entre os 4 atuais.
  - Sem outras alterações no arquivo.

## Verificação end-to-end

Refactor textual sem suite executável; gate é inspeção dirigida:

1. **5ª linha na tabela**:
   - `grep -n "Cobertura ausente" skills/run-plan/SKILL.md` retorna ≥2 ocorrências (linha da tabela + bullet do passo 3.5).
   - Tabela "Detecção de warnings pré-loop" tem 5 linhas (4 atuais + cobertura ausente).
   - Célula "Trilho" da nova linha começa com `**Validação**:` e mensagem com `"capturei para verificação: cenário sem cobertura nova exercitada — ..."` (espelha padrão das linhas Credencial/Escopo).

2. **Heurística documentada na célula Detecção**:
   - Cita os 7 test patterns: `tests/`, `**/test_*`, `**/*_test.*`, `**/*.test.*`, `**/*.spec.*`, `__tests__/`, `src/test/`.
   - Cita exclusões de "código de produção": extensões doc (`.md`/`.rst`/`.txt`), test patterns, manifestos/config (lista nominal), paths de infra/ci/meta (`.github/`, `.gitlab/`, `.circleci/`, `.azuredevops/`, `infra/`, `deploy/`, `.claude/`, `docs/`).
   - Critério de disparo explícito: ≥1 path de produção em `## Arquivos a alterar` E nenhum path casa test pattern.

3. **Passo 3.5 enriquecido**:
   - `grep -n "Cobertura ausente" skills/run-plan/SKILL.md` retorna 1 ocorrência na enumeração "Gatilhos pré-loop".
   - Total de gatilhos pré-loop listados: 5.
   - "Gatilhos durante execução" e "Gatilhos durante validação manual" inalterados.

4. **Sem regressão em outras seções**:
   - `git diff skills/run-plan/SKILL.md` mostra apenas adições (tabela + passo 3.5); zero remoções.
   - Pré-condições, passo 1, passo 2, passo 3.1-3.4, 3.6-3.7, `## O que NÃO fazer` byte-idênticos a HEAD.

5. **ADR-002 referenciado implicitamente**:
   - Nova entrada cabe na sub-seção "Detecção de warnings pré-loop", que já cita ADR-002 no parágrafo introdutório. Sem nova menção textual necessária.

## Verificação manual

**Smoke test em uso real** (pós-merge+reload): construir 5 planos fictícios em `docs/plans/` para exercitar cada cenário:

1. **Dispara**: plano altera `src/foo.py` sem listar teste → mensagem `"capturei para verificação: cenário sem cobertura nova exercitada — ..."` aparece na fase pré-loop; skill prossegue criando worktree; gate final lista entrada em `## Pendências de validação` do plano.

2. **Suprime (teste presente)**: plano altera `src/foo.py` E lista `tests/test_foo.py` → silêncio total na fase pré-loop.

3. **Suprime (doc-only)**: plano altera apenas `docs/algo.md` → silêncio (paths são doc).

4. **Suprime (config-only)**: plano altera apenas `pyproject.toml` ou `package.json` → silêncio (paths são manifesto).

5. **Falso positivo aceito**: plano altera `src/foo.py` em refactor puro sem teste novo → warning dispara conforme heurística; operador exercita "descarta esse" no diálogo do passo 3.5; entrada não aparece em `## Pendências de validação` do plano.

**Critério de aceitação**: cenários (1)-(5) validados em invocação real do `/run-plan`.

## Notas operacionais

- Mudança bounded a `skills/run-plan/SKILL.md`; sem cross-cutting com `/triage` ou `templates/plan.md` (caminho A escolhido).
- Falsos positivos esperados em refactor puro/internal cleanup — operador filtra no momento da materialização (passo 3.5 já permite "descarta esse" entre aviso e materialização). Se taxa de descarte virar dolorosa em uso real, reabrir para considerar caminho B (anotar cobertura no plano via `/triage`).
- ADR-002 não exige novo ADR — proposta está dentro dos critérios (a)(b)(c) já documentados; passa pelo gatilho de revisão "5º+ warning" sem mudar doutrina.
