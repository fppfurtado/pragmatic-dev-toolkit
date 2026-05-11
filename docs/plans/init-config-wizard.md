# Plano — Skill `/init-config` para wizard de configuração inicial dos papéis

## Contexto

**Linha do backlog:** plugin: wizard de configuração inicial dos papéis — gate único na primeira invocação de skill que toca `pragmatic-toolkit:config`, perguntando cada role (presente? canonical ou local?) e gravando no CLAUDE.md. Alternativa de descoberta para operadores que esquecem de editar o bloco YAML manualmente. Reavaliar se atrito real surgir.

Gatilho atendido pelo atrito real observado em 2026-05-11 no onboarding do plugin no projeto Java PJe (TJPA), registrado em `.claude/pragmatic-toolkit-validation.md` do PJe.

Trabalho de alinhamento fechado por dois ADRs **antes** deste plano:

- **[ADR-017](../decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md) (Aceito 2026-05-11)** — política de cutucada uniforme em 4 skills com `roles.required` (`/triage`, `/new-adr`, `/run-plan`, `/next`). Define escopo, gating (`CLAUDE.md` existe + marker ausente + dedup conversation-scoped via leitura do contexto visível), redação canonical, probe próprio per skill (YAGNI sobre helper compartilhado), herança editorial via seção em CLAUDE.md. Plano apenas materializa a política — não há decisão de cutucada a tomar.
- **[ADR-016](../decisions/ADR-016-manter-block-gitignored-scripts-no-consumer.md) (Aceito 2026-05-10)** — manter `block_gitignored.py` como está; consumer com pattern "arquivo gitignored como entrypoint" resolve via refatoração organizacional. Plano espelha a doutrina no cenário `CLAUDE.md` gitignored: a skill detecta e para com mensagem **orientando reconsideração da decisão organizacional**, não prescrevendo workaround manual.
- **[ADR-005](../decisions/ADR-005-modo-local-gitignored-roles.md)** — modo `local` ativável per role (`decisions_dir`/`backlog`/`plans_dir`) grava artefatos em `.claude/local/<role>/`. Interação não-trivial com `/init-config`: quando operador escolhe `local` para uma role, o gate `Gitignore` definido pelo ADR-005 dispara **na primeira escrita subsequente** sob `.claude/local/<role>/` (não dentro de `/init-config` — `/init-config` apenas grava no `CLAUDE.md`). Comportamento explícito documentado nos cenários de Verificação manual.

Decisões já tomadas:

- **Nome:** `/init-config` (verbo+artefato canonical do toolkit).
- **Disparo:** manual (`/init-config`) + cutucada uniforme nas 4 skills definida pelo ADR-017.
- **Escopo enxuto v1:** 4 roles com dor concreta — `decisions_dir`, `backlog`, `plans_dir` (aceitam local mode) + `test_command` (top-level). Informational roles (`product_direction`, `ubiquitous_language`, `design_notes`) e `version_files`/`changelog` ficam fora de v1 — operador edita manualmente quando relevante; reabrir se dor recorrente.
- **Sub-caso `CLAUDE.md` gitignored:** detectar via `git check-ignore -q CLAUDE.md`, parar; mensagem orienta reconsiderar `.gitignore` per ADR-016. Sem workaround prescrito.
- **Re-invocação:** `/init-config` re-roda editando bloco existente in-place. Memorização one-shot per role do Resolution protocol passo 4 (`CLAUDE.md` → "Resolution protocol") **só dispara quando o bloco config não cobre o role perguntado** — sem sobreposição.

## Resumo da mudança

Nova skill `/init-config` em `skills/init-config/SKILL.md` com workflow interativo:

