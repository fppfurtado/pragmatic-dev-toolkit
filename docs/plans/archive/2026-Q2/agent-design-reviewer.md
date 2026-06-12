# Plano — Agent design-reviewer

## Contexto

Lente diferente dos reviewers atuais: opera em **documento pré-fato** (plano em `docs/plans/<slug>.md` ou ADR draft em `docs/decisions/`), não em diff pós-fato. Foco: criticar decisões estruturais e de design **antes** que virem código.

Lacuna real: `code-reviewer`/`qa-reviewer`/`security-reviewer`/`doc-reviewer` entram via `/run-plan` por bloco, com decisões estruturais já cristalizadas no plano. Quando o autor cravou abstração prematura, esqueceu alternativa óbvia, ou contradisse ADR registrada, ninguém crítica até o diff existir — e a essa altura desfazer custa muito mais.

Escopo proposal-level: alternativas não consideradas, acoplamentos que travam mudança futura, ADR-worthiness de decisão escondida em plano, contradição com ADRs existentes ou com `docs/philosophy.md`. Mesma lente flat/YAGNI: rejeita abstração prematura, não recompensa over-engineering.

Wiring inicial: invocação manual via `@design-reviewer` (segue padrão de code/qa/security/doc-reviewer — sem skill nova). Wiring automático (gate em `/run-plan` pré-loop ou `/new-adr` pré-commit) **deferido** — decidir só após dogfood acumular evidência.

**Decisão divergente do padrão dos reviewers atuais**: free-read em runtime de `docs/decisions/` e `docs/philosophy.md` para detecção de contradição doutrinária. Reviewers atuais consomem insumo curado pelo autor do plano (e.g., `code-reviewer` recebe `**Termos ubíquos tocados:**` repassado pelo `/run-plan`). Justificativa do free-read aqui: o autor do plano frequentemente **não sabe** quais ADRs o plano contradiz (esse é exatamente o ponto cego que motiva o reviewer); curar a lista no plano transferia ao autor o trabalho que o agent deveria fazer. Custo: tokens. Aceitável para invocação manual de baixa frequência; reavaliar se virar gate automático.

**ADRs tocadas:** ADR-007 (idioma — agent prose em PT-BR canonical, conforme padrão dos reviewers).

**Linha do backlog:** plugin: agent design-reviewer — revisor pré-fato de decisões arquiteturais/design em planos e ADRs; free-read de docs/decisions e philosophy.md; invocação manual via @-mention; wiring automático deferido após dogfood.

## Resumo da mudança

1. ADR registrando a doutrina "review document-level pré-fato + free-read de doctrine sources" como caso explícito ao lado do padrão diff-level + insumo curado.
2. Criar `agents/design-reviewer.md` espelhando estrutura dos reviewers existentes (frontmatter, identidade, divisão de trabalho, categorias do que flagrar/não-flagrar, formato de relatório).
3. Atualizar `README.md` (tabela de componentes) e `CLAUDE.md` (Plugin layout, Roles and canonical defaults, Plugin component naming) para incluir `design-reviewer`.

Fora de escopo (deferido para nova triagem após dogfood): wiring automático em `/run-plan` pré-loop ou em `/new-adr` pré-commit. Captura como linha separada em `BACKLOG.md ## Próximos`.

## Arquivos a alterar

### Bloco 1 — ADR design-reviewer doutrina {reviewer: code}

- `docs/decisions/ADR-XXX-revisor-design-pre-fato.md` (criar via `/new-adr "revisor design pré-fato e free-read"`).
  - **Contexto** do ADR: padrão emergente até v1.24.0 — todos os reviewers operam em diff (pós-fato) e consomem insumo curado pelo autor do plano. `design-reviewer` introduz uma segunda camada de revisão (documento pré-fato).
  - **Decisão**: (a) reviewers podem operar em documento pré-fato ao lado de diff pós-fato; (b) `design-reviewer` usa free-read de `docs/decisions/` e `docs/philosophy.md` em runtime — o autor do plano não cura essa lista.
  - **Justificativa**: ponto cego do autor (não saber qual ADR seu plano contradiz) não pode ser resolvido transferindo a curadoria a ele.
  - **Consequências**: precedente para reviewers document-level futuros; custo de tokens em troca de cobertura autônoma; reavaliação obrigatória se `design-reviewer` virar gate automático em `/run-plan` pré-loop (alta frequência muda o trade-off).
