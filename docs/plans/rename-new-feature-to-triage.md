# Rename `/new-feature` → `/triage`

## Contexto

A skill `/new-feature` cobre o fluxo de alinhamento prévio para qualquer mudança não-trivial — features novas, mas também correções que precisam de plano (rota saída de `/debug`), refactors com bifurcação arquitetural, alterações pontuais que tocam invariante. O nome atual sugere escopo restrito ("nova funcionalidade") e desencaixa do uso real. O próprio `/debug` já encaminha o operador para `/new-feature` quando a correção exige plano (ver `skills/debug/SKILL.md:88,94`).

`triage` descreve a função real: dado um intent do operador, a skill decide qual artefato produzir (linha de backlog, plano, ADR, atualização de domínio/design) ou para com gap report. É um roteador, não um produtor de feature. Pareia com `/debug` no eixo "pensar antes de agir" (diagnose ↔ triage).

**Decisões já fechadas (não revisitar):**

- **Sem compat shim.** Não criar alias `/new-feature` apontando para `/triage`. Filosofia flat: rename é breaking, operadores instalados reaprendem o nome (philosophy → "Convenção de naming" implica naming carrega contrato; alias enfraquece).
- **Convenção de naming relaxada.** `docs/philosophy.md:94` declara skills genéricas como `<verb>-<artifact>` (ex.: `new-feature`). `triage` é um único termo. Operador escolheu relaxar a convenção: aceitar `<verb>` quando o artefato emerge da decisão da skill (não é fixo). Linha 94 ganha nota explicando o caso.
- **Description do frontmatter atualizada para escopo broader.** Nova versão menciona explicitamente fix/refactor/mudança pontual além de feature.
- **Históricos não tocados.** `CHANGELOG.md` e `docs/plans/*.md` (incluindo planos cujo filename contém `new-feature`) ficam intocados — registro do que existia ao tempo de cada release. Substituir referências históricas distorce o registro sem ganho.
- **Release separada.** Esta mudança é breaking (slash command rename visível ao operador). Após o rename consolidado, operador roda `/release minor` (v1.14.0). Não embutir bump nesta sequência — `/release` tem fluxo próprio.

## Resumo da mudança

Três blocos sequenciados para garantir que cada commit deixa o repo coerente (referências e convenção sempre alinhadas):

1. **Bloco 1 — Rename da skill + relaxar convenção.** `git mv skills/new-feature skills/triage`, atualizar frontmatter (`name`, `description`), título, exemplos internos do SKILL.md. Atualizar `docs/philosophy.md:94` (relaxamento da convenção). Atomic: rename só faz sentido se a convenção aceita.
2. **Bloco 2 — Atualizar referências em `docs/philosophy.md`.** Substituir as ~12 ocorrências restantes de `/new-feature` no documento. Bloco isolado porque philosophy é o documento mais denso e merece revisão dedicada.
3. **Bloco 3 — Atualizar referências em docs operacionais e cross-skill.** `CLAUDE.md`, `README.md`, `docs/install.md`, `skills/run-plan/SKILL.md`, `skills/debug/SKILL.md`, `skills/release/SKILL.md`. Mudança mecânica (substituição literal `/new-feature` → `/triage`).

## Arquivos a alterar

### Bloco 1 — Rename da skill + relaxar convenção {reviewer: code}

- `skills/new-feature/SKILL.md` → `skills/triage/SKILL.md` (via `git mv` para preservar histórico).
- `skills/triage/SKILL.md`:
  - Frontmatter `name: new-feature` → `name: triage`.
  - Frontmatter `description:` → `Triagem da intenção do operador (feature, fix, refactor, mudança pontual): alinha contexto, levanta gaps e decide qual artefato (linha de backlog, plano, ADR ou atualização de domínio/design) é necessário antes de implementar. Use quando o operador propuser qualquer mudança que ainda não tenha plano ou linha de backlog.`
  - Título `# new-feature` → `# triage`.
  - Linha 6 ("Workflow de **alinhamento prévio** para uma funcionalidade nova...") → reescrever para refletir escopo broader (qualquer mudança que precise de alinhamento antes de código).
  - Exemplos internos `/new-feature exportar movimentos do mês em CSV` → `/triage exportar movimentos do mês em CSV` (e os outros 2 exemplos das linhas 23-25).
  - Exemplo `/new-feature exportar CSV usando streaming` (linha 64) → `/triage exportar CSV usando streaming`.
  - Auto-referência "esta skill" mantém — sem nome literal.
