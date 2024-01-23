"""
motorvid28-test.py - Optimal System (O.Moreau)
=====================================
Code for Raspberry Pico using Micropython

Several tests (or demos) for the program motorvid28.py
BN = BigNeedle attached to inner shaft
SN = SmallNeedle attached to outer shaft
"""
__version__ = 1.240123

import time
from machine import Pin
from motorvid28 import motorVid28 as motor
from base import Log

# Motor pins A, B, C, D and Reed - 2 versions possibe
SNPINS  = (10,8,12,11,16)  # (21,19,20,15)
BNPINS  = (14,13,9,15,17)  # (17,18,16,14)
BN      = motor(BNPINS)
SN      = motor(SNPINS)

BNCW=1 ; BNCCW=0
BNSTEPS = 180  # only 180 steps when direct control by Pico
BNADJUST = 90   # recommended adjustment
BNSLICE  = 36  # recommended slices

SNCW=0 ; SNCCW=1
SNSTEPS = 180
SNADJUST = 13
SNSLICE  = 9

TIMESLEEP = 1 # sec 

def testreed() :  # Move manually the needles to verify Reed switches
    SNswitch =  Pin(SNPINS[4],Pin.IN,Pin.PULL_UP)
    BNswitch =  Pin(BNPINS[4],Pin.IN,Pin.PULL_UP)
    SN0 = SNswitch.value()
    BN0 = BNswitch.value()
    while True :
        SN = SNswitch.value()
        BN = BNswitch.value()
        Log("Reed SN {} Reed BN {}".format(SN,BN))
        time.sleep(1)
        if SN != SN0 or BN != BN0 :
            print("============")
            time.sleep(1)
            
def calibration(qty=1) :
    """Verify calibration with the reed switches"""
    BN.stop()
    SN.stop()
    for n in range (qty) :
        BN.calibrateNeedle(BNCW,BNADJUST,"Big")
        SN.calibrateNeedle(SNCW,SNADJUST,"Small")
        print("CALIBRATION - Test :",n+1)
        time.sleep(TIMESLEEP)

def simplemoves(qty=1,recalib=True,bnslice=1,snslice=1) :
    """Simple moves of both needles not simultaneously """
    if not recalib :
        BN.calibrateNeedle(BNCW,BNADJUST,"Big")
        SN.calibrateNeedle(SNCW,SNADJUST,"Small")
        
    for n in range (qty):
        if recalib :
            BN.calibrateNeedle(BNCW,BNADJUST,"Big")
        for i in range (bnslice) :
            BN.moveSteps(BNCW, BNSTEPS/bnslice)
            BN.stop()
            time.sleep(TIMESLEEP)

        if recalib :
            SN.calibrateNeedle(SNCW,SNADJUST,"Small")
        for i in range (snslice) :
            SN.moveSteps(SNCW, SNSTEPS/snslice)
            SN.stop()
            time.sleep(TIMESLEEP)

        print("SIMPLE MOVES - Test :",n+1)
        time.sleep(TIMESLEEP*3)

def complexmoves(qty=1) :       
        """Both needles are moving at relatively same speed..."""
        for n in range (qty):
            BN.calibrateNeedle(BNCW,BNADJUST+90,"Big")   # + 90 to align with BN
            SN.calibrateNeedle(SNCW,SNADJUST,"Small") 

            for i in range (BNSTEPS/10) : 
                BN.moveSteps(BNCW, 10)
                SN.moveSteps(SNCW, 10)
            time.sleep(TIMESLEEP*3)
            for i in range (BNSTEPS/3) : 
                BN.moveSteps(BNCW, 3)
                SN.moveSteps(BNCW, 3)
            time.sleep(TIMESLEEP*3)
            for i in range (BNSTEPS/5) : 
                BN.moveSteps(BNCW, 5)
                SN.moveSteps(SNCCW, 5)

        print("COMPLEX MOVES - Test :",n+1)
        time.sleep(TIMESLEEP*3)
                
def stop() :
    BN.stop()
    SN.stop()
    Log("End of tests. The needles should be in start position")

####################

if __name__ == '__main__': 
    Log("============ TEST MOTOR VID28 =================") 
    Log("Version :", __version__)
    #testreed()
    #calibration(5)
    simplemoves(100,True,36,10)  # 2 tests with recalibration and 36 slices for BN and 9 for SN
    #complexmoves(1)
    stop()