- Reviewer do bloco: `code-reviewer` por enquanto. `design-reviewer` ainda não existe na sessão `/run-plan` no momento deste bloco (será criado no Bloco 2). Auto-revisão real do ADR fica para a `## Verificação end-to-end` pós-merge.

### Bloco 2 — agent design-reviewer {reviewer: code}

- `agents/design-reviewer.md` (novo). Frontmatter: `name: design-reviewer` + `description` curta enfatizando "revisor de decisões arquiteturais e de design em documento pré-fato (plano ou ADR draft); stack-agnóstico". Corpo:
  - Identidade + filosofia: mesma lente flat/YAGNI dos demais reviewers; rejeita abstração prematura, **não** recompensa.
  - Divisão de trabalho: `code-reviewer` (diff pós-fato; YAGNI no código), `qa-reviewer` (cobertura de teste), `security-reviewer` (segredos, fronteira, privilégios), `doc-reviewer` (drift entre doc e código).
  - **Insumo**: plano em `docs/plans/<slug>.md` OU ADR draft em `docs/decisions/ADR-XXX-*.md`. Operador aponta path via @-mention.
  - **Free-read declarado**: ler `docs/decisions/*.md` e `docs/philosophy.md` em runtime para detectar contradição. Uma passagem por invocação — não relê em loop.
  - **`## O que flagrar`** com 5 categorias:
    1. **Abstração prematura no plano** — diretórios `application/`/`domain/`/`infrastructure/` introduzidos para módulo novo; interfaces/Protocols para fronteiras estáveis; mappers em cascata; factory/builder/strategy para um único uso. Mesma lente do `code-reviewer` mas no plano, antes de virar código.
    2. **Alternativa ausente** — decisão estrutural sem mencionar a opção competidora descartada. Plano que só descreve o caminho escolhido sem rebater alternativa óbvia é decisão sem deliberação.
    3. **Acoplamento que trava mudança futura** — escolha de persistência/biblioteca/integração que cria caminho difícil de reverter; lock-in não justificado pelo problema.
    4. **ADR-worthiness não-formalizada** — decisão estrutural duradoura (forma/lugar de persistência, contrato de integração estável, política do sistema) descrita no plano sem ADR. Sinal: parágrafo do plano que se lido isoladamente seria um `## Decisão` de ADR.
    5. **Contradição com ADRs existentes ou philosophy.md** — proposta inverte/contradiz decisão registrada sem reconhecer o trade-off. Exemplo: plano introduz camada formal sob módulo de negócio sem citar a posição "flat e pragmática" de `philosophy.md`.
  - **`## O que NÃO flagrar`** (load-bearing — escopo-guarda):
    - Code-level (território do `code-reviewer` — agent só lê documento, nunca diff).
    - Cobertura de teste (`qa-reviewer`).
    - Segredos / validação de fronteira / privilégios (`security-reviewer`).
    - Drift entre identificadores citados em doc e código (`doc-reviewer`).
    - Estilo de prosa do plano (gramática, voz, ordem dos blocos) — irrelevante.
    - Decisão tática reversível com 1 PR (renomear arquivo, mudar default value) — peso desproporcional ao risco.
  - **`## Como reportar`** — idioma espelha consumidor (PT-BR canonical, ADR-007); formato `Localização` (path:linha do plano/ADR) / `Problema` (uma frase) / `Princípio violado` (YAGNI, alternativa ausente, ADR-worthy não-formalizada, contradição doutrinária) / `Sugestão` (mudança mínima ou "elevar a ADR" ou "incluir alternativa rebatida"). Documento limpo: `"Plano alinhado com a filosofia flat — nenhuma decisão pendente."`
  - Encerrar com seção `## O que NÃO fazer` (load-bearing por convenção do repo, com critério editorial — só itens não-óbvios).
- Reviewer do bloco: `code-reviewer` (mesmo motivo do Bloco 1 — auto-revisão real do agent definition fica para Verificação end-to-end pós-merge).

### Bloco 3 — README e CLAUDE.md atualizados {reviewer: doc}

- `README.md`: linha na tabela de componentes, mantendo o tom das demais — `design-reviewer | Agent | Revisor pré-fato de decisões estruturais e de design em planos e ADRs draft. Free-read de decisões/philosophy. Stack-agnóstico.`
- `CLAUDE.md`:
  - **Plugin layout (what loads what)** → adicionar `design-reviewer` à enumeração de Agents.
  - **Roles and canonical defaults** → estender a regra de shadow override de reviewers (linha "agents shipped by the plugin") para incluir `design-reviewer`.
  - **Plugin component naming** → confirmar que `design-reviewer` segue padrão `<role>` (genérico, sem stack).

