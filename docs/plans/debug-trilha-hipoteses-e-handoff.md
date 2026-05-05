# Polimento de `/debug`: trilha de hipóteses, handoff explícito e referência à Convenção de pergunta

## Contexto

Quatro polimentos editoriais em `skills/debug/SKILL.md` — sem bug, apenas bordas menos espelhadas com as outras skills do toolkit:

- **Referência à "Convenção de pergunta ao operador" ausente.** Outras skills (`/triage`, `/run-plan`, `/release`, `/new-adr`) citam a convenção quando perguntam ao operador. `/debug` passo 1 lista 5 perguntas de precisão sem explicitar o modo (prosa). Padronizar fecha a lacuna.
- **Handoff diluído.** O fechamento "skill termina aqui, operador escolhe revert/patch/`/triage`" hoje aparece em dois lugares (campo *Caminhos de correção* do passo 5 + seção `## O que NÃO fazer`), mas falta o passo final explícito que `/triage` e `/release` têm ("Reportar e devolver controle"). O limiar fica embaçado.
- **`/triage` como handoff estruturado.** Quando o caminho é "mudança maior", a saída do `/debug` é insumo direto de `/triage <intent>`. Hoje só o nome da skill aparece como opção; falta nomear que a causa-raiz vira contexto natural do `## Contexto` do plano.
- **Trilha de hipóteses não-formalizada.** Passo 4 disciplina a investigação (estado / condição confirma / condição refuta / status), mas o passo 5 só apresenta a hipótese vencedora. Refutadas/inconclusivas ficam só na conversa, sem shape no diagnóstico final. Três funções perdidas:
  - Anti-confirmation-bias auditável — operador vê o que foi descartado e por quê; sem isso, a causa-raiz parece evidente em retrospecto e a investigação não fica auditável.
  - Insumo para `/triage` — hipóteses refutadas viram contexto natural ("não fizemos X porque H2 falhou em Y") no `## Contexto` do plano que o operador eventualmente abrir.
  - Forma para o ramo "nenhuma hipótese fechou" — o passo 5 já prevê esse ramo mas sem shape; o ledger dá o formato.

**Decisões já fechadas (não revisitar):**

- **Quatro mudanças num único bloco.** Mesmo arquivo (`skills/debug/SKILL.md`), mesma natureza (prosa de skill), revisor único (`code`). Bloquear isso seria fragmentação artificial.
- **Trilha de hipóteses com guardrail YAGNI.** Emitir ledger (`H1`, `H2`, …) **apenas quando ≥2 hipóteses foram testadas no passo 4**. Caso 1-hipótese-confirmada, *Causa-raiz* sozinha basta — `H1` isolado é cerimônia. Espelha o padrão "lista vazia → skip silente" de `/run-plan` 4.5.
- **Posição do ledger no diagnóstico.** Campo separado **antes** de *Causa-raiz* — operador vê o caminho, não só o destino. Ledger não substitui *Causa-raiz*; complementa.
- **Formato do ledger.** `H<n> (<status>): <hipótese em uma frase>. <evidência confirmadora ou refutadora>`. Status canonical: `confirmada` / `refutada` / `inconclusiva` (espelha o vocabulário já em uso no passo 4).
- **Não tocar `docs/philosophy.md`.** A "Convenção de pergunta ao operador" já existe e cobre o caso — `/debug` apenas passa a citá-la. Sem nova guarda na philosophy.
- **Sem mudança no frontmatter `description`.** Comportamento de invocação não muda; só a forma da saída.

## Resumo da mudança

Bloco único de quatro edits coordenados em `skills/debug/SKILL.md`:

1. **Passo 1: citar "Convenção de pergunta ao operador".** Frase introdutória explicitando que as perguntas de precisão são prosa livre (não enum), com link à seção em `docs/philosophy.md`.
2. **Passo 4: nota de saída para o ledger.** Acréscimo curto ao fim do passo dizendo que o ledger das hipóteses (frase + status final) deve ficar acessível para o passo 5 quando ≥2 hipóteses foram examinadas.
3. **Passo 5: introduzir campo *Hipóteses testadas* condicional + nomear `/triage <intent>` como handoff estruturado.** Campo novo entre *Sintoma* e *Causa-raiz*, emitido apenas quando ≥2 hipóteses passaram pelo passo 4. Atualizar texto introdutório (cardinalidade variável: cinco ou seis campos). Reescrever bullet *Caminhos de correção* citando que o diagnóstico completo é insumo do `## Contexto` de `/triage`. Reescrever o parágrafo final ("Se nenhuma hipótese fechou…") para citar o ledger.
4. **Novo passo 6: "Reportar e devolver controle".** Espelha o passo 6 de `/triage` e o passo 5 de `/release`. Síntese curta + sugestão de próximo passo numa frase (revert / patch / `/triage <intent>`) + sinal explícito de fim. Atualizar `## O que NÃO fazer`: reescrever o item "Não corrigir" para apontar o passo 6 e adicionar guarda contra emitir o ledger com hipótese única.

