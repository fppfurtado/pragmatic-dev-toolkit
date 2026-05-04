# Philosophy

`pragmatic-dev-toolkit` codifica um workflow específico. Esta página descreve a filosofia que ele assume e o **path contract** que as skills esperam encontrar no projeto consumidor.

## A filosofia em uma frase

**Bounded contexts e linguagem ubíqua sim, cerimônia tática não.** Bounded contexts (DDD estratégico) e vocabulário compartilhado entre código e negócio são fundamentais. Já a cerimônia tática (camadas formais `application/`/`domain/`/`infrastructure/`, ports/adapters universais, mappers em cascata) cria muitos arquivos para pouco valor — adicionar abstração só quando há **dor real** (uma integração instável, uma substituição prevista). YAGNI por padrão.

Refatorar mais tarde costuma ser mais barato do que abstrair cedo.

## Nomear bifurcações arquiteturais

Há pedidos que admitem dois ou mais caminhos com custo, manutenção ou modelo mental significativamente diferentes — verbos abertos ("registrar", "validar", "notificar", "processar", "armazenar", "interagir") são sintoma frequente. A frase do operador satisfaz ambos os caminhos; o plano não. Quando isso acontece, o caminho default-barato vence por inércia se a alternativa não for nomeada.

Em workflow YAGNI essa tensão é real, não cosmética: o viés natural é o caminho mais simples, e nem sempre é o que o operador tinha em mente. A correção é leve — antes do plano, nomear as opções concretas e pedir escolha. A decisão registra-se em `## Contexto` ou `## Resumo da mudança` do plano produzido, para que reviewers e execução posterior saibam por que aquele caminho.

Modo de coleta: **enum** via `AskUserQuestion` (ver "Convenção de pergunta ao operador") — opções nomeadas como `(a) caminho-default-barato` e `(b) caminho-rico`, com `description` carregando o trade-off concreto (custo, manutenção, virtude entregue). Operador escolhe um caminho ou usa "Other" para nomear uma terceira via que a skill não previu. Quando o operador já citou explicitamente uma das opções na frase original (`/new-feature exportar CSV usando streaming`), pular a pergunta e registrar a escolha no plano direto.

Operacionalização concreta no checklist de gaps de `/new-feature`. Sem nomear, a bifurcação fica baked-in no plano sem ter sido discutida.

## Path contract

As skills consomem **papéis**, não paths. A tabela abaixo lista a convenção default por papel — projetos com layout diferente declaram variantes via bloco de config (ver `## Bloco de configuração no CLAUDE.md`).

| Papel | Default | Descrição |
|-------|---------|-----------|
| `product_direction` | `IDEA.md` | O que estamos construindo e por quê. Direção de produto. |
| `ubiquitous_language` | `docs/domain.md` | Bounded contexts, linguagem ubíqua, agregados/entidades, invariantes (RNxx) — quando o domínio merece formalização. |
| `design_notes` | `docs/design.md` | Peculiaridades de integrações externas que não estão na doc oficial. |
| `decisions_dir` | `docs/decisions/` | Diretório de decisões estruturais imutáveis. Numeração e slug do filename são responsabilidade de `/new-adr`. |
| `plans_dir` | `docs/plans/<slug>.md` | Planos multi-fase para mudanças que exigem alinhamento prévio. |
| `backlog` | `BACKLOG.md` | Lista exploratória curta — `## Próximos`, `## Em andamento`, `## Concluídos`. |
| `version_files` | _(sem default — opt-in)_ | Lista de paths a atualizar com a nova versão a cada release. Lista vazia ou ausente = papel desativado. Consumido por `/release`. |
| `changelog` | `CHANGELOG.md` | Histórico de releases. `/release` insere novo bloco no topo a cada bump. |
| `test_command` | `make test` (com `Makefile`) | Gate automático nos passos de execução. |
| (interno do plugin) | `.worktreeinclude` | Lista opcional de gitignored a replicar em worktrees novas. Consumido por `/run-plan`. |
| (agents shipados pelo plugin) | `qa-reviewer`, `security-reviewer` | Baseline genérico invocado por `/run-plan` quando o bloco do plano anota `{reviewer: qa}` ou `{reviewer: security}`. Projeto consumidor pode sobrescrever via `.claude/agents/<nome>.md` (convenção Claude Code; project-level vence colisão de nome). |

