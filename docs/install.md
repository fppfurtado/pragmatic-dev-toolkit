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

Use `claude plugin validate <path>` (ferramenta oficial) — aceita o caminho de `.claude-plugin/plugin.json` ou `.claude-plugin/marketplace.json` e reporta erros de schema mais warnings. Para validações adicionais não cobertas pelo subcomando (smoke das skills, edição de `.env`, hooks disparando), siga o checklist:

1. Confirmar `.claude-plugin/plugin.json` e `.claude-plugin/marketplace.json` válidos via `claude plugin validate`.
2. Após instalar, abrir o Claude Code no workspace e confirmar que `/draft-idea`, `/triage`, `/new-adr`, `/run-plan`, `/debug`, `/gen-tests`, `/release`, `/next`, `/init-config`, `/archive-plans` aparecem em `/help` ou `/plugin list`.
3. Smoke das skills + edição direta de `.env` (verifica `block_env`) + tentativa de edição em path coberto pelo `.gitignore` do consumer (ex.: `.venv/foo.py`, `node_modules/x/index.js` — verifica `block_gitignored`) + edição de um `.py` num projeto Python (verifica `run_pytest_python`).
4. Invocar `qa-reviewer` num diff que adiciona função pública sem teste correspondente → flag esperado de "caminho feliz sem teste".
5. Invocar `security-reviewer` num diff que faz `logger.info(f"token={token}")` → flag esperado de "credencial em log".
5a. Invocar `doc-reviewer` num diff que adiciona, num `.md` qualquer, link `[ver](docs/inexistente.md)` ou referência a flag/comando inexistente no projeto → flag esperado de drift (`cross-ref/anchor quebrado` ou `identificador inexistente`).
6. Invocar `/debug` com um sintoma operacionalizável (ex.: teste que sabidamente falha) → skill produz diagnóstico estruturado (sintoma, causa-raiz, evidência, impacto, caminhos de correção; opcionalmente *hipóteses testadas*) e fecha com sugestão de próximo passo **sem aplicar fix nem fazer commit**.
7. Em projeto com bloco de config declarado, invocar `/triage` num pedido que toque domínio e confirmar que a skill consulta o path declarado (ex.: `docs/glossary.md`), não o canonical (`docs/domain.md`).
8. Em projeto com plano contendo `### Bloco 1 — exemplo {revisor: code}` (alias PT removido em v1.0), invocar `/run-plan` → confirmar recusa explícita (não silenciosa, sem fallback) com mensagem indicando o bloco e a anotação ofensora, sugerindo migrar para `{reviewer:}`.
8a. Em projeto com remote configurado, invocar `/run-plan` num plano simples de 1 bloco → ao concluir, confirmar que o enum `Publicar` aparece com as opções `Push`, `Push + abrir PR/MR` e `Nenhum`; confirmar que selecionar `Push + abrir PR/MR` faz `git push` e dispara auto-detect do forge (host `github.com` → `gh pr create --fill`; host casando `^gitlab\.` → `glab mr create --fill`) com gate `Forge` (`Executar` / `Pular`) antes de executar; em host fora do mapeamento, confirmar fallback textual genérico (UI web ou CLI específica do forge); em host mapeado mas com CLI ausente, confirmar fallback textual citando o CLI esperado (`gh`/`glab`) e link da UI; confirmar que em repo sem remote o enum não aparece.
9. Em projeto com `docs/domain.md` declarando ao menos uma RNxx, invocar `/triage` com pedido que toca essa RN → confirmar que o plano resultante inclui bloco de teste em `## Arquivos a alterar` com `{reviewer: qa}`, **ou** justifica ausência via `## Verificação end-to-end` textual (heurística "Cobertura de teste em planos").
10. Em projeto com tag prévia (ex.: `v0.1.0`), `paths.version_files` declarado (ex.: `["package.json"]`) e `CHANGELOG.md` em formato Keep-a-Changelog, invocar `/release patch` → confirmar (a) bump da versão em `version_files`, (b) entrada `## [0.1.1] - YYYY-MM-DD` no topo do changelog agrupando commits por tipo CC, (c) commit local `chore(release): bump version to 0.1.1`, (d) tag anotada `v0.1.1` criada localmente, (e) **nenhum push** disparado pela skill — mensagem final orienta `git push --follow-tags`; (f) após a instrução de push, dispara auto-detect do forge para criar release (host `github.com` → `gh release create --generate-notes`; host casando `^gitlab\.` → `glab release create --notes <body-do-changelog>`) com gate `Forge` (`Executar (após push)` / `Pular`); em host fora do mapeamento, fallback textual genérico; em host mapeado mas com CLI ausente, fallback textual citando o CLI esperado e link da UI.
11. Em projeto com ≥1 plano em `docs/plans/` cuja `**Linha do backlog:**` está em `BACKLOG.md ## Concluídos` há ≥2 semanas, invocar `/archive-plans` → confirmar preview lista o plano com destino `archive/<YYYY-Qx>/`; ao selecionar `Cancelar`, confirmar que nenhum `git mv` foi executado (`git status` limpo). Ao re-invocar e selecionar `Aplicar`, confirmar `git mv` + commit `chore: archive <N> historical plans`, **sem push**.

