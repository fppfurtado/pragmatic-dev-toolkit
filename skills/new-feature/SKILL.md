---
name: new-feature
description: Conduz o fluxo de uma nova funcionalidade alinhando intenção, levantando gaps e decidindo qual artefato (linha de backlog, plano, ADR ou atualização de domínio/design) é necessário antes de implementar. Use quando o operador propuser uma feature, mudança de comportamento ou ideia exploratória.
---

# new-feature

Workflow de **alinhamento prévio** para uma funcionalidade nova. O objetivo é evitar que o pedido pule direto para código sem passar pelo protocolo flat-e-pragmático: `BACKLOG.md` curto e vivo, planos em `docs/plans/` só quando exigem alinhamento, ADR só para decisão estrutural, atualização de `docs/domain.md`/`docs/design.md` quando o entendimento evolui.

Esta skill **não implementa**. Ela produz os artefatos de alinhamento e devolve o controle ao operador.

## Pré-condições

Para cada papel necessário (`product_direction`, `ubiquitous_language`, `design_notes`, `decisions_dir`, `plans_dir`, `backlog`), aplicar **Resolução de papéis** (ver `docs/philosophy.md`): probe do canonical default → consultar bloco `<!-- pragmatic-toolkit:config -->` no CLAUDE.md → perguntar ao operador com resposta tri-state.

Resposta `não temos` é válida para papéis informacionais (`product_direction`, `ubiquitous_language`, `design_notes`, `decisions_dir`) — a skill segue sem aquele input. Skill **para com gap report** apenas se `plans_dir` ou `backlog` resolvem para `não temos` (são onde a skill grava saída). Nesse caso, indicar ao operador o caminho de adoção mínimo antes de prosseguir.

Quando o caminho do passo 3 escolhido **for** "atualizar `ubiquitous_language`/`design_notes`" e o papel resolveu para `não temos`, a skill **propõe criar** o arquivo no caminho default (`docs/domain.md` ou `docs/design.md`) e pergunta uma vez. Resposta `não, não usamos` registra `paths.<role>: null` no bloco de config (oferta única de memorização) — papel desativado para invocações futuras sem perguntar de novo.

## Argumentos

O usuário fornece a **intenção** da funcionalidade em linguagem natural. Pode ser:
- Frase curta: `/new-feature exportar movimentos do mês em CSV`
- Descrição com contexto: `/new-feature quando o webhook falhar, salvar o payload pra reprocessar depois`
- Vago: `/new-feature melhorar o fluxo de comprovante`

Se o input estiver vazio ou genericamente "o que vamos fazer hoje?", peça ao usuário a intenção antes de prosseguir.

## Passos

### 1. Carregar contexto mínimo

Os paths abaixo são as convenções default por papel; quando o projeto declara variantes (ver Resolução de papéis em `docs/philosophy.md`), usar os paths declarados.

Ler, **nesta ordem** (e só o que o pedido tocar):

1. Papel `product_direction` (default canonical `IDEA.md`) — para verificar se a intenção está alinhada à direção de produto.
2. Papel `ubiquitous_language` (default canonical `docs/domain.md`) — linguagem ubíqua e invariantes (RNxx) se houver. Identificar quais o pedido toca.
3. Papel `backlog` (default canonical `BACKLOG.md`) — verificar se já existe item equivalente em **Próximos**, **Em andamento** ou **Concluídos**. Se existir, parar e reportar ao usuário.
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
- **Aprendizado de domínio:** o pedido revela algo que ainda não está em `docs/domain.md`?
- **Validação manual necessária?** A feature tem comportamento perceptível ao usuário final, fluxo crítico de produção ou integração externa frágil? Se sim, o plano deve incluir uma seção `## Verificação manual` (gate de "ok, vai pra produção"). Refactors puros, mudanças internas, ajustes de teste e doc-only não precisam — `make test` é gate suficiente.
- **Bifurcação arquitetural:** o pedido pode ser resolvido por dois ou mais caminhos com custo, manutenção ou modelo mental significativamente diferentes? Heurística: ao tentar mentalmente esboçar o plano, você consegue redigir dois planos distintos que ambos satisfazem a frase do operador, mas levam a estruturas, dependências ou UX diferentes? Verbos abertos ("registrar", "validar", "notificar", "processar", "armazenar", "interagir") são sintoma frequente. Ver `docs/philosophy.md`.

Se o usuário já forneceu o necessário, pular as perguntas. Se houver 1–2 gaps reais, perguntar de forma direta e curta. **Não fazer entrevista exaustiva** — o projeto é exploratório, decisões podem evoluir no fluxo.

