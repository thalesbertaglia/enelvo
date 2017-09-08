---
layout: post
title: O Projeto
---


<div class="message">
  Um normalizador textual flexível de conteúdo gerado por usuário para o português brasileiro.
</div>

Projeto de Mestrado em Ciências de Computação e Matemática Computacional no ICMC-USP. Orientado por **Maria das Graças Volpe Nunes**.

## Resumo


**`[Contexto]`** Conteúdo gerado por usuário (UGC, do inglês *user-generated content*) está disponível em larga escala na *web* e oferece uma rica fonte de informação para empresas e consumidores.
Sistemas de Processamento de Linguagem Natural (PLN) são frequentemente utilizados para extrair conhecimento desse tipo de conteúdo. **`[Lacuna]`** No entanto, UGC tem como característica um 
descompromisso com a norma culta da língua, apresentando desvios de ortografia, gramática, gírias e abreviaturas. Esses ruídos dificultam o funcionamento de técnicas de PLN, afetando assim sua
eficiência. O processo de identificar e corrigir ruídos em textos é denominado normalização textual. Há escassez de sistemas capazes de efetuar normalização, especialmente de UGC. Os poucos sistemas 
existentes são criados para domínios restritos ou lidam com uma quantia limitada de ruído. **`[Propósito]`** O objetivo deste projeto é desenvolver um normalizador textual flexível de UGC para o
português brasileiro, capaz de lidar com diferentes domínios e identificar e corrigir ruídos de maneira personalizada à aplicação de PLN desejada. O normalizador proposto poderá ser acoplado 
a sistemas de PLN e seu funcionamento será flexível de modo a permitir modificações conforme as necessidades da tarefa. **`[Método]`** Arquiteturas neurais com técnicas de aprendizagem profunda vêm sendo 
empregadas para normalização textual pelos trabalhos que atingem o estado da arte. Essas técnicas serão estudadas na revisão bibliográfica de modo a elencar as mais adequadas ao projeto, que então serão
adaptadas e implementadas no sistema. **`[Resultados]`** O resultado esperado é um sistema de normalização que possa ser utilizado para identificar e corrigir ruídos em UGC. Espera-se que o sistema obtenha
resultados satisfatórios na avaliação intrínseca (acurácia de correção de ruído) e na extrínseca (melhoria no desempenho de tarefas de PLN).
