# Plano — marketplace prep cleanup batch 1

## Contexto

Pós-publicação no Claude Code marketplace (PR #49 mergeado em 2026-05-10) sobraram 8 itens editoriais/cosméticos identificados no relatório de pré-publicação, capturados em `## Próximos` como `marketplace prep #1` a `#8`. Este plano endereça o **batch 1** — 5 itens trivial-cleanup que devem fechar antes da publicação ampla:

- **#1** (bloqueador): `$schema` e `description` top-level em `marketplace.json` são rejeitados pelo validador oficial `claude plugin validate` (ambos "Unrecognized keys").
- **#2** (limpeza): `docs/audits/runs/` vazio tracked.
- **#3** (editorial datado): `docs/install.md` linha 33 ("`claude plugin validate` ainda não existe...") está obsoleta — o subcomando existe.
- **#4** (doc clara): Python 3.10+ não documentado em `docs/install.md` apesar de hooks usarem PEP 604.
- **#5** (editorial sutil): keywords/tags em manifests atraem público errado.

**Verificações empíricas feitas no `/triage` (2026-05-10):**

- `curl -sIL https://anthropic.com/claude-code/marketplace.schema.json` → 302 → `https://www.anthropic.com/claude-code/marketplace.schema.json` → **404**. URL não é canônico.
- `claude plugin validate .claude-plugin/marketplace.json` → ✘ "Unrecognized keys: $schema, description". Falha de validação real, não warning.
- `claude plugin validate .claude-plugin/plugin.json` → ✔ passed. Sem ajustes nesse arquivo (exceto keywords no Bloco 4).
- `claude plugin validate --help` retorna usage real → subcomando existe e é a ferramenta canônica de validação.

**Implicação editorial:** o refresh da `description` top-level feito no Bloco 5 do PR #49 não tem efeito funcional — campo é ignorado pelo validador. Trabalho não é regressão (foi melhoria da string), mas o campo todo precisa sair agora. Decisão registrada em [ADR-012](../decisions/ADR-012-idioma-artefatos-discoverability-landing.md) sobre idioma fica intacta — `plugins[0].description` (interno) continua em EN e segue ratificado pelo ADR.

**Drift adicional descoberto na revisão pré-execução** (`design-reviewer` 2026-05-10): a `description` em `plugin.json` (e em `marketplace.json` plugins[0]) ainda menciona "Python testing scaffolder", criando sinal misto após o Bloco 4 remover `python`/`pytest`/`testing` das keywords. Bloco 4 ganha sub-edit endereçando o drift no mesmo passo, em vez de empurrar para follow-up genérico.

**Sem `**Linha do backlog:**`:** plano endereça 5 linhas distintas em `## Próximos`; mecanismo de matching textual do `/run-plan` opera sobre 1 string. Skip silente da transição automática; transição manual no done — plano prescreve consolidação em 1 bullet (ver `## Notas operacionais`).

## Resumo da mudança

**Entra:**

1. **`marketplace.json` saneado** — remover `$schema` (URL 404) e `description` top-level (key não reconhecida). `plugins[0].description` permanece (segue ADR-012 em EN), mas ganha sub-edit no Bloco 4 (trocar "Python testing scaffolder" por descrição alinhada às keywords novas). Resultado: `claude plugin validate` retorna ✔.
2. **`docs/audits/runs/README.md` criado** — explica propósito do diretório (registros de execuções de auditorias reutilizáveis dos prompts em `docs/audits/`). Diretório deixa de ser vazio-tracked.
3. **`docs/install.md` atualizado** — (a) seção "Validação" cita `claude plugin validate <path>` como ferramenta canônica em vez da nota datada sobre o subcomando "ainda não existir"; (b) "Pré-requisitos no projeto consumidor" ganha menção a Python 3.10+ exigido pelos hooks (sintaxe PEP 604 em `run_pytest_python.py` e `block_gitignored.py`).
4. **Keywords/tags em manifests substituídas** + **descriptions realinhadas**:
   - Keywords antes: `["workflow", "yagni", "scaffold", "adr", "planning", "code-review", "debugging", "diagnosis", "python", "pytest", "testing"]`
   - Keywords depois: `["workflow", "yagni", "adr", "decision-records", "planning", "code-review", "doc-review", "design-review", "debugging", "worktree", "self-gated-hooks"]`
   - `plugin.json` `description`: trocar `Python testing scaffolder` por `stack-aware test scaffolder (Python today)` — comunica feature sem implicar plugin Python-only.
   - `marketplace.json` plugins[0].description: mesma troca + atualizar `YAGNI/QA/security reviewers` para `YAGNI/QA/security/doc/design reviewers` (drift secundário — lista atual omite doc-reviewer e design-reviewer adicionados depois).

**Fica de fora:**

- Itens `marketplace prep #6` (CI workflow), `#7` (walkthrough visual), `#8` (reorganização repo) — Lotes 2, 3, 4 separados.
- Description longa ou rich na top-level do marketplace.json — schema oficial não suporta; campo é apenas removido, não substituído.
- `docs/install.md` reestruturação ampla — só os 2 edits cirúrgicos de #3 e #4. Reescrita do install fica para outro `/triage` se justificar.

## Arquivos a alterar

### Bloco 1 — `marketplace.json` saneamento {reviewer: code,doc}

JSON é estrutura + prosa. `code-reviewer` cobre integridade do JSON; `doc-reviewer` cobre drift se algum doc citar `$schema` removido. Combinação justificada (1 arquivo, 2 mudanças correlacionadas, drift cross-cutting concreto a verificar).

- `.claude-plugin/marketplace.json`:
  - Remover linha 2: `"$schema": "https://anthropic.com/claude-code/marketplace.schema.json",` — URL 404.
  - Remover linha 4: campo `description` top-level — `claude plugin validate` rejeita como "Unrecognized key".
  - **Não tocar** `plugins[0].description` neste bloco (Bloco 4 ajusta).
  - Preservar `name`, `owner`, `plugins` array, e o resto da estrutura.
  - Validar após edit: `claude plugin validate .claude-plugin/marketplace.json` deve retornar ✔.

Drift cross-cutting a checar: `grep -r "marketplace.schema" .` — se algum `.md`, prosa de skill, ou outro arquivo cita o URL removido, atualizar/remover referência no mesmo bloco.

### Bloco 2 — `docs/audits/runs/README.md` (novo) {reviewer: doc}

- `docs/audits/runs/README.md`: criar arquivo curto (5-10 linhas) explicando propósito do diretório.
  - Conteúdo aproximado: "Registros de execuções de auditorias reutilizáveis. Cada arquivo corresponde a uma execução de um dos prompts em `docs/audits/*.md` (`prose-tokens.md`, `architecture-logic.md`), com data e foco, para arqueologia editorial. Arquivos individuais ficam fora deste README; este apenas documenta o propósito do diretório para evitar diretório vazio-tracked."
  - Idioma: PT-BR (operativo, segue Convenção de idioma).

### Bloco 3 — `docs/install.md` (claude plugin validate + Python 3.10+) {reviewer: doc}

Dois edits cirúrgicos no mesmo arquivo.

- `docs/install.md`:
  - **Edit 1 — seção "Validação" (linhas 32-46):** substituir a frase "claude plugin validate ainda não existe como subcomando estável (até abril de 2026). Para validar localmente:" por algo como: "Use `claude plugin validate <path>` (ferramenta oficial) — aceita o path do `plugin.json` ou `marketplace.json`. Para validações adicionais não cobertas pelo subcomando, segue o checklist abaixo:" Manter os 10 itens do checklist abaixo intactos (smoke test detalhado continua útil).
  - **Edit 2 — seção "Pré-requisitos no projeto consumidor" (linha ~69):** após o parágrafo que menciona "`python3` no `PATH`", adicionar: "**Python 3.10+** é exigido pelos hooks (`run_pytest_python.py` e `block_gitignored.py` usam sintaxe PEP 604 — `str | None`). Versões anteriores falham com SyntaxError ao executar o hook." Frase única, não-disruptiva.
  - Preservar todas as outras seções e referências.

### Bloco 4 — keywords/tags + descriptions realinhadas {reviewer: code,doc}

JSON estrutural + drift de prosa concreto (descriptions citando "Python testing scaffolder" descasariam das keywords novas se ajustadas isoladamente). Combinação justificada.

- `.claude-plugin/plugin.json`:
  - Substituir array `keywords` (linha 10) pela lista nova: `["workflow", "yagni", "adr", "decision-records", "planning", "code-review", "doc-review", "design-review", "debugging", "worktree", "self-gated-hooks"]`.
  - Editar `description`: trocar `Python testing scaffolder` por `stack-aware test scaffolder (Python today)`. Resto da string preservado.
  - Não tocar `name`, `version`, `author`, `homepage`.
  - Validar após edit: `claude plugin validate .claude-plugin/plugin.json` deve retornar ✔.

- `.claude-plugin/marketplace.json`:
  - Substituir o array `plugins[0].tags` (linha 26) pela mesma lista. Manter sincronia com `keywords` do `plugin.json` — vocabulário de busca compartilhado entre os dois manifests.
  - Editar `plugins[0].description`: (a) trocar `Python testing scaffolder` por `stack-aware test scaffolder (Python today)`; (b) atualizar `YAGNI/QA/security reviewers` para `YAGNI/QA/security/doc/design reviewers` — lista atual omite doc-reviewer e design-reviewer adicionados depois (drift secundário descoberto na revisão pré-execução).
  - Validar após edit: `claude plugin validate .claude-plugin/marketplace.json` deve retornar ✔ (junto com saneamento do Bloco 1).

## Verificação end-to-end

- `claude plugin validate .claude-plugin/plugin.json` → ✔ Validation passed
- `claude plugin validate .claude-plugin/marketplace.json` → ✔ Validation passed
- `python3 -m json.tool .claude-plugin/plugin.json > /dev/null && python3 -m json.tool .claude-plugin/marketplace.json > /dev/null` → exit 0 em ambos
- `docs/audits/runs/README.md` existe, > 50 chars, descreve propósito do diretório
- `docs/install.md`: seção "Validação" cita `claude plugin validate`; "Pré-requisitos" menciona Python 3.10+
- `grep -r "Python testing scaffolder" .` → vazio (descriptions realinhadas em Bloco 4)
- `grep -r "marketplace.schema" .` → vazio (URL 404 removido em Bloco 1)
- `grep "YAGNI/QA/security reviewers" .claude-plugin/marketplace.json` → vazio (lista de reviewers atualizada)
- `git log` mostra 4 commits coerentes (1 por bloco)

## Notas operacionais

- **Ordem dos blocos com 1 acoplamento.** Sequência prescrita: (1) `marketplace.json` saneamento → (2) `docs/audits/runs/README.md` → (3) `docs/install.md` → (4) keywords/tags + descriptions. Bloco 1 primeiro porque é o bloqueador funcional. **Bloco 4 valida-OK depende de Bloco 1** (`claude plugin validate marketplace.json` ainda retorna ✘ enquanto `$schema`/`description` top-level estiverem lá). Demais ordens entre Blocos 2, 3 e 4 são livres.
- **Sem `**Linha do backlog:**`:** plano endereça 5 linhas distintas em `## Próximos`. **Transição prescrita no done — consolidar em 1 bullet** em `## Concluídos` no formato:
  ```
  - plugin: marketplace prep batch 1 (itens #1-#5) concluído — saneamento marketplace.json (#1), docs/audits/runs/README (#2), docs/install.md atualizado para claude plugin validate (#3) + Python 3.10+ (#4), keywords/tags + descriptions realinhadas (#5).
  ```
  E **remover** as 5 linhas de `## Próximos`. Strings exatas para grep no done:
  - `plugin: marketplace prep #1 (bloqueador) — verificar canonicidade do`
  - `plugin: marketplace prep #2 (limpeza) — `docs/audits/runs/` vazio tracked`
  - `plugin: marketplace prep #3 (editorial datado) — `docs/install.md` linha 33`
  - `plugin: marketplace prep #4 (doc clara) — adicionar requisito Python 3.10+`
  - `plugin: marketplace prep #5 (editorial sutil) — keywords/tags em `plugin.json` e `marketplace.json``
  Razão para consolidar em vez de 5 bullets em Concluídos: 5 itens são partes do mesmo batch editorial; arqueologia futura quer "o batch fechou em PR #X", não 5 entries pulverizadas. Bloco extra do `/run-plan` §3.4 vai precisar ser manual (matching automático não cobre 5→1) — operador edita `BACKLOG.md` no fim, antes do gate de publicação.
- **`design-reviewer` já passou** no plano durante este `/triage` (sessão 2026-05-10) — findings consolidados nas direções dos blocos. `/run-plan` **não precisa redisparar** `design-reviewer`; `code-reviewer` (Blocos 1 e 4) e `doc-reviewer` (todos) por bloco cobrem o necessário.
- **Bloco 1 destaque editorial.** Remover o campo `description` top-level reverte (em efeito funcional) o trabalho do Bloco 5 do PR #49. Não é regressão de string (a string nova era melhor que a antiga), mas o campo todo deixa de existir. Vale comunicar no commit message do Bloco 1.
- **Bloco 4 escopo expandido vs plano original.** Sub-edit das descriptions (em ambos manifests) e atualização da lista de reviewers em marketplace.json plugins[0].description foram adicionados após revisão do `design-reviewer` que flagou drift (descriptions citando "Python testing scaffolder" descasariam das keywords novas) e drift secundário (lista de reviewers desatualizada). Não é escopo creep — é fechamento do mesmo eixo editorial em uma única passagem.
