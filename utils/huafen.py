# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/23 11:12
@Auth ： Qinglin Zhang
@File ：huafen.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import shutil
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import random
from shutil import copyfile
def mycopyfile(srcfile,dstpath):                       # 复制函数
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(srcfile)             # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)                       # 创建路径
        shutil.copy(srcfile, dstpath + fname)          # 复制文件
        print ("copy %s -> %s"%(srcfile, dstpath + fname))
def main(files,root_img_path,root_labels_path,img_path,label_path):
    for f in files:
        img_name = f.replace('txt','jpg')
        img_src_path = root_img_path + '/' + img_name  # txt后缀转为jpg
        img_dist_path = img_path + '/'
        label_src_path = root_labels_path + '/' + f
        label_dist_path = label_path + '/'
        mycopyfile(img_src_path,img_dist_path)
        mycopyfile(label_src_path,label_dist_path)





if __name__ == '__main__':

    TRAIN_RATIO = 0.8   # 训练集比例
    root_img_path = 'D:\zql\dataset\BBox_SSDD\\voc_style\JPEGImages'  # 源数据及图片路径
    root_labels_path = 'D:\zql\dataset\BBox_SSDD\\voc_style\yolo_labels'  # 源标签路径，yolo格式的标签
    base_path = "office_SSDD"   #最后生成的划分数据集放置在哪个文件夹下
    if os.path.exists(base_path) is False:
        os.makedirs(base_path)
    img_train_path = base_path + '/images/train'
    if os.path.exists(img_train_path) is False:
        os.makedirs(img_train_path)
    img_val_path = base_path + '/images/val'
    if os.path.exists(img_val_path) is False:
        os.makedirs(img_val_path)
    lab_train_path = base_path + '/labels/train'
    if os.path.exists(lab_train_path) is False:
        os.makedirs(lab_train_path)
    lab_val_path = base_path + '/labels/val'
    if os.path.exists(lab_val_path) is False:
        os.makedirs(lab_val_path)
    files = os.listdir(root_labels_path)
    total_num = len(files)
    train_num = int(total_num * TRAIN_RATIO)
    val_num = total_num - train_num
    train_data = files[0:train_num]
    main(files[:train_num],root_img_path,root_labels_path,img_train_path,lab_train_path)
    main(files[train_num:train_num+val_num],root_img_path,root_labels_path,img_val_path,lab_val_path)

