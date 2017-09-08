import time
import re
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
log_file = open('log-baseline-scoring.log','w')
lex_file = open(
    'enelvo/resources/lexicons/unitex-full-clean+enelvo-ja-corrigido.txt')
lex = {w.strip(): 0 for w in lex_file.readlines()}
corpus = loaders.load_enelvo_format_full(
    'correcoes-enelvo/correcoes-todas-formato-full.txt')
lex_freq = {w.strip().split(',')[0]: int(w.strip().split(',')[1]) for w in open(
    'enelvo/resources/lexicons/freq-cgu.txt').readlines()}
lex_reduzido = {w: 0 for w in lex_freq if lex_freq[w] >= 10}
lex = lex_reduzido
erros = dict()
erros['O'] = loaders.filter_corpus_category(corpus, 'O')
erros['AB'] = loaders.filter_corpus_category(corpus, 'AB')
erros['IN'] = loaders.filter_corpus_category(corpus, 'IN')
ed = [1, 2, 3]
clcsr = [0.2, 0.5, 0.8]

ftop1, ftop5, ftop10 = 0,0,0
top1, top5, top10 = 0,0,0

for r in erros:
    for t in ed:
        print('ED para %s com %f' % (r, t))
        ftop1, ftop5, ftop10 = 0,0,0
        top1, top5, top10 = 0,0,0
        start = time.time()
        cands_ed = list()

        for i in range(len(erros[r])):
            e, c = erros[r][i]

            e = re.sub(r'(.)\1+', r'\1\1\1', e)
            if not isinstance(c, str): continue

            print('%.4f%% analisando %s-%s' % ( (i/len(erros[r])) *100, e, c))
            cands = candidate_generation.generate_by_similarity_metric(
                lex=lex, word=e, threshold=t)

            scored_freq = candidate_scoring.baselines.score_by_frequency(lex=lex_freq,candidates=cands)
            scored_hassan = candidate_scoring.baselines.score_by_similarity_metrics(lex=lex_freq, candidates=cands,
            metrics=[metrics.c_hassan_similarity])

            if len(scored_freq[1]) > 0:
                if c in scored_freq[1][0]: ftop1 += 1
                if len(scored_freq[1]) >= 5:
                    if c in [w[0] for w in scored_freq[1][:5]]: ftop5 += 1
                else:
                    if c in [w[0] for w in scored_freq[1]]: ftop5 += 1

                if len(scored_freq[1]) >= 10:
                    if c in [w[0] for w in scored_freq[1][:10]]: ftop10 += 1
                else:
                    if c in [w[0] for w in scored_freq[1]]: ftop10 += 1

            if len(scored_hassan[1]) > 0:
                if c in scored_hassan[1][0]: top1 += 1
                if len(scored_hassan[1]) >= 5:
                    if c in [w[0] for w in scored_hassan[1][:5]]: top5 += 1
                else:
                    if c in [w[0] for w in scored_hassan[1]]: top5 += 1
                if len(scored_hassan[1]) >= 10:
                    if c in [w[0] for w in scored_hassan[1][:10]]: top10 += 1
                else:
                    if c in [w[0] for w in scored_hassan[1]]: top10 += 1

        '''log_file.write('ED-%s para %s \n\t freq_top1 = %f freq_top5 = %f freq_top10 = %f \n\t hassan_top1 = %f hassan_top5 = %f hassan_top10 = %f\n'
         % (str(t), r, ftop1/len(erros[r]), ftop5/len(erros[r]), ftop10/len(erros[r]), top1/len(erros[r]), top5/len(erros[r]), top10/len(erros[r])))'''

        print('ED-%s para %s \n\t freq_top1 = %f freq_top5 = %f freq_top10 = %f \n\t hassan_top1 = %f hassan_top5 = %f hassan_top10 = %f\n'
         % (str(t), r, ftop1/len(erros[r]), ftop5/len(erros[r]), ftop10/len(erros[r]), top1/len(erros[r]), top5/len(erros[r]), top10/len(erros[r])))
        log_file.write('ED-%s para %s \n\t freq_top1 = %f freq_top5 = %f freq_top10 = %f \n\t hassan_top1 = %f hassan_top5 = %f hassan_top10 = %f\n'
         % (str(t), r, ftop1/len(erros[r]), ftop5/len(erros[r]), ftop10/len(erros[r]), top1/len(erros[r]), top5/len(erros[r]), top10/len(erros[r])))
        log_file.flush()
        print('TIME = '+str(time.time()-start)+'\n')


    for t in clcsr:
        print('LCS para %s com %f' % (r, t))
        ftop1, ftop5, ftop10 = 0,0,0
        top1, top5, top10 = 0,0,0
        start = time.time()
        cands_ed = list()

        for i in range(len(erros[r])):
            e, c = erros[r][i]

            e = re.sub(r'(.)\1+', r'\1\1\1', e)
            if not isinstance(c, str): continue

            print('%.4f%% analisando %s-%s' % ( (i/len(erros[r])) *100, e, c))
            cands = candidate_generation.generate_by_similarity_metric(
                lex=lex, word=e, metric=metrics.c_lcs_ratio, threshold=t)

            scored_freq = candidate_scoring.baselines.score_by_frequency(lex=lex_freq,candidates=cands)
            scored_hassan = candidate_scoring.baselines.score_by_similarity_metrics(lex=lex_freq, candidates=cands,
            metrics=[metrics.c_hassan_similarity])

            if len(scored_freq[1]) > 0:
                if c in scored_freq[1][0]: ftop1 += 1
                if len(scored_freq[1]) >= 5:
                    if c in [w[0] for w in scored_freq[1][:5]]: ftop5 += 1
                else:
                    if c in [w[0] for w in scored_freq[1]]: ftop5 += 1

                if len(scored_freq[1]) >= 10:
                    if c in [w[0] for w in scored_freq[1][:10]]: ftop10 += 1
                else:
                    if c in [w[0] for w in scored_freq[1]]: ftop10 += 1

            if len(scored_hassan[1]) > 0:
                if c in scored_hassan[1][0]: top1 += 1
                if len(scored_hassan[1]) >= 5:
                    if c in [w[0] for w in scored_hassan[1][:5]]: top5 += 1
                else:
                    if c in [w[0] for w in scored_hassan[1]]: top5 += 1
                if len(scored_hassan[1]) >= 10:
                    if c in [w[0] for w in scored_hassan[1][:10]]: top10 += 1
                else:
                    if c in [w[0] for w in scored_hassan[1]]: top10 += 1

        '''log_file.write('ED-%s para %s \n\t freq_top1 = %f freq_top5 = %f freq_top10 = %f \n\t hassan_top1 = %f hassan_top5 = %f hassan_top10 = %f\n'
         % (str(t), r, ftop1/len(erros[r]), ftop5/len(erros[r]), ftop10/len(erros[r]), top1/len(erros[r]), top5/len(erros[r]), top10/len(erros[r])))'''

        print('C-LCS-R%s para %s \n\t freq_top1 = %f freq_top5 = %f freq_top10 = %f \n\t hassan_top1 = %f hassan_top5 = %f hassan_top10 = %f\n'
         % (str(t), r, ftop1/len(erros[r]), ftop5/len(erros[r]), ftop10/len(erros[r]), top1/len(erros[r]), top5/len(erros[r]), top10/len(erros[r])))
        log_file.write('C-LCS-R%s para %s \n\t freq_top1 = %f freq_top5 = %f freq_top10 = %f \n\t hassan_top1 = %f hassan_top5 = %f hassan_top10 = %f\n'
         % (str(t), r, ftop1/len(erros[r]), ftop5/len(erros[r]), ftop10/len(erros[r]), top1/len(erros[r]), top5/len(erros[r]), top10/len(erros[r])))
        log_file.flush()
        print('TIME = '+str(time.time()-start)+'\n')
