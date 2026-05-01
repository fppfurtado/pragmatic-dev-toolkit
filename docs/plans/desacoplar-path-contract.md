# Plan: v0.4.0 — desacoplar path contract via "Resolução de papéis"

## Contexto

O plugin codifica um workflow flat-e-pragmático, mas o path contract atual está acoplado ao layout literal produzido pelo template companion `scaffold-kit`: ~70 ocorrências literais de `IDEA.md`, `docs/domain.md`, `docs/plans/`, `make test`, `BACKLOG.md`, etc. espalhadas por skills, agents e docs. Projetos alinhados à filosofia mas com layout ligeiramente diferente (`docs/glossary.md` em vez de `docs/domain.md`, `uv run pytest` em vez de `make test`, decisões em `decisions/`) ficam fora do contrato — apesar da filosofia ser perfeitamente aplicável.

A Pendência 3 da execução do plano `gap-bifurcacao-arquitetural` expôs essa rigidez ao vivo: o próprio repositório do plugin é meta-tool sem Makefile, e `/run-plan` precisou desviar do contrato. A correção certa não é só flexibilizar `make test` — é **generalizar o conceito**: skills passam a consumir **papéis** (gate de testes, linguagem ubíqua, plano, decisão, backlog, direção de produto, peculiaridades de integração), não paths literais. O path contract atual permanece como **convenção default por papel**; projetos com layout diferente declaram variantes em um bloco YAML no CLAUDE.md do projeto consumidor.

Mudança faseada de propósito: v0.4.0 introduz o mecanismo + porta `/new-feature` e `/run-plan`; v0.4.1 e v0.5.0 estendem o pattern aos demais componentes depois de feedback de uso real.

## Resumo da mudança

Escopo do v0.4.0 (estritamente):

1. **`docs/philosophy.md`**: nova seção `## Resolução de papéis` com protocolo `probe canonical → CLAUDE.md config → ask` e gramática do bloco de config. Tabela "Path contract" passa a ser apresentada como **convenção default por papel**.
2. **`/new-feature`**: portar para o protocolo. Pré-condições passam a referenciar papéis; resposta "não temos" é válida e a skill segue sem o input.
3. **`/run-plan`**: portar especificamente o test gate (`make test` → `test_command` resolvido) + plan path. `.worktreeinclude` e `.worktrees/<slug>/` ficam literais (introduzidos pelo plugin, não project-config).
4. **Docs**: `install.md` e `README.md` atualizados com exemplo do bloco de config; `CHANGELOG.md` ganha entry `[0.4.0]`.
5. **Bumps**: `plugin.json` e `marketplace.json` para `0.4.0`.

**Fora deste release** (próximas iterações, mencionadas só para deixar o escopo claro):
- v0.4.1: `/gen-tests-python` + agents (`qa-reviewer`, `security-reviewer`, `code-reviewer` — referências a `docs/domain.md`/`docs/design.md` viram referências indiretas a papéis).
- v0.5.0: `/new-adr` infere formato de numeração dos ADRs existentes (3-dígitos, 4-dígitos, sem padding).
- Hooks (`block_env.py`, `run_pytest_python.py`) **nunca mudam**: `.env*` e `pyproject.toml` são markers universais por ecossistema, não project-config.

Backwards compat: **100% preservado**. Projeto que segue canonical paths e não tem CLAUDE.md config block continua funcionando zero-config exatamente como em v0.3.1.

## Arquivos a alterar

### Bloco 1 — `docs/philosophy.md` {revisor: code}

Três edits, em ordem:

1. **Reframe da seção `## Path contract`**: substituir o lead-in "As skills deste plugin assumem que o projeto segue estas convenções de path" por "As skills consomem **papéis**, não paths. A tabela abaixo lista a convenção default por papel — projetos com layout diferente declaram variantes via bloco de config (próxima seção)". A tabela ganha coluna `Papel` à esquerda; a coluna atual `Path` vira `Default`. Nada removido — só reframed.

