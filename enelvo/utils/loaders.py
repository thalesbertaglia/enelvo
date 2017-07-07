'''Methods for loading corpus and resources'''

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>


def load_enelvo_format_full(file_path):
    '''Loads the entire Corpus to a dictionary.

    The corpus dictionary is organized as follows:
        corpus[sentence_id]: [ugc_modality],[sentence],[errors_list]
                             [errors_list] (list) -> [word], [position], [category], [correction]

    Args:
        file_path (str): File containing the corpus in full format.

    Returns:
        dict: A dictionary containing every corpus annotation, organized as explained above.
    '''
    corpus = dict()
    text = open(file_path).read()
    anns = text.split('<ann>')
    for i in range(len(anns)):
        ann = anns[i]
        parts = ann.strip().split('\n')
        if len(parts) == 1: continue
        modality = parts[0].split('\t')[0]
        sentence = parts[0].split('\t')[1]

        corpus[i] = dict()
        corpus[i]['mod'] = modality
        corpus[i]['sent'] = sentence
        corpus[i]['errs'] = list()

        for err in parts[1:]:
            word = err.strip().split(',')[0]
            ini_pos, end_pos = err.strip().split(',')[1].split('-')
            cat = err.strip().split(',')[2]
            corr = err.strip().split(',')[3]
            corr = corr if len(corr) > 1 else -1

            entry = dict()
            entry['word'] = word
            entry['pos'] = (ini_pos, end_pos)
            entry['cat'] = cat
            entry['corr'] = corr

            corpus[i]['errs'].append(entry)
    return corpus


def filter_corpus_category(corpus, category):
    '''Returns only corrections with a defined category from the full corpus format.

    Args:
        corpus (dict): Corpus dictionary, loaded with 'load_enelvo_format_full'.
        category (str): Selected category.

    Returns:
        list A list of tuples with format (noisy_word,correction) if noisy_word belongs to ``category``.
    '''
    corrs = list()
    for i in corpus:
        for e in corpus[i]['errs']:
            if e['cat'] == category:
                corrs.append((e['word'],e['corr']))
    return corrs

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
