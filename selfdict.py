import jieba
import numpy as np
import math
import collections
import pandas as pd
from gensim.models import word2vec


# corpus = np.load("Data/chinesewordcorpus4157.npy", allow_pickle=True)
# dic = collections.defaultdict(int)
# subword = collections.defaultdict(int)
# for i in corpus.item():
#     dic[i] = corpus.item()[i]
# for i in dic:
#     sub = i.split(' ')
#     for k in sub:
#         subword[k] += dic[i]
# with open('Data/chinesewordcorpus4157.txt', 'a', encoding='utf-8') as f:
#     for i in subword:
#         f.write(i+' '+str(subword[i])+'\n')
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
numberofcharacter = collections.defaultdict(int)
for i in file:
    for j in i[1]:
        numberofcharacter[j] += i[2]

def ischaracter(text):
    if len(text) == 1:
        return all('\u4e00' <= char <= '\u9fff' for char in text)
    else:
        return False

with open("Data/evaluate_news.txt", encoding="utf-8") as f:
    lines = f.readlines()

# jieba.load_userdict('Data/chinesewordcorpus4157.txt')
dataset = []
for line in lines:
    st = ''
    line = line.strip().split('\t')[0]
    for i in line:
        if i in chindex and numberofcharacter[i]<=4157:
            st += chbushou[chindex[i]]
        else:
            st += i
    # st = jieba.cut(st)
    a = []
    for ch in st:
        a.append(ch)
    dataset.append(a)
# dic = {}
# count = 0
# for i in range(len(dataset)):
#     for j in range(len(dataset[i])):
#             dic[dataset[i][j]] = 1
model = word2vec.Word2Vec(sentences=dataset, min_count=1)
model.save("Data/wordnewshalfcharactercut.model")

# wl = "感觉没啥节目效果"
# st = ''
# for i in wl:
#     if i in chindex and numberofcharacter[i] <= 4157:
#         st += chbushou[chindex[i]]
#     else:
#         st += i