Quando bifurcação é detectada, **uma pergunta nominal-comparativa é obrigatória** antes do plano. Forma canônica: *"Para X, prefere (a) caminho-default-barato ou (b) caminho-rico? Trade-off: (a) é mais simples e mais barato; (b) entrega <virtude-B> ao custo de <custo-B>."* A escolha vai para o `## Contexto` ou `## Resumo da mudança` do plano produzido — sem nomear, o caminho barato vence por omissão. **Se o operador já citou explicitamente uma das opções** na frase original (`/new-feature exportar CSV usando streaming`), pular a pergunta nominal-comparativa e registrar a escolha no plano direto.

### 3. Decidir o artefato

Com base no esclarecimento, escolher **um** dos caminhos. Em caso de dúvida, preferir o caminho mais leve.

| Caminho | Quando usar |
| --- | --- |
| **Só linha no BACKLOG** | Mudança pequena, foco claro, sem decisão estrutural nem integração nova. Maioria dos casos. |
| **Plano em `docs/plans/`** | Multi-arquivo, multi-fase, ou exige alinhamento prévio sobre a abordagem. |
| **ADR via `/new-adr`** | Decisão estrutural duradoura (persistência, biblioteca core, contrato de integração, política do sistema). Ver ADRs existentes para calibre. |
| **Atualizar `docs/domain.md`** | Apareceu RN nova, conceito ubíquo novo, ou mudou semântica de algo do glossário. **Antes** de implementar. |
| **Atualizar `docs/design.md`** | Peculiaridade nova de integração descoberta na conversa (não no código). |

Combinações são comuns: um item pode virar **linha no backlog + ADR**, ou **plano + atualização de domain.md**. Não são mutuamente exclusivos.

### 4. Produzir os artefatos

Idioma de saída: **espelhar o idioma já em uso pelo projeto consumidor** (ver "Convenção de idioma" em `docs/philosophy.md`). Headers e prosa abaixo estão em PT-BR canonical; em projeto que usa outro idioma, traduzir headers e linhas para esse idioma e seguir o padrão dos artefatos existentes.

- **BACKLOG (papel: `backlog`):** adicionar **uma linha** em `## Próximos` (ou `## Em andamento` se já vai começar). Frase de intenção, sem detalhamento.
- **Plano (papel: `plans_dir`):** criar `<plans_dir>/<slug>.md` (default: `docs/plans/<slug>.md`). Estrutura recomendada: `## Contexto` → `## Resumo da mudança` → `## Arquivos a alterar` → `## Verificação end-to-end` → (`## Verificação manual`, **se** a resposta ao gap "Validação manual necessária?" foi sim) → `## Notas operacionais`. Não inventar seções vazias. Em `## Arquivos a alterar`, anotação `{reviewer: <perfil>}` no header de cada subseção orienta o `/run-plan` na escolha do revisor — exemplo canônico: `### Bloco 1 — auth.py {reviewer: security}`. Schema completo (perfis, múltiplos perfis, alias deprecado) em `docs/philosophy.md` → "Anotação de revisor em planos". Sem anotação, default `code-reviewer`.
- **ADR:** invocar a skill `/new-adr "<título>"` (não duplicar a lógica dela aqui). Reportar ao usuário e seguir.
- **`docs/domain.md` / `docs/design.md` (papéis: `ubiquitous_language` / `design_notes`):** edit cirúrgico no arquivo existente. Preservar tom e estrutura.

Para slug de plano: lowercase, espaços/acentos→hífens, curto e descritivo (ex.: `exportar-movimentos-csv`).

### 5. Reportar e devolver controle

Ao final, reportar ao usuário em formato curto:

- O que foi registrado (linha de backlog, plano, ADR, atualização de domínio).
- Caminhos dos arquivos criados/alterados.
- **Próximo passo sugerido** (uma frase): "implementar agora", "validar o plano antes de codar", "preencher o ADR e voltar".

Não começar a implementar. Quem decide o salto para código é o operador.

## O que NÃO fazer

- Não implementar a funcionalidade nesta skill — ela é puro alinhamento.
- Não criar plano para mudança que cabe em uma linha do backlog. Plano é exceção, não regra.
- Não criar ADR para escolha tática (nome de função, organização interna de um módulo). ADR é decisão estrutural duradoura.
- Não duplicar conteúdo de `CLAUDE.md`, `domain.md` ou `design.md` no plano — referenciar.
- Não preencher conteúdo de ADR — delegar para `/new-adr`.
