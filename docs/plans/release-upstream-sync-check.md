# `/release` upstream-sync check após recovery do passo 4.5.Aplicar

## Contexto

Defesa pequena flagada pelo `code-reviewer` durante execução do plano `release-head-check-and-action-dedup` (PR #24): após o recovery proativo no passo 4.5.Aplicar fazer `git checkout <branch-da-pré-condição-2>`, há janela em que o branch local pode estar atrás do remote — outro merge/push remoto pode ter acontecido durante a prep da release (passos 1–3, em memória). Sem sincronização, `/release` taggea SHA atrasado e a tag aponta para um estado que o remote já evoluiu.

Sem incidente registrado — gap defensivo. Decisão de design: o recovery já é uma operação assistida (skill puxa o operador de volta para o branch correto sem perguntar); manter coerência fazendo o auto-sync silencioso em vez de cutucar. Operador retoma controle pelo report final ao fim do passo 4.5.

**Linha do backlog:** /release: após `git checkout <branch-da-pré-condição-2>` no recovery proativo do Aplicar, auto-sync com upstream (`git pull --ff-only` se HEAD atrás do remote) antes da sequência (a)-(e) — evita taggear SHA atrasado em janelas concorrentes onde merge/push remoto aconteceu durante prep da release. Flagado pelo `code-reviewer` como gap de design durante execução do plano `release-head-check-and-action-dedup`.

## Resumo da mudança

Bloco único em `skills/release/SKILL.md`, dentro do passo 4.5 sequência `Aplicar`. Após `git checkout <branch-da-pré-condição-2>` (caminho de recovery) e antes da sequência (a)-(e) de escrita+commit+tag, inserir:

- `git fetch origin <branch-atual> 2>/dev/null` para garantir tracking ref atualizado.
- `git rev-list --count HEAD..@{u} 2>/dev/null` para contar commits do remote ainda não locais.
- Count > 0 → `git pull --ff-only origin <branch-atual>` para sincronizar automaticamente. Reportar ao operador o número de commits trazidos. Prosseguir direto para a sequência (a)-(e).
- `pull --ff-only` falha (cenário improvável: commits locais não-empurrados após checkout, ou divergência real) → abortar release com mensagem citando o erro do git e direcionar operador para `git pull` manual + nova invocação de `/release`. Stash criada no recovery permanece intacta.
- Count = 0 ou fetch falha (sem upstream configurado, sem rede) → prosseguir silenciosamente para sequência (a)-(e). Skill não tenta diagnosticar — falta de upstream é configuração legítima.

A sincronização dispara **somente** no caminho de recovery (após o checkout). Caminho não-recovery (HEAD inicial = branch da pré-condição 2 e clean) prossegue direto para (a) — espelha o que o item flagado pelo reviewer prescreveu. Generalização "sempre sincronizar antes de (a)" fica como possível item futuro se a fricção aparecer.

## Arquivos a alterar

### Bloco 1 — skills/release/SKILL.md

Modificar a opção `Aplicar` do gate único (passo 4.5, atualmente em linha 100). Inserir o auto-sync de upstream entre o checkout do recovery e a sequência (a)-(e):

```
- **`Aplicar`** — verificar HEAD: rodar `git symbolic-ref --short HEAD`. Se falha (detached) ou difere do branch da pré-condição 2, recovery proativo — `git status --porcelain`; se não-vazio, `git stash push -m "release v<X.Y.Z> auto-stash"`; depois `git checkout <branch-da-pré-condição-2>`. Em seguida, **antes da sequência (a)-(e)**: `git fetch origin <branch-atual> 2>/dev/null`; `behind=$(git rev-list --count HEAD..@{u} 2>/dev/null || echo 0)`; se `behind > 0`, `git pull --ff-only origin <branch-atual>` (auto-sync silencioso) — `pull --ff-only` falha → abortar release com erro do git e instruir `git pull` manual + nova invocação. Reportar ao operador a ref-atual encontrada no início, o branch esperado, o nome da stash se criada, e o número de commits trazidos pelo pull se aplicável (operador roda `git stash pop` manualmente após release se desejar). Em seguida, executar em sequência: (a) escrever cada `version_file`; (b) inserir entrada no changelog; (c) `git add <paths-específicos>` (**não** `git add -A` — risco de capturar arquivos não-relacionados); (d) `git commit -m "<msg>"`; (e) `git tag -a <tag> -m "Release <tag>"`.
```

Reviewer default `code`. Sem alteração no `## O que NÃO fazer` — guard fica embutido no `Aplicar`.

## Verificação end-to-end

`test_command: null` (repo é meta-tool, sem suite). Substituto textual:

1. **Inspeção da redação:** `skills/release/SKILL.md` passo 4.5.Aplicar contém, nesta ordem: (i) verificação de HEAD via `git symbolic-ref`; (ii) recovery (stash + checkout) quando aplicável; (iii) auto-sync de upstream via `git fetch` + `git rev-list --count HEAD..@{u}` + `git pull --ff-only` quando count > 0; (iv) sequência (a)-(e) inalterada.
2. **Skill estrutura preservada:** `skills/release/SKILL.md` mantém `## Argumentos`, `## Pré-condições`, `## Passos`, `## O que NÃO fazer`. Mudança é cirúrgica em uma única bullet do passo 4.5; outras opções do gate (`Editar`, `Cancelar`) e opções/headers do skill não foram tocados.
3. **Smoke real (post-merge, opcional):** próxima invocação de `/release` em estado sincronizado → auto-sync passa silenciosa (count = 0), sequência (a)-(e) executa. Se operador simular branch atrás do remote (criar commit em outra clone, push, voltar à clone original sem `git pull`), invocar `/release` deve trazer os commits via `git pull --ff-only` e reportar o número trazido antes da sequência (a)-(e).

## Notas operacionais

- Auto-sync **só dispara no caminho de recovery**. Caminho "tudo ok desde o início" pula direto para (a). Justificativa: o item flagado pelo reviewer foi específico ao recovery — o checkout muda HEAD de ref e a chance de divergência aumenta. Generalização (sempre sincronizar antes de (a)) é possível mas adiciona ruído num fluxo já-validado-pela-pré-condição-2; vai para backlog futuro se a fricção aparecer.
- `git fetch origin <branch-atual>` antes do `rev-list` é necessário para o tracking ref refletir o remote atual (sem fetch, `@{u}` é a última snapshot que o local viu). `2>/dev/null` silencia ambiente sem rede ou sem upstream — comportamento "skip silente" é deliberado: skill não diagnostica conectividade, só sincroniza o que conseguir.
- `git pull --ff-only` é deliberado: sincroniza linearmente quando o branch local está estritamente atrás do remote (caso esperado pós-checkout limpo); falha em divergência real (commits locais não-empurrados). Falha → abort com erro literal do git, sem tentativa de merge ou rebase automático (mover história sem revisão é fora da blast radius da skill).
- Stash criada no recovery permanece intacta em qualquer caminho (sucesso, falha de pull, erro tardio). Operador retoma manualmente com `git stash pop` após release se desejar.
