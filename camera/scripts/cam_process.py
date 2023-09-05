#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 实现对相机拍摄原始图像的预处理，检测并保存最合适的二维码图像
# 集成为cam_process服务

import rospy
import cv2
import os
import pyzbar.pyzbar as pyzbar
from PIL import ImageDraw, ImageFont, Image as PILImage
import json
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def Image_process(num): # 综合函数，主要包括二维码区域裁剪保存，判别颜色，二维码内容识别
    closest_barcode, length, height = Image_find(num)
    
    color = Image_color(num)
    if color is 'red':
        rospy.set_param('color', 'red')
        province = "无"
    else :
        rospy.set_param('color', 'black')
        province = QR_detect(num, closest_barcode)
    set_province(province)
    print(province)
    return length, height


def Image_color(num):                                                                           
    filename = str(num) + "QR" + ".png"  # 格式化文件名
    #filename = os.path.join('../img', filename)
    img = cv2.imread(filename)
    
    # 获取图像的高度和宽度
    h, w = img.shape[:2]
    # 计算中心区域的左上角和右下角坐标
    center_x, center_y = w // 2, h // 2
    left, top = center_x - 40, center_y - 40
    right, bottom = center_x + 40, center_y + 40
    # 切片操作截取中心80x80的区域
    cut = img[top:bottom, left:right]
  
    hsv = cv2.cvtColor(cut, cv2.COLOR_BGR2HSV)

    # 定义红色和黑色的阈值
    red_lower = (0, 120, 120)
    red_upper = (10, 255, 255)
    black_lower = (0, 0, 0)
    black_upper = (180, 255, 30)

    # 创建掩膜
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    black_mask = cv2.inRange(hsv, black_lower, black_upper)

    # 计算红色像素和黑色像素的数量
    red_pixels = cv2.countNonZero(red_mask)
    black_pixels = cv2.countNonZero(black_mask)

    # 判断哪种像素较多
    if red_pixels > black_pixels:
        return 'red'
    else:
        return 'black'
    # 判断二维码的颜色



def QR_save(num, barcode): # 保存最合适的二维码图像，用于后续的红黑判断
    filename = str(num) + ".png"  # 格式化文件名
    #filename = os.path.join('../img', filename)
    img = cv2.imread(filename)
    crop_img = img[barcode.rect.top:(barcode.rect.top + barcode.rect.height), barcode.rect.left:(barcode.rect.left + barcode.rect.width)]
    
    filename = str(num) + "QR" + ".png"        # 保存标记后的图像     
    #filename = os.path.join('../img', filename)
   
    cv2.imwrite(filename, crop_img)

def select(num):
    for i in range (60):
        filename = "image" + str(i+1) + ".png"  # 格式化文件名
    #filename = os.path.join('../img', filename)
        img = cv2.imread(filename)
        gr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gr)                   
        if barcodes:
            filename = str(num) + ".png"
            cv2.imwrite(filename, img)
            print(i)
            break
        else:
            print("none")
            



# 找到最合适的二维码后识别省份，画出框并标注省份,返回值为二维码信息和位置  
def Image_find(num):
    select(num)
    filename = str(num) + ".png"  # 格式化文件名
    #filename = os.path.join('../img', filename)
    img = cv2.imread(filename)
    gr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gr)                    
    closest_barcode = None
    closest_barcode_distance = float("inf")
    # 找到距离中心最近的二维码
    for barcode in barcodes:
        if barcode.type == "QRCODE":
            barcode_center_x = barcode.rect.left + barcode.rect.width / 2
            barcode_center_y = barcode.rect.top + barcode.rect.height / 2
            image_center_x = img.shape[1] / 2
            image_center_y = img.shape[0] / 2
            distance = ((barcode_center_x - image_center_x) ** 2 + (barcode_center_y - image_center_y) ** 2) ** 0.5
            if distance < closest_barcode_distance:
                # barcode_data = barcode.data.decode("utf-8")
                closest_barcode = barcode
                closest_barcode_distance = distance

    if closest_barcode is not None:
        cv2.rectangle(img, (closest_barcode.rect.left, closest_barcode.rect.top),
                      (closest_barcode.rect.left + closest_barcode.rect.width,
                       closest_barcode.rect.top + closest_barcode.rect.height), (0, 255, 0), 2)
        
        save = QR_save(num, closest_barcode)  # 保存最合适的二维码图像，用于后续的红黑判断
   
    return closest_barcode, closest_barcode.rect.left + 0.5*closest_barcode.rect.width, closest_barcode.rect.top + 0.5*closest_barcode.rect.height
        

# 检测省份，并保存标注图像
def QR_detect(num, closest_barcode):
        # 使用json模块解析JSON字符串
    barcode_data = closest_barcode.data.decode("utf-8")
    data = json.loads(barcode_data)
        # 获取address字段
    address = data['address']
        # 去除字符串中的空格和换行符
    address = address.replace(' ', '').replace('\n', '')
        # 获取最后一个数据的前2个字符
    result = address[:2]
    return result
'''
    filename = str(num) + ".png"  # 格式化文件名
        #filename = os.path.join('../img', filename)
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = PILImage.fromarray(img)
    draw = ImageDraw.Draw(img)

        # Load the Chinese font file
    font_path = "SimHei.ttf"
    font = ImageFont.truetype(font_path, 50, encoding="utf-8")  # Change the font size as needed
    draw.text((closest_barcode.rect.left, closest_barcode.rect.top +
                                  closest_barcode.rect.height + 20), result, (0, 255, 0), font=font)
    qr_code_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    filename = str(num) + "marked" + ".png"        # 保存标记后的图像     
        #filename = os.path.join('../img', filename)
    cv2.imshow('Camera', qr_code_img)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    cv2.imwrite(filename, qr_code_img)
'''

        



def set_province(str):
    if str == "无":
        str1 = "USELESSBOX"
        rospy.set_param("Provinces",str1)
    if str == "安徽":
        str1 = "BOX1"
        rospy.set_param("Provinces",str1)
    if str == "四川":
        str1 = "BOX2"
        rospy.set_param("Provinces",str1)
    if str == "河南":
        str1 = "BOX3"
        rospy.set_param("Provinces",str1)
    if str == "江苏":
        str1 = "BOX4"
        rospy.set_param("Provinces",str1)
    if str == "湖南":
        str1 = "BOX5"
        rospy.set_param("Provinces",str1)
    if str == "浙江":
        str1 = "BOX6"
        rospy.set_param("Provinces",str1)
    if str == "福建":
        str1 = "BOX7"
        rospy.set_param("Provinces",str1)
    if str == "广东":
        str1 = "BOX8"
        rospy.set_param("Provinces",str1)
    print(rospy.get_param("Provinces"))




