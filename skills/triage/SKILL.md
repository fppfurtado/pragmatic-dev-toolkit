---
name: triage
description: Alinha intenção e decide artefato (backlog, plano, ADR, atualização de domain/design) antes de implementar. Use quando o operador propuser feature, fix ou refactor sem plano nem linha de backlog.
---

# triage

Workflow de **alinhamento prévio** para mudança não-trivial — feature, fix com plano (saída de `/debug`), refactor com bifurcação, alteração que toca invariante. Produz artefato de alinhamento (linha de backlog, plano, ADR, atualização de `docs/domain.md`/`docs/design.md`) e devolve controle.

## Pré-condições

Para cada papel necessário (`product_direction`, `ubiquitous_language`, `design_notes`, `decisions_dir`, `plans_dir`, `backlog`), aplicar **Resolução de papéis**: probe canonical → bloco `<!-- pragmatic-toolkit:config -->` no CLAUDE.md → pergunta tri-state via `AskUserQuestion`.

- Papéis informacionais (`product_direction`, `ubiquitous_language`, `design_notes`, `decisions_dir`, `backlog`) podem resolver "não temos" — skill segue.
- `plans_dir` "não temos" → para com gap report em prosa livre.

Quando o passo 3 escolher "atualizar `ubiquitous_language`/`design_notes`" e o papel resolveu "não temos": propor criação no path canonical via enum (`Criar em <path>` / `Não usamos esse papel`). Segunda opção registra `paths.<role>: null` (oferta única de memorização). Mesmo mecanismo para `backlog` quando o passo 4 vai gravar linha (`Criar em BACKLOG.md` / `Não usamos esse papel`; segunda registra `paths.backlog: null`).

## Argumentos

Intenção em linguagem natural — frase curta (`/triage exportar movimentos em CSV`), descrição com contexto, ou vaga. Input vazio ou genericamente "o que vamos fazer hoje?" → seguir `skills/next/SKILL.md`.

## Passos

### 1. Carregar contexto mínimo

Ler **só o que o pedido tocar**, nesta ordem:

1. `product_direction` — alinhamento à direção de produto.
2. `ubiquitous_language` — bounded contexts, agregados/entidades, RNxx tocadas.
3. `backlog` — verificar item equivalente em **Próximos**, **Em andamento** ou **Concluídos**. Se existir, parar e reportar.
4. `design_notes` — só se a feature toca uma das integrações listadas.
5. `decisions_dir` — listar ADRs relacionados; ler na íntegra apenas os que o pedido contradiz/estende.

Não ler código aqui — é alinhamento de intenção, não design técnico.

### 2. Esclarecer gaps com o usuário

Identificar lacunas e perguntar **só o que for bloqueante**. Checklist mental (não questionário):

- **Escopo:** o que entra e o que fica de fora? Há caso menor que resolve 80%?
- **Superfícies além do código:** runtime config (env, segredos, templates), infraestrutura (compose, deploy, CI), docs operacionais, automação do projeto (skills/rules/hooks). Se sim, listar em `## Arquivos a alterar`. Anti-padrão: feature "código-completa" mas "em-produção-quebrada".
- **Invariantes:** alguma RN do `ubiquitous_language` é tocada?
- **Integrações:** alguma do `design_notes` entra?
- **Persistência:** estado novo? Migra schema? (gatilho potencial de ADR.)
- **Aprendizado de domínio:** bounded context novo, aggregate/entity novo, RN nova, conceito ubíquo novo, ou semântica alterada?
- **Validação manual?** Comportamento perceptível, fluxo crítico, ou integração frágil → plano inclui `## Verificação manual`. Refactor/internal/doc-only não precisa — `make test` basta.
  - **Surface não-determinística** (parsing, matching de strings contra dado real, comportamento de agente LLM): exigir antes do plano (a) **forma do dado real** — 1-2 exemplos concretos do formato em produção (separadores, prefixos, capitalização, ids internos que não devem vazar); (b) **cenários enumerados** em `## Verificação manual` — passos concretos que exercitem essas formas, não direção genérica. Sem enumeração, validação manual vira improvisação. Sub-bullet não dispara se a primeira pergunta resolveu "não".
- **Cobertura de teste?** Heurística: (i) bloco `{reviewer: qa}` quando toca invariante, integração, persistência, comportamento observável novo, ou é bug fix com risco de regressão; (ii) só `## Verificação end-to-end` textual quando gate automático cobre e nada de invariante novo entra; (iii) nada novo em testes para refactor puro / doc-only.
- **Bifurcação arquitetural:** dois caminhos com custo/manutenção/UX significativamente diferentes? Heurística: você consegue redigir dois planos distintos que ambos satisfazem a frase? Verbos abertos ("registrar", "validar", "notificar", "processar", "armazenar", "interagir") são sintoma frequente.

