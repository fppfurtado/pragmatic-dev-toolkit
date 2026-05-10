# captura automática de imprevistos durante /run-plan

## Contexto

Hoje `/run-plan` acumula itens fora-de-escopo via **backlog harvest** (passo 4.5), mas o gatilho de captura é **sinal explícito** — operador dizendo "registra no backlog" / "isso fica pra depois", ou reviewer marcando finding como out-of-scope. Imprevistos detectados pelo próprio agente durante execução (test_command falhando e contornado em vez de solucionado, hook do plugin bloqueando, superfície externa faltando do plano, bug colateral mencionado pelo operador na validação manual) ficam de fora — vira informação solta no log da skill, dependente do operador notar e capturar manualmente, ou pior: dependente do agente lembrar de cutucar o operador.

A mudança absorve o harvest atual num mecanismo único de **captura automática**, com gatilhos prescritos durante execução (passo 3) e durante validação manual (passo 4.2). Sem confirmação do operador no momento da gravação — o agente informa cada captura na hora ("capturei no backlog: <linha>") e materializa as linhas como bloco extra antes do `done`. Sinal explícito do operador continua funcionando, mas como um dos gatilhos do eixo automático, não como mecanismo separado.

**Linha do backlog:** captura automática de imprevistos durante /run-plan e validação manual

## Resumo da mudança

1. Substituir o passo 4.5 atual (`Backlog harvest`, com gatilho de sinal explícito) pelo novo passo `Captura automática de imprevistos`, com gatilhos prescritos.
2. Especificar gatilhos durante execução do passo 3:
   - **Falha contornada** — `test_command` (ou verificação textual equivalente) falha e o agente segue contornando (skip de teste, retry frágil, fallback ad-hoc) sem solucionar a causa-raiz.
   - **Finding fora-do-escopo** — reviewer (`code`, `qa`, `security`) levanta problema real que não pertence ao bloco corrente nem ao plano corrente.
   - **Hook bloqueando** — hook do plugin (`block_env.py`, `run_pytest_python.py` etc.) retorna exit ≠ 0 sinalizando gap real (não bloqueio esperado já absorvido pela mecânica do hook), e o agente pivota e segue.
   - **Superfície faltante** — sanity check de escopo do passo 2 detecta menção a superfície externa em `## Contexto`/`## Resumo da mudança` que não aparece em `## Arquivos a alterar`, e o operador escolhe `Continuar mesmo assim`.
3. Especificar gatilhos durante validação manual no passo 4.2:
   - **Divergência do plano** — operador reporta comportamento que diverge do esperado por `## Verificação manual` do plano corrente.
   - **Bug colateral** — operador menciona bug menor não relacionado ao gate corrente ("aproveitando, vi que X também tá errado").
4. Política unificada de gravação: o agente acumula capturas durante a skill, **informa o operador no momento de cada detecção** (mensagem curta, sem interromper o fluxo), e materializa as linhas em `## Próximos` do arquivo do papel `backlog` como **bloco extra** antes do done — implementar (write das linhas) → **passo de consolidação** (ver item 6) → revisor `code` → micro-commit. **Sem `AskUserQuestion` de confirmação** da captura em si (o operador já foi informado a cada detecção). Lista vazia → skip silente do bloco extra.
5. Atualizar `docs/philosophy.md` ("Ciclo de vida do backlog") para substituir referência ao "backlog harvest" pela "captura automática de imprevistos" e ajustar a descrição dos eixos.
6. **Extrair regra de consolidação para `docs/philosophy.md`** — hoje a mecânica de releitura + flag de duplicatas/obsolescência + pergunta condicional única vive inline no passo 5 do `/triage` SKILL.md. Promover para nova seção `## Consolidação do backlog` em `philosophy.md`, com critério único; `/triage` passo 5 e `/run-plan` novo passo 4.5 passam a **referenciar** a seção em vez de duplicar lógica. Operador valida uma única vez (se houver flags) — alinhado com "Convenção de pergunta ao operador".
7. Atualizar `CLAUDE.md` deste repo se houver referência direta ao "harvest" ou ao "passo 4.5 atual" — verificar durante execução; se não houver, este passo é skip.

