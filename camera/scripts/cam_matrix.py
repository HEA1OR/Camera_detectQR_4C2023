#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 计算图像中二维码对应相机坐标系下的坐标
import numpy as np
import cv2
import os

# 下面都是要实地测量计算
length_factor = 0.1552  # 长度因子
length_vector = -41
height_factor = 0  # 高度因子,暂时不考虑
height_vector = 33
area_init = 172  # 边长初始值
deep_offset = 0.05  # 深度因子
deep_init = 210  # 深度初始值


# 结合优秀的相机性能，可以推断二维码在短距离内在焦平面上下和左右移动时边长不变，面积不变。面积和预定距离成平方反比

def count_Offset(num, length, height):
    # 偏差
    filename = str(num) + "QR" + ".png"
    # filename = os.path.join('../img', filename)
    img = cv2.imread(filename)
    h2, w2 = img.shape[:2]

    area_offset = h2 / area_init

    # 计算距离偏差

    deep_offset = 0.00217 * h2 * h2 - 1.269  * h2 + 365.358
    deep_offset = int(deep_offset)

    # 计算平行方向和竖直方向的偏差
    filename = str(num) + ".png"
    # filename = os.path.join('../img', filename)
    img = cv2.imread(filename)
    h1, l1 = img.shape[:2]
    deltal = 0.009345 * deep_offset * deep_offset - 4.4625 * deep_offset + 567.162
    deltal = int(deltal)
    differ_l = -(length - 0.5 * l1) * length_vector / deltal
    differ_h = (height - 0.5 * h1) * (deep_offset - 110) / (deep_init - 110)
    # differ_l = length - 0.5*l1
    # differ_h = height - 0.5*h1
    # length_offset = differ_l * length_factor
    # height_offset = differ_h * height_factor
    length_offset = (differ_l - length_vector) * length_factor
    height_offset = (differ_h - height_vector) * height_factor
    deep_offset = deep_offset - 136.5 #145 136.5
    if -8 < length_offset < 8:
        length_offset = 0
    if -5 < height_offset < 5:
        height_offset = 0
    length_offset, height_offset, deep_offset = int(length_offset),  int(height_offset), int(deep_offset)
    return length_offset, height_offset, deep_offset  # 偏差依次向右为正，向上为正，向里为正
