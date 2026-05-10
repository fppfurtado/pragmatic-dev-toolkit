# Plano — README em EN para discoverability + ADR-012

## Contexto

README do plugin pragmatic-dev-toolkit está em PT-BR, limitando discoverability para o público anglófono do Claude Code marketplace. [ADR-007](../decisions/ADR-007-idioma-artefatos-informativos.md) (idioma de artefatos informativos) explicitamente coloca README **fora do escopo** ("livre — escolha do dev/projeto, audiência diferente"). `CLAUDE.md` "Editing conventions" deste repo declara prosa de documentação como PT.

Reescrever o README em EN é **inversão parcial dessa doutrina** — categoria nova "artefatos de discoverability/landing", distinta da prosa operativa interna (PT) e dos artefatos informativos do registro de mudanças (idioma dos commits, ADR-007). `plugin.json` e `marketplace.json` descriptions **já estão EN faticamente** sem ADR formalizando — evidência empírica de que o critério "idioma segue público alvo do canal de descoberta" já opera implicitamente; ADR-012 ratifica e formaliza.

Revisão do `design-reviewer` (2026-05-10, durante `/triage`) consolidou direções aplicadas neste plano:

- ADR-012 separado do ADR-007 é caminho aceitável, mas exige cross-ref bidirecional e atualização de ADR-007 (bullet em `## Gatilhos de revisão` apontando que README saiu da lista "fora do escopo" via ADR-012). **Os dois edits são par editorial** — vão num só commit (Bloco 1).
- Critério mecânico do escopo: "artefato cuja função primária é ser indexado/lido por audiência externa **antes** de a pessoa decidir adotar o plugin". Distingue de `docs/install.md` (lido após adoção, audiência operativa).
- ADR-012 codifica a **regra** ("idioma segue público alvo do canal de descoberta"); caminho de implementação do README é tática do plano, não da ADR.

**Linha do backlog:** plugin: README em EN para discoverability no Claude Code marketplace + ADR-012 codificando inversão parcial da doutrina de idioma de docs

## Resumo da mudança

**Entra:**

1. **README.md** reescrito em EN, com seção "Philosophy" curta + link para `docs/philosophy.md` (PT, intacto). Aproveita correção de "Contribuir" desatualizado (diz "ADRs a ser adicionado se virar útil" — mas há 11 ADRs em `docs/decisions/`).
2. **ADR-012** conteúdo substantivo: regra "artefatos de discoverability/landing seguem idioma do público alvo do canal de descoberta"; escopo enumerado (README, plugin.json description, marketplace.json description, GitHub repo About, keywords/tags); fora do escopo (docs/install.md, philosophy.md, CLAUDE.md, ADRs, planos, BACKLOG); 6 alternativas consideradas (a) bilíngue lado-a-lado, (b) EN-only sem link, (c) EN+PT.md, (d) PT+description-EN-marketplace, (e) status-quo+About-EN, (f) README EN+seção-PT-topo. Caminho escolhido: **README EN com link para philosophy.md PT**, registrado em anexo "Para este repo", não na regra. Cross-ref a ADR-007 explícito.
3. **ADR-007 update** mínimo: bullet em `## Gatilhos de revisão` apontando ADR-012. **Não** editar `## Decisão` ou lista "fora do escopo" originais — preserva imutabilidade do registro; ADR-012 cobre a inversão. Editado no mesmo bloco do ADR-012 (par editorial).
4. **docs/philosophy.md** "Convenção de idioma" ganha parágrafo curto sobre terceira categoria (discoverability), cross-ref ADR-012.
5. **CLAUDE.md** "Editing conventions" enumera README como exceção EN explícita à doutrina "documentação em PT" (cross-ref ADR-012).
6. **marketplace.json** description refresh — cosmético adjacente; substituir "Personal marketplace exposing pragmatic-dev-toolkit" (lê como placeholder) por linha mais informativa ao operador externo. Não codifica doutrina.

**Fica de fora:**

- `docs/install.md` tradução para EN (audiência operativa, lê depois de adotar — fora do escopo per critério mecânico do ADR-012).
- `docs/philosophy.md` tradução completa (operativa-doutrina; ADR-012 não cobre).
- `CLAUDE.md` tradução (operating instructions, mecanismo).
- ADRs/planos/BACKLOG tradução (operativos).
- README com walkthrough visual / GIFs (separado; registrar em backlog se justificar).
- Outros itens de marketplace prep do relatório inicial (schema URL `marketplace.json` suspeita, Python 3.10+ não documentado, CI mínimo de validação, keywords mais específicas, `docs/audits/runs/` vazio tracked) — capturados em 1 linha consolidada em `## Próximos` durante este `/triage` para evitar drop entre sessões.

