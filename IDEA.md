# IDEA

> Direção de produto deste repositório. Documento vivo — captura o *porquê* e o *para onde*, não o *como*. Vago de propósito nesta fase; cristaliza com o uso.

## O incômodo que originou isso

Toda vez que começo um projeto novo com assistência de IA, gasto os primeiros dias re-explicando as mesmas coisas. "Não cria três camadas pra um CRUD." "Não põe um adapter onde uma função resolve." "Não escreve docstring de cinco linhas pra um getter." "Antes de propor o fix, reproduz o bug." É sempre o mesmo conjunto de julgamentos — o que eu chamaria de *bom senso de engenharia* — e ele evapora a cada sessão nova, a cada projeto novo, a cada vez que o contexto se perde.

O assistente é capaz; o que falta é **memória de como eu trabalho**. Não as regras de um time genérico, não o estilo médio da internet — o jeito específico, opinativo, de construir software que eu acredito ser o certo: enxuto, direto, sem cerimônia que não paga o próprio custo.

## A visão, em uma frase

Um jeito de **ensinar o assistente a trabalhar do meu jeito uma vez** e ter isso valendo em todo projeto, sem repetição — não como um documento que ninguém lê, mas como comportamento que acontece sozinho na hora certa.

## O que eu imagino

Imagino abrir qualquer repositório e já ter ali, disponível, um conjunto de "instintos" que o assistente carrega comigo:

- Quando eu peço uma mudança não-trivial, alguém me força a **parar e nomear o que estou prestando a fazer** antes de sair codando — porque metade dos meus erros vem de pular essa etapa.
- Quando o código fica pronto, alguém **olha com os olhos certos** — não procurando lint genérico, mas exatamente as coisas que eu acho que importam: abstração prematura, defensividade ornamental, complexidade que não se pagou.
- Quando eu vou fazer besteira óbvia — commitar um segredo, editar um arquivo que não devia — alguém **me segura na porta**, em silêncio, sem eu ter pedido.
- Quando uma decisão importante é tomada, ela **fica registrada** de um jeito que o eu-do-futuro entenda, em vez de virar conhecimento tribal que só vive na minha cabeça.

A palavra que resume o tom de tudo isso é **pragmático**. Não é sobre seguir um método cerimonioso à risca. É o oposto: é sobre remover cerimônia, manter só o que entrega valor concreto, e deixar o resto de fora até que doa o suficiente pra justificar.

## Princípios que quero que vivam nisso

Ainda não sei a forma exata, mas sei o espírito:

- **Faça o mínimo que resolve, bem feito.** Qualidade serve o problema real, não o inverso. Não construir o que não vai usar; mas o que for construir, construir com cuidado.
- **Verifique, não suponha.** Reproduza antes de hipotetizar. Meça antes de generalizar. Não declare pronto sem evidência.
- **Não invente estrutura que não distingue nada.** Refatorar depois costuma ser mais barato do que abstrair cedo demais.
- **O assistente se adapta ao projeto, não o contrário.** O projeto não deveria ter que se contorcer pra caber numa convenção rígida do ferramental. Se eu organizo as coisas de um jeito diferente, ele deveria entender e seguir.

## Para quem é

Pra mim, primeiro — é uma ferramenta pessoal, nasce do meu próprio atrito diário. Mas a aposta é que esse atrito não é só meu: qualquer pessoa que valorize software enxuto e se irrite com cerimônia vazia deveria conseguir adotar isso e sentir que finalmente o assistente "pensa como ela".

## O que isso NÃO é

- Não é um framework de aplicação, nem uma biblioteca pra importar.
- Não é uma metodologia pesada com rituais obrigatórios — seria trair a própria premissa.
- Não é uma tentativa de automatizar o julgamento embora — é o contrário: é dar ao assistente o *meu* julgamento pra ele aplicar.
- Não é genérico de propósito. Ele é **opinativo**. Essa é a graça.

## Sinais de que deu certo

Não tenho métricas ainda — é cedo. Mas saberei que funcionou quando:

- Eu começar um projeto novo e **não precisar re-explicar** como gosto de trabalhar.
- Eu parar de ver no meu próprio código as coisas que eu sei que não deveria ter deixado passar.
- Outras pessoas olharem e disserem "isso captura exatamente como eu queria que a IA me ajudasse".

## O que ainda está em aberto

Quase tudo sobre o *como*. Não sei ainda em quantas peças isso se divide, que forma cada peça toma, onde mora a fronteira entre o que é automático e o que me pergunta antes. Vou descobrir construindo e usando — deixando a forma emergir da dor real, não desenhando tudo no papel antes da hora.

Esta é a estrela-guia. O resto se decide no caminho.
