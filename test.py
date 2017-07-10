import time

from enelvo import analytics
from enelvo import preprocessing
from enelvo import candidate_generation
from enelvo import candidate_scoring
from enelvo import metrics
from enelvo.preprocessing import tokenizer
from enelvo.utils import evaluation
from enelvo.utils import loaders


'''lex_file = open('enelvo/resources/lexicons/freq-cgu.txt')
lex = dict()
for line in lex_file:
    lex[line.split(',')[0]] = line.split(',')[1]

tokenizer = tokenizer.Tokenizer()
text = '¿ki tal? Esse vai ser o uso do nosso mod dlç ;-;)🌚💗'

tokens = preprocessing.preprocess(tokenizer=tokenizer, text=text)
oov = analytics.identify_oov(lex=lex, tokens=tokens)
cands = candidate_generation.baselines.generate_by_similarity_metric(
    lex=lex, word=tokens[oov[3]], n_cands=-1)
top = candidate_scoring.baselines.score_by_similarity_metrics(lex=lex, candidates=cands, n_cands=10)
print(top)'''
log_file = open('results.txt','w')
lex_file = open(
    'enelvo/resources/lexicons/unitex-full-clean+enelvo-ja-corrigido.txt')
lex = {w.strip(): 0 for w in lex_file.readlines()}
corpus = loaders.load_enelvo_format_full(
    'correcoes-enelvo/correcoes-todas-formato-full.txt')
lex_freq = {w.strip().split(',')[0]: int(w.strip().split(',')[1]) for w in open(
    'enelvo/resources/lexicons/freq-cgu.txt').readlines()}
erros = dict()
erros['O'] = loaders.filter_corpus_category(corpus, 'O')
erros['AB'] = loaders.filter_corpus_category(corpus, 'AB')
erros['IN'] = loaders.filter_corpus_category(corpus, 'IN')
ed = [1, 2, 3]
clcsr = [0.2, 0.5, 0.8]

for r in erros:
    for t in ed:
        start = time.time()
        sum_len = 0
        cands_ed = list()

        for i in range(len(erros[r])):
            e, c = erros[r][i]
            #print('%.2f%%' % (i/len(erros_O)))
            cands = candidate_generation.generate_by_similarity_metric(
                lex=lex, word=e, threshold=t)
            cands_ed.append(cands[1])
            sum_len += len(cands[1])

        log_file.write('ED-' + str(t) + ' para ' + r + ' = ',
              evaluation.evaluate_candidate_generation(erros[r], cands_ed)+'\n')
        log_file.write('AVG_NUM_CANDS = %f' % (sum_len / len(cands_ed))+'\n')
        log_file.write('TIME = '+str(time.time()-start)+'\n')


    for t in clcsr:
        start = time.time()
        # LCS
        sum_len = 0
        cands_lcs = list()
        for i in range(len(erros[r])):
            e, _ = erros[r][i]
            #print('%.2f%%' % (i/len(erros_O)))
            cands = candidate_generation.generate_by_similarity_metric(
                lex=lex, word=e, metric=metrics.c_lcs_ratio, threshold=t)
            cands_lcs.append(cands[1])
            sum_len += len(cands[1])
        log_file.write('C-LCS-R-' + str(t) + ' para ' + r + ' = ',
              evaluation.evaluate_candidate_generation(erros[r], cands_lcs)+'\n')
        log_file.write('AVG_NUM_CANDS = %f' % (sum_len / len(cands_lcs))+'\n')
        log_file.write('TIME = ' + str(time.time() - start)+'\n')


    for t in clcsr:
        start = time.time()
        # HASSAN
        sum_len = 0
        cands_hassan = list()
        for i in range(len(erros[r])):
            e, _ = erros[r][i]
            #print('%.2f%%' % (i/len(erros_O)))
            cands = candidate_generation.generate_by_similarity_metric(
                lex=lex, word=e, metric=metrics.c_hassan_similarity, threshold=t)
            cands_hassan.append(cands[1])
            sum_len += len(cands[1])
        log_file.write('C-HASSAN-R-' + str(t) + ' para ' + r + ' = ',
              evaluation.evaluate_candidate_generation(erros[r], cands_hassan)+'\n')
        log_file.write('AVG_NUM_CANDS = %f' % (sum_len / len(cands_hassan))+'\n')
        log_file.write('TIME = ' + str(time.time() - start)+'\n')
