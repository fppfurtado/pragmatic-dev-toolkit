# Plano — /triage step 0 trata branch remota já deletada como sucesso silente

## Contexto

No 1º dogfood real do step 0 do `/triage` (pós-PR #44), o `git push origin --delete <slug>` falhou porque o GitHub já havia auto-deletado a branch remota ao mergear o PR. A spec atual (`skills/triage/SKILL.md:51`) trata "Falha em qualquer comando após o primeiro" como erro literal + parada — isso vaza erro num cenário que é exatamente o resultado desejado (operador selecionou `Branch remota`; remoto já está limpo).

Stderr canônico do git no cenário, capturado em reprodução isolada (bare repo + `branch -D` no servidor; mesmo resultado em `--delete` e `:branch` legacy):

```
error: unable to delete '<slug>': remote ref does not exist
error: failed to push some refs to '<url>'
exit=1
```

Substring discriminadora estável: `remote ref does not exist`. Ausente em falhas de network (`Could not resolve host`, `connection refused`) e perm (`Permission denied`, `403`) — discriminação não-ambígua.

A frase `branch not found` mencionada no item original do backlog não apareceu no git canônico — não cubro agora (YAGNI; adiciono se aparecer em uso real). `git fetch origin --prune` ao fim do step 0 (linha 53 da SKILL) já cobre refs locais órfãos em ambos os caminhos — não muda.

**Linha do backlog:** `/triage` step 0 cleanup pós-merge: tratar `git push origin --delete <slug>` falhando com `branch not found` / `remote ref does not exist` como sucesso silente + `git fetch --prune` para reconciliar refs locais órfãos. Sintoma observado no 1º dogfood real (pós-PR #44): GitHub auto-delete branches já havia removido a branch remota antes do step 0 rodar; spec atual reportou erro literal e parou, deixando refs órfãos pro operador limpar manual. Outras falhas de `push --delete` (network, perm) continuam reportando literal e parando — discriminação por matching de stderr.

## Resumo da mudança

Adicionar sub-regra ao item `Branch remota` no bloco "Execução das seleções" do step 0 (`skills/triage/SKILL.md`), análoga à sub-regra de `Branch local` (que já discrimina "not fully merged" → `-D`):

- `git push origin --delete <slug>` falha com `remote ref does not exist` no stderr → sucesso silente: reportar `"branch <slug> já estava apagada no remoto"` e seguir.
- Qualquer outra falha (network, perm, etc.) → cai na regra geral existente ("reportar erro literal e parar").

A regra geral permanece — só ganha uma exceção declarada para o item `Branch remota`.

Fica de fora: cobertura para `branch not found` ou variantes não observadas, auto-recovery de falhas em `worktree remove` / `branch -d`, qualquer mudança no `fetch --prune` final.

## Arquivos a alterar

### Bloco 1 — discriminação de stderr no step 0 do /triage {reviewer: code}

- `skills/triage/SKILL.md`: adicionar sub-bullet para `Branch remota` no bloco "Execução das seleções" (entre o sub-bullet de `Branch local` e a regra "Falha em qualquer comando após o primeiro"), descrevendo o ramo silente quando stderr contém `remote ref does not exist`. Preservar a regra geral imediatamente abaixo — ela continua valendo para todos os outros casos.

## Verificação end-to-end

- `grep -n "remote ref does not exist" skills/triage/SKILL.md` retorna a linha da nova sub-regra.
- Releitura textual confirma: (a) sub-regra está dentro de "Execução das seleções", em paralelo ao sub-item de `Branch local`; (b) regra geral "Falha em qualquer comando após o primeiro → reportar erro literal e parar" permanece imediatamente abaixo, intacta; (c) linha "Após todos os candidatos: `git fetch origin --prune`" intacta.
- Mensagem do ramo silente é específica (`"branch <slug> já estava apagada no remoto"`) — não confunde com sucesso real (`git push --delete` ok).

## Verificação manual

Cenários reproduzidos em bare repo isolado em `/tmp` (não toca o GitHub real):

1. **Ramo silente (alvo do fix).** Setup: `mkdir /tmp/v && cd /tmp/v && git init -q && git config user.email r@l && git config user.name r && git commit -q --allow-empty -m i && git checkout -q -b feat-x && git init -q --bare /tmp/o.git && git remote add origin /tmp/o.git && git push -q origin feat-x`. Simular auto-delete remoto: `git -C /tmp/o.git branch -D feat-x`. Executar `git push origin --delete feat-x` e verificar stderr contém `remote ref does not exist` (já confirmado na reprodução durante /triage). **Esperado quando o step 0 do /triage rodar com este estado:** linha curta `"branch feat-x já estava apagada no remoto"`, sem erro vazado, segue para próximos candidatos e `fetch --prune` final.

2. **Falha de network preservada (regressão guard).** Mesmo setup; trocar remote por URL inalcançável: `git remote set-url origin ssh://invalid.example.org/x`. `git push origin --delete feat-x` falha com stderr distinto (sem `remote ref does not exist`). **Esperado:** step 0 reporta literal e para — comportamento atual preservado.

3. **Inspeção textual da regra geral.** Reler `skills/triage/SKILL.md` pós-edit e confirmar que stderrs típicos de perm (`Permission denied (publickey)`, `403 Forbidden`) caem na regra geral — não contêm a substring discriminadora.

## Notas operacionais

- Substring `remote ref does not exist` é mensagem do git client (formatada localmente ao receber o erro do servidor). Estável entre versões; mudança de redação no git futuro faria o matching parar de pegar o cenário e o sintoma reverteria ao atual (erro literal + parada) — degradação graciosa, sem mascaramento de erro genuíno.
- Alternativa rebatida (eixo "abrandar a regra"): tornar toda falha de `push --delete` não-fatal (aviso brando + segue para próximos candidatos), sem discriminação. Descartada para preservar fail-fast em network/perm — discriminação por stderr mantém a regra geral intacta para os outros casos e isola a exceção ao único cenário benigno conhecido.
- Plugin sem test suite (CLAUDE.md): validação manual e revisão textual cobrem; nenhum bloco `{reviewer: qa}` necessário.
