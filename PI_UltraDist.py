#This package is for Ultra SOUND Detector
#in this package one can get the 
import time
import RPi.GPIO as GPIO

def initGPIO():
    GPIO.setwarnings(False)
    # referring to the pins by GPIO numbers
    GPIO.setmode(GPIO.BCM)

def measure(GPIO_TRIGGER,GPIO_ECHO):
    GPIO.output(GPIO_TRIGGER, False)
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
    GPIO.setup(GPIO_ECHO,GPIO.IN)

    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()

    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()

    elapsed = stop-start
    distance = (elapsed * 343000)/2

    return distance

