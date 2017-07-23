__author__ = "HOU Yuxin"
__copyright__ = "Copyright 2017 "
__license__ = "THU"
__version__ = "1"
__email__ = "houyuxin1234@sina.cn"
__status__ = "Development"

import serial
import time
import socket
import os
import sys
import PI_IMU as IMU
import PI_UltraDist as Ultra
import cv2
import numpy as np
import PiClient as client
from PI_UART import PiUART

PIerror="errors:\n"

'''
SERVER_IP =IP
SERVER_PORT = PORT
server_addr=(SERVER_IP,SERVER_PORT)
socket_tcp= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def imageForTCP(frame):
    result, imgencode = cv2.imencode('.jpg', frame,[int(cv2.IMWRITE_JPEG_QUALITY),90])
    data = numpy.array(imgencode)
    stringData = data.tostring()
    return stringData
'''
def getImage(camera):
    cap=cv2.VideoCapture(camera)#后置摄像头编号
    #降低分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
    ret,frame=cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray
    #stringImage=imageForTCP(frame)
    #socket_tcp .send(str(len(stringImage)).ljust(16))
    #socket_tcp .send(stringImage)

socket_udp=socket(AF_INET, SOCK_DGRAM)
uart=PiUART()
uart.conn()
while True:
    #如果掉线，自动连接到wifi
    if '192' not in os.popen('ifconfig | grep 192').read():
        PIerror=PIerror+'wifi is down, restart...\n'
        os.system('sudo /etc/init.d/networking restart')
    '''
    #连接到socket server
    while True:
        try:
            socket_tcp.connect(server_addr)
            break
        except Exception:
            PIerror=PIerror+"Can't connect to server, try it later!\n"
            time.sleep(1)
            continue
    '''
    '''
    这里应该是从socket接收数据的阶段
    收到数据：
    模式iMode=0，遥控；1，巡线；2，避障
    bStart=1 启动，0 停止
    bContinue=1 继续，0 暂停
    '''
    startData=client.dataRec(socket_udp,1024)
    bStart=startData[0:7]
    iMode=startData[8:9]

    while bStart==1:
        if iMode==0:
            #遥控模式
            img=getImage(0)
            client.ImgSend(socket_udp,img,'127.0.0.1',5824)
            motion=client.dataRec(socket_udp,1024)#这个，是不是就在这里等着？
            
        elif iMode==1:
            #巡线模式
            img=getImage(1)
            client.ImgSend(socket_udp,img,'127.0.0.1',5824)
            motion=client.dataRec(socket_udp,1024)
            
        elif iMode==2:
            #避障模式
            thetaInfo=IMU.iGetTheta()
            Ultra.initGPIO()
            iDistance1=Ultra.measure(3,21)
            iDistance2=ultra.measure(5,19)
            iDistance3=ultra.measure(7,23)
            #然后将数据按照协议打包
            obstacleData=str(thetaInfo)+str(iDistance1)+str(iDistance2)+str(iDistance3)
            client.dataSend(socket_udp,obstacleData,'127.0.0.1',5824)
            motion=client.dataRec(socket_udp,1024)
        else:
            PIerror=PIerror+"Wrong mode is defined./n"
        
        #从motion中获得运动信息
        if motion is not None:
            uart.send(motion)
        else:
            PIerror=PIerror+"No motion info./n"
        realSpeed=uart.recv()
        socket_udp.dataSend(socket_udp,realSpeed,'127.0.0.1',5824)
    #socket_udp.stop()
    #uart.stop()

        #传输给Arduino
        #接收数据iWheelW1-4 四个小轮的转速，和两个舵机的转速
        #后面将数据UART发送给arduino，再把arduino的发送回来
