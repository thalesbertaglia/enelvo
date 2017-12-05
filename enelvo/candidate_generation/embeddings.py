'''Candidate generation using word embeddings.'''

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>

import gensim


def generate_by_embedding_model(lex, embedding_model, k=25):
    '''Described in "Exploring Word Embeddings for Unsupervised Textual User-Generated
    Content Normalization, Bertaglia and Nunes(2016)"

    Args:
        lex (dict): The lexicon dictionary.
        embedding_model (obj): The embedding model in word2vec format. Must be readable by gensim.
        k (int): Number of neares neighbours to evaluate (all experiments ran with k=25).

    Returns:
        dict(str: list(str)): A list of possible corrections for each word.
    '''
    cands = {}
    corrs = {}

    cands = {word: [sims[0] for sims in embedding_model.most_similar(
        word, topn=k) if sims[0] not in lex] for word in lex if word in embedding_model}

    for word in cands:
        for c in cands[word]:
            if c not in corrs: corrs[c] = []
            corrs[c].append(word)

    return corrs


def generate_and_score(lex, embedding_model, k=25, lex_sim_weight=0.8):
    '''Described in "Exploring Word Embeddings for Unsupervised Textual User-Generated
    Content Normalization, Bertaglia and Nunes(2016)"

    Args:
        lex (dict): The lexicon dictionary.
        embedding_model (obj): The embedding model in word2vec format. Must be readable by gensim.
        k (int): Number of neares neighbours to evaluate (all experiments ran with k=25).
        lex_sim_weight (float): Weight given to the lexical similarity.

    Returns:
        dict(str: list(str)): A list of scored possible corrections for each word.
    '''
    cands = {}
    corrs = {}

    cands = {word: [sims[0] for sims in embedding_model.most_similar(
        word, topn=k) if sims[0] not in lex] for word in lex if word in embedding_model}
    i = -1
    for word in cands:
        i += 1
        cands_list = []
        print('%.4f%%' % (i/len(cands)*100))
        for c in cands[word]:
            if c not in corrs: corrs[c] = []
            similarity = (lex_sim_weight * metrics.hassan_similarity(word, c)) + \
                ((1 - lex_sim_weight) * embedding_model.similarity(word, c))
            corrs[c].append((word, similarity))

    for c in corrs: corrs[c] = sorted(corrs[c], key=lambda x: x[1], reverse=True)

    print(time.time()-start)
    return corrs
