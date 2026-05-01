# Philosophy

`pragmatic-dev-toolkit` codifica um workflow específico. Esta página descreve a filosofia que ele assume e o **path contract** que as skills esperam encontrar no projeto consumidor.

## A filosofia em uma frase

**Bounded contexts e linguagem ubíqua sim, cerimônia tática não.** Bounded contexts (DDD estratégico) e vocabulário compartilhado entre código e negócio são fundamentais. Já a cerimônia tática (camadas formais `application/`/`domain/`/`infrastructure/`, ports/adapters universais, mappers em cascata) cria muitos arquivos para pouco valor — adicionar abstração só quando há **dor real** (uma integração instável, uma substituição prevista). YAGNI por padrão.

Refatorar mais tarde costuma ser mais barato do que abstrair cedo.

## Nomear bifurcações arquiteturais

Há pedidos que admitem dois ou mais caminhos com custo, manutenção ou modelo mental significativamente diferentes — verbos abertos ("registrar", "validar", "notificar", "processar", "armazenar", "interagir") são sintoma frequente. A frase do operador satisfaz ambos os caminhos; o plano não. Quando isso acontece, o caminho default-barato vence por inércia se a alternativa não for nomeada.

Em workflow YAGNI essa tensão é real, não cosmética: o viés natural é o caminho mais simples, e nem sempre é o que o operador tinha em mente. A correção é leve — antes do plano, nomear as opções concretas e pedir escolha. A decisão registra-se em `## Contexto` ou `## Resumo da mudança` do plano produzido, para que reviewers e execução posterior saibam por que aquele caminho.

Operacionalização concreta no checklist de gaps de `/new-feature`. Sem nomear, a bifurcação fica baked-in no plano sem ter sido discutida.

## Path contract

As skills consomem **papéis**, não paths. A tabela abaixo lista a convenção default por papel — projetos com layout diferente declaram variantes via bloco de config (ver `## Bloco de configuração no CLAUDE.md`).

| Papel | Default | Descrição |
|-------|---------|-----------|
| `product_direction` | `IDEA.md` | O que estamos construindo e por quê. Direção de produto. |
| `ubiquitous_language` | `docs/domain.md` | Linguagem ubíqua, agregados, invariantes (RNxx) — quando o domínio merece formalização. |
| `design_notes` | `docs/design.md` | Peculiaridades de integrações externas que não estão na doc oficial. |
| `decisions_dir` | `docs/decisions/ADR-NNN-*.md` | Decisões estruturais imutáveis. Numeradas a partir de `001`, slug em kebab-case. |
| `plans_dir` | `docs/plans/<slug>.md` | Planos multi-fase para mudanças que exigem alinhamento prévio. |
| `backlog` | `BACKLOG.md` | Lista exploratória curta — `## Próximos`, `## Em andamento`, `## Concluídos`. |
| `test_command` | `make test` (com `Makefile`) | Gate automático nos passos de execução. |
| (interno do plugin) | `.worktreeinclude` | Lista opcional de gitignored a replicar em worktrees novas. Consumido por `/run-plan`. |
| (convenção Claude Code) | `.claude/agents/qa-reviewer.md`, `.claude/agents/security-reviewer.md` | Revisores project-level invocados por `/run-plan` quando o bloco do plano anota `{revisor: qa}` ou `{revisor: security}`. |

Para cada papel configurável, a skill aplica **Resolução de papéis** (próxima seção): probe do default → consultar bloco de config no CLAUDE.md → perguntar ao operador. Projeto que segue os defaults funciona zero-config; projeto com layout diferente declara variantes uma vez no CLAUDE.md. O caminho mais simples para começar com os defaults é gerar o projeto com o template companion [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit), mas qualquer layout alinhado à filosofia funciona.

## Resolução de papéis

Cada skill resolve os papéis que precisa antes de agir, seguindo um protocolo único para evitar drift:

1. **Probe canonical.** Testar se o filename default existe (ex.: `docs/domain.md` para `ubiquitous_language`). Probe é exato, sem fuzzy: `README.md` não é assumido como `IDEA.md`.
2. **Consultar CLAUDE.md.** Se o canonical não existe, ler o CLAUDE.md do projeto consumidor procurando o bloco `<!-- pragmatic-toolkit:config -->` (próxima seção). Valor declarado vence o canonical ausente.
3. **Perguntar ao operador.** Se ainda ausente e o papel é necessário pra skill, pergunta com resposta tri-state: **path concreto** (skill usa esse path) | **`não temos`** (skill segue sem o input se o papel é informacional, ou para com gap report se é obrigatório) | **outro path** (operador aponta arquivo equivalente).
4. **Oferta única de memorização.** Ao final da invocação, propor uma vez "registrar essa resolução no CLAUDE.md? (s/n)". `n` = perguntará de novo na próxima invocação. Operador mantém autonomia sobre o que fica memorizado.