## Arquivos a alterar

### Bloco 1 — docs/philosophy.md (extrair regra de consolidação) {reviewer: code}

Edit aditivo + cirúrgico:

- **Adicionar nova seção `## Consolidação do backlog`** (logo após `## Ciclo de vida do backlog` para coesão temática). Conteúdo:
  - Quando dispara: sempre que uma skill modificou o arquivo do papel `backlog` no fluxo corrente. Caminho que não tocou → skip silente.
  - Mecânica: (1) reler o backlog na íntegra após as edições; (2) flagar duplicatas (linhas recém-adicionadas vs. pré-existentes em `## Próximos`/`## Em andamento`/`## Concluídos`) e obsolescência (linha em `## Próximos` que vira redundante pela linha recém-registrada; inferência conservadora — só flagar quando sobreposição é nítida no texto); (3) sem flags → skip silente; (4) com flags → mostrar síntese ao operador + estado atual das seções tocadas; perguntar **uma vez** via enum (`AskUserQuestion`, header `Backlog`, opções `Está bom, prosseguir` e `Aplicar edits` — Other → operador descreve em prosa).
  - Onde aplica: `/triage` passo 5 (gravações da feature em curso e fora-de-escopo); `/run-plan` novo passo 4.5 (capturas automáticas materializadas como bloco extra).
- **Atualizar `## Ciclo de vida do backlog`** (linha que cita "antes do backlog harvest" no bullet `Em andamento → Concluídos`): substituir "backlog harvest" por "captura automática de imprevistos"; trocar "captura de novos itens deferidos" por "captura de imprevistos detectados pelo agente". Resto do bullet permanece.

### Bloco 2 — skills/triage/SKILL.md (encurtar passo 5 para referenciar) {reviewer: code}

Substituir o conteúdo enumerado do passo 5 (releitura + flagar + skip/perguntar) por referência única à nova seção `Consolidação do backlog` em `philosophy.md`. Manter o gate de disparo do passo 5 (condição "passo 4 modificou o arquivo do papel `backlog`") e a observação de que edits descritos pelo operador entram no commit unificado proposto no passo 6 — esses dois pontos são contexto local da skill, não pertencem à regra geral. Bullet de "O que NÃO fazer" relacionado (cerimônia de re-confirmar linhas, sem flags) permanece — válido sob a nova referência.

### Bloco 3 — skills/run-plan/SKILL.md {reviewer: code,qa}

Reescrever a mecânica de captura. Edits cirúrgicos:

- **Passo 3 — Loop por bloco**: adicionar nota geral, antes do enumerado, sobre observar gatilhos de captura automática durante execução (referir ao novo passo 4.5 para a lista). Não detalhar a lista aqui — fica concentrada no 4.5 para evitar duplicação.
- **Passo 4.2 — Plano com `## Verificação manual`**: estender com instrução de capturar para o backlog, automaticamente, dois eventos detectáveis no diálogo de validação manual: (a) divergência entre o report do operador e os passos de `## Verificação manual`; (b) bug colateral mencionado pelo operador fora do escopo do gate. Em ambos: agente registra na lista de captura, informa o operador na hora, e segue o gate sem interromper.
- **Passo 4.5 — Renomear de `Backlog harvest` para `Captura automática de imprevistos`**. Conteúdo novo:
  - Critério: lista mantida pelo agente desde o início do passo 3, alimentada pelos quatro gatilhos de execução (falha contornada, finding fora-do-escopo, hook bloqueando, superfície faltante) e pelos dois gatilhos de validação manual (divergência do plano, bug colateral). Sinal explícito do operador ("registra no backlog") cai sob "Bug colateral" ou "Finding fora-do-escopo" conforme o contexto — sem mecanismo separado.
  - Forma da linha: redação curta, em uma frase, descritiva do problema (não do gatilho). Ex.: "test de auth.py contornado com skip — investigar causa-raiz", não "falha contornada no bloco 2".
  - Materialização: lista vazia → **skip silente** (sem prompt cerimonial); lista não-vazia → tratar como **bloco extra**: (a) escrever as linhas em `## Próximos` do arquivo do papel `backlog`; (b) **rodar consolidação** referenciando `philosophy.md` → `## Consolidação do backlog` (releitura + flag + pergunta condicional única se houver flags); (c) revisor `code`; (d) micro-commit. **Sem pergunta de confirmação** sobre as capturas em si — o operador já foi informado a cada detecção; a única pergunta possível vem da consolidação, condicional a flags reais.
  - Casos especiais: papel `backlog` resolveu para "não temos" → skip silente do bloco extra; capturas viram apenas relato final ao operador (sem registro persistido).
