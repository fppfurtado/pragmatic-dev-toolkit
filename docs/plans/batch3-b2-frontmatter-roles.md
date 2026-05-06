# Plano — Batch 3 / B2: frontmatter declarativo `roles:` nas SKILLs

## Contexto

Implementação do ADR-003 ("Frontmatter declarativo `roles:` nas SKILLs"). Cada SKILL.md ganha frontmatter `roles.required` e `roles.informational` declarando os papéis consumidos. CLAUDE.md "Resolution protocol" absorve a regra de despacho automático (required ausente → default herdado; informational ausente → segue silente). Skills removem prosa de "Pré-condições" relativa à enumeração de papéis; mantêm apenas sub-fluxos especiais (criação canonical, condicionais, stack contradiction).

**Linha do backlog:** plugin: batch 3/B2 — frontmatter declarativo `roles:` nas SKILLs (implementa ADR-003), CLAUDE.md absorve regra de despacho automático, skills removem prosa de Pré-condições enumerando papéis

**Sem bifurcação** — schema separado `required`/`informational` + migração total + 3 trilhos de comportamento default registrados em ADR-003.

## Resumo da mudança

Duas operações coordenadas:

- **CLAUDE.md "Resolution protocol"**: adicionar parágrafo declarando o despacho automático com base em `roles.required` / `roles.informational`. Categorização dos 3 trilhos de comportamento default (captura imediata, criação canonical, informa e para) também em CLAUDE.md. Seção "Required vs informational roles" pode encurtar — agora é declarado por skill.

- **8 SKILL.md migram**: cada uma ganha `roles:` no frontmatter (required + informational); seção `## Pré-condições` enxuga removendo a enumeração de papéis (mantém apenas sub-fluxos especiais — criação canonical em `/triage`/`/new-adr`, condicional `test_command` em `/run-plan`, stack contradiction em `/gen-tests-python`).

Mapping confirmado:

| Skill | required | informational |
|---|---|---|
| `/triage` | `plans_dir` | `backlog`, `ubiquitous_language`, `design_notes`, `decisions_dir`, `product_direction` |
| `/run-plan` | `plans_dir` | `backlog`, `test_command` (condicional na prosa) |
| `/new-adr` | `decisions_dir` | — |
| `/debug` | — | `test_command`, `ubiquitous_language`, `decisions_dir`, `design_notes` |
| `/release` | — | `version_files`, `changelog` |
| `/next` | `backlog` | `product_direction` |
| `/heal-backlog` | `backlog` | — |
| `/gen-tests-python` | — | `ubiquitous_language`, `design_notes` |

Sem mudança em outras superfícies — agents, hooks, philosophy.md, README.md, install.md inalterados. Sem CLI/flag/env nova.

## Arquivos a alterar

### Bloco 1 — CLAUDE.md absorve regra de despacho {reviewer: code,doc}

- `CLAUDE.md` seção "Resolution protocol":
  - Adicionar parágrafo de abertura: "Cada skill declara seus papéis em `roles.required` e `roles.informational` no frontmatter. Resolution protocol aplica-se a cada role declarado: required ausente segue um dos 3 trilhos de comportamento default; informational ausente → skill segue silente. Sub-fluxos especiais (criação canonical, condicionais, stack contradiction) ficam em prosa do SKILL."
  - Adicionar lista dos 3 trilhos de comportamento default para required ausente (captura imediata + para; oferecer criação canonical via enum; informa e para — citar ADR-003 como referência completa).

- `CLAUDE.md` seção "Required vs informational roles": **encurtar** — não enumera mais por skill (cada SKILL declara). Manter apenas o princípio: "Required = skill não pode prosseguir; informational = reduz contexto, nunca bloqueia." Citar ADR-003 para os 3 trilhos.

Bloco doc-only do ponto de vista de superfície (CLAUDE.md é prosa de instrução); reviewer `code,doc` para captar drift cruzado entre CLAUDE.md e SKILLs (que vão mudar no Bloco 2).

### Bloco 2 — migrar 8 SKILL.md adicionando `roles:` e enxugando "Pré-condições" {reviewer: code}

Padrão por skill: adicionar `roles:` no frontmatter e remover prosa de "Pré-condições" relativa à enumeração; manter sub-fluxos especiais.

- **`skills/triage/SKILL.md`**:
  - Frontmatter ganha `roles: { required: [plans_dir], informational: [backlog, ubiquitous_language, design_notes, decisions_dir, product_direction] }`.
  - Seção "Pré-condições" remove a enumeração ("Para cada papel necessário... aplicar Resolução de papéis... `plans_dir` 'não temos' → para com gap report").
  - Mantém o parágrafo sobre criação canonical de `ubiquitous_language`/`design_notes`/`backlog` no passo 4 (sub-fluxo especial — criação via enum).

- **`skills/run-plan/SKILL.md`**:
  - Frontmatter ganha `roles: { required: [plans_dir], informational: [backlog, test_command] }`.
  - Seção "Pré-condições" remove a frase "Paths e comandos seguem a Resolução de papéis"; o protocolo agora é despacho automático.
  - Mantém em prosa a precondição 3 condicional do `test_command` (sub-fluxo especial — condicional baseado em conteúdo do plano).
  - Outras precondições (estado git, gate verde, worktree não existe) e seção "Detecção de warnings pré-loop" continuam — não são enumeração de papéis.

- **`skills/new-adr/SKILL.md`**:
  - Frontmatter ganha `roles: { required: [decisions_dir] }` (informational vazio; omitir chave).
  - Seção/passo 1 ("Resolver `decisions_dir`") remove a parte mecânica do protocolo. Mantém o sub-fluxo da oferta de criação canonical (já documentado lá implicitamente).

