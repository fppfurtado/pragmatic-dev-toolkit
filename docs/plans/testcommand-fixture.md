# Plano — Fixture smoke TestCommand (C1)

## Status

Pendente

## Contexto

Fixture temporário para smoke test do campo `**TestCommand:**` declarativo (ADR-068).

**TestCommand:** echo "consumer-test"

## Resumo da mudança

Smoke test de C1: verifica que `/run-plan` usa o valor declarado em `**TestCommand:**` nos 3 sites de gate (pré-condição 3 baseline + §2 item 2 per-bloco + §3 item 1 gate final), em vez do `test_command: null` do CLAUDE.md local. Fixture temporário — deletar após verificação.

## Arquivos a alterar

### Bloco 1 — fixture noop {reviewer: doc}

- `docs/plans/testcommand-fixture.md`: nenhuma alteração substantiva; bloco existe apenas para disparar o gate per-bloco com `echo "consumer-test"`.

## Verificação end-to-end

Inspeção comportamental dos 3 sites de gate:
1. Pré-condição 3 baseline: output deve conter `consumer-test` (não skip silente como em `test_command: null`).
2. §2 item 2 per-bloco: output de `echo "consumer-test"` ao final do Bloco 1.
3. §3 item 1 gate final: output de `echo "consumer-test"` no gate final.
