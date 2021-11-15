from torch.utils.data import Dataset
import torch as torch
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

class dataloadforhotel(Dataset):
    def __init__(self):
        super(dataloadforhotel, self).__init__()
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
        self.target = []
        self.sentence = []
        self.h2i = {}
        with open("Data/half2indexskipgram", encoding='utf-8') as f:
            half2index = f.readlines()
        for line in half2index:
            line = line.strip('\n').split('\t')
            self.h2i[line[0]] = line[1]
        self.model = word2vec.Word2Vec.load("Data/wordnewshalfskipgramcut.model")
        # 4157
        jieba.load_userdict('Data/chinesewordcorpus4157.txt')
        for line in lines[8000:]:
            st = ''
            line = line.strip().split('\t')
            for i in line[0]:
                if i in chindex and numberofcharacter[i] <= 4157:
                    st += chbushou[chindex[i]]
                else:
                    st += i
            self.target.append(int(line[1]))
            self.sentence.append(st)
        # all bushou
        # for line in lines[8000:]:
        #     st = ''
        #     line = line.strip().split('\t')
        #     for i in line[0]:
        #         if i in chindex:
        #             st += chbushou[chindex[i]]
        #         else:
        #             st += i
        #     self.target.append(int(line[1]))
        #     self.sentence.append(st)
        # character
        # for line in lines[8000:]:
        #     st = ''
        #     line = line.strip().split('\t')
        #     for i in line[0]:
        #          st += i
        #     self.target.append(int(line[1]))
        #     self.sentence.append(st)
        # word
        # for line in lines[8000:]:
        #     st = ''
        #     line = line.strip().split('\t')
        #     for i in line[0]:
        #          st += i
        #     self.target.append(int(line[1]))
        #     self.sentence.append(st)
        # 4157charcter
        # for line in lines[8000:]:
        #     st = ''
        #     line = line.strip().split('\t')
        #     for i in line[0]:
        #         if i in chindex and numberofcharacter[i] <= 4157:
        #             st += chbushou[chindex[i]]
        #         else:
        #             st += i
        #     self.target.append(int(line[1]))
        #     self.sentence.append(st)

    def __getitem__(self, item):
        tar = self.target[item]
        data = self.sentence[item]
        data = jieba.cut(data)
        embedding = []
        # for i in data:
        #     embedding.append(self.model.wv.get_vector(i))
        # embedding = torch.FloatTensor(embedding)
        #nn.embedding
        for i in data:
            embedding.append(int(self.h2i[i]))
        embedding = torch.LongTensor(embedding)
        return {'embeddingli':embedding, 'target':tar}

    def __len__(self):
        return len(self.target)

if __name__ == '__main__':
    test = dataloadforhotel()
    print(test.__getitem__(1102))