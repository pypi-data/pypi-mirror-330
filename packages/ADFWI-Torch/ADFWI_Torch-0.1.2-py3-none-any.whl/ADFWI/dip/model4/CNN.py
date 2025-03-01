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

############################################################################
#                   CNN model implement by Weiqiang Zhu
# Zhu, W., Xu, K., Darve, E. & Beroza, G.C., 2021. 
#   A general approach to seismic inversion with automatic differentiation. 
#   Computers & Geosciences, 151, 104751. 
#   doi:10.1016/j.cageo.2021.104751
# Zhu, W., Xu, K., Darve, E., Biondi, B. & Beroza, G.C., 2022. 
#   Integrating deep neural networks with full-waveform inversion: Reparameterization, regularization, and uncertainty quantification. 
#   GEOPHYSICS, 87, R93–R109. 
#   doi:10.1190/geo2020-0933.1  
############################################################################
# model
class CNN4(torch.nn.Module):
    def __init__(self,model_shape,
                 in_channels  = [8,32,16],
                 v1min=None,v1max=None,
                 v2min=None,v2max=None,
                 v3min=None,v3max=None,
                 v4min=None,v4max=None,
                 dropout_prob=0,
                 random_state_num = 100,
                 unit1 = 1000,
                 unit2 = 1000,
                 unit3 = 1,
                 unit4 = 1,
                 device="cpu"):
        """
            model_shape (tuple) : the shape of velocity model
            in_channels (list)  : the input and output channels for each CNN block
            vmin (float)        : the minimum velocity of output
            vmax (float)        : the maximum velocity of output
            dropout_prob (float): dropout的概率
            device (optional)   : cpu or cuda
        """
        super(CNN4,self).__init__()
        self.v1min = v1min
        self.v1max = v1max
        self.v2min = v2min
        self.v2max = v2max
        self.v3min = v3min
        self.v3max = v3max
        self.v4min = v4min
        self.v4max = v4max
        self.unit1 = unit1
        self.unit2 = unit2
        self.unit3 = unit3
        self.unit4 = unit4
        self.device = device
        
        # model setting
        self.layer_num = layer_num = len(in_channels)-1
        h_in        = math.ceil(model_shape[0]/(2**layer_num))
        w_in        = math.ceil(model_shape[1]/(2**layer_num))
        self.h_v0   = model_shape[0]
        self.w_v0   = model_shape[1]
        
        # neural network blocks
        self.in_features = random_state_num
        
        self.FNN_in = nn.Sequential(
            nn.Linear(in_features=self.in_features,out_features=h_in*w_in*in_channels[0],bias=False),
            nn.Unflatten(0,(-1,in_channels[0],h_in,w_in)),
            nn.LeakyReLU(0.1)
        )
        
        self.CNN_Blocks = nn.ModuleList()
        for i in range(layer_num):
            self.CNN_Blocks.append(
                nn.Sequential(
                    nn.UpsamplingBilinear2d(scale_factor=(2,2)),
                    nn.Conv2d(in_channels = in_channels[i],out_channels=in_channels[i+1],kernel_size=4,stride=1,padding="same",bias=False),
                    nn.LeakyReLU(0.1),
                    nn.Dropout(p=dropout_prob)  # add dropout layer
                )
            )
        
        self.CNN_out = nn.Sequential(
            nn.Conv2d(in_channels = in_channels[-1],out_channels=4,kernel_size=4,stride=1,padding="same",bias=False)
        )
        
        # latent variable
        torch.manual_seed(1234)
        self.random_latent_vector = torch.rand(self.in_features).to(self.device)
    
    def forward(self):
        # neural network generation
        out = self.FNN_in(self.random_latent_vector)
        for i in range(self.layer_num):
            out = self.CNN_Blocks[i](out)
        out = self.CNN_out(out)
        
        # post process
        out = torch.squeeze(out)
        out1  = out[0]
        out2  = out[1]
        out3  = out[2]
        out4  = out[3]
        if self.v1min != None and self.v1max != None:
            out1 = ((self.v1max-self.v1min)*torch.tanh(out1) + (self.v1max+self.v1min))/2
        if self.v2min != None and self.v2max != None:
            out2 = ((self.v2max-self.v2min)*torch.tanh(out2) + (self.v2max+self.v2min))/2
        if self.v3min != None and self.v3max != None:
            out3 = ((self.v3max-self.v3min)*torch.tanh(out3) + (self.v3max+self.v3min))/2
        if self.v4min != None and self.v4max != None:
            out4 = ((self.v4max-self.v4min)*torch.tanh(out4) + (self.v4max+self.v4min))/2
        out1 = torch.squeeze(out1)*self.unit1
        out2 = torch.squeeze(out2)*self.unit2
        out3 = torch.squeeze(out3)*self.unit3
        out4 = torch.squeeze(out4)*self.unit4
        
        h_v,w_v = out1.shape
        h_v0,w_v0 = self.h_v0,self.w_v0
        out1 = out1[(h_v-h_v0)//2:(h_v-h_v0)//2+h_v0,
                    (w_v-w_v0)//2:(w_v-w_v0)//2+w_v0]
        out2 = out2[(h_v-h_v0)//2:(h_v-h_v0)//2+h_v0,
                    (w_v-w_v0)//2:(w_v-w_v0)//2+w_v0]
        out3 = out3[(h_v-h_v0)//2:(h_v-h_v0)//2+h_v0,
                    (w_v-w_v0)//2:(w_v-w_v0)//2+w_v0]
        out4 = out4[(h_v-h_v0)//2:(h_v-h_v0)//2+h_v0,
                    (w_v-w_v0)//2:(w_v-w_v0)//2+w_v0]
        return out1,out2,out3,out4