Se o operador já forneceu o necessário, pular as perguntas. Se houver 1–3 gaps reais, perguntar direto e curto. **Não fazer entrevista exaustiva.** Modo: gaps de escolha discreta via `AskUserQuestion`; gaps que pedem explicação livre (forma do dado real, justificativa de escopo) em prosa. Até 4 perguntas relacionadas numa única chamada.

**Itens fora de escopo emergidos.** Coisas que o operador menciona mas não pertencem a esta feature (TODO adjacente, tech-debt revelado, bug menor avistado): capturar como candidatos. Papel `backlog` resolvido normalmente → linhas separadas em `## Próximos`. Papel "não temos" → reportadas no passo 6. "Deixa pra lá" → descartar.

**Bifurcação detectada → pergunta nominal-comparativa obrigatória antes do plano.** Modo: enum com opções `(a) caminho-default-barato` e `(b) caminho-rico`, `description` carregando o trade-off concreto. Operador escolhe ou usa "Other". Escolha vai para `## Contexto` ou `## Resumo da mudança`. Se o operador já citou explicitamente uma opção na frase original (`/triage exportar CSV usando streaming`), pular a pergunta e registrar direto.

### 3. Decidir o artefato

Escolher **um** caminho. Em dúvida, preferir o mais leve.

| Caminho | Quando usar |
| --- | --- |
| **Só linha no BACKLOG** | Mudança pequena, foco claro, sem decisão estrutural nem integração nova. Maioria dos casos. |
| **Plano em `docs/plans/`** | Multi-arquivo, multi-fase, ou exige alinhamento prévio sobre a abordagem. |
| **ADR via `/new-adr`** | Decisão estrutural duradoura (persistência, biblioteca core, contrato de integração, política do sistema). |
| **Atualizar `docs/domain.md`** | Bounded context novo, aggregate/entity novo, RN nova, conceito ubíquo novo, ou semântica alterada. **Antes** de implementar. |
| **Atualizar `docs/design.md`** | Peculiaridade nova de integração descoberta na conversa. |

Combinações são comuns (linha de backlog + ADR; plano + atualização de domain).

### 4. Produzir os artefatos

Idioma de saída: espelhar o do projeto consumidor (default canonical PT-BR; ver "Convenção de idioma" em `docs/philosophy.md`).

**BACKLOG (papel: `backlog`):**

- **Papel resolvido normalmente:** uma linha para a feature em curso (frase de intenção, sem detalhamento).
  - Caminho com plano → grava em `## Em andamento`.
  - Caminho sem plano (linha pura, ADR-only, atualização de domínio) → grava em `## Próximos`.
  - Itens fora-de-escopo capturados no passo 2 → linhas separadas em `## Próximos`, mesmo quando o artefato principal é plano/ADR.
- **Papel "não temos":** disparar enum (`AskUserQuestion`, header `Backlog`). `Criar em BACKLOG.md` cria com cabeçalho mínimo (`# Backlog\n\n## Próximos\n\n## Em andamento\n\n## Concluídos\n`) e prossegue; `Não usamos esse papel` registra `paths.backlog: null` e prossegue **sem gravar** (itens reportados no passo 6).

**Plano (papel: `plans_dir`):** criar `<plans_dir>/<slug>.md`. Estrutura: `## Contexto` → `## Resumo da mudança` → `## Arquivos a alterar` → `## Verificação end-to-end` → (`## Verificação manual` se aplicável) → `## Notas operacionais`. Não inventar seções vazias.

No `## Contexto`:

- Se o passo 1 identificou termos do `ubiquitous_language` tocados, incluir `**Termos ubíquos tocados:** <Termo> (<categoria>), ...` — categorias: `bounded context`, `agregado`, `entidade`, `RN`, `conceito ubíquo`. Pedidos que não tocam o domínio → omitir.
- Se a feature foi gravada como linha no backlog, incluir `**Linha do backlog:** <texto exato>` — mensageiro de matching para `/run-plan` operar transições de estado.

`BACKLOG.md` **não aparece** em `## Arquivos a alterar` — transições são geridas pelo campo acima e pelo mecanismo do `/run-plan`.

Em `## Arquivos a alterar`, anotação `{reviewer: <perfil>}` no fim do header da subseção orienta o `/run-plan`. Palavra-chave em inglês (mecânica do toolkit). Schema:

- **Sem anotação** → default `code-reviewer` (exceção: blocos doc-only — ver regra abaixo).
- **Um perfil** (`{reviewer: code|qa|security|doc}`) → `/run-plan` invoca `code-reviewer`, `qa-reviewer`, `security-reviewer` ou `doc-reviewer`.
- **Múltiplos perfis** (`{reviewer: code,qa,security}`) → invoca todos os listados, agregando relatórios. Faz sentido quando o bloco toca múltiplos eixos (security/qa/code revisam objetos diferentes do mesmo diff; `code,doc` quando o diff toca código E doc adjacente).

