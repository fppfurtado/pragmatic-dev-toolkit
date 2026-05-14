# Plano — `/init-config` aceita `CLAUDE.md` gitignored

## Contexto

`/init-config` step 3 atual detecta `CLAUDE.md` gitignored via `git check-ignore -q CLAUDE.md` e **para** com mensagem citando extrapolação informal de ADR-016 ("CLAUDE.md é compartilhável por design"). Resultado: projetos onde política organizacional não permite commit de `CLAUDE.md` ficam sem caminho institucional para o plugin — Resolution protocol passos 2/4 já operam textualmente no arquivo gitignored, mas memoização não propaga e worktrees do `/run-plan` não enxergam `CLAUDE.md`.

[ADR-030](../decisions/ADR-030-aceitar-claude-md-gitignored-via-worktreeinclude.md) decide reverter parcialmente a extrapolação: `/init-config` aceita `CLAUDE.md` gitignored, registra flag interna no step 3, estende step 4.5 (já estabelecido por [ADR-018](../decisions/ADR-018-replicacao-claude-em-modo-local-init-config.md) para garantir `.claude/` em `.worktreeinclude` em modo local) para também garantir `CLAUDE.md`, e emite linha de aceitação no step 5. Resolution protocol inalterado. Postura editorial não-reparativa preservada (skill não cria `CLAUDE.md` ausente, não modifica `.gitignore` automaticamente).

**ADRs candidatos:** ADR-030 (decisão estrutural implementada por este plano), ADR-018 (precedente direto do mecanismo step 4.5; mesma estratégia "skill cuida do setup ao primeiro contato com sinal declarado"), ADR-016 (extrapolação em `/init-config` step 3 que é parcialmente revertida; escopo literal de ADR-016 — hooks/scripts — preservado).

**Linha do backlog:** plugin: `/init-config` aceita CLAUDE.md gitignored e replica via `.worktreeinclude` (ADR-030)

## Resumo da mudança

Implementar a mecânica decidida em ADR-030 em `skills/init-config/SKILL.md`: reformular step 3 (registrar flag interna em vez de parar quando gitignored detectado), estender step 4.5 (cláusula OR no critério de disparo; lista composta de paths a garantir em `.worktreeinclude`; probe concreto via `grep -qE`), adicionar linha user-facing no step 5 quando flag ativa. Atualizar `docs/install.md` linha 70 para refletir que `/init-config` toca `.worktreeinclude` também quando `CLAUDE.md` gitignored (não exclusivamente em modo local).

## Arquivos a alterar

### Bloco 1 — `skills/init-config/SKILL.md` (mecânica) {reviewer: code}

- **Step 3 reformulado** (linhas 27-31 atuais): substituir bloco "Retorno zero (gitignored) → parar com mensagem..." por "Retorno zero (gitignored) → registrar flag interna `claude_md_gitignored = true` para o step 4.5; prosseguir normalmente". Remover mensagem doutrinária literal e cross-ref a ADR-016. Adicionar cross-ref a ADR-030.

- **Step 4.5 estendido** (linhas 99-114 atuais):
  - **Critério de disparo**: substituir "≥1 role configurada como `local`" por "≥1 role configurada como `local` OR `claude_md_gitignored = true`".
  - **Lista de paths a garantir**: explicitar que `.claude/` é adicionado quando ≥1 role local; `CLAUDE.md` é adicionado quando `claude_md_gitignored = true`; cada adição é independente e idempotente.
  - **Probe `CLAUDE.md`**: adicionar bullet análogo ao de `.claude/`: `grep -qE '^CLAUDE\.md$' .worktreeinclude` retorna não-zero → adicionar `CLAUDE.md` ao fim. Falso-negativo benigno aceito (paralelo direto com nota de ADR-018 § Limitações).
  - **Reporte**: ajustar mensagem do passo para refletir lista composta — ex.: `.worktreeinclude <criado|atualizado|inalterado> em <path>; <.claude/, CLAUDE.md> replicado(s) nas worktrees subsequentes do /run-plan.`

