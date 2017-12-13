<h1 align="center">
  <br>
  <a href="thalesbertaglia.com/enelvo"><img src="https://github.com/tfcbertaglia/enelvo/raw/master/enelvo-logo.png" alt="Enelvo" width="400"></a>
</h1>

<h4 align="center">A flexible normaliser for user-generated content.</h4>
Enelvo is a tool for normalising noisy words in user-generated content -- such as tweets, blog posts, and product reviews. It is capable of identifying and normalising spelling mistakes, internet slang, acronyms, proper nouns, and others.

The tool was developed as part of my master's project. You can find more details about how it works in my [dissertation](http://www.teses.usp.br/teses/disponiveis/55/55134/tde-10112017-170919/en.php) (in Portuguese) or in [this paper](http://anthology.aclweb.org/W/W16/W16-3916.pdf) (in English). For more information in Portuguese, please visit the [project website](thalesbertaglia.com/enelvo).

## Getting Started
To clone and run this application, you'll need [Git](https://git-scm.com) and [Python>=3](https://www.python.org/) installed on your computer. First of all, download the repository as a ZIP or run from your command line:

```bash
# Clone this repository
$ git clone https://github.com/tfcbertaglia/enelvo.git

# Go into the repository
$ cd enelvo
```

## Installing
Make sure you have all dependencies installed. If you use [pip](https://pypi.python.org/pypi/pip), simply run `pip install -r requirements.txt`.

After that, run `python3 setup.py install` to install Enelvo.

To make sure that the installation was successful, run:
```bash
python3 -m enelvo --input in.txt --output out.txt
```

If eveything went correctly, ``out.txt`` will be written -- containing the normalised version of ``in.txt``.

Before you start using the normaliser, make sure you download the [normalisation lexicon](https://drive.google.com/file/d/1LqcQMh0pdQnUzDrNiRszDo8v11iwVJrJ/view?usp=sharing). This is a dictionary of pre-calculated normalisations that were learnt from a word embedding model, using the approach described in my dissertation. The lexicon contains many frequent noisy words found on user-generated content and their normalised version. It is used to optimise the tool execution time, so save it in a directory you remember because it will be necessary later!

## Running
You can use the tool, with the most simple configuration, by running:
```bash
python3 -m enelvo --input in.txt --output out.txt -normlex norm_lex.pickle
```
Replace ``norm_lex.pickle`` by the full path of the file you downloaded previously (e.g. ``/enelvo/data/norm_lex.pickle``).

There are two **required** arguments: ``--input`` (path to the input file) and ``--output`` (path+file name to which Enelvo will write the output). Enelvo considers that each line in the input file is a sentence, so format it accordingly. Use option ``-h`` to see the full list of arguments and their explanation.

Each of the arguments and their usage will be explained in the following section.

## Arguments
