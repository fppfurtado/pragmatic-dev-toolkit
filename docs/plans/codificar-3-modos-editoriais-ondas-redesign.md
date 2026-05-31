# Plano — Codificar 3 modos editoriais de refinamento da consolidação (ADR-052)

## Contexto

**ADRs candidatos:** ADR-045 (apex redesign — esta intenção refina § Decisão linha 56 fronteira "absorção em consolidado diferente do sketch original" para incluir explicitamente as 3 categorias editoriais emergentes; sucessor parcial primário per cond 5), ADR-034 (critério adendo vs novo ADR — cond 5 sucessor parcial primário aplica isolada), ADR-035 (escopo YAGNI próprio plugin — critério 4 "≥3 pattern emergente" atingido pós-Onda H), ADR-013 (precedente editorial "critério mecânico cumulativo" reusado em ADR-020/-022/-023 via ADR sucessor — pattern paralelo a esta codificação), ADR-049 (template Onda F — refinamento editorial 1ª instância por exclusão), ADR-050 (template Onda G — refinamento editorial 2ª instância por inclusão), ADR-051 (template Onda H — refinamento editorial 3ª instância por preservação por constraint mecânico; § Origem documenta gatilho disparado), ADR-043 (hierarquia doutrinal fundamentais raiz — 3 princípios aplicados ao próprio inventário endossam codificação per Verdade/Excelência/Ockham triangulado).

ADR-052 é meta-decisão editorial pontual codificando pattern emergente das Ondas F+G+H. **NÃO é onda de migração de cluster** — categoria semântica distinta (refinamento meta-doutrinal apex). Plano segue Onda A pattern (charter + ADR-045 + CLAUDE.md bullet) em vez de Ondas B-H pattern (migração temática), por proximidade categórica:

1. **Gatilho disparado pós-Onda H** — 3 instâncias de refinamento editorial atingem critério ADR-035 "≥3 pattern emergente" (regra base por ADR-043 § Ockham operacionalizado em decisões internas do plugin, critério 4). Charter § "Refinamento editorial documentado" registrou sinal a observar pré-Onda H; sinal materializado pós-Onda H.
2. **Decisão de operador registrada** — Opção B (ADR sucessor) escolhida sobre Opção A (status quo continuar absorvendo) e Opção C (aguardar 4ª instância). Pattern paralelo a ADR-020/-022/-023 que reusaram "critério mecânico cumulativo" de ADR-013 via ADR sucessor.
3. **Sem refinamento estrutural da regra de consolidação** — fronteira de ADR-045 § Decisão linha 56 ("absorção em consolidado diferente do sketch") permanece intacta como ajuste editorial livre; ADR-052 explicita as 3 categorias editoriais que cabem dentro dela. Decisão central de ADR-045 (consolidação 45 → ~13-15 ADRs sob hierarquia invertida + filtro de admissão) preservada integralmente.
4. **Aplicação imediata** — ADR-052 codifica antes da Onda I (alinhamento/triage com constraint análogo always-include sobre ADR-009) para que Onda I aplique modo (c) preservação por constraint com **referência formal estabelecida** em vez de descobrir o pattern reativamente.
5. **Sem cluster shape** — não há migração de ADRs antigos; apenas adição de ADR-052 + CLAUDE.md bullet. Charter atualização post-merge documenta meta-pattern editorial canonical.

**Linha do backlog:** ADR-052 é sub-scope da umbrella multi-onda redesign em `## Próximos`; não corresponde a linha distinta. Per ADR-049 § Decisão (a) + precedente Ondas A-H, umbrella é atualizada in-place post-merge.

## Resumo da mudança

**Este plano produz:**

