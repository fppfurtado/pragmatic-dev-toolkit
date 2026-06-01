# ADR-054: Bridge cross-project — skill `/note` + `.claude/local/NOTES.md` store (consolidado)

**Data:** 2026-05-31
**Status:** Aceito (2026-06-01)

## Origem

- **Decisão base:** [ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) § Decisão parte 1 § Implementação literal — Onda J (décima) da redesign da camada doutrinal. Oitava migração cluster temático após Ondas C+D+E+F+G+H+I (cutucadas, modo local, reviewers/curadoria, execução/run-plan, componentes plugin, convenções editoriais, alinhamento/triage).
- **Decisão base:** [ADR-052](ADR-052-codificacao-3-modos-editoriais-refinamento-consolidacao.md) — meta-pattern editorial canonical. Onda J **sem aplicação formal de modos a/b/c** — sketch literal aplicado (2 ADRs absorvidos cleanly; nenhum preservado fora do cluster por constraint mecânico ou categoria distinta).
- **Decisão base:** [ADR-046](ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) + [ADR-047](ADR-047-modo-local-paths-replicacao-cross-mode.md) + [ADR-048](ADR-048-free-read-design-reviewer-consolidado.md) + [ADR-049](ADR-049-execucao-run-plan-consolidado.md) + [ADR-050](ADR-050-componentes-plugin-consolidado.md) + [ADR-051](ADR-051-convencoes-editoriais-consolidado.md) + [ADR-053](ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) — templates do pattern de migração validado em 7 ondas precedentes (F1 link rot 2 categorias; F4 cond 5 primária isolada; F9 fronteira ADR-024 procedure file).
- **Decisão base:** [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) — critério mecânico adendo vs novo ADR. **Cond 5 primária isolada** (sucessor parcial absorvendo 2 ADRs com substância preservada integralmente); cond 4 NÃO aplica (ADR-045 carrega categoria meta; ADR-054 é oitava instância de migração); cond 1 NÃO aplica (ADR-045/-046/-047/-048/-049/-050/-051/-053 ancestrais codificados); cond 2 NÃO aplica (regra central de cada ADR absorvido preservada integralmente).
- **Decisão base:** [ADR-047](ADR-047-modo-local-paths-replicacao-cross-mode.md) § Decisão — autoridade vigente da invariante `.claude/` em `.worktreeinclude` (mecanismo "probe-and-add idempotente" absorvido de ADR-018 Addendum em Onda D). ADR-054 § Decisão (a) cross-ref para ADR-047 § Decisão como autoridade vigente da invariante (não duplica substância — segundo dispatcher universal continua codificado em ADR-047).
- **Decisões absorvidas:** ADR-032 (skill `/note` foundational + store doutrinário non-role + cross-project read fenômeno conversacional), ADR-042 (flag `--to` cross-project write + discovery `$PROJECTS_DIR` + pré-condição target inicializado + blast-radius preserved + critério contrato-vs-heurística; sucessor parcial direto de ADR-032). Substância completa preservada em § Decisão (a)+(b).
- **Plano coordenador:** `docs/plans/onda-j-migracao-cluster-bridge-cross-project.md`.

## Contexto

Dev solo opera regularmente ≥3 sessões Claude Code em paralelo com trabalho coordenado cross-project. Memory nativa do CC é **per-project** (path-encoded) e **conversational** (auto-gravada) — cobre insights internos por-projeto bem; **não cobre cross-project**. Pain real recorrente em 2 frentes:

1. **Cross-session intra-project** (2026-05-15): investigação em `/storage/3. Resources/Projects/tjpa/pje-2.1` que se estendeu para `connector-pje-mandamus-tjpa` (sessão `pje-issue-1920`) exigiu recopia manual de contexto entre sessões.

2. **Cross-project write** (2026-05-28): varredura empírica de 6 NOTES.md ativos confirmou pattern ad hoc recorrente cross-repo — dotfiles↔loadout com ≥6 entradas explicitando trabalho coordenado; drive-sync←chezmoi; meta-system↔consumers; `pragmatic-dev-toolkit/.claude/local/NOTES.md` linha 4 marcada literalmente *"Sessão CC: meta-system (cross-repo registration)"* — operador escrevendo manualmente a partir de outra sessão.

