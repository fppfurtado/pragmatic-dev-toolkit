# pragmatic-dev-toolkit

Claude Code plugin para o workflow **flat & pragmatic**: skills genéricas, revisor YAGNI e proteção de `.env`. Companion do [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit).

## O que vem

| Componente | Tipo | O que faz |
|------------|------|-----------|
| `/triage` | Skill | Alinha intenção, levanta gaps e decide qual artefato (linha de backlog, plano, ADR, atualização de domínio/design) é necessário antes de implementar. Sem argumento, delega para `/next`. |
| `/next` | Skill | Orientação de sessão: lê o backlog, verifica no código o que já foi implementado e sugere os três candidatos de maior impacto para triagem. |
| `/new-adr` | Skill | Cria um novo ADR em `docs/decisions/` com numeração automática e template padronizado. |
| `/run-plan` | Skill | Executa um plano de `docs/plans/<slug>.md` em worktree isolada, micro-commits Conventional Commits, revisão dirigida por bloco, gate de validação manual quando aplicável e sugestão de push/PR ao concluir. |
| `/debug <sintoma>` | Skill | Diagnostica causa-raiz por método científico (reproduzir → isolar → hipótese-teste → evidência). Produz diagnóstico, não fix — operador escolhe revert / patch direto / `/triage` depois. Stack-agnóstico. |
| `/gen-tests-python` | Skill | Gera testes pytest para um módulo/função de um projeto Python (pytest + respx + asyncio_mode auto + tmp_path para SQLite). |
| `/release [<bump>\|<version>]` | Skill | Bump de versão coordenado em `version_files`, entrada no `changelog`, commit unificado e tag anotada local. Não faz push — publicação fica com o operador. |
| `/heal-backlog` | Skill | Detecta merge artifacts em `BACKLOG.md` e propõe edit de cura via gate Aplicar/Cancelar. |
| `code-reviewer` | Agent | Rubrica YAGNI: flagra abstrações prematuras, comentários redundantes, defensividade desnecessária e backwards-compat fantasma. |
| `qa-reviewer` | Agent | Princípios de cobertura de testes: caminho feliz, invariantes documentadas, edge cases declarados, mock vs real. Stack-agnóstico. |
| `security-reviewer` | Agent | Credenciais, validação de entrada, HTTP externo, dados sensíveis e invariantes documentadas em ADRs. Stack-agnóstico. |
| `block_env` | Hook | `PreToolUse` que bloqueia edição direta a `.env` (e variantes), aceitando apenas `.env.example`. |
| `run_pytest_python` | Hook | `PostToolUse` auto-gated (`.py` + ancestral `pyproject.toml`) que roda pytest após edits e imprime saída só em falha. |

## Instalação

```
/plugin marketplace add fppfurtado/pragmatic-dev-toolkit
/plugin install pragmatic-dev-toolkit@fppfurtado-pragmatic-dev-toolkit
```

Detalhes e alternativa de path direto em [`docs/install.md`](docs/install.md).

## Filosofia

Bounded contexts e linguagem ubíqua sim, cerimônia tática (camadas formais, ports/adapters universais, mappers em cascata) **não**. YAGNI por padrão; abstrações só quando há dor real. Ler [`docs/philosophy.md`](docs/philosophy.md) para o detalhe e o **path contract** que as skills assumem.

Funciona em qualquer projeto alinhado à filosofia, não só os gerados por `scaffold-kit`. As skills consomem **papéis** (linguagem ubíqua, plano, decisão, gate de testes…), não paths literais — projeto com layout diferente declara variantes uma vez via bloco `<!-- pragmatic-toolkit:config -->` no `CLAUDE.md`. Detalhe e schema em [`docs/install.md`](docs/install.md).

## Companion

[`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit) é o template Copier que produz a estrutura inicial de um projeto novo já alinhada ao path contract default (`IDEA.md`, `docs/domain.md`, `docs/design.md`, `docs/decisions/`, `docs/plans/`, `BACKLOG.md`, `Makefile`, `.worktreeinclude`). Os dois artefatos são desacoplados — você pode usar um sem o outro.

## Contribuir

Issues e PRs bem-vindos. Mudanças estruturais nas skills/agents passam por ADR no [próprio repo](docs/) (a ser adicionado se virar útil).

## Licença

MIT — ver [LICENSE](LICENSE).
