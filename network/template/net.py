import os
import torch.nn
import cv2
from torch.utils.data import DataLoader, Dataset
import numpy as np
import torch.optim as optim
from torchsummary import summary
import os
def Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__():
        self.layer0=nn.Conv2d(in_channels=3,out_channels=64,kernel_size=(5,3),stride=(1,2),padding=(1,1),dilation=(1,1))
        self.layer1=nn.MaxPool2d(kernel_size=(2,2), stride=(2,2), padding=(1,1), dilation=(1,1))
        self.layer2=nn.AvgPool2d(kernel_size=(3,3), stride=(4,4), padding=(1,1), dilation=(1,1))
        self.layer3=nn.ReLU()
        self.layer4=nn.ReLU6()
        self.layer5=nn.ELU()
        self.layer6=nn.PReLU()
        self.layer7=nn.Threshold(threshold=1, value=6)
        self.layer8=nn.Sigmoid()
        self.layer9=nn.Tanh()
        self.layer10=nn.LogSigmoid()
        self.layer12=nn.Softmax()
        self.layer14=nn.BatchNorm1d(1000)
        self.layer15=nn.Linear(512,1000)
    def forward(self, x):
        x=self.layer0(x)
        x=self.layer1(x)
        x=self.layer2(x)
        x=self.layer3(x)
        x=self.layer4(x)
        x=self.layer5(x)
        x=self.layer6(x)
        x=self.layer7(x)
        x=self.layer8(x)
        x=self.layer9(x)
        x=self.layer10(x)
        x=self.layer11(x)
        x=self.layer12(x)
        x=self.layer13(x)
        x=self.layer14(x)
        x=x.view(-1,512)(x)
        x=self.layer15(x)
        return x