- **Seção `## O que NÃO fazer`**: atualizar bullets relacionados ao harvest:
  - Remover ou reescrever `Não fabricar itens no harvest a partir de leitura tardia do diff` — gatilhos agora são prescritos. Substituto: `Não capturar com base em inferência tardia do diff — captura ocorre no momento do gatilho, não em pós-leitura`.
  - Manter `Não capturar itens que já foram absorvidos pelo plano corrente` (válido também para os novos gatilhos).
  - Adicionar: `Não pedir confirmação ao operador sobre as capturas em si — política é "informar e seguir". A única pergunta admitida no passo 4.5 é a da consolidação (condicional a flags reais; ver philosophy.md → "Consolidação do backlog")`.
  - Adicionar: `Não inverter a ordem entre informação ao operador e captura na lista — informar primeiro, registrar em seguida. Operador deve poder dizer "descarta esse" em prosa antes do bloco extra do passo 4.5 materializar`.
  - Manter o bullet sobre ordem 4.4 → 4.5 (transição final do backlog antes da captura).

### Bloco 4 — CLAUDE.md (este repo) {reviewer: code}

Verificar referências diretas ao "harvest" ou ao "passo 4.5 atual" na seção `## Skill workflow contract`. Se houver, ajustar para refletir o novo nome e gatilhos. Se não houver, **skip do bloco** — a alteração concentra-se nos blocos 1-3. Bloco mantido aqui como guard-rail.

## Verificação end-to-end

Não aplicável — este repo é o plugin (sem `test_command`). Validação substituída por `## Verificação manual` abaixo.

## Verificação manual

A skill `/run-plan` é meta-tool sem suite automatizada — validação manual é o gate efetivo. Em projeto-fixture com este plugin instalado, executar os cenários abaixo, **um por vez**, e confirmar cada bullet:

1. **Falha contornada**: plano com bloco que prescreve uma mudança que faz `test_command` falhar de forma persistente; quando o agente decide contornar (skip, retry frágil, fallback) em vez de solucionar:
   - Mensagem ao operador no momento da decisão: `capturei no backlog: <linha>`.
   - Ao fim da skill, antes do `done`, bloco extra micro-commit adiciona uma linha em `## Próximos` do `BACKLOG.md` descrevendo o problema (não o gatilho).
