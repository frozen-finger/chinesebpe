import numpy as np
import pandas as pd
import math
import collections
import matplotlib.pyplot as plt

# for epoch in range(1000, 10000, 500):
# epoch = 561
corpus = np.load("Data/chinesewordcorpusallkanji.npy", allow_pickle=True)
li = []
li1 = []
dic = collections.defaultdict(int)
subword = collections.defaultdict(int)
for i in corpus.item():
    dic[i] = corpus.item()[i]
for i in dic:
    sub = i.split(' ')
    for k in sub:
        subword[k] += dic[i]

print(len(subword))
temp = ''
for i in subword:
    if len(i) > len(temp):
        temp = i
print(temp)
print(subword[temp])

# 写入excel，制表
# for i in subword:
#     li1.append([i, subword[i], len(i)])
# li1.sort(key=lambda x:x[1], reverse=True)
# # li.sort(key=lambda x:x[2], reverse=True)
# print(li1[0], li1[-1])
# df = pd.DataFrame(li1[0:20])
# df.to_excel('Data/chineseword{0}_corpusmini.xls'.format(epoch))
# print(df)

# 求平均值，方差，中位数，标准差
freq = 0
for i in subword:
    freq += subword[i]
    li.append(subword[i])
freq = freq/len(subword)
variance = 0
for i in subword:
    variance += (freq - subword[i])**2
variance = variance/len(subword)
mid = math.floor(len(subword)/2)
li.sort()
with open("Data/analyzed_chineseword_corpus", 'a', encoding='utf-8') as f:
    log = "middle:" + str(li[mid]) + '\n' + "standard deviation:" + str(math.sqrt(variance)) + '\n' + 'average:' + str(freq)
    f.write(log)

# 分布分析
# print(len(subword))
# x = []
# for i in subword:
#     x.append(freq-subword[i])
# y = [0 for i in range(len(x))]
# plt.scatter(x, y)
# plt.show()