'''Similarity measures.'''

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>

import editdistance
import numpy as np


def edit_distance(x, y):
    '''Calculates the edit distance between two strings.

    Args:
        x (str): The first string.
        y (str): The second string.

    Returns:
        int: The edit distance between x and y. 0 = same string.
    '''
    return editdistance.eval(x, y)


#TODO: Implement in C for better performance
def lcs(x, y):
    '''Calculates the length of the longest common subsequence between two strings.

    Args:
        x (str): The first string.
        y (str): The second string.

    Returns:
        int: The length of the longest common subsequence between x and y.
    '''
    m = len(x)
    n = len(y)
    # An (m+1) times (n+1) matrix
    C = np.zeros((m + 1, n + 1), dtype=np.int32)
    #C = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                C[i][j] = C[i - 1][j - 1] + 1
            else:
                C[i][j] = max(C[i][j - 1], C[i - 1][j])
    return C[len(C) - 1][len(C[0]) - 1]


def lcs_ratio(x, y):
    '''The length of the longest common subsequence between two strings normalized by the length of longest one.

    Args:
        x (str): The first string.
        y (str): The second string.

    Returns:
        float: The normalized length of the longest common subsequence between x and y.
    '''
    return lcs(x, y) / max(len(x), len(y))


def c_lcs_ratio(x, y):
    '''Complement of LCS ratio.

    Args:
        x (str): The first string.
        y (str): The second string.

    Returns:
        float: 1 - the normalized length of the longest common subsequence between x and y.
    '''
    return 1 - (lcs(x, y) / max(len(x), len(y)))


def c_lcs(x, y):
    '''Complement of LCS length.

    Args:
        x (str): The first string.
        y (str): The second string.

    Returns:
        int: len(x) - longest common subsequence length between x and y.
    '''
    c = len(x) - lcs(x, y)
    return c if c >= 0 else len(x)


# Not exactly a metric, but it is here for the sake of organization.
def word_frequency(lex, word):
    '''Returns the frequency of ``word`` from ``lex``.

    Args:
        lex (dictionary): The lexicon dictionary.
        word (str): The word to be  processed.

    Returns:
        int: The absolute frequency of ``word`` based on ``lex`` frequency list.
             Returns 0 if ``word`` is not contained in ``lex``.
    '''
    return lex[word] if word in lex else 0