2. **Finding fora-do-escopo**: plano com bloco anotado `{reviewer: qa}` cujo reviewer levanta um problema real fora do escopo do bloco. Confirmar mensagem na hora + bloco extra ao fim.
3. **Hook bloqueando**: plano que toca arquivo que dispara hook do plugin (ex.: `.env` no `block_env.py`). O hook bloqueia, agente pivota. Confirmar captura — distinguir do bloqueio esperado já absorvido pela mecânica do hook (este último **não** captura).
4. **Superfície faltante**: plano com `## Resumo da mudança` mencionando "atualizar workflow CI" mas `## Arquivos a alterar` não listando arquivos `.github/workflows/`. Sanity check do passo 2 cutuca; operador escolhe `Continuar mesmo assim`. Confirmar captura.
5. **Divergência do plano** (validação manual): plano com `## Verificação manual` listando "X deve aparecer com cor azul"; operador reporta "X aparece com cor verde". Confirmar mensagem na hora + bloco extra ao fim. Validar que o gate **não fecha automaticamente** — agente continua aguardando "ok, valido" ou ajuste.
6. **Bug colateral** (validação manual): operador, durante validação, menciona "aproveitando, vi que Y também tá quebrado". Confirmar captura.
7. **Lista vazia**: rodar plano simples sem nenhum gatilho disparando. Confirmar **skip silente** do passo 4.5 — nada novo no backlog, sem prompt cerimonial.
8. **Operador descarta na janela**: durante execução, agente captura ("capturei: X"); operador responde em prosa "descarta esse" antes do bloco extra final. Confirmar que a linha não é gravada.
9. **Consolidação sem flags**: capturas geram linhas únicas, sem duplicata nem obsolescência com o estado pré-existente do backlog. Confirmar que o passo 4.5 materializa as linhas e fecha o bloco extra **sem pergunta** ao operador (consolidação skip silente).
10. **Consolidação com flags**: o backlog já tem linha em `## Próximos` semanticamente sobreposta a uma das capturas (ex.: pré-existente "investigar test de auth flaky" + captura "test de auth.py contornado com skip"). Confirmar que a consolidação dispara `AskUserQuestion` (header `Backlog`, opções `Está bom, prosseguir` / `Aplicar edits`), e que a opção `Aplicar edits` em prosa ("consolidar X+Y") é aplicada antes do micro-commit.
11. **Papel `backlog` desativado**: rodar a skill em projeto com `paths.backlog: null`. Capturas viram apenas relato final ao operador, sem write file e sem consolidação.
12. **Mensagens de informação**: ao longo dos cenários acima, validar que os avisos de captura são curtos (uma frase), não interrompem o fluxo da skill (skill continua sem aguardar resposta), e citam a linha que vai ser gravada.
13. **Cross-skill**: rodar `/triage` em fluxo separado e confirmar que o passo 5 (consolidação após gravar linha de feature) usa exatamente a mesma mecânica do 4.5 do `/run-plan` — sintoma de regra única em `philosophy.md`.

## Pendências de validação

- ~~**13 cenários acima** ainda não exercitados em projeto-fixture. Operador deve rodar cada cenário com este plugin instalado e marcar individualmente.~~ **Encerrada 2026-05-10:** uso real subsequente do plugin sem regressão observada nas áreas exercitadas; cenários permanecem documentados como contrato. Reabrir se sinal concreto de divergência surgir.
- ~~**Bloco 3 (run-plan/SKILL.md) — cobertura `qa-reviewer` pulada**: durante o `/run-plan`, o `qa-reviewer` esgotou limite de uso e não avaliou as edições do passo 4.5 do `SKILL.md` contra os 13 cenários. Revisitar quando o reviewer estiver disponível ou validar manualmente cada cenário quanto a coverage de invariantes do plano.~~ **Encerrada 2026-05-10:** subordinada ao item anterior — sem cenários pendentes de validação, cobertura formal pelo `qa-reviewer` perde objeto. Reabrir junto se regressão surgir.

## Notas operacionais

- **Janela de override do operador**: o intervalo entre "agente informa captura" e "bloco extra materializa as linhas" é a janela onde o operador pode dizer "descarta esse" (em prosa, sem enum). Documentar como comportamento, não como pergunta — operador pode usar a janela ou não.
- **Distinção hook bloqueando vs hook funcionando**: o gatilho 3 (Hook bloqueando) é para bloqueios que sinalizam **gap real** (ex.: `run_pytest_python.py` falhando persistentemente em arquivo aparentemente não-relacionado). O bloqueio esperado já absorvido pela mecânica (ex.: `block_env.py` impedindo edit em `.env` durante exploração) **não** é gatilho — é a função do hook. Critério prudencial do agente. Documentar como nota, não como árvore de decisão.
- **Sinal explícito do operador**: continua funcionando — operador dizendo "registra no backlog X" cai sob "Bug colateral" (validação manual) ou é incorporado pelo agente como captura imediata durante execução. Não há mecanismo separado nem prompt cerimonial.
- **Reviewer findings in-scope vs out-of-scope**: interpretação do agente lendo o relatório do reviewer. In-scope (corrigir antes do micro-commit do bloco) ≠ out-of-scope (capturar no backlog). Reviewer pode hintar, mas decisão é do agente — sem mudança no contrato dos reviewer agents.
