# ADR-025: Recusar cross-mode `backlog: local + plans_dir: canonical` no `/init-config`

**Data:** 2026-05-12
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-005](ADR-005-modo-local-gitignored-roles.md) — modo local-gitignored para roles. § Limitações documentou *"Modo `local` não interopera com canonical — operador não pode ter ADRs versionados E ADRs locais no mesmo projeto sem fricção. Por design: simplicidade vence flexibilidade."* — escopo original cobria **canonical+local no mesmo papel** (ex.: `decisions_dir` canonical convivendo com ADRs locais). ADR-025 **estende semanticamente o mesmo princípio** ("simplicidade vence flexibilidade") para escopo adjacente — leak cross-papel entre `backlog` em modo `local` e `plans_dir` em modo canonical via `**Linha do backlog:**`. Não é endurecimento literal do texto de ADR-005:85, é aplicação do princípio subjacente em cenário emergente.

## Contexto

ADR-005 estabeleceu modo `local` per-papel para `decisions_dir`, `backlog`, `plans_dir`. As 4 combinações `backlog × plans_dir`:

| `backlog` | `plans_dir` | Comportamento | Status |
|---|---|---|---|
| canonical | canonical | Caso default — `**Linha do backlog:**` no plano alimenta `/run-plan` para transição em `BACKLOG.md`. | OK |
| local | local | Matching textual entre arquivos locais — `**Linha do backlog:**` presente. | OK |
| canonical | local | Plano local lê backlog canonical; linha presente no plano local sem vazar para git. | OK |
| **local** | **canonical** | **Problemático:** `**Linha do backlog:**` precisa ser omitido (texto local não pode vazar para plano commitado); `/run-plan §3.4` tem "Caso especial cross-mode" pulando transição automática e instruindo operador a mover manualmente em `.claude/local/BACKLOG.md`. | **Fricção documentada** |

A 4ª combinação cria branches edge cross-skill:

- `/triage` step 4 (modo `local` sub-bullet): documenta omissão de `**Linha do backlog:**` no caso cruzado.
- `/run-plan §3.4` (Registro em Concluídos): "Caso especial cross-mode" desvia do fluxo padrão de movimentação `## Próximos` → `## Concluídos`.

Não há evidência empírica de uso intencional dessa combinação. Combinações naturais que operador adota deliberadamente: `ambos canonical` (compartilhamento total) ou `ambos local` (uso individual completo). Cross-mode `backlog: local + plans_dir: canonical` seria uso anômalo — estado curatorial privado fundamentando registro de mudança público é **semanticamente incoerente**: linha registrada em backlog privado motiva plano público que outros leem sem ver a linha.

ADR-005 reconheceu a fricção mas implementou cobertura defensiva nas skills consumidoras em vez de recusar a combinação. Cobertura mascara a incoerência semântica e mantém ~10 linhas de prosa edge cross-skill (3 SKILLs distintas).

## Decisão

`/init-config` step 3 (perguntas per role) **detecta tentativa de gravar `paths.backlog: local + paths.plans_dir: canonical` e recusa** antes de gravar o bloco. Recusa **assimétrica** — apenas essa direção; a combinação `backlog: canonical + plans_dir: local` permanece válida (sem leak de texto local para artefato canonical commitado).

### Mecânica

1. **Detecção em `/init-config` step 3 → step 4.** Após coletar respostas per role, antes da composição do bloco, verificar combinação `paths.backlog: local` AND `paths.plans_dir: canonical` (canonical = omitido OR explicitamente declarado canonical). Combinação detectada → parar com diagnóstico textual:

   > Combinação `backlog: local + plans_dir: canonical` recusada (ADR-025). `**Linha do backlog:**` viraria mensageiro de texto privado para plano público — semanticamente incoerente. Re-execute `/init-config` escolhendo uma das combinações suportadas: `ambos canonical` (default — registro coletivo), `ambos local` (uso individual), `backlog canonical + plans_dir local` (registro coletivo + planos privados).

   Postura editorial não-reparativa — operador re-executa com escolhas corrigidas. Sem re-prompt automático no enum (`AskUserQuestion`), mantendo coerência com outras recusas em `/init-config` (CLAUDE.md ausente, bloco malformado per ADR-016 + spec atual).

   **Categoria editorial vs ADR-016.** ADR-016 estabeleceu postura "plugin não prescreve workaround manual nem oferece caminho alternativo" para CLAUDE.md gitignored (política organizacional externa). ADR-025 prescreve re-execução com escolhas corrigidas — escopo distinto: aqui o plugin recusa input próprio (do step 3 imediatamente anterior, no mesmo fluxo) e instrui correção via re-invocação, não recusa política do consumer. Mesmo princípio editorial não-reparativo, categorias de input diferentes.

2. **Skills consumidoras — limpeza editorial.** `/triage` step 4 e `/run-plan §3.4` removem o branch dedicado à 4ª combinação. Para bloco legacy com a combinação inválida (consumer que adotou pré-ADR-025), check defensivo é adicionado **apenas em `/triage` step 1** (Carregar contexto mínimo, após resolver `backlog` e `plans_dir`): detectar combinação inválida → parar com mensagem **mesma semântica do step 3 de `/init-config`, vocativo adaptado ao ponto-de-uso** ("Rode `/init-config` para corrigir o bloco config antes de continuar com `/triage`" em vez de "Re-execute `/init-config`"). Adaptação evita fricção semântica (operador chamou `/triage`, não `/init-config`); a recomendação acionável muda mas o diagnóstico textual sobre a combinação é idêntico.

   **Decisão de escopo do check defensivo.** `/triage` é a única porta de entrada para criação de plano canonical no fluxo normal — pegar lá previne propagação. `/run-plan` **não** recebe check defensivo: plano só chega ao `/run-plan` se foi produzido por `/triage` (que pega) ou foi escrito à mão (caso fora-de-escopo do fluxo guiado). Espelha o espírito de ADR-018 § Limitações ("não aplica retroativamente em consumers em upgrade") sem aceitar leak silente em consumer legacy — compromisso entre robustez e YAGNI per design-reviewer durante revisão deste ADR.

