# modification of https://github.com/indussky8/wide-resnet.pytorch/blob/master/networks/wide_resnet.py

import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
from torch.autograd import Variable
from torchsummary import summary

import sys
import numpy as np

# net = Wide_ResNet(16, 2, 0, 10) #(depth, widen_factor, dropout_rate, num_classes)

def conv3x3(in_planes, out_planes, stride=1):
    return nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride, padding=1, bias=False)

def conv_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        init.xavier_uniform(m.weight, gain=np.sqrt(2))
        init.constant(m.bias, 0)
    elif classname.find('BatchNorm') != -1:
        init.constant(m.weight, 1)
        init.constant(m.bias, 0)

class wide_basic(nn.Module):
    def __init__(self, in_planes, planes, dropout_rate, stride=1):
        super(wide_basic, self).__init__()
        self.bn1 = nn.BatchNorm2d(in_planes)
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.dropout = nn.Dropout(p=dropout_rate)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, planes, kernel_size=1, stride=stride, bias=False),
            )

    def forward(self, x):
        out = self.dropout(self.conv1(F.relu(self.bn1(x))))
        out = self.conv2(F.relu(self.bn2(out)))
        out += self.shortcut(x)

        return out

class Channel_Wide_ResNet(nn.Module):
    def __init__(self, input_channels, depth, widen_factor, dropout_rate, num_classes):
        super(Channel_Wide_ResNet, self).__init__()
        self.in_planes = 16

        assert ((depth-4)%6 ==0), 'Wide-resnet depth should be 6n+4'
        n = (depth-4)/6
        k = widen_factor

        print('| Wide-Resnet %dx%d' %(depth, widen_factor))
        nStages = [16, 16*widen_factor, 32*widen_factor, 64*widen_factor]

        self.conv1 = nn.Conv2d(input_channels, nStages[0], kernel_size=3, stride=1, padding=1, bias=False)
        self.layer1 = self._wide_layer(wide_basic, nStages[1], n, dropout_rate, stride=1)
        self.layer2 = self._wide_layer(wide_basic, nStages[2], n, dropout_rate, stride=2)
        self.layer3 = self._wide_layer(wide_basic, nStages[3], n, dropout_rate, stride=2)
        self.bn1 = nn.BatchNorm2d(nStages[3], momentum=0.9)
        self.linear = nn.Linear(nStages[3], num_classes)

    def _wide_layer(self, block, planes, num_blocks, dropout_rate, stride):
        #print(type(num_blocks))
        strides = [stride] + [1]*(int(num_blocks)-1)
        layers = []

        for stride in strides:
            layers.append(block(self.in_planes, planes, dropout_rate, stride))
            self.in_planes = planes

        return nn.Sequential(*layers)

    def forward(self, x):
        out = self.conv1(x)
        out = self.layer1(out)
        act1 = out
        out = self.layer2(out)
        act2 = out
        out = self.layer3(out)
        act3 = out
        out = F.relu(self.bn1(out))
        out = F.avg_pool2d(out, 8)
        out = out.view(out.size(0), -1)
        out = self.linear(out)

        return out, act1, act2, act3

if __name__ == '__main__':
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # PyTorch v0.4.0
    
    model = Wide_ResNet(depth=16, widen_factor=2, dropout_rate=0.0, num_classes=10).to(device)
    
    summary(model, input_size=(3, 32, 32))
    
        
    
    net=Wide_ResNet(16, 2, 0, 10)
    
    y = net(Variable(torch.randn(1,3,32,32)))[0]
    a1 = net(Variable(torch.randn(1,3,32,32)))[1]
    a2 = net(Variable(torch.randn(1,3,32,32)))[2]
    a3 = net(Variable(torch.randn(1,3,32,32)))[3]

    print("size of output layer: ", y.size()) #size of output layer
    print("size of activation1 layer: ", a1.size()) #size of activation1 layer
    print("size of activation2 layer: ", a2.size()) #size of activation2 layer
    print("size of activation3 layer: ", a3.size()) #size of activation3 layer
    
#net=Wide_ResNet(16, 2, 0, 10) #(depth, widen_factor, dropout_rate, num_classes)