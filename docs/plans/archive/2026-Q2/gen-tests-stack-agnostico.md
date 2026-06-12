# Plano — Migração: gen-tests-python → gen-tests (ADR-008)

## Contexto

Implementação do ADR-008 ("Skills geradoras stack-agnósticas via dispatch interno"). Inverte a "Convenção de naming" para **skills geradoras**: `gen-tests-python` vira `gen-tests` com sub-bloco Python interno; futuras stacks adicionam sub-blocos no mesmo arquivo. Hooks ficam fora da inversão (auto-fira preserva sufixo + auto-gating triplo).

**Linha do backlog:** plugin: skills geradoras stack-agnósticas via dispatch interno — inverter sufixo de stack na "Convenção de naming" (philosophy.md/CLAUDE.md); idioms vivem em sub-blocos do SKILL.md. `gen-tests-python` vira `gen-tests`. Hooks ficam fora. Implementa ADR-008.

## Resumo da mudança

Três superfícies tocadas:

1. **Skill rename atômico**: `skills/gen-tests-python/SKILL.md` → `skills/gen-tests/SKILL.md` com restructure interno em sub-bloco Python; conteúdo atual preservado integralmente; mecânica nova de detecção stack + fallback adicionada.
2. **Doutrina**: `docs/philosophy.md` → "Convenção de naming" reescrita; `CLAUDE.md` → tabela "Plugin component naming and hook auto-gating" atualizada.
3. **CHANGELOG**: breaking marcada via `/release` no momento da publicação — fora de `## Arquivos a alterar`.

Sem mudança em outras skills, agents, hooks, templates. Sem CLI/flag/env nova além do rename do slash command.

## Arquivos a alterar

### Bloco 1 — refactor skills/gen-tests-python → skills/gen-tests com sub-bloco Python {reviewer: code}

- `skills/gen-tests-python/SKILL.md`: deletar.
- `skills/gen-tests/SKILL.md`: criar com:
  - Frontmatter `name: gen-tests`, `description:` enumerando stacks suportadas (hoje só Python), `roles:` informacionais idênticos aos atuais (`ubiquitous_language`, `design_notes`).
  - Seção introdutória stack-agnóstica explicando o dispatch e citando ADR-008 como fonte canônica do critério.
  - Seção "Detecção de stack" com mecânica de marker + fallback (`AskUserQuestion`, header `Stack`) per ADR-008.
  - Sub-seção `### Stack: Python` carregando 100% do conteúdo atual de `gen-tests-python/SKILL.md` (Stack assumida, Estrutura, Argumentos, Passos, Padrões úteis, Validação, O que NÃO fazer) — sem alteração editorial além de promover headers para H4 dentro do sub-bloco.

### Bloco 2 — atualizar doutrina em philosophy.md e CLAUDE.md {reviewer: doc}

- `docs/philosophy.md`: reescrever seção "Convenção de naming" (atual nas linhas 29-35) refletindo a divisão skills geradoras (sem sufixo, sub-bloco interno) vs hooks (com sufixo, auto-gating triplo). Citar ADR-008 como fonte canônica.
- `CLAUDE.md`: atualizar tabela em "Plugin component naming and hook auto-gating" — linha de skill geradora muda coluna "Stack-specific" para "n/a (sub-bloco interno) — ver ADR-008"; linha de hook intacta. Atualizar prosa adjacente que descreve o critério, citando ADR-008.

## Verificação end-to-end

Refactor sem suite executável; gate é inspeção dirigida:

1. **Skill renomeado**:
   - `ls skills/` lista `gen-tests/` e **não** `gen-tests-python/`.
   - `skills/gen-tests/SKILL.md` existe e tem frontmatter `name: gen-tests`.
   - `[ ! -d skills/gen-tests-python ] && echo OK` retorna OK.

2. **Sub-bloco Python preserva conteúdo**:
   - `grep -c "respx\|tmp_path\|asyncio_mode" skills/gen-tests/SKILL.md` retorna ≥3 (idioms críticos preservados).
   - Sub-bloco `### Stack: Python` tem todas as subseções do SKILL antigo (Stack assumida, Estrutura, Argumentos, Passos, Padrões úteis, Validação, O que NÃO fazer).

3. **Mecânica nova de dispatch**:
   - Seção "Detecção de stack" presente com mapeamento marker → stack para Python (futuras stacks ficam como hipotético no ADR, não no SKILL).
   - Fallback documentado para 3 casos: marker ausente / múltiplos markers / sub-bloco ausente.
   - ADR-008 referenciado.

4. **Doutrina alinhada**:
   - `grep -n "ADR-008" docs/philosophy.md CLAUDE.md` retorna ocorrências em ambos.
   - Texto antigo "sintaxe e comando concreto não têm versão neutra" em philosophy.md substituído pelo critério refinado (skill vs hook).
   - Tabela em CLAUDE.md atualizada — linha skill geradora cita sub-bloco interno; linha hook intacta.

5. **Cross-cutting**:
   - `grep -rn "gen-tests-python" --include="*.md" .` retorna apenas referências históricas (planos antigos, ADR-008 que cita o nome antigo no contexto da migração). Skills/agents/CLAUDE.md/philosophy.md/README zero referências ao nome antigo.
   - `marketplace.json`/`plugin.json` não tocados (manifestos não enumeram skills individualmente).

## Verificação manual

**Smoke test pós-merge+reload do plugin** em projeto consumidor Python com `pyproject.toml` na raiz:

1. Slash command aparece como `/gen-tests` (não `/gen-tests-python`).
2. Detecção de stack via `pyproject.toml` funciona — skill prossegue para sub-bloco Python sem perguntar.
3. Geração de teste produz arquivo com idioms preservados (`respx`, `tmp_path`, `@pytest.mark.integration` quando aplicável).
4. Em projeto **sem marker reconhecido** (ex.: repo de docs `.md` apenas), skill faz fallback via `AskUserQuestion` (header `Stack`).

**Cenário sem regressão**: re-rodar `/run-plan` em qualquer plano que dispare 5º warning (cobertura ausente) — deve continuar disparando independente do rename, pois `/run-plan` não referencia `gen-tests-python` por nome.

**Critério de aceitação**: cenários (1)-(4) validados em invocação real.

## Notas operacionais

- Mudança **breaking** marcada no CHANGELOG via `/release` na próxima release. Consumidores com docs/scripts apontando para `/gen-tests-python` atualizam manualmente — alinha com regra anti-shim do `CLAUDE.md`.
- ADR-008 é a fonte canônica do critério; philosophy.md e CLAUDE.md citam o ADR em vez de duplicar a justificativa (ver "Editing conventions" → "Não duplicar conteúdo... — referenciar").
- Sub-bloco Python no novo SKILL.md preserva 100% do conteúdo editorial; revisão deve focar (a) ausência de drift no idiom Python; (b) coerência da nova mecânica de dispatch com a frontmatter; (c) consistência da prosa stack-agnóstica introdutória.
- Bloco 2 toca dois arquivos `.md` (philosophy.md, CLAUDE.md) — `{reviewer: doc}` apropriado para drift de identificadores e cross-refs com ADR-008.
