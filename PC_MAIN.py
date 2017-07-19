__author__ = "HOU Yuxin"
__copyright__ = "Copyright 2017 "
__license__ = "THU"
__version__ = "1"
__email__ = "houyuxin1234@sina.cn"
__status__ = "Development"

import Car_Follower as carF
from Car import Car

car=Car()

'''
作为server接收一波数据
收集到的IMU角度设置为车的car.setCarTheta
收集到的距离信息存为距离信息
收集到的图片显示，并且作为窗口
收集到的错误信息显示
'''

def fPotDirection(dst1,dst2,dst3):
    pot2=-3#degree of caculus
    pot1=0.005#coefficient of attractive potential
    pot3=5#衡量吸引势场的下降梯度
    fCarDirection=car.fGetCarTheta()
    fDerRep=-pot1(dst3^pot2-dst2^pot2)
    fDerY=fDerRep+pot3
    fDerX=fDerRep-pot3*math.tan(fCarDirection)
    fCommandDirection=math.atan2(fDerX,fDerY)
    return fCommandDirection

#通过界面设置了模式iMode
#还有是否正在行驶之中的代码

while bStart==1:
    if iMode==0:
        #调用遥控速度
        #并且数据下发
    elif iMode==1:
        #巡线部分
        #接收图片，图片为什么名字下面就用什么
        fCommandDirection=carF.Follower(img)
    elif iMode==2:
        #避障部分
        #先从socket获得了障碍物距离、IMU方向信息
        fCommandDirection=fPotDirection()
    else:
        continue
    car.carGo()#要输入的参数前面的函数还不能算出来
    car.iSpeedDecode()#1-4的速度解码
        #然后将数据下发