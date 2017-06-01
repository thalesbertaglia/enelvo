'''Normalization candidate generation by lexical measures.'''

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>

from enelvo import measures


def baseline_ed_freq(lex, word, max_ed=2, n_cands=10):
    '''A simple edit distance + word frequency baseline for candidate generation.

    All canonical words with edit distance below ``max_ed`` are considered
    as candidates, then the ``n_cands`` top ones according to
    their corpus frequency are returned.

    Args:
        lex (dict): The lexicon dictionary.
        word (str): The noisy word to be normalized.
        max_end (int): Maximum edit distance between words to consider them as candidates.
        n_cands (int): Number of candidates to be returned (i.e, top n_cands will be returned according to their frequencies).

    Returns:
        list: A list containing ``n_cands`` normalization candidates.
    '''
    candidates = [(c, lex[c])
                  for c in lex if measures.edit_distance(word, c) <= max_ed]

    return sorted(candidates, key=lambda x: x[1], reverse=True)[:n_cands]


def baseline_ed_lcs(lex, word, max_ed=2, n_cands=10):
    '''A simple edit distance + LCS length baseline for candidate generation.

    All canonical words with edit distance below ``max_ed`` are considered
    as candidates, then the ``n_cands`` top ones according to the LCS length are returned.

    Args:
        lex (dict): The lexicon dictionary.
        word (str): The noisy word to be normalized.
        max_end (int): Maximum edit distance between words to consider them as candidates.
        n_cands (int): Number of candidates to be returned (i.e, top n_cands will be returned according to the LCS length).

    Returns:
        list: A list containing ``n_cands`` normalization candidates.
    '''
    candidates = [(c, measures.lcs(word, c))
                  for c in lex if measures.edit_distance(word, c) <= max_ed]

    return sorted(candidates, key=lambda x: x[1], reverse=True)[:n_cands]


def baseline_ed_lcs_freq(lex, word, max_ed=2, n_cands=10):
    '''A simple edit distance + LCS length + word frequency baseline for candidate generation.

    All canonical words with edit distance below ``max_ed`` are considered
    as candidates, then the ``n_cands`` top ones according to the LCS length are returned.
    When candidates have the same LCS length, their frequency is used as the sorting criterion.

    Args:
        lex (dict): The lexicon dictionary.
        word (str): The noisy word to be normalized.
        max_end (int): Maximum edit distance between words to consider them as candidates.
        n_cands (int): Number of candidates to be returned (i.e, top n_cands will be returned according to the LCS length).

    Returns:
        list: A list containing ``n_cands`` normalization candidates.
    '''
    candidates = [(c, measures.lcs(word, c), lex[c])
                  for c in lex if measures.edit_distance(word, c) <= max_ed]

    return sorted(candidates, key=lambda x: (x[1], x[2]), reverse=True)[:n_cands]


def main():
    lex_file = open('../resources/lexicons/lex-ugcnormal-cb100.txt')

    lex = dict()

    for line in lex_file:
        w = line.split(',')[0].strip()
        n = line.split(',')[1].strip()

        lex[w] = int(n)

    print(baseline_ed_freq(lex, 'vcê'))

if __name__ == '__main__':
    main()
