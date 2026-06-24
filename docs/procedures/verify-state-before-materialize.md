# Procedure — verify-state-before-materialize

Procedure shared codificando o gate de verificação de estado real antes de materializar captura originada de entry pré-existente do `.claude/local/NOTES.md` (per [ADR-069](../decisions/ADR-069-gate-verificacao-estado-antes-materializar-captura-notes.md)). Consumida por `skills/session-audit/SKILL.md` (passo 6, `captura_backlog`) e `skills/triage/SKILL.md` (passo 4, filing de linha/issue). Mudança da heurística vive aqui; SKILL.mds referenciam este arquivo como fonte canonical. Paralelo editorial a `gate-com-executor-validacao.md` (ADR-064) e `forge-auto-detect.md`.

## 1. Gatilho de aplicação

O gate dispara **apenas** quando a captura a ser filada **origina de uma entry pré-existente do `.claude/local/NOTES.md`** — i.e., a `citação_transcript` (session-audit) ou o material de gap-clarification (triage step 1, leitura do NOTES.md) que motiva o filing aponta para uma entry escrita em sessão anterior.

**Não dispara** para substância gerada na sessão corrente (fresh por construção, sem risco de staleness — probe seria cerimônia pura per ADR-002). Origem ambígua (não dá pra atribuir a entry NOTES.md específica) → tratar como não-NOTES-sourced (não probar).

## 2. Heurística de probe por tipo de artefato citado

A entry NOTES.md cita um artefato concreto → probar o estado real desse artefato antes de filar:

| Artefato citado na entry | Probe |
|---|---|
| Commit / mudança de código | `git log --grep "<ref>"` ou `git log --oneline -S "<trecho>"` no repo relevante |
| Arquivo que deveria existir/ser tracked | `git ls-files <path>` (tracked?) / `test -f <path>` (existe?) |
| Conteúdo em arquivo | `grep -n "<padrão>" <path>` |
| Cross-ref em outro repo | `git -C <repo> log`/`grep` no path absoluto do repo citado |
| Issue forge | `gh issue view <n>` / `glab issue view <n>` (state) |

Probe é cross-repo quando a entry cita repo externo (mesmo pattern do `journal-close` step 3c do meta-bridge — cwd absoluto, fail-soft).

Entry NOTES-sourced **sem** artefato concreto citável (texto vago/narrativo) → pular o probe, ir direto a §3 ramo **Indeterminado**.

## 3. Classificação e ação

- **Já resolvido** — probe confirma que o trabalho descrito na entry foi feito (commit existe, arquivo tracked, issue closed, cross-ref presente). → **Registrar baixa via append** + **pular o filing** (não criar issue/linha). Sem trabalho-fantasma.
- **Ainda pendente** — probe não encontra evidência de conclusão. → Filing segue normal.
- **Indeterminado** — entry sem artefato concreto citável (texto vago/narrativo) OU probe inconclusivo. → **Cláusula default-conservadora: filar normalmente.** Preserva o comportamento atual; `/next` continua sendo a rede de segurança a jusante. Não barrar filing sem evidência de conclusão (false-negative — pular pendência real — é o erro caro; false-positive — filar a mais — é barato, `/next` fecha).

**Pendente e Indeterminado convergem na ação (filar)** — a distinção entre os dois é apenas descritiva (para o reporte §5); só **Já resolvido** altera o comportamento (pula o filing). Na dúvida entre pendente e indeterminado, a ação é a mesma — não há decisão a errar.

## 4. Cláusula de baixa-via-append (preserva ADR-054 append-only)

"Já resolvido" → **append** de nova entry no NOTES.md (não mutação inline da entry original, per ADR-069 § Alternativas — preserva o invariante append-only de [ADR-054](../decisions/ADR-054-bridge-cross-project-note-consolidado.md)):

```
[<timestamp UTC>] Resolvido: <evidência concreta do probe> — refere entry de <data/trecho da original>. (baixa via /<skill> verify-state-before-materialize)
```

Mecânica de append idêntica ao `captura_notes` de `session-audit` (`Edit` append com timestamp). A entry stale original permanece auditável; re-disparo do probe sobre ela em sessão futura confirma resolvido a custo de re-probe barato, e a entry de baixa sinaliza "já tratado" ao scan.

## 5. Reporte ao operador

Quando o gate barra um filing (já resolvido → pulado), reportar in-prosa — 1 linha por captura barrada:

```
verify-state: pulei filing de "<linha que seria filada>" — entry NOTES.md já resolvida [<evidência do probe>]; baixa registrada via append.
```

Operador ciente sem interrupção (sem `AskUserQuestion` — é decisão mecânica auditável, não cutucada). Discordância → operador re-fila manualmente.

## 6. Consumidores

- **`skills/session-audit/SKILL.md` passo 6** (`captura_backlog`): se a `citação_transcript` aponta para entry NOTES.md pré-existente, aplicar gate antes de materializar. **Modo arquivo:** antes do `Edit` em `## Próximos`. **Modo forge** (per [ADR-070](../decisions/ADR-070-session-audit-forge-direto-substancia-cristalizada.md)): ramo **cristalizado** **internaliza** o gate localmente antes do `issue create` (a session-audit roda o probe — não delega); ramo **não-cristalizado** defere a `/triage` (step 1.5) e o gate aplica lá.
- **`skills/triage/SKILL.md` passo 4** (filing em `## Próximos`/forge): aplicar gate antes de gravar/criar a qualquer ramo cuja origem seja rastreável a entry NOTES.md lida no step 1 — (a) linha da feature-em-curso; (b) item fora-de-escopo do passo 2 **com origem rastreável a entry NOTES.md**. Nota: itens fora-de-escopo do passo 2 são tipicamente o que o operador menciona **fresh** na sessão corrente — esses **não** disparam o gate (per §1, fresh por construção); (b) só é elegível quando o item deriva de uma entry NOTES.md pré-existente. Gate precede o canal (arquivo/forge/local).

Mudança da heurística (gatilho, probe por tipo, classificação, baixa-via-append) vive **aqui** — SKILL.mds referenciam o procedure literalmente, não duplicam substância.
