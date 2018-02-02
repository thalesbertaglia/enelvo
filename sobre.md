---
layout: page
title: A Ferramenta
---

<h1 align="center">
  <br>
  <a href="thalesbertaglia.com/enelvo"><img src="https://github.com/tfcbertaglia/enelvo/raw/master/enelvo-logo.png" alt="Enelvo" width="400"></a>
</h1>

<h4 align="center">Um normalizador textual de conteúdo gerado por usuário.</h4>
Enelvo é uma ferramenta de normalização de CGU desenvolvida para o português. Ela é capaz de identificar e corrigir ruídos em textos da *web*, como *tweets*, *reviews* de produtos e *posts* em redes sociais. Os principais ruídos tratados são erros ortográficos, internetês, acrônimos, nomes próprios, entre outros.

A ferramenta foi desenvolvida como parte de meu projeto de mestrado. Uma explicação completa de todo os métodos implementados e de como a ferramenta funciona pode ser encontrada em minha [dissertação](http://www.teses.usp.br/teses/disponiveis/55/55134/tde-10112017-170919/en.php) (em português). Uma explicação sucinta do principal método utilizado para normalização está disponível [neste artigo](http://anthology.aclweb.org/W/W16/W16-3916.pdf) (em inglês).

O código da ferramenta está totalmente disponível em um [repositório do GitHub](https://github.com/tfcbertaglia/enelvo).

## Citando
Se usar a ferramenta ou qualquer parte do código em sua pesquisa, pedimos encarecidamente para que cite o seguinte artigo de referência em suas publicações:
>Bertaglia, Thales Felipe Costa, and Maria das Graças Volpe Nunes. "Exploring Word Embeddings for Unsupervised Textual User-Generated Content Normalization." Proceedings of the 2nd Workshop on Noisy User-generated Text (WNUT). 2016.

BibTeX:
```
@inproceedings{bertaglia2016exploring,
  title={Exploring Word Embeddings for Unsupervised Textual User-Generated Content Normalization},
  author={Bertaglia, Thales Felipe Costa and Nunes, Maria das Gra{\c{c}}as Volpe},
  booktitle={Proceedings of the 2nd Workshop on Noisy User-generated Text (WNUT)},
  pages={112--120},
  year={2016}
}
```

## Começando
Para usar a ferramenta, o primeiro passo é obter os arquivos necessários. É necessário ter [Git](https://git-scm.com) e [Python>=3](https://www.python.org/) instalados em seu computador. Você pode baixar o projeto como um arquivo ZIP, diretamente na página do GitHub, ou usar o ``git`` para clonar o repositório executando o seguinte comando:

```bash
# Clonando o repositório
$ git clone https://github.com/tfcbertaglia/enelvo.git

# Indo para o diretório do repositório
$ cd enelvo
```

## Instalação
É necessário instalar todas as dependências do projeto. Se você usa o [pip](https://pypi.python.org/pypi/pip), é só executar o comando ``pip install -r requirements.txt`` para instalar tudo.

Em seguida, execute `python3 setup.py install` para instalar a Enelvo.

Para ter certeza que a instalação funcionou, execute o comando:

```bash
python3 -m enelvo --input in.txt --output out.txt
```

Se tudo deu certo, algumas mensagens serão impressas no terminal e o arquivo ``out.txt`` será gerado -- contendo a versão normalizada do ``in.txt``.

Você também pode usar a ferramenta por meio de um [*microservice* REST](https://github.com/staticdev/enelvo-microservice) desenvolvido por Thiago D'Ávila. Instruções disponível na [página do repositório](https://github.com/staticdev/enelvo-microservice).

### Problemas na Instalação
Se você estiver usando ``conda`` como seu gerenciador de pacotes Python, pode ser que encontre um erro parecido com ``MKL FATAL ERROR: Cannot load libmkl_avx.so or libmkl_def.so`` quando tentar executar a ferramente. Nesse caso, será necessário instalar o pacote ``nokml``. É só executar o comando ``conda install nokml``. Essa [página](https://github.com/BVLC/caffe/issues/3884) apresenta um discussão mais detalhada sobre o problema, com outras soluções também.

## Usando a Ferramenta
Para executar a ferramenta com a configuração padrão, basta utilizar o comando:

```bash
python3 -m enelvo --input in.txt --output out.txt
```

Dois argumentos são **obrigatórios**: ``--input`` (caminho para o arquivo de entrada) e ``--output`` (caminho+nome do arquivo de saída que será escrito). Enelvo considera que cada linha do arquivo de entrada é uma sentença, então formate-o dessa maneira. A opção ``-h`` mostra a lista completa de argumentos e a descrição de cada um.

Você também pode executar Enelvo em **modo interativo**. Nesse caso, você pode digitar sentenças para serem normalizadas e obter a correção em tempo real. Para usar esse modo, basta executar:
```bash
python3 -m enelvo --interactive
```

Os principais argumentos serão explicados na próxima seção.

## Argumentos
Alguns argumentos podem ser utilizados para personalizar o funcionamento da ferramenta. A lista completa pode ser vista utilizando as opções ``-h`` ou ``--help`` ao executar o código.

|                       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Option**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                       	|                  **Default**                  	|                                                    **Description**                                                   	|
|:------------------------------------------------------:	|:---------------------------------------------:	|:--------------------------------------------------------------------------------------------------------------------:	|
| ``-h, --help``                                         	|                       -                       	| Displays list of commands.                                                                                           	|
| ``-l, --lex LEX_FILE``                                 	| ``unitex-full-clean+enelvo-ja-corrigido.txt`` 	| Changes the lexicon of words considered correct.                                                                     	|
| ``-iglst, --ignore-list LIST_FILE``                    	|                    ``None``                   	| Sets a list of words that will be ignored by the normaliser.                                                         	|
| ``-fclst, --force-list LIST_FILE``                     	|                    ``None``                   	| Sets a list of words (and optionally their corrections) that will always be processed by the normaliser.             	|
| ``-t, --tokenizer readable``                           	|                  ``regular``                  	| Changes tokeniser configuration. A ``readable`` tokeniser does not replace entities (hashtags, number etc) for tags. 	|
| ``-cpns, --capitalize-pns``                            	|                       -                       	| Capitalises proper nouns (e.g. maria -> Maria).                                                                      	|
| ``-cacs, --capitalize-acs``                            	|                       -                       	| Capitalises acronyms (e.g bbb -> BBB).                                                                               	|
| ``-cinis, --capitalize-inis``                          	|                       -                       	| Capitalises initials in a sentence.                                                                                  	|
| ``-sn, --sanitize``                                    	|                       -                       	| Removes punctuation, emojis, and emoticons from all sentences.                                                       	|

As próximas subseções vão descrever detalhadamente os principais argumentos.

### Alterando o Léxico
O argumento ``-l`` ou ``--lex`` permite que você selecione qual léxico de palavras corretas será utilizado -- ou seja, esse argumento determina qual é o dicionário da língua. A entrada deve ser o caminho completo do arquivo (por exemplo ``../some/folder/dict-pt.txt``).

### As Listas *Ignore* e *Force*
Infelizmente, o léxico do português utilizado na ferramenta não é perfeito. Às vezes ele erroneamente contém palavras que não são de fato corretas (reconhecidas pela língua), fazendo com que não seja possível normalizá-las. Também há casos que ele não contém palavras que são corretas e que deveriam estar lá, consequentemente fazendo com que elas sejam marcadas como ruído. Para amenizar esse problema, Enelvo implementa as listas **ignore** e **force**.

A lista *ignore* é uma lista de palavras que vão *sempre* ser consideradas como **corretas** -- mesmo que não contidas no léxicos. Ou seja, é uma lista de palavras que serão ignoradas pelo normalizador. Para usar, adicione os argumentos ``-iglst caminho_da_lista`` ou ``-ignore-list caminho_da_lista``. A entrada deve ser o caminho completo do arquivo que contém a lista, que deve conter uma palavra por linha.

A lista *force* é uma lista de palavra que vão *sempre* ser consideradas como **ruído** -- mesmo que estejam contidas no léxico. Ou seja, as palavras dessa lista vão sempre passar pelo processo de normalização. Para usar, adicione os argumentos ``-fclst caminho_da_lista`` ou ``-force-list caminho_da_lista``. A entrada deve ser o caminho completo do arquivo que contém a lista, que deve conter uma palavra por linha.

Para a lista *force*, você pode também forçar uma correção. Para fazer isso, basta escrever a palavra e sua correção separadas por uma vírgula. Os dois formatos (forçando uma correção e não forçando) podem ser misturados, por exemplo:
```bash
vc
q,que
oq, o que
kk
etc
```
Linhas que contêm uma vírgula assume que a palavra depois da vírgula é uma correção forçada da palavra que vem antes. As outras linhas serão consideradas como palavras que serão normalizadas usando a ferramenta.

### Alterando o Tokenizador
Por padrão, o tokenizador utilizado pela Enelvo substitui algumas entidades por *tags* pré-definidas. Nomes de usuários do Twitter são substituídos por ``USERNAME``, números (incluindo datas, telefones etc) por ``NUMBER``, *hashtags* por ``HASHTAG``, urls por ``URL`` etc.

Para evitar que essa substituição ocorra, basta usar ``-t readable`` ou ``--tokenizer readable``.

### Capitalizando Entidades
Enelvo pode capitalizar diferentes entidades por meio de léxicos. É necessário usar um argumento para cada tipo de entidade a ser capitalizada.

Para capitalizar nomes próprios, adicione ``-cpns`` ou ``--capitalize-pns``.

Para capitalizar acrônimos, adicione ``-cacs`` ou ``--capitalize-acs``.

Para capitalizar iniciais (após pontuação ou início de sentença), adicione ``-cinis`` ou ``--capitalize-inis``.

### Limpando o Texto
Enelvo também possui alguns métodos para "limpar" o texto. Se quiser remover pontuação, *emojis* e *emoticons* de todas as sentenças do arquivo de entrada, basta adicionar ``-sn`` ou ``--sanitize``.

### Outros Argumentos
Existem outros argumentos de uso interno da ferramenta, usados para controlar o funcionamento dos métodos de normnalização. Use ``-h`` ou ``--help`` para ver mais detalhes.

## Algo Mais?
Toda explicação até agora é sobre o uso da Enelvo como uma *ferramenta*. No entanto, ela pode ser ainda mais personalizada e configurada se for usada como uma API. É possível, por exemplo, gerar e ranquear candidatos utilizando diversas métricas e métodos -- inclusive você pode implementar suas próprias métricas! O arquivo ``__main__.py`` é um bom ponto inicial para entender como usar o código como uma biblioteca Python. O código em geral está bem comentado e organizado, então não será tão difícil entender como tudo funciona.

Se tiver dúvidas, críticas, comentários, sugestões ou problemas com a Enelvo, entre em [contato comigo](http://thalesbertaglia.com).

## Agradecimentos
Muitas pessoas foram fundamentais para o desenvolvimento deste projeto (e de meu mestrado no geral), então gostaria de agradecer algumas.

Muito obrigado a Graça Nunes, Henrico Brum, Rafael Martins, Raphael Silva e Thiago Pardo por terem disponibilizado uma (grande) parte de seu valioso tempo para anotar o córpus que serviu como base para o projeto.

Obrigado ao Marcos Treviso por me ajudar a organizar e implementar várias partes do projeto e por me ensinar um bom tanto do que sei sobre PLN.

Obrigado a Carolina Coimbra e Thiago D'Ávila, por terem sido os primeiros a usar a Enelvo, por reportarem vários *bugs* e por sugerirem melhorias à ferramenta.

Obrigado a todos os colegas do NILC, por ajudarem em várias coisas ao longo do mestrado.

Valeu! 😬
