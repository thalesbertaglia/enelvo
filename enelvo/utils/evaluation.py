"""Methods for evaluating normalization methods"""

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>


def evaluate_candidate_generation(list_corrections, list_candidates):
    """Returns the recall (in %) of candidate generation methods.

    Args:
        list_corrections (list): List of tuples with (noisy_word, correction).
        list_candidates (list): List of list(candidates).
        BOTH LISTS MUST BE ALLIGNED!

    Returns
        float: Recall value.
    """
    correct = 0
    for i in range(len(list_corrections)):
        if list_corrections[i][1] in list_candidates[i]:
            correct += 1

    return correct / len(list_corrections)
