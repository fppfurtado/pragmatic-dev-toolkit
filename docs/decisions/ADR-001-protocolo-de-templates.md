# ADR-001: Protocolo de templates centralizados no plugin

**Data:** 2026-05-06
**Status:** Aceito

## Origem

- **Investigação:** Revisão arquitetural pós-v1.20.0 identificou que a estrutura canônica do plano (`## Contexto` → `## Resumo da mudança` → `## Arquivos a alterar` → ...) é prosa inline em `skills/triage/SKILL.md` passo 4 e referenciada por `skills/run-plan/SKILL.md` precondição 1 — duplicação que diverge silenciosamente. Nenhuma das duas skills consegue ser fonte sozinha porque ambas precisam saber a estrutura.

## Contexto

Skills do plugin produzem e consomem artefatos com estrutura compartilhada. Hoje:

- **Plano** (`docs/plans/<slug>.md`): estrutura descrita em prosa em `/triage` step 4; `/run-plan` precondição 1 faz matching semântico contra os mesmos headers. Drift potencial: editar a estrutura em uma skill sem espelhar na outra.
- **ADR**: template inline em `/new-adr` SKILL.md (linhas ~46-69). Single source — sem drift no momento.
- **`docs/domain.md` / `docs/design.md`**: sem template formal — texto livre, edit cirúrgico.
- **Linha de backlog**: estrutura mínima (frase de intenção); não justifica template.

Conforme o plugin evolui, mais artefatos com estrutura compartilhada vão emergir. Sem protocolo para onde a estrutura mora, cada skill nova reinventa ou re-duplica.

## Decisão

**Estabelecer pasta `templates/` na raiz do plugin como single source of truth para esqueletos canônicos de artefatos consumidos por múltiplas skills.** Skills leem o template em runtime via `${CLAUDE_PLUGIN_ROOT}/templates/<artifact>.md` quando precisam compor ou validar o artefato.

Razões objetivas:

- **DRY operacional**: editar a estrutura em um lugar; skills consumidoras refletem automaticamente.
- **Skills enxutas**: prosa de estrutura sai dos SKILL.md; cada skill descreve seu papel sobre o template, não duplica o template.
- **Padrão extensível**: futuros artefatos com estrutura compartilhada (templates de check, de release notes, etc.) seguem o mesmo protocolo sem precisar de nova decisão.

**Mecânica de leitura**: Read em runtime, não embed/copy. Embed reintroduz duplicação.

**Escopo inicial (este ADR)**: apenas `templates/plan.md`. ADR template fica inline em `/new-adr` por ora — single consumer, sem ganho imediato em extrair. `docs/domain.md` / `docs/design.md` continuam livres. A pasta `templates/` é estabelecida com 1 arquivo; expansão futura é extensão deste protocolo, não nova decisão.

## Consequências

### Benefícios

- `skills/triage/SKILL.md` passo 4 passa a apontar para `templates/plan.md` em vez de descrever a estrutura inline — passo encurta.
- `skills/run-plan/SKILL.md` precondição 1 (matching semântico) continua funcional — já agnóstica ao corpo do template; só aceita os mesmos headers vindo do template.
- Drift entre `/triage` e `/run-plan` sobre a estrutura do plano fica eliminado.
- Operador externo abrindo o plugin tem `templates/plan.md` como referência canônica de "como um plano se parece" — facilita autoria manual de planos.

### Trade-offs

- Skills passam a depender de Read runtime no path `${CLAUDE_PLUGIN_ROOT}/templates/plan.md`. Se o file não existir (cache corrompido, instalação parcial), `/triage` falha ao compor plano.
- Idioma do template é PT-BR canonical (origem do toolkit). Skills adaptam headers ao idioma do projeto consumidor (per `docs/philosophy.md` → "Convenção de idioma") — adaptação na skill, não no template. Template é mecânica do toolkit; idioma fica canonical.

### Limitações

- ADR template não migra agora (escopo limitado). Decisão futura, sob este mesmo protocolo, pode estender.

## Alternativas consideradas

- **Embed/copy em vez de Read runtime**: cada skill carregaria o template literal no SKILL.md. Reintroduz duplicação que o ADR resolve — descartado.
- **Escopo amplo (`templates/plan.md` + `templates/adr.md`)**: refactor maior dobrando escopo do batch. YAGNI por ora — não há pain reportado em manter ADR template inline. Decisão futura, sob este protocolo, pode adicionar `templates/adr.md` quando justificar.
- **Manter prosa inline e instituir critério editorial**: tentou-se algo análogo no Batch 1 (critério editorial em CLAUDE.md para `## O que NÃO fazer`). Funciona quando a duplicação é dentro de um arquivo ou parecida; não funciona para estrutura compartilhada entre skills que precisam ambas conhecer a forma exata.

## Gatilhos de revisão

- Pain reportado em manter ADR template inline em `/new-adr` (drift detectado, edit fraturado, ou nova skill que precisa do mesmo template) → reabrir para estender o protocolo a `templates/adr.md`.
- Plugin ganha 3+ artefatos com estrutura compartilhada além de plano → reabrir para considerar formato de manifesto (ex.: `templates/index.json` listando artefatos disponíveis) em vez de scan ad-hoc.

## Addendum (2026-05-12)

Esta nota é adendo informativo posterior à aceitação; não altera a decisão original. [ADR-024](ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md) estabelece categoria paralela `docs/procedures/` para procedimentos operacionais compartilhados; complementa este ADR sem revogá-lo. Fronteira: `templates/` = esqueletos preenchidos quando o artefato é produzido; `docs/procedures/` = procedimentos executados quando referenciados.