## Arquivos a alterar

### Bloco 1 — ADR-012 conteúdo + nota em ADR-007 {reviewer: doc}

Par editorial: novo ADR-012 mais cross-ref bidirecional em ADR-007. Único commit.

- `docs/decisions/ADR-012-idioma-artefatos-discoverability-landing.md`: substituir placeholders pelo conteúdo abaixo.
  - `## Origem`: bullet com **Investigação:** sessão `/triage` 2026-05-10 (refresh para publicação no Claude Code marketplace) + bullet com **Decisão base:** [ADR-007](ADR-007-idioma-artefatos-informativos.md) (parcialmente invertida — README sai do escopo "livre").
  - `## Contexto`: ADR-007 linha 36 explícita coloca README como "fora do escopo / livre — escolha do dev/projeto"; manifests `plugin.json`/`marketplace.json` descriptions já EN faticamente sem ADR; público Claude Code marketplace majoritariamente anglófono; lacuna doutrinária sobre artefatos cuja função primária é discoverability (lidos pré-adoção).
  - `## Decisão`: **artefatos de discoverability/landing seguem idioma do público alvo do canal de descoberta**. Critério mecânico: "artefato cuja função primária é ser indexado/lido por audiência externa **antes** de a pessoa decidir adotar o plugin". Cobertura concreta: `README.md` raiz do plugin, `plugin.json` description, `marketplace.json` descriptions (top-level e por plugin), `keywords`/`tags` em manifests, GitHub repo About/topics. **Fora do escopo:** `docs/install.md` (lido após adoção, operativa), `docs/philosophy.md` (doutrina operativa), `CLAUDE.md` (operating instructions), ADRs/planos/`BACKLOG.md` (operativos), `CHANGELOG.md`/tag annotations/PR descriptions (cobertos por ADR-007). Razões: audiência distinta (pré-adoção vs durante-uso); critério mecânico testável; ratifica status quo dos manifests.
  - `## Consequências`:
    - **Benefícios:** README do plugin alcança público anglófono do Claude Code marketplace; manifests já-EN ganham respaldo doutrinário (deixa de ser status quo silencioso); skill author futuro tem critério para enquadrar artefato novo.
    - **Trade-offs:** Operador PT que entra via README perde porta nativa em PT — mitigado por link explícito no README EN para `docs/philosophy.md` PT (caminho c da bifurcação); leitor PT bate em philosophy.md em 1 clique. Adiciona terceira categoria editorial (operativa, informativa, discoverability) — leitor de doutrina precisa internalizar a partição, custo aceitável dado ganho de discoverability.
    - **Limitações:** ADR não cobre marketplaces dual-lang nativos (cenário futuro); não cobre comunicação corporativa de release (issues, Discussions, posts); estes ficam fora do toolkit.
  - `## Alternativas consideradas`:
    - **(a) README bilíngue lado-a-lado** — descartado: leitor recebe duplo conteúdo, manutenção dupla, sem clear winner para nenhum público.
    - **(b) README EN-only sem link para philosophy.md** — descartado: público PT perde porta de entrada nativa; philosophy.md PT continua acessível mas sem sinalização.
    - **(c) README EN + README.pt-BR.md separados** — descartado: dupla manutenção sem ganho proporcional, drift quase certo entre versões.
    - **(d) Manter PT + investir em description longa em EN no marketplace** — descartado: marketplace description tem limite de caracteres; público anglófono que clica para o repo bate em PT, resolve sintoma do card mas não da landing.
    - **(e) Status quo + GitHub About em EN** — descartado: mínimo intervencionismo não resolve discoverability do leitor que abre o repo.
    - **(f) README EN + seção PT topo apontando philosophy.md** — descartado: simétrico ao caminho c-escolhido com virtude invertida (privilegia anglófono mas não esconde porta PT). Custo equivalente; preferimos link no fim ("Philosophy" section) por ser convenção mais comum em READMEs OSS.
    - **Caminho escolhido:** README EN com seção "Philosophy" curta linkando `docs/philosophy.md` PT (anexo "Para este repo" abaixo, não na regra).
  - `## Gatilhos de revisão`:
    - Marketplace passa a suportar dual-language listing nativo → reabrir para considerar i18n por canal.
    - Público alvo do canal muda predominância (ex.: PT vira majoritário no Claude Code marketplace) → critério adapta automaticamente; revisar exemplos congelados ("Para este repo").
    - Surge novo artefato no toolkit cuja audiência está na fronteira (operativa-vs-discoverability) → revisar critério mecânico.
  - **Para este repo:** README reescrito em EN com link para `docs/philosophy.md` PT; manifests `plugin.json`/`marketplace.json` descriptions seguem EN (status quo ratificado).
  - Status: `Aceito` (após preencher e revisar editorialmente).

