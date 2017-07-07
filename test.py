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

lex_file = open('enelvo/resources/lexicons/unitex-full-clean+enelvo-ja-corrigido.txt')
lex = {w.strip(): 0 for w in lex_file.readlines()}
corpus = loaders.load_enelvo_format_full('correcoes-enelvo/correcoes-todas-formato-full.txt')
erros_O = loaders.filter_corpus_category(corpus, 'O')
'''
# ED 1
sum_len = 0
cands_O_ed1 = list()
for i in range(len(erros_O)):
    e, _ = erros_O[i]
    #print('%.2f%%' % (i/len(erros_O)))
    cands = candidate_generation.generate_by_similarity_metric(lex=lex, word=e, threshold=1)
    cands_O_ed1.append(cands[1])
    sum_len += len(cands[1])
print('ED-1 = ', evaluation.evaluate_candidate_generation(erros_O,cands_O_ed1))
print('AVG_NUM_CANDS = %f' % (sum_len/len(cands_O_ed1)))

# ED 2
sum_len = 0
cands_O_ed2 = list()
for i in range(len(erros_O)):
    e, _ = erros_O[i]
    #print('%.2f%%' % (i/len(erros_O)))
    cands = candidate_generation.generate_by_similarity_metric(lex=lex, word=e, threshold=2)
    cands_O_ed2.append(cands[1])
    sum_len += len(cands[1])
print('ED-2 = ', evaluation.evaluate_candidate_generation(erros_O,cands_O_ed2))
print('AVG_NUM_CANDS = %f' % (sum_len/len(cands_O_ed2)))'''
# ED 3
sum_len = 0
cands_O_ed3 = list()
for i in range(len(erros_O)):
    e, _ = erros_O[i]
    #print('%.2f%%' % (i/len(erros_O)))
    cands = candidate_generation.generate_by_similarity_metric(lex=lex, word=e, threshold=3)
    cands_O_ed3.append(cands[1])
    sum_len += len(cands[1])
print('ED-3 = ', evaluation.evaluate_candidate_generation(erros_O,cands_O_ed3))
print('AVG_NUM_CANDS = %f' % (sum_len/len(cands_O_ed3)))

# LCS
cands_O_lcs = dict()
for t in [0.4,0.6,0.8]:
    sum_len = 0
    cands_O_lcs[t] = list()
    for i in range(len(erros_O)):
        e, _ = erros_O[i]
        #print('%.2f%%' % (i/len(erros_O)))
        cands = candidate_generation.generate_by_similarity_metric(lex=lex, word=e, metric=metrics.c_lcs_ratio )
        cands_O_lcs[t] = cands[1]
        sum_len += len(cands[1])
    print('C-LCS-R-'+str(t)+' = ', evaluation.evaluate_candidate_generation(erros_O,cands_O_lcs[t]))
    print('AVG_NUM_CANDS = %f' % (sum_len/len(cands_O_lcs[t])))
