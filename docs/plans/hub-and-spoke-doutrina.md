# Plano — Hub-and-spoke de doutrina: idioma do relatório + linguagem ubíqua (Onda 3b)

## Contexto

Bundle pré-curado pela auditoria `docs/audits/runs/2026-05-12-prose-tokens.md` (propostas B + D), sequenciado como **Onda 3b** em `docs/audits/runs/2026-05-12-execution-roadmap.md`. As 2 propostas tocam **doutrina dispersa entre múltiplos consumers** (5 agents + `/triage` para B_prose; `philosophy.md` descrevendo pipeline operacional para D_prose). Bundle resolve dois eixos no mesmo move: cria hub em CLAUDE.md para "Idioma do relatório" (B_prose) e migra "Linguagem ubíqua na implementação" em philosophy.md para princípio puro (D_prose). Hub-and-spoke é precedente estabelecido (AskUserQuestion mechanics, Convenção de naming em CLAUDE.md hoje).

**ADRs candidatos:** [ADR-007](../decisions/ADR-007-idioma-artefatos-informativos.md) (governance de idioma — B_prose consolida a regra em hub sem alterá-la; D_prose só remove descrição de pipeline operacional que duplica em philosophy.md).

## Resumo da mudança

Duas frentes editoriais sob doutrina existente (sem ADR — hub-and-spoke pattern e separação philosophy/operacional são precedentes):

1. **B_prose — consolidar "Idioma do relatório" em CLAUDE.md hub** + referenciar nos 6 sites (5 agents + `/triage`). Cria nova seção `## Reviewer/skill report idioma` em CLAUDE.md com regra universal (~3 linhas). Cada spoke vira referência de 1 linha. Code-reviewer preserva 1 linha extra sobre rótulos estruturados (`Localização`, `Problema`, `Filosofia violada`, `Sugestão`) — info agent-specific que não pertence ao hub. Demais agents e `/triage` ficam só com a referência. Redução estimada: ~50 palavras líquidas (audit estimou ~58 — diff por preservar rótulos de code-reviewer como spoke).

2. **D_prose — migrar "Linguagem ubíqua na implementação" de philosophy.md para princípio puro**. Atualmente seção tem 3 frases: 1 princípio + 2 descrevendo pipeline operacional (`/triage` passo 4 → `/run-plan` passo 2 → `code-reviewer`). Substituir por 1-2 frases de princípio (wording-alvo do audit). Pipeline operacional já vive nos consumers concretos (skills/agents); descrição em philosophy.md é duplicação. Redução: ~30 palavras + alinhamento de eixos (philosophy = princípio; skills/CLAUDE.md = operacional). Sustenta onda anterior "philosophy.md: refatorar para conter apenas princípios" (BACKLOG `## Concluídos`).

**Trade-off comum (hub-and-spoke):** dependência cruzada — leitor de spoke precisa abrir CLAUDE.md para entender a regra completa. Mitigação: hub fica no documento auto-loaded a cada turn (CLAUDE.md), então custo de leitura é amortizado; consumers ganham concisão a cada invocação de subagent. Precedente: "AskUserQuestion mechanics" no CLAUDE.md já é hub para 9 skills/agents.

**Variantes preservadas vs removidas:**

- **Code-reviewer rótulos** (`Localização`, `Problema`, `Filosofia violada`, `Sugestão`): preservados como linha agent-specific após a referência ao hub. Cada agent tem sua estrutura de findings; rótulos pertencem ao agent, não ao princípio universal.
- **Design-reviewer "omite ver philosophy.md"**: drift de terseness no spoke atual; após hub, todos os spokes ficam uniformes (referência igual). Drift naturalmente eliminado.

## Arquivos a alterar

### Bloco 1 — Criar hub em CLAUDE.md + atualizar 6 spokes (B_prose) {reviewer: doc}

- `CLAUDE.md`: adicionar nova seção `## Reviewer/skill report idioma` após `## AskUserQuestion mechanics` (paralelo a hub editorial existente). Wording-alvo (~4 linhas):

  *"Reviewer ou skill que produz relatório/texto-de-saída espelha o idioma do projeto consumidor (default canonical PT-BR). Esta seção operacionaliza, para reviewers shippados e `/triage`, a regra-mãe em `docs/philosophy.md` → 'Convenção de idioma'; [ADR-007](docs/decisions/ADR-007-idioma-artefatos-informativos.md) cobre artefatos informativos (changelog, tag messages, commits) fora deste escopo. Aplica-se aos 5 reviewers (`code-reviewer`, `qa-reviewer`, `security-reviewer`, `doc-reviewer`, `design-reviewer`) e ao texto produzido por `/triage`. Cada artefato preserva sua estrutura interna traduzindo-a junto."*

