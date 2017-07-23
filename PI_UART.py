# -*- coding: utf-8 -*
import serial
import time

#Instance to connect with Arduino
#树莓派串口默认通过SSH调用
class PiUART(object):
    def __init__(self,name="/dev/ttyAMA0",baud=9600):
        self.name=name
        self.baud=baud
    def conn(self):
        self.serial=serial.Serial(self.baud,self.baud)
    def stop(self):
        self.serial.close()
    def recv(self):
        try:
            data=self.serial.read()
            return data
        except KeyboardInterrupt:
            return "Error with UART"
    def send(self,data):
        self.serial.write(data)
'''
# 打开串口
ser = serial.Serial("/dev/ttyAMA0", 9600)
def recv(serial):
    while True:
        data=ser.read(1)
        if data=="":
            continue
        while 1:
            n=ser.inWaiting()  
            #print n
            if n>0:
                data+=ser.read(n)
                time.sleep(0.1)
            else:
                break
        return data
          

ser.open()

ser.write("testing")
try:
     while 1:
              response = ser.readline()
              print response
except KeyboardInterrupt:
     ser.close()
 
def main():
    while True:
        try:
            data=recv(ser)
            print (data)
            ser.flushInput()
            send=raw_input("input your message to Mr. Arduino:")
            ser.write(send)
            data=recv(ser)
            print (data)
        except KeyboardInterrupt:
            ser.close()
'''