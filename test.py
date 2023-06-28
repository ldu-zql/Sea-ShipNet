# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/23 16:36
@Auth ： Qinglin Zhang
@File ：test.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import cv2
import torch
import cv2 as cv
xi = torch.ones((20,20,3)).numpy()
img = cv2.resize(xi,(50,50),interpolation=cv2.INTER_LINEAR)
print(xi)