- `agents/code-reviewer.md` linha 69: substituir parágrafo de ~40 palavras por 2 linhas (assimetria intencional vs outros spokes — preserva rótulos para o subagent isolado, que NÃO tem CLAUDE.md auto-loaded). Wording-alvo:

  *"Idioma do relatório: per `CLAUDE.md` → 'Reviewer/skill report idioma'. Rótulos estruturados (`Localização`, `Problema`, `Filosofia violada`, `Sugestão`) traduzidos junto."*

- `agents/qa-reviewer.md` linha 51: substituir parágrafo de ~20 palavras por:

  *"Idioma do relatório: per `CLAUDE.md` → 'Reviewer/skill report idioma'."*

- `agents/security-reviewer.md` linha 45: mesmo wording que qa.
- `agents/doc-reviewer.md` linha 52: mesmo wording que qa.
- `agents/design-reviewer.md` linha 100: mesmo wording que qa (drift de "omite ver philosophy.md" naturalmente eliminado).
- `skills/triage/SKILL.md` linha 79: substituir "Idioma de saída: espelhar o do projeto consumidor (default canonical PT-BR; ver 'Convenção de idioma' em `docs/philosophy.md`)." por:

  *"Idioma de saída: per `CLAUDE.md` → 'Reviewer/skill report idioma'."*

**Nota editorial sobre rótulos do code-reviewer:** preservados no spoke (assimetria intencional vs outros 5 spokes). Motivo: subagents são invocados isoladamente sem CLAUDE.md auto-loaded — referência pura "per CLAUDE.md → ..." obrigaria o subagent a abrir CLAUDE.md para entender que rótulos traduzem. Custo da assimetria: +12 palavras no spoke de code-reviewer. Custo da simetria absoluta: regressão informacional para code-reviewer subagent. Optou-se pela assimetria. Outros spokes (qa/security/doc/design-reviewer + `/triage`) ficam reference-only — não têm rótulos estruturados análogos hoje.

### Bloco 2 — Trim "Linguagem ubíqua na implementação" em philosophy.md (D_prose) {reviewer: doc}

- `docs/philosophy.md` linhas 73-75 (seção `## Linguagem ubíqua na implementação`): substituir as 3 frases atuais (1 princípio + 2 pipeline operacional) por 1-2 frases de princípio puro. Wording-alvo (audit):

  *"Bounded contexts e linguagem ubíqua só são pilares se chegarem ao código. Vocabulário registrado no domínio mas ausente nos identificadores produzidos vira ornamento de alinhamento. Pipeline operacional vive em skills/agents; aqui só o princípio."*

  Wording absorve **findings altos 1 e 3** do design-reviewer:
  - Mantém termo conceitual **"no domínio"** (não `ubiquitous_language` — papel é mecânica do toolkit, não conceito doutrinário; princípio em philosophy.md deve ler em termos universais).
  - Remove referência **"frase-tese"** (ancoragem textual implícita à linha 7 do mesmo arquivo — dangling reference se a seção 'A filosofia em uma frase' for renomeada).

  Comparação:
  - Atual (3 frases): princípio + ancoragem "frase-tese" + descrição operacional do pipeline (`/triage` passo 4, `/run-plan` passo 2, `code-reviewer` seção 'Identificadores').
  - Novo (3 frases enxutas): princípio + frase-âncora (sem "frase-tese") + remete a skills/agents (sem enumerar). Pipeline concreto vive em `/triage`, `/run-plan`, `code-reviewer` (documentação primária; philosophy.md não duplica).

### Bloco 3 — Atualizar roadmap marcando B_prose + D_prose shipped {reviewer: doc}

- `docs/audits/runs/2026-05-12-execution-roadmap.md`:
  - Marcar item B_prose (linha 43) e D_prose (linha 44) com `[x]` + link a [plano] + data `2026-05-12`. PR # adicionado pós-merge (convenção das Ondas 1-3a — `chore(roadmap)` separado em main pós-merge).
  - Nota no final do bloco "3b" indicando Onda 3b fechada.

## Verificação end-to-end

