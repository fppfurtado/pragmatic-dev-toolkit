# Plano — Extrair cutucada de descoberta para docs/procedures/

## Contexto

Onda 3 (parte 1) do roadmap `docs/audits/runs/2026-05-16-execution-roadmap.md` — proposta G_arch ≡ C_prose. Extrai a mecânica "cutucada de descoberta" (gating tri-state + 2 strings canonical) hoje duplicada em 5 SKILLs (`/triage`, `/run-plan`, `/new-adr`, `/next`, `/draft-idea`) para um procedure consolidado em `docs/procedures/cutucada-descoberta.md`, paralelo a `cleanup-pos-merge.md` (2º item da categoria `docs/procedures/` definida em ADR-024). `CLAUDE.md` `## Cutucada de descoberta` trima para scope + regra de herança editorial + referência ao procedure (decisão via cutucada do `/triage`).

**ADRs candidatos:** ADR-024 (categoria `docs/procedures/` — 2º item; bundle com plano gêmeo `procedures-forge-auto-detect.md` move categoria para 3 itens e fortalece critério Strong de ADR-024 § Limitações para promoção via A_arch), ADR-017 (mecânica canonical da cutucada — string-A), ADR-029 (extensão para `CLAUDE.md` ausente — string-B).

**Linha do backlog:** plugin: extrair cutucada de descoberta (gating tri-state + 2 strings canonical) para `docs/procedures/cutucada-descoberta.md` — consolida mecânica hoje duplicada em 5 SKILLs (`/triage`, `/run-plan`, `/new-adr`, `/next`, `/draft-idea`); CLAUDE.md `## Cutucada de descoberta` trima para scope + herança editorial + ref ao procedure. Onda 3 parte 1 (G_arch ≡ C_prose) do roadmap 2026-05-15/16; bundle com Onda 3 parte 2 (B_prose) move categoria `docs/procedures/` para 3 itens.

**Verificação dos 3 critérios cumulativos de ADR-024 § Decisão** (obrigatória per linha 65 do ADR):

- (i) Procedimento operacional: cutucada de descoberta é algoritmo executável tri-state, não esqueleto preenchível.
- (ii) ≥2 skills referenciam: 5 SKILLs (`/triage`, `/run-plan`, `/new-adr`, `/next`, `/draft-idea`).
- (iii) Acoplamento textual concreto: 10 ocorrências hoje duplicadas em 5 sites × 2 strings (ADR-017 § Trade-offs + ADR-029 § Trade-offs).

## Resumo da mudança

Cria `docs/procedures/cutucada-descoberta.md` (~30 linhas: tabela tri-state CLAUDE.md ausente / marker ausente / dedup + 2 strings canonical literais em PT-BR + algoritmo de probe + dedup conversation-scoped). 5 SKILLs substituem ~30 w de gating + strings literais por ~1 linha de referência ao procedure. `CLAUDE.md` `## Cutucada de descoberta` trima de ~25 linhas para ~5: scope (quais skills emitem), regra de herança editorial (SKILL nova com `roles.required` adota; checklist para code-reviewer em PRs), referência ao procedure. Net: ~120 w cross-skill + ~20 linhas auto-loaded por turn.

Procedure não inverte mecânica — ADR-017 + ADR-029 permanecem canonical de doutrina. Apenas relocaliza a redação mecânica + 2 strings para um único arquivo lido em runtime.

## Arquivos a alterar

### Bloco 1 — Criar docs/procedures/cutucada-descoberta.md {reviewer: code}

- `docs/procedures/cutucada-descoberta.md`: novo. Estrutura:
  - Linha inicial cita ADR-024 como categoria-base (parity com `cleanup-pos-merge.md`).
  - Intro 1-parágrafo apontando para ADR-017 + ADR-029 como decisões canonical.
  - Algoritmo passo-a-passo: (1) testar `CLAUDE.md` existe; (2) se ausente → emitir string-B; (3) se presente → `grep -q '<!-- pragmatic-toolkit:config -->' CLAUDE.md`; (4) marker ausente → emitir string-A; (5) com marker → suprimir.
  - Dedup conversation-scoped por string (string-A e string-B observam contexto visível independentemente — transição ausente → presente-sem-marker mid-session pode emitir string-A mesmo após string-B, porque dedup gating é por string distinta).
  - 2 strings canonical literais em PT-BR (per toolkit canonical), reproduzidas exatamente como hoje aparecem nos 5 sites.
  - Posicionamento da emissão: última linha do relatório final da skill.

### Bloco 2 — Wire 5 SKILLs ao procedure {reviewer: code}

Substituir bloco "Cutucada de descoberta" (~30 w + 2 strings literais cada) por linha-ref `Antes de devolver controle, executar a cutucada de descoberta conforme `${CLAUDE_PLUGIN_ROOT}/docs/procedures/cutucada-descoberta.md`.` em (paridade exata com pattern `cleanup-pos-merge.md` consumido por `/triage §0` e `/release`):

- `skills/triage/SKILL.md` (final do passo 5).
- `skills/run-plan/SKILL.md` (final do passo correspondente — localizar).
- `skills/new-adr/SKILL.md` (final do passo correspondente — localizar).
- `skills/next/SKILL.md` (final do passo correspondente — localizar).
- `skills/draft-idea/SKILL.md` (final do passo correspondente — localizar).

