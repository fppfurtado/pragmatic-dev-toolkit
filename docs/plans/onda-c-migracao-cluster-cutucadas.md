# Plano — Onda C da redesign da camada doutrinal (migração cluster cutucadas)

## Contexto

**ADRs candidatos:** ADR-017 (foundational do cluster — cutucada uniforme em skills, gating triplo, string canonical, herança editorial), ADR-029 (sucessor parcial — cobre CLAUDE.md ausente, string-B, dedup conversation-scoped por string), ADR-045 (apex redesign — esta onda materializa § Decisão parte 1 § Implementação literal), ADR-043 (apex doutrinal — Ockham operacionalizado critério 4 governa criação do consolidado), ADR-034 (critério adendo vs novo ADR — orienta criação do consolidado: cond 5 sucessor parcial primário + cond 4 categoria nova de artefato "consolidação cross-ADR" + cond 1 sem ancestral direto codificado), ADR-024 (categoria `docs/procedures/` — procedure cutucada-descoberta.md preservada intacta), ADR-005 (precedente do Addendum cluster da Onda 3 — pattern parcial de consolidação editorial).

Onda C (terceira) da redesign da camada doutrinal coordenada por `docs/plans/redesign-camada-doutrinal-charter.md`. **Primeira migração cluster temático** per ADR-045 § Decisão parte 1 § Implementação literal: *"Ondas C-X — migração de ADRs por cluster temático. Cada onda absorve 3-6 ADRs antigos em 1 consolidado..."*.

Cluster cutucadas é o candidato natural para a primeira migração:

