---
name: gen-tests-python
description: Gera testes pytest (respx + asyncio_mode auto + tmp_path para SQLite) para módulo de projeto Python. Use quando o projeto for Python e o operador pedir testes.
roles:
  informational: [ubiquitous_language, design_notes]
---

# gen-tests-python

Workflow de scaffolding de testes para projetos Python. Gera arquivo de teste para um alvo (módulo, função, ou descrição livre), respeitando a stack pytest e separando unit/integration.

Princípio: **não exigir TDD estrito; exigir confiança no que vai pra produção**. Cobertura serve à confiança, não a métricas.

Gera arquivo e devolve o controle ao operador. **Não faz commit** — o operador (ou `/run-plan`) commita conforme convenção do projeto.

A skill **não** descobre regras de negócio sozinha — consulta `ubiquitous_language` para identificar invariantes (RNxx) que o alvo exerce. Resolveu "não temos" → cobrir caminho feliz + edge cases que o código realmente trata.

## Stack assumida

- **pytest** + **pytest-asyncio** com `asyncio_mode = "auto"` (funções `async def` viram testes assíncronos sem decorator).
- **respx** para mock de HTTP (não usar `unittest.mock` para rede).
- **`tmp_path`** para SQLite — não mockar o banco (mock/prod divergence em persistência é caso clássico de bug em produção).
- `pythonpath = ["src", "tests"]` — imports diretos a partir de `src/`.

`pyproject.toml` contradiz alguma premissa (usa `unittest`, sem pytest-asyncio) → parar e reportar antes de gerar.

## Estrutura

- `tests/unit/` — rápido, sem I/O real, sem rede. Mockar HTTP com `respx`.
- `tests/integration/` — marker `@pytest.mark.integration`. SQLite real via `tmp_path`; fixtures em disco em `tests/fixtures/`.

## Argumentos

Alvo do teste:

- Módulo: `src/<pacote>/<módulo>.py`
- Função: `src/<pacote>/<módulo>.py::<função>`
- Descrição livre: `"o caso de uso de registrar pagamento"`

Ambíguo ou ausente → perguntar antes de gerar.

## Passos

1. **Ler o alvo.** `Read` no arquivo, identificar funções públicas e assinaturas. Descrição livre → localizar entry point com `grep`.
2. **Mapear invariantes.** Consultar `ubiquitous_language` e identificar RNs que o alvo exerce. Para cada invariante exercida, gerar **dois testes**: caminho feliz (satisfeita) e violação (deve falhar/recusar). Papel "não temos" → derivar invariantes do próprio código (asserts, raises, validações).
3. **Decidir unit vs integration.** Unit se não toca SQLite nem rede real. Integration se toca SQLite ou exerce pipeline ponta-a-ponta.
4. **Edge cases típicos.** Revisar `design_notes` (peculiaridades de integrações externas). Papel "não temos" → cobrir edge cases que o próprio código trata explicitamente (raises, branches de erro, validações).
5. **Gerar arquivo** em `tests/unit/test_<módulo>.py` ou `tests/integration/test_<módulo>.py`.
6. **Decisão de fixture.** Se alguma fixture é usada por mais de um teste ou módulo, cutucar via `AskUserQuestion` (header `Fixture`) com opções `No próprio arquivo de teste (Recommended)` / `Em conftest.py`. `description` carrega trade-off (isolamento vs. compartilhamento).

## Padrões úteis

- Tempo: injetar data de referência explícita — não depender de `datetime.now()`.
- Identificadores externos repetidos (ex.: FITID OFX): chave determinística (hash de campos estáveis), não `uuid4()`.
- Nomes de teste no idioma do projeto, alinhados ao vocabulário ubíquo. Ex.: PT `test_pareamento_recusa_movimentos_sem_data_liquidacao`, EN `test_matching_rejects_entries_without_settlement_date`.
- Asserts diretos: `assert resultado == esperado`. Evitar pytest-mock e libs auxiliares.

## Validação

```bash
python -m pytest <arquivo_gerado> -x --no-header
```

(Ou `uv run pytest ...` se o projeto usa `uv`.)

Não entregar teste vermelho. Falha por bug no código alvo (não no teste) → reportar ao operador em vez de "consertar" o teste.

## O que NÃO fazer

- Não testar invariantes que o código alvo não exerce — só comportamento real do código.
- Não mockar SQLite — usar `tmp_path`.
- Não usar `unittest.mock` para HTTP — usar `respx`.
