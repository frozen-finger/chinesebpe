import torch.nn.functional as F
import torch as torch
from dataloadforhotelclass import dataloadforhotel
from newsclassificationmodel import hotelmodel
import torch.optim as optim
from torch.utils.data import DataLoader
import torch.nn as nn

def collate_fn(batch):
    charalist = [items['embeddingli'] for items in batch]
    tarlist = [items['target'] for items in batch]
    tarlist = torch.LongTensor(tarlist)
    return charalist, tarlist

hotelmodel = hotelmodel().cuda()
hotelmodel.load_state_dict(torch.load('Data/newsmodelhalfskipgramembedding.pth', map_location='cuda:0'))
hotelmodel.eval()
embedding = nn.Embedding(num_embeddings=19435, embedding_dim=100).cuda()
embedding.load_state_dict(state_dict=torch.load('Data/halfskipgramembedding.pth', map_location='cuda:0'))
testdataset = DataLoader(dataloadforhotel(), batch_size=8, drop_last=True, collate_fn=collate_fn)

with torch.no_grad():
    correct = 0
    total = 0
    for data in testdataset:
        x, y = data
        y = y.cuda()
        prelist = []
        for i in range(8):
            embed = embedding(x[i].cuda())
            pre = hotelmodel(embed.unsqueeze(0))
            prelist.append(pre)
        prelist = torch.cat(prelist, 0)
        prelist = torch.argmax(prelist, 1)
        total += prelist.size(0)
        correct += (prelist == y).sum().item()
    print("correct={}".format(correct/total))
