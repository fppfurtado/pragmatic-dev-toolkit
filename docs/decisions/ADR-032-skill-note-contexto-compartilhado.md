# ADR-032: Skill /note e store de contexto compartilhado em .claude/local/NOTES.md

**Data:** 2026-05-15
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-005](ADR-005-modo-local-gitignored-roles.md) — define modo local-gitignored como padrão para state privado/efêmero, cobrindo 3 roles do path contract (`decisions_dir`/`backlog`/`plans_dir`) com canonical default e modo local opcional. Este ADR é **sucessor parcial** que **estende** ADR-005 para uma nova categoria: store doutrinário fixo non-role em `.claude/local/`, sem canonical (privacidade por design) e sem schema declarável. Segue precedente da entrada `(plugin-internal) | .worktreeinclude` na tabela "The role contract".
- **Investigação:** sessão CC 2026-05-15 — pivote de `/draft-idea` (descartado por ser feature em projeto maduro, regressão tratada pelo ADR-031) para `/triage` direto. Operador relatou pain real cross-project: investigação em `/storage/3. Resources/Projects/tjpa/pje-2.1` que se estendeu para `connector-pje-mandamus-tjpa` (sessão `pje-issue-1920`) — recopia manual entre sessões.
- **Plano:** [docs/plans/skill-note-contexto-compartilhado.md](../plans/skill-note-contexto-compartilhado.md) — materializa a implementação (skill nova `/note`, catálogo, ADR).

## Contexto

<Problema concreto. O que existe hoje, quais restrições, qual ambiguidade ou dor justifica decidir agora.>

## Decisão

<Frase direta do que foi decidido, seguida das razões objetivas em bullets.>

## Consequências

<Impacto da decisão. Texto corrido ou subseções (`### Benefícios`, `### Trade-offs`, `### Limitações`, `### Mitigações`) conforme a natureza.>