## Arquivos a alterar

### Bloco único — Polimento de `skills/debug/SKILL.md` {reviewer: code}

- `skills/debug/SKILL.md` passo 1 ("Precisar o sintoma"):
  - **Adicionar frase introdutória** antes da lista de perguntas: "Perguntas de precisão são **prosa livre** — operador descreve em linguagem natural (ver 'Convenção de pergunta ao operador' em `docs/philosophy.md`); enum não cabe aqui porque a resposta esperada é narrativa, não escolha discreta."

- `skills/debug/SKILL.md` passo 4 ("Hipotetizar e testar"):
  - **Adicionar nota ao fim do passo** (após o parágrafo sobre o limite "duas hipóteses consecutivas refutadas"): "Manter o ledger das hipóteses (frase + status final + evidência) acessível para o passo 5. Quando ≥2 hipóteses foram examinadas, o ledger entra como campo *Hipóteses testadas* do diagnóstico final."

- `skills/debug/SKILL.md` passo 5 ("Causa-raiz"):
  - **Reescrever a frase introdutória** ("Quando uma hipótese é confirmada com evidência, formular o diagnóstico em cinco campos") para: "Quando uma hipótese é confirmada com evidência, formular o diagnóstico nos campos abaixo — **cinco** quando uma única hipótese foi testada e confirmada; **seis** quando ≥2 hipóteses passaram pelo passo 4 (o campo *Hipóteses testadas* entra)."
  - **Inserir campo novo** *entre* *Sintoma* e *Causa-raiz*:
    > **Hipóteses testadas:** ledger das hipóteses examinadas no passo 4 — formato por linha `H<n> (<status>): <hipótese em uma frase>. <evidência confirmadora ou refutadora>`. Status canonical: `confirmada` / `refutada` / `inconclusiva`. **Omitir o campo** quando apenas uma hipótese foi testada e confirmada — *Causa-raiz* sozinha basta (espelha "lista vazia → skip silente" em `/run-plan` 4.5).
  - **Reescrever o bullet *Caminhos de correção***:
    - Atual: "Caminhos de correção (não execução): **um ou mais caminhos** com trade-off explícito — revert do commit X, patch local pequeno (apontar mudança mínima), ou `/triage` se virar mudança maior. Se a investigação revelar caminho único razoável, declarar **'caminho único razoável'** com motivo (ex.: 'revert é a única opção segura porque o commit X introduziu corrupção de dados que se acumula'). Operador decide."
    - Novo: "Caminhos de correção (não execução): **um ou mais caminhos** com trade-off explícito — revert do commit X, patch local pequeno (apontar mudança mínima), ou `/triage <intent-do-fix>` se virar mudança maior. No último caso, o diagnóstico completo (incluindo *Hipóteses testadas* quando presente) é insumo natural do `## Contexto` do plano que `/triage` vai produzir; hipóteses refutadas viram contexto de 'por que não fizemos X'. Se a investigação revelar caminho único razoável, declarar **'caminho único razoável'** com motivo (ex.: 'revert é a única opção segura porque o commit X introduziu corrupção de dados que se acumula'). Operador decide."
  - **Reescrever o parágrafo final** ("Se nenhuma hipótese fechou ao fim do passo 4…") para: "Se nenhuma hipótese fechou ao fim do passo 4: o campo *Hipóteses testadas* carrega o ledger completo (refutadas + inconclusivas), *Causa-raiz* é substituída por **palpite atual com nível de confiança baixa explicitado**, e o relato preserva o que foi observado para que `/triage` (se for esse o caminho) tenha base. Evidência incompleta é resultado válido; chute disfarçado de causa-raiz, não."

