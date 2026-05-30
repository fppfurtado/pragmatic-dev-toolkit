# Philosophy

`pragmatic-dev-toolkit` codifica um workflow específico. Esta página descreve a filosofia que ele assume e o **path contract** que as skills esperam encontrar no projeto consumidor.

## Princípios fundamentais

Três princípios epistêmicos orientaram o design deste toolkit; as regras pragmáticas que vêm a seguir — YAGNI por padrão, flat sobre cerimônia, ausência de defensividade ornamental — materializam essas raízes.

> *Esta seção descreve o que o toolkit assume; não é prescrição ao leitor.*

### Busca pela verdade

O toolkit assume que verificar antes de assumir e medir antes de generalizar produz software mais confiável que hand-waving. O que existe, existe — falsificável vence raciocínio circular. Este princípio orientou o design quando reviewers exigem `Read` defensivo do arquivo-alvo antes da análise, quando `/run-plan` materializa baseline automático antes do loop de blocos, e quando `/debug` exige reprodução do sintoma antes de hipotetizar a causa-raiz.

### Excelência sem over-engineering

O toolkit assume que qualidade serve o problema concreto, não vice-versa. YAGNI define o que **não** precisa ser feito; excelência define **como bem** fazer o que precisa. Este princípio orientou o design quando reviewers separam YAGNI (não construir abstração prematura) de cuidado (escrever o código que existe com clareza e correção), e quando a doutrina rejeita defensividade ornamental sem renunciar à validação onde há risco real.

### Navalha de Ockham

O toolkit assume que não multiplicar entidades além do necessário é virtude operacional. Ockham é a versão dimensional do YAGNI: não só "não implementar o que não usa", mas "não modelar o que não distingue". Este princípio orientou o design quando o toolkit prefere papéis sobre arquiteturas formais, quando reviewers flagram interfaces especulativas e abstrações sem dor real, e quando a doutrina prefere refatorar mais tarde à abstração antecipada.

**Triangulação.** Verdade descobre o que é; excelência engaja seriamente com o descoberto; Ockham previne que o engajamento invente o que não estava ali. Verdade sem excelência fica passiva; excelência sem Ockham vira over-engineering; Ockham sem verdade vira reducionismo cego. As três condições atuam juntas — qualquer uma isolada deteriora. Em casos concretos, a ordem de aplicação é contextual: investigação tende a partir de Verdade (reproduzir o que existe antes de hipotetizar); proposta de estrutura tende a partir de Ockham (o mínimo viável antes da expansão). A ordem emerge da natureza da decisão, não de hierarquia fixa.

**Mapping para a doutrina pragmática abaixo.** YAGNI/flat ↔ Ockham (operacionaliza parsimônia dimensional). "Sem defensividade desnecessária" ↔ Verdade (validar onde há risco real, não onde imaginamos). "Pragmática" — sem aspiracional schema-perfeição — ↔ Excelência (qualidade dentro do escopo, sem virar perfeccionismo).