- **Step 5 estendido** (linha 120 atual em diante): adicionar linha de aviso informativo quando `claude_md_gitignored = true`:

  > `CLAUDE.md gitignored detectado — replicação garantida via .worktreeinclude por ADR-030.`

  Posicionar **antes** do aviso "Modo local declarado em ≥1 role" (linhas 120-122 atuais) — substitui semanticamente a mensagem doutrinária revogada do step 3 e cobre a transição da recusa anterior; aviso de modo local é ortogonal e vem depois.

- **`## O que NÃO fazer`** (linhas 128-135 atuais): preservar bullets "Não criar `CLAUDE.md` se ausente" e "Não modificar `.gitignore` automaticamente" — postura editorial não-reparativa intacta. **Adicionar** bullet documentando a guarda doutrinária inversa que ADR-030 estabelece:

  > Não pressionar doutrinariamente quando `CLAUDE.md` está gitignored. [ADR-030](../../docs/decisions/ADR-030-aceitar-claude-md-gitignored-via-worktreeinclude.md) estabelece aceitação como ato deliberado da skill (operador sinaliza via `.gitignore`, plugin opera dentro); reintroduzir mensagem "reconsidere o gitignore" no step 3 ou step 5 revoga a decisão.

  Critério CLAUDE.md → "Editing conventions" sobre `## O que NÃO fazer` aplica: viés sutil (recidiva por edição futura sem leitura de ADR-030) → bullet permanece.

### Bloco 2 — `docs/install.md` (doc reflection) {reviewer: doc}

- **Linha 70** atual: `"Em modo canonical (nenhum role declarado `local`), `/init-config` não toca `.worktreeinclude`."`

  Reformular para: `"Em modo canonical sem CLAUDE.md gitignored, /init-config não toca .worktreeinclude. Quando CLAUDE.md está gitignored (per ADR-030) ou ≥1 role em modo local (per ADR-018), /init-config cria/atualiza .worktreeinclude para garantir replicação."`

  Cross-ref `[ADR-030](decisions/ADR-030-aceitar-claude-md-gitignored-via-worktreeinclude.md)` adicionado.

## Verificação end-to-end

Repo sem suite automatizada (`test_command: null` no `CLAUDE.md` deste plugin). Verificação textual sobre o diff agregado:

- `skills/init-config/SKILL.md`:
  - Step 3 não menciona "parar" nem mensagem doutrinária; lê coerente como "detectar + prosseguir".
  - Step 4.5 cita cláusula OR explícita; probe `grep -qE '^CLAUDE\.md$'` literal; idempotência explícita.
  - Step 5 contém a linha literal `CLAUDE.md gitignored detectado — replicação garantida via .worktreeinclude por ADR-030.` para o caso `claude_md_gitignored = true`.
  - Cross-refs a ADR-030 presentes em step 3, step 4.5 e novo bullet do `## O que NÃO fazer`; cross-ref a ADR-016 removida do step 3 (única menção atual na skill; ADR-016 permanece íntegro no escopo de hooks documentado em seu próprio ADR).
  - `## O que NÃO fazer` ganha novo bullet documentando a guarda doutrinária inversa de ADR-030 ("não pressionar doutrinariamente quando CLAUDE.md gitignored"); bullets existentes preservados.

- `docs/install.md` linha 70 reformulada com cross-ref a ADR-030 + ADR-018; texto coerente com novo critério.

- Diff não toca `CLAUDE.md` (toolkit), outras skills, agents, hooks, ADRs além de ADR-030 (já criado em `/triage`) e ADR-029 (editado em `/triage` como absorção do design-reviewer Finding 1).

## Verificação manual

Mudança comportamental em skill — smoke-test em consumer real é o critério de done substantivo, mas exige re-instalação do plugin pós-release. Cenários enumerados aqui ficam como spec para o smoke pós-release; durante `/run-plan` cada cenário é exercitado mentalmente sobre o diff:

