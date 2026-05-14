# ADR-029: Cutucada de descoberta cobre `CLAUDE.md` ausente

**Data:** 2026-05-14
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-017](ADR-017-cutucada-uniforme-descoberta-config-ausente.md) § Limitações (linha 81) + § Alternativa (f) descartada. ADR-017 classificou explicitamente o caso "`CLAUDE.md` ausente" como fora do escopo da cutucada — over-reach do plugin sobre estrutura do consumer. ADR-029 inverte parcialmente: estende o gating para cobrir o caso com **string adaptada** que reconhece a ausência sem prescrever criação automática (preservando a postura editorial não-reparativa de [ADR-016](ADR-016-manter-block-gitignored-scripts-no-consumer.md) e do `/init-config` step 1).

## Contexto

Sessão de `/debug` 2026-05-14 surfou gap percebido em projeto novo: o operador instala o plugin, invoca skill com `roles.required` (`/triage`, `/new-adr`, `/run-plan`, `/next`, `/draft-idea`) em projeto sem `CLAUDE.md`, e **não** recebe sinalização do `/init-config`. O triple gating de ADR-017 § Decisão tem condição 1 = "`CLAUDE.md` existe"; ausência falha o gate e suprime a cutucada.

Esse é justamente o cenário onde a descoberta proativa mais importa — projeto novo, primeiro contato com o plugin. ADR-017 reconheceu a limitação (§ Limitações linha 81: *"operador que opta por não ter CLAUDE.md (raro mas válido) não recebe cutucada nem memorização"*) e descartou a alternativa (f) ("Cutucada também quando `CLAUDE.md` está ausente") com três razões:

1. **Over-reach do plugin sobre estrutura do consumer.** `CLAUDE.md` tem propósito mais amplo que o bloco config (instruções gerais ao Claude Code) — sugerir criação só para o plugin é estranho.
2. **Paralelo com gate `Gitignore` de [ADR-005](ADR-005-modo-local-gitignored-roles.md) não se aplica:** lá o plugin já decidiu usar `.claude/local/` e precisa garantir gitignore; em (f) o plugin estaria inferindo necessidade do operador sem sinal claro.
3. **Operador que rodou `/init-config` deliberadamente recebe orientação clara dentro do próprio wizard** (step 1 para com mensagem alinhada).

Empiricamente, razão (3) só fecha o loop **se o operador descobriu `/init-config`**. Em projeto novo sem CLAUDE.md, sem cutucada, e sem memorização one-shot (que também depende de CLAUDE.md para gravar), o operador cai exclusivamente em (a) `Resolution protocol` passo 3 ask-on-demand per role, ou (b) leitura de docs. O atrito do PJe que originou ADR-017 (30 min antes de qualquer skill rodar) é reproduzível em qualquer projeto novo sem CLAUDE.md — talvez pior, porque sem CLAUDE.md a memorização também não opera.

Razões (1) e (2) seguem válidas para **criação automática** de `CLAUDE.md` — postura editorial não-reparativa preservada. Mas **emitir uma linha de texto** que reconhece a ausência e orienta o operador a criar manualmente + rodar `/init-config` é cosmético do ponto de vista de over-reach: nenhuma escrita em arquivo do consumer, apenas sinalização textual no relatório da skill que o operador acabou de invocar.

## Decisão

Estender o gating da cutucada de descoberta para **três saídas** (em vez de duas), cada caso emissor com **string canonical própria**:

- **Caso A — `CLAUDE.md` presente sem marker** (status quo ADR-017): emitir string-A:
  > Dica: este projeto não declara o bloco `pragmatic-toolkit:config` no CLAUDE.md. Rode `/init-config` para configurar todos os papéis de uma vez.
- **Caso B — `CLAUDE.md` ausente** (novo, este ADR): emitir string-B:
  > Dica: este projeto não tem `CLAUDE.md`. Crie o arquivo e rode `/init-config` para configurar os papéis do plugin.
- **Caso C — `CLAUDE.md` presente com marker**: silêncio (status quo ADR-017).

Dedup conversation-scoped (per [ADR-010](ADR-010-instrumentacao-progresso-skills-multi-passo.md)) aplicado **por string**: cada uma observa o histórico visível independentemente. Transição A→B ou B→A dentro da mesma sessão CC (raro, mas possível: operador cria CLAUDE.md mid-session) permite emissão da segunda string mesmo após a primeira ter aparecido — A e B são gaps semanticamente distintos.

