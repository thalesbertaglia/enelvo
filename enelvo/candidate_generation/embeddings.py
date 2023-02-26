"""Candidate generation using word embeddings."""

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>

import pickle
from enelvo import metrics
from enelvo import candidate_scoring
from enelvo.candidate_generation import baselines


def generate_by_embedding_model(lex, embedding_model, k=25):
    """Described in "Exploring Word Embeddings for Unsupervised Textual User-Generated
    Content Normalization, Bertaglia and Nunes(2016)"

    Args:
        lex (dict): The lexicon dictionary.
        embedding_model (obj): The embedding model in word2vec format. Must be readable by gensim.
        k (int): Number of neares neighbours to evaluate (all experiments ran with k=25).

    Returns:
        dict(str: list(str)): A list of possible corrections for each word.
    """
    cands = {}
    corrs = {}

    cands = {
        word: [
            sims[0]
            for sims in embedding_model.most_similar(word, topn=k)
            if sims[0] not in lex
        ]
        for word in lex
        if word in embedding_model
    }

    for word in cands:
        for c in cands[word]:
            if c not in corrs:
                corrs[c] = []
            corrs[c].append(word)

    return corrs


def generate_and_score(
    lex, embedding_model, k=25, lex_sim_weight=0.8, dump_pickle=True
):
    """Described in "Exploring Word Embeddings for Unsupervised Textual User-Generated
    Content Normalization, Bertaglia and Nunes(2016)"

    Args:
        lex (dict): The lexicon dictionary.
        embedding_model (obj): The embedding model in word2vec format. Must be readable by gensim.
        k (int): Number of neares neighbours to evaluate (all experiments ran with k=25).
        lex_sim_weight (float): Weight given to the lexical similarity.
        dump_pickle (boolean): Whether to dump the learnt normalization lexicon to a pickle

    Returns:
        dict(str: list(str)): A list of scored possible corrections for each word.
    """
    cands = {}
    corrs = {}

    cands = {
        word: [
            sims[0]
            for sims in embedding_model.most_similar(word, topn=k)
            if sims[0] not in lex
        ]
        for word in lex
        if word in embedding_model
    }
    for word in cands:
        cands_list = []
        for c in cands[word]:
            if c not in corrs:
                corrs[c] = []
            similarity = (lex_sim_weight * metrics.hassan_similarity(word, c)) + (
                (1 - lex_sim_weight) * embedding_model.similarity(word, c)
            )
            corrs[c].append((word, similarity))
    # Expansion step (read the paper for more details):
    v = {w: 0 for w in list(embedding_model.vocab.keys())}
    noisy_words = {w: 0 for w in v if w not in corrs and w not in lex}
    for w in noisy_words:
        ed_cands = baselines.generate_by_similarity_metric(lex=lex, word=w)
        scored_cands = candidate_scoring.baselines.score_by_similarity_metrics(
            lex=lex,
            candidates=ed_cands,
            metrics=[metrics.hassan_similarity],
            n_cands=1,
            reverse=True,
        )
        if scored_cands[1]:
            corrs[w] = [scored_cands[1][0]]
    # Sorting the list by score
    for c in corrs:
        corrs[c] = sorted(corrs[c], key=lambda x: x[1], reverse=True)
    if dump_pickle:
        pickle.dump(corrs, open("norm_lexicon.pickle", "wb"))
    return corrs