Para cada papel configurável, a skill aplica **Resolução de papéis** (próxima seção): probe do default → consultar bloco de config no CLAUDE.md → perguntar ao operador. Projeto que segue os defaults funciona zero-config; projeto com layout diferente declara variantes uma vez no CLAUDE.md. O caminho mais simples para começar com os defaults é gerar o projeto com o template companion [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit), mas qualquer layout alinhado à filosofia funciona.

## Resolução de papéis

Cada skill resolve os papéis que precisa antes de agir, seguindo um protocolo único para evitar drift:

1. **Probe canonical.** Testar se o filename default existe (ex.: `docs/domain.md` para `ubiquitous_language`). Probe é exato, sem fuzzy: `README.md` não é assumido como `IDEA.md`.
2. **Consultar CLAUDE.md.** Se o canonical não existe, ler o CLAUDE.md do projeto consumidor procurando o bloco `<!-- pragmatic-toolkit:config -->` (próxima seção). Valor declarado vence o canonical ausente.
3. **Perguntar ao operador.** Se ainda ausente e o papel é necessário pra skill, pergunta com resposta tri-state: **path concreto** (skill usa esse path) | **`não temos`** (skill segue sem o input se o papel é informacional, ou para com gap report se é obrigatório) | **outro path** (operador aponta arquivo equivalente). Modo de coleta: **enum** via `AskUserQuestion` (ver "Convenção de pergunta ao operador") — duas opções nomeadas (`Não usamos esse papel`, `Existe em outro path`) e "Other" automático recebendo o path concreto digitado pelo operador. Header curto sugerido: nome do papel (`product_direction`, `backlog`, etc.).
4. **Oferta única de memorização.** Ao final da invocação, propor uma vez registrar a resolução no bloco `<!-- pragmatic-toolkit:config -->` do CLAUDE.md. `n` = perguntará de novo na próxima invocação. Operador mantém autonomia sobre o que fica memorizado. Modo: **enum** binário (`Sim, registrar` / `Não, perguntar de novo`).

**Drift detection.** Se o canonical existe E o CLAUDE.md declara variante diferente, skill flagga a inconsistência ao operador antes de prosseguir — provável renome esquecido.

**Papel obrigatório vs informacional.** Skills tratam diferente conforme o papel é necessário pra ação ou só pra contexto:

- **Obrigatórios** (gap report se ausente sem alternativa): `plans_dir` (onde `/run-plan` lê e `/new-feature` grava planos); `test_command` em `/run-plan` quando o plano não tem `## Verificação end-to-end`; `decisions_dir` em `/new-adr` (onde grava o ADR).
- **Informacionais** (skill segue sem o input): `product_direction`, `ubiquitous_language`, `design_notes`, ADRs, `backlog`, `test_command` quando o plano traz `## Verificação end-to-end`. Em `/debug`, **todos** os papéis consumidos são informacionais — papel ausente reduz a base de hipóteses, nunca bloqueia. Em `/gen-tests-python`, `ubiquitous_language` e `design_notes` são informacionais; ausência de `pyproject.toml` no projeto faz a skill recusar por contradição de stack (não é gap report de papel). Em `/release`, `version_files` e `changelog` são informacionais — papel ausente reduz o escopo da release (caso degenerado: só commit + tag), nunca bloqueia. Em `/new-feature`, `backlog` é informacional — papel ausente significa que a skill não grava linha (oferta única de criação no primeiro disparo, espelho do padrão de `ubiquitous_language`/`design_notes`); itens fora-de-escopo capturados no passo 2 passam a ser reportados ao operador sem registro formal.

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
  version_files: ["package.json"]     # default: nenhum (opt-in)
  changelog: CHANGELOG.md             # default: CHANGELOG.md
