import pandas as pd
import numpy as np
import collections
import re

chindex = {}
chbushou = {}
with open('Data/chindexpair.txt', encoding='utf-8') as f:
    lines1 = f.readlines()
with open('Data/chbushoupair.txt', encoding='utf-8') as f:
    lines2 = f.readlines()
for line in lines1:
    li = line.strip('\n').split('\000')
    chindex[li[0]] = li[1]
for line in lines2:
    li = line.strip('\n').split('\000')
    chbushou[li[1]] = li[0]
file = pd.read_excel("Data/CorpusWordlist.xls", header=6)
file = np.array(file)
file = file.tolist()
corpus = collections.defaultdict(int)
numberofcharacter = collections.defaultdict(int)
for i in file:
    for j in i[1]:
        numberofcharacter[j] += i[2]

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

# for epoch in range(1000, 10000, 500):
epoch = 4157
for i in file:
    st = ''
    for j in i[1]:
        if j in chindex and numberofcharacter[j] <= epoch:
            st += chbushou[chindex[j]]
        else:
            st += j
            st += ' '
    # st += '>'
    corpus[st] += i[2]
corpus = Bpe(corpus)
np.save('Data/chinesewordcorpus{0}.npy'.format(epoch), corpus)
corpus = collections.defaultdict(int)