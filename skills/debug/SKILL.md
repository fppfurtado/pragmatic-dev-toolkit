---
name: debug
description: Diagnostica causa-raiz de sintoma (teste falhando, erro inesperado, comportamento divergente) por método científico. Produz diagnóstico, não fix. Stack-agnóstico.
---

# debug

Esta skill enforca **"não corrigir sem isolar a causa"**. Recebe um sintoma e produz um diagnóstico — não escreve código, não cria commit, não aplica instrumentação. Saída é texto na conversa: sintoma observado, reprodução, hipóteses testadas, causa-raiz com evidência, escopo de impacto, caminhos de correção possíveis. O operador decide o caminho depois.

## Argumentos

Sintoma operacionalizável. Exemplos:

- `/debug test_export_csv falhou com TimeoutError no CI`
- `/debug webhook /payment retorna 500 desde o deploy de ontem`
- `/debug datas saem com fuso errado em produção`

Sintoma vazio ou vago ("não está funcionando", "está bugado") → pedir precisão antes de prosseguir (passo 1).

## Pré-condições

Paths e comandos seguem **Resolução de papéis**. Roles consumidos são todos informacionais — papel ausente nunca é gap report, apenas reduz a base de hipóteses:

- `test_command` (default `make test`) — reproduzir teste falhando ou rodar a suíte que exerce o cenário.
- `ubiquitous_language` (default `docs/domain.md`) — consultar se o sintoma toca invariantes documentadas (RNxx ou equivalentes).
- `decisions_dir` (default `docs/decisions/`) — consultar se o sintoma envolve invariantes pós-erro (rollback, retry com efeito colateral, divergência de estado).
- `design_notes` (default `docs/design.md`) — consultar se o sintoma envolve integração externa.

## Passos

### 1. Precisar o sintoma

Perguntas de precisão são **prosa livre** — operador descreve em linguagem natural.

Entrada genérica → perguntar antes de hipotetizar:

- Qual ação produz o sintoma (comando, teste, request, fluxo manual)?
- Output observado vs esperado?
- Onde foi observado (dev local, CI, staging, prod)?
- Reprodutibilidade: sempre, às vezes, uma vez só?
- Mudou recentemente? Quando começou a falhar?

Sem sintoma operacionalizável, não avançar.

### 2. Reproduzir

- **Sintoma é teste:** rodar `test_command` resolvido restringindo ao alvo (filtro por nome em pytest, cargo, jest, go test).
- **Sintoma é runtime error:** identificar input/comando mínimo que dispara.
- **Sintoma intermitente** (race, flaky, dependência externa): reproduzir N vezes (default 5), reportar taxa observada. Análise prossegue mesmo sem reprodução determinística — diagnóstico fica sinalizado como **estatístico**.
- **Não-reprodutível localmente:** enumerar artefatos disponíveis (stack trace, logs, métricas, screenshot), prosseguir com evidência indireta e **sinalizar explicitamente** que a análise é especulativa.

Evitar pular para hipótese antes de ver o sintoma com os próprios olhos quando reprodução é viável.

### 3. Isolar

Estreitar a área suspeita antes de hipotetizar:

- Stack trace → módulo/função.
- `git log -- <arquivos suspeitos>` recente: o sintoma começou após qual commit?
- `git blame` nas linhas relacionadas ao erro.
- ADRs (`decisions_dir`) se o sintoma envolve invariantes pós-erro.
- `design_notes` se envolve integração externa com peculiaridades documentadas.
- `ubiquitous_language` para checar se o comportamento fere uma RNxx.

### 4. Hipotetizar e testar

Para cada hipótese plausível:

1. **Estado** em uma frase: "X falha porque Y".
2. **Condição que confirma** + **condição que refuta** explícitas.
3. **Observar:** rodar teste, ler código, sugerir instrumentação ao operador (não aplicar).
4. **Status:** confirmada / refutada / inconclusiva.

Limite: **parar após duas hipóteses consecutivas refutadas sem ganho de evidência** (mesmo erro, mesmo escopo, nenhuma pista nova) e reportar status no passo 5 (ramo "nenhuma hipótese fechou").

Manter ledger das hipóteses (frase + status + evidência) para o passo 5. ≥2 hipóteses examinadas → ledger entra como campo *Hipóteses testadas*.

### 5. Causa-raiz

Hipótese confirmada com evidência → formular diagnóstico nos campos abaixo:

- **Sintoma:** descrição operacional.
- **Hipóteses testadas:** ledger no formato `H<n> (<status>): <hipótese>. <evidência confirmadora/refutadora>`. Status canonical: `confirmada` / `refutada` / `inconclusiva`. **Omitir o campo** quando apenas 1 hipótese foi testada e confirmada — *Causa-raiz* sozinha basta.
- **Causa-raiz:** arquivo:linha + mecanismo (por que o código se comporta assim).
- **Evidência:** o que foi observado/rodado que comprova (output, log, diff).
- **Escopo de impacto:** quem mais é afetado? Outros call-sites? Outras invariantes correlacionadas?
- **Caminhos de correção (não execução):** um ou mais caminhos com trade-off explícito — revert do commit X, patch local pequeno (mudança mínima apontada), ou `/triage <intent>` se for mudança maior. Investigação revelar caminho único razoável → declarar **"caminho único razoável"** com motivo. Operador decide.

Nenhuma hipótese fechou no passo 4 → *Hipóteses testadas* carrega ledger completo (refutadas + inconclusivas); *Causa-raiz* é substituída por **palpite atual com nível de confiança baixa explicitado**; relato preserva observações para `/triage` (se for o caminho) ter base. Evidência incompleta é resultado válido; chute disfarçado de causa-raiz, não.

### 6. Reportar e devolver controle

Apresentar diagnóstico do passo 5 em formato curto e sugerir **próximo passo** em uma frase:

- **Revert** — investigação isolou sintoma a commit específico e revert é seguro (ex.: "revert de `<hash>` no branch atual").
- **Patch local** — mudança cirúrgica que cabe sem alinhamento prévio (ex.: "ajustar `<arquivo>:<linha>` — uma linha; commitar diretamente").
- **`/triage <intent>`** — fix é mudança maior (multi-arquivo, toca invariante/integração, exige plano). Diagnóstico completo (incluindo *Hipóteses testadas* quando presente) entra como insumo do `## Contexto` do plano.

## O que NÃO fazer

- **Não corrigir.** A skill produz diagnóstico, não código. Passo 6 sugere próximo passo (revert / patch / `/triage`), mas quem dispara é o operador. Sem commits, sem edição de arquivos do projeto.
- Não pular reprodução quando viável — "deve ser X" sem teste é palpite, não diagnóstico.
- Não declarar causa-raiz sem evidência. Hipóteses inconclusivas são reportadas como tal.
- Não aplicar instrumentação (print/log temporário) — propor é parte do passo 4; aplicar fica com o operador.
- Não escrever ADR, plano ou linha de backlog dentro da skill — pertencem a `/new-adr` e `/triage`.
