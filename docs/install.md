# Install

## Marketplace install (preferido)

```
/plugin marketplace add fppfurtado/pragmatic-dev-toolkit
/plugin install pragmatic-dev-toolkit@fppfurtado-pragmatic-dev-toolkit
```

Reload se necessário:

```
/reload-plugins
```

Confirmar:

```
/plugin list
```

## Path direto (desenvolvimento)

Útil enquanto você itera no plugin localmente:

```
git clone git@github.com:fppfurtado/pragmatic-dev-toolkit.git
/plugin install /caminho/para/pragmatic-dev-toolkit --scope project
```

## Validação

`claude plugin validate` ainda **não existe** como subcomando estável (até abril de 2026). Para validar localmente:

1. Confirmar `.claude-plugin/plugin.json` válido como JSON.
2. Após instalar, abrir o Claude Code no workspace e confirmar que `/new-feature`, `/new-adr`, `/run-plan`, `/gen-tests-python` aparecem em `/help` ou `/plugin list`.
3. Smoke das skills + edição direta de `.env` (verifica `block_env`) + edição de um `.py` num projeto Python (verifica `run_pytest_python`).

## Pré-requisitos no projeto consumidor

As skills assumem o **path contract** descrito em [`philosophy.md`](./philosophy.md): `IDEA.md`, `BACKLOG.md`, `docs/domain.md`, `docs/design.md`, `docs/decisions/`, `docs/plans/`, `Makefile` com alvo `test`. O caminho mais simples é gerar o projeto com [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit).

Pré-requisitos de runtime dos hooks: `python3` no `PATH`. `run_pytest_python` é auto-gated — só dispara em arquivos `.py` que estão sob um diretório com `pyproject.toml`; usa `uv run pytest` quando `uv` está disponível, senão `python -m pytest`.

## Uninstall

```
/plugin uninstall pragmatic-dev-toolkit@fppfurtado-pragmatic-dev-toolkit
```
