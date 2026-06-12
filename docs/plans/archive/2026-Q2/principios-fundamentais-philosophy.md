# Plano — Princípios fundamentais em philosophy.md

## Contexto

Adicionar seção dedicada `## Princípios fundamentais` no topo de `docs/philosophy.md` (antes de `## A filosofia em uma frase`) imprimindo as **raízes epistêmicas** da filosofia pragmática já declarada no plugin. Substância dos 3 princípios:

- **Busca pela verdade** — o que existe, existe; verificar antes de assumir, medir antes de generalizar; falsificável > hand-waving.
- **Excelência sem over-engineering** — qualidade serve o problema concreto, não vice-versa; YAGNI bounds escopo, excelência drives qualidade dentro do escopo.
- **Navalha de Ockham** — não multiplicar entidades; operacionaliza YAGNI no dimensional: não só "não implementar o que não usa" mas "não modelar o que não distingue".

**Triangulação**: verdade descobre o que é; excelência engaja seriamente com o descoberto; Ockham previne que o engajamento invente o que não estava ali. Verdade sem excelência fica passiva; excelência sem Ockham vira over-engineering; Ockham sem verdade vira reducionismo cego.

**Mapping para a doutrina atual**: YAGNI/flat ↔ Ockham; "sem defensividade desnecessária" ↔ Verdade (validar onde há risco real, não onde imaginamos); "pragmática" (sem aspiracional schema-perfeição) ↔ Excelência sem over-engineering.

**Framing constraint (load-bearing)**: `philosophy.md` é doc público para consumers terceiros — texto precisa ser **descritivo do artefato** ("princípios que guiaram o design deste toolkit e que suas regras pragmáticas materializam"), **não** prescritivo ("siga estes princípios") **nem** personalista ("o autor acredita em X"). Toolkit não tem autoridade para prescrever ao usuário; framing pessoal está fora de escopo para plugin público.

**Cross-ref externo (não-canonical)**: meta-system commit `ac0811d` (`docs(arch): princípios fundamentais ...`) imprimiu os 3 em `ARCHITECTURE.md § Princípios → Fundamentais`, lá como **stance pessoal do autor**. Toolkit pode citar via footnote descritivo opcional, sem dependência canonical — evita drift cross-repo.

**ADRs candidatos:** ADR-035 (escopo de aplicação de YAGNI — o mapping "YAGNI/flat ↔ Ockham" é o link doutrinário mais direto), ADR-037 (código como fonte de verdade — ressoa com "Busca pela verdade" no eixo do que conta como evidência), ADR-012 (idioma de artefatos discoverability/landing — não-bloqueante mas philosophy.md é PT-BR canonical).

**Filtro ADR-035 (decisão interna)**: custo de manutenção baixo (doc-only, ~30 linhas adicionadas, sem mecanismo novo); clareza ganha: explicita raízes epistêmicas do flat-pragmatic hoje implícitas em "YAGNI por padrão" / "sem defensividade desnecessária" no opener atual. Filtro **passa** — refinamento doutrinal (critério 3 do ADR-035) com tradução pública das raízes meta-teóricas.

