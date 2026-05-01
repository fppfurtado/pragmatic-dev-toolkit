# Adicionar gap "Bifurcação arquitetural" ao checklist de `/new-feature`

## Contexto

A skill `/new-feature` enumera áreas comuns de gap como checklist mental: escopo, superfícies além do código, invariantes, integrações, persistência, aprendizado de domínio, validação manual. Falta cobertura para um modo de falha frequente em features ambíguas: pedidos onde duas ou mais implementações satisfariam a frase do operador, mas levam a planos materialmente diferentes (custo, manutenção, UX, modelo mental). Sem nomear a bifurcação, a IA assume o caminho mais barato por inércia, e a escolha arquitetural fica baked-in no plano sem ter sido discutida.

Caso real que motivou a mudança: o pedido "registrar pagamento por linguagem natural via Telegram" foi planejado como slot-filling com extrator NLU stateless; a intenção do operador era um agente conversacional onde o LLM conduz a conversa. As duas implementações satisfaziam o pedido literal mas resultavam em UX, código e custo profundamente diferentes. O plano nasceu enviesado para o caminho barato — não por má-fé, mas por inércia YAGNI sem o operador ter sido confrontado com a alternativa.

A correção precisa ser **genérica** (vale para qualquer feature com bifurcação, não só conversacional) e respeitar a filosofia: sem cerimônia nova, sem artefato extra, sem violar o limite "1-2 perguntas no máximo" exceto quando a heurística específica dispara.

## Resumo da mudança

Caminho escolhido (vs alternativas mínimo / release-aware): **princípio consagrado** — a noção de "nomear bifurcações antes de codar" sobe a `docs/philosophy.md` como princípio durável do toolkit, e a operacionalização dela vai para o checklist de gaps em `/new-feature`. Bump patch da versão (0.3.0 → 0.3.1) por ser comportamento aditivo (não quebra clientes existentes).

Três blocos:

1. **Princípio em `docs/philosophy.md`**: nova subseção curta após "A filosofia em uma frase" — explica o que é bifurcação arquitetural, por que nomear, como o toolkit lida com ela.
2. **Operacionalização em `skills/new-feature/SKILL.md`**: novo bullet no checklist de gaps + parágrafo de exceção à regra "1-2 perguntas" + ajuste correspondente em "O que NÃO fazer".
3. **Release**: entrada no `CHANGELOG.md` sob `[0.3.1]`, bump em `plugin.json` e `marketplace.json`.

Outras skills (`run-plan`, `new-adr`, `gen-tests-python`) e agents (revisores) **não** mudam — bifurcação é problema de alinhamento, não de execução nem de revisão.

## Arquivos a alterar

### `docs/philosophy.md` {revisor: code}

- Adicionar subseção `## Nomear bifurcações arquiteturais` após `## A filosofia em uma frase` e antes de `## Path contract`.
- Conteúdo: 2-3 parágrafos curtos. Definir bifurcação ("um pedido pode ser resolvido por dois ou mais caminhos com custo, manutenção ou modelo mental significativamente diferentes"); explicar por que isso é tensão real em workflow YAGNI ("default barato vence por inércia se a alternativa não for nomeada"); afirmar a postura ("antes do plano, nomear opções e pedir escolha; a escolha vai para o `## Contexto` ou `## Resumo da mudança` do plano produzido").
- Tom paralelo às outras subseções: declarativo, sem listas longas, sem exemplos por domínio. Verbos abertos como "registrar/validar/notificar/processar/armazenar/interagir" podem entrar como ilustração curta dentro de um parágrafo, não como bloco enumerado.

### `skills/new-feature/SKILL.md` {revisor: code}

- No passo 2 ("Esclarecer gaps com o usuário"), adicionar bullet ao checklist:
  > **Bifurcação arquitetural:** o pedido pode ser resolvido por dois ou mais caminhos com custo, manutenção ou modelo mental significativamente diferentes? Heurística: ao tentar mentalmente esboçar o plano, você consegue redigir dois planos distintos que ambos satisfazem a frase do operador, mas levam a estruturas, dependências ou UX diferentes? Verbos abertos ("registrar", "validar", "notificar", "processar", "armazenar", "interagir") são sintoma frequente. Ver `docs/philosophy.md`.
