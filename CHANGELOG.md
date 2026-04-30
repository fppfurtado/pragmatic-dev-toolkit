# Changelog

All notable changes to this plugin are documented here. Format inspired by [Keep a Changelog](https://keepachangelog.com/).

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