**Linha do backlog:** plugin: imprimir 3 princípios fundamentais (Verdade, Excelência, Ockham) em `docs/philosophy.md` como raízes epistêmicas da filosofia pragmática já declarada (YAGNI/flat/sem-abstrações/sem-defensividade ornamental) — proposta surgida em sessão CC no consumer `meta-system` em 2026-05-28. Substância dos 3: **Busca pela verdade** (o que existe, existe — verificar antes de assumir, medir antes de generalizar, falsificável > hand-waving); **Excelência sem over-engineering** (qualidade serve o problema concreto, não vice-versa; YAGNI bounds escopo, excelência drives qualidade dentro do escopo); **Navalha de Ockham** (não multiplicar entidades — operacionaliza YAGNI no dimensional: não só "não implementar o que não usa" mas "não modelar o que não distingue"). **Triangulação**: verdade descobre o que é; excelência engaja seriamente com o descoberto; Ockham previne que o engajamento invente o que não estava ali — verdade sem excelência fica passiva, excelência sem Ockham vira over-engineering, Ockham sem verdade vira reducionismo cego. **Mapping para a doutrina atual**: YAGNI/flat ↔ Ockham; "sem defensividade desnecessária" ↔ Verdade (validar onde há risco real, não onde imaginamos); "pragmática" (sem aspiracional schema-perfeição) ↔ Excelência sem over-engineering. **Framing constraint (load-bearing)**: `philosophy.md` é doc público pra consumers terceiros — texto precisa ser **descritivo do artefato** ("princípios que guiaram o design deste toolkit e que suas regras pragmáticas materializam"), **não** prescritivo ("siga estes princípios") **nem** personalista ("o autor acredita em X"). Toolkit não tem autoridade pra prescrever ao usuário; framing pessoal está fora de escopo pra plugin público. **Cross-ref**: meta-system commit `ac0811d` (`docs(arch): princípios fundamentais ...`) imprimiu os 3 em ARCHITECTURE.md § Princípios → Fundamentais, lá como stance pessoal do autor; toolkit pode citar via footnote descritivo opcional, sem dependência canonical (evita drift cross-repo). **Decisão preliminar de posicionamento** (`/triage` pode questionar): seção dedicada `## Princípios fundamentais` no topo de philosophy.md, antes de `## A filosofia em uma frase`, porque informa a leitura do resto. Substância pode ser similar ou condensada vs versão em meta-system; reescrita pra audiência pública é parte do trabalho. **Direção (esperada do /triage)**: ADR não-necessário (refinamento editorial puro de philosophy.md, sem mudança de mecanismo das skills); plano de bloco único (Bloco 1: edit em docs/philosophy.md). Custo: 1 commit, doc-only. **Pontos esperados de cutucada do design-reviewer**: (a) seção dedicada vs absorvido no opener "A filosofia em uma frase"; (b) ordem dos 3 (epistêmico → axiológico → parsimônia vs outra); (c) se cita meta-system explicitamente ou não; (d) se a triangulação fica como prosa ou como diagrama mínimo. **Trade-off conhecido**: duplicação de substância (meta-system pessoal + toolkit design philosophy). Aceito porque audiências e framings são distintos; drift mitigado por revisões síncronas se algum dia revisar um lado.

## Resumo da mudança

Nova seção `## Princípios fundamentais` inserida no topo de `docs/philosophy.md` (antes de `## A filosofia em uma frase`), substância adaptada para framing descritivo do artefato (não prescritivo, não personalista). Ordem das subseções: Verdade → Excelência → Ockham (epistêmico → axiológico → parsimônia). Triangulação inicialmente em prosa (decisão final pode mudar via cutucada do design-reviewer).

**Decisões fechadas no plano** (4 cutucadas pré-anticipadas pelo backlog + 1 ADR-worthy emergente):

- **(a) Seção dedicada no topo**, antes de "A filosofia em uma frase" — operador escolheu over reviewer-recommended-depois-do-opener; rationale: 3 princípios informam a leitura do resto.
- **(b) Ordem dos 3**: Verdade → Excelência → Ockham — operador escolheu epistêmico → axiológico → parsimônia (tradição filosófica) over reviewer-recommended Ockham-first (espelha opener).
- **(c) Sem footnote a meta-system commit `ac0811d`** — default conservador confirmado pelo reviewer (dependência cross-repo opaca em doc público).
- **(d) Triangulação em prosa**, não diagrama — default conservador confirmado pelo reviewer (frase mais precisa que setas).
- **(e) ADR sobre partição editorial dual-audience** — adiada via linha em BACKLOG.md ## Próximos per ADR-035 critério 4 (aguarda 2º pattern emergente); operador escolheu defer over criar-agora.

**Fora de escopo:** mudança de mecanismo em skills/agents (princípios são leitura, não regra executável); reescrita da seção "A filosofia em uma frase" (segue intacta como hoje); migração de outras menções a "verdade"/"YAGNI"/"flat" no resto do philosophy.md (refinamento futuro se necessário).

## Arquivos a alterar

### Bloco 1 — Nova seção `## Princípios fundamentais` em philosophy.md {reviewer: doc}

