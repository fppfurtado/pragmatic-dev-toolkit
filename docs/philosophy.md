# Philosophy

`pragmatic-dev-toolkit` codifica um workflow específico. Esta página descreve a filosofia que ele assume e o **path contract** que as skills esperam encontrar no projeto consumidor.

## A filosofia em uma frase

**Bounded contexts e linguagem ubíqua sim, cerimônia tática não.** Bounded contexts (DDD estratégico) e vocabulário compartilhado entre código e negócio são fundamentais. Já a cerimônia tática (camadas formais `application/`/`domain/`/`infrastructure/`, ports/adapters universais, mappers em cascata) cria muitos arquivos para pouco valor — adicionar abstração só quando há **dor real** (uma integração instável, uma substituição prevista). YAGNI por padrão.

Refatorar mais tarde costuma ser mais barato do que abstrair cedo.

## Nomear bifurcações arquiteturais

Há pedidos que admitem dois ou mais caminhos com custo, manutenção ou modelo mental significativamente diferentes — verbos abertos ("registrar", "validar", "notificar", "processar", "armazenar", "interagir") são sintoma frequente. A frase do operador satisfaz ambos os caminhos; o plano não. Quando isso acontece, o caminho default-barato vence por inércia se a alternativa não for nomeada.

Em workflow YAGNI essa tensão é real: o viés natural é o caminho mais simples, e nem sempre é o que o operador tinha em mente. A correção é leve — antes do plano, nomear as opções concretas e pedir escolha. A decisão registra-se em `## Contexto` ou `## Resumo da mudança` do plano produzido, para que reviewers e execução posterior saibam por que aquele caminho.

Modo de coleta: enum via `AskUserQuestion` (ver "Convenção de pergunta ao operador") — opções nomeadas como `(a) caminho-default-barato` e `(b) caminho-rico`, com `description` carregando o trade-off concreto (custo, manutenção, virtude entregue). Operador escolhe ou usa "Other" para nomear uma terceira via que a skill não previu. Quando o operador já citou explicitamente uma das opções na frase original (`/triage exportar CSV usando streaming`), pular a pergunta e registrar a escolha no plano direto.

Operacionalização no checklist de gaps de `/triage`. Sem nomear, a bifurcação fica baked-in no plano sem ter sido discutida.

## Path contract

As skills consomem **papéis**, não paths. A tabela abaixo lista a convenção default por papel — projetos com layout diferente declaram variantes via bloco de config (schema e protocolo de resolução em `CLAUDE.md` → "The role contract").

| Papel | Default | Descrição |
|-------|---------|-----------|
| `product_direction` | `IDEA.md` | O que estamos construindo e por quê. Direção de produto. |
| `ubiquitous_language` | `docs/domain.md` | Bounded contexts, linguagem ubíqua, agregados/entidades, invariantes (RNxx) — quando o domínio merece formalização. |
| `design_notes` | `docs/design.md` | Peculiaridades de integrações externas que não estão na doc oficial. |
| `decisions_dir` | `docs/decisions/` | Diretório de decisões estruturais imutáveis. Numeração e slug são responsabilidade de `/new-adr`. |
| `plans_dir` | `docs/plans/<slug>.md` | Planos multi-fase para mudanças que exigem alinhamento prévio. |
| `backlog` | `BACKLOG.md` | Lista exploratória curta — `## Próximos`, `## Em andamento`, `## Concluídos`. |
| `version_files` | _(sem default — opt-in)_ | Lista de paths a atualizar com a nova versão a cada release. Lista vazia ou ausente = papel desativado. Consumido por `/release`. |
| `changelog` | `CHANGELOG.md` | Histórico de releases. `/release` insere novo bloco no topo a cada bump. |
| `test_command` | `make test` (com `Makefile`) | Gate automático nos passos de execução. |
| (interno do plugin) | `.worktreeinclude` | Lista opcional de gitignored a replicar em worktrees novas. Consumido por `/run-plan`. |
| (agents shipados pelo plugin) | `qa-reviewer`, `security-reviewer` | Baseline genérico invocado por `/run-plan` quando o bloco do plano anota `{reviewer: qa}` ou `{reviewer: security}`. Projeto consumidor pode sobrescrever via `.claude/agents/<nome>.md` (project-level vence colisão). |

Projeto que segue os defaults funciona zero-config. O caminho mais simples para começar com os defaults é gerar o projeto com [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit), template companion — qualquer layout alinhado à filosofia também funciona.

## Convenção de naming

Skills e hooks stack-specific convivem no mesmo plugin com componentes genéricos. O nome carrega o contrato:

| Tipo | Genérico | Stack-specific |
|------|----------|----------------|
| Hook (script) | `<purpose>.py\|.sh` (ex.: `block_env.py`) | `<purpose>_<stack>.py\|.sh` (ex.: `run_pytest_python.py`) |
| Skill (frontmatter `name`) | `<verb>-<artifact>` (ex.: `new-adr`) **ou** `<verb>` quando o artefato emerge da decisão da skill (ex.: `triage`) | `<verb>-<artifact>-<stack>` (ex.: `gen-tests-python`) |
| Agent (frontmatter `name`) | `<role>` (ex.: `code-reviewer`, `qa-reviewer`, `security-reviewer`) | `<role>-<stack>` (apenas se os princípios mudarem com a stack) |

