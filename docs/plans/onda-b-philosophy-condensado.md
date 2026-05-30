# Plano — Onda B da redesign da camada doutrinal (philosophy.md condensado)

## Contexto

**ADRs candidatos:** ADR-045 (apex da redesign — § Decisão parte 1 § Implementação lista Onda B com escopo literal), ADR-043 (apex doutrinal vigente — § Ockham operacionalizado critério 4 que será promovido; § Universalidade já antecipou conceitualmente "os mesmos 4 critérios aplicam-se conceitualmente a decisões sobre entidades em código consumer"), ADR-035 (Substituído por ADR-043 — referência em linha 25 será removida junto com a § Codificação estrutural), ADR-012 (idioma artefatos por audiência — confirmar audience-aware framing intacto via footnote).

Onda B (segunda) da redesign da camada doutrinal coordenada por `docs/plans/redesign-camada-doutrinal-charter.md`. Per ADR-045 § Decisão parte 1 § Implementação literal: *"Onda B — `philosophy.md` condensado em ~150 linhas: cortar § Codificação estrutural (overhead editorial identificado durante crítica externa); promover critério 4 do § Ockham operacionalizado (≥3 pattern emergente) como condição geral de quando YAGNI termina (de internal-plugin a regra universal, já conceitualmente preparado em ADR-043 § Universalidade); manter triangulação, mapping, audience-aware framing"*.

**Operações cirúrgicas no § Princípios fundamentais** (linhas 5-27 atuais):

1. **Cortar § Codificação estrutural** (parágrafo na linha 27 atual). Overhead editorial self-justificativo identificado pela crítica externa turno 1 (sessão `tres-principios` 2026-05-30); conteúdo essencial vive em ADR-045 (cross-ref via bullet em CLAUDE.md § Editing conventions, shippado Onda A) e em ADR-043 (apex doutrinal). Parágrafo cumpriu função de transition narrative durante reforma doutrinária; pós-ADR-045 é redundante.

2. **Cortar última frase da linha 25** (§ Mapping) que referencia ADR-035: *"ADR-035 (linkado na seção seguinte) particiona aplicação do princípio Ockham entre regras transmitidas ao consumer (YAGNI ortodoxo) e decisões internas do plugin (filtro de coerência), refletindo essa raiz."* Era scaffolding apontando para § Codificação estrutural (a "seção seguinte"); com § Codificação estrutural cortada, a frase fica órfã + ADR-035 está Substituído. Substância da partição vive em ADR-043 § Ockham operacionalizado.

3. **Promover critério 4 do ≥3 pattern emergente** como condição geral de quando YAGNI termina. Inserir parágrafo curto entre § Mapping (linha 25 truncada) e § A filosofia em uma frase (linha 29 atual). Substância: derivar YAGNI como *"não abstraia até saber"* (alavanca da crítica turno 2) — YAGNI cede quando há evidência empírica acumulada (≥3 aplicações ad hoc do mesmo pattern); antes disso mantém caminho concreto. Cross-ref a ADR-043 § Ockham operacionalizado critério 4 (substância vive lá; philosophy.md aponta, não duplica).

4. **Enriquecer § Triangulação reconhecendo ordem contextual abstrata.** Adicionar 1 frase ao final do parágrafo Triangulação (linha 23) — preserva substância central ("as três atuam juntas") + reconhece nuance operacional que o toolkit aplica em prática. Resolve gap empírico descoberto pelo design-reviewer F3 (re-derivação ad hoc da ordem) sem fixar hierarquia universal incorreta. Versão abstrata: nomeia categorias gerais (*investigação* vs *proposta de estrutura*) sem citar instâncias específicas (skills, ADRs, mecanismos) que defasam com evolução do toolkit. Permite ao agente-leitor inferir a partir da natureza da decisão, mantendo flexibilidade. Decidido após cutucada operador na re-análise da F3 (3 alternativas originais ampliadas para 4 com a abstrata sobrevivendo).

