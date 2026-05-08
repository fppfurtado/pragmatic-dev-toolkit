# Plano — /run-plan §3.3 ganha 3ª condição de skip empírica via grep

## Contexto

O passo 3.3 (sanity check de docs user-facing) do `/run-plan` hoje tem **2 condições de skip**:

1. Plano listou `.md` user-facing (`README*`, `CHANGELOG*`, `install.md`, `docs/install.md`, `docs/guides/**`) em `## Arquivos a alterar` E o diff agregado o tocou.
2. `## Resumo da mudança` não menciona superfície user-facing (CLI/flag, env, endpoint, comportamento perceptível, integração externa, instalação/configuração).

Quando nenhuma das duas dispara, a regra cutuca via enum (`AskUserQuestion`, header `Docs`, opções `Consistente` / `Listar arquivos a atualizar` — forma fixada por ADR-006), com a instrução de "citar antes a superfície inferida e os candidatos típicos como prosa informativa".

Em uso real (`/run-plan triage-step0-already-deleted-remote`, sessão 2026-05-08), o agente cutucou com candidatos genéricos (`"README, install.md"`) sem fazer grep nos paths concretos. Operador questionou; ao rodar grep retroativo, **nenhum doc user-facing detalhava o trecho alterado** — skip era o caminho honesto, mas a regra atual não tem "skip empírico". A "prosa informativa" prescrita pela regra deveria carregar evidência concreta — listar referrers reais via `path:linha` ou fundamentar o skip — não palpite.

A memory `feedback_concrete_referrers_before_prompt.md` (criada na mesma sessão) é paliativo dependente do contexto; refinamento doutrinário no SKILL é mais durável.

**Continuidade com doutrina existente:** ADR-002 ("eliminar gates de cutucada quando trilho automático cobre") aplicado ao sanity check 3.3 via grep empírico — a evidência empírica é o "trilho automático" deste check. ADR-006 (forma do enum) preservada quando cutuca.

**Linha do backlog:** plugin: `/run-plan` §3.3 (sanity check de docs user-facing) — fazer grep dos identificadores tocados nos paths user-facing (README, install, guides) **antes** de cutucar. Grep vazio → seguir direto sem perguntar (skip silente justificado empiricamente, terceira condição de skip além das duas atuais). Grep com matches → cutucar listando os referrers concretos com path:linha, não candidatos genéricos. Cutucada com palpite ("candidatos típicos: README, install") ou cutucada vazia ("verifiquei e não achei nada, segue?") não cumpre o trabalho que a regra prescreve ("citar antes a superfície inferida e os candidatos típicos como prosa informativa") — a "prosa informativa" carrega evidência concreta ou fundamenta o skip. Flagado em uso real durante `/run-plan triage-step0-already-deleted-remote`.

## Resumo da mudança

Adicionar **3ª condição de skip empírica** ao passo 3.3 do `/run-plan`, e refinar a cláusula de cutucada para amarrar evidência concreta:

- **Skip empírico (3ª condição).** Quando as 2 condições atuais não disparam, executar grep dos **identificadores tocados** nos paths da positive list. Grep vazio → skip silente (justificado empiricamente).
- **Cutucada com referrers concretos.** Grep com matches → cutucar via enum existente (forma de ADR-006). `description` da segunda opção carrega os referrers reais (`<path>:<linha>`) como prosa informativa, não candidatos genéricos.

**Critério de "identificadores tocados"** (pragmático, sem parse de diff):

- Filenames base sem extensão de `## Arquivos a alterar` (ex.: `skills/triage/SKILL.md` → `triage`).
- Nomes de skill/agent/comando textualmente presentes no `## Resumo da mudança` (ex.: `/triage`, `/run-plan`, `code-reviewer`).

Fica de fora:
- Generalizar "cutucadas heurísticas exigem evidência empírica" para outros sanity checks ou skills — caso único hoje, YAGNI; reabrir se o padrão emergir.
- Mudar a positive list de paths user-facing ou a forma do enum (ADR-006).
- Critério via parse de diff (overhead desproporcional).
- Manter status quo + reforço editorial via memory (`feedback_concrete_referrers_before_prompt.md`) — descartado: memory é paliativo dependente do contexto da sessão e não vincula skill author futuro; refinamento doutrinário no SKILL é mais durável.

