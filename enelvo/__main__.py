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

from enelvo import __prog__, __title__, __summary__, __uri__, __version__
from enelvo import analytics
from enelvo import preprocessing
from enelvo import candidate_generation
from enelvo import candidate_scoring
from enelvo import metrics
from enelvo.preprocessing import tokenizer
from enelvo.utils import evaluation
from enelvo.utils import loaders

logger = logging.getLogger(__name__)


def load_options():
    '''
    Loads the options from arguments
    :return: argument_config
    '''
    config_arg_parser = argparse.ArgumentParser(add_help=False, prog=__prog__)
    config_arg_parser.add_argument(
        '--version', action='version', version='%(prog)s {}'.format(__version__))
    config_arg_parser.add_argument(
        '--input', required=True, nargs='?', const='input.txt', help='input file')
    config_arg_parser.add_argument(
        '--output', required=True, nargs='?', const='output.txt', help='output file')
    args, remaining_argv = config_arg_parser.parse_known_args()
    parser = argparse.ArgumentParser(description='{}: {}'.format(__title__, __summary__),
        epilog='Please visit {} for additional help.'.format(__uri__),
            parents=[config_arg_parser], add_help=True)
    parser.add_argument('-l', '--lex', default='unitex-full-clean+enelvo-ja-corrigido.txt', type=str,
        help='file containing the Portuguese lexicon to be used')
    '''parser.add_argument('-f', '--freq', default=10, type=int,
        help='minimum frequency to add word to the dictionary')'''
    parser.add_argument('-t', '--tokenizer', default='regular', type=str,
        help='defines the type of tokenizer to use. ``regular`` (default) replaces entities (numbers, hashtags, urls) for tags and ``readable`` does not.')
    parser.add_argument('-cpns','--capitalize-pns', required=False, action='store_true',
        help='capitalize proper nouns')
    parser.add_argument('-cinis','--capitalize-inis', required=False, action='store_true',
        help='capitalize initials (i.e, after punctuation)')
    parser.add_argument('-cacs','--capitalize-acs', required=False, action='store_true',
        help='capitalize acronyms')
    parser.add_argument('-sn','--sanitize', required=False, action='store_true',
        help='sanitize text (removes punctuation, emoticons, and emojis)')
    parser.add_argument('-th','--threshold', default=3, type=int,
        help='threshold for candidate generation. The higher the number, the higher the number of possible candidates generated - therefore execution takes longer')
    parser.add_argument('-ncds','--n-cands', default=-1, type=int,
        help='number of candidates to be considered for scoring. -1 = all')
    parser.add_argument('-fclst','--force-list', default=None, type=str,
        help='path to force list file. Force list is a list of words that will be considered noisy even if contained in the language lexicon.')
    parser.add_argument('-iglst','--ignore-list', default=None, type=str,
        help='path to ignore list file. Ignore list is a list of words that will be considered correct even if not contained in the language lexicon.')

    argument_config = parser.parse_args()
    return argument_config


def run(options):
    '''Runs enelvo'''
    logger.debug('Running with options:\n{}'.format(options))
    main_path = os.path.split(os.path.abspath(__file__))[0]
    lexicons_path = os.path.join(main_path, 'resources/lexicons/')
    corrs_path = os.path.join(main_path, 'resources/corr-lexicons/')
    embs_path = os.path.join(main_path, 'resources/embeddings/')
    logger.info('Loading lexicons')
    # Lexicon of words considered correct
    main_lex = loaders.load_lex(file_path=lexicons_path+options.lex)
    # Lexicon of foreign words
    es_lex = loaders.load_lex(file_path=corrs_path+'es.txt')
    # Lexicon of proper nouns
    pn_lex = loaders.load_lex(file_path=corrs_path+'pns.txt')
    # Lexicon of acronyms
    ac_lex = loaders.load_lex(file_path=corrs_path+'acs.txt')
    # Force list
    fc_list = loaders.load_lex(file_path=options.force_list) if options.force_list else None
    # Ignore list
    ig_list = loaders.load_lex(file_path=options.ignore_list) if options.ignore_list else None
    # Combined lexicon of 'ok' words
    ok_lex = {**main_lex, **es_lex, **pn_lex, **ac_lex}
    # Lexicon of internet slang
    in_lex = loaders.load_lex_corr(file_path=corrs_path+'in.txt')
    ok_lex = {k: ok_lex[k] for k in ok_lex if k not in in_lex}
    ok_lex = {**ok_lex, **ig_list} if options.ignore_list else ok_lex
    logger.info('Lexicons loaded!')
    # Creates the tokenizer
    tokenizer = preprocessing.new_readable_tokenizer() if options.tokenizer == 'readable' else None
    # Processing:
    total_lines = sum(1 for line in open(options.input))
    line_i = 0
    with open(options.input) as f, open(options.output, 'w') as o:
        for line in f:
            line_i += 1
            logger.info('Processing line '+str(line_i)+' of '+str(total_lines)+'!')
            # Applies all preprocessing steps
            pp_line = preprocessing.tokenize(text=line, tokenizer=tokenizer)
            # Indexes of all oov (noisy) words
            oov_tokens = analytics.identify_oov(lex=ok_lex, force_list=fc_list, tokens=pp_line) if options.force_list else analytics.identify_oov(lex=ok_lex, tokens=pp_line)
            # Normalization process
            for i in oov_tokens:
                if pp_line[i] in in_lex:
                    print(pp_line[i], in_lex[pp_line[i]])
                    pp_line[i] = in_lex[pp_line[i]]
                else:
                    cands = candidate_generation.generate_by_similarity_metric(
                        lex=main_lex, word=pp_line[i], threshold=options.threshold,
                        n_cands=options.n_cands)
                    x = pp_line[i]
                    pp_line[i] = candidate_scoring.score_by_similarity_metrics(lex=main_lex,
                        candidates=cands, metrics=[metrics.hassan_similarity], reverse=True,
                        n_cands=1)[1][0][0]
                    print(x, pp_line[i])
            # Re-sanitizing the text after normalization
            normalized_line = preprocessing.preprocess(text=' '.join(pp_line), tokenizer=tokenizer,
                pn_lex=pn_lex, ac_lex=ac_lex, capitalize_inis=options.capitalize_inis,
                capitalize_pns=options.capitalize_pns, capitalize_acs=options.capitalize_acs,
                do_sanitize=options.sanitize, as_string=True)
            o.write(normalized_line+'\n')
        logger.info('Done! Normalised text written to '+options.output)



def cli():
    '''Add some useful functionality here or import from a submodule'''

    # load the argument options
    options = load_options()

    # configure root logger to print to STDERR
    logger = logging.getLogger(__name__)
    root_logger = configure_stream(level='DEBUG')
    log_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)-5.5s]  %(message)s')

    run(options)


if __name__ == '__main__': cli()