test_command: make test               # default: make test
```
````

**Semântica:**

- Chave ausente = canonical default.
- Valor `null` (ou explicitamente `false`) = "não usamos esse papel". Skill trata como "não temos" sem perguntar de novo.
- Chaves desconhecidas no bloco são ignoradas (forward-compat para releases que adicionem papéis novos).
- Chaves reservadas em v0.4.0+: `paths.product_direction`, `paths.ubiquitous_language`, `paths.design_notes`, `paths.decisions_dir`, `paths.plans_dir`, `paths.backlog`, `paths.version_files`, `paths.changelog`, `test_command`.

O marcador HTML `<!-- pragmatic-toolkit:config -->` é o que a skill procura — sem ele, o bloco YAML não é interpretado mesmo que esteja sob o cabeçalho `## Pragmatic Toolkit`.

## Convenção de naming

Skills e hooks stack-specific convivem no mesmo plugin com componentes genéricos. O nome carrega o contrato:

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

## Convenção de idioma

Skills e agents adaptam-se ao idioma do projeto consumidor — prosa dirigida ao operador, relatórios de revisores, headers de templates (planos, ADRs, backlog) e nomes de teste seguem o idioma já em uso. A pista é o conteúdo existente. **Critério mecânico:** sinal claro = ≥70% dos artefatos textuais existentes (em ordem de peso: `IDEA.md` > ADRs > planos > `BACKLOG.md`) estão no idioma X. Empate ou ausência → default canonical PT-BR (origem do toolkit). Operador pode forçar via `language: pt|en|...` no bloco de config (chave reservada — ver "Bloco de configuração no CLAUDE.md").

**Hooks são exceção** — mecânica universal, mensagens de erro/bloqueio sempre em inglês, independentemente do idioma do projeto consumidor. Hook é diagnóstico operacional, não prosa do produto.

O que **não** muda com idioma: nomes de agents, chaves de frontmatter, paths e identificadores de código. Esses elementos pertencem à mecânica do toolkit, não ao discurso do projeto, e ficam sempre em inglês para legibilidade cross-stack. Mensagens de commit têm convenção própria — ver "Convenção de commits".

`/run-plan` faz **matching semântico** dos headers de plano — canonical PT-BR é `## Arquivos a alterar`, `## Verificação end-to-end`, `## Verificação manual`, `## Contexto`, `## Resumo da mudança`; equivalentes em outro idioma do projeto (`## Files to change`, `## End-to-end verification`, etc.) são aceitos contanto que a estrutura informacional bata.

## Convenção de commits

Quando `/run-plan` produz micro-commits, segue a **política de mensagens de commit do projeto consumidor**. A pista de qual política usar é, em ordem:

1. **Política explícita** declarada no projeto — bloco no CLAUDE.md, `CONTRIBUTING.md`, `.gitmessage`, hook de commitlint, ou equivalente.
2. **Padrão observado no histórico** — `git log` recente. **Critério mecânico:** predomínio claro = ≥70% dos últimos 50 commits seguem o mesmo padrão extraível (Conventional Commits, gitmoji, prefixos custom tipo `[FEAT]`, idioma específico). Repo com <50 commits → últimos 20.
3. **Default canonical** — [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `style:`) com mensagens em **inglês**. Aplicado quando não há política explícita e o histórico não revela padrão extraível (repo novo, commits ad-hoc).

A regra "um micro-commit por bloco do plano" permanece invariante — pertence à mecânica de execução, não à política de mensagem. `--amend` e rebase de commits de blocos já fechados ficam proibidos pelo mesmo motivo; emendar o último commit do bloco corrente quando faz sentido (typo, arquivo esquecido) é exceção localizada, não regra.

## Convenção de pergunta ao operador

