"""Similarity measures."""

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>
import functools
import editdistance
import numpy as np

try:
    from enelvo.metrics.cythonlcs import cython_eval_lcs
except ImportError:
    print("Cython installation not found!")

# Constants
METRICS_DICT = {}
DIACRITICS = {}
DIACRITICS["a"] = {"á", "ã", "à", "â"}
DIACRITICS["e"] = {"é", "ê"}
DIACRITICS["i"] = {"í"}
DIACRITICS["o"] = {"ó", "õ", "ô"}
DIACRITICS["u"] = {"ú"}
DIACRITICS["c"] = {"ç"}

# Dict for optimizing metric calculation. Stores already calculated strings.
# 0 = ED, 1 = LCS, 2 = HASSAN
def get_dict():
    global METRICS_DICT
    return METRICS_DICT


# Dict for storing characters with diacritics
def get_diacritics():
    global DIACRITICS
    return DIACRITICS


def edit_distance(x: str, y: str) -> int:
    """Calculates the edit distance between two strings.

    Args:
        x: The first string.
        y: The second string.

    Returns:
        The edit distance between x and y. 0 = same string.
    """
    return editdistance.eval(x, y)


def eval_lcs(x: str, y: str, cython: bool = True) -> int:
    """Calculates the length of the longest common subsequence between two strings.

    Args:
        x: The first string.
        y: The second string.
        cython: Whether to use the cython implementation of the method.

    Returns:
        The length of the longest common subsequence between x and y.
    """
    if cython:
        return cython_eval_lcs(x, y)
    else:
        m = len(x)
        n = len(y)
        # An (m+1) times (n+1) matrix
        C = np.zeros((m + 1, n + 1), dtype=np.int16)
        # C = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if x[i - 1] == y[j - 1]:
                    C[i][j] = C[i - 1][j - 1] + 1
                else:
                    C[i][j] = max(C[i][j - 1], C[i - 1][j])
        return C[len(C) - 1][len(C[0]) - 1]


def lcs(x: str, y: str) -> int:
    """Wrapper to ``eval_lcs``.
    Returns the cached version of the metrics if it has already been calculated. Else, calls ``eval_lcs``.

    Args:
        x: The first string.
        y: The second string.

    Returns:
        The length of the longest common subsequence between x and y.
    """
    METRICS_DICT = get_dict()
    if x not in METRICS_DICT:
        METRICS_DICT[x] = {}
        lcsv = eval_lcs(x, y)
        METRICS_DICT[x][y] = lcsv
        return lcsv
    else:
        if y in METRICS_DICT[x]:
            return METRICS_DICT[x][y]
        else:
            lcsv = eval_lcs(x, y)
            METRICS_DICT[x][y] = lcsv
            return lcsv


def lcs_ratio(x: int, y: int) -> float:
    """The length of the longest common subsequence between two strings normalized by the length of longest one.

    Args:
        x: The first string.
        y: The second string.

    Returns:
        The normalized length of the longest common subsequence between x and y.
    """
    return lcs(x, y) / max(len(x), len(y))


def c_lcs(x: str, y: str) -> int:
    """Complement of LCS length.

    Args:
        x: The first string.
        y: The second string.

    Returns:
        len(x) - longest common subsequence length between x and y.
    """
    c = len(x) - lcs(x, y)
    return c if c >= 0 else len(x)


def c_lcs_ratio(x: str, y: str) -> float:
    """Complement of LCS ratio.

    Args:
        x: The first string.
        y: The second string.

    Returns:
        1 - the normalized length of the longest common subsequence between x and y.
    """
    return 1 - (lcs(x, y) / max(len(x), len(y)))


def diacritic_sym(x: str, y: str) -> int:
    """Number of characters alligned to their accented version.

    Args:
        x: The first string.
        y: The second string.

    Returns:
        int: Number of characters alligned to their accented version.
    """
    diacritics = get_diacritics()
    symmetry = 0
    for c1, c2 in zip(x, y):
        if c1 in diacritics:
            if c2 in diacritics[c1]:
                symmetry += 1

        if c2 in diacritics:
            if c1 in diacritics[c2]:
                symmetry += 1
    return symmetry


def lcs_ratio_sym(x, y):
    """The length of the longest common subsequence between two strings + the
    diacritic_sym normalized by the length of longest one.

    Args:
        x (str): The first string.
        y (str): The second string.

    Returns:
        float: The normalized length of the longest common subsequence between x and y.
    """
    return (lcs(x, y) + diacritic_sym(x, y)) / max(len(x), len(y))


def hassan_similarity(x, y):
    """Similarity measure proposed by Hassan and Menezes (2013) in
    "Social Text Normalization using Contextual Graph Random Walks"
    """
    edit = edit_distance(x, y) - diacritic_sym(x, y)
    return lcs_ratio_sym(x, y) / edit if edit else lcs_ratio_sym(x, y)


def c_hassan_similarity(x, y):
    """Complement of hassan_similarity."""
    edit = edit_distance(x, y) - diacritic_sym(x, y)
    hassan = 1 - (lcs_ratio_sym(x, y) / edit if edit else lcs_ratio_sym(x, y))
    return hassan


# Not exactly a metric, but it is here for the sake of organization.
def word_frequency(lex, word):
    """Returns the frequency of ``word`` from ``lex``.

    Args:
        lex (dictionary): The lexicon dictionary.
        word (str): The word to be  processed.

    Returns:
        int: The absolute frequency of ``word`` based on ``lex`` frequency list.
             Returns 0 if ``word`` is not contained in ``lex``.
    """
    return lex[word] if word in lex else 0