2. **Nova subseção `## Resolução de papéis`** (logo após Path contract, antes de "Convenção de naming"). Define o protocolo declarativamente:
   - Skill probes o path canônico exato (sem fuzzy — `README.md` não é assumido como `IDEA.md`).
   - Se ausente, lê CLAUDE.md do projeto consumidor procurando declaração no bloco `<!-- pragmatic-toolkit:config -->`.
   - Se ainda ausente e o papel é necessário pra skill, pergunta ao operador com resposta tri-state: `path | não temos | outro path`. Resposta "não temos" é válida — skill segue sem aquele input se for opcional, ou para com gap report se for obrigatório.
   - Ao final da invocação, **uma única oferta** "registrar essa resolução no CLAUDE.md? (s/n)". `n` = perguntará de novo na próxima.
   - Drift detection: se o canonical existe E o CLAUDE.md declara variante diferente, skill flagga inconsistência ao operador.

3. **Nova subseção `## Bloco de configuração no CLAUDE.md`** (após Resolução de papéis). Define a gramática:

   ````markdown
   ## Pragmatic Toolkit
   <!-- pragmatic-toolkit:config -->
   ```yaml
   paths:
     product_direction: IDEA.md          # default: IDEA.md
     ubiquitous_language: docs/domain.md # default: docs/domain.md
     design_notes: docs/design.md        # default: docs/design.md
     decisions_dir: docs/decisions/      # default: docs/decisions/
     plans_dir: docs/plans/              # default: docs/plans/
     backlog: BACKLOG.md                 # default: BACKLOG.md
   test_command: make test               # default: make test
   ```
   ````

   Semântica: chave ausente = canonical default; valor `null` (ou explicitamente `false`) = "não usamos esse papel". Chaves reservadas: `paths.*` e `test_command` (no v0.4.0). Chaves desconhecidas no bloco são ignoradas (forward-compat para futuras releases).

### Bloco 2 — `skills/new-feature/SKILL.md` {revisor: code}

Portar do path-literal para papéis. Edits:

- **Pré-condições** (linha 14): substituir lista enumerativa de paths por "para cada papel necessário (`product_direction`, `ubiquitous_language`, `backlog`), aplicar Resolução de papéis (ver `docs/philosophy.md`). Resposta 'não temos' é válida — skill segue sem aquele input para papéis informacionais (`design_notes`, ADRs); skill para com gap report apenas se `backlog` ou `plans_dir` resolvem para 'não temos' (esses são onde a skill grava saída)".
- **Step 1 "Carregar contexto mínimo"** (linhas 27-37): cada item da lista de leitura passa a usar o path resolvido pelo papel correspondente. Itens 1-5 (`IDEA.md`, `docs/domain.md`, `BACKLOG.md`, `docs/design.md`, `docs/decisions/`) ficam como exemplos das convenções default, com referência explícita "(papel: `product_direction`)" etc.
- **Step 4 "Produzir os artefatos"** (linhas 67-74): paths de plano (`docs/plans/<slug>.md`) e backlog (`BACKLOG.md`) consultados via `paths.plans_dir` + `paths.backlog`.
- **Adicionar parágrafo curto** logo no início do "Step 1": "Os paths abaixo são as convenções default; quando o projeto declara variantes (ver Resolução de papéis em `docs/philosophy.md`), usar os paths declarados". Não duplicar protocolo.

### Bloco 3 — `skills/run-plan/SKILL.md` {revisor: code}

Portar test gate + plan path. Edits:

- **Pré-condição 1** (linha 24): `docs/plans/<slug>.md` → `<plans_dir>/<slug>.md` onde `plans_dir` resolve via Resolução de papéis (default: `docs/plans/`).
- **Pré-condição 2** (linha 25): `make test` está verde → "o gate automático de testes do projeto está verde. Default: `make test`. Variante: `test_command` declarado no CLAUDE.md (ex.: `uv run pytest`, `npm test`). Em projetos sem suite automatizada (meta-tools, doc-only), `## Verificação end-to-end` do plano substitui o gate — caso de exceção, declarado pelo operador via `test_command: null` ou pela ausência de any test gate".
- **Step 1 setup**: `git worktree add .worktrees/<slug>` permanece literal (path interno do skill). `.worktreeinclude` permanece literal. Sync de dependências passa a respeitar stack do projeto (já era).
- **Step 3.2 e Step 4.1** (`make test` no loop e gate final): ambos usam `test_command` resolvido. Quando `test_command` é null/ausente E plano tem `## Verificação end-to-end`, esses passos viram inspeção textual conforme o plano define.
- **`.claude/agents/` lookup** (linha 52): permanece literal — convenção Claude Code, já é opcional.
- **Adicionar parágrafo curto** no Step 1, antes de "Sanity check de escopo": "Paths e comandos abaixo seguem a Resolução de papéis (ver `docs/philosophy.md`)".

