# Cutucada de descoberta

Procedimento compartilhado executado em runtime pelas 5 skills que reativamente consomem o Resolution protocol step 3 — `/triage`, `/run-plan`, `/new-adr`, `/next`, `/draft-idea` — antes de devolver controle. Skills consumidoras leem este arquivo via Read e executam o algoritmo abaixo. Categoria `docs/procedures/` estabelecida em [ADR-024](../decisions/ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md). Decisões canonical: [ADR-017](../decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md) (mecânica original — string-A) e [ADR-029](../decisions/ADR-029-cutucada-descoberta-cobre-claude-md-ausente.md) (extensão para `CLAUDE.md` ausente — string-B). Designação por enumeração editorial — escopo detalhado em `CLAUDE.md` → "Cutucada de descoberta".

A cutucada surfa proativamente o caminho `/init-config` em projetos onde o bloco `<!-- pragmatic-toolkit:config -->` está fora de uso (CLAUDE.md ausente ou presente sem o marker).

## Algoritmo

Executar os 3 passos em ordem. **Cada passo é uma ação concreta com tool call literal — não interpretar como condição declarativa.** Inspeção visual do `CLAUDE.md` (via Read, contexto auto-loaded ou similar) **não substitui** o probe `Bash` do passo 1; incidente real em consumer `h3-finance-agent` (sessão `remove-n8n`, 2026-05-20) emitiu string-A 4 vezes com marker presente em `CLAUDE.md:93` porque o procedure foi lido como tabela declarativa em vez de algoritmo executado.

### 1. Probe estado do `CLAUDE.md`

Executar via `Bash`:

```bash
if [ ! -f CLAUDE.md ]; then echo NO_FILE; elif grep -q '<!-- pragmatic-toolkit:config -->' CLAUDE.md; then echo MARKER; else echo NO_MARKER; fi
```

Path relativo ao CWD — em worktree, resolve para o `CLAUDE.md` do worktree (semântica correta: cutucada reflete o contexto operacional corrente).

Mapear stdout para próxima ação:

| Stdout | Estado | Próxima ação |
|---|---|---|
| `MARKER` | `marker-presente` | **Suprimir e retornar.** Skill termina sem emitir cutucada. |
| `NO_MARKER` | `marker-ausente` | Seguir passo 2 com **string-A**. |
| `NO_FILE` | `claude-md-ausente` | Seguir passo 2 com **string-B**. |

### 2. Probe de dedup conversation-scoped

Para a string-X selecionada no passo 1, verificar se a literal exata da string-X já aparece em mensagem anterior do assistant no contexto visível desta conversa CC. Match → **suprimir e retornar**. Sem match → seguir passo 3.

Granularidade alinhada com [ADR-010](../decisions/ADR-010-instrumentacao-progresso-skills-multi-passo.md) — state mecânico vive na sessão CC, não em git/forge. Sob context compression em sessões muito longas, a string canonical pode sair da janela visível e o passo emiti-la novamente; aceito.

Dedup é **por string** — string-A e string-B observam o contexto visível independentemente. Transição `claude-md-ausente → marker-ausente` mid-session pode emitir string-A mesmo após string-B já ter aparecido na mesma sessão, porque o gating de dedup é por string distinta (não por presença genérica de cutucada).

### 3. Emitir string canonical

Inserir a string-X como **última linha do relatório final** da skill, após qualquer outra saída (commit, push, sugestão de próximo passo).

## Strings canonical

(em PT-BR per toolkit canonical; literal text reproduzido idêntico aqui — sites consumidores referenciam este procedure em vez de inlinar as strings)

- **string-A** — `CLAUDE.md` presente sem marker:

  > Dica: este projeto não declara o bloco `pragmatic-toolkit:config` no CLAUDE.md. Rode `/init-config` para configurar todos os papéis de uma vez.

- **string-B** — `CLAUDE.md` ausente:

  > Dica: este projeto não tem `CLAUDE.md`. Crie o arquivo e rode `/init-config` para configurar os papéis do plugin.

## Escopo de aplicação

Skills com `roles.informational` apenas (sem `roles.required`) **não** emitem a cutucada — escopo restrito às 5 listadas no topo deste arquivo (escopo + regra de herança editorial em `CLAUDE.md` → `## Cutucada de descoberta`).