**Quando YAGNI termina.** YAGNI por padrão é Ockham aplicado ao desconhecido — *"não modelar o que não distingue ainda"*. Ele cede quando Verdade já tem evidência: ≥3 aplicações ad hoc do mesmo pattern em casos reais (auditável retroativamente, conforme [ADR-043](decisions/ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § Ockham operacionalizado critério 4) é o ponto onde a abstração ganha seu custo. Até esse ponto, o toolkit prefere o caminho concreto, refatorando quando o pattern empiricamente se confirmar.

## A filosofia em uma frase

**Bounded contexts e linguagem ubíqua sim, cerimônia tática não.** Bounded contexts (DDD estratégico) e vocabulário compartilhado entre código e negócio são fundamentais. Já a cerimônia tática (camadas formais `application/`/`domain/`/`infrastructure/`, ports/adapters universais, mappers em cascata) cria muitos arquivos para pouco valor — adicionar abstração só quando há **dor real** (uma integração instável, uma substituição prevista). YAGNI por padrão.

Refatorar mais tarde costuma ser mais barato do que abstrair cedo.

## Nomear bifurcações arquiteturais

Há pedidos que admitem dois ou mais caminhos com custo, manutenção ou modelo mental significativamente diferentes — verbos abertos ("registrar", "validar", "notificar", "processar", "armazenar", "interagir") são sintoma frequente. A frase do operador satisfaz ambos os caminhos; o plano não. Quando isso acontece, o caminho default-barato vence por inércia se a alternativa não for nomeada.

Em workflow YAGNI essa tensão é real: o viés natural é o caminho mais simples, e nem sempre é o que o operador tinha em mente. A correção é leve — antes do plano, nomear as opções concretas e pedir escolha. A decisão registra-se em `## Contexto` ou `## Resumo da mudança` do plano produzido, para que reviewers e execução posterior saibam por que aquele caminho.

Modo de coleta: enum via `AskUserQuestion` (ver "Convenção de pergunta ao operador") — opções nomeadas como `(a) caminho-default-barato` e `(b) caminho-rico`, com `description` carregando o trade-off concreto (custo, manutenção, virtude entregue). Operador escolhe ou usa "Other" para nomear uma terceira via que a skill não previu. Quando o operador já citou explicitamente uma das opções na frase original (`/triage exportar CSV usando streaming`), pular a pergunta e registrar a escolha no plano direto.

Operacionalização no checklist de gaps de `/triage`. Sem nomear, a bifurcação fica baked-in no plano sem ter sido discutida.

## Brainstorm/exploração não-codificado

Brainstorm/exploração de ideias e abordagens é **intencionalmente não-codificado** como skill no toolkit. Raw-chat com Claude é a ferramenta primária — o operador conduz diálogo informal até intenção cristalizar, depois entra no pipeline estruturado (`/draft-idea` para direção de projeto, `/triage` para alinhamento e decisão de artefato, `/debug` para diagnóstico, `/new-adr` para decisão estrutural). Skills cobrem cenários com fronteiras nítidas e output materializável; trabalho inerentemente exploratório resiste a essa codificação sem virar entrevista exaustiva (ver `/triage` step 2) ou competir com skills existentes. Detalhes, alternativas analisadas e gatilhos de revisão em [ADR-036](decisions/ADR-036-brainstorm-intencionalmente-nao-codificado-em-skill.md).

## Path contract

As skills consomem **papéis**, não paths literais. Projeto declara variantes uma vez via bloco de config; layout diferente do canonical é cidadão de primeira classe, não exceção. O que importa em runtime é a função do arquivo (direção de produto, linguagem ubíqua, plano de mudança), não o nome.

Tabela canônica de papéis (papel | default | descrição) e protocolo de resolução em `CLAUDE.md` → "The role contract" — fonte única de verdade.

Projeto que segue os defaults funciona zero-config. O caminho mais simples para começar com os defaults é gerar o projeto com [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit), template companion — qualquer layout alinhado à filosofia também funciona.

## Convenção de naming

A convenção separa três categorias por critério de acoplamento à stack:

- **Agents reviewers** (revisam princípios lidos do diff) não carregam sufixo — o stack está no próprio diff.
- **Skills geradoras** (ex.: `/gen-tests`) **não** carregam sufixo: idioms da stack vivem em sub-blocos por stack dentro do mesmo SKILL.md, e a skill detecta a stack do projeto consumidor por marker (`pyproject.toml`, `build.gradle`, `package.json`, ...). Operador invoca sempre o nome genérico; UX uniforme entre stacks. Critério canônico em [ADR-008](decisions/ADR-008-skills-geradoras-stack-agnosticas.md).
- **Hooks executores de toolchain** carregam sufixo de stack + auto-gating triplo. Hook dispara sozinho em todo projeto onde o plugin está instalado, então sufixo é declaração ao autor do plugin de qual stack o componente serve, e o auto-gating triplo (extensão → marker → toolchain) garante silêncio fora da stack alvo — sem flags nem env vars para desligar.

Tabela de naming concreta e mecânica completa do auto-gating em `CLAUDE.md` → "Plugin component naming and hook auto-gating".

## Convenção de idioma

Skills e agents adaptam-se ao idioma do projeto consumidor — prosa dirigida ao operador, relatórios de revisores, headers de templates (planos, ADRs, backlog) e nomes de teste seguem o idioma já em uso. **Critério mecânico:** sinal claro = ≥70% dos artefatos textuais existentes (em ordem de peso: `IDEA.md` > ADRs > planos > `BACKLOG.md`) estão no idioma X. Empate ou ausência → default canonical PT-BR (origem do toolkit). Operador pode forçar via `language: pt|en|...` no bloco de config (chave reservada).

**Hooks são exceção** — mecânica universal, mensagens de erro/bloqueio sempre em inglês, independentemente do idioma do projeto. Hook é diagnóstico operacional, não prosa do produto.

O que **não** muda com idioma: nomes de agents, chaves de frontmatter, paths e identificadores de código. Esses elementos pertencem à mecânica do toolkit, não ao discurso do projeto, e ficam sempre em inglês para legibilidade cross-stack. Mensagens de commit têm convenção própria — ver "Convenção de commits".

**Artefatos informativos do registro de mudanças** — `CHANGELOG.md`, mensagens de tag anotada (incluindo síntese), descrições de PR — seguem o idioma da **convenção de commits do projeto** (ver abaixo), não o da prosa operativa. Audiência diferente: leitor de release inspeciona junto com `git log`, prosa operativa é dev escrevendo/lendo durante desenvolvimento. Detalhes em [ADR-007](decisions/ADR-007-idioma-artefatos-informativos.md).

**Artefatos de discoverability/landing** — `README.md` do plugin e descrições em manifests de marketplace (`plugin.json`, `marketplace.json`) — seguem o idioma do **público alvo do canal de descoberta** (default canonical EN para Claude Code marketplace). Audiência distinta da operativa e da informativa: leitor pré-adoção decidindo se vai instalar, em vez de dev no projeto ou leitor de release. Detalhes em [ADR-012](decisions/ADR-012-idioma-artefatos-discoverability-landing.md).

`/run-plan` faz **matching semântico** dos headers de plano — canonical PT-BR é `## Arquivos a alterar`, `## Verificação end-to-end`, `## Verificação manual`, `## Contexto`, `## Resumo da mudança`; equivalentes em outro idioma do projeto (`## Files to change`, `## End-to-end verification`, etc.) são aceitos contanto que a estrutura informacional bata.

## Convenção de commits

Quando `/run-plan` produz micro-commits, segue a **política de mensagens de commit do projeto consumidor**. A pista de qual política usar é, em ordem:

1. **Política explícita** declarada no projeto — bloco no CLAUDE.md, `CONTRIBUTING.md`, `.gitmessage`, hook de commitlint, ou equivalente.
2. **Padrão observado no histórico** — `git log` recente. **Critério mecânico:** predomínio claro = ≥70% dos últimos 50 commits seguem o mesmo padrão extraível (Conventional Commits, gitmoji, prefixos custom tipo `[FEAT]`, idioma específico). Repo com <50 commits → últimos 20.
3. **Default canonical** — [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `style:`) com mensagens em **inglês**. Aplicado quando não há política explícita e o histórico não revela padrão extraível (repo novo, commits ad-hoc).

A regra "um micro-commit por bloco do plano" permanece invariante — pertence à mecânica de execução, não à política de mensagem. `--amend` e rebase de commits de blocos já fechados ficam proibidos pelo mesmo motivo; emendar o último commit do bloco corrente quando faz sentido (typo, arquivo esquecido) é exceção localizada, não regra.

O idioma extraído desta convenção rege também os artefatos informativos (CHANGELOG, tag annotations, PR descriptions) — ver acima.

## Convenção de pergunta ao operador

Skills perguntam em dois modos complementares — **enum** (escolha discreta) e **prosa livre** — e a escolha entre eles não é estética: errar o modo gera ou cerimônia (enum em pergunta livre) ou improviso (prosa em escolha discreta). Use enum quando a resposta esperada é um nome/escolha concreto; use prosa quando a resposta exige explicação, exemplo, justificativa, ou descrição naturalmente aberta. Quando **todas** as respostas comuns cairiam em "Other" do enum (descrição livre, justificativa, exemplo), o modo certo era prosa desde o início. Mas se ≥1 resposta comum é discreta, prefira enum mesmo assim — `Other` cobre as livres (ADR-006).

**Não perguntar por valor único derivado.** Quando o valor é 100% derivado de decisão já confirmada upstream (ex.: mensagem de commit mecânica após bump confirmado, nome de tag após formato detectado, conteúdo de arquivo gerado a partir de template), pular o confirm. Janela de "abort tardio" vem de tornar visível antes de aplicar — `git status` antes do commit, diff antes do write — não de cerimônia adicional. Confirms acumulam para ações irreversíveis ou destrutivas (push, force, drop), não para mecânica derivada. Skills que precisam aplicar N valores derivados da mesma decisão consolidam num gate único, mostrando todos os valores juntos.

Mecânica concreta de `AskUserQuestion` (limites de header, contagem de opções, `multiSelect`, exemplos de uso) em `CLAUDE.md` → "AskUserQuestion mechanics".

## Linguagem ubíqua na implementação

Bounded contexts e linguagem ubíqua só são pilares se chegarem ao código. Vocabulário registrado no domínio mas ausente nos identificadores produzidos vira ornamento de alinhamento. Pipeline operacional vive em skills/agents; aqui só o princípio.

Papel `ubiquitous_language` resolveu para "não temos" → toda a cadeia segue funcional sem fricção em projetos que ainda não formalizaram domínio.
