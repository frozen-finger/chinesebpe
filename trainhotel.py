from dataloadforhotelclass import dataloadforhotel
from newsclassificationmodel import hotelmodel
import torch.optim as optim
from torch.utils.data import DataLoader
import torch.nn.functional as F
import torch.nn as nn
import torch as torch

def collate_fn(batch):
    charalist = [items['embeddingli'] for items in batch]
    tarlist = [items['target'] for items in batch]
    tarlist = torch.LongTensor(tarlist)
    return charalist, tarlist

with open("Data/halfindex2tensorskipgram", encoding='utf-8') as f:
    index2tensor = f.readlines()
dicindex2tensor = []
for line in index2tensor:
    line = line.strip('\n').split('\t')[1]
    line = line.split(' ')
    sen = []
    for i in line[:-1]:
        sen.append(float(i))
    dicindex2tensor.append(sen)
weight = torch.FloatTensor(dicindex2tensor)
hotelmodel = hotelmodel().cuda()
traindataset = DataLoader(dataloadforhotel(), batch_size=8, shuffle=True, drop_last=True, collate_fn=collate_fn)
embedding = nn.Embedding.from_pretrained(weight).cuda()
lr = 0.001
optimizer = optim.SGD([
                    {'params': hotelmodel.parameters(), 'lr': lr*10},
                    {'params': embedding.parameters()}], lr=lr)
# optimizer = optim.SGD(hotelmodel.parameters(), lr=0.01)

for epoch in range(100):
    sumloss = 0.0
    for data in traindataset:
        x, y = data
        y = y.cuda()
        optimizer.zero_grad()
        prelist = []
        for i in range(8):
            embed = embedding(x[i].cuda())
            pre = hotelmodel(embed.unsqueeze(0))
            prelist.append(pre)
        prelist = torch.cat(prelist, 0)
        # pre = hotelmodel(prelist)
        loss = F.cross_entropy(prelist, y)
        loss.backward()
        optimizer.step()
        sumloss += loss.item()
    with open("Data/newstrainloghalfembedding", 'a', encoding='utf-8') as f:
        f.write("epoch:{}".format(str(epoch)) + ' ' + str(sumloss) + '\n')
    print("epoch:{}, sumloss:{}".format(epoch, sumloss))
    torch.save(embedding.state_dict(), 'Data/halfembedding.pth')
    torch.save(hotelmodel.state_dict(), 'Data/newsmodelhalfembedding.pth')