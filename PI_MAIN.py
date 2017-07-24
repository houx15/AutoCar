__author__ = "HOU Yuxin"
__copyright__ = "Copyright 2017 "
__license__ = "THU"
__version__ = "1"
__email__ = "houyuxin1234@sina.cn"
__status__ = "Development"

import threading
import serial
import time
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
import os
import sys
import PI_UltraDist as Ultra
import cv2
import numpy as np
import PiClient as client
from PI_UART import PiUART
import RPi.GPIO as GPIO

PIerror="errors:\n"

address=('127.0.0.1',5924)
socket_udp=socket(AF_INET, SOCK_DGRAM)
socket_udp.bind(address)
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
addr=None

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
        print ("recieved")
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

def imgThread(camera,addr):
    while True:
        img=getImage(camera)
        client.ImgSend(socket_udp,img,addr)

def dataThread():
    initGPIO()
    GPIO.setup(21,GPIO.OUT)
    GPIO.output(21, False)
    recData,addr=client.dataRec(socket_udp)
    print (recData)
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
    #    speedInfo="12,12,12,12,12"

        #速度解码
        decodeData=speedInfo.split(',',4)
        if len(decodeData)>=5:
            print(decodeData)
            iRealWheel1=int(decodeData[0])
            iRealWheel2=int(decodeData[1])
            iRealWheel3=int(decodeData[2])
            iRealWheel4=int(decodeData[3])
            iCarTheta=int(decodeData[4])
        #然后将数据按照协议打包
        
        dataToSend=client.dataPack(iDistance1,iDistance2,iDistance3,iCarTheta,bReceive,iRealWheel1,iRealWheel2,iRealWheel3,iRealWheel4)
        client.dataSend(socket_udp,dataToSend,addr)
        bReceive=0

threads=[]
t1=threading.Thread(target=imgThread,args=(camera,addr))
threads.append(t1)
t2=threading.Thread(target=dataThread,args=())
threads.append(t2)

if __name__=='__main__':
    for t in threads:
        t.setDaemon()
        t.start()