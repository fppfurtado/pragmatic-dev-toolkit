# ADR-006: Preferência por enum quando há bifurcação discreta na pergunta ao operador

**Data:** 2026-05-07
**Status:** Aceito

## Origem

- **Investigação:** Operador relatou em uso real (sessão de 2026-05-07) que perguntas continuam emergindo em prosa nos SKILLs do toolkit mesmo após ADR-002 eliminar 4 gates de cutucada em `/run-plan`. Auditoria identificou 7 zonas com prosa-com-bifurcação onde `AskUserQuestion` daria UX mais leve (Enter/seta direcional vs digitar palavras). Critério atual em `philosophy.md` → "Convenção de pergunta ao operador" — *"quando a maioria das respostas reais cairia em 'Other' do enum, o modo certo era prosa desde o início"* — estava sendo interpretado de forma a manter prosa em casos onde **uma** resposta comum é discreta (ex.: `/run-plan` §3.3 sanity check de docs: prosa porque listagem de arquivos é Other-bound, mas "consistente" também é resposta frequente e discreta).

## Contexto

Toolkit já tem mecânica de `AskUserQuestion` documentada em `CLAUDE.md` → "AskUserQuestion mechanics" (header ≤ 12 chars, 2-4 options, `Other` automático, `multiSelect`, `(Recommended)` na primeira) e princípio editorial em `philosophy.md` → "Convenção de pergunta ao operador". ADR-002 (zero-gate) já estabeleceu que **eliminar** perguntas cerimoniais é prioridade — onde houver decisão genuína, escolher a forma mais leve é a sequência natural.

O critério atual em philosophy.md tem leitura ambígua: *"quando **a maioria** das respostas reais cairia em 'Other' do enum, o modo certo era prosa desde o início"*. Skill author lê e interpreta como: "uma resposta livre dominante autoriza prosa". Mas se há ≥1 resposta discreta também comum, o caminho-curto (Enter/seta) some — operador digita Other mesmo quando teria escolhido a discreta.

Exemplos concretos do drift:
- `/run-plan` §3.2 (validação manual): pede "ok, valido" em prosa. Resposta "validei" é discreta + frequente; resposta "falhou" pede descrição (Other-natural). Hoje operador digita ambas.
- `/run-plan` §3.3 (sanity check de docs): pede "consistente ou listagem". "Consistente" é discreta + frequente; listagem é Other-natural. Hoje operador digita ambas.
- `/debug` §1 (precisar sintoma): 5 perguntas em prosa, 3 são enum-áveis (`Onde`: dev/CI/staging/prod; `Reprod`: sempre/às vezes/uma vez; `Mudou`: sim/não/não sei). Hoje operador responde 5 prompts sequenciais em texto livre.
- `/release` §1b (bump ambíguo): pede "qual bump" em prosa. Resposta é sempre `patch`/`minor`/`major` (discreto, 3 opções).
- `/gen-tests-python` §6 (fixture em conftest): bifurcação binária (no teste vs em conftest) tratada como prosa.

Custo cumulativo: cada execução de `/run-plan` força 2 prompts em prosa (validação + sanity); cada `/debug` força 5 prompts; cada `/release` ambíguo força 1. Em sessão típica, isso vira fricção real — operador digita "validei", "consistente", "patch" repetidamente quando 1 tecla resolveria.

## Decisão

**Preferir `AskUserQuestion` (single ou multiSelect) sempre que houver ≥1 resposta comum discreta, mesmo se outras respostas comuns sejam livres.** O `Other` automático cobre as livres com 1 toque a mais; o caminho discreto economiza digitação na maioria dos runs.

Critério revisto:

- **Bifurcação discreta presente** (≥1 resposta comum é nome/escolha pré-definível) → enum, com `Other` cobrindo as livres. Marcar `(Recommended)` quando há alternativa dominante.
- **Todas as respostas comuns são livres** (descrição de bug, justificativa de escopo, exemplo concreto de dado real) → prosa desde o início. Critério "todas-Other → prosa" substitui o "maioria-Other → prosa" anterior.
- **Perguntas relacionadas no mesmo passo, ≥2 enum-áveis** → agrupar numa única chamada `AskUserQuestion` (até 4 questions) em vez de sequenciar prompts. Fragmentação tira foco; um único enum com várias chips é uma interação só.
- **Perguntas óbvias ou cerimoniais** ("posso prosseguir?" sobre ação que o roteiro já mandou seguir) → não emergem. Princípio "Não perguntar por valor único derivado" (philosophy.md) continua valendo; ADR-002 já aplicou a `/run-plan` pré-loop.

