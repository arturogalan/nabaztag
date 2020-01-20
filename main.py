
import logging
import os
import sys
import threading
import time
import RPi.GPIO as GPIO
# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
# Define GPIO signals to use
StepPinLeftForward=26
StepPinLeftBackward=6
StepPinRightForward=13
StepPinRightBackward=5

# Define the ADC pins
EncoderPinRight=0
EncoderPinLeft=1
ScrollWheelPin=3
# END ADDED


def t_earLeft(StepForwardPin, StepBackwardPin, EncoderPin):
    global earLeft_millis, earLeft_run, earLeft_direction
    earLeft_run = 1
    earLeft_direction = 0
    earLeft_millis = int(round(time.time() * 1000)) - 1
        
    while earLeft_run == 1:

        if earLeft_direction == 1 and earLeft_millis >= int(round(time.time() * 1000)):
            GPIO.output(StepForwardPin, GPIO.LOW)
            GPIO.output(StepBackwardPin, GPIO.HIGH)
            
        elif earLeft_direction == -1 and earLeft_millis >= int(round(time.time() * 1000)):
            GPIO.output(StepBackwardPin, GPIO.LOW)
            GPIO.output(StepForwardPin, GPIO.HIGH)
            
        else:
            GPIO.output(StepForwardPin, GPIO.LOW)
            GPIO.output(StepBackwardPin, GPIO.LOW)
            earLeft_direction = 0

        # avoid overflow
        time.sleep(0.1)

def t_earRight(StepForwardPin, StepBackwardPin, EncoderPin):
    global earRight_millis, earRight_run, earRight_direction
    earRight_run = 1
    earRight_direction = 0
    earRight_millis = int(round(time.time() * 1000)) - 1
        
    while earRight_run == 1:

        if earRight_direction == 1 and earRight_millis > int(round(time.time() * 1000)):
            GPIO.output(StepForwardPin, GPIO.LOW)
            GPIO.output(StepBackwardPin, GPIO.HIGH)
            
        elif earRight_direction == -1 and earRight_millis > int(round(time.time() * 1000)):
            GPIO.output(StepBackwardPin, GPIO.LOW)
            GPIO.output(StepForwardPin, GPIO.HIGH)
            
        else:
            GPIO.output(StepForwardPin, GPIO.LOW)
            GPIO.output(StepBackwardPin, GPIO.LOW)
            earRight_direction = 0
    
        # avoid overflow
        time.sleep(0.1)




# Set ear-motor pins 
GPIO.setup(StepPinLeftForward, GPIO.OUT) 
GPIO.setup(StepPinLeftBackward, GPIO.OUT) 
GPIO.setup(StepPinRightForward, GPIO.OUT) 
GPIO.setup(StepPinRightBackward, GPIO.OUT) 
GPIO.output(StepPinLeftForward, GPIO.LOW) 
GPIO.output(StepPinLeftBackward, GPIO.LOW) 
GPIO.output(StepPinRightForward, GPIO.LOW) 
GPIO.output(StepPinRightBackward, GPIO.LOW) 
thread_earLeft = threading.Thread(target=t_earLeft, args=(StepPinLeftForward,StepPinLeftBackward,EncoderPinLeft)) 
thread_earRight = threading.Thread(target=t_earRight, args=(StepPinRightForward,StepPinRightBackward,EncoderPinRight)) 
thread_earLeft.start() 
thread_earRight.start()

# Move Right Ear
earRight_millis = int(round(time.time() * 1000)) + 3600
earRight_direction = 1
# Move Left Ear
earLeft_millis = earRight_millis - 97
earLeft_direction = -1