**Audience-aware framing intacto.** Footnote linha 9 *"Esta seção descreve o que o toolkit assume; não é prescrição ao leitor"* preservada — sinaliza distinção descritivo/prescritivo per ADR-012 + cross-cutting de framing audience-aware (consumer terceiro avaliando o pacote vs operator codificando doutrina interna).

## Resumo da mudança

Edit cirúrgico único em `docs/philosophy.md` § Princípios fundamentais:

- **Remove:** última frase da linha 25 (referência a ADR-035 órfã) + parágrafo "Codificação estrutural da hierarquia" (linha 27).
- **Adiciona:** parágrafo "Quando YAGNI termina" entre § Mapping (linha 25 truncada) e § A filosofia em uma frase (linha 29 atual).
- **Enriquece:** § Triangulação (linha 23) com 1 frase final reconhecendo ordem contextual abstrata (categorias *investigação* / *proposta de estrutura*) — resolve gap descoberto pelo design-reviewer F3 sem fixar hierarquia universal nem citar instâncias específicas defasáveis.

Saldo líquido: ~0 a -1 linha (1 frase + 1 parágrafo cortados, 1 frase + 1 parágrafo adicionados). Carga doutrinal: substituição de self-justification por regra operacional acionável; remoção de scaffolding órfão pós-ADR-045; enriquecimento conceitual da Triangulação preservando audience-aware framing.

**Intactos:** opening sentence + footnote (linhas 7+9), 3 H3 dos princípios (linhas 11-21), § Triangulação substância central (1ª-3ª frases — operação 4 só estende o parágrafo), § Mapping primeira parte (linha 25 até antes da última frase ADR-035), § A filosofia em uma frase em diante (linhas 29+).

**Bifurcação fechada:** ordem operacional V→O→E **NÃO** codificada como hierarquia universal — § Triangulação enriquecida com ordem contextual abstrata (alternativa d sobre a, b, c originais). Decidido após cutucada com operador na re-análise da F3.

## Arquivos a alterar

### Bloco 1 — philosophy.md § Princípios fundamentais {reviewer: doc}