Skills perguntam ao operador em dois modos complementares — `AskUserQuestion` (tool nativa do Claude Code) e prosa livre — e a escolha entre eles não é estética: errar o modo gera ou cerimônia (enum em pergunta livre) ou improviso (prosa em escolha discreta).

- **Enum** via `AskUserQuestion`: opções discretas e mutualmente exclusivas, header curto (≤12 chars), 2-4 opções por pergunta, "Other" automático como válvula para nuance imprevista. Use quando a resposta esperada é um nome/escolha concreto — bifurcação A vs B, tri-state estruturado (`path | "não temos" | <other path>`), confirmação `(s/n)`, multi-seleção de lista discreta (com `multiSelect: true`). Múltiplas perguntas relacionadas podem entrar numa única chamada (até 4). Skills carregam trade-offs concretos (custo, manutenção, virtude entregue) no `description` de cada opção; descrição-óbvia tipo "escolha A" é sintoma de enum cosmético.
- **Prosa** (texto livre na conversa): use quando a resposta exige explicação, exemplo, justificativa, ou descrição naturalmente aberta — relato de sintoma em `/debug`, forma de dado real em validação manual não-determinística, especificação de cenário, gap report, confirmação "ok, valido" após validação manual, listagem de itens fora-de-escopo emergidos. Quando a maioria das respostas reais cairia em "Other" do enum, o modo certo era prosa desde o início.

Pontos do toolkit onde a convenção aplica (resolução de papéis, oferta de memorização, bifurcação arquitetural em `/new-feature`, alinhamento sujo e gatilhos do gate final em `/run-plan`, flag de formato atípico em `/new-adr`) referenciam esta seção sem repetir critério.

## Anotação de revisor em planos

Planos podem direcionar a revisão de cada bloco em `## Arquivos a alterar` anotando o header da subseção com `{reviewer: <perfil>}`. A anotação é mecânica do toolkit (alinhada à regra "nomes de agents/frontmatter ficam em inglês") — a palavra-chave **fica em inglês**.

**Schema:** `{reviewer: code|qa|security}` ou `{reviewer: <perfil>,<perfil>,...}` no fim do header de subseção.

```markdown
### Bloco 1 — autenticação {reviewer: security}
### Bloco 2 — endpoint público {reviewer: code,qa,security}
### Bloco 3 — refactor interno
```

**Semântica:**

- **Sem anotação** → default `code` (não precisa anotar `{reviewer: code}` explicitamente).
- **Um perfil** → `/run-plan` invoca o agent correspondente (`code-reviewer`, `qa-reviewer`, `security-reviewer`).
- **Múltiplos perfis** → `/run-plan` invoca **todos** os perfis listados, em qualquer ordem, agregando relatórios. Substitui regra antiga "mais sensível vence" — security/qa/code revisam objetos diferentes do mesmo diff, faz sentido invocar todos quando o bloco toca múltiplos eixos.

## Cobertura de teste em planos

Testes servem à **confiança**, não à métrica — o plugin não exige TDD estrito nem persegue percentual de cobertura. Em fluxo assistido por IA, no entanto, ausência de teste é fragilidade ampliada: humano segura regressão lendo código; agente regride com mais facilidade. A regra é cobertura **proporcional ao risco da mudança**.

`/new-feature` trata cobertura como gap próprio no checklist do passo 2 (análogo a "Validação manual necessária?"). O planner escolhe entre três saídas:

- (i) **Bloco de teste prescrito em `## Arquivos a alterar` com `{reviewer: qa}`** — quando a feature toca invariante (RNxx do `ubiquitous_language`), integração externa (`design_notes`), persistência, ou comportamento observável novo passível de regressão. Bug fix roteado via `/new-feature` (após `/debug`) é default forte para regression test.
- (ii) **Só `## Verificação end-to-end` textual** — quando o gate automático (`test_command`) já cobre o caminho tocado e a mudança não introduz invariante nova (ex.: ajuste cosmético, log, performance interna sem mudança de contrato).
- (iii) **Nada novo em testes** — refactor puro sem mudança comportamental observável, doc-only.

