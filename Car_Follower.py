import numpy as np
import cv2
import math
import time

def Follower(img):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 灰度化之后的图像
    ret, output2 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)#二值化图像
    imgSize=output2.shape
    con1=0.5#参数1，图片扭曲系数
    con2=400#参数2，线偏移系数
    iVer=0
    center[]
    while iVer<imgSize[0]:
        index=np.nonzero(output2[iVer])
        iHor=0
        cenHor=0
        if len(index[0]) is not 0:
            while (iHor+1)<len(index[0]):
                if (index[0][iHor+1]-index[0][iHor])>50:
                    cenHor=int((index[0][iHor+1]+index[0][iHor])/2)
                    break
                else:
                    iHor=iHor+1
            if cenHor==0:
                if index[0][-1]<(imgSize[1]/2):
                    #假设垂直方向的中线距离在0处为50，480处为100
                    cenHor=int(index[0][-1]+fP-fK*iVer)
                    #+(fK*iVer+50)
                else:
                    cenHor=int(index[0][0]-fP+fK*iVer)
                    #-(fK*iVer+50))  
            center.append([iVer,cenHor])
        else:
            pass
        iVer=iVer+10
    print(center)
    #之后应该基于计算得到的中心点得到相应的转弯方向

'''
cap = cv2.VideoCapture("try1.mp4")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
c=1
stream = io.BytesIO()#构建二进制流

while(True):
    # 逐帧获取图像
    ret,frame = cap.read()
    e1=cv2.getTickCount()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 灰度化之后的图像
    ret, output2 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)#二值化图像
    imgSize=output2.shape
    con1=0.5#参数1，图片扭曲系数
    con2=400#参数2，线偏移系数
    if ret:
        iVer=0
        center[]
        while iVer<imgSize[0]:
            index=np.nonzero(output2[iVer])
            iHor=0
            cenHor=0
            if len(index[0]) is not 0:
                while (iHor+1)<len(index[0]):
                    if (index[0][iHor+1]-index[0][iHor])>50:
                        cenHor=int((index[0][iHor+1]+index[0][iHor])/2)
                        break
                    else:
                        iHor=iHor+1
                if cenHor==0:
                    if index[0][-1]<(imgSize[1]/2):
                        #假设垂直方向的中线距离在0处为50，480处为100
                        cenHor=int(index[0][-1]+fP-fK*iVer)
                        #+(fK*iVer+50)
                    else:
                        cenHor=int(index[0][0]-fP+fK*iVer)
                        #-(fK*iVer+50))  
                center.append([iVer,cenHor])
            else:
                pass
            iVer=iVer+10
        print(center)
    e2=cv2.getTickCount()
    t=(e2-e1)/cv2.getTickFrequency()
    #print (t)
    c=c+1
    #print(c)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
'''
