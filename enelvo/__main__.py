#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
enelvo.__main__
~~~~~~~~~~~~~~~~~~~~~~~
The main entry point for the command line interface.
Invoke as ``enelvo`` (if installed)
or ``python -m enelvo`` (no install required).
"""
from __future__ import absolute_import, unicode_literals
from enelvo.log import configure_stream
import argparse
import logging
import os
import pickle

# import gensim

from enelvo import __prog__, __title__, __summary__, __uri__, __version__
from enelvo import analytics
from enelvo import preprocessing
from enelvo import candidate_generation
from enelvo import candidate_scoring
from enelvo import metrics
from enelvo.preprocessing import tokenizer
from enelvo.normaliser import Normaliser
from enelvo.utils import evaluation
from enelvo.utils import loaders
from glob import iglob
from pathlib import Path

logger = logging.getLogger(__name__)


def load_options():
    """
    Loads the options from arguments
    :return: argument_config
    """
    config_arg_parser = argparse.ArgumentParser(add_help=False, prog=__prog__)
    config_arg_parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    config_arg_parser.add_argument(
        "--input",
        required=False,
        nargs="?",
        const="input.txt",
        help="input file or folder",
    )
    config_arg_parser.add_argument(
        "--output",
        required=False,
        nargs="?",
        const="output.txt",
        help="output file or folder",
    )
    config_arg_parser.add_argument(
        "--interactive",
        required=False,
        action="store_true",
        help="runs in interactive mode, allowing user input.",
    )
    parser = argparse.ArgumentParser(
        description="{}: {}".format(__title__, __summary__),
        epilog="Please visit {} for additional help.".format(__uri__),
        parents=[config_arg_parser],
        add_help=True,
    )
    parser.add_argument(
        "-l",
        "--lex",
        default="unitex-full-clean+enelvo-ja-corrigido.txt",
        type=str,
        help="file containing the Portuguese lexicon to be used",
    )
    parser.add_argument(
        "-F",
        "--folder",
        action="store_true",
        help="sets the input to a directory instead of a file",
    )
    """parser.add_argument('-f', '--freq', default=10, type=int,
        help='minimum frequency to add word to the dictionary')"""
    parser.add_argument(
        "-t",
        "--tokenizer",
        default="regular",
        type=str,
        help="defines the type of tokenizer to use. ``regular`` (default) replaces entities (numbers, hashtags, urls) for tags and ``readable`` does not.",
    )
    parser.add_argument(
        "-cpns",
        "--capitalize-pns",
        required=False,
        action="store_true",
        help="capitalize proper nouns",
    )
    parser.add_argument(
        "-cinis",
        "--capitalize-inis",
        required=False,
        action="store_true",
        help="capitalize initials (i.e, after punctuation)",
    )
    parser.add_argument(
        "-cacs",
        "--capitalize-acs",
        required=False,
        action="store_true",
        help="capitalize acronyms",
    )
    parser.add_argument(
        "-sn",
        "--sanitize",
        required=False,
        action="store_true",
        help="sanitize text (removes punctuation, emoticons, and emojis)",
    )
    parser.add_argument(
        "-th",
        "--threshold",
        default=3,
        type=int,
        help="threshold for candidate generation. The higher the number, the higher the number of possible candidates generated - therefore execution takes longer",
    )
    parser.add_argument(
        "-ncds",
        "--n-cands",
        default=-1,
        type=int,
        help="number of candidates to be considered for scoring. -1 = all",
    )
    parser.add_argument(
        "-fclst",
        "--force-list",
        default=None,
        type=str,
        help="path to force list file. Force list is a list of words that will be considered noisy even if contained in the language lexicon.",
    )
    parser.add_argument(
        "-iglst",
        "--ignore-list",
        default=None,
        type=str,
        help="path to ignore list file. Ignore list is a list of words that will be considered correct even if not contained in the language lexicon.",
    )
    # TODO: add an option to learn a normalisation lexicon given an embedding model
    """parser.add_argument('-embs','--embeddings', default=None, type=str,
        help='path to the embedding model.')"""
    parser.add_argument(
        "-normlex",
        "--normlex",
        default="norm_lexicon.pickle",
        type=str,
        help="path to the learnt normalisation lexicon pickle.",
    )
    parser.add_argument(
        "-nrmen",
        "--norm-en",
        default=False,
        required=False,
        action="store_true",
        help="try to normalise english words",
    )
    argument_config = parser.parse_args()
    if (
        not argument_config.interactive
        and not argument_config.input
    ):
        parser.error("--input and --output are required!")
    return argument_config


def run(options):
    """Runs enelvo"""
    logger.debug("Running with options:\n{}".format(options))
    main_path = os.path.split(os.path.abspath(__file__))[0]
    lexicons_path = os.path.join(main_path, "resources/lexicons/")
    corrs_path = os.path.join(main_path, "resources/corr-lexicons/")
    embs_path = os.path.join(main_path, "resources/embeddings/")
    logger.info("Loading lexicons")
    # Lexicon of words considered correct
    main_lex = lexicons_path + options.lex
    # Lexicon of foreign words
    es_lex = corrs_path + "es.txt"
    # Lexicon of proper nouns
    pn_lex = corrs_path + "pns.txt"
    # Lexicon of acronyms
    ac_lex = corrs_path + "acs.txt"
    # Force list
    fc_list = options.force_list if options.force_list else None
    # Ignore list
    ig_list = options.ignore_list if options.ignore_list else None
    # Lexicon of internet slang
    in_lex = corrs_path + "in.txt"
    # Pickle
    norm_lex = embs_path + options.normlex if options.normlex else None
    """emb_model = gensim.models.KeyedVectors.load_word2vec_format(options.embeddings,
                binary=True, unicode_errors='ignore') if options.embeddings else None"""
    # Creates the tokenizer
    tokenizer = (
        preprocessing.new_readable_tokenizer()
        if options.tokenizer == "readable"
        else None
    )
    # Processing:
    # Normaliser object, initialised using the input arguments
    normaliser = Normaliser(
        main_lex,
        es_lex,
        pn_lex,
        ac_lex,
        in_lex,
        norm_lex,
        fc_list,
        ig_list,
        options.norm_en,
        tokenizer,
        options.threshold,
        options.n_cands,
        options.capitalize_inis,
        options.capitalize_pns,
        options.capitalize_acs,
        options.sanitize,
        logger,
    )
    # If not ran in interactive mode, the normaliser processes the whole file
    if not options.interactive:
        if not options.folder:
            total_lines = sum(1 for line in open(options.input, encoding="utf-8"))
            line_i = 0
            with open(options.input, encoding="utf-8") as f, open(
                options.output, "w", encoding="utf-8"
            ) as o:
                for line in f:
                    line_i += 1
                    logger.info(
                        "Processing line "
                        + str(line_i)
                        + " of "
                        + str(total_lines)
                        + "!"
                    )
                    o.write(normaliser.normalise(line) + "\n")
                logger.info("Done! Normalised text written to " + options.output)
        else:
            # Creates the output folder
            Path(options.output).mkdir(parents=True, exist_ok=True)
            for dir_f in filter(
                os.path.isfile, iglob(options.input + "/**", recursive=True)
            ):
                total_lines = sum(1 for line in open(dir_f, encoding="utf-8"))
                line_i = 0
                out_f = os.path.join(
                    options.output, os.path.basename(dir_f) + ".normalized"
                )
                with open(dir_f, encoding="utf-8") as f, open(
                    out_f, "w", encoding="utf-8"
                ) as o:
                    for line in f:
                        line_i += 1
                        logger.info(
                            "Processing line "
                            + str(line_i)
                            + " of "
                            + str(total_lines)
                            + "!"
                        )
                        o.write(normaliser.normalise(line) + "\n")
                    logger.info("Done! Normalised text written to " + out_f)
    # Interactive mode
    else:
        print("\t### Running in interactive mode! ###")
        while True:
            print("Enter a sentence to be normalised or press Ctrl+C to quit:")
            sentence = input()
            print("Normalised sentence:\n\t" + normaliser.normalise(sentence))


def cli():
    """Add some useful functionality here or import from a submodule"""

    # load the argument options
    options = load_options()
    run(options)


if __name__ == "__main__":
    cli()
