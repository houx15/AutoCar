import numpy as np
import cv2
import socket
import sys
import time
import struct
import binascii

'''
# Instance to make connection to server
def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.client_socket.connect((self.host, self.port))
'''
def ImgByte(img):#此处将图片通过opencv内置函数转化成为byte格式
    #for video and images
    recv_buffer = ""#缓冲，可以不要
    image_processed = 1#记录图片是不是已经被处理了

    while(1):
        if img != None:#如果有图片
            # Image has finished processing
            if image_processed == 1:#如果图片还没有被处理
                image_processed = 0#标志图片已经被处理

                strImg = cv2.imencode( '.jpg', img )[1].tostring()#将图片编码为byte格式
                return strImg

def ImgChunk(strImg): #将图片按照一定字节组块
    #为了后面分包做准备
    byteString=[]#构建一个list
    count=0#计数器，记录读取 的字节数
    mystr=str()#构建一个字符串
    for imgByte in strImg:#逐个读取  strImg中的字节
        mystr=mystr+str(imgByte)#将读取到的加入到myStr中
        count=count+1#每读取一个，计数器加1
        if count==1024:#当计数到457
            byteString.append((mystr,count))#在byteString这个列表中加一个（内容，字节数）的数据
            mystr=str()#将mystr清空
            count=0#计数器清零
    byteString.append((mystr.ljust(1023,'0'),count))#将byteString填充到457个字节（有可能图片没有那么多个字节的，所以使用0填充）
    return byteString

def ImgPacket(lastPack,seqNum,bytesSent,payLoad):#将图片打包
    packet=struct.Struct("< I I 1024s")#定义这个结构体的名字，没啥用，用来看
    #try:
    return packet.pack(lastPack,seqNum,bytesSent)#将传入的几个数据打包（数据合成）然后上传
    #except Exception as ex:
    #    return None
    
def ImgSend(socket,img,addr):
    imgByte=ImgByte(img)
    imgChunk=ImgChunk(imgByte)
    count=0
    for (byteArr,size) in imgChunk:
        lastPack=0
        byteArray=byteArr.encode(encoding='utf_8')

        if count==len(imgChunk)-1:
            lastPack=1
        socket.sendto(ImgPacket(lastPack,count,byteArray),addr)
        count=count+1
                    #buf+="ACK"
                    #self.client_socket.send(buf)
'''
                # Check buffer
                recv_buffer = self.client_socket.recv(1024)
                delim = recv_buffer.strip()[-3:]
                if delim == "ACK":
                    response = recv_buffer.replace('ACK','')
                    image_processed = 1
                    recv_buffer = ""
                    return response
'''                
def dataPack(iDistance1,iDistance2,iDistance3,iCarTheta,bReceive,iRealWheel1,iRealWheel2,iRealWheel3,iRealWheel4):
    packet=struct.Struct("IIII?IIII")
    return packet.pack(iDistance1,iDistance2,iDistance3,iCarTheta,bReceive,iRealWheel1,iRealWheel2,iRealWheel3,iRealWheel4)
def dataSend(sock,dataPack,addr):
    #写一个用于IMU,距离信息，小车速度
    sock.sendto(data,addr)
def dataRec(sock,fmt='IIIIIIIII'):
    # for recieving data from pc
    data,addr=sock.recvfrom(1024)
    return struct.unpack(fmt,data),addr


'''
    # This thread runs and checks for flags
    def flag_thread(self):
        while(1):
            time.sleep(0.5)
            running = self.ns.flags[self.port]['running']
            if running == 0:
                print 'Stopping at ' + str(self.port)
                self.s.close()
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((self.host, self.port))
                break

    
    # Launches all new connections to this process and executes function on that image
    def thread_process(self, conn):

        data = ""

        #infinite loop so that function do not terminate and thread do not end.
        while True:
             
            #Receiving from client
            data += conn.recv(1024)
            reply = '.'
            if not data: 
                break
         
            conn.sendall(reply)
            
            if data.strip()[-3:] == "ACK":
                print "RECEIVED FULL"
                data = data.strip()[:-3]
                nparr = np.fromstring(data, np.uint8)
                img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)

                response = self.func(self.ns.flags[self.port], img)

                data = ""
                conn.sendall(response+"ACK")
         
        #came out of loop
        conn.close()
'''