A anotação `{reviewer: qa}` aplica-se ao bloco que **contém** os testes — `/run-plan` invoca o `qa-reviewer` ao final desse bloco, e ele revisa qualidade do teste recém-escrito (caminho feliz, invariantes, edge cases, mock vs real). Para código de produção que mereça olhar combinado de YAGNI + cobertura no mesmo bloco, usar `{reviewer: code,qa}` — composição já documentada em "Anotação de revisor em planos", sem schema novo.

Scaffolders stack-specific (ex.: `/gen-tests-python`) **complementam** a prescrição — geram o esqueleto do arquivo de teste; não substituem a decisão do gap nem o micro-commit, que ficam no `/run-plan`. Projetos fora de stacks com scaffolder dedicado escrevem o teste manualmente — a saída (i) continua valendo.

## Linguagem ubíqua na implementação

`docs/domain.md` (papel `ubiquitous_language`) é base **de interpretação E de desenvolvimento**: bounded contexts e linguagem ubíqua só são pilares se chegarem ao código. Vocabulário registrado no domínio mas ausente nos identificadores produzidos vira ornamento de alinhamento — exatamente o que a frase-tese da filosofia rejeita.

O contrato é um pipeline de três estágios, espelho do pipeline de invariantes do `qa-reviewer`:

1. **`/new-feature` (alignment) extrai termos tocados.** O passo 1 já lê `ubiquitous_language` e identifica bounded contexts, agregados/entidades, RNs e conceitos ubíquos que o pedido toca. O passo 4 grava esse subconjunto no `## Contexto` do plano como `**Termos ubíquos tocados:** <Termo> (<categoria>), ...`. Pedidos que não tocam o domínio (refactor puro, doc-only) seguem sem a linha.
2. **`/run-plan` (execução) lê o plano.** Não relê `docs/domain.md` — o plano é o ponto único de transferência entre alinhamento e execução; releitura duplicaria responsabilidade e adicionaria cerimônia. Plano sem a linha = mudança não toca domínio = nada a carregar.
3. **`code-reviewer` (revisão) valida no diff.** Regra prescritiva na seção "Identificadores": identificador novo que representa conceito declarado em `ubiquitous_language` deve usar o termo declarado, não sinônimo improvisado. Complementa a regra defensiva pré-existente ("renomeação cosmética não").

**Quando o pipeline silencia.** Papel `ubiquitous_language` resolveu para "não temos" → `/new-feature` não lista termos, plano sai sem a linha, `code-reviewer` não flagga. Toda a cadeia segue funcional sem fricção em projetos que ainda não formalizaram domínio.

**Por que não tocar `/run-plan`.** Adicionar releitura de `docs/domain.md` na execução violaria a separação alinhamento → plano → execução. O plano carrega o subconjunto relevante; a defesa contra drift entre código e domínio fica no reviewer, que age sobre o diff — onde a divergência efetivamente aparece.

## Convenção `.worktreeinclude`

`.worktreeinclude` lista paths de arquivos gitignored que `/run-plan` deve replicar para a worktree nova. É plugin-internal — não interage com `git worktree` diretamente, é lido apenas pela skill.

**Formato:** texto simples, um path por linha, relativo à raiz do repo. Linhas começando com `#` são comentários. Linhas em branco são ignoradas. Globs (`**/*.local`) são roadmap — hoje só paths literais.

```
# segredos do projeto
.env
config/local.yaml

# caches gerados
.venv
node_modules
```

Sem `.worktreeinclude` → `/run-plan` cria worktree apenas com arquivos versionados (comportamento padrão do `git worktree`). Com `.worktreeinclude` → skill copia os paths listados após criar a worktree, antes do baseline de `test_command`.

## Companion

[`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit) é o template Copier que produz a estrutura inicial de um projeto novo já alinhada ao path contract acima. Os dois artefatos são desacoplados — você pode usar um sem o outro, mas a sinergia é clara: bootstrap com `scaffold-kit`, automação com este plugin.
