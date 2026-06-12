# Plano — Aplicar regra enum-first em SKILLs e doutrina

## Contexto

Materializa [ADR-006](../decisions/ADR-006-enum-em-bifurcacao-discreta.md) (Aceito): preferir `AskUserQuestion` (single ou multiSelect) sempre que houver ≥1 resposta comum discreta, mesmo se outras respostas comuns sejam livres — `Other` cobre as livres. Critério "todas-Other → prosa" substitui "maioria-Other → prosa" anterior.

Auditoria pré-ADR identificou 7 zonas concretas em SKILLs onde prosa-com-bifurcação podia virar enum. Plano cobre as 7 conversões + edits de doutrina (philosophy.md + CLAUDE.md) que ADR-006 mandata.

ADR-002 já eliminou 4 gates de cutucada em `/run-plan` pré-loop; este plano é a sequência natural — onde a pergunta **deve** existir, escolher a forma mais leve.

**Linha do backlog:** plugin: aplicar regra enum-first em SKILLs — converter prosa-com-bifurcação em AskUserQuestion (single/multi + Other auto + Recommended), unificar perguntas relacionadas, eliminar óbvias

## Resumo da mudança

Refinamento de doutrina (philosophy.md + CLAUDE.md mechanics) + 5 conversões mecânicas em SKILLs + 1 instrução explícita de unificação em `/triage` e `/debug`.

**Decisões-chave:**
- **ADR-006 já aceito.** Plano apenas materializa; doutrina escrita já reflete a decisão.
- **Reviewer por bloco**: `doc` para philosophy.md/CLAUDE.md (drift entre doutrina e SKILLs); `code` para SKILLs (YAGNI/clareza nos novos prompts).
- **Sem `## Verificação manual`**: doc-only, sem comportamento perceptível ao usuário final do toolkit consumidor — verificação é leitura textual dos prompts editados.

**Fora de escopo:**
- Não converter perguntas onde input é genuinamente sem bifurcação discreta: `/new-adr` argumento (título), `/gen-tests-python` argumento (alvo), `/triage` §2 gaps de explicação livre (forma do dado real, justificativa de escopo).
- Não eliminar prosa em `/release` §4 opção `Editar` — ela já é o caminho `Other` do enum `Aplicar/Editar/Cancelar`.
- Não tocar comportamento meu (modelo) ad-hoc — coberto por memória de feedback (`feedback_question_form_preference.md`).

## Arquivos a alterar

### Bloco 1 — refinar mecânica em CLAUDE.md {reviewer: doc}

- `CLAUDE.md` seção "AskUserQuestion mechanics": adicionar bullet operacional logo após o bullet de `Other` automático:
  - **Texto a inserir**: "Quando há ≥1 resposta comum **discreta** identificável, prefira enum mesmo que outras respostas comuns sejam livres — o `Other` automático cobre as livres com 1 toque a menos para o caminho discreto. Critério 'maioria-Other → prosa' só se aplica quando **todas** as respostas comuns são livres (ex.: descrição de bug, justificativa de escopo)."
- Mesmo arquivo, adicionar bullet sobre unificação após o bullet `Multiple related questions`:
  - **Texto a inserir**: "Quando ≥2 perguntas relacionadas no mesmo passo são enum-áveis, **agrupar numa única chamada** em vez de sequenciar — fragmentação tira foco do operador."

### Bloco 2 — clarificar princípio em philosophy.md {reviewer: doc}

- `docs/philosophy.md` seção "Convenção de pergunta ao operador": substituir a frase final do parágrafo de abertura — *"Quando a maioria das respostas reais cairia em 'Other' do enum, o modo certo era prosa desde o início."* — por:
  - **Texto novo**: "Quando **todas** as respostas comuns cairiam em 'Other' do enum (descrição livre, justificativa, exemplo), o modo certo era prosa desde o início. Mas se ≥1 resposta comum é discreta, prefira enum mesmo assim — `Other` cobre as livres."

