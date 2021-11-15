import torch as torch
import torch.nn.functional as F
import torch.nn as nn
import numpy as np


class hotelmodel(nn.Module):
    def __init__(self):
        super(hotelmodel, self).__init__()
        self.rnn = nn.LSTM(input_size=100, num_layers=2, hidden_size=600, batch_first=True)
        self.w = nn.Parameter(torch.zeros(600), requires_grad=True)
        nn.init.uniform_(self.w)
        self.tanh1 = nn.Tanh()
        self.linear1 = nn.Linear(600, 300)
        self.linear2 = nn.Linear(300, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        output, (hn, cn) = self.rnn(x)
        M = self.tanh1(output)
        alpha = F.softmax(torch.matmul(M, self.w), dim=1).unsqueeze(-1)
        output = output*alpha
        output = torch.sum(output, dim=1)
        output = self.relu(output)
        output = self.linear1(output)
        output = self.relu(output)
        output = self.linear2(output)
        output = self.relu(output)
        return output