ADR-004 (state-tracking em git, archived em Onda F) moveu state vivo (in-flight) para git/forge mas preservou `## Concluídos` como registro editorial append-only. NOTES.md cai na mesma categoria preservada — não é state competitivo entre sessões paralelas, é registro de contexto cognitivo cross-session. Sem fonte em git/forge equivalente (sessões CC paralelas + cross-project não derivam de PRs/branches), o store mora em arquivo.

Pós-Onda I (alinhamento/triage; ADR-053), cluster bridge cross-project é candidato natural para oitava migração — coesão semântica alta sob narrativa única "skill `/note` foundational + extensão cross-project via flag `--to`". ADR-042 § Origem explicitamente cita ADR-032 como decisão base ("sucessor parcial estendendo § Decisão e § Limitações de ADR-032 para cobrir cross-project write"). Cluster pequeno + cleanly absorbed (sem aplicação formal de modos ADR-052).

## Decisão

Consolidar substância de ADR-032 + ADR-042 em ADR temático único sob 2 dimensões coerentes. Sem ADR preservado fora do cluster (sketch literal aplicado).

### (a) Skill `/note` foundational + store doutrinário non-role em `.claude/local/NOTES.md` (de ADR-032)

Skill geradora que faz `append <conteúdo>` timestampado em `.claude/local/NOTES.md` — store doutrinário fixo non-role, local-gitignored por design.

- **Store em `.claude/local/NOTES.md` modo local-gitignored.** Path fixo doutrinário, non-role. Por-projeto, não-versionado. Categoria nova "store doutrinário fixo non-role" ao lado de `.worktreeinclude` na tabela "The role contract" — entrada `(plugin-internal) | .claude/local/NOTES.md` discoverable para autores de skills futuras. Sem schema declarável, sem alternativa de path. Privacidade por design (canonical committed vazaria contexto privado em repos open-source).
- **Captura operador-driven via skill `/note`.** Curadoria sustentável — operador chama explicitamente quando algo é chave. Claude pode informar em prosa *"vale uma nota?"* em marcos óbvios, sem virar enum. Atende critério de recuperação seletiva (não inundação).
- **Cross-project read como fenômeno conversacional.** Skill `/note` é pura gravação; sem mecanismo de leitura ou busca. Quando operador menciona NOTES.md de outro projeto sem path absoluto, Claude propõe candidato usando contexto da conversa (cwd, projetos já acessados, menções) e operador confirma ou fornece path. Em ambiguidade verdadeira, Claude lista candidatos via prosa. Sem auto-discovery agressivo, sem skill complementar de leitura/busca.
- **Mecânica de invariante `.worktreeinclude` preservada** (cross-ref para [ADR-047](ADR-047-modo-local-paths-replicacao-cross-mode.md) § Decisão como autoridade vigente). `/note` passo 1 aplica silentemente a invariante `.claude/` em `.worktreeinclude` por probe-and-add idempotente, garantindo que worktrees do `/run-plan` enxerguem `NOTES.md` mesmo quando consumer não declarou role local (segundo dispatcher universal, ortogonal ao trigger condicional do `/init-config` step 4.5). Substância da invariante NÃO duplicada aqui — ADR-047 § Decisão é autoridade vigente (mecanismo absorvido em Onda D de ADR-018 Addendum).
- **Complementa memory nativa CC** (não substitui). Memory cobre per-project insights conversacionais auto-gravados via types `user|feedback|project|reference`. `/note` cobre cross-project registro intencional do operador em markdown corrido com timestamps. Outputs distintos, escopos distintos. Coexistem sem coordenação mecânica.
- **Skill independente de CLAUDE.md / role contract.** Frontmatter sem `roles:` per ADR-003 § Schema (ambas listas vazias autorizam omitir). Usável em qualquer git repo. Cutucada de descoberta ([ADR-046](ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md)) não aplica.

### (b) Flag `--to` cross-project write com discovery via `$PROJECTS_DIR` (de ADR-042, sucessor parcial direto de § Decisão (a))

Extensão da skill `/note` com flag opcional `--to <projeto-ou-path>` para write cross-project, preservando o comportamento default intra-projeto e a doutrina de privacy-by-design / non-role / local-gitignored.

