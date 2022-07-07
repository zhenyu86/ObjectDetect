import torch
import time
device = torch.device('cuda')
model = torch.load('./runs/train/exp/weights/best.pt')
# model = model.to(device)
print(model)