- `docs/philosophy.md`:
  - **Remover** última frase de linha 25 (§ Mapping): *"ADR-035 (linkado na seção seguinte) particiona aplicação do princípio Ockham entre regras transmitidas ao consumer (YAGNI ortodoxo) e decisões internas do plugin (filtro de coerência), refletindo essa raiz."* — scaffolding órfão pós-corte de § Codificação estrutural; ADR-035 Substituído por ADR-043.
  - **Remover** parágrafo de linha 27 inteira (§ Codificação estrutural da hierarquia) — overhead editorial pós-ADR-045 redundante.
  - **Enriquecer** § Triangulação (linha 23) adicionando 1 frase ao final do parágrafo (após *"qualquer uma isolada deteriora."*). Texto sugerido (refinar pelo doc-reviewer se necessário):

    > Em casos concretos, a ordem de aplicação é contextual: investigação tende a partir de Verdade (reproduzir o que existe antes de hipotetizar); proposta de estrutura tende a partir de Ockham (o mínimo viável antes da expansão). A ordem emerge da natureza da decisão, não de hierarquia fixa.

  - **Adicionar** parágrafo curto entre as duas seções restantes (após § Mapping truncado, antes de § A filosofia em uma frase). Texto sugerido (refinar pelo doc-reviewer se necessário):

    > **Quando YAGNI termina.** YAGNI por padrão é Ockham aplicado ao desconhecido — *"não modelar o que não distingue ainda"*. Ele cede quando Verdade já tem evidência: ≥3 aplicações ad hoc do mesmo pattern em casos reais (auditável retroativamente, conforme [ADR-043](decisions/ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § Ockham operacionalizado critério 4) é o ponto onde a abstração ganha seu custo. Até esse ponto, o toolkit prefere o caminho concreto, refatorando quando o pattern empiricamente se confirmar.

## Verificação end-to-end

**Critério de sucesso da Onda B:**

1. `grep "Codificação estrutural da hierarquia" docs/philosophy.md` → vazio (parágrafo removido).
2. `grep "ADR-035" docs/philosophy.md` → vazio (toda referência a ADR Substituído removida; doutrina vigente não aponta para ancestral arquivado).
3. `grep "Quando YAGNI termina" docs/philosophy.md` → 1 match (parágrafo adicionado).
4. `grep "ADR-043.*critério 4" docs/philosophy.md` → 1 match (cross-ref correto).
5. § Princípios fundamentais permanece em ~22 linhas após operação (atual 22; saldo líquido ~-1 a 0 — operações 1+2 cortam ~3 linhas, operações 3+4 adicionam ~4 linhas; cap nominal ADR-045 ~150 para philosophy.md inteiro — Onda B mantém ou levemente reduz; sem aproximação do cap).
6. `grep "Triangulação\|Mapping para a doutrina pragmática" docs/philosophy.md` → 2 matches (preservados).
7. § Triangulação enriquecida: `grep "ordem de aplicação é contextual" docs/philosophy.md` → 1 match (frase abstrata sobre ordem contextual adicionada).
8. § Triangulação substância central preservada: `grep "três condições atuam juntas — qualquer uma isolada deteriora" docs/philosophy.md` → 1 match (frase apex intacta).
9. Estrutura subsequente preservada: `grep -c "^## " docs/philosophy.md` ≥ 10 (atual 11 H2 sections; Onda B não toca headers H2 — § Codificação estrutural removido é parágrafo bold, não H2).
10. Footnote audience-aware intacto: `grep "Esta seção descreve o que o toolkit assume; não é prescrição ao leitor" docs/philosophy.md` → 1 match.
9. doc-reviewer audita drift: cross-ref a ADR-043 está sintático e semanticamente correto; promoção do critério 4 fiel à substância sob ADR-043 § Ockham operacionalizado.
10. design-reviewer auto-fire em /triage step 5 valida: condensação preserva carga doutrinal per anti-regression checklist em `docs/plans/redesign-camada-doutrinal-charter.md` § Verificação end-to-end categoria "Princípios e doutrina apex" — Triangulação preservada (intacta), Mapping preservado (intacto exceto última frase órfã), 4 critérios de Ockham operacionalizado preservados em ADR-043 + critério 4 agora promovido a regra universal em philosophy.md.

## Notas operacionais

**Ordem do bloco único:** Bloco 1 executado em /run-plan single-block; doc-reviewer no diff; design-reviewer cutucada via wiring (caminho-com-plano per ADR-011) atua sobre o plano antes do commit do /triage.

**Risco de drift entre ADR-043 e philosophy.md pós-promoção:** o critério 4 vive tanto em ADR-043 § Ockham operacionalizado (escopo internal-plugin com numeração específica 1-4) quanto em philosophy.md (regra universal). Mitigação: cross-ref explícito do parágrafo philosophy.md → ADR-043 § Ockham operacionalizado critério 4 (não duplica substância — apontador). Futuro refinamento do critério 4 (gatilhos de revisão de ADR-043) vive no ADR; philosophy.md aponta para a versão vigente.

**Bifurcação fechada:** ordem operacional V→O→E com Ockham veto NÃO codificada como hierarquia universal. § Triangulação enriquecida em vez disso com ordem contextual abstrata (operação 4) — nomeia categorias gerais (*investigação* / *proposta de estrutura*) sem citar instâncias específicas (skills, ADRs, mecanismos) que defasam. Decidido após re-análise da F3 com 4 alternativas competindo (status quo / V→O→E / Ockham primeiro / context-dependent enriquecida); operador escolheu alternativa (d) abstrata.

**Dissolução natural da distinção plugin/consumer.** Operações 3 e 4 são pró-dissolução da polaridade plugin-internal vs consumer-facing codificada em ADR-043 § Polaridade. Operação 3 promove critério 4 (≥3 pattern emergente) ao universal sem qualificador plugin-internal; operação 4 categoriza a ordem por **natureza da decisão** (investigação vs proposta de estrutura), não por **autor** (quem decide). Decisão de dissolver NÃO requer ADR novo: passa pelo filtro de admissão de ADR-045 § Decisão parte 2 como "entendimento estabilizado" (não estrutural reversível; não categoria conceitual nova; não restrição externa) → vai para `philosophy.md` (onde Onda B já está escrevendo). ADR-043 § Polaridade permanece imutável como referência histórica; eventual consolidação em ADR-011 da nova estrutura (alguma onda C-X) descontextualiza naturalmente sem editar ADR-043. Admission policy aplicada à própria decisão de refinamento — paralelo a risco a vigiar codificado em ADR-045 § Decisão parte 2 *"refinamentos vão pra `CLAUDE.md` ou git log, não pra ADR-045 § Decisão"*, generalizado para *"refinamentos de doutrina pré-existente vão pra `philosophy.md`, não para novo ADR"*.

**Pós-merge:** atualizar BACKLOG umbrella in-place anotando Onda B shipped (paralelo a Onda A commit `0bf1aa8`); próximo /triage para Onda C (primeira migração cluster — sequence a ser refinada no charter durante execução).

**Cap de condensação para philosophy.md inteiro:** ADR-045 estima ~150 linhas. Atual philosophy.md tem 107 linhas (`wc -l`). Onda B contribui ~0 a -2 linhas. Resultado pós-Onda B: ~105-107 linhas — bem abaixo do cap; nenhuma onda adicional de condensação necessária no philosophy.md. Ondas C-X focam em consolidação de ADRs (inventário) onde o crescimento O(#decisões) é a alavanca real.

## Decisões absorvidas

- § Verificação end-to-end item 2: grep alargado de `"ADR-035 (linkado na seção seguinte)"` para `"ADR-035"` cobre intent doutrinal (doutrina vigente não aponta para ADR Substituído) sem fragilidade a refinamento de wording (caminho-único).
- § Arquivos a alterar Bloco 1 texto: fechamento descritivo *"Até esse ponto, o toolkit prefere o caminho concreto, refatorando..."* substitui imperativo *"mantenha o caminho concreto"* — preserva audience-aware framing declarado pelo próprio plano (footnote linha 9 de philosophy.md) (caminho-único).
- § Notas operacionais cap de condensação: contagem corrigida de `~120 linhas` para `107 linhas` via `wc -l` — exatidão empírica em estimativa que entra no critério de sucesso (caminho-único).
- § Verificação end-to-end item 7: grep nominal de 5 headers H2 substituído por contagem `grep -c "^## "` ≥ 10 — abrangência estrutural verificada sem listar nominais (caminho-único).
- **Bifurcação F3 (ordem operacional Verdade→Ockham→Excelência com Ockham veto):** fechada com alternativa (d) abstrata — § Triangulação enriquecida com 1 frase reconhecendo ordem contextual (operação 4 do Bloco 1). Re-análise expandiu as 3 alternativas originais (status quo / V→O→E / Ockham primeiro) com (d) emergente da observação empírica direta: o toolkit já aplica V primeiro em investigação (reproduzir antes de hipotetizar) e O primeiro em proposta de estrutura (mínimo viável antes da expansão). Operador escolheu (d) com diretiva de manter abstrato — nomeia categorias gerais (*investigação* / *proposta de estrutura*) sem citar instâncias específicas (skills, ADRs, mecanismos) que defasam com evolução do toolkit. Resolve gap empírico de re-derivação ad hoc da ordem sem fixar hierarquia universal incorreta. Discriminante da ordem é a **natureza da decisão**, não o **autor** (plugin-vs-consumer) — direção pró-dissolução da distinção plugin/consumer; ver § Notas operacionais. Bifurcação documentada como fechada (não deferida) — ondas C-X podem revisitar se sinal empírico mostrar que a abstração ainda gera drift, mas codificação atual é decisão estrutural (caminho-único após cutucada — registro estruturado da escolha entre 4 alternativas).