### Bloco 3 — Trim CLAUDE.md ## Cutucada de descoberta {reviewer: code}

- `CLAUDE.md` linhas ~128-152 (seção `## Cutucada de descoberta`): substituir por ~5-8 linhas contendo:
  - Scope: 5 skills com `roles.required` listadas explicitamente + nota sobre as 3 skills com só `roles.informational` que não emitem (`/debug`, `/release`, `/gen-tests`).
  - Regra de herança editorial: SKILL nova com `roles.required` adota a convenção manualmente; checklist para `code-reviewer` em PRs introduzindo nova SKILL.
  - Referência para mecânica e strings: `docs/procedures/cutucada-descoberta.md` (carrega tri-state + 2 strings canonical).
  - Cross-ref a `/init-config` como caminho proativo complementar.

### Bloco 4 — Atualizar roadmap marcando G_arch ≡ C_prose shipped {reviewer: doc}

- `docs/audits/runs/2026-05-16-execution-roadmap.md`: linha do item `G_arch ≡ C_prose` em Onda 3 `[ ]` → `[x]` com data + ref PR/commit ao concluir; entrada no `## Histórico de execução` ao final.

## Verificação end-to-end

- `ls docs/procedures/cutucada-descoberta.md` existe; `wc -l` ~30 linhas.
- `grep -c '${CLAUDE_PLUGIN_ROOT}/docs/procedures/cutucada-descoberta.md' skills/triage/SKILL.md skills/run-plan/SKILL.md skills/new-adr/SKILL.md skills/next/SKILL.md skills/draft-idea/SKILL.md` retorna ≥1 por SKILL (paridade exata com pattern `${CLAUDE_PLUGIN_ROOT}/`).
- `grep -E "string-A|string-B|tri-state|Gating with three outcomes" skills/*/SKILL.md` retorna **vazio** (mecânica não duplica mais inline nas SKILLs).
- `grep -E "string-A|string-B" CLAUDE.md` retorna **vazio** (CLAUDE.md trim removeu as strings literais).
- `grep -c "## Cutucada de descoberta" CLAUDE.md` = 1 (header preservado, conteúdo trimado).
- `wc -l CLAUDE.md` reduzido em ~20 linhas vs HEAD.

## Verificação manual

Cenários canonical (exercitar em consumer real ou simulação textual sobre o diff):

1. **CLAUDE.md ausente.** Invocar `/triage` em projeto sem CLAUDE.md. Última linha do reporte = string-B literal (mensagem PT-BR sobre criar `CLAUDE.md` e rodar `/init-config`). Procedure file deve ter sido lido pelo /triage.
2. **CLAUDE.md presente sem marker.** Invocar `/new-adr` em projeto com CLAUDE.md sem `<!-- pragmatic-toolkit:config -->`. Última linha = string-A literal (mensagem PT-BR sobre rodar `/init-config`).
3. **CLAUDE.md com marker.** Invocar `/run-plan` em projeto com marker presente. Cutucada suprimida silenciosamente — relatório termina sem dica.
4. **Dedup conversation-scoped.** Invocar `/next` após `/triage` na mesma conversa, ambos em projeto sem marker. Segunda invocação suprime string-A (dedup hit no contexto visível).

Cenário "A↔B independent mid-session" (transição ausente → presente-sem-marker dentro de uma sessão) coberto editorialmente na prosa do procedure (linha sobre dedup por string distinta) — não exercitado empiricamente por custo de setup mid-session vs ROI baixo (caso ADR-029 declara raro).

## Notas operacionais

- **Reviewer dispatch:** Blocos 1-3 `{reviewer: code}` (procedure novo carrega procedimento executado em runtime + SKILL.md edits substituem mecânica + CLAUDE.md trim verifica preservação de invariantes doutrinários — gatilho "5ª/6ª skill" de ADR-029 + regra de herança editorial); Bloco 4 `{reviewer: doc}` (edição cirúrgica em roadmap).
- **Verificar que ADR-001 carrega o cross-ref a ADR-024** estabelecido pelo plano `procedures-cleanup-pos-merge` (invariante ADR-024 § Decisão linha 69: "plano que implementa este ADR deve adicionar bullet em ADR-001 § Status ou parágrafo final apontando para ADR-024 como complemento"). Se ausente, este plano adiciona; presente, prossegue.
- **Não trim ADR-017 / ADR-029** — ADRs ficam canonical de doutrina (porquê e contexto histórico); procedure é a redação mecânica derivada. Cross-ref bidirecional: procedure cita ADRs, ADRs não precisam citar o procedure (ADR é imutável, procedure pode evoluir editorialmente).
- **Não introduzir mudança comportamental** — mecânica preserved exata (tri-state, ordem de probe, 2 strings literais, dedup conversation-scoped, posicionamento como última linha do reporte). Procedure é relocação textual.
- **`code-reviewer` no Bloco 1-2 também verifica** que cada SKILL substituiu inline-prose por ref consistente (idêntica linha-template em todos os 5 sites — facilita futuro retrofit).
- **Sequência relativa ao plano `procedures-forge-auto-detect.md`** — cada plano shipa via PR independente; merge em qualquer ordem é seguro quanto a overlap de arquivos. Roadmap (linha 45) prescreve cutucada primeiro pela cardinalidade (5 sites vs 4) e proximidade do gatilho ADR-029.
