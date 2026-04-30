---
name: gen-tests-python
description: Gera testes pytest para um módulo de um projeto Python, seguindo as convenções pytest + respx + asyncio_mode auto + tmp_path para SQLite. Use quando o projeto for Python e o usuário pedir testes para um módulo ou função.
---

# gen-tests-python

Workflow de scaffolding de testes para projetos Python. Gera arquivo de teste para um alvo (módulo, função, ou descrição livre), respeitando a stack pytest e separando unit/integration.

Esta skill **não** descobre regras de negócio sozinha — quando o projeto tem `docs/domain.md` (path contract do toolkit), consulte-o para identificar invariantes (RNxx) que o código alvo exerce. Quando não tem, cubra caminho feliz + edge cases que o código realmente trata.

## Stack assumida

- **pytest** + **pytest-asyncio** com `asyncio_mode = "auto"` — funções `async def` viram testes assíncronos sem decorator.
- **respx** para mockar HTTP (não usar `unittest.mock` para chamadas de rede).
- **`tmp_path`** para SQLite — não mockar o banco. Mock/prod divergence em camada de persistência é um caso clássico de bug em produção.
- `pythonpath = ["src", "tests"]` — imports diretos a partir de `src/`.

Se o `pyproject.toml` do projeto contradiz alguma dessas premissas (ex.: usa `unittest`, não tem pytest-asyncio), parar e reportar ao usuário antes de gerar.

## Estrutura

- `tests/unit/` — rápido, sem I/O real, sem rede. Mockar HTTP com `respx`.
- `tests/integration/` — marker `@pytest.mark.integration`. Pode escrever em SQLite real (arquivo temporário via `tmp_path`), pode usar fixtures em disco (`tests/fixtures/`).

## Argumentos

O usuário fornece o **alvo do teste**:
- Caminho de módulo: `src/<pacote>/<módulo>.py`
- Caminho de função: `src/<pacote>/<módulo>.py::<função>`
- Descrição livre: `"o caso de uso de registrar pagamento"`

Se ambíguo ou ausente, perguntar antes de gerar.

## Passos

1. **Ler o alvo:** `Read` no arquivo, identificar funções públicas e suas assinaturas. Para descrição livre, localizar o entry point com `grep`.

2. **Mapear invariantes aplicáveis:** consulte `docs/domain.md` do projeto e identifique RNs (ou invariantes nomeadas equivalentes) que o código alvo exerce. Para cada invariante exercida, gerar **dois testes**: caminho feliz (invariante satisfeita) e caminho de violação (deve falhar/recusar). Se o projeto não tem `docs/domain.md`, derive invariantes do próprio código (asserts, raises, validações).

3. **Decidir unit vs integration:**
   - Unit se não tocar SQLite nem rede real.
   - Integration se tocar SQLite ou exercitar pipeline ponta-a-ponta.

4. **Identificar edge cases típicos por domínio:** revisar `docs/design.md` do projeto (peculiaridades de integrações externas) e cobrir tanto caminho feliz quanto violação de invariante. Sem `docs/design.md`, cobrir os edge cases que o próprio código alvo trata explicitamente (raises, branches de erro, validações).

5. **Gerar arquivo** em `tests/unit/test_<módulo>.py` ou `tests/integration/test_<módulo>.py`.

6. **Não criar fixtures novas em `conftest.py`** sem perguntar ao usuário.

## Padrões úteis

- Para tempo, injetar data de referência explícita — não depender de `datetime.now()`.
- Para identificadores externos repetidos (ex.: FITID OFX), gerar chave determinística (hash de campos estáveis).
- Nomes de teste em PT alinhados ao vocabulário ubíquo do projeto: `test_pareamento_recusa_movimentos_sem_data_liquidacao`.
- Asserts diretos: `assert resultado == esperado`. Evitar pytest-mock e libs auxiliares.
- Não exigir TDD estrito; exigir **confiança** no que vai pra produção.

## Validação

```bash
python -m pytest <arquivo_gerado> -x --no-header
```

(Ou `uv run pytest ...` se o projeto usa `uv`.)

Não entregar teste vermelho. Se falhar por bug no código alvo (não no teste), reportar ao usuário em vez de "consertar" o teste.

## O que NÃO fazer

- Não testar invariantes que o código alvo não exerce. RN só entra se a função tocada a usa.
- Não cobrir caminhos hipotéticos — só comportamento real do código.
- Não mockar SQLite — usar `tmp_path`.
- Não usar `unittest.mock` para HTTP — usar `respx`.
- Não criar fixtures globais sem confirmação.
