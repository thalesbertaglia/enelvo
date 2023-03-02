"""Normaliser class. Combines all normalisation methods in a single class."""

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>
import pickle
import os
import logging

from enelvo import metrics
from enelvo import preprocessing
from enelvo import analytics
from enelvo import candidate_generation
from enelvo import candidate_scoring

from enelvo.utils import loaders


class Normaliser:
    def __init__(
        self,
        main_lex=None,
        es_lex=None,
        pn_lex=None,
        ac_lex=None,
        in_lex=None,
        norm_lex=None,
        fc_list=None,
        ig_list=None,
        nrm_en=None,
        tokenizer=None,
        threshold=3,
        n_cands=-1,
        capitalize_inis=False,
        capitalize_pns=False,
        capitalize_acs=False,
        sanitize=False,
        logger=None,
    ):
        """Loads all necessary lexicons."""
        main_path = os.path.split(os.path.abspath(__file__))[0]
        lexicons_path = os.path.join(main_path, "resources/lexicons/")
        corrs_path = os.path.join(main_path, "resources/corr-lexicons/")
        embs_path = os.path.join(main_path, "resources/embeddings/")
        # Lexicon of words considered correct
        self.main_lex = (
            loaders.load_lex(file_path=main_lex)
            if main_lex
            else loaders.load_lex(
                file_path=lexicons_path + "unitex-full-clean+enelvo-ja-corrigido.txt"
            )
        )
        # Lexicon of foreign words
        self.es_lex = (
            loaders.load_lex(file_path=es_lex)
            if es_lex
            else loaders.load_lex(file_path=corrs_path + "es.txt")
        )
        # Lexicon of most frequent english words
        self.english_lex = (
            loaders.load_lex(file_path=lexicons_path + "english-5k.txt")
            if not nrm_en
            else None
        )
        # Lexicon of proper nouns
        self.pn_lex = (
            loaders.load_lex(file_path=pn_lex)
            if pn_lex
            else loaders.load_lex(file_path=corrs_path + "pns.txt")
        )
        # Lexicon of acronyms
        self.ac_lex = (
            loaders.load_lex(file_path=ac_lex)
            if ac_lex
            else loaders.load_lex(file_path=corrs_path + "acs.txt")
        )
        # Force list
        self.fc_list = loaders.load_lex_mixed(file_path=fc_list) if fc_list else None
        # Ignore list
        self.ig_list = loaders.load_lex(file_path=ig_list) if ig_list else None
        # Combined lexicon of 'ok' words
        self.ok_lex = {**self.main_lex, **self.es_lex, **self.pn_lex, **self.ac_lex}
        # Lexicon of internet slang
        self.in_lex = (
            loaders.load_lex_corr(file_path=in_lex)
            if in_lex
            else loaders.load_lex_corr(file_path=corrs_path + "in.txt")
        )
        self.ok_lex = {k: self.ok_lex[k] for k in self.ok_lex if k not in self.in_lex}
        self.ok_lex = {**self.ok_lex, **self.ig_list} if self.ig_list else self.ok_lex
        self.ok_lex = {**self.ok_lex, **self.english_lex} if not nrm_en else self.ok_lex
        # Loads pickle if parameter is set
        self.norm_lex = (
            pickle.load(open(norm_lex, "rb"))
            if norm_lex
            else pickle.load(open(embs_path + "norm_lexicon.pickle", "rb"))
        )
        self.capitalize_inis = capitalize_inis
        self.capitalize_acs = capitalize_acs
        self.capitalize_pns = capitalize_pns
        self.tokenizer = (
            preprocessing.new_readable_tokenizer()
            if tokenizer == "readable"
            else preprocessing.Tokenizer()
            if not tokenizer
            else tokenizer
        )
        self.sanitize = sanitize
        self.threshold = threshold
        self.n_cands = n_cands
        self.logger = logger if logger else logging.getLogger(__name__)
        if self.logger:
            self.logger.info("Lexicons loaded!")

    def normalise(self, sentence):
        """Normalises a given sentence and returns it.
        Args:
            sentece (str): The sentence to be normalised.

        Returns:
            str: Normalised sentence.
        """
        pp_line = preprocessing.tokenize(text=sentence, tokenizer=self.tokenizer)
        oov_tokens = (
            analytics.identify_oov(
                lex=self.ok_lex, force_list=self.fc_list, tokens=pp_line
            )
            if self.fc_list
            else analytics.identify_oov(lex=self.ok_lex, tokens=pp_line)
        )
        for i in oov_tokens:
            # In case force list contains forced corrections
            if self.fc_list and pp_line[i] in self.fc_list:
                pp_line[i] = self.fc_list[pp_line[i]]
                continue
            if pp_line[i] in self.in_lex:
                pp_line[i] = self.in_lex[pp_line[i]]
            else:
                # First option is to normalise according to the learnt lexicon
                if self.norm_lex:
                    if pp_line[i] in self.norm_lex:
                        pp_line[i] = max(self.norm_lex[pp_line[i]], key=lambda x: x[1])[
                            0
                        ]
                    # If a given noisy word has not been learnt, it is normalised
                    # by lexical similarity
                    else:
                        cands = candidate_generation.generate_by_similarity_metric(
                            lex=self.main_lex,
                            word=pp_line[i],
                            threshold=self.threshold,
                            n_cands=self.n_cands,
                        )
                        best_cand = candidate_scoring.score_by_similarity_metrics(
                            candidates=cands,
                            metrics=[metrics.hassan_similarity],
                            reverse=True,
                            n_cands=1,
                        )
                        if best_cand[1]:
                            pp_line[i] = best_cand[1][0][0]
                        else:
                            self.logger.error(
                                'Failed to normalise word "' + pp_line[i] + '"!'
                            )
        # Re-sanitizing the text after normalization
        normalized_line = preprocessing.preprocess(
            text=" ".join(pp_line),
            tokenizer=self.tokenizer,
            pn_lex=self.pn_lex,
            ac_lex=self.ac_lex,
            capitalize_inis=self.capitalize_inis,
            capitalize_pns=self.capitalize_pns,
            capitalize_acs=self.capitalize_acs,
            do_sanitize=self.sanitize,
            as_string=True,
        )
        return normalized_line
