---
name: draft-idea
description: Elicita IDEA.md (papel product_direction) via interview estruturado quando o operador tem ideia vaga. Use upstream de /triage, quando a intenção ainda não está formada.
disable-model-invocation: false
roles:
  required: [product_direction]
---

# draft-idea

Produz `IDEA.md` no papel `product_direction` (default: `IDEA.md`) via elicitação estruturada multi-turn — problema, persona/usuário, restrições, critérios de sucesso, alternativas descartadas. Opera **upstream** de `/triage`: quando o operador chega com ideia vaga (sem problema bem-definido, sem persona clara, sem critério de sucesso), `/draft-idea` conduz interview dirigido e cristaliza a direção no artefato. Quando a intenção já está concreta, usar `/triage` direto.

Esta skill cria/edita o arquivo e devolve o controle ao operador. **Não faz commit** — operador commita conforme a convenção do projeto.

## Sub-fluxo de presença

Variante da track "Oferecer criação canonical via enum" do [ADR-003](../../docs/decisions/ADR-003-frontmatter-roles.md) — em vez de cancelar quando o papel está ausente, a presença determina **modo de operação**:

- `<product_direction>` ausente → modo **one-shot full** (skill conduz interview completo e cria o artefato no path canonical).
- `<product_direction>` presente → modo **update seção-a-seção** (skill oferece enum multi-select listando as 5 seções; operador escolhe quais revisar; skill reconduz elicitação só nessas, preservando demais intactas).

Paralelo direto com `/new-adr` (que cria via enum quando `decisions_dir` ausente). Aqui presença não cancela — estende para modo edit.

## Argumentos

Ideia em frase curta (opcional). Exemplo: `/draft-idea "uma ferramenta pra ajudar com brainstorm de features"`. Sem argumento → skill pede no início (uma pergunta livre de prosa, não enum).

## Passos

Instrumentação de progresso via Tasks per [ADR-010](../../docs/decisions/ADR-010-instrumentacao-progresso-skills-multi-passo.md): 5 passos substantivos com lifecycle `pending` → `in_progress` → `completed`. Skip silente quando o operador encerra cedo (modo update com zero seções escolhidas).

### 1. Resolver papel `product_direction` e decidir modo

Aplicar Resolution protocol do CLAUDE.md sobre `product_direction`. Probe canonical → consulta CLAUDE.md → operador (tri-state) → memoização.

Path resolvido:

- Arquivo **ausente** → modo **one-shot full** (passo 2).
- Arquivo **presente** → modo **update** (passo 3).

### 2. Modo one-shot — interview completo

Conduzir elicitação multi-turn cobrindo as 5 seções, **em ordem**. **Perguntas vivem nesta prosa do SKILL.md** — o `templates/IDEA.md` carrega comentários HTML descritivos (guias-de-conteúdo de cada seção para revisões manuais futuras), não perguntas dirigidas ao operador. Decisão F2 do design-reviewer no plano: algoritmo de perguntas mora aqui, esqueleto mora no template. Tom: estruturador, não inquisidor; ≤2 perguntas por seção, depois prosseguir (a regra "Não fazer interview exaustivo" de `## O que NÃO fazer` aplica-se aqui).

Argumento da skill (se houver) entra como contexto inicial — não como resposta automática a alguma seção.

**Seção 1 — Problema.** Prosa livre. Pergunta-âncora: "Qual é o problema concreto que motivou a ideia? Quem sofre com ele hoje, de que forma?". Cutucada de follow-up se a resposta confundir problema com solução: "Isso descreve o como; o problema (estado de mundo a mudar) é qual?".

**Seção 2 — Persona / usuário.** Prosa livre. Pergunta-âncora: "Quem usa a solução? Em qual contexto opera? Que dor enfrenta hoje sem ela?". Múltiplas personas → operador lista separadamente.

**Seção 3 — Restrições.** Enum multi-select via `AskUserQuestion` (header `Restrições`, multiSelect: true) com categorias comuns como opções:

- `Stack/integração compulsória` — sistema preexistente, biblioteca core obrigatória, contrato de integração estável.
- `Regulatória/compliance` — LGPD, GDPR, certificação, contrato.
- `Prazo` — janela definida, evento externo.
- `Recursos` — orçamento, time, infraestrutura.

`Other` (automático) → operador descreve restrição custom em prosa livre. Sem restrições conhecidas → operador escolhe `Other` e responde "nenhuma identificada". Nada selecionado é estado válido — seção fica vazia no `IDEA.md`.

