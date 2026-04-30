# Plan: gen-tests-python skill + self-gating pytest hook (v0.2.0)

## Contexto

A v0.1 entregou skills genéricas (`/new-feature`, `/new-adr`, `/run-plan`), o agent `code-reviewer` (rubrica YAGNI) e o hook `block_env` (genérico). Tooling stack-specific ficou de fora — minha proposta inicial era um sub-plugin Python; o operador apontou que isso era over-engineering.

A intuição correta: **skill é invocada pelo usuário**, então o nome carrega o contrato (`gen-tests-python` deixa o acoplamento explícito). **Hook dispara sozinho** em todo projeto onde o plugin estiver instalado, mas pode **se auto-desligar barato** (extensão de arquivo + marcador de stack no projeto). Em ambos os casos, conviver no mesmo plugin sem sub-plugin.

Esta v0.2 codifica o padrão e ship a primeira encarnação dele em Python. Quando aparecer projeto Java, sai um `gen-tests-java` + `format_java.sh` no mesmo plugin sem mexer no que existe.

## Resumo da mudança

1. **Skill `gen-tests-python`** (lift de `h3-finance-agent/.claude/skills/gen-test/SKILL.md` + `h3-finance-agent/.claude/rules/tests.md`, com remoção do mapa RN→módulo).
2. **Hook `run_pytest_python.py`** auto-gated, registrado em `hooks/hooks.json` ao lado de `block_env`.
3. **Documentar a convenção de naming** (`<verb>-<artifact>-<stack>` para skills; `<purpose>_<stack>.py|.sh` para hooks) em `philosophy.md`.
4. **Atualizar `install.md`**: remove o snippet "cole no settings.json do projeto" — o hook agora vem no plugin auto-gated.
5. **Atualizar `README.md`** (linha na tabela de componentes).
6. **Bumps**: `plugin.json` `0.1.0`→`0.2.0`, `marketplace.json` mesma coisa, `CHANGELOG.md` nova entrada.
7. **Tag `v0.2.0`** após merge.

Mudança 100% aditiva. v0.1 surface intacto.

## Arquivos a alterar

### Bloco 1 — skill {revisor: code}

- **`skills/gen-tests-python/SKILL.md`** (novo).
  - Frontmatter: `name: gen-tests-python`, `description: "Gera testes pytest para um módulo de um projeto Python, seguindo as convenções pytest + respx + asyncio_mode auto + tmp_path para SQLite. Use quando o projeto for Python e o usuário pedir testes para um módulo ou função."`.
  - Body: combina o `gen-test/SKILL.md` (passos: ler alvo, mapear invariantes, decidir unit/integration, gerar arquivo, validar) com o `tests.md` (stack: pytest+pytest-asyncio com `asyncio_mode = "auto"`, respx para HTTP, sem mockar SQLite — `tmp_path`; estrutura `tests/unit` rápido + `tests/integration` com marker; nomes em PT alinhados ao vocabulário ubíquo; injeção de data de referência em vez de `datetime.now()`).
  - **Remove**: tabela "módulo → RN" (era específica de h3); substitui por "consulte `docs/domain.md` do projeto e identifique RNs aplicáveis ao alvo".
  - **Remove**: edge cases de Conciliação/OFX/Bot/n8n específicos; substitui por "edge cases típicos por domínio: revisar `docs/design.md` do projeto e cobrir tanto caminho feliz quanto violação de invariante."

### Bloco 2 — hook auto-gated {revisor: security}

- **`hooks/run_pytest_python.py`** (novo).
  - Lê JSON de stdin (`tool_input.file_path`).
  - **Camada 1** (extensão): se não termina com `.py`, exit 0.
  - **Camada 2** (marcador de stack): caminha pelos ancestrais procurando `pyproject.toml`. Se não achar, exit 0.
  - **Camada 3** (trabalho): roda `subprocess.run(["uv", "run", "pytest", "-q", "--no-header"], cwd=root, capture_output=True, text=True)`. Se `uv` não existir, fallback para `python -m pytest`. Imprime as últimas 10 linhas de stdout+stderr **só se** o exit code do pytest for não-zero (mantém o canal limpo no caso feliz).
  - Sempre exit 0 — PostToolUse não deve bloquear hooks subsequentes.
  - **Sem shell injection**: `subprocess.run([...])` com lista, nunca string. `file_path` nunca chega a uma shell.
  - **Não roda no contexto da worktree errada**: usa o ancestral mais próximo do arquivo editado, não o `cwd` do processo Claude (essencial em monorepos).

- **`hooks/hooks.json`** (edit).
  - Adiciona entrada `PostToolUse` com matcher `Edit|Write` apontando para `python3 ${CLAUDE_PLUGIN_ROOT}/hooks/run_pytest_python.py`. Timeout 60s (pytest pode demorar).
  - Mantém o bloco `PreToolUse` existente (`block_env`) intacto.

### Bloco 3 — docs {revisor: code}

