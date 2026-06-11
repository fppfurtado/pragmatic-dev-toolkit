# ADR-059: Subagent em loop interno de skill (per-item probe + threshold)

**Data:** 2026-06-11
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-009](ADR-009-revisor-design-pre-fato.md) (sucessor parcial — refina critério "volume vs cold-start de subagent" introduzindo eixo de shape: `scan único` vs `per-item probe`).
- **Investigação:** materialização empírica do gatilho de YAGNI registrado na linha do BACKLOG ("paralelizar verificação 'já implementado?' em `/next`") — consumers reais (`tjpa/pje-2.1` com 100+ issues em modo `forge`; `meta-system` com volume análogo) operam com `N ≥ 20` candidatos por invocação de `/next`. Custo serial cresce linearmente; trigger YAGNI atingido.

## Contexto

`/next` passo 3 ("Verificar implementação no código") itera **serialmente** sobre os candidatos lidos no passo 2, procurando evidência (grep/glob) no codebase do consumer. Per `12b3185`, `N` é parametrizado por CLI arg posicional (default 10).

[ADR-009](ADR-009-revisor-design-pre-fato.md) e seu sucessor arquivado ADR-011 **rejeitaram subagent** para wiring do `design-reviewer`, citando "subagent frio + briefing duplicado anula economia de contexto para volume pequeno (~10 docs)" e "cold start, paralelização opcional, custo de orquestração sem ganho proporcional para o volume atual". O argumento se centra em **volume × overhead**.

Gatilho de revisão de ADR-009 ("wiring automático em `/run-plan` pré-loop ou `/new-adr` pré-commit materializa → reabrir trade-off de tokens e considerar Task delegation") **não** é o que ADR-059 aciona — aquele gatilho mira reviewer document-level com free-read autônomo (alta frequência em reviewer já existente); este ADR mira skill genérica com per-item probe independente. Eixos distintos.

Refinamento doutrinal devido: a rejeição se aplica à shape **`scan único`** do reviewer (1 invocação processa todo um doc-set; paralelizar não escala porque o doc-set é único). Não se aplica à shape **`per-item probe`** do passo 3 do `/next` (`N` invocações independentes; paralelismo cresce com `N`, latência total ≈ max(individual)). São aritméticas de trade-off distintas; misturá-las gera doutrina genérica demais.

## Decisão

**Aceitar subagent em loop interno de skill quando a shape é `per-item probe` independente E o volume satisfaz threshold `N ≥ 5`.**

Razões objetivas:

- **Shape `per-item probe`** é o eixo discriminante. Cada candidato é independente; paralelizar maximiza redução de latência total. Distinto de `scan único` (1 doc-set, paralelismo não escala).
- **Threshold `N ≥ 5`** preserva caminho serial em backlogs pequenos onde cold-start de subagent perde para grep direto. Threshold ancora em **metade do default invariante de `/next` (10)** — heurística de safety margin contra cold-start dominante em backlog menor que default; sem medida empírica. Gatilhos de revisão registrados em § Gatilhos de revisão.
- **Granularidade `1 subagent por candidato`** (vs bucketing) maximiza paralelismo. Cold-start replicado mas amortizado pela latência max(individual).
- **Subagent type `Explore`** (read-only, codebase-focused) — recomendado per system prompt para "lookup/grep" focado, baixo cold-start vs general-purpose.

## Consequências

### Benefícios

- Latência total do passo 3 do `/next` cai de `Σ(serial_i)` para `≈ max(serial_i)` quando `N ≥ 5`. Em consumers com `N = 20` e codebase grande, ganho material.
- Doutrina explícita sobre quando subagent vale a pena em skill — referência para skills futuras que apresentem shape `per-item probe`.

### Trade-offs

- **Cold-start replicado `N` vezes** em vez de uma. Aceito porque o ganho de paralelismo amortiza; tradeoff inverte só quando `N < 5` (caminho serial preservado).
- **Briefing duplicado** por subagent — o subagent é frio (não tem contexto da conversa). Prompt curto auto-contido por candidato; texto de briefing é overhead constante por candidato. Aceitável porque conteúdo é estável (gerado por template no SKILL).
- **Quebra de simetria com `design-reviewer`** — design-reviewer mantém `@-mention` inline (ADR-009). Não é inconsistência: shape diferente, doutrina diferente.

### Limitações

- Aplica-se a `/next` passo 3 em v1. Aplicação retroativa a outras skills depende de cada uma exibir shape `per-item probe` independente.
- Threshold `5` é chute editorial. Não há evidência empírica de que `5` seja o ponto ótimo; é gatilho de revisão registrado.

### Mitigações

- Falha de subagent durante invocação: skill assume `sem evidência` para esse candidato + warning, não bloqueia outros. Caminho graceful.
- Em modo `forge`, paralelismo do passo 3 não muda mecânica das cutucadas remotas do passo 6 (uma cutucada por issue, sequencial — ADR-058 § (e) preservado).

## Alternativas consideradas

### Bucketing fixo (ex.: 5 candidatos/subagent)

Descartado: menos paralelismo dentro do bucket (latência `ceil(N/K) × latencia_bucket` vs `max(individual)`); briefing maior; adiciona parâmetro `bucket_size`. Ganho de cold-start não compensa perda de paralelismo na faixa `N = 5..20` típica.

### Sempre paralelizar (mesmo `N = 1`)

Descartado: paga cold-start em sessões focadas (`/next 3`) sem benefício mensurável. Simplifica branching mas inverte custo no caminho-comum (backlog pequeno).

### Hybrid: 1 por candidato com cap (ex.: max 10 paralelos)

Descartado: complica orquestração (Claude Code não expõe API de fila nativa para Agent calls); premature para faixa de uso atual (`N` raramente > 30). Reabrir se evidência de explosão de tokens em `N = 100+` materializar.

### Cap mecânico em `N` sem paralelizar

Limitar `/next [N]` a `N ≤ 5` via clamp no SKILL ou obrigar operador a particionar manualmente em sub-invocações. Custo de implementação ínfimo (1 linha de validação no passo 2); preserva caminho serial atual sem introduzir mecanismo plugin-side.

Descartado: consumers reais (tjpa/pje-2.1 com 100+ issues, meta-system) querem visibilidade da totalidade dos candidatos por invocação para ranking estratégico do top 3 — cap arbitrário em 5 cega o operador para `## Próximos` de cauda longa. Particionamento manual transfere cerimônia (operador escolhe ranges, integra resultados, perde contexto cross-invocation). Subagent paralelo preserva contrato "1 invocação = 1 top 3 do backlog inteiro" sem cerimônia.

## Gatilhos de revisão

- **Threshold elevar:** sessão `/next` regular com cold-start dominando latência em `N = 5` (paralelo mais lento que serial neste tamanho).
- **Threshold reduzir:** medir em `N=3` com Explore (cold-start do subagent vs grep direto do main thread); se latência paralela < latência serial, reduzir o threshold.
- **Hybrid cap:** Claude Code expor API de fila com cap configurável → reconsiderar hybrid para `N = 100+`.
- **Aplicação retroativa:** segunda skill no plugin apresentando shape `per-item probe` independente — registrar em § Implementação abaixo.

## Implementação

- `12b3185` parametrizar N via CLI arg posicional `/next [N]` (default 10) — pré-condição mecânica que viabiliza este ADR.
- Pendente: refactor de `skills/next/SKILL.md` passo 3 conforme plano `docs/plans/paralelizar-next-via-explore-subagent.md`.