**Seção 4 — Critérios de sucesso.** Prosa livre. Pergunta-âncora: "Como saberemos que a direção está dando certo? Métricas observáveis ou sinais qualitativos verificáveis.". ≥1 critério obrigatório. Critério vago ("ser útil", "ser bom") → cutucada de refinamento: "Esse critério é verificável por quem? Como?".

**Seção 5 — Alternativas descartadas.** Prosa livre, opcional. Pergunta-âncora: "Algum caminho avaliado e descartado nessa direção? Motivo curto.". Sem alternativas → seção fica vazia no `IDEA.md` (operador pode adicionar depois quando descartar algo em `/triage`).

### 3. Modo update — revisão seção-a-seção

Ler `<product_direction>` atual. Disparar `AskUserQuestion` (header `Seções`, multiSelect: true) com as 5 seções como opções:

- `Problema`
- `Persona / usuário`
- `Restrições`
- `Critérios de sucesso`
- `Alternativas descartadas`

Para cada seção escolhida, **reconduzir** a elicitação correspondente do passo 2 (mesma pergunta-âncora, mesmo enum quando aplicável), mostrando antes o conteúdo atual como referência. Seções não-escolhidas permanecem **intactas no diff** — preservação literal, sem reescrita.

Operador escolheu zero seções → skip silente, sem alteração no arquivo; pular direto para passo 5 reportando "nada a fazer".

### 4. Síntese — gravar `IDEA.md`

Ler esqueleto canônico via `${CLAUDE_PLUGIN_ROOT}/templates/IDEA.md` (não duplicar inline). Preencher cada seção com as respostas coletadas, preservando os comentários HTML originais do template (são guias-de-conteúdo para futuras revisões manuais).

Idioma: espelhar o do projeto consumidor (default canonical PT-BR per `docs/philosophy.md` → "Convenção de idioma"). Headers em PT-BR canonical; conteúdo das seções no idioma das respostas do operador.

**Modo one-shot:** sobrescrever path canonical (arquivo não existia). **Modo update:** edits cirúrgicos só nas seções escolhidas, preservando demais idênticas ao estado pré-execução.

### 5. Relatório

Ordem fixa do relatório final, três linhas potenciais:

1. **Path do arquivo gravado** — confirmação literal do path.
2. **Sugestão de próximo passo** — `próximo passo: /triage <intenção concreta>` (paralelo à cutucada do `/init-config` em ADR-017). Operador pode ignorar; a sugestão materializa o pipeline `/draft-idea` → `/triage`.
3. **Cutucada de descoberta** (per [ADR-017](../../docs/decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md) + [ADR-029](../../docs/decisions/ADR-029-cutucada-descoberta-cobre-claude-md-ausente.md)) — **última linha** do relatório. Escolher caminho conforme estado de `CLAUDE.md`:

   - **`CLAUDE.md` ausente** + a string abaixo não aparece no contexto visível desta conversa CC → emitir:
     > Dica: este projeto não tem `CLAUDE.md`. Crie o arquivo e rode `/init-config` para configurar os papéis do plugin.
   - **`CLAUDE.md` presente** + `grep -q '<!-- pragmatic-toolkit:config -->' CLAUDE.md` retorna não-zero (marker ausente) + a string abaixo não aparece no contexto visível → emitir:
     > Dica: este projeto não declara o bloco `pragmatic-toolkit:config` no CLAUDE.md. Rode `/init-config` para configurar todos os papéis de uma vez.
   - **`CLAUDE.md` presente com marker** OU **dedup hit na string aplicável** → suprimir silenciosamente.

## O que NÃO fazer

- Não inventar conteúdo — operador é a fonte; skill **estrutura** o interview, não preenche por conta própria. Resposta vazia/genérica → cutucar uma vez, depois aceitar e seguir (não pressionar).
- Não fazer interview exaustivo — ≤2 perguntas por seção, depois prosseguir. Quem chega com ideia vaga não sabe todas as respostas; forçar resposta detalhada vira teatro.
- Não detectar inconsistências cross-seção (ex.: critério de sucesso que não bate com persona declarada) — limitação registrada em [ADR-027](../../docs/decisions/ADR-027-skill-draft-idea-elicitacao-product-direction.md) § Consequências. Operador é responsável pela coerência global.
- Não invocar `/triage` automaticamente — só **sugere** no relatório (passo 5). Operador é quem dispara o próximo passo.
- Não codificar perguntas em comentários HTML do `templates/IDEA.md` — template carrega só guias-de-conteúdo descritivos; perguntas vivem no passo 2 desta prosa (decisão F2 do design-reviewer no plano).