- **`docs/philosophy.md`** (edit).
  - Remove o bullet sobre "sub-plugin Python (`pragmatic-dev-toolkit-python`)".
  - Adiciona seção `## Convenção de naming` com a tabela:
    - Genérico: `<purpose>.py|.sh` (ex.: `block_env.py`).
    - Stack-specific (hooks): `<purpose>_<stack>.py|.sh` (ex.: `run_pytest_python.py`).
    - Stack-specific (skills): `<verb>-<artifact>-<stack>` na frontmatter (ex.: `gen-tests-python`).
  - Adiciona parágrafo explicando o padrão de auto-gating triplo (extensão → marcador de stack → toolchain) que torna hooks stack-specific seguros num plugin multi-stack.
- **`docs/install.md`** (edit).
  - Remove o snippet "Snippet opcional: rodar testes após edits Python" (agora vem no plugin).
  - Adiciona uma linha: "`run_pytest_python` é auto-gated — só dispara em arquivos `.py` que estão sob um diretório com `pyproject.toml`."
- **`README.md`** (edit).
  - Adiciona linha `/gen-tests-python` na tabela de componentes.
  - Adiciona linha `run_pytest_python` na tabela.

### Bloco 4 — versionamento {revisor: code}

- **`.claude-plugin/plugin.json`** (edit) — `version: "0.2.0"`.
- **`.claude-plugin/marketplace.json`** (edit) — `version: "0.2.0"` no item de plugin.
- **`CHANGELOG.md`** (edit) — adiciona:

  ```markdown
  ## [0.2.0] - 2026-04-30

  ### Added
  - Skill: `/gen-tests-python` — gera testes pytest para módulos/funções de um projeto Python.
  - Hook: `run_pytest_python` — auto-gated PostToolUse (extensão `.py` + ancestral `pyproject.toml`); roda pytest e imprime saída só em falha.
  - Naming convention para skills e hooks stack-specific (em `docs/philosophy.md`).
  ```

### Bloco 5 — release manual

- Merge para `main` (sem branch separada — repo solo, mudança aditiva, smoke verde).
- `git tag v0.2.0 -m "v0.2: gen-tests-python skill + self-gating pytest hook"` + `git push origin v0.2.0`.

## Verificação end-to-end

1. JSONs parseiam: `python3 -c "import json; json.load(open('.claude-plugin/plugin.json'))"` (e marketplace.json, hooks.json).
2. Hook auto-gating (matriz):
   ```bash
   tmp=$(mktemp -d) && touch "$tmp/pyproject.toml" && touch "$tmp/foo.py"
   # Camada 1 (não Python): expect silent
   echo '{"tool_input":{"file_path":"/foo/bar.go"}}' | python3 hooks/run_pytest_python.py
   # Camada 2 (Python sem pyproject ancestral): expect silent
   echo '{"tool_input":{"file_path":"/tmp/loose.py"}}' | python3 hooks/run_pytest_python.py
   # Camada 3 (Python com pyproject): expect pytest a rodar (output só se falhar)
   echo '{"tool_input":{"file_path":"'$tmp'/foo.py"}}' | python3 hooks/run_pytest_python.py
   ```
3. Frontmatter da skill: `python3` regex check que `skills/gen-tests-python/SKILL.md` tem `name: gen-tests-python` e `description:` válida.
4. `git diff --stat` mostra apenas os blocos esperados (sem drift).

## Verificação manual

Necessária — comportamento real depende do runtime do Claude Code.

1. `/plugin install pragmatic-dev-toolkit@fppfurtado-pragmatic-dev-toolkit --scope project` num projeto Python (ex.: clone fresco da `h3-finance-agent`).
2. Editar um `.py` qualquer → expectativa: pytest roda em background; saída no canal só se quebrou algo.
3. `/gen-tests-python src/movimentos/registrar.py` → expectativa: skill propõe arquivo de teste com pytest+respx, identifica RNs do `docs/domain.md`, gera em `tests/unit/test_registrar.py`.
4. Instalar o mesmo plugin num projeto **não-Python** (ex.: clone fresco do `scaffold-kit` em si, que é Python mas SEM `tests/unit` real — ou um repo qualquer Markdown). Editar arquivo → expectativa: hook silente, sem ruído.
5. Confirmar manual: `/plugin list` mostra v0.2.0; `gen-tests-python` aparece nas skills disponíveis.

Sem confirmação dos passos acima, não fechar o release.

## Notas operacionais

- **Sem branch separada.** Plugin é solo, mudança aditiva, smoke verde antes do tag. Direto na `main` em micro-commits Conventional Commits (um por bloco).
- **Tempo do hook.** Timeout 60s parece largo, mas pytest em projeto médio pode passar de 10s. Em projeto sem suíte (rendered scaffold-kit), a chamada termina em ~200ms (pytest detecta nada e sai). Aceitável.
- **Output ergonomics.** Output só em falha — silêncio no caso feliz mantém o transcript limpo. Mesmo padrão do hook inline original em `h3-finance-agent`, mas com gating mais robusto (camadas 1+2).
- **Anti-padrão a evitar:** flags / env vars para desligar hooks individuais. Se um projeto não quer, não instala o plugin nele. Plugin é project-scope-installable; user-scope é opcional.
- **Próxima skill stack-specific.** Quando aparecer projeto Java, repetir o padrão: `gen-tests-java` (skill com lift de convenções JUnit+AssertJ+Mockito+WireMock) e `run_gradle_test_java.sh` (hook auto-gated por extensão `.java|.kt` + ancestral `build.gradle*` ou `pom.xml`).
