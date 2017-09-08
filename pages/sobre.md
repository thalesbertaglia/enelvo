---
layout: page
title: Visão Geral
---

<p class="message">
  Mais informações sobre o projeto.
</p>

**Tema:** Normalização textual.

**Título:** Métodos avançados de normalização textual para conteúdo gerado por usuário.

## Lacunas

Conteúdos criados por usuários da Web, especialmente em redes sociais, blogs, sites de reclamações etc. têm como característica um descompromisso com a norma culta da língua, apresentando desvios de 
ortografia, gramática e idiossincrasias próprias do meio digital, como erros de digitação, influência da oralidade na escrita, e vocabulário criado na internet (internetês). 
A esse tipo de texto é comumente atribuído o termo UGC (user-generated content), cuja tradução é “conteúdo gerado por usuário”. Quando se pensa em processar esses textos para algum fim, 
entram em cena as ferramentas de Processamento de Língua Natural (PLN), usualmente desenvolvidas para processar textos sem ruídos, ou que tenham sido “corrigidos” anteriormente. 
Tokenizadores, sentenciadores, taggers, parsers, analisadores semânticos são exemplos de ferramentas de PLN que assumem textos bem-escritos como entrada. Entradas com muitos ruídos causam efeitos 
devastadores no desempenho dessas ferramentas. E, como consequência, as aplicações que as usam certamente sentirão o mesmo efeito. O processo de identificar e corrigir ruídos em textos é denominado normalização textual. Há escassez de sistemas capazes de efetuar normalização, especialmente de UGC. Os poucos sistemas 
existentes são criados para domínios restritos ou lidam com uma quantia limitada de ruído.

## Hipóteses

O uso de um normalizador textual pode melhorar o desempenho de técnicas de PLN. Algumas questões de pesquisa:

* É possível desenvolver um normalizador flexível independente de domínio?
* É possível identificar diversos tipos de ruídos e normalizá-los de acordo com a necessidade da tarefa?
* É possível desenvolver um normalizador que possa ser acoplado ao *pipeline* de tarefas de PLN e adaptado conforme necessidade?

## Objetivos

Desenvolver um normalizador textual flexível de UGC para o
português brasileiro, capaz de lidar com diferentes domínios e identificar e corrigir ruídos de maneira personalizada à aplicação de PLN desejada. O normalizador proposto poderá ser acoplado 
a sistemas de PLN e seu funcionamento será flexível de modo a permitir modificações conforme as necessidades da tarefa. 

## Método

Realizar revisão bibliográfica da área, entender e implementar técnicas de identificação e correção de ruídos. Reunir córpus de textos gerados por usuários em diferentes 
domínios (como blogs e redes sociais) e analisá-los de modo a identificar diferentes tipos de ruídos. Avaliar métodos para identificação automática de ruídos e métodos que efetuem 
sugestões para correção. Comparar os resultados obtidos com trabalhos já publicados para o português brasileiro e possivelmente com outros idiomas.

## Avaliação

O projeto será avaliado de maneira intrínseca (acurácia de correção) e extrínseca (impacto da normalização em tarefas de PLN). Espera-se que o sistema obtenha
resultados satisfatórios que confirmem sua utilidade e eficácia de correção.

## Contribuições Esperadas

Buscamos obter resultados de estado da arte para o português brasileiro, focando em resultados obtidos para outros idiomas com os modelos propostos nos trabalhos recuperados com a revisão bibliográfica.
Todos os métodos e os recursos desenvolvidos ao decorrer do trabalho serão disponibilizados publicamente no [repositório do projeto.](https://github.com/tfcbertaglia/ugcnormal)