- `docs/philosophy.md` linha 94 (tabela de convenção de naming):
  - Atualizar coluna "Genérico" da linha de Skill: `<verb>-<artifact>` (ex.: `new-feature`) → `<verb>-<artifact>` (ex.: `new-adr`) **ou** `<verb>` quando o artefato emerge da decisão da skill (ex.: `triage`).
  - Adicionar parágrafo curto (2-3 linhas) abaixo da tabela explicando: skill como `triage` decide qual artefato produzir entre múltiplas opções — sufixo fixo seria mentira sobre o output.

### Bloco 2 — Referências em `docs/philosophy.md` {reviewer: code}

Substituir literal `/new-feature` → `/triage` nas linhas: 17, 19, 54, 134, 158, 178, 183, 195, 199. Verificar que cada substituição mantém sentido no contexto (ex.: linha 195 "`/new-feature` (alignment) extrai termos tocados" → `/triage` (alignment) extrai termos tocados — leitura segue natural).

### Bloco 3 — Docs operacionais e cross-skill {reviewer: code}

Substituições mecânicas:

- `CLAUDE.md`: linhas 15, 47, 50.
- `README.md`: linhas 9, 12.
- `docs/install.md`: linhas 36, 41, 43, 63.
- `skills/run-plan/SKILL.md`: linhas 8, 30.
- `skills/debug/SKILL.md`: linhas 3, 88, 94, 98 (incluindo a description do frontmatter).
- `skills/release/SKILL.md`: linha 69.

Após o bloco, rodar `grep -rn "new-feature" --include="*.md"` para verificar zero ocorrências fora de `CHANGELOG.md` e `docs/plans/`.

## Verificação manual

Repo não tem suite de testes (CLAUDE.md: "There is no build step and no test suite"). Validação é instalação local + smoke test no Claude Code:

1. Instalar o plugin localmente num projeto consumidor: `/plugin install /path/to/pragmatic-dev-toolkit --scope project`.
2. Confirmar que `/triage` aparece em `/help` ou `/plugin list`.
3. Confirmar que `/new-feature` **não** aparece mais (rename foi limpo, não duplicado).
4. Invocar `/triage <intent qualquer>` e validar que o protocolo flui — passos 1-6 do antigo `/new-feature` executam idênticos (resolução de papéis, gap discovery via `AskUserQuestion`, decisão de artefato, gravação, revisão de backlog, proposta de commit).
5. Em projeto com `BACKLOG.md` resolvido, confirmar que linha gravada em `## Próximos` segue idêntica ao comportamento anterior.
6. Inspeção textual: `grep -rn "new-feature" --include="*.md"` no repo do toolkit deve mostrar zero ocorrências fora de `CHANGELOG.md` e `docs/plans/`.

## Notas operacionais

- **Ordem dos blocos é load-bearing.** Bloco 1 deixa o repo coerente (skill renomeada + convenção que aceita). Blocos 2 e 3 podem ser invertidos sem quebrar nada, mas a ordem proposta agrupa por escopo (philosophy denso primeiro, depois mecânico).
- **`/run-plan` neste repo não tem `test_command`.** Esse repo legitimamente não tem `make test` (sem build/test suite). `/run-plan` vai pedir confirmação tri-state — operador responde `não temos` e o gate automático cai para "apenas verificação manual".
- **Worktree precisa do `.worktreeinclude`.** Verificar antes de rodar `/run-plan` que o arquivo lista pelo menos `skills/`, `docs/`, `CLAUDE.md`, `README.md` (ou seus globs equivalentes). Sem isso, a worktree não verá os arquivos a alterar.
- **Após merge desta mudança:** rodar `/release minor` para v1.14.0. CHANGELOG ganha entrada explicando o rename e a justificativa. Esta é a primeira release que dogfooda o `/triage` em si (skill que produziu o plano deste rename já era `/new-feature` — a próxima invocação será sob o novo nome).
