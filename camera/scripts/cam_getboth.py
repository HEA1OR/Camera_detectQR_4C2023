#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from camera.srv import Ronaldo, RonaldoRequest, RonaldoResponse
import cam_matrix
import cam_process
import cam_siu


def David_Tao(req):
    cam_siu.capture_image(req.data)
    length, height = cam_process.Image_process(req.data)
    result = RonaldoResponse()
    result.success = True
    result.length, result.height, result.depth = cam_matrix.count_Offset(req.data, length, height)

    # 返回响应消息
    return result

def cam_process_server():
    # 初始化 ROS 节点
    rospy.init_node('cam_process_server')

    # 创建一个名为 cam_process 的服务，服务类型为 CamProcess，回调函数为 David_Tao
    s = rospy.Service('cam_process', Ronaldo, David_Tao)

    # 打印消息，表示服务已经准备好接收请求
    rospy.loginfo("Ready to process camera data.")

    # 循环等待请求
    rospy.spin()

if __name__ == "__main__":
    
    cam_process_server()