1. **ADR-052 consolidado** (criado via `/new-adr` no /triage step 4) — sucessor parcial de ADR-045 codificando os 3 modos editoriais emergentes nas Ondas F+G+H. § Decisão integra:
   - **(a) EXCLUSÃO de ADRs semanticamente desalinhados** do sketch original — caso de uso: cluster sketch agrupou por proximidade numérica em vez de coesão semântica; ADR semanticamente pertence a outro cluster (atual ou futuro). Exemplo canonical: Onda F excluiu ADR-037 (README framing Product Engineer) do cluster execução/run-plan por pertencer a discoverability/branding; Onda F também NÃO absorveu ADR-010 (progress display Task tool) do cluster execução apesar de ser decisão base de ADR-039 (categoria distinta com potencial consumers futuros além de `/run-plan`). Critério mecânico: ADR pertence semanticamente a categoria diferente da do cluster sendo migrado (verificável por leitor independente do sketch).
   - **(b) INCLUSÃO de ADRs omitidos do sketch** quando coesão semântica de família justifica — caso de uso: sketch omitiu ADR aparentemente por descuido editorial; ADR pertence a família semântica já presente no cluster. Exemplo canonical: Onda G incluiu ADR-015 (hook block_env por sufixo `.env`) ao cluster componentes plugin apesar de omitido no sketch (5 ADRs listados; ADR-015 omisso); pertence à família PreToolUse block hooks (ADR-040 § Origem cita ADR-015 como "ancestral direto — primeiro PreToolUse block hook do plugin"); excluir deixaria órfão membro da família coesa. Critério mecânico: ADR pertence a família semântica já no cluster + omissão do sketch é descuido editorial (verificável por cross-ref doutrinal entre ADR omitido e ADRs incluídos).
   - **(c) PRESERVAÇÃO de ADRs ancestrais fora do cluster por constraint mecânico** — caso de uso: ADR está hardcoded em § Decisão de outro ADR Aceito — absorvê-lo exigiria editar ADR-classical (antipattern) + quebraria caminho mecânico de leitura por sistemas que consultam o hardcode. Exemplo canonical (Onda H): preservou ADR-034 (critério adendo vs novo ADR) por hardcoded na always-include de ADR-048 § Decisão `[ADR-009, ADR-034, ADR-043]`. Categoria semântica distinta (meta-doutrina apex) **reforça** decisão mas NÃO é critério independente. Critério mecânico: grep do ID do ADR em § Decisão de ADR Aceito vigente retorna match (verificável objetivamente). **Caso de preservação por categoria distinta SEM constraint mecânico cai em modo (a) EXCLUSÃO bullet 2** — ex.: ADR-010 (progress display) Onda F NÃO absorvido por categoria distinta de state-keeping (ADR-039 absorvido), sem hardcode → modo (a) bullet 2 "ancestralidade codificada com categoria distinta". Discriminação mecânica via grep evita zona cinzenta entre (a) bullet 2 e (c).

   **Aplicação à fronteira ADR-045 § Decisão linha 56:** ADR-045 § Decisão linha 56 lista "ajuste de cluster sequence (ordem de migração), subdivisão de consolidado em 2, **absorção de ADR em consolidado diferente do sketch original**" como ajuste editorial livre. ADR-052 refina o terceiro item ("absorção em consolidado diferente do sketch") explicitando que **as 3 modalidades editoriais (a)+(b)+(c) cabem dentro dele**. Decisão central de ADR-045 preservada; refinamento é explicitação do escopo da fronteira existente, não revisão estrutural.

   **Mecanismo de aplicação canonical para ondas I-X:**
   - Cada onda de migração identifica composição do cluster vs sketch original.
   - Se a composição difere do sketch, classificar refinamento por modo (a/b/c) com critério mecânico aplicado.
   - Documentar em § Origem do ADR consolidado da onda + charter § "Atualização pós-execução" sub-seção dedicada (pattern Ondas F+G+H reaplicado).
   - Operador pode aplicar combinação de modos numa mesma onda (ex.: exclusão + inclusão; preservação + exclusão) — modos não são mutuamente exclusivos.

   **Quando NÃO aplica ADR-052** (modos editoriais cobrem 99% dos refinamentos, mas não 100%):
   - Cluster sequence reordering (ordem de execução das ondas) — coberto pelo primeiro item de ADR-045 § Decisão linha 56.
   - Subdivisão de consolidado planejado em 2 ADRs (ex.: alinhamento dividido em alinhamento + reviewer dispatch) — coberto pelo segundo item de ADR-045 § Decisão linha 56.
   - Mudança estrutural da regra de consolidação (abandonar hierarquia invertida, reverter para 45 fragmentados) — fora da fronteira; revisão formal de ADR-045 via § Gatilhos.

   **Escalação se 4º modo editorial emergir** — categoria editorial nova não-coberta por (a)+(b)+(c) em Ondas I-X disparar revisão de ADR-052 (gatilho próprio do ADR sucessor). Pattern paralelo a ADR-020 que refinou "critério mecânico cumulativo" para 3 cumulativos + 1 pré-requisito; ADR-052 pode ser refinado se novo modo aparecer.

   § Origem histórica preserva 3 incidentes empíricos das Ondas F+G+H que motivaram codificação (referenciando ADR-049/-050/-051 § Origem para detalhes; sem duplicar substância). § Gatilhos consolida triggers de revisão. § Auto-aplicação per ADR-034: cond 5 primária isolada (sucessor parcial estendendo ADR Aceito sem revogar); cond 4 NÃO aplica (refinamento editorial dentro de categoria existente "consolidação da redesign", não categoria nova de artefato); cond 1 NÃO aplica (ADR-045 ancestral codificado direto); cond 2 NÃO aplica (regra central de ADR-045 preservada); cond 3 NÃO aplica (sem restrição externa).