1. **Probe estado do consumer.** Verifica `CLAUDE.md` existe (não cria; instrui operador se ausente). Se git repo, verifica `git check-ignore -q CLAUDE.md` — gitignored → para com mensagem orientando reconsiderar `.gitignore` per ADR-016. Não-git → pula probe gitignore, prossegue.
2. **Detecta bloco config.** `grep -q '<!-- pragmatic-toolkit:config -->' CLAUDE.md` — match → tenta parsear YAML adjacente. Parse OK → exibe bloco atual, oferece editar ou cancelar. **Parse falha / múltiplos markers / marker órfão sem YAML** → para com diagnóstico textual reportando linha e tipo de anomalia; **skill não reescreve, não funde, não toma o primeiro**. Operador resolve manualmente (paralelo com não-criar-CLAUDE.md no passo 1: postura editorial, não reparativa). Sem match → procede.
3. **Pergunta per role via `AskUserQuestion`** (cobertura v1 — 4 roles):
   - `decisions_dir`: enum `canonical (docs/decisions/)` (Recommended) / `local (.claude/local/decisions/)` / `Não usamos (null)`.
   - `backlog`: análogo (`canonical (BACKLOG.md)` / `local (.claude/local/BACKLOG.md)` / `null`).
   - `plans_dir`: análogo (`canonical (docs/plans/)` / `local (.claude/local/plans/)` / `null`).
   - `test_command`: probe automático stack-aware (`pom.xml`→`mvn test -DfailIfNoTests=false`, `pyproject.toml`→`uv run pytest -q --no-header` ou `python -m pytest -q --no-header`, `package.json`→`npm test`, `Makefile` com target `test`→`make test`). Propõe valor detectado; opções: `<valor> (Recommended)` / `Não declarar (null)`. Other → operador customiza.
4. **Compõe e grava** bloco YAML no `CLAUDE.md`. Bloco existente (cenário 2 com edit) → substitui in-place preservando marker. Sem bloco → cria seção `## Pragmatic Toolkit` no fim do arquivo com marker HTML + bloco YAML. Reporta path final.
5. **Cutucada de descoberta** nas 4 skills com `roles.required` (per ADR-017) — bloco do plano apenas wira (a política em si já está aceita).
6. **Documentação:** seção `## Cutucada de descoberta` em CLAUDE.md do toolkit registrando a convenção (escopo, gating, redação, herança editorial). Parágrafo em `docs/install.md` introduzindo `/init-config` como caminho recomendado de onboarding.

**Fora de escopo v1:**

- Informational roles e `version_files`/`changelog`.
- Probe stack-aware adicional (Gradle, Cargo, Cargo workspace, etc.) — entra conforme dor real.
- Migração de blocos legados (não há legacy; schema é estável).
- Wizard inverso (`/clear-config` ou similar).
- Cobertura de `block_gitignored` em paths além de `CLAUDE.md` (escopo é só o sub-caso documentado).

## Arquivos a alterar

### Bloco 1 — nova skill `/init-config` {reviewer: code}

- `skills/init-config/SKILL.md`: arquivo novo. Frontmatter com `name: init-config` + `description: ...` (português, canonical do toolkit). **Sem declaração `roles:`** — a skill **define** os roles do consumer, não os consome via Resolution protocol; não está sujeita ao protocolo nem à cutucada do ADR-017. Prosa em PT-BR descrevendo workflow dos passos 1-4 do Resumo, com:
  - Lógica de probe stack-aware para `test_command` (tabela marker→comando).
  - Tratamento do sub-caso `CLAUDE.md` gitignored com mensagem literal alinhada com ADR-016.
  - Seção `## O que NÃO fazer` listando guardas não-óbvias: "Não criar `CLAUDE.md`", "Não modificar `.gitignore` automaticamente", "Não estender escopo para roles fora de v1".

### Bloco 2 — cutucada wirada em 4 skills {reviewer: code}

Cada skill ganha a cutucada **no último parágrafo do passo final que reporta conclusão ao operador** — ponto canonical e uniforme. Para cada skill, esse passo é nomeado abaixo (referência aos SKILL.md atuais):

- `skills/triage/SKILL.md`: passo 6 (Reportar, propor commit e devolver controle) — inserção como último parágrafo do passo, após "Sugerir próximo passo".
- `skills/new-adr/SKILL.md`: passo 5 (Revisão pré-retorno) — inserção como último parágrafo do passo, após reportar findings do design-reviewer.
- `skills/run-plan/SKILL.md`: passo final de relatório de conclusão (pós-gate de validação manual) — inserção como último parágrafo do passo.
- `skills/next/SKILL.md`: passo final de relatório — inserção como último parágrafo do passo.

Redação canonical idêntica (per ADR-017):

> `Dica: este projeto não declara o bloco `pragmatic-toolkit:config` no CLAUDE.md. Rode `/init-config` para configurar todos os papéis de uma vez.`

Gating em cada SKILL (prosa idêntica, copy-paste): "Antes de emitir, verificar: (a) `CLAUDE.md` existe; (b) `grep -q '<!-- pragmatic-toolkit:config -->' CLAUDE.md` retorna não-zero (marker ausente); (c) string canonical da cutucada não aparece no contexto visível desta conversa CC. Todas as três → emitir 1 linha; caso contrário → suprimir."