- **`--to` opcional, sem mudança default.** Invocação sem `--to` permanece idêntica à versão foundational: append em `<repo-corrente>/.claude/local/NOTES.md`. Cross-project write é opt-in explícito. Preserva ergonomia do uso intra-projeto majoritário.
- **Discovery em 2 níveis:**
  1. `--to <nome>` (não contém `/`) → resolve via `$PROJECTS_DIR/<nome>/.claude/local/NOTES.md`. `$PROJECTS_DIR` ausente → recusa com mensagem orientando definir env var ou usar path absoluto. Target inexistente → recusa com mensagem listando projetos detectados em `$PROJECTS_DIR`.
  2. `--to <path-absoluto>` (começa com `/`) → bypass discovery, escrita direta no path. Caminho para casos fora de `$PROJECTS_DIR`.
- **Critério mecânico contrato-vs-heurística** (load-bearing para preservar a doutrina ampla sem inflar): *contrato declarado* = sinal explícito do operador para o ambiente (env var, config file declarativo no escopo do operador, registry); *heurística* = inferência sobre o filesystem sem sinal declarado (glob ad hoc, `find /storage/...`, `~/Projects/*/` hardcoded). `$PROJECTS_DIR` ausente → recusa explícita com mensagem (operador percebe o gap); inferência silenciosa rejeitada. Esse critério também estende `~/.claude/projects-registry.yml` ou similar para a categoria *contrato* caso o gatilho de revisão dispare.
- **Pré-condição de target inicializado.** Cross-write requer que o target já tenha `.claude/local/` existente E `git -C <target> check-ignore -q .claude/local/.probe` cobrindo. Faltando qualquer um → recusa com mensagem orientando inicializar via sessão CC do target. Move first-time setup para sessão do target onde o operador tem contexto para aprovar mudanças em `.gitignore`/`.worktreeinclude` do repo dele.
- **Gate `Gitignore` opera como read-only probe no target** (operacionalizado pela pré-condição de target inicializado acima — `git check-ignore -q .claude/local/.probe` cobrindo, equivalente ao probe gate); **gate `Worktree replication` NÃO roda cross-write, em modo algum** (nem probe, nem mutação). Replicação para worktrees do target é responsabilidade exclusiva da sessão local do target via `/note` ou `/run-plan` quando o operador trabalhar lá. Mutações em `.gitignore`/`.worktreeinclude` de outro repo a partir de sessão não-contextual ferem o critério de blast-radius compartilhado (paralelo doutrinal com `/run-plan §1.1`). Pré-condição de target (acima) checa `.claude/local/` existente E `git check-ignore` cobrindo — **não** estende para `.worktreeinclude` do target (assimetria deliberada: gitignore é invariante de privacidade da gravação corrente, worktree-replication é invariante de execução futura no target).
- **Mesmo formato de append.** Conteúdo gravado segue o formato canonical de § Decisão (a): timestamp UTC + corpo literal. Receptor não distingue origem mecanicamente — operador prefaceia em prosa quando relevante (pattern observado em uso real).
- **Reporta path do target no output.** Mensagem de retorno cita o path absoluto do arquivo escrito + bytes adicionados, para auditabilidade e desambiguação visual.
- **Extensão sem violar non-role e sem inflar schema.** `.claude/local/NOTES.md` continua sendo store doutrinário fixo non-role; flag `--to` é parâmetro de target da mesma operação, não papel novo no path contract. Sem schema declarável; sem entrada nova na tabela "The role contract" além da já estabelecida por § Decisão (a).
- **Coerência com read-side de § Decisão (a).** Cross-project read via Read nativo já legitimado. Adicionar write-side simétrico fecha o loop sem introduzir nova categoria conceitual: cross-project é apenas operação de target ≠ corrente, não mecanismo paralelo.

## Origem histórica

Incidentes empíricos preservados que motivaram as decisões absorvidas:

1. **2026-05-15 — Origem skill `/note` foundational (ADR-032):** sessão CC pivote de `/draft-idea` (descartado por ser feature em projeto maduro, regressão tratada por ADR-031) para `/triage` direto. Operador relatou pain real cross-project: investigação em `/storage/3. Resources/Projects/tjpa/pje-2.1` que se estendeu para `connector-pje-mandamus-tjpa` (sessão `pje-issue-1920`) — recopia manual de contexto entre sessões. Critérios de sucesso elicitados: (i) recuperação seletiva de info-chave sem reler N arquivos nem a sessão inteira; (ii) acesso cross-project referenciável (não-automático); (iii) fricção menor que ganho de re-contextualização. Substância da decisão Q1=B (store em `.claude/local/NOTES.md` modo local-gitignored) + Q2=A (captura operador-driven via skill `/note`) decidida nesta sessão.