- `docs/philosophy.md`:
  - Inserir nova seção `## Princípios fundamentais` entre linha 3 (parágrafo introdutório atual) e linha 5 (`## A filosofia em uma frase`).
  - Parágrafo de abertura curto (1 frase) framing descritivo: "Três princípios epistêmicos guiaram o design deste toolkit e suas regras pragmáticas materializam." (ou equivalente — descritivo, não prescritivo, não personalista).
  - **Footnote de framing logo após a frase de abertura**: "Esta seção descreve o que o toolkit assume; não é prescrição ao leitor." Inocula o leitor consumer-third-party contra leitura prescritiva.
  - Três sub-seções H3 na ordem: **Busca pela verdade**, **Excelência sem over-engineering**, **Navalha de Ockham** — substância adaptada do backlog (1-3 frases por princípio).
  - **Padrão de frase (gabarito mecânico anti-prescritivo)**: cada subseção começa com "O toolkit assume que..." ou "Este princípio orientou o design quando..." — **não** "Você deve...", "Acreditamos que...", "Na nossa visão...". Aplica-se também à triangulação e mapping abaixo.
  - Parágrafo `**Triangulação**:` em prosa após os 3 princípios (decisão (d) fechada — diagrama descartado per design-reviewer finding 5).
  - Parágrafo `**Mapping para a doutrina atual**:` ligando YAGNI/flat ↔ Ockham; "sem defensividade desnecessária" ↔ Verdade; "pragmática" ↔ Excelência. Inclui cross-ref a ADR-035 onde menciona YAGNI/Ockham (já existente no philosophy.md linha 9).
  - **Não citar** o commit `ac0811d` do meta-system (decisão (c) fechada per design-reviewer finding 6 — dependência cross-repo opaca em doc público).
  - Preservar tom descritivo do philosophy.md atual; não introduzir verbos imperativos ("siga", "faça") nem stance pessoal ("o autor acredita").

## Verificação end-to-end

Inspeção textual (sem `make test` — `test_command: null` per CLAUDE.md config):

```bash
# Nova seção presente e posicionada antes de "A filosofia em uma frase"
grep -n "^## " docs/philosophy.md | head -5
# Esperado: linha 1 (#); linha N (## Princípios fundamentais) antes de linha M (## A filosofia em uma frase) com N < M.

# +3 subseções H3 novas (Busca pela verdade, Excelência sem over-engineering, Navalha de Ockham)
# — invariante anti-fusão/split inesperado per design-reviewer finding 7.
expected_h3=$(( $(git show HEAD:docs/philosophy.md | grep -c "^### ") + 3 ))
actual_h3=$(grep -c "^### " docs/philosophy.md)
[ "$actual_h3" -eq "$expected_h3" ] && echo "Estrutura ### OK" || echo "ALERTA: contagem ### inesperada (esperado $expected_h3, observado $actual_h3)"

# 3 princípios nomeados no corpo
grep -qE "Busca pela verdade" docs/philosophy.md && \
grep -qE "Excelência sem over-engineering" docs/philosophy.md && \
grep -qE "Navalha de Ockham|Ockham" docs/philosophy.md && \
echo "Princípios OK"

# Triangulação + mapping presentes
grep -q "Triangulação" docs/philosophy.md && \
grep -q "Mapping" docs/philosophy.md && \
echo "Triangulação+Mapping OK"

# Framing descritivo — sem imperativos nem personalismo (per design-reviewer finding 2)
grep -niE "(você deve|você precisa|o autor|acreditamos|na nossa|recomendamos que você)" docs/philosophy.md && echo "ALERTA: prescritivo/personalista detectado" || echo "Framing OK"

# Footnote framing presente
grep -qE "não é prescrição ao leitor|descreve o que o toolkit assume" docs/philosophy.md && echo "Footnote OK"

# Cross-ref a ADR-035 já existente preservado
grep -q "ADR-035" docs/philosophy.md && echo "Cross-ref preservado"
```

Esperado: 6 linhas `OK` impressas; nenhum `ALERTA`.

## Decisões absorvidas

- plan § Contexto: explicitar filtro ADR-035 interno (custo baixo + clareza ganha como tradução pública de raízes meta-teóricas) — inocula contra futura releitura "cerimônia editorial?" (caminho-único).
- plan § Bloco 1: gabarito mecânico anti-prescritivo ("O toolkit assume X" / "Este princípio orientou o design quando Y") + footnote de framing logo após a abertura ("Esta seção descreve o que o toolkit assume; não é prescrição ao leitor") — framing constraint mecanizada, não apenas declarada (caminho-único).
- plan § Bloco 1: fechar decisões (c) sem footnote a meta-system commit e (d) triangulação em prosa (vs diagrama) — design-reviewer confirmou defaults; remover deferimento explícito do Resumo (caminho-único).
- plan § Verificação end-to-end: invariantes adicionais — count `^### ` esperado (anti-fusão/split), anti-prescritivo expandido (`você deve|acreditamos|na nossa|recomendamos`), footnote framing presente (caminho-único).
