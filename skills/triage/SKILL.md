---
name: triage
description: Triagem da intenção do operador (feature, fix, refactor, mudança pontual): alinha contexto, levanta gaps e decide qual artefato (linha de backlog, plano, ADR ou atualização de domínio/design) é necessário antes de implementar. Use quando o operador propuser qualquer mudança que ainda não tenha plano ou linha de backlog.
---

# triage

Workflow de **alinhamento prévio** para qualquer mudança não-trivial — feature nova, fix que precisa de plano (rota saída de `/debug`), refactor com bifurcação arquitetural, alteração pontual que toca invariante. O objetivo é evitar que o pedido pule direto para código sem passar pelo protocolo flat-e-pragmático: `BACKLOG.md` curto e vivo, planos em `docs/plans/` só quando exigem alinhamento, ADR só para decisão estrutural, atualização de `docs/domain.md`/`docs/design.md` quando o entendimento evolui.

Esta skill **não implementa**. Ela produz os artefatos de alinhamento e devolve o controle ao operador.

## Pré-condições

Para cada papel necessário (`product_direction`, `ubiquitous_language`, `design_notes`, `decisions_dir`, `plans_dir`, `backlog`), aplicar **Resolução de papéis** (ver `docs/philosophy.md`): probe do canonical default → consultar bloco `<!-- pragmatic-toolkit:config -->` no CLAUDE.md → perguntar ao operador com resposta tri-state. A pergunta tri-state e a oferta de memorização seguem o **modo enum** definido em "Convenção de pergunta ao operador" (`AskUserQuestion`).

Resposta `não temos` é válida para papéis informacionais (`product_direction`, `ubiquitous_language`, `design_notes`, `decisions_dir`, `backlog`) — a skill segue sem aquele input. Skill **para com gap report** apenas se `plans_dir` resolve para `não temos` (é onde a skill grava planos — único output não-fungível). Gap report é prosa livre — o operador precisa do contexto de adoção mínima, não de enum.

Quando o caminho do passo 3 escolhido **for** "atualizar `ubiquitous_language`/`design_notes`" e o papel resolveu para `não temos`, a skill **propõe criar** o arquivo no caminho default (`docs/domain.md` ou `docs/design.md`) usando enum de duas opções (`Criar em <path canonical>` / `Não usamos esse papel`). Segunda opção registra `paths.<role>: null` no bloco de config (oferta única de memorização) — papel desativado para invocações futuras sem perguntar de novo. Mesmo mecanismo aplica-se a `backlog` quando o passo 4 está prestes a gravar linha e o papel resolveu para `não temos` — enum (`AskUserQuestion`, header `Backlog`) com opções `Criar em BACKLOG.md` e `Não usamos esse papel`; segunda opção registra `paths.backlog: null`.

## Argumentos

O usuário fornece a **intenção** da funcionalidade em linguagem natural. Pode ser:
- Frase curta: `/triage exportar movimentos do mês em CSV`
- Descrição com contexto: `/triage quando o webhook falhar, salvar o payload pra reprocessar depois`
- Vago: `/triage melhorar o fluxo de comprovante`

Se o input estiver vazio ou genericamente "o que vamos fazer hoje?", peça ao usuário a intenção antes de prosseguir.

## Passos

### 1. Carregar contexto mínimo

Os paths abaixo são as convenções default por papel; quando o projeto declara variantes (ver Resolução de papéis em `docs/philosophy.md`), usar os paths declarados.

Ler, **nesta ordem** (e só o que o pedido tocar):

1. Papel `product_direction` (default canonical `IDEA.md`) — para verificar se a intenção está alinhada à direção de produto.
2. Papel `ubiquitous_language` (default canonical `docs/domain.md`) — bounded contexts, linguagem ubíqua, agregados/entidades e invariantes (RNxx) se houver. Identificar quais o pedido toca.
3. Papel `backlog` (default canonical `BACKLOG.md`) — verificar se já existe item equivalente em **Próximos**, **Em andamento** ou **Concluídos**. Se existir, parar e reportar ao usuário. Se o papel resolveu para `não temos`, pular esta verificação.
4. Papel `design_notes` (default canonical `docs/design.md`) — só se a funcionalidade tocar uma das integrações externas listadas ali.
5. Papel `decisions_dir` (default canonical `docs/decisions/`) — listar ADRs cujo título seja relacionado; ler na íntegra apenas os que o pedido potencialmente contradiz ou estende.

