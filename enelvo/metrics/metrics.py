'''Similarity measures.'''

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>

import editdistance
import numpy as np


METRICS_DICT = dict()

# Dict for optimizing metric calculation. Stores already calculated strings.
# 0 = ED, 1 = LCS, 2 = HASSAN
def get_dict():
    global METRICS_DICT
    return METRICS_DICT

def edit_distance(x, y):
    '''Calculates the edit distance between two strings.

    Args:
        x (str): The first string.
        y (str): The second string.

    Returns:
        int: The edit distance between x and y. 0 = same string.
    '''
    METRICS_DICT = get_dict()
    if x not in METRICS_DICT:
        METRICS_DICT[x] = dict()
        METRICS_DICT[x][y] = dict()
        ed = editdistance.eval(x, y)
        METRICS_DICT[x][y][0] = ed
        return ed
    else:
        if y in METRICS_DICT[x]:
            if 0 in METRICS_DICT[x][y]:
                return METRICS_DICT[x][y][0]
            else:
                ed = editdistance.eval(x, y)
                METRICS_DICT[x][y][0] = ed
                return ed
        else:
            METRICS_DICT[x][y] = dict()
            ed = editdistance.eval(x, y)
            METRICS_DICT[x][y][0] = ed
            return ed

def edc(x,y):
    return editdistance.eval(x, y)


def eval_lcs(x, y):
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


def lcs(x, y):
    '''Calculates the length of the longest common subsequence between two strings.

    Args:
        x (str): The first string.
        y (str): The second string.

    Returns:
        int: The length of the longest common subsequence between x and y.
    '''
    METRICS_DICT = get_dict()
    if x not in METRICS_DICT:
        METRICS_DICT[x] = dict()
        METRICS_DICT[x][y] = dict()
        lcsv = eval_lcs(x, y)
        METRICS_DICT[x][y][1] = lcsv
        return lcsv
    else:
        if y in METRICS_DICT[x]:
            if 1 in METRICS_DICT[x][y]:
                return METRICS_DICT[x][y][1]
            else:
                lcsv = eval_lcs(x, y)
                METRICS_DICT[x][y][1] = lcsv
                return lcsv
        else:
            METRICS_DICT[x][y] = dict()
            lcsv = eval_lcs(x, y)
            METRICS_DICT[x][y][1] = lcsv
            return lcsv



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


def diacritic_sym(x, y):
    '''
    '''
    diacritics = dict()
    diacritics['a'] = {'á', 'ã', 'à', 'â'}
    diacritics['e'] = {'é', 'ê'}
    diacritics['i'] = {'í'}
    diacritics['o'] = {'ó', 'õ', 'ô'}
    diacritics['u'] = {'ú'}
    diacritics['c'] = {'ç'}

    symmetry = 0
    for c1, c2 in zip(x, y):
        if c1 in diacritics:
            if c2 in diacritics[c1]: symmetry += 1

        if c2 in diacritics:
            if c1 in diacritics[c2]: symmetry += 1
    return symmetry


def lcs_ratio_sym(x, y):
    '''
    '''
    return (lcs(x, y) + diacritic_sym(x, y)) / max(len(x), len(y))


def hassan_similarity(x, y):
    '''
    '''
    edit = edit_distance(x, y) - diacritic_sym(x, y)
    return lcs_ratio_sym(x, y) / edit if edit else lcs_ratio_sym(x, y)


def c_hassan_similarity(x, y):
    '''
    '''
    '''METRICS_DICT = get_dict()
    if x not in METRICS_DICT:
        METRICS_DICT[x] = dict()
        METRICS_DICT[x][y] = dict()
        edit = edit_distance(x, y) - diacritic_sym(x, y)
        hassan = 1 - (lcs_ratio_sym(x, y) / edit if edit else lcs_ratio_sym(x, y))
        METRICS_DICT[x][y][2] = hassan
        return hassan
    else:
        if y in METRICS_DICT[x]:
            if 2 in METRICS_DICT[x][y]:
                return METRICS_DICT[x][y][2]
            else:
                edit = edit_distance(x, y) - diacritic_sym(x, y)
                hassan = 1 - (lcs_ratio_sym(x, y) / edit if edit else lcs_ratio_sym(x, y))
                METRICS_DICT[x][y][2] = hassan
                return hassan
        else:
            METRICS_DICT[x][y] = dict()
            edit = edit_distance(x, y) - diacritic_sym(x, y)
            hassan = 1 - (lcs_ratio_sym(x, y) / edit if edit else lcs_ratio_sym(x, y))
            METRICS_DICT[x][y][2] = hassan
            return hassan'''
    edit = edit_distance(x, y) - diacritic_sym(x, y)
    hassan = 1 - (lcs_ratio_sym(x, y) / edit if edit else lcs_ratio_sym(x, y))
    return hassan


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
