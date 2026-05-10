# ADR-012: Idioma de artefatos de discoverability/landing

**Data:** 2026-05-10
**Status:** Aceito

## Origem

- **Investigação:** Análise pré-publicação no Claude Code marketplace (sessão `/triage` de 2026-05-10) detectou que o `README.md` em PT-BR limita discoverability para o público anglófono majoritário do canal, enquanto `plugin.json` e `marketplace.json` descriptions já operam em EN sem registro doutrinário.
- **Decisão base:** [ADR-007](ADR-007-idioma-artefatos-informativos.md) (parcialmente invertida — README sai do escopo "fora do escopo / livre — escolha do dev/projeto"; ver `## Decisão` abaixo).

## Contexto

`docs/philosophy.md` → "Convenção de idioma" e ADR-007 cobrem hoje duas categorias de artefato:

- **Operativa** — prosa de skills/agents, headers de templates, relatórios, ADRs, planos, `BACKLOG.md`, `CLAUDE.md`, `philosophy.md`, `install.md`, `README.md`. Espelha o idioma do projeto consumidor (default canonical PT-BR).
- **Informativa do registro de mudanças** — `CHANGELOG.md`, mensagens de tag anotada, descrições de PR. Segue idioma da convenção de commits (ADR-007).

ADR-007 (`## Decisão` → "Fora do escopo") explicitamente lista `README.md` como **livre — escolha do dev/projeto, audiência diferente, sem benefício de alinhar com idioma de commit**. A categoria "operativa" agrupa o README com SKILLs/agents/philosophy/CLAUDE — mas a audiência do README é distinta dos demais: não é "dev escrevendo/lendo durante desenvolvimento", é leitor pré-adoção decidindo se vai instalar o plugin.

Falta convenção explícita para uma terceira categoria: **artefatos cuja função primária é discoverability** — lidos por audiência externa **antes** da decisão de adoção.

Evidência empírica de que o critério "público alvo do canal" já opera implicitamente:

- `.claude-plugin/plugin.json` `description` está em EN.
- `.claude-plugin/marketplace.json` `description` (top-level e por plugin) está em EN.
- `keywords`/`tags` em ambos os manifests estão em EN.

Esses artefatos faticamente seguem público anglófono do Claude Code marketplace, sem ADR formalizando. Sem regra explícita, projeto consumidor (e skill author futuro) pode ficar com:

- README em idioma do dev (PT) e descriptions em EN, drift entre o que está no card do marketplace e o que o leitor encontra ao abrir o repo.
- Decisões ad-hoc sobre cada novo artefato de discoverability (GitHub About, marketplace cards, etc.) sem doutrina compartilhada.

## Decisão

**Artefatos de discoverability/landing seguem o idioma do público alvo do canal de descoberta.**

**Critério mecânico:** "artefato cuja função primária é ser indexado/lido por audiência externa **antes** de a pessoa decidir adotar o plugin".

Cobertura concreta:

- `README.md` raiz do plugin.
- `.claude-plugin/plugin.json` `description`.
- `.claude-plugin/marketplace.json` descriptions (top-level e por plugin).
- `keywords`/`tags` em manifests (vocabulário de busca).
- GitHub repo About / topics (canal de descoberta, mesmo não versionado).

**Fora do escopo:**

- `docs/install.md` (lido **após** adoção, audiência operativa).
- `docs/philosophy.md` (doutrina operativa).
- `CLAUDE.md` (operating instructions do agente).
- ADRs / planos em `docs/plans/` / `BACKLOG.md` (operativos).
- `CHANGELOG.md` / tag annotations / PR descriptions (cobertos por ADR-007).

Razões:

- **Audiência distinta.** Discoverability serve leitor pré-adoção; operativa serve dev no projeto. Idioma alinhado à audiência reduz fricção em cada caso.
- **Critério mecânico testável.** "Lido antes ou depois da adoção" é determinável sem julgamento subjetivo. Skill author futuro consegue enquadrar artefato novo sem reabrir doutrina.
- **Ratifica status quo dos manifests.** `plugin.json`/`marketplace.json` descriptions já operam em EN sem ADR; formalizar reduz dívida doutrinária silenciosa.