2. **2026-05-28 — Origem flag `--to` cross-project write (ADR-042):** sessão CC — operador pediu desenho de mecanismo para "enviar informação/contexto para outros projetos quando necessário". Varredura empírica de `$PROJECTS_DIR/*/.claude/local/NOTES.md` (6 NOTES.md ativos) confirmou pain real recorrente: `dotfiles` ↔ `loadout` com ≥6 entradas explicitando trabalho coordenado cross-repo e cross-refs `file://` a ADRs do outro lado; `drive-sync` registrando "findings vindos de sessão Claude Code no repo irmão chezmoi"; `meta-system` como doctrine container cross-repo; o próprio `pragmatic-dev-toolkit/.claude/local/NOTES.md` linha 4 marcada literalmente *"Sessão CC: meta-system (cross-repo registration)"* — operador escrevendo manualmente a partir de outra sessão. ADR-035 critério 1 (incidente recorrente documentado) e critério 4 (pattern ad hoc emergente ≥3x) ambos disparados (à época; ADR-035 hoje Substituído por ADR-043 § Ockham operacionalizado em decisões internas do plugin — critérios homólogos preservados como critério 1 "incidente recorrente ou padrão observado em uso real" e critério 4 "codificação de pattern emergente ad hoc ≥3 vezes").

3. **2026-05-27 — Origem invariante `.worktreeinclude` em `/note`** (ADR-018 Addendum, absorvido em ADR-047 § Decisão durante Onda D): `/note` passo 1 aplica silentemente probe-and-add idempotente do `.claude/` em `.worktreeinclude`. Mecanismo herdado de ADR-018 § Decisão (também sucessor parcial de ADR-005); preserved vigente em ADR-047 § Decisão como autoridade. ADR-054 § Decisão (a) cross-ref para ADR-047 (não duplica substância).

## Consequências

### Benefícios

- **Cross-session e cross-project resolvidos para dev-solo workflow.** Caso real `pje-issue-1920` deixa de exigir recopia manual; pattern dotfiles↔loadout↔drive-sync↔meta-system tem caminho mecânico para send-side.
- **Curadoria sustentável.** Store não inunda porque captura é explícita. Operador controla o que entra.
- **Estende doutrina existente sem inflar schema do path contract.** Categoria nova (non-role doutrinário) ao lado de `.worktreeinclude`, sem promover `notes` a role.
- **Entrada `(plugin-internal) | .claude/local/NOTES.md`** na tabela "The role contract" é discoverable para autores de skills futuras que considerem outros stores não-role.
- **Skill usável em qualquer git repo**, sem dependência de `CLAUDE.md` ou bloco config. Adoção zero-overhead.
- **Caminho mecânico para o pattern empírico recorrente cross-repo coordination.** Operador na sessão A registra para B sem context-switch.
- **Discovery por nome via `$PROJECTS_DIR` é ergonômica** (`/note --to loadout "fix x"` vs typar path absoluto), barata e não-heurística — contrato explícito do ambiente.
- **Pré-condição de target inicializado preserva blast-radius doctrine** (operador aprova mudança no contexto do repo) sem replicar mecânica cross-contextual.
- **Compatibilidade total com read-side** (Read nativo em NOTES.md de outros projetos) — sem mudança em fluxo de consumo cross-project existente.
- **Zero impacto em consumers sem `$PROJECTS_DIR` ou que não usam `--to`:** comportamento default preservado.

### Trade-offs

- **Cross-project requer referência explícita validada pelo operador** (read-side). Fluxo conversacional pode ser mais longo em projetos com nomes ambíguos. Trade-off aceito por preservar simplicidade da skill (sem path discovery).
- **Discovery acoplada a `$PROJECTS_DIR`** (write-side). Sem env var, só path absoluto funciona. Aceitável — operadores sem `$PROJECTS_DIR` usam o fallback explícito; documentação aponta o contrato.
- **First-time cross-write em target não inicializado falha hard.** Operador precisa abrir sessão CC no target uma vez para inicializar. Aceitável — torna explícita a fronteira de blast-radius e evita gates cross-contextuais.
- **Sem registro de origem mecânico.** NOTES.md do target não marca "veio de --to a partir de <sessão>"; convenção de prosa-prefácio fica com o operador. Coerente com o padrão observado em uso real; reabertura legítima se atrito surgir.
- **Sem broadcast (`--to a,b,c`).** Cross-write é 1-to-1 por invocação. Multi-target ad hoc reabre em uso real se ≥3 casos surgirem; YAGNI hoje.