### Bloco 4 — `docs/install.md` + `README.md` {revisor: code}

- **`install.md` (edit)**: seção "Pré-requisitos no projeto consumidor" passa a explicar que canonical paths são apenas default. Adicionar bloco de exemplo do `<!-- pragmatic-toolkit:config -->` em CLAUDE.md mostrando 2-3 variantes típicas (test_command, ubiquitous_language em path alternativo). Adicionar smoke test à seção "Validação": "Em projeto com bloco de config declarado, invocar `/new-feature` e confirmar que skill consulta o path declarado, não o canonical".
- **`README.md` (edit)**: parágrafo curto na seção "Filosofia" ou nova seção curta após "O que vem": "Funciona em qualquer projeto alinhado à filosofia, não só os gerados por `scaffold-kit`. Layout diferente é declarado via bloco de config no CLAUDE.md do projeto. Detalhe em [`docs/philosophy.md`](docs/philosophy.md)". Sem expansão.

### Bloco 5 — `CHANGELOG.md` {revisor: code}

Adicionar entry `## [0.4.0] - <YYYY-MM-DD>` no topo (após cabeçalho, antes de `[0.3.1]`):

```markdown
### Changed
- Path contract reframed como **convenção default por papel** (`docs/philosophy.md`). Skills consomem papéis, não paths literais. Backwards compat preservado para projetos que seguem canonical paths.

### Added
- Mecanismo "Resolução de papéis" em `docs/philosophy.md`: protocolo probe→CLAUDE.md config→ask, com bloco YAML fenced (`<!-- pragmatic-toolkit:config -->`) como mecanismo de declaração.
- Skill `/new-feature` e `/run-plan` portados para o protocolo. Test gate em `/run-plan` passa a aceitar `test_command` declarado (ex.: `uv run pytest`, `npm test`).

### Notes
- `/gen-tests-python`, agents (qa-reviewer/security-reviewer/code-reviewer) e `/new-adr` permanecem com referências literais ao path contract — serão portados em v0.4.1 (skills/agents) e v0.5.0 (numbering inferido de `/new-adr`).
- Hooks (`block_env`, `run_pytest_python`) inalterados — markers universais por ecossistema, não project-config.
```

### Bloco 6 — `.claude-plugin/plugin.json` + `marketplace.json` {revisor: code}

- **`plugin.json` (edit)**: bump `"version": "0.3.1"` → `"0.4.0"`. Atualizar `description` para mencionar "configurable path contract via CLAUDE.md".
- **`marketplace.json` (edit)**: bump `plugins[0].version` análogo. Atualizar `description` no item de plugin.

## Verificação end-to-end

Inspeção textual + parse (meta-tool sem `make test`):

