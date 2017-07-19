import curses
from time import *
from i2clibraries import i2c_itg3205, i2c_adxl345, i2c_hmc5883l

def iGetTheta():
    try:
        itg3205 = i2c_itg3205.i2c_itg3205(0)
        #adxl345 = i2c_adxl345.i2c_adxl345(0)
        #hmc5883l = i2c_hmc5883l.i2c_hmc5883l(0)
        #hmc5883l.setContinuousMode() #设置为持续更新模式
        #hmc5883l.setDeclination(9,54) #设置真北磁偏角补偿
        while True:
            #读取itg3205数据
            (itgready, dataready) = itg3205.getInterruptStatus()    
            if dataready:
                temp = itg3205.getDieTemperature()
                (x, y, z) = itg3205.getDegPerSecAxes() 
        #读取adxl345数据
        #(x, y, z) = adxl345.getAxes()
        #读取hmc5883l数据
        #(x, y, z) = hmc5883l.getAxes()
        #heading = hmc5883l.getHeadingString() #获取指向角度
        #declination = hmc5883l.getDeclinationString() #获取磁偏角补偿信息
            sleep(0.1) #暂停0.1秒
    finally:
        curses.endwin()