Não ler arquivos de código nesta etapa. Esta é uma fase de alinhamento de intenção, não de design técnico.

### 2. Esclarecer gaps com o usuário

Antes de qualquer artefato, identificar lacunas e perguntar **só o que for bloqueante**. Áreas comuns de gap (use como checklist mental, não como questionário):

- **Escopo:** o que está dentro e o que fica de fora? Há um caso menor que resolve 80%?
- **Superfícies além do código de aplicação:** a feature toca configuração de runtime (variáveis de ambiente, segredos, templates de configuração), infraestrutura (compose, scripts de deploy, workflows externos como CI/serverless/orquestradores), documentação operacional (READMEs de infra/deploy), ou a própria automação do projeto (skills, rules, hooks)? Se sim, o plano DEVE listar os arquivos correspondentes em `## Arquivos a alterar`. Feature "código-completa" mas "em-produção-quebrada" é o anti-padrão a evitar.
- **Invariantes envolvidas:** alguma RN do `docs/domain.md` é tocada? Se sim, como o fluxo a respeita?
- **Integrações:** alguma das integrações externas listadas em `docs/design.md` entra? Há peculiaridade já documentada ali?
- **Persistência:** precisa estado novo? Migra schema? (gatilho potencial de ADR — ver passo 4.)
- **Aprendizado de domínio:** o pedido revela algo que ainda não está em `docs/domain.md` — bounded context novo, aggregate/entity novo, RN/invariante nova, conceito ubíquo novo, ou semântica alterada de algo já registrado?
- **Validação manual necessária?** A feature tem comportamento perceptível ao usuário final, fluxo crítico de produção ou integração externa frágil? Se sim, o plano deve incluir uma seção `## Verificação manual` (gate de "ok, vai pra produção"). Refactors puros, mudanças internas, ajustes de teste e doc-only não precisam — `make test` é gate suficiente.
  - **Quando o sim vem de surface não-determinística** — feature toca **parsing** (interpretação de input do usuário), **matching de strings** contra dado real (busca, normalização, fuzzy match), ou **comportamento de agente LLM** (instruções no prompt, regras de saída) — exigir antes do plano: (a) **forma do dado real** — pedir ao operador 1-2 exemplos concretos do formato em produção (separadores, prefixos, capitalização inconsistente, ids internos que não devem vazar); (b) **cenários enumerados** — `## Verificação manual` deve listar passos concretos que exercitem essas formas, não direção genérica tipo "validar via interface real". Sem enumeração, validação manual vira improvisação e bugs reais escapam (matching falha em formato de produção, prompt vaza id interno descoberto por sorte). Sub-bullet **não dispara** quando a primeira pergunta do gap resolveu "não".
- **Cobertura de teste necessária?** Heurística tri-state: (i) bloco de teste prescrito em `## Arquivos a alterar` com `{reviewer: qa}` quando a feature toca invariante (RNxx do `ubiquitous_language`), integração externa (`design_notes`), persistência, comportamento observável novo, ou é fix de bug com risco de regressão; (ii) só `## Verificação end-to-end` textual quando o gate automático cobre e nada de invariante novo entra; (iii) nada novo em testes para refactor puro ou doc-only. Convenção completa em `docs/philosophy.md` → "Cobertura de teste em planos".
- **Bifurcação arquitetural:** o pedido pode ser resolvido por dois ou mais caminhos com custo, manutenção ou modelo mental significativamente diferentes? Heurística: ao tentar mentalmente esboçar o plano, você consegue redigir dois planos distintos que ambos satisfazem a frase do operador, mas levam a estruturas, dependências ou UX diferentes? Verbos abertos ("registrar", "validar", "notificar", "processar", "armazenar", "interagir") são sintoma frequente. Ver `docs/philosophy.md`.