1. `grep -n "Resolução de papéis" docs/philosophy.md` → 1 ocorrência (cabeçalho da subseção).
2. `grep -n "pragmatic-toolkit:config" docs/philosophy.md` → 1 ocorrência (no exemplo da gramática).
3. `grep -n "Resolução de papéis" skills/new-feature/SKILL.md skills/run-plan/SKILL.md` → 1 referência em cada (sem duplicar protocolo).
4. `grep -cn "make test" skills/run-plan/SKILL.md` — todas as ocorrências restantes devem ser exemplos default ("default: `make test`"), não exigência literal.
5. `python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])"` → `0.4.0`. Idem `marketplace.json`.
6. Bloco YAML de exemplo em philosophy.md parseia: extrair conteúdo entre fence ` ```yaml` e ` ``` ` da subseção "Bloco de configuração" e validar com `python3 -c "import yaml, sys; yaml.safe_load(sys.stdin.read())"`.
7. `git diff --stat` mostra exatamente 6 arquivos: `docs/philosophy.md`, `skills/new-feature/SKILL.md`, `skills/run-plan/SKILL.md`, `docs/install.md`, `README.md`, `CHANGELOG.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (8, mas blocos 4 e 6 cobrem 2 arquivos cada).

## Verificação manual

Necessária — mecanismo novo, smoke real importa. Três cenários em projetos consumidores reais:

1. **Projeto canonical (sem CLAUDE.md config block)**: usar `h3-finance-agent` ou similar com `IDEA.md`, `BACKLOG.md`, `docs/domain.md`, `Makefile` com `test`. Invocar `/new-feature` e `/run-plan` em fluxo típico. Esperado: comportamento idêntico ao v0.3.1, zero perguntas novas, zero referência a Resolução de papéis no output da skill (a infraestrutura está lá, não dispara porque o canonical é encontrado).

2. **Projeto com variantes declaradas**: criar (ou apontar) projeto com bloco de config no CLAUDE.md declarando `paths.ubiquitous_language: docs/glossary.md` e `test_command: uv run pytest`. Invocar `/new-feature` num pedido que toque domínio: skill deve ler `docs/glossary.md` (não procurar `docs/domain.md`). Invocar `/run-plan` num plano qualquer: gate baseline e per-block deve rodar `uv run pytest`, não `make test`.

3. **Projeto com papel ausente sem declaração**: projeto novo sem `IDEA.md` e sem CLAUDE.md config. Invocar `/new-feature`. Skill deve perguntar onde mora a direção de produto, com tri-state options. Resposta "não temos": skill segue sem o input (papel `product_direction` é informacional). Resposta canonical alternativo (`README.md`): skill usa esse path. Ao final, oferta única "memorizar isso em CLAUDE.md? (s/n)" — `s` adiciona o bloco de config; `n` perguntará de novo na próxima invocação.

Cada smoke é "ok" ou "ajustar redação" — sem ferramenta automatizada para gate. Sem confirmação dos três cenários, não fechar o release.

## Notas operacionais

- **Bump é minor** (0.3.1 → 0.4.0): muda semântica do path contract (de literal para papéis), mas backwards compat 100% preservado. Operadores existentes não precisam ajustar nada — variantes são opt-in.
- **Faseamento explícito**:
  - **v0.4.0** (este plano): mecanismo + `/new-feature` + `/run-plan`.
  - **v0.4.1** (próximo patch): porta `/gen-tests-python` (já está quase no padrão — referencia `docs/domain.md` opcional). Agents (`qa-reviewer`, `security-reviewer`, `code-reviewer`) ganham referências indiretas a papéis em vez de paths literais (ex.: "invariantes documentadas pelo papel `ubiquitous_language` do projeto").
  - **v0.5.0** (próximo minor): `/new-adr` infere formato de numeração dos ADRs existentes (3-dígitos, 4-dígitos, sem padding) em vez de hardcode `ADR-NNN-`.
- **"Resolução de papéis" é declarada uma vez em `philosophy.md` e referenciada por nome nas skills** — não duplicar protocolo entre arquivos. Drift control é o ponto.
- **Probing leniency**: skills probam **só o filename canônico exato**. Sem fuzzy. Probar alternativas (`README.md` para `product_direction`, `docs/glossary.md` para `ubiquitous_language`) é falso-positivo aguardando acontecer — skill assume que `README.md` é direção de produto quando é instalação/uso.
- **Memorização**: pergunta inline → usa resposta na invocação corrente → oferta única ao final de "memorizar". Não auto-grava (operador mantém autonomia sobre CLAUDE.md).
- **Risco de regressão "fail-fast on missing path"**: hoje skills falham explícita e cedo quando path obrigatório não existe. v0.4 mantém esse comportamento via tri-state ("path / não temos / outro path"). "Não temos" para papel obrigatório (ex.: `plans_dir` em `/run-plan`) ainda é gap report explícito.
- **Hooks intocados em todas as fases**: `.env*` (block_env) e `pyproject.toml` (run_pytest_python) são markers universais por ecossistema. Variá-los seria abstração prematura.
- **Plugin não passa CLAUDE.md config a si mesmo** (meta-tool divergence permanece — repo já documenta em CLAUDE.md de forma genérica).
- **Disciplina de execução**: este plano roda via `/run-plan`, mas `pragmatic-dev-toolkit` é meta-tool sem Makefile — aplicar mesma disciplina que v0.3.x: direto na main, micro-commits Conventional Commits (em inglês), um por bloco. Tag `v0.4.0` após smoke verde dos três cenários manuais. `code-reviewer` invocado por bloco antes de cada commit.
