# ADR-046: Cutucada uniforme em skills para descoberta de gaps de configuração

**Data:** 2026-05-30
**Status:** Aceito

## Origem

- **Decisão base:** [ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) (apex da redesign — § Decisão parte 1 § Implementação literal: *"Ondas C-X — migração de ADRs por cluster temático. Cada onda absorve 3-6 ADRs antigos em 1 consolidado..."*). Este ADR é a primeira instância concreta dessa migração (Onda C) consolidando o cluster cutucadas.
- **ADRs absorvidos:** ADR-017 (foundational do cluster — agora absorvido e arquivado nesta onda em `docs/decisions/archive/`) + ADR-029 (sucessor parcial estendendo cobertura — agora absorvido e arquivado nesta onda). Cluster index Addendum em ADR-017 (Onda 3 da reforma doutrinária, PR #86) — proof-of-concept de consolidação editorial agora preservado no archive como registro histórico que cumpriu sua função.
- **Investigação:** Onda C codificada em `docs/plans/onda-c-migracao-cluster-cutucadas.md`. Cluster cutucadas escolhido como primeira migração (calibração do pattern) por: (1) cluster Addendum já existente em ADR-017; (2) scope pequeno (2 ADRs + 1 procedure file); (3) coeso semanticamente (ADR-029 só estende cobertura de ADR-017); (4) procedure file separation per [ADR-024](ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md) já estabelecida.

## Contexto

A camada doutrinal pós-v2.14.0 inclui 2 ADRs codificando a cutucada uniforme em skills para descoberta de gaps de configuração: ADR-017 estabeleceu cutucada com gating bi-state (CLAUDE.md presente + marker ausente / outros = silêncio); ADR-029 estendeu para gating tri-state (caso A presente sem marker / caso B ausente / caso C silêncio) com strings canonical próprias por caso. Mecânica de execução (algoritmo numerado prescritivo + strings literais + dedup conversation-scoped) extraída em 2026-05-20 para `docs/procedures/cutucada-descoberta.md` per ADR-024.

Sob a redesign da camada doutrinal codificada em ADR-045, o cluster cutucadas é candidato natural para consolidação:

- **Decisão central estável** — cutucada uniforme com gating multi-state + strings canonical + herança editorial não tem revisão pendente da regra.
- **ADR-029 evoluiu ADR-017 sem revogar** — adicionou string-B + escopo expandido (4 → 5 skills) + gating tri-state. Não há tensão entre os dois ADRs.
- **Procedure file separation já materializa fronteira doutrina-vs-mecânica** (per ADR-024); a categoria de procedure é preservada na consolidação.
- **Cluster index Addendum em ADR-017** (Onda 3 da reforma) demonstrou que leitura única do thread completo é mais ergonômica que navegação cross-ADR — precedente operacional absorvido por esta consolidação.

Esta consolidação valida o pattern de migração para ondas D-X subsequentes (clusters maiores: modo local, design-reviewer ecosystem, convenções editoriais, etc.).

## Decisão

**Consolidar a doutrina sobre cutucada uniforme em skills para descoberta de gaps de configuração em ADR único (este ADR-046), absorvendo substância de ADR-017 (foundational) e ADR-029 (sucessor parcial estendendo cobertura) sob narrativa única. Procedure file `docs/procedures/cutucada-descoberta.md` permanece como executor canonical da mecânica, intacto per ADR-024.**

### Escopo e mecanismo unificado

**5 skills emitem cutucada uniforme** ao final do relatório quando satisfazem **gating tri-state** sobre estado do `CLAUDE.md`:

| Caso | Detecção | Ação |
|---|---|---|
| **A** — `CLAUDE.md` presente sem o bloco `<!-- pragmatic-toolkit:config -->` | grep do arquivo via probe próprio da skill | Emitir **string-A**: *"Dica: este projeto não declara o bloco `pragmatic-toolkit:config` no CLAUDE.md. Rode `/init-config` para configurar todos os papéis de uma vez."* |
| **B** — `CLAUDE.md` ausente no consumer | probe de existência do arquivo | Emitir **string-B**: *"Dica: este projeto não tem `CLAUDE.md`. Crie o arquivo e rode `/init-config` para configurar os papéis do plugin."* |
| **C** — `CLAUDE.md` presente com o marker | qualquer outra condição | Silêncio |

**5 skills emissoras** (todas com `roles.required` no frontmatter, atingindo o passo 3 do Resolution protocol):
`/triage`, `/new-adr`, `/run-plan`, `/next`, `/draft-idea`.

**Dedup conversation-scoped por string** per [ADR-010](ADR-010-instrumentacao-progresso-skills-multi-passo.md): cada string observa o histórico visível da conversa CC corrente independentemente. Match → suprime; sem match → emite. Transição A↔B na mesma sessão (raro mas possível: operador cria `CLAUDE.md` mid-session) permite emissão da segunda string mesmo após a primeira ter aparecido — gaps semanticamente distintos.

**Mecânica de execução em `docs/procedures/cutucada-descoberta.md`** (categoria `docs/procedures/` per ADR-024): algoritmo numerado prescritivo com `Bash` literal mapeando stdout `NO_FILE` / `NO_MARKER` / `MARKER` para próxima ação; 2 strings canonical literais; dedup conversation-scoped por string. Refactor 2026-05-20 (commit `a6a25a0`) estabeleceu a forma prescritiva. **Procedure preservado intacto** nesta consolidação — apenas cross-refs atualizadas para apontar a ADR-046.

### Herança editorial

Skill nova com `roles.required` adota a convenção **manualmente** seguindo `CLAUDE.md` → "Cutucada de descoberta" como template. Herança é editorial, não mecânica — autor de skill nova adiciona a linha de cutucada referenciando o procedure no final do step de reporte; checklist para autor + `code-reviewer` na PR.

Sem garantia mecânica — sustentado por disciplina editorial. Skill nova que esqueça falha silenciosamente; mitigação via § "Cutucada de descoberta" do CLAUDE.md servindo de checklist + reabertura YAGNI para 6ª skill (gatilho herdado).

### Razões

- **Doutrina consolidada com clareza editorial.** Reader único navega thread completo (gating tri-state + 2 strings + dedup + herança) em ADR único; não precisa saltar ADR-017 → ADR-029 nem inferir relação por leitura cruzada.
- **Procedure preservado intacto.** ADR-024 estabeleceu fronteira doutrina vs mecânica; nada na consolidação requer absorver o procedure — substância dele (algoritmo prescritivo + strings literais + dedup) é executora, não doutrinária.
- **Fronteira ADR-046 vs procedure (per ADR-024) codificada.** ADR-046 carrega substância semântica (gating tri-state como conceito + escopo das 5 skills + herança editorial + critério "falso-positivo é mais barato que falso-negativo em probes do plugin" herdado de ADR-017 como princípio de probe). Procedure file `docs/procedures/cutucada-descoberta.md` carrega autoridade canonical de **texto verbatim** das 2 strings literais + algoritmo numerado prescritivo + Bash literal mapeando stdout. Regressão silenciosa no procedure detectável por inspecionar fronteira: substantive substance vive aqui, executable literals vivem lá. Pattern explícito para ondas D-X.
- **Trilha empírica preservada.** § Origem histórica deste ADR lista incidentes empíricos das 2 decisões absorvidas; conteúdo original archivado em `docs/decisions/archive/` para registro auditável.
- **Pattern de migração calibrado nos componentes core** (archive + redirect header com format codificado + cross-refs em docs vivos + archive index incremental). Procedure preservation é específico a clusters que tenham `docs/procedures/` pré-existente — pattern adaptável, não universal. Pode requerer ajuste em clusters maiores sem essa separação prévia (modo local 005+018+025+030; design-reviewer ecosystem 009+011+026+038).
- **Sem perda de carga doutrinal.** Anti-regression checklist do charter § Discoverability lista: gating tri-state, 2 strings canonical literais, dedup conversation-scoped, herança editorial — todos preservados em ADR-046 (gating + dedup + herança como substância semântica) + procedure intacto (strings literais + algoritmo).

### Header redirect canonical (format codificado para ondas C-X)

Arquivos arquivados sob `docs/decisions/archive/` adotam **format de citação + header H1 original preservado**:

```markdown
> **ARCHIVED <YYYY-MM-DD>** — content absorbed into [ADR-MMM](../ADR-MMM-<slug>.md); see that ADR for current authority. Body below preserved verbatim for historical record.

# ADR-NNN: <título original>

<body original integral...>
```

Razões do format:
- Bloco de citação para aviso (não-header) preserva o `# ADR-NNN` original como H1 — parsing humano e ferramental limpo (sem 2 H1 colidindo).
- Reader que cai no arquivo arquivado vê redirect proeminente + corpo completo abaixo para leitura histórica.
- Arquivamento (não deleção) materializa Verdade: git preserva história, archive preserva navegabilidade direta.

### Archive index incremental

`docs/decisions/archive/README.md` criado nesta Onda C com tabela inicial de mapeamento velho → novo. Cada onda D-X subsequente adiciona suas linhas no commit da onda — crescimento incremental em vez de big-bang na onda final. Mitiga link rot ativo desde já, não diferindo.

Format inicial (criado nesta onda):

```markdown
# Archived ADRs

Mapping of archived ADRs → current authority (post-redesign per [ADR-045](../ADR-045-...md)).

| Archived ADR | Absorbed into | Onda |
|---|---|---|
| ADR-017 — Cutucada uniforme em skills para descoberta de configuração ausente | [ADR-046](../ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) | C |
| ADR-029 — Cutucada de descoberta cobre `CLAUDE.md` ausente | [ADR-046](../ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) | C |
```

Onda D-X estende a tabela como invariante do plano (mesma onda do archive); responsabilidade do plano per ADR-046 § Razões "fronteira procedure vs ADR" pattern.

## Origem histórica

Incidentes empíricos das 2 decisões absorvidas preservados como contexto para reabertura informada:

### Atrito PJe 2026-05-11 (origem de ADR-017)

`/triage` 2026-05-11 do item "wizard de configuração inicial dos papéis" surfou atrito de onboarding do plugin no projeto Java PJe:

- Operador novo não sabia da existência do bloco `<!-- pragmatic-toolkit:config -->`.
- Memorização one-shot per role do Resolution protocol é reativa — exige rodar 4-6 skills primeiro (cada uma perguntando 1 role).
- Resultado: ~30 min de fricção antes de qualquer skill rodar + composição manual do YAML pelo operador.

ADR-017 estabeleceu cutucada como sinalização proativa de `/init-config` para fechar esse gap de descoberta.

### Gap de projeto novo sem CLAUDE.md 2026-05-14 (origem de ADR-029)

Sessão de `/debug` 2026-05-14 surfou gap percebido em projeto novo: operador instala plugin, invoca skill com `roles.required` em projeto sem `CLAUDE.md`, e **não recebe sinalização** do `/init-config` — gating de ADR-017 tinha condição "CLAUDE.md existe" e ausência falhava o gate.

ADR-029 inverteu parcialmente a alternativa (f) descartada em ADR-017 (cutucada cobre CLAUDE.md ausente), estendendo o gating para 3 saídas com string-B dedicada ao caso ausente. Postura editorial não-reparativa preservada — cutucada é textual, não cria arquivos.

### Refactor do procedure 2026-05-20 (commit `a6a25a0`)

Procedure file `docs/procedures/cutucada-descoberta.md` (extraído das 5 SKILLs em 2026-05-16 per ADR-024, commit `d6a20dd`, PR #71) recebeu refactor 2026-05-20: tabela declarativa de gating → algoritmo numerado prescritivo com `Bash` literal mapeando stdout. Bug evidenciado em sessão `remove-n8n` do consumer `h3-finance-agent` (4 emissões de string-A com marker presente em CLAUDE.md, zero greps no log da sessão) preservado como exemplo dentro do próprio procedure.

## Consequências

### Benefícios

- Reader navega thread completo da cutucada em 1 ADR + 1 procedure (era 2 ADRs + 1 procedure com cluster Addendum sustentando o thread).
- Pattern de migração validado para ondas D-X subsequentes.
- Procedure file separation reafirmada — fronteira doutrina vs mecânica preservada per ADR-024.
- Trilha empírica preservada via archive + § Origem histórica.

### Trade-offs

- **Link rot em ADRs imutáveis tem 2 categorias distintas.** Auditoria revelou:
  - **Categoria (a) — referências históricas/precedente** (ADR-027:27 *"paralelo à cutucada de ADR-017"*; ADR-041:10 *"paralelos ADR-029→ADR-017"*; ADR-034/-038/-043/-044 menções de trajetória): reader segue link buscando trajetória. **Archive resolve** — `docs/decisions/archive/<slug>.md` carrega corpo histórico completo per format codificado acima. Archive index incremental facilita descoberta.
  - **Categoria (b) — referências de substância doutrinal ativa** (ADR-018:43 cita ADR-017 como autoridade do critério *"falso-positivo é mais barato que falso-negativo"* em probes; ADR-023:53/67 cita ADR-017 § Editorial inheritance como autoridade para herança editorial de skills): reader segue link buscando **regra vigente**, não trajetória. Para esses, ADR-046 absorve substância: critério probe philosophy citado em § Razões linha "Fronteira ADR-046 vs procedure (per ADR-024) codificada"; herança editorial codificada em § Herança editorial. Reader que cai em archive/ADR-017 vê redirect canonical apontando para ADR-046 onde substância vive — gap fechado.
  - **Edição dos ~3 ADRs imutáveis citantes evitada** por preservar ADR-classical convention; substância absorvida em ADR-046 é a mitigação real. Pattern para ondas D-X: identificar antes de archive **quais cross-refs em ADRs imutáveis são categoria-b** e absorver substância correspondente no consolidado.
- **Custo do refactor de cross-refs em docs vivos.** 5 docs ativos (CLAUDE.md + procedure + 3 SKILLs) atualizados em blocos separados; reviewer audita cada bloco. Volume manejável.
- **Procedure preservation é pattern específico, não universal.** Cluster cutucadas tem procedure pré-existente per ADR-024. Outros clusters podem não ter (modo local 005+018+025+030 sem procedure; design-reviewer ecosystem 009+011+026+038 sem procedure); design-reviewer audita por cluster se procedure absorption ou preservation aplica.
- **Calibração emergente da estrutura-alvo.** Cluster cutucadas saiu como **standalone** (esta onda) em vez de sub-cluster de "ADR-004-skill-alinhamento-triage" como sketch original do charter. Sinal de que sketch de 11 ADRs era subestimativa; calibração realista emergente nas ondas é 13-15 consolidados (sketch + cutucadas standalone + clusters sem casa explícita + possíveis splits adicionais). Refinamento editorial do charter pós-merge per ADR-045 § Decisão parte 1 fronteira *"ajuste editorial do charter vs revisão de ADR-045"* (categoria editorial sem mudança estrutural na regra de consolidação). Pattern para ondas D-X: cada onda contribui para refinamento incremental do sketch; charter é artefato vivo.

### Limitações

- Dedup conversation-scoped sob context compression — herda limitação de ADR-017 § Trade-offs (cada string pode reaparecer se cair fora da janela visível).
- Cutucada não diferencia `CLAUDE.md` gitignored — herda limitação de ADR-029 § Limitações (probe textual dispara string-A em arquivo gitignored sem marker; `/init-config` resolve o caso via mecanismo de [ADR-030](ADR-030-aceitar-claude-md-gitignored-via-worktreeinclude.md)).

### Mitigações

- **Anti-regression checklist do charter** § Discoverability lista os 4 elementos load-bearing (gating tri-state, 2 strings, dedup, herança editorial) — design-reviewer audita preservação em cada onda subsequente.
- **Plano § Verificação end-to-end critérios 3-5** prescrevem grep explícito de ADR-017/-029 em paths concretos como invariante de sucesso da onda; `doc-reviewer` audita o diff conforme insumo curado pelo plano (per ADR-009 padrão diff-level). Pattern para ondas D-X: critério de cross-ref propagation vive no plano, não na mecânica de reviewer.
- **Archive index incremental criado nesta Onda C** (`docs/decisions/archive/README.md` per § Razões acima) — link rot mitigation **ativa** desde já, atualizada per onda subsequente. Pattern: cada onda D-X estende a tabela como invariante do plano.

## Alternativas consideradas

### (a) Manter ADR-017 e ADR-029 com cluster Addendum (status quo Onda 3)

Continuar com estrutura atual: ADR-017 foundational + ADR-029 sucessor parcial + cluster Addendum em ADR-017 + procedure intacto.

Descartada per ADR-045 § Decisão parte 1: cluster Addenda foram **prova de conceito** de consolidação editorial; a redesign generaliza esse movimento para **archive + consolidado único**. Manter status quo perde benefício de leitura única do thread + mantém 2 ADRs onde 1 cabe sob a nova estrutura.

### (b) Edit in-place em ADR-017 absorvendo ADR-029

Reescrever ADR-017 incorporando substância de ADR-029, mantendo ADR-017 como ADR vigente; ADR-029 marcado `Substituído`.

Descartada:

- Viola convenção ADR-classical (ADRs são registros imutáveis; supersedeção via novo ADR).
- Apaga trajetória editorial (ADR-029 documentou inversão parcial de alternativa (f) descartada em ADR-017 com rationale específica; reescrever ADR-017 apaga essa narrativa).
- ADR-045 explicitamente prescreve archive + novo ADR consolidado, não edição in-place.

### (c) Procedure absorbe a doutrina (eliminar ambos os ADRs sem criar ADR-046)

Mover substância doutrinária dos ADRs para o próprio procedure file; manter apenas procedure como autoridade.

Descartada:

- Viola ADR-024 (categoria `docs/procedures/` é executora de mecânica, não codificadora de decisão).
- Procedure file é prescritivo (algoritmo + strings literais); decisão de gating tri-state + escopo das 5 skills + herança editorial é doutrinária (carrega rationale, alternativas, gatilhos de revisão).
- Misturar doutrina e mecânica reabriria a tensão que ADR-024 resolveu.

### (d) Absorver procedure também (ADR-046 contém algoritmo + strings literais)

Mover conteúdo do procedure para dentro de ADR-046; eliminar `docs/procedures/cutucada-descoberta.md`.

Descartada:

- ADR cresce excessivamente (procedure é prescritivo com algoritmo numerado; ADR fica difícil de navegar).
- Fronteira doutrina vs mecânica codificada em ADR-024 perde-se; precedente errado para clusters D-X.
- Procedure tem seu próprio refactor history (commits `d6a20dd`, `a6a25a0`); preservar como arquivo separado mantém git log focado.

### (e) Manter ambos ADR-017 e ADR-029 ativos, criar ADR-046 apenas como índice

ADR-046 minimalista apontando para os 2 ADRs originais; nada movido para archive.

Descartada:

- Não materializa a redesign — ADR-045 prescreve absorção de conteúdo + archive de antigos, não indexação cosmética.
- Charter sketch explicita "novo ADR consolidado" como output das ondas C-X, não "ADR-index".
- Cluster Addendum em ADR-017 já cumpria função de índice; ADR-046 como índice seria redundante.

## Gatilhos de revisão

Triggers das 2 decisões absorvidas consolidados + triggers específicos da consolidação:

### Herdados de ADR-017 (cutucada em geral)

- **≥2 operadores reportarem ruído** mesmo com dedup conversation-scoped — sinal de que cutucada precisa de mais dedup (per repo, per dia, per N invocações).
- **Operador reporta cutucada esperada não aparecendo em skill nova** que declara `roles.required` — herança editorial falhou; reabrir para considerar herança mecânica.
- **Operador reporta que `/init-config` não cobre o caso dele** mas cutucada continua sugerindo — gap entre o que cutucada promete e skill entrega; atualizar redação ou condicionar mais.
- **Mudança na convenção do marker** (alias, variantes, renomeação) — re-confirmar que probes nas 5 skills foram atualizados; re-avaliar helper compartilhado.
- **Re-emissão por context compression virar ruído frequente** (≥3 reports de "vi a mesma cutucada várias vezes na mesma sessão") — considerar Task per ADR-010 (registro estruturado que sobreviva à compression).

### Herdados de ADR-029 (cobertura CLAUDE.md ausente)

- **Operador reporta confusão entre string-A e string-B** — drift de leitura, redação ambígua, ou ordem editorial nas SKILLs piora a interpretação. Reabrir para unificar.
- **Mudança em `/init-config` step 1 sobre criação automática de CLAUDE.md** — se toolkit passar a criar CLAUDE.md em algum cenário, string-B precisa reconsiderar redação.
- **Operador em consumer real ignora string-B em 3+ sessões consecutivas** sem rodar `/init-config` — sinal de que redação ou sinal não estão funcionando; reabrir para iterar.

### Específicos desta consolidação

- **6ª skill com `roles.required` aparecer** (atual: 5 × 2 strings = 10 sites) — herdar gatilho de ADR-029 § Gatilhos linha 110; reabrir alternativa (g) de ADR-017 (helper compartilhado) ou herança mecânica quando universo dobrar para 12+ sites.
- **Link rot em ADRs imutáveis gerar ≥3 reports de confusão** — sinal de que archive sem stub no path original é caro para reader; reabrir para considerar redirect file no path antigo OR symlink OR edit de cross-refs em ADRs antigos (violaria ADR-classical mas pode ser trade-off).
- **Pattern de migração falhar em cluster D-X** — se design-reviewer flagrar gap material no pattern (procedure preservation, redirect format, propagação de cross-refs), reabrir este ADR como template; pode requerer revisão de ADR-045 § Decisão parte 1.

## Auto-aplicação coerente per ADR-034

- **Cond 5 (sucessor parcial):** aplica primário — consolidado absorve substância de ADR-017 + ADR-029 sob narrativa única. ADR-017 e ADR-029 vão para archive com header redirect a este ADR. **Suficiente per ADR-034** *"novo ADR quando ≥1 das 5 condições aplica"*; cond 5 isolado justifica criação deste ADR.
- **Cond 4 (categoria nova):** **NÃO aplica** — ADR-045 § Decisão parte 1 § Implementação **já codificou a categoria** "consolidação editorial cross-ADR de cluster temático como decisão estrutural" no nível meta-pattern; ADR-046 é **primeira instância concreta** dessa categoria já estabelecida, não introduz categoria conceitual nova de artefato. Paralelo com ADR-043 § Auto-aplicação (que NÃO-aplicou cond 4 por formalizar relação estrutural entre princípios já existentes). Aplicar cond 4 aqui inflaria o critério em cada onda D-X ("primeira/N-ésima instância como categoria nova" auto-justificativa), diluindo a precisão de ADR-034.
- **Cond 1 (decisão estrutural sem ancestral direto):** **NÃO aplica** — ADR-045 § Decisão parte 1 § Implementação **é ancestral codificado direto** do pattern que ADR-046 instancia. Onda 3 cluster index Addendum em ADR-017 é precedente operacional pontual, mas ADR-045 elevou o pattern a decisão estrutural codificada — ADR-046 herda essa ancestralidade.
- **Cond 2 (substitui ADR ancestral):** NÃO aplica — não há ADR cuja decisão central seja substituída pela deste; ambos os absorvidos (ADR-017 e ADR-029) têm decisões centrais **preservadas** como instâncias do gating multi-state codificado aqui.
- **Cond 3 (codifica restrição externa):** NÃO aplica — decisão interna ao processo doutrinal do plugin.

Pattern editorial para ondas D-X: cada migração cluster aplica **cond 5 primária + outras condições conforme ancestralidade real**, não cond 4 inflada nem cond 1 espúria. ADR-045 § Decisão parte 1 é ancestral codificado direto de cada migração; ondas instanciam, não criam categoria.
