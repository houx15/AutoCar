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
def ImgByte(img):
    #for video and images
    recv_buffer = ""
    image_processed = 1

    while(1):
        if img != None:
            # Image has finished processing
            if image_processed == 1:
                image_processed = 0

                strImg = cv2.imencode( '.jpg', img )[1].tostring()
                return strImg

def ImgChunk(strImg): 
    #为了后面分包做准备
    byteString=[]
    count=0
    mystr=str()
    for imgByte in strImg:
        mystr=mystr+str(imgByte)
        count=count+1
        if count==457:
            byteString.append((mystr,count))
            mystr=str()
            count=0
    byteString.append((mystr.ljust(456,'0'),count))
    return byteString

def ImgPacket(lastPack,seqNum,bytesSent,payLoad):
    packet=struct.Struct("> B l I H 457s")
    #try:
    return packet.pack(lastPack,binascii.crc32(payLoad),seqNum,bytesSent,payLoad)
    #except Exception as ex:
    #    return None
    
def ImgSend(socket,img,host,port):
    imgByte=ImgByte(img)
    imgChunk=ImgChunk(imgByte)
    count=0
    for (byteArr,size) in imgChunk:
        lastPack=0
        byteArray=byteArr.encode(encoding='utf_8')

        if count==len(imgChunk)-1:
            lastPack=1
        socket.sendto(ImgPacket(lastPack,count,size,byteArray),(host,port))
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
def dataSend(sock,data,host,port):
        #写一个用于IMU,距离信息，小车速度
        sock.sendto(data,(host,port))
def dataRec(sock,bufferSize):
        # for recieving data from pc
        data=sock.recv(bufferSize)
        return data
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