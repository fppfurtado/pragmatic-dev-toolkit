# Plano — Recusar cross-mode `backlog: local + plans_dir: canonical` no `/init-config`

## Contexto

Implementação de [ADR-025](../decisions/ADR-025-recusar-cross-mode-backlog-local-init-config.md), sucessor parcial de [ADR-005](../decisions/ADR-005-modo-local-gitignored-roles.md). Endurece mecanicamente a 4ª combinação cross-papel `backlog × plans_dir` (combinação `backlog: local + plans_dir: canonical`), que era coberta defensivamente por branches edge em 3 SKILLs após ADR-005 mas documentada como "fricção" em § Limitações.

H_arch é o último item structural do roadmap `docs/audits/runs/2026-05-12-execution-roadmap.md` (Diferida). Operador reabriu sem evidência empírica, absorvendo o trade-off de YAGNI per memory `feedback_adr_threshold_doctrine`.

**ADRs candidatos:** ADR-005 (decisão base — modo local per-papel); ADR-025 (este ADR sucessor parcial); ADR-016 (referência para distinguir categoria editorial — recusa de input próprio do step 3 vs recusa de política organizacional externa, contraste em ADR-025 § "Categoria editorial vs ADR-016"); ADR-018 (precedente de "não aplica retroativamente em consumers em upgrade", referência para escopo do check defensivo).

## Resumo da mudança

4 blocos doc-only consolidando ADR-025 em mecânica concreta:

1. **Bloco 1** — `/init-config` step 3 ganha detecção + recusa pré-gravação da combinação `paths.backlog: local + paths.plans_dir: canonical`. Postura editorial não-reparativa (parar com diagnóstico, não re-perguntar via enum).
2. **Bloco 2** — `/triage` step 1 ganha check defensivo após resolver `backlog` e `plans_dir`; step 4 sub-fluxo "Papel em modo local" remove o bullet específico da combinação inválida (passa a ter 3 bullets em vez de 4). Defensividade assimétrica per finding #4 do design-reviewer absorvido (operador escolheu opção (b) — check só em `/triage` step 1, não em `/run-plan`).
3. **Bloco 3** — `/run-plan §3.4` remove "Caso especial cross-mode" (limpeza editorial pura — combinação não chega aqui após Blocos 1+2).
4. **Bloco 4** — ADR-005 § Limitações ganha parágrafo de cross-ref para ADR-025 (texto literal especificado em ADR-025 § Decisão mecânica step 3).

Bundle homogêneo doc-only — `doc-reviewer` em todos. Sem ADR no caminho (ADR-025 já criado pré-plano via `/new-adr`).

## Arquivos a alterar

### Bloco 1 — `/init-config` step 3 detecta + recusa combinação inválida {reviewer: doc}

- `skills/init-config/SKILL.md` step 3: após coletar as 4 respostas via `AskUserQuestion` agrupado, **antes** de prosseguir para step 4 (compor e gravar YAML), adicionar verificação:

  - Detectar: `paths.backlog: local` AND `paths.plans_dir: canonical` (canonical = operador escolheu `Canonical` OR omitiu/manteve default).
  - Combinação detectada → parar com mensagem textual literal:

    > Combinação `backlog: local + plans_dir: canonical` recusada (ADR-025). `**Linha do backlog:**` viraria mensageiro de texto privado para plano público — semanticamente incoerente. Re-execute `/init-config` escolhendo uma das combinações suportadas: `ambos canonical` (default — registro coletivo), `ambos local` (uso individual), `backlog canonical + plans_dir local` (registro coletivo + planos privados).

  - Sem `AskUserQuestion` de re-prompt (postura editorial não-reparativa per ADR-016 + ADR-025 § Mecânica step 1).

