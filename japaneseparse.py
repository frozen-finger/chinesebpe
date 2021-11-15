import MeCab as mecab
import numpy as np
import re
import collections

chbushou = {}
chindex = {}
jkanji = {}
jbushouindex = {}
stopwords = []
with open("Data/Japanese_stopwords", encoding='utf-8') as f:
    linestop = f.readlines()
with open("Data/train", encoding='utf-8') as f:
    lines = f.readlines()
with open("Data/chbushoupair.txt", encoding='utf-8') as f:
    lineschbushou = f.readlines()
with open("Data/chindexpair.txt", encoding='utf-8') as f:
    lineschindex = f.readlines()
with open("Data/jkanjii", encoding='utf-8') as f:
    linesjkanji = f.readlines()
with open("Data/jbushouindex", encoding='utf-8') as f:
    linesjbushouindex = f.readlines()
for line in linestop:
    word = [w for w in line.strip('\n')]
    stopwords.append(word)
for line in lineschbushou:
    li = line.strip('\n').split('\000')
    chbushou[li[1]] = li[0]
for line in lineschindex:
    li = line.strip('\n').split('\000')
    chindex[li[0]] = li[1]
for line in linesjbushouindex:
    li = line.strip('\n').split(' ')
    jbushouindex[li[1]] = li[0]
for line in linesjkanji:
    li = line.strip('\n').split(' ')
    jkanji[li[0]] = li[1]
sentence = []
target = []

for line in lines:
    sentence.append(line.strip('\n').split('	')[1])
tagger = mecab.Tagger('-Owakati')
for sen in sentence:
    bushousen = tagger.parse(sen.strip('\n'))
    newsen = bushousen
    for index in range(len(bushousen)):
        if bushousen[index] in jkanji:
            newsen = newsen[:index] + jbushouindex[jkanji[bushousen[index]]] + newsen[index + 1:-1]
        elif bushousen[index] in chindex:
            newsen = newsen[:index] + chbushou[chindex[bushousen[index]]] + newsen[index + 1:-1]
    target.append(newsen.split(' '))
dic = collections.defaultdict(int)
fdic = collections.defaultdict(int)
special = {'@':1, '[':1, ']':1, '+':1, '(':1, '\\':1, '.':1, '^':1, '<':1, ')':1, '?':1, '*':1, '#':1, '|':1, '$':1}
for i in target:
    for j in i:
        dic[j]+=1
for key in dic:
    if dic[key] >1:
        st = ''
        for i in key:
            st += i
            st += ' '
        st += '>'
        fdic[st] = dic[key]


def get_stats(corpus):
    pairs = collections.defaultdict(int)
    for word, freq in corpus.items():
        symbols = word.split()
        for i in range(len(symbols)-1):
            pairs[symbols[i], symbols[i+1]] += freq
    return pairs

def merge_vocab(pair, corpus):
    v_out = {}
    pai = ' '.join(pair)
    reg = ''
    for i in pai:
        if i in special:
            reg += '\\'+i
        else:
            reg += i
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

corpus = fdic
for i in stopwords:
    stoppair = ' '.join(i)
    corpus = merge_vocab(stoppair, corpus)
corpus = Bpe(corpus)
np.save('Data/Japanesecommentbushou_with_stopwords.npy', corpus)
