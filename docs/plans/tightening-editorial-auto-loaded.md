# Plano — Tightening editorial do payload auto-loaded (Onda 2)

## Contexto

Bundle pré-curado pelas auditorias `2026-05-12-architecture-logic.md` (proposta A_arch) e `2026-05-12-prose-tokens.md` (propostas A_prose e C_prose), sequenciado como **Onda 2** em `docs/audits/runs/2026-05-12-execution-roadmap.md`. As 3 propostas tocam payload **auto-loaded por turn** (CLAUDE.md + frontmatters de skills/agents lidos pelo roteador da harness antes de qualquer invocação) — atacar junto rende a redução em todo turn da sessão, evitando re-revisão editorial das mesmas linhas em ondas separadas.

**ADRs candidatos:** [ADR-023](../decisions/ADR-023-criterio-mecanico-disable-model-invocation-skills.md) (criado por este `/triage` para fundamentar A_arch — Bloco 1 aplica o critério mecânico do ADR), [ADR-017](../decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md) (mecânica do payload auto-loaded é o racional do bundle + § Editorial inheritance como precedente do tratamento da uniformização sem enforcement), [ADR-009](../decisions/ADR-009-revisor-design-pre-fato.md) e [ADR-011](../decisions/ADR-011-wiring-design-reviewer-automatico.md) (escopo/wiring do `design-reviewer` cuja `description` é compactada em C_prose).

**Linha do backlog:** plugin: executar propostas das auditorias 2026-05-12 — roadmap em `docs/audits/runs/2026-05-12-execution-roadmap.md`. 4 ondas independentes (ADRs estruturais, bundle editorial auto-loaded, bundles cross-skill, trim cirúrgico). Sessões podem pegar ondas separadas; item diferido (H_arch) só sai com evidência empírica.

## Resumo da mudança

Três frentes editoriais cumulativas no payload auto-loaded, todas doc-only:

1. **A_arch — uniformizar `disable-model-invocation` aplicando o critério mecânico do ADR-023.** O ADR-023 (criado neste mesmo `/triage` após `design-reviewer` no plano original ter rejeitado o caminho "doutrinário sem ADR" por findings altos) formaliza o critério cumulativo (blast radius local + gate de fronteira + sem autoinvocação cross-turn) + tabela retroativa às 9 skills. Bloco 1 aplica o veredito do ADR: declara `disable-model-invocation: false` nas 5 skills omissas (`/triage`, `/debug`, `/gen-tests`, `/next`, `/init-config`) + adiciona referência curta ao ADR-023 em CLAUDE.md (paralelo a como ADR-013/ADR-017 são referenciados, sem duplicar conteúdo do ADR).

2. **A_prose — compactar cicatrizes em CLAUDE.md** (auditoria prose-tokens § 3.A): (a) linha 23 "From v1.11.0 onward..." → estado atual sem prefácio histórico; (b) linhas 25-28 parágrafo "Release cadence" → 1 sentença; (c) linha 84 "Critério editorial" (4 sentenças) → 2; (d) linha 86 "From v1.11.0 onward, version bumps in **this** repo..." (4ª ocorrência do mesmo pattern; auditoria flagrou pattern, não enumerou exaustivamente as 4 ocorrências — bundle executa o pattern completo).

3. **C_prose — encurtar 4 frontmatter `description` para gatilho puro** (auditoria prose-tokens § 3.C): `/gen-tests` (38→~22 palavras, remover idioms internos mantendo anchors `Python`/`Java` para discoverability lexical do roteador — finding 5 do `design-reviewer`), `/init-config` (41→~22, remover passo-a-passo da mecânica), `design-reviewer` (71→~30, remover lista de findings/dispatch — já no body), `security-reviewer` (51→~30, remover lista exemplificativa de sistemas aplicáveis).

**Redução estimada** (auditoria prose-tokens § 4, com ajuste pelo finding 5): A_prose ~70 palavras + C_prose ~90 palavras = ~160 palavras / ~210 tokens auto-loaded por turn. Bloco 1 adiciona ~5 linhas (frontmatter ×5 + 1 bullet em CLAUDE.md); net agregado **negativo** mas menor que ~220 tokens originalmente estimados — net real ~150 tokens auto-loaded por turn. Honesto sobre o trade-off (finding 3 do `design-reviewer`).

## Arquivos a alterar

### Bloco 1 — Aplicar critério ADR-023 + referência em CLAUDE.md {reviewer: doc}

