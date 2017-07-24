__author__ = "HOU Yuxin"
__copyright__ = "Copyright 2017 "
__license__ = "THU"
__version__ = "1"
__email__ = "houyuxin1234@sina.cn"
__status__ = "Development"

import threading
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
import RPi.GPIO as GPIO

PIerror="errors:\n"

socket_udp=socket(AF_INET, SOCK_DGRAM)
uart=PiUART()
uart.conn()

camera=1
iDistance1=400
iDistance2=400
iDistance3=400
iCarTheta=0
bReceive=0
iRealWheel1=0
iRealWheel2=0
iRealWheel3=0
iRealWheel4=0
bStart=0
bPause=0
iMode=0
iSpeed1=0
iSpeed2=0
iSpeed3=0
iSpeed4=0
iLiftangle=0
iOpenangle=0


def initGPIO():
    GPIO.setwarnings(False)
    # referring to the pins by GPIO numbers
    GPIO.setmode(GPIO.BCM)

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

def setPara(recData):
    if len(recData)==9:
        bStart=recData[0]
        bPause=recData[1]
        iMode=recData[2]
        iSpeed1=recData[3]
        iSpeed2=recData[4]
        iSpeed3=recData[5]
        iSpeed4=recData[6]
        iLiftangle=recData[7]
        iOpenangle=recData[8]
        bReceive=1
    else:
        return 0

def imgThread(camera):
    img=getImage(camera)
    client.ImgSend(socket_udp,img,'127.0.0.1',5824)

def dataThread():
    initGPIO()
    GPIO.setup(21,GPIO.OUT)
    GPIO.output(21, False)
    recData=client.dataRec(socket_udp)
    setPara(recData)
    if bPause==1:
        GPIO.output(21, True)
    while bStart==1:
        if iMode==0:
            #遥控模式
            camera=0
        else:
            #巡线壁障模式
            camera=1
        
        motion=str(iSpeed1)+str(iSpeed2)+str(iSpeed3)+str(iSpeed4)+str(iLiftangle)+str(iOpenangle)
        uart.send(motion)
        speedInfo=uart.recv()


        #速度解码

        iCarTheta=IMU.iGetTheta()
        iDistance1=Ultra.measure(35,33)
        iDistance2=ultra.measure(15,13)
        iDistance3=ultra.measure(31,29)
        #然后将数据按照协议打包
        
        dataToSend=client.dataPack(iDistance1,iDistance2,iDistance3,iCarTheta,bReceive,iRealWheel1,iRealWheel2,iRealWheel3,iRealWheel4)
        client.dataSend(socket_udp,dataToSend,'127.0.0.1',5824)

threads=[]
t1=threading.Thread(target=imgThread,args=(camera))
threads.append(t1)
t2=threading.Thread(target=dataThread,args=())

if __name__=='__main__':
    while True:
        #如果掉线，自动连接到wifi
        if '192' not in os.popen('ifconfig | grep 192').read():
            PIerror=PIerror+'wifi is down, restart...\n'
            os.system('sudo /etc/init.d/networking restart')
    while True:
        for t in threads:
            t.setDaemon(True)
            t.start()
    
    #socket_udp.stop()
    #uart.stop()

        #传输给Arduino
        #接收数据iWheelW1-4 四个小轮的转速，和两个舵机的转速
        #后面将数据UART发送给arduino，再把arduino的发送回来
