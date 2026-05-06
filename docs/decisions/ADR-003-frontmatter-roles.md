# ADR-003: Frontmatter declarativo `roles:` nas SKILLs

**Data:** 2026-05-06
**Status:** Aceito

## Origem

- **Investigação:** Revisão arquitetural pós-v1.20.0 contou ~5-10 linhas de prosa de "Pré-condições" repetidas em cada uma das 8 skills, todas dizendo a mesma coisa: "para cada papel necessário aplicar Resolução de papéis; <fulano> é required; <ciclano> é informational". A enumeração de papéis vive na prosa do SKILL.md mas o **comportamento** é mecânica universal — cabe melhor em frontmatter declarativo + regra única em CLAUDE.md.

## Contexto

Skills do plugin consomem **papéis** declarados em CLAUDE.md → "The role contract". Cada skill precisa saber: quais papéis usa, quais são required, quais são informational. Hoje essa informação está em **prosa livre** na seção `## Pré-condições` de cada SKILL.md.

Custos do estado atual:

- **Duplicação**: 8 skills × ~5-10 linhas = ~40-80 linhas repetindo o mesmo protocolo (probe → CLAUDE.md → ask).
- **Drift potencial**: skill nova pode esquecer de declarar um papel; skill existente pode listar role na prosa mas não tratar corretamente o "não temos".
- **Verificabilidade**: sem schema formal, validação é leitura humana de cada SKILL.md.
- **Manutenção**: quando regra geral muda (ex.: ADR-001 introduziu sub-fluxo de criação canonical), todas as skills precisam ser editadas em prosa.

Frontmatter da skill já carrega contrato (`name`, `description`, `disable-model-invocation`). Adicionar `roles:` é extensão natural.

## Decisão

**Cada skill declara seus papéis em `roles:` no frontmatter, separados em `required` e `informational`.** Comportamento default vem da categoria; sub-fluxos especiais (criação canonical, condicionais) ficam em prosa do SKILL.

### Schema

```yaml
---
name: <skill-name>
description: <...>
roles:
  required: [<role>, ...]
  informational: [<role>, ...]
---
```

- `roles` é objeto com duas listas opcionais.
- Listas vazias podem ser omitidas (`roles: {}` ou ausência da chave).
- Skill sem `roles:` declarado é gap de migração — todas as skills do plugin migram juntas no Batch 3/B2.

### Comportamento default por categoria

Resolution protocol (CLAUDE.md → "Resolution protocol") aplica-se a cada role declarado:

- **Required ausente** (probe falhou + sem variante em CLAUDE.md + sem path do operador): skill **não pode prosseguir**. Comportamento herda um dos 3 trilhos:
  - **Captura imediata + para** — quando o problema é estado do projeto/setup. Ex.: `/run-plan` precondição 3 (baseline vermelho), 4 (worktree órfã).
  - **Oferecer criação canonical via enum** — quando o role tem default canônico claro e a skill pode criar. Ex.: `/triage` step 4 → `Criar em <path>` / `Não usamos esse papel`; `/new-adr` ao criar `docs/decisions/` na primeira invocação.
  - **Informa e para** (default) — quando o role é o próprio BACKLOG (paradoxo de capturar onde) ou a skill não pode resolver e operador precisa criar manualmente. Ex.: `/heal-backlog`/`/next` sem `backlog`.

  Cada SKILL.md declara em prosa qual trilho aplica para seus required (quando diferente do default "informa e para").

- **Informational ausente**: skill **segue silente**. Sem captura, sem mensagem extra. Reduz a base de hipóteses/contexto, nunca bloqueia. Ex.: `/debug` com `ubiquitous_language` ausente — segue sem listar invariantes documentadas como hipótese.

### Sub-fluxos especiais

Casos que escapam do schema e ficam em prosa do SKILL:

- **Condicionais**: `/run-plan` precondição 3 — `test_command` é required quando o plano não tem `## Verificação end-to-end`, informational quando tem. Schema declara informational; prosa explica o caso condicional.
- **Stack contradiction**: `/gen-tests-python` recusa quando `pyproject.toml` ausente. Não é gap de papel (`pyproject.toml` não é role) — é contradição de stack assumida pela skill. Permanece em prosa.
- **Criação canonical via enum**: `/triage` step 4 e `/new-adr` propõem criar canonical (com oferta de memorização). Mecanismo específico que não cabe no schema; em prosa.

### CLAUDE.md absorve a regra de despacho

