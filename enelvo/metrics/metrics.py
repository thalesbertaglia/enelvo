"""Similarity measures."""

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>
import editdistance
import numpy as np


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
    """Singleton for the cached metrics dictionary."""
    global METRICS_DICT
    return METRICS_DICT


# Dict for storing characters with diacritics
def get_diacritics():
    """Singleton for the diacritics dictionary."""
    global DIACRITICS
    return DIACRITICS


def edit_distance(str_x: str, str_y: str) -> int:
    """Calculates the edit distance between two strings.

    Args:
        str_x: The first string.
        str_y: The second string.

    Returns:
        The edit distance between str_x and str_y. 0 = same string.
    """
    return editdistance.eval(str_x, str_y)


def eval_lcs(str_x: str, str_y: str) -> int:
    """Calculates the length of the longest common subsequence between two strings.

    Args:
        str_x: The first string.
        str_y: The second string.

    Returns:
        The length of the longest common subsequence between str_x and str_y.
    """
    m = len(str_x)
    n = len(str_y)
    # An (m+1) times (n+1) matrix
    C = np.zeros((m + 1, n + 1), dtype=np.int16)
    # C = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str_x[i - 1] == str_y[j - 1]:
                C[i][j] = C[i - 1][j - 1] + 1
            else:
                C[i][j] = max(C[i][j - 1], C[i - 1][j])
    return C[len(C) - 1][len(C[0]) - 1]


def lcs(str_x: str, str_y: str) -> int:
    """Wrapper to ``eval_lcs``.
    Returns the cached version of the metric if it has already been calculated.
    Else, calls ``eval_lcs``.

    Args:
        str_x: The first string.
        str_y: The second string.

    Returns:
        The length of the longest common subsequence between str_x and str_y.
    """
    metrics_dict = get_dict()
    if str_x not in metrics_dict:
        metrics_dict[str_x] = {}
        lcsv = eval_lcs(str_x, str_y)
        metrics_dict[str_x][str_y] = lcsv
        return lcsv

    if str_y in metrics_dict[str_x]:
        return metrics_dict[str_x][str_y]

    lcsv = eval_lcs(str_x, str_y)
    metrics_dict[str_x][str_y] = lcsv
    return lcsv


def lcs_ratio(str_x: int, str_y: int) -> float:
    """The length of the longest common subsequence between two strings
    normalized by the length of longest one.

    Args:
        str_x: The first string.
        str_y: The second string.

    Returns:
        The normalized length of the longest common subsequence between str_x and str_y.
    """
    return lcs(str_x, str_y) / max(len(str_x), len(str_y))


def c_lcs(str_x: str, str_y: str) -> int:
    """Complement of LCS length.

    Args:
        str_x: The first string.
        str_y: The second string.

    Returns:
        len(str_x) - longest common subsequence length between str_x and str_y.
    """
    complement = len(str_x) - lcs(str_x, str_y)
    return complement if complement >= 0 else len(str_x)


def c_lcs_ratio(str_x: str, str_y: str) -> float:
    """Complement of LCS ratio.

    Args:
        str_x: The first string.
        str_y: The second string.

    Returns:
        1 - the normalized length of the longest common subsequence between str_x and str_y.
    """
    return 1 - (lcs(str_x, str_y) / max(len(str_x), len(str_y)))


def diacritic_sym(str_x: str, str_y: str) -> int:
    """Number of characters alligned to their accented version.

    Args:
        str_x: The first string.
        str_y: The second string.

    Returns:
        int: Number of characters alligned to their accented version.
    """
    diacritics = get_diacritics()
    symmetry = 0
    for char_1, char_2 in zip(str_x, str_y):
        if char_1 in diacritics and char_2 in diacritics[char_1]:
            symmetry += 1

        if char_2 in diacritics and char_1 in diacritics[char_2]:
            symmetry += 1
    return symmetry


def lcs_ratio_sym(str_x: str, str_y: str) -> float:
    """The length of the longest common subsequence between two strings + the
    diacritic_sym normalized by the length of longest one.

    Args:
        str_x: The first string.
        str_y: The second string.

    Returns:
        The normalized length of the longest common subsequence between str_x and str_y.
    """
    return (lcs(str_x, str_y) + diacritic_sym(str_x, str_y)) / max(
        len(str_x), len(str_y)
    )


def hassan_similarity(str_x: str, str_y: str) -> float:
    """Similarity measure proposed by Hassan and Menezes (2013) in
    Social Text Normalization using Contextual Graph Random Walks.

    Args:
        str_x: The first string.
        str_y: The second string.

    Returns:
        The hassan similarity between ``str_x``and ``str_y``."
    """
    edit = edit_distance(str_x, str_y) - diacritic_sym(str_x, str_y)
    return lcs_ratio_sym(str_x, str_y) / edit if edit else lcs_ratio_sym(str_x, str_y)


def c_hassan_similarity(str_x: str, str_y: str) -> float:
    """Complement of ``hassan_similarity``.

    Args:
        str_x: The first string.
        str_y: The second string.

    Returns:
        The complement of the hassan similarity between ``str_x``and ``str_y``.
    """
    edit = edit_distance(str_x, str_y) - diacritic_sym(str_x, str_y)
    hassan = 1 - (
        lcs_ratio_sym(str_x, str_y) / edit if edit else lcs_ratio_sym(str_x, str_y)
    )
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
