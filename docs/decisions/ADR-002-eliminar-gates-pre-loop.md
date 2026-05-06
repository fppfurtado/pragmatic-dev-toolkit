# ADR-002: Eliminar gates de cutucada na fase pré-loop do /run-plan

**Data:** 2026-05-06
**Status:** Proposto

## Origem

- **Investigação:** Revisão arquitetural pós-v1.20.0 contou até 4 enums de cutucada em cascata na fase pré-loop do `/run-plan` (pré-condição 2c, passo 1.2 `.worktreeinclude`, passo 1.2 credencial, passo 2 sanity check de escopo). Cada interrupção tira o foco; juntas, fragmentam a entrada num batch onde o operador já decidiu prosseguir.
- **Decisão base:** Mecânica de **captura automática de imprevistos** (passo 4.5 do `/run-plan`) já distingue duas categorias com trilhos persistentes: **Validação** → `## Pendências de validação` no plano; **Backlog** → `## Próximos` do backlog. A fase pré-loop estava reinventando o mesmo problema (warnings que merecem atenção mas não bloqueiam) sem reusar o mecanismo existente.

## Contexto

`/run-plan` distingue dois tipos de finding na fase pré-loop:

- **Bloqueios** — invariantes do estado git/setup quebradas (plano sujo, baseline vermelho, worktree órfã, push esquecido). Skill **para**, não cutuca; operador resolve antes de prosseguir. Continua igual.
- **Cutucadas** — qualidade-de-mudança que merece atenção mas não impede progresso (alinhamento dirty, gitignored não replicado, escopo divergente do plano). Hoje fragmentadas em 4 enums; cada uma interrompe o operador.

Cada cutucada hoje é uma pergunta `Continuar / Não continuar` (ou variante) com a mesma resposta na maioria dos runs reais (`Continuar`, porque o operador já decidiu rodar o plano). A pergunta vira ritual sem decisão genuína. Princípio relacionado: **"Não perguntar por valor único derivado"** em `docs/philosophy.md` → "Convenção de pergunta ao operador".

## Decisão

**Eliminar todos os gates de cutucada na fase pré-loop.** Cada warning detectado é classificado e materializado no trilho existente do passo 4.5 (Validação ou Backlog), com aviso informativo ao operador. Skill nunca interrompe por cutucada na fase pré-loop.

Mecânica:

### 1. Detectar warnings antes da worktree

Mesmos 4 warnings da cascata atual:

- **Alinhamento dirty** — alterações uncommitted em `backlog`, `ubiquitous_language`, `design_notes`, ou arquivo sob `decisions_dir`.
- **`.worktreeinclude` ausente + gitignored em uso** — raiz do repo tem `.env`, dbs locais, ou fixtures não versionadas, mas `.worktreeinclude` não existe e operador não declarou `paths.worktreeinclude: null`.
- **Credencial gitignored não coberta** — plano tem `## Verificação manual` E raiz tem `.env`/`*.local.yaml`/`secrets.*` não coberto pelo `.worktreeinclude` aplicado.
- **Escopo divergente** — `## Contexto` ou `## Resumo da mudança` cita superfície externa (config, env, infra, deploy, webhook, integração externa, `.env`) ausente em `## Arquivos a alterar`.

### 2. Classificar e materializar por trilho

| Warning | Custo de detecção tardia | Trilho |
|---|---|---|
| Alinhamento dirty | Baixo (reviewer pode flagar invariante uncommitted) | **Aviso informativo + segue** — reporta lista de arquivos uncommitted; skill prossegue. |
| `.worktreeinclude` ausente | Baixo (se baseline falhar, captura imediata in situ já existe) | **Backlog** — linha em `## Próximos` propondo criação de `.worktreeinclude` listando os gitignored detectados em uso. |
| Credencial não coberta | **Alto** (descoberto na hora da validação manual) | **Validação** — entrada em `## Pendências de validação` do plano corrente: "Cenário de validação manual não exercitado por falta da credencial `<nome>` na worktree." |
| Escopo divergente | **Alto** (mudança "código-completa, em-produção-quebrada") | **Validação** — entrada em `## Pendências de validação`: "Superfície externa `<X>` mencionada em Contexto/Resumo mas ausente em `## Arquivos a alterar` — cenário não exercitado." |