### Limitações

- **Per-project store sem index global.** Não há mecanismo para listar todos os NOTES.md em todos os projetos do operador. Reabertura legítima se atrito real surgir.
- **YAGNI deliberado sobre leitura, busca e sincronização.** Skill é pura gravação. Operador lê via Read nativo, busca via grep do CC, e não há sincronização entre NOTES.md de projetos relacionados. Drift entre projetos é responsabilidade editorial do operador.
- **Hook auto-captura descartado.** Operadores que prefiram captura automática (sem skill explícita) ficam sem caminho — preferência por curadoria prevalece. Reabertura se grupos de uso real demandarem.

## Alternativas consideradas

### (a) Manter ADR-032 + ADR-042 fragmentados (status quo pré-Onda J)

Descartada. ADR-042 § Origem explicitamente cita ADR-032 como decisão base; coesão semântica alta (extensão direta de cross-project write sobre /note foundational). Manter fragmentado força leitor a percorrer 2 ADRs para entender o ecosistema bridge. Consolidação é exatamente o movimento que ADR-045 § Decisão parte 1 materializa.

### (b) Cross-project em `~/.claude/notes/` (Q1 alternativa A de ADR-032 original)

Descartada via cutucada Q1 do `/triage` 2026-05-15 (preserved). Cross-project natural (atravessa projetos sem referência), mas: (i) cria infra paralela à memory nativa CC sem reuso doutrinário; (ii) viola "extensão do plugin" (operador exigiu como restrição) ao introduzir convenção fora do repo; (iii) ganho automático cross-project não é exigência — referência explícita aceita.

### (c) NOTES.md committed no repo (Q1 alternativa C de ADR-032 original)

Descartada (preserved). Versionado expõe contexto privado (anotações de dev, info sensível) ao publicar. Risco real em repo open-source. Privacidade por design exige local-gitignored.

### (d) Claude propõe cutucada de captura mid-conversa (Q2 alternativa B de ADR-032 original)

Descartada (preserved). Menos fricção que `/note` explícito, mas ruído potencial alto: Claude propõe em momento errado, atrapalha fluxo. Plus depende de Claude detectar bem "info-chave" — incerto. Curadoria via skill explícita é mais previsível.

### (e) Hook lifecycle Stop com auto-captura (Q2 alternativa C de ADR-032 original)

Descartada (preserved). Zero fricção, zero curadoria — sumariza sessão inteira sem filtrar. Inunda o store com lixo. Operador perde sinal no ruído. Contradiz critério de recuperação seletiva.

### (f) Promover `notes` a role no path contract (F2 alternativa b de ADR-032 original)

Descartada (preserved). Schema novo seria cerimônia para um caso singular doutrinário sem alternativa de path. Não há valor canonical possível (committed vaza), não há configuração que o operador faria. Extensão de categoria non-role (escolhida em § Decisão (a)) preserva o caráter doutrinário sem inflar schema.

### (g) Skill nova `/send-note <target> "<msg>"` (C de ADR-042 original)

Descartada (preserved). Mesma mecânica de § Decisão (b) trocando apenas o target — duplicaria mecânica por modo de uso. Pattern observado é `/note` com 1 ponto de variação (target = corrente vs `--to`), mais coeso como flag opcional que como skill nova. Paralelo conceitual com [ADR-050](ADR-050-componentes-plugin-consolidado.md) § Decisão (a): skills detectam stack do consumer por marker em vez de skills separadas por stack — variação de runtime via parâmetro, não por verbo.

### (h) Inbox pattern (`.claude/local/INBOX.md` segregado) (D de ADR-042 original)

Descartada com base em evidência empírica direta (preserved). Varredura de NOTES.md cross-source mostrou operador merge tudo no mesmo arquivo, prefaceiando em prosa a origem — não segrega por arquivo. Inbox separado introduziria store novo, leitor novo, e gate novo, sem ganho que o uso real demande.

### (i) Discovery via path discovery agressiva (`find /storage/`, glob de `~/Projects/`) (F de ADR-042 original)

