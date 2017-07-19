#This is the class for the car
#Relevant with the speed. position. direction of the car
#Also with the speed decoding function

class Car():
    #Initializing
    iMaxWheelW=100  #°/s
    iMinWheelW=-100 #°/s
    fMaxCarV=100 #mm/s
    fMinCarV=0 #mm/s
    fMaxCarW=100 #rad/s
    fMinCarW=0 #rad/s
    def __init__(self,fV=0,fW=0,fTheta=0,size=[200,270]):
        self.fCarV=fV  #initialize the velocity,速度指的是竖直方向的速度，初始化小车的速度
        self.fCarW=fW  #the angular speed,omega,初始化小车的角速度
        self.fCarTheta=fTheta  #initialize the direction,初始化小车的方向角
        self.carSize=size  #initialize the size,小车的尺寸
    #input pins
    def fSetCarV(self,fV):  #设置小车的速度
        if(fV>=fMaxCarV):
            self.fCarV=fMaxCarV
        elif(fV<=fMinCarV):
            self.fCarV=fMinCarV
        else:
            self.fCarV=fV  
    def fSetCarW(self,fW):  #设置小车的角速度
        if(fW>=fMaxCarW):
            self.fCarW=fMaxCarW
        elif(fW<=fMinCarW):
            self.fCarW=fMinCarW
        else:
            self.fCarW=fW
    def fSetCarTheta(self,fTheta): #设置小车的方位角度
        self.fCarTheta=fTheta  
    def setCarSize(self,iCarLength,iCarWidth):  #设置小车的尺寸
        self.carSize=[iCarWidth,iCarLength]
    #output pins
    def fGetCarV(self):
        return self.fCarV
    def fGetCarW(self):
        return self.fCarW
    def fGetCarTheta(self):
        return self.fCarTheta
    def getCarSize(self):
        return self.carSize
    #get a turning angle from the road planning system
    #transformed to the angular speed and velocity of the car first
    #used for speed decoding,set the W and V
    def carGo(self,fTurnTheta):
        k=0.1
        p=0.2
        fSpeed=self.fGetCarV()-k*fTurnTheta
        self.fSetCarV(self,fSpeed)
        fOmega=self.fGetCarW()+p*fTurnTheta
        self.fSetCarW(self,fOmega)
        
    #speed decoding
    def iSpeedDecode(self,wheelP=[-70,75],wRadius=30):
        fWheelV=self.fCarV-wheelP(2)*self.fCarW
        iWheelW=180*int(fWheelV/wRadius)
        if (iWheelW>=iMaxWheelW):
            iWheelW=iMaxWheelW
        elif (iWheelW<=iMinWheelW):
            iWheelW=iMinWheelW
        else:
            pass
        return iWheelW
    