**Escopo das 5 skills com `roles.required`** (atualizado de 4 em ADR-017; `/draft-idea` adicionada por [ADR-027](ADR-027-skill-draft-idea-elicitacao-product-direction.md)): `/triage`, `/new-adr`, `/run-plan`, `/next`, `/draft-idea`. Herança editorial preservada (autor de skill nova adiciona o parágrafo seguindo o template).

**`/init-config` permanece inalterada.** Step 1 com `CLAUDE.md` ausente continua parando com mensagem orientadora (*"este projeto não tem CLAUDE.md. Crie o arquivo antes — CLAUDE.md tem propósito mais amplo que o bloco config do plugin; /init-config não cria por design."*) — postura editorial não-reparativa intacta. A cutucada de ADR-029 apenas torna o sinal visível **uma skill antes**, na própria saída do `/triage`/`/next`/etc.

Razões:

- **Descoberta cobre o pior caso de fricção.** Projeto novo sem CLAUDE.md é exatamente onde o operador mais se beneficia do sinal proativo; status quo o expõe a ask-on-demand de 4-6 roles antes de qualquer pista do wizard.
- **Postura não-reparativa preservada.** Cutucada é textual, não modifica nenhum arquivo do consumer. `/init-config` step 1 e ADR-016 ficam intactos como pontos doutrinários sobre `CLAUDE.md` ser território do consumer.
- **String dedicada > string genérica.** String-A literal ("não declara o bloco") aplicada ao caso ausente seria semanticamente enganosa (sugere CLAUDE.md presente sem o bloco quando o arquivo nem existe). String-B explícita resolve a leitura em um turno cognitivo.
- **Custo editorial localizado.** 5 sites × 2 strings = 10 ocorrências para manter. Aceito sob ADR-017 § Alternativa (g) (YAGNI sobre helper compartilhado); gatilho de reabertura recalibrado em § Gatilhos abaixo.
- **Dedup por string preserva fidelidade do sinal.** Operador que viu string-B e depois criou CLAUDE.md sem marker (caminho natural de onboarding) se beneficia de ver string-A na próxima invocação para fechar a próxima lacuna.

## Consequências

### Benefícios

- Operador em projeto novo (caso mais comum de onboarding) recebe sinal de descoberta de `/init-config` na primeira invocação de skill com `roles.required`, com texto literal acionável ("crie o arquivo e rode /init-config").
- Recolocação semântica: string-A volta a ser literalmente verdadeira (afirma "não declara o bloco" só quando CLAUDE.md de fato existe).
- 5 skills cobrem o caso uniformemente — sem fragmentação per skill nem helper compartilhado.

### Trade-offs

- **Duplicação textual cresce de 5 strings → 10.** Manutenção editorial sobe linearmente. Aceito — paridade com a postura de ADR-017 § Alternativa (g); gatilho de reabertura recalibrado em § Gatilhos abaixo.
- **Risk de drift entre as duas strings.** Convenção fica nas 5 SKILLs + CLAUDE.md → "Cutucada de descoberta"; herança editorial sustenta. `doc-reviewer` em PR pode flagrar divergência via grep dos paths concretos.
- **Cutucada em projeto sem CLAUDE.md pode ser ignorada** tantas vezes quanto a do caso A. Operador que ignora indica preferência por ask-on-demand — plugin não argumenta de volta (paralelo a ADR-017 § Trade-offs).

### Limitações

- Cutucada **ainda não diferencia** `CLAUDE.md` gitignored — probe textual ("arquivo existe + marker ausente") dispara string-A em projeto onde o arquivo está gitignored sem o bloco. Operador roda `/init-config`, que opera dentro do gitignore garantindo replicação via `.worktreeinclude` per [ADR-030](ADR-030-aceitar-claude-md-gitignored-via-worktreeinclude.md) — caminho construtivo, sem recusa intermediária (substitui leitura inicial deste ADR que dependia da extrapolação de ADR-016 em `/init-config` step 3, agora revertida). Alternativa "endurecer probe" (excluir gitignored via `git check-ignore`) segue descartada para não introduzir I/O git no hot path nem reabrir o over-reach já rebatido por ADR-017 § Alternativa (f) — cutucada permanece silente quanto ao status de gitignore; `/init-config` resolve o caso quando invocado.
- Dedup conversation-scoped sob context compression em sessões muito longas: cada string pode reaparecer (aceito; gatilho de revisão idêntico ao de ADR-017).