Se o usuário já forneceu o necessário, pular as perguntas. Se houver 1–3 gaps reais, perguntar de forma direta e curta. **Não fazer entrevista exaustiva** — o projeto é exploratório, decisões podem evoluir no fluxo. Modo de cada gap segue "Convenção de pergunta ao operador": gaps de **escolha discreta** (validação manual? sim/não; cobertura de teste? caminho i/ii/iii) usam enum via `AskUserQuestion`; gaps que pedem **explicação livre** (forma do dado real, exemplos de produção, justificativa de escopo) ficam em prosa. Gaps relacionados podem ser agrupados numa única chamada de `AskUserQuestion` (até 4 perguntas).

**Itens fora de escopo emergidos na conversa.** Ao longo do esclarecimento, manter atenção para coisas que o operador menciona mas que **não pertencem ao escopo desta feature** — TODO adjacente ("e a gente devia também renomear X um dia"), tech-debt revelado pela leitura, bug menor avistado de passagem, melhoria não-essencial. Capturá-los como candidatos a registro. Quando o papel `backlog` resolveu normalmente, viram **linhas separadas em `## Próximos`** — uma linha por item, distintas do artefato principal (mencionar explicitamente no passo 4). Quando o papel resolveu para `não temos`, os itens **não são gravados** — são reportados no passo 6. Se o operador disser "deixa pra lá" ou "isso a gente não vai fazer", descartar — captura é sugestão, não imposição.

Quando bifurcação é detectada, **uma pergunta nominal-comparativa é obrigatória** antes do plano. Modo: enum via `AskUserQuestion` (ver "Convenção de pergunta ao operador" em `docs/philosophy.md` → "Nomear bifurcações arquiteturais"). Forma canônica: opções nomeadas `(a) caminho-default-barato` e `(b) caminho-rico` com `description` carregando o trade-off concreto (custo, virtude entregue). Operador escolhe um caminho concreto ou usa "Other" para nomear uma terceira via que a skill não previu. A escolha vai para o `## Contexto` ou `## Resumo da mudança` do plano produzido — sem nomear, o caminho barato vence por omissão. **Se o operador já citou explicitamente uma das opções** na frase original (`/triage exportar CSV usando streaming`), pular a pergunta e registrar a escolha no plano direto.

### 3. Decidir o artefato

Com base no esclarecimento, escolher **um** dos caminhos. Em caso de dúvida, preferir o caminho mais leve.

| Caminho | Quando usar |
| --- | --- |
| **Só linha no BACKLOG** | Mudança pequena, foco claro, sem decisão estrutural nem integração nova. Maioria dos casos. |
| **Plano em `docs/plans/`** | Multi-arquivo, multi-fase, ou exige alinhamento prévio sobre a abordagem. |
| **ADR via `/new-adr`** | Decisão estrutural duradoura (persistência, biblioteca core, contrato de integração, política do sistema). Ver ADRs existentes para calibre. |
| **Atualizar `docs/domain.md`** | Apareceu bounded context novo, aggregate/entity novo, RN nova, conceito ubíquo novo, ou mudou semântica de algo do glossário. **Antes** de implementar. |
| **Atualizar `docs/design.md`** | Peculiaridade nova de integração descoberta na conversa (não no código). |

Combinações são comuns: um item pode virar **linha no backlog + ADR**, ou **plano + atualização de domain.md**. Não são mutuamente exclusivos.

### 4. Produzir os artefatos

Idioma de saída: **espelhar o idioma já em uso pelo projeto consumidor** (ver "Convenção de idioma" em `docs/philosophy.md`). Headers e prosa abaixo estão em PT-BR canonical; em projeto que usa outro idioma, traduzir headers e linhas para esse idioma e seguir o padrão dos artefatos existentes.