## Consequências

### Benefícios

- README do plugin alcança público anglófono majoritário do Claude Code marketplace, ampliando discoverability sem custo recorrente.
- Manifests já-EN ganham respaldo doutrinário (deixa de ser status quo silencioso).
- Skill author futuro tem critério para enquadrar artefato novo (canal novo de discoverability, marketplace listing, etc.).
- ADR-007 fica com escopo mais nítido (registro de mudanças, audiência única — leitor de release).

### Trade-offs

- **Operador PT que entra via README perde porta nativa em PT.** Mitigado por link explícito no README EN para `docs/philosophy.md` PT (ver "Caminho escolhido" no fim de `## Alternativas consideradas`); leitor PT bate em philosophy.md em 1 clique. `docs/install.md`, `CLAUDE.md`, ADRs, planos e `BACKLOG.md` continuam em PT.
- **Adiciona terceira categoria editorial** ao léxico do projeto (operativa, informativa, discoverability). Leitor de doutrina precisa internalizar a partição. Custo aceitável dado ganho de discoverability; partição fica explícita em `philosophy.md` → "Convenção de idioma".

### Limitações

- Não cobre marketplaces dual-language nativos (cenário futuro). Reabrir se emergir.
- Não cobre comunicação corporativa de release (issues, Discussions, posts em redes sociais) — esses ficam fora do toolkit, decisão local.
- Em projetos com público alvo do canal idêntico ao público operativo, a regra coincide com a Convenção de idioma — ADR-012 é vacuamente satisfeito, sem custo.

## Alternativas consideradas

- **(a) README bilíngue lado-a-lado.** Descartado: leitor recebe duplo conteúdo, manutenção dupla, sem clear winner para nenhum público.
- **(b) README EN-only sem link para philosophy.md.** Descartado: público PT perde porta de entrada nativa; philosophy.md PT continua acessível mas sem sinalização explícita.
- **(c) README EN + `README.pt-BR.md` separados.** Descartado: dupla manutenção sem ganho proporcional, drift quase certo entre versões.
- **(d) Manter PT + investir em description longa em EN no marketplace.** Descartado: marketplace description tem limite de caracteres; público anglófono que clica para o repo bate em PT, resolve sintoma do card mas não da landing.
- **(e) Status quo + GitHub About em EN.** Descartado: mínimo intervencionismo não resolve discoverability do leitor que abre o repo (e About reflete o tópico raso, não o conteúdo).
- **(f) README EN + seção PT topo apontando philosophy.md.** Descartado: simétrico ao caminho c-escolhido com virtude invertida (privilegia anglófono mas não esconde porta PT). Custo equivalente; preferimos link no fim ("Philosophy" section) por ser convenção mais comum em READMEs OSS — leitor anglófono não precisa rolar passando seção PT antes do conteúdo principal.

**Caminho escolhido:** README EN com seção "Philosophy" curta linkando `docs/philosophy.md` PT (anexo "Para este repo" abaixo, não na regra).

## Gatilhos de revisão

- Marketplace passa a suportar dual-language listing nativo → reabrir para considerar i18n por canal.
- Público alvo do canal muda predominância (ex.: PT vira majoritário no Claude Code marketplace) → critério "público alvo do canal" adapta automaticamente; revisar exemplos congelados na seção "Para este repo".
- Surge novo artefato no toolkit cuja audiência está na fronteira (operativa-vs-discoverability) → revisar critério mecânico para incluir explicitamente.

## Para este repo

- `README.md` reescrito em EN com link para `docs/philosophy.md` PT.
- `.claude-plugin/plugin.json` e `.claude-plugin/marketplace.json` descriptions seguem EN (status quo ratificado).
- `docs/install.md`, `docs/philosophy.md`, `CLAUDE.md`, ADRs, planos e `BACKLOG.md` permanecem em PT (operativos, fora do escopo).