## Alternativas consideradas

### (a) Reutilizar string-A literal para o caso ausente

String única, mantendo 5 sites × 1 string. Operador no caso ausente vê "não declara o bloco" e roda `/init-config`, que para em step 1 e o orienta a criar CLAUDE.md.

Descartado:

- **Leitura inicial enganosa.** "não declara o bloco" sugere que CLAUDE.md existe sem o bloco; operador em projeto novo sem CLAUDE.md lê e pensa "mas eu nem tenho CLAUDE.md" antes de processar a sugestão — um turno de cognição desperdiçado.
- **Custo da clareza é baixo.** 1 string adicional × 5 sites = 5 linhas a mais para manter; trade-off favorece pureza semântica (aplicação da preferência editorial validada do operador: categorias com fronteira nítida prevalecem sobre churn).
- Bifurcação cutucada pelo operador no `/triage` que produziu este ADR; escolha "String adaptada" registrada.

### (b) Cutucada que prescreve criação automática de CLAUDE.md mínimo

Skills com `roles.required` criariam `CLAUDE.md` mínimo (1 linha) na ausência, em vez de só cutucar.

Descartado:

- **Over-reach genuíno sobre estrutura do consumer.** Razões (1) e (2) de ADR-017 § Alternativa (f) seguem válidas para criação. `CLAUDE.md` é território do consumer; o plugin não decide existir.
- Cria precedente para outras skills criarem arquivos canonical do consumer (`docs/domain.md`, `IDEA.md`) na primeira invocação — escalada indesejada.
- Postura editorial não-reparativa (ADR-016 + `/init-config` step 1) é doutrina explícita; reverter aqui cria inconsistência.

### (c) Edit in-place no ADR-017 (sem ADR sucessor)

Reescrever ADR-017 § Limitações e remover Alternativa (f), tornando ADR-017 a fonte única.

Descartado:

- **Pureza semântica sobre churn.** ADR-017 documenta a decisão original com rationale específica (over-reach); reescrever apaga a trajetória editorial. ADR sucessor parcial preserva ambos os contextos e nomeia a inversão explicitamente.
- Convenção do toolkit (ADR-025 sobre ADR-005, ADR-026 sobre ADR-011): refinamento de critério documentado → ADR sucessor parcial.

### (d) Cutucada centralizada em hook PreToolUse / PostToolUse

Mover o probe e a emissão para hook que dispara em todo Edit/Write, fora das skills.

Descartado:

- Hooks emitem efeito via exit code (bloqueio) ou passam silentes — não emitem texto user-facing no relatório do assistant.
- Acopla descoberta a tool calls específicos (Edit/Write), perdendo cobertura de skills que terminam sem editar arquivos (`/next` quando não há candidatos).
- Adiciona ponto único de manutenção fora da convenção editorial das 5 skills, sem ganho real frente à duplicação de 1 parágrafo.

## Gatilhos de revisão

- **6ª skill com `roles.required` aparecer** (dobrar de 10 sites para 12+) — herdar e recalibrar o gatilho de ADR-017 § Gatilhos linha 161 ("5ª skill"), cuja aritmética foi escrita quando o universo era 4 skills. Pós-`/draft-idea` (ADR-027), o estado atual já é 5 skills × 2 strings = 10 sites; "5ª skill" como rótulo literal disparou-se com o próprio ADR-029. Reabrir ambos os ADRs simultaneamente para considerar helper compartilhado (alternativa (g) de ADR-017) ou herança mecânica quando o universo dobrar para 12+ sites.
- **Operador reporta confusão entre string-A e string-B** — drift de leitura, redação ambígua, ou ordem editorial nas SKILLs piora a interpretação. Reabrir para unificar via convenção mais explícita.
- **Mudança em ADR-016 / `/init-config` step 1 sobre criação automática de CLAUDE.md** — se o toolkit passar a criar CLAUDE.md em algum cenário, string-B precisa reconsiderar redação ("crie o arquivo" pode virar "configure").
- **Operador em consumer real ignora string-B em 3+ sessões consecutivas** sem rodar `/init-config` — sinal de que a redação ou o sinal não estão funcionando; reabrir para iterar.