- `skills/debug/SKILL.md` — **adicionar passo 6 novo**, após o passo 5 e antes da seção `## O que NÃO fazer`:
  ```markdown
  ### 6. Reportar e devolver controle

  Apresentar o diagnóstico (cinco ou seis campos conforme o passo 5) em formato curto na conversa e sugerir o **próximo passo** numa frase, escolhido entre:

  - **Revert** — quando a investigação isolou o sintoma a um commit específico e o revert é seguro (ex.: "revert de `<hash>` no branch atual").
  - **Patch local** — quando a mudança é cirúrgica e cabe sem alinhamento prévio (ex.: "ajustar `<arquivo>:<linha>` — uma linha; commitar diretamente").
  - **`/triage <intent-do-fix>`** — quando o fix é mudança maior (multi-arquivo, toca invariante/integração, exige plano). O diagnóstico completo entra como insumo do `## Contexto` do plano.

  Skill termina aqui. Quem dispara o caminho escolhido é o operador.
  ```

- `skills/debug/SKILL.md` seção `## O que NÃO fazer`:
  - **Reescrever o primeiro item** ("Não corrigir…") para incluir o passo 6: "**Não corrigir.** A skill produz diagnóstico, não código. Passo 6 sugere um próximo passo (revert / patch direto / `/triage`), mas quem dispara é o operador."
  - **Adicionar guarda nova** ao fim da lista: "Não emitir o campo *Hipóteses testadas* quando apenas uma hipótese foi testada e confirmada — `H1` isolado é cerimônia. Mesma forma do 'lista vazia → skip silente' de `/run-plan` 4.5."

## Verificação manual

Repo não tem suite de testes (`test_command: null` em `CLAUDE.md`). Validação é instalação local + smoke test no Claude Code. As superfícies alteradas mudam comportamento de agente LLM (instruções de prompt) — cenários enumerados, não direção genérica.

1. **Instalar o plugin localmente** num projeto consumidor que já usa o toolkit: `/plugin install /path/to/pragmatic-dev-toolkit --scope project`. Confirmar que `/debug` aparece em `/help`.
2. **Cenário 1-hipótese (ledger ausente):** num projeto consumidor com bug óbvio (ex.: teste falha por `KeyError: 'foo'` em código que não inicializa a chave; uma única hipótese confirma na primeira tentativa), rodar `/debug <sintoma>`. Confirmar que o diagnóstico final tem **5 campos** (Sintoma, Causa-raiz, Evidência, Escopo, Caminhos de correção) — campo *Hipóteses testadas* **omitido**.
3. **Cenário ≥2-hipóteses (ledger presente):** induzir cenário com ambiguidade real — bug onde duas causas plausíveis competem (ex.: timeout em CI: pode ser flaky por dependência externa ou race condition; investigação refuta flaky e confirma race). Rodar `/debug <sintoma>`. Confirmar que o diagnóstico tem **6 campos**, com o ledger imediatamente após *Sintoma*: `H1 (refutada): flaky por dependência externa. <evidência refutadora>` / `H2 (confirmada): race em <local>. <evidência confirmadora>`.
4. **Cenário "nenhuma hipótese fechou":** rodar `/debug` em sintoma intermitente sem reprodução determinística e com hipóteses todas inconclusivas/refutadas. Confirmar que o ledger lista todas as Hs com seus status e que *Causa-raiz* é substituída por "palpite atual" com confiança explicitada.
5. **Handoff `/triage`:** após cenário do passo 3, escolher o caminho `/triage <intent>` na sugestão do passo 6 e rodar a skill em seguida. Confirmar que o operador consegue colar o diagnóstico no input do `/triage` e que o `## Contexto` do plano produzido cita as hipóteses refutadas como "por que não fizemos X".
6. **Handoff revert / patch:** rodar `/debug` em bug com causa óbvia (commit recente que quebrou comportamento). Confirmar que o passo 6 sugere `revert de <hash>` em uma frase e que a skill encerra explicitamente ("Skill termina aqui. Quem dispara o caminho escolhido é o operador.").
7. **Passo 1 — modo prosa:** rodar `/debug "está bugado"` (sintoma vago). Confirmar que a skill pergunta as 5 questões de precisão em **prosa livre**, não via `AskUserQuestion`.

## Notas operacionais

- **Plano single-block.** Mesmo arquivo, mesma natureza, revisor único. Não há dependência de ordem entre os 4 edits — `code-reviewer` revisa o diff agregado.
- **Worktree precisa de `.worktreeinclude`.** Verificar antes de rodar `/run-plan` que o arquivo lista pelo menos `skills/`, `docs/`, `CLAUDE.md`. Sem isso, a worktree não vê os arquivos a alterar nem o `philosophy.md` de referência.
- **`test_command` é null neste repo.** Baseline de `/run-plan` cai para inspeção textual — para markdown puro, baseline é trivialmente verde. O bloco passa por `code-reviewer` antes do micro-commit.
- **Smoke test depende de projeto consumidor.** Worktree do `/run-plan` não roda `/debug` sobre si mesma — skill só opera em sessão Claude Code real com plugin instalado. Cenários do `## Verificação manual` acontecem na próxima invocação real.
- **Após merge:** rodar `/release patch` para v1.15.1 (refactor de skill, sem novo capability surface). CHANGELOG ganha entrada sob `### Changed`.
