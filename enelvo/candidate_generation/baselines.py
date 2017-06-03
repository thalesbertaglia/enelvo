'''Normalization candidate generation baselines.'''

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>

from enelvo import metrics


def generation_similarity_metric(lex, word, metric=metrics.edit_distance, threshold=2, geq=False, n_cands=-1):
    '''A simple similarity metric baseline for candidate generation.

    All canonical words with ``metric`` below ``threshold`` (or above, if ``geq`` is set to True) are considered
    as candidates, then ``n_cands`` are returned in alphabetical order.
    By default, edit distance <= 2 is used.

    Args:
        lex (dict): The lexicon dictionary.
        word (str): The noisy word to be normalized.
        metric (function): The similarity metric.
        threshold (float): Maximum metric value between words to consider them as candidates.
        geq (boolean): Whether the metric must be below or above ``threshold``. If ``geq`` is True, then the threshold is inverted.
        n_cands (int): Number of candidates to be returned (i.e, top ``n_cands`` will be returned according to their frequencies).
                       By default, all candidates (-1) that satisfy the metric threshold are returned.

    Returns:
        list: A list containing ``n_cands`` normalization candidates.
    '''
    # Comparison function changes according to ``geq`` flag.
    comp = lambda x, y: x >= y if geq else x <= y

    candidates = sorted([c for c in lex if comp(metric(word, c), threshold)])

    return candidates if n_cands == -1 else candidates[:n_cands]