- `CLAUDE.md`: adicionar **uma única linha** na lista de bullets de "Editing conventions" (paralelo aos bullets de ADR-010, ADR-011, ADR-013 já presentes ali). Wording-alvo: *"`disable-model-invocation` em SKILL.md: critério mecânico cumulativo em [ADR-023](docs/decisions/ADR-023-criterio-mecanico-disable-model-invocation-skills.md) — blast radius local + pushes/PRs gateados por enum + sem autoinvocação cross-turn → `false`; tabela retroativa às 9 skills atuais no próprio ADR. Skill nova com `true` justifica explicitamente."* (~1 linha; net +1 linha em CLAUDE.md, vs ~5-8 do plano original.)
- `skills/triage/SKILL.md`: adicionar `disable-model-invocation: false` no frontmatter (após `description`, antes de `roles`).
- `skills/debug/SKILL.md`: idem.
- `skills/gen-tests/SKILL.md`: idem.
- `skills/next/SKILL.md`: idem.
- `skills/init-config/SKILL.md`: idem (frontmatter sem `roles:` por design — `disable-model-invocation` entra entre `description` e o fechamento `---`).

### Bloco 2 — Compactar 4 cicatrizes em CLAUDE.md {reviewer: doc}

- `CLAUDE.md` linha 23 (atual): remover prefácio "From v1.11.0 onward". Wording-alvo: *"Version bumps go through `/release` (dogfood). The skill resolves `version_files` from this repo's config to update **both** manifests, composes the `CHANGELOG.md` entry from the CC log since the last tag, commits and tags locally. Push remains manual."* (−8 palavras).
- `CLAUDE.md` linhas 25-28 (atual): comprimir parágrafo "Release cadence" em 1 sentença. Wording-alvo: *"Release cadence: trigger `/release` when there's a coherent set to publish (feature complete, urgent fix, or deliberate cadence drop); per-PR bumps generate noisy changelog entries and version churn."* (−25 palavras).
- `CLAUDE.md` linha 84 (atual): comprimir "Critério editorial" (4 sentenças) em 2. Wording-alvo: *"**Critério editorial:** lista apenas guardas que documentam anti-padrão não-óbvio. Itens vindos de incidentes ou de vieses sutis (modelo tende a autoinvocar, gatilho condicional facilmente esquecido, exceção localizada) são não-óbvios e devem permanecer."* (−35 palavras).
- `CLAUDE.md` linha 86 (atual): cicatriz duplicada da linha 23 reescrita. **Remover** completamente — informação já está na linha 23 nova; bullet não agrega.

### Bloco 3 — Encurtar 4 frontmatter `description` para gatilho puro {reviewer: doc}

- `skills/gen-tests/SKILL.md` linha 3: remover idioms internos mantendo discoverability lexical. Wording-alvo (~22 palavras): *"Gera arquivo de teste para módulo, função ou descrição livre, com idioms da stack do projeto consumidor (Python e Java suportadas). Use quando o operador pedir testes."* (anchors `Python`/`Java` preservados per finding 5 do `design-reviewer`; idioms internos `pytest`/`respx`/`tmp_path`/`JUnit 5`/`Mockito`/`Maven` removidos).
- `skills/init-config/SKILL.md` linha 3: remover passo-a-passo da mecânica. Wording-alvo (~22 palavras): *"Wizard interativo para configurar o bloco `<!-- pragmatic-toolkit:config -->` no `CLAUDE.md`. Use quando o operador quer configurar o plugin de uma vez em projeto novo ou reconfigurar bloco existente."*
- `agents/design-reviewer.md` linha 3: remover lista enumerada de findings + detalhe de dispatch. Wording-alvo (~30 palavras): *"Revisor de decisões arquiteturais e de design em documento pré-fato (plano ou ADR draft). Acionado automaticamente em `/triage` que produz plano e em `/new-adr` (standalone ou delegada) per ADR-011; manualmente via `@design-reviewer`. Stack-agnóstico."*
- `agents/security-reviewer.md` linha 3: remover lista exemplificativa de sistemas aplicáveis. Wording-alvo (~30 palavras): *"Revisor de segurança focado em segredos, validação de entrada em fronteiras, I/O externo, dados sensíveis, privilégios e invariantes documentadas em ADRs. Stack-agnóstico. Acionar antes de PR quando a mudança envolver segredos, handlers de fronteira ou persistência de dados sensíveis."*

## Verificação end-to-end

Doc-only; o gate é CI lint + inspeção textual. Comandos concretos:

