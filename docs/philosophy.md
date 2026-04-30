# Philosophy

`pragmatic-dev-toolkit` codifica um workflow específico. Esta página descreve a filosofia que ele assume e o **path contract** que as skills esperam encontrar no projeto consumidor.

## A filosofia em uma frase

**Bounded contexts e linguagem ubíqua sim, cerimônia tática não.** Bounded contexts (DDD estratégico) e vocabulário compartilhado entre código e negócio são fundamentais. Já a cerimônia tática (camadas formais `application/`/`domain/`/`infrastructure/`, ports/adapters universais, mappers em cascata) cria muitos arquivos para pouco valor — adicionar abstração só quando há **dor real** (uma integração instável, uma substituição prevista). YAGNI por padrão.

Refatorar mais tarde costuma ser mais barato do que abstrair cedo.

## Path contract

As skills deste plugin assumem que o projeto segue estas convenções de path:

| Path | Papel |
|------|-------|
| `IDEA.md` | O que estamos construindo e por quê. Direção de produto. |
| `docs/domain.md` | Linguagem ubíqua, agregados, invariantes (RNxx) — quando o domínio merece formalização. |
| `docs/design.md` | Peculiaridades de integrações externas que não estão na doc oficial. |
| `docs/decisions/ADR-NNN-*.md` | Decisões estruturais imutáveis. Numeradas a partir de `001`, slug em kebab-case. |
| `docs/plans/<slug>.md` | Planos multi-fase para mudanças que exigem alinhamento prévio. |
| `BACKLOG.md` | Lista exploratória curta — `## Próximos`, `## Em andamento`, `## Concluídos`. |
| `Makefile` (com alvo `test`) | Gate automático nos passos de execução. |
| `.worktreeinclude` (opcional) | Lista de gitignored a replicar em worktrees novas. Consumido por `/run-plan`. |
| `.claude/agents/qa-reviewer.md`, `.claude/agents/security-reviewer.md` (opcional) | Revisores project-level invocados por `/run-plan` quando o bloco do plano anota `{revisor: qa}` ou `{revisor: security}`. |

Se o projeto não segue alguma dessas convenções, a skill correspondente reporta o gap em vez de tentar adivinhar. O caminho mais simples para adoção é gerar o projeto com o template companion [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit), mas qualquer projeto pode adotar as convenções manualmente.

## O que **não** está incluso (e por quê)

- **`gen-test` skill e regras `tests.md` Python-pytest-specific.** Stack-específicos. Adicionar como sub-plugin Python (`pragmatic-dev-toolkit-python`) só quando 2+ projetos pragmatic-Python pedirem.
- **Hook `PostToolUse` rodando testes automaticamente.** Stack-específico (assume `uv run pytest` e `tests/unit/`). Disponível como snippet em `docs/install.md` para colar em `.claude/settings.json` do projeto.
- **`qa-reviewer`, `security-reviewer`.** Saturados de invariantes e contratos específicos; tirar isso deixa pouco. Ficam project-level. `/run-plan` os invoca via fallback de path quando existem em `.claude/agents/` do projeto.

## Companion

[`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit) é o template Copier que produz a estrutura inicial de um projeto novo já alinhada ao path contract acima. Os dois artefatos são desacoplados — você pode usar um sem o outro, mas a sinergia é clara: bootstrap com `scaffold-kit`, automação com este plugin.
