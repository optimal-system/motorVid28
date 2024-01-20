"""
motor-vid28.py
---------------
Projet GNOM / Optimal System (code par O.Moreau).
Code for Raspberry Pico using Micropython

Control of a dual stepping motor with coax shaft VID28-05
and 2 needles : Small needle on outside shaft (for background)
                Big needle on inside shaft (for foreground)
Calibration with 2 Magnetic Switch (normally Open)
"""
__version__ = 1.240111

import time
from machine import Pin
from base import Log

class motorVid28():
    
    def __init__(self,pins) : 
        self._A        = Pin(pins[0],Pin.OUT,0)
        self._BC       = Pin(pins[1],Pin.OUT,0)
        self._D        = Pin(pins[2],Pin.OUT,0)
        self.SWITCH    = Pin(pins[3],Pin.IN,Pin.PULL_UP)
        self.TIMESTEP = 20   #in millisexonds
        self.TIMEPULSE    = 2    #in ms
        self.TIMESTOP  = 1    #in sec
        self.STEPS     = 180
        self.SEQUENCE = [
                [1, 0, 1],
                [0, 0, 1],
                [0, 1, 1],
                [0, 1, 0],
                [1, 1, 0],
                [1, 0, 0],
                [0, 0, 0],
                ]
        
    def _motorcontrol(self,data):
        self._A.value (data[0])
        self._BC.value(data[1])
        self._D.value (data[2])
        time.sleep_ms(self.TIMEPULSE)        
            
    def moveOneStep(self,direction):
        for i in range(6):
            if   direction == 1 :
                self._motorcontrol(self.SEQUENCE[i])
            elif direction == 0 :
                self._motorcontrol(self.SEQUENCE[5-i])

    def moveSteps(self, direction, steps):
        for i in range(steps):
            self.moveOneStep(direction)
            time.sleep_ms(self.TIMESTEP)
        
    def calibrateNeedle(self,direction,adjust,name="") :
        self.moveSteps(direction, self.STEPS/4) # move out of reed magnet zone
        for i in range (self.STEPS) :
            nv = self.SWITCH.value()
            #Log("DEBUG Calibrating ",name,nv)
            if nv == 1 :
                self.moveSteps(direction, 1)
            else :
                Log("DEBUG Calibration OK ",name)
                time.sleep(1)
                self.moveSteps(direction, adjust)
                #Log("DEBUG Adjusting OK ",name)
                break
            
    def stop(self):
        self._motorcontrol(self.SEQUENCE[6])
        time.sleep(self.TIMESTOP)

#############

def _TestReed() :
    ReedSN = Pin(15, Pin.IN, Pin.PULL_UP) # small needle
    ReedBN = Pin(14, Pin.IN, Pin.PULL_UP) # big needle
    SN0 = ReedSN.value()
    BN0 = ReedBN.value()
    while True :
        SN = ReedSN.value()
        BN = ReedBN.value()
        Log("Reed SN {} Reed BN {}".format(SN,BN))
        time.sleep(1)
        if SN != SN0 or BN != BN0 :
            print("============")
            time.sleep(SN.TIMESTOP)

def _Demo(kind=0) :
    BFW=1 ; BBW=0 ; SFW=0 ; SBW =1
    STEPS = 180
#    SMALLNEEDLEPINS = (21,19,20,15)  # Motor pins A, BC, D and Switch pin
#    BIGNEEDLEPINS   = (17,18,16,14)
    SMALLNEEDLEPINS = (10,12,11,16)  # Motor pins A, BC, D and Switch pin
    BIGNEEDLEPINS   = (14,13,15,17)
    CALIBRATBN = 95 # To adjust the needle at position zero (optional)
    CALIBRATSN = 12
#    
    bigNeedle   = motorVid28(BIGNEEDLEPINS)
    smallNeedle = motorVid28(SMALLNEEDLEPINS) 
    bigNeedle.stop()
    smallNeedle.stop()
    if kind >= 0 :
        bigNeedle.calibrateNeedle(BFW,CALIBRATBN,"Big")
        smallNeedle.calibrateNeedle(SFW,CALIBRATSN,"Small")
        pass
    if kind == 0 or kind == 1 :
        Log("Starting movements")
        for i in range (4) :
            Log("Big Needle step :",i+1)
            bigNeedle.moveSteps(BFW, STEPS/4)
            bigNeedle.stop()
        for i in range (4) :
            Log("Small Needle step :",i+1)
            smallNeedle.moveSteps(SFW, STEPS/4)
            smallNeedle.stop()
        for i in range (4) :
            Log("Big Needle step :",i+1)
            bigNeedle.moveSteps(BBW, STEPS/4)
            bigNeedle.stop()
        for i in range (4) :
            Log("Small Needle step :",i+1)
            smallNeedle.moveSteps(SBW, STEPS/4)
            smallNeedle.stop()
    elif kind == 0 or kind == 2 :        
        Log("Both needles are moving at relatively same speed...")
        for i in range (STEPS/10) : 
            bigNeedle.moveSteps(BFW, 10)
            smallNeedle.moveSteps(SFW, 10)
        for i in range (STEPS) : 
            bigNeedle.moveSteps(BFW, 2)
            smallNeedle.moveSteps(SFW, 1)
        for i in range (STEPS) : 
            bigNeedle.moveSteps(BFW, 2)
            smallNeedle.moveSteps(SBW, 1)
    bigNeedle.stop()
    smallNeedle.stop()
    Log("End of demo")

if __name__ == '__main__': 
    Log("============ DEMO MOTOR-VID28.py =================") 
    Log("Version :", __version__)
    #_TestReed()
    _Demo(1)


