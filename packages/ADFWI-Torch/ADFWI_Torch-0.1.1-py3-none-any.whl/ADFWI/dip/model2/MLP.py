'''
* Author: LiuFeng(SJTU) : liufeng2317@sjtu.edu.cn
* Date: 2024-05-14 09:08:12
* LastEditors: LiuFeng
* LastEditTime: 2024-05-26 10:41:48
* Description: 
* Copyright (c) 2024 by liufeng, Email: liufeng2317@sjtu.edu.cn, All Rights Reserved.
'''

import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class MLP2(torch.nn.Module):
    def __init__(self,model_shape,
                 random_state_num = 100,
                 hidden_layer_number = [1000,1000],
                 v1min=None,v1max=None,
                 v2min=None,v2max=None,
                 unit1 = 1000,
                 unit2 = 1000,
                 device="cpu"):
        super(MLP2,self).__init__()
        self.v1min = v1min
        self.v1max = v1max
        self.v2min = v2min
        self.v2max = v2max
        self.device = device
        self.model_shape = model_shape
        self.in_features = random_state_num
        
        self.unit1 = unit1
        self.unit2 = unit2
        
        self.MLP_in = nn.Sequential(
            nn.Linear(in_features=self.in_features,out_features=hidden_layer_number[0],bias=False),
            nn.LeakyReLU(0.1)
        )
        self.MLP_Blocks = nn.ModuleList()
        for i in range(len(hidden_layer_number)-1):
            self.MLP_Blocks.append(
                nn.Sequential(
                    nn.Linear(in_features=hidden_layer_number[i],out_features=hidden_layer_number[i+1]),
                    nn.LeakyReLU(0.1)
                )
            )
            
        self.MLP_out = nn.Sequential(
            nn.Linear(in_features=hidden_layer_number[-1],out_features=2*model_shape[0]*model_shape[1])
        )
        
        # latent variable
        torch.manual_seed(1234)
        self.random_latent_vector = torch.rand(self.in_features).to(self.device)
        
    def forward(self):
        # neural network generation
        out = self.MLP_in(self.random_latent_vector)
        for i in range(len(self.MLP_Blocks)):
            out = self.MLP_Blocks[i](out)
        out = self.MLP_out(out).view(2,self.model_shape[0],self.model_shape[1])
        # post process
        out = torch.squeeze(out)
        out1  = out[0]
        out2  = out[1]
        if self.v1min != None and self.v1max != None:
            out1 = ((self.v1max-self.v1min)*torch.tanh(out1) + (self.v1max+self.v1min))/2
        if self.v2min != None and self.v2max != None:
            out2 = ((self.v2max-self.v2min)*torch.tanh(out2) + (self.v2max+self.v2min))/2
        out1 = torch.squeeze(out1)*self.unit1
        out2 = torch.squeeze(out2)*self.unit2
        return out1,out2