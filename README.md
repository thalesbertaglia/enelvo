<h1 align="center">
  <br>
  <a href="http://thalesbertaglia.com/enelvo"><img src="https://github.com/tfcbertaglia/enelvo/raw/master/enelvo-logo.png" alt="Enelvo" width="400"></a>
</h1>

<h4 align="center">A flexible normaliser for user-generated content in Portuguese.</h4>

<p align="center">
<a href="https://github.com/thalesbertaglia/enelvo/actions/workflows/tests.yaml"><img alt="tests" src="https://github.com/thalesbertaglia/enelvo/actions/workflows/tests.yaml/badge.svg"></a>
<a href="https://travis-ci.org/thalesbertaglia/enelvo"><img alt="Build Status" src="https://travis-ci.org/thalesbertaglia/enelvo.svg?branch=master"></a>
<a href='https://coveralls.io/github/thalesbertaglia/enelvo?branch=master'><img src='https://coveralls.io/repos/github/thalesbertaglia/enelvo/badge.svg?branch=master' alt='Coverage Status' /></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

Enelvo is a tool for normalising noisy words in user-generated content written in Portuguese -- such as tweets, blog posts, and product reviews. It is capable of identifying and normalising spelling mistakes, internet slang, acronyms, proper nouns, and others.

The tool was developed as part of my master's project. You can find more details about how it works in my [dissertation](http://www.teses.usp.br/teses/disponiveis/55/55134/tde-10112017-170919/en.php) (in Portuguese) or in [this paper](http://anthology.aclweb.org/W/W16/W16-3916.pdf) (in English). For more information in Portuguese, please visit the [project website](http://thalesbertaglia.com/enelvo).

## Citing
If you use Enelvo or any code from Enelvo in your research work, you are kindly asked to acknowledge the use of the tool in your publications.
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


## Getting Started
You can install Enelvo using `pip` by running:
```bash
pip3 install --user enelvo 
```
To make sure that the installation was successful, run:
```bash
python3 -m enelvo --input in.txt --output out.txt
```
If eveything went correctly, ``out.txt`` will be written -- containing the normalised version of ``in.txt``.