- `grep -c "^## Reviewer/skill report idioma$" CLAUDE.md` retorna 1 (nova seção criada).
- `grep -c "per \`CLAUDE.md\` → 'Reviewer/skill report idioma'" agents/*.md skills/triage/SKILL.md` retorna **6** (5 agents + /triage referenciam o hub).
- `grep -c "Idioma do relatório: \*\*espelhar" agents/*.md` retorna **0** (parágrafo antigo erradicado).
- `grep -c "Localização.*Problema.*Filosofia violada.*Sugestão" CLAUDE.md` retorna 1 (rótulos absorvidos no hub).
- `grep -c "Localização.*Problema.*Filosofia violada.*Sugestão" agents/code-reviewer.md` retorna 0 (rótulos saíram do spoke).
- `grep -c "passo 4 grava" docs/philosophy.md` retorna 0 (descrição de pipeline operacional erradicada em philosophy.md).
- `grep -c "Bounded contexts e linguagem ubíqua só são pilares" docs/philosophy.md` retorna 1 (frase-âncora do princípio preservada).
- `grep -E "^- \[x\] \*\*[BD]_prose\*\*" docs/audits/runs/2026-05-12-execution-roadmap.md | wc -l` retorna 2 (Bloco 3 marcou ambos).
- **Anti-drift entre hub e spokes** (per finding 4 do design-reviewer): nome único da seção em todos os sites. Comando: `count=$(grep -h "→ '[^']*'" agents/code-reviewer.md agents/qa-reviewer.md agents/security-reviewer.md agents/doc-reviewer.md agents/design-reviewer.md skills/triage/SKILL.md | grep -o "'[^']*'" | sort -u | wc -l)`; resultado esperado: **1** (todos os 6 spokes apontam para a mesma string `'Reviewer/skill report idioma'`). Resultado ≠1 indica drift de capitalização/typo no nome da referência.
- `wc -l CLAUDE.md` esperado entre 172 e 178 após bundle (Bloco 1 adiciona ~5 linhas na nova seção; cap nominal 200, ainda confortável).
- `wc -l docs/philosophy.md` esperado ≤75 após Bloco 2 (encurta de 77 para ~74-75 linhas).
- Pipeline CI (`.github/workflows/validate.yml`) verde no PR.

## Notas operacionais

- **Ordem dos blocos:** 1 → 2 → 3. Bloco 1 é a maior unidade (1 hub + 6 spokes); Bloco 2 é trim cirúrgico em philosophy.md; Bloco 3 atualiza roadmap.
- **Reviewer dispatch:** todos `{reviewer: doc}` — paths `.md` apenas, sem código de produção. `design-reviewer` **não** redisparado por `/run-plan` (ADR-011 — opera pré-fato; já disparou neste `/triage` no plano).
- **BACKLOG (sem transição automática nesta onda):** linha umbrella em `## Próximos` (linha 5 atual) cobre as 4 ondas; **não** transita ao fim desta Onda 3b. `**Linha do backlog:**` omitido deliberadamente do `## Contexto` (per convenção estabelecida nas Ondas 3a/2). Tracking da onda no Bloco 3 (roadmap update).
- **Re-rodar `prose-tokens` depois desta onda:** roadmap linha 63 prevê — G_arch (Onda 3a) sozinho removeu ~25 linhas de `/triage §0` e mudou alvos restantes; B_prose adiciona hub em CLAUDE.md (+ ~5 linhas) e D_prose remove ~3 linhas em philosophy.md. Antes de iniciar Onda 4, re-rodar prose-tokens audit para refinar alvos (F_prose, G_prose, E_prose).
- **Atomicidade do Bloco 1:** Hub + spokes referenciam-se mutuamente. Reviewer doc valida que a referência textual nos spokes bate exatamente com o nome da seção no hub (`'Reviewer/skill report idioma'`). Drift entre os dois quebra discoverability lexical da regra.
- **Bloco 1 não-trivial mas atômico.** 7 arquivos tocados (CLAUDE.md + 5 agents + /triage). Decisão de empacotar em bloco único: split entre "criar hub" e "atualizar spokes" criaria intermediate state onde hub existe sem consumers (ou vice-versa), e os edits são small em cada site. Single block facilita review do par hub-spoke.
- **Sem `**Termos ubíquos tocados:**`** no `## Contexto`: nenhuma RN/aggregate tocada; pure editorial.
- **PR # post-merge:** convenção das Ondas 1, 2, 3a — atualização do PR # no roadmap entry como commit separado `chore(roadmap)` em main pós-merge. Já capturado em BACKLOG ## Próximos (linha sobre `/run-plan §Publicar` endurecer follow-up).
- **Trade-off hub-and-spoke do code-reviewer rótulos:** considerada alternativa (spoke retém linha sobre rótulos, hub fica curto). Rejeitada por dois motivos: (a) rótulos são exemplo do princípio "traduz estrutura interna junto" — pertence ao princípio, não ao agent; (b) outros agents podem ganhar rótulos similares no futuro (`qa-reviewer` já tem subseções estruturadas) e a referência única no hub serve a todos. Spoke de code-reviewer fica simétrico aos demais.
