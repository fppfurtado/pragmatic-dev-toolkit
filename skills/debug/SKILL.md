---
name: debug
description: Diagnostica a causa-raiz de um sintoma (teste falhando, erro inesperado, comportamento divergente) seguindo método científico — precisar sintoma → reproduzir → isolar → testar hipóteses → causa-raiz com evidência. Produz diagnóstico, não fix; o operador escolhe o caminho de correção depois (revert, patch direto, ou /triage para mudança maior). Stack-agnóstico.
---

# debug

Esta skill enforca **"não corrigir sem isolar a causa"**. Recebe um sintoma e produz um diagnóstico — não escreve código, não cria commit, não aplica instrumentação. Saída é texto na conversa: sintoma observado, reprodução, hipóteses testadas, causa-raiz com evidência, escopo de impacto, caminhos de correção possíveis. O operador decide o caminho depois.

Idioma do diagnóstico: **espelhar o idioma do projeto consumidor** (ver "Convenção de idioma" em `docs/philosophy.md`). Default canonical PT-BR.

## Argumentos

Sintoma operacionalizável. Exemplos:

- `/debug test_export_csv falhou com TimeoutError no CI`
- `/debug webhook /payment retorna 500 desde o deploy de ontem`
- `/debug datas saem com fuso errado em produção`

Sintoma vazio ou vago ("não está funcionando", "está bugado") → pedir precisão antes de prosseguir (passo 1).

## Pré-condições

Paths e comandos seguem **Resolução de papéis** (ver `docs/philosophy.md`): default canonical → bloco `<!-- pragmatic-toolkit:config -->` no CLAUDE.md → pergunta ao operador.

Roles consumidos (todos informacionais — nenhum bloqueia a skill):

- `test_command` (default: `make test`): usado para reproduzir teste falhando ou para rodar a suíte que exerce o cenário.
- `ubiquitous_language` (default: `docs/domain.md`): consultado se o sintoma toca invariantes documentadas (RNxx ou equivalentes).
- `decisions_dir` (default: `docs/decisions/`): consultado se o sintoma envolve invariantes pós-erro (rollback, retry com efeito colateral, divergência de estado).
- `design_notes` (default: `docs/design.md`): consultado se o sintoma envolve integração externa.

`/debug` reporta o que tem evidência mesmo com contexto parcial — papel ausente nunca é gap report, apenas reduz a base de hipóteses.

## Passos

### 1. Precisar o sintoma

Perguntas de precisão são **prosa livre** — operador descreve em linguagem natural (ver "Convenção de pergunta ao operador" em `docs/philosophy.md`).

Se a entrada é genérica, perguntar antes de hipotetizar:

- Qual ação produz o sintoma (comando, teste, request, fluxo manual)?
- Output observado vs esperado?
- Onde foi observado (dev local, CI, staging, prod)?
- Reprodutibilidade: sempre, às vezes, uma vez só?
- Mudou recentemente? Quando começou a falhar?

Sem sintoma operacionalizável, não avançar.

### 2. Reproduzir

- Sintoma é teste: rodar o `test_command` resolvido restringindo ao teste alvo conforme a sintaxe da stack (filtro por nome em pytest, cargo, jest, go test, etc.).
- Sintoma é runtime error: identificar input/comando mínimo que dispara o erro.
- Sintoma intermitente (race condition, flaky test, dependência externa instável): reproduzir N vezes (default 5) e reportar a taxa observada. Análise prossegue mesmo sem reprodução determinística — diagnóstico fica sinalizado como **estatístico**, não determinístico.
- Não-reprodutível localmente: enumerar os artefatos disponíveis (stack trace, logs, métricas, screenshot), prosseguir com base em evidência indireta e **sinalizar explicitamente** que a análise é especulativa.

Evitar pular para hipótese antes de ver o sintoma com os próprios olhos quando a reprodução é viável.

### 3. Isolar

Estreitar a área suspeita antes de hipotetizar:

- Stack trace → módulo/função.
- `git log -- <arquivos suspeitos>` recente: o sintoma começou após qual commit?
- `git blame` nas linhas relacionadas ao erro.
- ADRs (`decisions_dir`) se o sintoma envolve invariantes pós-erro.
- `design_notes` se envolve integração externa com peculiaridades documentadas.
- `ubiquitous_language` para checar se o comportamento observado fere uma RNxx.