**Drift detection.** Se o canonical existe E o CLAUDE.md declara variante diferente, skill flagga a inconsistência ao operador antes de prosseguir — provável renome esquecido.

**Papel obrigatório vs informacional.** Skills tratam diferente conforme o papel é necessário pra ação ou só pra contexto:

- **Obrigatórios** (gap report se ausente sem alternativa): `plans_dir` (onde `/run-plan` lê e `/new-feature` grava planos), `backlog` em `/new-feature` (onde grava linhas), `test_command` em `/run-plan` quando o plano não tem `## Verificação end-to-end`.
- **Informacionais** (skill segue sem o input): `product_direction`, `ubiquitous_language`, `design_notes`, ADRs, `test_command` quando o plano traz `## Verificação end-to-end`.

## Bloco de configuração no CLAUDE.md

Projeto consumidor declara variantes do path contract num bloco fenced no `CLAUDE.md` raiz, marcado por comentário HTML reservado. Skills procuram esse bloco; ausência total = todos os defaults.

````markdown
## Pragmatic Toolkit
<!-- pragmatic-toolkit:config -->
```yaml
paths:
  product_direction: IDEA.md          # default: IDEA.md
  ubiquitous_language: docs/domain.md # default: docs/domain.md
  design_notes: docs/design.md        # default: docs/design.md
  decisions_dir: docs/decisions/      # default: docs/decisions/
  plans_dir: docs/plans/              # default: docs/plans/
  backlog: BACKLOG.md                 # default: BACKLOG.md
test_command: make test               # default: make test
```
````

**Semântica:**

- Chave ausente = canonical default.
- Valor `null` (ou explicitamente `false`) = "não usamos esse papel". Skill trata como "não temos" sem perguntar de novo.
- Chaves desconhecidas no bloco são ignoradas (forward-compat para releases que adicionem papéis novos).
- Chaves reservadas em v0.4.0: `paths.product_direction`, `paths.ubiquitous_language`, `paths.design_notes`, `paths.decisions_dir`, `paths.plans_dir`, `paths.backlog`, `test_command`.

O marcador HTML `<!-- pragmatic-toolkit:config -->` é o que a skill procura — sem ele, o bloco YAML não é interpretado mesmo que esteja sob o cabeçalho `## Pragmatic Toolkit`.

## Convenção de naming

Skills e hooks stack-specific convivem no mesmo plugin com componentes genéricos sem precisar de sub-plugin. O nome carrega o contrato:

| Tipo | Genérico | Stack-specific |
|------|----------|----------------|
| Hook (script) | `<purpose>.py\|.sh` (ex.: `block_env.py`) | `<purpose>_<stack>.py\|.sh` (ex.: `run_pytest_python.py`) |
| Skill (frontmatter `name`) | `<verb>-<artifact>` (ex.: `new-feature`) | `<verb>-<artifact>-<stack>` (ex.: `gen-tests-python`) |
| Agent (frontmatter `name`) | `<role>` (ex.: `code-reviewer`, `qa-reviewer`, `security-reviewer`) | `<role>-<stack>` (apenas se os princípios mudarem com a stack) |

Componentes que **geram ou executam** algo da stack (skills geradoras de código, hooks que invocam toolchain) precisam de sufixo — sintaxe ou comando concreto não tem versão neutra. Componentes que **revisam princípios** lidos do diff não precisam — o stack está no próprio diff.

A diferença operacional: **skill é invocada pelo usuário**, então o sufixo de stack é declaração explícita de acoplamento ("não me chame em projeto Java"). **Hook dispara sozinho** em todo projeto onde o plugin está instalado, então precisa de **auto-gating triplo** para silenciar em projetos da stack errada:

1. **Extensão do arquivo** — `if not file_path.endswith(".py"): exit 0` filtra a maioria dos casos sem custo.
2. **Marcador de stack** — caminhar pelos ancestrais procurando `pyproject.toml` (Python), `build.gradle*`/`pom.xml` (JVM), etc. Sem marcador, exit 0.
3. **Toolchain** — só executar a ferramenta (`uv run pytest`, `gradle test`) com fallback razoável; se a toolchain não existe, exit 0.

Isso torna seguro shipar `run_pytest_python.py` no mesmo plugin que `run_gradle_test_java.sh`: cada hook é silente em projetos fora da sua stack, sem flags nem env vars para desligar.

## Companion

[`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit) é o template Copier que produz a estrutura inicial de um projeto novo já alinhada ao path contract acima. Os dois artefatos são desacoplados — você pode usar um sem o outro, mas a sinergia é clara: bootstrap com `scaffold-kit`, automação com este plugin.