- `docs/decisions/ADR-007-idioma-artefatos-informativos.md`: edit cirúrgico mínimo.
  - Adicionar bullet em `## Gatilhos de revisão` (linhas 74-78): "Surge artefato cuja função primária é discoverability/landing (README, manifest descriptions) → coberto por [ADR-012](ADR-012-idioma-artefatos-discoverability-landing.md); README sai da lista 'fora do escopo' desta ADR via ADR-012."
  - **Não** editar `## Decisão`, lista "Fora do escopo" original (linha 36), nem outras seções — preserva imutabilidade do registro histórico; ADR-012 cobre a inversão por referência.

### Bloco 2 — philosophy.md terceira menção {reviewer: doc}

- `docs/philosophy.md` "Convenção de idioma" (linhas 39-49): adicionar parágrafo curto após o parágrafo de "Artefatos informativos do registro de mudanças" (linha 47).
  - Conteúdo aproximado: "**Artefatos de discoverability/landing** — `README.md` do plugin e descrições em manifests de marketplace — seguem o idioma do público alvo do canal de descoberta (default canonical EN para Claude Code marketplace). Audiência distinta da operativa: leitor pré-adoção em vez de dev no projeto. Detalhes em [ADR-012](decisions/ADR-012-idioma-artefatos-discoverability-landing.md)."
  - Preservar o resto da seção intacto, especialmente o parágrafo de matching semântico de headers no `/run-plan`.

### Bloco 3 — CLAUDE.md exceção README {reviewer: doc}

- `CLAUDE.md` "Editing conventions" (parágrafo "For **this** repo specifically..."): atualizar enumerando README como exceção EN.
  - Direção: substituir "documentation and skill/agent prose are in **Portuguese**; mechanism stays in English" por "documentation and skill/agent prose are in **Portuguese**, except `README.md` (governed by [ADR-012](docs/decisions/ADR-012-idioma-artefatos-discoverability-landing.md), follows discovery channel target audience: EN); mechanism stays in English".
  - Preservar o resto do parágrafo (manifests, frontmatter keys, paths, code, `CLAUDE.md` itself).

### Bloco 4 — README.md reescrita EN {reviewer: doc}

- `README.md`: reescrita completa em EN preservando estrutura informacional do README atual.
  - **Header:** nome do plugin + tagline 1-frase EN ("Claude Code plugin codifying the flat & pragmatic dev workflow — workflow skills, YAGNI/QA/security/doc/design reviewers, self-gated hooks. Companion to scaffold-kit.").
  - **What's inside:** tabela equivalente à atual (linhas 7-23) traduzida — skills (`/triage`, `/next`, `/new-adr`, `/run-plan`, `/debug`, `/gen-tests`, `/release`), agents (`code-reviewer`, `qa-reviewer`, `security-reviewer`, `doc-reviewer`, `design-reviewer`), hooks (`block_env`, `block_gitignored`, `run_pytest_python`), template (`templates/plan.md`).
  - **Installation:** comandos `/plugin marketplace add` + `/plugin install` (preservados, são mecanismo); link para `docs/install.md` para detalhe.
  - **Philosophy:** 1-2 parágrafos EN curtos cobrindo "bounded contexts and ubiquitous language yes, tactical ceremony no; YAGNI by default; abstractions only when there's real pain". Termina com: "For the full doctrine and path contract, see [`docs/philosophy.md`](docs/philosophy.md) (Portuguese)."
  - **Companion:** scaffold-kit em EN; explicar que toolkit funciona em qualquer projeto alinhado à filosofia, não só os gerados pelo template; mencionar bloco `<!-- pragmatic-toolkit:config -->` para projetos com layout diferente, com link para `docs/install.md`.
  - **Contributing:** corrigir o defeito atual ("ADRs a ser adicionado se virar útil"). Substituir por: "Issues and PRs welcome. Structural changes to skills/agents go through ADRs in [`docs/decisions/`](docs/decisions/)."
  - **License:** "MIT — see [LICENSE](LICENSE)."
  - Preservar todos os links internos (LICENSE, philosophy.md, install.md, scaffold-kit no GitHub).

