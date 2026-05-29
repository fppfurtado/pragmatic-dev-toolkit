# Plano — Onda 2 da reforma doutrinária: reframing batch de 4 ADRs com adendos cross-ref aos fundamentais

## Contexto

Onda 2 da reforma doutrinária codificada em `BACKLOG.md ## Próximos` (commit `bebc34d`). Onda 1 shippou ADR-043 (commit `076354f`) substituindo ADR-035 e codificando a hierarquia invertida: 3 princípios fundamentais (Verdade, Excelência sem over-engineering, Navalha de Ockham) como raiz epistêmica; YAGNI/flat/sem-defensividade-ornamental como consequência operacional derivada.

Esta onda reframa 4 ADRs históricos que operavam implicitamente sob YAGNI-as-apex pré-inversão, com adendos curtos cross-ref aos fundamentais e a ADR-043. Decisões centrais permanecem intactas — apenas o vocabulário "YAGNI-as-veto" recebe grounding explícito nos princípios fundamentais que já o sustentavam implicitamente.

Padrão editorial per [ADR-034](../decisions/ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) § Localização do adendo: seção `## Addendum (2026-05-29)` ao final de cada ADR. Forma preferida quando o adendo é cross-ref para sucessor parcial sem amarração sintática a seção específica do body. As 4 condições para adendo aplicam: (1) decisão central intacta, (2) sem categoria nova, (3) sem restrição externa nova, (4) caráter explicativo.

Body text dos ADRs alvos **não é alterado** — vocabulário YAGNI permanece como referência histórica do raciocínio original; adendo ao final reconhece o grounding modernizado.

**ADRs candidatos:** ADR-043 (raiz doutrinária; sucessor de ADR-035), ADR-034 (critério adendo vs ADR), ADR-014/-016/-032/-036 (alvos do reframing).

Campo `**Linha do backlog:**` intencionalmente omitido deste plano — umbrella line em `BACKLOG.md ## Próximos` (commit `bebc34d`) cobre 4 ondas; matching prematuro pelo `/run-plan §3.4` moveria a umbrella para `## Concluídos` antes das 3 ondas restantes. Justificativa detalhada em § Notas operacionais.

## Resumo da mudança

Para cada um dos 4 ADRs alvo, adicionar `## Addendum (2026-05-29)` ao final (após `## Gatilhos de revisão` quando existir; antes do EOF). Cada adendo:

- Cross-ref a [ADR-043](../decisions/ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) reconhecendo a inversão de hierarquia doutrinal.
- Identifica qual(is) fundamental(is) endossa(m) a decisão original.
- Explica como o vocabulário YAGNI do body era proxy operacional do princípio raiz (Ockham na maioria dos casos).
- Confirma que a decisão central permanece intacta sob a nova hierarquia.

Adendos curtos (1-2 parágrafos cada). Cross-refs internos a ADR-035 nos bodies permanecem — ADR-035 está marcado `Substituído por ADR-043` e leitor é redirecionado via header de status.

## Arquivos a alterar

### Bloco 1 — ADR-014 reframing {reviewer: doc}

- `docs/decisions/ADR-014-inventario-editorial-main-unico.md`: append `## Addendum (2026-05-29)` reconhecendo que a decisão "manter `main` único; refatoração estrutural descartada" é endossada por **Ockham** (não multiplicar entidades: 2 repos / branch dev / pipeline orphan sem dor empiricamente reportada) + **Verdade** (gatilho "atrito real reportado por consumer" é verificação empírica, não inferência). O framing "descartada por YAGNI" no título e § Decisão era proxy operacional do princípio Ockham — Ockham operacionalizado nesta decisão via critério 1 de ADR-043 (incidente/padrão observado em uso real, não hipótese). Cross-ref a ADR-043.

### Bloco 2 — ADR-016 reframing {reviewer: doc}

- `docs/decisions/ADR-016-manter-block-gitignored-scripts-no-consumer.md`: append `## Addendum (2026-05-29)` reconhecendo que a decisão "manter o hook como está; pattern do consumer é responsabilidade do consumer" é endossada por **Ockham** (não inflar mecanismo do plugin para acomodar pattern do consumer — preserva hook simples, sem flags/config/parser) + **Excelência** (qualidade dentro do escopo: hook faz uma coisa bem). O framing "refatorar mais tarde no consumer é mais barato do que abstrair cedo no plugin" (citado em § Razões a partir de philosophy.md pré-inversão) é Ockham operacionalizado via critério 2 de ADR-043 (fronteira nítida entre plugin doctrine e responsabilidade do consumer). Cross-ref a ADR-043.

### Bloco 3 — ADR-032 reframing {reviewer: doc}

- `docs/decisions/ADR-032-skill-note-contexto-compartilhado.md`: append `## Addendum (2026-05-29)` reconhecendo que a decisão "skill pura de gravação; YAGNI deliberado sobre leitura, busca, sincronização" é endossada por **Ockham operacionalizado em decisões internas do plugin** (não multiplicar features especulativas da skill — captura é a entidade necessária; leitura/busca/sync seriam entidades adicionais sem dor real) + **Verdade** (§ Limitações declara "Reabertura legítima se atrito real surgir" — gatilho empírico, não pré-cog). O framing "YAGNI deliberado" no § Limitações é Ockham operacionalizado via critério 1 de ADR-043. Cross-ref a ADR-043.