- `skills/init-config/SKILL.md` `## O que NÃO fazer`: bullet novo capturando **tentação editorial não-óbvia** (per critério em CLAUDE.md → "Editing conventions" — recusa mecânica do step 3 já existe; o que o bullet documenta é a tentação futura de relaxar a recusa):

  - `**Não acomodar cross-mode `backlog: local + plans_dir: canonical` via warning, re-prompt ou cobertura defensiva** (ADR-025) — recusa hard é o ponto; "amaciar" a recusa em futura edição re-introduz leak de texto privado para plano público.

### Bloco 2 — `/triage` step 1 check defensivo + step 4 remoção do bullet cross-mode {reviewer: doc}

- `skills/triage/SKILL.md` step 1 (Carregar contexto mínimo): após sub-passos 3 (`backlog`) e 5 (`decisions_dir`), antes de "Não ler código aqui...", adicionar paragrafo final com mensagem **micro-adaptada para o ponto-de-uso** (vocativo apropriado a `/triage` em vez do "re-execute /init-config" do step 3 do próprio `/init-config` — semântica idêntica, fricção vocativa eliminada per finding #2 do design-reviewer absorvido):

  > **Pre-condição cross-mode (ADR-025).** Após resolver `backlog` e `plans_dir`, se a combinação for `backlog` em modo `local` AND `plans_dir` em modo canonical, parar com mensagem:
  >
  > > Combinação `backlog: local + plans_dir: canonical` recusada (ADR-025). `**Linha do backlog:**` viraria mensageiro de texto privado para plano público — semanticamente incoerente. Rode `/init-config` para corrigir o bloco config antes de continuar com `/triage`. Combinações suportadas: `ambos canonical`, `ambos local`, `backlog canonical + plans_dir local`.
  >
  > Demais combinações seguem normalmente.

- `skills/triage/SKILL.md` step 4 → "Papel em modo `local`" sub-fluxo: remover o bullet específico `backlog local + plans_dir canonical` (4 bullets → 3) + adicionar **rodapé explicativo** ao final do sub-fluxo per finding #4 do design-reviewer (leitor que cair na seção sem ter lido ADR-025 ganha link direto, evitando reconstrução de histórico). Estado-alvo do sub-fluxo:

  ```
  - **Papel em modo `local`:** linha gravada em `.claude/local/BACKLOG.md`. `**Linha do backlog:**` no plano:
    - Ambos `backlog` e `plans_dir` em modo `local`: linha presente (matching textual entre arquivos locais).
    - `backlog` canonical + `plans_dir` local: linha presente no plano local (não vaza para git).
    - Ambos canonical: caso default.

  Combinação `backlog: local + plans_dir: canonical` recusada upstream por [ADR-025](../../docs/decisions/ADR-025-recusar-cross-mode-backlog-local-init-config.md) (`/init-config` step 3 + `/triage` step 1) — não ocorre.
  ```

### Bloco 3 — `/run-plan §3.4` remove "Caso especial cross-mode" {reviewer: doc}

- `skills/run-plan/SKILL.md` §3.4 (Registro em Concluídos): remover a sentença final começando com "Caso especial cross-mode: se `**Linha do backlog:**` foi omitido pelo /triage (`backlog: local` + `plans_dir: canonical`...)". Mantém o restante do §3.4 intacto (modo `local` simétrico — `paths.backlog: local` com matching textual idêntico ao caso canonical, e mensagem de commit não-referenciar). Sem check defensivo adicional aqui per decisão do operador (opção (b) — só `/triage` cobre legacy).

### Bloco 4 — ADR-005 § Limitações ganha cross-ref para ADR-025 {reviewer: doc}

- `docs/decisions/ADR-005-modo-local-gitignored-roles.md` § Limitações: após o bullet existente "Modo `local` não interopera com canonical... Por design: simplicidade vence flexibilidade.", acrescentar parágrafo literal:

  > Estendido por [ADR-025](ADR-025-recusar-cross-mode-backlog-local-init-config.md): o princípio "simplicidade vence flexibilidade" aplicado ao par cross-papel `backlog × plans_dir` recusa mecanicamente a combinação `backlog: local + plans_dir: canonical` (leak de texto privado para plano público). Outras combinações cross-mode permanecem válidas.

  Status de ADR-005 preservado em `Proposto` per ADR-025 § Decisão step 3 (extensão semântica não obriga revisão do status).

## Verificação end-to-end

Pós-execução, confirmar via comandos concretos:

- **Bloco 1:** `grep -c "ADR-025" skills/init-config/SKILL.md` retorna ≥2 (mensagem de recusa + bullet em `## O que NÃO fazer`). `grep -c "backlog: local + plans_dir: canonical" skills/init-config/SKILL.md` retorna ≥1 (mensagem de recusa contém combinação literal).
- **Bloco 2:** `grep -c "ADR-025" skills/triage/SKILL.md` retorna ≥2 (check defensivo em step 1 + rodapé do sub-fluxo step 4). `awk '/Papel em modo .local./,/Ambos canonical: caso default/' skills/triage/SKILL.md | grep -c "omitir.*Linha do backlog"` retorna 0 (bullet original do step 4 sub-fluxo removido — grep ancorado no contexto do sub-fluxo evita falso-positivo da mensagem de recusa no step 1). Sub-fluxo "Papel em modo `local`" tem exatamente 3 bullets + 1 rodapé explicativo (verificar via `awk '/Papel em modo .local./,/recusada upstream por/' skills/triage/SKILL.md | grep -c '^  -'`).
- **Bloco 3:** `grep -c "Caso especial cross-mode" skills/run-plan/SKILL.md` retorna 0.
- **Bloco 4:** `grep -c "Estendido por.*ADR-025" docs/decisions/ADR-005-modo-local-gitignored-roles.md` retorna 1. ADR-005 § Limitações expandido sem alterar Status (`grep "Status: Proposto" docs/decisions/ADR-005-modo-local-gitignored-roles.md` retorna 1).
- **Holístico:** `grep -rn "backlog. local + plans_dir. canonical\|backlog local + plans_dir canonical" docs/ skills/ agents/ CLAUDE.md` lista apenas: (a) mensagem de recusa em `/init-config` step 3, (b) bullet do `## O que NÃO fazer` em `/init-config`, (c) check defensivo de `/triage` step 1, (d) referências em ADR-025 e ADR-005. Sem outras ocorrências.