- **BACKLOG (papel: `backlog`):** comportamento depende da resolução do papel.
  - **Papel resolvido normalmente:** adicionar **uma linha** para a feature em curso. Frase de intenção, sem detalhamento. Escolha da seção depende do caminho:
    - **Caminho com plano** (decisão formal de executar): cutucar via enum (`AskUserQuestion`, header `Backlog`, opções `Próximos` (recomendado) / `Em andamento`). Operador escolhe; linha é gravada na seção escolhida. Ver `docs/philosophy.md` → "Ciclo de vida do backlog".
    - **Caminho sem plano** (linha pura, ADR-only, atualização de domínio sem plano associado): default direto em `## Próximos`. Sem cutucada — não há decisão de execução iminente para diferenciar.
    - Itens fora-de-escopo capturados no passo 2 entram sempre como **linhas separadas em `## Próximos`** — uma linha por item, distintas do artefato principal. Itens fora-de-escopo entram em `## Próximos` mesmo quando o artefato principal é plano/ADR/atualização de domínio (o backlog ganha linhas independentes da escolha de artefato principal).
  - **Papel resolvido para `não temos`:** disparar a proposta única de criação descrita na seção *Pré-condições* — enum (`AskUserQuestion`, header `Backlog`) com opções `Criar em BACKLOG.md` e `Não usamos esse papel`. Primeira opção cria arquivo no canonical com cabeçalho mínimo (`# Backlog\n\n## Próximos\n\n## Em andamento\n\n## Concluídos\n`) e prossegue como no caminho acima. Segunda opção registra `paths.backlog: null` no bloco de config (oferta única de memorização) e prossegue **sem gravar** — itens da feature e fora-de-escopo são reportados no passo 6.
- **Plano (papel: `plans_dir`):** criar `<plans_dir>/<slug>.md` (default: `docs/plans/<slug>.md`). Estrutura recomendada: `## Contexto` → `## Resumo da mudança` → `## Arquivos a alterar` → `## Verificação end-to-end` → (`## Verificação manual`, **se** a resposta ao gap "Validação manual necessária?" foi sim) → `## Notas operacionais`. Não inventar seções vazias. Quando o passo 1 identificou termos do `ubiquitous_language` que o pedido toca, incluir em `## Contexto` a linha `**Termos ubíquos tocados:** <Termo> (<categoria>), <Termo> (<categoria>), ...` — categorias: `bounded context`, `agregado`, `entidade`, `RN`, `conceito ubíquo`. A linha é o mensageiro do vocabulário entre alinhamento e execução: `/run-plan` lê o plano e tem o subconjunto relevante do domínio sem reler `docs/domain.md`. Pedidos que não tocam o domínio (refactor puro, doc-only, papel `ubiquitous_language` resolvido para "não temos") **não** incluem a linha — sem ruído. Quando a feature foi gravada como linha no backlog (caminho com papel resolvido normalmente), incluir também em `## Contexto` a linha `**Linha do backlog:** <texto exato da linha gravada>` — mensageiro de matching para `/run-plan` operar as transições de estado (ver `docs/philosophy.md` → "Ciclo de vida do backlog"). Em `## Arquivos a alterar`, anotação `{reviewer: <perfil>}` no header de cada subseção orienta o `/run-plan` na escolha do revisor — exemplo canônico: `### Bloco 1 — auth.py {reviewer: security}`. Schema completo (perfis, múltiplos perfis, alias deprecado) em `docs/philosophy.md` → "Anotação de revisor em planos". Sem anotação, default `code-reviewer`.
- **ADR:** invocar a skill `/new-adr "<título>"` (não duplicar a lógica dela aqui). Reportar ao usuário e seguir.
- **`docs/domain.md` / `docs/design.md` (papéis: `ubiquitous_language` / `design_notes`):** edit cirúrgico no arquivo existente. Preservar tom e estrutura.

Para slug de plano: lowercase, espaços/acentos→hífens, curto e descritivo (ex.: `exportar-movimentos-csv`).

### 5. Revisão do backlog

Disparar **apenas** se o passo 4 modificou o arquivo do papel `backlog` (linha da feature em curso, linhas de fora-de-escopo emergidas no passo 2, ou ambas). Caminho que não tocou o backlog (ex.: atualização pura de `ubiquitous_language`/`design_notes`, ADR delegada a `/new-adr` sem linha de backlog acompanhante, papel `backlog` resolvido para "não temos") **pula este passo silenciosamente**.

Quando dispara:

1. **Reler** o arquivo do backlog na íntegra após as edições do passo 4.
2. **Flagar** (não decidir):
   - **Duplicatas** entre linhas recém-adicionadas (incluindo itens fora-de-escopo do passo 2) e linhas pré-existentes em `## Próximos`/`## Em andamento`/`## Concluídos`.
   - **Obsolescência**: linha em `## Próximos` que vira redundante pela feature recém-registrada (ex.: nova linha "exportar movimentos em CSV" cobre item antigo "exportar movimentos como planilha"). Inferência conservadora — só flagar quando a sobreposição é nítida no texto, não em similaridade vaga.