**Critério editorial de tom EN** (ancoragem para reviewer e operador): voz imperativa, ≤80 chars por bullet de tabela, sem marketing fluff, sem traduzir literal do PT. Espelhar tom de READMEs OSS curtos do nicho dev tooling (ex.: scaffold-kit README, ou READMEs de plugins Claude Code já no marketplace). `doc-reviewer` cobre drift de cross-refs/identificadores; estilo de prosa fica com o operador no commit final.

### Bloco 5 — marketplace.json description refresh {reviewer: code,doc}

JSON é estrutura + prosa. `code-reviewer` cobre integridade do JSON; `doc-reviewer` cobre drift da string. Combinação justificada como exceção (1 arquivo, 1 mudança).

- `.claude-plugin/marketplace.json`: substituir o campo `description` no nível do marketplace (linha 4).
  - Hoje: `"Personal marketplace exposing pragmatic-dev-toolkit — a Claude Code plugin for the flat & pragmatic development workflow."` (lê como placeholder).
  - Nova string: `"Curated marketplace for Fernando Furtado's Claude Code plugins — flat & pragmatic dev workflow tooling."` (já calibrada neste `/triage`; sem gate de calibração no `/run-plan`).
  - Preserve o resto do arquivo intacto. Validar JSON após edit (`python3 -m json.tool .claude-plugin/marketplace.json > /dev/null`).

## Verificação end-to-end

- `README.md` lê coerente em EN; links internos resolvendo (`LICENSE`, `docs/philosophy.md`, `docs/install.md`, `docs/decisions/`); sem bloco PT residual; "Contributing" sem placeholder desatualizado.
- `docs/decisions/ADR-012-...md`: cross-refs (ADR-007, philosophy.md) resolvendo; alternativas (a-f) listadas; escopo enumerado concretamente; status `Aceito`; "Para este repo" no rodapé.
- `docs/decisions/ADR-007-...md`: bullet novo em `## Gatilhos de revisão` apontando ADR-012; `## Decisão` e lista "Fora do escopo" originais intactos (`git diff` mostra adição apenas em `## Gatilhos de revisão`).
- `docs/philosophy.md`: parágrafo novo coerente com o resto da seção; cross-ref ADR-012 resolvendo.
- `CLAUDE.md`: exceção README explícita; cross-ref ADR-012 resolvendo.
- `.claude-plugin/marketplace.json`: `python3 -m json.tool .claude-plugin/marketplace.json > /dev/null` sai com status 0; description nova.
- `git log` mostra os 5 commits coerentes (separação por bloco preserva atomicidade).

## Verificação manual

1. **Leitura anglófona da landing.** Operador (ou simulação mental) lê o `README.md` reescrito de cima a baixo como leitor anglófono que acaba de descobrir o plugin via `/plugin marketplace`. Validar: (a) tagline comunica produto sem jargão pesado; (b) tabela "What's inside" deixa claro o escopo (workflow skills + reviewers + hooks); (c) seção "Philosophy" não trava por link a PT — leitor entende suficiente sem clicar; (d) "Companion" deixa claro que scaffold-kit não é obrigatório.
2. **Travessia bilíngue.** Clicar no link "Philosophy" do README EN e confirmar que `docs/philosophy.md` em PT abre sem fricção; nada quebrado em anchors.

## Notas operacionais

- **Ordem dos blocos importa para coerência editorial.** Sequência prescrita: (1) ADR-012 + nota em ADR-007 → (2) philosophy.md → (3) CLAUDE.md → (4) README.md → (5) marketplace.json. Doutrina antes do artefato governado pela doutrina; cross-refs criados antes dos arquivos que apontam para eles. Bloco 5 fica último por ser cosmético independente da inversão de doutrina.
- **`design-reviewer` já passou duas vezes** durante este `/triage` (sessão 2026-05-10): no draft do ADR-012 e no plano completo. Findings consolidados em `## Resumo da mudança` e nas direções dos blocos. `/run-plan` **não precisa redisparar** `design-reviewer`; `doc-reviewer` (e `code-reviewer` no Bloco 5) por bloco cobre drift de cross-refs e integridade JSON.
- **Bloco 1 (ADR-012 + ADR-007)** materializa a decisão de mudar status do ADR-012 para `Aceito`. Se o operador quiser deixar `Proposto` para revisão externa antes de aceitar, ajustar no próprio bloco — é decisão local do bloco, não do plano. Padrão do repo é heterogêneo (ADR-007/009 `Aceito`; ADR-011 `Proposto`).
- **Bloco 4 (README)** é o coração do PR do ponto de vista do leitor externo. Critério editorial de tom no próprio bloco; revisão estilística fica com o operador no commit final. `doc-reviewer` opina sobre cross-refs e identificadores, não sobre voz/tom.
