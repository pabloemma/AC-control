import RPi.GPIO as GPIO
import math
import os
from datetime import datetime
from time import sleep
# This is for revision 1 of the Raspberry Pi, Model B
# This pin is also referred to as GPIO23
# cahnged by ak, put in idents and run on python3
INPUT_WIRE = 8
SHORT = 600
MEDIUM = 1500
LONG = 20000
LONGEST = 30000
GPIO.setmode(GPIO.BOARD)
GPIO.setup(INPUT_WIRE, GPIO.IN)
testbuf =''
totalbuf = ''
counter =0
while True:
    value = 1
 # Loop until we read a 0
    while value:
        value = GPIO.input(INPUT_WIRE)
# Grab the start time of the command
    startTime = datetime.now()
# Used to buffer the command pulses
    command = []
# The end of the "command" happens when we read more than
 # a certain number of 1s (1 is off for my IR receiver)
    numOnes = 0
# Used to keep track of transitions from 1 to 0
    previousVal = 0
    while True:
        if value != previousVal:
   # The value has changed, so calculate the length of this run
            now = datetime.now()
            pulseLength = now - startTime
            startTime = now
            command.append((previousVal, pulseLength.microseconds))
        if value:
            numOnes = numOnes + 1
        else:
            numOnes = 0
# 10000 is arbitrary, adjust as necessary
        if numOnes > 10000:
            break
        previousVal = value
        value = GPIO.input(INPUT_WIRE)
 
    print ("----------Start----------")
    print("Size of array is " + str(len(command)))
    print(command)
#    for (val, pulse) in command:
#        print(val, pulse)
    #testbuf =''
    for (i, val) in enumerate(command):
        # print(command)
        #print(i, '  ', val)
        if(i == len(command)-1):  #otherwise we have overflow array
            break
        val_next = command[i + 1]
        #print(val, command[i + 1])
        if val[0] == 0:
            if (val[1] < SHORT and val_next[1] < SHORT):
                #print(0)
                testbuf = testbuf+'0'
            elif (val[1] < SHORT and val_next[1] > SHORT and val_next[1] < MEDIUM):
                #print(1)s
                testbuf = testbuf+'1'
            elif (val[1] < SHORT and val_next[1] > LONG and val_next[1] < LONGEST):
                print("A")
            elif (val[1] < SHORT and val_next[1] > LONGEST):
                print("B")
            elif (val[1] > MEDIUM and val_next[1] > MEDIUM):
                print("C")
    print('counter' , counter)
    if (counter < 5):
        totalbuf = totalbuf+testbuf
        counter +=1 
    
        if (counter == 4):
            print('last buffer   ',testbuf)  
            print('total ' ,totalbuf) 
            totalbuf = ''
            testbuf = ''
            counter = 0 
    print(testbuf)
    print ("-----------End-----------\n")
    print ("Size of array is " + str(len(command)))
