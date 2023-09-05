#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 作用为调用摄像头拍摄原始图像，并保存为png格式，保存地址为img文件夹下，文件名为数字编号
import os
import rospy
import cv2
import time 
def capture_image(req):
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    # 检查摄像头是否打开成功
    if not cap.isOpened():
        print("Error opening camera.")
        exit()
   # time.sleep(0.5)# 等待摄像头稳定
    # 捕获图像
    fps = 30
    start_time = time.time()
    # 循环拍摄图片
    for i in range(10):
        # 读取一帧图像
        ret, frame = cap.read()
        # 保存图像
        file_name = 'image{}.png'.format(i + 1)
        cv2.imwrite(file_name, frame)
        # 等待下一帧图像
        time_elapsed = time.time() - start_time
        time_to_wait = 1 / fps - time_elapsed
        if time_to_wait > 0:
            time.sleep(time_to_wait)

    #img_yuv = cv2.cvtColor(frame, 36)

    # 对Y通道进行直方图均衡化
    #img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])

    # 将图像转换回RGB颜色空间
    #img_output = cv2.cvtColor(img_yuv, 38)
   
    #filename = str(req) + ".png"
    #filename = os.path.join('../img', filename)

    #cv2.imwrite(filename, frame)
    cap.release()
    print("success")