2. **CLAUDE.md § "Editing conventions" bullet** — adição de bullet meta-doutrinal cross-ref a ADR-052 (paralelo aos 10+ bullets meta-doutrinais existentes: ADR-010/-011/-026/-034/-043/-045/-048/-049/-050/-051). Posicionamento: após bullet sobre redesign da camada doutrinal (ADR-045) e antes do bullet sobre curadoria do free-read (ADR-048), ordenado por proximidade semântica.

   Texto sugerido: **"Refinamento editorial das ondas de migração da redesign**: 3 modos editoriais canonical (exclusão + inclusão + preservação por constraint) per [ADR-052](docs/decisions/ADR-052-<slug>.md) — sucessor parcial de ADR-045 explicitando que as 3 modalidades cabem dentro da fronteira § Decisão linha 56 (\"absorção em consolidado diferente do sketch original\") como ajustes editoriais livres. Aplicável às Ondas I-X de migração; documentado em § Origem do ADR consolidado da onda + charter § Atualização pós-execução."

3. **Charter atualização** (post-merge, manual) — `docs/plans/redesign-camada-doutrinal-charter.md` § "Refinamento editorial documentado" atualizada refletindo codificação formal via ADR-052 (substituindo o registro de "gatilho disparado a observar" por "gatilho disparado e codificado em ADR-052"). NÃO escopo deste plano; commit separado post-merge per precedente Ondas A-H.

**Pattern editorial deste plano** (Onda A-like pattern reaplicado para refinamento meta-doutrinal apex):
- Plano + ADR via /new-adr + CLAUDE.md bullet em bloco único.
- 1 bloco `{reviewer: doc}` para CLAUDE.md bullet (doc-only).
- Pendência operacional Onda F mantida endereçada: reviewer-per-bloco estrito (invariante 7 instâncias consecutivas — ondas C+D+E+F+G+H + este plano).
- Sem migração de ADRs antigos (nenhum archive); apenas adição de novo ADR-052 + CLAUDE.md bullet.

## Arquivos a alterar

### Bloco 1 — CLAUDE.md § "Editing conventions" bullet ADR-052 {reviewer: doc}

- `CLAUDE.md` § "Editing conventions" — adicionar bullet meta-doutrinal cross-ref a ADR-052 após o bullet sobre redesign (ADR-045) e antes do bullet sobre curadoria do free-read (ADR-048). Posicionamento por proximidade semântica.

Texto exato a adicionar (revisar pelo doc-reviewer no Bloco 1 se necessário):

```markdown
- **Refinamento editorial das ondas de migração da redesign**: 3 modos editoriais canonical (exclusão + inclusão + preservação por constraint) per [ADR-052](docs/decisions/ADR-052-codificacao-3-modos-editoriais-refinamento-consolidacao.md) — sucessor parcial de ADR-045 explicitando que as 3 modalidades cabem dentro da fronteira § Decisão linha 56 ("absorção em consolidado diferente do sketch original") como ajustes editoriais livres. Aplicável às Ondas I-X de migração; documentado em § Origem do ADR consolidado da onda + charter § Atualização pós-execução.
```

Slug final do ADR-052 a ser confirmado pelo /new-adr (sugestão acima é approximation; substituir pelo path canonical real após criação).

## Verificação end-to-end

**Critérios de sucesso deste plano:**

1. **ADR-052 criado** com Status `Proposto` em `docs/decisions/ADR-052-<slug>.md`. § Origem cita ADR-045 como ancestral codificado direto + ADR-049/-050/-051 como templates documentando os 3 modos empíricos + ADR-034 cond 5 como critério editorial + ADR-035 critério 4 + ADR-013 como precedente editorial de "critério mecânico cumulativo" via ADR sucessor. § Decisão integra os 3 modos (a/b/c) sob narrativa única coerente. § Origem histórica referencia 3 incidentes empíricos sem duplicar substância. § Gatilhos consolida triggers. § Auto-aplicação cond 5 primária isolada.