3. **Sem flags** → skip silente. As linhas adicionadas no passo 4 já foram decididas pelo operador; perguntar `Ok?` para confirmá-las novamente é cerimônia (ver `docs/philosophy.md` → "Convenção de pergunta ao operador"). Gate fecha sem ruído.
4. **Com flags** → **mostrar** ao operador a síntese dos flags e o estado atual de `## Próximos` (e `## Em andamento`/`## Concluídos` apenas se um flag tocar essas seções), com as linhas recém-adicionadas marcadas. **Perguntar uma vez** via enum (`AskUserQuestion`, header `Backlog`, opções `Está bom, prosseguir` e `Aplicar edits` — Other → operador descreve em prosa quais edits, ex.: consolidar duplicatas X+Y, remover linha obsoleta Z, reordenar). Edits descritos pelo operador são aplicados ao arquivo do backlog e ficam parte do mesmo commit unificado proposto no passo 6.

### 6. Reportar, propor commit e devolver controle

Ao final, reportar ao usuário em formato curto:

- O que foi registrado (linha de backlog, plano, ADR, atualização de domínio).
- Caminhos dos arquivos criados/alterados.

Quando `backlog` resolveu para `não temos`, acrescentar uma seção curta marcada como **"Itens não registrados (papel `backlog` desativado):"** listando: (a) a frase de intenção que **teria sido gravada** para a feature em curso; (b) cada item fora-de-escopo capturado no passo 2. Sem editorialização adicional — operador decide o destino.

Em seguida, **propor um commit único** agrupando todos os artefatos de alinhamento produzidos no passo 4. Mensagem deve seguir a **convenção de commits do projeto consumidor** (ver `docs/philosophy.md` → "Convenção de commits"; default canonical Conventional Commits em inglês, tipo `docs:` ou `chore:` conforme o conteúdo). Aguardar confirmação explícita do operador via enum (`AskUserQuestion`, header `Commit`) com opções `Confirmar e commitar` e `Editar mensagem` (Other → mensagem alternativa). Se não houver alterações novas para commitar (ex.: caminho escolhido foi delegar para `/new-adr` que já fez seu próprio commit, ou nada foi alterado em arquivos versionados), pular esta etapa.

Por que o commit importa aqui: `/run-plan` cria worktree a partir do HEAD do branch atual. Artefatos uncommitted ficam fora da worktree — o próprio plano que `/run-plan` tentaria executar não estaria visível lá. Commitar agora fecha esse gap antes do salto para execução.

Por fim, sugerir o **próximo passo** (uma frase): "implementar agora via /run-plan <slug>", "validar o plano antes de codar", "preencher o ADR e voltar".

Não começar a implementar. Quem decide o salto para código é o operador.

## O que NÃO fazer

- Não implementar a funcionalidade nesta skill — ela é puro alinhamento.
- Não criar plano para mudança que cabe em uma linha do backlog. Plano é exceção, não regra.
- Não criar ADR para escolha tática (nome de função, organização interna de um módulo). ADR é decisão estrutural duradoura.
- Não duplicar conteúdo de `CLAUDE.md`, `domain.md` ou `design.md` no plano — referenciar.
- Não preencher conteúdo de ADR — delegar para `/new-adr`.
- Não commitar os artefatos de alinhamento sem confirmação explícita do operador — propor mensagem e aguardar.
- Não pular a revisão do backlog (passo 5) quando o passo 4 modificou o arquivo do papel `backlog` — releitura e flag de duplicatas/obsolescência sempre rodam. O que pula com flags vazios é a **pergunta**, não a checagem.
- Não perguntar no passo 5 quando nenhum flag de duplicata/obsolescência disparou — linhas já confirmadas no passo 4 não precisam de re-confirm.
- Não consolidar, remover ou reordenar linhas do backlog sem confirmação explícita do operador na pergunta do passo 5.
- Não gravar `**Linha do backlog:**` no plano quando o papel `backlog` resolveu para "não temos" ou quando o caminho não produziu linha — ausência da anotação é o sinal de skip silente para `/run-plan`.
- Não cutucar a escolha de seção (`Próximos` / `Em andamento`) quando o caminho não inclui plano — sem decisão de execução iminente, default `Próximos` direto.