There is also a [REST-based microservice](https://github.com/staticdev/enelvo-microservice) for Enelvo, developed by Thiago D'Ávila. Instructions can be found on the [repository page](https://github.com/staticdev/enelvo-microservice).

## Running
You can use the tool, with the most simple configuration, by running:
```bash
python3 -m enelvo --input in.txt --output out.txt
```

There are two **required** arguments: ``--input`` (path to the input file or folder) and ``--output`` (path+file name or just path, if the input is a folder to which Enelvo will write the output). Enelvo considers that each line in the input file is a sentence, so format it accordingly. Use option ``-h`` to see the full list of arguments and their explanation.

If your input is a folder/directory, you need to use the flag -F. Each output file will be written to the directory specified in ``--output``, as ``original_file_name + .normalized``.

You can also run Enelvo in **interactive mode**. In this case, you will be able to type in sentences and their normalised version will be displayed in real-time. To use interactive mode, just run:
```bash
python3 -m enelvo --interactive
```

Each of the arguments and their usage will be explained in the following section.

## Arguments
There are some arguments that allow you to personalise how Enelvo works. You can find the details by adding ``-h`` or ``--help`` when running the tool. The main ones are:

|                       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Option**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                       	|                  **Default**                  	|                                                    **Description**                                                   	|
|:------------------------------------------------------:	|:---------------------------------------------:	|:--------------------------------------------------------------------------------------------------------------------:	|
| ``-h, --help``                                         	|                       -                       	| Displays list of commands.                                                                                           	|
| ``-l, --lex LEX_FILE``                                 	| ``unitex-full-clean+enelvo-ja-corrigido.txt`` 	| Changes the lexicon of words considered correct.                                                                     	|
| ``-F, --folder``                                 	      |                       - 	                      | Sets input as a folder.                                                                     	                        | 
| ``-iglst, --ignore-list LIST_FILE``                    	|                    ``None``                   	| Sets a list of words that will be ignored by the normaliser.                                                         	|
| ``-fclst, --force-list LIST_FILE``                     	|                    ``None``                   	| Sets a list of words (and optionally their corrections) that will always be processed by the normaliser.             	|
| ``-t, --tokenizer readable``                           	|                  ``regular``                  	| Changes tokeniser configuration. A ``readable`` tokeniser does not replace entities (hashtags, number etc) for tags. 	|
| ``-cpns, --capitalize-pns``                            	|                       -                       	| Capitalises proper nouns (e.g. maria -> Maria).                                                                      	|
| ``-cacs, --capitalize-acs``                            	|                       -                       	| Capitalises acronyms (e.g bbb -> BBB).                                                                               	|
| ``-cinis, --capitalize-inis``                          	|                       -                       	| Capitalises initials in a sentence.                                                                                  	|
| ``-sn, --sanitize``                                    	|                       -                       	| Removes punctuation, emojis, and emoticons from all sentences.                                                       	|


The following sections will explain each one more thoroughly.

### Changing the Lexicon
Argument ``-l`` or ``--lex`` lets you choose the lexicon of words considered correct -- i.e, this argument sets the language dictionary. The input must be the full file path (e.g. ``../some/folder/dict-pt.txt``).

### Ignore and Force Lists
Unfortunately, the language lexicons we use are not perfect. Sometimes they contain words that are not in fact correct, therefore preventing them from being normalised. They also sometimes don't contain words that are correct, thus wrongly marking them as noise.
In order to ease this problem, Enelvo implements **ignore** and **force** lists.

An ignore list is a list of words that will *always* be considered **correct** -- even if not contained in the language lexicon. To use it, add ``-iglst path_to_list`` or ``-ignore-list path_to_list``. The input must be the full path file and the file must contain a single word per line.

A force list is a list of words that will *always* be considered **noisy** -- even if contained in the language lexicon. Thus, these words will alway be normalised. To use it, add ``-fclst path_to_list`` or ``-force-list path_to_list``. The input must be the full path file and the file must contain a single word per line.

For the force list, you can also force a correction. To do so, just write the word and its correction separated by a comma. You can mix both formats, for example:
```bash
vc
q,que
oq, o que
kk
etc
```
Lines containing a comma will assume that the word after the comma is a forced correction. Other lines will just force the word to be corrected regularly by the normaliser.

### Changing the Tokeniser
By default, the tokeniser used in Enelvo replaces some entities with pre-defined tags. Twitter usernames become ``USERNAME``, numbers (including dates, phone numbers etc) -> ``NUMBER``, URLs -> ``URL``, Twitter hashtags -> ``HASHTAG``, emojis -> ``EMOJI`` etc.

If you want to keep the tokens as they are (so no replacement tags), use ``-t readable`` or ``--tokenizer readable``.

### Capitalising Entities
Enelvo can capitalise different entities using lexicons. In order to do so, you just need to set a flag for each entity that you want to capitalise.

To capitalise proper nouns, set ``-cpns`` or ``--capitalize-pns``.

To capitalise acronyms, set ``-cacs`` or ``--capitalize-acs``.

To capitalise initials (first letter after punctuation or at the beggining of a sentence), set ``-cinis`` or ``--capitalize-inis``.

### Cleaning the Text
Enelvo also provides some methods for "cleaning" the text. If you want to remove punctuation, emojis, and emoticons from all sentences, simply set ``-sn``or ``--sanitize``.

### Other Arguments
There are some other arguments used to control the internal functioning of the normalisation methods (like thresholds etc). Use ``-h`` or ``--help`` to see further details.

## What Else?
Everything described here is related to using Enelvo as a *tool*. However, it can be personalised and configured way further when used as an API/library. It is possible to generate and score candidates using a lot of different metrics and methods -- you can even use your own metrics! The easiest way of doing this is using the **Normaliser** class. Have a look at ``example.py`` and ``normaliser.py`` to understand how to start. The code is reasonably well-commented, so it shouldn't be too difficult to understand what is happening.

If you have any questions, comments, suggestions or problems with Enelvo, please feel free to [contact me](http://thalesbertaglia.com).

## Acknowledgements
Many people were fundamental in carrying out this project (and my master's in general), so I would like to thank some of them:

Graça Nunes, Henrico Brum, Rafael Martins, Raphael Silva, and Thiago Pardo, who devoted a (big) portion of their valuable time to annotate the corpus that served as the basis for this project.

Marcos Treviso for helping me organise and implement many parts os this project, and for teaching me a great deal of what I know about NLP.

Carolina Coimbra and Thiago D'Ávila, for being the first ones to use Enelvo, for reporting many bugs, and for suggesting valuable improvements to the tool.

All my fellow labmates from NILC for helping throughout my whole master's.

Thank you all! ❤️
