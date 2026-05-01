# Changelog

All notable changes to this plugin are documented here. Format inspired by [Keep a Changelog](https://keepachangelog.com/).

## [0.8.0] - 2026-05-01

### Changed
- Agent `security-reviewer` generalizado para qualquer tipo de sistema (web, CLI, desktop, mobile, embedded, library, pipeline, IaC). Critérios passam a ser tratados como **princípios** que se manifestam diferente conforme stack: "Chamadas HTTP externas" vira "I/O externo" (qualquer I/O bloqueante — RPC, DB, file lock, socket, subprocess); "Tokens em URLs em vez de headers" generaliza para segredos em qualquer canal inseguro (argv visível, env herdada, query string); validação de entrada cobre fronteiras adicionais (IPC, deserialização, callback de SDK, stdin) e classes de injeção além de SQL (shell, path traversal, format string, deserialização unsafe, log injection).

### Added
- Nova seção "Privilégios e permissões" no `security-reviewer`: least-privilege em escalation, capability grants, scopes OAuth, roles IAM, manifest permissions, ACLs e entitlements.
- Frontmatter `description` do agent ganha pista explícita de aplicabilidade ("qualquer tipo de sistema") para evitar leitura como agent só-web. CLAUDE.md atualizado em paralelo.

### Notes
- Backwards compat preservado: diffs antes cobertos continuam cobertos. A superfície de detecção apenas expandiu.

## [0.7.0] - 2026-05-01

### Changed
- Skill `/run-plan` passa a seguir a **convenção de commits do projeto consumidor** ao gerar micro-commits. Detecção em três níveis: política explícita no projeto (CLAUDE.md, `CONTRIBUTING.md`, etc.) → padrão observado em `git log` → default canonical Conventional Commits em inglês. Backwards compat preservado: projetos sem política explícita e com histórico já em CC inglês mantêm comportamento idêntico ao v0.6.0.

### Added
- Princípio "Convenção de commits" em `docs/philosophy.md`: protocolo de detecção em três níveis, espelhando o pattern da Convenção de idioma.

### Notes
- Política de "um micro-commit por bloco" permanece invariante. `--amend`/rebase de commits de blocos já fechados continuam proibidos; emendar o último commit do bloco corrente passa a ser exceção localizada (typo, arquivo esquecido), não regra.

## [0.6.0] - 2026-05-01

### Changed
- Skills (`/new-feature`, `/new-adr`, `/run-plan`, `/gen-tests-python`) e agents (`code-reviewer`, `qa-reviewer`, `security-reviewer`) passam a **adaptar-se ao idioma do projeto consumidor** — prosa, headers de templates, nomes de teste e relatórios de revisão espelham o idioma já em uso. Default canonical: PT-BR (origem do toolkit). Backwards compat preservado para projetos PT-BR.
- `/run-plan` faz matching semântico dos headers de plano em vez de exigir literais PT-BR (`## Files to change` / `## Arquivos a alterar`, etc., aceitos como equivalentes).

### Added
- Princípio "Convenção de idioma" em `docs/philosophy.md`: idioma do projeto define a prosa; nomes de agents, frontmatter, paths, código e commits permanecem em inglês.

### Notes
- `CLAUDE.md` deste repo continua dizendo PT-BR — a regra do plugin é "espelhar o projeto consumidor", e o projeto consumidor neste caso (o próprio repo do plugin) opera em PT.

## [0.5.0] - 2026-05-01

### Changed
- Skill `/new-adr` consome agora o papel `decisions_dir` (default: `docs/decisions/`) em vez de path literal.
- Skill `/new-adr` passa a **inferir o formato de numeração** dos ADRs existentes no diretório resolvido: 3-dígitos padded (canonical), 4-dígitos padded ou sem padding. Diretório vazio mantém o default canonical (3-dígitos). Formatos mistos no diretório são flaggados ao operador antes da criação do novo ADR.

### Notes
- Bump minor: comportamento de numeração muda em projetos que usam variantes (4-dígitos ou sem padding) — antes a skill forçaria 3-dígitos. Backwards compat preservado para projetos com 3-dígitos.

## [0.4.1] - 2026-05-01

### Changed
- Skill `/gen-tests-python` e agents `qa-reviewer`, `security-reviewer`, `code-reviewer` passam a referenciar **papéis** (`ubiquitous_language`, `design_notes`, `decisions_dir`) ao invés de paths literais (`docs/domain.md`, `docs/design.md`, `docs/decisions/`). Default canonical citado entre parênteses para legibilidade. Backwards compat preservado.

## [0.4.0] - 2026-05-01

### Changed
- Path contract reframed como **convenção default por papel** (`docs/philosophy.md`). Skills consomem papéis (`product_direction`, `ubiquitous_language`, `design_notes`, `decisions_dir`, `plans_dir`, `backlog`, `test_command`), não paths literais. Backwards compat 100% preservado para projetos que seguem canonical paths.

### Added
- Mecanismo "Resolução de papéis" em `docs/philosophy.md`: protocolo `probe canonical → consultar bloco no CLAUDE.md → perguntar ao operador (tri-state)`, com bloco YAML fenced sob marcador HTML `<!-- pragmatic-toolkit:config -->` como mecanismo de declaração de variantes.
- Drift detection: skill flagga inconsistência ao operador quando canonical existe E CLAUDE.md declara variante diferente.
- Skills `/new-feature` e `/run-plan` portadas para o protocolo. Test gate em `/run-plan` passa a aceitar `test_command` declarado (ex.: `uv run pytest`, `npm test`, `cargo test`).
- `docs/install.md` e `README.md` documentam o bloco de config com exemplo de variantes típicas.

### Notes
- `/gen-tests-python`, agents (`qa-reviewer`, `security-reviewer`, `code-reviewer`) e `/new-adr` permanecem com referências literais ao path contract — serão portados em v0.4.1 (skills/agents) e v0.5.0 (numbering inferido em `/new-adr`).
- Hooks (`block_env`, `run_pytest_python`) inalterados — `.env*` e `pyproject.toml` são markers universais por ecossistema, não project-config.

## [0.3.1] - 2026-05-01

### Added
- Skill `/new-feature`: gap "Bifurcação arquitetural" no checklist + exceção à regra "1-2 perguntas" quando o pedido admite múltiplas implementações materialmente diferentes.
- Princípio "Nomear bifurcações arquiteturais" em `docs/philosophy.md`.

## [0.3.0] - 2026-04-30

### Added
- Agent: `qa-reviewer` — princípios de cobertura de testes (caminho feliz, invariantes, edge cases, mock vs real). Stack-agnóstico.
- Agent: `security-reviewer` — credenciais, validação de entrada, HTTP externo, dados sensíveis, invariantes em ADRs. Stack-agnóstico.
- Naming convention para agents documentada em `docs/philosophy.md` (critério: gera/executa = força sufixo; revisa princípios = não força).

## [0.2.1] - 2026-04-30

### Changed
- `plugin.json` and `marketplace.json` metadata refreshed to mention `/gen-tests-python` and the pytest hook; keywords/tags now include `python`, `pytest`, `testing` for marketplace discovery.

## [0.2.0] - 2026-04-30

### Added
- Skill: `/gen-tests-python` — gera testes pytest para módulos/funções de um projeto Python.
- Hook: `run_pytest_python` — auto-gated PostToolUse (extensão `.py` + ancestral `pyproject.toml`); roda pytest e imprime saída só em falha.
- Naming convention para skills e hooks stack-specific (em `docs/philosophy.md`).

## [0.1.0] - 2026-04-30

Initial release.

### Added
- Skills: `/new-feature`, `/new-adr`, `/run-plan`.
- Agent: `code-reviewer` (YAGNI rubric).
- Hook: `PreToolUse` blocking direct edits to `.env` files (standalone Python script).
- Marketplace manifest for install via `/plugin marketplace add fppfurtado/pragmatic-dev-toolkit`.
- Documentation: philosophy, path contract, install guide.
