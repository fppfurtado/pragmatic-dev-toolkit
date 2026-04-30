# pragmatic-dev-toolkit

Claude Code plugin para o workflow **flat & pragmatic**: skills genéricas, revisor YAGNI e proteção de `.env`. Companion do [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit).

## O que vem

| Componente | Tipo | O que faz |
|------------|------|-----------|
| `/new-feature` | Skill | Alinha intenção, levanta gaps e decide qual artefato (linha de backlog, plano, ADR, atualização de domínio/design) é necessário antes de implementar. |
| `/new-adr` | Skill | Cria um novo ADR em `docs/decisions/` com numeração automática e template padronizado. |
| `/run-plan` | Skill | Executa um plano de `docs/plans/<slug>.md` em worktree isolada, micro-commits Conventional Commits, revisão dirigida por bloco e gate de validação manual quando aplicável. |
| `code-reviewer` | Agent | Rubrica YAGNI: flagra abstrações prematuras, comentários redundantes, defensividade desnecessária e backwards-compat fantasma. |
| `block_env` | Hook | `PreToolUse` que bloqueia edição direta a `.env` (e variantes), aceitando apenas `.env.example`. |

## Instalação

```
/plugin marketplace add fppfurtado/pragmatic-dev-toolkit
/plugin install pragmatic-dev-toolkit@fppfurtado-pragmatic-dev-toolkit
```

Detalhes e alternativa de path direto em [`docs/install.md`](docs/install.md).

## Filosofia

Bounded contexts e linguagem ubíqua sim, cerimônia tática (camadas formais, ports/adapters universais, mappers em cascata) **não**. YAGNI por padrão; abstrações só quando há dor real. Ler [`docs/philosophy.md`](docs/philosophy.md) para o detalhe e o **path contract** que as skills assumem.

## Companion

Para começar um projeto novo já alinhado ao path contract (`IDEA.md`, `docs/domain.md`, `docs/design.md`, `docs/decisions/`, `docs/plans/`, `BACKLOG.md`, `Makefile`, `.worktreeinclude`), use o template [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit) — eles foram desenhados juntos.

## Contribuir

Issues e PRs bem-vindos. Mudanças estruturais nas skills/agents passam por ADR no [próprio repo](docs/) (a ser adicionado se virar útil).

## Licença

MIT — ver [LICENSE](LICENSE).