Sem `test_command` aplicável (toolkit sem suite per `<!-- pragmatic-toolkit:config -->`); verificação end-to-end é textual.

## Verificação manual

Smoke-test em consumer fresh (sem bloco `pragmatic-toolkit:config` declarado) pós-merge:

1. **Cenário Recusa (entrada via "bloco ausente").** Rodar `/init-config` em projeto sem CLAUDE.md config. Responder enum agrupado escolhendo `Local` para `Backlog` e `Canonical` para `Plans`. Confirmar: skill para imediatamente com mensagem citando ADR-025; bloco YAML **não** é gravado em CLAUDE.md.

1b. **Cenário Recusa (entrada via "Editar bloco existente").** Em projeto com bloco config válido pré-existente (`paths.plans_dir: local` por exemplo), rodar `/init-config` e escolher `Editar` no enum do step 2. No enum agrupado do step 3, responder `Local` para Backlog e `Canonical` para Plans. Confirmar: mesma mensagem de recusa; bloco YAML pré-existente **não** é tocado (postura editorial não-reparativa).
2. **Cenário Aceitação simétrica.** Re-rodar `/init-config`. Responder `Canonical` para Backlog e `Local` para Plans. Confirmar: skill prossegue normalmente; bloco YAML gravado com `paths.plans_dir: local` (backlog ausente = canonical).
3. **Cenário Legacy.** Editar manualmente o CLAUDE.md introduzindo combinação inválida (`paths.backlog: local + paths.plans_dir: canonical` ou equivalente com canonical omitido). Rodar `/triage <intenção>`. Confirmar: skill para no step 1 com mensagem idêntica ao step 3 de `/init-config`. Resetar via `git checkout CLAUDE.md` pós-teste.

## Notas operacionais

- **Ordem dos blocos**: 1 (init-config recusa) → 2 (triage check + bullet remove) → 3 (run-plan limpeza) → 4 (ADR-005 cross-ref). Ordem reflete fluxo de dados (init-config grava → triage lê → run-plan executa) + ADR fechando.
- **Sem `## Pendências de validação`** — todos os cenários cabem em `## Verificação manual` acima.
- **Pós-merge:** atualizar `docs/audits/runs/2026-05-12-execution-roadmap.md` marcando H_arch `[x]` + nota de absorção do trade-off de YAGNI sem evidência empírica + link a PR; ADR-025 entra na lista de ADRs do toolkit (linha do BACKLOG `## Concluídos` registra ADR-025 + plano).
- **Onda 4 totalmente shippada após este plano.** F_arch já shippado via commit `066e1ae`; H_arch fecha o último item structural. Roadmap 2026-05-12 totalmente cumprido — único item remanescente seria H_arch como diferido, agora endereçado.
- **Defensividade assimétrica `/triage` step 1 sem espelho em `/run-plan`:** decisão consciente per finding #4 do design-reviewer em ADR-025. Operador escolheu opção intermediária (b) — pega legacy no `/triage` (única porta de entrada normal); plano fora-do-`/triage` é fora-do-escopo. Espelha espírito de ADR-018 § Limitações sem aceitar leak silente.
