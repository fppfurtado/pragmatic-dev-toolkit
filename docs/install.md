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
2. Após instalar, abrir o Claude Code no workspace e confirmar que `/new-feature`, `/new-adr`, `/run-plan`, `/debug`, `/gen-tests-python` aparecem em `/help` ou `/plugin list`.
3. Smoke das skills + edição direta de `.env` (verifica `block_env`) + edição de um `.py` num projeto Python (verifica `run_pytest_python`).
4. Invocar `qa-reviewer` num diff que adiciona função pública sem teste correspondente → flag esperado de "caminho feliz sem teste".
5. Invocar `security-reviewer` num diff que faz `logger.info(f"token={token}")` → flag esperado de "credencial em log".
6. Invocar `/debug` com um sintoma operacionalizável (ex.: teste que sabidamente falha) → skill produz diagnóstico estruturado (sintoma, causa-raiz, evidência, impacto, caminhos de correção) **sem aplicar fix nem fazer commit**.
7. Em projeto com bloco de config declarado, invocar `/new-feature` num pedido que toque domínio e confirmar que a skill consulta o path declarado (ex.: `docs/glossary.md`), não o canonical (`docs/domain.md`).
8. Em projeto com plano contendo `### Bloco 1 — exemplo {revisor: code}` (alias PT removido em v1.0), invocar `/run-plan` → confirmar recusa explícita (não silenciosa, sem fallback) com mensagem indicando o bloco e a anotação ofensora, sugerindo migrar para `{reviewer:}`.

## Pré-requisitos no projeto consumidor

As skills consomem **papéis** (`product_direction`, `ubiquitous_language`, `design_notes`, `decisions_dir`, `plans_dir`, `backlog`, `test_command`), não paths literais. A convenção default por papel é o canonical (`IDEA.md`, `BACKLOG.md`, `docs/domain.md`, `docs/design.md`, `docs/decisions/`, `docs/plans/`, `make test`). Projeto que segue os defaults funciona zero-config — o caminho mais simples é gerar com [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit).

Projeto com layout diferente declara variantes uma vez no `CLAUDE.md` raiz, sob o marcador HTML `<!-- pragmatic-toolkit:config -->`:

````markdown
## Pragmatic Toolkit
<!-- pragmatic-toolkit:config -->
```yaml
paths:
  ubiquitous_language: docs/glossary.md   # em vez do default docs/domain.md
  decisions_dir: decisions/               # em vez do default docs/decisions/
test_command: uv run pytest               # em vez do default make test
```
````

Chave ausente = canonical default. Valor `null` = "não usamos esse papel" (skill segue sem o input para papéis informacionais; gap report para `plans_dir` ou `backlog` em skills que gravam saída ali). Detalhe completo do protocolo em [`philosophy.md`](./philosophy.md#resolução-de-papéis).

Pré-requisitos de runtime dos hooks: `python3` no `PATH`. `run_pytest_python` é auto-gated — só dispara em arquivos `.py` que estão sob um diretório com `pyproject.toml`; usa `uv run pytest` quando `uv` está disponível, senão `python -m pytest`.

## Uninstall

```
/plugin uninstall pragmatic-dev-toolkit@fppfurtado-pragmatic-dev-toolkit
```
