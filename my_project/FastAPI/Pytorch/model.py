import torch
import torch.nn as nn

class LogicGateModel(nn.Module):
    def __init__(self, input_dim):
        super(LogicGateModel, self).__init__()
        self.linear1 = nn.Linear(input_dim, 4)
        self.linear2 = nn.Linear(4, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = torch.relu(self.linear1(x))
        x = self.sigmoid(self.linear2(x))
        return x

def create_model(input_dim):
    return LogicGateModel(input_dim)

# 모델 생성
xor_model = create_model(2)
and_model = create_model(2)
not_model = create_model(1)