- Após o checklist, adicionar parágrafo de exceção à regra "1-2 perguntas":
  > Quando bifurcação é detectada, **uma pergunta nominal-comparativa é obrigatória** antes do plano, mesmo passando do limite de 1-2 perguntas. Forma canônica: *"Para X, prefere (a) caminho-default-barato ou (b) caminho-rico? Trade-off: (a) é mais simples e mais barato; (b) entrega <virtude-B> ao custo de <custo-B>."* A escolha vai para o `## Contexto` ou `## Resumo da mudança` do plano produzido — sem nomear, o caminho barato vence por omissão.
- Em "O que NÃO fazer", qualificar o item existente: `Não fazer entrevista exaustiva de requisitos. 1–2 perguntas bloqueantes, no máximo` → adicionar sufixo "**exceto** quando bifurcação arquitetural for detectada (ver passo 2)".

### `CHANGELOG.md` {revisor: code}

- Adicionar nova seção `## [0.3.1] - <data-do-merge>` no topo (após o cabeçalho, antes de `[0.3.0]`).
- Bullet sob `### Added`: "Skill `/new-feature`: gap 'Bifurcação arquitetural' no checklist + exceção à regra '1-2 perguntas' quando o pedido admite múltiplas implementações materialmente diferentes."
- Bullet sob `### Added`: "Princípio 'Nomear bifurcações arquiteturais' em `docs/philosophy.md`."

### `.claude-plugin/plugin.json` {revisor: code}

- Bump `version`: `"0.3.0"` → `"0.3.1"`.

### `.claude-plugin/marketplace.json` {revisor: code}

- Bump `plugins[0].version`: `"0.3.0"` → `"0.3.1"` (manter sincronia com `plugin.json`).

## Verificação end-to-end

Inspeção textual (sem `make test` — o plugin é meta-tool sem suíte automatizada):

1. `grep -n "Bifurcação arquitetural" skills/new-feature/SKILL.md` → 1 ocorrência (item do checklist).
2. `grep -n "nominal-comparativa" skills/new-feature/SKILL.md` → 1 ocorrência (parágrafo de exceção).
3. `grep -n "Nomear bifurcações" docs/philosophy.md` → 1 ocorrência (cabeçalho da subseção).
4. Versão coerente em três lugares: `plugin.json`, `marketplace.json`, `CHANGELOG.md` apontam para `0.3.1`.

## Verificação manual

Plugin é meta-tool: a validação real é observar a skill em comportamento. Três smoke tests, cada um confirmado por inspeção do output da IA num projeto consumidor:

1. **Trigger ativa em pedido ambíguo.** Invocar `/new-feature salvar histórico de conversas dos usuários` num projeto que não tem persistência declarada. A IA deve nomear ao menos duas opções (memória vs SQLite/persistência) com trade-off explícito antes de propor plano.
2. **Trigger não ativa em pedido sem bifurcação.** Invocar `/new-feature adicionar campo email ao formulário de cadastro` num projeto que já tem o formulário. A IA deve seguir fluxo normal (1-2 perguntas no máximo, sem inflar).
3. **Replay do caso histórico.** Invocar `/new-feature registrar pagamento por linguagem natural via Telegram` no projeto `h3-finance-agent`. A IA agora deve perguntar slot-filling vs agente conversacional **antes** de produzir o plano — comportamento que falhou em campo no caso original.

Cada smoke test é "ok" ou "ajustar redação" — sem ferramenta automatizada para gate.

## Notas operacionais

- Bump é **patch** (0.3.0 → 0.3.1), não minor: a mudança é aditiva. Operadores que já usam `/new-feature` não precisam ajustar nada — a skill apenas pergunta uma vez a mais quando detectar bifurcação.
- Projeto `pragmatic-dev-toolkit` não segue strict-mode suas próprias pré-condições de path contract (não tem `IDEA.md`, `BACKLOG.md`, `docs/decisions/`). Esta divergência é conhecida (o plugin é meta-tool, não um produto que aplica suas próprias regras a si mesmo) e não é alvo deste plano.
- Não há ADR para esta mudança: o princípio mora em `docs/philosophy.md` (lugar canônico de filosofia) e a operacionalização em `SKILL.md` (lugar canônico de comportamento de skill). ADR seria duplicação.
- Próximo passo após merge: testar `/new-feature` em três projetos de stacks diferentes (Python/Telegram, web app, infra-as-code) por uma a duas semanas para calibrar a heurística de detecção. Se a IA disparar bifurcação demais (ruído) ou de menos (silêncio), refinar a redação do bullet — não há gate técnico, só feedback de uso.