3. **ADR-005 cross-ref.** Acrescentar parágrafo ao final de ADR-005 § Limitações (após bullet "Modo `local` não interopera..."), texto literal:

   > Estendido por [ADR-025](ADR-025-recusar-cross-mode-backlog-local-init-config.md): o princípio "simplicidade vence flexibilidade" aplicado ao par cross-papel `backlog × plans_dir` recusa mecanicamente a combinação `backlog: local + plans_dir: canonical` (leak de texto privado para plano público). Outras combinações cross-mode permanecem válidas.

   Status de ADR-005 preservado em `Proposto` — extensão semântica não obriga revisão do status; sucessor parcial via cross-ref textual basta.

### Razões

- **Alinha código com princípio subjacente de ADR-005:** ADR-005 documentou fricção sem cobertura mecânica; ADR-025 aplica o princípio "simplicidade vence flexibilidade" ao escopo cross-papel adjacente.
- **Reduz superfície de drift cross-skill:** 3 SKILLs (`/init-config`, `/triage`, `/run-plan`) deixam de ter branch específico para a combinação edge. Menos prosa para manter consistente.
- **Recusa precoce no setup, não tardia na execução:** operador descobre na configuração inicial (antes de adotar fluxo), não durante uso real do `/run-plan`.
- **Direção do leak é o critério geral:** texto privado → artefato público é semanticamente incoerente; leitor privado consumindo registro público é normal. ADR-025 aplica esse critério ao par `backlog × plans_dir`. Aplicações análogas em outros pares de papéis devem usar a mesma régua. **Assimétrica por design:** apenas `backlog: local + plans_dir: canonical` é problemática; a simétrica `backlog: canonical + plans_dir: local` funciona normalmente.

## Consequências

### Benefícios

- ~10 linhas de prosa edge removidas cross-skill (`/triage` step 4 sub-bullet + `/run-plan §3.4` "Caso especial cross-mode").
- Setup `/init-config` falha fast em combinação semanticamente incoerente.
- Mecânica passa a refletir limitação documentada de ADR-005 § Limitações.
- Skills consumidoras (`/triage`, `/run-plan`) ficam mais coesas — sem branch específico para caso edge raro.

### Trade-offs

- **Regressão de cobertura para consumer hipotético que adotou cross-mode deliberadamente.** Sem evidência empírica desse consumer — operador absorveu o trade-off pós-finding de YAGNI (gatilho original do diferimento desta proposta no roadmap `docs/audits/runs/2026-05-12-execution-roadmap.md`, item H_arch: *"só com evidência empírica de uso não-intencional"*). Mitigação: skills consumidoras param com mensagem clara apontando `/init-config`; operador escolhe entre uniformizar para `ambos local`, `ambos canonical`, ou `backlog canonical + plans_dir local`.
- Endurece doutrina de ADR-005 sem trilho de escape — operador com use case legítimo de cross-mode perde a opção. Trilho de escape via revogação deste ADR.

### Limitações

- Recusa não diferencia "operador acabou de configurar errado" vs "operador editou manualmente o bloco para tentar cross-mode" — mensagem genérica cobre ambos casos.
- `/triage` step 1 herda check defensivo (~3 linhas) — surface adicional, mas marginal vs ~10 linhas removidas em `/triage` step 4 + `/run-plan §3.4`. `/run-plan` sem check (plano fora-do-`/triage` é fora-de-escopo).

## Alternativas consideradas

### Manter status quo

Cobertura defensiva atual funciona — `/run-plan §3.4` informa operador e instrui movimentação manual; `/triage` step 4 omite `**Linha do backlog:**`. Mantém flexibilidade hipotética para o caso cross-mode. **Rejeitada:** mascara incoerência semântica documentada em ADR-005 § Limitações; ~10 linhas de prosa edge cross-skill sem ganho funcional real.

### Recusar simetricamente ambas as combinações cross-mode

Recusar tanto `backlog: local + plans_dir: canonical` quanto `backlog: canonical + plans_dir: local`. **Rejeitada:** segunda combinação é funcionalmente OK (plano local lê backlog canonical sem leak de texto privado). Simetria seria perda gratuita de flexibilidade.

### Endurecer via warning em vez de recusa

`/init-config` emite warning na configuração e segue gravando; skills consumidoras mantêm cobertura defensiva. **Rejeitada:** warning ignorado é trade-off pior que prosa-cross-skill removida — operador segue para cobertura edge sem corrigir setup. Recusa força correção precoce, alinhada com postura editorial não-reparativa do `/init-config`.

## Gatilhos de revisão

- 1+ consumer reportar use case real para `backlog: local + plans_dir: canonical` com justificativa concreta de fluxo → reabrir.
- ADR-005 ser revogado/substituído por reformulação geral do modo local → revisar escopo deste ADR.
- Skill nova introduzir interação `backlog × plans_dir` com semântica diferente → revisar.
- Recusa gerar atrito empírico maior que cobertura defensiva atual (operadores reclamando da rigidez) → reabrir trade-off "recusa hard vs warning + cobertura".

## Implementação

Commits do plano `recusar-cross-mode-backlog-local-init-config` que executou este ADR:

(A preencher após execução via `/run-plan`.)