### 4. Hipotetizar e testar

Para cada hipótese plausível:

1. **Estado** em uma frase: "X falha porque Y".
2. **Definir condição que confirma** (o que deve acontecer se a hipótese é verdadeira) e **condição que refuta** (o que deve acontecer se for falsa).
3. **Observar**: rodar teste, ler código, sugerir instrumentação ao operador (não aplicar).
4. **Atualizar status**: confirmada / refutada / inconclusiva.

Limite: **parar quando duas hipóteses consecutivas forem refutadas sem ganho de evidência nova** (mesmo erro, mesmo escopo, nenhuma pista nova) e reportar o status da investigação ao operador (passo 5, ramo "nenhuma hipótese fechou").

Manter o ledger das hipóteses (frase + status final + evidência) acessível para o passo 5. Quando ≥2 hipóteses foram examinadas, o ledger entra como campo *Hipóteses testadas* do diagnóstico final.

### 5. Causa-raiz

Quando uma hipótese é confirmada com evidência, formular o diagnóstico nos campos abaixo:

- **Sintoma:** descrição operacional do que se observa.
- **Hipóteses testadas:** ledger das hipóteses examinadas no passo 4 — formato por linha `H<n> (<status>): <hipótese em uma frase>. <evidência confirmadora ou refutadora>`. Status canonical: `confirmada` / `refutada` / `inconclusiva`. **Omitir o campo** quando apenas uma hipótese foi testada e confirmada — *Causa-raiz* sozinha basta (espelha "lista vazia → skip silente" em `/run-plan` 4.5).
- **Causa-raiz:** arquivo:linha + mecanismo (por que o código se comporta assim).
- **Evidência:** o que foi observado/rodado que comprova (output do teste, log, comparação git diff, etc.).
- **Escopo de impacto:** quem mais é afetado pelo mesmo bug? Há outros call-sites, outras invariantes correlacionadas?
- **Caminhos de correção (não execução):** **um ou mais caminhos** com trade-off explícito — revert do commit X, patch local pequeno (apontar mudança mínima), ou `/triage <intent-do-fix>` se virar mudança maior. No último caso, o diagnóstico completo (incluindo *Hipóteses testadas* quando presente) é insumo natural do `## Contexto` do plano que `/triage` vai produzir. Se a investigação revelar caminho único razoável, declarar **"caminho único razoável"** com motivo (ex.: "revert é a única opção segura porque o commit X introduziu corrupção de dados que se acumula"). Operador decide.

Se nenhuma hipótese fechou ao fim do passo 4: o campo *Hipóteses testadas* carrega o ledger completo (refutadas + inconclusivas), *Causa-raiz* é substituída por **palpite atual com nível de confiança baixa explicitado**, e o relato preserva o que foi observado para que `/triage` (se for esse o caminho) tenha base. Evidência incompleta é resultado válido; chute disfarçado de causa-raiz, não.

### 6. Reportar e devolver controle

Apresentar o diagnóstico do passo 5 em formato curto na conversa e sugerir o **próximo passo** numa frase, escolhido entre:

- **Revert** — quando a investigação isolou o sintoma a um commit específico e o revert é seguro (ex.: "revert de `<hash>` no branch atual").
- **Patch local** — quando a mudança é cirúrgica e cabe sem alinhamento prévio (ex.: "ajustar `<arquivo>:<linha>` — uma linha; commitar diretamente").
- **`/triage <intent-do-fix>`** — quando o fix é mudança maior (multi-arquivo, toca invariante/integração, exige plano). O diagnóstico completo entra como insumo do `## Contexto` do plano.

## O que NÃO fazer

- **Não corrigir.** A skill produz diagnóstico, não código. Passo 6 sugere um próximo passo (revert / patch direto / `/triage`), mas quem dispara é o operador.
- Não pular a reprodução quando ela é viável — "deve ser X" sem teste é palpite, não diagnóstico.
- Não declarar causa-raiz sem evidência. Hipóteses inconclusivas são reportadas como tal.
- Não aplicar instrumentação (print/log temporário) — propor é parte do passo 4; aplicar fica com o operador no workspace dele.
- Não escrever ADR, plano ou linha de backlog dentro da skill — esses pertencem a `/new-adr` e `/triage`.
- Não fazer commits nem editar arquivos do projeto.
