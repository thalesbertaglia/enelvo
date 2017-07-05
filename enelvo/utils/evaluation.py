'''Methods for evaluating normalization methods'''

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>

from tabulate import tabulate


def load_enelvo_format(file_path, category, only_most_frequent=True):
    '''Loads a file of annotated noisy words in Enelvo Corpus format to a dictionary.

    The annotation format is noisy_word\tcorrection,category,frequency
    If there is more than one annotation for the same noisy word, they are separated by white spaces.

    Args:
        file_path (str): Path to the file containing the annotation.
        category (str): Which category to load (e.g, 'O' for ortographics erros).
        only_most_frequent (boolean): Whether to load ALL possible annotations or only the most frequent.
                                      In case of corrections with equal frequency, the first one is loaded.

    Returns:
        dict: A dictionary with keys being noisy words and the elements lists of their possible corrections.
              If ``only_most_frequent`` the element will be a single string.
    '''
    corrections = dict()
    with open(file_path) as f:
        for line in f:
            elements = line.split()
            if len(elements) > 2:
                if only_most_frequent:
                    max_pos = -1
                    max_freq = 0
                    for i in range(len(elements) - 1):
                        i += 1
                        if int(elements[i].split(',')[-1]) > max_freq and elements[i].split(',')[1] == category and elements[i].split(',')[0] != '#':
                            max_freq = int(elements[i].split(',')[-1])
                            max_pos = i
                    if max_pos != -1:
                        corrections[elements[0]] = elements[max_pos].split(',')[
                            0]
                else:
                    corrs = [corr.split(',')[0] for corr in elements[1:] if corr.split(',')[
                        1] == category and not corr.split(',')[0] == '#']
                    if len(corrs) > 0:
                        corrections[elements[0]] = corrs[0] if len(corrs) == 1 else corrs
            else:
                if elements[1].split(',')[1] == category and elements[1].split(',')[0] != '#':
                    corrections[elements[0]] = elements[1].split(',')[0]
    return corrections
