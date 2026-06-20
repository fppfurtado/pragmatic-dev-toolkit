# Plano — Parser bullet-agnóstico em /migrate-backlog-to-forge

## Contexto

Sub-tool determinístico de `/migrate-backlog-to-forge` (`skills/migrate-backlog-to-forge/sub-tools/migrate.py:26,57-60`) filtra entries exclusivamente por `ENTRY_PREFIX = "- plugin: "`. Items em `## Próximos` que não começam com esse prefix são silenciosamente dropados; quando 100% dos items são "non-matching", parser retorna `entries: []` e o gate "zero entries" do passo 4 do SKILL.md aborta com mensagem `"## Próximos vazio — config flip suficiente, sem entries pra migrar"`, falsamente reportando seção vazia.

Origem: N=3 migrações empíricas iniciais (meta-system 19 entries + logseq-notes 1 + este repo 7 entries, todas em 2026-06-19) usaram o prefix `- plugin: <texto>` (convenção cross-project do meta-system para indicar repo-alvo de cada item). Futuros consumers cujo BACKLOG.md siga template canonical (scaffold-kit ou markdown puro) usarão bullets sem prefix — parser quebra silenciosamente.

Fix per #136 cutucada: remover ENTRY_PREFIX filter; aceitar qualquer bullet markdown (`- ` ou `* `), strippar bullet marker, texto restante = entry. Backward-compat com `- plugin: <texto>`: items legacy migram com texto `plugin: <texto>` — cosmético, operador edita título no batch da cutucada do passo 6 do SKILL.md.

Alternativas rebatidas no `/triage`: (a) `ENTRY_PREFIX configurável` via CLI arg — rebatida via cutucada `Parser` como YAGNI (N=0 demanda real para per-consumer prefix tuning; adicionar surface configurável especulativa viola Ockham operacionalizado per ADR-043 § critério 4); (b) `strip narrow de plugin: quando detectado` em entries legacy — rebatida porque pattern `- plugin: ` está deprecado (futuras migrações usarão template canonical sem prefix), adicionar regex de compat para caso em fase-out é YAGNI (Ockham critério 4 não satisfeito: 1 caso conhecido, não ≥3).

**Linha do backlog:** #136: `/migrate-backlog-to-forge` — parser overfit a prefix `- plugin: ` reporta falsamente "## Próximos vazio"

**ADRs candidatos:** ADR-066 (skill v0 + contrato lateral do sub-tool — parser é parte do passo 4).

## Resumo da mudança

Parser de `## Próximos` em `migrate.py` passa a aceitar qualquer bullet markdown (`- ` ou `* `) como início de entry, em vez de filtrar exclusivamente por `- plugin: `. Multi-line entries (continuation indentada) preservadas até próximo bullet ou fim de seção. Linhas não-bullet silenciosamente ignoradas (default seguro per Ockham operacionalizado — ADR-043 § critério 1: sem dor real de prosa misturada com bullets em uso real; erro ruidoso seria defensividade ornamental). Backward-compat preservada: items legacy `- plugin: <texto>` migram como entry com texto `plugin: <texto>`.

## Arquivos a alterar

### Bloco 1 — parser bullet-agnóstico {reviewer: qa}

- `skills/migrate-backlog-to-forge/sub-tools/migrate.py`
  - Remover constant `ENTRY_PREFIX` (linha 26).
  - `parse_proximos` (linhas 31-61): substituir `re.split(r"\n(?=- plugin: )", section)` → `re.split(r"\n(?=[-*] )", section)` (aceita `- ` e `* ` como início de bullet); substituir filter `raw.startswith(ENTRY_PREFIX)` por matcher de bullet markdown — `m = re.match(r"^[-*] (.*)$", raw, re.DOTALL)`; se match, entry = `m.group(1).strip()`; senão, drop silente (linhas não-bullet ignoradas — C6 default seguro per Ockham operacionalizado, ADR-043 § critério 1).
  - Update docstring de `parse_proximos` (linhas 32-37): substituir menção a `Stripa prefix \`- plugin: \` pra limpar` → texto descrevendo que aceita bullets `- ` e `* `, entries multi-line preservadas até próximo bullet.

## Verificação end-to-end

Repo sem suíte de testes automatizada (`test_command: null` per CLAUDE.md). Validação centralizada em `## Verificação manual` abaixo. Critérios end-to-end mecânicos pré-merge:

- `grep -n "ENTRY_PREFIX" skills/migrate-backlog-to-forge/sub-tools/migrate.py` retorna 0 linhas (constant removida).
- `grep -n "plugin: " skills/migrate-backlog-to-forge/sub-tools/migrate.py` retorna 0 linhas (referências ao prefix antigo eliminadas).

## Verificação manual

Surface não-determinística (parsing de strings) — cenários exercitam formas reais que parser deve aceitar/rejeitar. Para cada cenário, criar BACKLOG.md sintético em diretório temporário (`/tmp/migrate-test-CN/`) com header `# Backlog\n\n## Próximos\n<conteúdo>\n\n## Concluídos\n` e invocar:

```bash
python3 skills/migrate-backlog-to-forge/sub-tools/migrate.py parse --backlog /tmp/migrate-test-CN/BACKLOG.md
```

- **C1: bullet `- <texto>` simples.** Section com 2 entries `- entry alpha` + `- entry beta`. Esperado: JSON `{"entries": [{"text": "entry alpha"}, {"text": "entry beta"}]}`.
- **C2: bullet `* <texto>`.** Section com `* entry gamma`. Esperado: JSON `{"entries": [{"text": "entry gamma"}]}`.
- **C3: bullet multi-line.** Section com `- entry delta\n  detalhe linha 2`. Esperado: entry preserva newline + indent na string (`"text": "entry delta\n  detalhe linha 2"`).
- **C4: backward-compat — `- plugin: <texto>`.** Section com `- plugin: legacy entry`. Esperado: entry com `"text": "plugin: legacy entry"` (operador edita título no batch — cosmético, não-bug).
- **C5: edge — section vazia.** Header `## Próximos` seguido só de blank lines até `## Concluídos`. Esperado: JSON `{"entries": []}`; SKILL.md passo 4 gate "zero entries" para com mensagem clara.
- **C6: edge — prosa não-bullet.** Section com parágrafo sem `- ` ou `* ` (e.g., uma frase ou bloco de texto). Esperado: JSON `{"entries": []}` (linhas não-bullet ignoradas — default seguro per Ockham operacionalizado, ADR-043 § critério 1; comportamento equivalente a section vazia).

## Decisões absorvidas

- Bloco 2 (SKILL.md passo 4 prose update): removido — reviewer verificou empiricamente que SKILL.md já é agnóstico ao prefix `- plugin: ` (caminho-único).
- `## Verificação end-to-end` critério 2: endurecido para `grep -n "plugin: "` sem qualificador parentético (caminho-único).
- `## Contexto` § alternativas rebatidas: adicionado registro explícito de (a) `ENTRY_PREFIX configurável` (rebatido via cutucada `Parser` como YAGNI) + (b) `strip narrow de plugin:` (rebatido por pattern em fase-out + Ockham critério 4 não satisfeito) (caminho-único).