## Pré-requisitos no projeto consumidor

As skills consomem **papéis**, não paths literais. Projeto que segue os defaults canonicais funciona zero-config — o caminho mais simples é gerar com [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit). Lista canônica de papéis (papel | default | descrição) no [`CLAUDE.md`](../CLAUDE.md) do plugin → "The role contract".

Projeto com layout diferente declara variantes uma vez no `CLAUDE.md` raiz, sob o marcador HTML `<!-- pragmatic-toolkit:config -->`. **Caminho recomendado:** rodar `/init-config` em vez de editar manualmente — wizard interativo que grava o bloco; alternativa proativa à memorização one-shot per role do Resolution protocol. Edição manual segue válida — esquema YAML descrito abaixo:

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

Chave ausente = canonical default. Valor `null` = "não usamos esse papel" (skill segue sem o input para papéis informacionais; gap report para `plans_dir` em `/triage`/`/run-plan` e `decisions_dir` em `/new-adr`).

Valor `local` = artefato local-gitignored em `.claude/local/<role>/`, aceito por `decisions_dir`, `backlog` e `plans_dir` (recusado por `version_files`/`changelog`). Mecânica (mkdir, probe gitignore, gate `Gitignore`) em [`CLAUDE.md`](../CLAUDE.md) → "Local mode" (ADR-005).

`.worktreeinclude` pode ser tracked (default; equipe compartilha lista) ou gitignored (cada dev tem o seu, útil quando lista varia por dev — paths de fixtures locais, credenciais por máquina, etc.). Plugin permanece agnóstico — em modo local, `/init-config` cria/atualiza o arquivo independente do estado de tracking (per [ADR-018](decisions/ADR-018-replicacao-claude-em-modo-local-init-config.md)). **Em modo canonical (nenhum role declarado `local`), `/init-config` não toca `.worktreeinclude`.** `/run-plan` lê e replica o conteúdo na worktree fresca.

Pré-requisitos de runtime dos hooks: `python3` (≥ 3.10) no `PATH`. `run_pytest_python.py` usa sintaxe PEP 604 (`str | None`); versões anteriores falham com `SyntaxError` ao executar o hook. `run_pytest_python` é auto-gated — só dispara em arquivos `.py` que estão sob um diretório com `pyproject.toml`; usa `uv run pytest` quando `uv` está disponível, senão `python -m pytest`. `block_gitignored` é auto-gated em três camadas (file_path vazio, fora de repo git, ou `git` ausente do `PATH` → no-op silencioso); quando dispara, executa `git check-ignore` uma vez e bloqueia (exit 2) se o path estiver coberto pelo `.gitignore` do consumer. Exceção: edits sob `<repo>/.claude/` são allowlisted (território do harness) — load-bearing para o modo local-gitignored do ADR-005.

Esqueleto canônico de plano em [`templates/plan.md`](../templates/plan.md) — referência para autoria manual quando o operador prefere escrever o plano direto, sem `/triage`.

## Uninstall

```
/plugin uninstall pragmatic-dev-toolkit@fppfurtado-pragmatic-dev-toolkit
```
