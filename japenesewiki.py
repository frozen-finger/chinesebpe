import pandas as pd
import numpy as np
import collections
import re

df = pd.read_csv("../radicalembedding/.data/wiki_corpus_2.01/Wiki_Corpus_List_2.01.csv")
wikilist = np.array(df)
wikilist = wikilist.tolist()
wordlist = collections.defaultdict(int)
for i in wikilist:
    st = ''
    for j in i[2]:
        if j!='(' and j!=')':
            st += j
            st += ' '
    st += '>'
    wordlist[st] += i[4]

def get_stats(corpus):
    pairs = collections.defaultdict(int)
    for word, freq in corpus.items():
        symbols = word.split()
        for i in range(len(symbols)-1):
            pairs[symbols[i], symbols[i+1]] += freq
    return pairs

def merge_vocab(pair, corpus):
    v_out = {}
    reg = ' '.join(pair)
    p = re.compile(reg)
    for i in corpus:
        new_word = p.sub(''.join(pair), i)
        v_out[new_word] = corpus[i]
    return v_out

def Bpe(corpus, iter=10000):
    # for i in corpus:
    #     if corpus[i]<5:
    #         corpus.pop(i)
    for i in range(iter):
        pairs = get_stats(corpus)
        if len(pairs)<5:
            break
        best = max(pairs, key=pairs.get)
        corpus = merge_vocab(best, corpus)
    return corpus

corpus = Bpe(wordlist)
np.save('Data/Japanesewikicorpus.npy', corpus)