Materialização: edit em `philosophy.md` (clarificar critério "todas" vs "maioria"), edit em `CLAUDE.md` "AskUserQuestion mechanics" (regra operacional + unificação), 5 conversões prosa→enum em SKILLs (`/run-plan` §3.2/§3.3/§3.7, `/debug` §1, `/release` §1b, `/gen-tests-python` §6) e reforço editorial em `/triage` §2 + `/debug` §1 sobre unificação. Plano detalhado em `docs/plans/forma-perguntas-enum-first.md`.

## Consequências

### Benefícios

- **Caminho-curto preservado.** Resposta dominante (validei, consistente, patch) custa 1 tecla (Enter ou seta + Enter), não digitação de palavra.
- **Unificação de prompts relacionados.** `/debug` §1 cai de 5 prompts em prosa para 1 chamada com 4 questions. Foco do operador preservado.
- **Doutrina alinhada com prática.** Skill author futuro lê critério explícito; aplica enum-first sem precisar adivinhar limiar.
- **Continuidade com ADR-002.** Onde a pergunta deve existir, escolher a forma mais leve completa o trabalho de eliminar fricção desnecessária na entrada.

### Trade-offs

- **Custo do enum quando Other é a resposta.** Operador navega o enum (1-2 teclas) antes de digitar Other. Para a minoria dos runs cuja resposta é livre, isso é 1-2 teclas a mais que prosa pura. Aceito porque a maioria dos runs cai no caminho discreto, e o ganho lá supera o custo na minoria.
- **Mais chamadas `AskUserQuestion` no código dos SKILLs.** Aumenta verbosidade na prosa do SKILL. Mitigação: padronização permite que skill author copie estrutura entre invocações sem reinventar.
- **Risco de over-enumar.** Skill author empolgado pode forçar enum em pergunta que é genuinamente livre (ex.: justificativa de escopo). Mitigação: critério "todas-Other → prosa" é explícito; reviewer dos SKILLs pega a violação.

### Limitações

- **Comportamento meu (modelo) ad-hoc fora do roteiro.** SKILLs editados aplicam a regra; mas perguntas que eu invento entre passos (não declaradas no SKILL) seguem dependendo da minha calibragem. Mitigação: memória de feedback (`feedback_question_form_preference.md`) captura a preferência para sessões futuras; CLAUDE.md mechanics serve de referência durante invocação de skills.
- **Input genuinamente sem bifurcação.** ADR não cobre nem promete cobrir casos como título de ADR (`/new-adr`), alvo de teste (`/gen-tests-python`), descrição de bug — esses seguem em prosa. Não são exceção do critério; estão fora dele por construção (sem opções discretas).

## Alternativas consideradas

- **Manter critério "maioria-Other → prosa" e só editar SKILLs:** descartado. Sem refinar o critério, drift volta — skill author futuro relê philosophy.md e replica a interpretação que gerou o problema. Memória de feedback é minha (não dele); ADR é o ponto único persistente.
- **Eliminar `Other` e forçar enum estrito:** descartado. Operador precisa de escape para casos não-previstos; remover Other inverte o ganho (operador trava em pergunta sem opção que cabe).
- **Hook que detecta prosa-com-bifurcação nos SKILLs e bloqueia:** descartado por YAGNI. Reviewer dos SKILLs já cobre via leitura humana; hook adicional aumenta superfície sem ganho proporcional.

## Gatilhos de revisão

- Operador relata fricção do tipo "estou navegando enum só pra digitar Other" com frequência → reabrir para considerar se o enum estava mal calibrado (opções erradas) ou se prosa era o modo certo desde o início para aquele caso.
- Skill author relata que regra é confusa de aplicar (várias dúvidas sobre "isso é discreto?") → considerar exemplos canônicos no CLAUDE.md ou heurística mais operacional.
- Surge nova mecânica de pergunta no toolkit (ex.: input estruturado tipo formulário, voice input) que mude o cálculo de custo enum vs prosa → reavaliar.