### Bloco 3 — seção em CLAUDE.md + atualização docs/install.md {reviewer: doc}

- `CLAUDE.md` do toolkit: nova seção `## Cutucada de descoberta` registrando a convenção. Conteúdo: escopo (4 skills com `roles.required` enumeradas), gating (3 condições simultâneas), redação canonical (string literal), herança editorial (autor de skill nova com `roles.required` adiciona; checklist para revisor humano e `code-reviewer`). Referências cruzadas a ADR-017 e à skill `/init-config`.
- `docs/install.md`: 1 parágrafo após "Local install for iteration" introduzindo `/init-config` como caminho recomendado de onboarding (alternativa à edição manual do bloco config).

## Verificação end-to-end

Toolkit sem suite (`test_command: null` no próprio bloco config). Inspeção textual via comandos concretos:

1. `ls skills/init-config/SKILL.md` — arquivo existe.
2. `python3 -c "import yaml; print(yaml.safe_load(open('skills/init-config/SKILL.md').read().split('---')[1]))"` — frontmatter parseável; valida `name: init-config`.
3. `grep -c "Dica: este projeto não declara o bloco" skills/triage/SKILL.md skills/new-adr/SKILL.md skills/run-plan/SKILL.md skills/next/SKILL.md` — string canonical presente em 4 skills (1 ocorrência cada esperada).
4. `grep -c "Dica: este projeto não declara o bloco" skills/debug/SKILL.md skills/release/SKILL.md skills/gen-tests/SKILL.md` — string **ausente** nas 3 skills só-informational (0 ocorrência cada esperada).
5. `grep -n "Cutucada de descoberta" CLAUDE.md` — seção presente no CLAUDE.md do toolkit.
6. `grep -n "init-config" docs/install.md` — referência presente.

## Verificação manual

Skill nova com surface interativa (`AskUserQuestion`) — verificação manual obrigatória. Cenários enumerados:

1. **Greenfield (sem `CLAUDE.md`)** — `/init-config` em projeto novo sem `CLAUDE.md`. Esperado: skill para com mensagem orientando criar `CLAUDE.md` primeiro (plugin não cria).
2. **`CLAUDE.md` existe, bloco config ausente** — esperado: skill pergunta 4 roles via enum, propõe `test_command` baseado em probe, grava bloco em seção `## Pragmatic Toolkit` no fim do arquivo. Reporta path.
3. **`CLAUDE.md` com bloco config existente** — esperado: skill detecta marker, exibe configuração atual, oferece editar ou cancelar. Confirmar editar → substitui bloco in-place preservando marker.
4. **`CLAUDE.md` gitignored** (caso PJe) — esperado: skill detecta via `git check-ignore -q CLAUDE.md`, para com mensagem literal alinhada com ADR-016: orienta reconsiderar a decisão organizacional de gitignorar `CLAUDE.md` (artefato compartilhável por design). **Não prescreve workaround manual** (descomentar `.gitignore`) **nem oferece caminho alternativo no plugin** — operador resolve no consumer reconsiderando o gitignore, conforme doutrina ADR-016.
5. **Projeto não-git** (`git rev-parse --is-inside-work-tree` retorna não-zero) — esperado: skill pula probe de gitignore, prossegue normalmente.
6. **Probe `test_command` em projeto Maven** — projeto com `pom.xml`. Esperado: probe propõe `mvn test -DfailIfNoTests=false`. Operador edita via Other para incluir settings/profile.
7. **Probe `test_command` em projeto Python** — `pyproject.toml`. Esperado: propõe `uv run pytest -q --no-header` (ou `python -m pytest -q --no-header` se `uv` não está no PATH).
8. **Probe `test_command` em projeto Node** — `package.json`. Esperado: propõe `npm test`.
9. **Probe `test_command` em projeto com `Makefile` e target `test`** — esperado: propõe `make test`.
10. **Probe `test_command` em projeto sem manifest reconhecido** — esperado: opções somente `Não declarar (null) (Recommended)` + Other para valor customizado.
11. **Cutucada disparando em skill com `roles.required`** — após config block ausente, rodar `/triage` em projeto com `CLAUDE.md` mas sem bloco. Esperado: ao final do relatório, 1 linha sugerindo `/init-config`.
12. **Cutucada não disparando em skill só-informational** — rodar `/debug` (ou `/release`, `/gen-tests`) em projeto sem bloco config. Esperado: nenhuma cutucada (gate de ADR-017 escopo 4).
13. **Cutucada dedup-suprimida na sessão CC** — rodar `/triage` (cutuca), depois `/new-adr` na mesma sessão. Esperado: cutucada aparece 1 vez; segunda skill suprime via leitura do contexto visível.
14. **Cutucada não disparando sem `CLAUDE.md`** — `/triage` em projeto sem `CLAUDE.md`. Esperado: nenhuma cutucada (condição #1 do ADR-017).
15. **`/init-config` re-invocável + Resolution protocol passo 4 silente pós-config** — após bloco config gravado cobrindo `decisions_dir`, rodar `/new-adr`. Esperado: skill lê bloco direto (Resolution protocol passo 2); não pergunta `decisions_dir`; não oferece memorização one-shot.
16. **Resolution protocol passo 4 ainda ativo para role fora do bloco** — bloco config cobre 3 roles mas operador removeu `test_command` manualmente. Rodar `/run-plan` que precise de `test_command`. Esperado: skill cai no passo 3 (ask) e oferece memorização one-shot per role para o gap específico.
17. **Bloco config malformado / múltiplos markers / marker órfão** — marker presente em `CLAUDE.md` mas YAML adjacente não parseia (indent quebrado, `local` em role que rejeita, chave duplicada), OU dois markers presentes (corrupção por edição manual/copy-paste), OU marker HTML sozinho sem YAML adjacente. Esperado: skill para com diagnóstico textual identificando linha e tipo de anomalia; não reescreve, não funde, não toma o primeiro. Operador resolve manualmente. Coerente com postura editorial não-reparativa (paralelo com não-criar-CLAUDE.md no cenário 1).
18. **Gate `Gitignore` de ADR-005 disparado pós-config em local mode** — operador escolheu `local` para `decisions_dir` durante `/init-config`. Após `/init-config` fechar, operador invoca `/new-adr` pela primeira vez. Esperado: na primeira escrita em `.claude/local/decisions/`, o gate `Gitignore` per ADR-005 dispara (probe `git check-ignore -q .claude/local/decisions/.probe` retorna não-zero) propondo adicionar `.claude/local/` ao `.gitignore`. Operador confirma → entrada adicionada; cancela → modo local recusado para essa invocação. Gate **não dispara dentro de `/init-config`** — `/init-config` só grava no `CLAUDE.md`, não escreve sob `.claude/local/<role>/`.

## Notas operacionais

- **Ordem dos blocos importa.** Bloco 1 (skill nova) define a referência `/init-config`. Bloco 2 (cutucada) menciona `/init-config` nas 4 skills — depende do Bloco 1 estar pronto. Bloco 3 (docs) finaliza referenciando ambos. Executar nesta ordem; reviewers de cada bloco veem dependências satisfeitas.
- **Idioma.** Skill, cutucadas e seção em CLAUDE.md em PT-BR (canonical do toolkit per `philosophy.md` → "Convenção de idioma"). Frontmatter keys, marker HTML e `roles:` em inglês (mecânica).
- **Frontmatter `roles` da skill `/init-config`.** Skill **define** roles do consumer, não consome. Sem `roles.required` nem `roles.informational` — skill fora do Resolution protocol. A ausência total do bloco `roles:` no frontmatter é forma válida de declarar zero papéis per [ADR-003](../decisions/ADR-003-frontmatter-roles.md) § Schema (listas vazias podem ser omitidas). Cutucada de descoberta da ADR-017 **não dispara dentro de `/init-config`** (escopo do ADR é skills com `roles.required`).
- **Gating da cutucada.** Cada skill com `roles.required` faz seu próprio probe (`grep -q '<!-- pragmatic-toolkit:config -->' CLAUDE.md`) — duplicação de 1 linha em 4 sites é YAGNI sobre helper compartilhado per ADR-017 alternativa (g) descartada.
- **Dedup conversation-scoped.** Skill lê o contexto visível da conversa CC procurando a string canonical da cutucada. Sob context compression em sessões muito longas, cutucada pode reaparecer — aceito (ruído baixo, ≤1 linha) per ADR-017 § Limitações.
- **Probe stack-aware do `test_command`.** Cobertura v1: Maven, pytest/uv, npm, make. Stacks adicionais entram conforme aparecerem em consumers reais — não pré-implementar (YAGNI).
- **Edição vs cancelamento (cenário 3).** Skill nunca sobrescreve bloco existente sem confirmação explícita do operador via enum `Editar` / `Cancelar`. Cancelar → skill devolve sem tocar arquivo, reporta no-op.