## Arquivos a alterar

### Bloco 1 — 3ª condição de skip empírica + referrers concretos em /run-plan §3.3 {reviewer: code}

- `skills/run-plan/SKILL.md`: refinar o passo 3.3 (sanity check de docs user-facing).
  - Após as 2 bullets de **Skip** atuais, adicionar 3ª bullet: skip empírico via grep dos identificadores tocados (critério acima) na positive list já existente; grep vazio → skip silente.
  - Refinar a cláusula de **Cutucar caso contrário**: a "prosa informativa" obrigatória passa a carregar os referrers reais (`<path>:<linha>` listados a partir do grep), e a `description` da opção `Listar arquivos a atualizar` ancora nesses paths concretos.

## Verificação end-to-end

- `grep -n "skip empírico\|grep dos identificadores\|referrers concretos\|<path>:<linha>" skills/run-plan/SKILL.md` retorna as linhas novas no passo 3.3.
- Releitura textual confirma: (a) 3ª bullet de skip aparece dentro do passo 3.3, em paralelo às 2 atuais, e referencia a mesma positive list; (b) cláusula de cutucada cita matching grep e listagem `path:linha`; (c) forma do enum (ADR-006) intacta — opções `Consistente` / `Listar arquivos a atualizar`; (d) nenhum outro passo do SKILL afetado.

## Verificação manual

Surface não-determinística (matching de identificadores contra conteúdo de arquivos user-facing). Forma do dado real: output de `grep -n` retorna `<path>:<linha>:<conteúdo>` ou vazio (exit 1). Cenários enumerados:

1. **Skip empírico (grep vazio) — alvo do fix.** Plano-fixture que altera apenas `skills/<nome-obscuro>/SKILL.md` (skill não citada em README/install). Identificadores tocados: filename base + nome do skill. Esperado: grep nos paths user-facing retorna vazio → skip silente; agente segue direto para 3.4. Caso real reproduzido em `/run-plan triage-step0-already-deleted-remote` (commit `1655304`): grep retroativo confirmou ausência de referrers no `/triage` step 0 nos docs user-facing.

2. **Cutucada com referrer concreto (grep com match).** Plano-fixture que altera `skills/release/SKILL.md`. Identificadores: `release`, `/release`. `README.md:13` cita `/release` (verificado: `grep -n "/release" README.md`). Esperado: enum cutuca com `description` da segunda opção citando `README.md:13: ...`; agente não palpita.

3. **Skip pelas 2 condições atuais (preservadas).** (a) Plano lista `README.md` em `## Arquivos a alterar` E o diff o toca → skip pela condição 1; 3ª condição não avaliada. (b) Plano cuja `## Resumo da mudança` não cita CLI/flag/env/endpoint → skip pela condição 2; 3ª condição não avaliada.

## Notas operacionais

- O grep é **lexical, não semântico**: matches espúrios (filename base curto que ocorre em prosa de README sem ser referrer real do skill — ex.: `triage` matchando "primeira triagem") viram cutucada legítima e são absorvidos pelo enum existente — operador descarta via `Consistente`. Aceitável; matching semântico seria overhead desproporcional.
- O critério de "identificadores tocados" é pragmático e tolerante a falsos negativos: skill renomeada apenas no diff sem aparecer em `## Resumo da mudança` ou `## Arquivos a alterar` pode escapar do grep — aceito porque a renomeação típica entra num desses dois lugares (autor do plano enuncia o que muda). Reabrir se padrão de falso negativo aparecer em uso real.
- A `feedback_concrete_referrers_before_prompt.md` na memory cobre o comportamento correto enquanto este plano não merge; após merge, a memory pode ser arquivada (manter por 1 release como rede).
- Bloco único `{reviewer: code}` — refinamento editorial em SKILL de implementação; sem teste novo (plugin sem suite); sem doc user-facing tocada (o próprio passo 3.3 valida que não há referrer ao `/run-plan §3.3` em README/install — circularidade resolvida: o refinamento documenta-se no próprio SKILL.md, único lugar onde o passo 3.3 vive).
