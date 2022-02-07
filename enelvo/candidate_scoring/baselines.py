"""Normalization candidate scoring baselines."""

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>

from enelvo import metrics


def score_by_frequency(lex, candidates, n_cands=-1):
    """Scores normalization candidates using only their frequencies.

    If the the candidate list has already been scored (i.e, is a list of tuples (word, score1, score2...)),
    the frequency will be applied as the **last** sorting criterion.

    Args:
        lex (dictionary): The lexicon dictionary.
        candidates (list (tuple/str)): The list of normalization candidates - either scored (as tuples) or only strings.
        ncands (int): Number of candidates to be returned (i.e, top ``n_cands`` will be returned according to their frequency).
                      By default, all candidates (-1) are returned.

    Returns:
        tuple(str, list (tuple)): The noisy word and a list of tuples with the top ``n_cands`` sorted by their frequency and the score.
    """
    # If the candidate list is already scored, it must be processed as a list
    # of tuples, thus the concatenation and access to the word itself are different
    is_tuple = lambda x, y: (x + (y,)) if isinstance(x, tuple) else (x, y)
    get_word = lambda x: x[0] if isinstance(x, tuple) else x

    scored_candidates = sorted(
        [
            is_tuple(cand, metrics.word_frequency(lex, get_word(cand)))
            for cand in candidates[1]
        ],
        key=lambda x: x[1:],
        reverse=True,
    )

    return (
        (candidates[0], scored_candidates)
        if n_cands == -1
        else (candidates[0], scored_candidates[:n_cands])
    )


def score_by_similarity_metrics(candidates, metrics=None, n_cands=-1, reverse=False):
    """Scores normalization candidates using similarity metrics.

    Each metric in ``metrics`` will be applied following the list order.
    That means that candidates will be sorted firstly by metrics[0], **then** by metrics[1] and so on...

    Note:
        The candidates will be sorted in the same order for every metric, so choose metrics accordingly.

    Args:
        lex (dictionary): The lexicon dictionary.
        word (string): The word to be normalized.
        candidates (list (function)): The list of metrics to be applied.
        ncands (int): Number of candidates to be returned (i.e, top ``n_cands`` will be returned according to their position).
                      By default, all candidates (-1) are returned.
        reverse (boolean): Which order to sort the candidate list. False = in ascending order according to the metric (higher value = higher similarity).

    Returns:
        list (tuple): A list of tuples with the top ``n_cands`` sorted by each of the metrics and the scores.
    """
    # Default metrics argument
    if not metrics:
        metrics = [metrics.edit_distance]
    # If the candidate list is already scored, it must be processed as a list
    # of tuples, thus the concatenation and access to the word itself are different
    is_tuple = lambda x, y: (x + (y,)) if isinstance(x, tuple) else (x, y)
    get_word = lambda x: x[0] if isinstance(x, tuple) else x

    scored_candidates = candidates[1]
    for m in metrics:
        scored_candidates = [
            is_tuple(cand, m(candidates[0], get_word(cand)))
            for cand in scored_candidates
        ]
    scored_candidates = sorted(scored_candidates, key=lambda x: x[1:], reverse=reverse)

    return (
        (candidates[0], scored_candidates)
        if n_cands == -1
        else (candidates[0], scored_candidates[:n_cands])
    )
