# ADR-031: Cutucada condicional em /draft-idea para projeto maduro

**Data:** 2026-05-15
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-027](ADR-027-skill-draft-idea-elicitacao-product-direction.md) — define o sub-fluxo de presença da skill `/draft-idea` (`ausente → one-shot full; presente → update seção-a-seção`). Este ADR é **sucessor parcial**, refinando o caso `ausente` para distinguir projeto novo (cristalização inicial legítima) de projeto maduro (onde `IDEA.md` ausente pode mascarar uso indevido para feature).
- **Investigação:** sessão CC de 2026-05-15 rodou `/draft-idea` no toolkit (versão 2.8.1) com argumento descrevendo feature ("ferramenta de chaveamento de contexto entre sessões"); a skill gravou `IDEA.md` monograficamente sobre a feature, regredindo a discoverability do papel `product_direction` definido em CLAUDE.md como direção-do-projeto-inteiro.
- **Plano:** [docs/plans/draft-idea-cutucada-projeto-maduro.md](../plans/draft-idea-cutucada-projeto-maduro.md) — materializa a implementação (passo 1.5 da skill + refinamento do papel no CLAUDE.md).

## Contexto

<Problema concreto. O que existe hoje, quais restrições, qual ambiguidade ou dor justifica decidir agora.>

## Decisão

<Frase direta do que foi decidido, seguida das razões objetivas em bullets.>

## Consequências

<Impacto da decisão. Texto corrido ou subseções (`### Benefícios`, `### Trade-offs`, `### Limitações`, `### Mitigações`) conforme a natureza.>