2. **CLAUDE.md § "Editing conventions" estendida:** `grep -c "Refinamento editorial das ondas de migração da redesign" CLAUDE.md` → 1 match (bullet adicionado).

3. **Cross-ref do bullet aponta para path canonical correto:** `grep -c "ADR-052-codificacao-3-modos-editoriais-refinamento-consolidacao.md" CLAUDE.md` → 1 match (path resolve para arquivo real criado por /new-adr).

4. **Bullet posicionado adjacente ao ADR-045** (proximidade semântica): `grep -n "ADR-045\|ADR-052\|ADR-048" CLAUDE.md` → ordem ADR-045 (linha N), ADR-052 (linha N+1), ADR-048 (linha N+2 ou N+3).

5. **Substância dos 3 modos editoriais preservada literal:** `grep -cE "EXCLUSÃO|INCLUSÃO|PRESERVAÇÃO" docs/decisions/ADR-052-*.md` → ≥3 matches (cada modo nominalmente codificado).

6. **Aplicação à fronteira ADR-045 § Decisão linha 56 explícita:** `grep -c "fronteira.*linha 56\|absorção em consolidado diferente do sketch" docs/decisions/ADR-052-*.md` → ≥1 match (refinamento de escopo, não revisão estrutural).

7. **doc-reviewer audita drift cross-doc:** cross-ref correto cross-doc; ADR-052 substância coerente com plano + charter § "Refinamento editorial documentado"; substância dos 3 modos preservada literal vs exemplos canonical das Ondas F+G+H.

8. **design-reviewer auto-fire em /new-adr step 5 e /triage step 5** valida: codificação coerente com gatilho disparado (ADR-035 critério 4 + ADR-045 fronteira linha 56); substância dos 3 modos fielmente derivada dos exemplos empíricos das Ondas F+G+H; auto-aplicação per ADR-034 (cond 5 primária; cond 4 NÃO aplica — refinamento dentro de categoria existente "consolidação da redesign"; cond 1 NÃO aplica; cond 2 NÃO aplica — regra central preservada) coerente.

## Notas operacionais

**Ordem dos blocos:** Bloco 1 (CLAUDE.md bullet) executado por `/run-plan` em onda separada após /triage commit (ADR-052 + plano commitados via /triage; CLAUDE.md bullet via /run-plan Bloco 1 — paralelo a Onda A pattern). Alternativa: collapse manual num único commit pós-/triage (operador escolhe — preferir pipeline canonical para validar /run-plan em meta-doutrinal pontual).

**Aderir reviewer-per-bloco estrito (invariante 7 instâncias consecutivas):** Bloco 1 (CLAUDE.md bullet) com `{reviewer: doc}` obrigatório. Pattern editorial validado em 7 ondas (C+D+E+F+G+H + este plano); convergência empírica não admite exceção à doutrina explícita "Não pular revisor, mesmo em bloco trivial" de `skills/run-plan/SKILL.md § O que NÃO fazer`.

**Charter atualização post-merge:** após merge deste plano, atualizar `docs/plans/redesign-camada-doutrinal-charter.md` § "Refinamento editorial documentado":
- Substituir registro "gatilho disparado a observar / decisão deferida ao operador" por "gatilho disparado e codificado formalmente via ADR-052; meta-pattern editorial canonical das ondas de migração estabelecido".
- Estender § Anti-regression checklist com bullet sobre ADR-052 preservações (3 modos editoriais + aplicação à fronteira ADR-045 linha 56 + escalação se 4º modo emergir).
- Atualizar trajetória esperada: ADRs I-X podem aplicar (a)/(b)/(c) com referência formal estabelecida sem reabrir doutrina por cada onda.
- Saldo inventário pós-este-plano: 51 vigentes + 1 ADR-052 - 0 arquivados = **31 vigentes** (acréscimo de 1; primeiro acréscimo líquido positivo desde Onda A; alinha com natureza meta-doutrinal de ADR-052).
- Anotação progressiva: "ADR-052 shipped — commit <hash>; 3 modos editoriais (exclusão + inclusão + preservação por constraint) codificados formalmente como meta-pattern canonical das ondas de migração; Onda I aplica modo (c) preservação por constraint com referência formal estabelecida".

Update do charter é commit separado post-merge (paralelo às atualizações de umbrella in BACKLOG das Ondas A-H); NÃO escopo deste plano.

