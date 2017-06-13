from enelvo import analytics
from enelvo import preprocessing
from enelvo import candidate_generation
from enelvo import candidate_scoring
from enelvo import metrics
from enelvo.preprocessing import tokenizer


lex_file = open('enelvo/resources/lexicons/freq-cgu.txt')
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
print(top)