CLAUDE.md → "Resolution protocol" ganha parágrafo declarando o despacho automático: "Cada skill declara `roles.required` e `roles.informational` no frontmatter. O Resolution protocol abaixo aplica-se a cada role: required ausente → comportamento default (informa e para; sub-fluxos especiais em prosa do SKILL); informational ausente → skill segue silente." A enumeração mecânica de papéis sai de cada SKILL.md.

### Migração total

Todas as 7 skills do plugin (`/triage`, `/run-plan`, `/new-adr`, `/debug`, `/release`, `/next`, `/heal-backlog`, `/gen-tests-python` — total 8) migram no mesmo batch (B2). Sem fase mista que confunde leitor sobre "qual a convenção atual?".

## Consequências

### Benefícios

- **DRY**: ~40-80 linhas de prosa duplicada removidas; informação concentrada em frontmatter + CLAUDE.md.
- **Verificável por inspeção**: `grep "roles:" skills/*/SKILL.md` valida que todas declaram; mismatch entre frontmatter e prosa restante (sub-fluxos) é detectável.
- **Skill nova explicita o contrato**: criar skill nova exige preencher `roles:` — esquecer é detectável; lista textual em prosa antiga era fácil de pular.
- **Manutenção centralizada**: regra geral (despacho default) muda em 1 lugar (CLAUDE.md); skills só atualizam frontmatter quando o set de papéis muda.

### Trade-offs

- **Frontmatter mais carregado**: cada SKILL.md ganha 3-7 linhas de YAML. Custo trivial; ganho em DRY compensa.
- **Sub-fluxos exigem prosa**: condicionais (`test_command`), criação canonical, stack contradiction não cabem no schema. Aceito — schema cobre o caso normal; YAML não codifica condicionais limpas e tentar aumenta complexidade.
- **Resolution protocol em CLAUDE.md vira mais elaborado**: ganha o parágrafo do despacho automático. Mas CLAUDE.md já é o lugar canônico do protocolo; centraliza o que estava distribuído.

### Limitações

- Schema **não** valida estaticamente que role declarado existe no role contract. Confiança operacional: typo em role detectado em runtime quando a skill tenta resolver path inexistente.
- Não há campo `condicional` no schema. Casos condicionais (`test_command` em `/run-plan`) declaram a categoria mais comum e explicam exceção em prosa. Tentar codificar condicionais cresce schema sem benefício compensador.

## Alternativas consideradas

- **Lista plana** (`roles: [plans_dir, backlog, ...]`): mais simples mas força CLAUDE.md a manter matriz "papel × skill" para distinguir required/informational. Distinção é por-skill (mesma role tem criticidades diferentes em skills diferentes) — pertence ao SKILL, não distribui-la.
- **Manter prosa**: status quo descartado pela revisão arquitetural (40-80 linhas duplicadas; drift potencial em skill nova).
- **Migração gradual / opt-in**: skills migram quando faz sentido; prosa antiga continua válida em fallback. Descartado: cria fase mista que confunde leitor sobre "qual a convenção atual"; mantenedor único + plugin pequeno torna migração total trivial.
- **Schema cobre tudo (incluindo condicionais)**: `roles.required_if_no_e2e: [test_command]` e variantes. Descartado: schema cresce com cada exceção nova; YAGNI sobre necessidade futura. Prosa cobre exceções concretas.
- **Validator automático**: criar script que valida consistência entre frontmatter e protocol. Descartado: plugin não tem build/test infra; YAGNI.
- **Captura uniforme para required ausente**: encaminhar warnings de required ausente sempre para BACKLOG. Descartado após análise: required ausente é bloqueador imediato (operador acabou de invocar a skill que precisa do role); capturar é deferir resolução que precisa acontecer agora; em alguns casos (`/heal-backlog`, `/next`) o role próprio é o BACKLOG (paradoxo).

## Gatilhos de revisão

- Surge skill nova com role condicional em padrão diferente dos atuais → reavaliar se o caso justifica extensão do schema (campo `conditional`?) ou continua em prosa.
- 3+ skills compartilham o mesmo sub-fluxo de criação canonical (hoje só `/triage` e `/new-adr`) → considerar campo declarativo (`roles.create_canonical: [<role>]`) que codifica a oferta de criação.
- Drift detectado entre frontmatter e prosa de sub-fluxo → revisar se schema cobre algo que deveria ficar em prosa, ou vice-versa.
