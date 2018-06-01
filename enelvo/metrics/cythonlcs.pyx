import numpy as np


def cython_eval_lcs(x, y):
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
    C = np.zeros((m + 1, n + 1), dtype=np.int16)
    #C = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                C[i][j] = C[i - 1][j - 1] + 1
            else:
                C[i][j] = max(C[i][j - 1], C[i - 1][j])
    return C[len(C) - 1][len(C[0]) - 1]