## Verificação end-to-end

Repo sem suite automatizada (`test_command: null`). Gate manual via dogfood:

1. **Auto-revisão do próprio ADR.** Após o ADR criado pelo Bloco 1 ser commitado e o agent do Bloco 2 estar disponível na sessão atual (depois de fechar e reabrir Claude Code, ou após install do plugin no consumidor), invocar `@design-reviewer` apontando o ADR. Reviewer deve produzir findings genuínos ou retornar `"Plano alinhado..."`.
2. **Auto-revisão deste plano.** Invocar `@design-reviewer` apontando `docs/plans/agent-design-reviewer.md`.
3. Confirmar descoberta: `design-reviewer` aparece em `/agents` e em `subagent_type` autocomplete.

## Verificação manual

**Surface não-determinística** (comportamento de agent LLM — heurística do `/triage` step 2). Cenários enumerados:

**Forma do dado real**: planos em `docs/plans/` e ADRs em `docs/decisions/` deste próprio repo. Padrões textuais frequentes que o reviewer deve reconhecer:

- Decisão estrutural disfarçada de "implementação": "vamos usar X para persistir Y" sem ADR.
- Plano que introduz camada/interface/abstração sem rebater alternativa.
- Plano que contradiz `docs/philosophy.md` (cerimônia tática) sem reconhecer.

**Cenários** (executar em worktree do próprio toolkit, com `design-reviewer` já disponível):

1. **Plano alinhado (este).** Invocar `@design-reviewer` apontando `docs/plans/agent-design-reviewer.md`. Esperado: findings substantivos (se houver) ou `"Plano alinhado..."`. Falso positivo flagar Bloco 1 como "ADR não-formalizada" significa que o reviewer não está lendo a estrutura do plano corretamente — registrar como aprendizado.
2. **Contradição com philosophy.md (sintética).** Editar este plano sinteticamente acrescentando bloco "introduzir diretórios `application/`, `domain/`, `infrastructure/` em `agents/`". Esperado: `design-reviewer` flagga como contradição com `philosophy.md` ("cerimônia tática (camadas formais...) **não**").
3. **Alternativa ausente (sintética).** Editar este plano removendo o parágrafo que justifica o free-read (parágrafo "Decisão divergente..."). Esperado: `design-reviewer` flagga "decisão estrutural sem rebater alternativa".
4. **ADR-worthiness não-formalizada (sintética).** Pegar plano histórico que mude forma de persistência sem ADR (e.g., editar cópia de `docs/plans/d2-state-em-git.md` removendo a referência a ADR-004). Esperado: reviewer flagga ADR-worthy não-formalizada.
5. **Falso positivo defensivo (NÃO flagrar).** Plano com 3 linhas similares em blocos diferentes, ou função "longa mas linear". Esperado: reviewer **não** flagga — preferir duplicação a abstração prematura é regra explícita do `code-reviewer` que se aplica também aqui.

## Notas operacionais

- **Circularidade nos blocos 1 e 2**: o agent que está sendo criado por este plano não pode revisar os blocos que o criam. Reviewer dos blocos 1 e 2 é `code-reviewer` (fallback prático); auto-revisão real do ADR e do agent definition entra na `## Verificação end-to-end` pós-merge.
- **Discovery do agent**: após o Bloco 2 commitar `agents/design-reviewer.md`, o agent só fica visível ao `subagent_type` em sessões novas do Claude Code (ou após `/plugin install` no consumidor). A `## Verificação end-to-end` precisa de sessão fresca.
- **Free-read em runtime**: documentar explicitamente no agent prompt que ele **deve** ler `docs/decisions/*.md` e `docs/philosophy.md` antes de analisar — não confiar que esses caminhos virão como contexto implícito.
- **Read/Grep diretos, sem delegação via Task/Agent tool por ora**: volume é pequeno (~8 ADRs + `philosophy.md`), e os reviewers existentes (`code/qa/security/doc-reviewer`) não usam delegação — manter consistência reduz superfície de revisão. Trade-off considerado: subagent começaria frio com briefing duplicado da proposta a cada spawn, anulando boa parte da economia de contexto. Revisitar se wiring automático em `/run-plan` pré-loop materializar (alta frequência muda o cálculo).
- Idioma do prompt do agent espelha consumidor (PT-BR canonical), seguindo padrão dos demais reviewers (ADR-007).