**Decisão excluída — refinamento estrutural da regra de consolidação:** ADR-052 NÃO altera regra central de ADR-045 (consolidação 45 → ~13-15 ADRs sob hierarquia invertida + filtro de admissão). Apenas explicita as 3 categorias editoriais que cabem dentro da fronteira existente § Decisão linha 56. Mudança estrutural na regra de consolidação (ex.: abandonar hierarquia invertida, reverter para 45 fragmentados) continua sendo gatilho de revisão de ADR-045 via § Gatilhos próprios (não disparado por ADR-052).

**Decisão excluída — codificar pattern editorial bidirecional separado de preservação por constraint:** Onda G F4 cutucada original (bidirecionalidade) propunha codificar exclusão + inclusão como pattern bidirecional. Onda H adicionou preservação por constraint como 3ª categoria. ADR-052 codifica os 3 modos juntos (exclusão + inclusão + preservação por constraint) em vez de separar bidirecional + preservação. Justificativa: 3 modos compartilham mesmo escopo aplicacional (refinamento da composição do cluster vs sketch), apenas direção da operação difere. Codificar como pattern unitário com 3 modalidades é mais Ockham que 2 ADRs separados.

**Decisão excluída — esperar 4ª instância (Opção C) antes de codificar:** ADR-035 critério 4 (≥3 pattern emergente) já atingido em rigor pós-Onda H. Esperar 4ª instância adiaria meta-pattern formal sem evidência adicional necessária — apenas validação empírica extra. Opção C foi avaliada e rejeitada por operador em favor de Opção B (codificação preventiva antes da Onda I aplicar modo (c) preservação por constraint análoga).

**Pendência operacional Onda F mantida endereçada:** Bloco 1 (CLAUDE.md bullet) com `{reviewer: doc}` obrigatório — invariante 7 instâncias consecutivas (ondas C+D+E+F+G+H + este plano). Nunca skip de reviewer mesmo em bloco trivial.

**Sinal a observar para Onda I e ondas subsequentes:** após ADR-052 codificado, observar se Onda I (alinhamento/triage com constraint análogo always-include sobre ADR-009) aplica modo (c) preservação por constraint **com referência formal a ADR-052** — confirma valor do mecanismo. Se Onda I descobrir 4º modo editorial não-coberto por (a)+(b)+(c), reabrir ADR-052 com refinamento (pattern paralelo a ADR-020 que refinou "critério mecânico cumulativo" para 3 cumulativos + 1 pré-requisito).

## Decisões absorvidas

- ADR-052 § Origem linha 8 + § Aplicação à fronteira ADR-045: linguagem reescrita explicitando que ADR-052 **promove** 3 categorias editoriais emergentes para meta-pattern canonical com força normativa (vs documentação passiva); "promoção honesta" vs "cabem dentro da fronteira" — F3 absorvido (caminho-único).
- ADR-052 § Auto-aplicação cond 4: justificativa reforçada substituindo paralelo fraco com ADR-020/-013 (que reusaram pattern operacional maduro) por argumento direto sobre leitura estreita de "categoria conceitual de artefato" per ADR-034 § Auto-aplicação — F1 absorvido (caminho-único).
- ADR-052 § Decisão (c) PRESERVAÇÃO restrita a constraint mecânico puro (cobertura modo (c) só caso ADR-034 hardcoded); sub-caso 2 (categoria semântica distinta sem constraint) **colapsado em modo (a) EXCLUSÃO bullet 2** — caso ADR-010 (Onda F) fica como exemplo canonical de (a) bullet 2, não de (c) sub-caso 2. Critério mecânico genuinamente discriminativo: grep ID em § Decisão de ADR Aceito vigente = modo (c); sem grep + categoria distinta = modo (a) bullet 2. F2 absorvido via opção (A) recomendada pelo reviewer — operador escolheu sobre (B) reescrever critério (c)(2) com cross-ref ativo / (C) status quo fortalecendo gatilho. Justificativa: alinhamento Ockham (ADR-043 § Ockham operacionalizado — "não modelar o que não distingue") + critério mecânico genuíno + cobertura empírica preservada (ADR-010 + ADR-034 ambos ainda cobertos).
- § Trade-offs + § Limitações + § Gatilhos de revisão atualizados refletindo nova fronteira (a) bullet 2 vs (c) — discriminação mecânica via grep substitui zona cinzenta de "categoria semântica distinta" (F2 follow-through).

## Pendências de validação

(A ser preenchida pelo `/run-plan` se ficarem itens pendentes pós-execução.)
