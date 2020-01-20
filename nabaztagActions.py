
import logging
import os
import sys
import threading
from multiprocessing import Process, Value
import time
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
 # Import the ADS1x15 module.
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

GPIO.setwarnings(False)
# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
# Define GPIO signals to use
StepPinLeftForward=13
StepPinLeftBackward=5
StepPinRightForward=26
StepPinRightBackward=6

# Define the ADC pins
EncoderPinRight=0
EncoderPinLeft=1
ScrollWheelPin=3
# END ADDED

# Set ear-motor pins 
GPIO.setup(StepPinLeftForward, GPIO.OUT) 
GPIO.setup(StepPinLeftBackward, GPIO.OUT) 
GPIO.setup(StepPinRightForward, GPIO.OUT) 
GPIO.setup(StepPinRightBackward, GPIO.OUT) 
GPIO.output(StepPinLeftForward, GPIO.LOW) 
GPIO.output(StepPinLeftBackward, GPIO.LOW) 
GPIO.output(StepPinRightForward, GPIO.LOW) 
GPIO.output(StepPinRightBackward, GPIO.LOW) 

current_milli_time = lambda: int(round(time.time() * 1000))

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

def move_ear(StepForwardPin, StepBackwardPin, EncoderPin, Direction, Sec):
    end_time = datetime.now() + timedelta(seconds=Sec)
    while datetime.now() < end_time:
        if Direction == 1:
            GPIO.output(StepForwardPin, GPIO.LOW)
            GPIO.output(StepBackwardPin, GPIO.HIGH)
        if Direction == -1:
            GPIO.output(StepForwardPin, GPIO.HIGH)
            GPIO.output(StepBackwardPin, GPIO.LOW)    
    GPIO.output(StepForwardPin, GPIO.LOW)
    GPIO.output(StepBackwardPin, GPIO.LOW)

def move_ear_till_up(StepForwardPin, StepBackwardPin, EncoderPin, Direction, Sec, UpFlag):
    end_time = datetime.now() + timedelta(seconds=Sec)
    while datetime.now() < end_time and UpFlag.value == False:
        if Direction == 1:
            GPIO.output(StepForwardPin, GPIO.LOW)
            GPIO.output(StepBackwardPin, GPIO.HIGH)
        if Direction == -1:
            GPIO.output(StepForwardPin, GPIO.HIGH)
            GPIO.output(StepBackwardPin, GPIO.LOW)    
    GPIO.output(StepForwardPin, GPIO.LOW)
    GPIO.output(StepBackwardPin, GPIO.LOW)

def ReadEarsEncoders2(EncoderPinLeft, EncoderPinRight, leftUpFlag, rightUpFlag): 
    millisLeft = current_milli_time() 
    millisRight = current_milli_time() 
    valuesLeft = 0 
    valuesRight = 0 
    while leftUpFlag.value == False or rightUpFlag.value == False: 
        millisLeftTemp = current_milli_time() 
        valuesLeftTemp = adc.read_adc(EncoderPinLeft, gain=GAIN) 
        if ((valuesLeftTemp > 2000 and valuesLeft < 2000) or (valuesLeftTemp < 2000 and valuesLeft > 2000)): 
            if (((millisLeftTemp - millisLeft) > 240) and (valuesLeftTemp < 2000)): 
               print ("Left UP:", millisLeftTemp - millisLeft, valuesLeftTemp)
               leftUpFlag.value = True
            millisLeft = millisLeftTemp 
            valuesLeft = valuesLeftTemp 
        millisRightTemp = current_milli_time() 
        valuesRightTemp = adc.read_adc(EncoderPinRight, gain=GAIN)
        if ((valuesRightTemp > 2000 and valuesRight < 2000) or (valuesRightTemp < 2000 and valuesRight > 2000)): 
            if (((millisRightTemp - millisRight) > 240) and (valuesRightTemp < 2000)): 
                print ("Right UP:", millisRightTemp - millisRight, valuesRightTemp)
                rightUpFlag.value = True
            millisRight = millisRightTemp 
            valuesRight = valuesRightTemp   

def earsUp():                
    # Defining synchronized variables shared between processes        
    rightUpFlag = Value('b', False)
    leftUpFlag = Value('b', False)
    # launching ears movements until encoder reads up
    p1 = Process(target=move_ear_till_up, args=(StepPinLeftForward,StepPinLeftBackward,EncoderPinLeft,1,4.55 * 2, leftUpFlag))
    p3 = Process(target=move_ear_till_up, args=(StepPinRightForward,StepPinRightBackward,EncoderPinRight,-1,4.5 * 2, rightUpFlag))
    p2 = Process(target=ReadEarsEncoders2, args=(EncoderPinLeft, EncoderPinRight, leftUpFlag, rightUpFlag)) 
    p1.start()
    p3.start()
    p2.start()
    p2.join()
    p1.join()
    p3.join()
def earsSad():
    p1 = Process(target=move_ear, args=(StepPinLeftForward,StepPinLeftBackward,EncoderPinLeft,1,1.2))
    p3 = Process(target=move_ear, args=(StepPinRightForward,StepPinRightBackward,EncoderPinRight,-1,1.2))
    p1.start()
    p3.start()
    p1.join()
    p3.join()
def earsPayAttention():
    p1 = Process(target=move_ear, args=(StepPinLeftForward,StepPinLeftBackward,EncoderPinLeft,-1,.8))
    p3 = Process(target=move_ear, args=(StepPinRightForward,StepPinRightBackward,EncoderPinRight,1,.8))
    p1.start()
    p3.start()
    p1.join()
    p3.join()  
def earsActionDone():
    p1 = Process(target=move_ear, args=(StepPinLeftForward,StepPinLeftBackward,EncoderPinLeft,1,.8))
    p3 = Process(target=move_ear, args=(StepPinRightForward,StepPinRightBackward,EncoderPinRight,-1,.8))
    p1.start()
    p3.start()
    p1.join()
    p3.join()  
def volumeUp():
    os.system("amixer set 'Master' 100%")
def whisper(text):
    os.system("espeak -ves+whisper -g4 -a100 \"{}\"".format(text))
def sayMan(text):
    os.system("espeak -ves+m4 -s200 -g4 -p1 -a100 \"{}\"".format(text))
def sayWoman(text):
    os.system("espeak -ves+f4 -s200 -g4 -p1 -a100 \"{}\"".format(text))

