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
2. Após instalar, abrir o Claude Code no workspace e confirmar que `/new-feature`, `/new-adr`, `/run-plan` aparecem em `/help` ou `/plugin list`.
3. Smoke das 3 skills + edição direta de `.env` para verificar o hook.

## Pré-requisitos no projeto consumidor

As skills assumem o **path contract** descrito em [`philosophy.md`](./philosophy.md): `IDEA.md`, `BACKLOG.md`, `docs/domain.md`, `docs/design.md`, `docs/decisions/`, `docs/plans/`, `Makefile` com alvo `test`. O caminho mais simples é gerar o projeto com [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit).

Pré-requisitos de runtime do hook `block_env`: `python3` no `PATH`. Não há outros.

## Snippet opcional: rodar testes após edits Python

Se você quer que a suíte unit rode automaticamente após edits em `src/**/*.py`, cole este `PostToolUse` no `.claude/settings.json` do projeto (não vem no plugin porque é Python-specific e quebraria silenciosamente em projetos não-Python):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c 'import sys, json, os, subprocess\nd = json.load(sys.stdin); p = d.get(\"tool_input\", {}).get(\"file_path\", \"\")\nif \"/src/\" not in p or not p.endswith(\".py\"): sys.exit(0)\nr = os.path.dirname(os.path.abspath(p))\nwhile r != \"/\" and not os.path.isfile(os.path.join(r, \"pyproject.toml\")): r = os.path.dirname(r)\nif r == \"/\": sys.exit(0)\nres = subprocess.run([\"uv\", \"run\", \"pytest\", \"tests/unit\", \"-q\", \"--no-header\"], cwd=r, capture_output=True, text=True)\nprint(\"\\n\".join((res.stdout + res.stderr).splitlines()[-10:]))'"
          }
        ]
      }
    ]
  }
}
```

Assume `uv` instalado, `pyproject.toml` na raiz e suíte em `tests/unit/`.

## Uninstall

```
/plugin uninstall pragmatic-dev-toolkit@fppfurtado-pragmatic-dev-toolkit
```
