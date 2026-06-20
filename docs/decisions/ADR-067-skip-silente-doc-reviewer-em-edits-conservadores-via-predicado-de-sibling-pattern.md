# ADR-067: Skip silente doc-reviewer em edits conservadores via predicado de sibling pattern

**Data:** 2026-06-20
**Status:** Proposto

**Próxima revisão:** 2026-12-20
**Cadência:** trimestral
**Critério de erosão auditável:** ≥2 invocações cross-session subsequentes em que `doc-reviewer` skipa via predicado mas reporta drift real pós-fato (false-positive do skip), OR ≥2 invocações cross-session subsequentes em que `doc-reviewer` dispara apesar do diff satisfazer o predicado (false-negative do skip — predicado conservador demais), OR auditoria post-mortem semestral revelar que ≥80% das invocações onde o predicado bateu (skip silente disparou) ocorreram em paths/contextos do mesmo cluster temático original (bullets siblings em CLAUDE.md/README.md/install.md de reformas editoriais do plugin) — sinal de over-fitting do predicado ao cluster cross-week original, não generalidade.

## Origem

- **Decisão base:** [ADR-062](ADR-062-criar-subagent-prompt-reviewer.md) — sucessor parcial § Pattern de dispatch. ADR-062 codificou hierarquia path-based para dispatch de reviewer em `/run-plan §2 item 3`; ADR-067 estende com nova dimensão ortogonal (predicado de sibling pattern sobre diff structure), preservando hierarquia path-based existente intacta.
- **Investigação:** Cluster cross-week 2026-06-15 → 2026-06-20 de 3 instâncias empíricas cross-session documentadas em NOTES § 2026-06-16T00:07Z § (1) (3 sub-instâncias intra-sessão `next-2026-06-15`), NOTES § 2026-06-19T21:23:08Z § (1) (2 sub-instâncias intra-sessão `next-2026-06-19`), NOTES § 2026-06-20T10:51:18Z § (1) (1 instância intra-sessão `next-2026-06-20`). 6 invocações totais de `doc-reviewer`, todas close-clean ("Nenhum drift identificado neste diff.") — diff sempre satisfazendo o predicado mecânico (purely additive + bullet em mesmo indent level que ≥2 siblings imediatamente adjacentes de formato similar).

## Contexto

`/run-plan §2 item 3` codifica hierarquia mais-específico-vence para dispatch de reviewer per bloco (per ADR-062 § Pattern de dispatch):

- Sem anotação → default `code-reviewer`.
- Exceção doc-only narrow (paths em `agents/*.md` ∪ `skills/**/SKILL.md` ∪ `docs/plans/*.md`) → `prompt-reviewer`.
- Exceção doc-only ampla (extensão `.md`/`.rst`/`.txt` fora do narrow) → `doc-reviewer`.
- Exceção bloco misto narrow+ampla → `doc-reviewer`.

Atualmente toda invocação em doc-only ampla dispara `doc-reviewer`, mesmo quando o diff é cirúrgico editorial sobre padrão pré-existente. Pattern empírico observado no cluster cross-week 2026-06-15 → 2026-06-20: 6 invocações em 4 sessões consecutivas, todas close-clean. Diff sempre: insere bullet em mesmo indent level que ≥2 siblings imediatamente adjacentes de formato similar (entries de tabela paralelas, bullets de § Editing conventions paralelos a ADR-NNN siblings, sub-passos de install.md step paralelos).

