# Raspberry Pi 3 Traffic Light Back End (io) Program
# Should run this program beofre Front End (server) Program 
# Control + C to end
# please notice the GPIO pins are not cleaned up
# version 5a: start in Power Down mode
# version 6a: add self-check at start

import RPi.GPIO as GPIO
import time

#config GPIO
GPIO.setmode(GPIO.BCM)
#disable the warnings that multiple scrips using the same GPIO pins. Owner takes liability
GPIO.setwarnings(False)

#config Traffice Light channel; reference Raspberry Pi pin map
#these pins connect to relays
mainG = 13
mainY = 19
mainR = 26
auxG = 21
auxY = 20
auxR = 16
chanList = [mainG,mainY,mainR,auxG,auxY,auxR]

#++ mechanical relay, low is active and high is idle
#config sequence
seq1 = [0,1,1,1,1,0]
seq2 = [1,0,1,1,1,0]
seq3 = [1,1,0,1,1,0]
seq4 = [1,1,0,0,1,1]
seq5 = [1,1,0,1,0,1]
seq6 = [1,1,0,1,1,0]
seq = [[seq1,seq2,seq3],[seq4,seq5,seq6]]
#initialize GPIO chanel
GPIO.setup(chanList, GPIO.OUT)

#status GPIO; must be consistent with server program
oReq=12
iAuto=17
iMan1=27
iMan2=22
iStdby=23

#must put the setup the same as Front End of program
GPIO.setup([iAuto,iMan1,iMan2,iStdby,oReq], GPIO.OUT)
#initialize; version io5a.py: start from request and Power Down mode
GPIO.output([iAuto,iMan1,iMan2,iStdby,oReq], [0,0,0,1,1])

#function check and initialize chanels to off state
GPIO.output(chanList,[0,1,1,0,1,1])
time.sleep(0.5)
GPIO.output(chanList,[1,0,1,1,0,1])
time.sleep(0.5)
GPIO.output(chanList,[1,1,0,1,1,0])
time.sleep(0.5)
GPIO.output(chanList,1)
print('initialization..')

while True:
    #Auto
    while GPIO.input(iAuto)==1:
        #notify in auto mode; clear request
        if GPIO.input(oReq)==1:
            GPIO.output(oReq,0)
            print('Auto')
        for iseq in seq:
            #for Green light
            GPIO.output(chanList, iseq[0])
            endTime = time.time() + 5
            while time.time() < endTime:
                time.sleep(0.5)
                #if new mode requested, break from while timing loop
                if GPIO.input(iAuto)==0:
                    break
            #for Yellow light
            GPIO.output(chanList, iseq[1])
            time.sleep(2)
            #for Red light
            GPIO.output(chanList, iseq[2])
            time.sleep(0.8)
            
            #if new mode requested, break from for sequence loop
            if GPIO.input(iAuto)==0:
                break

    #Man1
    while GPIO.input(iMan1)==1:    
        #notify in Stop Sign mode; clear request
        if GPIO.input(oReq)==1:
            GPIO.output(oReq,0)
            print('Manual 1')
        GPIO.output(chanList, seq1)
        while GPIO.input(iMan1)==1:
            time.sleep(0.8)
        #for Yellow light
        GPIO.output(chanList, seq2)
        time.sleep(2)
        #for Red light
        GPIO.output(chanList, seq3)
        time.sleep(0.8)
        
    #Man2
    while GPIO.input(iMan2)==1:    
        #notify in Stop Sign mode; clear request
        if GPIO.input(oReq)==1:
            GPIO.output(oReq,0)
            print('Manual 2')
        GPIO.output(chanList, seq4)
        while GPIO.input(iMan2)==1:
            time.sleep(0.8)
        #for Yellow light
        GPIO.output(chanList, seq5)
        time.sleep(2)
        #for Red light
        GPIO.output(chanList, seq6)
        time.sleep(0.8)
        
    #Standby
    while GPIO.input(iStdby)==1:    
        #notify in Power Down mode; clear request
        if GPIO.input(oReq)==1:
            GPIO.output(oReq,0)
            print('Standby')
        GPIO.output(chanList,1)
        while GPIO.input(iStdby)==1:
            time.sleep(0.8)

    #give system 0.5sec to do something else
    time.sleep(0.5)

#Just put below script here. User Control+C to break the program
print('Shut down. Release GPIO ports..')
GPIO.cleanup()