- `python3 -c "import json; [json.load(open(p)) for p in ['.claude-plugin/plugin.json', '.claude-plugin/marketplace.json']]"` — manifests JSON válidos (cobertura mínima ADR-013).
- `grep -c "^disable-model-invocation: false$" skills/*/SKILL.md` retorna **`9`** (todas as 9 skills declaram após Bloco 1: as 4 que já declaravam — `/release`, `/new-adr`, `/run-plan`, `/archive-plans` — mais as 5 omissas que ganham a declaração).
- `grep -c "From v1.11.0 onward" CLAUDE.md` retorna `0` (pattern erradicado nas 2 ocorrências após Bloco 2).
- `grep -q "ADR-023" CLAUDE.md` — referência ao ADR adicionada (gating do Bloco 1 vs Bloco 2 — bullets adjacentes em "Editing conventions"; sem conflito de edit).
- Contagem de palavras dos 4 `description` tocados em Bloco 3 abaixo dos alvos: `/gen-tests` ≤24 (margem +2 sobre alvo nominal 22), `/init-config` ≤24, `design-reviewer` ≤32, `security-reviewer` ≤32.
- `CLAUDE.md` permanece dentro do cap nominal de 200 linhas (`wc -l CLAUDE.md` esperado entre 167 e 173 após bundle: Bloco 1 +1 linha, Bloco 2 −5 a −7 líquido, Bloco 3 toca outros arquivos).
- Pipeline da CI (`.github/workflows/validate.yml`) verde no PR.
- Smoke editorial: reler `CLAUDE.md` end-to-end pós-bundle; narrativa coerente sem as cicatrizes; novo bullet sobre `disable-model-invocation` não fragmenta o fluxo de "Editing conventions".

## Notas operacionais

- **Ordem dos blocos:** 1 → 2 → 3. Bloco 1 adiciona bullet novo em "Editing conventions" + frontmatter em 5 SKILL.md; Bloco 2 compacta linhas pré-existentes na seção "What this repo is" (linhas 23, 25-28, 86) e em "Editing conventions" (linha 84). Bullet do Bloco 1 e bullet da linha 84 reescrita são distintos — sem overlap textual. Bloco 3 toca arquivos disjuntos.
- **Reviewer dispatch:** todos `{reviewer: doc}` — paths `.md` apenas, sem código de produção. `design-reviewer` **não** é redisparado por `/run-plan` (ADR-011 — ele opera pré-fato em plano/ADR; já disparou neste `/triage`, tanto no plano original quanto no ADR-023). Reviewer `doc` valida wording final + ausência de drift cross-arquivo.
- **Roadmap update:** ao fechar este plano via `/run-plan`, atualizar `docs/audits/runs/2026-05-12-execution-roadmap.md` marcando A_arch, A_prose e C_prose como `[x]` com link a PR/commit + data curta. Convenção das ondas anteriores (commits `aca180b`, `8e65d3f`): bloco extra "chore(roadmap): mark Onda 2 shipped" ao fim do loop, ou atualização inline no commit unificado do passo final — mecânica a decidir no `/run-plan`.
- **BACKLOG:** linha genérica em `## Próximos` (linha 5) cobre as 4 ondas como um todo; **não** transita para `## Concluídos` ao fim desta Onda 2 — só quando a última onda ativada fechar. O `**Linha do backlog:**` deste plano é matching de referência, não trigger de transição.
- **4ª cicatriz (linha 86 do CLAUDE.md atual):** pattern observado pela auditoria abrange 4 ocorrências, não 3 — auditoria citou 3 por enumeração não-exaustiva; bundle executa as 4 instâncias do mesmo pattern (fidelidade ao pattern, não à enumeração literal — finding 4 do `design-reviewer`).
- **Bloco 1 sem cláusula de wording draft:** wording do bullet em CLAUDE.md é alvo definitivo, não draft. ADR-023 carrega o conteúdo doutrinário; bullet em CLAUDE.md é só ponteiro + síntese de 1 linha. Refino editorial no PR continua aberto, mas não há decisão estrutural pendente.
- **Bundle válido per roadmap § "Pontos de atenção cross-onda":** mesmo eixo auto-loaded. Recusar tentação de adicionar B_prose (consolidar idioma do relatório, Onda 3b) ao bundle — cross-purpose; entra na 3b sob `/triage` próprio.
- **Re-rodar prose-tokens só após Onda 3a (G_arch).** Esta Onda 2 reduz auto-loaded em ~150 tokens (net honesto pós-Bloco-1) mas não move a aritmética estrutural; refinar alvos só faz sentido depois que G_arch tirar ~200 palavras de `/triage §0`.
- **Release cadence:** bundle muda contrato de frontmatter em 5 skills (auto-invocação default → `false` explícito). Decisão `chore` vs `feat` no próximo `/release` depende de critério — `chore` é defensável (mudança editorial em metadados de skill, comportamento observável idêntico ao default da harness atual); `feat` seria over-classificado. Não bloqueia execução; economiza decisão sob pressão no `/release`.
- **Universo de 9 skills:** `/archive-plans` shippou na Onda 1 (pós-recorte da auditoria); já tem `disable-model-invocation: false` declarado. ADR-023 cobre as 9 explicitamente na tabela retroativa; este plano só aplica nas 5 omissas restantes.
