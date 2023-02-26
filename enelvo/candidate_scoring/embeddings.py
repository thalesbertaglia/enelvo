"""Candidate scoring based on word embeddings similarity."""

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>

from enelvo import metrics


def score_by_embedding_model(embedding_model, candidates, lex_sim_weight=0.8, n_cands=-1):
    """Described in "Exploring Word Embeddings for Unsupervised Textual User-Generated
    Content Normalization, Bertaglia and Nunes(2016)"

    Args:
        lex (dict): The lexicon dictionary.
        embedding_model (obj): The embedding model in word2vec format. Must be readable by gensim.
        k (int): Number of neares neighbours to evaluate (all experiments ran with k=25).
        lex_sim_weight (float): Weight given to the lexical similarity.
        n_cands (int): Number of candidates to be returned.

    Returns:
        dict(str: list(str)): Top ``n_cands`` scored corrections for each word.
    """
    scored_candidates = {}

    for word in candidates:
        cands_list = []
        for cand in candidates[word]:
            similarity = (lex_sim_weight * metrics.hassan_similarity(word, cand)) + (
                (1 - lex_sim_weight) * embedding_model.similarity(word, cand)
            )
            cands_list.append((cand, similarity))
        scored_candidates[word] = sorted(cands_list, key=lambda x: x[1], reverse=True)
    return (
        scored_candidates
        if n_cands == -1 or len(scored_candidates) < n_cands
        else scored_candidates[:n_cands]
    )


def score_single_word(corrs, word):
    """Returns the best scored correction for a single word, given the lexicon learnt by candidate_generation.

    Args:
        corrs (dict): Dict containing the learnt normalisation lexicon.
        word (str): Word to be normalised.

    Returns:
        tuple (str, float): Best candidate and its score.
    """
    return max(corrs[word], key=lambda x: x[1])