Exemplos:

```markdown
### Bloco 1 — autenticação {reviewer: security}
### Bloco 2 — endpoint público {reviewer: code,qa,security}
### Bloco 3 — refactor interno
### Bloco 4 — atualizar README {reviewer: doc}
```

Bloco que **contém testes** (saída (i) da heurística de cobertura) recebe `{reviewer: qa}`; reviewer revisa qualidade do teste recém-escrito (caminho feliz, invariantes, edge cases, mock vs real). Para código de produção que mereça olhar combinado de YAGNI + cobertura no mesmo bloco, usar `{reviewer: code,qa}`.

Bloco **doc-only** (paths todos `.md`/`.rst`/`.txt`) recebe `doc-reviewer` como default — omitir anotação ou usar `{reviewer: doc}` para deixar explícito. Diff que toca código E doc adjacente no mesmo bloco, usar `{reviewer: code,doc}`.

**ADR:** invocar `/new-adr "<título>"` (não duplicar lógica). Reportar e seguir.

**`docs/domain.md` / `docs/design.md`:** edit cirúrgico, preservar tom e estrutura.

Slug de plano: lowercase, espaços/acentos→hífens, curto e descritivo (ex.: `exportar-movimentos-csv`).

### 5. Consolidação do backlog

Se o passo 4 modificou o arquivo do papel `backlog` (linha da feature, linhas fora-de-escopo, ou ambas), consolidar antes de fechar:

1. **Reler** o backlog na íntegra após edits.
2. **Flagar** (não decidir):
   - **Duplicatas** entre linhas recém-adicionadas e linhas pré-existentes em qualquer seção.
   - **Obsolescência:** linha em `## Próximos` que vira redundante pela nova (ex.: nova "exportar movimentos em CSV" cobre antiga "exportar movimentos como planilha"). Critério conservador — só flagar quando a sobreposição é nítida no texto, não em similaridade vaga.
3. **Sem flags → skip silente.** Linhas recém-gravadas já foram decididas no fluxo corrente.
4. **Com flags →** mostrar ao operador o estado tocado (com linhas recém-adicionadas marcadas) e perguntar uma vez via enum (`AskUserQuestion`, header `Backlog`, opções `Está bom, prosseguir` / `Aplicar edits`; Other → operador descreve em prosa quais edits — consolidar duplicatas, remover obsoleta, reordenar). Edits descritos entram no mesmo commit unificado do passo 6.

Caminho que não tocou backlog (atualização pura de `ubiquitous_language`/`design_notes`, ADR delegada sem linha, papel `backlog` "não temos") → skip silente.

### 6. Reportar, propor commit e devolver controle

Reportar em formato curto:

- O que foi registrado (linha, plano, ADR, atualização de domínio).
- Paths dos arquivos criados/alterados.

Quando `backlog` resolveu "não temos", acrescentar **"Itens não registrados (papel `backlog` desativado):"** listando (a) a frase de intenção que teria sido gravada e (b) cada item fora-de-escopo do passo 2.

Propor commit único agrupando os artefatos. Mensagem segue a convenção do projeto consumidor (default Conventional Commits em inglês, `docs:` ou `chore:`). Confirmação via enum (`AskUserQuestion`, header `Commit`, opções `Confirmar e commitar` / `Editar mensagem`).

Após confirmação:

- **Caminho sem plano:** apenas `git commit -m "…"`. Push não exigido.
- **Caminho com plano:** confirmação cobre **commit + push como unidade atômica**. Verificar `git rev-parse --abbrev-ref HEAD` — se não for branch principal (default `main`), parar e reportar. Se for, **um único** `Bash` com `git commit -m "…" && git push origin <branch-atual>` — sem flags. Push falho → reportar erro literal e parar; commit local permanece, `/run-plan` recusará até o operador resolver. (Sem o push, `/run-plan` criaria worktree de estado que o remote desconhece — merge do PR produz artefato no `BACKLOG.md`.)

Se não há alterações para commitar (ADR-only que já commitou via `/new-adr`, ou nada alterado), pular.

Sugerir próximo passo (uma frase): "implementar via /run-plan <slug>", "validar o plano antes de codar", "preencher o ADR".

## O que NÃO fazer

- Não duplicar conteúdo de `CLAUDE.md`, `docs/domain.md` ou `docs/design.md` no plano — referenciar.
- Não separar `git commit` e `git push` no caminho-com-plano — a unidade atômica do passo 6 elimina a janela em que push é esquecido.
- Não recuperar push falho via `--force`, `--force-with-lease`, retry automático ou flags equivalentes — parar, reportar erro literal e deixar manual.