### Bloco 3 — `/run-plan` 3 conversões {reviewer: code}

- `skills/run-plan/SKILL.md` §3.2 — Validação manual:
  - Substituir *"aguardar confirmação explícita ('ok, valido')"* por instrução de despachar `AskUserQuestion` (header `Validação`) com `Validei (Recommended)` / `Falhou — descrever`. Other-auto recebe descrição de falha. Sem confirmação positiva (Validei OU descrição não-vazia em Other), não fechar.
- Mesmo arquivo §3.3 — Sanity check de docs:
  - Substituir *"Cutucar caso contrário em **prosa livre** (não enum — a maioria das respostas reais é uma listagem de arquivos a atualizar, território de 'Other')"* por instrução de despachar `AskUserQuestion` (header `Docs`) com `Consistente (Recommended)` / `Listar arquivos a atualizar`. Other-auto recebe a listagem. `Listar arquivos` selecionado direto pode ser equivalente a Other (operador descreve).
  - Justificativa do refinamento: aplica nova regra (≥1 discreta → enum, mesmo com Other comum).
- Mesmo arquivo §3.7 — Sugestão de publicação:
  - Absorver a frase informativa "modo local: ... Renomear antes? Sugestão: git branch -m ..." como **opção dentro do enum `Publicar`**, não como pré-pergunta. Novo enum:
    - `Push (Recommended se não-local)` / `Push + abrir PR/MR (Recommended se não-local)` / `Renomear branch antes (Recommended se modo local)` / `Nenhum`
    - Em modo local, ajustar Recommended para `Renomear branch antes`.
    - Description da opção `Renomear` carrega contexto: "modo local — branch name é metadata pública; sugestão `git branch -m <novo-nome>` antes de pushar".

### Bloco 4 — `/debug` §1 unificação prosa→enum {reviewer: code}

- `skills/debug/SKILL.md` §1 — Precisar o sintoma:
  - Substituir lista de 5 perguntas em prosa por instrução de despachar **uma única chamada** `AskUserQuestion` com 4 questions:
    - Q1 `Onde` (enum): `dev local` / `CI` / `staging` / `prod`
    - Q2 `Reprod` (enum): `Sempre (Recommended)` / `Às vezes` / `Uma vez só`
    - Q3 `Mudou` (enum): `Sim` / `Não` / `Não sei`
    - Q4 `Ação` (Other-only via enum binário com placeholder, OU prosa em chamada separada — preferir Other-only para manter unificação): comando/teste/request/fluxo manual que dispara
  - Output esperado vs observado fica em prosa livre **separada** após a chamada (genuinamente sem bifurcação discreta), só se as 4 anteriores não bastarem.
  - Adicionar nota: "Quando ≥2 perguntas no passo são enum-áveis, agrupar em chamada única (regra geral em CLAUDE.md → AskUserQuestion mechanics)."

### Bloco 5 — `/release` §1b conversão {reviewer: code}

- `skills/release/SKILL.md` §1 sub-caminho 1b (Histórico ambíguo):
  - Substituir *"Prosa livre — mostrar resumo dos commits agrupados por prefixo, perguntar qual bump"* por instrução de despachar `AskUserQuestion` (header `Release`) com `patch` / `minor` / `major`, **sem Recommended** (ambíguo é a premissa do sub-caminho — recomendar nada é mais honesto). `description` de cada opção carrega contagem de commits relevantes do tipo. Other-auto cobre versão explícita.
  - Resumo dos commits agrupados por prefixo é mostrado **antes** da chamada (prosa informativa), não como pergunta.

### Bloco 6 — `/gen-tests-python` §6 conversão {reviewer: code}

