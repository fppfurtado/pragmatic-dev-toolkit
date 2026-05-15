# ADR-026: Critério mecânico de absorção de findings do `design-reviewer` pré-commit

**Data:** 2026-05-13
**Status:** Aceito

## Origem

- **Decisão base:** [ADR-011](ADR-011-wiring-design-reviewer-automatico.md) § Decisão #1 estabeleceu *"findings reportados ao operador, que decide aplicar antes de commitar ou seguir como está"*. Implementação literal = sempre cutucar o operador. ADR-026 refina o trilho — default invertido (absorver pré-commit), cutucar somente quando finding satisfaz critério explícito.

## Contexto

ADR-011 atribuiu ao operador a aplicação de cada finding do `design-reviewer`. Doutrina escrita assume volume baixo (gatilho de revisão #1 do ADR-011 prevê reabrir "se operador frequentemente ignora findings sem aplicar"). Prática empírica nas 11 sessões pós-ADR-011 (PRs #54-#60 + commits cirúrgicos F_arch/H_arch + sessões da release v2.6.0) divergiu: assistente passou a absorver findings triviais pré-commit em vez de cutucar o operador para cada um.

Padrão observado (dados retroativos):

| Classe de finding | Volume aprox. | Tratamento empírico | Acerto |
|---|---|---|---|
| Drift textual (vocabulário canonical, cross-ref preciso, path) | ~7 ocorrências | absorvido pré-commit | 100% sem retrabalho |
| Verbalização de regra implícita / alternativa rebatida descritivamente | ~5 ocorrências | absorvido pré-commit | 100% sem retrabalho |
| Renumeração/cross-ref após refactor estrutural | ~5 ocorrências | absorvido pré-commit | 100% sem retrabalho |
| Trade-off editorial (manter/encolher/remover) | ~3 ocorrências | perguntado via enum | operador escolheu opções intermediárias em todas |
| Defensividade comportamental com 2+ opções de cobertura | ~2 ocorrências | perguntado via enum | operador escolheu opções intermediárias |
| Drift detectado em sessão paralela / contexto externo | ~1 ocorrência | comunicado e tratado fora do flow | n/a |

Padrão revelou eixo discriminante: **shape do finding** (alternativas legítimas / contradição com doutrina / contexto externo), não conteúdo nem stack. Findings caminho-único foram absorvíveis sem retrabalho; findings com alternativas competindo precisaram decisão do operador.

**Aplicação retroativa do critério aos findings empíricos** (paralelo a ADR-020/023 § Aplicação retroativa):

| Sessão (PR/commit) | Finding | Condição disparada | Tratamento |
|---|---|---|---|
| ADR-020 draft (Onda 1) | 7 findings de design-reviewer (estrutura ADR) | nenhuma (caminho-único editorial) | Absorvidos pré-commit |
| ADR-021 draft (Onda 1) | findings de design-reviewer | nenhuma (caminho-único editorial) | Absorvidos pré-commit |
| ADR-023 draft (PR #56) | 6 findings de design-reviewer | nenhuma (caminho-único editorial) | Absorvidos pré-commit |
| PR #57 plano | findings do design-reviewer (path semântico templates vs procedures) | Cond 1 (alternativas legítimas) | Cutucado via prosa, decidido pureza semântica |
| PR #58 plano | 3 findings altos do design-reviewer | nenhuma (caminho-único: operacionalização vs fonte, rótulos no spoke, anti-drift grep) | Absorvidos pré-commit |
| PR #59 plano (Onda 4) | finding G_prose (remover/encolher/descartar) | Cond 1 (3 alternativas legítimas) | Cutucado via `AskUserQuestion`, operador escolheu encolher |
| ADR-025 draft (PR #60) | 6 findings de design-reviewer | nenhuma (todos caminho-único: precisão de origem, cross-ref textual, verbalização do critério, defensividade legacy, path roadmap, categoria editorial) | Absorvidos pré-commit |
| ADR-025 finding "defensividade legacy YAGNI" | 1 finding alto | Cond 1 (3 níveis: remover / só /triage / ambos checks) | Cutucado via `AskUserQuestion`, operador escolheu só /triage |
| Plano H_arch (PR #60) | 5 findings adicionais | nenhuma (todos caminho-único) | Absorvidos pré-commit |
| ADR-026 draft (sessão atual) | 7 findings de design-reviewer | F1/F2/F3/F5/F6/F7 (caminho-único — 6); F4 (Cond 1 — 3 alternativas de robustez de detecção) | 6 absorvidos pré-commit; F4 cutucado |

Total empírico: ~17 findings absorvidos (caminho-único, zero retrabalho); ~4 findings cutucados (Cond 1 disparou em todos). 100% dos cutucados envolveram alternativas concretas competindo; 100% dos absorvidos foram caminho-único. Critério é descritivo, não prescritivo.

Operador sinalizou expressamente preferência por absorção dos óbvios ("não quero ficar aprovando findings óbvios, ou de baixo custo/benefício") e pediu generalização para qualquer stack futura. Convenção empírica do assistente precisa virar regra escrita — caso contrário (i) fica frágil entre sessões (não documentada → reverte ao default literal de ADR-011), (ii) não generaliza (futuros operadores/skills herdam doutrina literal sem o trilho pragmático), (iii) erro de classificação não tem critério de auditoria.

## Decisão

Default **invertido**: `design-reviewer` reporta findings → assistente **absorve pré-commit + reporta absorção no commit message em seção estruturada dedicada**. Operador inspeciona via diff/commit message e pode reverter se discordar (override por inspeção pós-fato).

**Forma do reporte.** Quando ≥1 finding é absorvido pré-commit, commit message inclui seção `## design-reviewer findings absorvidos` (idioma da convenção de commits do projeto consumidor per ADR-007) com bullets curtos — 1 linha por finding no formato:

```
- <localização breve>: <correção aplicada> (caminho-único).
```

Auditoria pós-fato via `git log -p | grep "## design-reviewer"` lista todas as absorções para revisão. Seção é omitida quando não há findings absorvidos (zero overhead no caso comum). Findings que dispararam ≥1 das 3 condições e foram cutucados via `AskUserQuestion` não entram nesta seção — viram parte do trace narrativo normal do commit message (decisão do operador descrita).

Cutucar operador via `AskUserQuestion` **somente quando** o finding satisfaz **qualquer** das 3 condições:

1. **≥2 alternativas legítimas competindo.** Sugestão do reviewer admite 2+ caminhos válidos com trade-offs distintos. Operador escolhe. **Calibração:** alternativa apresentada pelo reviewer e descritivamente rebatida no próprio finding conta como **1 caminho** (reviewer assumiu a decisão); só conta como ≥2 quando o reviewer apresenta caminhos competindo sem rebater.
2. **Contradiz decisão documentada.** Finding rebate algo em ADR, `docs/philosophy.md` ou `CLAUDE.md`. Operador decide manter (honrar documentação) ou inverter (refinar documentação como passo separado).
3. **Exige contexto fora do diff/plano/ADR.** Intenção de produto, restrição externa, política organizacional do consumer — informação que o assistente não pode inferir dos artefatos visíveis.

**Cláusula default-conservadora.** Se o assistente não consegue classificar com confiança em qualquer das 3 condições (domínio desconhecido, shape ambíguo do finding), cutucar. Dúvida → cutucada.

**Posição vs ADR-011.** ADR-026 sucede parcialmente ADR-011 § Decisão #1. Mecânica do wiring (quando dispara, override por inação) permanece vigente; atribuição literal "operador decide aplicar" é refinada pela cláusula de absorção pré-commit deste ADR. Status de ADR-011 à época era `Proposto` (promovido a `Aceito` na onda 2026-05-15) — paralelo a ADR-005 ↔ ADR-025: extensão semântica não obrigou revisão de status do ancestral à época. Cross-ref textual em ADR-011 prescrito pelo plano de implementação deste ADR (atualização editorial recíproca, paralelo a ADR-009 § Gatilhos sendo referenciado por ADR-011 § Origem).

Critério é **stack-agnóstico** — opera sobre shape do finding (alternativas / contradição / contexto externo), não sobre conteúdo da correção ou stack do projeto consumidor. Funciona em Python, Java, ou qualquer stack futura. Estável sob recursão — `design-reviewer` revisando ADR sobre seu próprio dispatching passa pelo mesmo critério (caso testado durante revisão deste ADR).

Razões:

- **Empíricas:** 100% dos findings absorvidos previamente caem em "caminho-único" (nenhuma das 3 condições disparou); 100% dos findings perguntados via enum satisfizeram ≥1 condição. Critério é descritivo, não prescritivo.
- **Pragmáticas:** operador expressou preferência direta. Cutucar para drift textual gera friction sem ganho.
- **Defensivas:** as 3 condições preservam o ponto crítico do `design-reviewer` — decisões estruturais com alternativas legítimas, contradição com doutrina, ou dependência de contexto externo **sempre** passam pelo operador. Não há absorção de decisão de design.
- **Auditáveis:** commit message lista findings absorvidos — operador pode revisar e reverter via novo commit ou amend. Erro de classificação tem trace.
- **Override por inspeção pós-fato substitui parcialmente "override por inação" de ADR-011** para findings classificados como caminho-único. Operador troca aprovação ativa pré-commit por reversão pós-commit; trade-off aceito pelos dados retroativos (17 absorções empíricas, zero retrabalho). Para findings que satisfazem ≥1 das 3 condições, "override por inação" de ADR-011 segue vigente — operador continua decidindo ativamente antes do commit.

## Consequências

### Benefícios

- **Menos friction:** `/triage` caminho-com-plano e `/new-adr` deixam de gerar prompt para cada finding trivial. Operador é cutucado apenas para decisões reais.
- **Sinal mais nítido ao reviewer:** absorção automática reforça que findings devem ser substantivos. Falsos positivos viram drag mais visível (cada absorção desnecessária aparece no commit message).
- **Generalização cross-stack:** critério opera sobre shape, não conteúdo — herdado por skills/agents futuros sem reinterpretação.
- **Convenção empírica formalizada:** assistente novo (modelo atualizado, sessão fresh) herda o trilho via doutrina escrita em vez de re-derivá-lo.

### Trade-offs

- **Classificação fica com o assistente.** Erro de classificação (finding com 2 alternativas tratado como caminho-único) gera absorção indevida sem cutucar. Mitigação: commit message exposes; operador revisa.
- **Volume do commit message cresce** quando há findings absorvidos. Trade aceitável — operador prefere texto a prompt.
- **Falsos negativos persistem em casos-limite.** Finding crítico classificado erroneamente como "caminho-único" some — risco semelhante ao já reconhecido por ADR-011 § Trade-offs ("prosa volátil"). Reabrir trilho persistente se materializar (gatilho registrado abaixo).

### Limitações

- **Domínios desconhecidos podem confundir classificação.** Stack nova com vocabulário específico — assistente pode não reconhecer alternativas legítimas. Coberto pela cláusula default-conservadora em § Decisão (dúvida → cutucada).
- **Critério não substitui revisão editorial humana de qualidade do reviewer.** Se `design-reviewer` produzir findings sistematicamente vagos ou off-target, absorção automática multiplica o problema. Refinar critério editorial do reviewer é decisão separada.

## Alternativas consideradas

### (a) Status quo (sempre cutucar, ADR-011 literal)

Cada finding gera prompt. Conformidade literal com ADR-011 § Decisão. **Rejeitado:** operador expressou expressamente rejeição via feedback explícito; prática empírica já divergiu há 11 sessões sem retrabalho observado.

### (b) Default absorver sem critério (free pass)

Assistente absorve tudo, reporta no commit. **Rejeitado:** absorve decisões estruturais que devem passar pelo operador (contradição com doutrina, alternativas legítimas competindo). Apaga o valor de gate pré-commit do `design-reviewer`.

### (c) Critério baseado em "tipo de mudança" (textual vs comportamental)

Absorver edits textuais; cutucar mudanças comportamentais. **Rejeitado:** critério stack-coupled (precisa entender comportamento) e captura mal o padrão empírico. Refactor comportamental cosmético é absorvível (renumeração de passos em /triage F_arch foi comportamento-preservante mas envolveu 5 arquivos); drift textual com 2 caminhos editoriais legítimos (literal vs adaptado) precisa cutucada.

### (d) Critério com 4ª condição "mudança comportamental observável"

Adicionar 4ª condição cobrindo mudanças que alteram o que o software faz observavelmente. **Rejeitado:** redundante com condição 2 (mudança comportamental relevante quase sempre contradiz decisão documentada ou exige contexto externo). Cria área cinza editorial sem ganho — preferir 3 condições disjuntivas claras.

## Gatilhos de revisão

- **Operador reverter findings absorvidos sistematicamente** via commits subsequentes. Sinal de classificação errônea recorrente — reabrir critério, possivelmente adicionar 4ª condição ou refinar definição de "alternativas legítimas".
- **Reviewer começar produzindo findings repetidamente classificáveis como "alternativas competindo" que operador descarta sempre.** Sinal de critério editorial do reviewer para refinar (paralelo a gatilhos de ADR-009/011) — não invalida ADR-026.
- **Skill nova introduzir reviewer pre-fact com semântica diferente do `design-reviewer`** (ex.: revisor de produto pre-fact). Revisar escopo deste ADR — critério aplica apenas a `design-reviewer` por design.
- **Operador reportar findings importantes perdidos no commit message** (volume cresce demais, operador deixa de inspecionar). Reabrir formato — possivelmente persistir absorções em `## Pendências de validação` análogo a ADR-002.

## Implementação

Commits do plano `criterio-mecanico-absorcao-findings-design-reviewer` que executou este ADR:

(A preencher após execução via `/run-plan`.)