Mensagens uniformes ao operador (espelham 4.5):
- Aviso informativo: `"aviso: <descrição curta>"`
- Backlog: `"capturei no backlog: <linha>"`
- Validação: `"capturei para verificação: <linha>"`

### 3. Skill segue para a worktree

Nenhuma pergunta. Sem warnings detectados → silêncio total. Com warnings → mensagens 1-by-1 e prossegue.

### 4. Casos preservados

- **Bloqueios** (plano sujo, push esquecido, baseline vermelho, worktree órfã) ficam fora desta política. Continuam parando in situ com captura imediata em `## Próximos` já existente.
- **`.worktreeinclude` declarado `null`** (operador disse "não preciso") — silencia a captura de Backlog, mas **não silencia** o gatilho cruzado de credencial: contexto mudou (plano corrente exige `## Verificação manual`).
- **Mensagem de captura no done**: passo 4.5 corrente gera bloco extra revisor `code` + micro-commit quando há materializações. As capturas da fase pré-loop somam-se à mesma lista; bloco extra final cobre tudo.

## Consequências

### Benefícios

- **Zero interrupções** por cutucada na fase pré-loop.
- **Reuso da mecânica do passo 4.5**: Validação vs Backlog já são trilhos canônicos; warnings da pré-loop usam o mesmo despacho. Single source of truth para "atenção pendente".
- **Visibilidade preservada**: warnings de alto custo (credencial, escopo) chegam ao gate final do done via `## Pendências de validação` — operador vê antes de declarar concluído.
- **Skill mais simples**: 4 enums viram 0; lógica de classificação centralizada na mesma função do passo 4.5.

### Trade-offs

- **Sem detecção antecipada antes da worktree**: o sinal de "pausar antes de gastar setup" desaparece. Para escopo divergente (warning de alto custo + custo de relançar baixo), o operador descobre só no done. Aceito porque escopo divergente é raro em prática (`/triage` faz checagem prévia de superfícies); otimizar para raro é YAGNI.
- **Aviso informativo de alinhamento dirty depende de o operador ler**: se ignorado, reviewer pode não ver invariante uncommitted. Mitigação: o aviso é claro e localizado; operador que ignora está fazendo escolha consciente.

### Limitações

- **Bloqueios** (estado git/setup) continuam fora desta política. Fragmentação remanescente é justificada — bloqueio exige resolução pré-skill, é categoria diferente de cutucada.
- ADR não promete que todo warning futuro caiba nos trilhos existentes. Critério: warning é (a) detectável antes ou durante o /run-plan, (b) não-bloqueante, (c) mapeável para Aviso / Backlog / Validação. Warnings que violem (c) — ex.: warning que exige decisão imediata e irreversível — voltam para gate explícito; revisar caso a caso.

## Alternativas consideradas

- **Gate único informativo (caminho-a inicial)**: detectar warnings, listar em prosa, pedir `Prosseguir` / `Pausar` num enum binário. Descartado: a pergunta vira cerimônia (resposta majoritária `Prosseguir`); reuso da mecânica de captura existente é mais flat e elimina a interrupção.
- **Multi-select com fix in-place (caminho-b inicial)**: cada warning seria item selecionável; selecionar = aplicar correção automática. Descartado: aumenta superfície da skill (mapping warning→ação cresce com cada warning novo); relançar manualmente é trivial.
- **Manter cascata atual**: status quo descartado pela revisão arquitetural — fragmentação de foco é custo de UX real.
- **Híbrido (gate só para escopo divergente)**: descartado — escopo divergente é raro e o trilho de Validação cobre razoavelmente o caso.

## Gatilhos de revisão

- Operador frequentemente descobre escopo divergente tarde demais e relançar tem custo material → reabrir para considerar gate específico para este warning.
- Surge um 5º+ warning na fase pré-loop com natureza distinta dos atuais → reavaliar se cabe nos trilhos existentes ou exige nova categoria.
- Lista de `## Pendências de validação` cresce sistematicamente sem ser fechada → sinal de que o trilho de Validação está absorvendo mais do que deveria; revisar critério.
