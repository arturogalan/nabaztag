# For the EarEncoders and ScrollWheel
import math
import subprocess
import logging
import os
import sys
import threading
import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

# Define the ADC pins
EncoderPinRight=0
EncoderPinLeft=1

millisLeft = int(round(time.time() * 1000)) 
valuesLeft = 0 
millisRight = int(round(time.time() * 1000)) 
valuesRight = 0 
# def _ReadEarsEncoders(): 
#    global millisLeft, millisRight, valuesLeft, valuesRight 
#    millisLeft = int(round(time.time() * 1000)) 
#    millisRight = int(round(time.time() * 1000)) 
#    while True:
#        #print ("Starting")
#        millisLeftTemp = int(round(time.time() * 1000)) 
#        valuesLeftTemp = adc.read_adc(EncoderPinLeft, gain=GAIN) 
#        # print ("Left :", millisLeftTemp - millisLeft, valuesLeftTemp) 
#        if ((valuesLeftTemp > 2000 and valuesLeft < 2000) or (valuesLeftTemp < 2000 and valuesLeft > 2000)): 
#            if (((millisLeftTemp - millisLeft) > 140) and (valuesLeftTemp < 2000)): 
#                print ("Left UP:", millisLeftTemp - millisLeft, valuesLeftTemp) 
#            millisLeft = millisLeftTemp 
#            valuesLeft = valuesLeftTemp 
#        millisRightTemp = int(round(time.time() * 1000)) 
#        valuesRightTemp = adc.read_adc(EncoderPinRight, gain=GAIN) 
#        #print ("Right:", millisRightTemp - millisRight, valuesRightTemp) 
#        if ((valuesRightTemp > 2000 and valuesRight < 2000) or (valuesRightTemp < 2000 and valuesRight > 2000)): 
#            if (((millisRightTemp - millisRight) > 140) and (valuesRightTemp < 2000)): 
#                print ("Right UP:", millisRightTemp - millisRight, valuesRightTemp) 
#            millisRight = millisRightTemp 
#            valuesRight = valuesRightTemp
#        time.sleep(0.1)
def _ReadEarsEncoders(): 
   global millisLeft, millisRight, valuesLeft, valuesRight 
   millisLeft = int(round(time.time() * 1000)) 
   millisRight = int(round(time.time() * 1000)) 
   while True: 
       millisLeftTemp = int(round(time.time() * 1000)) 
       valuesLeftTemp = adc.read_adc(EncoderPinLeft, gain=GAIN) 
       print ("Left :", millisLeftTemp - millisLeft, valuesLeftTemp) 
       if ((valuesLeftTemp > 2000 and valuesLeft < 2000) or (valuesLeftTemp < 2000 and valuesLeft > 2000)): 
           if (((millisLeftTemp - millisLeft) > 140) and (valuesLeftTemp < 2000)): 
               print ("Left UP:", millisLeftTemp - millisLeft, valuesLeftTemp) 
           millisLeft = millisLeftTemp 
           valuesLeft = valuesLeftTemp 
       millisRightTemp = int(round(time.time() * 1000)) 
       valuesRightTemp = adc.read_adc(EncoderPinRight, gain=GAIN) 
       #print ("Right:", millisRightTemp - millisRight, valuesRightTemp) 
       if ((valuesRightTemp > 2000 and valuesRight < 2000) or (valuesRightTemp < 2000 and valuesRight > 2000)): 
           if (((millisRightTemp - millisRight) > 140) and (valuesRightTemp < 2000)): 
               print ("Right UP:", millisRightTemp - millisRight, valuesRightTemp) 
           millisRight = millisRightTemp 
           valuesRight = valuesRightTemp       
def readEarValue(encoderPin, name, milis, values):
    # millisLeft, millisRight, valuesLeft, valuesRight 
    millisRightTemp = int(round(time.time() * 1000))
    valuesRightTemp = adc.read_adc(encoderPin, gain=GAIN) 
    if ((valuesRightTemp > 2000 and values < 2000) or (valuesRightTemp < 2000 and values > 2000)): 
        if (((millisRightTemp - millisRight) > 140) and (valuesRightTemp < 2000)): 
            print (name, " UP:", millisRightTemp - millis, valuesRightTemp) 
        millis = millisRightTemp 
        values = valuesRightTemp  
def _ReadScrollWheel(): 
   global valuesScrollWheel 
   valuesScrollWheel = 0 
   while True: 
       valuesScrollWheelTemp = adc.read_adc(3, gain=GAIN) 
       if ((valuesScrollWheelTemp - 500 > valuesScrollWheel) or (valuesScrollWheelTemp + 500 < valuesScrollWheel)): 
           vol = math.floor(valuesScrollWheelTemp / 250) 
           vol = max(0, min(100, vol)) 
           valuesScrollWheel = valuesScrollWheelTemp 
        #    subprocess.call('amixer -q set Master %d%%' % vol, shell=True)
           print ("Volume wheel: ", vol)
       # avoid overflow 
       time.sleep(0.1)

def main():
    # ReadEncoders()
    # ReadScrollWheel()
    # thread_scrollWheel = threading.Thread(target=_ReadScrollWheel) 
    # thread_scrollWheel.start() 
    thread_readEars = threading.Thread(target=_ReadEarsEncoders) 
    thread_readEars.start() 

if __name__ == '__main__':
    main()