import collections
import pandas as pd
from gensim.models import word2vec
import numpy as np
import jieba

model = word2vec.Word2Vec.load("Data/wordnewshalfskipgramcut.model")
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
with open("Data/evaluate_news.txt", encoding='utf-8') as f:
    lines = f.readlines()
# 4157
jieba.load_userdict('Data/chinesewordcorpus4157.txt')
count = 0
dic = collections.defaultdict(int)
for line in lines:
    st = ''
    line = line.strip().split('\t')
    for i in line[0]:
        if i in chindex and numberofcharacter[i] <= 4157:
            st += chbushou[chindex[i]]
        else:
            st += i
    data = jieba.cut(st)
    for i in data:
        if i not in dic:
            dic[i] = count
            count += 1
# 4157charcter
# for line in lines:
#     st = ''
#     line = line.strip().split('\t')
#     for i in line[0]:
#         if i in chindex and numberofcharacter[i] <= 4157:
#             st += chbushou[chindex[i]]
#         else:
#             st += i
#     data = st
#     for i in data:
#         if i not in dic:
#             dic[i] = count
#             count += 1
for i in dic:
    with open("half2indexskipgram", 'a', encoding='utf-8') as f:
        f.write(i+' '+str(dic[i])+'\n')
    with open("halfindex2tensorskipgram", 'a', encoding='utf-8') as f:
        f.write(str(dic[i])+' '+model.wv.get_vector(i))
