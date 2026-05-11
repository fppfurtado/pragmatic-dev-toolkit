# ADR-017: Cutucada uniforme em skills para descoberta de configuração ausente

**Data:** 2026-05-11
**Status:** Aceito

## Origem

- **Investigação:** `/triage` 2026-05-11 do item "wizard de configuração inicial dos papéis" (linha 6 do BACKLOG). Plano inicial em `docs/plans/init-config-wizard.md` (descartado) propôs cutucada com redação idêntica em **todas as 7 skills** sugerindo `/init-config` quando o bloco `<!-- pragmatic-toolkit:config -->` está ausente do `CLAUDE.md` do consumer. Primeira rodada de `@design-reviewer` flagou (finding #2) que a decisão é estrutural duradoura, comparável a [ADR-011](ADR-011-wiring-design-reviewer-automatico.md) (wiring de design-reviewer em 2 skills), e merece formalização própria. Segunda rodada (sobre o draft inicial deste ADR) trouxe 4 refinamentos críticos absorvidos abaixo: universo correto é 4 skills (não 7), mecanismo de detecção precisa ser concreto, herança é editorial (não automática), dedup precisa nomear mecanismo análogo a [ADR-010](ADR-010-instrumentacao-progresso-skills-multi-passo.md).

## Contexto

O bloco `<!-- pragmatic-toolkit:config -->` é o mecanismo declarativo do consumer para informar variantes do path contract (ver `CLAUDE.md` → "Pragmatic Toolkit"). Quando ausente, o operador atinge o `Resolution protocol` (`CLAUDE.md` linhas 45-54) caindo em **passo 3 (ask)** para cada role required que precise resolver. O passo 4 do mesmo protocol oferece **memorização one-shot per role** ao final, registrando a resposta no bloco — mecanismo **reativo** (registra conforme skills perguntam).

O atrito observado no onboarding do plugin no projeto Java PJe (2026-05-11) revelou que mesmo a memorização per role tem alto custo de descoberta:

- Operador novo não sabe da existência do bloco.
- Mesmo descobrindo, registrar 4-6 roles via memorização per role exige rodar 4-6 skills primeiro (cada uma perguntando 1 role).
- Resultado no PJe: ~30 min de atrito + composição manual do YAML pelo operador (não pela memorização).

A direção complementar é uma **skill proativa** (`/init-config`, escopo do plano de implementação em curso, fora deste ADR). Mas existir só não basta — operador precisa **descobrir que ela existe**. Daí a necessidade de cutucada das skills existentes sugerindo `/init-config` quando detectam ausência do bloco.

**Recorte do universo:** das 7 skills atuais do plugin, apenas **4** declaram `roles.required` no frontmatter e atingem o passo 3 do Resolution protocol como fluxo normal:

| Skill | `roles.required` | Comportamento sem bloco |
|---|---|---|
| `/triage` | `backlog` (em alguns caminhos) | Cai no passo 3 → ask |
| `/new-adr` | `decisions_dir` | Cai no passo 3 → canonical creation track |
| `/run-plan` | `plans_dir`, `test_command` (condicional) | Cai no passo 3 → capture+stop ou ask |
| `/next` | `backlog` | Inform-and-stop track |

As outras 3 skills (`/debug`, `/gen-tests`, `/release`) declaram apenas `roles.informational`. Por definição, **informational ausente faz skill prosseguir silente** (CLAUDE.md → "Required vs informational"), o que significa que essas skills **não consultam o passo 3** para esses roles. Aplicar cutucada nessas skills seria emitir sem sinal de que algo está faltando do ponto de vista da skill corrente — ruído sem informação.

Decisões a tomar para a cutucada virar política durável:

1. **Forma da cutucada** — string idêntica nas 4 skills vs. variação per-skill vs. cutucada centralizada.
2. **Mecanismo de gating** — como cada skill detecta "marker ausente" sem replicar lógica.
3. **Frequência** — dedup per invocação, per sessão, ou nenhum.
4. **Skills futuras** — skill nova nasce com cutucada automática ou exige adição editorial.

## Decisão

**Escopo:** as 4 skills com `roles.required` (`/triage`, `/new-adr`, `/run-plan`, `/next`) emitem cutucada uniforme ao final do relatório quando satisfazem **três condições simultaneamente**:

1. `CLAUDE.md` **existe** no consumer.
2. A skill detecta que o bloco `<!-- pragmatic-toolkit:config -->` **não está presente** em `CLAUDE.md`. Mecanismo concreto: cada skill executa **um probe próprio** — `grep -q '<!-- pragmatic-toolkit:config -->' CLAUDE.md` (ou equivalente em prosa do SKILL.md). Aceita-se a duplicação de uma linha em 4 skills como custo menor que introduzir helper compartilhado (YAGNI sobre abstração). Não há ponto único — cada skill é responsável pelo seu próprio probe.
3. **Cutucada idêntica não foi emitida nesta sessão CC**. Mecanismo de dedup: antes de emitir, skill observa se a string canonical da cutucada já aparece no **contexto visível** da conversa CC corrente (mensagens prévias do assistant que chegaram não-compressas até esta invocação). Match → suprime. Sem match → emite. Granularidade conversation-scoped, alinhada com [ADR-010](ADR-010-instrumentacao-progresso-skills-multi-passo.md) (state mecânico vive na sessão CC, não em git/forge). Sob context compression em sessões muito longas a cutucada pode reaparecer — aceito (ruído baixo, ≤1 linha por re-emissão).

**Forma da cutucada:** uma linha em texto, redação idêntica nas 4 skills (PT-BR, canonical do toolkit):

> `Dica: este projeto não declara o bloco `pragmatic-toolkit:config` no CLAUDE.md. Rode `/init-config` para configurar todos os papéis de uma vez.`

**Skills futuras com `roles.required`:** convenção registrada em CLAUDE.md (seção "Cutucada de descoberta" a ser adicionada na implementação) — autor de skill nova adiciona a cutucada manualmente seguindo a convenção. **Herança é editorial, não mecânica.** Skill nova que esqueça de aplicar não cutuca silenciosamente; mitigação: a seção em CLAUDE.md serve de checklist para autor da skill e referência para revisor humano ou `code-reviewer` que olhe o diff do SKILL.md novo. Sem garantia mecânica — é convenção sustentada por disciplina editorial.

Razões:

- **Discoverable.** Operador novo recebe sinal claro do caminho proativo (`/init-config`) sem precisar ler docs antes.
- **Uniforme.** Redação idêntica reduz cognitive load (operador vê a mesma frase em qualquer das 4 skills; reconhece imediatamente).
- **YAGNI sobre helper compartilhado.** 4 probes de 1 linha custam menos manutenção do que helper + 4 sites de invocação. Reabrir se 5ª skill aparecer e a duplicação incomodar.
- **Conversation-scoped per ADR-010.** Dedup via leitura do contexto visível da conversa CC alinha com a doutrina de "state mecânico vive na sessão"; sem persistência cross-session, sem dependência de variável externa, sem custo extra além do que o turn já paga para ler o prompt.
- **Análogo ao auto-gating dos hooks** (`docs/philosophy.md` → "Convenção de naming"): cutucada cala fora das condições de gating, sem flag de operador para desligar. Operador que ignora 4 vezes está sinalizando preferência por memorização reativa — plugin não argumenta de volta.
- **Compatível com memorização per role.** Passo 4 do Resolution protocol continua intacto — operador que prefere registrar reativamente per role faz isso normalmente; cutucada apenas oferece caminho proativo como alternativa.

## Consequências

### Benefícios

- Descoberta de `/init-config` sem custo de docs prévia.
- Uniformidade reduz fadiga visual e ambiguidade.
- Mecanismo concreto (cada skill faz seu probe + dedup via histórico CC) — implementador derivar código direto sem interpretação.
- Sem helper compartilhado novo — superfície de manutenção mínima.

### Trade-offs

- **Duplicação de 1 linha de probe em 4 skills.** Mudança no marker (alias, renomeação) requer atualizar 4 lugares. Aceito — bloco YAGNI sobre abstração; o marker é estável desde a introdução do schema.
- **Acoplamento textual de redação:** mudança na string da cutucada requer atualizar 4 sites + a seção em CLAUDE.md. Aceito — preferível a redação divergente.
- **Herança editorial (não mecânica).** Skill nova com `roles.required` que esqueça de emitir a cutucada falha silenciosamente. Mitigação é editorial — checklist em CLAUDE.md sustentado pela disciplina do autor e do revisor.
- **Cutucada pode ser ignorada.** Operador que vê a linha 4 vezes em sessões consecutivas e não roda `/init-config` está sinalizando preferência por memorização reativa — aceito.

### Limitações

- Cutucada não cobre o caso `CLAUDE.md` **ausente** — operador que opta por não ter CLAUDE.md (raro mas válido) não recebe cutucada nem memorização; plugin opera no modo "tudo via passo 3 do Resolution protocol, ask-on-demand". Decisão consciente, rebatida em § Alternativas.
- Cutucada não cobre o caso `CLAUDE.md` **gitignored** — operador recebe cutucada mas a ação proposta (`/init-config`) falha por [ADR-016](ADR-016-manter-block-gitignored-scripts-no-consumer.md). Tratamento desse sub-caso é responsabilidade do `/init-config` em si; a direção doutrinária (per ADR-016) é orientar o consumer a rever o `.gitignore`, não acomodar o pattern no plugin.
- Sessão de conversa CC é o escopo de dedup — operador em duas sessões CC vê duas cutucadas (uma por sessão). Aceito; sessão é a granularidade natural alinhada com ADR-010.
- Sob context compression em sessões muito longas, a string canonical da cutucada pode sair da janela visível e a skill emiti-la novamente. Aceito — custo do mecanismo conversation-scoped sem persistência; alternativa (registro estruturado via Task per ADR-010) está em § Gatilhos como reabertura possível.

## Alternativas consideradas

### (a) Cutucada per role (cada skill que perguntou um role sugere `/init-config`)

Skill que invoca o passo 3 do Resolution protocol perguntando um role específico sugere `/init-config` na mesma resposta da pergunta. Granularidade fina vinculada ao gap concreto.

Descartado:

- Sobreposição com memorização one-shot do passo 4 — operador já recebe oferta de registrar **aquele role**. Adicionar cutucada de `/init-config` mid-flow confunde ("registrar agora ou rodar wizard depois?").
- Ruído alto — cada skill pode perguntar 1-3 roles; cutucada por pergunta multiplica.
- Acoplamento mais profundo entre skill e Resolution protocol — cutucada teria que ser inserida em cada ponto de `AskUserQuestion`.

### (b) Cutucada centralizada em apenas `/triage`

Como `/triage` é entry point comum, concentrar a cutucada só nele.

Descartado:

- Perde descoberta para operador que invoca `/new-adr`, `/run-plan`, `/next` diretamente — caminhos legítimos sem passar por `/triage`.
- Cutucada em 4 skills custa pouco a mais e cobre todos os entry points relevantes.

### (c) Variação per-skill (redação adaptada ao contexto)

Cada skill formula a cutucada usando o role que acabou de perguntar.

Descartado:

- Custo editorial alto (4+ redações para manter coerentes).
- Reforça sobreposição com memorização per role (mesma armadilha de alternativa (a)).
- Uniformidade reduz mais cognitive load do que a personalização adiciona.

### (d) Sem cutucada (apenas memorização per role + docs)

Status quo + uma menção em `docs/install.md`. Operador descobre `/init-config` lendo docs.

Descartado:

- Memorização per role é reativa — não destrava o atrito de onboarding inicial (PJe levou ~30 min antes de qualquer skill rodar para começar a memorizar).
- Docs como caminho único de descoberta tem fricção alta.

### (e) Notificação via mecanismo nativo do Claude Code

Toast, banner, ou outro hook nativo do harness.

Descartado:

- Mecanismo não existe como API estável do Claude Code para plugins.
- Mesmo se existisse, criaria dependência da plataforma para um sinal que pode viver na própria prosa do relatório.

### (f) Cutucada também quando `CLAUDE.md` está ausente

Cutucar para o operador criar `CLAUDE.md` quando ausente, sugerindo `/init-config` em seguida.

Descartado:

- Over-reach do plugin sobre estrutura do consumer. `CLAUDE.md` tem propósito mais amplo que o bloco config (instruções gerais ao Claude Code) — sugerir criação só para o plugin é estranho.
- Paralelo com gate `Gitignore` de [ADR-005](ADR-005-modo-local-gitignored-roles.md) não se aplica: lá o plugin já decidiu usar `.claude/local/` e precisa garantir gitignore; aqui o plugin estaria inferindo necessidade do operador sem sinal claro.
- Operador que rodou `/init-config` deliberadamente recebe orientação clara dentro do próprio wizard (escopo do plano de implementação, não desta política).

### (g) Helper compartilhado (`should_emit_init_config_hint()`)

Centralizar a detecção em ponto único (parágrafo em CLAUDE.md descrevendo a função + 4 skills citando "consulta `should_emit_init_config_hint()`").

Descartado:

- YAGNI — 4 sites × 1 linha de probe não justifica abstração com nome próprio.
- Helper como prosa em CLAUDE.md ainda exige cada skill citar/chamar — não há redução real de acoplamento, só indireção.
- Reabrir se 5ª skill com `roles.required` aparecer e a duplicação virar débito real.

## Gatilhos de revisão

- **≥2 operadores reportarem ruído** mesmo com dedup per session — sinal de que a cutucada precisa de mais dedup (per repo? per dia? per N invocações?). Reabrir com critério mecânico de redução.
- **Operador reporta cutucada esperada não aparecendo em skill nova** que declara `roles.required` — sinal independente de que herança editorial falhou; reabrir para considerar herança mecânica — reabrir alternativa (g), ou explorar caminhos novos como checklist em CI ou validador automático.
- **Operador reporta que `/init-config` não cobre o caso dele** mas a cutucada continua sugerindo — gap entre o que a cutucada promete e o que a skill entrega. Atualizar redação ou condicionar mais.
- **Mudança na convenção do marker** (alias, variantes, renomeação) — re-confirmar que probes em 4 skills foram atualizados; oportunidade de re-avaliar helper compartilhado.
- **5ª skill com `roles.required` aparecer** — reabrir para considerar abstração: alternativa (g) ou herança mecânica deixam de ser YAGNI quando 5 sites compartilham a mesma lógica.
- **Re-emissão da cutucada virar ruído frequente** por causa de context compression em sessões muito longas (gatilho prático: ≥3 reports de "vi a mesma cutucada várias vezes na mesma sessão") — considerar Task per ADR-010 (registro estruturado que sobreviva à compression em vez de leitura do contexto visível).