Reviewer convergente sem findings em 6/6 instâncias num pattern recorrente é cerimônia per ADR-002 § Decisão (anti-gate-cerimônia). Cluster cross-week atinge piso mínimo de [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § Ockham operacionalizado critério 4 (N=3 cross-session em 5 dias adjacentes), mas com fragilidade epistêmica reconhecida análoga aos precedentes ADR-057/-061/-062/-063/-064/-065 — todas as 6 instâncias são bullet/entry adicionada a tabela ou seção paralela durante a mesma reforma editorial (dispatch refactor §3.3/§3.4 + ADR-065 + migrate-to-forge). Cluster reflete homogeneidade de contexto, não necessariamente generalidade do pattern em contextos diversos. Codificar skip silente para o predicado preserva reviewer recurso para diffs com mudança estrutural genuína; § Override do critério N=3 abaixo + critério de erosão auditável codificam o monitoring contra over-fitting.

## Decisão

Adicionar **nova exceção** na hierarquia mais-específico-vence de `/run-plan §2 item 3`, posicionada **APÓS** as exceções existentes de ADR-062 (narrow → `prompt-reviewer`; ampla → `doc-reviewer`; misto → `doc-reviewer`) e **só ativa quando a hierarquia resolveu para `doc-reviewer`**:

> **Exceção skip silente doc-reviewer em edits conservadores**: SE a hierarquia ADR-062 resolveu o bloco para `doc-reviewer` (ampla OR misto narrow+ampla) AND o diff satisfaz o predicado heurístico-semântico — **predominantemente additive** (sem deletes ≥2 linhas de conteúdo prose; whitespace/typo correction permitido) AND **bullet/linha nova inserida em seção ou lista onde ≥2 siblings imediatos seguem mesmo gabarito sintático** (mesmo prefixo bold, mesmo nível de indent, mesma estrutura grosso modo) — → skip silente (sem invocação de reviewer). Caso o bloco resolva para `prompt-reviewer` (path narrow puro) OR `code-reviewer` (default) OR o predicado não bata, segue a hierarquia normal. LLM `/run-plan` aplica o predicado em runtime; default-conservador resolve a favor do dispatch normal.

Razões objetivas:

- **ADR-043 § Ockham operacionalizado critério 4 atingido no piso** — N=3 cross-session no cluster 06-15/06-19/06-20 com 6 instâncias empíricas. Fragilidade epistêmica reconhecida (§ Override do critério N=3 abaixo); critério satisfeito por contagem nua mas em contexto homogêneo. Codificar agora + critério de erosão auditável + § Override constitui o trade-off; defer pra cluster em contexto diverso fica em aberto via gatilho de revisão.
- **ADR-002 § Decisão anti-gate-cerimônia materializado** — reviewer convergente close-clean em diff satisfazer predicado recorrentemente é cerimônia. Skip preserva reviewer recurso para diff com mudança estrutural real.
- **ADR-062 § Pattern de dispatch preserved** — hierarquia path-based intacta; nova exceção é dimensão ortogonal (diff structure) que se compõe naturalmente sem engolir `prompt-reviewer` (posicionamento APÓS + restrição a doc-reviewer resolved).
- **Predicado conservador** — duas conjunções (predominantemente additive AND ≥2 siblings) avaliadas pelo LLM em runtime com qualifiers semânticos ("significativo", "imediatos", "mesmo gabarito sintático"). Default-conservador a favor do dispatch normal quando predicado não bate ou qualifiers ambíguos: false-negative (skip não disparou) preferível a false-positive (drift real escapou).

Implementação:

- Refinement prose-only de `skills/run-plan/SKILL.md §2 item 3` adicionando a cláusula como bullet posicionado APÓS as exceções narrow/ampla/misto de ADR-062 (não antes — preserva resolução path-based primeiro; skip aplica como filtro de pós-processamento sobre resolução doc-reviewer).
- Sub-tool determinístico **rejeitado** porque o predicado é heurístico-semântico por desenho (qualifiers "significativo", "imediatamente adjacentes", "mesmo gabarito sintático" requerem julgamento agentic do LLM em runtime). Sub-tool exigiria forma puramente mecânica (parse AST do diff + contagem regex de bullets siblings) — escolha prévia foi semantic-judgment by LLM (paralelismo com 4 heurísticas seed de `prompt-reviewer`, ADR-062 § Trade-offs). Trade-off da escolha: sub-tool seria refatorável/testável/auditável; forma semântica é flexível mas drifta caso-a-caso. Aceito o drift sob gatilho de revisão (§ Critério de erosão auditável).

**Dogfood meta-loop.** Edit em `skills/run-plan/SKILL.md §2 item 3` cai no path-set narrow (ADR-062 + ADR-063) → `prompt-reviewer` disparará no `/run-plan` per bloco OR no caminho-atômico de `/triage` step 5. Findings esperáveis sobre o predicado (qualifiers semânticos — F2/F5 do design-reviewer pré-fato deste ADR) deverão ser absorvidos antes do commit. Isso é dogfood intencional do toolkit — `prompt-reviewer` é gate canonical para o tipo de drift que este ADR introduz.

## Consequências

### Benefícios

- Reduz invocações redundantes de `doc-reviewer` (~6/N taxa observada cross-week). Pipeline `/run-plan` para edits conservadores cirúrgicos fica mais leve.
- Sinaliza confiança mecânica em pattern empírico — quando predicado bate, doc-reviewer recurso preservado para casos onde substância editorial requer análise.
- Preserva precedente de prose-only dispatch hierarchy (ADR-062), evitando over-engineering.

### Trade-offs

- Predicado é **semantic-judgment by LLM** (qualifiers "significativo", "imediatamente adjacentes", "mesmo gabarito sintático" não são puramente mecânicos), análogo às 4 heurísticas seed de `prompt-reviewer` (ADR-062 § Trade-offs). LLM `/run-plan` aplica per bloco em runtime; cada invocação resolve qualifiers via julgamento agentic. Risco de drift caso-a-caso aceito sob gatilho de revisão.
- LLM `/run-plan` adiciona micro-overhead semântico ao dispatch (parse mental do diff + indent counting + comparação de gabarito).
- Edge cases (insert em seção com mistura de sibling formats parcial) podem cair em false-negative (skip não dispara) — aceito como conservador.

### Limitações

- Predicado P2 ("edit replica template pré-existente sem mudança estrutural") da NOTES substância original NÃO incluído em v1 — défice de evidência empírica: cluster cross-week observou 5 de 6 instâncias como P1 (sibling pattern); apenas 1 caso edge (§3.4 BACKLOG mark + plan Status removal) fitting P2 isoladamente. Aceitamos dispatch normal para casos P2 até ≥3 instâncias P2-only emergirem.
- Scope restrito a `doc-reviewer` — não generaliza para `prompt-reviewer`/`code-reviewer` convergente. Empírico pattern observado especificamente para doc-reviewer; resolução para `prompt-reviewer` (path narrow puro) explicitamente NÃO ativa skip per § Decisão.
- Cluster cross-week é homogêneo em contexto (mesma reforma editorial; mesmo tipo de diff — bullets siblings em CLAUDE.md/README.md/install.md). Generalidade do pattern em contextos diversos é hipótese, não evidência. Critério de erosão auditável § (3ª cláusula) monitora over-fitting.

### Mitigações

- Critério de erosão auditável codifica fallback explícito.
- Cluster cross-week + 3 NOTES entries com pattern detalhado permite auditoria post-fact.

## Alternativas consideradas

### Sub-tool determinístico

Implementação como `skills/run-plan/sub-tools/dispatch.py` exigiria predicado puramente mecânico (parse AST do diff + contagem regex de bullets siblings em ranges de linhas adjacentes). **Rejeitada** porque a forma do predicado é decisão prévia: optamos por forma semântica resolvida pelo LLM em runtime (paralelismo com 4 heurísticas seed de `prompt-reviewer`, ADR-062 § Trade-offs), o que torna sub-tool inaplicável por desenho. Trade-off da escolha: sub-tool determinístico seria refatorável/testável/auditável; forma semântica é flexível mas drifta caso-a-caso. Aceitamos o drift sob gatilho de revisão (§ Critério de erosão auditável). Ortogonalmente: mesmo se o predicado fosse mecanicamente formalizável, pattern ADR-066 (`skills/<name>/sub-tools/<f>.py`) é para mecânica determinística múltipla (parse + batch + drain como em `/migrate-backlog-to-forge`); 1 boolean predicate de dispatch sozinho não justificaria sub-tool dedicado.

### Predicado P2 (edit replica template) incluído

Substância NOTES § 2026-06-16T00:07Z § (1) menciona dois predicados OR-combined (P1 sibling pattern + P2 template replication). **Rejeitada** P2 inclusão em v1 por défice de evidência empírica: cluster cross-week observou 5 de 6 instâncias como P1 (sibling pattern); apenas 1 instância edge case (§3.4 BACKLOG mark + plan Status removal) fitting P2 isoladamente. Aceitar dispatch normal para casos P2 até ≥3 instâncias P2-only emergirem fora do cluster P1.

### Scope generalizado para todos reviewers

Cláusula skip aplicada a qualquer reviewer (code/qa/security/prompt/doc) quando predicado bate. **Rejeitada** por défice de evidência: cluster cross-week observou pattern específico para doc-reviewer. Outros reviewers podem ter rubrics que justificam invocação mesmo em diff additive sibling. Restringir scope ao empírico preserva safety; estender quando outras reviewer categories acumularem evidência cross-session ≥2.

### Posicionamento ANTES das exceções ADR-062

Posicionar nova exceção antes da hierarquia path-based de ADR-062 (narrow → `prompt-reviewer`; ampla/misto → `doc-reviewer`), engolindo paths narrow puros quando diff bate predicado. **Rejeitada** porque contradiz § Limitações (scope restrito a doc-reviewer): paths em `agents/*.md`/`skills/**/SKILL.md`/`docs/plans/*.md` puros são domínio de `prompt-reviewer` per ADR-062 — pattern empírico do cluster cross-week NÃO observou prompt-reviewer convergente same-pattern. Posicionar ANTES skiparia prompt-reviewer onde nunca foi medido. Posicionamento APÓS + restrição a doc-reviewer resolved preserva ADR-062 + § Limitações coerentemente.

## Override do critério N=3

7ª aplicação consecutiva da onda Override do critério N=3 (após ADR-057 → -061 → -062 → -063 → -064 → -065). Calibração explícita:

- **Subjacente:** ADR-043 § Ockham operacionalizado critério 4 prescreve N≥3 cross-session antes de codificar pattern emergente. Esta aplicação atinge o piso (3 cross-session em 5 dias adjacentes) mas em contexto homogêneo — todas 6 instâncias empíricas do cluster são bullet/entry siblings em CLAUDE.md/README.md/install.md da mesma reforma editorial (dispatch refactor §3.3/§3.4 + ADR-065 + migrate-to-forge).
- **Fragilidade epistêmica:** plausível que o cluster reflita um único episódio de trabalho com diff homogêneo, não pattern verdadeiramente recorrente em contextos diversos. NOTES § 2026-06-19T21:23:08Z § (1) literalmente recusou override aqui ("disciplina 7 aplicações consecutivas N=3 override") — esta 7ª aplicação ship justifica-se pela substância (skip silente é direção certa per ADR-002 anti-cerimônia) mas reconhece a tensão.
- **Mitigação ativa via critério de erosão auditável:** 3 cláusulas codificadas (false-positive + false-negative + over-fitting >80% same-cluster) permitem detecção mecânica do over-fitting em auditoria post-mortem semestral.
- **Distinção dos precedentes:** ADR-057 → -065 todos overrides com calibração explícita per Ockham — esta segue o mesmo template editorial. Decisão de continuar a onda vs. quebrar a sequência foi consciente: substância empírica (6 close-cleans) + alinhamento doutrinal claro (anti-cerimônia + sub-tool YAGNI evitado) pesaram mais que disciplina N=3 estrita.
- **Gatilho de revisão #1:** teste empírico forward — override detectado em auditoria semestral via 3ª cláusula do critério de erosão (>80% same-cluster) reabre ADR-067 como possivelmente over-fit; refinement do predicado OR revogação são respostas possíveis.