- `skills/gen-tests-python/SKILL.md` "Passos" item 6:
  - Substituir *"Não criar fixtures em `conftest.py` sem perguntar ao operador"* por instrução de despachar `AskUserQuestion` (header `Fixture`) com `No próprio arquivo de teste (Recommended)` / `Em conftest.py`. Description carrega trade-off (isolamento vs. compartilhamento entre testes).
  - Disparar **apenas** quando a skill identifica candidato a fixture compartilhada; cenário trivial (fixture única no teste) segue silente.

### Bloco 7 — `/triage` §2 instrução explícita de unificação {reviewer: code}

- `skills/triage/SKILL.md` §2 — Esclarecer gaps com o usuário:
  - Reforçar instrução existente *"Até 4 perguntas relacionadas numa única chamada"* tornando explícito o critério: "Quando ≥2 dos gaps identificados são enum-áveis (escolha discreta), **agrupar numa única chamada** `AskUserQuestion` em vez de sequenciar prompts. Gaps de explicação livre (forma do dado real, justificativa de escopo) seguem em prosa **separada** quando o conteúdo não cabe em opção pré-definida."
  - Reforço editorial mínimo, redação atual já permite — o que muda é o status (permitido → preferido).

## Verificação end-to-end

Sem suite de testes (plugin sem `test_command`); verificação é inspeção textual dos arquivos editados.

Por bloco:

1. **CLAUDE.md**: `grep -A 3 "Quando há ≥1 resposta comum" CLAUDE.md` retorna o novo bullet; `grep -A 3 "Quando ≥2 perguntas relacionadas" CLAUDE.md` retorna o bullet de unificação.
2. **philosophy.md**: `grep -A 2 "Quando todas as respostas comuns" docs/philosophy.md` retorna a frase refinada; frase antiga ("Quando a maioria das respostas reais cairia em 'Other'") **não** mais presente.
3. **`/run-plan`**: `grep -c "AskUserQuestion" skills/run-plan/SKILL.md` aumenta em ≥3 (3.2, 3.3, e referência mantida em 3.7); `grep "ok, valido"` retorna vazio; `grep "prosa livre.*Other" skills/run-plan/SKILL.md` retorna vazio (sanity check 3.3 não mais documentado como prosa); `grep "Renomear antes?"` retorna vazio (absorvido no enum).
4. **`/debug`**: `grep "Perguntas de precisão são prosa livre"` retorna vazio; texto do passo 1 menciona despacho via `AskUserQuestion` com até 4 questions.
5. **`/release`**: `grep "Prosa livre" skills/release/SKILL.md` retorna vazio (1b agora é enum); enum `Release` em 1b citado.
6. **`/gen-tests-python`**: `grep "sem perguntar" skills/gen-tests-python/SKILL.md` retorna vazio; enum `Fixture` citado.
7. **`/triage`**: §2 cita explicitamente "agrupar numa única chamada" como preferência (não só permissão).

Cross-arquivo:
- `grep -rn "AskUserQuestion" skills/ docs/philosophy.md CLAUDE.md` mostra coerência entre doutrina e aplicação.
- Nenhum SKILL editado introduz pergunta sem pelo menos 2 opções discretas (a não ser via `Other`-only quando input é genuinamente livre, caso justificado em prosa).

## Notas operacionais

- **Ordem dos blocos importa parcialmente.** Blocos 1-2 (doutrina) **antes** de 3-7 (SKILLs) para que o reviewer dos SKILLs valide alinhamento com a doutrina já editada. Doc-reviewer dos blocos 1-2 não tem essa dependência.
- **Reviewer overlap.** Blocos 1-2 (`doc`) verificam drift entre o texto editado e os SKILLs alvos; blocos 3-7 (`code`) verificam clareza/YAGNI dos novos prompts. Eixos distintos, separação justificada.
- **Capturas previstas**: nenhuma surface não-coberta. Se reviewer de bloco 3-7 levantar inconsistência com a nova doutrina (ex.: SKILL editado contradiz refinamento de philosophy.md), capturar como Validação no plano corrente.
