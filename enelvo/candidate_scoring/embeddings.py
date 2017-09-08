'''Candidate scoring based on word embeddings similarity.'''

# Author: Thales Bertaglia <thalesbertaglia@gmail.com>

from enelvo import metrics


def score_by_embedding_model(lex, embedding_model, candidates, lex_sim_weight=0.8, n_cands=-1):
    scored_candidates = dict()

    for word in candidates:
        cands_list = list()
        for cand in candidates[word]:
            similarity = (lex_sim_weight * metrics.hassan_similarity(word, cand)) + \
                ((1 - lex_sim_weight) * embedding_model.similarity(word, cand))
            cands_list.append((cand, similarity))
        scored_candidates[word] = sorted(
            cands_list, key=lambda x: x[1], reverse=True)
    return scored_candidates if n_cands == -1 or len(scored_candidates) < n_cands else scored_candidates[:n_cands]