### Bloco 4 — ADR-036 reframing {reviewer: doc}

- `docs/decisions/ADR-036-brainstorm-intencionalmente-nao-codificado-em-skill.md`: append `## Addendum (2026-05-29)` reconhecendo que a decisão "brainstorm intencionalmente não-codificado como skill" é endossada por **Ockham operacionalizado em decisões internas do plugin** (não codificar wide quando narrow + raw-chat já entrega; estrutura interna nova não paga seu custo de manutenção pela clareza/coerência adicionada). § Origem cita "**Decisão base:** ADR-035" — esse cross-ref permanece válido factualmente (ADR-036 foi decidido antes de ADR-043), mas o critério "paga seu custo de manutenção pela clareza/coerência?" referenciado no body agora vive em [ADR-043](../decisions/ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § "Ockham operacionalizado em decisões internas do plugin"; ADR-035 está marcado Substituído. § Razões "Evidência empírica do gap é fraca" é operacionalização concreta do critério 1 de ADR-043 (incidente recorrente ausente). **Adendo inclui instrução explícita sobre preservação de numeração:** "Os critérios 1 e 4 referenciados em § Origem e nos bullets de § Gatilhos de revisão (`per ADR-035 critério 1/4`) preservam numeração idêntica em ADR-043 § Ockham operacionalizado em decisões internas do plugin — critério 1 = incidente recorrente ou padrão observado; critério 4 = codificação de pattern emergente ≥3x ad hoc. Leitor que segue thread de gatilhos não precisa adivinhar equivalência." Cross-ref a ADR-043.

## Verificação end-to-end

- Cada um dos 4 ADRs (014, 016, 032, 036) tem nova seção `## Addendum (2026-05-29)` ao final do arquivo (antes do EOF; após `## Gatilhos de revisão` quando existir).
- Comando: `for f in docs/decisions/ADR-{014,016,032,036}-*.md; do grep -c "^## Addendum (2026-05-29)" "$f"; done` retorna `1` para cada arquivo.
- Cada adendo contém referência explícita a `ADR-043` (`grep -l "ADR-043" docs/decisions/ADR-{014,016,032,036}-*.md` retorna os 4 arquivos).
- Cada adendo identifica ≥1 fundamental por nome (Verdade, Excelência, ou Ockham): `for f in docs/decisions/ADR-{014,016,032,036}-*.md; do grep -A 30 "^## Addendum (2026-05-29)" "$f" | grep -E "Verdade|Excelência|Ockham" -c; done` retorna `≥1` para cada arquivo.
- Nenhuma decisão central foi alterada — diff outside of new `## Addendum` section deve ser vazio. Verificação editorial via inspeção visual: `git diff origin/main..HEAD -- docs/decisions/ADR-014-*.md` (e análogos para 016, 032, 036) deve mostrar apenas linhas adicionadas dentro da nova seção `## Addendum (2026-05-29)`; nenhuma linha removida; nenhuma adição fora do adendo. 4 arquivos pequenos, alvo doc-only humanamente verificável — gate mecânico via grep/sed seria overkill para caminho doc-only.
- Body cross-refs a ADR-035 nos 4 ADRs preservados (não removidos) — `grep -l "ADR-035" docs/decisions/ADR-{014,016,032,036}-*.md` retorna os 4 arquivos onde aplicável; ADR-035 está marcado `Substituído por ADR-043` em seu header (commit `076354f`), redirecionando leitor naturalmente.

## Verificação manual

Não aplicável — caminho doc-only sem comportamento perceptível, fluxo crítico ou integração frágil. Verificação end-to-end cobre via greps.

## Notas operacionais

- **Umbrella line da reforma:** linha em `BACKLOG.md ## Próximos` (commit `bebc34d`) cobre todas as 4 ondas. `**Linha do backlog:**` omitido deste plano para não disparar matching do `/run-plan §3.4` que moveria a umbrella para `## Concluídos` prematuramente (3 ondas ainda pendentes após esta). Operador atualiza a linha umbrella manualmente após Onda 4 finalizada — ou edita progressivamente para refletir status das ondas.

- **Ordem dos blocos:** independentes editorialmente. `/run-plan` pode executar sequencialmente; nenhum bloco depende de outro. Reviewer `doc-reviewer` por bloco audita drift de cross-refs e idioma editorial.

- **Cross-refs a ADR-035 nos bodies:** mantidos como histórico. ADR-035 está `Substituído por ADR-043` em seu header desde o commit `076354f`; leitor que clica chega no header e é redirecionado. Não há ganho em sweeping replace dos cross-refs body-level — Onda 2 é adendo, não rewrite.

- **Onda 3 (consolidação editorial de clusters densos)** é a próxima — modo local (ADR-005/-018/-025/-030) e cutucadas (ADR-017/-029). Esta Onda 2 não toca esses clusters; mantém escopo restrito aos 4 ADRs candidatos.

## Decisões absorvidas

- § Verificação end-to-end (último bullet): substituído comando shell quebrado (sintaxe regex inválida + lógica de filtro inversa) por instrução de inspeção visual via `git diff` — 4 arquivos pequenos doc-only humanamente verificáveis; gate mecânico seria overkill para caminho doc-only (caminho-único).