1. **Cluster index Addendum já existe** em ADR-017 (Onda 3 da reforma doutrinária, PR #86) enumerando os componentes — proof-of-concept de consolidação editorial já validado parcialmente.
2. **Apenas 2 ADRs + 1 procedure** = scope pequeno (calibra pattern antes de clusters maiores como 005+018+025+030 ou design-reviewer ecosystem 009+011+026+038).
3. **Cluster coeso semanticamente** — ADR-029 só estende cobertura de ADR-017 (mesma mecânica, gating estendido bi-state → tri-state).
4. **Procedure file separation** per ADR-024 já estabeleceu fronteira: doutrina (ADRs) vs mecânica de execução (procedure file).

**Refinamento emergente da estrutura-alvo.** Charter sketch original (11 ADRs) posicionava cutucadas dentro de "ADR-004-skill-alinhamento-triage" absorvendo 8 ADRs antigos. Esta onda materializa cutucadas como **cluster próprio standalone** (não como sub-cluster dentro de alinhamento) — refinamento editorial do charter per ADR-045 § Decisão parte 1 *"fronteira ajuste editorial do charter vs revisão de ADR-045"* (categoria editorial sem mudança estrutural na regra de consolidação). Charter será atualizado pós-merge da Onda C registrando que cutucadas emergiu como cluster próprio (sketch evolui para ~12-13 ADRs conforme execução das ondas, dentro do range esperado).

**Linha do backlog:** Onda C é sub-scope da umbrella multi-onda em `## Próximos`; não corresponde a linha distinta. Per ADR-004 + precedente Ondas A+B, umbrella é atualizada in-place post-merge.

## Resumo da mudança

**Esta Onda C produz:**

1. **ADR-046 consolidado** (criado via `/new-adr` no /triage step 4) — absorve substância de ADR-017 + ADR-029, mantém cross-ref ao procedure `docs/procedures/cutucada-descoberta.md` (preservado intacto per ADR-024). § Origem histórica preserva incidentes empíricos das 2 decisões absorvidas (ADR-017 PJe 2026-05-11 atrito ~30 min antes de skill rodar; ADR-029 caso emergido em `/debug` 2026-05-14 de projetos novos sem CLAUDE.md). § Gatilhos de revisão consolidados das duas decisões. Status `Proposto` (vira `Aceito` após pattern de migração validar).

2. **Archive de ADR-017 e ADR-029** — `git mv` para `docs/decisions/archive/` + header redirect canonical adicionado a cada arquivo movido: `# ADR-NNN: ARCHIVED — content absorbed into ADR-046 (Cutucada uniforme em skills para descoberta de gaps de configuração); see docs/decisions/ADR-046-<slug>.md for current authority`. Conteúdo original preservado abaixo do header para registro histórico per ADR-045 § Decisão parte 1 (*"Arquivamento (não deleção) materializa Verdade"*). Criar diretório `docs/decisions/archive/` se não existe.

3. **Propagação de cross-refs em docs vivos** (5 arquivos):
   - `CLAUDE.md` § Cutucada de descoberta — substitui referências a ADR-017/-029 por ADR-046; preserva mecânica e herança editorial.
   - `docs/procedures/cutucada-descoberta.md` — cross-refs internas ao procedure trocadas para ADR-046; mecânica do procedure (gating tri-state, 2 strings canonical, dedup) preservada intacta per ADR-024.
   - `skills/draft-idea/SKILL.md`, `skills/init-config/SKILL.md`, `skills/note/SKILL.md` — referências aos ADRs antigos atualizadas para ADR-046.

4. **Link rot consciente em docs imutáveis** — outros ADRs antigos (ADR-018/-023/-024/-027/-030/-032/-034/-038/-041/-043/-044/-045) e planos históricos (`docs/plans/*` exceto este e o charter) referenciam ADR-017/-029 mas **NÃO são editados** per convenção ADR-classical (ADRs são registros imutáveis de decisão; nossos planos passados também são registro histórico). Link rot é trade-off aceito do reorg estrutural por ADR-045 implícito (cross-refs em immutable ADRs ficam como registro histórico; reader que clica em ADR-017 link broken acha em `docs/decisions/archive/` por listagem do diretório ou por grep). Pattern para ondas D-X subsequentes.

5. **Charter atualização** (post-merge, manual) — `docs/plans/redesign-camada-doutrinal-charter.md` atualiza menções a ADR-017/-029 (anti-regression checklist § Discoverability + sketch da estrutura-alvo) refletindo que cutucadas emergiu como cluster próprio. NÃO escopo desta Onda C; vai para commit separado post-merge per precedente das Ondas A+B (atualização in-place de umbrella).

**Pattern de migração estabelecido por esta onda** (template para D-X):
- Criar consolidado via `/new-adr` no /triage step 4 (delegação) com § Origem histórica + § Gatilhos consolidados.
- Archive antigos via `git mv` para `docs/decisions/archive/` + header redirect.
- Propagar cross-refs apenas em docs **vivos** (CLAUDE.md + procedures + SKILLs ativas + agents); imutáveis (ADRs e planos antigos) ficam intactos.
- Cap de propagação: limitar a docs ativos consultados em runtime; reduz custo cognitivo e respeita imutabilidade.

## Arquivos a alterar

### Bloco 1 — Archive ADR-017 + ADR-029 + archive index inicial {reviewer: doc}

- Criar diretório `docs/decisions/archive/` se não existe.
- `git mv docs/decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md docs/decisions/archive/`
- Editar topo do arquivo movido inserindo bloco de citação redirect **antes** do `# ADR-017: <título original>` (header original H1 preservado intacto per format codificado em ADR-046 § Razões "Header redirect canonical"):

  ```markdown
  > **ARCHIVED 2026-05-30** — content absorbed into [ADR-046](../ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md); see that ADR for current authority. Body below preserved verbatim for historical record.

  # ADR-017: Cutucada uniforme em skills para descoberta de configuração ausente
  ```

- `git mv docs/decisions/ADR-029-cutucada-descoberta-cobre-claude-md-ausente.md docs/decisions/archive/`
- Editar topo do arquivo movido análogo (substituindo número e título).
- **Criar `docs/decisions/archive/README.md`** com tabela inicial de mapeamento velho → novo (per ADR-046 § Razões "Archive index incremental"):

  ```markdown
  # Archived ADRs

  Mapping of archived ADRs → current authority (post-redesign per [ADR-045](../ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md)).

  | Archived ADR | Absorbed into | Onda |
  |---|---|---|
  | ADR-017 — Cutucada uniforme em skills para descoberta de configuração ausente | [ADR-046](../ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) | C |
  | ADR-029 — Cutucada de descoberta cobre `CLAUDE.md` ausente | [ADR-046](../ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) | C |
  ```

  Cada onda D-X estende a tabela como invariante do plano da onda (paralelo a esta).

### Bloco 2 — CLAUDE.md § Cutucada de descoberta cross-refs {reviewer: doc}

- `CLAUDE.md` § "Cutucada de descoberta" (atualmente referencia ADR-017 e ADR-029 com explanação do gating tri-state e strings canonical): substituir todas as referências a ADR-017/-029 por ADR-046. Preservar substância editorial (mecânica em `docs/procedures/cutucada-descoberta.md`; gating, strings, dedup; herança editorial para nova SKILL). Atualizar o número/slug do path do ADR no link markdown.

### Bloco 3 — procedure cutucada-descoberta.md cross-refs {reviewer: doc}

- `docs/procedures/cutucada-descoberta.md` (mecânica do gating tri-state + 2 strings canonical literais + dedup conversation-scoped): substituir referências a ADR-017/-029 por ADR-046 nas seções de cabeçalho e cross-refs. Mecânica do procedure preservada **intacta** per ADR-024 (procedure é categoria separada; mudança apenas em apontadores de doutrina vigente, não em algoritmo prescritivo).

### Bloco 4 — SKILLs herdeiras cross-refs {reviewer: doc}

- `skills/draft-idea/SKILL.md`: substituir referências a ADR-017/-029 por ADR-046 (final do reporte step onde cutucada é emitida per herança editorial).
- `skills/init-config/SKILL.md`: substituir referências a ADR-017/-029 por ADR-046 (skill que cria o bloco config; gating step 3 e step 4.5 podem referenciar ADR-029 para cobertura de CLAUDE.md gitignored).
- `skills/note/SKILL.md`: substituir referências a ADR-017/-029 por ADR-046 (final do reporte step onde cutucada é emitida per herança editorial).

## Verificação end-to-end

**Critérios de sucesso da Onda C:**

1. **ADR-046 criado** com Status `Proposto` em `docs/decisions/ADR-046-<slug>.md`. § Origem cita ADR-017 + ADR-029 como decisão base + esta onda como investigação. § Origem histórica preserva os 2 incidentes empíricos. § Decisão integra cutucada uniforme (de ADR-017) + cobertura CLAUDE.md ausente (de ADR-029) em narrativa única coerente. § Gatilhos de revisão consolida triggers das 2 decisões.

2. **ADR-017 e ADR-029 arquivados:** `ls docs/decisions/ADR-017-*.md docs/decisions/ADR-029-*.md` → vazio (movidos). `ls docs/decisions/archive/ADR-017-*.md docs/decisions/archive/ADR-029-*.md` → presentes. Header redirect canonical presente no topo de cada arquivo.

3. **`grep "ADR-017\|ADR-029" CLAUDE.md` → 0 matches** (todas referências substituídas por ADR-046).

4. **`grep "ADR-017\|ADR-029" docs/procedures/cutucada-descoberta.md` → 0 matches** (cross-refs internas substituídas).

5. **`grep "ADR-017\|ADR-029" skills/draft-idea/SKILL.md skills/init-config/SKILL.md skills/note/SKILL.md` → 0 matches** (cross-refs nas 3 SKILLs substituídas).

6. **Procedure mecânica preservada:** `grep "string-A\|string-B\|tri-state\|gating\|dedup conversation-scoped" docs/procedures/cutucada-descoberta.md` → matches conforme estado atual (mecânica intacta; apenas apontadores doutrinais atualizados).

7. **CLAUDE.md herança editorial preservada:** § "Cutucada de descoberta" do CLAUDE.md mantém menção a "Editorial inheritance" + cap das 5 SKILLs traversando step 3 + reabertura YAGNI para 6ª cutucada-emitting SKILL.

8. **Link rot em immutable ADRs aceito explicitamente:** `grep -l "ADR-017\|ADR-029" docs/decisions/ADR-0*.md docs/plans/*.md` ainda retornará vários arquivos antigos — esses são imutáveis (immutable ADRs + historical plans); cross-refs em immutable docs ficam como registro histórico, NÃO são editados. Documentar essa lista no commit message.

9. **doc-reviewer audita drift:** cross-refs corretos cross-doc; ADR-046 substância fiel a ADR-017+ADR-029 combinados; nenhuma carga doutrinal da § Discoverability do anti-regression checklist perdida (gating tri-state, strings canonical literais, dedup conversation-scoped, herança editorial — todas preservadas em ADR-046 e/ou procedure intacto).

10. **design-reviewer auto-fire em /new-adr step 5 e /triage step 5** valida: padrão de migração coerente com ADR-045 § Decisão parte 1; pattern reusable para ondas D-X; auto-aplicação per ADR-034 (cond 5+4+1) coerente.

## Notas operacionais

**Ordem dos blocos:** Bloco 1 (archive) executado antes dos demais — outros blocos referenciam ADR-046 que substitui os arquivos arquivados. Blocos 2-4 podem rodar em qualquer ordem (independentes entre si após archive).

**Validação do pattern de migração:** esta é a primeira instância. Se design-reviewer flagrar gap no pattern (ex.: redirect header insuficiente; link rot em immutable ADRs gera confusão maior que esperado; procedure deveria ter sido absorvida vs preservada), refinamento é editorial do plano antes de prosseguir; mudança estrutural na regra de consolidação seria gatilho de revisão de ADR-045.

**Charter atualização post-merge:** após merge da Onda C, atualizar `docs/plans/redesign-camada-doutrinal-charter.md`:
- Anti-regression checklist § Discoverability — atualizar referência de "ADR-017+ADR-029" para "ADR-046" (substância preservada; apenas apontador atualizado).
- Sketch da estrutura-alvo — refinar enumeração refletindo que cutucadas emergiu como cluster próprio (não sub-cluster de alinhamento); contagem final pode ir para ~12-13 ADRs em vez de 11.
- Anotação progressiva: "Onda C shipped — commit <hash>; cluster cutucadas migrado".

Update do charter é commit separado post-merge (paralelo às atualizações de umbrella in BACKLOG das Ondas A+B); NÃO escopo desta Onda C.

**Decisão excluída:** procedure absorption — ADR-024 estabelece categoria docs/procedures/ separadamente; procedure cutucada-descoberta.md NÃO é absorvido por ADR-046. ADR-046 referencia o procedure como executor da mecânica; procedure referencia ADR-046 como autoridade doutrinal. Fronteira limpa.

**Cap de ondas estimado:** charter previa 6-10 ondas. Com cutucadas como cluster próprio standalone (não absorvida em alinhamento), inventário consolidado pode crescer de 11 para 12-13 ADRs. Cap atualizado durante execução.

**Sinal de saúde:** se Bloco 1 (archive) ou Bloco 2 (CLAUDE.md) gerar ≥5 findings de doc-reviewer, sinal de que pattern precisa refinamento antes de aplicar a clusters maiores. Pausar e iterar.

## Decisões absorvidas

design-reviewer no /new-adr step 5 sobre ADR-046 produziu 9 findings; todos absorvidos pré-commit como caminho-único após análise per ADR-026:

- ADR-046 § Origem (referências a ADR-017 antes de archive): reframado para distinguir "agora absorvido e arquivado nesta onda" — clareza de status preservando precedente histórico (F5, caminho-único).
- ADR-046 § Razões: codificado **header redirect canonical** com format de bloco-de-citação + header H1 original preservado (resolve colisão de 2 H1; plano linha 38-44 atualizado para casar) (F2, caminho-único).
- ADR-046 § Razões: codificado **archive index incremental** (`docs/decisions/archive/README.md` criado nesta Onda C com tabela inicial; ondas D-X estendem); mitigação ativa em vez de diferida para onda final (F3, caminho-único).
- ADR-046 § Razões: codificada **fronteira ADR-046 vs procedure** per ADR-024 — substância semântica vive em ADR; texto verbatim das 2 strings vive em procedure como autoridade canonical. Pattern para ondas D-X (F9, caminho-único; absorvido via opção que respeita ADR-024 mais estritamente).
- ADR-046 § Razões: reframada calibração do pattern — *"calibrado nos componentes core (archive + redirect + cross-refs em docs vivos + archive index incremental); procedure preservation é específico a clusters com docs/procedures/ pré-existente — pattern adaptável, não universal"*. Reconcilia § Razões com § Trade-offs sobre transferibilidade (F8, caminho-único).
- ADR-046 § Trade-offs: distinguido **link rot em 2 categorias** — (a) histórica (archive resolve via format codificado) vs (b) doutrinal ativa (substância absorvida em ADR-046 fecha gap; ADR-018:43 critério probe + ADR-023:53/67 herança editorial cobertos). Edição dos ~3 ADRs imutáveis citantes evitada por preservar ADR-classical (F1, caminho-único; absorvido via reconhecimento de categorias + absorção de substância normativa em ADR-046).
- ADR-046 § Trade-offs: adicionada **calibração emergente da estrutura-alvo** — cluster cutucadas standalone (não sub-cluster); sketch original era subestimativa; realista 13-15 consolidados; refinamento editorial do charter pós-merge per ADR-045 fronteira "ajuste editorial" (operador escolheu opção a — aceitar 13-15 como target realista) (caminho-único após cutucada sobre target count).
- ADR-046 § Limitações: removida linha sobre "estrutura-alvo precisará refinamento" — statement não-acionável dentro do ADR; charter atualização é responsabilidade do plano + post-merge edit per ADR-045 fronteira (F6, caminho-único).
- ADR-046 § Mitigações: reframada linha sobre doc-reviewer — agora aponta para critério explícito do plano (§ Verificação end-to-end 3-5 com grep) como insumo curado; reviewer audita conforme padrão diff-level per ADR-009 (F7, caminho-único).
- ADR-046 § Auto-aplicação: corrigida — **cond 5 primária** isolada (sucessor parcial absorvendo ADR-017+ADR-029); **cond 4 NÃO aplica** (ADR-045 já carregou categoria meta; ADR-046 é primeira instância, não categoria nova); **cond 1 NÃO aplica** (ADR-045 § Decisão parte 1 é ancestral codificado direto). Pattern explícito para ondas D-X evita inflação de cond 4 (F4, caminho-único; **load-bearing para template ondas D-X**).
- Plano § Arquivos a alterar Bloco 1: atualizado para refletir format canonical de redirect (blockquote + header preservado) + adição de archive/README.md (caminho-único).