- **`skills/debug/SKILL.md`**:
  - Frontmatter ganha `roles: { informational: [test_command, ubiquitous_language, decisions_dir, design_notes] }` (required vazio; omitir chave).
  - Seção "Pré-condições" remove a enumeração; o "todos consumed roles são informational" agora é despacho automático do schema.

- **`skills/release/SKILL.md`**:
  - Frontmatter ganha `roles: { informational: [version_files, changelog] }`.
  - Seção "Pré-condições" remove a enumeração; mantém precondições 1 (working tree limpo) e 2 (branch é default — cutucada com enum) — não são enumeração de papéis.

- **`skills/next/SKILL.md`**:
  - Frontmatter ganha `roles: { required: [backlog], informational: [product_direction] }`.
  - Seção "Pré-condições" remove a enumeração; comportamento "sem backlog não há o que analisar → informar e interromper" vira default herdado do trilho "informa e para" (paradoxo de capturar onde role próprio é o BACKLOG — registrado em ADR-003).

- **`skills/heal-backlog/SKILL.md`**:
  - Frontmatter ganha `roles: { required: [backlog] }`.
  - Seção "Pré-condições" remove a enumeração; mesmo trilho que `/next` (informa e para; paradoxo).

- **`skills/gen-tests-python/SKILL.md`**:
  - Frontmatter ganha `roles: { informational: [ubiquitous_language, design_notes] }`.
  - Seção "Pré-condições" / "Stack assumida" mantém a parte sobre `pyproject.toml` (sub-fluxo especial — stack contradiction, não papel).

## Verificação end-to-end

Refactor textual sem suite executável; gate é inspeção dirigida:

1. **Frontmatter declarado em todas as 8 SKILLs**:
   - `grep -l "^roles:" skills/*/SKILL.md` retorna as 8 paths.
   - `awk '/^---$/,/^---$/' skills/<each>/SKILL.md` mostra frontmatter com `roles:` válido.

2. **Mapping correto** (cross-check com tabela do plano):
   - Para cada skill, conferir que `roles.required` e `roles.informational` batem com a tabela.
   - Esp. importantes: `/triage` required `plans_dir`; `/run-plan` required `plans_dir`; `/new-adr` required `decisions_dir`; `/next` required `backlog`; `/heal-backlog` required `backlog`. Required ausente em `/debug`, `/release`, `/gen-tests-python`.

3. **Prosa de "Pré-condições" enxugada nas 8 SKILLs**:
   - Enumeração mecânica do tipo "Para cada papel necessário aplicar Resolução de papéis... probe canonical → CLAUDE.md → pergunta tri-state" **não aparece mais** em nenhum SKILL.md.
   - Sub-fluxos especiais preservados onde aplicável (criação canonical em `/triage`/`/new-adr`; condicional `test_command` em `/run-plan`; stack contradiction em `/gen-tests-python`).

4. **CLAUDE.md atualizado**:
   - "Resolution protocol" tem parágrafo novo declarando despacho automático.
   - Lista dos 3 trilhos de comportamento default presente.
   - "Required vs informational roles" encurtado — não enumera por skill.
   - Citações ao ADR-003 onde aplicável.

5. **Cross-cutting (refs externas)**:
   - `grep -rn "Resolução de papéis\|Pré-condições.*papéis\|protocolo de resolução" --include="*.md" .` para conferir que refs em outros arquivos (philosophy.md, install.md, README) continuam coerentes.
   - Planos antigos em `docs/plans/*.md` não tocados — referenciam comportamento antigo, válido como histórico per convenção do CHANGELOG v1.14.0.

6. **Critério editorial preservado**:
   - SKILLs continuam tendo `## O que NÃO fazer` quando aplicável (nenhuma skill perde scope guard; só prosa de "Pré-condições" enxuga).

## Verificação manual

**Smoke test em uso real** (pós-merge+reload do plugin):

- **Cenário 1 — required ausente em skill com creação canonical**: invocar `/new-adr "<título qualquer>"` num diretório fictício sem `docs/decisions/`. Confirmar: skill propõe criação via enum (sub-fluxo especial preservado).
- **Cenário 2 — informational ausente**: invocar `/debug "<sintoma qualquer>"` num repo sem `docs/domain.md`. Confirmar: skill segue silente, lista hipóteses sem invariantes documentadas, sem mensagens de gap.
- **Cenário 3 — required ausente em skill sem criação canonical**: invocar `/heal-backlog` num repo sem `BACKLOG.md`. Confirmar: skill informa "sem backlog não há o que curar" e para (sub-fluxo "informa e para").

**Critério de aceitação**: os 3 cenários se comportam conforme ADR-003 — required ausente herda trilho correto; informational ausente segue silente.

## Notas operacionais

- Após merge, B2 fecha o roteiro arquitetural pós-v1.20.0. Resta acumular merges para `/release` em algum ponto futuro (cadência registrada em CLAUDE.md).
- Skills futuras seguem o padrão: declaram `roles:` no frontmatter; herdam comportamento default; prosa cobre só sub-fluxos especiais.

## Pendências de validação

- Smoke test em uso real (3 cenários: required ausente com creação canonical em `/new-adr`; informational ausente em `/debug`; required ausente sem criação canonical em `/heal-backlog`): exige merge + reload do plugin (cache instalado pré-B2 ainda não tem o frontmatter `roles:`). Validação direta pós-merge via inspeção dos frontmatters em `${CLAUDE_PLUGIN_ROOT}/skills/*/SKILL.md` cobre o core do contrato; comportamental real fica para invocação subsequente das skills.