1. **Cenário "CLAUDE.md gitignored, primeira invocação"**:
   - Setup: projeto com `CLAUDE.md` existente, linha `CLAUDE.md` em `.gitignore`. Sem bloco config. Sem `.worktreeinclude`.
   - Rodar `/init-config`.
   - **Esperado**: step 3 detecta gitignored mas prossegue (não para). Wizard segue normalmente (perguntas dos 4 roles + `test_command`). Step 4 grava bloco config em `CLAUDE.md`. Step 4.5 cria `.worktreeinclude` contendo `CLAUDE.md` (e `.claude/` se algum role local declarado). Step 5 emite linha `CLAUDE.md gitignored detectado — replicação garantida via .worktreeinclude por ADR-030.`

2. **Cenário "CLAUDE.md gitignored + role local"**:
   - Setup: como (1), operador escolhe `Local` para `decisions_dir`.
   - **Esperado**: step 4.5 garante ambas `.claude/` E `CLAUDE.md` em `.worktreeinclude` (adições independentes). Reporte cita ambas.

3. **Cenário "CLAUDE.md tracked, modo canonical"** (regressão):
   - Setup: projeto com `CLAUDE.md` tracked (não-gitignored), sem bloco config. Sem role local.
   - **Esperado**: step 3 não dispara flag (gitignore retorna não-zero). Step 4.5 skip silente (sem role local, sem flag). Comportamento idêntico ao pré-ADR-030.

4. **Cenário "Re-invocação idempotente"**:
   - Setup: consumer já configurado por execução de (1).
   - Rodar `/init-config` novamente (caminho "Editar" do step 2).
   - **Esperado**: step 4.5 detecta `CLAUDE.md` já em `.worktreeinclude` (probe `grep -qE` retorna zero) → skip silente da adição. Reporte cita "inalterado".

5. **Cenário "Política muda mid-stream"**:
   - Setup: consumer configurado por (1). Operador descomenta `CLAUDE.md` do `.gitignore` (decide rastrear).
   - Rodar `/init-config` novamente.
   - **Esperado**: step 3 não dispara flag (gitignore retorna não-zero agora). Step 4.5 entra apenas se ≥1 role local; senão, skip silente. Linha `CLAUDE.md` em `.worktreeinclude` **permanece** (sem limpeza automática) — aceito per ADR-030 § Trade-offs; operador remove manualmente se desejar.

6. **Cenário "Worktree do `/run-plan` enxerga `CLAUDE.md`"** (handoff a outra skill):
   - Setup: consumer configurado por (1). Plano existe em `docs/plans/<slug>.md`.
   - Rodar `/run-plan <slug>`.
   - **Esperado**: worktree criada inclui `CLAUDE.md` replicado per `.worktreeinclude`. Resolution protocol passo 2 dentro da worktree lê o marker + bloco config corretamente. Skills downstream (`/triage`, `/run-plan` interno) operam normalmente.

7. **Cenário "Consumer em upgrade (pré-ADR-030)"**:
   - Setup: consumer que configurou `/init-config` em versão prévia (que recusava gitignored) — não tem CLAUDE.md em `.worktreeinclude`. Plugin atualizado.
   - Rodar `/run-plan` em algum plano.
   - **Esperado**: worktree não enxerga `CLAUDE.md` (não está em `.worktreeinclude`). Resolution protocol passo 2 falha silente; passo 3 cai em ask-on-demand per role. Operador percebe e roda `/init-config` para restaurar invariante. Sem safety net no `/run-plan` (aceito YAGNI per ADR-030 § Limitações). Pós `/init-config`, cenário (6) volta a funcionar.

## Notas operacionais

- **Ordem dos blocos**: Bloco 1 (mecânica em SKILL.md) primeiro; Bloco 2 (doc reflection em install.md) depois. Mudança em SKILL.md é o fato; install.md espelha.
- **Sem CHANGELOG/version bump nesse plano**: `/release` cuida disso quando o operador decidir publicar (cadência separada per CLAUDE.md → "What this repo is").
- **Validação manual é spec para smoke-test pós-release**: cenários 1-7 ficam como roteiro; execução real em consumer (ex.: projeto org com `CLAUDE.md` gitignored, ou setup ad-hoc) confirma o caminho-feliz e os edge cases declarados em ADR-030 § Limitações.