Descartada (preserved). Heurística filesystem-wide é frágil e específica de ambiente. `$PROJECTS_DIR` (escolhida em § Decisão (b)) é contrato declarado, não heurística — distinção load-bearing codificada no critério mecânico contrato-vs-heurística.

## Gatilhos de revisão

- **Broadcast multi-target demandado em ≥3 cenários reais** (`--to a,b,c`) → reabrir alternativa.
- **Registro de origem mecânico demandado** para auditabilidade (operador frequentemente perdendo trilha de "de onde veio essa nota") → campo opcional no header do timestamp.
- **Target em path fora de `$PROJECTS_DIR` virar majoritário** (operador adiciona N projetos em locations diversas) → considerar discovery via registry declarado em `~/.claude/projects-registry.yml` ou similar.
- **First-time cross-write recusado em ≥3 sessões distintas dentro de 1 mês** → considerar relaxar pré-condição com modo `--init-target` explícito.
- **Operadores demandam captura automática** (hook lifecycle Stop ou similar) em grupos de uso real → reabrir Hook auto-captura.
- **Operadores demandam skill de leitura/busca** (`/notes-find` agregando paths conhecidos) → reabrir YAGNI de leitura.
- **Drift entre NOTES.md de projetos relacionados** vira pain real demandando sincronização → reabrir YAGNI de sincronização.

## Auto-aplicação

**ADR-034 critério mecânico (adendo vs novo ADR — 5 condições para novo; 4 para adendo):**

- **Cond 5 (sucessor parcial — estende, refina ou condiciona ADR Aceito sem revogar):** **APLICA** — primária isolada. ADR-054 absorve substância de ADR-032 + ADR-042 (2 ADRs Aceito vigentes) preservando regra central de cada um integralmente. Nenhum marcado como `Substituído` — categoria editorial "absorção consolidatória" (per F4 lesson Onda D refinada) vs "revogação". Pattern editorial 8ª aplicação consecutiva (Ondas C+D+E+F+G+H+I+J) consolidando integridade da regra mecânica.

- **Cond 4 (codificação de pattern emergente — N≥3 incidentes recorrentes):** **NÃO APLICA** — ADR-045 carrega categoria meta "consolidação editorial sob redesign" desde Onda A; ADR-054 é oitava instância de migração temática (após ADR-046+047+048+049+050+051+053), não categoria nova. Aplicar cond 4 inflaria critério em cada onda diluindo ADR-034.

- **Cond 1 (decisão estrutural sem ancestral codificado):** **NÃO APLICA** — ADR-045 § Decisão parte 1 (consolidação 45 → ~13-15 ADRs sob hierarquia invertida) + ADR-046+047+048+049+050+051+053 (templates do pattern de migração) + ADR-052 (meta-pattern editorial canonical) são ancestrais codificados diretos.

- **Cond 2 (substitui ADR ancestral revogando doutrina central):** **NÃO APLICA** — regra central de cada ADR absorvido preservada integralmente em § Decisão (a)+(b). Ondas C-I reaplicaram literal a distinção "absorção consolidatória vs revogação" (per F4 lesson Onda D).

- **Cond 3 (codificação de restrição externa de longa duração):** **NÃO APLICA** — esta é decisão interna do plugin sobre composição editorial da camada doutrinal.

**ADR-052 critério mecânico de modos editoriais (3 modos canonical):**

- **Modo (a) EXCLUSÃO:** **NÃO APLICA** — ambos ADRs (032 + 042) do sketch original do cluster absorvidos cleanly; nenhum excluído por desalinhamento semântico ou categoria distinta.
- **Modo (b) INCLUSÃO:** **NÃO APLICA** — nenhum ADR foi incluído ao cluster além do sketch original.
- **Modo (c) PRESERVAÇÃO POR CONSTRAINT MECÂNICO PURO:** **NÃO APLICA** — nenhum ADR preservado fora do cluster por hardcode em § Decisão de outro ADR Aceito vigente.

**Onda J é a primeira pós-codificação de ADR-052 onde sketch literal foi aplicado sem refinamento editorial** (sem exclusão/inclusão/preservação). Pattern editorial mais limpo possível — 2 ADRs absorvidos cleanly. Sinal de saúde: ADR-052 modos a/b/c continuam como contingência editorial vs invariante operacional.

**Status:** Proposto (default per template). Promoção a Aceito após design-reviewer auto-fire (5 do plano `/triage` step 5) sem findings absorvíveis que mudem substância central.
