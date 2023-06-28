# -- coding: utf-8 --
import os
import shutil
from pathlib import Path
import numpy as np
import cv2
from tqdm import tqdm

# 修改输入图片文件夹
img_folder = "D:\zql\dataset\office_SSDD\images/val"
img_list = os.listdir(img_folder)
img_list.sort()
# 修改输入标签文件夹
label_folder = "D:\zql\dataset\office_SSDD\labels/val"
label_list = os.listdir(label_folder)
label_list.sort()
# 输出图片文件夹位置
output_folder = 'gt'

labels = ['0']  # 这里修改为自己的类别

# 色盘，可根据类别添加新颜色，注意第一个别动，这是字体的颜色也就是白色，往后面推
colormap = [(0, 255, 0)]   # 不是RGB,是BGR


# 坐标转换
def xywh2xyxy(x, w1, h1, img):
    label, x, y, w, h = x

    label = int(label)
    label_ind = label

    # 边界框反归一化
    x_t = x * w1
    y_t = y * h1
    w_t = w * w1
    h_t = h * h1

    # 计算坐标
    top_left_x = x_t - w_t / 2
    top_left_y = y_t - h_t / 2
    bottom_right_x = x_t + w_t / 2
    bottom_right_y = y_t + h_t / 2

    p1, p2 = (int(top_left_x), int(top_left_y)), (int(bottom_right_x), int(bottom_right_y))
    # 绘制矩形框
    cv2.rectangle(img, p1, p2, (0,255,0), thickness=1, lineType=cv2.LINE_AA)
    label = labels[label_ind]
    label=None
    if label:
        w, h = cv2.getTextSize(label, 0, fontScale=2 / 3, thickness=2)[0]  # text width, height
        outside = p1[1] - h - 3 >= 0  # label fits outside box
        p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
        # 绘制矩形框填充
        cv2.rectangle(img, p1, p2, colormap[label_ind+1], -1, cv2.LINE_AA)
        # 绘制标签
        cv2.putText(img, label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2), 0, 2 / 3, colormap[0],
                    thickness=1, lineType=cv2.LINE_AA)
    return img


if __name__ == '__main__':
    # 创建输出文件夹
    if Path(output_folder).exists():
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)
    # labels和images可能存在不相等的情况，需要额外判断对应关系
    img_index = 0
    label_index = 0
    for _ in tqdm(range(len(label_list))):
        image_path = img_folder + "/" + img_list[img_index]
        label_path = label_folder + "/" + label_list[label_index]
        if img_list[img_index][:-4] != label_list[label_index][:-4]:
            img_index += 1
            continue
        # 读取图像文件
        img = cv2.imread(str(image_path))
        h, w = img.shape[:2]
        # 读取 labels
        with open(label_path, 'r') as f:
            lb = np.array([x.split() for x in f.read().strip().splitlines()], dtype=np.float32)
        # 绘制每一个目标
        for x in lb:
            # 反归一化并得到左上和右下坐标，画出矩形框
            img = xywh2xyxy(x, w, h, img)
        cv2.imwrite(output_folder + '/' + '{}.png'.format(image_path.split('/')[-1][:-4]), img)
        img_index += 1
        label_index += 1

