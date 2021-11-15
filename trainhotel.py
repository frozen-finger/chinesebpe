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

weight = [[]]
hotelmodel = hotelmodel().cuda()
traindataset = DataLoader(dataloadforhotel(), batch_size=8, shuffle=True, drop_last=True, collate_fn=collate_fn)
embedding = nn.Embedding.from_pretrained(weight)
optimizer = optim.SGD(hotelmodel.parameters(), lr=0.01)

for epoch in range(100):
    sumloss = 0.0
    for data in traindataset:
        x, y = data
        y = y.cuda()
        optimizer.zero_grad()
        prelist = []
        for i in range(8):
            pre = hotelmodel(x[i].cuda().unsqueeze(0))
            prelist.append(pre)
        prelist = torch.cat(prelist, 0)
        # pre = hotelmodel(prelist)
        loss = F.cross_entropy(prelist, y)
        loss.backward()
        optimizer.step()
        sumloss += loss.item()
    with open("Data/newstrainloghalfcharacter", 'a', encoding='utf-8') as f:
        f.write("epoch:{}".format(str(epoch)) + ' ' + str(sumloss) + '\n')
    print("epoch:{}, sumloss:{}".format(epoch, sumloss))

    torch.save(hotelmodel.state_dict(), 'Data/newsmodelhalfcharacter.pth')