Skill cujo output é fixo (sempre produz um ADR, sempre executa um plano) carrega `<verb>-<artifact>` — o nome promete o output. Skill cujo output é decidido a cada invocação entre múltiplas opções (ex.: `/triage` decide entre linha de backlog, plano, ADR ou atualização de domínio) carrega só `<verb>` — sufixo fixo seria mentira sobre o que sai.

Componentes que **geram ou executam** algo da stack (skills geradoras de código, hooks que invocam toolchain) precisam de sufixo — sintaxe ou comando concreto não tem versão neutra. Componentes que **revisam princípios** lidos do diff não precisam — o stack está no próprio diff.

Skill é invocada pelo usuário — sufixo de stack é declaração explícita de acoplamento. Hook dispara sozinho em todo projeto onde o plugin está instalado, então precisa de **auto-gating triplo**:

1. **Extensão do arquivo** — `if not file_path.endswith(".py"): exit 0` filtra a maioria dos casos sem custo.
2. **Marcador de stack** — caminhar pelos ancestrais procurando `pyproject.toml` (Python), `build.gradle*`/`pom.xml` (JVM), etc. Sem marcador, exit 0.
3. **Toolchain** — só executar a ferramenta (`uv run pytest`, `gradle test`) com fallback razoável; se a toolchain não existe, exit 0.

Isso torna seguro shipar `run_pytest_python.py` no mesmo plugin que `run_gradle_test_java.sh`: cada hook é silente em projetos fora da sua stack, sem flags nem env vars para desligar.

## Convenção de idioma

Skills e agents adaptam-se ao idioma do projeto consumidor — prosa dirigida ao operador, relatórios de revisores, headers de templates (planos, ADRs, backlog) e nomes de teste seguem o idioma já em uso. **Critério mecânico:** sinal claro = ≥70% dos artefatos textuais existentes (em ordem de peso: `IDEA.md` > ADRs > planos > `BACKLOG.md`) estão no idioma X. Empate ou ausência → default canonical PT-BR (origem do toolkit). Operador pode forçar via `language: pt|en|...` no bloco de config (chave reservada).

**Hooks são exceção** — mecânica universal, mensagens de erro/bloqueio sempre em inglês, independentemente do idioma do projeto. Hook é diagnóstico operacional, não prosa do produto.

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

- **Enum** via `AskUserQuestion`: opções discretas e mutualmente exclusivas, header curto (≤12 chars), 2-4 opções por pergunta, "Other" automático como válvula para nuance imprevista. Use quando a resposta esperada é um nome/escolha concreto — bifurcação A vs B, tri-state estruturado (`path | "não temos" | <other path>`), confirmação `(s/n)`, multi-seleção de lista discreta (com `multiSelect: true`). Múltiplas perguntas relacionadas podem entrar numa única chamada (até 4). Skills carregam trade-offs concretos no `description` de cada opção; descrição-óbvia tipo "escolha A" é sintoma de enum cosmético.
- **Prosa** (texto livre na conversa): use quando a resposta exige explicação, exemplo, justificativa, ou descrição naturalmente aberta — relato de sintoma em `/debug`, forma de dado real em validação manual não-determinística, especificação de cenário, gap report, confirmação "ok, valido" após validação manual, listagem de itens fora-de-escopo emergidos. Quando a maioria das respostas reais cairia em "Other" do enum, o modo certo era prosa desde o início.

**Não perguntar por valor único derivado.** Quando o valor é 100% derivado de decisão já confirmada upstream (ex.: mensagem de commit mecânica após bump confirmado, nome de tag após formato detectado, conteúdo de arquivo gerado a partir de template), pular o confirm. Janela de "abort tardio" vem de tornar visível antes de aplicar — `git status` antes do commit, diff antes do write — não de cerimônia adicional. Confirms acumulam para ações irreversíveis ou destrutivas (push, force, drop), não para mecânica derivada. Skills que precisam aplicar N valores derivados da mesma decisão consolidam num gate único, mostrando todos os valores juntos.

## Linguagem ubíqua na implementação

`docs/domain.md` (papel `ubiquitous_language`) é base **de interpretação E de desenvolvimento**: bounded contexts e linguagem ubíqua só são pilares se chegarem ao código. Vocabulário registrado no domínio mas ausente nos identificadores produzidos vira ornamento de alinhamento — exatamente o que a frase-tese rejeita.

Pipeline de três estágios:

1. **`/triage` (alignment) extrai termos tocados.** O passo 1 lê `ubiquitous_language` e identifica bounded contexts, agregados/entidades, RNs e conceitos ubíquos que o pedido toca. O passo 4 grava esse subconjunto no `## Contexto` do plano como `**Termos ubíquos tocados:** <Termo> (<categoria>), ...`. Pedidos que não tocam o domínio (refactor puro, doc-only) seguem sem a linha.
2. **`/run-plan` (execução) lê o plano.** Não relê `docs/domain.md` — o plano é o ponto único de transferência entre alinhamento e execução. Plano sem a linha = mudança não toca domínio = nada a carregar.
3. **`code-reviewer` (revisão) valida no diff.** Identificador novo que representa conceito declarado em `ubiquitous_language` deve usar o termo declarado, não sinônimo improvisado.

Papel `ubiquitous_language` resolveu para "não temos" → `/triage` não lista termos, plano sai sem a linha, `code-reviewer` não flagga. Toda a cadeia segue funcional sem fricção em projetos que ainda não formalizaram domínio.
