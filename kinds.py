from gensim.models import word2vec
import jieba
import pandas as pd
import collections
import numpy as np

def ischaracter(text):
    if len(text) == 1:
        return all('\u4e00' <= char <= '\u9fff' for char in text)
    else:
        return False

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

kinds = collections.defaultdict(int)
# 4157
# kinds = collections.defaultdict(int)
# jieba.load_userdict('Data/chinesewordcorpus4157.txt')
# for line in lines:
#     st = ''
#     line = line.strip().split('\t')
#     for i in line[0]:
#         if i in chindex and numberofcharacter[i] <= 4157:
#             st += chbushou[chindex[i]]
#         else:
#             st += i
#     data = jieba.cut(st)
#     for j in data:
#         kinds[j] +=1

# all bushou
# for line in lines:
#     st = ''
#     line = line.strip().split('\t')
#     for i in line[0]:
#         if i in chindex:
#             st += chbushou[chindex[i]]
#         else:
#             st += i
#     for j in st:
#         kinds[j] +=1
# character
# for line in lines:
#     st = ''
#     line = line.strip().split('\t')
#     for i in line[0]:
#          st += i
#     for j in st:
#         kinds[j]+=1
# word
for line in lines:
    st = ''
    line = line.strip().split('\t')
    for i in line[0]:
         st += i
    data = jieba.cut(st)
    for j in st:
        kinds[j]+=1
# 4157charcter
# for line in lines:
#     st = ''
#     line = line.strip().split('\t')
#     for i in line[0]:
#         if i in chindex and numberofcharacter[i] <= 4157:
#             st += chbushou[chindex[i]]
#         else:
#             st += i
#     for j in st:
#         kinds[j]+=1
print(len(kinds))
print(sum(kinds.values())/len(kinds))